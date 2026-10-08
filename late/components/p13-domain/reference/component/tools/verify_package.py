"""NEW byte inventory verification for an extracted finite candidate."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parents[2]
def verify():
 m=json.loads((W/'PACKAGE-MANIFEST.json').read_text())
 for row in m['files']:
  p=W/row['path']
  if not p.is_file():raise RuntimeError('Missing packaged file '+row['path'])
  b=p.read_bytes()
  if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:raise RuntimeError('Changed packaged file '+row['path'])
 return len(m['files'])
if __name__=='__main__':print('PASS package bytes:',verify(),'; native acceptance: false')
