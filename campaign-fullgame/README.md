# Come and Knock on Our Door: full-campaign source WIP, r17

This editable 21-module SCI1.1 full-campaign checkpoint (P01–P14) disables the
three incidental CSV writers by default. It is work in progress. A complete
genuine start-to-finish route and native ending acceptance remain pending.

## Change and evidence

Only audioTrace, hostTrace and speechTrace change in canonical main.sc. The
previously compiled candidate changes exactly 11 script bytes; all heaps, other
scripts, effective layouts, method addresses, strings and relocations remain
unchanged. The historical extractor has two explicitly bounded raw instance
selector-label artifacts, documented and checked in testing/verify_trace_delta.py.
The staged game differs only in resource.000. Its resource.map and 1,711 audio/sync
files are unchanged. No saved setting or player diagnostic control is introduced.

The candidate's production compile, independent cold-output identity, exact-byte
and layout certificate, and 12 bounded normal-caller checks passed previously.
The offline diagnostic compile retained the original r16 output identity;
diagnostic behavior was not rerun. Bounded native startup, speech/mouth, zero CSV,
normal save/restore, one existing r16-save restore and earned VC03/restore checks
passed. P12 through the ending remain unrun on r17. These are scoped observations,
not universal save compatibility or complete campaign acceptance.

This public update preserves the r16 canonical-source builder architecture. Its
small receipt/staging changes and portable verifier adaptations have not been
compiled or tested again. OUTPUT-PINS.json binds the previously reviewed r17
candidate. See verification/R17-STATUS.json and verification/README.md. Existing
r16 verification JSON files remain unchanged historical records; no new public
cold-build or whole-suite pass is asserted.

## Reproduce and inspect

Requires Linux x86-64, Python 3.12+ and the pinned compiler's system libraries:
libstdc++, libm, libgcc_s and libc. No network, package install or game-engine
launch is used by these commands. Do not use Python -O/-OO.

    python3 -B campaign-fullgame/verify_payload.py
    python3 -B campaign-fullgame/reproduce.py --verify-only
    python3 -B campaign-fullgame/reproduce.py --out /path/to/new-r17-build
    python3 -B campaign-fullgame/testing/run_static.py --build /path/to/new-r17-build --out /path/to/static-result.json

Choose a new build directory outside this component. --check-existing verifies
an existing build without compiling. To compare two separately built checkouts:

    python3 -B campaign-fullgame/testing/verify_trace_delta.py --baseline /path/to/r16-build --candidate /path/to/r17-build

The latter reads built outputs and prints the bounded certificate; it does not
compile or launch the game. Build the r16 baseline from commit
6942753fc0081abc483c0cf99a122e1c542d75bd in a separate directory. That historical
checkout also supplies the original trace-enabled program for offline diagnosis.
This public builder has no diagnostic-mode switch. Do not substitute an r16 build
for r17 production or relabel diagnostic observations as production acceptance.

## Editable inputs and retained assets

source/src/*.sc and source/selectors.json are canonical editable source. Separate
compiler aliases preserve the original selector names/IDs and SCI vocabulary
limits. source/assets/ contains the 86 unchanged non-code resource inputs and
1,711 audio/sync files. The pinned compiler, corresponding audited source and
component licenses are inherited unchanged. authoring/ regenerates its documented
subset of 1,318 current files; binary art inputs and unavailable original masters
retain their explicit coverage limits. The r16 asset/provenance labels in those
unchanged documents identify the inherited asset revision, not the r17 program.

No current compiled game scripts/heaps, game resource pair, runtime, saves, play
captures or historical run directories are source inputs. Deliberate edits
invalidate hashes: establish new output pins and applicable acceptance without
weakening the exact-checkpoint verifier. Earlier source-bank components remain
historical and unchanged.

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
