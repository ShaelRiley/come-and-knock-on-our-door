#!/usr/bin/env python3
"""Emitted date-overlay order and strict publication; explicit scene fixtures.

P13 scene admission, legacy renderer/UI and P14 base admission are modeled.
Actual Main/late dispatch, date packing/input, owner read scope and publication
branches run. No native pixels, saves, earned progress or responsiveness pass.
"""
import argparse
from collections import deque
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


FIELDS = ('type', 'message', 'modifiers', 'x', 'y')


def key(message, event_type=4, tag=None):
    return dict(type=event_type, message=message, modifiers=2, x=31, y=117,
                tag=tag if tag is not None else str((event_type, message)))


class NormalEngineQuit(Exception):
    pass


class QueueFixture(DateFixture):
    def __init__(self, build=None, text=''):
        super().__init__(build, text=text)
        self.pending_events = deque()
        self.polls = []
        self.consumed = []
        self.base_calls = 0
        self.deny_after = None

    def call(self, obj, name, args=()):
        if (obj.module.number, name) == (996, 'h14Base'):
            self.base_calls += 1
            return int(self.deny_after is None or self.base_calls <= self.deny_after)
        return super().call(obj, name, args)

    def kernel(self, number, args):
        if self.knames.get(number) == 'GetEvent':
            assert len(args) == 2 and args[1] is self.h
            mask = args[0] & 0xffff
            assert mask in (0xffff, 0x7fff), 'Never skip ahead with keyboard-only polling'
            peek = bool(mask & 0x8000)
            self.polls.append({'mask': mask, 'peek': peek})
            # Any selects the actual head. Both peek and consume write fields.
            event = self.pending_events[0] if self.pending_events else dict(type=0, message=0, modifiers=0, x=319, y=199)
            if event['type'] == 2048:
                raise NormalEngineQuit('Stock kGetEvent can abort even on Quit peek')
            typed = {field: base.signed(event[field]) for field in FIELDS}
            self.h.p.update(typed)
            if event['type'] and not peek:
                self.pending_events.popleft()
                self.consumed.append(dict(event, **typed))
            return int(bool(event['type']))
        return super().kernel(number, args)

    def procedure(self, module, index, args):
        # Save/Load retirement reaches the real class-free date-bank export.
        # Dispatch emitted code instead of treating that call as a success stub.
        emitted = self.modules[module]
        return self.execute(self.h, emitted, 'export' + str(index),
                            emitted.layout['exports'][index], args)

    def fields(self):
        return {field: self.h.p[field] for field in FIELDS}

    def text(self):
        arrays = self.arrays(996)
        return ''.join(chr(c) for c in arrays['h14EditChars'][:arrays['h14Edit'][1]])

    def drain(self):
        return self.call(self.instance(996), 'h14DateDrain')

    def ordinary_next(self):
        kernel = next(k for k, name in self.knames.items() if name == 'GetEvent')
        assert self.kernel(kernel, [32767, self.h])
        return self.call(self.instance(996), 'h14Input')


