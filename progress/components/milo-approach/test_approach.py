#!/usr/bin/env python3
"""Focused genuine emitted motion/commit checks; source only for edited geometry.
No native engine, PCM or save-file claim. Explicit state fixtures isolate P02/P05.
"""
from pathlib import Path
import sys,json,hashlib,unittest
W=Path(__file__).resolve().parent;H=W/'fixture';sys.dont_write_bytecode=True
sys.path[:0]=[str(H/'tests'),str(H/'tools')]
import host
from domain_source_vm import VM as SourceInterpreter,parse
from source_tools import methods
from test_practical import input_action,enter_control
REPORT=[]
TARGET=None
class SourceGeometryVM(host.VM):
 def __init__(self):
  self.source=None;super().__init__()
  s=SourceInterpreter.__new__(SourceInterpreter);ast=parse((H/'src/module985.sc').read_text());cl=next(x for x in ast if x[:2]==['class','P05State'])
  s.p=self.objects['p05State'].p;s.arrays=self.arrays(985);s.constants={x[1]:x[2] for x in ast if x[0]=='define'};s.methods={x[1][0]:x for x in cl if isinstance(x,list) and x and x[0]=='method'};self.source=s
 def call(self,obj,name,args=()):
  if self.source and obj.name=='p05State' and name in ('hApproachX','hApproachY'):return self.source.call(name,*args)
  return super().call(obj,name,args)
def setup(engine=host.VM,start=(293,139),plan=False,bundle=True):
 old=host.VM
 try:host.VM=engine;h,d,a,p,q,r=host.setup(plan)
 finally:host.VM=old
 h.p.update(location=5,roomSeen=5,motionX=start[0]*64,motionY=start[1]*64,motionPhase=0,opening=0)
 if not plan:h.p.update(p02CopyJack=12 if bundle else 10,p02CopyBunny=12 if bundle else 1,p02CopyStringer=12 if bundle else 2,p02Compared=1 if bundle else 0,p02Observed=31 if bundle else 0)
 h.call('p02SyncInventory',0);h.call('p02HostInventory');host.frame(h)
 h.vm.budget=120000000
 return h,r

def record_arrival(h):
 events=[]
 def hook(obj,name,args,result):
  if name in ('hostActNow','p02ShowMilo','p02Commit','hTopics'):
   events.append(dict(method=name,args=list(args),position=[h.p['motionX'],h.p['motionY']],phase=h.p['motionPhase'],shown=h.p['p02MiloShown'],drawer=h.p['p02DrawerOpen']))
 h.vm.after_actual_call=hook
 return events

def finish(h):
 positions=[]
 for frame in range(120):
  if not h.p['motionPhase']:return positions
  positions.append((h.p['motionX'],h.p['motionY'],h.p['motionPhase']))
  h.vm.pump([{}])
 raise AssertionError('ordinary approach did not finish')

