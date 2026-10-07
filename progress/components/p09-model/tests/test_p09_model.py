"""Fair P09 routes, explicit presentation receipts and the unsigned-card limit."""
from copy import deepcopy
from dataclasses import replace
from itertools import permutations
import json
from pathlib import Path
import unittest

from cakood.model import Event, Result, Verb
from cakood.p02_model import ROOMS
from cakood.p09_model import (
    CARD, CLASS_CONTEXT_UNITS, CONSERVATORY, FIXED_OBJECTS, FLAG_IDS, LABEL_IDS,
    P09Context, P09Result, P09World, RECORD_UNITS, SCRIPT_BINDINGS, SOURCE_BINDINGS,
)

FIXTURE = json.loads((Path(__file__).parent / "fixtures/p09/canonical-bindings.json").read_text())
C = P09Context(CONSERVATORY, flags=frozenset(("EVENING_STARTED", "PLAN_AGREED")),
               inventory=frozenset(("grease_pencil", "wedge", "sample_tiles")))
SIDE = replace(C, conservatory_view="side")
LIVING = "L01_LIVING_ROOM"


def clone(world, context=C):
    return P09World.load(json.loads(json.dumps(world.save())), context=context)


def acknowledge(world, result, context=C):
    if result.line_ids:
        return world.acknowledge_presentation(context, result.presentation_id, record_id=result.line_ids[0])
    return world.acknowledge_presentation(context, result.presentation_id, speech_unit_ids=result.speech_unit_ids)


def clear(world, route="direct_question", context=C):
    return acknowledge(world, world.begin_presentation(context, route), context)


def finish(world=None, route="direct_question"):
    world = world or P09World()
    clear(world, route)
    result = acknowledge(world, world.discuss_terms(C))
    acknowledge(world, result)
    return world


