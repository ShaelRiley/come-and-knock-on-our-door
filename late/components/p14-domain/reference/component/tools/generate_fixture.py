"""NEW full-field current P14 canonical fixture, never reconstructed prose."""
from pathlib import Path
import hashlib,json,sys
C=Path(__file__).resolve().parents[1];sys.path.insert(0,str(C))
from tools.verify_inputs import verify
from cakood import p14_model as model
PINS={'complete-body.md':'18e2eb1a300cc1ac1192916441b640ca6134af619ee17eb424637b4dde28647c','full-line-catalog.json':'3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c','speech-units.json':'d143242b3d56f57331b0adfb73481425792c0757f57bc0c01a1b94561527c475'}
def fixture():
 verify()
 for name,h in PINS.items():
  if hashlib.sha256((C/'authority'/name).read_bytes()).hexdigest()!=h:raise RuntimeError('Authority mismatch '+name)
 cat=json.loads((C/'authority/full-line-catalog.json').read_text());speech=json.loads((C/'authority/speech-units.json').read_text())
 records=[r for r in cat['records'] if r['id'] in model.RECORD_UNITS]
 units=[u for u in speech['units'] if u['record_id'] in model.RECORD_UNITS]
 if {r['id'] for r in records}!=set(model.RECORD_UNITS) or len(records)!=125:raise RuntimeError('Incomplete P14 records')
 if len(units)!=43 or model.UNIT_SPEAKERS!={u['line_id']:u['speaker_id'] for u in units}:raise RuntimeError('P14 speaker mismatch')
 for rid,tokens in model.RECORD_UNITS.items():
  if tuple(u['line_id'] for u in units if u['record_id']==rid)!=tokens:raise RuntimeError('Unit order mismatch')
 return dict(scope='NEW current-canonical fixture, every record/unit field retained',editorial_revision=cat['editorial_revision'],catalog_sha256=PINS['full-line-catalog.json'],speech_sha256=PINS['speech-units.json'],gdd_sha256=PINS['complete-body.md'],records=records,speech_units=units,source_bindings=model.P14World.SOURCES,record_units=model.RECORD_UNITS)
if __name__=='__main__':
 p=C/'tests/fixtures/p14/canonical-bindings.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(fixture(),indent=2,ensure_ascii=False)+'\n');print('P14 fixture: 125 exact records, 43 units, 26 mandatory credits, 33 conditional asset credits')
