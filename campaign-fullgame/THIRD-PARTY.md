# Third-party rights and provenance

## Pinned headless compiler

The bundled compiler is SHA-256 `608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e` (2,501,464 bytes). Its complete build-required source closure and notices accompany it under `source/toolchain/`. The recorded 2026-10-06 CMake/GCC rebuild of that closure was byte-identical. See `docs/COMPILER-BUILD.json` for the result and `COMPILER-DEPENDENCY-CLOSURE.json` in the toolchain directory for all 179 source/header inputs, 69 translation units and their actual compiler dependency sets. The CMake recipe is unchanged and does not download dependencies.

The exact upstream revisions are lucasartsifier `45068351290ffd90e74186c69322d200fa60cafd` and SCICompanion `f1a603b48b1aa7abf94f78574a8f69a653e2ca62`. The snapshot also preserves inherited port/local changes, with source identity records and dated comment-only distribution notices. These commit IDs alone are not the modified-source identity.

Component-specific terms remain distinct:

- SCICompanion core and the derivative headless port: GPL-2.0-or-later. The full GPL text, original file notices, explicit SCICompanion program-level License.txt and port LICENSE/NOTICE are included
- FreeSCI/ScummVM codec adaptations: preserve the original named attributions, historical GPL-2.0-or-later notices and copyright context. Examined historical ScummVM sources corroborate lineage; the exact original copied revisions are not claimed
- CppFormat, Copyright Victor Zverovich: BSD-2-Clause. Full source and binary-redistribution notice is retained
- cpptoml, Copyright Chase Geigle: MIT. Its full sibling LICENSE is retained
- CRC32, Copyright Michael Barr: original public-domain declaration with notice-retention instruction and disclaimer, retained verbatim

`docs/COMPILER-RIGHTS.json` maps every retained compiler input to its component-specific evidence, exact hashes and primary source links. Additional notices reside under the compiler source's `third-party-notices/`. `DOWNSTREAM-PACKAGING-NOTICE.md` explains why the unchanged upstream NOTICE's untracked-vendor statement describes its original packaging rather than this downstream source bundle.

The reduction excludes unused GUI implementations/resources/cache files, CrystalEdit implementation, ColorQuantization and other unneeded vendor payloads. Prof-UIS, Sierra game data and vendor DLL/LIB/EXE payloads are absent. No blanket grant for the former full 792-file vendor copy is asserted. Original historical port-edit dates and exact historical codec-copy revisions remain qualified; this packaging record does not invent them or offer a legal warranty.

## Runtime and game assets

Runtime reference: official stock ScummVM 2026.3.0, FluidSynth 2.4.4 and FluidR3. These runtime/SoundFont binaries are separate and not bundled here. These external runtime dependencies are distinct from the retained historical compiler codec notices.

The nine unchanged natural audience/foley payloads retain their recorded CC0 sources and courtesy credits in `CREDITS-AND-RIGHTS.txt`. User-supplied MIDI ownership and authorized adaptation are recorded there. This snapshot grants no new blanket license for the game or music. Using a GPL compiler does not by itself determine the license of its generated game resources.
