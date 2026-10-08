"""P11 safety, reversibility, protected admissions and stale callback proof."""
import copy
from collections import deque
from dataclasses import replace
import itertools
import json
from pathlib import Path
import unittest

from cakood.model import Verb
from cakood.p04_model import GateHandoff
from cakood.p11_model import (P11Context, P11World, RescuePhase, PREREQUISITES,
    SIDE_PASSAGE, PORCH, COURTYARD, CONSERVATORY, RECORD_UNITS, UNIT_SPEAKERS)

GATE = GateHandoff('hold_open_peg', SIDE_PASSAGE, True, True, False, True, False, ())
C = P11Context(SIDE_PASSAGE, GATE, flags=PREREQUISITES)


def clone(world, context=None):
    return P11World.load(json.loads(json.dumps(world.save())), context=context)


def read(world, context, source):
    p = world.begin_presentation(context, source)
    if p.presentation_id:
        world.acknowledge_presentation(context, p.presentation_id, record_id=world.SOURCES[source])
    return p


def peg(world, context):
    world.request_peg(context)
    context = replace(context, gate=replace(context.gate, peg_engaged=True, gate_open=True))
    if world.pending_peg_request_id:
        world.acknowledge_peg(context, world.pending_peg_request_id)
    return context


def rescue(world=None, context=C, order=('peg', 'catch')):
    world = world or P11World()
    world.lift(context)
    for action in order:
        if action == 'peg': context = peg(world, context)
        else: world.release_catch(context)
    world.pull_handle(context); world.stage_display(context)
    return world, context


