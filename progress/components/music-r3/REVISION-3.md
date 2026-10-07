# Revision 3: coherent finite save/restore lifetime

The immutable R2 archive is `CaKoOD-Responsive-Music-Transport-Source-Candidate-R2-20261006.zip`, SHA256 `cbc795730b5b4e158fbbbd41e1338570439c9e05c365310ee58689416336f6f0`. Its independent verdict was REVISE because an actual successful Main.writeSave at generation [32767,32767]/error9 produced a valid frozen music snapshot that could not pass the required restore generation advance. Exact independent script, report, frozen typed snapshot and review are retained under `inputs/revision2/independent-review/`. All three preceding R2 corrections remain in place.

## Explicit finite-lifetime policy

A successful music snapshot needs one unused generation advance for early restore retirement. Active Main.writeSave therefore calls `rbSaveAdmit` before its existing domain/save guards or native SaveGame. At the maximum generation, with or without a previously rejected request, or with latched exhaustion error9, the attempt returns false, clears any previous audioSaveResult success and dirties the UI. No native save chooser is entered, no owner is retired and no gameplay state is changed. Every active save attempt clears its old result before any subsequent domain or music guard can reject it.

The footer says `SAVE UNAVAILABLE: MUSIC LIFETIME LIMIT.`. This diagnostic overlay does not change the music-health state: a healthy final issued generation can still finish its already-valid work. The presentation flag is range-checked but never trusted for admission; the real generation/error is checked every time. R cannot reset or wrap the generation, and canceling either chooser cannot renew it.

The last admissible saved generation is [32767,32766]. A successful load of that snapshot uses the existing exact restore protocol, advances once to [32767,32767], and resumes the saved bed after complete host admission. Further saves from that runtime are refused. Repeated loading of the same earlier snapshot reproduces its saved counter rather than claiming globally unique IDs: safety still rests on retirement of the previous native runtime and abandonment of its old invocation stack before restored dispatch. There is no game-history or musical-ledger reset.

## Loading earlier saves remains available

A running bed or connector keeps the existing chooser protocol. A fully retired failed music owner now has a narrow readSave-only path through `rbLoadChooser`: fresh static and complete broker validation must pass, the owner slot must be empty, both transports must be stopped, and no other chooser/restore may be active. The empty slot can then enter the native restore chooser without starting any sound. Cancellation releases only the chooser flag and preserves the failed generation, controls and empty slot. Selecting an earlier valid save replaces that failed runtime through the stock restore lifecycle.

This seam is not used by writeSave. It does not let an ownerless failed music snapshot be saved, admit corrupt static/owner state, replay a connector, restart a score, or bypass any P05/domain restore validator. Main's existing readSave critical-section guard remains ahead of the changed chooser call. The successful load invokes actual Main.replay, p05RestoreBegin, P05/986 retirement and validation, audioRestore, p05RestoreValidate and rbRestoreResume before the ordinary event loop resumes.

## Regression evidence and limits

The new fixture executes the complete emitted P05 host with its pinned genuine text resources and font. Its typed SaveGame interception captures the frozen graph, and its typed RestoreGame transfer clears the old parser graph and abandons the old invocation stack before invoking actual emitted Main.replay. No game or broker method is replaced by a mock. The harness explicitly models absent legacy Sound stop/dispose calls, native event-queue draining, saved parser reconstruction and cursor kernels. These are source/emitted lifecycle tests, never native save-file, physical-channel or listening proof.

Coverage includes the original genuine986 exhausted-save case; healthy maximum generation; last-admissible complete save/load/replay/resume; repeated earlier-save loads; save cancellation and retry; load cancellation after refusal; fully retired failure loading; changed static guard rejection; forged presentation flag rejection; and preservation of earlier result/probe/ABI contracts. All preceding 69 named tests remain required, with nine new revision-3 tests. The 23 primary and seven packaging negative-probe identity manifests remain unchanged.

Final current P06/P07 composition, native engine/channel/tail proof, listening review and explicit activation remain separate gates. No original MIDI or native Sound input, derived941/942 transport, source timing table, protected940/981 or PCM980 module is changed.

## Current recovery notice

The preceding authoring text is historical. This new rebuild does not restore missing historical review receipts or the old R3 ZIP. Its known R2 boundary report is freshly re-executed and labeled in RECOVERY-PROVENANCE.json. New full tests, guards, relocation and archive identities are mandatory.
