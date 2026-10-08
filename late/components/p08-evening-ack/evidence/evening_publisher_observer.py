"""Observe actual source/emitted publisher calls across raw ACK admission."""
import copy,unittest
from test_evening_boundaries import pending
from test_storage_kernel import service
from test_restore import load

class PublisherObserver(unittest.TestCase):
 def test_08_rejected_raw_state_precedes_actual_publishers_on_both_backends(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s,b=pending(source)
   for _ in range(4):service(h)
   h.call('writeSave');good=copy.deepcopy(b.saved);self.assertIsNotNone(good);live=h.vm.snapshot();seen=[]
   def observe(obj,name,args,result):
    if name in ('bInventory','qInventory'):seen.append((obj.name,name))
   h.vm.after_actual_call=observe
   for name,mutate in [('phase',lambda:s.arrays['h8EW'].__setitem__(0,2)),('invented_page',lambda:s.arrays['h8EW'].__setitem__(47,1)),('staged',lambda:s.arrays['h8EP'].__setitem__(0,1))]:
    h.vm.restore(copy.deepcopy(good));mutate();bad=h.vm.snapshot();h.vm.restore(copy.deepcopy(live));seen.clear()
    load(h,b,bad);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid']),(21,0),name);self.assertEqual(seen,[],(source,name))
    load(h,b,good);self.assertEqual(s.p['h8RestoreValid'],1,name)
    self.assertIn(('p03State','bInventory'),seen);self.assertIn(('p04State','qInventory'),seen)
   self.assertEqual(len(b.autosaved),1)
