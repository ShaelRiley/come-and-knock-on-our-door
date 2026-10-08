"""NEW ordinary composed owner readbacks across P14 consent and finale boundaries.
Reference-file coordination only; not an atomic native host save implementation.
"""
from pathlib import Path
from dataclasses import replace
import sys,json,os,time
H=Path(__file__).resolve().parents[1];C=H/'reference/component';sys.dont_write_bytecode=True
sys.path[:0]=[str(H/'tests'),str(H),str(C),str(C/'tests')]
if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
from verify_source import verify
verify()
from joined_pair import FinaleJoined,JoinedPair,N
from current_join import MemoryTransactionHost,P04,P08World,P09World,P10World,P11World,P12World,P13World,PEOPLE
from cakood.p14_model import P14World,TERMS,PENCIL
from cakood.verbal_contest import VerbalContests
from paired import restore_words,MEASUREMENTS
from test_domain import finale_context
x=FinaleJoined();rows=[];start=time.monotonic()
def roundtrip(label):
 j=x.j
 before=dict(p14=x.w.save(),words=list(x.w.h.v.persistent().values()),p13=j.w.save(),p7=j.h7.save_campaign_fixture(),p11=j.p11.save(),p12=j.p12.save(),p8=j.p8.save(),p9=j.p9.save(),p10=j.p10.save(),p4=j.p4.save(),vc=j.vc.save_with_evidence(),actors=dict(j.actors),physical=dict(j.physical),queue=j.queue_clear,board=j.board_room,inventory=sorted(x.inventory),terms_owner=x.terms_owner,pencil_owner=x.pencil_owner)
 path=H/'evidence/owner-readbacks'/f'{len(rows):03}-{label}.json';path.parent.mkdir(exist_ok=True)
 with path.open('w') as f:json.dump(before,f,indent=2);f.flush();os.fsync(f.fileno())
 saved=json.loads(path.read_text())
 j.p7,j.h7=MemoryTransactionHost.load_campaign_fixture(saved['p7'],j.c7);j.c7=replace(j.c7,ownership=j.h7.ownership_context())
 j.p11=P11World.load(saved['p11']);j.p12=P12World.load(saved['p12']);j.p8=P08World.load(saved['p8']);j.p9=P09World.load(saved['p9']);j.p10=P10World.load(saved['p10']);j.p4=P04();j.p4.load(saved['p4'])
 j.vc=VerbalContests.load_with_evidence(saved['vc'],owner_generation=j.vc.owner_generation+1);j.c12=replace(j.c12,contests=j.vc)
 j.actors=saved['actors'];j.physical={k:tuple(v) for k,v in saved['physical'].items()};j.queue_clear=saved['queue'];j.board_room=saved['board'];j.w=P13World.load(saved['p13'],context=j.context())
 x.inventory=set(saved['inventory']);x.terms_owner=saved['terms_owner'];x.pencil_owner=saved['pencil_owner'];x.w=P14World.load(saved['p14']);x.w.h.v=restore_words(saved['words']);x.w._project(x.context());x.w.h.queries()
 after=dict(p13=j.w.save(),p7=j.h7.save_campaign_fixture(),p11=j.p11.save(),p12=j.p12.save(),p8=j.p8.save(),p9=j.p9.save(),p10=j.p10.save(),p4=j.p4.save(),vc=j.vc.save_with_evidence(),p14=x.w.save(),words=list(x.w.h.v.persistent().values()))
 for key,value in after.items():
  if value!=before[key]:raise AssertionError(('ordinary owner restore changed state',label,key))
 rows.append(dict(label=label,file=str(path.relative_to(H)),first_wins=dict(x.w.winning_attempts),native_atomic_save=False))
roundtrip('practical-p13-loss');x.win_all();roundtrip('four-real-wins');x.start();roundtrip('commitments-start')
for person in PEOPLE:
 r=x.w.give_card(x.context(),person,person);x.w.acknowledge_presentation(x.context(),r.presentation_id,record_id=x.w.SOURCES['approve:'+person]);roundtrip('approve-'+person);x.w.pin_card(x.context(),person);roundtrip('pin-'+person)
x.show('signature');roundtrip('explicit-consent-read');x.event(x.w.pin_signature(x.context()));roundtrip('explicit-signature');x.event(x.w.give_pencil(x.context()));roundtrip('original-pencil-handoff')
for source in ('date','readback','return_pencil'):x.show(source);roundtrip(source)
x.event(x.w.complete_commitments(x.context()));roundtrip('game-complete');x.w.start_finale();roundtrip('finale-start')
for source in ('closing:professional','meal','tag'):
 c=finale_context(x.context(),source);r=x.w.begin_presentation(c,source);x.w.acknowledge_presentation(c,r.presentation_id,record_id=x.w.SOURCES[source]);x.w.advance_finale();roundtrip(source.replace(':','-'))
x.w.acknowledge_freeze(x.w.pending_freeze_id);roundtrip('freeze-logical-receipt');x.w.claim_celebration();x.w.advance_finale();roundtrip('credits-start')
first=x.w.credit_ids[0];x.show('credit:'+first);x.w.advance_finale();x.w.pause_finale(True);roundtrip('credits-one-paused');x.w.skip_finale();roundtrip('viewer-close')
report=dict(status='PASS',restarts=len(rows),rows=rows,paired=MEASUREMENTS,joined=N,elapsed_seconds=time.monotonic()-start,scope='Actual Python upstream owners plus source/emitted P14; fsync/readback ordinary reference JSON, not native atomic ownership or SaveGame')
(H/'evidence/owner-restarts.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS_ORDINARY_OWNER_RESTARTS',len(rows),MEASUREMENTS)
