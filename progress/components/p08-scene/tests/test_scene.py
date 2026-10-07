"""Source and freshly emitted SCI tests. Kernel mocks are not native acceptance."""
from pathlib import Path
import sys,json,re,copy,struct,io,wave,unittest
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H));sys.path.insert(0,str(H/'tools'));sys.path.insert(0,str(H/'tests'));sys.dont_write_bytecode=True
import generate
from generate import sha,norm,talk
from extend import ARRAYS,read_array
from source_tools import methods
from resource_codec import decode
from scene_vm import VM as SourceVM
from host import setup,frame,base
M=json.loads((H/'generated/manifest.json').read_text());TABLES=json.loads((H/'generated/static/manifest.json').read_text());EVIDENCE={};VMS=[]
PROPS=('sdEntry','sdLineKey','sdPart','sdPartCount','sdSpeaker','sdVoice','sdHeader','sdBytes','sdResource','sdAudioModule','sdVoiceEnd','sdFailure')
def source_setup():
 res={int(p.name.split('.')[0]):p.read_bytes().split(b'\0')[:-1] for p in (H/'inputs/resources').glob('*.text.bin')}
 for p in list((H/'generated').glob('*.text.bin'))+list((H/'generated/static').glob('*.text.bin')):res[int(p.name.split('.')[0])]=p.read_bytes().split(b'\0')[:-1]
 s=SourceVM(H/'generated/src/module982.sc','SceneDialogue',res);g=SourceVM(H/'generated/src/module985.sc','P05State',res);a=SourceVM(H/'generated/src/module981.sc','MusicTransport',res)
 for v in [s,g,a]:v.objects.update(script982=s,script985=g,script981=a)
 return s,g,a

def emitted():
 result=setup();result[0].vm.budget=100000000;VMS.append(result[0].vm);return result
