# P11: Move the Oversized Display Together

## Scope and canonical lock

`cakood/p11_model.py` models safe cooperative transport and a VC03-entry request.
It is isolated Python using the standard library, existing `Event`/`Result` and
seven-room registry, P04's immutable `GateHandoff`, and P10's internal finite
caption ledger. It neither runs VC03 nor reveals the display or completes P12.

Mechanics follow P11 and the VC03 section of the current GDD. Every player line
is an exact stable ID from full script editorial revision 3, catalog SHA-256
`1226a97873a3693867c08afe2731ddb55adef6f0eaeabc1222e103c04c0d9fa7`.
`tests/fixtures/p11/canonical-bindings.json` preserves record provenance,
obligations and exact speech/laugh metadata. Machine `code` is never dialogue;
`text` is always empty. No canonical source or native resource was edited.

- GDD: <https://docs.google.com/document/d/1D-tndxod3dJNOVANuA1e1c-Zm8Im6sew9qhuzm09vLU/edit>
- Script: <https://docs.google.com/document/d/1HpiFbCn7FniV3kLjTDP5nP1Ow0N5JMHuEeO0EeG1rEQ/edit>

## External ownership and prerequisites

`P11Context` supplies the actual room/apron state, prior flags, outside inventory,
NPC positions, cart/display locations, contest mode, and P04 gate handoff.
Starting requires `EVENING_STARTED`, P09's `RUMOR_CLEARED` and
`TERMS_CARD_AVAILABLE`, and historical P10 `CUES_RESTORED`. No previous contest
win is added as a gate. Prior branch facts are not duplicated or mutated here.

The only object IDs used are the original `folded_display`, `handcart`,
`hold_open_peg`, and their fixed control/position hotspots. None can be pocketed.
`inventory` is always empty. The host must visibly bring the existing cart and
securely attached display to L04 before calling `lift`; both supplied locations
must match. Once the rescue begins, `reserved_external_objects` identifies those
two objects so no other branch can transport a duplicate concurrently. The host
retains this single P11 projection until explicitly transferring it to P13.

Bunny's peg reach is from L03, Frankie's catch reach is from L05, and Felix must
be in L04. These are the canonical cross-side sightlines, not teleports or new
rooms. Rita's L04 staging gratitude waits until her actual arrival; physical
staging does not require her voice to finish or pretend she is there.

## Physical state and reversible safety

The states are `CART`, `SUPPORTED`, `FOLDED`, `STAGED`.

1. `lift` recognizes the already tested, available P04 peg and the existing
   padded cart. Jackie and Felix support the safe, covered panel. A pre-engaged
   peg is recorded at this moment and never reset.
2. `request_peg` asks Bunny to engage the existing P04 fixture. It emits
   `P11_PEG_REQUEST` with a request identity and owner `P04`; it does not set a
   second peg boolean. The host performs the P04 action and feeds the updated
   handoff back to `acknowledge_peg`. An unengaged peg cannot be acknowledged.
   If already engaged, the canonical `P11.SUCCESS.002` recognizes it without
   creating an unnecessary request.
3. `release_catch` is the explicit request to Frankie at the courtyard side.
   It releases P11's marked wing catch. The two helper requests can occur in
   either order, and neither automatically performs the final pull.
4. `pull_handle` rechecks the current actual P04 peg, catch and Felix. It folds
   the wings onto their padded stops and safely lowers the display to the cart
   immediately. This physical action does not wait for text, voice, music,
   animation, a reaction, or a timer.
5. `stage_display` parks the folded cart in the existing L04 hidden wall recess.
   It grants only `DISPLAY_STAGED` and `HELP_ACCEPTED`, once. No second screen
   item is created. Rita's panel stays covered, undamaged and unrevealed.

`set_back` is always available from `SUPPORTED`. It resets this support attempt
and its catch/pending peg request, preserves the actual P04 peg, preserves all
observed dialogue, and returns to the safe cart posture without solving P11.
Repeating it is quiet. Before ordinary travel or crossing to the audience apron,
the host invokes this hook atomically with movement. Menus, pause and save need
no special restriction and may retain the supported state. If the host already
changed rooms, the hook can still recover physical safety without inventing a
speaker line or moving a character back. `validate_context` rejects saving a
supported display with Jackie on another room/apron or Felix absent.

Pushing harder gives the exact fold-not-force line and changes nothing. Missing
peg and missing catch each have their own canonical failure. No breakage,
injury, death, exhaustion, hidden timer or permanent loss exists.

## Protected text and VC03

Physical safety is independent of caption receipts. `sincere` refers to all six
units of `P11.DIALOGUE.002`; VC03 eligibility requires every unit actually
presented. Pure queries, source queueing, hints, skipped/unseen pages and audio
completion are insufficient. A started `concern` scene remains protected until
all units of `P11.DIALOGUE.001` are displayed; it blocks a contest while pending.
A new initial-concern scene cannot be invented after safe folding/staging.

`request_contest` requires `STAGED`, all sincere units, no pending concern,
Jackie and Felix at L04, no apron, and no active contest. It emits only a durable
`P11_VC03_REQUEST`. The host then invokes the existing verbal-contest owner with
that safety evidence. Resolving an attempt, repertoire learning, result
presentation and all contest flags remain owned by `VerbalContests`.

