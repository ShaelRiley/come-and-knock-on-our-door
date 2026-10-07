# Come and Knock on Our Door: source-arranged score, approved-direction candidates

**Status:** The user approved the short relaxed-swing V3 audition. This bank carries its musical principles into the full score; the individual new cues and full native soundtrack remain candidates. The accepted V3 MIDI, SCI payload, WAV and MP3 are byte-locked and unchanged. V1 and V2 treatments are superseded historical work.

## Musical scope

Thirty main resources cover MUS01–MUS10: 22 principal states (including the full end-credit reprise) and eight bridges/passages. Eight additional resources cover MUS11 verbal competitions: one persistent bed, four opponent gain colors, a restrained thinking state, and two optional single-fire musical accents. Thirty reduced main companions are exact-clock CC7-only references. The score contains about 34 minutes across related arrangements, variations and short passages; this is not a claim of 34 minutes of unrelated themes or a 90-minute through-composed soundtrack.

The main score uses a shared gentle 60:40 swing, mostly 108–112 BPM, a grounded two-feel bass, sparse precise electric/acoustic piano shells, complete lead phrases, restrained guitar replies, selective string color, and phrase-level dynamics/dropout/reentry. The exact 60-second opening is at 120 BPM; the quiet ending eases to 100 BPM. Musical roles reflect the requested late-70s sitcom-pop / soft-rock palette, shaped by the later relaxed jazz/yacht-adjacent refinements. Instrumental duet phrasing is not recorded singing.

The distinct verbal-competition family uses original source-motif transformations with clipped brass, taut bass, dry percussion, dramatic space and its own coherent straight pocket at 120 BPM. It supports figurative verbal/social outcomes only. No film score, recording or franchise theme is quoted.

## Source identity and harmonic review

All five authorized MIDI bundles recur. The original 46 stems contain 55,596 notes and remain unchanged. The five selected phrase reductions have exact original note IDs, pitches, source times, and transformations; they are curated melodic reductions of polyphonic stems, not claims of literal full transcriptions or listening to unavailable source recordings.

- HOME_A / B01S06: 33-note household phrase; held opening, pickup/arrival shape and corrected F–Em7–Am7–Dm7–Gm11–Cmaj7–E7–Am7–Ab7–Gm7–C7 relationships retained
- PRESENTATION_A / B02S08: 45-note phrase; real quarter-beat ornaments retained; suspended Em-over-D into D7 cadence distinguished
- TOGETHER_A / B03S06: 17-note reduction; source pickup phase preserved; Fm7, Bb7, Gm7, C7(b9), Eb/G, Abmaj7 and Bb9sus4 colors coupled to the melody
- PRESENTATION_B / B04S02: 48-note reduction; chromatic Fm–Em7–Db9–Cmaj9 descent, quarter-beat turns and original wide-register figures preserved; the full 25.43-beat phrase is not cropped at 24
- TOGETHER_B / B05S05: 25-note reduction; source's existing ternary feel is explicitly normalized in both attacks and endpoints before applying the new pocket. The genuinely conflicting third at one source arrival is omitted rather than misrepresented as certain

Sparse voicings retain inversion roots and diminished fifths. Between-pulse harmonic arrivals include odd integer beats. Authored overrides take precedence at a shared timestamp. HOME's final major7 carry remains across major-tonic returns; at new minor-family entries the held note ends with an authored breath. Audible release/reverb at those joins still needs targeted listening.

## Files and reproducibility

- analysis/score-index.json: current exact resource, MIDI and payload hashes
- analysis/corrected-source-catalog.json: independently audited source phrase/harmony evidence
- analysis/*-manifest.json: complete notes, original-note lineage, expression timeline, harmony, binding and natural per-role key windows
- analysis/reduced-variants.json: CC7-only companions and exact equivalence
- analysis/verbal-competition-music-contract.json: canonical event/serial/one-PCM ownership
- analysis/native-transport-handoff.json: startup, loop, controller restoration and key-only wait metadata
- analysis/render-validation.json and validation-summary.json: fixed-SoundFont component profiles
- midi/: editable standard MIDI; native/: standalone stock-SCI resource candidates
- renders/: 44.1kHz stereo 16-bit WAV masters; full scored duration plus 6 seconds of natural release
- licenses/FluidR3_GM-copyright.txt: SoundFont license notice retained

The source bank inventory and original preserved bytes are under the earlier source-arrangements/source and analysis directories; that original source data remains authoritative even though its old arrangements are superseded. The production archive preserves the source files and evidence separately from superseded music.

Generators and tests are under tools/music-production: score_v4_core.py, compose_full_score_v4.py, compose_verbal_music_v4.py, reduced_score_v4.py, render_full_score_v4.py, finalize_score_v4.py, and test_full_score_v4.py. They use the existing stock-SCI converter and trusted FluidSynth library. No game runtime, player preference, master gain or device setting is edited.

## Native and listening gates

Resource numbers 100–129 and 140–147 are reserved isolated candidates. Different full cue states are not phase-equivalent; their authored bridges and musical entries need native tests. Only the reduced companions and contest colors have CC7-only equivalence. Use one parser, not concurrent full-score players.

No source note is clipped or rearticulated to manufacture per-bar safety gaps. Natural key-silent windows do not prove release-tail or reverb silence. The V3 stock transport component has separately demonstrated positive-gain reversal, channel-local muted-tail clearing, explicit CC11 reconstruction and bounded held-note replay. That is not whole-V4 acceptance. Each V4 cue supplies initial CC11 and absolute native-tick expression events for restore/remap reconstruction; loop and transition forms still need their own native tests.

Optional accents use one repeated high woodblock pitch and reserve the ACCENT function. Native isolation/lifecycle proof must establish that they replace that function without adding a ninth sounding part or writing shared percussion-channel controllers. Their perceived pitch/timbre against distant chords still needs listening.

Speech, existing-profile social-KO groans, audience response and everyday foley keep one serialized PCM owner. A fixed musical gap cannot time or end consequential speech. Transient cues must be consumed once after game commitment and never replayed by restore, reread or repeated input. Music never changes puzzle correctness or imposes a player countdown.

Offline renders model music_volume 161/255 and whole-Sound 100, with no loudness normalization. Zero clipping and bounded voices are engineering properties; they do not establish subjective musical quality, final speech/foley balance, Steam Deck acceptance, or native allocator behavior. Full-score human listening and native integration remain required.

## Spoilers

This production material contains explicit scene, character-state and puzzle bindings. The separate neutral-numbered listening files contain no story labels or puzzle solutions. Public previews are high-quality lossy MP3s; WAV masters are retained.
