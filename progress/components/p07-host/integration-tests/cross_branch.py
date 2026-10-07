"""Ordinary combined P06/P07 inventory, source, world and restore regressions."""
from pathlib import Path
import sys,unittest,copy,json
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tests'))
import host
from test_host import make,kitchen,finish,restore
from host import act,choice,close,frame
import p06_support
VMS=[]
def to_kitchen(h):
 if h.p['location']==0:act(h,2,1);act(h,0,1)
 if h.p['location']==1:act(h,0,12)
 assert h.p['location']==2
class CrossBranch(unittest.TestCase):
 def test_held_screen_materials_survive_partial_recipe_restore_and_cooking(self):
  h,d,a,p,q,r,s=make();VMS.append(h.vm);t=h.vm.objects['p06State']
  # Actual existing Bunny authority, kitchen invitation and P05 escort from here.
  act(h,6,2);choice(h,209,3);h.call('hostActNow',5,86,0);frame(h)
  self.assertEqual((s.p['h7SeenCount'],s.call('p07Projection',0)),(1,0))
  close(h,read=False);act(h,6,2);h.call('uiHostChoice',226,5)
  self.assertEqual((h.p['location'],r.p['hBunnyRoom'],r.p['hBunnyHome']),(2,2,2))
  self.assertEqual(s.call('p07Projection',0),0);self.assertEqual(s.p['h7PendingSource'],0)
  close(h);self.assertEqual((h.p['location'],r.p['hBunnyRoom']),(5,5))
  garage_save=h.vm.snapshot();bad=copy.deepcopy(garage_save);bad['objects']['p07State']['h7BunnyInvited']=0
  restore(h,bad);self.assertEqual((s.p['h7RestoreValid'],h.p['uiFailure']),(0,10))
  restore(h,garage_save);self.assertEqual((s.p['h7RestoreValid'],h.p['uiFailure']),(1,0))
  act(h,6,2);choice(h,209,2);self.assertEqual((h.p['location'],r.p['hBunnyRoom']),(2,2))
  h.vm.paint=[];h.call('renderCaption');self.assertEqual((h.p['currentCaption'],h.p['navNotice'],h.vm.paint),(0,0,[]))
  saved=h.vm.snapshot();restore(h,saved)
  self.assertEqual((s.p['h7RestoreValid'],h.p['location'],r.p['hBunnyRoom'],s.call('p07Projection',0)),(1,2,2,0))
  act(h,6,2);choice(h,226,4)
  self.assertEqual((r.p['hBunnyRoom'],r.p['hBunnyHome'],s.p['h7BunnyInvited']),(1,2,0))
  historical=h.vm.snapshot();restore(h,historical);self.assertEqual(s.p['h7RestoreValid'],1)
  p06_support.materials(h)
  act(h,0,16);act(h,2,33);act(h,5,37);act(h,2,33)
  self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[1,1]);self.assertTrue(t.call('h6PhysicalValid'))
  act(h,0,17);to_kitchen(h)
  # Both existing P03 and new P07 hint families remain reachable in the kitchen.
  h.call('p03PreparationHint');self.assertEqual(h.p['uiChoiceContext'],228);choice(h,228,2)
  self.assertEqual(p.p['p03HintLevel'],1);self.assertEqual(s.p['h7HintLevel'],0)
  h.call('p03PreparationHint');choice(h,228,1)
  self.assertEqual((p.p['p03HintLevel'],s.p['h7HintLevel'],s.call('p07Projection',0)),(1,1,0))
  self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[1,1])
  h.call('hostActNow',5,86,0);frame(h);self.assertEqual(s.p['h7SeenCount'],1)
  saved=h.vm.snapshot();restore(h,saved)
  self.assertEqual((s.p['h7RestoreValid'],t.p['h6RestoreValid'],s.call('p07Projection',0)),(1,1,0))
  self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[1,1])
  h.call('uiTurnPage',1);frame(h);close(h);before=list(t.arrays['p06Words']);finish(h,s)
  self.assertEqual(list(t.arrays['p06Words']),before)
  self.assertEqual([h.arrays['uiItems'].count(x) for x in [75,76]],[1,1])
  self.assertTrue(s.call('h7SaveReady'));self.assertTrue(t.call('h6SaveReady'))
 def test_upstream_restore_rejection_suspends_p07_before_own_admission(self):
  h,d,a,p,q,r,s=make();VMS.append(h.vm);kitchen(h);act(h,7,87,92);saved=h.vm.snapshot()
  t=h.vm.objects['p06State'];bad=copy.deepcopy(saved);bad['objects']['p06State']['h6ScreenOwner']=2
  restore(h,bad);self.assertEqual(s.p['h7RestoreValid'],0);self.assertEqual(h.p['uiFailure'],10)
  h.vm.ktrace=[];h.call('drawKitchen')
  self.assertFalse(any(n=='DrawCel' and a[0] in [233,234] for n,a in h.vm.ktrace))
  restore(h,saved);self.assertEqual((s.p['h7RestoreValid'],t.p['h6RestoreValid'],h.p['uiFailure']),(1,1,0))
 def test_ready_screen_and_ready_food_keep_independent_world_owners(self):
  h,d,a,p,q,r,t,v=p06_support.taught();VMS.append(h.vm);s=h.vm.objects['p07State']
  p06_support.finish(h,v,'yield');act(h,6,85);choice(h,219,7)
  self.assertTrue(t.call('p06Projection',0)&4);to_kitchen(h);finish(h,s)
  self.assertEqual((t.p['h6ScreenOwner'],t.p['h6ScreenRoom'],t.p['h6ScreenPosition']),(1,4,0))
  self.assertEqual((s.p['h7Owner'],s.p['h7OwnerRoom'],s.p['h7ReadyEvents']),(1,2,1))
  self.assertEqual(s.call('p07Projection',4),8);self.assertFalse(any(x in [81,92,93] for x in h.arrays['uiItems']))
  saved=h.vm.snapshot();restore(h,saved)
  self.assertEqual((t.p['h6RestoreValid'],s.p['h7RestoreValid']),(1,1))
  self.assertEqual((t.p['h6ScreenRoom'],s.p['h7OwnerRoom']),(4,2))
if __name__=='__main__':unittest.main(verbosity=2)
