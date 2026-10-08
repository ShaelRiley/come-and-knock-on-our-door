"""Fail closed on copied literal, canonical or dependency byte changes."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

def verify():
    entries = json.loads((ROOT/'provenance/input-inventory.json').read_text())
    for entry in entries:
        path = ROOT/entry['target']
        if not path.is_file():
            raise RuntimeError('Missing pinned input: '+entry['target'])
        data = path.read_bytes()
        if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise RuntimeError('Changed pinned input: '+entry['target'])
    partial = (ROOT/'historical/dependencies/p10-partial-prefix.py.txt').read_bytes()
    complete = (ROOT/'component/cakood/p10_model.py').read_bytes()
    if not complete.startswith(partial):
        raise RuntimeError('Literal P10 shared-caption prefix was altered')
    # Full P10 reconstruction has a deliberate marker following literal prefix.
    if len(complete) <= len(partial) or b'RECONSTRUCT' not in complete[len(partial):].upper():
        raise RuntimeError('Partial P10 was incorrectly installed as a full model')
    return len(entries)

if __name__ == '__main__':
    print('VERIFIED_PINNED_INPUTS='+str(verify()))
