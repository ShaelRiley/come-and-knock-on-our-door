"""Strict, finite P09 SCI boundary built from retained metadata.

This is newly reconstructed Python, not recovered historical source.  The
unchanged reference model remains the authority for causal save validation.
All file lookup is relative to this package; no recovery workspace is needed.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Mapping, Sequence

from reference.cakood.model import Event
from reference.cakood.p09_model import (
    CARD, RUMOR_SOURCES, P09Context, P09Result, P09World, Presentation,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "historical" / "manifest.json").read_text(encoding="utf-8"))
SERIAL_BASE: int = MANIFEST["serial_limb_base"]
MAX_SERIAL: int = MANIFEST["max_serial"]
SERIAL_NAMES: tuple[str, ...] = tuple(MANIFEST["serials"])
PERSISTED_PROPERTIES: tuple[str, ...] = tuple(MANIFEST["persisted_properties"])
ALL_PROPERTIES: tuple[str, ...] = tuple(MANIFEST["all_properties"])
SOURCE_IDS: dict[str, int] = dict(MANIFEST["sources"])
ROOM_IDS: dict[str, int] = dict(MANIFEST["rooms"])
CODE_IDS: dict[str, int] = dict(MANIFEST["codes"])
EVENT_IDS: dict[str, int] = dict(MANIFEST["events"])
LINE_IDS: dict[str, int] = dict(MANIFEST["line_ids"])
UNIT_IDS: dict[str, int] = dict(MANIFEST["speech_unit_ids"])
LINE_CAPACITY: int = MANIFEST["line_capacity"]
UNIT_CAPACITY: int = MANIFEST["speech_unit_capacity"]
EVENT_CAPACITY: int = MANIFEST["event_capacity"]
EVENT_ARG_CAPACITY: int = MANIFEST["event_arg_capacity"]
INVENTORY_CAPACITY: int = MANIFEST["external_inventory_capacity"]
SOURCE_TOKENS: dict[str, tuple[str, ...]] = {
    source: tuple(entry["token"] for entry in entries)
    for source, entries in MANIFEST["receipts"].items()
}
CONTEXT_PROPERTIES = (
    "p09ContextValid", "p09Room", "p09Apron", "p09Evening", "p09Plan",
    "p09StringerRoom", "p09RitaRoom", "p09View", "p09ContestActive",
    "p09ClaimRumor", "p09ClaimReady", "p09Epoch",
)
CONTEXT_FLAGS = {
    "EVENING_STARTED": "p09Evening", "PLAN_AGREED": "p09Plan",
    "RUMOR_CLEARED": "p09ClaimRumor", "TERMS_CARD_AVAILABLE": "p09ClaimReady",
}
RESULT_PROPERTIES = (
    "p09Code", "p09LineCount", "p09UnitCount", "p09EventCount",
    "p09ResultHi", "p09ResultLo", "p09PresentationSource",
    "p09PresentationHi", "p09PresentationLo",
)


class CodecError(ValueError):
    """The value is invalid or cannot be represented without losing data."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CodecError(message)


def _integer(value: object, low: int, high: int, name: str) -> int:
    _require(type(value) is int and low <= value <= high,
             f"{name} must be an integer in {low}..{high}; booleans are not integers")
    return value  # type: ignore[return-value]


def split_serial(value: int) -> tuple[int, int]:
    """Encode a 30-bit unsigned serial as two nonnegative 15-bit limbs."""
    return divmod(_integer(value, 0, MAX_SERIAL, "serial"), SERIAL_BASE)


def join_serial(high: int, low: int) -> int:
    return (_integer(high, 0, SERIAL_BASE - 1, "high limb") * SERIAL_BASE
            + _integer(low, 0, SERIAL_BASE - 1, "low limb"))


def _shape(properties: Mapping[str, int], names: Sequence[str], label: str) -> dict[str, int]:
    _require(isinstance(properties, Mapping), f"{label} must be a property mapping")
    _require(set(properties) == set(names), f"{label} has missing or unknown fields")
    return {name: _integer(properties[name], 0, SERIAL_BASE - 1, name) for name in names}


