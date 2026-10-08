"""NEW scoped admission probes. All mutations are in disposable isolated copies."""
from pathlib import Path
import sys,subprocess,shutil,json,tempfile
W=Path(__file__).resolve().parents[2];E=W/'evidence/guard-logs';E.mkdir(exist_ok=True)
CASES={
 'canonical_authority':('component/authority/full-line-catalog.json','append'),
 'literal_model_missing':('historical/literal-read/cakood/p13_model.py','missing'),
 'working_model_partial':('component/cakood/p13_model.py','partial'),
 'accepted_p12_changed':('component/cakood/p12_model.py','append'),
 'genuine_p07_missing':('component/dependencies/p07_owner/cakood/p07_model.py','missing'),
 'current_host_abi_changed':('component/dependencies/p07-current-host/module988.sc','append'),
 'retained_sci_changed':('component/stock-sci/p13-domain-adapter/src/methods.sc.in','append'),
 'generated_source_changed':('component/stock-sci/p13-domain-adapter/src/module995.sc','append'),
 'fixture_changed':('component/tests/fixtures/p13/canonical-bindings.json','append'),
 'domain_tests_missing':('component/stock-sci/p13-domain-adapter/tests/test_domain.py','missing'),
 'join_tests_missing':('component/tests/test_p13_current.py','missing'),
 'join_test_removed':('component/tests/test_p13_current.py','test_removed'),
 'contest_owner_missing':('component/dependencies/vc_owner/verbal_contest.py','missing')}
rows=[]
for label,(relative,mode) in CASES.items():
 with tempfile.TemporaryDirectory(prefix='p13-admission-') as td:
  d=Path(td)/'packet'
  for folder in ('component','historical','provenance'):shutil.copytree(W/folder,d/folder,ignore=shutil.ignore_patterns('__pycache__'))
  p=d/relative
  if mode=='missing':p.unlink()
  elif mode=='partial':p.write_text('"""Partial model, deliberately invalid admission."""\n')
  elif mode=='test_removed':p.write_text(p.read_text().replace('def test_real_pending_autosaves_failure_write_readback_receipts','def removed_real_pending_autosaves_failure_write_readback_receipts'))
  else:p.write_bytes(p.read_bytes()+b'\nCHANGED_FOR_SCOPED_PROBE\n')
  for opt in (False,True):
   r=subprocess.run([sys.executable,*(['-O'] if opt else []),str(d/'component/tools/run_tests.py')],capture_output=True,text=True)
   log=E/(label+('-optimized' if opt else '-normal')+'.log');log.write_text(r.stdout+r.stderr)
   if r.returncode==0:raise RuntimeError('Invalid packet admitted '+label)
   rows.append(dict(case=label,optimized=opt,exit_code=r.returncode,log=str(log.relative_to(W))))
(W/'evidence/admission-probes.json').write_text(json.dumps(dict(status='PASS',cases=rows,scope='13 scoped mutation cases, normal and optimized rejection; not exhaustive arbitrary-state security'),indent=2)+'\n')
print('PASS',len(rows),'scoped rejections')
