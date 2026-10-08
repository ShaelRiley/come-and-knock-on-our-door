"""Emitted save validator parity, corrupt transport and restore boundaries."""
from test_domain import (P11World,C,ENGAGED,replace,SIDE_PASSAGE,RECORD_UNITS,M,encode_world,encode_save,decode_words,Compiled,source_vm,HERE,hashlib,json,unittest,copy,itertools,ByteVM,Harness,CO)

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

def model_verdict(p):
 try:
  data=decode_words([p[k] for k in M['persisted_properties']])
  if encode_save(data)!=p:return 0
  P11World.load(data);return 1
 except (ValueError,TypeError,KeyError):return 0

class ValidationTests(unittest.TestCase):
 def test_compiled_validator_against_model_corruption_matrix(self):
  valid=snapshots();corpus=[('reachable',p) for p in valid]
  seeds=[valid[0],valid[len(valid)//2],max(valid,key=lambda p:sum(bool(v) for v in p.values()))]
  for seed in seeds:
   for key in M['persisted_properties']:
    for value in (-1,0,1,2,32767):
     p=seed.copy();p[key]=value;corpus.append((key+'='+str(value),p))
  for a,b in itertools.combinations(range(11,len(M['serials'])),2):
   if (a+b)%11:continue
   p=seeds[-1].copy()
   for limb in ('Hi','Lo'):p['p11'+M['serials'][a]+limb]=p['p11'+M['serials'][b]+limb]
   corpus.append((f'collision-{a}-{b}',p))
  machine=Compiled(HERE,993,source_vm.DEFAULTS);seen=set();accepted=rejected=0
  for label,p in corpus:
   key=tuple(p.values())
   if key in seen:continue
   seen.add(key);expected=model_verdict(p);props=source_vm.DEFAULTS.copy();props.update(p);actual=machine.execute('p11Validate',props)
   if actual!=expected:
    machine.trace=[];machine.execute('p11Validate',props)
    (HERE/'evidence/validation-failure.json').write_text(json.dumps(dict(label=label,expected=expected,actual=actual,properties=p,trace=machine.trace),indent=2))
   self.assertEqual(actual,expected,(label,p));accepted+=expected;rejected+=not expected
  report=dict(scope='Emitted SCI1.1 validator versus unchanged Python model, not native gameplay',reachable_snapshots=len(valid),unique_checks=len(seen),accepted=accepted,rejected=rejected,strict_stack_balance=True,executed_instructions=machine.steps,compiled_sha256=hashlib.sha256(machine.blob).hexdigest(),mismatches=0)
  (HERE/'evidence/compiled-validation.json').write_text(json.dumps(report,indent=2)+'\n')
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
 def test_corrupt_restore_clears_all_callbacks_and_fails_closed(self):
  for typ in (source_vm.VM,ByteVM):
   h=Harness(typ);c=h.rescue();h.show('sincere',c);h.action('request_contest','p11RequestContest',c=c);h.v.p['p11CatchLo']=0;h.v.p['p11CatchHi']=0
   self.assertEqual(h.v.call('p11AfterRestore'),0);self.assertEqual(h.v.p['p11ContextValid'],0);self.assertEqual(h.v.p['p11EventCount'],0);self.assertEqual(h.v.p['p11PresentationSource'],0)
   for method in ('p11Lift','p11SetBack','p11RequestContest','p11ClaimLaugh'):
    before=h.v.persistent();h.v.call(method);self.assertEqual(CO[h.v.p['p11Code']],'invalid_state');self.assertEqual(h.v.persistent(),before)

if __name__=='__main__':unittest.main()
