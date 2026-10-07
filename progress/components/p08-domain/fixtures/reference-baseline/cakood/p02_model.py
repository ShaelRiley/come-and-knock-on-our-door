"""Engine-neutral P01/P02 state, independent of rendering and audio playback.

The delivered P01 model is not modified. Its fields and transition functions are
reused behind explicit seven-room accessibility checks. All new rewards and
handoffs commit atomically before Result.events are returned to an adapter.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from functools import lru_cache
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from .model import Event, Result, Verb, World


SAVE_SCHEMA = 2
SAVE_KIND = "cakood-p02-world"
CONTENT_ROOT = Path(__file__).resolve().parents[1] / "content" / "p02"
COPY_IDS = ("copy_jack", "copy_bunny", "copy_stringer")
CORRECT_AIMS = frozenset(("feed_eight", "responsible_shared_use",
                          "discuss_future_collaborations"))
P01_FLAGS = frozenset(("TRAY_SAFE", "HOUSE_ENTERED"))
P02_FLAGS = frozenset(("INVITATIONS_COMPARED", "KNOW_EVENT_PURPOSE",
                       "KNOW_CUE_ORDER", "PLAN_AGREED"))
ONCE_IDS = frozenset(("A01", "P01_COMPLETE", "AUD_GREETING",
                      "P02_COMPARISON", "P02_COMPLETE"))
SOURCE_IDS = frozenset((*COPY_IDS, "master_invitation", "matched_border",
                        "stringer_inspection"))
INVENTORY_IDS = frozenset(("tray", "print_packet", "wedge", *COPY_IDS,
                           "compared_copies", "master_invitation", "grease_pencil"))
RESERVABLE_ITEMS = frozenset(("tray", "wedge", *COPY_IDS, "compared_copies"))
COPY_ORIGINS = {"copy_jack": "packet", "copy_bunny": "L01_LIVING_ROOM",
                "copy_stringer": "L07_CONSERVATORY"}


@dataclass(frozen=True)
class RoomSpec:
    id: str
    number: int
    title: str
    exits: Mapping[str, str]


def _room(id: str, number: int, title: str, **exits: str) -> RoomSpec:
    return RoomSpec(id, number, title, MappingProxyType(exits))


ROOMS = MappingProxyType({room.id: room for room in (
    _room("L03_PORCH", 0, "Porch", front_door="L01_LIVING_ROOM",
          exit_living="L01_LIVING_ROOM", exit_side="L04_SIDE_PASSAGE",
          exit_garage="L06_GARAGE", exit_conservatory="L07_CONSERVATORY"),
    _room("L01_LIVING_ROOM", 1, "Living room", front_door="L03_PORCH",
          exit_porch="L03_PORCH", exit_kitchen="L02_KITCHEN",
          exit_courtyard="L05_COURTYARD"),
    _room("L02_KITCHEN", 2, "Kitchen", exit_living="L01_LIVING_ROOM"),
    _room("L04_SIDE_PASSAGE", 3, "Side passage", exit_porch="L03_PORCH",
          exit_gate="L05_COURTYARD"),
    _room("L05_COURTYARD", 4, "Courtyard", exit_living="L01_LIVING_ROOM",
          exit_gate="L04_SIDE_PASSAGE"),
    _room("L06_GARAGE", 5, "Milo's garage lounge", exit_porch="L03_PORCH"),
    _room("L07_CONSERVATORY", 6, "Conservatory", exit_porch="L03_PORCH"),
)})
OBJECT_IDS = MappingProxyType({name: i + 1 for i, name in enumerate((
    "front_door", "bunny", "bench", "wedge", "tray", "print_packet",
    "board", "frankie", "audience_edge", "audience", "return_to_house",
    "exit_kitchen", "exit_courtyard", "exit_side", "exit_garage",
    "exit_conservatory", "exit_porch", "exit_living", "exit_gate",
    "copy_jack", "copy_bunny", "copy_stringer", "compared_copies",
    "master_invitation", "grease_pencil", "matched_border",
    "invitation_drawer", "milo", "stringer", "rita", "checklist", "journal",
))})
AIM_IDS = MappingProxyType({name: i + 1 for i, name in enumerate((
    "feed_eight", "responsible_shared_use", "discuss_future_collaborations",
    "romantic_mixer", "property_sale",
))})


@dataclass(frozen=True)
class DocumentView:
    id: str
    title: str
    text: str
    source_ids: tuple[str, ...]
    recorded: bool


@dataclass(frozen=True)
class TopicView:
    id: str
    label: str


@dataclass(frozen=True)
class AimView:
    id: str
    label: str
    selected: bool
    source_id: str


@dataclass(frozen=True)
class PreparationGoal:
    id: str
    label: str
    complete: bool = False
    implemented: bool = False


@lru_cache(maxsize=1)
def _content() -> dict[str, Any]:
    """Authored content is data, never parsed to determine puzzle truth."""
    return json.loads((CONTENT_ROOT / "text.json").read_text(encoding="utf-8"))


@dataclass
class P02World(World):
    copy_locations: dict[str, str] = field(default_factory=lambda: dict(COPY_ORIGINS))
    permissions: set[str] = field(default_factory=set)
    observed_sources: set[str] = field(default_factory=set)
    board_records: set[str] = field(default_factory=set)
    milo_shown: bool = False
    drawer_open: bool = False
    master_location: str = "drawer"
    selected_aims: set[str] = field(default_factory=set)
    plan_started: bool = False
    plan_open: bool = False
    hint_level: int = 0
    inventory_slots: list[str | None] = field(default_factory=lambda: ["tray", "print_packet"])
    copy_slot_gaps: dict[str, int] = field(default_factory=dict)
    inventory_slot_reservations: dict[str, int] = field(default_factory=dict)

    @property
    def phase(self) -> str:
        return "E02" if "PLAN_AGREED" in self.flags else "E01"

    @property
    def p02_available(self) -> bool:
        return P01_FLAGS <= self.flags

    @property
    def inventory(self) -> tuple[str, ...]:
        return tuple(item for item in self.inventory_slots if item is not None)

    def _held_items(self) -> tuple[str, ...]:
        items = ["print_packet"]
        if self.tray == "held":
            items.insert(0, "tray")
        if self.wedge == "inventory":
            items.append("wedge")
        items.extend(copy for copy in COPY_IDS if self.copy_locations[copy] == "inventory")
        if all(self.copy_locations[copy] == "bundle" for copy in COPY_IDS):
            items.append("compared_copies")
        if self.master_location == "inventory":
            items.append("master_invitation")
        if "PLAN_AGREED" in self.flags:
            items.append("grease_pencil")
        return tuple(items)

    @property
    def inventory_page_count(self) -> int:
        return max(1, (len(self.inventory_slots) + 7) // 8)

    def inventory_page(self, page: int = 0) -> tuple[str | None, ...]:
        if type(page) is not int or not 0 <= page < self.inventory_page_count:
            raise ValueError("Invalid inventory page")
        items = self.inventory_slots[page * 8:page * 8 + 8]
        return tuple(items + [None] * (8 - len(items)))

    def _result(self, text: str, *events: Event) -> Result:
        held = self._held_items()
        # Removing a physical item reserves its old empty slot until travel.
        # Re-picking that same item reuses the reservation instead of appending
        # an unbounded sequence of empty tray/wedge slots.
        for i, id in enumerate(self.inventory_slots):
            if id is not None and id not in held:
                self.inventory_slot_reservations[id] = i
            if id in COPY_IDS and self.copy_locations[id] == "board":
                self.copy_slot_gaps[id] = i
        source_slots = list(self.copy_slot_gaps.values()) + [
            i for i, id in enumerate(self.inventory_slots) if id in COPY_IDS]
        first_copy_slot = min(source_slots) if source_slots else None
        slots = [id if id in held else None for id in self.inventory_slots]
        for id in held:
            if id not in slots:
                if id == "compared_copies" and first_copy_slot is not None:
                    slots[first_copy_slot] = id
                elif id in self.inventory_slot_reservations:
                    slots[self.inventory_slot_reservations[id]] = id
                else:
                    slots.append(id)
            self.inventory_slot_reservations.pop(id, None)
        if "compared_copies" in held:
            self.copy_slot_gaps.clear()
            for id in COPY_IDS:
                self.inventory_slot_reservations.pop(id, None)
        if any(event.kind == "room" for event in events):
            slots = [id for id in slots if id is not None]
            self.copy_slot_gaps.clear()
            self.inventory_slot_reservations.clear()
        self.inventory_slots = slots
        return World._result(self, text, *events)

    def object_location(self, obj: str) -> str | None:
        """Single physical owner/location; records are never extra objects."""
        if obj in COPY_IDS:
            return self.copy_locations[obj]
        if obj in self.inventory:
            return "inventory"
        if obj == "master_invitation":
            return "drawer"
        if obj == "journal":
            return "journal"
        if obj == "wedge":
            return self.wedge
        if obj == "tray":
            return {"held": "inventory", "bench": "L03_PORCH",
                    "kitchen": "L02_KITCHEN"}[self.tray]
        if obj == "bunny":
            return "L01_LIVING_ROOM" if self.p02_available else "L03_PORCH"
        if obj in {"board", "frankie", "matched_border"}:
            return "L01_LIVING_ROOM"
        if obj == "checklist":
            return "L01_LIVING_ROOM" if "PLAN_AGREED" in self.flags else None
        if obj in {"milo", "invitation_drawer"}:
            return "L06_GARAGE"
        if obj in {"stringer", "rita"}:
            return "L07_CONSERVATORY"
        if obj in {"bench", "sill"}:
            return "L03_PORCH"
        if obj in {"front_door", "doorknob"}:
            return "front_threshold"
        return None

    def reachable(self, obj: str) -> bool:
        if self.on_apron:
            return obj in {"audience", "return_to_house", "journal"}
        if obj in {"audience_edge", "journal"}:
            return True
        if obj in ROOMS[self.room].exits:
            return True
        location = self.object_location(obj)
        if location in {"inventory", self.room}:
            return True
        if location == "front_threshold" or location == "door":
            return self.room in {"L03_PORCH", "L01_LIVING_ROOM"}
        if location == "sill":
            return self.room == "L03_PORCH"
        if location == "packet":
            return True
        if location in {"board", "pinned"}:
            return self.room == "L01_LIVING_ROOM"
        if location == "bundle":
            return "compared_copies" in self.inventory
        if location == "drawer":
            return self.room == "L06_GARAGE" and self.drawer_open and self.milo_shown
        return False

    def visible_objects(self) -> tuple[str, ...]:
        return tuple(obj for obj in OBJECT_IDS if self.reachable(obj))

    def p01_projection(self) -> World:
        """Diagnostic projection; remote rooms map to the entered-house state.

        This is never used to authorize interaction. The actual room above is
        always authoritative. P01 had no representation of neighbor rooms.
        """
        return World(room=self.room if self.room in {"L03_PORCH", "L01_LIVING_ROOM"}
                     else "L01_LIVING_ROOM", on_apron=self.on_apron, tray=self.tray,
                     wedge=self.wedge, door_open=self.door_open,
                     bunny_ready=self.bunny_ready, flags=self.flags & P01_FLAGS,
                     consumed=self.consumed & {"A01", "P01_COMPLETE", "AUD_GREETING"},
                     revision=self.revision)

    def _blocked(self, obj: str) -> Result:
        return self._result(f"{obj.replace('_', ' ').capitalize()} is not within reach here. Nothing is moved.")

    def walk(self, target: str) -> Result:
        if target == "audience_edge" and not self.on_apron:
            self.on_apron = True
            self.plan_open = False
            return self._result("Jack steps beyond this set's visible edge. The same room has a permanent return.",
                                Event("AUD_ENTER", "audience_mode", {"active": True, "room": self.room}))
        if target == "return_to_house" and self.on_apron:
            self.on_apron = False
            return self._result("Jack returns to the same set.", Event("AUD_EXIT", "audience_mode",
                                {"active": False, "room": self.room}))
        if self.on_apron:
            return self._result("Return to this set first. The audience apron is not a shortcut.")
        destination = ROOMS[self.room].exits.get(target)
        if destination is None:
            return self._result("That is not an exit from this room. The serving hatch passes objects only.")
        if {self.room, destination} == {"L03_PORCH", "L01_LIVING_ROOM"}:
            self.plan_open = False
            result = World.walk(self, "front_door")
            if any(event.id == "P01_COMPLETE" for event in result.events):
                return Result(result.text + " Bunny comes in to her usual place beside the living-room invitations.", result.events)
            return result
        if not self.p02_available:
            return self._result("Secure the covered tray and enter the house first; the invitations can wait safely.")
        self.room = destination
        self.plan_open = False
        return self._result(f"Jack walks to {ROOMS[destination].title}.",
                            Event("ROOM_" + destination.split("_")[0], "room",
                                  {"room": destination, "phase": self.phase}))

    def act(self, verb: Verb | str, obj: str, target: str | None = None) -> Result:
        verb = Verb(verb)
        if self.on_apron:
            if obj == "audience" and target is None and verb in {Verb.LOOK_AT, Verb.TALK_TO}:
                return World.act(self, verb, obj)
            if obj == "journal" and verb in {Verb.LOOK_AT, Verb.OPEN} and target is None:
                return self._result(self.journal_text())
            return self._result("Return to the set to reach that. Its permanent return is always available.")
        if not self.reachable(obj):
            return self._blocked(obj)
        if target is not None and not self.reachable(target):
            return self._blocked(target)
        if not self.p02_available:
            return World.act(self, verb, obj, target)
        if verb in {Verb.LOOK_AT, Verb.OPEN} and target is None:
            if obj in {*COPY_IDS, "master_invitation", "checklist"}:
                return self.read_document(obj)
            if obj == "journal":
                return self._result(self.journal_text())
            if obj == "matched_border":
                return self.compare_border()
            if obj == "board":
                return self._result(self.board_text())
            if obj == "compared_copies":
                return self._result("The same three originals are held together as one bundle. " +
                                    " ".join(self._document(copy).text for copy in COPY_IDS))
            if obj == "print_packet":
                if self.copy_locations["copy_jack"] == "packet":
                    return self.read_document("copy_jack")
                return self._result("Jack's existing packet is empty; his one invitation copy is accounted for separately.")
        if verb == Verb.TALK_TO and target is None:
            defaults = {"bunny": "invitation", "stringer": "invitation",
                        "milo": "invitation", "frankie": "invitation"}
            if obj in defaults:
                return self.talk_topic(obj, defaults[obj])
            if obj == "rita":
                return self._result("Rita's preparation branch is not implemented in this P02 checkpoint.")
        if verb == Verb.PICK_UP and obj in COPY_IDS and target is None:
            return self.collect_copy(obj)
        if verb == Verb.USE and obj in COPY_IDS and target == "board":
            return self.place_copy(obj)
        if verb == Verb.GIVE and obj == "compared_copies" and target == "milo":
            return self.show_milo()
        if obj == "invitation_drawer" and target is None and verb in {Verb.OPEN, Verb.CLOSE}:
            if not self.milo_shown:
                return self._result("The drawer is unlocked. Show Milo the compared copies so he can identify and offer the complete master.")
            desired = verb == Verb.OPEN
            if self.drawer_open == desired:
                return self._result("The invitation drawer is already " + ("open." if desired else "closed."))
            self.drawer_open = desired
            return self._result("Jack " + ("opens" if desired else "closes") + " the invitation drawer.",
                                Event("P02_DRAWER", "object", {"open": desired}))
        if verb == Verb.PICK_UP and obj == "master_invitation" and target is None:
            if self.master_location == "inventory":
                return self._result("Jack already has the one complete master and its reusable card supply.")
            if not self.milo_shown or not self.drawer_open or self.room != "L06_GARAGE":
                return self._result("Milo must offer the master from the open drawer first.")
            self.master_location = "inventory"
            return self._result("With Milo's permission, Jack takes the complete master from the open drawer. Open it to read all the qualifiers.",
                                Event("P02_MASTER_TAKEN", "inventory", {"item": obj}))
        if verb == Verb.USE and obj == "master_invitation" and target == "board":
            return self.begin_plan()
        # The unchanged P01 functions are only reachable for their actual local
        # nouns. In particular, remote Open door and Use wedge cannot mutate it.
        if obj in {"front_door", "wedge", "tray", "bench", "sill", "doorknob"}:
            return World.act(self, verb, obj, target)
        return self._result("That does not help here. Nothing is consumed, promised, or prepared.")

    @staticmethod
    def _text(text_id: str) -> str:
        entry = _content()["strings"][text_id]
        speaker = entry.get("speaker")
        spoken = {"Jack E. Tree", "Bunny Easter", "Frankie Maplewood", "Mr. Stringer",
                  "Milo Pennant", "Rita Stringer", "Audience"}
        return (speaker + ": " if speaker in spoken else "") + entry["text"]

    @classmethod
    def _paragraphs(cls, paragraph_ids: list[str]) -> str:
        return "\n\n".join(cls._text(id) for id in paragraph_ids)

    @classmethod
    def _exchange(cls, id: str) -> str:
        return cls._paragraphs(_content()["exchanges"][id]["paragraph_ids"])

    def _document(self, id: str) -> DocumentView:
        data = _content()["documents"][id]
        return DocumentView(id, self._text(data["title_id"]),
                            self._paragraphs(data["paragraph_ids"]),
                            tuple(data["paragraph_ids"]),
                            id in self.observed_sources or
                            (id == "checklist" and "PLAN_AGREED" in self.flags))

    def document_view(self, id: str, *, record: bool = False) -> DocumentView | None:
        """Read-only UI query. Use read_document to commit first observation."""
        if id not in {*COPY_IDS, "master_invitation", "checklist"} or not self.p02_available:
            return None
        if record:
            eligible = id in self.observed_sources or (id == "checklist" and "PLAN_AGREED" in self.flags)
        else:
            eligible = not self.on_apron and self.reachable(id)
            if id == "master_invitation":
                eligible = eligible and self.master_location == "inventory"
        return self._document(id) if eligible else None

    def read_document(self, id: str, *, record: bool = False) -> Result:
        document = self.document_view(id, record=record)
        if document is None:
            return self._result("That source has not been read or is not accessible here. Take the offered master before opening it.")
        if record or id == "checklist" or id in self.observed_sources:
            return self._result(document.text)
        self.observed_sources.add(id)
        if id == "master_invitation":
            self.flags.update(("KNOW_EVENT_PURPOSE", "KNOW_CUE_ORDER"))
        return self._result(document.text, Event("P02_READ_" + id.upper(), "knowledge",
                            {"source": id, "source_ids": document.source_ids}))

    def collect_copy(self, id: str) -> Result:
        if id not in COPY_IDS or not self.p02_available or self.on_apron or not self.reachable(id):
            return self._blocked(id)
        location = self.copy_locations[id]
        if location == "inventory":
            return self._result("Jack already holds that one original invitation.")
        if location in {"board", "bundle", "pinned"}:
            return self._result("That original is already part of the comparison. Its text remains readable; no extra copy is made.")
        permission = ""
        if id != "copy_jack":
            actor = "bunny" if id == "copy_bunny" else "stringer"
            data = _content()["topics"][actor + ".permission"]
            permission = self._paragraphs(data["paragraph_ids"]) + "\n\n"
            self.permissions.add(id)
        self.copy_locations[id] = "inventory"
        return self._result(permission + ("Jack takes his existing copy out of the print packet."
                            if id == "copy_jack" else "Jack takes the offered original invitation."),
                            Event("P02_TAKE_" + id.upper(), "inventory", {"item": id}))

    def place_copy(self, id: str) -> Result:
        if id not in COPY_IDS or not self.p02_available or self.on_apron or self.room != "L01_LIVING_ROOM":
            return self._result("The comparison board is in the living room. Bring the original there.")
        if self.copy_locations[id] != "inventory":
            return self._result("Use a held original copy. A repeated copy cannot fill another place on the board.")
        self.copy_locations[id] = "board"
        self.board_records.add(id)
        self.observed_sources.add(id)
        document = self._document(id)
        return self._result("Jack places the original on the board and reads its promise.\n\n" + document.text,
                            Event("P02_PLACE_" + id.upper(), "evidence", {"source": id}))

    def compare_border(self) -> Result:
        if not self.p02_available or self.on_apron or self.room != "L01_LIVING_ROOM":
            return self._blocked("matched_border")
        if "INVITATIONS_COMPARED" in self.flags:
            return self._result(self._exchange("comparison_recap"))
        if any(self.copy_locations[id] != "board" for id in COPY_IDS):
            return self._result("The unusual cropped border needs all three distinct originals side by side. " + self.board_text())
        self.flags.add("INVITATIONS_COMPARED")
        self.observed_sources.add("matched_border")
        self.copy_locations = dict.fromkeys(COPY_IDS, "bundle")
        return self._result(self._exchange("comparison_first"),
                            *self.once("P02_COMPARISON", "puzzle", puzzle="P02",
                                       phase="E01", source="matched_border"))

    def show_milo(self) -> Result:
        if not self.p02_available or self.on_apron or self.room != "L06_GARAGE":
            return self._blocked("milo")
        if self.milo_shown:
            return self._result(self._exchange("milo_master_held" if self.master_location == "inventory" else "milo_recap"))
        if "compared_copies" not in self.inventory or "INVITATIONS_COMPARED" not in self.flags:
            return self._result("Milo needs the three originals after their shared border has been compared on Frankie's board.")
        # Atomic exchange: no saveable 'Milo owns bundle' intermediate exists.
        self.milo_shown = True
        self.drawer_open = True
        return self._result(self._exchange("milo_first"),
                            Event("P02_MILO_EXCHANGE", "evidence", {"master_permitted": True,
                                  "bundle_owner": "inventory"}))

    def topic_views(self, actor: str) -> tuple[TopicView, ...]:
        if not self.p02_available or self.on_apron or not self.reachable(actor):
            return ()
        return tuple(TopicView(id, self._text(data["label_id"]))
                     for id, data in _content()["topics"].items() if data["actor"] == actor)

    def talk_topic(self, actor: str, topic: str) -> Result:
        if not self.p02_available or self.on_apron or not self.reachable(actor):
            return self._blocked(actor)
        if "." not in topic:
            topic = actor + "." + topic
        if topic == "frankie.invitation":
            topic = "frankie.plan"
        if topic == "milo.invitation":
            topic = "milo.master"
        if topic not in {view.id for view in self.topic_views(actor)}:
            return self._result("That topic is not available with this person.")
        data = _content()["topics"][topic]
        text = self._paragraphs(data["paragraph_ids"])
        events = []
        if actor in {"bunny", "stringer"} and topic.rsplit(".", 1)[1] in {"invitation", "accusation", "permission"}:
            copy = "copy_" + actor
            if topic.endswith(".permission"):
                if copy not in self.permissions:
                    self.permissions.add(copy)
                    events.append(Event("P02_PERMISSION_" + actor.upper(), "dialogue", {"copy": copy}))
            else:
                # The local recipient gives the complete accurate quotation,
                # regardless of where the one physical original now resides.
                if copy not in self.observed_sources:
                    self.observed_sources.add(copy)
                    events.append(Event("P02_READ_" + copy.upper(), "knowledge", {"source": copy}))
        if topic == "stringer.inspection" and "stringer_inspection" not in self.observed_sources:
            self.observed_sources.add("stringer_inspection")
            events.append(Event("P02_STRINGER_INSPECTION", "knowledge", {"source": "stringer_inspection"}))
        if topic == "milo.master" and self.milo_shown:
            text = self._exchange("milo_master_held" if self.master_location == "inventory" else "milo_recap")
        if topic == "frankie.plan" and "PLAN_AGREED" in self.flags:
            text = self._exchange("plan_recap")
        elif topic == "frankie.plan" and "KNOW_EVENT_PURPOSE" in self.flags:
            text = self._exchange("board_master_recap")
        return self._result(text, *events)

    def begin_plan(self) -> Result:
        if self.on_apron or self.room != "L01_LIVING_ROOM":
            return self._blocked("board")
        if "PLAN_AGREED" in self.flags:
            return self._result(self._exchange("plan_recap"))
        if self.master_location != "inventory" or "KNOW_EVENT_PURPOSE" not in self.flags:
            return self._result("Take and open the complete master first. The plan's answers must come from that source.")
        if self.plan_open:
            return self._result(self._exchange("board_master_recap"))
        text = self._exchange("board_master_recap" if self.plan_started else "board_master_first")
        self.plan_started = True
        self.plan_open = True
        return self._result(text, Event("P02_PLAN_OPEN", "plan_edit"))

    def cancel_plan(self) -> Result:
        if not self.plan_open:
            return self._result("The plan editor is already closed. Accepted choices are retained.")
        self.plan_open = False
        return self._result("Jack leaves the editable plan. Accepted choices remain for his return.",
                            Event("P02_PLAN_CLOSE", "plan_edit"))

    def aim_views(self) -> tuple[AimView, ...]:
        if not self.plan_open:
            return ()
        return tuple(AimView(id, self._text(data["label_id"]), id in self.selected_aims,
                             data["source_id"]) for id, data in _content()["aims"].items())

    def select_aim(self, id: str, selected: bool = True) -> Result:
        if id not in AIM_IDS or type(selected) is not bool:
            raise ValueError("Unknown aim or invalid selection")
        if not self.plan_open:
            return self._result("Use the read master with the living-room board to edit the plan first.")
        data = _content()["aims"][id]
        if id not in CORRECT_AIMS:
            return self._result(self._exchange(data["correction_exchange_id"]))
        if (id in self.selected_aims) == selected:
            return self._result("That choice is already " + ("selected." if selected else "clear."))
        if selected:
            self.selected_aims.add(id)
        else:
            self.selected_aims.remove(id)
        return self._result(self._text(data["label_id"]) + (" selected." if selected else " cleared."),
                            Event("P02_AIM", "plan_edit", {"aim": id, "selected": selected}))

    def confirm_plan(self) -> Result:
        if self.on_apron or self.room != "L01_LIVING_ROOM":
            return self._blocked("board")
        if "PLAN_AGREED" in self.flags:
            return self._result(self._exchange("plan_recap"))
        if not self.plan_open:
            return self._result("Use the read master with the board before agreeing the plan.")
        if self.selected_aims != CORRECT_AIMS:
            missing = sorted(CORRECT_AIMS - self.selected_aims, key=AIM_IDS.get)
            return self._result("The plan still needs: " + "; ".join(
                self._text(_content()["aims"][id]["label_id"]) for id in missing) +
                ". The other valid choices remain selected.")
        self.flags.add("PLAN_AGREED")
        self.copy_locations = dict.fromkeys(COPY_IDS, "pinned")
        self.plan_open = False
        return self._result(self._exchange("plan_complete"),
                            *self.once("P02_COMPLETE", "puzzle", puzzle="P02", phase="E02",
                                       items=("grease_pencil",), checklist="checklist"))

    def preparation_goals(self) -> tuple[PreparationGoal, ...]:
        if "PLAN_AGREED" not in self.flags:
            return ()
        return tuple(PreparationGoal(id, self._text(data["label_id"]))
                     for id, data in _content()["preparation_goals"].items())

    def board_text(self) -> str:
        if self.on_apron or self.room != "L01_LIVING_ROOM":
            return "The board is in the living room. Recorded observations can be read in the journal."
        if "PLAN_AGREED" in self.flags:
            return self._document("checklist").text
        if "INVITATIONS_COMPARED" in self.flags:
            return self._exchange("comparison_recap")
        missing = [id.replace("copy_", "") for id in COPY_IDS if id not in self.board_records]
        return "Original invitations on the board: " + str(len(self.board_records)) + "/3. " + (
            "Still needed: " + ", ".join(missing) + "." if missing else "Look at the matched border.")

    def journal_text(self) -> str:
        entries = [self._document(id).text for id in (*COPY_IDS, "master_invitation")
                   if id in self.observed_sources]
        if "matched_border" in self.observed_sources:
            entries.append(self._exchange("comparison_recap"))
        if "stringer_inspection" in self.observed_sources:
            entries.append(self._paragraphs(_content()["topics"]["stringer.inspection"]["paragraph_ids"]))
        if "PLAN_AGREED" in self.flags:
            entries.append(self._document("checklist").text)
        return "\n\n".join(entries) or "No invitation evidence has been recorded yet."

    def hint(self, level: int | None = None) -> Result:
        if level is not None and (type(level) is not int or level not in (1, 2, 3)):
            raise ValueError("Hint level must be 1, 2, or 3")
        if not self.p02_available:
            return self._result("Secure the tray with Bunny or the clean bench and wooden wedge, then enter the house.")
        requested = level if level is not None else min(3, self.hint_level + 1)
        text = self._text(f"p02.hint.{requested}")
        if "PLAN_AGREED" in self.flags:
            text += "\n\nThe plan is agreed. All five preparation goals remain unfinished in this P02 checkpoint."
        if requested <= self.hint_level:
            return self._result(text)
        self.hint_level = requested
        return self._result(text, Event("P02_HINT", "hint", {"level": requested}))

    def validate(self) -> None:
        def require(condition: bool, message: str) -> None:
            if not condition:
                raise ValueError("Invalid P02 state: " + message)

        require(type(self.room) is str and self.room in ROOMS, "unknown room")
        for name in ("on_apron", "door_open", "bunny_ready", "milo_shown", "drawer_open", "plan_started", "plan_open"):
            require(type(getattr(self, name)) is bool, name + " must be boolean")
        for name in ("flags", "consumed", "permissions", "observed_sources", "board_records", "selected_aims"):
            value = getattr(self, name)
            require(type(value) is set and all(type(item) is str for item in value), name + " must be a string set")
        require(type(self.revision) is int and self.revision >= 0, "invalid revision")
        require(type(self.hint_level) is int and 0 <= self.hint_level <= 3, "invalid hint level")
        require(self.flags <= P01_FLAGS | P02_FLAGS, "unsupported future flags")
        require(self.consumed <= ONCE_IDS, "unknown one-shot event")
        require(type(self.tray) is str and self.tray in {"held", "bench", "kitchen"}, "invalid tray location")
        require(type(self.wedge) is str and self.wedge in {"sill", "inventory", "door"}, "invalid wedge location")
        require(self.wedge != "door" or self.door_open, "installed wedge needs open door")
        require(("TRAY_SAFE" in self.flags) == (self.tray == "kitchen"), "tray safety mismatch")
        require("HOUSE_ENTERED" not in self.flags or self.tray == "kitchen", "house entered with unsafe tray")
        try:
            self.p01_projection().validate()
        except AssertionError as error:
            raise ValueError("Invalid P02 state: original P01 invariant") from error
        require(("HOUSE_ENTERED" in self.flags) == ("P01_COMPLETE" in self.consumed), "P01 completion ledger mismatch")
        require("A01" not in self.consumed or (self.bunny_ready and self.tray == "kitchen"), "invalid tray handoff ledger")
        require(self.room in {"L03_PORCH", "L01_LIVING_ROOM"} or self.p02_available, "neighborhood entered before P01")
        require(self.room != "L01_LIVING_ROOM" or self.p02_available, "house entered without tray")
        require(type(self.copy_locations) is dict and set(self.copy_locations) == set(COPY_IDS), "copy identity mismatch")
        require(all(type(value) is str for value in self.copy_locations.values()), "invalid copy owner type")
        require(self.permissions <= {"copy_bunny", "copy_stringer"}, "unknown collection permission")
        require(self.observed_sources <= SOURCE_IDS, "unknown knowledge source")
        require(self.board_records <= set(COPY_IDS), "unknown board record")
        require(self.board_records <= self.observed_sources, "unobserved board evidence")
        require(self.selected_aims <= CORRECT_AIMS, "unaccepted or unknown plan aim")
        require(type(self.master_location) is str and self.master_location in {"drawer", "inventory"}, "invalid master owner")
        require(type(self.inventory_slots) is list and
                all(id is None or type(id) is str for id in self.inventory_slots), "invalid inventory slots")
        require(len(self.inventory_slots) <= len(INVENTORY_IDS),
                "inventory exceeds the finite physical-item registry")
        held_slots = [id for id in self.inventory_slots if id is not None]
        require(len(set(held_slots)) == len(held_slots) and set(held_slots) == set(self._held_items()),
                "inventory slots disagree with unique physical ownership")
        require(type(self.copy_slot_gaps) is dict and set(self.copy_slot_gaps) <= set(COPY_IDS),
                "invalid copy slot bookkeeping")
        require(all(type(index) is int and 0 <= index < len(self.inventory_slots)
                    and self.inventory_slots[index] is None and self.copy_locations[id] == "board"
                    for id, index in self.copy_slot_gaps.items()), "invalid source slot gap")
        require(len(set(self.copy_slot_gaps.values())) == len(self.copy_slot_gaps), "duplicate source slot gap")
        require(type(self.inventory_slot_reservations) is dict
                and set(self.inventory_slot_reservations) <= RESERVABLE_ITEMS,
                "invalid inventory slot reservations")
        require(all(type(index) is int and 0 <= index < len(self.inventory_slots)
                    and self.inventory_slots[index] is None and id not in held_slots
                    for id, index in self.inventory_slot_reservations.items()),
                "invalid reserved empty slot")
        require(len(set(self.inventory_slot_reservations.values())) == len(self.inventory_slot_reservations),
                "duplicate reserved empty slot")
        require(self.copy_slot_gaps == {id: index for id, index in self.inventory_slot_reservations.items()
                                      if id in COPY_IDS}, "copy reservation mismatch")
        require("tray" not in self.inventory_slot_reservations or self.tray != "held", "reserved held tray")
        require("wedge" not in self.inventory_slot_reservations or self.wedge == "door", "reserved unmoved wedge")
        require("compared_copies" not in self.inventory_slot_reservations or "PLAN_AGREED" in self.flags,
                "reserved bundle before pinning")
        compared = "INVITATIONS_COMPARED" in self.flags
        agreed = "PLAN_AGREED" in self.flags
        read = "master_invitation" in self.observed_sources
        require(compared == ("matched_border" in self.observed_sources) == ("P02_COMPARISON" in self.consumed), "comparison ledger/source mismatch")
        require(agreed == ("P02_COMPLETE" in self.consumed), "plan completion ledger mismatch")
        require(read == ("KNOW_EVENT_PURPOSE" in self.flags) == ("KNOW_CUE_ORDER" in self.flags), "master knowledge mismatch")
        for id in COPY_IDS:
            location = self.copy_locations[id]
            if compared:
                require(location == ("pinned" if agreed else "bundle"), "compared originals must share one owner")
                require(self.board_records == set(COPY_IDS), "missing permanent comparison records")
            else:
                require(location in {COPY_ORIGINS[id], "inventory", "board"}, "invalid original owner")
                require((location == "board") == (id in self.board_records), "placement/record mismatch")
            if id != "copy_jack" and location != COPY_ORIGINS[id]:
                require(id in self.permissions, "copy moved without permission")
        require(not self.milo_shown or compared, "Milo has unseen evidence")
        require(not self.drawer_open or self.milo_shown, "drawer opened without exchange")
        require(self.master_location != "inventory" or self.milo_shown, "master taken without permission")
        require(not read or self.master_location == "inventory", "master knowledge without acquired source")
        require(not self.plan_started or read, "plan begun without reading master")
        require(not self.selected_aims or self.plan_started, "plan choices without beginning plan")
        require(not self.plan_open or (self.plan_started and not agreed and self.room == "L01_LIVING_ROOM" and not self.on_apron), "invalid open plan editor")
        require(not agreed or (read and self.selected_aims == CORRECT_AIMS and self.milo_shown), "premature agreed plan")
        if not self.p02_available:
            require(self.copy_locations == COPY_ORIGINS and not self.permissions and not self.observed_sources
                    and not self.board_records and not self.milo_shown and not self.drawer_open
                    and self.master_location == "drawer" and not self.selected_aims and not self.plan_started and not self.plan_open
                    and not self.hint_level and not (self.flags & P02_FLAGS), "P02 state before P01")

    def save(self) -> dict[str, Any]:
        """New explicit envelope; never a delivered native/P01 save format."""
        self.validate()
        state = asdict(self)
        for name in ("flags", "consumed", "permissions", "observed_sources", "board_records", "selected_aims"):
            state[name] = sorted(state[name])
        return {"kind": SAVE_KIND, "schema": SAVE_SCHEMA, "state": state}

    @classmethod
    def load(cls, data: Mapping[str, Any]) -> P02World:
        """Fail closed on unknown fields, bad types, impossible ownership or lore."""
        try:
            if type(data) is not dict or set(data) != {"kind", "schema", "state"}:
                raise ValueError("Invalid save envelope")
            if data["kind"] != SAVE_KIND or type(data["schema"]) is not int or data["schema"] != SAVE_SCHEMA:
                raise ValueError("Unsupported P02 save schema")
            raw = data["state"]
            if type(raw) is not dict or set(raw) != {f.name for f in fields(cls)}:
                raise ValueError("Missing or unknown state fields")
            state = dict(raw)
            for name in ("flags", "consumed", "permissions", "observed_sources", "board_records", "selected_aims"):
                value = state[name]
                if type(value) is not list or any(type(item) is not str for item in value) or len(set(value)) != len(value):
                    raise ValueError("Invalid serialized " + name)
                state[name] = set(value)
            if type(state["copy_locations"]) is not dict:
                raise ValueError("Invalid serialized copy ownership")
            state["copy_locations"] = dict(state["copy_locations"])
            if type(state["copy_slot_gaps"]) is not dict:
                raise ValueError("Invalid serialized copy slots")
            state["copy_slot_gaps"] = dict(state["copy_slot_gaps"])
            if type(state["inventory_slot_reservations"]) is not dict:
                raise ValueError("Invalid serialized inventory reservations")
            state["inventory_slot_reservations"] = dict(state["inventory_slot_reservations"])
            if type(state["inventory_slots"]) is not list:
                raise ValueError("Invalid serialized inventory slots")
            state["inventory_slots"] = list(state["inventory_slots"])
            world = cls(**state)
            world.validate()
            return world
        except (KeyError, TypeError, AssertionError) as error:
            raise ValueError("Invalid P02 save") from error
