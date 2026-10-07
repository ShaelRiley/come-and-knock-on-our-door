from support import *
import generate
class TransportProof(Scenario):
 def test_01_one_slot_serial_retire_start_and_all_five_bridges(self):
  for source,bridge in((151,148),(151,153),(152,149),(152,150),(152,154)):
   v=self.vm()if source==151 else self.contest_vm();d,w=self.enter(v)if source==151 else (v.objects['contestState'],v.domain_words());gate=next(g for g in generate.manifest(source)['gates']if g['bridge_resource']==bridge)
   if source==152:v.proc('rbRequest',151)
   t,p=self.staged_position(v,source,(gate['dispatch_first']+1)//2*2)
   self.assertEqual(v.poll(),1);self.assertEqual(v.status(0),bridge);self.assertEqual(v.max_parsers,1)
   before=v.status(19);self.arrive(v,152 if source==151 else 151);self.assertEqual(v.max_parsers,1);self.assertEqual(v.status(19),before+1)
   ops=[row[1]for row in v.sound_trace]
   for index,op in enumerate(ops):
    if op==6 and index: self.assertEqual(ops[index-2:index],[9,7])
   self.assertTrue(all(row[2]=='responsiveSound'for row in v.sound_trace))
 def test_02_cancel_before_gate_preserves_clock_and_no_new_parser(self):
  v=self.vm();d,w=self.enter(v);clock=v.parsers[v.objects['responsiveSound']];v.proc('rbRequest',151);self.tick(v,300)
  self.assertIs(v.parsers[v.objects['responsiveSound']],clock);self.assertEqual(v.status(19),1);self.assertEqual(v.status(18),0)
 def test_03_reverse_during_bridge_uses_latest_target(self):
  v=self.vm();self.enter(v);self.bridge(v);old=v.status(0);self.assertEqual(v.proc('rbRequest',151),1);self.arrive(v,151)
  self.assertEqual(v.status(19),3);self.assertNotIn(152,[r[3]for r in v.sound_trace if r[1]==6]);self.assertIn(old,(148,153))
 def test_04_repeated_reversals_and_new_context_do_not_replay_bridge(self):
  v=self.vm();d,w=self.enter(v);self.bridge(v)
  for _ in range(8):v.proc('rbRequest',151);v.proc('rbRequest',152)
  self.arrive(v,152);self.assertEqual(v.status(19),3);self.assertEqual(v.max_parsers,1)
 def test_05_all_apertures_have_actual_double_read_admission(self):
  count=0
  for source in(151,152):
   for gate in generate.manifest(source)['gates']:
    v=self.vm()if source==151 else self.contest_vm()
    if source==151:self.enter(v)
    if source==152:v.proc('rbRequest',151)
    self.staged_position(v,source,(gate['dispatch_first']+1)//2*2)
    before=len(v.sound_trace);self.assertEqual(v.poll(),1);self.assertEqual(v.status(0),gate['bridge_resource']);count+=1
    retired=[r[1]for r in v.sound_trace[before:]];self.assertGreaterEqual(retired.count(17),3)
  self.assertEqual(count,35)
 def test_06_second_read_outside_gate_preserves_source(self):
  v=self.vm();d,w=self.enter(v);gate=generate.manifest(151)['gates'][0];t,p=self.staged_position(v,151,gate['dispatch_first'])
  reads=[0]
  def delayed(vm,obj):
   reads[0]+=1
   if reads[0]==2:vm.parsers[obj]['tick']=gate['dispatch_last']+4
  v.after_read=delayed;self.assertEqual(v.poll(),0);self.assertEqual(v.status(0),151);self.assertEqual(v.status(18),0)
 def test_07_every_missed_aperture_rejects_late_cut(self):
  for source in(151,152):
   for gate in generate.manifest(source)['gates']:
    v=self.vm()if source==151 else self.contest_vm()
    if source==151:self.enter(v)
    if source==152:v.proc('rbRequest',151)
    self.staged_position(v,source,(gate['dispatch_last']+4)//2*2)
    self.assertEqual(v.poll(),0);self.assertEqual(v.status(0),source)
 def test_08_missed_frames_degrade_without_gameplay_block(self):
  v=self.vm();self.enter(v);v.advance(80);v.poll();self.assertEqual(v.status(6),1)
  self.assertEqual(v.status(0),151);self.assertEqual(v.status(5),0);self.assertLess(v.steps,100000000)
 def test_09_mute_pause_and_preferences_keep_one_clock(self):
  v=self.vm();self.enter(v);v.proc('rbPreference',63,0,1);pos=v.parsers[v.objects['responsiveSound']]['tick'];self.tick(v,1000)
  self.assertEqual(v.parsers[v.objects['responsiveSound']]['tick'],pos);self.assertEqual(v.status(0),151)
  v.proc('rbPreference',44,1,0);self.tick(v,400);self.assertEqual(v.status(0),151);self.assertEqual(v.parsers[v.objects['responsiveSound']]['volume'],0)
  v.proc('rbPreference',44,0,0);self.arrive(v);self.tick(v,8);self.assertEqual(v.status(20),44);self.assertEqual(v.parsers[v.objects['responsiveSound']]['volume'],44)
 def test_10_bridge_pause_and_muted_eot_never_replay(self):
  v=self.vm();self.enter(v);self.bridge(v);v.proc('rbPreference',35,0,1);pos=v.parsers[v.objects['responsiveSound']]['tick'];self.tick(v,1000)
  self.assertEqual(v.parsers[v.objects['responsiveSound']]['tick'],pos);v.proc('rbPreference',27,1,0);self.arrive(v);self.assertEqual(v.parsers[v.objects['responsiveSound']]['volume'],0)
  v.proc('rbPreference',27,0,0);self.tick(v,200);self.assertEqual(v.status(19),3)
 def test_11_bridge_does_not_finish_on_keys_or_early_signal(self):
  v=self.vm();self.enter(v);self.bridge(v);p=v.parsers[v.objects['responsiveSound']];p['keys'].clear();self.tick(v,20);self.assertEqual(v.status(1),2)
  p['signal']=255;v.poll();self.assertEqual(v.status(1),3);self.assertEqual(v.status(5),4)
 def test_12_context_loss_cannot_resurrect_contest(self):
  v=self.vm();d,w=self.enter(v);self.bridge(v);w[3]+=1;v.poll();self.assertEqual(v.status(2),151);self.arrive(v,151)
  self.assertNotIn(152,[r[3]for r in v.sound_trace if r[1]==6])
 def test_13_startup_rows_all_six_and_reversal_no_restart(self):
  for n in range(1,5):
   v=self.vm();d,w=self.enter(v,n);self.arrive(v);self.tick(v,6)
   table=json.loads((H/'generated/152-tables.json').read_text())['tables'];self.assertEqual(list(v.arrays(942)['currentGains']),table['stateGains'][8*n:8*n+8])
   starts=v.status(19);w[92]=3;w[99]=1;v.proc('rbEvent',2,d,1);self.tick(v,80);self.assertEqual(list(v.arrays(942)['currentGains']),table['stateGains'][40:48])
   v.proc('rbEvent',2,d,0);self.tick(v,80);self.assertEqual(v.status(19),starts)
 def test_14_startup_wrong_resource_prior_owner_and_offline_gate(self):
  v=MusicVM();self.assertEqual(v.proc('rbInit',v.objects['responsiveSound'],0,0,1),0)
  v.objects['musicTransport'].p['musicRunning']=1;self.assertEqual(v.proc('rbInit',v.objects['responsiveSound'],v.objects['musicTransport'],0,17061),0)
  self.assertEqual(v.proc('rbInit',v.objects['responsiveSound'],0,1,17061),0);self.assertFalse(v.parsers)
 def test_15_no_reserved_accent_or_global_synth_operations(self):
  v=self.vm();self.enter(v);self.arrive(v);self.tick(v,100)
  self.assertFalse([row for row in v.midi if row[3]==7]);self.assertFalse([row for row in v.sound_trace if row[3]in(146,147)])
  self.assertLessEqual({row[1]for row in v.sound_trace},{6,7,8,9,10,14,16,17,18})

 def test_16_superseded_intent_between_reads_never_retires_source(self):
  v=self.vm();d,w=self.enter(v);gate=generate.manifest(151)['gates'][0];self.staged_position(v,151,gate['dispatch_first']);reads=[0]
  def supersede(vm,obj):
   reads[0]+=1
   if reads[0]==2:vm.proc('rbRequest',151)
  v.after_read=supersede;self.assertEqual(v.poll(),0);self.assertEqual(v.status(0),151);self.assertEqual(v.status(18),0)

 def test_17_latest_home_row_survives_contest_and_bridge(self):
  v=self.vm();self.assertEqual(v.proc('rbHomeRequest',1),1);self.tick(v,100);self.assertEqual(v.objects['homeReadyTransport'].p['nextRequestedState'],1)
  d,w=self.enter(v);self.bridge(v);self.assertEqual(v.proc('rbHomeRequest',0),1);self.assertEqual(v.proc('rbHomeRequest',1),1);v.proc('rbRequest',151);self.arrive(v,151);self.tick(v,6)
  table=json.loads((H/'generated/151-tables.json').read_text())['tables'];self.assertEqual(list(v.arrays(941)['currentGains']),table['stateGains'][8:16]);self.assertEqual(v.max_parsers,1);self.assertEqual(v.status(19),3)
  self.assertEqual(v.proc('rbHomeRequest',2),0)
