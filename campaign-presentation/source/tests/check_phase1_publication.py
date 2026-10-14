#!/usr/bin/env python3
"""Emitted P13 publication/strict-close regressions; explicit admission fixtures.

No native saves, campaign receipts, pixels, audio or performance are accepted.
Ancestor history, legacy barriers, work routes and reader/scene admissions are
modeled. Actual emitted validation, input/arrival/cargo writes and Main gates run.
"""
import argparse
from collections import Counter
import json

from check_paint_scope import PaintFixture, main_case


class PhaseFixture(PaintFixture):
    def __init__(self, build=None):
        super().__init__(build)
        self.historical_good = True
        self.work_fixture = self.wrong_fixture = self.scene_fixture = False
        self.counts = Counter()
        self.a13 = self.arrays(995)
        for i in range(7):
            for field in (1, 2, 4):
                self.a13['h13Actors'][12*i+field] = 4
            self.a13['h13History'][88+12*i] = 4

    def arm(self):
        self.a13['h13Paint'][:7] = [2, self.h.p['location'], 2, 0, 0,
                                   self.a13['h13Lease'][2], self.a13['h13Work'][0]]
        self.a13['h13InputPaint'][:7] = [2, self.h.p['location'], 2, 0, 0, 0, 0]

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        self.counts[key] += 1
        if key in {(985, 'hBarrier'), (987, 'h6Barrier')}:
            return 0  # Completed legacy-controller admission fixture.
        if key == (995, 'h13Historical'):
            return int(self.call(obj, 'h13Baseline') and self.historical_good)
        if self.work_fixture and key in {(995, 'h13WorkValid'), (995, 'h13DeliveryValid')}:
            return 1  # Work/route admission modeled; actual publication writes run.
        if self.scene_fixture:
            if key == (995, 'p13Served'):
                return 1
            if key == (995, 'p13Present') and args[0] in (5, 7, 8, 10):
                return 1
            if key == (995, 'p13Validate'):
                return 1  # Scene ledger modeled; no receipt earned.
        if self.wrong_fixture and key in {(995, 'h13WrongMatch'), (995, 'h13ReaderCheck')}:
            return 1  # Reader identity modeled; actual animation branch runs.
        return super().call(obj, name, args)


def snapshot(v):
    return {'arrays': {k: list(a) for k, a in v.arrays(995).items()},
            'properties': dict(v.instance(995).p), 'dirty': v.h.p['dirty']}


def graph12(v):
    return sum(name == 'Graph' and args[0] == 12 for name, args in v.ktrace)


