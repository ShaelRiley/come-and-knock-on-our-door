"""Accepted P14 oracle versus source methods and actual emitted SCI instructions.

The compiled evaluator checks every self-send and return with a strict stack.
These tests certify state/receipt conformance, not rendering, sound or native IO.
"""
from pathlib import Path
import copy
import hashlib
import itertools
import json
import sys
import unittest
from dataclasses import replace

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT), str(ROOT / 'tests')]
from cakood.model import Verb
from cakood.p12_model import PEOPLE, COURTYARD, LIVING
from cakood.p14_model import (P14World, P14Context, PREREQUISITES, CONTEST_IDS,
    TERMS, PENCIL, CARD_IDS, CREDIT_ORDER, ASSET_CREDITS, CreditReplay,
    RECORD_UNITS, UNIT_SPEAKERS)
from test_late_campaign_models import (c14, contests, approve14, finish14,
    to_freeze, UNSIGNED)
from test_verbal_contest import prepared, play, leave
from codec import M, encode_world, encode_save, decode_words
import source_vm
from compiled_vm import Compiled

C = c14()
TONES = ('professional', 'friendly', 'cautiously_romantic')
PHASES = ('not_started', 'closing', 'meal', 'tag', 'freeze', 'credits', 'finished')
R = {v: k for k, v in M['line_ids'].items()}
U = {v: k for k, v in M['speech_unit_ids'].items()}
E = {v: k for k, v in M['events'].items()}
CO = {v: k for k, v in M['codes'].items()}
SO = {v: k for k, v in M['sources'].items()}
O = {v: k for k, v in M['objects'].items()}


def oid(obj):
    return M['objects'].get(obj, 32767)


def actors(c, **updates):
    return replace(c, npc_locations=tuple({**dict(c.npc_locations), **updates}.items()))


def finale_context(c, source):
    if source == 'tag':
        return replace(c, room=LIVING,
            npc_locations=tuple((p, LIVING) for p in PEOPLE[1:]))
    return c


class ByteVM:
    def __init__(self):
        self.machine = Compiled(HERE, 996, source_vm.DEFAULTS)
        self.p = source_vm.DEFAULTS.copy()
        self.call('p14Init')

    def call(self, name, *args):
        if any(type(x) is not int or not -32768 <= x <= 32767 for x in args):
            raise ValueError('SCI arguments must be signed integer words')
        if name not in source_vm.SIGNATURES or len(args) != source_vm.SIGNATURES[name]:
            raise ValueError('Unknown method or wrong arity')
        return self.machine.execute(name, self.p, args, strict=True)

    def persistent(self):
        return {k: self.p[k] for k in M['persisted_properties']}


