#!/usr/bin/env python3
"""Emitted date transaction guards with explicit synthetic completed ancestors.

Actual h14Base, P13 readiness/history/domain and physical predicates execute.
P1-P12 baseline admission and independent predecessor/pot-word providers are
modeled. The fixture is not earned progression, a saved game or native proof.

Run after building: python tests/check_date_transaction_guards.py
Use --build PATH to select another compiled candidate.
"""
import argparse
from collections import Counter, deque
import json

from presentation_vm import PresentationVM, base


FIELDS = ('type', 'message', 'modifiers', 'x', 'y')
OBJECTS = (2, 8, 28, 85, 30, 54, 29)
ORIGINS = (2, 1, 0, 3, 3, 3, 4)


def key(message, event_type=4, tag=None):
    return dict(type=event_type, message=message, modifiers=2, x=31, y=117,
                tag=tag if tag is not None else str((event_type, message)))


class NormalEngineQuit(Exception):
    pass


class RealGuardFixture(PresentationVM):
    """Real current guards with an explicitly synthetic completed predecessor."""
    def __init__(self, build=None, text='seed'):
        super().__init__(build)
        self.pending_events = deque()
        self.polls = []
        self.consumed = []
        self.on_consume = None
        self.observed = Counter()
        self.modeled = Counter()
        self.baseline_good = True
        self.barrier = False
        self.h6_barrier = False
        self.h.p.update(location=4, p02Revision=100, motionX=150, motionY=140,
                        motionPhase=0, onApron=0, opening=0, paused=0,
                        menuOpen=0, uiPanel=0, uiFailure=0, bridgeFailure=0,
                        type=4, message=ord('A'), modifiers=2, x=31, y=117)
        a = self.arrays(995)
        a['h13Lease'][:] = [1, 1, 0, 0]
        a['h13History'][0] = 2
        a['h13Cargo'][:] = [4, 4, 4, 4]
        for i, (obj, origin) in enumerate(zip(OBJECTS, ORIGINS)):
            b = i * 12
            route = {0: (2, 1, 4), 1: (1, 4), 2: (0, 1, 4),
                     3: (3, 4), 4: (3, 4), 5: (3, 4), 6: (4,)}[i]
            for offset, value in {0: obj, 1: origin, 2: 4, 4: origin,
                                  5: len(route), 6: len(route)-1, 9: 1}.items():
                a['h13Actors'][b+offset] = value
            a['h13History'][88+b] = origin
            for j, (source, target) in enumerate(zip(route, route[1:])):
                e = i * 256 + j * 4
                a['h13Edges'][e:e+4] = [source, target, j+1, j+2]
        # Independent provider vectors: never read through the mutable snapshot.
        self.predecessor_words = tuple(a['h13History'])
        self.pot_words = tuple(a['h13PotHistory'])
        p = self.instance(995)
        p.p.update(p13Initialized=1, p13ContextValid=1)
        serials = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 28: 6, 45: 7,
                   6: 8, 7: 9, 29: 10, 46: 11, 47: 12, 48: 13,
                   49: 14, 50: 15, 8: 16, 9: 17, 30: 18, 51: 19,
                   10: 20, 0: 20}
        for slot, serial in serials.items():
            assert self.call(p, 'p13SetSerial', (slot, 0, serial)) == 1
        # Synthetic but strictly validated cargo/actor history, not native proof.
        for i, row in enumerate((
                [2, 0, 2, 1, 3, 0, 2, 0, 0, 1],
                [4, 0, 4, 1, 2, 0, 0, 0, 0, 1],
                [6, 0, 8, 1, 2, 0, 1, 0, 1, 1],
                [9, 0, 17, 1, 2, 0, 1, 0, 0, 1])):
            a['h13Deliveries'][i*10:i*10+10] = row
            a['h13DeliveryFrames'][i] = row[4]
        a['h13ServePaint'][:] = [0, 5, 3]
        a['h13ScenePaint'][:] = [0, 9, 3, 0, 16, 3, 0, 20, 3]
        e = self.arrays(996)
        assert 0 <= len(text) <= 80 and all(32 <= ord(c) <= 126 for c in text)
        e['h14Edit'][:] = [1, len(text), 0, 1, 0]
        e['h14EditChars'][:] = list(map(ord, text)) + [0] * (80-len(text))
        e['h14Date'][:10] = [9, *map(ord, 'UNCHANGED')]
        self.observed.clear()
        self.modeled.clear()
        self.calls.clear()
        self.steps = 0

    def call(self, obj, name, args=()):
        k = (obj.module.number, name)
        self.observed[k] += 1
        if k == (995, 'h13Baseline'):
            self.modeled[k] += 1
            return int(self.baseline_good)
        if k == (994, 'h13PredecessorWord'):
            self.modeled[k] += 1
            return self.predecessor_words[args[0]]
        if k == (988, 'p07Read'):
            self.modeled[k] += 1
            return self.pot_words[args[0]]
        if k == (985, 'hBarrier'):
            self.modeled[k] += 1
            return int(self.barrier)
        if k == (987, 'h6Barrier'):
            self.modeled[k] += 1
            return int(self.h6_barrier)
        return super().call(obj, name, args)

    def kernel(self, number, args):
        if self.knames.get(number) != 'GetEvent':
            return super().kernel(number, args)
        assert len(args) == 2 and args[1] is self.h
        mask = args[0] & 0xffff
        assert mask in (0xffff, 0x7fff), 'No keyboard-only search or queue skipping'
        peek = bool(mask & 0x8000)
        self.polls.append({'mask': mask, 'peek': peek})
        event = self.pending_events[0] if self.pending_events else dict(
            type=0, message=0, modifiers=0, x=319, y=199)
        if event['type'] == 2048:
            raise NormalEngineQuit('Modeled stock kGetEvent aborts on Quit, even peek')
        self.h.p.update({field: base.signed(event[field]) for field in FIELDS})
        if event['type'] and not peek:
            self.pending_events.popleft()
            self.consumed.append(dict(event))
            if self.on_consume:
                self.on_consume(dict(event), len(self.consumed))
        return int(bool(event['type']))

    def input(self, message, event_type=4):
        self.h.p.update(type=event_type, message=message)
        return self.call(self.instance(996), 'h14Input')

    def fields(self):
        return {field: self.h.p[field] for field in FIELDS}

    def text(self):
        a = self.arrays(996)
        return ''.join(chr(c) for c in a['h14EditChars'][:a['h14Edit'][1]])

    def date(self):
        a = self.arrays(996)['h14Date']
        return ''.join(chr(c) for c in a[1:a[0]+1])

    @property
    def stats(self):
        return {'instructions': self.steps,
                'actual_methods': {f'{m}:{n}': v for (m,n),v in sorted(self.calls.items())},
                'modeled_calls': {f'{m}:{n}': v for (m,n),v in sorted(self.modeled.items())},
                'consumed_extra_events': len(self.consumed), 'polls': len(self.polls)}


