# Reproducible five-puzzle source snapshot, publication revision 2

This source view reproduces the same accepted five-puzzle game as publication revision 1. Game SCI, story, assets, tests, host/native seals and compiler executable remain byte-identical. Compiler packaging is reduced to the observed source/header/build dependency closure plus required notices/provenance. Dated comments have been added to inherited port files; no compiler logic is changed. Every omission and source change has an exact identity record.

Run `python3 verify_archive.py` for source integrity. Run `python3 rebuild.py --out /absolute/path/to/a-new-reproduction-directory` for the offline generators/eight-module/80-resource/780-file reconstruction. Linux x86-64, Python 3.10+ and ordinary C++ runtime libraries are required. No network or native engine is used.

The assembly inventory and its two literal driver checks were updated only for the compiler packaging changes and descriptive metadata. REBUILD-PUBLICATION-DELTA.diff records the entire executable driver change. Original host/native input seals, membership predicates and resource checks are unchanged. All eight Contest snapshot inputs and their historical limitations remain; see ../docs/CONTEST-SNAPSHOT-DEPENDENCIES.md.

The completed 44-test evidence is hash-bound, not rerun by this command. To intentionally rerun the full suite, use the generated writable reproduction tree and its p05-host-reconstruction/verify.py. Edited code requires new reviewed identities and a new program/save namespace. Historical component reports retain their original dates and acceptance scopes; later whole-build native scope is described in ../docs/NATIVE-SCOPE.md.

No private chat, credentials, native test saves/raw captures or temporary expanded probes are included. Original archival and publication revision 1 copies remain separately preserved. The new source ZIP has a distinct identity; it is not the earlier source artifact.
