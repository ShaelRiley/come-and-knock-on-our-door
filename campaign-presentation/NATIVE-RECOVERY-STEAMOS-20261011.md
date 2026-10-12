# SteamOS recovery and scoped native testing

## New repaired candidate: observed puzzles 1–4

The new isolated New Game uses receipt
`e65a343b88de7b3a049bdced423aef2f586ed76cc39aff8a988a2bd8cc4cb909`,
map `0c285097cc5cd04824d69ec365e90256f22cba6154c01089b71333545cfdb95d`,
and lineage `CAKOOD_PRESENTATION_RECOVERY_UI_FIX_UNACCEPTED_20261012_R2`.
The source repair is banked at local `c6c545109a4b402e9fd9762982efce33ecf1af84`
and GitHub `1f73f16795db2ee0f7965f3f45de53b45f21f06e`, with identical tree
`32b7db4367e3cee0b746157c3c0a4a9cfb0a8eed`.

This run began with empty saves, automatic New Game and the unchanged stock
engine. It reached Porch and created save 1. A REVEAL change followed by Load
visibly restored the original scene and setting. The first tool terminal later
became unavailable without its final cleanup record; its cause and exit code
are unknown. Its recorded process IDs were absent, and a read-only search for
this exact session's config argument found no remaining game. Work and saves
were preserved before relaunch. An initial fresh Load request stayed in the
chooser; the corrected ordinary saved-card selection visibly restored save 1.

Puzzles 1–4 subsequently completed through ordinary controls. Puzzle 2's full
six-card agreement, puzzle 3's full six-card scene and puzzle 4's full five-card
scene were observed. Five genuine saves exist. Slot 5 preserves puzzle 4
(103,261 bytes, SHA256
`4f6800103434b37d2535315a13eaac3a6b7a3f8dbcdde9d02c118ab5bd7db4c6`).
Ordinary game Menu/5 Quit at 19:05:55 UTC returned engine0 and task-server0.
The menu visibly retained Music, Voice and Effects ON. No subjective listening
claim is made, and opening Hold was not verified in this new run.

Wrong input-field requests, status-only actions and attempted travels that
remained in the departure scene are excluded from acceptance. Private evidence
records their corrections. No debug commands, state setters, imported saves
or save patching earned any of this progression.

Next: archive and empty the queue, resume this exact lineage through ordinary
F3 Load of slot 5, and complete puzzles 5–14, all four actual contest wins,
repaired late UI, critical late save/restore, ending/freeze/applause and all
58 credits. No completed player release is published.

## October 12 source repair and next native run

The frozen preceding run later completed the ordinary puzzle 13 preparation
visits and handoff. Slot 33 preserves that boundary (130,072 bytes, SHA256
`d3f4b4367627811816c1629a8f920e3f2efef1e07055818adbfbd6a0853b1af2`).
Only guest-program page 1 of 2 was observed; the Next request stayed on page 1.
No physical puzzle 13 delivery was completed. Several travel captures remained
in the departure scene, despite their intended destination filenames. Later
captures verified actual Living arrival. Ordinary game Menu/5 Quit returned
engine0 and task-server0 at 17:55:17 UTC. No original task game remains running.

A scoped main-thread sample at 17:48:23 measured 97.95% CPU. A separate read-only
diagnostic restored an unmodified copied slot 33 and logged repeated descendant
and ancestor validators during idle playback. Its first blank-card selection
is excluded from restored-save evidence. Counts include diagnostic overhead and
memo hits; no speed improvement or acoustic acceptance is inferred from them.

Before changing canonical inputs, the frozen source, build, stage and manifests
were backed up under the ignored project recovery-backup directory. All prior
saves, branches and evidence remain preserved. The October 12 repair is now
applied, compiled and staged privately in a new unaccepted save lineage.
source/RECOVERY-UI-FIX-20261012.md records the four affected source modules,
strict proof reuse, test fixture limits and process-local input workaround.
Four static, five targeted emitted and three existing late UI cases passed.

