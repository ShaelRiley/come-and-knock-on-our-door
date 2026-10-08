"""Same accepted-model oracle drives source and actual emitted SCI instructions."""
from pathlib import Path
import sys,json,unittest,itertools,copy,hashlib
from dataclasses import replace
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
sys.path[:0]=[str(HERE),str(ROOT),str(ROOT/'tests')]
from cakood.p12_model import P12World,P12Context,CurrentRig,PEOPLE,PREREQUISITES,COURTYARD,LIVING,KITCHEN,PORCH,SIDE
from cakood.p10_model import CUE_IDS,TILE_IDS,PAPER_IDS,ORDER
from cakood.model import Verb
from cakood.verbal_contest import VerbalContests
from test_verbal_contest import CATALOG,prepared,play,leave
from codec import M,encode_world,encode_save,decode_words
import source_vm

def contests(resolved=True,win=False):
 w=VerbalContests(CATALOG)
 if resolved:prepared('VC03',w);play(w,[win]*3,'VC03');leave(w)
 return w
RIG=CurrentRig(COURTYARD,True,'MIC',True)
C=P12Context(COURTYARD,flags=PREREQUISITES,npc_locations=tuple((p,COURTYARD) for p in PEOPLE[1:]),rig=RIG,contests=contests())
A=replace(C,on_apron=True)
RACK=dict(rack_id='cue_rack',location=COURTYARD,slots=TILE_IDS,words=ORDER,first_restored_serial=1)
R={v:k for k,v in M['line_ids'].items()};U={v:k for k,v in M['speech_unit_ids'].items()};E={v:k for k,v in M['events'].items()};CO={v:k for k,v in M['codes'].items()};SO={v:k for k,v in M['sources'].items()};O={v:k for k,v in M['objects'].items()};W={v:k for k,v in M['words'].items()}
def oid(obj):return M['objects'].get(obj,32767)
def actors(c,**updates):return replace(c,npc_locations=tuple({**dict(c.npc_locations),**updates}.items()))
class ByteVM:
 def __init__(self):self.machine=Compiled(HERE,994,source_vm.DEFAULTS);self.p=source_vm.DEFAULTS.copy();self.call('p12Init')
 def call(self,name,*args):
  if any(type(x) is not int or not -32768<=x<=32767 for x in args):raise ValueError('SCI argument')
  if name not in source_vm.SIGNATURES or len(args)!=source_vm.SIGNATURES[name]:raise ValueError('Method/arity')
  return self.machine.execute(name,self.p,args)
 def persistent(self):return {k:self.p[k] for k in M['persisted_properties']}

