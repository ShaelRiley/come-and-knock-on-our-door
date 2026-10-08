"""Reproduce P14 v1 mixed-branch observation acceptance with genuine owners.

No owner state or observation snapshot is hand-authored or rewritten. Two
branches start at the same paired public-owner save. Branch B claims one ordinary
logical result effect that branch A leaves unclaimed. That consumed earlier
effect disappears from the aggregate owner's later active-attempt projection,
so the final owner bytes coincide although the historical first wins differ.
"""
from pathlib import Path
import argparse, copy, hashlib, json, sys

parser=argparse.ArgumentParser()
parser.add_argument('--component',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
C=args.component.resolve();sys.path[:0]=[str(C),str(C/'tests')]
from cakood.verbal_contest import VerbalContests
from cakood.p14_model import P14World
from test_verbal_contest import prepared,play,leave
from test_late_campaign_models import c14,UNSIGNED

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(value):return hashlib.sha256(canonical(value)).hexdigest()
def first_win(owner):
    return next(a.outcome.id for a in owner.attempts if a.encounter_id=='VC01' and a.outcome.winner=='jack')

seed=prepared('VC01').save_with_evidence()
branches=[];action_traces=[]
for generation,outcomes in ((2,(True,False,False)),(3,(False,True,False))):
    owner=VerbalContests.load_with_evidence(copy.deepcopy(seed),owner_generation=generation)
    trace=[]
    for index,won in enumerate(outcomes):
        play(owner,[won]*3,'VC01')
        trace.append({'method':'real owner enter/begin_turn/acknowledge/choose_response/commit_response/commit_ko','encounter':'VC01','won':won,'serial':owner.active.serial})
        if generation==3 and index==0:
            result=owner.claim_effect(owner.active.outcome_id)
            if result is None:raise RuntimeError('Expected the real owner logical effect claim')
            trace.append({'method':'claim_effect','kind':result['kind'],'record_id':result['record_id'],'audio_played':False})
        leave(owner)
    for encounter in ('VC02','VC03','VC04'):
        prepared(encounter,owner);play(owner,[True]*3,encounter);leave(owner)
        trace.append({'method':'real owner prepare/play/leave','encounter':encounter,'won':True})
    branches.append(owner);action_traces.append(trace)

a,b=branches
if a.save()!=b.save():raise RuntimeError('Expected identical final ordinary owner bytes')
if (first_win(a),first_win(b))!=('VC01:A1:KO','VC01:A2:KO'):raise RuntimeError('Expected distinct genuine first-win chronology')
paired_a,paired_b=a.save_with_evidence(),b.save_with_evidence()
mixed=copy.deepcopy(paired_a);mixed['observations']=copy.deepcopy(paired_b['observations'])
args.output.mkdir(parents=True,exist_ok=True)
for name,data in [('seed',seed),('branch-a',paired_a),('branch-b',paired_b),('mixed-owner-a-observations-b',mixed)]:
    (args.output/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
accepted=False;result_code=None;winning_attempts=None;error=None
try:
    loaded=VerbalContests.load_with_evidence(mixed,owner_generation=4)
    world=P14World();result=world.start(c14(loaded),UNSIGNED)
    accepted=True;result_code=result.code;winning_attempts=world.winning_attempts
except ValueError as exc:error=str(exc)
report={
    'candidate':'P14 reference v1',
    'expected':'Reject the owner A / observation B mixed save before P14 admission',
    'actual':'ACCEPTED mixed save; first-win receipt substituted' if accepted else 'rejected',
    'defect_reproduced':accepted,
    'owner_a_first_win':first_win(a),'owner_b_first_win':first_win(b),
    'owner_a_revision':a.revision,'owner_b_revision':b.revision,
    'final_owner_bytes_identical':a.save()==b.save(),
    'raw_owner_sha256':hashlib.sha256(a.save()).hexdigest(),
    'observation_a_canonical_sha256':sha(paired_a['observations']),
    'observation_b_canonical_sha256':sha(paired_b['observations']),
    'paired_a_canonical_sha256':sha(paired_a),'paired_b_canonical_sha256':sha(paired_b),
    'mixed_canonical_sha256':sha(mixed),
    'result_code':result_code,'admitted_winning_attempts':winning_attempts,
    'rejection':error,'traces':action_traces,
    'scope':'ordinary branch/save-pairing consistency, genuine owner events; no native, atomic-storage or security claim',
}
(args.output/'result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if accepted:raise AssertionError('Mixed branch ledger accepted; P14 recorded VC01:A2:KO for the branch that won VC01:A1:KO')
