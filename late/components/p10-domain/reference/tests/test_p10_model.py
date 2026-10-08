"""New Python reference tests from retained adapter obligations, not recovered test bytes."""
from dataclasses import dataclass, replace
from pathlib import Path
import copy
import hashlib
import importlib.util
import itertools
import json
import random
import unittest
from cakood.p10_model import *
from cakood.p10_model import _Captioned, _Receipt
from cakood.p03_model import TILE_NATIVE_IDS, TILE_GROUP_NATIVE_ID
from cakood.model import Verb
ROOT = Path(__file__).resolve().parents[1]
C = P10Context(LIVING, flags=frozenset({'EVENING_STARTED'}),
    inventory=frozenset((*TILE_IDS, 'grease_pencil', 'master_invitation')))
RACK = replace(C, room=COURTYARD, bunny_room=COURTYARD, frankie_room=COURTYARD)
KNOWN = replace(C, flags=C.flags | {'KNOW_CUE_ORDER'})

def show(w, source, c=C):
    r = w.begin_presentation(c, source)
    return w.acknowledge_presentation(c, r.presentation_id, record_id=w.SOURCES[source])

def prepare(paper=False):
    w = P10World(); w.introduce(C); show(w, 'plan')
    if paper: w.prepare_paper(C)
    ids = PAPER_IDS if paper else TILE_IDS
    for cue, word in zip(ids, ORDER): w.write(C, cue, word)
    return w, ids

def install(w, ids):
    return [w.place(RACK, cue, i) for i, cue in enumerate(ids)]

def clone(w):
    return P10World.load(json.loads(json.dumps(w.save())))

class MilestoneTests(unittest.TestCase):
    def test_recovered_prefix_is_byte_exact(self):
        prefix = (ROOT/'inputs/literal-p10/partial/cakood-p10_model.py.txt').read_bytes()
        model = (ROOT/'cakood/p10_model.py').read_bytes()
        self.assertTrue(model.startswith(prefix))
        self.assertEqual(hashlib.sha256(prefix).hexdigest(), '8bef9f572284ea03eea25c51738952545eb6c5d31e7173a0df82e77228edca63')
        self.assertEqual(UNIT_SPEAKERS['P10.FAILURE.003.01'], 'frankie')

    def test_complete_ceramic_and_paper_routes_save_after_each_placement(self):
        for paper, order in itertools.product((False, True), itertools.permutations(range(3))):
            with self.subTest(paper=paper, order=order):
                w, ids = prepare(paper)
                events = []
                for i in order:
                    events.extend(w.place(RACK, ids[i], i).events); w = clone(w)
                self.assertTrue(w.ready); self.assertTrue(w.rack_correct)
                self.assertEqual(w.flags, {'CUES_RESTORED'})
                self.assertEqual(w.cue_handoff['words'], ORDER)
                self.assertEqual(sum(e.payload.get('restored_first_time', False) for e in events), 1)

    def test_queue_look_hint_do_not_teach_and_restore_invalidates_handle(self):
        w = P10World(); w.introduce(C); w.look(C, 'board'); w.hint(C, 3)
        r = w.begin_presentation(C, 'plan')
        self.assertFalse(w.knows_order(C)); self.assertEqual(w.choices(C), ())
        self.assertEqual(w.write(C, TILE_IDS[0], 'SERVE').code, 'read_plan_required')
        saved = clone(w)
        self.assertEqual(saved.acknowledge_presentation(C, r.presentation_id, record_id='P10.READ.001').code, 'stale_presentation')
        r = saved.resume_presentation(C, 'plan')
        saved.acknowledge_presentation(C, r.presentation_id, record_id='P10.READ.001')
        self.assertTrue(saved.knows_order(C)); self.assertEqual(saved.choices(C), tuple(CHOICE_IDS.values()))

    def test_original_grant_identity_and_nonconsuming_paper(self):
        abi = json.loads((ROOT/'dependencies/p04-abi.json').read_text())['objects']
        self.assertEqual(tuple(abi[x] for x in TILE_IDS), TILE_NATIVE_IDS)
        self.assertEqual(TILE_NATIVE_IDS, (48, 49, 50)); self.assertEqual(TILE_GROUP_NATIVE_ID, 35)
        w = P10World(); before = C.inventory
        self.assertEqual(w.pick_up_tiles(C).code, 'existing_tiles'); self.assertEqual(w.inventory, ())
        self.assertFalse(w.pick_up_tiles(C).events)
        r = w.prepare_paper(C); again = w.prepare_paper(C)
        self.assertEqual(r.events[0].payload['items'], PAPER_IDS)
        self.assertTrue(r.events[0].payload['original_preserved']); self.assertFalse(again.events)
        self.assertEqual(C.inventory, before); self.assertIn('master_invitation', C.inventory)
        self.assertEqual(w.inventory, PAPER_IDS)

    def test_reversible_labels_slots_and_latched_history(self):
        w, ids = prepare(); install(w, ids); first = w.restored_at
        w.write(RACK, ids[0], None); self.assertFalse(w.rack_correct); self.assertTrue(w.ready)
        self.assertEqual(w.cue_handoff['words'], (None, 'SHOW', 'TOAST'))
        w.write(RACK, ids[0], 'SERVE'); w.remove(RACK, 0)
        self.assertEqual(w.reserved_external_items, set(ids[1:]))
        w.place(RACK, ids[0], 0); self.assertEqual(w.restored_at, first)
        self.assertTrue(clone(w).rack_correct)

    def test_bread_only_event_and_single_source_start(self):
        w = P10World(); r = w.introduce(C); again = w.introduce(C)
        self.assertEqual([e.id for e in r.events], ['P10_BREAD_SERVED', 'P10_PRESENTATION_QUEUED'])
        self.assertEqual(r.events[0].payload, dict(serial=1, puzzle='P10', edible_only=True,
            tray_id='tray', consumed='bread_samples', plan_preserved=True))
        self.assertFalse(again.events); self.assertEqual(w.bread_at, 1)
        self.assertFalse(w.journal_records()); self.assertFalse(w.journal_units())

    def test_exact_current_authority_fixture(self):
        fixture = json.loads((ROOT/'tests/fixtures/p10/canonical-bindings.json').read_text())
        catalog = json.loads((ROOT/'authority/full-line-catalog.json').read_text())
        speech = json.loads((ROOT/'authority/speech-units.json').read_text())
        self.assertEqual(fixture['records'], {x['id']: x for x in catalog['records'] if x['id'].startswith('P10.')})
        self.assertEqual(fixture['speech_units'], [x for x in speech['units'] if x['record_id'].startswith('P10.')])
        self.assertEqual(set(fixture['records']), set(RECORD_UNITS))
        self.assertEqual(len(fixture['records']), 23); self.assertEqual(len(fixture['speech_units']), 20)


