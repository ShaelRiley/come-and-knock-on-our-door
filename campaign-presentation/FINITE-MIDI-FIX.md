# Ordinary finite-MIDI completion correction, revision 1

Status: all 46 modules compile, with a subsequent scoped native observation pass. The earlier P02 failure displayed “MUSIC UNAVAILABLE. F3 TO LOAD.” and refused saving after the household agreement. That warning did not recur in the scoped observation described in FINITE-MIDI-NATIVE-STATUS.md. Full-game native acceptance and native verification of the ending remain incomplete.

## Engine contract

The implementation targets the independently verified official ScummVM v2026.3.0 commit `fed42f2068dcafc6aafa1c28c77e4c88def74b66`:

- Final non-looping MIDI EOT sets `SIGNAL_OFFSET`, defined as `0xffff` (signed SCI word `-1`). The former value `255` was incorrect.
- The MIDI parser stops and clears its tracker to native tick 0.
- SCI1-late/SCI1.1 DoSound subcommand 17 exports the terminal signal, stops the Sound handle to 0, and exports the actual native ticker.

Official sources: [SCI EOT](https://github.com/scummvm/scummvm/blob/fed42f2068dcafc6aafa1c28c77e4c88def74b66/engines/sci/sound/midiparser_sci.cpp#L900), [base parser](https://github.com/scummvm/scummvm/blob/fed42f2068dcafc6aafa1c28c77e4c88def74b66/audio/midiparser.cpp#L387), [tracker clear](https://github.com/scummvm/scummvm/blob/fed42f2068dcafc6aafa1c28c77e4c88def74b66/audio/midiparser.h#L94), [native cue export](https://github.com/scummvm/scummvm/blob/fed42f2068dcafc6aafa1c28c77e4c88def74b66/engines/sci/sound/soundcmd.cpp#L636), [terminal constant](https://github.com/scummvm/scummvm/blob/fed42f2068dcafc6aafa1c28c77e4c88def74b66/engines/sci/engine/vm_types.h#L213).

## Source change

Both legacy and full-score bridge polling recognize the stopped terminal sample before applying running-clock regression checks. They revalidate the current sound object, owner/resource, exact bridge metadata, current generation and complete mutable ledger before retiring that owner and admitting the already-authorized successor.

The shared finite reader validates the canonical finite slot, its exact cue/suffix and source end. It checks native coordinate components and frozen-pause invariance, then recognizes signal `-1`, stopped handle 0 and actual native position 0. The first observation validates the immutable tables and latches completion. It records native 0, or suffix offset plus native 0 for the opening’s public coordinate. It never fabricates an authored-end position. Active playback retains its monotonic/source-bound checks; a latched completion cannot become a running sample.

Opening and later finite polling handle completion observed by either read. A terminal second read silences reconstruction and cannot reopen gain. Later finite completion retains the existing dialogue/edge prerequisites and performs full ledger validation once immediately before actual successor dispatch. While a stopped finite owner waits for visual progression or a later authorized target, repeated reads retain lightweight slot/cue/suffix/generation/pause/state checks. No new persistent fields, selectors or public procedure exports were added. The director reads broker-validated completion through additive rbStatus field 26 instead of reading the raw Sound signal.

All authored notes, rests, tails, controller payloads and timing windows are unchanged. Main remains the visual timeline authority. Save admission and restore checks remain in place. Bridge gain still opens only during its existing ticks 6–8 window; that separate gain-window concern is outside this correction.

## Compilation and static layout

- Baseline receipt SHA256: `d9c8806a330a5b2b485dd3b449028ee1c6bc966a7808d7f411b938c45a7a106a`. An isolated fresh baseline compile reproduced it exactly.
- Final candidate receipt SHA256: `f67cfaa896ec9c01f751a80b597af9bb693f02723ef8892cda550877f0d764d0`.
- Compiler SHA256: `608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e`.
- Module 943: 62,306 → 63,282 combined bytes, leaving 2,253 bytes under the 65,535-byte limit.
- Module 944: 6,908 → 6,904 combined bytes.
- The other 44 modules’ scripts and heaps are byte-identical. Every heap, local declaration/offset/count/initial value, class layout and selector identity is unchanged. Static resource map/volume identities are unchanged.
- Script export/internal code addresses changed in modules 943 and 944. Existing-save compatibility is not established. Use a genuine New Game and separate save lineage `CAKOOD_ORDINARY_FINITE_FIX_20261009_R1`; do not restore predecessor saves into this revision.

## Reproduce compilation

Use a separate copy of the sanitized source baseline with this revision’s replacement files applied. The baseline must remain unchanged. Python 3 and the bundled pinned Linux x86-64 compiler are sufficient; no network fetch or asset regeneration is required.

```sh
cd source
chmod u+x toolchain/scicompile
timeout --signal=TERM --kill-after=10s 180s bash -c 'ulimit -v 1048576; ulimit -t 150; exec python build.py --candidate'
```

The inspected build entrypoint compiles the explicit 46-module order, checks source/resource/audio identities and class/layout budgets, and writes `build/coherent/compile-receipt.json`. It does not launch the game or invoke a test harness. Compiler-source regeneration performed by that entrypoint is limited to existing selector aliases. No score/asset generator was run. The exact canonical modules and their generated counterparts match byte-for-byte; current build_broker.py source inputs and the director generator carry the correction. The older standalone presentation template retains its preexisting pause-helper structure; full earlier-stage template regeneration was not reviewed or executed.

## Remaining validation

A genuine New Game completed the full opening, P01 and P02, followed by F2 save, a REVEAL setting change, F3 restore, and normal exit. Music remained ON and no music warning appeared during this scoped observation.

This is a scoped observed pass, not full-game native acceptance. Native verification of the campaign ending remains incomplete; this is a verification limit, not an implementation omission. Exact cue identity, acoustic quality, subjective listening and timing/performance acceptance are not claimed. Portable game-model and internal test harnesses were not run for this revision.

The build profile and compile receipt retain their original compile-time status. They establish source/binary coherence; the later scoped observation does not change their bytes or imply broader acceptance.
