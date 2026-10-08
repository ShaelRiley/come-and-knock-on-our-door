"""Bounded ordinary UI/focus and transactional output gate, source + emitted.
All preparations are real prior campaign histories; no gameplay model is copied.
Native pixels, device I/O, listening, meeting and source ACKs remain out of scope.
"""
import unittest,copy,json
import host
from host import close,frame,act,base
from test_transactions import make,logical,Transactions
from test_practical import input_action,arrive,enter_control
from test_restore import Backend,load
from campaign_route import living

NATIVE=[34,63,81,120,40]
LABELS=['Hatch-side buffet position','Inward-facing speaker position','Display alcove','Gate-to-house lane','Small serving table','Kitchen hatch','Courtyard plan overlay']

def controls(h):
 h.call('uiBuildFocus')
 return [(h.arrays['uiActions'][i],h.arrays['uiPayloads'][i]) for i in range(h.p['uiControlCount'])]

def menu_pick(h,value):
 # Real paged keyboard focus route, including NEXT and ENTER. IDs are generation-bound.
 index=next(i for i in range(h.p['uiChoiceCount']) if h.arrays['uiChoiceIds'][i]%8==value)
 while h.p['uiPage']<index:enter_control(h,11)
 while h.p['uiPage']>index:enter_control(h,10)
 enter_control(h,13,index)

def place(h,obj,pos,verb=7,read=True):
 close(h);input_action(h,verb,obj,115+pos);arrive(h)
 if read:close(h)

def overlay(h,obj,operation=1,value=None):
 close(h);enter_control(h,1,122)
 assert h.p['uiChoiceContext']==230
 menu_pick(h,NATIVE.index(obj)+1)
 assert h.p['uiChoiceContext']==233
 menu_pick(h,operation)
 if value is not None:menu_pick(h,value);arrive(h)

def history_only(h):
 # Ordinary restore refreshes these derived contexts/result caches. Every saved
 # puzzle/history property and all later domain words still compare exactly.
 state=logical(h)
 for branch in ('p03','p04'):
  for suffix in ('ContextValid','Room','Apron','Plan','Tools','Code','LineCount','EventCount','ResultHi','ResultLo'):
   state[branch].pop(branch+suffix,None)
 return state

