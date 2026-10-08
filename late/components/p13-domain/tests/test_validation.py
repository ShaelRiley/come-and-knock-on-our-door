"""NEW source/emitted adaptation of retained validation tests; actual bytecode execution."""
from test_domain import *
import random
del DomainTests,BytecodeTests
ByteVM=PairedVM  # Current paired source/emitted evaluator

def snapshots():
 w=P13World();out=[w.save()]
 def act(fn,*args,c=C):getattr(w,fn)(c,*args);out.append(w.save())
 def show(s,c=C):
  act('begin_presentation',s,c=c)
  for token in w._tokens(s):
   if token in M['speech_unit_ids']:w.acknowledge_presentation(c,w._handle(s),speech_unit_ids=(token,))
   else:w.acknowledge_presentation(c,w._handle(s),record_id=token)
   out.append(w.save())
 act('start',POT,DISPLAY)
 for source in ('opening','rack','serve_preview','show_preview','toast_preview','program','display_help','board_help'):show(source)
 show('pot_help',K);act('deliver_pot','house_doorway',c=K);show('wrong_pot',K)
 w.acknowledge_wrong_visual(K,w.pending_wrong_visual_id);out.append(w.save());act('claim_laugh',c=K)
 act('give_program',c=P);act('confirm_seating');act('deliver_pot',c=K);act('pull_serve');show('rita_ready');act('deliver_display',c=D);act('open_screen');show('reveal');act('pull_show');act('deliver_board',c=L);act('request_contest',c=B)
 w.finish_contest_request(w.pending_contest_request_id,True);out.append(w.save());show('attention',B);act('pull_toast',c=B)
 for req in tuple(w.pending_autosaves):w.acknowledge_autosave(req['request_id']);out.append(w.save())
 return out

def model_valid(p):
 try:
  d=decode_words(list(p.values()));P13World.load(d);return encode_save(d)==p
 except (ValueError,KeyError,TypeError,IndexError):return False

class ValidationTests(unittest.TestCase):
 def test_emitted_validator_corrupt_saves_and_exact_model_parity(self):
  states=[encode_save(s) for s in snapshots()];cases={tuple(p.values()):p for p in states};rng=random.Random(130995)
  def add(p,changes):q={**p,**changes};cases[tuple(q.values())]=q
  done=states[-1];empty=states[0]
  for key in M['persisted_properties']:add(done,{key:-1});add(done,{key:0})
  for source,id in M['sources'].items():
   name=M['serials'][id+18];add(done,{'p13'+name+'Hi':0,'p13'+name+'Lo':0})
   for b in M['receipts'][source]:add(empty,{'p13RevisionLo':3,'p13'+M['serials'][b['slot']]+'Lo':2})
  for _ in range(220):
   p=rng.choice(states);key=rng.choice(M['persisted_properties']);add(p,{key:rng.choice((0,1,2,32767))})
  v=ByteVM();valid=invalid=0
  for p in cases.values():
   expected=model_valid(p);v.p.update(p);before=v.persistent();actual=bool(v.call('p13Validate'))
   self.assertEqual(actual,expected,('save parity',{k:x for k,x in p.items() if x!=done[k]}));self.assertEqual(before,v.persistent())
   if actual:valid+=1
   else:invalid+=1
  (HERE/'evidence/source-validation.json').write_text(json.dumps({'scope':'Actual emitted SCI and source paired validator','reachable_snapshots':len(states),'distinct_vectors':len(cases),'valid':valid,'rejected':invalid,'source_sha256':hashlib.sha256((HERE/'src/module995.sc').read_bytes()).hexdigest(),'passed':True},indent=2)+'\n')
 def test_overlay_all_layout_states_all_cues(self):
  v=ByteVM();vocab={v:k for k,v in M['preview_vocabulary'].items()};count=0
  for bits in itertools.product((False,True),repeat=6):
   c=replace(C,queue_clear=bits[0],lane_clear=bits[1],footprint_clear=bits[2],buffet_at_hatch=bits[3],hatch_visible=bits[4],display_concealed=bits[5]);h=Harness(ByteVM);h.project(c);v=h.v
   for cue in ORDER:
    idx=M['words'][cue];fields=[v.call('p13PreviewWord',idx,i) for i in range(4)]
    actual={'cue':cue,'record_id':R[fields[0]],'load_ids':tuple(vocab[x] for x in fields[2:] if x),'destination_id':vocab[fields[1]],'route_ids':ROUTES,**M['preview_facts']}
    actual.update(zip(('guest_lane_occupied','gate_lane_occupied','footprint_occupied','buffet_ready'),(bool(v.call('p13PreviewMarker',i)) for i in range(4))))
    self.assertEqual(actual,h.w.route_preview(c,cue))
    line=v.call('p13BlockedLayout',idx);expected=h.w.blocked_layout_binding(c,cue)
    self.assertEqual(R[line] if line else None,expected.get('label_record_id'));count+=1
  self.assertEqual(count,192)
  (HERE/'evidence/finite-projection.json').write_text(json.dumps({'layout_states':64,'cue_projections':count,'actual_emitted_bytecode':True,'source_only':False,'passed':True},indent=2)+'\n')
 def test_transport_strict_types_keys_receipt_order_and_corrupt_restore(self):
  raw=snapshots()[-1]
  for value in (True,'1',1.1,-1,M['max_serial']+1):
   bad=copy.deepcopy(raw);bad['state']['revision']=value
   with self.assertRaises(ValueError):encode_save(bad)
  for key,value in [('kind','other'),('schema',True),('state',[]),('extra',1)]:
   bad=copy.deepcopy(raw);bad[key]=value
   with self.assertRaises(ValueError):encode_save(bad)
  for key,value in [('wrong_source','reveal'),('autosaves',{'SERVE':True}),('presentations',{'bad':{'serial':1,'receipts':{}}})]:
   bad=copy.deepcopy(raw);bad['state'][key]=value
   with self.assertRaises(ValueError):encode_save(bad)
  bad=copy.deepcopy(raw);p=bad['state']['presentations']['reveal'];p['receipts']=dict(reversed(list(p['receipts'].items())))
  with self.assertRaises(ValueError):encode_save(bad)
  for typ in (source_vm.VM,ByteVM):
   h=Harness(typ);h.serve();p=encode_world(h.w);p['p13PotLo']=0;h.v.p.update(p);self.assertEqual(h.v.call('p13AfterRestore'),0);self.assertEqual(h.v.p['p13ContextValid'],0)
   self.assertEqual(h.v.p['p13EventCount'],0);self.assertEqual(h.v.p['p13PresentationSource'],0)
   before=h.v.persistent();h.v.call('p13PullShow');self.assertEqual(CO[h.v.p['p13Code']],'invalid_state');self.assertEqual(before,h.v.persistent())
 def test_context_handoff_bounds_and_large_inventory_fail_closed(self):
  base=[4,0,1,1,1,1,1,1,1,1,1,1,1,1,1,4,1,1,1,0,0,4,4,4,4,4,4,4,1,56,3,1,1,1,1,0,1]
  handoff=[oid('hotpot_pot'),M['rooms'][KITCHEN],1,8,1,1,oid('folded_display'),oid('handcart'),M['rooms'][SIDE],1,1,1,1,1,0,0,13]
  for typ in (source_vm.VM,ByteVM):
   v=typ()
   for i in range(len(base)-1):
    if i==29:continue
    bad=base.copy();bad[i]=-2;bad[-1]=i+1;self.assertEqual(v.call('p13Context',*bad),0)
   for i,x in ((14,2),(29,57),(30,2),(31,0),(34,0)):
    bad=base.copy();bad[i]=x;bad[-1]=50+i;self.assertEqual(v.call('p13Context',*bad),0)
   base[-1]=100;self.assertEqual(v.call('p13Context',*base),1)
   for obj in (0,115,421,32767,oid('jack'),oid('felix'),oid('hotpot_pot'),oid('handcart'),oid('folded_display'),oid('pledge_board')):
    base[-1]+=1;self.assertEqual(v.call('p13Context',*base),1);self.assertEqual(v.call('p13ContextItem',obj),0)
   base[-1]+=1;self.assertEqual(v.call('p13Context',*base),1);before=v.persistent()
   for i,x in ((0,42),(1,1),(2,0),(3,7),(4,0),(5,0),(6,103),(7,42),(8,4),(9,0),(10,0),(11,0),(12,0),(13,0),(14,1),(15,1),(16,11)):
    bad=handoff.copy();bad[i]=x;v.call('p13Handoff',*bad);self.assertEqual(CO[v.p['p13Code']],'invalid_argument');self.assertEqual(before,v.persistent())

