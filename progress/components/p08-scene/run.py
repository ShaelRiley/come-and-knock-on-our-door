#!/usr/bin/env python3
"""Fail-closed supported entry point. Source sealing is an explicit maintainer action."""
from pathlib import Path,PurePosixPath
import sys,json,hashlib,subprocess,shutil,zipfile
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
STATUS=[H/'VERIFICATION.json',H/'evidence/current-status.json']
ROOT_DIRS={'inputs','tools','tests','generated','build','evidence','delivery','negative-probes','portability','regression-probes'}
CONTROL_FILES={'SOURCE-SEAL.json','OUTPUT-SEAL.json','GATE-SEAL.json','VERIFICATION.json'}
GATE_FILES={'evidence/negative-checks.json','evidence/tests-final.log','evidence/static-generation.log','evidence/portability.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def state(status,**kw):
 for p in STATUS+([H/'delivery/PACKAGE-STATUS.json'] if len(sys.argv)>1 and sys.argv[1]=='package' else []):dump(p,dict(status=status,native_acceptance=False,**kw))
def require(ok,why):
 if not ok:raise RuntimeError(why)
def layout_check():
 for p in H.iterdir():
  require(not p.is_symlink(),'Symlink root member rejected: '+p.name)
  if p.is_dir():require(p.name in ROOT_DIRS,'Unclassified root member: '+p.name)
  else:require(p.is_file(),'Non-regular root member: '+p.name)
 for dirname in ['inputs','tools','tests','generated','build']:
  base=H/dirname
  if base.exists():
   require(base.is_dir() and not base.is_symlink(),'Invalid classified directory: '+dirname)
   for p in base.rglob('*'):require(not p.is_symlink() and (p.is_dir() or p.is_file()),'Non-regular classified member: '+str(p.relative_to(H)))
def member_path(name):
 require(type(name) is str and name and '\\' not in name,'Unsafe package member')
 rel=PurePosixPath(name)
 require(not rel.is_absolute() and '..' not in rel.parts and '.' not in rel.parts and rel.as_posix()==name,'Unsafe package member: '+name)
 p=H/name
 for q in [p,*p.parents]:
  if q==H:break
  require(not q.is_symlink(),'Symlink package member: '+name)
 require(p.is_file(),'Missing regular package member: '+name)
 return p
def source_files():
 layout_check()
 roots=[p for p in H.iterdir() if p.is_file() and p.name not in CONTROL_FILES]
 files=roots+[p for d in ['inputs','tools','tests'] for p in (H/d).rglob('*') if p.is_file()]
 require(not any('__pycache__' in p.parts or p.suffix=='.pyc' for p in files),'Unexpected cached Python input')
 return {str(p.relative_to(H)):sha(p) for p in sorted(files)}
def output_files():
 files=[p for d in ['generated','build'] for p in (H/d).rglob('*') if p.is_file()]+[H/'evidence/compile-proof.json',H/'evidence/tests.json']
 return {str(p.relative_to(H)):sha(p) for p in sorted(files)}
def input_check():
 seal=json.loads((H/'INPUT-SEAL.json').read_text());actual={str(p.relative_to(H)):sha(p) for p in sorted((H/'inputs').rglob('*')) if p.is_file()};require(actual==seal['files'],'Frozen input inventory/hash differs')
def source_check():
 require(json.loads((H/'SOURCE-SEAL.json').read_text())['files']==source_files(),'Source inventory/hash mismatch; explicit maintainer reseal required');input_check()
def test_check():
 t=json.loads((H/'evidence/tests.json').read_text());expected=json.loads((H/'tests/EXPECTED-TESTS.json').read_text())
 require(t['status']=='PASS' and t['test_ids']==expected and t['tests']==len(expected) and len(expected)>0 and t['skipped']==t['expected_failures']==0,'Test result is not exact clean PASS')
def outputs_check():
 seal=json.loads((H/'OUTPUT-SEAL.json').read_text());require(seal['source_seal_sha256']==sha(H/'SOURCE-SEAL.json'),'Output belongs to another source seal');require(output_files()==seal['files'],'Output inventory/hash mismatch');test_check()
 from tools.resource_codec import decode
 native=H/'generated/fixture-game';decoded=decode((native/'resource.map').read_bytes(),(native/'resource.000').read_bytes());receipt=json.loads((H/'build/coherent/compile-receipt.json').read_text())
 require(receipt['status']=='PASS_FRESH_COMPILE','Compile receipt not PASS')
 for row in receipt['modules']:
  for t,part in [(2,'script'),(17,'heap')]:require(hashlib.sha256(decoded[t,row['module']]).hexdigest()==row[part+'_sha256'],'Sealed packer emitted identity mismatch')
 for n in [208]:require(decoded[3,n]==(H/f'generated/{n}.text.bin').read_bytes(),'Sealed new text mismatch')
 for n in [240,241,242,244]:require(decoded[3,n]==(H/f'generated/static/{n}.text.bin').read_bytes(),'Sealed static text mismatch')
def command(cmd,log):
 with (H/'evidence'/log).open('w') as stream:result=subprocess.run(cmd,cwd=H,stdout=stream,stderr=subprocess.STDOUT,text=True)
 require(result.returncode==0,'Failed '+str(cmd)+'; see '+log)
def rebuild():
 for d in ['generated','build']:
  if (H/d).exists():shutil.rmtree(H/d)
  (H/d).mkdir()
 (H/'OUTPUT-SEAL.json').unlink(missing_ok=True);(H/'GATE-SEAL.json').unlink(missing_ok=True)
 from generate import generate
 from extend import extend
 from build import build
 generate();extend();build();command([sys.executable,str(H/'tests/run_suite.py')],'tests-final.log');test_check();source_check()
 dump(H/'OUTPUT-SEAL.json',dict(schema=1,status='PASS_BOUND_OUTPUTS',source_seal_sha256=sha(H/'SOURCE-SEAL.json'),files=output_files(),native_acceptance=False))
 outputs_check()
def negative_check():
 negative=json.loads((H/'evidence/negative-checks.json').read_text());wanted=json.loads((H/'tests/EXPECTED-NEGATIVES.json').read_text());contract=json.loads((H/'tests/EXPECTED-NEGATIVE-RESULTS.json').read_text())
 require(type(negative) is dict and set(negative)=={'status','checks','tests','source_seal_sha256','output_seal_sha256','native_acceptance'},'Negative report schema mismatch')
 require(type(wanted) is list and wanted and len(set(wanted))==len(wanted) and list(contract)==wanted,'Negative expected inventory mismatch')
 require(negative['status']=='PASS' and type(negative['tests']) is int and negative['tests']==len(wanted) and negative['native_acceptance'] is False,'Negative gate inventory is not exact PASS')
 require(type(negative['checks']) is list and len(negative['checks'])==len(wanted),'Negative row inventory mismatch')
 for name,row in zip(wanted,negative['checks']):
  require(type(row) is dict and set(row)=={'name','returncode','clean_baseline_verified','rejection','stale_pass_cleared'},'Negative row schema mismatch: '+name)
  require(type(row['name']) is str and row['name']==name,'Negative row order/identity mismatch: '+name)
  require(type(row['returncode']) is int and row['returncode']==contract[name]['returncode'],'Negative row returncode mismatch: '+name)
  require(row['clean_baseline_verified'] is True and row['stale_pass_cleared'] is True,'Negative row success flags mismatch: '+name)
  require(type(row['rejection']) is str and row['rejection']==contract[name]['rejection'],'Negative row rejection mismatch: '+name)
 require(negative['source_seal_sha256']==sha(H/'SOURCE-SEAL.json') and negative['output_seal_sha256']==sha(H/'OUTPUT-SEAL.json'),'Negative gate belongs to different sealed inputs/outputs')
 return negative
def portability_check():
 p=json.loads((H/'evidence/portability.json').read_text())
 require(set(p)=={'status','source_seal_sha256','output_seal_sha256','stable_files','source_only_clean_relocation','all_ten_modules_recompiled','all_registered_tests_rerun','exact_generated_outputs','native_acceptance'},'Portability proof schema mismatch')
 require(p['status']=='PASS' and p['native_acceptance'] is False and type(p['stable_files']) is int and p['stable_files']>0,'Portability proof not PASS')
 require(all(p[k] is True for k in ['source_only_clean_relocation','all_ten_modules_recompiled','all_registered_tests_rerun','exact_generated_outputs']),'Portability claim mismatch')
 require(p['source_seal_sha256']==sha(H/'SOURCE-SEAL.json') and p['output_seal_sha256']==sha(H/'OUTPUT-SEAL.json'),'Portability proof stale')

def seal_negative_evidence():
 source_check();outputs_check();negative_check();portability_check()
 dump(H/'GATE-SEAL.json',dict(schema=1,kind='EXACT_NEGATIVE_GATE_EVIDENCE',source_seal_sha256=sha(H/'SOURCE-SEAL.json'),output_seal_sha256=sha(H/'OUTPUT-SEAL.json'),files={name:sha(member_path(name)) for name in sorted(GATE_FILES)},native_acceptance=False))
def gate_check():
 negative_check();portability_check();gate=json.loads((H/'GATE-SEAL.json').read_text())
 require(type(gate) is dict and set(gate)=={'schema','kind','source_seal_sha256','output_seal_sha256','files','native_acceptance'},'Gate seal schema mismatch')
 require(type(gate['schema']) is int and gate['schema']==1 and gate['kind']=='EXACT_NEGATIVE_GATE_EVIDENCE' and gate['native_acceptance'] is False,'Gate seal kind mismatch')
 require(gate['source_seal_sha256']==sha(H/'SOURCE-SEAL.json') and gate['output_seal_sha256']==sha(H/'OUTPUT-SEAL.json'),'Gate seal belongs to different sealed inputs/outputs')
 require(type(gate['files']) is dict and set(gate['files'])==GATE_FILES,'Gate evidence inventory mismatch')
 require(gate['files']=={name:sha(member_path(name)) for name in sorted(GATE_FILES)},'Gate evidence byte identity mismatch')
 return gate

def package_members():
 source_check();outputs_check();gate=gate_check();members={}
 for group in [json.loads((H/'SOURCE-SEAL.json').read_text())['files'],json.loads((H/'OUTPUT-SEAL.json').read_text())['files'],gate['files']]:
  for name,digest in group.items():
   require(name not in members or members[name]==digest,'Conflicting package member identity')
   require(sha(member_path(name))==digest,'Sealed package member changed: '+name);members[name]=digest
 for name in ['SOURCE-SEAL.json','OUTPUT-SEAL.json','GATE-SEAL.json']:members[name]=sha(member_path(name))
 return dict(sorted(members.items()))
def package():
 members=package_members()
 dest=H/'delivery/P08-Scene-Data-Reconstruction-20261006.zip';dest.parent.mkdir(exist_ok=True)
 staging=dest.with_suffix('.zip.tmp');staging.unlink(missing_ok=True)
 with zipfile.ZipFile(staging,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name,digest in members.items():
   p=member_path(name);raw=p.read_bytes();require(hashlib.sha256(raw).hexdigest()==digest,'Package source changed during read: '+name)
   info=zipfile.ZipInfo('p08-scene-reconstruction/'+name,date_time=(2026,10,6,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o755 if p.name=='scicompile' else 0o644)<<16;z.writestr(info,raw)
 with zipfile.ZipFile(staging) as z:
  expected=['p08-scene-reconstruction/'+name for name in members]
  require(z.testzip() is None and z.namelist()==expected and len(set(z.namelist()))==len(expected),'Archive exact sealed inventory')
  for name,digest in members.items():require(hashlib.sha256(z.read('p08-scene-reconstruction/'+name)).hexdigest()==digest,'Archive sealed byte identity: '+name)
 require(package_members()==members,'Package inventories changed during write');staging.replace(dest)
 dump(H/'delivery/PACKAGE-MEMBERS.json',dict(schema=1,files=members,native_acceptance=False))
 dump(H/'delivery/ARTIFACT.json',dict(path=str(dest.relative_to(H)),sha256=sha(dest),bytes=dest.stat().st_size,files=len(members),source_seal_sha256=sha(H/'SOURCE-SEAL.json'),output_seal_sha256=sha(H/'OUTPUT-SEAL.json'),gate_seal_sha256=sha(H/'GATE-SEAL.json'),members_sha256=sha(H/'delivery/PACKAGE-MEMBERS.json'),native_acceptance=False));print((H/'delivery/ARTIFACT.json').read_text())
def main():
 state('RUNNING')
 try:
  require(not sys.flags.optimize,'Optimized Python forbidden')
  mode=sys.argv[1] if len(sys.argv)>1 else 'verify';require(mode in ['seal-source','rebuild','verify','package'],'Unknown mode')
  if mode=='seal-source':
   layout_check();input_check();(H/'GATE-SEAL.json').unlink(missing_ok=True);dump(H/'SOURCE-SEAL.json',dict(schema=1,kind='Explicit maintainer source identity; does not confer verification',files=source_files()));state('SOURCE_SEALED_NOT_VERIFIED');return
  source_check()
  if mode=='rebuild':rebuild()
  else:outputs_check()
  if mode=='package':package()
  state('PASS_BOUND_COMPONENT',source_seal_sha256=sha(H/'SOURCE-SEAL.json'),output_seal_sha256=sha(H/'OUTPUT-SEAL.json'),scope='Source/generated-data/coherent emitted fixture only; no native acceptance')
 except BaseException as e:
  state('FAILED',error=str(e));raise
if __name__=='__main__':main()