class Harness:
 def __init__(self,typ=source_vm.VM,world=None):
  self.w=world or P12World();self.v=typ();self.v.p.update(encode_world(self.w));self.epoch=1;self.context=None
 def project(self,c=C):
  if self.context==c:return
  self.context=c;self.epoch+=1
  rooms=dict(c.npc_locations)
  args=[M['rooms'][c.room],int(c.on_apron),*[int(x in c.flags) for x in ('EVENING_STARTED','CUES_RESTORED','DISPLAY_STAGED','HELP_ACCEPTED')],M['rooms'][c.rig.location],int(c.rig.connected),int(c.rig.source=='MIC'),int(c.rig.facing_inward),int(c.contest_active),int(c.resolved('VC03')),*[M['rooms'][rooms[p]] if p in rooms else -1 for p in PEOPLE[1:]],self.epoch]
  assert self.v.call('p12Context',*args)==1
  for obj in c.inventory:assert self.v.call('p12ContextItem',oid(obj))==1
 def events(self):
  events=[]
  for i in range(self.v.p['p12EventCount']):
   name=E[self.v.call('p12Event',i)];a,b,c,d=[self.v.call('p12EventArg',i,j) for j in range(4)]
   data={'serial':self.v.call('p12EventSerialHi',i)*32768+self.v.call('p12EventSerialLo',i),'puzzle':'P12'}
   assert d==0
   if name=='P12_PRESENTATION_QUEUED':data['source']=SO[a];kind='presentation';assert b==c==0
   elif name=='P12_PRESENTED':data.update(source=SO[a],canonical_tokens=tuple(x['token'] for x in M['receipts'][SO[a]][b:c+1]));kind='presentation'
   elif name=='P12_RACK_HANDOFF':data.update(owner='P12',previous_owner='P10',object_ids=('cue_rack',O[a],O[b],O[c]));kind='ownership'
   elif name=='P12_CUES_REORDERED':data['words']=(W[a],W[b],W[c]);kind='object'
   else:
    assert a==b==c==0
    kind={'P12_CATCH_RELEASED':'object','P12_RACK_ROTATED':'object','P12_INTRODUCTION_CLEAR':'puzzle','P12_CONFETTI':'presentation','LAF12':'laugh','P12_COLLECTION_POINTS':'movement'}[name]
    if name=='P12_CONFETTI':data['covered_panel_unchanged']=True
    if name=='LAF12':data['after_record']='P12.DIALOGUE.004'
    if name=='P12_COLLECTION_POINTS':data.update(destinations={'bunny':KITCHEN,'frankie':LIVING,'rita':SIDE,'felix':SIDE,'vivian':SIDE,'milo':PORCH},panel_covered=True)
   events.append((name,kind,data))
  return events
 def check(self,r):
  assert self.v.persistent()==encode_world(self.w),(r.code,'state')
  assert CO[self.v.p['p12Code']]==r.code,(CO[self.v.p['p12Code']],r.code)
  assert tuple(R[self.v.call('p12Line',i)] for i in range(self.v.p['p12LineCount']))==r.line_ids
  assert tuple(U[self.v.call('p12Unit',i)] for i in range(self.v.p['p12UnitCount']))==r.speech_unit_ids
  assert self.events()==[(x.id,x.kind,x.payload) for x in r.events],(self.events(),r.events)
  source=self.v.p['p12PresentationSource'];pid=f"P12:{SO[source]}:{self.v.p['p12PresentationHi']*32768+self.v.p['p12PresentationLo']}" if source else None
  expected=':'.join(r.presentation_id.split(':')[0:1]+r.presentation_id.split(':')[2:]) if r.presentation_id else None
  assert pid==expected,(pid,expected)
  return r
 def action(self,model,native,*args,c=C):
  self.project(c);r=getattr(self.w,model)(c,*args);native_args=args
  if model=='start':
   h=args[0];native_args=(oid(h['rack_id']),M['rooms'][h['location']],*divmod(h['first_restored_serial'],32768),*[oid(x) for x in h['slots']],*[M['words'][x] for x in h['words']])
  elif model in ('begin_presentation','resume_presentation'):native_args=(M['sources'][args[0]],)
  elif model=='order_cards':native_args=tuple(oid(x) for x in args[0])
  elif model=='choose_introduction':native_args=({'complete':1,'partnerships':2,'partners':3}[args[0] if args else 'complete'],)
  elif model=='view':native_args=(int(args[0]) if args else 0,)
  elif model=='dispatch':native_args=(list(Verb).index(Verb(args[0]))+1,oid(args[1]),oid(args[2]) if len(args)>2 and args[2] else 0)
  self.v.call(native,*native_args);return self.check(r)
 def begin(self,s,c=C):return self.action('begin_presentation','p12Begin',s,c=c)
 def resume(self,s,c=C):return self.action('resume_presentation','p12Resume',s,c=c)
 def ack(self,s,record=None,units=(),c=C):
  self.project(c);p=self.w.presentations[s];sid=M['sources'][s];self.v.call('p12Resume',sid)
  r=self.w.acknowledge_presentation(c,self.w._handle(s),record_id=record,speech_unit_ids=units)
  self.v.call('p12Acknowledge',sid,*divmod(p.serial,32768),self.epoch,M['line_ids'][record] if record else 0,M['speech_unit_ids'][units[0]] if units else 0,M['speech_unit_ids'][units[-1]] if units else 0)
  return self.check(r)
 def show(self,s,c=C):self.begin(s,c);return self.ack(s,record=self.w.SOURCES[s],c=c)
 def start(self,c=C,rack=RACK):return self.action('start','p12Handoff',rack,c=c)
 def repair(self,c=C,rack=RACK,ask=False):
  self.start(c,rack);a=replace(c,on_apron=True);self.show('audience_view' if ask else 'self_view',a)
  self.action('release_catch','p12ReleaseCatch',c=a);self.action('rotate_rack','p12Rotate',c=c)
  slots=tuple(sorted(self.w.slots,key=lambda x:ORDER.index(self.w.words[x])))
  self.action('order_cards','p12Order',slots,c=c)
 def introduction(self,c=C):self.repair(c);self.show('introduction',c);self.action('commit_introduction','p12CommitIntroduction',c=c)
 def confetti(self,c=C):self.introduction(c);self.action('release_confetti','p12ReleaseConfetti',c=c);self.show('confetti',c)
 def restore(self):
  self.w=P12World.load(decode_words(list(self.v.persistent().values())));assert self.v.call('p12AfterRestore')==1;self.context=None
 def queries(self):
  before=self.v.persistent()
  assert tuple(R[x] for i in range(len(self.w.journal_records())+1) if (x:=self.v.call('p12JournalAt',i,0)))==self.w.journal_records()
  assert tuple(U[x] for i in range(len(self.w.journal_units())+1) if (x:=self.v.call('p12JournalAt',i,1)))==self.w.journal_units()
  assert tuple(SO[x] for i in range(len(self.w.presentations)+1) if (x:=self.v.call('p12PendingAt',i)))==tuple(s for s,p in sorted(self.w.presentations.items(),key=lambda kv:kv[1].serial) if not self.w._complete(s))
  assert bool(self.v.call('p12Ready'))==self.w.ready
  assert bool(self.v.call('p12WelcomeCleared'))==bool(self.w.collection_at)
  assert bool(self.v.call('p12Viewed'))==self.w.viewed
  assert {O[x] for i in range(5) if (x:=self.v.call('p12ReservedAt',i))}==self.w.reserved_external_objects
  if self.w.start_at:assert tuple(W[self.v.call('p12VisibleWord',i)] for i in range(3))==self.w.visible_order
  assert before==self.v.persistent()

