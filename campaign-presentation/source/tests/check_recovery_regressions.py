#!/usr/bin/env python3
"""Emitted recovery regressions; explicit admission fixtures, never native proof.

The origin case runs the real strict P13 actor/route/cargo/delivery predicate.
Its already-validated predecessor and domain admissions are modeled. No fixture
earns campaign progress, supplies a native save, or validates the full ancestor.
"""
import argparse
import json
from presentation_vm import PresentationVM, S, base


class RecoveryFixture(PresentationVM):
    def __init__(self, build=None):
        super().__init__(build)
        self.delegate_context = 202
        self.delegations = []
        self.opened_topics = []
        self.history_ok = True
        self.ancestor_room_calls = 0
        self.ready = False
        self.ready_validation = None
        self.ready_validation_calls = 0

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        if key == (990, 'h9Active'):
            return 1
        if key == (990, 'h9Open'):
            self.opened_topics.append(args[0])
            return 1
        if key == (0, 'uiHostChoice'):
            self.delegations.append(tuple(args))
            self.h.p['uiChoiceContext'] = self.delegate_context
            return 1
        if key in {(994, 'h12Active'), (994, 'h12Handoff'), (994, 'h12Ctx')}:
            return 1
        if key in {(994, 'h12SuccessorHas'), (995, 'h13Has')}:
            return int(key == (995, 'h13Has') and self.ready_validation is not None)
        if key == (993, 'h11ReadMemo'):
            return 0
        if key == (995, 'h13Historical'):
            return self.history_ok
        if key == (995, 'p13Validate'):
            return 1
        if key == (994, 'h12SuccessorRoom'):
            self.ancestor_room_calls += 1
            i = (2, 8, 28, 85, 30, 54, 29).index(args[0])
            return self.arrays(995)['h13History'][88 + 12 * i]
        if self.ready_validation is not None:
            if key == (995, 'p13Ready'):
                return self.ready
            if key == (995, 'h13Valid'):
                self.ready_validation_calls += 1
                return self.ready_validation
            if key in {(995, 'h13ServeShown'), (995, 'h13SceneShown')}:
                return 1
        return super().call(obj, name, args)


def retained_menu(build, reference):
    v = RecoveryFixture(build)
    p = v.instance(990)
    p.p['h9Host'] = v.h
    v.h.p.update(uiPanel=2, uiChoiceContext=239, uiChoiceCount=2)
    a = v.arrays(0)
    a['uiChoiceIds'][0:2] = [104, 8]
    a['uiChoiceEnabled'][0:2] = [1, 1]
    assert v.call(p, 'h9Choice', (239, 104)) == 1
    restored = v.h.p['uiChoiceContext'] == 239
    if not reference:
        assert restored, 'Retained topic must retain the later menu route'
        assert v.call(p, 'h9Choice', (239, 8)) == 1
        assert v.opened_topics == [8], 'Next later topic must reach the later handler'
    assert v.delegations == [(202, 4)]
    # An intentional route into the earlier handler's other menu is preserved.
    v.h.p['uiChoiceContext'] = 239
    a['uiChoiceIds'][0] = 110
    v.delegate_context = 205
    assert v.call(p, 'h9Choice', (239, 110)) == 1
    assert v.h.p['uiChoiceContext'] == 205
    return {'retained_context_restored': restored, 'intentional_transition': 205}


def apron_menu(build, reference):
    v = RecoveryFixture(build)
    v.h.p.update(location=4, onApron=1, uiPanel=0, motionPhase=0)
    p = v.instance(994)
    assert v.call(p, 'h12Dispatch', (0, 410, 0)) == 1
    a = v.arrays(0)
    ids = list(a['uiChoiceIds'][:v.h.p['uiChoiceCount']])
    if not reference:
        assert v.h.p['uiPanel'] == 2 and v.h.p['uiChoiceContext'] == 252
        assert ids == [5, 6, 8], 'Audience-view menu must include the authored rehearsal'
    return {'menu_opened': v.h.p['uiPanel'] == 2, 'choice_ids': ids}


