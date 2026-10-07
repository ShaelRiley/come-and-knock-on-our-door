"""Ordinary Main save/restore entrypoints with an explicit deterministic kernel backend.
Snapshots are in-memory harness data, never native SCI save files or I/O proof.
"""
import copy,unittest
import host
from host import act,frame
from test_cloth import ready,check,history
from test_transactions import make,layout,logical

class RestoreTransfer(Exception):pass

class Backend:
 def __init__(self,vm):
  self.vm=vm;self.saved=None;self.save_result=1;self.restore_result=1
  self.original=vm._kernel;self.operations=[];vm._kernel=self.kernel
 def kernel(self,k,args):
  name=self.vm.knames.get(k)
  if name=='SaveGame':
   assert args==[0,-1,0],args
   self.vm.ktrace.append((name,tuple(args)));self.operations.append(('save',self.save_result))
   if self.save_result==1:self.saved=copy.deepcopy(self.vm.snapshot())
   return self.save_result
  if name=='RestoreGame':
   assert args==[0,-1,0],args
   self.vm.ktrace.append((name,tuple(args)));self.operations.append(('restore',self.restore_result))
   if self.restore_result and self.saved is not None:
    self.vm.restore(copy.deepcopy(self.saved))
    raise RestoreTransfer() # successful native restore discards the old invocation stack
   return 0
  return self.original(k,args)

def replay(h,events=None):
 vm=h.vm;vm.event_queue=list(events or [{},{}])
 try:h.call('replay')
 except host.base.EndOfEvents:pass
 finally:vm.event_queue=None
 assert vm.depth==0

def load(h,backend,snapshot=None,events=None):
 if snapshot is not None:backend.saved=copy.deepcopy(snapshot)
 h.vm.event_queue=[{}]
 try:
  try:h.call('readSave')
  except RestoreTransfer:replay(h,events)
  else:raise AssertionError('Main readSave did not enter successful restore')
 finally:h.vm.event_queue=None

