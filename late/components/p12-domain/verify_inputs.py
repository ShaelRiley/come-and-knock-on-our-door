"""Fail closed on changed immutable inputs, even with optimized Python."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent
R2_PINS={
 'SOURCE-MANIFEST.json':'ff596620dbfc140289fe7ca2b1d1eb39a554ac6c9a20cb626e6e70e3f0e26d9d',
 'COMPILER-DEPENDENCY-CLOSURE.json':'8f735116ee63ca6706631a93ae9cd0ae6c912ff153691cb1f8e2ac356ed293d8',
 'README.md':'82724b5689801c6d627b8660fb91c476fe6600c98fe49ee0bb4f869be94a865f',
 'scicompile':'608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e'}
def verify_compiler_closure():
    root=H/'toolchain'
    for name,digest in R2_PINS.items():
        p=root/name
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
            raise ValueError('Audited R2 compiler metadata mismatch: '+name)
    m=json.loads((root/'SOURCE-MANIFEST.json').read_text())['files']
    expected={'source/'+p for p in m}|set(R2_PINS)
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    if len(m)!=198 or actual!=expected:
        raise ValueError('Audited R2 compiler closure membership mismatch')
    for name,digest in m.items():
        if hashlib.sha256((root/'source'/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Audited R2 compiler source mismatch: '+name)
    c=json.loads((root/'COMPILER-DEPENDENCY-CLOSURE.json').read_text())
    if (c['translation_unit_count'],c['observed_source_header_count'],c['vendor_source_header_count'])!=(69,179,128):
        raise ValueError('Audited R2 compiler dependency counts mismatch')
    rows=c['source_header_files'];names={r['path'] for r in rows}
    if len(rows)!=179 or len(names)!=179 or sum(p.startswith('vendor/') for p in names)!=128:
        raise ValueError('Audited R2 compiler dependency membership mismatch')
    for r in rows:
        p=root/c['source_base']/r['path']
        if p.stat().st_size!=r['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:
            raise ValueError('Audited R2 compiler dependency changed: '+r['path'])
    units=c['translation_units']
    if len(units)!=69 or len({u['source'] for u in units})!=69 or {p for u in units for p in u['dependencies']}!=names:
        raise ValueError('Audited R2 translation-unit closure mismatch')
    return {'source_files':198,'build_inputs':179,'vendor_inputs':128,'translation_units':69}
def verify():
    rows=json.loads((H/'INPUT-INVENTORY.json').read_text())['files']
    for row in rows:
        p=H/row['path']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
            raise ValueError('Immutable input mismatch: '+row['path'])
    verify_compiler_closure()
    return len(rows)
if __name__=='__main__':print('PASS_INPUT_INVENTORY',verify())
