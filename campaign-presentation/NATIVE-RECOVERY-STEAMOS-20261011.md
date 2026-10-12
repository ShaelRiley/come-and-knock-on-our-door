# SteamOS recovery: exact candidate preserved, native input blocked

## Recovery after the machine restart

The later recovery found a clean checkout on
`work/steamos-native-recovery-20261011` at local commit
`9f06852234aaaecb95d874e91f445a5cd03ea859`, newer than the preceding handoff's
`9902a33` reference. No reset, branch replacement, pull or merge was performed.
The opening save, private evidence, and exact staged game survived the reboot.
A project-scoped private archive and Git bundle were made under ignored
`source/build/recovery-backups/20261011T230820Z/` before further native tests.
No old task game or recording process was found running after reboot.

The missing restart instruction was recovered verbatim from project session
`01a12c9a-d764-7562-86bc-7162745a2aab`:

```sh
codex resume 01a12c9a-d764-7562-86bc-7162745a2aab --model gpt-6.1-sol --cd /home/deck --sandbox workspace-write --ask-for-approval on-request --approve-for-me
```

This was a SteamOS-host instruction, not a container command. Installed Codex
0.162.1 help confirms those options. `--approve-for-me` routes approval review;
it does not disable the sandbox. The recorded failed operation was ordinary
game input through `write_stdin` to task terminal 31243. The prior session's
granular policy had `sandbox_approval: false`; even its later interruption
request was rejected by that policy. The keyboard failure's cause is unknown.

The current session successfully obtained narrow desktop and network approvals
and launched the installed runtime. A restart is not currently necessary.
Git command-line pushing separately failed because its configured
`/usr/bin/gh` credential helper is missing. The connected GitHub tool banked
the preserved source tree on the existing recovery branch at
`5e8204ba3338b4a0632c1380ad8f4f28c80d68d5`; its tree
`e81904b4d5c7159a6c5d960fe2e9ad2dfdd9796f` exactly matches local `9f06852`.
Different commit metadata explains the different commit ID. Local history was
preserved; no force push or finished player release was made.

Current host inspection reports SteamOS 3.8.28. Candidate, installed engine and
SoundFont hashes below were verified again. A new bounded private launcher
uses a separate, visible, windowed Xwayland display, records its own process
IDs, and cleans up only its children on stop, EOF, idle timeout or deadline.
No automated input is directed into Konsole or approval dialogs. Screenshots
from its first smoke test visibly demonstrated opening Hold, Next, Skip,
the game menu and ordinary Quit; ScummVM recorded a normal close. Its Save
request was captured before the chooser appeared and was not counted as Save.

Later isolated tests visibly reached the native Save chooser. Mouse selections
did not visibly work. No new save, restore, puzzle or contest pass is claimed.
Tests closed through the recorded cleanup paths. The control investigation
tested SDL's process-local `SDL_VIDEO_X11_XINPUT2=0` setting in the unchanged
SDL implementation. With that setting, directed normal mouse events selected
New Save and opened the name dialog; Enter created an isolated genuine opening
save. Ordinary F3 and saved-card selection returned to the saved opening.
The following complete automatic opening ran to Porch with full motion and
Music ON. A second genuine save was made there; ordinary Space visibly enabled
the scene's hotspot labels. Evidence remains private under
`source/build/native-sessions/20261012-input-diagnosis-core/`.
Load of the Porch save visibly restored REVEAL from the changed HIDE setting,
the original caption and the closed-window scene state after a conversation.
Puzzle 1 subsequently completed through ordinary visible actions and actual
Living arrival. A genuine third save preserves that progress. The separate
display later closed; ScummVM exited with XIO and code 1, without a recorded
engine error or normal log close. Its cause is unresolved and normal Quit is
not claimed for that run. The opening and Porch saves also remain intact.
These are scoped control/Save/Load/opening/P01 observations; P02-P14, all four
contest wins and late acceptance remain incomplete on this installed runtime.

The sections below retain the preceding session's historical observations and
permission boundary; references to a live process or disabled approvals there
describe that earlier boundary, not the current post-reboot state.

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
