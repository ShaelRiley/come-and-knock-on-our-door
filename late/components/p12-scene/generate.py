#!/usr/bin/env python3
"""New additive P12 and finite VC03 scene exporter; not recovered historical source."""
from pathlib import Path
from copy import deepcopy
import json,sys,re,itertools,importlib.util,argparse
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE/'inputs/model';AUTHORITY=HERE/'inputs/authority';BASELINE=HERE/'inputs';SCI=HERE/'inputs/p08'
sys.path.insert(0,str(ROOT))
from cakood import p12_model as model
import caption_util as util
from guard import input_check
sha,dump,norm,paginate=util.sha,util.dump,util.norm,util.paginate
TEXT_RESOURCE,MODULE=213,924
CATALOG_SHA='3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c'
SPEECH_SHA='d143242b3d56f57331b0adfb73481425792c0757f57bc0c01a1b94561527c475'
GDD_SHA='18e2eb1a300cc1ac1192916441b640ca6134af619ee17eb424637b4dde28647c'

def generate(render_principals=False):
 input_check();out=HERE/'generated';out.mkdir(exist_ok=True);(out/'speech').mkdir(exist_ok=True);(HERE/'snapshot').mkdir(exist_ok=True);(HERE/'evidence').mkdir(exist_ok=True)
 assert sha((AUTHORITY/'full-line-catalog.json').read_bytes())==CATALOG_SHA
 assert sha((AUTHORITY/'speech-units.json').read_bytes())==SPEECH_SHA
 assert sha((AUTHORITY/'complete-body.md').read_bytes())==GDD_SHA
 catalog=json.loads((AUTHORITY/'full-line-catalog.json').read_text());speech=json.loads((AUTHORITY/'speech-units.json').read_text())
 cat={r['id']:r for r in catalog['records']};allunits={u['line_id']:u for u in speech['units']}
 fixture=json.loads((ROOT/'tests/fixtures/p12/canonical-bindings.json').read_text());adapter=json.loads((HERE/'inputs/domain/schema.json').read_text());pin=json.loads((HERE/'COMPATIBILITY.json').read_text())
 records={rid:cat[rid] for rid in sorted(adapter['line_ids'],key=adapter['line_ids'].get)}
 units=[allunits[uid] for uid in sorted(adapter['speech_unit_ids'],key=adapter['speech_unit_ids'].get)]
 assert len(records)==30 and len(units)==36
 assert list(records.values())==fixture['records'];assert records==adapter['canonical_records'];assert adapter['speech_metadata']==units==fixture['speech_units']
 assert adapter['source_bindings']==fixture['source_bindings']==model.P12World.SOURCES
 assert fixture['record_units']=={k:list(v) for k,v in model.RECORD_UNITS.items()}
 assert (fixture['catalog_sha256'],fixture['speech_sha256'],fixture['gdd_sha256'])==(CATALOG_SHA,SPEECH_SHA,GDD_SHA)
 assert sha((ROOT/'cakood/p12_model.py').read_bytes())==adapter['model_sha256']
 assert sha((ROOT/'tests/fixtures/p12/canonical-bindings.json').read_bytes())==adapter['fixture_sha256']
 assert sha((HERE/'inputs/domain/src/module994.sc').read_bytes())==adapter['source_sha256']
 assert pin['text']==TEXT_RESOURCE and pin['audio']==MODULE
 inventory=json.loads((HERE/'inputs/typed-resource-inventory.json').read_text())
 assert not any(r['type']==3 and r['number']==TEXT_RESOURCE for r in inventory['typed'])
 assert not set(range(1400,1490))&set(inventory['documents']['occupied'])
 assert MODULE not in pin['predecessor']['audio_modules']
 # Check exact current domain method bindings without importing its implementation.
 src=(HERE/'inputs/domain/src/p12-domain.sc').read_text() if (HERE/'inputs/domain/src/p12-domain.sc').exists() else next((HERE/'inputs/domain/src').glob('*.sc')).read_text()
 sys.path.insert(0,str(HERE/'tools'));from source_tools import methods
 method_bodies=methods(src)
 signatures={n:re.search(r'\(method \(([^)]*)\)',body)[1] for n,body in method_bodies.items()}
 for n in ['p12Line','p12Unit','p12Begin','p12Resume','p12Acknowledge','p12SerialHi','p12SerialLo']:assert n in signatures,n
 protected={str(p.relative_to(HERE)):sha(p.read_bytes()) for p in sorted((HERE/'inputs').rglob('*')) if p.is_file()}
 profile_hash=sha((SCI/'inputs/talk-prototype/profiles.json').read_bytes());renderer_hash=sha((SCI/'inputs/talk-prototype/talk.py').read_bytes())
 gap=json.loads((HERE/'inputs/gap-v0/generated/manifest.json').read_text());frozen_principals={v['fragment_id']:v for v in gap['speech']}
 assert len(frozen_principals)==39 and gap['renderer_sha256']==renderer_hash and gap['profile_sha256']==profile_hash
 audience_root=HERE/'inputs/audience-component'
 assert sha((audience_root/'audience.py').read_bytes())=='7f4cb97029074a40c5e19e81e55ff7fbbd4a7b2a7e319c66a841f9a9dbc11a5f'
 assert sha((audience_root/'generated/manifest.json').read_bytes())=='f8c57fd4ade8090a1f538e07cc832e864c935ca07fda924970ebf92cba8e6acf'
 audience_manifest=json.loads((audience_root/'generated/manifest.json').read_text())
 assert audience_manifest['handoff_sha256']=='ad08a2d68dfd2e6cdb84df857de4c5104d69aee122d0e6d42e24863989b8cb45'
 assert audience_manifest['principal_renderer_sha256']==renderer_hash and audience_manifest['principal_profiles_sha256']==profile_hash
 spec=importlib.util.spec_from_file_location('frozen_original_audience',audience_root/'audience.py');audience=importlib.util.module_from_spec(spec);spec.loader.exec_module(audience)
 assert all(callable(getattr(audience,n)) for n in ['schedule','render','sync_patch','patch_name','select_observed_fragments'])

 dynamic_records={'P12.DIALOGUE.001','P12.LOOK.003'}
 assert {rid for rid,r in records.items() if r.get('dynamic_bindings')}==dynamic_records
 assert {v for r in records.values() for txt in ([x['text'] for x in r['text']] if isinstance(r['text'],list) else [r['text']]) for v in re.findall(r'\{([^{}]+)\}',txt)}=={'visible_cue_order'}
 variants=[]
 for rid in sorted(dynamic_records):
  original=cat[rid];unit=next(u for u in units if u['record_id']==rid)
  for order in itertools.permutations((1,2,3)):
   words=[next(k for k,v in adapter['words'].items() if v==n) for n in order]
   binding={'visible_cue_order':', '.join(words)};selected=deepcopy(original);selected['text']=original['text'].format(**binding);selected['text_sha256']=sha(json.dumps(selected['text'],ensure_ascii=False).encode())
   projected=deepcopy(unit);projected['text']=selected['text'];projected['caption_text']=unit['caption_text'].replace('{visible_cue_order}',binding['visible_cue_order'])
   variants.append((selected,[projected],'cue_'+''.join(map(str,order)),dict(kind='observed_visible_cue_order',word_ids=list(order),bindings=binding,query='p12VisibleWord',query_indices=[0,1,2],no_default=True)))
 bank=[];bank_index={};pages=[];routes=[];vroutes=[];voices=[]
 def entry(text):
  raw=text.encode('ascii');assert b'\0' not in raw
  if raw not in bank_index:bank_index[raw]=len(bank);bank.append(raw)
  return bank_index[raw]
 def export_record(record,record_units,document,local,variant_id=None,predicate=None,emit=True):
  rid=record['id'];first=len(pages);segments=util.source_segments(record,record_units)
  for si,segment in enumerate(segments):
   raw=segment['source_text']
   if variant_id:
    template=cat[rid]['text'];token='{visible_cue_order}';at=template.index(token);bound=predicate['bindings']['visible_cue_order']
    segment.update(source_template=template,source_template_sha256=sha(template.encode()),binding=predicate,
      substitution=dict(name='visible_cue_order',template_char_range=[at,at+len(token)],expanded_char_range=[at,at+len(bound)],observed_value=bound))
   segment.update(source_text_sha256=sha(raw.encode()),source_words=len(raw.split()),source_characters=len(raw),source_utf8_bytes=len(raw.encode()))
   unit=next((u for u in record_units if u['line_id']==segment['line_id']),None);uid=adapter['speech_unit_ids'].get(segment['line_id'],0)
   if unit:segment['canonical_speech_unit']=allunits[unit['line_id']]
   group=paginate(raw) if emit else [];header=entry(norm(segment['source_speaker']));assert len(bank[header])*6<=204
   for part,p in enumerate(group):
    p.update(record_id=rid,document_id=document,local_line_key=local,global_line_key=document,line_id=segment['line_id'],speech_unit_id=uid,
      variant_id=variant_id,source_pointer=segment['source_pointer'],segment_index=si,source_text_sha256=segment['source_text_sha256'],part=part,part_count=len(group),
      last_of_unit=bool(unit and part==len(group)-1),resource=TEXT_RESOURCE,entry=entry(p['text']),header_entry=header,display_name=segment['source_speaker'],speaker_id=segment['speaker_id'],
      speaker_number=util.SPEAKERS.get(segment['speaker_id'],0),role=segment['role'],voice_index=0,audio_module=0,duration_ticks=0,canonical_location=record['location'],
      source_words=len(p['raw_text'].split()),source_characters=len(p['raw_text']),source_utf8_bytes=len(p['raw_text'].encode()),canonical_speech_unit=allunits[unit['line_id']] if unit else None,
      binding=predicate,delivery='silent_text',mouth_gate='no_actor_mouth',document_kind='variant_record' if variant_id else 'record')
    if unit and segment['speaker_id'] not in util.talk.PROFILES:
     p.update(delivery='canonical_speech_caption_only_no_approved_profile',role='canonical_speech_without_profile',audio_gap='No approved procedural profile for this canonical speaker; no substituted voice')
    if unit and segment['speaker_id'] in util.talk.PROFILES:
     noun=len(voices)+1;fragment=segment['line_id']+('.'+variant_id if variant_id else '')+f'.page{part+1:02d}'
     plan=util.talk.schedule(fragment,segment['speaker_id'],p['raw_text']);frozen=frozen_principals[fragment]
     assert (frozen['voice_index'],frozen['speaker_id'],frozen['raw_text'])==(noun,segment['speaker_id'],p['raw_text'])
     audio=(HERE/'inputs/gap-v0/generated/speech'/frozen['audio_file']).read_bytes();sync=(HERE/'inputs/gap-v0/generated/speech'/frozen['sync_file']).read_bytes()
     assert sha(audio)==frozen['audio_sha256'] and sha(sync)==frozen['sync_sha256'] and sync==util.talk.sync_patch(plan)
     if render_principals:assert util.talk.render(plan)==audio
     filename=util.talk.patch_name(MODULE,noun)
     (out/'speech'/filename).write_bytes(audio);(out/'speech'/('#'+filename[1:])).write_bytes(sync)
     v={k:p[k] for k in ['record_id','line_id','variant_id','speaker_id','raw_text','raw_text_sha256','part','part_count','source_char_range','source_utf8_byte_range']}
     v.update(fragment_id=fragment,voice_index=noun,audio36=dict(module=MODULE,noun=noun,verb=1,cond=0,seq=1),audio_file=filename,sync_file='#'+filename[1:],audio_sha256=sha(audio),sync_sha256=sha(sync),
       duration_ticks=plan['duration_ticks'],mouth_events=plan['mouth_events'],generation='unchanged_approved_local_original_procedural_renderer',profile_sha256=profile_hash,renderer_sha256=renderer_hash,
       canonical_speech_unit=allunits[unit['line_id']],binding=predicate,laugh_opportunity=unit.get('laugh_opportunity'),audible_gate='host_proves_actual_audible_presence_and_current_pa_context',mouth_gate='host_proves_actual_visible_speaker')
     voices.append(v);p.update(voice_index=noun,audio_module=MODULE,duration_ticks=v['duration_ticks'],delivery='principal',mouth_gate=v['mouth_gate'])
    p['fields']=[p['entry'],document,part,len(group),p['speaker_number'],p['voice_index'],header,p['bytes_with_nul']]
    p.update(record_page=len(pages)-first,document_page=len(pages)-first,page_index=len(pages));pages.append(p)
  return dict(record_id=rid,variant_id=variant_id,local_line_key=local,global_line_key=document,document_id=document,document_kind='variant_record' if variant_id else 'record',dispatch='scene',first_page=first,
    page_count=len(pages)-first,page_indices=list(range(first,len(pages))),kind=record['kind'],source_ref=record['source_ref'],trigger=record['trigger'],source_obligations=record['source_obligations'],
    canonical_provenance=cat[rid],canonical_location=record['location'],source_text=record['text'],source_text_json_sha256=record['text_sha256'],segments=segments,canonical_units=[u['line_id'] for u in record_units],predicate=predicate,binding_required=rid in dynamic_records and not variant_id,source_template=cat[rid]['text'] if rid in dynamic_records else None)
 for rid,r in records.items():routes.append(export_record(r,[u for u in units if u['record_id']==rid],1399+adapter['line_ids'][rid],adapter['line_ids'][rid],emit=rid not in dynamic_records))
 base_record_pages=len(pages)
 unit_routes=[];vunits=[]
 def export_unit(u,record,document,variant=None):
  first=len(pages);originals=[pages[i] for i in record['page_indices'] if pages[i]['line_id']==u['line_id']]
  assert originals or record['binding_required']
  for index,original in enumerate(originals):
   p=deepcopy(original);p.update(document_id=document,global_line_key=document,document_page=index,document_kind='variant_unit' if variant else 'speech_unit',source_record_page_index=original['page_index'],page_index=len(pages));p['fields'][1]=document;pages.append(p)
  return dict(record_id=u['record_id'],line_id=u['line_id'],speech_unit_id=adapter['speech_unit_ids'].get(u['line_id'],0),variant_id=variant,
    local_line_key=record['local_line_key'],document_id=document,global_line_key=document,document_kind='variant_unit' if variant else 'speech_unit',dispatch='scene',first_page=first,page_count=len(pages)-first,
    page_indices=list(range(first,len(pages))),source_record_document=record['document_id'],source_record_pages=[p['record_page'] for p in originals],canonical_speech_unit=allunits[u['line_id']],source_text=u['text'],source_text_sha256=sha(u['text'].encode()),binding_required=record['binding_required'],predicate=record['predicate'],source_template=allunits[u['line_id']]['text'] if u['record_id'] in dynamic_records else None)
 by_id={r['record_id']:r for r in routes}
 for u in units:unit_routes.append(export_unit(u,by_id[u['record_id']],1429+adapter['speech_unit_ids'][u['line_id']]))
 for i,(r,us,variant,predicate) in enumerate(variants):vroutes.append(export_record(r,us,1466+i,adapter['line_ids'][r['id']],variant,predicate))
 for i,((r,us,variant,predicate),route) in enumerate(zip(variants,vroutes)):vunits.append(export_unit(us[0],route,1478+i,variant))

 # Integrate the separately authored frozen group component only after principal
 # numbering is complete. Every canonical/group identity is checked before reuse.
 assert len(voices)==39 and [v['voice_index'] for v in voices]==list(range(1,40))
 for row in audience_manifest['speech']:
  selected=[p for p in pages if (p['line_id'],p['variant_id'])==(row['line_id'],row['variant_id'])]
  assert len(selected)==2 and {p['document_kind'] for p in selected} in ({'record','speech_unit'},{'variant_record','variant_unit'})
  plan=audience.schedule(row['fragment_id'],'audience',row['raw_text'])
  assert row['voice_index'] in range(40,47) and row['audio36']==dict(module=924,noun=row['voice_index'],verb=1,cond=0,seq=1)
  assert row['audio_file']==audience.patch_name(**{'module':924,'noun':row['voice_index']})
  assert plan['duration_ticks']==row['duration_ticks'] and plan['mouth_events']==row['mouth_events'] and plan['runtime_speaker_number']==0
  for kind in ('audio','sync'):
   raw=(audience_root/'generated/speech'/row[kind+'_file']).read_bytes();assert sha(raw)==row[kind+'_sha256'];(out/'speech'/row[kind+'_file']).write_bytes(raw)
  v=deepcopy(row);v.update(profile_sha256=audience_manifest['profile_sha256'],renderer_sha256=audience_manifest['renderer_sha256'],generation='new_original_group_component_pending_independent_review',audible_gate='future_host_proves_actual_current_audience_eligibility_and_pa_cue_context',mouth_gate='no_principal_or_group_mouth')
  voices.append(v)
  for p in selected:
   for key in ['record_id','line_id','variant_id','speaker_id','raw_text','raw_text_sha256','source_char_range','source_utf8_byte_range','word_range','part','part_count','binding','canonical_speech_unit']:assert p[key]==row[key],key
   assert p['speaker_number']==0 and p['voice_index']==0
   p.update(voice_index=row['voice_index'],audio_module=924,duration_ticks=row['duration_ticks'],delivery='original_procedural_group_voice',role='canonical_speech',mouth_gate='no_principal_or_group_mouth');p.pop('audio_gap',None);p['fields'][5]=row['voice_index']
 assert [v['voice_index'] for v in voices]==list(range(1,47))

 by_unit={u['line_id']:u for u in unit_routes}
 record_receipts={r['record_id']:dict(record_id=r['record_id'],record_number=r['local_line_key'],document_id=r['document_id'],pages=[[r['document_id'],n] for n in range(r['page_count'])],
   binding_required=r['binding_required'],canonical_tokens=list(model.RECORD_UNITS[r['record_id']] or (r['record_id'],)),units=[dict(line_id=u,speech_unit_id=adapter['speech_unit_ids'][u],record_pages=by_unit[u]['source_record_pages'],last_record_page=by_unit[u]['source_record_pages'][-1] if by_unit[u]['source_record_pages'] else None,unit_document=by_unit[u]['document_id']) for u in r['canonical_units']]) for r in routes}
 unit_receipts={u['line_id']:dict(line_id=u['line_id'],record_id=u['record_id'],speech_unit_id=u['speech_unit_id'],document_id=u['document_id'],pages=[[u['document_id'],n] for n in range(u['page_count'])],record_pages=[[u['source_record_document'],n] for n in u['source_record_pages']],binding_required=u['binding_required'],source_text_sha256=u['source_text_sha256']) for u in unit_routes}
 source_receipts={s:dict(source_number=adapter['sources'][s],record_ids=[rid],documents=[by_id[rid]['document_id']],binding_required=by_id[rid]['binding_required'],canonical_tokens=[t['token'] for t in adapter['receipts'][s]],token_numbers=[adapter['tokens'][t['token']] for t in adapter['receipts'][s]]) for s,rid in adapter['source_bindings'].items()}
 payload=b'\0'.join(bank)+b'\0';assert len(payload)<32768;(out/f'{TEXT_RESOURCE}.text.bin').write_bytes(payload)
 offsets=[];pos=0
 for b in bank:offsets.append(pos);pos+=len(b)+1
 for p in pages:p.update(text_bank_byte_range=[offsets[p['entry']],offsets[p['entry']]+p['bytes_with_nul']],display_ascii_sha256=sha(bank[p['entry']]))
 docs=[{k:r[k] for k in ['document_id','record_id','variant_id','document_kind','first_page','page_count','page_indices']}|({k:r[k] for k in ['line_id','speech_unit_id']} if 'line_id' in r else {}) for r in routes+unit_routes+vroutes+vunits if r['page_count']]
 assert [r['document_id'] for r in docs]==[d for d in range(1400,1490) if d not in (1407,1408,1437,1438)]
 assert not any('{' in p['text'] or '}' in p['text'] or '{' in p['raw_text'] or '}' in p['raw_text'] for p in pages)
 host=dict(domain_script=994,domain_standalone_species=1,domain_production_reserved_species=16,scene_script=982,scene_species=4,
   record_document='Exact p12Line keys 1..30; all 29 P12 records plus VC03.NEED_RESOLUTION; two dynamic records require explicit observed-order variant selection',unit_document='Exact p12Unit keys 1..36; each complete unit has an independent route',
   acknowledge=signatures['p12Acknowledge'],method_bindings=signatures,
   dynamic_binding='p12VisibleWord(0), (1), (2) supply the observed left-to-right word IDs. Snapshot the exact current source/start/epoch and physical rack projection. Select one of six explicit variants for each dynamic record/unit. Template route IDs are reserved and non-displayable. No fallback, inferred desired order, or literal placeholder.',
   presentation='Existing sdOpen/sdDraw/Graph12/sdPresented/sdSpeak only; no new selector or API.',
   lease='Exact source/start/epoch plus complete visible page evidence; retire on close, travel, apron, menu, restore or replacement.',
   presence='Future host must prove current source eligibility, actual actor presence and current PA/cue context for every presentation and resume. A speaker ID or canonical location is never that proof.',
   introduction='The complete introduction is required before readiness. Confetti, cleanup, and collection are separate later transitions and need their own required evidence.',
   audience='New original group timbre uses canonical speaker_id audience, runtime speaker0, closed-mouth Sync only, and Voice volume/mute. Audience controls retain laughter semantics. Actual current audience eligibility remains a future host requirement. No native/listening or pre-existing acceptance claim.',
   silence='Printed evidence, choices, labels, hints and reader records with no speech units have no voice or mouth activity.',generic_codes='Unbound status codes remain unbound; no invented fallback text.')
 manifest=dict(schema=1,scope='New editable P12 scene/procedural audio implementation; no native or recovered exporter claim.',catalog_sha256=CATALOG_SHA,speech_sha256=SPEECH_SHA,gdd_sha256=GDD_SHA,
   protected_inputs_sha256=protected,text_resource=TEXT_RESOURCE,text_resource_sha256=sha(payload),text_bytes=len(payload),entries=len(bank),max_body_bytes=max(p['bytes_with_nul'] for p in pages),audio_modules=[MODULE],profile_sha256=profile_hash,renderer_sha256=renderer_hash,
   geometry=dict(columns=50,body_lines=3,font=util.font_metrics(),body=[6,158,314,182],header=[6,147,210,155],header_separate=True),speaker_numbers=util.SPEAKERS,
   line_keys={r['record_id']:r['document_id'] for r in routes},local_line_keys=adapter['line_ids'],local_unit_keys=adapter['speech_unit_ids'],unit_documents={r['line_id']:r['document_id'] for r in unit_routes},
   canonical_speech_units=units,routes=routes,unit_routes=unit_routes,variant_routes=vroutes,variant_unit_routes=vunits,document_routes=docs,dynamic_records=sorted(dynamic_records),reserved_template_documents=[1407,1408,1437,1438],pages=pages,speech=voices,missing_speech=[],audience_component=dict(archive_sha256='78d0a6bd6be42d0a96dcb731da3b8c61b1d46b9151ee8e1b23c0074f235fcfaf',manifest_sha256=sha((audience_root/'generated/manifest.json').read_bytes()),renderer_sha256=audience_manifest['renderer_sha256'],profile_sha256=audience_manifest['profile_sha256'],status='NEW_ORIGINAL_PENDING_INDEPENDENT_REVIEW',speaker_number=0,voice_lane=1,volume_and_mute='Voice',audience_control='Laughter only',principal_pairs_reused_exactly=39),source_bindings=adapter['source_bindings'],
   record_receipts=record_receipts,unit_receipts=unit_receipts,source_receipts=source_receipts,silent_readers={s:r for s,r in source_receipts.items() if not model.RECORD_UNITS[adapter['source_bindings'][s]]},host_api=host,
   receipt_semantics=dict(full_record_requires_all_pages=True,unit_requires_all_unit_pages=True,queue_open_last_page_audio_completion_are_not_display_receipts=True,full_source_and_unit_authority_distinct=True,variant_identity_required=True,partial_selected_unit_never_complete=True),
   ownership_contract=dict(peg_owner='P04',original_display=42,original_cart=72,original_controls=adapter['own_objects'],p14='All four actual contest wins remain required. VC03 resolution is distinct from an actual win; no signature or reveal consent supplied.'),
   coverage=dict(authority_records=len(records),canonical_speech_units=len(units),record_documents=len(routes),unit_documents=len(unit_routes),variant_record_documents=len(vroutes),variant_unit_documents=len(vunits),routable_documents=len(docs),record_pages=base_record_pages,unit_pages=sum(r['page_count'] for r in unit_routes),variant_record_pages=sum(r['page_count'] for r in vroutes),variant_unit_pages=sum(r['page_count'] for r in vunits),pages=len(pages),voiced_fragments=len(voices),caption_only_pages=sum(not p['voice_index'] for p in pages),source_words=sum(s['source_words'] for r in routes for s in r['segments']),source_characters=sum(s['source_characters'] for r in routes for s in r['segments'])),
   explicit_gaps=['New Audience audio pending independent component and combined review; no native/listening proof','No production species16 or native host activation','No native pixels, actual actors, audio listening, controller or SaveGame/RestoreGame proof','Future source receipts, actor/PA context, host ownership and native save/audio presentation remain separate'])
 dump(out/'manifest.json',manifest)
 for name,value in [('line-document-map',{r['record_id']:{k:r[k] for k in ['local_line_key','document_id','page_count','binding_required']} for r in routes}),('unit-document-map',{r['line_id']:{k:r[k] for k in ['speech_unit_id','document_id','page_count','source_record_document','source_record_pages','binding_required']} for r in unit_routes}),('binding-variant-map',dict(records=vroutes,units=vunits,templates=[r for r in routes if r['binding_required']],query='p12VisibleWord',indices=[0,1,2],no_fallback=True)),('receipt-map',{k:manifest[k] for k in ['record_receipts','unit_receipts','source_receipts','receipt_semantics']}),('host-contract',host)]:dump(out/(name+'.json'),value)
 dump(HERE/'snapshot/canonical-records.json',dict(records=list(records.values())))
 dump(HERE/'snapshot/canonical-speech-units.json',dict(units=units))
 dump(HERE/'snapshot/domain-method-bindings.json',signatures)

 audience_routes=[r for r in routes+vroutes if r['page_count'] and r['segments'][0]['speaker_id']=='audience'];audience_rows=[]
 for noun,r in enumerate(audience_routes,40):
  selected=[pages[j] for j in r['page_indices']];assert len(selected)==1;p=selected[0]
  fragment=p['line_id']+('.'+p['variant_id'] if p['variant_id'] else '')+f".page{p['part']+1:02d}"
  audience_rows.append({k:p[k] for k in ['record_id','line_id','variant_id','speaker_id','raw_text','raw_text_sha256','source_char_range','source_utf8_byte_range','word_range','part','part_count','document_id','page_index','binding','canonical_speech_unit']}|dict(fragment_id=fragment,proposed_audio36=dict(module=924,noun=noun,verb=1,cond=0,seq=1),page_count=1,canonical_template=r['source_template'] or p['canonical_speech_unit']['text']))
 dump(HERE/'snapshot/audience-audio-handoff.json',dict(status='COORDINATION_ONLY_NOT_ACCEPTED_AUDIO',principal_audio_nouns=list(range(1,40)),proposed_audience_nouns=list(range(40,47)),rows=audience_rows,canonical_speech_sha256=manifest['speech_sha256'],principal_renderer_sha256=manifest['renderer_sha256'],principal_profiles_sha256=manifest['profile_sha256']))

 dump(HERE/'evidence/allocation-check.json',dict(status='PASS',text=TEXT_RESOURCE,audio_module=MODULE,documents=[1400,1489],reserved_template_documents=[1407,1408,1437,1438],new_selectors=[],typed_inventory='inputs/typed-resource-inventory.json'))
 print(json.dumps(manifest['coverage'],indent=2));return manifest
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--render-principals',action='store_true',help='Optional intentional full principal rerender against frozen identities; normal rebuild reuses exact validated PCM');generate(parser.parse_args().render_principals)
