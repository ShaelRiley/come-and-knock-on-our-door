"""NEW current-authority/current-API tests. Not historical test passes."""
from contextlib import redirect_stdout
from copy import deepcopy
from dataclasses import replace
import hashlib
import io
from itertools import product
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

from cakood.model import Event, Result
from cakood.p08_model import (P08World, PREPARATIONS, LABEL_IDS, SCRIPT_BINDINGS,
    SOURCE_BINDINGS, LAYOUT_OBJECTS, READINESS_RECORDS, Position, Facing, StartPhase,
    COURTYARD, KITCHEN)
from tests.current_api_support import Preparation, host6
from tests.test_p08_model import C, fit
from tools.regenerate_fixture import regenerate

ROOT = Path(__file__).resolve().parents[1]


class CurrentAuthorityTests(unittest.TestCase):
    def test_all_71_imported_inputs_and_literal_recovery_hashes(self):
        inputs = json.loads((ROOT / 'inputs/SOURCE-INPUTS.json').read_bytes())
        self.assertEqual(len(inputs), 71)
        for item in inputs:
            with self.subTest(path=item['path']):
                data = (ROOT / item['path']).read_bytes()
                self.assertEqual(len(data), item['bytes'])
                self.assertEqual(hashlib.sha256(data).hexdigest(), item['sha256'])
        packet = ROOT / 'inputs/literal-p08'
        manifest = json.loads((packet / 'provenance/recovery-file-inventory.json').read_bytes())
        self.assertEqual(len(manifest['files']), 27)
        for path, record in manifest['files'].items():
            self.assertEqual(hashlib.sha256((packet / path).read_bytes()).hexdigest(),
                             record['sha256_of_recovered_bytes_today'])
        for path, recovered in [('cakood/p08_model.py', 'p08_model.py'),
                                ('tests/test_p08_model.py', 'test_p08_model.py'),
                                ('docs/recovered-p08-state-contract.md', 'p08-state-contract.md')]:
            self.assertEqual((ROOT / path).read_bytes(), (packet / 'recovered-final' / recovered).read_bytes())

    def test_original_literal_assembly_replays_without_touching_packet(self):
        packet = ROOT / 'inputs/literal-p08'
        with tempfile.TemporaryDirectory(prefix='p08-literal-reassembly-') as tmp:
            target = Path(tmp) / 'packet'
            shutil.copytree(packet, target)
            original = (packet / 'provenance/reassemble_text_only.py').read_text()
            old = "BASE = Path('/workspace/shared/cakood-context-recovery-batch2/courtyard-models')"
            self.assertEqual(original.count(old), 1)
            relocated = original.replace(old, f'BASE = Path({str(target)!r})')
            with redirect_stdout(io.StringIO()):
                exec(compile(relocated, 'path-relocated-literal-assembly', 'exec'), {'__name__': '__assembly__'})
            for filename in ('p08_model.py', 'test_p08_model.py', 'p08-state-contract.md'):
                self.assertEqual((target / 'recovered-final' / filename).read_bytes(),
                                 (packet / 'recovered-final' / filename).read_bytes())

    def test_fixture_regenerates_identically_and_binds_all_current_metadata(self):
        fixture_path = ROOT / 'tests/fixtures/p08/canonical-bindings.json'
        before = fixture_path.read_bytes()
        with redirect_stdout(io.StringIO()):
            regenerate()
        self.assertEqual(fixture_path.read_bytes(), before)
        fixture = json.loads(before)
        authority = ROOT / 'inputs/authority'
        catalog = json.loads((authority / 'full-line-catalog.json').read_bytes())
        speech = json.loads((authority / 'speech-units.json').read_bytes())
        records = {r['id']: r for r in catalog['records'] if r['id'].startswith('P08.')}
        self.assertEqual(len(records), 44)
        self.assertEqual(set(fixture['records']), set(records))
        for rid, record in records.items():
            units = [u for u in speech['units'] if u['record_id'] == rid]
            self.assertEqual(fixture['records'][rid], {
                **{key: record[key] for key in ('text_sha256', 'speaker_id', 'source_obligations')},
                'speech_units': [u['line_id'] for u in units],
                'speech_speakers': {u['line_id']: u['speaker_id'] for u in units}})
        self.assertEqual(fixture['editorial_laugh_metadata'], {
            u['line_id']: u['laugh_opportunity'] for u in speech['units']
            if u['record_id'] in records and u.get('laugh_opportunity')})
        for field, path in [('catalog_sha256', 'full-line-catalog.json'),
                            ('speech_sha256', 'speech-units.json'), ('gdd_sha256', 'complete-body.md')]:
            self.assertEqual(fixture[field], hashlib.sha256((authority / path).read_bytes()).hexdigest())

    def test_current_canonical_result_surface_and_source_words(self):
        fixture = json.loads((ROOT / 'tests/fixtures/p08/canonical-bindings.json').read_bytes())
        routed = set(LABEL_IDS.values()) | {rid for ids in SCRIPT_BINDINGS.values() for rid in ids}
        self.assertLessEqual(routed, fixture['records'].keys())
        self.assertEqual(fixture['catalog_sha256'], '3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c')
        self.assertEqual(fixture['editorial_revision'], 3)
        self.assertEqual(fixture['records']['P08.READ.004']['text_sha256'],
                         'a7d6a0019468db46fbac78fc4600de5844cb11e218e9605d3f868b320badfd25')
        result = P08World().place(C, 'pa_kit', Position.WALL)
        self.assertIsInstance(result, Result)
        self.assertTrue(all(isinstance(event, Event) for event in result.events))
        self.assertEqual(result.text, '')
        for ids in SOURCE_BINDINGS.values():
            self.assertLessEqual(set(ids), fixture['records'].keys())


