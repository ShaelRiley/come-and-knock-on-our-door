"""Identical domain oracle cases against source and emitted SCI instructions."""
from pathlib import Path
import sys,json,unittest,random,copy,itertools,hashlib
from dataclasses import replace
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
sys.path[:0]=[str(HERE),str(ROOT)]
from cakood.p11_model import P11World,P11Context,RescuePhase,SIDE_PASSAGE,PORCH,COURTYARD,CONSERVATORY,PREREQUISITES,RECORD_UNITS
from cakood.p04_model import GateHandoff
from cakood.model import Verb
from codec import M,encode_world,encode_save,decode_words
import source_vm
from compiled_vm import Compiled
GATE=GateHandoff(peg_id="hold_open_peg",peg_location=SIDE_PASSAGE,plan_line_ids=(),tested=True,peg_available=True,peg_engaged=False,gate_open=True,wedge_in_gate=False)
C=P11Context(SIDE_PASSAGE,GATE,flags=PREREQUISITES)
ENGAGED=replace(C,gate=replace(GATE,peg_engaged=True))
R={v:k for k,v in M['line_ids'].items()};U={v:k for k,v in M['speech_unit_ids'].items()};E={v:k for k,v in M['events'].items()};CO={v:k for k,v in M['codes'].items()};SO={v:k for k,v in M['sources'].items()};O={v:k for k,v in M['objects'].items()}
def oid(obj):return M['objects'].get(obj,32767) if obj else 0

class ByteVM:
 def __init__(self):
  self.machine=Compiled(HERE,993,source_vm.DEFAULTS);self.p=source_vm.DEFAULTS.copy();self.call('p11Init')
 def call(self,name,*args):
  if any(type(x) is not int or not -32768<=x<=32767 for x in args):raise ValueError('SCI arguments require signed words')
  if name not in source_vm.SIGNATURES or len(args)!=source_vm.SIGNATURES[name]:raise ValueError('Invalid method/arity')
  return self.machine.execute(name,self.p,args)
 def persistent(self):return {k:self.p[k] for k in M['persisted_properties']}

