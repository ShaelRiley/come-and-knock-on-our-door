"""Observable unchanged-reference, source, emitted and ordinary restore gates."""
from pathlib import Path
from dataclasses import replace
from copy import deepcopy
from itertools import permutations
import json,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
from harness import SourceDomain,EmittedDomain,snapshot
from codec.p09_codec import encode_world,decode_world,select_persisted,encode_context,decode_result,ResultImage,RESULT_PROPERTIES
from reference.cakood.p09_model import P09World,P09Context,CONSERVATORY,CARD,RECORD_UNITS
from reference.cakood.model import Verb
M=json.loads((ROOT/'schema.json').read_text())
C=P09Context(CONSERVATORY,flags=frozenset(('EVENING_STARTED','PLAN_AGREED')))

class Trio:
 def __init__(self,world=None,context=C):
  self.w=world or P09World();self.s=SourceDomain();self.e=EmittedDomain();self.epoch=0
  for d in (self.s,self.e):d.p.update(encode_world(self.w))
  self.context(context)
 def call(self,name,*args):
  a=self.s.call(name,*args);b=self.e.call(name,*args)
  if a!=b:raise AssertionError((name,'return',a,b))
  if snapshot(self.s)!=snapshot(self.e):raise AssertionError((name,'source/emitted state mismatch'))
  return a
 def context(self,c):
  self.c=c;self.epoch+=1;im=encode_context(c,epoch=self.epoch)
  assert self.call('p09Context',*im.arguments)==1
  for i,v in enumerate(im.held):
   if v:assert self.call('p09ContextItem',i)==1
 def image(self):
  p=self.s.p;a=self.s.arrays
  return ResultImage({k:p[k] for k in RESULT_PROPERTIES},tuple(a['p09Lines']),tuple(a['p09Units']),tuple(a['p09Events']),tuple(a['p09EventArgs']))
 def compare(self,expected):
  got=decode_result(self.image())
  assert got==expected,('result',got,expected)
  assert select_persisted(self.s.p)==encode_world(self.w),('state',select_persisted(self.s.p),encode_world(self.w))
  assert decode_world(select_persisted(self.e.p)).save()==self.w.save()
  return expected
 def begin(self,source):
  expected=self.w.begin_presentation(self.c,source);self.call('p09Begin',M['sources'][source]);return self.compare(expected)
 def resume(self,source):
  expected=self.w.resume_presentation(self.c,source);self.call('p09Resume',M['sources'][source]);return self.compare(expected)
 def ack(self,source,record=None,units=(),ticket=None):
  p=self.w.presentations[source];expected=self.w.acknowledge_presentation(self.c,f'P09:{source}:{p.serial}',record_id=record,speech_unit_ids=units)
  hi,lo=divmod(p.serial,32768);args=(M['sources'][source],hi,lo,self.epoch,M['line_ids'].get(record,0),M['speech_unit_ids'].get(units[0],0) if units else 0,M['speech_unit_ids'].get(units[-1],0) if units else 0)
  self.call('p09Acknowledge',*args);return self.compare(expected)
 def acknowledge_pending(self,source,result):
  return self.ack(source,record=result.line_ids[0] if result.line_ids else None,units=result.speech_unit_ids)
 def query(self,method,*args):
  if method=='look':r=self.w.look(self.c,args[0]);self.call('p09Look',M['objects'][args[0]])
  elif method=='topics':r=self.w.topics(self.c);self.call('p09Topics')
  elif method=='hint':r=self.w.hint(self.c,*args);self.call('p09Hint',0 if not args or args[0] is None else args[0])
  elif method=='ask':r=self.w.ask_three_things(self.c);self.call('p09Ask')
  elif method=='act':
   verb,obj,*rest=args;target=rest[0] if rest else None;r=self.w.act(self.c,verb,obj,target)
   self.call('p09Act',list(Verb).index(Verb(verb))+1,M['objects'][obj],M['objects'][target] if target else 0)
  return self.compare(r)
 def observed(self):
  before=deepcopy(self.w.save());records=[];units=[];pending=[]
  for i in range(20):
   r=self.call('p09JournalAt',i,0);u=self.call('p09JournalAt',i,1)
   if r:records.append(next(k for k,v in M['line_ids'].items() if v==r))
   if u:units.append(next(k for k,v in M['speech_unit_ids'].items() if v==u))
  for i in range(9):
   v=self.call('p09PendingAt',i)
   if v:pending.append(next(k for k,n in M['sources'].items() if n==v))
  assert tuple(records)==self.w.journal_records(),('records',records,self.w.journal_records())
  assert tuple(units)==self.w.journal_units(),('units',units,self.w.journal_units())
  assert tuple(pending)==self.w.pending_presentations
  assert decode_world(select_persisted(self.s.p)).save()==before

