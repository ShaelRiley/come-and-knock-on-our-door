#!/usr/bin/env python3
"""Finite MIDI restore: real emitted broker, explicit stock-kernel/save model.

This is not ScummVM, a native save, campaign progression, or audio acceptance.
The only story admissions modeled here are finite-cue eligibility and VC readiness.
The model adds the actual byte-serialized native hold and positive-hold EOT rule.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import os
import sys


def source_root():
    for p in Path(__file__).resolve().parents:
        if (p / 'tests/score/finite_vm.py').is_file():
            return p
    raise RuntimeError('Source root not found')


S = source_root()
sys.path[:0] = [str(S / 'tests/score')]
from finite_vm import FiniteVM, Object, signed


class HoldVM(FiniteVM):
    def __init__(self):
        super().__init__(instructions_per_tick=0)
        self.hold_calls = []
        self.story_admissions = []
        self.budget = 150000000
        # Explicit earlier-domain scalar admissions, never a campaign fixture.
        self.objects['contestState'].p.update(vcReady=1, vcBusy=0, vcLoading=0, vcUncertain=0)
        self.objects['p14State'].p['p14Phase'] = 5

    def call(self, obj, name, args=()):
        if (obj.module.number, name) in ((996, 'p14Ready'), (994, 'p12Ready')):
            self.story_admissions.append((obj.module.number, name, list(args)))
            return 1
        if obj.module.number == 994 and name == 'p12Present':
            self.story_admissions.append((994, name, list(args)))
            return int(tuple(args) == (16,))
        return super().call(obj, name, args)

    def _kernel(self, k, args):
        if self.knames[k] != 'DoSound':
            return super()._kernel(k, args)
        op = args[0]
        if op == 12:
            assert len(args) == 3 and isinstance(args[1], Object)
            obj = args[1]
            assert obj is self.objects['responsiveSound'] and obj in self.parsers
            self.hold_calls.append((obj.name, obj.p['number'], args[2]))
            self.parsers[obj]['hold'] = signed(args[2])
            return 0
        if op == 17:
            obj = args[1]
            assert obj in self.parsers
            p = self.parsers[obj]
            # SCI1.1 UpdateCues copies a pending native signal, consumes it,
            # and syncs ticker. A positive MIDI hold leaves the prior script
            # signal/live handle unchanged when the parser jumps to tick0.
            if p['signal']:
                obj.p['signal'] = signed(p['signal'])
                if p['signal'] == 65535:
                    obj.p['handle'] = 0
                    p.update(playing=False, status='stopped')
            p['signal'] = 0
            tick = p['tick']
            obj.p.update(min=tick // 3600, sec=tick % 3600 // 60,
                         frame=tick % 60 // 2, vol=p['volume'])
            if self.after_read:
                self.after_read(self, obj)
            return 0
        result = super()._kernel(k, args)
        if op == 6:
            self.parsers[args[1]].update(hold=-1, native_loop=1, eot_loops=0)
        if op == 8:
            self.parsers[args[1]]['hold'] = -1
        return result

    def advance(self, ticks):
        assert ticks >= 0
        for _ in range(ticks):
            self.now = signed(self.now + 1)
            for obj, p in self.parsers.items():
                if not p['playing'] or p['pauses'] or p['status'] != 'playing' or not p['native_loop']:
                    continue
                tick = p['tick'] + 1
                if tick >= p['end']:
                    # Actual MidiParser_SCI checks positive native hold after
                    # decrementing the finite loop; the base parser resets its
                    # clock on terminal EOT. No terminal tuple is invented.
                    p['native_loop'] -= 1
                    if p['native_loop'] or p['hold'] > 0:
                        p['eot_loops'] += 1
                    else:
                        p['signal'] = 65535
                    tick = 0
                    p['keys'].clear()
                p['tick'] = tick
                if p['native_loop']:
                    for ch, events in p['streams'].items():
                        for at, msg in events:
                            if at == tick:
                                self.apply_midi(obj, ch, msg, 'native')

    def setup(self, cue):
        a = self.arrays(943)
        sound = self.objects['responsiveSound']
        for name, value in [('rbSound', sound), ('rbEnabled', 1), ('fsEnabled', 1),
                            ('rbGenerationLo', 1), ('rbDesired', 151)]:
            a[name][0] = value
        if cue == 100:
            assert self.proc('rbPresentation', 0, 100, 0, 0) == 1
        else:
            a['fsTarget'][0] = cue
            a['rbDesired'][0] = cue
            if cue in (119, 121):
                assert self.proc('rbPresentation', 0, cue, 0, 0) == 1
            else:
                assert self.proc('rbScoreRequest', cue, 0, 1) == 1
        assert self.proc('rbValidate') == 1
        return sound

    def restore_paused(self):
        sound = self.objects['responsiveSound']
        assert self.proc('rbBeforeChooser') == 1
        p = self.parsers[sound]
        assert p['status'] == 'paused' and p['hold'] == -1
        state = self.snapshot()
        native = copy.deepcopy(p)
        # Explicit kernel serialization/reconstruction model: syncAsByte loads
        # saved -1 (ff) into int16 as255; saved paused slots skip Play's reset.
        native['hold'] = p['hold'] & 255
        native['pauses'] = 0
        self.restore(state)
        self.parsers = {sound: native}
        assert native['hold'] == 255 and self.snapshot() == state
        return sound


def run(reference=False):
    rows = []
    #119 is the exact observed failure; all mode4 cue paths share the unchanged
    # restore dispatch. Resource/no-native-hold coverage is separately bound.
    for cue in (119,):
        v = HoldVM()
        s = v.setup(cue)
        v.advance(12)
        assert v.proc('rbPresentationPosition') == 12
        v.arrays(943)['rpPosition'][0] = 12
        v.restore_paused()
        assert v.proc('rbRestoreBegin', s) == 1
        checkpoint = v.snapshot()
        checkpoint_native = copy.deepcopy(v.parsers[s])
        assert v.proc('rbRestoreResume', v.objects['contestState']) == 1
        p = v.parsers[s]
        if reference:
            assert p['hold'] == 255 and not v.hold_calls
        assert p['pauses'] == 0 and v.arrays(943)['rpPause'][0] == 0
        v.advance(p['end'] - 12 - 2)
        assert v.proc('rbPresentationPosition') == p['end'] - 2
        v.arrays(943)['rpPosition'][0] = p['end'] - 2
        v.advance(2)
        position = v.proc('rbPresentationPosition')
        if reference:
            assert position == -1 and p['eot_loops'] == 1
            assert s.p['handle'] is s and s.p['signal'] != -1
        else:
            assert position == 0 and p['eot_loops'] == 0, ('restored finite owner loops instead of native EOT', cue, p['hold'], position, p['eot_loops'], s.p['signal'], s.p['handle'])
            assert p['hold'] == 0 and v.hold_calls == [('responsiveSound', s.p['number'], 0)]
            assert s.p['handle'] == 0 and s.p['signal'] == -1
            assert v.arrays(943)['rpTerminal'][0] == 1
        rows.append(dict(case='finite-' + str(cue), native_hold=p['hold'], eot_position=position,
                         modeled_eot_loops=p['eot_loops'], instructions=v.steps))
    # Rejected restore paths must never gain a native normalization side effect.
    for case in ('wrong-owner', 'stale-generation', 'missing-checkpoint', 'invalid-pause', 'frozen-position'):
        v.restore(checkpoint)
        v.parsers = {s: copy.deepcopy(checkpoint_native)}
        v.hold_calls = []
        a = v.arrays(943)
        if case == 'wrong-owner':
            result = v.proc('rbRestoreBegin', v.objects['bed'])
        elif case == 'missing-checkpoint':
            a['rpRestoreCheckpoint'][0] = 0
            result = v.proc('rbRestoreResume', v.objects['contestState'])
        else:
            if case == 'stale-generation':
                def mutate(machine, _sound):
                    machine.arrays(943)['rbGenerationLo'][0] += 1
                    machine.after_read = None
                v.after_read = mutate
            elif case == 'frozen-position':
                a['rpFrozenPosition'][0] = 1
            else:
                a['rpPause'][0] = 0
                a['rpPauseSampleValid'][0] = 1
            result = v.proc('rbRestoreResume', v.objects['contestState'])
        assert result == 0 and not v.hold_calls, (case, result, v.hold_calls)
        rows.append(dict(case=case, rejected=True, normalization_calls=0, instructions=v.steps))
    return dict(status='PASS_REFERENCE_REPRODUCES_POSITIVE_HOLD_FAILURE' if reference else 'PASS',
                cases=rows, native_acceptance=False,
                scope='Actual emitted broker/restore/position/EOT guards with explicit native hold/save kernel model; story eligibility admissions modeled')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', type=Path, default=S / 'build/coherent')
    parser.add_argument('--reference', action='store_true')
    args = parser.parse_args()
    os.environ['CAKOOD_SCORE_BUILD'] = str(args.build.resolve())
    result = run(args.reference)
    result['receipt_sha256'] = hashlib.sha256((args.build / 'compile-receipt.json').read_bytes()).hexdigest()
    print(json.dumps(result, indent=2))
