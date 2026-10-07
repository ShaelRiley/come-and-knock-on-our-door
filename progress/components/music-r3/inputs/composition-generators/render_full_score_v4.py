#!/usr/bin/env python3
"""Offline fixed-SoundFont rendering/profiling of accepted-direction candidates."""
import json,copy,sys
from pathlib import Path
import render_score as engine
import score_v4_core as c
OUT=c.OUT;engine.OUT=OUT

def main():
 full=sorted([json.loads(p.read_text())for p in(OUT/'analysis').glob('*-manifest.json')],key=lambda r:r['resource_id']);profiles=[]
 for m in full:
  for volume in(161,255):
   r=engine.render(m,volume,write=volume==161);profiles.append(r);print(json.dumps(r),flush=True)
 reduced=json.loads((OUT/'analysis/reduced-variants.json').read_text())['variants']
 for q in reduced:
  base=next(m for m in full if m['cue_id']==q['cue_id']);m=copy.deepcopy(base);m['cue_id']+='__REDUCED';m['native_payload_path']=q['native_payload_path'];r=engine.render(m,255,write=False);profiles.append(r);print(json.dumps(r),flush=True)
 result={'status':'OFFLINE_COMPONENT_ONLY_NOT_NATIVE_OR_PERCEPTUAL_ACCEPTANCE','full_candidates':len(full),'reduced_companions':len(reduced),'profiles':profiles,'sample_rate':44100,'fluid_synth':'2.4.4','soundfont':'FluidR3_GM.sf2','soundfont_sha256':engine.p.sha(engine.p.SOUNDFONT),'library_sha256':engine.p.sha(engine.p.LIBRARY),'settings':'Documented SCI volume/controller model at161 and255, whole-Sound100; exact native musical streams,4ms callback model. No loudness normalization or user settings changed.','limits':['Native physical-channel allocation, CC11 remap/restore, role ramps/tail clearing, actual PCM overlap and Steam Deck listening remain separate gates','Only V3short musical direction was approved by the user; these full cues are not individually accepted','Complete preview WAVs include6seconds release after scored duration']}
 (OUT/'analysis/render-validation.json').write_text(json.dumps(result,indent=2))
 print('TOTAL_PROFILES',len(profiles),'CLIPPED',sum(r['samples_at_or_above_full_scale']for r in profiles),'MAX_SAMPLE_VOICES',max(r['max_active_fluid_voices']for r in profiles),flush=True)
if __name__=='__main__':main()
