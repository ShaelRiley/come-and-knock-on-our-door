"""P11 cooperative, reversible display rescue and safe VC03 entry handoff.

Working current-canon adaptation of the byte-exact recovered transcription in
historical/. See CURRENT-CONTRACT.md and provenance/working-model.diff.

P04 remains the gate authority. P11 never starts or resolves a contest, reveals
Rita's work, grants a P12 reward, or turns audio completion into physical safety.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Any, ClassVar

from .model import Verb
from .p02_model import ROOMS
from .p04_model import GateHandoff
from .p10_model import _Captioned, CaptionResult

SAVE_KIND = "cakood-p11-branch"
SAVE_SCHEMA = 1
SIDE_PASSAGE = "L04_SIDE_PASSAGE"
PORCH = "L03_PORCH"
COURTYARD = "L05_COURTYARD"
CONSERVATORY = "L07_CONSERVATORY"
PREREQUISITES = frozenset(("EVENING_STARTED", "RUMOR_CLEARED", "TERMS_CARD_AVAILABLE", "CUES_RESTORED"))
FIXED_OBJECTS = frozenset(("folded_display", "display_wing", "wing_catch", "display_handle",
    "staging_pocket", "handcart", "hold_open_peg", "side_gate", "ceramic_panel", "audience",
    "jack", "felix", "bunny", "frankie", "rita", "stringer", "milo", "vivian"))


class RescuePhase(IntEnum):
    CART = 0
    SUPPORTED = 1
    FOLDED = 2
    STAGED = 3


RECORD_UNITS = {'P11.CHOICE.001': (),
 'P11.CHOICE.002': (),
 'P11.CHOICE.003': (),
 'P11.CHOICE.004': (),
 'P11.DIALOGUE.001': ('P11.DIALOGUE.001.01',
                      'P11.DIALOGUE.001.02',
                      'P11.DIALOGUE.001.03',
                      'P11.DIALOGUE.001.04',
                      'P11.DIALOGUE.001.05'),
 'P11.DIALOGUE.002': ('P11.DIALOGUE.002.01',
                      'P11.DIALOGUE.002.02',
                      'P11.DIALOGUE.002.03',
                      'P11.DIALOGUE.002.04',
                      'P11.DIALOGUE.002.05',
                      'P11.DIALOGUE.002.06'),
 'P11.FAILURE.001': ('P11.FAILURE.001.01',),
 'P11.FAILURE.002': ('P11.FAILURE.002.01',),
 'P11.FAILURE.003': ('P11.FAILURE.003.01',),
 'P11.HINT.1': (),
 'P11.HINT.2': (),
 'P11.HINT.3': (),
 'P11.LOOK.001': ('P11.LOOK.001.01',),
 'P11.LOOK.002': ('P11.LOOK.002.01',),
 'P11.LOOK.003': ('P11.LOOK.003.01',),
 'P11.LOOK.004': ('P11.LOOK.004.01',),
 'P11.OPEN.001': ('P11.OPEN.001.01', 'P11.OPEN.001.02', 'P11.OPEN.001.03', 'P11.OPEN.001.04'),
 'P11.SUCCESS.001': ('P11.SUCCESS.001.01', 'P11.SUCCESS.001.02'),
 'P11.SUCCESS.002': ('P11.SUCCESS.002.01',),
 'P11.SUCCESS.003': ('P11.SUCCESS.003.01',),
 'P11.SUCCESS.004': ('P11.SUCCESS.004.01',),
 'P11.SUCCESS.005': ('P11.SUCCESS.005.01', 'P11.SUCCESS.005.02', 'P11.SUCCESS.005.03', 'P11.SUCCESS.005.04'),
 'P11.SUCCESS.006': ('P11.SUCCESS.006.01',),
 'VC03.ENTRY': ('VC03.ENTRY.01', 'VC03.ENTRY.02', 'VC03.ENTRY.03'),
 'VC03.NOT_READY': (),
 'VC03.REMATCH': ('VC03.REMATCH.01',)}
UNIT_SPEAKERS = {'P11.DIALOGUE.001.01': 'bunny',
 'P11.DIALOGUE.001.02': 'jack',
 'P11.DIALOGUE.001.03': 'frankie',
 'P11.DIALOGUE.001.04': 'jack',
 'P11.DIALOGUE.001.05': 'bunny',
 'P11.DIALOGUE.002.01': 'felix',
 'P11.DIALOGUE.002.02': 'jack',
 'P11.DIALOGUE.002.03': 'felix',
 'P11.DIALOGUE.002.04': 'jack',
 'P11.DIALOGUE.002.05': 'felix',
 'P11.DIALOGUE.002.06': 'jack',
 'P11.FAILURE.001.01': 'felix',
 'P11.FAILURE.002.01': 'felix',
 'P11.FAILURE.003.01': 'felix',
 'P11.LOOK.001.01': 'jack',
 'P11.LOOK.002.01': 'jack',
 'P11.LOOK.003.01': 'jack',
 'P11.LOOK.004.01': 'jack',
 'P11.OPEN.001.01': 'felix',
 'P11.OPEN.001.02': 'jack',
 'P11.OPEN.001.03': 'felix',
 'P11.OPEN.001.04': 'jack',
 'P11.SUCCESS.001.01': 'bunny',
 'P11.SUCCESS.001.02': 'jack',
 'P11.SUCCESS.002.01': 'bunny',
 'P11.SUCCESS.003.01': 'frankie',
 'P11.SUCCESS.004.01': 'felix',
 'P11.SUCCESS.005.01': 'felix',
 'P11.SUCCESS.005.02': 'jack',
 'P11.SUCCESS.005.03': 'frankie',
 'P11.SUCCESS.005.04': 'jack',
 'P11.SUCCESS.006.01': 'rita',
 'VC03.ENTRY.01': 'felix',
 'VC03.ENTRY.02': 'jack',
 'VC03.ENTRY.03': 'felix',
 'VC03.REMATCH.01': 'felix'}


@dataclass(frozen=True)
class P11Context:
    room: str
    gate: GateHandoff
    on_apron: bool = False
    flags: frozenset[str] = frozenset()
    inventory: frozenset[str] = frozenset()
    felix_room: str = SIDE_PASSAGE
    bunny_room: str = PORCH
    frankie_room: str = COURTYARD
    rita_room: str = CONSERVATORY
    cart_room: str = SIDE_PASSAGE
    display_room: str = SIDE_PASSAGE
    contest_active: bool = False

    def __post_init__(self) -> None:
        if any(type(x) is not str or x not in ROOMS for x in (
                self.room, self.felix_room, self.bunny_room, self.frankie_room,
                self.rita_room, self.cart_room, self.display_room)):
            raise ValueError("Unknown campaign room")
        if any(type(x) is not bool for x in (self.on_apron, self.contest_active)):
            raise ValueError("Campaign modes must be boolean")
        for x in (self.flags, self.inventory):
            if type(x) is not frozenset or any(type(y) is not str for y in x):
                raise ValueError("Campaign facts must be frozen string sets")
        if self.inventory & FIXED_OBJECTS:
            raise ValueError("Fixed rescue objects and people cannot be pocketed")
        g = self.gate
        if (type(g) is not GateHandoff or g.peg_id != "hold_open_peg" or g.peg_location != SIDE_PASSAGE
                or any(type(x) is not bool for x in (g.tested, g.peg_available, g.peg_engaged,
                                                    g.gate_open, g.wedge_in_gate))
                or (g.peg_available and not g.tested)
                or (g.peg_engaged and (not g.peg_available or not g.gate_open or g.wedge_in_gate))
                or (g.wedge_in_gate and not g.gate_open)):
            raise ValueError("Invalid P04 gate handoff")


P11Result = CaptionResult


@dataclass
class P11World(_Captioned):
    phase: int = int(RescuePhase.CART)
    first_lift_at: int = 0
    lift_at: int = 0
    catch_at: int = 0
    fold_at: int = 0
    stage_at: int = 0
    peg_request_at: int = 0
    peg_ack_at: int = 0
    advance_peg_at: int = 0
    contest_request_at: int = 0
    laugh_at: int = 0
    hint_level: int = 0
    PUZZLE: ClassVar[str] = "P11"
    KIND: ClassVar[str] = SAVE_KIND
    SOURCES: ClassVar[dict[str, str]] = {
        "intro": "P11.OPEN.001", "concern": "P11.DIALOGUE.001",
        "sincere": "P11.DIALOGUE.002", "wing": "P11.LOOK.001", "peg": "P11.LOOK.002",
        "catch": "P11.LOOK.003", "fold": "P11.SUCCESS.005", "staged": "P11.SUCCESS.006"}
    UNITS: ClassVar[dict[str, tuple[str, ...]]] = RECORD_UNITS
    SPEAKERS: ClassVar[dict[str, str]] = UNIT_SPEAKERS

    @property
    def supported(self) -> bool:
        return self.phase == RescuePhase.SUPPORTED

    @property
    def ready(self) -> bool:
        return self.phase == RescuePhase.STAGED

    @property
    def flags(self) -> frozenset[str]:
        return frozenset(("DISPLAY_STAGED", "HELP_ACCEPTED")) if self.ready else frozenset()

    @property
    def inventory(self) -> tuple[str, ...]:
        return ()

    @property
    def sincere_complete(self) -> bool:
        return self._complete("sincere")

    @property
    def concern_pending(self) -> bool:
        return "concern" in self.presentations and not self._complete("concern")

    @property
    def contest_eligible(self) -> bool:
        return self.ready and self.sincere_complete and not self.concern_pending

    @property
    def rescue_credit_variant(self) -> str | None:
        """Current catalog's exact predicate order; no new state or dialogue."""
        if not self.ready:
            return None
        if self.peg_ack_at:
            return "ordinary"
        if self.advance_peg_at:
            return "pre_engaged"
        return None

    @property
    def reserved_external_objects(self) -> frozenset[str]:
        return frozenset(("folded_display", "handcart")) if self.first_lift_at else frozenset()

    @property
    def display_handoff(self) -> dict[str, Any] | None:
        if not self.ready:
            return None
        return {"display_id": "folded_display", "cart_id": "handcart", "location": SIDE_PASSAGE,
                "position": "staging_pocket", "folded": True, "padded": True,
                "covered": True, "undamaged": True, "panel_revealed": False,
                "transport_owner": "P13", "rita_reveal_consent": False,
                "shared_helpers": ("jack", "felix", "bunny", "frankie")}

    @property
    def pending_peg_request_id(self) -> str | None:
        return f"P11:{self._epoch}:peg:{self.peg_request_at}" if self.peg_request_at else None

    @property
    def pending_contest_request_id(self) -> str | None:
        return f"P11:{self._epoch}:VC03:{self.contest_request_at}" if self.contest_request_at else None

    @staticmethod
    def _context(context: P11Context) -> None:
        if type(context) is not P11Context:
            raise ValueError("P11 requires campaign context")

    def _block(self, context: P11Context, *, safety_recovery: bool = False) -> CaptionResult | None:
        self._context(context)
        if safety_recovery:
            return None
        if not self.first_lift_at and not PREREQUISITES <= context.flags:
            return self._result("p09_and_p10_required")
        if context.on_apron or context.room != SIDE_PASSAGE:
            return self._result("offscreen")
        if context.contest_active:
            return self._result("contest_active")
        return None

    def _speaker_present(self, context: P11Context, speaker: str) -> bool:
        if speaker == "jack":
            return True
        # P11 explicitly establishes cross-side conversational sightlines.
        expected = {"felix": SIDE_PASSAGE, "bunny": PORCH, "frankie": COURTYARD,
                    "rita": SIDE_PASSAGE}
        return getattr(context, speaker + "_room", None) == expected.get(speaker)

    def _presentation_block(self, context: P11Context, source: str, tokens: tuple[str, ...]) -> CaptionResult | None:
        block = self._block(context)
        if block is not None:
            return block
        if not self.first_lift_at:
            return self._result("rescue_not_started")
        if source == "concern" and source not in self.presentations and not self.supported:
            return self._result("initial_concern_finished")
        if source in ("intro", "wing", "peg", "catch") and not self.supported:
            return self._result("supported_scene_finished")
        if source == "fold" and not self.fold_at:
            return self._result("display_not_folded")
        if source == "staged" and not self.ready:
            return self._result("display_not_staged")
        # Current VC03 variant binding explicitly stages Bunny on her porch
        # side during this existing protected scene. It claims no peg toggle.
        if source == "sincere" and context.bunny_room != PORCH:
            return self._result("bunny_at_porch_required")
        # Accepted scene-continuity interpretation: Felix is a listener during
        # Jackie's replies too. New receipts/resumes need him present; existing
        # prefixes survive interruption without moving either actor.
        if source == "sincere" and context.felix_room != SIDE_PASSAGE:
            return self._result("felix_required")
        # Sincere/concern text can resume safely after returning or staging.
        # Physical escape is deliberately independent of these text receipts.
        for token in tokens:
            speaker = self.SPEAKERS.get(token)
            if speaker is not None and not self._speaker_present(context, speaker):
                return self._result("speaker_absent")
        return None

    def lift(self, context: P11Context) -> CaptionResult:
        block = self._block(context)
        if block is not None:
            return block
        if self.phase != RescuePhase.CART:
            return self._result("already_supported" if self.supported else "already_folded")
        if context.felix_room != SIDE_PASSAGE:
            return self._result("felix_required")
        if context.cart_room != SIDE_PASSAGE or context.display_room != SIDE_PASSAGE:
            return self._result("existing_cart_and_display_required")
        if not context.gate.tested or not context.gate.peg_available:
            return self._result("tested_gate_required")
        self.phase = int(RescuePhase.SUPPORTED)
        self.lift_at = self.revision + 1
        if not self.first_lift_at:
            self.first_lift_at = self.lift_at
        self.catch_at = self.peg_request_at = self.peg_ack_at = 0
        self.advance_peg_at = self.lift_at if context.gate.peg_engaged else 0
        return self._commit("display_supported", "P11_LIFT", records=("P11.OPEN.001",),
            display_id="folded_display", cart_id="handcart", supported_by=("jack", "felix"),
            panel_safe=True, no_timer=True, advance_peg=context.gate.peg_engaged)

    def set_back(self, context: P11Context) -> CaptionResult:
        # This is also the travel/menu escape hook: no actor or clue gate may
        # strand Jackie. It never teleports a missing helper or moves a room.
        self._context(context)
        if not self.supported:
            return self._result("already_safe")
        self.phase = int(RescuePhase.CART)
        self.catch_at = self.peg_request_at = self.peg_ack_at = self.advance_peg_at = 0
        self.contest_request_at = 0
        records = ("P11.SUCCESS.004",) if not context.on_apron and context.room == SIDE_PASSAGE and context.felix_room == SIDE_PASSAGE else ()
        return self._commit("display_back_on_cart", "P11_SET_BACK", "safety", records=records,
                            catch_reset=True, peg_preserved=True, movement_free=True, items_preserved=True)

    def request_peg(self, context: P11Context) -> CaptionResult:
        block = self._block(context)
        if block is not None:
            return block
        if not self.supported:
            return self._result("support_required")
        if context.bunny_room != PORCH:
            return self._result("bunny_at_porch_required")
        if context.gate.peg_engaged:
            return self._result("gate_already_pegged", "P11.SUCCESS.002")
        if not context.gate.tested or not context.gate.peg_available:
            return self._result("tested_gate_required")
        if self.peg_request_at:
            return self._result("peg_request_pending")
        self.peg_request_at = self.revision + 1
        return self._commit("peg_requested", "P11_PEG_REQUEST", "external_action_request",
            records=("P11.CHOICE.002",), request_id=self.pending_peg_request_id,
            owner="P04", peg_id="hold_open_peg", engaged=True, helper="bunny")

    def acknowledge_peg(self, context: P11Context, request_id: str) -> CaptionResult:
        if type(request_id) is not str:
            raise ValueError("Peg receipt requires its request ID")
        self._context(context)
        if request_id != self.pending_peg_request_id:
            return self._result("stale_peg_request")
        block = self._block(context)
        if block is not None:
            return block
        if not self.supported or context.bunny_room != PORCH:
            return self._result("helper_unavailable")
        if not context.gate.peg_engaged:
            return self._result("peg_not_yet_engaged")
        self.peg_request_at = 0
        self.peg_ack_at = self.revision + 1
        return self._commit("peg_acknowledged", "P11_PEG_ACK", "handoff",
            records=("P11.SUCCESS.001",), owner="P04", peg_id="hold_open_peg", helper="bunny")

    def release_catch(self, context: P11Context) -> CaptionResult:
        block = self._block(context)
        if block is not None:
            return block
        if not self.supported:
            return self._result("support_required")
        if context.frankie_room != COURTYARD:
            return self._result("frankie_at_courtyard_required")
        if self.catch_at:
            return self._result("catch_already_released", "P11.SUCCESS.003")
        self.catch_at = self.revision + 1
        return self._commit("catch_released", "P11_CATCH_RELEASED", records=("P11.SUCCESS.003",),
                            helper="frankie", catch_id="wing_catch")

    def pull_handle(self, context: P11Context) -> CaptionResult:
        block = self._block(context)
        if block is not None:
            return block
        if not self.supported:
            return self._result("already_folded" if self.fold_at else "support_required")
        if context.felix_room != SIDE_PASSAGE:
            return self._result("felix_required")
        if not context.gate.peg_engaged:
            return self._result("peg_required", "P11.FAILURE.002")
        if not self.catch_at:
            return self._result("catch_required", "P11.FAILURE.003")
        # An external change without its requested P04 acknowledgment is not
        # evidence of Bunny's work or an advance peg. The host must reconcile
        # its missing receipt, or use the always-safe set-back hook before a
        # new lift snapshots the existing peg. Never toggle it for credit.
        if not self.peg_ack_at and not self.advance_peg_at:
            return self._result("peg_history_required")
        self.phase = int(RescuePhase.FOLDED)
        self.fold_at = self.revision + 1
        self.peg_request_at = 0
        # Fold/lower completes now, even if every caption/sound was interrupted.
        return self._commit("display_folded_safe", "P11_FOLD", "safety",
            supported=False, padded=True, panel_safe=True, cart_id="handcart",
            caption_source="fold", laugh_emitted=False)

    def stage_display(self, context: P11Context) -> CaptionResult:
        block = self._block(context)
        if block is not None:
            return block
        if self.ready:
            return self._result("already_staged", "P11.LOOK.004")
        if self.phase != RescuePhase.FOLDED:
            return self._result("safe_fold_required")
        if context.felix_room != SIDE_PASSAGE:
            return self._result("felix_required")
        self.phase = int(RescuePhase.STAGED)
        self.stage_at = self.revision + 1
        return self._commit("display_staged", "P11_STAGED", "puzzle",
            flags=("DISPLAY_STAGED", "HELP_ACCEPTED"), **self.display_handoff,
            caption_source="staged")

    def push_harder(self, context: P11Context) -> CaptionResult:
        block = self._block(context)
        if block is not None:
            return block
        if not self.supported:
            return self._result("display_safe")
        return self._result("fold_do_not_force", *( ("P11.FAILURE.001",) if context.felix_room == SIDE_PASSAGE else ()))

    def look(self, context: P11Context, obj: str) -> CaptionResult:
        if type(obj) is not str:
            raise ValueError("Objects require stable IDs")
        block = self._block(context)
        if block is not None:
            return block
        if obj == "folded_display" and self.ready:
            return self._result("display_staged", "P11.LOOK.004")
        source = {"folded_display": "wing", "display_wing": "wing", "wing_catch": "catch",
                  "hold_open_peg": "peg"}.get(obj)
        if source is not None and self.supported:
            return self._result("look", self.SOURCES[source])
        return self._result("no_p11_description")

    def request_contest(self, context: P11Context) -> CaptionResult:
        block = self._block(context)
        if block is not None:
            return block
        if not self.contest_eligible:
            return self._result("rescue_and_conversation_required", "VC03.NOT_READY")
        if context.felix_room != SIDE_PASSAGE:
            return self._result("felix_required")
        if self.contest_request_at:
            return self._result("contest_request_pending")
        self.contest_request_at = self.revision + 1
        return self._commit("contest_requested", "P11_VC03_REQUEST", "contest_request",
            records=("VC03.REMATCH" if "VC03_RESOLVED" in context.flags else "VC03.ENTRY",),
            encounter_id="VC03", request_id=self.pending_contest_request_id,
            safety_complete=True, sincere_text_presented=True, shared_credit_required=True,
            rescue_credit_variant=self.rescue_credit_variant,
            peg_ack_at=self.peg_ack_at, advance_peg_at=self.advance_peg_at)

    def acknowledge_contest_request(self, context: P11Context, request_id: str, *, cancelled: bool = False) -> CaptionResult:
        if type(request_id) is not str or type(cancelled) is not bool:
            raise ValueError("Contest receipt requires request ID and explicit cancellation")
        self._context(context)
        if request_id != self.pending_contest_request_id:
            return self._result("stale_contest_request")
        if not cancelled and (not self.contest_eligible or context.room != SIDE_PASSAGE
                              or context.on_apron or context.felix_room != SIDE_PASSAGE):
            return self._result("contest_handoff_unavailable")
        self.contest_request_at = 0
        return self._commit("contest_request_cancelled" if cancelled else "contest_request_acknowledged",
                            "P11_VC03_ACK", "handoff", encounter_id="VC03", cancelled=cancelled)

    def claim_laugh(self, context: P11Context) -> CaptionResult:
        block = self._block(context)
        if block is not None:
            return block
        if self.laugh_at:
            return self._result("laugh_already_consumed")
        if (not self.contest_eligible or not self._complete("fold")
                or self.contest_request_at or context.contest_active):
            return self._result("protected_scene")
        self.laugh_at = self.revision + 1
        return self._commit("earned_physical_reaction", "LAF11", "comedy",
                            source_id="P11.SUCCESS.005.02", never_double_fire=True)

    def hint(self, context: P11Context, level: int) -> CaptionResult:
        if type(level) is not int or level not in (1, 2, 3):
            raise ValueError("Hint level must be 1, 2 or 3")
        block = self._block(context)
        if block is not None:
            return block
        if level <= self.hint_level:
            return self._result("hint", f"P11.HINT.{level}")
        self.hint_level = level
        return self._commit("hint", "P11_HINT", "hint", records=(f"P11.HINT.{level}",), level=level)

    def act(self, context: P11Context, verb: Verb | str, obj: str, target: str | None = None) -> CaptionResult:
        verb = Verb(verb)
        if type(obj) is not str or (target is not None and type(target) is not str):
            raise ValueError("Objects require stable IDs")
        if verb == Verb.LOOK_AT:
            return self.look(context, obj)
        if verb == Verb.PULL and obj == "display_handle":
            return self.pull_handle(context)
        if verb == Verb.PUSH and obj == "folded_display":
            return self.push_harder(context)
        if verb == Verb.USE and obj == "folded_display" and target == "handcart":
            return self.set_back(context)
        if verb == Verb.USE and obj == "handcart" and target == "staging_pocket":
            return self.stage_display(context)
        if verb == Verb.PICK_UP and obj == "folded_display":
            return self.lift(context)
        if verb == Verb.TALK_TO:
            if obj == "bunny" and target == "peg":
                return self.request_peg(context)
            if obj == "frankie" and target == "catch":
                return self.release_catch(context)
            if obj == "felix" and target == "contest":
                return self.request_contest(context)
            if obj == "felix" and target == "sincere":
                return self.begin_presentation(context, "sincere")
        block = self._block(context)
        return block if block is not None else self._result("no_p11_action")

    def validate_context(self, context: P11Context) -> None:
        self._context(context)
        self.validate()
        if self.first_lift_at and not PREREQUISITES <= context.flags:
            raise ValueError("P11 progress without prior branch handoffs")
        if context.flags & {"DISPLAY_STAGED", "HELP_ACCEPTED"} and not self.ready:
            raise ValueError("Campaign claims unearned rescue completion")
        if self.first_lift_at and (context.cart_room != SIDE_PASSAGE or context.display_room != SIDE_PASSAGE):
            raise ValueError("Conflicting display/cart owners; transfer explicitly to P13")
        if self.supported and (context.room != SIDE_PASSAGE or context.on_apron or context.felix_room != SIDE_PASSAGE):
            raise ValueError("Return display to cart before campaign travel")
        if context.contest_active and self.supported:
            raise ValueError("Never run a contest while supporting the display")

    def validate(self) -> None:
        self._validate_captions()
        self._validate_serials("first_lift_at", "lift_at", "catch_at", "fold_at", "stage_at",
            "peg_request_at", "peg_ack_at", "advance_peg_at", "contest_request_at", "laugh_at")
        if type(self.phase) is not int or self.phase not in set(RescuePhase):
            raise ValueError("Invalid rescue phase")
        if type(self.hint_level) is not int or self.hint_level not in range(4):
            raise ValueError("Invalid hint level")
        if self.first_lift_at:
            if not self.first_lift_at <= self.lift_at:
                raise ValueError("Invalid attempt chronology")
        elif any((self.phase, self.lift_at, self.catch_at, self.fold_at, self.stage_at,
                  self.peg_request_at, self.peg_ack_at, self.advance_peg_at, self.presentations)):
            raise ValueError("Rescue fact before first lift")
        if self.phase == RescuePhase.CART and any((self.catch_at, self.fold_at, self.stage_at,
                                                   self.peg_request_at, self.peg_ack_at, self.advance_peg_at)):
            raise ValueError("Unsafe residue after cart recovery")
        if self.catch_at and not self.lift_at < self.catch_at:
            raise ValueError("Catch release belongs to another support attempt")
        if self.peg_request_at and (not self.supported or self.peg_request_at <= self.lift_at):
            raise ValueError("Stale peg request")
        if self.peg_ack_at and self.peg_ack_at <= self.lift_at:
            raise ValueError("Peg acknowledgment before support")
        if self.advance_peg_at and self.advance_peg_at != self.lift_at:
            raise ValueError("Advance peg identity mismatch")
        if self.phase >= RescuePhase.FOLDED:
            if not self.first_lift_at <= self.lift_at < self.catch_at < self.fold_at:
                raise ValueError("Fold without helper release")
            if not self.peg_ack_at and not self.advance_peg_at:
                raise ValueError("Fold without canonical peg provenance")
            if self.peg_ack_at and not self.peg_ack_at < self.fold_at:
                raise ValueError("Peg acknowledgment after safe folding")
        elif self.fold_at or self.stage_at:
            raise ValueError("Premature safe-stage reward")
        if self.ready and not self.fold_at < self.stage_at:
            raise ValueError("Staging before safe folding")
        if not self.ready and self.stage_at:
            raise ValueError("Unexpected staging serial")
        if self.contest_request_at and (not self.contest_eligible or self.contest_request_at <= self.stage_at):
            raise ValueError("Unsafe or premature contest request")
        if self.contest_request_at and self.contest_request_at <= max(self.presentations["sincere"].receipts.values()):
            raise ValueError("Contest request precedes complete sincere text")
        if self.contest_request_at and "concern" in self.presentations and self.contest_request_at <= max(
                self.presentations["concern"].receipts.values()):
            raise ValueError("Contest request precedes complete concern text")
        if self.laugh_at and (not self.contest_eligible or not self._complete("fold") or self.laugh_at <= self.stage_at):
            raise ValueError("Reaction over unsupported or protected scene")
        if self.laugh_at and self.laugh_at <= max((*self.presentations["sincere"].receipts.values(),
                                                  *self.presentations["fold"].receipts.values())):
            raise ValueError("Reaction before protected/payoff text completed")
        if self.laugh_at and "concern" in self.presentations and self.laugh_at <= max(
                self.presentations["concern"].receipts.values()):
            raise ValueError("Reaction before initial concern completed")
        for source, p in self.presentations.items():
            if not self.first_lift_at < p.serial:
                raise ValueError("Caption before rescue")
            if source == "fold" and not 0 < self.fold_at < p.serial:
                raise ValueError("Fold caption before physical safety")
            if source == "staged" and not 0 < self.stage_at < p.serial:
                raise ValueError("Staging caption before actual staging")
