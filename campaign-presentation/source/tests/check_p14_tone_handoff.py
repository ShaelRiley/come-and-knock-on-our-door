#!/usr/bin/env python3
"""Emitted P14 handoff checks with explicit completed-ancestor fixtures.

Acquire, its first rendered interface, context, matching, domain validation,
original-item checks and history copy/validation execute the compiled methods.
Earlier campaign facts, original ownership, actor rooms and contest provenance
are fixture inputs. This is not native gameplay, save, presentation, audio or
campaign acceptance.
"""
import argparse
import hashlib
import json
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]

from presentation_vm import PresentationVM, base


class HandoffFixture(PresentationVM):
    def __init__(self, tone=0, build=None):
        super().__init__(build)
        self.base_ready = self.all_here = self.pencil_held = True
        self.card_held = self.card_owner_valid = self.physical_ready = True
        self.facts = [1] * 28
        self.win_lo = [1, 2, 3, 4]
        self.board_room = 4
        self.boundary = [0] * 2046
        self.h.p.update(location=4, onApron=0, motionPhase=0,
                        uiInventoryExtent=2, p02Revision=1)
        self.arrays(0)['uiItems'][0:2] = [25, 399]
        self.arrays(987)['p06Words'][4] = tone
        date = '2026-10-16'
        self.arrays(996)['h14Date'][0:len(date) + 1] = [len(date), *map(ord, date)]

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        # Prior campaign admission is explicit, not earned by this fixture.
        if key == (996, 'h14Base'):
            return int(self.base_ready)
        if key == (996, 'h14Fact'):
            return self.facts[args[0]]
        if key == (996, 'h14RawRoom'):
            return 4
        if key == (985, 'hVCSession'):
            return 0
        if key == (985, 'hVCWinningHi'):
            return 0
        if key == (985, 'hVCWinningLo'):
            return self.win_lo[args[0] - 1]
        if key == (995, 'h13Location'):
            assert list(args) == [433]
            return self.board_room
        if key == (995, 'h13AllHere'):
            return int(self.all_here)
        if key == (995, 'h13ReadyPhysical'):
            return int(self.physical_ready)
        if key == (995, 'h13BoundaryCount'):
            return len(self.boundary)
        if key == (995, 'h13BoundaryWord'):
            return self.boundary[args[0]]
        if key == (990, 'h9CardHeld'):
            assert list(args) == [399]
            return int(self.card_held and self.card_owner_valid)
        if key == (990, 'h9OwnershipValid'):
            return int(self.card_owner_valid)
        if key == (0, 'campaignHeld'):
            assert list(args) == [25]
            return int(self.pencil_held)
        return super().call(obj, name, args)

    def execute(self, obj, module, name, pc, args):
        # Domain emission still executes, but its unrelated music/Foley
        # notifications cannot turn this fixture into audio acceptance.
        if module.number in (944, 946):
            return 1
        return super().execute(obj, module, name, pc, args)

    def procedure(self, module, index, args):
        # This handoff reaches real cross-script bank/history procedures that
        # the smaller interface fixtures never invoke.
        emitted = self.modules[module]
        return self.execute(self.h, emitted, 'export' + str(index),
                            emitted.layout['exports'][index], args)

    def acquire(self):
        return self.call(self.instance(996), 'h14Acquire')

    def committed(self):
        p = self.instance(996)
        return (p.p['p14RevisionHi'], p.p['p14RevisionLo'],
                self.call(p, 'p14Present', (1,)), self.arrays(996)['h14Owner'][0])


