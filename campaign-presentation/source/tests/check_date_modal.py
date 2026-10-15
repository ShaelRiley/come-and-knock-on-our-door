#!/usr/bin/env python3
"""Emitted date-overlay order and strict publication; explicit scene fixtures.

P13 scene admission, legacy renderer/UI and P14 base admission are modeled.
Actual Main/late dispatch, date packing/input, owner read scope and publication
branches run. No native pixels, saves, earned progress or responsiveness pass.
"""
import argparse
import json

from check_paint_scope import DrawFixture
from presentation_vm import PresentationVM, base


class DateFixture(DrawFixture):
    def __init__(self, build=None, text='Sunday, November 1'):
        super().__init__(build, main=True)
        self.h.p.update(uiPanel=0, uiDocument=0, uiPage=0)
        self.arrays(995)['h13Reader'][:] = [0] * 24
        self.arrays(996)['h14Owner'][:] = [0] * 8
        self.arrays(996)['h14Edit'][:] = [1, len(text), 0, 0, 0]
        self.arrays(996)['h14EditChars'][:] = [ord(c) for c in text] + [0] * (80-len(text))
        self.arrays(995)['h13Cargo'][:] = [4] * 4
        for i in range(7):
            self.arrays(995)['h13Actors'][12*i+2] = 4
        self.instance(995).p.update(p13ServedLo=1, p13ScreenLo=1,
                                   p13ShowLo=1)
        self.date_depth = 0
        self.date_ranges = []
        self.draw_events = []
        self.before_overlay_mutation = None
        self.expected_text = text

    def call(self, obj, name, args=()):
        args = tuple(args)
        key = (obj.module.number, name)
        if key == (996, 'h14DateDraw'):
            start = len(self.draw_events)
            self.date_depth += 1
            try:
                result = PresentationVM.call(self, obj, name, args)
            finally:
                self.date_depth -= 1
            if result:
                self.date_ranges.append((start, len(self.draw_events)))
            return result
        if key in {(994, 'h12Frame'), (996, 'h14Frame')}:
            # Execute the actual wrapper order, including the former early draw.
            return PresentationVM.call(self, obj, name, args)
        if key in {(995, 'h13Active'), (995, 'h13Valid'),
                   (995, 'p13Served'), (995, 'p13ShowComplete'),
                   (995, 'p13Ready'), (996, 'h14Base')}:
            return 1  # Complete-scene/base admission only; no progress earned.
        if key in {(994, 'h12LaughFrame'), (994, 'h12WelcomeFrame'),
                   (994, 'h12SuccessorFrame'), (994, 'h12Draw'),
                   (994, 'h12PaintMatch'), (997, 'h14ReplayActive')}:
            return 0  # Unrelated earlier scene and replay callbacks.
        if key == (0, 'uiRender'):
            # An ordinary UI overlay may cross the date rectangle. Main must
            # composite the modal after this point as well as after P13 paint.
            graph = next(k for k, label in self.knames.items() if label == 'Graph')
            self.kernel(graph, [11, 66, 5, 92, 250, 1, 3, 0, 0])
            if self.before_overlay_mutation:
                self.before_overlay_mutation(self)
            return 0
        return super().call(obj, name, args)

    def kernel(self, k, args):
        name = self.knames.get(k)
        if name in {'Graph', 'Display', 'DrawCel'}:
            detail = base.read_string(args[0]) if name == 'Display' else tuple(args)
            self.draw_events.append((name, detail, bool(self.date_depth)))
        return super().kernel(k, args)

    def render(self):
        return self.call(self.h, 'render')

    def input(self, key):
        self.h.p.update(type=4, message=key)
        return self.call(self.instance(996), 'h14Input')

    def date(self):
        a = self.arrays(996)['h14Date']
        return ''.join(chr(a[i+1]) for i in range(a[0]))


def raster(event):
    return event[0] in {'Display', 'DrawCel'} or (event[0] == 'Graph' and event[1][0] == 11)


def overlay_last(v):
    if len(v.date_ranges) != 1:
        return False
    start, end = v.date_ranges[0]
    return (end > start and all(not raster(e) for e in v.draw_events[end:]))


def graph12(v):
    return sum(e[0] == 'Graph' and e[1][0] == 12 for e in v.draw_events)


def durable(v):
    return {n: dict(v.instance(n).p) for n in (995, 996)}


