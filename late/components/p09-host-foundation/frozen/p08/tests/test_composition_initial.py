"""Real prior campaign + legal meeting edges on the freshly composed program."""
import copy
import unittest
import host
from host import act,close
from test_rendezvous import fixture,finish,step
from test_layout_controls import place,overlay,controls,menu_pick
from test_practical import enter_control
from test_transactions import logical
from test_restore import Backend,load


class CompositionInitial(unittest.TestCase):
    def test_01_legal_route_gait_frames_and_moving_input(self):
        for source in (False,True):
            h,p,q,r,t,u,v,s=fixture(source)
            before=logical(h);words=list(s.arrays['p08Words']);jack=h.p['location']
            cels={237:set(),238:set()};edges=[]
            for _ in range(250):
                if not s.call('h8RouteBusy'):break
                h.vm.ktrace.clear()
                pose=s.call('h8RoutePose',s.call('h8RouteActor'))
                edges+=step(h)
                for name,args in h.vm.ktrace:
                    if name=='DrawCel' and args[0] in cels:
                        self.assertEqual(args[2],pose);cels[args[0]].add(args[2])
                if s.call('h8RouteBusy'):
                    self.assertEqual(s.call('h8LayoutInput'),0)
                    self.assertEqual(s.call('h8LayoutMenu',230,0,7),0)
            self.assertEqual(edges,[(0,1,4),(1,1,4)])
            self.assertEqual(cels,{237:{1,2,3,4},238:{1,2,3,4}})
            self.assertEqual((h.p['location'],s.call('h8RouteMeeting'),s.call('h8LayoutInput')),(jack,1,1))
            self.assertEqual(logical(h),before);self.assertEqual(list(s.arrays['p08Words']),words)
            h.vm.ktrace.clear();h.call('drawWorld')
            actors=[args for name,args in h.vm.ktrace if name=='DrawCel' and args[0] in (218,219,237,238)]
            self.assertEqual(sorted(a[0] for a in actors),[218,219])
            self.assertTrue(all(a[2]==0 for a in actors))
            ids=controls(h)
            self.assertEqual((ids.count((1,8)),ids.count((1,2))),(1,1))

    def test_02_assembled_named_layout_and_overlap_recovery(self):
        for source in (False,True):
            h,p,q,r,t,u,v,s=fixture(source);finish(h);old=logical(h)
            for n in (34,63,81,120,40):place(h,n,4,8 if n==120 else 7)
            self.assertEqual(list(s.arrays['p08Words'][:5]),[4]*5)
            self.assertEqual((r.p['hBunnyRoom'],t.p['h6FrankieRoom']),(4,4))
            self.assertEqual(s.call('h8RouteMeeting'),1)
            enter_control(h,2,9);h.vm.pump([{'type':1,'x':192,'y':120}])
            self.assertEqual(h.p['uiChoiceContext'],234)
            menu_pick(h,4);self.assertEqual(h.p['uiNounA'],120)
            enter_control(h,1,116)
            from test_practical import arrive
            arrive(h);close(h)
            self.assertEqual(s.arrays['p08Words'][3],1)
            for n,pos in ((34,1),(63,2),(81,3),(40,1)):overlay(h,n,1,pos);close(h)
            self.assertEqual(list(s.arrays['p08Words'][:5]),[1,2,3,1,1])
            self.assertEqual(s.call('h8OwnersValid'),1)
            self.assertEqual(logical(h),old)
            self.assertEqual(list(s.arrays['p08Words'][14:40]),[0]*26)
            self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))

    def test_03_assembled_save_restore_and_reversible_return(self):
        for source in (False,True):
            h,p,q,r,t,u,v,s=fixture(source);finish(h)
            place(h,81,3);place(h,63,2)
            words=list(s.arrays['p08Words']);route=list(s.arrays['h8RouteWords']);backend=Backend(h.vm)
            h.call('writeSave');self.assertIsNotNone(backend.saved)
            self.assertEqual(backend.operations,[('save',1)])
            saved=copy.deepcopy(backend.saved)
            act(h,0,18);finish(h)
            self.assertEqual((h.p['location'],r.p['hBunnyRoom'],t.p['h6FrankieRoom']),(1,1,1))
            load(h,backend,saved)
            self.assertEqual((h.p['location'],r.p['hBunnyRoom'],t.p['h6FrankieRoom']),(4,4,4))
            self.assertEqual(list(s.arrays['p08Words']),words)
            self.assertEqual(s.call('h8RouteMeeting'),1)
            self.assertEqual(s.call('h8LayoutInput'),1)
            self.assertEqual(s.call('h8SaveReady'),1)
            h.vm.ktrace.clear();h.call('drawWorld')
            self.assertFalse(any(name=='DrawCel' and args[0] in (237,238) for name,args in h.vm.ktrace))
            place(h,81,4);self.assertEqual(s.arrays['p08Words'][2],4)


if __name__=='__main__':unittest.main()
