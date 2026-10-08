"""Fresh spaced-path build and finite tests, never changing the original output."""
from pathlib import Path
import shutil,subprocess,sys,json,hashlib
H=Path(__file__).resolve().parents[1];D=H/'relocated/clean spaced path/p13-domain-reconstruction'
def main():
 if D.exists():shutil.rmtree(D)
 shutil.copytree(H,D,ignore=shutil.ignore_patterns('delivery','probes','relocated','__pycache__'))
 shutil.rmtree(D/'build')
 results=[]
 commands=[['generate.py'],['build.py'],['run_tests.py','domain'],['run_tests.py','validation'],['run_tests.py','finite'],['tools/probe_current.py'],['tools/audit_emission.py']]
 for i,args in enumerate(commands):
  p=subprocess.run([sys.executable,'-B',*args],cwd=D,capture_output=True,text=True);log=p.stdout+p.stderr
  (H/f'evidence/relocation-{i}.log').write_text(log)
  results.append(dict(command=args,returncode=p.returncode))
  if p.returncode:raise RuntimeError(('Fresh relocation failed',args,log))
 p=subprocess.run([sys.executable,'-B',str(H/'tools/compare_relocation.py'),str(D)],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 for f in ['build/isolated/selectors.json','build/isolated/selector-list.json']:
  if (H/f).read_bytes()!=(D/f).read_bytes():raise RuntimeError('Selector relocation changed')
 for group in ['domain','validation','finite']:
  shutil.copy2(D/f'evidence/verified-{group}.json',H/f'evidence/relocated-verified-{group}.json')
 shutil.copy2(D/'evidence/current-emitted.json',H/'evidence/relocated-current-emitted.json')
 (H/'evidence/relocation.json').write_text(json.dumps(dict(status='PASS',spaced_path=str(D.relative_to(H)),commands=results,source_script_heap_selectors_exact=True,normalized_abi_exact=True,native_acceptance=False),indent=2)+'\n');print('PASS_SPACED_PATH_FULL_FINITE_REBUILD')
if __name__=='__main__':main()
