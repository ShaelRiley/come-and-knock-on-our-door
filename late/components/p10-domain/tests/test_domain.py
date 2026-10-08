"""One exact oracle suite runs both generated SCI source and emitted SCI instructions."""
from pathlib import Path
import sys,json,unittest,random,copy,itertools,hashlib
from dataclasses import replace
HERE=Path(__file__).resolve().parents[1];ROOT=HERE/'reference'
sys.path[:0]=[str(HERE),str(ROOT)]
from cakood.p10_model import P10World,P10Context,LIVING,KITCHEN,COURTYARD,ORDER,TILE_IDS,PAPER_IDS,CUE_IDS,RECORD_UNITS,CHOICE_IDS
from cakood.model import Verb
from codec import M,encode_world,encode_save,decode_words
import source_vm
from compiled_vm import Compiled
C=P10Context(LIVING,flags=frozenset(('EVENING_STARTED',)),inventory=frozenset((*TILE_IDS,'grease_pencil','master_invitation')))
RACK=replace(C,room=COURTYARD,bunny_room=COURTYARD,frankie_room=COURTYARD)
KNOWN=replace(C,flags=C.flags|{'KNOW_CUE_ORDER'})
R={v:k for k,v in M['line_ids'].items()};U={v:k for k,v in M['speech_unit_ids'].items()}
E={v:k for k,v in M['events'].items()};CO={v:k for k,v in M['codes'].items()};SO={v:k for k,v in M['sources'].items()}
O={v:k for k,v in M['objects'].items()};W={0:None,**{v:k for k,v in M['words'].items()}}

def oid(obj):return M['objects'].get(M['object_aliases'].get(obj,obj),32767) if obj else 0

class ByteVM:
 def __init__(self):
  self.machine=Compiled(HERE,992,source_vm.DEFAULTS);self.p=source_vm.DEFAULTS.copy();self.call('p10Init')
 def call(self,name,*args):
  if any(type(x) is not int or not -32768<=x<=32767 for x in args):raise ValueError('SCI arguments require signed words')
  if name not in source_vm.SIGNATURES or len(args)!=source_vm.SIGNATURES[name]:raise ValueError('Invalid method/arity')
  return self.machine.execute(name,self.p,args)
 def persistent(self):return {k:self.p[k] for k in M['persisted_properties']}

