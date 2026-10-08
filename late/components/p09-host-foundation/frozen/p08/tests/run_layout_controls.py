"""Fixed eight-case gate with a durable receipt after each completed case."""
import sys,json,time,unittest,hashlib
from pathlib import Path
import host
from test_layout_controls import LayoutControls
H=host.H
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=['derive.py','HOST-SELECTORS.json','tests/test_layout_controls.py','tests/source_host.py','tests/domain_source_vm.py','tools/host_vm.py','build/coherent/compile-receipt.json']+[str(p.relative_to(H)) for d in ('templates','src') for p in sorted((H/d).glob('*')) if p.is_file()]
binding={n:sha(H/n) for n in files};(H/'evidence/layout-controls-binding.json').write_text(json.dumps(binding,indent=2)+'\n')
class Result(unittest.TextTestResult):
 def startTest(self,test):self.started=time.monotonic();super().startTest(test)
 def stopTest(self,test):
  super().stopTest(test)
  assert all(sha(H/n)==d for n,d in binding.items()),'source/compile changed during gate'
  failed=any(t is test for t,e in self.errors+self.failures)
  result={'case':test._testMethodName,'status':'FAIL' if failed else 'PASS','seconds':round(time.monotonic()-self.started,3),'backends':['emitted','editable source989+changed bridges'],'compile_receipt_sha256':binding['build/coherent/compile-receipt.json'],'test_source_sha256':binding['tests/test_layout_controls.py'],'native_acceptance':False}
  (H/'evidence'/('layout-'+test._testMethodName+'.json')).write_text(json.dumps(result,indent=2)+'\n')
  print('CASE_RECEIPT',json.dumps(result),flush=True)
suite=unittest.defaultTestLoader.loadTestsFromTestCase(LayoutControls)
r=unittest.TextTestRunner(verbosity=2,resultclass=Result,failfast=True).run(suite)
sys.exit(not r.wasSuccessful())
