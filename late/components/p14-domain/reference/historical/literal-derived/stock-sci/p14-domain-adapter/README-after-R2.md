# P14 final commitments and ending: isolated SCI1.1 domain adapter

Script996 exports `p14State` at export0. The standalone fixture uses species1;
production reserves species18. This module implements the accepted P14 state
model with exact canonical IDs and a finite, strict SCI save projection. It does
not install content into the campaign or implement ending artwork, typography,
music, playback, controller input, or native SaveGame/RestoreGame integration.

Run from the repository root:

```sh
sh stock-sci/p14-domain-adapter/build.sh
```

The build uses only the already approved pinned LucasArtsifier
`45068351290ffd90e74186c69322d200fa60cafd` and SCICompanion
`f1a603b48b1aa7abf94f78574a8f69a653e2ca62`. It regenerates exact records and
speakers, runs the compiler Boolean hazard scanner, compiles and packages a
standalone two-script fixture, validates resource/class/selector/relocation/SCO
structure, and runs accepted-model oracles on both parsed source and emitted SCI
instructions. The bytecode evaluator rejects unsupported instructions, invalid
memory bounds and unbalanced return stacks. This is emitted-bytecode regression
proof, not stock ScummVM execution or a desktop/audio test.

`manifest.json` provides every source/record/unit/token/status/event identity,
complete approved records and speech metadata, property order, allocations and
source hashes. The full revision3 catalog is bound to SHA-256
`1226a97873a3693867c08afe2731ddb55adef6f0eaeabc1222e103c04c0d9fa7`.
The quiet tag remains `P14.ENDING.002.02`, speaker `jack`: Put “It’s a meal”
underneath. In very large letters. No superseded pencil line is introduced.

## Native state and context

Eight original pledge cards use435–442 in canonical PEOPLE order: jack, bunny,
frankie, milo, vivian, rita, felix, stringer. The pledge board is P13's object433.
The original P09 terms card and P02 grease pencil retain existing identities.
No ninth pledge card, extra signature, new romance choice, real calendar event,
booking or contest win is fabricated.

Persist exactly the642 words in `manifest.persisted_properties`, in order. Two-word serials use
base32768, maximum1,073,741,823. Unicode date characters use the same limb format,
up to80 code points; no truncation or ASCII substitution occurs. Full credit
selection order, pause/skip/replay state, source starts, contiguous individual
text receipts, eight pins and every physical/finale milestone are durable.
Unused date/credit slots must be zero. `codec.py` rejects malformed envelopes,
field types, unknown keys and bad prefix ordering before conversion can lose
information. Native validation independently checks the finite state. A structurally loadable
credits cursor already at the roll length is refused before advance can move
beyond the array; this preserves state where the model would raise during its
post-mutation validation. Normal reachable transitions are unchanged.

The host owns atomic saves of this state together with campaign flags, actual
contest owner/timeline, external inventory, physical board/actors and upstream
ownership. The date and Vivian tone are snapshotted when commitments start;
subsequent rendering context cannot silently change either.

Project a fresh context with a strictly increasing runtime epoch1–32767:

```text
p14Context(room,apron,flagsHi,flagsLo,boardRoom,inputTone,contestActive,
           bunnyRoom,frankieRoom,miloRoom,vivianRoom,ritaRoom,felixRoom,
           stringerRoom,epoch)
p14ContextItem(object)                         for each actual inventory item
p14ContextWin(contestIndex,attemptHi,attemptLo) for EVERY actual latched win
p14ContextDateChar(index,codepointHi,codepointLo)
p14SealContext()
```

Flags are a bitset in `manifest.prerequisites` order, split at bit15. A plain
`ALL_VC_WON` flag has no authority. `codec.project_context` validates the actual
P14Context and VerbalContests owner, streams winning attempts in their real
ordered timeline, and seals the snapshot. Each contest is zero-based0–3;
outcome ordinals are positive, canonical `VCnn:Aordinal:KO` identities. Native
state snapshots the first real win and later context must still contain that
exact winning outcome. A later loss does not erase it; another saved timeline
cannot donate a missing win. No synthetic win is granted by this adapter.

Dates are sequential code-point receipts, not a hash or external mutable string.
Actor room -1 means absent; room IDs follow manifest. Tone0/1/2 means the existing
professional/friendly/cautiously-romantic P06 selection. Context inventory
rejects people and all P14-owned pledge cards. Builder errors invalidate the
entire snapshot. Context setters work only before sealing. All actions needing
context reject an unsealed or invalid snapshot.

