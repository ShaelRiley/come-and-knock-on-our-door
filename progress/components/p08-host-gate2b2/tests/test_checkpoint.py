"""First bounded contract gate: genuine P03 actions plus explicit domain fixtures.
No active P08 campaign dispatch, native UI or native saved-game acceptance.
"""
from pathlib import Path
import copy,json,sys,unittest
import host
from host import act,choice
from source_host import VM as SourceVM
H=host.H;EMITTED=host.VM

def make(source=False):
 old=host.VM;host.VM=SourceVM if source else EMITTED
 try:h,d,a,p,q,r=host.setup()
 finally:host.VM=old
 s=h.vm.objects['p08State'];assert s.call('h8Init',h)==1
 return h,p,s

def ceramics(h,p,cloth):
 for args in ((0,17),(0,16),(5,37),(7,25,40)):act(h,*args)
 choice(h,204,1)
 for args in ((0,17),(2,1),(0,1),(0,12),(4,cloth),(0,18),(0,17),(0,16),(7,cloth,34),(1,40,30)):act(h,*args)
 assert p.p['p03Ready']==1 and p.call('p03Validate')==1

def context(s,p):
 # Explicit unit-test fixture only. Whole-campaign preparation derivation is a later gate.
 assert s.call('p08SetContext',5,0,8191,0,0,p.p['p03Padding'],5,3,0,0,0,0)==1

def commit(s):assert s.p['p08Busy']==1 and s.call('p08Commit')!=0

def claim(s,p,key,pos):
 context(s,p);s.call('p08Place',key,pos,0);commit(s)

def publish_fixture(s,key):
 i=s.call('h8OwnerIndex',key);words=s.arrays['p08Words'];off=58+i*2;receipt=list(words[off:off+2])
 assert s.call('p08SetCallback',0,0,0,0,0,0,0,1,*words[12:14])==1
 s.call('p08AcknowledgeHandoff',key,*receipt);commit(s)
 s.arrays['h8OwnerCodes'][i]=8
 for k in range(2):s.arrays['h8OwnerReceipts'][i*2+k]=receipt[k]
 # This is a unit fixture of a completed host publication, not an integration route.

class Checkpoint(unittest.TestCase):
 def test_genuine_original_cloth_history_and_no_implicit_handoff(self):
  for source in (False,True):
   for cloth,padding in ((39,1),(38,2)):
    h,p,s=make(source);ceramics(h,p,cloth)
    before=dict(p.p);self.assertEqual(s.call('h8OriginalCloth'),cloth)
    self.assertEqual(s.call('h8OwnersValid'),1);self.assertEqual(s.call('h8Barrier'),1)
    for obj,owner in ((34,3),(36,3),(63,5),(81,6),(40,3),(38,3),(39,3)):
     self.assertEqual(s.call('h8PhysicalOwner',obj),owner)
    self.assertEqual(dict(p.p),before);self.assertEqual(p.p['p03Padding'],padding)
 def test_exact_transfer_receipt_and_later_ack_required(self):
  for source in (False,True):
   h,p,s=make(source);ceramics(h,p,39);prior=dict(p.p)
   claim(s,p,1,1);self.assertEqual(s.call('h8OwnersValid'),0)
   self.assertEqual(s.call('h8Owns',1),0)
   publish_fixture(s,1);self.assertEqual(s.call('h8OwnersValid'),1)
   self.assertEqual([s.call('h8PhysicalOwner',x) for x in (34,36)],[8,8])
   original=s.arrays['h8OwnerReceipts'][1];s.arrays['h8OwnerReceipts'][1]=original+1
   self.assertEqual(s.call('h8OwnersValid'),0);s.arrays['h8OwnerReceipts'][1]=original
   ack=s.arrays['p08Words'][69];s.arrays['p08Words'][69]=original
   self.assertEqual(s.call('h8Owns',1),0);s.arrays['p08Words'][69]=ack
   self.assertEqual(s.call('h8OwnersValid'),1);self.assertEqual(dict(p.p),prior)
 def test_padding_authority_requires_original_cloth_and_hook_or_pocket(self):
  for source in (False,True):
   for cloth in (39,38):
    h,p,s=make(source);ceramics(h,p,cloth);prior=dict(p.p)
    claim(s,p,1,1);publish_fixture(s,1);claim(s,p,4,1)
    context(s,p);s.call('p08Unpack');commit(s);publish_fixture(s,22)
    self.assertEqual(s.call('h8OwnersValid'),0)
    for location in (1,2):
     s.p['h8PaddingPlace']=location;self.assertEqual(s.call('h8OwnersValid'),1)
     self.assertEqual(s.call('h8PhysicalOwner',cloth),8)
     self.assertEqual(s.call('h8PhysicalOwner',77-cloth),3)
    self.assertEqual(dict(p.p),prior);self.assertEqual(p.call('p03Validate'),1)
    saved=dict(p.p);p.p.update(p03Ready=0,p03Approved=0,p03CompleteHi=0,p03CompleteLo=0)
    self.assertEqual(p.call('p03Validate'),1);self.assertEqual(s.call('h8OwnersValid'),0)
    p.p.update(saved)
    padding=p.p['p03Padding'];p.p['p03Padding']=0
    self.assertEqual(s.call('h8OwnersValid'),0);p.p['p03Padding']=padding
 def test_unsigned_receipts_across_signed_limb_boundaries(self):
  for source in (False,True):
   h,p,s=make(source)
   for ah,al,bh,bl in ((0,32767,0,-32768),(0,-1,1,0),(32767,-1,-32768,0),(-1,-2,-1,-1)):
    self.assertEqual(s.call('h8SerialBefore',ah,al,bh,bl),1)
    self.assertEqual(s.call('h8SerialBefore',bh,bl,ah,al),0)
    self.assertEqual(s.call('h8SerialBefore',ah,al,ah,al),0)
 def test_inherited_ownership_guards_are_still_strict(self):
  for source in (False,True):
   h,p,s=make(source);r=h.vm.objects['p05State'];t=h.vm.objects['p06State']
   self.assertEqual(r.call('hPhysicalValid'),1);self.assertEqual(t.call('h6OwnersValid'),1)
   r.p['hPAOwner']=2;self.assertEqual(r.call('hPhysicalValid'),0)
   t.p['h6ScreenOwner']=2;self.assertEqual(t.call('h6OwnersValid'),0)
   self.assertEqual(s.call('h8Barrier'),1)
if __name__=='__main__':unittest.main(verbosity=2)
