"""NEW independent tests of current source identity and genuine owner joins."""
import copy,json,itertools,unittest,hashlib,tempfile,os,importlib.util
from pathlib import Path
from dataclasses import replace
from current_join import *
from test_late_campaign_models import c13,POT,DISPLAY,GATE,actors
from cakood.p13_model import RECORD_UNITS,UNIT_SPEAKERS
from cakood.p08_model import Facing
from test_verbal_contest import read_all
from test_domain import Harness,M,CO
from source_vm import VM,restore_words
from codec import encode_save,encode_world
C=Path(__file__).resolve().parents[1];W=C.parent

class CurrentTests(unittest.TestCase):
 def test_current_canon_full_metadata_and_equal_credits_unchanged(self):
  fixture=json.loads((C/'tests/fixtures/p13/canonical-bindings.json').read_text())
  cat=json.loads((C/'authority/full-line-catalog.json').read_text());speech=json.loads((C/'authority/speech-units.json').read_text())
  self.assertEqual(fixture['records'],[r for r in cat['records'] if r['id'] in RECORD_UNITS])
  self.assertEqual(fixture['speech_units'],[u for u in speech['units'] if u['record_id'] in RECORD_UNITS])
  self.assertEqual((len(fixture['records']),len(fixture['speech_units']),len(fixture['support_records'])),(45,40,4))
  self.assertEqual(UNIT_SPEAKERS,{u['line_id']:u['speaker_id'] for u in fixture['speech_units']})
  self.assertTrue(all(r['source_obligations'] for r in fixture['records']))
  # Complete authority hashes protect full equal writer credits beyond P13.
  self.assertEqual(hashlib.sha256((C/'authority/complete-body.md').read_bytes()).hexdigest(),'18e2eb1a300cc1ac1192916441b640ca6134af619ee17eb424637b4dde28647c')
  self.assertEqual(hashlib.sha256((C/'authority/full-line-catalog.json').read_bytes()).hexdigest(),'3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c')
  for row in fixture['support_records']:
   self.assertEqual(row,next(r for r in cat['records'] if r['id']==row['id']))

 def test_original_complete_class_and_shared_p12_bytes_preserved(self):
  part=(W/'historical/literal-read-partial/tests/test_late_campaign_models.py.lines197-289.part').read_text()
  klass=part[:part.index('\n\nclass P14Tests')]
  self.assertIn(klass,(C/'tests/test_late_campaign_models.py').read_text())
  literal=(W/'historical/literal-read/cakood/p13_model.py').read_bytes()
  self.assertEqual((len(literal),len(literal.splitlines())),(27204,483))
  self.assertEqual(hashlib.sha256(literal).hexdigest(),'0cd474faba3820d7a5b30be7fc7f78131141d9866e0288b10a8704fe02553eb5')
  prefix=(W/'historical/literal-read-partial/cakood/p12_model.py.part').read_bytes()
  self.assertEqual((C/'cakood/p12_model.py').read_bytes()[:len(prefix)],prefix)

 def test_genuine_cooked_pot_full_read_history_and_unique_transfer(self):
  j=Joined();pot=pot_projection(j.p7,j.c7)
  self.assertEqual(pot,POT);self.assertEqual(len(j.p7_reads),3)
  catalog={r['id']:r for r in json.loads((C/'authority/full-line-catalog.json').read_text())['records']}
  for record in j.p7_reads:self.assertEqual(record['text'],catalog[record['record_id']]['text'])
  self.assertEqual(set(j.p7.state['observations']),{'recipe','jug_mark','herb_label'})
  for source,row in j.p7.state['observations'].items():
   self.assertEqual(len(row['pages']),1);self.assertGreater(row['pages'][0]['serial'],row['request'])
  early=copy.deepcopy(j.p7.save());original_display=j.p11.save()
  self.assertEqual(j.w.start(j.context(),pot,j.p11.display_handoff).code,'p12_collection_handoff_required')
  self.assertEqual(j.p7.save(),early)
  j.serve();self.assertEqual(j.h7.handoffs,1);self.assertEqual(j.h7.owner,OwnedObject('hotpot_pot','P13',COURTYARD))
  self.assertEqual([o.object_id for o in j.p7.projection(j.c7).objects if o.object_id=='hotpot_pot'],[])
  self.assertEqual(j.physical['hotpot_pot'],('P13',COURTYARD));self.assertNotIn('hotpot_pot',j.w.inventory)
  saved7=j.p7.save();self.assertEqual(saved7['state']['handoff']['delivery_serial'],j.w.pot_at)
  result=j.p7.handoff_to_p13(j.c7,P13Handoff('P13:OWN:hotpot_pot',j.w.pot_at),host=j.h7)
  self.assertEqual(result.code,'already_handed_off');self.assertEqual(j.h7.handoffs,1)
  self.assertEqual(j.p7.save(),saved7);self.assertEqual(j.p11.save(),original_display)
  # Release conserves saved reader/ingredient receipts, introducing handoff only.
  for k,v in early['state']['receipts'].items():
   if k!='handoff':self.assertEqual(v,saved7['state']['receipts'][k])
  self.assertEqual(early['state']['observations'],saved7['state']['observations'])

 def test_actual_p07_transaction_failure_retains_source_pot(self):
  p,c,h,reads=cook_pot();c=replace(c,flags=c.flags|{'INTRODUCTION_CLEAR'})
  before=p.save();physical=h.snapshot();h.fail_prepare=True
  with self.assertRaises(Exception):p.handoff_to_p13(c,P13Handoff('P13:OWN:hotpot_pot',1),host=h)
  self.assertEqual(p.save(),before);self.assertEqual(h.snapshot(),physical)
  h.fail_prepare=False;h.fail_commit=True
  with self.assertRaises(Exception):p.handoff_to_p13(c,P13Handoff('P13:OWN:hotpot_pot',1),host=h)
  self.assertEqual(p.save(),before);self.assertEqual(h.snapshot(),physical)

 def test_p12_cleanup_prefixes_are_not_collection_or_rita_consent(self):
  j=Joined();self.assertTrue(j.p12.ready);self.assertFalse(j.p12.welcome_cleared)
  j.p12.release_confetti(j.c12);shown(j.p12,j.c12,'confetti');r=j.p12.begin_presentation(j.c12,'cleanup')
  for token in j.p12._tokens('cleanup')[:-1]:
   j.p12.acknowledge_presentation(j.c12,r.presentation_id,speech_unit_ids=(token,))
   self.assertEqual(j.w.start(j.context(),pot_projection(j.p7,j.c7),j.p11.display_handoff).code,'p12_collection_handoff_required')
  j.p12.acknowledge_presentation(j.c12,r.presentation_id,speech_unit_ids=j.p12._tokens('cleanup')[-1:]);j.p12.finish_welcome(j.c12)
  self.assertTrue(j.p12.welcome_cleared);self.assertFalse(j.w.rita_consented)
  self.assertEqual(j.w.start(j.context(),pot_projection(j.p7,j.c7),j.p11.display_handoff).code,'deliveries_started')

 def test_genuine_rescues_loss_toast_and_original_display_conservation(self):
  for pre in (False,True):
   with self.subTest(preengaged=pre):
    j=Joined(preengaged=pre);display=j.p11.save();gate=j.p4.save();p12_intro=j.p12.save()
    self.assertEqual(j.p11.rescue_credit_variant,'pre_engaged' if pre else 'ordinary')
    self.assertFalse(j.p11.display_handoff['rita_reveal_consent'])
    r=j.finish();self.assertEqual(r.code,'toast_complete');self.assertEqual(j.w.flags,{'SERVED','DISPLAY_REVEALED','TOAST_READY'})
    self.assertTrue(j.vc.progress['VC04'].resolved);self.assertFalse(j.vc.progress['VC04'].won)
    self.assertFalse(any(j.vc.progress[e].won for e in ('VC01','VC02','VC03')))
    self.assertFalse(j.p9.terms_card_handoff['signed']);self.assertEqual(j.p11.save(),display);self.assertEqual(j.p4.save(),gate)
    self.assertEqual({k:j.physical[k] for k in ('folded_display','handcart')},{'folded_display':('P13',COURTYARD),'handcart':('P13',COURTYARD)})
    self.assertFalse({'GAME_COMPLETE','SIGNED','VC04_WON'}&j.w.flags)
    self.assertEqual(j.p12.save()['state']['presentations']['introduction'],p12_intro['state']['presentations']['introduction'])

 def test_real_actor_departures_arrivals_and_helper_rechecks(self):
  j=Joined();j.start()
  self.assertEqual(j.actors,{'bunny':KITCHEN,'frankie':LIVING,'milo':PORCH,'vivian':SIDE,'rita':SIDE,'felix':SIDE,'stringer':COURTYARD})
  before=j.w.save();self.assertEqual(j.w.deliver_pot(j.context(KITCHEN)).code,'helpers_absent');self.assertEqual(j.w.save(),before)
  j.serve();self.assertEqual(j.w.ask_rita(j.context()).code,'speaker_absent')
  j.move('rita',COURTYARD,'observed return');request=j.w.ask_rita(j.context());self.assertFalse(j.w.rita_consented)
  j.move('rita',SIDE,'observed departure before receipt');self.assertEqual(j.w.acknowledge_presentation(j.context(),request.presentation_id,record_id='P13.DIALOGUE.004').code,'speaker_absent')
  j.move('rita',COURTYARD,'observed return');shown(j.w,j.context(),'rita_ready')
  j.move('felix',COURTYARD,'observed early departure');before=j.w.save()
  self.assertEqual(j.w.deliver_display(j.context(SIDE)).code,'transport_helpers_absent');self.assertEqual(j.w.save(),before)
  j.move('felix',SIDE,'observed return for cart');self.assertEqual(j.w.deliver_display(j.context(SIDE)).code,'display_delivered')
  self.assertTrue(all(row['path'][0]!=row['path'][-1] or len(row['path'])==1 for row in j.trace if row['kind']=='logical-actor-arrival'))

 def test_current_owner_impossible_gate_snapshots_rejected_both_oracles(self):
  for delta in (dict(peg_engaged=True,gate_open=True,wedge_in_gate=True),dict(peg_engaged=False,gate_open=False,wedge_in_gate=True)):
   with self.assertRaises(ValueError):replace(c13(),gate=replace(GATE,**delta))
   h=Harness();h.project();args=[h.v.p['p13'+name] for name in M['context']]
   for key,value in delta.items():
    name={'peg_engaged':'PegEngaged','gate_open':'GateOpen','wedge_in_gate':'WedgeInGate'}[key];args[M['context'].index(name)]=int(value)
   args[-1]+=1;self.assertEqual(h.v.call('p13Context',*args),0);self.assertEqual(CO[h.v.p['p13Code']],'invalid_context')
  j=Joined();j.serve();j.move('rita',COURTYARD,'consent');shown(j.w,j.context(),'rita_ready')
  j.p4.set_peg(0);before=j.w.save();self.assertEqual(j.w.deliver_display(j.context(SIDE)).code,'tested_peg_required');self.assertEqual(j.w.save(),before)
  j.p4.set_peg(1);self.assertEqual(j.w.deliver_display(j.context(SIDE)).code,'display_delivered')

 def test_genuine_p08_reversible_layout_then_occupied_protection(self):
  j=Joined();j.start();j.p8.place(j.c8,'serving_table',Position.LANE)
  self.assertFalse(j.context().buffet_at_hatch);self.assertFalse(j.context().lane_clear)
  preview=j.w.route_preview(j.context(),'SERVE');self.assertFalse(preview['buffet_ready']);self.assertIsNone(preview['timer'])
  self.assertEqual(j.w.blocked_layout_binding(j.context(),'SERVE')['label_record_id'],'P08.LABEL.002')
  j.p8.place(j.c8,'serving_table',Position.HATCH);j.serve()
  protection=frozenset(o for o in ('ceramic_carrier','serving_table','credit_slate','completed_screen') if j.w.protect_furniture(j.context(),o).code=='occupied_furniture_protected')
  protected=replace(j.c8,protected_objects=protection);before=j.p8.save()
  for o in protection:self.assertEqual(j.p8.place(protected,o,Position.LANE).code,'occupied_object')
  self.assertEqual(j.p8.save(),before)
  # Screen remains reversible until occupied by the delivered display.
  j.p8.place(j.c8,'completed_screen',Position.HATCH)
  self.assertFalse(j.context().display_concealed);self.assertFalse(j.context().hatch_visible)
  j.p8.place(j.c8,'completed_screen',Position.ALCOVE);j.reveal()
  protected=replace(j.c8,protected_objects=protection|{'completed_screen'});before=j.p8.save()
  self.assertEqual(j.p8.place(protected,'completed_screen',Position.LANE).code,'occupied_object');self.assertEqual(j.p8.save(),before)

 def test_wrong_routes_retain_genuine_loads_and_laugh_needs_caption_visual(self):
  j=Joined();j.start();j.move('frankie',COURTYARD,'observed hatch receiver')
  p7=j.p7.save();p11=j.p11.save();physical=copy.deepcopy(j.physical)
  for route in ('house_doorway','side_gate'):
   j.w.deliver_pot(j.context(KITCHEN),route);self.assertEqual(j.physical,physical);self.assertEqual(j.p7.save(),p7);self.assertEqual(j.p11.save(),p11)
  token=j.w.pending_wrong_visual_id
  self.assertEqual(j.w.acknowledge_wrong_visual(j.context(KITCHEN),token).code,'wrong_route_caption_required')
  self.assertFalse(j.w.claim_laugh(j.context(KITCHEN)).events);shown(j.w,j.context(KITCHEN),'wrong_pot')
  j.w.audio_finished();self.assertFalse(j.w.claim_laugh(j.context(KITCHEN)).events)
  j.w=P13World.load(j.w.save(),context=j.context());self.assertEqual(j.w.acknowledge_wrong_visual(j.context(KITCHEN),token).code,'stale_visual')
  j.w.acknowledge_wrong_visual(j.context(KITCHEN),j.w.pending_wrong_visual_id);self.assertEqual([e.id for e in j.w.claim_laugh(j.context(KITCHEN)).events],['LAF13'])
  j.w.deliver_pot(j.context(KITCHEN),'house_doorway');self.assertFalse(j.w.claim_laugh(j.context(KITCHEN)).events)
  j.finish();self.assertTrue(j.w.ready);self.assertEqual(j.h7.handoffs,1)

 def test_all_real_reveal_prefixes_restore_history_and_consent(self):
  for count in range(6):
   j=Joined();j.serve();j.move('rita',COURTYARD,'consent');shown(j.w,j.context(),'rita_ready');j.w.deliver_display(j.context(SIDE));j.w.open_screen(j.context());j.move('bunny',COURTYARD,'reveal participant')
   r=j.w.begin_presentation(j.context(),'reveal');tokens=j.w._tokens('reveal')
   if count:j.w.acknowledge_presentation(j.context(),r.presentation_id,speech_unit_ids=tokens[:count])
   prior=j.w.save();others=[x.save() for x in (j.p7,j.p11,j.p12,j.vc)];j.w=P13World.load(json.loads(json.dumps(prior)),context=j.context())
   self.assertEqual(j.w.save(),prior);self.assertEqual(j.w.acknowledge_presentation(j.context(),r.presentation_id,record_id='P13.DIALOGUE.005').code,'stale_presentation')
   if count<5:
    self.assertEqual(j.w.pull_show(j.context()).code,'rita_presentation_required');shown(j.w,j.context(),'reveal')
   self.assertEqual(j.w.pull_show(j.context()).code,'show_complete');self.assertEqual([x.save() for x in (j.p7,j.p11,j.p12,j.vc)],others)

 def test_real_vc04_unread_loss_then_rematch_preserves_wins(self):
  j=Joined();j.board();self.assertEqual(j.w.call_attention(j.context()).code,'vc04_resolution_required')
  request=j.contest(False,read_result=False);self.assertEqual(request.line_ids,('VC04.ENTRY',));self.assertTrue(j.vc.progress['VC04'].resolved)
  self.assertEqual(j.w.call_attention(j.context()).code,'contest_active');self.assertEqual(j.w.pull_toast(j.context()).code,'contest_active')
  leave(j.vc);shown(j.w,j.context(),'attention');j.w.pull_toast(j.context());state=j.w.save()
  for win in (True,False):
   self.assertEqual(j.contest(win).line_ids,('VC04.REMATCH',));self.assertTrue(j.vc.progress['VC04'].won)
   self.assertTrue(j.w.ready);self.assertEqual(j.w.flags,{'SERVED','DISPLAY_REVEALED','TOAST_READY'})
   for field in ('served_at','show_at','toast_at','presentations'):self.assertEqual(j.w.save()['state'][field],state['state'][field])
   self.assertFalse(j.p9.terms_card_handoff['signed'])

 def test_real_pending_autosaves_failure_write_readback_receipts(self):
  j=Joined();j.finish();self.assertEqual([r['cue'] for r in j.w.pending_autosaves],list(ORDER));before=j.w.save();old=j.w.pending_autosaves[0]['request_id']
  with tempfile.TemporaryDirectory() as td:
   directory=Path(td)
   with self.assertRaises(OSError):(directory/'absent'/'save.json').write_text(json.dumps(j.w.save()))
   self.assertEqual(j.w.save(),before);j.w=P13World.load(j.w.save(),context=j.context());self.assertEqual(j.w.acknowledge_autosave(old).code,'stale_autosave')
   for request in tuple(j.w.pending_autosaves):
    target=directory/(request['cue']+'.json');data=j.w.save()
    with target.open('w') as handle:json.dump(data,handle);handle.flush();os.fsync(handle.fileno())
    loaded=json.loads(target.read_text());self.assertEqual(P13World.load(loaded,context=j.context()).save(),data)
    self.assertEqual(j.w.acknowledge_autosave(request['request_id']).code,'autosave_acknowledged')
    self.assertEqual(j.w.acknowledge_autosave(request['request_id']).code,'stale_autosave')
  self.assertEqual(j.w.pending_autosaves,());self.assertTrue(j.w.ready)

 def test_current_pa_attention_rechecks_through_p08_orientation(self):
  j=Joined();j.board();j.contest();j.p8.orient_pa(j.c8,Facing.NEIGHBOR)
  self.assertEqual(j.w.call_attention(j.context()).code,'working_microphone_required')
  j.p8.orient_pa(j.c8,Facing.INWARD);p=j.w.call_attention(j.context());self.assertIsNotNone(p.presentation_id)
  j.rig=replace(j.rig,connected=False);self.assertEqual(j.w.acknowledge_presentation(j.context(),p.presentation_id,record_id='P13.SUCCESS.008').code,'working_microphone_required')
  j.rig=replace(j.rig,connected=True);shown(j.w,j.context(),'attention');self.assertEqual(j.w.pull_toast(j.context()).code,'toast_complete')

 def test_corrupt_receipts_order_context_and_source_restore_barriers(self):
  j=Joined();j.finish();good=j.w.save()
  for source in ('rita_ready','reveal','attention'):
   corrupt=copy.deepcopy(good);corrupt['state']['presentations'].pop(source)
   with self.assertRaises(ValueError):P13World.load(corrupt)
   with self.assertRaises(ValueError):restore_words(list(encode_save(corrupt).values()))
  for field in ('seated_at','pot_at','served_at','display_at','screen_at','show_at','board_at'):
   corrupt=copy.deepcopy(good);corrupt['state'][field]=0
   with self.assertRaises(ValueError):P13World.load(corrupt)
   with self.assertRaises(ValueError):restore_words(list(encode_save(corrupt).values()))
  with self.assertRaises(ValueError):j.w.validate_context(j.context(board_room=LIVING))
  with self.assertRaises(ValueError):j.w.validate_context(j.context(buffet_at_hatch=False))
  for obj in ('hotpot_pot','folded_display','handcart','pledge_board'):
   with self.assertRaises(ValueError):j.context(inventory=frozenset({obj}))
  self.assertEqual(M['objects']['hotpot_pot'],92);self.assertEqual(M['objects']['handcart'],72);self.assertEqual(M['objects']['folded_display'],42);self.assertEqual(M['objects']['completed_screen'],81)

if __name__=='__main__':unittest.main()
