"""Retained strict transport case and reachable snapshots; no corruption matrix run."""
from test_domain import (P11World,C,ENGAGED,replace,SIDE_PASSAGE,RECORD_UNITS,M,encode_world,encode_save,decode_words,source_vm,HERE,json,unittest,copy,Harness,CO)
from test_adaptations import PairedVM
MEASUREMENTS=[]
def snapshots():
 out=[]
 def add(w):out.append(encode_world(w))
 w=P11World();add(w);w.hint(C,2);add(w);w.lift(C);add(w)
 for source in ('intro','wing','peg','catch','concern','sincere'):
  r=w.begin_presentation(C,source);add(w)
  for u in w._tokens(source):w.acknowledge_presentation(C,r.presentation_id,speech_unit_ids=(u,));add(w)
 w.request_peg(C);add(w);w.acknowledge_peg(ENGAGED,w.pending_peg_request_id);add(w);w.release_catch(ENGAGED);add(w)
 w.set_back(ENGAGED);add(w);w.lift(ENGAGED);add(w);w.release_catch(ENGAGED);add(w);w.pull_handle(ENGAGED);add(w);w.stage_display(ENGAGED);add(w)
 for source in ('fold','staged'):
  c=replace(ENGAGED,rita_room=SIDE_PASSAGE);r=w.begin_presentation(c,source);add(w)
  for u in w._tokens(source):w.acknowledge_presentation(c,r.presentation_id,speech_unit_ids=(u,));add(w)
 w.request_contest(ENGAGED);add(w);w.acknowledge_contest_request(ENGAGED,w.pending_contest_request_id,cancelled=True);add(w);w.claim_laugh(ENGAGED);add(w)
 for revision in (32766,32767,32768,M['max_serial']):
  w=P11World(revision=revision);add(w)
  if revision<M['max_serial']-2:w.lift(C);add(w)
 return out

class TransportTests(unittest.TestCase):
 def test_legitimate_saved_history_roundtrips(self):
  states=snapshots();v=PairedVM()
  for p in states:
   data=json.loads(json.dumps(decode_words(list(p.values()))))
   self.assertEqual(encode_save(data),p);P11World.load(data)
   v.p.update(p);self.assertEqual(v.call('p11AfterRestore'),1)
   self.assertEqual(v.persistent(),p);self.assertEqual(v.p['p11ContextValid'],0)
   self.assertEqual(v.source.arrays['p11Lease'],[0]*9)
  MEASUREMENTS.append(dict(gate='legal_save_history',states=len(states),paired_calls=v.calls,emitted_instructions=v.emitted.machine.steps))
 def test_strict_transport_types_partial_reads_unknown_fields(self):
  pristine=P11World().save()
  for mutation in (lambda d:d.update(schema=True),lambda d:d['state'].update(revision=True),lambda d:d['state'].update(phase=True),lambda d:d['state'].update(hint_level=True),lambda d:d['state'].update(revision=M['max_serial']+1),lambda d:d['state'].update(game_complete=True),lambda d:d['state'].pop('first_lift_at')):
   value=copy.deepcopy(pristine);mutation(value)
   with self.assertRaises(ValueError):encode_save(value)
  w=P11World();w.lift(C);r=w.begin_presentation(C,'sincere');w.acknowledge_presentation(C,r.presentation_id,speech_unit_ids=RECORD_UNITS['P11.DIALOGUE.002'][:2])
  for mutation in (lambda d:d['state']['presentations']['sincere'].update(serial=0),lambda d:d['state']['presentations']['sincere']['receipts'].update({'P11.DIALOGUE.002.01':0}),lambda d:d['state']['presentations']['sincere'].update(receipts={'P11.DIALOGUE.002.02':4,'P11.DIALOGUE.002.01':4})):
   value=w.save();mutation(value)
   with self.assertRaises(ValueError):encode_save(value)
  words=list(encode_world(w).values())
  for value in (True,-1,32768,'0'):
   bad=words.copy();bad[2]=value
   with self.assertRaises(ValueError):decode_words(bad)
  for n in range(len(words)):
   with self.assertRaises(ValueError):decode_words(words[:n])
   with self.assertRaises(ValueError):source_vm.restore_words(words[:n])

if __name__=='__main__':unittest.main()
