# P14: Put the Promises in Writing and Present the Finale

## Scope, exact wording and source provenance

`cakood/p14_model.py` models the final commitments, a post-completion ending
sequence, full canonical credit records and a detached menu credit replay.
It is standard-library domain logic, with no native runtime or media playback.
`tests/fixtures/p14/canonical-bindings.json` freezes full revision-3 source
records, speech units/speakers, hashes and obligations. Catalog SHA-256:
`1226a97873a3693867c08afe2731ddb55adef6f0eaeabc1222e103c04c0d9fa7`.
No player-facing text is invented: every result has empty `text` and only exact
canonical record IDs. Machine statuses are never captions.

The approved current `P14.ENDING.002.02` is Jackie's line, “Put ‘It’s a meal’
underneath. In very large letters.” Parent/writer provenance review confirmed
this was the intentional accepted V2 rewrite and remains the current V3 binding.
Do not restore the superseded bigger-pencil line from an older GDD quotation.
The simultaneous reach for the same pencil, audience glance, LAF14 and subsequent
freeze-frame/full credits remain the presentation contract. This module changes
neither source catalog nor GDD.

## Final gate: all tasks and four real wins

`start` requires the full earlier canonical task set, from safe entry and the
agreed plan through every preparation, P08's genuinely started evening, P09/P10,
P11's safe rescue, P12's repaired rack/truthful introduction, and P13's served
meal, reveal and toast. It checks the actual `VerbalContests` owner and all four
latched wins, not a caller's `ALL_VC_WON` string. It snapshots the actual winning
outcome IDs. A concluded loss may have enabled earlier practical progress but
cannot pass this gate. A later loss does not erase a real earlier win; restoring
an older timeline does not merge in wins from another one.

`notebook_gate` lists each missing contest, its opponent and canonical rematch
room. It neither closes exploration nor grants a win. VC03/VC04 safety, learning,
result presentation and rematches remain with their existing owners.

The physical pledge board must already be in L05. The original P09 card must be
present, unsigned, undated and owned for signature by P14. The host provides the
previously selected in-fiction repair date, plus P06's existing Vivian tone.
No real calendar entry, new romance choice or guaranteed booking is created.
The date/tone snapshot does not change on later rendering callbacks.

## Individual consent, inventory and completion

`start` creates exactly eight named pledge-card identities. Their fixed
commitments are the canonical `P14.CARD.*` records. Each seven-nonplayer card is
given to its actual named contributor; Jackie confirms his own cooking/cleanup
card. Only the exact visibly presented `P14.APPROVE.*` line records approval.
A queued line, a hint, a wrong card, an absent speaker or an audio callback cannot
approve anything. Wrong assignments use the recipient's canonical correction
and preserve prior approvals. Pinned cards leave inventory once and cannot be
duplicated by repeated action or reload.

After all eight approved cards are pinned, Stringer's whole
`P14.DIALOGUE.003` scene must be presented. It states concrete conduct-based
terms and privacy boundaries. `pin_signature` then transfers the original P09
card onto the board, signed by Stringer. Forge/coerce attempts use the authored
refusal and change nothing. Consent is not inferred from a contest result.

Give the original grease pencil to the actual Frankie. The host temporarily
removes it from pocket inventory. Read her date announcement, the whole dated
card readback with the selected `{repair_date}`, and the pencil-return line in
that order. `complete_commitments` then returns the same pencil and sets both
`COMMITMENTS_SIGNED` and `GAME_COMPLETE`, once, before the finale begins.
Repeated completion is quiet. A pending readback or missing final return receipt
cannot complete the game. `validate_context` catches a signed card or borrowed
pencil simultaneously present in external inventory.

The eight individual pledge cards remain on the board. The signed P09 terms
card is a distinct original object, never a ninth fabricated pledge. P02/P09
owners retain historical records; host ownership transfers must be atomic with
this branch save and must stop their old inventory projections from being used.

## Post-completion ending and credits

`start_finale` requires legitimate completed commitments. The normal sequence is:

1. Vivian's exact existing professional/friendly/cautiously romantic closing
2. `P14.ENDING.001`, the sincere unposed meal; no laugh event can fire here
3. The quiet L01 tag, `P14.ENDING.002`, with the original shared-pencil action
4. An explicitly rendered happy freeze-frame; one optional cleared celebration
5. Every ordered `END.CREDIT.*` block, then selected actual asset acknowledgments

