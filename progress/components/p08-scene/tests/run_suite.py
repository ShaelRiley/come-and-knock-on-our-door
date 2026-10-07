from pathlib import Path
import sys,json,unittest
H=Path(__file__).resolve().parents[1];OUT=H/'evidence/tests.json';OUT.write_text('{"status":"RUNNING","native_acceptance":false}\n');sys.dont_write_bytecode=True
def status(value,error=None):
 for p in [H/'VERIFICATION.json',H/'evidence/current-status.json']:
  p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(dict(status=value,error=error,native_acceptance=False))+'\n')
status('TESTS_RUNNING_NOT_ACCEPTED')
try:
 if sys.flags.optimize:raise RuntimeError('Optimized Python forbidden')
 import test_scene
 suite=unittest.defaultTestLoader.loadTestsFromModule(test_scene)
 def flatten(s):
  for t in s:
   if isinstance(t,unittest.TestSuite):yield from flatten(t)
   else:yield t
 ids=[t.id() for t in flatten(suite)];expected=json.loads((H/'tests/EXPECTED-TESTS.json').read_text())
 if not ids or ids!=expected:raise RuntimeError('Exact test inventory mismatch')
 result=unittest.TextTestRunner(verbosity=2).run(suite)
 if result.testsRun!=len(ids) or not result.wasSuccessful() or result.skipped or result.expectedFailures or result.unexpectedSuccesses:raise RuntimeError('Non-exact clean test result')
 OUT.write_text(json.dumps(dict(status='PASS',test_ids=ids,tests=result.testsRun,skipped=0,expected_failures=0,measurements=test_scene.EVIDENCE,instructions=sum(v.steps for v in test_scene.VMS),emitted_send_packets=sum(len(v.packets) for v in test_scene.VMS),emitted_returns=sum(len(v.returns) for v in test_scene.VMS),reviewed_method_arity_checked=True,operand_stack_bounds_checked=True,native_acceptance=False),indent=2)+'\n')
except BaseException as e:
 status('FAILED',str(e))
 OUT.write_text(json.dumps(dict(status='FAILED',error=str(e),native_acceptance=False))+'\n');raise
