#!/usr/bin/env python3
"""New additive P11 and finite VC03 scene exporter; not recovered historical source."""
from pathlib import Path
from copy import deepcopy
import json,sys,re
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE/'inputs/model';AUTHORITY=HERE/'inputs/authority';BASELINE=HERE/'inputs';SCI=HERE/'inputs/p08'
sys.path.insert(0,str(ROOT))
from cakood import p11_model as model
import caption_util as util
from guard import input_check
sha,dump,norm,paginate=util.sha,util.dump,util.norm,util.paginate
TEXT_RESOURCE,MODULE=212,923
CATALOG_SHA='3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c'
SPEECH_SHA='d143242b3d56f57331b0adfb73481425792c0757f57bc0c01a1b94561527c475'
GDD_SHA='18e2eb1a300cc1ac1192916441b640ca6134af619ee17eb424637b4dde28647c'

def generate():
 input_check();out=HERE/'generated';out.mkdir(exist_ok=True);(out/'speech').mkdir(exist_ok=True);(HERE/'snapshot').mkdir(exist_ok=True);(HERE/'evidence').mkdir(exist_ok=True)
 assert sha((AUTHORITY/'full-line-catalog.json').read_bytes())==CATALOG_SHA
 assert sha((AUTHORITY/'speech-units.json').read_bytes())==SPEECH_SHA
 assert sha((AUTHORITY/'complete-body.md').read_bytes())==GDD_SHA
 catalog=json.loads((AUTHORITY/'full-line-catalog.json').read_text());speech=json.loads((AUTHORITY/'speech-units.json').read_text())
 cat={r['id']:r for r in catalog['records']};allunits={u['line_id']:u for u in speech['units']}
 fixture=json.loads((ROOT/'tests/fixtures/p11/canonical-bindings.json').read_text());adapter=json.loads((HERE/'inputs/domain/schema.json').read_text());pin=json.loads((HERE/'COMPATIBILITY.json').read_text())
 records={rid:cat[rid] for rid in sorted(adapter['line_ids'],key=adapter['line_ids'].get)}
 units=[allunits[uid] for uid in sorted(adapter['speech_unit_ids'],key=adapter['speech_unit_ids'].get)]
 assert len(records)==26 and len(units)==36
 assert records==fixture['records'];assert adapter['speech_metadata']==units==fixture['speech_units']
 assert adapter['source_bindings']==fixture['source_bindings']==model.P11World.SOURCES
 assert fixture['record_units']=={k:list(v) for k,v in model.RECORD_UNITS.items()}
 assert (fixture['catalog_sha256'],fixture['speech_sha256'],fixture['gdd_sha256'])==(CATALOG_SHA,SPEECH_SHA,GDD_SHA)
 assert pin['text']==TEXT_RESOURCE and pin['audio']==MODULE
 # Check exact current domain method bindings without importing its implementation.
 src=(HERE/'inputs/domain/src/p11-domain.sc').read_text() if (HERE/'inputs/domain/src/p11-domain.sc').exists() else next((HERE/'inputs/domain/src').glob('*.sc')).read_text()
 sys.path.insert(0,str(HERE/'tools'));from source_tools import methods
 method_bodies=methods(src)
 signatures={n:re.search(r'\(method \(([^)]*)\)',body)[1] for n,body in method_bodies.items()}
 for n in ['p11Line','p11Unit','p11Begin','p11Resume','p11Acknowledge','p11RescueCreditVariant','p11SerialHi','p11SerialLo']:assert n in signatures,n
 protected={str(p.relative_to(HERE)):sha(p.read_bytes()) for p in sorted((HERE/'inputs').rglob('*')) if p.is_file()}
 profile_hash=sha((SCI/'inputs/talk-prototype/profiles.json').read_bytes());renderer_hash=sha((SCI/'inputs/talk-prototype/talk.py').read_bytes())
 # Finite outcomes use original unit IDs plus explicit variant identity, never invented IDs.
 variants=[]
 for rid in ['VC03.WIN','VC03.LOSS']:
  original=cat[rid];assert original==fixture['vc03_records'][rid]
  assert [u for u in allunits.values() if u['record_id']==rid]==[u for u in fixture['vc03_speech_units'] if u['record_id']==rid]
  for variant in original['finite_variants']:
   selected=deepcopy(original);selected['text']=variant['text'];selected['text_sha256']=sha(json.dumps(selected['text'],ensure_ascii=False).encode())
   selected_units=[]
   for u in [v for v in allunits.values() if v['record_id']==rid]:
    chosen=deepcopy(u)
    if 'finite_variants' in u:
     v=next(v for v in u['finite_variants'] if v['variant_id']==variant['variant_id']);chosen.update(text=v['text'],caption_text=v['caption_text'])
    assert chosen['text']==selected['text'][len(selected_units)]['text']
    selected_units.append(chosen)
   variants.append((selected,selected_units,variant['variant_id'],variant))
 bank=[];bank_index={};pages=[];routes=[];vroutes=[];voices=[]
 def entry(text):
  raw=text.encode('ascii');assert b'\0' not in raw
  if raw not in bank_index:bank_index[raw]=len(bank);bank.append(raw)
  return bank_index[raw]
 def export_record(record,record_units,document,local,variant_id=None,predicate=None):
  rid=record['id'];first=len(pages);segments=util.source_segments(record,record_units)
  for si,segment in enumerate(segments):
   raw=segment['source_text']
   if variant_id:
    index=next(i for i,v in enumerate(cat[rid]['finite_variants']) if v['variant_id']==variant_id)
    segment['selected_text_pointer']=segment['source_pointer'];segment['source_pointer']=f'/finite_variants/{index}'+segment['source_pointer']
   segment.update(source_text_sha256=sha(raw.encode()),source_words=len(raw.split()),source_characters=len(raw),source_utf8_bytes=len(raw.encode()))
   unit=next((u for u in record_units if u['line_id']==segment['line_id']),None);uid=adapter['speech_unit_ids'].get(segment['line_id'],0)
   if unit:segment['canonical_speech_unit']=unit
   group=paginate(raw);header=entry(norm(segment['source_speaker']));assert len(bank[header])*6<=204
   for part,p in enumerate(group):
    p.update(record_id=rid,document_id=document,local_line_key=local,global_line_key=document,line_id=segment['line_id'],speech_unit_id=uid,
      variant_id=variant_id,source_pointer=segment['source_pointer'],segment_index=si,source_text_sha256=segment['source_text_sha256'],part=part,part_count=len(group),
      last_of_unit=bool(unit and part==len(group)-1),resource=TEXT_RESOURCE,entry=entry(p['text']),header_entry=header,display_name=segment['source_speaker'],speaker_id=segment['speaker_id'],
      speaker_number=util.SPEAKERS.get(segment['speaker_id'],0),role=segment['role'],voice_index=0,audio_module=0,duration_ticks=0,canonical_location=record['location'],
      source_words=len(p['raw_text'].split()),source_characters=len(p['raw_text']),source_utf8_bytes=len(p['raw_text'].encode()),canonical_speech_unit=unit,
      delivery='silent_text',mouth_gate='no_actor_mouth',document_kind='variant_record' if variant_id else 'record')
    if unit:
     noun=len(voices)+1;fragment=segment['line_id']+('.'+variant_id if variant_id else '')+f'.page{part+1:02d}'
     plan=util.talk.schedule(fragment,segment['speaker_id'],p['raw_text']);audio=util.talk.render(plan);sync=util.talk.sync_patch(plan);filename=util.talk.patch_name(MODULE,noun)
     (out/'speech'/filename).write_bytes(audio);(out/'speech'/('#'+filename[1:])).write_bytes(sync)
     v={k:p[k] for k in ['record_id','line_id','variant_id','speaker_id','raw_text','raw_text_sha256','part','part_count','source_char_range','source_utf8_byte_range']}
     v.update(fragment_id=fragment,voice_index=noun,audio36=dict(module=MODULE,noun=noun,verb=1,cond=0,seq=1),audio_file=filename,sync_file='#'+filename[1:],audio_sha256=sha(audio),sync_sha256=sha(sync),
       duration_ticks=plan['duration_ticks'],mouth_events=plan['mouth_events'],generation='unchanged_approved_local_original_procedural_renderer',profile_sha256=profile_hash,renderer_sha256=renderer_hash,
       canonical_speech_unit=unit,laugh_opportunity=unit.get('laugh_opportunity'),audible_gate='host_proves_actual_audible_presence_in_rescue_geometry',mouth_gate='host_proves_actual_visible_speaker_in_rescue_geometry')
     voices.append(v);p.update(voice_index=noun,audio_module=MODULE,duration_ticks=v['duration_ticks'],delivery='principal',mouth_gate=v['mouth_gate'])
    p['fields']=[p['entry'],document,part,len(group),p['speaker_number'],p['voice_index'],header,p['bytes_with_nul']]
    p.update(record_page=len(pages)-first,document_page=len(pages)-first,page_index=len(pages));pages.append(p)
  return dict(record_id=rid,variant_id=variant_id,local_line_key=local,global_line_key=document,document_id=document,document_kind='variant_record' if variant_id else 'record',dispatch='scene',first_page=first,
    page_count=len(pages)-first,page_indices=list(range(first,len(pages))),kind=record['kind'],source_ref=record['source_ref'],trigger=record['trigger'],source_obligations=record['source_obligations'],
    canonical_provenance=cat[rid],canonical_location=record['location'],source_text=record['text'],source_text_json_sha256=record['text_sha256'],segments=segments,canonical_units=[u['line_id'] for u in record_units],predicate=predicate)
 for rid,r in records.items():routes.append(export_record(r,[u for u in units if u['record_id']==rid],1299+adapter['line_ids'][rid],adapter['line_ids'][rid]))
 base_record_pages=len(pages)
 unit_routes=[];vunits=[]
 def export_unit(u,record,document,variant=None):
  first=len(pages);originals=[pages[i] for i in record['page_indices'] if pages[i]['line_id']==u['line_id']]
  assert originals
  for index,original in enumerate(originals):
   p=deepcopy(original);p.update(document_id=document,global_line_key=document,document_page=index,document_kind='variant_unit' if variant else 'speech_unit',source_record_page_index=original['page_index'],page_index=len(pages));p['fields'][1]=document;pages.append(p)
  return dict(record_id=u['record_id'],line_id=u['line_id'],speech_unit_id=adapter['speech_unit_ids'].get(u['line_id'],0),variant_id=variant,
    local_line_key=record['local_line_key'],document_id=document,global_line_key=document,document_kind='variant_unit' if variant else 'speech_unit',dispatch='scene',first_page=first,page_count=len(pages)-first,
    page_indices=list(range(first,len(pages))),source_record_document=record['document_id'],source_record_pages=[p['record_page'] for p in originals],canonical_speech_unit=u,source_text=u['text'],source_text_sha256=sha(u['text'].encode()))
 by_id={r['record_id']:r for r in routes}
 for u in units:unit_routes.append(export_unit(u,by_id[u['record_id']],1325+adapter['speech_unit_ids'][u['line_id']]))
 for i,(r,us,variant,predicate) in enumerate(variants):vroutes.append(export_record(r,us,1362+i,0,variant,predicate))
 for i,((r,us,variant,predicate),route) in enumerate(zip(variants,vroutes)):
  for j,u in enumerate(us):vunits.append(export_unit(u,route,1366+2*i+j,variant))
 by_unit={u['line_id']:u for u in unit_routes}
 record_receipts={r['record_id']:dict(record_id=r['record_id'],record_number=r['local_line_key'],document_id=r['document_id'],pages=[[r['document_id'],n] for n in range(r['page_count'])],
   canonical_tokens=list(model.RECORD_UNITS[r['record_id']] or (r['record_id'],)),units=[dict(line_id=u,speech_unit_id=adapter['speech_unit_ids'][u],record_pages=by_unit[u]['source_record_pages'],last_record_page=by_unit[u]['source_record_pages'][-1],unit_document=by_unit[u]['document_id']) for u in r['canonical_units']]) for r in routes}
 unit_receipts={u['line_id']:dict(line_id=u['line_id'],record_id=u['record_id'],speech_unit_id=u['speech_unit_id'],document_id=u['document_id'],pages=[[u['document_id'],n] for n in range(u['page_count'])],record_pages=[[u['source_record_document'],n] for n in u['source_record_pages']],source_text_sha256=u['source_text_sha256']) for u in unit_routes}
 source_receipts={s:dict(source_number=adapter['sources'][s],record_ids=[rid],documents=[by_id[rid]['document_id']],canonical_tokens=[t['token'] for t in adapter['receipts'][s]],token_numbers=[adapter['tokens'][t['token']] for t in adapter['receipts'][s]]) for s,rid in adapter['source_bindings'].items()}
 payload=b'\0'.join(bank)+b'\0';assert len(payload)<32768;(out/f'{TEXT_RESOURCE}.text.bin').write_bytes(payload)
 offsets=[];pos=0
 for b in bank:offsets.append(pos);pos+=len(b)+1
 for p in pages:p.update(text_bank_byte_range=[offsets[p['entry']],offsets[p['entry']]+p['bytes_with_nul']],display_ascii_sha256=sha(bank[p['entry']]))
 docs=[{k:r[k] for k in ['document_id','record_id','variant_id','document_kind','first_page','page_count','page_indices']}|({k:r[k] for k in ['line_id','speech_unit_id']} if 'line_id' in r else {}) for r in routes+unit_routes+vroutes+vunits]
 assert [r['document_id'] for r in docs]==list(range(1300,1374))
 host=dict(domain_script=993,domain_standalone_species=1,domain_production_reserved_species=15,scene_script=982,scene_species=4,
   record_document='Exact p11Line keys1..26; additive maps only',unit_document='Exact p11Unit keys1..36; variants retain original outcome unit IDs separately',
   acknowledge=signatures['p11Acknowledge'],method_bindings=signatures,
   rescue_credit_getter=signatures['p11RescueCreditVariant'],rescue_serial_getters=[signatures['p11SerialHi'],signatures['p11SerialLo']],rescue_serial_slots={'peg_ack_at':7,'advance_peg_at':8},
   request_snapshot='Future host must snapshot getter variant and both serials with exact P11 VC03 request; generic contest owner currently emits base wording.',
   presentation='Existing sdOpen/sdDraw/Graph12/sdPresented/sdSpeak only; no new selector or API.',lease='Exact source/start/epoch plus complete visible page evidence; retire on close, travel, apron, menu, restore or replacement.',
   presence='Bunny at actual porch side and Frankie at actual courtyard side can be audible across rescue geometry. Never teleport actors to the player room. Host proves eligibility and actual visible/audible presence.',
   sincere='Bunny canonical porch presence and Felix continuous listener required for every new sincere receipt and resume, including final Jackie-only reply.',
   silence='Printed/interface/choice/hint records have no voice or mouth activity.',generic_codes='Unbound status codes remain unbound; no invented fallback text.')
 manifest=dict(schema=1,scope='New editable P11 scene/procedural audio implementation with additive finite VC03 variants; no native or recovered exporter claim.',catalog_sha256=CATALOG_SHA,speech_sha256=SPEECH_SHA,gdd_sha256=GDD_SHA,
   protected_inputs_sha256=protected,text_resource=TEXT_RESOURCE,text_resource_sha256=sha(payload),text_bytes=len(payload),entries=len(bank),max_body_bytes=max(p['bytes_with_nul'] for p in pages),audio_modules=[MODULE],profile_sha256=profile_hash,renderer_sha256=renderer_hash,
   geometry=dict(columns=50,body_lines=3,font=util.font_metrics(),body=[6,158,314,182],header=[6,147,210,155],header_separate=True),speaker_numbers=util.SPEAKERS,
   line_keys={r['record_id']:r['document_id'] for r in routes},local_line_keys=adapter['line_ids'],local_unit_keys=adapter['speech_unit_ids'],unit_documents={r['line_id']:r['document_id'] for r in unit_routes},
   canonical_speech_units=units,routes=routes,unit_routes=unit_routes,variant_routes=vroutes,variant_unit_routes=vunits,document_routes=docs,pages=pages,speech=voices,missing_speech=[],source_bindings=adapter['source_bindings'],
   record_receipts=record_receipts,unit_receipts=unit_receipts,source_receipts=source_receipts,silent_readers={s:r for s,r in source_receipts.items() if not model.RECORD_UNITS[adapter['source_bindings'][s]]},host_api=host,
   receipt_semantics=dict(full_record_requires_all_pages=True,unit_requires_all_unit_pages=True,queue_open_last_page_audio_completion_are_not_display_receipts=True,full_source_and_unit_authority_distinct=True,variant_identity_required=True,partial_selected_unit_never_complete=True),
   ownership_contract=dict(peg_owner='P04',original_display=42,original_cart=72,original_controls=adapter['own_objects'],p14='All four actual contest wins remain required. VC03 loss can allow practical P12 progress; no WIN/signature/reveal consent supplied.'),
   coverage=dict(authority_records=len(records),canonical_speech_units=len(units),record_documents=len(routes),unit_documents=len(unit_routes),variant_record_documents=len(vroutes),variant_unit_documents=len(vunits),routable_documents=len(docs),record_pages=base_record_pages,unit_pages=sum(r['page_count'] for r in unit_routes),variant_record_pages=sum(r['page_count'] for r in vroutes),variant_unit_pages=sum(r['page_count'] for r in vunits),pages=len(pages),voiced_fragments=len(voices),caption_only_pages=sum(not p['voice_index'] for p in pages),source_words=sum(s['source_words'] for r in routes for s in r['segments']),source_characters=sum(s['source_characters'] for r in routes for s in r['segments'])),
   explicit_gaps=['No production species15 or native host activation','No native pixels, actual actors, audio listening, controller or SaveGame/RestoreGame proof','Generic contest owner not yet variant-aware; future snapshot/dispatch required'])
 dump(out/'manifest.json',manifest)
 for name,value in [('line-document-map',{r['record_id']:{k:r[k] for k in ['local_line_key','document_id','page_count']} for r in routes}),('unit-document-map',{r['line_id']:{k:r[k] for k in ['speech_unit_id','document_id','page_count','source_record_document','source_record_pages']} for r in unit_routes}),('variant-document-map',dict(records=vroutes,units=vunits,selection=cat['VC03.WIN']['variant_binding'])),('receipt-map',{k:manifest[k] for k in ['record_receipts','unit_receipts','source_receipts','receipt_semantics']}),('host-contract',host)]:dump(out/(name+'.json'),value)
 dump(HERE/'snapshot/canonical-records.json',dict(records=list(records.values()),outcomes=[cat['VC03.WIN'],cat['VC03.LOSS']]))
 dump(HERE/'snapshot/canonical-speech-units.json',dict(units=units,outcomes=[u for u in allunits.values() if u['record_id'] in ['VC03.WIN','VC03.LOSS']]))
 dump(HERE/'snapshot/domain-method-bindings.json',signatures)
 dump(HERE/'evidence/allocation-check.json',dict(status='PASS',text=TEXT_RESOURCE,audio_module=MODULE,documents=[1300,1373],new_selectors=[],typed_inventory='inputs/typed-resource-inventory.json'))
 print(json.dumps(manifest['coverage'],indent=2));return manifest
if __name__=='__main__':generate()
