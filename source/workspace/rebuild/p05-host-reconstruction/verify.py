#!/usr/bin/env python3
"""Public fail-closed source/emitted verifier. No native or release acceptance."""
from pathlib import Path
import sys,json,hashlib,subprocess,os,traceback
H=Path(__file__).resolve().parent;R=H.parent;OUT=H/'VERIFICATION.json'
OUT.write_text('{"status":"RUNNING","native_acceptance":false}\n')
# Acceptance is retired before every project-local import, argument check or read.
sys.dont_write_bytecode=True
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,why):
 if not ok:raise RuntimeError(why)
def inventory():
 data=json.loads((H/'INPUTS.json').read_text());require(type(data.get('schema')) is int and data['schema']==1,'Input manifest schema')
 require(sha(H/'EXPECTED-INPUT-PATHS.json')=='1b52926ecae901c09d751dad2b79850b403adc48d44e199569395138a9e513fa','Fixed inventory membership identity changed')
 expected=json.loads((H/'EXPECTED-INPUT-PATHS.json').read_text())
 for key in ['local','external']:require(set(data.get(key,{}))==set(expected[key]),'Missing/extra input inventory members: '+key)
 for base,key in [(H,'local'),(R,'external')]:
  for rel,meta in data[key].items():
   require(not Path(rel).is_absolute() and '..' not in Path(rel).parts,'Manifest path escape')
   p=base/rel;require(p.stat().st_size==meta['bytes'] and sha(p)==meta['sha256'],'Exact input changed: '+key+'/'+rel)
 return data
try:
 require(not sys.flags.optimize,'Optimized Python is forbidden')
 require(len(sys.argv)==1,'No partial/skip/zero-test verification modes')
 for name in ['CAKOOD_BUILD','CAKOOD_CHECKPOINT','CAKOOD_SELECTORS']:require(not os.environ.get(name),'Unbound environment override '+name)
 inputs=inventory();seal=sha(H/'INPUTS.json')
 sys.path.insert(0,str(H/'tools'));from validate_selected_inputs import check
 check(H)
 E=H/'evidence';E.mkdir(exist_ok=True)
 commands=[['derive.py'],['build.py'],['tests/verify_architecture.py'],['tests/audit_emitted.py'],['tests/run_suite.py']]
 for args in commands:
  log=E/('verify-'+Path(args[0]).stem+'.log')
  with log.open('w') as f:result=subprocess.run([sys.executable,*args],cwd=H,stdout=f,stderr=subprocess.STDOUT)
  require(result.returncode==0,'Verification command failed: '+' '.join(args)+'; see '+str(log.relative_to(H)))
 inventory();require(sha(H/'INPUTS.json')==seal,'Input seal changed during verification')
 receipt=json.loads((H/'build/coherent/compile-receipt.json').read_text());require(receipt['status']=='PASS_FRESH_COMPILE','Fresh coherent compile missing')
 abi=json.loads((H/'build/coherent/ABI-MAPPINGS.json').read_text())
 for row in receipt['modules']:
  number=row['module'];source=H/'src'/('main.sc' if number==0 else f'module{number}.sc')
  require(sha(source)==row['source_sha256']==abi['modules'][str(number)]['sha256'],'Source/emitted ABI binding mismatch')
  require(sha(H/f'build/coherent/compiled/{number}.scr.bin')==row['script_sha256'] and sha(H/f'build/coherent/compiled/{number}.scr.bin.hep')==row['heap_sha256'],'Compiled bytes changed')
  require(row['combined_bytes']<=65535,'SCI16 segment budget exceeded')
 proofs={}
 for file,status in [('evidence/architecture-abi.json','PASS_ARCHITECTURE_ABI_SOURCE'),('evidence/static-emitted.json','PASS_STATIC_EMITTED_UNIVERSE'),('evidence/suite.json','PASS')]:
  require(json.loads((H/file).read_text())['status']==status,'Missing fresh proof '+file);proofs[file]=sha(H/file)
 OUT.write_text(json.dumps({'status':'PASS_SOURCE_EMITTED_STATIC_ONLY','input_manifest_sha256':seal,'proofs':proofs,'compiled_modules':receipt['modules'],'native_acceptance':False,'remaining':['Independent final review','Stock ScummVM 2026.3.0 native proof','MUS11 presentation integration']},indent=2)+'\n')
 print('PASS_SOURCE_EMITTED_STATIC_ONLY')
except BaseException as e:
 OUT.write_text(json.dumps({'status':'FAIL','error':str(e),'native_acceptance':False},indent=2)+'\n');raise
