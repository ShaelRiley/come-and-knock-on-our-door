"""Closed P10 ownership gate, paired editable-source and emitted execution.

Campaign admission is earned by test_card_ownership.committed: actual P01-P08
actions and the accepted evening ACK. That baseline intentionally freezes player
travel after ACK. Ownership mutations use actual host context through h10Txn;
plan Begin/Acknowledge uses explicitly local accepted-domain room1 inputs without
moving the host, changing history flags, or claiming an active reader. ACKs are closed harness inputs,
not evidence of native P10 reader/UI activation. SaveGame/RestoreGame use the
ordinary Main entrypoints and the deterministic backend, not native save files.

P08 requires the genuine P03 grant, so a P03-absent *whole-campaign* paper route
does not exist. Paper's independent domain recipe remains a separate domain
proof; these integration cases never erase or manufacture campaign readiness.
"""
import sys
sys.dont_write_bytecode = True
import copy
import itertools
import unittest

import host
from campaign_route import living
from source_host import VM as SourceVM
from test_card_ownership import committed, fresh, owners, terms, words as card_words
from test_restore import Backend, load
from test_return_caption import first_entry


EMITTED = host.VM
CUES = (48, 49, 50, 412, 413, 414)
OWNED = (35, 48, 49, 50, 410, 411, 412, 413, 414)
PERMUTATIONS = tuple(itertools.permutations(range(3)))
PREPARED = {}


def txn(d, op, *args):
    assert len(args) <= 7
    return d.call('h10Txn', op, *(tuple(args) + (0,) * (7 - len(args))))


def ack_args(d, source, record=None, first=0, last=0):
    if record is None:
        record = d.call('p10SourceRecord', source)
    return (source, d.call('p10SerialHi', source + 3),
            d.call('p10SerialLo', source + 3), d.p['p10Epoch'],
            record, first, last)


def acknowledge(d, source, record=None, first=0, last=0):
    return txn(d, 7, *ack_args(d, source, record, first, last))


def context(h, d):
    """No supplied location, actor placement, knowledge, or readiness claims."""
    assert d.call('h10Ctx') == 1
    s = h.vm.objects['p08State']
    assert (d.p['p10Room'], d.p['p10Apron'], d.p['p10Evening']) == (
        h.p['location'], h.p['onApron'], s.call('h8EveningCommitted'))
    assert tuple(d.p[n] for n in ('p10BunnyRoom', 'p10FrankieRoom', 'p10RitaRoom')) == tuple(
        s.call('h8ActorRoom', actor) for actor in (2, 3, 7))
    assert d.p['p10KnowOrder'] == 0


def plan_context(h, d):
    """Local domain fixture only; actual player remains in frozen room4.

    This deliberately does not go through h10Txn's actual-room authority.
    It supplies no P03/evening/readiness flags and earns the domain receipt
    through real Begin/Acknowledge before returning to actual host context.
    """
    owner = h.vm.objects['p08State']
    assert h.p['location'] == 4 and owner.call('h8ActionBarrier') == 1
    assert d.call('h10Take', 0) == 1
    assert d.call('p10Context', 1, 0, owner.call('h8EveningCommitted'), 0,
                  owner.call('h8ActorRoom', 2), owner.call('h8ActorRoom', 3),
                  owner.call('h8ActorRoom', 7), 0, d.call('p10Ready'), d.p['p10Epoch'] + 1) == 1
    for obj in (24, 25, 48, 49, 50):
        if h.call('campaignHeld', obj):
            assert d.call('p10ContextItem', obj) == 1
    assert txn(d, 3, 48, 1) == -1  # Actual-host transaction rejects fixture room.


def plan_receipt(h, d):
    plan_context(h, d)
    assert d.call('p10Begin', 2) == 35
    assert d.call('h10Take', 0) == 1
    assert d.call('p10Acknowledge', *ack_args(d, 2)) == 37
    assert d.call('h10Take', 0) == 1
    context(h, d)