class LayoutControls(unittest.TestCase):
 def test_01_named_positions_piles_overlap_and_lower_object(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=make(source);old=logical(h)
   self.assertEqual([base.read_string(s.call('h8LayoutLabel',n)) for n in range(116,123)],LABELS)
   self.assertTrue(all((1,n) in controls(h) for n in NATIVE+[116,117,118,119,121,122,71,18,19,9]))
   for n in NATIVE:place(h,n,4,8 if n==120 else 7)
   self.assertEqual(list(s.arrays['p08Words'][:5]),[4]*5)
   self.assertEqual(logical(h),old)
   # One overlapping point includes the lower table; topmost sprite must not win.
   mask=s.call('h8LayoutHit',192,120);self.assertTrue(mask & 8);self.assertGreater(mask.bit_count(),1)
   enter_control(h,2,9)
   h.vm.pump([{'type':1,'x':192,'y':120}])
   self.assertEqual((h.p['uiPanel'],h.p['uiChoiceContext']),(2,234))
   self.assertEqual({h.arrays['uiChoiceIds'][i]%8 for i in range(h.p['uiChoiceCount'])},{i+1 for i in range(5) if mask&(1<<i)})
   menu_pick(h,4);self.assertEqual(h.p['uiNounA'],120)
   enter_control(h,1,116);arrive(h)
   self.assertEqual(s.arrays['p08Words'][3],1)
   self.assertEqual(s.arrays['h8CommittedOutput'][4],26) # canonical PULL success
   close(h);self.assertEqual(logical(h),old)
   # Named overlay still exposes every object after severe occlusion.
   overlay(h,81,1,3);close(h)
   self.assertEqual(s.arrays['p08Words'][2],3)
   self.assertEqual(logical(h),old)

 def test_02_both_table_directions_and_independent_pa_facing(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=make(source);old=logical(h)
   place(h,120,1,8,False);self.assertEqual(s.arrays['h8CommittedOutput'][4],25);close(h)
   place(h,120,3,9);place(h,120,1,9,False)
   self.assertEqual(s.arrays['h8CommittedOutput'][4],26);close(h)
   place(h,63,2);position=s.arrays['p08Words'][1]
   overlay(h,63,5,2);self.assertEqual((s.arrays['p08Words'][1],s.arrays['p08Words'][5]),(position,2));close(h)
   self.assertEqual(s.call('h8LayoutCel',1),3)
   overlay(h,63,5,1);close(h)
   self.assertEqual((s.arrays['p08Words'][1],s.arrays['p08Words'][5]),(position,1))
   self.assertEqual(logical(h),old)
   self.assertEqual((r.p['hPAOwner'],r.p['hPARoom'],r.p['hCartOwner'],r.p['hCartRoom']),(2,4,1,5))
   # The original equipment credit remains a separate real reader after transfer.
   retained=(s.p['h8CommittedCount'],list(s.arrays['h8CommittedOutput']))
   input_action(h,5,71);arrive(h)
   self.assertEqual((h.p['uiPanel'],h.p['uiDocument']),(4,462));close(h)
   self.assertEqual((s.p['h8CommittedCount'],list(s.arrays['h8CommittedOutput'])),retained)
   self.assertEqual(logical(h),old)

 def test_03_exact_output_append_capacity_rollback_and_uncertainty(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=make(source);d=h.vm.objects['sceneDialogue']
   input_action(h,5,121);arrive(h)
   self.assertEqual((h.p['uiPanel'],h.p['uiDocument']),(4,985))
   old_document=h.p['uiDocument'];old_generation=d.p['sdGeneration'];prefix=list(h.arrays['bridgeQueue'][:h.p['bridgeQueueCount']])
   self.assertEqual(s.call('h8UIRun',1,1,1),1)
   self.assertEqual((h.p['uiDocument'],d.p['sdGeneration']),(old_document,old_generation))
   self.assertEqual(list(h.arrays['bridgeQueue'][:len(prefix)]),prefix)
   self.assertEqual(h.arrays['bridgeQueue'][len(prefix)],991)
   while h.p['bridgeQueueCount']<32:h.call('h7PublishNative',1,985,0)
   words=list(s.arrays['p08Words']);owners=list(s.arrays['h8OwnerReceipts']);out=list(s.arrays['h8CommittedOutput']);queue=list(h.arrays['bridgeQueue']);kinds=list(d.arrays['sdQueueKinds']);old=logical(h)
   self.assertEqual(s.call('h8UIRun',1,2,2),0)
   self.assertEqual(list(s.arrays['p08Words']),words);self.assertEqual(list(s.arrays['h8OwnerReceipts']),owners)
   self.assertEqual(list(s.arrays['h8CommittedOutput']),out);self.assertEqual(list(h.arrays['bridgeQueue']),queue)
   self.assertEqual(list(d.arrays['sdQueueKinds']),kinds);self.assertEqual(logical(h),old)
   self.assertEqual((h.p['uiDocument'],d.p['sdGeneration']),(old_document,old_generation))
   # Ordinary close drains the actual reader. Empty storage may then be reused.
   close(h,False);self.assertEqual(h.p['bridgeQueueIndex'],32)
   self.assertEqual(s.call('h8UIRun',1,2,2),1);self.assertEqual(h.p['bridgeQueueCount'],1);close(h)
   def fault(obj,name,args,result):
    if obj.name=='cakood' and name=='h7PublishNative' and not getattr(h.vm,'layout_fault',False):
     h.vm.layout_fault=True;h.arrays['bridgeQueue'][h.p['bridgeQueueCount']-1]=999
   h.vm.after_actual_call=fault
   self.assertEqual(s.call('h8UIRun',1,3,3),0)
   self.assertEqual((s.p['h8Failure'],s.p['h8Enabled'],s.p['h8RestoreValid']),(20,0,0))
   frozen=list(s.arrays['p08Words']);h.call('hostActNow',0,18,0)
   self.assertEqual(h.p['location'],4);self.assertEqual(list(s.arrays['p08Words']),frozen)
   # A changed publication count cannot consume slots that were not reserved.
   h,p,q,r,t,u,v,s=make(source);queue=list(h.arrays['bridgeQueue']);count=h.p['bridgeQueueCount']
   def count_fault(obj,name,args,result):
    if obj.name=='p08State' and name=='h8CommitReserved' and result:s.p['h8CommittedCount']=3
   h.vm.after_actual_call=count_fault
   self.assertEqual(s.call('h8UIRun',1,1,1),0)
   self.assertEqual(s.p['h8Failure'],20)
   self.assertEqual(list(h.arrays['bridgeQueue']),queue);self.assertEqual(h.p['bridgeQueueCount'],count)

 def test_04_cancel_stale_repeated_travel_and_ordinary_restore(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=make(source);before=list(s.arrays['p08Words'])
   overlay(h,120,1)
   self.assertEqual(h.p['uiChoiceContext'],231);token=h.arrays['uiChoiceIds'][0]
   h.vm.pump([{'type':4,'message':27}]);self.assertEqual(s.arrays['h8UI'][1],0)
   h.call('uiHostChoice',231,token);self.assertEqual(list(s.arrays['p08Words']),before)
   overlay(h,120,1);newtoken=h.arrays['uiChoiceIds'][0];self.assertNotEqual(newtoken,token)
   h.call('uiHostChoice',231,token);self.assertEqual(list(s.arrays['p08Words']),before)
   backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved)
   saved=copy.deepcopy(backend.saved)
   menu_pick(h,1);arrive(h);close(h);self.assertEqual(s.arrays['p08Words'][3],1)
   h.call('uiHostChoice',231,newtoken);self.assertEqual(s.arrays['p08Words'][3],1)
   load(h,backend,saved,events=[{'type':4,'message':13},{'type':1,'x':200,'y':170},{},{}])
   self.assertEqual((s.p['h8RestoreValid'],h.p['uiPanel'],s.arrays['h8UI'][1]),(1,0,0))
   self.assertEqual(list(s.arrays['p08Words']),before)
   h.call('uiHostChoice',231,newtoken);self.assertEqual(list(s.arrays['p08Words']),before)
   # A canonical P08 reader and its queued record survive ordinary save/load.
   input_action(h,5,121);arrive(h);frame(h)
   h.call('writeSave');reader=copy.deepcopy(backend.saved)
   reader_identity=(h.p['uiDocument'],h.p['uiPage'],h.p['bridgeQueueCount'],h.p['bridgeQueueIndex'])
   close(h);place(h,120,4,8)
   load(h,backend,reader)
   self.assertEqual((h.p['uiDocument'],h.p['uiPage'],h.p['bridgeQueueCount'],h.p['bridgeQueueIndex']),reader_identity)
   self.assertEqual(list(s.arrays['p08Words']),before);close(h)
   overlay(h,120,1);traveltoken=h.arrays['uiChoiceIds'][0]
   h.call('hostActNow',0,18,0);close(h)
   self.assertEqual(h.p['location'],1);self.assertEqual(s.arrays['h8UI'][1],0);self.assertEqual(h.p['uiPanel'],0)
   self.assertEqual([h.call('p02ObjectLocation',n) for n in range(116,123)],[4]*7)
   h.call('uiHostChoice',231,traveltoken);self.assertEqual(list(s.arrays['p08Words']),before)

 def test_05_original_cloth_and_two_record_unpack_publication(self):
  for source in (False,True):
   for cloth,padding in ((39,1),(38,2)):
    h,p,q,r,t,u,v,s=make(source,cloth);old=logical(h)
    place(h,34,1);place(h,120,1,8)
    input_action(h,2,34);arrive(h)
    self.assertEqual((s.arrays['p08Words'][6],s.arrays['p08Words'][7],s.p['h8PaddingPlace']),(1,padding,1))
    self.assertEqual(list(s.arrays['h8CommittedOutput'][4:6]),[20,20+padding])
    self.assertEqual(list(h.arrays['bridgeQueue'][:2]),[992,992+padding]);close(h)
    self.assertEqual(logical(h),old)
    living(h);act(h,0,12);input_action(h,4,cloth);arrive(h);close(h)
    self.assertEqual(s.call('h8ClothHeld',cloth),1)
    living(h);act(h,0,13);place(h,120,4,9);place(h,120,1,8)
    self.assertEqual(s.call('h8ClothHeld',cloth),1)
    self.assertEqual((p.p['p03Padding'],p.p['p03Ready'],p.call('p03Validate')),(padding,1,1))
    self.assertEqual((u.p['h7OwnerRoom'],r.p['hCartRoom']),(2,5))

 def test_06_original_plan_and_token_lifecycle(self):
  Transactions.test_native_completed_screen_and_courtyard_plan_keep_distinct_routes(self)

 def test_07_render_hatch_no_observations_and_full_program_budget(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=make(source);before=list(s.arrays['p08Words']);old=logical(h)
   h.vm.ktrace=[];h.call('drawWorld')
   cels=[a for n,a in h.vm.ktrace if n=='DrawCel']
   self.assertEqual(sum(a[0]==305 for a in cels),1)
   self.assertTrue(any(a[0]==227 and a[2]==8 for a in cels))
   self.assertEqual(h.call('p02Exit',121),-1)
   for action in (0,2,5):
    h.call('hostActNow',action,121,0);close(h)
    self.assertEqual(h.p['location'],4)
   self.assertEqual(list(s.arrays['p08Words']),before);self.assertEqual(logical(h),old)
   for n in ('p08Introduce','p08AcknowledgeSource','p08RequestStart','p08AcknowledgeChecklist','p08ConfirmStart','p08AcknowledgeAutosave'):
    self.assertEqual(h.vm.calls[989,n],0,n)
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))
  Transactions.test_domain_methods_selectors_and_compiler_budget_preserved(self)
  receipt=json.loads((host.H/'build/coherent/compile-receipt.json').read_text())
  self.assertLessEqual(next(m['combined_bytes'] for m in receipt['modules'] if m['module']==0)-63380,650)

 def test_08_obscured_callbacks_focus_and_generation_recovery(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=make(source);old=history_only(h)
   # Actual Tab events visit the shared keyboard/controller focus roster.
   seen=set();controls(h)
   for _ in range(h.p['uiControlCount']+1):
    i=h.p['uiFocus'];seen.add((h.arrays['uiActions'][i],h.arrays['uiPayloads'][i]))
    h.vm.pump([{'type':4,'message':9}])
   self.assertTrue(all((1,n) in seen for n in NATIVE+[116,117,118,119,121,122]))
   overlay(h,120,1);token=h.arrays['uiChoiceIds'][0]
   before=(list(s.arrays['p08Words']),list(s.arrays['h8OwnerReceipts']),list(s.arrays['h8CommittedOutput']),list(h.arrays['bridgeQueue']),h.p['bridgeQueueCount'])
   for flag in ('paused','menuOpen','opening'):
    h.p[flag]=1
    h.call('uiHostChoice',231,token)
    self.assertEqual(s.call('h8UIRun',1,4,1),0)
    self.assertEqual((list(s.arrays['p08Words']),list(s.arrays['h8OwnerReceipts']),list(s.arrays['h8CommittedOutput']),list(h.arrays['bridgeQueue']),h.p['bridgeQueueCount']),before)
    self.assertEqual((h.p['uiPanel'],s.arrays['h8UI'][1]),(2,231))
    self.assertEqual(s.call('h8LayoutActive'),1)
    h.p[flag]=0
   h.call('uiClose')
   # Bounded counter fixture, not a fabricated puzzle or ownership history.
   s.arrays['h8UI'][0]=4095
   self.assertEqual(s.call('h8LayoutMenu',230,0,7),0)
   place(h,120,4,8);self.assertEqual(s.arrays['p08Words'][3],4)
   backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved)
   load(h,backend,events=[{'type':4,'message':13},{'type':1,'x':200,'y':170},{},{}])
   self.assertEqual(s.arrays['h8UI'][0],0)
   overlay(h,120,3,1);close(h)
   self.assertEqual(s.arrays['p08Words'][3],1)
   self.assertEqual(history_only(h),old)

if __name__=='__main__':unittest.main(verbosity=2)
