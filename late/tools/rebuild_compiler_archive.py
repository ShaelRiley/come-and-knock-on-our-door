#!/usr/bin/env python3
"""Rebuild the P11 packaging-test ZIP from the existing editable198-file closure."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[2]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out.resolve()
 if out.exists() or ROOT==out or ROOT in out.parents:raise ValueError('Choose a new path outside the source tree')
 maps=json.loads((ROOT/'late/manifests/COMPONENTS.json').read_text());source=maps['p12-domain']['files']
 def read(name):
  row=source[name];p=PurePosixPath(row['from'])
  if p.is_absolute() or '..' in p.parts:raise ValueError('Unsafe mapping')
  raw=(ROOT/p).read_bytes()
  if sha(raw)!=row['sha256'] or len(raw)!=row['bytes']:raise ValueError('Changed compiler input '+name)
  return raw
 manifest=read('toolchain/SOURCE-MANIFEST.json');files=json.loads(manifest)['files']
 if len(files)!=198:raise ValueError('Expected approved198-file closure')
 out.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  members=[('SOURCE-MANIFEST.json',manifest)]+[('source/'+n,read('toolchain/source/'+n)) for n in sorted(files)]
  for n,raw in members:
   if n.startswith('source/') and sha(raw)!=files[n[7:]]:raise ValueError('Closure digest mismatch')
   info=zipfile.ZipInfo(n,(2026,10,7,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,raw,compresslevel=6)
 expected=maps['p11-scene']['files']['inputs/compiler-source.zip'];raw=out.read_bytes()
 if sha(raw)!=expected['sha256'] or len(raw)!=expected['bytes']:raise ValueError('Derived archive differs from this edition')
 with zipfile.ZipFile(out) as z:
  if len(z.infolist())!=199 or z.testzip() is not None:raise ValueError('Invalid closure archive')
 print(json.dumps({'status':'PASS_EXACT_DETERMINISTIC_COMPILER_ARCHIVE','members':199,'source_files':198,'sha256':sha(raw),'bytes':len(raw),'compiler_bootstrap_performed':False}))
if __name__=='__main__':main()
