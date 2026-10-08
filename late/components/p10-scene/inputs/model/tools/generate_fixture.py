"""New portable current-authority fixture, not a recovered historical fixture."""
from pathlib import Path
import hashlib
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cakood import p10_model as model
PINS = {
    'full-line-catalog.json': '3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c',
    'speech-units.json': 'd143242b3d56f57331b0adfb73481425792c0757f57bc0c01a1b94561527c475',
    'complete-body.md': '18e2eb1a300cc1ac1192916441b640ca6134af619ee17eb424637b4dde28647c',
}
def fixture():
    for name, digest in PINS.items():
        if hashlib.sha256((ROOT/'authority'/name).read_bytes()).hexdigest() != digest:
            raise ValueError('Changed authority: ' + name)
    catalog = json.loads((ROOT/'authority/full-line-catalog.json').read_text())
    speech = json.loads((ROOT/'authority/speech-units.json').read_text())
    records = {x['id']: x for x in catalog['records'] if x['id'].startswith('P10.')}
    units = [x for x in speech['units'] if x['record_id'].startswith('P10.')]
    if set(records) != set(model.RECORD_UNITS):
        raise ValueError('Canonical record registry differs')
    if {u['line_id']: u['speaker_id'] for u in units} != model.UNIT_SPEAKERS:
        raise ValueError('Canonical speaker registry differs')
    for record, expected in model.RECORD_UNITS.items():
        actual = tuple(u['line_id'] for u in units if u['record_id'] == record)
        if actual != expected:
            raise ValueError('Canonical unit order differs: ' + record)
    return dict(scope='New current-authority P10 binding fixture; no historical-byte claim',
                catalog_sha256=PINS['full-line-catalog.json'], speech_sha256=PINS['speech-units.json'],
                gdd_sha256=PINS['complete-body.md'], editorial_revision=catalog['editorial_revision'],
                historical_catalog_sha256='1226a97873a3693867c08afe2731ddb55adef6f0eaeabc1222e103c04c0d9fa7',
                composition_scope='Accepted reference models with modeled autosave acknowledgment; no native save I/O or completed P08 host integration',
                records=records, speech_units=units, source_bindings=model.P10World.SOURCES,
                record_units=model.RECORD_UNITS, speakers=model.UNIT_SPEAKERS)
if __name__ == '__main__':
    destination = ROOT/'tests/fixtures/p10/canonical-bindings.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(fixture(), ensure_ascii=False, indent=2)+'\n')
    print('Verified current authority; wrote 23 records and 20 speech units')
