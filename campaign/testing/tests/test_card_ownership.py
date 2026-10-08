"""Inactive ownership foundation; genuine domain actions, ordinary mocked saves.
P09 contexts here are local model inputs, NOT a native source-reader/epoch proof.
P08 history is earned through actual existing P01-P08 host actions and ACK.
"""
import sys
sys.dont_write_bytecode=True
import copy,json,unittest
from pathlib import Path
import host
from source_host import VM as SourceVM
from test_return_caption import boot,first_entry
from test_confirmation_boundaries import stage
from test_layout_controls import menu_pick
from test_storage_kernel import service
from storage_kernel_profile import StorageBackend
from test_restore import Backend,load
H=Path(__file__).resolve().parents[1]
EMITTED=host.VM
CACHE={}

def fresh(source):
 old=host.VM;host.VM=SourceVM if source else EMITTED
 try:return boot(H)
 finally:host.VM=old

def committed(source):
 if source not in CACHE:
  h,*_=stage(source,'menu');s=h.vm.objects['p08State'];b=StorageBackend(h.vm,occupied=range(1,26))
  menu_pick(h,1)
  for _ in range(5):service(h)
  assert s.call('h8EveningCommitted')==1 and s.call('h8EveningReady')==0
  CACHE[source]=h.vm.snapshot()
 vm=SourceVM() if source else EMITTED();vm.budget=900000000;vm.restore(copy.deepcopy(CACHE[source]));return vm.objects['cakood'],vm.objects['p09State']

def context(d):
 assert d.call('p09Context',6,0,1,1,6,6,0,0,d.p['p09RumorCleared'],d.p['p09Ready'],d.p['p09Epoch']+1)==1

def acknowledge(d,source,first=0,last=0,record=0):
 return d.call('p09Acknowledge',source,d.call('p09SerialHi',source+3),d.call('p09SerialLo',source+3),d.p['p09Epoch'],record,first,last)

def terms(d,count=5):
 context(d);assert d.call('p09Begin',4)==17
 assert acknowledge(d,4,4,4)==19 # Earliest genuine Stringer correction.
 assert d.p['p09RumorCleared']==1
 assert d.call('p09Begin',7)==17
 for unit in range(9,9+count):assert acknowledge(d,7,unit,unit)==19
 assert d.call('p09Validate')==1

def words(d):return [d.call('p09Word',i) for i in range(77)]
def owners(h):
 p=h.vm.objects['p03State'];q=h.vm.objects['p04State'];s=h.vm.objects['p08State']
 return (list(h.arrays['p02Slots']),list(h.arrays['p02Reserved']),list(p.arrays['bSlots']),list(p.arrays['bReserve']),list(q.arrays['qSlots']),list(q.arrays['qReserve']),list(s.arrays['h8OwnerReceipts']),list(s.arrays['h8OwnerCodes']))

def card_check(t,h,d,present):
 t.assertEqual(d.call('h9SaveReady'),1)
 t.assertEqual(h.call('campaignHeld',399),int(present))
 t.assertEqual(h.call('p02ObjectLocation',399),10 if present else -1)
 t.assertEqual(h.call('campaignReachable',399),0) # No P09 player dispatch in this gate.
 slots=list(h.arrays['uiItems']);t.assertEqual(slots.count(399),int(present))
 t.assertEqual(d.call('h9CardReservation',399),slots.index(399) if present else -1)
 t.assertEqual((d.call('h9Active'),h.vm.objects['p08State'].call('h8EveningReady')),(0,0))

