# MUS11 host integration contract

## Ownership

Main remains the sole arbiter of full-score ownership. Existing credits kind1 and world kind2 retain their current meanings. A future reviewed host may add owner kind3 for `(ScriptID 940 0)`, while keeping a single `musicOwner` slot.

No940 call implicitly stops981, changes an underlying room, or starts a second parser. `vcStart(sound, priorOwner, lease, transitionProof)` refuses an actually running prior MusicTransport, an occupied940 lease, the wrong Sound resource, invalid context or missing required background proof. The host must finish the selected natural transition, stop/dispose the outgoing owner, then change the owner slot and call940. `transitionProof=1` is an isolated offline fixture seam, not user authorization and not an accepted native gate. Do not put an unconditional literal1 in a live host.

The future host must also retire a credits Sound through its existing kind1 path before reaching this interface. The940 prior-owner parameter is a MusicTransport, not a credits Sound. Passing0 is valid only after Main has independently proved its owner slot empty. Do not treat the runtime mock's concurrent-parser assertion as a production broker implementation.

Use `(use "module940")` and the compiler-generated SCO public procedures in a coherent source build. Exports are listed in `generated/api.json`; export0 is the instance. All43 transport methods use existing selectors. Do not splice940 compiled bytes into a separately compiled class universe.

## Canonical committed-event reads

`vcEvent(event, domain986, thinking)` reads only the committed `vcRead` interface and the domain readiness/busy/uncertain flags. It does not call any mutation method. Every prepared-but-uncommitted operation is rejected for musical notification.

| Event | Numeric value | Required committed evidence | Music result |
|---|---:|---|---|
| VC_ENTER |1| active90=1, encounter91 in1–4, phase92=1, cursor95=0, nonzero two-limb attempt2/3 newer than that encounter's saved highwater | Save identity and request required140 bed with opponent gain row |
| VC_TURN |2| phase2–4; slot99 equals cursor95+1 in1–5; same attempt/encounter; ordered current turn | `thinking=1` selects145 gain row;0 selects the opponent row |
| VC_RESPONSE_COMMITTED |3| phase5; committed cursor95 matches observed exchange; not already consumed | Consume optional response accent once; current implementation plays none |
| VC_KO_COMMITTED |4| phase7; committed KO102=1; same attempt, unconsumed result | Consume result once, including explicit yield with zero responses; current implementation plays no accent |
| VC_EXIT |5| phase8; KO102=1 and result-presented104=1 | Request exit transition; discard further stale events |

Attempt identity is two base32768 limbs, not a wrapping scalar or an invented serial. Response identity is `(encounter, attemptHi, attemptLo, exchangeSlot)`. Result identity is `(encounter, attemptHi, attemptLo, resultSlot0)`. A highwater is scoped to the relevant attempt and encounter. The event counters are diagnostic and are not identity.

Specific encounter bindings remain VC01/Milo/P05/L06; VC02/Vivian/P06/L03; VC03/Felix/after safe P11 rescue and before P12 introduction/L04; VC04/Mr.Stringer/after P13 delivery and before toast/L05. Nothing here creates a later puzzle, admits an encounter, awards a win, changes composure, teaches an insult pair or alters concessions.

Call events immediately after the corresponding existing host persistence+`vcCommit` succeeds. Selection preview, `vcChoose`, a busy prepared candidate, `vcClaimEffect` retry, text reread and restore are not substitutes. The emitted tests execute actual986 prepare/commit, three completed responses, KO and final acknowledgment.

## Stage, menu and PCM boundaries

P05's `hVCStageEnter` and `hVCStageLeave` own visual presentation. They do not by themselves prove a committed VC_ENTER/VC_EXIT. M-menu, Close, `speechCancel`, `voiceOff`, save chooser and visual stage retirement must not become a contest yield or a new musical attempt.

Use thinking/line gain state while actual consequential speech owns the existing serialized PCM lane. It is not a speech timer or correctness hint. Real utterance completion controls return to the opponent color. Preserve owner980 and all existing speech, groan, audience and foley priorities. Do not add DoAudio/DoSync calls to940.

## Ordinary controls and frame polling

After the sole owner slot points to940, route the existing `setWholeTarget`, `setMuted`, `setPaused`, remap and frame-poll calls to that instance. `vcPoll(lease)` rejects stale leases. Keep the latest user's master/music preferences; do not write global master volume, device settings, SoundFont gain or PCM gain.

The six state rows are exact140–145 gains, not six parsers. States1–4 are opponents;5 is the restrained thinking/line row;0 is a source-reference baseline for the isolated transport. On startup, the selected row is copied into current gains and program/pan/CC11/gain controllers are rebuilt during tick6–8. A second position read must still fit the guard before whole-Sound gain opens. The first authored note is tick12.

Regular positive-gain reversals retain one clock. Only inactive TEXTURE/ACCENT channels2/6 cross zero in this bank; the generator and tests prove they contain no140 note events. Existing bounded muted-tail clearing is channel-local. It is not a claim that the synth's residual release or global reverb is silent.