The epoch must come from an owner outside the restored branch and never wrap
while an old callback can exist. `p14AfterRestore()` discards result buffers,
leases, context validity and staged-builder validity, then validates all durable
words. It does not reset corrupt state into a new game. Reproject a fresh epoch
before resuming. At epoch exhaustion drain callbacks and begin a new host
session. Cancelled or restored caption/freeze handles have no authority.

## Commitment API and exact consent

```text
p14StartCommitments(object,location,signed,dated,owner,record)
p14GiveCard(personIndex,recipientIndex)
p14ConfirmJackie()
p14PinCard(personIndex)
p14RequestSignature(method)     0 agreed terms, 1 forge, 2 coerce
p14PinSignature()
p14GivePencil()
p14CompleteCommitments()
p14Act(verb,object,target)
```

Start requires all28 earlier task facts, four real wins, the board physically in
L05, the original terms card in inventory, an agreed fictional date and no active
contest. Its finite terms metadata is object=`renewal_repair_card`, location1
(inventory), signed0, dated0 (no date), owner14 (P14 signature owner), record2
(the exact P09.READ.002 handoff enum). The host must obtain this metadata from the
actual P09 owner; native arguments cannot authenticate an arbitrary host.

Each approval comes only from its own exact presented `P14.APPROVE.person`
receipt, with the actual named speaker present. Wrong assignments return the
recipient's canonical correction and preserve all approvals. Pinned cards leave
the P14 inventory once. After all eight pins, Stringer's entire five-unit
`P14.DIALOGUE.003` must be visible before signing the original P09 terms card.
Forge/coerce requests emit the authored refusal and do not change state.

At signature, atomically remove the original terms card from external inventory.
At pencil handoff, atomically remove the original grease pencil from inventory.
Show date announcement, complete selected-date readback and pencil-return line
in that order. Completion atomically returns the same pencil and sets both
COMMITMENTS_SIGNED and GAME_COMPLETE exactly once before the ending. Context
validation rejects the borrowed pencil or signed terms simultaneously in pocket
inventory, and rejects completed state without its returned pencil.

## Text receipts and queries

```text
p14Begin(source)
p14Resume(source)
p14Acknowledge(source,startHi,startLo,epoch,recordID,firstUnitID,lastUnitID)
p14Cancel(source,startHi,startLo,epoch)
```

A receipt certifies actually visible text, never an audio callback. A whole
record uses both unit IDs0; a speech receipt uses record0 and a contiguous
inclusive unit range. Queuing, hinting, skipping a reader page, absent speakers,
wrong units, stale epochs or partial signature/readback do not grant consent.
Non-speech cards and credit pages require every page visibly rendered before
the whole-record receipt; the host persists partial page position separately.
Partial speech receipts survive reload. Resume needs only the remaining speakers.
`p14AudioFinished()` has no gameplay authority.

Read results through p14Code, p14LineCount, p14UnitCount, p14EventCount,
p14ResultHi/Lo and p14PresentationSource/Hi/Lo. Indexed getters are `p14Line`,
`p14Unit`, `p14Event`, `p14EventArg(index,arg)`, `p14EventSerialHi/Lo`. Capacities:
3 records,8 speech units,1 event and4 event arguments. Codes are internal statuses
and must never be used as player-facing prose. Unknown/out-of-range result
indices return0. Unused event arguments are0. Every event includes puzzle P14
and its committed two-limb serial.

Pure queries: `p14Ready`, `p14Approved(person)`, `p14InventoryAt(index)`,
`p14ReservedAt(index)`, `p14PencilWithFrankie`, `p14CurrentSource`,
`p14CreditRecord(index)`, `p14FreezePending`, `p14MissingWin(index)`,
`p14WonCount`, `p14NotebookRecord`, `p14RematchRoom(index)`,
`p14JournalAt(index,units)` and `p14PendingAt(index)`. Date and win limb getters
are p14DateHiAt/DateLoAt and p14WinHiAt/WinLoAt. `p14CreditAt` is an internal
source-ID getter; `p14CreditRecord` returns the canonical record ID for rendering.
Journal/pending order follows durable source starts through one transient sorted
index per query, not a hardcoded solution. Notebook queries expose the exact
missing-win record, actual count and each canonical opponent/rematch location
without closing exploration or granting progress.

## Finale and session-safe credit replay

