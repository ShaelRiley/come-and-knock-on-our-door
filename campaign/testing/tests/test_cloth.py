"""Original-cloth continuation through actual legacy dispatch and inventory publishers.
This gate does not claim native pixels or ordinary P08 save/restore yet.
"""
import copy,unittest,sys
from pathlib import Path
import host
from host import act,choice,close,frame
from test_transactions import make,layout,logical
from campaign_route import living
from test_practical import input_action,arrive
from source_host import VM as SourceVM


def ready(source=False,cloth=39):
 h,p,q,r,t,u,v,s=make(source,cloth);layout(s)
 living(h);act(h,0,12)
 assert h.p['location']==2 and s.p['h8PaddingPlace']==1
 assert s.call('h8ClothRawValid')==1
 return h,p,q,r,t,u,v,s

def history(p):return {k:p.p[k] for k in ('p03Padding','p03Towel','p03Napkin','p03Ready','p03Approved','p03Slate','p03CompleteHi','p03CompleteLo')}

def check(test,h,p,q,s,cloth,place):
 test.assertEqual(s.p['h8PaddingPlace'],place)
 test.assertEqual(s.call('h8ClothRawValid'),1);test.assertEqual(p.call('p03Validate'),1);test.assertEqual(q.call('qValidateLayout'),1)
 test.assertEqual([list(items).count(cloth) for items in (h.arrays['uiItems'],p.arrays['bSlots'],q.arrays['qSlots'])],[int(place==2)]*3)
 test.assertEqual(h.call('campaignHeld',cloth),int(place==2))
 test.assertEqual(h.call('p02ObjectLocation',cloth),10 if place==2 else 2)

