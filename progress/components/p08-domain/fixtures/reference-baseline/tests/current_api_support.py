"""NEW integration harness over unchanged current APIs, never legacy API stubs.

This is Python protocol evidence. Logical source-page acknowledgments are trusted
test-host inputs, not evidence that a native reader or audio player rendered them.
P03 has no public JSON loader: its exact State fields plus after_restore are an
explicitly new test serialization adapter. Other branches use their actual saves.
"""
from copy import deepcopy
from dataclasses import asdict, replace
import json

from dependencies.p03 import p03_model as p3
from dependencies.p04 import p04_model as p4
from dependencies.p05.cakood import p05_model as p5, composition as host5
from dependencies.p06.cakood import p06_model as p6, composition as host6
from dependencies.p06.cakood.verbal_contest import VerbalContests, Phase
from dependencies.p07.cakood import p07_model as p7
from cakood.p08_model import P08Context, P08World, COURTYARD, KITCHEN, Position

PLAN = frozenset({'PLAN_AGREED'})
TOOLS = frozenset({'grease_pencil', 'master_invitation', 'wedge'})
DESTINATIONS = {'ceramic_carrier': Position.HATCH, 'pa_kit': Position.WALL,
                'completed_screen': Position.ALCOVE, 'serving_table': Position.HATCH,
                'credit_slate': Position.HATCH}


def expect(actual, expected):
    if actual != expected:
        raise AssertionError(f'{actual!r} != {expected!r}')


def drain(contests):
    while pending := contests.pending_text():
        contests.acknowledge_text(pending.receipt)


def resolve_loss(contests, encounter, world, context):
    expect(world.request_contest(context).code, 'contest_requested')
    # The branch itself has admitted the request through its actual practical gate.
    contests.introduce(encounter, admitted=True)
    world.acknowledge_contest_request(world.pending_request.serial)
    drain(contests)
    for lesson in contests.recap(encounter):
        contests.present_lesson(encounter, lesson.pair_id)
        drain(contests)
    contests.enter(encounter, 719, admitted=True)
    for _ in range(3):
        contests.begin_turn(contests.active.id)
        drain(contests)
        contests.yield_exchange(contests.active.exchange_id)
        drain(contests)
    expect(contests.active.phase, Phase.KO_PENDING)
    contests.commit_ko(contests.active.outcome_id)
    drain(contests)
    if encounter + '_RESOLVED' not in contests.flags or encounter + '_WON' in contests.flags:
        raise AssertionError('Genuine non-win result did not resolve the social gate')