def _read_serial(properties: Mapping[str, int], name: str) -> int:
    return join_serial(properties["p09" + name + "Hi"], properties["p09" + name + "Lo"])


def _put_serial(properties: dict[str, int], name: str, serial: int) -> None:
    high, low = split_serial(serial)
    properties["p09" + name + "Hi"] = high
    properties["p09" + name + "Lo"] = low


def _model_validate(world: P09World, context: P09Context | None = None) -> None:
    _require(type(world) is P09World, "Expected the unchanged reference P09World type")
    try:
        world.validate()
        if context is not None:
            world.validate_context(context)
    except (ValueError, TypeError, AttributeError) as error:
        raise CodecError(str(error)) from error


def encode_world(world: P09World, *, context: P09Context | None = None) -> dict[str, int]:
    """Return exactly the 77 persisted SCI properties, without mutating world.

    The model's causal checks run first.  Serial overflow is an explicit error,
    never truncation or wraparound.  Context, when supplied, adds the model's
    campaign handoff checks; it is not stored in these properties.
    """
    _model_validate(world, context)
    properties = {name: 0 for name in PERSISTED_PROPERTIES}
    properties.update(p09Initialized=1, p09RumorCleared=int(world.rumor_cleared),
                      p09Ready=int(world.ready), p09HintLevel=world.hint_level)
    accusation = world.presentations.get("accusation")
    properties["p09Restricted"] = int(accusation is not None and accusation.variant == "stringer_only")
    _put_serial(properties, "Revision", world.revision)
    for name, event in (("Rumor", "P09_RUMOR"), ("Terms", "P09_TERMS"), ("Shared", "P09_SHARED_WISH")):
        _put_serial(properties, name, world.consumed.get(event, 0))
    for source, source_id in SOURCE_IDS.items():
        presentation = world.presentations.get(source)
        if presentation is None:
            continue
        _put_serial(properties, SERIAL_NAMES[3 + source_id], presentation.serial)
        for entry in MANIFEST["receipts"][source]:
            _put_serial(properties, SERIAL_NAMES[entry["slot"]], presentation.receipts.get(entry["token"], 0))
    return properties


def decode_world(properties: Mapping[str, int], *, context: P09Context | None = None) -> P09World:
    """Decode an exact 77-property image, rejecting invalid causal states."""
    raw = _shape(properties, PERSISTED_PROPERTIES, "persisted image")
    _require(raw["p09Initialized"] == 1, "Uninitialized images are not model saves")
    for name in ("p09RumorCleared", "p09Ready", "p09Restricted"):
        _integer(raw[name], 0, 1, name)
    _integer(raw["p09HintLevel"], 0, 3, "p09HintLevel")
    flags = {flag for flag, prop in (("RUMOR_CLEARED", "p09RumorCleared"),
                                     ("TERMS_CARD_AVAILABLE", "p09Ready")) if raw[prop]}
    consumed = {}
    for name, event in (("Rumor", "P09_RUMOR"), ("Terms", "P09_TERMS"), ("Shared", "P09_SHARED_WISH")):
        serial = _read_serial(raw, name)
        if serial:
            consumed[event] = serial
    presentations = {}
    for source, source_id in SOURCE_IDS.items():
        start = _read_serial(raw, SERIAL_NAMES[3 + source_id])
        receipts = {entry["token"]: _read_serial(raw, SERIAL_NAMES[entry["slot"]])
                    for entry in MANIFEST["receipts"][source]}
        receipts = {token: serial for token, serial in receipts.items() if serial}
        _require(bool(start) or not receipts, f"{source} receipts have no presentation start")
        if start:
            variant = "stringer_only" if source == "accusation" and raw["p09Restricted"] else "full"
            presentations[source] = Presentation(start, variant, receipts)
    _require(not raw["p09Restricted"] or "accusation" in presentations,
             "Restricted variant requires an accusation presentation")
    world = P09World(flags, presentations, consumed, _read_serial(raw, "Revision"), raw["p09HintLevel"])
    _model_validate(world, context)
    return world


