"""NEW review-time exact source seal; runtime verification never reseals inputs."""
from pathlib import Path
import json,hashlib,sys,unittest,difflib
W=Path(__file__).resolve().parent;C=W/'component';D=C/'stock-sci/p14-domain-adapter';sys.path[:0]=[str(C),str(C/'tests'),str(D),str(D/'tests')]
from tools.assertions import load
names=[]
def cases(s):
 for item in s:
  if isinstance(item,unittest.TestSuite):yield from cases(item)
  else:yield item.id()
for p in (D/'tests/test_domain.py',D/'tests/test_validation.py',C/'tests/test_p14_current.py',C/'tests/test_p14_pairing.py'):
 m=load(p.stem,p);names.extend(cases(unittest.defaultTestLoader.loadTestsFromModule(m)))
(C/'tests/EXPECTED-TESTS.json').write_text(json.dumps(sorted(names),indent=2)+'\n')
pins={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(C.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and (p.suffix=='.py' or p.name=='EXPECTED-TESTS.json')}
(W/'provenance/working-source-pins.json').write_text(json.dumps(pins,indent=2)+'\n')
rows=json.loads((W/'provenance/input-inventory.json').read_text());diffs=[]
for r in rows:
 target=W/r['target']
 if not target.exists():continue
 if not r['pinned']:
  if r['target']=='component/cakood/verbal_contest.py':origin=W/'historical/accepted-p13/verbal_contest.py'
  elif r['target']=='component/tests/test_verbal_contest.py':origin=W/'historical/accepted-p13/test_verbal_contest.py'
  elif r['target']=='component/cakood/p14_model.py':origin=W/'historical/literal-read/cakood/p14_model.py'
  elif r['target'].startswith('component/stock-sci/'):
   origin=W/'historical/literal-final'/r['target'][len('component/'):]
  else:continue
  if origin.read_bytes()!=target.read_bytes():
   diff=''.join(difflib.unified_diff(origin.read_text().splitlines(True),target.read_text().splitlines(True),fromfile=str(origin.relative_to(W)),tofile=str(target.relative_to(W))))
   name=r['target'].replace('/','__')+'.diff';(W/'provenance'/name).write_text(diff)
   diffs.append({'target':r['target'],'original':str(origin.relative_to(W)),'original_sha256':hashlib.sha256(origin.read_bytes()).hexdigest(),'working_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'diff':name})
(W/'provenance/working-differences.json').write_text(json.dumps({'classification':'NEW portability/current-owner ABI/source-only test adaptations; exact differences below','files':diffs},indent=2)+'\n')
print('Sealed',len(pins),'working sources;',len(names),'named tests;',len(diffs),'recovered/accepted-file diffs')
