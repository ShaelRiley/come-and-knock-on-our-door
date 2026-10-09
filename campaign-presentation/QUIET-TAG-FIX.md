# Quiet-tag exit correction and player documentation: unaccepted source

This revision is compiled and statically reviewed only. No native execution, staging, portable game-model or internal test-harness execution was performed for this candidate. Full-game native verification, including the campaign ending, remains incomplete; this is a verification limit, not a claim that the ending is unimplemented.

Save lineage: CAKOOD_QUIET_TAG_FIX_UNACCEPTED_20261009_R1. Save compatibility is unproved. Start a genuine New Game with a separate save directory when this candidate is approved for runtime validation; do not import predecessor saves.

## Source correction

In source/src/module996.sc, the quiet-tag exit predicate now checks the original object against the existing OBJ_EXIT_LIVING constant (18). The former expression looked up an exit after the host had already moved from courtyard 4 to living room 1 and therefore resolved -1. Existing phase, custody, prior/current room and exactly-one-revision-increment guards remain in place. This is the source-level cause and proposed correction; runtime behavior has not been verified.

source/src/module999.sc only corrects a stale comment about the ending director. Its emitted script and heap remain identical. The build profile declares a separate unaccepted lineage. Coverage pins bind these edits, stage.py and four player-document templates. The staging script now selects the player-facing LICENSE, CREDITS, PLAYER-GUIDE and RIGHTS-CONTEXT templates. Those files are source templates for future packaging, not evidence that any player package has been staged or accepted.

## Compilation and static evidence

All 46 modules compiled with the pinned compiler. Only module 996's emitted script changed; all 46 heaps and the other 45 scripts are byte-identical. Module 996's combined allocation decreased from 56,758 to 56,750 bytes. Local declarations, initial values, offsets, exports, selectors, class owners and object layouts remain unchanged. Twenty method addresses and five script relocation entries move by -9 bytes; the relocation-table offset changes from 48,332 to 48,322. These code-address changes mean unchanged heap layouts do not establish save compatibility.

Compiler receipt SHA256: afc13f32aaf19d338aef7e2ea5df77f4db9f3b9c866fdef5c1cb7a1763d96c78. Compact compile and static comparison records are in checks/quiet-tag-fix/. Rebuilding source with the existing build.py entrypoint is authoritative. No runtime binaries or large generated ABI duplicates are part of this delta.

## Historical observations and remaining work

FINITE-MIDI-NATIVE-STATUS.md describes the earlier CAKOOD_ORDINARY_FINITE_FIX_20261009_R1 build and compile receipt f67cfaa896ec9c01f751a80b597af9bb693f02723ef8892cda550877f0d764d0. Its genuine New Game, opening, P01/P02 and save/restore observation does not validate this changed candidate. The runtime information in the player guide identifies that earlier observation, not a launch of this revision.

Native acceptance, full-game and ending verification, save/restore coverage and exact audio/cue validation remain unperformed for this candidate. Subjective listening remains unperformed. Technical compilation and static comparison do not replace these checks.

All historical rights qualifications remain. Read LICENSE.md, CREDITS-AND-RIGHTS.txt, CREDITS.txt and rights/ together; source/player-package/RIGHTS-CONTEXT.md explains the future player package's corresponding records. No blanket game or user-provided-music license is added.