def batching(build=None):
    cases = []
    # A real SCI1.1-style Down/Up stream must advance multiple characters per
    # frame while the batch still counts EVENTS and retains every input guard.
    v = QueueFixture(build)
    assert v.input(ord('A')) == 1
    v.pending_events.extend([key(32768, 8), key(ord('B')), key(32768, 8),
                     key(ord('C')), key(32768, 8), key(ord('D')),
                     key(32768, 8), key(ord('E'))])
    assert v.drain() == 7 and len(v.consumed) == 7
    assert v.base_calls == 8 and v.text() == 'ABCD'
    assert len(v.pending_events) == 1 and v.pending_events[0]['message'] == ord('E')
    assert v.fields() == {field: v.consumed[-1][field] for field in FIELDS}
    assert all(r['mask'] in (65535, 32767) for r in v.polls)
    cases.append('fixed7extra events/8total; FIFO interleaved DownUp yields4chars;8full guards')

    # Enter remains the queue head until the real Main render and strict paint
    # publication have acknowledged the complete edited text.
    v = QueueFixture(build)
    assert v.input(ord('A')) == 1
    enter = key(13, tag='enter')
    v.pending_events.extend([key(ord('B')), key(32768, 8), enter, key(ord('C'))])
    assert v.drain() == 2 and v.text() == 'AB' and v.pending_events[0] == enter
    assert v.arrays(996)['h14Edit'][3] == 0 and v.date() == ''
    assert v.fields() == {field: v.consumed[-1][field] for field in FIELDS}
    v.render()
    assert overlay_last(v) and graph12(v) and v.arrays(996)['h14Edit'][3] == 1
    assert v.ordinary_next() == 1 and v.date() == 'AB'
    assert v.arrays(996)['h14Edit'][0] == 0 and len(v.pending_events) == 1
    cases.append('queued Enter stays unconsumed until actual Main.render/strict paint, then ordinary input commits')

    barriers = [key(27), key(9), key(15360), key(31), key(127),
                dict(type=1, message=0, modifiers=3, x=99, y=113, tag='mouse-down'),
                dict(type=2, message=0, modifiers=1, x=78, y=124, tag='mouse-up'),
                dict(type=64, message=2, modifiers=0, x=67, y=134, tag='direction')]
    for barrier in barriers:
        v = QueueFixture(build)
        assert v.input(ord('A')) == 1
        before = v.fields()
        v.pending_events.extend([barrier, key(ord('B'))])
        assert v.drain() == 0 and v.base_calls == 1
        assert list(v.pending_events) == [barrier, key(ord('B'))] and v.fields() == before
    cases.append('8barrier types stay queued; every event property restored; no skip ahead')

    v = QueueFixture(build)
    assert v.input(ord('A')) == 1
    before = v.fields()
    assert v.drain() == 0 and v.fields() == before and v.base_calls == 1
    cases.append('empty peek restores all5fields')


    v = QueueFixture(build)
    assert v.input(ord('A')) == 1
    v.deny_after = 2
    v.pending_events.extend([key(ord('B')), key(ord('C')), key(ord('D'))])
    assert v.drain() == 2 and v.base_calls == 3
    assert v.text() == 'AB' and v.arrays(996)['h14Edit'][0] == 0
    assert v.date() == '' and len(v.pending_events) == 1
    cases.append('hostile base invalidation rechecks on each event, cancels editor and stops; no committed date')

    v = QueueFixture(build)
    assert v.input(ord('A')) == 1
    v.pending_events.extend([key(ord('|')), key(ord('B'))])
    assert v.drain() == 1 and v.text() == 'A' and v.arrays(996)['h14Edit'][2] == 1
    assert len(v.pending_events) == 1
    polls = len(v.polls)
    assert v.drain() == 0 and len(v.polls) == polls
    v.render()
    assert 'Unsupported character or date too long.' in v.paint
    cases.append('unsupported character is rejected by unchanged input; stop before later edit hides warning')

    v = QueueFixture(build, text='A' * 79)
    assert v.input(ord('B')) == 1
    v.pending_events.extend([key(ord('C')), key(ord('D'))])
    assert v.drain() == 1 and len(v.text()) == 80
    assert v.arrays(996)['h14Edit'][2] == 1 and len(v.pending_events) == 1
    cases.append('80char limit unchanged; length error remains for normal painting')

    v = QueueFixture(build, text='AB')
    assert v.input(ord('C')) == 1
    v.pending_events.extend([key(8), key(ord('D')), key(32768, 8)])
    assert v.drain() == 3 and v.text() == 'ABD' and v.base_calls == 4
    cases.append('Backspace and KeyUp use unchanged actual input semantics')

    for operation in ('inactive', 'save', 'load'):
        v = QueueFixture(build)
        v.pending_events.append(key(ord('Z')))
        if operation == 'inactive':
            v.arrays(996)['h14Edit'][0] = 0
        else:
            v.call(v.instance(996), 'h14Save' if operation == 'save' else 'h14Load', () if operation == 'save' else (0,))
        assert v.arrays(996)['h14Edit'][0] == 0
        before = v.fields()
        assert v.drain() == 0 and not v.polls and len(v.pending_events) == 1 and v.fields() == before
    cases.append('inactive editor and actual Save/Load cancellation leave queues and fields untouched')

    v = QueueFixture(build)
    assert v.input(ord('A')) == 1
    v.pending_events.append(dict(type=2048, message=0, modifiers=0, x=0, y=0, tag='quit'))
    try:
        v.drain()
        raise AssertionError('Quit should follow modeled stock-engine abort, not wait')
    except NormalEngineQuit:
        assert len(v.pending_events) == 1 and not v.consumed
    cases.append('QUIT retains normal stock-engine abort even when encountered by Peek')
    return {'status': 'PASS_EMITTED_NOT_NATIVE', 'case_count': len(cases), 'cases': cases,
            'native_acceptance': False,
            'scope': 'Actual compiled h14DateDrain, unchanged h14Input, real Main render/strict date paint and Save/Load cancellation; modeled stock queue and completed campaign admissions.',
            'limits': ['No native speedup, SDL/X11 delivery, subjective input quality or full-game acceptance is demonstrated.',
                       'Before native use, the compiled candidate must retain all original strict owner/restore/render checks and pass the existing date-modal suite.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--reference', action='store_true')
    mode.add_argument('--batching', action='store_true')
    args = parser.parse_args()
    report = batching(args.build) if args.batching else run(args.build, args.reference)
    print(json.dumps(report, indent=2))
