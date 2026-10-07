# Come and Knock on Our Door: WIP source bank revision 2, 2026-10-07

This is an editable development source checkpoint, not a new playable release.
The last tested player release is the five-puzzle checkpoint at commit
`ab65f4a6f3aea28ba849a0a99074a989cdeef458` and tag
`v0.5.0-checkpoint-20261006-r2`. Its source/data/compiler dependencies remain
preserved here. Its public main/tag are outside this source preparation.

## What is banked

`progress/` preserves isolated P06/P07 host work, P08 domain and scene data,
responsive Music R3, P09 reference model/domain/scene data, editable courtyard
art masters, and a separate Milo approach correction. These components have
different acceptance scopes. None is silently composed into the five-puzzle game.

**Selected P08 source:** corrected Gate2b2 distinguishes completed screen object 81,
Vivian's COURTYARD PLAN object 83, and miniature token 80. The original component
completed its fixed 22-case source/emitted gate; this public edition's fresh
22-case affected gate also passes. Earlier Gate2b1 is no longer selected.
Ordinary Main save/load/replay is exercised through deterministic kernels, with
no native save I/O, meeting, readiness or E03 acceptance. The preserved courtyard
art contract contains an obsolete proposed screen identifier; use the selected
host's current identity map. See `progress/docs/STATUS.md` before integration.

## Reproduce one isolated component

Use Linux x86-64, Python3.10+ without optimization and ordinary C++ runtime
libraries. Art conversion additionally uses the exact packages listed in the
art component's requirements. No download or installation is performed.

```sh
python3 progress/verify_source.py
python3 progress/reproduce.py p09-domain --out /absolute/new/p09-build
python3 progress/reproduce.py p09-domain --phase test --suite codec --out /absolute/new/p09-build
```

Each output folder must be new for a build. Components are materialized into
writable isolated trees using hash-checked relative mappings; duplicate frozen
inputs are stored only once. A build verifies its generated/emitted files
against explicit expected hashes. It neither launches ScummVM nor creates a
player release. The bounded test commands are documented in
`progress/docs/REPRODUCE.md`. Source edits need new identities and fresh tests.

The unchanged root `reproduce.py` still reconstructs the tested five-puzzle
baseline. Read `progress/docs/BASELINE-README.md` and the existing `docs/` for
that baseline's exact reproduction and native scope.

## Rights and provenance

The original game has no new blanket license. Existing `LICENSE.md`,
`THIRD-PARTY.md`, `CREDITS-AND-RIGHTS.txt` and all required third-party notices
remain. Every compiler invocation uses the exact pinned executable whose
build-verified minimal corresponding source is in the baseline toolchain.
Broad vendor/GUI trees and proprietary Prof-UIS are excluded.

`progress/docs/PUBLIC-EDITION.md` explains the deliberately trimmed public
edition, frozen dependencies, generated audio, exact source changes and scope
limits. This is a new source edition; it is not a byte-identical copy of an
internal development package.
