"""NEW executable host protocol, not a native renderer/save implementation.

Use genuine unchanged VerbalContests. The host's critical section includes
complete output preparation, owner replacement, and model publish. A native
host must independently prove atomicity/durability and callback retirement.
"""
from __future__ import annotations
from dataclasses import dataclass, field, replace
from copy import deepcopy
from typing import Protocol
import hashlib
from pathlib import Path
import sys
import threading
from .p06_model import (P06World, P06Context, P06Result, OwnedObject, PORCH, COURTYARD,
                        BusyError, StateError, canonical_record, canonical_units, _Leases)
from .verbal_contest import VerbalContests, Phase

LOAN_RECORDS = ('P06.SUCCESS.006', 'P06.SYSTEM.002')
LOAN_OBJECTS = (OwnedObject('completed_screen', 'P06', COURTYARD),)

class HostPreparationError(RuntimeError):
    """Host guarantees no mutation occurred."""

class HostCommitUncertain(RuntimeError):
    """Never retry blindly: load authoritative composed state first."""

class TransactionHost(Protocol):
    def prepare(self, records: tuple[str, ...], objects: tuple[OwnedObject, ...]) -> object: ...
    def commit(self, prepared: object) -> None: ...


def context_with_contest(context: P06Context, contests: VerbalContests) -> P06Context:
    """Read actual Contest state; refuse externally fabricated social flags."""
    if type(context) is not P06Context or type(contests) is not VerbalContests:
        raise StateError('Exact P06/accepted Contest types required')
    with contests._lock:
        contests.validate()
        actual = contests.flags
        claimed = frozenset(x for x in context.flags if x.startswith('VC0') or x == 'ALL_VC_WON')
        if not claimed <= actual: raise StateError('Campaign social flags disagree with actual Contest')
        active = contests.active
        busy = bool(contests.pending_text() or active and active.phase != Phase.DONE)
        return replace(context, flags=context.flags | actual, contest_active=busy,
                       result_pending=contests.result_presentation_pending)


def borrow_screen_synchronously(world: P06World, context: P06Context,
                                 contests: VerbalContests, host: TransactionHost) -> P06Result:
    """One player loan choice, one complete-screen projection, exact output once.

    During this critical section no input, save, restore or contest mutation may
    run. Readers see old committed state. Both locks are nonblocking to avoid
    deadlock. Private Contest guard use is pinned to the bundled accepted source.
    """
    if type(world) is not P06World or type(contests) is not VerbalContests:
        raise StateError('Exact reference owner types required')
    if not world._lock.acquire(blocking=False): raise BusyError('Concurrent P06 transaction')
    locked_contest = False
    guarded = False
    try:
        world._ensure_live()
        if world._busy or world._uncertain: raise BusyError('P06 owner unavailable')
        locked_contest = contests._lock.acquire(blocking=False)
        if not locked_contest or contests._busy or contests._uncertain:
            raise BusyError('Contest owner unavailable')
        context = context_with_contest(context, contests)
        candidate = P06World.load(world.save(), context)
        request = candidate.borrow_screen(context)
        if request.code != 'loan_pending': return request
        complete = candidate.acknowledge_handoff(context, request.token, LOAN_OBJECTS)
        if complete.code != 'screen_ready': return complete
        candidate.validate(replace(context, ownership=LOAN_OBJECTS))
        # Resolve all exact output and construct result before any host mutation.
        result = P06Result(code='screen_ready', line_ids=LOAN_RECORDS,
            speech_unit_ids=tuple(u for r in LOAN_RECORDS for u in canonical_units(r)),
            events=request.events + complete.events)
        world._busy = True
        contests._busy = True
        guarded = True
        prepared = host.prepare(LOAN_RECORDS, LOAN_OBJECTS)
        try:
            host.commit(prepared)
        except HostPreparationError:
            raise
        except BaseException:
            world._uncertain = True
            raise
        # In-memory publish only: no callback, I/O or further fallible operation.
        world._state, world._lease = candidate._state, candidate._lease
        return result
    finally:
        if guarded:
            contests._busy = False
            world._busy = False
        if locked_contest: contests._lock.release()
        world._lock.release()