def select_persisted(properties: Mapping[str, int]) -> dict[str, int]:
    """Explicitly select save properties from an exact 98-property runtime image.

    This checks all values as finite SCI limbs but does not validate transient
    context/results.  Decode those separately if they are being used.
    """
    raw = _shape(properties, ALL_PROPERTIES, "runtime image")
    return {name: raw[name] for name in PERSISTED_PROPERTIES}


def current_object_ids() -> dict[str, int]:
    """Use current reconstruction mappings, never the historical campaign map."""
    path = ROOT / "schema.json"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))["objects"]
    except (OSError, ValueError, KeyError) as error:
        raise CodecError("Current schema.json objects mapping is required for inventory conversion") from error
    return _object_ids(raw)


def _object_ids(objects: Mapping[str, int] | None) -> dict[str, int]:
    if objects is None:
        return current_object_ids()
    _require(isinstance(objects, Mapping), "Object IDs must be a mapping")
    result = {}
    for name, numeric_id in objects.items():
        _require(type(name) is str and bool(name), "Object names must be nonempty strings")
        result[name] = _integer(numeric_id, 1, INVENTORY_CAPACITY - 1, "object ID")
    _require(len(set(result.values())) == len(result), "Object IDs must be unique")
    return result


@dataclass(frozen=True)
class ContextImage:
    properties: dict[str, int]
    held: tuple[int, ...]

    @property
    def arguments(self) -> tuple[int, ...]:
        """The eleven positional arguments for the SCI p09Context method."""
        return tuple(self.properties[name] for name in CONTEXT_PROPERTIES[1:])


def encode_context(context: P09Context, *, epoch: int = 1,
                   object_ids: Mapping[str, int] | None = None) -> ContextImage:
    """Encode an exact context. Foreign flags/unknown inventory are errors."""
    _require(type(context) is P09Context, "Expected the unchanged reference P09Context type")
    context.__post_init__()
    _integer(epoch, 1, SERIAL_BASE - 1, "epoch")
    _require(context.flags <= CONTEXT_FLAGS.keys(), "Context flags exceed the finite P09 representation")
    objects = _object_ids(object_ids)
    _require(context.inventory <= objects.keys(), "Inventory contains an object absent from the current registry")
    properties = dict(
        p09ContextValid=1, p09Room=ROOM_IDS[context.room], p09Apron=int(context.on_apron),
        p09Evening=int("EVENING_STARTED" in context.flags), p09Plan=int("PLAN_AGREED" in context.flags),
        p09StringerRoom=ROOM_IDS[context.stringer_room], p09RitaRoom=ROOM_IDS[context.rita_room],
        p09View=int(context.conservatory_view == "side"), p09ContestActive=int(context.contest_active),
        p09ClaimRumor=int("RUMOR_CLEARED" in context.flags),
        p09ClaimReady=int("TERMS_CARD_AVAILABLE" in context.flags), p09Epoch=epoch,
    )
    held = [0] * INVENTORY_CAPACITY
    for name in context.inventory:
        held[objects[name]] = 1
    return ContextImage(properties, tuple(held))


