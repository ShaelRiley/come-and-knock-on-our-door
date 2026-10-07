"""Exact P06/P07 text and deterministic procedural cast audio; no story authorship."""
from pathlib import Path
import sys,json,re,hashlib,struct,copy
H=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(H/'inputs/talk-prototype'))
import talk
SPEAKERS={'jack':1,'bunny':2,'frankie':3,'stringer':4,'milo':5,'vivian':6,'rita':7,'felix':8}
TRANSLATE=str.maketrans({'‘':"'",'’':"'",'“':'"','”':'"','–':'-','—':' - ','…':'...','●':'.'})
def require(ok,why):
 if not ok:raise RuntimeError(why)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(p,value):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def norm(text):
 value=text.translate(TRANSLATE).upper();value.encode('ascii');require('\0' not in value and '|' not in value,'Unsafe text');return value
def paginate(text):
 words=list(re.finditer(r'\S+',text));require(bool(words),'Empty source')
 lines=[];tokens=[];width=0;first=0
 for index,word in enumerate(words):
  token=norm(word.group());require(len(token)<=50,'Unbreakable word')
  source_break=index and '\n' in text[words[index-1].end():word.start()]
  if tokens and (source_break or width+1+len(token)>50):lines.append((first,index,' '.join(tokens)));tokens=[];width=0
  if not tokens:first=index
  tokens.append(token);width+=len(token)+(len(tokens)>1)
 if tokens:lines.append((first,len(words),' '.join(tokens)))
 pages=[]
 for line_start in range(0,len(lines),3):
  group=lines[line_start:line_start+3];first_word,last_word=group[0][0],group[-1][1]
  start=0 if not pages else words[first_word].start();end=words[last_word].start() if last_word<len(words) else len(text)
  raw=text[start:end];shown='\n'.join(line[2] for line in group)
  pages.append(dict(text=shown,raw_text=raw,word_range=[first_word,last_word],source_char_range=[start,end],source_utf8_byte_range=[len(text[:start].encode()),len(text[:end].encode())],raw_text_sha256=sha(raw.encode()),bytes_with_nul=len(shown.encode())+1))
 require(''.join(p['raw_text'] for p in pages)==text,'Source span mismatch')
 require(all(len(p['text'].splitlines())<=3 and max(map(len,p['text'].splitlines()))<=50 and p['bytes_with_nul']<=153 for p in pages),'Geometry overflow')
 return pages

def source_segments(record,units):
 def segment(pointer,text,speaker,speaker_id,line_id=None):
  role='cast_voice' if line_id is not None and speaker_id in SPEAKERS else 'printed_evidence' if record['kind']=='read' else 'interface_label' if record['kind']=='label' else 'choice_caption' if record['kind']=='choice' else 'cast_caption_only' if speaker_id in SPEAKERS else 'narration_control'
  return dict(source_pointer=pointer,source_text=text,source_text_sha256=sha(text.encode()),source_speaker=speaker,line_id=line_id,speaker_id=speaker_id,role=role)
 text=record['text']
 if isinstance(text,list):
  require(len(text)==len(units),'Multi-speaker unit count '+record['id']);result=[]
  for i,(line,u) in enumerate(zip(text,units)):
   require(u['text']==line['text'] and u['speaker']==line['speaker'],'Multi-speaker identity')
   result.append(segment(f'/text/{i}/text',line['text'],line['speaker'],u['speaker_id'],u['line_id']))
  return result
 if units:
  require(len(units)==1 and units[0]['text']==text,'Unit text identity '+record['id']);u=units[0]
  return [segment('/text',text,u['speaker'],u['speaker_id'],u['line_id'])]
 return [segment('/text',text,record['speaker'],record.get('speaker_id','text'))]

