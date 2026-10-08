"""NEW import shell and selected retained helpers; full retained P13Tests below.
All these tests use synthetic-shaped contexts; genuine owner joins are separate.
No reconstruction of the missing historical late-campaign test suite is claimed.
"""
import copy,json,itertools,unittest
from dataclasses import replace
from pathlib import Path
from hashlib import sha256
from cakood.model import Verb
from cakood.p04_model import GateHandoff
from cakood.p10_model import TILE_IDS,ORDER
from cakood.p12_model import P12World,P12Context,CurrentRig,PEOPLE,COURTYARD,KITCHEN,LIVING,SIDE,PORCH
from cakood.p12_model import PREREQUISITES as P12REQ
from cakood.p13_model import P13World,P13Context,PREREQUISITES as P13REQ,PROGRAM,BOARD
from cakood.verbal_contest import VerbalContests,Phase
from test_verbal_contest import CATALOG,prepared,play,leave
RIG=CurrentRig(COURTYARD,True,'MIC',True)
ACTORS=tuple((p,COURTYARD) for p in PEOPLE[1:])
GATE=GateHandoff('hold_open_peg',SIDE,True,True,True,True,False,())
RACK={'rack_id':'cue_rack','location':COURTYARD,'slots':TILE_IDS,'words':ORDER,'first_restored_serial':1}
POT={'object_id':'hotpot_pot','room':KITCHEN,'lid_closed':True,'portions':8,'portion_kind':'tasting','includes_jackie':True}
DISPLAY={'display_id':'folded_display','cart_id':'handcart','location':SIDE,'position':'staging_pocket','folded':True,'padded':True,'covered':True,'undamaged':True,'panel_revealed':False,'rita_reveal_consent':False,'transport_owner':'P13'}


def contests(wins=(),losses=()):
    w=VerbalContests(CATALOG)
    for enc in (*wins,*losses):
        prepared(enc,w);play(w,[enc in wins]*3,enc);leave(w)
    return w


def read(w,c,source):
    p=w.begin_presentation(c,source)
    if p.presentation_id:
        w.acknowledge_presentation(c,p.presentation_id,record_id=w.SOURCES[source])
    return p


def clone(w,c=None):return type(w).load(json.loads(json.dumps(w.save())),context=c)
def actors(c,**updates):return replace(c,npc_locations=tuple({**dict(c.npc_locations),**updates}.items()))
def c12(vc=None):return P12Context(COURTYARD,flags=P12REQ,npc_locations=ACTORS,rig=RIG,contests=vc or contests(losses=('VC03',)))
def c13(vc=None):return P13Context(COURTYARD,flags=P13REQ,npc_locations=ACTORS,rig=RIG,contests=vc or contests(losses=('VC04',)),gate=GATE,welcome_cleared=True,queue_clear=True,buffet_at_hatch=True,hatch_visible=True,display_concealed=True,lane_clear=True,footprint_clear=True)


def repair12(c=None,w=None,ask=False):
    c=c or c12();w=w or P12World();w.start(c,RACK)
    a=replace(c,on_apron=True);read(w,a,'audience_view' if ask else 'self_view')
    w.release_catch(a);w.rotate_rack(c);w.order_cards(c,TILE_IDS)
    return w,c


def finish12():
    w,c=repair12();read(w,c,'introduction');w.commit_introduction(c);w.release_confetti(c)
    read(w,c,'confetti');read(w,c,'cleanup');w.finish_welcome(c)
    return w,c


def serve13(w=None,c=None):
    w=w or P13World();c=c or c13();w.start(c,POT,DISPLAY)
    p=actors(replace(c,room=PORCH),milo=PORCH);w.give_program(p);w.confirm_seating(c)
    kitchen=actors(replace(c,room=KITCHEN),bunny=KITCHEN)
    w.deliver_pot(kitchen);w.pull_serve(c)
    return w,c


