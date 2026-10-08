"""Mutate the disposable cold rebuild only; retain every input failure as evidence."""
from pathlib import Path
import json,sys,subprocess
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from guard import require,sha
import run

def main():
 run.output_check();target=H/'portability/cold source only/P14 component';require(target.is_dir(),'Cold reconstruction required');results=[]
 def check(name,operation,undo,opt=False):
  try:
   operation();cmd=[sys.executable,'-O' if opt else '-B',str(target/'run.py'),'verify'];p=subprocess.run(cmd,cwd=target,capture_output=True,text=True);v=json.loads((target/'VERIFICATION.json').read_text());require(p.returncode!=0 and v['status']=='FAILED','Invalid candidate admitted '+name);results.append(dict(probe=name,rejected=True,stale_pass_cleared=True,reason=v['reason']))
  finally:undo()
 def bytes_case(name,path,change):
  p=target/path;original=p.read_bytes();check(name,lambda:p.write_bytes(change(original)),lambda:p.write_bytes(original))
 bytes_case('source_tamper','caption_layout.py',lambda b:b+b'\n# mutation\n')
 bytes_case('input_tamper','inputs/canonical-bindings.json',lambda b:b+b' ')
 bytes_case('output_tamper','generated/215.text.bin',lambda b:b'X'+b[1:])
 p=target/'generated/215.text.bin';original=p.read_bytes();check('output_missing',p.unlink,lambda:p.write_bytes(original))
 for name,path in [('extra_output','generated/unexpected.bin'),('extra_source','unsealed_probe.py'),('extra_input','inputs/unexpected.bin')]:
  p=target/path;check(name,lambda p=p:p.write_bytes(b'probe'),lambda p=p:p.unlink())
 p=target/'tools/probe-link.py';check('source_symlink',lambda:p.symlink_to(target/'caption_layout.py'),p.unlink)
 bytes_case('stale_test_gate','evidence/tests.json',lambda b:b.replace(b'"PASS"',b'"FAILED"',1))
 p=target/'GATE-SEAL.json';check('forged_gate_seal',lambda:p.write_text('{}'),p.unlink)
 check('optimized_python',lambda:None,lambda:None,opt=True)
 p=subprocess.run([sys.executable,'-B',str(target/'run.py'),'verify'],cwd=target,capture_output=True,text=True);require(p.returncode==0,'Restored cold fixture is not valid')
 r=dict(status='PASS',checks=len(results),results=results,source_seal_sha256=sha(H/'SOURCE-SEAL.json'),output_seal_sha256=sha(H/'OUTPUT-SEAL.json'));(H/'evidence/negative-checks.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
if __name__=='__main__':main()