class Preparation:
    """Five real branches completed through public actions; one shared Contest."""
    def __init__(self, cloth='clean_towel'):
        if cloth not in ('clean_towel', 'clean_napkin'):
            raise ValueError('Exact canonical padding required')
        self.cloth = cloth
        self.p3 = p3.P03()
        expect(self.p3.context(6, 0, 1, 1), 1)
        expect(self.p3.look(37), p3.Code.OBSERVED)  # exact class-card source receipt
        expect(self.p3.begin_credit(), p3.Code.CREDIT_OPEN)
        expect(self.p3.select(1), p3.Code.CREDIT_WRITTEN)
        expect(self.p3.context(2, 0, 1, 1), 1)
        expect(self.p3.collect(39 if cloth == 'clean_towel' else 38), p3.Code.CLOTH_COLLECTED)
        expect(self.p3.context(6, 0, 1, 1), 1)
        expect(self.p3.pad(39 if cloth == 'clean_towel' else 38), p3.Code.CARRIER_PADDED)
        expect(self.p3.give_slate(), p3.Code.CREDIT_APPROVED)
        expect(self.p3.state.ready, 1)

        self.p4 = p4.P04()
        expect(self.p4.context(3, 0, 1, 1), 1)
        expect(self.p4.open_gate(), p4.Code.GATE_OPEN)
        expect(self.p4.place_wedge(), p4.Code.GATE_WEDGED)
        expect(self.p4.context(3, 0, 1, 0), 1)  # held wedge is now reserved
        expect(self.p4.move_bunting(p4.Bunting.HELD), p4.Code.BUNTING_MOVED)
        expect(self.p4.move_bunting(p4.Bunting.HOOK), p4.Code.BUNTING_MOVED)
        expect(self.p4.recover_wedge(), p4.Code.WEDGE_RECOVERED)
        expect(self.p4.context(3, 0, 1, 1), 1)
        expect(self.p4.close_gate(1), p4.Code.GATE_CHECKED)
        expect(self.p4.open_gate(), p4.Code.GATE_OPEN)
        expect(self.p4.set_peg(1), p4.Code.PEG_ENGAGED)

        self.contests = VerbalContests()
        self.c5 = p5.P05Context(p5.GARAGE, flags=PLAN, inventory=TOOLS, bunny_room=p5.GARAGE)
        self.p5 = p5.P05World()
        self.p5.invite_listener(self.c5, p5.Listener.BUNNY)
        self.p5.connect_microphone(self.c5)
        self.p5.select_source(self.c5, p5.Source.MIC)
        self.p5.aim_speaker(self.c5, p5.Listener.BUNNY.value)
        expect(self.p5.test_microphone(self.c5, p5.Listener.BUNNY).code, 'soundcheck_passed')
        self.p5.begin_credit(self.c5)
        self.p5.select_credit(self.c5, p5.CREDIT_ID)
        self.p5.agree_role(self.c5)
        resolve_loss(self.contests, 'VC01', self.p5, self.c5)
        self.h5 = host5.MemoryTransactionHost()
        self.c5 = replace(self.c5, flags=PLAN | self.contests.flags)
        expect(host5.borrow_kit_synchronously(self.p5, self.c5, self.h5).code, 'sound_ready')

        self.c6 = p6.P06Context(p6.PORCH, flags=PLAN | self.contests.flags, inventory=TOOLS)
        self.p6 = p6.P06World()
        permission = replace(self.c6, room=p6.LIVING)
        request = self.p6.read_source(permission, 'sheet_permission')
        self.p6.acknowledge_source(permission, 'sheet_permission', p6.SOURCE_BINDINGS['sheet_permission'],
            request.token, presented_units=p6.canonical_units(p6.SOURCE_BINDINGS['sheet_permission']), complete=True)
        self.p6.pick_up(replace(self.c6, room=p6.KITCHEN), 'clean_spare_sheet')
        self.p6.pick_up(replace(self.c6, room=p6.SIDE), 'large_laundry_clips')
        self.p6.agree_scope(self.c6)
        self.p6.arrange_sheet(self.c6, p6.Assembly.UPPER_RAIL)
        self.p6.attach_clips(self.c6)
        self.p6.move_miniature(self.c6, p6.Miniature.DISPLAY)
        resolve_loss(self.contests, 'VC02', self.p6, self.c6)
        self.h6 = host6.MemoryTransactionHost()
        expect(host6.borrow_screen_synchronously(self.p6, self.c6, self.contests, self.h6).code, 'screen_ready')
        self.c6 = replace(self.c6, flags=PLAN | self.contests.flags)

        self.c7 = p7.P07Context(KITCHEN, flags=PLAN, inventory=TOOLS, bunny_room=KITCHEN)
        self.p7 = p7.P07World()
        request = self.p7.open_source(self.c7, p7.Source.RECIPE)
        for page in request.pages:
            self.p7.acknowledge_source_page(self.c7, request.token, page)
        for action in (p7.Action.ADD_BASE, p7.Action.MEASURE_STOCK, p7.Action.ADD_STOCK,
                       p7.Action.ADD_VEGETABLES, p7.Action.COOK, p7.Action.TURN_HEAT_OFF,
                       p7.Action.ADD_HERBS, p7.Action.CLOSE_LID):
            self.p7.perform(self.c7, action,
                **({'measure': p7.Measure.EIGHT_TASTING_BOWLS} if action == p7.Action.MEASURE_STOCK else {}))
        if 'FOOD_READY' not in self.p7.flags:
            raise AssertionError('Actual current cooking actions did not complete')
        self.owners = {
            'ceramic_carrier': {'owner': 'P03', 'room': 'kitchen_pass'},
            'ceramic_service': {'owner': 'P03', 'room': 'kitchen_pass'},
            'credit_slate': {'owner': 'P03', 'room': 'kitchen_pass'},
            cloth: {'owner': 'P03', 'room': 'embedded_padding'},
            'ceramic_sample_tiles': {'owner': 'inventory', 'room': 'inventory'},
            'hotpot_pot': {'owner': 'P07', 'room': KITCHEN},
        }

    def context(self):
        flags = PLAN | self.p4.flags | self.p5.flags | self.p6.flags | self.p7.flags | self.contests.flags
        if self.p3.state.ready:
            flags |= {'CERAMICS_READY'}
        return P08Context(COURTYARD, flags=frozenset(flags), inventory=TOOLS | {'ceramic_sample_tiles'},
            carrier_padding={1: 'clean_towel', 2: 'clean_napkin'}[self.p3.state.padding],
            frankie_room=COURTYARD, bunny_room=COURTYARD)

    def prior_saves(self):
        return {'p03': asdict(self.p3.state), 'p04': self.p4.save(), 'p05': self.p5.save(),
                'p06': self.p6.save(), 'p07': self.p7.save(), 'contests': self.contests.save().decode()}

    def owner_map(self):
        return deepcopy(self.owners | self.h5.owners | self.h6.owners)

    def reconcile(self, world):
        """New test-host P03 map and actual unchanged P05/P06 transfer consumers."""
        context = self.context()
        for claim in world.pending_handoffs:
            if claim['object_id'] == 'completed_screen':
                self.h6.bind_p08(world, context)
                self.h6.apply_p08_handoff(self.h6.pending_p08_screen_claim())
                continue
            if claim['object_id'] == 'pa_kit':
                self.h5.apply_p08_handoff(claim)
            else:
                for obj in (claim['object_id'], *claim['includes']):
                    expect(self.owners[obj]['owner'], claim['from_owner'])
                    self.owners[obj] = {'owner': claim['to_owner'], 'room': claim['room']}
            expect(world.acknowledge_handoff(claim['handoff_id'], claim['serial']).code, 'handoff_acknowledged')

    def fit(self):
        world = P08World()
        for obj, destination in DESTINATIONS.items():
            world.place(self.context(), obj, destination)
            self.reconcile(world)
        world.unpack_service(self.context())
        self.reconcile(world)
        return world

    def save_composed(self, world):
        return {'branches': self.prior_saves(), 'p08': world.save(), 'owners': self.owner_map(),
                'campaign': {'room': COURTYARD, 'apron': False, 'inventory': sorted(self.context().inventory)}}

    def restore_composed(self, data):
        """New test serializer; not a production host or historical save format."""
        data = json.loads(json.dumps(data))
        branches = data['branches']
        self.p3 = p3.P03()
        self.p3.state = p3.State(**branches['p03'])
        expect(self.p3.after_restore(), 1)
        self.p4 = p4.P04()
        self.p4.load(branches['p04'])
        self.contests = VerbalContests.load(branches['contests'].encode(), owner_generation=2)
        self.h5.owners = {key: data['owners'][key] for key in ('pa_kit', 'handcart')}
        self.h6.owners = {'completed_screen': data['owners']['completed_screen']}
        self.owners = {key: value for key, value in data['owners'].items()
                       if key not in ('pa_kit', 'handcart', 'completed_screen')}
        self.p5 = p5.P05World.load(branches['p05'], replace(self.c5, ownership=self.h5.ownership_context()))
        self.p6 = p6.P06World.load(branches['p06'], replace(self.c6, ownership=self.h6.ownership_context()))
        self.p7 = p7.P07World.load(branches['p07'], self.c7)
        world = P08World.load(data['p08'], self.context())
        self.h6.bind_p08(world, self.context())
        return world
