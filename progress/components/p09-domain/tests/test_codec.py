"""Tests of the newly reconstructed finite codec against the unchanged model."""
from copy import deepcopy
from dataclasses import replace
from itertools import permutations
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from codec.p09_codec import (
    ALL_PROPERTIES, CONTEXT_PROPERTIES, INVENTORY_CAPACITY, MANIFEST, MAX_SERIAL,
    PERSISTED_PROPERTIES, SERIAL_BASE, CodecError, ContextImage, EventImage, ResultImage,
    decode_context, decode_event, decode_result, decode_world,
    encode_context, encode_event, encode_result, encode_world, join_serial,
    select_persisted, split_serial,
)
from reference.cakood.p09_model import (
    CARD, CONSERVATORY, P09Context, P09Result, P09World, Presentation, RECORD_UNITS,
)
from reference.cakood.model import Event

C = P09Context(CONSERVATORY, flags=frozenset(("EVENING_STARTED", "PLAN_AGREED")))
SIDE = replace(C, conservatory_view="side")
LIVING = "L01_LIVING_ROOM"
OBJECTS = {"wedge": 4, "grease_pencil": 25, "new_current_object": 150,
           "stringer": 29, CARD: 399}


def acknowledge(world, result, context=C):
    if result.line_ids:
        return world.acknowledge_presentation(context, result.presentation_id, record_id=result.line_ids[0])
    return world.acknowledge_presentation(context, result.presentation_id, speech_unit_ids=result.speech_unit_ids)


def set_serial(properties, name, value):
    properties["p09" + name + "Hi"], properties["p09" + name + "Lo"] = split_serial(value)


def finished():
    world = P09World()
    acknowledge(world, world.ask_three_things(C))
    success = acknowledge(world, world.discuss_terms(C))
    acknowledge(world, success)
    return world