def valid_tone_case(tone, build=None):
    v = HandoffFixture(tone, build)
    p = v.instance(996)
    p06_before = list(v.arrays(987)['p06Words'])
    assert v.acquire() == 1, ('P14 must accept optional tone', tone)
    normalized = 0 if tone == 0 else tone - 1
    assert p.p['p14InputTone'] == p.p['p14Tone'] == normalized
    assert v.arrays(996)['h14Facts'][30] == normalized
    assert v.call(p, 'p14Present', (1,)) == 1
    assert v.arrays(996)['h14Owner'][0:3] == [1, 1, 4]
    assert v.call(p, 'p14Validate') == v.call(p, 'h14Valid') == 1
    assert v.call(p, 'h14Match') == 1
    assert list(v.arrays(987)['p06Words']) == p06_before, 'P14 must not invent a P06 choice'
    # A different effective ending tone must invalidate the current context.
    v.arrays(987)['p06Words'][4] = 2 if normalized == 0 else 1
    assert v.call(p, 'h14Match') == 0
    return 'actual Acquire/Ctx/Match tone' + str(tone) + ' maps' + str(normalized)


def rejected_case(label, mutate, build=None, tone=0):
    v = HandoffFixture(tone, build)
    mutate(v)
    before = v.committed()
    assert v.acquire() == 0, label
    assert v.committed() == before == (0, 0, 0, 0), label + ' must not commit or take ownership'
    return label


def rendered_handoff_case(build=None):
    v = HandoffFixture(0, build)
    # The complete emitted renderer and its repeated strict owner checks need
    # more instructions than the smaller domain-only cases. Keep a finite cap.
    v.budget = 20000000
    p = v.instance(996)
    inventory = list(v.arrays(0)['uiItems'])
    extent = v.h.p['uiInventoryExtent']
    assert v.acquire() == 1
    committed = v.committed()
    # Match native ordering: Acquire is followed by uiRender, which builds the
    # real controls. Do not stub labels, controls, renderer or TextSize, and do
    # not pre-build a second control frame before rendering this one.
    v.call(v.h, 'uiRender')
    assert v.h.p['uiFailure'] == 0, 'First P14 world frame must fit the interface'
    arrays = v.arrays(0)
    controls = {arrays['uiPayloads'][i]: base.read_string(arrays['uiLabels'][i])
                for i in range(v.h.p['uiControlCount'])
                if arrays['uiActions'][i] == 3}
    for obj, short, full in (
        (25, 'PENCL', 'Original grease pencil'),
        (399, 'TERMS', 'Original renewal and repair card'),
    ):
        assert controls[obj] == short, 'Inventory control must keep its compact label'
        assert base.read_string(v.call(v.h, 'uiHostShortLabel', (obj,))) == short
        assert base.read_string(v.call(v.h, 'uiHostItemLabel', (obj,))) == full
        assert v.call(p, 'h14Owns', (obj,)) == 1
        assert v.call(p, 'h14Held', (obj,)) == 1
        assert v.call(p, 'h14Location', (obj,)) == 10
    # Promise cards are opened through the board menu. Acquire must not invent
    # dense inventory cells for them or disturb either original's existing cell.
    assert list(arrays['uiItems']) == inventory
    assert v.h.p['uiInventoryExtent'] == extent
    assert not set(range(435, 443)).intersection(inventory)
    assert v.call(p, 'p14Validate') == v.call(p, 'h14Valid') == 1
    assert v.call(p, 'h14Match') == 1
    assert v.committed() == committed
    assert v.call(p, 'h14Save') == 1, 'Valid post-acquisition state must remain saveable'
    assert v.call(p, 'p14Validate') == v.call(p, 'h14Valid') == 1
    assert v.committed() == committed, 'Rendering/save preparation must not commit progress'
    return 'actual Acquire then first uiRender preserves compact originals, full names, ownership and save gate'


