"""Earned P08 plus real doorway controls, draw-resource assertions in both modes.
No disk snapshots, save editing, native/pixel claims, or progress injection.
"""
import copy, json, unittest
import host
import test_rendezvous
from test_p09_active import gate_b, walk
from test_practical import input_action, arrive
from test_layout_controls import controls
from test_coexistence_r2 import choice_for, read_close
from test_p10_active import pick
from test_restore import Backend, load
from room_paint_source import PaintSource
from domain_source_vm import parse
from source_tools import methods

class RoomRenderFix(unittest.TestCase):
 def test_actual_travel_background_and_rejected_frozen_interception(self):
  for source in (False, True):
   print('ROOM_RENDER_BACKEND',source,flush=True)
   h,_=gate_b(source);vm=h.vm;s=vm.objects['p08State'];owner_rooms=[s.call('h8ActorRoom',i) for i in range(2,9)]
   if not source:
    earned=copy.deepcopy(test_rendezvous.CACHE[False])
    self.assertEqual(earned['program'],vm.snapshot()['program'])
    test_rendezvous.CACHE[True]=earned
    print('SOURCE_PREFIX_REUSE: authenticated same-program ordinary-input emitted P01-P07 admission; no state edits',flush=True)
   adapter=None
   if source:
    vm.source_calls=set();vm.source_branches=set();vm.source_instructions=set();vm.source_returns=[]
    adapter=PaintSource(vm,991,'SceneRenderer','sceneRenderer',{'h6BaseDrawWorld'})
    original=vm.call
    def call(obj,name,args=()):
     if obj.name=='sceneRenderer' and name=='h6BaseDrawWorld':return adapter.external(adapter.call(name,*args))
     return original(obj,name,args)
    vm.call=call
   def draw(expected):
    vm.ktrace.clear();h.call('drawWorld')
    views=[a[0] for n,a in vm.ktrace if n=='DrawCel']
    self.assertIn(expected,views)
    if expected!=305:self.assertNotIn(305,views)
    self.assertEqual([s.call('h8ActorRoom',i) for i in range(2,9)],owner_rooms)
    self.assertEqual(s.call('h8EveningReady'),1)
    npc_views={2:219,3:218,4:222,5:221,6:236,7:223,8:225}
    room=h.p['location']
    for actor,view in npc_views.items():
     self.assertEqual(views.count(view),int(s.call('h8ActorRoom',actor)==room),('NPC draw mismatch',source,room,actor,view,views))
    if room!=2:self.assertNotIn(217,views) # alternate speaking Bunny porch art
    print('ROOM_DRAW',source,room,expected,[v for v in views if v in npc_views.values()],flush=True)
    return views
   draw(305)
   walk(h,18,1)
   for _ in range(3):draw(101)
   # Exact frozen source interception rejected on this legitimately reached state.
   if source:
    repaired=adapter.methods['h6BaseDrawWorld']
    from room_render_fix import OLD
    old=OLD
    adapter.methods['h6BaseDrawWorld']=parse(old)[0]
    vm.ktrace.clear();h.call('drawWorld')
    views=[a[0] for n,a in vm.ktrace if n=='DrawCel']
    self.assertIn(305,views);self.assertNotIn(101,views)
    print('REJECTED_FROZEN_INTERCEPTION',views,flush=True)
    adapter.methods['h6BaseDrawWorld']=repaired
    draw(101)
   choice_for(h,7,2,verb=2);self.assertEqual(h.p['uiDocument'],1202)
   read_close(h);self.assertEqual(vm.objects['p10State'].call('p10Complete',2),1)
   b=Backend(vm);h.call('writeSave');self.assertIsNotNone(b.saved);saved=copy.deepcopy(b.saved)
   load(h,b,saved);draw(101)
   walk(h,12,2);draw(300)
   u=vm.objects['p07State'];self.assertEqual(u.p['h7BunnyInvited'],0)
   self.assertIn((1,2),controls(h))
   input_action(h,6,2);arrive(h)
   self.assertEqual((h.p['uiPanel'],h.p['uiChoiceContext']),(2,226))
   pick(h,4)
   self.assertEqual((h.p['location'],s.call('h8ActorRoom',2),u.p['h7BunnyInvited'],s.p['h8Failure']),(2,2,0,0))
   self.assertEqual(u.call('h7ReturnBunny'),0)
   print('REFUSED_FINAL_RETURN',source,0,flush=True)
   vm.pump([{'type':4,'message':27},{}])
   choice_for(h,5,1)
   self.assertEqual((h.p['uiDocument'],h.p['uiPageCount']),(1200,6))
   self.assertEqual(h.call('dialogueCanSpeak',2),1)
   read_close(h);self.assertEqual(vm.objects['p10State'].call('p10Complete',1),1)
   self.assertEqual(u.p['h7BunnyInvited'],0)
   admitted=copy.deepcopy(vm.snapshot())
   for mutation in ('restore_invalid','failure','apron','foreign_final_owner'):
    vm.restore(copy.deepcopy(admitted))
    if mutation=='restore_invalid':u.p['h7RestoreValid']=0
    elif mutation=='failure':u.p['h7Failure']=1
    elif mutation=='apron':h.p['onApron']=1
    else:h.p['p08']=vm.objects['P08State']
    vm.ktrace.clear();self.assertEqual(u.call('h7DrawBunny'),0)
    self.assertNotIn(219,[a[0] for n,a in vm.ktrace if n=='DrawCel'])
   vm.restore(copy.deepcopy(admitted));draw(300)

   walk(h,18,1);draw(101)
   walk(h,17,0);draw(100)
   walk(h,16,6);draw(302)
   walk(h,17,0);draw(100)
   input_action(h,2,1);arrive(h);host.close(h)
   walk(h,1,1);draw(101)
   walk(h,13,4);draw(305)
   print('PASS_ROOM_RENDER_BACKEND',source,flush=True)

 def test_z_genuine_invitation_prefinal_return_and_final_refusal(self):
  from test_rendezvous import fixture,kitchen,finish
  import test_confirmation_boundaries,test_p09_active
  from source_host import VM as SourceVM
  # Actual invitation and menu return before final publication must still work.
  for source in (False,True):
   h,*_=fixture(source);u=h.vm.objects['p07State'];s=h.vm.objects['p08State']
   kitchen(h);finish(h);walk(h,18,1);finish(h);walk(h,12,2)
   self.assertEqual(u.p['h7BunnyInvited'],1)
   input_action(h,6,2);arrive(h);pick(h,4)
   self.assertEqual((h.p['location'],s.call('h8ActorRoom',2),u.p['h7BunnyInvited']),(1,1,0))
   print('PASS_PREFINAL_INVITED_RETURN',source,flush=True)
  # Earn a second real final history with the invitation retained; no flags set.
  h,*_=fixture(False);kitchen(h)
  self.assertEqual(h.vm.objects['p07State'].p['h7BunnyInvited'],1)
  test_rendezvous.CACHE[False]=copy.deepcopy(h.vm.snapshot())
  test_confirmation_boundaries.CACHE.pop(False,None);test_p09_active.CACHE.pop(False,None)
  h,_=gate_b(False);earned=copy.deepcopy(h.vm.snapshot())
  self.assertEqual(h.vm.objects['p07State'].p['h7BunnyInvited'],1)
  for source in (False,True):
   vm=SourceVM() if source else host.VM()
   self.assertEqual(vm.snapshot()['program'],earned['program'])
   vm.restore(copy.deepcopy(earned));vm.budget=900000000
   h=vm.objects['cakood'];u=vm.objects['p07State'];s=vm.objects['p08State']
   walk(h,18,1);walk(h,12,2);input_action(h,6,2);arrive(h)
   self.assertEqual((h.p['uiPanel'],h.p['uiChoiceContext']),(2,226))
   pick(h,4)
   self.assertEqual((h.p['location'],s.call('h8ActorRoom',2),u.p['h7BunnyInvited'],s.p['h8Failure']),(2,2,1,0))
   self.assertEqual(u.call('h7ReturnBunny'),0)
   vm.pump([{'type':4,'message':27},{}]);choice_for(h,5,1)
   self.assertEqual((h.p['uiDocument'],h.p['uiPageCount']),(1200,6))
   self.assertEqual(h.call('dialogueCanSpeak',2),1)
   read_close(h);self.assertEqual(vm.objects['p10State'].call('p10Complete',1),1)
   self.assertEqual((s.call('h8ActorRoom',2),u.p['h7BunnyInvited'],s.p['h8Failure']),(2,1,0))
   print('PASS_FINAL_INVITED_RETURN_REFUSAL_AND_P10',source,flush=True)