class ModelBehaviorTests(unittest.TestCase):
    def test_all_eight_material_mixes_keep_original_units(self):
        for bits in itertools.product((0, 1), repeat=3):
            with self.subTest(bits=bits):
                w, _ = prepare(); w.prepare_paper(C)
                ids = tuple((PAPER_IDS if bits[i] else TILE_IDS)[i] for i in range(3))
                for i, cue in enumerate(ids): w.write(C, cue, ORDER[i])
                install(w, ids)
                self.assertTrue(w.rack_correct)
                self.assertEqual(w.reserved_external_items, set(ids) & set(TILE_IDS))
                self.assertEqual(set(w.inventory), set(PAPER_IDS) - set(ids))
                self.assertEqual(w.cue_handoff['slots'], ids)

    def test_all_wrong_orders_specific_feedback_and_repair(self):
        for order in itertools.permutations(range(3)):
            w, ids = prepare()
            for slot, i in enumerate(order):
                r = w.place(RACK, ids[i], slot)
                if i == 1 and slot == 0: self.assertEqual(r.line_ids, ('P10.FAILURE.002',))
                if i == 2 and slot != 2: self.assertEqual(r.line_ids, ('P10.FAILURE.003',))
            self.assertEqual(w.ready, order == (0, 1, 2))
            for i in range(3): w.remove(RACK, i)
            install(w, ids); self.assertTrue(w.rack_correct)

    def test_blank_feedback_requires_bunny_and_does_not_mutate(self):
        w = P10World(); w.introduce(C); before = w.save()
        r = w.place(RACK, TILE_IDS[0], 0)
        self.assertEqual(r.code, 'blank_cue'); self.assertEqual(r.line_ids, ('P10.FAILURE.001',))
        away = replace(RACK, bunny_room=LIVING)
        self.assertEqual(w.place(away, TILE_IDS[0], 0).line_ids, ())
        self.assertEqual(w.save(), before)

    def test_toast_feedback_does_not_ventriloquize_frankie(self):
        w, ids = prepare(); away = replace(RACK, frankie_room=LIVING)
        r = w.place(away, ids[2], 0)
        self.assertEqual(r.code, 'cue_placed'); self.assertEqual(r.line_ids, ())
        w.remove(RACK, 0)
        self.assertEqual(w.place(RACK, ids[2], 0).line_ids, ('P10.FAILURE.003',))

    def test_occupied_slot_and_same_item_are_nonmutating_then_move(self):
        w, ids = prepare(); w.place(RACK, ids[0], 0); before = w.save()
        self.assertEqual(w.place(RACK, ids[1], 0).code, 'remove_occupied_cue_first')
        self.assertEqual(w.place(RACK, ids[0], 0).code, 'cue_already_placed')
        self.assertEqual(w.save(), before)
        r = w.place(RACK, ids[0], 1)
        self.assertEqual(w.slots, [None, ids[0], None])
        self.assertEqual(r.events[0].payload, dict(serial=w.revision, puzzle='P10',
            item=ids[0], origin='cue_rack', destination='cue_rack', slot=1, restored_first_time=False))

    def test_host_ownership_conservation_and_context_duplicate_rejection(self):
        w, ids = prepare(); pocket = set(C.inventory)
        for i, cue in enumerate(ids):
            ctx = replace(RACK, inventory=frozenset(pocket))
            r = w.place(ctx, cue, i); pocket.remove(cue)
            w.validate_context(replace(RACK, inventory=frozenset(pocket)))
            self.assertEqual((pocket & set(ids)) | w.reserved_external_items, set(ids))
            self.assertFalse((pocket & set(ids)) & w.reserved_external_items)
            with self.assertRaises(ValueError): w.validate_context(ctx)
            self.assertEqual(r.events[0].payload['origin'], 'inventory')
        for i, cue in enumerate(ids):
            r = w.remove(replace(RACK, inventory=frozenset(pocket)), i); pocket.add(cue)
            self.assertEqual(r.events[0].payload['destination'], 'inventory')
            w.validate_context(replace(RACK, inventory=frozenset(pocket)))
        self.assertEqual(frozenset(pocket), C.inventory)

    def test_material_and_pencil_prerequisites_do_not_grant_objects(self):
        w = P10World(); empty = replace(KNOWN, inventory=frozenset())
        self.assertEqual(w.prepare_paper(empty).code, 'master_card_required')
        self.assertEqual(w.pick_up_tiles(empty).code, 'p03_tiles_required')
        self.assertEqual(w.write(empty, TILE_IDS[0], 'SERVE').code, 'cue_unavailable')
        self.assertEqual(w.write(replace(KNOWN, inventory=frozenset(TILE_IDS)), TILE_IDS[0], 'SERVE').code, 'pencil_required')
        self.assertEqual(w.write(KNOWN, PAPER_IDS[0], 'SERVE').code, 'cue_unavailable')
        self.assertEqual(w.inventory, ()); self.assertEqual(w.revision, 0)
        w.prepare_paper(KNOWN)
        self.assertEqual(w.write(replace(KNOWN, inventory=frozenset({'grease_pencil'})), PAPER_IDS[0], 'SERVE').code, 'cue_written')
        self.assertFalse(w.bread_at)

    def test_snack_discovery_required_before_installation(self):
        w = P10World(); w.write(KNOWN, TILE_IDS[0], 'SERVE')
        self.assertEqual(w.place(replace(KNOWN, room=COURTYARD), TILE_IDS[0], 0).code, 'snacks_not_discovered')
        self.assertEqual(w.slots, [None] * 3)

    def test_base_barriers_are_nonmutating(self):
        for ctx, expected in [(replace(C, flags=frozenset()), 'evening_required'),
                              (replace(C, on_apron=True), 'offscreen'),
                              (replace(C, contest_active=True), 'contest_active')]:
            w = P10World(); before = w.save()
            for call in [lambda: w.introduce(ctx), lambda: w.prepare_paper(ctx),
                         lambda: w.write(ctx, TILE_IDS[0], None), lambda: w.place(ctx, TILE_IDS[0], 0),
                         lambda: w.remove(replace(ctx, room=COURTYARD), 0), lambda: w.hint(ctx, 1),
                         lambda: w.look(ctx, 'board'), lambda: w.pick_up_tiles(ctx),
                         lambda: w.begin_presentation(ctx, 'plan')]:
                self.assertEqual(call().code, expected); self.assertEqual(w.save(), before)

    def test_source_room_and_actor_barriers(self):
        w = P10World()
        self.assertEqual(w.begin_presentation(RACK, 'plan').code, 'offscreen')
        self.assertEqual(w.begin_presentation(C, 'rack').code, 'offscreen')
        self.assertEqual(w.introduce(replace(C, bunny_room=COURTYARD)).code, 'speaker_absent')
        self.assertEqual(w.begin_presentation(C, 'intro').code, 'snacks_not_discovered')
        self.assertEqual(w.begin_presentation(C, 'bread_agreement').code, 'snacks_not_discovered')
        self.assertEqual(w.begin_presentation(C, 'notebook').code, 'cues_not_restored')
        self.assertEqual(w.begin_presentation(C, 'credit').code, 'tile_substitution_required')
        self.assertEqual(w.begin_presentation(replace(C, inventory=frozenset()), 'tiles').code, 'tiles_unavailable')
        for room in ('L03_PORCH', 'L04_SIDE_PASSAGE', 'L06_GARAGE', CONSERVATORY):
            self.assertEqual(w.introduce(replace(C, room=room, bunny_room=room)).code, 'speaker_absent')
        self.assertFalse(w.revision)

    def test_offscreen_reserved_tiles_remain_inaccessible(self):
        w, ids = prepare(); install(w, ids)
        away = replace(C, inventory=C.inventory-set(ids)); present = replace(away, room=COURTYARD)
        self.assertEqual(w.begin_presentation(away, 'tiles').code, 'tiles_unavailable')
        r = w.begin_presentation(present, 'tiles')
        self.assertEqual(w.acknowledge_presentation(away, r.presentation_id, record_id='P10.LOOK.002').code, 'tiles_unavailable')
        self.assertEqual(w.acknowledge_presentation(present, r.presentation_id, record_id='P10.LOOK.002').code, 'presentation_acknowledged')
        for cue in ids:
            self.assertEqual(w.look(away, cue).code, 'offscreen')
            self.assertEqual(w.write(away, cue, None).code, 'offscreen')
        self.assertEqual(w.remove(away, 0).code, 'offscreen')

    def test_credit_requires_actual_ceramic_substitution_and_rita(self):
        w, ids = prepare(True); install(w, ids)
        self.assertEqual(w.begin_presentation(replace(RACK, rita_room=COURTYARD), 'credit').code, 'tile_substitution_required')
        w.remove(RACK, 0); w.write(C, TILE_IDS[0], 'SERVE'); w.place(RACK, TILE_IDS[0], 0)
        self.assertEqual(w.begin_presentation(RACK, 'credit').code, 'speaker_absent')
        ctx = replace(RACK, rita_room=COURTYARD); r = w.begin_presentation(ctx, 'credit')
        w.acknowledge_presentation(ctx, r.presentation_id, speech_unit_ids=('P10.DIALOGUE.001.01',))
        self.assertEqual(w.acknowledge_presentation(RACK, r.presentation_id, speech_unit_ids=('P10.DIALOGUE.001.02',)).code, 'speaker_absent')
        w.acknowledge_presentation(ctx, r.presentation_id, speech_unit_ids=('P10.DIALOGUE.001.02',))
        self.assertIn('P10.DIALOGUE.001', w.journal_records())
        self.assertEqual(w.flags, {'CUES_RESTORED'})

    def test_bread_agreement_keeps_existing_exact_two_units(self):
        w = P10World(); w.introduce(C); r = w.begin_presentation(C, 'bread_agreement')
        for unit in ('P10.DIALOGUE.002.01', 'P10.DIALOGUE.002.02'):
            w.acknowledge_presentation(C, r.presentation_id, speech_unit_ids=(unit,))
        self.assertEqual(w.journal_units(), ('P10.DIALOGUE.002.01', 'P10.DIALOGUE.002.02'))
        self.assertFalse(w.flags); before = w.save()
        self.assertEqual(w.begin_presentation(C, 'bread_agreement').line_ids, ('P10.DIALOGUE.002',))
        self.assertEqual(w.save(), before)

    def test_notebook_and_board_are_repeatable_after_later_edits(self):
        w, ids = prepare(); install(w, ids); show(w, 'notebook', RACK)
        w.remove(RACK, 0); w.write(RACK, ids[1], None); w = clone(w)
        before = w.save()
        self.assertEqual(w.begin_presentation(C, 'plan').line_ids, ('P10.READ.001',))
        self.assertEqual(w.begin_presentation(RACK, 'notebook').line_ids, ('P10.READ.002',))
        self.assertEqual(w.save(), before); self.assertTrue(w.knows_order(C))
        self.assertIn('P10.READ.002', w.journal_records()); self.assertFalse(w.rack_correct)

    def test_pure_queries_are_deeply_detached_and_do_not_consume_sources(self):
        w, ids = prepare(); install(w, ids); before = w.save()
        for _ in range(2):
            w.choices(C); w.journal_records(); w.journal_units(); w.object_location(ids[0], C)
            w.look(C, 'board'); w.look(RACK, 'rack_spring_clips'); w.inventory; w.reserved_external_items
        handoff = w.cue_handoff; handoff['slots'] = (); saved = w.save(); saved['state']['labels'][ids[0]] = None
        self.assertEqual(w.save(), before); self.assertTrue(w.rack_correct)

    def test_rack_clips_are_distinct_and_never_consume_laundry_clips(self):
        w, ids = prepare(); ctx = replace(RACK, inventory=RACK.inventory | {'laundry_clips'})
        self.assertEqual(w.look(ctx, 'rack_spring_clips').line_ids, ('P10.LOOK.003',))
        before = ctx.inventory
        for i, cue in enumerate(ids): w.place(ctx, cue, i)
        self.assertEqual(ctx.inventory, before); self.assertTrue(w.cue_handoff['built_in_clips'])
        self.assertNotIn('laundry_clips', w.reserved_external_items)

    def test_nine_verbs_unknown_objects_and_audience_cannot_change_state(self):
        w = P10World(); before = w.save()
        for verb, obj in itertools.product(Verb, ('audience', 'renewal_repair_card', 'garbage', 'rack_spring_clips')):
            r = w.act(C, verb, obj)
            self.assertFalse(r.events); self.assertEqual(w.save(), before)
        self.assertEqual(w.act(C, Verb.OPEN, 'board').code, 'presentation_pending')
        self.assertEqual(w.act(C, Verb.PICK_UP, 'ceramic_sample_tiles').code, 'existing_tiles')
        self.assertEqual(w.act(C, Verb.USE, 'master_invitation', 'cue_rack').code, 'paper_prepared')
        self.assertEqual(w.act(C, Verb.TALK_TO, 'bunny', 'cues').code, 'presentation_pending')
        self.assertEqual(w.act(C, Verb.TALK_TO, 'bunny', 'bread').code, 'presentation_pending')

    def test_hint_events_only_on_new_highest_level(self):
        w = P10World()
        for level, expected in [(1, True), (3, True), (2, False), (3, False)]:
            r = w.hint(C, level); self.assertEqual(bool(r.events), expected)
            self.assertEqual(r.line_ids, (f'P10.HINT.{level}',))
        self.assertEqual(w.hint_level, 3); self.assertFalse(w.knows_order(C))

    def test_seeded_edits_restore_and_conserve_all_six_units(self):
        rng = random.Random(1010); w, _ = prepare(); w.prepare_paper(C)
        for cue, word in zip(PAPER_IDS, ORDER): w.write(C, cue, word)
        for i in range(250):
            action = rng.choice(('write', 'place', 'remove', 'hint', 'look'))
            ctx = replace(RACK, inventory=RACK.inventory-w.reserved_external_items)
            if action == 'write': w.write(ctx, rng.choice(CUE_IDS), rng.choice((None, *ORDER)))
            elif action == 'place': w.place(ctx, rng.choice(CUE_IDS), rng.randrange(3))
            elif action == 'remove': w.remove(ctx, rng.randrange(3))
            elif action == 'hint': w.hint(ctx, rng.randrange(1, 4))
            else: w.look(ctx, rng.choice((*CUE_IDS, 'cue_rack', 'board', 'tray')))
            current = replace(RACK, inventory=RACK.inventory-w.reserved_external_items)
            w.validate_context(current)
            self.assertEqual(set(w.inventory) | (set(w.slots)-{None}) | (set(TILE_IDS)-w.reserved_external_items), set(CUE_IDS))
            w = clone(w)

