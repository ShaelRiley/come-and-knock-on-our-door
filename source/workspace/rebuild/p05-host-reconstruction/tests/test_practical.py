import unittest,json,sys,hashlib,copy
from host import *
VMS=[]
def make(*a,**kw):
 t=setup(*a,**kw);VMS.append(t[0].vm);return t

def enter_control(h,action,payload=None,index=0):
 h.call('uiBuildFocus');ids=[i for i in range(h.p['uiControlCount']) if h.arrays['uiActions'][i]==action and (payload is None or h.arrays['uiPayloads'][i]==payload)]
 assert ids,(action,payload);h.p['uiFocus']=ids[index];h.vm.pump([{'type':4,'message':13}]);assert h.p['uiFailure']==0

def input_action(h,v,o,t=0,index=0):
 enter_control(h,2,v);h.call('uiBuildFocus')
 mode=3 if any(h.arrays['uiActions'][i]==3 and h.arrays['uiPayloads'][i]==o for i in range(h.p['uiControlCount'])) else 1
 enter_control(h,mode,o,index=index)
 if t:enter_control(h,1,t,index=index)

def arrive(h):
 h.vm.pump([{}]*70);assert h.p['motionPhase']==0

def restore(h,state,events=None):
 vm=h.vm;vm.restore(state);vm.event_queue=list(events or [{},{}]);
 try:h.call('replay')
 except base.EndOfEvents:pass
 finally:vm.event_queue=None
 assert vm.depth==0
 return h

