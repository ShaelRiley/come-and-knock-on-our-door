# Public source edition and dependency policy

This source bank is an explicit publication adaptation of separately verified
development components. Revision 2 selects the corrected P08 Gate2b2 host and
retains the other nine components byte-exactly. Their completed validation is
rechecked against the final component inputs; the corrected host has its own
fresh affected gate. This is not the unchanged internal backup archive.

The baseline is commit `ab65f4a6f3aea28ba849a0a99074a989cdeef458`, Git tree
`ddb0e1a8da76361dd08abb8249077a17365d03ee`. Its source, frozen game data,
compiler executable, compiler source closure and notices are reused unchanged.
Only the root README gains the WIP introduction; its original text is preserved
in `BASELINE-README.md`. Baseline authority bytes are preserved exactly,
including their already-public historical provenance.

## Readable source and deduplicated inputs

`components/` contains the newly needed files. `manifests/COMPONENTS.json`
maps every original component-relative path to its stored source path, SHA256,
size and executable mode. Identical inputs reuse existing baseline or component
files. The reproduction script resolves these checked relative paths into a
new isolated directory. It never edits the frozen repository or another build.
No Git history, special filesystem links or external backup archive is needed.

Gameplay/domain/renderer implementations and behavioral tests remain unchanged.
The explicit `publication_changes` entries record input-inventory revisions,
removal of administrative identifiers, and two Music score-generator provenance
strings changed from private resource identifiers to a public source hash.
Those two strings affect provenance fields only, not notes, timing or scoring.
P09's generated manifest and extension contract necessarily carry updated
metadata hashes; `OUTPUT-METADATA-ADAPTATIONS.json` enumerates the exact allowed
field changes. Every other selected generated and emitted output must match
the original component hashes.

## Compiler and licenses

All components use compiler SHA256
`608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e`.
The corresponding source is supplied once at
`source/workspace/rebuild/p03-editable-checkpoint/toolchain/`.
The baseline's independently build-verified closure has 179 source/header
inputs and 69 translation units. `docs/COMPILER-BUILD.json`,
`docs/COMPILER-RIGHTS.json` and `THIRD-PARTY.md` retain its provenance,
compatibility changes, license analysis and exact executable reproduction.
No broad private compiler/vendor tree, GUI resources or proprietary Prof-UIS
is included in the new component payloads.

Existing third-party licenses and notices remain intact. The original game
and new project work receive no new blanket license through this bank.

## Frozen and regenerated audio

The 946 P07 speech/sync inputs are retained byte-exactly. Identical files reuse
the baseline; new frozen inputs are stored once. Their missing historical
authoring masters are not represented as recovered editable source.

P08's newly generated speech/sync and P09's new twenty fragments can be omitted
from the component's output layer because the complete pinned renderer,
profiles, canonical text and source inputs regenerate them offline. Fresh
rebuilds and exact output comparisons are required before this bank is sealed.
Frozen predecessor audio needed as a test input stays included. P09 historical
PCM was unavailable; its audio is a new deterministic render from original
profiles, not a claim of historical byte identity.

Music's accepted source MIDI/native payloads and irreproducible audition renders
remain included. The redundant nested R1 source ZIP and unused old proof
packets are omitted; compact negative-control fixtures actually referenced by
the tests remain. No dependency on a missing native SoundFont render is hidden.

## Exclusions and verification scope

The new payloads exclude private conversation and recovery correspondence,
administrative receipts, credentials, signed download URLs, native captures,
actual test saves, temporary expanded copies and unused historical packets.
Technical frozen ABI/source/compiled negative fixtures remain where the tests
need them. They are not evidence that a newer source version has passed.

The new publication driver records each command's actual exit status and
log hash, then compares outputs. Failing phases stay failures. Bounded phases
can be run separately; this avoids relabeling a partially completed long suite
as a full pass. No phase grants playable, native, listening or integrated-host
acceptance, and no remote publication action is performed by these tools.


## Revision2 dependency correction and final proof

The exact 448-byte orphan-template negative fixture is retained at its original
component-relative path under evidence/. It is required test input, not a
historical log. Its earlier omission caused a real failed packaging validation;
the failed record remains separately preserved. The corrected public edition
then passed a fresh original 22-case run with no resumed or borrowed passes.
The other nine component file maps are unchanged. All 389 completed task cases
and 442 selected generated/emitted outputs are bound by VALIDATION.json.

Some shared unchanged inputs retain earlier component directory names because
the file map deduplicates bytes. COMPONENTS.json selects Gate2b2; it does not
select the historical Gate2b1 host or its removed defective source modules.