## Frozen chooser and restore

Before a real modal native save/load chooser:

1. Preserve the current Main foley/speech retirement order
2. Call `vcBeforeChooser(lease)`; abort chooser entry if it fails
3. The transport acquires its owned pause and holds whole-Sound gain silent; the parser's saved position is frozen

On chooser cancel/failure return, call `vcAfterChooser(lease)` once. It refreshes civil/tick anchors and uses the existing bounded rejoin path. Do not substitute ordinary non-frozen `beforeSave`/`afterSave` around the actual modal chooser.

On successful restore, after the domain's saved committed state is validated and ready to be read but before any saved presentation can dispatch, call `vcAfterRestore(lease, domain986)`. It freshly verifies text243 against every static local table and calls `vcResume(domain986)` to reconcile durable identity. Committed cursor/result state is marked consumed without emitting events, even if its musical notification had not run before the snapshot. The transport then follows `afterFrozenRestore`, reconstructing current gains/programs/pans/CC11 and lifecycle rather than replaying old responses/KO.

`vcMutableValid` rejects out-of-range current gains, target rows inconsistent with selected state, and invalid whole-Sound targets. Invalid context, missing constants, uncertain position or recovery expiry must be reported as required-family unavailable and remain fail-closed; silently calling the world cue a successful MUS11 activation is incorrect.

## Static-table guard addition

Keep P05's current981/982/985 `hStaticAt` additions and `hStaticAll` replay checks against240–242 exactly.940 adds a separate public `vcVerifyTables()` backed by243. Add that call to the future combined replay path before940 metadata can influence Sound state. It reads every20-word decimal chunk from the packaged text resource each time; it never trusts a saved hash/check flag.

Do not call inherited `hStaticAt` on940 expecting it to address940 tables: an inherited981 method would read981 locals. Use the new public procedure.940 introduces no fixed heap UI strings other than the instance name, which is never used for routing, text lookup, identity or Sound calls. The compiled name/resource/hash identity is checked offline.

## Natural serial handoff proposal, explicitly unaccepted

Actual native metadata supports these candidate fade/retire windows:

-102→140: the existing natural-turnaround cue starts at4126. A proposed owner-local gain envelope reaches0 at4246, after all authored102 key-offs; the final no-held-key rejoin interval is4246–4248, before end4255
-140→102: the existing natural-turnaround cue starts at3852. The proposed envelope reaches0 at3962; final no-held-key interval3962–3964, before end3972

The proposed envelope uses the current user whole-Sound target, not a permanently captured preference. Cancellation reverses through the existing bounded ramp toward the current target, keeping the outgoing parser and clock. A stale request generation or expired interval never disposes the owner. Only the reviewed Main broker may perform stop/dispose, owner-slot replacement and target startup in one host transaction. There is no added sleep or synthetic silent bar. Target startup retains its original authored12-tick onset and native controller guard.

This is a concrete offline timing proposal, not proof that the change sounds natural.102's F-major-family at112 BPM and140's F-minor-family at120 BPM require evaluation of the fade versus a separately source-derived C7-to-target-family bridge. Any new bridge should be a new candidate resource after allocation review; all38 original pairs remain byte-locked. All release/reverb, allocator and musical acceptance flags in `handoff-candidates.json` remain false. If this transition is judged unsuitable, author and test the bridge instead of forcing the fade into the live host.

## Optional accents

146/147 are source-preserved, disabled candidates. Enabling either requires isolated native proof of reserved ACCENT replacement, channel/voice ownership, no shared percussion-controller writes, one-shot retirement and protected speech. Missing them does not invalidate required140 background behavior. Conversely, their optional status is not permission to omit the background family.

### Practical latency limitation

Waiting exclusively for the full composed turnaround can defer a newly requested change by nearly a full cycle:70.718081 seconds for102,66.001320 seconds for140. This makes the fade/entry scheme an offline fallback candidate, not a recommendation to ship that delay. A responsive live contest entrance likely needs a shorter source-derived bridge at reviewed natural phrase endpoints. Do not hide this latency by an arbitrary cut, silent wait, score-driven input deadline or premature claim of MUS11 activation.

### Whole-contest concession is a non-KO ending

An explicit whole-contest concession (`vcRead(101)==2`) is a non-KO native ending. Accepted986's terminal bookkeeping uses its committed result flag102 for this path too. That flag alone never authorizes zero composure meters, a groan, a KO presentation or a later KO accent. The current940 ledger consumes a terminal result once but plays no accent and does not touch meters or PCM. Its event name is not semantic permission to add those effects.

Any future true-KO accent must additionally establish the committed normal-composure outcome (`vcRead(101)==1`), the actual committed exhausted participant (`vcRead(96)==0` or `vcRead(97)==0`) and the appropriate existing profile/line lifecycle. Whole-contest concession must retain its explicit non-KO result treatment. This distinction remains mandatory even after optional146/147 native isolation passes.
