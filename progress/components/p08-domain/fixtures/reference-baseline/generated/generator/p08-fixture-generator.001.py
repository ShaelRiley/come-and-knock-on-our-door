from pathlib import Path
import hashlib,json
base=Path('inputs/authority')
d=json.loads((base/'full-line-catalog.json').read_text())
s=json.loads((base/'speech-units.json').read_text())
records={}
for r in d['records']:
 if not r['id'].startswith('P08.'):continue
 u=[x for x in s['units'] if x['record_id']==r['id']]
 records[r['id']]={k:r[k] for k in ('text_sha256','speaker_id','source_obligations')}
 records[r['id']].update(speech_units=[x['line_id'] for x in u],speech_speakers={x['line_id']:x['speaker_id'] for x in u})
 for x in u:
  if x.get('laugh_opportunity'):print('LAUGH',x['line_id'],x['laugh_opportunity'])
f={'purpose':'P08 stable ID/hash provenance only. Current approved full catalog owns player words.',
 'editorial_revision':d['editorial_revision'],'catalog_sha256':hashlib.sha256((base/'full-line-catalog.json').read_bytes()).hexdigest(),
 'speech_sha256':hashlib.sha256((base/'speech-units.json').read_bytes()).hexdigest(),
 'gdd_sha256':hashlib.sha256(Path('inputs/authority/complete-body.md').read_bytes()).hexdigest(),
 'records':records,'proposed_native_object_ids':dict(enumerate(['gate_lane','buffet_position','speaker_position','display_alcove','serving_table','kitchen_hatch','plan_overlay','circulation_plan','sightline_plan','placement_symbols'],116)),
 'reserved_native_object_ids':[126,127,128,129]}
Path('tests/fixtures/p08/canonical-bindings.json').write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n')