Next: begin a separate stock-ScummVM New Game using empty private saves and
verify the repaired candidate through all 14 puzzles, four actual wins, late UI,
changed-state save/restore, ending/freeze/applause and all 58 credits. Earlier
native observations and saves apply to the preserved frozen candidate only;
they cannot verify changed compiled scripts. Subjective listening and controller
hardware acceptance remain unperformed. Publication remains blocked.

The following sections preserve the earlier recovery and native history.

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

## Current installed-runtime progression on October 12

The latest continuation completed all five physical P11 transfers and its
practical scene through ordinary controls. A supported-display save was followed
by a changed state and native Load; the supported state visibly returned. Separate
slots 24–26 preserve these boundaries. The third contest's six new practice
exchanges were fully observed, and slot 28 preserves all 18 learned replies.
The intermittent scored-match input was investigated on an isolated copy of
slot 28, using read-only diagnostics. Raw keys reached the focused task window;
SDL recorded a large controller-axis flood while ordinary game events stalled.
The comparison run with process-local joystick disabling removed the axis flood
and responded to ordinary Close, Return, global menu and Quit. This identifies
a usable input workaround, not the controller hardware's underlying cause.

The original acceptance session then resumed with only its isolated INI's
`joystick_num=-1` setting changed. The regular launcher, engine, game bytes,
unmuted audio and genuine save lineage remained unchanged. Three native scored
rounds, knockout, explicit third win, concession and complete flourish were
observed. P11 is complete; slot 29 preserves that boundary (122,097 bytes,
SHA256 `2a45643c54897dbc6c93c833127f63730ef6e0143550e7c954ef95b09cef5543`).

All seven P12 guests were physically gathered through ordinary invitations and
travel. Slot 30 preserves that state (122,107 bytes, SHA256
`4803d9c6d9b1d86a98e426976e99ddfaf79e9daebf8b2fce9ec0b52c609f9928`).
The three welcome-review cards were subsequently observed but not saved. The
latest run ended at its 30-minute lifetime limit at 17:00:45 UTC, before the
queued Save31 and Quit executed. Slot 31 does not exist; normal Quit is not
claimed for this run. The task engine was terminated by the bounded launcher,
whose own server then exited normally. A scoped process sample during that
reader found the SDL audio thread busy; its cause remains unresolved. It does
not establish a game-validator performance defect or subjective audio acceptance.

The following native run completed the full welcome, mechanism repair,
eight-card introduction, visible confetti, five-card shared scene and four-card
cleanup. All seven collection handoffs were observed, including actual travel
and visible arrivals where a room change was required. The game admitted the
P13 menu afterward; its initial handoff remains gated until its ordinary
preparation visits. Slot 32 preserves this boundary (127,394 bytes, SHA256
`9fff4101c5ff2c23c29a5b429c3636bacb3e9091829f6ecc63b57320399b6874`).
Slot 31 (125,548 bytes, SHA256
`5093f18045756b61a426a595b94a584483a32a60c84fe8b6c268aed55605dc02`)
was saved after the mechanism repair, a viewpoint change was made, and ordinary
Load restored the saved mechanism and viewpoint. P12's main progression is
complete, but its optional rehearsal menu was inaccessible: native Walk-to Rack
on the audience apron opened no menu, and the sole source caller excludes that
viewpoint. A scratch repair exists privately; it is not applied or accepted.
The engine then closed through the game's own Menu/5 Quit control at
17:39:21 UTC, with engine and task-server exit code 0. The earlier Ctrl-F5
request did not visibly open the runtime menu and is not counted as an exit.

Next: archive and empty the old queue before relaunch, restore genuine slot 32
through F3 (chooser page 6, top-right), and complete P13–P14, VC04, the remaining
late UI, ending and all 58 credits. Repair the two P09 issues and the unreachable
P12 menu, then retest the changed candidate. All saves and diagnostic artifacts
stay private. Full native acceptance remains false; no player release was made.