class ActionGates(unittest.TestCase):
 def test_all_four_correction_routes(self):
  for source in ('chairs','direct_question','front_context','accusation'):
   with self.subTest(source=source):
    t=Trio();r=t.begin(source);self.assertFalse(t.w.rumor_cleared);t.acknowledge_pending(source,r)
    self.assertTrue(t.w.rumor_cleared);earliest=t.w.consumed['P09_RUMOR']
    r=t.begin('terms');r=t.acknowledge_pending('terms',r)
    self.assertTrue(t.w.ready);self.assertEqual(t.w.consumed['P09_RUMOR'],earliest)
    self.assertFalse(t.w.terms_card_handoff['signed']);self.assertIsNone(t.w.terms_card_handoff['repair_date'])
    t.acknowledge_pending('terms',r);t.query('ask');t.query('topics')
 def test_terms_every_unit_and_success_separate(self):
  t=Trio();t.acknowledge_pending('chairs',t.begin('chairs'));t.begin('terms')
  for i,u in enumerate(RECORD_UNITS['P09.DIALOGUE.002']):
   r=t.ack('terms',units=(u,));self.assertEqual(t.w.ready,i==4)
  t.context(replace(C,room='L02_KITCHEN',stringer_room='L01_LIVING_ROOM'))
  r=t.resume('terms');t.acknowledge_pending('terms',r)
  t.query('act',Verb.OPEN,CARD);t.ack('terms_card',record='P09.READ.002')
 def test_partial_accusation_actor_eligibility(self):
  t=Trio();t.begin('accusation');t.ack('accusation',units=('P09.FAILURE.001.01',))
  self.assertFalse(t.w.class_context_known)
  t.context(replace(C,stringer_room='L02_KITCHEN'));r=t.resume('accusation');t.acknowledge_pending('accusation',r)
  self.assertTrue(t.w.class_context_known)
  t=Trio(context=replace(C,rita_room='L02_KITCHEN'));r=t.begin('accusation');t.acknowledge_pending('accusation',r)
  self.assertFalse(t.w.class_context_known);self.assertEqual(t.w.presentations['accusation'].variant,'stringer_only')
  t.context(C);t.begin('accusation');self.assertFalse(t.w.class_context_known)
 def test_admission_views_and_blocks(self):
  for context,source in [(replace(C,flags=frozenset()),'chairs'),(replace(C,on_apron=True),'chairs'),
    (replace(C,contest_active=True),'chairs'),(C,'intro'),(replace(C,conservatory_view='side'),'front_context'),
    (replace(C,stringer_room='L02_KITCHEN'),'direct_question'),(C,'terms'),(C,'shared_wish')]:
   with self.subTest(context=context,source=source):Trio(context=context).begin(source)
  t=Trio();t.acknowledge_pending('chairs',t.begin('chairs'))
  t.context(replace(C,flags=frozenset(('EVENING_STARTED',))));t.begin('terms')
 def test_act_card_protection_and_fixed_tags(self):
  t=Trio();t.query('act',Verb.OPEN,'chair_tag');t.query('act',Verb.PICK_UP,'chair_tag');t.query('act',Verb.TALK_TO,'stringer')
  t.acknowledge_pending('chairs',t.begin('chairs'));t.acknowledge_pending('terms',t.begin('terms'))
  for verb in (Verb.GIVE,Verb.USE,Verb.PUSH,Verb.PULL,Verb.CLOSE,Verb.PICK_UP):t.query('act',verb,CARD)
  t.query('act',Verb.OPEN,CARD)

