"""Six-page voiced intro: genuine assembly, actual frames, durable continuation."""
import copy,unittest
import host
from host import frame,close
from test_rendezvous import fixture,finish
from test_restore import Backend,load
from test_practical import input_action,arrive

class Intro(unittest.TestCase):
 def test_01_actual_meeting_partial_close_talk_resume_and_restore(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source)
   self.assertEqual(list(s.arrays['p08Words'][52:54]),[0,0])
   finish(h);d=h.vm.objects['sceneDialogue']
   self.assertEqual((h.p['uiDocument'],h.p['uiPanel'],h.p['uiPageCount']),(973,4,6))
   self.assertEqual((s.call('h8IntroCheck',0),s.call('h8IntroCheck',1)),(1,1))
   once=list(s.arrays['p08Words'][52:54]);self.assertNotEqual(once,[0,0])
   self.assertEqual(list(s.arrays['h8IntroWords'][:3]),once+[0])
   self.assertEqual(list(s.arrays['p08Words'][32:40]),[0]*8)
   h.call('dialoguePresented');self.assertEqual(s.arrays['h8IntroWords'][2],0)
   frame(h);self.assertEqual(s.arrays['h8IntroWords'][2],1)
   h.call('uiTurnPage',1);frame(h);self.assertEqual(s.arrays['h8IntroWords'][2],3)
   self.assertEqual(s.call('h8SaveReady'),1)
   backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved);partial=copy.deepcopy(backend.saved)
   close(h,read=False)
   self.assertEqual((s.arrays['h8IntroWords'][2],s.arrays['h8IntroWords'][4]),(3,0))
   for _ in range(3):frame(h)
   self.assertNotEqual(h.p['uiDocument'],973) if h.p['uiPanel'] else None
   input_action(h,6,8);arrive(h)
   self.assertEqual((h.p['uiDocument'],h.p['uiPage']),(973,2))
   self.assertEqual(list(s.arrays['p08Words'][52:54]),once)
   close(h);self.assertEqual(s.arrays['h8IntroWords'][2],63)
   self.assertEqual(list(s.arrays['p08Words'][32:40]),[0]*8)
   self.assertEqual(s.call('h8SaveReady'),1)
   load(h,backend,partial)
   self.assertEqual((s.p['h8RestoreValid'],s.p['h8Failure']),(1,0))
   self.assertEqual((s.arrays['h8IntroWords'][2],h.p['uiPage']),(3,1))
   self.assertEqual(list(s.arrays['p08Words'][52:54]),once)
   close(h);self.assertEqual(s.arrays['h8IntroWords'][2],63)
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))

if __name__=='__main__':unittest.main(verbosity=2)
