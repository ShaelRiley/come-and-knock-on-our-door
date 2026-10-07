"""P08 courtyard layout and deliberate, caller-executed pre-evening autosave.

The campaign owns rooms, apron travel, prior branches, actors and actual I/O.
Canonical record IDs are presentation references; machine codes are not prose.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from enum import IntEnum
from types import MappingProxyType
from typing import Any, Mapping

from .model import Event, Result, Verb
from .p02_model import ROOMS

SAVE_KIND = "cakood-p08-branch"
SAVE_SCHEMA = 1
COURTYARD = "L05_COURTYARD"
KITCHEN = "L02_KITCHEN"
LIVING = "L01_LIVING_ROOM"
PREPARATIONS = frozenset(("PLAN_AGREED", "CERAMICS_READY", "GATE_TESTED", "HOLD_OPEN_AVAILABLE",
    "PA_TESTED", "MILO_ROLE_AGREED", "VC01_RESOLVED", "SOUND_READY", "SCREEN_BUILT",
    "VIVIAN_SCOPE_AGREED", "VC02_RESOLVED", "SCREEN_READY", "FOOD_READY"))
FLAG_IDS = frozenset(("LAYOUT_READY", "EVENING_STARTED"))
LAYOUT_OBJECTS = ("ceramic_carrier", "pa_kit", "completed_screen", "serving_table", "credit_slate")
CLOTH_IDS = ("clean_towel", "clean_napkin")
ONCE_IDS = frozenset(("P08_INTRO", "P08_UNPACK", "P08_EVENING"))


class Position(IntEnum):
    UNPLACED = 0
    HATCH = 1
    WALL = 2
    ALCOVE = 3
    LANE = 4


class Facing(IntEnum):
    INWARD = 1
    NEIGHBOR = 2


class StartPhase(IntEnum):
    NONE = 0
    CHECKLIST = 1
    CONFIRMATION = 2
    AUTOSAVE = 3


POSITION_OBJECTS = MappingProxyType({"buffet_position": Position.HATCH,
    "speaker_position": Position.WALL, "display_alcove": Position.ALCOVE,
    "gate_lane": Position.LANE})
LABEL_IDS = MappingProxyType(dict(zip(("gate_lane", "buffet_position", "speaker_position",
    "display_alcove", "serving_table", "kitchen_hatch", "plan_overlay"),
    (f"P08.LABEL.{i:03}" for i in range(1, 8)))))
FIXED_OBJECTS = frozenset((*LAYOUT_OBJECTS, *LABEL_IDS, "ceramic_service", "circulation_plan",
    "sightline_plan", "placement_symbols", "linen_hook", "hotpot_pot", "frankie", "bunny"))
SOURCE_BINDINGS = MappingProxyType({"circulation_plan": ("P08.READ.001",),
    "sightline_plan": ("P08.READ.002",), "placement_symbols": ("P08.READ.003",),
    "credit_slate": ("P08.READ.004",)})
SCRIPT_BINDINGS = MappingProxyType({
    "intro": ("P08.SCENE.001",),
    **{obj: (f"P08.LOOK.{i:03}",) for i, obj in enumerate(LABEL_IDS, 1)},
    **SOURCE_BINDINGS,
    "carrier": ("P08.SUCCESS.001",), "unpack": ("P08.SUCCESS.002",),
    "clean_towel": ("P08.SYSTEM.001",), "clean_napkin": ("P08.SYSTEM.002",),
    "pa": ("P08.SUCCESS.003",), "screen": ("P08.SUCCESS.004",),
    "table_push": ("P08.SUCCESS.005",), "table_pull": ("P08.SUCCESS.006",),
    "credit": ("P08.SUCCESS.007",), "lane_blocked": ("P08.FAILURE.001",),
    "hatch_hidden": ("P08.FAILURE.002",), "pa_backward": ("P08.FAILURE.003",),
    "display_visible": ("P08.FAILURE.004",), "all_ready": ("P08.SYSTEM.003",),
    "layout_dialogue": ("P08.DIALOGUE.001",),
    "readiness": ("P08.CHOICE.001", "P08.DIALOGUE.002", "P08.SYSTEM.004"),
    "begin_choice": ("P08.CHOICE.002",), "decline_choice": ("P08.CHOICE.003",),
    "declined": ("P08.SYSTEM.005",), "started": ("P08.SYSTEM.006",),
    **{f"hint_{i}": (f"P08.HINT.{i}",) for i in range(1, 4)},
})
READINESS_RECORDS = ("P08.DIALOGUE.002", "P08.SYSTEM.004")
EVENING_POSITIONS = MappingProxyType({"bunny": KITCHEN, "frankie": LIVING,
    "stringer": "L07_CONSERVATORY", "rita": "L07_CONSERVATORY", "milo": COURTYARD,
    "vivian": COURTYARD, "felix": "L04_SIDE_PASSAGE"})


@dataclass(frozen=True)
class P08Context:
    room: str
    on_apron: bool = False
    flags: frozenset[str] = frozenset()
    inventory: frozenset[str] = frozenset()
    carrier_padding: str | None = None
    frankie_room: str = LIVING
    bunny_room: str = LIVING
    contest_active: bool = False
    protected_objects: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if any(type(x) is not str or x not in ROOMS for x in (self.room, self.frankie_room, self.bunny_room)):
            raise ValueError("Unknown campaign room")
        if type(self.on_apron) is not bool or type(self.contest_active) is not bool:
            raise ValueError("Campaign mode must be boolean")
        for value in (self.flags, self.inventory, self.protected_objects):
            if type(value) is not frozenset or any(type(x) is not str for x in value):
                raise ValueError("Campaign facts must be frozen string sets")
        if self.inventory & FIXED_OBJECTS or not self.protected_objects <= set(LAYOUT_OBJECTS):
            raise ValueError("Invalid layout-object ownership")
        if self.carrier_padding is not None and (type(self.carrier_padding) is not str or self.carrier_padding not in CLOTH_IDS):
            raise ValueError("Unknown P03 padding")
        if "CERAMICS_READY" in self.flags and self.carrier_padding is None:
            raise ValueError("P03 must identify the cloth to return")
        if self.carrier_padding in self.inventory:
            raise ValueError("Carrier padding cannot also be pocket inventory")
        for reward, dependencies in {
            "SOUND_READY": {"PA_TESTED", "MILO_ROLE_AGREED", "VC01_RESOLVED"},
            "SCREEN_READY": {"SCREEN_BUILT", "VIVIAN_SCOPE_AGREED", "VC02_RESOLVED"},
            "HOLD_OPEN_AVAILABLE": {"GATE_TESTED"},
            "VC01_WON": {"VC01_RESOLVED"}, "VC02_WON": {"VC02_RESOLVED"},
        }.items():
            if reward in self.flags and not dependencies <= self.flags:
                raise ValueError("Inconsistent prior branch: " + reward)


@dataclass(frozen=True)
class P08Result(Result):
    code: str = ""
    line_ids: tuple[str, ...] = ()
    speech_unit_ids: tuple[str, ...] = ()


@dataclass
class P08World:
    positions: dict[str, int] = field(default_factory=lambda: dict.fromkeys(LAYOUT_OBJECTS, 0))
    facing: int = Facing.INWARD.value
    service_unpacked: bool = False
    returned_padding: str | None = None
    unpacked_surface_receipts: dict[str, int] = field(default_factory=dict)
    flags: set[str] = field(default_factory=set)
    observed_sources: set[str] = field(default_factory=set)
    source_serials: dict[str, int] = field(default_factory=dict)
    placement_serials: dict[str, int] = field(default_factory=dict)
    consumed: dict[str, int] = field(default_factory=dict)
    ownership_serials: dict[str, int] = field(default_factory=dict)
    acknowledged_handoffs: dict[str, int] = field(default_factory=dict)
    request_serial: int = 0
    pending_request_serial: int = 0
    pending_requested_at: int = 0
    pending_phase: int = StartPhase.NONE.value
    checklist_receipt: int = 0
    confirmed_at: int = 0
    completed_request_serial: int = 0
    completed_requested_at: int = 0
    completed_checklist_receipt: int = 0
    completed_confirmation_receipt: int = 0
    revision: int = 0
    hint_level: int = 0

    @property
    def inventory(self) -> tuple[str, ...]:
        return ()

    @property
    def conditions(self) -> dict[str, bool]:
        p = self.positions
        return {"buffet_at_hatch": self.service_unpacked and all(p[x] == Position.HATCH
                    for x in ("ceramic_carrier", "serving_table", "credit_slate")),
                "sound_facing_inward": p["pa_kit"] == Position.WALL and self.facing == Facing.INWARD,
                "display_concealed": p["completed_screen"] == Position.ALCOVE,
                "hatch_visible": p["completed_screen"] != Position.HATCH,
                "lane_clear": Position.LANE not in p.values()}

    @property
    def ready(self) -> bool:
        return all(self.conditions.values())

    @property
    def evening_started(self) -> bool:
        return "EVENING_STARTED" in self.flags

    @property
    def pending_request_id(self) -> str | None:
        return f"P08:START:{self.pending_request_serial}" if self.pending_request_serial else None

    @property
    def layout_handoff(self) -> dict[str, Any]:
        return {"positions": dict(self.positions), "facing": self.facing,
                "service_unpacked": self.service_unpacked, "conditions": self.conditions,
                "returned_padding": self.returned_padding, "padding_room": KITCHEN,
                "padding_location": "linen_hook", "evening_started": self.evening_started}

    @property
    def pending_handoffs(self) -> tuple[dict[str, Any], ...]:
        """Host applies each ownership transfer once, then acknowledges its ID.

        An old branch's completion projection is historical after this handoff.
        No item grant or player-facing interaction is implied by this protocol.
        """
        origins = {"ceramic_carrier": "P03", "credit_slate": "P03", "pa_kit": "P05",
                   "completed_screen": "P06", "padding": "P03"}
        return tuple({"handoff_id": f"P08:OWN:{obj}", "serial": serial,
            "from_owner": origins[obj], "to_owner": "P08", "object_id": self.returned_padding if obj == "padding" else obj,
            "includes": ("ceramic_service",) if obj == "ceramic_carrier" else (),
            "destination": "linen_hook" if obj == "padding" else "courtyard_layout",
            "room": KITCHEN if obj == "padding" else COURTYARD}
            for obj, serial in self.ownership_serials.items() if obj not in self.acknowledged_handoffs)

    def acknowledge_handoff(self, handoff_id: str, serial: int) -> P08Result:
        if type(handoff_id) is not str or type(serial) is not int:
            raise ValueError("Ownership acknowledgment requires exact ID and serial")
        matches = [x for x in self.pending_handoffs if x["handoff_id"] == handoff_id and x["serial"] == serial]
        if not matches:
            return self._result("stale_handoff")
        key = handoff_id.removeprefix("P08:OWN:")
        self.acknowledged_handoffs[key] = self.revision + 1
        return self._commit("handoff_acknowledged", (), (("P08_OWNERSHIP_ACK", "ownership_ack", {
            "handoff_id": handoff_id, "handoff_serial": serial}),))

    @staticmethod
    def _context(context: P08Context) -> None:
        if type(context) is not P08Context:
            raise ValueError("P08 requires explicit campaign context")

    @staticmethod
    def _choice(value: int, enum: type[IntEnum]) -> int:
        if type(value) not in (int, enum) or value not in tuple(enum):
            raise ValueError("Unknown P08 choice")
        return int(value)

    def object_location(self, obj: str, context: P08Context) -> str | None:
        self._context(context)
        if type(obj) is not str:
            raise ValueError("Objects require stable string IDs")
        if obj in ("frankie", "bunny"):
            return getattr(context, obj + "_room")
        if obj == "circulation_plan":
            return COURTYARD if "GATE_TESTED" in context.flags else None
        if obj == "sightline_plan":
            return COURTYARD if "SCREEN_READY" in context.flags else None
        if obj == "hotpot_pot":
            return KITCHEN if "FOOD_READY" in context.flags else None
        if obj == self.returned_padding or obj == "linen_hook":
            return KITCHEN
        if obj in ("ceramic_carrier", "credit_slate", "ceramic_service"):
            if "CERAMICS_READY" not in context.flags:
                return None
            key = "ceramic_carrier" if obj == "ceramic_service" else obj
            return COURTYARD if self.positions[key] else "kitchen_pass"
        if obj == "pa_kit":
            return COURTYARD if "SOUND_READY" in context.flags else None
        if obj == "completed_screen":
            return COURTYARD if "SCREEN_READY" in context.flags else None
        if obj in FIXED_OBJECTS:
            return COURTYARD
        return None

    def reachable(self, context: P08Context, obj: str) -> bool:
        location = self.object_location(obj, context)
        return not context.on_apron and (obj in context.inventory or location == context.room
            or (location == "kitchen_pass" and context.room in (KITCHEN, COURTYARD)))

    def _blocked(self, context: P08Context, *objects: str, preparation: bool = True) -> P08Result | None:
        self._context(context)
        if preparation and not PREPARATIONS <= context.flags:
            return self._result("preparations_required")
        if preparation and context.contest_active:
            return self._result("contest_active")
        if context.on_apron or any(not self.reachable(context, obj) for obj in objects):
            return self._result("offscreen")
        if preparation and context.room != COURTYARD:
            return self._result("courtyard_required")
        if self.returned_padding is not None and self.returned_padding != context.carrier_padding:
            raise ValueError("P03 padding handoff changed")
        return None

    def _result(self, code: str, *bindings: str) -> P08Result:
        self.validate()
        return P08Result("", (), code, tuple(x for binding in bindings for x in SCRIPT_BINDINGS[binding]))

    def _commit(self, code: str, bindings: tuple[str, ...], notices: tuple[tuple[str, str, dict[str, Any]], ...]) -> P08Result:
        self.revision += 1
        events = []
        for id, kind, data in notices:
            if id in ONCE_IDS:
                if id in self.consumed:
                    raise ValueError("Duplicate P08 one-shot")
                self.consumed[id] = self.revision
            events.append(Event(id, kind, {"serial": self.revision, "puzzle": "P08", **data}))
        self.validate()
        return P08Result("", tuple(events), code, tuple(x for binding in bindings for x in SCRIPT_BINDINGS[binding]))

    def _clear_request(self) -> None:
        self.pending_phase = self.pending_request_serial = self.pending_requested_at = self.checklist_receipt = self.confirmed_at = 0

    def _sync_layout(self) -> None:
        self.flags.discard("LAYOUT_READY")
        if self.ready:
            self.flags.add("LAYOUT_READY")
        self._clear_request()

    def journal_records(self) -> tuple[str, ...]:
        return tuple(line for source, lines in SOURCE_BINDINGS.items() if source in self.observed_sources for line in lines)

    def look(self, context: P08Context, obj: str) -> P08Result:
        blocked = self._blocked(context, obj, preparation=False)
        if blocked is not None:
            return blocked
        if obj == "plan_overlay" and self.ready:
            return self._result("layout_ready", "plan_overlay", "all_ready")
        if obj == "credit_slate" and self.positions[obj] != Position.HATCH:
            return self._result("inspect_state")
        return self._result("observed", obj) if obj in SCRIPT_BINDINGS else self._result("inspect_state")

    def acknowledge_source(self, context: P08Context, source: str, record_id: str) -> P08Result:
        if (type(source) is not str or source not in SOURCE_BINDINGS or type(record_id) is not str
                or record_id not in SOURCE_BINDINGS[source]):
            raise ValueError("Unknown presented P08 source record")
        blocked = self._blocked(context, source, preparation=False)
        if blocked is not None:
            return blocked
        if source == "credit_slate" and self.positions[source] != Position.HATCH:
            return self._result("credit_not_displayed")
        if source in self.observed_sources:
            return self._result("source_already_observed")
        self.observed_sources.add(source)
        self.source_serials[source] = self.revision + 1
        return self._commit("source_observed", (), (("P08_OBSERVE", "knowledge", {
            "source": source, "presented_record_id": record_id}),))

    def introduce(self, context: P08Context) -> P08Result:
        blocked = self._blocked(context, "frankie", "bunny")
        if blocked is not None:
            return blocked
        if "P08_INTRO" in self.consumed or self.evening_started:
            return self._result("layout_state")
        return self._commit("introduced", ("intro",), (("P08_INTRO", "dialogue", {}),))

    def place(self, context: P08Context, obj: str, position: int, *, pull: bool = False) -> P08Result:
        if type(obj) is not str or obj not in LAYOUT_OBJECTS or type(pull) is not bool:
            raise ValueError("Unknown movable P08 object")
        position = self._choice(position, Position)
        if position == Position.UNPLACED:
            raise ValueError("Unplaced is a saved initial state, not a destination")
        blocked = self._blocked(context, obj)
        if blocked is not None:
            return blocked
        if obj in context.protected_objects:
            return self._result("occupied_object")
        if self.positions[obj] == position:
            return self._result("already_positioned")
        self.positions[obj] = position
        first_claim = obj != "serving_table" and obj not in self.ownership_serials
        if first_claim:
            self.ownership_serials[obj] = self.revision + 1
        self.placement_serials[obj] = self.revision + 1
        self._sync_layout()
        binding = None
        if position == Position.LANE:
            binding = "lane_blocked"
        elif obj == "completed_screen":
            binding = "screen" if position == Position.ALCOVE else "hatch_hidden" if position == Position.HATCH else "display_visible"
        elif obj == "pa_kit":
            binding = "pa_backward" if self.facing == Facing.NEIGHBOR else "pa" if position == Position.WALL else None
        elif position == Position.HATCH:
            binding = {"ceramic_carrier": "carrier", "credit_slate": "credit",
                       "serving_table": "table_pull" if pull else "table_push"}.get(obj)
        bindings = (binding or "plan_overlay",) + (("all_ready",) if self.ready else ())
        claims = tuple(("P08_OWNERSHIP_HANDOFF", "ownership_handoff", h) for h in self.pending_handoffs
                       if first_claim and h["object_id"] == obj)
        return self._commit("positioned", bindings, claims + (("P08_PLACE", "layout", {
            "object_id": obj, "position": position, "conditions": self.conditions,
            "service_moves_with_carrier": obj == "ceramic_carrier" and self.service_unpacked}),))

    def orient_pa(self, context: P08Context, facing: int) -> P08Result:
        facing = self._choice(facing, Facing)
        blocked = self._blocked(context, "pa_kit")
        if blocked is not None:
            return blocked
        if "pa_kit" in context.protected_objects:
            return self._result("occupied_object")
        if facing == self.facing:
            return self._result("already_oriented")
        self.facing = facing
        self.placement_serials["pa_facing"] = self.revision + 1
        self._sync_layout()
        binding = "pa_backward" if facing == Facing.NEIGHBOR else "pa" if self.positions["pa_kit"] == Position.WALL else None
        return self._commit("oriented", (binding,) if binding else (), (("P08_ORIENT", "layout", {
            "facing": facing, "conditions": self.conditions}),))

    def unpack_service(self, context: P08Context) -> P08Result:
        blocked = self._blocked(context, "ceramic_carrier")
        if blocked is not None:
            return blocked
        if self.service_unpacked:
            return self._result("already_unpacked")
        if self.positions["ceramic_carrier"] != Position.HATCH or self.positions["serving_table"] != Position.HATCH:
            return self._result("buffet_surface_required")
        self.service_unpacked = True
        self.unpacked_surface_receipts = {obj: self.placement_serials[obj] for obj in ("ceramic_carrier", "serving_table")}
        self.returned_padding = context.carrier_padding
        self.ownership_serials["padding"] = self.revision + 1
        self._sync_layout()
        claims = tuple(("P08_OWNERSHIP_HANDOFF", "ownership_handoff", h) for h in self.pending_handoffs
                       if h["object_id"] == self.returned_padding)
        return self._commit("service_unpacked", ("unpack", self.returned_padding), claims + (
            ("P08_UNPACK", "object", {"service": "ceramic_service", "room": COURTYARD,
                "padding": self.returned_padding, "return_room": KITCHEN, "return_location": "linen_hook"}),))

    def layout_dialogue(self, context: P08Context) -> P08Result:
        blocked = self._blocked(context, "frankie", "bunny")
        if blocked is not None:
            return blocked
        return self._result("layout_dialogue", "layout_dialogue") if self.ready else self._result("layout_incomplete")

    def request_start(self, context: P08Context) -> P08Result:
        blocked = self._blocked(context, "frankie")
        if blocked is not None:
            return blocked
        if self.evening_started:
            return self._result("evening_started")
        if not self.ready:
            return self._result("layout_incomplete")
        if self.pending_handoffs:
            return self._result("handoff_pending")
        if self.pending_phase:
            return self.pending_presentation(context)
        self.request_serial += 1
        self.pending_request_serial = self.request_serial
        self.pending_requested_at = self.revision + 1
        self.pending_phase = StartPhase.CHECKLIST.value
        return self._commit("readiness_requested", ("readiness",), (("P08_READINESS", "presentation", {
            "request_id": self.pending_request_id, "required_records": READINESS_RECORDS}),))

    def pending_presentation(self, context: P08Context) -> P08Result:
        blocked = self._blocked(context, "frankie")
        if blocked is not None:
            return blocked
        if self.pending_phase == StartPhase.CHECKLIST:
            return self._result("readiness_requested", "readiness")
        if self.pending_phase == StartPhase.CONFIRMATION:
            return self._result("confirmation_pending", "begin_choice", "decline_choice")
        return self._result("autosave_pending" if self.pending_phase == StartPhase.AUTOSAVE else "no_pending_start")

    def acknowledge_readiness(self, context: P08Context, request_id: str, record_ids: tuple[str, ...]) -> P08Result:
        if type(request_id) is not str or type(record_ids) is not tuple or record_ids != READINESS_RECORDS:
            raise ValueError("Readiness requires the exact presented checklist and confirmation")
        blocked = self._blocked(context, "frankie")
        if blocked is not None:
            return blocked
        if request_id != self.pending_request_id or self.pending_phase != StartPhase.CHECKLIST:
            return self._result("stale_readiness")
        self.pending_phase = StartPhase.CONFIRMATION.value
        self.checklist_receipt = self.revision + 1
        return self._commit("confirmation_pending", ("begin_choice", "decline_choice"), (("P08_CHECKLIST_PRESENTED", "presentation", {"request_id": request_id}),))

    def confirm_start(self, context: P08Context, request_id: str, accepted: bool) -> P08Result:
        if type(request_id) is not str or type(accepted) is not bool:
            raise ValueError("Readiness needs explicit boolean confirmation")
        blocked = self._blocked(context, "frankie")
        if blocked is not None:
            return blocked
        if request_id != self.pending_request_id or self.pending_phase != StartPhase.CONFIRMATION:
            return self._result("stale_confirmation")
        if not accepted:
            self._clear_request()
            return self._commit("declined", ("declined",), (("P08_START_DECLINED", "choice", {"request_id": request_id}),))
        self.pending_phase = StartPhase.AUTOSAVE.value
        self.confirmed_at = self.revision + 1
        return self._commit("autosave_requested", (), (("P08_AUTOSAVE_REQUEST", "autosave_request", {
            "request_id": request_id, "before_phase": "E03", "must_complete_before_transition": True}),))

    def retry_autosave(self, context: P08Context, request_id: str) -> P08Result:
        blocked = self._blocked(context, "frankie")
        if blocked is not None:
            return blocked
        if type(request_id) is not str:
            raise ValueError("Autosave requests require stable string IDs")
        if request_id != self.pending_request_id or self.pending_phase != StartPhase.AUTOSAVE:
            return self._result("stale_autosave")
        return self._commit("autosave_requested", (), (("P08_AUTOSAVE_REQUEST", "autosave_request", {
            "request_id": request_id, "before_phase": "E03", "must_complete_before_transition": True}),))

    def acknowledge_autosave(self, context: P08Context, request_id: str, succeeded: bool) -> P08Result:
        if type(request_id) is not str or type(succeeded) is not bool:
            raise ValueError("Autosave needs explicit successful-I/O acknowledgment")
        blocked = self._blocked(context, "frankie")
        if blocked is not None:
            return blocked
        if request_id != self.pending_request_id or self.pending_phase != StartPhase.AUTOSAVE:
            return self._result("stale_autosave")
        if not succeeded:
            return self._result("autosave_failed")
        self.flags.add("EVENING_STARTED")
        self.completed_request_serial = self.pending_request_serial
        self.completed_requested_at = self.pending_requested_at
        self.completed_checklist_receipt = self.checklist_receipt
        self.completed_confirmation_receipt = self.confirmed_at
        self._clear_request()
        return self._commit("evening_started", ("started",), (("P08_EVENING", "phase", {
            "phase": "E03", "request_id": request_id, "autosave_acknowledged": True,
            "npc_positions": dict(EVENING_POSITIONS), "essential_access_retained": True}),))

    def cancel_start(self, context: P08Context) -> P08Result:
        self._context(context)
        if not self.pending_phase:
            return self._result("no_pending_start")
        request_id = self.pending_request_id
        self._clear_request()
        return self._commit("start_cancelled", (), (("P08_START_CANCELLED", "choice", {"request_id": request_id}),))

    def hint(self, context: P08Context, level: int | None = None) -> P08Result:
        self._context(context)
        if level is not None and (type(level) is not int or level not in (1, 2, 3)):
            raise ValueError("Hint level must be 1, 2 or 3")
        if not PREPARATIONS <= context.flags:
            return self._result("preparations_required")
        requested = level if level is not None else min(3, self.hint_level + 1)
        if requested <= self.hint_level:
            return self._result("hint", f"hint_{requested}")
        self.hint_level = requested
        return self._commit("hint", (f"hint_{requested}",), (("P08_HINT", "hint", {"level": requested}),))

    def act(self, context: P08Context, verb: Verb | str, obj: str, target: str | None = None) -> P08Result:
        verb = Verb(verb)
        if type(obj) is not str or (target is not None and type(target) is not str):
            raise ValueError("Objects require stable string IDs")
        if verb == Verb.LOOK_AT and target is None:
            return self.look(context, obj)
        blocked = self._blocked(context, obj, *((target,) if target else ()))
        if blocked is not None:
            return blocked
        if obj in LAYOUT_OBJECTS and target in POSITION_OBJECTS:
            if verb == Verb.USE or (obj == "serving_table" and verb in (Verb.PUSH, Verb.PULL)):
                return self.place(context, obj, POSITION_OBJECTS[target], pull=verb == Verb.PULL)
        if obj == "ceramic_carrier" and verb in (Verb.OPEN, Verb.USE) and target is None:
            return self.unpack_service(context)
        if obj == "frankie" and verb == Verb.TALK_TO and target is None:
            return self.request_start(context)
        return self._result("unhelpful")

    def validate_context(self, context: P08Context) -> None:
        self.validate()
        self._context(context)
        if (self.placement_serials or self.consumed or self.request_serial or self.hint_level) and not PREPARATIONS <= context.flags:
            raise ValueError("P08 progress without all preparations")
        if self.returned_padding is not None and self.returned_padding != context.carrier_padding:
            raise ValueError("Saved cloth differs from P03 entitlement")
        if context.flags & (FLAG_IDS - self.flags):
            raise ValueError("Caller claims uncommitted P08 flags")

    def validate(self) -> None:
        def require(ok: bool, message: str) -> None:
            if not ok:
                raise ValueError("Invalid P08 state: " + message)
        require(type(self.positions) is dict and set(self.positions) == set(LAYOUT_OBJECTS), "positions")
        require(all(type(x) is int and x in tuple(Position) for x in self.positions.values()), "position value")
        require(type(self.facing) is int and self.facing in tuple(Facing), "facing")
        require(type(self.service_unpacked) is bool, "unpacking")
        require(self.returned_padding is None or (type(self.returned_padding) is str and self.returned_padding in CLOTH_IDS), "padding")
        require(type(self.flags) is set and all(type(x) is str for x in self.flags) and self.flags <= FLAG_IDS, "flags")
        require(type(self.observed_sources) is set and all(type(x) is str for x in self.observed_sources)
                and self.observed_sources <= set(SOURCE_BINDINGS), "sources")
        require(type(self.revision) is int and self.revision >= 0, "revision")
        require(type(self.hint_level) is int and 0 <= self.hint_level <= 3, "hint")
        for ledger, keys in ((self.source_serials, set(SOURCE_BINDINGS)),
                             (self.placement_serials, {*LAYOUT_OBJECTS, "pa_facing"}), (self.consumed, ONCE_IDS),
                             (self.ownership_serials, {"ceramic_carrier", "credit_slate", "pa_kit", "completed_screen", "padding"}),
                             (self.acknowledged_handoffs, set(self.ownership_serials)),
                             (self.unpacked_surface_receipts, {"ceramic_carrier", "serving_table"})):
            require(type(ledger) is dict and set(ledger) <= keys, "ledger keys")
            require(all(type(x) is int and 0 < x <= self.revision for x in ledger.values()), "receipt serial")
        expected_claims = {obj for obj in LAYOUT_OBJECTS if obj != "serving_table" and self.positions[obj]}
        if self.service_unpacked:
            expected_claims.add("padding")
        require(set(self.unpacked_surface_receipts) == ({"ceramic_carrier", "serving_table"} if self.service_unpacked else set()), "unpack surface receipt mismatch")
        if self.service_unpacked:
            require(all(serial < self.consumed.get("P08_UNPACK", 0) and serial <= self.placement_serials.get(obj, 0)
                        for obj, serial in self.unpacked_surface_receipts.items()), "unpack before surface placement")
        require(set(self.ownership_serials) == expected_claims, "ownership claim mismatch")
        require(all(self.ownership_serials[obj] < serial for obj, serial in self.acknowledged_handoffs.items()), "ack before ownership transfer")
        require(all(serial <= self.placement_serials[obj] for obj, serial in self.ownership_serials.items() if obj != "padding"), "claim after placement")
        require(not self.service_unpacked or self.ownership_serials["padding"] == self.consumed.get("P08_UNPACK"), "cloth handoff mismatch")
        require(not self.pending_phase or not self.pending_handoffs, "pending start before host handoff")
        require(not self.evening_started or not self.pending_handoffs, "evening before host handoff")
        require(set(self.source_serials) == self.observed_sources, "source receipt mismatch")
        require(all(bool(value) == (obj in self.placement_serials) for obj, value in self.positions.items()), "placement receipt mismatch")
        require(self.facing == Facing.INWARD or "pa_facing" in self.placement_serials, "uncommitted facing")
        require(self.service_unpacked == (self.returned_padding is not None) == ("P08_UNPACK" in self.consumed), "unpack receipt mismatch")
        require(not self.service_unpacked or bool(self.positions["ceramic_carrier"] and self.positions["serving_table"]), "unpacking without a surface")
        require(("LAYOUT_READY" in self.flags) == self.ready, "stale readiness")
        require(self.evening_started == ("P08_EVENING" in self.consumed), "phase receipt mismatch")
        require(not self.evening_started or self.service_unpacked, "evening without service")
        require(type(self.pending_phase) is int and self.pending_phase in tuple(StartPhase), "pending phase")
        require(all(type(x) is int and x >= 0 for x in (self.request_serial, self.pending_request_serial,
                                                      self.pending_requested_at, self.checklist_receipt, self.confirmed_at, self.completed_request_serial, self.completed_requested_at,
                                                      self.completed_checklist_receipt, self.completed_confirmation_receipt)), "request counters")
        require(self.pending_request_serial <= self.request_serial <= self.revision, "request serial")
        require(bool(self.pending_phase) == bool(self.pending_requested_at), "request timestamp mismatch")
        require(self.pending_requested_at <= self.revision, "future request timestamp")
        require(bool(self.pending_phase) == bool(self.pending_request_serial), "pending request mismatch")
        require(not self.pending_phase or (self.ready and not self.evening_started), "pending on invalid layout")
        require(bool(self.checklist_receipt) == (self.pending_phase >= StartPhase.CONFIRMATION), "checklist receipt")
        require(bool(self.confirmed_at) == (self.pending_phase == StartPhase.AUTOSAVE), "confirmation receipt")
        require(self.checklist_receipt <= self.revision and self.confirmed_at <= self.revision, "future acknowledgment")
        require(not self.checklist_receipt or self.pending_requested_at < self.checklist_receipt, "checklist before request")
        if self.pending_phase:
            require(max((*self.placement_serials.values(), *self.acknowledged_handoffs.values(), self.consumed["P08_UNPACK"])) < self.pending_requested_at, "request predates layout or handoff")
        require(not self.confirmed_at or self.checklist_receipt < self.confirmed_at, "confirmation before checklist")
        require(not self.evening_started or self.request_serial > 0, "evening without a request")
        require(len(set(self.source_serials.values())) == len(self.source_serials), "duplicate source receipt")
        require(not set(self.source_serials.values()) & (set(self.consumed.values()) | set(self.placement_serials.values())), "source shares unrelated action")
        require(len(set(self.consumed.values())) == len(self.consumed), "duplicate one-shot serial")
        require(all(bool(x) == self.evening_started for x in (self.completed_request_serial, self.completed_requested_at,
                    self.completed_checklist_receipt, self.completed_confirmation_receipt)), "completed start receipt mismatch")
        if self.evening_started:
            require(self.completed_request_serial <= self.request_serial, "future completed request")
            require(self.completed_requested_at < self.completed_checklist_receipt < self.completed_confirmation_receipt < self.consumed["P08_EVENING"], "autosave/confirmation order")
            require(max(self.acknowledged_handoffs.values()) < self.completed_requested_at, "start before handoff acknowledgment")
            require(self.consumed["P08_UNPACK"] < self.consumed["P08_EVENING"], "evening before unpack")

    def save(self) -> dict[str, Any]:
        self.validate()
        state = asdict(self)
        for name in ("flags", "observed_sources"):
            state[name] = sorted(state[name])
        return {"kind": SAVE_KIND, "schema": SAVE_SCHEMA, "state": state}

    @classmethod
    def load(cls, data: Mapping[str, Any], context: P08Context | None = None) -> P08World:
        try:
            if (type(data) is not dict or set(data) != {"kind", "schema", "state"}
                    or data["kind"] != SAVE_KIND or type(data["schema"]) is not int or data["schema"] != SAVE_SCHEMA
                    or type(data["state"]) is not dict or set(data["state"]) != {f.name for f in fields(cls)}):
                raise ValueError("Invalid P08 save envelope")
            state = dict(data["state"])
            for name in ("flags", "observed_sources"):
                value = state[name]
                if type(value) is not list or any(type(x) is not str for x in value) or len(set(value)) != len(value):
                    raise ValueError("Invalid serialized " + name)
                state[name] = set(value)
            for name in ("positions", "source_serials", "placement_serials", "consumed", "ownership_serials", "acknowledged_handoffs", "unpacked_surface_receipts"):
                if type(state[name]) is not dict:
                    raise ValueError("Invalid serialized ledger")
                state[name] = dict(state[name])
            world = cls(**state)
            world.validate()
            if context is not None:
                world.validate_context(context)
            return world
        except (KeyError, TypeError) as error:
            raise ValueError("Invalid P08 save") from error
