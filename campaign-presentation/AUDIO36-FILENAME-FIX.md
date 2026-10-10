# Audio36 filename correction: native acceptance pending

Ordinary native testing of the presentation-label candidate completed the opening, P01–P05 and the first contest win. P01, P04 and mid-contest save/restore checks passed with Music ON. A fresh process restored P04, and a separate P05 save was retained. Those scoped observations do not validate a complete campaign.

The native log reported `Failed to find audio entry (932, 19, 1, 0, 1)` when the menu used its metal click. The unmodified official ScummVM SCI resource parser decodes every audio36 filename field in base 36. The expanded audience/Foley exporter had used hexadecimal for the noun field. Nouns 16 and above therefore addressed different resources.

Fifteen runtime files now use their correct base-36 names: six expanded laugh takes and nine material Foley takes. Their exact PCM bytes, source credits, performance identities and ownership rules are preserved. No SCI source changes in this correction. No voice or mouth-sync resources change. The editable exporter now uses a bounded base-36 formatter. The pins check verifies all 49 authored audience/Foley/applause tuples against the actual filenames and unchanged PCM hashes, and verifies the exporter's names without regenerating audio.

`authoring/audio/AUDIO36-FILENAME-FIX.json` records every old/new name and preserved hash. AUDIO-INVENTORY.json and FINAL-COVERAGE-MANIFEST.json pin the corrected membership and authoring inputs. Historical public source checkpoints retain the earlier names. Existing stage directories and genuine saves were preserved separately; no unfinished player release is published.

Native regression and start-to-finish acceptance of the corrected build remain pending. The candidate lineage is CAKOOD_PRESENTATION_AUDIO36_FIX_UNACCEPTED_20261010_R1. Final acceptance begins with a genuine New Game and empty separate save directory. Subjective listening remains unperformed; numerical checks are not listening. Historical rights qualifications remain in force.

Fresh compilation passes all 46 modules, receipt SHA256 a45e3344bd4ac61c9251dcca5cb5ee72116efce514ad9f3d7da9e0290a755fcb. All 92 compiled script/heap artifacts are byte-identical to the label candidate. Fresh independent stage closure passes: 1,759 game files, 254 typed resources, four player documents and eight rights files. All four bounded static cases pass. These are static observations, not native campaign acceptance.
