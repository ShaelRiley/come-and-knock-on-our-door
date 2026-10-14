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


if __name__ == '__main__':
    main()
