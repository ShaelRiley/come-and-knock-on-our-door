"""NEW exact packaged member verification, including evidence and historical files."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parents[2]
def main():
 m=json.loads((W/'PACKAGE-MANIFEST.json').read_text())
 for r in m['files']:
  p=W/r['path']
  if not p.is_file() or p.stat().st_size!=r['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:raise RuntimeError('Package member changed '+r['path'])
 print('Exact package members:',len(m['files']))
if __name__=='__main__':main()
