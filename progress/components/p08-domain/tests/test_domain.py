"""New explicit SCI parity, representation, publication and consistency tests."""
from copy import deepcopy
from dataclasses import replace
from itertools import product
from pathlib import Path
import hashlib,json,os,random,sys,tempfile,unittest
from adapter import *
from cakood.p08_model import P08World as Reference,PREPARATIONS,SCRIPT_BINDINGS,LABEL_IDS,StartPhase
from tests.current_api_support import Preparation
C=P08Context('L05_COURTYARD',flags=PREPARATIONS,carrier_padding='clean_towel',inventory=frozenset(('grease_pencil','ceramic_sample_tiles','wedge')),frankie_room='L05_COURTYARD',bunny_room='L05_COURTYARD')
DEST=dict(zip(LAYOUT_OBJECTS,(1,2,3,1,1)))
BACKENDS=(FastSourceWorld,FastEmittedWorld)
METRICS={'vectors':0,'finite_layouts':0,'restore_roundtrips':0,'raw_rejections':0,'boundary_vectors':0,'slow_crosscheck_calls':0,'composition_cloths':0,'context_cases':0,'capacity_failures':0,'validation_mutations':0}
def fit(cls,c=C):
 w=cls()
 for obj,pos in DEST.items():w.place(c,obj,pos)
 w.unpack_service(c)
 for h in w.pending_handoffs:w.acknowledge_handoff(h['handoff_id'],h['serial'])
 return w
def start(w,c=C):
 w.request_start(c);token=w.pending_request_id;w.acknowledge_readiness(c,token,READINESS_RECORDS);w.confirm_start(c,token,True);return token

def state(w):return w._state() if isinstance(w,SciWorld) else w.save()['state']
def set_live(vm,words):
 if hasattr(vm,'locals'):
  start_,size=vm.array_ranges['p08Words'];vm.locals[start_:start_+size]=words
 else:vm.arrays['p08Words'][:]=words

def check_units(test,w,result):
 output=w.vm.arrays['p08Output'];units=tuple(UNIT[x] for x in output[O['units']:O['units']+output[O['unit_count']]])
 fixture=json.loads((H/'fixtures/canonical-bindings.json').read_text())
 expected=tuple(u for r in result.line_ids for u in fixture['records'][r]['speech_units'])
 test.assertEqual(units,expected)

