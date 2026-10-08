"""NEW reproduction of pre-existing helper's unordered/unlearned alias choice."""
from pathlib import Path
import subprocess,sys,os,json
W=Path(__file__).resolve().parent
code='''from pathlib import Path
import sys,importlib.util
W=Path(sys.argv[1]);C=W/'component';sys.path[:0]=[str(C),str(C/'tests')]
spec=importlib.util.spec_from_file_location('original_helper',W/'historical/accepted-p13/test_verbal_contest.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
w=m.VerbalContests(m.CATALOG)
for enc in ('VC01','VC02','VC03','VC04'):m.prepared(enc,w);m.play(w,[True]*3,enc);m.leave(w)
print('Four original helper wins completed')
'''
rows=[]
for seed in range(20):
 r=subprocess.run([sys.executable,'-c',code,str(W)],capture_output=True,text=True,env={**os.environ,'PYTHONHASHSEED':str(seed)})
 rows.append({'seed':seed,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 if r.returncode:break
if not rows[-1]['returncode']:raise RuntimeError('Original helper issue did not reproduce')
(W/'evidence/original-helper-alias-failure.json').write_text(json.dumps({'scope':'Test helper compatibility contrast only; accepted owner unchanged','original':rows,'correction':'Select a deterministic actual learned response from accepted_response_ids intersect available_responses'},indent=2)+'\n')
print('Preserved old helper failure at PYTHONHASHSEED',rows[-1]['seed'])
