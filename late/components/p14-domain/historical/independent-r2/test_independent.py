"""Independent ordinary P14 owner/save/consent/replay checks, source-only.

Run with --component pointing to the unmodified extracted candidate component.
Expected ordinary behavior is asserted; the cross-branch regression fails on v1.
"""
from pathlib import Path
import argparse, copy, hashlib, json, sys, unittest
from dataclasses import replace

parser = argparse.ArgumentParser()
parser.add_argument('--component', type=Path, required=True)
parser.add_argument('--results', type=Path, required=True)
args, rest = parser.parse_known_args()
C = args.component.resolve()
D = C / 'stock-sci/p14-domain-adapter'
sys.path[:0] = [str(C), str(C/'tests'), str(D), str(D/'tests')]
from cakood.verbal_contest import VerbalContests, Phase, YIELD_EXCHANGE
from test_verbal_contest import prepared, play, leave, read_all
from test_late_campaign_models import c14, UNSIGNED, read, finish14
from finale_join import FinaleJoined
from cakood.p14_model import (P14World, CreditReplay, CONTEST_IDS, PEOPLE,
    TERMS, PENCIL, CARD_IDS, COURTYARD, LIVING, CREDIT_ORDER, ASSET_CREDITS)
from codec import NativeCreditReplay, encode_world, project_context, M
import source_vm

def finish_attempt(owner, encounter, won):
    prepared(encounter, owner)
    play(owner, [won]*3, encounter)
    leave(owner)

def forked_histories():
    seed = prepared('VC01').save_with_evidence()
    branches = []
    for generation, outcomes in ((2, (True,False,False)), (3, (False,True,False))):
        owner = VerbalContests.load_with_evidence(copy.deepcopy(seed), owner_generation=generation)
        for won in outcomes:
            play(owner, [won]*3, 'VC01')
            leave(owner)
        for encounter in CONTEST_IDS[1:]:
            finish_attempt(owner, encounter, True)
        branches.append(owner)
    return branches