class Harness:
    def __init__(self, typ=source_vm.VM, world=None):
        self.w = world or P14World()
        self.v = typ()
        self.v.p.update(encode_world(self.w))
        self.epoch = 1
        self.context = None

    def project(self, c=C):
        if self.context == c:
            return
        self.context = c
        self.epoch += 1
        flags = sum(1 << i for i, flag in enumerate(sorted(PREREQUISITES)) if flag in c.flags)
        rooms = dict(c.npc_locations)
        args = (M['rooms'][c.room], int(c.on_apron), *divmod(flags, 32768),
            M['rooms'][c.board_room], TONES.index(c.vivian_tone), int(c.contest_active),
            *(M['rooms'][rooms[p]] if p in rooms else -1 for p in PEOPLE[1:]), self.epoch)
        assert self.v.call('p14Context', *args) == 1
        for obj in c.inventory:
            assert self.v.call('p14ContextItem', oid(obj)) == 1
        if c.contests:
            for a in c.contests.attempts:
                if a.outcome is not None and a.outcome.winner == 'jack':
                    attempt = int(a.outcome.id.split(':')[1][1:])
                    assert self.v.call('p14ContextWin', CONTEST_IDS.index(a.encounter_id),
                        *divmod(attempt, 32768)) == 1
        for i, ch in enumerate(c.repair_date):
            assert self.v.call('p14ContextDateChar', i, *divmod(ord(ch), 32768)) == 1
        assert self.v.call('p14SealContext') == 1

    def events(self):
        out = []
        for i in range(self.v.p['p14EventCount']):
            name = E[self.v.call('p14Event', i)]
            a, b, c, d = [self.v.call('p14EventArg', i, j) for j in range(4)]
            data = {'serial': self.v.call('p14EventSerialHi', i) * 32768 +
                self.v.call('p14EventSerialLo', i), 'puzzle': 'P14'}
            assert d == 0, (name, a, b, c, d)
            if name == 'P14_PRESENTATION_QUEUED':
                data['source'] = SO[a]
                kind = 'presentation'
                assert b == c == 0
            elif name == 'P14_PRESENTED':
                data.update(source=SO[a], canonical_tokens=tuple(
                    x['token'] for x in M['receipts'][SO[a]][b:c + 1]))
                kind = 'presentation'
            elif name == 'P14_CARD_PINNED':
                person = PEOPLE[a]
                data.update(card_id=CARD_IDS[person], person=person, location='pledge_board')
                kind = 'object'
                assert b == c == 0
            elif name == 'P14_FINALE_SCENE':
                phase = PHASES[a]
                data.update(phase=phase, room=LIVING if phase == 'tag' else None,
                    scene_direction_id='END.FREEZE' if phase == 'freeze' else None)
                kind = 'presentation'
                assert b == c == 0
            elif name == 'P14_FINALE_PAUSE':
                data['paused'] = bool(a)
                kind = 'presentation'
                assert b == c == 0
            else:
                assert a == b == c == 0, (name, a, b, c)
                kind, payload = {
                    'P14_COMMITMENT_START': ('puzzle', {'cards': tuple(CARD_IDS.values())}),
                    'P14_TERMS_SIGNED': ('ownership', {'object_id': TERMS,
                        'from_owner': 'P09', 'to_owner': 'P14', 'location': 'pledge_board',
                        'signed_by': 'stringer'}),
                    'P14_PENCIL_HANDOFF': ('ownership', {'object_id': PENCIL,
                        'from_owner': 'inventory', 'to_owner': 'frankie', 'temporary': True}),
                    'P14_GAME_COMPLETE': ('puzzle', {'flags': ('COMMITMENTS_SIGNED', 'GAME_COMPLETE'),
                        'return_object': PENCIL, 'return_to': 'inventory', 'before_finale': True,
                        'terms_card_location': 'pledge_board'}),
                    'P14_FINALE_BEGIN': ('presentation', {'room': COURTYARD,
                        'complete_credit_ids': tuple(self.w.credit_ids)}),
                    'P14_FREEZE_PRESENTED': ('presentation', {'direction_record': 'END.FREEZE'}),
                    'LAF14': ('laugh', {'after_record': 'P14.ENDING.002', 'protect_meal': True}),
                    'P14_CELEBRATION': ('presentation', {'cleared_asset_required': True,
                        'pcm_policy': 'single_composite_or_serial', 'transient_only': True}),
                    'P14_FINALE_SKIP': ('presentation', {'drop_transient_audio': True,
                        'completion_unchanged': True}),
                }[name]
                data.update(payload)
            out.append((name, kind, data))
        return out

    def check(self, result):
        expected = encode_world(self.w)
        actual = self.v.persistent()
        assert actual == expected, (result.code, {k: (actual[k], x)
            for k, x in expected.items() if actual[k] != x})
        assert CO[self.v.p['p14Code']] == result.code, (CO[self.v.p['p14Code']], result.code)
        assert tuple(R[self.v.call('p14Line', i)]
            for i in range(self.v.p['p14LineCount'])) == result.line_ids
        assert tuple(U[self.v.call('p14Unit', i)]
            for i in range(self.v.p['p14UnitCount'])) == result.speech_unit_ids
        assert self.events() == [(x.id, x.kind, x.payload) for x in result.events], (
            self.events(), result.events)
        sid = self.v.p['p14PresentationSource']
        native = (SO[sid], self.v.p['p14PresentationHi'] * 32768 +
            self.v.p['p14PresentationLo']) if sid else None
        wanted = (result.presentation_id.split(':', 2)[2].rsplit(':', 1)[0],
            int(result.presentation_id.rsplit(':', 1)[1])) if result.presentation_id else None
        assert native == wanted, (native, wanted)
        return result

    def action(self, model, native, *args, c=C):
        self.project(c)
        result = getattr(self.w, model)(c, *args)
        params = args
        if model == 'start':
            params = (oid(TERMS), 1, 0, 0, 14, M['terms_record_id'])
        elif model in ('begin_presentation', 'resume_presentation'):
            params = (M['sources'][args[0]],)
        elif model in ('give_card', 'pin_card'):
            params = tuple(PEOPLE.index(p) for p in args)
        elif model == 'request_signature':
            params = (('agreed_terms', 'forge', 'coerce').index(args[0] if args else 'agreed_terms'),)
        elif model == 'dispatch':
            params = (list(Verb).index(Verb(args[0])) + 1, oid(args[1]),
                oid(args[2]) if len(args) > 2 and args[2] else 0)
        self.v.call(native, *params)
        return self.check(result)

    def plain(self, model, native, *args):
        result = getattr(self.w, model)(*args)
        self.v.call(native, *(int(x) if type(x) is bool else x for x in args))
        return self.check(result)

    def begin(self, source, c=C):
        return self.action('begin_presentation', 'p14Begin', source, c=c)

    def resume(self, source, c=C):
        return self.action('resume_presentation', 'p14Resume', source, c=c)

    def ack(self, source, record=None, units=(), c=C):
        self.project(c)
        p = self.w.presentations[source]
        sid = M['sources'][source]
        self.v.call('p14Resume', sid)
        result = self.w.acknowledge_presentation(c, self.w._handle(source),
            record_id=record, speech_unit_ids=units)
        self.v.call('p14Acknowledge', sid, *divmod(p.serial, 32768), self.epoch,
            M['line_ids'][record] if record else 0,
            M['speech_unit_ids'][units[0]] if units else 0,
            M['speech_unit_ids'][units[-1]] if units else 0)
        return self.check(result)

    def show(self, source, c=C):
        self.begin(source, c)
        return self.ack(source, record=self.w.SOURCES[source], c=c)

    def start(self, c=C):
        return self.action('start', 'p14StartCommitments', UNSIGNED, c=c)

    def approvals(self, c=C, order=PEOPLE):
        self.start(c)
        for person in order:
            self.show('approve:' + person, c)
            self.action('pin_card', 'p14PinCard', person, c=c)
        return c

    def finish(self, c=C):
        self.approvals(c)
        self.show('signature', c)
        self.action('pin_signature', 'p14PinSignature', c=c)
        c = replace(c, inventory=c.inventory - {TERMS})
        self.action('give_pencil', 'p14GivePencil', c=c)
        c = replace(c, inventory=c.inventory - {PENCIL})
        for source in ('date', 'readback', 'return_pencil'):
            self.show(source, c)
        self.action('complete_commitments', 'p14CompleteCommitments', c=c)
        return replace(c, inventory=c.inventory | {PENCIL})

    def start_finale(self, urls=()):
        result = self.w.start_finale(urls)
        masks = [0, 0, 0]
        for index, (record, url) in enumerate(ASSET_CREDITS.items()):
            if url in urls:
                masks[index // 15] |= 1 << (index % 15)
        self.v.call('p14StartFinale', *masks)
        return self.check(result)

    def freeze(self, c=C, urls=()):
        c = self.finish(c)
        self.start_finale(urls)
        for source in ('closing:' + self.w.vivian_tone, 'meal', 'tag'):
            c = finale_context(c, source)
            self.show(source, c)
            self.plain('advance_finale', 'p14AdvanceFinale')
        return c

    def ack_freeze(self):
        result = self.w.acknowledge_freeze(self.w.pending_freeze_id)
        self.v.call('p14AcknowledgeFreeze', *divmod(self.w.finale_started_at, 32768), self.epoch)
        return self.check(result)

    def restore(self):
        self.w = P14World.load(decode_words(list(self.v.persistent().values())))
        assert self.v.call('p14AfterRestore') == 1
        self.context = None

    def queries(self):
        before = self.v.persistent()
        assert tuple(R[x] for i in range(len(self.w.journal_records()) + 1)
            if (x := self.v.call('p14JournalAt', i, 0))) == self.w.journal_records()
        assert tuple(U[x] for i in range(len(self.w.journal_units()) + 1)
            if (x := self.v.call('p14JournalAt', i, 1))) == self.w.journal_units()
        assert tuple(SO[x] for i in range(len(self.w.presentations) + 1)
            if (x := self.v.call('p14PendingAt', i))) == tuple(s for s, p in sorted(
                self.w.presentations.items(), key=lambda kv: kv[1].serial) if not self.w._complete(s))
        assert bool(self.v.call('p14Ready')) == self.w.ready
        assert bool(self.v.call('p14PencilWithFrankie')) == self.w.pencil_with_frankie
        assert tuple(O[x] for i in range(9) if (x := self.v.call('p14InventoryAt', i))) == self.w.inventory
        assert {O[x] for i in range(2) if (x := self.v.call('p14ReservedAt', i))} == self.w.reserved_external_objects
        assert self.v.call('p14CurrentSource') == M['sources'].get(self.w.current_finale_source, 0)
        assert tuple(R[x] for i in range(len(self.w.credit_ids) + 1)
            if (x := self.v.call('p14CreditRecord', i))) == tuple(self.w.credit_ids)
        assert ''.join(chr(self.v.call('p14DateHiAt', i) * 32768 +
            self.v.call('p14DateLoAt', i)) for i in range(self.v.p['p14DateLength'])) == self.w.repair_date
        assert PHASES[self.v.p['p14Phase']] == self.w.finale_phase
        assert bool(self.v.call('p14FreezePending')) == bool(self.w.pending_freeze_id)
        assert {p for i, p in enumerate(PEOPLE) if self.v.call('p14Approved', i)} == self.w.approved
        if self.w.start_at:
            assert {enc: f'{enc}:A{self.v.call("p14WinHiAt", i) * 32768 + self.v.call("p14WinLoAt", i)}:KO'
                for i, enc in enumerate(CONTEST_IDS)} == self.w.winning_attempts
        assert before == self.v.persistent()


class DomainTests(unittest.TestCase):
    VM = source_vm.VM

    def h(self, world=None):
        return Harness(self.VM, world)

    def test_every_canonical_task_and_actual_win_gate(self):
        for flag in PREREQUISITES:
            h = self.h()
            h.start(replace(C, flags=C.flags - {flag}))
            self.assertFalse(h.w.start_at)
        for missing in CONTEST_IDS:
            vc = contests(wins=tuple(x for x in CONTEST_IDS if x != missing), losses=(missing,))
            h = self.h()
            c = replace(C, contests=vc, flags=C.flags | {'ALL_VC_WON', missing + '_WON'})
            h.start(c)
            self.assertFalse(h.w.inventory)
        for c in (replace(C, contests=None), replace(C, room=LIVING), replace(C, on_apron=True),
                replace(C, board_room=LIVING), replace(C, repair_date=''),
                replace(C, inventory=C.inventory - {TERMS})):
            h = self.h()
            h.start(c)
            self.assertFalse(h.w.start_at)
        active = copy.deepcopy(C.contests)
        active.enter('VC01', 0)
        h = self.h()
        h.start(replace(C, contests=active))
        self.assertFalse(h.w.start_at)

    def test_exact_first_wins_later_losses_and_other_timeline(self):
        vc = contests(wins=CONTEST_IDS)
        first = {a.encounter_id: a.outcome.id for a in vc.attempts}
        for encounter in CONTEST_IDS:
            play(vc, [False] * 3, encounter)
            leave(vc)
            play(vc, [True] * 3, encounter)
            leave(vc)
        c = replace(C, contests=vc)
        h = self.h()
        h.start(c)
        self.assertEqual(h.w.winning_attempts, first)
        h.project(c)
        self.assertEqual(h.v.call('p14ValidateContext'), 1)
        other = contests(losses=CONTEST_IDS)
        for encounter in CONTEST_IDS:
            play(other, [True] * 3, encounter)
            leave(other)
        wrong = replace(C, contests=other)
        with self.assertRaises(ValueError):
            h.w.validate_context(wrong)
        h.project(wrong)
        self.assertEqual(h.v.call('p14ValidateContext'), 0)
        before = h.v.persistent()
        h.v.call('p14PinCard', 0)
        self.assertEqual(CO[h.v.p['p14Code']], 'invalid_context')
        self.assertEqual(before, h.v.persistent())

    def test_all_eight_approval_receipts_and_wrong_recipients(self):
        h = self.h()
        h.start()
        for i, person in enumerate(PEOPLE):
            h.action('give_card', 'p14GiveCard', person, person)
            self.assertNotIn(person, h.w.approved)
            h.action('pin_card', 'p14PinCard', person)
            h.plain('audio_finished', 'p14AudioFinished')
            self.assertNotIn(person, h.w.approved)
            h.ack('approve:' + person, record='P14.APPROVE.' + person)
            h.action('pin_card', 'p14PinCard', person)
            h.action('pin_card', 'p14PinCard', person)
            h.action('give_card', 'p14GiveCard', PEOPLE[(i + 1) % 8], person)
            self.assertEqual(len(h.w.inventory), 7 - i)
        self.assertEqual(h.w.inventory, ())
        h.queries()

    def test_different_approval_pin_orders_restore_and_unique_ownership(self):
        orders = [PEOPLE[n:] + PEOPLE[:n] for n in range(8)] + [tuple(reversed(PEOPLE))]
        for order in orders:
            h = self.h()
            h.approvals(order=order)
            self.assertEqual(set(h.w.pinned), set(PEOPLE))
            h.restore()
            h.queries()
            h.action('request_signature', 'p14RequestSignature')
        h = self.h()
        h.start()
        for person in PEOPLE:
            h.show('approve:' + person)
        for person in reversed(PEOPLE):
            h.action('pin_card', 'p14PinCard', person)
        h.queries()

    def test_signature_requires_whole_five_unit_consent_with_stale_restore(self):
        base, c = approve14()
        for prefix in range(6):
            h = self.h(P14World.load(base.save()))
            h.action('request_signature', 'p14RequestSignature', 'forge', c=c)
            h.action('request_signature', 'p14RequestSignature', 'coerce', c=c)
            h.action('request_signature', 'p14RequestSignature', c=c)
            tokens = h.w._tokens('signature')
            if prefix:
                h.ack('signature', units=tokens[:prefix], c=c)
            p = h.w.presentations['signature']
            epoch = h.epoch
            h.restore()
            h.project(c)
            before = h.v.persistent()
            h.v.call('p14Acknowledge', M['sources']['signature'], *divmod(p.serial, 32768),
                epoch, M['line_ids']['P14.DIALOGUE.003'], 0, 0)
            self.assertEqual(CO[h.v.p['p14Code']], 'stale_presentation')
            self.assertEqual(before, h.v.persistent())
            if prefix < 5:
                h.action('pin_signature', 'p14PinSignature', c=c)
                h.resume('signature', c)
                h.ack('signature', units=tokens[prefix:], c=c)
            h.action('pin_signature', 'p14PinSignature', c=c)
            self.assertEqual(h.w.reserved_external_objects, {TERMS})
            h.project(c)
            self.assertEqual(h.v.call('p14ValidateContext'), 0)
            c2 = replace(c, inventory=c.inventory - {TERMS})
            h.project(c2)
            self.assertEqual(h.v.call('p14ValidateContext'), 1)
            h.queries()

    def test_pencil_date_readback_return_and_completion_before_finale(self):
        h = self.h()
        h.start()
        h.action('give_pencil', 'p14GivePencil')
        h.action('pin_signature', 'p14PinSignature')
        h.action('complete_commitments', 'p14CompleteCommitments')
        h.approvals()
        h.show('signature')
        h.action('pin_signature', 'p14PinSignature')
        c = replace(C, inventory=C.inventory - {TERMS})
        h.action('give_pencil', 'p14GivePencil', c=replace(c, inventory=frozenset()))
        h.action('give_pencil', 'p14GivePencil', c=actors(c, frankie=LIVING))
        h.action('give_pencil', 'p14GivePencil', c=c)
        self.assertTrue(h.w.pencil_with_frankie)
        h.project(c)
        self.assertEqual(h.v.call('p14ValidateContext'), 0)
        c = replace(c, inventory=c.inventory - {PENCIL})
        h.begin('readback', c)
        h.begin('return_pencil', c)
        for source in ('date', 'readback', 'return_pencil'):
            h.begin(source, c)
            h.plain('audio_finished', 'p14AudioFinished')
            h.action('complete_commitments', 'p14CompleteCommitments', c=c)
            self.assertFalse(h.w.ready)
            h.ack(source, record=h.w.SOURCES[source], c=c)
            h.restore()
        h.action('complete_commitments', 'p14CompleteCommitments', c=actors(c, frankie=LIVING))
        h.action('complete_commitments', 'p14CompleteCommitments', c=c)
        self.assertEqual(h.w.flags, {'COMMITMENTS_SIGNED', 'GAME_COMPLETE'})
        self.assertEqual(h.w.finale_phase, 'not_started')
        self.assertEqual(h.w.dynamic_bindings, {'repair_date': C.repair_date})
        h.action('complete_commitments', 'p14CompleteCommitments', c=c)
        h.project(replace(c, inventory={PENCIL} | c.inventory))
        self.assertEqual(h.v.call('p14ValidateContext'), 1)
        h.queries()

    def test_all_closing_tones_and_all_canonical_credits_require_text(self):
        for tone in TONES:
            h = self.h()
            c = h.finish(replace(C, vivian_tone=tone))
            h.start_finale()
            self.assertEqual(h.w.current_finale_source, 'closing:' + tone)
            h.show('closing:' + tone, c)
            h.queries()
        h = self.h()
        c = h.freeze(urls=tuple(ASSET_CREDITS.values()))
        h.plain('advance_finale', 'p14AdvanceFinale')
        h.plain('claim_celebration', 'p14ClaimCelebration')
        h.ack_freeze()
        h.plain('advance_finale', 'p14AdvanceFinale')
        self.assertEqual(h.w.credit_ids, [*CREDIT_ORDER, *ASSET_CREDITS])
        for record in h.w.credit_ids:
            self.assertEqual(h.w.current_finale_source, 'credit:' + record)
            h.plain('advance_finale', 'p14AdvanceFinale')
            h.show('credit:' + record, c)
            h.restore()
            h.plain('advance_finale', 'p14AdvanceFinale')
        self.assertEqual(h.w.finale_phase, 'finished')
        h.queries()

    def test_quiet_meal_tag_receipts_freeze_and_effects_exactly_once(self):
        h = self.h()
        c = h.finish()
        h.start_finale()
        h.plain('claim_tag_laugh', 'p14ClaimTagLaugh')
        h.show('closing:professional', c)
        h.plain('advance_finale', 'p14AdvanceFinale')
        for index, token in enumerate(h.w._tokens('meal')):
            h.begin('meal', c)
            h.ack('meal', units=(token,), c=c)
            h.plain('claim_tag_laugh', 'p14ClaimTagLaugh')
            self.assertFalse(h.w.laugh_at)
        h.plain('advance_finale', 'p14AdvanceFinale')
        c = finale_context(c, 'tag')
        h.begin('tag', c)
        h.ack('tag', units=h.w._tokens('tag')[:1], c=c)
        h.plain('claim_tag_laugh', 'p14ClaimTagLaugh')
        h.ack('tag', units=h.w._tokens('tag')[1:], c=c)
        h.plain('claim_tag_laugh', 'p14ClaimTagLaugh')
        self.assertTrue(h.w.laugh_at)
        h.plain('advance_finale', 'p14AdvanceFinale')
        epoch = h.epoch
        h.restore()
        h.project(c)
        before = h.v.persistent()
        h.v.call('p14AcknowledgeFreeze', *divmod(h.w.finale_started_at, 32768), epoch)
        self.assertEqual(CO[h.v.p['p14Code']], 'stale_freeze')
        self.assertEqual(before, h.v.persistent())
        h.ack_freeze()
        h.plain('claim_celebration', 'p14ClaimCelebration')
        h.restore()
        h.plain('claim_celebration', 'p14ClaimCelebration')
        h.plain('claim_tag_laugh', 'p14ClaimTagLaugh')
        h.queries()

    def test_pause_restore_resume_and_skip_every_finale_phase(self):
        w, c = finish14()
        w.start_finale()
        states = [(w.save(), c)]
        for source in ('closing:professional', 'meal', 'tag'):
            c = finale_context(c, source)
            w.begin_presentation(c, source)
            w.acknowledge_presentation(c, w._handle(source), record_id=w.SOURCES[source])
            w.advance_finale()
            states.append((w.save(), c))
        w.acknowledge_freeze(w.pending_freeze_id)
        w.advance_finale()
        states.append((w.save(), c))
        for save, c in states:
            h = self.h(P14World.load(save))
            h.project(c)
            h.plain('pause_finale', 'p14PauseFinale', True)
            h.restore()
            h.action('present_finale', 'p14PresentFinale', c=c)
            h.plain('advance_finale', 'p14AdvanceFinale')
            h.plain('claim_celebration', 'p14ClaimCelebration')
            h.plain('claim_tag_laugh', 'p14ClaimTagLaugh')
            h.plain('pause_finale', 'p14PauseFinale', False)
            h.plain('pause_finale', 'p14PauseFinale', True)
            h.plain('skip_finale', 'p14SkipFinale')
            self.assertTrue(h.w.ready)
            self.assertFalse(h.w.finale_paused)
            self.assertEqual(h.w.finale_phase, 'finished')
            h.plain('skip_finale', 'p14SkipFinale')
            h.queries()

    def test_dispatch_hints_and_invalid_signed_word_arguments(self):
        h = self.h()
        h.start()
        for verb, obj in itertools.product(Verb, ('unknown', TERMS, PENCIL, CARD_IDS['bunny'])):
            h.action('dispatch', 'p14Act', verb, obj)
        h.action('dispatch', 'p14Act', Verb.GIVE, CARD_IDS['bunny'], 'bunny')
        h.ack('approve:bunny', record='P14.APPROVE.bunny')
        h.action('dispatch', 'p14Act', Verb.USE, CARD_IDS['bunny'], 'pledge_board')
        for level in (1, 2, 3):
            h.action('hint', 'p14Hint', level, c=replace(C, room=LIVING))
        for value in (True, '1', 1.0, 32768, -32769):
            with self.assertRaises(ValueError):
                h.v.call('p14Hint', value)
        for value in (-1, 0, 4, 32767):
            h.v.call('p14Hint', value)
            self.assertEqual(CO[h.v.p['p14Code']], 'invalid_argument')
        h.queries()

    def test_record_and_unit_mapping_keeps_exact_quiet_canonical_line(self):
        fixture = json.loads((ROOT / 'tests/fixtures/p14/canonical-bindings.json').read_text())
        unit = next(u for u in fixture['speech_units'] if u['line_id'] == 'P14.ENDING.002.02')
        self.assertEqual(unit['speaker_id'], 'jack')
        self.assertEqual(unit['text'], 'Put “It’s a meal” underneath. In very large letters.')
        self.assertEqual(RECORD_UNITS, {r['id']: tuple(u['line_id'] for u in fixture['speech_units']
            if u['record_id'] == r['id']) for r in fixture['records']})
        self.assertEqual(UNIT_SPEAKERS, {u['line_id']: u['speaker_id'] for u in fixture['speech_units']})
        self.assertEqual(set(M['sources']), set(P14World.SOURCES))


class BytecodeTests(DomainTests):
    VM = ByteVM


if __name__ == '__main__':
    unittest.main()
