"""NEW ordinary-current-flow regressions; no native or full-campaign claim."""
from pathlib import Path
import copy,json,unittest,itertools,tempfile,os,hashlib
from dataclasses import replace
from finale_join import FinaleJoined
from test_late_campaign_models import c14,contests,UNSIGNED,finish14,read
from test_verbal_contest import prepared,play,leave,CATALOG
from cakood.p14_model import *
from cakood.verbal_contest import VerbalContests,Phase

class CurrentJoinTests(unittest.TestCase):
 def test_real_p13_loss_completes_practical_work_but_no_signature(self):
  x=FinaleJoined();c=x.context();before=x.j.w.save();vc=x.j.vc.snapshot()
  self.assertTrue(x.j.w.ready);self.assertTrue({'SERVED','DISPLAY_REVEALED','TOAST_READY'}<=c.flags)
  self.assertEqual(P14World.missing_wins(c),CONTEST_IDS)
  for _ in range(3):
   self.assertEqual(x.start().code,'all_four_actual_wins_required');g=x.w.notebook_gate(c)
   self.assertEqual(g['won_count'],0);self.assertTrue(g['practical_progress_unchanged'])
  self.assertEqual(x.j.w.save(),before);self.assertEqual(x.j.vc.snapshot(),vc);self.assertFalse(x.w.signature_at)
  self.assertFalse(x.w.ready);self.assertEqual(x.w.inventory,())

 def test_every_actual_win_subset_and_final_threshold(self):
  for bits in itertools.product((False,True),repeat=4):
   vc=contests(wins=tuple(e for e,b in zip(CONTEST_IDS,bits) if b),losses=tuple(e for e,b in zip(CONTEST_IDS,bits) if not b))
   c=c14(vc);w=P14World();r=w.start(c,UNSIGNED)
   self.assertEqual(bool(w.start_at),all(bits),bits)
   self.assertEqual(w.notebook_gate(c)['won_count'],sum(bits))
   self.assertEqual(r.code,'commitments_started' if all(bits) else 'all_four_actual_wins_required')

 def test_genuine_rematches_preserve_learning_prior_wins_and_first_receipts(self):
  x=FinaleJoined();prior=x.j.vc.snapshot()['knowledge'];rooms=dict(x.j.actors)
  for i,enc in enumerate(CONTEST_IDS):
   x.contest(enc,True);self.assertEqual(x.w.notebook_gate(x.context())['won_count'],i+1)
   self.assertEqual(x.j.vc.snapshot()['knowledge'],prior)
  first={a.encounter_id:a.outcome.id for a in x.j.vc.attempts if a.outcome.winner=='jack'}
  for enc in CONTEST_IDS:x.contest(enc,False)
  self.assertEqual(x.w.notebook_gate(x.context())['won_count'],4)
  self.assertEqual(x.start().code,'commitments_started');self.assertEqual(x.w.winning_attempts,first)
  self.assertEqual(x.j.actors,rooms)
  packet=x.restore_contests();self.assertEqual(x.j.vc.snapshot()['knowledge'],prior)
  self.assertEqual(x.w.winning_attempts,first);x.w.validate_context(x.context())
  self.assertEqual(packet['owner']['payload']['state']['history'],x.j.vc.snapshot()['history'])

 def test_unread_real_win_and_active_rematch_cannot_start(self):
  x=FinaleJoined()
  for enc in CONTEST_IDS[:-1]:x.contest(enc,True)
  x.contest('VC04',True,read_result=False)
  self.assertTrue('ALL_VC_WON' in x.j.vc.flags);self.assertEqual(x.start().code,'contest_active')
  leave(x.j.vc);self.assertEqual(x.start().code,'commitments_started')
  x.j.vc.enter('VC04',0,admitted=True)
  self.assertEqual(x.w.give_card(x.context(),'rita','rita').code,'contest_active')

 def test_owner_aggregates_never_synthesize_positive_attempt_receipts(self):
  v=contests(wins=CONTEST_IDS);raw=v.save()
  unpaired=VerbalContests.load(raw,owner_generation=2)
  self.assertEqual(unpaired.missing_wins,())
  with self.assertRaisesRegex(ValueError,'paired observed'):tuple(unpaired.attempts)
  before=P14World().save();w=P14World()
  with self.assertRaisesRegex(ValueError,'paired observed'):w.start(c14(unpaired),UNSIGNED)
  self.assertEqual(w.save(),before)
  saved=v.save_with_evidence();broken=copy.deepcopy(saved);broken['observations'].pop(0)
  with self.assertRaises(ValueError):VerbalContests.load_with_evidence(broken,owner_generation=2)
  other=contests(losses=CONTEST_IDS);broken['owner']=json.loads(other.save())
  with self.assertRaises(ValueError):VerbalContests.load_with_evidence(broken,owner_generation=2)

 def test_original_p09_terms_are_earned_and_transferred_once(self):
  x=FinaleJoined();p9=x.j.p9
  self.assertTrue(p9.ready);self.assertTrue(p9.rumor_cleared)
  self.assertEqual(p9.consumed['P09_TERMS'],p9.presentations['terms'].receipts['P09.DIALOGUE.002.05'])
  self.assertEqual(p9.terms_card_handoff,UNSIGNED);original=p9.save()
  x.finish();self.assertEqual(x.terms_owner,'P14');self.assertNotIn(TERMS,x.inventory)
  self.assertEqual(sum(n=='P14_TERMS_SIGNED' for n,p in x.events),1)
  self.assertEqual(p9.save(),original) # Old projection suppression belongs to host.
  self.assertEqual(x.w.reserved_external_objects,{TERMS});self.assertTrue(x.w.ready)
  self.assertEqual(x.pencil_owner,'inventory');self.assertIn(PENCIL,x.inventory)
  self.assertEqual(sum(n=='P14_PENCIL_HANDOFF' for n,p in x.events),1)
  self.assertEqual(sum(n=='P14_GAME_COMPLETE' for n,p in x.events),1)
  self.assertEqual(x.w.dynamic_bindings,{'repair_date':'the agreed Saturday'})

 def test_wins_cannot_override_rita_vivian_or_any_individual_consent(self):
  x=FinaleJoined();x.win_all();x.start();c=x.context()
  for person in PEOPLE:
   self.assertEqual(x.w.pin_card(c,person).code,'approval_required')
   if person!='jack':
    absent=replace(c,npc_locations=tuple((p,LIVING if p==person else r) for p,r in c.npc_locations))
    self.assertEqual(x.w.give_card(absent,person,person).code,'recipient_absent')
   r=x.w.give_card(c,person,person);x.w.audio_finished()
   self.assertNotIn(person,x.w.approved)
   old=r.presentation_id;x.w=P14World.load(x.w.save())
   self.assertEqual(x.w.acknowledge_presentation(c,old,record_id='P14.APPROVE.'+person).code,'stale_presentation')
   read(x.w,c,'approve:'+person);x.w.pin_card(c,person)
  self.assertEqual(set(x.w.pinned),set(PEOPLE));self.assertFalse(x.w.signature_at)
  for method in ('forge','coerce'):
   self.assertEqual(x.w.request_signature(c,method).line_ids,('P14.FAILURE.002',));self.assertFalse(x.w.signature_at)

 def test_actual_people_board_and_original_inventory_gate(self):
  x=FinaleJoined();x.win_all();c=x.context()
  self.assertEqual(x.w.start(replace(c,board_room=LIVING),UNSIGNED).code,'board_not_physically_delivered')
  self.assertEqual(x.w.start(replace(c,inventory=frozenset({PENCIL})),UNSIGNED).code,'original_terms_card_required')
  self.assertEqual(x.w.start(replace(c,repair_date=''),UNSIGNED).code,'agreed_fictional_date_required')
  for k,v in [('signed',True),('location','pledge_board'),('repair_date','Saturday'),('signature_owner','P09'),('terms_record_id','P09.READ.001')]:
   with self.assertRaises(ValueError):x.w.start(c,{**UNSIGNED,k:v})
  self.assertFalse(x.w.start_at)

 def test_partial_source_save_readback_resume_and_repeated_signature(self):
  for prefix in range(6):
   x=FinaleJoined();x.win_all();x.approvals();c=x.context();w=x.w
   p=w.request_signature(c);tokens=w._tokens('signature')
   if prefix:w.acknowledge_presentation(c,p.presentation_id,speech_unit_ids=tokens[:prefix])
   with tempfile.TemporaryDirectory(prefix='p14 save ' ) as td:
    path=Path(td)/'partial signature.json';data={'world':w.save(),'contest':x.j.vc.save_with_evidence()}
    with path.open('w') as f:json.dump(data,f);f.flush();os.fsync(f.fileno())
    back=json.loads(path.read_text());self.assertEqual(back,data)
   x.j.vc=VerbalContests.load_with_evidence(back['contest'],owner_generation=2);x.w=P14World.load(back['world']);c=x.context()
   self.assertEqual(x.w.acknowledge_presentation(c,p.presentation_id,record_id='P14.DIALOGUE.003').code,'stale_presentation')
   if prefix<5:self.assertEqual(x.w.pin_signature(c).code,'whole_consent_scene_required')
   read(x.w,c,'signature');x.event(x.w.pin_signature(c));after=x.w.save()
   self.assertEqual(x.w.pin_signature(x.context()).code,'already_signed');self.assertEqual(x.w.save(),after)

 def test_detached_parallel_credit_viewers_never_mutate_completed_or_contest(self):
  x=FinaleJoined();x.finish();x.w.start_finale(tuple(ASSET_CREDITS.values()));x.w.skip_finale()
  original=x.w.save();owner=x.j.vc.snapshot();session={'world':copy.deepcopy(original),'contest':x.j.vc.save_with_evidence(),'unrelated':{'room':LIVING,'inventory':[PENCIL]}}
  one=x.w.create_credit_replay(session);two=x.w.create_credit_replay(session);two_initial=two.save()
  one.world.pause_finale(True);one=CreditReplay.load(json.loads(json.dumps(one.save())))
  returned=one.return_session(cancel=True);returned['unrelated']['inventory'].clear()
  self.assertEqual(one.return_session(),session);self.assertEqual(two.save(),two_initial)
  for record in two.world.credit_ids:
   read(two.world,x.context(),'credit:'+record);two.world.advance_finale()
  self.assertEqual(two.return_session(),session);self.assertEqual(x.w.save(),original);self.assertEqual(x.j.vc.snapshot(),owner)

 def test_two_source_credit_viewers_keep_owner_arenas_and_sessions_independent(self):
  from codec import NativeCreditReplay,encode_world,project_context,M
  import source_vm
  x=FinaleJoined();x.finish();x.w.start_finale();x.w.skip_finale()
  source=source_vm.VM();source.p.update(encode_world(x.w))
  origin=copy.deepcopy((source.p,source.arrays,x.w.save(),x.j.vc.snapshot()))
  session={'contest':x.j.vc.save_with_evidence(),'inventory':[PENCIL]}
  first=NativeCreditReplay.create(source,session,source_vm.VM)
  second=NativeCreditReplay.create(source,session,source_vm.VM)
  untouched=copy.deepcopy((second.viewer.p,second.viewer.arrays,second.save()))
  project_context(first.viewer.call,x.context(),1)
  sid=M['sources']['credit:'+CREDIT_ORDER[0]]
  first.viewer.call('p14Begin',sid)
  hi=first.viewer.p['p14PresentationHi'];lo=first.viewer.p['p14PresentationLo']
  first.viewer.call('p14Acknowledge',sid,hi,lo,1,M['line_ids'][CREDIT_ORDER[0]],0,0)
  first.viewer.call('p14AdvanceFinale');first.viewer.call('p14PauseFinale',1)
  first=NativeCreditReplay.load(json.loads(json.dumps(first.save())),source_vm.VM)
  self.assertEqual(first.viewer.p['p14CreditCursor'],1);self.assertTrue(first.viewer.p['p14Paused'])
  returned=first.return_session(cancel=True);returned['inventory'].clear()
  self.assertEqual(first.return_session(),session)
  self.assertEqual((second.viewer.p,second.viewer.arrays,second.save()),untouched)
  self.assertEqual((source.p,source.arrays,x.w.save(),x.j.vc.snapshot()),origin)
  self.assertEqual(second.return_session(cancel=True),session)

 def test_current_canonical_fields_equal_including_all_writer_and_asset_credits(self):
  c=Path(__file__).resolve().parents[1];fixture=json.loads((c/'tests/fixtures/p14/canonical-bindings.json').read_text())
  cat={r['id']:r for r in json.loads((c/'authority/full-line-catalog.json').read_text())['records']}
  speech={u['line_id']:u for u in json.loads((c/'authority/speech-units.json').read_text())['units']}
  self.assertEqual(len(fixture['records']),125);self.assertEqual(len(fixture['speech_units']),43)
  for record in fixture['records']:self.assertEqual(record,cat[record['id']])
  for unit in fixture['speech_units']:self.assertEqual(unit,speech[unit['line_id']])
  writers=[r for r in CREDIT_ORDER if r.startswith('END.CREDIT.WRITERS.') and not r.endswith('HEADER')]
  self.assertEqual(len(writers),8);self.assertEqual(len(CREDIT_ORDER),26);self.assertEqual(len(ASSET_CREDITS),33)
  for r in writers:self.assertIn(r,{x['id'] for x in fixture['records']})

 def test_notebook_location_boundary_never_moves_post_p13_actors(self):
  x=FinaleJoined();before=dict(x.j.actors);g=x.w.notebook_gate(x.context())
  for enc in CONTEST_IDS:self.assertEqual(g['rematch_locations'][enc],REMATCH_LOCATIONS[enc])
  self.assertEqual(x.j.actors,before)
  self.assertNotEqual(before['milo'],REMATCH_LOCATIONS['VC01'])
  self.assertNotEqual(before['vivian'],REMATCH_LOCATIONS['VC02'])
  self.assertNotEqual(before['felix'],REMATCH_LOCATIONS['VC03'])
  self.assertEqual(before['stringer'],REMATCH_LOCATIONS['VC04'])

if __name__=='__main__':unittest.main()
