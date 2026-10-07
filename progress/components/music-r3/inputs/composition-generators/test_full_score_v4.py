#!/usr/bin/env python3
import unittest,json,math,sys,collections,hashlib
from pathlib import Path
import score_v4_core as c
OUT=c.OUT
class V4Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.rs=sorted([json.loads(p.read_text())for p in(OUT/'analysis').glob('*-manifest.json')],key=lambda r:r['resource_id']);cls.bank=c.sources();cls.raw={}
  for sid in('B01S06','B02S08','B03S06','B04S02','B05S05'):cls.raw[sid]={n['id']:n for n in json.loads((c.OLD/'analysis'/f'{sid}.json').read_text())['notes']}
 def test_accepted_audition_unchanged(self):
  lock=json.loads((OUT/'analysis/accepted-v3-lock.json').read_text())
  for f in lock['files']:self.assertEqual(hashlib.sha256((c.ROOT/f['path']).read_bytes()).hexdigest(),f['sha256'])
 def test_all_eleven_families_and_full_credits(self):
  names=[r['cue_id']for r in self.rs]
  for n in range(1,12):self.assertTrue(any(x.startswith(f'MUS{n:02d}_')for x in names),n)
  self.assertIn('MUS10_FULL_END_CREDITS',names);self.assertGreater(next(r['duration_seconds']for r in self.rs if r['cue_id']=='MUS10_FULL_END_CREDITS'),120)
  self.assertEqual(len(self.rs),38)
 def test_native_source_roundtrip_and_payloads(self):
  for r in self.rs:
   smf=(OUT/r['midi_path']).read_bytes();native=(OUT/r['native_payload_path']).read_bytes();converted,timing=c.g.convert_smf(smf);decoded=c.g.decode_sound(native)
   self.assertEqual(sorted(converted),sorted((t,m)for ch,es in decoded.items()if ch!=15 for t,m in es),r['cue_id']);self.assertLessEqual(max(t['error_us']for t in timing),8333.5);self.assertLess(len(native),65536);self.assertEqual(c.sha(smf),r['sha256']['midi']);self.assertEqual(c.sha(native),r['sha256']['native'])
 def test_balanced_notes_and_role_voice_budgets(self):
  for r in self.rs:
   decoded=c.g.decode_sound((OUT/r['native_payload_path']).read_bytes());profile=c.d.held_profile(decoded);self.assertLessEqual(max(n for _,n in profile),18)
   active=set();peaks=collections.Counter()
   for t,ch,msg in sorted(((t,ch,m)for ch,es in decoded.items()for t,m in es),key=lambda x:(x[0],0 if x[2][0]&240==128 else 1)):
    if msg[0]&240==144 and msg[2]:active.add((ch,msg[1]));peaks[ch]=max(peaks[ch],sum(k==ch for k,p in active))
    elif msg[0]&240==128:active.discard((ch,msg[1]))
   for role in r['roles']:self.assertLessEqual(peaks[role['channel']],role['voices'],(r['cue_id'],role,peaks))
   self.assertLessEqual(sum(x['voices']for x in r['roles']),24)
 def test_every_melody_note_traces_to_original_pitch(self):
  bundles=set()
  for r in self.rs:
   if 'notes'not in r:continue
   for n in r['notes']:
    s=n.get('source')
    if not s:continue
    original=self.raw[s['stem']][s['source_note_id']];self.assertEqual(original['pitch'],s['source_pitch']);self.assertEqual(original['beat'],s['source_beat']);self.assertEqual(n['pitch'],original['pitch']+s['transposition']);bundles.add(s['stem'][:3])
  self.assertEqual(bundles,{'B01','B02','B03','B04','B05'})
 def test_source_rhythm_and_harmony_follow_same_grid(self):
  for r in self.rs:
   if 'notes'not in r:continue
   origin=(r['initial_guard']['attack_tick']*.016667*r['bpm']/60)if r['resource_id']!=100 else 0
   # Exact source ticks determine actual origin more accurately than native
   # quantized time; infer it from one note and its unswung coordinate.
   origin=r['notes'][0]['beat']-c.sw(r['notes'][0]['unswung_beat'],r['swing_offbeat_fraction'])
   for n in r['notes']:
    self.assertAlmostEqual(n['beat'],origin+c.sw(n['unswung_beat'],r['swing_offbeat_fraction']),places=6)
    s=n.get('source')
    if not s:continue
    grid=c.eighth_grid(self.bank[s['motif']]);self.assertEqual(s['source_grid_beat'],grid[s['source_note_id']])
    matching=[u for u in r['source_motif_uses']if u['motif']==s['motif']and u['channel']==n['channel']and u['transpose']==s['transposition']and abs(u['start_beat']+(s['source_grid_beat']-u['source_offset'])*u['scale']-n['unswung_beat'])<.00001]
    self.assertTrue(matching,(r['cue_id'],s))
   for h in r.get('harmony',[]):
    if 'source_motif'not in h:continue
    source_h=[x for x in self.bank[h['source_motif']]['harmony']if abs(c.harmony_grid(x)-h['source_harmony_beat'])<.00001]
    self.assertTrue(source_h);self.assertEqual(h['root_pc'],(source_h[0]['root_pc']+h['transposition'])%12)
 def test_no_double_swing_or_invented_third(self):
  m=self.bank['TOGETHER_B'];self.assertTrue(m['rhythm']['source_already_ternary']);grid=c.eighth_grid(m);self.assertEqual(grid[412],0);self.assertAlmostEqual(grid[536],16.5)
  h=next(h for h in m['harmony']if h['quality']=='ambiguous_third');self.assertEqual(set(c.dyad_pcs(h)),{11,6})
  q=next(h for h in m['harmony']if h['quality']=='minor_major7');self.assertEqual(set(c.dyad_pcs(q)),{3,11})
 def test_no_guard_chop_and_natural_loop_tails(self):
  for r in self.rs:
   if 'notes'not in r:continue
   self.assertTrue(all(not n.get('source',{}).get('guard_continuation')for n in r['notes']if n.get('source')))
   for cue in r['section_cues']:self.assertFalse(cue['is_global_safe_gate'])
   if r['loop']:self.assertGreater(r['loop']['natural_key_release_before_end_ticks'],0)
 def test_expression_timeline_and_initial_state_explicit(self):
  for r in self.rs:
   if 'notes'not in r:continue
   self.assertIn('cc11',r['initial_controllers']['3']);self.assertIn('cc11',r['initial_controllers']['4']);self.assertTrue(r['expression_timeline'])
   for e in r['expression_timeline']:self.assertEqual(e['controller'],11);self.assertGreaterEqual(e['native_tick'],0)
 def test_quiet_companions_exact_clock(self):
  qs=json.loads((OUT/'analysis/reduced-variants.json').read_text())['variants'];self.assertEqual(len(qs),30)
  strip=lambda x:{ch:[(t,m)for t,m in es if not(m[0]&240==176 and m[1]==7)]for ch,es in x.items()}
  for q in qs:
   r=next(r for r in self.rs if r['cue_id']==q['cue_id']);full=c.g.decode_sound((OUT/r['native_payload_path']).read_bytes());low=c.g.decode_sound((OUT/q['native_payload_path']).read_bytes());self.assertEqual(strip(full),strip(low));cv,_=c.g.convert_smf((OUT/q['midi_path']).read_bytes());self.assertEqual(sorted(cv),sorted((t,m)for ch,es in low.items()if ch!=15 for t,m in es))
 def test_contest_colors_same_one_clock(self):
  base=next(r for r in self.rs if r['resource_id']==140);strip=lambda x:{ch:[(t,m)for t,m in es if not(m[0]&240==176 and m[1]==7)]for ch,es in x.items()};a=strip(c.g.decode_sound((OUT/base['native_payload_path']).read_bytes()))
  for num in range(141,146):
   r=next(r for r in self.rs if r['resource_id']==num);self.assertEqual(a,strip(c.g.decode_sound((OUT/r['native_payload_path']).read_bytes())));self.assertTrue(r['phase_equivalence']['same_program_note_tempo_expression_and_loop_events'])
 def test_contest_events_and_single_pcm_constraints(self):
  r=json.loads((OUT/'analysis/verbal-competition-music-contract.json').read_text());self.assertEqual(set(r['encounters']),{'VC01','VC02','VC03','VC04'});self.assertEqual(set(r['events']),{'VC_ENTER','VC_TURN','VC_RESPONSE_COMMITTED','VC_KO_COMMITTED','VC_EXIT'})
  for num in(146,147):
   x=next(r for r in self.rs if r['resource_id']==num);self.assertIn('serial',x['gdd_binding']['single_fire_key']);self.assertEqual(x['roles'][0]['channel'],7);self.assertIn('reserved',x['routing'].lower())
 def test_protected_speech_and_quiet_end(self):
  speech=next(r for r in self.rs if r['resource_id']==129)
  self.assertFalse([n for n in speech['notes']if 8<=n['unswung_beat']<20]);self.assertFalse([n for n in speech['notes']if n['unswung_beat']<8 and n['unswung_beat']+n['unswung_duration']>8])
  ending=next(r for r in self.rs if r['resource_id']==119);self.assertIsNone(ending['loop']);self.assertFalse([n for n in ending['notes']if n['unswung_beat']>=76])
 def test_reviewed_inversions_diminished_fifths_and_arrivals(self):
  for r in self.rs:
   if 'notes'not in r:continue
   effective={h['beat']:h for h in r['harmony']}
   for beat,h in effective.items():
    if beat>=r['beats']:continue
    shells=[n for n in r['notes']if n['channel']==1 and abs(n['unswung_beat']-beat)<.001]
    if shells and h.get('bass_pc',h['root_pc'])!=h['root_pc'] and h['quality'].startswith('major'):
     self.assertIn(h['root_pc'],{n['pitch']%12 for n in shells},(r['cue_id'],beat,h))
    if shells and 'diminished'in h['quality']:
     self.assertIn((h['root_pc']+6)%12,{n['pitch']%12 for n in shells},(r['cue_id'],beat,h))
  routing=next(r for r in self.rs if r['resource_id']==117)
  at=lambda beat:[n['pitch']%12 for n in routing['notes']if n['channel']==0 and abs(n['unswung_beat']-beat)<.001]
  self.assertEqual(at(5),[2]);self.assertEqual(at(6),[8])
  speech=next(r for r in self.rs if r['resource_id']==129)
  shell={n['pitch']%12 for n in speech['notes']if n['channel']==1 and n['unswung_beat']==24}
  self.assertEqual(shell,{0,7}) # Abmaj7 third/seventh, not dominantGb
 def test_reviewed_minor_family_joins_and_initial_attack(self):
  for r in self.rs:
   if 'notes'not in r:continue
   decoded=c.g.decode_sound((OUT/r['native_payload_path']).read_bytes())
   first=min(t for ch,es in decoded.items()if ch!=15 for t,m in es if m[0]&240==144 and m[2])
   self.assertEqual(r['initial_guard']['attack_tick'],first);self.assertGreater(first,r['initial_guard']['guard_tick'])
   effective={h['beat']:h for h in r['harmony']}
   for beat,h in effective.items():
    if not h['quality'].startswith('minor'):continue
    bad=[n for n in r['notes']if n.get('source') and n['source']['motif']=='HOME_A' and n['pitch']%12==(h['root_pc']+11)%12 and n['unswung_beat']<beat and n['unswung_beat']+n['unswung_duration']>beat]
    self.assertFalse(bad,(r['cue_id'],beat))
 def test_individual_acceptance_not_overclaimed(self):
  for r in self.rs:self.assertFalse(r['validation']['native_runtime_tested']);self.assertFalse(r['validation']['human_listening_approved'])
if __name__=='__main__':unittest.main()
