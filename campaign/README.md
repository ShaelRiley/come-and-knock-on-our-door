# Ten-puzzle campaign source: room, actor and legacy-return repair

This editable SCI1.1 source component reconstructs the exact fourteen-module
program used for the bounded native ten-puzzle functional checks on 2026-10-08.
It is an update to the P08–P10 public regression source, for the existing
revision-3 CaKoOD source bank. It is not a runtime distribution or whole-game
completion claim. P11–P14 remain separate work.

## Current verification

- `OUTPUT-PINS.json` and `SOURCE-MANIFEST.json` identify the repaired program.
- `COLD-REBUILD-RESULT.json` records a fresh build matching all 14 generated
  sources, 111 compiler/resource outputs and the normalized full-module ABI.
- `repair/VERIFICATION.json` and `repair/verification/` record the new bounded
  repair regression and structural checks. Read `testing/README.md` for scope.
- `repair/NATIVE-COVERAGE.md` is a concise summary of separately observed native
  behavior. Native observations are distinct from portable DrawCel traces and
  mocked storage. No private saves, captures or raw native reports are included.
- `INTEGRATION-INVENTORY.json` is the active final file, size, hash and mode map.
  `verify_payload.py` checks it, including membership. It excludes only itself
  from its own file list; the archive/delta manifest binds that inventory file.

The earlier ten-method, 2,860.142-second source/emitted result remains historical
at `testing/verification/`. It tested the pre-repair compile receipt beginning
`473d8fb1`; it has not been relabeled as a new full-suite result. The current
compile receipt is `148c1068ffa166fa373b46233beb104ae19199fd86940de93b26335d41d8d702`.
Historical inventories and baseline acceptance/adaptation receipts are retained
for provenance, not as assertions about current membership or coverage.

## Reproduce and test

Requires Linux x86-64, Python 3.12+ and the pinned compiler's system libraries
(`libstdc++`, `libm`, `libgcc_s`, `libc`). No network, installation, private
service, engine launch or publication is part of these commands. Do not use
optimized Python. From the source bank root:

    python3 -B campaign/verify_payload.py
    python3 -B campaign/reproduce.py --verify-only
    python3 -B campaign/testing/run_repair.py --work /path/to/new-repair-work
    python3 -B campaign/repair/verify_scope.py --work /path/to/new-repair-work

The new work directory must be outside `campaign/` and must not already exist.
`run_repair.py` cold-builds from source before running the two paired repair
methods. `verify_scope.py` verifies the three-method source delta, unchanged
saved layout and untouched script intervals, plus 65,536-value scalar checks.
To build without gameplay tests, use:

    python3 -B campaign/reproduce.py --out /path/to/new-build-work

The earlier ten-method gate is still runnable against the repaired program:

    python3 -B campaign/testing/run_suite.py --work /path/to/new-full-suite-work

It was not rerun for this narrow repair; running it takes tens of minutes.
Cold identity alone and historical passes are not a new dynamic or native pass.

## What changed

Exactly three generated gameplay methods change:

- Module 991 `h6BaseDrawWorld`: use the P08 courtyard renderer only in the
  courtyard interior, allowing the actual destination room to paint elsewhere.
- Module 988 `h7DrawBunny`: admit Bunny's valid final kitchen ownership as well
  as a prefinal invitation, while retaining restore, failure, room and apron
  guards. Preserve scalar mouth/facing behavior in the same byte budget.
- Module 988 `h7ReturnBunny`: refuse the obsolete kitchen return action after
  valid final publication, before beginning any transition or owner mutation.
  Genuine invited returns before final publication continue to work.

`source/room_render_fix.py` performs exact old-method guards and substitutions;
`source/derive.py` applies it after existing composition. Frozen inputs, the
compiler, selectors, fourteen heap files, exports, locals, properties, method
entry addresses, relocation data and bytes outside the three method intervals
are unchanged. See `repair/SOURCE-CHANGE.diff`, `repair/BASELINE-SCOPE.json` and
`repair/REPAIR-NOTES.md`. Static address preservation alone is not a guarantee
for arbitrary old or future saves.

## Authoring, history and rights

Edit derivation scripts, `templates/`, `renderer_templates/`, `gate_b_templates/`,
`p09_active.sc.in`, `p10_active.sc.in` or `p10-input/patch/` in a reconstructed
work directory. Generated `src/`, `selectors.json` and `build/` are outputs.
This archive intentionally contains no generated current `build/` directory.
Expected output pins identify this checkpoint; deliberately edited games need
new verification and pins.

The seven-puzzle R3 `p07-host` component, `progress/reproduce.py`, and all other
R3 components are unchanged. Its existing reconstruction remains:

    python3 -B progress/reproduce.py p07-host --out /path/to/new-seven-puzzle-work

`repair/history/` preserves replaced baseline receipts verbatim. Existing
`PUBLIC-ADAPTATION.json`, `PRIVACY-AUDIT.json`, `INTEGRITY-CHECKS.json`,
`R3-REUSE-MAP.json` and `testing/VERIFICATION.json` are also historical receipts;
current repair coverage and exclusions are in `repair/`. The compiler's six
previously audited temporary-directory defaults/examples are unchanged.

Keep this component with the source bank's `LICENSE.md`, `THIRD-PARTY.md`,
`CREDITS-AND-RIGHTS.txt` and existing compiler notices. No new blanket game
license is granted.
