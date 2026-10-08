"""P14 explicit individual promises and a saveable, post-completion finale.

Every narrative record is an exact current-script ID. Rendering receipts certify
visible text, never audio playback. Replay owns a detached presentation timeline.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar
import copy
import json

from .model import Event, Verb
from .p08_model import PREPARATIONS
from .p10_model import CaptionResult
from .p12_model import _LateWorld, SceneContext, PEOPLE, COURTYARD, LIVING

SAVE_KIND='cakood-p14-branch'
SAVE_SCHEMA=1
TERMS='renewal_repair_card'
PENCIL='grease_pencil'
CARD_IDS={person:f'pledge_card_{person}' for person in PEOPLE}
PREREQUISITES=PREPARATIONS | frozenset(('TRAY_SAFE','HOUSE_ENTERED','EVENING_STARTED',
    'RUMOR_CLEARED','TERMS_CARD_AVAILABLE','CUES_RESTORED','DISPLAY_STAGED','HELP_ACCEPTED',
    'AUD_CUE_VIEW','CUE_RAIL_RELEASED','CUE_RACK_FACING_HOST','INTRODUCTION_CLEAR',
    'SERVED','DISPLAY_REVEALED','TOAST_READY'))
CONTEST_IDS=('VC01','VC02','VC03','VC04')
REMATCH_LOCATIONS={'VC01':'L06_GARAGE','VC02':'L03_PORCH','VC03':'L04_SIDE_PASSAGE','VC04':COURTYARD}


@dataclass(frozen=True)
class P14Context(SceneContext):
    board_room: str=COURTYARD
    repair_date: str=''
    vivian_tone: str='professional'

    def __post_init__(self):
        super().__post_init__()
        if self.board_room not in (LIVING,COURTYARD):raise ValueError('Invalid board location')
        if type(self.repair_date) is not str or len(self.repair_date)>80 or any(ord(x)<32 for x in self.repair_date):raise ValueError('Invalid in-fiction repair date')
        if self.vivian_tone not in ('professional','friendly','cautiously_romantic'):raise ValueError('Invalid P06 closing variant')
        if set(CARD_IDS.values()) & self.inventory:raise ValueError('P14 cards must not be duplicated outside their owner')

P14Result=CaptionResult
RECORD_UNITS = {'P14.OPEN.001': ('P14.OPEN.001.01', 'P14.OPEN.001.02', 'P14.OPEN.001.03'),
 'P14.CARD.jack': (),
 'P14.LABEL.jack': (),
 'P14.APPROVE.jack': ('P14.APPROVE.jack.01',),
 'P14.WRONG.jack': ('P14.WRONG.jack.01',),
 'P14.CARD.bunny': (),
 'P14.LABEL.bunny': (),
 'P14.APPROVE.bunny': ('P14.APPROVE.bunny.01',),
 'P14.WRONG.bunny': ('P14.WRONG.bunny.01',),
 'P14.CARD.frankie': (),
 'P14.LABEL.frankie': (),
 'P14.APPROVE.frankie': ('P14.APPROVE.frankie.01',),
 'P14.WRONG.frankie': ('P14.WRONG.frankie.01',),
 'P14.CARD.milo': (),
 'P14.LABEL.milo': (),
 'P14.APPROVE.milo': ('P14.APPROVE.milo.01',),
 'P14.WRONG.milo': ('P14.WRONG.milo.01',),
 'P14.CARD.vivian': (),
 'P14.LABEL.vivian': (),
 'P14.APPROVE.vivian': ('P14.APPROVE.vivian.01',),
 'P14.WRONG.vivian': ('P14.WRONG.vivian.01',),
 'P14.CARD.rita': (),
 'P14.LABEL.rita': (),
 'P14.APPROVE.rita': ('P14.APPROVE.rita.01',),
 'P14.WRONG.rita': ('P14.WRONG.rita.01',),
 'P14.CARD.felix': (),
 'P14.LABEL.felix': (),
 'P14.APPROVE.felix': ('P14.APPROVE.felix.01',),
 'P14.WRONG.felix': ('P14.WRONG.felix.01',),
 'P14.CARD.stringer': (),
 'P14.LABEL.stringer': (),
 'P14.APPROVE.stringer': ('P14.APPROVE.stringer.01',),
 'P14.WRONG.stringer': ('P14.WRONG.stringer.01',),
 'P14.SUCCESS.001': ('P14.SUCCESS.001.01',),
 'P14.FAILURE.001': ('P14.FAILURE.001.01',),
 'P14.CHOICE.001': (),
 'P14.DIALOGUE.001': ('P14.DIALOGUE.001.01',),
 'P14.CHOICE.002': (),
 'P14.DIALOGUE.002': ('P14.DIALOGUE.002.01',),
 'P14.CHOICE.003': (),
 'P14.DIALOGUE.003': ('P14.DIALOGUE.003.01',
                      'P14.DIALOGUE.003.02',
                      'P14.DIALOGUE.003.03',
                      'P14.DIALOGUE.003.04',
                      'P14.DIALOGUE.003.05'),
 'P14.FAILURE.002': ('P14.FAILURE.002.01',),
 'P14.SUCCESS.002': ('P14.SUCCESS.002.01',),
 'P14.SUCCESS.003': ('P14.SUCCESS.003.01',),
 'P14.READ.001': ('P14.READ.001.01',),
 'P14.SUCCESS.004': ('P14.SUCCESS.004.01',),
 'P14.DIALOGUE.004': ('P14.DIALOGUE.004.01',),
 'P14.DIALOGUE.005': ('P14.DIALOGUE.005.01',),
 'P14.DIALOGUE.006': ('P14.DIALOGUE.006.01',),
 'P14.ENDING.001': ('P14.ENDING.001.01',
                    'P14.ENDING.001.02',
                    'P14.ENDING.001.03',
                    'P14.ENDING.001.04',
                    'P14.ENDING.001.05'),
 'P14.ENDING.002': ('P14.ENDING.002.01', 'P14.ENDING.002.02'),
 'P14.READ.002': (),
 'P14.SYSTEM.001': (),
 'P14.HINT.1': (),
 'P14.HINT.2': (),
 'P14.HINT.3': (),
 'VC.NOTEBOOK.WINS': (),
 'VC.GATE.MISSING_WINS': (),
 'VC.GATE.ALL_WON': (),
 'END.CREDIT.TITLE': (),
 'END.CREDIT.FICTIONAL.STUDIO': (),
 'END.CREDIT.REAL.CREATION': (),
 'END.CREDIT.CAST': (),
 'END.CREDIT.WRITERS.HEADER': (),
 'END.CREDIT.WRITERS.HEAD': (),
 'END.CREDIT.WRITERS.ASSISTANT': (),
 'END.CREDIT.WRITERS.CLUB': (),
 'END.CREDIT.WRITERS.SOCIAL': (),
 'END.CREDIT.WRITERS.META': (),
 'END.CREDIT.WRITERS.ENSEMBLE': (),
 'END.CREDIT.WRITERS.ADVENTURE': (),
 'END.CREDIT.WRITERS.OUTSIDER': (),
 'END.CREDIT.REAL.PRODUCTION': (),
 'END.CREDIT.FICTIONAL.PRODUCERS': (),
 'END.CREDIT.FICTIONAL.FLOOR': (),
 'END.CREDIT.FICTIONAL.CAMERA': (),
 'END.CREDIT.FICTIONAL.SOUND': (),
 'END.CREDIT.FICTIONAL.ART': (),
 'END.CREDIT.FICTIONAL.WARDROBE': (),
 'END.CREDIT.FICTIONAL.POST': (),
 'END.CREDIT.FICTIONAL.PRODUCTION': (),
 'END.CREDIT.FICTIONAL.MUSIC': (),
 'END.CREDIT.FICTIONAL.AUDIENCE': (),
 'END.CREDIT.REAL.ASSISTANCE': (),
 'END.CREDIT.THANKS': (),
 'END.FREEZE': (),
 'END.UI.PAUSE': (),
 'END.UI.CONTINUE': (),
 'END.UI.SKIP': (),
 'END.UI.REPLAY': (),
 'END.UI.ACKNOWLEDGMENTS': (),
 'END.UI.RETURN': (),
 'END.ASSET.AUDIENCE.01': (),
 'END.ASSET.AUDIENCE.02': (),
 'END.ASSET.AUDIENCE.03': (),
 'END.ASSET.AUDIENCE.04': (),
 'END.ASSET.AUDIENCE.05': (),
 'END.ASSET.AUDIENCE.06': (),
 'END.ASSET.AUDIENCE.07': (),
 'END.ASSET.AUDIENCE.08': (),
 'END.ASSET.AUDIENCE.09': (),
 'END.ASSET.AUDIENCE.10': (),
 'END.ASSET.AUDIENCE.11': (),
 'END.ASSET.AUDIENCE.12': (),
 'END.ASSET.AUDIENCE.13': (),
 'END.ASSET.AUDIENCE.14': (),
 'END.ASSET.AUDIENCE.15': (),
 'END.ASSET.AUDIENCE.16': (),
 'END.ASSET.AUDIENCE.17': (),
 'END.ASSET.AUDIENCE.18': (),
 'END.ASSET.AUDIENCE.19': (),
 'END.ASSET.AUDIENCE.20': (),
 'END.ASSET.AUDIENCE.21': (),
 'END.ASSET.AUDIENCE.22': (),
 'END.ASSET.AUDIENCE.23': (),
 'END.ASSET.AUDIENCE.24': (),
 'END.ASSET.FOLEY.01': (),
 'END.ASSET.FOLEY.02': (),
 'END.ASSET.FOLEY.03': (),
 'END.ASSET.FOLEY.04': (),
 'END.ASSET.FOLEY.05': (),
 'END.ASSET.FOLEY.06': (),
 'END.ASSET.FOLEY.07': (),
 'END.ASSET.FOLEY.08': (),
 'END.ASSET.FOLEY.09': ()}
UNIT_SPEAKERS = {'P14.OPEN.001.01': 'frankie',
 'P14.OPEN.001.02': 'jack',
 'P14.OPEN.001.03': 'frankie',
 'P14.APPROVE.jack.01': 'jack',
 'P14.WRONG.jack.01': 'jack',
 'P14.APPROVE.bunny.01': 'bunny',
 'P14.WRONG.bunny.01': 'bunny',
 'P14.APPROVE.frankie.01': 'frankie',
 'P14.WRONG.frankie.01': 'frankie',
 'P14.APPROVE.milo.01': 'milo',
 'P14.WRONG.milo.01': 'milo',
 'P14.APPROVE.vivian.01': 'vivian',
 'P14.WRONG.vivian.01': 'vivian',
 'P14.APPROVE.rita.01': 'rita',
 'P14.WRONG.rita.01': 'rita',
 'P14.APPROVE.felix.01': 'felix',
 'P14.WRONG.felix.01': 'felix',
 'P14.APPROVE.stringer.01': 'stringer',
 'P14.WRONG.stringer.01': 'stringer',
 'P14.SUCCESS.001.01': 'jack',
 'P14.FAILURE.001.01': 'frankie',
 'P14.DIALOGUE.001.01': 'jack',
 'P14.DIALOGUE.002.01': 'jack',
 'P14.DIALOGUE.003.01': 'stringer',
 'P14.DIALOGUE.003.02': 'jack',
 'P14.DIALOGUE.003.03': 'stringer',
 'P14.DIALOGUE.003.04': 'frankie',
 'P14.DIALOGUE.003.05': 'stringer',
 'P14.FAILURE.002.01': 'jack',
 'P14.SUCCESS.002.01': 'jack',
 'P14.SUCCESS.003.01': 'frankie',
 'P14.READ.001.01': 'frankie',
 'P14.SUCCESS.004.01': 'frankie',
 'P14.DIALOGUE.004.01': 'vivian',
 'P14.DIALOGUE.005.01': 'vivian',
 'P14.DIALOGUE.006.01': 'vivian',
 'P14.ENDING.001.01': 'bunny',
 'P14.ENDING.001.02': 'jack',
 'P14.ENDING.001.03': 'bunny',
 'P14.ENDING.001.04': 'frankie',
 'P14.ENDING.001.05': 'jack',
 'P14.ENDING.002.01': 'milo',
 'P14.ENDING.002.02': 'jack'}
CREDIT_ORDER = ('END.CREDIT.TITLE', 'END.CREDIT.FICTIONAL.STUDIO', 'END.CREDIT.REAL.CREATION', 'END.CREDIT.CAST', 'END.CREDIT.WRITERS.HEADER', 'END.CREDIT.WRITERS.HEAD', 'END.CREDIT.WRITERS.ASSISTANT', 'END.CREDIT.WRITERS.CLUB', 'END.CREDIT.WRITERS.SOCIAL', 'END.CREDIT.WRITERS.META', 'END.CREDIT.WRITERS.ENSEMBLE', 'END.CREDIT.WRITERS.ADVENTURE', 'END.CREDIT.WRITERS.OUTSIDER', 'END.CREDIT.REAL.PRODUCTION', 'END.CREDIT.FICTIONAL.PRODUCERS', 'END.CREDIT.FICTIONAL.FLOOR', 'END.CREDIT.FICTIONAL.CAMERA', 'END.CREDIT.FICTIONAL.SOUND', 'END.CREDIT.FICTIONAL.ART', 'END.CREDIT.FICTIONAL.WARDROBE', 'END.CREDIT.FICTIONAL.POST', 'END.CREDIT.FICTIONAL.PRODUCTION', 'END.CREDIT.FICTIONAL.MUSIC', 'END.CREDIT.FICTIONAL.AUDIENCE', 'END.CREDIT.REAL.ASSISTANCE', 'END.CREDIT.THANKS')
ASSET_CREDITS = {'END.ASSET.AUDIENCE.01': 'https://freesound.org/people/Benboncan/sounds/82386/',
 'END.ASSET.AUDIENCE.02': 'https://freesound.org/people/FunWithSound/sounds/381375/',
 'END.ASSET.AUDIENCE.03': 'https://freesound.org/people/lonemonk/sounds/72842/',
 'END.ASSET.AUDIENCE.04': 'https://freesound.org/people/lonemonk/sounds/72843/',
 'END.ASSET.AUDIENCE.05': 'https://freesound.org/people/mglennsound/sounds/678668/',
 'END.ASSET.AUDIENCE.06': 'https://freesound.org/people/mglennsound/sounds/678669/',
 'END.ASSET.AUDIENCE.07': 'https://freesound.org/people/mglennsound/sounds/678670/',
 'END.ASSET.AUDIENCE.08': 'https://freesound.org/people/ShangusBurger/sounds/763954/',
 'END.ASSET.AUDIENCE.09': 'https://freesound.org/people/ShangusBurger/sounds/763960/',
 'END.ASSET.AUDIENCE.10': 'https://freesound.org/people/ShangusBurger/sounds/763961/',
 'END.ASSET.AUDIENCE.11': 'https://freesound.org/people/ShangusBurger/sounds/763962/',
 'END.ASSET.AUDIENCE.12': 'https://freesound.org/people/snakebarney/sounds/138112/',
 'END.ASSET.AUDIENCE.13': 'https://freesound.org/people/ShangusBurger/sounds/763956/',
 'END.ASSET.AUDIENCE.14': 'https://freesound.org/people/ShangusBurger/sounds/763957/',
 'END.ASSET.AUDIENCE.15': 'https://freesound.org/people/ShangusBurger/sounds/763958/',
 'END.ASSET.AUDIENCE.16': 'https://freesound.org/people/ShangusBurger/sounds/763950/',
 'END.ASSET.AUDIENCE.17': 'https://freesound.org/people/ShangusBurger/sounds/763951/',
 'END.ASSET.AUDIENCE.18': 'https://freesound.org/people/ShangusBurger/sounds/763952/',
 'END.ASSET.AUDIENCE.19': 'https://freesound.org/people/ShangusBurger/sounds/763959/',
 'END.ASSET.AUDIENCE.20': 'https://freesound.org/people/FunWithSound/sounds/588394/',
 'END.ASSET.AUDIENCE.21': 'https://freesound.org/people/HowardV/sounds/581528/',
 'END.ASSET.AUDIENCE.22': 'https://freesound.org/people/Nox_Sound/sounds/752711/',
 'END.ASSET.AUDIENCE.23': 'https://freesound.org/people/freesound/sounds/25296/',
 'END.ASSET.AUDIENCE.24': 'https://freesound.org/people/kikorurelas/sounds/767470/',
 'END.ASSET.FOLEY.01': 'https://freesound.org/people/Caitlin_100/sounds/365483/',
 'END.ASSET.FOLEY.02': 'https://freesound.org/people/Karla_Bezuidenhout/sounds/708683/',
 'END.ASSET.FOLEY.03': 'https://freesound.org/people/slamaxu/sounds/509878/',
 'END.ASSET.FOLEY.04': 'https://freesound.org/people/scholzi982/sounds/566189/',
 'END.ASSET.FOLEY.05': 'https://freesound.org/people/piedo/sounds/214693/',
 'END.ASSET.FOLEY.06': 'https://freesound.org/people/IENBA/sounds/607911/',
 'END.ASSET.FOLEY.07': 'https://freesound.org/people/qubodup/sounds/805208/',
 'END.ASSET.FOLEY.08': 'https://kenney.nl/assets/impact-sounds',
 'END.ASSET.FOLEY.09': 'https://kenney.nl/assets/rpg-audio'}


@dataclass
class P14World(_LateWorld):
    start_at: int=0
    entry_flags: list[str]=field(default_factory=list)
    winning_attempts: dict[str,str]=field(default_factory=dict)
    pinned: dict[str,int]=field(default_factory=dict)
    signature_at: int=0
    pencil_at: int=0
    complete_at: int=0
    repair_date: str=''
    vivian_tone: str='professional'
    finale_started_at: int=0
    finale_phase: str='not_started'
    finale_paused: bool=False
    finale_skipped: bool=False
    replay_mode: bool=False
    credit_ids: list[str]=field(default_factory=list)
    credit_cursor: int=0
    frame_at: int=0
    celebration_at: int=0
    laugh_at: int=0
    PUZZLE: ClassVar[str]='P14'
    KIND: ClassVar[str]=SAVE_KIND
    SOURCES: ClassVar[dict[str,str]]={
        'opening':'P14.OPEN.001', **{f'approve:{p}':f'P14.APPROVE.{p}' for p in PEOPLE},
        **{f'card:{p}':f'P14.CARD.{p}' for p in PEOPLE},
        'warm_toast':'P14.DIALOGUE.001','dry_toast':'P14.DIALOGUE.002',
        'signature':'P14.DIALOGUE.003','date':'P14.SUCCESS.003',
        'readback':'P14.READ.001','return_pencil':'P14.SUCCESS.004',
        'closing:professional':'P14.DIALOGUE.004','closing:friendly':'P14.DIALOGUE.005',
        'closing:cautiously_romantic':'P14.DIALOGUE.006','meal':'P14.ENDING.001','tag':'P14.ENDING.002',
        **{'credit:'+r:r for r in (*CREDIT_ORDER,*ASSET_CREDITS)}}
    UNITS: ClassVar=RECORD_UNITS
    SPEAKERS: ClassVar=UNIT_SPEAKERS

    @staticmethod
    def missing_wins(c):
        if c.contests is None:return CONTEST_IDS
        c.contests.validate()
        return c.contests.missing_wins

    @classmethod
    def notebook_gate(cls,c):
        missing=cls.missing_wins(c)
        return {'line_id':'VC.GATE.MISSING_WINS' if missing else 'VC.GATE.ALL_WON',
            'missing_contest_ids':missing,'rematch_locations':{x:REMATCH_LOCATIONS[x] for x in missing},
            'wins':4-len(missing),'won_count':4-len(missing),
            'missing_contest_names':', '.join({'VC01':'Milo Pennant','VC02':'Vivian Voss',
                'VC03':'Felix Bunt','VC04':'Mr. Stringer'}[x] for x in missing),
            'practical_progress_unchanged':True}

    @property
    def ready(self):return bool(self.complete_at)
    @property
    def flags(self):return frozenset(('COMMITMENTS_SIGNED','GAME_COMPLETE')) if self.complete_at else frozenset()
    @property
    def approved(self):return frozenset(p for p in PEOPLE if self._complete('approve:'+p))
    @property
    def inventory(self):return tuple(CARD_IDS[p] for p in PEOPLE if self.start_at and p not in self.pinned)
    @property
    def reserved_external_objects(self):
        return frozenset((TERMS,)) if self.signature_at else frozenset()
    @property
    def pencil_with_frankie(self):return bool(self.pencil_at and not self.complete_at)
    @property
    def dynamic_bindings(self):return {'repair_date':self.repair_date}
    @property
    def pending_freeze_id(self):return f'P14:{self._epoch}:freeze:{self.finale_started_at}' if self.finale_phase=='freeze' and not self.frame_at else None

    def _gate(self,c):
        if type(c) is not P14Context:raise ValueError('P14 context required')
        block=self._scene(c)
        if block is not None:return block
        if not PREREQUISITES<=c.flags:return self._result('canonical_tasks_incomplete')
        if self.missing_wins(c):return self._result('all_four_actual_wins_required','VC.GATE.MISSING_WINS')
        if c.board_room!=COURTYARD:return self._result('board_not_physically_delivered')
        return None

    def start(self,c,terms_handoff):
        block=self._gate(c)
        if block is not None:return block
        if self.start_at:return self._result('commitments_already_started')
        h=terms_handoff
        if (type(h) is not dict or h.get('object_id')!=TERMS or h.get('location')!='inventory'
                or h.get('signed') is not False or h.get('repair_date') is not None
                or h.get('signature_owner')!='P14' or h.get('terms_record_id')!='P09.READ.002'):
            raise ValueError('The original unsigned P09 terms card is required')
        if TERMS not in c.inventory:return self._result('original_terms_card_required')
        if not c.repair_date:return self._result('agreed_fictional_date_required')
        self.entry_flags=sorted(PREREQUISITES)
        self.winning_attempts={encounter:next(a.outcome.id for a in c.contests.attempts
            if a.encounter_id==encounter and a.outcome is not None and a.outcome.winner=='jack') for encounter in CONTEST_IDS}
        self.repair_date=c.repair_date;self.vivian_tone=c.vivian_tone
        self.start_at=self.revision+1
        return self._commit('commitments_started','P14_COMMITMENT_START','puzzle',cards=tuple(CARD_IDS.values()))

    def _block(self,c):
        block=self._gate(c)
        if block is not None:return block
        if not self.start_at:return self._result('commitments_not_started')
        if self.complete_at:return self._result('commitments_already_complete')
        self.validate_context(c)
        return None

    def _presentation_block(self,c,source,tokens):
        finale=source.startswith(('closing:','credit:')) or source in ('meal','tag')
        if finale:
            if type(c) is not P14Context:raise ValueError('P14 context required')
            if not self.complete_at or self.finale_phase=='not_started':return self._result('finale_not_started')
            if self.finale_paused:return self._result('finale_paused')
            if source!=self.current_finale_source:return self._result('not_current_finale_scene')
            block=self._scene(c,LIVING if source=='tag' else COURTYARD) if not source.startswith('credit:') else None
            if block is not None:return block
            return self._speakers(c,tokens)
        block=self._block(c)
        if block is not None:return block
        if source.startswith('approve:'):
            person=source.split(':')[1]
            if person in self.pinned:return self._result('promise_already_pinned')
        if source=='signature':
            if set(self.pinned)!=set(PEOPLE):return self._result('all_eight_approved_and_pinned_required')
            if TERMS not in c.inventory and not self.signature_at:return self._result('original_terms_card_required')
        if source in ('date','readback','return_pencil'):
            if not self.pencil_at:return self._result('pencil_handoff_required')
            if source=='readback' and not self._complete('date'):return self._result('date_text_required')
            if source=='return_pencil' and not self._complete('readback'):return self._result('complete_readback_required')
        return self._speakers(c,tokens)

    def give_card(self,c,card_person,recipient):
        if card_person not in PEOPLE or recipient not in PEOPLE:raise ValueError('Unknown named card or recipient')
        block=self._block(c)
        if block is not None:return block
        if not c.at(recipient,COURTYARD):return self._result('recipient_absent')
        if card_person!=recipient:return self._result('unrelated_promise_returned',f'P14.WRONG.{recipient}')
        if recipient=='jack':return self.confirm_jackie(c)
        return self.begin_presentation(c,'approve:'+recipient)

    def confirm_jackie(self,c):return self.begin_presentation(c,'approve:jack')

    def pin_card(self,c,person):
        if person not in PEOPLE:raise ValueError('Unknown card')
        block=self._block(c)
        if block is not None:return block
        if person in self.pinned:return self._result('card_already_pinned')
        if person not in self.approved:return self._result('approval_required','P14.FAILURE.001')
        self.pinned[person]=self.revision+1
        return self._commit('approved_card_pinned','P14_CARD_PINNED',records=('P14.SUCCESS.001',),
            card_id=CARD_IDS[person],person=person,location='pledge_board')

    def request_signature(self,c,method='agreed_terms'):
        if method not in ('agreed_terms','forge','coerce'):raise ValueError('Unknown signature action')
        block=self._block(c)
        if block is not None:return block
        if self.signature_at:return self._result('already_signed')
        if method!='agreed_terms':return self._result('signature_refused','P14.FAILURE.002')
        return self.begin_presentation(c,'signature')

    def pin_signature(self,c):
        block=self._block(c)
        if block is not None:return block
        if self.signature_at:return self._result('already_signed')
        if not self._complete('signature'):return self._result('whole_consent_scene_required')
        if TERMS not in c.inventory:return self._result('original_terms_card_required')
        self.signature_at=self.revision+1
        return self._commit('terms_signed_and_pinned','P14_TERMS_SIGNED','ownership',records=('P14.SUCCESS.002',),
            object_id=TERMS,from_owner='P09',to_owner='P14',location='pledge_board',signed_by='stringer')

    def give_pencil(self,c):
        block=self._block(c)
        if block is not None:return block
        if self.pencil_at:return self._result('pencil_already_handed_over')
        if not self.signature_at:return self._result('signed_terms_required')
        if PENCIL not in c.inventory:return self._result('original_pencil_required')
        if not c.at('frankie',COURTYARD):return self._result('frankie_absent')
        self.pencil_at=self.revision+1
        return self._commit('pencil_handed_over','P14_PENCIL_HANDOFF','ownership',object_id=PENCIL,
            from_owner='inventory',to_owner='frankie',temporary=True)

    def complete_commitments(self,c):
        if self.complete_at:return self._result('commitments_already_complete')
        block=self._block(c)
        if block is not None:return block
        if not self._complete('return_pencil'):return self._result('complete_dated_readback_and_return_required')
        if not c.at('frankie',COURTYARD):return self._result('frankie_absent')
        self.complete_at=self.revision+1
        return self._commit('game_complete','P14_GAME_COMPLETE','puzzle',
            flags=('COMMITMENTS_SIGNED','GAME_COMPLETE'),return_object=PENCIL,return_to='inventory',
            before_finale=True,terms_card_location='pledge_board')

    @property
    def current_finale_source(self):
        if self.finale_phase=='closing':return 'closing:'+self.vivian_tone
        if self.finale_phase in ('meal','tag'):return self.finale_phase
        if self.finale_phase=='credits' and self.credit_cursor<len(self.credit_ids):return 'credit:'+self.credit_ids[self.credit_cursor]
        return None

    def start_finale(self,shipped_source_urls=()):
        if not self.complete_at:return self._result('legitimate_completion_required')
        if self.finale_started_at:return self._result('finale_already_started')
        if (type(shipped_source_urls) is not tuple or any(type(x) is not str for x in shipped_source_urls)
                or not set(shipped_source_urls)<=set(ASSET_CREDITS.values())):
            raise ValueError('Asset source requires a canonical acknowledgment; production audit remains external')
        self.credit_ids=list(CREDIT_ORDER)+[r for r,url in ASSET_CREDITS.items() if url in shipped_source_urls]
        self.finale_started_at=self.revision+1;self.finale_phase='closing'
        return self._commit('finale_started','P14_FINALE_BEGIN','presentation',room=COURTYARD,
            complete_credit_ids=tuple(self.credit_ids))

    def present_finale(self,c):
        if self.finale_paused:return self._result('finale_paused')
        source=self.current_finale_source
        if source:return self.begin_presentation(c,source)
        return self._result('freeze_frame_pending' if self.finale_phase=='freeze' else 'no_pending_finale_text')

    def advance_finale(self):
        if self.finale_paused:return self._result('finale_paused')
        if self.finale_phase in ('not_started','finished'):return self._result('finale_inactive')
        source=self.current_finale_source
        if source and not self._complete(source):return self._result('whole_finale_record_required')
        if self.finale_phase=='freeze' and not self.frame_at:return self._result('visible_freeze_required')
        if self.finale_phase=='credits':
            self.credit_cursor+=1
            if self.credit_cursor==len(self.credit_ids):self.finale_phase='finished'
        else:self.finale_phase={'closing':'meal','meal':'tag','tag':'freeze','freeze':'credits'}[self.finale_phase]
        return self._commit('finale_advanced','P14_FINALE_SCENE','presentation',phase=self.finale_phase,
            room=LIVING if self.finale_phase=='tag' else None,
            scene_direction_id='END.FREEZE' if self.finale_phase=='freeze' else None)

    def acknowledge_freeze(self,request_id):
        if self.finale_paused:return self._result('finale_paused')
        if request_id is None or request_id!=self.pending_freeze_id:return self._result('stale_freeze')
        self.frame_at=self.revision+1
        return self._commit('freeze_presented','P14_FREEZE_PRESENTED','presentation',direction_record='END.FREEZE')

    def claim_tag_laugh(self):
        if self.laugh_at:return self._result('laugh_consumed')
        if self.finale_paused or self.finale_phase not in ('tag','freeze') or not self._complete('tag'):
            return self._result('tag_laugh_unavailable')
        self.laugh_at=self.revision+1
        return self._commit('laugh_consumed','LAF14','laugh',after_record='P14.ENDING.002',protect_meal=True)

    def claim_celebration(self):
        if self.celebration_at:return self._result('celebration_consumed')
        if self.finale_paused or self.finale_phase!='freeze' or not self.frame_at:return self._result('celebration_unavailable')
        self.celebration_at=self.revision+1
        return self._commit('celebration_consumed','P14_CELEBRATION','presentation',
            cleared_asset_required=True,pcm_policy='single_composite_or_serial',transient_only=True)

    def pause_finale(self,paused=True):
        if type(paused) is not bool:raise ValueError('Pause must be boolean')
        if self.finale_phase in ('not_started','finished') or paused==self.finale_paused:return self._result('pause_unchanged')
        self.finale_paused=paused
        return self._commit('finale_paused' if paused else 'finale_resumed','P14_FINALE_PAUSE','presentation',paused=paused)

    def skip_finale(self):
        if self.finale_phase in ('not_started','finished'):return self._result('finale_inactive')
        self.finale_phase='finished';self.finale_skipped=True;self.finale_paused=False
        return self._commit('finale_skipped','P14_FINALE_SKIP','presentation',drop_transient_audio=True,completion_unchanged=True)

    def create_credit_replay(self,invoking_session):
        if not self.complete_at or not self.finale_started_at:raise ValueError('Credits unlock only after legitimate completion')
        # Copy-by-value: replay never merges progress into another saved timeline.
        saved=json.loads(json.dumps(invoking_session,allow_nan=False))
        if type(saved) is not dict:raise ValueError('Invoking session must be a save object')
        detached=P14World.load(self.save())
        for source in tuple(detached.presentations):
            if source.startswith('credit:'):del detached.presentations[source]
        # Menu replay is the ending credit roll, not a repetition of consent/story.
        detached.finale_phase='credits';detached.credit_cursor=0;detached.replay_mode=True
        detached.finale_paused=False;detached.finale_skipped=False
        detached.validate()
        return CreditReplay(detached,saved)

    def dispatch(self,c,verb,obj,target=None):
        if not isinstance(verb,Verb):verb=Verb(verb)
        person=next((p for p,card in CARD_IDS.items() if card==obj),None)
        if verb==Verb.GIVE and person and target in PEOPLE:return self.give_card(c,person,target)
        if verb==Verb.USE and person and target=='pledge_board':return self.pin_card(c,person)
        if verb==Verb.GIVE and obj==TERMS and target=='stringer':return self.request_signature(c)
        if verb==Verb.GIVE and obj==PENCIL and target=='frankie':return self.give_pencil(c)
        return self._result('unhandled_action')

    def validate_context(self,c):
        if type(c) is not P14Context:raise ValueError('P14 context required')
        if self.start_at:
            if not PREREQUISITES<=c.flags or self.missing_wins(c):raise ValueError('Final commitment gate lost')
            if c.contests.active is not None and not self.complete_at:raise ValueError('Contest overlaps commitments')
            actual={a.outcome.id for a in c.contests.attempts if a.outcome is not None and a.outcome.winner=='jack'}
            if not set(self.winning_attempts.values())<=actual:raise ValueError('Winning attempts belong to another timeline')
        if self.signature_at and TERMS in c.inventory:raise ValueError('Signed card duplicated in inventory')
        if self.pencil_with_frankie and PENCIL in c.inventory:raise ValueError('Pencil held twice')
        if self.complete_at and PENCIL not in c.inventory:raise ValueError('Final pencil not returned')

    def validate(self):
        self._validate_captions()
        self._validate_serials('start_at','signature_at','pencil_at','complete_at','finale_started_at','frame_at','celebration_at','laugh_at')
        if type(self.entry_flags) is not list or type(self.winning_attempts) is not dict or type(self.pinned) is not dict:raise ValueError('Invalid commitment ledger')
        if type(self.repair_date) is not str or len(self.repair_date)>80 or any(ord(x)<32 for x in self.repair_date):raise ValueError('Invalid fictional date')
        if self.vivian_tone not in ('professional','friendly','cautiously_romantic'):raise ValueError('Invalid tone')
        if self.start_at:
            if self.entry_flags!=sorted(PREREQUISITES) or set(self.winning_attempts)!=set(CONTEST_IDS) or not self.repair_date:raise ValueError('Incomplete final gate evidence')
            for key,identity in self.winning_attempts.items():
                if type(identity) is not str or not identity.startswith(key+':A') or not identity.endswith(':KO') or not identity[len(key)+2:-3].isdigit():raise ValueError('Invalid winning-attempt identity')
        elif self.entry_flags or self.winning_attempts or self.pinned or self.presentations or self.signature_at or self.pencil_at or self.complete_at or self.repair_date:raise ValueError('Commitment state before gate')
        if not set(self.pinned)<=set(PEOPLE):raise ValueError('Unknown pinned promise')
        for person,serial in self.pinned.items():
            if type(serial) is not int or not 0<self._done_at('approve:'+person)<serial<=self.revision:raise ValueError('Pin before explicit approval')
        if self.signature_at:
            if set(self.pinned)!=set(PEOPLE) or not max(self.pinned.values())<self._done_at('signature')<self.signature_at:raise ValueError('Premature signature')
        if self.pencil_at and not 0<self.signature_at<self.pencil_at:raise ValueError('Pencil before signed terms')
        if self.complete_at and not self.pencil_at<self._done_at('date')<self._done_at('readback')<self._done_at('return_pencil')<self.complete_at:raise ValueError('Completion before dated readback')
        for source,p in self.presentations.items():
            gate=self.start_at
            if source=='signature':gate=max(self.pinned.values(),default=0) if len(self.pinned)==8 else 0
            if source=='date':gate=self.pencil_at
            if source=='readback':gate=self._done_at('date')
            if source=='return_pencil':gate=self._done_at('readback')
            if source.startswith('closing:') or source in ('meal','tag') or source.startswith('credit:'):gate=self.complete_at
            if not 0<gate<p.serial:raise ValueError('Premature P14 caption')
        phases=('not_started','closing','meal','tag','freeze','credits','finished')
        if self.finale_phase not in phases or any(type(x) is not bool for x in (self.finale_paused,self.finale_skipped,self.replay_mode)):raise ValueError('Invalid finale controls')
        if type(self.credit_ids) is not list or type(self.credit_cursor) is not int or not 0<=self.credit_cursor<=len(self.credit_ids):raise ValueError('Invalid credit cursor')
        if self.finale_started_at:
            if not 0<self.complete_at<self.finale_started_at or self.finale_phase=='not_started':raise ValueError('Finale before completion')
            if tuple(self.credit_ids[:len(CREDIT_ORDER)])!=CREDIT_ORDER or len(set(self.credit_ids))!=len(self.credit_ids) or not set(self.credit_ids[len(CREDIT_ORDER):])<=set(ASSET_CREDITS):raise ValueError('Incomplete or invented credit roll')
        elif self.finale_phase!='not_started' or self.credit_ids or self.credit_cursor or self.finale_paused or self.frame_at or self.celebration_at or self.laugh_at or self.finale_skipped:raise ValueError('Finale state before start')
        if self.replay_mode and (not self.complete_at or not self.finale_started_at or self.finale_phase not in ('credits','finished')):raise ValueError('Invalid replay mode')
        if not self.replay_mode and self.finale_phase=='credits' and not self.frame_at:raise ValueError('Credits before visible freeze')
        if self.finale_phase in ('meal','tag','freeze') and not self._complete('closing:'+self.vivian_tone):raise ValueError('Closing scene skipped')
        if self.finale_phase in ('tag','freeze') and not self._complete('meal'):raise ValueError('Quiet meal skipped')
        if self.finale_phase=='freeze' and not self._complete('tag'):raise ValueError('Final tag skipped')
        if self.frame_at and not 0<self._done_at('tag')<self.frame_at:raise ValueError('Freeze before tag')
        if self.celebration_at and not 0<self.frame_at<self.celebration_at:raise ValueError('Celebration before frame')
        if self.laugh_at and not 0<self._done_at('tag')<self.laugh_at:raise ValueError('Laugh over quiet meal')
        for record in self.credit_ids[:self.credit_cursor]:
            if not self._complete('credit:'+record):raise ValueError('Credit cursor exceeds displayed text')
        if self.finale_phase=='finished' and not self.finale_skipped and self.credit_cursor!=len(self.credit_ids):raise ValueError('Unfinished credit roll')


@dataclass
class CreditReplay:
    """Detached credit viewer; return a byte-equivalent JSON session on exit."""
    world: P14World
    invoking_session: dict
    returned: bool=False

    def save(self):
        return {'kind':'cakood-credit-replay','schema':1,'world':self.world.save(),
                'invoking_session':copy.deepcopy(self.invoking_session),'returned':self.returned}

    @classmethod
    def load(cls,data):
        if (type(data) is not dict or set(data)!={'kind','schema','world','invoking_session','returned'}
                or data['kind']!='cakood-credit-replay' or type(data['schema']) is not int or data['schema']!=1
                or type(data['invoking_session']) is not dict or type(data['returned']) is not bool):raise ValueError('Invalid replay save')
        world=P14World.load(data['world'])
        if not world.complete_at or not world.replay_mode or world.finale_phase not in ('credits','finished'):raise ValueError('Invalid detached roll')
        return cls(world,copy.deepcopy(data['invoking_session']),data['returned'])

    def return_session(self,cancel=False):
        if type(cancel) is not bool:raise ValueError('Invalid replay exit')
        if self.world.finale_phase!='finished':
            if not cancel:raise ValueError('Finish or explicitly close the replay')
            self.world.skip_finale()
        self.returned=True
        return copy.deepcopy(self.invoking_session)
