"""Ordinary input, Graph12 receipts and same-build emitted-VM regression corpus.
Not a native ScummVM launch, audible listening test, or native saved-game proof.
"""
import unittest,copy,json,sys
from host import *
VMS=[]
def make(plan=True):
 h,d,a,p,q,r=setup(plan);h.vm.budget=120000000;VMS.append(h.vm)
 return h,d,a,p,q,r,h.vm.objects['p07State']
def kitchen(h):act(h,0,12);assert h.p['location']==2

def control(h,action,payload):
 h.call('uiBuildFocus');ids=[i for i in range(h.p['uiControlCount']) if h.arrays['uiActions'][i]==action and h.arrays['uiPayloads'][i]==payload]
 assert ids,(action,payload,list(h.arrays['uiPayloads']));h.p['uiFocus']=ids[-1];h.vm.pump([{'type':4,'message':13}]);assert h.p['uiFailure']==0

def keyboard(h,verb,obj,target=0):
 control(h,2,verb);control(h,1,obj)
 if target:control(h,1,target)
 h.vm.pump([{}]*70);assert h.p['motionPhase']==0
 close(h)

def restore(h,state,events=None):
 h.vm.restore(state);h.vm.event_queue=list(events or [{},{}])
 try:h.call('replay')
 except base.EndOfEvents:pass
 finally:h.vm.event_queue=None
 assert h.vm.depth==0

def finish(h,s,stockfirst=False):
 act(h,5,86);act(h,7,89,90);choice(h,227,2)
 if stockfirst:act(h,7,90,92);act(h,7,87,92)
 else:act(h,7,87,92);act(h,7,90,92)
 act(h,7,88,92);act(h,7,94);act(h,7,94);act(h,7,91,92);act(h,3,93)
 assert s.call('p07Projection',0)==3

