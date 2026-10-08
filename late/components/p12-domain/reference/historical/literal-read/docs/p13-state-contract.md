# P13: Send Everything through the Right Door

## Scope and canonical lock

`cakood/p13_model.py` is an isolated domain model using standard Python, the
existing gate/contest owners and P12's shared visible-caption ledger. The exact
revision-3 script bindings and attribution are in
`tests/fixtures/p13/canonical-bindings.json`; its supporting P08 label records
provide exact blocked-place names. Catalog SHA-256:
`1226a97873a3693867c08afe2731ddb55adef6f0eaeabc1222e103c04c0d9fa7`.
All player text is returned by canonical record ID. Machine statuses and preview
identifiers are not dialogue. No script or GDD text has been edited.

## Campaign and object handoffs

`P13Context` carries actual actors, current PA, the P04 `GateHandoff`, current
P08 furniture conditions, queue state, board location and the actual
`VerbalContests` instance. Starting also requires P12's completed cleanup and
collection-point handoff, exposed as `welcome_cleared`. `INTRODUCTION_CLEAR`
alone must not skip the shared confetti/departure presentation.

`start` accepts the original P07 `pot_handoff` and safe P11 `display_handoff`.
The pot must be lidded and contain eight tasting portions, including Jackie's.
The existing cart/display must be folded, padded, covered, undamaged and safely
staged in L04. P11 conveys no Rita reveal consent. The emitted ownership event
transfers those exact identities to P13; it never creates replacement inventory.
Older P07/P11 projections become historical. Host ownership and this save must
change atomically, before another branch can act on the objects.

P13 creates the canonical guest-program card once, and places the blank pledge
board in L01. `inventory` contains only the program until Milo receives it. The
pot, cart, display and board are world objects, not pocket copies. The host must
apply movement events to actual actors and the board before supplying the next
context. `validate_context` rejects duplicate ownership and an undelivered board
projection after delivery.

## Turn-based routing and consent

The `preview` source is a visible canonical cue reader. `route_preview` separately
returns the three route identities, load/destination IDs, known width-fit facts
and current occupied-lane markers. It includes no countdown. Actual hotspot
geometry and measured sprite width remain a native-art responsibility; the
model does not invent pixel measurements. `blocked_layout_binding` supplies the
specific approved P08 label for the authored `{blocked_place_name}` slot.

- **Guests:** At L03, give the program to the actual Milo. `P13_GUEST_ROUTE`
  directs the house/rear-arch route. `confirm_seating` requires the observed
  clear queue and Milo's actual arrival at L05. It does not infer seating from
  a queued line or clock.
- **SERVE:** Jackie and Bunny at L02 pass the original pot through the hatch.
  Frankie must actually be at L05; buffet/hatch placement must currently be
  valid. Food moves directly to the buffet. Pulling SERVE afterward commits
  `SERVED`. No food travels through the audience seating.
- **SHOW:** Only after serving, ask Rita at L05. Her exact ready-to-reveal
  sentence must be visibly read; querying, queueing or audio completion does
  not grant consent. At L04, Felix and Vivian then transport the existing
  display/cart through the currently engaged, tested P04 peg and clear lane.
  P13 never changes the peg itself. The alcove and screening must be ready.
  Only after arrival and Rita's consent/presence can the screen's viewing side
  open. Read her whole presentation, then pull SHOW to set `DISPLAY_REVEALED`.
- **TOAST:** After SHOW, Frankie takes the original board from L01 through the
  clear house route. The host projects the board and Frankie at L05. `SERVED`,
  `DISPLAY_REVEALED` and physical board delivery make VC04 eligible. Its actual
  resolved result, after exit, permits a working-microphone attention call.
  Read the whole attention line, then pull TOAST to set `TOAST_READY`.

A concluded VC04 loss permits practical completion. Winning is P14's separate
requirement. `request_contest` emits an epoch-bound request; cancellation or
acknowledgment clears only that request. It does not introduce or score an
attempt, grant resolution, set wins, rewrite a signature, change consent or
alter completed deliveries. A rematch uses `VC04.REMATCH` and remains available.

## Safe failures, current furniture and checkpoints

Wrong routes retain the original load and every completed delivery. The first
canonical wrong-route class can queue one scripted visual. LAF13 additionally
requires its displayed caption and an explicit acknowledgment that the harmless
visual actually rendered. Merely making a mistake or stopping speech cannot
trigger laughter. Repeated retries remain quiet. Other unsupported routes use
existing route readers, without pretending a side-gate attempt was a hatch gag.

Before delivery the host may move furniture through P08 and then reproject the
new conditions. A newly blocked place prevents that delivery. After food
arrives, the occupied buffet/service/slate are protected; after the display
arrives, its screen is protected. `protect_furniture` reports the existing
in-world refusal. P13 does not become another furniture owner.

Each completed cue emits `P13_AUTOSAVE_REQUEST`. Requests remain durable until
the host confirms a real successful save. `pending_autosaves` survives reload
with fresh request handles; stale receipts do nothing. An emitted request is
not a claim that storage succeeded. Checkpoint failure does not undo a served
meal, completed reveal or toast. Host retries the real save independently.

## Save and presentation protocol

Envelope `cakood-p13-branch`, schema 1. Persist the branch, gate, PA, actor/layout
positions, inventory/ownership and contest owner together. Pending captions keep
their exact contiguous speech prefix. Restore rotates runtime callback epochs
for captions, VC04 requests, wrong-visual receipts and autosave requests.
Pause/menu/mute/voice completion do not perform deliveries or authorize Rita's
reveal. Native adapters acknowledge an entire non-speech record only after all
pages have been visible. Events describe committed logical actions, not proof
that an animation or sound played.

## Proposed IDs and evidence

The registry hash at final recheck is
`d3b646fe027af35c569215ece6f7a6e3519a43341f9715dd367f99995959587c`.
Propose objects 432 `guest_program_card`, 433 `pledge_board` and 434
`screen_pull_tab`. Reuse the existing pot, screen, cart, display, gate and cue
identities. Proposals only: no registry or native resource was allocated.

The focused late-campaign tests cover the actual P07/P11 handoffs, real actor
locations, each prerequisite and route order, all reveal-prefix save points,
consent barriers, current peg/layout/microphone changes, safe VC04 loss/rematch,
three durable autosaves, protected occupied furniture and stale callbacks. The
bounded route-state graph tries all premature operations and proves recovery to
TOAST from every reached state. Passing these tests is not native playability,
art, animation, controller or audio acceptance.
