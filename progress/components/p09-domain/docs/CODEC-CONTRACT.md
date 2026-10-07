# P09 numeric codec and representability contract

This codec is a **new reconstruction**, authored against the retained domain
metadata and the unchanged Python reference model. It is not recovered
historical adapter source, and passing its tests does not establish native
playability, rendering, sound, or stock-ScummVM acceptance.

## Authority and files

- `codec/p09_codec.py` is the new typed boundary implementation.
- `reference/cakood/p09_model.py` is imported unchanged. Its `validate` and
  `validate_context` methods are the causal authority for world saves.
- `historical/manifest.json` supplies retained P09 property names, serial slots,
  room/source/line/unit/event/code IDs, capacity limits, and the unsigned card
  handoff. Its historical **external campaign object IDs are not used**.
- `schema.json["objects"]` supplies the current, unique external object map for
  context inventory. An explicitly supplied `object_ids` map can replace this
  input for tests or a host with an already validated current registry.
- All resource lookup is relative to this deliverable root. No recovery-machine
  absolute path is embedded in the codec.

## Persisted world: 77 properties

`encode_world(world, context=None)` returns a fresh `dict[str, int]` containing
exactly the 77 retained persisted property names in retained order.
`decode_world(properties, context=None)` returns a fresh unchanged-reference
`P09World`. Both reject invalid causal state and never mutate their inputs.

Five scalar properties encode initialized status, rumor-cleared status,
card-ready status, the restricted accusation variant, and hint level. The
remaining 72 properties encode 36 serial slots: revision, three one-shot
serials, nine presentation starts, and 23 receipt serials. Each serial is
`high * 32768 + low`; each limb is in `0..32767`. `0` means no start, one-shot,
or receipt in an optional slot. Revision may be zero. The maximum serial is
`1073741823`. No value is truncated, wrapped, clamped, or coerced. Python
booleans, floats, strings, negative values, and oversized limbs are rejected.

`p09Initialized` must equal 1 for a model save. Zero-filled SCI construction
storage must be initialized by its owner before decoding. `p09Restricted = 1`
means exactly the `stringer_only` accusation variant; it requires an accusation
presentation and cannot carry Rita's second receipt. With `p09Restricted = 0`,
an accusation may still have only its first receipt while waiting for Rita.

The unchanged model enforces, among other rules:

- Receipts are an ordered contiguous prefix, strictly after their own start
- Starts are unique and cannot collide with receipt serials
- Unrelated presentations cannot acknowledge at the same serial
- The rumor one-shot is exactly the earliest first receipt among rumor sources
- Terms start after the rumor correction; card readiness and the terms one-shot
  match the fifth terms receipt
- The success caption is separately acknowledged after the card grant
- Shared wish starts after acknowledged class context, and its one-shot matches
  its final unit
- Reading the card starts after its physical grant
- Intro cannot be newly queued after the rumor correction
- Flags and one-shots match receipts, and revision covers committed actions

This is exact validation of the reference model's saved-state contract, not a
claim of exhaustive historical reachability. For example, the reference allows
revision gaps and arbitrary nonnegative revision values; the codec adds the
finite upper bound without inventing stricter history requirements.

The finite model subset is all worlds accepted by `P09World.validate()` whose
serials fit the retained 30-bit envelope. An optional context adds exactly
`world.validate_context(context)`: P08 evening handoff, agreed plan when terms
exist, and no campaign claim of an unearned P09 flag. Context may be offscreen or
on the apron during save/load. World conversion does not require its external
inventory to be representable, because inventory is not stored in the world.

For accepted worlds, `decode_world(encode_world(world)).save() == world.save()`.
For accepted property images, encoding the decoded world reproduces every one
of the 77 properties exactly. These conversions preserve receipts, notebook
records/units, pending sources, restricted variants, and callback identity.

`decode_world` rejects an unfiltered 98-property runtime dictionary. To make
the boundary explicit, use `decode_world(select_persisted(runtime_properties))`.
The selector requires the exact 98-field shape and finite integer limbs but
does not claim to validate transient context or result semantics. Decode those
images separately when needed.

Overflow raises `CodecError`, a `ValueError` subclass. A caller handling actions
must preflight or restore its own candidate state on overflow; this pure codec
does not roll back mutations previously performed by a caller. SCI should
return `serial_exhausted` and leave its persistent state unchanged when a new
action cannot obtain a serial. Reads, repeats, and no-op acknowledgments need
no new serial.

