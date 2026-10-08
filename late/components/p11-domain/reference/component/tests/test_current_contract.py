"""New tests for current canon and the explicitly new numeric-owner bridge."""
import copy
from dataclasses import replace
import itertools
import json
from pathlib import Path
import unittest

from cakood.p04_model import project_gate
from cakood.p11_model import P11World, P11Context, RescuePhase, RECORD_UNITS, FIXED_OBJECTS
from cakood.p03_model import TILE_IDS, TILE_NATIVE_IDS, TILE_GROUP_NATIVE_ID
from dependencies.p04_numeric_model import P04, Obj, Bunting, Code
from dependencies.p03_numeric_model import P03
from test_p11_model import C, GATE, SIDE_PASSAGE, PORCH, COURTYARD, CONSERVATORY, read, rescue, clone

ROOT = Path(__file__).resolve().parents[1]


def repaired_gate():
    owner = P04()
    owner.context(3, 0, 1, 1)
    owner.topic(Obj.FELIX, 1)
    owner.open_gate()
    owner.place_wedge()
    owner.context(3, 0, 1, 0)
    owner.move_bunting(Bunting.HELD)
    owner.move_bunting(Bunting.HOOK)
    owner.recover_wedge()
    owner.context(3, 0, 1, 1)
    owner.close_gate(1)
    owner.open_gate()
    if not owner.validate() or not owner.tested:
        raise RuntimeError('Numeric P04 preparation did not complete')
    return owner


def select_variant(record, world):
    """Evaluate only the catalog's two explicit operators in fixture tests."""
    for variant in record['finite_variants']:
        predicates = variant['when']['all']
        if all((getattr(world, p['field']) > p['value']) if p['op'] == 'gt'
               else (getattr(world, p['field']) == p['value']) for p in predicates):
            return variant['variant_id']
    return None


