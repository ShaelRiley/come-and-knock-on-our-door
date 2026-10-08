"""Next finite intro gate: publication, corrupted restore, and real route return."""
import copy,unittest
import host
from host import act,frame,close
from test_rendezvous import fixture,finish
from test_restore import Backend,load

class IntroTransactions(unittest.TestCase):
 def test_04_atomic_queue_failure_uncertainty_and_recovery(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);d=h.vm.objects['sceneDialogue']
   # Deliberate capacity fixture through the actual old publisher; it is not
   # represented as an ordinary story history containing32 repeated records.
   h.call('bridgeBegin')
   for _ in range(16):h.call('h7PublishNative',2,385,386)
   queue=list(h.arrays['bridgeQueue']);kinds=list(d.arrays['sdQueueKinds']);domain=list(s.arrays['p08Words'])
   finish(h)
   self.assertEqual((s.call('h8RouteMode'),r.p['hBunnyRoom'],t.p['h6FrankieRoom']),(2,4,4))
   self.assertEqual(list(s.arrays['p08Words']),domain)
   self.assertEqual(list(h.arrays['bridgeQueue']),queue);self.assertEqual(list(d.arrays['sdQueueKinds']),kinds)
   self.assertEqual(list(s.arrays['h8IntroWords']),[0]*8)
   h.call('bridgeBegin');backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved)
   good=copy.deepcopy(backend.saved);live=h.vm.snapshot()
   for boundary in ('h8CommitReserved','h8UIPublish'):
    h.vm.restore(copy.deepcopy(live));fired=[]
    def fault(obj,name,args,result):
     if obj.name=='p08State' and name==boundary and result and not fired:
      fired.append(name);h.arrays['bridgeQueue'][0]=974
      if boundary=='h8CommitReserved':h.p['bridgeQueueCount']=1
    h.vm.after_actual_call=fault;self.assertEqual(s.call('h8IntroAction'),0,boundary);h.vm.after_actual_call=None
    self.assertEqual(fired,[boundary]);self.assertEqual(s.p['h8Failure'],20)
    self.assertEqual(s.arrays['h8IntroWords'][2],0);self.assertEqual(s.call('h8ActionBarrier'),1)
    self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))
    load(h,backend,good);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid']),(0,1))
    self.assertEqual(list(s.arrays['p08Words'][52:54]),[0,0])

 def test_05_corrupt_intro_restore_rejects_before_publishers(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);finish(h);frame(h);backend=Backend(h.vm);h.call('writeSave')
   good=copy.deepcopy(backend.saved);live=h.vm.snapshot()
   mutations=[('mask',lambda:s.arrays['h8IntroWords'].__setitem__(2,64)),
    ('reserved',lambda:s.arrays['h8IntroWords'].__setitem__(7,1)),('once',lambda:s.arrays['h8IntroWords'].__setitem__(1,99)),
    ('phase',lambda:s.arrays['h8IntroWords'].__setitem__(4,3)),('session',lambda:s.arrays['h8IntroContext'].__setitem__(4,99)),
    ('actor',lambda:s.arrays['h8IntroContext'].__setitem__(13,1)),('queue',lambda:h.arrays['bridgeQueue'].__setitem__(s.arrays['h8IntroWords'][5],974))]
   for name,mutate in mutations:
    h.vm.restore(copy.deepcopy(good));mutate();bad=h.vm.snapshot();h.vm.restore(copy.deepcopy(live));calls=h.vm.calls.copy()
    load(h,backend,bad)
    self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid']),(21,0),name)
    for key in ((983,'bInventory'),(984,'qInventory')):self.assertEqual(h.vm.calls[key],calls[key],name)
    load(h,backend,good);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.arrays['h8IntroWords'][2]),(0,1,1),name)

 def test_06_real_return_source_crossing_and_reassembly_resume(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);finish(h)
   h.call('uiTurnPage',2);frame(h);self.assertEqual(s.arrays['h8IntroWords'][2],4)
   once=list(s.arrays['p08Words'][52:54]);epoch=s.arrays['h8IntroWords'][3];close(h,read=False)
   self.assertEqual(s.call('h8ReaderAction',13),1);close(h)
   self.assertNotEqual(list(s.arrays['p08Words'][32:34]),[0,0]);self.assertEqual(s.arrays['h8IntroWords'][2],4)
   act(h,0,18);finish(h);self.assertEqual(s.call('h8RouteMode'),0)
   self.assertEqual((r.p['hBunnyRoom'],t.p['h6FrankieRoom']),(1,1))
   backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved);saved=copy.deepcopy(backend.saved)
   load(h,backend,saved);self.assertEqual((s.p['h8RestoreValid'],s.arrays['h8IntroWords'][2]),(1,4))
   act(h,0,13);finish(h)
   self.assertGreater(s.arrays['h8IntroWords'][3],epoch)
   self.assertEqual((h.p['uiDocument'],h.p['uiPage'],s.arrays['h8IntroWords'][2]),(973,0,4))
   self.assertEqual(list(s.arrays['p08Words'][52:54]),once)
   close(h);self.assertEqual(s.arrays['h8IntroWords'][2],63)
   act(h,0,18);finish(h);act(h,0,13);finish(h)
   self.assertEqual(s.arrays['h8IntroWords'][4],0)
   self.assertEqual(list(s.arrays['p08Words'][52:54]),once)

if __name__=='__main__':unittest.main(verbosity=2)
