"""Complete source, immutable typed namespace and deterministic PCM/Sync verification."""
from pathlib import Path
import json,wave,struct,sys,zipfile
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
import generate
from guard import input_check,require,sha

def verify():
 input_check();m=json.loads((H/'generated/manifest.json').read_text());bank=(H/'generated/212.text.bin').read_bytes();entries=bank.split(b'\0')[:-1]
 require(m['coverage']==dict(authority_records=26,canonical_speech_units=36,record_documents=26,unit_documents=36,variant_record_documents=4,variant_unit_documents=8,routable_documents=74,record_pages=45,unit_pages=36,variant_record_pages=11,variant_unit_pages=11,pages=103,voiced_fragments=47,caption_only_pages=9,source_words=532,source_characters=2828),'Exact coverage')
 cat={r['id']:r for r in json.loads((H/'inputs/authority/full-line-catalog.json').read_text())['records']};units={u['line_id']:u for u in json.loads((H/'inputs/authority/speech-units.json').read_text())['units']}
 for path,digest in m['protected_inputs_sha256'].items():require(sha(H/path)==digest,'Protected input '+path)
 for r in m['routes']+m['variant_routes']:
  c=cat[r['record_id']];selected=next(v['text'] for v in c['finite_variants'] if v['variant_id']==r['variant_id']) if r['variant_id'] else c['text']
  require(r['source_text']==selected and r['source_obligations']==c['source_obligations'],'Record preservation')
  rebuilt=[]
  for i,s in enumerate(r['segments']):
   rows=[m['pages'][j] for j in r['page_indices'] if m['pages'][j]['segment_index']==i];raw=''.join(p['raw_text'] for p in rows)
   require(raw==s['source_text'],'Complete span')
   pointed=c
   for part in s['source_pointer'].strip('/').split('/'):
    pointed=pointed[int(part)] if isinstance(pointed,list) else pointed[part]
   require(pointed==raw,'Canonical source JSON pointer')
   start=byte=word=0
   for p in rows:
    require((p['source_char_range'][0],p['source_utf8_byte_range'][0],p['word_range'][0])==(start,byte,word),'Contiguous ranges')
    start,byte,word=p['source_char_range'][1],p['source_utf8_byte_range'][1],p['word_range'][1]
    require(raw[slice(*p['source_char_range'])]==p['raw_text'] and raw.encode()[slice(*p['source_utf8_byte_range'])].decode()==p['raw_text'],'Exact raw slices')
   require((start,byte,word)==(len(raw),len(raw.encode()),len(raw.split())),'Full ranges')
   if s['line_id']:
    u=units[s['line_id']];chosen=next(v['text'] for v in u['finite_variants'] if v['variant_id']==r['variant_id']) if r['variant_id'] and 'finite_variants' in u else u['text']
    require((raw,s['speaker_id'],s['source_speaker'])==(chosen,u['speaker_id'],u['speaker']),'Canonical speaker/unit')
   else:require(all((p['voice_index'],p['audio_module'],p['duration_ticks'])==(0,0,0) for p in rows),'Silence')
   rebuilt.append({'speaker':s['source_speaker'],'text':raw})
  require((rebuilt if isinstance(selected,list) else rebuilt[0]['text'])==selected,'Source reconstruction')
 for r in m['unit_routes']+m['variant_unit_routes']:require(''.join(m['pages'][i]['raw_text'] for i in r['page_indices'])==r['source_text'],'Exact selected unit')
 for p in m['pages']:
  require(bank[slice(*p['text_bank_byte_range'])]==p['text'].encode()+b'\0','Text span');require(len(p['text'].splitlines())<=3 and max(map(len,p['text'].splitlines()))<=50 and p['bytes_with_nul']<=153,'Caption geometry')
  require(p['source_utf8_bytes']==len(p['raw_text'].encode()),'UTF8 bytes');require(entries[p['header_entry']].decode()==generate.norm(p['display_name']),'Header identity')
 names=set();frames=0
 for v in m['speech']:
  plan=generate.util.talk.schedule(v['fragment_id'],v['speaker_id'],v['raw_text']);audio=H/'generated/speech'/v['audio_file'];sync=H/'generated/speech'/v['sync_file'];names|={audio.name,sync.name}
  require(sha(audio)==v['audio_sha256'] and sha(sync)==v['sync_sha256'],'Voice hash')
  require(audio.read_bytes()==generate.util.talk.render(plan) and sync.read_bytes()==generate.util.talk.sync_patch(plan),'Exact complete second render')
  require(v['mouth_events']==plan['mouth_events'] and plan['mouth_events'][-1]=={'tick':v['duration_ticks'],'pose':0},'Mouth closure')
  raw=sync.read_bytes();require(raw[:2]==b'\x8e\x00' and raw[-2:]==b'\xff\xff','Sync framing');rows=list(struct.iter_unpack('<hh',raw[2:-2]));require(rows[-1]==(v['duration_ticks'],0) and [r[0] for r in rows]==sorted(r[0] for r in rows) and all(p in (0,1,2) for t,p in rows),'Independent Sync parse')
  with wave.open(str(audio)) as w:require((w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes())==(1,2,22050,round(v['duration_ticks']*22050/60)),'PCM format duration');frames+=w.getnframes()
 require(names=={p.name for p in (H/'generated/speech').iterdir()},'Speech inventory')
 old=json.loads((H/'inputs/p08/inputs/baseline-GAME-MANIFEST.json').read_text());anchors={Path(p).name for p in old['files'] if Path(p).name.startswith(('@','#'))}
 actual={p.name for d in ['p08/generated/speech','p09-speech','p10-speech'] for p in (H/'inputs'/d).iterdir()}
 require(len(anchors)==946 and len(actual)==162 and not anchors&actual and not names&(anchors|actual),'Preserved audio namespace')
 typed=json.loads((H/'inputs/typed-resource-inventory.json').read_text());require(not any(r['type']==3 and r['number']==212 for r in typed['typed']),'Text212 collision');require(not set(range(1300,1374))&set(typed['documents']['occupied']),'Document collision')
 report=dict(status='PASS_SOURCE_DATA_AUDIO',coverage=m['coverage'],voice_fragments=len(m['speech']),second_render_all_fragments=True,pcm_frames=frames,prior_speech_filename_reservations=1108,prior_speech_files_rewritten=0,previous_pcm_sync_files_frozen=162,older_pcm_sync_identity_anchors=946,text_sha256=sha(H/'generated/212.text.bin'),text_bytes=len(bank),new_current_authority_implementation=True,native_acceptance=False)
 (H/'evidence/data-audio-gate.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':verify()