class WorldCodecTests(unittest.TestCase):
    def roundtrip(self, world, context=C):
        before = deepcopy(world.save())
        properties = encode_world(world, context=context)
        self.assertEqual(tuple(properties), PERSISTED_PROPERTIES)
        self.assertEqual(len(properties), 77)
        self.assertTrue(all(type(value) is int and 0 <= value < SERIAL_BASE for value in properties.values()))
        restored = decode_world(properties, context=context)
        self.assertEqual(restored.save(), before)
        self.assertEqual(encode_world(restored), properties)
        self.assertEqual(world.save(), before)
        self.assertEqual(restored.journal_records(), world.journal_records())
        self.assertEqual(restored.journal_units(), world.journal_units())
        self.assertEqual(restored.pending_presentations, world.pending_presentations)
        return restored

    def test_all_rumor_route_orders_roundtrip_after_every_commit(self):
        for order in permutations(("chairs", "direct_question", "front_context", "accusation")):
            with self.subTest(order=order):
                world = self.roundtrip(P09World())
                for source in order:
                    queued = world.begin_presentation(C, source)
                    world = self.roundtrip(world)
                    acknowledge(world, queued)
                    world = self.roundtrip(world)
                success = acknowledge(world, world.discuss_terms(C))
                world = self.roundtrip(world)
                self.assertTrue(world.ready)
                self.assertIn("terms", world.pending_presentations)
                acknowledge(world, success)
                self.roundtrip(world)

    def test_interleaved_pending_sources_and_earliest_rumor_receipt(self):
        world = P09World()
        queued = {source: world.begin_presentation(C, source)
                  for source in ("direct_question", "chairs", "front_context")}
        acknowledge(world, queued["chairs"])
        earliest = world.consumed["P09_RUMOR"]
        for source in ("front_context", "direct_question"):
            acknowledge(world, queued[source])
            world = self.roundtrip(world)
            self.assertEqual(world.consumed["P09_RUMOR"], earliest)
        bad = encode_world(world)
        set_serial(bad, "Rumor", world.presentations["direct_question"].receipts["P09.DIALOGUE.001.01"])
        with self.assertRaisesRegex(CodecError, "rumor receipt chronology"):
            decode_world(bad)

    def test_every_partial_terms_prefix_and_card_reader(self):
        for count in range(6):
            world = P09World()
            acknowledge(world, world.inspect_chairs(C))
            queued = world.discuss_terms(C)
            if count:
                world.acknowledge_presentation(C, queued.presentation_id,
                    speech_unit_ids=RECORD_UNITS["P09.DIALOGUE.002"][:count])
            world = self.roundtrip(world)
            self.assertEqual(world.ready, count == 5)
            if count < 5:
                acknowledge(world, world.resume_presentation(C, "terms"))
            world = self.roundtrip(world)
            self.assertEqual(world.terms_card_handoff, MANIFEST["card_handoff"])
            self.assertFalse(world.terms_card_handoff["signed"])
            self.assertIsNone(world.terms_card_handoff["repair_date"])
            handoff = world.terms_card_handoff
            handoff["signed"] = True
            self.assertFalse(world.terms_card_handoff["signed"])
            elsewhere = replace(C, room=LIVING)
            acknowledge(world, world.resume_presentation(elsewhere, "terms"), elsewhere)
            reader = world.begin_presentation(elsewhere, "terms_card")
            world = self.roundtrip(world, elsewhere)
            acknowledge(world, reader, elsewhere)
            self.roundtrip(world, elsewhere)

    def test_partial_full_accusation_preserves_rita_receipt_boundary(self):
        world = P09World()
        queued = world.accuse(C)
        absent = replace(C, rita_room=LIVING)
        world.acknowledge_presentation(absent, queued.presentation_id,
                                      speech_unit_ids=("P09.FAILURE.001.01",))
        world = self.roundtrip(world, absent)
        self.assertEqual(encode_world(world)["p09Restricted"], 0)
        self.assertFalse(world.class_context_known)
        self.assertEqual(world.resume_presentation(absent, "accusation").code, "speaker_absent")
        self.assertEqual(world.resume_presentation(C, "accusation").speech_unit_ids,
                         ("P09.FAILURE.001.02",))
        acknowledge(world, world.resume_presentation(C, "accusation"))
        world = self.roundtrip(world)
        self.assertTrue(world.class_context_known)

    def test_restricted_accusation_is_not_full_record_or_class_context(self):
        absent = replace(C, rita_room=LIVING)
        world = P09World()
        result = world.accuse(absent)
        world = self.roundtrip(world, absent)
        self.assertEqual(encode_world(world)["p09Restricted"], 1)
        acknowledge(world, result, absent)
        world = self.roundtrip(world, absent)
        self.assertTrue(world.rumor_cleared)
        self.assertFalse(world.class_context_known)
        self.assertNotIn("P09.FAILURE.001", world.journal_records())
        self.assertEqual(world.accuse(C).code, "presentation_complete")
        bad = encode_world(world)
        set_serial(bad, "AccusationReceipt2", world.revision)
        with self.assertRaises(CodecError):
            decode_world(bad)

    def test_intro_suppression_shared_wish_hints_and_tag_receipts(self):
        world = P09World()
        world.introduce(SIDE)
        self.roundtrip(world)
        acknowledge(world, world.begin_presentation(C, "chair_tag"))
        world.hint(C, 2)
        acknowledge(world, world.ask_three_things(C))
        self.assertNotIn("intro", world.pending_presentations)
        shared = world.connect_shared_wish(C)
        for unit in RECORD_UNITS["P09.DIALOGUE.003"]:
            world.acknowledge_presentation(C, shared.presentation_id, speech_unit_ids=(unit,))
            world = self.roundtrip(world)
        self.assertIn("P09_SHARED_WISH", world.consumed)
        self.assertEqual(world.flags, {"RUMOR_CLEARED"})

    def test_serial_boundaries_and_overflow_are_explicit(self):
        for value in (0, 1, 32767, 32768, 32769, MAX_SERIAL - 1, MAX_SERIAL):
            self.assertEqual(join_serial(*split_serial(value)), value)
            self.roundtrip(P09World(revision=value))
        for invalid in (True, False, -1, MAX_SERIAL + 1, 1.0, "1", None):
            with self.subTest(value=invalid), self.assertRaises(CodecError):
                split_serial(invalid)
        for high, low in ((True, 0), (0, False), (-1, 0), (0, -1), (32768, 0), (0, 32768)):
            with self.subTest(high=high, low=low), self.assertRaises(CodecError):
                join_serial(high, low)
        world = P09World(revision=MAX_SERIAL + 1)
        world.validate()  # The model is unbounded; this codec explicitly is not.
        with self.assertRaises(CodecError):
            encode_world(world)

    def test_large_serial_trace_crosses_limb_boundary_without_changing_causality(self):
        world = finished()
        offset = MAX_SERIAL - world.revision
        world.revision += offset
        for presentation in world.presentations.values():
            presentation.serial += offset
            presentation.receipts = {token: stamp + offset for token, stamp in presentation.receipts.items()}
        world.consumed = {event: stamp + offset for event, stamp in world.consumed.items()}
        self.roundtrip(world)

    def test_invalid_property_shapes_types_and_uninitialized_images(self):
        original = encode_world(P09World())
        invalids = [dict(original, extra=0), {key: value for key, value in original.items() if key != "p09Ready"}]
        for field, value in (("p09Initialized", 0), ("p09Initialized", True), ("p09Ready", 2),
                             ("p09HintLevel", 4), ("p09RevisionLo", -1), ("p09RevisionHi", 32768),
                             ("p09RevisionLo", 0.0), ("p09Restricted", 1), ("p09RumorCleared", 1)):
            invalids.append(dict(original, **{field: value}))
        for bad in invalids:
            with self.subTest(image=bad), self.assertRaises(CodecError):
                decode_world(bad)

    def test_invalid_causal_serials_flags_holes_and_collisions(self):
        original = encode_world(finished())
        changes = (
            (("TermsStart", 1),),                         # colliding starts/terms before rumor
            (("TermsReceipt2", 0),),                      # receipt hole
            (("TermsReceipt6", 4),),                      # outcome equals card grant
            (("Terms", 2),),                              # mismatched card one-shot
            (("DirectQuestionStart", 0),),                # receipts without start
            (("ChairTagReceipt1", 2),),                   # fabricated receipt without start
            (("ChairTagStart", 1),),                      # duplicate presentation start
            (("ChairTagStart", 3), ("ChairTagReceipt1", 4)), # cross-source receipt collision
            (("Revision", 3),),                          # future receipts
            (("SharedWishStart", 1),),                    # class context comes later
            (("TermsCardStart", 3),),                     # reader predates grant
        )
        for edits in changes:
            bad = dict(original)
            for name, serial in edits:
                set_serial(bad, name, serial)
            with self.subTest(edits=edits), self.assertRaises(CodecError):
                decode_world(bad)
        for field in ("p09Ready", "p09RumorCleared"):
            bad = dict(original, **{field: 0})
            with self.assertRaises(CodecError):
                decode_world(bad)

    def test_campaign_context_validation_and_independent_ownership(self):
        world = finished()
        raw = encode_world(world)
        for context in (replace(C, flags=frozenset()), replace(C, flags=frozenset(("EVENING_STARTED",)))):
            with self.assertRaises(CodecError):
                decode_world(raw, context=context)
        with self.assertRaises(CodecError):
            decode_world(encode_world(P09World()), context=replace(C, flags=C.flags | {"RUMOR_CLEARED"}))
        restored = decode_world(raw)
        raw["p09Ready"] = 0
        self.assertTrue(restored.ready)
        restored.presentations["terms"].receipts.clear()
        self.assertTrue(world.ready)
        self.assertTrue(world.presentations["terms"].receipts)

    def test_full_runtime_selection_is_explicit(self):
        raw = dict(MANIFEST["all_properties"])
        raw.update(encode_world(P09World()))
        self.assertEqual(len(raw), 98)
        self.assertEqual(decode_world(select_persisted(raw)).save(), P09World().save())
        with self.assertRaises(CodecError):
            decode_world(raw)
        raw["unknown"] = 0
        with self.assertRaises(CodecError):
            select_persisted(raw)


