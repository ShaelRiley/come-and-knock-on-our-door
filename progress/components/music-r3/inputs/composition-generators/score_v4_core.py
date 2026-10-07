#!/usr/bin/env python3
"""Accepted-feel authoring: source-aware grids, one swing map, natural phrases.
Existing V3 files are read-only. No runtime or player configuration is changed.
"""
from pathlib import Path
import json,sys,math,copy,collections,hashlib,struct
ROOT=Path(__file__).resolve().parents[2];OLD=ROOT/'assets/music-production/source-arrangements';V3=ROOT/'assets/music-production/source-arrangements-v3-swing';OUT=ROOT/'assets/music-production/source-arrangements-v4-approved';sys.path.insert(0,str(ROOT/'stock-sci/audio-proof'))
import generate as g
import generate_density as d
PPQ=480
DEFAULT_ROLES=[dict(name=n,channel=c,program=p,volume=v,pan=pan,voices=voices)for n,c,p,v,pan,voices in [('BASS',0,33,110,64,1),('KEYS',1,4,107,49,2),('TEXTURE',2,48,70,75,2),('LEAD',3,59,112,55,1),('REPLY',4,73,109,75,1),('GUITAR',5,27,96,82,2),('ACCENT',6,11,94,40,2),('KIT',9,0,98,64,4)]]
def sha(b):return hashlib.sha256(b).hexdigest()
def sources():
 old={m['id']:m for m in json.loads((OLD/'analysis/curated-motifs.json').read_text())['motifs']}
 verified=json.loads((OUT/'analysis/corrected-source-catalog.json').read_text()) if (OUT/'analysis/corrected-source-catalog.json').exists()else {'motifs':[]}
 for m in verified['motifs']:old[m['id']]=m
 home=old['HOME_A'];home['rhythm']={'reference_beat':home['start_beat'],'preserve_grid_beats':.5,'onsets':[{'source_note_id':n['id'],'grid_beat':round((n['beat']-home['start_beat'])*2)/2,'duration':n['duration']}for n in home['source_notes']]}
 v3=json.loads((V3/'analysis/RELAXED_SWING_FEEL_V3-manifest.json').read_text());home['harmony']=[]
 for h in v3['harmony']:
  if h.get('source_relative_beat')is not None and h['beat']<36:
   quality='minor'if h['label'].startswith(('Em','Am','Dm','Gm'))else 'dominant'if h['label']in('E7','Ab7','C7')else 'major'
   home['harmony'].append(dict(beat=h['source_relative_beat'],root_pc=h['root'],quality=quality,label=h['label'],dyad=h['dyad'],evidence=h['evidence']))
 home['audit_status']='Source-harmony and rhythm verified in accepted V3'
 return old

def sw(t,ratio=.6):
 b=math.floor(t);f=t-b;return b+(f*ratio/.5 if f<=.5 else ratio+(f-.5)*(1-ratio)/.5)
def eighth_grid(m):
 rows=m['rhythm']['onsets'];return {r['source_note_id']:r.get('normalized_straight_grid_beat',r.get('grid_beat_from_preferred_anchor',r.get('grid_beat')))for r in rows}
def harmony_grid(h):return h.get('normalized_straight_grid_beat',h.get('grid_beat_from_preferred_anchor',h['beat']))

def dyad_pcs(h):
 if 'dyad'in h:return [p%12 for p in h['dyad']]
 root=h['root_pc'];q=h['quality'];label=h.get('label','')
 # With an inversion bass already supplying the third, retain root/fifth in
 # the two-note shell. A third/fifth shell would erase Eb/G or G/B into minor.
 if h.get('bass_pc',root)!=root and q.startswith('major'):return[root,(root+7)%12]
 if q=='ambiguous_third':iv=(0,7)
 elif q=='neighbor_unison':iv=(0,0)
 elif q=='minor_major7':iv=(3,11)
 elif q=='major_sixth':iv=(4,9)
 elif q=='dominant_suspended':iv=(5,9)if 'Em upper'in label else(5,10)
 elif 'diminished'in q:iv=(3,6) # bass supplies root; retain the defining diminished fifth
 elif q.startswith('minor'):iv=(3,10)if '7'in label or '11'in label else(3,7)
 elif q=='dominant':iv=(4,10)
 else:iv=(4,11)if 'maj'in label.lower()else(4,7)
 return[(root+x)%12 for x in iv]
