from support import *
from save_fixture import SaveVM,full_fixture,load_earlier
import types
class Revision3SaveProof(Scenario):
 @classmethod
 def setUpClass(cls):
  cls.base=full_fixture()
 def max_generation(self,v,lo=32767):
  a=v.arrays(943);a['rbGenerationHi'][0]=32767;a['rbGenerationLo'][0]=lo
 def frame(self,v,n=2):v.advance(n);return v.objects['cakood'].call('audioPoll',n)
 def capture(self,v,result=1):
  v.saves=[];v.save_result=result;v.objects['cakood'].call('writeSave');return v.saves[0]if v.saves else None
 def assert_refused(self,v):
  h=v.objects['cakood'];before=list(v.domain_words());h.p['audioSaveResult']=1;v.saves=[]
  self.assertEqual(h.call('writeSave'),0);self.assertFalse(v.saves);self.assertEqual(h.p['audioSaveResult'],0);self.assertEqual(h.p['dirty'],1)
  self.assertEqual(list(v.domain_words()),before);self.assertEqual(v.status(7),0)
  v.paint.clear();h.call('render');self.assertIn('SAVE UNAVAILABLE: MUSIC LIFETIME LIMIT.',v.paint)
 def last_saved(self):
  v=self.vm();self.max_generation(v,32766);saved=self.capture(v);self.assertIsNotNone(saved);self.assertEqual(v.objects['cakood'].p['audioSaveResult'],1);return v,saved
 def assert_replayed(self,z,saved):
  h=z.objects['cakood'];self.assertEqual((z.status(3),z.status(4),z.status(7),z.status(8)),(32767,32767,0,0));self.assertEqual(z.status(5),0)
  self.assertEqual(h.p['uiFailure'],0);self.assertEqual(z.objects['p05State'].p['hFailure'],0)
  for mod,name in[(0,'replay'),(0,'p05RestoreBegin'),(0,'p05RetireTransient'),(0,'p05RestoreValidate'),(0,'eventLoop'),(985,'hRestoreBegin'),(985,'hRestoreValidate'),(986,'vcAfterRestore')]:self.assertGreater(z.calls[mod,name],saved.calls[mod,name],(mod,name))
  self.assertEqual(list(z.domain_words()),list(saved.domain_words()));self.assertEqual(z.max_parsers,1);self.assertEqual(z.status(19),saved.status(19));self.assertEqual(z.status(16),saved.status(16));self.assertEqual(z.status(17),saved.status(17))
 def test_01_actual_committed_ceiling_refuses_before_native_save(self):
  v=self.vm();d=v.objects['contestState'];w=v.domain_words();w[6]=1
  for i in range(10,22):w[i]=1
  self.assertEqual(d.call('vcEnter',1,0,7,1),1);self.assertEqual(d.call('vcCommit'),1);self.assertEqual(v.proc('rbHostCommitted',3,d),1);self.assertEqual(d.call('vcSaveReady'),1)
  # Match the independent emitted Main fixture: real986, no synthetic scene admission.
  v.objects['cakood'].p.update(p05=0,p04=0)
  self.max_generation(v);self.assertEqual(v.proc('rbRequest',151),0);self.assertEqual(v.status(5),9)
  parser=v.parsers[v.objects['responsiveSound']];self.assert_refused(v);self.assertIs(v.parsers[v.objects['responsiveSound']],parser)
 def test_02_ceiling_without_failed_request_has_honest_save_overlay(self):
  v=self.vm();self.max_generation(v);h=v.objects['cakood'];self.assertEqual(v.status(5),0);self.assert_refused(v)
  self.assertEqual(v.proc('rbUiState'),1);self.assertEqual(h.p['musicUnavailable'],0)
  h.p.update(type=4,message=114);h.call('input');self.assertEqual((v.status(3),v.status(4),v.status(5)),(32767,32767,0));self.assert_refused(v)
 def test_03_last_admissible_save_actual_restore_entry_and_resume(self):
  v,saved=self.last_saved();pos=saved.parsers[saved.objects['responsiveSound']]['tick'];z=load_earlier(v,saved);self.assert_replayed(z,saved)
  self.assertIn('responsiveSound',v.native_restore_retired);self.assertFalse(v.parsers);self.assertEqual(z.parsers[z.objects['responsiveSound']]['tick'],pos)
  for _ in range(8):self.frame(z)
  self.assertGreater(z.parsers[z.objects['responsiveSound']]['tick'],pos);self.assert_refused(z)
 def test_04_repeated_earlier_loads_preserve_snapshot_lifetime(self):
  v,saved=self.last_saved()
  for _ in range(3):
   self.max_generation(v);self.assertEqual(v.proc('rbAdvanceGeneration'),0);self.assert_refused(v)
   v=load_earlier(v,saved);self.assert_replayed(v,saved);self.assertEqual(v.proc('rbSaveAdmit'),0)
 def test_05_save_cancel_retry_then_successful_full_restore(self):
  v=self.vm();self.max_generation(v,32766);p=v.parsers[v.objects['responsiveSound']];pos=p['tick']
  canceled=self.capture(v,0);self.assertIsNotNone(canceled);self.assertEqual(v.objects['cakood'].p['audioSaveResult'],0);self.assertEqual(v.status(7),0);self.assertEqual(v.status(4),32766);self.assertIs(v.parsers[v.objects['responsiveSound']],p);self.assertEqual(p['tick'],pos)
  saved=self.capture(v,1);self.assertEqual(v.objects['cakood'].p['audioSaveResult'],1);self.assert_replayed(load_earlier(v,saved),saved)
 def test_06_refused_save_load_cancel_and_retry_never_reset_generation(self):
  v=self.vm();self.max_generation(v);v.proc('rbAdvanceGeneration');h=v.objects['cakood'];self.assert_refused(v);p=v.parsers[v.objects['responsiveSound']];pos=p['tick']
  for _ in range(2):
   h.call('readSave');self.assertEqual(v.status(7),0);self.assertEqual(v.status(4),32767);self.assertEqual(v.status(5),9);self.assertIs(v.parsers[v.objects['responsiveSound']],p);self.assertEqual(p['tick'],pos);self.assertEqual(h.call('musicRetry'),0);self.assert_refused(v)
  self.assertEqual(v.load_calls,2)
 def test_07_retired_failed_owner_can_cancel_or_load_earlier_save(self):
  v,saved=self.last_saved();self.max_generation(v);v.proc('rbAdvanceGeneration');v.proc('rbFail',9);self.assertFalse(v.parsers);self.assertEqual(v.status(1),3);self.assert_refused(v)
  v.objects['cakood'].call('readSave');self.assertEqual(v.load_calls,1);self.assertEqual(v.status(7),0);self.assertFalse(v.parsers);self.assertEqual(v.status(5),9)
  z=load_earlier(v,saved);self.assert_replayed(z,saved);self.assertEqual(v.load_calls,2)
 def test_08_load_recovery_and_save_keep_fresh_guards(self):
  v,saved=self.last_saved();self.max_generation(v);v.proc('rbAdvanceGeneration');v.proc('rbFail',9)
  b=bytearray(v.resources[3,247]);b[0]=ord('x');v.resources[3,247]=bytes(b)
  self.assertEqual(v.objects['cakood'].call('readSave'),0);self.assertEqual(v.load_calls,0);self.assertFalse(v.parsers);self.assertEqual(v.status(7),0)
  u=self.vm();self.max_generation(u,32766);u.objects['cakood'].p['audioSaveResult']=1;u.resources[3,247]=bytes(b);u.objects['cakood'].call('writeSave');self.assertFalse(u.saves);self.assertEqual(u.objects['cakood'].p['audioSaveResult'],0)
  u=self.vm();self.max_generation(u);u.arrays(943)['rbSaveRefused'][0]=0;self.assert_refused(u)
  u=self.vm();u.arrays(943)['rbSaveRefused'][0]=2;self.assertEqual(u.proc('rbValidate'),0)
 def test_09_exact_original_success_unrestorable_counterexample_pinned(self):
  report=json.loads((H/'inputs/revision2/independent-review/exhausted-save-probe.json').read_text())
  self.assertEqual((report['domain_save_ready'],report['save_kernel_entered'],report['save_result'],report['saved_music_validate'],report['restore_begin_return']),(1,1,1,1,0))

  old=json.loads((H/'inputs/revision2/api-r2.json').read_text());new=json.loads((H/'generated/api.json').read_text())
  for module,api in old.items():
   for name,index in api.items():self.assertEqual(new[module][name],index,(module,name))
