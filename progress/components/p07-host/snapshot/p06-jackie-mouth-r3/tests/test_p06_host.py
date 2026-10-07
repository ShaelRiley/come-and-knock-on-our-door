"""Ordinary game QA against the real emitted host and source-executed987.
No native ScummVM, audio listening, GUI automation, arbitrary-storage attacks,
network actions or new puzzle implementation in the oracle.
"""
import unittest,copy,json,hashlib
from p06_support import *
PROOFS=[]

class P06Host(unittest.TestCase):
 def test_source_and_emitted_permission_ownership_and_reversible_geometry(self):
  observations=[]
  for kind in ['source','bytecode']:
   h,d,a,p,q,r,s,v=new(kind)
   act(h,0,12);act(h,4,75)
   self.assertEqual(s.p['h6LastCode'],44);self.assertEqual(s.call('p06Projection',1),0)
   act(h,0,18);materials(h)
   self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[1,1])
   act(h,6,85);choice(h,219,3)
   self.assertEqual(s.call('p06Projection',0),0)
   act(h,6,85);choice(h,219,1)
   act(h,7,75,73);choice(h,221,1)
   self.assertEqual((s.call('p06Projection',5),s.call('p06Projection',1),s.call('p06Projection',2)),(1,0,1))
   self.assertEqual(h.arrays['uiItems'].count(75),0)
   act(h,7,76,74);self.assertEqual(s.p['h6LastCode'],51)
   act(h,7,75,73);choice(h,221,2);act(h,7,76,74)
   self.assertEqual(s.call('p06Projection',5),3)
   self.assertFalse(any(i in [75,76] for i in h.arrays['uiItems']))
   for pos,wanted in [(2,(0,0)),(3,(1,0)),(1,(1,1)),(0,(0,1)),(1,(1,1))]:
    act(h,8,80);choice(h,222,pos)
    self.assertEqual((s.call('p06Projection',3),s.call('p06Projection',4)),wanted)
    frame(h)
   act(h,9,74);self.assertEqual((s.call('p06Projection',5),s.call('p06Projection',2)),(2,1))
   act(h,9,75);self.assertEqual((s.call('p06Projection',5),s.call('p06Projection',1)),(0,1))
   act(h,7,75,73);choice(h,221,2);act(h,7,76,74)
   self.assertEqual(s.call('p06Projection',5),3)
   observations.append(logical(h));self.assertEqual(s.call('h6SaveReady'),1)
  self.assertEqual(*observations);PROOFS.append({'case':'source-bytecode practical parity','scope_and_inventory_exact':True})

 def test_optional_tone_mixer_and_contest_do_not_purchase_scope(self):
  h,d,a,p,q,r,s,v=new();practical(h,s,scope=False)
  before=s.call('p06Projection',0);act(h,6,85);choice(h,219,6)
  self.assertEqual((s.call('p06Projection',0),v.call('vcRead',7)),(before,0))
  act(h,6,85);choice(h,219,1)
  for tone in [1,2,3,1]:
   act(h,6,85);choice(h,219,2);choice(h,220,tone)
   self.assertEqual((s.call('p06Projection',0),s.call('p06Projection',6)),(3,tone))
  act(h,6,85);choice(h,219,4)
  for answer in [1,2,1]:
   act(h,6,85);choice(h,219,5);choice(h,223,answer)
   self.assertEqual((s.call('p06Projection',0),s.call('p06Projection',7)),(3,answer))
  self.assertEqual(v.call('vcFlags'),0)

 def test_actual_all_page_all_unit_graph12_barrier_and_silent_records(self):
  for kind in ['source','bytecode']:
   h,d,a,p,q,r,s,v=new(kind);a.p['voiceMuted']=1
   act(h,6,8);h.call('uiHostChoice',202,11)
   self.assertEqual((s.p['h6PendingPages'],s.p['h6SeenCount']), (3,0))
   before=list(s.arrays['p06Words'])
   for guard in ['paused','menuOpen','opening']:
    h.p[guard]=1;h.call('dialoguePresented');h.p[guard]=0
    self.assertEqual(list(s.arrays['p06Words']),before)
   s.call('h6Presented',906,0,d.p['sdGeneration']-1)
   self.assertEqual(list(s.arrays['p06Words']),before)
   h.vm.draw_success=False
   with self.assertRaises(base.VMError):frame(h)
   h.vm.draw_success=True;self.assertEqual(list(s.arrays['p06Words']),before)
   frame(h);self.assertEqual(s.p['h6SeenCount'],1)
   h.call('uiTurnPage',2);frame(h)
   self.assertEqual((s.p['h6SeenCount'],s.call('p06Read',7),s.call('p06Read',8)),(2,0,0))
   h.call('uiTurnPage',-1);frame(h)
   self.assertEqual(s.p['h6PendingSource'],0);self.assertTrue(s.call('p06Read',8))
   close(h);act(h,0,17);h.call('hostActNow',5,82,0)
   self.assertEqual(s.p['h6PendingPages'],1)
   self.assertEqual(s.call('p06UnitCount',10),0)
   self.assertEqual(s.call('p06Journal',1),0)
   played=a.p['played'];frame(h);self.assertEqual(s.call('p06Journal',1),10)
   self.assertEqual(a.p['played'],played);self.assertEqual(a.p['voiceMuted'],1)

 def test_close_cancel_travel_and_replacement_never_award_read(self):
  h,d,a,p,q,r,s,v=new();act(h,6,8);h.call('uiHostChoice',202,11);frame(h)
  h.call('uiClose');self.assertEqual(s.call('p06Read',8),0);self.assertEqual(s.p['h6PendingSource'],0)
  act(h,6,8);h.call('uiHostChoice',202,11);frame(h)
  h.call('hostActNow',0,17,0);self.assertEqual(h.p['location'],0)
  self.assertEqual(s.call('p06Read',8),0);self.assertEqual(s.p['h6PendingSource'],0)
  h.call('hostActNow',5,77,0);self.assertEqual(s.p['h6PendingSource'],3)
  frame(h);h.call('hostActNow',5,82,0)
  self.assertEqual(s.p['h6PendingSource'],1);self.assertEqual(s.call('p06Journal',3),0)
  close(h);self.assertEqual(s.call('p06Journal',1),10)

 def test_partial_restore_preserves_exact_reader_queue_identity_and_silence(self):
  for kind in ['source','bytecode']:
   h,d,a,p,q,r,s,v=new(kind);act(h,6,8);h.call('uiHostChoice',202,11);frame(h)
   before=logical(h);snapshot=h.vm.snapshot();played=a.p['played'];oldtoken=list(s.arrays['h6TicketSession'])
   for _ in range(2):
    restore(h,copy.deepcopy(snapshot),[{'type':4,'message':13},{'type':1,'x':80,'y':170},{}])
    self.assertEqual((s.p['h6RestoreValid'],s.p['h6SeenCount'],h.p['uiFailure']),(1,1,0))
    self.assertEqual(logical(h),before)
    self.assertEqual((a.p['played'],a.p['lane'],d.p['sdPendingStart']),(played,0,0))
    self.assertEqual(s.call('h6ReaderIdentity'),1)
   self.assertNotEqual(list(s.arrays['h6TicketSession']),oldtoken)
   close(h);self.assertTrue(s.call('p06Read',8))
  PROOFS.append({'case':'whole-VM same-build restore','freshness':'total synchronous retirement; not globally fresh saved counters','source':'retained exact queue slot, queue count/index, source record, room, page and unit bitmap'})

 def test_inconsistent_saved_reader_and_current_owner_fail_closed(self):
  h,d,a,p,q,r,s,v=new();act(h,6,8);h.call('uiHostChoice',202,11);frame(h);snapshot=h.vm.snapshot()
  def offset(name):return next(x['word_offset'] for x in h.vm.abi['modules']['987']['locals'] if x['name']==name)
  cases=[('h6PendingRecord',10),('h6PendingDocument',891),('h6PendingQueue',1),('h6PendingQueueCount',2),('h6PendingPages',2),('h6PendingRoom',0),('h6ScreenRoom',4)]
  for key,value in cases:
   bad=copy.deepcopy(snapshot);bad['objects']['p06State'][key]=value;restore(h,bad,[{}])
   self.assertEqual((s.p['h6RestoreValid'],h.p['uiFailure']),(0,10),key)
  for name,index,value in [('h6Seen',0,2),('h6Seen',1,1),('h6UnitsSeen',0,0),('h6UnitsSeen',8,1)]:
   bad=copy.deepcopy(snapshot);bad['locals']['987'][offset(name)+index]=value;restore(h,bad,[{}])
   self.assertEqual((s.p['h6RestoreValid'],h.p['uiFailure']),(0,10),(name,index))
  restore(h,snapshot,[{},{}]);self.assertEqual(s.p['h6RestoreValid'],1)

 def test_recap_teaches_missing_ab_without_vc01_and_exact_saved_deck(self):
  h,d,a,p,q,r,s,v=taught();self.assertEqual(v.call('vcRead',6),0)
  self.assertFalse(any(v.call('vcLearned',i,j) for i in range(13,25) for j in [1,2]))
  start(h,v);deck=list(v.arrays['vcWords'])[106:111]
  self.assertEqual(len(set(deck)),5)
  self.assertTrue(all(7<=i<=12 for i in deck[:2]));self.assertTrue(all(1<=i<=6 for i in deck[2:]))
  before=logical(h);saved=h.vm.snapshot();restore(h,saved,[{},{}]);self.assertEqual(logical(h),before)
  self.assertEqual(list(v.arrays['vcWords'])[106:111],deck)
  self.assertEqual((r.p['hVCEncounter'],s.p['h6RestoreValid']),(2,1))

 def test_yield_is_nonko_loss_readable_concession_and_single_unplaced_loan(self):
  for kind in ['source','bytecode']:
   h,d,a,p,q,r,s,v=taught(kind);finish(h,v,'yield')
   self.assertEqual((v.call('vcFlags'),v.call('vcRead',100),v.call('vcRead',101)),(2,2,2))
   receipts=[(x['record'],x['unit']) for x in getattr(h.vm,'receipts',[])]
   self.assertIn((50,16),receipts);self.assertIn((50,17),receipts)
   self.assertFalse(any(record in [52,53] for record,unit in receipts))
   before=s.call('p06Projection',6);act(h,6,85);choice(h,219,7)
   self.assertEqual((s.call('p06Projection',0),s.p['h6ScreenOwner'],s.p['h6ScreenRoom'],s.p['h6ScreenPosition']),(7,1,4,0))
   self.assertEqual((s.call('p06Projection',6),s.call('p06Projection',7)),(before,0))
   self.assertFalse(any(73<=x<=85 for x in h.arrays['uiItems']))
   state=logical(h);act(h,6,85);choice(h,219,7);self.assertEqual(logical(h),state)
   saved=h.vm.snapshot();played=a.p['played'];restore(h,saved,[{},{}]);self.assertEqual(logical(h),state);self.assertEqual(a.p['played'],played)
   act(h,2,1);act(h,0,1);act(h,0,13);self.assertEqual(h.p['location'],4)
   self.assertEqual(h.call('p02ObjectLocation',81),4)
   act(h,5,82);self.assertEqual(s.call('p06Journal',1),10)
   self.assertEqual(s.p['h6ScreenPosition'],0)

 def test_real_scored_loss_groan_and_later_win_have_separate_flags(self):
  h,d,a,p,q,r,s,v=taught();finish(h,v,'loss')
  self.assertEqual((v.call('vcFlags'),v.call('vcRead',96),v.call('vcRead',97),v.call('vcRead',101)),(2,0,3,1))
  self.assertEqual(r.p['hVCExtra'],0)
  self.assertTrue(any(n=='hVCShowGroan' and module==985 for module,n in h.vm.calls))
  finish(h,v,'win');self.assertEqual(v.call('vcFlags'),34)
  self.assertEqual((s.call('p06Projection',0),s.call('p06Projection',6),s.call('p06Projection',7)),(3,0,0))
  self.assertEqual((v.call('vcRead',6),r.call('p05Flags')),(0,0))
  finish(h,v,'yield');self.assertEqual(v.call('vcFlags'),34)

 def test_unread_result_and_every_vivian_concession_page_block_loan(self):
  h,d,a,p,q,r,s,v=taught();start(h,v)
  h.call('uiHostChoice',217,26)
  # Genuine yield completes the outcome but all result/concession text remains unread.
  self.assertEqual(v.call('vcFlags'),2);self.assertEqual(r.p['hContestBlocked'],1)
  before=list(s.arrays['p06Words']);room=h.p['location']
  for name,args in [('uiHostChoice',(219,7)),('hostActNow',(0,14,0)),('uiHostAct',(0,17,0)),('bridgeActAtArrival',(6,85,0)),('uiHostConfirm',(219,)),('p03PreparationHint',()),('startReplay',())]:
   h.call(name,*args);self.assertEqual(list(s.arrays['p06Words']),before);self.assertEqual(h.p['location'],room)
  guard=0
  while r.p['hContestBlocked']:
   guard+=1;self.assertLess(guard,8)
   h.call('uiHostChoice',219,7);self.assertEqual(s.p['h6ScreenRoom'],0)
   consume_current(h)
  self.assertEqual(v.call('vcRead',92),8)
  act(h,6,85);choice(h,219,7);self.assertEqual(s.p['h6ScreenRoom'],4)

 def test_practical_order_independence_and_shared_repertoire_owner(self):
  h,d,a,p,q,r,s,v=taught();finish(h,v,'yield');act(h,6,85);choice(h,219,7)
  # P05 ordinary actions still work after the P06-first path; A learning persists.
  act(h,0,15);self.assertEqual(h.p['location'],5)
  act(h,0,9);act(h,6,10);choice(h,210,1);act(h,0,11)
  act(h,7,65,66);act(h,7,64);choice(h,212,1);act(h,8,68);choice(h,213,2);act(h,6,65);choice(h,214,2)
  act(h,7,25,71);act(h,6,28);choice(h,211,3);act(h,6,28);choice(h,211,4)
  self.assertEqual(r.p['hVCEncounter'],1);start(h,v);reply(h,26)
  self.assertEqual(v.call('vcFlags'),3);act(h,6,28);choice(h,211,5)
  self.assertEqual((r.call('p05Flags'),s.call('p06Projection',0)),(7,7))
  self.assertEqual((r.p['hPARoom'],s.p['h6ScreenRoom']),(4,4))

 def test_preplan_apron_wrong_room_nine_verbs_and_physical_speech(self):
  for plan,apron in [(False,0),(True,1)]:
   h,d,a,p,q,r,s,v=new(plan=plan);h.p.update(location=0,roomSeen=0,onApron=apron,apronSeen=apron)
   before=list(s.arrays['p06Words'])
   for obj in range(73,86):
    for verb in range(10):h.call('hostActNow',verb,obj,0)
   self.assertEqual(list(s.arrays['p06Words']),before);self.assertEqual(v.call('vcFlags'),0)
  h,d,a,p,q,r,s,v=new()
  self.assertEqual((h.call('dialogueCanSpeak',6),h.call('dialogueCanSpeak',3)),(0,1))
  act(h,0,17);self.assertEqual((h.call('dialogueCanSpeak',6),h.call('dialogueCanSpeak',3)),(1,0))
  h.p['motionPhase']=1;self.assertEqual(h.call('dialogueCanSpeak',6),0);h.p['motionPhase']=0
  h.vm.ktrace=[];h.call('drawWorld');self.assertTrue(any(n=='DrawCel' and args[0]==236 for n,args in h.vm.ktrace))
  before=list(s.arrays['p06Words']);act(h,0,14);act(h,7,75,73);self.assertEqual(list(s.arrays['p06Words']),before)

 def test_failed_route_reservation_keeps_all_owners_outputs_and_inventory(self):
  h,d,a,p,q,r,s,v=taught();finish(h,v,'yield')
  before=logical(h);snapshot=h.vm.snapshot();starts=d.arrays['sdStarts'];old=starts[925];starts[925]=-1
  act(h,6,85);h.call('uiHostChoice',219,7)
  self.assertEqual(logical(h),before);self.assertEqual((s.p['p06Busy'],h.p['bridgeQueueCount']),(0,0))
  self.assertTrue(all(x==0 for x in s.arrays['p06Output']))
  # Broken canonical table fails closed; resume only from the exact valid whole-VM snapshot.
  restore(h,snapshot,[{},{}]);act(h,6,85);choice(h,219,7);self.assertEqual(s.call('p06Projection',0),7)

 def test_synchronous_publication_blocks_native_reentry_and_save(self):
  h,d,a,p,q,r,s,v=taught();finish(h,v,'yield');observed=[]
  def hook(obj,name,args,result):
   if obj.name=='cakood' and name=='h6PublishNative' and s.p['h6Critical']:
    observed.append([s.p['p06Busy'],s.p['h6Critical'],s.p['h6ScreenRoom']])
    old=list(s.arrays['p06Words']);h.call('hostActNow',0,14,0);h.call('uiHostChoice',219,1)
    self.assertEqual(list(s.arrays['p06Words']),old);self.assertEqual(s.call('h6SaveReady'),0)
    self.assertEqual(h.call('writeSave'),0)
  h.vm.after_actual_call=hook;act(h,6,85);choice(h,219,7);h.vm.after_actual_call=None
  self.assertEqual(observed,[[1,1,0]]);self.assertEqual(s.p['h6ScreenRoom'],4)

 def test_keyboard_two_noun_cancel_and_inventory_metrics(self):
  h,d,a,p,q,r,s,v=new();materials(h)
  for obj,label in [(75,'SHEET'),(76,'CLIPS')]:
   text=base.read_string(h.call('uiHostShortLabel',obj));self.assertEqual(text,label);self.assertLessEqual(len(text)*6,32)
  enter_control(h,2,7);enter_control(h,3,75)
  self.assertEqual(s.call('p06Projection',5),0)
  h.vm.pump([{'type':4,'message':27},{}]);self.assertEqual(s.call('p06Projection',5),0)
  input_action(h,7,75,73);arrive(h);self.assertEqual(h.p['uiChoiceContext'],221)
  h.p['uiPage']=0;h.p['uiFocus']=0;enter_control(h,13,index=0);close(h)
  self.assertEqual(s.call('p06Projection',5),2)
  input_action(h,7,76,74);arrive(h);close(h);self.assertEqual(s.call('p06Projection',5),3)
  h.call('uiBuildFocus');self.assertTrue(any(h.arrays['uiPayloads'][i]==80 for i in range(h.p['uiControlCount'])))


 def test_real_control_precedence_preserves_door_bench_and_specific_components(self):
  h,d,a,p,q,r,s,v=new();act(h,0,17)
  h.p['doorOpen']=1;h.call('uiBuildFocus')
  def hit(x,y):
   i=h.call('uiHit',x,y);self.assertGreaterEqual(i,0)
   return h.arrays['uiActions'][i],h.arrays['uiPayloads'][i]
  self.assertEqual(hit(200,80),(18,1));self.assertEqual(hit(215,116),(18,1))
  self.assertEqual(hit(110,100),(1,3));self.assertEqual(hit(75,120),(1,85))
  self.assertEqual(hit(26,105),(1,80));self.assertEqual(hit(15,105),(1,78));self.assertEqual(hit(42,102),(1,79))
  self.assertEqual(hit(289,82),(1,82));self.assertEqual(hit(260,47),(1,74))
  self.assertEqual(hit(275,80),(1,73));self.assertEqual(hit(310,120),(1,9))
  act(h,0,1);materials(h);act(h,7,75,73);choice(h,221,1);h.call('uiBuildFocus')
  self.assertEqual(hit(265,110),(1,75))
  input_action(h,7,75,73);arrive(h);self.assertEqual((h.p['uiPanel'],h.p['uiChoiceContext']),(2,221));choice(h,221,2)
  h.call('uiBuildFocus');self.assertEqual(hit(265,75),(1,75))
  input_action(h,9,75);arrive(h);close(h)
  self.assertEqual(h.arrays['uiItems'].count(75),1)


 def test_loan_output_restore_keeps_two_queued_records_without_republication(self):
  h,d,a,p,q,r,s,v=taught();finish(h,v,'yield');act(h,6,85)
  h.call('uiHostChoice',219,7)
  self.assertEqual((s.call('p06Projection',0),h.p['bridgeQueueCount'],h.p['bridgeQueueIndex'],h.p['uiDocument']),(7,2,1,924))
  self.assertEqual([h.call('p04QueueItem',i) for i in range(2)],[924,925])
  frame(h);saved=h.vm.snapshot();played=a.p['played'];before=list(s.arrays['p06Words'])
  restore(h,saved,[{},{}])
  self.assertEqual((h.p['bridgeQueueCount'],h.p['bridgeQueueIndex'],h.p['uiDocument']),(2,1,924))
  self.assertEqual(list(s.arrays['p06Words']),before);self.assertEqual(a.p['played'],played)
  close(h);self.assertEqual(h.p['bridgeQueueCount'],2);self.assertEqual(h.p['bridgeQueueIndex'],2)
  self.assertEqual((s.p['h6ScreenOwner'],s.p['h6ScreenRoom'],s.p['h6ScreenPosition']),(1,4,0))


 def test_restore_publishes_inventory_only_after_domain_context_and_owner_admission(self):
  h,d,a,p,q,r,s,v=new();materials(h)
  self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[1,1])
  saved=h.vm.snapshot();events=[]
  def hook(obj,name,args,result):
   if obj.name=='p06State' and name=='h6Inventory':events.append(['inventory',s.p['h6RestoreValid'],result])
   if obj.name=='cakood' and name=='h6PublishNative':events.append(['publish',s.p['h6RestoreValid'],s.p['h6Critical'],s.call('p06SaveReady'),s.call('p06ValidateContextLive'),s.call('h6OwnersValid'),r.p['hRestoreValid'],v.p['vcReady']])
  h.vm.after_actual_call=hook;restore(h,saved,[{},{}]);h.vm.after_actual_call=None
  self.assertIn(['inventory',0,0],events)
  publish=[row for row in events if row[0]=='publish']
  self.assertTrue(publish);self.assertTrue(all(row[2:]==[1,1,1,1,1,1] for row in publish))
  self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[1,1])
  events.clear();bad=copy.deepcopy(saved);bad['objects']['p06State']['h6ScreenRoom']=4
  h.vm.after_actual_call=hook;restore(h,bad,[{}]);h.vm.after_actual_call=None
  self.assertFalse(any(row[0]=='publish' for row in events));self.assertEqual(s.p['h6RestoreValid'],0)


 def test_p03_read_and_pickup_keep_carried_p06_inventory(self):
  for kind in ['source','bytecode']:
   h,d,a,p,q,r,s,v=new(kind);materials(h);owned=list(s.arrays['p06Words'])
   act(h,0,16)
   for args in [(5,33),(5,34),(4,35),(5,36)]:
    act(h,*args)
    self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[1,1],(kind,args))
    self.assertEqual(s.call('h6PhysicalValid'),1);self.assertEqual(list(s.arrays['p06Words']),owned)
   saved=h.vm.snapshot();restore(h,saved,[{},{}])
   self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[1,1])
   self.assertEqual(s.call('h6SaveReady'),1)

 def test_p04_inventory_publications_keep_carried_p06_inventory(self):
  h,d,a,p,q,r,s,v=new();materials(h);owned=list(s.arrays['p06Words']);act(h,0,14)
  for args in [(5,60),(2,60),(7,4,60),(9,62),(7,62,55),(4,4)]:
   act(h,*args)
   self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[1,1],args)
   self.assertEqual(s.call('h6PhysicalValid'),1);self.assertEqual(list(s.arrays['p06Words']),owned)

 def test_original_candidate1_exposes_p03_projection_regression(self):
  import host as runtime_host
  oldroot=runtime_host.H
  try:
   runtime_host.H=H/'inputs/r1'
   h,d,a,p,q,r=runtime_host.setup();VMS.append(h.vm);s=h.vm.objects['p06State']
   h.vm.budget=100000000;materials(h);act(h,0,16)
   self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[1,1])
   before=list(s.arrays['p06Words']);act(h,5,33)
   self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[0,0])
   with self.assertRaises(AssertionError):self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[1,1])
   self.assertEqual([s.call('p06Projection',i) for i in [1,2]],[1,1])
   self.assertEqual(s.call('h6PhysicalValid'),0);self.assertEqual(list(s.arrays['p06Words']),before)
  finally:runtime_host.H=oldroot

 def test_each_or_both_props_survive_p03_read_close_journal_failed_actions_and_travel(self):
  for held in ['sheet','clips','both']:
   h,d,a,p,q,r,s,v=new()
   if held in ['sheet','both']:
    act(h,6,8);choice(h,202,11);act(h,0,12);act(h,4,75);act(h,0,18)
   act(h,0,17)
   if held in ['clips','both']:act(h,0,14);act(h,4,76);act(h,0,17)
   wanted=[int(held in ['sheet','both']),int(held in ['clips','both'])]
   before=list(s.arrays['p06Words'])
   def inventory_ok():
    self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],wanted,held)
    self.assertEqual(s.call('h6PhysicalValid'),1);self.assertEqual(list(s.arrays['p06Words']),before)
   act(h,0,16);inventory_ok()
   h.call('hostActNow',5,33,0);inventory_ok();frame(h);h.call('uiClose');inventory_ok()
   act(h,5,33);inventory_ok();act(h,5,34);inventory_ok()
   act(h,5,32);choice(h,208,101);h.call('uiClose');frame(h);inventory_ok()
   act(h,7,35,47);inventory_ok();act(h,1,35,30);inventory_ok()
   act(h,0,17);act(h,0,14);inventory_ok()
   for args in [(2,60),(7,4,60),(9,62)]:act(h,*args);inventory_ok()
   saved=h.vm.snapshot();restore(h,saved,[{},{}]);inventory_ok()
   act(h,0,17);act(h,0,16);inventory_ok()
