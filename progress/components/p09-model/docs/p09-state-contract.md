# P09: Ask What Is Actually Leaving

## Scope and canonical lock

`cakood/p09_model.py` is an engine-independent branch using the existing `Verb`,
`Event`, `Result`, and seven-room registry. It implements the short chair
investigation and grants an unsigned renewal-and-repair card. It does not
implement an eviction clock, persuasion meter, legal simulation, actual
signature, future promise approval, or game completion.

Mechanics follow the current GDD, especially lines 175–182, its world/NPC
schedule, dependency graph, knowledge rules, and inventory lifecycle. Words
come from complete player-script editorial revision 3. The fixture at
`tests/fixtures/p09/canonical-bindings.json` records all 20 P09 record IDs,
record text hashes, obligations, all 20 speech units with speaker/laugh metadata,
and source-file hashes. No player prose is copied into the model: `text` is
empty and machine result codes must never be displayed as dialogue.

- GDD: <https://docs.google.com/document/d/1D-tndxod3dJNOVANuA1e1c-Zm8Im6sew9qhuzm09vLU/edit>
- Complete script: <https://docs.google.com/document/d/1HpiFbCn7FniV3kLjTDP5nP1Ow0N5JMHuEeO0EeG1rEQ/edit>
- Catalog SHA-256: `1226a97873a3693867c08afe2731ddb55adef6f0eaeabc1222e103c04c0d9fa7`

No canonical source, native resource, registry, art, music, executable, or
installation is changed by this work. Passing these domain tests is not native
playability, build, visual, sound, or stock-ScummVM acceptance evidence.

## Campaign ownership

`P09Context` is frozen and supplies:

- `room`, `on_apron`, external `flags` and external `inventory`
- Actual `stringer_room` and `rita_room`, both initially L07 per the P08 schedule
- `conservatory_view`, either `side` or `front`, within the existing L07 screen
- `contest_active`, which protects an active contest from new scene actions

The caller owns travel, NPC movement, audience-apron state, viewpoint changes,
global flags, and outside inventory. A front/side viewpoint is not a room,
shortcut, or second campaign map. To honor the front-listening route, the host
walks Jackie to the conservatory-front hotspot, supplies `front`, and invokes
`hear_front_context`. The branch never teleports a character. Actual relevant
speaker presence is checked again at the presentation acknowledgment barrier.

All P09 source actions require caller flag `EVENING_STARTED`. Terms additionally
require `PLAN_AGREED`. P09 does not demand P10 or a contest win, and produces
neither P10 nor later puzzle flags. An agreed plan is durable caller knowledge;
holding, giving, or reopening a physical plan is not another requirement.

P09 owns only its generated card, stable object ID `renewal_repair_card`.
`world.inventory` projects either nothing or this one object. Caller inventory
must exclude the P09 card and all P09 fixed objects/NPCs. This follows the prior
branch model convention and prevents duplicate ownership within a context.

When `P09_TERMS` is emitted, `terms_card_handoff` describes the grant:

```json
{
  "object_id": "renewal_repair_card",
  "location": "inventory",
  "signed": false,
  "repair_date": null,
  "signature_owner": "P14",
  "terms_record_id": "P09.READ.002"
}
```

The host identifies the one grant by event ID and persisted serial. It uses
P09's projection until P14 explicitly takes ownership, then retires that old
projection. It must not replay P09's grant to duplicate a card or replace P14's
later signed state with an unsigned copy. P14 transport, signatures, dates,
approvals, and completion are outside this module; the handoff does not claim
those systems exist yet.

## Fair investigation routes

All four supported routes use the same `RUMOR_CLEARED` reward. Nothing requires
the opening fragment, reading the ambiguous tag, picking up an object, or
visiting the routes in a particular order.

| Action | Exact presentation | Earliest acknowledged correction |
| --- | --- | --- |
| `inspect_chairs` | `P09.LOOK.001` | Whole record or `.01` speech unit |
| `ask_three_things` | `P09.DIALOGUE.001` | Its `.01` speech unit |
| `hear_front_context` | `P09.DIALOGUE.001` | Its `.01` speech unit, at caller's front view |
| `accuse` | `P09.FAILURE.001` | Stringer's `.01` speech unit |

The canonical `P09.LOOK.001` obligation explicitly permits observation itself
to clear the misunderstanding. Therefore chair inspection remains valid with
both NPCs elsewhere, and does not silently require the subsequent conversation.
The direct and front-context record's trigger explicitly names these routes;
the model does not invent a new front-context line.

The full accusation record contains Rita's second line. If she is absent when
the scene starts, the branch queues only canonical unit `P09.FAILURE.001.01`.
That exact Stringer correction clears the rumor without a relationship penalty.
The full record cannot be acknowledged for this restricted variant. If both
were present when queued but Rita later leaves, Stringer's first unit can still
be acknowledged; her remaining line waits for her actual presence.

`P09.READ.001` is the ambiguous tag, and `P09.OPEN.001` is the incomplete
overheard exchange. Neither clears the rumor. Hints also grant no knowledge.
Refusing to burn, hide, or take the chair tag uses `P09.FAILURE.002` and consumes
nothing. The chair/tag remain fixtures.

Chair identification does not automatically reveal anybody's private wishes.
`class_context_known` requires an acknowledged exact class-space statement:
`P09.DIALOGUE.001.01` or `P09.FAILURE.001.02`. `connect_shared_wish` uses canonical
choice `P09.CHOICE.004` and dialogue `P09.DIALOGUE.003` only when that context is
known and both Stringers are present. Its one-shot event is optional and never
gates terms or card delivery. It works before or after the terms conversation.

