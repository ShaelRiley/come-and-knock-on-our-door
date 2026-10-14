#!/usr/bin/env python3
"""Emitted paint scope/publication checks with explicit modeled admissions.

No fixture earns campaign progress, creates native saves or accepts performance,
pixels or sound. Ancestor history, renderer and reader identity are modeled;
actual emitted read guards, P13 validation and Main publication branches run.
"""
import argparse
import json

from presentation_vm import PresentationVM


class PaintFixture(PresentationVM):
    def __init__(self, build=None):
        super().__init__(build)
        self.history_good = True
        self.owner_history_good = True
        self.h.p.update(p08=self.instance(989), location=4, p02Revision=2,
                        motionX=0, motionY=0, motionPhase=0, onApron=0,
                        opening=0, paused=0, menuOpen=0, uiPanel=0,
                        uiDocument=0, bridgeReaderActive=0, uiFailure=0,
                        bridgeFailure=0)
        self.instance(989).p.update(h8Host=self.h, h8Lease=1)
        self.arrays(0)['h11MainRead'][0] = 1
        self.arrays(993)['h11OwnerState'][0] = 1
        self.arrays(993)['h11OwnerState'][3] = 1
        self.instance(995).p.update(p13Initialized=1, p13ContextValid=1)
        a = self.arrays(995)
        a['h13Lease'][0:2] = [1, 1]
        a['h13History'][0] = 2
        a['h13Cargo'][:] = [2, 3, 3, 1]
        for i, (obj, room) in enumerate(zip((2, 8, 28, 85, 30, 54, 29),
                                             (2, 1, 0, 3, 3, 3, 4))):
            b = 12 * i
            for offset, value in {0: obj, 1: room, 2: room, 4: room,
                                  5: 1, 9: 1}.items():
                a['h13Actors'][b + offset] = value
            a['h13History'][88 + b] = room

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        if key == (993, 'h11OwnerHistory'):
            return int(self.owner_history_good)
        if key in {(995, 'h13Historical'), (995, 'h13Baseline')}:
            return int(self.history_good)
        return super().call(obj, name, args)

    def begin(self):
        q = self.instance(993)
        assert self.call(q, 'h11ReadBegin') == 1
        assert self.call(q, 'h11ReadResume') == 1
        assert self.call(q, 'h11ReadMemo') == 1
        p = self.instance(995)
        assert self.call(p, 'h13Valid') == 1
        assert self.arrays(995)['h13RenderMemo'][0] == 1
        return p, q


class DrawFixture(PaintFixture):
    def __init__(self, build=None, main=False):
        super().__init__(build)
        self.main_test = main
        self.renderer_good = True
        self.phase2_mutation = None
        self.fail_resume = False
        self.events = []
        self.phase2_memo = []
        self.phase1_calls = 0
        self.h.p['p09'] = self.instance(990)
        self.instance(990).p['h9Host'] = self.h
        if main:
            self.arrays(0)['h11MainRead'][0] = 0
            self.h.p.update(currentCaption=0, navNoticeTicks=0, uiPanel=4,
                            uiDocument=1550, uiPage=0)
            self.instance(982).p.update(sdActive=1, sdFailure=0, sdGeneration=2,
                                       sdPage=0, sdDocument=1550, sdCount=1)
            reader = self.arrays(995)['h13Reader']
            for index, value in {0: 1, 1: 1550, 2: 1, 6: 0, 7: 1}.items():
                reader[index] = value

    def call(self, obj, name, args=()):
        args = tuple(args)
        key = (obj.module.number, name)
        if key == (991, 'h8VD'):
            self.events.append('renderer')
            if self.main_test:
                self.instance(982).p['sdPaintGeneration'] = 2
            return int(self.renderer_good)
        if key in {(993, 'h11ReadBoundary'), (993, 'h11ReadResume'),
                   (993, 'h11ReadEnd')}:
            self.events.append(name)
            if (name == 'h11ReadResume' and self.fail_resume
                    and 'renderer' in self.events):
                # Model a physical mutation between boundary and Resume.
                self.h.p['motionX'] += 1
                self.fail_resume = False
        if key == (994, 'h12Frame'):
            if args == (2,):
                self.events.append('late-phase2')
                self.phase2_memo.append(super().call(self.instance(993),
                                                    'h11ReadMemo'))
                result = super().call(self.instance(995), 'h13Frame', (2,))
                if self.phase2_mutation:
                    self.phase2_mutation(self)
                return result
            return 0
        if key in {(992, 'h10Frame'), (993, 'h11OwnerFrame'), (993, 'h11Frame'),
                   (989, 'h8ReaderFrame'), (989, 'h8VF'), (990, 'h9Frame'),
                   (996, 'h14MenuFrame'), (996, 'h14Frame')}:
            return 0
        if key in {(990, 'h9UI'), (990, 'h9ReaderCheck'), (0, 'uiRender'),
                   (0, 'renderCaption')}:
            return 0
        if key == (0, 'drawWorld'):
            return super().call(self.instance(990), 'h9Draw')
        if key == (0, 'p03Checkpoint'):
            return 1
        if self.main_test and key == (995, 'h13ReaderCheck'):
            return 1  # Reader identity only; no valid receipt is fabricated.
        if key == (995, 'h13Frame') and args == (1,):
            self.phase1_calls += 1
        return super().call(obj, name, args)


