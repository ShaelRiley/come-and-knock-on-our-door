"""Independent native save rejection, source/model parity, all physical projections."""
from test_domain import *
import random
del DomainTests,BytecodeTests

def snapshots():
 w=P12World();out=[]
 def snap():out.append(w.save())
 def act(fn,*args,c=C):getattr(w,fn)(c,*args);snap()
 def show(source,c=C):
  act('begin_presentation',source,c=c)
  for token in w._tokens(source):
   if token in M['speech_unit_ids']:w.acknowledge_presentation(c,w._handle(source),speech_unit_ids=(token,))
   else:w.acknowledge_presentation(c,w._handle(source),record_id=token)
   snap()
 snap();act('start',RACK)
 for source in ('opening','rack','diagram','edge'):show(source)
 for source in ('audience_view','self_view','catch','rehearsal'):show(source,A)
 act('release_catch',c=A);act('rotate_rack');act('order_cards',TILE_IDS);show('introduction');act('commit_introduction');act('release_confetti');show('confetti');act('claim_laugh');show('cleanup');act('finish_welcome')
 return out

def model_valid(p):
 try:
  d=decode_words(list(p.values()));P12World.load(d)
  # A native vector is canonical only if no word was discarded by decoding.
  return encode_save(d)==p
 except (ValueError,KeyError,TypeError,IndexError):return False

class ValidationTests(unittest.TestCase):
 def test_emitted_validator_corrupt_saves_and_model_parity(self):
  states=[encode_save(s) for s in snapshots()];cases={tuple(p.values()):p for p in states};rng=random.Random(120994)
  def add(p,changes):
   q={**p,**changes};cases[tuple(q.values())]=q
  done=states[-1];empty=states[0]
  for key in M['persisted_properties']:
   add(done,{key:-1});add(done,{key:0})
  for source,id in M['sources'].items():
   name=M['serials'][id+7]
   add(done,{'p12'+name+'Hi':0,'p12'+name+'Lo':0})
   for b in M['receipts'][source]:
    name=M['serials'][b['slot']]
    add(empty,{'p12RevisionLo':3,'p12'+name+'Lo':2})
  for _ in range(180):
   p=rng.choice(states);key=rng.choice(M['persisted_properties']);add(p,{key:rng.choice((0,1,2,32767))})
  v=ByteVM();valid=invalid=0
  for p in cases.values():
   expected=model_valid(p);v.p.update(p);before=v.persistent();actual=bool(v.call('p12Validate'))
   self.assertEqual(actual,expected,('save parity',{k:x for k,x in p.items() if x!=done[k]}));self.assertEqual(before,v.persistent())
   if actual:valid+=1
   else:invalid+=1
  report={'scope':'Actual emitted script994 validation; all self sends and stack returns checked','reachable_snapshots':len(states),'distinct_vectors':len(cases),'valid':valid,'rejected':invalid,'instructions_executed':v.machine.steps,'script_sha256':hashlib.sha256(v.machine.blob).hexdigest(),'passed':True}
  (HERE/'evidence/compiled-validation.json').write_text(json.dumps(report,indent=2)+'\n')
 def test_all_720_physical_rack_projections_and_orientations(self):
  v=ByteVM();count=0
  # 20 cue subsets x6 assigned word orders x6 slot orders=720 physical projections.
  # Both audience-facing and released/observed inward orientations are validated.
  for cues in itertools.combinations(CUE_IDS,3):
   for words in itertools.permutations(ORDER):
    w=P12World();w.start(C,{**RACK,'slots':cues,'words':words})
    w.begin_presentation(A,'self_view');w.acknowledge_presentation(A,w._handle('self_view'),record_id='P12.LOOK.003');w.release_catch(A)
    for facing in (False,True):
     if facing:w.rotate_rack(C)
     for slots in itertools.permutations(cues):
      q=copy.deepcopy(w);q.slots=list(slots);q.validate();p=encode_world(q);v.p.update(p)
      self.assertEqual(v.call('p12Validate'),1);self.assertEqual(tuple(W[v.call('p12VisibleWord',i)] for i in range(3)),q.visible_order)
      self.assertEqual(bool(v.call('p12RackCorrect')),q.visible_order==ORDER);count+=1
  self.assertEqual(count,1440)
  (HERE/'evidence/finite-projection.json').write_text(json.dumps({'physical_projections':720,'orientation_projections':count,'actual_emitted_bytecode':True,'stack_balance':True,'passed':True},indent=2)+'\n')
 def test_strict_codec_malformed_types_and_restore_fail_closed(self):
  raw=snapshots()[-1]
  for value in (True,'1',1.1,-1,M['max_serial']+1):
   bad=copy.deepcopy(raw);bad['state']['revision']=value
   with self.assertRaises(ValueError):encode_save(bad)
  for key,value in [('kind','other'),('schema',True),('state',[]),('extra',1)]:
   bad=copy.deepcopy(raw);bad[key]=value
   with self.assertRaises(ValueError):encode_save(bad)
  for key,value in [('slots',['cue_rack']*3),('words',{'bad':'SERVE'}),('presentations',{'bad':{'serial':1,'receipts':{}}})]:
   bad=copy.deepcopy(raw);bad['state'][key]=value
   with self.assertRaises(ValueError):encode_save(bad)
  bad=copy.deepcopy(raw);p=bad['state']['presentations']['introduction'];p['receipts']=dict(reversed(list(p['receipts'].items())))
  with self.assertRaises(ValueError):encode_save(bad)
  for typ in (source_vm.VM,ByteVM):
   h=Harness(typ);h.repair();h.begin('introduction');h.project();p=encode_world(h.w);p['p12ReleaseLo']=0;h.v.p.update(p);self.assertEqual(h.v.call('p12AfterRestore'),0);self.assertEqual(h.v.p['p12ContextValid'],0)
   self.assertEqual(h.v.p['p12EventCount'],0);self.assertEqual(h.v.p['p12PresentationSource'],0)
   before=h.v.persistent();h.v.call('p12ReleaseConfetti');self.assertEqual(CO[h.v.p['p12Code']],'invalid_state');self.assertEqual(before,h.v.persistent())
 def test_context_words_and_unregistered_inventory_fail_closed(self):
  args=[4,0,1,1,1,1,4,1,1,1,0,1,4,4,4,4,4,4,4,1]
  for typ in (source_vm.VM,ByteVM):
   v=typ()
   for i in range(len(args)):
    for x in (-2,7,32767):
     if i==19 and x>0:continue
     bad=list(args);bad[i]=x
     if i!=19:bad[-1]=100+i*3+(x%3)
     self.assertEqual(v.call('p12Context',*bad),0)
   args[-1]=500;self.assertEqual(v.call('p12Context',*args),1)
   for obj in (0,93,115,394,409,421,32767,oid('jack'),oid('felix')):
    args[-1]+=1;self.assertEqual(v.call('p12Context',*args),1);self.assertEqual(v.call('p12ContextItem',obj),0);self.assertEqual(v.p['p12ContextValid'],0)
if __name__=='__main__':unittest.main()
