"""Verify every vendored input without reading its former absolute source path."""
from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[2]
def verify():
    entries=json.loads((ROOT/'provenance/input-inventory.json').read_text())
    if len(entries) != 43:
        raise RuntimeError('Incomplete input inventory')
    for entry in entries:
        path=ROOT/entry['target'];data=path.read_bytes()
        if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
            raise RuntimeError('Vendored input mismatch: '+entry['target'])
    return len(entries)
if __name__=='__main__':print('VERIFIED_INPUTS='+str(verify()))
