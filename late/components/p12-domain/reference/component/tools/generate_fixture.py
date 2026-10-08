"""New, portable binding fixture from exact current authority, with all metadata."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from tools.verify_inputs import verify
from cakood import p12_model as model
PINS={'full-line-catalog.json':'3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c','speech-units.json':'d143242b3d56f57331b0adfb73481425792c0757f57bc0c01a1b94561527c475','complete-body.md':'18e2eb1a300cc1ac1192916441b640ca6134af619ee17eb424637b4dde28647c'}
def fixture():
 verify()
 for name,digest in PINS.items():
  if hashlib.sha256((ROOT/'authority'/name).read_bytes()).hexdigest()!=digest:raise RuntimeError('Authority mismatch: '+name)
 catalog=json.loads((ROOT/'authority/full-line-catalog.json').read_text());speech=json.loads((ROOT/'authority/speech-units.json').read_text())
 records=[r for r in catalog['records'] if r['id'].startswith('P12.') or r['id']=='VC03.NEED_RESOLUTION']
 units=[u for u in speech['units'] if u['record_id'] in {r['id'] for r in records}]
 if set(model.RECORD_UNITS)!={r['id'] for r in records}:raise RuntimeError('Incomplete P12 record binding')
 if model.UNIT_SPEAKERS!={u['line_id']:u['speaker_id'] for u in units}:raise RuntimeError('P12 speaker mismatch')
 for rid,tokens in model.RECORD_UNITS.items():
  if tuple(u['line_id'] for u in units if u['record_id']==rid)!=tokens:raise RuntimeError('Unit sequence mismatch: '+rid)
 return dict(scope='New current-canonical P12 fixture; all record and speech metadata preserved',catalog_sha256=PINS['full-line-catalog.json'],speech_sha256=PINS['speech-units.json'],gdd_sha256=PINS['complete-body.md'],records=records,speech_units=units,source_bindings=model.P12World.SOURCES,record_units=model.RECORD_UNITS,editorial_revision=catalog['editorial_revision'])
if __name__=='__main__':
 target=ROOT/'tests/fixtures/p12/canonical-bindings.json';target.parent.mkdir(parents=True,exist_ok=True)
 data=fixture();target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');print('Canonical bindings:',len(data['records']),'records,',len(data['speech_units']),'speech units')