def run(build=None):
    cases = []
    v = PhaseFixture(build)
    v.arm()
    expected = snapshot(v)
    expected['arrays']['h13Witness'][:] = [1, 4, 2, 0, 0, 0, 0]
    expected['arrays']['h13InputPaint'][0] = 0
    expected['arrays']['h13Paint'][0] = 0
    assert v.call(v.instance(995), 'h13WorldFrame', (1,)) == 0
    assert snapshot(v) == expected
    assert graph12(v) == 1 and v.counts[995, 'h13Valid'] == 0
    cases.append('idle handoff publishes exact input witness, retires paint and changes no durable fact')

    for room in (2, 3):
        v = PhaseFixture(build)
        v.a13['h13Lease'][0] = 0
        v.h.p['location'] = room
        v.arm()
        assert v.call(v.instance(995), 'h13WorldFrame', (1,)) == 1
        assert graph12(v) == 2 and v.a13['h13Pickup'][0 if room == 2 else 1] == 2
        assert v.a13['h13Witness'][0] == 1
        cases.append(f'prelease room{room} physical source pickup and flush preserved')

    for index in range(7):
        v = PhaseFixture(build)
        v.a13['h13Lease'][2] = 1 << index
        v.a13['h13Actors'][12*index+3] = 1
        v.arm()
        before = snapshot(v)
        assert v.call(v.instance(995), 'h13WorldFrame', (1,)) == 1
        expected = before
        expected['arrays']['h13Witness'][:] = [1, 4, 2, 0, 0, 0, 0]
        expected['arrays']['h13InputPaint'][0] = expected['arrays']['h13Paint'][0] = 0
        expected['arrays']['h13Lease'][2] = 0
        expected['arrays']['h13Actors'][12*index+7] = 2
        expected['arrays']['h13Actors'][12*index+8] = 1
        assert snapshot(v) == expected
        assert graph12(v) == 2 and v.counts[995, 'h13Valid'] == 2
        cases.append(f'actor{index} arrival preserves strict pre/post proof and exact durable fields')

    for kind, room, pot_passed in ((1,4,0), (2,2,0), (2,4,1), (3,4,0), (4,4,0)):
        v = PhaseFixture(build)
        v.work_fixture = True
        v.h.p['location'] = room
        v.a13['h13Work'][:12] = [kind, {1:2,2:4,3:6,4:9}[kind], 0, 1, 1,
                                pot_passed, room, 0, 0, 2 if pot_passed else 0, 1, 1]
        leader = {1:2,2:-1,3:5,4:1}[kind]
        if leader >= 0:
            v.a13['h13Lease'][2] = 1 << leader
            v.a13['h13Actors'][12*leader+3] = 1
        v.arm()
        v.call(v.instance(995), 'h13WorldFrame', (1,))
        assert graph12(v) == 2 and v.counts[995, 'h13Valid'] == 2
        if kind == 2 and room == 2:
            assert v.a13['h13Work'][5] == 1 and v.a13['h13Work'][9] == 2
            assert v.counts[995, 'h13FinishDelivery'] == 0
        else:
            assert v.counts[995, 'h13FinishDelivery'] == 1 and v.a13['h13Work'][0] == 0
            assert v.a13['h13Deliveries'][10*(kind-1)+4] == 2
        cases.append(f'work{kind}/room{room}/passed{pot_passed} retains actual publication and strict proof calls; route admission modeled')

    v = PhaseFixture(build)
    v.scene_fixture = True
    v.arm()
    assert v.call(v.instance(995), 'h13WorldFrame', (1,)) == 0
    assert graph12(v) == 1 and v.a13['h13Witness'][0] == 1
    assert v.a13['h13ServePaint'][2] == 2
    assert [v.a13['h13ScenePaint'][i] for i in (2,5,8)] == [2,2,2]
    cases.append('input, serve and scene witnesses publish before no-op guard; scene ledger modeled')

    v = PhaseFixture(build)
    v.wrong_fixture = True
    v.a13['h13WrongPaint'][0] = v.a13['h13WrongPaint'][9] = 2
    v.instance(982).p.update(sdPaintGeneration=1, sdGeneration=1)
    v.arm()
    assert v.call(v.instance(995), 'h13WorldFrame', (1,)) == 0
    assert graph12(v) == 2 and v.h.p['dirty'] == 1
    cases.append('active wrong-animation phase1 executes before no-op guard; reader identity modeled')

    for label, mutate in (
        ('serial', lambda v: v.instance(995).p.update(p13ProgramLo=1)),
        ('owner', lambda v: v.arrays(993)['h11OwnerEdges'].__setitem__(319,1)),
        ('prerequisite', lambda v: v.arrays(993)['h11PrereqWords'].__setitem__(200,1)),
        ('actor-origin', lambda v: v.arrays(995)['h13Actors'].__setitem__(1,3)),
        ('unused-route-tail', lambda v: v.arrays(995)['h13Edges'].__setitem__(255,1)),
        ('historical', lambda v: setattr(v, 'history_good', False)),
    ):
        _, result = main_case(build, mutate)
        assert result['phase1_calls'] == result['p13Acknowledge_calls'] == result['graph12_calls'] == 0
        cases.append(f'actual Main strict End rejects raw {label} mutation before phase1/Graph12/ack')

    for used, admitted in ((0,0), (0,1), (1,0), (1,1)):
        for failure in ('none', 'baseline', 'history', 'lease', 'serial'):
            v = PhaseFixture(build)
            if failure == 'baseline': v.history_good = False
            if failure == 'history': v.historical_good = False
            if failure == 'lease': v.a13['h13Lease'][0] = 0
            if failure == 'serial': v.instance(995).p['p13ProgramLo'] = 1
            v.a13['h13RenderMemo'][:] = [used, admitted]
            before = snapshot(v)
            result = v.call(v.instance(995), 'h13RenderClose')
            before['arrays']['h13RenderMemo'] = [0,0]
            assert snapshot(v) == before
            expected = int(not ((used and failure != 'none') or (admitted and failure == 'baseline')))
            assert result == expected and v.counts[995, 'h13Valid'] == used
            baseline_calls = (int(failure != 'lease') + (admitted if failure != 'none' else 0)) if used else admitted
            assert v.counts[995, 'h13Baseline'] == baseline_calls
            cases.append(f'Close used{used}/admitted{admitted}/{failure}: strict dominance/failure fallback, unchanged facts')
    assert len(cases) == 43
    return {'status': 'PASS_NOT_NATIVE', 'case_count': len(cases), 'cases': cases,
            'scope': 'Actual emitted P13 input/arrival/cargo publication, strict Close and Main failure gate; explicit historical/work/reader/scene fixtures',
            'limits': 'No native performance, saves, sound, pixels, campaign receipts, progression or acceptance',
            'native_acceptance': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build')
    args = parser.parse_args()
    print(json.dumps(run(args.build), indent=2))