class HostTests(unittest.TestCase):
 def test_real_recipe_pages_not_titles_look_audio_skip_or_partial(self):
  h,d,a,p,q,r,s=make();kitchen(h)
  act(h,2,86);self.assertEqual(s.call('p07Projection',0),0)
  act(h,7,89,90);choice(h,227,2);self.assertEqual(s.p['h7LastCode'],40)
  h.call('hostActNow',5,86,0);self.assertEqual((h.p['uiDocument'],h.p['uiPageCount']),(932,2))
  self.assertEqual(s.call('p07Projection',0),0)
  # Merely reaching document and audio signals cannot supply Graph12 evidence.
  s.call('p07PresentationSignal',1);s.call('p07PresentationSignal',2);s.call('p07PresentationSignal',3)
  self.assertEqual(s.call('p07Projection',0),0)
  frame(h);self.assertEqual(s.p['h7SeenCount'],1)
  close(h,read=False);self.assertEqual(s.call('p07Projection',0),0)
  h.call('hostActNow',5,86,0);frame(h);h.call('uiTurnPage',1)
  # A page-change intent is insufficient until frame flush.
  self.assertEqual(s.call('p07Projection',0),0)
  frame(h);self.assertEqual(s.call('p07Projection',0),1)
  self.assertEqual(s.p['h7PendingSource'],0)
 def test_overlay_fail_stale_identity_and_repeat_receipts(self):
  h,d,a,p,q,r,s=make();kitchen(h);h.call('hostActNow',5,86,0);frame(h)
  h.call('uiTurnPage',1);saved=h.vm.snapshot()
  for prop,value in [('menuOpen',1),('paused',1),('uiFailure',10),('bridgeFailure',1)]:
   h.vm.restore(saved);h.p[prop]=value;s.call('h7Presented',932,1,d.p['sdGeneration']);self.assertEqual(s.call('p07Projection',0),0)
  h.vm.restore(saved);s.call('h7Presented',932,0,d.p['sdGeneration']);self.assertEqual(s.call('p07Projection',0),0)
  frame(h);words=list(s.arrays['p07Words']);frame(h);self.assertEqual(list(s.arrays['p07Words']),words)
 def test_both_base_stock_orders_exact_one_pot_and_lid(self):
  for order in (False,True):
   h,d,a,p,q,r,s=make();kitchen(h);finish(h,s,order)
   self.assertEqual((s.call('p07Projection',4),s.call('p07Projection',5),s.call('p07Projection',6)),(8,0,1))
   self.assertEqual((s.p['h7Owner'],s.p['h7OwnerRoom'],s.p['h7ReadyEvents']),(1,2,1))
   h.vm.ktrace=[];h.call('drawWorld');draws=[list(args) for name,args in h.vm.ktrace if name=='DrawCel']
   self.assertEqual([x for x in draws if x[0]==234 and x[2]!=10],[[234,0,9,63,65,-1,0]])
   self.assertTrue(any(x[:5]==[233,0,0,68,67] for x in draws));self.assertFalse(any(x[:3]==[233,0,7] for x in draws))
   words=list(s.arrays['p07Words'])
   for verb,obj,target in [(3,93,0),(7,91,92),(7,94,0),(4,92,0)]:act(h,verb,obj,target)
   self.assertEqual(list(s.arrays['p07Words']),words);self.assertEqual(s.p['h7ReadyEvents'],1)
   self.assertTrue(all(not (86<=o<=94) for o in h.arrays['uiItems']))
 def test_rejected_inputs_refill_and_no_consumption(self):
  h,d,a,p,q,r,s=make();kitchen(h)
  for verb,obj,target,code in [(7,88,92,42),(7,90,92,41),(7,91,92,46),(7,94,0,43),(3,93,0,23),(4,87,0,25)]:
   words=list(s.arrays['p07Words']);inv=list(h.arrays['uiItems']);act(h,verb,obj,target)
   self.assertEqual(s.p['h7LastCode'],code);self.assertEqual(list(s.arrays['p07Words']),words);self.assertEqual(list(h.arrays['uiItems']),inv)
  act(h,5,86);act(h,7,89,90);words=list(s.arrays['p07Words']);choice(h,227,1)
  self.assertEqual(s.p['h7LastCode'],39);self.assertEqual(list(s.arrays['p07Words']),words)
  act(h,7,89,90);choice(h,227,2);act(h,7,87,92);act(h,7,90,92);act(h,7,88,92);act(h,7,94)
  words=list(s.arrays['p07Words']);act(h,7,91,92);self.assertEqual(s.p['h7LastCode'],45);self.assertEqual(list(s.arrays['p07Words']),words)
  act(h,7,94);act(h,7,91,92);words=list(s.arrays['p07Words']);act(h,4,92);self.assertEqual(s.p['h7LastCode'],22);self.assertEqual(list(s.arrays['p07Words']),words)
 def test_optional_readings_keyboard_first_second_nouns_and_hints(self):
  h,d,a,p,q,r,s=make();kitchen(h)
  keyboard(h,5,90);keyboard(h,5,91)
  self.assertEqual((s.arrays['p07Words'][69],s.arrays['p07Words'][110],s.call('p07Projection',0)),(1,1,0))
  keyboard(h,5,86);keyboard(h,7,87,92)
  self.assertTrue(s.call('h7LiveNZ',4));self.assertEqual(s.call('p07Projection',0),1)
  keyboard(h,7,89,90);self.assertEqual(h.p['uiChoiceContext'],227)
  control(h,13,0);close(h) # Actual CHOOSE on the first, eight-bowl choice page
  keyboard(h,7,90,92);keyboard(h,7,88,92)
  keyboard(h,7,94);self.assertEqual((s.p['h7LastCode'],s.call('p07Projection',2)),(33,1))
  self.assertEqual(h.p['uiNounA'],0)
  before=list(s.arrays['p07Words']);keyboard(h,7,91,92)
  self.assertEqual(s.p['h7LastCode'],45);self.assertEqual(list(s.arrays['p07Words']),before)
  keyboard(h,7,94);self.assertEqual((s.p['h7LastCode'],s.call('p07Projection',2)),(34,0))
  keyboard(h,7,91,92);keyboard(h,3,93)
  self.assertEqual((s.call('p07Projection',0),s.p['h7ReadyEvents']),(3,1))
  # Actual LOOK AT5 on an ordinary fixture displays its canonical inspection.
  h.call('hostActNow',5,92,0);self.assertEqual(h.p['uiDocument'],966);close(h)
  h.call('hostActNow',5,87,0);self.assertEqual(h.p['uiDocument'],934);close(h)
  h.call('p03PreparationHint');choice(h,228,1);self.assertEqual(s.p['h7HintLevel'],1)
  for _ in range(3):h.call('p03PreparationHint');choice(h,228,1)
  self.assertEqual(s.p['h7HintLevel'],3)
 def test_explicit_bunny_invitation_preserves_actor_and_p05_escort(self):
  h,d,a,p,q,r,s=make();act(h,6,2);self.assertEqual(h.p['uiChoiceContext'],209)
  self.assertIn(3,list(h.arrays['uiChoiceIds'])[:h.p['uiChoiceCount']]);choice(h,209,3)
  self.assertEqual((h.p['location'],r.p['hBunnyRoom'],s.p['h7BunnyInvited']),(2,2,1))
  self.assertTrue(s.call('h7LiveNZ',2));self.assertTrue(r.call('hPhysicalValid'))
  h.vm.ktrace=[];h.call('drawWorld');self.assertEqual(sum(1 for n,x in h.vm.ktrace if n=='DrawCel' and x[0]==219),1)
  act(h,6,2);choice(h,226,4);self.assertEqual((h.p['location'],r.p['hBunnyRoom']),(1,1))
  act(h,6,2);choice(h,209,1);self.assertEqual((h.p['location'],r.p['hBunnyRoom']),(5,5))
  words=list(r.arrays['p05Words']);h.call('uiHostChoice',209,3)
  self.assertEqual((h.p['location'],r.p['hBunnyRoom']),(5,5));self.assertEqual(list(r.arrays['p05Words']),words)
  act(h,6,2);choice(h,209,2);self.assertEqual((h.p['location'],r.p['hBunnyRoom']),(1,1))
  act(h,6,2);choice(h,209,3);self.assertEqual((h.p['location'],r.p['hBunnyRoom']),(2,2))
 def test_exact_comic_and_sincere_slices_no_sibling_leakage(self):
  h,d,a,p,q,r,s=make();act(h,6,2);choice(h,209,3);act(h,7,87,92)
  act(h,6,2);h.call('uiHostChoice',226,2)
  self.assertEqual((h.p['uiDocument'],h.p['uiPageCount']),(971,3))
  seen=[]
  for page in range(3):
   if page:h.call('uiTurnPage',1)
   frame(h);seen.append((d.p['sdEntry'],d.p['sdVoice'],d.p['sdSpeaker']))
  self.assertEqual(seen,[(49,24,2),(50,25,1),(51,26,2)])
  h.call('uiTurnPage',1);self.assertEqual(h.p['uiPage'],2);close(h)
  act(h,6,2);h.call('uiHostChoice',226,3);self.assertEqual((h.p['uiDocument'],h.p['uiPageCount']),(972,2))
  seen=[]
  for page in range(2):
   if page:h.call('uiTurnPage',1)
   frame(h);seen.append((d.p['sdEntry'],d.p['sdVoice'],d.p['sdSpeaker']))
  self.assertEqual(seen,[(52,27,1),(53,28,2)]);self.assertEqual(s.p['h7LastEvent'],0)
  h.call('uiTurnPage',-10);self.assertEqual(h.p['uiPage'],0);self.assertEqual(d.p['sdEntry'],52)
 def test_onion_laugh_only_after_second_unit_once_and_cancelled(self):
  h,d,a,p,q,r,s=make();act(h,6,2);choice(h,209,3);act(h,7,87,92);act(h,6,2);h.call('uiHostChoice',226,2)
  frame(h);self.assertEqual(s.p['h7LaughCount'],0)
  a.p['lastLaughEvent']=7007 # A legitimate older transport occurrence may share the numeric ID
  h.call('uiTurnPage',1);frame(h);frame(h)
  self.assertEqual(s.p['h7LaughCount'],1);self.assertEqual(a.p['lastLaughEvent'],7008)
  h.call('uiTurnPage',1);frame(h);self.assertEqual(a.p['pendingLaugh'],0)
  close(h);act(h,6,2);choice(h,226,3);self.assertEqual(s.p['h7LaughCount'],1)
  act(h,6,2);choice(h,226,2);self.assertEqual(s.p['h7LaughCount'],1)
 def test_travel_retains_single_pot_and_other_inventory(self):
  h,d,a,p,q,r,s=make();kitchen(h);finish(h,s);inv=list(h.arrays['uiItems']);words=list(s.arrays['p07Words'])
  act(h,0,18);self.assertEqual(h.p['location'],1);act(h,0,13);self.assertEqual(h.p['location'],4)
  self.assertEqual(s.call('h7Location',92),2);self.assertEqual(h.call('campaignReachable',92),0)
  h.vm.ktrace=[];h.call('drawWorld');self.assertFalse(any(n=='DrawCel' and x[0] in (233,234) for n,x in h.vm.ktrace))
  self.assertEqual(list(s.arrays['p07Words']),words);self.assertEqual(list(h.arrays['uiItems']),inv)
 def test_save_restore_partial_ready_alias_and_no_stale_callbacks(self):
  h,d,a,p,q,r,s=make();kitchen(h);h.call('hostActNow',5,86,0);frame(h)
  old=list(s.arrays['h7TicketSession']);saved=h.vm.snapshot();restore(h,saved)
  self.assertEqual((s.p['h7RestoreValid'],s.call('p07Projection',0)),(1,0));self.assertNotEqual(list(s.arrays['h7TicketSession']),old)
  hi,lo=s.p['h7TicketHi'],s.p['h7TicketLo'];s.call('p07SetInput',1,hi,lo,*old);s.call('p07PageBegin')
  for i in range(16):s.call('p07PageWord',i,s.call('p07Digest',1,i))
  self.assertEqual(s.call('p07AcknowledgePage',1,4,0,1),16);self.assertEqual(s.call('p07Projection',0),0)
  h.call('uiTurnPage',1);frame(h);self.assertEqual(s.call('p07Projection',0),1);close(h);finish(h,s)
  saved=h.vm.snapshot();restore(h,saved);self.assertEqual((s.p['h7RestoreValid'],s.call('p07Projection',0),s.p['h7ReadyEvents']),(1,3,1))
  # Same-build identity excludes cross-build imported state.
  bad=copy.deepcopy(saved);bad['program']['988'][0]='0'*64
  with self.assertRaises(base.VMError):h.vm.restore(bad)
 def test_invalid_restored_payload_context_owner_inventory_rejected(self):
  h,d,a,p,q,r,s=make();kitchen(h);saved=h.vm.snapshot();at=next(x['word_offset'] for x in h.vm.abi['modules']['988']['locals'] if x['name']=='p07Words')
  bads=[]
  bad=copy.deepcopy(saved);bad['locals']['988'][at+18]=1;bads.append(bad)
  bad=copy.deepcopy(saved);bad['objects']['p07State']['h7Owner']=2;bads.append(bad)
  bad=copy.deepcopy(saved);bad['objects']['p05State']['hBunnyRoom']=2;bads.append(bad)
  bad=copy.deepcopy(saved);bad['objects']['p07State']['h7HintLevel']=4;bads.append(bad)
  bad=copy.deepcopy(saved);bad['objects']['p07State']['h7BunnyHome']=3;bads.append(bad)
  bad=copy.deepcopy(saved);bad['objects']['p07State']['h7BunnyInvited']=1;bads.append(bad)
  seen=next(x['word_offset'] for x in h.vm.abi['modules']['988']['locals'] if x['name']=='h7Seen')
  bad=copy.deepcopy(saved);bad['locals']['988'][seen]=1;bads.append(bad)
  for bad in bads:
   restore(h,bad);self.assertEqual(s.p['h7RestoreValid'],0);self.assertEqual(h.p['uiFailure'],10)
  restore(h,saved);self.assertEqual((s.p['h7RestoreValid'],h.p['uiFailure']),(1,0))
 def test_source_and_emitted_ordinary_cooking_parity(self):
  import host as module
  from source_host import VM as SourceVM
  original=module.VM;results=[]
  try:
   for engine in [original,SourceVM]:
    module.VM=engine;h,d,a,p,q,r,s=make();kitchen(h)
    h.call('hostActNow',5,86,0);frame(h);self.assertEqual(s.call('p07Projection',0),0)
    h.call('uiTurnPage',1);frame(h);close(h)
    act(h,7,88,92);self.assertEqual(s.p['h7LastCode'],42)
    finish(h,s,True)
    results.append(dict(words=list(s.arrays['p07Words']),ownership=[s.p['h7Owner'],s.p['h7OwnerRoom']],items=list(h.arrays['uiItems']),ready=s.p['h7ReadyEvents']))
   self.assertEqual(results[0],results[1])
  finally:module.VM=original
 def test_historical_stove_ui_negative_oracle(self):
  import host as runtime
  root=runtime.H
  try:
   runtime.H=H/'inputs/pre-review';h,d,a,p,q,r=runtime.setup();h.vm.budget=120000000;VMS.append(h.vm);s=h.vm.objects['p07State']
   kitchen(h);act(h,5,86);act(h,7,87,92);act(h,7,89,90);choice(h,227,2);act(h,7,90,92);act(h,7,88,92)
   words=list(s.arrays['p07Words']);control(h,2,7);control(h,1,94);h.vm.pump([{}]*70)
   self.assertEqual(h.p['uiNounA'],94);self.assertEqual(list(s.arrays['p07Words']),words)
   control(h,1,94);h.vm.pump([{}]*70);close(h)
   self.assertEqual(s.call('h7LiveNZ',12),0)
  finally:runtime.H=root
 def test_atomic_output_reservation_failure_aborts_candidate(self):
  h,d,a,p,q,r,s=make();kitchen(h);act(h,5,86);act(h,7,89,90);choice(h,227,2)
  act(h,7,87,92);act(h,7,90,92);act(h,7,88,92);act(h,7,94);act(h,7,94);act(h,7,91,92)
  words=list(s.arrays['p07Words']);calls=[]
  def inject(obj,name,args,result):
   if obj is s and name=='p07Perform' and args==[9,0]:
    calls.append(result);h.p['bridgeQueueCount']=32
  h.vm.after_actual_call=inject
  h.call('hostActNow',3,93,0);h.vm.after_actual_call=None
  self.assertEqual(calls,[36]);self.assertEqual(list(s.arrays['p07Words']),words)
  self.assertEqual((s.p['p07Busy'],s.p['h7ReadyEvents'],s.call('p07Projection',3)),(0,0,0))
  h.p['bridgeQueueCount']=h.p['bridgeQueueIndex']=0
  act(h,3,93);self.assertEqual((s.p['h7ReadyEvents'],s.call('p07Projection',0)),(1,3))
 def test_all_canonical_routes_alias_static_guards_and_closed_lid_hit(self):
  h,d,a,p,q,r,s=make();self.assertTrue(s.call('h7RoutesReady'))
  for doc in range(1,971):
   old=int(d.arrays['sdCounts'][doc]);self.assertEqual(d.call('sdPageCount',doc),old)
  kitchen(h);finish(h,s);h.call('uiBuildFocus');idx=h.call('uiHit',75,68)
  self.assertEqual(h.arrays['uiPayloads'][idx],93)
  saved=h.vm.snapshot();restore(h,saved);self.assertTrue(s.p['h7RestoreValid'])
  d.arrays['sdPageData'][1062*8]+=1;self.assertEqual(s.call('h7ReservePages',972),0)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(HostTests))
 report={'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':[(str(t),v) for t,v in result.failures],'errors':[(str(t),v) for t,v in result.errors],'instructions':sum(v.steps for v in VMS),'native_acceptance':False}
 (H/'evidence/p07-host-tests.json').write_text(json.dumps(report,indent=2)+'\n')
 raise SystemExit(not result.wasSuccessful())