## Campaign context: 12 properties plus 400 inventory bits

`encode_context(context, epoch=1, object_ids=None)` returns `ContextImage`:

- `.properties` contains the eleven context status/fact fields and `p09Epoch`
- `.held` is a 400-element tuple of exact integer 0/1 bits indexed by current
  object ID; index 0 and unmapped IDs must remain zero
- `.arguments` is the eleven positional arguments expected by `p09Context`:
  room, apron, evening, plan, Stringer room, Rita room, view, contest,
  rumor claim, ready claim, epoch

Front view is 0, side view is 1. Epoch is an explicit positive transient integer
in `1..32767`; it is not a saved P09-world serial and is not present in
`P09Context`. `decode_context(image)` reconstructs the exact reference context;
the caller retains the epoch in `image.properties` for callback leasing.

The finite context subset uses the seven retained rooms, exact booleans, and
only the four flags `EVENING_STARTED`, `PLAN_AGREED`, `RUMOR_CLEARED`, and
`TERMS_CARD_AVAILABLE`. Every external inventory object must have a unique
current ID in `1..399`. The reference's exclusions still apply: fixed P09
objects and the branch-owned card cannot be supplied as external inventory.
Unknown IDs, duplicate numeric mappings, foreign flags, and unknown object
names are rejected. Nothing is silently discarded or renamed. In particular,
the old test-only `sample_tiles` name is not silently turned into a different
registered object. A campaign that has unrelated flags must explicitly build
its own P09 projection before invoking this exact codec.

## Transient results and events

`encode_result(result, revision=None)` returns `ResultImage` with nine result
properties and fixed arrays: 8 line IDs, 6 speech-unit IDs, 3 event IDs, and 9
event arguments. Each event receives three consecutive argument slots. Counts
describe used slots, and every unused slot must be zero. Text must be empty;
the codec transports canonical IDs, never replacement player prose.

Pass `revision=world.revision` for query results and for comparison with native
transient storage. If omitted, revision is inferred from the first event, or is
zero for an eventless result. All events in one result must have the same
positive serial, held in `p09ResultHi/Lo`. The reference result has no separate
revision field; decoding returns the result, while the image retains that
transient serial. Re-encoding an eventless decoded image with its stored
revision preserves the image exactly.

`presentation_id` is absent or has exact canonical form
`P09:<source>:<positive decimal serial>`. Source and serial must appear together
in native storage. No padded, signed, overflowing, or foreign callback ID is
accepted. World/context validity at callback time remains the adapter's job.

`encode_event(event)` and `decode_event(EventImage(...))` use the retained
three-argument interface, with inclusive **zero-based source-token indices**:

| Event | Argument 1 | Argument 2 | Argument 3 |
|---|---|---|---|
| P09_PRESENTATION_QUEUED | source ID | 0 | 0 |
| P09_PRESENTED | source ID | first newly presented index | last newly presented index |
| P09_RUMOR | rumor source ID | 0 | 0 |
| P09_TERMS | card object 399 | 0 | 0 |
| P09_SHARED_WISH | optional marker 1 | 0 | 0 |
| P09_HINT | hint level 1..3 | 0 | 0 |

Payloads are reconstructed and compared with exact field/value types. Extra
payload data, unknown event kinds, noncontiguous receipts, list-for-tuple
substitution, mixed serials, and a receipt crossing the terms/grant barrier are
rejected. Event conversion does not replace full world causal validation.

The card event always means object `renewal_repair_card`, location `inventory`,
`signed = False`, no repair date, signature owner `P14`, and terms record
`P09.READ.002`. There is no property or event argument permitting P09 to sign,
consume, date, or assign the card, approve a future promise, or complete the
game. A forged signed or otherwise changed handoff is rejected during encoding.

## Executable verification

From the deliverable root:

```sh
python -m unittest discover -s tests -p test_codec.py -v
```

The codec suite currently has 21 tests. It checks all 24 rumor-route orderings,
each partial terms prefix, interleaved earliest rumor receipts, full versus
restricted partial accusation, notebook and pending-caption behavior, all six
event types, exact argument indices, card invariants, context ownership and
finite mappings, malformed/causally invalid saves, fixed-array padding, and
zero/limb/max/overflow boundaries. The reference model and earlier inputs are
left unchanged.
