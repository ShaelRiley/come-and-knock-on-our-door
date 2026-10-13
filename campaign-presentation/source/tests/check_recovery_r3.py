#!/usr/bin/env python3
"""Emitted regressions with explicit ancestor, domain and arrival fixtures.

No fixture earns campaign progress, creates a native save or accepts pixels.
The restore test runs the actual host finalizer, prerequisite projection,
contest world check, owner lease check, context setter and session binder.
Unrelated ancestor/domain admissions are modeled and reported as such.
"""
import argparse
import json

from presentation_vm import PresentationVM, base
from check_recovery_regressions import RecoveryFixture


class RestoreFixture(PresentationVM):
    def __init__(self, build=None):
        super().__init__(build)
        self.context_leases = []
        self.h.p.update(location=4, onApron=0, motionPhase=0,
                        motionX=18432, motionY=8192, motionLoop=0,
                        p02PlanAgreed=1, uiPanel=2, uiChoiceContext=218,
                        uiChoiceCount=2, uiPage=0)
        for prop, number in [('p03', 983), ('p04', 984), ('p05', 985),
                             ('p06', 987), ('p07', 988), ('p08', 989)]:
            self.h.p[prop] = self.instance(number)
        self.instance(983).p.update(p03Ready=1, p03Padding=1)
        self.instance(985).p['hRestoreValid'] = 1
        self.instance(987).p['h6RestoreValid'] = 1
        self.instance(988).p['h7RestoreValid'] = 1
        p = self.instance(989)
        p.p.update(h8Host=self.h, h8Lease=1, h8Restoring=1,
                   h8RestoreValid=0, h8Enabled=0, p08Ready=0)
        self.arrays(989)['p08Session'][7] = 1
        owner = self.arrays(993)
        owner['h11OwnerState'][0:4] = [1, 0, 5, 1]
        for i in range(5):
            owner['h11Owners'][12 * i + 6] = 1
        q = self.instance(985)
        q.p.update(hHost=self.h, hContest=self.instance(986),
                   hContestEnabled=1, hVCEncounter=4, hVCSession=1,
                   hVCShown=0, hVCStage=1, hVCRoom=4,
                   hVCJackX=18432, hVCJackY=8192, hVCJackLoop=0)
        ui = self.arrays(0)
        ui['uiChoiceIds'][0:2] = [1, 2]
        ui['uiChoiceEnabled'][0:2] = [1, 1]
        ui['uiChoiceLabels'][0] = self.call(q, 'hVCReplyLabel', (21,))
        ui['uiChoiceLabels'][1] = self.call(q, 'hVCLabel', (13,))

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        if key in {(989, 'h8PublishersReady'), (989, 'h8OwnersValid'),
                   (989, 'h8ClothRawValid'), (989, 'h8InventoryRawValid'),
                   (989, 'h8ReaderRestore'), (993, 'h11OwnerValid'),
                   (983, 'p03Validate'), (984, 'p04Validate'),
                   (984, 'p04Ready'), (987, 'h6SaveReady'),
                   (988, 'h7SaveReady'), (985, 'hVCRoutesReady'),
                   (985, 'hPhysicalValid'), (985, 'hContext'),
                   (985, 'p05SaveReady'), (986, 'vcSaveReady'),
                   (0, 'p05RetireTransient')}:
            return 1
        if key == (989, 'h8Preparations'):
            self.context_leases.append(self.instance(989).p['h8Lease'])
        if key == (989, 'p08ValidateCurrent'):
            return int(not (obj.p['p08Ready'] and obj.p['p08ContextValid']))
        if key in {(983, 'p03Ready'), (983, 'p03Padding')}:
            return 1
        if key in {(985, 'p05Flags'), (987, 'p06Projection')}:
            return 7
        if key == (988, 'p07Projection'):
            return 2
        if key == (986, 'vcFlags'):
            return 51
        if key == (986, 'vcRead'):
            return {90: 1, 91: 4, 92: 4, 98: 21}.get(args[0], 0)
        if key == (995, 'h13Has'):
            return 1
        if key in {(995, 'h13Room'), (995, 'h13VCAdmission')}:
            ready = super().call(self.instance(993), 'h11OwnerReady')
            return (4 if ready else -1) if name == 'h13Room' else ready
        return super().call(obj, name, args)


def restore_order(build, reference):
    v = RestoreFixture(build)
    restored = v.call(v.instance(989), 'h8RestoreFinish')
    if reference:
        assert restored == 0 and v.context_leases == [2]
    else:
        assert restored == 1 and v.context_leases == [1]
        assert v.instance(989).p['h8Lease'] == 2
        assert v.instance(989).p['h8RestoreValid'] == 1
        assert v.instance(989).p['p08ContextValid'] == 1
        assert v.arrays(989)['p08Session'][7] == 2
        for i in range(5):
            denied = RestoreFixture(build)
            denied.arrays(993)['h11Owners'][12 * i + 6] = 0
            assert denied.call(denied.instance(989), 'h8RestoreFinish') == 0
            assert denied.instance(989).p['h8Lease'] == 1
            assert denied.instance(989).p['h8Failure'] == 21
    return {'restored': bool(restored), 'context_validation_leases': v.context_leases,
            'denied_incomplete_owners': 0 if reference else 5}


