"""Gate2a: genuine whole-prior-campaign histories; bounded direct host transactions.
No P08 player menu/dispatch, whole-campaign P08 restore or native acceptance claim.
"""
import copy,json,unittest,sys
from pathlib import Path
import host
from source_host import VM as SourceVM
from campaign_route import prepared
from host import act,choice,close
H=host.H;EMITTED=host.VM;CACHE={}

def make(source=False,cloth=39):
 key=(source,cloth)
 if key not in CACHE:
  values=prepared(source,cloth);CACHE[key]=values[0].vm.snapshot();return values
 vm=SourceVM() if source else EMITTED();vm.budget=900000000
 vm.restore(copy.deepcopy(CACHE[key]))
 return tuple(vm.objects[n] for n in ('cakood','p03State','p04State','p05State','p06State','p07State','contestState','p08State'))

def logical(h):
 vm=h.vm
 return dict(p03={k:v for k,v in vm.objects['p03State'].p.items() if k.startswith('p03')},p04={k:v for k,v in vm.objects['p04State'].p.items() if k.startswith('p04')},p05=list(vm.arrays(985)['p05Words']),p06=list(vm.arrays(987)['p06Words']),p07=list(vm.arrays(988)['p07Words']),vc=list(vm.arrays(986)['vcWords']),inventory=list(h.arrays['uiItems']))

def layout(s):
 for obj,pos in ((3,4),(5,4),(1,4),(2,4),(4,4)):
  assert s.call('h8RunLayout',1,obj,pos)==1,(obj,s.p['h8LastCode'],s.p['h8Failure'])
 for obj,pos in ((1,1),(2,2),(3,3),(4,1),(5,1)):
  assert s.call('h8RunLayout',1,obj,pos)==1,(obj,s.p['h8LastCode'],s.p['h8Failure'])
 assert s.call('h8RunLayout',4,0,0)==1