class Restore(unittest.TestCase):
 def test_ordinary_save_load_preserves_both_cloth_places(self):
  for source in (False,True):
   for cloth in (39,38):
    h,p,q,r,t,u,v,s=ready(source,cloth);backend=Backend(h.vm);original=history(p)
    self.assertEqual(s.call('h8SaveReady'),1)
    h.call('writeSave');self.assertIsNotNone(backend.saved);hook=copy.deepcopy(backend.saved)
    words=list(s.arrays['p08Words']);act(h,4,cloth);check(self,h,p,q,s,cloth,2)
    h.call('writeSave');pocket=copy.deepcopy(backend.saved)
    receipts=list(s.arrays['h8ClothHistory']);act(h,7,cloth,45);check(self,h,p,q,s,cloth,1)
    load(h,backend,pocket,events=[{'type':4,'message':27},{'type':4,'message':13},{},{}])
    self.assertEqual((s.p['h8RestoreValid'],s.p['h8Restoring'],s.p['h8Enabled'],h.p['uiFailure']),(1,0,1,0))
    check(self,h,p,q,s,cloth,2);self.assertEqual(list(s.arrays['h8ClothHistory']),receipts)
    self.assertEqual(list(s.arrays['p08Words']),words);self.assertEqual(history(p),original)
    load(h,backend,hook);check(self,h,p,q,s,cloth,1)
    self.assertEqual(list(s.arrays['h8ClothHistory']),[0]*6)
    self.assertEqual(list(s.arrays['p08Words']),words);self.assertEqual(history(p),original)
    load(h,backend,hook);check(self,h,p,q,s,cloth,1)
    act(h,4,cloth);check(self,h,p,q,s,cloth,2)
    self.assertEqual(list(s.arrays['h8ClothHistory']),[0,1,0,1,0,0])

 def test_raw_corruption_rejected_before_inventory_publication(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=ready(source);backend=Backend(h.vm)
   h.call('writeSave');clean=copy.deepcopy(backend.saved);live=h.vm.snapshot()
   def mutate(kind):
    if kind=='ui_tail':h.arrays['uiItems'][63]=25
    elif kind=='ui_duplicate':h.arrays['uiItems'][1]=h.arrays['uiItems'][0]
    elif kind=='ui_fixed':h.arrays['uiItems'][0]=63
    elif kind=='ui_unheld':h.arrays['uiItems'][0]=75
    elif kind=='extent_negative':h.p['uiInventoryExtent']=-1
    elif kind=='extent_oversized':h.p['uiInventoryExtent']=65
    elif kind=='padding_history':p.p['p03Padding']=0
    elif kind=='owner_receipt':s.arrays['h8OwnerReceipts'][1]+=1
    elif kind=='cloth_receipt':s.arrays['h8ClothHistory'][3]=1
    elif kind=='reservation_alias':
     i=q.p['qExtent'];q.p['qExtent']=i+1;q.arrays['qReserve'][4]=i;q.arrays['qReserve'][39]=i
    elif kind=='busy':s.p['p08Busy']=1
    elif kind=='uncertain':s.p['p08Uncertain']=1
    elif kind=='critical':s.p['h8Critical']=1
    else:raise AssertionError(kind)
   for kind in ('ui_tail','ui_duplicate','ui_fixed','ui_unheld','extent_negative','extent_oversized','padding_history','owner_receipt','cloth_receipt','reservation_alias','busy','uncertain','critical'):
    with self.subTest(source=source,kind=kind):
     h.vm.restore(copy.deepcopy(clean));mutate(kind)
     h.p.update(motionVerb=7,motionFirst=39,motionSecond=45,motionPhase=1,audioPending=1)
     bad=h.vm.snapshot();before=list(h.arrays['uiItems'])
     # Corruption belongs to the requested saved file, not the current loading session.
     h.vm.restore(copy.deepcopy(live));calls=h.vm.calls.copy();h.vm.ktrace=[]
     load(h,backend,bad)
     self.assertEqual((s.p['h8Failure'],s.p['h8Enabled'],s.p['h8RestoreValid'],s.p['h8Restoring']),(21,0,0,0))
     self.assertEqual(list(h.arrays['uiItems']),before)
     self.assertEqual(h.vm.calls[(983,'bInventory')],calls[(983,'bInventory')])
     self.assertEqual(h.vm.calls[(984,'qInventory')],calls[(984,'qInventory')])
     self.assertEqual((h.p['motionVerb'],h.p['motionFirst'],h.p['motionSecond'],h.p['motionPhase'],h.p['audioPending']),(0,0,0,0,0))
     self.assertIn(('DoAudio',(3,)),h.vm.ktrace);self.assertIn(('DoSync',(2,)),h.vm.ktrace)
     old=list(s.arrays['p08Words']);room=h.p['location'];h.call('hostActNow',0,18,0);h.call('writeSave')
     self.assertEqual(list(s.arrays['p08Words']),old);self.assertEqual(h.p['location'],room)
   load(h,backend,clean);check(self,h,p,q,s,39,1)
   self.assertEqual((s.p['h8Failure'],s.p['h8Enabled'],s.p['h8RestoreValid']),(0,1,1))

 def test_save_restore_cancel_failure_and_retry_keep_ownership(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=ready(source);backend=Backend(h.vm);act(h,4,39)
   words=list(s.arrays['p08Words']);receipts=list(s.arrays['h8ClothHistory']);old=history(p)
   for result in (0,0,1):
    backend.save_result=result;h.call('writeSave')
    self.assertEqual(h.p['audioSaveResult'],result)
    self.assertEqual(list(s.arrays['p08Words']),words);self.assertEqual(list(s.arrays['h8ClothHistory']),receipts)
    check(self,h,p,q,s,39,2)
    if result==0:self.assertIsNone(backend.saved)
   self.assertEqual(backend.operations,[('save',0),('save',0),('save',1)])
   saved=copy.deepcopy(backend.saved);backend.restore_result=0
   for _ in range(2):
    h.call('readSave');check(self,h,p,q,s,39,2)
    self.assertEqual(list(s.arrays['p08Words']),words);self.assertEqual(list(s.arrays['h8ClothHistory']),receipts)
   act(h,7,39,45);check(self,h,p,q,s,39,1)
   # A failed replacement cannot erase the earlier successful pocket snapshot.
   backend.save_result=0;h.call('writeSave');self.assertEqual(backend.saved,saved)
   backend.restore_result=1;load(h,backend,saved);check(self,h,p,q,s,39,2)
   self.assertEqual(list(s.arrays['h8ClothHistory']),receipts);self.assertEqual(history(p),old)

 def test_genuine_early_plan_save_restore_keeps_reservation_holes(self):
  import campaign_route
  class Stop(Exception):pass
  stage=campaign_route.stage
  try:
   for source in (False,True):
    def capture(h,label):
     if label=='P02':
      backend=Backend(h.vm);p=h.vm.objects['p03State'];q=h.vm.objects['p04State'];s=h.vm.objects['p08State']
      before=(list(h.arrays['uiItems']),list(p.arrays['bSlots']),list(q.arrays['qSlots']))
      self.assertEqual(s.call('h8SaveReady'),1);h.call('writeSave');self.assertIsNotNone(backend.saved)
      load(h,backend);self.assertEqual((s.p['h8Enabled'],s.p['h8Failure']),(1,0))
      self.assertEqual((list(h.arrays['uiItems']),list(p.arrays['bSlots']),list(q.arrays['qSlots'])),before)
      self.assertEqual(s.call('h8Preparations'),1);raise Stop()
    campaign_route.stage=capture
    with self.assertRaises(Stop):campaign_route.prepared(source)
  finally:campaign_route.stage=stage

 def test_unimplemented_host_histories_reject_even_when_domain_valid(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=ready(source);backend=Backend(h.vm)
   h.call('writeSave');clean=copy.deepcopy(backend.saved);live=h.vm.snapshot()
   for kind in ('intro','source','hint','canceled_request','checklist_pending','confirmed_pending','evening'):
    with self.subTest(source=source,kind=kind):
     h.vm.restore(copy.deepcopy(clean));w=s.arrays['p08Words'];w[12]=0;w[13]=100
     if kind=='intro':w[53]=90
     elif kind=='source':w[33]=90
     elif kind=='hint':w[10]=1
     else:
      w[15]=1
      if kind in ('checklist_pending','confirmed_pending'):
       w[11]=2 if kind=='checklist_pending' else 3;w[17]=1;w[19]=90;w[21]=91
       if kind=='confirmed_pending':w[23]=92
      elif kind=='evening':
       w[9]=1;w[25]=1;w[27]=90;w[29]=91;w[31]=92;w[57]=93
     self.assertEqual(s.call('p08ValidateCurrent',0),0,kind)
     self.assertEqual(s.call('h8SaveReady'),0,kind)
     expected=list(w);bad=h.vm.snapshot();h.vm.restore(copy.deepcopy(live));load(h,backend,bad)
     self.assertEqual((s.p['h8Failure'],s.p['h8Enabled']),(21,0))
     self.assertEqual(list(s.arrays['p08Words']),expected)
   # Recovery cancellation is distinct from per-frame admission. Exercise two
   # cancellations, another invalid load, then one fully validated good load.
   backend.restore_result=0
   for _ in range(2):
    attempts=len(backend.operations);h.vm.event_queue=[{}]
    try:h.call('readSave')
    finally:h.vm.event_queue=None
    self.assertEqual(len(backend.operations),attempts+1)
    self.assertEqual((s.p['h8Failure'],s.p['h8Enabled']),(21,0))
   backend.restore_result=1;load(h,backend,bad)
   self.assertEqual((s.p['h8Failure'],s.p['h8Enabled']),(21,0))
   load(h,backend,clean);self.assertEqual((s.p['h8Failure'],s.p['h8Enabled']),(0,1))

 def test_mid_restore_actions_and_later_owner_failure_stay_locked(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=ready(source);backend=Backend(h.vm);h.call('writeSave')
   saved=copy.deepcopy(backend.saved);live=h.vm.snapshot();seen=[]
   guarded=[('hostActNow',(0,18,0)),('uiHostAct',(0,18,0)),('bridgeActAtArrival',(0,18,0)),('uiHostChoice',(204,1)),('uiHostConfirm',(201,)),('writeSave',()),('readSave',()),('dialoguePresented',()),('uiClose',()),('speechPoll',())]
   def reenter(obj,name,args,result):
    if obj.name=='p08State' and name=='p08LoadFinish' and s.p['h8Restoring']==1 and not seen:
     seen.append('loaded');before=logical(h);words=list(s.arrays['p08Words']);operations=list(backend.operations)
     for method,values in guarded:h.call(method,*values)
     self.assertEqual(logical(h),before);self.assertEqual(list(s.arrays['p08Words']),words)
     self.assertEqual(backend.operations,operations);self.assertEqual(s.p['h8Enabled'],0)
    if obj.name=='p08State' and name=='p08BindSession' and s.p['h8Restoring']==1:
     self.assertEqual(h.vm.event_queue,[{}]);self.assertEqual((h.p['type'],h.p['message'],h.p['motionPhase'],h.p['audioPending']),(0,0,0,0))
     seen.append('retired-before-bind')
   h.vm.after_actual_call=reenter
   load(h,backend,saved,events=[{'type':1,'x':106,'y':98},{'type':4,'message':13},{},{}])
   self.assertEqual(seen,['loaded','retired-before-bind']);check(self,h,p,q,s,39,1)
   h.vm.after_actual_call=None
   # Real P06 geography is checked after P08 raw admission and public branch load.
   h.vm.restore(copy.deepcopy(saved));t.p['h6VivianRoom']=5;bad=h.vm.snapshot()
   h.vm.restore(copy.deepcopy(live));before=h.vm.calls[(989,'p08LoadFinish')];load(h,backend,bad)
   self.assertEqual((s.p['h8Failure'],s.p['h8Enabled'],s.p['h8RestoreValid']),(21,0,0))
   if not source:self.assertGreater(h.vm.calls[(989,'p08LoadFinish')],before)
   self.assertEqual(t.p['h6VivianRoom'],5)
   load(h,backend,saved);self.assertEqual(t.p['h6VivianRoom'],0);check(self,h,p,q,s,39,1)

if __name__=='__main__':unittest.main(verbosity=2)
