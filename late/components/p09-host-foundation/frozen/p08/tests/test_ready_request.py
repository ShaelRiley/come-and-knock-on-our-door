"""First readiness gate: real choice, five exact pages, pending save and cancellation."""
import copy,unittest
import host
from host import frame,close,act
from test_rendezvous import fixture,finish
from test_layout_controls import place,overlay,menu_pick
from test_practical import input_action,arrive
from test_restore import Backend,load

class ReadyRequest(unittest.TestCase):
 def test_01_actual_choice_pages_pending_restore_and_layout_cancel(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);finish(h);close(h,read=False)
   self.assertEqual(s.arrays['h8IntroWords'][2],0)
   for obj in (13,14,15):self.assertEqual(s.call('h8ReaderAction',obj),1);close(h)
   place(h,120,1,8);place(h,34,1);act(h,2,34)
   place(h,63,2);overlay(h,63,5,1);place(h,81,3);place(h,40,1)
   self.assertEqual(s.call('h8ReaderAction',5),1);close(h)
   self.assertEqual((s.arrays['p08Words'][8],s.p['p08Wins']),(1,0))
   known=list(s.arrays['p08Words'][32:40]);self.assertTrue(all(known[i] or known[i+1] for i in range(0,8,2)))
   before=list(s.arrays['p08Words']);input_action(h,6,8);arrive(h)
   self.assertEqual((h.p['uiPanel'],h.p['uiChoiceContext']),(2,236))
   self.assertEqual(host.base.read_string(h.arrays['uiChoiceLabels'][0]),"WE'RE READY TO START.")
   self.assertEqual(list(s.arrays['p08Words']),before)
   self.assertEqual(s.arrays['h8IntroWords'][2],0)
   menu_pick(h,1)
   self.assertEqual((h.p['uiDocument'],s.arrays['p08Words'][11],s.arrays['h8R'][11]),(1007,1,0))
   self.assertEqual(list(s.arrays['p08Words'][32:40]),known)
   self.assertEqual(s.call('h8RChk',0),1)
   frame(h);self.assertEqual(s.arrays['h8R'][11],0)
   h.call('uiClose');self.assertEqual(h.p['uiDocument'],1008)
   h.call('dialoguePresented');self.assertEqual(s.arrays['h8R'][11],0)
   frame(h);self.assertEqual(s.arrays['h8R'][11],1)
   self.assertEqual(s.call('h8SaveReady'),1)
   backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved);partial=copy.deepcopy(backend.saved)
   for page,mask in ((1,3),(2,7)):
    h.call('uiTurnPage',1);self.assertNotEqual(s.arrays['h8R'][11],mask);frame(h);self.assertEqual(s.arrays['h8R'][11],mask)
   h.call('uiClose');self.assertEqual(h.p['uiDocument'],1009)
   frame(h);self.assertEqual(s.arrays['h8R'][11],15)
   self.assertEqual(list(s.arrays['p08Words'][20:24]),[0]*4)
   h.call('uiTurnPage',1);frame(h);self.assertEqual(s.arrays['h8R'][11],31)
   # This finite gate earns display evidence only. No checklist ACK or final Yes yet.
   self.assertEqual(s.arrays['p08Words'][11],1);self.assertEqual(list(s.arrays['p08Words'][20:24]),[0]*4)
   load(h,backend,partial)
   self.assertEqual((s.p['h8RestoreValid'],s.p['h8Failure'],s.arrays['h8R'][11]),(1,0,1))
   self.assertEqual((h.p['uiDocument'],h.p['uiPage']),(1008,0))
   close(h,read=False);self.assertEqual((s.arrays['h8R'][0],s.arrays['h8R'][12]),(1,0))
   place(h,63,4)
   self.assertEqual((s.arrays['p08Words'][11],s.arrays['h8R'][0],s.arrays['h8R'][11]),(0,0,0))
   self.assertEqual(list(s.arrays['p08Words'][32:40]),known)
   self.assertEqual(s.arrays['h8IntroWords'][2],0)
   self.assertEqual(s.call('h8SaveReady'),1)
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))

if __name__=='__main__':unittest.main(verbosity=2)
