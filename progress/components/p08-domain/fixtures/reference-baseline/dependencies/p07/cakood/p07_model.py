"""NEW readable P07 reference reconstruction, revision 2; not a recovered native ABI.

Canonical source bytes are separate from executable logic. All player output is
identified by canonical IDs. The host owns actual readable display, campaign
movement, audio and eventual P13 delivery. See DESIGN.md for trust boundaries.
"""
from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path
from threading import RLock
from types import MappingProxyType
from uuid import uuid4

KITCHEN = 'L02_KITCHEN'
LIVING = 'L01_LIVING_ROOM'
COURTYARD = 'L05_COURTYARD'
ROOMS = frozenset((LIVING, KITCHEN, 'L03_PORCH', 'L04_SIDE_PASSAGE', COURTYARD,
                   'L06_GARAGE', 'L07_CONSERVATORY'))
MAX_SERIAL = 0xFFFFFFFF
SAVE_KIND = 'cakood-p07-reconstruction'
SAVE_SCHEMA = 1
SERIAL_ENCODING = 'uint32-json;native-u16-high-low'
_RAW = Path(__file__).with_name('canonical-bindings.json').read_bytes()
CANONICAL_SHA256 = sha256(_RAW).hexdigest()
_CANON = json.loads(_RAW)
_RECORDS = {r['id']: r for r in _CANON['records']}
_UNITS = {u['line_id']: u for u in _CANON['speech_units']}


class Source(Enum):
    RECIPE = 'recipe'
    JUG_MARK = 'jug_mark'
    HERB_LABEL = 'herb_label'


class Measure(Enum):
    SIX_SUPPERS = 'six_suppers'
    EIGHT_TASTING_BOWLS = 'eight_tasting_bowls'


class Action(Enum):
    INTRODUCE = 'introduce'
    ADD_BASE = 'add_base'
    MEASURE_STOCK = 'measure_stock'
    ADD_STOCK = 'add_stock'
    ADD_VEGETABLES = 'add_vegetables'
    COOK = 'cook'
    TURN_HEAT_OFF = 'turn_heat_off'
    ADD_HERBS = 'add_herbs'
    CLOSE_LID = 'close_lid'
    CHECK_TRANSPORT = 'check_transport'
    ONION_MISUNDERSTANDING = 'onion_misunderstanding'
    SINCERE_FOLLOWUP = 'sincere_followup'
    REFILL_PANTRY = 'refill_pantry'


class Signal(Enum):
    AUDIO_END = 'audio_end'
    AUDIO_SKIP = 'audio_skip'
    ANIMATION_END = 'animation_end'


OBJECTS = ('hotpot_recipe', 'bean_tomato_base', 'vegetable_bowl', 'stock_bottle',
           'measuring_jug', 'herb_sachet', 'hotpot_pot', 'pot_lid', 'stove')
FIXTURES = frozenset(OBJECTS)
SOURCE_BINDINGS = MappingProxyType({Source.RECIPE: 'P07.READ.001', Source.JUG_MARK: 'P07.READ.002',
                                    Source.HERB_LABEL: 'P07.READ.003'})
LABEL_IDS = MappingProxyType({obj: f'P07.LABEL.{i:03}' for i, obj in enumerate(OBJECTS, 1)})
LOOK_IDS = MappingProxyType(dict(zip(OBJECTS, ('P07.LOOK.001', 'P07.INVENTORY.001',
    'P07.INVENTORY.002', 'P07.INVENTORY.003', 'P07.INVENTORY.004', 'P07.INVENTORY.005',
    'P07.LOOK.002', 'P07.LOOK.003', 'P07.LOOK.004'))))
RECEIPT_NAMES = ('intro', 'base', 'measure', 'stock', 'vegetables', 'cooked', 'heat_off',
                 'herbs', 'complete', 'onion', 'sincere', 'laugh', 'handoff')
STATE_KEYS = frozenset(('revision', 'receipts', 'observations', 'reader', 'handoff'))
OWN_FLAGS = frozenset(('FOOD_READY', 'KNOW_EIGHT_PORTIONS'))


def _int(value, low=0, high=MAX_SERIAL):
    if type(value) is not int or not low <= value <= high:
        raise ValueError('Expected a bounded integer, never bool')
    return value


