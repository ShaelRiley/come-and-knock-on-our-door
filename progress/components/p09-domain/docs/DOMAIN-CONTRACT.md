# New P09 SCI domain boundary

The complete domain body and generator are new implementation. The five exact
historical methods are reused as a visibly separate trailing source block:
`p09ValidateContext`, `p09Topics`, `p09Begin`, `p09Resume`, and `p09Acknowledge`.
Their method signatures, body bytes, sources, receipt indices and result codes
agree with the unchanged model and retained manifest. New supporting methods
implement finite storage, causal validation, pure observations and host leases.

## Current versus historical allocations

Only P09's own object numbers 395–399 are imported as stable branch identities.
Current P05 external IDs come from accepted module985 definitions, with PA kit
63. P06 uses host IDs 73–85; P07 uses 86–94. The historical wider map assigned
different meanings to several of those numbers. `schema.json` contains current
mapping provenance, and retains old build/source/registry hash fields only under
`historical_unverified_build_pins`. Those old pins do not describe this output.
The retained P08 116–123 reservation is explicitly proposed, not an activated
allocation. A later host must validate its actual external object map and
produce the bounded context projection. Arbitrary foreign flags and unknown
inventory objects require that explicit projection; the typed codec does not
silently discard them.

## Persisted and transient storage

SCI owns exactly the 77 model properties described in CODEC-CONTRACT.md.
Every ordinary save image accepted by the codec is checked by the unchanged
model; the SCI validator independently checks the same finite causal rules.
Save mutation uses `p09LoadBegin`, all 77 indexed `p09LoadWord` calls and then
`p09LoadCommit`. Validation occurs before adoption; failure restores every old
persisted word. Either result discards context, leases and outgoing output.
Incomplete staging contains -1 words and is rejected. All 98 runtime properties
are retained for metadata comparison, but only the selected 77 belong in a save.

No save method accepts signature, repair date, duplicate card count or a P14
completion flag. The card is derived from the exact fifth terms receipt and
one-shot stamp. Its success line is a sixth, separately resumable receipt.

## Presentation callbacks and finite epochs

`p09Context` accepts the historical eleven arguments and a fresh epoch in
1..32767. Each accepted context epoch must be greater than the previous value
in the active object. It clears every old lease. `p09Begin` and `p09Resume` arm
only the specified source at that epoch. Acknowledgment must match the source,
two-limb start serial, epoch and lease, then the next canonical contiguous
receipt prefix. A single receipt cannot cross the terms/grant/success barrier.
`p09Invalidate` cancels every lease; `p09AfterRestore` cancels them and validates
the restored state. No audio-end or queue callback enters this acknowledgment
path. Successful visible captions are the host's receipt-certification duty.

The host epoch issuer is intentionally external and is **not a restored P09
property**. A later native host must own a non-rewinding epoch sequence across
cancel, navigation and native restore, reproject after restore, and never reuse
an old epoch. Merely restoring an object then incrementing its restored epoch
would not meet this contract. At epoch exhaustion the host must cancel all
outstanding callbacks and establish a new session before continuing; this
domain rejects reuse and nonpositive/signed-overflow epochs. Ordinary component
load preserves the active object's epoch and clears leases. Native engine save
restoration and host-wide epoch issuance remain integration gates.

The model serial envelope is 0..1073741823. Every mutating action preflights a
new serial before writing state. Exhaustion returns `serial_exhausted`; it does
not wrap. Idempotent acknowledgment and reads may still succeed. No histories
outside this finite SCI envelope are silently treated as equivalent.

## Observations and state ownership

Look, topics, location, reachability and journal/pending queries are pure with
respect to the persisted model. Journal records require the complete canonical
record; journal units preserve acknowledged source chronology and deduplicate
the same unit across routes. A first partial Stringer correction clears rumor
without inventing Rita's class explanation. Only all five terms units grant
the unsigned card atomically. Side/front are viewpoints in the same L07 room.

The P08 evening handoff and agreed plan are external context. Their dedicated
admission validator catches inconsistent saves/host projections; ordinary
actions retain the reference's specific evening, plan, actor and view barriers.
The domain owns only RUMOR_CLEARED and TERMS_CARD_AVAILABLE, never contest wins.

## Verification limits

Source/emitted checks execute identical calls on the readable source evaluator
and actual freshly compiled SCI bytecode, then compare every property, local
array, return value and decoded model result. The accepted evaluators are copied
without changes. Boolean-valued helper operands are explicitly normalized for
the pinned compiler. These are bounded deterministic component proofs, not a
replacement engine, screen presentation, audible playback or ScummVM acceptance.
Independent review and live host/native integration remain separate gates.
