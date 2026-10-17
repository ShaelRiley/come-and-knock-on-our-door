#!/usr/bin/env python3
"""Emitted late-interface regressions, with explicit scene-admission fixtures.

These fixtures admit P13/P14 for isolated interface checks; they do not earn
puzzles, deliveries, contests, native saves, or ending acceptance. Control
registration, hit testing, menu availability, serial/paint comparisons, and
label drawing execute the unchanged compiled SCI methods.
"""
import argparse
import hashlib
import json
import resource

from presentation_vm import PresentationVM, S, base
from inspect_opening_view import decode_view


class LateUIFixture(PresentationVM):
    def __init__(self, stage=13, build=None):
        super().__init__(build)
        self.stage = stage
        self.admission_calls = {}
        self.h.p.update(location=0, uiPanel=0, onApron=0, opening=0,
                        paused=0, menuOpen=0, p02Revision=1)
        self.arrays(995)['h13Lease'][0:2] = [1, 1]
        for index, obj in enumerate((2, 8, 28, 85, 30, 54, 29)):
            self.arrays(995)['h13Actors'][index * 12] = obj
            self.arrays(995)['h13Actors'][index * 12 + 2] = 0
        self.arrays(995)['h13Cargo'][:] = [2, 3, 3, 1]
        if stage == 14:
            self.arrays(996)['h14Owner'][0:3] = [1, 1, 4]

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        # Only complete-scene admissions are modeled. The methods under test,
        # including their actual availability/ownership/paint guards, run.
        admissions = {(995, 'h13Active'): 1, (995, 'h13Valid'): 1,
                      (996, 'h14Base'): int(self.stage == 14),
                      (996, 'h14Valid'): int(self.stage == 14)}
        if key in admissions:
            label = f'{key[0]}:{key[1]}'
            self.admission_calls[label] = self.admission_calls.get(label, 0) + 1
            return admissions[key]
        return super().call(obj, name, args)

    def choices(self, obj):
        self.call(self.instance(995), 'h13Menu', (obj,))
        arrays = self.arrays(0)
        assert not self.h.p['uiFailure'], 'Menu must fit the normal interface'
        return {arrays['uiChoiceIds'][i]: bool(arrays['uiChoiceEnabled'][i])
                for i in range(self.h.p['uiChoiceCount'])}

    def hit_object(self, x, y):
        index = self.call(self.h, 'uiHit', (x, y))
        return None if index < 0 else self.arrays(0)['uiPayloads'][index]


