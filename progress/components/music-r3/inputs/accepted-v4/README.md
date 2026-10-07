# CaKoOD MUS11 R2: additive source/emitted binding proof

**Status: isolated candidate, not live P05 integration or native/listening acceptance.**

This packet restores an editable MUS11 transport and committed-event binding around the preserved V4 resource140. It does not replace the accepted V3 audition, the original981 controller, PCM owner980, the P05 host, any game state, or any of the38 pinned V4 MIDI/native pairs.

## R2 verifier-only correction

R2 rejects skipped tests, expected failures, unexpected successes, ordinary failures and errors explicitly. All29 required test methods must actually succeed. R1’s real29-test execution remains valid; its public gate could incorrectly accept a later skipped/expected-failure suite. See `REVISION-R2.md` and the13 isolated negative probes. Game/music source, test methods, compiled resources and the existing musical/native limits are unchanged.

## What is implemented

- Script940 contains one `contestTransport` instance of the existing `MusicTransport` species3, overriding all43 transport methods, plus12 class-free binding/validation procedures. It creates no class and allocates no selector
- A single140 score parser follows six exact CC7 rows: base140, opponent references141–144, and restrained thinking/line reference145. References141–145 never become independent players
- All105 event-gap rejoin windows,106 held-key rows,48 CC11 events, channel/program/pan maps, initial/loop expression values and history predicates are derived from the unchanged140 native stream and full manifest
- The derivation reproduces original102's194 windows,1,428 held-note words and both194-word history tables exactly before deriving140
- Startup colors open through the genuine pre-attack guard at ticks6–8, before the authored first attack at12. A non-base color does not impose an artificial2.3-second wait. Missed guards follow bounded recovery and remain silent until reconstruction succeeds
- Canonical VC01–VC04 event bindings read accepted986 committed state. Two15-bit attempt limbs, exchange slots1–5 and the committed KO flag are retained. Candidate/prepared state, old or duplicate events, wrong identities and visual menu retirement cannot commit musical events
- Frozen chooser cancel/restore preserves the current bed, one clock, gain/expression state and consumed events. Restore also suppresses committed presentations that preceded the snapshot but had no musical notification yet
- Exact static constants are checked against freshly read text243 on startup and relevant save/restore boundaries. Mutable gain validation is separate. No restored validation flag is trusted
- Optional146/147 accents remain disabled. Their events are consumed once without delayed playback. No channel7 player, ninth role, PCM or voice data is introduced

## Rebuild

Run `python3 run.py`, then `python3 verify.py`.

The pinned compiler is included. No installation or network is needed. `run.py` is the only aggregate acceptance gate. It recreates generated source/data and fresh emitted resources, runs conservative emitted stack/arity checks, requires the exact nonempty test inventory, and writes `evidence/current-status.json`. `verify.py` rejects a stale receipt if any verified source, input or compiled byte changed.

`python3 tools/guard_checks.py` additionally verifies missing helpers, broken imports, zero discovery, test syntax errors, optimized Python, corrupt inputs, skipped/expected-failure/unexpected-success/error/failure outcomes, a stale PASS, and a true source-only rebuild after relocation into a path containing spaces.

No native launcher or GUI is invoked by any of these commands. The Sound implementation in `tools/music_vm.py` is an explicitly typed test mock, not ScummVM or FluidSynth.

## Source and data

- `src/binding-locals.inc`, `src/binding-procedures.inc`: readable authoritative committed-event and lifecycle code
- `generate.py`: deterministic table derivation and explicit transport port from the pinned reconstructed981 source
- `generated/module940.sc`: complete readable emitted-source input, including all43 overridden methods; never a compiled-module splice
- `generated/tables.json`, `generated/243.text.bin`: derivation data and fresh-resource equality reference
- `inputs/original981/`: untouched reconstructed source/API/layout reference
- `inputs/domain/module986.sc`: accepted contest domain source used in actual emitted commit-boundary tests
- `inputs/music/`: preserved manifests, MIDI and native references, including all38 full pairs
- `inputs/accepted-v3/`: all four byte-locked original audition inputs
- `inputs/composition-generators/`: preserved composition source, never executed by this packet's rebuild
- `inputs/runtime-source/`, `inputs/runtime-provenance.json`: exact2026.3.0 retained source and selected runtime pins
- `HOST-CONTRACT.md`: required future one-owner P05 wiring and explicit staged gaps
- `generated/handoff-candidates.json`, `handoff.py`: cancelable, metadata-based phrase-end fade/entry proposal, with all musical/native/tail acceptance flags false

## Allocations and measured budget

940 occupies the retained registry's reserved940–977 music-script bank. This is a script allocation, not an audio resource number. Actual music resource numbers remain100–129 and140–147. Text243 is reserved after P05's240–242.

The initial proposed limits were12KB script,16KB heap and6,000 table words. Current measurements are in `evidence/compile.json` and `evidence/layouts.json`. At this revision940 compiles to9,784 script bytes and3,204 heap bytes, with1,509 total locals including1,423 table words; text243 is9,559 bytes. No new species or selectors are introduced. The original981 script and heap retain their exact SHA-256 identities.

No fuller historical registry was found beyond the retained subset and the coherent current vocabulary. This packet therefore establishes compatibility with that retained universe, not an invented complete historical allocation database.

## Explicit remaining gates

1. Review the additive source and the future Main owner hooks against the latest P05 static-table guards. Preserve981/982/985 guard additions; do not replace those modules from this fixture
2. Choose and review the natural cross-family transition. The preserved bank has no MUS11-specific entry/exit bridge. The candidate fade/entry plan is described precisely, but parallel F-major/F-minor color, tempo change and residual release/reverb still need listening/native tests
3. Run stock ScummVM2026.3.0 with the pinned FluidSynth2.4.4+deb13u3 library and FluidR3 GM bank. Verify physical-channel remapping, controller ordering, startup timing, frozen native chooser/save behavior and practical PCM overlap
4. If accents are desired, independently prove reserved-ACCENT channel/voice isolation and lifecycle before enabling146/147
5. Native full-score listening, actual four-encounter host activation and remaining room/ending integrations remain staged

The user approved the short V3 relaxed-swing direction. Individual full V4 cues remain candidates until their own gates pass.

Whole-contest concession is a non-KO ending. The terminal-result ledger is not authorization for a zero-meter pose, groan or KO accent. The host contract makes that distinction explicit, and all optional accents remain disabled.
