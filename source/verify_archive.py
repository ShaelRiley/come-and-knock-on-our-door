#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
P=Path(__file__).resolve().parent;O=P/'ARCHIVE-CHECK.json';O.write_text('{"status":"RUNNING"}\n')
def require(ok,message):
 if not ok:raise RuntimeError(message)
try:
 require(not sys.flags.optimize,'Optimized archive checks are forbidden')
 membership=P/'ARCHIVE-MEMBERS.json'
 require(hashlib.sha256(membership.read_bytes()).hexdigest()=='2b06ec5e845a40fa5500a991c7aa2acd13a621954fe51cab154c7d5584d1e8b4','Archive membership identity changed')
 expected=json.loads(membership.read_text());require(len(expected)==1442 and len(expected)==len(set(expected)),'Archive member extent changed')
 rows={}
 for line in (P/'SHA256SUMS').read_text().splitlines():
  digest,name=line.split('  ',1);path=Path(name)
  require(name not in rows and len(digest)==64 and not path.is_absolute() and '..' not in path.parts,'Invalid checksum entry')
  rows[name]=digest
 require(set(rows)==set(expected),'Missing/extra checksum inventory')
 actual={str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and str(p.relative_to(P)) not in ('ARCHIVE-CHECK.json','LAST-REBUILD.json')}
 require(actual==set(expected)|{'SHA256SUMS'},'Unsealed source-view member')
 for name,digest in rows.items():
  p=P/name;require(p.is_file() and not p.is_symlink(),'Missing/nonregular archive input '+name)
  require(hashlib.sha256(p.read_bytes()).hexdigest()==digest,'Archive bytes differ: '+name)
 O.write_text(json.dumps({'status':'PASS_ARCHIVE_IDENTITY','immutable_files':len(rows),'native_acceptance':False},indent=2)+'\n');print(O.read_text())
except BaseException as e:
 O.write_text(json.dumps({'status':'FAIL','error':str(e),'native_acceptance':False})+'\n');raise