class CurrentCanonTests(unittest.TestCase):
    def test_variants_and_speech_match_current_catalog_predicates(self):
        fixture = json.loads((ROOT/'tests/fixtures/p11/canonical-bindings.json').read_text())
        for engaged in (False, True):
            w, c = rescue(context=replace(C, gate=replace(GATE, peg_engaged=engaged)))
            variant = 'pre_engaged' if engaged else 'ordinary'
            self.assertEqual(w.rescue_credit_variant, variant)
            for record in ('VC03.WIN', 'VC03.LOSS'):
                source = fixture['vc03_records'][record]
                self.assertEqual(select_variant(source, w), variant)
                self.assertEqual(source['variant_binding']['priority'], ['ordinary', 'pre_engaged'])
                unit = next(u for u in fixture['vc03_speech_units'] if u['line_id'] == record+'.02')
                self.assertEqual(select_variant(unit, w), variant)
                chosen = next(v for v in source['finite_variants'] if v['variant_id'] == variant)
                spoken = next(v for v in unit['finite_variants'] if v['variant_id'] == variant)
                self.assertEqual(chosen['text'][1]['text'], spoken['text'])
            read(w, c, 'sincere')
            event = w.request_contest(c).events[0]
            self.assertEqual(event.payload['rescue_credit_variant'], variant)
            self.assertEqual(event.payload['peg_ack_at'], w.peg_ack_at)
            self.assertEqual(event.payload['advance_peg_at'], w.advance_peg_at)
            self.assertEqual(clone(w, c).rescue_credit_variant, variant)

    def test_preengaged_does_not_require_or_invent_a_new_peg_action(self):
        owner = repaired_gate(); owner.set_peg(1); snapshot = owner.save()
        c = replace(C, gate=project_gate(owner))
        w = P11World(); w.lift(c); w.release_catch(c); w.pull_handle(c); w.stage_display(c)
        self.assertTrue(w.ready)
        self.assertEqual(w.peg_ack_at, 0)
        self.assertEqual(w.advance_peg_at, w.lift_at)
        self.assertEqual(w.rescue_credit_variant, 'pre_engaged')
        self.assertEqual(owner.save(), snapshot)

    def test_unacknowledged_external_peg_cannot_fabricate_rescue_credit(self):
        w = P11World(); w.lift(C); w.release_catch(C)
        c = replace(C, gate=replace(GATE, peg_engaged=True))
        before = w.save()
        r = w.pull_handle(c)
        self.assertEqual(r.code, 'peg_history_required')
        self.assertEqual((r.text, r.line_ids, r.events), ('', (), ()))
        self.assertEqual(w.save(), before)
        # Always-safe recovery needs no disengage/re-engage, audio or dialogue.
        w.set_back(c); w.lift(c); w.release_catch(c); w.pull_handle(c); w.stage_display(c)
        self.assertEqual(w.rescue_credit_variant, 'pre_engaged')

    def test_pending_real_peg_receipt_can_reconcile_before_pull(self):
        w=P11World(); w.lift(C); w.request_peg(C); token=w.pending_peg_request_id
        c=replace(C, gate=replace(GATE, peg_engaged=True)); w.release_catch(c)
        self.assertEqual(w.pull_handle(c).code, 'peg_history_required')
        w.acknowledge_peg(c, token)
        self.assertEqual(w.pull_handle(c).code, 'display_folded_safe')
        w.stage_display(c)
        self.assertEqual(w.rescue_credit_variant, 'ordinary')

    def test_current_save_rejects_missing_or_late_peg_history(self):
        w,c=rescue(); original=w.save()
        for changes in ({'peg_ack_at':0,'advance_peg_at':0},
                        {'peg_ack_at':w.fold_at}, {'peg_ack_at':w.stage_at}):
            data=copy.deepcopy(original); data['state'].update(changes)
            with self.assertRaises(ValueError):P11World.load(data, context=c)
        self.assertEqual(w.save(),original)

    def test_bunny_presence_is_required_for_existing_sincere_scene_only(self):
        c=replace(C, gate=replace(GATE, peg_engaged=True), bunny_room=CONSERVATORY)
        w=P11World(); w.lift(c); w.release_catch(c); w.pull_handle(c); w.stage_display(c)
        self.assertTrue(w.ready); before=w.save()
        self.assertEqual(w.begin_presentation(c,'sincere').code,'bunny_at_porch_required')
        self.assertEqual(w.save(),before)
        at_porch=replace(c,bunny_room=PORCH); p=w.begin_presentation(at_porch,'sincere')
        before=w.save()
        self.assertEqual(w.acknowledge_presentation(c,p.presentation_id,
            record_id='P11.DIALOGUE.002').code,'bunny_at_porch_required')
        self.assertEqual(w.save(),before)
        w.acknowledge_presentation(at_porch,p.presentation_id,record_id='P11.DIALOGUE.002')
        self.assertTrue(w.contest_eligible)
        self.assertEqual(c.bunny_room,CONSERVATORY)

    def test_ordinary_has_catalog_priority_if_both_historical_serials_exist(self):
        c=replace(C,gate=replace(GATE,peg_engaged=True))
        w=P11World();w.lift(c)
        released=replace(c,gate=replace(c.gate,peg_engaged=False))
        w.request_peg(released);w.acknowledge_peg(c,w.pending_peg_request_id)
        w.release_catch(c);w.pull_handle(c);w.stage_display(c)
        self.assertGreater(w.advance_peg_at,0);self.assertGreater(w.peg_ack_at,0)
        self.assertEqual(w.rescue_credit_variant,'ordinary')

    def test_rematch_preserves_exact_rescue_facts_and_independent_resolution(self):
        for engaged in (False,True):
            w,c=rescue(context=replace(C,gate=replace(GATE,peg_engaged=engaged)))
            read(w,c,'sincere'); rescue_state=(w.phase,w.peg_ack_at,w.advance_peg_at,w.flags)
            for outcome in (frozenset(),frozenset({'VC03_RESOLVED'}),frozenset({'VC03_RESOLVED','VC03_WON'})):
                current=replace(c,flags=c.flags|outcome)
                request=w.request_contest(current)
                self.assertEqual(request.line_ids,('VC03.REMATCH',) if outcome else ('VC03.ENTRY',))
                w.acknowledge_contest_request(current,w.pending_contest_request_id)
                self.assertEqual((w.phase,w.peg_ack_at,w.advance_peg_at,w.flags),rescue_state)
                self.assertFalse(w.flags & {'VC03_WON','VC03_RESOLVED','INTRODUCTION_CLEAR','GAME_COMPLETE'})

    def test_original_objects_remain_reserved_covered_and_unrevealed(self):
        w,c=rescue();handoff=w.display_handoff
        self.assertEqual(w.reserved_external_objects,{'folded_display','handcart'})
        self.assertEqual(w.inventory,())
        self.assertEqual((handoff['display_id'],handoff['cart_id']),('folded_display','handcart'))
        self.assertTrue(handoff['padded'] and handoff['covered'] and handoff['undamaged'])
        self.assertFalse(handoff['panel_revealed'] or handoff['rita_reveal_consent'])
        for obj in FIXED_OBJECTS:
            with self.assertRaises(ValueError):replace(c,inventory=frozenset({obj}))


