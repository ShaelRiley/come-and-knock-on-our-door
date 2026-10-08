"""New independent current-canon/owner joins and scoped source barriers."""
import copy,json,itertools,hashlib,unittest
from dataclasses import replace
from pathlib import Path
from cakood.p12_model import *
from cakood.p10_model import P10World,P10Context,TILE_IDS,PAPER_IDS,ORDER
from cakood.p09_model import P09World,P09Context
from cakood.p11_model import P11World,P11Context
from cakood.p04_model import project_gate
from cakood.p13_model import P13World,P13Context,PREREQUISITES as REQ13
from cakood.verbal_contest import VerbalContests,Catalog,Phase
from dependencies.p03_numeric_model import P03
from dependencies.p04_numeric_model import P04,Obj,Bunting
from test_verbal_contest import prepared,play,leave,read_all
from test_domain import C,A,RACK,Harness,contests
from codec import M,encode_save,decode_words,encode_world
from source_vm import VM,restore_words
ROOT=Path(__file__).resolve().parents[1]

def shown(w,c,s):
 p=w.begin_presentation(c,s)
 if p.presentation_id:w.acknowledge_presentation(c,p.presentation_id,record_id=w.SOURCES[s])
 return p

def gate_owner():
 p=P04();p.context(3,0,1,1);p.topic(Obj.FELIX,1);p.open_gate();p.place_wedge()
 p.context(3,0,1,0);p.move_bunting(Bunting.HELD);p.move_bunting(Bunting.HOOK);p.recover_wedge()
 p.context(3,0,1,1);p.close_gate(1);p.open_gate()
 if not p.tested or not p.validate():raise RuntimeError('Real gate did not pass')
 return p

def genuine_upstream(ids=TILE_IDS,preengaged=False,win=False):
 p3=P03();p3.context(6,0,1,1);p3.look(37);p3.begin_credit();p3.select(1)
 p3.context(2,0,1,1);p3.collect(38);p3.context(6,0,1,1);p3.pad(38);p3.give_slate()
 if p3.inventory()!=[35] or [p3.location(i) for i in (48,49,50)]!=[10,10,10]:raise RuntimeError('Original tiles not earned')
 flags=frozenset({'EVENING_STARTED','PLAN_AGREED'})
 p9=P09World();c9=P09Context('L07_CONSERVATORY',flags=flags)
 for source,record in (('direct_question','P09.DIALOGUE.001'),('terms','P09.DIALOGUE.002')):
  p=p9.begin_presentation(c9,source);p9.acknowledge_presentation(c9,p.presentation_id,record_id=record)
 flags|=p9.flags
 p10=P10World();pocket=set((*TILE_IDS,'grease_pencil','master_invitation'))
 c10=P10Context(LIVING,flags=flags,inventory=frozenset(pocket))
 p10.introduce(c10);shown(p10,c10,'plan')
 if set(ids)&set(PAPER_IDS):p10.prepare_paper(c10)
 for cue,word in zip(ids,ORDER):p10.write(c10,cue,word)
 for i,cue in enumerate(ids):
  p10.place(replace(c10,room=COURTYARD,inventory=frozenset(pocket)),cue,i);pocket.discard(cue)
 if not p10.ready:raise RuntimeError('Real P10 did not restore cues')
 flags|=p10.flags
 gate=gate_owner()
 if preengaged:gate.set_peg(1)
 c11=P11Context(SIDE,project_gate(gate),flags=flags)
 p11=P11World();p11.lift(c11)
 if not preengaged:
  p11.request_peg(c11);token=p11.pending_peg_request_id
  gate.set_peg(1);c11=replace(c11,gate=project_gate(gate));p11.acknowledge_peg(c11,token)
 p11.release_catch(c11);p11.pull_handle(c11);p11.stage_display(c11);shown(p11,c11,'sincere')
 if not p11.contest_eligible:raise RuntimeError('Protected rescue admission unfinished')
 request=p11.request_contest(c11)
 if request.code!='contest_requested':raise RuntimeError('Actual contest handoff missing')
 rescue_snapshot=P11World.load(p11.save(),context=c11)
 p11.acknowledge_contest_request(c11,p11.pending_contest_request_id)
 vc=prepared('VC03');play(vc,[win]*3,'VC03');captions=[];leave(vc,rescue=rescue_snapshot,shown=captions)
 c=replace(C,flags=flags|p11.flags,inventory=frozenset(pocket),contests=vc)
 return p3,gate,p9,p10,p11,vc,c,captions