def decode_context(image: ContextImage, *, object_ids: Mapping[str, int] | None = None) -> P09Context:
    _require(type(image) is ContextImage, "Expected ContextImage")
    raw = _shape(image.properties, CONTEXT_PROPERTIES, "context image")
    _require(raw["p09ContextValid"] == 1, "Invalid contexts have no reference representation")
    _integer(raw["p09Epoch"], 1, SERIAL_BASE - 1, "epoch")
    for name in ("p09Apron", "p09Evening", "p09Plan", "p09View", "p09ContestActive", "p09ClaimRumor", "p09ClaimReady"):
        _integer(raw[name], 0, 1, name)
    rooms = {value: name for name, value in ROOM_IDS.items()}
    _require(all(raw[name] in rooms for name in ("p09Room", "p09StringerRoom", "p09RitaRoom")), "Unknown room ID")
    _require(type(image.held) is tuple and len(image.held) == INVENTORY_CAPACITY,
             "Held inventory must be a fixed 400-slot tuple")
    for value in image.held:
        _integer(value, 0, 1, "inventory bit")
    objects = {value: name for name, value in _object_ids(object_ids).items()}
    held = {index for index, value in enumerate(image.held) if value}
    _require(held <= objects.keys(), "Held inventory has an unknown current object ID")
    try:
        return P09Context(
            rooms[raw["p09Room"]], bool(raw["p09Apron"]),
            frozenset(flag for flag, prop in CONTEXT_FLAGS.items() if raw[prop]),
            frozenset(objects[index] for index in held), rooms[raw["p09StringerRoom"]],
            rooms[raw["p09RitaRoom"]], "side" if raw["p09View"] else "front", bool(raw["p09ContestActive"]),
        )
    except ValueError as error:
        raise CodecError(str(error)) from error


@dataclass(frozen=True)
class EventImage:
    event_id: int
    arguments: tuple[int, int, int]
    serial: int


@dataclass(frozen=True)
class ResultImage:
    properties: dict[str, int]
    lines: tuple[int, ...]
    units: tuple[int, ...]
    events: tuple[int, ...]
    event_args: tuple[int, ...]


def _lookup_id(numeric_id: int, mapping: Mapping[str, int], name: str) -> str:
    _integer(numeric_id, 0, SERIAL_BASE - 1, name)
    reverse = {value: key for key, value in mapping.items()}
    _require(numeric_id in reverse, f"Unknown {name}")
    return reverse[numeric_id]


