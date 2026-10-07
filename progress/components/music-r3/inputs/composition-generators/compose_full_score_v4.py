#!/usr/bin/env python3
"""Varied source-derived soundtrack under approved relaxed/sparse V3 principles.
No existing audition, runtime, player preference or game logic is changed.
"""
import json,copy,struct,collections
from pathlib import Path
import score_v4_core as c
OUT=c.OUT
HOME='HOME_A';PRES='PRESENTATION_A';SHOW='PRESENTATION_B';WARM='TOGETHER_A';REPLY='TOGETHER_B'

def harmony_override(score,beat,root,label,quality='dominant',bass=None):
 h=dict(beat=beat,root_pc=root,label=label,quality=quality,origin='authored link between complete source phrases')
 if bass is not None:h['bass_pc']=bass
 score.harmony.append(h)

def longform(name,num,style,primary=HOME,secondary=HOME,trans=0,secondary_trans=0,bpm=112,binding=None,quiet=False):
 score=c.Score(name,num,bpm,132,True,style);score.binding=binding or{}
 # A / answering A / a genuinely different view / return plus one composed
 # release bar. The tail preserves source endpoints rather than cutting notes.
 motifs=[primary,primary,secondary,primary]
 for j,mid in enumerate(motifs):
  start=j*32;tr=secondary_trans if j==2 else trans
  curve=([69,73,79,77,74,72,69,66]if j==0 else[61,64,70,73,78,81,75,70]if j==1 else[64,68,71,75,72,68,65,63]if j==2 else[70,73,77,78,74,71,68,66])
  if quiet:curve=[v-7 for v in curve]
  score.motif(mid,start,span=32,ch=3 if j%2==0 else 4,transpose=tr,velocity_curve=curve,section=['A_STATEMENT','A_PRIME_REPLY','B_NEW_COLOR','A_DOUBLE_PRIME_RETURN'][j])
  # Full source phrases shorter than eight bars retain their real shape and
  # finish naturally. The remaining time is a composed harmonic breath.
  if mid==SHOW:
   harmony_override(score,start+28,(0+tr)%12,'C7-derived turnaround','dominant')
  elif mid==WARM:
   harmony_override(score,start+24,(0+tr)%12,'C7-derived reply link','dominant')
  elif mid==REPLY:
   # Final G/B is preserved, then source keyCm is settled before its next call.
   harmony_override(score,start+20,(0+tr)%12,'minor arrival after source G/B','minor')
   harmony_override(score,start+28,(7+tr)%12,'dominant into next phrase','dominant')
 # Resolve the last primary's actual ending into its opening tonal region.
 root=(c.sources()[primary]['harmony'][0]['root_pc']+trans)%12
 quality='minor'if primary in(SHOW,WARM,REPLY)else'major'
 score.tail(128,root,f'{root} natural phrase-release bar',quality=quality)
 drop=[(32,40),(80,84)]
 if quiet:drop +=[(0,4),(48,56),(96,100)]
 walking=[(16,24),(112,120)]if style in('kitchen','showy','supper')else[]
 texture=[(48,56),(112,120)]if style in('courtyard','credited','together')else[]
 score.accompany(dropouts=drop,walking_sections=walking,texture_sections=texture,intensity=.83 if quiet else 1.)
 score.annotations += ['Audited motif and harmony are transposed together; ornaments/pickup phase use each source-specific grid.','33-bar form contains32bars of thematic development plus a composed turnaround/release bar. This is musical form, not an imposed pre-bar safety gap.','Different state cues are complete compositions. Their note streams are not claimed phase-equivalent; native transitions need authored entry/bridge handling.']
 return score

def sparse_fragment(score,mid,start,source_offset,source_limit,span,ch=3,transpose=0,velocity=66,scale=1.):
 score.motif(mid,start,span=span,ch=ch,transpose=transpose,scale=scale,velocity_curve=[velocity]*16,source_offset=source_offset,source_limit=source_limit,section='SOURCE_FRAGMENT_RESPONSE')

