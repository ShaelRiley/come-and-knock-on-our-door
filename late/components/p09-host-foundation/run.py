#!/usr/bin/env python3
"""Reproducible bounded foundation gate with exact source/output binding."""
from pathlib import Path
import hashlib,json,subprocess,sys,time,unittest,zipfile
H=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(H));sys.path.insert(0,str(H/'tests'));sys.path.insert(0,str(H/'tools'))
from derive import derive,dump,sha,require
CASES=['test_foundation.Foundation',
 'test_composition_initial.CompositionInitial.test_02_assembled_named_layout_and_overlap_recovery',
 'test_composition_initial.CompositionInitial.test_03_assembled_save_restore_and_reversible_return',
 'test_intro.Intro', 'test_ready_confirmation.ReadyConfirmation']

def source_files():
 paths=[p for f in ('frozen','toolchain','src','templates','tests','tools') for p in (H/f).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
 paths += [p for p in H.iterdir() if p.is_file() and (p.suffix in ('.py','.md') or p.name in ('INPUT-SEAL.json','ALLOCATION-PLAN.json','HOST-ALLOCATION.json','selectors.json','SOURCE-DEPENDENCY-MAP.json','INTEGRATION-DELTA.json','TEST-CONTRACT.json'))]
 return {str(p.relative_to(H)):sha(p) for p in sorted(set(paths))}
def identity():return hashlib.sha256(json.dumps(source_files(),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def output_files():
 return {str(p.relative_to(H)):sha(p) for p in sorted((H/'build/coherent').rglob('*')) if p.is_file() and p.suffix!='.sco'}
def source_check():require(source_files()==json.loads((H/'SOURCE-SEAL.json').read_text()),'Source seal changed; explicitly reseal reviewed edits')
def test():
 source_check();derive(check=True)
 from audit import audit
 audit();fingerprint=identity();outputs=output_files()
 suite=unittest.defaultTestLoader.loadTestsFromNames(CASES)
 require(suite.countTestCases()==8,'Exact eight bounded cases required')
 proof={'status':'RUNNING','binding_sha256':fingerprint,'cases':[],'native_acceptance':False}
 target=H/'evidence/behavior-gate.json';dump(target,proof)
 class Result(unittest.TextTestResult):
  def startTest(self,t):self.start=time.monotonic();super().startTest(t)
  def addSuccess(self,t):
   super().addSuccess(t);proof['cases'].append({'case':t.id(),'status':'PASS','seconds':round(time.monotonic()-self.start,3)});dump(target,proof)
  def addFailure(self,t,e):super().addFailure(t,e);proof['cases'].append({'case':t.id(),'status':'FAIL','error':self._exc_info_to_string(e,t)});dump(target,proof)
  def addError(self,t,e):super().addError(t,e);proof['cases'].append({'case':t.id(),'status':'ERROR','error':self._exc_info_to_string(e,t)});dump(target,proof)
 result=unittest.TextTestRunner(verbosity=2,resultclass=Result,failfast=True).run(suite)
 require(identity()==fingerprint and output_files()==outputs,'Program/test inputs changed during tests')
 proof['status']='PASS' if result.wasSuccessful() and len(proof['cases'])==8 else 'FAILED';dump(target,proof)
 require(proof['status']=='PASS','Behavior gate failed')
 gate={'status':'PASS_INACTIVE_FOUNDATION','source_sha256':fingerprint,'output_files':outputs,'cases':8,'active_p09':False,'native_acceptance':False,'scope':'Complete coherent production compile, source/emitted inactive boot/dispatch, prior real action histories and ordinary mocked save/restore','compile_receipt_sha256':sha(H/'build/coherent/compile-receipt.json'),'behavior_receipt_sha256':sha(target),'audit_receipt_sha256':sha(H/'evidence/static-audit.json')}
 dump(H/'VERIFICATION.json',gate);dump(H/'CURRENT-GATE.json',gate);print('PASS_INACTIVE_FOUNDATION')
 return gate
def check():
 source_check();derive(check=True)
 gate=json.loads((H/'VERIFICATION.json').read_text())
 require(gate['status']=='PASS_INACTIVE_FOUNDATION' and gate['source_sha256']==identity(),'Unbound verification')
 require(gate['output_files']==output_files(),'Compiled output membership/bytes changed')
 for path,key in [('build/coherent/compile-receipt.json','compile_receipt_sha256'),('evidence/behavior-gate.json','behavior_receipt_sha256'),('evidence/static-audit.json','audit_receipt_sha256')]:require(sha(H/path)==gate[key],'Receipt changed '+path)
 require(json.loads((H/'evidence/behavior-gate.json').read_text())['status']=='PASS','Behavior result')
 print('PASS_BOUND_VERIFICATION');return gate
def package():
 check()
 cold=json.loads((H/'evidence/cold-reproducibility.json').read_text());require(cold['status']=='PASS' and cold['source_sha256']==identity(),'Cold reproducibility required')
 paths=set(source_files())|set(output_files())|{'SOURCE-SEAL.json','VERIFICATION.json','CURRENT-GATE.json'}
 paths.update(str(p.relative_to(H)) for p in (H/'evidence').iterdir() if p.is_file())
 inventory={n:sha(H/n) for n in sorted(paths)};dump(H/'PACKAGE-INVENTORY.json',inventory)
 target=H/'delivery/Come-and-Knock-on-Our-Door-P09-Inactive-Host-Foundation-20261007.zip'
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in sorted(paths|{'PACKAGE-INVENTORY.json'}):
   item=zipfile.ZipInfo('p09-host-foundation/'+n,date_time=(2026,10,7,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED
   item.external_attr=(0o100755 if n=='toolchain/scicompile' else 0o100644)<<16;z.writestr(item,(H/n).read_bytes())
 print(target,sha(target));return target
if __name__=='__main__':
 try:
  require(not sys.flags.optimize,'Optimized Python forbidden')
  cmd=sys.argv[1] if len(sys.argv)>1 else 'check'
  if cmd=='seal':derive();dump(H/'SOURCE-SEAL.json',source_files());print('SEALED_NOT_VERIFIED')
  elif cmd=='rebuild':
   dump(H/'VERIFICATION.json',{'status':'BUILDING','native_acceptance':False});source_check()
   subprocess.run([sys.executable,'-B',str(H/'build.py')],check=True);test()
  elif cmd=='test':
   dump(H/'VERIFICATION.json',{'status':'TESTING','native_acceptance':False});test()
  elif cmd=='check':check()
  elif cmd=='package':package()
  else:raise RuntimeError('Use seal, rebuild, test, check, or package')
 except BaseException as e:
  dump(H/'VERIFICATION.json',{'status':'FAILED','reason':str(e),'native_acceptance':False});raise