class IndependentChecks(unittest.TestCase):
    def test_failed_owner_persistence_does_not_observe_or_change_result(self):
        owner = prepared('VC01')
        owner.enter('VC01', 0, admitted=True)
        token = owner.yield_contest(owner.active.id)
        before = owner.snapshot()
        observations = copy.deepcopy(owner.__dict__.get('_observed_results', []))
        def rejected_save(_):
            raise OSError('injected ordinary storage failure')
        owner._persist = rejected_save
        with self.assertRaises(OSError):
            owner.commit_ko(token)
        self.assertEqual(owner.snapshot(), before)
        self.assertEqual(owner.__dict__.get('_observed_results', []), observations)
        self.assertEqual(owner.attempts, ())
        owner._persist = None
        owner.commit_ko(token)
        observed = copy.deepcopy(owner._observed_results)
        self.assertEqual(len(observed), 1)
        self.assertEqual(observed[0], owner.snapshot())
        with self.assertRaises(ValueError):
            owner.commit_ko(token)
        leave(owner)
        self.assertEqual(owner._observed_results, observed)
        self.assertEqual(owner.attempts[0].outcome.winner, 'opponent')

    def test_restore_pending_result_keeps_identity_and_rejects_old_callback(self):
        owner = prepared('VC01')
        play(owner, [True]*3, 'VC01')
        old = owner.pending_text().receipt
        packet = owner.save_with_evidence()
        restored = VerbalContests.load_with_evidence(json.loads(json.dumps(packet)), owner_generation=2)
        self.assertEqual(restored.attempts, owner.attempts)
        before = restored.save_with_evidence()
        with self.assertRaises(ValueError):
            restored.acknowledge_text(old)
        self.assertEqual(restored.save_with_evidence(), before)
        self.assertIsNotNone(restored.active)
        leave(restored)
        self.assertIsNone(restored.active)
        self.assertEqual(restored.attempts, owner.attempts)
        self.assertEqual(restored.snapshot()['knowledge'], owner.snapshot()['knowledge'])

    def test_aggregate_only_repeated_admission_preserves_world_and_won_flags(self):
        owner, _ = forked_histories()
        unpaired = VerbalContests.load(owner.save(), owner_generation=4)
        world = P14World()
        before = copy.deepcopy(world.__dict__)
        flags = unpaired.flags
        for _ in range(4):
            with self.assertRaises(ValueError):
                world.start(c14(unpaired), UNSIGNED)
            self.assertEqual(world.__dict__, before)
            self.assertEqual(unpaired.flags, flags)
            self.assertEqual(P14World.notebook_gate(c14(unpaired))['won_count'], 4)
        world.validate()

    def test_missing_stale_duplicate_reordered_ledger_rejected(self):
        owner, _ = forked_histories()
        packet = owner.save_with_evidence()
        alternatives = []
        for label in ('missing', 'duplicate', 'reversed', 'stale'):
            changed = copy.deepcopy(packet)
            if label == 'missing': changed['observations'].pop(0)
            if label == 'duplicate': changed['observations'].insert(1, copy.deepcopy(changed['observations'][0]))
            if label == 'reversed': changed['observations'].reverse()
            if label == 'stale': changed['observations'].pop()
            alternatives.append((label, changed))
        before = owner.save_with_evidence()
        for label, changed in alternatives:
            with self.subTest(label=label), self.assertRaises(ValueError):
                VerbalContests.load_with_evidence(changed, owner_generation=7)
        self.assertEqual(owner.save_with_evidence(), before)

    def test_actual_toast_and_every_signature_actor_are_current_barriers(self):
        route = FinaleJoined()
        route.win_all()
        world = route.w
        context = route.context()
        before = world.save()
        self.assertEqual(world.start(replace(context, flags=context.flags-{'TOAST_READY'}), UNSIGNED).code, 'canonical_tasks_incomplete')
        self.assertEqual(world.save(), before)
        route.approvals()
        for person in ('stringer', 'frankie'):
            absent = replace(route.context(), npc_locations=tuple((p, LIVING if p==person else room) for p,room in route.context().npc_locations))
            before = world.save()
            self.assertEqual(world.request_signature(absent).code, 'speaker_absent')
            self.assertEqual(world.save(), before)
        self.assertFalse(world.signature_at)

    def test_approval_identity_card_uniqueness_and_repeated_pin(self):
        route = FinaleJoined()
        route.win_all()
        route.start()
        for person in reversed(PEOPLE):
            before = route.w.save()
            wrong = PEOPLE[(PEOPLE.index(person)+1)%len(PEOPLE)]
            self.assertEqual(route.w.give_card(route.context(), person, wrong).code, 'unrelated_promise_returned')
            self.assertEqual(route.w.save(), before)
            self.assertEqual(route.w.pin_card(route.context(), person).code, 'approval_required')
            with self.assertRaises(ValueError):
                replace(route.context(), inventory=frozenset({*route.inventory,CARD_IDS[person]}))
            route.show('approve:'+person)
            route.w.pin_card(route.context(), person)
            after = route.w.save()
            self.assertEqual(route.w.pin_card(route.context(), person).code, 'card_already_pinned')
            self.assertEqual(route.w.save(), after)
            self.assertNotIn(CARD_IDS[person], route.w.inventory)
        self.assertEqual(set(route.w.approved),set(PEOPLE))
        self.assertEqual(route.w.inventory,())

    def test_signature_requires_explicit_action_and_original_pencil_readback(self):
        route = FinaleJoined()
        route.win_all()
        route.approvals()
        route.show('signature')
        self.assertFalse(route.w.signature_at)
        before = route.w.save()
        self.assertEqual(route.w.give_pencil(route.context()).code,'signed_terms_required')
        self.assertEqual(route.w.save(),before)
        route.event(route.w.pin_signature(route.context()))
        self.assertFalse(route.w.ready)
        before = route.w.save()
        self.assertEqual(route.w.give_pencil(replace(route.context(),inventory=frozenset())).code,'original_pencil_required')
        self.assertEqual(route.w.save(),before)
        route.event(route.w.give_pencil(route.context()))
        for source, code in [('readback','date_text_required'),('return_pencil','complete_readback_required')]:
            before=route.w.save()
            self.assertEqual(route.w.begin_presentation(route.context(),source).code,code)
            self.assertEqual(route.w.save(),before)
        route.show('date')
        before=route.w.save()
        self.assertEqual(route.w.complete_commitments(route.context()).code,'complete_dated_readback_and_return_required')
        self.assertEqual(route.w.save(),before)
        for source in ('readback','return_pencil'):route.show(source)
        route.event(route.w.complete_commitments(route.context()))
        saved=route.w.save()
        self.assertEqual(route.w.complete_commitments(route.context()).code,'commitments_already_complete')
        self.assertEqual(route.w.save(),saved)
        self.assertEqual(route.inventory,{PENCIL})
        self.assertTrue(route.w.ready)
        self.assertEqual([e[0] for e in route.events],['P14_TERMS_SIGNED','P14_PENCIL_HANDOFF','P14_GAME_COMPLETE'])

    def test_all_tones_and_single_asset_selection_survive_full_finale(self):
        for tone in ('professional','friendly','cautiously_romantic'):
            with self.subTest(tone=tone):
                world, context = finish14(c=c14())
                # Tone is an explicit accepted upstream input at entry.
                world, context = finish14(c=replace(c14(),vivian_tone=tone))
                aid,url = list(ASSET_CREDITS.items())[7]
                world.start_finale((url,url))
                self.assertEqual(world.credit_ids,[*CREDIT_ORDER,aid])
                for source in ('closing:'+tone,'meal','tag'):
                    if source=='tag': context=replace(context,room=LIVING,npc_locations=tuple((p,LIVING) for p in PEOPLE[1:]))
                    self.assertEqual(world.current_finale_source,source)
                    before=world.save()
                    self.assertEqual(world.advance_finale().code,'whole_finale_record_required')
                    self.assertEqual(world.save(),before)
                    if source=='meal':self.assertEqual(world.claim_tag_laugh().code,'tag_laugh_unavailable')
                    read(world,context,source)
                    world.advance_finale()
                old=world.pending_freeze_id
                world=P14World.load(world.save())
                self.assertEqual(world.acknowledge_freeze(old).code,'stale_freeze')
                self.assertEqual(world.claim_celebration().code,'celebration_unavailable')
                world.acknowledge_freeze(world.pending_freeze_id)
                self.assertEqual(world.claim_celebration().code,'celebration_consumed')
                world.advance_finale()
                for rid in world.credit_ids:
                    read(world,context,'credit:'+rid)
                    world.advance_finale()
                self.assertEqual(world.finale_phase,'finished')
                self.assertTrue(world.ready)

    def test_parallel_replay_viewers_partial_progress_restore_and_defensive_return(self):
        route=FinaleJoined();route.finish();route.w.start_finale();route.w.skip_finale()
        before=copy.deepcopy((route.w.save(),route.j.vc.save_with_evidence()))
        session={'world':before[0],'contests':before[1],'open_task':{'done':False}}
        first=route.w.create_credit_replay(session)
        second=route.w.create_credit_replay(session)
        untouched=second.save()
        read(first.world,route.context(),'credit:'+first.world.credit_ids[0]);first.world.advance_finale();first.world.pause_finale(True)
        first=CreditReplay.load(json.loads(json.dumps(first.save())))
        self.assertEqual(first.world.credit_cursor,1);self.assertTrue(first.world.finale_paused)
        returned=first.return_session(cancel=True);returned['open_task']['done']=True
        self.assertEqual(first.return_session(),session)
        self.assertEqual(second.save(),untouched)
        self.assertEqual((route.w.save(),route.j.vc.save_with_evidence()),before)

    def test_cross_branch_observations_must_not_substitute_first_win(self):
        one,two=forked_histories()
        a,b=one.save_with_evidence(),two.save_with_evidence()
        self.assertEqual(a['owner']['payload']['state']['history'],b['owner']['payload']['state']['history'])
        self.assertEqual(one.snapshot()['knowledge'],two.snapshot()['knowledge'])
        self.assertNotEqual(a['owner'],b['owner'])
        first=lambda v:next(row.outcome.id for row in v.attempts if row.encounter_id=='VC01' and row.outcome.winner=='jack')
        self.assertEqual(first(one),'VC01:A1:KO');self.assertEqual(first(two),'VC01:A2:KO')
        mixed=copy.deepcopy(a);mixed['observations']=copy.deepcopy(b['observations'])
        # Each input is a valid ordinary save. Pairing these independent parts
        # models the stale/wrong-branch sidecar the new boundary must reject.
        with self.assertRaises(ValueError):
            VerbalContests.load_with_evidence(mixed,owner_generation=4)

class JsonResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs);self.rows=[]
    def addSuccess(self,test):
        super().addSuccess(test);self.rows.append({'test':test.id(),'status':'PASS'})
    def addFailure(self,test,err):
        super().addFailure(test,err);self.rows.append({'test':test.id(),'status':'FAIL','detail':self._exc_info_to_string(err,test)})
    def addError(self,test,err):
        super().addError(test,err);self.rows.append({'test':test.id(),'status':'ERROR','detail':self._exc_info_to_string(err,test)})

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(IndependentChecks)
    result=unittest.TextTestRunner(verbosity=2,resultclass=JsonResult).run(suite)
    args.results.write_text(json.dumps({'optimized':bool(sys.flags.optimize),'tests':result.testsRun,'rows':result.rows},indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
