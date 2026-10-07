import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'authority'; cat=root/'full-line-catalog.json'; speech=root/'speech-units.json'; gdd=root/'complete-body.md'
rows=json.loads(cat.read_text())['records']; units=json.loads(speech.read_text())['units']; revision=json.loads((root/'CURRENT-SCRIPT-REVISION.json').read_text())
records={}
for r in rows:
 if r['id'].startswith('P09.'):
  us=[u for u in units if u['record_id']==r['id']]
  records[r['id']]={'text_sha256':r['text_sha256'],'speaker_id':r['speaker_id'],'trigger':r['trigger'],'source_obligations':r['source_obligations'],'speech_units':[u['line_id'] for u in us], 'speech_speakers':{u['line_id']:u['speaker_id'] for u in us}}
data={'purpose':'P09 stable ID/hash provenance only. Current approved full catalog owns player words.', 'editorial_revision':revision['editorial_revision'],'catalog_sha256':hashlib.sha256(cat.read_bytes()).hexdigest(),'speech_sha256':hashlib.sha256(speech.read_bytes()).hexdigest(),'gdd_sha256':hashlib.sha256(gdd.read_bytes()).hexdigest(),'records':records,'speech_metadata':[{k:u[k] for k in ('line_id','record_id','speaker_id','laugh_opportunity')} for u in units if u['record_id'].startswith('P09.')], 'binding_rules':{'rumor_routes':['P09.LOOK.001','P09.DIALOGUE.001','P09.FAILURE.001.01'],'chair_tag_alone_does_not_clear':True,'audience_has_no_p09_disclosure':True,'terms_required_units':[f'P09.DIALOGUE.002.{i:02}' for i in range(1,6)],'unsigned_card_outcome':'P09.SUCCESS.001','card_signature_owner':'P14'}}
p=Path(__file__).resolve().parents[1]/'tests/fixtures/p09/canonical-bindings.json'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n'); print(len(records),'records and',len(data['speech_metadata']),'speech units bound')
