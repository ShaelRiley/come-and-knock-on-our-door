"""Independent corrupted-save rejection and detached credit-timeline coverage."""
from test_domain import *
import random
del DomainTests, BytecodeTests


def snapshots():
    """Reachable model snapshots at every visible receipt and physical transfer."""
    w = P14World()
    c = C
    out = []

    def snap():
        out.append(w.save())

    def act(method, *args):
        getattr(w, method)(c, *args)
        snap()

    def show(source):
        act('begin_presentation', source)
        for token in w._tokens(source):
            if token in M['speech_unit_ids']:
                w.acknowledge_presentation(c, w._handle(source), speech_unit_ids=(token,))
            else:
                w.acknowledge_presentation(c, w._handle(source), record_id=token)
            snap()

    snap()
    act('start', UNSIGNED)
    for source in ('opening', 'warm_toast', 'dry_toast'):
        show(source)
    for person in PEOPLE:
        show('card:' + person)
        show('approve:' + person)
        act('pin_card', person)
    show('signature')
    act('pin_signature')
    c = replace(c, inventory=c.inventory - {TERMS})
    act('give_pencil')
    c = replace(c, inventory=c.inventory - {PENCIL})
    for source in ('date', 'readback', 'return_pencil'):
        show(source)
    act('complete_commitments')
    c = replace(c, inventory=c.inventory | {PENCIL})
    w.start_finale(tuple(ASSET_CREDITS.values()))
    snap()
    for source in ('closing:professional', 'meal', 'tag'):
        c = finale_context(c, source)
        show(source)
        if source == 'tag':
            w.claim_tag_laugh()
            snap()
        w.advance_finale()
        snap()
    w.acknowledge_freeze(w.pending_freeze_id)
    snap()
    w.claim_celebration()
    snap()
    w.advance_finale()
    snap()
    for record in w.credit_ids:
        show('credit:' + record)
        w.advance_finale()
        snap()
    return out


def model_valid(props):
    try:
        data = decode_words(list(props.values()))
        P14World.load(data)
        # Do not accept noncanonical unused words dropped by the decoder.
        return encode_save(data) == props
    except (ValueError, KeyError, TypeError, IndexError, OverflowError):
        return False


