from support import *
import hashlib
class HostCompositionProof(unittest.TestCase):
 def test_01_exact_guarded_hosts_and_segment_budget(self):
  rows=json.loads((H/'evidence/host-composition.json').read_text());self.assertEqual({r['host']for r in rows},{'p05-composition','p06-composition'})
  for row in rows:
   self.assertFalse(row['activation']);self.assertEqual(row['new_selectors'],0)
   for module in row['modules']:self.assertLess(module['combined_bytes'],65536)
 def test_02_actual_commit_hook_and_no_activation(self):
  for name in('p05-composition','p06-composition'):
   main=(H/f'build/{name}/src/main.sc').read_text();host=(H/f'build/{name}/src/module985.sc').read_text()
   self.assertNotIn('(rbInit ',main);self.assertIn('(if ok (rbHostCommitted operation hContest) (= hContestBlocked 1)) (return ok))',host)
   self.assertLess(host.index('(if ok (= ok (self hVCCommit:)))'),host.index('(rbHostCommitted operation hContest)'))
   self.assertIn('(return (rbRestoreBegin responsiveSound))',main);self.assertIn('(if (not (rbRestoreResume (ScriptID 986 0)))',main)
   if name=='p06-composition':
    line=next(s for s in main.splitlines()if s.startswith('(method (p05RestoreValidate)'));self.assertLess(line.index('h6RestoreValidate'),line.index('rbRestoreResume'))
 def test_03_existing_owner_and_guard_sources_not_replaced(self):
  for name,folder in(('p05-composition','p05'),('p06-composition','p06-frozen')):
   for source in(H/f'inputs/{folder}/src').glob('module*.sc'):
    if source.name=='module985.sc':continue
    self.assertEqual(source.read_bytes(),(H/f'build/{name}/src'/source.name).read_bytes())
 def test_04_no_new_selectors_or_classes_in_full_universes(self):
  for name,folder in(('p05-composition','p05'),('p06-composition','p06-frozen')):
   expected=json.loads((H/f'inputs/{folder}/selectors.json').read_text());actual={r['name']:r['selector_id']for r in json.loads((H/f'build/{name}/selector-list.json').read_text())};self.assertEqual(expected,actual)
   for n in(941,942,943):
    from extract_sci11 import extract
    layout=extract(H/f'build/{name}/compiled/{n}.scr.bin',H/f'build/{name}/compiled/{n}.scr.bin.hep',H/f'build/{name}/selector-list.json')
    self.assertFalse(any(o['is_class']for o in layout['objects']))
 def test_05_actual_emitted_main_shared_slot_control_adapter(self):
  for name in('p05-composition','p06-composition'):
   v=MusicVM(name);host=v.objects['cakood'];sound=v.objects['responsiveSound'];original=v.objects['musicTransport']
   self.assertEqual(v.proc('rbInit',sound,original,0,17061),1);host.p['opening']=0
   self.assertEqual(host.call('musicSelectOwner'),1);self.assertEqual(host.p['musicOwnerKind'],3);self.assertIs(host.p['musicOwner'],sound)
   host.p.update(masterVolume=80,musicMuted=0,paused=0,menuOpen=0,audioDuckTicks=0,audioDesired=1)
   self.assertEqual(host.call('musicRequests'),1);self.assertEqual(v.status(20),80);self.assertEqual(v.objects['homeReadyTransport'].p['nextRequestedState'],1)
   host.p['menuOpen']=1;host.call('audioHolds');self.assertEqual(v.status(22),1)
   host.p['menuOpen']=0;host.call('audioHolds');self.assertEqual(v.status(22),0)
   self.assertEqual(host.call('musicStopOwner'),1);self.assertEqual(v.status(23),0);self.assertEqual(host.p['musicOwnerKind'],0);self.assertFalse(v.parsers)
 def test_06_disabled_host_hook_is_music_state_noop(self):
  for name in('p05-composition','p06-composition'):
   v=MusicVM(name);d=v.objects['contestState'];before=list(v.domain_words())
   for op in(3,4,6,8,9):self.assertEqual(v.proc('rbHostCommitted',op,d),0)
   self.assertEqual(list(v.domain_words()),before);self.assertFalse(v.parsers);self.assertEqual(v.status(23),0)
