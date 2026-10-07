"""NEW offline verification. Known legacy failures are diagnostics, never passes."""
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import sys
import traceback
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
os.chdir(ROOT)

GAPS = {
    'test_canonical_bindings_exact_ids_and_result_surface':
        'Historical catalog digest 1226a978 is superseded by exact current 3c6a8dc5; original assertion untouched',
    'test_composes_real_prior_models_without_rewriting_their_history':
        'Historical P03Context/P03World and downstream historical interfaces unavailable; current APIs tested separately',
    'test_native_object_proposals_do_not_duplicate_existing_manifest_ids':
        'Historical global stock-sci/p07-domain-adapter/manifest.json unavailable; current P07 uses branch-local IDs',
}


def statistics(result):
    return {'run': result.testsRun, 'passed': result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
            'failed_assertions': len(result.failures), 'errors': len(result.errors), 'skipped': len(result.skipped),
            'failures': [{'test': t.id(), 'traceback': trace} for t, trace in result.failures],
            'error_details': [{'test': t.id(), 'traceback': trace} for t, trace in result.errors]}


def main():
    from tools.seal import check
    if sys.argv[1:] == ['--check-seal']:
        print(json.dumps(check(), indent=2))
        return 0
    if sys.argv[1:]:
        raise ValueError('Unknown verification argument')
    reports = ROOT / 'reports'
    reports.mkdir(exist_ok=True)
    latest = reports / 'latest.json'
    # A later import or test failure must never leave a stale successful status.
    report = {'status': 'running', 'timestamp_utc': datetime.now(timezone.utc).isoformat()}
    latest.write_text(json.dumps(report, indent=2) + '\n')
    output = io.StringIO()
    try:
        report['source_seal'] = check()
        with redirect_stdout(output), redirect_stderr(output):
            from tests.test_p08_model import P08Tests
            from tests import test_current_compatibility
            loader = unittest.TestLoader()
            all_names = loader.getTestCaseNames(P08Tests)
            if len(all_names) != 25 or not set(GAPS) <= set(all_names):
                raise AssertionError('Recovered suite membership changed')
            runner = unittest.TextTestRunner(stream=output, verbosity=2)
            legacy = runner.run(unittest.TestSuite(P08Tests(name) for name in all_names))
            report['unmodified_legacy_diagnostic'] = statistics(legacy)
            failed_names = {t._testMethodName for t, _ in legacy.failures + legacy.errors}
            if (legacy.testsRun != 25 or len(legacy.failures) != 1 or len(legacy.errors) != 2
                    or legacy.skipped or failed_names != set(GAPS)):
                raise AssertionError('Unexpected legacy diagnostic outcome; inspect report')
            # Exact failure causes must remain visible and not mask a new defect.
            traces = '\n'.join(trace for _, trace in legacy.failures + legacy.errors)
            for required in ('AssertionError:', '3c6a8dc5', '1226a978',
                             "No module named 'cakood.p03_model'", 'stock-sci/p07-domain-adapter/manifest.json'):
                if required not in traces:
                    raise AssertionError('Legacy diagnostic cause changed: ' + required)
            applicable = runner.run(unittest.TestSuite(P08Tests(name) for name in all_names if name not in GAPS))
            report['applicable_recovered'] = statistics(applicable)
            current = runner.run(loader.loadTestsFromModule(test_current_compatibility))
            report['new_current_compatibility'] = statistics(current)
            if applicable.testsRun != 22 or current.testsRun != 11:
                raise AssertionError('Required test membership changed')
            if not applicable.wasSuccessful() or not current.wasSuccessful():
                raise AssertionError('Applicable verification failed')
        report['source_seal_after'] = check()
        if report['source_seal_after'] != report['source_seal']:
            raise AssertionError('Verification changed sealed source inputs')
        report['status'] = 'applicable-python-baseline-passed-with-explicit-legacy-gaps'
        report['applicable_total'] = {'passed': 33, 'failed': 0, 'errors': 0, 'skipped': 0}
        report['legacy_gaps_not_counted_as_passes'] = GAPS
        report['not_run'] = ['Full upstream regression suites', 'P08 SCI port/compiler/emitted parity',
                             'Native host ownership and real ScummVM autosave',
                             'Native input, art, dialogue/audio, controller or listening acceptance',
                             'Complete recovered P09 suite (only recovered P08-to-P09 gate was run)']
        code = 0
    except BaseException:
        report['status'] = 'failed'
        report['blocker'] = traceback.format_exc()
        output.write(report['blocker'])
        code = 1
    (reports / 'latest-tests.log').write_text(output.getvalue())
    latest.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
