# P08–P10 portable dynamic regression extension

This separately scoped extension supplements the unchanged public source-only
campaign closure. `../reproduce.py` remains a cold-build identity check; it does
not execute gameplay. This runner cold-builds the exact fourteen-module program,
then executes the current ten paired regression methods against that build.

## Run

From any directory, with Python 3.12+ and the compiler prerequisites documented
in the campaign source toolchain (tested with Python 3.12 on Linux):

```
python3 -B /path/to/campaign/testing/run_suite.py --work /path/to/new-regression-work
```

The work directory must not exist and must be outside `campaign/`. The source
closure, compiler sources, generation steps and all 111 pinned output hashes
are checked by the existing public reproducer. The harness is copied only after
the cold build passes. Expect tens of minutes, not seconds. The runner refuses
optimized Python, P09 diagnostic cache reuse, P10 development snapshot reuse,
and selector overrides. No network, GUI launch, native runtime, or publication
step is part of this command.

Progress and final results are written to
`new-regression-work/evidence/PUBLIC-REGRESSION-RESULT.json`. Capture stdout/stderr
to retain the detailed unittest and campaign-route log. A cold-build success is
not a dynamic pass. Only terminal status PASS with ten successful methods is a
complete pass of this declared gate.

## Exact scope

- Three P09 methods: actual first-click approach and modal route; exact terms
  units and original-card ownership with restore; stale/foreign metadata and
  fresh post-restore presentation-frame rejection.
- Six P10 methods: two active paper/bread/rack and reader-credit methods, one
  actual installed-cue reorder/undo method, one reserved-action rejection
  method, and the two fresh inactive P09/P10 high-ID/ordinary-save guards.
- One cross-chapter method: genuine P01–P08 prerequisite route, P09/P10
  coexistence, ownership, ordinary mocked save/restore, and cross-chapter
  preservation. The corrected route explicitly performs ordinary Open on the
  closed front door before Walk. Walking through a closed door is not treated
  as a valid test shortcut.

Every selected method runs emitted and source-backed variants. Original tests,
assertions and support implementations are copied byte-for-byte; their hashes
are in HARNESS-MANIFEST.json. The corrected cross-chapter version is the only
cross-chapter method selected. Historical rejected attempts and old receipts
are deliberately not input fixtures for this extension.

The supported entry point is run_suite.py, not broad unittest discovery. Some
support modules retain historical test classes and legacy standalone entry
points verbatim; those are not selected by this bounded gate, and their old
project fixtures are not included. This is the complete current ten-method
P08–P10 acceptance gate, not every historical campaign test.

## Execution boundaries

`tools/host_vm.py` executes freshly compiled SCI1.1 bytecode with typed,
deterministic kernel mocks. `tests/source_host.py` interprets the new P08/P09/P10
state methods and an explicit list of changed bridges, renderer, dialogue and
host methods. Other methods still run emitted bytecode. The precise interpreted
method ownership is visible in SourceVM.__init__; source-backed does not mean
that every campaign method is interpreted.

The tests exercise actual control input, approach/arrival, reader Close,
presentation frames, ownership and ordinary SaveGame/RestoreGame code paths.
StorageBackend/Backend are deterministic kernel implementations. These tests
are not evidence of native pixels, audible output, GUI behavior, native save
files, controller hardware, or ScummVM/native acceptance. No P11–P14 or ending
completion is claimed.

## Prerequisites and cache policy

The fresh runner starts with an empty evidence directory. The genuine
campaign_route.prepared actions earn the prerequisite state; no positive
campaign flags or actor placements are invented to skip that route. Within a
run, snapshots avoid repeating the same earned prefix for every assertion.

The inherited rendezvous fixture may use a disk cache only when its exact
compiled-program identity and creator-file hashes match, and the serialized
state SHA-256 validates. Its origin is the genuine prerequisite route. The
snapshot VM independently rejects a foreign compiled program and malformed
state. These are reproducibility/integrity checks, not a cryptographic trust
boundary against a malicious editor of the local source and cache together.
The canonical runner uses a new work directory, so no preexisting disk cache
is carried into a run; any cache it later reuses was generated in that run.
The original cache checks remain intact. Optional P09 diagnostic and P10
unverified development caches are forbidden by the runner, even though their
historical implementation remains visible in the original support source.

The final result binds all current source, test, oracle and compiled-module
bytes before/after execution and rechecks all pinned compiled/resource outputs.
The compiled receipt remains SHA-256
473d8fb1546d9802825055e4c92b9a6024262be948bdc053d05fea3d3d93a0e1.