class DomainTests(unittest.TestCase):
 def compare(self,ref,world,name,*args,**kwargs):
  expected=getattr(ref,name)(*args,**kwargs);actual=getattr(world,name)(*args,**kwargs)
  self.assertEqual(actual,expected,(type(world).__name__,name,args));self.assertEqual(state(world),state(ref),(name,args));check_units(self,world,actual);METRICS['vectors']+=1
  return actual
 def test_all_actions_result_events_state_and_exact_unit_vectors(self):
  for cls in BACKENDS:
   for cloth in CLOTH_IDS:
    c=replace(C,carrier_padding=cloth);ref=Reference();w=cls()
    for obj in (*LABEL_IDS,*SOURCE_BINDINGS,'hotpot_pot'):
     self.compare(ref,w,'look',c,obj)
    self.compare(ref,w,'introduce',c);self.compare(ref,w,'introduce',c)
    self.compare(ref,w,'unpack_service',c)
    for obj in ('circulation_plan','sightline_plan','placement_symbols'):
     self.compare(ref,w,'acknowledge_source',c,obj,SOURCE_BINDINGS[obj][0])
    self.compare(ref,w,'hint',c,3);self.compare(ref,w,'hint',c,1)
    for obj,pos in DEST.items():
     for destination in (4,2,pos):self.compare(ref,w,'place',c,obj,destination,pull=True)
    self.compare(ref,w,'orient_pa',c,2);self.compare(ref,w,'orient_pa',c,1)
    self.compare(ref,w,'unpack_service',c);self.compare(ref,w,'unpack_service',c)
    self.compare(ref,w,'request_start',c)
    for claim in tuple(ref.pending_handoffs):
     self.compare(ref,w,'acknowledge_handoff',claim['handoff_id'],claim['serial'])
    self.compare(ref,w,'acknowledge_source',c,'credit_slate','P08.READ.004')
    self.compare(ref,w,'layout_dialogue',c)
    self.compare(ref,w,'request_start',c);token=ref.pending_request_id
    self.compare(ref,w,'confirm_start',c,token,True)
    self.compare(ref,w,'pending_presentation',c)
    self.compare(ref,w,'acknowledge_readiness',c,token,READINESS_RECORDS)
    self.compare(ref,w,'confirm_start',c,token,False)
    self.compare(ref,w,'request_start',c);token=ref.pending_request_id
    self.compare(ref,w,'acknowledge_readiness',c,token,READINESS_RECORDS)
    self.compare(ref,w,'confirm_start',c,token,True)
    self.compare(ref,w,'acknowledge_autosave',c,token,False)
    self.compare(ref,w,'retry_autosave',c,token)
    self.compare(ref,w,'acknowledge_autosave',c,token,True)
    self.compare(ref,w,'acknowledge_autosave',c,token,True)
    self.compare(ref,w,'place',c,'serving_table',4)
    self.compare(ref,w,'place',replace(c,protected_objects=frozenset(('serving_table',))),'serving_table',1)
    self.compare(ref,w,'place',c,'serving_table',1)
 def test_independent_slow_interpreters_match_opcode_accelerators(self):
  worlds=[SourceWorld(),EmittedWorld(),FastSourceWorld(),FastEmittedWorld()]
  calls=[('introduce',(C,)),('look',(C,'plan_overlay')),('acknowledge_source',(C,'circulation_plan','P08.READ.001'))]
  calls += [('place',(C,o,p)) for o,p in DEST.items()]
  calls += [('unpack_service',(C,)),('orient_pa',(C,2)),('orient_pa',(C,1))]
  for name,args in calls:
   results=[getattr(w,name)(*args) for w in worlds]
   self.assertTrue(all(r==results[0] for r in results));self.assertTrue(all(state(w)==state(worlds[0]) for w in worlds));METRICS['slow_crosscheck_calls']+=1
  for claim in worlds[0].pending_handoffs:
   results=[w.acknowledge_handoff(claim['handoff_id'],claim['serial']) for w in worlds];self.assertTrue(all(r==results[0] for r in results));METRICS['slow_crosscheck_calls']+=1
  for name,args in [('request_start',(C,)),('acknowledge_readiness',(C,'P08:START:1',READINESS_RECORDS)),('confirm_start',(C,'P08:START:1',True)),('retry_autosave',(C,'P08:START:1')),('acknowledge_autosave',(C,'P08:START:1',False)),('acknowledge_autosave',(C,'P08:START:1',True))]:
   results=[getattr(w,name)(*args) for w in worlds];self.assertTrue(all(r==results[0] for r in results));self.assertTrue(all(state(w)==state(worlds[0]) for w in worlds));METRICS['slow_crosscheck_calls']+=1
  for w in worlds:self.assertEqual(type(w).load(w.save(),C).save(),w.save())
 def test_every_preparation_raw_context_dependency_and_vc_losses(self):
  for cls in BACKENDS:
   for missing in PREPARATIONS:
    w=cls();flags=PREPARATIONS-{missing};mask=sum(v for k,v in M['preparations'].items() if k in flags)
    try:c=replace(C,flags=flags);coherent=True
    except ValueError:coherent=False
    accepted=w.vm.call('p08SetContext',5,0,mask,0,0,1,5,5,0,0,0,0)
    self.assertEqual(bool(accepted),coherent,missing)
    if coherent:self.assertEqual(w.place(c,'serving_table',1).code,'preparations_required')
    METRICS['context_cases']+=1
   for args in [(0,0,8191,0,0,1,5,5,0,0,0,0),(5,2,8191,0,0,1,5,5,0,0,0,0),(5,0,8191,4,0,1,5,5,0,0,0,0),(5,0,8191,0,0,0,5,5,0,0,0,0),(5,0,8191,0,0,1,5,5,0,32,0,0),(5,0,8191,0,0,1,5,5,0,0,1,0),(5,0,8191,0,0,1,5,5,0,0,0,1)]:
    self.assertEqual(w.vm.call('p08SetContext',*args),0);METRICS['context_cases']+=1
 def test_unknown_targets_and_inventory_only_binding_queries(self):
  for cls in BACKENDS:
   ref=Reference();w=cls()
   for target in ('unknown','', 'not_a_destination'):
    for verb in (Verb.OPEN,Verb.USE,Verb.LOOK_AT):self.compare(ref,w,'act',C,verb,'ceramic_carrier',target)
   for key in SCRIPT_BINDINGS:
    c=replace(C,inventory=C.inventory|{key}) if key not in FIXED_OBJECTS and key!=C.carrier_padding else C
    self.compare(ref,w,'look',c,key)
   c=replace(C,inventory=C.inventory|{'unknown'})
   self.compare(ref,w,'act',c,Verb.OPEN,'ceramic_carrier','unknown')
 def test_wrong_handoff_strings_cannot_alias_the_padding_key(self):
  for cls in BACKENDS:
   ref=Reference();w=cls()
   for x in (ref,w):x.place(C,'ceramic_carrier',1);x.place(C,'serving_table',1);x.unpack_service(C)
   serial=ref.ownership_serials['padding']
   for name in ('P08:OWN:__handoff_padding__','padding','P08:OWN:serving_table'):
    self.compare(ref,w,'acknowledge_handoff',name,serial)
   self.compare(ref,w,'acknowledge_handoff','P08:OWN:padding',serial)
 def test_output_admission_rolls_back_without_partial_records_or_events(self):
  for cls in BACKENDS:
   for caps in ((0,6,2),(3,5,2),(3,6,0)):
    w=cls();before=w.save();w._context(C);self.assertEqual(w.vm.call('p08Admission',*caps),1)
    code=w.vm.call('p08Introduce');self.assertEqual(code,M['codes']['output_full']);self.assertFalse(w.vm.p['p08Busy']);self.assertEqual(w.save(),before)
    out=w.vm.arrays['p08Output'];self.assertEqual((out[3],out[7],out[14]),(0,0,0));METRICS['capacity_failures']+=1
   w=cls();before=w.save();w._context(C);w.vm.call('p08Admission',3,6,1)
   self.assertEqual(w.vm.call('p08Place',OBJ['ceramic_carrier'],1,0),M['codes']['output_full']);self.assertEqual(w.save(),before);METRICS['capacity_failures']+=1
   w=fit(cls);before=w.save();w._context(C);w.vm.call('p08Admission',2,6,2)
   self.assertEqual(w.vm.call('p08RequestStart'),M['codes']['output_full']);self.assertEqual(w.save(),before);METRICS['capacity_failures']+=1
 def test_candidate_atomic_commit_abort_busy_and_uncertain_publication(self):
  for cls in BACKENDS:
   w=cls();before=w.save();w._context(C)
   self.assertEqual(w.vm.call('p08Place',1,1,0),M['codes']['positioned']);self.assertEqual(state(w),before['state']);self.assertTrue(w.vm.p['p08Busy'])
   self.assertEqual(w.vm.call('p08CandidateWord',F['carrier_position']),1)
   self.assertEqual(w.vm.call('p08CandidateOutput',O['event_count']),2)
   self.assertEqual(w.vm.call('p08OutputWord',O['code']),0)
   self.assertEqual(w.vm.call('p08Place',2,2,0),M['codes']['busy'])
   self.assertEqual(w.vm.call('p08Abort'),1);self.assertEqual(w.save(),before)
   w._context(C);w.vm.call('p08Place',1,1,0);self.assertEqual(w.vm.call('p08Commit'),1);self.assertEqual(w.positions['ceramic_carrier'],1)
   self.assertEqual(w.vm.call('p08Commit'),0)
   w._context(C);w.vm.call('p08Place',2,2,0);committed=state(w)
   self.assertEqual(w.vm.call('p08StorageUncertain'),1);self.assertEqual(w.vm.call('p08Commit'),0);self.assertEqual(w.vm.call('p08Abort'),0)
   self.assertEqual(w.vm.call('p08Place',2,2,0),M['codes']['storage_uncertain']);self.assertEqual(state(w),committed)
 def test_stale_callback_sessions_and_layout_revision_are_rejected(self):
  for cls in BACKENDS:
   w=fit(cls);w.request_start(C);token=w.pending_request_id;oldsession=w.session;oldrev=w.revision
   saved=w.save();w=cls.load(saved,C);w._context(C)
   w.vm.call('p08SetCallback',*oldsession,*pair(oldrev))
   self.assertEqual(w.vm.call('p08AcknowledgeReadiness',*pair(1),RECORD['P08.DIALOGUE.002'],RECORD['P08.SYSTEM.004']),M['codes']['stale_session'])
   self.assertEqual(w.pending_phase,1)
   w.place(C,'serving_table',4);w.place(C,'serving_table',1);w._context(C)
   w.vm.call('p08SetCallback',*w.session,*pair(oldrev))
   self.assertEqual(w.vm.call('p08AcknowledgeSource',OBJ['circulation_plan'],RECORD['P08.READ.001']),M['codes']['stale_session'])
   self.assertEqual(w.observed_sources,set());self.assertEqual(w.acknowledge_autosave(C,token,True).code,'stale_autosave')
 def test_unsigned_serial_boundaries_and_explicit_exhaustion(self):
  bounds=(32767,32768,65535,65536,2147483647,2147483648,4294967294,4294967295)
  for cls in BACKENDS:
   for value in bounds:
    r=Reference();r.revision=value;w=cls.load(r.save(),C)
    before=w.save();result=w.place(C,'serving_table',1)
    if value==4294967295:self.assertEqual(result.code,'serial_exhausted');self.assertEqual(w.save(),before)
    else:self.assertEqual(result,r.place(C,'serving_table',1));self.assertEqual(w.save(),r.save())
    METRICS['boundary_vectors']+=1
   for value in bounds[:-1]:
    r=fit(Reference);r.revision=value;r.request_serial=value-1;w=cls.load(r.save(),C)
    result=w.request_start(C);self.assertEqual(result,r.request_start(C));self.assertEqual(w.save(),r.save());METRICS['boundary_vectors']+=1
   r=Reference();r.revision=4294967296
   with self.assertRaises(ValueError):cls.load(r.save(),C)
 def test_streamed_save_rejects_bad_header_length_order_and_state(self):
  for cls in BACKENDS:
   w=fit(cls);before=state(w);frame=M['header']+w.vm.arrays['p08Words']
   for index in (0,1,2,3,4,19):
    self.assertEqual(w.vm.call('p08LoadBegin'),1)
    for i,v in enumerate(frame[:index]):self.assertEqual(w.vm.call('p08LoadWord',i,v),1)
    self.assertEqual(w.vm.call('p08LoadWord',index,word(frame[index]+1)),0);self.assertEqual(state(w),before);METRICS['raw_rejections']+=1
   w.vm.call('p08LoadBegin');w.vm.call('p08LoadWord',0,frame[0]);self.assertEqual(w.vm.call('p08LoadFinish',0),M['codes']['invalid_state']);self.assertEqual(state(w),before);METRICS['raw_rejections']+=1
   w.vm.call('p08LoadBegin');self.assertEqual(w.vm.call('p08LoadWord',1,frame[1]),0);self.assertEqual(state(w),before);METRICS['raw_rejections']+=1
   for name,value in [('service_unpacked',0),('facing',0),('returned_padding',0),('layout_ready',0),('pending_phase',3),('carrier_position',0),('hint_level',4)]:
    invalid=list(frame);invalid[20+F[name]]=value;w.vm.call('p08LoadBegin')
    for i,v in enumerate(invalid):self.assertEqual(w.vm.call('p08LoadWord',i,v),1)
    self.assertEqual(w.vm.call('p08LoadFinish',0),M['codes']['invalid_state'],name);self.assertEqual(state(w),before);METRICS['raw_rejections']+=1
 def test_reference_save_consistency_mutation_parity(self):
  snapshots=[];r=Reference();snapshots.append(r.save());r=fit(Reference);snapshots.append(r.save());r.request_start(C);snapshots.append(r.save());t=r.pending_request_id;r.acknowledge_readiness(C,t,READINESS_RECORDS);snapshots.append(r.save());r.confirm_start(C,t,True);snapshots.append(r.save());r.acknowledge_autosave(C,t,True);snapshots.append(r.save())
  for snap in snapshots:
   variants=[]
   for name in SERIALS:
    for value in (0,1,snap['state']['revision']+1):d=deepcopy(snap);d['state'][name]=value;variants.append(d)
   for name,(prefix,keys) in GROUPS.items():
    for key in keys:
     d=deepcopy(snap);d['state'][name][key]=max(1,snap['state']['revision']);variants.append(d)
     d=deepcopy(snap);d['state'][name].pop(key,None);variants.append(d)
   for d in variants:
    try:Reference.load(d,C);expected=True
    except ValueError:expected=False
    for cls in BACKENDS:
     try:cls.load(d,C);actual=True
     except ValueError:actual=False
     self.assertEqual(actual,expected,(cls.__name__,d));METRICS['validation_mutations']+=1
 def test_all_44_canonical_records_units_speakers_and_obligations(self):
  fixture=json.loads((H/'fixtures/canonical-bindings.json').read_text());data=json.loads((H/'fixtures/p08-canonical-presentation.json').read_text())
  self.assertEqual(len(data['records']),44);self.assertEqual(set(M['records']),set(fixture['records']))
  for cls in (SourceWorld,EmittedWorld):
   w=cls()
   for rid,record in fixture['records'].items():
    self.assertEqual(w.vm.call('p08UnitCount',RECORD[rid]),len(record['speech_units']))
    self.assertEqual([UNIT[w.vm.call('p08Unit',RECORD[rid],i)] for i in range(len(record['speech_units']))],record['speech_units'])
   for obj,rid in LABEL_IDS.items():self.assertEqual(w.vm.call('p08LabelRecord',OBJ[obj]),RECORD[rid])
  for r in data['records']:
   f=fixture['records'][r['id']];self.assertEqual({k:r[k] for k in ('text_sha256','speaker_id','source_obligations')},{k:f[k] for k in ('text_sha256','speaker_id','source_obligations')})
  self.assertEqual({u['line_id']:u['laugh_opportunity'] for u in data['speech_units'] if u.get('laugh_opportunity')},fixture['editorial_laugh_metadata'])
 def test_actual_prior_preparations_one_owner_and_caller_checkpoint(self):
  # P06's literal-Python type guard is intentionally untouched. This new
  # numeric-domain host harness jointly stages its owner map and candidate ACK.
  for cls in BACKENDS:
   for cloth in CLOTH_IDS:
    prior=Preparation(cloth);histories=prior.prior_saves();c=prior.context();w=cls();owners=prior.owner_map()
    self.assertLessEqual(PREPARATIONS,c.flags);self.assertFalse(prior.contests.flags&{'VC01_WON','VC02_WON'})
    for obj,pos in DEST.items():w.place(c,obj,pos)
    w.unpack_service(c)
    for claim in w.pending_handoffs:
     before=state(w);oldmap=deepcopy(owners);w.vm.call('p08SetCallback',*w.session,*pair(w.revision))
     key=22 if claim['object_id'] in CLOTH_IDS else OBJ[claim['object_id']]
     self.assertEqual(w.vm.call('p08AcknowledgeHandoff',key,*pair(claim['serial'])),M['codes']['handoff_acknowledged'])
     staged=deepcopy(owners)
     for obj in (claim['object_id'],*claim['includes']):
      self.assertEqual(staged[obj]['owner'],claim['from_owner']);staged[obj]={'owner':claim['to_owner'],'room':claim['room']}
     # Definitive preparation failure aborts both without publishing.
     self.assertEqual(w.vm.call('p08Abort'),1);self.assertEqual(state(w),before);self.assertEqual(owners,oldmap)
     w.vm.call('p08SetCallback',*w.session,*pair(w.revision));w.vm.call('p08AcknowledgeHandoff',key,*pair(claim['serial']))
     self.assertEqual(w.vm.call('p08Commit'),1);owners=staged
    self.assertEqual(prior.prior_saves(),histories);self.assertEqual(owners['hotpot_pot'],{'owner':'P07','room':'L02_KITCHEN'});self.assertEqual(owners['handcart'],{'owner':'P05','room':'L06_GARAGE'})
    self.assertEqual([prior.p3.location(i) for i in (48,49,50)],[10,10,10]);self.assertEqual(prior.p3.inventory(),[35]);projection=prior.p7.projection(prior.c7);self.assertEqual(projection.tasting_bowls,8);self.assertTrue(projection.lid_closed);self.assertFalse(projection.heat_on)
    token=start(w,c);checkpoint={'p08':w.save(),'owners':owners,'prior':histories};self.assertFalse(w.evening_started)
    with tempfile.TemporaryDirectory(prefix='p08-domain-caller-') as tmp:
     dest=Path(tmp)/'pre-evening.json';stage=dest.with_suffix('.tmp');payload=json.dumps(checkpoint,sort_keys=True).encode()
     with stage.open('wb') as stream:stream.write(payload);stream.flush();os.fsync(stream.fileno())
     os.replace(stage,dest);fd=os.open(tmp,os.O_RDONLY)
     try:os.fsync(fd)
     finally:os.close(fd)
     self.assertEqual(dest.read_bytes(),payload);self.assertFalse(w.evening_started)
     self.assertEqual(w.acknowledge_autosave(c,token,True).line_ids,('P08.SYSTEM.006',));self.assertTrue(w.evening_started)
     restored=cls.load(json.loads(dest.read_bytes())['p08'],c);self.assertFalse(restored.evening_started);self.assertEqual(restored.pending_phase,3)
     self.assertEqual(restored.acknowledge_autosave(c,token,False).code,'autosave_failed');self.assertEqual(restored.retry_autosave(c,token).code,'autosave_requested')
     self.assertTrue(cls.load(w.save(),c).evening_started)
    self.assertEqual(prior.prior_saves(),histories);self.assertFalse(w.flags&{'SERVED','DISPLAY_STAGED','GAME_COMPLETE'});METRICS['composition_cloths']+=1

