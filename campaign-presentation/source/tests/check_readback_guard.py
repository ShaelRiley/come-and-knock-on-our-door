#!/usr/bin/env python3
"""Readback strict-guard factoring: actual emitted P13/P14 and text-bank checks.

The completed ancestor/serial ledger and earlier provider scalars are synthetic.
No native game, player progression, save, audio or responsiveness passes here.
Run: python tests/check_readback_guard.py [--build COMPILED_DIRECTORY]
"""
import argparse
from collections import Counter
import copy
import json

from check_date_transaction_guards import RealGuardFixture


class ReadbackFixture(RealGuardFixture):
    def __init__(self, build=None):
        self.prior_models = Counter()
        self.bank_validations = 0
        self.constructed_memo = False
        super().__init__(build)
        self.budget = 80000000
        self.h.p['uiInventoryExtent'] = 2
        self.arrays(0)['uiItems'][:2] = [25, 399]
        self.arrays(996)['h14Edit'][0] = 0
        self.arrays(996)['h14Date'][:] = [25] + [ord('X')] * 25 + [0] * 55
        self.arrays(987)['p06Words'][4] = 0

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        if key == (993, 'h11ReadMemo') and self.constructed_memo:
            # One compatibility case models admission to the existing R5 memo.
            # It must still execute original Base's physical readiness gates.
            self.prior_models[key] += 1
            return 1
        if key == (996, 'h14Fact'):
            self.prior_models[key] += 1
            return 1
        if key in {(985, 'hVCSession'), (985, 'hVCWinningHi')}:
            self.prior_models[key] += 1
            return 0
        if key == (985, 'hVCWinningLo'):
            self.prior_models[key] += 1
            return (1, 2, 3, 4)[args[0] - 1]
        if key in {(990, 'h9CardHeld'), (990, 'h9OwnershipValid')}:
            self.prior_models[key] += 1
            return 1
        if key == (0, 'campaignHeld'):
            assert tuple(args) == (25,)
            self.prior_models[key] += 1
            return 1
        return super().call(obj, name, args)

    def procedure(self, module, index, args):
        emitted = self.modules[module]
        return self.execute(self.h, emitted, 'export' + str(index),
                            emitted.layout['exports'][index], args)

    def execute(self, obj, emitted, name, pc, args):
        if emitted.number in (944, 946):
            self.prior_models[emitted.number, 'audio-notification'] += 1
            return 1
        if emitted.number == 999 and pc == emitted.layout['exports'][4]:
            self.bank_validations += 1
        return super().execute(obj, emitted, name, pc, args)

    def complete_source(self, source):
        p = self.instance(996)
        self.call(p, 'p14Begin', (source,))
        assert p.p['p14PresentationSource'] == source
        self.call(p, 'p14Acknowledge',
                  (source, self.call(p, 'p14SerialHi', (source + 16,)),
                   self.call(p, 'p14SerialLo', (source + 16,)), p.p['p14Epoch'],
                   self.call(p, 'p14SourceRecord', (source,)), 0, 0))
        assert self.call(p, 'p14Complete', (source,)) == 1


def prepare(build):
    v = ReadbackFixture(build)
    p = v.instance(996)
    assert v.call(p, 'h14Acquire') == 1
    for person in range(8):
        v.complete_source(person + 2)
        v.call(p, 'p14PinCard', (person,))
    v.complete_source(20)
    v.call(p, 'p14PinSignature')
    assert v.call(p, 'h14Ctx') == 1
    v.call(p, 'p14GivePencil')
    assert v.call(p, 'h14Ctx') == 1
    v.complete_source(21)
    assert v.call(p, 'h14Menu', (433,)) == 1
    assert v.call(p, 'h14Ctx') == 1
    ids = v.arrays(0)['uiChoiceIds'][:v.h.p['uiChoiceCount']]
    v.h.p['uiPage'] = ids.index(36)
    for phase in (0, 2, 1):
        assert v.call(p, 'h14MenuFrame', (phase,)) == 1
    return v


