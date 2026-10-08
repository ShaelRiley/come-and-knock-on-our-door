"""E03 literal ACK kernel from genuine prior gameplay, with mocked storage only."""
import copy,unittest
import host
from test_confirmation_boundaries import stage,talk
from test_layout_controls import menu_pick
from test_storage_kernel import service
from test_restore import load
from storage_kernel_profile import StorageBackend

class EveningAck(unittest.TestCase):
 def test_01_save_ack_witness_unchanged_actors_and_post_ack_restore(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=stage(source,'menu');backend=StorageBackend(h.vm,occupied=range(1,26));acks=[]
   def observe(obj,name,args,result):
    if obj.name=='p08State' and name=='p08AcknowledgeAutosave':acks.append((args,result))
   h.vm.after_actual_call=observe
   menu_pick(h,1);before=list(s.arrays['p08Words']);owners=list(s.arrays['h8OwnerReceipts'])
   rooms=[s.call('h8ActorRoom',i) for i in range(1,9)];queue=list(h.arrays['bridgeQueue'])
   for _ in range(5):service(h)
   self.assertEqual((s.p['h8Failure'],s.arrays['h8EW'][0],s.arrays['p08Words'][9]),(0,1,1))
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady'),s.call('h8S',6)),(1,0,0))
   self.assertEqual(list(s.arrays['h8EW'][31:39]),before[16:24])
   self.assertEqual(list(s.arrays['h8EW'][41:48]),[1013,1017,1129,1,1134,4,0])
   self.assertEqual(list(s.arrays['h8OwnerReceipts']),owners);self.assertEqual([s.call('h8ActorRoom',i) for i in range(1,9)],rooms)
   self.assertEqual(list(h.arrays['bridgeQueue']),queue);self.assertEqual(h.p['uiPanel'],0)
   self.assertEqual(s.arrays['h8EW'][12],26);self.assertEqual(s.call('h8SaveReady'),1)
   self.assertEqual(s.call('h8ActionBarrier'),1)
   self.assertEqual(len(acks),1)
   words=list(s.arrays['p08Words']);witness=list(s.arrays['h8EW'])
   for _ in range(5):service(h)
   self.assertEqual(len(acks),1)
   h.call('uiClose');h.call('dialoguePresented');self.assertEqual(list(s.arrays['h8EW']),witness)
   h.call('writeSave');self.assertIsNotNone(backend.saved)
   saved=copy.deepcopy(backend.saved);ack_calls=len(acks);io=list(backend.auto_operations)
   load(h,backend,saved)
   self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,1,1,0))
   self.assertEqual(list(s.arrays['p08Words']),words);self.assertEqual(list(s.arrays['h8EW']),witness)
   self.assertEqual([s.call('h8ActorRoom',i) for i in range(1,9)],rooms)
   self.assertEqual(backend.auto_operations,io);self.assertEqual(len(acks),ack_calls)
   self.assertEqual(s.call('h8SaveReady'),1)

if __name__=='__main__':unittest.main(verbosity=2)
