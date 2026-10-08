# New P07 design and host contract

Every implementation choice in this document is a new reconstruction unless PROVENANCE.md identifies a literal witness. None is a claim to have recovered the missing Python or SCI implementation.

## Public shape

`P07World` owns one bounded P07 timeline. `P07Context` is frozen and strictly typed: exact campaign room strings, real Boolean set/apron modes, frozen string sets for flags/inventory, actual Bunny room/apron/elsewhere-invitation facts, and a tuple of immutable pot ownership claims. Mutable sets/lists, booleans masquerading as numeric choices, unknown rooms, contradictory P07 flags and pocket copies of kitchen fixtures fail closed.

The public action choices are typed `Action`, `Measure`, `Source` and `Signal` enums. `perform(context, action, measure=..., host=...)` handles logical player actions; `use_stove` is the convenience toggle for cook then off. `look`, `label`, `hint`, `measure_choices`, `projection`, `flags`, `state`, `save` and `validate` are read-only queries. `state`, canonical records, canonical units and save envelopes are full detached copies. Result/projection structures and their nested collections are immutable.

Other entry points are:

- `open_source(context, source)`: present or resume an exact source request
- `acknowledge_source_page(context, token, page)`: trusted host receipt only after actual complete display
- `cancel_source(token, context=...)`: cancel the uncommitted reader; its exact token is required
- `presentation_signal(signal, token=None)`: always presentation-only, with no progress or reward
- `load`, `from_json`, `restore`, `to_json`: strict persistence and exact timeline replacement
- `handoff_to_p13(context, request, host=...)`: bounded synchronous host transfer of the existing completed pot

Passing no transaction host runs the isolated reference state machine. Native integration must use an equivalent atomic host boundary; returning a successful result from the standalone model is not proof that a native object or renderer changed.

## Finite cooking contract

P02 is represented by the external PLAN_AGREED flag. Physical preparation and source reads require it. Pure inspections do not create progress. A progressed save cannot be composed with a pre-P02 context. The host owns campaign phase and actual room movement.

The cooking chain has receipts for base, correct measure, stock, vegetables, cooked, heat off, herbs and complete:

1. Base can be added before or after measuring/pouring stock
2. Vegetables require base, but do not require stock already in the pot
3. Selecting the correct eight-bowl measure requires the actual complete recipe source receipt
4. Pouring stock requires that measured jug. It cannot add a second measure
5. Cook requires base, measured stock and vegetables, and immediately produces the cooked, heat-on state
6. Turn heat off follows cooking. No timer or audio/animation callback is involved
7. Add herbs requires cooked food with heat off
8. Close lid commits FOOD_READY once and emits exact P07.SUCCESS.008 and P07.SUCCESS.009

The six-supper selection is a rejected attempt with canonical feedback and no state or ingredient loss. Herbs over active heat similarly leave the sachet and all physical state unchanged. Wrong order, repeat actions and forgotten-lid feedback are non-destructive. Undefined early failures return text-free machine codes rather than newly invented dialogue.

Pantry supplies are refillable throughout preparation. Each pot component is recorded once. `REFILL_PANTRY` is an idempotent availability check, not a resource multiplier. After completion the batch is closed: no new ingredient, relighting, second pot, pocket reward, or reopened cooking chain is possible. The empty jug and label-bearing containers remain inspectable world props. The model has no burning, spoilage, hunger, illness, toxic combination or allergy states.

The read-only physical projection has one P07 pot until transfer, a correctly placed lid, exact contents, heat/lid state, pantry availability, and no pocket items. Eight tasting bowls including Jackie are available only for the completed batch. It never projects eight full suppers. The pot waits at the L02 kitchen station until the real P13 interface releases it.

## Exact source and page causality

The three observed sources are recipe, jug mark and herb label. They bind only to P07.READ.001, P07.READ.002 and P07.READ.003 respectively. A LOOK paraphrase, label, hint, source availability, queued output, speech end or skipped audio cannot establish observation.

Only the actual recipe annotation is a required puzzle knowledge gate. The two optional observations are tracked exactly but are not additional mandatory reading steps. KNOW_EIGHT_PORTIONS is derived from the complete recipe receipt in the P02-enabled context, not from hearing an equivalent sentence in a hint.

Each source's entire canonical text fits one logical 48-column, 14-row reader page. The new source-page descriptor stores the exact record ID, source ID, zero-based page index, page count, full literal text, and SHA-256. Page identity is not an invented native resource number. The host must show all of that actual text before acknowledging it. A heading, truncated body, different source, guessed page count or stale token is rejected. A muted or audio-skipped page that really was fully displayed can be acknowledged immediately; sound is never the gate.

