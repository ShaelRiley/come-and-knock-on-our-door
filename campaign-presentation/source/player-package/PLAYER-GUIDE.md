# Come and Knock on Our Door: player guide

Keep the extracted folder together and start the game with `launch.sh`. The launcher checks the game files and runtime, selects the bundled music SoundFont, and keeps this game's settings and saves separate from other ScummVM games.

## Install and launch on Linux or Steam Deck

Use Steam Deck Desktop Mode with Steam running. The launcher requires Python 3 and stock ScummVM 2026.3.0 with SCI and FluidSynth support. Python 3 is present on the tested Steam Deck; on another Linux system, install it through that system's software manager if `python3 --version` is unavailable.

If ScummVM is not already installed, install the Flathub application through Discover or Konsole:

```sh
flatpak install --user flathub org.scummvm.ScummVM
```

The launcher checks the installed version and capabilities before opening the game. If Flathub supplies another version, that version has not been established as equivalent for this release. The required tested version is 2026.3.0.

Extract the release archive, open its extracted folder in Dolphin, and use **Open Terminal Here**. Check the package and runtime, then launch:

```sh
./launch.sh --verify-only
./launch.sh
```

The game starts windowed so the ordinary close button remains available. To request full screen, use `./launch.sh --fullscreen`. ScummVM and FluidSynth remain external dependencies. The exact FluidR3 GM SoundFont and its full notices are included in `runtime/`; no separate SoundFont download or development checkout is required.

## Mouse and keyboard controls

The supported control target is a standard mouse and keyboard in Linux or Steam Deck Desktop Mode. Left-click selects visible controls; right-click uses the default action.

Optional built-in Deck mappings are configuration information only: with Steam running and the default Desktop layout selected, use the right trackpad to move the pointer, R2 for left-click, L2 for right-click, and **STEAM+X** for the on-screen keyboard. These mappings match the installed Valve Desktop layout; an active custom layout may differ. Physical operation of the Deck's built-in trackpad, triggers, buttons and on-screen keyboard has not been verified; the mouse and keyboard routes were exercised in stock ScummVM. A Gaming Mode controller layout has not been accepted.

Direct ScummVM joystick input is disabled for this game process to avoid the observed controller-axis event flood. This preserves Steam's desktop mouse/keyboard mapping and does not disable devices globally or change another application's settings.

Use the visible action buttons and scene targets. Choose a verb, then the relevant person or object; follow the displayed sentence when an action needs a second target. Right-click uses the default action.

For a route that needs no function keys, press **M**, then **1 Save**, **2 Load**, **4 Resume**, or **5 Quit**. Select the save/load slot in the chooser. Use a new slot to retain earlier saves. F2 and F3 also open Save and Load. Save before closing the window; window close is not an automatic save.

Tab / Shift-Tab moves focus, arrow keys navigate focus or the displayed panel, Enter activates, and Esc cancels or goes back. Outside dialogue and panels, Space shows hotspots and H opens hints. Active scenes can temporarily restrict controls; follow their on-screen labels.

During the opening, N advances, H or Space holds/resumes, X or Esc skips, and T toggles reduced motion. The matching on-screen controls are available.

## Music and sound

The launcher selects FluidSynth, the bundled FluidR3 GM SoundFont and 44,100 Hz stereo output. Leave music enabled in ScummVM and in the game.

If the game is silent, keep it open and use the Desktop Mode speaker icon → **Audio Volume → Applications → Come and Knock on Our Door**. Unmute this game's entry. KDE retained that entry as muted on the tested host; extracting a new copy does not reset the host setting. This mute setting is independent of the game's Music, Voice and Effects controls. The game and launcher preserve host audio preferences: neither automatically unmutes the application nor changes its host volume or default output device.

Y toggles music; + and - adjust game volume. During ordinary gameplay, A toggles the audience, V toggles voice, [ and ] adjust voice level, E toggles effects, and comma/period adjust effects level. Enabling voice takes effect on the next line.

Audio verification uses objective measurements of the game's own PCM stream. Subjective listening was unavailable and is not claimed. See `ACCEPTANCE.json` for the recorded validation scope and any remaining limitations.

## Saves and settings

The default folder for this release's save lineage is:

```text
~/.local/share/come-and-knock-on-our-door/38437e336b41e8f4/
```

It contains `saves/`, `scummvm.ini`, `SAVE-LINEAGE.json`, screenshots and the runtime log. If an absolute `XDG_DATA_HOME` is set, it replaces `~/.local/share` in that path. Back up the whole folder to preserve saves and settings. Moving the extracted game folder is supported; launch again from its new location.

The launcher preserves existing saves and this launcher's volume preferences, and leaves the normal ScummVM configuration and other games alone. Saves from earlier development builds belong to other lineages; do not copy them into this release's save directory. Use `./launch.sh --user-data /absolute/path/to/a/new-folder` only when you deliberately want a separate set of saves and settings.

## Included files and rights

`game/` contains the complete runtime data. `runtime/` contains the FluidR3 GM SoundFont and its notices. Keep `CREDITS.txt`, `LICENSE.md`, `RIGHTS-CONTEXT.md`, `rights/`, `GAME-MANIFEST.json`, `STATIC-STAGE-MANIFEST.json` and `ACCEPTANCE.json` with the package. The manifests distinguish compilation/staging records from native acceptance and identify the source and runtime file hashes.

The package preserves the existing game and asset rights. Read the accompanying notices for their exact terms and retained historical qualifications.
