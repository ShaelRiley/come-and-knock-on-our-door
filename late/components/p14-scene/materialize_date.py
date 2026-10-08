"""Explicit selected-snapshot audio materialization, separate from native playback.

No default date and no fallback clip. Artifacts are eligible only for their exact
owner/date/source/epoch snapshot and their unchanged original Frankie profile.
"""
from pathlib import Path
import json,hashlib
from mapping import validate_date_snapshot,date_plan,digest,require,date_is_current
from caption_util import talk
H=Path(__file__).resolve().parent
AUDIO=927
def materialize(snapshot,destination):
 validate_date_snapshot(snapshot);plan=date_plan(snapshot);root=Path(destination);root.mkdir(parents=True,exist_ok=True)
 require(not any(root.iterdir()),'New empty destination required')
 profile=hashlib.sha256((H/'inputs/p08/inputs/talk-prototype/profiles.json').read_bytes()).hexdigest();renderer=hashlib.sha256((H/'inputs/p08/inputs/talk-prototype/talk.py').read_bytes()).hexdigest();rows=[]
 for p in plan['pages']:
  fragment='P14.READ.001.01.selected.'+hashlib.sha256(plan['source_text'].encode()).hexdigest()+'.page'+str(p['page']+1)
  timing=talk.schedule(fragment,'frankie',p['raw_text']);audio=talk.render(timing);require(audio==talk.render(timing),'Procedural rerender identity');sync=talk.sync_patch(timing);name=talk.patch_name(AUDIO,p['page']+1)
  (root/name).write_bytes(audio);(root/('#'+name[1:])).write_bytes(sync)
  rows.append(dict(page=p['page'],raw_text=p['raw_text'],source_char_range=p['source_char_range'],source_utf8_byte_range=p['source_utf8_byte_range'],fragment_id=fragment,audio_file=name,sync_file='#'+name[1:],audio36=dict(module=AUDIO,noun=p['page']+1,verb=1,cond=0,seq=1),audio_sha256=hashlib.sha256(audio).hexdigest(),sync_sha256=hashlib.sha256(sync).hexdigest(),duration_ticks=timing['duration_ticks'],mouth_events=timing['mouth_events']))
 result=dict(scope='Selected-date procedural artifact; native playback integration unaccepted',snapshot=snapshot,snapshot_sha256=digest(snapshot),record_id='P14.READ.001',unit_id='P14.READ.001.01',speaker_id='frankie',source_text=plan['source_text'],source_text_sha256=hashlib.sha256(plan['source_text'].encode()).hexdigest(),profile_sha256=profile,renderer_sha256=renderer,rows=rows,double_render_exact=True,native_audio_acceptance=False,required_live_actor_and_pa_context=True)
 (root/'manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');return result

def eligible(artifact,plan,domain):
 return (type(artifact) is dict and artifact.get('snapshot')==plan.get('snapshot') and artifact.get('snapshot_sha256')==plan.get('snapshot_sha256') and artifact.get('source_text')==plan.get('source_text') and date_is_current(plan,domain))
