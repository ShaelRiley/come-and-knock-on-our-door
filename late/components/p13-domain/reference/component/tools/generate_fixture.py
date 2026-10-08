"""NEW full-field current P13 canonical fixture with original P08 support labels."""
from pathlib import Path
import hashlib,json,sys
C=Path(__file__).resolve().parents[1];sys.path.insert(0,str(C))
from tools.verify_inputs import verify
from cakood import p13_model as model
PINS={'complete-body.md':'18e2eb1a300cc1ac1192916441b640ca6134af619ee17eb424637b4dde28647c','full-line-catalog.json':'3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c','speech-units.json':'d143242b3d56f57331b0adfb73481425792c0757f57bc0c01a1b94561527c475'}
SUPPORT=('P08.LABEL.001','P08.LABEL.002','P08.LABEL.004','P08.LABEL.006')
def fixture():
 verify()
 for name,h in PINS.items():
  if hashlib.sha256((C/'authority'/name).read_bytes()).hexdigest()!=h:raise RuntimeError('Authority mismatch '+name)
 cat=json.loads((C/'authority/full-line-catalog.json').read_text());speech=json.loads((C/'authority/speech-units.json').read_text())
 records=[r for r in cat['records'] if r['id'] in model.RECORD_UNITS]
 support=[r for r in cat['records'] if r['id'] in SUPPORT]
 units=[u for u in speech['units'] if u['record_id'] in model.RECORD_UNITS]
 if {r['id'] for r in records}!=set(model.RECORD_UNITS) or len(records)!=45:raise RuntimeError('Incomplete P13 records')
 if len(units)!=40 or model.UNIT_SPEAKERS!={u['line_id']:u['speaker_id'] for u in units}:raise RuntimeError('P13 speaker mismatch')
 if {r['id'] for r in support}!=set(SUPPORT):raise RuntimeError('Missing P08 labels')
 for rid,tokens in model.RECORD_UNITS.items():
  if tuple(u['line_id'] for u in units if u['record_id']==rid)!=tokens:raise RuntimeError('Unit order mismatch')
 return dict(scope='NEW current-canonical fixture, full record/unit fields retained',editorial_revision=cat['editorial_revision'],catalog_sha256=PINS['full-line-catalog.json'],speech_sha256=PINS['speech-units.json'],gdd_sha256=PINS['complete-body.md'],records=records,support_records=support,speech_units=units,source_bindings=model.P13World.SOURCES,record_units=model.RECORD_UNITS)
if __name__=='__main__':
 p=C/'tests/fixtures/p13/canonical-bindings.json';p.parent.mkdir(parents=True,exist_ok=True);f=fixture();p.write_text(json.dumps(f,indent=2,ensure_ascii=False)+'\n');print('P13 canonical fixture: 45 records, 40 units, 4 P08 support labels')