def _enum(value, cls):
    if type(value) is not cls:
        raise ValueError('Expected an exact typed enum')
    return value


def _keys(value, expected):
    if type(value) is not dict or set(value) != set(expected):
        raise ValueError('Missing, extra or malformed fields')


def split_serial(value: int) -> tuple[int, int]:
    _int(value)
    return value >> 16, value & 65535


def join_serial(high: int, low: int) -> int:
    return (_int(high, 0, 65535) << 16) | _int(low, 0, 65535)


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def canonical_record(record_id: str) -> dict:
    return deepcopy(_RECORDS[record_id])


def canonical_unit(unit_id: str) -> dict:
    return deepcopy(_UNITS[unit_id])


@dataclass(frozen=True)
class OwnedObject:
    """Same named owner/room shape as P05; P07 only recognizes its own pot."""
    object_id: str
    owner: str
    room: str

    def __post_init__(self):
        if (type(self.object_id) is not str or self.object_id != 'hotpot_pot'
                or type(self.owner) is not str or self.owner not in {'P07', 'P13'}
                or type(self.room) is not str
                or self.room != (KITCHEN if self.owner == 'P07' else COURTYARD)):
            raise ValueError('Invalid exact pot ownership')


@dataclass(frozen=True)
class P07Context:
    room: str
    on_apron: bool = False
    flags: frozenset[str] = frozenset()
    inventory: frozenset[str] = frozenset()
    bunny_room: str = LIVING
    bunny_on_apron: bool = False
    bunny_invited_elsewhere: bool = False
    ownership: tuple[OwnedObject, ...] = ()

    def __post_init__(self):
        for room in (self.room, self.bunny_room):
            if type(room) is not str or room not in ROOMS:
                raise ValueError('Unknown campaign room')
        for b in (self.on_apron, self.bunny_on_apron, self.bunny_invited_elsewhere):
            if type(b) is not bool:
                raise ValueError('Campaign modes must be exact booleans')
        for facts in (self.flags, self.inventory):
            if type(facts) is not frozenset or any(type(v) is not str or not v for v in facts):
                raise ValueError('Campaign facts must be frozen string sets')
        if self.inventory & FIXTURES:
            raise ValueError('Kitchen fixtures and the single pot cannot be pocket duplicates')
        if (type(self.ownership) is not tuple or len(self.ownership) > 1
                or any(type(v) is not OwnedObject for v in self.ownership)):
            raise ValueError('Malformed or duplicate pot ownership')


@dataclass(frozen=True)
class ReceiptToken:
    source: Source
    request: int
    session: str
    lease: str


@dataclass(frozen=True)
class SourcePage:
    source: Source
    record_id: str
    index: int
    count: int
    text: str
    sha256: str


def source_pages(source: Source) -> tuple[SourcePage, ...]:
    """One complete source page, never a title, LOOK paraphrase or audio clip.

    All three canonical source records fit the existing 48 x 14 reader.
    Pagination here is a NEW logical binding, not an old native page number.
    """
    _enum(source, Source)
    record_id = SOURCE_BINDINGS[source]
    value = _RECORDS[record_id]['text']
    return (SourcePage(source, record_id, 0, 1, value, sha256(value.encode()).hexdigest()),)


@dataclass(frozen=True)
class Event:
    id: str
    serial: int
    after_unit_id: str = ''


@dataclass(frozen=True)
class P07Result:
    code: str
    revision: int
    record_ids: tuple[str, ...] = ()
    speech_unit_ids: tuple[str, ...] = ()
    events: tuple[Event, ...] = ()
    token: ReceiptToken | None = None
    pages: tuple[SourcePage, ...] = ()
    text: str = ''  # Deliberately empty: no new player-facing prose.

    @property
    def line_ids(self):
        return self.record_ids


@dataclass(frozen=True)
class PhysicalObject:
    object_id: str
    owner: str
    room: str
    location: str
    available: bool


@dataclass(frozen=True)
class Projection:
    objects: tuple[PhysicalObject, ...]
    contents: tuple[str, ...]
    pantry_refillable: bool
    heat_on: bool
    lid_closed: bool
    tasting_bowls: int
    full_suppers: int
    includes_jackie: bool
    flags: frozenset[str]
    pocket_items: tuple[str, ...] = ()