```text
p14StartFinale(assetMask0,assetMask1,assetMask2)
p14PresentFinale()
p14AdvanceFinale()
p14AcknowledgeFreeze(finaleStartHi,finaleStartLo,epoch)
p14ClaimTagLaugh()
p14ClaimCelebration()
p14PauseFinale(paused)
p14SkipFinale()
```

Start requires legitimate completion. Three15-bit masks select the33 recognized
asset acknowledgments in canonical order (last mask0–7). `codec.credit_masks`
accepts only actual recognized shipped source URLs; all26 full mandatory credit
blocks are always included. Audition candidates are not selected by default.
Unknown sources fail explicitly. Full records retain URLs, names and licenses.
This selection does not replace final shipped-package/dependency licensing audit.

The normal phase order is closing → sincere meal → quiet L01 tag → visible
freeze → credits → finished. The inherited Vivian tone chooses the exact closing.
The host stages L01 and actual actor positions for the tag. No laugh can be
claimed during the sincere meal. LAF14 is consumed once after the entire tag.
The epoch-bound actual visible-frame receipt precedes one optional celebration.
END.FREEZE is stage metadata, never a spoken caption. Celebration only returns a
logical event requiring cleared audio and one PCM owner: composite or serial
laugh/cheer/applause. It does not claim any sound played.

Pause blocks new text/advances. Skip drops transient playback and closes the
viewer without changing earned consent, object transfers or completion. Restore
never auto-plays laughter/celebration. Every credit needs a visible whole-record
receipt before cursor advance; truncated/hidden credit text cannot complete it.

`codec.NativeCreditReplay.create(sourceVM,invoking_session,vm_factory)` copies
the native durable state into a fresh independent viewer, validates it and calls
`p14PrepareReplay()` only on that detached instance. The invoking session is a
deep JSON copy. Native replay clears previous credit receipts, selects credits
phase and retains completed consent history without granting it to the invoking
world. `save()/load(data,vm_factory)` preserves both worlds, cursor, pause and
return state. `return_session(cancel=False)` returns the invoking JSON by value
only at finish; `cancel=True` explicitly closes first. Mutating one returned
value cannot change a later return. Production must use an isolated heap/session
and persist the entire envelope atomically; never call p14PrepareReplay on the
active gameplay world. Replay does not repeat story scenes, signatures, physical
transfers, LAF14 or rewards.

## Event argument contract

P14_PRESENTATION_QUEUED: source,0,0,0; presentation/source
P14_PRESENTED: source,firstTokenIndex,lastTokenIndex,0; presentation/source and
exact canonical token range
P14_CARD_PINNED: personIndex,0,0,0; object/card_id,person,location pledge_board
P14_FINALE_SCENE: phaseIndex,0,0,0; presentation/phase, room L01 for tag else null,
scene_direction_id END.FREEZE for freeze else null
P14_FINALE_PAUSE: paused,0,0,0; presentation/paused

All following have zero args and these exact model payloads:

- P14_COMMITMENT_START: puzzle/cards (all eight canonical card identities)
- P14_TERMS_SIGNED: ownership/object_id original terms, from_owner P09,
  to_owner P14, location pledge_board, signed_by stringer
- P14_PENCIL_HANDOFF: ownership/object_id grease_pencil, from_owner inventory,
  to_owner frankie, temporary true
- P14_GAME_COMPLETE: puzzle/flags COMMITMENTS_SIGNED and GAME_COMPLETE,
  return_object grease_pencil, return_to inventory, before_finale true,
  terms_card_location pledge_board
- P14_FINALE_BEGIN: presentation/room L05, complete_credit_ids from current list
- P14_FREEZE_PRESENTED: presentation/direction_record END.FREEZE
- LAF14: laugh/after_record P14.ENDING.002, protect_meal true
- P14_CELEBRATION: presentation/cleared_asset_required true,
  pcm_policy single_composite_or_serial, transient_only true
- P14_FINALE_SKIP: presentation/drop_transient_audio true,
  completion_unchanged true

## Remaining production gates

Full-universe compilation preserving existing selectors/species and avoiding
music proof reservations, canonical reader/controller bindings, date substitution,
real individual speaker/actor staging and ownership transfers, board/inventory
rendering, genuine freeze pixels, complete credit typography and lossless URL
wrapping, isolated native replay/session restoration, host save-kernel round trips,
non-restored epoch lifecycle, single-lane final audio and credits-theme reprise,
cleared final media/asset/dependency notices, muted/controller/reduced-motion play,
and stock ScummVM end-to-end gameplay acceptance remain open. Script997 is not
used by this adapter; the class-free contest presentation owner retains it.
