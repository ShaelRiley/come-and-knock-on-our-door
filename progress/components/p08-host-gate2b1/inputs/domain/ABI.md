# P08 SCI ABI revision 2

Script 989 exports instance `p08State` at export 0, class `P08State`, species 11.
It has no superclass, kernels, external sends, Main hooks, native objects, static
text banks, audio modules, or art resources. New selectors occupy only the
coordinator's 2600–2799 reservation. `selectors.json` preserves every name/ID in
the captured current P07 host selector vocabulary. Host selectors 2800–2999 are
not used. Existing species 0–10 remain owned by their original scripts.

## Editable state

The generated manifest is the complete exact offset/width authority. There are
88 saved words. Five positions begin at UNPLACED=0; the only destination choices
are HATCH=1, WALL=2, ALCOVE=3, LANE=4. PA facing is independently INWARD=1 or
NEIGHBOR=2. Padding is NONE=0, original clean towel=1, original clean napkin=2.
There is no inventory furniture and no full-screen pre-placement from P06's
miniature. Start phases are NONE=0, CHECKLIST=1, CONFIRMATION=2, AUTOSAVE=3.

Each serial is an unsigned32 number carried as two signed16 bit-pattern words,
high then low. Values 0x8000–0xffff appear as negative SCI words. Comparisons use
explicit unsigned-limb ordering, never a signed whole-serial comparison. Zero is
an absent receipt. Overflow at 0xffffffff returns `serial_exhausted` without a
candidate or live-state change; no serial wraps. This finite limit is a new SCI
representation bound, not a claim that the unbounded Python model had it.

Saved receipts cover revision, request counter, pending and completed request,
checklist and explicit confirmation, four observed sources, all five last
placements plus PA facing, three one-shots, original five owner transfers and
ACKs, and both original unpacking-surface receipts. Source membership is exactly
nonzero source receipts. Flags are two explicit words checked against physical
readiness and the evening one-shot. R2 explicitly stores the complete ownership-ledger key sequence, including
already ACKed claims. Its count is saved at word 82 and its five key slots at
83–87. Valid keys are carrier=1, PA=2, screen=3, credit=5, padding=22. The
sequence is a duplicate-free permutation of exactly the nonzero owner claims;
unused tail words are zero. Pending handoffs filter this saved sequence without
reordering it. On typed JSON restore, incoming ownership dictionary order is
encoded exactly, including sorted or otherwise permuted JSON. Raw SCI restore
retains the same words. New first transfers append to the saved full sequence;
ACKs and later movements leave it unchanged. R1 incorrectly reconstructed this
order from transfer serials and did not preserve all ordinary restore inputs.

`p08Words` is committed state, `p08Work` is a candidate, and `p08Load` is the
streaming ordinary-restore buffer. Each is 88 words. `p08Output` and
`p08Prepared` are 39 words each. Session and callback identities are eight words
each, with a separate two-word callback revision. None of these identities are
process-global freshness evidence.

## Context and branch-local IDs

`p08SetContext(room, apron, preparations, wins, claimedFlags, padding, frankie,
bunny, contest, protectedMask, inventoryConflict, paddingPocket)` accepts only a
valid complete numeric context. Preparation bits are the 13 individual facts in
the manifest; all must be present for layout preparation. VC01/VC02 RESOLVED are
required, wins are not. Cross-branch dependencies are checked explicitly. Wins
and claimed P08 flags are each separate two-bit masks. Protected furniture uses
one bit per five movable objects. True Boolean fields must be exactly 0 or 1.

Rooms 1–7 follow their L01–L07 names. Location 8 is the shared kitchen-pass object
interface, never a travel destination. Object IDs are branch-local manifest
keys, not native allocations. IDs 1–5 are the five layout objects; 22 is the
internal padding handoff key. Historical native object proposals 116–123 are
not allocated here. Unknown nonempty strings lower to -1, empty strings to -2,
and absent optional targets to 0. The separate empty sentinel preserves the
literal model's empty-target truthiness behavior. `p08Inventory` supplies only
ordinary lookup membership for the current object/target; fixed layout objects
and carrier padding may not be claimed as pocket inventory.

`p08Query` provides location, reachability, condition-mask, and pending-handoff
count, with no observations. Five condition bits in order are buffet-at-hatch,
sound-facing-inward, display-concealed, hatch-visible, lane-clear. All five
readiness bits must be true. The sole hotpot remains in the kitchen.

## Output and transactions

Default maxima are three canonical records, six speech units and two events.
`p08Admission` may lower these capacities. A whole result must fit; overflow
returns `output_full`, clears partial output, and discards the candidate.

The output layout is manifest-driven: code at 0, revision high/low at 1–2,
record count at 3 and three records at 4–6, unit count at 7 and six units at 8–13,
event count at 14 and two 12-word event rows at 15–38. Each event row is kind,
commit serial high/low, object/source, choice/record, request high/low, ownership
serial high/low, condition mask, carried-service Boolean, reserved zero.
Event kinds lower the literal fixed payload schemas documented in
`tests/adapter.py`; that file only translates words, not gameplay transitions.
Original P08 result `speech_unit_ids` remains empty for literal result parity;
the distinct numeric SCI unit channel is checked against exact canonical units.

Successful mutations expose `p08CandidateWord` and `p08CandidateOutput` while
busy. Live words do not change. After the host has staged all effects, it calls
`p08Commit` synchronously. A definitive unchanged host failure calls `p08Abort`.
Uncertain publication calls `p08StorageUncertain`, which locks further actions,
commit and abort until whole-campaign recovery. Do not call internal helper
selectors directly from a host; use the documented entrypoints.

## Save and lifetime

The ordinary branch envelope is 108 words: magic 20536, schema 2, serial width
32, state count 88, sixteen signed words of the canonical-fixture SHA-256, then
88 state words. `p08SaveWord` reads committed state only. Stream exact consecutive
indices through `p08LoadBegin`, `p08LoadWord`, `p08LoadFinish(withContext)`.
Wrong identity, order, length, state consistency, or optional context is rejected
without changing live words. No partial restore is published. Successful load is
quiet, retires callback readiness/context, and requires a new session binding.

`p08AfterRestore` also retires this VM's session readiness. The caller must retire
outside-VM callbacks before any saved dispatcher resumes. Bind a new eight-word
lifetime identity with `p08BindSession`. Every source, ownership, readiness,
confirmation, retry, and save ACK must first call `p08SetCallback` with that
identity plus the revision of its actual receipt/request. A stale revision or
session is rejected. Layout movement clears pending start and changes revision;
restore never merges completion from another timeline. Room/session replacement
must retire external reader/render/save leases even if a saved numeric token is
identical. The domain does not claim process-global freshness or perform I/O.

## R2 compatibility and additional selectors

The literal reference JSON envelope remains kind `cakood-p08-branch`, schema 1.
Only this unintegrated port's raw numeric save schema changes to 2. R1 numeric
frames are rejected rather than silently inventing their missing order. No
native save migration or production integration is claimed. All preexisting
state offsets 0–81 and output payload meanings are retained.

R1's 102 P08 selector IDs are preserved alongside all 1,697 prior names. Only
`p08AppendOwner`=2702 and `p08PendingKey`=2703 are added, inside the assigned
2600–2799 range. The builder uses the frozen R1 mapping and fills unused IDs;
it does not re-sort and renumber accepted P08 methods. `p08PendingKey(index)`
returns the indexed pending ownership key from committed SCI words, or zero
when absent/out of bounds. The typed adapter translates that numeric sequence;
it has no private Python order field. The append helper is internal.
