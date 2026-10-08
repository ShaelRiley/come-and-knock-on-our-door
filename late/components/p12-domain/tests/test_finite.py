"""New bounded P12 serial, authority, live receipt and evaluator probes."""
import copy,json,itertools,hashlib,unittest
from dataclasses import replace
from test_domain import Harness,C,A,RACK,RIG,M,CO,oid,P12World,TILE_IDS,ORDER,PEOPLE,LIVING,encode_world,encode_save,decode_words,HERE
from paired import PairedVM,MEASUREMENTS as COUNTERS
from harness import EmittedDomain,source_base
MEASUREMENTS=[]
class FiniteTests(unittest.TestCase):
 def test_serial_limb_carry_and_last_handoff_commit(self):
  for revision in (32766,32767,32768,65535,65536,M['max_serial']-1,M['max_serial']):
   h=Harness(PairedVM,P12World(revision=revision));h.project();before=h.v.persistent()
   if revision<M['max_serial']:
    h.start();self.assertEqual(h.w.revision,revision+1);h.restore();h.queries()
   else:
    h.v.call('p12Handoff',oid('cue_rack'),4,0,1,*[oid(x) for x in TILE_IDS],1,2,3)
    self.assertEqual(CO[h.v.p['p12Code']],'serial_exhausted');self.assertEqual(h.v.persistent(),before)
   h.action('hint','p12Hint',1);h.v.call('p12AudioFinished');h.check(h.w.audio_finished())
  MEASUREMENTS.append(dict(gate='serial_limb_and_last_handoff',cases=7))

 def test_every_mutating_boundary_exhausts_without_partial_state(self):
  # All snapshots are reached by ordinary play. Only the serial capacity is
  # advanced, a supported reference posture; no fabricated completion facts.
  base=Harness();cases=[]
  def action(model,native,*args,c=C):
   native_args=args
   if model=='start':native_args=(oid('cue_rack'),4,0,1,*[oid(x) for x in TILE_IDS],1,2,3)
   elif model=='begin_presentation':native_args=(M['sources'][args[0]],)
   elif model=='order_cards':native_args=tuple(oid(x) for x in args[0])
   cases.append((base.w.save(),c,native,native_args,None));base.action(model,native,*args,c=c)
  def show(s,c=C):
   action('begin_presentation','p12Begin',s,c=c)
   p=base.w.presentations[s]
   cases.append((base.w.save(),c,'p12Acknowledge',(),s));base.ack(s,record=base.w.SOURCES[s],c=c)
  action('start','p12Handoff',RACK);show('self_view',A)
  action('release_catch','p12ReleaseCatch',c=A);action('rotate_rack','p12Rotate');action('order_cards','p12Order',TILE_IDS)
  show('introduction');action('commit_introduction','p12CommitIntroduction');action('release_confetti','p12ReleaseConfetti');show('confetti')
  action('claim_laugh','p12ClaimLaugh');show('cleanup');action('finish_welcome','p12FinishWelcome')
  for save,c,native,args,source in cases:
   save['state']['revision']=M['max_serial'];h=Harness(PairedVM,P12World.load(save));h.project(c)
   if source:
    sid=M['sources'][source];p=h.w.presentations[source];h.v.call('p12Resume',sid)
    args=(sid,*divmod(p.serial,32768),h.epoch,M['line_ids'][h.w.SOURCES[source]],0,0)
   before=h.v.persistent();h.v.call(native,*args)
   self.assertEqual(CO[h.v.p['p12Code']],'serial_exhausted',native);self.assertEqual(h.v.persistent(),before,native)
   self.assertEqual(h.v.p['p12EventCount'],0,native)
  MEASUREMENTS.append(dict(gate='all_mutating_boundaries_at_capacity',cases=len(cases)))

 def test_last_receipt_duplicate_and_commit_barriers(self):
  for source in ('introduction','confetti','cleanup'):
   h=Harness(PairedVM);h.repair()
   if source!='introduction':h.show('introduction');h.action('commit_introduction','p12CommitIntroduction');h.action('release_confetti','p12ReleaseConfetti')
   if source=='cleanup':h.show('confetti')
   h.begin(source);tokens=h.w._tokens(source);h.ack(source,units=tokens[:-1])
   h.w.revision=M['max_serial']-1;h.v.p.update(encode_world(h.w));h.ack(source,units=tokens[-1:]);h.restore()
   self.assertEqual(h.w.revision,M['max_serial']);before=h.v.persistent();h.ack(source,units=tokens[-1:]);self.assertEqual(h.v.persistent(),before)
   self.assertFalse(h.w.welcome_cleared)
   h.v.call('p12CommitIntroduction' if source=='introduction' else 'p12FinishWelcome')
   self.assertEqual(CO[h.v.p['p12Code']],'cleanup_text_required' if source=='confetti' else 'serial_exhausted')
   self.assertEqual(h.v.persistent(),before)

 def test_epoch_exhaustion_and_explicit_callback_retirement(self):
  h=Harness(PairedVM);h.epoch=32765;h.start();h.begin('opening')
  p=h.w.presentations['opening'];old=(M['sources']['opening'],*divmod(p.serial,32768),h.epoch,M['line_ids'][h.w.SOURCES['opening']],0,0)
  h.project(replace(C,rig=replace(RIG,source='TAPE')));self.assertEqual(h.v.p['p12Epoch'],32767)
  args=[4,0,1,1,1,1,4,1,1,1,0,1,*([4]*7),32767];before=h.v.persistent()
  self.assertEqual(h.v.call('p12Context',*args),0);self.assertEqual(h.v.persistent(),before)
  self.assertEqual(h.v.p['p12ContextValid'],0);self.assertEqual(h.v.arrays['p12Lease'],[0]*12)
  with self.assertRaises(ValueError):h.v.call('p12Context',*args[:-1],32768)
  h.restore();h.epoch=0;h.resume('opening');before=h.v.persistent()
  h.v.call('p12Acknowledge',*old);self.assertEqual(CO[h.v.p['p12Code']],'stale_presentation');self.assertEqual(h.v.persistent(),before)
  h.ack('opening',record=h.w.SOURCES['opening'])

 def test_strict_source_emitted_arity_stack_opcode_and_bounds(self):
  v=PairedVM()
  for args in ((),(1,2),(True,),('1',),(1.0,),(32768,),(-32769,)):
   with self.assertRaises(ValueError):v.call('p12Hint',*args)
  with self.assertRaises(ValueError):v.call('not_a_method')
  with self.assertRaises(AssertionError):v.source.ev(source_base.Array(['p12Lines',3]),{})
  with self.assertRaises(ValueError):v.source.ev(['made_up_opcode'],{})
  from host_vm import VMError
  for opcode,needle in ((29,'Operand stack underflow'),(32,'Unsupported opcode')):
   d=EmittedDomain();vm=d.vm;m,pc=vm.resolve(d.object,'p12Ready');vm.method_boundaries(m,pc)
   _,_,end=vm.decode(m,pc);m.decoded[pc]=(opcode,[],end)
   with self.assertRaisesRegex(VMError,needle):d.call('p12Ready')
  d=EmittedDomain();selector=next(i for i,n in d.vm.names.items() if n=='p12Ready')
  with self.assertRaisesRegex(VMError,'Send argument count'):d.vm.send(d.object,[selector,1])

 def test_current_authority_all_fields_and_exact_original_methods(self):
  from verify_source import verify
  info=verify();self.assertEqual(info['literal_methods'],59)
  self.assertEqual(len(M['persisted_properties']),102);self.assertEqual(len(M['serials']),46)
  self.assertEqual([M['objects'][x] for x in ('completed_screen','courtyard_plan','screen_token','clip_marks','handcart','folded_display')],[81,83,80,84,72,42])
  self.assertEqual([M['objects'][x] for x in TILE_IDS],[48,49,50])
  self.assertEqual(M['own_objects'],{'swivel_release_catch':419,'rack_rotating_handle':420})
  root=HERE/'reference/component';cat=json.loads((root/'authority/full-line-catalog.json').read_text())['records'];units=json.loads((root/'authority/speech-units.json').read_text())['units']
  self.assertEqual(M['canonical_records'],{r['id']:r for r in cat if r['id'].startswith('P12.') or r['id']=='VC03.NEED_RESOLUTION'})
  self.assertEqual(M['speech_metadata'],[u for u in units if u['record_id'].startswith('P12.')])
  self.assertEqual((len(M['canonical_records']),len(M['speech_metadata'])),(30,36))
  MEASUREMENTS.append(dict(gate='authority_methods_and_abi',**info))

 def test_every_named_speaker_rechecked_for_actual_receipt(self):
  stages={};base=Harness();base.start()
  for source in M['sources']:
   if source in ('introduction','confetti','cleanup'):continue
   stages[source]=base.w.save()
  base.repair();stages['introduction']=base.w.save();base.show('introduction');base.action('commit_introduction','p12CommitIntroduction');base.action('release_confetti','p12ReleaseConfetti');stages['confetti']=base.w.save();base.show('confetti');stages['cleanup']=base.w.save()
  count=0
  for source,data in stages.items():
   c=A if source in ('audience_view','self_view','catch','rehearsal') else C
   for index,token in enumerate(P12World()._tokens(source)):
    speaker=P12World.SPEAKERS.get(token)
    if speaker not in PEOPLE[1:]:continue
    h=Harness(PairedVM,P12World.load(data));h.begin(source,c)
    tokens=h.w._tokens(source)
    if index:h.ack(source,units=tokens[:index],c=c)
    away=replace(c,npc_locations=tuple((p,LIVING if p==speaker else room) for p,room in c.npc_locations));before=h.v.persistent()
    self.assertEqual(h.ack(source,units=(token,),c=away).code,'speaker_absent');self.assertEqual(h.v.persistent(),before)
    self.assertEqual(h.ack(source,units=(token,),c=c).code,'presentation_acknowledged');count+=1
  self.assertEqual(count,13);MEASUREMENTS.append(dict(gate='live_named_speaker_receipts',cases=count,paired_totals=dict(COUNTERS)))

if __name__=='__main__':unittest.main()
