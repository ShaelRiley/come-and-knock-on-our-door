"""P09's chair investigation; campaign travel and the render barrier are external.

Queries are pure. Presentations retain exact canonical record/unit receipts,
including a pending completion caption after the unsigned card is granted.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from types import MappingProxyType
from typing import Any, Mapping

from .model import Event, Result, Verb
from .p02_model import ROOMS

SAVE_KIND = "cakood-p09-branch"
SAVE_SCHEMA = 1
CONSERVATORY = "L07_CONSERVATORY"
CARD = "renewal_repair_card"
FLAG_IDS = frozenset(("RUMOR_CLEARED", "TERMS_CARD_AVAILABLE"))
ONCE_IDS = frozenset(("P09_RUMOR", "P09_TERMS", "P09_SHARED_WISH"))
RUMOR_SOURCES = frozenset(("chairs", "direct_question", "front_context", "accusation"))
FIXED_OBJECTS = frozenset(("tagged_chairs", "chair_tag", "conservatory_front",
    "conservatory_side", "audience", "stringer", "rita", "jack", "bunny", "frankie",
    "milo", "vivian", "felix"))
LABEL_IDS = MappingProxyType({"tagged_chairs": "P09.LABEL.001", CARD: "P09.INVENTORY.001"})
SOURCE_BINDINGS = MappingProxyType({
    "intro": ("P09.OPEN.001",), "chair_tag": ("P09.READ.001",),
    "chairs": ("P09.LOOK.001",), "direct_question": ("P09.DIALOGUE.001",),
    "front_context": ("P09.DIALOGUE.001",), "accusation": ("P09.FAILURE.001",),
    "terms": ("P09.DIALOGUE.002", "P09.SUCCESS.001"),
    "shared_wish": ("P09.DIALOGUE.003",), "terms_card": ("P09.READ.002",),
})
SCRIPT_BINDINGS = MappingProxyType({
    **SOURCE_BINDINGS,
    "card_look": ("P09.LOOK.002", "P09.READ.002"),
    "direct_choice": ("P09.CHOICE.001",), "accusation_choice": ("P09.CHOICE.002",),
    "terms_choice": ("P09.CHOICE.003",), "shared_wish_choice": ("P09.CHOICE.004",),
    "tag_refusal": ("P09.FAILURE.002",),
    **{f"hint_{i}": (f"P09.HINT.{i}",) for i in range(1, 4)},
})
RECORD_UNITS = MappingProxyType({
    record: tuple(f"{record}.{i:02}" for i in range(1, count + 1))
    for record, count in (("P09.OPEN.001", 2), ("P09.LOOK.001", 1),
        ("P09.DIALOGUE.001", 3), ("P09.FAILURE.001", 2),
        ("P09.DIALOGUE.002", 5), ("P09.DIALOGUE.003", 4),
        ("P09.SUCCESS.001", 1), ("P09.LOOK.002", 1), ("P09.FAILURE.002", 1))
})
CLASS_CONTEXT_UNITS = frozenset(("P09.DIALOGUE.001.01", "P09.FAILURE.001.02"))


@dataclass(frozen=True)
class P09Context:
    room: str
    on_apron: bool = False
    flags: frozenset[str] = frozenset()
    inventory: frozenset[str] = frozenset()
    stringer_room: str = CONSERVATORY
    rita_room: str = CONSERVATORY
    conservatory_view: str = "front"
    contest_active: bool = False

    def __post_init__(self) -> None:
        if any(type(x) is not str or x not in ROOMS
               for x in (self.room, self.stringer_room, self.rita_room)):
            raise ValueError("Unknown campaign room")
        if type(self.on_apron) is not bool or type(self.contest_active) is not bool:
            raise ValueError("Campaign modes must be boolean")
        if type(self.conservatory_view) is not str or self.conservatory_view not in {"side", "front"}:
            raise ValueError("Use the side or front viewpoint of the existing L07 screen")
        for value in (self.flags, self.inventory):
            if type(value) is not frozenset or any(type(x) is not str for x in value):
                raise ValueError("Campaign facts must be frozen string sets")
        if self.inventory & (FIXED_OBJECTS | {CARD}):
            raise ValueError("Caller duplicates a P09 fixed or branch-owned object")


@dataclass(frozen=True)
class P09Result(Result):
    code: str = ""
    line_ids: tuple[str, ...] = ()
    speech_unit_ids: tuple[str, ...] = ()
    presentation_id: str | None = None


@dataclass
class Presentation:
    serial: int
    variant: str = "full"
    receipts: dict[str, int] = field(default_factory=dict)


def _record_tokens(record: str) -> tuple[str, ...]:
    return RECORD_UNITS.get(record, (record,))


def _tokens(source: str, presentation: Presentation) -> tuple[str, ...]:
    if source == "accusation" and presentation.variant == "stringer_only":
        return ("P09.FAILURE.001.01",)
    return tuple(token for record in SOURCE_BINDINGS[source] for token in _record_tokens(record))


@dataclass
class P09World:
    flags: set[str] = field(default_factory=set)
    presentations: dict[str, Presentation] = field(default_factory=dict)
    consumed: dict[str, int] = field(default_factory=dict)
    revision: int = 0
    hint_level: int = 0

    @property
    def rumor_cleared(self) -> bool:
        return "RUMOR_CLEARED" in self.flags

    @property
    def ready(self) -> bool:
        return "TERMS_CARD_AVAILABLE" in self.flags

    @property
    def inventory(self) -> tuple[str, ...]:
        return (CARD,) if self.ready else ()

    @property
    def terms_card_handoff(self) -> dict[str, Any] | None:
        return {"object_id": CARD, "location": "inventory", "signed": False,
                "repair_date": None, "signature_owner": "P14",
                "terms_record_id": "P09.READ.002"} if self.ready else None

    @property
    def class_context_known(self) -> bool:
        return any(CLASS_CONTEXT_UNITS & p.receipts.keys() for p in self.presentations.values())

    @property
    def pending_presentations(self) -> tuple[str, ...]:
        return tuple(source for source, p in sorted(self.presentations.items(), key=lambda x: x[1].serial)
                     if len(p.receipts) < len(_tokens(source, p))
                     and not (source == "intro" and self.rumor_cleared))

    def journal_records(self) -> tuple[str, ...]:
        """Only whole records already presented; never enlarge a partial quote."""
        records = []
        for source, p in sorted(self.presentations.items(), key=lambda x: x[1].serial):
            for record in SOURCE_BINDINGS[source]:
                if set(_record_tokens(record)) <= p.receipts.keys() and record not in records:
                    records.append(record)
        return tuple(records)

    def journal_units(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(token for _, p in sorted(self.presentations.items(), key=lambda x: x[1].serial)
                                   for token in p.receipts if token in {u for us in RECORD_UNITS.values() for u in us}))

    @staticmethod
    def _context(context: P09Context) -> None:
        if type(context) is not P09Context:
            raise ValueError("P09 requires explicit campaign context")

    @staticmethod
    def _source(source: str) -> None:
        if type(source) is not str or source not in SOURCE_BINDINGS:
            raise ValueError("Unknown P09 presentation source")

    def _result(self, code: str, *bindings: str) -> P09Result:
        self.validate()
        return P09Result("", (), code,
                         tuple(record for binding in bindings for record in SCRIPT_BINDINGS[binding]))

    def object_location(self, obj: str, context: P09Context | None = None) -> str | None:
        if type(obj) is not str:
            raise ValueError("Objects require stable string IDs")
        if context is not None:
            self._context(context)
        if obj in {"stringer", "rita"}:
            return getattr(context, obj + "_room") if context else None
        if obj in {"tagged_chairs", "chair_tag", "conservatory_front", "conservatory_side"}:
            return CONSERVATORY
        if obj == CARD and self.ready:
            return "inventory"
        return None

    def reachable(self, context: P09Context, obj: str) -> bool:
        self._context(context)
        if type(obj) is not str:
            raise ValueError("Objects require stable string IDs")
        return not context.on_apron and (obj in self.inventory or obj in context.inventory
                                        or self.object_location(obj, context) == context.room)

    def _base_block(self, context: P09Context, *, action: bool = True) -> P09Result | None:
        self._context(context)
        if "EVENING_STARTED" not in context.flags:
            return self._result("evening_required")
        if context.on_apron:
            return self._result("offscreen")
        if action and context.contest_active:
            return self._result("contest_active")
        return None

    def _presentation_block(self, context: P09Context, source: str,
                            tokens: tuple[str, ...]) -> P09Result | None:
        blocked = self._base_block(context)
        if blocked is not None:
            return blocked
        if source == "terms_card" or (source == "terms" and tokens == _record_tokens("P09.SUCCESS.001")):
            return None if self.ready else self._result("card_unavailable")
        if context.room != CONSERVATORY:
            return self._result("offscreen")
        if source == "intro" and context.conservatory_view != "side":
            return self._result("side_view_required")
        if source == "front_context" and context.conservatory_view != "front":
            return self._result("front_view_required")
        if source in {"intro", "direct_question", "front_context", "terms", "shared_wish"}:
            if context.stringer_room != CONSERVATORY:
                return self._result("speaker_absent")
        if source == "shared_wish" and context.rita_room != CONSERVATORY:
            return self._result("speaker_absent")
        if source == "accusation":
            if "P09.FAILURE.001.01" in tokens and context.stringer_room != CONSERVATORY:
                return self._result("speaker_absent")
            if "P09.FAILURE.001.02" in tokens and context.rita_room != CONSERVATORY:
                return self._result("speaker_absent")
        if source == "terms" and "PLAN_AGREED" not in context.flags:
            return self._result("plan_required")
        return None

    def look(self, context: P09Context, obj: str) -> P09Result:
        """A query never queues, acknowledges, or changes notebook knowledge."""
        self._context(context)
        if type(obj) is not str:
            raise ValueError("Objects require stable string IDs")
        if obj == "audience":
            return self._result("audience_has_no_p09_information")
        blocked = self._base_block(context, action=False)
        if blocked is not None:
            return blocked
        if not self.reachable(context, obj):
            return self._result("offscreen")
        binding = {"tagged_chairs": "chairs", "chair_tag": "chair_tag", CARD: "card_look"}.get(obj)
        return self._result("observed", *((binding,) if binding else ()))

    def topics(self, context: P09Context) -> P09Result:
        blocked = self._base_block(context, action=False)
        if blocked is not None:
            return blocked
        if context.room != CONSERVATORY or context.stringer_room != CONSERVATORY:
            return self._result("speaker_absent")
        bindings = ["direct_choice"]
        if not self.rumor_cleared:
            bindings.append("accusation_choice")
        if self.rumor_cleared and not self.ready and "PLAN_AGREED" in context.flags:
            bindings.append("terms_choice")
        if self.class_context_known and context.rita_room == CONSERVATORY:
            bindings.append("shared_wish_choice")
        return self._result("topics", *bindings)

    def begin_presentation(self, context: P09Context, source: str) -> P09Result:
        """Queue an exact source; acknowledge only after captions were displayed."""
        self._source(source)
        self._context(context)
        if source in self.presentations:
            return self.resume_presentation(context, source)
        variant = "stringer_only" if source == "accusation" and context.rita_room != CONSERVATORY else "full"
        p = Presentation(self.revision + 1, variant)
        tokens = _tokens(source, p)
        blocked = self._presentation_block(context, source, tokens)
        if blocked is not None:
            return blocked
        if source == "intro" and self.rumor_cleared:
            return self._result("rumor_already_cleared")
        if source == "terms" and not self.rumor_cleared:
            return self._result("rumor_context_required")
        if source == "shared_wish" and not self.class_context_known:
            return self._result("class_context_required")
        self.revision += 1
        self.presentations[source] = p
        result = self.resume_presentation(context, source)
        return P09Result(result.text, (Event("P09_PRESENTATION_QUEUED", "presentation",
            {"serial": self.revision, "puzzle": "P09", "source": source}),),
            result.code, result.line_ids, result.speech_unit_ids, result.presentation_id)

    def resume_presentation(self, context: P09Context, source: str) -> P09Result:
        self._source(source)
        self._context(context)
        if source not in self.presentations:
            return self._result("presentation_not_queued")
        if source == "intro" and self.rumor_cleared:
            return self._result("rumor_already_cleared")
        p = self.presentations[source]
        remaining = tuple(token for token in _tokens(source, p) if token not in p.receipts)
        if not remaining:
            return self._result("presentation_complete")
        next_record = next(record for record in SOURCE_BINDINGS[source] if remaining[0] in _record_tokens(record))
        tokens = tuple(token for token in _record_tokens(next_record) if token in remaining)
        blocked = self._presentation_block(context, source, tokens)
        if blocked is not None:
            return blocked
        self.validate()
        full = tokens == _record_tokens(next_record)
        return P09Result("", (), "presentation_pending", (next_record,) if full else (),
                         () if full else tokens, f"P09:{source}:{p.serial}")

    def acknowledge_presentation(self, context: P09Context, presentation_id: str,
                                 *, record_id: str | None = None,
                                 speech_unit_ids: tuple[str, ...] = ()) -> P09Result:
        """Acknowledge a full canonical record or an exact contiguous unit prefix.

        The caller certifies successful visible presentation. Skipping audio is
        fine; queuing text, an interrupted unseen page, or an unopened journal
        is not presentation. Out-of-order and cross-source receipts are rejected.
        """
        self._context(context)
        if (type(presentation_id) is not str or type(speech_unit_ids) is not tuple
                or any(type(x) is not str for x in speech_unit_ids)
                or (record_id is not None and type(record_id) is not str)
                or (record_id is None) == (not speech_unit_ids)
                or len(set(speech_unit_ids)) != len(speech_unit_ids)):
            raise ValueError("Acknowledge exactly one canonical record or nonempty speech-unit sequence")
        source = next((source for source, p in self.presentations.items()
                       if presentation_id == f"P09:{source}:{p.serial}"), None)
        if source is None:
            raise ValueError("Unknown or stale P09 presentation")
        p = self.presentations[source]
        expected = _tokens(source, p)
        if record_id is not None:
            if record_id not in SOURCE_BINDINGS[source]:
                raise ValueError("Record does not belong to this presentation")
            tokens = _record_tokens(record_id)
        else:
            tokens = speech_unit_ids
            if any(token not in {u for us in RECORD_UNITS.values() for u in us} for token in tokens):
                raise ValueError("Unknown canonical P09 speech unit")
        if any(token not in expected for token in tokens):
            raise ValueError("Receipt exceeds the queued canonical presentation")
        indices = [expected.index(token) for token in tokens]
        if indices != list(range(indices[0], indices[0] + len(indices))):
            raise ValueError("Speech receipts must be ordered and contiguous")
        new = tuple(token for token in tokens if token not in p.receipts)
        if not new:
            return self._result("presentation_already_acknowledged")
        if new != expected[len(p.receipts):len(p.receipts) + len(new)]:
            raise ValueError("An earlier canonical unit has not been presented")
        if source == "intro" and self.rumor_cleared:
            return self._result("rumor_already_cleared")
        # A single receipt cannot leap over the card grant into its outcome.
        if "P09.SUCCESS.001.01" in new and any(x.startswith("P09.DIALOGUE.002.") for x in new):
            raise ValueError("Acknowledge terms before presenting the completion outcome")
        blocked = self._presentation_block(context, source, new)
        if blocked is not None:
            return blocked
        self.revision += 1
        p.receipts.update({token: self.revision for token in new})
        events = [Event("P09_PRESENTED", "presentation", {"serial": self.revision,
            "puzzle": "P09", "source": source, "canonical_tokens": new})]
        if source in RUMOR_SOURCES and not self.rumor_cleared:
            self.flags.add("RUMOR_CLEARED")
            self.consumed["P09_RUMOR"] = self.revision
            events.append(Event("P09_RUMOR", "knowledge", {"serial": self.revision,
                "puzzle": "P09", "source": source, "flag": "RUMOR_CLEARED"}))
        if source == "terms" and set(RECORD_UNITS["P09.DIALOGUE.002"]) <= p.receipts.keys() and not self.ready:
            self.flags.add("TERMS_CARD_AVAILABLE")
            self.consumed["P09_TERMS"] = self.revision
            events.append(Event("P09_TERMS", "puzzle", {"serial": self.revision,
                "puzzle": "P09", "flag": "TERMS_CARD_AVAILABLE", **self.terms_card_handoff}))
        if source == "shared_wish" and len(p.receipts) == len(expected) and "P09_SHARED_WISH" not in self.consumed:
            self.consumed["P09_SHARED_WISH"] = self.revision
            events.append(Event("P09_SHARED_WISH", "dialogue", {"serial": self.revision,
                "puzzle": "P09", "optional": True}))
        result = self.resume_presentation(context, source)
        return P09Result("", tuple(events), "presentation_acknowledged", result.line_ids,
                         result.speech_unit_ids, result.presentation_id)

    def introduce(self, context: P09Context) -> P09Result:
        return self.begin_presentation(context, "intro")

    def inspect_chairs(self, context: P09Context) -> P09Result:
        return self.begin_presentation(context, "chairs")

    def ask_three_things(self, context: P09Context) -> P09Result:
        if "direct_question" in self.presentations and "direct_question" not in self.pending_presentations:
            blocked = self._presentation_block(context, "direct_question", ("P09.DIALOGUE.001.01",))
            if blocked is not None:
                return blocked
            self.validate()
            return P09Result("", (), "rumor_recap", (), ("P09.DIALOGUE.001.01",))
        return self.begin_presentation(context, "direct_question")

    def hear_front_context(self, context: P09Context) -> P09Result:
        return self.begin_presentation(context, "front_context")

    def accuse(self, context: P09Context) -> P09Result:
        return self.begin_presentation(context, "accusation")

    def discuss_terms(self, context: P09Context) -> P09Result:
        return self.begin_presentation(context, "terms")

    def connect_shared_wish(self, context: P09Context) -> P09Result:
        return self.begin_presentation(context, "shared_wish")

    def refuse_tag_destruction(self, context: P09Context) -> P09Result:
        blocked = self._base_block(context)
        if blocked is not None:
            return blocked
        return self._result("tag_preserved", "tag_refusal") if self.reachable(context, "chair_tag") else self._result("offscreen")

    def hint(self, context: P09Context, level: int | None = None) -> P09Result:
        self._context(context)
        if level is not None and (type(level) is not int or level not in (1, 2, 3)):
            raise ValueError("Hint level must be 1, 2 or 3")
        if "EVENING_STARTED" not in context.flags:
            return self._result("evening_required")
        if self.ready:
            return self._result("terms_card_available")
        requested = level if level is not None else min(3, self.hint_level + 1)
        if requested <= self.hint_level:
            return self._result("hint", f"hint_{requested}")
        self.hint_level = requested
        self.revision += 1
        result = self._result("hint", f"hint_{requested}")
        return P09Result("", (Event("P09_HINT", "hint", {"serial": self.revision,
            "puzzle": "P09", "level": requested}),), result.code, result.line_ids)

    def act(self, context: P09Context, verb: Verb | str, obj: str, target: str | None = None) -> P09Result:
        verb = Verb(verb)
        self._context(context)
        if type(obj) is not str or (target is not None and type(target) is not str):
            raise ValueError("Objects require stable string IDs")
        if obj == "audience" and target is None:
            return self._result("audience_has_no_p09_information")
        if verb == Verb.LOOK_AT and target is None:
            return self.look(context, obj)
        blocked = self._base_block(context)
        if blocked is not None:
            return blocked
        if not self.reachable(context, obj) or (target is not None and not self.reachable(context, target)):
            return self._result("offscreen")
        if verb == Verb.TALK_TO and obj == "stringer" and target is None:
            return self.topics(context)
        if verb == Verb.OPEN and obj == CARD and target is None:
            return self.begin_presentation(context, "terms_card")
        if obj == CARD or target == CARD:
            return self._result("unsigned_card_reserved_for_p14")
        if verb == Verb.PICK_UP and obj in {"chair_tag", "tagged_chairs"}:
            return self.refuse_tag_destruction(context)
        return self._result("no_change")

    def validate_context(self, context: P09Context) -> None:
        self._context(context)
        self.validate()
        if (self.presentations or self.hint_level) and "EVENING_STARTED" not in context.flags:
            raise ValueError("P09 progress requires the caller's P08 evening handoff")
        if "terms" in self.presentations and "PLAN_AGREED" not in context.flags:
            raise ValueError("Terms require the caller's agreed household plan")
        for flag in FLAG_IDS & context.flags:
            if flag not in self.flags:
                raise ValueError("Campaign P09 flag has no branch receipt")

    def validate(self) -> None:
        def require(ok: bool, message: str) -> None:
            if not ok:
                raise ValueError("Invalid P09 state: " + message)

        require(type(self.revision) is int and self.revision >= 0, "revision")
        require(type(self.hint_level) is int and 0 <= self.hint_level <= 3, "hint level")
        require(type(self.flags) is set and self.flags <= FLAG_IDS, "foreign flags")
        require(type(self.presentations) is dict and self.presentations.keys() <= SOURCE_BINDINGS.keys(), "sources")
        require(type(self.consumed) is dict and self.consumed.keys() <= ONCE_IDS, "one-shots")
        require(all(type(x) is int and 1 <= x <= self.revision for x in self.consumed.values()), "one-shot serial")
        starts = []
        acknowledgments: dict[int, str] = {}
        for source, p in self.presentations.items():
            require(type(p) is Presentation, "presentation type")
            require(type(p.serial) is int and 1 <= p.serial <= self.revision, "presentation serial")
            require(type(p.variant) is str and (p.variant == "full" or
                    (source == "accusation" and p.variant == "stringer_only")), "presentation variant")
            starts.append(p.serial)
            require(type(p.receipts) is dict, "receipt map")
            tokens = _tokens(source, p)
            require(list(p.receipts) == list(tokens[:len(p.receipts)]), "receipt prefix")
            stamps = list(p.receipts.values())
            require(all(type(x) is int and p.serial < x <= self.revision for x in stamps), "receipt serial")
            require(stamps == sorted(stamps), "receipt order")
            for stamp in stamps:
                require(acknowledgments.get(stamp, source) == source, "unrelated presentations share receipt")
                acknowledgments[stamp] = source
            if source == "terms":
                require("P09_RUMOR" in self.consumed and self.consumed["P09_RUMOR"] < p.serial,
                        "terms precede rumor correction")
                if "P09.SUCCESS.001.01" in p.receipts:
                    require(p.receipts["P09.DIALOGUE.002.05"] < p.receipts["P09.SUCCESS.001.01"],
                            "outcome precedes card grant")
            if source == "shared_wish":
                require(any(stamp < p.serial for other in self.presentations.values()
                            for token, stamp in other.receipts.items() if token in CLASS_CONTEXT_UNITS),
                        "shared wish lacks acknowledged class context")
            if source == "terms_card":
                require("P09_TERMS" in self.consumed and self.consumed["P09_TERMS"] < p.serial,
                        "card reader precedes physical grant")
        require(len(set(starts)) == len(starts) and not set(starts) & acknowledgments.keys(), "action serial collision")
        rumor_receipts = [next(iter(p.receipts.values())) for source, p in self.presentations.items()
                          if source in RUMOR_SOURCES and p.receipts]
        require(self.rumor_cleared == bool(rumor_receipts), "rumor flag/receipt mismatch")
        require(("P09_RUMOR" in self.consumed) == bool(rumor_receipts), "rumor one-shot mismatch")
        if rumor_receipts:
            require(self.consumed["P09_RUMOR"] == min(rumor_receipts), "rumor receipt chronology")
        terms = self.presentations.get("terms")
        terms_stamp = terms.receipts.get("P09.DIALOGUE.002.05") if terms else None
        require(self.ready == bool(terms_stamp), "card flag/complete terms mismatch")
        require(self.consumed.get("P09_TERMS") == terms_stamp, "card one-shot mismatch")
        shared = self.presentations.get("shared_wish")
        shared_stamp = shared.receipts.get("P09.DIALOGUE.003.04") if shared else None
        require(self.consumed.get("P09_SHARED_WISH") == shared_stamp, "shared wish one-shot mismatch")
        intro = self.presentations.get("intro")
        if intro and rumor_receipts:
            require(intro.serial < min(rumor_receipts), "new rumor setup after known correction")
        require(self.revision >= len(starts) + len(acknowledgments) + bool(self.hint_level), "uncommitted actions")

    def save(self) -> dict[str, Any]:
        self.validate()
        state = asdict(self)
        state["flags"] = sorted(self.flags)
        return {"kind": SAVE_KIND, "schema": SAVE_SCHEMA, "state": state}

    @classmethod
    def load(cls, data: Mapping[str, Any], *, context: P09Context | None = None) -> P09World:
        try:
            if (type(data) is not dict or set(data) != {"kind", "schema", "state"}
                    or data["kind"] != SAVE_KIND or type(data["schema"]) is not int or data["schema"] != SAVE_SCHEMA):
                raise ValueError("Unsupported P09 save envelope")
            raw = data["state"]
            if type(raw) is not dict or set(raw) != {x.name for x in fields(cls)}:
                raise ValueError("Missing or unknown P09 save fields")
            state = dict(raw)
            flags = state["flags"]
            if type(flags) is not list or any(type(x) is not str for x in flags) or len(set(flags)) != len(flags):
                raise ValueError("Invalid serialized flags")
            state["flags"] = set(flags)
            if type(state["presentations"]) is not dict or type(state["consumed"]) is not dict:
                raise ValueError("Invalid serialized ledger")
            presentations = {}
            for source, p in state["presentations"].items():
                if type(p) is not dict or set(p) != {x.name for x in fields(Presentation)} or type(p["receipts"]) is not dict:
                    raise ValueError("Invalid serialized presentation")
                presentations[source] = Presentation(p["serial"], p["variant"], dict(p["receipts"]))
            state["presentations"] = presentations
            state["consumed"] = dict(state["consumed"])
            world = cls(**state)
            world.validate()
            if context is not None:
                world.validate_context(context)
            return world
        except (KeyError, TypeError) as error:
            raise ValueError("Invalid P09 save") from error
