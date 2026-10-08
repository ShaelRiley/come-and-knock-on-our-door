"""NEW narrow interface bridge over a frozen, current-canonical contest owner.

No result grants. The missing historical contest implementation is not recovered.
SceneContext's original exact-type/progress interface is preserved by this wrapper.
A DONE attempt is no longer active for scene gating; rematches remain owner-owned.
"""
from dataclasses import dataclass
from types import MappingProxyType
from dependencies.vc_owner.verbal_contest import (
    VerbalContests as Owner, Catalog, Phase, ENCOUNTERS, YIELD_EXCHANGE)

@dataclass(frozen=True)
class Progress:
    resolved: bool
    won: bool

class VerbalContests(Owner):
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
