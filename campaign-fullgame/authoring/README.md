# Bounded asset authoring

This directory contains portable deterministic authoring for a verified subset of the current r16 assets. The game build uses the exact inputs in `source/assets/`; it does not depend on regenerating this optional subset. No historical routes, proof transcripts or storage references are needed.

## Run

Python 3.10 or later is required. The physical-view recipe additionally uses Pillow. The recorded test used Python 3.12.14 and Pillow 12.3.0; consult `COVERAGE.json` for the measured versions. Install Pillow from its normal package registry if needed. All other recipes use the standard library.

From the component root, write to a fresh empty directory outside the source package:

    python3 -B authoring/regenerate.py --output /path/to/new-assets --workers 2

The command generates resource and audio subdirectories and checks every output against `EXPECTED-GENERATED.json`. The recorded full run generated 1,318 files with zero mismatches: 1,307 audio/sync files and 11 packed assets. `VERIFICATION.json` records the scope; `COVERAGE.json` lists exact coverage and binary-only inputs.

For a smaller task, use `--only primitives`, `--only speech`, `--only cadence`, `--only chime` or `--only physical`. `--only` reports bounded selected coverage rather than claiming all outputs. Physical generation reads the exact bundled 216/224/225/227 resource bytes and verifies their input hashes. It never overwrites those inputs.

## Edit

- `glyphs.json` and `lowercase-punctuation.json`: original 5×7 bitmap forms for font0/1
- `palette.json` and `cursor.json`: original indexed palette and cursor
- `midi.py`, `safe_midi.py`, `credit_midi.py`, `midi_mix.py`: original diagnostic music/stinger, provisional credit cue and GM patch encoding
- `profiles.json`, `voice.py`, `speech-recipes.json`: original character synthesis, exact text fragments and output names for the recovered speech recipes
- `audience-profile.json` and `audience.py`: original separate group voice; no principal mouth animation
- `cadence.py`: 121 original Frankie pulse/silence atoms and their sync files
- `regenerate.py`: original two-second celebration chime
- `physical_views.py`: current physical phase views 239–241 from the bundled project cels

After an intentional edit, `--allow-changes` writes changed outputs and explicitly reports differences from the canonical pins. Review and integrate changed assets separately; editing speech text here does not automatically update script tables, captions, reader maps or host state. `SOURCE-ADAPTATIONS.json` describes the portable extracts. Original synthesis algorithms and profiles were retained; historical packaging/controller entrypoints were omitted.

## Limits and rights

The recovered recipes regenerate 532 speech pairs, 242 cadence files, the chime and 11 noncode resources. The remaining 404 audio/sync files and 75 noncode packed assets are preserved as exact binary inputs. They are not represented as newly recovered original masters. That remainder includes nine CC0 recordings; those recordings are intentionally not synthesized by these generators.

All 239–241 physical outputs reuse pixels from historical VIEW224, including the linen/cart padding. Its origin-record qualification remains, together with VIEW221–223,300,302. Deterministic regeneration does not establish rights clearance. See `rights/PROVENANCE.md` and the credits. No blanket game or asset license is granted by this directory. New generated reconstruction is not recovered historical artwork.

Generated output does not certify native rendering, listening quality, route behavior, timing or final campaign acceptance. The canonical source build and bounded static checks have their own reports.
