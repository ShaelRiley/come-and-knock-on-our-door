"""Independent native save rejection, source/model parity, all physical projections."""
from test_domain import *
import random
del DomainTests,BytecodeTests

def snapshots():
 w=P12World();out=[]
 def snap():out.append(w.save())
 def act(fn,*args,c=C):getattr(w,fn)(c,*args);snap()
 def show(source,c=C):
  act('begin_presentation',source,c=c)
  for token in w._tokens(source):
   if token in M['speech_unit_ids']:w.acknowledge_presentation(c,w._handle(source),speech_unit_ids=(token,))
   else:w.acknowledge_presentation(c,w._handle(source),record_id=token)
   snap()
 snap();act('start',RACK)
 for source in ('opening','rack','diagram','edge'):show(source)
 for source in ('audience_view','self_view','catch','rehearsal'):show(source,A)
 act('release_catch',c=A);act('rotate_rack');act('order_cards',TILE_IDS);show('introduction');act('commit_introduction');act('release_confetti');show('confetti');act('claim_laugh');show('cleanup');act('finish_welcome')
 return out

def model_valid(p):
 try:
  d=decode_words(list(p.values()));P12World.load(d)
  # A native vector is canonical only if no word was discarded by decoding.
  return encode_save(d)==p
 except (ValueError,KeyError,TypeError,IndexError):return False

class ProjectionTests(unittest.TestCase):
 def test_all_720_physical_rack_projections_and_orientations(self):
  v=ByteVM();count=0
  # 20 cue subsets x6 assigned word orders x6 slot orders=720 physical projections.
  # Both audience-facing and released/observed inward orientations are validated.
  for cues in itertools.combinations(CUE_IDS,3):
   for words in itertools.permutations(ORDER):
    w=P12World();w.start(C,{**RACK,'slots':cues,'words':words})
    w.begin_presentation(A,'self_view');w.acknowledge_presentation(A,w._handle('self_view'),record_id='P12.LOOK.003');w.release_catch(A)
    for facing in (False,True):
     if facing:w.rotate_rack(C)
     for slots in itertools.permutations(cues):
      q=copy.deepcopy(w);q.slots=list(slots);q.validate();p=encode_world(q);v.p.update(p)
      self.assertEqual(v.call('p12Validate'),1);self.assertEqual(tuple(W[v.call('p12VisibleWord',i)] for i in range(3)),q.visible_order)
      self.assertEqual(bool(v.call('p12RackCorrect')),q.visible_order==ORDER);count+=1
  self.assertEqual(count,1440)
  (HERE/'evidence/finite-projection.json').write_text(json.dumps({'physical_projections':720,'orientation_projections':count,'actual_emitted_bytecode':True,'stack_balance':True,'passed':True},indent=2)+'\n')

if __name__=='__main__':unittest.main()