def voicing(pcs,previous=(57,64),low=53,high=73):
 candidates=[(a,b)for a in range(low,high+1)for b in range(a+3,high+1)if {a%12,b%12}==set(pcs)]
 if not candidates:candidates=[(low+(pcs[0]-low)%12,low+(pcs[1]-low)%12+12)]
 return min(candidates,key=lambda ab:abs(ab[0]-previous[0])+abs(ab[1]-previous[1]))

class Score:
 def __init__(self,name,num,bpm=112,beats=132,loop=True,style='house',swing=.6,startup=True):
  self.name=name;self.num=num;self.bpm=bpm;self.beats=beats;self.loop=loop;self.style=style;self.swing=swing;self.origin=round(.2*bpm/60*PPQ)/PPQ if startup else 0
  self.roles=copy.deepcopy(DEFAULT_ROLES);self.notes=[];self.controllers=[];self.harmony=[];self.sections=[];self.uses=[];self.binding={};self.annotations=[];self.speech_windows=[];self.markers=[];self.tempo_map=[{'beat':0,'bpm':bpm}]
  self._configure()
 def _configure(self):
  specs={'house':{},'kitchen':{1:0,3:73,4:11},'porch':{1:4,3:27,4:73},'passage':{1:4,3:71,4:27},'courtyard':{1:4,3:59,4:73},'showy':{1:4,3:65,4:59},'sincere':{1:4,3:27,4:73},'precise':{1:0,3:11,4:71},'credited':{1:4,3:73,4:11},'supper':{1:4,3:59,4:65},'pressure':{1:4,3:71,4:59},'together':{1:4,3:59,4:73},'quiet':{1:4,3:73,4:27},'exposed':{1:0,3:71,4:73},'action':{1:4,3:61,4:59,5:27}}
  for r in self.roles:
   if r['channel']in specs.get(self.style,{}):r['program']=specs[self.style][r['channel']]
   if self.style in('quiet','exposed'):r['volume']=round(r['volume']*.84)
   if self.style=='action'and r['channel']in(0,9):r['volume']=min(120,r['volume']+8)
 def at(self,u):return self.origin+sw(u,self.swing)
 def add(self,u,dur,ch,p,vel,source=None,gesture=''):
  if u>=self.beats or dur<=.025:return
  end=min(u+dur,self.beats)
  self.notes.append(dict(beat=self.at(u),duration=self.at(end)-self.at(u),unswung_beat=u,unswung_duration=end-u,channel=ch,pitch=int(p),velocity=max(1,min(106,round(vel))),source=source,gesture=gesture))
 def cc(self,ch,u,controller,value):self.controllers.append((round(self.at(u)*PPQ),-2,bytes((0xb0|ch,controller,value))))
 def chord(self,u):
  hs=sorted(self.harmony,key=lambda h:h['beat']);return next((h for h in reversed(hs)if h['beat']<=u+.00001),hs[0])
 def motif(self,mid,start,span=32,ch=3,transpose=0,scale=1.,velocity_curve=None,source_offset=0,source_limit=None,section=None,melody=True):
  bank=sources();m=bank[mid];grid=eighth_grid(m);rhythm_rows={x['source_note_id']:x for x in m['rhythm']['onsets']}
  velocity_curve=velocity_curve or[69,73,79,77,74,72,69,66]
  phrase_notes=[]
  for n in m['source_notes']:
   rawrel=grid[n['id']]
   if rawrel<source_offset-.001 or(source_limit is not None and rawrel>=source_limit-.001):continue
   rel=(rawrel-source_offset)*scale
   if rel>=span-.001:continue
   dur=rhythm_rows[n['id']].get('normalized_straight_duration',n['duration'])*scale
   p=n['pitch']+transpose
   # Register adjustment is global to the phrase; never snap melody pitches to
   # an unrelated local harmony. Wide original figures remain source-authentic.
   phrase_notes.append((rel,dur,p,n))
  if melody:
   for i,(rel,dur,p,n)in enumerate(phrase_notes):
    nxt=phrase_notes[i+1][0]if i+1<len(phrase_notes)else rel+dur
    dur=min(dur*(.985 if dur>=1 else .95),max(.05,nxt-rel-.018))
    # Do not truncate at span: natural source endings can cross a section join.
    if start+rel+dur>self.beats:raise ValueError(f'{self.name}: source phrase needs a composed tail beyond score end')
    bar=min(len(velocity_curve)-1,int(rel//4));vel=velocity_curve[bar]+(3 if abs(rel%8)<.02 else 0)
    self.add(start+rel,dur,ch,p,vel,dict(motif=mid,stem=m['stem_id'],source_note_id=n['id'],source_pitch=n['pitch'],source_beat=n['beat'],source_duration=n['duration'],transposition=transpose,source_grid_beat=grid[n['id']],source_offset=source_offset,scale=scale,grid_reference=m['rhythm'].get('preferred_ensemble_grid_origin_source_beat',m['rhythm']['reference_beat']),rhythm='Audited source-aware grid then common swing; phrase-scale transformation applies equally to melody and harmony; no guard chopping'),gesture='whole source-derived phrase')
  # Inherited harmony at the fragment entry is explicit.
  hs=m['harmony'];at_entry=max((h for h in hs if harmony_grid(h)<=source_offset+.001),key=harmony_grid,default=hs[0]);selected=[(0,at_entry)]
  selected +=[((harmony_grid(h)-source_offset)*scale,h)for h in hs if harmony_grid(h)>source_offset+.001 and(harmony_grid(h)-source_offset)*scale<span]
  for rel,h in selected:
   item=copy.deepcopy(h);item.update(beat=start+rel,root_pc=(h['root_pc']+transpose)%12,source_motif=mid,source_harmony_beat=harmony_grid(h),transposition=transpose,scale=scale)
   if 'dyad'in item:item['dyad']=[p+transpose for p in item['dyad']]
   if 'bass_pc'in item:item['bass_pc']=(item['bass_pc']+transpose)%12
   self.harmony.append(item)
  self.uses.append(dict(motif=mid,stem=m['stem_id'],start_beat=start,span=span,channel=ch,transpose=transpose,scale=scale,source_offset=source_offset,note_ids=[x[3]['id']for x in phrase_notes]if melody else[],lead_ownership='whole phrase/explicit source fragment, not note-by-note hocket',velocity_curve=velocity_curve,source_audit=m.get('audit_status')))
  self.sections.append((self.at(start),section or mid))
  if melody:
   for rel,val in[(0,90),(1,96),(2,103),(3,100),(4,98),(8,110),(12,105),(16,100),(20,96),(24,90),(27,94),(29.5,96)]:
    if rel<span:self.cc(ch,start+rel,11,val)
 def tail(self,start,root=5,label='Fmaj7',length=4,quality='major'):
  self.harmony.append(dict(beat=start,root_pc=root,quality=quality,label=label,origin='authored natural phrase-release / turnaround bar'))
  self.sections.append((self.at(start),'NATURAL_TURNAROUND'))
 def accompany(self,dropouts=(),walking_sections=(),texture_sections=(),intensity=1.):
  if not self.harmony:raise ValueError('Harmony required before accompaniment')
  self.harmony.sort(key=lambda h:h['beat'])
  effective_harmony=list({h['beat']:h for h in self.harmony}.values())
  def drop(u):return any(a<=u<b for a,b in dropouts)
  prev=(57,64);bass=[];styles=self.style
  for bar in range(math.ceil(self.beats/4)):
   bt=bar*4;phase=bar%8;quiet=styles in('quiet','exposed','passage');soft=drop(bt)
   level=intensity*(.78 if soft else 1.)
   if bar%16>=8 and bar%16<10:level*=.9
   if styles=='action':pulse=[0,1.5,2,3]if phase in(2,6)else[0,2]
   elif any(a<=bt<b for a,b in walking_sections):pulse=[0,1,2,3]
   else:pulse=[0,2]
   for at in pulse:
    u=bt+at;h=self.chord(u);root=36+h.get('bass_pc',h['root_pc'])
    while root>47:root-=12
    # Roots/fifths clarify broad pulses; restrained passing motion appears only
    # in intentionally walking passages, not scattered anticipations everywhere.
    if at==0 or any(abs(x['beat']-u)<.001 for x in effective_harmony) or h['quality']=='neighbor_unison':p=root
    elif at==2:p=(36+h['root_pc']) if h.get('bass_pc',h['root_pc'])!=h['root_pc'] else root+(6 if 'diminished'in h['quality']else 7)
    elif at==1:p=root+(3 if h['quality'].startswith('minor')or 'diminished'in h['quality']else 4)
    else:
     nh=self.chord(min(self.beats-.01,u+1));p=36+nh.get('bass_pc',nh['root_pc'])-1
     while p>47:p-=12
    bass.append([u,p,.75 if len(pulse)>2 else 1.25,(66 if at==0 else 61)*level])
   if not soft:
    if styles in('house','courtyard','together','supper'):pattern=[(0,.6),(2.5,.4)]if phase%2==0 else[(1.5,.42)]
    elif styles=='kitchen':pattern=[(0,.38),(2,.4)]if phase%2==0 else[(1,.35),(3,.3)]
    elif styles in('porch','sincere'):pattern=[(1,.55)]if phase%2==0 else[(2.5,.42)]
    elif styles in('passage','quiet','exposed'):pattern=[(0,.7)]if phase%2==0 else[]
    elif styles in('precise','credited'):pattern=[(0,.44),(2,.42)]if phase%2==0 else[(1.5,.38)]
    elif styles=='action':pattern=[(0,.22),(2.5,.18)]if phase%2==0 else[(1,.18)]
    else:pattern=[(0,.45)]if phase%2==0 else[(2,.36)]
    for at,dur in pattern:
     u=bt+at;h=self.chord(u);pv=voicing(dyad_pcs(h),prev);prev=pv
     for p in pv:self.add(u,dur,1,p,(54 if at==0 else 49)*level,gesture='sparse chord-aware comp')
    # Guitar answers vary by setting and phrase; it never fills every gap.
    if phase in((1,5)if styles not in('showy','action')else(2,6)) and not quiet:
     u=bt+2;h=self.chord(u)
     for p in voicing(dyad_pcs(h),prev):self.add(u,.28 if styles!='action'else .16,5,p+12,(48 if styles!='action'else 58)*level,gesture='single guitar answer')
   if any(a<=bt<b for a,b in texture_sections) and phase in(0,4)and not soft:
    h=self.chord(bt);pv=voicing(dyad_pcs(h),(67,72),60,79)
    for p in pv:self.add(bt+1,2.4,2,p,42*level,gesture='brief phrase-level string color, not permanent pad')
   # Rhythm vocabularies differ while preserving a shared within-cue grid.
   if styles in('quiet','exposed'):hat=[(0,23),(2,23)];kick=[0];snare=[]
   elif styles=='action':hat=[(0,31),(.5,22),(1,29),(1.5,20),(2,34),(2.5,23),(3,29),(3.5,21)];kick=[0,2];snare=[1,3]
   elif styles=='porch':hat=[(0,26),(1,27),(2,28),(3,27),(3.5,19)];kick=[0,2];snare=[3]
   elif styles=='kitchen':hat=[(0,29),(1,28),(1.5,20),(2,30),(3,29),(3.5,20)];kick=[0,2];snare=[1,3]
   else:hat=[(0,28),(1,31),(1.5,21),(2,30),(3,31),(3.5,21)];kick=[0,2];snare=[1,3]
   for at,v in hat:self.add(bt+at,.09,9,42,v*level,gesture='one shared pocket')
   for at in kick:self.add(bt+at,.10,9,36,(46 if styles!='action'else 58)*level,gesture='grounded broad pulse')
   for at in snare:self.add(bt+at,.09,9,38 if styles in('action','showy')else 37,(29 if styles!='action'else 48)*level,gesture='restrained backbeat')
   if styles=='courtyard'and phase==6:self.add(bt+3,.1,9,39,32*level,gesture='one ensemble handclap')
  # Clarify harmonic moves between the broad pulses, including odd integer
  # beats as well as offbeats, with no arbitrary bass
  # displacement. Remove a following redundant bass pulse rather than stutter.
  for h in effective_harmony:
   u=h['beat']
   if u%2 and u<self.beats:
    root=36+h.get('bass_pc',h['root_pc'])
    while root>47:root-=12
    bass.append([u,root,.92,60*intensity])
  bass.sort(key=lambda x:x[0]);dedup=[]
  for e in bass:
   if dedup and abs(dedup[-1][0]-e[0])<.001:continue
   if dedup and e[0]-dedup[-1][0]<.7 and e[1]==dedup[-1][1]:continue
   dedup.append(e)
  for i,(u,p,dur,v)in enumerate(dedup):
   if i+1<len(dedup):dur=min(dur,dedup[i+1][0]-u-.03)
   self.add(u,dur,0,p,v,gesture='source-harmony-aware bass')
  # Between-pulse harmonic changes receive one quiet shell when comp is present;
  # this explicitly preserves things such as the approved Ab7/Gm7/C7 cadence.
  for h in effective_harmony:
   u=h['beat']
   if u%2 and u<self.beats and not drop(u):
    if any(n['channel']==1 and abs(n['unswung_beat']-u)<.001 for n in self.notes):continue
    earlier=[n for n in self.notes if n['channel']==1 and n['unswung_beat']<u]
    if earlier:
     lastu=max(n['unswung_beat']for n in earlier);prior=sorted({n['pitch']for n in earlier if n['unswung_beat']==lastu})
     localprev=tuple(prior[-2:])if len(prior)>=2 else prev
    else:localprev=prev
    for p in voicing(dyad_pcs(h),localprev):self.add(u,.38,1,p,49*intensity,gesture='source harmonic change')
  self.annotations += ['One explicit swing map per cue; source-specific rhythmic grids preserve ornaments and pickup phase.','Small ensemble and phrase-level dropout/reentry; distinct accompaniment vocabularies by setting.','No note is cut, split or rearticulated to manufacture a native safety gap.']
 def finish(self):
  # A HOME major-third cadence may carry naturally across its major tonic,
  # but its E/Eb-equivalent semitone must not linger into a new minor family.
  # End only that final source note as a phrase breath, never every bar/role.
  for h in list({h['beat']:h for h in sorted(self.harmony,key=lambda h:h['beat'])}.values()):
   if not h['quality'].startswith('minor'):continue
   join=h['beat'];boundary=self.at(join)
   for n in self.notes:
    src=n.get('source')
    if src and src['motif']=='HOME_A' and n['pitch']%12==(h['root_pc']+11)%12 and n['unswung_beat']<join and n['beat']+n['duration']>boundary:
     n['duration']=self.at(join-.04)-n['beat'];n['unswung_duration']=join-.04-n['unswung_beat']
     src['join_articulation']='Final HOME cadence ends a .04-beat breath before a new minor-family entry; source onset/pitch intact, major7 carry deliberately shortened for harmonic continuity'
     self.annotations.append(f'Authored major-to-minor phrase breath at beat{join:g}; no safety-guard rearticulation')
  # Natural monophonic ownership: only terminate a prior same-channel/same-pitch
  # articulation when the next authored attack genuinely replaces it.
  # Release a sparse piano shell as the next authored piano chord enters.
  # This is harmonic articulation, not a timing guard or full-band rest.
  piano_starts=sorted({n['beat']for n in self.notes if n['channel']==1})
  for n in self.notes:
   if n['channel']==1:
    later=next((t for t in piano_starts if t>n['beat']+.00001),None)
    if later is not None:n['duration']=min(n['duration'],later-n['beat']-.008)
  bykey=collections.defaultdict(list)
  for n in self.notes:bykey[n['channel'],n['pitch']].append(n)
  ns=[]
  for key,notes in bykey.items():
   notes.sort(key=lambda x:x['beat']);last=None
   for n in notes:
    if last and abs(last['beat']-n['beat'])<.00001:continue
    if last:last['duration']=min(last['duration'],n['beat']-last['beat']-.012)
    ns.append(n);last=n
  self.notes=[n for n in ns if n['duration']>.02]
  events=[]
  for r in self.roles:
   ch=r['channel'];events.append((0,-10,bytes((0xc0|ch,r['program']))))
   for cc,v in[(7,r['volume']),(10,r['pan']),(64,0),(1,0),(11,100 if ch in(3,4)else 127)]:events.append((0,-9,bytes((0xb0|ch,cc,v))))
   events.append((0,-8,bytes((0xe0|ch,0,64))))
  events+=self.controllers
  for n in self.notes:events +=[(round(n['beat']*PPQ),2,bytes((0x90|n['channel'],n['pitch'],n['velocity']))),(round((n['beat']+n['duration'])*PPQ),0,bytes((0x80|n['channel'],n['pitch'],0)))]
  for t,label in self.sections+self.markers:
   b=label.encode('ascii','replace');events.append((round(t*PPQ),-20,b'\xff\x06'+g.vlq(len(b))+b))
  # Tempo steps are genuine SMF events and are integrated before SCI rounding.
  for t in self.tempo_map:events.append((round(self.at(t['beat'])*PPQ)if t['beat']else 0,-30,b'\xff\x51\x03'+round(60e6/t['bpm']).to_bytes(3,'big')))
  end=round(self.at(self.beats)*PPQ);events +=[(0,-29,b'\xff\x58\x04\x04\x02\x18\x08'),(end,99,b'\xff\x2f\0')]
  body=bytearray();prev=0
  for tick,order,msg in sorted(events,key=lambda x:(x[0],x[1])):body+=g.vlq(tick-prev)+msg;prev=tick
  smf=b'MThd'+struct.pack('>IHHH',6,0,1,PPQ)+b'MTrk'+struct.pack('>I',len(body))+body
  converted,timing=g.convert_smf(smf);times,tempos=d.source_times(smf);streams=collections.defaultdict(list)
  for tick,msg in converted:streams[msg[0]&15].append((tick,msg))
  start=times.get(round(self.origin*PPQ),{'sci_tick':12})['sci_tick'];endtick=times[end]['sci_tick']
  controls=[(0,b'\xcf\0'),(0,b'\xbf\x50\0'),(6,b'\xcf\x01')]
  if self.loop:controls +=[(start,b'\xbf\x50\0'),(start,b'\xcf\x7f')]
  section_cues=[]
  for i,(beat,label)in enumerate(self.sections,2):
   tick=times[round(beat*PPQ)]['sci_tick'];controls.append((tick,bytes((0xcf,i))));section_cues.append(dict(cue=i,tick=tick,label=label,is_global_safe_gate=False))
  controls.append((endtick,b'\xbf\x50\0'));streams[15]=sorted(controls,key=lambda x:x[0])
  payload=g.sound_resource(dict(streams),{r['channel']:r['voices']for r in self.roles});decoded=g.decode_sound(payload);peak=max(n for _,n in d.held_profile(decoded));assert peak<=18,(self.name,peak)
  # Loop turnaround is composed into the form, allowing all key releases to
  # happen naturally before EOT; the score never chops every bar for safety.
  firstattack=min((t for ch,es in decoded.items()if ch!=15 for t,m in es if m[0]&240==144 and m[2]),default=0)
  lastoff=max((t for ch,es in decoded.items()if ch!=15 for t,m in es if m[0]&240==128),default=0)
  assert lastoff<endtick,(self.name,'needs a natural ending')
  windows={}
  for ch,es in decoded.items():
   if ch==15:continue
   active=set();silent=0;out=[]
   for tick,msg in es:
    if msg[0]&240==144 and msg[2]:
     if not active and tick-silent>=9:out.append(dict(key_silent_start=silent,next_attack=tick,first_possible_guard=silent+3,last_possible_guard=tick-6))
     active.add(msg[1])
    elif msg[0]&240==128:
     active.discard(msg[1])
     if not active:silent=tick
   if not active and endtick-silent>=9:out.append(dict(key_silent_start=silent,next_attack=endtick,first_possible_guard=silent+3,last_possible_guard=endtick-6))
   windows[str(ch)]=out
  (OUT/'midi'/f'{self.name}.mid').write_bytes(smf);(OUT/'native'/f'{self.num:03d}.sound.bin').write_bytes(payload);(OUT/'native'/f'sound.{self.num:03d}').write_bytes(b'\x84\0'+payload)
  r=dict(cue_id=self.name,resource_id=self.num,bpm=self.bpm,swing_offbeat_fraction=self.swing,beats=self.beats,bars=self.beats/4,style=self.style,duration_seconds=endtick*16667/1e6,loop={'start_tick':start,'end_tick':endtick,'natural_key_release_before_end_ticks':endtick-lastoff}if self.loop else None,roles=self.roles,notes=self.notes,note_count=len(self.notes),harmony=self.harmony,sections=self.sections,section_cues=section_cues,source_motif_uses=self.uses,expression_timeline=[dict(source_tick=t,native_tick=times[t]['sci_tick'],channel=m[0]&15,controller=m[1],value=m[2])for t,_,m in self.controllers],initial_controllers={str(r['channel']):{'cc7':r['volume'],'cc10':r['pan'],'cc11':100 if r['channel']in(3,4)else 127,'cc64':0,'pitch_bend':8192}for r in self.roles},tempo_map=tempos,gdd_binding=self.binding,annotations=self.annotations,speech_windows=self.speech_windows,initial_guard={'cue':1,'guard_tick':6,'attack_tick':firstattack,'loop_origin_tick':start,'metadata_basis':'Actual earliest exported note attack; section markers are not global safe gates'},natural_role_key_windows=windows,max_held_notes=peak,native_payload_bytes=len(payload),native_payload_path=f'native/{self.num:03d}.sound.bin',midi_path=f'midi/{self.name}.mid',sha256={'midi':sha(smf),'native':sha(payload)},maximum_quantization_error_us=max(x['error_us']for x in timing),validation={'source_bytes_and_events_checked':True,'note_balance':True,'native_runtime_tested':False,'human_listening_approved':False},status='COMPOSED_FROM_USER_APPROVED_V3_PRINCIPLES; this full cue is not individually listening/native approved',native_contract='One musical sequence clock. No global-safe meaning assigned to section cues. Use natural per-role key/tail windows and tested muted-role clearing/positive-gain ramps; no blanket bar chop. CC11 timeline is explicit because SCI remap does not cache expression. Cross-family swaps use authored musical transitions. One PCM speech/laughter/foley lane remains separate.')
  (OUT/'analysis'/f'{self.name}-manifest.json').write_text(json.dumps(r,indent=2));print(self.name,self.num,round(r['duration_seconds'],3),'s',len(self.notes),'notes',peak,'held',flush=True);return r