The audience has no P09 canonical disclosure. Querying or talking to it returns
no clue records, no speech units, and no knowledge events. Presence beyond a
scenic edge does not turn the audience into private witnesses.

## Presentation and knowledge barrier

`look`, `topics`, `journal_records`, `journal_units`, `object_location`,
`reachable`, and `resume_presentation` are pure queries. Looking up the correct
record is not evidence that a player saw it.

The host starts an actionable scene/read with the named helper or
`begin_presentation(context, source)`. It saves a unique presentation identity
and returns the exact next canonical record, or the remaining exact units of
an interrupted/restricted record. Repeating a pending request returns the same
identity and does not create another action or reward. Multiple interrupted
sources may coexist, so a pending joke cannot block a fair alternative route.

After text is successfully visible, the host calls:

```python
world.acknowledge_presentation(context, presentation_id,
                               record_id="P09.DIALOGUE.001")
# Or after presenting a precise contiguous portion:
world.acknowledge_presentation(context, presentation_id,
                               speech_unit_ids=("P09.DIALOGUE.001.01",))
```

Exactly one of those forms is accepted. Record identity, source membership,
ordered speech-unit prefix, physical reachability, actual speakers, and story
prerequisites are checked. A selected choice, hint, guessed ID, arbitrary text,
another puzzle's record, or a later out-of-order unit is not an acknowledgment.

The host's render barrier is a trust boundary: this engine-independent model
cannot inspect pixels. Muted captions count; skipped audio after visible text
counts. Queued text, an unseen/cancelled page, or unopened notebook does not.
Only whole successfully presented text permits a whole-record acknowledgment.

Each successfully acknowledged token has a durable action serial. Duplicate
receipts are idempotent. A full-record receipt can finish an already presented
prefix without repeating its knowledge reward. The notebook returns a whole
record only when every token of that record is acknowledged; partial or
Stringer-only receipts expose only their exact recorded units.

The rumor flag commits on the first actual correction, not after subsequent
jokes. Those remaining units stay pending and may be resumed without granting
another flag. A repeated completed direct question returns the already-known
exact short correction `P09.DIALOGUE.001.01` with no state change. An interrupted
old opening fragment is suppressed once the rumor is corrected.

## Terms and interruption recovery

`discuss_terms` requires an acknowledged correction, the agreed plan, and
Stringer physically present at L07. All five units of `P09.DIALOGUE.002` must
be presented before `TERMS_CARD_AVAILABLE` commits. This preserves the entire
conduct-based agreement: household care, agreed guests/noise, responsible use,
renewal commitment, and Stringer's funded/scheduled repair. No partial demand,
choice label, inventory description, or hint awards the card.

The card grants atomically on that complete-dialogue receipt, once. The same
presentation then retains `P09.SUCCESS.001` as a pending outcome. Saving, leaving
the room, resuming, or canceling audio at this point does not remove the card,
regrant it, or require another agreement. The self-spoken success caption can
resume on the ordinary set in another room without conjuring Stringer there.
It cannot be acknowledged in the same operation as the as-yet-uncommitted terms.

The card remains unsigned, with no chosen repair date. `Open` can queue its
canonical reader `P09.READ.002`; pure Look supplies `P09.LOOK.002` and that reader
without adding notebook evidence. P09 refuses using the card as craft material,
forging it with the pencil, giving it as an early signature, or consuming it.
No action sets `COMMITMENTS_SIGNED`, `GAME_COMPLETE`, or a contest flag.

`hint` remembers the requested hint level but never changes knowledge or grants
an item. Native audio/laugh output must obey the canonical speech metadata;
this module creates no extra laugh cue and no laughter-based state transition.

## Save validation

Save envelope: `kind = cakood-p09-branch`, `schema = 1`. State contains only
branch flags, presentation receipts, consumed one-shot serials, revision, and
hint level. A presentation has a start serial, fixed canonical variant, and
ordered per-token receipt map. Exact expected words/units are derived from
code bindings and cannot be supplied as custom save content.

Loading rejects unknown/missing envelope or state fields, boolean numeric
serials, duplicate or future flags, unknown presentation variants, non-prefix
or backward receipts, unrelated actions sharing serials, mismatched reward
ledgers, terms started before a rumor correction, a card reader before a grant,
shared-wish scenes without earlier class evidence, and completion outcomes
acknowledged before the card grant. `load(..., context=context)` additionally
validates the P08 evening handoff, agreed plan where needed, and any aggregate
P09 flags supplied by the host. Room/apron changes do not erase valid receipts.

This validates causal branch structure, not cryptographic save authenticity.
The host remains responsible for saving its own room, viewpoint, global state,
outside inventory, NPC positions, and later ownership transfers consistently.

## Proposed future native IDs

These are proposals only, not allocations, selectors, or imported resources.
The unmodified `docs/native-resource-registry.json` had no numeric/range overlap
with 395–409 when checked. Its SHA-256 was
`314e893b283af706cf0c33d79d1e25d5bc1121593c171499ed3282c17fecb357`.
Existing native manifests and independently typed namespaces must be checked
again before implementation.

| Proposed object ID | Stable object |
| --- | --- |
| 395 | `tagged_chairs` |
| 396 | `chair_tag` |
| 397 | `conservatory_front` |
| 398 | `conservatory_side` |
| 399 | `renewal_repair_card` |
| 400–409 | Unassigned; no new story objects implied |

## Verification

`python -m unittest discover -s tests -p test_p09_model.py -v` covers 36 tests,
including every fair route and all 24 route orders, false/partial/cross-source
receipts, actual NPC positions, front/side and audience boundaries, deferred
outcomes, optional-scene order, card persistence/protection, JSON round trips,
save tampering, and canonical bindings. The module adds no dependency or tool
installation and requires no native runtime to execute these tests.