def run(build=None):
    v = prepare(build)
    p = v.instance(996)
    before = dict(v.calls)
    banks = v.bank_validations
    fields = tuple(v.h.p[k] for k in ('type', 'message', 'modifiers', 'x', 'y'))
    assert v.call(p, 'h14Choice', (256, 36)) == 1
    d = v.instance(982)
    assert d.p['sdActive'] == 1 and d.p['sdDocument'] == 1800 and d.p['sdFailure'] == 0
    assert d.p['sdPendingStart'] == 1 and d.p['sdArmed'] == 0 and d.p['sdAudioToken'] == -1
    assert d.p['sdPaintGeneration'] == -1
    assert v.arrays(996)['h14Reader'][:3] == [1, 1800, 22]
    delta = lambda module, name: v.calls[module, name] - before.get((module, name), 0)
    assert delta(995, 'h13Valid') == 7, 'Three duplicate readiness scans removed; seven stay actual'
    assert delta(996, 'p14Validate') == 6, 'Every original P14 domain validation remains actual'
    assert delta(996, 'h14HistoryValid') == 4, 'Every original frozen-history comparison remains actual'
    assert v.bank_validations - banks == 6, 'Every original immutable bank validation remains actual'
    assert fields == tuple(v.h.p[k] for k in ('type', 'message', 'modifiers', 'x', 'y'))
    assert v.call(p, 'p14Complete', (22,)) == 0, 'Unpainted opening never earns a reader receipt'
    cases = ['actual Choice36 preserves all P14/history/bank validators and five event fields']

    for kind in ('cargo', 'owner-history', 'P14-ledger', 'context', 'render-live', 'constructed-R5-memo'):
        q = copy.deepcopy(v)
        obj = q.instance(996)
        if kind == 'cargo':
            q.arrays(995)['h13Cargo'][3] = 1
        elif kind == 'owner-history':
            q.proc(999, 11, obj, 0, 0, 1)
        elif kind == 'P14-ledger':
            obj.p['p14DateLength'] = 81
        elif kind == 'context':
            obj.p['p14ContextValid'] = 0
        elif kind == 'render-live':
            q.arrays(0)['h11MainRead'][0] = 1
        else:
            q.arrays(0)['h11MainRead'][0] = 1
            q.arrays(996)['h14RenderMemo'][0] = 1
            q.arrays(995)['h13RenderMemo'][0] = 1
            q.arrays(995)['h13Cargo'][3] = 1
            q.constructed_memo = True
        old = dict(q.calls)
        result = q.call(obj, 'h14Match')
        assert result == (1 if kind == 'render-live' else 0), kind
        if kind == 'render-live':
            assert q.calls[996, 'h14Base'] - old.get((996, 'h14Base'), 0) == 1
            assert q.calls[995, 'h13ReadyPhysical'] - old.get((995, 'h13ReadyPhysical'), 0) == 2
        if kind == 'constructed-R5-memo':
            assert q.calls[996, 'h14Base'] - old.get((996, 'h14Base'), 0) == 1
            assert q.calls[995, 'h13ReadyPhysical'] - old.get((995, 'h13ReadyPhysical'), 0) == 1
            assert q.calls[996, 'h14Valid'] == old.get((996, 'h14Valid'), 0)
        assert q.call(obj, 'p14Complete', (22,)) == 0
        assert q.instance(982).p['sdAudioToken'] == -1
        cases.append(kind)
    return {'status': 'PASS_EMITTED_READBACK_GUARDS_NOT_NATIVE', 'case_count': len(cases),
            'cases': cases, 'native_acceptance': False,
            'fixture': 'Synthetic ledger/earlier baseline; actual P13/P14/history/context/bank validators. One explicitly modeled R5 memo admission.'}


