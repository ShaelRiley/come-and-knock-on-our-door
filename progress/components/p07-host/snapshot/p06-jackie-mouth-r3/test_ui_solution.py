"""Actual emitted UI event dispatcher solution, with explicit P01/P02 fixture.
No direct puzzle action, topic-choice, source-page or scoring calls are used.
The event/kernel interpreter is not native ScummVM or CUA.
"""
from pathlib import Path
import sys,json,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'tests'))
from host import setup,base
from test_practical import restore
OUT=H/'evidence/ui-solution.json';OUT.write_text('{"status":"RUNNING","native_acceptance":false}\n')
h,d,a,p,q,r=setup();s=h.vm.objects['p06State'];v=h.vm.objects['contestState'];h.vm.budget=300000000
# Explicit inherited prerequisites only. No P06/Contest flag or knowledge is seeded.
h.p['p01Consumed']=1
assert s.call('p06Projection',0)==0 and v.call('vcFlags')==0
assert not any(v.call('vcLearned',i,j) for i in range(1,25) for j in [1,2])
TRACE=[];READS=[]
def pump(events):
 h.vm.pump(events);assert h.p['uiFailure']==0,(h.p['uiFailure'],h.p['location'],h.p['uiPanel'])
def control(action,payload=None):
 h.call('uiBuildFocus')
 ids=[i for i in range(h.p['uiControlCount']) if h.arrays['uiActions'][i]==action and (payload is None or h.arrays['uiPayloads'][i]==payload)]
 assert ids,('missing actual control',action,payload,h.p['location'],h.p['uiPanel'],h.p['uiChoiceContext'])
 index=ids[0];left,top,right,bottom=[h.arrays[n][index] for n in ['uiLefts','uiTops','uiRights','uiBottoms']]
 # Find a real unoccluded pixel of the control. Reverse hit order is authoritative.
 point=None
 for x,y in [((left+right)//2,(top+bottom)//2)]+[(x,y) for y in range(top,bottom) for x in range(left,right)]:
  if h.call('uiHit',x,y)==index:point=(x,y);break
 assert point,('control entirely covered',action,payload)
 TRACE.append({'control':action,'payload':h.arrays['uiPayloads'][index],'point':point,'room':h.p['location'],'panel':h.p['uiPanel'],'context':h.p['uiChoiceContext'],'page':h.p['uiPage']})
 pump([{'type':1,'x':point[0],'y':point[1]},{}])
def scenes():
 for _ in range(200):
  if h.p['uiPanel'] not in [1,4]:return
  pump([{}]);READS.append([h.p['uiDocument'],h.p['uiPage'],h.p['uiPageCount']])
  if h.p['uiPage']+1<h.p['uiPageCount']:control(11,0)
  else:control(12,0)
 raise RuntimeError('Scene did not terminate')
def world():
 scenes()
 if h.p['uiPanel']==2:control(12,0)
 assert h.p['uiPanel']==0
 pump([{'type':4,'message':27},{}])
def arrival():
 for _ in range(200):
  if not h.p['motionPhase']:return
  pump([{}])
 raise RuntimeError('Approach never arrived')
def action(verb,obj,target=None):
 world()
 if verb:control(2,verb)
 h.call('uiBuildFocus')
 mode=3 if any(h.arrays['uiActions'][i]==3 and h.arrays['uiPayloads'][i]==obj for i in range(h.p['uiControlCount'])) else 1
 control(mode,obj)
 if target is not None:
  assert h.p['uiNounA']==obj,('first noun not retained',obj,h.p['uiNounA'])
  control(1,target)
 arrival();scenes()
 TRACE.append({'completed_action':[verb,obj,target],'room':h.p['location'],'panel':h.p['uiPanel'],'context':h.p['uiChoiceContext']})
def choose(context,choice_id,read=True):
 assert (h.p['uiPanel'],h.p['uiChoiceContext'])==(2,context),(context,choice_id,h.p['uiPanel'],h.p['uiChoiceContext'])
 slots=[i for i in range(h.p['uiChoiceCount']) if h.arrays['uiChoiceIds'][i]==choice_id];assert len(slots)==1
 wanted=slots[0]
 while h.p['uiPage']<wanted:control(11,0)
 while h.p['uiPage']>wanted:control(10,0)
 control(13,wanted)
 if read:scenes()

action(6,8);choose(202,11)
assert s.call('p06Read',8)>0
action(0,12);action(4,75);assert s.call('p06Projection',1)==1
action(0,18);action(0,17);action(0,14);action(4,76)
action(0,17);action(5,82);action(5,77)
assert s.call('p06Journal',1)==10 and s.call('p06Journal',3)==18
action(6,85);choose(219,1)
action(7,75,73);choose(221,1);assert s.call('p06Projection',5)==1
# Reversal uses two real nouns, selecting the draped world sheet and bare frame.
action(7,75,73);choose(221,2);action(7,76,74)
assert s.call('p06Projection',5)==3
action(8,80);choose(222,2);assert s.call('p06Projection',4)==0
action(8,80);choose(222,1);assert (s.call('p06Projection',3),s.call('p06Projection',4))==(1,1)
action(6,85);choose(219,6)
for pair in range(1,13):choose(215,1);choose(216,pair)
assert v.call('vcRead',6)==0 and all(v.call('vcLearned',i,j) for i in range(1,13) for j in [1,2])
choose(215,2);assert (v.call('vcRead',91),v.call('vcRead',92))==(2,3)
# Start a genuine reply to bind the mouth path to the real player-owned PCM lane.
pair=v.call('vcRead',106+v.call('vcRead',95));choose(217,pair);choose(218,1,read=False);pump([{},{}])
assert a.p['lane']==1 and a.p['speaker']==1,(a.p['lane'],a.p['speaker'])
for muted in [0,1]:
 a.call('setOff',1,muted);a.p['mouth']=2;h.vm.ktrace=[];h.p['dirty']=1;pump([{}])
 assert any(n=='DrawCel' and args[0]==216 and args[1]==1 for n,args in h.vm.ktrace)
 if muted:assert a.call('ownerGain')==0
state=h.vm.snapshot();score=(v.call('vcRead',96),v.call('vcRead',97));played=a.p['played']
restore(h,state,[{},{}]);assert s.p['h6RestoreValid']==1
assert (a.p['lane'],a.p['mouth'],d.p['sdPendingStart'])==(0,0,0)
assert a.p['played']==played and (v.call('vcRead',96),v.call('vcRead',97))==score
scenes();assert h.p['uiChoiceContext']==217
choose(217,26);assert v.call('vcFlags')==2 and v.call('vcRead',101)==2
assert any(record==50 and unit==16 for record,unit in [(x['record'],x['unit']) for x in h.vm.receipts])
assert any(record==50 and unit==17 for record,unit in [(x['record'],x['unit']) for x in h.vm.receipts])
action(6,85);choose(219,7)
assert (s.call('p06Projection',0),s.p['h6ScreenRoom'],s.p['h6ScreenPosition'])==(7,4,0)
assert not any(i in [75,76] for i in h.arrays['uiItems'])
report={'status':'PASS','fixture':'P01 complete/P02 plan agreed only; zero P06 and Contest progress/knowledge initially','control_dispatch':'actual mouse GetEvent -> uiPointer/uiHit/uiActivate; Escape key; real approach/arrival and paginated choices/readers','direct_gameplay_action_or_choice_calls':False,'steps':TRACE,'read_pages':READS,'instructions':h.vm.steps,'frames':h.vm.frames,'normal_muted_restore_mouth':'PASS, real VC02 reply; retained216, zero muted gain, no audio/mouth replay on restore','final_flags':{'P06':s.call('p06Projection',0),'VC':v.call('vcFlags')},'compile_receipt_sha256':hashlib.sha256((H/'build/coherent/compile-receipt.json').read_bytes()).hexdigest(),'native_acceptance':False,'listening':False}
OUT.write_text(json.dumps(report,indent=2)+'\n');print('PASS real emitted UI solution,',len(TRACE),'control/action steps,',len(READS),'source pages; muted/restore mouth gates')
