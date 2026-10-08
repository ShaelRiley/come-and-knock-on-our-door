"""Fail closed on changed immutable inputs, even with optimized Python."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent
def verify():
    rows=json.loads((H/'INPUT-INVENTORY.json').read_text())['files']
    for row in rows:
        p=H/row['path']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
            raise ValueError('Immutable input mismatch: '+row['path'])
    return len(rows)
if __name__=='__main__':print('PASS_INPUT_INVENTORY',verify())
