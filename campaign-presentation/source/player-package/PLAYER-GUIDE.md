# Come and Knock on Our Door: player guide

This is an unaccepted work-in-progress candidate. Packaging and earlier bounded runtime observations are not a completed full-game playtest or a release acceptance. Read `GAME-MANIFEST.json` for this package's status and save-lineage identifier.

## What is included

Keep the package together. `game/` contains `resource.map`, `resource.000`, and the loose audio/sync files. `CREDITS.txt`, `LICENSE.md`, `RIGHTS-CONTEXT.md`, and `rights/` accompany those files. ScummVM, FluidSynth, the FluidR3 SoundFont, and compiler/source tooling are not bundled.

## Runtime and music

Install a ScummVM build with the SCI engine and an actual working FluidSynth music device, plus the FluidR3 GM SoundFont (`FluidR3_GM.sf2`). Select FluidSynth explicitly as the music device and select that SoundFont. Leave game Music ON; use audible music and game volume settings. Matching the ScummVM version alone is insufficient: the inspected Debian 13 build lacked FluidSynth support.

The bounded native observations used a locally built, unmodified official ScummVM v2026.3.0, source commit `fed42f2068dcafc6aafa1c28c77e4c88def74b66`; the observed executable's SHA-256 was `329e467e8714cba4c4eafbabdfa84ae4c7c7496062cd41bdc8cdfac4a7d031a6`. Its runtime selected `--music-driver=fluidsynth`, the FluidR3 GM SoundFont, and a 44,100 Hz output rate. This identifies the observed runtime, not a promise that every build with that version or another operating system has equivalent capability. Neither that runtime nor the SoundFont is supplied here.

## Add and start the game

1. Extract the package without changing the files inside `game/`.
2. In ScummVM, use Add Game and select the package's `game/` subfolder, not the package's top folder. The engine is SCI (`engineid=sci`) and the game ID is SCI fan-made (`gameid=sci-fanmade`).
3. Create a new, empty save folder used only by this exact candidate. Set this game's Save Path to that folder. Do not share a predecessor's save directory.
4. In the game's ScummVM settings, explicitly select FluidSynth and your installed `FluidR3_GM.sf2`. Use a 44,100 Hz output rate where the build exposes that setting. Ensure music is enabled in ScummVM and Music is ON in the game.
5. Start the game from a genuine New Game. Do not import or load a predecessor save to skip the opening or reach a later scene.

Prior builds belong to separate save lineages. Compatibility with their saves is not established and must not be assumed. New saves belong only to the exact candidate that made them; successful saving/loading across the full campaign remains a release check.

If FluidSynth is absent from the selectable devices, use a build that actually includes it. If music is silent, check the selected device, SoundFont path, game Music ON state, volume and system audio output. A visible game window does not prove correct music playback. Report the runtime build, package identity and the scene where a problem occurred.

## Normal controls

Use the visible action buttons and scene targets with the mouse. Select verbs such as Walk To, Look At, Talk To, Pick Up, Give or Use, then the relevant object or person; follow the displayed sentence for actions requiring another target. Right-click uses the default action.

During ordinary gameplay, Tab / Shift-Tab moves focus; arrow keys navigate focus or the displayed panel; Enter activates the focused control; Esc cancels or goes back. In the scene view, outside dialogue and other panels, Space shows hotspots and H opens hints. M opens the menu, F2 saves, and F3 loads. Active scenes and panels can use their own controls or temporarily disable an action; follow their on-screen labels.

During the opening, N advances, H or Space holds/resumes, X or Esc skips, and T toggles reduced motion. The matching on-screen buttons are also available. F2 saves and F3 loads through the game's supported controls.

Y toggles music; + and - change game volume. During ordinary gameplay, A toggles the audience, V toggles voice, [ and ] adjust voice level, E toggles effects, and comma/period adjust effects level. Enabling voice takes effect on the next line. Use the displayed controls and accessibility options as needed.

## Credits and status

Read `CREDITS.txt` for the people and individually attributed material, `LICENSE.md` for retained rights, and `RIGHTS-CONTEXT.md` for the scope of historical provenance records. Their presence does not grant new redistribution rights or imply full-game acceptance. A fresh build, staged membership verification, exact-runtime launch, genuine New Game playthrough, save/load coverage and objective audio checks remain separate checks for any new candidate. Subjective listening was unavailable and remains unperformed; numerical audio measurements and native runtime checks do not replace it. This is a disclosed validation limit, not a claim of listening approval.