The earlier progression in this genuine New Game lineage completed
puzzles 1 through 10 and two actual contest wins in the installed, unmodified
ScummVM engine identified below.
The automatic opening ran fully with Music ON and full motion. Ordinary Save,
Load, inventory, room travel, document pages, plan choices and the completion
exchanges were visibly reviewed. New isolated native saves preserve each puzzle
boundary. The P04 save is `cakood-native.008`, 103,146 bytes, SHA256
`4c1408578ba0c843ff0ddeec598e1c59c802e70c7d4dac4ea69060d23de3b81f`.
The later P07 boundary is `cakood-native.016`, 105,581 bytes, SHA256
`95309f27f5b05ec08f458d1155362db1f7d2e15329c37ad861f67de7a96fdb10`.
Both are private under the existing `20261012-input-diagnosis-core` session and
are excluded from the public tree. `SAVE-IDENTITY.json` and `PROGRESS.md` there retain
all earlier save identities and the continuation instructions.

The P04 boundary was saved after the complete exchange. The ordinary game
menu's Quit then returned engine code 0; the bounded launcher recorded its own
server cleanup and the runtime log closed normally. No Music unavailable,
missing authored-audio or fatal engine warning was found in the inspected log
through this boundary. The live task audio stream was independently identified
as unmuted, uncorked 44,100 Hz stereo output. These are scoped runtime and output
observations, not subjective listening or exact acoustic/timing acceptance.

Observer corrections: a selected world action can still be walking; issuing
Escape early cancels it. The game REVEAL controls identify current art-specific
rectangles, which supersede older reference coordinates. A placed document can
overlay a board target. Inputs ignored by an open reader did not count as
progress. In the private launcher, a file queue is reopened from its beginning;
archive and empty it before each resume. Check terminal completion before a new
launch; an older run's final display record can overwrite the same session file.
One earlier continuation ended at its recorded idle timeout while an independent
approval was pending. It was replayed through ordinary controls from the verified
P01 save; no state shortcut or imported predecessor save was used.

Fresh-process native Load of the P04 boundary passed. The first contest's
pending reply was saved, changed, then restored through F3; the original reply
and both scores returned. The P05 and P06 contests reached actual knockouts,
explicit recorded wins, concessions and progression. Their completed boundary
saves are slots 12 and 15. P07's full source document, physical preparation and
character scene were observed, followed by its completed-state system response.
Ordinary game Quit after the P07 save returned engine and task-server code 0;
no task game remains running at this boundary. Music, Voice and Effects were ON.

One P06 continuation ended at the recorded 180-second idle limit during evidence
review. Its unsaved actions were repeated from the genuine P05 save, using normal
controls. A wrong inventory-slot click did not complete assembly and was not
counted as progress. The clip exchange's first page was observed; the whole
multi-page clip dialogue is not claimed. The subsequent complete demonstration
and loan exchanges were reviewed. Screenshot captures and task-window recordings
remain private, along with the saved input audit and process identities.

P08's physical setup, readiness exchange, ordinary evening confirmation,
game-created pre-evening save and complete evening exchange were observed.
P09 reached its complete terms and success exchange and its physical card;
both card pages were reviewed. P10's physical ceramic assembly reached its
success exchange, with all seven available source readings reviewed. Genuine
slots 21 and 22 preserve those chapter boundaries. At that earlier boundary P11 was in progress:
three actual companion/object transfers reached their destination visibly.
Slot 23 preserves those transfers. Normal Quit after this save returned engine
and task-server code 0; no task game remains at this boundary.

Two defects are pending correction and native retesting. Selecting a retained
earlier Stringer topic changes the conversation context from 239 to 202 while
keeping the later menu IDs. Returning to that menu can route a new choice to
the earlier handler; closing and reopening the conversation visibly restores
the correct route. The physical renewal card also displays the generic ITEM
inventory label because the host label dispatch excludes object 399. The
candidate was not edited during these observations. Neither issue is counted
as a passed UI regression. Private screenshots, saves and operating records
remain excluded from the source checkpoint.

That earlier continuation resumed slot 23 before reaching the latest boundary
reported above. Full native acceptance remains false. No completed player
release has been made. Subjective listening remains unverified.

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
