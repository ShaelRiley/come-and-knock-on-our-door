#!/usr/bin/env python3
"""Fixed, durably recorded source/emitted cases for this exact combined program.
Resume only a verified interruption on identical source/test/compiler bytes.
"""
from pathlib import Path
import hashlib,json,sys,unittest,traceback
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tests'));sys.path.insert(0,str(H/'tools'))
if sys.flags.optimize:raise RuntimeError('Optimized Python forbidden')
from test_transactions import Transactions
from test_cloth import Cloth

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fingerprint():
 paths=set()
 for folder in ('src','templates','tests','tools'):
  paths.update(p for p in (H/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
 for name in ('derive.py','generate_routes.py','build.py','selectors.json','HOST-SELECTORS.json','SOURCE-INPUTS.json','toolchain/scicompile','build/coherent/compile-receipt.json','build/coherent/selector-list.json','build/coherent/ABI-MAPPINGS.json'):
  paths.add(H/name)
 paths.update((H/'build/coherent/compiled').glob('*'))
 rows={str(p.relative_to(H)):sha(p) for p in sorted(paths)}
 return {'sha256':hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'files':rows}

all_tests=list(unittest.defaultTestLoader.loadTestsFromTestCase(Transactions))+list(unittest.defaultTestLoader.loadTestsFromTestCase(Cloth))
ids=[t.id() for t in all_tests]
expected=H/'tests/EXPECTED-GATE2B1.json'
if not expected.exists():raise RuntimeError('Missing fixed test inventory')
if json.loads(expected.read_text())['cases']!=ids:raise RuntimeError('Fixed test membership changed')
identity=fingerprint();out=H/'evidence/gate2b1-cases.json'
proof={'status':'RUNNING','binding':identity,'expected_cases':ids,'cases':[],'native_acceptance':False,'backends':['editable989-and-changed983984-bridges','whole-emitted-campaign']}
if '--resume' in sys.argv:
 if not out.exists():raise RuntimeError('No interruption receipt')
 saved=json.loads(out.read_text())
 if saved['binding']!=identity or saved['expected_cases']!=ids:raise RuntimeError('Changed inputs cannot reuse completed cases')
 if any(r['status']=='FAIL' for r in saved['cases']):raise RuntimeError('Failure requires a fresh gate')
 proof['cases']=[r for r in saved['cases'] if r['status']=='PASS']
passed={r['case'] for r in proof['cases']}

def write():
 temp=out.with_suffix('.tmp');temp.write_text(json.dumps(proof,indent=2)+'\n');temp.replace(out)
write()
class Recorded(unittest.TextTestResult):
 def startTest(self,test):
  super().startTest(test);proof['active_case']=test.id();write()
 def addSuccess(self,test):
  super().addSuccess(test)
  if fingerprint()!=identity:raise RuntimeError('Inputs changed during a case')
  proof['cases'].append({'case':test.id(),'status':'PASS','binding_sha256':identity['sha256']});proof.pop('active_case',None);write()
 def addFailure(self,test,err):
  super().addFailure(test,err);proof['cases'].append({'case':test.id(),'status':'FAIL','error':self._exc_info_to_string(err,test)});write()
 def addError(self,test,err):
  super().addError(test,err);proof['cases'].append({'case':test.id(),'status':'FAIL','error':self._exc_info_to_string(err,test)});write()
runner=unittest.TextTestRunner(verbosity=2,resultclass=Recorded)
result=runner.run(unittest.TestSuite(t for t in all_tests if t.id() not in passed))
if fingerprint()!=identity:raise RuntimeError('Inputs changed during gate')
proof['status']='PASS' if result.wasSuccessful() and {r['case'] for r in proof['cases'] if r['status']=='PASS'}==set(ids) else 'FAIL'
proof.pop('active_case',None);write()
print(json.dumps({'status':proof['status'],'binding_sha256':identity['sha256'],'completed_cases':len(proof['cases']),'expected_cases':len(ids),'native_acceptance':False},sort_keys=True))
sys.exit(0 if proof['status']=='PASS' else 1)
