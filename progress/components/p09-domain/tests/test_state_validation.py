"""Bounded causal-save validation parity against source and emitted bytecode.

Every case compares a real call to p09Validate with strict decode_world
acceptance. Inputs are actual signed SCI words, not Python-only hostile types.
This suite does not reinterpret or replace either accepted evaluator.
"""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import time
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from harness import SourceDomain, EmittedDomain, snapshot
from codec.p09_codec import CodecError, MAX_SERIAL, encode_world, decode_world
from reference.cakood.p09_model import P09Context, P09World, CONSERVATORY, RECORD_UNITS

C = P09Context(CONSERVATORY, flags=frozenset(("EVENING_STARTED", "PLAN_AGREED")))
SIDE = replace(C, conservatory_view="side")
MEASUREMENTS = []
COUNTEREXAMPLES = []
GROUP_SIZE = 40


def clone(world):
    return P09World.load(world.save())


def receipt(world, source, *, record=None, units=(), context=C):
    p = world.presentations[source]
    return world.acknowledge_presentation(context, f"P09:{source}:{p.serial}",
                                          record_id=record, speech_unit_ids=units)


def representative_worlds():
    worlds = {"initial": P09World()}
    world = P09World()
    world.ask_three_things(C)
    receipt(world, "direct_question", units=("P09.DIALOGUE.001.01",))
    worlds["partial_receipt"] = clone(world)
    receipt(world, "direct_question", record="P09.DIALOGUE.001")
    world.discuss_terms(C)
    receipt(world, "terms", units=RECORD_UNITS["P09.DIALOGUE.002"][:2])
    worlds["partial_terms"] = clone(world)
    receipt(world, "terms", record="P09.DIALOGUE.002")
    worlds["terms_granted"] = clone(world)
    receipt(world, "terms", record="P09.SUCCESS.001")
    worlds["success_complete"] = clone(world)
    world.connect_shared_wish(C)
    receipt(world, "shared_wish", units=RECORD_UNITS["P09.DIALOGUE.003"][:2])
    receipt(world, "shared_wish", units=RECORD_UNITS["P09.DIALOGUE.003"][2:])
    worlds["shared_complete"] = clone(world)
    return worlds


def interleaved_world():
    world = P09World()
    world.introduce(SIDE)
    receipt(world, "intro", units=("P09.OPEN.001.01",), context=SIDE)
    for source in ("chair_tag", "direct_question", "front_context", "chairs", "accusation"):
        world.begin_presentation(C, source)
    receipt(world, "direct_question", units=("P09.DIALOGUE.001.01",))
    world.connect_shared_wish(C)
    world.discuss_terms(C)
    receipt(world, "front_context", record="P09.DIALOGUE.001")
    receipt(world, "shared_wish", units=RECORD_UNITS["P09.DIALOGUE.003"][:2])
    receipt(world, "terms", units=RECORD_UNITS["P09.DIALOGUE.002"][:3])
    receipt(world, "chair_tag", record="P09.READ.001")
    receipt(world, "chairs", record="P09.LOOK.001")
    receipt(world, "accusation", record="P09.FAILURE.001")
    receipt(world, "terms", record="P09.DIALOGUE.002")
    world.begin_presentation(C, "terms_card")
    receipt(world, "terms_card", record="P09.READ.002")
    receipt(world, "shared_wish", units=RECORD_UNITS["P09.DIALOGUE.003"][2:])
    receipt(world, "direct_question", record="P09.DIALOGUE.001")
    receipt(world, "terms", record="P09.SUCCESS.001")
    world.validate()
    return world


def shifted(world, final_revision):
    world = clone(world)
    offset = final_revision - world.revision
    if offset < 0:
        raise ValueError("Shift must preserve positive action serials")
    world.revision = final_revision
    for presentation in world.presentations.values():
        presentation.serial += offset
        presentation.receipts = {token: serial + offset for token, serial in presentation.receipts.items()}
    world.consumed = {event: serial + offset for event, serial in world.consumed.items()}
    world.validate()
    return world


BASE_WORLDS = representative_worlds()


def mutation_groups():
    """Every persisted field gets scalar, sign, boundary, and adjacent probes."""
    for state_name, world in BASE_WORLDS.items():
        original = encode_world(world)
        probes = []
        for field, before in original.items():
            candidates = sorted({-1, 0, 1, 2, 32767, before - 1, before + 1})
            for after in candidates:
                if after != before and -32768 <= after <= 32767:
                    probes.append((state_name, original, field, after))
        for index in range(0, len(probes), GROUP_SIZE):
            yield state_name, index // GROUP_SIZE, probes[index:index + GROUP_SIZE]