class P09Tests(unittest.TestCase):
    def test_canonical_bindings_and_exact_speech_units(self):
        ids = set(LABEL_IDS.values()) | {r for rs in SCRIPT_BINDINGS.values() for r in rs}
        self.assertEqual(ids, FIXTURE["records"].keys())
        self.assertEqual(FIXTURE["editorial_revision"], 3)
        self.assertEqual(FIXTURE["catalog_sha256"], "3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c")
        for record, units in RECORD_UNITS.items():
            self.assertEqual(list(units), FIXTURE["records"][record]["speech_units"])
        self.assertEqual(FIXTURE["records"]["P09.DIALOGUE.001"]["trigger"],
            "Ask what three things are leaving OR inspect tagged chairs OR walk to the conservatory front and hear complete context")
        self.assertIn("Observation itself may clear", FIXTURE["records"]["P09.LOOK.001"]["source_obligations"][0])

    def test_look_topics_journal_and_resume_queries_are_pure(self):
        world = P09World(); before = world.save()
        self.assertEqual(world.look(C, "tagged_chairs").line_ids, ("P09.LOOK.001",))
        self.assertEqual(world.look(C, "chair_tag").line_ids, ("P09.READ.001",))
        self.assertIn("P09.CHOICE.001", world.topics(C).line_ids)
        self.assertEqual(world.journal_records(), ())
        self.assertEqual(world.journal_units(), ())
        self.assertEqual(world.resume_presentation(C, "chairs").code, "presentation_not_queued")
        self.assertEqual(world.save(), before)

    def test_all_fair_routes_need_presentation_but_no_object_ritual(self):
        for route in ("chairs", "direct_question", "front_context", "accusation"):
            with self.subTest(route=route):
                world = P09World(); result = world.begin_presentation(C, route)
                self.assertIsInstance(result, Result)
                self.assertIsInstance(result.events[0], Event)
                self.assertEqual(result.text, "")
                self.assertFalse(world.flags)
                world = clone(world)
                acknowledge(world, world.resume_presentation(C, route))
                self.assertEqual(world.flags, {"RUMOR_CLEARED"})
                self.assertEqual(world.inventory, ())
                self.assertFalse(world.ready)
                self.assertNotIn("intro", world.presentations)
                self.assertNotIn("chair_tag", world.presentations)
                self.assertEqual(world.discuss_terms(C).line_ids, ("P09.DIALOGUE.002",))

    def test_complete_context_unit_alone_is_enough_and_joke_stays_pending(self):
        world = P09World(); p = world.ask_three_things(C)
        result = world.acknowledge_presentation(C, p.presentation_id,
                                               speech_unit_ids=("P09.DIALOGUE.001.01",))
        self.assertTrue(world.rumor_cleared)
        self.assertTrue(world.class_context_known)
        self.assertEqual(result.speech_unit_ids, ("P09.DIALOGUE.001.02", "P09.DIALOGUE.001.03"))
        self.assertNotIn("P09.DIALOGUE.001", world.journal_records())
        self.assertEqual(world.journal_units(), ("P09.DIALOGUE.001.01",))
        self.assertEqual(world.discuss_terms(C).code, "presentation_pending")

    def test_chair_inspection_is_independent_of_npc_presence(self):
        context = replace(C, stringer_room=LIVING, rita_room=LIVING)
        world = P09World(); clear(world, "chairs", context)
        self.assertTrue(world.rumor_cleared)
        self.assertFalse(world.class_context_known)
        self.assertEqual(world.ask_three_things(context).code, "speaker_absent")
        self.assertEqual(world.discuss_terms(context).code, "speaker_absent")
        self.assertEqual(world.connect_shared_wish(C).code, "class_context_required")

    def test_bare_tag_intro_and_hints_never_clear_the_rumor(self):
        world = P09World()
        acknowledge(world, world.introduce(SIDE), SIDE)
        acknowledge(world, world.begin_presentation(C, "chair_tag"))
        for i in (1, 2, 3):
            world.hint(C, i)
        self.assertFalse(world.flags)
        self.assertFalse(world.class_context_known)
        self.assertEqual(world.discuss_terms(C).code, "rumor_context_required")
        self.assertEqual(world.inventory, ())
        self.assertEqual(world.journal_records(), ("P09.OPEN.001", "P09.READ.001"))

    def test_natural_direct_question_works_without_tag_opening_or_intro(self):
        world = P09World()
        self.assertEqual(world.act(C, Verb.TALK_TO, "stringer").line_ids,
                         ("P09.CHOICE.001", "P09.CHOICE.002"))
        clear(world)
        self.assertEqual(set(world.presentations), {"direct_question"})
        self.assertEqual(world.introduce(SIDE).code, "rumor_already_cleared")

    def test_repeated_question_uses_a_known_exact_recap_and_no_new_events(self):
        world = P09World(); clear(world); before = world.save()
        recap = world.ask_three_things(C)
        self.assertEqual(recap.code, "rumor_recap")
        self.assertEqual(recap.speech_unit_ids, ("P09.DIALOGUE.001.01",))
        self.assertFalse(recap.events)
        self.assertEqual(world.save(), before)
        self.assertEqual(world.ask_three_things(replace(C, stringer_room=LIVING)).code, "speaker_absent")

    def test_interrupted_old_rumor_opening_is_suppressed_after_correction(self):
        world = P09World(); opening = world.introduce(SIDE)
        clear(world, "chairs")
        before = world.save()
        self.assertEqual(world.resume_presentation(SIDE, "intro").code, "rumor_already_cleared")
        self.assertEqual(acknowledge(world, opening, SIDE).code, "rumor_already_cleared")
        self.assertNotIn("intro", world.pending_presentations)
        self.assertEqual(world.save(), before)

    def test_front_context_uses_caller_owned_l07_viewpoint(self):
        world = P09World(); before = world.save()
        self.assertEqual(world.hear_front_context(SIDE).code, "front_view_required")
        self.assertEqual(world.save(), before)
        result = world.hear_front_context(C)
        self.assertEqual(result.line_ids, ("P09.DIALOGUE.001",))
        before = world.save()
        self.assertEqual(world.acknowledge_presentation(SIDE, result.presentation_id,
            record_id="P09.DIALOGUE.001").code, "front_view_required")
        self.assertEqual(world.save(), before)
        acknowledge(world, result)
        self.assertTrue(world.rumor_cleared)
        self.assertEqual(set(ROOMS), {"L01_LIVING_ROOM", "L02_KITCHEN", "L03_PORCH", "L04_SIDE_PASSAGE",
                                     "L05_COURTYARD", "L06_GARAGE", "L07_CONSERVATORY"})

    def test_accusation_corrects_immediately_without_persuasion_penalty(self):
        world = P09World(); clear(world, "accusation")
        self.assertTrue(world.rumor_cleared)
        self.assertTrue(world.class_context_known)
        self.assertEqual(world.discuss_terms(C).line_ids, ("P09.DIALOGUE.002",))
        self.assertFalse(any("penalty" in key or "persuasion" in key for key in world.save()["state"]))

    def test_absent_rita_uses_only_stringers_exact_correction(self):
        context = replace(C, rita_room=LIVING)
        world = P09World(); p = world.accuse(context)
        self.assertEqual(p.line_ids, ())
        self.assertEqual(p.speech_unit_ids, ("P09.FAILURE.001.01",))
        with self.assertRaises(ValueError):
            world.acknowledge_presentation(context, p.presentation_id, record_id="P09.FAILURE.001")
        acknowledge(world, p, context)
        self.assertTrue(world.rumor_cleared)
        self.assertFalse(world.class_context_known)
        self.assertNotIn("P09.FAILURE.001", world.journal_records())
        self.assertNotIn("P09.FAILURE.001.02", world.journal_units())
        self.assertEqual(clone(world).accuse(C).code, "presentation_complete")
        clear(world)
        self.assertTrue(world.class_context_known)

    def test_presentations_recheck_npc_locations_before_acknowledgment(self):
        world = P09World(); p = world.accuse(C); before = world.save()
        departed = replace(C, rita_room=LIVING)
        self.assertEqual(world.acknowledge_presentation(departed, p.presentation_id,
            record_id="P09.FAILURE.001").code, "speaker_absent")
        self.assertEqual(world.save(), before)
        world.acknowledge_presentation(departed, p.presentation_id, speech_unit_ids=("P09.FAILURE.001.01",))
        self.assertTrue(world.rumor_cleared)
        self.assertFalse(world.class_context_known)
        before = world.save()
        self.assertEqual(world.resume_presentation(departed, "accusation").code, "speaker_absent")
        self.assertEqual(world.save(), before)
        acknowledge(world, world.resume_presentation(C, "accusation"))
        self.assertTrue(world.class_context_known)

    def test_terms_need_agreed_plan_but_not_physical_paper_or_optional_scene(self):
        world = P09World(); clear(world, "chairs")
        no_plan = replace(C, flags=frozenset(("EVENING_STARTED",)))
        before = world.save()
        self.assertEqual(world.discuss_terms(no_plan).code, "plan_required")
        self.assertEqual(world.save(), before)
        empty_pockets = replace(C, inventory=frozenset())
        result = acknowledge(world, world.discuss_terms(empty_pockets), empty_pockets)
        self.assertTrue(world.ready)
        self.assertNotIn("shared_wish", world.presentations)
        self.assertEqual(world.inventory, (CARD,))
        self.assertEqual(result.line_ids, ("P09.SUCCESS.001",))

    def test_full_terms_are_required_before_granting_unsigned_card(self):
        world = P09World(); clear(world); p = world.discuss_terms(C)
        for unit in RECORD_UNITS["P09.DIALOGUE.002"][:-1]:
            world.acknowledge_presentation(C, p.presentation_id, speech_unit_ids=(unit,))
            self.assertFalse(world.ready)
            self.assertEqual(world.inventory, ())
            world = clone(world)
        result = world.acknowledge_presentation(C, p.presentation_id, speech_unit_ids=("P09.DIALOGUE.002.05",))
        grant = [e for e in result.events if e.id == "P09_TERMS"]
        self.assertEqual(len(grant), 1)
        self.assertEqual(grant[0].payload["object_id"], CARD)
        self.assertFalse(grant[0].payload["signed"])
        self.assertIsNone(grant[0].payload["repair_date"])
        self.assertEqual(grant[0].payload["signature_owner"], "P14")
        self.assertEqual(world.flags, FLAG_IDS)
        self.assertNotIn("COMMITMENTS_SIGNED", world.flags)
        self.assertNotIn("GAME_COMPLETE", world.flags)

    def test_card_grant_survives_interrupted_success_caption_without_regrant(self):
        world = P09World(); clear(world)
        result = acknowledge(world, world.discuss_terms(C))
        self.assertEqual(world.pending_presentations, ("terms",))
        saved = world.save(); world = clone(world)
        elsewhere = replace(C, room=LIVING, stringer_room=LIVING)
        result = world.resume_presentation(elsewhere, "terms")
        self.assertEqual(result.line_ids, ("P09.SUCCESS.001",))
        self.assertEqual(world.save(), saved)
        result = acknowledge(world, result, elsewhere)
        self.assertFalse(any(e.id == "P09_TERMS" for e in result.events))
        self.assertEqual(world.pending_presentations, ())
        self.assertEqual(world.inventory, (CARD,))
        self.assertEqual(world.discuss_terms(C).code, "presentation_complete")

    def test_duplicate_receipts_and_resume_do_not_replay_rewards(self):
        world = P09World(); p = world.ask_three_things(C)
        acknowledge(world, p); before = world.save()
        for _ in range(3):
            self.assertFalse(acknowledge(world, p).events)
            self.assertEqual(world.resume_presentation(C, "direct_question").code, "presentation_complete")
            self.assertEqual(world.save(), before)
        t = world.discuss_terms(C); outcome = acknowledge(world, t)
        before = world.save()
        self.assertFalse(acknowledge(world, t).events)
        self.assertEqual(world.save(), before)
        acknowledge(world, outcome)
        self.assertFalse(acknowledge(world, outcome).events)

    def test_requeue_same_pending_source_preserves_identity(self):
        world = P09World(); p = world.ask_three_things(C); before = world.save()
        for _ in range(3):
            replay = world.ask_three_things(C)
            self.assertEqual(replay.presentation_id, p.presentation_id)
            self.assertFalse(replay.events)
            self.assertEqual(world.save(), before)

    def test_optional_shared_wish_requires_known_class_context_and_actual_participants(self):
        world = P09World(); clear(world, "chairs")
        self.assertEqual(world.connect_shared_wish(C).code, "class_context_required")
        clear(world)
        for absent in (replace(C, rita_room=LIVING), replace(C, stringer_room=LIVING)):
            self.assertEqual(world.connect_shared_wish(absent).code, "speaker_absent")
        result = acknowledge(world, world.connect_shared_wish(C))
        self.assertEqual(world.flags, {"RUMOR_CLEARED"})
        self.assertEqual([e.id for e in result.events], ["P09_PRESENTED", "P09_SHARED_WISH"])
        self.assertTrue(result.events[-1].payload["optional"])
        self.assertFalse(world.connect_shared_wish(C).events)

    def test_optional_wish_before_or_after_terms_does_not_change_rewards(self):
        for order in permutations(("terms", "shared_wish")):
            world = P09World(); clear(world)
            for source in order:
                result = acknowledge(world, world.begin_presentation(C, source))
                if source == "terms":
                    acknowledge(world, result)
                world = clone(world)
            self.assertEqual(world.flags, FLAG_IDS)
            self.assertEqual(world.inventory, (CARD,))

    def test_both_new_chair_sources_and_success_outcome_survive_interleaving(self):
        world = P09World()
        pending = {source: world.begin_presentation(C, source) for source in ("chairs", "direct_question", "front_context")}
        clear_result = acknowledge(world, pending["chairs"])
        self.assertEqual(len([e for e in clear_result.events if e.id == "P09_RUMOR"]), 1)
        outcome = acknowledge(world, world.discuss_terms(C))
        world = clone(world)
        for source in ("front_context", "direct_question"):
            result = acknowledge(world, world.resume_presentation(C, source))
            self.assertFalse(any(e.id == "P09_RUMOR" for e in result.events))
        acknowledge(world, outcome)
        self.assertEqual(world.flags, FLAG_IDS)
        self.assertEqual(world.pending_presentations, ())

    def test_all_rumor_route_orders_preserve_exactly_one_reward_and_available_terms(self):
        for order in permutations(("chairs", "direct_question", "front_context", "accusation")):
            world = P09World(); events = []
            for source in order:
                events.extend(clear(world, source).events)
                world = clone(world)
            self.assertEqual(sum(e.id == "P09_RUMOR" for e in events), 1)
            self.assertEqual(world.flags, {"RUMOR_CLEARED"})
            acknowledge(world, world.discuss_terms(C))
            self.assertEqual(world.flags, FLAG_IDS)

    def test_card_read_has_its_own_presentation_receipt(self):
        world = finish(); before = world.save()
        result = world.look(C, CARD)
        self.assertEqual(result.line_ids, ("P09.LOOK.002", "P09.READ.002"))
        self.assertEqual(world.save(), before)
        self.assertNotIn("P09.READ.002", world.journal_records())
        result = world.act(replace(C, room=LIVING), Verb.OPEN, CARD)
        acknowledge(world, result, replace(C, room=LIVING))
        self.assertIn("P09.READ.002", world.journal_records())
        self.assertFalse(world.terms_card_handoff["signed"])

    def test_card_cannot_be_consumed_forged_signed_or_used_as_craft(self):
        world = finish(); before = world.save()
        for verb, obj, target in ((Verb.USE, "grease_pencil", CARD), (Verb.GIVE, CARD, "stringer"),
                                  (Verb.PICK_UP, CARD, None), (Verb.USE, CARD, "sample_tiles")):
            result = world.act(C, verb, obj, target)
            self.assertEqual(result.code, "unsigned_card_reserved_for_p14")
            self.assertEqual(world.save(), before)

    def test_refused_tag_destruction_preserves_state_and_external_inventory(self):
        world = P09World(); before = world.save()
        result = world.refuse_tag_destruction(C)
        self.assertEqual(result.line_ids, ("P09.FAILURE.002",))
        self.assertEqual(world.act(C, Verb.PICK_UP, "chair_tag").code, "tag_preserved")
        self.assertEqual(world.save(), before)
        self.assertEqual(C.inventory, frozenset(("grease_pencil", "wedge", "sample_tiles")))

    def test_audience_has_no_rumor_or_private_class_context_answers(self):
        world = P09World(); before = world.save()
        for room in ROOMS:
            for apron in (False, True):
                context = replace(C, room=room, on_apron=apron)
                for query in (lambda: world.look(context, "audience"),
                              lambda: world.act(context, Verb.TALK_TO, "audience")):
                    result = query()
                    self.assertEqual(result.code, "audience_has_no_p09_information")
                    self.assertFalse(result.line_ids or result.speech_unit_ids or result.events)
                    self.assertEqual(world.save(), before)
        with self.assertRaises(ValueError):
            world.begin_presentation(replace(C, on_apron=True), "audience")

    def test_all_routes_reject_offscreen_apron_pre_evening_and_contest(self):
        for context, code in ((replace(C, room=LIVING), "offscreen"),
                              (replace(C, on_apron=True), "offscreen"),
                              (replace(C, flags=frozenset()), "evening_required"),
                              (replace(C, contest_active=True), "contest_active")):
            for route in ("chairs", "direct_question", "front_context", "accusation"):
                world = P09World(); before = world.save()
                self.assertEqual(world.begin_presentation(context, route).code, code)
                self.assertEqual(world.save(), before)
        world = P09World(); p = world.ask_three_things(C); before = world.save()
        self.assertEqual(world.acknowledge_presentation(replace(C, on_apron=True), p.presentation_id,
            record_id="P09.DIALOGUE.001").code, "offscreen")
        self.assertEqual(world.save(), before)

    def test_acknowledgment_rejects_wrong_out_of_order_and_fabricated_canonical_data(self):
        world = P09World(); p = world.ask_three_things(C)
        attempts = (
            {"record_id": "P09.READ.001"}, {"record_id": "P09.CHOICE.001"},
            {"record_id": "P09.HINT.3"}, {"record_id": "P14.SUCCESS.001"},
            {"speech_unit_ids": ("P09.DIALOGUE.001.02",)},
            {"speech_unit_ids": ("P09.DIALOGUE.001.01", "P09.DIALOGUE.001.03")},
            {"speech_unit_ids": ("P09.DIALOGUE.001.01", "P09.DIALOGUE.001.01")},
            {"speech_unit_ids": ("P09.READ.001",)}, {"speech_unit_ids": ["P09.DIALOGUE.001.01"]},
            {"record_id": "P09.DIALOGUE.001", "speech_unit_ids": ("P09.DIALOGUE.001.01",)}, {},
        )
        for kwargs in attempts:
            before = world.save()
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                world.acknowledge_presentation(C, p.presentation_id, **kwargs)
            self.assertEqual(world.save(), before)
        for id in ("P09:direct_question:999", "P08:direct_question:1", "", True):
            with self.assertRaises(ValueError):
                world.acknowledge_presentation(C, id, record_id="P09.DIALOGUE.001")

    def test_success_cannot_be_acknowledged_before_terms(self):
        world = P09World(); clear(world); p = world.discuss_terms(C); before = world.save()
        with self.assertRaises(ValueError):
            world.acknowledge_presentation(C, p.presentation_id, record_id="P09.SUCCESS.001")
        with self.assertRaises(ValueError):
            world.acknowledge_presentation(C, p.presentation_id,
                speech_unit_ids=RECORD_UNITS["P09.DIALOGUE.002"] + RECORD_UNITS["P09.SUCCESS.001"])
        self.assertEqual(world.save(), before)

    def test_every_partial_terms_prefix_survives_json_save_and_revisit(self):
        for split in range(6):
            world = P09World(); clear(world); p = world.discuss_terms(C)
            if split:
                world.acknowledge_presentation(C, p.presentation_id,
                    speech_unit_ids=RECORD_UNITS["P09.DIALOGUE.002"][:split])
            world = clone(world)
            result = world.resume_presentation(C, "terms")
            if split < 5:
                acknowledge(world, result)
                result = world.resume_presentation(C, "terms")
            self.assertTrue(world.ready)
            acknowledge(world, result)
            self.assertEqual(clone(world).flags, FLAG_IDS)

    def test_full_record_can_finish_a_partial_caption_without_duplicate_knowledge(self):
        world = P09World(); p = world.ask_three_things(C)
        world.acknowledge_presentation(C, p.presentation_id, speech_unit_ids=("P09.DIALOGUE.001.01",))
        result = world.acknowledge_presentation(C, p.presentation_id, record_id="P09.DIALOGUE.001")
        self.assertFalse(any(e.id == "P09_RUMOR" for e in result.events))
        self.assertEqual(world.journal_records(), ("P09.DIALOGUE.001",))

    def test_invalid_context_and_choice_types_fail_explicitly(self):
        for kwargs in ({"room": "L08_AUDIENCE"}, {"room": True}, {"on_apron": 1},
                       {"contest_active": 0}, {"conservatory_view": "hidden"},
                       {"flags": {"EVENING_STARTED"}}, {"inventory": frozenset((CARD,))},
                       {"inventory": frozenset(("stringer",))}, {"rita_room": "missing"}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                replace(C, **kwargs)
        world = P09World()
        for source in (False, "audience", "signature", "future_renewal"):
            with self.assertRaises(ValueError):
                world.begin_presentation(C, source)
        for level in (True, False, 0, 4, "3", 1.0):
            with self.assertRaises(ValueError):
                world.hint(C, level)
        with self.assertRaises(ValueError):
            world.look({}, "chair_tag")

    def test_loader_rejects_wrong_schema_unknown_fields_bool_serials_and_missing_receipts(self):
        base = finish().save()
        changes = [
            lambda d: d.update(schema=True), lambda d: d.update(kind="cakood-p08-branch"),
            lambda d: d["state"].update(future_ending=True),
            lambda d: d["state"].update(revision=True),
            lambda d: d["state"].update(hint_level=True),
            lambda d: d["state"]["flags"].append("GAME_COMPLETE"),
            lambda d: d["state"]["flags"].append("RUMOR_CLEARED"),
            lambda d: d["state"]["flags"].remove("TERMS_CARD_AVAILABLE"),
            lambda d: d["state"]["consumed"].update(P09_TERMS=1),
            lambda d: d["state"]["consumed"].update(P14_COMPLETE=5),
            lambda d: d["state"]["presentations"]["terms"].update(serial=True),
            lambda d: d["state"]["presentations"]["terms"].update(variant="signed"),
            lambda d: d["state"]["presentations"]["terms"]["receipts"].pop("P09.DIALOGUE.002.02"),
            lambda d: d["state"]["presentations"]["terms"]["receipts"].update({"P09.DIALOGUE.002.01": True}),
            lambda d: d["state"]["presentations"]["terms"]["receipts"].update({"P14.SIGNATURE": 5}),
            lambda d: d["state"]["presentations"]["terms"].update(forged_field="ignored"),
            lambda d: d["state"].update(presentations={}),
        ]
        for change in changes:
            data = deepcopy(base); change(data)
            with self.subTest(data=data), self.assertRaises(ValueError):
                P09World.load(data)

    def test_loader_checks_causal_order_and_caller_handoff(self):
        world = finish(); base = world.save()
        data = deepcopy(base); data["state"]["presentations"]["terms"]["serial"] = 1
        with self.assertRaises(ValueError):
            P09World.load(data)
        data = deepcopy(base); receipts = data["state"]["presentations"]["terms"]["receipts"]
        receipts["P09.SUCCESS.001.01"] = receipts["P09.DIALOGUE.002.05"]
        with self.assertRaises(ValueError):
            P09World.load(data)
        for context in (replace(C, flags=frozenset()), replace(C, flags=frozenset(("EVENING_STARTED",)))):
            with self.assertRaises(ValueError):
                P09World.load(base, context=context)
        with self.assertRaises(ValueError):
            P09World.load(P09World().save(), context=replace(C, flags=C.flags | FLAG_IDS))
        self.assertEqual(P09World.load(base, context=replace(C, room=LIVING, on_apron=True)).save(), base)

    def test_loader_rejects_fabricated_reader_or_shared_wish_without_prior_context(self):
        for source, record in (("terms_card", "P09.READ.002"), ("shared_wish", "P09.DIALOGUE.003.01")):
            data = P09World().save()
            data["state"]["revision"] = 2
            data["state"]["presentations"][source] = {"serial": 1, "variant": "full", "receipts": {record: 2}}
            with self.assertRaises(ValueError):
                P09World.load(data)

    def test_load_and_returned_handoff_do_not_share_mutable_save_state(self):
        world = finish(); data = world.save(); restored = P09World.load(data)
        data["state"]["presentations"]["terms"]["receipts"].clear()
        data["state"]["consumed"].clear()
        self.assertEqual(restored.flags, FLAG_IDS)
        restored.validate()
        handoff = restored.terms_card_handoff; handoff["signed"] = True
        self.assertFalse(restored.terms_card_handoff["signed"])


if __name__ == "__main__":
    unittest.main()
