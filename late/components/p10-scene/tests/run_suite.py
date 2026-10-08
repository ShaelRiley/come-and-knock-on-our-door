from pathlib import Path
import sys,unittest,json
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tests'))
import test_export,test_current,test_composition
suite=unittest.defaultTestLoader.loadTestsFromModule(test_export);suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(test_current));suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(test_composition))
def ids(s):return [i for t in s for i in (ids(t) if isinstance(t,unittest.TestSuite) else [t.id()])]
names=ids(suite);expected=json.loads((H/'tests/EXPECTED-TESTS.json').read_text());assert names==expected
out=H/'evidence/tests.json';out.write_text(json.dumps(dict(status='RUNNING',native_acceptance=False)))
r=unittest.TextTestRunner(verbosity=2).run(suite)
if not r.wasSuccessful() or r.skipped or r.expectedFailures:out.write_text(json.dumps(dict(status='FAILED',native_acceptance=False)));raise SystemExit(1)
out.write_text(json.dumps(dict(status='PASS',test_ids=names,tests=r.testsRun,skipped=0,expected_failures=0,measurements=test_current.EVIDENCE,native_acceptance=False),indent=2)+'\n')
