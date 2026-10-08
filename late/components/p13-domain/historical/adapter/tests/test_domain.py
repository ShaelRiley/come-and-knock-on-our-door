"""Accepted-model oracle runs against source and actual compiled SCI instructions."""
from pathlib import Path
import sys,json,unittest,itertools,copy,hashlib
from dataclasses import replace
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
sys.path[:0]=[str(HERE),str(ROOT),str(ROOT/'tests')]
from cakood.p13_model import P13World,P13Context,PREREQUISITES,PROGRAM,BOARD,ROUTES
from cakood.p12_model import CurrentRig,PEOPLE,COURTYARD,LIVING,KITCHEN,PORCH,SIDE
from cakood.p10_model import ORDER
from cakood.model import Verb
from test_late_campaign_models import c13,actors,contests,POT,DISPLAY,GATE,RIG
from test_verbal_contest import prepared,play,leave
from codec import M,encode_world,encode_save,decode_words
import source_vm
from compiled_vm import Compiled
C=c13();P=actors(replace(C,room=PORCH),milo=PORCH);K=actors(replace(C,room=KITCHEN),bunny=KITCHEN)
D=actors(replace(C,room=SIDE),felix=SIDE,vivian=SIDE);L=actors(replace(C,room=LIVING),frankie=LIVING);B=replace(C,board_room=COURTYARD)
R={v:k for k,v in M['line_ids'].items()};U={v:k for k,v in M['speech_unit_ids'].items()};E={v:k for k,v in M['events'].items()};CO={v:k for k,v in M['codes'].items()};SO={v:k for k,v in M['sources'].items()};O={v:k for k,v in M['objects'].items()};W={v:k for k,v in M['words'].items()}
def oid(obj):return M['objects'].get(obj,32767)
class ByteVM:
 def __init__(self):self.machine=Compiled(HERE,995,source_vm.DEFAULTS);self.p=source_vm.DEFAULTS.copy();self.call('p13Init')
 def call(self,name,*args):
  if any(type(x) is not int or not -32768<=x<=32767 for x in args):raise ValueError('SCI argument')
  if name not in source_vm.SIGNATURES or len(args)!=source_vm.SIGNATURES[name]:raise ValueError('Method/arity')
  return self.machine.execute(name,self.p,args)
 def persistent(self):return {k:self.p[k] for k in M['persisted_properties']}

