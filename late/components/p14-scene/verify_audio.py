from pathlib import Path
import sys,json,hashlib,struct,wave
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from caption_util import talk
from guard import require
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((H/'generated/manifest.json').read_text());require(m['audio_rendered'],'Audio has not been rendered');names=set();frames=0
for v in m['speech']:
 p=talk.schedule(v['fragment_id'],v['speaker_id'],v['raw_text']);a=H/'generated/speech'/v['audio_file'];s=H/'generated/speech'/v['sync_file'];names|={a.name,s.name}
 require(sha(a)==v['audio_sha256'] and sha(s)==v['sync_sha256'],'Audio hash');require(a.read_bytes()==talk.render(p),'Repeated original render');require(s.read_bytes()==talk.sync_patch(p),'Exact Sync')
 require(v['mouth_events'][-1]=={'tick':v['duration_ticks'],'pose':0},'Closed final mouth')
 raw=s.read_bytes();require(raw[:2]==bytes((0x8e,0)) and raw[-2:]==bytes((255,255)),'Sync framing');pairs=list(struct.iter_unpack('<hh',raw[2:-2]));require(pairs[-1]==(v['duration_ticks'],0) and [x[0] for x in pairs]==sorted(x[0] for x in pairs),'Sync ticks')
 with wave.open(str(a)) as w:require((w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes())==(1,2,22050,round(v['duration_ticks']*22050/60)),'PCM format');frames+=w.getnframes()
require(names=={p.name for p in (H/'generated/speech').iterdir()},'Complete new speech inventory')
pred=H/'frozen-candidates/p13-scene-reconstruction';oldnames={p.name for p in pred.rglob('*') if p.is_file() and p.name.startswith(('@','#'))};anchors={Path(n).name for n in json.loads((pred/'inputs/p08/inputs/baseline-GAME-MANIFEST.json').read_text())['files'] if Path(n).name.startswith(('@','#'))};require(len(anchors)==946 and len(oldnames)==434 and not anchors&oldnames,'Prior audio reservation identity');require(not names&(oldnames|anchors),'Prior audio namespace collision')
old=json.loads((pred/'generated/manifest.json').read_text());retained=0
for v in old['speech']:
 for kind in ('audio','sync'):
  p=pred/'generated/speech'/v[kind+'_file'];require(sha(p)==v[kind+'_sha256'],'P13 audio changed');retained+=1
report=dict(status='PASS_STATIC_ORIGINAL_AUDIO',fragments=len(m['speech']),second_render_every_fragment_exact=True,pcm_frames=frames,prior_p13_files_hash_checked=retained,prior_audio_filenames_locally_reserved=len(oldnames),older_identity_anchors=len(anchors),total_prior_audio_filename_reservations=len(oldnames|anchors),new_names=len(names),pending_runtime_audio_unit='P14.READ.001.01',dynamic_date_materialization_separate=True,no_external_audio_used=True,native_acceptance=False,listening_acceptance=False)
(H/'evidence/audio-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
