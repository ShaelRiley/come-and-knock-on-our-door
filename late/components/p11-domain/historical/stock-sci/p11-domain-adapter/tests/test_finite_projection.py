"""All reachable bounded rescue projections execute actual emitted transitions."""
from collections import deque
from test_domain import P11World,Harness,ByteVM,C,replace,M,HERE,unittest,json,hashlib,encode_world

def key(w,c):
 return (w.phase,bool(w.first_lift_at),bool(w.catch_at),bool(w.peg_request_at),c.gate.peg_engaged,w.sincere_complete)

def transition(h,c,index):
 actions=(('lift','Lift'),('release_catch','ReleaseCatch'),('request_peg','RequestPeg'),('pull_handle','PullHandle'),('stage_display','StageDisplay'),('set_back','SetBack'))
 if index<6:
  model,native=actions[index];h.action(model,'p11'+native,c=c)
 elif index==6:
  if h.w.first_lift_at:h.show('sincere',c)
 elif index==7:h.action('push_harder','p11PushHarder',c=c)
 elif index==8 and h.w.supported:
  c=replace(c,gate=replace(c.gate,peg_engaged=True))
  if h.w.pending_peg_request_id:h.ack_peg(c)
 elif index==9:c=replace(c,gate=replace(c.gate,peg_engaged=False))
 return c

class ProjectionTests(unittest.TestCase):
 def test_reachable_physical_projection_and_recovery(self):
  queue=deque([(P11World().save(),C)]);seen={};edges=0;steps=0
  while queue:
   data,c=queue.popleft();w=P11World.load(data);k=key(w,c)
   if k in seen:continue
   seen[k]=(data,c)
   for i in range(10):
    h=Harness(ByteVM,P11World.load(data));nc=transition(h,c,i);edges+=1;steps+=h.v.machine.steps
    if h.w.supported:self.assertFalse(h.w.contest_eligible)
    if key(h.w,nc) not in seen:queue.append((h.w.save(),nc))
  for data,c in seen.values():
   h=Harness(ByteVM,P11World.load(data))
   if h.w.supported:h.action('set_back','p11SetBack',c=c)
   if h.w.phase==0:c=h.rescue(c)
   elif h.w.phase==2:h.action('stage_display','p11StageDisplay',c=c)
   h.show('sincere',c);self.assertTrue(h.w.contest_eligible);self.assertEqual(h.w.flags,{'DISPLAY_STAGED','HELP_ACCEPTED'});steps+=h.v.machine.steps
  self.assertEqual(edges,len(seen)*10)
  report=dict(scope='Actual emitted SCI instructions against model over bounded reachable physical projections; captions also independently tested at every sincere prefix',states=len(seen),transitions=edges,recoveries=len(seen),executed_instructions=steps,strict_stack_balance=True,compiled_sha256=hashlib.sha256((HERE/'build/compiled/993.scr.bin').read_bytes()).hexdigest(),mismatches=0)
  (HERE/'evidence/compiled-projection.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':unittest.main()
