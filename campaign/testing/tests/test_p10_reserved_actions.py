"""Unsupported reserved identities never reach a legacy action dispatcher."""
import unittest,json
import host
from test_p10_active import ready
from test_cue_ownership import history

class P10ReservedActions(unittest.TestCase):
 def test_active_high_ids_and_retired_aggregate_are_consumed(self):
  for source in (False,True):
   h,d=ready(source);before=history(d);items=list(h.arrays['uiItems'])
   self.assertEqual(d.call('h10Active'),1)
   self.assertEqual(d.call('h10Stop',48,0),0)
   self.assertEqual(h.vm.objects['p08State'].call('h8ActionBarrier'),0)
   p=h.vm.objects['p03State'];q=h.vm.objects['p04State']
   old=(list(h.arrays['p02Slots']),list(p.arrays['bSlots']),list(q.arrays['qSlots']))
   legacy=[]
   def observe(obj,name,args,result):
    if name in ('p02Act','p03Act','p04Act','bDispatch','qDispatch','hDispatch','h6Dispatch','h7Dispatch','h8Dispatch'):
     legacy.append((obj.name,name,list(args)))
   h.vm.after_actual_call=observe
   try:
    for obj in (48,49,50,412,413,414):
     for verb in (1,2,3,4,6,8,9):h.call('hostActNow',verb,obj,0)
    for verb in range(10):h.call('hostActNow',verb,35,0)
    for obj in (410,411):
     for verb in (1,3,4,6,8,9):h.call('hostActNow',verb,obj,0)
    for target in (35,48,49,50,410,411,412,413,414):
     for verb in (1,2,3,4,6,8,9):h.call('hostActNow',verb,25,target)
   finally:h.vm.after_actual_call=None
   self.assertEqual(legacy,[])
   self.assertEqual(history(d),before)
   self.assertEqual(list(h.arrays['uiItems']),items)
   self.assertEqual((list(h.arrays['p02Slots']),list(p.arrays['bSlots']),list(q.arrays['qSlots'])),old)
   self.assertEqual(h.call('campaignHeld',35),0)
   self.assertEqual(h.call('campaignReachable',35),0)
   self.assertEqual(d.call('h10Inv'),1)
   (host.H/'evidence'/('p10-reserved-proof-'+str(source)+'.json')).write_text(json.dumps({'backend':'source' if source else 'emitted','legacy_dispatches':legacy,'attempts':127,'native_acceptance':False},indent=2)+'\n')