def _same_typed(left: object, right: object) -> bool:
    """Prevent equality of bool/int or list/tuple from hiding lossy conversion."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return (left.keys() == right.keys()
                and all(_same_typed(left[key], right[key]) for key in left))
    if isinstance(left, tuple):
        return len(left) == len(right) and all(_same_typed(a, b) for a, b in zip(left, right))
    return left == right


def decode_event(image: EventImage) -> Event:
    """Decode the historical three-argument event interface.

    Presented receipts use inclusive zero-based indices in that source's token
    list.  Fixed card data always comes from the unsigned handoff contract.
    """
    _require(type(image) is EventImage, "Expected EventImage")
    event_id = _lookup_id(image.event_id, EVENT_IDS, "event ID")
    serial = _integer(image.serial, 1, MAX_SERIAL, "event serial")
    _require(type(image.arguments) is tuple and len(image.arguments) == EVENT_ARG_CAPACITY,
             "Event requires exactly three arguments")
    for value in image.arguments:
        _integer(value, 0, SERIAL_BASE - 1, "event argument")
    first, second, third = image.arguments
    payload: dict = {"serial": serial, "puzzle": "P09"}
    if event_id in {"P09_PRESENTATION_QUEUED", "P09_PRESENTED", "P09_RUMOR"}:
        source = _lookup_id(first, SOURCE_IDS, "source ID")
        payload["source"] = source
        if event_id == "P09_PRESENTED":
            tokens = SOURCE_TOKENS[source]
            _require(0 <= second <= third < len(tokens), "Presented token indices are out of bounds")
            selected = tokens[second:third + 1]
            _require(not ("P09.SUCCESS.001.01" in selected and any(token.startswith("P09.DIALOGUE.002.") for token in selected)),
                     "One receipt cannot cross the terms/card-grant presentation barrier")
            payload["canonical_tokens"] = selected
        else:
            _require(second == third == 0, "Unused event arguments must be zero")
            if event_id == "P09_RUMOR":
                _require(source in RUMOR_SOURCES, "Invalid rumor source")
                payload["flag"] = "RUMOR_CLEARED"
        kind = "knowledge" if event_id == "P09_RUMOR" else "presentation"
    elif event_id == "P09_TERMS":
        _require(image.arguments == (399, 0, 0), "Terms event requires the unsigned card object 399")
        payload.update(flag="TERMS_CARD_AVAILABLE", **MANIFEST["card_handoff"])
        kind = "puzzle"
    elif event_id == "P09_SHARED_WISH":
        _require(image.arguments == (1, 0, 0), "Shared-wish event requires the optional marker")
        payload["optional"] = True
        kind = "dialogue"
    else:
        _require(1 <= first <= 3 and second == third == 0, "Invalid hint event arguments")
        payload["level"] = first
        kind = "hint"
    return Event(event_id, kind, payload)


def encode_event(event: Event) -> EventImage:
    _require(type(event) is Event and type(event.payload) is dict, "Expected reference Event with a dictionary payload")
    _require(type(event.id) is str and event.id in EVENT_IDS, "Unknown event ID")
    serial = _integer(event.payload.get("serial"), 1, MAX_SERIAL, "event serial")
    if event.id in {"P09_PRESENTATION_QUEUED", "P09_PRESENTED", "P09_RUMOR"}:
        source = event.payload.get("source")
        _require(type(source) is str and source in SOURCE_IDS, "Unknown event source")
        arguments = (SOURCE_IDS[source], 0, 0)
        if event.id == "P09_PRESENTED":
            selected = event.payload.get("canonical_tokens")
            tokens = SOURCE_TOKENS[source]
            _require(type(selected) is tuple and bool(selected)
                     and all(type(token) is str and token in tokens for token in selected),
                     "Presented event needs canonical source tokens")
            first = tokens.index(selected[0])
            last = first + len(selected) - 1
            _require(selected == tokens[first:last + 1], "Presented event tokens must be contiguous and ordered")
            arguments = (SOURCE_IDS[source], first, last)
    elif event.id == "P09_TERMS":
        arguments = (399, 0, 0)
    elif event.id == "P09_SHARED_WISH":
        arguments = (1, 0, 0)
    else:
        arguments = (_integer(event.payload.get("level"), 1, 3, "hint level"), 0, 0)
    image = EventImage(EVENT_IDS[event.id], arguments, serial)
    canonical = decode_event(image)
    _require(type(event.kind) is str and event.kind == canonical.kind and _same_typed(event.payload, canonical.payload),
             "Event kind/payload differs from the exact P09 event contract")
    return image


def _encode_ids(values: tuple[str, ...], mapping: Mapping[str, int], capacity: int, label: str) -> tuple[int, ...]:
    _require(type(values) is tuple and len(values) <= capacity, f"{label} exceeds its fixed capacity")
    _require(all(type(value) is str and value in mapping for value in values), f"Unknown {label}")
    return tuple(mapping[value] for value in values) + (0,) * (capacity - len(values))


def _decode_ids(values: tuple[int, ...], count: int, mapping: Mapping[str, int], capacity: int, label: str) -> tuple[str, ...]:
    _require(type(values) is tuple and len(values) == capacity, f"{label} array has the wrong size/type")
    _integer(count, 0, capacity, label + " count")
    for value in values:
        _integer(value, 0, SERIAL_BASE - 1, label + " ID")
    _require(not any(values[count:]), f"Unused {label} slots must be zero")
    return tuple(_lookup_id(value, mapping, label + " ID") for value in values[:count])


def encode_result(result: P09Result, *, revision: int | None = None) -> ResultImage:
    """Encode a model result into fixed native arrays and nine properties.

    Supply world.revision to retain the transient serial for query-only results.
    Otherwise it is inferred from the events, or zero for an eventless result.
    """
    _require(type(result) is P09Result, "Expected the unchanged reference P09Result type")
    _require(type(result.text) is str and result.text == "", "Player prose is not representable in this domain result")
    _require(type(result.code) is str and result.code in CODE_IDS, "Unknown result code")
    _require(type(result.events) is tuple and len(result.events) <= EVENT_CAPACITY, "Result exceeds its three-event capacity")
    event_images = tuple(encode_event(event) for event in result.events)
    if revision is None:
        revision = event_images[0].serial if event_images else 0
    _integer(revision, 0, MAX_SERIAL, "result revision")
    _require(all(event.serial == revision for event in event_images), "All result events must share the result revision")
    lines = _encode_ids(result.line_ids, LINE_IDS, LINE_CAPACITY, "line")
    units = _encode_ids(result.speech_unit_ids, UNIT_IDS, UNIT_CAPACITY, "speech unit")
    properties = {name: 0 for name in RESULT_PROPERTIES}
    properties.update(p09Code=CODE_IDS[result.code], p09LineCount=len(result.line_ids),
                      p09UnitCount=len(result.speech_unit_ids), p09EventCount=len(event_images))
    _put_serial(properties, "Result", revision)
    if result.presentation_id is not None:
        _require(type(result.presentation_id) is str, "Presentation ID must be a string or None")
        parts = result.presentation_id.split(":")
        _require(len(parts) == 3 and parts[0] == "P09" and parts[1] in SOURCE_IDS,
                 "Invalid P09 presentation ID")
        try:
            serial = int(parts[2])
        except ValueError as error:
            raise CodecError("Invalid presentation serial") from error
        _integer(serial, 1, MAX_SERIAL, "presentation serial")
        _require(parts[2] == str(serial), "Presentation serial must use canonical decimal form")
        properties["p09PresentationSource"] = SOURCE_IDS[parts[1]]
        _put_serial(properties, "Presentation", serial)
    events = tuple(event.event_id for event in event_images) + (0,) * (EVENT_CAPACITY - len(event_images))
    event_args = tuple(value for event in event_images for value in event.arguments)
    event_args += (0,) * (EVENT_CAPACITY * EVENT_ARG_CAPACITY - len(event_args))
    return ResultImage(properties, lines, units, events, event_args)


def decode_result(image: ResultImage) -> P09Result:
    _require(type(image) is ResultImage, "Expected ResultImage")
    raw = _shape(image.properties, RESULT_PROPERTIES, "result image")
    code = _lookup_id(raw["p09Code"], CODE_IDS, "result code")
    lines = _decode_ids(image.lines, raw["p09LineCount"], LINE_IDS, LINE_CAPACITY, "line")
    units = _decode_ids(image.units, raw["p09UnitCount"], UNIT_IDS, UNIT_CAPACITY, "speech unit")
    _decode_ids(image.events, raw["p09EventCount"], EVENT_IDS, EVENT_CAPACITY, "event")
    _require(type(image.event_args) is tuple and len(image.event_args) == EVENT_CAPACITY * EVENT_ARG_CAPACITY,
             "Event argument array must contain exactly nine slots")
    for value in image.event_args:
        _integer(value, 0, SERIAL_BASE - 1, "event argument")
    used = raw["p09EventCount"] * EVENT_ARG_CAPACITY
    _require(not any(image.event_args[used:]), "Unused event argument slots must be zero")
    serial = _read_serial(raw, "Result")
    events = tuple(decode_event(EventImage(image.events[index],
                   image.event_args[index * EVENT_ARG_CAPACITY:(index + 1) * EVENT_ARG_CAPACITY], serial))
                   for index in range(raw["p09EventCount"]))
    presentation_serial = _read_serial(raw, "Presentation")
    source_id = raw["p09PresentationSource"]
    _require(bool(source_id) == bool(presentation_serial), "Presentation source and serial must appear together")
    presentation_id = None
    if source_id:
        source = _lookup_id(source_id, SOURCE_IDS, "presentation source")
        presentation_id = f"P09:{source}:{presentation_serial}"
    return P09Result("", events, code, lines, units, presentation_id)


_require(SERIAL_BASE == 32768 and MAX_SERIAL == SERIAL_BASE ** 2 - 1, "Unsupported serial metadata")
_require(len(SERIAL_NAMES) == 36 and len(PERSISTED_PROPERTIES) == 77 and len(ALL_PROPERTIES) == 98,
         "Unexpected P09 property layout")
_require(set(PERSISTED_PROPERTIES) | set(CONTEXT_PROPERTIES) | set(RESULT_PROPERTIES) == set(ALL_PROPERTIES),
         "Inconsistent property metadata")