class DomainTests(unittest.TestCase):
 VM=source_vm.VM
 def h(self,world=None):return Harness(self.VM,world)
 def test_safe_prerequisites_actual_rack_single_handoff(self):
  for flag in PREREQUISITES:
   h=self.h();h.start(replace(C,flags=C.flags-{flag}));self.assertFalse(h.w.start_at)
  for ids in (TILE_IDS,PAPER_IDS,(TILE_IDS[0],PAPER_IDS[1],TILE_IDS[2])):
   h=self.h();h.start(rack={**RACK,'slots':ids});self.assertEqual(h.w.visible_order,('SHOW','SERVE','TOAST'));h.start();h.queries()
 def test_view_release_orders_all_card_orders_and_materials(self):
  for ask,first,ids in itertools.product((False,True),('view','release'),(TILE_IDS,PAPER_IDS,(TILE_IDS[2],PAPER_IDS[0],TILE_IDS[0]))):
   h=self.h();h.start(rack={**RACK,'slots':ids});a=A
   if first=='release':h.action('release_catch','p12ReleaseCatch',c=a);h.action('rotate_rack','p12Rotate')
   h.show('audience_view' if ask else 'self_view',a)
   h.action('release_catch','p12ReleaseCatch',c=a);h.action('rotate_rack','p12Rotate')
   for perm in itertools.permutations(ids):
    h.action('order_cards','p12Order',perm);h.queries()
    self.assertEqual(bool(h.v.call('p12RackCorrect')),h.w.visible_order==ORDER)
   h.action('order_cards','p12Order',ids);h.action('choose_introduction','p12Choose','complete');h.action('order_cards','p12Order',tuple(reversed(ids)));h.queries()
 def test_apron_rotated_state_routes_and_rehearsal_without_vc03(self):
  c=replace(C,contests=contests(False));a=replace(c,on_apron=True);h=self.h();h.start(c)
  for s in ('opening','rack','diagram','edge'):h.show(s,c)
  for s in ('audience_view','self_view','catch','rehearsal'):h.show(s,a)
  h.action('release_catch','p12ReleaseCatch',c=a);h.action('rotate_rack','p12Rotate',c=c);h.action('order_cards','p12Order',TILE_IDS,c=c)
  for s in M['sources']:h.begin(s,a if s in ('audience_view','self_view','catch','rehearsal') else c)
  h.action('choose_introduction','p12Choose','complete',c=c);self.assertFalse(h.w.ready);h.queries()
 def test_current_rig_resolved_loss_and_truthful_choices(self):
  h=self.h();h.repair()
  for rig in (replace(RIG,location=LIVING),replace(RIG,connected=False),replace(RIG,source='TAPE'),replace(RIG,facing_inward=False)):
   h.action('choose_introduction','p12Choose','complete',c=replace(C,rig=rig))
  h.action('choose_introduction','p12Choose','partnerships');h.action('choose_introduction','p12Choose','partners')
  h.action('choose_introduction','p12Choose','partnerships',c=actors(C,vivian=LIVING));h.action('choose_introduction','p12Choose','partners',c=actors(C,bunny=LIVING))
  h.action('choose_introduction','p12Choose','complete',c=replace(C,contests=contests(False),flags=C.flags|{'VC03_RESOLVED'}))
  h.show('introduction');h.action('commit_introduction','p12CommitIntroduction',c=replace(C,rig=replace(RIG,connected=False)))
  h.action('commit_introduction','p12CommitIntroduction');self.assertTrue(h.w.ready);self.assertFalse(C.contests.progress['VC03'].won)
 def test_all_introduction_prefixes_restoration_cancel_audio(self):
  for prefix in range(9):
   h=self.h();h.repair();h.begin('introduction');tokens=h.w._tokens('introduction');old=h.epoch;p=h.w.presentations['introduction'];sid=M['sources']['introduction']
   if prefix:h.ack('introduction',units=tokens[:prefix])
   h.v.call('p12AudioFinished');h.check(h.w.audio_finished());self.assertFalse(h.w.ready)
   h.restore();h.project();before=h.v.persistent()
   h.v.call('p12Acknowledge',sid,*divmod(p.serial,32768),old,M['line_ids']['P12.DIALOGUE.002'],0,0);self.assertEqual(CO[h.v.p['p12Code']],'stale_presentation');self.assertEqual(before,h.v.persistent())
   h.action('commit_introduction','p12CommitIntroduction')
   if prefix<8:h.resume('introduction');h.ack('introduction',units=tokens[prefix:])
   h.action('commit_introduction','p12CommitIntroduction');self.assertTrue(h.w.ready);h.queries()
  h=self.h();h.repair();h.begin('introduction');h.ack('introduction',units=h.w._tokens('introduction')[:2]);p=h.w.presentations['introduction'];epoch=h.epoch
  r=h.w.cancel_presentation(h.w._handle('introduction'));h.v.call('p12Cancel',sid,*divmod(p.serial,32768),epoch);h.check(r);h.context=None;h.resume('introduction');h.show('introduction');h.queries()
 def test_all_source_prefixes_real_speakers_and_partial_reader(self):
  for source in M['sources']:
   total=len(P12World()._tokens(source));base=self.h()
   if source=='cleanup':base.confetti()
   elif source=='confetti':base.introduction();base.action('release_confetti','p12ReleaseConfetti')
   elif source=='introduction':base.repair()
   else:base.start()
   for prefix in range(total+1):
    h=self.h(P12World.load(base.w.save()))
    c=A if source in ('audience_view','self_view','catch','rehearsal') else C
    h.begin(source,c);tokens=h.w._tokens(source)
    if prefix:
     if source=='diagram':h.ack(source,record=h.w.SOURCES[source],c=c)
     else:h.ack(source,units=tokens[:prefix],c=c)
    h.restore();h.resume(source,c)
    if prefix<total:h.ack(source,record=h.w.SOURCES[source],c=c)
    if prefix==total:h.queries()
  h=self.h();h.repair();h.begin('introduction');away=actors(C,stringer=LIVING,rita=LIVING)
  h.ack('introduction',units=h.w._tokens('introduction')[:6],c=away)
  h.ack('introduction',record='P12.DIALOGUE.002',c=away);h.ack('introduction',record='P12.DIALOGUE.002');h.queries()
 def test_harmless_once_only_confetti_laugh_and_collection(self):
  h=self.h();h.start();h.action('claim_laugh','p12ClaimLaugh');h.action('release_confetti','p12ReleaseConfetti');h.action('finish_welcome','p12FinishWelcome')
  h.repair();h.show('introduction');h.action('commit_introduction','p12CommitIntroduction');h.action('claim_laugh','p12ClaimLaugh')
  for p in PEOPLE[1:]:h.action('release_confetti','p12ReleaseConfetti',c=actors(C,**{p:LIVING}))
  h.action('release_confetti','p12ReleaseConfetti');h.action('release_confetti','p12ReleaseConfetti');h.action('claim_laugh','p12ClaimLaugh');h.begin('cleanup')
  h.show('confetti');h.action('claim_laugh','p12ClaimLaugh');h.restore();h.action('claim_laugh','p12ClaimLaugh');h.show('cleanup');h.action('finish_welcome','p12FinishWelcome');h.restore();h.action('finish_welcome','p12FinishWelcome');h.queries()
  self.assertNotIn('DISPLAY_REVEALED',h.w.flags)
  h=self.h();h.confetti();h.show('cleanup');h.action('finish_welcome','p12FinishWelcome');h.action('claim_laugh','p12ClaimLaugh');self.assertFalse(h.w.laugh_at)
 def test_context_gates_and_inventory_conservation(self):
  for c in (replace(C,room=LIVING),A,replace(C,contests=contests(False))):
   h=self.h();h.start(c);h.begin('opening',c);h.action('rotate_rack','p12Rotate',c=c)
  h=self.h();h.start();h.project(C);self.assertEqual(h.v.call('p12ValidateContext'),1)
  for obj in ('cue_rack',*TILE_IDS):
   h.project(replace(C,inventory=frozenset((obj,))));self.assertEqual(h.v.call('p12ValidateContext'),0)
   before=h.v.persistent();h.v.call('p12Rotate');self.assertEqual(CO[h.v.p['p12Code']],'invalid_context');self.assertEqual(before,h.v.persistent())
  for flag in PREREQUISITES:h.project(replace(C,flags=C.flags-{flag}));self.assertEqual(h.v.call('p12ValidateContext'),0)
  h=self.h();h.introduction();h.project(replace(C,contests=contests(False)));self.assertEqual(h.v.call('p12ValidateContext'),0)
 def test_dispatch_queries_hints_and_unknowns(self):
  h=self.h();h.start()
  for verb,obj in itertools.product(Verb,('audience','cue_rack','swivel_release_catch','rack_rotating_handle','microphone','unknown')):h.action('dispatch','p12Act',verb,obj)
  h.action('dispatch','p12Act',Verb.LOOK_AT,'cue_rack',c=A);h.action('dispatch','p12Act',Verb.TALK_TO,'audience',c=A)
  for level in (1,2,3):h.action('hint','p12Hint',level,c=replace(C,room=LIVING));h.queries()
 def test_invalid_prefix_lease_context_and_signed_word_limits(self):
  h=self.h();h.repair();h.begin('introduction');sid=M['sources']['introduction'];p=h.w.presentations['introduction'];before=h.v.persistent();record=M['line_ids']['P12.DIALOGUE.002'];u=[M['speech_unit_ids'][t] for t in h.w._tokens('introduction')]
  for a in [(sid,0,p.serial,h.epoch,record,1,1),(sid,0,p.serial,h.epoch,0,u[2],u[3]),(sid,0,p.serial+1,h.epoch,record,0,0),(sid,0,p.serial,h.epoch+1,record,0,0),(sid,0,p.serial,h.epoch,0,u[3],u[1])]:
   h.v.call('p12Acknowledge',*a);self.assertIn(CO[h.v.p['p12Code']],('invalid_argument','stale_presentation'));self.assertEqual(before,h.v.persistent())
  h.v.call('p12Invalidate');h.context=None;h.project();h.v.call('p12Acknowledge',sid,0,p.serial,h.epoch-1,record,0,0);self.assertEqual(CO[h.v.p['p12Code']],'stale_presentation')
  h.resume('introduction');h.show('introduction');h.queries()
  for x in (True,'1',1.0,32768,-32769):
   with self.assertRaises(ValueError):h.v.call('p12Hint',x)
  for x in (-1,0,4,32767):
   h.v.call('p12Hint',x);self.assertEqual(CO[h.v.p['p12Code']],'invalid_argument')
 def test_invalid_handoffs_active_contest_and_exact_getter_bounds(self):
  h=self.h();h.project();base=[oid('cue_rack'),4,0,1,*[oid(x) for x in TILE_IDS],1,2,3];before=h.v.persistent()
  for i,x in ((0,oid('board')),(1,1),(2,-1),(3,0),(4,oid('board')),(5,oid(TILE_IDS[0])),(7,0),(8,1),(9,4)):
   args=base.copy();args[i]=x;h.v.call('p12Handoff',*args);self.assertEqual(CO[h.v.p['p12Code']],'invalid_argument');self.assertEqual(before,h.v.persistent())
  h.project(replace(C,inventory=frozenset((TILE_IDS[0],))));h.v.call('p12Handoff',*base);self.assertEqual(CO[h.v.p['p12Code']],'invalid_context');self.assertEqual(before,h.v.persistent())
  vc=prepared('VC03');vc.enter('VC03',0,admitted=True);active=replace(C,contests=vc);h.start(active);h.start();h.begin('opening',active);h.action('release_confetti','p12ReleaseConfetti',c=active)
  h.queries();before=h.v.persistent()
  for method in ('p12Line','p12Unit','p12Event','p12EventSerialHi','p12EventSerialLo','p12SlotAt','p12VisibleWord','p12ReservedAt','p12PendingAt'):
   for index in (-1,32767):self.assertEqual(h.v.call(method,index),0)
  for a,b in ((-1,0),(0,-1),(0,4),(1,0),(32767,32767)):self.assertEqual(h.v.call('p12EventArg',a,b),0)
  self.assertEqual(before,h.v.persistent())
 def test_serial_carry_exhaustion_and_pure_actions(self):
  h=self.h(P12World(revision=32767));h.start();self.assertEqual(h.w.start_at,32768);h.show('self_view',A);h.restore();h.queries()
  h=self.h(P12World(revision=M['max_serial']));h.project();before=h.v.persistent()
  h.v.call('p12Handoff',oid('cue_rack'),4,0,1,*[oid(x) for x in TILE_IDS],1,2,3);self.assertEqual(CO[h.v.p['p12Code']],'serial_exhausted');self.assertEqual(before,h.v.persistent())
  h.action('hint','p12Hint',1);h.v.call('p12AudioFinished');h.check(h.w.audio_finished())

if __name__=='__main__':unittest.main()
