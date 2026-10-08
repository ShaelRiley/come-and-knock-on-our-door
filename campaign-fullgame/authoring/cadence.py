"""Portable original selected-date Frankie atom synthesis, adapted 2026-10-08."""
from pathlib import Path
import json,hashlib,io,wave,struct
import voice as talk
H=Path(__file__).resolve().parent
def sha(data):return hashlib.sha256(data).hexdigest()
def generate(destination=None):
 out=Path(destination or H/'generated');out.mkdir(parents=True,exist_ok=True);rows=[];profile=talk.PROFILES['frankie']
 for step in range(-5,5):
  for duration in [5,6,7]:
   for phase in range(4):
    noun=1+((step+5)*3+duration-5)*4+phase
    frequency=round(profile['pitch_hz']*2**(step/12),6)
    # Render through the unchanged original additive renderer, then extract one
    # pulse and its original three-tick syllable gap. Absolute rounding phase
    # matters because 22050/60 is a half-integer and Python round is ties-to-even.
    plan={'speaker':'frankie','duration_ticks':phase+duration+3,'pulses':[{'start':phase,'end':phase+duration,'frequency':frequency}]}
    full=talk.render(plan)
    with wave.open(io.BytesIO(full),'rb') as w:pcm=w.readframes(w.getnframes())
    pcm=pcm[round(phase*talk.RATE/60)*2:]
    dest=io.BytesIO()
    with wave.open(dest,'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(talk.RATE);w.writeframes(pcm)
    data=dest.getvalue();mouth=[{'tick':0,'pose':2},{'tick':max(2,duration*2//3),'pose':1},{'tick':duration,'pose':0},{'tick':duration+3,'pose':0}]
    sync=talk.sync_patch({'mouth_events':mouth});name=talk.patch_name(927,noun)
    (out/name).write_bytes(data);(out/('#'+name[1:])).write_bytes(sync)
    rows.append(dict(noun=noun,step=step,pulse_ticks=duration,tail_ticks=3,rounding_phase=phase,frequency=frequency,frames=len(pcm)//2,audio=name,sync='#'+name[1:],audio_sha256=sha(data),sync_sha256=sha(sync),mouth_events=mouth))
 name=talk.patch_name(927,121);dest=io.BytesIO()
 with wave.open(dest,'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(talk.RATE);w.writeframes(bytes(round(4000*talk.RATE/60)*2))
 data=dest.getvalue();sync=talk.sync_patch({'mouth_events':[{'tick':0,'pose':0},{'tick':4000,'pose':0}]})
 (out/name).write_bytes(data);(out/('#'+name[1:])).write_bytes(sync)
 rows.append(dict(noun=121,silence_ticks=4000,audio=name,sync='#'+name[1:],audio_sha256=sha(data),sync_sha256=sha(sync)))
 manifest=dict(schema=1,module=927,scope='Original composited Frankie atoms, not pre-rendered dates and not whole-page waveform identity',speaker='frankie',speaker_id=3,host_object=8,profile=profile,profile_file_sha256=sha((H/'profiles.json').read_bytes()),renderer_sha256=sha((H/'voice.py').read_bytes()),sample_rate=22050,channels=1,sample_width=2,rows=rows)
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');return manifest
