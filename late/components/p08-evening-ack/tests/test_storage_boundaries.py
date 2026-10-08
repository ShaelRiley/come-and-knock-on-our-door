"""Exact-tag file fixtures plus actual SCI request/dispatch; no native I/O claim."""
import copy,unittest
import host
from host import close
from test_confirmation_boundaries import stage,talk,persistent
from test_layout_controls import menu_pick
from test_storage_kernel import service
from test_restore import load
from storage_kernel_profile import StorageBackend

class StorageBoundaries(unittest.TestCase):
 def test_02_sparse_full_ambiguous_and_unsupported_first_candidate(self):
  for source in (False,True):
   fixtures=[('sparse',[1,3,20,90],[],[],4,2),('full',list(range(1,100)),[],[],3,0),
    ('other_target',[1,3,20,90],['unrelated-target.002'],[],3,2),('unsupported',[1,2,3],[],[2],3,2)]
   for name,occupied,raw,unsupported,state,slot in fixtures:
    h,p,q,r,t,u,v,s=stage(source,'pending');backend=StorageBackend(h.vm,occupied,raw,unsupported);original=copy.deepcopy(backend.raw);words=list(s.arrays['p08Words'])
    service(h);self.assertEqual((s.arrays['h8IO'][0],s.arrays['h8IO'][10]),(state,slot),name)
    self.assertEqual(list(s.arrays['p08Words']),words,name);self.assertTrue(all(backend.raw[n]==b for n,b in original.items()),name)
    if name=='sparse':self.assertEqual(backend.auto_operations,[('enumerate',4),('exists','*.002',0),('save',2,1)])
    elif name=='full':
     self.assertEqual(backend.checks,list(range(101,200)));self.assertEqual(backend.auto_operations,[('enumerate',20)]);self.assertEqual(s.arrays['h8IO'][12],3)
    else:
     self.assertEqual(backend.checks,[101,102]);self.assertEqual(backend.auto_operations[-1],('exists','*.002',1));self.assertEqual(s.arrays['h8IO'][12],2)
    count=len(backend.auto_operations)
    for _ in range(5):service(h)
    self.assertEqual(len(backend.auto_operations),count);self.assertEqual(s.call('h8S',6),int(name=='sparse'))
    talk(h);menu_pick(h,2);self.assertEqual(s.arrays['p08Words'][11],0);self.assertEqual(s.arrays['h8IO'][0],0)

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
   self.assertEqual(fired,[1]);self.assertEqual(s.call('h8S',6),1);self.assertEqual(backend.auto_operations[-3:],[('enumerate',2),('exists','*.002',0),('save',2,1)])
   self.assertTrue(all(backend.raw[n]==b for n,b in original.items()));self.assertEqual(s.arrays['p08Words'][11],3)
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))

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
   self.assertEqual(backend.auto_operations[-3:],[('enumerate',2),('exists','*.003',0),('save',3,1)]);self.assertEqual(s.call('h8S',6),1)
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))

 def test_05_raw_inflight_corruption_and_staged_false_success_rejected(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=stage(source,'pending');backend=StorageBackend(h.vm);service(h);saved=copy.deepcopy(backend.autosaved[1]);live=h.vm.snapshot()
   mutations=[('zero_slot',lambda:s.arrays['h8IO'].__setitem__(10,0)),('result',lambda:s.arrays['h8IO'].__setitem__(11,1)),
    ('request',lambda:s.arrays['h8IO'].__setitem__(4,99)),('staged',lambda:s.arrays['h8IP'].__setitem__(29,1))]
   for name,mutate in mutations:
    h.vm.restore(copy.deepcopy(saved));mutate();bad=h.vm.snapshot();h.vm.restore(copy.deepcopy(live));calls=h.vm.calls.copy();load(h,backend,bad)
    self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid']),(21,0),name)
    self.assertEqual((s.call('h8S',8),s.call('h8S',6)),(0,0),name)
    for key in ((983,'bInventory'),(984,'qInventory')):self.assertEqual(h.vm.calls[key],calls[key],name)
    load(h,backend,saved);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.call('h8S',6)),(0,1,0))
   # Saved post-write host receipt is also retired on ordinary restore.
   h.vm.restore(copy.deepcopy(live));h.call('writeSave');receipt=copy.deepcopy(backend.saved);load(h,backend,receipt)
   self.assertEqual((s.arrays['h8IO'][0],s.call('h8S',6)),(3,0))
   h.vm.restore(copy.deepcopy(receipt));h.arrays['uiItems'][63]=25;bad=h.vm.snapshot();h.vm.restore(copy.deepcopy(live));load(h,backend,bad)
   self.assertEqual((s.p['h8Failure'],s.call('h8S',6),s.call('h8S',8)),(21,0,0));load(h,backend,receipt)
   self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.call('h8S',6)),(0,1,0))
   h,p,q,r,t,u,v,s=stage(source,'menu');backend=StorageBackend(h.vm);h.call('writeSave');good=copy.deepcopy(backend.saved);fired=[]
   def corrupt(obj,name,args,result):
    if obj.name=='p08State' and name=='h8S' and list(args)==[1] and result and not fired:
     fired.append(1);s.arrays['h8IP'][0]=4;s.arrays['h8IP'][10]=1;s.arrays['h8IP'][11]=1
   h.vm.after_actual_call=corrupt;menu_pick(h,1);h.vm.after_actual_call=None
   self.assertEqual(fired,[1]);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid']),(20,0));self.assertEqual(s.call('h8S',6),0);self.assertEqual(backend.auto_operations,[])
   load(h,backend,good);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.arrays['p08Words'][11]),(0,1,2))
   # Explicit serial-capacity fixture: rejects before committing the real Yes.
   s.arrays['h8IO'][1]=-1;s.arrays['h8IO'][2]=-2;talk(h);before=persistent(s);menu_pick(h,1)
   self.assertEqual(persistent(s),before);self.assertEqual(backend.auto_operations,[]);self.assertEqual(s.arrays['h8IP'][29],0)

if __name__=='__main__':unittest.main(verbosity=2)