def assert_retired(v):
    a = v.arrays(996)
    assert a['h14Batch'][0] == 0
    assert not any(a['h14BatchEdit']) and not any(a['h14BatchChars'])


def run(build=None):
    cases = []
    v = RealGuardFixture(build, '')
    v.pending_events.extend([key(32768, 8), key(ord('B')), key(32768, 8)] +
                            [key(ord('C') + i//2) if i % 2 == 0 else key(32768, 8)
                             for i in range(28)] + [key(ord('Z'))])
    assert v.input(ord('A')) == 1
    assert len(v.consumed) == 31 and len(v.pending_events) == 1
    assert len(v.text()) == 16 and v.text().startswith('AB')
    assert v.calls[996, 'h14Base'] == 2
    assert v.calls[995, 'h13ReadyPhysical'] == 2
    assert v.calls[995, 'h13Valid'] == 2 and v.calls[995, 'h13Historical'] == 2
    assert v.calls[995, 'p13Validate'] == 2
    assert v.modeled[994, 'h13PredecessorWord'] == 2*2064
    assert v.modeled[988, 'p07Read'] == 2*199
    assert v.date() == 'UNCHANGED' and v.arrays(996)['h14Edit'][3:5] == [0, 0]
    assert v.fields() == {f: base.signed(v.consumed[-1][f]) for f in FIELDS}
    assert not any(name in ('Graph', 'Display', 'DrawCel') for name, _ in v.ktrace)
    assert_retired(v)
    positive_stats = v.stats
    cases.append('32-event bounded transaction executes both real full endpoint chains; 16 chars; no commit/paint')

    def captured(v):
        v.arrays(995)['h13History'][200] ^= 1
    def underlying(v):
        words = list(v.predecessor_words); words[200] ^= 1
        v.predecessor_words = tuple(words)
    def actor(v):
        v.arrays(995)['h13Actors'][0] = 8
    def tail(v):
        v.arrays(995)['h13Edges'][255] = 1
    def delivery(v):
        v.arrays(995)['h13Deliveries'][2] += 1
    def serial(v):
        v.instance(995).p['p13RevisionLo'] = 1
    mutations = [('captured predecessor word', captured), ('underlying predecessor word', underlying),
                 ('actor identity', actor), ('unused route tail', tail),
                 ('delivery serial', delivery), ('domain serial ceiling', serial)]
    for label, mutation in mutations:
        v = RealGuardFixture(build)
        old_chars = list(v.arrays(996)['h14EditChars'])
        mutation(v)
        v.pending_events.append(key(ord('B')))
        assert v.input(ord('A')) == 1
        assert not v.polls and len(v.pending_events) == 1
        assert v.text() == 'seed' and list(v.arrays(996)['h14EditChars']) == old_chars
        assert not v.arrays(996)['h14Edit'][0] and v.date() == 'UNCHANGED'
        assert_retired(v)
        cases.append('strict entry rejects ' + label + ' before editing or polling')
        v = RealGuardFixture(build)
        old_chars = list(v.arrays(996)['h14EditChars'])
        v.pending_events.extend([key(ord('B')), key(ord('C'))])
        v.on_consume = lambda event, index, v=v, mutation=mutation: mutation(v) if index == 1 else None
        assert v.input(ord('A')) == 1
        assert v.calls[996, 'h14Base'] == 2
        assert v.text() == 'seed' and list(v.arrays(996)['h14EditChars']) == old_chars
        assert v.arrays(996)['h14Edit'][0] == 0
        assert v.arrays(996)['h14Edit'][3:5] == [0, 0] and v.date() == 'UNCHANGED'
        assert_retired(v)
        cases.append('real strict exit discards all tentative edits after ' + label + ' invalidation')

    for args in ((1,), (0,), (1, 2)):
        v = RealGuardFixture(build)
        before = list(v.arrays(996)['h14EditChars'])
        assert v.call(v.instance(996), 'h14Input', args) == 1
        assert list(v.arrays(996)['h14EditChars']) == before
        assert v.calls[996, 'h14Base'] == 0 and v.date() == 'UNCHANGED'
        assert_retired(v)
    cases.append('internal optional calls outside transaction have no edit authority')

    def nested(v):
        assert v.call(v.instance(996), 'h14Input') == 1
    def wrong_mode(v):
        assert v.call(v.instance(996), 'h14Input', (0,)) == 1
    def wrong_argc(v):
        assert v.call(v.instance(996), 'h14Input', (1, 2)) == 1
    def save(v):
        assert v.call(v.instance(996), 'h14Save') == 0
    poisons = [('nested ordinary input', nested), ('wrong internal mode', wrong_mode),
               ('wrong internal argc', wrong_argc), ('active-batch Save refusal', save)]
    for label, poison in poisons:
        v = RealGuardFixture(build)
        v.pending_events.extend([key(ord('B')), key(ord('C'))])
        v.on_consume = lambda event, index, v=v, poison=poison: poison(v) if index == 1 else None
        assert v.input(ord('A')) == 1 and v.calls[996, 'h14Base'] == 2
        assert v.text() == 'seed' and v.date() == 'UNCHANGED'
        assert v.arrays(996)['h14Edit'][0] == 0 and len(v.pending_events) == 1
        assert_retired(v)
        cases.append(label + ' poisons transaction; no date commit or backup authority remains')

    changes = [('room', lambda v: v.h.p.update(location=1)),
               ('revision', lambda v: v.h.p.update(p02Revision=101)),
               ('motion', lambda v: v.h.p.update(motionPhase=1)),
               ('position', lambda v: v.h.p.update(motionX=151)),
               ('owner', lambda v: v.arrays(996)['h14Owner'].__setitem__(0, 1)),
               ('replay', lambda v: v.arrays(997)['h14ReplayMeta'].__setitem__(0, 1)),
               ('pause', lambda v: v.h.p.update(paused=1)),
               ('menu', lambda v: v.h.p.update(menuOpen=1)),
               ('bridge failure', lambda v: v.h.p.update(bridgeFailure=1))]
    for label, change in changes:
        v = RealGuardFixture(build)
        v.pending_events.extend([key(ord('B')), key(ord('C'))])
        v.on_consume = lambda event, index, v=v, change=change: change(v) if index == 1 else None
        assert v.input(ord('A')) == 1 and v.calls[996, 'h14Base'] == 2
        assert v.text() == 'seed' and v.date() == 'UNCHANGED'
        assert not v.arrays(996)['h14Edit'][0]
        assert_retired(v)
        cases.append('identity/context change (' + label + ') cancels unpublished bank')

    return {'status': 'PASS_EMITTED_NOT_NATIVE', 'case_count': len(cases), 'cases': cases,
            'positive_stats': positive_stats, 'native_acceptance': False,
            'actual_validation': ['h14Base', 'h13ReadyPhysical', 'h13Valid', 'h13Historical',
                                  'p13Validate', 'actor/edge/work/delivery predicates',
                                  'serve and all three scene-serial acknowledgements'],
            'modeled_boundaries': ['Completed P1-P12 h13Baseline admission',
                                   'Independent fixed 2064 predecessor + 199 pot-history words',
                                   'Earlier hBarrier/h6Barrier absence'],
            'synthetic_setup': 'P13 serial ledger and physical routes/receipts seeded only in emitted VM; no saved game or earned progress.',
            'limits': 'No native gameplay, speed, delivery, save compatibility, pixels, sound or release acceptance.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build')
    args = parser.parse_args()
    print(json.dumps(run(args.build), indent=2))
