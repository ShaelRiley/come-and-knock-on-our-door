"""Finite reference/source gate. Explicit discovery, no optimized-away checks."""
from pathlib import Path
import sys,unittest,json,hashlib
C=Path(__file__).resolve().parents[1];D=C/'stock-sci/p12-domain-adapter'
sys.path[:0]=[str(C),str(C/'tests'),str(D),str(D/'tests')]
from tools.verify_inputs import verify
from tools.generate_fixture import fixture
from tools.assertions import load
from tools.verify_source import verify as verify_source
verify()
verify_source()
expected=json.loads(json.dumps(fixture()))
if json.loads((C/'tests/fixtures/p12/canonical-bindings.json').read_text())!=expected:raise RuntimeError('Stale fixture')
suite=unittest.TestSuite()
for path in [D/'tests/test_domain.py',C/'tests/test_p12_current.py']:
 if not path.is_file():raise RuntimeError('Required test missing: '+str(path))
 module=load(path.stem,path);suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
if suite.countTestCases()!=26:raise RuntimeError('Finite test coverage disappeared')
r=unittest.TextTestRunner(verbosity=2).run(suite)
if not r.wasSuccessful():sys.exit(1)
print('PASS finite reference/source gate; tests='+str(r.testsRun)+'; optimized='+str(sys.flags.optimize))
