# Corrected P07 reference revision 2

This revision addresses independent review of the original new reconstruction. It does not recover an original implementation or establish native acceptance.

## Preserved original

The original packet is unchanged:

- Filename: P07-reference-reconstruction-20261006.zip
- SHA-256: b96d71ca79d7e3b182d2e8ee61c94d29e5ca316452f00311466855af4ad4455f

Revision 2 is a separate directory and archive. Its original authorities, all 42 P07 records and all 27 speech units remain unchanged. The canonical save schema and valid saves are preserved; newly rejected histories were unreachable under the original public action semantics.

## Source-history validation defect

The original validator considered omitted serial gap lengths without tracking which sources were still unread. That accepted three representative impossible histories:

1. New read/cancel serials after all three sources had already been learned
2. A supposed replacement of the sole remaining unread source by itself, although same-source reopening is a no-op
3. An odd-length closed cancellation gap when the one remaining unread source only permits alternating open/cancel commits

The corrected validator walks all retained events in chronological order and tracks the possible pending source identities and the unread-source set. Its closed-form gap reachability is constant-time in each gap's length, including the full unsigned 32-bit range. The implementation and proof obligations are described in DESIGN.md.

The independent reviewer's unchanged literal scripts and original counterexamples/reports are retained in evidence/independent-review-initial. The corrected full source-history comparison is recorded in evidence/source-history-r2.json. Tests execute the unchanged scripts in temporary isolated output directories under both ordinary and optimized Python.

Results:

- Revision-10 source-slot oracle: 8,442 candidates; 4,278 reachable accepts; 4,164 unreachable rejects; zero mismatches. This closes the original 1,236 false accepts without rejecting any reachable layout
- Whole cooking/comedy/sincerity/handoff slot oracle: 576 candidates across six source-order histories; 226 reachable accepts; 350 unreachable rejects; zero mismatches. This closes the original 182 false accepts in that extended set
- Dedicated regressions retain the exact three counterexamples, all final-source read/cancel orders, valid replacements and large unsigned counter parity

## Verification coverage defect

The original verifier accepted a total test count of at least 55. Removing the two finite-state tests still left 56 tests and incorrectly retained unconditional coverage claims.

Revision 2 uses an explicit tools/required-checks.json acceptance inventory, which sealing does not regenerate. It discovers and checks every required test ID before running any tests, then requires those same named checks in the completed output. Required coverage records are emitted only after the associated finite loops and assertions finish. Missing, duplicated or changed metrics fail verification; the report's coverage is copied from measured output rather than unconditional constants.

The regression reproduces emptying tests/test_finite_space.py and recomputing MANIFEST.sha256 exactly as sealing does. Verification now fails at required-name discovery, overwrites a stale PASS and emits no coverage section. Another regression supplies successful test names without loop metrics and proves those cannot count as coverage.

The original 58 tests were rerun before the R2 additions and passed under both ordinary and optimized Python. The expanded acceptance inventory has 65 named tests. Existing isolated imports, missing-original portability, canonical corruption, stale-PASS and golden-fixture guards remain active.

## P13 boundary, deliberately limited

P13Handoff remains a declarative description for a trusted synchronous future-host transaction. It is not a capability or asynchronous callback ticket. The original review's fourth demonstration correctly shows that the same request value can be reused with a new reference host after timeline restoration or in a different reference world. This behavior is not represented as a request freshness guarantee.

The class and design documentation now state this limitation explicitly. A real future P13 host must authorize actual delivery conditions and separately bind asynchronous dispatch to its current world/session and outside-VM execution lease. This packet neither implements real P13 nor proves such a native boundary. The existing exact-pot owner checks, atomic handoff, domain/owner restore consistency and no-SERVED-grant invariants remain tested.

No native code, object/selector allocation, Main edits, publication or uploads are part of this correction.
