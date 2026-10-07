"""NEW explicit inventory creation/check. Verification never silently reseals."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def members():
    return sorted(path for path in ROOT.rglob('*') if path.is_file()
                  and path.name != 'SOURCE-SEAL.json'
                  and not {'__pycache__', '.pytest_cache'} & set(path.relative_to(ROOT).parts)
                  and path.relative_to(ROOT).parts[0] != 'reports')


def inventory():
    return {str(path.relative_to(ROOT)): {'bytes': path.stat().st_size,
             'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for path in members()}


def check():
    path = ROOT / 'SOURCE-SEAL.json'
    sealed = json.loads(path.read_bytes())
    actual = inventory()
    if sealed['files'] != actual:
        missing = sorted(set(sealed['files']) - set(actual))
        extra = sorted(set(actual) - set(sealed['files']))
        changed = sorted(p for p in set(actual) & set(sealed['files']) if actual[p] != sealed['files'][p])
        raise ValueError(f'Fixed inventory mismatch: missing={missing}, extra={extra}, changed={changed}')
    return {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'files': len(actual), 'bytes': sum(x['bytes'] for x in actual.values())}


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--create']:
        data = {'kind': 'new fixed restoration source/input inventory; not historical hashes',
                'files': inventory()}
        (ROOT / 'SOURCE-SEAL.json').write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
    elif sys.argv[1:]:
        raise SystemExit('Use --create only for an intentional new local development seal')
    print(json.dumps(check(), indent=2))