class CaptionAndValidationTests(unittest.TestCase):
    def test_intro_partial_receipts_survive_absence_and_replay(self):
        w = P10World(); r = w.introduce(C); pid = r.presentation_id
        away = replace(C, bunny_room=COURTYARD)
        self.assertEqual(w.acknowledge_presentation(away, pid, record_id='P10.OPEN.001').code, 'speaker_absent')
        self.assertEqual(w.acknowledge_presentation(away, pid, speech_unit_ids=('P10.OPEN.001.01',)).code, 'presentation_acknowledged')
        self.assertEqual(w.journal_units(), ('P10.OPEN.001.01',)); self.assertEqual(w.journal_records(), ())
        self.assertEqual(w.resume_presentation(away, 'intro').code, 'speaker_absent')
        self.assertEqual(w.resume_presentation(C, 'intro').speech_unit_ids, RECORD_UNITS['P10.OPEN.001'][1:])
        w.acknowledge_presentation(C, pid, speech_unit_ids=('P10.OPEN.001.02', 'P10.OPEN.001.03'))
        w = clone(w); old = pid; pid = w.resume_presentation(C, 'intro').presentation_id
        self.assertNotEqual(old, pid)
        self.assertEqual(w.acknowledge_presentation(C, old, record_id='P10.OPEN.001').code, 'stale_presentation')
        w.acknowledge_presentation(C, pid, record_id='P10.OPEN.001')
        self.assertEqual(w.journal_records(), ('P10.OPEN.001',))
        self.assertEqual(w.journal_units(), RECORD_UNITS['P10.OPEN.001'])
        before = w.save()
        self.assertEqual(w.acknowledge_presentation(C, pid, record_id='P10.OPEN.001').code, 'presentation_already_acknowledged')
        self.assertEqual(w.begin_presentation(C, 'intro').line_ids, ('P10.OPEN.001',))
        self.assertEqual(w.resume_presentation(C, 'intro').line_ids, ())
        self.assertEqual(w.save(), before)

    def test_wrong_record_out_of_order_noncontiguous_and_duplicate_receipts(self):
        w = P10World(); pid = w.introduce(C).presentation_id; before = w.save()
        cases = [dict(record_id='P10.HINT.1'), dict(speech_unit_ids=('P10.OPEN.001.02',)),
                 dict(speech_unit_ids=('P10.OPEN.001.01','P10.OPEN.001.03')),
                 dict(speech_unit_ids=('P10.OPEN.001.01','P10.OPEN.001.01')),
                 dict(record_id='P10.OPEN.001',speech_unit_ids=('P10.OPEN.001.01',)),
                 dict(speech_unit_ids=['P10.OPEN.001.01']), dict(), dict(speech_unit_ids=(True,))]
        for kw in cases:
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError): w.acknowledge_presentation(C, pid, **kw)
                self.assertEqual(w.save(), before)
        plan = w.begin_presentation(C, 'plan')
        with self.assertRaises(ValueError): w.acknowledge_presentation(C, plan.presentation_id, speech_unit_ids=('P10.READ.001',))

    def test_whole_record_after_partial_checks_only_new_speakers(self):
        w = P10World(); r = w.introduce(C)
        w.acknowledge_presentation(C, r.presentation_id, speech_unit_ids=RECORD_UNITS['P10.OPEN.001'][:5])
        self.assertEqual(w.acknowledge_presentation(replace(C,bunny_room=COURTYARD), r.presentation_id, record_id='P10.OPEN.001').code, 'speaker_absent')
        w.acknowledge_presentation(C, r.presentation_id, record_id='P10.OPEN.001')
        self.assertEqual(w.journal_units(), RECORD_UNITS['P10.OPEN.001'])

    def test_cross_world_and_restored_epochs_are_unique(self):
        w = P10World(); pid = w.introduce(C).presentation_id
        other = P10World(); other.introduce(C)
        self.assertEqual(other.acknowledge_presentation(C,pid,record_id='P10.OPEN.001').code,'stale_presentation')
        restored = [clone(w) for _ in range(3)]
        self.assertEqual(len({x._handle('intro') for x in restored} | {pid}), 4)
        for x in restored: self.assertEqual(x.save(), w.save())

    def test_all_sources_partial_resume_complete_and_saved_learning(self):
        w, ids = prepare(); install(w, ids); ctx = replace(RACK, rita_room=COURTYARD)
        for source in w.SOURCES:
            here = C if source == 'plan' else ctx
            r = w.begin_presentation(here, source)
            if w._complete(source): continue
            for token in w._tokens(source):
                if token in UNIT_SPEAKERS: kw = dict(speech_unit_ids=(token,))
                else: kw = dict(record_id=token)
                w.acknowledge_presentation(here, r.presentation_id, **kw)
                w = clone(w)
                r = w.resume_presentation(here, source)
            self.assertTrue(w._complete(source))
        self.assertEqual(set(w.journal_records()), set(w.SOURCES.values()))
        self.assertEqual(set(w.journal_units()), {t for s in w.SOURCES for t in w._tokens(s) if t in UNIT_SPEAKERS})
        self.assertTrue(w.knows_order(C)); self.assertTrue(w.ready)

    def test_source_start_order_controls_saved_journal_order(self):
        w = P10World(); a = w.introduce(C); b = w.begin_presentation(C,'plan')
        w.acknowledge_presentation(C,b.presentation_id,record_id='P10.READ.001')
        w.acknowledge_presentation(C,a.presentation_id,record_id='P10.OPEN.001')
        self.assertEqual(w.journal_records(), ('P10.OPEN.001','P10.READ.001'))
        self.assertEqual(clone(w).journal_records(), w.journal_records())

    def test_shared_caption_subclass_keeps_exact_behavior(self):
        @dataclass
        class SharedProbe(_Captioned):
            PUZZLE = 'probe'; KIND = 'probe-save'
            SOURCES = {'read': 'P10.READ.001', 'speak': 'P10.DIALOGUE.002'}
            UNITS = RECORD_UNITS; SPEAKERS = UNIT_SPEAKERS
            def validate(self): self._validate_captions()
            def validate_context(self, context): self.validate()
            def _presentation_block(self, context, source, tokens): return None
        w = SharedProbe(); r = w.begin_presentation(None,'speak')
        w.acknowledge_presentation(None,r.presentation_id,speech_unit_ids=('P10.DIALOGUE.002.01',))
        restored = SharedProbe.load(json.loads(json.dumps(w.save())))
        self.assertEqual(restored.acknowledge_presentation(None,r.presentation_id,record_id='P10.DIALOGUE.002').code,'stale_presentation')
        resumed = restored.resume_presentation(None,'speak')
        self.assertEqual(resumed.speech_unit_ids, ('P10.DIALOGUE.002.02',))
        restored.acknowledge_presentation(None,resumed.presentation_id,record_id='P10.DIALOGUE.002')
        self.assertEqual(restored.journal_records(), ('P10.DIALOGUE.002',))
        self.assertEqual(restored.journal_units(), RECORD_UNITS['P10.DIALOGUE.002'])

    def test_invalid_save_envelope_and_scalar_types_fail_closed(self):
        pristine = P10World().save()
        mutations = [lambda d:d.update(schema=True), lambda d:d.update(extra=0), lambda d:d.update(kind='other'),
            lambda d:d['state'].update(revision=True), lambda d:d['state'].update(revision=-1),
            lambda d:d['state'].update(unknown=1), lambda d:d['state'].update(hint_level=True),
            lambda d:d['state'].update(hint_level=4), lambda d:d['state'].update(bread_at=True),
            lambda d:d['state'].update(labels={}), lambda d:d['state']['labels'].update({TILE_IDS[0]:True}),
            lambda d:d['state'].update(slots=[True,None,None]), lambda d:d['state'].update(slots=(None,None,None)),
            lambda d:d['state'].update(slots=[None,None]), lambda d:d['state'].update(presentations=[])]
        for i, mutation in enumerate(mutations):
            with self.subTest(i=i):
                value=copy.deepcopy(pristine);mutation(value)
                with self.assertRaises(ValueError): P10World.load(value)

    def test_invalid_caption_serials_prefixes_and_collisions(self):
        w = P10World(); r = w.introduce(C)
        w.acknowledge_presentation(C,r.presentation_id,speech_unit_ids=RECORD_UNITS['P10.OPEN.001'][:2])
        w.begin_presentation(C,'plan')
        changes = [lambda d:d['state']['presentations']['intro'].update(serial=0),
            lambda d:d['state']['presentations']['intro'].update(serial=True),
            lambda d:d['state']['presentations']['intro']['receipts'].update({'P10.OPEN.001.01':0}),
            lambda d:d['state']['presentations']['intro']['receipts'].update({'P10.OPEN.001.01':True}),
            lambda d:d['state']['presentations']['intro'].update(receipts={'P10.OPEN.001.02':3}),
            lambda d:d['state']['presentations']['intro'].update(receipts={'P10.OPEN.001.02':3,'P10.OPEN.001.01':3}),
            lambda d:d['state']['presentations']['intro'].update(receipts={'P10.OPEN.001.01':4,'P10.OPEN.001.02':3}),
            lambda d:d['state']['presentations']['plan'].update(serial=2),
            lambda d:d['state']['presentations']['plan'].update(serial=3),
            lambda d:d['state']['presentations']['plan'].update(extra=True),
            lambda d:d['state']['presentations'].update(unknown={'serial':4,'receipts':{}})]
        for i, change in enumerate(changes):
            with self.subTest(i=i):
                value=w.save();change(value)
                with self.assertRaises(ValueError):P10World.load(value)

    def test_invalid_physical_save_and_causal_prerequisites(self):
        w, ids = prepare(); install(w, ids); show(w,'notebook',RACK)
        changes = [lambda d:d['state'].update(bread_at=0), lambda d:d['state'].update(restored_at=0),
            lambda d:d['state'].update(restored_at=d['state']['bread_at']),
            lambda d:d['state'].update(restored_at=d['state']['revision']+1),
            lambda d:d['state']['slots'].__setitem__(1,TILE_IDS[0]),
            lambda d:d['state']['slots'].__setitem__(0,PAPER_IDS[0]),
            lambda d:d['state']['labels'].__setitem__(PAPER_IDS[0],'SERVE'),
            lambda d:d['state'].update(restored_at=d['state']['presentations']['notebook']['serial'])]
        for i, change in enumerate(changes):
            with self.subTest(i=i):
                value=w.save();change(value)
                with self.assertRaises(ValueError):P10World.load(value)

    def test_context_claims_and_types_fail_closed(self):
        for fields in [dict(room='wrong'),dict(room=True),dict(on_apron=1),dict(contest_active=1),
                       dict(flags={'EVENING_STARTED'}),dict(inventory=frozenset({True})),
                       dict(inventory=frozenset({'board'})),dict(inventory=frozenset({PAPER_IDS[0]}))]:
            with self.assertRaises(ValueError):replace(C,**fields)
        w=P10World()
        with self.assertRaises(ValueError):w.validate_context(replace(C,flags=C.flags|{'CUES_RESTORED'}))
        w.introduce(C)
        with self.assertRaises(ValueError):P10World.load(w.save(),context=replace(C,flags=frozenset()))
        with self.assertRaises(ValueError):w.hint(None,1)

    def test_invalid_action_inputs_are_nonmutating(self):
        w=P10World();before=w.save()
        for value in (True,1.5,'1',-1,3):
            with self.assertRaises(ValueError):w.remove(RACK,value)
            with self.assertRaises(ValueError):w.place(RACK,TILE_IDS[0],value)
        for value in (True,'DANCE',1,[]):
            with self.assertRaises(ValueError):w.write(C,TILE_IDS[0],value)
        for value in (True,0,4,'1'):
            with self.assertRaises(ValueError):w.hint(C,value)
        with self.assertRaises(ValueError):w.write(C,'laundry_clips','SERVE')
        with self.assertRaises(ValueError):w.begin_presentation(C,'unknown')
        with self.assertRaises(ValueError):w.act(C,'Eat','master_invitation')
        self.assertEqual(w.save(),before)