class ContextCodecTests(unittest.TestCase):
    def test_exact_context_roundtrip_and_method_argument_order(self):
        context = replace(C, room=LIVING, on_apron=True, rita_room=LIVING,
                          conservatory_view="side", contest_active=True,
                          flags=C.flags | {"RUMOR_CLEARED", "TERMS_CARD_AVAILABLE"},
                          inventory=frozenset(("wedge", "new_current_object")))
        image = encode_context(context, epoch=7, object_ids=OBJECTS)
        self.assertEqual(set(image.properties), set(CONTEXT_PROPERTIES))
        self.assertEqual(image.arguments, (1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 7))
        self.assertEqual(len(image.held), 400)
        self.assertEqual(image.held[150], 1)
        self.assertEqual(decode_context(image, object_ids=OBJECTS), context)

    def test_foreign_context_facts_are_explicitly_unrepresentable(self):
        for context in (replace(C, flags=C.flags | {"FOREIGN_FLAG"}),
                        replace(C, inventory=frozenset(("sample_tiles",)))):
            with self.assertRaises(CodecError):
                encode_context(context, object_ids=OBJECTS)
        for epoch in (0, -1, True, SERIAL_BASE):
            with self.assertRaises(CodecError):
                encode_context(C, epoch=epoch, object_ids=OBJECTS)

    def test_decode_rejects_unknown_ids_fixed_objects_and_branch_owned_card(self):
        image = encode_context(C, object_ids=OBJECTS)
        for index in (0, 151, OBJECTS["stringer"], OBJECTS[CARD]):
            held = list(image.held)
            held[index] = 1
            with self.subTest(index=index), self.assertRaises(CodecError):
                decode_context(ContextImage(dict(image.properties), tuple(held)), object_ids=OBJECTS)
        for name, value in (("p09Room", 7), ("p09View", 2), ("p09ContextValid", 0),
                             ("p09ContestActive", True), ("p09Epoch", 0)):
            with self.subTest(name=name), self.assertRaises(CodecError):
                decode_context(ContextImage(dict(image.properties, **{name: value}), image.held), object_ids=OBJECTS)


