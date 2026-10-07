import unittest,json,copy
from host import *
from test_practical import input_action,arrive,restore,enter_control
from test_contest import taught,start,reply,win,consume_current
VMS=[]
class PresentationControls(unittest.TestCase):
 def test_genuine_exchange_wince_stage_single_owner_and_retirement(self):
  h,d,a,p,q,r,v=taught();VMS.append(h.vm);start(h,v)
  world={k:h.p[k] for k in ('motionX','motionY','motionLoop','motionPhase')}
  correct=v.call('vcRead',106+v.call('vcRead',95));h.call('uiHostChoice',217,correct);h.call('uiHostChoice',218,1)
  self.assertEqual((v.call('vcRead',96),v.call('vcRead',97),r.p['hVCHitActor']),(3,2,2))
  h.vm.ktrace=[];h.call('drawWorld');actors=[x for n,x in h.vm.ktrace if n=='DrawCel' and x[0] in (214,219,221,330)]
  self.assertEqual([(x[0],x[1],x[2]) for x in actors],[(330,0,1),(214,1,0)])
  self.assertEqual({k:h.p[k] for k in world},world)
  h.p['dirty']=0;r.call('hStageTick',6);r.call('hStageTick',6);r.call('hStageTick',6)
  self.assertEqual(r.call('hStagePose',2),0);self.assertEqual(h.p['dirty'],1)
  r.p['hVCReducedMotion']=1;r.p['hStageHitAge']=0;r.call('hStageTick',6);r.call('hStageTick',6);r.call('hStageTick',6)
  self.assertEqual(r.call('hStagePose',2),1)
  before=list(v.arrays['vcWords']);h.call('uiHostMenu');self.assertEqual((r.p['hVCHitActor'],r.p['hVCWinceActor']),(0,0));self.assertEqual(list(v.arrays['vcWords']),before)
  self.assertEqual({k:h.p[k] for k in world},world)
 def test_required_ko_record_precedes_result_and_restore_is_silent(self):
  for lose in [False,True]:
   h,d,a,p,q,r,v=taught();VMS.append(h.vm);h.vm.budget=40000000;start(h,v)
   for _ in range(2):reply(h,25 if lose else v.call('vcRead',106+v.call('vcRead',95)))
   h.call('uiHostChoice',217,25 if lose else v.call('vcRead',106+v.call('vcRead',95)));h.call('uiHostChoice',218,1)
   while v.call('vcRead',92)!=7:consume_current(h)
   self.assertEqual((r.p['hVCExtra'],r.p['hVCRecord'],r.p['hVCUnit'],r.p['hVCWinceActor']),(1,46 if lose else 45,10 if lose else 9,1 if lose else 2))
   self.assertEqual(v.call('vcRead',130),0);self.assertEqual(r.p['hContestBlocked'],1)
   h.vm.ktrace=[];frame(h);frame(h)
   plays=[x for n,x in h.vm.ktrace if n=='DoAudio' and x[0]==2]
   self.assertEqual(len(plays),1);self.assertEqual(plays[0][1],915)
   words=list(v.arrays['vcWords']);saved=h.vm.snapshot();played=a.p['played']
   restore(h,saved,[{'type':4,'message':13},{}]);frame(h)
   self.assertEqual(a.p['played'],played);self.assertEqual(list(v.arrays['vcWords']),words)
   self.assertEqual((r.p['hVCHitActor'],r.p['hVCWinceActor']),(0,0))
   self.assertEqual(r.p['hVCExtra'],1);h.call('uiClose');self.assertEqual(r.p['hVCExtra'],0)
   self.assertEqual((v.call('vcRead',92),v.call('vcRead',130)),(7,0));close(h)
   self.assertEqual(r.p['hContestBlocked'],0);self.assertEqual(r.call('hStageActive'),0);frame(h)
 def test_courtyard_hardware_keyboard_sources_and_wiring_remain_reachable(self):
  h,d,a,p,q,r,v=taught();VMS.append(h.vm);h.vm.budget=40000000;win(h,v);act(h,6,28);choice(h,211,5)
  act(h,0,17);act(h,2,1);act(h,0,1);act(h,0,13)
  self.assertEqual(h.p['location'],4);frame(h);h.call('uiBuildFocus')
  controls=[(h.arrays['uiActions'][i],h.arrays['uiPayloads'][i]) for i in range(h.p['uiControlCount'])]
  for obj in [18,19,9,63,64,65,66,67,68,70,71]:self.assertIn((1,obj),controls)
  self.assertNotIn((1,72),controls);self.assertNotIn((1,69),controls)
  for obj in [64,65,66,67,68,70]:self.assertEqual((h.call('approachX',obj),h.call('approachY',obj)),(114,140))
  before=(r.p['hPAOwner'],r.p['hPARoom'],r.p['hCartOwner'],r.p['hCartRoom'])
  for connected in [0,1]:
   input_action(h,9,66) if not connected else input_action(h,7,65,66)
   arrive(h);close(h);self.assertEqual(r.arrays['p05Words'][66],connected)
   for source in [0,1]:
    input_action(h,7,64);arrive(h);h.call('uiHostChoice',212,source);close(h)
    self.assertEqual(r.arrays['p05Words'][67],source);frame(h)
  for obj,source in [(64,1),(66,2),(71,3)]:
   input_action(h,5,obj);arrive(h);frame(h);close(h);self.assertGreater(r.call('p05Journal',source),0)
  self.assertEqual((r.p['hPAOwner'],r.p['hPARoom'],r.p['hCartOwner'],r.p['hCartRoom']),before)
  self.assertEqual(r.call('p05Flags'),7);self.assertEqual(h.call('campaignHeld',25),1)
  saved=h.vm.snapshot();restore(h,saved,[{},{}]);frame(h);self.assertEqual(r.p['hRestoreValid'],1)
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PresentationControls));(H/'evidence/presentation-controls-tests.json').write_text(json.dumps({'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':[(str(t),s) for t,s in result.failures],'errors':[(str(t),s) for t,s in result.errors],'instructions':sum(v.steps for v in VMS),'native_acceptance':False},indent=2)+'\n');raise SystemExit(not result.wasSuccessful())