class SceneTests(unittest.TestCase):
 def test_canonical_records_characters_words_speakers_and_units(self):
  catalog={r['id']:r for r in json.loads((H/'inputs/authority/full-line-catalog.json').read_text())['records']};units={u['line_id']:u for u in json.loads((H/'inputs/authority/speech-units.json').read_text())['units']}
  self.assertEqual(len(M['routes']),45);self.assertEqual([r['record_id'] for r in M['routes']],[r for r in catalog if r.startswith('P08.')]+['TRANSITION.P08.01'])
  self.assertEqual(M['canonical_records'],[r for r in catalog.values() if r['id'].startswith('P08.')]);self.assertEqual(M['canonical_transition_records'],[catalog['TRANSITION.P08.01']]);self.assertEqual(M['canonical_speech_units'],[u for u in units.values() if u['record_id'].startswith('P08.')]);self.assertEqual(M['canonical_transition_speech_units'],[u for u in units.values() if u['record_id']=='TRANSITION.P08.01'])
  found=set()
  for route in M['routes']:
   record=catalog[route['record_id']];self.assertEqual(route['source_text'],record['text']);self.assertEqual(route['source_obligations'],record['source_obligations']);self.assertEqual(route['source_ref'],record['source_ref'])
   for si,segment in enumerate(route['segments']):
    pages=[p for p in M['pages'] if p['record_id']==route['record_id'] and p['segment_index']==si];text=segment['source_text'];self.assertEqual(''.join(p['raw_text'] for p in pages),text);self.assertEqual(sha(text.encode()),segment['source_text_sha256']);last=(0,0,0)
    for p in pages:
     a,b=p['source_char_range'];x,y=p['source_utf8_byte_range'];c,d=p['word_range'];self.assertEqual((a,x,c),last);self.assertEqual(text[a:b],p['raw_text']);self.assertEqual(text.encode()[x:y].decode(),p['raw_text']);self.assertEqual(sha(p['raw_text'].encode()),p['raw_text_sha256']);self.assertEqual(' '.join(p['text'].split()),' '.join(norm(p['raw_text']).split()));last=b,y,d
    self.assertEqual(last,(len(text),len(text.encode()),len(re.findall(r'\S+',text))))
    if segment['line_id']:
     u=units[segment['line_id']];found.add(u['line_id']);self.assertEqual((text,segment['source_speaker'],segment['speaker_id']),(u['text'],u['speaker'],u['speaker_id']))
  self.assertEqual(found,{k for k in units if k.startswith(('P08.','TRANSITION.P08.01.'))});self.assertEqual(len(found),37)
  EVIDENCE['source_coverage']=dict(records=45,units=37,pages=len(M['pages']),all_characters_words_utf8_and_speakers_exact=True)
 def test_allocation_enum_identity_separate_transition_and_output_windows(self):
  self.assertEqual([r['document_id'] for r in M['routes']],list(range(973,1018)));self.assertEqual([r['global_line_key'] for r in M['routes']],list(range(729,774)))
  enums=json.loads((H/'inputs/p08-domain-manifest.json').read_text())
  for r in M['routes']:self.assertEqual(r['record'],enums['records'].get(r['record_id'],0))
  for u in M['unit_routes']:self.assertEqual(u['unit'],enums['units'].get(u['line_id'],0))
  transition=[r for r in M['routes'] if r['owner']=='transition'];self.assertEqual(len(transition),1);self.assertEqual(transition[0]['record_id'],'TRANSITION.P08.01');self.assertEqual(transition[0]['document_id'],1017)
  transition_units=[u for u in M['unit_routes'] if u['owner']=='transition'];self.assertEqual([u['transition_unit'] for u in transition_units],[1,2,3,4]);self.assertEqual({u['record'] for u in transition_units},{0});self.assertEqual({u['unit'] for u in transition_units},{0})
  mapping=json.loads((H/'generated/line-document-unit-map.json').read_text());self.assertEqual(len(mapping['output_windows']),45+37)
  for u in M['unit_routes']:
   matched=[p for p in M['pages'] if p['document_id']==u['document_id'] and u['first_record_page']<=p['record_page']<u['first_record_page']+u['page_count']]
   self.assertEqual(len(matched),u['page_count']);self.assertEqual({p['line_id'] for p in matched},{u['line_id']})
  self.assertEqual(len(M['canonical_records']),44);self.assertEqual(len(M['canonical_speech_units']),33);self.assertEqual(len(M['canonical_transition_speech_units']),4)
 def test_silent_controls_and_exact_eight_profiles(self):
  self.assertEqual(set(talk.PROFILES),set(generate.SPEAKERS));self.assertEqual(len(talk.PROFILES),8)
  canonical={u['line_id'] for u in json.loads((H/'inputs/authority/speech-units.json').read_text())['units']};voiced={v['line_id'] for v in M['speech']}
  self.assertEqual(len(voiced),37);self.assertTrue(voiced<=canonical)
  for p in M['pages']:
   if not p['line_id']:self.assertEqual((p['voice_index'],p['audio_module'],p['duration_ticks']),(0,0,0))
   if p['voice_index']:self.assertIn(p['line_id'],canonical);self.assertIn(p['speaker_id'],talk.PROFILES)
  for r in M['routes']:
   if r['kind'] in ['label','read','inventory','choice']:self.assertTrue(all(not p['voice_index'] for p in M['pages'] if p['record_id']==r['record_id']))
 def test_all_pcm_and_sync_reproduce_exactly(self):
  names=set();total_frames=0
  for v in M['speech']:
   plan=talk.schedule(v['fragment_id'],v['speaker_id'],v['raw_text']);audio=(H/'generated/speech'/v['audio_file']).read_bytes();sync=(H/'generated/speech'/v['sync_file']).read_bytes()
   self.assertEqual(audio,talk.render(plan));self.assertEqual(sync,talk.sync_patch(plan));self.assertEqual(sha(audio),v['audio_sha256']);self.assertEqual(sha(sync),v['sync_sha256']);self.assertEqual(plan['duration_ticks'],v['duration_ticks']);self.assertEqual(plan['mouth_events'],v['mouth_events'])
   with wave.open(io.BytesIO(audio),'rb') as w:
    self.assertEqual((w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getcomptype()),(1,2,22050,'NONE'));raw=w.readframes(w.getnframes());total_frames+=w.getnframes();samples=struct.unpack('<'+'h'*(len(raw)//2),raw);self.assertLess(min(samples),0);self.assertGreater(max(samples),0)
   self.assertEqual(sync[:2],b'\x8e\0');self.assertEqual(sync[-2:],b'\xff\xff');self.assertEqual(talk.patch_name(**v['audio36']),v['audio_file']);names.update([v['audio_file'],v['sync_file']])
  self.assertEqual(names,{p.name for p in (H/'generated/speech').iterdir()});self.assertEqual(len(names),82);EVIDENCE['audio']=dict(fragments=41,files=82,total_pcm_frames=total_frames,deterministic_second_render=True,external_voices=0)
 def test_all_old_tables_text_pcm_sync_and_unrelated_methods_preserved(self):
  before=(H/'inputs/src/module982.sc').read_text();after=(H/'generated/src/module982.sc').read_text()
  for name in ARRAYS:self.assertEqual(read_array(after,name)[:len(read_array(before,name))],read_array(before,name))
  inp=H/'inputs/native-game';out=H/'generated/fixture-game';a=decode((inp/'resource.map').read_bytes(),(inp/'resource.000').read_bytes());b=decode((out/'resource.map').read_bytes(),(out/'resource.000').read_bytes())
  for k,v in a.items():
   if k not in {(3,240),(3,241),(3,244),(2,982),(17,982),(2,985),(17,985)}:self.assertEqual(b[k],v)
  original=json.loads((H/'inputs/baseline-GAME-MANIFEST.json').read_text());names={n for n in original['files'] if n.startswith(('@','#'))};self.assertEqual(len(names),946)
  self.assertFalse(names.intersection(p.name for p in (H/'generated/speech').iterdir()))
  self.assertEqual({p.name for p in out.iterdir()},{'resource.map','resource.000','manifest.json'})
  changes=json.loads((H/'generated/extension-contract.json').read_text())['changed_methods']
  for path in (H/'generated/src').glob('*.sc'):
   old=methods((H/'inputs/src'/path.name).read_text());new=methods(path.read_text())
   for name in old:
    if name not in changes[path.name]:self.assertEqual(old[name],new[name])
 def test_source_and_emitted_every_new_page_and_invalid_bounds(self):
  src,guard,music=source_setup();h,d,a,p,q,r=emitted();count=0
  for route in M['routes']:
   self.assertEqual(src.call('sdOpen',route['document_id'],0,0,0,0),1);self.assertEqual(d.call('sdOpen',route['document_id'],0,0,0,a),1)
   for page in [p for p in M['pages'] if p['document_id']==route['document_id']]:
    src.p['sdPage']=page['record_page'];d.p['sdPage']=page['record_page'];self.assertEqual(src.call('sdLoad'),1);self.assertEqual(d.call('sdLoad'),1)
    self.assertEqual({k:src.p[k] for k in PROPS},{k:d.p[k] for k in PROPS});self.assertEqual(src.arrays['sdTextBuffer'],page['text']);self.assertEqual(str(d.arrays['sdTextBuffer']),page['text']);self.assertEqual(str(d.arrays['sdHeaderBuffer']),norm(page['display_name']));self.assertEqual(src.call('sdDraw',0),1);self.assertIn(page['text'],[x[-1] for x in src.paint if x[0]=='text']);count+=1
  oldgen=src.p['sdGeneration'];self.assertEqual(src.call('sdAfterRestore',0),1);self.assertGreater(src.p['sdGeneration'],oldgen);self.assertEqual(src.p['sdPendingStart'],0)
  for bad in [-32768,-1,0,1018,32767]:self.assertEqual(src.call('sdRoute',bad),-1);self.assertEqual(d.call('sdRoute',bad),-1);self.assertEqual(d.call('sdPageCount',bad),0)
  self.assertEqual(count,68);EVIDENCE['source_emitted_pages']=count
 def test_all1070_old_emitted_pages_and_p07_aliases_remain_exact(self):
  h,d,a,p,q,r=emitted();s=(H/'inputs/src/module982.sc').read_text();tables={n:read_array(s,n) for n in ARRAYS};seen=set()
  for doc,(start,count) in enumerate(zip(tables['sdStarts'],tables['sdCounts'])):
   if doc<1 or start<0 or count==0:continue
   self.assertEqual(d.call('sdOpen',doc,0,0,0,a),1)
   for page in range(count):
    d.p['sdPage']=page;self.assertEqual(d.call('sdLoad'),1);row=start+page;f=tables['sdPageData'][row*8:row*8+8];self.assertEqual([d.p[k] for k in PROPS[:8]],f);self.assertEqual(d.p['sdResource'],tables['sdTextResources'][row]);self.assertEqual(d.p['sdAudioModule'],tables['sdAudioModules'][row]);self.assertEqual(d.p['sdVoiceEnd'],tables['sdPageDurations'][row]);seen.add(row)
  for doc,start,count in [(971,1059,3),(972,1062,2)]:
   self.assertEqual(d.call('sdRoute',doc),start);self.assertEqual(d.call('sdPageCount',doc),count)
   self.assertEqual(d.call('sdOpen',doc,0,0,0,a),1)
   for page in range(count):
    d.p['sdPage']=page;self.assertEqual(d.call('sdLoad'),1);self.assertEqual([d.p[k] for k in PROPS[:8]],tables['sdPageData'][(start+page)*8:(start+page+1)*8])
  self.assertEqual(seen,set(range(1070)));EVIDENCE['old_emitted_pages']=len(seen)
 def test_every_new_page_actual_emitted_renderer_graph12_and_geometry(self):
  h,d,a,p,q,r=emitted();snap=[list(p.arrays[k]) for k in p.arrays];p05=list(r.arrays['p05Words']);qstate=copy.deepcopy(q.p);records=[]
  for route in M['routes']:
   self.assertEqual(h.call('dialogueOpen',route['document_id']),1)
   for page in [x for x in M['pages'] if x['document_id']==route['document_id']]:
    if page['record_page']:h.call('uiTurnPage',1)
    graphs=sum(n=='Graph' and args[0]==12 for n,args in h.vm.ktrace);paint=len(h.vm.paint);frame(h)
    self.assertGreater(sum(n=='Graph' and args[0]==12 for n,args in h.vm.ktrace),graphs);self.assertIn(page['text'],h.vm.paint[paint:]);self.assertIn(norm(page['display_name']),h.vm.paint[paint:]);self.assertEqual(d.p['sdPaintGeneration'],d.p['sdGeneration']);self.assertEqual(h.call('scenePageIdentity'),1);records.append([route['document_id'],page['record_page']])
  self.assertEqual(list(r.arrays['p05Words']),p05);self.assertEqual(q.p,qstate)
  self.assertEqual(len(records),68);self.assertTrue(h.vm.measurements);self.assertTrue(all(t['rect'][2]<=24 and t['rect'][3]<=308 for t in h.vm.measurements if t['width']==308));EVIDENCE['rendered_pages']=records;EVIDENCE['graph12_frames']=h.vm.frames
 def test_unpresented_failed_graph_and_audio_end_skip_never_acknowledge(self):
  h,d,a,p,q,r=emitted();h.call('dialogueOpen',973);generation=d.p['sdGeneration'];old=list(r.arrays['p05Words']);self.assertNotEqual(d.p['sdPaintGeneration'],generation);self.assertEqual(d.call('sdPresented',generation,0,a.p['token']),0)
  h.vm.draw_success=False
  with self.assertRaises(base.VMError):frame(h)
  self.assertEqual(list(r.arrays['p05Words']),old);self.assertEqual(a.p['played'],0);h.vm.draw_success=True
  h.call('speechCancel');self.assertEqual(list(r.arrays['p05Words']),old);h.vm.audio_position=-1;h.call('audioPoll');h.call('speechPoll');self.assertEqual(list(r.arrays['p05Words']),old)
  for flag in ['menuOpen','paused','opening']:
   h.p[flag]=1;h.call('dialoguePresented');self.assertEqual(list(r.arrays['p05Words']),old);h.p[flag]=0
  frame(h);self.assertEqual(list(r.arrays['p05Words']),old);EVIDENCE['knowledge_scope']='No new P08 host adapter is installed, and scene presentation alone grants no campaign knowledge'
 def test_current_actor_presence_remains_audible_gate(self):
  h,d,a,p,q,r=emitted();h.call('dialogueOpen',973);self.assertEqual(d.p['sdSpeaker'],1);self.assertEqual(h.call('dialogueCanSpeak',1),1);frame(h)
  self.assertTrue(any(n=='DoAudio' and args[:2]==(2,918) for n,args in h.vm.ktrace))
  h.p['motionPhase']=1;self.assertEqual(h.call('dialogueCanSpeak',1),0);h.p['motionPhase']=0;h.p['onApron']=1;self.assertEqual(h.call('dialogueCanSpeak',2),0)
  self.assertEqual(h.call('dialogueCanSpeak',6),0)
 def test_restore_each_document_clears_audio_and_stale_presentation(self):
  src,guard,music=source_setup();h,d,a,p,q,r=emitted();count=0
  for route in M['routes']:
   self.assertEqual(src.call('sdOpen',route['document_id'],0,0,0,0),1);src.p['sdPage']=route['page_count']-1;self.assertEqual(src.call('sdLoad'),1);sg=src.p['sdGeneration'];saved_source=copy.deepcopy(src.p);src.p=copy.deepcopy(saved_source);self.assertEqual(src.call('sdAfterRestore',0),1);self.assertGreater(src.p['sdGeneration'],sg);self.assertEqual((src.p['sdPendingStart'],src.p['sdArmed']),(0,0))
   self.assertEqual(d.call('sdOpen',route['document_id'],0,0,0,a),1);d.p['sdPage']=route['page_count']-1;self.assertEqual(d.call('sdLoad'),1);oldgen=d.p['sdGeneration'];saved=h.vm.snapshot();h.vm.restore(saved);self.assertEqual(d.call('sdAfterRestore',a),1)
   self.assertGreater(d.p['sdGeneration'],oldgen);self.assertEqual((d.p['sdPendingStart'],d.p['sdArmed'],a.p['lane'],a.p['pendingLaugh']),(0,0,0,0));self.assertEqual(d.call('sdPresented',oldgen,d.p['sdPage'],a.p['token']),0);count+=1
  self.assertEqual(count,45);EVIDENCE['restored_scene_documents']=count
 def test_every_static_family_and_extended_tail_matches_current_arrays(self):
  h,d,a,p,q,r=emitted();self.assertEqual(r.call('hStaticAll'),1);checked=[]
  for table in TABLES['tables']:
   array=h.vm.arrays(table['module'])[table['name']]
   self.assertEqual([x&65535 for x in array],table['values']);self.assertEqual(r.call('hStaticCount',table['id']),table['count'])
   for i in sorted({0,table['count']//2,table['count']-1}):self.assertEqual(r.call('hStaticRange',table['id'],i,1),1);checked.append([table['name'],i])
  self.assertEqual(len({p[0] for p in checked}),20);EVIDENCE['static_families_checked']=checked
 def test_static_resource_chunk_edges_exact_last_entries(self):
  h,d,a,p,q,r=emitted();chunks=[];transitions=[]
  for table in TABLES['tables']:
   for start in range(0,table['count'],20):
    values=table['values'][start:start+20];chunks.append((''.join(f'{v:05d} ' for v in values+[0]*(20-len(values)))).encode()+b'\0')
  self.assertGreater(len(chunks),960);self.assertLessEqual(len(chunks),1440)
  for row in TABLES['bank_map']:
   resource,first=row['resource'],row['first_chunk'];expected=b''.join(chunks[first:first+480]);actual=(H/f'generated/static/{resource}.text.bin').read_bytes();self.assertEqual(actual,expected);self.assertLess(len(actual),65536);self.assertTrue(all(len(c)==121 for c in chunks[first:first+480]))
  for chunk in [0,479,480,959,960,len(chunks)-1]:
   table=next(t for t in TABLES['tables'] if t['first_chunk']<=chunk<t['first_chunk']+(t['count']+19)//20);index=(chunk-table['first_chunk'])*20;self.assertEqual(r.call('hStaticLoad',table['id'],index),1)
   for slot,value in enumerate(table['values'][index:index+20]):self.assertEqual(r.call('hStaticValue',slot)&65535,value)
   transitions.append(dict(chunk=chunk,table=table['name'],index=index))
  EVIDENCE['static_bank_edges']=transitions;EVIDENCE['static_chunks']=len(chunks)