class Practical(unittest.TestCase):
 def test_before_plan_consistent_garage_explicit_geometry_delta(self):
  h,d,a,p,q,r=make(False);h.p.update(location=5,roomSeen=5)
  h.call('uiBuildFocus')
  controls=[(h.arrays['uiActions'][i],h.arrays['uiPayloads'][i],[h.arrays[x][i] for x in ['uiLefts','uiTops','uiRights','uiBottoms']]) for i in range(h.p['uiControlCount'])]
  self.assertIn((1,27,[46,48,76,79]),controls)
  self.assertTrue(all(any(a==1 and o==obj for a,o,rect in controls) for obj in (17,28)))
  self.assertFalse(any(a==1 and 63<=o<=72 for a,o,rect in controls))
  self.assertEqual((h.call('approachX',27),h.call('approachY',27)),(74,139))
  h.vm.ktrace=[];h.call('drawWorld');views=[a[0] for n,a in h.vm.ktrace if n=='DrawCel']
  self.assertIn(304,views);self.assertIn(229,views);self.assertIn(221,views)
  # Approved additive presentation delta; original P02 logical methods stay exact.
  from source_tools import methods
  old=methods((H/'snapshot/r2/main.sc').read_text());new=methods((H/'src/main.sc').read_text())
  for name in ['p02Act','p02Held','p02Take','p02Init']:
   if name in old:self.assertEqual(new[name],old[name],name)
 def test_before_plan_original_bundle_drawer_master_path_remains_live(self):
  h,d,a,p,q,r=make(False);h.p.update(location=5,roomSeen=5,p02CopyJack=12,p02CopyBunny=12,p02CopyStringer=12,p02Compared=1,p02Observed=31)
  h.call('p02SyncInventory',0);frame(h)
  act(h,1,23,28);self.assertEqual((h.p['p02MiloShown'],h.p['p02DrawerOpen']),(1,1))
  input_action(h,4,24);arrive(h);close(h)
  self.assertEqual(h.p['p02MasterHeld'],1);self.assertEqual(h.arrays['uiItems'].count(24),1)
  self.assertEqual(r.call('p05Flags'),0);self.assertEqual(h.vm.objects['contestState'].call('vcFlags'),0)
 def test_preplan_and_apron_hardware_arguments_fail_closed(self):
  for plan,apron in [(False,0),(True,1)]:
   h,d,a,p,q,r=make(plan);h.p.update(location=5,roomSeen=5,onApron=apron,apronSeen=apron)
   before=list(r.arrays['p05Words']);position=(h.p['location'],h.p['onApron'])
   for obj in range(63,73):
    for verb in range(10):
     h.call('hostActNow',verb,obj,0)
     h.call('hostActNow',7,25,obj)
   self.assertEqual(list(r.arrays['p05Words']),before);self.assertEqual((h.p['location'],h.p['onApron']),position)
   self.assertEqual(r.call('p05Flags'),0);self.assertEqual(h.vm.objects['contestState'].call('vcFlags'),0)
   frame(h)
 def test_real_audience_controls_practical_and_no_contest_loan(self):
  h,d,a,p,q,r=make();frame(h);practical(h,r)
  self.assertEqual((r.call('p05Flags'),r.p['hPAOwner'],r.p['hPARoom'],r.p['hCartRoom']),(3,1,5,5))
  self.assertEqual(h.call('campaignHeld',25),1)
  self.assertEqual(r.call('hLocation',-2),-1) # cable is a domain fixture query, never an inventory ID
  self.assertEqual(r.call('p05Location',-2),5)
  before=list(r.arrays['p05Words']);act(h,6,28);choice(h,211,5)
  self.assertEqual(list(r.arrays['p05Words']),before);self.assertEqual(r.call('p05Flags'),3)
  self.assertEqual(r.p['hLastCode'],68)
  self.assertTrue(any('EVERY WORD' in t for t in h.vm.paint))
  self.assertTrue(any('SOUND EQUIPMENT COURTESY OF MILO PENNANT' in t for t in h.vm.paint))
  self.assertEqual(h.p['uiFailure'],0)
 def test_bunny_canonical_invitation_visible_transition_and_return(self):
  h,d,a,p,q,r=make();act(h,6,2);h.call('uiHostChoice',209,1)
  self.assertEqual((r.p['hBunnyRoom'],h.p['location'],r.p['hEscort']),(1,1,1))
  close(h);self.assertEqual((r.p['hBunnyRoom'],h.p['location'],r.p['hEscort']),(5,5,0))
  self.assertEqual(h.call('dialogueCanSpeak',2),1)
  act(h,0,17);act(h,2,1);act(h,0,1);self.assertEqual(h.p['location'],1)
  h.call('uiBuildFocus');self.assertFalse(any(h.arrays['uiActions'][i]==1 and h.arrays['uiPayloads'][i]==2 for i in range(h.p['uiControlCount'])))
  self.assertEqual(h.call('campaignReachable',2),0);self.assertEqual(h.call('dialogueCanSpeak',2),0)
  garage(h);act(h,6,2);choice(h,209,2)
  self.assertEqual((r.p['hBunnyRoom'],h.p['location']),(1,1));self.assertEqual(r.arrays['p05Words'][69],0)
  h.call('uiBuildFocus');self.assertTrue(any(h.arrays['uiActions'][i]==1 and h.arrays['uiPayloads'][i]==2 for i in range(h.p['uiControlCount'])))
 def test_bunny_equal_soundcheck_route(self):
  h,d,a,p,q,r=make();act(h,6,2);choice(h,209,1)
  for args in ((7,65,66),(7,64)):act(h,*args)
  choice(h,212,1);act(h,8,68);choice(h,213,1);act(h,6,65);choice(h,214,1)
  self.assertEqual(r.call('p05Flags'),1);self.assertEqual(r.call('p05TestedListener'),1)
  self.assertEqual(h.p['uiFailure'],0)
 def test_source_receipt_only_exact_unobscured_graph12(self):
  for source,obj,line in [(1,64,6),(2,66,11)]:
   h,d,a,p,q,r=make();garage(h);h.call('hostActNow',5,obj,0)
   self.assertEqual(r.call('p05Journal',source),0)
   self.assertEqual(h.p['uiDocument'],420+line)
   for prop in ['menuOpen','paused','opening']:
    h.p[prop]=1;h.call('dialoguePresented');self.assertEqual(r.call('p05Journal',source),0);h.p[prop]=0
   gen=d.p['sdGeneration'];r.call('hPresented',420+line,0,gen-1);self.assertEqual(r.call('p05Journal',source),0)
   h.vm.draw_success=False
   with self.assertRaises(base.VMError):frame(h)
   self.assertEqual(r.call('p05Journal',source),0)
   h.vm.draw_success=True;frame(h)
   for pg in range(1,h.p['uiPageCount']):h.call('uiTurnPage',1);frame(h)
   self.assertEqual(r.call('p05Journal',source),line)
   serial=r.arrays['p05Words'][1];frame(h);frame(h);self.assertEqual(r.arrays['p05Words'][1],serial)
   close(h)
 def test_close_travel_replaced_source_never_award(self):
  h,d,a,p,q,r=make();garage(h);h.call('hostActNow',5,64,0);self.assertTrue(r.p['hPendingSource'])
  h.call('uiClose');self.assertEqual(r.call('p05Journal',1),0);self.assertEqual(r.p['hPendingSource'],0)
  h.call('hostActNow',5,66,0);old=(r.p['hTicketHi'],r.p['hTicketLo'],list(r.arrays['hTicketSession']))
  h.call('uiClose');act(h,0,17)
  r.call('p05SetInput',1,*old[:2],*old[2]);r.call('hContext',0);self.assertNotEqual(r.call('p05AcknowledgeSource',2,11),21)
  self.assertEqual(r.call('p05Journal',2),0)
 def test_wrong_socket_direction_and_silent_audience_cards(self):
  h,d,a,p,q,r=make();garage(h);before=list(r.arrays['p05Words']);act(h,7,65,64)
  self.assertEqual(list(r.arrays['p05Words']),before);self.assertEqual(r.p['hLastCode'],38)
  act(h,0,9);act(h,6,10);choice(h,210,1);act(h,0,11);act(h,7,65,66);act(h,7,64);choice(h,212,1)
  act(h,6,65);choice(h,214,2);self.assertEqual(r.call('p05Flags'),0);self.assertTrue(any('UNCLEAR:' in t for t in h.vm.paint))
  for doc in [451,455,459]:
   d.call('sdOpen',doc,0,0,0,a)
   for page in range(d.p['sdCount']):
    d.p['sdPage']=page;d.call('sdLoad')
    if d.p['sdSpeaker']==0:self.assertEqual(d.p['sdVoice'],0)
 def test_full_keyboard_arrival_and_escape_preserve_domain(self):
  h,d,a,p,q,r=make();garage(h);before=list(r.arrays['p05Words'])
  input_action(h,7,65,66)
  self.assertEqual(list(r.arrays['p05Words']),before);self.assertGreater(h.p['motionPhase'],0)
  h.vm.pump([{'type':4,'message':27}]+[{}]*70);self.assertEqual(list(r.arrays['p05Words']),before)
  input_action(h,7,65,66);arrive(h);close(h)
  self.assertEqual(r.arrays['p05Words'][66],1)
  for method in ['uiInput','uiActivate','uiHostAct','motionArrive','bridgeActAtArrival','eventLoop']:
   self.assertGreater(h.vm.calls[0,method],0)
 def test_plan_loss_at_arrival_and_offscreen_protect_hardware(self):
  h,d,a,p,q,r=make();garage(h);before=list(r.arrays['p05Words']);input_action(h,7,65,66);h.p['p02PlanAgreed']=0;arrive(h)
  self.assertEqual(list(r.arrays['p05Words']),before)
  h.p['p02PlanAgreed']=1;act(h,0,17);act(h,7,65,66);self.assertEqual(list(r.arrays['p05Words']),before)
 def test_garage_exit_has_live_keyboard_reachability_and_before_travel_hook(self):
  h,d,a,p,q,r=make();garage(h)
  self.assertEqual(h.call('p02Exit',17),0);self.assertEqual(h.call('campaignReachable',17),1)
  before=h.vm.calls[983,'bBeforeTravel'];h.p['uiVerb']=0;enter_control(h,1,17);arrive(h);close(h)
  self.assertEqual(h.p['location'],0);self.assertGreater(h.vm.calls[983,'bBeforeTravel'],before)
 def test_mark_selection_exact_rect_and_keyboard(self):
  h,d,a,p,q,r=make();garage(h)
  self.assertEqual([r.call('hMarkAt',280,y) for y in [119,120,133,134,143,144]],[0,1,1,2,2,0])
  h.p.update(x=280,y=125,uiLastX=280,uiLastY=125,uiVerb=0);enter_control(h,1,69,index=1)
  self.assertEqual(r.p['hSelectedMark'],2);arrive(h)
  self.assertEqual((h.p['motionX']//64,h.p['motionY']//64),(285,140))
 def test_restore_retirement_preserves_partial_logical_reader_silently(self):
  h,d,a,p,q,r=make();garage(h)
  # Every canonical P05 source is one page; preserve an unpresented logical request.
  # No synthetic multi-page production source is inserted for the test.
  practical(h,r);h.call('hostActNow',5,71,0)
  self.assertEqual(h.p['uiPageCount'],1);self.assertEqual(r.p['hSeenCount'],0)
  state=h.vm.snapshot();oldticket=(r.p['hTicketHi'],r.p['hTicketLo'],list(r.arrays['hTicketSession']))
  played=a.p['played'];logical=list(r.arrays['p05Words']);self.assertEqual(r.call('hSaveReady'),1)
  restore(h,state,[{'type':4,'message':13},{'type':1,'x':280,'y':110},{}])
  self.assertEqual(r.p['hRestoreValid'],1);self.assertEqual(r.p['hSeenCount'],0)
  self.assertEqual(list(r.arrays['p05Words']),logical);self.assertEqual(a.p['played'],played)
  self.assertEqual((a.p['lane'],a.p['pendingLaugh'],d.p['sdArmed'],d.p['sdPendingStart']),(0,0,0,0))
  self.assertEqual(h.p['motionPhase'],0);self.assertEqual(h.p['type'],0)
  r.call('p05SetInput',1,*oldticket[:2],*oldticket[2]);self.assertNotEqual(r.call('p05AcknowledgeSource',3,42),21)
  frame(h);self.assertEqual(r.call('p05Journal',3),42)
  # Repeated same snapshot is safe through retirement, not uniqueness of a rolled-back counter.
  restore(h,state,[{'type':4,'message':13},{}]);self.assertEqual(r.call('p05Journal',3),0)
  self.assertEqual(r.p['hSeenCount'],0);self.assertEqual(a.p['played'],played)
 def test_restore_rejects_corrupt_source_bitmap_and_physical_owner(self):
  h,d,a,p,q,r=make();garage(h);h.call('hostActNow',5,64,0);state=h.vm.snapshot()
  arr=h.vm.abi['modules']['985']['locals'];offset=next(x['word_offset'] for x in arr if x['name']=='hSeen')
  state['locals']['985'][offset+63]=1
  restore(h,state,[{}]);self.assertEqual(r.p['hPendingSource'],0);self.assertEqual(r.call('p05Journal',1),0)
  state=h.vm.snapshot();state['objects']['p05State']['hPARoom']=4
  restore(h,state,[{}]);self.assertEqual(r.p['hFailure'],4);self.assertEqual(r.call('hBarrier'),1)
 def test_practical_interleaves_bunting_and_ceramic_rewards_with_world_frames(self):
  h,d,a,p,q,r=make();practical(h,r);p05=list(r.arrays['p05Words'])
  for args in ((0,17),(0,14),(2,60),(7,4,60),(9,62),(0,17),(0,16),(5,37),(7,25,40)):act(h,*args)
  h.call('uiHostChoice',204,1);close(h)
  if h.p['uiPanel']:h.call('uiClose');frame(h)
  for args in ((0,17),(2,1),(0,1),(0,12),(4,39),(0,18),(0,17),(0,16),(7,39,34),(1,40,30)):act(h,*args)
  self.assertEqual((p.p['p03Ready'],q.p['p04Bunting'],h.arrays['uiItems'].count(62),h.arrays['uiItems'].count(35)),(1,1,1,1))
  self.assertEqual(list(r.arrays['p05Words']),p05)
  state=h.vm.snapshot();restore(h,state,[{'type':4,'message':13},{}]);frame(h)
  self.assertEqual(list(r.arrays['p05Words']),p05);self.assertEqual((h.arrays['uiItems'].count(62),h.arrays['uiItems'].count(35)),(1,1))
  self.assertEqual(h.p['uiFailure'],0)
 def test_actual_missing_output_route_rolls_back_domain(self):
  h,d,a,p,q,r=make();garage(h);before=list(r.arrays['p05Words'])
  # Explicit negative test corrupts only this VM's route array after admission.
  old=d.arrays['sdCounts'][445];d.arrays['sdCounts'][445]=0
  self.assertEqual(r.call('hRun',6,66),0);self.assertEqual(list(r.arrays['p05Words']),before)
  self.assertEqual(r.p['hFailure'],1);self.assertEqual(h.p['bridgeQueueCount'],0)
  d.arrays['sdCounts'][445]=old
 def test_missing_routes_and_transaction_reentry_fail_closed(self):
  h,d,a,p,q,r=make();garage(h);old=list(r.arrays['p05Words']);r.p['hEnabled']=0
  act(h,7,65,66);self.assertEqual(list(r.arrays['p05Words']),old)
  r.p['hEnabled']=1;r.p['hCritical']=1
  for method,args in [('hostActNow',(7,65,66)),('uiHostChoice',(212,1)),('uiHostChoice',(204,1)),('uiHostConfirm',(201,)),('writeSave',()),('readSave',())]:
   h.call(method,*args);self.assertEqual(list(r.arrays['p05Words']),old)
  self.assertEqual(h.vm.kernel_attempts['SaveGame'],0);self.assertEqual(h.vm.kernel_attempts['RestoreGame'],0)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Practical))
 report=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,failures=[(str(t),s) for t,s in result.failures],errors=[(str(t),s) for t,s in result.errors],instructions=sum(v.steps for v in VMS),frames=sum(v.frames for v in VMS),native_acceptance=False)
 (H/'evidence/practical-tests.json').write_text(json.dumps(report,indent=2)+'\n');raise SystemExit(not result.wasSuccessful())
