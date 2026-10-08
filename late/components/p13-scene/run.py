"""Sealed component rebuild/verify/package boundary. No native launch or host activation."""
from pathlib import Path,PurePosixPath
import sys,json,hashlib,subprocess,shutil,zipfile
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from guard import input_check,require,sha
CONTROL={'SOURCE-SEAL.json','OUTPUT-SEAL.json','GATE-SEAL.json','VERIFICATION.json','PACKAGE-MEMBERS.json'}
SOURCE_DIRS=['inputs','tools','tests']
OUTPUT_DIRS=['generated','snapshot','build']
EVIDENCE=['evidence/allocation-check.json','evidence/data-audio-gate.json','evidence/compile-proof.json','evidence/window-compile.json','evidence/tests.json','evidence/emission-audit.json']
GATES=['evidence/relocation.json','evidence/negative-checks.json']
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def state(status,**kw):dump(H/'VERIFICATION.json',dict(status=status,native_acceptance=False,**kw))
def paths(dirs):
 result=[]
 for dirname in dirs:
  root=H/dirname;require(root.is_dir() and not root.is_symlink(),'Invalid directory '+dirname)
  for p in sorted(root.rglob('*')):
   require(not p.is_symlink(),'Symlink rejected '+str(p.relative_to(H)))
   require(p.is_file() or p.is_dir(),'Nonregular member')
   if p.is_file():require('__pycache__' not in p.parts and p.suffix!='.pyc','Cached Python input');result.append(p)
 return result
def source_files():
 for p in H.iterdir():require(not p.is_symlink(),'Root symlink rejected')
 roots=[p for p in H.iterdir() if p.is_file() and p.name not in CONTROL]
 return {str(p.relative_to(H)):sha(p) for p in sorted(roots+paths(SOURCE_DIRS))}
def output_files():return {str(p.relative_to(H)):sha(p) for p in sorted(paths(OUTPUT_DIRS)+[H/n for n in EVIDENCE])}
def source_check():
 input_check();require(source_files()==json.loads((H/'SOURCE-SEAL.json').read_text())['files'],'Source inventory/hash mismatch')
def test_check():
 t=json.loads((H/'evidence/tests.json').read_text());e=json.loads((H/'tests/EXPECTED-TESTS.json').read_text());require(t['status']=='PASS' and t['test_ids']==e and t['tests']==len(e)==36 and t['skipped']==t['expected_failures']==0,'Exact clean test inventory required')
def output_check():
 o=json.loads((H/'OUTPUT-SEAL.json').read_text());require(o['source_seal_sha256']==sha(H/'SOURCE-SEAL.json'),'Stale output source identity');require(o['files']==output_files(),'Output inventory/hash mismatch');test_check()
 from tools.resource_codec import decode
 r=decode((H/'generated/fixture-game/resource.map').read_bytes(),(H/'generated/fixture-game/resource.000').read_bytes())
 for row in json.loads((H/'build/coherent/compile-receipt.json').read_text())['modules']:
  for t,part in [(2,'script'),(17,'heap')]:require(hashlib.sha256(r[t,row['module']]).hexdigest()==row[part+'_sha256'],'Packed emitted identity mismatch')
 require(r[3,214]==(H/'generated/214.text.bin').read_bytes(),'Packed Text214 mismatch')
def command(cmd,log):
 with (H/'evidence'/log).open('w') as f:p=subprocess.run(cmd,cwd=H,stdout=f,stderr=subprocess.STDOUT,text=True)
 require(p.returncode==0,'Failed '+log)
def seal_output():
 source_check();test_check();dump(H/'OUTPUT-SEAL.json',dict(schema=1,source_seal_sha256=sha(H/'SOURCE-SEAL.json'),files=output_files(),native_acceptance=False));output_check()
def rebuild():
 for name in OUTPUT_DIRS:
  if (H/name).exists():shutil.rmtree(H/name)
  (H/name).mkdir()
 (H/'evidence').mkdir(exist_ok=True)
 for name in ['OUTPUT-SEAL.json','GATE-SEAL.json']:(H/name).unlink(missing_ok=True)
 for script,log in [('generate.py','generation.log'),('verify_data.py','data-audio.log'),('extend_dialogue.py','extension.log'),('build.py','compile.log'),('tests/run_suite.py','tests.log'),('tools/audit_emission.py','emission-audit.log')]:command([sys.executable,str(H/script)],log)
 seal_output()