def main():
 ready=set(c.sources());assert all(mid in ready and 'rhythm'in c.sources()[mid]for mid in(HOME,PRES,SHOW,WARM,REPLY))
 reports=[]
 # Exact60s opening at120BPM, only8BPM above the accepted listening reference.
 # It retains the approved pocket and sparse phrase ownership, not V1's blocks.
 s=c.Score('MUS01_OPENING',100,120,120,False,'house',startup=False)
 s.binding={'episode':'E00','autoplay_seconds':60,'opening_only':True}
 harmony_override(s,0,0,'C7 introductory invitation');harmony_override(s,8,0,'C7 pickup')
 for j,start in enumerate((12,44,76)):
  s.motif(HOME,start,span=32,ch=3 if j!=1 else 4,velocity_curve=([69,73,79,77,74,72,69,66]if j!=1 else[61,64,70,73,78,81,75,70]),section=['TITLE_THEME','SOFTER_REPLY','ENSEMBLE_RETURN'][j])
 s.tail(108,5,'Fmaj7 open-door cadence',length=12)
 s.accompany(dropouts=[(44,52)],texture_sections=[(92,100)],intensity=1.)
 # Quiet startup is outside the musical phrase; subsequent attacks keep their
 # authored grid. No other notes are cropped for a guard.
 s.notes=[n for n in s.notes if n['beat']>=.4]
 for sec,name in zip(range(6,54,6),['JACKIE','BUNNY','FRANKIE','STRINGER','MILO','VIVIAN','RITA','FELIX']):
  s.markers +=[(sec*2,'INTRO_'+name),((sec+2)*2,'FREEZE_'+name)]
 s.annotations.append('60-second visual timing is unchanged; exact card markers are presentation data, not puzzle state. This cue is an adaptation of the approved feel, not a claim of individual listening approval.')
 reports.append(s.finish())
 # Home/neighborhood states share the accepted tonal region and swing pocket,
 # with clear instrumental, density and form variation instead of random notes.
 specs=[
 ('MUS01_INVITATION',101,'porch',HOME,HOME,0,0,112,{'episodes':['E01'],'puzzles':['P01','P02'],'locations':['L03','L01']}),
 ('MUS02_HOUSE_LIVING',102,'house',HOME,HOME,0,0,112,{'episode':'E02','location':'L01'}),
 ('MUS02_HOUSE_KITCHEN',103,'kitchen',HOME,HOME,0,0,112,{'episode':'E02','location':'L02','puzzle':'P07'}),
 ('MUS03_PORCH',104,'porch',HOME,HOME,0,0,112,{'episode':'E02','location':'L03'}),
 ('MUS03_SIDE_PASSAGE',105,'passage',HOME,HOME,0,-12,112,{'episode':'E02','location':'L04','puzzles':['P04','P06']}),
 ('MUS03_COURTYARD',106,'courtyard',HOME,PRES,0,-2,112,{'episode':'E02','location':'L05','puzzle':'P08'}),
 ('MUS04_MILO_SHOWY',107,'showy',SHOW,HOME,0,0,112,{'episode':'E02','location':'L06','puzzle':'P05','state':'before sincere agreement'}),
 ('MUS04_MILO_SINCERE',108,'sincere',HOME,SHOW,0,0,112,{'episode':'E02','location':'L06','puzzle':'P05','state':'after committed sincere agreement'}),
 ('MUS05_STRINGERS_PRECISE',109,'precise',PRES,HOME,0,2,110,{'episode':'E02','location':'L07','puzzle':'P03','state':'before credit'}),
 ('MUS05_STRINGERS_CREDITED',110,'credited',HOME,PRES,2,0,110,{'episode':'E02','location':'L07','puzzle':'P03','state':'credit committed'}),
 ('MUS06_SUPPER_COMPOSURE',111,'supper',PRES,HOME,-2,0,110,{'episode':'E03','puzzles':['P08_READY','P09','P10'],'state':'surface composure'}),
 ('MUS06_SUPPER_PRESSURE',112,'pressure',SHOW,WARM,0,0,110,{'episode':'E03','puzzles':['P09','P10'],'state':'comic pressure, no countdown'}),
 ('MUS07_RESCUE_PRESSURE',113,'pressure',REPLY,SHOW,-7,0,112,{'episode':'E04','puzzle':'P11','state':'stable pressure, no death timer'}),
 ('MUS07_RESCUE_COORDINATED',114,'together',WARM,HOME,0,0,112,{'episode':'E04','puzzle':'P11','state':'help accepted'}),
 ('MUS08_MICROPHONE_PREPARATION',115,'precise',PRES,SHOW,-2,0,108,{'episode':'E05','puzzle':'P12','state':'before truth; no future reveal'}),
 ('MUS08_MICROPHONE_HONEST',116,'together',WARM,HOME,0,0,108,{'episode':'E05','puzzle':'P12','state':'truth already committed; use speech-owned gap first'}),
 ('MUS09_THREE_DOORS_ROUTING',117,'courtyard',REPLY,HOME,-7,0,108,{'episode':'E06','puzzle':'P13','state':'routing underway; no answer predicted'}),
 ('MUS09_THREE_DOORS_PROMISES',118,'together',HOME,WARM,0,0,108,{'episode':'E06','puzzles':['P13','P14'],'state':'earned routing, stated promises'}),
 ]
 for spec in specs:
  score=longform(*spec[:8],binding=spec[8])
  if score.name=='MUS04_MILO_SINCERE':
   # The theatrical source appears once as a quieter, intact reminiscence,
   # not three repetitions of its flourish after the character drops the bluff.
   score.annotations.append('Showy source material appears only in the contrasting middle section, surrounded by spacious HOME; the repeated main voice is now restrained guitar.')
  reports.append(score.finish())
 # Quiet ending: complete HOME, then the sustained TOGETHER statement, a
 # source-compatibleC7 link and a spaciousF-major close with deliberate silence.
 s=c.Score('MUS10_HOUSEHOLD_QUIET',119,100,80,False,'quiet')
 s.binding={'episode':'E07','puzzle':'P14','state':'committed ending only'}
 s.motif(HOME,0,32,ch=4,velocity_curve=[57,59,64,62,60,58,55,54])
 s.motif(WARM,36,24,ch=3,velocity_curve=[55,58,62,64,61,56])
 harmony_override(s,60,0,'C7 closing breath');s.tail(64,5,'Fmaj7 quiet close',length=16)
 s.accompany(dropouts=[(32,40),(72,80)],intensity=.67)
 # Last4beats are intentional musical silence after all natural source tails.
 s.notes=[n for n in s.notes if n['unswung_beat']<76];s.annotations.append('Nonlooping ending with final4beats free of note attacks. Source phrase endpoints remain intact; residual release/reverb is natural.')
 reports.append(s.finish())
 s=c.Score('MUS_AUDIENCE_EXPOSED',120,112,36,True,'exposed');s.binding={'state':'HOME-compatible exposed-stage color only; other families use their own reduced mask'}
 s.motif(HOME,0,32,ch=4,velocity_curve=[59,61,65,63,61,59,58,57]);s.tail(32,5,'Fmaj7 breath');s.accompany(dropouts=[(8,16)],intensity=.7);reports.append(s.finish())
 # Full television-style end-credit reprise is required after the quiet tag
 # and separate cleared audience celebration. It is not another puzzle timer.
 s=c.Score('MUS10_FULL_END_CREDITS',121,112,260,False,'courtyard')
 s.binding={'episode':'E07','state':'after GAME_COMPLETE, pencil tag, happy freeze and audience celebration','credit_music':'extended household-theme reprise; pause/skip/replay preserve completion'}
 for j in range(8):
  mid=PRES if j==2 else WARM if j==4 else HOME;tr=-2 if mid==PRES else 0
  s.motif(mid,j*32,32,ch=3 if j%2==0 else 4,transpose=tr,velocity_curve=([65,69,74,75,72,68,65,63]if j in(1,4)else[70,74,80,78,75,72,69,67]),section='CREDIT_REPRISE_'+str(j+1))
  if mid==WARM:harmony_override(s,j*32+24,0,'C7 return to household theme')
 s.tail(256,5,'Fmaj7 final warm release')
 s.accompany(dropouts=[(32,40),(128,140),(224,228)],texture_sections=[(80,96),(176,192),(240,256)],intensity=.97)
 s.annotations.append('Extended65-bar nonlooping reprise for a readable full fictional/actual credit roll. The exact UI roll may pause/skip; music never changes GAME_COMPLETE or repeats a reward. No audience PCM or actual credit names are baked into the MIDI.')
 reports.append(s.finish())
 # Eight bounded links/passages. Narrative ownership is separate from MIDI time.
 link_specs=[
 ('BRIDGE_INVITATION_HOUSE',122,112,HOME,16,16,32,0,{'event':'P02 committed reveal'}),
 ('BRIDGE_EXPLORATION_SUPPER',123,112,HOME,16,16,32,0,{'event':'E03 explicit Ready'}),
 ('BRIDGE_SUPPER_RESCUE',124,110,SHOW,16,12,26,0,{'event':'E04 scene ownership'}),
 ('BRIDGE_MICROPHONE_DOORS',125,108,REPLY,16,11,18,-7,{'event':'E05 complete then E06'}),
 ('BRIDGE_PROMISES_QUIET',126,108,WARM,16,14,22,0,{'event':'P14 committed completion'}),
 ('PASSAGE_RESCUE_RESOLUTION',127,112,WARM,16,14,22,0,{'event':'P11 committed help/completion'}),
 ('PASSAGE_CONFETTI_RESPONSE',128,108,PRES,16,24,32,-2,{'event':'P12 collective response after consequential words'}),
 ]
 for name,num,bpm,mid,beats,offset,limit,tr,binding in link_specs:
  s=c.Score(name,num,bpm,beats,False,'together');s.binding=binding
  sparse_fragment(s,mid,0,offset,limit,12,ch=3,transpose=tr,velocity=65)
  target=5 if num not in(126,)else 5
  harmony_override(s,12,0,'C7 into F');s.accompany(dropouts=[(8,12)],intensity=.77)
  if num==123:s.tempo_map=[{'beat':0,'bpm':112},{'beat':4,'bpm':111},{'beat':8,'bpm':110},{'beat':12,'bpm':110}]
  if num==124:s.tempo_map=[{'beat':0,'bpm':110},{'beat':4,'bpm':111},{'beat':8,'bpm':112},{'beat':12,'bpm':112}]
  if num==126:s.tempo_map=[{'beat':0,'bpm':108},{'beat':4,'bpm':105},{'beat':8,'bpm':102},{'beat':12,'bpm':100}]
  s.annotations.append('This composed serial link is event-owned and never required for puzzle correctness. Tempo changes occur only as authored source events; target scene must match final tempo and harmonic entry.')
  reports.append(s.finish())
 s=c.Score('PASSAGE_SPEECH_SPACE',129,108,32,False,'quiet');s.binding={'event':'P12 consequential words; scene-owned silence may extend'}
 sparse_fragment(s,HOME,0,16,23,8,ch=4,velocity=58)
 s.motif(WARM,20,12,ch=3,source_offset=14,source_limit=22,velocity_curve=[61,61,58])
 harmony_override(s,8,5,'F quiet hold','major');harmony_override(s,20,8,'Abmaj7 source reply','major');s.accompany(dropouts=[(4,24)],intensity=.5)
 s.notes=[n for n in s.notes if not(8<=n['unswung_beat']<20)and not(n['unswung_beat']<8 and n['unswung_beat']+n['unswung_duration']>8)]
 s.speech_windows=[dict(from_beat=8,to_beat=20,policy='Runtime must hold/extend silence until actual consequential speech ends; this fixed excerpt is not a timer or implemented gate.')]
 reports.append(s.finish())
 plan={'status':'FULL_SCORE_CANDIDATES_UNDER_APPROVED_V3_PRINCIPLES_NOT_WHOLE_SOUNDTRACK_ACCEPTANCE','accepted_reference_library_id':'sha256:192eb02dc7996d337e33173b9d921ef70b747b1bdfc4f5ae7e62a7964684c698','source_bundles_used':sorted({u['stem'][:3]for r in reports for u in r['source_motif_uses']}),'principal_states':22,'bridges_and_passages':8,'accepted_audition_bytes_changed':False,'new_insult_family':'MUS11 event-owned action-comedy family is separately composed; see verbal-competition-music-contract.json','cues':[{k:v for k,v in r.items()if k not in('notes','harmony','natural_role_key_windows')}for r in reports]}
 (OUT/'analysis/full-score-plan.json').write_text(json.dumps(plan,indent=2));print('V4 MAIN BANK',len(reports),'resources')
if __name__=='__main__':main()