def main_case(build, mutation=None, resume_fail=False):
    v = DrawFixture(build, main=True)
    v.phase2_mutation = mutation
    v.fail_resume = resume_fail
    v.call(v.h, 'render')
    graph12 = sum(name == 'Graph' and args[0] == 12 for name, args in v.ktrace)
    return v, {'phase1_calls': v.phase1_calls,
               'p13Acknowledge_calls': v.calls[995, 'p13Acknowledge'],
               'graph12_calls': graph12, 'phase2_memo': v.phase2_memo}


def run(build=None):
    cases = []
    v = DrawFixture(build)
    _, q = v.begin()
    v.arrays(995)['h13RenderMemo'][0] = 0
    before = v.calls[995, 'p13Validate']
    v.events.clear()
    assert v.call(v.instance(990), 'h9Draw') == 1
    assert v.phase2_memo == [1]
    assert v.calls[995, 'p13Validate'] - before == 1
    order = v.events
    assert (order.index('renderer') < order.index('h11ReadBoundary')
            < order.index('h11ReadResume') < order.index('late-phase2'))
    assert v.call(q, 'h11ReadEnd') == 1
    cases.append('Boundary then Resume before late paint; repeated paint queries reuse one proof')

    v, positive = main_case(build)
    assert positive['phase1_calls'] == positive['p13Acknowledge_calls'] == 1
    assert positive['graph12_calls'] == 1
    assert list(v.arrays(993)['h11Read']) == [0] * 14
    cases.append('actual Main success branch reaches Frame1/Graph12/receipt hook; no receipt earned')
    for label, mutation in (
        ('owner route', lambda v: v.arrays(993)['h11OwnerEdges'].__setitem__(319, 1)),
        ('prerequisite word', lambda v: v.arrays(993)['h11PrereqWords'].__setitem__(200, 1)),
        ('P13 serial', lambda v: v.instance(995).p.update(p13ProgramLo=1)),
        ('P13 origin', lambda v: v.arrays(995)['h13Actors'].__setitem__(1, 3)),
        ('P13 unused route tail', lambda v: v.arrays(995)['h13Edges'].__setitem__(255, 1)),
        ('ancestor history', lambda v: setattr(v, 'history_good', False)),
    ):
        v, result = main_case(build, mutation)
        assert result['phase2_memo'] == [1]
        assert (result['phase1_calls'] == result['p13Acknowledge_calls']
                == result['graph12_calls'] == 0), (label, result)
        assert list(v.arrays(995)['h13RenderMemo']) == [0, 0]
        assert list(v.arrays(993)['h11Read']) == [0] * 14
        cases.append(label + ' mutation fails strict End with no publication or receipt hook')

    _, failed = main_case(build, resume_fail=True)
    assert failed['phase2_memo'] == []
    assert (failed['phase1_calls'] == failed['p13Acknowledge_calls']
            == failed['graph12_calls'] == 0)
    cases.append('failed Resume skips late callbacks and Main publication')

    v = DrawFixture(build)
    _, q = v.begin()
    v.renderer_good = False
    assert v.call(v.instance(990), 'h9Draw') == 0 and not v.phase2_memo
    assert v.call(q, 'h11ReadEnd') == 1
    cases.append('renderer failure skips callbacks and safely closes the unchanged proof')

    v = DrawFixture(build)
    v.instance(990).p['h9Host'] = 0
    assert v.call(v.instance(990), 'h9Draw') == 0 and not v.events
    assert v.call(v.objects['P09State'], 'h9Draw') == 0 and not v.events
    cases.append('invalid host and noncanonical receiver cannot render or resume')

    v = DrawFixture(build)
    v.arrays(993)['h11OwnerState'][0] = 0
    v.arrays(993)['h11OwnerState'][3] = 0
    v.arrays(995)['h13Lease'][0] = 0
    v.h.p['opening'] = 1
    assert v.call(v.instance(990), 'h9Draw') == 1
    assert v.phase2_memo == [0]
    cases.append('dormant owner retains its result and cannot enable read memo')

    v = DrawFixture(build)
    p, q = v.begin()
    p.p['p13ProgramLo'] = 1
    serial = p.p['p13RevisionHi'], p.p['p13RevisionLo']
    assert v.call(p, 'p13Start', (1,)) == 0
    v.call(p, 'p13Begin', (1,))
    assert (p.p['p13RevisionHi'], p.p['p13RevisionLo']) == serial
    assert v.call(q, 'h11ReadEnd') == 0
    cases.append('strict mutation entries reject invalid domain before serial commit')
    assert len(cases) == 13
    return {'status': 'PASS_NOT_NATIVE', 'case_count': len(cases), 'cases': cases,
            'scope': 'Actual emitted draw/boundary/read scope/P13 validation and Main publication; ancestor history, renderer, reader identity and unrelated callbacks modeled',
            'limits': 'No native timing, pixels, audio, saves, campaign receipts, progression or acceptance',
            'native_acceptance': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build')
    args = parser.parse_args()
    print(json.dumps(run(args.build), indent=2))
