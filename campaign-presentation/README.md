# Come and Knock on Our Door: reconstructed candidate, native acceptance pending

Recovery after the SteamOS restart preserved local checkpoint `9f06852`, the
surviving opening save and private evidence. All 1,759 staged game files still
match the frozen candidate. The preserved source tree is banked on GitHub at
`5e8204b`; local history was not reset. Installed stock ScummVM 2026.3.0, SCI,
FluidSynth, PNG and the required SoundFont were verified again. Narrow execution
approvals now work. A separate bounded windowed display and SDL's process-local
core-X11 setting demonstrated ordinary game input and genuine Save/Load.
The complete automatic opening has reached gameplay. Full campaign acceptance
remains in progress; the current installed-runtime New Game has completed puzzles 1–4, with genuine boundary saves and normal Quit. No completed player release is published. See
NATIVE-RECOVERY-STEAMOS-20261011.md for recovered restart instructions, exact
permission diagnosis and scoped observed results.

For native continuation, `source/native_session.py` verifies the exact staged
candidate and prepares a separate stock-ScummVM session with private saves.
All six launcher guard checks pass. See NATIVE-SESSION-20261011.md for developer
setup and resume commands. Inspect surviving processes and saves before
launching another game. The helper does not establish native acceptance.

The earlier October 11 reconstruction reproduced all 46 modules and the complete staged game. Four static cases and six emitted presentation regressions passed. That earlier workspace lacked a native desktop and did not launch a game; RECOVERY-20261011.md and checks/recovery-20261011/RESULTS.json retain its historical results. The later SteamOS recovery above launched the installed runtime, but did not complete the required campaign playthrough. No completed player release is published.

All 46 modules have compiled and staged. A genuine New Game on frozen source `7ccc3c1f2348419536646582d2029cf3f7956bca` completed the automatic opening, puzzles 1–11 and three actual contest wins with Music ON. Genuine saves/restores and opening controls passed. Puzzle 12 was in progress; Bunny's escort survived the labelled left ENTER and physically reached Living. The live terminal then disconnected, and read-only workspace recovery did not complete. NATIVE-ACCEPTANCE-20261011-SCOPED.md records the scoped passes, observer corrections and exact testing boundary. Puzzles 12–14, the fourth contest and the complete ending/58 credits remain unverified. No completed player release is published. If private saves cannot be recovered on identical game bytes, reconstruct this public source and repeat a genuine New Game in an empty Save Path. LATE-UI-FIX.md documents the source corrections. Earlier reports remain historical evidence.

This is an editable work-in-progress source snapshot. It combines the performed opening, approved-direction full score, natural audience reactions and material-specific Foley with the existing campaign. It is a new save lineage and must begin with a genuine New Game.

The snapshot is source and asset work, not a declaration of native full-game acceptance. FINITE-MIDI-FIX.md and FINITE-MIDI-NATIVE-STATUS.md retain historical information about the earlier finite-MIDI build; that runtime coverage does not validate this changed candidate. The included status manifest distinguishes completed objective checks from checks not yet performed. Subjective listening is unperformed because the available audio-input path does not support it; numerical audio measurements do not substitute for that judgment.

Build the exact candidate with Python 3 and the bundled pinned Linux x86-64 compiler:

    cd source
    python build.py --candidate

The builder checks exact source/resource/audio membership, protected resource identities, the original class universe and the 65,535-byte script/heap limit. It refuses a partial presentation or timing-fixture art. The staging script copies the four player-facing documentation templates and refuses to overwrite a prior stage. Fresh static staging has been reproduced; it does not establish native acceptance.

All eight individually credited fictional writers, the original cast, existing puzzle/contest progression and actual-date speech controller are preserved. Hold, Next, Skip, save/load, accessibility settings and replay use the shared host lifecycle. Music and picture retain their separate observed clocks and are never made consistent by patching save files.

Third-party licenses and source qualifications are in CREDITS-AND-RIGHTS.txt, LICENSE.md and rights/. No new blanket license is selected for the game or user-provided music. Compiler corresponding source and notices remain under source/toolchain/source.

The complete source contains 46 SCI modules, 64 distinct opening action poses, 24 source-labeled audience performances, material Foley, the recorded final applause mixture and 58 credit cards. Fresh staging includes player-facing credits and offline license texts beside the game files. It remains a candidate for native acceptance, not a finished player release.

Editable art/audio inputs are under authoring/. Editable score inputs and portable score checks are under source/authoring/score and source/tests/score. See source/tests/README.md for bounded checks. Project source and asset files are pinned in PUBLIC-MANIFEST.json. PUBLIC-PROVENANCE-REVISION.json records the historical baseline sanitization; its earlier compiler and runtime claims do not apply to this correction. Runtime assets are included, so the game build does not fetch external content. Optional asset regeneration uses the dependencies named in each authoring README.

The ending’s music preserves the 48.2-second quiet-household cadence even if the player reaches early credits quickly; credits music then enters at actual completion. Next and Skip remain responsive, and all text/credits remain available when music is muted.