def run(build=None, reference=False):
    cases = []
    v = DateFixture(build)
    before = durable(v)
    v.render()
    assert 'PLEDGES' in v.paint, 'Actual P13 board paint must run in the scene fixture'
    assert sum(e[0] == 'DrawCel' for e in v.draw_events) >= 7
    assert 'Choose the agreed in-fiction repair date' in v.paint
    assert v.expected_text in v.paint
    if reference:
        assert not overlay_last(v), 'Reference must reproduce a later overpaint'
        assert v.arrays(996)['h14Edit'][3] == 1
        return {'status': 'REFERENCE_OCCLUSION_REPRODUCED_NOT_NATIVE',
                'case_count': 1, 'native_acceptance': False,
                'scope': 'Actual old dispatch acknowledges a modal painted before P13/UI'}
    assert overlay_last(v), 'Date must follow every world and ordinary UI raster draw'
    assert durable(v) == before, 'Painting must not mutate P13/P14 domain properties'
    assert v.arrays(996)['h14Owner'][0] == 0
    assert v.arrays(996)['h14Edit'][3:5] == [1, 0]
    assert graph12(v) == 1
    cases.append('actual Main/994/995/996 dispatch paints all seven actors and board before final date overlay')

    v.input(13)
    assert v.date() == v.expected_text and not v.arrays(996)['h14Edit'][0]
    assert v.arrays(996)['h14Owner'][0] == 0
    cases.append('published final modal permits exact ordinary Enter date without acquiring an owner')

    v = DateFixture(build)
    v.call(v.instance(996), 'h14Frame', (2,))
    assert not v.date_ranges and v.arrays(996)['h14Edit'][4] == 0
    cases.append('phase2 domain callback no longer paints or marks date before later world callbacks')

    v = DateFixture(build)
    v.arrays(996)['h14Edit'][0] = 0
    v.render()
    assert not v.date_ranges and v.arrays(996)['h14Edit'][3:5] == [0, 0]
    assert 'Choose the agreed in-fiction repair date' not in v.paint
    cases.append('dormant date hook paints and acknowledges nothing')

    for label, mutation in (
        ('owner route', lambda v: v.arrays(993)['h11OwnerEdges'].__setitem__(319, 1)),
        ('prerequisite word', lambda v: v.arrays(993)['h11PrereqWords'].__setitem__(200, 1)),
        ('host position', lambda v: v.h.p.update(motionX=v.h.p['motionX']+1)),
    ):
        v = DateFixture(build)
        v.before_overlay_mutation = mutation
        before = durable(v)
        v.render()
        assert overlay_last(v)
        assert v.arrays(996)['h14Edit'][3] == 0 and graph12(v) == 0
        assert durable(v) == before
        v.input(13)
        assert not v.date() and not v.arrays(996)['h14Owner'][0]
        cases.append(label + ' mutation fails actual strict End; no date readiness, flush or Enter admission')

    v = DateFixture(build)
    v.input(13)
    assert not v.date()
    cases.append('Enter before a successful final modal publication cannot commit the date')

    v = DateFixture(build)
    v.render()
    v.input(ord('!'))
    assert v.arrays(996)['h14Edit'][3] == 0
    v.input(13)
    assert not v.date()
    cases.append('ordinary character edit clears readiness until its own successful final paint')

    v = DateFixture(build, text='A'*80)
    v.render()
    assert overlay_last(v) and 'A'*80 in v.paint
    v.input(8)
    assert v.arrays(996)['h14Edit'][1] == 79 and v.arrays(996)['h14Edit'][3] == 0
    v.render()
    v.input(13)
    assert v.date() == 'A'*79
    cases.append('80-character packing and ordinary Backspace/repaint/Enter preserve exact text')

    v = DateFixture(build)
    v.input(ord('|'))
    v.render()
    assert overlay_last(v) and 'Unsupported character or date too long.' in v.paint
    assert v.arrays(996)['h14Edit'][1] == len(v.expected_text)
    v.input(27)
    assert not v.date() and not v.arrays(996)['h14Edit'][0]
    cases.append('unsupported-character help remains final-visible and ordinary Escape cancels without a date')

    assert len(cases) == 11
    return {'status': 'PASS_EMITTED_NOT_NATIVE', 'case_count': len(cases),
            'cases': cases, 'native_acceptance': False,
            'scope': 'Actual emitted Main/late dispatch, date packing/input, owner strict End and acknowledgement',
            'fixtures': 'P13 complete-scene and P14 base admissions, legacy world renderer/UI and unrelated callbacks',
            'limits': 'No native pixels, saves, campaign progress, audio or responsiveness acceptance'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build')
    parser.add_argument('--reference', action='store_true')
    args = parser.parse_args()
    print(json.dumps(run(args.build, args.reference), indent=2))
