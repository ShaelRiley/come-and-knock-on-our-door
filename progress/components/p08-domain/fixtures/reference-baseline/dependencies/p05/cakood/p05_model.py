"""NEW independent P05 reference model, 2026-10-06.

The host owns actor movement, readable-source observation, contest resolution,
physical ownership and presentation. Nothing here detects sound or scores VC01.
See DESIGN.md for newly chosen schema, bounded serials and trust boundaries.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from enum import IntEnum
import json
from pathlib import Path
from types import MappingProxyType
from typing import Callable
from uuid import uuid4

GARAGE = "L06_GARAGE"
LIVING = "L01_LIVING_ROOM"
KITCHEN = "L02_KITCHEN"
COURTYARD = "L05_COURTYARD"
ROOMS = frozenset((GARAGE, LIVING, KITCHEN, COURTYARD, "L03_PORCH", "L04_SIDE_PASSAGE", "L07_CONSERVATORY"))
SAVE_KIND = "cakood-p05-reconstruction"
SAVE_SCHEMA = 1
MAX_SERIAL = 0xFFFFFFFF
_NO_CONTEXT = object()
CREDIT_ID = "milo_equipment"
CREDIT_TEXT = "Sound equipment courtesy of Milo Pennant"
FLAG_IDS = frozenset(("PA_TESTED", "MILO_ROLE_AGREED", "SOUND_READY"))


class Listener(IntEnum):
    BUNNY = 1
    AUDIENCE = 2  # witnessed comparison uses 2; remaining allocation is NEW


class Source(IntEnum):
    TAPE = 0
    MIC = 1


OBJECTS = ("pa_kit", "input_selector", "microphone", "mic_socket", "loudspeaker",
           "speaker_swivel_handle", "marked_listening_position", "slogan_tape",
           "equipment_credit_slate", "handcart")
KIT_PARTS = frozenset(OBJECTS) - {"handcart", "marked_listening_position"}
FIXED_OBJECTS = frozenset((*OBJECTS, "microphone_cable", "bunny", "milo", "audience"))
LABEL_IDS = MappingProxyType({obj: f"P05.LABEL.{i:03}" for i, obj in enumerate(OBJECTS, 1)})
SOURCE_BINDINGS = MappingProxyType({"input_selector": "P05.READ.001", "mic_socket": "P05.READ.002",
                                    "equipment_credit_slate": "P05.READ.003"})
SCRIPT_BINDINGS = MappingProxyType({
    **{obj: (f"P05.LOOK.{i:03}",) for i, obj in enumerate(OBJECTS, 1)},
    "intro": ("P05.SCENE.001",), "tape": ("P05.DIALOGUE.001",),
    "connect": ("P05.SUCCESS.001",), "mic": ("P05.SUCCESS.002",), "aim": ("P05.SUCCESS.003",),
    "invite_bunny": ("P05.CHOICE.001", "P05.DIALOGUE.002"),
    "invite_audience": ("P05.CHOICE.002", "P05.DIALOGUE.003"),
    "test_choice": ("P05.CHOICE.003",), "sentence": ("P05.DIALOGUE.004",),
    "bunny_clear": ("P05.SUCCESS.004",), "audience_clear": ("P05.SUCCESS.005", "P05.SYSTEM.001"),
    "wrong_socket": ("P05.FAILURE.001",), "bunny_unclear": ("P05.FAILURE.002",),
    "audience_unclear": ("P05.FAILURE.003", "P05.SYSTEM.002"),
    "credit_choice": ("P05.CHOICE.004",), "credit": ("P05.READ.003", "P05.DIALOGUE.005"),
    "flattery": ("P05.FAILURE.004",), "role": ("P05.DIALOGUE.006",),
    "loan": ("P05.DIALOGUE.007",), "complete": ("P05.SUCCESS.006",),
    "contest_not_ready": ("VC01.NOT_READY",), "need_resolution": ("VC01.NEED_RESOLUTION",),
    **{f"hint_{i}": (f"P05.HINT.{i}",) for i in range(1, 4)},
})
ONCE_IDS = frozenset(("P05_INTRO", "P05_FEEDBACK_BUNNY", "P05_FEEDBACK_AUDIENCE", "P05_CREDIT",
                      "P05_ROLE", "P05_COMPLETE", "LAF05", "AUD_SOUNDTEST"))
_BINDINGS = json.loads(Path(__file__).with_name("canonical-bindings.json").read_text(encoding="utf-8"))
_RECORDS = _BINDINGS["records"]


def canonical_record(record_id: str) -> dict:
    """Detached literal final-catalog record; never synthesize dialogue."""
    return deepcopy(_RECORDS[record_id])


def split_serial(value: int) -> tuple[int, int]:
    _integer(value, 0, MAX_SERIAL)
    return value >> 16, value & 0xFFFF


def join_serial(high: int, low: int) -> int:
    _integer(high, 0, 0xFFFF); _integer(low, 0, 0xFFFF)
    return (high << 16) | low


def _integer(value, low=0, high=MAX_SERIAL):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("Expected a bounded integer, never a boolean")


def _choice(value, enum):
    if type(value) not in (int, enum) or value not in tuple(enum):
        raise ValueError("Invalid P05 choice")
    return int(value)


@dataclass(frozen=True)
class OwnedObject:
    object_id: str
    owner: str
    room: str

    def __post_init__(self):
        if (type(self.object_id) is not str or self.object_id not in {"pa_kit", "handcart"}
                or type(self.owner) is not str or self.owner not in {"P05", "P08", "P11", "P13"}
                or type(self.room) is not str or self.room not in ROOMS):
            raise ValueError("Invalid campaign ownership projection")
        if self.object_id == "pa_kit" and self.owner not in {"P05", "P08"}:
            raise ValueError("Unknown PA owner")
        if self.object_id == "pa_kit" and self.owner == "P08" and self.room != COURTYARD:
            raise ValueError("P08 PA ownership remains in the courtyard")
        if self.object_id == "handcart" and self.owner == "P08":
            raise ValueError("P08 never owns or moves the handcart")


@dataclass(frozen=True)
class P05Context:
    room: str
    on_apron: bool = False
    flags: frozenset[str] = frozenset()
    inventory: frozenset[str] = frozenset()
    bunny_room: str = LIVING
    milo_room: str = GARAGE
    audience_present: bool = True
    contest_active: bool = False
    ownership: tuple[OwnedObject, ...] = ()

    def __post_init__(self):
        for value in (self.room, self.bunny_room, self.milo_room):
            if type(value) is not str or value not in ROOMS:
                raise ValueError("Unknown campaign room")
        for value in (self.on_apron, self.audience_present, self.contest_active):
            if type(value) is not bool:
                raise ValueError("Campaign modes must be booleans")
        for value in (self.flags, self.inventory):
            if type(value) is not frozenset or any(type(x) is not str or not x for x in value):
                raise ValueError("Campaign facts must be frozen nonempty string sets")
        if self.inventory & FIXED_OBJECTS:
            raise ValueError("P05 fixtures cannot also be pocket inventory")
        if (type(self.ownership) is not tuple or any(type(x) is not OwnedObject for x in self.ownership)
                or len({x.object_id for x in self.ownership}) != len(self.ownership)):
            raise ValueError("Duplicate or invalid owner projection")
        for reward, requirements in {
            "VC01_WON": {"VC01_RESOLVED"}, "MILO_ROLE_AGREED": {"PA_TESTED"},
            "SOUND_READY": {"PA_TESTED", "MILO_ROLE_AGREED", "VC01_RESOLVED"},
        }.items():
            if reward in self.flags and not requirements <= self.flags:
                raise ValueError("Inconsistent campaign flags: " + reward)


@dataclass(frozen=True)
class ReceiptToken:
    kind: str
    serial: int
    session: str


@dataclass(frozen=True)
class ContestRequest:
    encounter_id: str
    serial: int  # opaque session-scoped dispatch ticket, not a saved SCI integer
    receipt_serial: int  # bounded logical request receipt


@dataclass(frozen=True)
class Event:
    id: str
    kind: str
    payload: dict = field(default_factory=dict)


@dataclass(frozen=True)
class P05Result:
    text: str = ""
    events: tuple[Event, ...] = ()
    code: str = ""
    line_ids: tuple[str, ...] = ()
    speech_unit_ids: tuple[str, ...] = ()
    token: ReceiptToken | None = None


@dataclass
class _State:
    revision: int = 0
    connected: bool = False
    source: int = Source.TAPE.value
    aim: int = 0
    hardware_serial: int = 0
    invitations: dict = field(default_factory=dict)
    active_invites: dict = field(default_factory=dict)
    tests: dict = field(default_factory=dict)
    credit_open: int = 0
    credit_written: int = 0
    role: int = 0
    contest_request: int = 0
    loan_request: int = 0
    loan_test: int = 0
    loan_hardware: int = 0
    complete: int = 0
    completed_request: int = 0
    completion_test: int = 0
    completion_hardware: int = 0
    sources: dict = field(default_factory=dict)
    pending_source: dict = field(default_factory=dict)
    consumed: dict = field(default_factory=dict)
    hint_level: int = 0


class WorldBusyError(RuntimeError):
    """No input or save is accepted inside an atomic host loan commit."""


class P05World:
    def __init__(self):
        self._state = _State()
        self._transaction_active = False
        self._session = uuid4().hex  # deliberately not saved; rejects pre-restore callbacks

    def _ensure_idle(self):
        if self._transaction_active:
            raise WorldBusyError("P05 host transaction is in progress")

    @property
    def revision(self):
        return self._state.revision

    @revision.setter
    def revision(self, value):
        self._ensure_idle()
        _integer(value, self.revision, MAX_SERIAL)
        if (self._state.loan_request or self._state.contest_request) and value != self.revision:
            raise ValueError("Pending loan reserves its completion/cancellation serial")
        candidate = deepcopy(self._state); candidate.revision = value
        self._validate(candidate)
        self._state = candidate

    @property
    def flags(self):
        s = self._state
        return frozenset((*(('PA_TESTED',) if s.tests else ()),
                          *(('MILO_ROLE_AGREED',) if s.role else ()),
                          *(('SOUND_READY',) if s.complete else ())))

    @property
    def inventory(self):
        return ()

    @property
    def reserved_external_items(self):
        return frozenset()

    @property
    def source(self):
        return Source(self._state.source)

    @property
    def microphone_connected(self):
        return self._state.connected

    @property
    def speaker_aim(self):
        return self._state.aim

    @property
    def tested_listener(self):
        if not self._state.tests:
            return None
        return Listener(int(max(self._state.tests, key=lambda k: self._state.tests[k]["serial"])))

    @property
    def current_hardware_working(self):
        s = self._state
        return s.connected and s.source == Source.MIC and str(s.aim) in s.tests

    @property
    def credit_text(self):
        return CREDIT_TEXT if self._state.credit_written else None

    @property
    def credit_token(self):
        return self._token("credit", self._state.credit_open)

    @property
    def pending_request(self):
        receipt = self._state.contest_request
        if not receipt:
            return None
        return ContestRequest("VC01", (int(self._session, 16) << 32) | receipt, receipt)

    @property
    def pending_handoff(self):
        s = self._state
        if not s.loan_request:
            return None
        return {"handoff_id": "P05:LOAN", "serial": s.loan_request,
                "objects": ({"object_id": "pa_kit", "owner": "P05", "room": COURTYARD,
                             "location": "courtyard_staging", "layout_applied": False},
                            {"object_id": "handcart", "owner": "P05", "room": GARAGE,
                             "location": "visible_parking"}),
                "token": self._token("loan", s.loan_request)}

    @property
    def kit_handoff(self):
        if not self._state.complete:
            return None
        return {"object_id": "pa_kit", "owner": "P05", "room": COURTYARD,
                "location": "courtyard_staging", "layout_applied": False,
                "historical": True, "serial": self._state.complete}

    def _token(self, kind, serial):
        return ReceiptToken(kind, serial, self._session) if serial else None

    def _matches(self, token, kind, serial):
        return (type(token) is ReceiptToken and type(token.serial) is int and serial > 0
                and token == self._token(kind, serial))

    def _result(self, code, *bindings, events=(), token=None, records=()):
        ids = tuple(x for b in bindings for x in SCRIPT_BINDINGS[b]) + tuple(records)
        if any(x not in _RECORDS for x in ids):
            raise ValueError("Unknown canonical record")
        units = tuple(u["line_id"] for rid in ids for u in _RECORDS[rid]["speech_units"])
        return P05Result("", tuple(events), code, ids, units, token)

    def _commit(self, code: str, mutate: Callable, *bindings, notices=(), token_kind=None, records=()):
        self.validate()
        if self._state.loan_request and code not in {"sound_ready", "handoff_cancelled"}:
            return self._result("handoff_in_progress")
        if self._state.contest_request and code not in {"contest_request_acknowledged", "contest_request_cancelled"}:
            return self._result("contest_request_pending")
        if self.revision == MAX_SERIAL:
            return self._result("serial_exhausted")
        candidate = deepcopy(self._state)
        candidate.revision += 1
        mutate(candidate, candidate.revision)
        self._validate(candidate)
        events = tuple(Event(id, kind, deepcopy({"serial": candidate.revision, "puzzle": "P05", **data}))
                       for id, kind, data in notices)
        result = self._result(code, *bindings, events=events,
                              token=self._token(token_kind, candidate.revision) if token_kind else None,
                              records=records)
        self._state = candidate
        return result

    def validate(self, context=_NO_CONTEXT):
        self._ensure_idle()
        self._validate(self._state)
        if context is not _NO_CONTEXT:
            if type(context) is not P05Context:
                raise ValueError("P05 requires explicit campaign context")
            context.__post_init__()
            s = self._state
            progress = bool(s.invitations or s.tests or s.hardware_serial or s.credit_open or s.credit_written or s.role or s.loan_request or s.complete or "P05_INTRO" in s.consumed)
            if progress and "PLAN_AGREED" not in context.flags:
                raise ValueError("P05 progress requires its campaign plan")
            if (s.complete or s.loan_request) and "VC01_RESOLVED" not in context.flags:
                raise ValueError("P05 loan requires external VC01 resolution")
            if (context.flags & FLAG_IDS) - self.flags:
                raise ValueError("Campaign claims unearned P05 progress")
            for owned in context.ownership:
                if not s.complete:
                    if owned.owner != "P05" or owned.room != GARAGE:
                        raise ValueError("Physical loan claimed before branch completion")
                elif owned.object_id == "pa_kit" and owned.owner == "P05" and owned.room != COURTYARD:
                    raise ValueError("Historical P05 PA staging conflicts with host ownership")
        return True

    @staticmethod
    def _validate(s):
        if type(s) is not _State:
            raise ValueError("Unknown state")
        serial_fields = ("revision", "hardware_serial", "credit_open", "credit_written", "role", "contest_request", "loan_request",
                         "loan_test", "loan_hardware", "complete", "completed_request", "completion_test", "completion_hardware")
        for name in serial_fields:
            _integer(getattr(s, name), 0, s.revision if name != "revision" else MAX_SERIAL)
        if type(s.connected) is not bool:
            raise ValueError("Connection must be boolean")
        _integer(s.source, 0, 1); _integer(s.aim, 0, 2); _integer(s.hint_level, 0, 3)
        if not s.hardware_serial and (s.connected or s.source or s.aim):
            raise ValueError("Hardware lacks its change receipt")
        for name in ("invitations", "active_invites", "tests", "sources", "pending_source", "consumed"):
            if type(getattr(s, name)) is not dict:
                raise ValueError("Receipt maps must be dictionaries")
        if not set(s.invitations) <= {"1", "2"} or set(s.active_invites) != set(s.invitations):
            raise ValueError("Unknown or missing listener invitation")
        for key, serial in s.invitations.items():
            _integer(serial, 1, s.revision)
            if type(s.active_invites[key]) is not bool:
                raise ValueError("Invitation active state must be boolean")
        if not set(s.tests) <= set(s.invitations):
            raise ValueError("Test lacks invitation")
        test_serials = []
        for key, receipt in s.tests.items():
            if type(receipt) is not dict or set(receipt) != {"serial", "invitation", "hardware"}:
                raise ValueError("Malformed test receipt")
            for value in receipt.values():
                _integer(value, 1, s.revision)
            if receipt["invitation"] != s.invitations[key] or not receipt["invitation"] < receipt["serial"] or not receipt["hardware"] < receipt["serial"]:
                raise ValueError("Test receipt does not match invited listener or hardware ordering")
            if receipt["hardware"] > s.hardware_serial:
                raise ValueError("Test hardware is from the future")
            if receipt["hardware"] == s.hardware_serial and not (s.connected and s.source == Source.MIC and s.aim == int(key)):
                raise ValueError("Unchanged tested hardware contradicts its soundcheck")
            test_serials.append(receipt["serial"])
        if len({r["hardware"] for r in s.tests.values()}) != len(s.tests):
            raise ValueError("Different listener aims require distinct hardware receipts")
        if len(set(test_serials)) != len(test_serials):
            raise ValueError("Distinct tests cannot share a receipt")
        first_test = min(test_serials, default=0)
        if s.credit_open and (not first_test or s.credit_open <= first_test or s.credit_written or s.loan_request or s.complete
                              or not (s.connected and s.source == Source.MIC and str(s.aim) in s.tests)
                              or s.hardware_serial >= s.credit_open):
            raise ValueError("Invalid open credit interaction")
        if s.credit_written and (not first_test or s.credit_written <= first_test):
            raise ValueError("Credit lacks prior soundcheck")
        if s.role and not 0 < s.credit_written < s.role:
            raise ValueError("Role lacks exact credited test")
        if s.contest_request and not (0 < s.role < s.contest_request == s.revision < MAX_SERIAL and not s.loan_request):
            raise ValueError("Invalid pending external contest request")
        if s.loan_request:
            if not (s.role < s.loan_request and s.role and s.loan_test in test_serials
                    and s.loan_test < s.loan_request and s.loan_hardware == s.hardware_serial
                    and s.connected and s.source == Source.MIC and str(s.aim) in s.tests
                    and s.tests[str(s.aim)]["serial"] == s.loan_test and not s.complete
                    and s.loan_request == s.revision and s.revision < MAX_SERIAL):
                raise ValueError("Invalid current loan transaction")
        elif s.loan_test or s.loan_hardware:
            raise ValueError("Orphaned loan receipts")
        if s.complete:
            if not (0 < s.role < s.completed_request < s.complete
                    and s.completion_test in test_serials and s.completion_test < s.completed_request
                    and 0 < s.completion_hardware < s.completed_request
                    and s.completion_hardware <= s.hardware_serial):
                raise ValueError("Completion lacks ordered practical/role/host receipts")
            completed_listener = next(key for key, value in s.tests.items() if value["serial"] == s.completion_test)
            if s.tests[completed_listener]["hardware"] > s.completion_hardware:
                raise ValueError("Completion hardware predates its successful test")
            if s.hardware_serial == s.completion_hardware and not (s.connected and s.source == Source.MIC and s.aim == int(completed_listener)):
                raise ValueError("Unchanged completed hardware cannot contradict loan")
        elif s.completed_request or s.completion_test or s.completion_hardware:
            raise ValueError("Orphaned completion receipts")
        if not set(s.sources) <= set(SOURCE_BINDINGS):
            raise ValueError("Unknown observed source")
        for key, serial in s.sources.items():
            _integer(serial, 1, s.revision)
            if key == "equipment_credit_slate" and not 0 < s.credit_written < serial:
                raise ValueError("Read slate predates written credit")
        if s.pending_source:
            p = s.pending_source
            if (set(p) != {"serial", "source", "record_id", "room"} or type(p["source"]) is not str
                    or p["source"] not in SOURCE_BINDINGS or p["record_id"] != SOURCE_BINDINGS[p["source"]]
                    or type(p["room"]) is not str or p["room"] not in ROOMS or p["source"] in s.sources):
                raise ValueError("Invalid pending readable source")
            _integer(p["serial"], 1, s.revision)
            if p["source"] == "equipment_credit_slate" and not 0 < s.credit_written < p["serial"]:
                raise ValueError("Pending slate predates credit")
        if not set(s.consumed) <= ONCE_IDS:
            raise ValueError("Unknown one-shot receipt")
        for value in s.consumed.values():
            _integer(value, 1, s.revision)
        for id, serial in (("P05_CREDIT", s.credit_written), ("P05_ROLE", s.role), ("P05_COMPLETE", s.complete)):
            if s.consumed.get(id, 0) != serial:
                raise ValueError("Missing/mismatched one-shot receipt")
        for key, id in (("1", "P05_FEEDBACK_BUNNY"), ("2", "P05_FEEDBACK_AUDIENCE")):
            if s.consumed.get(id, 0) != s.tests.get(key, {}).get("serial", 0):
                raise ValueError("Feedback receipt must match actual listener test")
        if s.consumed.get("LAF05", 0) != first_test:
            raise ValueError("One-time success cue must match first successful test")
        if s.consumed.get("AUD_SOUNDTEST", 0) != s.tests.get("2", {}).get("serial", 0):
            raise ValueError("Audience cue must match audience test exactly")
        # Every known use of one hardware commit must describe one configuration,
        # including historical loan snapshots after later physical edits.
        hardware_signatures = {}
        def bind_hardware(serial, signature):
            if serial:
                previous = hardware_signatures.setdefault(serial, signature)
                if previous != signature:
                    raise ValueError("Conflicting signatures for one hardware receipt")
        bind_hardware(s.hardware_serial, (s.connected, s.source, s.aim))
        for key, receipt in s.tests.items():
            bind_hardware(receipt["hardware"], (True, Source.MIC.value, int(key)))
        for hardware, tested in ((s.loan_hardware, s.loan_test), (s.completion_hardware, s.completion_test)):
            if hardware:
                listener = next(int(key) for key, value in s.tests.items() if value["serial"] == tested)
                bind_hardware(hardware, (True, Source.MIC.value, listener))
        nonhardware = [s.credit_open, s.credit_written, s.role, s.contest_request, s.loan_request, s.complete,
                       s.completed_request, s.consumed.get("P05_INTRO", 0), s.pending_source.get("serial", 0),
                       *s.invitations.values(), *test_serials, *s.sources.values()]
        hardware_refs = {s.hardware_serial, s.loan_hardware, s.completion_hardware,
                         *(receipt["hardware"] for receipt in s.tests.values())} - {0}
        if hardware_refs & set(nonhardware):
            raise ValueError("Hardware receipts cannot alias known non-hardware commits")
        primary = [s.hardware_serial, s.credit_open, s.credit_written, s.role, s.contest_request, s.loan_request,
                   s.complete, s.completed_request, s.consumed.get("P05_INTRO", 0),
                   s.pending_source.get("serial", 0), *s.invitations.values(), *test_serials, *s.sources.values()]
        primary = [x for x in primary if x]
        if len(primary) != len(set(primary)):
            raise ValueError("Unrelated commits cannot share a receipt")

    def save(self):
        self.validate()
        return {"kind": SAVE_KIND, "schema": SAVE_SCHEMA, "state": deepcopy(asdict(self._state))}

    @classmethod
    def load(cls, data, context=None):
        if type(data) is not dict or set(data) != {"kind", "schema", "state"}:
            raise ValueError("Malformed P05 save envelope")
        if type(data["kind"]) is not str or data["kind"] != SAVE_KIND or type(data["schema"]) is not int or data["schema"] != SAVE_SCHEMA:
            raise ValueError("Incompatible P05 save")
        state = data["state"]
        if type(state) is not dict or set(state) != set(_State.__dataclass_fields__):
            raise ValueError("Unknown or missing saved P05 field")
        result = cls(); result._state = _State(**deepcopy(state))
        result.validate() if context is None else result.validate(context)
        return result

    def to_json(self):
        return json.dumps(self.save(), sort_keys=True, separators=(",", ":"))

    @classmethod
    def from_json(cls, text, context=None):
        if type(text) is not str or len(text.encode("utf-8")) > 65536:
            raise ValueError("Expected bounded JSON save text")
        def unique_pairs(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError("Duplicate JSON key")
                result[key] = value
            return result
        def reject_constant(value):
            raise ValueError("Non-finite JSON number")
        try:
            data = json.loads(text, object_pairs_hook=unique_pairs, parse_constant=reject_constant)
        except (RecursionError, UnicodeError) as exc:
            raise ValueError("Malformed bounded JSON save") from exc
        return cls.load(data, context)

    def restore(self, data, context=None):
        """Validate first; failure leaves state AND live callback session unchanged."""
        self._ensure_idle()
        candidate = type(self).load(data, context)
        self._state, self._session = candidate._state, candidate._session
        return self._result("restored")

    def object_location(self, context, obj):
        self.validate(context)
        if type(obj) is not str:
            raise ValueError("Object IDs are strings")
        if obj in ("bunny", "milo"):
            return getattr(context, obj + "_room")
        root = "pa_kit" if obj in KIT_PARTS or obj == "microphone_cable" else obj
        override = next((x for x in context.ownership if x.object_id == root), None)
        if override:
            return override.room if override.owner == "P05" else None
        if root == "pa_kit":
            return COURTYARD if self._state.complete else GARAGE
        if root in {"handcart", "marked_listening_position", "audience"}:
            return GARAGE
        return None

    def _blocked(self, context, *, room=None, obj=None, milo=False, allow_apron=False, preparation=True):
        self.validate(context)
        if preparation and "PLAN_AGREED" not in context.flags:
            return self._result("plan_required")
        if context.contest_active:
            return self._result("contest_active")
        if context.on_apron and not allow_apron:
            return self._result("return_from_apron")
        if room is not None and context.room != room:
            return self._result("offscreen")
        if obj is not None and self.object_location(context, obj) != context.room:
            return self._result("offscreen")
        if milo and context.milo_room != context.room:
            return self._result("milo_absent")
        return None

    def introduce(self, context):
        blocked = self._blocked(context, room=GARAGE, obj="pa_kit", milo=True)
        if blocked: return blocked
        if "P05_INTRO" in self._state.consumed or self._state.complete or self._state.hardware_serial:
            return self._result("intro_already_seen_or_setup_changed")
        return self._commit("introduced", lambda s, n: s.consumed.update(P05_INTRO=n), "intro",
                            notices=(("P05_INTRO", "presentation", {}),))

    def look(self, context, obj):
        blocked = self._blocked(context, obj=obj, preparation=False)
        if blocked: return blocked
        return self._result("inspect", obj) if obj in OBJECTS else self._result("inspect_state")

    def read_source(self, context, source):
        if type(source) is not str or source not in SOURCE_BINDINGS:
            raise ValueError("Unknown readable source")
        blocked = self._blocked(context, obj=source, preparation=False)
        if blocked: return blocked
        if source == "equipment_credit_slate" and not self._state.credit_written:
            return self._result("credit_blank")
        if source in self._state.sources:
            return self._result("source_already_observed", records=(SOURCE_BINDINGS[source],))
        p = self._state.pending_source
        if p and p["source"] == source and p["room"] == context.room:
            return self._result("source_pending", token=self._token("source", p["serial"]), records=(p["record_id"],))
        def change(s, n):
            s.pending_source = {"serial": n, "source": source, "record_id": SOURCE_BINDINGS[source], "room": context.room}
        return self._commit("source_pending", change, token_kind="source", records=(SOURCE_BINDINGS[source],))

    def acknowledge_source(self, context, source, record_id, token):
        if type(source) is not str or source not in SOURCE_BINDINGS or type(record_id) is not str or record_id != SOURCE_BINDINGS[source]:
            raise ValueError("Wrong exact source/record binding")
        blocked = self._blocked(context, obj=source, preparation=False)
        if blocked: return blocked
        p = self._state.pending_source
        if not (p and p["source"] == source and p["room"] == context.room and self._matches(token, "source", p["serial"])):
            return self._result("stale_source")
        def change(s, n):
            s.sources[source] = n; s.pending_source = {}
        return self._commit("source_observed", change, notices=(("P05_SOURCE_OBSERVED", "knowledge", {"source": source, "record_id": record_id}),))

    def journal_records(self):
        return tuple(rid for source, rid in SOURCE_BINDINGS.items() if source in self._state.sources)

    def cancel_source(self, context, token):
        self.validate(context)
        p = self._state.pending_source
        if not p or not self._matches(token, "source", p["serial"]): return self._result("stale_source")
        return self._commit("source_cancelled", lambda s, n: setattr(s, "pending_source", {}))

    def invite_listener(self, context, listener):
        listener = _choice(listener, Listener); key = str(listener)
        if listener == Listener.BUNNY:
            blocked = self._blocked(context, room=context.bunny_room)
        else:
            blocked = self._blocked(context, room=GARAGE, allow_apron=True)
            if not blocked and (not context.on_apron or not context.audience_present):
                return self._result("audience_invitation_requires_apron")
        if blocked: return blocked
        if self._state.active_invites.get(key): return self._result("already_invited")
        if self._state.complete: return self._result("already_borrowed")
        def change(s, n):
            s.invitations.setdefault(key, n); s.active_invites[key] = True
        data = {"listener": listener, "from_room": context.room, "destination": GARAGE,
                "visible_escort_required": listener == Listener.BUNNY, "host_owns_positions": True}
        return self._commit("listener_invited", change, "invite_bunny" if listener == Listener.BUNNY else "invite_audience",
                            notices=(("P05_INVITE", "listener_request", data),))

    def dismiss_listener(self, context, listener):
        listener = _choice(listener, Listener); key = str(listener)
        blocked = self._blocked(context, room=GARAGE, allow_apron=listener == Listener.AUDIENCE)
        if blocked: return blocked
        if not self._state.active_invites.get(key): return self._result("not_invited")
        return self._commit("listener_dismissed", lambda s, n: s.active_invites.update({key: False}),
                            notices=(("P05_RETURN_LISTENER", "listener_return_request", {"listener": listener, "host_owns_positions": True}),))

    @staticmethod
    def _cancel_interactions(s):
        s.credit_open = 0; s.loan_request = s.loan_test = s.loan_hardware = 0

    def _hardware(self, context, field, value, code, binding=None):
        blocked = self._blocked(context, obj="pa_kit")
        if blocked: return blocked
        if getattr(self._state, field) == value: return self._result("unchanged")
        if self._state.loan_request: return self._result("handoff_in_progress")
        def change(s, n):
            setattr(s, field, value); s.hardware_serial = n; self._cancel_interactions(s)
        return self._commit(code, change, *((binding,) if binding else ()),
                            notices=(("P05_HARDWARE", "hardware", {"field": field, "value": value}),))

    def connect_microphone(self, context, socket="mic_socket"):
        if type(socket) is not str: raise ValueError("Socket must be an object ID")
        blocked = self._blocked(context, obj="pa_kit")
        if blocked: return blocked
        if socket != "mic_socket": return self._result("wrong_socket", "wrong_socket")
        return self._hardware(context, "connected", True, "microphone_connected", "connect")

    def disconnect_microphone(self, context):
        return self._hardware(context, "connected", False, "microphone_disconnected")

    def select_source(self, context, source):
        source = _choice(source, Source)
        return self._hardware(context, "source", source, "source_selected", "mic" if source == Source.MIC else None)

    def aim_speaker(self, context, listener):
        blocked = self._blocked(context, room=GARAGE, obj="pa_kit")
        if blocked: return blocked
        if type(listener) is int and listener == 0:
            aim = 0  # explicit away position; NEW design for reversible testing
        else: aim = _choice(listener, Listener)
        return self._hardware(context, "aim", aim, "speaker_aimed", "aim" if aim else None)

    def test_microphone(self, context, listener, *, complete_sentence=True):
        listener = _choice(listener, Listener); key = str(listener)
        if type(complete_sentence) is not bool: raise ValueError("Sentence choice is explicit, not audio completion")
        blocked = self._blocked(context, room=GARAGE, obj="pa_kit", milo=True)
        if blocked: return blocked
        s = self._state
        if not s.active_invites.get(key): return self._result("listener_not_invited")
        if (listener == Listener.BUNNY and context.bunny_room != GARAGE) or (listener == Listener.AUDIENCE and not context.audience_present):
            return self._result("listener_absent")
        if not complete_sentence: return self._result("complete_sentence_required", "test_choice")
        if not s.connected: return self._result("microphone_unplugged")
        if s.source != Source.MIC: return self._result("mic_source_required")
        if s.aim != listener:
            return self._result("speaker_wrong_direction", "sentence", "bunny_unclear" if listener == Listener.BUNNY else "audience_unclear")
        if key in s.tests: return self._result("already_tested")
        cue = "P05_FEEDBACK_BUNNY" if listener == Listener.BUNNY else "P05_FEEDBACK_AUDIENCE"
        first = not s.tests
        def change(state, n):
            state.tests[key] = {"serial": n, "invitation": state.invitations[key], "hardware": state.hardware_serial}
            state.consumed[cue] = n
            if first: state.consumed["LAF05"] = n
            if listener == Listener.AUDIENCE: state.consumed["AUD_SOUNDTEST"] = n
        notices = [(cue, "practical_test", {"listener": listener})]
        if first: notices.append(("LAF05", "optional_success_cue", {"not_a_correctness_detector": True}))
        if listener == Listener.AUDIENCE: notices.append(("AUD_SOUNDTEST", "optional_success_cue", {"caption_required": True}))
        return self._commit("soundcheck_passed", change, "sentence", "bunny_clear" if listener == Listener.BUNNY else "audience_clear", notices=tuple(notices))

    def begin_credit(self, context):
        blocked = self._blocked(context, obj="equipment_credit_slate", milo=True)
        if blocked: return blocked
        if not self._state.tests: return self._result("test_required")
        if self._state.credit_written: return self._result("credit_already_written")
        if not self.current_hardware_working: return self._result("working_hardware_required")
        if "grease_pencil" not in context.inventory: return self._result("pencil_required")
        if self._state.credit_open:
            return self._result("credit_open", "credit_choice", token=self.credit_token)
        return self._commit("credit_open", lambda s, n: setattr(s, "credit_open", n), "credit_choice", token_kind="credit")

    def select_credit(self, context, credit_id, token=None):
        if type(credit_id) is not str: raise ValueError("Credit choice must be a stable ID")
        blocked = self._blocked(context, obj="equipment_credit_slate", milo=True)
        if blocked: return blocked
        if token is not None and not self._matches(token, "credit", self._state.credit_open): return self._result("stale_credit")
        if not self._state.credit_open: return self._result("credit_not_open")
        if "grease_pencil" not in context.inventory: return self._result("pencil_required")
        if not self.current_hardware_working: return self._result("working_hardware_required")
        if credit_id != CREDIT_ID: return self._result("inaccurate_credit")
        def change(s, n):
            s.credit_written = n; s.credit_open = 0; s.consumed["P05_CREDIT"] = n
        return self._commit("credit_written", change, "credit", notices=(("P05_CREDIT", "credit", {"choice_id": CREDIT_ID}),))

    def cancel_credit(self, context, token=None):
        self.validate(context)
        if token is not None and not self._matches(token, "credit", self._state.credit_open): return self._result("stale_credit")
        if not self._state.credit_open: return self._result("credit_not_open")
        return self._commit("credit_cancelled", lambda s, n: setattr(s, "credit_open", 0))

    def agree_role(self, context):
        blocked = self._blocked(context, obj="equipment_credit_slate", milo=True)
        if blocked: return blocked
        if self._state.role: return self._result("role_already_agreed")
        if not self._state.credit_written: return self._result("credit_required")
        if not self.current_hardware_working: return self._result("working_hardware_required")
        def change(s, n): s.role = n; s.consumed["P05_ROLE"] = n
        return self._commit("role_agreed", change, "role", notices=(("P05_ROLE", "agreement", {"role": "greeter", "credit_id": CREDIT_ID}),))

    def flatter(self, context):
        blocked = self._blocked(context, milo=True)
        if blocked: return blocked
        return self._result("test_required", "flattery") if not self._state.tests else self._result("practical_state_unchanged")

    def contest_ready(self, context):
        blocked = self._blocked(context, milo=True)
        if blocked: return blocked
        return self._result("contest_terms_ready") if self._state.role else self._result("contest_not_ready", "contest_not_ready")

    def request_contest(self, context: P05Context) -> P05Result:
        """Request external VC01 introduction/rematch; never scores or teaches."""
        blocked = self._blocked(context, milo=True)
        if blocked: return blocked
        if not self._state.role:
            return self._result("contest_not_ready", "contest_not_ready")
        if self._state.loan_request:
            return self._result("handoff_in_progress")
        if self._state.contest_request:
            return self._result("contest_request_pending")
        if self.revision >= MAX_SERIAL - 1:
            return self._result("serial_exhausted")
        record = "VC01.REMATCH" if "VC01_RESOLVED" in context.flags else "VC01.ENTRY"
        return self._commit("contest_requested", lambda s, n: setattr(s, "contest_request", n),
                            records=(record,), notices=(("P05_CONTEST_REQUEST", "external_contest_request", {
                                "encounter_id": "VC01", "opponent": "milo", "room": context.room}),))

    def acknowledge_contest_request(self, serial: int, *, cancelled: bool = False) -> P05Result:
        """Host-only ACK of the external request, not a contest result receipt.

        The witnessed integer signature is retained. Its NEW ticket contains a
        runtime session plus the bounded saved receipt, so old-load callbacks
        cannot accidentally clear a resumed request with the same saved serial.
        """
        self.validate()
        _integer(serial, 1, (1 << 160) - 1)
        if type(cancelled) is not bool:
            raise ValueError("Contest cancellation must be explicit boolean")
        pending = self.pending_request
        if pending is None or serial != pending.serial:
            return self._result("stale_contest_request")
        code = "contest_request_cancelled" if cancelled else "contest_request_acknowledged"
        return self._commit(code, lambda s, n: setattr(s, "contest_request", 0),
                            notices=(("P05_CONTEST_REQUEST_ACK", "external_contest_ack", {
                                "encounter_id": "VC01", "cancelled": cancelled,
                                "request_receipt": pending.receipt_serial}),))

    def borrow_kit(self, context):
        blocked = self._blocked(context, room=GARAGE, milo=True)
        if blocked: return blocked
        if self._state.complete: return self._result("already_borrowed")
        if self._state.contest_request: return self._result("contest_request_pending")
        if not self._state.role: return self._result("practical_terms_required")
        if "VC01_RESOLVED" not in context.flags: return self._result("contest_resolution_required", "need_resolution")
        if not self.current_hardware_working: return self._result("working_hardware_required")
        if self._state.loan_request:
            return self._result("handoff_pending", "loan", token=self._token("loan", self._state.loan_request))
        if self.revision >= MAX_SERIAL - 1:
            return self._result("serial_exhausted")
        def change(s, n):
            s.loan_request = n; s.loan_test = s.tests[str(s.aim)]["serial"]; s.loan_hardware = s.hardware_serial
        return self._commit("handoff_pending", change, "loan", token_kind="loan",
                            notices=(("P05_LOAN_REQUEST", "ownership_transaction", {"handoff_id": "P05:LOAN", "objects": ("pa_kit", "handcart")}),))

    def acknowledge_handoff(self, context, token, objects):
        """Trusted host-only receipt AFTER atomic visible movement; never audio/queue end."""
        self.validate(context)
        if not self._matches(token, "loan", self._state.loan_request): return self._result("stale_handoff")
        if context.on_apron or context.contest_active: return self._result("host_transaction_blocked")
        expected = (OwnedObject("pa_kit", "P05", COURTYARD), OwnedObject("handcart", "P05", GARAGE))
        if type(objects) is not tuple or objects != expected:
            raise ValueError("Host must acknowledge exact PA staging and visible garage cart")
        if self.revision == MAX_SERIAL: return self._result("serial_exhausted")
        def change(s, n):
            s.complete = n; s.completed_request = s.loan_request; s.completion_test = s.loan_test
            s.completion_hardware = s.loan_hardware; s.consumed["P05_COMPLETE"] = n
            s.loan_request = s.loan_test = s.loan_hardware = 0
        return self._commit("sound_ready", change, "complete", notices=(("P05_COMPLETE", "puzzle", {"handoff_id": "P05:LOAN", "objects": tuple(asdict(x) for x in expected), "preserve": ("microphone_cable", "grease_pencil")}),))

    def cancel_handoff(self, context, token):
        """Host must cancel/roll back its uncommitted physical transaction first."""
        self.validate(context)
        if not self._matches(token, "loan", self._state.loan_request): return self._result("stale_handoff")
        def change(s, n): s.loan_request = s.loan_test = s.loan_hardware = 0
        return self._commit("handoff_cancelled", change)

    def hint(self, context, level):
        _integer(level, 1, 3)
        blocked = self._blocked(context, allow_apron=True)
        if blocked: return blocked
        binding = "need_resolution" if self._state.role and "VC01_RESOLVED" not in context.flags else f"hint_{level}"
        if level <= self._state.hint_level: return self._result("hint", binding)
        return self._commit("hint", lambda s, n: setattr(s, "hint_level", level), binding)
