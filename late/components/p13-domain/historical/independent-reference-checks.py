"""Independent finite P13 review; no producer writes or native acceptance.

Run on the freshly materialized candidate. Assertions use unittest under -O.
The composed restart fixture below is review coordination, not production host
implementation or proof of atomic cross-owner publication.
"""
from pathlib import Path
import copy, hashlib, json, os, sys, unittest
from dataclasses import replace

ROOT = Path(__file__).resolve().parent
PACKET = ROOT / 'candidate/p13-reference-reconstruction'
C = PACKET / 'component'
D = C / 'stock-sci/p13-domain-adapter'
sys.path[:0] = [str(C), str(C/'tests'), str(D), str(D/'tests')]
from current_join import *
from cakood.verbal_contest import VerbalContests
from cakood.p13_model import PROGRAM
from cakood.p08_model import Facing
from tools.assertions import load
from test_verbal_contest import CATALOG
from dependencies.p07_owner.cakood.composition import HostPreparationError
td = load('independent_retained_domain_helpers', D/'tests/test_domain.py')

COUNTS = dict(restarts=0, source_query_snapshots=0, source_operation_comparisons=0, immutable_failures=0)
OBSERVATIONS = []

class Independent(unittest.TestCase):
    def roundtrip(self, j, label):
        """Explicitly coordinate owner reloading at one logical boundary."""
        before = dict(p13=j.w.save(), p7=j.h7.save_campaign_fixture(),
                      p11=j.p11.save(), p12=j.p12.save(), p8=j.p8.save(),
                      p4=j.p4.save(), vc=j.vc.save().decode(),
                      actors=j.actors, physical=j.physical, queue=j.queue_clear,
                      board=j.board_room)
        target=ROOT/'snapshots'/('optimized' if sys.flags.optimize else 'normal')
        target.mkdir(parents=True, exist_ok=True)
        path=target/(str(COUNTS['restarts']).zfill(3)+'-'+label+'.json')
        with path.open('w') as out:
            json.dump(before,out,indent=2);out.flush();os.fsync(out.fileno())
        saved=json.loads(path.read_text())
        j.p7,j.h7=MemoryTransactionHost.load_campaign_fixture(saved['p7'],j.c7)
        j.c7=replace(j.c7,ownership=j.h7.ownership_context())
        j.p11=P11World.load(saved['p11'])
        j.p12=P12World.load(saved['p12'])
        j.p8=P08World.load(saved['p8'])
        j.p4=P04();j.p4.load(saved['p4'])
        j.vc=VerbalContests.load(saved['vc'].encode(),CATALOG,
                               owner_generation=j.vc.owner_generation+1)
        j.c12=replace(j.c12,contests=j.vc)
        j.actors=saved['actors'];j.physical={k:tuple(v) for k,v in saved['physical'].items()}
        j.queue_clear=saved['queue'];j.board_room=saved['board']
        j.w=P13World.load(saved['p13'],context=j.context())
        self.assertEqual(j.w.save(),before['p13'])
        self.assertEqual(j.h7.save_campaign_fixture(),before['p7'])
        self.assertEqual(j.p11.save(),before['p11'])
        self.assertEqual(j.p12.save(),before['p12'])
        self.assertEqual(j.p4.save(),before['p4'])
        self.assertEqual(j.vc.save().decode(),before['vc'])
        h=td.Harness(world=P13World.load(j.w.save(),context=j.context()))
        h.project(j.context());h.queries()
        COUNTS['source_query_snapshots']+=1;COUNTS['restarts']+=1
        for fn,method,room,args in (
            ('give_program','p13GiveProgram',PORCH,()),
            ('confirm_seating','p13ConfirmSeating',COURTYARD,()),
            ('deliver_pot','p13DeliverPot',KITCHEN,()),
            ('pull_serve','p13PullServe',COURTYARD,()),
            ('deliver_display','p13DeliverDisplay',SIDE,()),
            ('open_screen','p13OpenScreen',COURTYARD,()),
            ('pull_show','p13PullShow',COURTYARD,()),
            ('deliver_board','p13DeliverBoard',LIVING,()),
            ('request_contest','p13RequestContest',COURTYARD,()),
            ('begin_presentation','p13Begin',COURTYARD,('attention',)),
            ('pull_toast','p13PullToast',COURTYARD,())):
            h=td.Harness(world=P13World.load(j.w.save(),context=j.context()))
            h.action(fn,method,*args,c=j.context(room))
            COUNTS['source_operation_comparisons']+=1

    def unchanged(self,j,fn,context,expected,*args):
        before=j.w.save();owners=(j.p7.save(),j.p11.save(),j.p12.save(),j.p4.save())
        result=getattr(j.w,fn)(context,*args)
        self.assertEqual(result.code,expected)
        self.assertEqual(j.w.save(),before)
        self.assertEqual((j.p7.save(),j.p11.save(),j.p12.save(),j.p4.save()),owners)
        COUNTS['immutable_failures']+=1
        return result

    def test_restart_each_real_delivery_and_caption_boundary(self):
        for pre in (False,True):
            j=Joined(preengaged=pre,vc03win=pre);j.start();self.roundtrip(j,'start')
            j.w.give_program(j.context(PORCH));self.roundtrip(j,'program')
            self.unchanged(j,'confirm_seating',j.context(),'guest_route_not_yet_clear')
            j.move('milo',COURTYARD,'observed arrival');j.queue_clear=True
            j.w.confirm_seating(j.context());self.roundtrip(j,'seating')
            j.move('frankie',COURTYARD,'observed hatch receiver')
            j.w.deliver_pot(j.context(KITCHEN));self.roundtrip(j,'pot-logical-delivery')
            self.assertEqual(j.h7.owner.owner,'P07')  # Separate source-release boundary.
            c7=replace(j.c7,flags=j.c7.flags|j.p12.flags)
            j.p7.handoff_to_p13(c7,P13Handoff('P13:OWN:hotpot_pot',j.w.pot_at),host=j.h7)
            j.c7=replace(c7,ownership=j.h7.ownership_context())
            j.physical['hotpot_pot']=('P13',COURTYARD)
            self.roundtrip(j,'pot-owner-release')
            self.assertEqual(j.h7.handoffs,1)
            j.w.pull_serve(j.context());self.roundtrip(j,'serve')
            j.move('rita',COURTYARD,'observed consent speaker')
            j.w.ask_rita(j.context());self.roundtrip(j,'consent-queued')
            shown(j.w,j.context(),'rita_ready');self.roundtrip(j,'consent-read')
            self.assertEqual(j.w.deliver_display(j.context(SIDE)).code,'display_delivered')
            for actor in ('felix','vivian'):j.move(actor,COURTYARD,'display transport arrival')
            for obj in ('folded_display','handcart'):j.physical[obj]=('P13',COURTYARD)
            self.roundtrip(j,'display-arrival')
            j.w.open_screen(j.context());self.roundtrip(j,'screen-open')
            j.move('bunny',COURTYARD,'observed reveal participant')
            j.w.begin_presentation(j.context(),'reveal');self.roundtrip(j,'reveal-queued')
            for index,token in enumerate(j.w._tokens('reveal')):
                p=j.w.resume_presentation(j.context(),'reveal')
                self.assertEqual(j.w.acknowledge_presentation(j.context(),p.presentation_id,
                                      speech_unit_ids=(token,)).code,'presentation_acknowledged')
                self.roundtrip(j,'reveal-'+str(index+1))
            j.w.pull_show(j.context());self.roundtrip(j,'show')
            j.board();self.roundtrip(j,'board-arrival')
            j.w.request_contest(j.context());self.roundtrip(j,'contest-request')
            j.w.finish_contest_request(j.w.pending_contest_request_id,False)
            self.roundtrip(j,'contest-cancel')
            self.assertFalse(j.vc.progress['VC04'].resolved)
            j.contest(False,read_result=False);self.roundtrip(j,'unread-loss')
            self.unchanged(j,'pull_toast',j.context(),'contest_active')
            leave(j.vc);self.roundtrip(j,'concluded-loss')
            j.w.call_attention(j.context());self.roundtrip(j,'attention-queued')
            shown(j.w,j.context(),'attention');self.roundtrip(j,'attention-read')
            j.w.pull_toast(j.context());self.roundtrip(j,'toast')
            for cue in ORDER:
                request=next(x for x in j.w.pending_autosaves if x['cue']==cue)
                j.w.acknowledge_autosave(request['request_id']);self.roundtrip(j,'ack-'+cue)
            self.assertTrue(j.w.ready);self.assertFalse(j.w.pending_autosaves)
            self.assertFalse(j.vc.progress['VC04'].won)
            self.assertFalse(j.p9.terms_card_handoff['signed'])

    def test_global_cancel_and_restore_retire_only_runtime_receipts(self):
        j=Joined();j.serve();j.move('rita',COURTYARD,'consent')
        request=j.w.ask_rita(j.context());autosave=j.w.pending_autosaves[0]['request_id']
        before=j.w.save();self.assertEqual(j.w.cancel_presentation(request.presentation_id).code,'presentation_cancelled')
        self.assertEqual(j.w.save(),before)
        self.assertEqual(j.w.acknowledge_autosave(autosave).code,'stale_autosave')
        self.assertEqual(j.w.acknowledge_presentation(j.context(),request.presentation_id,
                         record_id='P13.DIALOGUE.004').code,'stale_presentation')
        shown(j.w,j.context(),'rita_ready');self.assertTrue(j.w.rita_consented)
        current=j.w.pending_autosaves[0]['request_id']
        self.roundtrip(j,'cancellation')
        self.assertEqual(j.w.acknowledge_autosave(current).code,'stale_autosave')
        j.w.acknowledge_autosave(j.w.pending_autosaves[0]['request_id'])
        self.assertFalse(j.w.pending_autosaves)

    def test_each_delivery_actor_departure_and_offscreen_apron_are_reversible(self):
        j=Joined();j.start()
        for context in (j.context(LIVING),j.context(PORCH,on_apron=True)):
            self.unchanged(j,'give_program',context,'offscreen')
        j.move('milo',LIVING,'departure')
        self.unchanged(j,'give_program',j.context(PORCH),'milo_absent')
        j.move('milo',PORCH,'return');j.w.give_program(j.context(PORCH))
        j.move('milo',COURTYARD,'arrival');j.queue_clear=True;j.w.confirm_seating(j.context())
        j.move('frankie',COURTYARD,'receiver');j.move('bunny',LIVING,'departure')
        self.unchanged(j,'deliver_pot',j.context(KITCHEN),'helpers_absent')
        j.move('bunny',KITCHEN,'return');self.assertEqual(j.w.deliver_pot(j.context(KITCHEN)).code,'pot_delivered')
        j.w.pull_serve(j.context());j.move('rita',COURTYARD,'consent');shown(j.w,j.context(),'rita_ready')
        for actor in ('felix','vivian'):
            j.move(actor,LIVING,'departure')
            self.unchanged(j,'deliver_display',j.context(SIDE),'transport_helpers_absent')
            j.move(actor,SIDE,'return')
        j.w.deliver_display(j.context(SIDE));j.move('rita',SIDE,'departure')
        self.unchanged(j,'open_screen',j.context(),'rita_consent_and_presence_required')
        j.move('rita',COURTYARD,'return');j.w.open_screen(j.context())
        j.move('bunny',COURTYARD,'reveal participant');shown(j.w,j.context(),'reveal');j.w.pull_show(j.context())
        j.move('frankie',COURTYARD,'not at board')
        self.unchanged(j,'deliver_board',j.context(LIVING),'board_and_frankie_required')
        j.board();j.move('stringer',LIVING,'departure')
        self.unchanged(j,'request_contest',j.context(),'stringer_absent')
        j.move('stringer',COURTYARD,'return');j.contest();shown(j.w,j.context(),'attention')
        self.assertEqual(j.w.pull_toast(j.context()).code,'toast_complete')

    def test_p07_actual_owner_mismatch_rolls_back_then_retries_unique_release(self):
        j=Joined();j.start();j.w.give_program(j.context(PORCH))
        j.move('milo',COURTYARD,'arrival');j.queue_clear=True;j.w.confirm_seating(j.context())
        j.move('frankie',COURTYARD,'receiver');j.w.deliver_pot(j.context(KITCHEN))
        c7=replace(j.c7,flags=j.c7.flags|j.p12.flags)
        request=P13Handoff('P13:OWN:hotpot_pot',j.w.pot_at)
        prior=j.p7.save();owner=j.h7.owner
        j.h7.owner=OwnedObject('hotpot_pot','P13',COURTYARD)
        bad_host=j.h7.snapshot()
        with self.assertRaises(HostPreparationError):j.p7.handoff_to_p13(c7,request,host=j.h7)
        self.assertEqual(j.p7.save(),prior);self.assertEqual(j.h7.snapshot(),bad_host)
        j.h7.owner=owner
        self.assertEqual(j.p7.handoff_to_p13(c7,request,host=j.h7).code,'pot_handed_off')
        j.c7=replace(c7,ownership=j.h7.ownership_context())
        self.roundtrip(j,'p07-retried-release')
        self.assertEqual(j.p7.handoff_to_p13(j.c7,request,host=j.h7).code,'already_handed_off')
        self.assertEqual(j.h7.handoffs,1)

    def test_reveal_remaining_speaker_receipts_after_departure(self):
        j=Joined();j.serve();j.move('rita',COURTYARD,'consent');shown(j.w,j.context(),'rita_ready')
        j.w.deliver_display(j.context(SIDE));j.w.open_screen(j.context());j.move('bunny',COURTYARD,'reveal')
        p=j.w.begin_presentation(j.context(),'reveal');tokens=j.w._tokens('reveal')
        for index,token in enumerate(tokens):
            speaker=j.w.SPEAKERS[token]
            if speaker in j.actors:
                j.move(speaker,LIVING,'speaker temporarily leaves')
                before=j.w.save()
                self.assertEqual(j.w.acknowledge_presentation(j.context(),p.presentation_id,
                                 speech_unit_ids=(token,)).code,'speaker_absent')
                self.assertEqual(j.w.save(),before)
                j.move(speaker,COURTYARD,'speaker returns')
            j.w.acknowledge_presentation(j.context(),p.presentation_id,speech_unit_ids=(token,))
        self.assertEqual(j.w.pull_show(j.context()).code,'show_complete')

    def test_first_wrong_caption_survives_other_wrong_routes_and_closes_after_reveal(self):
        j=Joined();j.start();j.w.give_program(j.context(PORCH),'kitchen_hatch')
        first=j.w.wrong_source;self.assertEqual(first,'wrong_people')
        j.move('frankie',COURTYARD,'receiver');j.w.deliver_pot(j.context(KITCHEN),'house_doorway')
        self.assertEqual(j.w.wrong_source,first)
        j.move('milo',PORCH,'caption participant');shown(j.w,j.context(PORCH),first)
        self.roundtrip(j,'first-wrong-caption')
        j.w.acknowledge_wrong_visual(j.context(PORCH),j.w.pending_wrong_visual_id)
        self.assertEqual([e.id for e in j.w.claim_laugh(j.context(PORCH)).events],['LAF13'])
        self.assertFalse(j.w.claim_laugh(j.context(PORCH)).events)
        j.finish();self.roundtrip(j,'late-wrong-repeat')
        self.assertFalse(j.w.claim_laugh(j.context()).events)
        self.assertEqual(j.h7.handoffs,1)

    def test_pending_contest_cancel_restore_reissue_never_grants_outcomes(self):
        j=Joined();j.board();owner=j.vc.save()
        j.w.request_contest(j.context());old=j.w.pending_contest_request_id
        before=j.w.save();j.w=P13World.load(before,context=j.context())
        self.assertEqual(j.w.finish_contest_request(old,True).code,'stale_contest_request')
        self.assertEqual(j.w.save(),before)
        self.assertEqual(j.w.finish_contest_request(j.w.pending_contest_request_id,False).code,'contest_request_cancelled')
        self.assertEqual(j.vc.save(),owner);self.assertFalse(j.vc.progress['VC04'].resolved)
        j.w.request_contest(j.context());j.w.finish_contest_request(j.w.pending_contest_request_id,True)
        self.assertEqual(j.vc.save(),owner)
        self.unchanged(j,'pull_toast',j.context(),'vc04_resolution_required')
        prepared('VC04',j.vc);play(j.vc,[False]*3,'VC04');leave(j.vc)
        shown(j.w,j.context(),'attention');j.w.pull_toast(j.context())
        self.assertFalse(j.vc.progress['VC04'].won)

    def test_current_gate_and_pa_changes_dont_rewrite_earned_history(self):
        j=Joined();j.serve();j.move('rita',COURTYARD,'consent');shown(j.w,j.context(),'rita_ready')
        gate_before=j.p4.save();j.p4.set_peg(0);j.p4.close_gate(1)
        self.unchanged(j,'deliver_display',j.context(SIDE),'tested_peg_required')
        j.p4.open_gate();j.p4.set_peg(1)
        self.assertEqual(j.p4.tested,True);self.assertNotEqual(j.p4.save(),gate_before)
        j.w.deliver_display(j.context(SIDE));j.w.open_screen(j.context())
        j.move('bunny',COURTYARD,'observed reveal participant');shown(j.w,j.context(),'reveal')
        j.w.pull_show(j.context());j.board();j.contest();shown(j.w,j.context(),'attention')
        before=j.w.save();j.p8.orient_pa(j.c8,Facing.NEIGHBOR)
        self.unchanged(j,'pull_toast',j.context(),'working_microphone_required')
        self.assertEqual(j.w.save(),before)
        j.p8.orient_pa(j.c8,Facing.INWARD);j.w.pull_toast(j.context())
        self.assertTrue(j.w.ready)

    def test_repeated_successful_actions_keep_all_owner_and_delivery_serials(self):
        j=Joined();j.finish();initial=j.w.save();upstream=(j.p7.save(),j.p11.save(),j.p12.save(),j.p4.save())
        operations=[('give_program',PORCH,'program_already_given'),('confirm_seating',COURTYARD,'already_seated'),
                    ('deliver_pot',KITCHEN,'pot_already_delivered'),('pull_serve',COURTYARD,'serve_already_complete'),
                    ('deliver_display',SIDE,'display_already_delivered'),('open_screen',COURTYARD,'viewing_side_already_open'),
                    ('pull_show',COURTYARD,'show_already_complete'),('deliver_board',LIVING,'board_already_delivered'),
                    ('pull_toast',COURTYARD,'toast_already_complete')]
        for fn,room,code in operations:
            for repeat in range(2):self.unchanged(j,fn,j.context(room),code)
        self.assertEqual(j.w.save(),initial)
        self.assertEqual((j.p7.save(),j.p11.save(),j.p12.save(),j.p4.save()),upstream)

    def test_won_rematch_survives_loss_then_owner_restore_respects_timeline(self):
        j=Joined();j.finish();loss_save=j.vc.save();p13=j.w.save()
        j.contest(True);win_save=j.vc.save();self.assertTrue(j.vc.progress['VC04'].won)
        j.contest(False);self.assertTrue(j.vc.progress['VC04'].won)
        j.vc.restore(loss_save,owner_generation=j.vc.owner_generation+1)
        self.assertFalse(j.vc.progress['VC04'].won);self.assertTrue(j.vc.progress['VC04'].resolved)
        j.w.validate_context(j.context())
        for key,value in p13['state'].items():
            if key!='revision':self.assertEqual(j.w.save()['state'][key],value)
        j.vc.restore(win_save,owner_generation=j.vc.owner_generation+1)
        self.assertTrue(j.vc.progress['VC04'].won)
        self.assertEqual(j.w.flags,{'SERVED','DISPLAY_REVEALED','TOAST_READY'})
        self.assertFalse(j.p9.terms_card_handoff['signed'])

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Independent)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    output=dict(tests=result.testsRun,passed=result.wasSuccessful(),optimized=bool(sys.flags.optimize),
                counts=COUNTS,scope='Independent finite reference tests; no native proof')
    (ROOT/('independent-optimized.json' if sys.flags.optimize else 'independent-normal.json')).write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output))
    raise SystemExit(not result.wasSuccessful())