def show13(w=None,c=None):
    w,c=serve13(w,c);read(w,c,'rita_ready')
    side=actors(replace(c,room=SIDE),felix=SIDE,vivian=SIDE)
    w.deliver_display(side);w.open_screen(c);read(w,c,'reveal');w.pull_show(c)
    return w,c


def finish13(w=None,c=None):
    w,c=show13(w,c)
    living=actors(replace(c,room=LIVING),frankie=LIVING);w.deliver_board(living)
    c=replace(c,board_room=COURTYARD);read(w,c,'attention');w.pull_toast(c)
    return w,c


class P13Tests(unittest.TestCase):
    def test_single_objects_and_p12_collection_required(self):
        w=P13World();c=c13()
        self.assertEqual(w.start(replace(c,welcome_cleared=False),POT,DISPLAY).code,'p12_collection_handoff_required')
        for p,d in (({**POT,'portions':7},DISPLAY),(POT,{**DISPLAY,'covered':False}),(POT,{**DISPLAY,'rita_reveal_consent':True})):
            with self.assertRaises(ValueError):w.start(c,p,d)
        w.start(c,POT,DISPLAY);self.assertEqual(w.inventory,(PROGRAM,))
        before=w.save();w.start(c,POT,DISPLAY);self.assertEqual(w.save(),before)
        self.assertIn('handcart',w.reserved_external_objects)

    def test_practical_deliveries_preserve_actual_locations(self):
        w,c=serve13();self.assertEqual(w.pot_location,'buffet');self.assertNotIn('hotpot_pot',w.inventory)
        self.assertEqual(w.flags,{'SERVED'});self.assertFalse(w.rita_consented)
        self.assertEqual(w.open_screen(c).code,'footprint_required')
        side=actors(replace(c,room=SIDE),felix=SIDE,vivian=SIDE)
        self.assertEqual(w.deliver_display(side).code,'rita_consent_required')
        read(w,c,'rita_ready')
        for change in ({'lane_clear':False},{'footprint_clear':False},{'display_concealed':False},{'gate':replace(GATE,peg_engaged=False)}):
            before=w.save();w.deliver_display(replace(side,**change));self.assertEqual(w.save(),before)
        w.deliver_display(side);self.assertEqual(w.display_location,'display_footprint')
        self.assertFalse(w.screen_at);self.assertNotIn('DISPLAY_REVEALED',w.flags)

    def test_actual_rita_caption_consent_no_audio_or_query(self):
        w,c=serve13();p=w.ask_rita(c);self.assertFalse(w.rita_consented)
        w.audio_finished();self.assertFalse(w.rita_consented)
        old=p.presentation_id;w=clone(w);self.assertEqual(w.acknowledge_presentation(c,old,record_id='P13.DIALOGUE.004').code,'stale_presentation')
        read(w,c,'rita_ready');self.assertTrue(w.rita_consented)

    def test_reveal_prefixes_cannot_skip_show(self):
        for prefix in range(6):
            w,c=serve13();read(w,c,'rita_ready')
            w.deliver_display(actors(replace(c,room=SIDE),felix=SIDE,vivian=SIDE));w.open_screen(c)
            p=w.begin_presentation(c,'reveal');tokens=w._tokens('reveal')
            if prefix:w.acknowledge_presentation(c,p.presentation_id,speech_unit_ids=tokens[:prefix])
            w=clone(w)
            if prefix<len(tokens):
                self.assertEqual(w.pull_show(c).code,'rita_presentation_required');read(w,c,'reveal')
            w.pull_show(c);self.assertIn('DISPLAY_REVEALED',w.flags)

    def test_guest_queue_program_and_board_real_handoffs(self):
        w=P13World();c=c13();w.start(c,POT,DISPLAY)
        self.assertEqual(w.confirm_seating(c).code,'guest_route_not_yet_clear')
        w.give_program(actors(replace(c,room=PORCH),milo=PORCH))
        self.assertEqual(w.inventory,());self.assertEqual(w.confirm_seating(replace(c,queue_clear=False)).code,'guest_route_not_yet_clear')
        w,c=show13();living=actors(replace(c,room=LIVING),frankie=LIVING)
        for change in ({'queue_clear':False},{'board_room':COURTYARD}):
            before=w.save();w.deliver_board(replace(living,**change));self.assertEqual(w.save(),before)
        w.deliver_board(living);self.assertTrue(w.contest_eligible)
        with self.assertRaises(ValueError):w.validate_context(c)
        w.validate_context(replace(c,board_room=COURTYARD))

    def test_vc04_safe_request_cancel_rematch_and_actual_resolution(self):
        c=c13(contests());w=P13World();w.start(c,POT,DISPLAY)
        self.assertEqual(w.request_contest(c).code,'contest_not_ready')
        w,c=show13(c=c);w.deliver_board(actors(replace(c,room=LIVING),frankie=LIVING));c=replace(c,board_room=COURTYARD)
        r=w.request_contest(c);old=w.pending_contest_request_id
        self.assertEqual(r.line_ids,('VC04.ENTRY',));w=clone(w)
        self.assertEqual(w.finish_contest_request(old).code,'stale_contest_request')
        w.finish_contest_request(w.pending_contest_request_id,False)
        self.assertEqual(w.call_attention(c).code,'vc04_resolution_required')
        prepared('VC04',c.contests);play(c.contests,[False]*3,'VC04');leave(c.contests)
        read(w,c,'attention');w.pull_toast(c);self.assertTrue(w.ready)
        self.assertFalse(c.contests.progress['VC04'].won)
        self.assertEqual(w.request_contest(c).line_ids,('VC04.REMATCH',))

    def test_autosave_each_cue_durable_and_stale_after_load(self):
        w,c=finish13();self.assertEqual([x['cue'] for x in w.pending_autosaves],list(ORDER))
        old=w.pending_autosaves[0]['request_id'];w=clone(w,c)
        self.assertEqual(w.acknowledge_autosave(old).code,'stale_autosave')
        for req in tuple(w.pending_autosaves):w.acknowledge_autosave(req['request_id'])
        self.assertEqual(w.pending_autosaves,())
        before=w.save();w.pull_serve(c);w.pull_show(c);w.pull_toast(c);self.assertEqual(w.save(),before)

    def test_wrong_route_laugh_requires_caption_and_rendered_visual(self):
        w=P13World();c=c13();w.start(c,POT,DISPLAY)
        kitchen=actors(replace(c,room=KITCHEN),bunny=KITCHEN)
        w.deliver_pot(kitchen,'house_doorway');self.assertEqual(w.pot_location,KITCHEN)
        self.assertFalse(w.claim_laugh(kitchen).events)
        read(w,kitchen,'wrong_pot');self.assertFalse(w.claim_laugh(kitchen).events)
        w.acknowledge_wrong_visual(kitchen,w.pending_wrong_visual_id)
        self.assertEqual(w.claim_laugh(kitchen).events[0].id,'LAF13')
        w=clone(w);w.deliver_pot(kitchen,'house_doorway');self.assertFalse(w.claim_laugh(kitchen).events)

    def test_occupied_furniture_and_current_mic(self):
        w,c=finish13();self.assertEqual(w.protect_furniture(c,'serving_table').line_ids,('P13.FAILURE.008',))
        self.assertEqual(w.protect_furniture(c,'completed_screen').code,'occupied_furniture_protected')
        self.assertEqual(w.protect_furniture(c,'pa_kit').code,'movement_owned_by_p08')
        w,c=show13();w.deliver_board(actors(replace(c,room=LIVING),frankie=LIVING));c=replace(c,board_room=COURTYARD)
        for rig in (replace(RIG,source='TAPE'),replace(RIG,connected=False),replace(RIG,facing_inward=False)):
            self.assertEqual(w.call_attention(replace(c,rig=rig)).code,'working_microphone_required')

