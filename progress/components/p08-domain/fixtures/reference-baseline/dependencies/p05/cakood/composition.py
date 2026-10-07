"""NEW reference host composition; no rendering, SCI VM, or contest simulation.

The synchronous helper owns a no-input/no-save critical section. Host.prepare
must validate exact output capacity and destinations without changing anything.
Host.commit must atomically publish the already-prepared reader records and
physical owner map, or raise while leaving both unchanged. A native host must
implement/prove those requirements; an ordinary nontransactional queue is not
this protocol. The provided in-memory host is executable protocol evidence only.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Protocol
from .p05_model import (COURTYARD, GARAGE, OwnedObject, P05Context, P05Result,
                        P05World, canonical_record)

LOAN_RECORDS = ("P05.DIALOGUE.007", "P05.SUCCESS.006")
LOAN_OBJECTS = (OwnedObject("pa_kit", "P05", COURTYARD), OwnedObject("handcart", "P05", GARAGE))


class TransactionHost(Protocol):
    def prepare(self, records: tuple[str, ...], objects: tuple[OwnedObject, ...]) -> object: ...
    def commit(self, prepared: object) -> None: ...


class HostPreparationError(RuntimeError):
    pass


def borrow_kit_synchronously(world: P05World, context: P05Context, host: TransactionHost) -> P05Result:
    """One player borrow choice; no acknowledgment UI or arbitrary visible wait.

    All fallible model work occurs on a candidate. Failure cannot mutate world.
    Call under the host's critical section; no reentrant game input/save allowed.
    Host preparation is not a source observation receipt.
    """
    candidate = P05World.load(world.save(), context)
    request = candidate.borrow_kit(context)
    if request.code != "handoff_pending":
        return request
    complete = candidate.acknowledge_handoff(context, request.token, LOAN_OBJECTS)
    if complete.code != "sound_ready":
        return complete
    candidate.validate(context)
    result = P05Result("", request.events + complete.events, "sound_ready", LOAN_RECORDS,
                       tuple(unit["line_id"] for rid in LOAN_RECORDS for unit in canonical_record(rid)["speech_units"]))
    world._transaction_active = True
    try:
        prepared = host.prepare(LOAN_RECORDS, LOAN_OBJECTS)
        host.commit(prepared)
        # No further fallible operation, callback, event dispatch or I/O in between.
        world._state = candidate._state
        world._session = candidate._session
    finally:
        world._transaction_active = False
    return result


@dataclass
class MemoryTransactionHost:
    """Test/reference host with atomic memory replacement and explicit failure knobs."""
    owners: dict = field(default_factory=lambda: {"pa_kit": {"owner": "P05", "room": GARAGE},
                                                 "handcart": {"owner": "P05", "room": GARAGE}})
    presented: list = field(default_factory=list)
    queue_capacity: int = 2
    fail_prepare: bool = False
    fail_commit: bool = False
    loan_commits: int = 0

    def prepare(self, records, objects):
        if self.fail_prepare or self.queue_capacity < len(records):
            raise HostPreparationError("Exact canonical output cannot be committed")
        if records != LOAN_RECORDS or objects != LOAN_OBJECTS:
            raise HostPreparationError("Unexpected loan transaction")
        expected = {"pa_kit": {"owner": "P05", "room": GARAGE},
                    "handcart": {"owner": "P05", "room": GARAGE}}
        if self.owners != expected or self.loan_commits:
            raise HostPreparationError("Original loan objects are not owned exactly once")
        for rid in records:
            canonical_record(rid)  # exact routes must resolve before state mutation
        return {"owners": {x.object_id: {"owner": x.owner, "room": x.room} for x in objects},
                "presented": [*self.presented, *records], "loan_commits": 1}

    def commit(self, prepared):
        if self.fail_commit:
            raise HostPreparationError("Simulated queue/host failure before commit")
        owners, presented, commits = deepcopy(prepared["owners"]), list(prepared["presented"]), prepared["loan_commits"]
        self.owners, self.presented, self.loan_commits = owners, presented, commits

    def apply_p08_handoff(self, handoff):
        """Apply retained P08's exact stable PA claim once, before its ACK."""
        if (handoff.get("handoff_id") != "P08:OWN:pa_kit" or handoff.get("object_id") != "pa_kit"
                or handoff.get("from_owner") != "P05" or handoff.get("to_owner") != "P08"
                or handoff.get("room") != COURTYARD):
            raise HostPreparationError("Unexpected P08 ownership claim")
        if self.owners.get("pa_kit") == {"owner": "P08", "room": COURTYARD}:
            return False
        if self.owners.get("pa_kit") != {"owner": "P05", "room": COURTYARD}:
            raise HostPreparationError("P05 loan is not physically staged")
        self.owners = {**self.owners, "pa_kit": {"owner": "P08", "room": COURTYARD}}
        return True

    def ownership_context(self):
        return tuple(OwnedObject(obj, data["owner"], data["room"]) for obj, data in sorted(self.owners.items()))
