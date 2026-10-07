"""P08 reversible physical layout, ownership and explicit autosave barrier."""
from copy import deepcopy
from dataclasses import replace
from itertools import permutations
import json
from pathlib import Path
import unittest

from cakood.model import Event, Result, Verb
from cakood.p08_model import (
    COURTYARD, KITCHEN, LIVING, PREPARATIONS, FLAG_IDS, LABEL_IDS,
    LAYOUT_OBJECTS, Facing, P08Context, P08World, Position, READINESS_RECORDS,
    SCRIPT_BINDINGS, SOURCE_BINDINGS, StartPhase,
)

FIXTURE = json.loads((Path(__file__).parent / "fixtures/p08/canonical-bindings.json").read_text())
C = P08Context(COURTYARD, flags=PREPARATIONS, carrier_padding="clean_towel",
               inventory=frozenset(("grease_pencil", "ceramic_sample_tiles", "wedge")),
               frankie_room=COURTYARD, bunny_room=COURTYARD)
DESTINATIONS = {"ceramic_carrier": Position.HATCH, "pa_kit": Position.WALL,
                "completed_screen": Position.ALCOVE, "serving_table": Position.HATCH,
                "credit_slate": Position.HATCH}


def clone(world, context=C):
    return P08World.load(json.loads(json.dumps(world.save())), context)


def acknowledge_host(world):
    for h in world.pending_handoffs:
        world.acknowledge_handoff(h["handoff_id"], h["serial"])


def fit(world=None, context=C):
    world = world or P08World()
    for obj, pos in DESTINATIONS.items():
        world.place(context, obj, pos)
    world.unpack_service(context)
    acknowledge_host(world)
    return world


def await_autosave(world, context=C):
    world.request_start(context)
    token = world.pending_request_id
    world.acknowledge_readiness(context, token, READINESS_RECORDS)
    result = world.confirm_start(context, token, True)
    return token, result