def renewal_label(build, reference):
    v = RecoveryFixture(build)
    v.h.p['p09'] = v.instance(990)
    long_label = base.read_string(v.call(v.h, 'uiHostItemLabel', (399,)))
    short_label = base.read_string(v.call(v.h, 'uiHostShortLabel', (399,)))
    if not reference:
        assert long_label == 'Renewal and repair card' and short_label == 'TERMS'
    return {'long_label': long_label, 'short_label': short_label}


def origin_fixture(build):
    v = RecoveryFixture(build)
    v.h.p['p02Revision'] = 2
    a = v.arrays(995)
    a['h13Lease'][0:2] = [1, 1]
    a['h13History'][0] = 2
    a['h13Cargo'][:] = [2, 3, 3, 1]
    for i, (obj, room) in enumerate(zip((2, 8, 28, 85, 30, 54, 29), (2, 1, 0, 3, 3, 3, 4))):
        b = 12 * i
        for offset, value in {0: obj, 1: room, 2: room, 4: room, 5: 1, 9: 1}.items():
            a['h13Actors'][b + offset] = value
        a['h13History'][88 + b] = room
    return v


def strict_origins(build, reference):
    v = origin_fixture(build)
    p = v.instance(995)
    assert v.call(p, 'h13Valid') == 1
    calls = v.ancestor_room_calls
    if not reference:
        assert calls == 0, 'One validated history must avoid seven new ancestor scans'
    a = v.arrays(995)
    mutations = 0
    for i in range(7):
        b = 12 * i
        old = a['h13Actors'][b + 1]
        a['h13Actors'][b + 1] = (old + 1) % 7
        assert v.call(p, 'h13Valid') == 0, 'Forged origin must fail'
        a['h13Actors'][b + 1] = old
        e = 256 * i + 255
        a['h13Edges'][e] = 1
        assert v.call(p, 'h13Valid') == 0, 'Unused route tail must remain checked'
        a['h13Edges'][e] = 0
        mutations += 2
    # A genuine-shaped route still passes and its revision cannot be forged.
    a['h13Actors'][2] = 1
    a['h13Actors'][5] = 2
    a['h13Actors'][6] = 1
    a['h13Edges'][0:4] = [2, 1, 1, 2]
    assert v.call(p, 'h13Valid') == 1
    a['h13Edges'][3] = 1
    assert v.call(p, 'h13Valid') == 0
    v.history_ok = False
    assert v.call(p, 'h13Valid') == 0, 'Ancestor denial must still deny the descendant'
    if not reference:
        v.history_ok = True
        a['h13Edges'][3] = 2
        a['h13History'][0] = 1
        assert v.call(p, 'h13Valid') == 0, 'An earlier predecessor phase must fail'
    return {'initial_ancestor_room_calls': calls, 'rejected_mutations': mutations + (2 if reference else 3),
            'scope': 'Actual strict descendant predicate; ancestor/domain admission fixtures'}


def readiness_denial(build, reference):
    v = RecoveryFixture(build)
    p = v.instance(995)
    v.arrays(995)['h13Cargo'][:] = [4, 4, 4, 4]
    v.ready_validation = 1
    assert v.call(p, 'h13ReadyPhysical') == 0
    calls = v.ready_validation_calls
    if not reference:
        assert calls == 0, 'Incomplete chapter should deny before expensive validation'
    v.ready = True
    v.ready_validation = 0
    assert v.call(p, 'h13ReadyPhysical') == 0
    v.ready_validation = 1
    assert v.call(p, 'h13ReadyPhysical') == 1
    v.arrays(995)['h13Cargo'][3] = 1
    assert v.call(p, 'h13ReadyPhysical') == 0
    return {'incomplete_chapter_validation_calls': calls, 'ready_ancestor_denial_preserved': True}


CASES = {'retained_menu': retained_menu, 'apron_menu': apron_menu,
         'renewal_label': renewal_label, 'strict_origins': strict_origins,
         'readiness_denial': readiness_denial}
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=CASES)
    parser.add_argument('--build')
    parser.add_argument('--reference', action='store_true')
    args = parser.parse_args()
    print(json.dumps({'status': 'REFERENCE_EMITTED_NOT_NATIVE' if args.reference else 'PASS_EMITTED_NOT_NATIVE',
                      'case': args.case, 'native_acceptance': False,
                      **CASES[args.case](args.build, args.reference)}))
