#!/usr/bin/env python3
"""Distinct original action-comedy family for canonicalVC01–VC04.
One persistent musical clock; no PCM or physical-combat semantics authored here.
"""
import json,copy,struct,hashlib
from pathlib import Path
import score_v4_core as c
OUT=c.OUT
EVENTS=['VC_ENTER','VC_TURN','VC_RESPONSE_COMMITTED','VC_KO_COMMITTED','VC_EXIT']
ENCOUNTERS={'VC01':{'opponent':'Milo','puzzle':'P05','location':'L06'},'VC02':{'opponent':'Vivian','puzzle':'P06','location':'L03'},'VC03':{'opponent':'Felix','after_puzzle':'P11 safe rescue','before_puzzle':'P12 public introduction','location':'L04'},'VC04':{'opponent':'Mr. Stringer','after':'P13 served/revealed/board delivered','before':'toast','location':'L05'}}

def change_cc7(smf,gains):
 ppq,events=c.g.parse_smf(smf);body=bytearray();prev=0
 for tick,order,msg in events:
  if msg[0]<240 and msg[0]&240==176 and msg[1]==7:msg=bytes((msg[0],7,gains[msg[0]&15]))
  if msg[0]==255:msg=msg[:2]+c.g.vlq(len(msg)-2)+msg[2:]
  body+=c.g.vlq(tick-prev)+msg;prev=tick
 return b'MThd'+struct.pack('>IHHH',6,0,1,ppq)+b'MTrk'+struct.pack('>I',len(body))+body

def variant(base,name,num,gains,encounter,thinking=False):
 r=copy.deepcopy(base);r.update(cue_id=name,resource_id=num,native_payload_path=f'native/{num:03d}.sound.bin',midi_path=f'midi/{name}.mid')
 midi=change_cc7((OUT/base['midi_path']).read_bytes(),gains);streams=c.g.decode_sound((OUT/base['native_payload_path']).read_bytes())
 for ch,es in streams.items():
  if ch!=15:streams[ch]=[(t,bytes((m[0],7,gains[ch])))if m[0]&240==176 and m[1]==7 else(t,m)for t,m in es]
 payload=c.g.sound_resource(streams,{role['channel']:role['voices']for role in r['roles']})
 for role in r['roles']:role['volume']=gains[role['channel']];r['initial_controllers'][str(role['channel'])]['cc7']=gains[role['channel']]
 r['gdd_binding']={'family':'MUS11_VERBAL_COMPETITIONS','events':EVENTS,'encounter':encounter,'encounter_contract':ENCOUNTERS.get(encounter),'state':'low-density thinking/turn'if thinking else'opponent color','same_note_program_expression_clock_as':base['cue_id']}
 r['sha256']={'midi':c.sha(midi),'native':c.sha(payload)};r['native_payload_bytes']=len(payload)
 r['phase_equivalence']={'base_resource':base['resource_id'],'difference':'CC7 only','same_program_note_tempo_expression_and_loop_events':True,'intended_runtime':'Use one persistent base sequence and gain-state selection, not independently started variant players. Entry across zero needs proven natural-window/tail clearing; positive gains may use tested ramps.'}
 (OUT/r['midi_path']).write_bytes(midi);(OUT/r['native_payload_path']).write_bytes(payload);(OUT/'native'/f'sound.{num:03d}').write_bytes(b'\x84\0'+payload);(OUT/'analysis'/f'{name}-manifest.json').write_text(json.dumps(r,indent=2));return r

