#!/usr/bin/env python3
"""Original deterministic abstract-speech renderer and integration reference.

The text is NOT synthesized intelligible speech. Word-vowel groups provide an
approximate syllabic rhythm; punctuation provides breathing/turn pauses. Mouth
poses represent amplitude cadence, not phonemes. Native implementation polls the
one PCM lane's position, never a second free-running animation timer.
"""
from __future__ import annotations
from pathlib import Path
import hashlib, io, json, math, re, struct, wave

HERE=Path(__file__).resolve().parent
RATE=22050
MAX_TEXT=500
MAX_TICKS=1800
PROFILES={p['id']:p for p in json.loads((HERE/'profiles.json').read_text())['profiles']}
PUNCT={',':9,';':13,':':13,'.':17,'!':19,'?':21,'…':24,'—':15,'–':12,'-':4}

def base36(n:int,width:int)->str:
    if n<0:raise ValueError('Negative resource number')
    s=''
    while n:s='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[n%36]+s;n//=36
    if len(s)>width:raise ValueError('Audio36 field overflow')
    return (s or '0').rjust(width,'0')

def patch_name(module:int,noun:int,verb:int=1,cond:int=0,seq:int=1)->str:
    if not(0<=module<36**3 and all(0<=n<=255 for n in (noun,verb,cond)) and 0<=seq<36):
        raise ValueError('Audio36 tuple outside proven filename/kernel range')
    return '@'+base36(module,3)+base36(noun,2)+base36(verb,2)+'.'+base36(cond,2)+base36(seq,1)

def schedule(line_id:str,speaker:str,text:str)->dict:
    if speaker not in PROFILES:raise ValueError('Unknown speaker')
    if not text.strip() or len(text)>MAX_TEXT:raise ValueError('Caption must have 1..500 characters; split longer pages')
    p=PROFILES[speaker]; tick=3; pulses=[]; events=[{'tick':0,'pose':0}]; i=0
    tokens=list(re.finditer(r"[\w]+(?:['’][\w]+)*|[^\w\s]",text,re.UNICODE))
    for token in tokens:
        word=token.group()
        if not any(c.isalnum() for c in word):
            tick+=PUNCT.get(word,0);continue
        letters=word.lower(); groups=list(re.finditer(r'[aeiouy]+',letters))
        syllables=max(1,len(groups))
        if len(letters)>3 and letters.endswith('e') and not letters.endswith(('le','ee')) and syllables>1:syllables-=1
        for j in range(syllables):
            variation=((sum(map(ord,letters))+j)%3)-1
            duration=max(4,p['pulse_ticks']+variation)
            step=p['pitch_steps'][i%len(p['pitch_steps'])]
            # Phrase-final contour is authored punctuation, not language recognition.
            if token.end()==len(text) or (token.end()<len(text) and text[token.end()] in '.!?'):
                step+=3 if text[token.end():token.end()+1]=='?' else -2
            frequency=p['pitch_hz']*2**(step/12)
            pulses.append({'start':tick,'end':tick+duration,'frequency':round(frequency,6),'source_start':token.start(),'source_end':token.end(),'word':word})
            events.extend([{'tick':tick,'pose':2},{'tick':tick+max(2,duration*2//3),'pose':1},{'tick':tick+duration,'pose':0}])
            tick+=duration+p['gap_ticks'];i+=1
        tick+=p['word_gap_ticks']
    tick+=3
    if tick>MAX_TICKS:raise ValueError('Utterance exceeds 30 seconds; split the authored caption page')
    if not pulses:raise ValueError('Line must contain a spoken word')
    events.append({'tick':tick,'pose':0})
    return {'schema':1,'line_id':line_id,'speaker':speaker,'text':text,'duration_ticks':tick,'sample_rate':RATE,'pulses':pulses,'mouth_events':events,'mouth_meaning':['closed','narrow','open'],'sync':'Audio36 DoAudio(6) position at 60 Hz','approximate_syllables':True}

def render(plan:dict)->bytes:
    p=PROFILES[plan['speaker']];samples=[0.0]*round(plan['duration_ticks']*RATE/60)
    norm=sum(p['harmonics'])
    for pulse in plan['pulses']:
        start=round(pulse['start']*RATE/60);end=round(pulse['end']*RATE/60);n=end-start;phase=0
        for j in range(n):
            u=j/max(1,n-1);t=j/RATE
            attack=min(1,j/(RATE*.008));release=min(1,(n-1-j)/(RATE*.018))
            envelope=max(0,attack*release)*math.exp(-p['decay']*u)
            f=pulse['frequency']*(1+p['glide']*(1-u)+p['vibrato_depth']*math.sin(2*math.pi*p['vibrato_hz']*t))
            phase+=2*math.pi*f/RATE
            value=sum(a*math.sin((k+1)*phase) for k,a in enumerate(p['harmonics']))/norm
            samples[start+j]=0.19*envelope*value
    stream=io.BytesIO()
    with wave.open(stream,'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(RATE)
        w.writeframes(struct.pack('<'+'h'*len(samples),*(round(x*32767) for x in samples)))
    return stream.getvalue()

def sync_patch(plan:dict)->bytes:
    # Native Sync36 resource: external type14 header, signed16 tick/cue pairs, -1 end.
    return bytes((0x8e,0))+b''.join(struct.pack('<hh',e['tick'],e['pose']) for e in plan['mouth_events'])+struct.pack('<h',-1)

def pose_at(plan:dict,tick:int)->int:
    pose=0
    for event in plan['mouth_events']:
        if event['tick']>tick:break
        pose=event['pose']
    return pose if 0<=tick<plan['duration_ticks'] else 0