def run(build=None):
    cases = [valid_tone_case(tone, build) for tone in (0, 1, 2, 3)]
    cases.append(rendered_handoff_case(build))
    for raw in (-1, 4):
        cases.append(rejected_case('nonzero invalid tone' + str(raw) + ' rejected',
                                   lambda v: None, build, tone=raw))
    boundaries = [
        ('ancestor admission unavailable', lambda v: setattr(v, 'base_ready', False)),
        ('missing actual companion', lambda v: setattr(v, 'all_here', False)),
        ('moving player', lambda v: v.h.p.update(motionPhase=1)),
        ('no accepted date', lambda v: v.arrays(996)['h14Date'].__setitem__(0, 0)),
        ('original pencil not held', lambda v: setattr(v, 'pencil_held', False)),
        ('original terms not held', lambda v: setattr(v, 'card_held', False)),
        ('terms ownership invalid', lambda v: setattr(v, 'card_owner_valid', False)),
        ('pencil absent from dense inventory', lambda v: v.arrays(0)['uiItems'].__setitem__(0, 0)),
        ('terms absent from dense inventory', lambda v: v.arrays(0)['uiItems'].__setitem__(1, 0)),
        ('fourth actual win provenance absent', lambda v: v.win_lo.__setitem__(3, 0)),
        ('required predecessor fact absent', lambda v: v.facts.__setitem__(17, 0)),
        ('board not physically delivered', lambda v: setattr(v, 'board_room', 1)),
        ('wrong entry room', lambda v: v.h.p.update(location=1)),
    ]
    for label, mutate in boundaries:
        cases.append(rejected_case(label, mutate, build))

    v = HandoffFixture(0, build)
    assert v.acquire() == 1
    before = v.committed()
    v.win_lo[3] = 99
    assert v.call(v.instance(996), 'h14Ctx') == 0
    assert v.call(v.instance(996), 'h14Match') == 0
    assert v.committed() == before
    cases.append('changed winning provenance rejects rebuilt context without new commit')

    for label, mutate in (
        ('changed predecessor history', lambda v: v.boundary.__setitem__(100, 1)),
        ('lost predecessor ownership', lambda v: setattr(v, 'card_owner_valid', False)),
        ('lost physical readiness', lambda v: setattr(v, 'physical_ready', False)),
    ):
        v = HandoffFixture(0, build)
        assert v.acquire() == 1
        before = v.committed()
        mutate(v)
        assert v.call(v.instance(996), 'h14Match') == 0
        assert v.committed() == before
        cases.append(label + ' still rejects Match')
    return {'status': 'PASS_NOT_NATIVE', 'case_count': len(cases), 'cases': cases,
            'scope': 'Actual emitted P14 Acquire/first uiRender/Ctx/Match, inventory labels, ownership/save gate, start/domain, item/date/win context and history checks; completed-ancestor and host-ownership fixture inputs explicit',
            'limits': 'No native saves, input, pixels, audio, dates typed through UI, campaign progression or acceptance',
            'native_acceptance': False}


class StoredFixture(HandoffFixture):
    def __init__(self, build=None):
        super().__init__(0, build)
        self.budget = 30000000
        self.events = []
        self.context_facts = [4,0,1,1,1,1,1,1,1,1,1,0,1,1,4,4,1,1,1,0,1,
                              4,4,4,4,4,4,4,0,0,0,0,0,0,0,0]
        self.arrays(995)['h13Lease'][0:2] = [1, 1]
        p = self.instance(995)
        assert self.call(p, 'p13Init') == 1
        serial = 0
        def stamp(slot):
            nonlocal serial
            serial += 1
            assert self.call(p, 'p13SetSerial', (slot, 0, serial)) == 1
        for slot in range(1, 6):
            stamp(slot)
        def reader(source):
            stamp(source + 18)
            start = self.call(p, 'p13ReceiptBase', (source,))
            for slot in range(start, start + self.call(p, 'p13Capacity', (source,))):
                stamp(slot)
        reader(10)
        stamp(6)
        stamp(7)
        reader(11)
        stamp(8)
        stamp(9)
        reader(12)
        stamp(10)
        stamp(15)
        stamp(16)
        self.call(p, 'p13SetSerial', (0, 0, serial))
        assert self.call(p, 'p13Validate') == 1
        assert self.call(p, 'h13Ctx') == 1
        assert self.call(p, 'p13ValidateContext') == 1
        self.events.clear()

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        if key in ((995, 'h13BoundaryCount'), (995, 'h13BoundaryWord')):
            return PresentationVM.call(self, obj, name, args)
        if key in ((995, 'h13Active'), (995, 'h13Valid')):
            return 1  # Completed physical/historical admission only.
        if key == (995, 'h13Fact'):
            return self.context_facts[args[0]]
        if key in ((995, 'h13Stored'), (996, 'h14Stored'), (995, 'h13Ctx'),
                   (995, 'p13AcknowledgeAutosave')):
            self.events.append({'module': key[0], 'method': name, 'args': list(args)})
        return super().call(obj, name, args)

    def boundary_words(self):
        return [self.call(self.instance(995), 'h13BoundaryWord', (i,)) for i in range(2046)]


