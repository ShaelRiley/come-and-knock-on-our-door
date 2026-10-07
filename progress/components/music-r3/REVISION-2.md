# Revision 2: three bounded independent review corrections

The preceding archive is retained unchanged under `inputs/revision1/source.zip`, SHA256 `eefb7b1748d1fa4e0c2ea0b4feed4a967b9b2c83b3c17c3acca2e4dcb44abd80`. It is a superseded source/emitted candidate whose independent verdict was REVISE. Exact review scripts, receipts and counterexamples are pinned under `inputs/independent-review/`. Independently rerunning the two emitted host scripts and the empty-probe packaging mutation on an isolated extraction reproduced all three findings; those terminal results are pinned under `inputs/revision1/reproduced/`.

## 1. Honest emitted Main status and keyboard retry

`rbAvailable` remains a strict ready-at-target predicate. It is no longer misused as the host failure predicate. The additive broker exposes UI states: 0 intentionally inactive, 1 healthy current owner, 2 healthy family request pending, 3 connector running, 4 startup/recovery or frozen lifecycle, 5 a genuinely retryable inherited transport failure, 6 a non-retryable failure. Healthy pending and connector phases clear Main.musicUnavailable and render their own concise status. The inactive admission leaves the original Main music lane and footer untouched.

The guarded Main render hook delegates the active footer to broker943. Its five strings are freshly read from the allocated Text247, into a cleared presentation buffer. No string or presentation-cache value grants ownership or validates static state. A retryable failure displays `MUSIC UNAVAILABLE. R TO RETRY.`; a fatal failure displays `MUSIC UNAVAILABLE.` without an ineffective invitation. The actual Main R keyboard route invokes a freshly validated inherited retryRejoin on the current Sound/parser. It neither starts a second player nor resets an exhausted generation. Pending and connector states return false from retry and never invite it. Main is dirtied when the presentation state changes.

Regression tests execute ordinary emitted Main.audioPoll, Main.render and Main.input against a coherent full P05 source compile. The retained genuine font0 is pinned for the emitted renderer. Display/Sound kernels remain explicit typed mocks: this is emitted UI/control-flow evidence, not native rendering or listening proof.

## 2. Exhausted generation is sticky through later work

Once advancing the two 15-bit generation limbs fails at [32767,32767], broker error9 latches. Further requests, including an equal-target coalescing request, cannot authorize work. Every later bed poll continues the current clock and user controls but cannot retire the bed at an aperture. The second-read handoff check rejects an exhaustion that occurred within the position-read interval. A connector already in flight may complete at its real end; it is then retired without starting its old target. No wait, immediate tail erasure or new native owner is introduced.

The final successfully issued generation [32767,32767] remains valid until a subsequent advance fails; the value alone is not an error. A runtime retry cannot clear the exhausted state. Fresh init/fully admitted saved-state behavior retains existing guards. Context invalidation follow-through was already correct and is not redesigned.

## 3. Exact negative-probe membership and result admission

`REQUIRED-GUARDS.json` fixes the 23 primary identities. Packaging validates the exact nonempty set, uniqueness, actual count, PASS_REJECTED result, useful error and terminal/exit evidence, and exact real unittest outcome vectors for the six outcome probes. Count, a matching receipt hash and vacuous all() no longer suffice.

`REQUIRED-PACKAGING-GUARDS.json` fixes seven actual package-subprocess rejection probes: empty, duplicate, missing or substituted identities; bad result; inconsistent count; stale receipt. Every probe starts from the freshly passing bound primary report. Each must fail for its specific primary-proof defect before it can reach a missing secondary proof. Packaging requires both complete reports bound to the current aggregate receipt, exact verified-files manifest and respective fixed identity manifest.

## Preservation and remaining scope

No MIDI or native Sound input is edited. Scripts941/942 and all source-derived note-off/timing data remain byte-identical to revision1. Changes are confined to broker943, its Text247 UI suffix, guarded Main adapter and proof tooling/tests/documentation. Original940/243 and all protected host modules/resources retain their pins. The full R1 set of 52 tests is retained, with 17 additional revision-2 tests. The final current P06/P07 composition is a separate gate; this packet still uses its explicitly pinned P05 and P06-candidate1 plus inventory-R2 fixtures. No native launch, listening acceptance, activation or publication is implied.
