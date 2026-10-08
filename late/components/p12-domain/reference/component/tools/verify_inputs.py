"""Scoped fail-closed guards for original source, current authority, dependencies."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
def verify():
 rows=json.loads((ROOT/'provenance/input-inventory.json').read_text())
 for row in rows:
  path=ROOT/row['target']
  if not path.is_file():raise RuntimeError('Missing pinned input: '+row['target'])
  raw=path.read_bytes()
  if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:
   raise RuntimeError('Changed pinned input: '+row['target'])
 prefix=(ROOT/'historical/literal-read-partial/cakood/p12_model.py.part').read_bytes()
 tail=(ROOT/'provenance/reconstructed-tail.py.txt').read_bytes()
 model=(ROOT/'component/cakood/p12_model.py').read_bytes()
 if model!=prefix+tail or b'NEW RECONSTRUCTION' not in tail:
  raise RuntimeError('P12 must be literal complete prefix plus labeled new tail')
 return len(rows)
if __name__=='__main__':print('Pinned inputs:',verify())
