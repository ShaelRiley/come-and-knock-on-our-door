"""NEW individually banked finite source/emitted gates. No optimized execution."""
from pathlib import Path
import sys,json,unittest,time,io,hashlib
H=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(H/'tests'),str(H),str(H/'reference/component'),str(H/'reference/component/tests')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
 from verify_source import verify
 verify()
 import test_domain as d,test_validation as v
 from paired import MEASUREMENTS
 groups={}
 names=unittest.defaultTestLoader.getTestCaseNames(d.DomainTests)
 for i,name in enumerate(names):groups['domain-'+str(i).zfill(2)]=[d.DomainTests(name),d.BytecodeTests(name)]
 for i,name in enumerate(unittest.defaultTestLoader.getTestCaseNames(v.ValidationTests)):
  if name in ('test_all_6561_approval_and_pin_ledger_projections','test_emitted_validator_reachable_and_corrupt_model_parity'):continue
  groups['validation-'+str(i).zfill(2)]=[v.ValidationTests(name)]
 expected={g:[x.id() for x in tests] for g,tests in groups.items()}
 if '--list' in sys.argv:print(json.dumps(expected,indent=2));return
 frozen=json.loads((H/'tests/EXPECTED-TESTS.json').read_text())
 if expected!=frozen:raise RuntimeError('Named finite gate admission changed')
 selected=sys.argv[1:]
 if not selected:raise ValueError('Specify one or more bounded test bank names')
 for group in selected:
  tests=groups[group];start=time.monotonic();out=io.StringIO();r=unittest.TextTestRunner(stream=out,verbosity=2).run(unittest.TestSuite(tests));text=out.getvalue();print(text,flush=True)
  record=dict(status='PASS' if r.wasSuccessful() else 'FAILED',tests=r.testsRun,test_ids=expected[group],elapsed_seconds=time.monotonic()-start,paired=dict(MEASUREMENTS),native_acceptance=False,host_integration=False,source_sha256=sha(H/'src/module996.sc'),manifest_sha256=sha(H/'manifest.json'),runner_sha256=sha(Path(__file__)),test_sha256={p.name:sha(p) for p in (H/'tests').glob('*.py')})
  target=H/'evidence'/('bank-'+group+'.json');log=target.with_suffix('.log')
  if target.exists():
   prior=json.loads(target.read_text())
   if prior['status']=='FAILED':target.rename(target.with_name('prior-failure-'+str(time.time_ns())+'.json'));log.rename(log.with_name('prior-failure-'+str(time.time_ns())+'.log'))
  target.write_text(json.dumps(record,indent=2)+'\n');log.write_text(text)
  if not r.wasSuccessful():raise SystemExit(1)
if __name__=='__main__':main()