class Harness:
 def __init__(self,typ=source_vm.VM,world=None):
  self.w=world or P11World();self.v=typ();self.v.p.update(encode_world(self.w));self.epoch=1;self.context=None
 def project(self,c):
  if self.context==c:return
  self.context=c;self.epoch+=1;g=c.gate
  a=[M['rooms'][c.room],int(c.on_apron),*[int(f in c.flags) for f in ('EVENING_STARTED','RUMOR_CLEARED','TERMS_CARD_AVAILABLE','CUES_RESTORED')],*[M['rooms'][getattr(c,x+'_room')] for x in ('felix','bunny','frankie','rita','cart','display')],int(c.contest_active),int(bool(c.flags&{'DISPLAY_STAGED','HELP_ACCEPTED'})),int('VC03_RESOLVED' in c.flags),*[int(getattr(g,x)) for x in ('tested','peg_available','peg_engaged','gate_open','wedge_in_gate')],self.epoch]
  assert self.v.call('p11Context',*a)==1
  for obj in c.inventory:assert self.v.call('p11ContextItem',oid(obj))==1
 def events(self):
  events=[]
  for i in range(self.v.p['p11EventCount']):
   name=E[self.v.call('p11Event',i)];a,b,c,d=[self.v.call('p11EventArg',i,j) for j in range(4)]
   serial=self.v.call('p11EventSerialHi',i)*32768+self.v.call('p11EventSerialLo',i);data={'serial':serial,'puzzle':'P11'};kind='object'
   if name=='P11_PRESENTATION_QUEUED':data['source']=SO[a];kind='presentation';assert b==c==d==0
   elif name=='P11_PRESENTED':
    source=SO[a];data.update(source=source,canonical_tokens=tuple(x['token'] for x in M['receipts'][source][b:c+1]));kind='presentation';assert d==0
   elif name=='P11_LIFT':data.update(display_id='folded_display',cart_id='handcart',supported_by=('jack','felix'),panel_safe=True,no_timer=True,advance_peg=bool(a));assert b==c==d==0
   elif name=='P11_SET_BACK':data.update(catch_reset=True,peg_preserved=True,movement_free=True,items_preserved=True);kind='safety';assert a==b==c==d==0
   elif name=='P11_PEG_REQUEST':data.update(request_id=f'P11:{self.w._epoch}:peg:{serial}',owner='P04',peg_id='hold_open_peg',engaged=True,helper='bunny');kind='external_action_request';assert a==self.epoch and b==c==d==0
   elif name=='P11_PEG_ACK':data.update(owner='P04',peg_id='hold_open_peg',helper='bunny');kind='handoff';assert a==b==c==d==0
   elif name=='P11_CATCH_RELEASED':data.update(helper='frankie',catch_id='wing_catch');assert a==b==c==d==0
   elif name=='P11_FOLD':data.update(supported=False,padded=True,panel_safe=True,cart_id='handcart',caption_source='fold',laugh_emitted=False);kind='safety';assert a==b==c==d==0
   elif name=='P11_STAGED':data.update(flags=('DISPLAY_STAGED','HELP_ACCEPTED'),**self.w.display_handoff,caption_source='staged');kind='puzzle';assert a==b==c==d==0
   elif name=='P11_VC03_REQUEST':data.update(encounter_id='VC03',request_id=f'P11:{self.w._epoch}:VC03:{serial}',safety_complete=True,sincere_text_presented=True,shared_credit_required=True);kind='contest_request';assert a==self.epoch and b==c==d==0
   elif name=='P11_VC03_ACK':data.update(encounter_id='VC03',cancelled=bool(a));kind='handoff';assert a in (0,1) and b==c==d==0
   elif name=='LAF11':data.update(source_id='P11.SUCCESS.005.02',never_double_fire=True);kind='comedy';assert a==b==c==d==0
   else:data['level']=a;kind='hint';assert b==c==d==0
   events.append((name,kind,data))
  return events
 def check(self,result):
  assert self.v.persistent()==encode_world(self.w),(result.code,'state',self.v.persistent(),encode_world(self.w))
  assert CO[self.v.p['p11Code']]==result.code,(CO[self.v.p['p11Code']],result.code)
  lines=tuple(R[self.v.call('p11Line',i)] for i in range(self.v.p['p11LineCount']));units=tuple(U[self.v.call('p11Unit',i)] for i in range(self.v.p['p11UnitCount']))
  assert lines==result.line_ids,(lines,result.line_ids);assert units==result.speech_unit_ids,(units,result.speech_unit_ids)
  assert self.events()==[(e.id,e.kind,e.payload) for e in result.events],(self.events(),result.events)
  source=self.v.p['p11PresentationSource'];pid=f"P11:{SO[source]}:{self.v.p['p11PresentationHi']*32768+self.v.p['p11PresentationLo']}" if source else None
  expected=':'.join(result.presentation_id.split(':')[0:1]+result.presentation_id.split(':')[2:]) if result.presentation_id else None
  assert pid==expected,(pid,expected)
  return result
 def action(self,model,native,*args,c=C):
  self.project(c);result=getattr(self.w,model)(c,*args);native_args=args
  if model in ('begin_presentation','resume_presentation'):native_args=(M['sources'][args[0]],)
  elif model=='look':native_args=(oid(args[0]),)
  elif model=='act':native_args=(list(Verb).index(Verb(args[0]))+1,oid(args[1]),M['topic_targets'].get(args[2],oid(args[2])) if len(args)>2 else 0)
  self.v.call(native,*native_args);return self.check(result)
 def begin(self,source,c=C):return self.action('begin_presentation','p11Begin',source,c=c)
 def resume(self,source,c=C):return self.action('resume_presentation','p11Resume',source,c=c)
 def ack(self,source,record=None,units=(),c=C):
  self.project(c);p=self.w.presentations[source];sid=M['sources'][source];self.v.call('p11Resume',sid)
  r=self.w.acknowledge_presentation(c,self.w._handle(source),record_id=record,speech_unit_ids=units)
  self.v.call('p11Acknowledge',sid,*divmod(p.serial,32768),self.epoch,M['line_ids'][record] if record else 0,M['speech_unit_ids'][units[0]] if units else 0,M['speech_unit_ids'][units[-1]] if units else 0)
  return self.check(r)
 def show(self,source,c=C):
  self.begin(source,c);return self.ack(source,record=self.w.SOURCES[source],c=c)
 def ack_peg(self,c=C):
  self.project(c);serial=self.w.peg_request_at;r=self.w.acknowledge_peg(c,self.w.pending_peg_request_id or 'stale');self.v.call('p11AcknowledgePeg',*divmod(serial,32768),self.epoch);return self.check(r)
 def ack_contest(self,c=C,cancelled=False):
  self.project(c);serial=self.w.contest_request_at;r=self.w.acknowledge_contest_request(c,self.w.pending_contest_request_id or 'stale',cancelled=cancelled);self.v.call('p11AcknowledgeContest',*divmod(serial,32768),self.epoch,int(cancelled));return self.check(r)
 def rescue(self,c=C,order=('peg','catch')):
  self.action('lift','p11Lift',c=c)
  for a in order:
   if a=='peg':
    self.action('request_peg','p11RequestPeg',c=c);c=replace(c,gate=replace(c.gate,peg_engaged=True,gate_open=True))
    if self.w.peg_request_at:self.ack_peg(c)
   else:self.action('release_catch','p11ReleaseCatch',c=c)
  self.action('pull_handle','p11PullHandle',c=c);self.action('stage_display','p11StageDisplay',c=c);return c
 def restore(self):
  saved=decode_words(list(self.v.persistent().values()));self.w=P11World.load(saved);assert self.v.call('p11AfterRestore')==1;self.context=None
 def queries(self):
  before=self.v.persistent()
  records=tuple(R[x] for i in range(10) if (x:=self.v.call('p11JournalAt',i,0)));units=tuple(U[x] for i in range(25) if (x:=self.v.call('p11JournalAt',i,1)))
  pending=tuple(SO[x] for i in range(10) if (x:=self.v.call('p11PendingAt',i)))
  assert records==self.w.journal_records(),(records,self.w.journal_records());assert units==self.w.journal_units(),(units,self.w.journal_units())
  assert pending==tuple(s for s,p in sorted(self.w.presentations.items(),key=lambda kv:kv[1].serial) if not self.w._complete(s))
  for method,attr in [('Ready','ready'),('Supported','supported'),('SincereComplete','sincere_complete'),('ConcernPending','concern_pending'),('ContestEligible','contest_eligible')]:assert bool(self.v.call('p11'+method))==getattr(self.w,attr)
  assert tuple(O[x] for i in range(4) if (x:=self.v.call('p11InventoryAt',i)))==self.w.inventory
  assert {O[x] for i in range(4) if (x:=self.v.call('p11ReservedAt',i))}==self.w.reserved_external_objects
  handoff=copy.deepcopy(M['display_handoff']) if self.v.call('p11Ready') else None
  if handoff:handoff['shared_helpers']=tuple(handoff['shared_helpers'])
  assert handoff==self.w.display_handoff;assert before==self.v.persistent()