class ValidationParityTests(unittest.TestCase):
    def setUp(self):
        self.source = SourceDomain()
        self.emitted = EmittedDomain()
        self.start = time.monotonic()
        self.checked = 0
        self.accepted = 0
        self.rejected = 0

    def tearDown(self):
        MEASUREMENTS.append({
            "test": self.id(), "cases_checked": self.checked,
            "model_accepted": self.accepted, "model_rejected": self.rejected,
            "seconds": round(time.monotonic() - self.start, 6),
            "emitted_instructions": self.emitted.vm.steps,
        })

    def compare(self, properties, label, expected=None):
        model_error = None
        try:
            decode_world(properties)
            accepted = True
        except CodecError as error:
            accepted = False
            model_error = str(error)
        if expected is not None:
            self.assertEqual(accepted, expected, (label, model_error))
        for domain in (self.source, self.emitted):
            domain.p.update(properties)
        before_source = snapshot(self.source)
        before_emitted = snapshot(self.emitted)
        source_result = self.source.call("p09Validate")
        emitted_result = self.emitted.call("p09Validate")
        self.checked += 1
        self.accepted += int(accepted)
        self.rejected += int(not accepted)
        if source_result != int(accepted) or emitted_result != int(accepted):
            counterexample = {
                "label": label, "codec_accepted": accepted, "codec_error": model_error,
                "source_result": source_result, "emitted_result": emitted_result,
                "properties": properties,
            }
            COUNTEREXAMPLES.append(counterexample)
            print("VALIDATION_COUNTEREXAMPLE " + json.dumps(counterexample, sort_keys=True), flush=True)
        self.assertEqual(source_result, int(accepted), (label, model_error, "source"))
        self.assertEqual(emitted_result, int(accepted), (label, model_error, "emitted"))
        self.assertEqual(snapshot(self.source), before_source, (label, "source validation mutated state"))
        self.assertEqual(snapshot(self.emitted), before_emitted, (label, "emitted validation mutated state"))
        self.assertEqual(snapshot(self.source), snapshot(self.emitted), (label, "source/emitted full-state mismatch"))

    def test_valid_interleaving_repeated_stamps_and_revision_gaps(self):
        complex_world = interleaved_world()
        all_stamps = [stamp for p in complex_world.presentations.values() for stamp in p.receipts.values()]
        self.assertLess(len(set(all_stamps)), len(all_stamps))
        self.assertEqual(len(complex_world.presentations), 9)
        self.compare(encode_world(complex_world), "nine-source interleaving", expected=True)
        for state_name, original in BASE_WORLDS.items():
            world = clone(original)
            world.revision += 29  # The model permits unused revision gaps.
            self.compare(encode_world(world), state_name + ":revision_gap", expected=True)
        partial = clone(BASE_WORLDS["partial_receipt"])
        partial.revision += 7
        partial.discuss_terms(C)
        receipt(partial, "terms", record="P09.DIALOGUE.002")
        self.compare(encode_world(partial), "gap followed by new actions", expected=True)

    def test_valid_serial_limb_boundaries_preserve_receipt_chronology(self):
        complex_world = interleaved_world()
        for boundary in (32767, 32768, 32769, 65535, 65536, MAX_SERIAL - 1, MAX_SERIAL):
            self.compare(encode_world(shifted(complex_world, boundary)),
                         f"interleaved shifted to {boundary}", expected=True)
        for boundary in (0, 32767, 32768, MAX_SERIAL):
            self.compare(encode_world(P09World(revision=boundary)),
                         f"empty revision {boundary}", expected=True)


def attach_mutation_test(state_name, group, probes):
    def test(self):
        for state, original, field, value in probes:
            properties = dict(original)
            properties[field] = value
            label = f"{state}:{field}:{original[field]}->{value}"
            with self.subTest(case=label):
                self.compare(properties, label)
    test.__name__ = f"test_corruption_{state_name}_{group:02d}"
    test.__doc__ = f"{len(probes)} independent one-field corruptions of {state_name}."
    setattr(ValidationParityTests, test.__name__, test)


for _state_name, _group, _probes in mutation_groups():
    attach_mutation_test(_state_name, _group, _probes)


if __name__ == "__main__":
    started = time.monotonic()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ValidationParityTests)
    result = unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)
    evidence = {
        "status": "PASS" if result.wasSuccessful() else "FAIL",
        "scope": "Bounded signed-word causal-save validation parity; not native playability",
        "tests_run": result.testsRun,
        "cases_checked": sum(row["cases_checked"] for row in MEASUREMENTS),
        "model_accepted": sum(row["model_accepted"] for row in MEASUREMENTS),
        "model_rejected": sum(row["model_rejected"] for row in MEASUREMENTS),
        "seconds": round(time.monotonic() - started, 6),
        "max_group_seconds": max((row["seconds"] for row in MEASUREMENTS), default=0),
        "groups": MEASUREMENTS, "counterexamples": COUNTEREXAMPLES,
        "failures": [{"test": str(test), "traceback": detail} for test, detail in result.failures],
        "errors": [{"test": str(test), "traceback": detail} for test, detail in result.errors],
    }
    target = ROOT / "evidence" / "validation-parity.json"
    target.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print("VALIDATION_SUMMARY " + json.dumps({key: value for key, value in evidence.items()
          if key not in {"groups", "counterexamples", "failures", "errors"}}, sort_keys=True), flush=True)
    raise SystemExit(0 if result.wasSuccessful() else 1)
