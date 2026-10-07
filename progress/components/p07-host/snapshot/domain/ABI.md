# P07 R2 SCI ABI

## Allocation and immutable logic

Script988, class species10, export0 exports the `p07State` instance. Species9/script987 is reserved but unimplemented. The input compiler and all prior sources are pinned in `inputs/LOCK.json`. New p07-prefixed properties/method selectors are alphabetically assigned from1800, bounded by1999. Baseline selectors, including the compiler's internal selectors, are unchanged.

All canonical record, speech-unit, source-page digest, save-header, source-slot, label and LOOK mappings are compiled immediate-return methods. There are no canonical lookup arrays in serialized SCI locals. Local arrays hold mutable state, staging, output, tickets or validation scratch only. Heap strings are only compiler object/class names, not trusted source-page prose. Neither this design nor a saved counter establishes an external callback lease. A whole-VM restore still serializes locals, properties and heap strings; the host must gate dispatch and check the accepted build identity.

## Word representation

`manifest.json` is the exact numeric contract. SCI words are signed16 carriers of unsigned bit patterns. A serial consists of high then low raw unsigned16 limbs, allowing0..4,294,967,295. No15-bit truncation or saturating repair is used. Comparison splits the sign ranges; subtraction retains borrow and wraps only representational limb arithmetic. Source opening reserves one following acknowledgment/cancel serial. No method iterates across omitted serial slots.

The persistent payload has199 words:

- Revision:2 words
- Thirteen named cooking/optional/handoff receipts:26 words; laugh aliases onion exactly
- Three observations and one pending reader:four rows of41 words
- Trusted P13 handoff record:7 words

Each source row is presence, source enum, record enum,16 digest words, request high/low, page count, page index,16 page-digest words, page-serial high/low. Absent rows must be entirely zero. An observed row has exactly one page; a pending row has zero page payload and request equal to the current revision. Record/source/digest identities are checked against compiled constants. No orphan word is discarded.

The handoff row is presence, delivery-id enum, delivery-serial high/low, route enum, object enum, destination enum. Static identities are exactly P13:OWN:hotpot_pot, kitchen_hatch, hotpot_pot and L05_COURTYARD. Delivery serial is declarative data, never a session-bound authority.

## Save admission

The native envelope is219 words:magic20535, schema1, serial encoding32, payload count199,16 words of the canonical256-bit pin, then the199 payload words. `p07SaveWord(index)` reads it; `p07SaveReady()` validates the committed state. Export is blocked while a candidate, load or uncertain commit is outstanding.

Load uses `p07LoadBegin(219)`, exactly one ordered `p07LoadWord(index,value)` at each index, then `p07LoadCommit(withContext)` where withContext is0 or1. Header errors, omissions, duplicates, out-of-order writes, invalid native values and malformed complete states fail. Failed loads leave live state unchanged and do not repair it. A successful load leaves dispatch unbound until external retirement and a new session binding. `p07LoadCancel()` discards staging.

The independently implemented reference-envelope codec is `tests/adapter.py`: it checks exact keys/types, source row shapes, uint32 bounds, canonical SHA identity, canonical JSON SHA256 integrity, duplicate JSON keys and the32KiB JSON bound before lowering. It never invokes the reference validator to decide SCI acceptance. Native integer transport cannot distinguish Python bool from int or preserve arbitrary JSON types: an actual native caller must perform equivalent typed admission. The SCI implementation then independently validates every payload word, aliases, causal ordering and exact omitted-source history. The new fixed-word native envelope is deliberately incompatible with a JSON envelope; there is no asserted original save compatibility.

## Host-facing entry points

The exact arities and enums appear in the generated source/manifest. Treat all other methods as internal helpers, not dispatched player actions.

- Startup/lifecycle: `p07Init`, `p07BindSession(a..h)`, `p07AfterRestore`, `p07SessionWord(index)`, `p07RejectInput`
- Immutable-context admission: `p07Context(room,apron,plan,introduction,claims,bunnyRoom,bunnyApron,bunnyInvited,owner,ownerRoom)`, then `p07ContextItem(-1)` for each unrelated pocket item. A P07 fixture/pot must not also be in inventory. The context setter validates shape; action/load validation checks the appropriate timeline
- Actions: `p07Perform(action,measure)`, `p07UseStove`, `p07Hint(level)`, `p07MeasureChoices`, `p07Look(localObject)`, `p07Label(localObject)`
- Reader: `p07OpenSource(source)`, `p07SetInput(source,requestHi,requestLo,session0..7)`, `p07PageBegin`,16 ordered `p07PageWord` calls, `p07AcknowledgePage(source,record,index,count)`, `p07CancelSource(withContext)`
- Non-authoritative presentation: `p07PresentationSignal(signal)`; audio/animation completion never grants knowledge
- Future trusted handoff: `p07Handoff(delivery,hi,lo,route,object,destination,hostPresent)`
- Transaction: `p07CandidateWord`, `p07CandidateOutput`, `p07Commit`, `p07Abort`, `p07StorageUncertain`
- Committed read-only state/output: `p07Read`, `p07OutputWord`, `p07Projection`, `p07Object`, save/load methods above

Every rejected mutating/admission call retires transient published effects/output; typed requests rejected before numeric lowering must first call `p07RejectInput`. Read-only getters do not retire output. Invalid calls cannot republish a previous FOOD_READY, laugh, record slice or source token. Prepared candidate output is separate and cannot be overwritten by a rejected reentrant action.

## Output and transactions

The20-word output contains result code, revision, up to two records, up to five exact speech units, optional event/serial/after-unit, source token/request and displayed-page identity. Use only the explicit counts. Interface records legitimately have no speech units. Onion uses exactly.01–.03 and LAF07 after.02; sincerity uses exactly.04–.05 without laugh. Closing the lid emits FOOD_READY once per timeline.

Successful state changes set `p07Busy` and stage both state and output. Committed state stays unchanged, normal output access is blocked, and candidate getters expose the prepared transaction. The host reserves/render-validates all exact outputs and physical changes, atomically publishes the whole host candidate, then calls `p07Commit`. No callback, allocation, validation, I/O or possible new failure is allowed between final host publication and that assignment-only commit. Before publication, `p07Abort` leaves state and outputs unchanged/retired. If storage publication is uncertain, use `p07StorageUncertain`; it blocks commit, abort, load, reinitialization and further dispatch until the host reconstructs from known durable state in a new instance.
