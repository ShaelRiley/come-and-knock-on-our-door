#!/usr/bin/env python3
"""Two fresh compilations, comparing exact source/manifest/emitted artifact bytes."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
H=Path(__file__).resolve().parents[1]
FILES=['src/module993.sc','manifest.json','build/isolated/compiled/0.scr.bin','build/isolated/compiled/0.scr.bin.hep','build/isolated/compiled/993.scr.bin','build/isolated/compiled/993.scr.bin.hep','build/isolated/selectors.json','build/isolated/selector-list.json','build/isolated/ABI-MAPPINGS.json']
def snapshot():return {p:hashlib.sha256((H/p).read_bytes()).hexdigest() for p in FILES}
def main():
 if sys.flags.optimize:raise RuntimeError('Optimized verification forbidden')
 results=[]
 for index in (1,2):
  b=H/'build/isolated'
  if b.exists():shutil.rmtree(b)
  log=''
  for script in ('generate.py','build.py'):
   r=subprocess.run([sys.executable,'-B',script],cwd=H,capture_output=True,text=True)
   log+=r.stdout+r.stderr
   if r.returncode:
    (H/f'evidence/clean-rebuild-{index}.log').write_text(log);raise RuntimeError(('Clean rebuild failed',index,script))
  (H/f'evidence/clean-rebuild-{index}.log').write_text(log);results.append(snapshot())
 if results[0]!=results[1]:raise RuntimeError('Nondeterministic clean rebuild')
 (H/'evidence/clean-rebuild.json').write_text(json.dumps(dict(status='PASS_EXACT_TWO_CLEAN_BUILDS',artifacts=results[1],native_acceptance=False),indent=2)+'\n')
 print('PASS_EXACT_TWO_CLEAN_BUILDS',len(FILES),'artifacts')
if __name__=='__main__':main()
