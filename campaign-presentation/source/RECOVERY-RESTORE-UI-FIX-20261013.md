# Restore and late interface repair candidate, 2026-10-13

This is an unaccepted source candidate, with a separate R3 save lineage.
The previous R2 native run began with empty saves and genuinely reached all
four puzzle 13 cargo deliveries and the first scored round of contest four.
It did not win contest four, reach puzzle 14 or the ending, or observe any of
the 58 credits. Its save 37, made during the second-round confirmation,
restored into interface error 10. Original saves and evidence are preserved.

## Restore diagnosis and repair

Read-only stock ScummVM breakpoints on copies of saves 36 and 37 established
that the initial contest-world and puzzle 5 restore validators passed.
Main then rejected at the puzzle 8 restore finalizer. That finalizer recycled
its session lease before projecting prerequisites. The prerequisite query
reentered the active contest's strict late owner chain, whose puzzle 11 owner
still held the previous lease. Main rebinds that owner only after the puzzle 8
finalizer succeeds. The same world was consequently rejected after the lease
changed. Copied-save diagnostics do not count as gameplay acceptance.

`module989.sc`, `h8RestoreFinish`, now projects and validates the restored
context while all predecessor owners still hold the same lease. It then
cycles and binds the lease and performs the original current-context check.
Input/audio retirement, full physical and ancestor validation, failure
handling, reader validation and the later owner rebind remain required.
No progress, arrivals, receipts or owner validity are synthesized.

## Repairs tied to ordinary native observations

- `main.sc`, `uiHostDefaultVerb`, and `module994.sc`, `h12Dispatch`: use the
  ordinary Open action for the cue rack's existing apron menu. The previous
  Walk-to repair lost the rack object in Main's actual action-at-arrival path.
  Explicit Look retains the authored visible-faces reader.
- `module995.sc`, `h13Menu` and `h13Choice`: reflect the required room and
  actual presence of every speaker in reader-choice availability. A private
  stateless helper checks the existing authored token speakers and raw actor
  rooms. Reader admission still performs its complete strict validation.
- `module993.sc`, `h11Controls`: register the visible bodies of three
  relocated actors under their existing owner/room guards, alongside the
  retained text-label controls. Their poses and paint anchors are unchanged.
- `module995.sc`, `h13PaintWorld`: paint the existing actors in front of cargo,
  keep the serving and later status captions inside the visible world, and
  make the eight existing portion cels legible. No asset, pose or cargo state
  changes. The opened viewing panel previously covered Rita and Felix.
- `module991.sc`, `renderCaption`: retire the earlier preparation caption
  after the late owner takes over. Contest HUD priority remains first.

All approved dialogue, opening, score, laugh tracks, art assets, character
poses, ending and credits are preserved. No selectors or classes are added.
The eight protected inputs retain their exact original bytes.

## Supplementary evidence and required native retest

`tests/check_recovery_r3.py` exercises emitted restore-finalizer/context/owner
lease checks, the real default/action/arrival/menu path, and room/speaker
availability. Unrelated ancestor/domain admissions and elapsed walking are
explicit fixtures. All three reference cases reproduced the defects against
the frozen R2 compile. These checks do not earn campaign progress, create
native saves, accept pixels or sound, or establish complete-chain validity.

Fresh compilation of all 46 modules, all four bounded static checks, six
emitted presentation cases, five existing recovery cases, three existing
late UI cases and the three new regression cases passed. Eight protected
inputs and all selector/class identities are preserved. Relative to R2,
86 compiled artifacts are unchanged; only six declared scripts changed.
The largest script/heap pair is 64,992 bytes, below the SCI16 limit.
Fresh staging contains all 1,759 game files and 254 typed resources. A new empty-save
stock ScummVM playthrough is required for all 14 puzzles, all four actual
contest wins, late interaction and save/restore, the ending and all 58 credit
cards. Late-scene performance and subjective audio acceptance remain open.
Publication remains blocked until the complete release criteria pass.

## Recoverable previous build

The prechange backup is under the ignored project path
`build/recovery-backups/20261013T0205Z-before-native-restore-fixes/`.
It already contains all 46 source modules, test sources, build scripts and
input profiles. The untouched R2 `stage` was moved into that backup. An archive-step path
error was followed incorrectly by a compile attempt, which was interrupted
and retained as `interrupted-r3-coherent`. The original 92 script/heap files
were recovered from the untouched stage into `coherent`, with an exact match
to the recorded R2 compile-receipt hash. The original ABI also matches all
46 restored compiler-source identities. No mixed-build tests count.
Native evidence and original saves remain in
`build/native-sessions/20261012-recovery-ui-r2-newgame/`.
The archived runtime path must be used for any later inspection of that old
build; the original R2 INI and its recorded identities are retained unchanged.