class ApproachTests(unittest.TestCase):
 def test_give_ordinary_ui_only_commits_at_exact_new_anchor(self):
  for engine in (host.VM,SourceGeometryVM):
   for start in [(293,139),(100,139),(101,138),TARGET]:
    with self.subTest(engine=engine.__name__,start=start):
     h,r=setup(engine,start);ev=record_arrival(h);input_action(h,1,23,28)
     if start!=TARGET:self.assertEqual((h.p['p02MiloShown'],h.p['p02DrawerOpen']),(0,0));self.assertGreater(h.p['motionPhase'],0)
     path=finish(h)
     self.assertEqual((h.p['motionX']//64,h.p['motionY']//64),TARGET)
     self.assertEqual((h.p['p02MiloShown'],h.p['p02DrawerOpen'],h.p['p02MasterHeld']),(1,1,0))
     self.assertEqual(h.p['motionLoop'],0)
     relevant=[e for e in ev if e['method'] in ('hostActNow','p02ShowMilo')];self.assertTrue(relevant)
     self.assertTrue(all(e['position']==[TARGET[0]*64,TARGET[1]*64] and e['phase']==0 for e in relevant))
     self.assertEqual(sum(e['method']=='p02Commit' and e['args'][0]==401 for e in ev),1)
     self.assertEqual((h.p['uiPanel'],h.p['uiPageCount']),(4,4))
     self.assertTrue(all(y>=132*64 for _,y,_ in path))
     REPORT.append(dict(case='ordinary GIVE',engine=engine.__name__,start=start,target=TARGET,path=path,events=ev))
 def test_talk_and_related_single_noun_verbs_use_same_anchor(self):
  for engine in (host.VM,SourceGeometryVM):
   for verb in (0,2,3,4,5,6,7,8,9):
    with self.subTest(engine=engine.__name__,verb=verb):
     h,r=setup(engine,(100,139));ev=record_arrival(h)
     # uiHostAct is the ordinary sentence dispatch after noun composition.
     
     if verb==6:input_action(h,verb,28)
     else:h.call('uiHostAct',verb,28,0)
     self.assertGreater(h.p['motionPhase'],0)
     self.assertEqual(h.p['p02MiloShown'],0);path=finish(h)
     self.assertEqual((h.p['motionX']//64,h.p['motionY']//64),TARGET)
     self.assertEqual(any(e['method']=='hostActNow' for e in ev),verb!=0)
     self.assertTrue(all(e['position']==[TARGET[0]*64,TARGET[1]*64] for e in ev if e['method']=='hostActNow'))
     self.assertEqual((h.p['p02MiloShown'],h.p['p02DrawerOpen']),(0,0))
     REPORT.append(dict(case='related verb',engine=engine.__name__,verb=verb,path=path,events=ev))
 def test_escape_cancels_pending_give_without_commit(self):
  h,r=setup();ev=record_arrival(h);input_action(h,1,23,28)
  h.vm.pump([{'type':4,'message':27}]);finish(h)
  self.assertEqual((h.p['motionPhase'],h.p['p02MiloShown'],h.p['p02DrawerOpen']),(0,0,0));self.assertFalse(any(e['method']=='p02Commit' for e in ev))
 def test_room_apron_context_guard_prevents_stale_arrival(self):
  for prop,val in [('location',1),('onApron',1)]:
   h,r=setup();ev=record_arrival(h);h.call('uiHostAct',1,23,28);h.p[prop]=val
   for _ in range(120):
    if not h.p['motionPhase']:break
    h.call('motionAdvance',6)
   self.assertEqual((h.p['p02MiloShown'],h.p['p02DrawerOpen']),(0,0));self.assertFalse(any(e['method']=='p02Commit' for e in ev))
 def test_missing_bundle_not_granted_and_repeated_give_not_recommitted(self):
  h,r=setup(bundle=False);ev=record_arrival(h);h.call('uiHostAct',1,23,28);finish(h)
  self.assertEqual((h.p['p02MiloShown'],h.p['p02DrawerOpen']),(0,0))
  h,r=setup();ev=record_arrival(h);input_action(h,1,23,28);finish(h);host.close(h)
  input_action(h,1,23,28);finish(h)
  self.assertEqual(sum(e['method']=='p02Commit' and e['args'][0]==401 for e in ev),1)
 def test_other_targets_controls_and_later_bunny_retained(self):
  before=methods((W/'baseline-module985.sc').read_text());after=methods((H/'src/module985.sc').read_text())
  self.assertEqual(set(before),set(after));self.assertEqual([n for n in before if before[n]!=after[n]],['hApproachX'])
  for plan in (False,True):
   h,r=setup(plan=plan)
   if plan:
    # Actual consent/escort through authoritative P05 action in living room.
    h.p.update(location=1,roomSeen=1);host.act(h,6,2);host.choice(h,209,1);self.assertEqual((h.p['location'],r.p['hBunnyRoom']),(5,5))
   for obj,xy in {2:(268,139),17:(29,135),9:(303,138),27:(74,139),24:(74,139),72:(78,139),63:(169,139),65:(121,139),71:(108,139)}.items():
    self.assertEqual((h.call('approachX',obj),h.call('approachY',obj)),xy)
   h.p.update(motionX=TARGET[0]*64,motionY=TARGET[1]*64,motionPhase=0);h.call('uiBuildFocus')
   controls={h.arrays['uiPayloads'][i] for i in range(h.p['uiControlCount']) if h.arrays['uiActions'][i]==1}
   self.assertTrue({17,28,27,9}.issubset(controls))
   if plan:
    self.assertTrue({2,63,64,65,66,67,68,69,70,71,72}.issubset(controls))
    for xy,obj in [((60,110),72),((20,100),17),((308,100),9),((100,100),28),((268,90),2)]:
     hit=h.call('uiHit',*xy);self.assertGreaterEqual(hit,0);self.assertEqual(h.arrays['uiPayloads'][hit],obj)
   h.vm.ktrace=[];h.call('drawWorld');draws=[a for n,a in h.vm.ktrace if n=='DrawCel']
   self.assertEqual(sum(a[0]==221 for a in draws),1);self.assertEqual(sum(a[0] in (214,216) for a in draws),1)
   self.assertEqual(sum(a[0]==219 for a in draws),int(plan))
   REPORT.append(dict(case='retained garage',plan=plan,draws=draws,controls=sorted(controls)))
if __name__=='__main__':
 delta=json.loads((W/'APPROACH-DELTA.json').read_text());TARGET=tuple(delta['target_feet'])
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(ApproachTests);result=unittest.TextTestRunner(verbosity=2).run(suite)
 report=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,errors=len(result.errors),failures=len(result.failures),subcase_traces=REPORT,native_acceptance=False,limits='Typed emitted kernel VM; source interpreter only for hApproachX/hApproachY while unchanged movement/actions remain emitted.')
 (W/'evidence/approach-test-results.json').write_text(json.dumps(report,indent=2)+'\n')
 raise SystemExit(not result.wasSuccessful())
