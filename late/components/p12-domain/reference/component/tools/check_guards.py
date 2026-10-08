"""New finite guard probes; no broad adversarial save-security claim."""
from pathlib import Path
import shutil,subprocess,sys,json
W=Path(__file__).resolve().parents[2];P=W/'probes';P.mkdir(exist_ok=True)
CASES={
 'changed canonical authority':('component/authority/full-line-catalog.json','append'),
 'missing literal prefix':('historical/literal-read-partial/cakood/p12_model.py.part','missing'),
 'partial working model':('component/cakood/p12_model.py','partial'),
 'changed accepted P10':('component/cakood/p10_model.py','append'),
 'changed retained SCI':('component/stock-sci/p12-domain-adapter/src/methods.sc.in','append'),
 'changed generated source':('component/stock-sci/p12-domain-adapter/src/module994.sc','append'),
 'changed canonical fixture':('component/tests/fixtures/p12/canonical-bindings.json','append'),
 'missing domain test':('component/stock-sci/p12-domain-adapter/tests/test_domain.py','missing'),
 'missing join test':('component/tests/test_p12_current.py','missing'),
 'missing contest owner':('component/dependencies/vc_owner/verbal_contest.py','missing')}
results=[]
for label,(relative,action) in CASES.items():
 dst=P/label
 shutil.copytree(W/'component',dst/'component',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 for name in ('historical','provenance'):shutil.copytree(W/name,dst/name,dirs_exist_ok=True)
 path=dst/relative
 if action=='missing':path.unlink()
 elif action=='partial':path.write_bytes((dst/'historical/literal-read-partial/cakood/p12_model.py.part').read_bytes())
 else:path.write_bytes(path.read_bytes()+b'\nCHANGED_FOR_SCOPED_PROBE\n')
 for optimized in (False,True):
  cmd=[sys.executable,*(['-O'] if optimized else []),str(dst/'component/tools/run_tests.py')]
  p=subprocess.run(cmd,capture_output=True,text=True)
  log=dst/('optimized.log' if optimized else 'normal.log');log.write_text(p.stdout+p.stderr)
  if p.returncode==0:raise RuntimeError('Guard accepted '+label)
  results.append(dict(case=label,optimized=optimized,exit_code=p.returncode,log=str(log.relative_to(W))))
(W/'evidence/guard-probes.json').write_text(json.dumps(dict(status='PASS',cases=results),indent=2)+'\n')
print('PASS:',len(results),'scoped normal/optimized rejection probes')
