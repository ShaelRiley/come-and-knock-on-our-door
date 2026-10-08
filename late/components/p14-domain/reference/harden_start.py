"""NEW current compatibility admission fix, supported by preserved failure."""
from pathlib import Path
import sys,json,dataclasses
W=Path(__file__).resolve().parent;C=W/'component';sys.path[:0]=[str(C),str(C/'tests')]
from cakood.p14_model import P14World
from cakood.verbal_contest import VerbalContests
from test_late_campaign_models import contests,c14,UNSIGNED
v=contests(wins=('VC01','VC02','VC03','VC04'));unpaired=VerbalContests.load(v.save(),owner_generation=2)
w=P14World();before=w.save()
try:w.start(c14(unpaired),UNSIGNED)
except ValueError as e:
 result={'scope':'Original literal method with actual owner plus new observation bridge, aggregate-only historical save','exception':str(e),'before':before,'state_after_exception':{k:v for k,v in dataclasses.asdict(w).items() if not k.startswith('_')}}
try:w.validate()
except ValueError as e:result['post_failure_validation_error']=str(e)
(W/'evidence/original-start-partial-mutation.json').write_text(json.dumps(result,indent=2)+'\n')
p=C/'cakood/p14_model.py';s=p.read_text()
old="""        self.entry_flags=sorted(PREREQUISITES)
        self.winning_attempts={encounter:next(a.outcome.id for a in c.contests.attempts
            if a.encounter_id==encounter and a.outcome is not None and a.outcome.winner=='jack') for encounter in CONTEST_IDS}
"""
new="""        # NEW current-owner ABI admission: collect every genuine observation
        # before mutating durable state; aggregate-only saves cannot supply it.
        winning_attempts={encounter:next(a.outcome.id for a in c.contests.attempts
            if a.encounter_id==encounter and a.outcome is not None and a.outcome.winner=='jack') for encounter in CONTEST_IDS}
        self.entry_flags=sorted(PREREQUISITES)
        self.winning_attempts=winning_attempts
"""
if s.count(old)!=1:raise RuntimeError('Literal start boundary changed')
p.write_text(s.replace(old,new))
p=W/'provenance/input-inventory.json';rows=json.loads(p.read_text())
for r in rows:
 if r['target']=='component/cakood/p14_model.py':r['pinned']=False
p.write_text(json.dumps(rows,indent=2)+'\n')
print('Moved genuine win-evidence collection before durable entry mutation')