class ValidationTests(unittest.TestCase):
    def test_emitted_validator_reachable_and_corrupt_model_parity(self):
        states = [encode_save(s) for s in snapshots()]
        cases = {tuple(p.values()): p for p in states}
        rng = random.Random(140996)
        done, empty = states[-1], states[0]

        def add(p, changes):
            q = {**p, **changes}
            cases[tuple(q.values())] = q

        for key in M['persisted_properties']:
            add(done, {key: -1})
            add(done, {key: 0})
        for source, sid in M['sources'].items():
            name = M['serials'][M['source_start_offset'] + sid - 1]
            add(done, {'p14' + name + 'Hi': 0, 'p14' + name + 'Lo': 0})
            for receipt in M['receipts'][source]:
                name = M['serials'][receipt['slot']]
                add(empty, {'p14RevisionLo': 3, 'p14' + name + 'Lo': 2})
        for _ in range(240):
            p = rng.choice(states)
            key = rng.choice(M['persisted_properties'])
            add(p, {key: rng.choice((0, 1, 2, 32767))})
        vm = ByteVM()
        valid = invalid = 0
        for p in cases.values():
            expected = model_valid(p)
            vm.p.update(p)
            before = vm.persistent()
            actual = bool(vm.call('p14Validate'))
            self.assertEqual(actual, expected, ('save parity',
                {k: x for k, x in p.items() if x != done[k]}))
            self.assertEqual(before, vm.persistent())
            if actual:
                valid += 1
            else:
                invalid += 1
        report = {'scope': 'Actual emitted script996 validation; strict self sends and stack returns',
            'reachable_snapshots': len(states), 'distinct_vectors': len(cases),
            'valid': valid, 'rejected': invalid, 'instructions_executed': vm.machine.steps,
            'script_sha256': hashlib.sha256(vm.machine.blob).hexdigest(), 'passed': True}
        (HERE / 'evidence/compiled-validation.json').write_text(json.dumps(report, indent=2) + '\n')

    def test_all_6561_approval_and_pin_ledger_projections(self):
        # Each person's state is pending / visibly approved / physically pinned.
        # Removing later ledgers from this reachable snapshot keeps valid serial
        # gaps and preserves the exact approval-before-pin ordering for each card.
        base, _ = approve14()
        vm = ByteVM()
        count = 0
        for projection in itertools.product(range(3), repeat=8):
            w = P14World.load(base.save())
            for person, state in zip(PEOPLE, projection):
                if state < 2:
                    del w.pinned[person]
                if state == 0:
                    del w.presentations['approve:' + person]
            w.validate()
            vm.p.update(encode_world(w))
            self.assertEqual(vm.call('p14Validate'), 1, projection)
            self.assertEqual(tuple(O[x] for i in range(9)
                if (x := vm.call('p14InventoryAt', i))), w.inventory)
            count += 1
        self.assertEqual(count, 6561)
        (HERE / 'evidence/finite-approval-projection.json').write_text(json.dumps({
            'approval_pin_projections': count, 'persons': list(PEOPLE),
            'actual_emitted_bytecode': True, 'strict_stack_balance': True,
            'instructions_executed': vm.machine.steps, 'passed': True}, indent=2) + '\n')

    def test_strict_codec_schema_types_causal_gates_and_restore_failure(self):
        raw = snapshots()[-1]
        for value in (True, '1', 1.1, -1, M['max_serial'] + 1):
            bad = copy.deepcopy(raw)
            bad['state']['revision'] = value
            with self.assertRaises(ValueError):
                encode_save(bad)
        for key, value in [('kind', 'other'), ('schema', True), ('state', []), ('extra', 1)]:
            bad = copy.deepcopy(raw)
            bad[key] = value
            with self.assertRaises(ValueError):
                encode_save(bad)
        for key, value in [('winning_attempts', {}), ('pinned', {}),
                ('repair_date', ''), ('repair_date', 'bad\nfictional date'),
                ('credit_ids', ['END.CREDIT.INVENTED']), ('credit_cursor', 200),
                ('finale_phase', 'credits'), ('replay_mode', 1),
                ('presentations', {'invented': {'serial': 1, 'receipts': {}}})]:
            bad = copy.deepcopy(raw)
            bad['state'][key] = value
            if key == 'finale_phase':
                bad['state']['frame_at'] = 0
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                encode_save(bad)
        bad = copy.deepcopy(raw)
        receipts = bad['state']['presentations']['signature']['receipts']
        bad['state']['presentations']['signature']['receipts'] = dict(reversed(list(receipts.items())))
        with self.assertRaises(ValueError):
            encode_save(bad)
        for typ in (source_vm.VM, ByteVM):
            h = Harness(typ, P14World.load(raw))
            h.project(replace(C, inventory=frozenset((PENCIL,))))
            # A missing dated signature invalidates otherwise completed state.
            h.v.p['p14SignatureHi'] = h.v.p['p14SignatureLo'] = 0
            self.assertEqual(h.v.call('p14AfterRestore'), 0)
            self.assertEqual(h.v.p['p14ContextValid'], 0)
            self.assertEqual(h.v.p['p14EventCount'], 0)
            self.assertEqual(h.v.p['p14PresentationSource'], 0)
            before = h.v.persistent()
            h.v.call('p14AdvanceFinale')
            self.assertEqual(CO[h.v.p['p14Code']], 'invalid_state')
            self.assertEqual(before, h.v.persistent())

    def test_credit_replay_is_detached_preserves_invoking_session_on_return(self):
        completed, c = finish14()
        completed.start_finale(tuple(ASSET_CREDITS.values()))
        completed.skip_finale()
        original = completed.save()
        invoking = {'kind': 'another-unfinished-evening', 'complete': False,
            'inventory': ['grease_pencil'], 'nested': {'wins': [], 'room': LIVING}}
        saved = copy.deepcopy(invoking)
        replay = completed.create_credit_replay(invoking)
        invoking['nested']['wins'].append('VC01')
        self.assertEqual(completed.save(), original)
        replay.world.pause_finale(True)
        replay = CreditReplay.load(json.loads(json.dumps(replay.save())))
        returned = replay.return_session(cancel=True)
        self.assertEqual(returned, saved)
        returned['inventory'].clear()
        self.assertEqual(replay.return_session(), saved)
        self.assertEqual(completed.save(), original)
        for typ in (source_vm.VM, ByteVM):
            replay = completed.create_credit_replay(saved)
            h = Harness(typ, replay.world)
            h.project(c)
            self.assertEqual(h.w.finale_phase, 'credits')
            self.assertTrue(h.w.replay_mode)
            before = encode_world(completed)
            h.plain('claim_tag_laugh', 'p14ClaimTagLaugh')
            h.plain('claim_celebration', 'p14ClaimCelebration')
            for record in h.w.credit_ids:
                h.show('credit:' + record, c)
                h.restore()
                h.plain('advance_finale', 'p14AdvanceFinale')
            replay.world = h.w
            self.assertEqual(replay.return_session(), saved)
            self.assertEqual(encode_world(completed), before)
            self.assertTrue(h.w.ready)

    def test_all_caption_prefixes_restore_and_real_actor_receipts(self):
        initial = P14World()
        initial.start(C, UNSIGNED)
        approved, c = approve14()
        signed = P14World.load(approved.save())
        signed.begin_presentation(c, 'signature')
        signed.acknowledge_presentation(c, signed._handle('signature'), record_id=signed.SOURCES['signature'])
        signed.pin_signature(c)
        c = replace(c, inventory=c.inventory - {TERMS})
        signed.give_pencil(c)
        c = replace(c, inventory=c.inventory - {PENCIL})
        base_states = [(s, initial.save(), C) for s in initial.SOURCES
            if s in ('opening', 'warm_toast', 'dry_toast') or s.startswith(('approve:', 'card:'))]
        base_states.append(('signature', approved.save(), C))
        for s in ('date', 'readback', 'return_pencil'):
            base_states.append((s, signed.save(), c))
            signed.begin_presentation(c, s)
            signed.acknowledge_presentation(c, signed._handle(s), record_id=signed.SOURCES[s])
        signed.complete_commitments(c)
        c = replace(c, inventory=c.inventory | {PENCIL})
        signed.start_finale()
        for s in ('closing:professional', 'meal', 'tag'):
            c = finale_context(c, s)
            base_states.append((s, signed.save(), c))
            signed.begin_presentation(c, s)
            signed.acknowledge_presentation(c, signed._handle(s), record_id=signed.SOURCES[s])
            signed.advance_finale()
        for typ in (source_vm.VM, ByteVM):
            for source, save, c in base_states:
                tokens = P14World()._tokens(source)
                for prefix in range(len(tokens) + 1):
                    h = Harness(typ, P14World.load(save))
                    h.begin(source, c)
                    if prefix:
                        if tokens[0] in M['speech_unit_ids']:
                            h.ack(source, units=tokens[:prefix], c=c)
                        else:
                            h.ack(source, record=h.w.SOURCES[source], c=c)
                    h.restore()
                    h.resume(source, c)
                    if prefix < len(tokens):
                        h.ack(source, record=h.w.SOURCES[source], c=c)
                    self.assertTrue(h.w._complete(source))
            h = Harness(typ, P14World.load(approved.save()))
            h.begin('signature', C)
            h.ack('signature', units=h.w._tokens('signature')[:3], c=actors(C, frankie=LIVING))
            self.assertEqual(len(h.w.presentations['signature'].receipts), 3)
            h.ack('signature', record=h.w.SOURCES['signature'], c=actors(C, frankie=LIVING))
            self.assertEqual(len(h.w.presentations['signature'].receipts), 3)
            h.ack('signature', record=h.w.SOURCES['signature'])


if __name__ == '__main__':
    unittest.main()