class Harness:
 def __init__(self,typ=source_vm.VM,world=None):
  self.w=world or P13World();self.v=typ();self.v.p.update(encode_world(self.w));self.epoch=1;self.context=None;self.history=[]
 def project(self,c=C):
  if self.context==c:return
  self.context=c;self.epoch+=1;rooms=dict(c.npc_locations);g=c.gate
  args=[M['rooms'][c.room],int(c.on_apron),*[int(x in c.flags) for x in ('INTRODUCTION_CLEAR','FOOD_READY','DISPLAY_STAGED','HELP_ACCEPTED','EVENING_STARTED')],*[int(getattr(c,x)) for x in ('welcome_cleared','queue_clear','buffet_at_hatch','hatch_visible','display_concealed','lane_clear','footprint_clear')],M['rooms'][c.board_room],M['rooms'][c.rig.location],int(c.rig.connected),int(c.rig.source=='MIC'),int(c.rig.facing_inward),int(c.contest_active),int(c.resolved('VC04')),*[M['rooms'][rooms[p]] if p in rooms else -1 for p in PEOPLE[1:]],int(g is not None),oid(g.peg_id) if g else 0,M['rooms'][g.peg_location] if g else 0,*[int(getattr(g,x)) if g else 0 for x in ('tested','peg_available','peg_engaged','gate_open','wedge_in_gate')],self.epoch]
  assert self.v.call('p13Context',*args)==1
  for obj in c.inventory:assert self.v.call('p13ContextItem',oid(obj))==1
 def events(self):
  events=[]
  for i in range(self.v.p['p13EventCount']):
   name=E[self.v.call('p13Event',i)];a,b,c,d=[self.v.call('p13EventArg',i,j) for j in range(4)]
   serial=self.v.call('p13EventSerialHi',i)*32768+self.v.call('p13EventSerialLo',i)
   data={'serial':serial,'puzzle':'P13'};kind='object';assert d==0
   if name=='P13_PRESENTATION_QUEUED':data['source']=SO[a];kind='presentation';assert b==c==0
   elif name=='P13_PRESENTED':data.update(source=SO[a],canonical_tokens=tuple(x['token'] for x in M['receipts'][SO[a]][b:c+1]));kind='presentation'
   elif name=='P13_DELIVERY_OWNERSHIP':data.update(transfer_from={'hotpot_pot':'P07','folded_display':'P11','handcart':'P11'},owner='P13',board_location=LIVING,program_owner='inventory');kind='ownership'
   elif name=='P13_ROUTE_ATTEMPT':data.update(load_unchanged=True,attempt=a*32768+b);kind='route';assert c==0
   elif name=='P13_GUEST_ROUTE':data.update(card_id=PROGRAM,card_to='milo',route=(PORCH,LIVING,'rear_arch',COURTYARD),milo_joins_after_queue=True);kind='movement'
   elif name=='P13_GUEST_ROUTE_COMPLETE':kind='movement'
   elif name=='P13_POT_DELIVERED':data.update(object_id='hotpot_pot',from_room=KITCHEN,to_room=COURTYARD,position='buffet',route='kitchen_hatch');kind='movement'
   elif name in ('P13_SERVE','P13_SHOW','P13_TOAST'):data.update(cue=W[a]);kind='puzzle'
   elif name=='P13_DISPLAY_DELIVERED':data.update(object_ids=('folded_display','handcart'),from_room=SIDE,to_room=COURTYARD,position='display_footprint',covered=True,helpers=('felix','vivian'));kind='movement'
   elif name=='P13_SCREEN_OPENED':data.update(display_reveal_owner='rita',damage=False)
   elif name=='P13_BOARD_DELIVERED':data.update(object_id=BOARD,from_room=LIVING,to_room=COURTYARD,helper='frankie',route='house_doorway');kind='movement'
   elif name=='P13_VC04_REQUEST':data.update(request_id=f'P13:epoch:VC04:{serial}',encounter='VC04',safe=True);kind='contest_request'
   elif name=='P13_CONTEST_HANDOFF':data.update(accepted=bool(a));kind='handoff'
   elif name=='P13_AUTOSAVE_REQUEST':data={'cue':W[a],'serial':serial,'request_id':f'P13:epoch:save:{W[a]}:{serial}'};kind='autosave'
   elif name=='P13_AUTOSAVE_ACK':data.update(cue=W[a]);kind='autosave_ack'
   elif name=='P13_WRONG_VISUAL':kind='presentation'
   elif name=='LAF13':kind='laugh'
   else:raise AssertionError(name)
   if name not in ('P13_PRESENTATION_QUEUED','P13_PRESENTED','P13_ROUTE_ATTEMPT','P13_SERVE','P13_SHOW','P13_TOAST','P13_CONTEST_HANDOFF','P13_AUTOSAVE_REQUEST','P13_AUTOSAVE_ACK'):assert a==b==c==0
   events.append((name,kind,data))
  return events
 def check(self,r):
  assert self.v.persistent()==encode_world(self.w),(r.code,'state',{k:(v,encode_world(self.w)[k]) for k,v in self.v.persistent().items() if v!=encode_world(self.w)[k]})
  assert CO[self.v.p['p13Code']]==r.code,(CO[self.v.p['p13Code']],r.code)
  assert tuple(R[self.v.call('p13Line',i)] for i in range(self.v.p['p13LineCount']))==r.line_ids
  assert tuple(U[self.v.call('p13Unit',i)] for i in range(self.v.p['p13UnitCount']))==r.speech_unit_ids
  expected=[]
  for e in r.events:
   p=dict(e.payload)
   if 'request_id' in p:
    bits=p['request_id'].split(':');bits[1]='epoch';p['request_id']=':'.join(bits)
   expected.append((e.id,e.kind,p))
  assert self.events()==expected,(self.events(),expected)
  source=self.v.p['p13PresentationSource'];pid=f"P13:{SO[source]}:{self.v.p['p13PresentationHi']*32768+self.v.p['p13PresentationLo']}" if source else None
  expected=':'.join(r.presentation_id.split(':')[0:1]+r.presentation_id.split(':')[2:]) if r.presentation_id else None
  assert pid==expected,(pid,expected)
  self.w.validate();assert self.v.call('p13Validate')==1
  self.history.append(self.w.save());return r
 def action(self,model,native,*args,c=C):
  self.project(c);r=getattr(self.w,model)(c,*args);native_args=args
  if model=='start':
   p,d=args;native_args=(oid(p['object_id']),M['rooms'][p['room']],int(p['lid_closed']),p['portions'],int(p['portion_kind']=='tasting'),int(p['includes_jackie']),oid(d['display_id']),oid(d['cart_id']),M['rooms'][d['location']],int(d['position']=='staging_pocket'),*[int(d[x]) for x in ('folded','padded','covered','undamaged','panel_revealed','rita_reveal_consent')],13)
  elif model in ('begin_presentation','resume_presentation'):native_args=(M['sources'][args[0]],)
  elif model in ('give_program','deliver_pot','deliver_display','deliver_board'):native_args=(M['routes'][args[0] if args else {'give_program':'house_doorway','deliver_pot':'kitchen_hatch','deliver_display':'side_gate','deliver_board':'house_doorway'}[model]],)
  elif model in ('preview',):native_args=(M['words'][args[0]],)
  elif model=='protect_furniture':native_args=(oid(args[0]),)
  elif model=='dispatch':native_args=(list(Verb).index(Verb(args[0]))+1,-M['words'][args[1]] if args[1] in M['words'] else oid(args[1]),(-M['routes'][args[2]] if args[2] in M['routes'] else oid(args[2])) if len(args)>2 and args[2] else 0)
  self.v.call(native,*native_args);return self.check(r)
 def begin(self,s,c=C):return self.action('begin_presentation','p13Begin',s,c=c)
 def resume(self,s,c=C):return self.action('resume_presentation','p13Resume',s,c=c)
 def ack(self,s,record=None,units=(),c=C):
  self.project(c);p=self.w.presentations[s];sid=M['sources'][s];self.v.call('p13Resume',sid)
  r=self.w.acknowledge_presentation(c,self.w._handle(s),record_id=record,speech_unit_ids=units)
  self.v.call('p13Acknowledge',sid,*divmod(p.serial,32768),self.epoch,M['line_ids'][record] if record else 0,M['speech_unit_ids'][units[0]] if units else 0,M['speech_unit_ids'][units[-1]] if units else 0)
  return self.check(r)
 def show(self,s,c=C):self.begin(s,c);return self.ack(s,record=self.w.SOURCES[s],c=c)
 def start(self,c=C):return self.action('start','p13Handoff',POT,DISPLAY,c=c)
 def serve(self,c=C):
  self.start(c);self.action('give_program','p13GiveProgram',c=actors(replace(c,room=PORCH),milo=PORCH));self.action('confirm_seating','p13ConfirmSeating',c=c)
  self.action('deliver_pot','p13DeliverPot',c=actors(replace(c,room=KITCHEN),bunny=KITCHEN));self.action('pull_serve','p13PullServe',c=c)
 def reveal(self,c=C):
  self.serve(c);self.show('rita_ready',c);self.action('deliver_display','p13DeliverDisplay',c=actors(replace(c,room=SIDE),felix=SIDE,vivian=SIDE));self.action('open_screen','p13OpenScreen',c=c)
 def showcue(self,c=C):self.reveal(c);self.show('reveal',c);self.action('pull_show','p13PullShow',c=c)
 def board(self,c=C):self.showcue(c);self.action('deliver_board','p13DeliverBoard',c=actors(replace(c,room=LIVING),frankie=LIVING))
 def finish(self,c=C):self.board(c);c=replace(c,board_room=COURTYARD);self.show('attention',c);self.action('pull_toast','p13PullToast',c=c)
 def restore(self):
  self.w=P13World.load(decode_words(list(self.v.persistent().values())));assert self.v.call('p13AfterRestore')==1;self.context=None
 def request_finish(self,accepted=False):
  self.project(self.context or B);hi,lo=divmod(self.w.contest_request_at,32768);r=self.w.finish_contest_request(self.w.pending_contest_request_id,accepted)
  self.v.call('p13FinishContestRequest',hi,lo,self.epoch,int(accepted));return self.check(r)
 def save_ack(self,cue):
  self.project(self.context or B);q=next(x for x in self.w.pending_autosaves if x['cue']==cue);r=self.w.acknowledge_autosave(q['request_id'])
  self.v.call('p13AcknowledgeAutosave',M['words'][cue],*divmod(q['serial'],32768),self.epoch,1);return self.check(r)
 def visual(self,c):
  self.project(c);hi,lo=divmod(self.w.wrong_at,32768);r=self.w.acknowledge_wrong_visual(c,self.w.pending_wrong_visual_id)
  self.v.call('p13AcknowledgeWrongVisual',hi,lo,self.epoch);return self.check(r)
 def queries(self):
  before=self.v.persistent()
  assert tuple(R[x] for i in range(len(self.w.journal_records())+1) if (x:=self.v.call('p13JournalAt',i,0)))==self.w.journal_records()
  assert tuple(U[x] for i in range(len(self.w.journal_units())+1) if (x:=self.v.call('p13JournalAt',i,1)))==self.w.journal_units()
  assert tuple(SO[x] for i in range(len(self.w.presentations)+1) if (x:=self.v.call('p13PendingAt',i)))==tuple(s for s,p in sorted(self.w.presentations.items(),key=lambda kv:kv[1].serial) if not self.w._complete(s))
  for method,value in [('p13Ready',self.w.ready),('p13Served',bool(self.w.served_at)),('p13ShowComplete',bool(self.w.show_at)),('p13RitaConsented',self.w.rita_consented),('p13ContestEligible',self.w.contest_eligible),('p13PotDelivered',bool(self.w.pot_at)),('p13DisplayDelivered',bool(self.w.display_at))]:assert bool(self.v.call(method))==value
  assert {O[x] for i in range(6) if (x:=self.v.call('p13ReservedAt',i))}==self.w.reserved_external_objects
  assert tuple(O[x] for i in range(2) if (x:=self.v.call('p13InventoryAt',i)))==self.w.inventory
  assert tuple(W[x] for i in range(4) if (x:=self.v.call('p13PendingSaveAt',i)))==tuple(x['cue'] for x in self.w.pending_autosaves)
  assert self.v.call('p13BoardLocation')==M['rooms'][COURTYARD if self.w.board_at else LIVING]
  assert self.v.call('p13PendingContestHi')*32768+self.v.call('p13PendingContestLo')==self.w.contest_request_at
  assert self.v.call('p13PendingWrongHi')*32768+self.v.call('p13PendingWrongLo')==(self.w.wrong_at if self.w.pending_wrong_visual_id else 0)
  assert before==self.v.persistent()

