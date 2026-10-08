"""Typed deferred attempt ownership, ordinary restore and cancellation; no I/O."""
import copy,unittest
import host
from test_confirmation_boundaries import stage,talk
from test_layout_controls import menu_pick
from test_restore import Backend,load

class StorageScaffold(unittest.TestCase):
 def test_01_actual_yes_stages_one_attempt_and_restore_retires_it(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=stage(source,'pending');before=list(s.arrays['p08Words']);cp=list(s.arrays['h8CP']);attempt=list(s.arrays['h8IO'])
   self.assertEqual(attempt[:3],[1,0,1]);self.assertEqual(s.call('h8S',3),1);self.assertEqual(s.arrays['h8IP'][29],0)
   self.assertEqual(attempt[3:7],list(s.arrays['h8R'][3:5])+list(s.arrays['h8R'][20:22]));self.assertEqual(attempt[13:],list(s.arrays['h8RC']))
   for _ in range(20):self.assertEqual(s.call('h8S',0),0)
   self.assertEqual(list(s.arrays['h8IO']),attempt);self.assertEqual(s.call('h8S',6),0);self.assertEqual(h.vm.kernel_attempts['SaveGame'],0)
   self.assertEqual((len(s.arrays['h8Names']),len(s.arrays['h8Slots']),len(s.arrays['h8Pattern'])),(361,20,4))
   backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved);saved=copy.deepcopy(backend.saved);live=h.vm.snapshot();load(h,backend,saved)
   self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.arrays['p08Words'][11]),(0,1,3))
   self.assertEqual(list(s.arrays['p08Words']),before);self.assertEqual(list(s.arrays['h8CP']),cp)
   self.assertEqual(list(s.arrays['h8IO'][:3]),[3,0,2]);self.assertEqual(s.arrays['h8IO'][12],5);self.assertEqual(s.arrays['h8IO'][11],0)
   self.assertEqual(list(s.arrays['h8IO'][13:]),list(s.arrays['h8RC']));self.assertNotEqual(s.arrays['h8IO'][8],attempt[8])
   self.assertEqual(s.call('h8S',6),0);self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))
   for index in (3,6,14,22):
    h.vm.restore(copy.deepcopy(saved));s.arrays['h8IO'][index]+=1;bad=h.vm.snapshot();h.vm.restore(copy.deepcopy(live));calls=h.vm.calls.copy();load(h,backend,bad)
    self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid']),(21,0),index)
    for key in ((983,'bInventory'),(984,'qInventory')):self.assertEqual(h.vm.calls[key],calls[key],index)
    load(h,backend,saved)
   talk(h);menu_pick(h,2);self.assertEqual(s.arrays['p08Words'][11],0)
   self.assertEqual(list(s.arrays['h8IO']),[0,0,2]+[0]*26);self.assertEqual(s.call('h8SaveReady'),1)

if __name__=='__main__':unittest.main(verbosity=2)