@dataclass
class MemoryTransactionHost:
    """Reference-only atomic host; the owner map is entitlement, not render state."""
    owners: dict = field(default_factory=lambda: {'completed_screen': {'owner': 'P06', 'room': PORCH}})
    presented: list = field(default_factory=list)
    queue_capacity: int = 2
    fail_prepare: bool = False
    fail_commit: bool = False
    loan_commits: int = 0

    def prepare(self, records, objects):
        if self.fail_prepare or self.queue_capacity < len(records): raise HostPreparationError('Exact output cannot be committed')
        if records != LOAN_RECORDS or objects != LOAN_OBJECTS: raise HostPreparationError('Wrong loan transaction')
        if self.owners != {'completed_screen': {'owner': 'P06', 'room': PORCH}} or self.loan_commits:
            raise HostPreparationError('Original screen is not owned exactly once')
        for record in records: canonical_record(record)
        return {'owners': {'completed_screen': {'owner': 'P06', 'room': COURTYARD}},
                'presented': [*self.presented, *records], 'loan_commits': 1}

    def commit(self, prepared):
        if self.fail_commit: raise HostPreparationError('Definitive unchanged simulated failure')
        owners = deepcopy(prepared['owners'])
        presented, commits = list(prepared['presented']), prepared['loan_commits']
        self.owners, self.presented, self.loan_commits = owners, presented, commits

    def bind_p08(self, world, context):
        """Admit a genuine live/restored P08 owner and retire the prior binding.

        The campaign supplies its authoritative replacement instance after restore.
        This never moves an object or acknowledges a placement by itself.
        """
        _check_p08_source(world, context)
        world.validate(); world.validate_context(context)
        _check_screen_reconciliation(self, world)
        binding = _P08Binding(world, context, _Leases.acquire())
        previous = getattr(self, '_p08_binding', None)
        if previous is not None:
            with previous.lock:
                if previous.busy: raise HostPreparationError('P08 reconciliation is busy')
                previous.retired = True
        self._p08_binding = binding

    def pending_p08_screen_claim(self):
        """Issue an unsaved ticket for the bound live owner's exact pending claim."""
        binding = getattr(self, '_p08_binding', None)
        if binding is None or binding.retired: raise HostPreparationError('Live P08 binding required')
        with binding.lock:
            if binding.busy: raise HostPreparationError('P08 reconciliation is busy')
            binding.world.validate(); binding.world.validate_context(binding.context)
            _check_screen_reconciliation(self, binding.world)
            claim = _screen_claim(binding.world)
            return P08ScreenClaim(binding.lease, claim['serial'], binding.world.revision) if claim else None

    def apply_p08_handoff(self, ticket):
        """Atomically reconcile actual live P08 placement, current owner, and ACK.

        Dictionary-only calls are rejected. Direct P08 input must be serialized by
        the campaign throughout this no-callback critical section. Native durable
        joint publication remains an explicit host obligation, not proved here.
        """
        binding = getattr(self, '_p08_binding', None)
        if (type(ticket) is not P08ScreenClaim or any(type(x) is not int for x in
                (ticket.lease, ticket.serial, ticket.revision)) or binding is None or binding.retired
                or ticket.lease != binding.lease):
            raise HostPreparationError('Exact live P08 receipt ticket required')
        if not binding.lock.acquire(blocking=False): raise HostPreparationError('Concurrent P08 handoff')
        try:
            if binding.busy: raise HostPreparationError('Reentrant P08 handoff')
            binding.busy = True
            world = binding.world
            world.validate(); world.validate_context(binding.context)
            _check_screen_reconciliation(self, world)
            if ticket == binding.completed_ticket:
                return False
            claim = _screen_claim(world)
            if (claim is None or ticket.serial != claim['serial'] or ticket.revision != world.revision):
                raise HostPreparationError('Stale or mismatched P08 pending placement')
            before = world.save()
            candidate = type(world).load(before, binding.context)
            result = candidate.acknowledge_handoff(claim['handoff_id'], claim['serial'])
            if result.code != 'handoff_acknowledged': raise HostPreparationError('P08 did not accept exact pending claim')
            candidate.validate(); candidate.validate_context(binding.context)
            staged_state = deepcopy(candidate.__dict__)
            staged_owners = {'completed_screen': {'owner': 'P08', 'room': COURTYARD}}
            changed = self.owners != staged_owners
            if self.fail_prepare or self.fail_commit:
                raise HostPreparationError('Definitive unchanged P08 reconciliation failure')
            # No callback/I/O follows. Detect any illicit intervening mutation before
            # the synchronous joint in-memory publish; campaign serialization still
            # governs P08, whose retained implementation has no intrinsic lock.
            if world.save() != before: raise HostPreparationError('P08 changed during handoff preparation')
            world.__dict__, self.owners, binding.completed_ticket = staged_state, staged_owners, ticket
            return changed
        finally:
            binding.busy = False
            binding.lock.release()

    def ownership_context(self):
        return tuple(OwnedObject(o, d['owner'], d['room']) for o, d in sorted(self.owners.items()))


