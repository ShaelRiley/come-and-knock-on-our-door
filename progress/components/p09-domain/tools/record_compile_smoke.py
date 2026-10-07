#!/usr/bin/env python3
"""Re-run the real fresh compile and focused dual-oracle gates; persist evidence."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import io
import json
import subprocess
import sys
import unittest

sys.dont_write_bytecode = True
H = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(H / 'tests'))
E = H / 'evidence/gate2-compile-smoke.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(value):
    E.parent.mkdir(parents=True, exist_ok=True)
    E.write_text(json.dumps(value, indent=2) + '\n')


def run():
    write(dict(status='RUNNING', native_acceptance=False))
    compiled = subprocess.run([sys.executable, '-B', str(H / 'build.py')], cwd=H, capture_output=True, text=True)
    if compiled.returncode:
        raise RuntimeError(compiled.stdout + compiled.stderr)
    from harness import compare_calls
    import test_serial_gates
    calls = [('p09Validate', ()), ('p09Context', (6,0,1,1,6,6,0,0,0,0,1)),
             ('p09ValidateContext', ()), ('p09Look', (395,)), ('p09Begin', (3,)),
             ('p09Acknowledge', (3,0,1,1,4,0,0)), ('p09Validate', ()),
             ('p09Acknowledge', (3,0,1,1,4,0,0)), ('p09PendingAt', (0,)),
             ('p09JournalAt', (0,0)), ('p09JournalAt', (0,1))]
    source, emitted, results = compare_calls(calls)
    expected = [1,1,1,10,17,19,1,18,0,4,3]
    assert results == expected, (results, expected)
    assert source.p['p09RumorCleared'] == 1 and source.p['p09RevisionLo'] == 2
    output = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_serial_gates)
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise RuntimeError(output.getvalue())
    receipt = json.loads((H / 'build/isolated/compile-receipt.json').read_text())
    inputs = ['src/module990.sc', 'schema.json', 'build.py', 'tests/harness.py',
              'tests/test_serial_gates.py', 'tools/record_compile_smoke.py',
              'tools/compiler-main.sc', 'tools/domain_metadata.py', 'codec/p09_codec.py',
              'reference/cakood/p09_model.py', 'toolchain/scicompile']
    write(dict(status='PASS_COMPILE_SMOKE_SERIAL_GATES', generated_utc=datetime.now(timezone.utc).isoformat(),
               commands=['python -B tools/record_compile_smoke.py', 'python -B build.py',
                         'python -B tests/test_serial_gates.py'],
               source_and_emitted_compared='Every call return, full properties, every local array',
               compile_stdout=compiled.stdout, compile_receipt=receipt,
               smoke=dict(calls=[dict(method=n, args=list(a)) for n,a in calls], returns=results,
                          emitted_instructions=emitted.vm.steps, property_count=len(source.p),
                          local_array_count=len(source.arrays), rumor=source.p['p09RumorCleared'],
                          revision_limbs=[source.p['p09RevisionHi'], source.p['p09RevisionLo']]),
               serial_gates=dict(tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                                 skipped=len(result.skipped), tests=test_serial_gates.MEASUREMENTS, output=output.getvalue()),
               input_sha256={p:sha(H / p) for p in inputs},
               accepted_helpers=json.loads((H / 'tools/ACCEPTED-HELPERS.json').read_text()),
               native_acceptance=False, production_integrated=False, runtime_package=False,
               limitation='Bounded source evaluator and actual compiled SCI bytecode evaluator; not ScummVM/native execution'))
    print('PASS_COMPILE_SMOKE_SERIAL_GATES', result.testsRun, 'tests;', emitted.vm.steps, 'smoke instructions')


if __name__ == '__main__':
    try:
        run()
    except BaseException as exc:
        write(dict(status='FAILED', error=str(exc), native_acceptance=False))
        raise