def intersects(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def display_rectangle(v, args):
    x, y = args[2:4]
    width = next(args[i + 1] for i in range(1, len(args) - 1) if args[i] == 106)
    measure = v.arrays(0)['uiMeasure']
    pointer = base.Pointer(measure.region, measure.start * 2)
    text_size = next(k for k, name in v.knames.items() if name == 'TextSize')
    v.kernel(text_size, [pointer, args[0], 0, width])
    return (x, y, x + measure[3], y + measure[2])


def control_priority():
    v = LateUIFixture()
    assert v.call(v.h, 'uiHostWorldControls') == 1
    assert not v.h.p['uiFailure']
    arrays = v.arrays(0)
    assert 3 in arrays['uiPayloads'][:v.h.p['uiControlCount']], 'Porch bench retained'
    # The native defect was a visible torso selecting the bench. Both the
    # original bench control and the current character controls remain real.
    for index, obj in enumerate((2, 8, 28, 85, 30, 54, 29)):
        assert v.hit_object(41 + 41 * index, 104) == obj
    assert v.hit_object(80, 140) == 432, 'Held program remains selectable'
    assert v.hit_object(100, 116) == 3, 'Uncovered bench remains selectable'
    assert v.hit_object(321, 201) is None
    details = {'p13_person_hits': 7, 'held_item_hits': 1, 'uncovered_prop_hits': 1}
    # Ending characters use the same registration path and actual P14 owner.
    ending = LateUIFixture(stage=14)
    ending.h.p['location'] = 4
    assert ending.call(ending.h, 'uiHostWorldControls') == 1
    assert not ending.h.p['uiFailure']
    for index, obj in enumerate((2, 8, 28, 85, 30, 54, 29)):
        assert ending.hit_object(41 + 41 * index, 104) == obj
    assert ending.hit_object(180, 137) == 433
    controls=ending.arrays(0);count=ending.h.p['uiControlCount']
    boards=[i for i in range(count) if controls['uiPayloads'][i]==433]
    assert len(boards)==1
    board=boards[0]
    assert tuple(controls[name][board] for name in ('uiTops','uiLefts','uiBottoms','uiRights'))==(109,158,143,201)
    # Exact original body rectangles remain registered. Their upper visible bodies stay selectable.
    for index,obj in enumerate((2,8,28,85,30,54,29)):
        actors=[i for i in range(count) if controls['uiPayloads'][i]==obj]
        assert len(actors)==1
        i=actors[0]
        assert tuple(controls[name][i] for name in ('uiTops','uiLefts','uiBottoms','uiRights'))==(62,24+41*index,124,59+41*index)
    for x,y in ((158,109),(200,109),(158,123),(200,123),(180,142)):
        assert ending.hit_object(x,y)==433,('Covered legs are owned by visible foreground board',x,y)
    assert ending.hit_object(180,108)==85
    assert ending.hit_object(157,115)==85
    assert ending.hit_object(201,115)==30
    # Pre-acquisition entry keeps the literal original broad board route; no predecessor owner change.
    class PreOwner(LateUIFixture):
        def call(self,obj,name,args=()):
            if obj.module.number==995 and name=='h13ReadyPhysical':return 1
            return super().call(obj,name,args)
    pre=PreOwner(stage=14);pre.h.p.update(location=4,uiControlCount=0)
    pre.arrays(996)['h14Owner'][0]=0
    assert pre.call(pre.instance(996),'h14Controls')==1
    pa=pre.arrays(0);assert pre.h.p['uiControlCount']==1
    assert pa['uiPayloads'][0]==433
    assert tuple(pa[name][0] for name in ('uiTops','uiLefts','uiBottoms','uiRights'))==(128,158,144,310)
    # Real ending room ownership must move Milo's control with him.
    ending.arrays(996)['h14Owner'][2] = 1
    ending.h.p.update(location=1, uiControlCount=0)
    assert ending.call(ending.h, 'uiHostWorldControls') == 1
    assert ending.hit_object(123, 104) == 28
    assert not ending.h.p['uiFailure']
    details.update(p14_person_hits=7, ending_board_hits=1, ending_milo_room_hits=1)
    return [v, ending], details


def reading_availability():
    v = LateUIFixture()
    for obj in (432, 28):
        for room in range(5):
            v.h.p['location'] = room
            assert v.choices(obj)[13] == (room == 4)
    p = v.instance(995)
    a = v.arrays(995)
    v.h.p['location'] = 4
    for index in range(7):
        a['h13Actors'][index * 12 + 2] = 4
    assert not v.choices(30)[17] and not v.choices(30)[18]
    p.p['p13ServedLo'] = 10
    assert not v.choices(30)[17], 'Unpainted serving must not enable readiness'
    a['h13ServePaint'][:] = [0, 10, 1]
    assert v.choices(30)[17]
    p.p['p13ScreenLo'] = 11
    assert not v.choices(30)[18], 'Unpainted screen must not enable presentation'
    a['h13ScenePaint'][0:3] = [0, 11, 1]
    assert v.choices(30)[18]
    a['h13ServePaint'][1] = 9
    a['h13ScenePaint'][1] = 12
    assert not v.choices(30)[17] and not v.choices(30)[18], 'Serials must match'
    a['h13ServePaint'][:] = [0, 10, 2]
    a['h13ScenePaint'][0:3] = [0, 11, 2]
    assert not v.choices(30)[17] and not v.choices(30)[18], 'Future paint cannot admit'
    return [v], {'program_room_choices': 10, 'rita_paint_states': 7}


def held_item_labels():
    v = LateUIFixture()
    p = v.instance(995)
    assert v.call(p, 'h13PaintWorld') == 1
    assert 'GUEST PROGRAM' in v.paint
    backing = (17, 136, 97, 144)
    font = v.resources[7, 0]
    glyphs = set()
    for column, char in enumerate('GUEST PROGRAM'):
        offset = int.from_bytes(font[6 + ord(char) * 2:8 + ord(char) * 2], 'little')
        width, height = font[offset:offset + 2]
        assert (width, height) == (6, 8)
        rows = font[offset + 2:offset + 2 + height]
        assert not rows[7], 'Preserve the actual blank last glyph row above the footer'
        glyphs.update((18 + column * width + x, 137 + y)
                      for y, row in enumerate(rows) for x in range(width)
                      if row & (128 >> x))
    assert all(backing[0] <= x < backing[2] and backing[1] <= y < backing[3]
               for x, y in glyphs)
    assert 14 < backing[0] < backing[2] < 145 and 134 < backing[1] < backing[3] <= 144
    arrows = decode_view(v.resources[0, 228])[0][10]
    old_arrow_pixels = {(23 + i % arrows['width'], 132 + i // arrows['width'])
                        for i, value in enumerate(arrows['pixels'])
                        if value != arrows['clear_key']}
    assert old_arrow_pixels & glyphs, 'Actual original floor-arrow ink intersects the unchanged label'
    for room in (0, 4):
        v.h.p.update(location=room, uiPanel=0)
        v.ktrace.clear()
        before = {'properties': {n: dict(v.instance(n).p) for n in (994, 995, 996)},
                  'locals': {n: {k: list(a) for k, a in v.arrays(n).items()}
                             for n in (994, 995, 996)}}
        assert v.call(p, 'h13PaintWorld') == 1
        after = {'properties': {n: dict(v.instance(n).p) for n in (994, 995, 996)},
                 'locals': {n: {k: list(a) for k, a in v.arrays(n).items()}
                            for n in (994, 995, 996)}}
        assert before == after, 'Held-item contrast must not change owner, domain or receipt state'
        labels = [(i, args) for i, (name, args) in enumerate(v.ktrace)
                  if name == 'Display' and base.read_string(args[0]) == 'GUEST PROGRAM']
        assert len(labels) == 1
        at, args = labels[0]
        assert display_rectangle(v, args) == (18, 137, 96, 145)
        assert args[args.index(102) + 1] == 2 and args[args.index(105) + 1] == 0
        assert v.ktrace[at - 1] == ('Graph', (11, 136, 17, 144, 97, 1, 0, 0, 0))
        # Ordered emitted fills remove every pre-existing floor-arrow pixel
        # under actual bundled-font ink, without touching the footer at144.
        colors = {point: 15 for point in glyphs}
        for name, packet in v.ktrace[:at]:
            if name != 'Graph' or packet[0] != 11:
                continue
            _, top, left, bottom, right, _, color, *_ = packet
            for x, y in colors:
                if left <= x < right and top <= y < bottom:
                    colors[x, y] = color
        assert set(colors.values()) == {0}
    v.paint.clear()
    v.ktrace.clear()
    p.p['p13ProgramLo'] = 1
    assert v.call(p, 'h13PaintWorld') == 1
    assert 'GUEST PROGRAM' not in v.paint, 'Delivered item must leave held-item band'
    assert ('Graph', (11, 136, 17, 144, 97, 1, 0, 0, 0)) not in v.ktrace
    p.p['p13ProgramLo'] = 0
    for panel in (2, 4):
        v.h.p['uiPanel'] = panel
        v.paint.clear()
        v.ktrace.clear()
        v.call(p, 'h13PaintWorld')
        assert 'GUEST PROGRAM' not in v.paint, 'Label must not cover menus/readers'
        assert ('Graph', (11, 136, 17, 144, 97, 1, 0, 0, 0)) not in v.ktrace
    v.h.p.update(uiPanel=0, location=1)
    v.ktrace.clear()
    assert v.call(p, 'h13PaintWorld') == 1
    labels = [args for name, args in v.ktrace
              if name == 'Display' and base.read_string(args[0]) == 'PLEDGES']
    assert len(labels) == 1
    args = labels[0]
    width = next(args[i + 1] for i in range(1, len(args) - 1) if args[i] == 106)
    measure = v.arrays(0)['uiMeasure']
    pointer = base.Pointer(measure.region, measure.start * 2)
    # Existing typed kernel checks the bundled font's actual 6x8 advances.
    text_size = next(k for k, name in v.knames.items() if name == 'TextSize')
    v.kernel(text_size, [pointer, args[0], 0, width])
    assert measure[2] == 8 and measure[3] <= width, 'Pledge label must fit one row'
    pledge_height, pledge_width = measure[2], measure[3]
    v.ktrace.clear()
    v.call(v.instance(991), 'drawLiving', (v.h,))
    v.call(p, 'h13PaintWorld')
    court = next(args for name, args in v.ktrace
                 if name == 'Display' and base.read_string(args[0]) == 'COURT')
    court_rect = display_rectangle(v, court)
    board = next(args for name, args in v.ktrace
                 if name == 'Graph' and args[:5] == (11, 109, 158, 145, 201))
    board_rect = (board[2], board[1], board[4], board[3])
    assert not intersects(court_rect, board_rect), (court_rect, board_rect)
    v.h.p['uiControlCount'] = 0
    v.call(v.h, 'uiHostWorldControls')
    assert v.hit_object(166, 104) == 13, 'Relocated text remains over the Court exit'
    assert v.hit_object(180, 140) == 433, 'Board control remains at its original position'
    return [v], {'held_label_states': 4, 'held_backing_rooms': 2,
                 'held_backing_rectangle': backing, 'held_opaque_glyph_pixels': len(glyphs),
                 'original_floor_arrow_glyph_collisions': len(old_arrow_pixels & glyphs),
                 'pledge_label_rows': pledge_height // 8,
                 'pledge_text_width': pledge_width, 'emitted_display_width': width,
                 'court_text_rectangle': court_rect, 'board_rectangle': board_rect}


def caption_layout():
    v = LateUIFixture()
    p = v.instance(995)
    a = v.arrays(995)
    a['h13Cargo'][:] = [4, 4, 4, 4]
    for i in range(7):
        a['h13Actors'][i * 12 + 2] = 4
    p.p.update(p13ScreenLo=11, p13ServedLo=12, p13ShowLo=13, p13ToastLo=14)
    expected = {"RITA'S VIEWING SIDE OPEN", 'RITA HAS PRESENTED HER WORK',
                '8 TASTING PORTIONS SERVED', 'TOAST: BOARD AND PEOPLE READY'}
    results = []
    for panel in (0, 2, 4):
        v.h.p.update(location=4, uiPanel=panel)
        v.ktrace.clear()
        assert v.call(p, 'h13PaintWorld') == 1
        displays = {base.read_string(args[0]): args for name, args in v.ktrace
                    if name == 'Display' and base.read_string(args[0]) in expected}
        assert set(displays) == expected, 'All four existing statuses remain visible'
        rects = {text: display_rectangle(v, args) for text, args in displays.items()}
        for text, rect in rects.items():
            assert 0 <= rect[0] < rect[2] <= 320 and 44 <= rect[1] < rect[3] <= 62, (text, rect)
            assert rect[3] - rect[1] == 8, (text, 'status wrapped')
            assert not intersects(rect, (23, 132, 299, 142)), 'Keep original travel lane clear'
            assert not intersects(rect, (18, 118, 130, 132)), 'Keep original portions clear'
        pairs = list(rects.items())
        for i, (text, rect) in enumerate(pairs):
            for other, other_rect in pairs[i + 1:]:
                assert not intersects(rect, other_rect), (text, other)
        portions = [args for name, args in v.ktrace
                    if name == 'DrawCel' and args[:3] == (228, 0, 6)]
        assert len(portions) == 8 and [args[3] for args in portions] == list(range(18, 117, 14))
        results.append({'panel': panel, 'rectangles': rects, 'original_portions': len(portions)})
    return [v], {'caption_states': results}


CASES = {'control_priority': control_priority,
         'reading_availability': reading_availability,
         'held_item_labels': held_item_labels,
         'caption_layout': caption_layout}


def run(case):
    fixtures, detail = CASES[case]()
    return {'status': 'PASS_EMITTED_NOT_NATIVE', 'case': case,
            'native_acceptance': False,
            'scope': 'Scene-admission fixtures; unchanged compiled UI; no campaign progress',
            'instructions': sum(v.steps for v in fixtures),
            'admission_fixtures': [v.admission_calls for v in fixtures],
            'compile_receipt_sha256': hashlib.sha256(
                (S / 'build/coherent/compile-receipt.json').read_bytes()).hexdigest(),
            'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            **detail}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=CASES)
    args = parser.parse_args()
    print(json.dumps(run(args.case)))