class RouteMatrixTests(unittest.TestCase):
 def test_all_premature_deliveries_at_each_canonical_stage(self):
  w=P13World();states=[w.save()]
  def act(fn,*args,c=C):getattr(w,fn)(c,*args);states.append(w.save())
  def show(s,c=C):w.begin_presentation(c,s);w.acknowledge_presentation(c,w._handle(s),record_id=w.SOURCES[s]);states.append(w.save())
  act('start',POT,DISPLAY);act('give_program',c=P);act('confirm_seating');act('deliver_pot',c=K);act('pull_serve');show('rita_ready');act('deliver_display',c=D);act('open_screen');show('reveal');act('pull_show');act('deliver_board',c=L);show('attention',B);act('pull_toast',c=B)
  cases=[('give_program','p13GiveProgram',(),P),('confirm_seating','p13ConfirmSeating',(),C),('deliver_pot','p13DeliverPot',(),K),('pull_serve','p13PullServe',(),C),('deliver_display','p13DeliverDisplay',(),D),('open_screen','p13OpenScreen',(),C),('pull_show','p13PullShow',(),C),('deliver_board','p13DeliverBoard',(),L),('request_contest','p13RequestContest',(),C),('begin_presentation','p13Begin',('attention',),C),('pull_toast','p13PullToast',(),C)]
  count=0
  for state in states:
   for fn,method,args,c in cases:
    h=Harness(ByteVM,P13World.load(state));cc=replace(c,board_room=COURTYARD if h.w.board_at else LIVING);h.action(fn,method,*args,c=cc);count+=1
  # Fixed objects and symbolic route/cue tokens occupy different dispatch namespaces.
  for typ in (source_vm.VM,ByteVM):
   h=Harness(typ);h.start()
   for verb,obj,target in [(Verb.PULL,'front_door',None),(Verb.PULL,'bunny',None),(Verb.PULL,'bench',None),(Verb.USE,'hotpot_pot','front_door'),(Verb.USE,'folded_display','bunny'),(Verb.PULL,'SERVE',None),(Verb.PULL,'SHOW',None),(Verb.PULL,'TOAST',None),(Verb.USE,'hotpot_pot','house_doorway')]:
    h.action('dispatch','p13Act',verb,obj,target,c=K if verb==Verb.USE else C)
  (HERE/'evidence/route-matrix.json').write_text(json.dumps({'canonical_stages':len(states),'candidate_operations':len(cases),'source_model_comparisons':count,'symbolic_dispatch_namespace_checked':True,'passed':True},indent=2)+'\n')

if __name__=='__main__':unittest.main()
