"""Bounded input, build and source structure tripwires in disposable copies."""
from pathlib import Path
import json,shutil,subprocess,sys,hashlib
H=Path(__file__).resolve().parents[1];P=H/'probes/current guards'
def main():
 cases=[('optimized generation','generate.py',None,None,'Optimized'),('optimized build','build.py',None,None,'Optimized'),('optimized tests','run_tests.py',None,None,'Optimized'),('changed catalog','generate.py','reference/component/authority/full-line-catalog.json','append','Immutable input mismatch'),('changed compiler','build.py','toolchain/scicompile','append','Immutable input mismatch'),('changed evaluator','build.py','tools/host_vm.py','append','Accepted evaluator/helper changed'),('missing test','run_tests.py','tests/test_domain.py','missing','Incomplete or unexpected discovery'),('changed original','generate.py','historical/src/methods.sc.in','append','Immutable input mismatch'),('changed editable template','build.py','src/methods.sc.in','append','Literal P12 template changed'),('changed emitted source','build.py','src/module994.sc','append','Generated binding mismatch'),('missing fixture','generate.py','reference/component/tests/fixtures/p12/canonical-bindings.json','missing','Immutable input mismatch'),('changed registry','generate.py','reference/component/authority/retained-registry-subset.json','append','Immutable input mismatch'),('bad object ABI','build.py','manifest.json','abi','External ABI mismatch'),('Boolean body hazard','build.py','src/module994.sc','boolean','Bare Boolean'),('self arity hazard','build.py','src/module994.sc','arity','Self-send arity mismatch')]
 results=[]
 for label,script,relative,action,needle in cases:
  dst=P/label
  if dst.exists():shutil.rmtree(dst)
  shutil.copytree(H,dst,ignore=shutil.ignore_patterns('probes','relocated','delivery','__pycache__'))
  if relative:
   path=dst/relative
   if action=='missing':path.unlink()
   elif action=='append':path.write_bytes(path.read_bytes()+b'\nGUARD_PROBE\n')
   elif action=='abi':
    m=json.loads(path.read_text());m['objects']['completed_screen']=80;path.write_text(json.dumps(m))
   else:
    s=path.read_text();needle_source='(= answer 0)\n (switch slot'
    if needle_source not in s:raise RuntimeError('Missing generated probe insertion')
    extra='(if 1 (== 1 2))' if action=='boolean' else '(self p12Clear: 1)'
    s=s.replace(needle_source,'(= answer 0)\n '+extra+'\n (switch slot',1);path.write_text(s)
    m=json.loads((dst/'manifest.json').read_text());m['source_sha256']=hashlib.sha256(path.read_bytes()).hexdigest();(dst/'manifest.json').write_text(json.dumps(m))
  cmd=[sys.executable,*(['-O'] if label.startswith('optimized') else []),'-B',script,*(['domain'] if script=='run_tests.py' else [])]
  p=subprocess.run(cmd,cwd=dst,capture_output=True,text=True);log=p.stdout+p.stderr
  (dst/'guard-result.log').write_text(log)
  if p.returncode==0 or needle not in log:raise RuntimeError((label,p.returncode,log))
  results.append(dict(case=label,returncode=p.returncode,expected=needle,output=log.replace(str(dst),'<probe>')))
 (H/'evidence/guard-probes.json').write_text(json.dumps(dict(status='PASS',probes=results),indent=2)+'\n');print('PASS_CURRENT_GUARDS',len(results))
if __name__=='__main__':main()
