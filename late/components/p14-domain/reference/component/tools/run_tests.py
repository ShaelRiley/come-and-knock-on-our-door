"""NEW explicit reference/source test discovery with assertions active under -O."""
from pathlib import Path
import sys,unittest,json
C=Path(__file__).resolve().parents[1];D=C/'stock-sci/p14-domain-adapter'
sys.path[:0]=[str(C),str(C/'tests'),str(D),str(D/'tests')]
from tools.verify_inputs import verify
from tools.generate_fixture import fixture
from tools.assertions import load
from tools.verify_source import verify as verify_source
from tools.verify_working import verify as verify_working
verify()
verify_working()
verify_source()
if json.loads((C/'tests/fixtures/p14/canonical-bindings.json').read_text())!=json.loads(json.dumps(fixture())):raise RuntimeError('Stale fixture')
(D/'evidence').mkdir(exist_ok=True)
suite=unittest.TestSuite()
for path in [D/'tests/test_domain.py',D/'tests/test_validation.py',C/'tests/test_p14_current.py',C/'tests/test_p14_pairing.py']:
 if not path.is_file():raise RuntimeError('Required test missing '+str(path))
 m=load(path.stem,path);suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(m))
def cases(s):
 for item in s:
  if isinstance(item,unittest.TestSuite):yield from cases(item)
  else:yield item.id()
expected=json.loads((C/'tests/EXPECTED-TESTS.json').read_text())
if sorted(cases(suite))!=expected:raise RuntimeError('Required test identities changed or disappeared')
if '--admit-only' in sys.argv:
 print('Admitted',len(expected),'named source/reference tests; native acceptance: false')
 raise SystemExit(0)
if '--focused-pairing' in sys.argv:
 excluded={'test_validation.ValidationTests.test_all_6561_approval_and_pin_ledger_projections',
           'test_validation.ValidationTests.test_emitted_validator_reachable_and_corrupt_model_parity'}
 def flatten(s):
  for item in s:
   if isinstance(item,unittest.TestSuite):yield from flatten(item)
   else:yield item
 suite=unittest.TestSuite(t for t in flatten(suite) if t.id() not in excluded)
 if len(tuple(cases(suite)))!=len(expected)-2:raise RuntimeError('Focused suite missing unexpected tests')
 print('P14-REF-001 focused gate: two unchanged long matrices excluded',flush=True)
result=unittest.TextTestRunner(verbosity=2).run(suite)
print('Finite P14 reference/source tests:',result.testsRun,'optimized:',sys.flags.optimize,'native acceptance: false')
if not result.wasSuccessful():raise SystemExit(1)
