# Isolated reproduction commands

Run Python3.10+ without `-O` or `-OO` on Linux x86-64. The pinned compiler uses
ordinary libstdc++, libm, libgcc_s, libc and the ELF loader. Courtyard conversion
also requires Pillow12.3.0, NumPy2.3.5 and SciPy1.17.0. The driver does not
install software, access a network, stage an active game or launch ScummVM.

From repository root:

```sh
python3 progress/verify_source.py
python3 progress/reproduce.py COMPONENT --out /absolute/new/output
```

The build output must not exist. It contains `component/`, fresh logs and a
durable `build-result.json`. The component maps restore exact input paths and
executable modes; file sharing is by copied bytes, not symlinks. Failed output
directories are retained as evidence; use a new path for the next clean build.

Available component names are `p07-host`, `p08-domain`, `p08-scene`,
`p08-host-gate2b2`, `music-r3`, `p09-model`, `p09-domain`, `p09-scene`,
`milo-approach` and `courtyard-art`. The corrected Gate2b2 has a fixed 22-case affected gate; reproduction alone is
not acceptance. The separate Milo
fixture builds a fresh P07 dependency, copies its build scaffold, then compiles
the guarded correction without changing the P07 source.

P08/P09 scene build phases already regenerate audio, coherently compile and
run their fixed 13/25-case suites. Other build phases compile/generate and
compare exact frozen outputs; they do not implicitly run all behavioral tests.

## Bounded test phases

After a completed matching build:

```sh
python3 progress/reproduce.py COMPONENT --phase test --suite SUITE --out /absolute/new/output
```

| Component | Suite names |
| --- | --- |
| p07-host | p07, audio, p05, p06, cross-branch, caption |
| p08-domain | source, emitted, domain, finite, order |
| p08-scene | all |
| p08-host-gate2b2 | all, the current fixed 22-case affected suite |
| music-r3 | all |
| p09-model | all |
| p09-domain | codec, domain, state, serial, reference |
| p09-scene | all |
| milo-approach | all |

P07's six suites contain15+5+44+22+3+8=97 fixed cases. Each suite has a separate
receipt; all six must pass to claim a new full 97-case run. The original common
audit packaged with the broad compiler tree is not reused as a new public
edition PASS. Historical completion is reported separately.

Music's aggregate starts from absent build outputs and generates its test
checkpoints through the normal suite imports; the driver clears only the
owned isolated build directory before this full 78-case aggregate. It never
removes source inputs or weakens the fixed membership and result guards.

Each phase writes an explicit result. A build PASS is not a test-suite PASS;
one suite PASS is not a full component/package PASS. Source edits invalidate
input identities and need a deliberately reviewed new source bank. The current
driver is for the frozen edition; it must not bless edited data by silently
changing expected hashes.

The baseline's separate root `reproduce.py` retains its original five-puzzle
generator/eight-module/80-resource/780-file reproduction. See its preserved
README and existing compiler documentation for those independent commands.