class DomainTests(unittest.TestCase):
 VM=source_vm.VM
 def h(self,world=None):return Harness(self.VM,world)
 def test_exact_order_deliveries_three_durable_saves_loss_suffices(self):
  h=self.h();h.finish();h.queries();self.assertTrue(h.w.ready);self.assertFalse(C.contests.progress['VC04'].won)
  self.assertEqual([x['cue'] for x in h.w.pending_autosaves],list(ORDER));h.restore();h.project(B)
  for cue in ORDER:h.save_ack(cue)
  h.queries();self.assertFalse(h.w.pending_autosaves)
  for fn,method,c in [('give_program','p13GiveProgram',replace(P,board_room=COURTYARD)),('confirm_seating','p13ConfirmSeating',B),('deliver_pot','p13DeliverPot',replace(K,board_room=COURTYARD)),('pull_serve','p13PullServe',B),('deliver_display','p13DeliverDisplay',replace(D,board_room=COURTYARD)),('open_screen','p13OpenScreen',B),('pull_show','p13PullShow',B),('deliver_board','p13DeliverBoard',replace(L,board_room=COURTYARD)),('pull_toast','p13PullToast',B)]:h.action(fn,method,c=c)
 def test_handoff_prerequisites_single_object_ownership(self):
  for flag in PREREQUISITES:h=self.h();h.start(replace(C,flags=C.flags-{flag}));self.assertFalse(h.w.start_at)
  h=self.h();h.start(replace(C,welcome_cleared=False));h.start();h.start();h.queries()
  h.project(replace(C,inventory=frozenset((PROGRAM,))));self.assertEqual(h.v.call('p13ValidateContext'),0)
  before=h.v.persistent();h.v.call('p13PullServe');self.assertEqual(CO[h.v.p['p13Code']],'invalid_context');self.assertEqual(before,h.v.persistent())
 def test_guests_queue_actual_helpers_and_current_layout(self):
  h=self.h();h.start();h.action('confirm_seating','p13ConfirmSeating');h.action('give_program','p13GiveProgram',c=replace(C,room=PORCH));h.action('give_program','p13GiveProgram',c=P)
  for c in (replace(C,queue_clear=False),actors(C,milo=PORCH)):h.action('confirm_seating','p13ConfirmSeating',c=c)
  h.action('deliver_pot','p13DeliverPot',c=K);h.action('confirm_seating','p13ConfirmSeating')
  for c in (actors(K,bunny=COURTYARD),actors(K,frankie=LIVING),replace(K,queue_clear=False),replace(K,buffet_at_hatch=False),replace(K,hatch_visible=False)):h.action('deliver_pot','p13DeliverPot',c=c)
  h.action('deliver_pot','p13DeliverPot',c=K);h.action('pull_serve','p13PullServe');h.queries()
 def test_wrong_routes_first_visual_laugh_no_load_reset(self):
  for source,fn,method,c,wrong in [('wrong_people','give_program','p13GiveProgram',P,'kitchen_hatch'),('wrong_pot','deliver_pot','p13DeliverPot',K,'house_doorway'),('wrong_display','deliver_display','p13DeliverDisplay',D,'kitchen_hatch')]:
   h=self.h()
   if source=='wrong_display':h.serve();h.show('rita_ready')
   else:h.start()
   h.action(fn,method,wrong,c=c);h.action('claim_laugh','p13ClaimLaugh',c=c);h.visual(c);h.show(source,c);h.action('claim_laugh','p13ClaimLaugh',c=c);h.visual(c);h.action('claim_laugh','p13ClaimLaugh',c=c)
   self.assertTrue(h.w.laugh_at);h.restore();h.action(fn,method,wrong,c=c);h.action('claim_laugh','p13ClaimLaugh',c=c);h.queries()
  h=self.h();h.start();h.action('give_program','p13GiveProgram','side_gate',c=P);h.action('deliver_pot','p13DeliverPot','side_gate',c=K);self.assertFalse(h.w.wrong_at)
  h.serve();h.show('rita_ready');h.action('deliver_display','p13DeliverDisplay','house_doorway',c=D);self.assertFalse(h.w.wrong_at)
 def test_consent_screen_current_gate_and_speakers(self):
  h=self.h();h.start();h.begin('rita_ready');h.action('deliver_display','p13DeliverDisplay',c=D);h.action('open_screen','p13OpenScreen');h.serve();h.begin('rita_ready')
  h.v.call('p13AudioFinished');h.check(h.w.audio_finished());h.action('deliver_display','p13DeliverDisplay',c=D);self.assertFalse(h.w.rita_consented)
  h.ack('rita_ready',record='P13.DIALOGUE.004',c=actors(C,rita=SIDE));h.ack('rita_ready',record='P13.DIALOGUE.004')
  for c in (actors(D,felix=COURTYARD),actors(D,vivian=COURTYARD),replace(D,gate=None),replace(D,gate=replace(GATE,peg_engaged=False)),replace(D,lane_clear=False),replace(D,footprint_clear=False),replace(D,display_concealed=False)):
   h.action('deliver_display','p13DeliverDisplay',c=c)
  h.action('deliver_display','p13DeliverDisplay',c=D)
  for c in (actors(C,rita=SIDE),replace(C,display_concealed=False)):h.action('open_screen','p13OpenScreen',c=c)
  h.action('open_screen','p13OpenScreen');h.queries()
 def test_all_reveal_prefixes_restore_stale_audio_and_show_barrier(self):
  for prefix in range(6):
   h=self.h();h.reveal();h.begin('reveal');tokens=h.w._tokens('reveal');p=h.w.presentations['reveal'];old=h.epoch
   if prefix:h.ack('reveal',units=tokens[:prefix])
   h.v.call('p13AudioFinished');h.check(h.w.audio_finished());h.restore();h.project(C);before=h.v.persistent()
   h.v.call('p13Acknowledge',M['sources']['reveal'],*divmod(p.serial,32768),old,M['line_ids']['P13.DIALOGUE.005'],0,0)
   self.assertEqual(CO[h.v.p['p13Code']],'stale_presentation');self.assertEqual(before,h.v.persistent())
   h.action('pull_show','p13PullShow')
   if prefix<5:h.resume('reveal');h.ack('reveal',units=tokens[prefix:]);h.action('pull_show','p13PullShow')
   self.assertTrue(h.w.show_at);h.queries()
 def test_board_actual_projection_queue_and_vc04_request_lifecycle(self):
  c=c13(contests());h=self.h();h.start(c);h.action('request_contest','p13RequestContest',c=c);h.showcue(c)
  for cc in (replace(L,queue_clear=False),replace(L,board_room=COURTYARD),actors(L,frankie=COURTYARD)):
   h.action('deliver_board','p13DeliverBoard',c=replace(cc,contests=c.contests))
  h.action('deliver_board','p13DeliverBoard','kitchen_hatch',c=replace(L,contests=c.contests));h.action('deliver_board','p13DeliverBoard',c=replace(L,contests=c.contests))
  h.project(c);self.assertEqual(h.v.call('p13ValidateContext'),0);c=replace(c,board_room=COURTYARD)
  h.action('request_contest','p13RequestContest',c=actors(c,stringer=LIVING));h.action('request_contest','p13RequestContest',c=c);h.action('request_contest','p13RequestContest',c=c);h.begin('attention',c)
  old=h.epoch;serial=h.w.contest_request_at;h.restore();h.project(c);before=h.v.persistent();h.v.call('p13FinishContestRequest',*divmod(serial,32768),old,1)
  self.assertEqual(CO[h.v.p['p13Code']],'stale_contest_request');self.assertEqual(before,h.v.persistent());h.request_finish(False);h.begin('attention',c)
  prepared('VC04',c.contests);play(c.contests,[False]*3,'VC04');leave(c.contests);h.context=None
  h.show('attention',c);h.action('pull_toast','p13PullToast',c=c);h.action('request_contest','p13RequestContest',c=c);h.request_finish(True);self.assertFalse(c.contests.progress['VC04'].won);h.queries()
 def test_actual_microphone_and_attention_text_needed_for_toast(self):
  h=self.h();h.board()
  for rig in (replace(RIG,location=LIVING),replace(RIG,connected=False),replace(RIG,source='TAPE'),replace(RIG,facing_inward=False)):
   c=replace(B,rig=rig);h.begin('attention',c);h.action('pull_toast','p13PullToast',c=c)
  h.action('pull_toast','p13PullToast',c=B);h.begin('attention',B);h.v.call('p13AudioFinished');h.check(h.w.audio_finished());h.action('pull_toast','p13PullToast',c=B)
  h.ack('attention',record='P13.SUCCESS.008',c=B);h.action('pull_toast','p13PullToast',c=replace(B,rig=replace(RIG,connected=False)));h.action('pull_toast','p13PullToast',c=B);h.queries()
 def test_checkpoint_failed_stale_duplicate_restore_do_not_undo_cues(self):
  h=self.h();h.finish();h.project(B);saved=h.v.persistent();reqs=list(h.w.pending_autosaves);old=h.epoch
  for q in reqs:
   args=(M['words'][q['cue']],*divmod(q['serial'],32768),h.epoch)
   h.v.call('p13AcknowledgeAutosave',*args,0);self.assertEqual(CO[h.v.p['p13Code']],'autosave_failed');self.assertEqual(saved,h.v.persistent())
   h.v.call('p13AcknowledgeAutosave',args[0],args[1],args[2]+1,args[3],1);self.assertEqual(CO[h.v.p['p13Code']],'stale_autosave');self.assertEqual(saved,h.v.persistent())
  h.restore();h.project(B)
  for q in reqs:
   h.v.call('p13AcknowledgeAutosave',M['words'][q['cue']],*divmod(q['serial'],32768),old,1);self.assertEqual(CO[h.v.p['p13Code']],'stale_autosave')
   h.save_ack(q['cue']);before=h.v.persistent();h.v.call('p13AcknowledgeAutosave',M['words'][q['cue']],*divmod(q['serial'],32768),h.epoch,1);self.assertEqual(CO[h.v.p['p13Code']],'stale_autosave');self.assertEqual(before,h.v.persistent())
  self.assertTrue(h.w.ready);h.queries()
 def test_sources_all_prefixes_and_current_speaker_receipts(self):
  for source in M['sources']:
   base=self.h();c=C
   if source=='attention':base.board();c=B
   elif source=='reveal':base.reveal()
   elif source=='rita_ready':base.serve()
   elif source=='wrong_display':base.serve();base.show('rita_ready');base.action('deliver_display','p13DeliverDisplay','kitchen_hatch',c=D);c=actors(D,felix=SIDE)
   else:
    base.start()
    if source=='wrong_people':base.action('give_program','p13GiveProgram','kitchen_hatch',c=P);c=P
    if source=='wrong_pot':base.action('deliver_pot','p13DeliverPot','house_doorway',c=K);c=K
    if source=='pot_help':c=K
   total=len(base.w._tokens(source))
   for prefix in range(total+1):
    h=self.h(P13World.load(base.w.save()));h.begin(source,c);tokens=h.w._tokens(source)
    if prefix:
     if tokens[0] not in M['speech_unit_ids']:h.ack(source,record=h.w.SOURCES[source],c=c)
     else:h.ack(source,units=tokens[:prefix],c=c)
    h.restore();h.resume(source,c)
    if prefix<total:h.ack(source,record=h.w.SOURCES[source],c=c)
    h.queries()
 def test_protected_furniture_dispatch_hints_and_preview(self):
  h=self.h();h.start()
  for cue in ORDER:h.action('preview','p13Preview',cue)
  for obj in ('ceramic_carrier','serving_table','credit_slate','completed_screen','pa_kit'):h.action('protect_furniture','p13ProtectFurniture',obj)
  for verb,obj in itertools.product(Verb,('rita','hotpot_pot','folded_display','screen_pull_tab','microphone','unknown')):h.action('dispatch','p13Act',verb,obj)
  for level in (1,2,3):h.action('hint','p13Hint',level)
  h.finish()
  for obj in ('ceramic_carrier','serving_table','credit_slate','completed_screen','pa_kit'):h.action('protect_furniture','p13ProtectFurniture',obj,c=B)
  h.queries()
 def test_serial_carry_exhaustion_signed_words_and_cancel(self):
  h=self.h(P13World(revision=32767));h.start();self.assertEqual(h.w.start_at,32768);h.show('opening');h.restore();h.queries()
  h=self.h();h.start();h.begin('opening');s=h.w.presentations['opening'];r=h.w.cancel_presentation(h.w._handle('opening'));h.v.call('p13Cancel',M['sources']['opening'],*divmod(s.serial,32768),h.epoch);h.check(r);h.context=None;h.resume('opening');h.show('opening');h.queries()
  h=self.h(P13World(revision=M['max_serial']));h.project();before=h.v.persistent();h.v.call('p13Handoff',103,2,1,8,1,1,42,66,3,1,1,1,1,1,0,0,13);self.assertEqual(CO[h.v.p['p13Code']],'serial_exhausted');self.assertEqual(before,h.v.persistent())
  for value in (True,'1',1.0,32768,-32769):
   with self.assertRaises(ValueError):h.v.call('p13Hint',value)

class BytecodeTests(DomainTests):VM=ByteVM
if __name__=='__main__':unittest.main()
