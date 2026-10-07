from support import *
class RestoreProof(Scenario):
 def test_01_bed_chooser_cancel_once_clock_and_preferences(self):
  v=self.vm();self.enter(v);v.proc('rbPreference',57,0,0);self.assertEqual(v.proc('rbBeforeChooser'),1)
  sound=v.objects['responsiveSound'];pos=v.parsers[sound]['tick'];self.tick(v,1800);self.assertEqual(v.parsers[sound]['tick'],pos)
  self.assertEqual(v.proc('rbBeforeChooser'),0);v.proc('rbPreference',43,0,0);self.assertEqual(v.proc('rbAfterChooser'),1);self.assertEqual(v.proc('rbAfterChooser'),0)
  self.assertEqual(v.status(20),43);self.assertEqual(v.status(19),1)
 def test_02_bridge_chooser_cancel_keeps_exact_parser_once(self):
  v=self.vm();self.enter(v);self.bridge(v);self.tick(v,30);sound=v.objects['responsiveSound'];p=v.parsers[sound];pos=p['tick'];keys=dict(p['keys'])
  self.assertEqual(v.proc('rbBeforeChooser'),1);self.tick(v,3600);self.assertEqual(p['tick'],pos);self.assertEqual(p['keys'],keys)
  v.proc('rbPreference',39,0,0);self.assertEqual(v.proc('rbAfterChooser'),1);self.assertIs(v.parsers[sound],p);self.assertEqual(p['volume'],39);self.assertEqual(v.status(19),2)
 def test_03_pending_response_suppressed_on_restore(self):
  v=self.vm();d,w=self.enter(v);w[92]=3;w[99]=1;v.proc('rbEvent',2,d,1);w[92]=5;w[95]=1
  self.assertEqual(v.status(16),0);self.assertEqual(v.proc('rbBeforeChooser'),1);pos=v.parsers[v.objects['responsiveSound']]['tick']
  self.assertEqual(v.proc('rbRestoreBegin',v.objects['responsiveSound']),1);self.assertEqual(v.proc('rbEvent',3,d,0),0)
  self.assertEqual(v.proc('rbRestoreResume',d),1);self.assertEqual(v.status(13),1);self.assertEqual(v.status(16),0);self.assertEqual(v.proc('rbEvent',3,d,0),0)
  self.assertEqual(v.parsers[v.objects['responsiveSound']]['tick'],pos);self.assertEqual(v.status(19),1)
 def test_04_pending_ko_suppressed_no_replay(self):
  v=self.vm();d,w=self.enter(v);w[92]=7;w[101]=1;w[102]=1;w[96]=0
  self.assertEqual(v.proc('rbBeforeChooser'),1);self.assertEqual(v.proc('rbRestoreBegin',v.objects['responsiveSound']),1);self.assertEqual(v.proc('rbRestoreResume',d),1)
  self.assertEqual(v.status(14),1);self.assertEqual(v.status(17),0);self.assertEqual(v.proc('rbEvent',4,d,0),0)
 def test_05_bridge_restore_retires_before_dispatch_and_never_replays(self):
  v=self.vm();d,w=self.enter(v);self.bridge(v);old=v.status(0);v.proc('rbPreference',52,1,0);self.assertEqual(v.proc('rbBeforeChooser'),1)
  self.assertEqual(v.proc('rbRestoreBegin',v.objects['responsiveSound']),1);self.assertEqual(v.status(0),0);self.assertFalse(v.parsers);self.assertEqual(v.poll(),0)
  self.assertEqual(v.proc('rbRestoreResume',d),1);self.assertEqual(v.status(0),152);self.assertEqual(v.status(19),3);self.assertEqual(v.parsers[v.objects['responsiveSound']]['volume'],0)
  self.assertEqual(sum(r[1]==6 and r[3]==old for r in v.sound_trace),1);self.assertEqual(v.max_parsers,1)
 def test_06_fresh_static_corruption_and_saved_flag_cannot_bypass(self):
  for resource in(245,246,247):
   v=self.vm();self.enter(v);v.proc('rbBeforeChooser');data=bytearray(v.resources[3,resource]);data[0]=ord('x');v.resources[3,resource]=bytes(data)
   self.assertEqual(v.proc('rbRestoreBegin',v.objects['responsiveSound']),0);self.assertFalse(v.parsers);self.assertEqual(v.status(1),3)
 def test_07_saved_mutable_admission_rejects_each_family(self):
  changes=[(943,'rbDesired',999),(943,'rbWhole',101),(943,'rbMuted',2),(943,'rbResponse',4),(943,'rbChooser',2),(943,'rbHighwater',7),(941,'currentGains',128),(941,'targetGains',-1)]
  for mod,name,value in changes:
   v=self.vm();self.enter(v);v.arrays(mod)[name][0]=value;self.assertEqual(v.proc('rbValidate'),0,(mod,name))
 def test_08_saved_owner_property_ranges_and_consistency(self):
  for name,value in [('ownedBed',0),('musicPosition',4255),('transportMode',10),('wholeGain',101),('pausedCheckpoint',1),('rejoinWindow',32767),('recoveryBed',1)]:
   v=self.vm();v.objects['homeReadyTransport'].p[name]=value;self.assertEqual(v.proc('rbValidate'),0,name)
 def test_09_saved_ledger_ahead_of_committed_domain_rejected(self):
  v=self.vm();d,w=self.enter(v);w[92]=3;w[99]=1;v.proc('rbEvent',2,d,1);w[92]=5;w[95]=1;v.proc('rbEvent',3,d,0)
  v.proc('rbBeforeChooser');self.assertEqual(v.proc('rbRestoreBegin',v.objects['responsiveSound']),1);w[95]=0;w[99]=0
  self.assertEqual(v.proc('rbRestoreResume',d),0);self.assertEqual(v.status(1),3)
 def test_10_repeated_snapshot_restore_retirement_is_not_saved_uniqueness(self):
  v=self.vm();d,w=self.enter(v);self.bridge(v);v.proc('rbBeforeChooser');snapshot=copy.deepcopy(v)
  for _ in range(3):
   restored=copy.deepcopy(snapshot);d=restored.objects['contestState'];self.assertEqual(restored.proc('rbRestoreBegin',restored.objects['responsiveSound']),1);self.assertFalse(restored.parsers)
   self.assertEqual(restored.proc('rbRestoreResume',d),1);self.assertEqual(restored.status(19),3);self.assertEqual(restored.max_parsers,1)

 def test_11_disabled_flag_cannot_hide_saved_owner(self):
  v=self.vm();v.proc('rbBeforeChooser');v.arrays(943)['rbEnabled'][0]=0
  self.assertEqual(v.proc('rbRestoreBegin',v.objects['responsiveSound']),0);self.assertFalse(v.parsers);self.assertEqual(v.status(1),3)
 def test_12_unknown_owner_rejected_before_property_dispatch(self):
  v=self.vm();v.arrays(943)['rbOwner'][0]=999
  self.assertEqual(v.proc('rbValidate'),0)
