#!/usr/bin/env python3
"""Cold-build and identify the full-campaign WIP. No runtime or gameplay is run."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent

def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical_sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def files(root):
 result={}
 for p in sorted(root.rglob('*')):
  require(not p.is_symlink(),'Unexpected symlink: '+str(p.relative_to(root)))
  if p.is_file():result[str(p.relative_to(root))]={'sha256':sha(p),'bytes':p.stat().st_size,'executable':bool(p.stat().st_mode&0o111)}
 return result

def verify_inputs():
 require(not sys.flags.optimize,'Optimized Python is not supported')
 expected=json.loads((H/'SOURCE-MANIFEST.json').read_text())['files']
 actual=files(H/'source');require(actual==expected,'Input membership, bytes or executable modes differ')
 return actual

def check_outputs(out):
 pins=json.loads((H/'OUTPUT-PINS.json').read_text());B=out/'build/coherent'
 actual={n:sha(B/n) for n in pins['outputs']};require(actual==pins['outputs'],'Rebuilt output identity mismatch')
 names={'compile-receipt.json','selector-list.json','selector-aliases.json','selector-alias-ledger.json','resource.map','resource.000','manifest.json','game.ini','verification-checkpoint/reference/resources.json'}
 names.update(str(p.relative_to(B)) for d in ['compiled','src','verification-checkpoint/assets/resources','speech'] for p in (B/d).rglob('*') if p.is_file() and p.suffix!='.sco')
 require(names==set(pins['outputs']),'Rebuilt output membership mismatch')
 actual_src={p.name:sha(p) for p in (out/'src').glob('*.sc')}
 require(actual_src==pins['canonical_sources'],'Canonical source identity mismatch')
 require(sha(out/'selectors.json')==pins['selectors_sha256'],'Selector identity mismatch')
 abi=json.loads((B/'ABI-MAPPINGS.json').read_text())
 require(abi==json.loads((B/'verification-checkpoint/source-provenance/ABI-MAPPINGS.json').read_text()),'ABI copies differ')
 for module in abi['modules'].values():
  for key in ['script','heap']:
   path=Path(module['reference_layout'][key]);require(path==B/'compiled'/path.name,'Unexpected ABI path')
   module['reference_layout'][key]='build/coherent/compiled/'+path.name
 require(canonical_sha(abi)==pins['normalized_abi_sha256'],'ABI differs beyond relocation')
 require(all(p.is_file() and not p.is_symlink() for p in (out/'stage/game').iterdir()),'Non-file or symlink in staged game')
 game={p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in (out/'stage/game').iterdir() if p.is_file()}
 require(game==pins['stage_files'],'Staged game membership or bytes differ')
 return {'status':'PASS_PUBLIC_OUTPUT_IDENTITY','source_manifest_sha256':sha(H/'SOURCE-MANIFEST.json'),'source_input_files':len(files(H/'source')),'compile_receipt_sha256':pins['compile_receipt_sha256'],'canonical_sources':len(actual_src),'exact_build_outputs':len(actual),'exact_current_stage_files':len(game),'normalized_abi_sha256':pins['normalized_abi_sha256'],'all_stage_file_bytes_identical':True,'source_only_start':'NOT_ASSERTED_BY_OUTPUT_IDENTITY_CHECK','compiled_scripts_copied_as_inputs':False,'runtime_bundled':False,'full_causal_route_acceptance':False,'native_acceptance':False}

def main():
 ap=argparse.ArgumentParser(description=__doc__);g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--out',type=Path);g.add_argument('--verify-only',action='store_true');g.add_argument('--check-existing',type=Path);a=ap.parse_args()
 inputs=verify_inputs()
 if a.verify_only:print('PASS_PUBLIC_SOURCE',len(inputs),'files');return
 if a.check_existing:report=check_outputs(a.check_existing.resolve())
 else:
  out=a.out.resolve();require(not out.exists(),'Output directory must not exist');require(not out.is_relative_to(H),'Build outside this source component')
  shutil.copytree(H/'source',out)
  require(not (out/'build').exists() and not (out/'stage').exists(),'Cold output required')
  for script in ['build.py','stage.py']:
   run=subprocess.run([sys.executable,'-B',str(out/script)],cwd=out,capture_output=True,text=True)
   (out/(script+'.log')).write_text(run.stdout+run.stderr)
   require(run.returncode==0,'Failed '+script+'; see its log in the output directory')
  report=check_outputs(out);report.update(status='PASS_PUBLIC_CANONICAL_COLD_REBUILD',source_only_start=True);(out/'PUBLIC-COLD-REBUILD.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
