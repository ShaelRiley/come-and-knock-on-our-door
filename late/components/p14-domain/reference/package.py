"""NEW deterministic source/evidence packaging, excludes helpers and readback."""
from pathlib import Path
import json,hashlib,zipfile
W=Path(__file__).resolve().parent;out=W/'delivery';out.mkdir(exist_ok=True)
paths=[p for p in sorted(W.rglob('*')) if p.is_file() and not any(x in ('delivery','__pycache__','.library-current','probes') for x in p.relative_to(W).parts) and p.name!='PACKAGE-MANIFEST.json']
rows=[dict(path=str(p.relative_to(W)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]
m=W/'PACKAGE-MANIFEST.json';m.write_text(json.dumps({'schema':1,'scope':'Editable finite P14 reference package; no native/compiled acceptance','files':rows},indent=2)+'\n');paths.append(m)
p=out/'CaKoOD-P14-Reference-Reconstruction-20261007.zip'
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(paths):
  info=zipfile.ZipInfo('p14-reference-reconstruction/'+str(f.relative_to(W)),(2026,10,7,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,f.read_bytes())
print(json.dumps({'file':str(p.resolve()),'bytes':p.stat().st_size,'members':len(paths),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
