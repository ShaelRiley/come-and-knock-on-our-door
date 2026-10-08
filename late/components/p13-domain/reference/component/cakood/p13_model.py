"""P13 turn-based physical deliveries, Rita's consent, and VC04 handoff."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar

from .model import Event, Verb
from .p04_model import GateHandoff
from .p10_model import CaptionResult, ORDER
from .p12_model import (_LateWorld, SceneContext, COURTYARD, KITCHEN, LIVING, SIDE, PORCH, PEOPLE)

SAVE_KIND='cakood-p13-branch'
SAVE_SCHEMA=1
ROUTES=('house_doorway','kitchen_hatch','side_gate')
PROGRAM='guest_program_card'
BOARD='pledge_board'
PREREQUISITES=frozenset(('INTRODUCTION_CLEAR','FOOD_READY','DISPLAY_STAGED','HELP_ACCEPTED','EVENING_STARTED'))


@dataclass(frozen=True)
class P13Context(SceneContext):
    gate: GateHandoff | None = None
    welcome_cleared: bool = False
    queue_clear: bool = False
    buffet_at_hatch: bool = False
    hatch_visible: bool = False
    display_concealed: bool = False
    lane_clear: bool = False
    footprint_clear: bool = False
    board_room: str = LIVING

    def __post_init__(self):
        super().__post_init__()
        if any(type(v) is not bool for v in (self.welcome_cleared,self.queue_clear,self.buffet_at_hatch,self.hatch_visible,
                self.display_concealed,self.lane_clear,self.footprint_clear)):
            raise ValueError('Layout observations must be boolean')
        if self.board_room not in (LIVING,COURTYARD):raise ValueError('Invalid board location')
        if self.gate is not None:
            g=self.gate
            if (type(g) is not GateHandoff or g.peg_id!='hold_open_peg' or g.peg_location!=SIDE
                    or any(type(x) is not bool for x in (g.tested,g.peg_available,g.peg_engaged,g.gate_open,g.wedge_in_gate))
                    or g.peg_available and not g.tested or g.peg_engaged and not (g.peg_available and g.gate_open)
                    # NEW current P04 owner invariant, independently contrasted.
                    or g.wedge_in_gate and (g.peg_engaged or not g.gate_open)):
                raise ValueError('Invalid current P04 gate')
        if self.inventory & {'hotpot_pot','handcart','folded_display',BOARD}:
            raise ValueError('Large delivery object cannot be pocketed')

P13Result=CaptionResult
RECORD_UNITS = {'P13.OPEN.001': ('P13.OPEN.001.01', 'P13.OPEN.001.02', 'P13.OPEN.001.03'),
 'P13.LOOK.001': ('P13.LOOK.001.01',),
 'P13.LABEL.001': (),
 'P13.LABEL.002': (),
 'P13.LABEL.003': (),
 'P13.READ.001': (),
 'P13.READ.002': (),
 'P13.READ.003': (),
 'P13.INVENTORY.001': (),
 'P13.READ.004': (),
 'P13.INVENTORY.002': (),
 'P13.LOOK.002': ('P13.LOOK.002.01',),
 'P13.CHOICE.001': (),
 'P13.SUCCESS.001': ('P13.SUCCESS.001.01',
                     'P13.SUCCESS.001.02',
                     'P13.SUCCESS.001.03'),
 'P13.DIALOGUE.001': ('P13.DIALOGUE.001.01',),
 'P13.DIALOGUE.002': ('P13.DIALOGUE.002.01',),
 'P13.DIALOGUE.003': ('P13.DIALOGUE.003.01',),
 'P13.SUCCESS.002': ('P13.SUCCESS.002.01',),
 'P13.SUCCESS.003': ('P13.SUCCESS.003.01',),
 'P13.FAILURE.001': ('P13.FAILURE.001.01',),
 'P13.FAILURE.002': ('P13.FAILURE.002.01',),
 'P13.FAILURE.003': ('P13.FAILURE.003.01',),
 'P13.FAILURE.004': ('P13.FAILURE.004.01',),
 'P13.CHOICE.002': (),
 'P13.DIALOGUE.004': ('P13.DIALOGUE.004.01',),
 'P13.CHOICE.003': (),
 'P13.SUCCESS.004': ('P13.SUCCESS.004.01',
                     'P13.SUCCESS.004.02',
                     'P13.SUCCESS.004.03'),
 'P13.FAILURE.005': ('P13.FAILURE.005.01',),
 'P13.SUCCESS.005': ('P13.SUCCESS.005.01',),
 'P13.DIALOGUE.005': ('P13.DIALOGUE.005.01',
                      'P13.DIALOGUE.005.02',
                      'P13.DIALOGUE.005.03',
                      'P13.DIALOGUE.005.04',
                      'P13.DIALOGUE.005.05'),
 'P13.SUCCESS.006': ('P13.SUCCESS.006.01',),
 'P13.SUCCESS.007': ('P13.SUCCESS.007.01',),
 'P13.FAILURE.006': ('P13.FAILURE.006.01',),
 'P13.SUCCESS.008': ('P13.SUCCESS.008.01',),
 'P13.SUCCESS.009': ('P13.SUCCESS.009.01',),
 'P13.FAILURE.007': ('P13.FAILURE.007.01',),
 'P13.FAILURE.008': ('P13.FAILURE.008.01',),
 'P13.FAILURE.009': ('P13.FAILURE.009.01',),
 'P13.HINT.1': (),
 'P13.HINT.2': (),
 'P13.HINT.3': (),
 'VC04.ENTRY': ('VC04.ENTRY.01', 'VC04.ENTRY.02', 'VC04.ENTRY.03'),
 'VC04.REMATCH': ('VC04.REMATCH.01',),
 'VC04.NOT_READY': (),
 'VC04.NEED_RESOLUTION': ()}
UNIT_SPEAKERS = {'P13.OPEN.001.01': 'jack',
 'P13.OPEN.001.02': 'bunny',
 'P13.OPEN.001.03': 'frankie',
 'P13.LOOK.001.01': 'jack',
 'P13.LOOK.002.01': 'jack',
 'P13.SUCCESS.001.01': 'milo',
 'P13.SUCCESS.001.02': 'jack',
 'P13.SUCCESS.001.03': 'milo',
 'P13.DIALOGUE.001.01': 'bunny',
 'P13.DIALOGUE.002.01': 'felix',
 'P13.DIALOGUE.003.01': 'frankie',
 'P13.SUCCESS.002.01': 'bunny',
 'P13.SUCCESS.003.01': 'jack',
 'P13.FAILURE.001.01': 'bunny',
 'P13.FAILURE.002.01': 'jack',
 'P13.FAILURE.003.01': 'felix',
 'P13.FAILURE.004.01': 'rita',
 'P13.DIALOGUE.004.01': 'rita',
 'P13.SUCCESS.004.01': 'felix',
 'P13.SUCCESS.004.02': 'vivian',
 'P13.SUCCESS.004.03': 'felix',
 'P13.FAILURE.005.01': 'vivian',
 'P13.SUCCESS.005.01': 'jack',
 'P13.DIALOGUE.005.01': 'rita',
 'P13.DIALOGUE.005.02': 'bunny',
 'P13.DIALOGUE.005.03': 'rita',
 'P13.DIALOGUE.005.04': 'stringer',
 'P13.DIALOGUE.005.05': 'rita',
 'P13.SUCCESS.006.01': 'jack',
 'P13.SUCCESS.007.01': 'frankie',
 'P13.FAILURE.006.01': 'frankie',
 'P13.SUCCESS.008.01': 'jack',
 'P13.SUCCESS.009.01': 'jack',
 'P13.FAILURE.007.01': 'frankie',
 'P13.FAILURE.008.01': 'jack',
 'P13.FAILURE.009.01': 'frankie',
 'VC04.ENTRY.01': 'stringer',
 'VC04.ENTRY.02': 'jack',
 'VC04.ENTRY.03': 'stringer',
 'VC04.REMATCH.01': 'stringer'}


@dataclass
class P13World(_LateWorld):
    start_at: int=0
    program_at: int=0
    seated_at: int=0
    pot_at: int=0
    served_at: int=0
    display_at: int=0
    screen_at: int=0
    show_at: int=0
    board_at: int=0
    toast_at: int=0
    contest_request_at: int=0
    wrong_at: int=0
    wrong_source: str=''
    wrong_visual_at: int=0
    laugh_at: int=0
    attempts: int=0
    autosaves: dict[str,int]=field(default_factory=dict)
    PUZZLE: ClassVar[str]='P13'
    KIND: ClassVar[str]=SAVE_KIND
    SOURCES: ClassVar[dict[str,str]]={
        'opening':'P13.OPEN.001','rack':'P13.LOOK.001','serve_preview':'P13.READ.001',
        'show_preview':'P13.READ.002','toast_preview':'P13.READ.003','program':'P13.READ.004',
        'pot_help':'P13.DIALOGUE.001','display_help':'P13.DIALOGUE.002','board_help':'P13.DIALOGUE.003',
        'rita_ready':'P13.DIALOGUE.004','reveal':'P13.DIALOGUE.005','attention':'P13.SUCCESS.008',
        'wrong_pot':'P13.FAILURE.001','wrong_people':'P13.FAILURE.002','wrong_display':'P13.FAILURE.003'}
    UNITS: ClassVar=RECORD_UNITS
    SPEAKERS: ClassVar=UNIT_SPEAKERS

    @property
    def inventory(self):return (PROGRAM,) if self.start_at and not self.program_at else ()
    @property
    def reserved_external_objects(self):return frozenset(('hotpot_pot','handcart','folded_display',BOARD,PROGRAM)) if self.start_at else frozenset()
    @property
    def flags(self):
        return frozenset(n for n,v in (('SERVED',self.served_at),('DISPLAY_REVEALED',self.show_at),('TOAST_READY',self.toast_at)) if v)
    @property
    def ready(self):return bool(self.toast_at)
    @property
    def rita_consented(self):return self._complete('rita_ready')
    @property
    def contest_eligible(self):return bool(self.served_at and self.show_at and self.board_at)
    @property
    def pot_location(self):return 'buffet' if self.pot_at else KITCHEN
    @property
    def display_location(self):return 'display_footprint' if self.display_at else 'staging_pocket'
    @property
    def pending_contest_request_id(self):return f'P13:{self._epoch}:VC04:{self.contest_request_at}' if self.contest_request_at else None
    @property
    def pending_wrong_visual_id(self):return f'P13:{self._epoch}:wrong:{self.wrong_at}' if self.wrong_at and not self.wrong_visual_at else None
    @property
    def pending_autosaves(self):
        return tuple({'cue':cue,'serial':serial,'request_id':f'P13:{self._epoch}:save:{cue}:{serial}'}
                     for cue,serial in self._cue_serials().items() if serial and cue not in self.autosaves)
    def _cue_serials(self):return dict(zip(ORDER,(self.served_at,self.show_at,self.toast_at)))

    def start(self,c,pot_handoff,display_handoff):
        if type(c) is not P13Context:raise ValueError('P13 context required')
        block=self._scene(c)
        if block is not None:return block
        if self.start_at:return self._result('deliveries_already_started')
        if not PREREQUISITES<=c.flags:return self._result('p12_required')
        if not c.welcome_cleared:return self._result('p12_collection_handoff_required')
        p,d=pot_handoff,display_handoff
        if (type(p) is not dict or p.get('object_id')!='hotpot_pot' or p.get('room')!=KITCHEN
                or p.get('lid_closed') is not True or type(p.get('portions')) is not int or p['portions']!=8
                or p.get('portion_kind')!='tasting' or p.get('includes_jackie') is not True):
            raise ValueError('The single cooked P07 pot is required')
        if (type(d) is not dict or d.get('display_id')!='folded_display' or d.get('cart_id')!='handcart'
                or d.get('location')!=SIDE or d.get('position')!='staging_pocket'
                or any(d.get(x) is not True for x in ('folded','padded','covered','undamaged'))
                or d.get('panel_revealed') is not False or d.get('rita_reveal_consent') is not False
                or d.get('transport_owner')!='P13'):
            raise ValueError('The safely staged P11 cart and covered display are required')
        if PROGRAM in c.inventory:raise ValueError('Program already exists outside P13')
        self.start_at=self.revision+1
        return self._commit('deliveries_started','P13_DELIVERY_OWNERSHIP','ownership',
            transfer_from={'hotpot_pot':'P07','folded_display':'P11','handcart':'P11'},
            owner='P13', board_location=LIVING, program_owner='inventory')

    def _block(self,c,room=COURTYARD):
        if type(c) is not P13Context:raise ValueError('P13 context required')
        block=self._scene(c,room)
        if block is not None:return block
        if not self.start_at:return self._result('delivery_handoff_required')
        if self.contest_request_at:return self._result('contest_request_pending')
        self.validate_context(c)
        return None

    def _presentation_block(self,c,source,tokens):
        room=KITCHEN if source in ('pot_help','wrong_pot') else c.room if source in ('display_help','board_help','wrong_people','wrong_display') else COURTYARD
        block=self._block(c,room)
        if block is not None:return block
        if source=='rita_ready' and not self.served_at:return self._result('serve_first','P13.FAILURE.004')
        if source=='reveal' and not self.screen_at:return self._result('screen_still_closed')
        if source=='attention':
            if not self.contest_eligible:return self._result('deliveries_required','P13.FAILURE.007')
            if not c.resolved('VC04'):return self._result('vc04_resolution_required','VC04.NEED_RESOLUTION')
            if not c.rig.working:return self._result('working_microphone_required')
        if source.startswith('wrong_') and source!=self.wrong_source:return self._result('wrong_scene_not_triggered')
        return self._speakers(c,tokens)

    def preview(self,c,cue):
        if cue not in ORDER:raise ValueError('Unknown cue')
        return self.begin_presentation(c,cue.lower()+'_preview')

    def route_preview(self,c,cue):
        if cue not in ORDER:raise ValueError('Unknown cue')
        if type(c) is not P13Context:raise ValueError('P13 context required')
        load={'SERVE':('people','hotpot_pot'),'SHOW':('folded_display','handcart'),'TOAST':(BOARD,)}[cue]
        destination={'SERVE':'buffet','SHOW':'display_footprint','TOAST':'pledge_board_position'}[cue]
        return {'cue':cue,'record_id':self.SOURCES[cue.lower()+'_preview'],'load_ids':load,
            'destination_id':destination,'route_ids':ROUTES,
            'pot_fits_hatch':True,'people_use_house':True,'display_fits_hatch':False,
            'display_requires_folded_width':True,'guest_lane_occupied':not c.queue_clear,
            'gate_lane_occupied':not c.lane_clear,'footprint_occupied':not c.footprint_clear,
            'buffet_ready':c.buffet_at_hatch and c.hatch_visible,'timer':None}

    def blocked_layout_binding(self,c,cue):
        # Exact already-approved P08 hotspot labels, not new failure prose.
        labels=(('P08.LABEL.002','Hatch-side buffet position',c.buffet_at_hatch),
                ('P08.LABEL.006','Kitchen hatch',c.hatch_visible)) if cue=='SERVE' else (
                ('P08.LABEL.001','Gate-to-house lane',c.lane_clear),
                ('P08.LABEL.004','Display alcove',c.footprint_clear and c.display_concealed))
        blocked=next(((id,text) for id,text,ready in labels if not ready),None)
        return {'blocked_place_name':blocked[1],'label_record_id':blocked[0]} if blocked else {}

    def _route_feedback(self,code,*records):
        self.attempts+=1
        return self._commit(code,'P13_ROUTE_ATTEMPT','route',records=records,
            load_unchanged=True,attempt=self.attempts)

    def _wrong(self,c,source):
        self.attempts+=1
        if not self.wrong_at:
            self.wrong_at=self.revision+1
            self.wrong_source=source
        return self._commit('wrong_route','P13_ROUTE_ATTEMPT','route',
            records=(self.SOURCES[source],), load_unchanged=True, attempt=self.attempts)

    def give_program(self,c,route='house_doorway'):
        if route not in ROUTES:raise ValueError('Unknown route')
        block=self._block(c,PORCH)
        if block is not None:return block
        if self.program_at:return self._result('program_already_given')
        if not c.at('milo',PORCH):return self._result('milo_absent')
        if route=='kitchen_hatch':return self._wrong(c,'wrong_people')
        if route!='house_doorway':return self._route_feedback('people_need_house','P13.READ.001')
        self.program_at=self.revision+1;self.attempts+=1
        return self._commit('guest_route_requested','P13_GUEST_ROUTE','movement',
            records=('P13.SUCCESS.001',), card_id=PROGRAM, card_to='milo',
            route=(PORCH,LIVING,'rear_arch',COURTYARD),milo_joins_after_queue=True)

    def confirm_seating(self,c):
        block=self._block(c)
        if block is not None:return block
        if self.seated_at:return self._result('already_seated')
        if not self.program_at or not c.queue_clear or not c.at('milo',COURTYARD):return self._result('guest_route_not_yet_clear')
        self.seated_at=self.revision+1
        return self._commit('guests_seated','P13_GUEST_ROUTE_COMPLETE','movement')

    def deliver_pot(self,c,route='kitchen_hatch'):
        if route not in ROUTES:raise ValueError('Unknown route')
        block=self._block(c,KITCHEN)
        if block is not None:return block
        if self.pot_at:return self._result('pot_already_delivered')
        if not (c.at('bunny',KITCHEN) and c.at('frankie',COURTYARD)):return self._result('helpers_absent')
        if route=='house_doorway':return self._wrong(c,'wrong_pot')
        if route!='kitchen_hatch':return self._route_feedback('pot_needs_hatch','P13.READ.001')
        if not self.seated_at or not c.queue_clear:return self._result('clear_guest_queue_first')
        if not (c.buffet_at_hatch and c.hatch_visible):return self._result('buffet_or_hatch_blocked','P13.FAILURE.009')
        self.pot_at=self.revision+1;self.attempts+=1
        return self._commit('pot_delivered','P13_POT_DELIVERED','movement',records=('P13.SUCCESS.002',),
            object_id='hotpot_pot',from_room=KITCHEN,to_room=COURTYARD,position='buffet',route=route)

    def _cue(self,c,cue,field,record):
        setattr(self,field,self.revision+1)
        r=self._commit(cue.lower()+'_complete','P13_'+cue,'puzzle',records=(record,),cue=cue)
        pending=next(x for x in self.pending_autosaves if x['cue']==cue)
        return CaptionResult('',r.events+(Event('P13_AUTOSAVE_REQUEST','autosave',pending),),r.code,r.line_ids)

    def pull_serve(self,c):
        block=self._block(c)
        if block is not None:return block
        if self.served_at:return self._result('serve_already_complete')
        if not self.pot_at:return self._result('food_not_delivered')
        return self._cue(c,'SERVE','served_at','P13.SUCCESS.003')

    def ask_rita(self,c):return self.begin_presentation(c,'rita_ready')

    def deliver_display(self,c,route='side_gate'):
        if route not in ROUTES:raise ValueError('Unknown route')
        block=self._block(c,SIDE)
        if block is not None:return block
        if self.display_at:return self._result('display_already_delivered')
        if not self.served_at:return self._result('serve_first','P13.FAILURE.004')
        if not self.rita_consented:return self._result('rita_consent_required')
        if not all(c.at(p,SIDE) for p in ('felix','vivian')):return self._result('transport_helpers_absent')
        if route=='kitchen_hatch':return self._wrong(c,'wrong_display')
        if route!='side_gate':return self._route_feedback('display_needs_gate','P13.READ.002')
        g=c.gate
        if g is None or not (g.tested and g.peg_available and g.peg_engaged and g.gate_open):return self._result('tested_peg_required')
        if not (c.lane_clear and c.footprint_clear and c.display_concealed):return self._result('display_lane_or_footprint_blocked','P13.FAILURE.009')
        self.display_at=self.revision+1;self.attempts+=1
        return self._commit('display_delivered','P13_DISPLAY_DELIVERED','movement',records=('P13.SUCCESS.004',),
            object_ids=('folded_display','handcart'),from_room=SIDE,to_room=COURTYARD,
            position='display_footprint',covered=True,helpers=('felix','vivian'))

    def open_screen(self,c):
        block=self._block(c)
        if block is not None:return block
        if self.screen_at:return self._result('viewing_side_already_open')
        if not self.display_at:return self._result('footprint_required','P13.FAILURE.005')
        if not self.rita_consented or not c.at('rita',COURTYARD):return self._result('rita_consent_and_presence_required')
        if not c.display_concealed:return self._result('screen_required')
        self.screen_at=self.revision+1
        return self._commit('viewing_side_open','P13_SCREEN_OPENED',records=('P13.SUCCESS.005',),
            display_reveal_owner='rita',damage=False)

    def pull_show(self,c):
        block=self._block(c)
        if block is not None:return block
        if self.show_at:return self._result('show_already_complete')
        if not self._complete('reveal'):return self._result('rita_presentation_required')
        return self._cue(c,'SHOW','show_at','P13.SUCCESS.006')

    def deliver_board(self,c,route='house_doorway'):
        if route not in ROUTES:raise ValueError('Unknown route')
        block=self._block(c,LIVING)
        if block is not None:return block
        if self.board_at:return self._result('board_already_delivered')
        if not self.show_at:return self._result('show_required','P13.FAILURE.007')
        if not self.seated_at or not c.queue_clear:return self._result('guest_queue_occupied','P13.FAILURE.006')
        if c.board_room!=LIVING or not c.at('frankie',LIVING):return self._result('board_and_frankie_required')
        if route!='house_doorway':return self._route_feedback('board_needs_house_route','P13.READ.003')
        self.board_at=self.revision+1;self.attempts+=1
        return self._commit('board_delivered','P13_BOARD_DELIVERED','movement',records=('P13.SUCCESS.007',),
            object_id=BOARD,from_room=LIVING,to_room=COURTYARD,helper='frankie',route=route)

    def request_contest(self,c):
        if self.contest_request_at:return self._result('contest_request_pending')
        block=self._block(c)
        if block is not None:return block
        if not self.contest_eligible:return self._result('contest_not_ready','VC04.NOT_READY')
        if not c.at('stringer',COURTYARD):return self._result('stringer_absent')
        self.contest_request_at=self.revision+1
        return self._commit('contest_requested','P13_VC04_REQUEST','contest_request',
            records=('VC04.REMATCH' if c.resolved('VC04') else 'VC04.ENTRY',),
            request_id=self.pending_contest_request_id,encounter='VC04',safe=True)

    def finish_contest_request(self,request_id,accepted=False):
        if type(accepted) is not bool:raise ValueError('Invalid contest receipt')
        if not request_id or request_id!=self.pending_contest_request_id:return self._result('stale_contest_request')
        self.contest_request_at=0
        return self._commit('contest_request_acknowledged' if accepted else 'contest_request_cancelled',
            'P13_CONTEST_HANDOFF','handoff',accepted=accepted)

    def call_attention(self,c):return self.begin_presentation(c,'attention')
    def pull_toast(self,c):
        block=self._block(c)
        if block is not None:return block
        if self.toast_at:return self._result('toast_already_complete')
        if not self.contest_eligible:return self._result('deliveries_required','P13.FAILURE.007')
        if not c.resolved('VC04'):return self._result('vc04_resolution_required','VC04.NEED_RESOLUTION')
        if not c.rig.working:return self._result('working_microphone_required')
        if not self._complete('attention'):return self._result('attention_text_required')
        return self._cue(c,'TOAST','toast_at','P13.SUCCESS.009')

    def acknowledge_autosave(self,request_id):
        match=next((x for x in self.pending_autosaves if x['request_id']==request_id),None)
        if match is None:return self._result('stale_autosave')
        self.autosaves[match['cue']]=self.revision+1
        return self._commit('autosave_acknowledged','P13_AUTOSAVE_ACK','autosave_ack',cue=match['cue'])

    def acknowledge_wrong_visual(self,c,request_id):
        block=self._block(c,c.room)
        if block is not None:return block
        if request_id is None or request_id!=self.pending_wrong_visual_id:return self._result('stale_visual')
        if not self._complete(self.wrong_source):return self._result('wrong_route_caption_required')
        self.wrong_visual_at=self.revision+1
        return self._commit('wrong_visual_presented','P13_WRONG_VISUAL','presentation')

    def claim_laugh(self,c):
        block=self._block(c,c.room)
        if block is not None:return block
        if self.laugh_at:return self._result('laugh_consumed')
        if not self.wrong_visual_at or self.show_at or self.screen_at:return self._result('laugh_window_closed')
        self.laugh_at=self.revision+1
        return self._commit('laugh_consumed','LAF13','laugh')

    def protect_furniture(self,c,obj):
        # Caller applies any allowed movement through P08, then reprojects layout.
        protected = ({'ceramic_carrier','serving_table','credit_slate'} if self.pot_at else set()) | ({'completed_screen'} if self.display_at else set())
        if obj in protected:return self._result('occupied_furniture_protected','P13.FAILURE.008')
        return self._result('movement_owned_by_p08')

    def dispatch(self,c,verb,obj,target=None):
        if not isinstance(verb,Verb):verb=Verb(verb)
        if verb==Verb.PULL and obj in ORDER:return {'SERVE':self.pull_serve,'SHOW':self.pull_show,'TOAST':self.pull_toast}[obj](c)
        if verb==Verb.GIVE and obj==PROGRAM and target=='milo':return self.give_program(c)
        if verb==Verb.GIVE and obj==BOARD and target=='frankie':return self.deliver_board(c)
        if verb==Verb.USE and obj=='hotpot_pot' and target in ROUTES:return self.deliver_pot(c,target)
        if verb==Verb.USE and obj=='folded_display' and target in ROUTES:return self.deliver_display(c,target)
        if verb==Verb.USE and obj=='screen_pull_tab':return self.open_screen(c)
        if verb==Verb.USE and obj=='microphone':return self.call_attention(c)
        if verb==Verb.TALK_TO and obj=='rita':return self.ask_rita(c)
        return self._result('unhandled_action')

    def validate_context(self,c):
        if type(c) is not P13Context:raise ValueError('P13 context required')
        if self.start_at and (not PREREQUISITES<=c.flags or not c.welcome_cleared):raise ValueError('Missing P13 prerequisites')
        if self.reserved_external_objects & c.inventory:raise ValueError('Duplicate delivery inventory')
        if self.board_at and c.board_room!=COURTYARD:raise ValueError('Board projection not delivered')
        if self.toast_at and not c.resolved('VC04'):raise ValueError('Toast without contest result')
        if self.pot_at and not c.buffet_at_hatch:raise ValueError('Occupied buffet moved')

    def validate(self):
        self._validate_captions()
        names=('start_at','program_at','seated_at','pot_at','served_at','display_at','screen_at','show_at',
               'board_at','toast_at','contest_request_at','wrong_at','wrong_visual_at','laugh_at')
        self._validate_serials(*names)
        if type(self.attempts) is not int or not 0<=self.attempts<=self.revision:raise ValueError('Invalid turns')
        if type(self.autosaves) is not dict or not set(self.autosaves)<=set(ORDER):raise ValueError('Invalid autosaves')
        if not self.start_at and (self.presentations or self.attempts or self.autosaves or any(getattr(self,n) for n in names[1:])):raise ValueError('P13 state before handoff')
        chain=(self.start_at,self.program_at,self.seated_at,self.pot_at,self.served_at,self.display_at,self.screen_at,self.show_at,self.board_at,self.toast_at)
        for prior,current in zip(chain,chain[1:]):
            if current and not 0<prior<current:raise ValueError('Delivery order violated')
        if self.display_at and not self.served_at<self._done_at('rita_ready')<self.display_at:raise ValueError('Display without Rita consent')
        if self.show_at and not self.screen_at<self._done_at('reveal')<self.show_at:raise ValueError('Show before Rita presentation')
        if self.toast_at and not self.board_at<self._done_at('attention')<self.toast_at:raise ValueError('Toast before attention')
        if self.contest_request_at and not self.board_at<self.contest_request_at:raise ValueError('Premature VC04')
        if self.wrong_at:
            if self.wrong_source not in ('wrong_pot','wrong_people','wrong_display') or not self.start_at<self.wrong_at:raise ValueError('Invalid wrong route')
        elif self.wrong_source or self.wrong_visual_at or self.laugh_at:raise ValueError('Untriggered wrong scene')
        if self.wrong_visual_at and not self.wrong_at<self._done_at(self.wrong_source)<self.wrong_visual_at:raise ValueError('Unpresented wrong-route scene')
        if self.laugh_at and not 0<self.wrong_visual_at<self.laugh_at:raise ValueError('Unpresented wrong-route laugh')
        for cue,serial in self.autosaves.items():
            if type(serial) is not int or not 0<self._cue_serials()[cue]<serial<=self.revision:raise ValueError('Invalid autosave receipt')
        for source,p in self.presentations.items():
            gate={'rita_ready':self.served_at,'reveal':self.screen_at,'attention':self.board_at}.get(source,self.start_at)
            if not 0<gate<p.serial:raise ValueError('Premature scene')
