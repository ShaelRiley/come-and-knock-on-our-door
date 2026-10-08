#!/usr/bin/env python3
"""Make a deterministic source-only ZIP from the exact verified WIP tree."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
sys.dont_write_bytecode=True
import verify_source
ROOT=verify_source.ROOT
def main():
 if len(sys.argv)!=2:raise SystemExit('Usage: python3 progress/package.py /absolute/new-source.zip')
 out=Path(sys.argv[1]).resolve()
 if out.exists() or out==ROOT or ROOT in out.parents:raise RuntimeError('Choose a new archive outside the source tree')
 verify_source.main();rows=verify_source.inventory();manifest=ROOT/verify_source.MANIFEST
 rows[verify_source.MANIFEST]={'sha256':verify_source.sha(manifest),'bytes':manifest.stat().st_size,'mode':manifest.stat().st_mode&0o777}
 out.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,row in sorted(rows.items()):
   p=ROOT/n
   if verify_source.sha(p)!=row['sha256']:raise RuntimeError('Source changed during packaging')
   i=zipfile.ZipInfo('CaKoOD-WIP-Source-20261007-r3/'+n,date_time=(2026,10,7,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=(0o100000|row['mode'])<<16;z.writestr(i,p.read_bytes(),compresslevel=6)
 with zipfile.ZipFile(out) as z:
  if z.testzip() is not None or len(z.infolist())!=len(rows):raise RuntimeError('ZIP inventory/CRC mismatch')
  for n,row in rows.items():
   i=z.getinfo('CaKoOD-WIP-Source-20261007-r3/'+n)
   if hashlib.sha256(z.read(i)).hexdigest()!=row['sha256'] or (i.external_attr>>16)&0o777!=row['mode']:raise RuntimeError('ZIP bytes/mode differ')
 verify_source.main()
 print(json.dumps({'archive':out.name,'sha256':verify_source.sha(out),'bytes':out.stat().st_size,'files':len(rows),'native_acceptance':False,'playable_release':False},sort_keys=True))
if __name__=='__main__':main()