def stinger(name,num,kind):
 """Candidate for reserved ACCENT role. Not a second score or PCM lane."""
 m=c.sources()['PRESENTATION_B'];src=m['source_notes'][:3]
 # Rhythm-only reduction of the authorized evenly spacedC/Eb/C call.
 # One repeated high woodblock pitch avoids a descending melodic triad;
 # timbral/pitched audibility against distant chords still needs listening.
 times=[0,.18,.36]if kind=='result'else[0,.20]
 pitches=[76,76,76]if kind=='result'else[76,76]
 duration=.86 if kind=='result'else .56
 events=[];ch=7
 events +=[(0,-5,bytes((0xc0|ch,115))),(0,-4,bytes((0xb0|ch,7,91))),(0,-4,bytes((0xb0|ch,10,64))),(0,-4,bytes((0xb0|ch,11,127))),(0,-4,bytes((0xb0|ch,64,0)))]
 trace=[]
 for i,(sec,pitch)in enumerate(zip(times,pitches)):
  t=round(sec*960);end=round((sec+.085)*960);events +=[(t,2,bytes((0x90|ch,pitch,67 if i==0 else 56))),(end,0,bytes((0x80|ch,pitch,0)))];n=src[i]
  trace.append(dict(source_stem=m['stem_id'],source_note_id=n['id'],source_pitch=n['pitch'],source_beat=n['beat'],transformation='source evenly spaced call rhythm uniformly condensed to single-pitch woodblock punctuation; melodic contour intentionally removed, not literal source melody',output_pitch=pitch,output_seconds=sec))
 end=round(duration*960);events +=[(0,-20,b'\xff\x51\x03\x07\xa1\x20'),(end,99,b'\xff\x2f\0')];body=bytearray();prev=0
 for t,o,msg in sorted(events,key=lambda x:(x[0],x[1])):body+=c.g.vlq(t-prev)+msg;prev=t
 smf=b'MThd'+struct.pack('>IHHH',6,0,1,480)+b'MTrk'+struct.pack('>I',len(body))+body;ev,tm=c.g.convert_smf(smf);ending=round(duration*1e6/16667);streams={7:ev,15:[(0,b'\xcf\0'),(ending,b'\xbf\x50\0')]};payload=c.g.sound_resource(streams,{7:1,15:0});c.d.held_profile(c.g.decode_sound(payload))
 r={'cue_id':name,'resource_id':num,'category':'reserved_accent_one_shot_candidate','bpm':120,'duration_seconds':ending*16667/1e6,'loop':None,'roles':[{'name':'ACCENT','channel':7,'program':115,'volume':91,'pan':64,'voices':1}],'native_payload_path':f'native/{num:03d}.sound.bin','midi_path':f'midi/{name}.mid','native_payload_bytes':len(payload),'source_trace':trace,'sha256':{'midi':c.sha(smf),'native':c.sha(payload)},'max_held_notes':1,'maximum_quantization_error_us':max(x['error_us']for x in tm),'gdd_binding':{'family':'MUS11_VERBAL_COMPETITIONS','event':'VC_KO_COMMITTED'if kind=='result'else'VC_RESPONSE_COMMITTED','single_fire_key':'encounter + attempt serial + exchange/result serial','semantic':'social result only, no physical impact or injury'},'routing':'Optional MIDI punctuation occupies the reserved ACCENT function; integration must prove spare native channel/isolation and existing stinger lifecycle. Do not stack players or add an instrument role beyond the eight-role budget. Never write shared percussion-channel9 controllers from this cue. Existing voice groan and optional crowd reaction are serialized separately on the one PCM lane.','lifecycle':'Consume once after committed outcome; never on selection preview, reread, restore or repeated input. Clear stale pending cue on context change. Musical timing never delays or determines correctness. Skip/duck if it would cover a consequential line.','validation':{'native_runtime_tested':False,'human_listening_approved':False,'note_balance':True}}
 (OUT/r['midi_path']).write_bytes(smf);(OUT/r['native_payload_path']).write_bytes(payload);(OUT/'native'/f'sound.{num:03d}').write_bytes(b'\x84\0'+payload);(OUT/'analysis'/f'{name}-manifest.json').write_text(json.dumps(r,indent=2));return r