class PriorComponentTests(unittest.TestCase):
    def test_accepted_p03_p08_models_then_p10_without_p09(self):
        import sys
        spec=importlib.util.spec_from_file_location('accepted_p03_numeric',ROOT/'dependencies/p03_numeric_model.py')
        module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
        p3=module.P03();p3.context(6,0,1,1);p3.look(37);p3.begin_credit();p3.select(1)
        p3.context(2,0,1,1);p3.collect(38);p3.context(6,0,1,1);p3.pad(38);p3.give_slate()
        self.assertTrue(p3.validate());self.assertEqual(p3.state.ready,1)
        self.assertEqual(p3.inventory(),[35]);self.assertEqual([p3.location(i) for i in TILE_NATIVE_IDS],[10,10,10])
        p3_before=copy.deepcopy(p3.state)
        from cakood.p08_model import P08World,P08Context,PREPARATIONS,Position,READINESS_RECORDS,EVENING_POSITIONS
        p8=P08World();c8=P08Context(COURTYARD,flags=PREPARATIONS,carrier_padding='clean_napkin',
            inventory=C.inventory,frankie_room=COURTYARD,bunny_room=COURTYARD)
        for obj,pos in [('ceramic_carrier',Position.HATCH),('pa_kit',Position.WALL),
                        ('completed_screen',Position.ALCOVE),('serving_table',Position.HATCH),('credit_slate',Position.HATCH)]:
            p8.place(c8,obj,pos)
        p8.unpack_service(c8)
        for h in p8.pending_handoffs:p8.acknowledge_handoff(h['handoff_id'],h['serial'])
        p8.request_start(c8);token=p8.pending_request_id
        p8.acknowledge_readiness(c8,token,READINESS_RECORDS);p8.confirm_start(c8,token,True)
        w=P10World();c10=replace(C,room=KITCHEN,bunny_room=EVENING_POSITIONS['bunny'],
            frankie_room=EVENING_POSITIONS['frankie'],rita_room=EVENING_POSITIONS['rita'],flags=frozenset(c8.flags|p8.flags))
        self.assertEqual(w.introduce(c10).code,'evening_required')
        p8.acknowledge_autosave(c8,token,True);c10=replace(c10,flags=frozenset(c8.flags|p8.flags));p8_before=p8.save()
        self.assertEqual(w.introduce(c10).code,'presentation_pending')
        show(w,'plan',replace(c10,room=LIVING))
        for cue,word in zip(TILE_IDS,ORDER):w.write(c10,cue,word)
        pocket=set(c10.inventory)
        for i,cue in enumerate(TILE_IDS):
            w.place(replace(c10,room=COURTYARD,inventory=frozenset(pocket)),cue,i);pocket.remove(cue)
        w.validate_context(replace(c10,room=COURTYARD,inventory=frozenset(pocket)))
        self.assertTrue(w.ready);self.assertEqual(p3.state,p3_before);self.assertEqual(p8.save(),p8_before)
        self.assertFalse({'RUMOR_CLEARED','TERMS_CARD_AVAILABLE'} & (c10.flags|w.flags))
        self.assertEqual(p8.returned_padding,'clean_napkin')
        self.assertNotIn('P09', ''.join(w.flags))

    def test_accepted_current_p09_schema_retains_tile_names(self):
        schema=json.loads((ROOT/'dependencies/p09-schema.json').read_text())
        self.assertEqual(tuple(schema['objects'][x] for x in TILE_IDS),(48,49,50))

if __name__ == '__main__': unittest.main()