def gate_check():
 seal=json.loads((H/'GATE-SEAL.json').read_text());require(set(seal['files'])==set(GATES),'Gate inventory mismatch');require(seal['source_seal_sha256']==sha(H/'SOURCE-SEAL.json') and seal['output_seal_sha256']==sha(H/'OUTPUT-SEAL.json'),'Stale gate binding')
 require(seal['files']=={n:sha(H/n) for n in GATES},'Gate evidence hash mismatch')
 for n in GATES:
  r=json.loads((H/n).read_text());require(r['status']=='PASS' and r['source_seal_sha256']==sha(H/'SOURCE-SEAL.json') and r['output_seal_sha256']==sha(H/'OUTPUT-SEAL.json'),'Invalid gate '+n)
 p=json.loads((H/GATES[0]).read_text());require(p['clean_source_only_rebuild'] is True and p['exact_stable_output_inventory'] is True and p['tests']==36,'Incomplete portability')
 p=json.loads((H/GATES[1]).read_text());require(p['checks']==['source_tamper','input_tamper','output_tamper','output_missing','output_extra','symlink','gate_tamper','unsealed_extra_source'] and len(p['results'])==8 and all(r['rejected'] and r['stale_pass_cleared'] for r in p['results']),'Incomplete negative gate')
def seal_gates():
 source_check();output_check();dump(H/'GATE-SEAL.json',dict(schema=1,source_seal_sha256=sha(H/'SOURCE-SEAL.json'),output_seal_sha256=sha(H/'OUTPUT-SEAL.json'),files={n:sha(H/n) for n in GATES},native_acceptance=False));gate_check()
def package():
 source_check();output_check();gate_check();members={}
 for n in ['SOURCE-SEAL.json','OUTPUT-SEAL.json','GATE-SEAL.json']:
  for p,d in json.loads((H/n).read_text())['files'].items():
   require(p not in members or members[p]==d,'Conflicting inventory');members[p]=d
  members[n]=sha(H/n)
 dest=H/'delivery/P13-Scene-Editable-Component-20261007.zip';dest.parent.mkdir(exist_ok=True);tmp=dest.with_suffix('.tmp')
 with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as z:
  for n,d in sorted(members.items()):
   rel=PurePosixPath(n);require(not rel.is_absolute() and '..' not in rel.parts,'Unsafe package path');p=H/n;require(p.is_file() and not p.is_symlink() and sha(p)==d,'Package member drift')
   info=zipfile.ZipInfo('p13-scene-reconstruction/'+n,date_time=(2026,10,7,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o755 if p.name=='scicompile' else 0o644)<<16;z.writestr(info,p.read_bytes())
 with zipfile.ZipFile(tmp) as z:
  require(z.testzip() is None and len(z.namelist())==len(members),'Package inventory')
  for n,d in members.items():require(hashlib.sha256(z.read('p13-scene-reconstruction/'+n)).hexdigest()==d,'Package bytes')
 source_check();output_check();gate_check();tmp.replace(dest)
 dump(H/'delivery/FINAL-ARTIFACT.json',dict(path=str(dest.relative_to(H)),sha256=sha(dest),bytes=dest.stat().st_size,files=len(members),native_acceptance=False))
 print((H/'delivery/FINAL-ARTIFACT.json').read_text())
def main():
 state('RUNNING')
 try:
  require(not sys.flags.optimize,'Optimized Python forbidden');mode=sys.argv[1] if len(sys.argv)>1 else 'verify'
  require(mode in ['seal-source','seal-output','rebuild','verify','seal-gates','package'],'Unknown mode')
  if mode=='seal-source':input_check();dump(H/'SOURCE-SEAL.json',dict(schema=1,files=source_files()));state('SOURCE_SEALED_NOT_VERIFIED');return
  source_check()
  if mode=='rebuild':rebuild()
  elif mode=='seal-output':seal_output()
  else:output_check()
  if mode=='verify' and (H/'GATE-SEAL.json').exists():gate_check()
  if mode=='seal-gates':seal_gates()
  if mode=='package':package()
  state('PASS_BOUND_COMPONENT',source_seal_sha256=sha(H/'SOURCE-SEAL.json'),output_seal_sha256=sha(H/'OUTPUT-SEAL.json'),scope='Source/data/coherent emitted fixture; no P13 host/native acceptance')
 except BaseException as e:state('FAILED',error=str(e));raise
if __name__=='__main__':main()
