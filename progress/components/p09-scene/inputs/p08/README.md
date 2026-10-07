# P08 scene-data source checkpoint

New editable reconstruction for Come and Knock on Our Door, derived against the current P07 ten-module SCI1.1 source. This is not recovered historical implementation or a playable P08 host release.

This source was restored from the durable initial checkpoint after an executor reset. The original checkpoint's compile proof is historical evidence only. Later source/emitted tests passed before the reset, but those local reports were lost. Current generation, compilation and fixed-suite status comes only from freshly bound proof. Source-only relocation and packaging gates remain separate requirements for final component acceptance. Native pixels, listening, OS input and native save/load remain untested.

## Data and exact boundaries

- 44 canonical P08 records/33 speech units, plus separate TRANSITION.P08.01/four units
- Initial generation produced68 pages,41 deterministic procedural cast fragments and27 silent pages
- Exact source characters, UTF-8 spans, words, speakers, obligations, full canonical metadata and the existing eight author contributions stay intact
- Original eight cast profiles and abstract syllabic renderer are retained; these are non-intelligible procedural voices
- Text208 and Audio36/Sync36 module918; documents973–1016 plus transition1017; global lines729–773
- Existing1,070 pages and special P07 aliases971/972 keep their tuples; array holes preserve the special aliases
- Existing50-column/three-line/font0 geometry and153-byte text buffer

Only current982 arrays, document/resource bounds and static accessor, plus985 static count/offset methods are extended. All20 static families are rederived. Initial compilation used1,029 of1,440 chunks in banks240/241/244. Labels242 remain exact and separately owned music text243 is outside the writes. No selectors or classes are added. Initial Main remains62,648 bytes with2,887 bytes of headroom;982 is49,816 with15,719 bytes remaining. Address relocation within982 does not change selector/class/page identity.

The generated complete-record and unit-only window map is for future host integration. Unit receipts cannot stand for a full record. The transition uses a separate owner and transition-unit namespace, with domain record/unit0. Current request/generation-bound, unobscured Graph12 receipts are owned by the host. Opening, rendering, skipping or audio completion grant no P08 observation, ownership, readiness or E03. P08 host actions and campaign completion are outside this data component.

## Dependencies and future staging

Component rebuild uses included frozen inputs and the pinned Linux x86-64 compiler, Python3 standard library and system libstdc++, libm, libgcc_s, libc and ELF loader. No external project archive or network is required for the component's rebuild. Compiler SHA256:608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e.

Optional compiler source: cakood-p07-rebuild-source.zip,43,773,494bytes,SHA25681befeaa241c597f31b14330703d2df55f28846b44279c7402815fbb97c0899f. Its toolchain/SOURCE-MANIFEST.json is SHA256dfb78557a9b270d9272f8052d2fe08a7c2eb21a55fce239255126eeb202ced4b and identifies the local compatibility patches as well as upstream sources.

Future playable staging additionally requires cakood-p07-private-candidate.zip,78,784,481bytes,SHA2568363e75eba9df20808f134d94b3acdb250e29996c42eb9a101a226a4b91e43da. Its948 game files include946 old PCM/Sync files; exact filenames and hashes are in inputs/baseline-GAME-MANIFEST.json. Old PCM is not duplicated or rewritten. Recompile the complete latest source/class/selector universe before staging any new scene data. This component's fixture contains only a packed map/volume; new audio is stored once in generated/speech. It is not a self-contained playable runtime. A subsequently integrated game needs stock ScummVM with SCI1.1 support; no native runtime is installed or launched here.

## Verification and supported commands

The intended fixed suite covers exact canonical record/unit/transition membership and editorial metadata, character/word/UTF-8/speaker reconstruction, complete/unit-only maps, deterministic PCM/Sync, mute eligibility, every old page/alias, every new source/emitted page, bounded emitted Graph12 renderer calls and geometry, actor eligibility, audio skip/end behavior, ordinary per-document source/emitted restore, static families and bank boundaries. The current inherited emitted harness checks kernel/property arity, operand stack/variable bounds and instruction boundaries. Reviewed scene/static method arity is also checked explicitly.

Source-only relocation must regenerate scene/text/audio/static/compiled outputs exactly. Packaging must require exact source/output/proof inventories and clean fixed test membership, reject stale/missing/extra/contradictory proof, and exclude unsealed files. All such acceptance remains pending on this restored source until its gates finish. Deterministic harness results never stand for native UI, audible playback or native SCI saves.

The test and packaging sources have been reconstructed with13 fixed cases,17 negative acceptance cases and21 packaging regression cases. The first bounded execution gate runs generation, compilation and the fixed suite. It does not establish relocation, packaging or native acceptance. The complete supported sequence is:

    python -B run.py seal-source
    python -B run.py rebuild
    python -B tools/portable_verify.py
    python -B tools/negative_probes.py
    python -B tools/review_regressions.py
    python -B run.py package

The seal-source command records source identity only; it never confers a pass. Fresh outputs and tests are mandatory afterward. The package path is delivery/P08-Scene-Data-Reconstruction-20261006.zip. Complete source-only regeneration requires no historical generated/proof files. The initial checkpoint version is preserved in Library history.
