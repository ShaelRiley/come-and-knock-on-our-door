# Come and Knock on Our Door: full-campaign source WIP, r16

This is an editable, independently reproducible source checkpoint for the current
21-module SCI1.1 full-campaign implementation (P01–P14). It is work in progress.
A complete genuine start-to-finish route and native ending acceptance are still
pending. This is not a completed-game claim or a new player distribution.

## What is banked

- The exact 21 canonical SCI source files and selector dictionary from r16
- The 86 current non-code packed resource inputs and 1,711 current project
  audio/synchronization files, each individually hash-bound
- A deterministic compile-only selector alias transform; canonical source stays
  readable and retains the exact original selector names and IDs
- The pinned Linux compiler, its audited corresponding source, build instructions,
  component licenses, modification provenance and dependency inventory
- Recoverable asset-authoring recipes with their own explicit coverage limits
- A portable cold-build verifier and bounded static resource/reference tests

The cold build independently reproduced the exact r16 compile receipt
`b3f839512100c06368ce903ecc018bad8ac600ce6ccf647401f693b50c56ce48`,
all 21 scripts/heaps, 1,871 substantive build outputs and all 1,713 staged game
files. The full ABI matches after only relocating its generated path fields.
Current game resource packing contains 130 typed resources. No precompiled game
scripts, game heaps, current resource-map/volume pair, runtime engine, save files,
play-session captures or historical run directories are source inputs.

## Reproduce

Requires Linux x86-64, Python 3.12+ and the pinned compiler's system libraries:
libstdc++, libm, libgcc_s and libc. No network access, package installation,
external service or game-engine launch is performed. Do not use Python -O/-OO.
From the source-bank root:

    python3 -B campaign-fullgame/verify_payload.py
    python3 -B campaign-fullgame/reproduce.py --verify-only
    python3 -B campaign-fullgame/reproduce.py --out /path/to/new-fullgame-build
    python3 -B campaign-fullgame/testing/run_static.py --build /path/to/new-fullgame-build --out /path/to/static-result.json

Choose a new, nonexistent build directory outside this component. The cold-build
command produces developer-local outputs and verifies them against OUTPUT-PINS.json.
It does not launch, package or certify a player release. `--check-existing` checks
an already rebuilt directory without compiling again.

`verification/COLD-REBUILD.json` and `verification/STATIC-REFERENCES.json` are the
fresh results for this exact source checkpoint. The static test checks 177 direct
DrawCel references, 77 GetFarText references, 3 literal Audio36 calls, 3 Sound
defaults, and 1,446 authored P05–P14/shared-Contest pages with 752 voiced-page
references. It also checks text equality, entry bounds and audio/sync hashes,
and rejects three malformed resource-pair fixtures. These are source/asset checks,
not gameplay, timing, rendering, save compatibility or native-audio acceptance.
Computed references and symbolic assembly operands are not exhaustively evaluated.
The test does not independently re-prove P01–P04's authored reader tables.

## Editing and historical material

`source/src/*.sc` is editable canonical program source, not generated code that
must be reverse engineered. `source/selectors.json` is its canonical selector map.
The build makes separate compiler-only aliases for new P14 selector strings to
fit SCI1.1's 16-bit vocabulary offsets. Do not edit compiled aliases as canonical
source. `source/assets/` contains the exact current binary asset inputs. Text
resources are NUL-separated ASCII; VIEW/font/audio assets use the documented SCI
formats implemented by the included project tools and recoverable recipes.

The independent public builder replaces the historical composition pipeline with
these frozen canonical authoring inputs. It preserves program/output identity;
it does not purport to reproduce every intermediate derivation file or old test
run. Earlier public source-bank components remain unchanged and preserve their
own history. The authoring directory independently regenerates 1,318 current files exactly,
including 1,307 audio/sync files and 11 packed resources. It explains which assets regenerate exactly,
which inherit current binary art and which editable masters are unavailable.

Deliberate edits naturally invalidate checkpoint hashes. Work in a new directory,
edit the canonical source and/or explicit asset inputs, build with `source/build.py`
in the copied source tree, and establish new output pins and applicable dynamic
and native acceptance before publishing a replacement. The exact-checkpoint
verifier must not be weakened to make modified outputs appear unchanged.

## Rights and boundaries

Read LICENSE.md, THIRD-PARTY.md, CREDITS-AND-RIGHTS.txt and rights/ before reusing
or redistributing content. Public visibility does not grant a new blanket game
or music license. Compiler licenses apply to their own components.

The remaining individual historical art-origin receipt gap is specifically
VIEW221–224, 300 and 302. Existing project-output continuity is verified. Missing
masters alone are not treated as missing rights, and the gap is not an allegation
of infringement. Derivative art retains its inherited qualifications. User music
ownership is an assertion, not independently certified ownership.

Project speech, laughter and foley are static game assets with recorded provenance;
they are not play-session recordings. Only assets in the exact current stage are
included. Unused audio candidates, private evidence and runtime engines are absent.