@dataclass(frozen=True)
class P13Handoff:
    """Trusted bounded host input, after real P13 has authorized this delivery.

    It does not implement seating, helper scheduling, buffet checks or SERVE.
    Those remain the P13 owner's responsibility. This is declarative data, not
    a session-bound authorization capability or a callback ticket. A real P13
    host must independently bind dispatch to its current session/lease.
    """
    delivery_id: str
    delivery_serial: int
    route: str = 'kitchen_hatch'
    object_id: str = 'hotpot_pot'
    destination: str = COURTYARD

    def __post_init__(self):
        _int(self.delivery_serial, 1)
        if (type(self.delivery_id) is not str or self.delivery_id != 'P13:OWN:hotpot_pot'
                or type(self.route) is not str or self.route != 'kitchen_hatch'
                or type(self.object_id) is not str or self.object_id != 'hotpot_pot'
                or type(self.destination) is not str or self.destination != COURTYARD):
            raise ValueError('Unsupported P13 pot handoff')


class RetiredLeaseError(RuntimeError):
    pass


class WorldBusyError(RuntimeError):
    pass


class HostLease:
    """UNSAVED host lifetime boundary. Native host must provide equivalent safety.

    Retire outside the restored VM before restoring that VM or replacing its
    callback dispatcher. Restored serials or a saved nonce prove no freshness.
    """
    def __init__(self):
        self._id = uuid4().hex
        self._active = True
        self._lock = RLock()

    @property
    def identity(self):
        return self._id

    @property
    def active(self):
        with self._lock:
            return self._active

    def retire(self):
        with self._lock:
            self._active = False

    def require_active(self):
        if not self._active:
            raise RetiredLeaseError('Host has retired this execution lease')


def _new_state():
    return {'revision': 0, 'receipts': dict.fromkeys(RECEIPT_NAMES, 0),
            'observations': {}, 'reader': None, 'handoff': None}


def _flags(state):
    return frozenset((['KNOW_EIGHT_PORTIONS'] if 'recipe' in state['observations'] else [])
                     + (['FOOD_READY'] if state['receipts']['complete'] else []))


def _envelope(state):
    core = {'kind': SAVE_KIND, 'schema': SAVE_SCHEMA, 'serial_encoding': SERIAL_ENCODING,
            'canonical_sha256': CANONICAL_SHA256, 'state': deepcopy(state)}
    return {**core, 'integrity_sha256': sha256(_json(core).encode()).hexdigest()}



def _validate_source_chronology(revision, chronology, final_reader):
    """Exact omitted-slot reachability, including which sources remain unread.

    Between retained commits, only unretained source openings, replacements or
    cancellations can consume a serial. Learning is permanent and must have a
    retained page receipt, so an omitted acknowledgment is never permitted.
    A gap is a walk on the loop-free complete graph whose vertices are no
    reader plus each STILL UNREAD source identity. Same-source reopening and
    a known-source read with no pending reader consume no serial.

    With zero unread sources no omitted step exists. With one, walks alternate
    between no reader and that exact source. With two or three, every vertex
    is reachable after any gap of at least two steps. This closed form handles
    the entire uint32 domain without iterating billions of serial slots.
    """
    unread = {source.value for source in Source}
    possible = {None}
    previous = 0

    def omitted_steps(states, count):
        if count == 0:
            return states
        vertices = unread | {None}
        if not unread:
            return set()
        if len(unread) == 1 and count % 2 == 0:
            return states
        if count == 1 or len(unread) == 1:
            return {target for current in states for target in vertices if target != current}
        return vertices if states else set()

    for serial, kind, source in sorted(chronology):
        possible = omitted_steps(possible, serial - previous - 1)
        if kind == 'physical':
            possible = {None} if None in possible else set()
        elif kind == 'request':
            possible = {source} if source in unread and possible - {source} else set()
        else:
            possible = {None} if source in unread and source in possible else set()
            unread.discard(source)
        if not possible:
            raise ValueError('Unreachable source identity/pending-reader chronology')
        previous = serial
    possible = omitted_steps(possible, revision - previous)
    if final_reader not in possible:
        raise ValueError('Unreachable final source-reader state')