class FiniteTests(unittest.TestCase):
 def test_all_2048_layouts_reference_source_emitted_and_ordinary_restores(self):
  worlds=[fit(Reference),fit(FastSourceWorld),fit(FastEmittedWorld)]
  for positions in product((1,2,3,4),repeat=5):
   for facing in (1,2):
    for obj,pos in zip(LAYOUT_OBJECTS,positions):
     values=[w.place(C,obj,pos) for w in worlds];self.assertEqual(values[1:],values[:1]*2)
    values=[w.orient_pa(C,facing) for w in worlds];self.assertEqual(values[1:],values[:1]*2)
    c,p,s,t,k=positions;expected={'buffet_at_hatch':c==t==k==1,'sound_facing_inward':p==2 and facing==1,'display_concealed':s==3,'hatch_visible':s!=1,'lane_clear':4 not in positions}
    for w in worlds:self.assertEqual(w.conditions,expected);self.assertEqual(w.ready,all(expected.values()));self.assertEqual(state(w),state(worlds[0]))
    # Full public save/load at every layout, with fresh callback session.
    for i,w in enumerate(worlds):
     snapshot=w.save();worlds[i]=type(w).load(snapshot,C);self.assertEqual(worlds[i].save(),snapshot);METRICS['restore_roundtrips']+=1
    METRICS['finite_layouts']+=1
  self.assertEqual(METRICS['finite_layouts'],2048);self.assertEqual(METRICS['restore_roundtrips'],6144)

if __name__=='__main__':unittest.main()