class OwnerCompositionTests(unittest.TestCase):
    def test_numeric_p04_request_then_owner_commit_in_both_helper_orders(self):
        for order in itertools.permutations(('peg','catch')):
            owner=repaired_gate();c=replace(C,gate=project_gate(owner));w=P11World();w.lift(c)
            for action in order:
                if action=='catch':w.release_catch(c)
                else:
                    before=owner.save();w.request_peg(c);token=w.pending_peg_request_id
                    self.assertEqual(owner.save(),before)
                    self.assertEqual(w.acknowledge_peg(c,token).code,'peg_not_yet_engaged')
                    self.assertEqual(owner.set_peg(1),Code.PEG_ENGAGED)
                    c=replace(c,gate=project_gate(owner));w.acknowledge_peg(c,token)
            w.pull_handle(c);w.stage_display(c)
            self.assertTrue(w.ready);self.assertEqual(w.rescue_credit_variant,'ordinary')
            self.assertEqual(c.bunny_room,PORCH);self.assertEqual(c.frankie_room,COURTYARD)

    def test_owner_projection_is_readonly_validated_and_strict(self):
        owner=P04(); before=copy.deepcopy(owner.state); handoff=project_gate(owner)
        self.assertFalse(handoff.tested or handoff.peg_available or handoff.peg_engaged)
        self.assertEqual(owner.state,before)
        self.assertEqual(P11World().lift(replace(C,gate=handoff)).code,'tested_gate_required')
        with self.assertRaises(ValueError):project_gate(object())
        owner.state.peg=True
        with self.assertRaises(ValueError):project_gate(owner)
        for gate in (replace(GATE,peg_engaged=True,wedge_in_gate=True),
                     replace(GATE,wedge_in_gate=True,gate_open=False)):
            with self.assertRaises(ValueError):replace(C,gate=gate)

    def test_numeric_gate_release_is_observed_at_final_pull(self):
        owner=repaired_gate();owner.set_peg(1);c=replace(C,gate=project_gate(owner))
        w=P11World();w.lift(c);w.release_catch(c)
        owner.set_peg(0);released=replace(c,gate=project_gate(owner));before=w.save()
        self.assertEqual(w.pull_handle(released).code,'peg_required')
        self.assertEqual(w.save(),before);w.set_back(released)
        self.assertFalse(owner.state.peg)

    def test_p03_original_grant_then_p09_p10_join_without_any_contest_win(self):
        from cakood.p09_model import P09Context,P09World
        from cakood.p10_model import P10Context,P10World,ORDER,LIVING
        for order in itertools.permutations(('P09','P10')):
            p3=P03();p3.context(6,0,1,1);p3.look(37);p3.begin_credit();p3.select(1)
            p3.context(2,0,1,1);p3.collect(38);p3.context(6,0,1,1);p3.pad(38);p3.give_slate()
            self.assertTrue(p3.validate());self.assertEqual(p3.inventory(),[TILE_GROUP_NATIVE_ID])
            self.assertEqual([p3.location(i) for i in TILE_NATIVE_IDS],[10,10,10])
            flags=frozenset({'EVENING_STARTED','PLAN_AGREED'})
            p9=P09World();p10=P10World()
            for branch in order:
                if branch=='P09':
                    context=P09Context(CONSERVATORY,flags=flags)
                    for source,record in [('direct_question','P09.DIALOGUE.001'),('terms','P09.DIALOGUE.002')]:
                        presentation=p9.begin_presentation(context,source)
                        p9.acknowledge_presentation(context,presentation.presentation_id,record_id=record)
                    flags=flags|p9.flags
                else:
                    pocket=set((*TILE_IDS,'grease_pencil'));context=P10Context(LIVING,flags=flags,inventory=frozenset(pocket))
                    p10.introduce(context);presentation=p10.begin_presentation(context,'plan')
                    p10.acknowledge_presentation(context,presentation.presentation_id,record_id='P10.READ.001')
                    for cue,word in zip(TILE_IDS,ORDER):p10.write(context,cue,word)
                    for slot,cue in enumerate(TILE_IDS):
                        p10.place(replace(context,room=COURTYARD,inventory=frozenset(pocket)),cue,slot);pocket.remove(cue)
                    p10.validate_context(replace(context,room=COURTYARD,inventory=frozenset(pocket)))
                    flags=flags|p10.flags
                if branch==order[0]:
                    self.assertEqual(P11World().lift(replace(C,flags=flags)).code,'p09_and_p10_required')
            self.assertFalse(p9.terms_card_handoff['signed'])
            owner=repaired_gate();owner.set_peg(1)
            w,c=rescue(context=replace(C,flags=flags,gate=project_gate(owner)))
            read(w,c,'sincere');self.assertTrue(w.contest_eligible)
            self.assertFalse(any('VC' in flag for flag in flags))

    def test_numeric_and_symbolic_identity_bridge_is_pinned_to_current_abi(self):
        abi=json.loads((ROOT/'dependencies/p04-abi.json').read_text())['objects']
        schema=json.loads((ROOT/'dependencies/p09-schema.json').read_text())['objects']
        self.assertEqual(tuple(abi[x] for x in TILE_IDS),TILE_NATIVE_IDS)
        self.assertEqual(tuple(schema[x] for x in TILE_IDS),TILE_NATIVE_IDS)
        self.assertEqual(abi['hold_open_peg'],int(Obj.HOLD_OPEN_PEG))
        self.assertEqual(abi['folded_display'],42)

if __name__=='__main__':unittest.main()
