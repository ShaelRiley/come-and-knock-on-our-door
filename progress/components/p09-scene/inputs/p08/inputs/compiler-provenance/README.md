# Pinned compiler

Bundled binary: `scicompile`, Linux x86-64 ELF, dynamically linked against libstdc++, libm, libgcc_s and libc. Tested on Debian with GCC 14.2.0 runtime. Binary SHA-256: `608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e`.

Source upstream revisions:
- lucasartsifier: `45068351290ffd90e74186c69322d200fa60cafd`
- SCICompanion: `f1a603b48b1aa7abf94f78574a8f69a653e2ca62`

All available source is included under `source/lucasartsifier`, including active compatibility shims and patched files, licenses and build notes. `.git`, generated `build` directories and Python caches are excluded. `SOURCE-MANIFEST.json` binds every included source file. This snapshot includes local port patches; the revision numbers alone do not describe those changes. In particular, the active patched Compile.cpp hash is `d90df228ab6c1e0af29d6ba0265b895a2fcdd50c6b22844786b7aa1ce24fa803`.

The main reconstruction requires no C++ build. To rebuild the compiler itself, install CMake and a compatible GNU C++ toolchain, then from the checkpoint root:

```sh
cmake -S toolchain/source/lucasartsifier/tools/scicompile -B toolchain/rebuilt
cmake --build toolchain/rebuilt -j2
```

The included CMake recipe requires CMake >=3.16, uses GNU C++14 and the existing compatibility flags, and does not fetch dependencies. The source snapshot was independently compiled using CMake 3.31.10/GCC 14.2.0 during packaging and produced a byte-identical compiler executable; see `evidence/compiler-source-build.json` and its build log. Rebuilding in a different path/toolchain is not promised to reproduce the executable hash. Keep a newly built compiler separate; this frozen build and compiler gate accept only the exact pinned binary. A compiler replacement needs explicit revalidation of all emitted artifacts and a new checkpoint's pin, not silent substitution.

Root `licenses/` contains the scicompile GPL-2 text, SCICompanion notice, lucasartsifier license/notice, asset notices and ScummVM notices. The source tree retains upstream licensing files. Inclusion does not grant rights beyond those notices; this is a private development recovery, not a new public release.
