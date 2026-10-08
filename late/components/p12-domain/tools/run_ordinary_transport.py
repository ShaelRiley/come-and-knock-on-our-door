"""One unchanged accepted test: 47 ordinary saves and exact receipt restoration."""
from pathlib import Path
import sys,unittest,json
H=Path(__file__).resolve().parents[1]
if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
sys.path[:0]=[str(H/'tests'),str(H),str(H/'reference/component'),str(H/'reference/component/tests')]
from verify_source import verify
verify()
from test_transport import TransportTests
suite=unittest.TestSuite([TransportTests('test_ordinary_saved_histories_roundtrip_in_both_evaluators')])
r=unittest.TextTestRunner(verbosity=2).run(suite)
if r.testsRun!=1 or not r.wasSuccessful():raise SystemExit(1)
print('PASS_UNCHANGED_ORDINARY_TRANSPORT_47_SAVES')