def courtyard(h):
    if h.p['location'] != 4:
        living(h)
        host.act(h, 0, 13)
    assert h.p['location'] == 4 and not h.p['onApron']


def history(d):
    """Persistent domain history; transient context/leases/results excluded."""
    return tuple(d.call('h10Word', 0, i, 0) for i in range(61))


def gate(d):
    return tuple(tuple(d.arrays[n]) for n in ('h10M', 'h10S', 'h10R', 'h10E'))


def events(d):
    return tuple((d.call('p10Event', i), d.call('p10EventSerialHi', i),
                  d.call('p10EventSerialLo', i),
                  tuple(d.call('p10EventArg', i, j) for j in range(4)))
                 for i in range(d.p['p10EventCount']))


def ui(h):
    return (tuple(h.arrays['uiItems']), h.p['uiInventoryExtent'],
            h.p['uiInventoryPages'], h.p['uiInventoryPage'],
            h.p['uiNounA'], h.p['uiVerb'], h.p['uiFocus'])


def unrelated(h):
    return tuple((obj, h.call('campaignHeld', obj), h.call('p02ObjectLocation', obj))
                 for obj in (24, 25, 76, 399))


def ready(source, paper=True, card=False):
    """Snapshot only after authentic campaign, travel, and closed P10 actions."""
    key = (source, paper, card)
    if key not in PREPARED:
        h, p09 = committed(source)
        d = h.vm.objects['p10State']
        p = h.vm.objects['p03State']
        assert p.p['p03Ready'] == 1 and p.call('p03Validate') == 1
        assert h.vm.objects['p08State'].call('h8EveningCommitted') == 1
        courtyard(h)
        context(h, d)
        assert d.p['p10BunnyRoom'] == h.p['location']
        assert txn(d, 1) == 35
        assert acknowledge(d, 1) == 37
        plan_receipt(h, d)
        assert d.call('p10Complete', 2) == 1 and d.call('p10KnowsOrder') == 1
        assert h.p['location'] == 4
        if paper:
            assert txn(d, 2) == 19
        if card:
            terms(p09)
            assert p09.call('h9ProjectCard') == 1
            assert d.call('h10Proj') == 1
        assert d.call('h10Save') == 1
        PREPARED[key] = h.vm.snapshot()
    vm = SourceVM() if source else EMITTED()
    vm.budget = 900000000
    vm.restore(copy.deepcopy(PREPARED[key]))
    return vm.objects['cakood'], vm.objects['p10State']