@dataclass(frozen=True)
class P08ScreenClaim:
    lease: int
    serial: int
    revision: int


@dataclass
class _P08Binding:
    world: object
    context: object
    lease: int
    completed_ticket: P08ScreenClaim | None = None
    retired: bool = False
    busy: bool = False
    lock: object = field(default_factory=threading.RLock)


def _check_p08_source(world, context):
    module = sys.modules.get(type(world).__module__)
    expected = Path(__file__).resolve().parents[1] / 'tests/fixtures/p08_model.py'
    source = Path(getattr(module, '__file__', ''))
    if (module is None or getattr(module, 'P08World', None) is not type(world)
            or getattr(module, 'P08Context', None) is not type(context) or not source.is_file()
            or hashlib.sha256(source.read_bytes()).digest() != hashlib.sha256(expected.read_bytes()).digest()):
        raise HostPreparationError('Unchanged retained P08 implementation and context required')


def _screen_claim(world):
    claims = [x for x in world.pending_handoffs if x['object_id'] == 'completed_screen']
    if len(claims) > 1: raise HostPreparationError('Duplicate P08 screen claim')
    if not claims: return None
    claim = claims[0]
    expected = {'handoff_id': 'P08:OWN:completed_screen', 'serial': claim.get('serial'), 'object_id': 'completed_screen',
                'from_owner': 'P06', 'to_owner': 'P08', 'includes': (), 'destination': 'courtyard_layout', 'room': COURTYARD}
    if (claim != expected or type(claim['serial']) is not int or claim['serial'] <= 0
            or world.positions['completed_screen'] == 0
            or world.ownership_serials.get('completed_screen') != claim['serial']):
        raise HostPreparationError('Invalid actual P08 placement claim')
    return claim


def _check_screen_reconciliation(host, world):
    if host.loan_commits != 1 or host.owners not in (
            {'completed_screen': {'owner': 'P06', 'room': COURTYARD}},
            {'completed_screen': {'owner': 'P08', 'room': COURTYARD}}):
        raise HostPreparationError('No genuine staged screen loan to reconcile')
    position = world.positions['completed_screen']
    claimed = world.ownership_serials.get('completed_screen', 0)
    acknowledged = world.acknowledged_handoffs.get('completed_screen', 0)
    owner = host.owners['completed_screen']['owner']
    if position == 0:
        if claimed or acknowledged or owner != 'P06': raise HostPreparationError('P08 ownership without placement')
    elif not claimed:
        raise HostPreparationError('Placed screen has no claim')
    if acknowledged and owner != 'P08':
        raise HostPreparationError('Acknowledged P08 screen conflicts with authoritative owner map')
    if position and not acknowledged and _screen_claim(world) is None:
        raise HostPreparationError('Placed screen lacks pending ownership receipt')
