#!/usr/bin/env python3
"""Emitted P14 handoff checks with explicit completed-ancestor fixtures.

Acquire, context, matching, domain validation, original-item checks and history
copy/validation execute the compiled methods. Earlier campaign facts, original
ownership, actor rooms and contest provenance are fixture inputs. This is not
native gameplay, save, presentation, audio or campaign acceptance.
"""
import argparse
import json

from presentation_vm import PresentationVM


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


def run(build=None):
    cases = [valid_tone_case(tone, build) for tone in (0, 1, 2, 3)]
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
            'scope': 'Actual emitted P14 Acquire/Ctx/Match, start/domain, item/date/win context and history checks; completed-ancestor and host-ownership fixture inputs explicit',
            'limits': 'No native saves, input, pixels, audio, dates typed through UI, campaign progression or acceptance',
            'native_acceptance': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build')
    args = parser.parse_args()
    print(json.dumps(run(args.build), indent=2))
