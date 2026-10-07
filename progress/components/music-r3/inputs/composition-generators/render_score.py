#!/usr/bin/env python3
"""Offline exact-candidate native-stream render using approved FluidSynth/FluidR3.
Never opens an audio device. No game/player configuration changes or normalization.
"""
from pathlib import Path
import sys,json,wave,math,argparse,hashlib
import numpy as np
from scipy.signal import resample_poly
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'assets/music-production/source-arrangements'
sys.path.insert(0,str(ROOT/'stock-sci/audio-proof'))
import generate as g
import profile_fluidsynth as p
class Synth(p.Synth):
 def __init__(self,volume):super().__init__(p.LIBRARY,p.SOUNDFONT);self.volume=volume
 def send(self,msg):
  if msg[0]&240==176 and msg[1]==7:
   v=msg[2]*100//127;master=(self.volume+1)*15//256;v=v*master//15 if v*master else 0
   if msg[2] and master:v=max(1,v)
   self.call('fluid_synth_cc',msg[0]&15,7,v)
  else:super().send(msg)
def db(v):return 20*math.log10(v)if v else None
def render(manifest,volume=161,write=True):
 streams=g.decode_sound((OUT/manifest.get('native_payload_path',f"native/{manifest['resource_id']:03d}.sound.bin")).read_bytes())
 ev=[]
 for ch,es in streams.items():
  if ch==15:continue
  for t,msg in es:ev.append((p.callback_index(t*16667),msg))
 end_us=round(manifest['duration_seconds']*1e6);endcb=(end_us+3999)//4000
 for ch in streams:
  if ch!=15:
   ev.extend([(endcb-1,bytes((0xb0|ch,123,0))),(endcb-1,bytes((0xb0|ch,64,0)))])
 ev.sort(key=lambda x:(x[0],0 if x[1][0]&240==128 else 1))
 synth=Synth(volume);chunks=[];frames=idx=maxvoices=0
 try:
  for cb in range(endcb+1500):
   while idx<len(ev)and ev[idx][0]<=cb:synth.send(ev[idx][1]);idx+=1
   maxvoices=max(maxvoices,synth.active());target=round((cb+1)*p.RATE*.004)
   a,b=synth.render(target-frames);frames=target;chunks.append(np.column_stack((a,b)))
  audio=np.concatenate(chunks);peak=float(abs(audio).max());tp=float(abs(resample_poly(audio,4,1,axis=0)).max());rms=float(np.sqrt(np.mean(audio.astype(float)**2)))
  report=dict(cue_id=manifest['cue_id'],music_volume=volume,whole_sound=100,sample_peak_dbfs=db(peak),oversampled_4x_peak_dbfs=db(tp),rms_dbfs=db(rms),samples_at_or_above_full_scale=int(np.count_nonzero(abs(audio)>=1)),max_active_fluid_voices=maxvoices,final_active_fluid_voices=synth.active(),duration_seconds=len(audio)/p.RATE,notes='One exact decoded SCI pass plus6-second release; musical channels retain authored logical IDs. Native allocator/lifecycle/speech/laughter overlap and human listening are separate gates. No loudness normalization or user gain override.')
  assert peak<1,report
  if write:
   path=OUT/'renders'/f"{manifest['cue_id']}-FluidR3-v{volume}.wav"
   with wave.open(str(path),'wb')as f:f.setparams((2,2,p.RATE,0,'NONE','not compressed'));f.writeframes(np.round(np.clip(audio,-1,1)*32767).astype('<i2').tobytes())
   report.update(file=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
  return report
 finally:synth.close()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--cue',action='append');parser.add_argument('--new-bank',action='store_true');args=parser.parse_args();reports=[]
 paths=sorted((OUT/'analysis').glob('*-manifest.json'))
 for path in paths:
  m=json.loads(path.read_text())
  if args.cue and m['cue_id'] not in args.cue:continue
  if args.new_bank and m['resource_id']<110:continue
  for v in (161,255):
   r=render(m,v,write=v==161);reports.append(r);print(json.dumps(r),flush=True)
 result=dict(status='OFFLINE_COMPONENT_RENDER_ONLY',sample_rate=p.RATE,fluidsynth={'version':'2.4.4','sha256':p.sha(p.LIBRARY)},soundfont={'name':'FluidR3_GM.sf2','sha256':p.sha(p.SOUNDFONT),'license_notice':'licenses/FluidR3_GM-copyright.txt'},scummvm_model='SCI master floor((music_volume+1)*15/256); whole-Sound100;4ms callback quantization; same documented FluidSynth defaults as the native proof',renders=reports)
 old_path=OUT/'analysis/render-validation.json'
 if old_path.exists():
  old=json.loads(old_path.read_text());changed={(r['cue_id'],r['music_volume'])for r in reports}
  result['renders']=[r for r in old.get('renders',[])if (r['cue_id'],r['music_volume'])not in changed]+reports
 old_path.write_text(json.dumps(result,indent=2))
if __name__=='__main__':main()
