"""Replay accepted genuine joins with newly paired source and emitted P13 calls."""
from pathlib import Path
import sys,unittest,io,json,time,importlib.util
H=Path(__file__).resolve().parents[1];C=H/'reference/component'
sys.path[:0]=[str(H/'tests'),str(H),str(C),str(C/'tests')]
if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
from verify_source import verify
verify()
import joined_pair
from paired import PairedVM,MEASUREMENTS
from test_domain import Harness
spec=importlib.util.spec_from_file_location('current_emitted_tests',C/'tests/test_p13_current.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.Joined=joined_pair.Joined
m.Harness=lambda *a,**kw:Harness(PairedVM,*a,**kw)
suite=unittest.defaultTestLoader.loadTestsFromTestCase(m.CurrentTests)
if suite.countTestCases()!=15:raise RuntimeError('Current tests missing')
out=io.StringIO();result=unittest.TextTestRunner(stream=out,verbosity=2).run(suite)
text=out.getvalue();print(text,end='');p=H/'evidence/current-emitted.json'
if p.exists() and json.loads(p.read_text())['status']=='FAILED':p.rename(p.with_name('current-emitted-failure-'+str(time.time_ns())+'.json'))
p.write_text(json.dumps(dict(status='PASS' if result.wasSuccessful() else 'FAILED',tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),counts=joined_pair.N,paired=MEASUREMENTS,log=text,native_acceptance=False),indent=2)+'\n')
raise SystemExit(not result.wasSuccessful())