class ArrivalFixture(RecoveryFixture):
    def __init__(self, build=None):
        super().__init__(build)
        self.requests = []
        self.readers = []

    def call(self, obj, name, args=()):
        key = (obj.module.number, name)
        if key == (0, 'motionRequest'):
            self.requests.append(tuple(args))
            # Model elapsed walking only. Dispatch the actual retained action,
            # object and target through Main's unchanged arrival method.
            return super().call(self.h, 'bridgeActAtArrival', tuple(args[2:]))
        if key in {(992, 'h10Stop'), (995, 'h13Dispatch'),
                   (996, 'h14Dispatch')}:
            return 0
        if key == (0, 'campaignReachable'):
            return 1
        if key == (0, 'campaignHeld'):
            return 0
        if key in {(0, 'speechCancel'), (0, 'motionCancel')}:
            return 1
        if key == (994, 'h12Open'):
            self.readers.append(args[0])
            return 1
        return super().call(obj, name, args)


def apron_route(build, reference):
    v = ArrivalFixture(build)
    v.h.p.update(location=4, onApron=1, uiPanel=0, motionPhase=0)
    verb = v.call(v.h, 'uiHostDefaultVerb', (410,))
    v.call(v.h, 'uiHostAct', (verb, 410, 0))
    ids = list(v.arrays(0)['uiChoiceIds'][:v.h.p['uiChoiceCount']])
    if reference:
        assert verb == 5 and v.readers == [6] and ids == []
    else:
        assert verb == 2 and ids == [5, 6, 8]
        assert v.requests[-1][2:] == (2, 410, 0)
        v.h.p.update(uiPanel=0, uiChoiceCount=0)
        v.call(v.h, 'uiHostAct', (5, 410, 0))
        assert v.readers == [6], 'Explicit Look must retain the authored reader'
    return {'default_verb': verb, 'ordinary_arrival_menu_ids': ids,
            'scope': 'Emitted default/action/arrival/menu; elapsed-walk fixture'}


class SceneFixture(PresentationVM):
    def __init__(self, build=None):
        super().__init__(build)
        self.h.p.update(location=4, onApron=0, uiPanel=0, p02Revision=1)
        a = self.arrays(995)
        a['h13Lease'][0:2] = [1, 1]
        for i, obj in enumerate((2, 8, 28, 85, 30, 54, 29)):
            a['h13Actors'][12 * i] = obj
            a['h13Actors'][12 * i + 2] = 4

    def call(self, obj, name, args=()):
        if (obj.module.number, name) in {(995, 'h13Active'), (995, 'h13Valid')}:
            return 1
        return super().call(obj, name, args)

    def choices(self, obj):
        self.call(self.instance(995), 'h13Menu', (obj,))
        a = self.arrays(0)
        assert not self.h.p['uiFailure']
        return {a['uiChoiceIds'][i]: bool(a['uiChoiceEnabled'][i])
                for i in range(self.h.p['uiChoiceCount'])}

    def room(self, obj, room):
        self.arrays(995)['h13Actors'][12 * (2, 8, 28, 85, 30, 54, 29).index(obj) + 2] = room


def speaker_availability(build, reference):
    v = SceneFixture(build)
    assert v.choices(410)[2]
    v.room(2, 2)
    if reference:
        assert v.choices(410)[2]
        return {'absent_speaker_was_enabled': True}
    assert not v.choices(410)[2]
    v.room(2, 4); v.room(8, 1)
    assert not v.choices(410)[2]
    v.room(8, 4)
    p = v.instance(995)
    p.p.update(p13ServedLo=10, p13ScreenLo=11)
    v.arrays(995)['h13ServePaint'][:] = [0, 10, 1]
    v.arrays(995)['h13ScenePaint'][0:3] = [0, 11, 1]
    assert v.choices(30)[17] and v.choices(30)[18]
    for absent in (2, 29):
        v.room(absent, 2)
        assert not v.choices(30)[18] and v.choices(30)[17]
        v.room(absent, 4)
    v.h.p['location'] = 3
    assert not v.choices(30)[17] and not v.choices(30)[18]
    v.h.p['location'] = 4
    assert not v.choices(2)[14]
    v.h.p['location'] = 2; v.room(2, 2)
    assert v.choices(2)[14]
    v.room(2, 4)
    assert not v.choices(2)[14]
    v.h.p['location'] = 3; v.room(54, 3)
    assert v.choices(54)[15]
    v.room(54, 4)
    assert not v.choices(54)[15]
    return {'room_and_required_speaker_denials': 8, 'authored_available_reads': 5}


CASES = {'restore_order': restore_order, 'apron_route': apron_route,
         'speaker_availability': speaker_availability}
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=CASES)
    parser.add_argument('--build')
    parser.add_argument('--reference', action='store_true')
    args = parser.parse_args()
    print(json.dumps({'status': 'REFERENCE_EMITTED_NOT_NATIVE' if args.reference else 'PASS_EMITTED_NOT_NATIVE',
                      'case': args.case, 'native_acceptance': False,
                      'scope': 'Explicit ancestor/domain/arrival fixtures; no earned campaign state',
                      **CASES[args.case](args.build, args.reference)}))