class CurrentTests(unittest.TestCase):
 def test_entire_literal_prefix_and_shared_classes_preserved(self):
  raw=(ROOT/'cakood/p12_model.py').read_bytes();prefix=(ROOT.parent/'historical/literal-read-partial/cakood/p12_model.py.part').read_bytes()
  self.assertEqual(len(prefix),11306);self.assertEqual(raw[:11306],prefix)
  self.assertEqual(hashlib.sha256(prefix).hexdigest(),'3d45272ea67aa9a7e4c208952da8e895b40c581fff99ec5c81f0b29f3f4c6622')

 def test_full_current_fixture_preserves_metadata_and_obligations(self):
  f=json.loads((ROOT/'tests/fixtures/p12/canonical-bindings.json').read_text())
  catalog=json.loads((ROOT/'authority/full-line-catalog.json').read_text())['records'];speech=json.loads((ROOT/'authority/speech-units.json').read_text())['units']
  self.assertEqual(f['records'],[r for r in catalog if r['id'].startswith('P12.') or r['id']=='VC03.NEED_RESOLUTION'])
  self.assertEqual(f['speech_units'],[u for u in speech if u['record_id'] in RECORD_UNITS])
  self.assertEqual((len(f['records']),len(f['speech_units'])),(30,36))
  self.assertTrue(all(r['source_obligations'] for r in f['records']))

 def test_real_p03_p09_p10_p04_p11_to_p12_all_materials_both_rescues(self):
  for ids,pre in itertools.product((TILE_IDS,PAPER_IDS,(TILE_IDS[2],PAPER_IDS[0],TILE_IDS[0])),(False,True)):
   with self.subTest(ids=ids,preengaged=pre):
    p3,p4,p9,p10,p11,vc,c,captions=genuine_upstream(ids,pre)
    before=[copy.deepcopy(vars(p3)),*[x.save() for x in (p4,p9,p10,p11,vc)]]
    self.assertFalse(p9.terms_card_handoff['signed']);self.assertFalse(p11.display_handoff['rita_reveal_consent'])
    self.assertEqual(p11.rescue_credit_variant,'pre_engaged' if pre else 'ordinary')
    self.assertTrue(vc.progress['VC03'].resolved);self.assertFalse(vc.progress['VC03'].won)
    h=Harness();h.repair(c,p10.cue_handoff);h.show('introduction',c);h.action('commit_introduction','p12CommitIntroduction',c=c)
    self.assertTrue(h.w.ready);self.assertFalse(h.w.welcome_cleared)
    self.assertEqual(h.w.reserved_external_objects,{'cue_rack',*ids})
    self.assertEqual([copy.deepcopy(vars(p3)),*[x.save() for x in (p4,p9,p10,p11,vc)]],before)
    self.assertFalse(h.w.flags & {'DISPLAY_REVEALED','GAME_COMPLETE','VC03_WON'})

 def test_real_rescue_serials_select_exact_current_vc03_result_before_receipt(self):
  for pre,win in itertools.product((False,True),(False,True)):
   p3,p4,p9,p10,p11,vc,c,captions=genuine_upstream(preengaged=pre,win=win)
   rid='VC03.WIN' if win else 'VC03.LOSS';variant='pre_engaged' if pre else 'ordinary'
   shown=next(p for p in captions if p.unit_id==rid+'.02')
   unit=vc.catalog.speech_unit(shown.unit_id)
   expected=next(v for v in unit['finite_variants'] if v['variant_id']==variant)
   self.assertEqual(shown.text,expected['text']);self.assertIn(('rescue_credit_variant',variant),shown.bindings)
   self.assertEqual(vc.progress['VC03'].won,win);self.assertTrue(vc.progress['VC03'].resolved)
   self.assertEqual(p11.rescue_credit_variant,variant)
   if pre:self.assertNotEqual(shown.text,unit['text'])
   history=p11.save();rematch=[];play(vc,[not win]*3);leave(vc,rescue=p11,shown=rematch)
   other_id='VC03.LOSS' if win else 'VC03.WIN'
   other=next(p for p in rematch if p.unit_id==other_id+'.02')
   other_unit=vc.catalog.speech_unit(other.unit_id)
   other_expected=next(v for v in other_unit['finite_variants'] if v['variant_id']==variant)
   self.assertEqual(other.text,other_expected['text']);self.assertIn(('rescue_credit_variant',variant),other.bindings)
   self.assertEqual(p11.save(),history);self.assertTrue(vc.progress['VC03'].resolved)
   self.assertTrue(vc.progress['VC03'].won)

 def test_new_wrapper_derives_progress_and_blocks_real_unread_contest_result(self):
  vc=prepared();c=replace(C,contests=vc);h=Harness();h.repair(c)
  vc.enter('VC03',0,admitted=True)
  self.assertEqual(h.w.choose_introduction(c).code,'contest_active')
  vc.yield_contest(vc.active.id);vc.commit_ko(vc.active.outcome_id)
  self.assertTrue(vc.progress['VC03'].resolved);self.assertFalse(vc.progress['VC03'].won)
  self.assertEqual(h.w.choose_introduction(c).code,'contest_active')
  before=vc.save();read_all(vc)
  self.assertIsNone(vc.active);self.assertNotEqual(vc.save(),before)
  self.assertEqual(h.w.choose_introduction(c).code,'presentation_pending')
  with self.assertRaises(TypeError):vc.progress['VC03']=None
  with self.assertRaises(Exception):vc.progress['VC03'].won=True

 def test_real_lost_contest_rematch_win_retains_independent_result(self):
  vc=prepared();play(vc,[False]*3);leave(vc);self.assertFalse(vc.progress['VC03'].won)
  play(vc,[True]*3);leave(vc);self.assertTrue(vc.progress['VC03'].won)
  play(vc,[False]*3);leave(vc);self.assertTrue(vc.progress['VC03'].won)
  self.assertTrue(vc.progress['VC03'].resolved)

 def test_historical_intro_flag_cannot_skip_own_shared_presentation(self):
  c=replace(C,flags=C.flags|{'INTRODUCTION_CLEAR'})
  h=Harness();h.start(c);self.assertFalse(h.w.ready or h.w.welcome_cleared)
  self.assertEqual(h.w.release_confetti(c).code,'introduction_required')
  self.assertEqual(h.w.finish_welcome(c).code,'cleanup_text_required')
  h.repair(c);self.assertEqual(h.w.commit_introduction(c).code,'whole_introduction_required')
  self.assertFalse(h.w.welcome_cleared)

 def test_collection_handoff_requires_intro_confetti_cleanup_and_cannot_sign(self):
  p3,p4,p9,p10,p11,vc,c,captions=genuine_upstream()
  h=Harness();h.repair(c,p10.cue_handoff);h.show('introduction',c);h.action('commit_introduction','p12CommitIntroduction',c=c)
  pot={'object_id':'hotpot_pot','room':KITCHEN,'lid_closed':True,'portions':8,'portion_kind':'tasting','includes_jackie':True}
  p13=P13World();c13=P13Context(COURTYARD,flags=REQ13,npc_locations=c.npc_locations,rig=c.rig,contests=vc,gate=project_gate(p4),welcome_cleared=h.w.welcome_cleared)
  self.assertEqual(p13.start(c13,pot,p11.display_handoff).code,'p12_collection_handoff_required')
  self.assertEqual(h.w.finish_welcome(c).code,'cleanup_text_required')
  h.action('release_confetti','p12ReleaseConfetti',c=c);h.show('confetti',c)
  self.assertEqual(p13.start(c13,pot,p11.display_handoff).code,'p12_collection_handoff_required')
  h.show('cleanup',c);event=h.action('finish_welcome','p12FinishWelcome',c=c).events[0]
  self.assertEqual(event.payload['destinations'],{'bunny':KITCHEN,'frankie':LIVING,'rita':SIDE,'felix':SIDE,'vivian':SIDE,'milo':PORCH})
  self.assertTrue(event.payload['panel_covered']);self.assertTrue(h.w.welcome_cleared)
  c13=replace(c13,welcome_cleared=h.w.welcome_cleared)
  self.assertEqual(p13.start(c13,pot,p11.display_handoff).code,'deliveries_started')
  self.assertFalse(p13.rita_consented);self.assertFalse(p9.terms_card_handoff['signed'])
  self.assertEqual(h.w.release_confetti(c).code,'confetti_already_released')
  self.assertEqual(h.w.finish_welcome(c).events,())

 def test_all_shared_scene_prefixes_persist_without_early_completion(self):
  for source in ('introduction','confetti','cleanup'):
   for prefix in range(len(P12World()._tokens(source))+1):
    h=Harness();h.repair()
    if source!='introduction':h.show('introduction');h.action('commit_introduction','p12CommitIntroduction');h.action('release_confetti','p12ReleaseConfetti')
    if source=='cleanup':h.show('confetti')
    h.begin(source);tokens=h.w._tokens(source)
    if prefix:h.ack(source,units=tokens[:prefix])
    old=h.w._handle(source);oldsave=h.w.save();h.restore()
    self.assertEqual(h.w.save(),oldsave)
    self.assertEqual(h.w.acknowledge_presentation(C,old,record_id=h.w.SOURCES[source]).code,'stale_presentation')
    self.assertFalse(h.w.welcome_cleared)
    if prefix<len(tokens):
     method='commit_introduction' if source=='introduction' else 'finish_welcome'
     self.assertNotIn(getattr(h.w,method)(C).code,('introduction_clear','collection_started'))
     h.resume(source);h.ack(source,units=tokens[prefix:])
    self.assertTrue(h.w._complete(source))

 def test_physical_cue_rack_duplicate_is_rejected_before_handoff(self):
  for obj in ('cue_rack',*TILE_IDS):
   w=P12World();c=replace(C,inventory=frozenset({obj}));before=w.save()
   with self.assertRaises(ValueError):w.start(c,RACK)
   self.assertEqual(w.save(),before)

 def test_literal_start_defect_contrast_and_corrected_repeat_semantics(self):
  c=replace(C,inventory=frozenset({'cue_rack'}))
  original=P12World()
  # Execute only the recovered method on the reconstructed class. This is NOT
  # execution of a missing historical full model.
  result=original._literal_start(c,RACK)
  self.assertEqual(result.code,'rack_rehung');self.assertGreater(original.start_at,0)
  h=Harness();h.project(c)
  h.v.call('p12Handoff',M['objects']['cue_rack'],M['rooms'][COURTYARD],0,1,*[M['objects'][x] for x in TILE_IDS],1,2,3)
  self.assertEqual(h.v.p['p12Code'],M['codes']['invalid_context'])
  with self.assertRaises(ValueError):h.w.start(c,RACK)
  self.assertEqual(h.w.start_at,0)
  valid=P12World();self.assertEqual(valid.start(C,RACK).code,'rack_rehung');before=valid.save()
  self.assertEqual(valid.start(C,RACK).code,'already_rehung')
  self.assertEqual(valid.start(c,{}).code,'already_rehung')
  self.assertEqual(valid.save(),before)

 def test_pending_source_rechecks_each_live_speaker_pa_and_context(self):
  h=Harness();h.repair();h.begin('introduction');h.ack('introduction',units=h.w._tokens('introduction')[:6])
  for person in ('stringer','rita'):
   c=replace(C,npc_locations=tuple((p,LIVING if p==person else room) for p,room in C.npc_locations));before=h.w.save()
   self.assertEqual(h.w.resume_presentation(c,'introduction').code,'speaker_absent');self.assertEqual(h.w.save(),before)
  self.assertEqual(h.w.resume_presentation(replace(C,rig=replace(C.rig,source='TAPE')),'introduction').code,'selector_tape')
  self.assertEqual(h.w.resume_presentation(replace(C,room=LIVING),'introduction').code,'offscreen')
  h.resume('introduction');h.ack('introduction',units=h.w._tokens('introduction')[6:]);self.assertFalse(h.w.ready)
  h.action('commit_introduction','p12CommitIntroduction');self.assertTrue(h.w.ready)

 def test_scoped_restore_barriers_against_skipped_shared_scenes(self):
  h=Harness();h.confetti();h.show('cleanup');h.action('finish_welcome','p12FinishWelcome')
  good=h.w.save()
  for source in ('self_view','introduction','confetti','cleanup'):
   bad=copy.deepcopy(good);bad['state']['presentations'].pop(source)
   with self.assertRaises(ValueError):P12World.load(bad)
   with self.assertRaises(ValueError):restore_words(list(encode_save(bad).values()))
  for name in ('start_at','release_at','face_at','intro_at','confetti_at'):
   bad=copy.deepcopy(good);bad['state'][name]=0
   with self.assertRaises(ValueError):P12World.load(bad)
   with self.assertRaises(ValueError):restore_words(list(encode_save(bad).values()))

 def test_pure_queries_and_reversible_mistakes_leave_no_implicit_grants(self):
  c=replace(C,contests=contests(False));h=Harness();h.start(c)
  for choice in ('partners','partnerships'):
   before=h.w.save();self.assertEqual(h.w.choose_introduction(c,choice).code,'incomplete_introduction');self.assertEqual(h.w.save(),before)
  h.show('rehearsal',replace(c,on_apron=True));self.assertFalse(h.w.ready or h.w.viewed)
  before=h.w.save()
  for _ in range(50):h.w.audio_finished();h.w.hint(c,3);h.w.journal_records();h.w.journal_units()
  self.assertEqual(h.w.save(),before);self.assertEqual(h.w.flags,frozenset())

if __name__=='__main__':unittest.main()
