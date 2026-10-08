#!/usr/bin/env python3
"""Hash-check the public source closure and compile it in a new directory.

This verifies source/output identity only. It does not run or attest gameplay.
"""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent

def require(ok,reason):
 if not ok:raise RuntimeError(reason)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical_sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def verify_sources():
 require(not sys.flags.optimize,'Optimized Python is forbidden')
 source=H/'source';expected=json.loads((H/'SOURCE-MANIFEST.json').read_text())['files']
 found={}
 for p in sorted(source.rglob('*')):
  require(not p.is_symlink(),'Symlink in source closure: '+str(p.relative_to(source)))
  if p.is_file():found[str(p.relative_to(source))]={'sha256':sha(p),'bytes':p.stat().st_size,'executable':bool(p.stat().st_mode&0o111)}
 require(found==expected,'Public source membership, bytes, or executable mode changed')
 return source,found

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path);parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
 require(args.verify_only != (args.out is not None),'Choose exactly one of --verify-only or --out NEW_DIRECTORY')
 source,inputs=verify_sources()
 if args.verify_only:print('PASS_PUBLIC_SOURCE',len(inputs),'files');return
 out=args.out.resolve();require(not out.exists(),'Output directory must not exist')
 require(not out.is_relative_to(H),'Build outside the public component to keep its source-only boundary clean')
 expected=json.loads((H/'OUTPUT-PINS.json').read_text());shutil.copytree(source,out);(out/'src').mkdir()
 require(not (out/'build').exists() and not list((out/'src').iterdir()),'Cold start required')
 p=subprocess.run([sys.executable,'-B',str(out/'build.py')],cwd=out,capture_output=True,text=True)
 (out/'fresh-build.log').write_text(p.stdout+p.stderr)
 require(p.returncode==0,'Fresh build failed; see fresh-build.log in the output directory')
 B=out/'build/coherent'
 actual={n:sha(B/n) for n in expected['outputs']};require(actual==expected['outputs'],'Compiled/resource output identity mismatch')
 # Membership is checked as well as each pinned file; no extra module can hide.
 names={'compile-receipt.json','selector-list.json','resource.map','resource.000'}
 names.update(str(p.relative_to(B)) for d in ('compiled','verification-checkpoint/assets/resources') for p in (B/d).rglob('*') if p.is_file())
 require(names==set(expected['outputs']),'Output membership changed')
 sources={p.name:sha(p) for p in sorted((out/'src').glob('*.sc'))};require(sources==expected['sources'],'Derived source identity mismatch')
 require(sha(out/'selectors.json')==expected['selectors_sha256'],'Selector identity mismatch')
 abi=json.loads((B/'ABI-MAPPINGS.json').read_text())
 for mod in abi['modules'].values():
  for field in ('script','heap'):
   path=Path(mod['reference_layout'][field]);require(path==B/'compiled'/path.name,'Unexpected ABI reference path')
   mod['reference_layout'][field]='build/coherent/compiled/'+path.name
 require(canonical_sha(abi)==expected['normalized_abi_sha256'],'ABI changed beyond reference-path relocation')
 report={'status':'PASS_PUBLIC_SOURCE_COLD_REBUILD','source_only_start':True,'input_file_count':len(inputs),'exact_output_count':len(actual),'exact_source_count':len(sources),'outputs':actual,'sources':sources,'selectors_sha256':expected['selectors_sha256'],'normalized_abi_sha256':expected['normalized_abi_sha256'],'abi_exact_except_relocated_reference_paths':True,'coexistence_acceptance':'NOT_ASSERTED_BY_THIS_CHECK','native_acceptance':False,'runtime_package':False}
 (out/'PUBLIC-COLD-REBUILD.json').write_text(json.dumps(report,indent=2)+'\n')
 print(report['status'],len(sources),'sources',len(actual),'outputs; paired/native acceptance not asserted')
if __name__=='__main__':main()
