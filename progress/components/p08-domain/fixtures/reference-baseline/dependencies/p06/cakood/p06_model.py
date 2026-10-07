"""NEW independent P06 reference reconstruction, 2026-10-06.

Player words are literal catalog records. The campaign owns travel, actors,
Contest, readable presentation, persistence, and physical owner publication.
Saved 32-bit receipts are history, not whole-VM callback freshness. See DESIGN.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from enum import IntEnum
from functools import wraps
import hashlib
import json
from pathlib import Path
import threading
from types import MappingProxyType

PORCH = 'L03_PORCH'
KITCHEN = 'L02_KITCHEN'
SIDE = 'L04_SIDE_PASSAGE'
COURTYARD = 'L05_COURTYARD'
LIVING = 'L01_LIVING_ROOM'
ROOMS = frozenset((PORCH, KITCHEN, SIDE, COURTYARD, LIVING, 'L06_GARAGE', 'L07_CONSERVATORY'))
MAX_SERIAL = 0xFFFFFFFF
SAVE_KIND = 'cakood-p06-reconstruction'
SAVE_SCHEMA = 2
FLAG_IDS = frozenset(('SCREEN_BUILT', 'VIVIAN_SCOPE_AGREED', 'SCREEN_READY'))

class Tone(IntEnum):
    UNSPECIFIED = 0
    PROFESSIONAL = 1
    FRIENDLY = 2
    CAUTIOUSLY_ROMANTIC = 3

class MixerAnswer(IntEnum):
    UNANSWERED = 0
    ANOTHER_OCCASION = 1
    AFTER_HOUSEHOLD = 2

class Assembly(IntEnum):
    BARE = 0
    LOWER_LEGS = 1
    UPPER_RAIL = 2
    CLIPPED = 3

class Miniature(IntEnum):
    CLEAR = 0
    DISPLAY = 1
    HATCH = 2
    BOTH = 3

class Verb(IntEnum):
    GIVE = 1
    OPEN = 2
    CLOSE = 3
    PICK_UP = 4
    LOOK = 5
    TALK_TO = 6
    USE = 7
    PUSH = 8
    PULL = 9

class StateError(ValueError): pass
class SerialExhausted(StateError): pass
class BusyError(RuntimeError): pass
class RetiredOwnerError(RuntimeError): pass

OBJECTS = ('folding_screen_frame', 'upper_rail_clip_marks', 'clean_spare_sheet', 'large_laundry_clips',
           'sample_layout', 'arriving_visitor_figure', 'display_figure', 'miniature_screen_token', 'completed_screen')
LABEL_IDS = MappingProxyType({obj: f'P06.LABEL.{i:03}' for i, obj in enumerate(OBJECTS, 1)})
LOOK_IDS = MappingProxyType(dict(zip(OBJECTS, ('P06.LOOK.001', 'P06.LOOK.002', 'P06.INVENTORY.001',
    'P06.INVENTORY.002', 'P06.LOOK.003', 'P06.LOOK.004', 'P06.LOOK.005', 'P06.LOOK.006', 'P06.INVENTORY.003'))))
SOURCE_BINDINGS = MappingProxyType({'assembly_drawing': 'P06.READ.001', 'clip_marks': 'P06.LOOK.002',
    'sample_layout': 'P06.LOOK.003', 'sheet_permission': 'P06.DIALOGUE.004', 'courtyard_plan': 'P06.READ.002'})
ACTION_BINDINGS = MappingProxyType({
    'scope': ('P06.SCENE.001',),
    **{f'tone_{i}': (f'P06.CHOICE.{i:03}', f'P06.DIALOGUE.{i:03}') for i in range(1, 4)},
    'pickup_sheet': ('P06.SUCCESS.001',), 'pickup_clips': ('P06.SUCCESS.002',),
    'drape': ('P06.SUCCESS.003',), 'clip': ('P06.SUCCESS.004',), 'lower': ('P06.FAILURE.001',),
    'move': ('P06.SYSTEM.001',), 'bad_hatch': ('P06.FAILURE.002',), 'demo': ('P06.SUCCESS.005',),
    'flirt': ('P06.FAILURE.003',), 'mixer': ('P06.DIALOGUE.005',),
    'mixer_1': ('P06.CHOICE.004', 'P06.DIALOGUE.006'), 'mixer_2': ('P06.CHOICE.005', 'P06.DIALOGUE.007'),
    'loan': ('P06.SUCCESS.006', 'P06.SYSTEM.002'),
    'contest': ('VC02.ENTRY',), 'rematch': ('VC02.REMATCH',),
    'contest_not_ready': ('VC02.NOT_READY',), 'need_resolution': ('VC02.NEED_RESOLUTION',),
    **{f'hint_{i}': (f'P06.HINT.{i}',) for i in range(1, 4)},
})
FIXED = frozenset(OBJECTS) | frozenset(('assembly_drawing', 'courtyard_plan', 'vivian', 'frankie'))
PARTS = frozenset(('folding_screen_frame', 'upper_rail_clip_marks', 'clean_spare_sheet', 'large_laundry_clips', 'completed_screen', 'assembly_drawing'))
_BINDING_BYTES = Path(__file__).with_name('canonical-bindings.json').read_bytes()
CATALOG_HASH = hashlib.sha256(_BINDING_BYTES).hexdigest()
_BINDINGS = json.loads(_BINDING_BYTES)
_RECORDS = {r['id']: r for r in _BINDINGS['records']}
_UNITS = {r: tuple(u['line_id'] for u in _BINDINGS['speech_units'] if u['record_id'] == r) for r in _RECORDS}


def canonical_record(record_id):
    return deepcopy(_RECORDS[record_id])


def canonical_units(record_id):
    return tuple(_UNITS[record_id])


def _require(condition, message, error=StateError):
    if not condition: raise error(message)


def _integer(value, low=0, high=MAX_SERIAL):
    _require(type(value) is int and low <= value <= high, 'Expected bounded integer, never boolean')


def _enum(value, cls):
    _require(type(value) in (int, cls) and value in tuple(cls), 'Invalid enumerated choice')
    return int(value)


def split_serial(value):
    _integer(value)
    return value >> 16, value & 0xFFFF


def join_serial(high, low):
    _integer(high, 0, 0xFFFF); _integer(low, 0, 0xFFFF)
    return high * 65536 + low


class _Leases:
    """Unsaved Python-process allocator only. Native VM needs external retirement."""
    lock = threading.Lock()
    next = 1

    @classmethod
    def acquire(cls):
        with cls.lock:
            _require(cls.next <= MAX_SERIAL, 'Runtime lease exhausted', SerialExhausted)
            value = cls.next
            cls.next += 1
            return value


@dataclass(frozen=True)
class OwnedObject:
    object_id: str
    owner: str
    room: str

    def __post_init__(self):
        _require(type(self.object_id) is str and self.object_id == 'completed_screen', 'Unknown P06 ownership identity')
        _require(type(self.owner) is str and self.owner in ('P06', 'P08'), 'Unknown screen owner')
        _require(type(self.room) is str and self.room in (PORCH, COURTYARD), 'Invalid screen room')
        _require(self.owner != 'P08' or self.room == COURTYARD, 'P08 screen stays in courtyard')


@dataclass(frozen=True)
class P06Context:
    room: str
    flags: frozenset[str] = frozenset()
    inventory: frozenset[str] = frozenset()
    vivian_room: str = PORCH
    frankie_room: str = LIVING
    on_apron: bool = False
    contest_active: bool = False
    result_pending: bool = False
    ownership: tuple[OwnedObject, ...] = ()

    def __post_init__(self):
        for value in (self.room, self.vivian_room, self.frankie_room):
            _require(type(value) is str and value in ROOMS, 'Unknown campaign room')
        for value in (self.on_apron, self.contest_active, self.result_pending):
            _require(type(value) is bool, 'Campaign modes must be booleans')
        for value in (self.flags, self.inventory):
            _require(type(value) is frozenset and all(type(x) is str and x for x in value), 'Campaign facts must be frozen string sets')
        _require(not self.inventory & FIXED, 'P06-owned props cannot also be external inventory')
        _require(type(self.ownership) is tuple and all(type(x) is OwnedObject for x in self.ownership)
                 and len(self.ownership) <= 1, 'Duplicate or invalid screen owner')
        for value in self.ownership: value.__post_init__()
        _require('VC02_WON' not in self.flags or 'VC02_RESOLVED' in self.flags, 'Win requires true resolution')
        _require('SCREEN_READY' not in self.flags or {'SCREEN_BUILT', 'VIVIAN_SCOPE_AGREED', 'VC02_RESOLVED'} <= self.flags,
                 'Screen readiness lacks prerequisites')


@dataclass(frozen=True)
class ReceiptToken:
    kind: str
    serial: int
    lease: int


@dataclass(frozen=True)
class ContestRequest:
    encounter_id: str
    serial: int  # opaque runtime ticket: lease * 2**32 + saved logical receipt
    receipt_serial: int


@dataclass(frozen=True)
class Event:
    id: str
    serial: int
    kind: str
    payload: tuple[tuple[str, str | int | bool], ...] = ()


@dataclass(frozen=True)
class P06Result:
    text: str = ''
    code: str = ''
    line_ids: tuple[str, ...] = ()
    speech_unit_ids: tuple[str, ...] = ()
    events: tuple[Event, ...] = ()
    token: ReceiptToken | None = None


@dataclass
class _State:
    revision: int = 0
    scope: int = 0
    tone: int = 0
    tone_serial: int = 0
    permission: int = 0
    sheet_pickup: int = 0
    clips_pickup: int = 0
    assembly: int = 0
    assembly_serial: int = 0
    drape_serial: int = 0
    build_serial: int = 0
    first_build: int = 0
    first_build_drape: int = 0
    unclip_serial: int = 0
    unclip_build: int = 0
    unclip_drape: int = 0
    miniature: int = 0
    layout_serial: int = 0
    demonstration: int = 0
    demo_build: int = 0
    demo_drape: int = 0
    mixer: int = 0
    mixer_answer: int = 0
    answer_serial: int = 0
    loan_request: int = 0
    loan_build: int = 0
    loan_layout: int = 0
    complete: int = 0
    completed_request: int = 0
    completion_build: int = 0
    completion_layout: int = 0
    contest_request: int = 0
    sources: dict = field(default_factory=dict)
    pending_source: dict = field(default_factory=dict)
    hint: int = 0
    hint_serial: int = 0


def _command(method):
    @wraps(method)
    def call(self, *args, **kwargs):
        if not self._lock.acquire(blocking=False): raise BusyError('Concurrent P06 command')
        try:
            self._ensure_live()
            _require(not self._busy, 'P06 transaction in progress', BusyError)
            if self._uncertain and method.__name__ != 'restore':
                raise BusyError('Unknown host commit outcome; restore authoritative composed snapshot')
            return method(self, *args, **kwargs)
        finally:
            self._lock.release()
    return call


class P06World:
    def __init__(self):
        self._state = _State()
        self._lock = threading.RLock()
        self._busy = False
        self._retired = False
        self._uncertain = False
        self._lease = _Leases.acquire()

    def _ensure_live(self):
        if self._retired: raise RetiredOwnerError('Old P06 host owner retired')

    @_command
    def retire(self):
        """Host calls before discarding/replacing this callback owner."""
        self._retired = True

    @property
    def revision(self): return self._state.revision

    @property
    def flags(self):
        s = self._state
        return frozenset(
            ([ 'VIVIAN_SCOPE_AGREED' ] if s.scope else []) +
            ([ 'SCREEN_BUILT' ] if s.assembly == Assembly.CLIPPED else []) +
            ([ 'SCREEN_READY' ] if s.complete else []))

    @property
    def inventory(self):
        s = self._state
        return frozenset((['clean_spare_sheet'] if s.sheet_pickup and s.assembly == Assembly.BARE else []) +
                         (['large_laundry_clips'] if s.clips_pickup and s.assembly != Assembly.CLIPPED else []))

    @property
    def pending_request(self):
        s = self._state.contest_request
        return ContestRequest('VC02', self._lease * (1 << 32) + s, s) if s else None

    @property
    def pending_source(self):
        return deepcopy(self._state.pending_source)

    @property
    def observed_sources(self): return frozenset(self._state.sources)

    @property
    def miniature_conditions(self):
        p = self._state.miniature
        return MappingProxyType({'display_hidden': p in (Miniature.DISPLAY, Miniature.BOTH),
                                 'hatch_visible': p in (Miniature.CLEAR, Miniature.DISPLAY)})

    @property
    def assembly(self): return Assembly(self._state.assembly)

    @property
    def tone(self): return Tone(self._state.tone)

    @property
    def mixer_answer(self): return MixerAnswer(self._state.mixer_answer)

    @property
    def screen_handoff(self):
        s = self._state
        return ({'object_id': 'completed_screen', 'owner': 'P06', 'room': COURTYARD,
                 'position': 'UNPLACED', 'clips_attached': True, 'serial': s.complete} if s.complete else None)

    def _token(self, kind, serial): return ReceiptToken(kind, serial, self._lease)

    def _matches(self, token, kind, serial):
        return (type(token) is ReceiptToken and type(token.serial) is int and type(token.lease) is int
                and type(token.kind) is str and serial > 0 and token == self._token(kind, serial))

    def _result(self, code, route=None, *, records=(), event=None, token=None):
        records = ACTION_BINDINGS[route] if route else tuple(records)
        for record in records: canonical_record(record)
        return P06Result(code=code, line_ids=records, speech_unit_ids=tuple(u for r in records for u in _UNITS[r]),
                         events=(event,) if event else (), token=token)

    def _apply(self, update, code, route=None, *, records=(), token_kind=None, keep_reader=False, reserve=0):
        s = deepcopy(self._state)
        _require(s.revision + 1 + reserve <= MAX_SERIAL, 'P06 receipt space exhausted', SerialExhausted)
        s.revision += 1
        if not keep_reader: s.pending_source = {}
        update(s)
        self._validate(s)
        result = self._result(code, route, records=records,
            event=Event('P06:' + code, s.revision, 'committed'),
            token=self._token(token_kind, s.revision) if token_kind else None)
        self._state = s
        return result

    def validate(self, context=None):
        self._ensure_live()
        self._validate(self._state)
        if context is not None:
            _require(type(context) is P06Context, 'Expected immutable P06 context')
            context.__post_init__()
            s = self._state
            progress = any((s.scope, s.permission, s.sheet_pickup, s.clips_pickup, s.assembly_serial,
                            s.layout_serial, s.mixer, s.contest_request, s.complete, s.sources, s.pending_source, s.hint_serial))
            _require(not progress or 'PLAN_AGREED' in context.flags, 'P06 progress requires agreed P02 plan')
            _require(not ((context.flags & FLAG_IDS) - self.flags), 'Campaign claims unearned P06 state')
            _require(not (s.complete or s.loan_request) or 'VC02_RESOLVED' in context.flags, 'Loan requires actual external resolution')
            for owner in context.ownership:
                if s.complete:
                    _require(owner.room == COURTYARD, 'Completed screen cannot return to porch via old projection')
                else:
                    _require(owner.owner == 'P06' and owner.room == PORCH, 'Foreign/staged screen claimed before loan')
        return True

    @staticmethod
    def _validate(s):
        _require(type(s) is _State, 'Unknown state')
        _integer(s.revision)
        enum_fields = {'tone': Tone, 'mixer_answer': MixerAnswer, 'assembly': Assembly, 'miniature': Miniature}
        for name, cls in enum_fields.items():
            _require(type(getattr(s, name)) is int, 'Saved enums must be plain integers')
            _enum(getattr(s, name), cls)
        for name in _State.__dataclass_fields__:
            if name not in {'revision', 'sources', 'pending_source', 'hint', *enum_fields}:
                _integer(getattr(s, name), 0, s.revision)
        _integer(s.hint, 0, 3)
        _require(bool(s.hint) == bool(s.hint_serial), 'Hint receipt mismatch')
        _require(bool(s.tone) == bool(s.tone_serial), 'Tone receipt mismatch')
        _require(not s.tone or 0 < s.scope < s.tone_serial, 'Tone is optional characterization after scope')
        _require(not s.sheet_pickup or 0 < s.permission < s.sheet_pickup, 'Sheet pickup precedes actual permission')
        _require(s.assembly == Assembly.BARE or s.sheet_pickup > 0, 'Cloth arrangement lacks sheet')
        _require(not s.assembly_serial or 0 < s.sheet_pickup < s.assembly_serial, 'Assembly precedes pickup')
        _require(s.assembly == Assembly.BARE or s.assembly_serial > 0, 'Arrangement lacks receipt')
        _require(bool(s.drape_serial) == (s.assembly in (Assembly.UPPER_RAIL, Assembly.CLIPPED)), 'Drape receipt contradicts cloth position')
        if s.drape_serial:
            _require(s.sheet_pickup < s.drape_serial <= s.assembly_serial, 'Drape chronology invalid')
        _require(bool(s.build_serial) == (s.assembly == Assembly.CLIPPED), 'Build receipt contradicts attached clips')
        if s.build_serial:
            _require(s.build_serial == s.assembly_serial and 0 < s.clips_pickup < s.build_serial
                     and s.drape_serial < s.build_serial, 'Clip operation lacks picked clips/prior drape')
        if s.assembly == Assembly.UPPER_RAIL:
            _require(s.drape_serial <= s.assembly_serial, 'Upper-rail receipt invalid')
        _require(bool(s.first_build) == bool(s.first_build_drape), 'First assembly history incomplete')
        if s.first_build:
            _require(0 < s.sheet_pickup < s.first_build_drape < s.first_build <= s.assembly_serial
                     and 0 < s.clips_pickup < s.first_build, 'First build lacks ordered parts and drape')
            _require(not s.build_serial or s.first_build <= s.build_serial, 'Current build predates first build')
        _require(not s.build_serial or bool(s.first_build), 'Built screen lacks first build history')
        _require(not s.miniature or s.layout_serial > 0, 'Miniature position lacks placement')
        _require(not s.layout_serial or s.first_build > 0 and s.first_build < s.layout_serial, 'Miniature demonstration before assembly')
        _require(bool(s.demonstration) == bool(s.demo_build) == bool(s.demo_drape), 'Demonstration history incomplete')
        if s.demonstration:
            _require(s.first_build <= s.demo_build < s.demonstration <= s.layout_serial, 'Demonstration chronology invalid')
            _require(s.demo_build <= s.assembly_serial and 0 < s.sheet_pickup < s.demo_drape < s.demo_build, 'Demonstration build/drape chronology invalid')
            if s.demo_build == s.assembly_serial:
                _require(s.assembly == Assembly.CLIPPED, 'Unchanged demonstrated build contradicts assembly')
            if s.demonstration == s.layout_serial:
                _require(s.miniature == Miniature.DISPLAY, 'Unchanged approved mock-up contradicts sightlines')
        if s.miniature == Miniature.DISPLAY:
            _require(s.demonstration > 0, 'Approved miniature lacks actual demonstration')
        _require(not s.mixer or s.scope and s.scope < s.mixer, 'Mixer conversation requires actual scope')
        _require(bool(s.mixer_answer) == bool(s.answer_serial), 'Mixer answer receipt mismatch')
        _require(not s.answer_serial or 0 < s.mixer < s.answer_serial, 'Answer predates invitation')
        _require(not (s.loan_request and s.contest_request), 'Concurrent exclusive handoffs')
        for request in (s.loan_request, s.contest_request):
            _require(not request or request == s.revision < MAX_SERIAL, 'Pending request must reserve ACK/cancel serial')
        if s.contest_request:
            _require(0 < s.scope < s.contest_request and 0 < s.demonstration < s.contest_request
                     and s.assembly == Assembly.CLIPPED, 'Contest request lacks truthful demonstrated terms')
            _require(s.complete or s.miniature == Miniature.DISPLAY, 'Initial contest needs current successful mock-up')
        if s.loan_request:
            _require(not s.complete and 0 < s.scope < s.loan_request and 0 < s.demonstration < s.loan_request
                     and s.assembly == Assembly.CLIPPED and s.miniature == Miniature.DISPLAY
                     and s.loan_build == s.build_serial and s.loan_layout == s.layout_serial
                     and s.loan_build < s.loan_request and s.loan_layout < s.loan_request,
                     'Invalid loan candidate')
        else:
            _require(not (s.loan_build or s.loan_layout), 'Orphan loan snapshot')
        if s.complete:
            _require(0 < s.scope < s.completed_request and s.complete == s.completed_request + 1 and 0 < s.demonstration < s.completed_request
                     and s.assembly == Assembly.CLIPPED and s.completion_build == s.build_serial
                     and s.completion_build < s.completed_request and 0 < s.completion_layout < s.completed_request
                     and s.demonstration <= s.completion_layout <= s.layout_serial, 'Completion lacks ordered exact physical and scope receipts')
            if s.completion_layout == s.layout_serial:
                _require(s.miniature == Miniature.DISPLAY, 'Unchanged loan mock-up contradicts approved snapshot')
        else:
            _require(not (s.completed_request or s.completion_build or s.completion_layout), 'Orphan completion snapshot')
        _require(type(s.sources) is dict and set(s.sources) <= set(SOURCE_BINDINGS), 'Unknown source ledger')
        source_primary = []
        for key, receipt in s.sources.items():
            _require(type(receipt) is dict and set(receipt) == {'opened', 'serial'}, 'Invalid source receipt structure')
            _integer(receipt['opened'], 1, s.revision); _integer(receipt['serial'], 1, s.revision)
            _require(receipt['opened'] + 1 == receipt['serial'], 'Source ACK must immediately follow its uncancelled opening')
            if key == 'sheet_permission':
                _require(receipt['serial'] == s.permission, 'Permission does not equal complete Frankie source receipt')
            if key == 'courtyard_plan':
                _require(0 < s.demonstration < receipt['opened'], 'Plan source predates successful demonstration')
            source_primary += [receipt['opened'], receipt['serial']]
        _require(bool(s.permission) == ('sheet_permission' in s.sources), 'Missing complete Frankie source confirmation')
        p = s.pending_source
        _require(type(p) is dict, 'Pending source must be map')
        if p:
            _require(set(p) == {'source', 'record_id', 'room', 'serial'}, 'Invalid pending source structure')
            _require(type(p['source']) is str and p['source'] in SOURCE_BINDINGS and p['source'] not in s.sources
                     and type(p['record_id']) is str and p['record_id'] == SOURCE_BINDINGS[p['source']]
                     and type(p['room']) is str and p['room'] in ROOMS, 'Invalid pending source binding')
            _integer(p['serial'], 1, s.revision)
            _require(p['serial'] == s.revision < MAX_SERIAL and not (s.loan_request or s.contest_request), 'Pending reader serial/busy violation')
            expected_room = COURTYARD if s.complete and p['source'] in ('assembly_drawing', 'clip_marks') else PORCH
            _require(p['source'] == 'sheet_permission' or p['room'] == expected_room, 'Physical source opened remotely')
            _require(p['source'] != 'courtyard_plan' or 0 < s.demonstration < p['serial'], 'Plan opened before approval')
        # Primary independent operations cannot alias. Physical references can alias
        # only if their semantic signatures agree (same drape/build/layout commit).
        primary = [s.scope, s.tone_serial, s.sheet_pickup, s.clips_pickup, s.mixer, s.answer_serial,
                   s.loan_request, s.complete, s.completed_request, s.contest_request, s.hint_serial,
                   p.get('serial', 0), *source_primary]
        nonzero = [x for x in primary if x]
        _require(len(nonzero) == len(set(nonzero)), 'Independent receipts alias')
        signatures = {}
        def bind(serial, kind):
            if not serial: return
            _require(serial not in nonzero, 'Physical receipt aliases unrelated operation')
            old = signatures.setdefault(serial, kind)
            _require(old == kind, 'One physical receipt has contradictory roles')
        bind(s.drape_serial, 'drape'); bind(s.first_build_drape, 'drape'); bind(s.demo_drape, 'drape'); bind(s.unclip_drape, 'drape')
        bind(s.unclip_serial, 'unclip')
        for r in (s.build_serial, s.first_build, s.demo_build, s.loan_build, s.completion_build, s.unclip_build): bind(r, 'build')
        for r in (s.layout_serial, s.demonstration, s.loan_layout, s.completion_layout): bind(r, 'layout')
        if s.assembly_serial:
            kind = 'build' if s.assembly == Assembly.CLIPPED else ('drape' if s.assembly_serial == s.drape_serial else 'unclip' if s.assembly_serial == s.unclip_serial else 'assembly_edit')
            bind(s.assembly_serial, kind)
        build_signatures = {}
        for built, draped in ((s.first_build, s.first_build_drape), (s.build_serial, s.drape_serial), (s.demo_build, s.demo_drape), (s.unclip_build, s.unclip_drape)):
            if built:
                old = build_signatures.setdefault(built, draped)
                _require(old == draped, 'One build receipt cites contradictory draping')
        _require(bool(s.unclip_serial) == bool(s.unclip_build) == bool(s.unclip_drape), 'Incomplete unclipping history')
        if s.unclip_serial:
            _require(0 < s.sheet_pickup < s.unclip_drape < s.unclip_build < s.unclip_serial <= s.assembly_serial
                     and s.first_build <= s.unclip_build, 'Unclip must follow an actual correctly draped build')
            if s.assembly == Assembly.CLIPPED:
                _require(s.unclip_serial < s.build_serial, 'Rebuild must follow unclip')
                _require(s.drape_serial > s.unclip_serial or s.drape_serial == s.unclip_drape,
                         'Rebuild uses neither retained nor newly draped cloth')
            else:
                _require(max(s.first_build, s.demo_build) <= s.unclip_build, 'Latest known build was not unclipped')
                if s.assembly == Assembly.UPPER_RAIL and s.assembly_serial == s.unclip_serial:
                    _require(s.drape_serial == s.unclip_drape, 'Unclipping must retain its actual drape')
                else:
                    _require(s.unclip_serial < s.assembly_serial, 'Cloth edit requires a separate earlier unclip')
                    if s.assembly == Assembly.UPPER_RAIL:
                        _require(s.drape_serial == s.assembly_serial, 'Redrape must be its own latest edit')
        if s.first_build and s.assembly != Assembly.CLIPPED:
            _require(s.unclip_serial > 0, 'Any undo of a built screen requires its explicit unclip receipt')
        if s.assembly == Assembly.UPPER_RAIL and s.assembly_serial != s.drape_serial:
            _require(s.assembly_serial == s.unclip_serial, 'Upper rail differs from direct drape only after unclipping')
        if s.assembly == Assembly.BARE and s.assembly_serial:
            _require(s.sheet_pickup + 2 <= s.assembly_serial, 'Removing a bare sheet requires an earlier arrangement')
        # Distinct known builds require distinct intervening unclips. The latest
        # explicit receipt cannot stand in for an earlier undo that was replaced
        # by a later one. Reserve a real unused causal slot, not numeric distance.
        occupied = set(nonzero) | set(signatures)
        hidden = set()
        def reserve_slot(after, before):
            slot = after + 1
            for taken in sorted(occupied | hidden):
                if taken < slot: continue
                if taken > slot: break
                slot += 1
            _require(slot < before, 'No available revision for a required earlier physical undo')
            hidden.add(slot)
        builds = sorted(build_signatures)
        known_drapes = {serial for serial, kind in signatures.items() if kind == 'drape'}
        for built, draped in build_signatures.items():
            _require(not any(draped < other < built for other in known_drapes),
                     'A known intervening drape contradicts the build snapshot')
        for earlier, later in zip(builds, builds[1:]):
            draped = build_signatures[later]
            limit = draped if draped > earlier else later
            if draped <= earlier:
                _require(draped == build_signatures[earlier], 'Rebuild reused an obsolete drape')
            if not (earlier < s.unclip_serial < limit and s.unclip_build == earlier):
                reserve_slot(earlier, limit)
        if s.assembly == Assembly.BARE and s.assembly_serial and not s.first_build:
            reserve_slot(s.sheet_pickup, s.assembly_serial)
        # Bounds on the number of known distinct operations catch receipt compaction.
        _require(len(set(nonzero) | set(signatures)) <= s.revision, 'More known operations than elapsed revisions')

    @_command
    def save(self):
        self.validate()
        return {'kind': SAVE_KIND, 'schema': SAVE_SCHEMA, 'catalog': CATALOG_HASH, 'state': deepcopy(asdict(self._state))}

    @classmethod
    def load(cls, data, context=None):
        _require(type(data) is dict and set(data) == {'kind', 'schema', 'catalog', 'state'}, 'Invalid save envelope')
        _require(type(data['kind']) is str and data['kind'] == SAVE_KIND and type(data['schema']) is int
                 and data['schema'] == SAVE_SCHEMA and type(data['catalog']) is str and data['catalog'] == CATALOG_HASH,
                 'Incompatible P06 schema/catalog')
        raw = data['state']
        _require(type(raw) is dict and set(raw) == set(_State.__dataclass_fields__), 'Unknown/missing P06 fields')
        state = _State(**deepcopy(raw)); cls._validate(state)
        result = cls(); result._state = state; result.validate(context)
        return result

    @_command
    def restore(self, data, context=None):
        candidate = type(self).load(data, context)
        self._state, self._lease = candidate._state, candidate._lease
        self._uncertain = False
        return self._result('restored')

    def to_json(self):
        return json.dumps(self.save(), sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)

    @classmethod
    def from_json(cls, text, context=None):
        _require(type(text) is str and len(text.encode('utf-8')) <= 65536, 'Expected bounded JSON text')
        def unique(pairs):
            out = {}
            for k, v in pairs:
                _require(k not in out, 'Duplicate JSON key'); out[k] = v
            return out
        def constant(_): raise StateError('Nonfinite number')
        try: data = json.loads(text, object_pairs_hook=unique, parse_constant=constant)
        except (RecursionError, UnicodeError, json.JSONDecodeError) as exc: raise StateError('Malformed JSON') from exc
        return cls.load(data, context)

    def _gate(self, context, *, room=None, actor=None, exclusive=True):
        self.validate(context)
        if exclusive and (self._state.loan_request or self._state.contest_request): return 'handoff_pending'
        if context.result_pending: return 'contest_result_pending'
        if context.contest_active: return 'contest_active'
        if context.on_apron: return 'return_to_set'
        if 'PLAN_AGREED' not in context.flags: return 'plan_required'
        if room is not None and context.room != room: return 'wrong_room'
        if actor is not None and context.room != getattr(context, actor + '_room'): return actor + '_absent'
        return None

    def object_location(self, context, obj):
        self.validate(context)
        _require(type(obj) is str, 'Object ID must be string')
        if obj in ('vivian', 'frankie'): return getattr(context, obj + '_room')
        if obj == 'clip_marks': obj = 'upper_rail_clip_marks'
        s = self._state
        if obj in PARTS and s.complete:
            owner = next(iter(context.ownership), None)
            return COURTYARD if owner and owner.owner == 'P06' else None
        if obj == 'completed_screen': return PORCH if s.assembly == Assembly.CLIPPED else None
        if obj == 'clean_spare_sheet':
            return 'inventory' if obj in self.inventory else PORCH if s.sheet_pickup else KITCHEN
        if obj == 'large_laundry_clips':
            return 'inventory' if obj in self.inventory else PORCH if s.clips_pickup else SIDE
        if obj == 'courtyard_plan': return PORCH if s.demonstration else None
        if obj in FIXED: return PORCH
        return None

    def world_projection(self, context):
        """Read-only root identities only: attached parts are not extra world objects."""
        self.validate(context)
        s = self._state
        roots = set(OBJECTS) - PARTS
        if s.assembly == Assembly.CLIPPED: roots.add('completed_screen')
        else:
            roots.add('folding_screen_frame')
            if s.assembly == Assembly.BARE: roots.add('clean_spare_sheet')
            roots.add('large_laundry_clips')
        if s.demonstration: roots.add('courtyard_plan')
        return MappingProxyType({o: self.object_location(context, o) for o in sorted(roots)
                                 if self.object_location(context, o) not in (None, 'inventory')})

    def source_location(self, context, source):
        """Physical access, including a source carried by the current P08 owner.

        This does not project another branch's object or grant notebook knowledge.
        """
        self.validate(context)
        _require(type(source) is str and source in SOURCE_BINDINGS, 'Unknown source')
        if source == 'sheet_permission': return context.frankie_room
        if source in ('assembly_drawing', 'clip_marks') and self._state.complete:
            owner = next(iter(context.ownership), None)
            return owner.room if owner else None
        if source == 'courtyard_plan' and not self._state.demonstration: return None
        return PORCH

    def look(self, context, obj):
        self.validate(context)
        _require(type(obj) is str, 'Object ID must be string')
        if context.on_apron: return self._result('return_to_set')
        if obj == 'assembly_drawing': rid = SOURCE_BINDINGS[obj]
        elif obj == 'courtyard_plan': rid = SOURCE_BINDINGS[obj]
        elif obj == 'clip_marks': rid = SOURCE_BINDINGS[obj]
        elif obj in LOOK_IDS: rid = LOOK_IDS[obj]
        else: return self._result('unsupported_object')
        source = {'assembly_drawing': 'assembly_drawing', 'upper_rail_clip_marks': 'clip_marks',
                  'clip_marks': 'clip_marks', 'sample_layout': 'sample_layout', 'courtyard_plan': 'courtyard_plan'}.get(obj)
        location = self.source_location(context, source) if source else self.object_location(context, obj)
        if location not in (context.room, 'inventory'): return self._result('unreachable')
        return self._result('look', records=(rid,))

    def label(self, obj):
        _require(type(obj) is str and obj in LABEL_IDS, 'Unknown label')
        return self._result('label', records=(LABEL_IDS[obj],))

    def journal_records(self):
        return tuple(SOURCE_BINDINGS[s] for s in sorted(self._state.sources))

    def _source_gate(self, context, source):
        _require(type(source) is str and source in SOURCE_BINDINGS, 'Unknown source')
        denied = self._gate(context, actor='frankie' if source == 'sheet_permission' else None)
        if denied: return denied
        if source == 'courtyard_plan' and not self._state.demonstration: return 'plan_not_marked'
        if self.source_location(context, source) != context.room: return 'wrong_room'
        return None

    @_command
    def read_source(self, context, source):
        denied = self._source_gate(context, source)
        if denied: return self._result(denied)
        record = SOURCE_BINDINGS[source]
        if source in self._state.sources: return self._result('source_observed', records=(record,))
        p = self._state.pending_source
        if p and p['source'] == source and p['room'] == context.room:
            return self._result('source_pending', records=(record,), token=self._token('source', p['serial']))
        def change(s): s.pending_source = {'source': source, 'record_id': record, 'room': context.room, 'serial': s.revision}
        return self._apply(change, 'source_pending', records=(record,), token_kind='source', reserve=1)

    @_command
    def acknowledge_source(self, context, source, record_id, token, *, presented_units, complete):
        _require(type(complete) is bool, 'Complete-page attestation must be boolean')
        _require(type(presented_units) is tuple and all(type(x) is str for x in presented_units), 'Exact speech units required')
        denied = self._source_gate(context, source)
        if denied: return self._result(denied)
        p = self._state.pending_source
        if not (p and p['source'] == source and p['room'] == context.room and type(record_id) is str
                and record_id == p['record_id'] and self._matches(token, 'source', p['serial'])):
            return self._result('stale_source')
        if not complete or presented_units != _UNITS[record_id]: return self._result('source_incomplete')
        opened = p['serial']
        def change(s):
            s.sources[source] = {'opened': opened, 'serial': s.revision}
            if source == 'sheet_permission': s.permission = s.revision
        return self._apply(change, 'source_observed')

    @_command
    def cancel_source(self, token):
        p = self._state.pending_source
        if not p or not self._matches(token, 'source', p['serial']): return self._result('stale_source')
        return self._apply(lambda s: None, 'source_cancelled')

    @_command
    def agree_scope(self, context):
        denied = self._gate(context, room=PORCH, actor='vivian')
        if denied: return self._result(denied)
        if self._state.scope: return self._result('already_agreed')
        return self._apply(lambda s: setattr(s, 'scope', s.revision), 'scope_agreed', 'scope')

    def introduce(self, context): return self.agree_scope(context)

    @_command
    def choose_tone(self, context, tone):
        tone = _enum(tone, Tone); _require(tone != 0, 'Choose an authored tone')
        denied = self._gate(context, actor='vivian')
        if denied: return self._result(denied)
        if not self._state.scope: return self._result('scope_required')
        if self._state.tone == tone: return self._result('unchanged_tone')
        def change(s): s.tone, s.tone_serial = tone, s.revision
        return self._apply(change, 'tone_chosen', f'tone_{tone}')

    @_command
    def flirt_only(self, context):
        denied = self._gate(context, actor='vivian')
        return self._result(denied) if denied else self._result('concrete_terms_required', 'flirt')

    def ask_sheet_permission(self, context): return self.read_source(context, 'sheet_permission')

    @_command
    def pick_up(self, context, obj):
        _require(type(obj) is str, 'Object ID must be string')
        if obj not in ('clean_spare_sheet', 'large_laundry_clips'): return self._result('not_pocketable')
        sheet = obj == 'clean_spare_sheet'
        denied = self._gate(context, room=KITCHEN if sheet else SIDE)
        if denied: return self._result(denied)
        if self._state.sheet_pickup if sheet else self._state.clips_pickup: return self._result('already_collected')
        if sheet and not self._state.permission: return self._result('frankie_confirmation_required')
        return self._apply(lambda s: setattr(s, 'sheet_pickup' if sheet else 'clips_pickup', s.revision),
                           'sheet_collected' if sheet else 'clips_collected', 'pickup_sheet' if sheet else 'pickup_clips')

    @_command
    def arrange_sheet(self, context, arrangement):
        arrangement = _enum(arrangement, Assembly)
        _require(arrangement in (Assembly.BARE, Assembly.LOWER_LEGS, Assembly.UPPER_RAIL), 'Use attach_clips for assembled screen')
        denied = self._gate(context, room=PORCH, actor='vivian' if arrangement == Assembly.LOWER_LEGS else None)
        if denied: return self._result(denied)
        s = self._state
        if s.complete: return self._result('screen_transferred')
        if not s.sheet_pickup: return self._result('sheet_required')
        if s.assembly == Assembly.CLIPPED: return self._result('detach_clips_first')
        if s.assembly == arrangement: return self._result('unchanged_arrangement')
        def change(s):
            s.assembly, s.assembly_serial = arrangement, s.revision
            s.drape_serial = s.revision if arrangement == Assembly.UPPER_RAIL else 0
        route = 'lower' if arrangement == Assembly.LOWER_LEGS else 'drape' if arrangement == Assembly.UPPER_RAIL else None
        return self._apply(change, 'sheet_arranged', route)

    @_command
    def attach_clips(self, context):
        denied = self._gate(context, room=PORCH, actor='vivian')
        if denied: return self._result(denied)
        s = self._state
        if s.complete: return self._result('screen_transferred')
        if s.assembly == Assembly.CLIPPED: return self._result('already_built')
        if not s.clips_pickup: return self._result('clips_required')
        if s.assembly != Assembly.UPPER_RAIL: return self._result('upper_rail_required')
        def change(s):
            s.assembly, s.assembly_serial, s.build_serial = Assembly.CLIPPED.value, s.revision, s.revision
            if not s.first_build: s.first_build, s.first_build_drape = s.revision, s.drape_serial
        return self._apply(change, 'screen_built', 'clip')

    @_command
    def detach_clips(self, context):
        denied = self._gate(context, room=PORCH)
        if denied: return self._result(denied)
        if self._state.complete: return self._result('screen_transferred')
        if self._state.assembly != Assembly.CLIPPED: return self._result('clips_not_attached')
        def change(s):
            s.unclip_serial, s.unclip_build, s.unclip_drape = s.revision, s.build_serial, s.drape_serial
            s.assembly, s.assembly_serial, s.build_serial = Assembly.UPPER_RAIL.value, s.revision, 0
        return self._apply(change, 'clips_detached')

    @_command
    def move_miniature(self, context, position):
        position = _enum(position, Miniature)
        denied = self._gate(context, room=PORCH, actor='vivian')
        if denied: return self._result(denied)
        if self._state.assembly != Assembly.CLIPPED: return self._result('screen_required')
        if self._state.miniature == position: return self._result('unchanged_miniature')
        def change(s):
            s.miniature, s.layout_serial = position, s.revision
            if position == Miniature.DISPLAY and not s.demonstration:
                s.demonstration, s.demo_build, s.demo_drape = s.revision, s.build_serial, s.drape_serial
        records = ACTION_BINDINGS['move'] + (ACTION_BINDINGS['demo'] if position == Miniature.DISPLAY else
                                            ACTION_BINDINGS['bad_hatch'] if position in (Miniature.HATCH, Miniature.BOTH) else ())
        return self._apply(change, 'miniature_moved', records=records)

    @_command
    def mention_mixer(self, context):
        denied = self._gate(context, actor='vivian')
        if denied: return self._result(denied)
        if not self._state.scope: return self._result('scope_required')
        if self._state.mixer: return self._result('mixer_already_mentioned')
        return self._apply(lambda s: setattr(s, 'mixer', s.revision), 'mixer_mentioned', 'mixer')

    @_command
    def answer_mixer(self, context, answer):
        answer = _enum(answer, MixerAnswer); _require(answer != 0, 'Choose an authored commitment-preserving answer')
        denied = self._gate(context, actor='vivian')
        if denied: return self._result(denied)
        if not self._state.mixer: return self._result('mixer_not_mentioned')
        if self._state.mixer_answer == answer: return self._result('unchanged_mixer_answer')
        def change(s): s.mixer_answer, s.answer_serial = answer, s.revision
        return self._apply(change, 'mixer_answered', f'mixer_{answer}')

    def _practical_ready(self):
        s = self._state
        return bool(s.scope and s.assembly == Assembly.CLIPPED and s.demonstration and
                    (s.complete or s.miniature == Miniature.DISPLAY))

    @_command
    def request_contest(self, context):
        denied = self._gate(context, actor='vivian', room=None if self._state.complete else PORCH, exclusive=False)
        if denied: return self._result(denied)
        if self._state.loan_request: return self._result('handoff_pending')
        if not self._practical_ready(): return self._result('contest_not_ready', 'contest_not_ready')
        route = 'rematch' if 'VC02_RESOLVED' in context.flags else 'contest'
        if self._state.contest_request:
            return self._result('contest_requested', route, token=self._token('contest', self._state.contest_request))
        return self._apply(lambda s: setattr(s, 'contest_request', s.revision), 'contest_requested', route,
                           token_kind='contest', reserve=1)

    @_command
    def acknowledge_contest_request(self, serial, *, cancelled=False):
        _require(type(cancelled) is bool, 'Cancellation must be explicit boolean')
        pending = self.pending_request
        if type(serial) is not int or pending is None or serial != pending.serial: return self._result('stale_contest_request')
        return self._apply(lambda s: setattr(s, 'contest_request', 0), 'contest_cancelled' if cancelled else 'contest_dispatched')

    @_command
    def borrow_screen(self, context):
        denied = self._gate(context, actor='vivian', room=None if self._state.complete else PORCH, exclusive=False)
        if denied: return self._result(denied)
        s = self._state
        if s.complete: return self._result('already_ready')
        if s.contest_request: return self._result('handoff_pending')
        if not self._practical_ready(): return self._result('practical_work_required')
        if 'VC02_RESOLVED' not in context.flags: return self._result('resolution_required', 'need_resolution')
        if s.loan_request: return self._result('loan_pending', token=self._token('loan', s.loan_request))
        def change(s): s.loan_request, s.loan_build, s.loan_layout = s.revision, s.build_serial, s.layout_serial
        # No success wording before exact physical/output publication by the host.
        return self._apply(change, 'loan_pending', token_kind='loan', reserve=1)

    @_command
    def acknowledge_handoff(self, context, token, objects):
        denied = self._gate(context, room=PORCH, actor='vivian', exclusive=False)
        if denied: return self._result(denied)
        if not self._matches(token, 'loan', self._state.loan_request): return self._result('stale_handoff')
        _require(type(objects) is tuple and objects == (OwnedObject('completed_screen', 'P06', COURTYARD),), 'Exact one-screen staging acknowledgment required')
        def change(s):
            s.complete, s.completed_request = s.revision, s.loan_request
            s.completion_build, s.completion_layout = s.loan_build, s.loan_layout
            s.loan_request = s.loan_build = s.loan_layout = 0
        return self._apply(change, 'screen_ready', 'loan')

    @_command
    def cancel_handoff(self, token):
        if not self._matches(token, 'loan', self._state.loan_request): return self._result('stale_handoff')
        def change(s): s.loan_request = s.loan_build = s.loan_layout = 0
        return self._apply(change, 'loan_cancelled')

    @_command
    def hint(self, context, level):
        _integer(level, 1, 3)
        denied = self._gate(context)
        if denied: return self._result(denied)
        if level <= self._state.hint: return self._result('hint', f'hint_{level}')
        def change(s): s.hint, s.hint_serial = level, s.revision
        return self._apply(change, 'hint', f'hint_{level}')

    def act(self, context, verb, obj, target=None):
        """Nine-verb routing; named choice methods supply authored concrete options."""
        verb = _enum(verb, Verb)
        _require(type(obj) is str and (target is None or type(target) is str), 'Named object IDs required')
        if verb == Verb.LOOK: return self.look(context, obj)
        if verb == Verb.PICK_UP: return self.pick_up(context, obj)
        if verb == Verb.TALK_TO and obj == 'vivian': return self.agree_scope(context)
        if verb == Verb.TALK_TO and obj == 'frankie': return self.ask_sheet_permission(context)
        if verb == Verb.USE and obj == 'clean_spare_sheet' and target == 'folding_screen_frame':
            return self.arrange_sheet(context, Assembly.UPPER_RAIL)
        if verb == Verb.USE and obj == 'large_laundry_clips' and target == 'upper_rail_clip_marks': return self.attach_clips(context)
        if verb == Verb.PULL and obj == 'large_laundry_clips': return self.detach_clips(context)
        if verb == Verb.PULL and obj == 'clean_spare_sheet': return self.arrange_sheet(context, Assembly.BARE)
        if verb in (Verb.PUSH, Verb.PULL) and obj == 'miniature_screen_token': return self._result('named_miniature_choice_required')
        return self._result('unsupported_action')
