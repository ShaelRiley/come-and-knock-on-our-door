import unittest,json,copy
from host import *
from test_practical import restore,enter_control
VMS=[]
def prepared():
 h,d,a,p,q,r=setup();VMS.append(h.vm);practical(h,r);v=h.vm.objects['contestState'];return h,d,a,p,q,r,v

def taught(muted=False):
 h,d,a,p,q,r,v=prepared()
 if muted:a.p.update(voiceMuted=1,audienceMuted=1,effectsMuted=1)
 act(h,6,28);choice(h,211,4)
 assert v.call('vcFlags')==0 and r.call('p05Flags')==3
 for pair in range(1,7):choice(h,215,1);choice(h,216,pair)
 assert all(v.call('vcLearned',i,j) for i in range(1,7) for j in [1,2])
 return h,d,a,p,q,r,v

def start(h,v):choice(h,215,2);assert v.call('vcRead',92)==3

def reply(h,pair):
 v=h.vm.objects['contestState'];score=(v.call('vcRead',96),v.call('vcRead',97))
 choice(h,217,pair)
 if pair!=26:
  assert (v.call('vcRead',96),v.call('vcRead',97))==score
  assert v.call('vcRead',92)==4 and h.p['uiChoiceContext']==218
  choice(h,218,1)

def win(h,v):
 start(h,v)
 for _ in range(3):reply(h,v.call('vcRead',106+v.call('vcRead',95)))
 assert v.call('vcFlags')&17==17

def consume_current(h):
 for p in range(h.p['uiPageCount']):
  if h.p['uiPage']!=p:h.call('uiTurnPage',p-h.p['uiPage'])
  frame(h)
 h.call('uiClose')

def drive_to_result(h,v):
 start(h,v)
 for _ in range(2):reply(h,v.call('vcRead',106+v.call('vcRead',95)))
 h.call('uiHostChoice',217,v.call('vcRead',106+v.call('vcRead',95)))
 h.call('uiHostChoice',218,1)
 while v.call('vcRead',92)!=7:consume_current(h)
 if h.vm.objects['p05State'].p['hVCExtra']:consume_current(h)
 assert h.p['uiPanel']==4