def check(t, h, d):
    t.assertEqual((d.call('p10Validate'), d.call('h10Valid'),
                   d.call('h10Inv'), d.call('h10Save')), (1, 1, 1, 1))
    slots = list(h.arrays['uiItems'])
    t.assertEqual(len(set(d.arrays['h10S'])), 6)
    t.assertEqual(tuple(d.arrays['h10S']), tuple(range(d.arrays['h10S'][0], d.arrays['h10S'][0] + 6)))
    t.assertEqual(h.p['uiInventoryPages'], max(1, (h.p['uiInventoryExtent'] + 7) // 8))
    t.assertLess(h.p['uiInventoryPage'], h.p['uiInventoryPages'])
    rack = tuple(d.call('p10SlotAt', i) for i in range(3))
    t.assertEqual(tuple(d.arrays['h10R']), rack)
    for i, obj in enumerate(CUES):
        held = int(obj not in rack and (i < 3 or d.call('p10Present', 2)))
        position = 4 if obj in rack else (10 if held else -1)
        t.assertEqual(h.call('campaignHeld', obj), held, obj)
        t.assertEqual(h.call('p02ObjectLocation', obj), position, obj)
        t.assertEqual(h.call('campaignReachable', obj), 0, obj)
        t.assertEqual(slots.count(obj), held, obj)
        t.assertEqual(slots[d.arrays['h10S'][i]], obj if held else 0, obj)
        t.assertNotIn(obj, h.arrays['p02Slots'])
        t.assertNotIn(obj, h.vm.objects['p03State'].arrays['bSlots'])
        t.assertNotIn(obj, h.vm.objects['p04State'].arrays['qSlots'])
    t.assertNotIn(35, slots)
    t.assertEqual(h.vm.objects['p08State'].call('h8EveningReady'), 0)
    t.assertEqual(h.vm.objects['p09State'].call('h9Active'), 0)


class CueOwnership(unittest.TestCase):
    def test_01_fresh_closed_gate_high_ids_and_ordinary_save(self):
        for source in (False, True):
            with self.subTest(source=source):
                h = fresh(source)
                d = h.vm.objects['p10State']
                before, old, view = history(d), owners(h), ui(h)
                for obj in (-32768, -1, 0, 24, 25, 35, 48, 49, 50, 76,
                            94, 95, 394, 399, 400, 409, 410, 411, 412, 413, 414, 415, 32767):
                    self.assertEqual(d.call('h10Q', 0, obj), 1 if obj in OWNED else -2)
                    self.assertEqual(d.call('p10CueIndex', obj), CUES.index(obj) if obj in CUES else -1)
                    self.assertEqual(h.call('p03HostReservation', obj), -1 if obj > 32 or obj < 0 else h.arrays['p02Reserved'][obj])
                    if obj in OWNED:
                        self.assertEqual((h.call('campaignHeld', obj), h.call('campaignReachable', obj),
                                          h.call('p02ObjectLocation', obj)), (0, 0, -1))
                for obj in OWNED:
                    for verb in range(10):
                        for method in ('hostActNow', 'uiHostAct'):
                            self.assertEqual(h.call(method, verb, obj, 0), 0)
                            self.assertEqual(h.call(method, verb, 25, obj), 0)
                self.assertEqual((history(d), owners(h), ui(h)), (before, old, view))
                self.assertEqual(tuple(d.arrays['h10S']), (-1,) * 6)
                for obj in CUES:
                    self.assertEqual(h.call('h10UI', 0, obj), 0)
                self.assertEqual(ui(h), view)
                self.assertEqual(d.call('h10Save'), 1)
                self.assertEqual(txn(d, 2), -1)  # No valid current context yet.
                first_entry(h)
                host.act(h, 0, 12)
                backend = Backend(h.vm)
                h.call('writeSave')
                self.assertIsNotNone(backend.saved)
                load(h, backend)
                self.assertEqual(history(d), before)
                self.assertEqual(d.call('h10Save'), 1)
                self.assertEqual(d.p['p10ContextValid'], 0)
                self.assertEqual(tuple(d.arrays['p10Lease']), (0,) * 8)

    def test_02_real_context_plan_receipt_and_exact_two_event_intake(self):
        for source in (False, True):
            with self.subTest(source=source):
                h, _ = committed(source)
                d = h.vm.objects['p10State']
                context(h, d)
                self.assertEqual(d.call('p10KnowsOrder'), 0)
                self.assertEqual(txn(d, 3, 48, 1), 22)
                self.assertEqual(txn(d, 6, 2), 2)  # Plan is in actual room 1.
                self.assertEqual(txn(d, 1), 35)
                intro = events(d)
                self.assertEqual([v[0] for v in intro], [3, 1])
                self.assertEqual([v[2] for v in intro], [1, 2])
                consumed = gate(d)
                for _ in range(3):
                    self.assertEqual(d.call('h10Take', 0), 1)
                    self.assertEqual(gate(d), consumed)
                # A counterfeit replay must neither advance the cursor nor
                # partially publish its earlier event before rejecting later.
                clean = h.vm.snapshot()
                for field, index in (('p10Events', 1), ('p10EventArgs', 4),
                                     ('p10EventHi', 1), ('p10EventLo', 1)):
                    h.vm.restore(copy.deepcopy(clean))
                    d.arrays[field][index] += 1
                    self.assertEqual(d.call('h10Take', 0), 0, field)
                    self.assertEqual(gate(d), consumed, field)
                h.vm.restore(copy.deepcopy(clean))
                self.assertEqual(acknowledge(d, 1), 37)
                self.assertEqual(txn(d, 1), 34)
                self.assertEqual(d.p['p10EventCount'], 0)
                room = h.p['location']
                host.act(h, 0, 18)
                self.assertEqual(h.p['location'], room)  # Real post-ACK travel remains blocked.
                plan_context(h, d)
                self.assertEqual(d.p['p10Room'], 1)
                self.assertEqual(d.call('p10KnowsOrder'), 0)
                self.assertEqual(d.call('p10Begin', 2), 35)
                stale = ack_args(d, 2)
                self.assertEqual(d.call('h10Valid'), 0)
                context(h, d)  # Exact event intake precedes retiring the fixture lease.
                self.assertEqual(d.call('h10Valid'), 1)
                self.assertEqual(d.call('p10Acknowledge', *stale), 38)
                self.assertEqual(d.call('p10KnowsOrder'), 0)
                plan_context(h, d)
                self.assertEqual(d.call('p10Begin', 2), 35)
                self.assertEqual(d.call('h10Take', 0), 1)
                self.assertEqual(d.call('p10Acknowledge', *ack_args(d, 2)), 37)
                self.assertEqual(d.call('h10Take', 0), 1)
                self.assertEqual(d.call('p10Count', 2), 1)
                self.assertEqual(d.p['p10KnowOrder'], 0)
                self.assertEqual(d.call('p10KnowsOrder'), 1)
                after = history(d), gate(d)
                self.assertEqual(d.call('p10Acknowledge', *ack_args(d, 2)), 36)
                self.assertEqual(d.call('h10Take', 0), 1)
                self.assertEqual((history(d), gate(d)), after)
                context(h, d)
                self.assertEqual(h.p['location'], room)
                self.assertEqual(d.p['p10BunnyRoom'], h.vm.objects['p08State'].call('h8ActorRoom', 2))
                master = h.p['p02MasterHeld']
                self.assertEqual(txn(d, 2), 19)
                self.assertEqual(events(d)[0][0], 4)
                paper = history(d), gate(d), ui(h)
                for _ in range(3):
                    self.assertEqual(d.call('h10Take', 0), 1)
                    self.assertEqual((history(d), gate(d), ui(h)), paper)
                self.assertEqual(txn(d, 2), 17)
                self.assertEqual(d.p['p10EventCount'], 0)
                self.assertEqual(h.p['p02MasterHeld'], master)
                self.assertEqual(txn(d, 8, 1), 31)
                self.assertEqual(events(d)[0][0], 8)
                hinted = history(d), gate(d)
                self.assertEqual(d.call('h10Take', 0), 1)
                self.assertEqual(txn(d, 8, 1), 31)
                self.assertEqual(d.p['p10EventCount'], 0)
                self.assertEqual((history(d), gate(d)), hinted)
                check(self, h, d)

    def permutations(self, cues, paper):
        for source in (False, True):
            h, d = ready(source, paper=paper)
            clean = h.vm.snapshot()
            old = owners(h), unrelated(h)
            for label_order, install_order in itertools.product(PERMUTATIONS, repeat=2):
                with self.subTest(source=source, cues=cues, labels=label_order, install=install_order):
                    h.vm.restore(copy.deepcopy(clean))
                    for index in range(3):
                        self.assertEqual(txn(d, 3, cues[index], label_order[index] + 1), 24)
                        self.assertEqual(events(d)[0][0], 5)
                    for count, index in enumerate(install_order, 1):
                        self.assertEqual(txn(d, 4, cues[index], label_order[index]), 28)
                        self.assertEqual(events(d)[0][0], 6)
                        self.assertEqual(d.call('p10RackCorrect'), int(count == 3))
                        self.assertEqual(d.call('p10Ready'), int(count == 3))
                        self.assertEqual(d.call('h10Take', 0), 1)
                        check(self, h, d)
                    self.assertEqual(tuple(d.call('p10LabelFor', d.call('p10SlotAt', i)) for i in range(3)), (1, 2, 3))
                    self.assertEqual((owners(h), unrelated(h)), old)
                    self.assertEqual(d.call('p10Present', 2), int(paper))
                    if paper:
                        self.assertTrue(all(d.arrays['p10Held'][obj] == 0 for obj in CUES[3:]))

    def test_03_ceramic_all_label_and_install_permutations(self):
        self.permutations((48, 49, 50), paper=False)

    def test_04_paper_all_label_and_install_permutations(self):
        self.permutations((412, 413, 414), paper=True)

    def test_05_mixed_all_label_and_install_permutations(self):
        self.permutations((48, 413, 50), paper=True)

    def test_06_removed_erased_reordered_current_correct_and_first_completion(self):
        for source in (False, True):
            with self.subTest(source=source):
                h, d = ready(source)
                old = owners(h), unrelated(h)
                for i, obj in enumerate((48, 413, 50)):
                    self.assertEqual(txn(d, 3, obj, i + 1), 24)
                    self.assertEqual(txn(d, 4, obj, i), 28)
                first = d.call('p10SerialHi', 3), d.call('p10SerialLo', 3)
                self.assertNotEqual(first, (0, 0))
                self.assertEqual(txn(d, 5, 0), 30)
                self.assertEqual((d.call('p10RackCorrect'), d.call('p10Ready')), (0, 1))
                check(self, h, d)
                self.assertEqual(txn(d, 4, 413, 0), 28)  # Existing original moves, origin=2.
                self.assertEqual(events(d)[0][3], (413, 0, 0, 2))
                self.assertEqual(txn(d, 4, 48, 1), 28)
                self.assertEqual(d.call('p10RackCorrect'), 0)
                self.assertEqual(txn(d, 3, 413, 0), 24)
                self.assertEqual(d.call('p10LabelFor', 413), 0)
                self.assertEqual((d.call('p10RackCorrect'), d.call('p10Ready')), (0, 1))
                self.assertEqual(txn(d, 3, 413, 1), 24)
                self.assertEqual(txn(d, 3, 48, 2), 24)
                self.assertEqual(d.call('p10RackCorrect'), 1)
                self.assertEqual(events(d)[0][3][2], 0)  # Completion stamp never regranted.
                self.assertEqual((d.call('p10SerialHi', 3), d.call('p10SerialLo', 3)), first)
                self.assertEqual(txn(d, 3, 48, 2), 23)
                self.assertEqual(txn(d, 4, 48, 1), 25)
                self.assertEqual(d.p['p10EventCount'], 0)
                self.assertEqual(txn(d, 9), 16)
                self.assertEqual(txn(d, 2), 17)
                check(self, h, d)
                self.assertEqual((owners(h), unrelated(h)), old)

    def test_07_retired_aggregate_and_legacy_publishers_cannot_duplicate_originals(self):
        for source in (False, True):
            with self.subTest(source=source):
                h, d = ready(source, card=True)
                p, q, p09 = [h.vm.objects[n] for n in ('p03State', 'p04State', 'p09State')]
                before, old, card = history(d), unrelated(h), card_words(p09)
                for obj in OWNED:
                    for verb in range(10):
                        for noun, target in ((obj, 0), (25, obj)):
                            self.assertEqual(h.call('hostActNow', verb, noun, target), 0)
                            self.assertEqual(h.call('uiHostAct', verb, noun, target), 0)
                            self.assertEqual(h.call('bridgeActAtArrival', verb, noun, target), 0)
                            self.assertEqual(p.call('bDispatch', h, verb, noun, target), 1)
                            self.assertEqual(p09.call('h9Dispatch', verb, noun, target), 1)
                    self.assertEqual(p.call('bAppend', obj), 1)
                    self.assertEqual(p.call('b8Append', obj), 1)
                    self.assertEqual(h.call('uiInventoryAdd', obj), 0)
                    self.assertEqual(h.call('uiInventoryRemove', obj), 0)
                    for args in ((obj, 25, 24), (25, obj, 24), (24, 25, obj)):
                        self.assertEqual(h.call('uiInventoryCombine', *args), 0)
                # Stale legacy presentation callback is cancellation-only.
                p.p['bPendingObject'] = 35
                self.assertEqual(p.call('bPresented', h, 1, 0), 0)
                self.assertEqual(p.p['bPendingObject'], 0)
                self.assertEqual((p.call('bHeld', h, 35), p.call('bReachable', h, 35),
                                  q.call('qHeld', h, 35)), (0, 0, 0))
                for publish in (lambda: p.call('bInventory', h), lambda: q.call('qInventory', h),
                                lambda: h.call('p02HostInventory'),
                                lambda: h.vm.objects['p06State'].call('h6Inventory')):
                    self.assertEqual(publish(), 1)
                    check(self, h, d)
                    self.assertEqual((history(d), unrelated(h), card_words(p09)), (before, old, card))
                    # A normal repeated publication must not collapse the last
                    # page or move a selected held original or either late owner.
                    h.p.update(uiInventoryPage=h.p['uiInventoryPages'] - 1,
                               uiNounA=412, uiVerb=7, uiFocus=3)
                    published = ui(h), tuple(d.arrays['h10S']), p09.call('h9CardReservation', 399)
                    self.assertEqual(publish(), 1)
                    self.assertEqual((ui(h), tuple(d.arrays['h10S']), p09.call('h9CardReservation', 399)), published)
                    check(self, h, d)
                self.assertEqual(h.call('uiInventoryCompact'), 0)
                check(self, h, d)

    def test_08_ui_selection_pages_and_noncue_ownership_are_separate(self):
        for source in (False, True):
            with self.subTest(source=source):
                h, d = ready(source, card=True)
                old, card = owners(h), card_words(h.vm.objects['p09State'])
                other = unrelated(h)
                h.p['uiInventoryPage'] = h.p['uiInventoryPages'] - 1
                page = h.p['uiInventoryPage']
                h.p.update(uiNounA=24, uiVerb=7, uiFocus=3)
                self.assertEqual(txn(d, 3, 48, 1), 24)
                self.assertEqual((h.p['uiNounA'], h.p['uiVerb'], h.p['uiFocus'], h.p['uiInventoryPage']), (24, 7, 3, page))
                h.p.update(uiNounA=48, uiVerb=7)
                self.assertEqual(txn(d, 4, 48, 0), 28)
                self.assertEqual((h.p['uiNounA'], h.p['uiVerb'], h.p['uiFocus'], h.p['uiInventoryPage']), (0, 0, 3, page))
                reservations = tuple(d.arrays['h10S'])
                self.assertEqual(txn(d, 5, 0), 30)
                self.assertEqual(tuple(d.arrays['h10S']), reservations)
                self.assertEqual(h.arrays['uiItems'][reservations[0]], 48)
                self.assertEqual((owners(h), unrelated(h), card_words(h.vm.objects['p09State'])), (old, other, card))
                check(self, h, d)

    def test_09_partial_and_completed_ordinary_save_restore_and_failure_recovery(self):
        for source in (False, True):
            with self.subTest(source=source):
                h, d = ready(source, card=True)
                self.assertEqual(txn(d, 3, 48, 1), 24)
                self.assertEqual(txn(d, 4, 48, 0), 28)
                backend = Backend(h.vm)
                h.call('writeSave')
                self.assertIsNotNone(backend.saved)
                partial, partial_history = copy.deepcopy(backend.saved), history(d)
                load(h, backend, partial)
                self.assertEqual(history(d), partial_history)
                self.assertEqual(d.p['p10ContextValid'], 0)
                self.assertEqual(tuple(d.arrays['p10Lease']), (0,) * 8)
                self.assertEqual(tuple(d.arrays['p10Held']), (0,) * 415)
                self.assertEqual(txn(d, 2), -1)
                context(h, d)
                for slot, obj in ((1, 413), (2, 50)):
                    self.assertEqual(txn(d, 3, obj, slot + 1), 24)
                    self.assertEqual(txn(d, 4, obj, slot), 28)
                self.assertEqual(d.call('p10Ready'), 1)
                h.call('writeSave')
                completed, complete_history = copy.deepcopy(backend.saved), history(d)
                self.assertNotEqual(completed, partial)
                for _ in range(2):
                    load(h, backend, completed)
                    self.assertEqual(history(d), complete_history)
                    check(self, h, d)
                load(h, backend, partial)
                self.assertEqual(history(d), partial_history)
                self.assertEqual(d.call('p10Ready'), 0)
                check(self, h, d)
                backend.save_result = 0
                saved = copy.deepcopy(backend.saved)
                h.call('writeSave')
                self.assertEqual(backend.saved, saved)
                backend.restore_result = 0
                h.vm.event_queue = [{}]
                try:
                    h.call('readSave')
                finally:
                    h.vm.event_queue = None
                self.assertEqual(history(d), partial_history)
                backend.restore_result = 1
                load(h, backend, completed)
                check(self, h, d)
                self.assertIn(('save', 1), backend.operations)
                self.assertIn(('save', 0), backend.operations)
                self.assertIn(('restore', 0), backend.operations)
                self.assertIn(('restore', 1), backend.operations)

    def test_10_corrupt_ordinary_restore_is_rejected_before_repair_and_good_save_recovers(self):
        for source in (False, True):
            h, d = ready(source, card=True)
            self.assertEqual(txn(d, 3, 48, 1), 24)
            self.assertEqual(txn(d, 4, 48, 0), 28)
            self.assertEqual(txn(d, 3, 414, 2), 24)
            self.assertEqual(txn(d, 4, 414, 1), 28)
            backend = Backend(h.vm)
            h.call('writeSave')
            self.assertIsNotNone(backend.saved)
            good, good_history = copy.deepcopy(backend.saved), history(d)
            live = h.vm.snapshot()  # Current session after SaveGame returns.
            for kind in ('missing', 'duplicate', 'slot_mismatch', 'selected_installed',
                         'rack_mismatch', 'high_id', 'legacy_owner', 'event_cursor',
                         'paper_double_projection', 'noncontiguous_empty_paper',
                         'ceramic_double_projection', 'forged_first_restoration', 'unearned_order'):
                with self.subTest(source=source, kind=kind):
                    h.vm.restore(copy.deepcopy(good))
                    held_slot, installed_slot = d.arrays['h10S'][1], d.arrays['h10S'][0]
                    if kind == 'missing':
                        h.arrays['uiItems'][held_slot] = 0
                    elif kind == 'duplicate':
                        h.arrays['uiItems'][installed_slot] = 49
                    elif kind == 'slot_mismatch':
                        d.arrays['h10S'][1] = installed_slot
                    elif kind == 'selected_installed':
                        h.p['uiNounA'] = 48
                    elif kind == 'rack_mismatch':
                        d.arrays['h10R'][0] = 49
                    elif kind == 'high_id':
                        h.arrays['uiItems'][held_slot] = 415
                    elif kind == 'legacy_owner':
                        h.vm.objects['p04State'].arrays['qSlots'][0] = 412
                    elif kind == 'event_cursor':
                        d.arrays['h10M'][4] -= 1
                    elif kind == 'ceramic_double_projection':
                        d.arrays['p10Held'][48] = 1
                    elif kind == 'forged_first_restoration':
                        d.p['p10RestoredHi'] = d.p['p10PlanReceipt1Hi']
                        d.p['p10RestoredLo'] = d.p['p10PlanReceipt1Lo']
                    elif kind == 'unearned_order':
                        d.p['p10KnowOrder'] = 1
                    elif kind == 'paper_double_projection':
                        # Paper originals belong to p10InventoryAt, never the
                        # external p10Held projection, even when genuinely held.
                        d.arrays['p10Held'][412] = 1
                    elif kind == 'noncontiguous_empty_paper':
                        # Paper 414 is installed, leaving its reserved UI cell
                        # zero. Moving that reservation to another unique zero
                        # must not pass as an equivalent inventory layout.
                        extent = h.p['uiInventoryExtent']
                        self.assertLess(extent, 64)
                        self.assertEqual(h.arrays['uiItems'][extent], 0)
                        self.assertEqual(h.arrays['uiItems'][d.arrays['h10S'][5]], 0)
                        d.arrays['h10S'][5] = extent
                        h.p['uiInventoryExtent'] = extent + 1
                        h.p['uiInventoryPages'] = (extent + 8) // 8
                    bad = h.vm.snapshot()
                    bad_items = tuple(h.arrays['uiItems'])
                    before_ops = len(backend.operations)
                    h.call('writeSave')
                    self.assertEqual(len(backend.operations), before_ops)
                    self.assertEqual(tuple(h.arrays['uiItems']), bad_items)
                    h.vm.restore(copy.deepcopy(live))
                    load(h, backend, bad)
                    self.assertEqual(d.arrays['h10M'][1], 0)
                    self.assertEqual(h.p['uiFailure'], 10)
                    self.assertEqual(d.call('h10Save'), 0)
                    self.assertEqual(d.call('h10Proj'), 0)
                    self.assertEqual(tuple(h.arrays['uiItems']), bad_items)
                    self.assertEqual(txn(d, 2), -1)
                    load(h, backend, good)
                    self.assertEqual(history(d), good_history)
                    self.assertEqual(h.p['uiFailure'], 0)
                    check(self, h, d)

    def test_11_bad_event_transaction_rolls_back_and_bounds_never_touch_legacy_arrays(self):
        for source in (False, True):
            with self.subTest(source=source):
                h, d = ready(source)
                before = history(d), gate(d), ui(h), owners(h)
                fired = []

                def corrupt_result(obj, name, args, result):
                    if obj.name == 'p10State' and name == 'p10Write' and result == 24:
                        obj.arrays['p10EventArgs'][1] = 9
                        fired.append(name)

                h.vm.after_actual_call = corrupt_result
                try:
                    self.assertEqual(txn(d, 3, 48, 1), -1)
                finally:
                    h.vm.after_actual_call = None
                self.assertEqual(fired, ['p10Write'])
                self.assertEqual((history(d), gate(d), ui(h), owners(h)), before)
                self.assertEqual(txn(d, 3, 48, 1), 24)
                check(self, h, d)
                clean = h.vm.snapshot()
                old = owners(h)
                for index, obj in ((-32768, 48), (-1, 48), (64, 48), (32767, 48),
                                   (0, -1), (0, 35), (0, 95), (0, 410), (0, 411),
                                   (0, 415), (0, 32767)):
                    view = ui(h)
                    self.assertEqual(h.call('h10UI', index, obj), 0)
                    self.assertEqual(ui(h), view)
                    self.assertEqual(owners(h), old)
                for op in (-32768, -1, 0, 10, 32767):
                    self.assertEqual(txn(d, op), -1)
                # A real bounded reservation failure, with no request to repair
                # invalid storage or index any legacy object-ID array.
                for slot in d.arrays['h10S']:
                    h.arrays['uiItems'][slot] = 0
                for i in range(6):
                    d.arrays['h10S'][i] = -1
                h.p['uiInventoryExtent'] = 64
                h.p['uiInventoryPages'] = 8
                view = ui(h), gate(d), owners(h)
                self.assertEqual(d.call('h10Proj'), 0)
                self.assertEqual((ui(h), gate(d), owners(h)), view)
                h.vm.restore(copy.deepcopy(clean))
                check(self, h, d)


if __name__ == '__main__':
    unittest.main(verbosity=2)
