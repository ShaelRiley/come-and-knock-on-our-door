"""Actual deferred SCI kernel call under bounded exact-tag deterministic kernels."""
import copy,unittest
import host
from test_confirmation_boundaries import stage,talk
from test_layout_controls import menu_pick
from test_restore import load
from storage_kernel_profile import StorageBackend

def service(h):h.vm.pump([{},{}])

class StorageKernel(unittest.TestCase):
 def test_01_more_than_twenty_manuals_actual_save_and_inflight_restore_retry(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=stage(source,'menu');backend=StorageBackend(h.vm,occupied=range(1,26));original=copy.deepcopy(backend.raw)
   menu_pick(h,1);self.assertEqual(s.arrays['h8IO'][0],1);self.assertEqual(backend.auto_operations,[])
   request=list(s.arrays['p08Words'][16:18]);confirmation=list(s.arrays['p08Words'][22:24]);words=list(s.arrays['p08Words']);owners=list(s.arrays['h8OwnerReceipts'])
   service(h);self.assertEqual(backend.auto_operations,[('enumerate',20),('exists','*.026',0),('save',26,1)])
   self.assertEqual(backend.checks,list(range(101,127)));self.assertEqual((s.arrays['h8IO'][0],s.arrays['h8IO'][10],s.call('h8S',6)),(4,26,1))
   self.assertEqual(list(s.arrays['p08Words']),words);self.assertEqual(list(s.arrays['h8OwnerReceipts']),owners)
   self.assertEqual((r.p['hBunnyRoom'],t.p['h6FrankieRoom'],s.call('h8EveningCommitted'),s.call('h8EveningReady')),(4,4,0,0))
   self.assertTrue(all(backend.raw[n]==value for n,value in original.items()))
   for _ in range(10):service(h)
   self.assertEqual(len([r for r in backend.auto_operations if r[0]=='save']),1)
   saved=copy.deepcopy(backend.autosaved[26]);self.assertIsNotNone(saved)
   # The saved file is genuinely pre-ack: an in-flight request, no success receipt.
   live=h.vm.snapshot();h.vm.restore(copy.deepcopy(saved));self.assertEqual((s.arrays['p08Words'][11],s.arrays['h8IO'][0],s.arrays['h8IO'][11]),(3,2,0));h.vm.restore(copy.deepcopy(live))
   load(h,backend,saved);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.arrays['h8IO'][0],s.arrays['h8IO'][12]),(0,1,3,5))
   self.assertEqual(s.call('h8S',6),0);self.assertEqual(list(s.arrays['h8IO'][1:3]),[0,2])
   self.assertEqual(list(s.arrays['p08Words'][16:18]),request);self.assertEqual(list(s.arrays['p08Words'][22:24]),confirmation)
   for _ in range(5):service(h)
   self.assertEqual(len([r for r in backend.auto_operations if r[0]=='save']),1)
   talk(h);self.assertEqual([h.arrays['uiChoiceEnabled'][i] for i in range(2)],[1,1]);menu_pick(h,1)
   self.assertEqual(s.arrays['h8IO'][0],1);self.assertEqual(list(s.arrays['h8IO'][1:3]),[0,3]);service(h)
   self.assertEqual(backend.auto_operations[-3:],[('enumerate',20),('exists','*.027',0),('save',27,1)])
   self.assertEqual((s.call('h8S',6),s.arrays['p08Words'][11]),(1,3));self.assertEqual(list(s.arrays['p08Words'][16:18]),request)
   self.assertEqual(list(s.arrays['p08Words'][22:24]),confirmation);self.assertTrue(all(backend.raw[n]==value for n,value in original.items()))
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))

if __name__=='__main__':unittest.main(verbosity=2)