def generate():
 require(not sys.flags.optimize,'Optimized Python forbidden')
 catalog_file=H/'inputs/authority/full-line-catalog.json';speech_file=H/'inputs/authority/speech-units.json'
 require(sha(catalog_file.read_bytes())=='3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c','Catalog hash')
 require(sha(speech_file.read_bytes())=='d143242b3d56f57331b0adfb73481425792c0757f57bc0c01a1b94561527c475','Speech hash')
 catalog=json.loads(catalog_file.read_text());speech=json.loads(speech_file.read_text());enums=json.loads((H/'inputs/p08-domain-manifest.json').read_text())
 records=[r for r in catalog['records'] if r['id'].startswith('P08.')];transition=[r for r in catalog['records'] if r['id']=='TRANSITION.P08.01']
 units=[u for u in speech['units'] if u['record_id'].startswith('P08.')];transition_units=[u for u in speech['units'] if u['record_id']=='TRANSITION.P08.01']
 require(len(records)==44 and len(units)==33 and len(transition)==1 and len(transition_units)==4,'Authority membership')
 require(list(enums['records'])==[r['id'] for r in records] and list(enums['units'])==[u['line_id'] for u in units],'Exact domain enum order')
 require(set(talk.PROFILES)==set(SPEAKERS) and len(talk.PROFILES)==8,'Eight original cast profiles')
 out=H/'generated';(out/'speech').mkdir(parents=True,exist_ok=True)
 pages=[];voices=[];routes=[];unitmaps=[];bank=[];indices={}
 def entry(value):
  encoded=value.encode('ascii')
  if encoded not in indices:indices[encoded]=len(bank);bank.append(encoded)
  return indices[encoded]
 for i,r in enumerate(records+transition):
  is_transition=r['id']=='TRANSITION.P08.01';owner='transition' if is_transition else 'P08';record=enums['records'].get(r['id'],0)
  runits=[u for u in units+transition_units if u['record_id']==r['id']]
  require(sha(json.dumps(r['text'],ensure_ascii=False).encode())==r['text_sha256'],'Canonical text hash')
  doc=973+i;globalkey=729+i;segments=source_segments(r,runits);start=len(pages)
  for si,seg in enumerate(segments):
   split=paginate(seg['source_text']);header=norm(seg['source_speaker']);require(len(header)*6<=204,'Header overflow');hindex=entry(header);first_unit_page=len(pages)-start
   unit=enums['units'].get(seg['line_id'],0)
   for part,page in enumerate(split):
    page.update(puzzle='P08',owner=owner,record_id=r['id'],record=record,document_id=doc,local_line_key=i+1,global_line_key=globalkey,line_id=seg['line_id'],unit=unit,transition_unit=si+1 if is_transition else 0,source_pointer=seg['source_pointer'],segment_index=si,source_text_sha256=seg['source_text_sha256'],part=part,part_count=len(split),resource=208,entry=entry(page['text']),header_entry=hindex,display_name=seg['source_speaker'],speaker_id=seg['speaker_id'],speaker_number=SPEAKERS.get(seg['speaker_id'],0),role=seg['role'],voice_index=0,audio_module=0,duration_ticks=0,record_page=len(pages)-start,absolute_page=1070+len(pages))
    if seg['role']=='cast_voice':
     noun=len(voices)+1;require(noun<=255,'Audio noun exhaustion');fragment=f"{seg['line_id']}.page{part+1:02d}";plan=talk.schedule(fragment,seg['speaker_id'],page['raw_text']);audio=talk.render(plan);sync=talk.sync_patch(plan);name=talk.patch_name(918,noun)
     (out/'speech'/name).write_bytes(audio);(out/'speech'/('#'+name[1:])).write_bytes(sync)
     voice={k:page[k] for k in ('puzzle','owner','record_id','line_id','unit','transition_unit','speaker_id','speaker_number','raw_text','raw_text_sha256','source_pointer','source_char_range','source_utf8_byte_range','word_range','part','part_count')}
     voice.update(fragment_id=fragment,voice_index=noun,audio36=dict(module=918,noun=noun,verb=1,cond=0,seq=1),audio_file=name,sync_file='#'+name[1:],audio_sha256=sha(audio),sync_sha256=sha(sync),duration_ticks=plan['duration_ticks'],mouth_events=plan['mouth_events']);voices.append(voice);page.update(voice_index=noun,audio_module=918,duration_ticks=plan['duration_ticks'])
    page['fields']=[page['entry'],globalkey,part,len(split),page['speaker_number'],page['voice_index'],hindex,page['bytes_with_nul']];pages.append(page)
   unitmaps.append(dict(owner=owner,record_id=r['id'],record=record,line_id=seg['line_id'],unit=unit,transition_unit=si+1 if is_transition else 0,document_id=doc,global_line_key=globalkey,first_record_page=first_unit_page,page_count=len(split),absolute_page_start=1070+start+first_unit_page,source_pointer=seg['source_pointer'],silent=seg['role']!='cast_voice',aggregate_receipt_forbidden=len(segments)>1))
  count=len(pages)-start;require(1<=count<=64,'Document ceiling')
  routes.append(dict(owner=owner,puzzle='P08',record_id=r['id'],record=record,document_id=doc,local_line_key=i+1,global_line_key=globalkey,first_page=start,absolute_page_start=1070+start,page_count=count,source_text=r['text'],source_text_json_sha256=r['text_sha256'],source_ref=r['source_ref'],source_obligations=r['source_obligations'],kind=r['kind'],segments=segments))
 payload=b'\0'.join(bank)+b'\0';require(len(payload)<32768,'Text bank bound');(out/'208.text.bin').write_bytes(payload)
 require({p.name for p in (out/'speech').iterdir()}=={v[k] for v in voices for k in ('audio_file','sync_file')},'Unexpected speech file')
 font=(H/'inputs/resources/000.font.bin').read_bytes();count,height=struct.unpack_from('<HH',font,2);glyphs=[tuple(font[struct.unpack_from('<H',font,6+2*c)[0]:][:2]) for c in range(count)]
 require(count==128 and height==8 and set(glyphs)=={(6,8)},'Font metrics')
 manifest=dict(schema=1,kind='NEW RECONSTRUCTION; not recovered historical implementation',native_acceptance=False,editorial_revision=3,canonical_records=records,canonical_speech_units=units,canonical_transition_records=transition,canonical_transition_speech_units=transition_units,existing_pages=1070,added_pages=len(pages),total_pages=1070+len(pages),speaker_numbers=SPEAKERS,profile_sha256=sha((H/'inputs/talk-prototype/profiles.json').read_bytes()),renderer_sha256=sha((H/'inputs/talk-prototype/talk.py').read_bytes()),geometry=dict(columns=50,lines=3,font=0,buffer_bytes=153,font_sha256=sha(font),glyph_advance=6,glyph_height=8,body=[6,158,314,182],header=[6,147,210,155]),routes=routes,pages=pages,speech=voices,unit_routes=unitmaps,text_sha256=sha(payload),text_bytes=len(payload),source_barrier='Each actual source page requires successful unobscured render and Graph12 before current request/generation acknowledgement. Opening, metadata, audio completion and skip confer no receipt.',audible_eligibility='Current host actor/speaker presence controls eligibility.',scope_exclusions=['native screen/input/listening','P08 host actions','observation/ownership/readiness/E03 grants','campaign completion'])
 dump(out/'manifest.json',manifest)
 windows=[]
 for route in routes:
  windows.append(dict(kind='complete_record',owner=route['owner'],record_id=route['record_id'],record=route['record'],unit=0,document_id=route['document_id'],first_record_page=0,page_count=route['page_count'],requires_actual_per_page_receipts=True))
 for u in unitmaps:
  if u['line_id']:windows.append(dict(kind='unit_only',**u,requires_actual_per_page_receipts=True))
 dump(out/'line-document-unit-map.json',dict(routes=routes,units=unitmaps,output_windows=windows,transition_namespace='Separate from P08 domain records/units; record=unit=0, transition_unit=1..4',receipt_contract='A complete-record output may acknowledge only pages actually presented; a unit-only output uses its exact first_record_page/page_count window. Never promote a unit-only receipt to the aggregate record. Host integration owns actual Graph12 receipt delivery and request/generation validation.'))
 print(json.dumps(dict(records=44,units=33,transition_records=1,transition_units=4,pages=len(pages),voice_fragments=len(voices),silent_pages=sum(not p['voice_index'] for p in pages),text_bytes=len(payload))))
 return manifest
if __name__=='__main__':generate()
