"""NEW clean source-only spaced-path reconstruction and bounded representative banks."""
from pathlib import Path
import sys,shutil,json,subprocess,hashlib
H=Path(__file__).resolve().parents[1];D=H/'relocated/source only cold spaced path/p14-domain-reconstruction'
def ignore(path,names):
 return [n for n in names if n=='__pycache__' or (Path(path)==H and n in ('delivery','probes','relocated','build','evidence','checkpoints','PACKAGE-MANIFEST.json'))]
def main():
 if D.exists():raise ValueError('Relocation already exists; preserve it and choose a new disposable path')
 shutil.copytree(H,D,ignore=ignore);(D/'evidence').mkdir();results=[]
 commands=[['generate.py'],['build.py'],['run_tests.py','domain-02','domain-05','domain-07','domain-13','validation-01','validation-06'],['tools/run_finite_bank.py','3'],*([ 'tools/probe_current.py',str(i)] for i in [3,7,8,10]) ,['tools/probe_pairing.py'],['tools/audit_emission.py']]
 for i,args in enumerate(commands):
  p=subprocess.run([sys.executable,'-B',*args],cwd=D,capture_output=True,text=True);log=p.stdout+p.stderr
  (H/f'evidence/relocation-{i:02}.log').write_text(log);results.append(dict(command=args,returncode=p.returncode));print(i,args,p.returncode,flush=True)
  if p.returncode:raise RuntimeError(('Spaced relocation failed',args,log))
 p=subprocess.run([sys.executable,'-B',str(H/'tools/compare_relocation.py'),str(D)],capture_output=True,text=True)
 (H/'evidence/relocation-compare.log').write_text(p.stdout+p.stderr)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 for name in ['build/isolated/selectors.json','build/isolated/selector-list.json']:
  if (H/name).read_bytes()!=(D/name).read_bytes():raise ValueError('Selectors differ after relocation')
 result=dict(status='PASS',spaced_path=str(D.relative_to(H)),commands=results,source_script_heap_selectors_exact=True,normalized_abi_exact=True,native_acceptance=False,long_matrices_repeated=False)
 (H/'evidence/relocation.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS_SOURCE_ONLY_SPACED_REBUILD')
if __name__=='__main__':main()
