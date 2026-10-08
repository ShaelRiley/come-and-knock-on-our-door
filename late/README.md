# Later editable source components

Corrected public edition, revision2: revision1 removed two unused administrative inputs and updated their dependency metadata. This revision corrects the public description of that completed work; component inputs and outputs are unchanged. See `late/CORRECTION-REVISION1.json` and `late/CORRECTION-REVISION2.json`.
All components here are work in progress at the production/native boundary.
Prior independent acceptance applies only to each component's stated finite
source/emitted scope. This edition separately verifies its public dependency
closure and reconstruction. The game is not complete.

## Included components

- `p09-host-foundation`: inactive coherent twelve-module foundation, production
  species12/export0, reserved selectors3000–3163; dispatch remains closed
- `p09-geometry-scaffold`: measured source/emitted tags and approach geometry,
  three further selectors3164–3166; no earned P09 state or native acceptance
- `p10-domain` through `p14-domain`: editable reference models, literal and
  reconstructed SCI, codecs, canonical fixtures and source/emitted harnesses;
  each domain compiles as an isolated species1 fixture, not the campaign host
- `p10-scene` through `p13-scene`: canonical scene exporters, current caption
  and speech bindings, original procedural audio and exact ancestor fixtures
- `p12-scene` includes the accepted seven original Audience reply variants
  while preserving all39 principal speech pairs
- `p14-scene`: accepted R1 class-free999 bank, 125 records,43 canonical units,
  59 credits, case-preserving font1 and explicit date-materialization tools;
  production date capture and arbitrary-date native speech remain open

E03 actor presentation, active P09 card/reader/ownership integration, later
hosts, full campaign composition, native saves, native rendering and listening
are separate unfinished gates. Inherited status strings inside frozen data
may say candidate or pending; the scope above describes the independently
accepted source component, not a promotion of those fixtures into the game.

- `scene991-renderer`: stateless extraction of fourteen Main paint methods into
  reserved script991/species13/export0; Main is54642 bytes with10893 free, all
  earlier owner modules remain exact and P09 stays inactive
- `p08-evening-ack`: accepted14-scenario source/emitted storage ACK and witness
  kernel; Main is unchanged, selector2991 h8E is added, EveningReady remains
  false and actors stay in their prior meeting positions

These last two components preserve distinct accepted ancestors. They have not
been combined into a new tested campaign or playable release.

## Environment

Use Linux x86-64, Python3.10+ without optimization, the ordinary dynamic C++
runtime libraries required by the pinned compiler, and Pillow for image
rendering/review. The game audio renderer is supplied as editable source.
No download or package installation is performed by these commands. Exact
versions used for this edition are in `VALIDATION.json`.

## Reproduction

From the repository root:

```sh
python3 progress/verify_source.py
python3 late/reproduce.py p09-geometry-scaffold --out /absolute/new/p09
python3 late/reproduce.py p10-domain --out /absolute/new/p10-domain
python3 late/reproduce.py p10-domain --phase test --suite finite --out /absolute/new/p10-domain
python3 late/reproduce.py p14-scene --out /absolute/new/p14-scene
```

`--phase materialize` creates an editable component without running it. A build
requires a new output folder outside the source repository; `--phase test`
requires the matching completed build. All mapped source paths, sizes, hashes
and executable modes are checked before copying. Every declared stable output
is checked against `manifests/EXPECTED-OUTPUTS.json`. Metadata containing
component-root paths is compared after replacing that exact root; typed resource
inventories are compared after sorting their entries by type/number. No field
or resource is omitted by these declared normalizations. Their hashes are in
`manifests/NORMALIZED-OUTPUTS.json`.

Scene builds include their retained scene test suites. P14 additionally runs
the80 date-length cases, static audio checks, emitted audit and font review.
For separate domain suites, use these names with `--phase test --suite NAME`:

- P10: `domain`, `finite`, `transport`, `reference`
- P11: `domain`, `adaptations`, `finite`, `transport`, `finite_projection`
- P12: `domain`, `finite`, `transport`, `projection`
- P13: `domain`, `validation`, `finite`
- P14: named bounded groups from the materialized `tests/EXPECTED-TESTS.json`
- P09 foundation or geometry: `all`
- SceneRenderer991: `first`, `matrix`, `supplement` after `matrix`, `order`,
  `preparation`; the build runs the20-comparison `first` group
- P08 evening ACK: `ack01` through `ack07`, `publisher`, `prior`, `storage`

No command launches ScummVM or installs a new player build. Some supplied
fixture APIs require generated ancestor outputs: their necessary bytes remain
in the component mapping. Identical payloads, including compiler sources,
canonical authority and audio, are physically stored once across this tree.
The map makes their component-relative reconstruction explicit.

## Editing and verification

Edit the materialized ordinary files. The immutable public source manifest
intentionally rejects unnoticed edits; regenerate and review new source/input
and output seals when making a new component version. Never transplant an
isolated domain's species1 resources or an older P08 host over newer campaign
state. Read each generated contract and preserve its exact source/emitted
ownership and callback boundaries.

`VALIDATION.json` distinguishes exact binary/resource comparisons, public-only
metadata changes, newly executed tests and inherited acceptance. Its isolation
statement is precise: Python read/network hooks cover Python processes, not
arbitrary native system calls. Native compiler tracing was unavailable because
the environment denied ptrace. Compiler executable pins, explicit local
arguments, source universes and matched outputs are recorded; no stronger
OS sandbox or compiler-bootstrap result is claimed.
