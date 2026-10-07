"""R2 ownership-order regressions. The literal model is never modified.
Key-only reordering is ordinary persistence of a valid reference save.
"""
from copy import deepcopy
from itertools import permutations
import json,unittest
from adapter import *
from cakood.p08_model import P08World as Reference,PREPARATIONS,COURTYARD
C=P08Context(COURTYARD,flags=PREPARATIONS,carrier_padding='clean_towel',frankie_room=COURTYARD,bunny_room=COURTYARD)
BACKENDS=(FastSourceWorld,FastEmittedWorld)
METRICS={'sorted_reproductions':0,'permutation_cases':0,'pending_queue_comparisons':0,'ordered_ack_events':0,'raw_roundtrips':0,'continuation_cases':0,'continuation_actions':0,'raw_rejections':0,'atomic_order_cases':0}
KEYS={'ceramic_carrier':1,'pa_kit':2,'completed_screen':3,'credit_slate':5,'padding':22}
def snapshot(w):return w._state() if isinstance(w,SciWorld) else w.save()['state']
def prepare_all():
 w=Reference()
 for key,pos in [('credit_slate',1),('pa_kit',2),('completed_screen',3),('ceramic_carrier',1),('serving_table',1)]:w.place(C,key,pos)
 w.unpack_service(C);return w

def reordered(data,order):
 data=deepcopy(data);d=data['state']['ownership_serials'];data['state']['ownership_serials']={k:d[k] for k in order}
 return json.loads(json.dumps(data))
def raw_restore(w):
 frame=[w.vm.call('p08SaveWord',i) for i in range(len(M['header'])+M['state_words'])]
 new=type(w)();assert new.vm.call('p08LoadBegin')==1
 for i,value in enumerate(frame):assert new.vm.call('p08LoadWord',i,value)==1
 assert new.vm.call('p08LoadFinish',0)==M['codes']['restored']
 new.session=(*pair(next(SESSION)),0,0,0,0,0,1);assert new.vm.call('p08BindSession',*new.session)==1
 METRICS['raw_roundtrips']+=1
 return new

