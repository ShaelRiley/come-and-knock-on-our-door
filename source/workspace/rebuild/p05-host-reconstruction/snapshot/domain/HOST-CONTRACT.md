# Required native host boundaries

None of these boundaries is implemented by frozen P04 Main. This isolated domain proof must not be reported as native P05 acceptance.

## 1. Campaign snapshot and movement

Supply actual current room, apron state, Milo/Bunny positions, audience presence, inventory, external contest facts and ownership. Domain invitation only requests a visible Bunny escort or audience agreement; it never teleports actors. Preserve normal return/escort actions and save positions together with domain state. During an external contest, block conflicting P05 actions. A domain request or ACK must never resolve, win or teach VC01.

The domain accepts external resolved loss. It neither requires a win nor manufactures a result. On rematch, check Milo's actual current accessible room. The campaign owns movement/access and contest availability; no garage-only rematch restriction is introduced.

## 2. Reader receipt, not queue receipt

Read-only inspection does not grant observation. `p05ReadSource` opens/resumes an exact source+record+room request and returns a scoped token. The host may call `p05AcknowledgeSource` only after the exact readable record has actually been presented at the reachable arrival-side location. Queuing, audio completion, early Close/Back, selecting a record, merely having it available, or clicking a wrong-location stale button is not such evidence. Cancel invalidates the logical request. Replacing/resuming after restore issues a fresh callback token. Slate reading requires the exact credit to exist.

Preserve optional speech/laugh metadata, but drive no success, notebook observation, ownership or contest score from audio completion. The existing single PCM owner and lifecycle remain untouched.

## 3. Session leases and native restore: unresolved host gate

Reference UUIDs are **not** an SCI implementation. This domain compares all 128 session bits and all 32 logical receipt bits. The native host must bind a fresh nonzero 128-bit session lease on initialization and after every accepted restore. A lease must never be reused while any callback bearing it could still be dispatched, including callbacks from another world instance and a repeatedly restored snapshot.

Native `RestoreGame` restores heap/locals, including stale runtime fields. Therefore `p05AfterRestore()` is a mandatory first post-restore action, before queue/input/choice resumption. It blocks all domain actions and clears current callback readiness. Then retire restored/previous callback queues, bind a fresh session with `p05BindSession(lease8)`, revalidate composed campaign context, and resume logical reader/request state to acquire current tickets. Binding rejects a zero lease and immediate reuse. The host must also enforce process-wide/cross-world freshness or prove retirement of **all** obsolete callbacks; the domain cannot infer that fact.

A monotonic counter saved in SCI memory is inadequate: restoring the same snapshot twice repeats its successor. No nonexistent kernel, wall-clock uniqueness assumption, saved PRNG assumption or hidden Python UUID is used here. A stock-SCI host still needs a supported lifecycle mechanism with demonstrated freshness/retirement. This is a concrete remaining native integration gate. Until proved, do not enable asynchronous native P05 callbacks or call this package restore-safe in ScummVM.

The fixed-word save loader gives executable domain-level invalidation evidence, but is not a replacement for the above whole-game RestoreGame hook.

## 4. One borrow choice, synchronous atomic host transaction

The player chooses borrow once. Do not expose a new confirmation puzzle or wait state. Under the host critical section:

1. Establish trusted context and obtain a fresh candidate lease
2. `p05PrepareLoan(lease8)` computes and validates the candidate, exact loan+completion records and ownership destinations while preserving original persistent state
3. Prevalidate both exact readable routes/capacity and both physical destinations: PA P05/courtyard staging, cart P05/visible garage parking. Pencil and cable are never pocket rewards
4. Atomically publish physical owner projection and exact reader output, or leave both unchanged
5. Immediately call `p05CommitLoan()`: only already-validated state/session assignments occur here, with no callback, dispatch, save, I/O or failure-prone work between physical and domain commit
6. On preparation/commit failure before publication, or after complete physical rollback, call `p05AbortLoan()` and leave the player's original state unchanged

The domain refuses reentrant action, context replacement, save, load, reset and restore lifecycle entry during the prepared critical section. Prepared output survives rejected reentry. The host must also prohibit its own SaveGame, input and external callbacks during the entire critical section. No partial native queue is assumed atomic merely because it exposes a `commit` method. Exact output and both owner writes require native failure/rollback evidence.

The accepted Python helper validates the candidate against the supplied context after completion. Consequently, for this helper interface a context explicitly claiming **pre-loan** PA ownership in the garage would conflict with completed P05 courtyard staging and fail. Supply an otherwise authoritative domain context without ownership overrides during candidate preparation, while independently prevalidating the actual old owners in the host transaction. Publish and supply the new exact owner projection after success. This existing reference-interface constraint is documented rather than silently changed in the SCI port.

Low-level `p05Borrow`/`p05AcknowledgeHandoff`/`p05CancelHandoff` exist for parity and recovery. Their staged request never proves the objects moved. ACK is trusted host-only after atomic movement with exact destinations. Cancellation is trusted host-only after cancellation/rollback. Starting a request reserves completion/cancel capacity. No unrelated mutating action can spend it.

## 5. Ownership and later consumers

Historical completion is not an ownership grant replayed on load. Current host ownership is authoritative. P05 kit includes credit slate and cable; all kit parts follow PA to courtyard. Handcart and garage mark are separate. P08's retained `P08:OWN:pa_kit` claim must apply exactly once after its genuine placement, then receive its own original ACK. After P08 ownership, P05 projects no PA/component/cable location. Cart may pass to P11/P13, never P08.

Current hardware may be edited without erasing historical tests/credit/role/completion. Later puzzles must inspect their own current working-hardware interface, not infer it from SOUND_READY. Save all branch/host owner state together and prove no reward replay.

## Before native integration

Do not append blindly to frozen Main. Measure capacity and design a separate host adapter. Recompile every affected module together against one allocation. Combine the separately reviewed scene/art/contest work only after coherent compilation and independent review. Then obtain stock-ScummVM fresh-input, interruption/restore, same-build save and physical/source-receipt evidence. Publication and binary compatibility remain outside this packet.
