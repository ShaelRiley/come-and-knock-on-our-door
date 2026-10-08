# P14 reference correction R2: targeted ACCEPT

Date: 2026-10-07. This review accepts the P14-REF-001 correction and the current source/reference boundary under the limits below. It is not emitted-bytecode, native-game, production atomic-save, rendering, audio or full-game acceptance.

## Outcome

R2 rejects the exact genuine mixed-branch save that version 1 accepted. The unchanged independent strong reproduction was executed against both versions in normal and optimized Python. Version 1 still accepts the wrong ledger and fails the expected-rejection assertion. R2 rejects it before P14 admission with `Owner-side commit witness does not match the paired observed history`.

Both histories start from the same paired prefix. Branch A wins VC01 at A1, then loses twice. Branch B loses at A1, wins at A2, then loses. Both subsequently win VC02–VC04. One public logical outcome-effect claim on B makes the final raw owner saves byte-identical at revision 390. Their raw SHA-256 remains `b133d5a68077dfab4c321a7241a18162ac6f11a54658337095126897360b69c0`. The actual observations and genuine first-winning ordinals remain different.

R2's saved owner-side witnesses distinguish those otherwise identical raw owner blobs:

- Branch A: count 6, head `ad6733ebf103e31b91a1f4496992009673e0b56e59b47e848b2e7c5460ffd6fc`
- Branch B: count 6, head `129c13fcd30febdcafc4ea39fc244d87e6c3ef3fa0bfe0c2541f1a7c9947dbaa`

The original scripts were not edited. Their retained hardcoded report label says “P14 reference v1” even when invoked with R2; `evidence/unchanged-reviewer-reruns.json` records the actual candidate, script hash, mode and expected result. The R2 runs save complete genuine A/B pairs and the rejected mixed pair under `evidence/r2-strong-normal/` and `evidence/r2-strong-optimized/`.

## Why the correction closes P14-REF-001

The facade stores an immutable count/head witness on the actual owner instance. It evolves the head from the prior owner-held witness and the actual successful outcome snapshot. A fresh outcome changes the witness; lessons, result reading, effect consumption, repeated rejected callbacks and other non-outcome operations do not. The pre-transaction binding check compares the existing observation list with that retained witness and does not adopt or reseal a substituted list.

The accepted owner's transaction, subsequent observation/witness update and paired-save snapshot share the same reentrant lock. Independent tests demonstrate a save waiting while an outcome's persistence callback is blocked; the resulting pair contains both the completed owner outcome and its witness/observation. Supplied tests separately stop immediately after the accepted owner commit and before observation capture, proving the paired snapshot also waits across that interval.

Schema 2 preserves the accepted raw owner payload/checksum and adds `reference_commit_witness` to the composite owner record. Loading checks the independent stored witness against the separate observations, then applies the existing complete-history, chronology, current-state and retained-learning validation. This is the needed saved pairing distinction rather than a hash of the final aggregate owner bytes or a constant lineage label.

Paired restore first validates a disposable candidate. Invalid pairing, malformed raw input and invalid or stale restore generations leave the live state, generation, witness, observations and transient suppression unchanged. Successful same-pair restores preserve exact first-win identities and by-value isolation. Later genuine losses evolve the witness while preserving earlier earned wins, learning and P14's first-win receipts.

Raw load/restore explicitly detaches unsupported evidence. It preserves the accepted owner's earned WON flags and knowledge. Subsequent raw-owner gameplay does not silently manufacture the missing history. Repeated P14 admission attempts then reject without changing the P14 world. Unwitnessed schema-1 envelopes are deliberately unsupported rather than upgraded by inventing a historical witness.

The paired file writer atomically replaces one reference JSON envelope using the accepted temporary-file/fsync/replace implementation. Both supplied replacement failure and independent pre-replacement fsync failure preserve the previous valid file. The accepted raw `_persist` hook continues to store raw owner data only; the correction does not turn it into a paired-history transaction hook.

## Independently completed checks

