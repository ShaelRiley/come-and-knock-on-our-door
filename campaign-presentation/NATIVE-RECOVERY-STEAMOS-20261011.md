# SteamOS recovery: exact candidate preserved, native input blocked

The interrupted local conversation and private test records were recovered on
October 11, 2026 using GPT-6.1 Sol. The checkout and GitHub reference branch
were both at `9902a33bcb6cf08eeef702646a4ddc1199f06bf1`; there were no newer
tracked edits or staged changes. Existing branches, releases, save folders,
screenshots, recordings and logs were preserved.

## Candidate and installed runtime

The existing compile receipt and all 1,759 staged game files pass the exact
candidate check. The compile receipt remains
`86be8b73aa37587bbc704f3d3722cf60c06a202b73d30c1e828b4ed02995619c`;
the sorted game-file map remains
`269da8264540dab06e88fa1aa087c84448f3e7d548be673b87afdb56fee288ec`.
No game source, compiled resource or runtime asset was changed during recovery.

SteamOS 3.8.16 has the system Flatpak `org.scummvm.ScummVM` 2026.3.0 installed,
at app commit
`6d302a35477722825777671f5254291770876d1393fe27fdf3b90144293250e7`.
Its actual engine binary SHA256 is
`357551b05742a1119087522719e9c1f9ad5624fcc5cd515be9666bc1dab64c5a`.
The installed manifest sources the official release archive and lists only a
desktop metainfo patch for ScummVM. SCI, FluidSynth and PNG support were
verified with the installed runtime's capability commands. FluidR3 GM matches
the required SHA256
`74594e8f4250680adf590507a306655a299935343583256f3b722c48a1bc1cb0`.

The private launcher records its own wrapper hash. That hash is distinct from
the engine binary identity above; both were retained in the private recovery
record. Matching a wrapper or version string alone does not establish engine
identity. The predecessor runtime in NATIVE-ACCEPTANCE-20261011-SCOPED.md has a
different binary hash and its private puzzle-11 save was not recovered here.

## Observed recovery boundary

A surviving genuine New Game process was found in its native opening Save
dialog. Its candidate, installed runtime, SoundFont and session configuration
matched the recovered records. Both pre-interruption test save folders were
empty. The visible Save dialog was used to make a genuine held-opening save;
the resulting game save remains private. The opening returned visibly after
saving. Ordinary Skip, the game menu and its Quit action then worked, and the
runtime log recorded a successful normal close. Restore was not exercised.

Subsequent genuine New Games used separate, initially empty save folders.
Opening frames and the Porch were captured. On the shared Wayland desktop,
pointer movement and the stock ScummVM global menu worked, but repeated game
keyboard and mouse commands did not visibly activate. Inputs that reached
another window, hover highlights and unchanged screenshots were not counted
as completed actions. No additional puzzle, contest or opening-control pass
is claimed.

A separate visible Xwayland display was prepared with the same installed
engine and unchanged game. Its ordinary UI control path remains unverified:
the tool rejected the input request before it reached the game. Its attempted
recording also selected a transient startup window and failed; it is not
full-opening evidence. A current Porch screenshot was captured from the actual
game window. The separate game process was still present at the recovery
boundary; normal exit or saved progress from that run is not claimed.

FluidSynth, 44,100 Hz output, nonzero volumes and unmuted configuration were
retained, and Music was never intentionally toggled off. A live ScummVM output
stream was identified. Isolated acoustic output, subjective listening and a
complete observed Music-ON campaign pass remain unverified on this installation.

## Exact blocker and continuation

The current Codex approval policy disables sandbox approval prompts. Sending
ordinary UI input to the isolated native session returned:

`write_stdin rejected: approval required by policy, but AskForApproval::Granular.sandbox_approval is false`

The same policy rejected the attempted terminal interruption. This is a tool
permission boundary. The earlier shared-display input failure is still
unresolved; the isolated route is not yet a verified fix. No game code defect
or successful workaround is inferred from either boundary.

Restore local execution approvals for the existing development task. Inspect
the surviving process and private records before launching anything else,
then prove visible ordinary input and save/restore. Resume a genuine save only
when candidate, actual engine, SoundFont and effective configuration identities
match. Otherwise use another separate empty Save Path and genuine New Game.

Complete all 14 puzzles, four actual contest wins, P13's four physical cargo
deliveries, the affected late interface regressions, companion travel,
save/restore, ending controls and all 58 credit cards with Music ON. Earlier
scoped observations remain historical; this recovery adds no full-game native
acceptance. Private saves and test artifacts are excluded from this source
checkpoint. No finished player release or download is published.