class ResultCodecTests(unittest.TestCase):
    def check_result(self, result, world):
        image = encode_result(result, revision=world.revision)
        self.assertEqual(decode_result(image), result)
        self.assertEqual(encode_result(decode_result(image), revision=world.revision), image)
        self.assertEqual((len(image.lines), len(image.units), len(image.events), len(image.event_args)), (8, 6, 3, 9))
        for event in result.events:
            self.assertEqual(decode_event(encode_event(event)), event)
        return image

    def test_real_results_cover_all_six_event_types_and_multiple_receipts(self):
        world = P09World()
        seen = set()
        results = [world.hint(C, 2)]
        for result in results:
            self.check_result(result, world)
            seen.update(event.id for event in result.events)
        for source in ("intro", "chair_tag", "chairs", "direct_question", "front_context", "accusation", "terms", "shared_wish", "terms_card"):
            context = SIDE if source == "intro" else C
            result = world.begin_presentation(context, source)
            self.check_result(result, world)
            seen.update(event.id for event in result.events)
            while result.presentation_id:
                result = acknowledge(world, result, context)
                self.check_result(result, world)
                seen.update(event.id for event in result.events)
        self.assertEqual(seen, set(MANIFEST["events"]))
        for result in (world.topics(C), world.look(C, CARD), world.ask_three_things(C),
                       world.refuse_tag_destruction(C), world.hint(C), world.look(C, "audience")):
            self.check_result(result, world)

    def test_presented_arguments_use_inclusive_source_indices(self):
        world = P09World()
        result = world.ask_three_things(C)
        self.check_result(result, world)
        world.acknowledge_presentation(C, result.presentation_id,
                                      speech_unit_ids=("P09.DIALOGUE.001.01",))
        result = world.acknowledge_presentation(C, result.presentation_id,
                                               record_id="P09.DIALOGUE.001")
        image = self.check_result(result, world)
        self.assertEqual(image.event_args[:3], (4, 1, 2))
        terms = world.discuss_terms(C)
        result = acknowledge(world, terms)
        image = self.check_result(result, world)
        self.assertEqual(image.event_args[:6], (7, 0, 4, 399, 0, 0))
        result = acknowledge(world, result)
        self.assertEqual(self.check_result(result, world).event_args[:3], (7, 5, 5))

    def test_partial_restricted_accusation_result(self):
        world = P09World()
        absent = replace(C, rita_room=LIVING)
        result = world.accuse(absent)
        image = self.check_result(result, world)
        self.assertEqual(image.lines, (0,) * 8)
        self.assertEqual(image.units[0], MANIFEST["speech_unit_ids"]["P09.FAILURE.001.01"])
        result = acknowledge(world, result, absent)
        self.assertEqual(self.check_result(result, world).event_args[:6], (6, 0, 0, 6, 0, 0))

    def test_event_payloads_cannot_gain_signed_card_or_drop_foreign_data(self):
        world = P09World()
        acknowledge(world, world.inspect_chairs(C))
        result = acknowledge(world, world.discuss_terms(C))
        card_event = result.events[1]
        for key, value in (("signed", True), ("signed", 0), ("repair_date", "tomorrow"),
                           ("signature_owner", "P09"), ("extra", 1), ("serial", True)):
            bad = replace(card_event, payload=dict(card_event.payload, **{key: value}))
            with self.subTest(key=key, value=value), self.assertRaises(CodecError):
                encode_event(bad)
        presented = result.events[0]
        with self.assertRaises(CodecError):
            encode_event(replace(presented, payload=dict(presented.payload, canonical_tokens=list(presented.payload["canonical_tokens"]))))
        for image in (EventImage(4, (399, 1, 0), 1), EventImage(4, (399, 0, 0), 0),
                      EventImage(2, (7, 0, 5), 2), EventImage(3, (1, 0, 0), 1),
                      EventImage(2, (4, 2, 1), 2), EventImage(6, (True, 0, 0), 2)):
            with self.subTest(image=image), self.assertRaises(CodecError):
                decode_event(image)

    def test_results_reject_prose_capacity_overflow_unknown_ids_and_mixed_event_serials(self):
        good = P09World().topics(C)
        for bad in (replace(good, text="invented prose"), replace(good, code="unknown"),
                    replace(good, line_ids=("P09.CHOICE.001",) * 9),
                    replace(good, speech_unit_ids=("P09.OPEN.001.01",) * 7),
                    replace(good, line_ids=("P14.FORGED",)),
                    replace(good, presentation_id="P09:chairs:01"),
                    replace(good, presentation_id="P09:chairs:0"),
                    replace(good, presentation_id="P09:chairs:1073741824")):
            with self.subTest(result=bad), self.assertRaises(CodecError):
                encode_result(bad)
        world = P09World()
        result = world.inspect_chairs(C)
        with self.assertRaises(CodecError):
            encode_result(result, revision=world.revision + 1)
        with self.assertRaises(CodecError):
            encode_result(replace(result, events=result.events * 4))

    def test_result_decode_rejects_hidden_padding_bad_counts_and_orphan_presentation_serials(self):
        image = encode_result(P09World().topics(C), revision=MAX_SERIAL)
        self.assertEqual(join_serial(image.properties["p09ResultHi"], image.properties["p09ResultLo"]), MAX_SERIAL)
        bad_images = (
            replace(image, lines=image.lines[:-1] + (1,)),
            replace(image, units=(1,) + image.units[1:]),
            replace(image, events=(1, 0, 0)),
            replace(image, event_args=(1,) + image.event_args[1:]),
            replace(image, properties=dict(image.properties, p09LineCount=9)),
            replace(image, properties=dict(image.properties, p09PresentationLo=1)),
            replace(image, properties=dict(image.properties, p09PresentationSource=1)),
            replace(image, properties=dict(image.properties, p09Code=0)),
            replace(image, properties=dict(image.properties, p09EventCount=True)),
        )
        for bad in bad_images:
            with self.subTest(image=bad), self.assertRaises(CodecError):
                decode_result(bad)


if __name__ == "__main__":
    unittest.main()
