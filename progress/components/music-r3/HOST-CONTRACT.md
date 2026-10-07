# Guarded responsive music host interface

## Scope and identities

Module943 owns serialized music-only locals and no class. Module941 and942 are separately named instances of MusicTransport/species3. There are no new selector IDs. The existingSound class has one new inactive instance, `responsiveSound`. In an activated future host Main uses its one `musicOwner` slot with kind3 and that Sound object; broker943 serializes all family/connector ownership internally. Kind1 credits and kind2 original981 keep their meanings while the candidate is disabled.

The compiler API is `generated/api.json`. Internal exported helpers are linkable for emitted verification; callers must follow the public host boundary, not call `rbStartBed`/`rbStartBridge` to bypass it. `rbInit(sound, actualPriorTransport, priorKind, 17061)` is deliberately an isolated fixture seam. Production sources contain no invocation. PriorKind must be0 after Main's existing credits or transport retirement, and any actual prior transport must report stopped. Neither0 nor17061 is evidence of native or listening approval.

The single native object is always retired in this order: owner-local whole gain0; actual owner's stop; actual dispose; broker owner slot0; assign new Sound number and initialize/play. No two initialized/running slots are permitted in the emitted oracle. Original980 PCM is never called by a music module. Existing Main PCM/foley/speech retirement ordering is preserved by the adapter.

## Actual committed notifications

The sole event adapter is inserted into985 hVCApply after hVCCommit succeeded and hCritical cleared. It never changes the original operation result:

- operation3 → VC_ENTER1: active90=1, encounter91=1–4, phase92=1, cursor95=0, newer nonzero attempt2/3
- operation4 → VC_TURN2: committed phase2–4, current slot99=cursor95+1 in1–5; ordered exact same encounter/attempt
- operation6 → VC_RESPONSE_COMMITTED3: phase5 and cursor equals the observed exchange, consumed once
- operation8 → VC_KO_COMMITTED4 only with phase7, result102=1, reason101=1 and an actually zero participant meter96/97
- operation9 → VC_EXIT5 only when acknowledgment reaches phase8 with terminal102=1 and result-presented104=1

Reason101=2 whole-contest concession reaches EXIT but is never a KO. Claims10/11, selection5, prepare operations, source views, M-menu and visual hVCStageLeave do not emit music. A real thinking/line state may use `rbEvent(2,domain,1)` only while that exact committed turn remains current; completion uses0. There is no timer or guessed utterance completion. Until that host speech seam is independently proved, the compiled adapter uses only the committed-turn opponent row.

152 has the exact140–145 CC7 colors on one152 parser. Those references do not play independently. Optional response/KO accents are consumed but never queued or played. The generation is two nonwrapping15-bit limbs and exhausts fail-closed. A new request replaces the target; a stale caller generation cannot retire the current owner.

## Musical transaction and boundaries

For a running bed, poll its source-derived apertures only. Both position reads must be monotonic and within the same aperture. A late second read, uncertain clock or missed window leaves the source intact. A canceled request preserves its source parser and position. The source is never truncated because held keys alone look quiet.

Every bridge has a genuine6–8 controller guard before attack12. A missed startup guard stays inaudible and is marked degraded, but gameplay continues. Natural bridge completion requires native signal255 and position at its source-derived end, accounting for SCI's2-tick displayed quantization; zero keys alone cannot complete it. End selects the latest valid family once. The key-clear gates do not imply release/reverb silence.

The static guards are fresh at startup, chooser admission and successful restore admission. Runtime normal polls use the already-admitted constant tables without a saved validation flag. Native time spent validating and rebuilding controllers is not measured by this packet and must be included in any future actual latency claim.

## Controls and save/restore

- `rbHomeRequest(state)` preserves the existing HOME main/reduced row0/1, including changes while contest or a bridge owns the Sound. Main routes its existing audioDesired value through this idempotent call. The latest row is used on the next HOME entry, with no new clock or parallel player
- `rbPreference(whole,muted,paused)` preserves the latest per-owner target0–100 and actual0/1 controls. It never changes global master volume or synth/PCM settings
- `rbBeforeChooser()` validates, silences and freezes the current parser. It refuses duplicate entry. A bridge uses one owned pause independent of user pause
- `rbAfterChooser()` cancels/fails back once, keeping the exact existing bed or bridge clock. No note/bridge/accent is restarted
- The Main replay route first completes existing P05 (and P06 when included) hRestoreBegin retirement. `rbRestoreBegin(responsiveSound)` then validates fresh static and complete modeled owner/intent/ledger state, invalidates the prior musical generation and disposes any saved transient bridge before the old replay body can dispatch work
- Main's audioRestore branch stays frozen while rbRestoring is set. Only the final Main p05RestoreValidate success, after every included P05/P06 domain/physical/scene check, invokes `rbRestoreResume(validated986)`
- A saved bed follows its actual afterFrozenRestore protocol and keeps its saved native clock, current gains and expression/history reconstruction. A saved bridge is never replayed: after full domain admission it starts the validated current bed through its normal startup guard
- Reconciliation consumes committed cursor/result state without invoking rbEvent or playing anything, including a response/KO committed before snapshot but not yet notified musically. A saved music ledger ahead of committed domain is invalid
- Repeated loads can reproduce the saved generation. Safety relies on complete retirement plus stock RestoreGame abandoning the old invocation stack, not claimed globally unique saved IDs

The pinned2026.3.0 savegame.cpp clears the old playlist before deserializing/reconstructing saved music entries, and sci.cpp starts replay after abandoning the prior VM stack. The new source has no asynchronous callbacks or secondary music tasks. These are source facts, not native proof of resume or tail behavior. The typed mock deliberately does not claim physical-channel or reverb fidelity.

## Composition and preservation

`integrate.py` consumes exact pinned full source snapshots. It preserves source and fresh emitted bytes for original980/981/982/983/984/986 and987 in P06. OnlyMain/985 receive narrow guards and music hooks. Main remains below the SCI64KiB segment bound; current measurements are `evidence/host-composition.json`. Existing240/241/242/244 guards and accepted940/243 are preserved.

The P06 snapshot is frozen candidate1 plus the exact inventory-fixR2 delta, pending that worker's final full QA. Its shared985 host chooses encounter1/2, and986 remains unchanged. A later accepted P06/P07 composition must explicitly re-pin the full source and fresh compile all modules together. Never silently read a moving source tree or splice this packet's compiled resources into production.

## Revision-2 status and failure boundary

Read `REVISION-2.md` for the exact UI states and guard evidence. `rbAvailable()` means ready at the current requested family, not health. Active Main uses `rbHostStatus(self)` and `rbDrawStatus(musicUnavailable)`; disabled admission delegates unchanged to its original lane. `rbRetry(responsiveSound)` is admitted only for a genuinely retryable inherited failure, freshly validates complete ownership/static state, and retains the parser/clock. An exhausted generation is sticky error9: no later bed poll or connector completion can start pending musical work. A connector already playing ends naturally and is retired. User controls and gameplay remain live. No saved UI cache is authority.

## Revision-3 finite lifetime and load admission

Active Main.writeSave clears its old result and calls `rbSaveAdmit` before existing guards. Generation [32767,32767] or error9 refuses before native SaveGame with a save-specific footer. A snapshot at [32767,32766] retains exactly one advance for the unchanged early restore protocol. `rbLoadChooser(host)` is used only by Main.readSave: ordinary owned states use the existing chooser; an empty failed owner requires fresh full validation and both stopped transports before entering a cancelable load chooser. No save or restore guard is bypassed. See `REVISION-3.md`.