- Fresh candidate Library readback: version 2, 2,828,906 bytes, 419 ZIP members, SHA-256 `e225ea5f2ba113a12b3cc8b84c3c56fad4778b95a08a717910e9bf12f7227cb1`. Every payload member equals the frozen R2 producer. The supplied package manifest verifies its 418 listed entries.
- Exact unchanged strong reproduction and all ten original independent tests executed against v1 and R2 in both Python modes. The v1 wrong-ledger failure remains reproduced; all ten tests and the expected rejection pass on R2.
- All 43 focused supplied source tests pass independently in normal and optimized Python: 14 retained domain tests, six relevant retained validation/replay tests, 13 current-flow tests and ten pairing tests. Assertion preservation remains active under optimization.
- Seven new independent R2 tests pass in both modes: failed raw restore; failed paired restore/generation; successful raw restore followed by a later real loss without synthetic evidence or lost wins; by-value paired load/restore plus later-loss first-win preservation; non-outcome witness stability; file fsync failure preserving the previous pair; and save waiting through the accepted owner persistence/commit boundary.
- The 32 supplied missing/altered-input admission probes all reject before tests.
- In a fresh directory containing spaces, the fixture, generated SCI, manifest and object bindings were deleted and regenerated. All four outputs match exactly. Test admission succeeds there, and all 17 independent tests pass again in normal and optimized Python. The full 43-test suite was independently run in the primary extracted directory; a second full run after relocation is not claimed.
- Independent byte comparisons prove the accepted contest owner, P14 model, exact canonical fixture, final codec, retained SCI method template, generated SCI, manifest and object bindings are unchanged from v1. The supplied guarded source admission confirms all 77 retained method bodies, 669 properties, 642 persisted words and 202 serials.
- All 1,265 v1 producer files remain unchanged from the original rejection review. All 1,453 frozen R2 producer files remain unchanged throughout this targeted review.

The 6,561-projection and 1,485-vector long matrices were not rerun in this targeted correction review. No new result is attributed to them. The original v0 independent REJECT report, exact failure evidence and ZIP are preserved intact under `prior-review-v0/`; this targeted ACCEPT supersedes that verdict only for candidate version 2.

## Preservation and remaining limits

The model's original evidence-before-entry-mutation correction remains the only P14 model delta from the literal recovered source. There are no new P14 transition, consent, prose, credit-selection or finite-layout changes in R2. The 125 canonical records, 43 speech units, eight writer blocks, 26 mandatory credits and 33 conditional asset acknowledgments are retained, and their existing exactness/current-flow checks pass. All four actual WON flags, eight individual approvals and unique cards, the complete five-unit consent scene plus explicit signature, original terms card, agreed in-fiction date, original pencil handoff/readback/return, all three closing tones, finale meal/tag/freeze/credits and detached parallel viewers remain covered by the passing focused tests.

The P09 original unsigned card is genuinely earned while its separate success caption remains pending. P05/P06/tray/entry facts remain accepted upstream inputs. Notebook rematch hints for VC01–VC03 still disagree with actual post-P13 actor locations; this remains a host-routing boundary, and actors were not teleported. No win substitutes for consent.

The witness is an ordinary consistency checksum, not authentication or tamper-proof provenance. The Python lock and atomic reference JSON file establish only this reference behavior. Production native owner/ledger atomic persistence, cross-owner ownership and rollback, current-ABI host integration, actual rematch-room admission, native saves and replay heaps, rendering/credit layout, sound, shipped-asset clearance, controller/accessibility behavior and full-game ScummVM acceptance remain separate open gates. No browser, native game/save, GitHub or frozen producer was modified or launched.

## Reproduce

Extract `input/CaKoOD-P14-Reference-Reconstruction-20261007.zip` into a disposable directory. The accepted component is the extracted `p14-reference-reconstruction/component`.

```
python3 tests/reproduce_mixed_branch.py --component /path/p14-reference-reconstruction/component --output repro
python3 tests/test_independent.py --component /path/p14-reference-reconstruction/component --results original-tests.json
python3 tests/test_r2_independent.py --component /path/p14-reference-reconstruction/component --results r2-tests.json
python3 /path/p14-reference-reconstruction/component/tools/run_tests.py --focused-pairing
python3 -O /path/p14-reference-reconstruction/component/tools/run_tests.py --focused-pairing
```

All five commands pass against the reviewed R2 candidate. The first command passes by rejecting the mixed branch before P14 starts.
