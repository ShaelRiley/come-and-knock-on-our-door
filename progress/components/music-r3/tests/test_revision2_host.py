from support import *
import generate,types
class Revision2HostProof(Scenario):
 @classmethod
 def setUpClass(cls):
  v=MusicVM('p05-composition');h=v.objects['cakood'];s=v.objects['responsiveSound']
  if v.proc('rbInit',s,v.objects['musicTransport'],0,17061)!=1:raise RuntimeError('Host admission failed')
  h.p.update(opening=0,audioReady=1,masterVolume=61,musicMuted=0,paused=0,menuOpen=0,audioDuckTicks=0,audioDesired=0,onApron=0,location=1,p05=0,p04=0)
  for _ in range(3):v.advance(2);h.call('audioPoll',2)
  cls.base=v
 def committed_enter(self,v):
  d=v.objects['contestState'];d.call('vcInit');d.call('vcBindGeneration',0,1);w=v.domain_words();w[6]=1
  for i in range(10,22):w[i]=1
  self.assertEqual(d.call('vcEnter',1,0,7,1),1);self.assertEqual(d.call('vcCommit'),1);before=list(w)
  self.assertEqual(v.proc('rbHostCommitted',3,d),1);self.assertEqual(list(w),before)
  return d,w
 def frame(self,v,n=2):v.advance(n);return v.objects['cakood'].call('audioPoll',n)
 def paint(self,v):
  v.paint.clear();v.objects['cakood'].call('render');return list(v.paint)
 def to_bridge(self,v):
  for _ in range(2400):
   if v.status(1)==2:return
   self.frame(v)
  self.fail('Connector never arrived')
 def ceiling(self,v):
  a=v.arrays(943);a['rbGenerationHi'][0]=32767;a['rbGenerationLo'][0]=32767
 def test_01_inactive_admission_keeps_original_lane_and_footer(self):
  v=MusicVM('p05-composition');h=v.objects['cakood'];h.p.update(opening=0,audioReady=0,location=1,p05=0,p04=0,menuOpen=0)
  self.assertEqual(v.proc('rbInit',v.objects['responsiveSound'],0,0,1),0)
  h.call('audioPoll',2);self.assertEqual(v.proc('rbUiState'),0);self.assertEqual(h.p['musicUnavailable'],0);self.assertFalse(v.parsers)
  self.assertFalse(any('MUSIC 'in x for x in self.paint(v)))
  h.p['musicUnavailable']=1;self.assertIn('MUSIC UNAVAILABLE. R TO RETRY.',self.paint(v))
 def test_02_committed_pending_is_not_unavailable_or_retryable(self):
  v=self.vm();d,w=self.committed_enter(v);h=v.objects['cakood'];before=list(w);h.call('audioPoll',2)
  self.assertEqual((v.status(0),v.status(2),v.status(5)),(151,152,0));self.assertEqual(h.p['musicUnavailable'],0)
  self.assertEqual(v.proc('rbUiState'),2);self.assertEqual(h.call('musicRetry'),0)
  paint=self.paint(v);self.assertIn('MUSIC CHANGE PENDING.',paint);self.assertFalse(any('UNAVAILABLE'in x or'R TO RETRY'in x for x in paint))
  self.assertEqual(list(w),before);self.assertEqual(v.status(19),1)
 def test_03_running_connector_has_honest_footer(self):
  v=self.vm();self.committed_enter(v);self.to_bridge(v);h=v.objects['cakood'];starts=v.status(19)
  self.assertEqual(v.proc('rbUiState'),3);self.assertEqual(h.p['musicUnavailable'],0)
  self.assertIn('MUSIC CHANGE IN PROGRESS.',self.paint(v));self.assertEqual(h.call('musicRetry'),0)
  self.assertEqual(v.status(19),starts);self.assertEqual(v.max_parsers,1)
 def test_04_real_rejoin_failure_offers_functional_keyboard_retry(self):
  v=self.vm();h=v.objects['cakood'];t=v.objects['homeReadyTransport'];sound=v.objects['responsiveSound'];parser=v.parsers[sound];before=list(v.domain_words())
  for _ in range(10):self.frame(v)
  pos=parser['tick'];t.call('failHistory',3);h.call('audioPoll',2)
  self.assertEqual(v.proc('rbUiState'),5);self.assertEqual(h.p['musicUnavailable'],1);self.assertIn('MUSIC UNAVAILABLE. R TO RETRY.',self.paint(v))
  h.p.update(type=4,message=114);calls=v.calls[0,'musicRetry'];h.call('input')
  self.assertEqual(v.calls[0,'musicRetry'],calls+1);self.assertEqual(v.proc('rbUiState'),4);self.assertEqual(h.p['musicUnavailable'],0)
  self.assertIs(v.parsers[sound],parser);self.assertEqual(parser['tick'],pos);self.assertEqual(v.status(19),1)
  for _ in range(100):self.frame(v)
  self.assertEqual(v.proc('rbUiState'),1);self.assertEqual(h.p['musicUnavailable'],0);self.assertEqual(v.status(19),1);self.assertEqual(list(v.domain_words()),before)
  self.assertFalse(any('UNAVAILABLE'in x or'RECOVERING'in x for x in self.paint(v)))
 def test_05_ceiling_failure_latches_through_ordinary_later_aperture_poll(self):
  v=self.vm();d,w=self.committed_enter(v);h=v.objects['cakood'];sound=v.objects['responsiveSound'];parser=v.parsers[sound];before=list(w)
  self.ceiling(v);self.assertEqual(v.proc('rbRequest',151),0);self.assertEqual(v.status(5),9)
  for _ in range(150):self.frame(v)
  self.assertGreater(parser['tick'],generate.manifest(151)['gates'][0]['dispatch_last'])
  self.assertEqual((v.status(0),v.status(18),v.status(19)),(151,0,1));self.assertIs(v.parsers[sound],parser)
  self.assertEqual(h.p['musicUnavailable'],1);self.assertEqual(v.proc('rbUiState'),6);self.assertEqual(h.call('musicRetry'),0)
  self.assertIn('MUSIC UNAVAILABLE.',self.paint(v));self.assertFalse(any('R TO RETRY'in x for x in v.paint));self.assertEqual(list(w),before)
  self.assertEqual(v.proc('rbRequest',152),0)
 def test_06_ceiling_on_connector_never_starts_stale_target_at_end(self):
  v=self.vm();self.committed_enter(v);self.to_bridge(v);self.frame(v,20);bridge=v.status(0);self.ceiling(v)
  self.assertEqual(v.proc('rbRequest',151),0)
  for _ in range(90):self.frame(v)
  self.assertEqual((v.status(0),v.status(1),v.status(5),v.status(19)),(0,3,9,2));self.assertFalse(v.parsers)
  self.assertEqual(sum(r[1]==6 and r[3]==bridge for r in v.sound_trace),1);self.assertFalse([r for r in v.sound_trace if r[1]==6 and r[3]==152])
  self.assertEqual(v.objects['cakood'].p['musicUnavailable'],1)
 def test_07_ceiling_between_position_reads_blocks_retirement(self):
  v=self.vm();self.committed_enter(v);self.ceiling(v);gate=generate.manifest(151)['gates'][0]
  self.staged_position(v,151,gate['dispatch_first']);reads=[0]
  def reject(vm,obj):
   reads[0]+=1
   if reads[0]==2:self.assertEqual(vm.proc('rbRequest',151),0)
  v.after_read=reject;v.objects['cakood'].call('audioPoll',2)
  self.assertEqual(v.status(5),9);self.assertEqual(v.status(0),151);self.assertEqual(v.status(18),0)
 def test_08_final_available_generation_can_finish_its_valid_intent(self):
  v=self.vm();d=v.objects['contestState'];d.call('vcInit');d.call('vcBindGeneration',0,1);w=v.domain_words();w[6]=1
  for i in range(10,22):w[i]=1
  a=v.arrays(943);a['rbGenerationHi'][0]=32767;a['rbGenerationLo'][0]=32766
  d.call('vcEnter',1,0,7,1);d.call('vcCommit');self.assertEqual(v.proc('rbHostCommitted',3,d),1)
  self.assertEqual((v.status(3),v.status(4),v.status(5)),(32767,32767,0));self.to_bridge(v)
  for _ in range(90):self.frame(v)
  self.assertEqual(v.status(0),152);self.assertEqual(v.status(5),0);self.assertEqual(v.max_parsers,1)
 def test_09_ceiling_preserves_user_controls_and_current_clock(self):
  v=self.vm();self.committed_enter(v);self.ceiling(v);v.proc('rbRequest',151);h=v.objects['cakood'];p=v.parsers[v.objects['responsiveSound']]
  h.p.update(masterVolume=39,musicMuted=1,paused=1);self.frame(v);pos=p['tick']
  for _ in range(10):self.frame(v)
  self.assertEqual(p['tick'],pos);self.assertEqual(p['volume'],0);self.assertEqual(v.status(20),39)
  h.p.update(paused=0);self.frame(v);self.assertEqual(v.status(0),151);self.assertEqual(v.status(19),1);self.assertEqual(v.status(5),9)
 def test_10_pending_chooser_cancellation_does_not_create_failure(self):
  for method in('writeSave','readSave'):
   v=self.vm();self.committed_enter(v);h=v.objects['cakood'];s=v.objects['responsiveSound'];p=v.parsers[s];before=list(v.domain_words());old=v._kernel;seen=[]
   def kernel(vm,k,args):
    if vm.knames[k]in('SaveGame','RestoreGame'):
     seen.append((vm.status(7),p['pauses'],p['volume']));vm.advance(30);return 0
    return old(k,args)
   v._kernel=types.MethodType(kernel,v);h.call(method);h.call('audioPoll',2)
   self.assertEqual(seen,[(1,1,0)]);self.assertIs(v.parsers[s],p);self.assertEqual(v.status(19),1);self.assertEqual(h.p['musicUnavailable'],0);self.assertEqual(list(v.domain_words()),before)
