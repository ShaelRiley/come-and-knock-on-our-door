# Reproducible native test session

The full game is implemented but remains an unaccepted candidate. The missing
completion step is an ordinary full playthrough in unchanged stock ScummVM,
including the late chapters, fourth contest, ending, credits and save/restore.
No intermediate player package is published.

`source/native_session.py` prepares that test session. It verifies all 1,759
staged game files against the frozen game-file map, the compile receipt,
current module source and save lineage. It checks the runtime's version,
SCI engine and FluidSynth device, and the exact FluidR3 GM SoundFont identity.
Use a trusted, unmodified official ScummVM 2026.3.0 build; version output alone
does not prove that an executable is unmodified.

From `campaign-presentation/source`, build and stage in a fresh checkout:

```sh
python3 build.py --candidate
python3 stage.py --candidate
python3 native_session.py --check-game
```

Staging refuses to overwrite an earlier stage. The file check is available
without ScummVM or a graphical desktop. It does not certify native behavior.

In a desktop-capable developer session, supply the installed dependencies:

```sh
python3 native_session.py --launch --scummvm /path/to/scummvm --soundfont /path/to/FluidR3_GM.sf2
```

Omit `--launch` to check runtime capabilities without starting a game. Launch
creates a separate empty save folder and private configuration with FluidSynth,
44,100 Hz output and nonzero audio volumes. It uses the regular SCI fan-made
target and ordinary game controls. It does not inject events, use a debugger,
import predecessor saves or grant progress. Observe Music ON inside the game
and check the actual sound output during native testing.

The launcher prints the session folder. Its default location is the ignored
`source/build/native-sessions/` directory. Save files, configuration, runtime
identities, logs and screenshots remain private developer outputs. Existing
session folders are never overwritten. An explicit external `--session` path
is allowed; repository-local paths must remain under the ignored directory.

To continue an existing genuine session, add `--resume --session /original/session`
to the launch command. The helper checks candidate, runtime, SoundFont and
effective configuration identity, while permitting harmless ScummVM preferences.
Load the genuine save through the game's normal F3 interface. Resuming does not
certify the save's provenance; retain the original run's evidence. If the old
private saves are unavailable, repeat New Game in a fresh session.

All six launcher checks pass: exact candidate files, forged-map rejection,
existing-save preservation, harmless preference changes, game/audio mismatch
rejection and required runtime capabilities/SoundFont. Runtime capability probes
in these tests are fixtures. No native ScummVM was launched in this workspace,
and `native_acceptance` remains false. The actual file map remains
`269da8264540dab06e88fa1aa087c84448f3e7d548be673b87afdb56fee288ec`.

Run the helper checks after building and staging:

```sh
python3 tests/check_native_session.py
```

The remaining native scope is recorded in `NATIVE-ACCEPTANCE-20261011-SCOPED.md`.
The current workspace lacks ScummVM, a graphical display and native desktop
controls; its package sources also fail DNS resolution. Enabling a real native
testing session is required to finish acceptance and release packaging.
