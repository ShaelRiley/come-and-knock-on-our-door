"""Same accepted storage probes; terminal success now consumes the IO receipt into ACK."""
from test_storage_boundaries import *

class StorageAfterAck(unittest.TestCase):
 def test_03_false_result_explicit_retry_modes_and_inflight_reentry(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=stage(source,'pending');backend=StorageBackend(h.vm,occupied=[1,3],result=0);original=copy.deepcopy(backend.raw);words=list(s.arrays['p08Words']);opened=h.vm.snapshot()
   # Explicit transient negative fixtures; no preparation or receipt is synthesized.
   for field in ('dirty','type','opening','paused','menuOpen','uiPanel','motionPhase'):
    h.vm.restore(copy.deepcopy(opened));h.p['dirty']=0;h.p['type']=0;h.p[field]=1
    self.assertEqual(s.call('h8S',0),0,field);self.assertEqual(backend.auto_operations,[]);self.assertEqual(list(s.arrays['p08Words']),words)
   h.vm.restore(copy.deepcopy(opened));service(h)
   self.assertEqual((s.arrays['h8IO'][0],s.arrays['h8IO'][12],s.call('h8S',6)),(3,4,0))
   self.assertEqual(backend.auto_operations,[('enumerate',2),('exists','*.002',0),('save',2,0)]);self.assertEqual(backend.raw,original)
   for _ in range(8):service(h)
   self.assertEqual(len(backend.auto_operations),3);self.assertEqual(s.call('h8RAct',6),0)
   # A successful ordinary manual chooser cannot certify the failed automatic call.
   h.call('writeSave');self.assertIsNotNone(backend.saved);self.assertEqual(s.call('h8S',6),0);self.assertEqual(list(s.arrays['p08Words']),words)
   backend.auto_result=1;fired=[]
   def reentry(snapshot):
    fired.append(1);before=persistent(s);manual=len(backend.operations)
    self.assertEqual(s.call('h8S',8),1);self.assertEqual(s.call('h8S',6),0)
    for method,args in [('hostActNow',(0,18,0)),('uiHostChoice',(237,1)),('writeSave',()),('readSave',()),('p03PreparationHint',())]:h.call(method,*args)
    for op in (2,3,6):self.assertEqual(s.call('h8RAct',op),0)
    self.assertEqual(persistent(s),before);self.assertEqual(len(backend.operations),manual)
   backend.before_return=reentry;talk(h);menu_pick(h,1);service(h)
   self.assertEqual(fired,[1]);service(h);self.assertEqual(s.call('h8S',6),0);self.assertEqual(s.call('h8EveningCommitted'),1);self.assertEqual(backend.auto_operations[-3:],[('enumerate',2),('exists','*.002',0),('save',2,1)])
   self.assertTrue(all(backend.raw[n]==b for n,b in original.items()));self.assertEqual(s.arrays['p08Words'][11],0)
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(1,0))

 def test_04_abandoned_return_cannot_ack_restored_snapshot(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=stage(source,'pending');backend=StorageBackend(h.vm,occupied=[1]);fired=[]
   def abandoned(snapshot):
    fired.append(1);vm=h.vm;previous=vm.event_queue
    vm.restore(copy.deepcopy(snapshot));vm.event_queue=[{},{}]
    # Fault profile intentionally lets an abandoned call return after a genuine
    # whole-campaign replay. Native restore discards that old stack instead.
    try:h.call('replay')
    except host.base.EndOfEvents:pass
    finally:vm.event_queue=previous
   backend.before_return=abandoned;service(h)
   self.assertEqual(fired,[1]);self.assertIn(2,backend.autosaved)
   self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.arrays['h8IO'][0],s.arrays['h8IO'][12]),(0,1,3,5))
   self.assertEqual(s.call('h8S',6),0);self.assertEqual(list(s.arrays['h8IO'][1:3]),[0,2]);self.assertEqual(s.arrays['p08Words'][11],3)
   for _ in range(6):service(h)
   self.assertEqual(len([r for r in backend.auto_operations if r[0]=='save']),1)
   h.call('writeSave');self.assertIsNotNone(backend.saved);self.assertEqual(s.call('h8S',6),0)
   backend.before_return=None;talk(h);menu_pick(h,1);service(h)
   self.assertEqual(backend.auto_operations[-3:],[('enumerate',2),('exists','*.003',0),('save',3,1)]);service(h);self.assertEqual(s.call('h8S',6),0);self.assertEqual(s.call('h8EveningCommitted'),1)
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(1,0))

