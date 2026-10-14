#!/usr/bin/env python3
"""Actual emitted Main header branch; explicit unrelated render admissions.

This fixture does not earn campaign progress, create SCI saves or accept pixels.
It catches the inline legacy caption missed by the renderer-only R3 check.
"""
import argparse
import json

from presentation_vm import PresentationVM


class HeaderFixture(PresentationVM):
    def __init__(self, build=None):
        super().__init__(build)
        self.h.p.update(opening=0, paused=0, menuOpen=0, uiPanel=0,
                        currentCaption=0, navNoticeTicks=0, location=4)

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        # This test executes Main's real inline caption branch. Its separate
        # caption delegate and unrelated scene/owner admissions are fixtures.
        if key in {(0, 'renderCaption'), (0, 'drawWorld')}:
            return 0
        if key == (0, 'p03Checkpoint'):
            return 1
        if name in {'h11ReadBegin', 'h11ReadResume', 'h11ReadEnd',
                    'h11ReadFinish'}:
            return 1
        if name in {'h14MenuFrame', 'h14Frame', 'h13Frame', 'h12Frame',
                    'h11OwnerFrame', 'h11Frame', 'h10Frame', 'h8ReaderFrame',
                    'h9Frame', 'h8VF'}:
            return 0
        return super().call(obj, name, args)


def header_case(build, chapter, reference=False):
    v = HeaderFixture(build)
    if chapter == 13:
        v.arrays(995)['h13Lease'][0] = 1
    elif chapter == 14:
        v.arrays(996)['h14Owner'][0] = 1
    v.call(v.h, 'render')
    present = "RITA'S PREPARATION COMPLETE." in v.paint
    expected = chapter == 12 or reference
    assert present == expected, (chapter, present, v.paint)
    assert ('YOU CAN CONTINUE EXPLORING.' in v.paint) == expected
    return {'chapter': chapter, 'legacy_preparation_caption': present,
            'instructions': v.steps,
            'scope': 'Emitted Main header/Display trace; modeled unrelated admissions'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--build')
    p.add_argument('--reference', action='store_true')
    a = p.parse_args()
    rows = [header_case(a.build, chapter, a.reference) for chapter in (12, 13, 14)]
    print(json.dumps({'status': 'PASS_NOT_NATIVE', 'cases': rows,
                      'native_acceptance': False}, indent=2))


if __name__ == '__main__':
    main()
