"""Checklist ACK and explicit Yes; checkpoint intent is never storage success."""
import copy,unittest
import host
from host import frame,close,act
from test_rendezvous import fixture,finish
from test_layout_controls import place,overlay,menu_pick
from test_practical import input_action,arrive
from test_restore import Backend,load

def ready(source):
 h,p,q,r,t,u,v,s=fixture(source);finish(h);close(h,read=False)
 assert s.arrays['h8IntroWords'][2]==0
 place(h,120,1,8);place(h,34,1);act(h,2,34)
 place(h,63,2);overlay(h,63,5,1);place(h,81,3);place(h,40,1)
 assert s.arrays['p08Words'][8]==1 and s.p['p08Wins']==0
 assert list(s.arrays['p08Words'][32:40])==[0]*8
 return h,p,q,r,t,u,v,s

def request(h):
 s=h.vm.objects['p08State'];before=list(s.arrays['p08Words'])
 input_action(h,6,8);arrive(h)
 assert (h.p['uiPanel'],h.p['uiChoiceContext'])==(2,236)
 assert list(s.arrays['p08Words'])==before
 menu_pick(h,1);assert h.p['uiDocument']==1007
 h.call('uiClose');assert h.p['uiDocument']==1008

class ReadyConfirmation(unittest.TestCase):
 def test_01_exact_checklist_explicit_yes_pending_save_restore_and_cancel(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=ready(source);request(h)
   for page,mask in ((0,1),(1,3),(2,7)):
    if page:h.call('uiTurnPage',1)
    frame(h);self.assertEqual((s.arrays['h8R'][11],s.arrays['p08Words'][11]),(mask,1))
   self.assertEqual(list(s.arrays['p08Words'][20:24]),[0]*4)
   h.call('uiClose');self.assertEqual(h.p['uiDocument'],1009)
   frame(h);self.assertEqual((s.arrays['h8R'][11],s.arrays['p08Words'][11]),(15,1))
   h.call('uiTurnPage',1);self.assertEqual(s.arrays['p08Words'][11],1)
   frame(h);self.assertEqual((s.arrays['h8R'][11],s.arrays['p08Words'][11]),(31,2))
   self.assertNotEqual(list(s.arrays['p08Words'][20:22]),[0,0]);self.assertEqual(list(s.arrays['p08Words'][22:24]),[0,0])
   self.assertEqual(list(h.arrays['bridgeQueue'])[s.arrays['h8R'][13]:s.arrays['h8R'][13]+2],[1010,1011])
   close(h);self.assertEqual((h.p['uiPanel'],h.p['uiChoiceContext']),(2,237))
   labels=[host.base.read_string(h.arrays['uiChoiceLabels'][i]) for i in range(2)]
   self.assertEqual(labels,['BEGIN THE EVENING.','NOT YET.'])
   before=list(s.arrays['p08Words']);self.assertEqual(s.call('h8RAct',3),0);self.assertEqual(list(s.arrays['p08Words']),before)
   self.assertEqual(s.call('h8RCtl',13,1),0) # No native choice-dispatch latch.
   self.assertEqual(list(s.arrays['h8CP']),[0]*8)
   saves=sum(k=='SaveGame' for k,a in h.vm.ktrace)
   menu_pick(h,1)
   self.assertEqual(s.arrays['p08Words'][11],3);self.assertNotEqual(list(s.arrays['p08Words'][22:24]),[0,0])
   self.assertEqual(list(s.arrays['h8CP']),[1]+list(s.arrays['p08Words'][16:18])+list(s.arrays['p08Words'][22:24])+[0]*3)
   self.assertEqual(sum(k=='SaveGame' for k,a in h.vm.ktrace),saves)
   self.assertEqual((r.p['hBunnyRoom'],t.p['h6FrankieRoom'],s.arrays['p08Words'][9]),(4,4,0))
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))
   self.assertEqual(s.call('h8SaveReady'),1)
   backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved);pending=copy.deepcopy(backend.saved)
   self.assertEqual((s.arrays['p08Words'][11],s.arrays['h8CP'][0]),(3,1))
   load(h,backend,pending)
   self.assertEqual((s.p['h8RestoreValid'],s.p['h8Failure'],s.arrays['p08Words'][11],s.arrays['h8CP'][0]),(1,0,3,1))
   self.assertEqual(list(s.arrays['h8C']),[0]*10)
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))
   input_action(h,6,8);arrive(h);self.assertEqual(h.p['uiChoiceContext'],237)
   self.assertEqual([h.arrays['uiChoiceEnabled'][i] for i in range(2)],[0,1])
   menu_pick(h,2)
   self.assertEqual((s.arrays['p08Words'][11],s.arrays['p08Words'][8]),(0,1))
   self.assertEqual(list(s.arrays['h8CP']),[0]*8)
   self.assertEqual(list(s.arrays['p08Words'][32:40]),[0]*8)
   self.assertEqual(s.arrays['h8IntroWords'][2],0)
   self.assertEqual(s.call('h8SaveReady'),1)

if __name__=='__main__':unittest.main(verbosity=2)