class P08Tests(unittest.TestCase):
    def test_canonical_bindings_exact_ids_and_result_surface(self):
        ids = set(LABEL_IDS.values()) | {x for xs in SCRIPT_BINDINGS.values() for x in xs}
        self.assertLessEqual(ids, FIXTURE["records"].keys())
        self.assertEqual(FIXTURE["editorial_revision"], 3)
        self.assertEqual(FIXTURE["catalog_sha256"], "1226a97873a3693867c08afe2731ddb55adef6f0eaeabc1222e103c04c0d9fa7")
        result = P08World().place(C, "pa_kit", Position.WALL)
        self.assertIsInstance(result, Result)
        self.assertTrue(all(isinstance(e, Event) for e in result.events))
        self.assertEqual(result.text, "")
        self.assertEqual(FIXTURE["records"]["P08.READ.004"]["text_sha256"],
                         'a7d6a0019468db46fbac78fc4600de5844cb11e218e9605d3f868b320badfd25')

    def test_native_object_proposals_do_not_duplicate_existing_manifest_ids(self):
        manifest = json.loads((Path(__file__).parents[1] / "stock-sci/p07-domain-adapter/manifest.json").read_text())
        existing = manifest["objects"]
        aliases = FIXTURE["source_aliases"]
        for obj, number in FIXTURE["reused_native_object_ids"].items():
            self.assertEqual(existing[aliases.get(obj, obj)], number)
        proposed = {int(x) for x in FIXTURE["proposed_native_object_ids"]}
        self.assertFalse(proposed & set(existing.values()))
        self.assertEqual(FIXTURE["reused_native_object_ids"]["pa_kit"], 73)
        self.assertNotIn("pa_rig", LAYOUT_OBJECTS)

    def test_p06_screen_handoff_is_unplaced_and_p07_pot_stays_kitchen(self):
        world = P08World()
        self.assertEqual(world.positions["completed_screen"], Position.UNPLACED)
        self.assertEqual(world.object_location("completed_screen", C), COURTYARD)
        self.assertFalse(world.conditions["display_concealed"])
        self.assertEqual(world.object_location("hotpot_pot", C), KITCHEN)
        before = world.save()
        self.assertEqual(world.act(C, Verb.PICK_UP, "hotpot_pot").code, "offscreen")
        self.assertEqual(world.save(), before)
        fit(world)
        self.assertEqual(world.object_location("hotpot_pot", C), KITCHEN)
        self.assertEqual(world.inventory, ())
        self.assertNotIn("SERVED", world.flags)

    def test_all_preparations_and_resolutions_but_not_wins_required(self):
        # Coherent incomplete contexts cannot place anything or return cloth.
        for missing in ("CERAMICS_READY", "FOOD_READY", "PLAN_AGREED"):
            context = replace(C, flags=PREPARATIONS - {missing})
            world = P08World(); before = world.save()
            self.assertEqual(world.place(context, "serving_table", Position.HATCH).code, "preparations_required")
            self.assertEqual(world.save(), before)
        for ready, parts in (("SOUND_READY", {"PA_TESTED", "MILO_ROLE_AGREED", "VC01_RESOLVED"}),
                             ("SCREEN_READY", {"SCREEN_BUILT", "VIVIAN_SCOPE_AGREED", "VC02_RESOLVED"})):
            for missing in parts:
                with self.assertRaises(ValueError):
                    replace(C, flags=PREPARATIONS - {missing})
                context = replace(C, flags=PREPARATIONS - {missing, ready})
                self.assertEqual(P08World().place(context, "pa_kit", Position.WALL).code, "preparations_required")
        world = fit()
        token, _ = await_autosave(world)
        world.acknowledge_autosave(C, token, True)
        self.assertEqual(world.flags, set(FLAG_IDS))
        self.assertFalse(any("WON" in f for f in world.flags))
        self.assertNotIn("GAME_COMPLETE", world.flags)

    def test_composes_real_prior_models_without_rewriting_their_history(self):
        from cakood.p03_model import P03Context, P03World, CONSERVATORY
        from cakood.p04_model import P04Context, P04World, SIDE_PASSAGE
        from cakood.p05_model import P05Context, P05World, GARAGE, Listener, Source
        from cakood.p06_model import P06Context, P06World, PORCH, Scope, Position as ScreenPosition
        from cakood.p07_model import P07Context, P07World
        plan = frozenset(("PLAN_AGREED",))
        tools = frozenset(("grease_pencil", "master_invitation", "wedge"))
        p3 = P03World(); c3 = P03Context(CONSERVATORY, flags=plan, inventory=tools)
        p3.look(c3, "class_card"); p3.begin_credit(c3); p3.select_credit(c3, "rita_stringer")
        p3.collect_cloth(replace(c3, room=KITCHEN), "clean_napkin")
        p3.pad_carrier(c3, "clean_napkin"); p3.give_slate(c3)
        p4 = P04World(); c4 = P04Context(SIDE_PASSAGE, flags=plan, inventory=tools)
        p4.open_gate(c4); p4.place_wedge(c4)
        held = replace(c4, inventory=tools - p4.reserved_external_items)
        p4.move_bunting(held, "inventory"); p4.move_bunting(held, "fixed_hook")
        p4.recover_wedge(held); p4.close_gate(c4, test=True); p4.set_peg(c4, True)
        p5 = P05World(); c5 = P05Context(GARAGE, flags=plan, inventory=tools, bunny_room=GARAGE)
        p5.invite_listener(replace(c5, room=LIVING, bunny_room=LIVING), Listener.BUNNY)
        p5.connect_microphone(c5); p5.select_source(c5, Source.MIC)
        p5.aim_speaker(c5, Listener.BUNNY.value); p5.test_microphone(c5, Listener.BUNNY)
        p5.begin_credit(c5); p5.select_credit(c5, "milo_equipment"); p5.agree_role(c5)
        p5.borrow_kit(replace(c5, flags=plan | {"VC01_RESOLVED"}))
        p6 = P06World(); c6 = P06Context(PORCH, flags=plan, inventory=tools)
        p6.agree_scope(c6, Scope.PROFESSIONAL); p6.ask_sheet(replace(c6, room=LIVING))
        p6.collect(replace(c6, room=KITCHEN), "clean_sheet")
        p6.collect(replace(c6, room=SIDE_PASSAGE), "laundry_clips")
        p6.drape_sheet(c6); p6.attach_clips(c6); p6.place_token(c6, ScreenPosition.DISPLAY_ALCOVE)
        p6.borrow_screen(replace(c6, flags=plan | {"VC02_RESOLVED"}))
        p7 = P07World(); c7 = P07Context(KITCHEN, flags=plan, inventory=tools)
        p7.acknowledge_source(c7, "recipe", "P07.READ.001")
        p7.add_base(c7); p7.measure_stock(c7, 8); p7.add_stock(c7); p7.add_vegetables(c7)
        p7.use_stove(c7); p7.use_stove(c7); p7.add_herbs(c7); p7.close_lid(c7)
        prior = (p3, p4, p5, p6, p7)
        snapshots = [w.save() for w in prior]
        flags = plan | {"VC01_RESOLVED", "VC02_RESOLVED"}
        for w in prior:
            flags |= w.flags
        context = replace(C, flags=frozenset(flags), carrier_padding=p3.cloth_return_entitlement[0],
                          inventory=tools | set(p3.inventory))
        self.assertFalse(p6.screen_handoff["layout_applied"])
        world = fit(context=context)
        token, _ = await_autosave(world, context)
        world.acknowledge_autosave(context, token, True)
        self.assertEqual([w.save() for w in prior], snapshots)
        self.assertEqual(world.returned_padding, "clean_napkin")
        self.assertEqual(p3.tile_ids, ("rita_sample_tile_1", "rita_sample_tile_2", "rita_sample_tile_3"))
        self.assertEqual(p7.pot_handoff["room"], KITCHEN)
        self.assertEqual(p7.pot_handoff["waiting_until"], "P13")
        self.assertEqual(set(world.ownership_serials), {"ceramic_carrier", "credit_slate", "pa_kit", "completed_screen", "padding"})
        self.assertFalse(world.flags & {"VC01_WON", "VC02_WON", "DISPLAY_STAGED", "SERVED"})

    def test_complete_all_120_placement_orders_and_restore_each_action(self):
        for order in permutations(LAYOUT_OBJECTS):
            world = P08World()
            for obj in order:
                world.place(C, obj, DESTINATIONS[obj])
                acknowledge_host(world)
                world = clone(world)
            self.assertFalse(world.ready)
            world.unpack_service(C); acknowledge_host(world); world = clone(world)
            self.assertTrue(world.ready)
            token, request = await_autosave(world)
            self.assertEqual(request.events[0].kind, "autosave_request")
            self.assertNotIn("P08.SYSTEM.006", request.line_ids)
            world = clone(world)
            self.assertFalse(world.evening_started)
            result = world.acknowledge_autosave(C, token, True)
            self.assertEqual(result.line_ids, ("P08.SYSTEM.006",))
            self.assertEqual(result.events[0].payload["npc_positions"]["frankie"], LIVING)
            self.assertTrue(clone(world).evening_started)

    def test_pass_is_shared_reachable_object_interface_not_room_travel(self):
        world = P08World()
        self.assertEqual(world.object_location("ceramic_carrier", C), "kitchen_pass")
        self.assertTrue(world.reachable(C, "ceramic_carrier"))
        self.assertTrue(world.reachable(replace(C, room=KITCHEN), "ceramic_carrier"))
        self.assertFalse(world.reachable(replace(C, room=LIVING), "ceramic_carrier"))
        self.assertEqual(world.place(replace(C, room=KITCHEN), "ceramic_carrier", Position.HATCH).code, "courtyard_required")
        result = world.place(C, "ceramic_carrier", Position.HATCH)
        self.assertEqual(world.object_location("ceramic_service", C), COURTYARD)
        handoff = result.events[0]
        self.assertEqual(handoff.kind, "ownership_handoff")
        self.assertEqual(handoff.payload["from_owner"], "P03")
        self.assertEqual(handoff.payload["includes"], ("ceramic_service",))
        self.assertEqual(C.room, COURTYARD)
        self.assertEqual(C.inventory, frozenset(("grease_pencil", "ceramic_sample_tiles", "wedge")))

    def test_ownership_handoff_exact_once_with_stale_and_repeated_ack(self):
        world = P08World(); world.place(C, "ceramic_carrier", Position.HATCH)
        h = world.pending_handoffs[0]
        world = clone(world)
        self.assertEqual(world.pending_handoffs[0], h)
        before = world.save()
        self.assertEqual(world.acknowledge_handoff(h["handoff_id"], h["serial"] + 1).code, "stale_handoff")
        self.assertEqual(world.save(), before)
        self.assertEqual(world.acknowledge_handoff(h["handoff_id"], h["serial"]).code, "handoff_acknowledged")
        before = world.save()
        self.assertFalse(world.acknowledge_handoff(h["handoff_id"], h["serial"]).events)
        self.assertEqual(world.save(), before)
        result = world.place(C, "ceramic_carrier", Position.LANE)
        self.assertFalse(any(e.kind == "ownership_handoff" for e in result.events))
        self.assertEqual(world.pending_handoffs, ())
        world.place(C, "ceramic_carrier", Position.HATCH)
        self.assertEqual(world.ownership_serials["ceramic_carrier"], h["serial"])

    def test_transition_waits_for_host_to_retire_old_ownership_projections(self):
        world = P08World()
        for obj, position in DESTINATIONS.items():
            world.place(C, obj, position)
        world.unpack_service(C)
        self.assertTrue(world.ready)
        self.assertEqual(len(world.pending_handoffs), 5)
        self.assertEqual(world.request_start(C).code, "handoff_pending")
        acknowledge_host(world)
        self.assertEqual(world.request_start(C).code, "readiness_requested")

    def test_exact_padding_returns_once_and_tiles_never_change(self):
        for cloth, line in (("clean_towel", "P08.SYSTEM.001"), ("clean_napkin", "P08.SYSTEM.002")):
            context = replace(C, carrier_padding=cloth)
            world = P08World()
            before = world.save()
            self.assertEqual(world.unpack_service(context).code, "buffet_surface_required")
            self.assertEqual(world.save(), before)
            world.place(context, "ceramic_carrier", Position.HATCH)
            self.assertEqual(world.unpack_service(context).code, "buffet_surface_required")
            world.place(context, "serving_table", Position.HATCH)
            result = world.unpack_service(context)
            self.assertIn(line, result.line_ids)
            self.assertEqual(world.returned_padding, cloth)
            self.assertEqual(world.object_location(cloth, context), KITCHEN)
            h = next(x for x in world.pending_handoffs if x["object_id"] == cloth)
            self.assertEqual(h["destination"], "linen_hook")
            self.assertNotIn("ceramic_sample_tiles", str(result.events))
            before = world.save()
            self.assertFalse(world.unpack_service(context).events)
            self.assertEqual(world.save(), before)
            self.assertEqual(clone(world, context).returned_padding, cloth)
            with self.assertRaises(ValueError):
                clone(world, replace(context, carrier_padding="clean_napkin" if cloth == "clean_towel" else "clean_towel"))

    def test_every_object_can_move_away_and_back_without_losing_rewards(self):
        world = fit()
        original_handoffs = dict(world.ownership_serials)
        for obj, correct in DESTINATIONS.items():
            for wrong in (Position.HATCH, Position.WALL, Position.ALCOVE, Position.LANE):
                if wrong == correct:
                    continue
                result = world.place(C, obj, wrong)
                self.assertFalse(world.ready)
                self.assertNotIn("LAYOUT_READY", world.flags)
                if wrong == Position.LANE:
                    self.assertIn("P08.FAILURE.001", result.line_ids)
                world = clone(world)
                world.place(C, obj, correct)
                self.assertTrue(world.ready)
                self.assertEqual(world.returned_padding, "clean_towel")
                self.assertEqual(world.ownership_serials, original_handoffs)
        backward = world.orient_pa(C, Facing.NEIGHBOR)
        self.assertFalse(world.ready)
        self.assertIn("P08.FAILURE.003", backward.line_ids)
        self.assertFalse(world.orient_pa(C, Facing.NEIGHBOR).events)
        world = clone(world); world.orient_pa(C, Facing.INWARD)
        self.assertTrue(world.ready)

    def test_spatial_feedback_and_no_invented_panel_movement(self):
        world = fit()
        self.assertIn("P08.FAILURE.002", world.place(C, "completed_screen", Position.HATCH).line_ids)
        self.assertFalse(world.conditions["hatch_visible"])
        self.assertIn("P08.FAILURE.004", world.place(C, "completed_screen", Position.WALL).line_ids)
        self.assertFalse(world.conditions["display_concealed"])
        self.assertNotIn("DISPLAY_STAGED", world.flags)
        self.assertIsNone(world.object_location("folded_display", C))
        self.assertFalse(world.act(C, Verb.PICK_UP, "folded_display").events)
        self.assertFalse(world.act(C, Verb.OPEN, "kitchen_hatch").events)

    def test_queries_do_not_record_knowledge_or_grant_layout(self):
        world = P08World(); before = world.save()
        for obj in (*LABEL_IDS, *SOURCE_BINDINGS):
            world.look(C, obj)
        world.journal_records()
        self.assertEqual(world.save(), before)
        self.assertEqual(world.journal_records(), ())
        for source in ("circulation_plan", "sightline_plan", "placement_symbols"):
            world.acknowledge_source(C, source, SOURCE_BINDINGS[source][0])
        world.hint(C, 3)
        self.assertFalse(world.ready)
        self.assertFalse(world.flags)
        self.assertEqual(len(world.journal_records()), 3)
        with self.assertRaises(ValueError):
            world.acknowledge_source(C, "sightline_plan", "P08.HINT.3")
        before = world.save()
        self.assertFalse(world.acknowledge_source(C, "sightline_plan", "P08.READ.002").events)
        self.assertEqual(world.save(), before)
        self.assertEqual(world.acknowledge_source(C, "credit_slate", "P08.READ.004").code, "credit_not_displayed")
        world.place(C, "credit_slate", Position.HATCH)
        world.acknowledge_source(C, "credit_slate", "P08.READ.004")
        self.assertIn("P08.READ.004", world.journal_records())

    def test_prior_plans_do_not_appear_before_their_actual_handoffs(self):
        no_preps = P08Context(COURTYARD)
        world = P08World()
        for obj in ("circulation_plan", "sightline_plan", "ceramic_carrier", "pa_kit", "completed_screen"):
            self.assertFalse(world.reachable(no_preps, obj))
        self.assertEqual(world.look(no_preps, "sightline_plan").code, "offscreen")
        self.assertEqual(world.look(no_preps, "gate_lane").code, "observed")

    def test_apron_no_remote_manipulation_no_private_audience_answers(self):
        world = fit(); apron = replace(C, on_apron=True); before = world.save()
        for action in (lambda: world.place(apron, "completed_screen", Position.LANE),
                       lambda: world.look(apron, "circulation_plan"),
                       lambda: world.acknowledge_source(apron, "circulation_plan", "P08.READ.001"),
                       lambda: world.request_start(apron),
                       lambda: world.act(apron, Verb.TALK_TO, "audience")):
            self.assertFalse(action().events)
        self.assertEqual(world.save(), before)
        self.assertFalse(world.flags & {"RUMOR_CLEARED", "KNOW_TERMS", "CUES_RESTORED", "ALL_VC_WON"})
        self.assertEqual(world.save(), clone(world, apron).save())

    def test_readiness_requires_frankie_and_full_checklist_ack_not_query(self):
        world = fit(); before = world.save()
        self.assertEqual(world.request_start(replace(C, frankie_room=LIVING)).code, "offscreen")
        self.assertEqual(world.save(), before)
        world.request_start(C); token = world.pending_request_id
        self.assertEqual(world.confirm_start(C, token, True).code, "stale_confirmation")
        world.pending_presentation(C)
        self.assertEqual(world.pending_phase, StartPhase.CHECKLIST)
        with self.assertRaises(ValueError):
            world.acknowledge_readiness(C, token, ("P08.DIALOGUE.002",))
        self.assertEqual(world.acknowledge_readiness(C, token, READINESS_RECORDS).code, "confirmation_pending")
        self.assertEqual(world.acknowledge_readiness(C, token, READINESS_RECORDS).code, "stale_readiness")

    def test_not_yet_cancels_without_phase_or_save_and_retries_cleanly(self):
        world = fit(); world.request_start(C); old = world.pending_request_id
        world.acknowledge_readiness(C, old, READINESS_RECORDS)
        result = world.confirm_start(C, old, False)
        self.assertEqual(result.line_ids, ("P08.SYSTEM.005",))
        self.assertFalse(world.evening_started)
        self.assertEqual(world.pending_phase, StartPhase.NONE)
        self.assertFalse(any(e.kind == "autosave_request" for e in result.events))
        world = clone(world); world.request_start(C)
        self.assertNotEqual(world.pending_request_id, old)
        self.assertEqual(world.confirm_start(C, old, True).code, "stale_confirmation")

    def test_autosave_failure_retry_restore_and_success_are_explicit_and_once(self):
        world = fit(); token, request = await_autosave(world)
        self.assertTrue(request.events[0].payload["must_complete_before_transition"])
        pending = world.save()
        self.assertEqual(world.acknowledge_autosave(C, token, False).code, "autosave_failed")
        self.assertEqual(world.save(), pending)
        world = clone(world)
        self.assertEqual(world.pending_presentation(C).code, "autosave_pending")
        self.assertEqual(world.retry_autosave(C, token).events[0].payload["request_id"], token)
        result = world.acknowledge_autosave(C, token, True)
        self.assertEqual([e.id for e in result.events], ["P08_EVENING"])
        self.assertTrue(world.evening_started)
        before = world.save()
        self.assertFalse(world.acknowledge_autosave(C, token, True).events)
        self.assertFalse(world.retry_autosave(C, token).events)
        self.assertFalse(world.request_start(C).events)
        self.assertEqual(world.save(), before)
        # Loading pre-transition state restores that timeline; no progress merge.
        old = P08World.load(pending, C)
        self.assertFalse(old.evening_started)
        self.assertEqual(old.pending_request_id, token)

    def test_interruptions_preserve_pending_and_movement_invalidates_stale_callbacks(self):
        for phase in StartPhase.CHECKLIST, StartPhase.CONFIRMATION, StartPhase.AUTOSAVE:
            world = fit(); world.request_start(C); token = world.pending_request_id
            if phase >= StartPhase.CONFIRMATION:
                world.acknowledge_readiness(C, token, READINESS_RECORDS)
            if phase == StartPhase.AUTOSAVE:
                world.confirm_start(C, token, True)
            before = world.save()
            for away in (replace(C, room=LIVING), replace(C, on_apron=True), replace(C, contest_active=True)):
                self.assertFalse(world.pending_presentation(away).events)
                self.assertEqual(world.save(), before)
                world = clone(world, away)
            self.assertEqual(world.pending_phase, phase)
            world.place(C, "completed_screen", Position.HATCH)
            world.place(C, "completed_screen", Position.ALCOVE)
            self.assertTrue(world.ready)
            self.assertEqual(world.pending_phase, StartPhase.NONE)
            self.assertEqual(world.acknowledge_autosave(C, token, True).code, "stale_autosave")
            self.assertFalse(world.evening_started)
            world.request_start(C)
            self.assertNotEqual(world.pending_request_id, token)

    def test_cancel_pending_autosave_prevents_late_transition(self):
        world = fit(); token, _ = await_autosave(world)
        self.assertEqual(world.cancel_start(replace(C, on_apron=True)).code, "start_cancelled")
        self.assertEqual(world.acknowledge_autosave(C, token, True).code, "stale_autosave")
        self.assertFalse(world.cancel_start(C).events)
        self.assertFalse(world.evening_started)

    def test_later_layout_reversal_preserves_evening_and_caller_protects_occupied_objects(self):
        world = fit(); token, _ = await_autosave(world); world.acknowledge_autosave(C, token, True)
        world.place(C, "serving_table", Position.LANE)
        self.assertTrue(world.evening_started)
        self.assertFalse(world.ready)
        self.assertTrue(clone(world).evening_started)
        world.place(C, "serving_table", Position.HATCH)
        protected = replace(C, protected_objects=frozenset(("ceramic_carrier", "serving_table", "pa_kit")))
        before = world.save()
        self.assertEqual(world.place(protected, "serving_table", Position.LANE).code, "occupied_object")
        self.assertEqual(world.orient_pa(protected, Facing.NEIGHBOR).code, "occupied_object")
        self.assertEqual(world.save(), before)

    def test_p09_cannot_start_until_real_save_ack_then_uses_caller_phase(self):
        from cakood.p09_model import P09Context, P09World, CONSERVATORY
        courtyard = fit(); token, _ = await_autosave(courtyard)
        chairs = P09World()
        context = P09Context(CONSERVATORY, flags=frozenset(C.flags | courtyard.flags))
        self.assertEqual(chairs.inspect_chairs(context).code, "evening_required")
        courtyard.acknowledge_autosave(C, token, True)
        context = replace(context, flags=frozenset(C.flags | courtyard.flags))
        presentation = chairs.inspect_chairs(context)
        self.assertFalse(chairs.rumor_cleared)
        chairs.acknowledge_presentation(context, presentation.presentation_id, record_id="P09.LOOK.001")
        self.assertTrue(chairs.rumor_cleared)
        self.assertNotIn("RUMOR_CLEARED", courtyard.flags)
        self.assertNotIn("CUES_RESTORED", chairs.flags | courtyard.flags)

    def test_nine_verb_surface_no_pickup_grants_or_implicit_start(self):
        world = P08World()
        world.act(C, Verb.USE, "ceramic_carrier", "buffet_position")
        result = world.act(C, Verb.PULL, "serving_table", "buffet_position")
        self.assertIn("P08.SUCCESS.006", result.line_ids)
        world.act(C, Verb.OPEN, "ceramic_carrier")
        world.act(C, Verb.USE, "pa_kit", "speaker_position")
        world.act(C, Verb.USE, "completed_screen", "display_alcove")
        world.act(C, Verb.USE, "credit_slate", "buffet_position")
        acknowledge_host(world)
        self.assertTrue(world.ready)
        before = world.save()
        for verb in (Verb.GIVE, Verb.CLOSE, Verb.PICK_UP):
            self.assertFalse(world.act(C, verb, "serving_table").events)
        self.assertEqual(world.save(), before)
        self.assertEqual(world.act(C, Verb.TALK_TO, "frankie").code, "readiness_requested")
        self.assertFalse(world.evening_started)

    def test_bad_contexts_inputs_and_snapshot_aliases(self):
        for change in ({"room": "L08"}, {"on_apron": 1}, {"flags": set()},
                       {"carrier_padding": "new_towel"}, {"carrier_padding": None},
                       {"inventory": frozenset(("hotpot_pot",))},
                       {"inventory": frozenset(("clean_towel",))},
                       {"protected_objects": frozenset(("hotpot_pot",))}):
            with self.assertRaises(ValueError):
                replace(C, **change)
        world = fit(); before = world.save()
        for value in (True, "1", -1, 0, 99):
            with self.assertRaises(ValueError):
                world.place(C, "serving_table", value)
        self.assertEqual(world.save(), before)
        snapshot = world.layout_handoff; snapshot["positions"]["completed_screen"] = 0
        snapshot["conditions"]["lane_clear"] = False
        self.assertTrue(world.ready)
        saved = world.save(); restored = P08World.load(saved, C)
        saved["state"]["positions"]["completed_screen"] = 0
        self.assertTrue(restored.ready)

    def test_save_validation_rejects_forged_rewards_receipts_and_malformed_envelopes(self):
        world = fit(); token, _ = await_autosave(world); world.acknowledge_autosave(C, token, True)
        base = world.save()
        mutations = [
            lambda d: d.update(schema=True),
            lambda d: d["state"].update(extra=1),
            lambda d: d["state"]["flags"].append("GAME_COMPLETE"),
            lambda d: d["state"]["flags"].append("LAYOUT_READY"),
            lambda d: d["state"]["positions"].update(completed_screen=True),
            lambda d: d["state"].update(returned_padding=None),
            lambda d: d["state"]["consumed"].pop("P08_UNPACK"),
            lambda d: d["state"]["acknowledged_handoffs"].clear(),
            lambda d: d["state"]["ownership_serials"].pop("pa_kit"),
            lambda d: d["state"].update(completed_confirmation_receipt=0),
            lambda d: d["state"].update(completed_requested_at=d["state"]["revision"]),
            lambda d: d["state"]["unpacked_surface_receipts"].update(serving_table=d["state"]["revision"]),
            lambda d: d["state"].update(completed_checklist_receipt=d["state"]["revision"]),
            lambda d: d["state"].update(pending_phase=3),
            lambda d: d["state"]["source_serials"].update(sightline_plan=1),
        ]
        for mutate in mutations:
            bad = deepcopy(base); mutate(bad)
            with self.assertRaises(ValueError):
                P08World.load(bad, C)
        with self.assertRaises(ValueError):
            P08World.load(base, replace(C, flags=PREPARATIONS - {"FOOD_READY"}))
        with self.assertRaises(ValueError):
            P08World().validate_context(replace(C, flags=PREPARATIONS | {"EVENING_STARTED"}))


if __name__ == "__main__":
    unittest.main()
