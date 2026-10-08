"""P09/P10 coexistence in one exact program, with one earned prefix/backend.

All new progress is through player controls, approach/arrival, canonical readers,
and ordinary Main save/restore. The shared prefix genuinely earns P01-P08.
Snapshots are exact-program harness data, never native save/pixel/audio evidence.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import unittest

import host
from test_card_ownership import owners, words as p09_words
from test_cue_ownership import CUES, history as p10_words
from test_p09_active import gate_b, walk
from test_p10_active import input_action, arrive, pick
from test_practical import enter_control
from test_restore import Backend, load


def read_close(h):
    """Read remaining canonical pages and use actual NEXT/CLOSE controls."""
    for _ in range(80):
        if h.p['uiPanel'] not in (1, 4):
            return
        enter_control(h, 11 if h.p['uiPage'] + 1 < h.p['uiPageCount'] else 12)
    raise AssertionError('Reader failed to return through actual Close controls')


def choice_for(h, obj, topic, verb=5):
    input_action(h, verb, obj)
    arrive(h)
    pick(h, topic)


def rack_choice(h, slot, action):
    choice_for(h, 410, 20 + slot)
    pick(h, action)
    read_close(h)


class Coexistence(unittest.TestCase):
    def ownership(self, h, d9, d10, original, old_owners, reservations=None):
        self.assertEqual(owners(h), old_owners)
        self.assertEqual(d9.call('h9InventoryValid'), 1)
        self.assertEqual(d10.call('h10Inv'), 1)
        items = list(h.arrays['uiItems'])
        self.assertEqual(items.count(399), int(original))
        self.assertEqual(h.call('campaignHeld', 399), int(original))
        card = d9.call('h9CardReservation', 399)
        self.assertEqual(card, items.index(399) if original else -1)
        slots = list(d10.arrays['h10S'])
        self.assertEqual(slots, list(range(slots[0], slots[0] + 6)))
        self.assertGreaterEqual(slots[0], 0)
        if reservations is not None:
            self.assertEqual(slots, reservations)
        if original:
            self.assertNotIn(card, slots)
            self.assertGreater(card, slots[-1])  # P10 was earned before P09.
        for cue, slot in zip(CUES, slots):
            held = h.call('campaignHeld', cue)
            self.assertEqual(items.count(cue), held, cue)
            self.assertEqual(items[slot], cue if held else 0, cue)
        self.assertEqual(len([v for v in items if v]), len(set(v for v in items if v)))
        return slots

    def save_restore(self, h, d9, d10, b, old_owners, slots, original=True):
        before = (p09_words(d9), p10_words(d10), list(h.arrays['uiItems']),
                  list(d10.arrays['h10S']), d9.call('h9CardReservation', 399))
        h.call('writeSave')
        self.assertIsNotNone(b.saved)
        load(h, b, copy.deepcopy(b.saved))
        self.assertEqual(h.p['uiFailure'], 0)
        self.assertEqual((p09_words(d9), p10_words(d10), list(h.arrays['uiItems']),
                          list(d10.arrays['h10S']), d9.call('h9CardReservation', 399)), before)
        self.assertEqual(d9.call('h9SaveReady'), 1)
        self.assertEqual(d10.call('h10Save'), 1)
        self.ownership(h, d9, d10, original, old_owners, slots)

    def test_p10_first_then_original_card_both_cue_families_and_restore(self):
        self.assertFalse(os.environ.get('P09_DIAGNOSTIC_CACHE'))
        self.assertFalse(os.environ.get('P10_DEV_REUSE'))
        paired = []
        for source in (False, True):
            backend = 'source' if source else 'emitted'
            print('COEXISTENCE BACKEND', backend, flush=True)
            h, d9 = gate_b(source)
            d10 = h.vm.objects['p10State']
            sd = h.vm.objects['sceneDialogue']
            old_owners = owners(h)
            untouched_p09 = p09_words(d9)
            self.assertEqual((d9.call('h9Active'), d10.call('h10Active')), (1, 1))
            self.assertEqual((d9.p['p09Ready'], d10.call('p10Ready')), (0, 0))
            slots = self.ownership(h, d9, d10, False, old_owners)

            # Actual exit/approach plus the very first P10 input must survive the
            # just-arrived world's fresh-frame boundary without a second click.
            walk(h, 18, 1)
            pending = []
            def observe(obj, name, args, result):
                if obj.name == 'p10State' and name == 'h10Dispatch':
                    pending.append(list(d10.arrays['h10PendingAction']))
            h.vm.after_actual_call = observe
            input_action(h, 2, 7)
            arrive(h)
            h.vm.after_actual_call = None
            self.assertTrue(any(row[0] for row in pending), pending)
            self.assertEqual((h.p['uiPanel'], h.p['uiChoiceContext']), (2, 240))
            pick(h, 2)
            self.assertEqual((h.p['uiDocument'], sd.p['sdResource']), (1202, 211))
            self.assertEqual(d9.arrays['h9R'][0], 0)
            self.assertEqual(h.vm.objects['P09State'].call('h9Frame', 0), 0)
            d9.call('h9Frame', 1)
            read_close(h)
            self.assertEqual(d10.call('p10Complete', 2), 1)
            self.assertEqual(p09_words(d9), untouched_p09)

            walk(h, 12, 2)
            choice_for(h, 5, 1)
            self.assertEqual((h.p['uiDocument'], sd.p['sdResource']), (1200, 211))
            read_close(h)
            self.assertEqual(d10.call('p10Complete', 1), 1)
            walk(h, 18, 1)
            walk(h, 13, 4)
            choice_for(h, 410, 8)
            read_close(h)
            for slot, cue in enumerate((412, 413, 414)):
                choice_for(h, cue, slot + 1)
                read_close(h)
                choice_for(h, cue, 4)
                pick(h, slot)
                read_close(h)
            self.assertEqual([d10.call('p10SlotAt', i) for i in range(3)], [412, 413, 414])
            self.assertEqual((d10.call('p10RackCorrect'), d10.call('p10Ready')), (1, 1))
            self.assertEqual(d9.p['p09Ready'], 0)
            self.assertEqual(p09_words(d9), untouched_p09)
            first_restoration = (d10.p['p10RestoredHi'], d10.p['p10RestoredLo'])
            self.assertNotEqual(first_restoration, (0, 0))
            p10_complete_first = p10_words(d10)
            self.ownership(h, d9, d10, False, old_owners, slots)
            b = Backend(h.vm)
            self.save_restore(h, d9, d10, b, old_owners, slots, original=False)
            print('COEXISTENCE P10 ready before untouched P09', backend, flush=True)

            # The first P09 reader after real travel must be admitted by P09,
            # while P10's canonical reader and persistent receipts stay retired.
            walk(h, 18, 1)
            walk(h, 17, 0)
            walk(h, 16, 6)
            input_action(h, 5, 395)
            arrive(h)
            self.assertEqual((h.p['uiDocument'], sd.p['sdResource']), (1103, 210))
            self.assertEqual(d9.call('p09Count', 3), 1)
            self.assertEqual(d10.arrays['h10Reader'][0], 0)
            self.assertEqual(h.vm.objects['P10State'].call('h10Frame', 0), 0)
            d10.call('h10Frame', 1)
            self.assertEqual(p10_words(d10), p10_complete_first)
            read_close(h)

            input_action(h, 6, 29)
            arrive(h)
            self.assertEqual(h.p['uiChoiceContext'], 239)
            pick(h, 7)
            self.assertEqual((h.p['uiDocument'], h.p['uiPageCount']), (1109, 5))
            self.assertEqual(d9.call('p09Count', 7), 1)
            for page in range(1, 5):
                self.assertEqual(h.call('campaignHeld', 399), 0)
                enter_control(h, 11)
                self.assertEqual(d9.call('p09Count', 7), page + 1)
                self.assertEqual(p10_words(d10), p10_complete_first)
            self.assertEqual(d9.p['p09Ready'], 1)
            self.assertEqual(d9.call('p09Count', 7), 5)
            self.ownership(h, d9, d10, True, old_owners, slots)
            self.save_restore(h, d9, d10, b, old_owners, slots)
            self.assertEqual((h.p['uiDocument'], d9.call('p09Count', 7)), (1109, 5))
            enter_control(h, 11)
            self.assertEqual((h.p['uiDocument'], d9.call('p09Count', 7)), (1116, 6))
            read_close(h)
            input_action(h, 2, 399)
            arrive(h)
            self.assertEqual((h.p['uiDocument'], h.p['uiPageCount']), (1111, 2))
            read_close(h)
            self.assertEqual(d9.call('p09Count', 9), 1)
            self.assertEqual(p10_words(d10), p10_complete_first)
            p09_complete = p09_words(d9)
            print('COEXISTENCE original399 and paper rack restored together', backend, flush=True)

            walk(h, 17, 0)
            # The front door is closed after leaving: OPEN precedes WALK in
            # the genuine campaign route, and both use actual player controls.
            input_action(h, 2, 1)
            arrive(h)
            read_close(h)
            walk(h, 1, 1)
            walk(h, 13, 4)
            for slot in range(3):
                rack_choice(h, slot, 5)
            self.assertEqual([h.call('campaignHeld', cue) for cue in CUES], [1] * 6)
            self.assertEqual(d10.call('p10Ready'), 1)
            self.ownership(h, d9, d10, True, old_owners, slots)
            self.save_restore(h, d9, d10, b, old_owners, slots)

            for slot, cue in enumerate((48, 49, 50)):
                choice_for(h, cue, slot + 1)
                read_close(h)
                choice_for(h, cue, 4)
                pick(h, slot)
                read_close(h)
            self.assertEqual([d10.call('p10SlotAt', i) for i in range(3)], [48, 49, 50])
            self.assertEqual([h.call('campaignHeld', cue) for cue in CUES], [0, 0, 0, 1, 1, 1])
            self.assertEqual((d10.call('p10RackCorrect'), d10.call('p10Ready')), (1, 1))
            self.assertEqual((d10.p['p10RestoredHi'], d10.p['p10RestoredLo']), first_restoration)
            self.assertEqual(p09_words(d9), p09_complete)
            self.save_restore(h, d9, d10, b, old_owners, slots)
            for _ in range(2):
                self.assertEqual(h.call('p02HostInventory'), 1)
                self.ownership(h, d9, d10, True, old_owners, slots)
            self.assertEqual(d9.call('p09Validate'), 1)
            self.assertEqual(d10.call('p10Validate'), 1)
            if source:
                for owner, methods in (
                    ('p09State', ('h9Dispatch', 'h9Choice', 'h9Draw', 'h9Frame', 'h9Restore')),
                    ('p10State', ('h10Dispatch', 'h10Choice', 'h10Frame', 'h10Txn')),
                    ('cakood', ('drawWorld', 'uiHostChoice', 'uiHostClosed'))):
                    for method in methods:
                        self.assertGreater(h.vm.sources[owner].source_calls[method], 0, (owner, method))
            result = {
                'p09_words': p09_words(d9), 'p10_words': list(p10_words(d10)),
                'inventory': list(h.arrays['uiItems']), 'cue_reservations': list(d10.arrays['h10S']),
                'original399_reservation': d9.call('h9CardReservation', 399),
                'first_restoration': list(first_restoration),
                'rack': [d10.call('p10SlotAt', i) for i in range(3)],
            }
            paired.append(result)
            receipt = dict(result, backend=backend, status='PASS', native_acceptance=False,
                           actual_first_arrival=True, p10_completed_before_p09=True,
                           ordinary_restore_checkpoints=4, optional_diagnostic_snapshot_reuse=False,
                           inherited_authenticated_prerequisite_cache_allowed=True,
                           test_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
            (host.H / 'evidence' / ('coexistence-r2-proof-' + backend + '.json')).write_text(
                json.dumps(receipt, indent=2) + '\n')
            print('COEXISTENCE PASS', backend, flush=True)
        self.assertEqual(paired[0], paired[1], 'Source and emitted coexistence outcomes diverged')


if __name__ == '__main__':
    unittest.main(verbosity=2)