def post_save_history(build=None, reference=False):
    cases = []
    for success in (0, 1):
        v = StoredFixture(build)
        p, owner = v.instance(995), v.instance(996)
        assert v.acquire() == 1
        assert v.call(owner, 'h14HistoryValid') == v.call(owner, 'h14Valid') == 1
        assert v.call(p, 'p13Present', (17,)) == 0
        before = v.boundary_words()
        # SaveGame is a mocked storage boundary. This is its in-memory test
        # snapshot, not an SCI save and never imported into a native runtime.
        disk = v.snapshot()
        v.events.clear()
        v.events.append({'kernel': 'SaveGame', 'return': success})
        v.call(owner, 'h14Stored', (success,))
        returned = v.call(p, 'h13Stored', (success,))
        assert returned == success, 'Failed storage must retain its original zero return'
        after = v.boundary_words()
        live_history = v.call(owner, 'h14HistoryValid')
        changed = [{'index': i, 'before': a, 'after': b}
                   for i, (a, b) in enumerate(zip(before, after)) if a != b]
        if reference and success:
            assert live_history == 0 and changed
            assert {r['index'] for r in changed} == {1937, 1971}
            assert v.call(p, 'p13Present', (17,)) == 1
        else:
            assert after == before and live_history == 1
            assert v.call(p, 'p13Present', (17,)) == 0
            if success:
                assert not any(e.get('method') in ('h13Ctx', 'p13AcknowledgeAutosave') for e in v.events)
        events = list(v.events)
        v.restore(disk)
        assert v.boundary_words() == before
        assert v.call(owner, 'h14HistoryValid') == v.call(owner, 'h14Valid') == 1
        assert v.call(p, 'p13Present', (17,)) == 0
        cases.append({'case': 'post-P14 storage result' + str(success), 'callback_return': returned,
                      'changed_boundary_words': changed, 'live_history_valid': live_history,
                      'restored_mock_disk_history_valid': 1, 'events': events})
    # Before transfer, all three existing successful acknowledgments retain
    # their domain validators. Failed storage never creates an ACK; a second
    # successful callback remains idempotent with no duplicate serial commit.
    for cue in (1, 2, 3):
        for success in (0, 1):
            v = StoredFixture(build)
            p = v.instance(995)
            v.call(p, 'p13SetSerial', (cue + 14, 0, 0))
            assert v.call(p, 'p13Validate') == 1
            before = v.boundary_words()
            v.call(p, 'h13Stored', (success,))
            assert v.call(p, 'p13Present', (cue + 14,)) == success
            assert v.call(p, 'p13Validate') == 1
            if success == 0:
                assert v.boundary_words() == before
            else:
                assert v.boundary_words() != before
                stable = v.boundary_words()
                v.call(p, 'h13Stored', (1,))
                assert v.boundary_words() == stable
            cases.append({'case': 'pre-P14 cue' + str(cue) + '/success' + str(success),
                          'ack_present': success, 'domain_validate': 1})
    return {'status': 'REFERENCE_POST_SAVE_HISTORY_DEFECT_REPRODUCED_NOT_NATIVE' if reference else 'PASS_EMITTED_NOT_NATIVE',
            'case_count': len(cases), 'cases': cases, 'native_acceptance': False,
            'compile_receipt_sha256': hashlib.sha256((Path(build) if build else SOURCE / 'build/coherent').joinpath('compile-receipt.json').read_bytes()).hexdigest(),
            'scope': 'Actual emitted h13Stored/Ctx/p13Context/ACK/serial/domain validation, P14 Acquire/history copy/strict history and2046actual boundary-word queries. Ancestor facts/physical readiness are fixtures; SaveGame ordering is modeled from actual Main source.',
            'limits': 'Ledger serials are explicit valid unit-fixture data, not earned campaign state. Snapshot/restore is VM test serialization, never a native save. No GUI,input,source/runtime mutation, native acceptance or claim of a fixed build.'}


