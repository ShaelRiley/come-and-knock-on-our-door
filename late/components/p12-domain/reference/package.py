"""Create finite, deterministic review package; excludes recursive probes/builds."""
from pathlib import Path
import hashlib,json,zipfile
W=Path(__file__).resolve().parent

def files():
 items=[]
 for name in ('component','historical','provenance','evidence'):
  items.extend(p for p in (W/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.zip'))
 items.extend(W/n for n in ('README.md','STATUS.json','package.py','freeze_inputs.py'))
 if (W/'probes').exists():items.extend((W/'probes').glob('*/*.log'))
 return sorted(set(items),key=lambda p:str(p.relative_to(W)))

def main():
 rows=[]
 for p in files():
  b=p.read_bytes();rows.append(dict(path=str(p.relative_to(W)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 manifest=W/'PACKAGE-MANIFEST.json';manifest.write_text(json.dumps(dict(scope='Finite P12 reference reconstruction review candidate; every included payload enumerated',files=rows),indent=2)+'\n')
 out=W/'delivery/P12-Reference-Reconstruction-Review01.zip';out.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  for p in [*files(),manifest]:
   info=zipfile.ZipInfo('p12-reference-reconstruction/'+str(p.relative_to(W)),date_time=(2026,10,7,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
   z.writestr(info,p.read_bytes())
 print(json.dumps(dict(file=str(out),bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),payloads=len(rows),members=len(rows)+1)))
if __name__=='__main__':main()
