# P05 + VC01 native candidate staging

Private, newly reconstructed stock SCI1.1 candidate. This is a staging tool for the independently reviewed P05 host; it does not launch ScummVM or claim native acceptance.

`python stage.py` requires the completed source/emitted host gate and writes a fresh game directory using the current whole-universe scripts/heaps/vocabulary, native art/text and exact accepted PCM/Sync assets. It rejects mixed or changed inputs and any prior game directory. `python check.py` independently checks the sealed packed map, volume, speech and namespace.

Namespace: `cakood-p05-reconstruction-20261006-r1`. P03/P04 saves and configurations must not be imported. The required native runtime is the pinned stock ScummVM2026.3.0. The separate MUS11 binding is not activated in this candidate; practical controls, source receipts, VC01 scoring/result barriers, stage, KO groan and save/load are the native proof scope.

No publication, GUI launch or native audio/listening acceptance is performed by these scripts.
