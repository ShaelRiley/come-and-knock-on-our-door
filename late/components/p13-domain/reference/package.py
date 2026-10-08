"""NEW reusable source archive, excluding transient caches and recursive deliveries."""
from pathlib import Path
import json,hashlib,zipfile
W=Path(__file__).resolve().parent;D=W/'delivery';D.mkdir(exist_ok=True)
files=[]
for p in sorted(W.rglob('*')):
 rel=p.relative_to(W)
 if p.is_file() and not {'checkpoints','delivery','probes','__pycache__'}&set(rel.parts) and p.name!='PACKAGE-MANIFEST.json':
  raw=p.read_bytes();files.append(dict(path=str(rel),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
(W/'PACKAGE-MANIFEST.json').write_text(json.dumps(dict(scope='P13 finite reference/source candidate only',files=files),indent=2)+'\n')
p=D/'P13-Reference-Reconstruction-Review01.zip'
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:
 for row in files:z.write(W/row['path'],'p13-reference-reconstruction/'+row['path'])
 z.write(W/'PACKAGE-MANIFEST.json','p13-reference-reconstruction/PACKAGE-MANIFEST.json')
print(json.dumps(dict(path=str(p.resolve()),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),files=len(files)+1),indent=2))