class P11ModelTests(unittest.TestCase):
    def test_both_p09_and_p10_are_required_but_no_contest_win_is(self):
        for missing in PREREQUISITES:
            w=P11World(); before=w.save()
            self.assertEqual(w.lift(replace(C, flags=C.flags-{missing})).code, 'p09_and_p10_required')
            self.assertEqual(w.save(), before)
        w=P11World(); self.assertEqual(w.lift(C).code, 'display_supported')
        self.assertFalse(any('VC' in flag for flag in C.flags))

    def test_actual_p09_p10_branches_join_in_either_order(self):
        from cakood.p09_model import P09Context, P09World
        from cakood.p10_model import P10Context, P10World, TILE_IDS, ORDER, LIVING
        for order in itertools.permutations(('P09', 'P10')):
            p09=P09World(); p10=P10World()
            flags=frozenset(('EVENING_STARTED','PLAN_AGREED'))
            for branch in order:
                if branch == 'P09':
                    c09=P09Context(CONSERVATORY,flags=flags)
                    for source in ('direct_question','terms'):
                        p=p09.begin_presentation(c09,source)
                        record='P09.DIALOGUE.001' if source=='direct_question' else 'P09.DIALOGUE.002'
                        p09.acknowledge_presentation(c09,p.presentation_id,record_id=record)
                    flags=flags|p09.flags
                else:
                    c10=P10Context(LIVING,flags=flags,
                                   inventory=frozenset((*TILE_IDS,'grease_pencil')))
                    p10.introduce(c10)
                    p=p10.begin_presentation(c10,'plan')
                    p10.acknowledge_presentation(c10,p.presentation_id,record_id='P10.READ.001')
                    for i,obj in enumerate(TILE_IDS):
                        p10.write(c10,obj,ORDER[i])
                        p10.place(replace(c10,room=COURTYARD),obj,i)
                    flags=flags|p10.flags
                # Each branch's first completion alone is insufficient for P11.
                if branch == order[0]:
                    self.assertEqual(P11World().lift(replace(C,flags=flags)).code,'p09_and_p10_required')
            self.assertTrue(p09.ready and p10.ready)
            w,c=rescue(context=replace(C,flags=flags))
            read(w,c,'sincere')
            self.assertTrue(w.contest_eligible)
            self.assertEqual(p09.inventory,('renewal_repair_card',))
            self.assertFalse(p09.terms_card_handoff['signed'])

    def test_lift_requires_original_cart_display_and_actual_felix(self):
        for key in ('cart_room','display_room','felix_room'):
            w=P11World(); before=w.save(); w.lift(replace(C, **{key:CONSERVATORY}))
            self.assertEqual(w.save(), before)
        self.assertEqual(P11World().inventory, ())

    def test_peg_request_does_not_forge_p04_ownership(self):
        w=P11World(); w.lift(C); r=w.request_peg(C)
        self.assertFalse(C.gate.peg_engaged)
        self.assertEqual(r.events[0].payload['owner'], 'P04')
        self.assertEqual(w.acknowledge_peg(C, w.pending_peg_request_id).code, 'peg_not_yet_engaged')
        self.assertEqual(w.pull_handle(C).code, 'peg_required')
        self.assertFalse(w.ready)

    def test_each_helper_order_has_identical_safe_result(self):
        for order in itertools.permutations(('peg','catch')):
            w,c=rescue(order=order)
            self.assertTrue(w.ready)
            self.assertEqual(w.flags, {'DISPLAY_STAGED','HELP_ACCEPTED'})
            self.assertFalse(w.supported)
            self.assertFalse(w.display_handoff['panel_revealed'])
            self.assertFalse(w.display_handoff['rita_reveal_consent'])
            self.assertTrue(w.display_handoff['covered'])
            self.assertEqual(w.display_handoff['cart_id'], 'handcart')
            self.assertFalse(w.contest_eligible)
            self.assertEqual(clone(w,c).save(), w.save())

    def test_preengaged_peg_is_preserved_and_satisfies_substep(self):
        c=replace(C, gate=replace(GATE, peg_engaged=True))
        w=P11World(); w.lift(c)
        self.assertEqual(w.advance_peg_at, w.lift_at)
        before=w.save()
        self.assertEqual(w.request_peg(c).line_ids, ('P11.SUCCESS.002',))
        self.assertEqual(w.save(), before)
        w.release_catch(c); w.pull_handle(c); w.stage_display(c)
        self.assertTrue(w.ready)
        self.assertEqual(w.peg_ack_at, 0)

    def test_released_peg_is_rechecked_at_pull(self):
        w=P11World(); w.lift(C); c=peg(w,C); w.release_catch(c)
        before=w.save()
        self.assertEqual(w.pull_handle(C).code, 'peg_required')
        self.assertEqual(w.save(), before)
        self.assertEqual(w.pull_handle(c).code, 'display_folded_safe')

    def test_helper_locations_follow_opposite_sides_without_teleport(self):
        w=P11World(); w.lift(C); before=w.save()
        self.assertEqual(w.request_peg(replace(C,bunny_room=SIDE_PASSAGE)).code, 'bunny_at_porch_required')
        self.assertEqual(w.release_catch(replace(C,frankie_room=SIDE_PASSAGE)).code, 'frankie_at_courtyard_required')
        self.assertEqual(w.save(), before)
        self.assertEqual(C.bunny_room, PORCH); self.assertEqual(C.frankie_room, COURTYARD)

    def test_pull_missing_substeps_gives_exact_canonical_feedback(self):
        w=P11World(); w.lift(C); before=w.save()
        self.assertEqual(w.pull_handle(C).line_ids, ('P11.FAILURE.002',))
        self.assertEqual(w.save(), before)
        c=peg(w,C); before=w.save()
        self.assertEqual(w.pull_handle(c).line_ids, ('P11.FAILURE.003',))
        self.assertEqual(w.save(), before)

    def test_physical_safety_never_requires_caption_audio_or_reaction(self):
        w,c=rescue()
        self.assertEqual(w.presentations,{})
        self.assertTrue(w.ready)
        self.assertEqual(w.laugh_at,0)
        self.assertEqual(w.request_contest(c).code,'rescue_and_conversation_required')
        self.assertFalse(w.flags & {'INTRODUCTION_CLEAR','VC03_RESOLVED','VC03_WON','GAME_COMPLETE'})

    def test_sincere_units_must_all_be_seen_before_contest(self):
        w=P11World(); w.lift(C); p=w.begin_presentation(C,'sincere')
        units=RECORD_UNITS['P11.DIALOGUE.002']
        w.acknowledge_presentation(C,p.presentation_id,speech_unit_ids=units[:5])
        w,c=rescue(w)
        self.assertFalse(w.sincere_complete)
        self.assertEqual(w.request_contest(c).line_ids,('VC03.NOT_READY',))
        w.acknowledge_presentation(c,p.presentation_id,speech_unit_ids=units[5:])
        self.assertTrue(w.contest_eligible)
        self.assertEqual(w.request_contest(c).line_ids,('VC03.ENTRY',))

    def test_sincere_conversation_can_start_on_safe_cart_after_interruption(self):
        w,c=rescue(); read(w,c,'sincere')
        self.assertTrue(w.sincere_complete); self.assertTrue(w.contest_eligible)
        self.assertEqual(w.phase,RescuePhase.STAGED)
        self.assertIn('P11.DIALOGUE.002',w.journal_records())

    def test_sincere_text_alone_cannot_start_contest_while_supported(self):
        w=P11World(); w.lift(C); read(w,C,'sincere')
        self.assertTrue(w.sincere_complete)
        before=w.save(); self.assertEqual(w.request_contest(C).code,'rescue_and_conversation_required')
        self.assertEqual(w.save(),before); self.assertFalse(w.contest_eligible)

    def test_concern_remains_protected_across_safe_recovery(self):
        w=P11World(); w.lift(C); p=w.begin_presentation(C,'concern')
        w.acknowledge_presentation(C,p.presentation_id,speech_unit_ids=('P11.DIALOGUE.001.01',))
        w,c=rescue(w); read(w,c,'sincere'); read(w,c,'fold')
        self.assertTrue(w.concern_pending); self.assertFalse(w.contest_eligible)
        self.assertEqual(w.claim_laugh(c).code,'protected_scene')
        w.acknowledge_presentation(c,p.presentation_id,record_id='P11.DIALOGUE.001')
        self.assertTrue(w.contest_eligible)
        self.assertEqual(w.claim_laugh(c).events[0].id,'LAF11')

    def test_no_fresh_concern_is_invented_after_safe_staging(self):
        w,c=rescue(); before=w.save()
        self.assertEqual(w.begin_presentation(c,'concern').code,'initial_concern_finished')
        self.assertEqual(w.save(),before)

    def test_laf11_is_single_earned_output_never_replayed_after_load(self):
        w,c=rescue(); read(w,c,'sincere'); read(w,c,'fold')
        self.assertEqual(w.claim_laugh(c).events[0].id,'LAF11')
        restored=clone(w); before=restored.save()
        self.assertEqual(restored.claim_laugh(c).code,'laugh_already_consumed')
        self.assertEqual(restored.save(),before)
        self.assertEqual(restored.begin_presentation(c,'fold').code,'presentation_complete')

    def test_laugh_waits_for_safe_staging_full_payoff_and_sincerity(self):
        w=P11World(); w.lift(C); read(w,C,'sincere'); c=peg(w,C); w.release_catch(c); w.pull_handle(c)
        read(w,c,'fold'); self.assertEqual(w.claim_laugh(c).code,'protected_scene')
        w.stage_display(c); self.assertEqual(w.claim_laugh(c).code,'earned_physical_reaction')

    def test_set_back_is_always_safe_and_resets_only_current_posture(self):
        for peg_first, catch_first in itertools.product((False,True),repeat=2):
            w=P11World(); w.lift(C); c=peg(w,C) if peg_first else C
            if catch_first: w.release_catch(c)
            read(w,c,'sincere'); w.set_back(c)
            self.assertEqual(w.phase,RescuePhase.CART)
            self.assertFalse(w.catch_at); self.assertFalse(w.peg_request_at)
            self.assertTrue(w.sincere_complete); self.assertFalse(w.ready)
            self.assertEqual(c.gate.peg_engaged,peg_first)
            before=w.save(); self.assertEqual(w.set_back(c).code,'already_safe'); self.assertEqual(w.save(),before)
            w,c=rescue(w,c); self.assertTrue(w.ready)

    def test_travel_escape_does_not_trap_menu_or_apron(self):
        w=P11World(); w.lift(C); c=replace(C,room=CONSERVATORY,on_apron=True,contest_active=True,
                                        flags=frozenset(),felix_room=CONSERVATORY)
        with self.assertRaises(ValueError): w.validate_context(c)
        self.assertEqual(w.set_back(c).code,'display_back_on_cart')
        self.assertFalse(w.supported)
        self.assertEqual(c.room,CONSERVATORY)

    def test_old_peg_callback_is_stale_after_return_and_after_load(self):
        w=P11World(); w.lift(C); w.request_peg(C); old=w.pending_peg_request_id
        restored=clone(w); before=restored.save()
        self.assertEqual(restored.acknowledge_peg(C,old).code,'stale_peg_request')
        self.assertEqual(restored.save(),before)
        w.set_back(C); w.lift(C); w.request_peg(C)
        self.assertNotEqual(old,w.pending_peg_request_id)
        self.assertEqual(w.acknowledge_peg(C,old).code,'stale_peg_request')

    def test_caption_callback_from_abandoned_save_timeline_cannot_commit(self):
        w=P11World(); w.lift(C); p=w.begin_presentation(C,'sincere')
        restored=clone(w); before=restored.save()
        self.assertEqual(restored.acknowledge_presentation(C,p.presentation_id,
            record_id='P11.DIALOGUE.002').code,'stale_presentation')
        self.assertEqual(restored.save(),before)
        read(restored,C,'sincere'); self.assertTrue(restored.sincere_complete)

    def test_staged_rita_speech_waits_for_actual_presence_not_physical_progress(self):
        w,c=rescue(); self.assertTrue(w.ready)
        self.assertEqual(w.begin_presentation(c,'staged').code,'speaker_absent')
        read(w,replace(c,rita_room=SIDE_PASSAGE),'staged')
        self.assertIn('P11.SUCCESS.006',w.journal_records())
        self.assertFalse(w.display_handoff['rita_reveal_consent'])

    def test_pure_look_hints_and_notebook_do_not_award_sincere_receipts(self):
        w=P11World(); w.lift(C); before=w.save()
        w.look(C,'display_wing'); w.journal_records(); w.journal_units()
        self.assertEqual(w.save(),before)
        w.hint(C,3); self.assertFalse(w.sincere_complete)
        self.assertFalse(w.ready)

    def test_duplicate_physical_actions_do_not_regrant(self):
        w,c=rescue(); before=w.save()
        for action in (w.stage_display,w.pull_handle,w.lift,w.set_back):
            self.assertFalse(action(c).events)
            self.assertEqual(w.save(),before)
        self.assertEqual(w.inventory,())

    def test_contest_handoff_is_exact_idempotent_and_cancellable(self):
        w,c=rescue(); read(w,c,'sincere'); w.request_contest(c); token=w.pending_contest_request_id
        before=w.save(); self.assertEqual(w.request_contest(c).code,'contest_request_pending')
        self.assertEqual(w.save(),before)
        away=replace(c,felix_room=CONSERVATORY)
        self.assertEqual(w.acknowledge_contest_request(away,token).code,'contest_handoff_unavailable')
        w.acknowledge_contest_request(away,token,cancelled=True)
        self.assertTrue(w.ready); self.assertIsNone(w.pending_contest_request_id)
        self.assertEqual(w.acknowledge_contest_request(c,token).code,'stale_contest_request')
        w.request_contest(c); fresh=w.pending_contest_request_id
        self.assertNotEqual(token,fresh)
        restored=clone(w)
        self.assertEqual(restored.acknowledge_contest_request(c,fresh).code,'stale_contest_request')
        restored.acknowledge_contest_request(c,restored.pending_contest_request_id)
        self.assertFalse(restored.flags & {'VC03_RESOLVED','VC03_WON'})

    def test_later_contest_loss_or_rematch_never_undoes_rescue(self):
        w,c=rescue(); read(w,c,'sincere')
        c=replace(c,flags=c.flags|{'VC03_RESOLVED','VC03_WON'})
        self.assertEqual(w.request_contest(c).line_ids,('VC03.REMATCH',))
        self.assertTrue(w.ready); self.assertTrue(w.sincere_complete)
        self.assertFalse(w.display_handoff['panel_revealed'])

    def test_save_rejects_future_rewards_nonprefix_receipts_and_invalid_phases(self):
        w,c=rescue(); read(w,c,'sincere'); pristine=w.save()
        mutations=(lambda s:s.update(phase=True),lambda s:s.update(catch_at=0),
                   lambda s:s.update(stage_at=1),lambda s:s.update(laugh_at=1),
                   lambda s:s.update(peg_request_at=1),lambda s:s.update(phase=1),
                   lambda s:s.update(game_complete=True),
                   lambda s:s['presentations']['sincere']['receipts'].pop('P11.DIALOGUE.002.01'),
                   lambda s:s.update(contest_request_at=s['stage_at']))
        for mutate in mutations:
            d=copy.deepcopy(pristine); mutate(d['state'])
            with self.assertRaises(ValueError): P11World.load(d)
        self.assertEqual(w.save(),pristine)

    def test_saves_at_every_sincere_page_preserve_exact_prefix(self):
        for n in range(7):
            w=P11World(); w.lift(C); p=w.begin_presentation(C,'sincere')
            units=RECORD_UNITS['P11.DIALOGUE.002']
            if n: w.acknowledge_presentation(C,p.presentation_id,speech_unit_ids=units[:n])
            w=clone(w,C); self.assertEqual(w.journal_units(),units[:n])
            w,c=rescue(w); read(w,c,'sincere'); self.assertTrue(w.contest_eligible)

    def test_load_rejects_contest_or_laugh_before_completed_concern(self):
        for consequence in ('contest', 'laugh'):
            w=P11World(); w.lift(C); read(w,C,'concern')
            w,c=rescue(w); read(w,c,'sincere'); read(w,c,'fold')
            if consequence == 'contest': w.request_contest(c)
            else: w.claim_laugh(c)
            data=w.save(); state=data['state']; state['revision']+=1
            receipts=state['presentations']['concern']['receipts']
            for token in receipts: receipts[token]=state['revision']
            with self.assertRaises(ValueError): P11World.load(data,context=c)

    def test_bounded_state_exploration_has_recovery_from_every_state(self):
        def key(w,c):
            return (w.phase,bool(w.first_lift_at),bool(w.catch_at),bool(w.peg_request_at),
                    c.gate.peg_engaged,w.sincere_complete)
        queue=deque([(P11World(),C)]); seen={}; edges=0
        def action(w,c,index):
            if index==0: w.lift(c)
            elif index==1: w.release_catch(c)
            elif index==2: w.request_peg(c)
            elif index==3: w.pull_handle(c)
            elif index==4: w.stage_display(c)
            elif index==5: w.set_back(c)
            elif index==6:
                if w.first_lift_at: read(w,c,'sincere')
            elif index==7: w.push_harder(c)
            elif index==8 and w.supported:
                c=replace(c,gate=replace(c.gate,peg_engaged=True))
                if w.pending_peg_request_id:
                    w.acknowledge_peg(c,w.pending_peg_request_id)
            elif index==9:
                c=replace(c,gate=replace(c.gate,peg_engaged=False))
            return c
        while queue:
            w,c=queue.popleft(); k=key(w,c)
            if k in seen: continue
            seen[k]=(w.save(),c)
            for i in range(10):
                nxt=clone(w); nc=action(nxt,c,i); edges+=1; nxt.validate()
                if nxt.supported: self.assertFalse(nxt.contest_eligible)
                if key(nxt,nc) not in seen: queue.append((nxt,nc))
        self.assertIn((1,True,True,True,False,False),seen)
        self.assertIn((3,True,True,False,True,True),seen)
        for data,c in seen.values():
            w=P11World.load(data)
            if w.supported: w.set_back(c)
            if w.phase==RescuePhase.CART: w,c=rescue(w,c)
            elif w.phase==RescuePhase.FOLDED: w.stage_display(c)
            read(w,c,'sincere')
            self.assertTrue(w.contest_eligible)
            self.assertEqual(w.flags,{'DISPLAY_STAGED','HELP_ACCEPTED'})
        self.assertEqual(edges,len(seen)*10)

    def test_all_verbs_and_fixed_objects_do_not_invent_plot(self):
        w=P11World(); w.lift(C)
        for verb,obj in itertools.product(Verb,('ceramic_panel','hold_open_peg','audience','staging_pocket')):
            r=w.act(C,verb,obj)
            self.assertEqual(r.text,'')
            self.assertTrue(set(r.line_ids)<=set(RECORD_UNITS))
        self.assertFalse(w.ready)

    def test_fixture_locks_canonical_ids_speakers_and_laf11(self):
        f=json.loads((Path(__file__).parent/'fixtures/p11/canonical-bindings.json').read_text())
        self.assertEqual(f['catalog_sha256'],'1226a97873a3693867c08afe2731ddb55adef6f0eaeabc1222e103c04c0d9fa7')
        self.assertEqual(set(RECORD_UNITS),set(f['records']))
        self.assertEqual(UNIT_SPEAKERS,{u['line_id']:u['speaker_id'] for u in f['speech_units']})
        laugh=[u['line_id'] for u in f['speech_units'] if (u.get('laugh_opportunity') or {}).get('canonical_cue_id')=='LAF11']
        self.assertEqual(laugh,['P11.SUCCESS.005.02'])


if __name__=='__main__': unittest.main()
