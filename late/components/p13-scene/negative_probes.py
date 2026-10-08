"""Bounded altered-copy admission/package tests; the accepted workroot stays intact."""
from pathlib import Path
import sys,json,shutil,subprocess
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
import run

def verify():
 run.source_check();run.output_check();dest=H/'probes/disposable component';dest.parent.mkdir(exist_ok=True)
 if dest.exists():shutil.rmtree(dest)
 source=json.loads((H/'SOURCE-SEAL.json').read_text())['files'];output=json.loads((H/'OUTPUT-SEAL.json').read_text())['files']
 for n in [*source,*output,'SOURCE-SEAL.json','OUTPUT-SEAL.json']:
  p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(H/n,p)
 def call():
  p=subprocess.run([sys.executable,str(dest/'run.py'),'verify'],cwd=dest,capture_output=True,text=True);status=json.loads((dest/'VERIFICATION.json').read_text());return p,status
 p,status=call();assert p.returncode==0 and status['status']=='PASS_BOUND_COMPONENT'
 checks=['source_tamper','input_tamper','output_tamper','output_missing','output_extra','symlink','gate_tamper','unsealed_extra_source'];results=[]
 for name in checks:
  target={'source_tamper':'mapping.py','input_tamper':'inputs/domain/schema.json','output_tamper':'generated/214.text.bin','output_missing':'generated/214.text.bin','output_extra':'generated/unsealed.txt','symlink':'generated/214.text.bin','gate_tamper':'GATE-SEAL.json','unsealed_extra_source':'unsealed.py'}[name]
  path=dest/target;old=path.read_bytes() if path.exists() else None
  if name in ['source_tamper','input_tamper','output_tamper']:path.write_bytes(old+b'\n')
  elif name=='output_missing':path.unlink()
  elif name=='symlink':path.unlink();path.symlink_to(dest/'inputs/p08/generated/208.text.bin')
  elif name=='gate_tamper':path.write_text(json.dumps(dict(files={},source_seal_sha256='wrong',output_seal_sha256='wrong')))
  else:path.write_text('unsealed extra')
  p,status=call();assert p.returncode!=0 and status['status']=='FAILED',(name,p.stdout,p.stderr,status)
  results.append(dict(name=name,rejected=True,stale_pass_cleared=True,error=status['error']))
  path.unlink(missing_ok=True)
  if old is not None:path.write_bytes(old)
  p,status=call();assert p.returncode==0 and status['status']=='PASS_BOUND_COMPONENT',name
 run.source_check();run.output_check();run.dump(H/'evidence/negative-checks.json',dict(status='PASS',source_seal_sha256=run.sha(H/'SOURCE-SEAL.json'),output_seal_sha256=run.sha(H/'OUTPUT-SEAL.json'),checks=checks,results=results,native_acceptance=False));print('PASS eight admission negatives and baseline restorations')
if __name__=='__main__':verify()
