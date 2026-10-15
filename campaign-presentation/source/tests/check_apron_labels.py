#!/usr/bin/env python3
"""Emitted apron-label regression; never native acceptance.

Uses the existing typed VM. P12 admission and unrelated successor controls are
fixtures; actual background drawing, P12 drawing/controls, reveal UI, font
measurement and reverse hit testing execute the selected compiled build.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE / 'tests'), str(SOURCE / 'tools')]
from presentation_vm import PresentationVM, base
from check_late_ui import display_rectangle
from inspect_opening_view import decode_view


ART = {
    102: '3e57f74ca80aab39c2355808c617900bdd93f70a0cfe30236dabcc7376150cd8',
    103: '758ffae11a60eedbce4315e48b1c1693e072f514de41ffebca38c86dde75dcb8',
}
PAPER = (166, 131, 278, 144)
PAPER_COLOR = 10
INK_COLOR = 167
CONTROL = (166, 128, 304, 142)


class ApronFixture(PresentationVM):
    def __init__(self, build=None, room=4, apron=True, active=True, successor=False):
        super().__init__(build)
        self.active = active
        self.successor = successor
        self.keep_controls = False
        self.h.p.update(location=room, onApron=int(apron), opening=0, paused=0,
                        menuOpen=0, uiPanel=0, p05=0, p08=0, uiControlCount=0,
                        uiFailure=0, uiReveal=0, uiFocus=0)

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        if key == (994, 'h12Active'):
            return int(self.active)  # Explicit complete-P12-scene admission.
        if key == (995, 'h13Has'):
            return int(self.successor)  # Separate inactive/successor guard cases.
        if key == (994, 'h12SuccessorControls'):
            return 0  # Unrelated companion controls are outside this label test.
        if self.keep_controls and key == (0, 'uiBuildFocus'):
            # Preserve the controls just registered by the real methods below;
            # no control or label packet is supplied by the fixture.
            return 0
        return super().call(obj, name, args)

    def controls(self):
        self.h.p['uiControlCount'] = 0
        if self.h.p['onApron']:
            self.call(self.h, 'h6BaseControls')
        self.call(self.instance(994), 'h12Controls')
        a = self.arrays(0)
        return {a['uiPayloads'][i]: (i, (a['uiLefts'][i], a['uiTops'][i],
                                       a['uiRights'][i], a['uiBottoms'][i]))
                for i in range(self.h.p['uiControlCount'])}

    def hit(self, x, y):
        i = self.call(self.h, 'uiHit', (x, y))
        return None if i < 0 else self.arrays(0)['uiPayloads'][i]


def displays(v, text):
    return [(i, args) for i, (name, args) in enumerate(v.ktrace)
            if name == 'Display' and base.read_string(args[0]) == text]


def state(v):
    # Only the existing transient h12Paint witness may change during h12Draw.
    return {'properties': {n: dict(v.instance(n).p) for n in (994, 995, 996)},
            'locals': {n: {k: list(a) for k, a in v.arrays(n).items()
                            if not (n == 994 and k == 'h12Paint')}
                       for n in (994, 995, 996)}}


def restore_baked_ink(v, cel, before_label):
    """Check pixels actually restored, not a prescribed implementation packet."""
    original = cel['pixels']
    result = bytearray(original)
    clears = []
    for name, args in v.ktrace[:before_label]:
        if name != 'Graph' or args[0] != 11 or args[6] != PAPER_COLOR:
            continue
        _, top, left, bottom, right, *_ = args
        assert 0 <= left < right <= 320 and 0 <= top < bottom <= 144
        clears.append((left, top, right, bottom))
        for y in range(top, bottom):
            for x in range(left, right):
                at = y*320+x
                if original[at] != PAPER_COLOR:
                    assert (PAPER[0] <= x < PAPER[2] and PAPER[1] <= y < PAPER[3]
                            and original[at] == INK_COLOR), 'Clear erased unrelated authored illustration'
                result[at] = PAPER_COLOR
    ink = [(x, y) for y in range(PAPER[1], PAPER[3])
           for x in range(PAPER[0], PAPER[2]) if original[y*320+x] == INK_COLOR]
    return all(result[y*320+x] == PAPER_COLOR for x, y in ink), clears


def issue(issues, condition, label):
    if not condition:
        issues.append(label)


def run(build=None, reference=False):
    issues = []
    cases = []
    decoded = {}
    v = ApronFixture(build)
    manifest = json.loads((SOURCE / 'AUDIENCE-ART-MANIFEST.json').read_text())
    for number, digest in ART.items():
        data = v.resources[0, number]
        assert hashlib.sha256(data).hexdigest() == digest, 'Compiled apron art changed'
        assert data == (SOURCE / f'assets/resources/{number}.view.bin').read_bytes()
        entry = next(e for e in manifest['resources'] if e['view'] == number)
        assert entry['sha256'] == digest
        cel = decode_view(data)[0][0]
        assert (cel['width'], cel['height']) == (320, 144)
        paper = [cel['pixels'][y*320+x] for y in range(PAPER[1], PAPER[3])
                 for x in range(PAPER[0], PAPER[2])]
        assert Counter(paper) == {PAPER_COLOR: 1247, INK_COLOR: 209}
        decoded[number] = cel
        cases.append(f'VIEW{number} compiled/source/approved hash and independently decoded paper unchanged')
    assert hashlib.sha256(v.resources[7, 0]).hexdigest() == manifest['font0_sha256']
    # The typed VM loads only view/text/font payloads. Check its bound palette
    # file directly rather than inventing a palette-kernel implementation.
    palette = (v.checkpoint / 'assets/resources/999.palette.bin').read_bytes()
    assert palette == (SOURCE / 'assets/resources/999.palette.bin').read_bytes()
    assert hashlib.sha256(palette).hexdigest() == manifest['palette999_sha256']

    for room, label in ((0, 'PORCH'), (4, 'COURTYARD')):
        v = ApronFixture(build, room=room)
        before = state(v)
        v.call(v.instance(991), 'h6BaseDrawWorld', (v.h,))
        assert label in v.paint, 'Current room identification disappeared'
        assert any(name == 'DrawCel' and args[0] in ART for name, args in v.ktrace)
        assert state(v) == before
        issue(issues, not displays(v, 'RETURN'), f'{label}: redundant RETURN over baked return lettering')
        cases.append(f'{label} apron retains actual background/current room and no state mutation')

    for apron in (True, False):
        caption = 'SWIVEL RELEASE' if apron else 'ROTATE CLOCKWISE'
        payload = 419 if apron else 420
        for reveal, focused in ((False, False), (False, True), (True, False)):
            v = ApronFixture(build, apron=apron)
            controls = v.controls()
            assert controls[payload][1] == CONTROL
            if apron:
                assert controls[11][1] == (8, 102, 112, 134)
                assert controls[10][1] == (161, 52, 307, 130)
                assert v.hit(20, 122) == 11 and v.hit(250, 100) == 10
                assert v.hit(200, 136) == v.hit(200, 129) == 419
            before = state(v)
            assert v.call(v.instance(994), 'h12Draw') == 1
            assert state(v) == before, 'Label repair changed campaign/reader/owner state'
            static = displays(v, caption)
            assert len(static) == 1
            index, args = static[0]
            rect = display_rectangle(v, args)
            assert (CONTROL[0] <= rect[0] < rect[2] <= CONTROL[2]
                    and CONTROL[1] <= rect[1] < rect[3] <= CONTROL[3])
            assert rect[3]-rect[1] == 8, 'Required action caption wrapped'
            cleared, clear_boxes = restore_baked_ink(v, decoded[103], index)
            if apron:
                issue(issues, cleared, 'apron: baked audience lettering survives under required swivel caption')
            else:
                assert not clear_boxes, 'House-side paint must not clear apron paper'
            witness = v.arrays(994)['h12Paint']
            # This admitted fixture has epoch0, no acquired cue originals and
            # zero visible words. Preserve its whole existing physical witness.
            assert list(witness) == [1, 0, int(apron), 0, 0, 0, 0]
            assert not any(name == 'Graph' and a[0] == 12 for name, a in v.ktrace)

            v.h.p.update(uiReveal=int(reveal), uiFocus=controls[payload][0] if focused else 0)
            v.keep_controls = True
            v.ktrace.clear()
            v.call(v.h, 'uiRender')
            assert not v.h.p['uiFailure']
            dynamic = displays(v, caption)
            assert len(dynamic) == int(reveal or focused)
            if dynamic:
                dynamic_rect = display_rectangle(v, dynamic[0][1])
                issue(issues, rect == dynamic_rect,
                      f'{caption}: static and ordinary reveal/focus label glyph origins differ')
            if apron:
                assert v.hit(20, 122) == 11 and v.hit(250, 100) == 10 and v.hit(200, 136) == 419
            cases.append(f'{caption}/reveal{int(reveal)}/focus{int(focused)}: actual caption, glyph fit, paint witness and hit targets')

    for label, kwargs in (('inactive', {'active': False}),
                          ('other room', {'room': 3}),
                          ('successor', {'successor': True})):
        v = ApronFixture(build, **kwargs)
        before = state(v)
        assert v.call(v.instance(994), 'h12Draw') == 0
        assert not any(name in {'Graph', 'Display', 'DrawCel'} for name, _ in v.ktrace)
        assert state(v) == before
        assert list(v.arrays(994)['h12Paint']) == [0] * 7
        cases.append(label + ': real h12Draw guard does not paint, publish or mutate')

    if reference:
        assert any('redundant RETURN' in e for e in issues)
        assert any('baked audience' in e for e in issues)
        assert any('glyph origins differ' in e for e in issues)
    else:
        assert not issues, issues
    assert len(cases) == 13
    return {'status': ('REFERENCE_DEFECTS_REPRODUCED_NOT_NATIVE' if reference
                       else 'PASS_EMITTED_NOT_NATIVE'),
            'case_count': len(cases), 'cases': cases, 'observed_defects': sorted(set(issues)),
            'compile_receipt_sha256': hashlib.sha256((v.build / 'compile-receipt.json').read_bytes()).hexdigest(),
            'native_acceptance': False,
            'scope': 'Actual emitted background/P12 draw/control/reveal/hit paths and independent asset/font decoding',
            'fixtures': 'P12 scene admission, unrelated companion controls, preserving already-registered controls during UI drawing',
            'limits': 'No native pixels, ordinary progression, saves, sound, performance or acceptance'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build')
    parser.add_argument('--reference', action='store_true')
    args = parser.parse_args()
    print(json.dumps(run(args.build, args.reference), indent=2))
