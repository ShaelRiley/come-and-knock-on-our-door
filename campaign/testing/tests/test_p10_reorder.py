"""Actual rack-to-rack move and occupied-slot rejection, both execution backends."""
import unittest,json,hashlib
import host
from test_p10_active import ready,input_action,arrive,pick
from host import close,act
from campaign_route import living

class P10Reorder(unittest.TestCase):
 def test_actual_installed_cue_move_and_undo(self):
  for source in (False,True):
   print('P10 REORDER BACKEND',source,flush=True)
   h,d=ready(source);living(h)
   input_action(h,2,7);arrive(h);pick(h,2);close(h)
   act(h,0,12);input_action(h,5,5);arrive(h);pick(h,1);close(h)
   living(h);act(h,0,13)
   input_action(h,5,410);arrive(h);pick(h,8);close(h)
   for slot,cue in enumerate((412,413,414)):
    input_action(h,5,cue);arrive(h);pick(h,slot+1);close(h)
    input_action(h,5,cue);arrive(h);pick(h,4);pick(h,slot);close(h)
   self.assertEqual(d.call('p10RackCorrect'),1)
   serial=(d.p['p10RestoredHi'],d.p['p10RestoredLo'])
   history=[d.call('h10Word',0,i,0) for i in range(61)]
   # Occupied destination must preserve every persistent domain word.
   input_action(h,5,410);arrive(h);pick(h,21);pick(h,4);pick(h,0);close(h)
   self.assertEqual([d.call('h10Word',0,i,0) for i in range(61)],history)
   input_action(h,5,410);arrive(h);pick(h,20);pick(h,5);close(h)
   # Move an already-installed original identity, not a freshly-held substitute.
   input_action(h,5,410);arrive(h);pick(h,21);pick(h,4);pick(h,0);close(h)
   self.assertEqual([d.call('p10SlotAt',i) for i in range(3)],[413,0,414])
   self.assertEqual(h.call('campaignHeld',413),0)
   self.assertEqual(list(h.arrays['uiItems']).count(413),0)
   self.assertEqual(d.call('p10RackCorrect'),0)
   self.assertEqual(d.call('p10Ready'),1)
   input_action(h,5,410);arrive(h);pick(h,20);pick(h,5);close(h)
   for slot,cue in enumerate((412,413)):
    input_action(h,5,cue);arrive(h);pick(h,4);pick(h,slot);close(h)
   self.assertEqual(d.call('p10RackCorrect'),1)
   self.assertEqual((d.p['p10RestoredHi'],d.p['p10RestoredLo']),serial)
   self.assertEqual(d.call('h10Inv'),1)
   print('P10 REORDER PASS',source,serial,flush=True)
   report={'backend':'source' if source else 'emitted','native_acceptance':False,
    'actual_installed_move':True,'occupied_rejected_without_history_change':True,
    'first_restoration':list(serial),'rack':[d.call('p10SlotAt',i) for i in range(3)],
    'compile_receipt_sha256':hashlib.sha256((host.H/'build/coherent/compile-receipt.json').read_bytes()).hexdigest()}
   (host.H/'evidence'/('p10-reorder-proof-'+str(source)+'.json')).write_text(json.dumps(report,indent=2)+'\n')
