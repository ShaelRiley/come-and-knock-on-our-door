"""Finite source/emitted table/API gate; no new UI, render, gameplay or native claim."""
import json,copy,unittest,importlib.util
from pathlib import Path
import host
from source_host import VM as SourceVM
from test_return_caption import boot,first_entry
H=host.H
G=json.loads((H/'inputs/layout-geometry/geometry-manifest.json').read_text())
OBJECTS=['ceramic_carrier','pa_kit','completed_screen','serving_table','credit_slate']
ZONES=['HATCH','WALL','ALCOVE','LANE']
def decode():
 spec=importlib.util.spec_from_file_location('view_decoder',H/'inputs/layout-geometry/view_decoder.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 return m.decode_view((H/'snapshot/resources/228.view.bin').read_bytes())[0]
class Geometry(unittest.TestCase):
 def test_every_origin_cel_dimension_and_named_zone(self):
  cels=decode()
  for VM in (host.VM,SourceVM):
   vm=VM();s=vm.objects['p08State'];before=vm.snapshot()
   for i,obj in enumerate(OBJECTS):
    for pos,xy in enumerate(G['origins'][obj]):
     self.assertEqual([s.call('h8LayoutOrigin',i,pos,axis) for axis in (0,1)],xy)
   for cel,c in enumerate(cels):
    self.assertEqual([s.call('h8CelSize',cel,axis) for axis in (0,1)],[c['width'],c['height']])
   for pos,zone in enumerate(ZONES,1):
    self.assertEqual([s.call('h8LayoutZone',pos,k) for k in range(7)],G['zone_rects'][zone]+G['zone_approaches'][zone])
   self.assertEqual(vm.snapshot(),before)
 def test_native_identity_alias_and_invalid_boundaries(self):
  for VM in (host.VM,SourceVM):
   vm=VM();s=vm.objects['p08State'];before=vm.snapshot()
   self.assertEqual([s.call('h8LayoutNative',i) for i in range(5)],[34,63,81,120,40])
   self.assertEqual([s.call('h8LayoutIndex',n) for n in (34,36,63,81,120,40)],[0,0,1,2,3,4])
   for n in (80,83,72,35,38,39,43,45,121,122,-1,32767):self.assertEqual(s.call('h8LayoutIndex',n),-1)
   for method,args in [('h8LayoutNative',(-1,)),('h8LayoutNative',(5,)),('h8LayoutOrigin',(-1,0,0)),('h8LayoutOrigin',(5,0,0)),('h8LayoutOrigin',(0,-1,0)),('h8LayoutOrigin',(0,5,0)),('h8LayoutOrigin',(0,0,2)),('h8LayoutZone',(0,0)),('h8LayoutZone',(5,0)),('h8LayoutZone',(1,-1)),('h8LayoutZone',(1,7)),('h8CelSize',(-1,0)),('h8CelSize',(18,0)),('h8CelSize',(0,2))]:
    self.assertEqual(s.call(method,*args),-1,(method,args))
   self.assertEqual(vm.snapshot(),before)
 def test_actual_early_actor_queries_are_pure_and_evening_is_unavailable(self):
  emitted=host.VM
  try:
   for VM in (emitted,SourceVM):
    host.VM=VM;h=boot(H);s=h.vm.objects['p08State'];r=h.vm.objects['p05State'];t=h.vm.objects['p06State']
    for entered in (False,True):
     if entered:first_entry(h,'bunny')
     before=h.vm.snapshot()
     self.assertEqual([s.call('h8ActorRoom',n) for n in range(1,9)],[h.p['location'],h.call('p02ObjectLocation',2),t.p['h6FrankieRoom'],6,r.p['hMiloRoom'],t.p['h6VivianRoom'],6,3])
     self.assertEqual(s.call('h8ActorRoom',0),-1);self.assertEqual(s.call('h8ActorRoom',9),-1)
     self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))
     self.assertEqual(h.vm.snapshot(),before)
    # A raw unsupported flag is neither authority nor permission to repair state.
    s.arrays['p08Words'][9]=1;before=h.vm.snapshot()
    self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0));self.assertEqual(h.vm.snapshot(),before)
  finally:host.VM=emitted
if __name__=='__main__':unittest.main(verbosity=2)