class ReceiptGates(unittest.TestCase):
 def reject(self,t,source,record=0,first=0,last=0,code='invalid_argument',serial=None,epoch=None):
  before=encode_world(t.w);p=t.w.presentations[source]
  hi,lo=divmod(p.serial if serial is None else serial,32768)
  got=t.call('p09Acknowledge',M['sources'][source],hi,lo,t.epoch if epoch is None else epoch,record,first,last)
  self.assertEqual(got,M['codes'][code]);self.assertEqual(select_persisted(t.s.p),before)
 def test_out_of_order_cross_source_and_stale_receipts(self):
  t=Trio();t.begin('direct_question')
  self.reject(t,'direct_question',first=5,last=5)
  self.reject(t,'direct_question',record=8)
  self.reject(t,'direct_question',record=6,first=4,last=4)
  self.reject(t,'direct_question',first=4,last=3)
  self.reject(t,'direct_question',record=6,serial=2,code='stale_callback')
  t.ack('direct_question',units=('P09.DIALOGUE.001.01',));t.ack('direct_question',record='P09.DIALOGUE.001')
  t.ack('direct_question',record='P09.DIALOGUE.001')
 def test_cannot_cross_terms_outcome_or_expand_restricted_accusation(self):
  t=Trio();t.acknowledge_pending('chairs',t.begin('chairs'));t.begin('terms')
  self.reject(t,'terms',first=9,last=20)
  self.reject(t,'terms',record=17)
  self.assertFalse(t.w.ready)
  t=Trio(context=replace(C,rita_room='L02_KITCHEN'));t.begin('accusation')
  self.reject(t,'accusation',record=8)
  t.ack('accusation',units=('P09.FAILURE.001.01',));self.assertFalse(t.w.class_context_known)
 def test_intro_remains_canceled_after_correction(self):
  t=Trio(context=replace(C,conservatory_view='side'));t.begin('intro');t.acknowledge_pending('chairs',t.begin('chairs'))
  t.resume('intro');t.ack('intro',record='P09.OPEN.001')
  self.assertEqual(t.w.presentations['intro'].receipts,{})
 def test_epoch_reuse_exhaustion_and_partial_actor_blocks(self):
  t=Trio();self.assertEqual(t.call('p09Context',6,0,1,1,6,6,0,0,0,0,t.epoch),0)
  self.assertEqual(t.call('p09Context',6,0,1,1,6,6,0,0,0,0,32767),1)
  self.assertEqual(t.call('p09Context',6,0,1,1,6,6,0,0,0,0,32767),0)
  self.assertEqual(t.call('p09Context',6,0,1,1,6,6,0,0,0,0,-32768),0)
  t=Trio();t.begin('accusation');t.context(replace(C,rita_room='L02_KITCHEN'));t.resume('accusation')
  t.ack('accusation',units=('P09.FAILURE.001.01',))
  self.assertTrue(t.w.rumor_cleared);self.assertFalse(t.w.class_context_known)