class Harness:
 def __init__(self,typ=source_vm.VM,world=None):
  self.w=world or P10World();self.v=typ();self.v.p.update(encode_world(self.w));self.epoch=1;self.context=None
 def project(self,c):
  if self.context==c:return
  self.context=c;self.epoch+=1
  a=[M['rooms'][c.room],int(c.on_apron),int('EVENING_STARTED' in c.flags),int('KNOW_CUE_ORDER' in c.flags),M['rooms'][c.bunny_room],M['rooms'][c.frankie_room],M['rooms'][c.rita_room],int(c.contest_active),int('CUES_RESTORED' in c.flags),self.epoch]
  assert self.v.call('p10Context',*a)==1
  for obj in c.inventory:assert self.v.call('p10ContextItem',oid(obj))==1
 def events(self):
  events=[]
  for i in range(self.v.p['p10EventCount']):
   name=E[self.v.call('p10Event',i)];a,b,c,d=[self.v.call('p10EventArg',i,j) for j in range(4)]
   serial=self.v.call('p10EventSerialHi',i)*32768+self.v.call('p10EventSerialLo',i)
   data={'serial':serial,'puzzle':'P10'}
   if name=='P10_PRESENTATION_QUEUED':data['source']=SO[a];kind='presentation';assert b==c==d==0
   elif name=='P10_PRESENTED':
    source=SO[a];data.update(source=source,canonical_tokens=tuple(x['token'] for x in M['receipts'][source][b:c+1]));kind='presentation';assert d==0
   elif name=='P10_BREAD_SERVED':data.update(edible_only=True,tray_id='tray',consumed='bread_samples',plan_preserved=True);kind='object';assert a==b==c==d==0
   elif name=='P10_PAPER_PREPARED':data.update(items=PAPER_IDS,source='master_invitation',original_preserved=True,copies=1);kind='inventory';assert a==b==c==d==0
   elif name=='P10_CUE_WRITTEN':data.update(cue=O[a],word=W[b],icon=W[b],restored_first_time=bool(c));kind='object';assert d==0
   elif name=='P10_CUE_PLACED':data.update(item=O[a],origin='inventory' if d==1 else 'cue_rack',destination='cue_rack',slot=b,restored_first_time=bool(c));kind='inventory_transfer';assert d in (1,2)
   elif name=='P10_CUE_REMOVED':data.update(item=O[a],origin='cue_rack',destination='inventory');kind='inventory_transfer';assert b==c==d==0
   else:data['level']=a;kind='hint';assert b==c==d==0
   events.append((name,kind,data))
  return events
 def check(self,result):
  assert self.v.persistent()==encode_world(self.w),(result.code,'state',self.v.persistent(),encode_world(self.w))
  assert CO[self.v.p['p10Code']]==result.code,(CO[self.v.p['p10Code']],result.code)
  lines=tuple(R[self.v.call('p10Line',i)] for i in range(self.v.p['p10LineCount']))
  units=tuple(U[self.v.call('p10Unit',i)] for i in range(self.v.p['p10UnitCount']))
  assert lines==result.line_ids,(lines,result.line_ids)
  assert units==result.speech_unit_ids,(units,result.speech_unit_ids)
  assert self.events()==[(e.id,e.kind,e.payload) for e in result.events],(self.events(),result.events)
  source=self.v.p['p10PresentationSource']
  pid=f"P10:{SO[source]}:{self.v.p['p10PresentationHi']*32768+self.v.p['p10PresentationLo']}" if source else None
  expected=':'.join(result.presentation_id.split(':')[0:1]+result.presentation_id.split(':')[2:]) if result.presentation_id else None
  assert pid==expected,(pid,expected)
  return result
 def action(self,model,native,*args,c=C):
  self.project(c);result=getattr(self.w,model)(c,*args);native_args=args
  if model in ('begin_presentation','resume_presentation'):native_args=(M['sources'][args[0]],)
  elif model=='look':native_args=(oid(args[0]),)
  elif model=='write':native_args=(oid(args[0]),M['words'][args[1]] if args[1] else 0)
  elif model=='place':native_args=(oid(args[0]),args[1])
  elif model=='act':native_args=(list(Verb).index(Verb(args[0]))+1,oid(args[1]),M['topic_targets'].get(args[2],oid(args[2])) if len(args)>2 else 0)
  self.v.call(native,*native_args);return self.check(result)
 def begin(self,source,c=C):return self.action('begin_presentation','p10Begin',source,c=c)
 def resume(self,source,c=C):return self.action('resume_presentation','p10Resume',source,c=c)
 def ack(self,source,record=None,units=(),c=C):
  self.project(c);p=self.w.presentations[source];sid=M['sources'][source]
  # Re-arm the exact saved source after a changed physical context.
  self.v.call('p10Resume',sid)
  r=self.w.acknowledge_presentation(c,self.w._handle(source),record_id=record,speech_unit_ids=units)
  hi,lo=divmod(p.serial,32768)
  self.v.call('p10Acknowledge',sid,hi,lo,self.epoch,M['line_ids'][record] if record else 0,M['speech_unit_ids'][units[0]] if units else 0,M['speech_unit_ids'][units[-1]] if units else 0)
  return self.check(r)
 def show(self,source,c=C):
  self.begin(source,c)
  return self.ack(source,record=self.w.SOURCES[source],c=c)
 def prepare(self,paper=False):
  self.action('introduce','p10Introduce');self.show('plan')
  if paper:self.action('prepare_paper','p10PreparePaper')
  ids=PAPER_IDS if paper else TILE_IDS
  for obj,word in zip(ids,ORDER):self.action('write','p10Write',obj,word)
  return ids
 def restore(self):
  saved=decode_words(list(self.v.persistent().values()));self.w=P10World.load(saved)
  assert self.v.call('p10AfterRestore')==1
  self.context=None
 def queries(self):
  before=self.v.persistent()
  records=tuple(R[x] for i in range(8) if (x:=self.v.call('p10JournalAt',i,0)))
  units=tuple(U[x] for i in range(15) if (x:=self.v.call('p10JournalAt',i,1)))
  pending=tuple(SO[x] for i in range(8) if (x:=self.v.call('p10PendingAt',i)))
  assert records==self.w.journal_records(),(records,self.w.journal_records())
  assert units==self.w.journal_units(),(units,self.w.journal_units())
  assert pending==tuple(s for s,p in sorted(self.w.presentations.items(),key=lambda kv:kv[1].serial) if not self.w._complete(s))
  assert bool(self.v.call('p10Ready'))==self.w.ready
  assert bool(self.v.call('p10RackCorrect'))==self.w.rack_correct
  assert tuple(O[x] for i in range(4) if (x:=self.v.call('p10InventoryAt',i)))==self.w.inventory
  assert {O[x] for i in range(4) if (x:=self.v.call('p10ReservedAt',i))}==self.w.reserved_external_items
  slots=tuple(O[x] if (x:=self.v.call('p10SlotAt',i)) else None for i in range(3))
  words=tuple(W[self.v.call('p10LabelFor',self.v.call('p10SlotAt',i))] for i in range(3))
  handoff=None if not self.v.call('p10Ready') else dict(rack_id='cue_rack',location=COURTYARD,slots=slots,words=words,correct_now=bool(self.v.call('p10RackCorrect')),known_order=ORDER,built_in_clips=True,editable=True,first_restored_serial=self.v.p['p10RestoredHi']*32768+self.v.p['p10RestoredLo'])
  assert handoff==self.w.cue_handoff
  assert before==self.v.persistent()

