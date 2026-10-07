#!/usr/bin/env python3
"""Final candidate index and explicit native transport handoff. No runtime edits."""
import json,hashlib,subprocess
from pathlib import Path
import score_v4_core as c
O=c.OUT
rs=sorted([json.loads(p.read_text())for p in(O/'analysis').glob('*-manifest.json')],key=lambda r:r['resource_id'])
windows=[]
for r in rs:
 if not r.get('loop'):continue
 a,b=r['loop']['start_tick'],r['loop']['end_tick'];period=b-a;channels={}
 for ch,ws in r['natural_role_key_windows'].items():
  intervals=sorted([(max(a,w['first_possible_guard']),min(b,w['last_possible_guard']))for w in ws if min(b,w['last_possible_guard'])>=max(a,w['first_possible_guard'])])
  gaps=[intervals[i+1][0]-intervals[i][1]for i in range(len(intervals)-1)] if intervals else[]
  if intervals:gaps.append(intervals[0][0]+period-intervals[-1][1])
  wait=max(gaps)*16667/1e6 if gaps else None
  channels[ch]={'guard_intervals_native_ticks':intervals,'worst_key_only_wait_seconds':wait,'key_only_not_release_or_reverb_clear':True}
 windows.append({'cue_id':r['cue_id'],'resource_id':r['resource_id'],'loop':r['loop'],'channels':channels})
(O/'analysis/native-transport-handoff.json').write_text(json.dumps({'status':'CANDIDATE_DATA_NOT_NATIVE_TRANSPORT_ACCEPTANCE','timing':'Native tick is16667microseconds; use exact exported ticks, not hardcoded ticks/bar. Wait values use the same16667microsecond tick.','cc11':'Initial controller maps and absolute expression_timeline in each full manifest are authoritative. On seek/restore/remap, reconstruct latest CC11 value at current loop position. SCI trackState/remapChannel do not cache/reapply CC11 automatically.','quiet_companions':'30 reduced references changeCC7 only; one parser/gain-state architecture. Logical note/program/tempo/CC11/loop events identical. Positive-gain transitions require bounded tested ramps. Zero-entry roles need natural key-silent windows plus tested muted-release clearing; these windows alone do not prove silence.','contest':'140 is the persistent contest bed.141–145 areCC7-only reference color/thinking states, never concurrent music players.146–147 reserve ACCENT function and require independent native channel isolation/lifecycle proof; they do not authorize a ninth sounding role or secondPCM lane.','cross_family':'Distinct full states are not phase-equivalent. Use authored phrase bridges/valid musical entry points, with event timing never deciding gameplay. Speech silence must extend for actual consequential speech; fixed MIDI durations are not dialogue timers.','initial_guard':'Each full manifest reports actual first exported note attack separately from loop origin. Section cue markers have no implicit global-safe meaning.','gates':['Stock-runtime channel remap/restore includingCC11','Gain-state reversal and zero-entry release clearing','Actual speech/laughter/foley overlap on onePCM owner','Pause/seek/save/restore/skip/mute, no transient replay','Target-device full-score listening','Targeted listening atHOME-to-minor joins: held-note overlaps removed, release/reverb still needs ears'], 'key_window_reports':windows},indent=2))
index={'status':'CANDIDATE_FULL_SCORE_UNDER_APPROVED_V3_PRINCIPLES_NOT_NATIVE_OR_FULL_LISTENING_ACCEPTANCE','accepted_reference':'sha256:192eb02dc7996d337e33173b9d921ef70b747b1bdfc4f5ae7e62a7964684c698','main_families':'MUS01–MUS10','additional_family':'MUS11_VERBAL_COMPETITIONS','main_principal_states':22,'main_bridges_and_passages':8,'contest_base_colors_thinking':6,'contest_single_fire_punctuations':2,'full_resources':len(rs),'reduced_companions':30,'source_bundles':sorted({u['stem'][:3]for r in rs for u in r.get('source_motif_uses',[])}),'total_scored_seconds':sum(r['duration_seconds']for r in rs),'native_status':'Isolated payloads only; current runtime untouched.','public_delivery':'Neutral track names/metadata. This technical archive contains story and puzzle bindings.','files':[{k:r[k]for k in('cue_id','resource_id','midi_path','native_payload_path','duration_seconds','sha256')}for r in rs]}
(O/'analysis/score-index.json').write_text(json.dumps(index,indent=2))
proof=json.loads((O/'analysis/render-validation.json').read_text());p=proof['profiles'];assert len(p)==106 and all(x['samples_at_or_above_full_scale']==0 and x['final_active_fluid_voices']==0 for x in p)
for x in p:
 if 'file'in x:assert hashlib.sha256((c.ROOT/x['file']).read_bytes()).hexdigest()==x['sha256']
summary={'profiles':len(p),'clipped_samples':sum(x['samples_at_or_above_full_scale']for x in p),'max_active_fluid_voices':max(x['max_active_fluid_voices']for x in p),'all_final_voices_zero':True,'highest_sample_peak_dbfs':max(x['sample_peak_dbfs']for x in p),'highest_4x_peak_dbfs':max(x['oversampled_4x_peak_dbfs']for x in p),'max_held_midi_notes':max(r['max_held_notes']for r in rs),'native_acceptance':False,'full_score_listening_acceptance':False,'accepted_v3_changed':False}
(O/'analysis/validation-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
