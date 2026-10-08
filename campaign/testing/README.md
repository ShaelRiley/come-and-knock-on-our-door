# Portable campaign regressions

The current narrow repair entry point is:

    python3 -B campaign/testing/run_repair.py --work /path/to/new-repair-work
    python3 -B campaign/repair/verify_scope.py --work /path/to/new-repair-work

Use Python 3.12+ on Linux x86-64 with the pinned compiler's system libraries.
The directory must be new and outside `campaign/`. The runner cold-builds all
14 modules and checks all 111 pinned outputs before copying the harness.
It rejects optimized Python and optional diagnostic, development-snapshot or
selector overrides. No network, GUI or engine launch occurs.

## Current two-method repair gate

Each method exercises emitted and source-backed paths on the repaired program.
The first earns P01–P08 through real control/arrival/reader actions, checks actual
travel and room-background/actor resource selection, and demonstrates that the
old courtyard interception fails on the same legitimately reached living-room
state. It exercises the serving-board and six-page Bunny readers, mocked
ordinary save/restore, final Return refusal with no invitation, and Bunny's
restore/failure/apron/foreign-owner rejection guards.

The second exercises a genuine prefinal invitation and valid return, then earns
a separate final history with the invitation retained. The ordinary menu and
direct legacy Return call refuse without moving Bunny, clearing that invitation
or producing failure; the six-page P10 reader remains usable afterward.

These tests do not inject positive campaign progress to skip prerequisites.
They reuse an in-process genuinely earned emitted P01–P07 prefix for source
admission only after matching the exact compiled program. Later tested actions
execute on their selected backend. Negative cases deliberately invalidate one
field and restore the earned snapshot afterward. The new directory contains no
preexisting fixture cache. The inherited cache may only reuse genuinely earned
in-run state with matching program, creator-file and state hashes. That is an
integrity check, not a cryptographic boundary against a malicious local editor.

The original repair assertions remain intact. Public adaptations replace one
private-path frozen-method lookup with the identical guarded `OLD` source
constant and reuse identical `choice_for`/`read_close` helpers already present
in `test_coexistence_r2.py`. `SourceModule` adds unsigned SCI16 comparison and
interprets both changed Bunny methods. `room_paint_source.py` interprets source
labels/control flow for the mixed-assembly room renderer; it does not replay
preselected draw results. Other unselected methods execute emitted bytecode.

DrawCel assertions prove selected resource IDs, counts and guards. They do not
prove rendered pixels, hotspot geometry, audible output, native saved games or
subjective quality. StorageBackend/Backend are deterministic kernel mocks.
Native findings and their narrower limitations are summarized separately in
`../repair/NATIVE-COVERAGE.md`.

`PUBLIC-REPAIR-RESULT.json` in the work directory's `evidence/` records progress
and terminal results. Only terminal PASS with both methods, unchanged bound
inputs and exact final outputs is the declared repair-gate pass. Structural and
65,536-value scalar checks write `PUBLIC-REPAIR-SCOPE.json` separately.

## Historical wider gate

`run_suite.py` remains available for the ten P09/P10/cross-chapter methods. It
uses current source/output/harness manifests, so it runs against the repaired
program if invoked now. It was not rerun for this narrowly scoped repair.
The terminal receipts in `verification/`, `VERIFICATION.json`, `VALIDATION.json`
and `EXECUTED-CANDIDATE-MANIFEST.json` describe the prior pre-repair program:
compile receipt `473d8fb1546d9802825055e4c92b9a6024262be948bdc053d05fea3d3d93a0e1`.
All ten paired methods then passed in 2,860.142 seconds. Preserve those receipts
as historical evidence. `../repair/verification/` holds the new repair results.

Use these entry points instead of broad unittest discovery: some retained
support files include historical test classes requiring fixtures outside this
bounded public closure. No P11–P14, ending, accessibility or whole-game
acceptance follows from either portable gate.
