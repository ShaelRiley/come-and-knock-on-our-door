"""New bounded serial, save trust-boundary and emitted guard checks."""
import unittest,json,copy,tempfile,os
from test_domain import Harness,PairedVM,P13World,M,CO,C,P,K,D,L,B,oid,ORDER,POT,DISPLAY,encode_world,encode_save,decode_words,HERE
from paired import restore_words
from harness import EmittedDomain
MEASUREMENTS=[]
class FiniteTests(unittest.TestCase):
 def test_every_mutating_boundary_exhausts_atomically(self):
  h=Harness();cases=[]
  def action(model,native,*args,c=C):
   native_args=args
   if model=='start':native_args=(oid('hotpot_pot'),M['rooms']['L02_KITCHEN'],1,8,1,1,oid('folded_display'),oid('handcart'),M['rooms']['L04_SIDE_PASSAGE'],1,1,1,1,1,0,0,13)
   elif model in ('give_program','deliver_pot','deliver_display','deliver_board'):native_args=(M['routes'][args[0] if args else {'give_program':'house_doorway','deliver_pot':'kitchen_hatch','deliver_display':'side_gate','deliver_board':'house_doorway'}[model]],)
   elif model=='begin_presentation':native_args=(M['sources'][args[0]],)
   cases.append((h.w.save(),c,native,native_args,None));h.action(model,native,*args,c=c)
  def show(s,c=C):
   action('begin_presentation','p13Begin',s,c=c);cases.append((h.w.save(),c,'p13Acknowledge',(),s));h.ack(s,record=h.w.SOURCES[s],c=c)
  action('start','p13Handoff',POT,DISPLAY);action('give_program','p13GiveProgram','kitchen_hatch',c=P);show('wrong_people',P)
  cases.append((h.w.save(),P,'p13AcknowledgeWrongVisual',(), 'visual'));h.visual(P)
  action('claim_laugh','p13ClaimLaugh',c=P);action('give_program','p13GiveProgram',c=P);action('confirm_seating','p13ConfirmSeating')
  action('deliver_pot','p13DeliverPot',c=K);action('pull_serve','p13PullServe');show('rita_ready');action('deliver_display','p13DeliverDisplay',c=D);action('open_screen','p13OpenScreen');show('reveal');action('pull_show','p13PullShow');action('deliver_board','p13DeliverBoard',c=L)
  action('request_contest','p13RequestContest',c=B);cases.append((h.w.save(),B,'p13FinishContestRequest',(),'contest'));h.request_finish(True)
  show('attention',B);action('pull_toast','p13PullToast',c=B)
  for cue in ORDER:cases.append((h.w.save(),B,'p13AcknowledgeAutosave',(),cue));h.save_ack(cue)
  for saved,c,native,args,s in cases:
   saved['state']['revision']=M['max_serial'];v=Harness(PairedVM,P13World.load(saved));v.project(c)
   if native=='p13Acknowledge':
    p=v.w.presentations[s];v.v.call('p13Resume',M['sources'][s]);args=(M['sources'][s],*divmod(p.serial,32768),v.epoch,M['line_ids'][v.w.SOURCES[s]],0,0)
   elif s=='visual':args=(*divmod(v.w.wrong_at,32768),v.epoch)
   elif s=='contest':args=(*divmod(v.w.contest_request_at,32768),v.epoch,1)
   elif s in ORDER:
    q=next(q for q in v.w.pending_autosaves if q['cue']==s);args=(M['words'][s],*divmod(q['serial'],32768),v.epoch,1)
   before=v.v.persistent();v.v.call(native,*args);self.assertEqual(CO[v.v.p['p13Code']],'serial_exhausted',native);self.assertEqual(v.v.persistent(),before);self.assertEqual(v.v.p['p13EventCount'],0)
  MEASUREMENTS.append(dict(gate='mutation_capacity_atomicity',boundaries=len(cases)))
 def test_serial_limb_carry_and_last_handoff(self):
  for revision in (32766,32767,32768,65535,65536,M['max_serial']-1):
   h=Harness(PairedVM,P13World(revision=revision));h.start();self.assertEqual(h.w.revision,revision+1);h.restore();h.queries()
  MEASUREMENTS.append(dict(gate='serial_carry',cases=6))
 def test_pending_save_io_failure_then_verified_success_and_boolean_trust(self):
  h=Harness(PairedVM);h.finish();h.project(B)
  with tempfile.TemporaryDirectory() as td:
   root=__import__('pathlib').Path(td)
   for q in tuple(h.w.pending_autosaves):
    args=(M['words'][q['cue']],*divmod(q['serial'],32768),h.epoch);before=h.v.persistent()
    with self.assertRaises(OSError):(root/'absent'/'save.json').write_text(json.dumps(h.w.save()))
    h.v.call('p13AcknowledgeAutosave',*args,0);self.assertEqual(CO[h.v.p['p13Code']],'autosave_failed');self.assertEqual(h.v.persistent(),before)
    for invalid in (-1,2,32767):
     h.v.call('p13AcknowledgeAutosave',*args,invalid);self.assertEqual(CO[h.v.p['p13Code']],'invalid_argument');self.assertEqual(h.v.persistent(),before)
    target=root/(q['cue']+'.json')
    with target.open('w') as f:json.dump(h.w.save(),f);f.flush();os.fsync(f.fileno())
    self.assertEqual(P13World.load(json.loads(target.read_text())).save(),h.w.save());h.save_ack(q['cue'])
   self.assertFalse(h.w.pending_autosaves)
  # The finite ABI trusts success=1. It cannot establish that native SaveGame
  # actually succeeded; the test above acts as the correctly behaving caller.
  MEASUREMENTS.append(dict(gate='autosave_caller_contract',actual_temporary_files=3,native_savegame=False,success_boolean_is_trusted=True))
 def test_all_ordinary_save_snapshots_restart_actual_bytecode(self):
  from test_validation import snapshots
  states=snapshots()
  for s in states:
   words=list(encode_save(s).values());v=restore_words(words);self.assertEqual(decode_words(list(v.persistent().values())),s);self.assertEqual(v.p['p13ContextValid'],0)
   self.assertEqual(v.p['p13EventCount'],0);self.assertEqual(v.p['p13PresentationSource'],0)
  MEASUREMENTS.append(dict(gate='ordinary_save_transport',reachable_snapshots=len(states)))
 def test_emitted_bad_opcode_stack_packet_and_strict_arity_rejected(self):
  from host_vm import VMError
  v=PairedVM()
  for args in ((),(1,2),(True,),('1',),(1.0,),(32768,),(-32769,)):
   with self.assertRaises(ValueError):v.call('p13Hint',*args)
  for opcode,needle in ((29,'Operand stack underflow'),(32,'Unsupported opcode')):
   d=EmittedDomain();vm=d.vm;m,pc=vm.resolve(d.object,'p13Ready');vm.method_boundaries(m,pc);_,_,end=vm.decode(m,pc);m.decoded[pc]=(opcode,[],end)
   with self.assertRaisesRegex(VMError,needle):d.call('p13Ready')
  d=EmittedDomain();sel=next(i for i,n in d.vm.names.items() if n=='p13Ready')
  with self.assertRaisesRegex(VMError,'Send argument count'):d.vm.send(d.object,[sel,1])
if __name__=='__main__':unittest.main()
