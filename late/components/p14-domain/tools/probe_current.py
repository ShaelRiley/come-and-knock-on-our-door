"""NEW replay of all accepted current join tests with paired finite P14 actions."""
from pathlib import Path
import sys,unittest,io,json,time,importlib.util
H=Path(__file__).resolve().parents[1];C=H/'reference/component';sys.dont_write_bytecode=True
sys.path[:0]=[str(H/'tests'),str(H),str(C),str(C/'tests')]
if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
from verify_source import verify
verify()
import joined_pair,source_vm
from paired import PairedVM,MEASUREMENTS
source_vm.VM=PairedVM
spec=importlib.util.spec_from_file_location('current_emitted_tests',C/'tests/test_p14_current.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.FinaleJoined=joined_pair.FinaleJoined;m.P14World=joined_pair.ModelFactory()
names=unittest.defaultTestLoader.getTestCaseNames(m.CurrentJoinTests)
if len(names)!=13:raise RuntimeError('Incomplete current tests')
if len(sys.argv)==1:raise ValueError('Specify a bounded bank 0 through 12')
index=int(sys.argv[1]);name=names[index];out=io.StringIO();start=time.monotonic();result=unittest.TextTestRunner(stream=out,verbosity=2).run(unittest.TestSuite([m.CurrentJoinTests(name)]));text=out.getvalue();print(text,end='')
p=H/'evidence'/f'current-emitted-{index:02}.json'
if p.exists() and json.loads(p.read_text())['status']=='FAILED':p.rename(p.with_name('current-emitted-failure-'+str(time.time_ns())+'.json'))
p.write_text(json.dumps(dict(status='PASS' if result.wasSuccessful() else 'FAILED',tests=result.testsRun,test_id=name,failures=len(result.failures),errors=len(result.errors),counts=joined_pair.N,paired=MEASUREMENTS,elapsed_seconds=time.monotonic()-start,log=text,native_acceptance=False,upstream_owners='Accepted Python reference',witness='R2 reference boundary; native atomic integration pending'),indent=2)+'\n')
raise SystemExit(not result.wasSuccessful())