class FeedbackFixture(HandoffFixture):
    def __init__(self, build=None):
        super().__init__(0, build)
        self.budget = 30000000
        self.status_events = []
        self.ctx_events = []
        self.open_events = []
        self.reject_refresh = False

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        if key == (996, 'p14Status'):
            self.status_events.append(list(args))
        if key == (996, 'h14Open'):
            self.open_events.append({'source': args[0], 'line0': super().call(obj, 'p14Line', (0,))})
        if key == (996, 'h14Ctx'):
            if self.reject_refresh and self.status_events:
                # Explicit epoch-exhaustion fixture: actual Ctx rejects before
                # clearing, while the sealed prior context can still Match.
                obj.p['p14Epoch'] = 32767
            before = (obj.p['p14LineCount'], list(self.arrays(996)['p14Lines']))
            value = super().call(obj, name, args)
            self.ctx_events.append({'before': before, 'after': (obj.p['p14LineCount'], list(self.arrays(996)['p14Lines'])),
                                    'returned': value, 'actual_match_after': super().call(obj, 'h14Match')})
            return value
        return super().call(obj, name, args)

    def complete_source(self, source):
        p = self.instance(996)
        self.call(p, 'p14Begin', (source,))
        assert p.p['p14PresentationSource'] == source
        hi = self.call(p, 'p14SerialHi', (source + 16,))
        lo = self.call(p, 'p14SerialLo', (source + 16,))
        self.call(p, 'p14Acknowledge', (source, hi, lo, p.p['p14Epoch'], self.call(p, 'p14SourceRecord', (source,)), 0, 0))
        assert self.call(p, 'p14Complete', (source,)) == 1

    def pin_menu(self):
        p = self.instance(996)
        assert self.call(p, 'h14Menu', (435,)) == 1
        assert self.call(p, 'h14Ctx') == 1
        self.h.p['uiPage'] = 9
        assert self.call(self.h, 'p05ChoiceValue', (9, 0)) == 140
        for phase in (0, 2, 1):
            assert self.call(p, 'h14MenuFrame', (phase,)) == 1
        assert self.arrays(996)['h14MenuPaint'][0] == 3
        self.status_events.clear(); self.ctx_events.clear(); self.open_events.clear()