class DomainTests(unittest.TestCase):
 VM=source_vm.VM
 def h(self,w=None):return Harness(self.VM,w)
 def test_helper_orders_preengaged_and_physical_safety_before_text(self):
  for ctx,order in itertools.product((C,ENGAGED),itertools.permutations(('peg','catch'))):
   h=self.h();c=h.rescue(ctx,order);self.assertTrue(h.w.ready);self.assertFalse(h.w.presentations);h.queries()
   h.action('request_contest','p11RequestContest',c=c);self.assertFalse(h.w.contest_eligible)
   for model,native in [('lift','Lift'),('pull_handle','PullHandle'),('stage_display','StageDisplay'),('set_back','SetBack')]:h.action(model,'p11'+native,c=c)
   h.restore();h.queries();self.assertEqual(h.w.advance_peg_at,h.w.lift_at if ctx.gate.peg_engaged else 0)
 def test_every_sincere_prefix_restore_then_eligible(self):
  units=RECORD_UNITS['P11.DIALOGUE.002']
  for n in range(7):
   h=self.h();h.action('lift','p11Lift');h.begin('sincere')
   if n:h.ack('sincere',units=units[:n])
   h.restore();h.queries();c=h.rescue();h.action('request_contest','p11RequestContest',c=c)
   self.assertEqual(h.w.contest_eligible,n==6)
   h.ack('sincere',record='P11.DIALOGUE.002',c=c);h.action('request_contest','p11RequestContest',c=c);h.queries()
 def test_concern_stays_protected_after_recovery_and_staging(self):
  h=self.h();h.action('lift','p11Lift');h.begin('concern');h.ack('concern',units=('P11.DIALOGUE.001.01',))
  h.action('set_back','p11SetBack');h.show('sincere');c=h.rescue();h.show('fold',c)
  h.action('claim_laugh','p11ClaimLaugh',c=c);h.action('request_contest','p11RequestContest',c=c);h.restore()
  self.assertTrue(h.w.concern_pending);h.ack('concern',record='P11.DIALOGUE.001',c=c);h.action('claim_laugh','p11ClaimLaugh',c=c);h.queries()
  h=self.h();c=h.rescue();h.begin('concern',c);self.assertNotIn('concern',h.w.presentations)
 def test_all_sources_speakers_and_journal_receipts(self):
  h=self.h();h.action('lift','p11Lift')
  for source in ('intro','wing','peg','catch','concern','sincere'):h.show(source)
  c=h.rescue();h.show('fold',c);h.begin('staged',c);self.assertNotIn('staged',h.w.presentations)
  c=replace(c,rita_room=SIDE_PASSAGE);h.show('staged',c);h.queries();h.restore();h.queries()
  for source in M['sources']:h.begin(source,c);h.resume(source,c)
 def test_cross_side_helpers_and_current_gate_acknowledgment(self):
  h=self.h();h.action('lift','p11Lift');h.action('request_peg','p11RequestPeg',c=replace(C,bunny_room=SIDE_PASSAGE));h.action('release_catch','p11ReleaseCatch',c=replace(C,frankie_room=SIDE_PASSAGE))
  h.action('pull_handle','p11PullHandle');h.action('request_peg','p11RequestPeg');h.action('request_peg','p11RequestPeg');h.ack_peg(C)
  self.assertFalse(h.w.peg_ack_at);h.ack_peg(ENGAGED);h.ack_peg(ENGAGED);h.action('pull_handle','p11PullHandle',c=ENGAGED)
  h.action('release_catch','p11ReleaseCatch',c=ENGAGED);h.action('release_catch','p11ReleaseCatch',c=ENGAGED)
  h.action('pull_handle','p11PullHandle');self.assertTrue(h.w.supported);h.action('pull_handle','p11PullHandle',c=ENGAGED);h.queries()
 def test_safety_recovery_travel_and_prior_progress(self):
  for peg,catch in itertools.product((False,True),repeat=2):
   h=self.h();h.action('lift','p11Lift');h.show('sincere')
   if peg:h.action('request_peg','p11RequestPeg');h.ack_peg(ENGAGED)
   if catch:h.action('release_catch','p11ReleaseCatch')
   away=replace(ENGAGED if peg else C,room=CONSERVATORY,on_apron=True,felix_room=CONSERVATORY,flags=frozenset(),contest_active=True)
   h.project(away);self.assertEqual(h.v.call('p11ValidateContext'),0)
   h.action('set_back','p11SetBack',c=away);h.action('set_back','p11SetBack',c=away);self.assertTrue(h.w.sincere_complete)
   h.restore();c=h.rescue(ENGAGED if peg else C);h.queries();self.assertTrue(h.w.contest_eligible)
 def test_prerequisites_context_and_unique_object_ownership(self):
  for flag in PREREQUISITES:
   h=self.h();h.action('lift','p11Lift',c=replace(C,flags=C.flags-{flag}));self.assertFalse(h.w.first_lift_at)
  changes=[{'on_apron':True},{'room':PORCH},{'contest_active':True},{'felix_room':PORCH},{'cart_room':PORCH},{'display_room':PORCH},{'gate':replace(GATE,tested=False,peg_available=False)}]
  for change in changes:
   h=self.h();h.action('lift','p11Lift',c=replace(C,**change));self.assertFalse(h.w.first_lift_at)
  h=self.h();h.project(replace(C,flags=C.flags|{'DISPLAY_STAGED'}));self.assertEqual(h.v.call('p11ValidateContext'),0)
  c=h.rescue();pocket=frozenset(('rita_sample_tile_1','rita_sample_tile_2','rita_sample_tile_3','master_invitation','grease_pencil','renewal_repair_card','wedge'))
  for change in [{},{'cart_room':PORCH},{'display_room':PORCH},{'flags':frozenset()}]:
   ctx=replace(c,inventory=pocket,**change);h.project(ctx)
   try:h.w.validate_context(ctx);expected=1
   except ValueError:expected=0
   self.assertEqual(h.v.call('p11ValidateContext'),expected);self.assertEqual(ctx.inventory,pocket)
  h.queries()
 def test_contest_receipt_cancellation_rematch_and_active_modes(self):
  h=self.h();c=h.rescue();h.show('sincere',c);h.action('request_contest','p11RequestContest',c=c);h.action('request_contest','p11RequestContest',c=c)
  away=replace(c,felix_room=CONSERVATORY);h.ack_contest(away);h.ack_contest(away,True);h.ack_contest(c)
  h.action('request_contest','p11RequestContest',c=c);h.restore();h.ack_contest(replace(c,contest_active=True))
  h.action('request_contest','p11RequestContest',c=replace(c,flags=c.flags|{'VC03_RESOLVED','VC03_WON'}));h.ack_contest(c);h.queries()
  self.assertEqual(h.w.flags,{'DISPLAY_STAGED','HELP_ACCEPTED'})
 def test_laughter_single_fire_protected_and_restored(self):
  h=self.h();h.action('lift','p11Lift');h.action('claim_laugh','p11ClaimLaugh');h.show('sincere');h.action('claim_laugh','p11ClaimLaugh')
  c=h.rescue();h.action('claim_laugh','p11ClaimLaugh',c=c);h.begin('fold',c);h.ack('fold',units=RECORD_UNITS['P11.SUCCESS.005'][:3],c=c);h.action('claim_laugh','p11ClaimLaugh',c=c)
  h.ack('fold',record='P11.SUCCESS.005',c=c);h.action('request_contest','p11RequestContest',c=c);h.action('claim_laugh','p11ClaimLaugh',c=c);h.ack_contest(c,True)
  h.action('claim_laugh','p11ClaimLaugh',c=c);h.restore();h.action('claim_laugh','p11ClaimLaugh',c=c);h.queries()
 def test_partial_prefix_speaker_rechecks_and_pure_queries(self):
  h=self.h();h.action('lift','p11Lift');h.begin('concern');away=replace(C,bunny_room=SIDE_PASSAGE)
  h.ack('concern',record='P11.DIALOGUE.001',c=away);self.assertFalse(h.w.journal_units())
  h.ack('concern',units=('P11.DIALOGUE.001.01',));away=replace(C,bunny_room=SIDE_PASSAGE,frankie_room=SIDE_PASSAGE)
  h.ack('concern',units=('P11.DIALOGUE.001.02',),c=away);self.assertEqual(len(h.w.journal_units()),2)
  for obj in ('display_wing','folded_display','hold_open_peg','wing_catch','ceramic_panel'):h.action('look','p11Look',obj)
  for level in (1,3,2,3):h.action('hint','p11Hint',level)
  h.action('push_harder','p11PushHarder');h.action('push_harder','p11PushHarder',c=replace(C,felix_room=CONSERVATORY));h.queries()
 def test_invalid_ranges_stale_caption_restore_and_cancel(self):
  h=self.h();h.action('lift','p11Lift');h.begin('sincere');p=h.w.presentations['sincere'];sid=M['sources']['sincere'];old=h.epoch;before=h.v.persistent()
  for args in [(sid,0,p.serial,old,M['line_ids']['P11.HINT.1'],0,0),(sid,0,p.serial,old,0,M['speech_unit_ids']['P11.DIALOGUE.002.02'],M['speech_unit_ids']['P11.DIALOGUE.002.03']),(sid,0,p.serial+1,old,M['line_ids']['P11.DIALOGUE.002'],0,0),(sid,0,p.serial,old+1,M['line_ids']['P11.DIALOGUE.002'],0,0)]:
   h.v.call('p11Acknowledge',*args);self.assertIn(CO[h.v.p['p11Code']],('invalid_argument','stale_presentation'));self.assertEqual(before,h.v.persistent())
  h.v.call('p11Invalidate');h.v.call('p11Acknowledge',sid,0,p.serial,old,M['line_ids']['P11.DIALOGUE.002'],0,0);self.assertEqual(CO[h.v.p['p11Code']],'invalid_context')
  h.context=None;h.resume('sincere');h.restore();h.resume('sincere')
  h.v.call('p11Acknowledge',sid,0,p.serial,old,M['line_ids']['P11.DIALOGUE.002'],0,0);self.assertEqual(CO[h.v.p['p11Code']],'stale_presentation')
  h.ack('sincere',record='P11.DIALOGUE.002');h.ack('sincere',record='P11.DIALOGUE.002');h.queries()
 def test_stale_peg_and_contest_after_restore_and_abandoned_attempt(self):
  h=self.h();h.action('lift','p11Lift');h.action('request_peg','p11RequestPeg');serial=h.w.peg_request_at;old=h.epoch
  h.restore();h.project(ENGAGED);before=h.v.persistent();h.v.call('p11AcknowledgePeg',*divmod(serial,32768),old);self.assertEqual(CO[h.v.p['p11Code']],'stale_peg_request');self.assertEqual(before,h.v.persistent())
  h.action('set_back','p11SetBack');h.action('lift','p11Lift');h.action('request_peg','p11RequestPeg');h.v.call('p11AcknowledgePeg',*divmod(serial,32768),h.epoch);self.assertEqual(CO[h.v.p['p11Code']],'stale_peg_request')
  c=h.rescue();h.show('sincere',c);h.action('request_contest','p11RequestContest',c=c);serial=h.w.contest_request_at;old=h.epoch;h.restore();h.project(c);before=h.v.persistent()
  h.v.call('p11AcknowledgeContest',*divmod(serial,32768),old,0);self.assertEqual(CO[h.v.p['p11Code']],'stale_contest_request');self.assertEqual(before,h.v.persistent());h.ack_contest(c);h.queries()
 def test_all_verbs_and_specific_dispatch(self):
  h=self.h()
  for verb,obj in itertools.product(Verb,('ceramic_panel','hold_open_peg','audience','staging_pocket','unknown')):h.action('act','p11Act',verb,obj)
  for verb,obj,target in [(Verb.PICK_UP,'folded_display',None),(Verb.PUSH,'folded_display',None),(Verb.TALK_TO,'bunny','peg'),(Verb.TALK_TO,'frankie','catch'),(Verb.TALK_TO,'felix','sincere'),(Verb.PULL,'display_handle',None),(Verb.USE,'folded_display','handcart'),(Verb.PICK_UP,'folded_display',None)]:h.action('act','p11Act',verb,obj,target)
  c=h.rescue();h.action('act','p11Act',Verb.USE,'handcart','staging_pocket',c=c);h.show('sincere',c);h.action('act','p11Act',Verb.TALK_TO,'felix','contest',c=c);h.queries()
 def test_invalid_context_fixed_inventory_getters_and_argument_types(self):
  h=self.h();h.project(C)
  for method in ('Line','Unit','Event','EventSerialHi','EventSerialLo','InventoryAt','ReservedAt'):
   for value in (-1,32767):self.assertEqual(h.v.call('p11'+method,value),0)
  for args in ((-1,0),(0,-1),(99,0),(0,4)):self.assertEqual(h.v.call('p11EventArg',*args),0)
  for obj in ('folded_display','handcart','hold_open_peg','bunny','staging_pocket','unknown'):
   h.context=None;h.project(C);self.assertEqual(h.v.call('p11ContextItem',oid(obj)),0);self.assertEqual(h.v.p['p11ContextValid'],0)
  for method,args in [('p11Begin',(0,)),('p11Hint',(4,)),('p11Act',(0,0,0)),('p11AcknowledgeContest',(0,0,1,2))]:
   h.context=None;h.project(C);before=h.v.persistent();h.v.call(method,*args);self.assertEqual(CO[h.v.p['p11Code']],'invalid_argument');self.assertEqual(before,h.v.persistent())
  for value in (True,1.5,'1'):
   with self.assertRaises(ValueError):h.v.call('p11Hint',value)
 def test_serial_carry_exhaustion_atomicity(self):
  for revision in (32766,32767,32768):
   h=self.h(P11World(revision=revision));c=h.rescue();h.show('sincere',c);h.action('request_contest','p11RequestContest',c=c);h.queries()
  h=self.h(P11World(revision=M['max_serial']));h.project(C);before=h.v.persistent()
  for method,args in [('p11Lift',()),('p11Hint',(1,))]:h.v.call(method,*args);self.assertEqual(CO[h.v.p['p11Code']],'serial_exhausted');self.assertEqual(before,h.v.persistent())
 def test_context_gate_shape_and_epoch_fail_closed(self):
  base=[3,0,1,1,1,1,3,0,4,6,3,3,0,0,0,1,1,0,1,0,3]
  variants=[]
  for index in range(20):
   bad=base.copy();bad[index]=7 if index in (0,6,7,8,9,10,11) else 2;variants.append(bad)
  for index in (15,16,18):
   bad=base.copy();bad[17]=1;bad[index]=0;variants.append(bad)
  for epoch in (0,1,2):
   bad=base.copy();bad[-1]=epoch;variants.append(bad)
  for args in variants:
   h=self.h();h.project(C);before=h.v.persistent();self.assertEqual(h.v.call('p11Context',*args),0)
   self.assertEqual(h.v.p['p11ContextValid'],0);self.assertEqual(CO[h.v.p['p11Code']],'invalid_context');self.assertEqual(before,h.v.persistent())
 def test_supported_serial_headroom_preserves_safe_release(self):
  w=P11World();w.lift(C);w.revision=M['max_serial']-1
  h=self.h(w);h.project(C);before=h.v.persistent()
  for method,args in [('p11Hint',(1,)),('p11RequestPeg',()),('p11ReleaseCatch',()),('p11Begin',(M['sources']['sincere'],))]:
   h.v.call(method,*args);self.assertEqual(CO[h.v.p['p11Code']],'serial_exhausted');self.assertEqual(h.v.persistent(),before)
  h.action('set_back','p11SetBack');self.assertFalse(h.w.supported);self.assertEqual(h.w.revision,M['max_serial'])
  h=self.h(P11World(revision=M['max_serial']-1));h.project(C);before=h.v.persistent();h.v.call('p11Lift')
  self.assertEqual(CO[h.v.p['p11Code']],'serial_exhausted');self.assertEqual(before,h.v.persistent())
  w=P11World();w.lift(ENGAGED);w.release_catch(ENGAGED);w.revision=M['max_serial']-1;h=self.h(w)
  h.action('pull_handle','p11PullHandle',c=ENGAGED);self.assertEqual(h.w.phase,2);self.assertEqual(h.w.revision,M['max_serial'])
  h.v.p.update(p11Phase=1);self.assertEqual(h.v.call('p11Validate'),0)
 def test_seeded_physical_and_caption_parity(self):
  rng=random.Random(1111);h=self.h();c=C
  actions=[('lift','Lift'),('request_peg','RequestPeg'),('release_catch','ReleaseCatch'),('pull_handle','PullHandle'),('stage_display','StageDisplay'),('set_back','SetBack'),('push_harder','PushHarder'),('request_contest','RequestContest'),('claim_laugh','ClaimLaugh')]
  for _ in range(140):
   if rng.randrange(5)==0:c=replace(c,gate=replace(c.gate,peg_engaged=not c.gate.peg_engaged))
   if rng.randrange(7)==0:
    source=rng.choice(tuple(M['sources']));r=h.begin(source,c)
    if r.presentation_id:h.ack(source,record=h.w.SOURCES[source],c=c)
   else:
    model,native=rng.choice(actions);h.action(model,'p11'+native,c=c)
   if rng.randrange(13)==0:h.restore()
  h.queries()
 def test_deciding_operands_in_source_vm(self):
  v=source_vm.VM();self.assertEqual(v.ev(['or',0,17],{}),17);self.assertEqual(v.ev(['and',4,23],{}),23)

class CompiledDomainTests(DomainTests):VM=ByteVM
if __name__=='__main__':unittest.main()
