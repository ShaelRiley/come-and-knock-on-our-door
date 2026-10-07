"""NEW path-only harness for the preserved original generator and exact edits.

Output is regenerated against current canonical bytes, NOT recovered fixture
bytes. This deliberately does not update historical assertions or object IDs.
"""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEPS = (
    'original-recorded/p08-fixture-generator.001.py.txt',
    'recorded-edits/p08-fixture.002-laugh-metadata.py.txt',
    'recorded-edits/p08-fixture.003-native-proposals.py.txt',
)
SUBSTITUTIONS = {
    '/workspace/shared/cakood/full-script': 'inputs/authority',
    '/workspace/shared/cakood/verbal-competitions-update/current-gdd.txt':
        'inputs/authority/complete-body.md',
}


def regenerate():
    old = Path.cwd()
    os.chdir(ROOT)
    try:
        (ROOT / 'tests/fixtures/p08').mkdir(parents=True, exist_ok=True)
        (ROOT / 'generated/generator').mkdir(parents=True, exist_ok=True)
        scope = {'__name__': '__fixture_regeneration__'}
        changes = []
        for path in STEPS:
            original = (ROOT / 'inputs/literal-p08' / path).read_text()
            rewritten = original
            replacements = []
            for before, after in SUBSTITUTIONS.items():
                count = rewritten.count(before)
                if count:
                    replacements.append({'before': before, 'after': after, 'count': count})
                    rewritten = rewritten.replace(before, after)
            target = ROOT / 'generated/generator' / Path(path).name.removesuffix('.txt')
            target.write_text(rewritten)
            exec(compile(rewritten, str(target), 'exec'), scope)
            changes.append({'source': 'inputs/literal-p08/' + path,
                            'executed_path': str(target.relative_to(ROOT)),
                            'path_only_replacements': replacements})
        fixture = ROOT / 'tests/fixtures/p08/canonical-bindings.json'
        data = json.loads(fixture.read_bytes())
        result = {'kind': 'newly regenerated fixture, not recovered original bytes',
                  'steps': changes, 'fixture_sha256': hashlib.sha256(fixture.read_bytes()).hexdigest(),
                  'fixture_bytes': fixture.stat().st_size, 'record_count': len(data['records']),
                  'catalog_sha256': data['catalog_sha256'], 'speech_sha256': data['speech_sha256'],
                  'gdd_sha256': data['gdd_sha256'],
                  'historical_catalog_assertion': '1226a97873a3693867c08afe2731ddb55adef6f0eaeabc1222e103c04c0d9fa7',
                  'historical_fixture_sha256_available': False,
                  'object_ids': 'Unchanged historical proposals only; no current registry allocation'}
        (ROOT / 'generated/fixture-provenance.json').write_text(json.dumps(result, indent=2) + '\n')
        return result
    finally:
        os.chdir(old)


if __name__ == '__main__':
    print(json.dumps(regenerate(), indent=2))