def choice_feedback(build=None, reference=False):
    rows = []
    for approved, reject, repeat in ((False, False, False), (True, False, False), (True, True, False), (True, False, True)):
        v = FeedbackFixture(build)
        p = v.instance(996)
        assert v.acquire() == 1
        if approved:
            v.complete_source(2)
        if repeat:
            v.call(p, 'p14PinCard', (0,))
            assert v.call(p, 'p14Present', (9,)) == 1
        v.pin_menu()
        v.reject_refresh = reject
        revision = p.p['p14RevisionLo']
        assert v.call(p, 'h14Choice', (256, 140)) == 1
        line = 0 if repeat else (34 if approved else 35)
        assert any(event[1] == line for event in v.status_events), v.status_events
        assert v.call(p, 'p14Present', (9,)) == int(approved)
        expected_commit = int(approved and not repeat)
        assert p.p['p14RevisionLo'] == revision + expected_commit
        assert v.call(p, 'h14HistoryValid') == v.call(p, 'h14Valid') == 1
        if line and not reject:
            assert v.ctx_events[-1]['before'][0] == 1 and v.ctx_events[-1]['after'][0] == 0
        if reject:
            assert v.ctx_events[-1]['returned'] == 0
            assert v.ctx_events[-1]['actual_match_after'] == 1
            assert v.call(p, 'p14Line', (0,)) == 34
            if reference:
                assert v.open_events == [{'source': 0, 'line0': 34}]
                assert v.arrays(996)['h14Reader'][0] == 1
                assert v.arrays(996)['h14Reader'][1] == 1633
            else:
                assert not v.open_events and v.arrays(996)['h14Reader'][0] == 0
                assert v.h.p['uiPanel'] == v.h.p['uiBackPanel'] == 0
        elif reference or repeat:
            assert not v.open_events and v.call(p, 'p14Line', (0,)) == 0
            assert v.arrays(996)['h14Reader'][0] == 0
        else:
            assert v.open_events == [{'source': 0, 'line0': line}]
            assert v.arrays(996)['h14Reader'][0] == 1
            assert v.arrays(996)['h14Reader'][1] == v.call(p, 'h14Record', (line,))
            assert v.arrays(996)['h14Reader'][1] == (1633 if approved else 1634)
            assert v.arrays(996)['h14Reader'][2] == 0
        rows.append({'approved_fixture': approved, 'reject_refresh_fixture': reject, 'repeat_pin': repeat, 'domain_status_events': v.status_events,
                     'ctx_clear_events': v.ctx_events, 'open_events': v.open_events,
                     'pin_serial_present': int(approved), 'revision_change': expected_commit,
                     'reader_document': v.arrays(996)['h14Reader'][1],
                     'strict_history_valid': 1})
    return {'status': 'REFERENCE_FEEDBACK_CLEAR_DEFECT_REPRODUCED_NOT_NATIVE' if reference else 'PASS_EMITTED_NOT_NATIVE',
            'case_count': len(rows), 'cases': rows, 'native_acceptance': False,
            'compile_receipt_sha256': hashlib.sha256((Path(build) if build else SOURCE / 'build/coherent').joinpath('compile-receipt.json').read_bytes()).hexdigest(),
            'scope': 'Actual emitted Acquire, p14Begin/Acknowledge approval, menu construction/three phase menu witness, h14Choice, p14PinCard/Status, h14Ctx/p14Context/Invalidate/Clear and strict owner/history predicates. Earlier campaign facts, ownership and actor rooms are explicit fixtures. No native input/progression/save/reader evidence.'}


class RawOriginalsFixture(HandoffFixture):
    """Actual P14/raw-original predicates with explicit earlier domain facts."""
    def __init__(self, build=None):
        super().__init__(0, build)
        self.budget = 60000000
        self.route_admissions = False
        self.route_returns = []
        self.h.p.update(p02PlanAgreed=1, p03=self.instance(983),
                        p04=self.instance(984), p05=self.instance(985),
                        p06=self.instance(987), p08=self.instance(989),
                        p09=self.instance(990))
        self.instance(985).p['hContest'] = self.instance(986)
        self.instance(989).p['h8Host'] = self.h
        self.instance(990).p.update(h9Host=self.h, p09Ready=1)
        self.arrays(990)['h9CardAdmission'][0] = 1
        self.arrays(990)['h9CardSlot'][0] = 1
        q = self.instance(984)
        q.p.update(qInventoryStarted=1, qExtent=1, qLastRoom=4)
        self.arrays(984)['qSlots'][0] = 25
        self.arrays(984)['qReserve'][:] = [-1] * 63

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        if key == (990, 'p09Validate'):
            # Prior P09 domain is admitted, but actual ownership singleton,
            # old-map exclusions, raw card count and reserved slot are checked.
            return 1
        if key in ((990, 'h9OwnershipValid'), (990, 'h9CardHeld')):
            return PresentationVM.call(self, obj, name, args)
        if key == (0, 'campaignHeld') and self.arrays(996)['h14Owner'][0]:
            return PresentationVM.call(self, obj, name, args)
        if self.route_admissions:
            admitted = {
                (992, 'h10Save'): 1, (989, 'h8RouteSaveValid'): 1,
                (989, 'h8Barrier'): 0, (989, 'h8ActionBarrier'): 0,
                (989, 'h8SupportedHistory'): 1,
                (989, 'h8PublishersReady'): 1, (989, 'h8OwnersValid'): 1,
                (989, 'h8Preparations'): 8191, (989, 'h8ContestBusy'): 0,
                (989, 'p08SetContext'): 1, (989, 'p08ValidateCurrent'): 0,
            }
            if key in admitted:
                return admitted[key]
        result = super().call(obj, name, args)
        if key in ((989, 'h8InventoryRawValid'), (989, 'h8ProjectContext'),
                   (989, 'h8Context'), (989, 'h8SaveReady')):
            self.route_returns.append((name, result))
        return result


