#!/usr/bin/env python3
"""Verify all archived payload hashes and refuse unexpected files."""
from pathlib import Path
import hashlib,json,sys
H=Path(__file__).resolve().parents[1]
def main():
    root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else H
    m=json.loads((root/'PACKAGE-MANIFEST.json').read_text())
    expected=set()
    for row in m['files']:
        rel=Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts or row['path'] in expected:raise ValueError('Invalid archive manifest path')
        expected.add(row['path']);p=root/rel
        if not p.is_file() or p.stat().st_size!=row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
            raise ValueError('Package member differs: '+row['path'])
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and not any(n in ('delivery','probes','relocated','__pycache__') for n in p.relative_to(root).parts) and p.suffix not in ('.pyc',) and p!=root/'PACKAGE-MANIFEST.json'}
    if actual!=expected:raise ValueError(('Unexpected/missing package members',sorted(actual-expected),sorted(expected-actual)))
    frozen={r['path'] for r in json.loads((root/'INPUT-INVENTORY.json').read_text())['files']}
    if not frozen<=expected:raise ValueError(('Archive omits frozen inputs',sorted(frozen-expected)))
    import importlib.util
    spec=importlib.util.spec_from_file_location('package_input_guard',root/'verify_inputs.py')
    guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard);guard.verify()
    print('PASS_PACKAGE_MANIFEST',len(expected),'members')
if __name__=='__main__':main()
