"""P12 physical cue repair and caption-confirmed public welcome, no native IO."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar
from uuid import uuid4

from .model import Event, Verb
from .p02_model import ROOMS
from .p10_model import _Captioned, CaptionResult, ORDER, CUE_IDS
from .verbal_contest import VerbalContests

COURTYARD = 'L05_COURTYARD'
LIVING = 'L01_LIVING_ROOM'
KITCHEN = 'L02_KITCHEN'
PORCH = 'L03_PORCH'
SIDE = 'L04_SIDE_PASSAGE'
PEOPLE = ('jack', 'bunny', 'frankie', 'milo', 'vivian', 'rita', 'felix', 'stringer')
PREREQUISITES = frozenset(('EVENING_STARTED', 'CUES_RESTORED', 'DISPLAY_STAGED', 'HELP_ACCEPTED'))
SAVE_KIND = 'cakood-p12-branch'
SAVE_SCHEMA = 1


@dataclass(frozen=True)
class CurrentRig:
    """Current P08-owned rig projection; historical PA_TESTED is insufficient."""
    location: str = COURTYARD
    connected: bool = False
    source: str = 'TAPE'
    facing_inward: bool = False

    def __post_init__(self):
        if self.location not in ROOMS or self.source not in ('MIC', 'TAPE'):
            raise ValueError('Invalid current rig')
        if any(type(v) is not bool for v in (self.connected, self.facing_inward)):
            raise ValueError('Rig switches must be boolean')

    @property
    def working(self):
        return self.location == COURTYARD and self.connected and self.source == 'MIC' and self.facing_inward


@dataclass(frozen=True)
class SceneContext:
    room: str
    flags: frozenset[str] = frozenset()
    inventory: frozenset[str] = frozenset()
    on_apron: bool = False
    npc_locations: tuple[tuple[str, str], ...] = ()
    rig: CurrentRig = CurrentRig()
    contests: VerbalContests | None = None

    def __post_init__(self):
        if type(self.room) is not str or self.room not in ROOMS or type(self.on_apron) is not bool:
            raise ValueError('Invalid campaign location')
        if any(type(x) is not frozenset or any(type(y) is not str for y in x)
               for x in (self.flags, self.inventory)):
            raise ValueError('Campaign facts must be frozen string sets')
        if (type(self.npc_locations) is not tuple
                or any(type(p) is not tuple or len(p) != 2 or p[0] not in PEOPLE[1:]
                       or p[1] not in ROOMS for p in self.npc_locations)
                or len(dict(self.npc_locations)) != len(self.npc_locations)):
            raise ValueError('Invalid actual actor locations')
        if type(self.rig) is not CurrentRig:
            raise ValueError('Current rig is required')
        if self.contests is not None:
            if type(self.contests) is not VerbalContests:
                raise ValueError('Contest authority must be VerbalContests')
            self.contests.validate()
        if self.inventory & set(PEOPLE):
            raise ValueError('People cannot be pocketed')

    @property
    def contest_active(self):
        return self.contests is not None and self.contests.active is not None

    def resolved(self, encounter):
        return self.contests is not None and self.contests.progress[encounter].resolved

    def at(self, person, room):
        return self.room == room if person == 'jack' else dict(self.npc_locations).get(person) == room


P12Context = SceneContext
P12Result = CaptionResult
RECORD_UNITS = {'P12.OPEN.001': ('P12.OPEN.001.01', 'P12.OPEN.001.02', 'P12.OPEN.001.03'),
 'P12.LOOK.001': ('P12.LOOK.001.01',),
 'P12.READ.001': (),
 'P12.LOOK.002': ('P12.LOOK.002.01',),
 'P12.FAILURE.001': ('P12.FAILURE.001.01',),
 'P12.SUCCESS.001': ('P12.SUCCESS.001.01',),
 'P12.CHOICE.001': (),
 'P12.DIALOGUE.001': ('P12.DIALOGUE.001.01',),
 'P12.LOOK.003': ('P12.LOOK.003.01',),
 'P12.LOOK.004': ('P12.LOOK.004.01',),
 'P12.SUCCESS.002': ('P12.SUCCESS.002.01',),
 'P12.SUCCESS.003': ('P12.SUCCESS.003.01',),
 'P12.SUCCESS.004': ('P12.SUCCESS.004.01',),
 'P12.SUCCESS.005': ('P12.SUCCESS.005.01',),
 'P12.FAILURE.002': ('P12.FAILURE.002.01',),
 'P12.FAILURE.003': ('P12.FAILURE.003.01',),
 'P12.CHOICE.002': (),
 'P12.FAILURE.004': ('P12.FAILURE.004.01',),
 'P12.CHOICE.003': (),
 'P12.FAILURE.005': ('P12.FAILURE.005.01',),
 'P12.CHOICE.004': (),
 'P12.DIALOGUE.002': ('P12.DIALOGUE.002.01',
                      'P12.DIALOGUE.002.02',
                      'P12.DIALOGUE.002.03',
                      'P12.DIALOGUE.002.04',
                      'P12.DIALOGUE.002.05',
                      'P12.DIALOGUE.002.06',
                      'P12.DIALOGUE.002.07',
                      'P12.DIALOGUE.002.08'),
 'P12.CHOICE.005': (),
 'P12.DIALOGUE.003': ('P12.DIALOGUE.003.01',),
 'P12.DIALOGUE.004': ('P12.DIALOGUE.004.01',
                      'P12.DIALOGUE.004.02',
                      'P12.DIALOGUE.004.03',
                      'P12.DIALOGUE.004.04',
                      'P12.DIALOGUE.004.05'),
 'P12.SUCCESS.006': ('P12.SUCCESS.006.01',
                     'P12.SUCCESS.006.02',
                     'P12.SUCCESS.006.03',
                     'P12.SUCCESS.006.04'),
 'P12.HINT.1': (),
 'P12.HINT.2': (),
 'P12.HINT.3': (),
 'VC03.NEED_RESOLUTION': ()}
UNIT_SPEAKERS = {'P12.OPEN.001.01': 'stringer',
 'P12.OPEN.001.02': 'jack',
 'P12.OPEN.001.03': 'stringer',
 'P12.LOOK.001.01': 'jack',
 'P12.LOOK.002.01': 'jack',
 'P12.FAILURE.001.01': 'jack',
 'P12.SUCCESS.001.01': 'jack',
 'P12.DIALOGUE.001.01': 'audience',
 'P12.LOOK.003.01': 'jack',
 'P12.LOOK.004.01': 'jack',
 'P12.SUCCESS.002.01': 'jack',
 'P12.SUCCESS.003.01': 'jack',
 'P12.SUCCESS.004.01': 'jack',
 'P12.SUCCESS.005.01': 'jack',
 'P12.FAILURE.002.01': 'jack',
 'P12.FAILURE.003.01': 'jack',
 'P12.FAILURE.004.01': 'vivian',
 'P12.FAILURE.005.01': 'bunny',
 'P12.DIALOGUE.002.01': 'jack',
 'P12.DIALOGUE.002.02': 'jack',
 'P12.DIALOGUE.002.03': 'jack',
 'P12.DIALOGUE.002.04': 'jack',
 'P12.DIALOGUE.002.05': 'jack',
 'P12.DIALOGUE.002.06': 'jack',
 'P12.DIALOGUE.002.07': 'stringer',
 'P12.DIALOGUE.002.08': 'rita',
 'P12.DIALOGUE.003.01': 'audience',
 'P12.DIALOGUE.004.01': 'milo',
 'P12.DIALOGUE.004.02': 'bunny',
 'P12.DIALOGUE.004.03': 'vivian',
 'P12.DIALOGUE.004.04': 'milo',
 'P12.DIALOGUE.004.05': 'rita',
 'P12.SUCCESS.006.01': 'frankie',
 'P12.SUCCESS.006.02': 'bunny',
 'P12.SUCCESS.006.03': 'rita',
 'P12.SUCCESS.006.04': 'milo'}


@dataclass
class _LateWorld(_Captioned):
    """Shared bounded-caption mechanics, never an audio completion callback."""
    @classmethod
    def load(cls,data,*,context=None):
        try:
            return super().load(data,context=context)
        except (TypeError,KeyError,AttributeError,IndexError) as exc:
            raise ValueError('Malformed branch state') from exc
    def _scene(self, c, room=COURTYARD, apron=False):
        if not isinstance(c, SceneContext):
            raise ValueError('Campaign scene context is required')
        c.__post_init__()
        if c.room != room or c.on_apron != apron:
            return self._result('offscreen')
        if c.contest_active:
            return self._result('contest_active')
        return None

    def _speakers(self, c, tokens, room=None):
        for token in tokens:
            speaker = self.SPEAKERS.get(token)
            if speaker in PEOPLE[1:] and not c.at(speaker, room or c.room):
                return self._result('speaker_absent')
        return None

    def _done_at(self, source):
        return max(self.presentations[source].receipts.values()) if self._complete(source) else 0

    def cancel_presentation(self, presentation_id):
        if presentation_id not in {self._handle(s) for s in self.presentations}:
            return self._result('stale_presentation')
        # All old runtime callbacks become stale; shown text remains in the save.
        self._epoch = uuid4().hex
        return self._result('presentation_cancelled')

    def audio_finished(self, *args, **kwargs):
        return self._result('audio_has_no_authority')

    def hint(self, c, level):
        if type(level) is not int or level not in (1, 2, 3):
            raise ValueError('Invalid hint level')
        return self._result('hint', f'{self.PUZZLE}.HINT.{level}')


@dataclass
class P12World(_LateWorld):
    start_at: int = 0
    release_at: int = 0
    face_at: int = 0
    intro_at: int = 0
    confetti_at: int = 0
    laugh_at: int = 0
    collection_at: int = 0
    slots: list[str] = field(default_factory=list)
    words: dict[str, str] = field(default_factory=dict)
    PUZZLE: ClassVar[str] = 'P12'
    KIND: ClassVar[str] = SAVE_KIND
    SOURCES: ClassVar[dict[str,str]] = {
        'opening':'P12.OPEN.001', 'rack':'P12.LOOK.001', 'diagram':'P12.READ.001',
        'edge':'P12.LOOK.002', 'audience_view':'P12.DIALOGUE.001',
        'self_view':'P12.LOOK.003', 'catch':'P12.LOOK.004',
        'rehearsal':'P12.DIALOGUE.003', 'introduction':'P12.DIALOGUE.002',
        'confetti':'P12.DIALOGUE.004', 'cleanup':'P12.SUCCESS.006'}
    UNITS: ClassVar = RECORD_UNITS
    SPEAKERS: ClassVar = UNIT_SPEAKERS

    @property
    def viewed(self):
        return self._complete('self_view') or self._complete('audience_view')

    @property
    def ready(self):
        return bool(self.intro_at)

    @property
    def flags(self):
        return frozenset(n for n, v in (
            ('AUD_CUE_VIEW', self.viewed), ('CUE_RAIL_RELEASED', self.release_at),
            ('CUE_RACK_FACING_HOST', self.face_at), ('INTRODUCTION_CLEAR', self.intro_at)) if v)

    @property
    def inventory(self):
        return ()

    @property
    def reserved_external_objects(self):
        return frozenset(('cue_rack', *self.slots)) if self.start_at else frozenset()

    @property
    def visible_order(self):
        return tuple(self.words[x] for x in self.slots)

    @property
    def dynamic_bindings(self):
        return {'visible_cue_order': ', '.join(self.visible_order)}

    def start(self, c, cue_handoff):
        block = self._scene(c)
        if block is not None: return block
        if self.start_at: return self._result('already_rehung')
        if not PREREQUISITES <= c.flags: return self._result('p11_required')
        h = cue_handoff
        if (type(h) is not dict or h.get('rack_id') != 'cue_rack' or h.get('location') != COURTYARD
                or type(h.get('first_restored_serial')) is not int or h['first_restored_serial'] <= 0
                or not isinstance(h.get('slots'), (list,tuple)) or len(h['slots']) != 3
                or len(set(h['slots'])) != 3 or not set(h['slots']) <= set(CUE_IDS)
                or tuple(sorted(h.get('words', ()))) != tuple(sorted(ORDER))):
            raise ValueError('An actual reusable P10 rack is required')
        if set(h['slots']) & c.inventory: raise ValueError('Cue duplicated in inventory')
        self.slots = list(h['slots'])
        self.words = dict(zip(self.slots,h['words']))
        self.slots[0], self.slots[1] = self.slots[1], self.slots[0]
        self.start_at = self.revision + 1
        return self._commit('rack_rehung', 'P12_RACK_HANDOFF', 'ownership',
            owner='P12', previous_owner='P10', object_ids=('cue_rack',*self.slots))

    def _block(self, c, apron=False):
        block=self._scene(c,apron=apron)
        if block is not None: return block
        if not self.start_at: return self._result('rack_handoff_required')
        self.validate_context(c)
        return None

    # NEW RECONSTRUCTION: everything below is newly authored from the complete
    # retained P12 SCI methods/codecs and current canonical authority. It is not
    # claimed to be the missing historical Python tail. Shared classes above and
    # the entire 11,306-byte recovered prefix remain unchanged.

    @property
    def welcome_cleared(self):
        """P13's physical handoff requires completed cleanup and departures."""
        return bool(self.collection_at)

    @property
    def rack_correct(self):
        return self.visible_order == ORDER

    # Proved interface correction: retained SCI p12Handoff rejects a held rack,
    # while the literal Python start checks only held cards. Keep the original
    # bytes and delegate after the additional physical-ownership check.
    _literal_start = start

    def start(self, c, cue_handoff):
        if (isinstance(c, SceneContext) and c.room == COURTYARD and not c.on_apron
                and not c.contest_active and not self.start_at
                and PREREQUISITES <= c.flags and 'cue_rack' in c.inventory):
            raise ValueError('Cue rack duplicated in inventory')
        return self._literal_start(c, cue_handoff)

    def _intro_block(self, c):
        if not (self.viewed and self.face_at and self.rack_correct):
            return self._result('repair_rack_first')
        if not c.resolved('VC03'):
            return self._result('vc03_resolution_required', 'VC03.NEED_RESOLUTION')
        if c.rig.location != COURTYARD: return self._result('pa_not_present')
        if not c.rig.connected: return self._result('microphone_unplugged', 'P12.FAILURE.002')
        if c.rig.source != 'MIC': return self._result('selector_tape', 'P12.FAILURE.003')
        if not c.rig.facing_inward: return self._result('speaker_not_facing_inward')
        return None

    def _presentation_block(self, c, source, tokens):
        apron = source in ('audience_view', 'self_view', 'catch', 'rehearsal')
        block = self._block(c, apron=apron)
        if block is not None: return block
        if source in ('audience_view', 'self_view', 'catch') and self.face_at:
            return self._result('faces_now_on_set')
        if source in ('rack', 'diagram') and self.face_at:
            return self._result('rack_now_facing_host')
        if source == 'introduction':
            block = self._intro_block(c)
            if block is not None: return block
        if source == 'confetti' and not self.confetti_at:
            return self._result('confetti_not_released')
        if source == 'cleanup' and not self._complete('confetti'):
            return self._result('confetti_scene_pending')
        return self._speakers(c, tokens)

    def view(self, c, ask=False):
        if type(ask) is not bool: raise ValueError('Audience choice must be boolean')
        return self.begin_presentation(c, 'audience_view' if ask else 'self_view')

    def release_catch(self, c):
        block = self._block(c, apron=True)
        if block is not None: return block
        if self.release_at: return self._result('catch_already_released')
        self.release_at = self.revision + 1
        return self._commit('catch_released', 'P12_CATCH_RELEASED', records=('P12.SUCCESS.002',))

    def rotate_rack(self, c):
        block = self._block(c)
        if block is not None: return block
        if self.face_at: return self._result('already_facing_host')
        if not self.release_at: return self._result('catch_required', 'P12.FAILURE.001')
        if not self.viewed: return self._result('audience_side_observation_required')
        self.face_at = self.revision + 1
        return self._commit('rack_facing_host', 'P12_RACK_ROTATED', records=('P12.SUCCESS.004',))

    def order_cards(self, c, cards):
        if (type(cards) not in (list, tuple) or len(cards) != 3
                or any(type(card) is not str for card in cards)
                or len(set(cards)) != 3 or set(cards) != set(self.slots)):
            raise ValueError('Reorder the three actual rack cards')
        block = self._block(c)
        if block is not None: return block
        if not self.face_at: return self._result('rotate_first')
        if self.ready or 'introduction' in self.presentations:
            return self._result('welcome_order_protected')
        if list(cards) == self.slots: return self._result('order_unchanged')
        self.slots = list(cards)
        return self._commit('cues_reordered', 'P12_CUES_REORDERED', words=self.visible_order,
                            records=('P12.SUCCESS.005',) if self.rack_correct else ())

    def choose_introduction(self, c, choice='complete'):
        if choice not in ('complete', 'partnerships', 'partners'):
            raise ValueError('Unknown introduction choice')
        block = self._block(c)
        if block is not None: return block
        if self.ready: return self._result('introduction_already_clear')
        if choice != 'complete':
            person, record = ('vivian', 'P12.FAILURE.004') if choice == 'partnerships' else ('bunny', 'P12.FAILURE.005')
            if not c.at(person, COURTYARD): return self._result('speaker_absent')
            return self._result('incomplete_introduction', record)
        return self.begin_presentation(c, 'introduction')

    def commit_introduction(self, c):
        block = self._block(c)
        if block is not None: return block
        if self.ready: return self._result('introduction_already_clear')
        block = self._intro_block(c)
        if block is not None: return block
        if not self._complete('introduction'): return self._result('whole_introduction_required')
        self.intro_at = self.revision + 1
        return self._commit('introduction_clear', 'P12_INTRODUCTION_CLEAR', 'puzzle')

    def release_confetti(self, c):
        block = self._block(c)
        if block is not None: return block
        if self.confetti_at: return self._result('confetti_already_released')
        if not self.ready: return self._result('introduction_required')
        if any(not c.at(p, COURTYARD) for p in PEOPLE[1:]):
            return self._result('ensemble_absent')
        self.confetti_at = self.revision + 1
        return self._commit('confetti_released', 'P12_CONFETTI', 'presentation', covered_panel_unchanged=True)

    def claim_laugh(self, c):
        block = self._block(c)
        if block is not None: return block
        if self.laugh_at: return self._result('laugh_consumed')
        if not self._complete('confetti') or self.collection_at:
            return self._result('laugh_window_closed')
        self.laugh_at = self.revision + 1
        return self._commit('laugh_consumed', 'LAF12', 'laugh', after_record='P12.DIALOGUE.004')

    def finish_welcome(self, c):
        block = self._block(c)
        if block is not None: return block
        if self.collection_at: return self._result('collection_already_started')
        if not self._complete('cleanup'): return self._result('cleanup_text_required')
        self.collection_at = self.revision + 1
        return self._commit('collection_started', 'P12_COLLECTION_POINTS', 'movement',
            destinations={'bunny': KITCHEN, 'frankie': LIVING, 'rita': SIDE,
                          'felix': SIDE, 'vivian': SIDE, 'milo': PORCH}, panel_covered=True)

    def dispatch(self, c, verb, obj, target=None):
        verb = Verb(verb)
        if verb == Verb.LOOK_AT and obj == 'cue_rack':
            return self.view(c) if c.on_apron else self.begin_presentation(c, 'rack')
        if verb == Verb.TALK_TO and obj == 'audience': return self.view(c, True)
        if verb == Verb.PULL and obj == 'swivel_release_catch': return self.release_catch(c)
        if verb == Verb.PULL and obj == 'rack_rotating_handle': return self.rotate_rack(c)
        if verb == Verb.USE and obj == 'microphone': return self.choose_introduction(c)
        return self._result('unhandled_action')

    def validate_context(self, c):
        if not isinstance(c, SceneContext): raise ValueError('Campaign scene context is required')
        c.__post_init__()
        self.validate()
        if self.start_at:
            if not PREREQUISITES <= c.flags: raise ValueError('P11 prerequisite removed')
            if self.reserved_external_objects & c.inventory:
                raise ValueError('P12-owned rack or cards duplicated in inventory')
        if self.ready and not c.resolved('VC03'):
            raise ValueError('Introduction requires actual resolved VC03')

    def validate(self):
        self._validate_captions()
        self._validate_serials('start_at', 'release_at', 'face_at', 'intro_at',
                               'confetti_at', 'laugh_at', 'collection_at')
        if type(self.slots) is not list or type(self.words) is not dict:
            raise ValueError('Malformed cue rack')
        if self.start_at:
            if (len(self.slots) != 3 or any(type(x) is not str for x in self.slots)
                    or len(set(self.slots)) != 3 or not set(self.slots) <= set(CUE_IDS)
                    or set(self.words) != set(self.slots)
                    or any(type(x) is not str for x in self.words.values())
                    or sorted(self.words.values()) != sorted(ORDER)):
                raise ValueError('Rack must conserve its three unique original cues and words')
        elif (self.slots or self.words or self.presentations or any((self.release_at,
                self.face_at, self.intro_at, self.confetti_at, self.laugh_at, self.collection_at))):
            raise ValueError('P12 state requires actual P10 rack handoff')
        for parent, child in ((self.start_at, self.release_at), (self.release_at, self.face_at),
                              (self.face_at, self.intro_at), (self.intro_at, self.confetti_at),
                              (self.confetti_at, self.collection_at)):
            if child and not 0 < parent < child: raise ValueError('Invalid physical chronology')
        observations = [self._done_at(s) for s in ('self_view', 'audience_view') if self._complete(s)]
        observation = min(observations, default=0)
        if self.face_at and not 0 < observation < self.face_at:
            raise ValueError('Rotation requires the displayed audience-side observation')
        if self.intro_at and not (self.rack_correct and 0 < self._done_at('introduction') < self.intro_at):
            raise ValueError('Introduction requires all truthful canonical text')
        if self.laugh_at and not 0 < self.confetti_at < self._done_at('confetti') < self.laugh_at:
            raise ValueError('Laugh precedes shared confetti text')
        if self.collection_at and not 0 < self._done_at('cleanup') < self.collection_at:
            raise ValueError('Collection follows completed cleanup text')
        for source, p in self.presentations.items():
            if not 0 < self.start_at < p.serial: raise ValueError('Presentation precedes rack handoff')
            if source == 'introduction' and not (0 < self.face_at < p.serial and observation and self.rack_correct):
                raise ValueError('Introduction precedes physical cue repair')
            if source == 'confetti' and not 0 < self.confetti_at < p.serial:
                raise ValueError('Confetti scene precedes physical flourish')
            if source == 'cleanup' and not 0 < self._done_at('confetti') < p.serial:
                raise ValueError('Cleanup precedes shared confetti scene')
