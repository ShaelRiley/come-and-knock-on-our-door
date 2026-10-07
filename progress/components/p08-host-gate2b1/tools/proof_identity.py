"""Portable, read-only identities shared by verification and packaging.

Names are root-relative POSIX paths; directory links are never followed. Python
cache files are not proof inputs. A proof is a byte identity, not a signature or
an independent claim that trusted tests cover native gameplay.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import re
import stat

SOURCE_PIN = '281f11335655a1cb89cf3499ba09c71aa193f814b75c6c4948deb44641aaebb1'
COMPILER_PIN = '608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e'
DOMAIN_PIN = '947541e4376ca2f73dd497a8ce2885c52276cfc912af7fe98efd81da6b12f956'
P06_SEAL_PIN = 'a2bc8b94db0c2e4d4a4807efced51ff055b42f2b164c7de944d24cd0cce43c74'
P06_DELTA_PIN = '76fd9a6d84013aae5ded12b4117ebf6822ba7f9172ea8d56351add4e4802b8bc'
P06_MOUTH_PIN = '508234a816fa0f1e4b0cd793224eb727fa6074670093632f55b68faa22a87726'
P06_BEFORE_987 = '439e25743f14a1a277a7e064e184a113981dff6da985c86b58169ccb4b30d5af'
P06_AFTER_987 = '9384e6f9a31799dd1f69756c483d207537c16c462754fe57bc5d829bd69f21e3'
P06_MOUTH_COMPILE = '628117379862d95a273c1bfd7525d65c1d586151a10042eff1a75ee9d9a130ba'
P06_BEFORE_MAIN = '4058298dc9f1cfafa4d4cf655e0236d9dd1f9810a73e653ffa677fb88f98284a'
P06_AFTER_MAIN = 'e3b5fce42c97d3125b93de2a127072ae0b9bc00e8b7691a00f0c30e9e9e919c9'
P06_DELTA_COMPILE = '000ee8737deed3ec47a919b64858ad704af60d5d26955ced48fe1ccc62903867'
INPUT_DIRS = ('snapshot', 'toolchain', 'src', 'templates', 'generated', 'tests', 'tools', 'fixtures', 'integration-tests', 'inputs')
AUDIT_ROOT_EXECUTABLES = ('verify.py', 'stage.py', 'package.py')
ROOT_INPUTS = ('SOURCE-INPUTS.json', 'P06-BASE.json', 'selectors.json', 'build.py', 'derive.py', 'generate_routes.py', 'import_p06.py', 'import_p06_delta.py', 'import_p06_mouth.py') + AUDIT_ROOT_EXECUTABLES
DELIVERY_ROOTS = ('README.md', 'INTEGRATION-CONTRACT.md', 'PROVENANCE.md', 'NATIVE-FOLLOW-THROUGH.md', 'evidence/combined-mouth-probe.json', 'evidence/combined-mouth-probe.log', 'evidence/packaging-guards.json', 'evidence/packaging-guards.log', 'evidence/independent-review/r3/REVIEW.md', 'evidence/independent-review/r3/static-review.json', 'evidence/independent-review/r3/control-results.json', 'evidence/independent-review/r3/bunny-results.json', 'evidence/independent-review/r3/check_static.py', 'evidence/independent-review/r3/recheck_controls.py', 'evidence/independent-review/r3/recheck_bunny.py')
CACHE_DIRS = {'__pycache__', '.pytest_cache'}


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def safe_relative(name):
    require(isinstance(name, str) and bool(name), 'Empty/non-string member name')
    require('\\' not in name and ':' not in name and '\x00' not in name, 'Unsafe member name: ' + repr(name))
    p = PurePosixPath(name)
    require(not p.is_absolute() and p.as_posix() == name and all(x not in ('', '.', '..') for x in name.split('/')), 'Unsafe member name: ' + repr(name))
    return name


def checked_path(root, name):
    safe_relative(name)
    root = Path(root)
    require(not root.is_symlink() and root.is_dir(), 'Regular proof root required')
    p = root
    for part in PurePosixPath(name).parts:
        p = p / part
        require(not p.is_symlink(), 'Symlink forbidden: ' + name)
    require(p.is_file() and stat.S_ISREG(p.stat().st_mode), 'Regular file required: ' + name)
    return p


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + '\n').encode()


def digest_map(files):
    return sha_bytes(json.dumps(files, sort_keys=True, separators=(',', ':')).encode())


def load(root, name):
    # Duplicate JSON keys must not hide a path, test result, or resource.
    def pairs(rows):
        result = {}
        for k, v in rows:
            require(k not in result, 'Duplicate JSON key: ' + k)
            result[k] = v
        return result
    return json.loads(checked_path(root, name).read_text(), object_pairs_hook=pairs)


def paths_in(root, subdir):
    safe_relative(subdir)
    root = Path(root)
    require(not root.is_symlink() and root.is_dir(), 'Regular proof root required')
    base = root / subdir
    require(base.is_dir() and not base.is_symlink(), 'Regular directory required: ' + subdir)
    found = []
    for current, dirs, files in os.walk(base, followlinks=False):
        for name in list(dirs):
            p = Path(current) / name
            require(not p.is_symlink(), 'Directory symlink forbidden: ' + str(p.relative_to(root)))
            if name in CACHE_DIRS:
                dirs.remove(name)
        for name in files:
            p = Path(current) / name
            rel = p.relative_to(root).as_posix()
            checked_path(root, rel)
            if p.suffix in ('.pyc', '.pyo'):
                continue
            found.append(rel)
    return sorted(found)


def file_inventory(root, subdirs=(), root_files=()):
    names = list(root_files)
    for subdir in subdirs:
        names.extend(paths_in(root, subdir))
    require(len(names) == len(set(names)), 'Overlapping input inventory')
    return {name: sha(checked_path(root, name)) for name in sorted(names)}


def require_files(root, expected):
    require(isinstance(expected, dict) and bool(expected), 'Empty/invalid identity map')
    for name, expected_sha in expected.items():
        require(isinstance(expected_sha, str) and re.fullmatch('[a-f0-9]{64}', expected_sha), 'Invalid SHA256: ' + name)
        require(sha(checked_path(root, name)) == expected_sha, 'Byte identity changed: ' + name)


def proof_inputs(root):
    """Every executable harness, immutable input, readable source and build byte."""
    return file_inventory(root, INPUT_DIRS + ('build',), ROOT_INPUTS)


def delivery_inputs(root):
    return file_inventory(root, ('packaging-tests',), DELIVERY_ROOTS)


def validate_frozen(root):
    require(sha(checked_path(root, 'SOURCE-INPUTS.json')) == SOURCE_PIN, 'Frozen SOURCE-INPUTS authority changed')
    frozen = load(root, 'SOURCE-INPUTS.json')
    actual = file_inventory(root, ('snapshot', 'toolchain', 'inputs'))
    require(actual == frozen, 'Frozen source/resource/compiler/audio inventory or bytes changed')
    require(sha(checked_path(root, 'toolchain/scicompile')) == COMPILER_PIN, 'Pinned compiler changed')
    require(sha(checked_path(root, 'snapshot/domain/module988.sc')) == DOMAIN_PIN, 'Accepted P07 domain changed')
    require(sha(checked_path(root, 'snapshot/base/P06-HANDOFF-SEAL.json')) == P06_SEAL_PIN, 'P06 handoff changed')
    compiler = load(root, 'toolchain/SOURCE-MANIFEST.json')['files']
    require(file_inventory(root, ('toolchain/source',)) == {'toolchain/source/' + safe_relative(k): v for k, v in compiler.items()}, 'Compiler source manifest membership/bytes changed')
    speech = load(root, 'snapshot/SPEECH-INPUTS.json')
    require(set(paths_in(root, 'snapshot/speech')) == {'snapshot/speech/' + safe_relative(k) for k in speech}, 'Speech membership changed')
    for name, row in speech.items():
        p = checked_path(root, 'snapshot/speech/' + name)
        require(sha(p) == row['sha256'] and p.stat().st_size == row['bytes'], 'Speech changed: ' + name)
    validate_p06_authorities(root)
    validate_pre_review_fixture(root)
    return frozen


def archive_rows(root, identities):
    require_files(root, identities)
    return {name: {'sha256': digest, 'bytes': checked_path(root, name).stat().st_size, 'mode': 0o755 if name == 'toolchain/scicompile' else 0o644} for name, digest in sorted(identities.items())}


def guarded_main_reverse(after, delta):
    """One exact sealed replacement must reverse to the original whole-file SHA."""
    require(isinstance(after, bytes), 'Guarded Main must be bytes')
    old = delta['guard_before'].encode()
    new = delta['replacement_after'].encode()
    require(old and new and old != new and after.count(new) == 1, 'Main delta replacement guard missing or ambiguous')
    require(sha_bytes(after) == delta['after_main_sha256'], 'Main delta after identity differs')
    before = after.replace(new, old, 1)
    require(sha_bytes(before) == delta['before_main_sha256'], 'Main reverse delta does not equal original candidate1')
    return before


def validate_p06_unchanged_sources(root, original, mouth_before=None):
    for n in range(980, 988):
        name = 'src/module%d.sc' % n
        row = original['files'][name]
        path = checked_path(root, 'snapshot/base/' + Path(name).name)
        data = mouth_before if n == 987 and mouth_before is not None else path.read_bytes()
        require(len(data) == row['bytes'] and sha_bytes(data) == row['sha256'], 'Non-Main P06 base source changed: '+name)
    row = original['files']['selectors.json']
    path = checked_path(root, 'snapshot/base/selectors.json')
    require(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], 'P06 base selectors changed outside guarded delta')


def validate_historical_fixture(root, folder, manifest, original, count):
    require(isinstance(manifest, dict) and len(manifest) == count, 'Historical negative fixture count differs')
    require(set(paths_in(root, folder)) == {folder+'/'+safe_relative(n) for n in manifest}, 'Historical negative fixture membership differs')
    for name, digest in manifest.items():
        require(name in original['files'] and original['files'][name]['sha256'] == digest, 'Historical fixture is not a candidate1 sealed file: '+name)
        path = checked_path(root, folder+'/'+name)
        require(sha(path) == digest and path.stat().st_size == original['files'][name]['bytes'], 'Historical negative fixture bytes differ: '+name)


def validate_p06_authorities(root):
    root = Path(root)
    original_name = 'snapshot/base/P06-HANDOFF-SEAL.json'
    require(sha(checked_path(root, original_name)) == P06_SEAL_PIN, 'Original P06 candidate1 authority changed')
    original = load(root, original_name)
    prefix = 'snapshot/p06-inventory-fix-r2/'
    require(sha(checked_path(root, prefix+'DELTA-SEAL.json')) == P06_DELTA_PIN, 'P06 guarded delta seal changed')
    seal = load(root, prefix+'DELTA-SEAL.json')
    require(seal.get('status') == 'FROZEN_GUARDED_INVENTORY_FIX_R2' and seal.get('base_seal_sha256') == P06_SEAL_PIN and seal.get('native_acceptance') is False and seal.get('full_revision2_qa') == 'pending', 'P06 delta authority/status mismatch')
    require(set(paths_in(root, prefix.rstrip('/'))) == {prefix+'DELTA-SEAL.json'} | {prefix+safe_relative(n) for n in seal['files']}, 'P06 delta file membership differs')
    for name, row in seal['files'].items():
        path = checked_path(root, prefix+name)
        require(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], 'P06 delta payload changed: '+name)
    delta = load(root, prefix+'REVISION-2-DELTA.json')
    require(delta.get('status') == 'EXACT_GUARDED_MAIN_DELTA' and delta.get('before_main_sha256') == P06_BEFORE_MAIN and delta.get('after_main_sha256') == P06_AFTER_MAIN and delta.get('changed_methods') == ['p03HostUIItem'] and delta.get('selectors_unchanged') is True and delta.get('other_source_and_emitted_modules_unchanged') == list(range(980,988)) and delta.get('compile_receipt_sha256') == P06_DELTA_COMPILE and delta.get('native_acceptance') is False and delta.get('full_revision2_qa') == 'pending', 'P06 exact guarded delta contract differs')
    after = checked_path(root, 'snapshot/base/main.sc').read_bytes()
    require(after == checked_path(root, prefix+'src/main.sc').read_bytes(), 'Imported base Main differs from exact delta output')
    before = guarded_main_reverse(after, delta)
    require(original['files']['src/main.sc'] == {'sha256':P06_BEFORE_MAIN, 'bytes':len(before)}, 'Original Main handoff identity differs')
    mouth_before, mouth_provenance = validate_p06_mouth(root)
    validate_p06_unchanged_sources(root, original, mouth_before)
    fixture = load(root, 'snapshot/r1-fixture-manifest.json')
    validate_historical_fixture(root, 'inputs/r1', fixture, original, 95)
    require(checked_path(root, 'inputs/r1/src/main.sc').read_bytes() == before, 'Negative fixture Main is not reverse-guarded candidate1')
    old_compile = load(root, 'inputs/r1/build/coherent/compile-receipt.json')
    new_compile = load(root, prefix+'build/coherent/compile-receipt.json')
    require(sha(checked_path(root, prefix+'build/coherent/compile-receipt.json')) == P06_DELTA_COMPILE, 'Delta compile identity differs')
    expected_modules = list(range(980,988))+[0]
    require([r['module'] for r in old_compile['modules']] == [r['module'] for r in new_compile['modules']] == expected_modules, 'P06 delta compile module universe differs')
    require(new_compile['modules'][:-1] == old_compile['modules'][:-1], 'P06 non-Main compiled module changed by Main-only delta')
    require(new_compile['status'] == old_compile['status'] == 'PASS_FRESH_COMPILE' and new_compile['native_acceptance'] is False and new_compile['class_owners'] == old_compile['class_owners'] and new_compile['compiler_sha256'] == old_compile['compiler_sha256'] == COMPILER_PIN, 'P06 delta compile authority differs')
    main = new_compile['modules'][-1]
    require(main['source_sha256'] == P06_AFTER_MAIN and main['script_sha256'] == sha(checked_path(root, prefix+'build/coherent/compiled/0.scr.bin')) and main['heap_sha256'] == sha(checked_path(root, prefix+'build/coherent/compiled/0.scr.bin.hep')) and main['combined_bytes'] == delta['main_combined_bytes'] == 61752 and delta['main_headroom'] == 65535-61752, 'P06 delta Main compile bound differs')
    provenance = load(root, 'P06-BASE.json')
    require(provenance.get('applied_guarded_deltas') == [dict(seal_sha256=P06_DELTA_PIN, before_main_sha256=P06_BEFORE_MAIN, after_main_sha256=P06_AFTER_MAIN, compile_receipt_sha256=P06_DELTA_COMPILE, full_revision2_qa='pending'), mouth_provenance], 'P06 applied delta provenance differs')
    return dict(original_seal_sha256=P06_SEAL_PIN, applied_delta_seal_sha256=P06_DELTA_PIN, mouth_delta_seal_sha256=P06_MOUTH_PIN, historical_fixture_files=95, full_revision2_qa='pending')


def guarded_mouth_reverse(after, delta):
    adapted = dict(delta, before_main_sha256=delta['before_module987_sha256'], after_main_sha256=delta['after_module987_sha256'])
    return guarded_main_reverse(after, adapted)


def validate_p06_mouth(root):
    prefix = 'snapshot/p06-jackie-mouth-r3/'
    require(sha(checked_path(root, prefix+'DELTA-SEAL.json')) == P06_MOUTH_PIN, 'P06 mouth delta authority changed')
    seal = load(root, prefix+'DELTA-SEAL.json')
    require(seal.get('status') == 'FROZEN_GUARDED_P06_MOUTH_R3' and seal.get('native_acceptance') is False and seal.get('listening') is False, 'P06 mouth delta status differs')
    require(set(paths_in(root, prefix.rstrip('/'))) == {prefix+'DELTA-SEAL.json'} | {prefix+safe_relative(n) for n in seal['files']}, 'P06 mouth delta membership differs')
    for name,row in seal['files'].items():
        path = checked_path(root, prefix+name)
        require(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], 'P06 mouth delta payload differs: '+name)
    delta = load(root, prefix+'PRESENTATION-DELTA.json')
    require(delta.get('status') == 'EXACT_GUARDED_PRESENTATION_ONLY_DELTA' and delta.get('before_module987_sha256') == P06_BEFORE_987 and delta.get('after_module987_sha256') == P06_AFTER_987 and delta.get('changed_methods') == ['h6DrawJack'] and delta.get('selectors_unchanged') is True and delta.get('state_or_publication_changes') is False and delta.get('domain_methods_unchanged') == 105 and delta.get('compile_receipt_sha256') == P06_MOUTH_COMPILE and delta.get('native_acceptance') is False and delta.get('listening') is False, 'P06 mouth contract differs')
    after = checked_path(root, 'snapshot/base/module987.sc').read_bytes()
    require(after == checked_path(root, prefix+'src/module987.sc').read_bytes(), 'Imported module987 differs from sealed output')
    before = guarded_mouth_reverse(after, delta)
    require(checked_path(root, 'snapshot/base/ABI-MAPPINGS.json').read_bytes() == checked_path(root, prefix+'build/coherent/ABI-MAPPINGS.json').read_bytes(), 'Imported P06 ABI differs')
    old = load(root, 'snapshot/p06-inventory-fix-r2/build/coherent/compile-receipt.json')
    new = load(root, prefix+'build/coherent/compile-receipt.json')
    require(sha(checked_path(root, prefix+'build/coherent/compile-receipt.json')) == P06_MOUTH_COMPILE, 'P06 mouth compile differs')
    require(new['status'] == 'PASS_FRESH_COMPILE' and new['class_owners'] == old['class_owners'] and new['compiler_sha256'] == COMPILER_PIN and new['native_acceptance'] is False and [r['module'] for r in new['modules']] == [r['module'] for r in old['modules']], 'P06 mouth compile universe differs')
    require([r for r in new['modules'] if r['module'] != 987] == [r for r in old['modules'] if r['module'] != 987], 'P06 mouth delta changed another emitted module')
    row = next(r for r in new['modules'] if r['module'] == 987)
    require(row['source_sha256'] == P06_AFTER_987 and row['script_sha256'] == sha(checked_path(root, prefix+'build/coherent/compiled/987.scr.bin')) and row['heap_sha256'] == sha(checked_path(root, prefix+'build/coherent/compiled/987.scr.bin.hep')), 'P06 mouth emitted identity differs')
    return before, dict(seal_sha256=P06_MOUTH_PIN, before_module987_sha256=P06_BEFORE_987, after_module987_sha256=P06_AFTER_987, compile_receipt_sha256=P06_MOUTH_COMPILE, focused_source_emitted_cases=18, combined_acceptance=False)


def validate_pre_review_fixture(root):
    manifest = load(root, 'snapshot/pre-review-fixture.json')
    require(manifest.get('classification') == 'UNACCEPTED historical negative oracle for independently reproduced P07 UI/restore defects' and manifest.get('compile_receipt_sha256') == '7b76d17d1295fce9ed60e643e143298e8ab3e2e453753ec2ee8d0c0674c3c46a', 'Historical P07 negative fixture classification differs')
    files = manifest['files']
    require(len(files) == 109 and file_inventory(root, ('inputs/pre-review',)) == {'inputs/pre-review/'+safe_relative(n):d for n,d in files.items()}, 'Historical P07 negative fixture membership or bytes differs')
    require(sha(checked_path(root, 'inputs/pre-review/build/coherent/compile-receipt.json')) == manifest['compile_receipt_sha256'], 'Historical P07 compile differs')
