# Contest snapshot: exact role in the accepted five-puzzle build

All eight files under `source/workspace/rebuild/p05-host-reconstruction/snapshot/contest/` are retained unchanged. They are fixed members of the accepted host's INPUTS.json and EXPECTED-INPUT-PATHS.json. Removing any one would require changing the original build guards. No historical false acceptance marker has been deleted or relabeled.

## Direct dependencies

- `module986.sc`: derive.py:212 copies it into src/module986.sc. tools/validate_selected_inputs.py:11 independently pins its SHA-256
- `selectors.json`: build.py:45 uses it to reserve the Contest ABI before compiling the complete universe
- `canonical-bindings.json` and `manifest.json`: generate_contest_labels.py:5,16–18 uses them to generate canonical label text. tools/validate_static_inputs.py:7–9,22–26 validates their pins, and tests/test_contest.py:130 plus tests/test_saved_consistency.py:14 consume them
- `REVIEW-RESULT.json`: tools/validate_selected_inputs.py:12 explicitly pins its hash. Both derive.py:6–7 and build.py:15–16 invoke this guard. This is a direct guarded dependency, not removable unused proof
- `ABI.md`, `HOST-CONTRACT.md`, `SHA256SUMS`: retained inventory/provenance dependencies. No semantic parser callsite was found, but verify.py:13–20 checks their fixed membership and hashes

In addition, tests/verify_architecture.py:33 hashes all snapshot files. The offline source/rebuild.py retains the accepted host input seal and the exact verifier source pin, invokes its inventory predicate before and after generation, and checks all emitted resources and game files. The publication revision changes only the outer source-packaging identities needed by compiler-source filtering; it does not alter these host/native guards.

## Exact identities

- ABI.md: ae81f799dd28eb2b3cb075bfea1d8ec74ea7cf87198091c97902d8e95adee98a
- HOST-CONTRACT.md: f034fa3d5d77de5548f0263dfa4ba760bdb7eaf5156a4623fa3aadbd55b3d087
- REVIEW-RESULT.json: 236c2782a5dc5028c97043959c41f22345a1d1a6cee88f3d000ce5a9314b0ff6
- SHA256SUMS: db6419161bc579f716e5c5da88b12f3bea32ff9a40a9ef03388a017d6a190d74
- canonical-bindings.json: cd11fda0a88847aa2d6650acf76d8a606ac9f62004dd18090f61033d69c7851e
- manifest.json: bef627740b7b2c8b8a082c2063c7dbd2b3a0df26da8830c80851e09f5fdf164b
- module986.sc: 9dfbe07a0092eff89b0b919706d8e82a743b30ec9615906953e68fc85655bb81
- selectors.json: 3d2f1acc9098c26da231daa64e74bd308252e11f711bf100af5d289160cb2742

## Whole-build connection and boundaries

The snapshot module986.sc equals the accepted derived source byte-for-byte. The actual packaged resource decoder yields script986 (10,636 bytes, SHA-256 1ceaf4c6f0fe3331574fd9bb77b7f0ef523ab2a5b5c037b18826024781c9b0e0) and heap986 (1,120 bytes, SHA-256 6ecaaf18eb84ceda24696a35db25f154eca52d3e7975c289f44d96dda861b8db). Their identities are bound by the accepted package manifest dcf4be1c89dba28a4557ac9b9176d7b9894f40be8eeec1aa74f64b0f7473d3bb and the offline reconstruction receipt.

All 780 packaged files match the actual game's five-puzzle native run. The later whole-build native report identity is 5a55917da7b316479223b264c9309f5690774823fba6416cd5c6d7b28a2a69d6, fingerprint 3be11ae9485b85f2f9c8f98f04868a184a078be898d77fbc64f9b7447c21ee35. It records bounded Contest loss/rematch/win/yield and save/restore coverage, normal exit 0, and unchanged game files, with a presentation finding. It does not claim full presentation or full-campaign acceptance. See NATIVE-SCOPE.md.

The standalone REVIEW-RESULT.json retains native_acceptance:false, publication:false and its other original limitations. Those are historical component-scope facts. Including its source in this later native-tested whole program does not promote that standalone report to a different acceptance scope.