A source request gets its own unsigned receipt. The one complete page acknowledgment is the next serial and is saved with its exact source/page digest and source request pointer. Independent primary commits cannot alias either serial. Partial, extra, duplicate, contradictory, orphaned and reordered page receipts are rejected on load. The optional sources can be read in any order and after completion.

A pending reader occupies one bounded slot and reserves a serial for completion or cancellation. Reopening it resumes the same logical request. Replacing it invalidates the old token. Other mutating player actions refuse while it is pending; cancel returns control without consuming ingredients or learning. Read-only observations do not themselves dismiss an active reader. The presentation host must explicitly cancel a reader when replacing/dismissing its displayed page before acknowledgment.

`cancel_source` can accept the exact host callback token without a player context because it only cancels a reader and cannot move anything, learn a fact or grant a reward. Supplying a host for atomic publication should also supply the actual current context. No fabricated context is used to authorize a physical action.

Source receipts are trusted host testimony about real display. A Python reference cannot prove that pixels were shown or a player understood them. Native exact-page capture and lifecycle proof remain required. The unkeyed save checksum detects corruption; it is not cryptographic proof against a party that rewrites a coherent whole history and recomputes its hash.

## Optional cast beats and output slices

The introduction and onion misunderstanding require Bunny actually in the kitchen on the same set side, with no outstanding invitation elsewhere. The context explicitly represents that P05 conflict; P07 never moves or summons her. If Bunny is absent, cooking remains completable without any introduction, comic beat or sincerity flag.

P07.SCENE.002 is routed in two exact canonical unit slices:

- Comic misunderstanding: units .01, .02 and .03
- Optional sincere follow-up: units .04 and .05

The logical onion receipt consumes LAF07 once, anchored after .02 (the comic misread), never after sincerity. The sincere receipt is separate and cannot appear without the prior misunderstanding. Declining or never reaching the follow-up leaves it honestly unset and does not block food. The follow-up can still occur after food completion if Bunny is genuinely present.

`P07Result.record_ids` identifies the source records; `speech_unit_ids` defines the exact slice to present. The host must honor that slice instead of expanding a scene record to its entire dialogue. `render_exact` demonstrates this rule and rejects a structured scene lacking explicit units. All text is looked up from the retained catalog; `result.text` stays empty. Every record and unit has a tested route. Editorial laugh opportunities do not become new runtime awards or correctness gates.

The logical LAF07 event may be dropped/muted by the audio system. It must not be replayed on save/load, repeated failures, a quiet repeat, or over the sincere units. Audio callbacks cannot change the onion, sincere, recipe, cooking or completion receipts.

## Atomic candidate and physical publication

Every mutating call builds and validates a detached state candidate. Failure leaves the original model unchanged. With a transaction host:

1. Form the exact before/after save snapshots, physical projections and canonical output before mutation
2. Enter the world lock and no-reentrant-input/no-save critical section
3. Host `prepare` verifies original object ownership, every destination, exact output resolution/capacity and transaction identity without publishing anything
4. Host `commit` atomically publishes both prepared physical state and exact output, or raises with both unchanged
5. The world performs only the already-validated state assignment after successful host commit

No validation, callback, event dispatch, save or I/O occurs between host commit and model assignment. Concurrent inputs serialize under a reentrant lock; reentrant operations during host publication are rejected explicitly. The host fixture uses compare-and-swap against its before snapshot, preventing two independently copied worlds from both committing to one host.

The in-memory host retains only the latest output batch. It is a protocol fixture, not a native UI queue or actual full-source display. Its failure knobs prove preparation, capacity and commit failures leave model, ownership and output intact; retry is safe. A native host that can partially mutate and then fail must add a real rollback/transaction mechanism before using this contract.

## P13 ownership boundary

`P13Handoff` is a bounded trusted input naming the existing hotpot, the stable transfer ID P13:OWN:hotpot_pot, a bounded P13-owned delivery serial, the kitchen hatch route and L05 courtyard destination. This value is a declarative transfer description, not an authorization capability. Its numeric serial is a logical external receipt, not callback freshness evidence. The same description can be reused against another independently restored reference world when a newly constructed synchronous host owns that restored pot; accepting it does not prove that an old callback is fresh. This interface is synchronous host-only and must not be used as a delayed callback without a separate current-session/current-lease dispatch check owned by the host. P13Handoff itself has no such capability binding. No P13 request freshness guarantee is claimed by this packet.