class Cloth(unittest.TestCase):
 def test_original_take_return_and_all_legacy_publishers(self):
  for source in (False,True):
   for cloth in (39,38):
    h,p,q,r,t,u,v,s=ready(source,cloth);before=history(p);core=list(s.arrays['p08Words'])
    act(h,4,cloth);check(self,h,p,q,s,cloth,2)
    first=list(s.arrays['h8ClothHistory']);self.assertEqual(first,[0,1,0,1,0,0])
    act(h,4,cloth);self.assertEqual(list(s.arrays['h8ClothHistory']),first)
    for owner,method,args in [(p,'bInventory',(h,)),(q,'qInventory',(h,)),(t,'h6Inventory',()),(h,'p02HostInventory',()),(h,'p03HostUIItem',(63,0))]:
     owner.call(method,*args);check(self,h,p,q,s,cloth,2)
    act(h,5,cloth);check(self,h,p,q,s,cloth,2)
    self.assertEqual(history(p),before);self.assertEqual(list(s.arrays['p08Words']),core)
    act(h,7,cloth,45);check(self,h,p,q,s,cloth,1)
    self.assertEqual(list(s.arrays['h8ClothHistory']),[0,2,0,1,0,2])
    act(h,7,cloth,45);self.assertEqual(list(s.arrays['h8ClothHistory']),[0,2,0,1,0,2])
    act(h,4,45);check(self,h,p,q,s,cloth,2)
    self.assertEqual(list(s.arrays['h8ClothHistory']),[0,3,0,3,0,2])
    self.assertEqual(history(p),before);self.assertEqual(list(s.arrays['p08Words']),core)
 def test_carry_across_rooms_wedge_hint_and_later_layout(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=ready(source);before=history(p);act(h,4,39)
   h.call('p03PreparationHint');choice(h,228,2);check(self,h,p,q,s,39,2)
   for args in ((0,18),(0,17),(0,14),(2,60),(7,4,60)):
    act(h,*args);check(self,h,p,q,s,39,2)
   self.assertEqual(q.p['p04Wedge'],1);self.assertEqual(h.call('campaignHeld',4),0)
   act(h,4,4);self.assertEqual(q.p['p04Wedge'],0)
   living(h);act(h,0,13)
   self.assertEqual(s.call('h8Context'),1);self.assertEqual(s.call('h8RunLayout',1,4,4),1)
   check(self,h,p,q,s,39,2);self.assertEqual(history(p),before)
   saved=list(s.arrays['h8ClothHistory']);act(h,7,39,45)
   self.assertEqual(list(s.arrays['h8ClothHistory']),saved);check(self,h,p,q,s,39,2)
 def test_roster_capacity_and_reservation_fail_before_publication(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=ready(source);before=history(p);domain=list(s.arrays['p08Words']);ui=list(h.arrays['uiItems'])
   extent=q.p['qExtent'];slot=q.arrays['qReserve'][39]
   q.p['qExtent']=64;q.arrays['qReserve'][39]=-1
   self.assertEqual(s.call('h8MoveCloth',2),0)
   self.assertEqual(s.p['h8PaddingPlace'],1);self.assertEqual(list(s.arrays['h8ClothHistory']),[0]*6)
   self.assertEqual(list(h.arrays['uiItems']),ui);self.assertEqual(q.p['qFailure'],0)
   q.p['qExtent']=extent;q.arrays['qReserve'][39]=extent
   self.assertEqual(s.call('h8MoveCloth',2),0);self.assertEqual(list(h.arrays['uiItems']),ui)
   q.arrays['qReserve'][39]=slot
   self.assertEqual(s.call('h8MoveCloth',2),1);check(self,h,p,q,s,39,2)
   self.assertEqual(history(p),before);self.assertEqual(list(s.arrays['p08Words']),domain)
 def test_post_publication_inventory_mismatch_locks_actions(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=ready(source);before=history(p)
   def corrupt(obj,name,args,result):
    if obj.name=='p03State' and name=='bInventory' and result and s.p['h8Critical'] and not getattr(h.vm,'cloth_fault',False):
     h.vm.cloth_fault=True;h.arrays['uiItems'][0]=39
   h.vm.after_actual_call=corrupt
   self.assertEqual(s.call('h8MoveCloth',2),0)
   self.assertEqual((s.p['h8Failure'],s.p['h8Enabled'],s.p['h8RestoreValid']),(20,0,0))
   h.call('hostActNow',0,18,0);h.call('writeSave')
   self.assertEqual(h.p['location'],2);self.assertEqual(h.vm.kernel_attempts['SaveGame'],0)
   self.assertEqual(history(p),before)
 def test_measured_hook_keyboard_two_noun_and_original_cels(self):
  hook_calls=[(11,87,103,90,108,1,7,0,0),(11,88,104,89,107,1,12,0,0),(11,89,104,96,106,1,7,0,0),(11,89,105,95,106,1,10,0,0),(11,94,104,97,110,1,7,0,0),(11,94,105,96,109,1,10,0,0),(11,92,108,96,110,1,7,0,0),(11,92,108,95,109,1,12,0,0)]
  for source in (False,True):
   for cloth,cel,x in ((39,5,101),(38,6,104)):
    h,p,q,r,t,u,v,s=ready(source,cloth);h.call('uiBuildFocus')
    ids=[i for i in range(h.p['uiControlCount']) if h.arrays['uiActions'][i]==1 and h.arrays['uiPayloads'][i] in (cloth,45)]
    self.assertEqual(len(ids),1);i=ids[0]
    self.assertEqual([h.arrays[n][i] for n in ('uiLefts','uiTops','uiRights','uiBottoms')],[97,84,121,110])
    self.assertEqual(h.arrays['uiPayloads'][i],cloth)
    self.assertEqual((h.call('approachX',cloth),h.call('approachY',cloth)),(139,130))
    self.assertEqual((h.call('approachX',77-cloth),h.call('approachY',77-cloth)),(124,130))
    self.assertFalse(any(h.arrays['uiActions'][i]==1 and h.arrays['uiPayloads'][i] in (34,36,40) for i in range(h.p['uiControlCount'])))
    h.vm.ktrace=[];h.call('drawKitchen')
    self.assertEqual([a for n,a in h.vm.ktrace if n=='Graph' and a in hook_calls],hook_calls)
    self.assertIn(('DrawCel',(224,0,cel,x,96,-1,0)),h.vm.ktrace)
    self.assertFalse(any(n=='DrawCel' and a[:3] in ((224,0,1),(224,0,4)) for n,a in h.vm.ktrace))
    input_action(h,4,cloth);arrive(h);close(h);check(self,h,p,q,s,cloth,2)
    h.call('uiBuildFocus');ids=[i for i in range(h.p['uiControlCount']) if h.arrays['uiActions'][i]==1 and h.arrays['uiPayloads'][i] in (cloth,45)]
    self.assertEqual([h.arrays['uiPayloads'][i] for i in ids],[45])
    h.vm.ktrace=[];h.call('drawKitchen');self.assertNotIn(('DrawCel',(224,0,cel,x,96,-1,0)),h.vm.ktrace)
    input_action(h,7,cloth,45);arrive(h);close(h);check(self,h,p,q,s,cloth,1)
    # The other original remains a normal drawer item with its own old P03 lifecycle.
    act(h,4,77-cloth)
    self.assertEqual(h.arrays['uiItems'].count(77-cloth),1);check(self,h,p,q,s,cloth,1)
 def test_alias_and_preexisting_diagnostics_reject_unchanged(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=ready(source);pristine=h.vm.snapshot()
   for owner,prefix,validator in ((p,'b','b8Valid'),(q,'q','q8Valid')):
    extent=owner.p[prefix+'Extent'];owner.p[prefix+'Extent']=extent+1
    owner.arrays[prefix+'Reserve'][4]=extent;owner.arrays[prefix+'Reserve'][39]=extent
    self.assertEqual(owner.call(validator),0)
    ui=list(h.arrays['uiItems']);self.assertEqual(s.call('h8MoveCloth',2),0)
    self.assertEqual((s.p['h8PaddingPlace'],list(s.arrays['h8ClothHistory'])),(1,[0]*6))
    self.assertEqual(list(h.arrays['uiItems']),ui);h.vm.restore(copy.deepcopy(pristine))
   for owner,flag in ((p,'bFailure'),(q,'qFailure')):
    owner.p[flag]=3;ui=list(h.arrays['uiItems'])
    self.assertEqual(s.call('h8MoveCloth',2),0);self.assertEqual(owner.p[flag],3)
    self.assertEqual((s.p['h8PaddingPlace'],s.p['h8Failure'],h.p['uiFailure']),(1,0,0))
    self.assertEqual(list(s.arrays['h8ClothHistory']),[0]*6);self.assertEqual(list(h.arrays['uiItems']),ui)
    h.vm.restore(copy.deepcopy(pristine))
   def late_failure(obj,name,args,result):
    if obj.name=='p04State' and name=='qInventory' and result and s.p['h8Critical']:
     q.p['qFailure']=3
   h.vm.after_actual_call=late_failure
   self.assertEqual(s.call('h8MoveCloth',2),0)
   self.assertEqual((s.p['h8Failure'],s.p['h8Enabled']),(20,0))
 def test_existing_p06_held_props_survive_old_publishers(self):
  from p06_support import materials
  for source in (False,True):
   old=host.VM;host.VM=SourceVM if source else old
   try:h,d,a,p,q,r=host.setup()
   finally:host.VM=old
   s=h.vm.objects['p08State'];h.p['p08']=s
   if not s.p['h8Host']:self.assertEqual(s.call('h8Init',h),1)
   materials(h);living(h);act(h,0,12);act(h,4,39)
   for owner,method,args in [(p,'bInventory',(h,)),(h,'p02HostInventory',()),(h,'p03HostUIItem',(63,0))]:
    owner.call(method,*args)
    self.assertEqual([h.arrays['uiItems'].count(x) for x in (39,75,76)],[1,1,1])
    self.assertEqual(h.vm.objects['p06State'].call('h6PhysicalValid'),1)
   self.assertEqual(s.call('h8Owns',22),0);self.assertEqual(p.p['p03Towel'],1)
 def test_real_early_plan_reservations_remain_valid(self):
  import campaign_route
  class Stop(Exception):pass
  original_stage=campaign_route.stage;original_entry=campaign_route.first_entry
  try:
   for source in (False,True):
    for route in ('bunny','wedge'):
     def enter(h,ignored='bunny'):return original_entry(h,route)
     def stage(h,label):
      if label=='P02':
       p=h.vm.objects['p03State'];q=h.vm.objects['p04State'];s=h.vm.objects['p08State']
       self.assertEqual(p.call('b8Valid'),1);self.assertEqual(q.call('q8Valid'),1)
       self.assertEqual(s.call('h8SaveReady'),1)
       raise Stop()
     campaign_route.first_entry=enter;campaign_route.stage=stage
     with self.assertRaises(Stop):campaign_route.prepared(source)
  finally:campaign_route.first_entry=original_entry;campaign_route.stage=original_stage
 def test_method_template_guard_rejects_prior_discarded_tail(self):
  sys.path.insert(0,str(host.H));from derive import check_method_template
  from source_tools import methods
  valid='(method (example) (return 1))'
  orphan=(host.H/'evidence/orphan-template-fragment.txt').read_text()
  self.assertEqual(set(methods(valid+orphan)),{'example'}) # prior extractor silently discarded invalid text
  with self.assertRaises(RuntimeError):check_method_template(valid+orphan)
  with self.assertRaises(RuntimeError):check_method_template(valid+valid)
  for p in (host.H/'templates').glob('*.sc.in'):check_method_template(p.read_text())

if __name__=='__main__':unittest.main(verbosity=2)
