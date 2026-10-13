# Portable checks

Build first with `python build.py --candidate` from source/. Then run:

    python tests/run_static_checks.py
    python tests/check_presentation.py opening_geometry
    python tests/check_presentation.py credit_overlay
    python tests/check_presentation.py laf11_wait
    python tests/check_presentation.py laf11_timeout
    python tests/check_presentation.py laf11_token_cancel
    python tests/check_presentation.py laf11_page_cancel

Each command creates a fresh bounded VM process. The strict VM executes emitted SCI bytecode with typed kernel mocks. Rendering regressions explicitly model read-only reader guards, and the LAF11 wait fixture mocks the durable claim; these are not earned campaign or native-save evidence. The opening test executes66 actual stateless projections and checks the exact final asset geometry. Static checks bind all assets, selectors, protected source and untouched core methods.

Score tests and their bounded process runner are under tests/score/. No test launches a native engine. A native full campaign and ending remain a separate acceptance step.

Late-interface regressions run against the same compiled candidate:

    python tests/check_late_ui.py control_priority
    python tests/check_late_ui.py reading_availability
    python tests/check_late_ui.py held_item_labels

These checks model only full-scene admission with explicit P13/P14 fixtures.
The actual emitted world-control registration, reverse hit testing, menu
availability, serial/paint guards and label drawing execute unchanged. They
cover character torsos over retained props, the ending's moved Milo control,
held-program selection/visibility, the guest program's room restriction,
Rita's painted serving/screen requirements, and the one-row pledge label.
They do not earn campaign progress or establish pixels, native saves, actual
deliveries, contest wins, acoustic quality, performance, or native acceptance.

After staging, check native-session preparation with:

    python native_session.py --check-game
    python tests/check_native_session.py

The file check verifies the exact frozen game bytes. The six launcher guard
checks cover candidate/runtime identity, existing-save preservation and
configuration reuse. Their runtime capability probes are fixtures; they do
not launch ScummVM or establish native acceptance. The separate launcher uses
ordinary stock ScummVM with private saves when a desktop-capable development
session is available. See ../../NATIVE-SESSION-20261011.md.

The October 13 restore/action/speaker regressions run against the compiled R3
candidate with explicitly modeled ancestor/domain admission and elapsed walking:

    python tests/check_recovery_r3.py restore_order
    python tests/check_recovery_r3.py apron_route
    python tests/check_recovery_r3.py speaker_availability

They retain the actual emitted restore finalizer and owner lease check, Main's
default/action/arrival path, and authored room/speaker availability. They reject
incomplete owners without weakening gameplay admission. `--reference --build
PATH` reproduces the original defects against the archived R2 compile. Neither
mode establishes native save/restore or full-game acceptance. The R3 native run
must begin with separate empty saves.
