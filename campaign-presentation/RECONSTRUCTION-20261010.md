# Fresh reconstruction and preservation audit, October 10, 2026

The public development branch `wip/quiet-tag-source-checkpoint-20261009`
was verified at `4515cdac507f5744d2043993c7895af75f57f5d4` and reconstructed
in a fresh checkout. No applicable `AGENTS.md` was present.

The bundled pinned compiler compiled all 46 modules. The receipt reproduced
SHA256 `afc13f32aaf19d338aef7e2ea5df77f4db9f3b9c866fdef5c1cb7a1763d96c78`.
`stage.py --candidate` then produced 1,759 game files, 254 typed resources,
four player documents and eight rights files. The staged manifest SHA256 is
`a656bd5a328e72f5aac9d12d9f19a1a13210b5e2d3abcfbea50fd1aecb48baf6`.
This reproduces static staging; it does not establish native acceptance.

The first bounded static suite exposed a stale preservation entry:
`module996.sc:h14Travel` still appeared in `unchanged_methods` despite the
explicit correction described in `QUIET-TAG-FIX.md`. The method was moved
to `reviewed_modified_methods` with both its original and corrected hashes.
The preservation check now verifies every reviewed method against its exact
candidate hash as well as checking unchanged methods and selectors. All
four bounded static cases pass. No game script, emitted program, resource,
audio asset, selector or save layout was changed by this audit correction.

A streaming recursive publication inspection of the tracked source payload
covered 10,215 files and 915 nested archive members across nine archives,
reading 745,160,996 bytes. No supported credential-pattern or private-file
finding appeared. The reusable inspector is
`source/tools/audit_publication.py`; reports identify locations and rule names
without printing possible credentials. This technical scan does not expand
the retained historical rights qualifications or certify legal clearance.

The native runtime has been built from unmodified official ScummVM
`v2026.3.0`, commit `fed42f2068dcafc6aafa1c28c77e4c88def74b66`, with SCI,
FluidSynth and PNG. Its device inventory explicitly includes FluidSynth.
Native campaign acceptance, the ending and save/restore acceptance remain
pending. No finished player release is authorized by these static results.

Use a genuine New Game and an empty separate Save Path. The earlier scoped
finite-MIDI observations remain historical and do not validate this candidate.
Subjective listening remains unperformed. No private saves, screenshots,
audio captures or operating records are included in this source checkpoint.
