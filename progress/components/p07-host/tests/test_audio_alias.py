"""Bounded exact slice interruption/restore and rejected cross-branch targets."""
import unittest,copy,json
from test_host import *
class AudioAliasTests(unittest.TestCase):
 def comic(self):
  h,d,a,p,q,r,s=make();act(h,6,2);choice(h,209,3);act(h,7,87,92);act(h,6,2);h.call('uiHostChoice',226,2);frame(h)
  return h,d,a,p,q,r,s
 def test_alias_restore_never_expands_to_sibling_units(self):
  h,d,a,p,q,r,s=self.comic();h.call('uiTurnPage',1);frame(h)
  saved=h.vm.snapshot();restore(h,saved)
  self.assertEqual((h.p['uiDocument'],h.p['uiPageCount'],h.p['uiPage'],d.p['sdEntry']),(971,3,1,50))
  self.assertEqual((s.p['h7RestoreValid'],s.p['h7LaughPending'],a.p['pendingLaugh']),(1,0,0))
  close(h);act(h,6,2);h.call('uiHostChoice',226,3);frame(h)
  saved=h.vm.snapshot();restore(h,saved)
  self.assertEqual((h.p['uiDocument'],h.p['uiPageCount'],h.p['uiPage'],d.p['sdEntry']),(972,2,0,52))
  self.assertEqual((s.p['h7RestoreValid'],s.p['h7LaughPending'],a.p['pendingLaugh']),(1,0,0))
 def test_close_menu_and_voice_mute_retire_unplayed_onion(self):
  for boundary in ['uiClose','uiHostMenu','voiceOff']:
   h,d,a,p,q,r,s=self.comic();self.assertEqual(s.p['h7LaughPending'],1)
   h.call(boundary);self.assertEqual(s.p['h7LaughPending'],0);self.assertEqual(a.p['pendingLaugh'],0)
   self.assertEqual(s.p['h7LaughCount'],0)
 def test_audience_mute_consumes_without_playback_or_later_raise(self):
  h,d,a,p,q,r,s=self.comic();a.call('setOff',2,1)
  h.call('uiTurnPage',1);frame(h);frame(h)
  self.assertEqual((s.p['h7LaughCount'],a.p['pendingLaugh'],a.p['lastLaughEvent']),(1,0,7007))
  a.call('setOff',2,0)
  for _ in range(4):frame(h)
  self.assertEqual((s.p['h7LaughCount'],a.p['pendingLaugh']),(1,0))
 def test_existing_bunny_topic_order_is_preserved(self):
  h,d,a,p,q,r,s=make();act(h,6,2)
  self.assertEqual(list(h.arrays['uiChoiceIds'])[:h.p['uiChoiceCount']],[1,3])
 def test_foreign_first_second_nouns_preserve_state_and_inventory(self):
  h,d,a,p,q,r,s=make();kitchen(h);before=list(s.arrays['p07Words']);inv=list(h.arrays['uiItems'])
  for verb,obj,target in [(7,25,92),(7,87,44),(1,90,2),(7,39,94),(9,93,0)]:
   act(h,verb,obj,target);self.assertEqual(list(s.arrays['p07Words']),before);self.assertEqual(list(h.arrays['uiItems']),inv)
  h.call('uiBuildFocus')
  payloads=[h.arrays['uiPayloads'][i] for i in range(h.p['uiControlCount']) if h.arrays['uiActions'][i]==1]
  self.assertTrue(all(x in payloads for x in [18,-103,43,44]));self.assertTrue(all(x in payloads for x in range(86,95)))
if __name__=='__main__':unittest.main(verbosity=2)
