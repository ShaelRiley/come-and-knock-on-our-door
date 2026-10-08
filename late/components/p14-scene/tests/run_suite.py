from pathlib import Path
import sys,unittest,json,io
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests'),str(H/'tools')]
from guard import input_check,require,sha
input_check()
loader=unittest.TestLoader();suite=unittest.TestSuite(loader.loadTestsFromName(n) for n in ('test_export','test_runtime','test_domain_bindings','test_calle'))
def leaves(s):
 for v in s:
  if isinstance(v,unittest.TestSuite):yield from leaves(v)
  else:yield v.id()
names=list(leaves(suite));expected=json.loads((H/'tests/EXPECTED-TESTS.json').read_text());require(names==expected,'Expected exact ordered tests')
stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite);print(stream.getvalue(),end='')
report=dict(status='PASS' if result.wasSuccessful() else 'FAILED',tests=result.testsRun,ids=names,failures=len(result.failures),errors=len(result.errors),source_seal_sha256=sha(H/'SOURCE-SEAL.json'),input_seal_sha256=sha(H/'INPUT-SEAL.json'),native_acceptance=False)
(H/'evidence/tests.json').write_text(json.dumps(report,indent=2)+'\n');raise SystemExit(not result.wasSuccessful())