class Contest(unittest.TestCase):
 def test_intro_ack_does_not_grant_resolution_or_learning(self):
  h,d,a,p,q,r,v=prepared();act(h,6,28);h.call('uiHostChoice',211,4)
  self.assertEqual((v.call('vcRead',6),v.call('vcFlags'),r.call('p05Flags')),(1,0,3))
  self.assertFalse(any(v.call('vcLearned',i,k) for i in range(1,25) for k in [1,2]))
  before=list(v.arrays['vcWords']);h.call('uiClose')
  self.assertEqual(list(v.arrays['vcWords']),before);self.assertEqual(h.p['uiDocument'],854)
  close(h);self.assertEqual(v.call('vcFlags'),0)
  self.assertEqual([(x['record'],x['unit']) for x in h.vm.receipts if x['record']==41],[(41,1),(41,2),(41,3)])
 def test_real_learning_scoring_win_and_atomic_loan(self):
  h,d,a,p,q,r,v=taught();win(h,v)
  self.assertEqual((r.call('p05Flags'),r.p['hPARoom']),(3,5))
  receipts=[(x['record'],x['unit']) for x in h.vm.receipts]
  self.assertIn((33,0),receipts);self.assertIn((42,4),receipts);self.assertIn((42,5),receipts)
  self.assertTrue(all(x['pages']==x['seen'] and x['graph12']>0 for x in h.vm.receipts))
  before=list(r.arrays['p05Words']);act(h,6,28);choice(h,211,5)
  self.assertEqual((r.call('p05Flags'),r.p['hPAOwner'],r.p['hPARoom'],r.p['hCartOwner'],r.p['hCartRoom']),(7,1,4,1,5))
  self.assertEqual(h.call('campaignHeld',25),1);self.assertFalse(any(63<=i<=72 for i in h.arrays['uiItems']))
  state=list(r.arrays['p05Words']);act(h,6,28);choice(h,211,5);self.assertEqual(list(r.arrays['p05Words']),state)
 def test_result_concession_barrier_blocks_every_ordinary_route(self):
  h,d,a,p,q,r,v=taught();drive_to_result(h,v)
  self.assertEqual(v.call('vcFlags'),17);self.assertEqual(r.p['hContestBlocked'],1)
  p05=list(r.arrays['p05Words']);p03=[(k,x) for k,x in p.p.items() if k.startswith('p03')];p04=[(k,x) for k,x in q.p.items() if k.startswith('p04')]
  original_doc=h.p['uiDocument'];h.call('uiClose')
  self.assertEqual(h.p['uiDocument'],original_doc);self.assertEqual(v.call('vcRead',130),0)
  for method,args in [('hostActNow',(0,17,0)),('hostActNow',(7,65,66)),('uiHostAct',(0,17,0)),('bridgeActAtArrival',(6,28,0)),('uiHostChoice',(211,5)),('uiHostChoice',(204,1)),('uiHostChoice',(207,2)),('uiHostConfirm',(201,)),('p03PreparationHint',()),('p02Hint',(1,)),('p02Journal',()),('startReplay',())]:
   h.call(method,*args);self.assertEqual(r.arrays['p05Words'],p05,(method,args));self.assertEqual(h.p['location'],5);self.assertEqual(r.p['hPARoom'],5)
  self.assertEqual([(k,x) for k,x in p.p.items() if k.startswith('p03')],p03)
  self.assertEqual([(k,x) for k,x in q.p.items() if k.startswith('p04')],p04)
  consume_current(h);self.assertEqual(v.call('vcRead',92),7);self.assertEqual(r.p['hContestBlocked'],1)
  self.assertEqual((r.p['hVCRecord'],r.p['hVCUnit']),(42,4))
  consume_current(h);self.assertEqual(v.call('vcRead',92),7);self.assertEqual(r.p['hContestBlocked'],1)
  self.assertEqual((r.p['hVCRecord'],r.p['hVCUnit']),(42,5))
  frame(h);self.assertEqual(v.call('vcRead',92),8);self.assertEqual(r.p['hContestBlocked'],1)
  h.call('uiHostChoice',211,5);self.assertEqual(r.p['hPARoom'],5)
  h.call('uiClose');frame(h);self.assertEqual(r.p['hContestBlocked'],0)
 def test_explicit_loss_yield_concession_and_later_win_latches(self):
  h,d,a,p,q,r,v=taught();start(h,v);reply(h,26)
  self.assertEqual(v.call('vcFlags'),1);self.assertEqual(v.call('vcRead',100),2)
  receipts=[(x['record'],x['unit']) for x in h.vm.receipts];self.assertIn((35,0),receipts);self.assertIn((43,6),receipts);self.assertIn((43,7),receipts)
  act(h,6,28);choice(h,211,5);self.assertEqual(r.call('p05Flags'),7)
  act(h,6,28);choice(h,211,4);win(h,v);self.assertEqual(v.call('vcFlags'),17)
  start(h,v);reply(h,26);self.assertEqual(v.call('vcFlags'),17)
  self.assertEqual(r.call('p05Flags'),7);self.assertEqual(r.p['hPARoom'],4)
  self.assertIn((36,0),[(x['record'],x['unit']) for x in h.vm.receipts])
 def test_muted_learning_and_explicit_exchange_yield(self):
  h,d,a,p,q,r,v=taught(muted=True);start(h,v)
  for _ in range(3):reply(h,25)
  self.assertEqual(v.call('vcFlags'),1);self.assertEqual((v.call('vcRead',96),v.call('vcRead',97)),(0,3))
  self.assertIn((32,0),[(x['record'],x['unit']) for x in h.vm.receipts])
  self.assertTrue(any('MILO' in t for t in h.vm.paint));self.assertEqual(h.p['uiFailure'],0)
 def test_stale_receipts_graph_failure_pause_menu_and_restore_result(self):
  h,d,a,p,q,r,v=taught();drive_to_result(h,v);old=list(v.arrays['vcWords'])
  for guard in ['menuOpen','paused','opening']:
   h.p[guard]=1;h.call('dialoguePresented');self.assertEqual(list(v.arrays['vcWords']),old);h.p[guard]=0
  r.call('hVCPresented',h.p['uiDocument'],0,d.p['sdGeneration']-1);self.assertEqual(list(v.arrays['vcWords']),old)
  h.vm.draw_success=False
  with self.assertRaises(base.VMError):frame(h)
  self.assertEqual(list(v.arrays['vcWords']),old);h.vm.draw_success=True
  saved=h.vm.snapshot();played=a.p['played'];oldgen=(v.p['vcGenerationHi'],v.p['vcGenerationLo'])
  restore(h,saved,[{'type':4,'message':13},{'type':1,'x':80,'y':170},{}])
  self.assertEqual(list(v.arrays['vcWords']),old);self.assertNotEqual((v.p['vcGenerationHi'],v.p['vcGenerationLo']),oldgen)
  self.assertEqual((r.p['hContestBlocked'],v.call('vcRead',92),a.p['played']),(1,7,played))
  self.assertEqual((a.p['lane'],a.p['pendingLaugh'],d.p['sdPendingStart']),(0,0,0))
  close(h);self.assertEqual(v.call('vcRead',92),8)
  restore(h,saved,[{'type':4,'message':13},{}]);self.assertEqual(v.call('vcRead',92),7);self.assertEqual(r.p['hContestBlocked'],1)
  self.assertEqual(a.p['played'],played)
 def test_pending_reply_cancel_restore_reentry_and_all24_full_labels(self):
  h,d,a,p,q,r,v=taught();fixture_trace=[]
  # Explicit future-state fixture only. The accepted domain receives bounded
  # external lesson receipts; production host admits no P06/P11/P13 scene here.
  # No result, campaign prerequisite, ownership or score flag is fabricated.
  for pair in range(7,25):
   source=4+(pair-1)//6+1
   self.assertEqual(v.call('vcLesson',source,pair,0,1),1);self.assertEqual(v.call('vcCommit'),1)
   while v.call('vcRead',126):
    cursor=v.call('vcRead',130);record=v.call('vcRead',132+cursor);unit=v.call('vcRead',136+cursor)
    fixture_trace.append(dict(source=source,pair=pair,record=record,unit=unit))
    v.call('vcSetInput',v.p['vcGenerationHi'],v.p['vcGenerationLo'],v.call('vcRead',4),v.call('vcRead',5),4,cursor,record,unit)
    self.assertEqual(v.call('vcAcknowledge'),1);self.assertEqual(v.call('vcCommit'),1)
  self.assertEqual(v.call('vcFlags'),0)
  (H/'evidence/future-knowledge-fixture.json').write_text(json.dumps({'scope':'Explicit test-only future-domain lesson receipts, not production scene admission or campaign completion','trace':fixture_trace,'native_acceptance':False},indent=2)+'\n')
  start(h,v);self.assertEqual(h.p['uiChoiceCount'],26)
  catalog=json.loads((H/'snapshot/contest/canonical-bindings.json').read_text());records={x['id']:x for x in catalog['records']}
  for i in range(24):
   if i:enter_control(h,11,0)
   frame(h)
   expected=records[f'IR{i+1:02d}.REPLY']['text'].upper().replace('’',"'")
   self.assertEqual(base.read_string(h.arrays['uiChoiceLabels'][i]),expected)
   self.assertEqual(h.p['uiFailure'],0)
  score=(v.call('vcRead',96),v.call('vcRead',97));h.call('uiHostChoice',217,24);frame(h)
  self.assertEqual((v.call('vcRead',92),v.call('vcRead',98)),(4,24));self.assertEqual((v.call('vcRead',96),v.call('vcRead',97)),score)
  self.assertEqual(r.call('hSaveReady'),1);saved=h.vm.snapshot();restore(h,saved,[{'type':4,'message':13},{}]);frame(h)
  self.assertEqual((v.call('vcRead',92),v.call('vcRead',98),h.p['uiChoiceContext']),(4,24,218))
  h.call('uiClose');frame(h);self.assertEqual(h.p['uiChoiceContext'],217);self.assertEqual((v.call('vcRead',96),v.call('vcRead',97)),score)
  h.call('uiHostChoice',217,1);self.assertEqual(v.call('vcRead',98),1);h.call('uiHostChoice',218,2);frame(h)
  self.assertEqual((v.call('vcRead',96),v.call('vcRead',97)),score)
  h.call('uiHostChoice',217,2);h.call('uiHostChoice',218,1)
  self.assertEqual(v.call('vcRead',96)+v.call('vcRead',97),5)
  frozen=list(v.arrays['vcWords']);h.call('uiHostChoice',218,1);self.assertEqual(list(v.arrays['vcWords']),frozen)
  close(h);self.assertEqual(h.p['uiFailure'],0)
 def test_practice_uses_present_milo_and_never_bunny_learn_a_route(self):
  h,d,a,p,q,r,v=taught()
  self.assertEqual(r.p['hBunnyRoom'],1);self.assertEqual(h.p['location'],5)
  for pair in range(1,7):
   record=78+(pair-1)*3;unit=41+(pair-1)*5
   self.assertIn((record,unit),[(x['record'],x['unit']) for x in h.vm.receipts])
   self.assertEqual(r.call('hVCRoute',record,128+pair),0)
  self.assertEqual(v.call('vcFlags'),0)
 def test_partial_multi_item_read_restore_keeps_completed_unit_and_unread_concession(self):
  h,d,a,p,q,r,v=taught();drive_to_result(h,v)
  consume_current(h) # generic result read; first concession now open
  frame(h) # first concession read, second concession remains queued
  self.assertEqual((r.p['hVCRecord'],r.p['hVCUnit'],r.p['hVCDone'],v.call('vcRead',130)),(42,4,1,2))
  state=h.vm.snapshot();played=a.p['played'];words=list(v.arrays['vcWords'])
  restore(h,state,[{'type':4,'message':13},{}])
  self.assertEqual(list(v.arrays['vcWords']),words);self.assertEqual((r.p['hVCDone'],r.p['hVCSeenCount'],r.p['hFailure']),(1,1,0))
  self.assertEqual(a.p['played'],played);self.assertEqual(r.p['hContestBlocked'],1)
  h.call('uiClose');self.assertEqual((r.p['hVCRecord'],r.p['hVCUnit']),(42,5));self.assertEqual(v.call('vcRead',92),7)
  self.assertEqual(a.p['played'],played);frame(h);self.assertEqual(v.call('vcRead',92),8)
 def test_restore_wrong_document_binding_and_corrupt_seen_map_fail_closed(self):
  for corruption in ['document','seen']:
   h,d,a,p,q,r,v=taught();drive_to_result(h,v);saved=h.vm.snapshot();played=a.p['played']
   if corruption=='document':
    saved['objects']['p05State']['hVCDocument']=576
    saved['objects']['cakood']['uiDocument']=576
    saved['objects']['sceneDialogue']['sdDocument']=576
   else:
    offset=next(x['word_offset'] for x in h.vm.abi['modules']['985']['locals'] if x['name']=='hVCSeen')
    saved['locals']['985'][offset+63]=1
   restore(h,saved,[{'type':4,'message':13},{}])
   self.assertEqual((r.p['hFailure'],h.p['uiFailure']),(28,10));self.assertEqual(v.call('vcRead',92),7)
   self.assertEqual((a.p['played'],a.p['lane'],a.p['pendingLaugh']),(played,0,0))
   self.assertEqual(r.call('p05Flags'),3);self.assertEqual(r.p['hPARoom'],5)
 def test_missing_second_intro_unit_aborts_domain_and_p05_request(self):
  h,d,a,p,q,r,v=prepared();p05=list(r.arrays['p05Words']);contest=list(v.arrays['vcWords'])
  count=d.arrays['sdCounts'][855];d.arrays['sdCounts'][855]=0
  act(h,6,28);h.call('uiHostChoice',211,4)
  self.assertEqual(list(v.arrays['vcWords']),contest);self.assertEqual(list(r.arrays['p05Words']),p05)
  self.assertEqual((v.p['vcBusy'],r.p['p05Busy'],h.p['bridgeQueueCount']),(0,0,0))
  self.assertEqual(r.p['hFailure'],40);self.assertEqual(r.call('hSaveReady'),0)
  d.arrays['sdCounts'][855]=count;h.call('uiHostChoice',211,4);self.assertEqual(v.call('vcRead',6),0)
 def test_loan_second_queue_failure_rolls_back_both_publications(self):
  h,d,a,p,q,r,v=taught();win(h,v);before=list(r.arrays['p05Words']);old_count=d.arrays['sdCounts'][467];fired=[]
  def fault(obj,name,args,result):
   if obj.name=='cakood' and name=='p05Queue' and tuple(args)==(46,) and result==1 and not fired:
    fired.append(True);d.arrays['sdCounts'][467]=0
  h.vm.after_actual_call=fault
  act(h,6,28);h.call('uiHostChoice',211,5);h.vm.after_actual_call=None;d.arrays['sdCounts'][467]=old_count
  self.assertEqual(fired,[True]);self.assertEqual(list(r.arrays['p05Words']),before)
  self.assertEqual((r.p['hPARoom'],r.p['hCartRoom'],h.p['bridgeQueueCount'],r.p['p05Busy']),(5,5,0,0))
  self.assertEqual(r.call('p05Flags'),3)
  self.assertNotEqual(r.p['hFailure'],0);self.assertEqual(r.call('hSaveReady'),0)
  h.call('uiHostChoice',211,5);self.assertEqual(r.call('p05Flags'),3)
 def test_prepared_loan_rejects_reentrant_input_and_save(self):
  h,d,a,p,q,r,v=taught();win(h,v);fired=[]
  def probe(obj,name,args,result):
   if obj.name=='p05State' and name=='p05PrepareLoan' and r.p['p05Busy'] and not fired:
    fired.append(True);before=list(r.arrays['p05Words']);candidate=list(r.arrays['p05Stage']);position=h.p['location']
    for method,a1 in [('hostActNow',(0,17,0)),('uiHostChoice',(217,25)),('uiHostChoice',(211,5)),('writeSave',()),('readSave',())]:h.call(method,*a1)
    self.assertEqual(list(r.arrays['p05Words']),before);self.assertEqual(list(r.arrays['p05Stage']),candidate);self.assertEqual(h.p['location'],position)
  h.vm.after_actual_call=probe;act(h,6,28);choice(h,211,5);h.vm.after_actual_call=None
  self.assertEqual(fired,[True]);self.assertEqual(r.call('p05Flags'),7)
  self.assertEqual(h.vm.kernel_attempts['SaveGame'],0);self.assertEqual(h.vm.kernel_attempts['RestoreGame'],0)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Contest))
 report=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,failures=[(str(t),s) for t,s in result.failures],errors=[(str(t),s) for t,s in result.errors],instructions=sum(v.steps for v in VMS),frames=sum(v.frames for v in VMS),receipts=sum(len(getattr(v,'receipts',[])) for v in VMS),native_acceptance=False)
 (H/'evidence/contest-host-tests.json').write_text(json.dumps(report,indent=2)+'\n');raise SystemExit(not result.wasSuccessful())
