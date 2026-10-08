# Pinned headless compiler and minimal corresponding source

Executable: Linux x86-64, 2,501,464 bytes, SHA-256 608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e. Dynamically linked system libraries are libstdc++, libm, libgcc_s and libc.

Source upstream revisions: lucasartsifier 45068351290ffd90e74186c69322d200fa60cafd; SCICompanion f1a603b48b1aa7abf94f78574a8f69a653e2ca62. The full vendor checkout is not bundled. This revision contains all 179 project source/header inputs consumed by the 69 CMake translation units, plus the unchanged CMake build script, required notices and modified-source provenance. Exact retained files are in SOURCE-MANIFEST.json; actual compiler dependency sets are in COMPILER-DEPENDENCY-CLOSURE.json. System compiler headers/libraries are installed separately.

Build from this directory with CMake >=3.16 and GNU C++ (verified with CMake 3.31.10 and GCC 14.2.0):

    cmake -S source/lucasartsifier/tools/scicompile -B /new/compiler-build
    cmake --build /new/compiler-build -j2

No dependency fetch is performed. The reduced source was built and the resulting executable compared byte-for-byte with the accepted pin. See repository docs/COMPILER-BUILD.json. A different compiler/toolchain is not promised to produce that binary identity; do not substitute an unverified compiler into this checkpoint.

The code preserves the inherited headless port and local compiler changes. New comments dated 2026-10-06 provide prominent modification/distribution notices without changing executable logic. The original modification dates are not invented. MODIFIED-SOURCE-PROVENANCE.json and INHERITED-PORT-CHANGES.diff identify inherited changes, including changes beyond the old mechanical-port shorthand. Upstream BUILD_NOTES.md and COMPILE_ALL_NOTES.md remain historical documentation.

The upstream license/notice texts are preserved, with a separate downstream packaging note explaining the included vendor closure. Exact program/component terms and primary evidence are mapped in repository docs/COMPILER-RIGHTS.json. No blanket licensing claim is made for unused material from the full upstream vendor tree.
