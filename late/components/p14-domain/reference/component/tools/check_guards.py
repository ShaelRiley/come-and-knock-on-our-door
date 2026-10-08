"""NEW bounded required-input admission probes, never arbitrary-save research."""
from pathlib import Path
import shutil,tempfile,subprocess,json,sys
W=Path(__file__).resolve().parents[2]
CASES={
 'historical_model_missing':('historical/literal-read/cakood/p14_model.py','delete'),
 'canonical_authority_changed':('component/authority/full-line-catalog.json','append'),
 'accepted_owner_changed':('component/dependencies/vc_owner/verbal_contest.py','append'),
 'accepted_p13_changed':('component/cakood/p13_model.py','append'),
 'accepted_p12_missing':('component/cakood/p12_model.py','delete'),
 'genuine_p09_missing':('component/cakood/p09_model.py','delete'),
 'observer_missing':('component/cakood/contest_evidence.py','delete'),
 'working_model_changed':('component/cakood/p14_model.py','append'),
 'retained_sci_changed':('component/stock-sci/p14-domain-adapter/src/methods.sc.in','append'),
 'retained_codec_changed':('component/stock-sci/p14-domain-adapter/codec.py','append'),
 'source_generated_changed':('component/stock-sci/p14-domain-adapter/src/module996.sc','append'),
 'fixture_changed':('component/tests/fixtures/p14/canonical-bindings.json','json'),
 'current_abi_changed':('component/dependencies/p13-current-manifest.json','append'),
 'domain_tests_missing':('component/stock-sci/p14-domain-adapter/tests/test_domain.py','delete'),
 'join_test_removed':('component/tests/test_p14_current.py','remove_test'),
 'required_names_changed':('component/tests/EXPECTED-TESTS.json','json'),
}
def main():
 out=W/'evidence/guard-logs';out.mkdir(exist_ok=True);rows=[]
 with tempfile.TemporaryDirectory(prefix='p14 guard ') as td:
  dest=Path(td)/'source only';shutil.copytree(W,dest,ignore=shutil.ignore_patterns('delivery','probes','__pycache__','.library-current'))
  for name,(relative,operation) in CASES.items():
   p=dest/relative;original=p.read_bytes()
   if operation=='delete':p.unlink()
   elif operation=='json':p.write_text('{}\n')
   elif operation=='remove_test':p.write_text(p.read_text().replace('def test_real_p13_loss_completes_practical_work_but_no_signature','def removed_real_p13_loss_completes_practical_work_but_no_signature'))
   else:p.write_bytes(original+b'\n# scoped admission change\n')
   for optimized in (False,True):
    cmd=[sys.executable,*(['-O'] if optimized else []),str(dest/'component/tools/run_tests.py'),'--admit-only']
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
    log=r.stdout+r.stderr;(out/f'{name}-{"optimized" if optimized else "normal"}.log').write_text(log)
    if r.returncode==0:raise RuntimeError('Changed input admitted: '+name)
    rows.append({'case':name,'optimized':optimized,'returncode':r.returncode,'rejected':True})
   p.write_bytes(original)
 (W/'evidence/admission-probes.json').write_text(json.dumps({'scope':'32 bounded missing/changed-input probes; source gate only','cases':rows,'passed':True},indent=2)+'\n')
 print('Required-input guards: all',len(rows),'rejected before tests')
if __name__=='__main__':main()