The caller is the real P13 owner, which must have established its actual seating, helper consent, buffet, route and delivery conditions. P07 additionally checks FOOD_READY, the later INTRODUCTION_CLEAR campaign fact, actual kitchen/Bunny presence, no apron, and original pot ownership. It then atomically releases the same pot and lid to P13. It does not allocate a replacement, move another object, award SERVED, or fabricate P13 dialogue/behavior. The real P13 implementation still owns confirmation of SERVE and the rest of its sequence.

After transfer, the P07 projection omits the pot, lid and their contents entirely, while its historical FOOD_READY remains true and pantry reopening remains forbidden. Current owner context must agree with the saved handoff. Mixing a pre-transfer P07 save with a post-transfer P13 owner map is rejected. The fixture can restore the complete owner/domain snapshot together, with no presentation or grant replay.

## Unsigned serials, strict saves and reachability

Receipts use 0 for absence and 1…0xffffffff for committed events. JSON stores exact unsigned integers; `split_serial`/`join_serial` define the future portable high/low unsigned-16 mapping. The low limb rolls over without wrapping the total serial. Full exhaustion fails without success output, mutation or ingredient consumption. A pending source reserves its single completion/cancellation serial, so the last representable serial cannot strand it.

Save schema `cakood-p07-reconstruction`, version 1, is intentionally incompatible with unproved older binary formats. The envelope pins canonical input identity and an integrity digest. Exact keys, exact scalar/container types, bounds, receipt uniqueness, source/page identity, branch prerequisites, physical ordering, optional-beat causality and handoff ownership are all validated. There are no independently loadable FOOD_READY or knowledge Booleans to repair.

Observed page acknowledgment immediately follows its retained request because a pending reader blocks other mutations. Revision 2 validates the exact source identities still unread at each point in the ordered retained history, including every source request, complete-page receipt, physical receipt and final pending reader.

An omitted serial can only be an unretained source opening, replacement or cancellation. It cannot be an omitted learning event, because observed sources are permanent. Between retained commits, the possible reader states form a complete graph without self-loops: no reader plus each still-unread source. Reopening the same pending source does not consume a serial. Reading a known source with no pending reader does not consume one either.

- With no unread sources, no omitted serial is possible
- With one unread source, omitted steps alternate exactly between no reader and that identity; parity matters
- With two or three unread sources, a single step reaches every other reader state, and any gap of at least two steps can reach every state

At a retained physical receipt the reader must be absent. At a retained request the source must still be unread and differ from any existing pending reader. At its complete-page receipt that exact source must be pending; it becomes learned and the reader clears. The final possible reader must match the saved reader exactly. This closed-form graph walk validates the whole unsigned 32-bit serial range without iterating over enormous gaps.

The independent reviewer’s complete chronology oracle covers 8,442 layouts through revision 10, including three source identities, a possible pending reader and a physical base receipt. Revision 2 matches all 4,278 reachable and 4,164 unreachable layouts with zero mismatches. It rejects all 1,236 impossible layouts the original gap-length-only rule accepted. Every valid read/replacement/cancellation order in that complete bounded oracle remains accepted.

`from_json` rejects duplicate keys, NaN/infinities, excessive size, malformed deep nesting, wrong schemas and extra/missing state fields. Invalid restore validates first and preserves the existing state, lease and live token. Valid restore replaces the exact saved timeline; it never merges later progress, repairs a missing prerequisite or replays a grant.

## Freshness is an outside-VM obligation

Each world has a runtime-only session and an explicit `HostLease`. Source tokens bind source/request/session/lease. New instances and restored instances issue different tokens even when their saved counters match. Tokens and leases are never serialized.

`restore` retires the old lease before adopting the fully validated replacement. Worlds sharing that old lease become unusable. Tests also model the host retiring a lease before discarding an old VM and loading its replacement under a new lease.

This is not proof of whole-VM freshness by itself. A native save that rewinds the VM could also rewind in-VM nonce/counter state. The actual host must own lease retirement outside the restored VM or equivalently discard the old dispatcher and all callbacks before accepting calls into the replacement. It must do this at a safe transaction boundary. No saved counter, receipt, Python nonce or P13 serial is claimed to solve that external problem.

## Next implementation gates

- Reconstruct SCI domain988 separately and prove parity with these exact transitions and corpus
- Explicitly materialize 0/1 at the witnessed SCI Boolean consumers; do not reuse raw operand-valued `and`/`or` results in comparisons or counts
- Allocate native objects/selectors only through the parent integration inventory
- Bind real exact-page rendering, host queue capacity and atomic object/output publication
- Save campaign actor positions, P05 invitation state, owner map and domain timeline coherently
- Prove outside-VM callback retirement and stock ScummVM save/load behavior
- Implement and prove the actual P13 host conditions, single-pot delivery and SERVE confirmation

None of those native gates is passed by this reference packet.
