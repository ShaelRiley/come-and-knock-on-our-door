# Come and Knock on Our Door

A stock-ScummVM adventure game in active development. This branch preserves the **exact five-puzzle development build** tested on 6 October 2026. The full campaign is unfinished. Later P06/P07 and responsive-music work is kept separate and is not silently included in this build.

## Play

Use the full `Come-and-Knock-on-Our-Door-Five-Puzzle-Checkpoint-20261006.zip` release asset. Extract it into a new folder, add that folder to stock ScummVM, and follow `README-FIRST.txt`. Use a new game entry, a fresh Save Path and New Game. Older saves are incompatible. The release includes game data and instructions, not a ScummVM runtime or SoundFont.

Reference native setup: ScummVM 2026.3.0, FluidSynth 2.4.4 and FluidR3. Existing room music remains provisional; the full revised score and contest music are not activated. One repeated room-arrival caption can describe a moved character; its separately tested source correction is for a later build.

## Reproduce the exact build

On Linux x86-64 with Python 3.10+ (tested 3.12) and ordinary C++ runtime libraries:

```sh
python3 reproduce.py --out /absolute/path/to/a-new-build-directory
```

The output directory must not exist. This performs an offline relocated reconstruction of the four generators, eight SCI modules and all 80 packed resources, then requires all 780 game files to match the tested build. It does not install software or launch ScummVM. The bundled pinned compiler executable is accompanied by the build-verified corresponding source closure and required notices.

The compiler source closure independently rebuilds the exact pinned executable from 179 source/header inputs in 69 translation units. See `docs/COMPILER-BUILD.json`, `docs/COMPILER-RIGHTS.json` and the toolchain dependency manifest. Revision 2 changes only compiler packaging, dated source comments and publication metadata; game code, assets and tests remain exact.

The completed 44-case host evidence is hash-bound by this reproduction, not rerun by it. A deliberate full rerun is documented in `source/README.md`. Source/code changes require new seals, tests and a new save/build identity; an old PASS must not be reused for edited code.

## Where to edit

- `source/workspace/rebuild/p05-host-reconstruction/`: readable SCI host templates, controller and geometry generators, source tests and derived `src/` modules
- `source/workspace/rebuild/p05-host-reconstruction/derive.py`: guarded composition of the current Main/domain/presentation source
- `source/authority/`: approved GDD, final script catalog, speech-unit and contest-pair authorities
- `source/workspace/rebuild/p03-editable-checkpoint/toolchain/`: pinned compiler and supplied corresponding source
- `source/workspace/rebuild/p05-native-candidate-reconstruction/game/`: exact game data, stored once; speech-export mapping reconstructs source input paths for building

Edit authoritative templates/generators, not only their derived `src/` output. Some earlier code was recovered or reconstructed symbolically; identifiers, compiler mappings and provenance remain included. This is reproducible editable game source with frozen authored art/audio inputs, not a claim that every missing historical authoring master was recovered. See `docs/SOURCE-STATUS.md`.

## Verification and scope

The exact current game completed a fresh opening/invitation/fifth-puzzle/first-contest native route, manual saves/restores, genuine loss/rematch/win and physical follow-through. Prior third/fourth native proofs are separately scoped. No test saves, native recordings or walkthrough are included in the playable ZIP. See `docs/NATIVE-SCOPE.md` and `manifests/CURRENT-BUILD.json`.

This repository contains project source, technical provenance and ordinary test evidence. It excludes credentials, personal data, raw native captures and temporary expanded test copies.

## Rights

No new blanket license is granted for the original game. Third-party tooling/assets retain their included terms. See `LICENSE.md`, `THIRD-PARTY.md`, the source notices and the release’s credits file.
