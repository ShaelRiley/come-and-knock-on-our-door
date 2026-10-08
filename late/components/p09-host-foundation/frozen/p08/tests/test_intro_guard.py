import unittest
import host
from host import frame
from test_rendezvous import fixture,finish

class IntroGuard(unittest.TestCase):
 def test_07_earned_pages_skip_receipt_resources_but_new_pages_validate(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);finish(h)
   self.assertEqual(s.call('h8IntroCheck',1),1);frame(h)
   count=h.vm.calls[(985,'hStaticRange')]
   for _ in range(20):self.assertEqual(s.call('h8IntroCheck',1),0)
   self.assertEqual(h.vm.calls[(985,'hStaticRange')],count)
   self.assertEqual(s.call('h8IntroCheck',0),1)
   graphs=sum(k=='Graph' and args[0]==12 for k,args in h.vm.ktrace)
   draws=sum(k=='DrawCel' for k,args in h.vm.ktrace)
   once=list(s.arrays['p08Words'][52:54])
   for _ in range(5):frame(h);self.assertEqual(s.arrays['h8IntroWords'][2],1)
   self.assertEqual(sum(k=='Graph' and args[0]==12 for k,args in h.vm.ktrace),graphs+5)
   self.assertGreater(sum(k=='DrawCel' for k,args in h.vm.ktrace),draws)
   self.assertEqual(list(s.arrays['p08Words'][52:54]),once)
   d=h.vm.objects['sceneDialogue'];self.assertEqual(d.p['sdPaintGeneration'],d.p['sdGeneration'])
   h.call('uiTurnPage',1);self.assertEqual(s.call('h8IntroCheck',1),1);frame(h)
   self.assertEqual(s.arrays['h8IntroWords'][2],3)
   self.assertEqual(s.call('h8IntroCheck',1),0)
   s.arrays['h8IntroContext'][4]=99
   self.assertEqual(s.call('h8IntroCheck',0),0)
