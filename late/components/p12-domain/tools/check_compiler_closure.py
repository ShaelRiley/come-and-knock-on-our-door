"""Focused R2 closure admission probes; no game behavior matrix replay."""
from pathlib import Path
import json,shutil,subprocess,sys
H=Path(__file__).resolve().parents[1];P=H/'probes/closure correction'
def main():
 cases=[('extra source','toolchain/source/lucasartsifier/unused-gui.cpp','extra','closure membership'),('missing notice','toolchain/source/lucasartsifier/DOWNSTREAM-PACKAGING-NOTICE.md','missing','Immutable input mismatch'),('changed notice','toolchain/source/lucasartsifier/third-party-notices/fmt-BSD-2-Clause-NOTICE.txt','append','Immutable input mismatch'),('changed compiler manifest','toolchain/SOURCE-MANIFEST.json','append','Immutable input mismatch'),('changed dependency closure','toolchain/COMPILER-DEPENDENCY-CLOSURE.json','append','Immutable input mismatch'),('changed compiler','toolchain/scicompile','append','Immutable input mismatch'),('changed required source','toolchain/source/lucasartsifier/tools/scicompile/main.cpp','append','Immutable input mismatch'),('source removed from inventory','toolchain/source/lucasartsifier/tools/scicompile/main.cpp','unpin_then_append','Audited R2 compiler source mismatch'),('changed authority','reference/component/authority/full-line-catalog.json','append','Immutable input mismatch')]
 results=[]
 for name,relative,action,needle in cases:
  dst=P/name
  if dst.exists():shutil.rmtree(dst)
  shutil.copytree(H,dst,ignore=shutil.ignore_patterns('probes','delivery','relocated','__pycache__'))
  path=dst/relative
  if action=='missing':path.unlink()
  elif action=='extra':path.write_text('// deliberately excluded closure probe\n')
  else:
   path.write_bytes(path.read_bytes()+b'\nCLOSURE_PROBE\n')
   if action=='unpin_then_append':
    p=dst/'INPUT-INVENTORY.json';m=json.loads(p.read_text());m['files']=[r for r in m['files'] if r['path']!=relative];p.write_text(json.dumps(m))
  for optimized in (False,True):
   proc=subprocess.run([sys.executable,*(['-O'] if optimized else []),'-B','verify_inputs.py'],cwd=dst,capture_output=True,text=True);log=proc.stdout+proc.stderr
   if proc.returncode==0 or needle not in log:raise RuntimeError((name,optimized,proc.returncode,log))
   results.append(dict(case=name,optimized=optimized,exit_code=proc.returncode,expected=needle,output=log.replace(str(dst),'<probe>')))
 (H/'evidence/compiler-closure-admission.json').write_text(json.dumps(dict(status='PASS',probes=results),indent=2)+'\n');print('PASS_FOCUSED_CLOSURE_GUARDS',len(results))
if __name__=='__main__':main()
