"""NEW fail-closed current authority and frozen dependency admission."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parents[2]
def verify():
 rows=json.loads((W/'provenance/input-inventory.json').read_text())
 for r in rows:
  if not r['pinned']:continue
  p=W/r['target']
  if not p.is_file():raise RuntimeError('Missing pinned input: '+r['target'])
  b=p.read_bytes()
  if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:raise RuntimeError('Changed pinned input: '+r['target'])
 return sum(r['pinned'] for r in rows)
if __name__=='__main__':print('Pinned inputs:',verify())