def main():
 s=c.Score('MUS11_VERBAL_COMPETITIONS_BASE',140,120,132,True,'action',swing=.5)
 s.binding={'family':'MUS11_VERBAL_COMPETITIONS','events':EVENTS,'encounters':ENCOUNTERS,'meaning':'face-to-face verbal competition, not physical fighting'}
 for j,mid in enumerate(['PRESENTATION_B','PRESENTATION_B','TOGETHER_A','PRESENTATION_B']):
  s.motif(mid,j*32,32,ch=3 if j%2==0 else 4,velocity_curve=[76,79,82,78,73,70,74,72],section=['TAUT_SOURCE_CALL','MUTED_ANSWER','SPACIOUS_TURN','RETURN'][j])
  s.harmony.append(dict(beat=j*32+(24 if mid=='TOGETHER_A'else 28),root_pc=0,quality='dominant',label='C7 link back intoFminor',origin='authored action-comedy turnaround'))
 # A distinct source-motif transformation: clipped orchestral attacks but
 # unchanged source onset/harmonic alignment; only the major sustainedC anchor
 # keeps its dramatic space. This palette applies only to contests.
 for n in s.notes:
  if n['source']and n['source']['motif']=='PRESENTATION_B':
   n['duration']=min(n['duration'],.48 if n['source']['source_duration']>=1.5 else.24)
   n['source']['articulation_transform']='clipped action-comedy brass; source attack/harmony relation retained'
 s.tail(128,5,'Fm7 natural contest turnaround',quality='minor')
 s.accompany(dropouts=[(32,40),(72,80)],walking_sections=[(16,24),(112,120)],intensity=.94)
 s.annotations += ['Separate original late-70s action-comedy palette: taut bass, clipped brass, dry sharp kit and controlled electric guitar. No movie melody, recording or ethnic caricature is quoted.','Main exploration score remains its accepted relaxed sparse swing. The contest family uses its own coherent straight pocket, never scattered offbeat displacement.','Dialogue setup, selected retort, existing-profile social-KO groan and optional audience reaction use one serialized PCM owner. Music is ducked/cleared around those slots, not used to score correctness.']
 base=s.finish();reports=[base]
 standard={r['channel']:r['volume']for r in base['roles']}
 colors={'VC01':{1:92,3:112,4:92,5:104,2:0,6:0,9:103},'VC02':{1:109,3:86,4:105,5:76,2:0,6:0,9:87},'VC03':{1:87,3:91,4:88,5:111,2:0,6:0,9:104},'VC04':{1:101,3:93,4:112,5:72,2:0,6:0,9:89}}
 for num,(vc,values)in enumerate(colors.items(),141):reports.append(variant(base,f'MUS11_{vc}_COLOR',num,{**standard,**values},vc))
 thinking={**standard,1:67,2:0,3:24,4:25,5:35,6:0,9:55,0:92};reports.append(variant(base,'MUS11_THINKING_TURN',145,thinking,'any',True))
 reports +=[stinger('MUS11_RESPONSE_PUNCTUATION',146,'response'),stinger('MUS11_SOCIAL_RESULT',147,'result')]
 contract={'canonical_gdd_contract':'/workspace/shared/cakood/verbal-competitions-update/CANONICAL-CONTRACT.md','family':'MUS11_VERBAL_COMPETITIONS','status':'COMPOSED_CANDIDATES_NOT_NATIVE_OR_LISTENING_ACCEPTED','encounters':ENCOUNTERS,'events':EVENTS,'music_ownership':{'VC_ENTER':'Select opponent gain color and start/derive one persistent bed; no correct-response hint.','VC_TURN':'Choose low-density thinking/line mix; leave room for setup/retort, without a player timer.','VC_RESPONSE_COMMITTED':'After game commits exactly one composure change, consume optional one-shot once.','VC_KO_COMMITTED':'One social-result accent, then authored existing-profile groan before optional audience reaction on single PCM lane. No injury meaning.','VC_EXIT':'Discard stale transients and restore the valid underlying room/phase cue through a natural musical transition.'},'serials':'Every consumed response/result key includes encounter, attempt and exchange/result serial. Music never mutates composure, learned pairs, win flags, concessions or puzzle state.','save_pause_skip':'Save/restore reconstruct current bed/state/expression without replaying consumed transient cues; pause, skip, menu or mute is not a yield. Native lifecycle tests remain required.','variant_equivalence':'Resources141–145 are CC7-only references of140; do not play them concurrently. Runtime should maintain one score clock and apply tested state gains.','pcm':'One owner only: speech setup/retort, social-KO groan, audience reaction and foley are serialized or dropped by integrated arbiter. No new PCM file/player authored.','score_limit':'Reserved ACCENT one-shots require native channel/isolation proof and must replace that logical role, not add a ninth sounding part.','resources':[{'cue_id':r['cue_id'],'resource_id':r['resource_id'],'sha256':r['sha256'],'native_payload_path':r['native_payload_path']}for r in reports]}
 (OUT/'analysis/verbal-competition-music-contract.json').write_text(json.dumps(contract,indent=2));print('CONTEST CANDIDATES',len(reports))
if __name__=='__main__':main()
