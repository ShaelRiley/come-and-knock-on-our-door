"""Admission negatives in disposable copies; assertion disabling is rejected."""
from pathlib import Path
import json,shutil,subprocess,sys
H=Path(__file__).resolve().parents[1];P=H/'probes/current guards'
def main():
 cases=[('optimized generation','generate.py',None),('optimized build','build.py',None),('optimized tests','run_tests.py',None),('changed catalog','verify_inputs.py','reference/component/authority/full-line-catalog.json'),('changed compiler','build.py','toolchain/scicompile'),('changed evaluator','build.py','tools/host_vm.py'),('missing test','run_tests.py','tests/test_domain.py'),('changed original','generate.py','historical/adapter/src/methods.sc.in'),('changed editable template','build.py','src/methods.sc.in'),('changed source','build.py','src/module995.sc'),('missing fixture','generate.py','reference/component/tests/fixtures/p13/canonical-bindings.json'),('changed registry','generate.py','reference/component/authority/retained-registry-subset.json'),('changed schema','build.py','manifest.json'),('changed bytecode','tests/harness.py','build/isolated/compiled/995.scr.bin'),('changed heap','tests/harness.py','build/isolated/compiled/995.scr.bin.hep'),('changed selectors','tests/harness.py','build/isolated/selector-list.json'),('changed ABI','tests/harness.py','build/isolated/ABI-MAPPINGS.json')]
 results=[]
 for label,script,relative in cases:
  dst=P/label
  if dst.exists():shutil.rmtree(dst)
  shutil.copytree(H,dst,ignore=shutil.ignore_patterns('probes','relocated','delivery','__pycache__'))
  if relative:
   path=dst/relative
   if label.startswith('missing'):path.unlink()
   else:path.write_bytes(path.read_bytes()+b'\nGUARD_PROBE\n')
  cmd=[sys.executable,*(['-O'] if label.startswith('optimized') else []),'-B',script]
  p=subprocess.run(cmd,cwd=dst,capture_output=True,text=True);log=p.stdout+p.stderr
  if p.returncode==0:raise RuntimeError((label,'Admitted invalid input'))
  results.append(dict(case=label,returncode=p.returncode,output=log.replace(str(dst),'<probe>')))
 sys.path.insert(0,str(H));from verify_source import syntax
 source=(H/'src/module995.sc').read_text()
 for label,extra,expected in [('boolean body hazard','(if 1 (== 1 2))','Bare Boolean'),('self arity','(self p13Clear: 1)','Self-send arity'),('comparison arity','(if (== 1 2 3) (return 0))','Comparison arity')]:
  changed=source.replace('(method (p13Init)', '(method (p13Init) '+extra,1)
  if changed==source:raise RuntimeError('Guard insertion missing')
  try:syntax(changed)
  except ValueError as e:
   if expected not in str(e):raise
   results.append(dict(case=label,rejected=str(e)))
  else:raise RuntimeError('Source syntax hazard admitted')
 (H/'evidence/guard-probes.json').write_text(json.dumps(dict(status='PASS',probes=results),indent=2)+'\n');print('PASS_CURRENT_GUARDS',len(results))
if __name__=='__main__':main()
