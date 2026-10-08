"""Finite ACK transaction and restore faults; no native filesystem claim."""
import copy,unittest
import host
from test_confirmation_boundaries import stage,talk
from test_layout_controls import menu_pick
from test_storage_kernel import service
from test_restore import load,RestoreTransfer,replay
from storage_kernel_profile import StorageBackend

def pending(source,result=1):
 h,p,q,r,t,u,v,s=stage(source,'menu');b=StorageBackend(h.vm,result=result);menu_pick(h,1)
 return h,p,q,r,t,u,v,s,b

def until_io(h,s):
 for _ in range(8):
  if s.arrays['h8IO'][0] in (3,4):return
  h.vm.pump([{}])
 raise AssertionError('No completed I/O attempt')

def logical(h,s):
 return (list(s.arrays['p08Words']),list(s.arrays['h8OwnerReceipts']),list(s.arrays['h8OwnerCodes']),
         [s.call('h8ActorRoom',i) for i in range(1,9)],list(h.arrays['bridgeQueue']))

class EveningBoundaries(unittest.TestCase):
 def test_02_false_return_preack_restore_fresh_retry_and_cancel(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s,b=pending(source,0);before=logical(h,s)
   for _ in range(4):service(h)
   self.assertEqual(logical(h,s),before);self.assertEqual(s.arrays['h8EW'][0],0);self.assertEqual(s.call('h8EveningCommitted'),0)
   self.assertEqual(s.arrays['h8IO'][0],3);talk(h);menu_pick(h,2);self.assertEqual(s.arrays['p08Words'][11],0)
   h,p,q,r,t,u,v,s,b=pending(source);until_io(h,s);self.assertEqual(s.arrays['h8IO'][0],4)
   pre=copy.deepcopy(next(iter(b.autosaved.values())));original_generation=list(s.arrays['h8IO'][1:3])
   service(h);self.assertEqual(s.call('h8EveningCommitted'),1)
   load(h,b,pre);self.assertEqual((s.call('h8EveningCommitted'),s.arrays['h8IO'][0],s.arrays['p08Words'][11]),(0,3,3))
   self.assertNotEqual(list(s.arrays['h8IO'][1:3]),original_generation)
   for _ in range(3):service(h)
   self.assertEqual(len(b.autosaved),1);talk(h);menu_pick(h,1)
   for _ in range(4):service(h)
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady'),len(b.autosaved)),(1,0,2))

 def test_03_output_refusal_explicit_same_receipt_retry_and_pending_restore(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s,b=pending(source);until_io(h,s);self.assertEqual(s.arrays['h8IO'][0],4)
   before=logical(h,s);io=list(s.arrays['h8IO']);h.p['bridgeSilent']=1
   service(h);self.assertEqual(logical(h,s),before);self.assertEqual(list(s.arrays['h8IO']),io)
   self.assertEqual(list(s.arrays['h8EC']),[io[1],io[2],1]);self.assertEqual(list(s.arrays['h8EP']),[0]*48)
   h.p['bridgeSilent']=0
   for _ in range(3):service(h)
   self.assertEqual(logical(h,s),before);self.assertEqual(len(b.autosaved),1)
   h.call('writeSave');self.assertIsNotNone(b.saved);failed_pending=copy.deepcopy(b.saved)
   talk(h);self.assertEqual([h.arrays['uiChoiceEnabled'][i] for i in range(2)],[1,1]);menu_pick(h,1)
   for _ in range(3):service(h)
   self.assertEqual((s.call('h8EveningCommitted'),len(b.autosaved)),(1,1))
   load(h,b,failed_pending);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.arrays['h8IO'][0]),(0,1,3))
   self.assertEqual(list(s.arrays['h8EC']),[0]*3);self.assertEqual(s.call('h8SaveReady'),1)
   for _ in range(3):service(h)
   self.assertEqual(len(b.autosaved),1);talk(h);menu_pick(h,2);self.assertEqual(s.arrays['p08Words'][11],0)

 def test_04_serial_output_capacity_and_stale_identity_refuse_before_commit(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s,b=pending(source);until_io(h,s);base=h.vm.snapshot()
   mutations=[('record_capacity',lambda:s.p.__setitem__('p08RecordCapacity',0)),('event_capacity',lambda:s.p.__setitem__('p08EventCapacity',0)),
    ('request',lambda:s.arrays['h8IO'].__setitem__(4,99)),('revision',lambda:s.arrays['h8IO'].__setitem__(6,99)),
    ('session',lambda:s.arrays['p08Session'].__setitem__(4,99)),('lease',lambda:s.p.__setitem__('h8Lease',99)),
    ('attempt_generation',lambda:s.arrays['h8IO'].__setitem__(2,0)),('route_generation',lambda:s.arrays['h8RouteWords'].__setitem__(31,99))]
   for name,mutate in mutations:
    h.vm.restore(copy.deepcopy(base));mutate();before=logical(h,s);service(h)
    self.assertEqual(logical(h,s),before,name);self.assertEqual(s.arrays['h8EW'][0],0,name)
    self.assertEqual(s.call('h8EveningCommitted'),0,name)
   h.vm.restore(copy.deepcopy(base))
   for arr,indices in [('p08Words',(12,13)),('h8R',(20,21)),('h8IO',(5,6))]:
    for i in indices:s.arrays[arr][i]=-1
   before=logical(h,s);service(h);self.assertEqual(logical(h,s),before)
   self.assertEqual(s.arrays['h8EW'][0],0);self.assertEqual(s.p['p08Busy'],0)

 def test_05_invalid_saved_witness_rejected_before_publishers_and_recoverable(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s,b=pending(source)
   for _ in range(4):service(h)
   h.call('writeSave');good=copy.deepcopy(b.saved);self.assertIsNotNone(good);live=h.vm.snapshot()
   mutations=[('phase',lambda:s.arrays['h8EW'].__setitem__(0,2)),('schema',lambda:s.arrays['h8EW'].__setitem__(1,2)),
    ('success',lambda:s.arrays['h8EW'].__setitem__(13,0)),('slot',lambda:s.arrays['h8EW'].__setitem__(12,100)),
    ('request',lambda:s.arrays['h8EW'].__setitem__(6,99)),('generation',lambda:s.arrays['h8EW'].__setitem__(4,99)),
    ('transition_document',lambda:s.arrays['h8EW'].__setitem__(42,1016)),('invented_seen_mask',lambda:s.arrays['h8EW'].__setitem__(47,1)),
    ('actor',lambda:r.p.__setitem__('hMiloRoom',4)),('staged_witness',lambda:s.arrays['h8EP'].__setitem__(0,1))]
   for name,mutate in mutations:
    h.vm.restore(copy.deepcopy(good));mutate();bad=h.vm.snapshot();h.vm.restore(copy.deepcopy(live));calls=h.vm.calls.copy()
    load(h,b,bad);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid']),(21,0),name)
    for key in ((983,'bInventory'),(984,'qInventory')):self.assertEqual(h.vm.calls[key],calls[key],name)
    load(h,b,good);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.call('h8EveningCommitted')),(0,1,1),name)
   self.assertEqual(len(b.autosaved),1)

 def test_06_complete_precommit_map_and_uncertain_postcommit_failure(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s,b=pending(source);until_io(h,s);base=h.vm.snapshot();good=copy.deepcopy(next(iter(b.autosaved.values())))
   changes=[('witness',lambda:s.arrays['h8EP'].__setitem__(12,99)),('prep',lambda:h.p.__setitem__('p02PlanAgreed',0)),
    ('reserved_document',lambda:s.arrays['h8ReservedDocuments'].__setitem__(0,1016)),
    ('reserved_owner',lambda:s.arrays['h8ReservedOwners'].__setitem__(0,3)),
    ('room',lambda:r.p.__setitem__('hMiloRoom',4)),('queue',lambda:h.p.__setitem__('bridgeQueueCount',h.p['bridgeQueueCount']+1)),
    ('session',lambda:s.arrays['p08Session'].__setitem__(4,99))]
   for name,mutate in changes:
    h.vm.restore(copy.deepcopy(base));before=list(s.arrays['p08Words']);owners=list(s.arrays['h8OwnerReceipts']);fired=[]
    def fault(obj,method,args,result):
     if obj.name=='p08State' and method=='h8UIReserve' and list(args)==[2] and s.p['p08Busy'] and not fired:fired.append(1);mutate()
    h.vm.after_actual_call=fault;service(h);h.vm.after_actual_call=None
    self.assertEqual(fired,[1],name);self.assertEqual(list(s.arrays['p08Words']),before,name)
    self.assertEqual(list(s.arrays['h8OwnerReceipts']),owners,name);self.assertEqual(s.arrays['h8EW'][0],0,name)
   h.vm.restore(copy.deepcopy(base));fired=[]
   def corrupt(obj,method,args,result):
    if obj.name=='p08State' and method=='h8CommitReserved' and result and not fired:fired.append(1);h.p['bridgeQueueCount']+=1
   h.vm.after_actual_call=corrupt;service(h);h.vm.after_actual_call=None
   self.assertEqual(fired,[1]);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid']),(20,0))
   self.assertEqual(s.call('h8EveningReady'),0);load(h,b,good)
   self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.arrays['h8EW'][0],s.arrays['p08Words'][11]),(0,1,0,3))

 def test_07_raw_input_lock_preserves_save_load_and_pure_history(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s,b=pending(source)
   for _ in range(4):service(h)
   before=logical(h,s);witness=list(s.arrays['h8EW']);xy=(h.p['motionX'],h.p['motionY'])
   for event in ({'type':1,'x':160,'y':140},{'type':4,'message':13},{'type':4,'message':27},{'type':1,'x':278,'y':30}):
    h.vm.pump([event,{}]);self.assertEqual(logical(h,s),before);self.assertEqual(h.p['motionPhase'],0)
    self.assertEqual((h.p['motionX'],h.p['motionY']),xy);self.assertEqual(list(s.arrays['h8EW']),witness)
   h.vm.pump([{'type':4,'message':15360},{}]);self.assertIsNotNone(b.saved)
   saved=copy.deepcopy(b.saved);self.assertEqual(s.call('h8EveningCommitted'),1)
   for field,value in [('h8Restoring',1),('h8RestoreValid',0),('h8Enabled',0)]:
    old=s.p[field];s.p[field]=value;self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(1,0));s.p[field]=old
   b.saved=copy.deepcopy(saved);restored=False
   try:h.vm.pump([{'type':4,'message':15616}])
   except RestoreTransfer:restored=True;replay(h)
   self.assertTrue(restored);self.assertEqual(s.p['h8RestoreValid'],1);self.assertEqual(list(s.arrays['h8EW']),witness)

if __name__=='__main__':unittest.main(verbosity=2)