A receipt acknowledges or cancels the specific request once. Stale identities
cannot start a different attempt. The stable practical rescue flags do not
change on VC03 wins, losses, rematches, cancellation or later result wording.
A later resolved result selects `VC03.REMATCH` for the next request. The branch
never sets `VC03_RESOLVED`, `VC03_WON`, `INTRODUCTION_CLEAR`, `DISPLAY_REVEALED`,
`TOAST_READY`, `COMMITMENTS_SIGNED` or `GAME_COMPLETE`.

`display_handoff` describes the exact safely staged cart/display, covered panel,
shared helper identities, and future owner P13. `rita_reveal_consent: false`
means P11 grants no P13 reveal consent. P13 must obtain her explicit cue then.

## Audio and presentation

No action in this model plays audio. Caption pages/units are acknowledged through
the same trusted visible-text barrier described in `p10-state-contract.md`.
`fold` is `P11.SUCCESS.005`; `staged` is Rita's `P11.SUCCESS.006`.

`claim_laugh` emits LAF11 once only after safe staging, completed protected text,
completed fold payoff text, and no contest/request. The canonical alternative
speech binding is `P11.SUCCESS.005.02`; it must not double-fire alongside the
physical payoff. Consumed state survives saves, so restoration does not replay
it. This conservative domain timing deliberately leaves the native adapter to
place the earned payoff naturally and obey the single-PCM-owner policy. No laugh
is emitted from initial concern, sincere conversation, safety recovery or wrong
physical actions. Editorial laugh opportunities in the catalog are metadata,
not a new gameplay reward or mandatory reaction.

## Save/load and callbacks

Envelope `cakood-p11-branch`, schema 1, stores phase, action serials, helper/catch
state, pending handoffs, finite caption receipts and the consumed laugh serial.
It serializes no sound, timer or other room authority. Reload retains the exact
logical state and issues a fresh runtime callback epoch. Old peg, contest or
caption handles from a pre-load or abandoned timeline are stale even when their
numeric serial matches. The host resumes a saved presentation or retrieves the
current pending request identity after load.

Validation rejects malformed state, unknown phases, boolean serials, impossible
attempt chronology, safe folding before the helper catch, staging before fold,
non-prefix or backward caption receipts, unsafe/premature contest requests,
reaction before its protected/payoff text, and conflicting aggregate ownership.
It is structural, not cryptographic save authenticity. P04 gate state, campaign
positions and this branch must be saved/restored in one transaction.

## Explicit canonical integration seams

1. **Sincere scene timing.** The script trigger says the honest conversation is
   while safely supported. The GDD permits immediate physical recovery and only
   requires the sincere beat complete before VC03. Therefore physical rescue
   never waits on its receipt. Exact existing text can begin/resume at the safe
   cart or staging position after an interruption. A later scene adapter must
   stage that continuation naturally; no line was rewritten and no additional
   conversation prerequisite was added to rescuing anyone. This timing choice
   was explicitly reviewed during this domain task.
2. **Advance peg and spoken credit.** The GDD honors a peg engaged before carrying.
   VC03's current WIN/LOSS lines literally say Bunny secured the gate. This model
   preserves that pre-engaged state and the canonical four-person shared-credit
   contract, without inventing an action Bunny did not perform or rewriting the
   result line. The precise wording for this legitimate variant needs canonical
   review before native VC03 staging. Mechanical progress does not depend on
   forcing Bunny to disengage/re-engage a safe gate.
3. **P04 control ownership.** The campaign adapter must execute the requested
   P04 helper action and return observed state. This isolated module cannot
   mutate P04 by itself. Request emission is not acknowledgment of real success.
4. **Native caption pages.** Whole-record receipt means all pages were visible;
   partial speech-unit receipts remain exact. Pagination of non-speech records
   is outside the domain ledger. Never acknowledge a record merely because its
   first page opened or its audio stopped.

## Proposed native IDs, not reservations

The parent recorded 410–429 as a P10/P11 proposal, explicitly not allocated;
this task did not edit the registry. Its rechecked hash is
`8edd498090c4d14ea4f5e8c547d3cb18cd1070148c06b6f7f88ac985653f2d71`, with no
different owner's range overlapping. P10 proposes 410–414. This module proposes:

| Proposal | Fixed control/position |
| --- | --- |
| 415 | `display_wing` |
| 416 | `wing_catch` |
| 417 | `display_handle` |
| 418 | `staging_pocket` |

419–429 stay unassigned. Existing display/cart/gate IDs are reused. No registry,
script/selector, view, text or audio number was allocated, and packaged manifests
must be rechecked before any native use.

## Focused verification

`python -m unittest discover -s tests -p test_p11_model.py -v`

The 32 focused tests exercise actual P09/P10 branch completion in both orders,
both helper orders, pre-engaged and subsequently released pegs,
actual opposite-side reach, safety before text, all seven sincere-prefix save
points, interrupted concern, menu/travel recovery, retries, stale caption/peg/
contest callbacks, muted caption completion, single-fire LAF11, malformed saves,
no premature later reward, every verb's bounded fallback, and canonical metadata.
A bounded gameplay-state graph explores ten actions including outside peg state
changes; every reached physical/progress state has a route to safe staging and
VC03 eligibility. No native execution, art, timing or listening proof is claimed.
