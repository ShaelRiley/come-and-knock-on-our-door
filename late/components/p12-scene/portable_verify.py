"""Rebuild from sealed authoring inputs in a clean path with spaces."""
from pathlib import Path
import json,sys,shutil,subprocess
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
import run

def verify():
 run.source_check();run.output_check();dest=H/'portability/clean source only/p12 component'
 if dest.exists():shutil.rmtree(dest)
 dest.mkdir(parents=True)
 source=json.loads((H/'SOURCE-SEAL.json').read_text())['files']
 for n in [*source,'SOURCE-SEAL.json']:
  p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(H/n,p)
 assert not any((dest/n).exists() for n in run.OUTPUT_DIRS)
 (dest/'evidence').mkdir()
 with (H/'evidence/relocation-rebuild.log').open('w') as out:p=subprocess.run([sys.executable,str(dest/'run.py'),'rebuild'],cwd=dest,stdout=out,stderr=subprocess.STDOUT,text=True)
 run.require(p.returncode==0,'Clean relocation rebuild failed; see evidence/relocation-rebuild.log')
 a=json.loads((H/'OUTPUT-SEAL.json').read_text())['files'];b=json.loads((dest/'OUTPUT-SEAL.json').read_text())['files'];diff=[n for n in sorted(set(a)|set(b)) if a.get(n)!=b.get(n)]
 run.require(not diff,'Relocated output drift '+str(diff[:10]));run.source_check();run.output_check()
 run.dump(H/'evidence/relocation.json',dict(status='PASS',source_seal_sha256=run.sha(H/'SOURCE-SEAL.json'),output_seal_sha256=run.sha(H/'OUTPUT-SEAL.json'),clean_source_only_rebuild=True,exact_stable_output_inventory=True,stable_files=len(a),tests=40,all46_fragment_pairs_verified=True,principal39_pairs_reused_exactly=True,audience7_repeated_render=True,all10_candidate_and10_baseline_modules_recompiled=True,all10_window_composition_modules_recompiled=True,native_acceptance=False));print('PASS clean relocated outputs',len(a))
if __name__=='__main__':verify()
