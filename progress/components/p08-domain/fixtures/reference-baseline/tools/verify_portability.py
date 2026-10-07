"""NEW small fixed-member relocation and fail-closed inventory probes."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.seal import check


def main():
    seal = check()
    manifest = json.loads((ROOT / 'SOURCE-SEAL.json').read_bytes())
    report = {'source_seal': seal, 'guards': [], 'relocated': None,
              'method': 'copy only fixed source members and seal; no archives, network or original source reads'}
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH='')
    with tempfile.TemporaryDirectory(prefix='p08 portability ') as tmp:
        target = Path(tmp) / 'fresh reference with spaces'
        for name in [*manifest['files'], 'SOURCE-SEAL.json']:
            destination = target / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, destination)

        def run(*args):
            return subprocess.run([sys.executable, 'tools/verify.py', *args], cwd=target,
                                  env=env, text=True, capture_output=True)

        p08 = target / 'cakood/p08_model.py'
        original = p08.read_bytes()
        p08.write_bytes(original + b'\n# disposable altered-source probe\n')
        result = run('--check-seal')
        report['guards'].append({'case': 'changed_source', 'returncode': result.returncode,
                                'rejected': result.returncode != 0, 'output': result.stdout + result.stderr})
        p08.write_bytes(original)
        extra = target / 'cakood/unlisted_member.py'
        extra.write_text('raise RuntimeError("This must never be imported")\n')
        result = run('--check-seal')
        report['guards'].append({'case': 'unlisted_source', 'returncode': result.returncode,
                                'rejected': result.returncode != 0, 'output': result.stdout + result.stderr})
        extra.unlink()
        missing = target / 'dependencies/p06/cakood/verbal_contest.py'
        saved = missing.read_bytes()
        missing.unlink()
        stale = target / 'reports/latest.json'
        stale.parent.mkdir(exist_ok=True)
        stale.write_text('{"status":"deliberately stale success"}\n')
        result = run()
        status = json.loads(stale.read_bytes())['status']
        report['guards'].append({'case': 'missing_dependency_clears_stale_success', 'returncode': result.returncode,
                                'rejected': result.returncode != 0 and status == 'failed',
                                'new_status': status, 'output': result.stdout + result.stderr})
        missing.write_bytes(saved)
        result = run()
        report['relocated'] = json.loads(stale.read_bytes())
        report['relocated_returncode'] = result.returncode
        (ROOT / 'reports/relocated-tests.log').write_bytes((target / 'reports/latest-tests.log').read_bytes())
    report['status'] = ('passed' if all(g['rejected'] for g in report['guards'])
                        and report['relocated_returncode'] == 0
                        and report['relocated']['source_seal'] == seal else 'failed')
    report['original_seal_after'] = check()
    if report['original_seal_after'] != seal:
        report['status'] = 'failed'
    (ROOT / 'reports/portability.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'guard_count': len(report['guards']),
                      'relocated_total': report['relocated'].get('applicable_total'), 'source_seal': seal}, indent=2))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