class OrderTests(unittest.TestCase):
 def compare_queue(self,ref,world):
  self.assertEqual(world.pending_handoffs,ref.pending_handoffs)
  self.assertEqual(list(world.ownership_serials.items()),list(ref.ownership_serials.items()))
  self.assertEqual(snapshot(world),snapshot(ref));METRICS['pending_queue_comparisons']+=1
 def act(self,ref,world,name,*args):
  expected=getattr(ref,name)(*args);actual=getattr(world,name)(*args)
  self.assertEqual(actual,expected);self.compare_queue(ref,world);METRICS['continuation_actions']+=1
  return actual
 def test_review_sorted_pending_reproduction_and_ordered_ack_receipts(self):
  ref=Reference();ref.place(C,'credit_slate',1);ref.place(C,'ceramic_carrier',1)
  saved=json.loads(json.dumps(ref.save(),sort_keys=True))
  for cls in BACKENDS:
   r=Reference.load(saved,C);w=cls.load(saved,C);self.compare_queue(r,w)
   self.assertEqual([h['object_id'] for h in w.pending_handoffs],['ceramic_carrier','credit_slate'])
   for claim in tuple(r.pending_handoffs):
    a=r.acknowledge_handoff(claim['handoff_id'],claim['serial']);b=w.acknowledge_handoff(claim['handoff_id'],claim['serial']);self.assertEqual(a,b);METRICS['ordered_ack_events']+=1
   self.assertEqual(w.acknowledged_handoffs,{'ceramic_carrier':3,'credit_slate':4});self.compare_queue(r,w);METRICS['sorted_reproductions']+=1
 def test_all_120_key_permutations_each_pending_partial_and_fully_acked_prefix(self):
  base=prepare_all().save()
  for order in permutations(base['state']['ownership_serials']):
   for ack_count in range(6):
    r=Reference.load(reordered(base,order),C)
    for claim in r.pending_handoffs[:ack_count]:r.acknowledge_handoff(claim['handoff_id'],claim['serial'])
    saved=json.loads(json.dumps(r.save()));pending=tuple(r.pending_handoffs)
    events=[r.acknowledge_handoff(x['handoff_id'],x['serial']) for x in pending]
    for cls in BACKENDS:
     w=cls.load(saved,C);before=Reference.load(saved,C);self.compare_queue(before,w)
     self.assertEqual(set(w.__dict__),{'vm','session'})
     w=raw_restore(w);self.compare_queue(before,w)
     actual=[w.acknowledge_handoff(x['handoff_id'],x['serial']) for x in w.pending_handoffs]
     self.assertEqual(actual,events);METRICS['ordered_ack_events']+=len(actual)
     self.compare_queue(r,w)
    METRICS['permutation_cases']+=1
  self.assertEqual(METRICS['permutation_cases'],720)
 def test_sorted_and_permuted_loads_then_new_transfers_and_evening_continuation(self):
  for order in [('credit_slate','ceramic_carrier'),('ceramic_carrier','credit_slate')]:
   for ack_count in range(3):
    for mode in ('preserve','sorted','reverse'):
     r=Reference();r.place(C,'credit_slate',1);r.place(C,'ceramic_carrier',1);r=Reference.load(reordered(r.save(),order),C)
     for claim in r.pending_handoffs[:ack_count]:r.acknowledge_handoff(claim['handoff_id'],claim['serial'])
     saved=r.save()
     if mode=='sorted':saved=json.loads(json.dumps(saved,sort_keys=True))
     elif mode=='reverse':saved=reordered(saved,list(reversed(saved['state']['ownership_serials'])))
     else:saved=json.loads(json.dumps(saved))
     for cls in BACKENDS:
      ref=Reference.load(saved,C);w=cls.load(saved,C);self.compare_queue(ref,w);w=raw_restore(w)
      for name,args in [('place',(C,'pa_kit',2)),('place',(C,'completed_screen',3)),('place',(C,'serving_table',1)),('unpack_service',(C,))]:
       self.act(ref,w,name,*args);w=raw_restore(w);self.compare_queue(ref,w)
      # Acknowledged old keys remain in the full order; new transfers append.
      self.assertEqual(list(w.ownership_serials),list(saved['state']['ownership_serials'])+['pa_kit','completed_screen','padding'])
      for claim in tuple(ref.pending_handoffs):self.act(ref,w,'acknowledge_handoff',claim['handoff_id'],claim['serial']);METRICS['ordered_ack_events']+=1
      for name,args in [('request_start',(C,)),('acknowledge_readiness',(C,'P08:START:1',READINESS_RECORDS)),('confirm_start',(C,'P08:START:1',True)),('acknowledge_autosave',(C,'P08:START:1',False)),('retry_autosave',(C,'P08:START:1')),('acknowledge_autosave',(C,'P08:START:1',True)),('place',(C,'serving_table',4)),('place',(C,'serving_table',1))]:self.act(ref,w,name,*args)
      w=raw_restore(w);self.compare_queue(ref,w);self.assertTrue(w.evening_started);METRICS['continuation_cases']+=1
 def test_order_is_saved_in_sci_words_and_all_pending_accessors_are_bounded(self):
  self.assertEqual(M.get('raw_save_schema'),2);self.assertEqual(M['state_words'],88);self.assertEqual(M['header'][:4],[20536,2,32,88])
  saved=prepare_all().save();order=['padding','pa_kit','credit_slate','completed_screen','ceramic_carrier'];saved=reordered(saved,order)
  for cls in BACKENDS:
   w=cls.load(saved,C);words=w.vm.arrays['p08Words'];self.assertEqual(words[F['owner_order_count']],5);self.assertEqual(words[F['owner_order_0']:F['owner_order_0']+5],[KEYS[k] for k in order])
   self.assertEqual([w.vm.call('p08PendingKey',i) for i in range(5)],[KEYS[k] for k in order])
   for index in (-32768,-1,5,6,32767):self.assertEqual(w.vm.call('p08PendingKey',index),0)
   w=raw_restore(w);self.assertEqual(list(w.ownership_serials),order)
 def test_invalid_order_metadata_and_r1_raw_schema_are_rejected_without_live_changes(self):
  self.assertIn('owner_order_count',F)
  r=Reference();r.place(C,'credit_slate',1);r.place(C,'ceramic_carrier',1);saved=r.save()
  variants=[('count_negative','owner_order_count',-1),('count_too_large','owner_order_count',6),('count_missing_claim','owner_order_count',1),('zero_live_key','owner_order_0',0),('duplicate_key','owner_order_1',5),('foreign_key','owner_order_0',4),('absent_claim','owner_order_0',22),('tail_key','owner_order_2',3)]
  for cls in BACKENDS:
   w=cls.load(saved,C);before=list(w.vm.arrays['p08Words']);frame=M['header']+before
   for name,field,value in variants:
    candidate=list(frame);candidate[20+F[field]]=value;self.assertEqual(w.vm.call('p08LoadBegin'),1)
    for i,v in enumerate(candidate):self.assertEqual(w.vm.call('p08LoadWord',i,v),1)
    self.assertEqual(w.vm.call('p08LoadFinish',0),M['codes']['invalid_state'],name);self.assertEqual(w.vm.arrays['p08Words'],before);METRICS['raw_rejections']+=1
   old_header=list(M['header']);old_header[1]=1;old_header[3]=82;self.assertEqual(w.vm.call('p08LoadBegin'),1);self.assertEqual(w.vm.call('p08LoadWord',0,old_header[0]),1);self.assertEqual(w.vm.call('p08LoadWord',1,old_header[1]),0);self.assertEqual(w.vm.arrays['p08Words'],before);METRICS['raw_rejections']+=1
 def test_order_append_is_atomic_and_reversal_or_ack_does_not_reorder(self):
  self.assertIn('owner_order_count',F)
  for cls in BACKENDS:
   w=cls();before=list(w.vm.arrays['p08Words']);w._context(C);w.vm.call('p08Place',5,1,0)
   self.assertEqual(w.vm.call('p08CandidateWord',F['owner_order_count']),1);self.assertEqual(w.vm.call('p08CandidateWord',F['owner_order_0']),5);self.assertEqual(w.vm.arrays['p08Words'],before)
   self.assertEqual(w.vm.call('p08Abort'),1);self.assertEqual(w.vm.arrays['p08Words'],before)
   w._context(C);w.vm.call('p08Admission',3,6,1);self.assertEqual(w.vm.call('p08Place',5,1,0),M['codes']['output_full']);self.assertEqual(w.vm.arrays['p08Words'],before)
   w.vm.call('p08Admission',3,6,2);w.place(C,'credit_slate',1);w.place(C,'ceramic_carrier',1)
   order=w.vm.arrays['p08Words'][F['owner_order_count']:]
   w.place(C,'credit_slate',4);claim=w.pending_handoffs[0];w.acknowledge_handoff(claim['handoff_id'],claim['serial']);self.assertEqual(w.vm.arrays['p08Words'][F['owner_order_count']:],order)
   METRICS['atomic_order_cases']+=1
