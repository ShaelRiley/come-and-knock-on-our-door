"""NEW atomic reference host protocol. This is not a future P13 implementation.

The actual host must implement a no-input/no-save critical section, validate all
physical changes and exact output routes first, then publish both atomically.
A queue that can partially publish and fail does not implement this protocol.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import asdict, dataclass
from threading import RLock
from typing import Protocol
from .p07_model import (COURTYARD, KITCHEN, OwnedObject, P07Context, P07Result,
                        P07World, Projection, canonical_record, canonical_unit)


@dataclass(frozen=True)
class Transaction:
    before_save: dict
    after_save: dict
    before_projection: Projection
    after_projection: Projection
    output: P07Result


class TransactionHost(Protocol):
    def prepare(self, transaction: Transaction) -> object: ...
    def commit(self, prepared: object) -> None: ...


class HostPreparationError(RuntimeError):
    pass


@dataclass(frozen=True)
class RenderedRecord:
    record_id: str
    unit_ids: tuple[str, ...]
    texts: tuple[str, ...]


def render_exact(result: P07Result) -> tuple[RenderedRecord, ...]:
    """Honor unit-level slices. Never expand the onion slice into sincerity."""
    rendered = []
    for rid in result.record_ids:
        selected = tuple(uid for uid in result.speech_unit_ids if canonical_unit(uid)['record_id'] == rid)
        if selected:
            texts = tuple(canonical_unit(uid)['text'] for uid in selected)
        else:
            text = canonical_record(rid)['text']
            if type(text) is not str:
                raise HostPreparationError('A structured scene requires explicit exact unit IDs')
            texts = (text,)
        rendered.append(RenderedRecord(rid, selected, texts))
    if any(not any(uid in row.unit_ids for row in rendered) for uid in result.speech_unit_ids):
        raise HostPreparationError('Orphaned speech unit')
    return tuple(rendered)


@dataclass(frozen=True)
class Prepared:
    expected_integrity: str
    domain: dict
    projection: Projection
    output: P07Result
    rendered: tuple[RenderedRecord, ...]
    owner: OwnedObject
    publication_count: int
    food_ready_grants: int
    laugh_grants: int
    handoffs: int


class MemoryTransactionHost:
    """Reference atomic memory replacement, failure knobs and independent owner.

    Only the latest output batch is retained: no unbounded pending queue. This
    fixture proves protocol behavior, not an actual renderer or SCI host.
    """
    def __init__(self, world: P07World, context: P07Context):
        self._lock = RLock()
        self.domain = world.save()
        self.physical = world.projection(context)
        handed_off = bool(self.domain['state']['handoff'])
        self.owner = OwnedObject('hotpot_pot', 'P13' if handed_off else 'P07', COURTYARD if handed_off else KITCHEN)
        self.output = None
        self.rendered = ()
        self.publication_count = 0
        self.food_ready_grants = int(bool(self.domain['state']['receipts']['complete']))
        self.laugh_grants = int(bool(self.domain['state']['receipts']['laugh']))
        self.handoffs = int(handed_off)
        self.output_capacity = 8
        self.fail_prepare = False
        self.fail_commit = False

    def snapshot(self):
        with self._lock:
            return deepcopy({'domain': self.domain, 'physical': self.physical, 'owner': self.owner,
                             'output': self.output, 'rendered': self.rendered,
                             'publication_count': self.publication_count,
                             'food_ready_grants': self.food_ready_grants,
                             'laugh_grants': self.laugh_grants, 'handoffs': self.handoffs})

    def prepare(self, transaction):
        with self._lock:
            if type(transaction) is not Transaction or self.fail_prepare:
                raise HostPreparationError('Host preparation failed')
            if transaction.before_save != self.domain or transaction.before_projection != self.physical:
                raise HostPreparationError('Host/domain snapshots disagree')
            if len(transaction.output.record_ids) > self.output_capacity:
                raise HostPreparationError('Exact output capacity unavailable')
            rendered = render_exact(transaction.output)
            candidate = P07World.load(transaction.after_save)
            state = candidate.state
            before = transaction.before_save['state']
            expected_owner = OwnedObject('hotpot_pot', 'P13' if before['handoff'] else 'P07',
                                         COURTYARD if before['handoff'] else KITCHEN)
            if self.owner != expected_owner:
                raise HostPreparationError('The exact existing pot is not at its prior owner')
            owner = self.owner
            handoffs = self.handoffs
            if state['handoff'] and not before['handoff']:
                if self.handoffs or not before['receipts']['complete']:
                    raise HostPreparationError('No second pot or duplicate handoff')
                owner = OwnedObject('hotpot_pot', 'P13', COURTYARD)
                handoffs += 1
            food = self.food_ready_grants + sum(e.id == 'FOOD_READY' for e in transaction.output.events)
            laugh = self.laugh_grants + sum(e.id == 'LAF07' for e in transaction.output.events)
            if food > 1 or laugh > 1:
                raise HostPreparationError('Duplicate logical grant')
            return Prepared(self.domain['integrity_sha256'], deepcopy(transaction.after_save),
                            transaction.after_projection, transaction.output, rendered, owner,
                            self.publication_count + 1, food, laugh, handoffs)

    def commit(self, prepared):
        with self._lock:
            if type(prepared) is not Prepared or self.fail_commit:
                raise HostPreparationError('Host commit failed before mutation')
            if prepared.expected_integrity != self.domain['integrity_sha256']:
                raise HostPreparationError('Concurrent host transaction won the compare-and-swap')
            domain = deepcopy(prepared.domain)
            # All possible copying/failure is above the replacement.
            (self.domain, self.physical, self.output, self.rendered, self.owner,
             self.publication_count, self.food_ready_grants, self.laugh_grants, self.handoffs) = (
                domain, prepared.projection, prepared.output, prepared.rendered, prepared.owner,
                prepared.publication_count, prepared.food_ready_grants, prepared.laugh_grants, prepared.handoffs)

    def ownership_context(self):
        with self._lock:
            return (self.owner,)

    def save_campaign_fixture(self):
        """Save persistent state only; presentation and old leases never survive."""
        with self._lock:
            return {'schema': 'p07-memory-host-fixture-1', 'domain': deepcopy(self.domain),
                    'owner': asdict(self.owner)}

    @classmethod
    def load_campaign_fixture(cls, saved, context):
        if type(saved) is not dict or set(saved) != {'schema', 'domain', 'owner'} or saved['schema'] != 'p07-memory-host-fixture-1':
            raise ValueError('Malformed composition fixture')
        if type(saved['owner']) is not dict or set(saved['owner']) != {'object_id', 'owner', 'room'}:
            raise ValueError('Malformed owner')
        from dataclasses import replace
        context = replace(context, ownership=(OwnedObject(**saved['owner']),))
        world = P07World.load(saved['domain'], context)
        return world, cls(world, context)
