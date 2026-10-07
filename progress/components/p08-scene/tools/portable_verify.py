"""Source-only clean relocation; outputs and proof cannot be imported as inputs."""
from pathlib import Path
import sys,json,hashlib,shutil,subprocess
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H));import run as entry
OUT=H/'evidence/portability.json';entry.dump(OUT,dict(status='RUNNING',native_acceptance=False))
try:
 entry.require(not sys.flags.optimize,'Optimized Python forbidden');entry.source_check();entry.outputs_check()
 D=H/'portability';D.mkdir(exist_ok=True);root=D/'clean source only with spaces'
 if root.exists():shutil.rmtree(root)
 root.mkdir();source=json.loads((H/'SOURCE-SEAL.json').read_text())['files']
 for name,digest in source.items():
  p=root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(H/name,p)
 shutil.copy2(H/'SOURCE-SEAL.json',root/'SOURCE-SEAL.json');(root/'evidence').mkdir(exist_ok=True)
 entry.require(not (root/'generated').exists() and not (root/'build').exists(),'Preexisting relocation outputs')
 process=subprocess.run([sys.executable,'-B','run.py','rebuild'],cwd=root,capture_output=True,text=True);(D/'source-only-rebuild.log').write_text(process.stdout+process.stderr)
 entry.require(process.returncode==0,'Source-only relocated rebuild failed; see portability/source-only-rebuild.log')
 def stable(base):return {str(p.relative_to(base)):entry.sha(p) for d in ['generated','build'] for p in sorted((base/d).rglob('*')) if p.is_file() and p.suffix!='.log'}
 a=stable(H);b=stable(root);entry.require(a==b,'Relocated output bytes differ: '+repr([k for k in set(a)|set(b) if a.get(k)!=b.get(k)]))
 entry.dump(OUT,dict(status='PASS',source_seal_sha256=entry.sha(H/'SOURCE-SEAL.json'),output_seal_sha256=entry.sha(H/'OUTPUT-SEAL.json'),stable_files=len(a),source_only_clean_relocation=True,all_ten_modules_recompiled=True,all_registered_tests_rerun=True,exact_generated_outputs=True,native_acceptance=False));print('Portable exact outputs',len(a))
 shutil.rmtree(root)
except BaseException as e:
 entry.dump(OUT,dict(status='FAILED',error=str(e),native_acceptance=False));raise