def run_reopen(build=None):
    """Actual Choice36/menu/reader/domain guards; synthetic completion fixture.

    The earlier campaign providers are the existing explicit models. Completion
    is an actual domain Acknowledge call, not observed text/paint/native gameplay.
    SceneDialogue Close + h14Retire execute the ordinary close contract; full
    Main.uiClose is not claimed by this component test.
    """
    v = prepare(build)
    p, d = v.instance(996), v.instance(982)
    assert v.call(p, 'h14Choice', (256, 36)) == 1
    assert d.p['sdActive'] == 1 and d.p['sdDocument'] == 1800 and d.p['sdFailure'] == 0
    assert v.arrays(996)['h14Reader'][:3] == [1, 1800, 22]
    # Execute the actual current-source whole-record admission. This fixture
    # supplies the completed-readback precondition, never native page evidence.
    assert v.call(p, 'p14Complete', (22,)) == 0
    v.call(p, 'p14Acknowledge',
           (22, v.call(p, 'p14SerialHi', (38,)), v.call(p, 'p14SerialLo', (38,)),
            p.p['p14Epoch'], v.call(p, 'p14SourceRecord', (22,)), 0, 0))
    assert v.call(p, 'p14Complete', (22,)) == 1
    assert v.call(d, 'sdClose', (0,)) == 1
    assert v.call(p, 'h14Retire') == 1
    v.h.p.update(uiPanel=0, uiBackPanel=0)
    assert v.call(p, 'h14Menu', (433,)) == 1
    assert v.call(p, 'h14Ctx') == 1
    ids = v.arrays(0)['uiChoiceIds'][:v.h.p['uiChoiceCount']]
    v.h.p['uiPage'] = ids.index(36)
    for phase in (0, 2, 1):
        assert v.call(p, 'h14MenuFrame', (phase,)) == 1
    assert v.h.p['uiPanel'] == 2 and v.h.p['uiChoiceContext'] == 256
    assert v.arrays(996)['h14MenuPaint'][0] == 3

    def invariant():
        return dict(serials={k: value for k, value in p.p.items()
                             if k.endswith(('Hi', 'Lo')) and
                             not k.startswith(('p14Result', 'p14Presentation'))},
                    physical={k: p.p[k] for k in ('p14DateLength', 'p14Tone', 'p14Phase',
                              'p14CreditCount', 'p14CreditCursor', 'p14Paused', 'p14Skipped', 'p14Replay')},
                    date=list(v.arrays(996)['h14Date']),
                    owner=list(v.arrays(996)['h14Owner']),
                    frozen_history=list(v.arrays(999)['fbOwnerHistory']))
    before = invariant()
    assert v.call(p, 'h14Choice', (256, 36)) == 1
    observed = dict(active=d.p['sdActive'], document=d.p['sdDocument'], failure=d.p['sdFailure'],
                    reader=list(v.arrays(996)['h14Reader'][:3]), panel=v.h.p['uiPanel'],
                    presentation_source=p.p['p14PresentationSource'])
    assert observed['active'] == 1 and observed['document'] == 1800 and observed['failure'] == 0 and observed['reader'] == [1, 1800, 22], ('COMPLETED_READBACK_REOPEN_REFUSED', observed)
    assert v.h.p['uiPanel'] == 4 and d.p['sdPage'] == 0 and d.p['sdCount'] == 2
    assert p.p['p14PresentationSource'] == 22
    assert (p.p['p14PresentationHi'], p.p['p14PresentationLo']) == (v.call(p, 'p14SerialHi', (38,)), v.call(p, 'p14SerialLo', (38,)))
    assert v.arrays(996)['p14Lease'][22] == p.p['p14Epoch']
    assert v.call(p, 'h14DateMatch') == 1 and v.call(p, 'h14ReaderCheck') == 1
    assert invariant() == before, 'Reopening must not alter serials/date/owner/history'
    cases = ['actual painted-menu Choice36 reopens completed dynamic1800 with renewed typed lease and unchanged ledger']

    # Explicit hostile component mutations; never applied to a native game/save.
    reader = v.arrays(996)['h14Reader']
    reader[2] = 0
    assert v.call(p, 'h14DateBind') == 0 and v.call(p, 'h14DateMatch') == 0
    reader[2] = 22
    assert v.call(p, 'h14DateMatch') == 1
    cases.append('source0 still cannot bind/reuse the exact dynamic readback')
    epoch = p.p['p14Epoch']
    p.p['p14Epoch'] = epoch + 1
    assert v.call(p, 'h14DateMatch') == 0
    p.p['p14Epoch'] = epoch
    assert v.call(p, 'h14DateMatch') == 1
    cases.append('stale date-bank epoch is rejected')
    v.arrays(996)['h14Owner'][0] = 0
    assert v.call(p, 'h14DateMatch') == 0
    v.arrays(996)['h14Owner'][0] = 1
    assert v.call(p, 'h14DateMatch') == 1
    cases.append('wrong successor owner cannot admit the reader')
    v.arrays(996)['p14Lease'][22] = epoch - 1
    v.call(p, 'p14Acknowledge',
           (22, v.call(p, 'p14SerialHi', (38,)), v.call(p, 'p14SerialLo', (38,)),
            epoch, v.call(p, 'p14SourceRecord', (22,)), 0, 0))
    assert p.p['p14Code'] == 59, ('Expected original CODE_STALE_PRESENTATION', p.p['p14Code'])
    assert invariant() == before
    cases.append('wrong source lease cannot acknowledge even an already-complete source')
    return dict(status='PASS_EMITTED_COMPLETED_READBACK_REOPEN_NOT_NATIVE', case_count=len(cases),
                cases=cases, native_acceptance=False, instructions=v.steps,
                limits='Synthetic completed ancestors/domain ACK and modeled kernel operations; actual emitted Choice36/menu/context/P13/P14/history/bank/close contract. No native text, audio, input or save acceptance.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build')
    parser.add_argument('--reopen', action='store_true')
    args = parser.parse_args()
    print(json.dumps(run_reopen(args.build) if args.reopen else run(args.build), indent=2))
