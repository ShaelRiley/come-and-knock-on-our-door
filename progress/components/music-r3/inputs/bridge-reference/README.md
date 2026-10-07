# CaKoOD responsive bridge reconstruction candidate R2

Status: editable, deterministically encoded and offline tested composition candidates. Not historical recovery, live P05 integration, native SCI acceptance or listening approval.

## R2 verification-only correction and additional seam

R2 fixes three independently reproduced acceptance gaps: missing audition WAVs, extra unpinned generated outputs, and ignored extra test classes. It uses fixed source/generated/render/test inventories and receipt-bound archive member lists. All existing composition source, MIDI, native resources, manifests, tables and12 original WAVs remain byte-identical. One additional existing-gate149 serial seam is documented in REVISION-R2.md; it changes no selection or music.

## What is new

Seven typed Sound resources, locally allocated after inspecting the retained registry, current P05 host/native maps and MUS11 R2 map:

- 148: HOME Am7–Ab7–Gm7–C7 connector toward the contest F-minor family, 2.300046s including the normal 0.2s controller startup
- 149: contest Cmaj7–C7 connector toward HOME F-major, 2.250045s
- 150: contest C7 connector toward HOME, 2.250045s
- 151: separately named transition-ready HOME arrangement derived from102
- 152: separately named transition-ready contest arrangement derived from140
- 153: HOME Gm7–C7 connector toward contest, 2.266712s
- 154: contest middle-section Gm7–C7 connector toward HOME, 2.266712s

No script, text, selector, species, PCM or voice resource is allocated. Sound151/152 are alternative arrangements, not replacements for102/140. The accepted exact140 parser and940 transport stay unchanged. Five small connectors are needed because the real source phrases leave different harmonies; one generic cut was not substituted for this analysis.

## Why new arrangements were necessary

The unchanged102 stream has only four robust all-key gaps before its full turnaround, at the ends of its Am7 clauses near beats26/58/90/122. Its apparent two-bar boundaries have mostly0–2 native ticks of clearance. Actual140 also has a sustained middle phrase without a short robust global gap. A bridge alone cannot cure that scheduling limitation without truncating notes or claiming an unproved engine mechanism.

The unchanged-source proposals are preserved in generated/phrase-gates.json and generated/latency.json. Their conservative waits are17.184s from102 and12.034s from140. They are expressly not the responsive shipping solution.

New151 changes only16 note releases out of660 notes. New152 changes only19 releases out of790. Every attack, pitch, velocity, channel, role, program, pan, CC7, CC11, pedal, tempo and original loop/control event is retained exactly. The changed note-offs are fully enumerated in each new manifest with old/new SMF ticks. No note is dropped or re-attacked. The longest shortening is about1.04 beats in151 and1.10 beats in152; these are audible articulation changes that require audition.

HOME's two-bar harmonic clauses receive explicit closing breaths. In152 the original late quarter-beat flourish at15.75 remains intact: the gate moves to the following tonic arrival before16.5, likewise48.5/112.5. The long middle C spanning78–82.943 is preserved completely; gates72/78/84/88 follow the actual harmonic/answer structure instead of cutting it at80. See src/ready-arrangements.json and each manifest's gate rationale.

## Measured candidate timing

Under active playback, unchanged intent and no more than2 native ticks (33.334ms) between host polls:

- 151→152: conservative≤4.350087s to serial retirement, ≤4.550091s to bridge first attack, ≤6.850137s to target first attack
- 152→151: conservative≤4.283419s to serial retirement, ≤4.483423s to bridge first attack, ≤6.750135s to target first attack

The full-cycle sweep tested8,486 HOME and7,920 contest request/poll-phase cases. Actual maximum scheduling waits in that model were4.250085s and4.150083s. The larger conservative bounds above are the published contract. The original≤4.32s bridge-onset goal was not met; the measured bounds include each new bridge's genuine12-tick startup guard. Pausing, muting, chooser time, repeated missed frames or changing requests invalidate a wall-clock guarantee; input and gameplay never wait for music.

## Source and rebuild

