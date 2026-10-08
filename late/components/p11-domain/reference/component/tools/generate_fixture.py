"""New portable P11 fixture, bound to current authority, not original recovery."""
from pathlib import Path
import hashlib
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cakood import p11_model as model

PINS = {
    'full-line-catalog.json': '3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c',
    'speech-units.json': 'd143242b3d56f57331b0adfb73481425792c0757f57bc0c01a1b94561527c475',
    'complete-body.md': '18e2eb1a300cc1ac1192916441b640ca6134af619ee17eb424637b4dde28647c',
    'accepted-insult-pairs.json': '62c3329fe59a92d407dbdbd3850966581386be9fcc5ed0c2cd276ed528316bdc',
}

def fixture():
    for name, digest in PINS.items():
        if hashlib.sha256((ROOT/'authority'/name).read_bytes()).hexdigest() != digest:
            raise ValueError('Changed authority: ' + name)
    catalog = json.loads((ROOT/'authority/full-line-catalog.json').read_text())
    speech = json.loads((ROOT/'authority/speech-units.json').read_text())
    records = {x['id']: x for x in catalog['records'] if x['id'] in model.RECORD_UNITS}
    units = [x for x in speech['units'] if x['record_id'] in records]
    if set(records) != set(model.RECORD_UNITS):
        raise ValueError('Canonical record registry differs')
    if {u['line_id']: u['speaker_id'] for u in units} != model.UNIT_SPEAKERS:
        raise ValueError('Canonical speaker registry differs')
    for record, expected in model.RECORD_UNITS.items():
        actual = tuple(u['line_id'] for u in units if u['record_id'] == record)
        if actual != expected:
            raise ValueError('Canonical unit order differs: ' + record)
    vc03 = {x['id']: x for x in catalog['records'] if x['id'].startswith('VC03.')}
    pairs = json.loads((ROOT/'authority/accepted-insult-pairs.json').read_text())
    return dict(scope='New current-authority P11 binding fixture; no historical-byte claim',
        catalog_sha256=PINS['full-line-catalog.json'], speech_sha256=PINS['speech-units.json'],
        gdd_sha256=PINS['complete-body.md'], accepted_pairs_sha256=PINS['accepted-insult-pairs.json'],
        historical_catalog_sha256='1226a97873a3693867c08afe2731ddb55adef6f0eaeabc1222e103c04c0d9fa7',
        editorial_revision=catalog['editorial_revision'], records=records, speech_units=units,
        source_bindings=model.P11World.SOURCES, record_units=model.RECORD_UNITS,
        vc03_records=vc03, vc03_speech_units=[u for u in speech['units'] if u['record_id'].startswith('VC03.')],
        contest_authority_scope='Retained exact VC03 records, variants and accepted-pair authority; no contest implementation or result mutation',
        accepted_pair_count=len(pairs['pairs']))

if __name__ == '__main__':
    path = ROOT/'tests/fixtures/p11/canonical-bindings.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    data = fixture()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    print('Verified current authority: %s records, %s speech units' % (len(data['records']), len(data['speech_units'])))