The host stages the change to L01 and supplies actual speaker positions. Every
pending speech unit remains caption-addressable. A source is advanced only once
all its text was displayed; non-speech credit pages must all be visible before
whole-record receipt. LAF14 can be consumed once only after the complete separate
tag punchline. The freeze uses `END.FREEZE` as stage-direction metadata, not a
spoken caption. Its epoch-bound visible-frame receipt must precede celebration.

`claim_celebration` emits only a logical, single-consumption presentation event.
The host must select cleared final audio and obey one PCM owner: one composite
or serial laugh/cheer/applause cues. The credits' extended household-theme reprise
and single-lane playback remain native production work. The domain never claims
that audio actually played or that assets have been cleared merely because an
event was returned.

Pause, resume, skip and silent completion preserve gameplay and all consent.
A paused viewer refuses new text receipts/advances. Skip drops transient media
and ends the viewer without granting or revoking anything. Saves persist exact
scene, caption prefix, credit cursor, pause state, consumed laughter/celebration
and selected credit records. Reload never auto-plays an event.

## Credits selection and release limits

`CREDIT_ORDER` contains the full current fictional/actual credit roll, including
Shael Riley's exact actual credit wording, dot/OpenAI acknowledgment, all eight
fictional AI writers and the exact fictional “Music by Haru Suno” credit.
`start_finale(shipped_source_urls=...)` selects `END.ASSET.*` acknowledgments only
for explicitly supplied, recognized shipped sources. Audition candidates are
not included by default. Unknown sources raise a clear error rather than hiding
missing credits. URLs, adaptation wording and author/license details remain in
the original full record; no truncation or invented credit text is allowed.

This selection is not a final release audit. Production still must reconcile
all shipped assets/dependencies, runtime, compiler, font, soundfont and source
music notices against the final package. The script's `END.PRODUCTION.*` records
are production instructions, not player captions, so they are intentionally not
placed in the roll. Actual additional required notices need authored/verified
bindings before release. Native typography and lossless URL wrapping remain
unproven here.

## Replay and saves

`create_credit_replay(invoking_session)` makes a separate completed presentation
copy and a deep JSON copy of the invoking save. It replays credits only, without
repeating story, consent, physical transfers, LAF14 or rewards. The originating
world is unchanged. The invoking save can even be an unfinished evening with
no wins; returning never merges in the completed source world's progress.
`CreditReplay.save/load` preserves both timelines, viewer position and pause.
Closing/cancelling or finishing returns the invoking JSON session by value.
Mutating the returned object cannot alter a subsequent return.

The main envelope is `cakood-p14-branch`, schema 1; replay uses
`cakood-credit-replay`, schema 1. Strict loading rejects malformed ledgers,
missing gate evidence, pins before approval, premature signatures/readbacks,
normal credits before the visible freeze, invented credit IDs and cursors beyond
displayed text. This is structural validation, not cryptographic save security.
External context validation additionally verifies the stored winning outcomes
against the supplied contest timeline. Old caption/freeze handles are invalid
after restore or cancellation.

## Proposed identities and verification

Registry hash at inspection:
`d3b646fe027af35c569215ece6f7a6e3519a43341f9715dd367f99995959587c`.
Propose objects 435–442 for the eight cards in `PEOPLE` order: Jackie, Bunny,
Frankie, Milo, Vivian, Rita, Felix, Stringer. Reuse P02's pencil, P09's terms card
and P13's board. These numbers are proposals only; no registry, native script,
selector, view, text or audio allocation was made.

Run `python -m unittest discover -s tests -p test_late_campaign_models.py -v`.
The exhaustive approval/pin graph checks all 6,561 valid per-person states and
34,992 actual action transitions. Additional tests cover every missing task or
win, later losses, old timelines, all signature prefixes, date/readback ordering,
three closing variants, every finale phase, every canonical credit record,
manifest selection, stale callbacks, replay isolation and malformed saves.
Real P07/P09/P10/P11 handoffs are exercised for both cue materials. These are
engine-independent proofs; native presentation, sound, input, deployment and
full final-package acceptance remain separate.
