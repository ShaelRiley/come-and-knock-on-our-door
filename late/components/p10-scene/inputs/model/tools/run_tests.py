"""Hash/check authority and inputs, reject empty discovery, then run unittest."""
from pathlib import Path
import json
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT/'tools')]
from verify_inputs import verify
from generate_fixture import fixture
print('VERIFIED_INPUTS=' + str(verify()))
if json.loads((ROOT/'tests/fixtures/p10/canonical-bindings.json').read_text()) != json.loads(json.dumps(fixture())):
    raise RuntimeError('Current fixture differs from verified canonical input')
suite = unittest.defaultTestLoader.discover(str(ROOT/'tests'), pattern='test_*.py')
count = suite.countTestCases()
if count != 40:
    raise RuntimeError('Incomplete or unexpected test discovery: ' + str(count))
result = unittest.TextTestRunner(verbosity=2).run(suite)
if not result.wasSuccessful():
    raise SystemExit(1)
print('GUARDED_TEST_COUNT=' + str(count))
