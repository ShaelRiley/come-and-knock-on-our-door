#!/usr/bin/env python3
"""Emitted owner/read-scope boundaries; modeled prerequisite history only.

These checks earn no progress and create no native save or acceptance.
"""
import json
from presentation_vm import PresentationVM


class ScopeFixture(PresentationVM):
    def __init__(self):
        super().__init__()
        self.history_good = True
        self.history_calls = 0
        self.h.p.update(p08=self.instance(989), location=4, p02Revision=1,
                        motionX=0, motionY=0, motionPhase=0, onApron=0)
        self.instance(989).p.update(h8Host=self.h, h8Lease=1)
        self.arrays(0)['h11MainRead'][0] = 1
        self.arrays(993)['h11OwnerState'][0] = 1
        self.arrays(993)['h11OwnerState'][3] = 1

    def call(self, obj, name, args=()):
        if (obj.module.number, name) == (993, 'h11OwnerHistory'):
            self.history_calls += 1
            return int(self.history_good)
        return super().call(obj, name, args)

    def begin(self):
        p = self.instance(993)
        assert self.call(p, 'h11ReadBegin') == 1
        assert self.call(p, 'h11ReadResume') == 1
        assert self.call(p, 'h11ReadMemo') == 1
        return p


def main():
    v = ScopeFixture(); p = v.begin(); n = v.history_calls
    for _ in range(10):
        assert v.call(p, 'h11OwnerValid') == 1
    assert v.history_calls == n, 'Repeated paint queries must reuse only the live proof'
    assert v.call(p, 'h11ReadEnd') == 1
    assert v.history_calls > n, 'End must run the full owner check'
    assert v.call(p, 'h11ReadFinish') == 1
    v.history_good = False
    assert v.call(p, 'h11OwnerValid') == 0, 'Outside paint must remain strict'

    denied = ScopeFixture(); p = denied.begin(); denied.history_good = False
    assert denied.call(p, 'h11ReadBoundary') == 0
    assert denied.arrays(993)['h11Read'][2] == 1
    assert denied.call(p, 'h11OwnerValid') == 0

    changed = ScopeFixture(); p = changed.begin()
    changed.arrays(993)['h11PrereqWords'][200] ^= 1
    assert changed.call(p, 'h11ReadEnd') == 0, 'Full proof comparison catches raw mutation'
    assert changed.arrays(993)['h11Read'][2] == 1

    moved = ScopeFixture(); p = moved.begin(); moved.h.p['motionX'] = 1
    assert moved.call(p, 'h11ReadMemo') == 0, 'Physical mismatch invalidates paint reuse'
    assert moved.call(p, 'h11ReadEnd') == 0
    print(json.dumps({'status': 'PASS_NOT_NATIVE', 'cases': 4,
                      'scope': 'Actual emitted read guard, owner validator and boundaries; modeled prerequisite history',
                      'native_acceptance': False}))


def late_menu_phase0(build=None, reference=False):
    from check_date_modal import DateFixture
    class TraceFixture(DateFixture):
        def __init__(self):
            super().__init__(build)
            self.phase0 = []
            self.timeline = []
            self.receipts = []
        def call(self, obj, name, args=()):
            key = (obj.module.number, name)
            if key[0] == 996 and name in ('h14MenuFrame', 'h14Frame'):
                if tuple(args) == (0,):
                    live = PresentationVM.call(self, self.instance(993), 'h11ReadMemo')
                    self.phase0.append((name, bool(live)))
                if tuple(args) == (1,):
                    self.timeline.append((name, 1))
                    self.receipts.append(name)
            if key[0] == 993 and name in ('h11ReadEnd', 'h11ReadFinish'):
                self.timeline.append((name, 'start'))
                value = super().call(obj, name, args)
                self.timeline.append((name, 'done', value))
                return value
            return super().call(obj, name, args)
    rows = []
    expected = [('h14MenuFrame', False), ('h14Frame', False)] if reference else [('h14Frame', False), ('h14MenuFrame', True)]
    for panel in (0, 2, 4):
        v = TraceFixture()
        v.h.p.update(uiPanel=panel, uiChoiceContext=256, uiChoiceCount=1)
        v.render()
        assert v.phase0 == expected, v.phase0
        assert v.arrays(996)['h14Edit'][3] == 1
        end = v.timeline.index(('h11ReadEnd', 'done', 1))
        menu = v.timeline.index(('h14MenuFrame', 1))
        frame = v.timeline.index(('h14Frame', 1))
        finish = v.timeline.index(('h11ReadFinish', 'start'))
        assert end < menu < frame < finish, v.timeline
        rows.append({'panel': panel, 'phase0_guarded': v.phase0,
                     'success_order': 'strict End then original phase1 receipts then Finish'})
    failures = []
    for physical in (True, False):
        v = TraceFixture()
        v.h.p.update(uiPanel=2, uiChoiceContext=256, uiChoiceCount=1)
        if physical:
            v.before_overlay_mutation = lambda q: q.h.p.__setitem__('motionX', q.h.p['motionX'] + 1)
        else:
            v.before_overlay_mutation = lambda q: q.arrays(993)['h11PrereqWords'].__setitem__(200, q.arrays(993)['h11PrereqWords'][200] ^ 1)
        v.render()
        assert v.phase0 == expected
        assert ('h11ReadEnd', 'done', 0) in v.timeline
        assert ('h11ReadFinish', 'start') in v.timeline
        assert not v.receipts, v.timeline
        assert v.arrays(996)['h14Edit'][3] == 0
        assert v.arrays(996)['h14MenuPaint'][0] != 3
        assert v.arrays(996)['h14Reader'][11:13] == [0, 0]
        assert v.arrays(996)['h14Reader'][19] == 0
        assert v.instance(982).p['sdPaintGeneration'] == -1
        failures.append('physical motion witness' if physical else 'raw owner proof word')
    return {'status': 'PASS_REFERENCE_ORIGINAL_MENU_PHASE0_NOT_NATIVE' if reference else 'PASS_EMITTED_LATE_MENU_PHASE0_NOT_NATIVE',
            'native_acceptance': False, 'cases': rows,
            'strict_End_failures': failures,
            'failure_order': 'End rejects, no phase1 receipt calls, original Finish retires staging',
            'scope': 'Actual compiled Main.render and original phase0/End/Finish under explicit DateFixture ancestor admission. Menu0 alone moves into guarded scope; Frame0 and freeze lifecycle remain outside, unchanged. Default owner-scope tests remain unchanged.',
            'limits': ['No native performance or campaign acceptance.', 'Full h14Frame0 relocation is excluded from this candidate.']}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--late-menu-phase0', action='store_true')
    parser.add_argument('--reference', action='store_true')
    parser.add_argument('--build')
    args = parser.parse_args()
    if args.late_menu_phase0:
        print(json.dumps(late_menu_phase0(args.build, args.reference)))
    else:
        main()