class CardOwnership(unittest.TestCase):
 def test_01_fresh_inactive_high_id_guards_and_ordinary_save(self):
  for source in (False,True):
   h=fresh(source);d=h.vm.objects['p09State'];p10=h.vm.objects['p10State'];before=words(d);old=owners(h);p10old=(dict(p10.p),{n:list(v) for n,v in p10.arrays.items()})
   for obj in (-32768,-1,0,32,94,95,394,395,396,397,398,399,400,32767):
    self.assertEqual(d.call('h9CardIndex',obj),0 if obj==399 else -1)
    self.assertEqual(d.call('h9CardReservation',obj),-1)
    if obj>=95:self.assertEqual(h.call('campaignHeld',obj),0)
    self.assertEqual(h.call('p03HostReservation',obj),-1)
   for obj in range(395,400):
    for v in range(1,10):
     h.call('hostActNow',v,obj,0);h.call('hostActNow',v,25,obj)
   self.assertEqual(words(d),before);self.assertEqual(owners(h),old)
   self.assertEqual(h.call('p02HostInventory'),1);card_check(self,h,d,False)
   first_entry(h);host.act(h,0,12);backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved)
   load(h,backend);card_check(self,h,d,False)
   self.assertEqual((dict(p10.p),{n:list(v) for n,v in p10.arrays.items()}),p10old)

 def test_02_each_terms_unit_earns_one_unsigned_original_before_separate_success(self):
  for source in (False,True):
   h,d=committed(source);old=owners(h);context(d)
   self.assertEqual(d.call('p09Begin',4),17);self.assertEqual(acknowledge(d,4,4,4),19)
   self.assertEqual(d.call('h9ProjectCard'),1);card_check(self,h,d,False)
   self.assertEqual(d.call('p09Begin',7),17)
   for unit in range(9,14):
    self.assertEqual(acknowledge(d,7,unit,unit),19)
    self.assertEqual(d.p['p09Ready'],int(unit==13))
    self.assertEqual(d.call('h9ProjectCard'),1);card_check(self,h,d,unit==13)
   self.assertEqual(d.call('p09Count',7),5);self.assertEqual(d.call('p09PendingAt',0),4)
   self.assertIn(7,[d.call('p09PendingAt',i) for i in range(9)])
   # Selection is a closed host-state fixture, not an active card control.
   h.p.update(uiInventoryPage=h.p['uiInventoryPages']-1,uiNounA=399,uiVerb=7,uiFocus=3)
   view=tuple(h.p[n] for n in ('uiInventoryExtent','uiInventoryPages','uiInventoryPage','uiNounA','uiVerb','uiFocus'))
   after=words(d);slots=list(h.arrays['uiItems']);reservation=d.call('h9CardReservation',399)
   for _ in range(3):
    self.assertEqual(acknowledge(d,7,13,13),18);self.assertEqual(d.call('h9ProjectCard'),1);self.assertEqual(h.call('p02HostInventory'),1)
    self.assertEqual(words(d),after);self.assertEqual(list(h.arrays['uiItems']),slots);self.assertEqual(d.call('h9CardReservation',399),reservation)
    self.assertEqual(tuple(h.p[n] for n in ('uiInventoryExtent','uiInventoryPages','uiInventoryPage','uiNounA','uiVerb','uiFocus')),view)
   self.assertEqual(owners(h),old)
   self.assertEqual(acknowledge(d,7,20,20),19);self.assertEqual(d.call('p09Count',7),6)
   self.assertEqual(d.call('h9ProjectCard'),1);card_check(self,h,d,True)
   for action in (1,3,4,7,8,9):self.assertEqual(d.call('p09Act',action,399,0),24)
   self.assertEqual(owners(h),old)

 def test_03_partial_and_card_save_restore_resume_without_regrant(self):
  for source in (False,True):
   h,d=committed(source);terms(d,3);self.assertEqual(d.call('h9ProjectCard'),1);backend=Backend(h.vm)
   h.call('writeSave');self.assertIsNotNone(backend.saved);partial=copy.deepcopy(backend.saved);partialwords=words(d)
   load(h,backend,partial);self.assertEqual(words(d),partialwords);card_check(self,h,d,False)
   self.assertEqual(d.p['p09ContextValid'],0);self.assertEqual(list(d.arrays['p09Lease']),[0]*10)
   context(d);self.assertEqual(d.call('p09Resume',7),17)
   for unit in (12,13):self.assertEqual(acknowledge(d,7,unit,unit),19)
   self.assertEqual(d.call('h9ProjectCard'),1);old=owners(h);cardwords=words(d)
   self.assertEqual(d.call('p09Count',7),5)
   h.call('writeSave');card=copy.deepcopy(backend.saved);self.assertNotEqual(card,partial)
   for _ in range(2):
    load(h,backend,card);card_check(self,h,d,True);self.assertEqual(words(d),cardwords);self.assertEqual(owners(h),old)
   context(d);self.assertEqual(d.call('p09Resume',7),17);self.assertEqual(acknowledge(d,7,20,20),19)
   self.assertEqual(d.call('p09Count',7),6);self.assertEqual(d.call('h9ProjectCard'),1)
   h.call('writeSave');completed=copy.deepcopy(backend.saved);load(h,backend,completed);card_check(self,h,d,True)
   load(h,backend,partial);card_check(self,h,d,False);self.assertEqual(words(d),partialwords)

 def test_04_owner_consistency_duplicate_capacity_and_high_id_reject_without_old_array_writes(self):
  for source in (False,True):
   h,d=committed(source);terms(d);self.assertEqual(d.call('h9ProjectCard'),1);clean=h.vm.snapshot();old=owners(h)
   for kind in ('duplicate','high_id','reservation','legacy_owner'):
    h.vm.restore(copy.deepcopy(clean));slot=d.call('h9CardReservation',399)
    if kind=='duplicate':h.arrays['uiItems'][h.p['uiInventoryExtent']]=399;h.p['uiInventoryExtent']+=1
    elif kind=='high_id':h.arrays['uiItems'][slot]=400
    elif kind=='reservation':d.arrays['h9CardSlot'][0]=slot-1
    else:h.vm.objects['p04State'].arrays['qSlots'][0]=399
    state=(list(h.arrays['uiItems']),list(d.arrays['h9CardSlot']),owners(h))
    self.assertEqual(d.call('h9InventoryValid'),0,kind);self.assertEqual(d.call('h9ProjectCard'),0,kind)
    backend=Backend(h.vm);h.call('writeSave');self.assertIsNone(backend.saved)
    self.assertEqual((list(h.arrays['uiItems']),list(d.arrays['h9CardSlot']),owners(h)),state)
   h.vm.restore(copy.deepcopy(clean));self.assertEqual(owners(h),old)
   # Full roster is a bounded capacity condition; no publication can overrun64.
   slot=d.call('h9CardReservation',399);h.arrays['uiItems'][slot]=0;h.p['uiInventoryExtent']=64
   before=list(h.arrays['uiItems']);self.assertEqual(d.call('h9ProjectCard'),0);self.assertEqual(list(h.arrays['uiItems']),before)
   # Negative staged-rebuild fixture: 58 legacy cells leave six slots but
   # not seven. Reject before projecting cues or mutating either reservation.
   h.vm.restore(copy.deepcopy(clean));p10=h.vm.objects['p10State']
   for i,obj in enumerate(h.arrays['uiItems']):
    if obj==399 or obj in (48,49,50,412,413,414):h.arrays['uiItems'][i]=0
   h.p['uiInventoryExtent']=58;h.p['uiInventoryPages']=8
   p10.arrays['h10S'][:]=[-1]*6
   before=(list(h.arrays['uiItems']),list(p10.arrays['h10S']),list(d.arrays['h9CardSlot']),h.p['uiInventoryExtent'])
   self.assertEqual(d.call('h9ProjectCard'),0)
   self.assertEqual((list(h.arrays['uiItems']),list(p10.arrays['h10S']),list(d.arrays['h9CardSlot']),h.p['uiInventoryExtent']),before)

 def test_05_ordinary_rejected_save_recovery_never_repairs_missing_card(self):
  for source in (False,True):
   h,d=committed(source);terms(d);self.assertEqual(d.call('h9ProjectCard'),1);backend=Backend(h.vm)
   h.call('writeSave');good=copy.deepcopy(backend.saved);self.assertIsNotNone(good);live=h.vm.snapshot()
   slot=d.call('h9CardReservation',399);h.arrays['uiItems'][slot]=0;bad=h.vm.snapshot();h.vm.restore(copy.deepcopy(live))
   load(h,backend,bad);self.assertEqual(d.arrays['h9CardAdmission'][0],0);self.assertNotIn(399,h.arrays['uiItems']);self.assertEqual(d.p['p09Ready'],1)
   self.assertEqual(h.p['uiFailure'],10);self.assertEqual(d.call('h9ProjectCard'),0);self.assertEqual(d.call('h9SaveReady'),0)
   for _ in range(2):
    backend.restore_result=0;h.vm.event_queue=[{}]
    try:h.call('readSave')
    finally:h.vm.event_queue=None
    self.assertNotIn(399,h.arrays['uiItems'])
   backend.restore_result=1;load(h,backend,good);card_check(self,h,d,True);self.assertEqual(h.p['uiFailure'],0)
   backend.save_result=0;before=copy.deepcopy(backend.saved);h.call('writeSave');self.assertEqual(backend.saved,before);card_check(self,h,d,True)

 def test_06_persistent_history_required_and_dispatch_closed_even_for_genuine_card(self):
  for source in (False,True):
   h=fresh(source);d=h.vm.objects['p09State'];terms(d)
   self.assertEqual(d.call('p09Validate'),1);self.assertEqual(d.call('h9OwnershipValid'),0);self.assertEqual(d.call('h9ProjectCard'),0)
   self.assertNotIn(399,h.arrays['uiItems'])
   h,d=committed(source);terms(d);self.assertEqual(d.call('h9ProjectCard'),1);before=words(d);slots=list(h.arrays['uiItems']);old=owners(h)
   for obj in range(395,400):
    for v in range(1,10):
     self.assertEqual(d.call('h9Dispatch',v,obj,0),1);h.call('hostActNow',v,obj,0)
   self.assertEqual(words(d),before);self.assertEqual(list(h.arrays['uiItems']),slots);self.assertEqual(owners(h),old)
   self.assertEqual(d.call('h9UI',0),0);self.assertEqual(d.call('h9UI',1),0);card_check(self,h,d,True)

if __name__=='__main__':unittest.main(verbosity=2)
