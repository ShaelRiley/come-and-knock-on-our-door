"""Independent canonical reference model. No SCI runtime or historical ABI claim.

Every mutation is copy/validate/persist/publish. Text receipts, not audio callbacks,
advance learning and readable-result presentation. Runtime tokens carry a bounded
host-owned generation; their saved logical IDs never change on restore.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import threading
from dataclasses import dataclass
from enum import IntEnum
from functools import wraps
from types import MappingProxyType
from typing import Callable, Iterable

MAX_SERIAL = (1 << 30) - 1
LIMB_BASE = 1 << 15
SCHEMA = 1
MAX_SAVE_BYTES = 131072
YIELD_EXCHANGE = 'yield_exchange'
TIERS = 'ABCD'

class ContestError(ValueError): pass
class StateError(ContestError): pass
class ReceiptError(ContestError): pass
class CorruptSave(ContestError): pass
class SerialExhausted(ContestError): pass
class ReentrancyError(ContestError): pass
class DurabilityUncertain(OSError): pass

class Phase(IntEnum):
    TURN_READY = 1
    SETUP_PENDING = 2
    CHOICE = 3
    RESPONSE_PENDING = 4
    FEEDBACK_PENDING = 5
    KO_PENDING = 6
    RESULT_PENDING = 7
    DONE = 8

@dataclass(frozen=True)
class PairSpec:
    id: str
    retort_id: str
    accepted_response_ids: frozenset[str]

    @property
    def tier(self): return TIERS[(int(self.id[2:]) - 1) // 6]

@dataclass(frozen=True)
class Encounter:
    id: str
    opponent: str
    speaker_id: str
    tier: int
    host_requirements: tuple[str, ...]

ENCOUNTERS = MappingProxyType({
    'VC01': Encounter('VC01', 'Milo Pennant', 'milo', 1, ('PA_TESTED', 'MILO_ROLE_AGREED')),
    'VC02': Encounter('VC02', 'Vivian Voss', 'vivian', 2, ('SCREEN_BUILT', 'VIVIAN_SCOPE_AGREED')),
    'VC03': Encounter('VC03', 'Felix Bunt', 'felix', 3, ('DISPLAY_STAGED', 'PROTECTED_RESCUE_CONVERSATION_FINISHED')),
    'VC04': Encounter('VC04', 'Mr. Stringer', 'stringer', 4, ('SERVED', 'DISPLAY_REVEALED', 'PLEDGE_BOARD_PHYSICALLY_DELIVERED')),
})

@dataclass(frozen=True)
class EventId:
    owner_generation: int
    attempt: int
    kind: str
    slot: int = 0

@dataclass(frozen=True)
class TextReceipt:
    owner_generation: int
    serial: int
    item: int
    record_id: str
    unit_id: str | None

@dataclass(frozen=True)
class Presentation:
    receipt: TextReceipt
    text: str
    record_id: str
    unit_id: str | None
    speaker_id: str | None
    bindings: tuple[tuple[str, str], ...] = ()

@dataclass(frozen=True)
class Lesson:
    pair_id: str
    setup_learned: bool
    reply_learned: bool
    record_ids: tuple[str, ...]

@dataclass(frozen=True)
class Attempt:
    id: EventId
    serial: int
    encounter_id: str
    phase: Phase
    seed: int
    deck: tuple[str, ...]
    cursor: int
    jackie_composure: int
    opponent_composure: int
    pending_response: str | None
    exchange_id: EventId | None
    outcome_id: EventId
    winner: str | None
    reason: str | None
    exchanges: tuple[tuple[str, str, bool], ...]


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')

def _integer(value, lo=0, hi=MAX_SERIAL):
    return type(value) is int and lo <= value <= hi

def _require(condition, message, error=StateError):
    if not condition: raise error(message)

def split_serial(value):
    _require(_integer(value), 'serial out of range')
    return value // LIMB_BASE, value % LIMB_BASE

def join_serial(high, low):
    _require(_integer(high, 0, 32767) and _integer(low, 0, 32767), 'invalid serial limbs')
    return high * LIMB_BASE + low


def _locked(method):
    @wraps(method)
    def call(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    return call


class Catalog:
    """Immutable semantic IDs, with full canonical text supplied separately.

    The witnessed three-argument PairSpec constructor is retained. Supplying specs
    is permitted only when they exactly match the complete canonical 24-pair set.
    """
    def __init__(self, pairs: Iterable[PairSpec] | None = None, *, fixture: Path | None = None):
        path = fixture or Path(__file__).resolve().parents[1] / 'data' / 'canonical-bindings.json'
        data = json.loads(path.read_text())
        specs = [PairSpec(p['pair_id'], p['pair_id'] + '.REPLY', frozenset(p['accepted_response_ids'])) for p in data['pairs']]
        if pairs is not None:
            given = list(pairs)
            _require(len(given) == 24 and {p.id: p for p in given} == {p.id: p for p in specs}, 'catalog must preserve all 24 exact answer sets')
        _require(len(specs) == 24 and [p.id for p in specs] == [f'IR{i:02}' for i in range(1, 25)], 'invalid canonical pair sequence')
        _require(sum(len(p.accepted_response_ids) - 1 for p in specs) == 12, 'invalid cross-answer count')
        self.pairs = MappingProxyType({p.id: p for p in specs})
        self._records = {r['id']: r for r in data['records']}
        self._units = {u['line_id']: u for u in data['speech_units']}
        self._data = data
        _require(len(self._records) == len(data['records']), 'duplicate record')
        _require(len(self._units) == len(data['speech_units']), 'duplicate speech unit')
        for p in data['pairs']:
            for suffix, field in [('SETUP', 'insult'), ('REPLY', 'counter'), ('RECAP', 'semantic_hook')]:
                _require(self._records[p['pair_id'] + '.' + suffix]['text'] == p[field], 'canonical wording mismatch')
            _require(all(r in {q.retort_id for q in specs} for r in p['accepted_response_ids']), 'unknown answer')
        ledger = data['writer_ledger']
        _require(len(ledger['writers']) == 8 and all(w['accepted_count'] == 3 and sum(p['writer_id'] == w['writer_id'] for p in data['pairs']) == 3 for w in ledger['writers']), 'writer balance mismatch')
        self.fingerprint = hashlib.sha256(_canonical({'pairs':data['pairs'], 'records':data['records'], 'units':data['speech_units'], 'ledger':ledger})).hexdigest()

    def record(self, record_id): return copy.deepcopy(self._records[record_id])
    def speech_unit(self, unit_id): return copy.deepcopy(self._units[unit_id])
    def eligible(self, encounter_id):
        n = ENCOUNTERS[encounter_id].tier * 6
        return tuple(f'IR{i:02}' for i in range(1, n + 1))
    def items(self, record_id, *, encounter_id=None):
        record = self._records[record_id]
        if record['kind'] == 'insult':
            unit = record_id + '.' + encounter_id + '.01' if encounter_id else None
            if unit: _require(unit in self._units, 'setup speaker binding unavailable')
            return [{'record': record_id, 'unit': unit}]
        units = [u for u in self._units.values() if u['record_id'] == record_id]
        if isinstance(record['text'], list):
            _require(len(units) == len(record['text']), 'ensemble record is not fully bound')
            return [{'record': record_id, 'unit': u['line_id']} for u in units]
        # Canonical single text may be read silently; a single unit binds speech.
        return [{'record': record_id, 'unit': units[0]['line_id'] if len(units) == 1 else None}]


class _Shuffle:
    """16-bit full-period LCG, reducible to byte products in signed SCI words."""
    def __init__(self, seed): self.state = seed
    def next(self):
        # 25173*x+13849 mod 65536. No intermediate above signed16 in this form.
        lo, hi = self.state % 256, self.state // 256
        t = 85 * lo + 25
        low = t % 256
        high = ((85 * hi) % 256 + (98 * lo) % 256 + 54 + t // 256) % 256
        self.state = high * 256 + low
        # Byte-swapped output avoids low-bit LCG correlations in small moduli.
        return low * 256 + high
    def below(self, n):
        limit = 65536 - 65536 % n
        while True:
            value = self.next()
            if value < limit: return value % n
    def shuffle(self, group):
        group = list(group)
        for i in range(len(group) - 1, 0, -1):
            j = self.below(i + 1)
            group[i], group[j] = group[j], group[i]
        return group


def make_deck(encounter_id, seed):
    _require(encounter_id in ENCOUNTERS and _integer(seed, 0, 65535), 'invalid deck input')
    tier = ENCOUNTERS[encounter_id].tier
    rand = _Shuffle(seed)
    recent = [f'IR{i:02}' for i in range((tier - 1) * 6 + 1, tier * 6 + 1)]
    if tier == 1: return tuple(rand.shuffle(recent)[:5])
    earlier = [f'IR{i:02}' for i in range(1, (tier - 1) * 6 + 1)]
    return tuple(rand.shuffle(recent)[:2] + rand.shuffle(earlier)[:3])


def _new_state():
    return {'revision': 0, 'attempt_serial': 0, 'presentation_serial': 0,
            'introduced': [], 'knowledge': {f'IR{i:02}': {'setup':False, 'reply':False} for i in range(1, 25)},
            'history': {e: {'completed':0, 'wins':0, 'latest_winner':None, 'concession_record':None, 'last_outcome':None} for e in ENCOUNTERS},
            'active':None, 'presentation':None}


class VerbalContests:
    def __init__(self, catalog: Catalog | None = None, *, owner_generation=1, persist: Callable[[bytes], None] | None = None):
        _require(_integer(owner_generation, 1), 'invalid host ownership generation')
        self.catalog = catalog or Catalog()
        self.owner_generation = owner_generation
        self._state = _new_state()
        self._persist = persist
        self._lock = threading.RLock()
        self._busy = False
        self._uncertain = False
        self._suppressed = set()
        self.validate()

    def _transaction(self, operation):
        if not self._lock.acquire(blocking=False): raise ReentrancyError('concurrent mutation')
        entered = False
        try:
            if self._busy: raise ReentrancyError('reentrant mutation')
            if self._uncertain: raise StateError('storage outcome uncertain; recover authoritative snapshot first')
            self._busy = True
            entered = True
            candidate = copy.deepcopy(self._state)
            _require(candidate['revision'] < MAX_SERIAL, 'revision exhausted', SerialExhausted)
            result = operation(candidate)
            candidate['revision'] += 1
            self._validate(candidate)
            if self._persist:
                try: self._persist(self._encode(candidate))
                except DurabilityUncertain:
                    self._uncertain = True
                    raise
            self._state = candidate
            return result
        finally:
            if entered: self._busy = False
            self._lock.release()

    def snapshot(self):
        with self._lock: return copy.deepcopy(self._state)
    @property
    def revision(self): return self._state['revision']
    @property
    def flags(self):
        h = self._state['history']
        flags = {e + '_RESOLVED' for e in h if h[e]['completed']}
        flags.update(e + '_WON' for e in h if h[e]['wins'])
        if all(h[e]['wins'] for e in h): flags.add('ALL_VC_WON')
        return frozenset(flags)
    @property
    def result_presentation_pending(self):
        a = self._state['active']
        return bool(a and a['phase'] == Phase.RESULT_PENDING)
    @property
    def missing_wins(self): return tuple(e for e in ENCOUNTERS if not self._state['history'][e]['wins'])
    @property
    @_locked
    def active(self):
        a = self._state['active']
        if a is None: return None
        return Attempt(self._event(a, 'attempt'), a['serial'], a['encounter'], Phase(a['phase']), a['seed'], tuple(a['deck']), a['cursor'], a['jackie'], a['opponent'], a['pending_response'], self._event(a, 'exchange', a['exchange_slot']) if a['exchange_slot'] else None, self._event(a, 'outcome'), a['winner'], a['reason'], tuple((x['pair'], x['response'], x['correct']) for x in a['exchanges']))
    def _event(self, a, kind, slot=0): return EventId(self.owner_generation, a['serial'], kind, slot)
    def _check_event(self, a, token, kind, slot=0):
        _require(type(token) is EventId and _integer(token.owner_generation, 1) and _integer(token.attempt, 1) and _integer(token.slot, 0, 5) and token == self._event(a, kind, slot), 'stale or mismatched event', ReceiptError)
    def _idle(self, s):
        _require(s['presentation'] is None, 'readable presentation still pending')
        _require(s['active'] is None or s['active']['phase'] == Phase.DONE, 'attempt still active')
    def _start_presentation(self, s, purpose, source, items, pair=None):
        _require(s['presentation'] is None, 'presentation already pending')
        _require(s['presentation_serial'] < MAX_SERIAL, 'presentation serial exhausted', SerialExhausted)
        s['presentation_serial'] += 1
        s['presentation'] = {'serial':s['presentation_serial'], 'purpose':purpose, 'source':source, 'pair':pair, 'items':items, 'cursor':0}
    def _present_records(self, s, purpose, source, records, pair=None):
        items = []
        for rid in records: items += self.catalog.items(rid, encounter_id=source if source in ENCOUNTERS else None)
        self._start_presentation(s, purpose, source, items, pair)

    def introduce(self, encounter_id, *, admitted=False):
        """Host attests current narrative prerequisites; this does not grant them."""
        _require(encounter_id in ENCOUNTERS and admitted is True, 'host narrative admission required')
        def change(s):
            self._idle(s)
            _require(encounter_id not in s['introduced'], 'already introduced')
            s['introduced'].append(encounter_id)
            s['introduced'].sort()
            self._present_records(s, 'entry', encounter_id, [encounter_id + '.ENTRY'])
        self._transaction(change)
        return self.pending_text()

    def recap(self, encounter_id):
        _require(encounter_id in self._state['introduced'], 'contest not introduced')
        return tuple(Lesson(p, self._state['knowledge'][p]['setup'], self._state['knowledge'][p]['reply'], (p+'.SETUP', p+'.REPLY', p+'.RECAP')) for p in self.catalog.eligible(encounter_id))

    def present_lesson(self, encounter_id, pair_id, *, half=None):
        """Request readable text; only acknowledge_text teaches its displayed half."""
        _require(half in (None, 'setup', 'reply', 'recap'), 'invalid lesson half')
        def change(s):
            self._idle(s)
            _require(encounter_id in s['introduced'] and pair_id in self.catalog.eligible(encounter_id), 'ineligible lesson')
            records = [pair_id + '.' + h.upper() for h in ([half] if half else ['setup', 'reply', 'recap'])]
            self._present_records(s, 'lesson', encounter_id, records, pair_id)
        self._transaction(change)
        return self.pending_text()

    def present_external_lesson(self, pair_id, *, source, admitted=False, half=None):
        """Explicit host receipt route for canonical P02/P06/safe-P11/P12–P13 banter."""
        source_tier = {'P02':'A', 'P06':'B', 'P11_SAFE':'C', 'P12_P13':'D'}
        _require(admitted is True and source in source_tier and pair_id in self.catalog.pairs and self.catalog.pairs[pair_id].tier == source_tier[source], 'host learning admission required')
        _require(half in (None, 'setup', 'reply', 'recap'), 'invalid lesson half')
        def change(s):
            self._idle(s)
            records = [pair_id + '.' + h.upper() for h in ([half] if half else ['setup', 'reply', 'recap'])]
            # Read-only notebook text does not invent speakers outside existing cast.
            self._present_records(s, 'lesson', source, records, pair_id)
        self._transaction(change)
        return self.pending_text()

    def cancel_lesson(self):
        def change(s):
            _require(s['presentation'] is not None and s['presentation']['purpose'] == 'lesson', 'only practice text may be closed')
            s['presentation'] = None
        self._transaction(change)

    @_locked
    def pending_text(self):
        p = self._state['presentation']
        if p is None: return None
        item = p['items'][p['cursor']]
        rid, uid = item['record'], item['unit']
        record = self.catalog._records[rid]
        unit = self.catalog._units[uid] if uid else None
        raw = unit['text'] if unit else record['text']
        _require(isinstance(raw, str), 'record requires individual unit presentation')
        e = ENCOUNTERS.get(p['source'])
        bindings = {'opponent_name': e.opponent} if e else {}
        text = raw
        for key, value in bindings.items(): text = text.replace('{' + key + '}', value)
        return Presentation(TextReceipt(self.owner_generation, p['serial'], p['cursor'], rid, uid), text, rid, uid, unit['speaker_id'] if unit else None, tuple(sorted(bindings.items())))

    def acknowledge_text(self, receipt):
        def change(s):
            p = s['presentation']
            _require(p is not None, 'no presentation pending', ReceiptError)
            item = p['items'][p['cursor']]
            expected = TextReceipt(self.owner_generation, p['serial'], p['cursor'], item['record'], item['unit'])
            _require(type(receipt) is TextReceipt and _integer(receipt.owner_generation, 1) and _integer(receipt.serial, 1) and _integer(receipt.item) and receipt == expected, 'stale or mismatched text receipt', ReceiptError)
            if p['purpose'] == 'lesson':
                suffix = item['record'].rsplit('.', 1)[1].lower()
                if suffix in ('setup','reply'): s['knowledge'][p['pair']][suffix] = True
            p['cursor'] += 1
            if p['cursor'] == len(p['items']):
                purpose = p['purpose']
                s['presentation'] = None
                a = s['active']
                if purpose == 'setup': a['phase'] = Phase.CHOICE.value
                elif purpose == 'feedback': a['phase'] = (Phase.KO_PENDING if a['winner'] else Phase.TURN_READY).value
                elif purpose == 'result':
                    a['phase'] = Phase.DONE.value
                    a['result_presented'] = True
        self._transaction(change)
        return self.pending_text()

    def available_responses(self):
        return tuple(p.retort_id for p in self.catalog.pairs.values() if self._state['knowledge'][p.id]['reply'])
    def notebook_pair(self, pair_id):
        _require(pair_id in self.catalog.pairs, 'unknown pair')
        k = self._state['knowledge'][pair_id]
        # No return of an unlearned answer or its semantic explanation.
        return {'pair_id':pair_id, 'setup':self.catalog._records[pair_id+'.SETUP']['text'] if k['setup'] else None,
                'reply':self.catalog._records[pair_id+'.REPLY']['text'] if k['reply'] else None,
                'accepted_learned_responses':tuple(r for r in self.available_responses() if r in self.catalog.pairs[pair_id].accepted_response_ids) if k['setup'] else ()}
    def practice_response(self, pair_id, response_id):
        _require(pair_id in self.catalog.pairs and self._state['knowledge'][pair_id]['setup'], 'setup not learned')
        _require(response_id in self.available_responses(), 'reply not learned')
        return 'VC.PRACTICE.CORRECT' if response_id in self.catalog.pairs[pair_id].accepted_response_ids else 'VC.PRACTICE.MISMATCH'

    def enter(self, encounter_id, seed, *, admitted=False):
        _require(encounter_id in ENCOUNTERS and admitted is True, 'current host narrative admission required')
        deck = make_deck(encounter_id, seed)
        def change(s):
            self._idle(s)
            _require(encounter_id in s['introduced'], 'contest not introduced')
            _require(all(all(s['knowledge'][p].values()) for p in self.catalog.eligible(encounter_id)), 'complete eligible repertoire must be presented first')
            _require(s['attempt_serial'] < MAX_SERIAL, 'attempt serial exhausted', SerialExhausted)
            s['attempt_serial'] += 1
            s['active'] = {'serial':s['attempt_serial'], 'encounter':encounter_id, 'phase':Phase.TURN_READY.value,
                'seed':seed, 'deck':list(deck), 'cursor':0, 'jackie':3, 'opponent':3, 'pending_response':None,
                'exchange_slot':0, 'winner':None, 'reason':None, 'exchanges':[], 'ko_committed':False,
                'ko_consumed':False, 'result_presented':False, 'had_prior_win':bool(s['history'][encounter_id]['wins'])}
        self._transaction(change)
        return self.active

    def begin_turn(self, attempt_id):
        def change(s):
            a = s['active']; _require(a is not None, 'no attempt')
            self._check_event(a, attempt_id, 'attempt')
            _require(a['phase'] == Phase.TURN_READY and s['presentation'] is None, 'turn is not ready')
            a['exchange_slot'] = a['cursor'] + 1
            a['phase'] = Phase.SETUP_PENDING.value
            self._present_records(s, 'setup', a['encounter'], [a['deck'][a['cursor']]+'.SETUP'])
        self._transaction(change)
        return self.pending_text()

    def choose_response(self, exchange_id, response_id):
        def change(s):
            a = s['active']; _require(a is not None, 'no attempt')
            self._check_event(a, exchange_id, 'exchange', a['exchange_slot'])
            _require(a['phase'] in (Phase.CHOICE, Phase.RESPONSE_PENDING), 'not choosing a response')
            _require(response_id == YIELD_EXCHANGE or response_id in self.available_responses(), 'reply not learned')
            a['pending_response'] = response_id
            a['phase'] = Phase.RESPONSE_PENDING.value
        self._transaction(change)

    def commit_response(self, exchange_id):
        def change(s):
            a = s['active']; _require(a is not None, 'no attempt')
            self._check_event(a, exchange_id, 'exchange', a['exchange_slot'])
            _require(a['phase'] == Phase.RESPONSE_PENDING, 'response not pending')
            response = a['pending_response']; pair = a['deck'][a['cursor']]
            correct = response in self.catalog.pairs[pair].accepted_response_ids
            a['opponent' if correct else 'jackie'] -= 1
            a['exchanges'].append({'slot':a['exchange_slot'], 'pair':pair, 'response':response, 'correct':correct, 'effect_consumed':False})
            a['cursor'] += 1
            a['pending_response'] = None
            a['phase'] = Phase.FEEDBACK_PENDING.value
            if a['jackie'] == 0 or a['opponent'] == 0:
                a['winner'] = 'jackie' if a['opponent'] == 0 else 'opponent'
                a['reason'] = 'zero'
            feedback = 'VC.RESULT.HIT_OPPONENT' if correct else ('VC.RESULT.YIELD_EXCHANGE' if response == YIELD_EXCHANGE else 'VC.RESULT.HIT_JACKIE')
            records = ([] if response == YIELD_EXCHANGE else [response]) + [feedback]
            self._present_records(s, 'feedback', a['encounter'], records)
        self._transaction(change)
        return self.pending_text()

    def yield_exchange(self, exchange_id):
        self.choose_response(exchange_id, YIELD_EXCHANGE)
        return self.commit_response(exchange_id)

    def yield_contest(self, attempt_id):
        def change(s):
            a = s['active']; _require(a is not None, 'no attempt')
            self._check_event(a, attempt_id, 'attempt')
            _require(a['phase'] in (Phase.TURN_READY, Phase.SETUP_PENDING, Phase.CHOICE, Phase.RESPONSE_PENDING), 'finish committed feedback/result first')
            s['presentation'] = None
            a['pending_response'] = None
            a['winner'] = 'opponent'; a['reason'] = 'yield'
            a['phase'] = Phase.KO_PENDING.value
        self._transaction(change)
        return self.active.outcome_id

    def commit_ko(self, outcome_id):
        def change(s):
            a = s['active']; _require(a is not None, 'no attempt')
            self._check_event(a, outcome_id, 'outcome')
            _require(a['phase'] == Phase.KO_PENDING and not a['ko_committed'], 'outcome not pending')
            h = s['history'][a['encounter']]
            _require(h['completed'] < MAX_SERIAL and h['wins'] < MAX_SERIAL, 'result history exhausted', SerialExhausted)
            h['completed'] += 1
            if a['winner'] == 'jackie': h['wins'] += 1
            h['latest_winner'] = a['winner']
            h['concession_record'] = a['encounter'] + ('.WIN' if a['winner'] == 'jackie' else '.LOSS')
            h['last_outcome'] = a['serial']
            a['ko_committed'] = True
            a['phase'] = Phase.RESULT_PENDING.value
            generic = 'VC.RESULT.YIELD_CONTEST' if a['reason'] == 'yield' else ('VC.RESULT.WIN' if a['winner'] == 'jackie' else 'VC.RESULT.LOSS')
            records = [generic, h['concession_record']]
            if a['winner'] == 'opponent' and a['had_prior_win']: records.append('VC.RESULT.EARLIER_WIN')
            self._present_records(s, 'result', a['encounter'], records)
        self._transaction(change)
        return self.pending_text()

    @_locked
    def claim_effect(self, event_id):
        """Persist consumption before host plays one transient; no audio is run here."""
        _require(type(event_id) is EventId, 'invalid effect token', ReceiptError)
        a = self._state['active']; _require(a is not None, 'no attempt')
        _require(event_id.kind in ('exchange', 'outcome'), 'not an effect event', ReceiptError)
        self._check_event(a, event_id, event_id.kind, event_id.slot if event_id.kind == 'exchange' else 0)
        key = (event_id.attempt, event_id.kind, event_id.slot)
        if key in self._suppressed: return None
        if event_id.kind == 'exchange':
            _require(1 <= event_id.slot <= len(a['exchanges']), 'exchange not committed')
            if a['exchanges'][event_id.slot - 1]['effect_consumed']: return None
            if a['phase'] != Phase.FEEDBACK_PENDING or event_id.slot != a['cursor']: return None
        else:
            _require(a['ko_committed'], 'KO not committed')
            if a['ko_consumed'] or a['reason'] == 'yield': return None
            if a['phase'] != Phase.RESULT_PENDING or self._state['presentation']['cursor'] != 0: return None
        def change(s):
            b = s['active']
            if event_id.kind == 'exchange': b['exchanges'][event_id.slot - 1]['effect_consumed'] = True
            else: b['ko_consumed'] = True
        self._transaction(change)
        if event_id.kind == 'exchange':
            x = a['exchanges'][event_id.slot - 1]
            return {'event_id':event_id, 'kind':'non_contact_wince', 'loser':'opponent' if x['correct'] else 'jackie'}
        return {'event_id':event_id, 'kind':'standing_social_ko', 'record_id':a['encounter'] + ('.KO.OPPONENT' if a['winner'] == 'jackie' else '.KO.JACKIE')}

    def lifecycle(self, action):
        _require(action in ('skip','mute','pause','menu','save','load','room_change','new_speech'), 'unknown lifecycle action')
        with self._lock:
            _require(not self._busy, 'reentrant lifecycle change', ReentrancyError)
            a = self._state['active']
            if a:
                self._suppressed = {(a['serial'], 'exchange', x['slot']) for x in a['exchanges']}
                if a['ko_committed']: self._suppressed.add((a['serial'], 'outcome', 0))
            else: self._suppressed.clear()
        # Text and logical state are deliberately untouched. Hosts clear PCM/poses.

    def _encode(self, state):
        payload = {'schema':SCHEMA, 'catalog':self.catalog.fingerprint, 'state':state}
        return _canonical({'payload':payload, 'sha256':hashlib.sha256(_canonical(payload)).hexdigest()})
    def save(self):
        with self._lock:
            _require(not self._busy and not self._uncertain, 'cannot save during unresolved transaction', ReentrancyError)
            self.validate()
            self.lifecycle('save')
            return self._encode(self._state)
    def save_file(self, path):
        atomic_write(Path(path), self.save())
    @classmethod
    def load(cls, blob, catalog=None, *, owner_generation, persist=None):
        model = cls(catalog, owner_generation=owner_generation, persist=persist)
        model._state = model._decode(blob)
        model.lifecycle('load')
        return model
    @classmethod
    def load_file(cls, path, catalog=None, *, owner_generation, persist=None):
        with Path(path).open('rb') as f: blob = f.read(MAX_SAVE_BYTES + 1)
        return cls.load(blob, catalog, owner_generation=owner_generation, persist=persist)
    def restore(self, blob, *, owner_generation):
        _require(_integer(owner_generation, 1), 'invalid restore ownership generation')
        with self._lock:
            _require(not self._busy, 'reentrant restore', ReentrancyError)
            # A queued restore may become stale while waiting for this lock.
            _require(owner_generation > self.owner_generation, 'restore requires a new host ownership generation')
            candidate = self._decode(blob)
            # This is an exact timeline replacement, never a union of earned wins.
            self._state = candidate
            self.owner_generation = owner_generation
            self._uncertain = False
            self._suppressed.clear()
            self.lifecycle('load')
    def _decode(self, blob):
        _require(type(blob) is bytes and len(blob) <= MAX_SAVE_BYTES, 'invalid save size/type', CorruptSave)
        def no_dupes(pairs):
            out = {}
            for key, value in pairs:
                _require(key not in out, 'duplicate JSON key', CorruptSave)
                out[key] = value
            return out
        try:
            env = json.loads(blob.decode('utf-8'), object_pairs_hook=no_dupes, parse_constant=lambda _: (_ for _ in ()).throw(CorruptSave('nonfinite JSON')))
            _require(type(env) is dict and set(env) == {'payload','sha256'}, 'invalid envelope', CorruptSave)
            p = env['payload']
            _require(type(p) is dict and set(p) == {'schema','catalog','state'}, 'invalid payload', CorruptSave)
            _require(type(p['schema']) is int and p['schema'] == SCHEMA and p['catalog'] == self.catalog.fingerprint, 'incompatible schema/catalog', CorruptSave)
            _require(type(env['sha256']) is str and env['sha256'] == hashlib.sha256(_canonical(p)).hexdigest(), 'checksum mismatch', CorruptSave)
            self._validate(p['state'])
            return p['state']
        except CorruptSave: raise
        except (ValueError, TypeError, KeyError, IndexError, RecursionError, OverflowError) as exc: raise CorruptSave('invalid save structure') from exc
    def validate(self):
        with self._lock: self._validate(self._state)
        return True

    def _validate(self, s):
        """Semantic validation is independent of the save checksum."""
        def check(value, message): _require(value, message, CorruptSave)
        def keys(value, expected): check(type(value) is dict and set(value) == set(expected.split()), 'unexpected state fields')
        keys(s, 'revision attempt_serial presentation_serial introduced knowledge history active presentation')
        check(all(_integer(s[k]) for k in ('revision','attempt_serial','presentation_serial')), 'invalid serial')
        check(s['attempt_serial'] <= s['revision'] and s['presentation_serial'] <= s['revision'], 'serial exceeds revision')
        check(type(s['introduced']) is list and s['introduced'] == sorted(set(s['introduced'])) and set(s['introduced']) <= set(ENCOUNTERS), 'invalid introduced encounters')
        check(type(s['knowledge']) is dict and set(s['knowledge']) == set(self.catalog.pairs), 'invalid knowledge pool')
        for k in s['knowledge'].values():
            keys(k, 'setup reply'); check(all(type(v) is bool for v in k.values()), 'invalid learning bit')
        check(type(s['history']) is dict and set(s['history']) == set(ENCOUNTERS), 'invalid history')
        completed = 0
        for e, h in s['history'].items():
            keys(h, 'completed wins latest_winner concession_record last_outcome')
            check(_integer(h['completed']) and _integer(h['wins']) and h['wins'] <= h['completed'], 'invalid result counts')
            completed += h['completed']
            if not h['completed']: check(h['wins'] == 0 and h['latest_winner'] is None and h['concession_record'] is None and h['last_outcome'] is None, 'empty history has outcome')
            else:
                check(e in s['introduced'] and h['latest_winner'] in ('jackie','opponent'), 'invalid winner')
                # Every completed attempt required the full eligible repertoire.
                # Learning cannot disappear later in the same retained history,
                # even after a loss/yield or while a lower-tier rematch is active.
                check(all(all(s['knowledge'][pair].values()) for pair in self.catalog.eligible(e)), 'completed encounter repertoire not retained')
                check(h['latest_winner'] != 'jackie' or h['wins'] > 0, 'unlatched win')
                check(h['latest_winner'] != 'opponent' or h['wins'] < h['completed'], 'loss missing from counts')
                check(h['concession_record'] == e + ('.WIN' if h['latest_winner'] == 'jackie' else '.LOSS'), 'wrong concession')
                check(_integer(h['last_outcome'], 1, s['attempt_serial']), 'invalid outcome serial')
        check(completed <= s['attempt_serial'], 'too many results')
        serials = [h['last_outcome'] for h in s['history'].values() if h['last_outcome'] is not None]
        check(len(serials) == len(set(serials)), 'reused outcome serial')
        # All results for each encounter must fit by its last outcome serial.
        # Check cumulative deadlines too: individually plausible counts can
        # collectively claim more completed attempts than a prefix contains.
        prefix_completed = 0
        for history in sorted((h for h in s['history'].values() if h['completed']), key=lambda h: h['last_outcome']):
            prefix_completed += history['completed']
            check(prefix_completed <= history['last_outcome'], 'impossible result history chronology')
        a = s['active']; p = s['presentation']
        if a is None: check(s['attempt_serial'] == 0 and completed == 0, 'missing active history')
        else:
            keys(a, 'serial encounter phase seed deck cursor jackie opponent pending_response exchange_slot winner reason exchanges ko_committed ko_consumed result_presented had_prior_win')
            check(_integer(a['serial'], 1) and a['serial'] == s['attempt_serial'], 'active serial mismatch')
            check(a['encounter'] in s['introduced'], 'active encounter not introduced')
            check(_integer(a['phase'], 1, 8), 'invalid phase')
            phase = Phase(a['phase'])
            check(_integer(a['seed'], 0, 65535), 'invalid seed')
            check(type(a['deck']) is list and tuple(a['deck']) == make_deck(a['encounter'], a['seed']), 'deck/seed mismatch')
            check(len(a['deck']) == len(set(a['deck'])) == 5, 'repeated deck pair')
            check(all(all(s['knowledge'][pair].values()) for pair in self.catalog.eligible(a['encounter'])), 'active pool not fully learned')
            check(_integer(a['cursor'], 0, 5) and type(a['exchanges']) is list and len(a['exchanges']) == a['cursor'], 'invalid cursor')
            check(_integer(a['jackie'], 0, 3) and _integer(a['opponent'], 0, 3), 'invalid composure')
            check(all(type(a[k]) is bool for k in ('ko_committed','ko_consumed','result_presented','had_prior_win')), 'invalid state bit')
            j = o = 3
            for i, x in enumerate(a['exchanges'], 1):
                keys(x, 'slot pair response correct effect_consumed')
                check(j > 0 and o > 0, 'scored beyond KO')
                check(type(x['slot']) is int and x['slot'] == i and x['pair'] == a['deck'][i - 1], 'exchange identity mismatch')
                check(type(x['correct']) is bool and type(x['effect_consumed']) is bool, 'invalid exchange bit')
                check(x['response'] == YIELD_EXCHANGE or x['response'] in [self.catalog.pairs[q].retort_id for q in s['knowledge'] if s['knowledge'][q]['reply']], 'unlearned committed response')
                check(x['correct'] == (x['response'] in self.catalog.pairs[x['pair']].accepted_response_ids), 'incorrect score')
                if x['correct']: o -= 1
                else: j -= 1
            check((j, o) == (a['jackie'], a['opponent']), 'composure differs from committed exchanges')
            check(a['winner'] in (None,'jackie','opponent') and a['reason'] in (None,'zero','yield'), 'invalid result')
            if min(j,o) == 0:
                check(a['winner'] == ('jackie' if o == 0 else 'opponent') and a['reason'] == 'zero', 'zero has wrong outcome')
            elif a['winner'] is not None:
                check(a['winner'] == 'opponent' and a['reason'] == 'yield', 'nonzero outcome is not explicit yield')
            else: check(a['reason'] is None, 'reason without winner')
            check((a['winner'] is not None) == (phase in (Phase.KO_PENDING, Phase.RESULT_PENDING, Phase.DONE) or phase == Phase.FEEDBACK_PENDING and min(j,o)==0), 'phase/result mismatch')
            check(a['ko_committed'] == (phase in (Phase.RESULT_PENDING, Phase.DONE)), 'result commit mismatch')
            check(not a['ko_consumed'] or a['ko_committed'] and a['reason']=='zero', 'invalid KO effect consumption')
            check(a['result_presented'] == (phase == Phase.DONE), 'result presentation mismatch')
            check(_integer(a['exchange_slot'], 0, 5), 'invalid exchange slot')
            if phase in (Phase.SETUP_PENDING, Phase.CHOICE, Phase.RESPONSE_PENDING):
                check(a['cursor'] < 5 and a['exchange_slot'] == a['cursor'] + 1, 'pending exchange slot mismatch')
            elif a['reason'] == 'yield': check(a['exchange_slot'] in (a['cursor'], a['cursor']+1), 'yield slot mismatch')
            else: check(a['exchange_slot'] == a['cursor'], 'committed slot mismatch')
            if phase == Phase.RESPONSE_PENDING:
                check(a['pending_response'] == YIELD_EXCHANGE or a['pending_response'] in [self.catalog.pairs[q].retort_id for q in s['knowledge'] if s['knowledge'][q]['reply']], 'invalid pending response')
            else: check(a['pending_response'] is None, 'response outside choice phase')
            check(completed == a['serial'] - (0 if a['ko_committed'] else 1), 'unaccounted attempt')
            h = s['history'][a['encounter']]
            previous_wins = h['wins'] - (1 if a['ko_committed'] and a['winner']=='jackie' else 0)
            check(a['had_prior_win'] == bool(previous_wins), 'previous-win history mismatch')
            if a['ko_committed']:
                check(h['last_outcome'] == a['serial'] and h['latest_winner'] == a['winner'], 'committed history mismatch')
            else: check(all(v is None or v < a['serial'] for v in serials), 'uncommitted result in history')
        if p is None:
            check(a is None or a['phase'] not in (Phase.SETUP_PENDING, Phase.FEEDBACK_PENDING, Phase.RESULT_PENDING), 'missing text presentation')
        else:
            keys(p, 'serial purpose source pair items cursor')
            check(_integer(p['serial'], 1) and p['serial'] == s['presentation_serial'], 'invalid text serial')
            check(p['purpose'] in ('entry','lesson','setup','feedback','result'), 'invalid presentation purpose')
            check(type(p['items']) is list and len(p['items']) > 0 and _integer(p['cursor'], 0, len(p['items'])-1), 'invalid text cursor')
            expected = []
            if p['purpose'] in ('entry','lesson'):
                check(a is None or a['phase'] == Phase.DONE, 'practice/entry during scored play')
                if p['purpose'] == 'entry':
                    check(p['source'] in s['introduced'] and p['pair'] is None, 'bad entry')
                    expected = self.catalog.items(p['source']+'.ENTRY', encounter_id=p['source'])
                else:
                    check(p['pair'] in self.catalog.pairs, 'unknown lesson')
                    if p['source'] in ENCOUNTERS:
                        check(p['source'] in s['introduced'] and p['pair'] in self.catalog.eligible(p['source']), 'ineligible lesson source')
                    else:
                        check(p['source'] in ('P02','P06','P11_SAFE','P12_P13') and self.catalog.pairs[p['pair']].tier == {'P02':'A','P06':'B','P11_SAFE':'C','P12_P13':'D'}[p['source']], 'invalid external lesson')
                    ids = [x['record'] for x in p['items']]
                    allowed = [p['pair']+'.'+t for t in ('SETUP','REPLY','RECAP')]
                    check(ids == allowed or len(ids)==1 and ids[0] in allowed, 'invalid lesson sequence')
                    for rid in ids: expected += self.catalog.items(rid, encounter_id=p['source'] if p['source'] in ENCOUNTERS else None)
            else:
                check(a is not None and p['source'] == a['encounter'] and p['pair'] is None, 'active presentation source mismatch')
                kind_phase = {'setup':Phase.SETUP_PENDING, 'feedback':Phase.FEEDBACK_PENDING, 'result':Phase.RESULT_PENDING}
                check(a['phase'] == kind_phase[p['purpose']], 'text/phase mismatch')
                if p['purpose'] == 'setup': ids = [a['deck'][a['cursor']]+'.SETUP']
                elif p['purpose'] == 'feedback':
                    check(a['cursor'] > 0, 'feedback without exchange')
                    x = a['exchanges'][-1]
                    rid = 'VC.RESULT.HIT_OPPONENT' if x['correct'] else ('VC.RESULT.YIELD_EXCHANGE' if x['response']==YIELD_EXCHANGE else 'VC.RESULT.HIT_JACKIE')
                    ids = ([] if x['response']==YIELD_EXCHANGE else [x['response']]) + [rid]
                else:
                    rid = 'VC.RESULT.YIELD_CONTEST' if a['reason']=='yield' else ('VC.RESULT.WIN' if a['winner']=='jackie' else 'VC.RESULT.LOSS')
                    ids = [rid, a['encounter']+('.WIN' if a['winner']=='jackie' else '.LOSS')]
                    if a['winner']=='opponent' and a['had_prior_win']: ids.append('VC.RESULT.EARLIER_WIN')
                for rid in ids: expected += self.catalog.items(rid, encounter_id=a['encounter'])
            check(p['items'] == expected, 'canonical presentation binding changed')
            # Earlier displayed lesson halves must already be in knowledge.
            if p['purpose']=='lesson':
                for item in p['items'][:p['cursor']]:
                    half = item['record'].rsplit('.',1)[1].lower()
                    if half in ('setup','reply'): check(s['knowledge'][p['pair']][half], 'displayed lesson not learned')


def atomic_write(path: Path, blob: bytes):
    """Atomic replacement; pre-replace failure leaves previous file intact.

    A directory-fsync failure after replacement has uncertain crash durability;
    callers must fail closed and reload the authoritative file, not retry effects.
    """
    path = Path(path)
    _require(type(blob) is bytes and len(blob) <= MAX_SAVE_BYTES, 'invalid persistence payload')
    temp = None
    replaced = False
    try:
        fd, temp = tempfile.mkstemp(prefix='.'+path.name+'.', suffix='.tmp', dir=path.parent)
        with os.fdopen(fd, 'wb') as file:
            file.write(blob); file.flush(); os.fsync(file.fileno())
        os.replace(temp, path)
        replaced = True
        d = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try: os.fsync(d)
        finally: os.close(d)
    except OSError as exc:
        if replaced: raise DurabilityUncertain('file replaced but directory durability not confirmed') from exc
        raise
    finally:
        if temp and os.path.exists(temp): os.unlink(temp)
