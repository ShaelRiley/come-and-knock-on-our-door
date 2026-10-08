# P14-REF-001 correction candidate, revision 2

This revision corrects the new reference observation/save compatibility boundary only. It is ready for targeted review after the gates in STATUS.json finish. It does not grant independent acceptance or any new native, SCI, finite-storage, host, scene, audio or full-game proof.

## Reproduction and preserved rejection

Version 1 accepted a genuine but unrelated first-win history. Both branches restored the same paired prefix, then played VC01 win/loss/loss versus loss/win/loss. One real logical effect claim equalized the final raw owner saves at revision 390, SHA-256 b133d5a68077dfab4c321a7241a18162ac6f11a54658337095126897360b69c0. Aggregate counts, later state and a hash of that final raw owner blob could not distinguish the branches.

All 1,265 files of the original producer remain unchanged. The exact v1 Library archive is included under prior-revisions/v1. The independent rejection report, exact unchanged test/reproduction scripts, common prefix, genuine A/B failing saves and mixed envelope are preserved under review-v1. Fresh execution of the unchanged strong repro fails on v1 in both modes and rejects the mixed pair on R2 in both modes. Its historical hardcoded report label still says “P14 reference v1”; the supplied component path, output directory and exact-script identity record identify which revision was actually exercised.

## Owner-held commit witness

The accepted contest implementation is byte-identical. The reference facade now maintains a frozen count/head witness on the actual owner instance. Each newly observed committed outcome extends the previous owner-held head with the actual validated post-commit snapshot and sequence number. It does not recompute and adopt a new head from whichever observation list happens to be supplied at save time.

Identical restored prefixes retain the same commitment. Different subsequent genuine outcomes evolve to different commitments. A fixed lineage ID is neither used nor relied upon. The SHA-256 chain is an ordinary consistency checksum, not a credential, authentication mechanism or tamper-proof provenance claim.

The witness advances only after the accepted owner's transaction succeeds. Rejected persistence, stale/duplicate result callbacks and non-outcome operations do not advance it. Observations and witness updates share the accepted owner's reentrant lock. Paired save construction uses that same lock, preventing a snapshot between the raw owner commit and its observation/witness update. A focused concurrency test demonstrates this boundary.

The new schema-2 envelope keeps the original raw owner payload/checksum intact and adds reference_commit_witness to the composite owner record. The separate observation list must reproduce that independently stored count/head, then satisfy the existing complete-history, serial, knowledge and current-owner checks. A mixed owner-A/observations-B envelope fails before P14 admission even when the unchanged raw owner save bytes coincide.

Raw owner save()/load()/restore() retain their accepted data and outcome semantics. Raw loads/restores intentionally detach reference evidence: earned WON flags and learning remain intact, while P14 admission rejects the unsupported missing witness without partial mutation. An unwitnessed v1 paired envelope is also explicitly unsupported; R2 never manufactures a historical witness to upgrade it.

## Save and restore interface

- save_with_evidence() returns one locked by-value schema-2 snapshot
- load_with_evidence() validates the complete composite owner and ledger in a disposable owner before returning it
- restore_with_evidence() validates the pair first, then replaces the live owner state, witness and observations under one lock while retaining the accepted generation and effect-suppression behavior
- save_with_evidence_file() writes the entire envelope through the existing atomic temporary-file/fsync/replace writer
- load_with_evidence_file() validates that complete envelope

A pre-replacement write failure leaves the prior valid file intact. The existing writer reports uncertain crash durability if directory fsync fails after replacement. The accepted raw _persist callback still persists raw owner data only; it is not a paired-history persistence hook. Production native transaction/storage integration must save the composite data atomically and remains pending. The reference file path and Python lock establish only the explicitly tested reference behavior.

## Narrow verification

The unchanged reviewer strong repro and all ten independent tests pass on R2 in normal and optimized Python. Ten new pairing tests cover same-prefix branch forks, live wrong-ledger rejection without resealing, paired file roundtrip and failed replacement, failed result persistence, pending effects/stale callbacks, later losses after P14 entry, raw-restore evidence detachment without lost wins, unsupported v1 envelopes, and snapshot/commit locking.

The focused producer gate runs 43 named tests in each mode: all 14 retained source-domain methods, six relevant retained validation/replay methods, all 13 existing current-flow tests, and the ten new pairing tests. The unchanged 6,561-projection and 1,485-vector matrices are excluded and are not claimed rerun. Their earlier v1 logs remain historical producer evidence, alongside the independent rejection.

The original P14 admission ordering fix, P14 model, 77 retained SCI methods, codec, canonical fixture and generated finite source are unchanged from v1. All original consent, actual four-win gating, first-win stability, signature/pencil, three closing tones and detached parallel replay checks remain in the focused suite. Existing 32 scoped normal/optimized admission probes remain part of the gate. Clean spaced-path regeneration verifies unchanged fixture/source/manifest/object bindings, followed by the focused suite in both modes.

One new test initially queried save_with_evidence() before attempting an effect claim. The inherited owner deliberately suppresses transient effects on save, so that test's expected claim was wrong. The corrected test observes the owner-held witness without saving first. Its initial failure log is preserved; no owner effect behavior was changed.

Exact v1-to-R2 code diffs are in provenance/r2-differences.json and its referenced patches. New executable behavior is confined to contest_evidence.py and the reference facade. The test runner and named-test admission add the focused correction suite. All historical/literal files remain exact.

## Remaining scope

Targeted independent acceptance of this correction is pending. Production native atomic owner/evidence saving, cross-owner ownership/rollback, real actor/rematch-room reconciliation, native rendering/audio/save kernels, isolated native replay, final asset/licensing checks and full-game completion remain open. The finite SCI layout remains 669 properties/642 persisted words; no selector or storage ABI changed. Browser, native game/saves, published main and GitHub were not touched.
