"""Finite SCI serial gates at codec-valid model boundaries, using both oracles."""
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
H = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(H))
sys.path.insert(0, str(H / 'tests'))
from harness import SourceDomain, EmittedDomain, snapshot
from codec.p09_codec import MAX_SERIAL, SERIAL_BASE, PERSISTED_PROPERTIES, encode_world, decode_world
from reference.cakood.p09_model import CONSERVATORY, P09Context, P09World

C = P09Context(CONSERVATORY, flags=frozenset(('EVENING_STARTED', 'PLAN_AGREED')))
MEASUREMENTS = []


class SerialGates(unittest.TestCase):
    def setUp(self):
        self.source = SourceDomain()
        self.emitted = EmittedDomain()
        self.calls = 0
        self.assertEqual(snapshot(self.source), snapshot(self.emitted))

    def tearDown(self):
        MEASUREMENTS.append(dict(test=self.id(), paired_calls=self.calls,
                                 emitted_instructions=self.emitted.vm.steps))

    def call(self, name, *args):
        left = self.source.call(name, *args)
        right = self.emitted.call(name, *args)
        self.calls += 1
        self.assertEqual(left, right, (name, args, 'return'))
        self.assertEqual(snapshot(self.source), snapshot(self.emitted), (name, args, 'complete state'))
        return left

    def persisted(self):
        return {k: self.source.p[k] for k in PERSISTED_PROPERTIES}

    def load_hint(self, revision, hint=1):
        world = P09World(revision=revision, hint_level=hint)
        props = encode_world(world, context=C)
        self.assertEqual(decode_world(props, context=C).save(), world.save())
        self.assertEqual(self.call('p09LoadBegin'), 1)
        for index, key in enumerate(PERSISTED_PROPERTIES):
            self.assertEqual(self.call('p09LoadWord', index, props[key]), 1)
        self.assertEqual(self.call('p09LoadCommit'), 1)
        self.assertEqual(self.persisted(), props)
        self.assertEqual(self.call('p09Validate'), 1)
        epoch = self.source.p['p09Epoch'] + 1
        self.assertEqual(self.call('p09Context', 6, 0, 1, 1, 6, 6, 0, 0, 0, 0, epoch), 1)
        self.assertEqual(self.call('p09ValidateContext'), 1)
        return world

    def test_logical_helpers_return_normalized_booleans(self):
        for revision in (32767, 32768, 65536, MAX_SERIAL):
            with self.subTest(revision=revision):
                self.load_hint(revision)
                self.assertEqual(self.call('p09Present', 0), 1)
                self.assertEqual(self.call('p09Present', 1), 0)
                self.assertEqual(self.call('p09Equal', 0, 0), 1)
                self.assertEqual(self.call('p09Equal', 0, 1), 0)
                self.assertEqual(self.call('p09Less', 1, 0), 1)
                self.assertEqual(self.call('p09Less', 0, 1), 0)

    def test_hint_commit_carries_low_limb_at_32767(self):
        world = self.load_hint(SERIAL_BASE - 1)
        world.hint(C, 2)
        self.assertEqual(self.call('p09Hint', 2), 23)
        self.assertEqual((self.source.p['p09RevisionHi'], self.source.p['p09RevisionLo']), (1, 0))
        self.assertEqual(self.persisted(), encode_world(world, context=C))
        self.assertEqual(self.source.p['p09EventCount'], 1)
        self.assertEqual(self.call('p09Validate'), 1)
        world.hint(C, 3)
        self.assertEqual(self.call('p09Hint', 3), 23)
        self.assertEqual((self.source.p['p09RevisionHi'], self.source.p['p09RevisionLo']), (1, 1))
        self.assertEqual(self.persisted(), encode_world(world, context=C))

    def test_last_representable_commit_then_fail_closed(self):
        world = self.load_hint(MAX_SERIAL - 1)
        world.hint(C, 2)
        self.assertEqual(self.call('p09Hint', 2), 23)
        self.assertEqual(self.persisted(), encode_world(world, context=C))
        self.assertEqual((self.source.p['p09RevisionHi'], self.source.p['p09RevisionLo']), (32767, 32767))
        before = self.persisted()
        self.assertEqual(self.call('p09Hint', 3), 29)
        self.assertEqual(self.persisted(), before)
        self.assertEqual(self.source.p['p09EventCount'], 0)
        self.assertEqual(self.call('p09Validate'), 1)
        self.assertEqual(decode_world(self.persisted(), context=C).save(), world.save())

    def test_max_serial_blocks_presentation_and_preserves_save(self):
        world = self.load_hint(MAX_SERIAL)
        before = self.persisted()
        self.assertEqual(self.call('p09Begin', 3), 29)
        self.assertEqual(self.persisted(), before)
        self.assertEqual(self.source.p['p09EventCount'], 0)
        self.assertEqual(self.source.p['p09PresentationSource'], 0)
        self.assertEqual(list(self.source.arrays['p09Lease']), [0] * 10)
        self.assertEqual(self.call('p09Hint', 2), 29)
        self.assertEqual(self.persisted(), before)
        self.assertEqual(self.call('p09Validate'), 1)
        self.assertEqual(decode_world(self.persisted(), context=C).save(), world.save())

    def test_max_serial_allows_idempotent_existing_hint(self):
        world = self.load_hint(MAX_SERIAL, hint=3)
        before = self.persisted()
        self.assertEqual(self.call('p09Hint', 3), 23)
        self.assertEqual(self.persisted(), before)
        self.assertEqual(self.source.p['p09EventCount'], 0)
        self.assertEqual(decode_world(self.persisted(), context=C).save(), world.save())


if __name__ == '__main__':
    unittest.main(verbosity=2)