def _validate_state(state):
    _keys(state, STATE_KEYS)
    rev = _int(state['revision'])
    receipts = state['receipts']; _keys(receipts, RECEIPT_NAMES)
    for serial in receipts.values():
        _int(serial, 0, rev)
    primary = [v for k, v in receipts.items() if v and k != 'laugh']
    chronology = [(serial, 'physical', name) for name, serial in receipts.items()
                  if serial and name != 'laugh']
    observations = state['observations']
    if type(observations) is not dict or not set(observations) <= {v.value for v in Source}:
        raise ValueError('Unknown or malformed source observations')

    def reader_receipt(row, source, complete):
        _keys(row, ('source', 'record_id', 'source_sha256', 'request', 'pages'))
        expected = source_pages(source)[0]
        if (type(row['source']) is not str or row['source'] != source.value
                or type(row['record_id']) is not str or row['record_id'] != expected.record_id
                or type(row['source_sha256']) is not str or row['source_sha256'] != expected.sha256):
            raise ValueError('Wrong exact source binding')
        _int(row['request'], 1, rev); primary.append(row['request'])
        chronology.append((row['request'], 'request', source.value))
        if type(row['pages']) is not list or len(row['pages']) != int(complete):
            raise ValueError('Incomplete, duplicate or fabricated source page receipts')
        if complete:
            page = row['pages'][0]; _keys(page, ('index', 'sha256', 'serial'))
            _int(page['index'], 0, 0)
            if type(page['sha256']) is not str or page['sha256'] != expected.sha256:
                raise ValueError('Wrong source page digest')
            _int(page['serial'], row['request'] + 1, row['request'] + 1)
            if page['serial'] > rev:
                raise ValueError('Source receipt lies beyond the saved timeline')
            primary.append(page['serial'])
            chronology.append((page['serial'], 'page', source.value))

    for name, row in observations.items():
        reader_receipt(row, Source(name), True)
    reader = state['reader']
    if reader is not None:
        if type(reader) is not dict or reader.get('source') not in {v.value for v in Source}:
            raise ValueError('Invalid pending source')
        if reader['source'] in observations:
            raise ValueError('Already learned source cannot retain a pending knowledge receipt')
        reader_receipt(reader, Source(reader['source']), False)
        if reader['request'] != rev or rev == MAX_SERIAL:
            raise ValueError('Pending reader must be current and reserve one completion/cancel serial')
    if len(primary) != len(set(primary)):
        raise ValueError('Independent commits cannot share serials')
    if len(primary) > rev:
        raise ValueError('Impossible minimum commit count')
    _validate_source_chronology(rev, chronology, reader['source'] if reader else None)

    def after(later, *earlier):
        if receipts[later] and any(not receipts[e] or receipts[later] <= receipts[e] for e in earlier):
            raise ValueError('Unreachable cooking receipt order: ' + later)

    recipe = observations.get('recipe')
    if receipts['measure'] and (not recipe or receipts['measure'] <= recipe['pages'][0]['serial']):
        raise ValueError('Measured tasting stock requires the actual complete recipe first')
    after('stock', 'measure')
    after('vegetables', 'base')
    after('cooked', 'base', 'stock', 'vegetables')
    after('heat_off', 'cooked')
    after('herbs', 'heat_off')
    after('complete', 'herbs')
    after('onion', 'base')
    after('sincere', 'onion')
    if receipts['onion'] and receipts['complete'] and receipts['onion'] >= receipts['complete']:
        raise ValueError('Onion misunderstanding belongs during preparation')
    if receipts['laugh'] != receipts['onion']:
        raise ValueError('LAF07 is the once-only comic misread, never a sincere receipt')
    if receipts['intro'] and receipts['complete'] and receipts['intro'] >= receipts['complete']:
        raise ValueError('Preparation introduction cannot first occur after completion')
    handoff = state['handoff']
    if (handoff is not None) != bool(receipts['handoff']):
        raise ValueError('Orphaned physical handoff')
    if handoff is not None:
        _keys(handoff, ('delivery_id', 'delivery_serial', 'route', 'object_id', 'destination'))
        P13Handoff(**handoff)
        after('handoff', 'complete')
    return True