- src/bridge-score.json: readable primary bridge composition data
- ready.py/add_bridges: the two explicit source-derived ii–V connector variants
- src/ready-arrangements.json: duration-only articulation policy and phrase choices
- build.py, ready.py, tables.py: deterministic MIDI/native authoring, phrase analysis and uncompiled candidate transport tables
- generated/: all seven editable MIDI files, native payloads, SCI sound patches, complete note/edit/event metadata, gates, timings and new candidate tables
- inputs/: pinned arrangement/source/encoder references, map/registry snapshots, all retained music pairs/V3/original981 references, and protected host-source snapshots
- tools/: unchanged recovered native encoder/decoder and FluidSynth API renderer machinery
- src/handoff_model.py: typed offline lifecycle model only

For the complete source plus auditions checkout, run:

python3 run.py
python3 verify.py
python3 guard_checks.py
python3 run.py
python3 package.py

For an extracted source-only packet, use python3 run.py --source-only and python3 verify.py --source-only. Source-only means no WAVs are present at all; a partial set is rejected even in this mode. python3 package.py --source-only emits only a clearly labeled source archive and no successful audio artifact. Complete audition packaging requires all13 receipt-bound WAVs, with no extras. No entrypoint installs software, launches a GUI, touches the live game or player preferences, or publishes anything.

The original render.py is byte-preserved. Rerender the original12 WAVs with LD_LIBRARY_PATH=../runtime/lib python3 render.py, then add the13th with the same environment and python3 supplemental_render.py. These commands require the exact already pinned FluidSynth/FluidR3 runtime beside this component. Every MIDI/native resource rebuild remains independent of that runtime. The complete24-probe regression suite also needs all13 audition WAVs; its source-only relocation test runs without them in an isolated copy.

## Verification and acoustic limits

The suite discovers the full intended test-file/module surface, requires the explicit18 test identities, and rejects missing/extra tests, skips, expected failures and unexpected successes. The fixed24-probe R2 gate suite includes all three exact pristine-R1 counterexamples, their R2 rejections, source-only relocation into spaces, partial/extra output inventories, missing helpers, test discovery and optimized Python. The historical ten R1 probes are retained as earlier evidence. It checks exact native/MIDI event equivalence, all note balances and per-role budgets, original attacks/controllers, natural one-shot release/loop behavior, exact gates, all request phases, late/missed windows, cancellation, current preferences, pause/mute/chooser/restore, stale generations, and deterministic rebuild. The Python broker is not emitted SCI code and does not establish native lifecycle behavior.

The pinned FluidSynth2.4.4+dfsg-1+deb13u3 / FluidR3 renders use the recovered4ms callback model with chorus and reverb enabled. No audio device or game process is opened. Seven resources at bench music volumes161/255, both new beds for two cycles, six serial seams and deterministic repeats passed without clipping. Peak FluidSynth voices were27; these are sample-layer/release voices, distinct from the native held-key budget.

Zero held keys does not mean silence. At the six tested source retirements there were7–21 active FluidSynth voices and preceding25ms RMS approximately−50 to−43dBFS. The renderer retains synth release/reverb state across the serial handoff; new program/controller writes can still affect release audibility. Its logical-channel model does not prove stock SCI channel reassignment, controller interaction with release voices, actual native stop/dispose behavior, or perceived musical continuity. No tail-clearing sleep is inserted. The6s appended render release is measurement only, never a game delay.

## Remaining gates

1. Review the actual duration-only edits and listen to full151/152 plus the six seam WAVs, including cancellation/redirection between the two F families
2. Independently review the source, allocation and timing evidence
3. Reserve the seven typed Sound IDs in the combined coordinator registry; allocate any future new scripts/text only after their own typed map check
4. Compile a separately named candidate transport for151/152 with fresh static guards and prove the native single-owner handoff, actual polling cadence, controller/physical-channel behavior and audible tails
5. Preserve P05 static240–242 and accepted MUS11's243 checks. Do not turn offline transitionProof=1 into live permission
6. Only then choose whether these arrangements belong in the game. Full V4 cues remain candidates; the user's short V3 relaxed-swing approval remains unchanged

Whole-contest concession is non-KO. M-menu is not VC_EXIT. Music does not commit events, decide outcomes, run a gameplay timer or call PCM/voice callbacks.
