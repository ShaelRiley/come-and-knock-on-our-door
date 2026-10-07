"""Canonical source and complete regenerated PCM verification, no native runtime."""
from pathlib import Path
import json,hashlib,wave,io,sys
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
import generate
from guard import input_check,require,sha

def verify():
 input_check();m=json.loads((H/'generated/manifest.json').read_text());bank=(H/'generated/210.text.bin').read_bytes();entries=bank.split(b'\0')[:-1]
 require(m['coverage']['record_pages']==33 and m['coverage']['unit_pages']==20 and m['coverage']['caption_only_pages']==13,'Exact page coverage')
 cat={r['id']:r for r in json.loads((H/'inputs/authority/full-line-catalog.json').read_text())['records']};units={u['line_id']:u for u in json.loads((H/'inputs/authority/speech-units.json').read_text())['units']}
 for path,digest in m['protected_inputs_sha256'].items():require(sha(H/path)==digest,'Protected input '+path)
 words=chars=0
 for r in m['routes']:
  c=cat[r['record_id']];require(r['source_text']==c['text'] and r['source_obligations']==c['source_obligations'],'Record preservation')
  for i,s in enumerate(r['segments']):
   rows=[m['pages'][j] for j in r['page_indices'] if m['pages'][j]['segment_index']==i]
   raw=''.join(p['raw_text'] for p in rows);require(raw==s['source_text'],'Complete span');words+=len(raw.split());chars+=len(raw)
   if s['line_id']:require((raw,s['speaker_id'],s['source_speaker'])==(units[s['line_id']]['text'],units[s['line_id']]['speaker_id'],units[s['line_id']]['speaker']),'Speaker identity')
   else:require(all((p['voice_index'],p['audio_module'],p['duration_ticks'])==(0,0,0) for p in rows),'Silence')
 for p in m['pages']:
  require(bank[slice(*p['text_bank_byte_range'])]==p['text'].encode()+b'\0','Text span');require(len(p['text'].splitlines())<=3 and max(map(len,p['text'].splitlines()))<=50,'Caption geometry')
  require(p['source_utf8_bytes']==len(p['raw_text'].encode()),'UTF8 bytes')
  require(entries[p['header_entry']].decode()==generate.norm(p['display_name']),'Header identity')
 require((words,chars)==(371,2051),'Full source counts')
 names=set();frames=0
 for v in m['speech']:
  require(v['canonical_speech_unit']==units[v['line_id']] and v['laugh_opportunity']==units[v['line_id']]['laugh_opportunity'],'Unit and laugh metadata')
  plan=generate.util.talk.schedule(v['fragment_id'],v['speaker_id'],v['raw_text']);audio=H/'generated/speech'/v['audio_file'];sync=H/'generated/speech'/v['sync_file'];names|={audio.name,sync.name}
  require(sha(audio)==v['audio_sha256'] and sha(sync)==v['sync_sha256'],'Voice hash')
  require(audio.read_bytes()==generate.util.talk.render(plan) and sync.read_bytes()==generate.util.talk.sync_patch(plan),'Exact complete second render')
  require(v['mouth_events']==plan['mouth_events'] and plan['mouth_events'][-1]=={'tick':v['duration_ticks'],'pose':0},'Finite mouth events')
  with wave.open(str(audio)) as w:
   require((w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes())==(1,2,22050,round(v['duration_ticks']*22050/60)),'PCM format duration');frames+=w.getnframes()
 require(names=={p.name for p in (H/'generated/speech').iterdir()},'Exact speech inventory')
 old=json.loads((H/'inputs/p08/inputs/baseline-GAME-MANIFEST.json').read_text());prior={Path(p).name for p in old['files'] if Path(p).name.startswith(('@','#'))}|{p.name for p in (H/'inputs/p08/generated/speech').iterdir()}
 require(len(prior)==1028 and not names&prior,'Old PCM/Sync namespace preserved')
 anchors=json.loads((H/'historical/scene-data/PROVENANCE.json').read_text())['historical_missing_output_anchors'];text_anchor=next(a for a in anchors if a['path']=='generated/210.text.bin');matched=sha(H/'generated/210.text.bin')==text_anchor['sha256']
 report=dict(status='PASS_SOURCE_DATA_AUDIO',coverage=m['coverage'],voice_fragments=20,second_render_all_fragments=True,pcm_frames=frames,prior_speech_files=1028,prior_speech_files_rewritten=0,text_sha256=sha(H/'generated/210.text.bin'),text_bytes=len(bank),historical_text_anchor_sha256=text_anchor['sha256'],historical_text_anchor_matched=matched,historical_manifest_and_scene_source_identity_not_claimed=True,native_acceptance=False)
 (H/'evidence/data-audio-gate.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':verify()
