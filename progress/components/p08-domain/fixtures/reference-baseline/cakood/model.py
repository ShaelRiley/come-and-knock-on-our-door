"""P01 domain logic. Engine adapters own rendering, input and audio playback.

Only committed changes produce events. Sound cannot mutate this model. Objects
are addressed by stable IDs, independent of final art resolution.
"""
from dataclasses import dataclass, field, asdict
from enum import StrEnum


class Verb(StrEnum):
    GIVE = "Give"
    OPEN = "Open"
    CLOSE = "Close"
    PICK_UP = "Pick up"
    LOOK_AT = "Look at"
    TALK_TO = "Talk to"
    USE = "Use"
    PUSH = "Push"
    PULL = "Pull"


ROOMS = ("L03_PORCH", "L01_LIVING_ROOM")


@dataclass(frozen=True)
class Event:
    id: str
    kind: str
    payload: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Result:
    text: str
    events: tuple[Event, ...] = ()


@dataclass
class World:
    room: str = "L03_PORCH"
    on_apron: bool = False
    tray: str = "held"  # held, bench, kitchen
    wedge: str = "sill"  # sill, inventory, door
    door_open: bool = False
    bunny_ready: bool = False
    flags: set[str] = field(default_factory=set)
    consumed: set[str] = field(default_factory=set)
    revision: int = 0

    def _result(self, text, *events):
        if events:
            self.revision += 1
        self.validate()
        return Result(text, tuple(events))

    def once(self, event_id, kind, **payload):
        if event_id in self.consumed:
            return ()
        self.consumed.add(event_id)
        return (Event(event_id, kind, payload),)

    def validate(self):
        assert self.room in ROOMS
        assert self.tray in {"held", "bench", "kitchen"}
        assert self.wedge in {"sill", "inventory", "door"}
        assert self.wedge != "door" or self.door_open
        assert ("TRAY_SAFE" in self.flags) == (self.tray == "kitchen")
        assert "HOUSE_ENTERED" not in self.flags or self.tray == "kitchen"

    def walk(self, target):
        if target == "audience_edge" and not self.on_apron:
            self.on_apron = True
            return self._result("Beyond the unfinished flat, an audience sits facing the set. The house is still right there.", Event("AUD_ENTER", "audience_mode", {"active": True, "room": self.room}))
        if target == "return_to_house" and self.on_apron:
            self.on_apron = False
            return self._result("Jack steps back onto the same set.", Event("AUD_EXIT", "audience_mode", {"active": False, "room": self.room}))
        if self.on_apron:
            return self._result("The apron returns to this room. It isn't a shortcut through the house.")
        if target == "front_door":
            if self.room == "L01_LIVING_ROOM":
                self.room = "L03_PORCH"
                self.door_open = self.wedge == "door"
                return self._result("Jack steps onto the porch.", Event("ROOM_L03", "room", {"room": self.room}))
            if not self.door_open:
                return self._result("The front door is closed.")
            if self.tray == "held" and self.wedge != "door":
                self.door_open = False
                return self._result("The spring draws the door shut. Bunny or the clean bench can take one job off my hands.", Event("DOOR_CLOSE", "object"))
            if self.tray == "bench":
                return self._result("I'd better bring the tray. The wedge can hold the door while I pick it up.")
            self.room = "L01_LIVING_ROOM"
            self.tray = "kitchen"
            self.flags.update(("TRAY_SAFE", "HOUSE_ENTERED"))
            self.door_open = self.wedge == "door"
            events = (Event("ROOM_L01", "room", {"room": self.room}),)
            events += self.once("P01_COMPLETE", "puzzle", puzzle="P01")
            return self._result("The bread samples are safely at the kitchen pass. Frankie looks up from the planning board.", *events)
        return self._result("Jack walks over. There is no timed test.")

    def act(self, verb, obj, target=None):
        verb = Verb(verb)
        if self.on_apron:
            if obj == "audience" and verb == Verb.TALK_TO:
                return self._result("Jack: Good evening. Audience: [A few people wave.]", *self.once("AUD_GREETING", "visible_reaction", caption="A few audience members wave."))
            if obj == "audience" and verb == Verb.LOOK_AT:
                return self._result("People, chairs, and a narrow return path. They can see the set, not anyone's private thoughts.")
            return self._result("Step back onto the set to reach that. Return to the house is always available.")
        porch = self.room == "L03_PORCH"
        if obj in {"bench", "bunny", "sill"} and not porch:
            return self._result("That is on the porch side of the set.")
        if verb == Verb.LOOK_AT:
            descriptions = {
                "tray": "Three jobs, two hands. The arithmetic remains hostile.",
                "bench": "Clean, flat, and broad enough for the covered tray.",
                "front_door": "A self-closing front door. A wedge-shaped gap is visible underneath.",
                "wedge": "A brightly painted wooden wedge. Its shape matches the door gap.",
                "bunny": "Bunny sorts invitations by the openable front window.",
                "board": "Frankie's board is waiting for the complete invitation. P02 lies beyond this proof slice.",
                "print_packet": "Supper club: new partners welcome. There is an oddly cropped border.",
            }
            return self._result(descriptions.get(obj, "Jack takes a closer look."))
        if verb == Verb.TALK_TO and obj == "bunny":
            if self.bunny_ready:
                if self.tray == "kitchen":
                    return self._result("Bunny: The tray is safely at the kitchen pass.")
                return self._result("Bunny: The window is open. Pass the tray through.")
            self.bunny_ready = True
            return self._result("Jack: Could you give me a hand? Bunny opens the window. Bunny: Pass the tray through.", Event("BUNNY_READY", "dialogue"))
        if verb == Verb.GIVE and obj == "tray" and target == "bunny" and porch:
            if self.tray != "held":
                return self._result("The tray is already safely placed.")
            if not self.bunny_ready:
                return self._result("Talk to Bunny first so she can open the window.")
            self.tray = "kitchen"
            self.flags.add("TRAY_SAFE")
            return self._result("Bunny accepts the tray with one hand. Bunny: You could have knocked. It is in the title.", *self.once("A01", "comedy", caption="Jack glances toward the audience; a few people chuckle."))
        if verb == Verb.USE and obj == "tray" and target == "bench" and porch:
            if self.tray != "held":
                return self._result("The tray is already safely placed.")
            self.tray = "bench"
            return self._result("Jack sets the covered tray on the clean bench.", Event("TRAY_BENCH", "object"))
        if verb == Verb.PICK_UP and obj == "tray" and porch:
            if self.tray != "bench":
                return self._result("The tray is already held or safely inside.")
            self.tray = "held"
            if self.wedge != "door":
                self.door_open = False
            return self._result("Jack picks up the tray.", Event("TRAY_HELD", "object"))
        if verb == Verb.PICK_UP and obj == "wedge":
            if self.wedge == "inventory":
                return self._result("The wedge is already in Jack's pocket.")
            if not porch and self.wedge != "door":
                return self._result("The wedge is still on the porch sill.")
            self.wedge = "inventory"
            self.door_open = False
            return self._result("Jack pockets the wedge. The door can still be opened normally.", Event("WEDGE_HELD", "object"))
        if verb == Verb.OPEN and obj == "front_door":
            if self.door_open:
                return self._result("The front door is already open.")
            self.door_open = True
            return self._result("Jack opens the front door.", Event("DOOR_OPEN", "object"))
        if verb == Verb.CLOSE and obj == "front_door":
            if self.wedge == "door":
                return self._result("Pick up the wedge first.")
            if not self.door_open:
                return self._result("The front door is already closed.")
            self.door_open = False
            return self._result("Jack closes the door.", Event("DOOR_CLOSE", "object"))
        if verb == Verb.USE and obj == "wedge" and target == "front_door":
            if self.wedge == "door":
                return self._result("The wedge is already holding the door open.")
            if self.wedge == "sill":
                return self._result("Pick up the brightly painted wedge from the sill first.")
            if not self.door_open:
                return self._result("Open the door before placing the wedge.")
            if self.tray == "held":
                return self._result("Put the tray safely on the bench, or pass it to Bunny, to free a hand.")
            self.wedge = "door"
            return self._result("The wedge holds the door open.", Event("WEDGE_DOOR", "object"))
        if obj == "tray" and target in {"doorknob", "front_door"}:
            return self._result("That is a hinge, not a third roommate. The clean bench would work.")
        return self._result("That doesn't help here. Nothing is lost or damaged.")

    def save(self):
        data = asdict(self)
        data["flags"] = sorted(self.flags)
        data["consumed"] = sorted(self.consumed)
        return data

    @classmethod
    def load(cls, data):
        restored = dict(data)
        restored["flags"] = set(restored["flags"])
        restored["consumed"] = set(restored["consumed"])
        world = cls(**restored)
        world.validate()
        return world
