#!/usr/bin/env python3
"""Fresh isolated P11 source compile. This is not a production/runtime package."""
from pathlib import Path
import hashlib
import json
import shutil
import struct
import subprocess
import sys

sys.dont_write_bytecode = True
H = Path(__file__).resolve().parent
B = H / 'build/isolated'
COMPILER_SHA256 = '608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e'
sys.path.insert(0, str(H / 'tools'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def build():
    from verify_source import verify
    verify()
    dump(B / 'compile-receipt.json', {'status': 'BUILDING', 'native_acceptance': False})
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is forbidden')
    from domain_metadata import declarations, selector_map
    from extract_sci11 import extract
    import pack
    compiler = H / 'toolchain/scicompile'
    if sha(compiler) != COMPILER_SHA256:
        raise RuntimeError('Pinned compiler identity mismatch')
    for row in json.loads((H / 'tools/ACCEPTED-HELPERS.json').read_text())['files']:
        if sha(H / row['destination']) != row['sha256']:
            raise RuntimeError(('Accepted evaluator/helper changed', row['destination']))
    sources = {0: H / 'tools/compiler-main.sc', 993: H / 'src/module993.sc'}
    source_texts = {number: path.read_text() for number, path in sources.items()}
    schema_hash = sha(H / 'manifest.json') if (H / 'manifest.json').exists() else None
    selectors = selector_map(source_texts.values())
    pack.SELECTORS = selectors
    owners = [0, 993]
    resources = {(6, 996): struct.pack('<4H', 0, 0, 0, 993),
                 (6, 997): pack.selector_resource()}
    pack.pack_resources(resources, B)
    pack.validate_resources(B)
    (B / 'src').mkdir(exist_ok=True)
    (B / 'compiled').mkdir(exist_ok=True)
    for stale in (B / 'src').glob('*.sco'):
        stale.unlink()
    for number, original in sources.items():
        (B / 'src' / ('main.sc' if number == 0 else f'module{number}.sc')).write_text(source_texts[number])
    (B / 'game.ini').write_text('[Game]\nName=P11 isolated domain\nLanguage=sci\n[Script]\nn000=main\nn993=module993\n')
    selector_list = [dict(name=k, selector_id=v) for k, v in sorted(selectors.items(), key=lambda x: x[1])]
    dump(B / 'selectors.json', selectors)
    dump(B / 'selector-list.json', selector_list)
    abi = dict(selectors=selector_list, modules={})
    rows = []
    for number, original in sources.items():
        source = B / 'src' / ('main.sc' if number == 0 else f'module{number}.sc')
        script = B / f'compiled/{number}.scr.bin'
        heap = Path(str(script) + '.hep')
        script.unlink(missing_ok=True)
        heap.unlink(missing_ok=True)
        result = subprocess.run([str(compiler), '--version', 'sci11', str(B), str(source), str(script)], capture_output=True, text=True)
        log = result.stdout + result.stderr
        (B / f'compile-{number}.log').write_text(log)
        if result.returncode or '[error]' in log or not script.exists() or not heap.exists():
            raise RuntimeError(('Compiler failed', number, log))
        layout = extract(script, heap, B / 'selector-list.json')
        locals_ = declarations(source.read_text())
        if sum(a['word_count'] for a in locals_) != layout['locals_word_count']:
            raise RuntimeError(('Local declaration/layout mismatch', number))
        for array in locals_:
            start, count = array['word_offset'], array['word_count']
            actual = layout['locals'][start:start+count]
            if [v & 65535 for v in array['initial_words']] != actual:
                raise RuntimeError(('Compiled local initializer mismatch', number, array['name']))
            array['initial_words'] = actual
        classes = [dict(name=o['name'], properties=o['properties'], methods=o['methods']) for o in layout['objects'] if o['is_class']]
        abi['modules'][str(number)] = dict(source=str(original.relative_to(H)), sha256=sha(source),
                local_words=layout['locals_word_count'], locals=locals_, classes=classes, reference_layout=layout)
        combined = script.stat().st_size + heap.stat().st_size + (2 if script.stat().st_size & 2 else 0)
        if combined > 65535:
            raise RuntimeError(('SCI16 resource budget exceeded', number, combined))
        rows.append(dict(module=number, source_sha256=sha(source), script_sha256=sha(script),
                         heap_sha256=sha(heap), combined_bytes=combined,
                         class_species=[o['species'] for o in layout['objects'] if o['is_class']]))
        dump(B / f'layout-{number}.json', layout)
    domain = abi['modules']['993']['reference_layout']
    classes = [o for o in domain['objects'] if o['is_class']]
    instances = [o for o in domain['objects'] if not o['is_class']]
    if len(classes) != 1 or classes[0]['name'] != 'P11State' or classes[0]['species'] != 1:
        raise RuntimeError('Standalone P11State must occupy species 1')
    instance = next((o for o in instances if o['name'] == 'p11State'), None)
    if instance is None or instance['superclass'] != 1 or domain['exports'] != [instance['heap_offset']]:
        raise RuntimeError('p11State must be sole export at index 0')
    checkpoint = B / 'verification-checkpoint'
    dump(checkpoint / 'reference/resources.json', [])
    dump(checkpoint / 'source-provenance/ABI-MAPPINGS.json', abi)
    dump(B / 'ABI-MAPPINGS.json', abi)
    for row in rows:
        if sha(sources[row['module']]) != row['source_sha256']:
            raise RuntimeError(('Source changed during compile', row['module']))
    if schema_hash is not None and sha(H / 'manifest.json') != schema_hash:
        raise RuntimeError('Schema changed during compile')
    receipt = dict(status='PASS_FRESH_COMPILE', modules=rows, class_owners=owners,
                   isolated_species=1, production_reserved_species=15, production_integrated=False,
                   compiler_sha256=sha(compiler), native_acceptance=False, runtime_package=False,
                   selector_sha256=sha(B / 'selector-list.json'), abi_sha256=sha(B / 'ABI-MAPPINGS.json'),
                   schema_sha256=schema_hash)
    dump(B / 'compile-receipt.json', receipt)
    print('PASS_FRESH_COMPILE', [(r['module'], r['combined_bytes']) for r in rows])
    return receipt


if __name__ == '__main__':
    try:
        build()
    except BaseException as exc:
        dump(B / 'compile-receipt.json', dict(status='FAILED', reason=str(exc), native_acceptance=False))
        raise