class DomainTests(unittest.TestCase):
 VM=source_vm.VM
 def h(self,world=None):return Harness(self.VM,world)
 def test_both_materials_every_installation_order(self):
  for paper,order in itertools.product((False,True),itertools.permutations(range(3))):
   h=self.h();ids=h.prepare(paper)
   for i in order:h.action('place','p10Place',ids[i],i,c=RACK);h.restore()
   self.assertTrue(h.w.ready);h.queries()
 def test_all_material_mixes_and_historical_edits(self):
  for bits in itertools.product((0,1),repeat=3):
   h=self.h();h.prepare();h.action('prepare_paper','p10PreparePaper')
   ids=tuple((PAPER_IDS if bits[i] else TILE_IDS)[i] for i in range(3))
   for i,obj in enumerate(ids):h.action('write','p10Write',obj,ORDER[i]);h.action('place','p10Place',obj,i,c=RACK)
   original=h.w.restored_at
   h.action('write','p10Write',ids[0],'TOAST',c=RACK);h.queries()
   h.action('write','p10Write',ids[0],None,c=RACK);h.action('write','p10Write',ids[0],'SERVE',c=RACK)
   h.action('remove','p10Remove',0,c=RACK);h.queries();h.action('place','p10Place',ids[0],0,c=RACK)
   self.assertEqual(original,h.w.restored_at);h.queries()
 def test_all_wrong_orders_repair_and_moves(self):
  for order in itertools.permutations(range(3)):
   h=self.h();ids=h.prepare()
   for slot,i in enumerate(order):h.action('place','p10Place',ids[i],slot,c=RACK)
   for i in range(3):h.action('remove','p10Remove',i,c=RACK)
   h.action('place','p10Place',ids[0],0,c=RACK);h.action('place','p10Place',ids[0],1,c=RACK)
   h.action('place','p10Place',ids[1],1,c=RACK);h.action('remove','p10Remove',1,c=RACK)
   for i,obj in enumerate(ids):h.action('place','p10Place',obj,i,c=RACK)
   self.assertTrue(h.w.rack_correct);h.queries()
 def test_read_barrier_prefixes_and_speakers(self):
  h=self.h();h.action('introduce','p10Introduce');h.action('introduce','p10Introduce')
  away=replace(C,bunny_room=COURTYARD)
  h.ack('intro',record='P10.OPEN.001',c=away)
  h.ack('intro',units=('P10.OPEN.001.01',),c=away);h.queries()
  h.resume('intro');h.ack('intro',units=('P10.OPEN.001.02','P10.OPEN.001.03'))
  h.ack('intro',record='P10.OPEN.001');h.ack('intro',record='P10.OPEN.001');h.begin('intro');h.resume('intro')
  h.action('look','p10Look','board');h.action('hint','p10Hint',3)
  h.action('write','p10Write',TILE_IDS[0],'SERVE');h.begin('plan')
  self.assertFalse(h.w.knows_order(C));h.ack('plan',record='P10.READ.001')
  self.assertTrue(h.w.knows_order(C));h.queries()
 def test_conservation_original_identities_and_master(self):
  h=self.h();h.action('pick_up_tiles','p10PickUpTiles');h.action('prepare_paper','p10PreparePaper');h.action('prepare_paper','p10PreparePaper')
  h.action('introduce','p10Introduce')
  pocket=set(C.inventory);ctx=replace(KNOWN,room=COURTYARD,bunny_room=COURTYARD,frankie_room=COURTYARD)
  for i,obj in enumerate(TILE_IDS):
   h.action('write','p10Write',obj,ORDER[i],c=replace(ctx,inventory=frozenset(pocket)))
   h.action('place','p10Place',obj,i,c=replace(ctx,inventory=frozenset(pocket)));pocket.remove(obj)
   current=replace(ctx,inventory=frozenset(pocket));h.project(current)
   h.w.validate_context(current);self.assertEqual(h.v.call('p10ValidateContext'),1)
   self.assertEqual(set(TILE_IDS),(pocket&set(TILE_IDS))|set(h.w.reserved_external_items))
  self.assertEqual(set(h.w.inventory),set(PAPER_IDS));self.assertIn('master_invitation',pocket)
  for i,obj in enumerate(TILE_IDS):
   h.action('remove','p10Remove',i,c=replace(ctx,inventory=frozenset(pocket)));pocket.add(obj)
  self.assertTrue(set(TILE_IDS)<=pocket);h.queries()
 def test_context_boundaries_and_exact_feedback(self):
  contexts=(replace(C,flags=frozenset()),replace(C,on_apron=True),replace(C,contest_active=True),replace(C,room=KITCHEN),replace(C,bunny_room=COURTYARD))
  for ctx in contexts:
   h=self.h()
   for source in M['sources']:h.begin(source,ctx)
   h.action('introduce','p10Introduce',c=ctx);h.action('prepare_paper','p10PreparePaper',c=ctx)
   h.action('pick_up_tiles','p10PickUpTiles',c=ctx);h.action('hint','p10Hint',1,c=ctx)
   h.action('look','p10Look','tray',c=ctx)
  h=self.h();h.prepare()
  h.action('write','p10Write',TILE_IDS[0],None)
  h.action('place','p10Place',TILE_IDS[0],0,c=RACK)
  h.action('place','p10Place',TILE_IDS[0],0,c=replace(RACK,bunny_room=LIVING))
  h.action('place','p10Place',TILE_IDS[2],0,c=replace(RACK,frankie_room=LIVING));h.action('remove','p10Remove',0,c=RACK)
  h.action('place','p10Place',TILE_IDS[2],0,c=RACK);h.action('remove','p10Remove',0,c=RACK)
  h.action('place','p10Place',TILE_IDS[1],0,c=RACK);h.queries()
 def test_outcome_sources_and_pure_choices(self):
  h=self.h();ids=h.prepare()
  for i,obj in enumerate(ids):h.action('place','p10Place',obj,i,c=RACK)
  h.begin('credit',RACK);h.show('credit',replace(RACK,rita_room=COURTYARD))
  h.show('bread_agreement',RACK);h.show('notebook',RACK);h.show('rack',RACK);h.show('tiles',RACK)
  h.project(RACK);before=h.v.persistent();h.v.call('p10Choices')
  self.assertEqual(tuple(R[h.v.call('p10Line',i)] for i in range(h.v.p['p10LineCount'])),tuple(CHOICE_IDS.values()))
  self.assertEqual(before,h.v.persistent());h.queries()
  h=self.h();h.action('write','p10Write',TILE_IDS[0],'SHOW',c=KNOWN);self.assertFalse(h.w.journal_records())
 def test_offscreen_reserved_tiles_and_host_flags(self):
  h=self.h();ids=h.prepare()
  for i,obj in enumerate(ids):h.action('place','p10Place',obj,i,c=RACK)
  away=replace(C,inventory=C.inventory-set(ids));present=replace(away,room=COURTYARD)
  h.begin('tiles',away);h.begin('tiles',present);h.ack('tiles',record='P10.LOOK.002',c=away);h.ack('tiles',record='P10.LOOK.002',c=present)
  h.project(RACK);self.assertEqual(h.v.call('p10ValidateContext'),0)
  h.project(present);self.assertEqual(h.v.call('p10ValidateContext'),1)
  h.project(replace(present,flags=frozenset()));self.assertEqual(h.v.call('p10ValidateContext'),0)
  h=self.h();h.project(replace(C,flags=C.flags|{'CUES_RESTORED'}));self.assertEqual(h.v.call('p10ValidateContext'),0)
 def test_material_prerequisites_and_non_consumption(self):
  h=self.h();empty=replace(KNOWN,inventory=frozenset())
  h.action('prepare_paper','p10PreparePaper',c=empty);h.action('pick_up_tiles','p10PickUpTiles',c=empty)
  h.action('write','p10Write',TILE_IDS[0],'SERVE',c=empty)
  h.action('write','p10Write',TILE_IDS[0],'SERVE',c=replace(KNOWN,inventory=frozenset(TILE_IDS)))
  h.action('write','p10Write',TILE_IDS[0],'SERVE',c=KNOWN)
  h.action('place','p10Place',TILE_IDS[0],0,c=replace(KNOWN,room=COURTYARD))
  h.action('prepare_paper','p10PreparePaper',c=KNOWN)
  h.action('prepare_paper','p10PreparePaper',c=empty)
  h.action('write','p10Write',PAPER_IDS[0],'SERVE',c=replace(KNOWN,inventory=frozenset(('grease_pencil',))))
  self.assertEqual(h.w.inventory,PAPER_IDS);self.assertFalse(h.w.bread_at)
  h.project(C);before=h.v.persistent();h.v.call('p10Choices')
  self.assertEqual(h.v.p['p10LineCount'],0);self.assertEqual(before,h.v.persistent());h.queries()
 def test_all_verbs_and_unknown_objects_are_safe(self):
  h=self.h()
  for verb,obj in itertools.product(Verb,('audience','renewal_repair_card','garbage','rack_spring_clips')):h.action('act','p10Act',verb,obj)
  for verb,obj,target in [(Verb.OPEN,'board',None),(Verb.OPEN,'notebook',None),(Verb.PICK_UP,'ceramic_sample_tiles',None),(Verb.USE,'master_invitation','cue_rack'),(Verb.TALK_TO,'bunny','cues'),(Verb.TALK_TO,'bunny','bread'),(Verb.TALK_TO,'rita','credit')]:h.action('act','p10Act',verb,obj,target)
 def test_stale_restore_cancel_wrong_prefix_and_types(self):
  h=self.h();h.action('introduce','p10Introduce');sid=M['sources']['intro'];p=h.w.presentations['intro'];before=h.v.persistent()
  for args in [(sid,0,p.serial,h.epoch,M['line_ids']['P10.HINT.1'],0,0),(sid,0,p.serial,h.epoch,0,M['speech_unit_ids']['P10.OPEN.001.02'],M['speech_unit_ids']['P10.OPEN.001.03']),(sid,0,p.serial+1,h.epoch,M['line_ids']['P10.OPEN.001'],0,0),(sid,0,p.serial,h.epoch+1,M['line_ids']['P10.OPEN.001'],0,0),(sid,0,p.serial,h.epoch,M['line_ids']['P10.OPEN.001'],1,1)]:
   h.v.call('p10Acknowledge',*args);self.assertIn(CO[h.v.p['p10Code']],('invalid_argument','stale_presentation'));self.assertEqual(before,h.v.persistent())
  old=h.epoch;h.v.call('p10Invalidate');self.assertEqual(h.v.p['p10EventCount'],0);self.assertEqual(h.v.p['p10LineCount'],0);self.assertEqual(h.v.p['p10PresentationSource'],0);h.v.call('p10Acknowledge',sid,0,p.serial,old,M['line_ids']['P10.OPEN.001'],0,0);self.assertEqual(CO[h.v.p['p10Code']],'invalid_context')
  h.context=None;h.resume('intro');h.v.call('p10Acknowledge',sid,0,p.serial,old,M['line_ids']['P10.OPEN.001'],0,0);self.assertEqual(CO[h.v.p['p10Code']],'stale_presentation')
  h.ack('intro',units=('P10.OPEN.001.01',));h.begin('plan');h.restore()
  self.assertEqual(h.v.p['p10ContextValid'],0);self.assertEqual(h.v.p['p10EventCount'],0)
  h.project(C);h.v.call('p10Acknowledge',sid,0,p.serial,old,M['line_ids']['P10.OPEN.001'],0,0);self.assertEqual(CO[h.v.p['p10Code']],'stale_presentation')
  h.ack('intro',record='P10.OPEN.001');h.ack('plan',record='P10.READ.001');h.queries()
  for invalid in (True,1.5,'1'):
   with self.assertRaises(ValueError):h.v.call('p10Remove',invalid)
 def test_serial_carry_exhaustion_and_atomic_intro(self):
  for revision in (32766,32767,32768):
   h=self.h(P10World(revision=revision));h.action('introduce','p10Introduce');h.show('plan');h.queries()
  for revision in (M['max_serial']-1,M['max_serial']):
   h=self.h(P10World(revision=revision));h.project(C);before=h.v.persistent();h.v.call('p10Introduce')
   self.assertEqual(CO[h.v.p['p10Code']],'serial_exhausted');self.assertEqual(before,h.v.persistent())
  h=self.h(P10World(revision=M['max_serial']-2));h.action('introduce','p10Introduce');before=h.v.persistent();h.v.call('p10Hint',1)
  self.assertEqual(CO[h.v.p['p10Code']],'serial_exhausted');self.assertEqual(before,h.v.persistent());h.action('introduce','p10Introduce')
 def test_invalid_context_inventory_bounds_and_getters(self):
  h=self.h();h.project(C)
  for method in ('p10Line','p10Unit','p10Event','p10EventSerialHi','p10EventSerialLo','p10InventoryAt','p10ReservedAt','p10SlotAt','p10CueAt'):
   for value in (-1,32767):self.assertEqual(h.v.call(method,value),0)
  for args in ((-1,0),(0,-1),(99,0),(0,4)):self.assertEqual(h.v.call('p10EventArg',*args),0)
  for obj in ('board','cue_rack',PAPER_IDS[0],'bunny'):
   h.context=None;h.project(C);self.assertEqual(h.v.call('p10ContextItem',oid(obj)),0);self.assertEqual(h.v.p['p10ContextValid'],0)
  h.context=None;h.project(C);self.assertEqual(h.v.call('p10ContextItem',124),0)
  for method,args in [('p10Write',(oid(TILE_IDS[0]),4)),('p10Write',(oid('renewal_repair_card'),1)),('p10Place',(oid(TILE_IDS[0]),3)),('p10Remove',(-1,)),('p10Hint',(0,)),('p10Begin',(0,))]:
   h.context=None;h.project(C);before=h.v.persistent();h.v.call(method,*args);self.assertEqual(CO[h.v.p['p10Code']],'invalid_argument');self.assertEqual(before,h.v.persistent())
 def test_seeded_reversible_action_parity(self):
  rng=random.Random(1010);h=self.h();h.prepare();h.action('prepare_paper','p10PreparePaper')
  for _ in range(100):
   method=rng.choice(('write','place','remove','hint','look'))
   if method=='write':h.action(method,'p10Write',rng.choice(CUE_IDS),rng.choice((None,*ORDER)),c=RACK)
   elif method=='place':h.action(method,'p10Place',rng.choice(CUE_IDS),rng.randrange(3),c=RACK)
   elif method=='remove':h.action(method,'p10Remove',rng.randrange(3),c=RACK)
   elif method=='hint':h.action(method,'p10Hint',rng.randint(1,3),c=RACK)
   else:h.action(method,'p10Look',rng.choice((*CUE_IDS,'cue_rack','board','tray')),c=RACK)
  h.queries()
 def test_deciding_operands_in_source_vm(self):
  v=source_vm.VM()
  self.assertEqual(v.ev(['or',0,17],{}),17);self.assertEqual(v.ev(['and',4,23],{}),23)

class CompiledDomainTests(DomainTests):VM=ByteVM

if __name__=='__main__':unittest.main()