class Transactions(unittest.TestCase):
 def test_real_campaign_loss_loss_preparation_and_actor_mapping(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=make(source)
   self.assertEqual(s.call('h8Preparations'),8191);self.assertEqual(v.call('vcFlags'),3)
   self.assertEqual(s.call('h8Context'),1);self.assertEqual(s.p['p08Wins'],0)
   self.assertEqual([s.call('h8ToDomain',i) for i in range(7)],[3,1,2,4,5,6,7])
   self.assertEqual(s.p['p08FrankieRoom'],s.call('h8ToDomain',t.p['h6FrankieRoom']))
   self.assertEqual(s.p['p08BunnyRoom'],s.call('h8ToDomain',r.p['hBunnyRoom']))
   self.assertNotEqual((s.p['p08FrankieRoom'],s.p['p08BunnyRoom']),(5,5))
   self.assertEqual(s.call('p08RequestStart'),16) # actual unreachable Frankie; no fabricated position
 def test_atomic_owners_order_moves_and_both_original_padding_variants(self):
  for source in (False,True):
   for cloth,padding in ((39,1),(38,2)):
    h,p,q,r,t,u,v,s=make(source,cloth);before=logical(h)
    layout(s)
    self.assertEqual(list(s.arrays['p08Words'][83:88]),[3,5,1,2,22])
    self.assertEqual(s.call('p08PendingKey',0),0)
    self.assertEqual((r.p['hPAOwner'],r.p['hPARoom'],r.p['hCartOwner'],r.p['hCartRoom']),(2,4,1,5))
    self.assertEqual((t.p['h6ScreenOwner'],t.p['h6ScreenRoom'],t.p['h6ScreenPosition']),(2,4,3))
    self.assertEqual(s.call('h8OwnersValid'),1);self.assertEqual(r.call('hPhysicalValid'),1);self.assertEqual(t.call('h6OwnersValid'),1)
    self.assertEqual((p.p['p03Padding'],s.arrays['p08Words'][7],s.p['h8PaddingPlace']),(padding,padding,1))
    self.assertEqual(s.call('h8OriginalCloth'),cloth);self.assertEqual(s.call('h8PhysicalOwner',cloth),8)
    self.assertEqual(logical(h),before)
    receipts=list(s.arrays['h8OwnerReceipts']);order=list(s.arrays['p08Words'][83:88]);state=list(s.arrays['p08Words'])
    self.assertEqual(s.call('h8RunLayout',4,0,0),1);self.assertEqual(list(s.arrays['p08Words']),state)
    self.assertEqual(s.call('h8RunLayout',3,0,2),1);self.assertEqual(s.call('h8RunLayout',3,0,1),1)
    self.assertEqual(s.call('h8RunLayout',2,3,4),1);self.assertEqual(t.p['h6ScreenPosition'],4)
    self.assertEqual(list(s.arrays['h8OwnerReceipts']),receipts);self.assertEqual(list(s.arrays['p08Words'][83:88]),order)
    self.assertEqual(logical(h),before)
    # Progressed P08 ordinary save is now admitted; kernel outcomes have their own restore cases.
    self.assertEqual(s.call('h8SaveReady'),1)
 def test_output_reservation_failure_aborts_without_publication(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=make(source);before=list(s.arrays['p08Words']);owners=list(s.arrays['h8OwnerReceipts']);old=logical(h)
   for count in (32,32767):
    h.p['bridgeQueueCount']=count
    self.assertEqual(s.call('h8RunLayout',1,1,1),0)
   self.assertEqual(list(s.arrays['p08Words']),before);self.assertEqual(list(s.arrays['h8OwnerReceipts']),owners)
   self.assertEqual(s.p['p08Busy'],0);self.assertEqual(logical(h),old)
   h.p['bridgeQueueCount']=0
   dialogue=h.vm.objects['sceneDialogue'];first=dialogue.arrays['sdStarts'][991]
   dialogue.arrays['sdStarts'][991]=32767
   self.assertEqual(s.call('h8RunLayout',1,1,1),0)
   self.assertEqual(list(s.arrays['p08Words']),before)
   self.assertEqual(r.p['hFailure'],40) # immutable route corruption locks its owning source
   dialogue.arrays['sdStarts'][991]=first
   self.assertEqual(s.call('h8RunLayout',1,1,1),0) # editing corrupt bytes is not recovery
   # A fresh whole-campaign harness snapshot is separate from pending native restore work.
   h,p,q,r,t,u,v,s=make(source)
   self.assertEqual(s.call('h8RunLayout',1,1,1),1);self.assertEqual(s.call('h8Owns',1),1)
 def test_ack_serial_storage_reserved_before_first_commit(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=make(source);old=logical(h)
   # Explicit near-exhaustion domain fixture; all preparation evidence remains genuine.
   s.arrays['p08Words'][12]=-1;s.arrays['p08Words'][13]=-2
   before=list(s.arrays['p08Words'])
   self.assertEqual(s.call('h8RunLayout',1,1,1),0)
   self.assertEqual(list(s.arrays['p08Words']),before);self.assertEqual(s.p['p08Busy'],0)
   self.assertEqual(list(s.arrays['h8OwnerCodes']),[3,5,6,3,3]);self.assertEqual(logical(h),old)
 def test_reentry_and_uncertain_publication_lock_campaign_actions(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=make(source);before=logical(h);s.p['h8Critical']=1
   for method,args in [('hostActNow',(0,18,0)),('uiHostAct',(0,18,0)),('bridgeActAtArrival',(0,18,0)),('uiHostChoice',(204,1)),('uiHostConfirm',(201,)),('writeSave',()),('readSave',()),('p03PreparationHint',()),('p02Hint',(1,)),('p02Journal',()),('dialoguePresented',()),('uiClose',()),('speechPoll',())]:h.call(method,*args)
   self.assertEqual(logical(h),before);self.assertEqual(h.p['location'],4)
   self.assertEqual(h.vm.kernel_attempts['SaveGame'],0);self.assertEqual(h.vm.kernel_attempts['RestoreGame'],0)
   s.p['h8Critical']=0
   def fault(obj,name,args,result):
    if obj.name=='p08State' and name=='p08Commit' and result and not getattr(h.vm,'injected',False):
     h.vm.injected=True;s.arrays['h8TransferKeys'][0]=5
   h.vm.after_actual_call=fault
   self.assertEqual(s.call('h8RunLayout',1,1,1),0)
   self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.p['h8Enabled']),(20,0,0))
   self.assertEqual(s.call('h8RunLayout',1,2,2),0)
   h.call('hostActNow',0,18,0);h.call('writeSave')
   self.assertEqual(h.p['location'],4);self.assertEqual(h.vm.kernel_attempts['SaveGame'],0)
 def test_domain_methods_selectors_and_compiler_budget_preserved(self):
  from source_tools import methods
  old=methods((H/'inputs/domain/module989.sc').read_text());new=methods((H/'src/module989.sc').read_text())
  self.assertTrue(all(new[k]==v for k,v in old.items()))
  selectors=json.loads((H/'selectors.json').read_text())
  for source in ('inputs/base/selectors.json','inputs/domain/selectors.json'):
   self.assertTrue(all(selectors[k]==v for k,v in json.loads((H/source).read_text()).items()))
  receipt=json.loads((H/'build/coherent/compile-receipt.json').read_text())
  self.assertEqual(receipt['class_owners'],[0,0,980,981,982,983,984,985,986,987,988,989])
  self.assertTrue(all(r['combined_bytes']<=65535 for r in receipt['modules']))
  self.assertFalse((H/'snapshot/resources/243.text.bin').exists())
 def test_native_completed_screen_and_courtyard_plan_keep_distinct_routes(self):
  from campaign_route import living
  from test_practical import input_action,arrive
  for source in (False,True):
   h,p,q,r,t,u,v,s=make(source)
   identities=json.loads((H/'HOST-NATIVE-IDS.json').read_text())['objects']
   for row in identities:
    provider=h if row['provider']=='p03Label' else r if row['provider']=='hLabel' else t
    self.assertEqual(host.base.read_string(provider.call(row['provider'],row['native'])),row['label'])
    self.assertEqual(s.call('h8PhysicalOwner',row['native']),row['prior_p08_adapter_owner'])
   self.assertEqual(host.base.read_string(t.call('h6Label',81)),'COMPLETED SCREEN')
   self.assertEqual(host.base.read_string(t.call('h6Label',83)),'COURTYARD PLAN')
   self.assertEqual(s.call('h8PhysicalOwner',81),6);self.assertEqual(s.call('h8PhysicalOwner',83),0)
   layout(s)
   for row in identities:
    self.assertEqual(s.call('h8PhysicalOwner',row['native']),row['after_towel_layout_owner'])
    self.assertEqual(s.call('h8OwnedNative',row['native']),int(row['after_towel_layout_owner']==8))
   self.assertEqual(s.call('h8PhysicalOwner',81),8)
   self.assertEqual(s.call('h8OwnedNative',81),1);self.assertEqual(s.call('h8OwnedNative',83),0)
   self.assertEqual(h.call('p02ObjectLocation',81),4);self.assertEqual(h.call('p02ObjectLocation',83),0)
   self.assertEqual(s.call('h8Dispatch',5,83,0),0)
   words=list(s.arrays['p08Words']);old=list(t.arrays['p06Words'])
   living(h);act(h,0,17);self.assertEqual(h.p['location'],0)
   input_action(h,5,83);arrive(h)
   self.assertEqual((h.p['uiPanel'],h.p['uiDocument']),(4,t.call('h6Document',36)))
   self.assertEqual(list(s.arrays['p08Words']),words)
   now=list(t.arrays['p06Words'])
   # The genuine plan read may newly observe source5. Keep every older construction,
   # scope and loan fact exact while allowing its real revision/source receipts.
   self.assertEqual(now[2:83],old[2:83]);self.assertEqual(now[87:],old[87:])
   self.assertTrue(any(now[83:85]) and any(now[85:87]))
   self.assertEqual((t.p['h6ScreenOwner'],t.p['h6ScreenRoom'],t.p['h6ScreenPosition']),(2,4,3))
   close(h)
   self.assertEqual((h.call('p02ObjectLocation',80),h.call('campaignHeld',80)),(0,0))
   for verb,position in ((8,2),(9,1)):
    input_action(h,verb,80);arrive(h)
    self.assertEqual((h.p['uiPanel'],h.p['uiChoiceContext']),(2,222))
    choice(h,222,position)
    self.assertEqual(t.arrays['p06Words'][30],position)
    self.assertEqual(t.call('p06Projection',0),7)
    self.assertEqual((t.p['h6ScreenOwner'],t.p['h6ScreenRoom'],t.p['h6ScreenPosition']),(2,4,3))
    self.assertEqual(list(s.arrays['p08Words']),words)
   self.assertEqual(s.call('h8PhysicalOwner',80),0)

if __name__=='__main__':unittest.main(verbosity=2)
