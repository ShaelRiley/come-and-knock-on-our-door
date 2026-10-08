"""P10 reusable service cues; scene rendering and campaign ownership are external.

Only canonical record/unit IDs are returned. Queuing, hints and pure reads are
not evidence of displayed text. The small caption ledger is shared with P11.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from typing import Any, ClassVar, Mapping
from uuid import uuid4

from .model import Event, Result, Verb
from .p02_model import ROOMS
from .p03_model import TILE_IDS

SAVE_KIND = "cakood-p10-branch"
SAVE_SCHEMA = 1
LIVING = "L01_LIVING_ROOM"
KITCHEN = "L02_KITCHEN"
COURTYARD = "L05_COURTYARD"
CONSERVATORY = "L07_CONSERVATORY"
ORDER = ("SERVE", "SHOW", "TOAST")
PAPER_IDS = tuple(f"master_invitation_cue_{i}" for i in range(1, 4))
CUE_IDS = (*TILE_IDS, *PAPER_IDS)
FIXED_OBJECTS = frozenset(("board", "tray", "cue_rack", "rack_spring_clips", "audience",
                          "jack", "bunny", "frankie", "rita", "milo", "felix", "vivian", "stringer"))
LABEL_IDS = {"ceramic_sample_tiles": "P10.LABEL.001", "cue_rack": "P10.LABEL.002"}
CHOICE_IDS = dict(zip(ORDER, (f"P10.CHOICE.{i:03}" for i in range(1, 4))))
RECORD_UNITS = {'P10.CHOICE.001': (),
 'P10.CHOICE.002': (),
 'P10.CHOICE.003': (),
 'P10.DIALOGUE.001': ('P10.DIALOGUE.001.01', 'P10.DIALOGUE.001.02'),
 'P10.DIALOGUE.002': ('P10.DIALOGUE.002.01', 'P10.DIALOGUE.002.02'),
 'P10.FAILURE.001': ('P10.FAILURE.001.01',),
 'P10.FAILURE.002': ('P10.FAILURE.002.01',),
 'P10.FAILURE.003': ('P10.FAILURE.003.01',),
 'P10.HINT.1': (),
 'P10.HINT.2': (),
 'P10.HINT.3': (),
 'P10.LABEL.001': (),
 'P10.LABEL.002': (),
 'P10.LOOK.001': ('P10.LOOK.001.01',),
 'P10.LOOK.002': ('P10.LOOK.002.01',),
 'P10.LOOK.003': ('P10.LOOK.003.01',),
 'P10.OPEN.001': ('P10.OPEN.001.01',
                  'P10.OPEN.001.02',
                  'P10.OPEN.001.03',
                  'P10.OPEN.001.04',
                  'P10.OPEN.001.05',
                  'P10.OPEN.001.06'),
 'P10.READ.001': (),
 'P10.READ.002': (),
 'P10.SUCCESS.001': ('P10.SUCCESS.001.01',),
 'P10.SUCCESS.002': ('P10.SUCCESS.002.01',),
 'P10.SUCCESS.003': ('P10.SUCCESS.003.01',),
 'P10.SUCCESS.004': ('P10.SUCCESS.004.01',)}
UNIT_SPEAKERS = {'P10.DIALOGUE.001.01': 'jack',
 'P10.DIALOGUE.001.02': 'rita',
 'P10.DIALOGUE.002.01': 'jack',
 'P10.DIALOGUE.002.02': 'bunny',
 'P10.FAILURE.001.01': 'bunny',
 'P10.FAILURE.002.01': 'jack',
 'P10.FAILURE.003.01': 'frankie',
 'P10.LOOK.001.01': 'jack',
 'P10.LOOK.002.01': 'jack',
 'P10.LOOK.003.01': 'jack',
 'P10.OPEN.001.01': 'jack',
 'P10.OPEN.001.02': 'bunny',
 'P10.OPEN.001.03': 'jack',
 'P10.OPEN.001.04': 'bunny',
 'P10.OPEN.001.05': 'jack',
 'P10.OPEN.001.06': 'bunny',
 'P10.SUCCESS.001.01': 'jack',
 'P10.SUCCESS.002.01': 'jack',
 'P10.SUCCESS.003.01': 'jack',
 'P10.SUCCESS.004.01': 'jack'}


@dataclass(frozen=True)
class P10Context:
    room: str
    on_apron: bool = False
    flags: frozenset[str] = frozenset()
    inventory: frozenset[str] = frozenset()
    bunny_room: str = LIVING
    frankie_room: str = LIVING
    rita_room: str = CONSERVATORY
    contest_active: bool = False

    def __post_init__(self) -> None:
        if any(type(x) is not str or x not in ROOMS for x in
               (self.room, self.bunny_room, self.frankie_room, self.rita_room)):
            raise ValueError("Unknown campaign room")
        if any(type(x) is not bool for x in (self.on_apron, self.contest_active)):
            raise ValueError("Campaign modes must be boolean")
        for x in (self.flags, self.inventory):
            if type(x) is not frozenset or any(type(y) is not str for y in x):
                raise ValueError("Campaign facts must be frozen string sets")
        if self.inventory & (FIXED_OBJECTS | set(PAPER_IDS)):
            raise ValueError("Caller duplicates a fixed or P10-owned object")


@dataclass(frozen=True)
class CaptionResult(Result):
    code: str = ""
    line_ids: tuple[str, ...] = ()
    speech_unit_ids: tuple[str, ...] = ()
    presentation_id: str | None = None


P10Result = CaptionResult


@dataclass
class _Receipt:
    serial: int
    receipts: dict[str, int] = field(default_factory=dict)


@dataclass
class _Captioned:
    """A finite source ledger, with a fresh callback epoch after every load.

    Whole-record acknowledgments certify that every page was displayed. Unit
    acknowledgments certify only the exact contiguous speech prefix shown.
    """
    presentations: dict[str, _Receipt] = field(default_factory=dict)
    revision: int = 0
    _epoch: str = field(default_factory=lambda: uuid4().hex, init=False, repr=False, compare=False)
    PUZZLE: ClassVar[str]
    KIND: ClassVar[str]
    SOURCES: ClassVar[dict[str, str]]
    UNITS: ClassVar[dict[str, tuple[str, ...]]]
    SPEAKERS: ClassVar[dict[str, str]]

    def _tokens(self, source: str) -> tuple[str, ...]:
        record = self.SOURCES[source]
        return self.UNITS.get(record) or (record,)

    def _complete(self, source: str) -> bool:
        p = self.presentations.get(source)
        return p is not None and tuple(p.receipts) == self._tokens(source)

    def _handle(self, source: str) -> str:
        return f"{self.PUZZLE}:{self._epoch}:{source}:{self.presentations[source].serial}"

    def _result(self, code: str, *records: str) -> CaptionResult:
        self.validate()
        if any(r not in self.UNITS for r in records):
            raise ValueError("Unknown canonical record")
        return CaptionResult("", (), code, tuple(records))

    def _commit(self, code: str, event_id: str, kind: str = "object", *,
                records: tuple[str, ...] = (), **payload: Any) -> CaptionResult:
        self.revision += 1
        self.validate()
        return CaptionResult("", (Event(event_id, kind,
            {"serial": self.revision, "puzzle": self.PUZZLE, **payload}),), code, records)

    def _presentation_block(self, context: Any, source: str, tokens: tuple[str, ...]) -> CaptionResult | None:
        raise NotImplementedError

    def begin_presentation(self, context: Any, source: str) -> CaptionResult:
        if type(source) is not str or source not in self.SOURCES:
            raise ValueError("Unknown presentation source")
        block = self._presentation_block(context, source, self._tokens(source))
        if block is not None:
            return block
        if source in self.presentations:
            if self._complete(source):
                return self._result("presentation_complete", self.SOURCES[source])
            return self.resume_presentation(context, source)
        self.revision += 1
        self.presentations[source] = _Receipt(self.revision)
        shown = self.resume_presentation(context, source)
        return CaptionResult("", (Event(self.PUZZLE + "_PRESENTATION_QUEUED", "presentation",
            {"serial": self.revision, "puzzle": self.PUZZLE, "source": source}),),
            shown.code, shown.line_ids, shown.speech_unit_ids, shown.presentation_id)

    def resume_presentation(self, context: Any, source: str) -> CaptionResult:
        if type(source) is not str or source not in self.SOURCES:
            raise ValueError("Unknown presentation source")
        if source not in self.presentations:
            return self._result("presentation_not_started")
        p = self.presentations[source]
        remaining = self._tokens(source)[len(p.receipts):]
        if not remaining:
            return self._result("presentation_complete")
        block = self._presentation_block(context, source, remaining)
        if block is not None:
            return block
        self.validate()
        return CaptionResult("", (), "presentation_pending",
            (self.SOURCES[source],) if not p.receipts else (),
            remaining if p.receipts else (), self._handle(source))

    def acknowledge_presentation(self, context: Any, presentation_id: str, *,
            record_id: str | None = None, speech_unit_ids: tuple[str, ...] = ()) -> CaptionResult:
        if (type(presentation_id) is not str or type(speech_unit_ids) is not tuple
                or any(type(t) is not str for t in speech_unit_ids)
                or (record_id is not None and type(record_id) is not str)
                or (record_id is None) == (not speech_unit_ids)):
            raise ValueError("Acknowledge one whole displayed record or a speech-unit prefix")
        source = next((s for s in self.presentations if self._handle(s) == presentation_id), None)
        if source is None:
            return self._result("stale_presentation")
        if record_id is not None and record_id != self.SOURCES[source]:
            raise ValueError("Record does not belong to this presentation")
        p = self.presentations[source]
        expected = self._tokens(source)
        tokens = expected if record_id else speech_unit_ids
        if (not tokens or len(set(tokens)) != len(tokens)
                or any(t not in expected for t in tokens)
                or (record_id is None and any(t not in self.SPEAKERS for t in tokens))):
            raise ValueError("Receipt exceeds canonical text")
        indices = tuple(expected.index(t) for t in tokens)
        if indices != tuple(range(indices[0], indices[0] + len(indices))):
            raise ValueError("Speech receipts must be contiguous and in order")
        new = tuple(t for t in tokens if t not in p.receipts)
        if not new:
            return self._result("presentation_already_acknowledged")
        if new != expected[len(p.receipts):len(p.receipts) + len(new)]:
            raise ValueError("Earlier text has not been presented")
        block = self._presentation_block(context, source, new)
        if block is not None:
            return block
        self.revision += 1
        p.receipts.update({t: self.revision for t in new})
        self.validate()
        return CaptionResult("", (Event(self.PUZZLE + "_PRESENTED", "presentation",
            {"serial": self.revision, "puzzle": self.PUZZLE,
             "source": source, "canonical_tokens": new}),), "presentation_acknowledged")

    def journal_records(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(self.SOURCES[s] for s, p in sorted(
            self.presentations.items(), key=lambda item: item[1].serial) if self._complete(s)))

    def journal_units(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(t for _, p in sorted(self.presentations.items(),
            key=lambda item: item[1].serial) for t in p.receipts if t in self.SPEAKERS))

    def _validate_captions(self) -> None:
        if type(self.revision) is not int or self.revision < 0 or type(self.presentations) is not dict:
            raise ValueError("Invalid presentation ledger")
        operations: dict[int, str] = {}
        for source, p in self.presentations.items():
            if type(source) is not str or source not in self.SOURCES or type(p) is not _Receipt:
                raise ValueError("Unknown caption source")
            if type(p.serial) is not int or not 0 < p.serial <= self.revision or type(p.receipts) is not dict:
                raise ValueError("Invalid presentation serial")
            if p.serial in operations:
                raise ValueError("Duplicate source serial")
            operations[p.serial] = source + ":start"
            if tuple(p.receipts) != self._tokens(source)[:len(p.receipts)]:
                raise ValueError("Non-prefix caption receipts")
            prior = p.serial
            for token, serial in p.receipts.items():
                if type(serial) is not int or not p.serial < serial <= self.revision or serial < prior:
                    raise ValueError("Invalid receipt order")
                if serial in operations and operations[serial] != source:
                    raise ValueError("Unrelated operations share a serial")
                operations[serial] = source
                prior = serial

    def _validate_serials(self, *names: str) -> None:
        for name in names:
            x = getattr(self, name)
            if type(x) is not int or not 0 <= x <= self.revision:
                raise ValueError("Invalid " + name)

    def save(self) -> dict[str, Any]:
        self.validate()
        state = {k: v for k, v in asdict(self).items() if not k.startswith("_")}
        return {"kind": self.KIND, "schema": 1, "state": state}

    @classmethod
    def load(cls, data: Mapping[str, Any], *, context: Any = None):
        if (type(data) is not dict or set(data) != {"kind", "schema", "state"}
                or data["kind"] != cls.KIND or type(data["schema"]) is not int or data["schema"] != 1
                or type(data["state"]) is not dict):
            raise ValueError("Invalid branch save envelope")
        expected = {f.name for f in fields(cls) if not f.name.startswith("_")}
        raw = data["state"]
        if set(raw) != expected or type(raw.get("presentations")) is not dict:
            raise ValueError("Unknown or missing branch state")
        import copy
        state = copy.deepcopy(raw)
        for source, p in state["presentations"].items():
            if type(p) is not dict or set(p) != {"serial", "receipts"}:
                raise ValueError("Malformed caption receipt")
            state["presentations"][source] = _Receipt(**p)
        world = cls(**state)
        world.validate()
        if context is not None:
            world.validate_context(context)
        return world


@dataclass
class P10World(_Captioned):
    bread_at: int = 0
    paper_at: int = 0
    restored_at: int = 0
    labels: dict[str, str | None] = field(default_factory=lambda: dict.fromkeys(CUE_IDS))
    slots: list[str | None] = field(default_factory=lambda: [None, None, None])
    hint_level: int = 0
    PUZZLE: ClassVar[str] = "P10"
    KIND: ClassVar[str] = SAVE_KIND
    SOURCES: ClassVar[dict[str, str]] = {
        "intro": "P10.OPEN.001", "plan": "P10.READ.001", "notebook": "P10.READ.002",
        "tiles": "P10.LOOK.002", "rack": "P10.LOOK.003",
        "credit": "P10.DIALOGUE.001", "bread_agreement": "P10.DIALOGUE.002"}
    UNITS: ClassVar[dict[str, tuple[str, ...]]] = RECORD_UNITS
    SPEAKERS: ClassVar[dict[str, str]] = UNIT_SPEAKERS

    @property
    def ready(self) -> bool:
        return self.restored_at > 0

    @property
    def flags(self) -> frozenset[str]:
        return frozenset(("CUES_RESTORED",)) if self.ready else frozenset()

    @property
    def rack_correct(self) -> bool:
        return tuple(self.labels[x] if x else None for x in self.slots) == ORDER


    # NEW RECONSTRUCTION STARTS HERE. The bytes above are the recovered prefix.
    # These methods follow retained SCI methods/tests plus current canonical GDD.
    # No claim is made that this is the lost historical Python implementation.

    @property
    def inventory(self) -> tuple[str, ...]:
        return tuple(x for x in PAPER_IDS if self.paper_at and x not in self.slots)

    @property
    def reserved_external_items(self) -> frozenset[str]:
        return frozenset(x for x in self.slots if x in TILE_IDS)

    @property
    def cue_handoff(self) -> dict[str, Any] | None:
        if not self.ready:
            return None
        return dict(rack_id="cue_rack", location=COURTYARD, slots=tuple(self.slots),
                    words=tuple(self.labels[x] if x else None for x in self.slots),
                    correct_now=self.rack_correct, known_order=ORDER,
                    built_in_clips=True, editable=True, first_restored_serial=self.restored_at)

    def knows_order(self, context: P10Context) -> bool:
        self._require_context(context)
        return ("KNOW_CUE_ORDER" in context.flags or self._complete("plan")
                or self._complete("notebook"))

    def choices(self, context: P10Context) -> tuple[str, ...]:
        self.validate()
        return tuple(CHOICE_IDS.values()) if self.knows_order(context) else ()

    @staticmethod
    def _require_context(context: P10Context) -> None:
        if type(context) is not P10Context:
            raise ValueError("Expected P10 campaign context")
        context.__post_init__()

    def _base_block(self, context: P10Context, room: str | None = None) -> CaptionResult | None:
        self.validate()
        self._require_context(context)
        if "EVENING_STARTED" not in context.flags:
            return self._result("evening_required")
        if context.on_apron or (room is not None and context.room != room):
            return self._result("offscreen")
        if context.contest_active:
            return self._result("contest_active")
        return None

    def _presentation_block(self, context: P10Context, source: str,
                            tokens: tuple[str, ...]) -> CaptionResult | None:
        block = self._base_block(context, {"plan": LIVING, "rack": COURTYARD}.get(source))
        if block is not None:
            return block
        if source in ("intro", "bread_agreement") and not self.bread_at:
            return self._result("snacks_not_discovered")
        if source == "notebook" and not self.ready:
            return self._result("cues_not_restored")
        if source == "tiles" and not (set(TILE_IDS) & context.inventory or
                (context.room == COURTYARD and self.reserved_external_items)):
            return self._result("tiles_unavailable")
        if source == "credit" and not (self.ready and self.reserved_external_items):
            return self._result("tile_substitution_required")
        for token in tokens:
            actor = self.SPEAKERS.get(token)
            if actor in ("bunny", "frankie", "rita") and getattr(context, actor + "_room") != context.room:
                return self._result("speaker_absent")
        return None

    def introduce(self, context: P10Context) -> CaptionResult:
        block = self._base_block(context)
        if block is not None:
            return block
        if context.bunny_room != context.room or context.room not in (LIVING, KITCHEN, COURTYARD):
            return self._result("speaker_absent")
        events = ()
        if not self.bread_at:
            self.bread_at = self.revision + 1
            events = self._commit("bread_served", "P10_BREAD_SERVED", edible_only=True,
                                  tray_id="tray", consumed="bread_samples", plan_preserved=True).events
        result = self.begin_presentation(context, "intro")
        return CaptionResult(result.text, events + result.events, result.code,
                             result.line_ids, result.speech_unit_ids, result.presentation_id)

    def object_location(self, obj: str, context: P10Context) -> str | None:
        self._require_context(context)
        if type(obj) is not str:
            raise ValueError("Object identity must be a string")
        if obj in self.slots:
            return "cue_rack"
        if obj in self.inventory or obj in context.inventory:
            return "inventory"
        if obj in ("bunny", "frankie", "rita"):
            return getattr(context, obj + "_room")
        return {"board": LIVING, "tray": KITCHEN, "cue_rack": COURTYARD,
                "rack_spring_clips": COURTYARD}.get(obj)

    def look(self, context: P10Context, obj: str) -> CaptionResult:
        block = self._base_block(context)
        if block is not None:
            return block
        location = self.object_location(obj, context)
        if not (location in ("inventory", context.room) or
                location == "cue_rack" and context.room == COURTYARD):
            return self._result("offscreen")
        if obj == "board":
            return self._result("plan", "P10.READ.001")
        if obj in TILE_IDS:
            return self._result("tiles", "P10.LOOK.002")
        if obj in ("cue_rack", "rack_spring_clips"):
            return self._result("rack", "P10.LOOK.003")
        if obj == "tray" and self.bread_at:
            return self._result("crumbs", "P10.LOOK.001")
        return self._result("no_p10_description")

    def pick_up_tiles(self, context: P10Context) -> CaptionResult:
        block = self._base_block(context)
        if block is not None:
            return block
        if not set(TILE_IDS) <= context.inventory | self.reserved_external_items:
            return self._result("p03_tiles_required")
        return self._result("existing_tiles", "P10.SUCCESS.001")

    def prepare_paper(self, context: P10Context) -> CaptionResult:
        block = self._base_block(context)
        if block is not None:
            return block
        if self.paper_at:
            return self._result("paper_already_prepared", "P10.SUCCESS.004")
        if "master_invitation" not in context.inventory:
            return self._result("master_card_required")
        self.paper_at = self.revision + 1
        return self._commit("paper_prepared", "P10_PAPER_PREPARED", "inventory",
                            records=("P10.SUCCESS.004",), items=PAPER_IDS,
                            source="master_invitation", original_preserved=True, copies=1)

    def _cue_block(self, context: P10Context, cue: str) -> CaptionResult | None:
        if type(cue) is not str or cue not in CUE_IDS:
            raise ValueError("Unknown cue identity")
        block = self._base_block(context)
        if block is not None:
            return block
        if cue in self.slots:
            if context.room != COURTYARD:
                return self._result("offscreen")
        elif cue not in context.inventory and cue not in self.inventory:
            return self._result("cue_unavailable")
        return None

    def _restore_if_correct(self) -> bool:
        if self.bread_at and self.rack_correct and not self.ready:
            self.restored_at = self.revision + 1
            return True
        return False

    def write(self, context: P10Context, cue: str, word: str | None) -> CaptionResult:
        if word is not None and (type(word) is not str or word not in ORDER):
            raise ValueError("Unknown cue word")
        block = self._cue_block(context, cue)
        if block is not None:
            return block
        if "grease_pencil" not in context.inventory:
            return self._result("pencil_required")
        if word and not self.knows_order(context):
            return self._result("read_plan_required", "P10.READ.001")
        if self.labels[cue] == word:
            return self._result("label_unchanged")
        self.labels[cue] = word
        restored = self._restore_if_correct()
        return self._commit("cue_written", "P10_CUE_WRITTEN", records=("P10.SUCCESS.002",),
                            cue=cue, word=word, icon=word, restored_first_time=restored)

    @staticmethod
    def _require_slot(slot: int) -> None:
        if type(slot) is not int or not 0 <= slot < 3:
            raise ValueError("Unknown rack slot")

    def place(self, context: P10Context, cue: str, slot: int) -> CaptionResult:
        self._require_slot(slot)
        block = self._cue_block(context, cue)
        if block is not None:
            return block
        if context.room != COURTYARD:
            return self._result("offscreen")
        if not self.bread_at:
            return self._result("snacks_not_discovered")
        if self.slots[slot] == cue:
            return self._result("cue_already_placed")
        word = self.labels[cue]
        if word is None:
            return self._result("blank_cue", *(('P10.FAILURE.001',) if context.bunny_room == context.room else ()))
        if self.slots[slot] is not None:
            return self._result("remove_occupied_cue_first")
        origin = "inventory"
        if cue in self.slots:
            origin = "cue_rack"
            self.slots[self.slots.index(cue)] = None
        self.slots[slot] = cue
        restored = self._restore_if_correct()
        records = ("P10.SUCCESS.003",) if self.rack_correct else ()
        if word == "SHOW" and slot == 0:
            records = ("P10.FAILURE.002",)
        elif word == "TOAST" and slot != 2 and context.frankie_room == context.room:
            records = ("P10.FAILURE.003",)
        return self._commit("cue_placed", "P10_CUE_PLACED", "inventory_transfer", records=records,
                            item=cue, origin=origin, destination="cue_rack", slot=slot,
                            restored_first_time=restored)

    def remove(self, context: P10Context, slot: int) -> CaptionResult:
        self._require_slot(slot)
        block = self._base_block(context, COURTYARD)
        if block is not None:
            return block
        cue = self.slots[slot]
        if cue is None:
            return self._result("slot_empty")
        self.slots[slot] = None
        return self._commit("cue_removed", "P10_CUE_REMOVED", "inventory_transfer",
                            item=cue, origin="cue_rack", destination="inventory")

    def hint(self, context: P10Context, level: int) -> CaptionResult:
        if type(level) is not int or not 1 <= level <= 3:
            raise ValueError("Unknown hint level")
        block = self._base_block(context)
        if block is not None:
            return block
        records = (f"P10.HINT.{level}",)
        if level > self.hint_level:
            self.hint_level = level
            return self._commit("hint", "P10_HINT", "hint", records=records, level=level)
        return self._result("hint", *records)

    def act(self, context: P10Context, verb: Verb | str, obj: str,
            target: str | None = None) -> CaptionResult:
        verb = Verb(verb)
        if type(obj) is not str or (target is not None and type(target) is not str):
            raise ValueError("Object and topic identities must be strings")
        if verb == Verb.LOOK_AT:
            return self.look(context, obj)
        if verb == Verb.OPEN and obj in ("board", "notebook", "journal"):
            return self.begin_presentation(context, "plan" if obj == "board" else "notebook")
        if verb == Verb.PICK_UP and obj == "ceramic_sample_tiles":
            return self.pick_up_tiles(context)
        if verb == Verb.USE and obj == "master_invitation" and target == "cue_rack":
            return self.prepare_paper(context)
        if verb == Verb.TALK_TO and obj == "bunny":
            if target == "bread":
                return self.begin_presentation(context, "bread_agreement")
            if target == "cues":
                return self.introduce(context)
        if verb == Verb.TALK_TO and obj == "rita" and target == "credit":
            return self.begin_presentation(context, "credit")
        block = self._base_block(context)
        return block if block is not None else self._result("no_p10_action")

    def validate_context(self, context: P10Context) -> None:
        self.validate()
        self._require_context(context)
        if self.revision and "EVENING_STARTED" not in context.flags:
            raise ValueError("P10 progress requires the committed P08 evening")
        if "CUES_RESTORED" in context.flags and not self.ready:
            raise ValueError("Caller claims unearned cue restoration")
        if context.inventory & self.reserved_external_items:
            raise ValueError("Placed original tile also projected in campaign inventory")

    def validate(self) -> None:
        self._validate_captions()
        self._validate_serials("bread_at", "paper_at", "restored_at")
        if type(self.hint_level) is not int or not 0 <= self.hint_level <= 3:
            raise ValueError("Invalid hint level")
        if type(self.labels) is not dict or set(self.labels) != set(CUE_IDS):
            raise ValueError("Invalid cue label registry")
        if any(x is not None and (type(x) is not str or x not in ORDER) for x in self.labels.values()):
            raise ValueError("Invalid cue label")
        if type(self.slots) is not list or len(self.slots) != 3:
            raise ValueError("Invalid rack slots")
        if any(x is not None and (type(x) is not str or x not in CUE_IDS) for x in self.slots):
            raise ValueError("Invalid rack identity")
        occupied = [x for x in self.slots if x is not None]
        if len(occupied) != len(set(occupied)):
            raise ValueError("One cue occupies two slots")
        if occupied and not self.bread_at:
            raise ValueError("Rack installation predates snack discovery")
        if not self.paper_at and (any(self.labels[x] for x in PAPER_IDS) or set(occupied) & set(PAPER_IDS)):
            raise ValueError("Paper has not been prepared")
        if self.ready and not 0 < self.bread_at < self.restored_at:
            raise ValueError("Restoration predates snack discovery")
        if self.rack_correct and not self.ready:
            raise ValueError("Correct rack lacks restoration history")
        for source, receipt in self.presentations.items():
            if source in ("intro", "bread_agreement") and not 0 < self.bread_at < receipt.serial:
                raise ValueError("Caption predates snack discovery")
            if source in ("notebook", "credit") and not 0 < self.restored_at < receipt.serial:
                raise ValueError("Caption predates restoration")
