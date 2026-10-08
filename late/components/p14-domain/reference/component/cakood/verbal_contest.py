"""NEW narrow interface bridge over a frozen, current-canonical contest owner.

No result grants. The missing historical contest implementation is not recovered.
SceneContext's original exact-type/progress interface is preserved by this wrapper.
A DONE attempt is no longer active for scene gating; rematches remain owner-owned.
"""
from dataclasses import dataclass
from types import MappingProxyType
from dependencies.vc_owner.verbal_contest import (
    VerbalContests as Owner, Catalog, Phase, ENCOUNTERS, YIELD_EXCHANGE, ReentrancyError)

@dataclass(frozen=True)
class Progress:
    resolved: bool
    won: bool

class VerbalContests(Owner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .contest_evidence import initialize
        initialize(self)

    @property
    def progress(self):
        self.validate()
        flags = self.flags
        return MappingProxyType({e: Progress(e+'_RESOLVED' in flags, e+'_WON' in flags)
                                 for e in ENCOUNTERS})

    @property
    def active(self):
        attempt = super().active
        return None if attempt is not None and attempt.phase == Phase.DONE else attempt

    # Revision 2: serialize outcome observation and its owner-held witness with
    # the accepted transaction using the same reentrant lock and failure policy.
    def _transaction(self, operation):
        if not self._lock.acquire(blocking=False):
            raise ReentrancyError('concurrent mutation')
        try:
            from .contest_evidence import check_binding, capture
            check_binding(self)
            result = super()._transaction(operation)
            capture(self)
            return result
        finally:
            self._lock.release()

    @property
    def attempts(self):
        from .contest_evidence import attempts
        return attempts(self)

    @classmethod
    def load(cls, blob, catalog=None, *, owner_generation, persist=None):
        owner = super().load(blob, catalog, owner_generation=owner_generation, persist=persist)
        from .contest_evidence import detach
        detach(owner)
        return owner

    def restore(self, blob, *, owner_generation):
        from .contest_evidence import detach
        with self._lock:
            super().restore(blob, owner_generation=owner_generation)
            detach(self)

    def save_with_evidence(self):
        from .contest_evidence import save
        return save(self)

    @classmethod
    def load_with_evidence(cls, data, *, owner_generation):
        from .contest_evidence import load
        return load(cls, data, owner_generation=owner_generation)

    def restore_with_evidence(self, data, *, owner_generation):
        # Validate the whole pair before replacing any live owner state. Use the
        # accepted raw restore to retain epoch/effect suppression semantics.
        candidate = type(self).load_with_evidence(data, owner_generation=owner_generation)
        raw = candidate.save()
        with self._lock:
            super().restore(raw, owner_generation=owner_generation)
            self._reference_commit_witness = candidate._reference_commit_witness
            self._observed_results = candidate._observed_results

    def save_with_evidence_file(self, path):
        from .contest_evidence import save_file
        save_file(self, path)

    @classmethod
    def load_with_evidence_file(cls, path, *, owner_generation):
        from .contest_evidence import load_file
        return load_file(cls, path, owner_generation=owner_generation)
