"""P14 canonical bank exporter. New code; no production-host/native claim."""
from pathlib import Path
from copy import deepcopy
import json,sys,argparse,re
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'inputs/model'))
from cakood import p14_model as model
import caption_util as old
from caption_layout import paginate,display,admit_date,sha
TEXT,AUDIO,FIRST=215,926,1600
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def generate(plan_only=False):
 if sys.flags.optimize:raise RuntimeError('Optimized Python forbidden')
 from guard import input_check
 input_check()
 for file,expected in [('full-line-catalog.json','3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c'),('speech-units.json','d143242b3d56f57331b0adfb73481425792c0757f57bc0c01a1b94561527c475'),('complete-body.md','18e2eb1a300cc1ac1192916441b640ca6134af619ee17eb424637b4dde28647c')]:
  assert sha((H/'inputs/authority'/file).read_bytes())==expected,'Authority pin '+file
 f=json.loads((H/'inputs/canonical-bindings.json').read_text());a=json.loads((H/'inputs/reference-schema.json').read_text())
 cat={r['id']:r for r in f['records']};units={u['line_id']:u for u in f['speech_units']}
 authority={r['id']:r for r in json.loads((H/'inputs/authority/full-line-catalog.json').read_text())['records']};speech={u['line_id']:u for u in json.loads((H/'inputs/authority/speech-units.json').read_text())['units']}
 assert all(authority[rid]==r for rid,r in cat.items()) and all(speech[uid]==u for uid,u in units.items())
 assert list(cat)==list(a['line_ids']) and list(units)==list(a['speech_unit_ids'])
 assert a['canonical_records']==cat and a['speech_metadata']==list(units.values())
 assert a['source_bindings']==f['source_bindings']==model.P14World.SOURCES
 assert {k:list(v) for k,v in model.RECORD_UNITS.items()}==f['record_units']
 assert len(a['credit_order'])==26 and len(a['asset_credits'])==33
 dynamic={r['id'] for r in cat.values() if r.get('dynamic_bindings')};assert dynamic=={'P14.READ.001','VC.NOTEBOOK.WINS','VC.GATE.MISSING_WINS'}
 out=H/'generated';out.mkdir(exist_ok=True);(out/'speech').mkdir(exist_ok=True)
 bank=[];entries={};pages=[];voices=[]
 def entry(text):
  raw=text.encode('ascii');assert b'|' not in raw and b'\0' not in raw
  if raw not in entries:entries[raw]=len(bank);bank.append(raw)
  return entries[raw]
 def record(r,document,variant=None,binding=None):
  rid=r['id'];us=[deepcopy(u) for u in units.values() if u['record_id']==rid]
  if binding:
   for u in us:u['text']=u['text'].format(**binding['values']);u['caption_text']=u['caption_text'].format(**binding['values'])
  segments=old.source_segments(r,us);first=len(pages);unbound=rid in dynamic and variant is None
  for si,segment in enumerate(segments):
   raw=segment['source_text'];group=[] if unbound else paginate(raw,preserve_case=r['kind']=='credit')
   header=entry(display(segment['source_speaker']));assert len(bank[header])*6<=204
   if binding:segment.update(source_template=cat[rid]['text'],binding=binding)
   u=next((u for u in us if u['line_id']==segment['line_id']),None)
   for part,p in enumerate(group):
    p.update(record_id=rid,document_id=document,line_id=segment['line_id'],speech_unit_id=a['speech_unit_ids'].get(segment['line_id'],0),local_line_key=a['line_ids'][rid],global_line_key=document,variant_id=variant,binding=binding,source_pointer=segment['source_pointer'],segment_index=si,source_text_sha256=sha(raw.encode()),part=part,part_count=len(group),last_of_unit=bool(u and part==len(group)-1),resource=TEXT,entry=entry(p['text']),header_entry=header,display_name=segment['source_speaker'],speaker_id=segment['speaker_id'],speaker_number=old.SPEAKERS.get(segment['speaker_id'],0),voice_index=0,audio_module=0,duration_ticks=0,role=segment['role'],canonical_speech_unit=units[u['line_id']] if u else None,delivery='silent_text',mouth_gate='no_actor_mouth',document_kind='variant_record' if variant else 'record')
    if u:
     assert u['speaker_id'] in old.talk.PROFILES,'No invented or substituted voice'
     noun=len(voices)+1;assert noun<=255
     fragment=u['line_id']+('.'+variant if variant else '')+f'.page{part+1:02d}'
     plan=old.talk.schedule(fragment,u['speaker_id'],p['raw_text']);audio=None if plan_only else old.talk.render(plan);sync=old.talk.sync_patch(plan);filename=old.talk.patch_name(AUDIO,noun)
     if audio is not None:(out/'speech'/filename).write_bytes(audio);(out/'speech'/('#'+filename[1:])).write_bytes(sync)
     voices.append(dict(fragment_id=fragment,voice_index=noun,line_id=u['line_id'],record_id=rid,canonical_speech_unit=units[u['line_id']],speaker_id=u['speaker_id'],raw_text=p['raw_text'],raw_text_sha256=p['raw_text_sha256'],source_char_range=p['source_char_range'],source_utf8_byte_range=p['source_utf8_byte_range'],audio36=dict(module=AUDIO,noun=noun,verb=1,cond=0,seq=1),audio_file=filename,sync_file='#'+filename[1:],audio_sha256=sha(audio) if audio else None,sync_sha256=sha(sync),duration_ticks=plan['duration_ticks'],mouth_events=plan['mouth_events'],profile_sha256=sha((H/'inputs/p08/inputs/talk-prototype/profiles.json').read_bytes()),renderer_sha256=sha((H/'inputs/p08/inputs/talk-prototype/talk.py').read_bytes()),generation='unchanged original procedural principal profile',binding=binding))
     p.update(voice_index=noun,audio_module=AUDIO,duration_ticks=plan['duration_ticks'],delivery='original_procedural_principal',mouth_gate='host_proves_actual_visible_speaker')
    p.update(record_page=len(pages)-first,document_page=len(pages)-first,page_index=len(pages));p['fields']=[p['entry'],document,part,len(group),p['speaker_number'],p['voice_index'],header,p['bytes_with_nul']];pages.append(p)
  return dict(record_id=rid,document_id=document,local_line_key=a['line_ids'][rid],variant_id=variant,binding=binding,binding_required=unbound,document_kind='variant_record' if variant else 'record',first_page=first,page_count=len(pages)-first,page_indices=list(range(first,len(pages))),kind=r['kind'],canonical_provenance=cat[rid],source_text=r['text'],segments=segments,canonical_units=[u['line_id'] for u in us],source_ref=r['source_ref'],source_obligations=r['source_obligations'])
 routes=[record(r,FIRST+a['line_ids'][r['id']]-1) for r in cat.values()];byid={r['record_id']:r for r in routes};uroutes=[]
 for uid,u in units.items():
  r=byid[u['record_id']];doc=FIRST+len(routes)+a['speech_unit_ids'][uid]-1;first=len(pages);originals=[pages[i] for i in r['page_indices'] if pages[i]['line_id']==uid]
  for i,p in enumerate(originals):
   q=deepcopy(p);q.update(document_id=doc,global_line_key=doc,document_kind='speech_unit',document_page=i,page_index=len(pages),source_record_page_index=p['page_index']);q['fields'][1]=doc;pages.append(q)
  uroutes.append(dict(record_id=u['record_id'],line_id=uid,speech_unit_id=a['speech_unit_ids'][uid],document_id=doc,document_kind='speech_unit',first_page=first,page_count=len(originals),page_indices=list(range(first,len(pages))),canonical_speech_unit=u,source_record_document=r['document_id'],source_record_pages=[p['record_page'] for p in originals],binding_required=r['binding_required'],variant_id=None,binding=None))
 variants=[]
 for mask in range(16):
  missing=[c for i,c in enumerate(a['contest_ids']) if not mask&(1<<i)];values={'won_count':4-len(missing),'missing_contest_names':', '.join(a['contest_names'][a['contest_ids'].index(c)] for c in missing)}
  for rid in ['VC.NOTEBOOK.WINS']+(['VC.GATE.MISSING_WINS'] if missing else []):
   selected=deepcopy(cat[rid]);selected['text']=selected['text'].format(**values);variant='wins_'+str(mask)
   variants.append(record(selected,1768+len(variants),variant,dict(kind='actual_retained_contest_win_mask',mask=mask,missing_contest_ids=missing,values=values,no_default=True)))
 assert len(variants)==31
 # Canonical date templates remain reserved. Runtime binding has separate slots.
 docs=[r for r in routes+uroutes+variants if r['page_count']]
 assert not any('{' in p['raw_text'] or '}' in p['raw_text'] for p in pages)
 payload=b'\0'.join(bank)+b'\0';assert len(payload)<32768;(out/f'{TEXT}.text.bin').write_bytes(payload)
 offsets=[];pos=0
 for b in bank:offsets.append(pos);pos+=len(b)+1
 for p in pages:p.update(text_bank_byte_range=[offsets[p['entry']],offsets[p['entry']]+p['bytes_with_nul']],display_ascii_sha256=sha(bank[p['entry']]))
 src_receipts={source:dict(source_number=a['sources'][source],record_id=rid,document_id=byid[rid]['document_id'],canonical_tokens=[v['token'] for v in a['receipts'][source]],token_numbers=[a['tokens'][v['token']] for v in a['receipts'][source]]) for source,rid in a['source_bindings'].items()}
 m=dict(schema=1,scope='New canonical P14 scene source candidate; not host, native or listening acceptance',catalog_sha256=f['catalog_sha256'],speech_sha256=f['speech_sha256'],gdd_sha256=f['gdd_sha256'],text_resource=TEXT,audio_modules=[AUDIO],text_bytes=len(payload),text_resource_sha256=sha(payload),routes=routes,unit_routes=uroutes,variant_routes=variants,document_routes=docs,pages=pages,speech=voices,audio_rendered=not plan_only,canonical_records=list(cat.values()),canonical_speech_units=list(units.values()),source_bindings=a['source_bindings'],source_receipts=src_receipts,credit_order=a['credit_order'],asset_credits=a['asset_credits'],dynamic_records=sorted(dynamic),reserved_template_documents=[r['document_id'] for r in routes+uroutes if r['binding_required']],runtime_date_documents=[1800,1801],geometry=dict(columns=50,body_lines=3,max_body_bytes=153,font0_preserved=old.font_metrics(),p14_font_resource=1,p14_font_metrics={'width':6,'height':8,'printable_ASCII':[32,126]},url_characters_and_case_preserved=True),coverage=dict(records=len(routes),units=len(uroutes),static_record_pages=sum(r['page_count'] for r in routes),static_unit_pages=sum(r['page_count'] for r in uroutes),notebook_variant_documents=len(variants),notebook_variant_pages=sum(r['page_count'] for r in variants),pages=len(pages),voices=len(voices),credits=59,mandatory_credits=26,conditional_credits=33),receipt_semantics=dict(source_unit_doc_page_identity_required=True,audio_never_grants_approval_consent_signature_pencil=True,selected_credit_source_proof_required=True,no_arbitrary_date_fallback=True),open_gates=['Production native date snapshot and audio materialization integration','Production host ownership','Native rendering, controller, audio/listening','Full campaign class-selector composition','Independent source acceptance'])
 dump(out/'manifest.json',m);dump(out/'receipt-map.json',dict(source_receipts=src_receipts,record_routes=routes,unit_routes=uroutes));print(json.dumps(m['coverage']));return m
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--plan-only',action='store_true');generate(p.parse_args().plan_only)