class CurrentCompositionTests(unittest.TestCase):
    def test_real_preparations_both_cloths_and_single_physical_owner(self):
        for cloth in ('clean_towel', 'clean_napkin'):
            with self.subTest(cloth=cloth):
                prior = Preparation(cloth)
                before = prior.prior_saves()
                self.assertLessEqual(PREPARATIONS, prior.context().flags)
                self.assertFalse(prior.contests.flags & {'VC01_WON', 'VC02_WON'})
                world = prior.fit()
                self.assertTrue(world.ready)
                self.assertEqual(world.pending_handoffs, ())
                self.assertEqual(world.returned_padding, cloth)
                self.assertEqual(prior.prior_saves(), before)
                owners = prior.owner_map()
                for obj in ('ceramic_carrier', 'ceramic_service', 'credit_slate', 'pa_kit', 'completed_screen'):
                    self.assertEqual(owners[obj], {'owner': 'P08', 'room': COURTYARD})
                self.assertEqual(owners[cloth], {'owner': 'P08', 'room': KITCHEN})
                self.assertEqual(world.layout_handoff['padding_location'], 'linen_hook')
                self.assertEqual(owners['hotpot_pot'], {'owner': 'P07', 'room': KITCHEN})
                self.assertEqual(owners['handcart'], {'owner': 'P05', 'room': 'L06_GARAGE'})
                self.assertEqual(prior.p3.inventory(), [35])
                self.assertEqual([prior.p3.location(x) for x in (48, 49, 50)], [10, 10, 10])
                projection = prior.p7.projection(prior.c7)
                self.assertEqual(projection.tasting_bowls, 8)
                self.assertTrue(projection.includes_jackie)
                self.assertTrue(projection.lid_closed)
                self.assertFalse(projection.heat_on)
                self.assertEqual(world.inventory, ())
                self.assertFalse(world.flags & {'SERVED', 'DISPLAY_STAGED', 'GAME_COMPLETE'})
                snapshot = prior.save_composed(world)
                prior.reconcile(world)
                world.unpack_service(prior.context())
                self.assertEqual(prior.save_composed(world), snapshot)

    def test_every_upstream_requirement_is_preserved(self):
        for missing in PREPARATIONS:
            with self.subTest(missing=missing):
                flags = PREPARATIONS - {missing}
                try:
                    context = replace(C, flags=flags)
                except ValueError:
                    # Existing context cross-branch dependency checks reject this
                    # incoherent claim even before an action can be attempted.
                    continue
                world = P08World()
                before = world.save()
                self.assertEqual(world.place(context, 'serving_table', Position.HATCH).code,
                                 'preparations_required')
                self.assertEqual(world.save(), before)

    def test_current_p06_transaction_failures_leave_both_owners_unchanged(self):
        prior = Preparation()
        world = P08World()
        world.place(prior.context(), 'completed_screen', Position.ALCOVE)
        prior.h6.bind_p08(world, prior.context())
        ticket = prior.h6.pending_p08_screen_claim()
        before = world.save(), prior.owner_map(), prior.prior_saves()
        for failure in ('fail_prepare', 'fail_commit'):
            setattr(prior.h6, failure, True)
            with self.assertRaises(host6.HostPreparationError):
                prior.h6.apply_p08_handoff(ticket)
            self.assertEqual((world.save(), prior.owner_map(), prior.prior_saves()), before)
            setattr(prior.h6, failure, False)
        self.assertTrue(prior.h6.apply_p08_handoff(ticket))
        self.assertFalse(prior.h6.apply_p08_handoff(ticket))
        self.assertEqual(world.pending_handoffs, ())

    def test_actual_composed_checkpoint_disk_io_precedes_evening(self):
        prior = Preparation('clean_napkin')
        world = prior.fit()
        original_history = prior.prior_saves()
        context = prior.context()
        world.request_start(context)
        request = world.pending_request_id
        world.acknowledge_readiness(context, request, READINESS_RECORDS)
        output = world.confirm_start(context, request, True)
        self.assertEqual(output.events[0].kind, 'autosave_request')
        self.assertFalse(world.evening_started)
        checkpoint = prior.save_composed(world)
        with tempfile.TemporaryDirectory(prefix='p08-caller-save-') as tmp:
            path = Path(tmp) / 'pre-evening.json'
            staged = path.with_suffix('.tmp')
            payload = json.dumps(checkpoint, ensure_ascii=False, sort_keys=True).encode()
            with staged.open('wb') as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(staged, path)
            directory = os.open(tmp, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
            self.assertEqual(path.read_bytes(), payload)
            self.assertFalse(world.evening_started)
            result = world.acknowledge_autosave(context, request, True)
            self.assertEqual(result.line_ids, ('P08.SYSTEM.006',))
            self.assertTrue(world.evening_started)
            post = prior.save_composed(world)
            restored = prior.restore_composed(json.loads(path.read_bytes()))
            self.assertFalse(restored.evening_started)
            self.assertEqual(restored.pending_phase, StartPhase.AUTOSAVE)
            self.assertEqual(prior.prior_saves(), original_history)
            self.assertEqual(restored.retry_autosave(prior.context(), request).events[0].kind, 'autosave_request')
            # Ordinary post-transition save/load is quiet and does not replay a grant.
            restored = prior.restore_composed(post)
            self.assertTrue(restored.evening_started)
            before = prior.save_composed(restored)
            self.assertFalse(restored.acknowledge_autosave(prior.context(), request, True).events)
            self.assertEqual(prior.save_composed(restored), before)

    def test_composed_save_load_each_pending_phase_and_failure_retry(self):
        prior = Preparation()
        world = prior.fit()
        context = prior.context()
        world.request_start(context)
        request = world.pending_request_id
        self.assertEqual(world.pending_phase, StartPhase.CHECKLIST)
        world = prior.restore_composed(prior.save_composed(world))
        self.assertEqual(world.pending_phase, StartPhase.CHECKLIST)
        world.acknowledge_readiness(context, request, READINESS_RECORDS)
        world = prior.restore_composed(prior.save_composed(world))
        self.assertEqual(world.pending_phase, StartPhase.CONFIRMATION)
        world.confirm_start(context, request, True)
        before = prior.save_composed(world)
        failed = world.acknowledge_autosave(context, request, False)
        self.assertFalse(failed.events)
        self.assertEqual(prior.save_composed(world), before)
        world = prior.restore_composed(before)
        self.assertEqual(world.retry_autosave(context, request).events[0].kind, 'autosave_request')
        self.assertFalse(world.evening_started)
        self.assertTrue(world.acknowledge_autosave(context, request, True).events)

    def test_cancel_and_layout_change_cancel_late_callbacks_in_composed_state(self):
        prior = Preparation()
        world = prior.fit()
        context = prior.context()
        for cancellation in ('not_yet', 'cancel', 'move'):
            with self.subTest(cancellation=cancellation):
                world.request_start(context)
                request = world.pending_request_id
                world.acknowledge_readiness(context, request, READINESS_RECORDS)
                if cancellation == 'not_yet':
                    world.confirm_start(context, request, False)
                else:
                    world.confirm_start(context, request, True)
                    if cancellation == 'cancel':
                        world.cancel_start(context)
                    else:
                        world.place(context, 'serving_table', Position.LANE)
                before = prior.save_composed(world)
                self.assertFalse(world.acknowledge_autosave(context, request, True).events)
                self.assertEqual(prior.save_composed(world), before)
                self.assertFalse(world.evening_started)
                if cancellation == 'move':
                    world.place(context, 'serving_table', Position.HATCH)
                self.assertTrue(world.ready)


class FiniteLayoutTests(unittest.TestCase):
    def test_all_2048_placed_layouts_against_independent_spatial_oracle(self):
        count = 0
        for positions in product((1, 2, 3, 4), repeat=5):
            for facing in (1, 2):
                world = fit()
                for obj, position in zip(LAYOUT_OBJECTS, positions):
                    world.place(C, obj, position)
                world.orient_pa(C, facing)
                carrier, pa, screen, table, credit = positions
                expected = {'buffet_at_hatch': carrier == table == credit == 1,
                            'sound_facing_inward': pa == 2 and facing == 1,
                            'display_concealed': screen == 3,
                            'hatch_visible': screen != 1,
                            'lane_clear': 4 not in positions}
                self.assertEqual(world.conditions, expected)
                self.assertEqual(world.ready, all(expected.values()))
                self.assertEqual('LAYOUT_READY' in world.flags, all(expected.values()))
                restored = P08World.load(json.loads(json.dumps(world.save())), C)
                self.assertEqual(restored.save(), world.save())
                count += 1
        self.assertEqual(count, 2048)
