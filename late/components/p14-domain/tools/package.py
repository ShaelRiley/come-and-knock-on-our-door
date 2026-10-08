"""Deterministic finite checkpoint archive with exact payload inventory."""
from pathlib import Path
import hashlib,json,sys,zipfile
H=Path(__file__).resolve().parents[1]
EXCLUDE={'delivery','probes','relocated','__pycache__','.git'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 sys.path.insert(0,str(H))
 from verify_inputs import verify
 verify()
 stage=sys.argv[1]
 files=[p for p in sorted(H.rglob('*')) if p.is_file() and not set(p.relative_to(H).parts)&EXCLUDE and p.suffix not in ('.pyc',) and p!=H/'PACKAGE-MANIFEST.json']
 rows=[dict(path=str(p.relative_to(H)),bytes=p.stat().st_size,sha256=sha(p)) for p in files]
 frozen={r['path'] for r in json.loads((H/'INPUT-INVENTORY.json').read_text())['files']}
 missing=frozen-{r['path'] for r in rows}
 if missing:raise ValueError(('Archive omits frozen inputs',sorted(missing)))
 manifest=H/'PACKAGE-MANIFEST.json';manifest.write_text(json.dumps(dict(stage=stage,files=rows),indent=2)+'\n')
 out=H/'delivery/P14-Editable-Domain-Reconstruction-20261007.zip'
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in files+[manifest]:
   info=zipfile.ZipInfo(str(Path('p14-domain-reconstruction')/p.relative_to(H)),(2026,10,7,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(p.stat().st_mode&0xffff)<<16;z.writestr(info,p.read_bytes())
 result=dict(stage=stage,path=str(out),sha256=sha(out),bytes=out.stat().st_size,members=len(files)+1)
 (H/f'delivery/{stage}-archive.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
