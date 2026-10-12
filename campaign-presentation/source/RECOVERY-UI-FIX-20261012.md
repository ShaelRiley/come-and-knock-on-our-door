# Recovery UI repair candidate, 2026-10-12

This is an unaccepted source candidate. The preceding frozen candidate reached
puzzles 1–12 and three actual contest wins in an isolated, genuine New Game run.
Its puzzle 12 rehearsal was unreachable, puzzle 13 had no completed deliveries,
and puzzle 14, contest four, the ending and all 58 credits remained unaccepted.
Old native saves embed the preceding scripts and cannot accept these repairs.
A separate genuine New Game run is required for this candidate.

The frozen source, compiled resources, stage and build manifests were backed up
under the ignored project build directory before any canonical changes. Native
saves and evidence remain in their original isolated session. No assets, approved
dialogue, score, laughs, character presentation or ending are changed here.

## Changes tied to observed defects

- `module990.sc`, `h9Choice`: an earlier topic delegated through context 202
  retained later menu IDs but lost their owner. Restore context 239 if the
  earlier handler still has context 202; preserve deliberate transitions such
  as context 205. Native captures 336–344 document the preceding wrong routing.
- `main.sc`, `uiHostItemLabel` and `uiHostShortLabel`: include the existing
  renewal and repair card, object 399, in label lookup. Use its authored full
  name and the compact label `TERMS`. Do not extend any physical geometry range.
  Native capture 367 documented its fallback `ITEM` label.
- `module994.sc`, `h12Dispatch`: ordinary Walk-to on the cue rack opens its
  already-authored menu on either side of the audience edge. Look-at on the
  apron keeps the visible-faces reader. Native capture 720 showed the missing
  apron menu. Its existing source 8 rehearsal was never observed on that build.
- `module995.sc`, `h13Valid`: keep strict `h13Historical`, which first validates
  the predecessor and compares all 2064 predecessor words and 199 pot words.
  Require collection phase 2 explicitly. Compare the seven actor origins with
  the identical, just-checked predecessor rooms at history indices `88+12*i`.
  These indices are `2 + 84 + 2 + 12*i`: two lease words, seven first-phase
  actors, and the collection actor's current-room field. This removes seven
  redundant calls through `h12SuccessorRoom` and its full ancestor validation.
  All actor, revision, unused route-tail, work, cargo, delivery and frame checks
  remain, as do the strict render-close rechecks. No new memo or weaker proof.
- `module995.sc`, `h13ReadyPhysical`: deny unfinished chapter state and active
  work before calling the expensive physical predicate. A ready chapter still
  requires every original strict predicate, scene paint and cargo condition.

The isolated session creator also retains the observed process-local
`joystick_num=-1` workaround for future test sessions. This avoids the controller
axis flood seen in the read-only input diagnostic. It changes only the test INI;
it does not establish controller hardware acceptance or change host settings.

## Evidence and limits

The frozen compiled program reproduced all three UI defects in targeted emitted
tests. Its origin test made seven repeated ancestor-room queries, and unfinished
readiness called the physical validator. These tests explicitly model ancestor
and domain admissions; they do not validate the complete ancestor chain, earn
campaign progress, create native saves or establish native acceptance.

In the genuine frozen run after the puzzle 13 handoff, a process sample measured
the main thread at 97.95% CPU and ordinary controls became substantially slow.
A separate read-only diagnostic restored a copied, unmodified save 33 and logged
repeated puzzle 13, puzzle 12 and earlier-owner validations during idle playback.
Breakpoint counts include memo hits and logging overhead and are not a timing
benchmark. The first diagnostic attempt selected a blank chooser card and is
explicitly excluded from restored-save evidence.

Compilation, preservation checks and emitted regressions will be recorded
separately from the new stock-ScummVM playthrough. Performance improvement,
repaired interaction, visual/audio behavior and complete campaign acceptance
remain unverified until observed. Publication remains blocked.

The fresh 46-module compile passed. All four bounded static checks and all five
targeted emitted regression cases passed, as did the existing three late UI
cases. The repaired emitted origin case makes zero additional ancestor-room
queries and rejects 17 forged origin/route/phase/admission variations. These
results remain supplementary evidence with the fixture limits stated above.
