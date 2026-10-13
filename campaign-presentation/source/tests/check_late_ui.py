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


class LateUIFixture(PresentationVM):
    def __init__(self, stage=13):
        super().__init__()
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
    assert ending.hit_object(230, 137) == 433
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
    v.paint.clear()
    p.p['p13ProgramLo'] = 1
    assert v.call(p, 'h13PaintWorld') == 1
    assert 'GUEST PROGRAM' not in v.paint, 'Delivered item must leave held-item band'
    p.p['p13ProgramLo'] = 0
    for panel in (2, 4):
        v.h.p['uiPanel'] = panel
        v.paint.clear()
        v.call(p, 'h13PaintWorld')
        assert 'GUEST PROGRAM' not in v.paint, 'Label must not cover menus/readers'
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
    return [v], {'held_label_states': 4, 'pledge_label_rows': measure[2] // 8,
                 'pledge_text_width': measure[3], 'emitted_display_width': width}


CASES = {'control_priority': control_priority,
         'reading_availability': reading_availability,
         'held_item_labels': held_item_labels}


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
