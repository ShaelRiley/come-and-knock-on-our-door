#!/usr/bin/env python3
"""Build rights-traceable PCM candidates. No native or listening acceptance."""
from pathlib import Path
import json,hashlib,subprocess,wave,shutil
import numpy as np
from scipy.signal import butter,sosfiltfilt,resample_poly
R=Path(__file__).resolve().parent;B=R/'assets/recovered/CaKoOD-clean-laughter-24-source-candidates';F=R/'assets/recovered/Everyday-Foley-Developer-Bank-Spoilers/Everyday-Foley-Candidate-Bank';O=R/'assets/audio36';A=R/'assets/audition';A.mkdir(exist_ok=True)
base=R.parents[1]/'source/assets/audio'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decode(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar','22050','-f','f32le','-']),'<f4').astype(float)
def save(p,x):
 x=np.clip(x,-.89,.89);y=np.rint(x*32767).astype('<i2')
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(22050);w.writeframes(y.tobytes())
 return dict(file=str(p.relative_to(R)),sha256=sha(p),duration_seconds=round(len(x)/22050,6),peak_dbfs=round(20*np.log10(max(abs(x).max(),1e-10)),3),clipped_samples=int((abs(x)>=1).sum()))
def process(x,target=-24):
 x=x-np.mean(x);x=sosfiltfilt(butter(2,80,'highpass',fs=22050,output='sos'),x);x=sosfiltfilt(butter(4,6000,'lowpass',fs=22050,output='sos'),x)
 rms=np.sqrt(np.mean(x*x));gain=min(10**(target/20)/max(rms,1e-8),.65/max(abs(x).max(),1e-8));x*=gain
 n=min(441,len(x)//3);x[:n]*=np.linspace(0,1,n);x[-n:]*=np.linspace(1,0,n);return x
manifest=dict(schema='CAKOOD_PCM_EXPANDED_CANDIDATE_V2',native_acceptance=False,subjective_audition='UNPERFORMED_UNSUPPORTED_AUDIO_INPUT',source_rights_verified=True,voice_lane_unchanged=True,laughs=[],foley=[],celebration={},limitations=['Tier classifications follow historical source descriptions, not new listening judgments.','Native timing and subjective naturalness remain separate gates.'])
old={763960:1,763956:2,763959:3};nextid=4;reel=[];cue=[];t=0
credits=json.loads((R/'credit-record-map.json').read_text())
for e in json.load(open(B/'manifest.json'))['entries']:
 s=e['source'];sid=s['id'];src=B/s['source_path'];assert sha(src)==e['source_metrics']['sha256']
 take=old.get(sid,nextid)
 if sid not in old:nextid+=1
 tier={'light':1,'medium':2,'full':3}[e['tier']]
 if sid in old:
  p=base/f'@0PK{take:02X}01.001';meta=dict(file=str(p),sha256=sha(p),preserved_existing_bytes=True);x=decode(p);module=920;noun=take;start=0;end=len(x)/22050;policy='preserved existing cleared reference bytes, full original preview duration; no new subjective acceptance claimed'
 else:
  module=931;noun=take-3;x=decode(src);start=0;end=len(x)/22050;policy='complete source take; only20ms edge safety fades'
  if end>7:
   # One source contributes ONE take only; choose the lowest-energy ending aperture.
   n=441;power=np.array([np.mean(x[i:i+n]**2) for i in range(0,len(x)-n,n)])
   choices=np.arange(150,min(350,len(power)));j=int(choices[np.argmin(power[choices])]);end=(j+1)*.02
   x=x[:int(end*22050)];policy='one excerpt per source, low-energy endpoint between3–7s; subjective boundary review unperformed'
   n=min(6615,len(x)//4);x[-n:]*=np.linspace(1,0,n)
  x=process(x,{'light':-25,'medium':-23,'full':-21}[e['tier']]);meta=save(O/f'@0PV{noun:02X}01.001',x)
 entry=dict(stable_take_id=take,performance_id=take,source_take_id=e['source_take_id'],tier=tier,audio36=[module,noun,1,0,1],source=s,source_sha256=sha(src),source_interval=[start,end],edit_policy=policy,credit_record=credits.get(s['url']),subjective_audition='UNPERFORMED',**meta)
 manifest['laughs'].append(entry);cue.append(dict(take=take,tier=tier,start=round(t,4),end=round(t+len(x)/22050,4)));reel.extend([x,np.zeros(11025)]);t+=len(x)/22050+.5
save(A/'expanded-laughter-24.wav',np.concatenate(reel));(A/'expanded-laughter-cues.json').write_text(json.dumps(cue,indent=2)+'\n')
fm=json.load(open(F/'manifest.json'));fsource={s['id']:s for s in fm['sources']}
chosen=['tray_clatter_a','tray_clatter_b','cloth_handle_a','cloth_handle_b','paper_pickup_a','paper_pickup_b','page_turn_a','page_turn_b','door_mechanism_open_c','door_mechanism_close_b','footstep_concrete_a','footstep_concrete_b','footstep_carpet_a','footstep_carpet_b','impact_soft_a','impact_soft_b','window_open_a','window_wood_close_a']
for n,name in enumerate(chosen,1):
 e=next(a for a in fm['assets'] if a['id']==name);p=F/e['pcm_file'];assert sha(p)==e['pcm_sha256'];out=O/f'@0PW{n:02X}01.001';shutil.copy2(p,out)
 manifest['foley'].append(dict(stable_take_id=300+n,name=name,audio36=[932,n,1,0,1],source=fsource[e['source_id']],credit_record=credits.get(fsource[e['source_id']]['source_url']),historical_edit=e,file=str(out.relative_to(R)),sha256=sha(out),subjective_audition='UNPERFORMED'))
for n,name in [(19,'metalClick.ogg'),(20,'metalLatch.ogg'),(21,'creak1.ogg'),(22,'creak2.ogg')]:
 p=R/'assets/source/rpg-audio/Audio'/name;out=O/f'@0PW{n:02X}01.001';meta=save(out,process(decode(p),-27));manifest['foley'].append(dict(stable_take_id=300+n,name=name,audio36=[932,n,1,0,1],source=dict(title=name,creator='Kenney / Kenney Vleugels',source_url='https://kenney.nl/assets/rpg-audio',license='CC0-1.0',license_url='https://creativecommons.org/publicdomain/zero/1.0/',source_file=str(p.relative_to(R)),source_sha256=sha(p)),credit_record='END.ASSET.FOLEY.09',subjective_audition='UNPERFORMED',**meta))
# Original authored modal ceramic contacts. These are synthetic foley, never audience performances.
for n,f in [(23,1830),(24,2180)]:
 tt=np.arange(int(.26*22050))/22050;x=sum(a*np.sin(2*np.pi*hz*tt)*np.exp(-tt/tau) for a,hz,tau in [(1,f,.045),(.34,f*1.41,.024),(.15,f*2.71,.011)])*.12;x[:90]*=np.linspace(0,1,90)
 meta=save(O/f'@0PW{n:02X}01.001',x);manifest['foley'].append(dict(stable_take_id=300+n,name='authored_ceramic_contact_'+str(n-22),audio36=[932,n,1,0,1],source=dict(title='Original modal ceramic contact',creator='CaKoOD production',source_file='build_assets.py',license='Original project-authored synthesis; no third-party recording'),subjective_audition='UNPERFORMED',**meta))
# Recorded applause/cheer plus a short established hearty laugh, one authored PCM mix.
ap=process(decode(R/'assets/source/applause.wav'),-23);la=decode(base/'@0PK0301.001');length=max(len(ap),len(la));mix=np.zeros(length);mix[:len(ap)]+=ap*.85;mix[:len(la)]+=la*.30;mix*=min(1,.65/max(abs(mix)));meta=save(O/'@0PT0101.001',mix)
manifest['celebration']=dict(stable_take_id=201,audio36=[929,1,1,0,1],source_components=[dict(title='Applause',creator='Blender Foundation; applause edit by LeeZH',source_url='https://opengameart.org/content/applause',license='CC-BY-3.0',license_url='https://creativecommons.org/licenses/by/3.0/',source_file='assets/source/applause.wav',source_sha256=sha(R/'assets/source/applause.wav')),next(a['source'] for a in manifest['laughs'] if a['stable_take_id']==3)],modifications='Authored mix of recorded applause/cheer and established hearty laugh; mono, 22050Hz PCM16, filtering, gain and20ms edge fades; no synthetic crowd.',subjective_audition='UNPERFORMED',**meta)
manifest['counts']=dict(distinct_laugh_performances=len(manifest['laughs']),per_tier={t:sum(a['tier']==t for a in manifest['laughs']) for t in [1,2,3]},new_laugh_files=21,new_foley_files=24,real_recorded_celebration_files=1)
(R/'ASSET-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');shutil.copy2(O/'@0PT0101.001',A/'finale-recorded-laugh-cheer-applause.wav')
print(manifest['counts'])
