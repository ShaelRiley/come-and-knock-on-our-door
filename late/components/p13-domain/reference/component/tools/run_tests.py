"""NEW explicit finite reference/source discovery, assertions retained under -O."""
from pathlib import Path
import sys,unittest,json
C=Path(__file__).resolve().parents[1];D=C/'stock-sci/p13-domain-adapter'
sys.path[:0]=[str(C),str(C/'tests'),str(D),str(D/'tests')]
from tools.verify_inputs import verify
from tools.generate_fixture import fixture
from tools.assertions import load
from tools.verify_source import verify as verify_source
verify()
verify_source()
if json.loads((C/'tests/fixtures/p13/canonical-bindings.json').read_text())!=json.loads(json.dumps(fixture())):raise RuntimeError('Stale fixture')
suite=unittest.TestSuite()
for path in [C/'tests/test_late_campaign_models.py',D/'tests/test_domain.py',D/'tests/test_validation.py',C/'tests/test_p13_current.py']:
 if not path.is_file():raise RuntimeError('Required test missing '+str(path))
 m=load(path.stem,path);suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(m))
def cases(suite):
 for item in suite:
  if isinstance(item,unittest.TestSuite):yield from cases(item)
  else:yield item.id()
expected=json.loads((C/'tests/EXPECTED-TESTS.json').read_text())
if sorted(cases(suite))!=expected:raise RuntimeError('Finite test identities changed or disappeared')
result=unittest.TextTestRunner(verbosity=2).run(suite)
print('Finite reference/source tests:',result.testsRun,'optimized:',sys.flags.optimize,'native acceptance: false')
if not result.wasSuccessful():raise SystemExit(1)