def raw_originals(build=None, reference=False):
    """The existing raw map must retain genuine originals after legal handoff."""
    from copy import copy
    v = RawOriginalsFixture(build)
    p, s, q, card = (v.instance(n) for n in (996, 989, 984, 990))
    assert v.acquire() == 1
    raw = list(v.arrays(0)['uiItems'])
    cases = []

    def complete(source):
        v.call(p, 'p14Begin', (source,))
        assert p.p['p14PresentationSource'] == source
        hi = v.call(p, 'p14SerialHi', (source + 16,))
        lo = v.call(p, 'p14SerialLo', (source + 16,))
        rec = v.call(p, 'p14SourceRecord', (source,))
        v.call(p, 'p14Acknowledge', (source, hi, lo, p.p['p14Epoch'], rec, 0, 0))
        assert v.call(p, 'p14Complete', (source,))

    def boundary(label, expected_held):
        assert list(v.arrays(0)['uiItems']) == raw
        assert v.call(p, 'p14Validate') == v.call(p, 'h14Valid') == 1
        assert [v.call(v.h, 'campaignHeld', (obj,)) for obj in (25, 399)] == expected_held
        assert v.call(card, 'h9InventoryValid') == 1
        assert v.call(q, 'q8Valid') == v.call(q, 'qHeld', (v.h, 25)) == 1
        assert v.call(q, 'qFind', (25,)) == 0
        expected = int(not reference or expected_held == [1, 1])
        assert v.call(s, 'h8InventoryRawValid') == expected, label
        v.route_returns = []
        v.route_admissions = True
        try:
            assert v.call(s, 'h8SaveReady') == expected, label + ' actual Save chain'
        finally:
            v.route_admissions = False
        assert ('h8InventoryRawValid', expected) in v.route_returns
        assert ('h8ProjectContext', expected) in v.route_returns
        assert ('h8Context', expected) in v.route_returns
        assert list(v.arrays(0)['uiItems']) == raw
        cases.append(label + ': actual held semantics preserved; raw/card/pencil provenance and Save route checked')

    def reject(label, mutate, restore):
        mutate()
        try:
            assert v.call(s, 'h8InventoryRawValid') == 0, label
        finally:
            restore()
        cases.append(label + ' rejected')

    for person in range(8):
        complete(person + 2)
        v.call(p, 'p14PinCard', (person,))
        assert v.call(p, 'p14Present', (person + 9,))
    boundary('before terms signature', [1, 1])
    complete(20)
    v.call(p, 'p14PinSignature')
    assert v.call(p, 'p14Present', (2,))
    assert v.call(p, 'h14Ctx') == 1
    boundary('signed original terms retained', [1, 0])
    reject('wrong original399 reserved slot',
           lambda: v.arrays(990)['h9CardSlot'].__setitem__(0, 0),
           lambda: v.arrays(990)['h9CardSlot'].__setitem__(0, 1))
    reject('wrong canonical P09 owner',
           lambda: v.h.p.update(p09=v.instance(983)),
           lambda: v.h.p.update(p09=card))
    v.call(p, 'p14GivePencil')
    assert v.call(p, 'p14Present', (3,))
    assert v.call(p, 'h14Ctx') == 1
    boundary('original pencil loan retained', [0, 0])
    reject('missing P04 original25 slot',
           lambda: v.arrays(984)['qSlots'].__setitem__(0, 0),
           lambda: v.arrays(984)['qSlots'].__setitem__(0, 25))
    reject('invalid P04 reservation at occupied slot',
           lambda: v.arrays(984)['qReserve'].__setitem__(25, 0),
           lambda: v.arrays(984)['qReserve'].__setitem__(25, -1))
    reject('legacy original25 no longer held',
           lambda: v.h.p.update(p02PlanAgreed=0),
           lambda: v.h.p.update(p02PlanAgreed=1))
    reject('wrong canonical P04 owner',
           lambda: v.h.p.update(p04=v.instance(983)),
           lambda: v.h.p.update(p04=q))
    alias = copy(v.h)
    alias.p = dict(v.h.p)
    reject('noncanonical Main inventory host',
           lambda: s.p.update(h8Host=alias),
           lambda: s.p.update(h8Host=v.h))
    for source in (21, 22, 23):
        complete(source)
    v.call(p, 'p14CompleteCommitments')
    assert v.call(p, 'p14Ready')
    assert v.call(p, 'h14Ctx') == 1
    boundary('completed commitments before StartFinale', [1, 0])
    reject('changed frozen P13 history',
           lambda: v.boundary.__setitem__(100, 1),
           lambda: v.boundary.__setitem__(100, 0))
    reject('invalid P14 domain',
           lambda: p.p.update(p14Phase=99),
           lambda: p.p.update(p14Phase=0))
    reject('invalid P14 owner marker',
           lambda: v.arrays(996)['h14Owner'].__setitem__(0, 2),
           lambda: v.arrays(996)['h14Owner'].__setitem__(0, 1))
    reject('duplicate retained original399',
           lambda: (v.h.p.update(uiInventoryExtent=3), v.arrays(0)['uiItems'].__setitem__(2, 399)),
           lambda: (v.arrays(0)['uiItems'].__setitem__(2, 0), v.h.p.update(uiInventoryExtent=2)))
    reject('nonzero raw entry beyond extent',
           lambda: v.h.p.update(uiInventoryExtent=1),
           lambda: v.h.p.update(uiInventoryExtent=2))
    reject('forbidden retired original34',
           lambda: (v.h.p.update(uiInventoryExtent=3), v.arrays(0)['uiItems'].__setitem__(2, 34)),
           lambda: (v.arrays(0)['uiItems'].__setitem__(2, 0), v.h.p.update(uiInventoryExtent=2)))
    reject('unheld pinned promise435 is not a retained-original exception',
           lambda: (v.h.p.update(uiInventoryExtent=3), v.arrays(0)['uiItems'].__setitem__(2, 435)),
           lambda: (v.arrays(0)['uiItems'].__setitem__(2, 0), v.h.p.update(uiInventoryExtent=2)))
    assert v.call(p, 'p14Validate') == v.call(p, 'h14Valid') == 1
    assert list(v.arrays(0)['uiItems']) == raw
    return {'status': 'R9_REFERENCE_INCOMPATIBILITY' if reference else 'PASS_NOT_NATIVE',
            'case_count': len(cases), 'cases': cases,
            'scope': 'Actual emitted P14 domain/ownership/held methods, Main.campaignHeld and raw inventory checks, canonical P09 ownership/card count/slot, P04 original layout/find/held, and h8SaveReady->Context->ProjectContext. Earlier campaign predicates are explicit fixture inputs.',
            'limits': 'P09 domain validation and completed P13 physical/history facts are admitted; real P14, raw/held and retained-original provenance predicates are not. No native SaveGame, restore, pixels/audio or campaign acceptance.',
            'native_acceptance': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--post-save-history', action='store_true')
    mode.add_argument('--choice-feedback', action='store_true')
    mode.add_argument('--raw-originals', action='store_true')
    parser.add_argument('--reference', action='store_true', help='Diagnose original emitted defect; requires an explicit focused mode')
    args = parser.parse_args()
    if args.reference and not (args.post_save_history or args.choice_feedback or args.raw_originals):
        parser.error('--reference requires an explicit focused mode')
    report = (raw_originals(args.build, args.reference) if args.raw_originals else
              choice_feedback(args.build, args.reference) if args.choice_feedback else
              post_save_history(args.build, args.reference) if args.post_save_history else run(args.build))
    print(json.dumps(report, indent=2))
