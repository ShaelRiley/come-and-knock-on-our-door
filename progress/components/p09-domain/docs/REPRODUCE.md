# Bounded reproduction

Run each command from the component root and keep its actual exit status and
output. Do not infer a completed later gate from an earlier PASS. The unchanged
reference uses the one documented current-catalog test pin, preserved in
`reference/provenance/`; its 36 behavioral tests remain intact.

If the ZIP extractor does not preserve the compiler's executable bit, restore
it with `chmod u+x toolchain/scicompile` after verifying the pinned hash. The
Library relocation check used that exact extraction step; no software was
downloaded or installed.

1. `python3 -B verify_inventory.py`
2. `PYTHONPATH=reference python3 -B -m unittest discover -s reference/tests -p test_p09_model.py -v`
3. `python3 -B -m unittest discover -s tests -p test_codec.py -v`
4. `python3 -B generate.py`
5. `python3 -B tools/record_compile_smoke.py`
6. `PYTHONPATH=tests python3 -B -m unittest test_domain.ActionGates -v`
7. `PYTHONPATH=tests python3 -B -m unittest test_domain.ObservationGates -v`
8. `PYTHONPATH=tests python3 -B -m unittest test_domain.SaveGates -v`
9. `PYTHONPATH=tests python3 -B -m unittest test_domain.ReceiptGates -v`
10. `python3 -B tests/test_state_validation.py`

The last command is 54 bounded tests covering 2,002 signed-word validation
cases. It compares independent SCI source/emitted validators with the unchanged
model codec; it is not a search for unrelated vulnerabilities. Each small
group is reported as it finishes. The first completed run took about 42 seconds.

The tests compare event payloads and exact presentation IDs, not just state
flags. No evaluator operation is replaced with a Python model callback.
`tools/ACCEPTED-HELPERS.json` records byte-identical evaluator provenance.
`build.py` uses only the already-present pinned compiler. All generated outputs
are inside this component. No live native game or predecessor is changed.

`checkpoint.py GATE_NAME` writes a hash-inventoried ZIP under `delivery/` and
excludes delivery archives and relocation work. It does not upload or declare
a test result. Existing checkpoints use the same Library identity and preserve
version receipts outside the ZIP. `STATUS.json` states the most recent completed
component gates and the remaining independent/host/native work.
