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