class ObservationGates(unittest.TestCase):
 def test_journal_chronology_partial_and_shared(self):
  t=Trio(context=replace(C,conservatory_view='side'));t.begin('intro');t.ack('intro',units=('P09.OPEN.001.01',))
  t.begin('chair_tag');t.ack('chair_tag',record='P09.READ.001');t.context(C)
  t.begin('front_context');t.begin('direct_question');t.ack('direct_question',units=('P09.DIALOGUE.001.01',));t.observed()
  t.ack('front_context',record='P09.DIALOGUE.001');t.begin('shared_wish');t.ack('shared_wish',units=RECORD_UNITS['P09.DIALOGUE.003']);t.observed()
 def test_queries_hints_and_queue_do_not_grant_knowledge(self):
  t=Trio();t.query('look','tagged_chairs');t.query('look','chair_tag');t.query('topics')
  for level in (None,1,3,2,3):t.query('hint',level)
  t.begin('direct_question');t.resume('direct_question');self.assertFalse(t.w.rumor_cleared);self.assertEqual(t.w.journal_records(),())
  t.query('look','audience');t.query('act',Verb.TALK_TO,'audience');t.observed()
 def test_route_orders_earliest_receipt(self):
  # Six independently bounded subcases per group; all 24 orders over this test.
  for order in permutations(('chairs','direct_question','front_context','accusation')):
   with self.subTest(order=order):
    t=Trio()
    for s in order:t.acknowledge_pending(s,t.begin(s))
    self.assertEqual(t.w.consumed['P09_RUMOR'],2)
    for i,r in enumerate(t.w.journal_records()):self.assertEqual(t.call('p09JournalAt',i,0),M['line_ids'][r])

class SaveGates(unittest.TestCase):
 def test_restore_clears_leases_and_pending_success_resumes(self):
  t=Trio();t.acknowledge_pending('chairs',t.begin('chairs'));t.acknowledge_pending('terms',t.begin('terms'))
  saved=encode_world(t.w);serial=t.w.presentations['terms'].serial;old=t.epoch
  self.assertEqual(t.call('p09LoadBegin'),1)
  for i,v in enumerate(saved.values()):self.assertEqual(t.call('p09LoadWord',i,v),1)
  self.assertEqual(t.call('p09LoadCommit'),1)
  self.assertEqual(t.call('p09Acknowledge',7,0,serial,old,17,0,0),M['codes']['invalid_context'])
  t.context(C);self.assertEqual(t.call('p09Acknowledge',7,0,serial,old,17,0,0),M['codes']['stale_callback'])
  self.assertEqual(t.call('p09Acknowledge',7,0,serial,t.epoch,17,0,0),M['codes']['stale_callback'])
  r=t.resume('terms');t.acknowledge_pending('terms',r);t.observed()
 def test_invalid_load_rolls_back_and_rejects_card_forgery(self):
  t=Trio();t.acknowledge_pending('chairs',t.begin('chairs'));before=encode_world(t.w)
  for key,value in [('p09Ready',1),('p09TermsLo',2),('p09RumorLo',1),('p09ChairsReceipt1Lo',1),('p09Restricted',1),('p09Initialized',0)]:
   image=dict(before);image[key]=value;t.call('p09LoadBegin')
   for i,v in enumerate(image.values()):t.call('p09LoadWord',i,v)
   self.assertEqual(t.call('p09LoadCommit'),0,(key,value));self.assertEqual(select_persisted(t.s.p),before)
 def test_canceled_and_context_changed_callbacks(self):
  t=Trio();t.begin('direct_question');serial=t.w.presentations['direct_question'].serial;old=t.epoch
  t.call('p09Invalidate');t.context(C)
  self.assertEqual(t.call('p09Acknowledge',4,0,serial,old,6,0,0),M['codes']['stale_callback'])
  self.assertEqual(t.call('p09Acknowledge',4,0,serial,t.epoch,6,0,0),M['codes']['stale_callback'])
  r=t.resume('direct_question');t.acknowledge_pending('direct_question',r)
 def test_claims_and_external_card_ownership(self):
  t=Trio();t.context(replace(C,flags=C.flags|{'RUMOR_CLEARED'}));self.assertEqual(t.call('p09ValidateContext'),0)
  t.context(C);self.assertEqual(t.call('p09ContextItem',399),0);self.assertEqual(t.call('p09ValidateContext'),0)
  self.assertEqual(t.w.inventory,())

if __name__=='__main__':unittest.main()
