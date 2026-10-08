"""Actual cutaway contents over genuine route histories; draw traces, not pixels."""
from test_composition_initial import CompositionInitial
from test_rendezvous import fixture,finish,step,kitchen
from test_layout_controls import place
from test_transactions import logical


class SceneComposition(CompositionInitial):
    def inspect_frame(self,h):
        s=h.vm.objects['p08State'];u=h.vm.objects['p07State'];camera=s.call('h8RouteCamera')
        jack=h.p['location'];before=logical(h)
        h.vm.ktrace.clear();h.call('drawWorld')
        cels=[args for name,args in h.vm.ktrace if name=='DrawCel']
        background={1:101,2:300,4:305}[camera]
        self.assertEqual(sum(a[0]==background for a in cels),1)
        if camera==1:
            self.assertEqual(sum(a[0]==220 and a[2]==0 for a in cels),1)
            self.assertEqual(sum(a[0]==220 and a[2]==1 for a in cels),h.p['p02BoardRecords'].bit_count())
        elif camera==2:
            pot=u.call('h7PotCel')
            self.assertGreaterEqual(pot,0)
            self.assertEqual(sum(a[0]==234 and a[2]==pot and a[3:5]==(63,65) for a in cels),1)
            self.assertEqual(sum(a[0]==233 and a[2]==0 for a in cels),1)
        else:
            self.assertEqual(sum(a[0]==227 and a[2]==8 for a in cels),1)
            self.assertTrue(any(a[0]==228 and a[2]==7 for a in cels))
            self.assertFalse(any(a[0] in (233,234) for a in cels))
        people=[a for a in cels if a[0] in (214,216,218,219,237,238)]
        for actor,views in [(0,(218,237)),(1,(219,238))]:
            expected=int(camera==s.call('h8RouteRoom',actor))
            self.assertEqual(sum(a[0] in views for a in people),expected)
        self.assertEqual(sum(a[0] in (214,216) for a in people),int(camera==jack and not h.p['onApron']))
        feet=[a[4]+78*a[7]//128 for a in people]
        self.assertEqual(feet,sorted(feet))
        self.assertEqual(h.p['location'],jack);self.assertEqual(logical(h),before)
        return camera

    def test_04_living_and_current_court_props_through_return(self):
        for source in (False,True):
            h,p,q,r,t,u,v,s=fixture(source);seen=set()
            for _ in range(250):
                if not s.call('h8RouteBusy'):break
                seen.add(self.inspect_frame(h));step(h)
            self.assertEqual(seen,{1,4})
            self.inspect_frame(h)
            place(h,81,3);place(h,63,2)
            words=list(s.arrays['p08Words'])
            from host import act
            act(h,0,18);seen=set()
            for _ in range(250):
                if not s.call('h8RouteBusy'):break
                seen.add(self.inspect_frame(h));step(h)
            self.assertEqual(seen,{1,4});self.assertEqual(list(s.arrays['p08Words']),words)
            self.assertEqual((h.p['location'],r.p['hBunnyRoom'],t.p['h6FrankieRoom']),(1,1,1))

    def test_05_actual_kitchen_origin_keeps_single_pot_and_invitation(self):
        for source in (False,True):
            h,p,q,r,t,u,v,s=fixture(source);kitchen(h)
            history=(r.p['hBunnyHome'],u.p['h7BunnyInvited'],u.p['h7BunnyHome'],u.p['h7OwnerRoom'])
            seen=set()
            for _ in range(250):
                if not s.call('h8RouteBusy'):break
                seen.add(self.inspect_frame(h));step(h)
            self.assertEqual(seen,{1,2,4})
            self.assertEqual((r.p['hBunnyHome'],u.p['h7BunnyInvited'],u.p['h7BunnyHome'],u.p['h7OwnerRoom']),history)
            self.assertEqual((u.p['h7OwnerRoom'],r.p['hCartRoom']),(2,5))
            s.call('h8RouteCancel');seen=set()
            for _ in range(250):
                if not s.call('h8RouteBusy'):break
                seen.add(self.inspect_frame(h));step(h)
            self.assertEqual(seen,{1,2,4})
            self.assertEqual((r.p['hBunnyRoom'],t.p['h6FrankieRoom']),(2,1))
            self.assertEqual((r.p['hBunnyHome'],u.p['h7BunnyInvited'],u.p['h7BunnyHome'],u.p['h7OwnerRoom']),history)
