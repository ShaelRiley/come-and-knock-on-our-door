from pathlib import Path
import sys,unittest,json,io,time
H=Path(__file__).resolve().parents[1];sys.dont_write_bytecode=True
sys.path[:0]=[str(H/'tests'),str(H),str(H/'reference/component'),str(H/'reference/component/tests')]
if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
from verify_source import verify
verify()
import test_finite as m
from paired import MEASUREMENTS
names=unittest.defaultTestLoader.getTestCaseNames(m.FiniteTests)
if len(names)!=4:raise ValueError('Finite tests missing')
i=int(sys.argv[1]);start=time.monotonic();out=io.StringIO();r=unittest.TextTestRunner(stream=out,verbosity=2).run(unittest.TestSuite([m.FiniteTests(names[i])]))
p=H/'evidence'/f'finite-{i:02}.json'
if p.exists() and json.loads(p.read_text())['status']=='FAILED':p.rename(p.with_name('finite-failure-'+str(time.time_ns())+'.json'))
p.write_text(json.dumps(dict(status='PASS' if r.wasSuccessful() else 'FAILED',test=names[i],tests=r.testsRun,paired=MEASUREMENTS,measurements=m.MEASUREMENTS,elapsed_seconds=time.monotonic()-start,log=out.getvalue(),native_acceptance=False),indent=2)+'\n');print(out.getvalue());raise SystemExit(not r.wasSuccessful())