class P07World:
    def __init__(self, *, lease: HostLease | None = None):
        if lease is not None and type(lease) is not HostLease:
            raise ValueError('Expected an explicit host lease')
        self._lease = lease if lease is not None else HostLease()
        self._lease.require_active()
        self._session = uuid4().hex
        self._state = _new_state()
        self._lock = RLock()
        self._busy = False

    @contextmanager
    def _access(self):
        with self._lock, self._lease._lock:
            self._lease.require_active()
            if self._busy:
                raise WorldBusyError('No reentrant input, save or restore during host publication')
            yield

    @property
    def lease(self):
        return self._lease

    @property
    def revision(self):
        with self._access():
            return self._state['revision']

    @property
    def flags(self):
        with self._access():
            return _flags(self._state)

    @property
    def state(self):
        with self._access():
            return deepcopy(self._state)

    def _context(self, context, state=None):
        if type(context) is not P07Context:
            raise ValueError('Expected immutable P07Context')
        s = self._state if state is None else state
        if context.flags & OWN_FLAGS - _flags(s):
            raise ValueError('Campaign claims unsupported P07 progress')
        if (any(s['receipts'].values()) or s['observations'] or s['reader']) and 'PLAN_AGREED' not in context.flags:
            raise ValueError('Progressed P07 cannot be composed with a pre-P02 timeline')
        if context.ownership:
            expected = OwnedObject('hotpot_pot', 'P13', COURTYARD) if s['handoff'] else OwnedObject('hotpot_pot', 'P07', KITCHEN)
            if context.ownership != (expected,):
                raise ValueError('Campaign pot ownership contradicts this saved timeline')
        if s['handoff'] and 'INTRODUCTION_CLEAR' not in context.flags:
            raise ValueError('P13 handoff requires the real campaign introduction')

    def validate(self, context=None):
        with self._access():
            _validate_state(self._state)
            if context is not None:
                self._context(context)
            return True

    def save(self):
        with self._access():
            _validate_state(self._state)
            return _envelope(self._state)

    def to_json(self):
        return _json(self.save())

    @classmethod
    def load(cls, envelope, context=None, *, lease=None):
        _keys(envelope, ('kind', 'schema', 'serial_encoding', 'canonical_sha256', 'state', 'integrity_sha256'))
        if (type(envelope['kind']) is not str or envelope['kind'] != SAVE_KIND
                or type(envelope['schema']) is not int or envelope['schema'] != SAVE_SCHEMA
                or type(envelope['serial_encoding']) is not str or envelope['serial_encoding'] != SERIAL_ENCODING
                or type(envelope['canonical_sha256']) is not str or envelope['canonical_sha256'] != CANONICAL_SHA256):
            raise ValueError('Unsupported reconstruction save format')
        core = {k: v for k, v in envelope.items() if k != 'integrity_sha256'}
        if type(envelope['integrity_sha256']) is not str or envelope['integrity_sha256'] != sha256(_json(core).encode()).hexdigest():
            raise ValueError('Save integrity mismatch')
        state = deepcopy(envelope['state']); _validate_state(state)
        world = cls(lease=lease); world._state = state
        if context is not None:
            world._context(context)
        return world

    @classmethod
    def from_json(cls, text, context=None, *, lease=None):
        if type(text) is not str or len(text.encode()) > 32768:
            raise ValueError('Expected bounded save JSON')
        def pairs(items):
            obj = {}
            for key, value in items:
                if key in obj:
                    raise ValueError('Duplicate JSON key')
                obj[key] = value
            return obj
        def constant(value):
            raise ValueError('Non-finite JSON number')
        try:
            data = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
            return cls.load(data, context, lease=lease)
        except (RecursionError, TypeError, OverflowError) as exc:
            raise ValueError('Malformed save') from exc

    def restore(self, envelope, context=None):
        """Validate first; then retire old lease, cancel old callbacks, replace timeline.

        Host must atomically restore its owner map/presentation with this timeline.
        A whole-VM rewind additionally requires an OUTSIDE-VM lease retirement.
        """
        with self._access():
            candidate = self.load(envelope, context)
            self._lease.retire()
            self._state = candidate._state
            self._lease = candidate._lease
            self._session = candidate._session

    def _result(self, code, state=None, records=(), *, units=None, events=(), token=None, pages=()):
        s = self._state if state is None else state
        if units is None:
            units = tuple(u['line_id'] for rid in records for u in _CANON['speech_units'] if u['record_id'] == rid)
        if any(r not in _RECORDS for r in records) or any(u not in _UNITS for u in units):
            raise ValueError('Unbound canonical output')
        return P07Result(code, s['revision'], tuple(records), tuple(units), tuple(events), token, tuple(pages))

    def _token(self, reader):
        return ReceiptToken(Source(reader['source']), reader['request'], self._session, self._lease.identity)

    def _token_matches(self, token):
        reader = self._state['reader']
        return (type(token) is ReceiptToken and reader is not None and token == self._token(reader)
                and type(token.request) is int and type(token.source) is Source)

    def _guard(self, context):
        self._context(context)
        if context.room != KITCHEN or context.on_apron:
            return 'offscreen'
        if 'PLAN_AGREED' not in context.flags:
            return 'plan_required'
        return None

    def _bunny(self, context):
        return context.bunny_room == KITCHEN and not context.bunny_on_apron and not context.bunny_invited_elsewhere

    def _next(self, state, reserve=0):
        if state['revision'] >= MAX_SERIAL - reserve:
            return None
        state['revision'] += 1
        return state['revision']

    def _publish(self, candidate, result, context, host):
        _validate_state(candidate)
        if candidate == self._state:
            return result
        if host is None:
            self._state = candidate
            return result
        # Every possible domain failure occurs before entering the host commit.
        from .composition import Transaction
        old_context = context
        new_context = context
        if candidate['handoff'] and not self._state['handoff']:
            from dataclasses import replace
            new_context = replace(context, ownership=(OwnedObject('hotpot_pot', 'P13', COURTYARD),))
        transaction = Transaction(_envelope(self._state), _envelope(candidate),
                                  self._projection(self._state, old_context),
                                  self._projection(candidate, new_context), result)
        self._busy = True
        try:
            prepared = host.prepare(transaction)
            host.commit(prepared)
            # No callbacks, validation, allocation, I/O or event dispatch here.
            self._state = candidate
        finally:
            self._busy = False
        return result

    def open_source(self, context: P07Context, source: Source, *, host=None):
        with self._access():
            _enum(source, Source)
            if error := self._guard(context):
                return self._result(error)
            s = deepcopy(self._state)
            rid = SOURCE_BINDINGS[source]; pages = source_pages(source)
            if source.value in s['observations']:
                if s['reader']:
                    if self._next(s) is None:
                        return self._result('serial_exhausted')
                    s['reader'] = None
                return self._publish(s, self._result('source_known', s, (rid,), pages=pages), context, host)
            if s['reader'] and s['reader']['source'] == source.value:
                return self._result('source_pending', s, (rid,), token=self._token(s['reader']), pages=pages)
            if self._next(s, reserve=1) is None:
                return self._result('serial_exhausted')
            page = pages[0]
            s['reader'] = {'source': source.value, 'record_id': rid, 'source_sha256': page.sha256,
                           'request': s['revision'], 'pages': []}
            result = self._result('source_pending', s, (rid,), token=self._token(s['reader']), pages=pages)
            return self._publish(s, result, context, host)

    def acknowledge_source_page(self, context: P07Context, token: ReceiptToken, page: SourcePage, *, host=None):
        """Trusted host receipt AFTER the exact full page has really been displayed."""
        with self._access():
            if error := self._guard(context):
                return self._result(error)
            if not self._token_matches(token):
                return self._result('stale_receipt')
            expected = source_pages(token.source)[0]
            if (type(page) is not SourcePage or type(page.index) is not int or type(page.count) is not int
                    or type(page.source) is not Source or page != expected):
                return self._result('wrong_source_page')
            s = deepcopy(self._state)
            serial = self._next(s)
            if serial is None:
                return self._result('serial_exhausted')
            row = s['reader']; row['pages'] = [{'index': 0, 'sha256': expected.sha256, 'serial': serial}]
            s['observations'][token.source.value] = row; s['reader'] = None
            return self._publish(s, self._result('source_observed', s), context, host)

    def cancel_source(self, token: ReceiptToken, *, host=None, context=None):
        with self._access():
            if not self._token_matches(token):
                return self._result('stale_receipt')
            if context is None:
                context = P07Context(KITCHEN, flags=frozenset({'PLAN_AGREED', 'INTRODUCTION_CLEAR'}))
            self._context(context)
            s = deepcopy(self._state)
            if self._next(s) is None:
                return self._result('serial_exhausted')
            s['reader'] = None
            return self._publish(s, self._result('source_cancelled', s), context, host)

    def presentation_signal(self, signal: Signal, token=None):
        with self._access():
            _enum(signal, Signal)
            return self._result('presentation_only')

    def perform(self, context: P07Context, action: Action, *, measure=None, host=None):
        with self._access():
            _enum(action, Action)
            if action == Action.MEASURE_STOCK:
                _enum(measure, Measure)
            elif measure is not None:
                raise ValueError('Unexpected measure argument')
            if error := self._guard(context):
                return self._result(error)
            s = deepcopy(self._state); r = s['receipts']
            # A host must finish/cancel its reader before another logical action.
            # No ingredient is consumed by any failed or pending-reader action.
            if s['reader']:
                return self._result('reader_pending')
            if action == Action.CHECK_TRANSPORT:
                if r['complete']:
                    return self._result('pot_handed_off' if r['handoff'] else 'pot_waiting', records=() if r['handoff'] else ('P07.LOOK.005',))
                return self._result('lid_required', records=('P07.FAILURE.003',)) if r['herbs'] else self._result('food_not_finished')
            if action == Action.REFILL_PANTRY:
                return self._result('pantry_closed' if r['complete'] else 'pantry_refillable')
            if r['complete'] and action != Action.SINCERE_FOLLOWUP:
                return self._result('already_complete')
            field, records, events, units = None, (), (), None
            if action == Action.INTRODUCE:
                if not self._bunny(context):
                    return self._result('bunny_absent')
                field, records = 'intro', ('P07.SCENE.001',)
            elif action == Action.ADD_BASE:
                field, records = 'base', ('P07.SUCCESS.001',)
            elif action == Action.MEASURE_STOCK:
                if measure == Measure.SIX_SUPPERS:
                    return self._result('measure_too_small', records=('P07.FAILURE.002',))
                if 'recipe' not in s['observations']:
                    return self._result('recipe_required')
                field, records = 'measure', ('P07.SUCCESS.002',)
            elif action == Action.ADD_STOCK:
                if not r['measure']:
                    return self._result('measured_stock_required')
                field, records = 'stock', ('P07.SUCCESS.003',)
            elif action == Action.ADD_VEGETABLES:
                if not r['base']:
                    return self._result('base_required')
                field, records = 'vegetables', ('P07.SUCCESS.004',)
            elif action == Action.COOK:
                if not (r['base'] and r['stock'] and r['vegetables']):
                    return self._result('cooked_components_required')
                field, records = 'cooked', ('P07.SUCCESS.005',)
            elif action == Action.TURN_HEAT_OFF:
                if not r['cooked']:
                    return self._result('not_cooked')
                field, records = 'heat_off', ('P07.SUCCESS.006',)
            elif action == Action.ADD_HERBS:
                if r['cooked'] and not r['heat_off']:
                    return self._result('herbs_over_heat', records=('P07.FAILURE.001',))
                if not r['heat_off']:
                    return self._result('cook_first')
                field, records = 'herbs', ('P07.SUCCESS.007',)
            elif action == Action.CLOSE_LID:
                if not r['herbs']:
                    return self._result('food_not_finished')
                field, records = 'complete', ('P07.SUCCESS.008', 'P07.SUCCESS.009')
            elif action == Action.ONION_MISUNDERSTANDING:
                if not r['base']:
                    return self._result('preparation_required')
                if not self._bunny(context):
                    return self._result('bunny_absent')
                field, records = 'onion', ('P07.SCENE.002',)
                units = tuple(f'P07.SCENE.002.{i:02}' for i in (1, 2, 3))
            elif action == Action.SINCERE_FOLLOWUP:
                if not r['onion']:
                    return self._result('misunderstanding_not_played')
                if not self._bunny(context):
                    return self._result('bunny_absent')
                field, records = 'sincere', ('P07.SCENE.002',)
                units = tuple(f'P07.SCENE.002.{i:02}' for i in (4, 5))
            if r[field]:
                return self._result('already_done')
            serial = self._next(s)
            if serial is None:
                return self._result('serial_exhausted')
            r[field] = serial
            if field == 'onion':
                r['laugh'] = serial
                events = (Event('LAF07', serial, 'P07.SCENE.002.02'),)
            if field == 'complete':
                events = (Event('FOOD_READY', serial),)
            return self._publish(s, self._result('food_ready' if field == 'complete' else field, s,
                                                records, units=units, events=events), context, host)

    def use_stove(self, context, *, host=None):
        with self._access():
            # Keep the toggle choice and commit under the same lock.
            action = Action.TURN_HEAT_OFF if self._state['receipts']['cooked'] else Action.COOK
            return self.perform(context, action, host=host)

    def hint(self, context, level: int):
        with self._access():
            _int(level, 1, 3)
            self._context(context)
            return self._result('hint', records=(f'P07.HINT.{level}',))

    def measure_choices(self, context):
        with self._access():
            if error := self._guard(context):
                return self._result(error)
            return self._result('measure_choices', records=('P07.CHOICE.001', 'P07.CHOICE.002'))

    def look(self, context, object_id: str):
        with self._access():
            self._context(context)
            if type(object_id) is not str or object_id not in FIXTURES:
                raise ValueError('Unknown P07 object')
            if context.on_apron or context.room != KITCHEN:
                return self._result('offscreen')
            r = self._state['receipts']
            if object_id in {'hotpot_pot', 'pot_lid'} and r['handoff']:
                return self._result('foreign_owner')
            rid = LOOK_IDS[object_id]
            if object_id == 'hotpot_pot' and r['complete']:
                rid = 'P07.LOOK.005'
            if object_id == 'measuring_jug' and r['measure'] and not r['stock']:
                rid = 'P07.INVENTORY.006'
            return self._result('look', records=(rid,))

    def label(self, object_id: str):
        with self._access():
            if type(object_id) is not str or object_id not in FIXTURES:
                raise ValueError('Unknown P07 object')
            return self._result('label', records=(LABEL_IDS[object_id],))

    def _projection(self, state, context):
        self._context(context, state)
        r = state['receipts']; complete = bool(r['complete']); foreign = bool(r['handoff'])
        objects = []
        for obj in OBJECTS:
            if foreign and obj in {'hotpot_pot', 'pot_lid'}:
                continue
            location = 'kitchen_fixture'
            if obj == 'hotpot_pot':
                location = 'kitchen_waiting' if complete else 'stove'
            elif obj == 'pot_lid':
                location = 'on_hotpot' if complete else 'beside_hotpot'
            elif obj == 'measuring_jug':
                location = 'measured_eight' if r['measure'] and not r['stock'] else 'empty_jug'
            usable = not complete if obj in {'bean_tomato_base', 'vegetable_bowl', 'stock_bottle', 'herb_sachet'} else True
            objects.append(PhysicalObject(obj, 'P07', KITCHEN, location, usable))
        contents = tuple(name for name in ('base', 'stock', 'vegetables', 'herbs') if r[name]) if not foreign else ()
        return Projection(tuple(objects), contents, not complete, bool(r['cooked'] and not r['heat_off']),
                          complete and not foreign, 8 if complete and not foreign else 0,
                          0, complete and not foreign, _flags(state))

    def projection(self, context):
        with self._access():
            return self._projection(self._state, context)

    def handoff_to_p13(self, context: P07Context, request: P13Handoff, *, host):
        """Atomic host-only release of this exact pot; emits no SERVED grant."""
        with self._access():
            if type(request) is not P13Handoff:
                raise ValueError('Expected exact P13 handoff evidence')
            if host is None:
                raise ValueError('P13 transfer requires a physical transaction host')
            if error := self._guard(context):
                return self._result(error)
            s = deepcopy(self._state); r = s['receipts']
            if s['handoff']:
                return self._result('already_handed_off')
            if s['reader']:
                return self._result('reader_pending')
            if not r['complete']:
                return self._result('food_not_ready')
            if 'INTRODUCTION_CLEAR' not in context.flags:
                return self._result('p13_not_available')
            if not self._bunny(context):
                return self._result('bunny_absent')
            if self._next(s) is None:
                return self._result('serial_exhausted')
            r['handoff'] = s['revision']
            s['handoff'] = {k: getattr(request, k) for k in ('delivery_id', 'delivery_serial', 'route', 'object_id', 'destination')}
            return self._publish(s, self._result('pot_handed_off', s), context, host)
