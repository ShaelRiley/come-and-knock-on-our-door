"""Actual source observation routes. Kernel traces prove source/emitted flow only."""
import copy,unittest
import host
from host import frame,close
from test_rendezvous import fixture,finish
from test_restore import Backend,load
from test_layout_controls import place,menu_pick
from test_practical import input_action,arrive
from test_transactions import logical

def history_only(h):
 state=logical(h)
 for branch,fields in [('p03',['p03Room']),('p04',['p04Room','p04Code','p04EventCount','p04LineCount','p04ResultLo'])]:
  for field in fields:state[branch].pop(field)
 return state



class SourceReader(unittest.TestCase):
    def test_01_two_page_source_requires_completed_frames_and_restores_partial(self):
        for source in (False,True):
            h,p,q,r,t,u,v,s=fixture(source);finish(h);before=history_only(h)
            self.assertEqual(s.call('h8ReaderAction',15),1)
            d=h.vm.objects['sceneDialogue']
            self.assertEqual((h.p['uiPanel'],h.p['uiDocument'],h.p['uiPage']),(4,990,0))
            self.assertEqual(s.arrays['h8ReaderWords'][0],2)
            self.assertEqual(s.arrays['h8ReaderWords'][11],0)
            self.assertEqual(list(s.arrays['p08Words'][32:40]),[0]*8)
            h.call('dialoguePresented');d.call('sdPresented',d.p['sdGeneration'],0,h.vm.objects['presentationAudio'].p['token'])
            self.assertEqual(s.arrays['h8ReaderWords'][11],0)
            frame(h)
            self.assertEqual(s.arrays['h8ReaderWords'][11],1)
            self.assertEqual(list(s.arrays['p08Words'][36:38]),[0,0])
            self.assertEqual(s.call('h8SaveReady'),1)
            backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved);partial=copy.deepcopy(backend.saved)
            h.call('uiTurnPage',1)
            self.assertEqual(s.arrays['h8ReaderWords'][11],1)
            frame(h)
            self.assertEqual(s.arrays['h8ReaderWords'][0],3)
            self.assertEqual(s.arrays['h8ReaderWords'][11],3)
            observed=list(s.arrays['p08Words'][36:38]);self.assertNotEqual(observed,[0,0])
            self.assertEqual(list(s.arrays['h8SourceWords'][4:6]),observed)
            self.assertEqual(s.call('h8SaveReady'),1)
            load(h,backend,partial)
            self.assertEqual((s.p['h8RestoreValid'],s.p['h8Failure']),(1,0))
            self.assertEqual(list(s.arrays['p08Words'][36:38]),[0,0])
            self.assertEqual(s.arrays['h8ReaderWords'][11],1)
            h.call('uiTurnPage',1);frame(h)
            self.assertEqual(list(s.arrays['p08Words'][36:38]),observed)
            close(h);self.assertEqual(list(s.arrays['h8ReaderWords']),[0]*40)
            self.assertEqual(s.call('h8SaveReady'),1)
            self.assertEqual(history_only(h),before)

    def test_02_actual_overlay_and_slate_dispatch_all_four_sources(self):
        for source in (False,True):
            h,p,q,r,t,u,v,s=fixture(source);finish(h);before=history_only(h)
            # Existing labels are links from this overlay, not reassigned native IDs.
            for choice,document,slot in ((1,988,32),(2,989,34),(3,990,36)):
                input_action(h,5,122);self.assertEqual(h.p['uiChoiceContext'],235)
                labels=[host.base.read_string(h.arrays['uiChoiceLabels'][i]) for i in range(h.p['uiChoiceCount'])]
                self.assertEqual(labels,[host.base.read_string(h.call('uiHostItemLabel',53)),host.base.read_string(h.call('uiHostItemLabel',83)),host.base.read_string(s.call('h8LayoutLabel',122))])
                menu_pick(h,choice);self.assertEqual(h.p['uiDocument'],document)
                close(h);self.assertNotEqual(list(s.arrays['p08Words'][slot:slot+2]),[0,0])
            self.assertEqual(history_only(h),before)
            self.assertEqual(list(s.arrays['p08Words'][38:40]),[0,0])
            input_action(h,5,40);arrive(h);close(h)
            self.assertEqual(list(s.arrays['p08Words'][38:40]),[0,0])
            place(h,40,1)
            input_action(h,5,40);arrive(h)
            self.assertEqual(h.p['uiDocument'],1000);close(h)
            self.assertNotEqual(list(s.arrays['p08Words'][38:40]),[0,0])
            observed=list(s.arrays['p08Words'][32:40]);revision=list(s.arrays['p08Words'][12:14])
            input_action(h,5,40);arrive(h);close(h)
            self.assertEqual(list(s.arrays['p08Words'][32:40]),observed)
            self.assertEqual(list(s.arrays['p08Words'][12:14]),revision)
            self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))
            self.assertEqual(host.base.read_string(t.call('h6Label',83)),'COURTYARD PLAN')
            self.assertEqual(host.base.read_string(t.call('h6Label',84)),'CLIP MARKS')
            from host import act
            act(h,5,83)
            self.assertEqual(list(s.arrays['p08Words'][32:40]),observed)

    def test_03_graph_accumulator_abort_obscured_and_direct_completion(self):
        for source in (False,True):
            h,p,q,r,t,u,v,s=fixture(source);finish(h)
            self.assertEqual(s.call('h8ReaderAction',13),1);d=h.vm.objects['sceneDialogue'];opened=h.vm.snapshot()
            original=h.vm._kernel
            for result in (0,1,-1):
                h.vm.restore(copy.deepcopy(opened))
                def kernel(k,args):
                    value=original(k,args)
                    return result if h.vm.knames.get(k)=='Graph' and args[0]==12 else value
                h.vm._kernel=kernel
                frame(h)
                self.assertNotEqual(list(s.arrays['p08Words'][32:34]),[0,0])
                self.assertEqual(s.arrays['h8ReaderWords'][0],3)
            h.vm._kernel=original
            for name in ('opening','paused','menuOpen'):
                h.vm.restore(copy.deepcopy(opened));h.p[name]=1
                h.call('render');h.call('dialoguePresented')
                self.assertEqual(list(s.arrays['p08Words'][32:34]),[0,0],name)
                self.assertEqual(s.arrays['h8ReaderWords'][11],0)
            h.vm.restore(copy.deepcopy(opened));h.vm.draw_success=False
            with self.assertRaises(host.base.VMError):h.call('render')
            self.assertEqual(list(s.arrays['p08Words'][32:34]),[0,0])
            self.assertEqual(s.arrays['h8ReaderWords'][11],0)
            h.vm.draw_success=True;h.vm.restore(copy.deepcopy(opened))
            self.assertEqual(s.call('h8ReaderFrame',0),1);d.call('sdDraw',0)
            self.assertEqual(list(s.arrays['p08Words'][32:34]),[0,0])
            count=sum(n=='Graph' and a[0]==12 for n,a in h.vm.ktrace)
            self.assertEqual(s.call('h8ReaderFrame',1),1)
            self.assertEqual(sum(n=='Graph' and a[0]==12 for n,a in h.vm.ktrace),count+1)
            h.call('dialoguePresented')
            observed=list(s.arrays['p08Words'][32:34]);self.assertNotEqual(observed,[0,0])
            h.call('dialoguePresented');self.assertEqual(list(s.arrays['p08Words'][32:34]),observed)

    def test_04_stale_exact_identity_never_observes_or_repairs(self):
        for source in (False,True):
            h,p,q,r,t,u,v,s=fixture(source);finish(h)
            s.call('h8ReaderAction',13);d=h.vm.objects['sceneDialogue'];opened=h.vm.snapshot()
            def group(index,value):s.arrays['h8ReaderWords'][index]=value
            mutations=[('ui_document',lambda:h.p.__setitem__('uiDocument',989)),('ui_page',lambda:h.p.__setitem__('uiPage',1)),
                ('document',lambda:d.p.__setitem__('sdDocument',989)),('generation',lambda:d.call('sdMark',2)),
                ('entry',lambda:d.p.__setitem__('sdEntry',28)),('header',lambda:d.p.__setitem__('sdHeader',0)),
                ('part_count',lambda:d.p.__setitem__('sdPartCount',2)),('speaker',lambda:d.p.__setitem__('sdSpeaker',1)),
                ('full_count',lambda:d.p.__setitem__('sdCount',2)),('window',lambda:d.arrays['sdWindowBounds'].__setitem__(1,1)),
                ('queue_index',lambda:h.p.__setitem__('bridgeQueueIndex',0)),('queue_kind',lambda:d.arrays['sdQueueKinds'].__setitem__(0,0)),
                ('queue_document',lambda:h.arrays['bridgeQueue'].__setitem__(0,989)),('room',lambda:h.p.__setitem__('location',1)),
                ('apron',lambda:h.p.__setitem__('onApron',1)),('bunny',lambda:r.p.__setitem__('hBunnyRoom',1)),
                ('frankie',lambda:t.p.__setitem__('h6FrankieRoom',1)),('milo',lambda:r.p.__setitem__('hMiloRoom',4)),
                ('vivian',lambda:t.p.__setitem__('h6VivianRoom',4)),('revision',lambda:s.arrays['p08Words'].__setitem__(13,1)),
                ('group',lambda:group(10,2)),('lease',lambda:group(8,2))]
            mutations += [(f'session_{i}',lambda i=i:s.arrays['p08Session'].__setitem__(i,99)) for i in range(8)]
            for name,mutate in mutations:
                h.vm.restore(copy.deepcopy(opened));self.assertEqual(s.call('h8ReaderFrame',0),1);d.call('sdDraw',0);mutate()
                changed=copy.deepcopy((h.p['location'],r.p['hBunnyRoom'],t.p['h6FrankieRoom'],r.p['hMiloRoom'],t.p['h6VivianRoom'],list(s.arrays['p08Session'])))
                s.call('h8ReaderFrame',1);h.call('dialoguePresented')
                self.assertEqual(list(s.arrays['p08Words'][32:40]),[0]*8,name)
                self.assertEqual(s.arrays['h8ReaderWords'][11],0,name)
                self.assertEqual((h.p['location'],r.p['hBunnyRoom'],t.p['h6FrankieRoom'],r.p['hMiloRoom'],t.p['h6VivianRoom'],list(s.arrays['p08Session'])),changed,name)

    def test_05_complete_queue_reservation_and_uncertain_publication(self):
        for source in (False,True):
            h,p,q,r,t,u,v,s=fixture(source);finish(h);d=h.vm.objects['sceneDialogue']
            # Deliberate saturation through the real publisher, not a claimed
            # ordinary 32-record story route. Nothing is discarded for capacity.
            h.call('bridgeBegin')
            for _ in range(16):h.call('h7PublishNative',2,385,386)
            old=list(s.arrays['p08Words']),list(h.arrays['bridgeQueue']),list(d.arrays['sdQueueKinds']),h.p['bridgeQueueCount'],h.p['bridgeQueueIndex']
            self.assertEqual(s.call('h8ReaderAction',13),0)
            self.assertEqual((list(s.arrays['p08Words']),list(h.arrays['bridgeQueue']),list(d.arrays['sdQueueKinds']),h.p['bridgeQueueCount'],h.p['bridgeQueueIndex']),old)
            self.assertEqual(list(s.arrays['h8ReaderWords']),[0]*40)
            h.call('bridgeBegin');clean=h.vm.snapshot()
            for boundary in ('h8CommitReserved','h8UIPublish'):
                h.vm.restore(copy.deepcopy(clean));fired=[]
                def fault(obj,name,args,result):
                    if obj.name=='p08State' and name==boundary and result and not fired:
                        fired.append(name);h.arrays['bridgeQueue'][0]=989
                        if boundary=='h8CommitReserved':h.p['bridgeQueueCount']=1
                h.vm.after_actual_call=fault
                self.assertEqual(s.call('h8ReaderAction',13),0,boundary)
                h.vm.after_actual_call=None
                self.assertEqual(fired,[boundary]);self.assertEqual(s.p['h8Failure'],20)
                self.assertEqual(s.call('h8ActionBarrier'),1)
                self.assertEqual(list(s.arrays['p08Words'][32:40]),[0]*8)

    def test_06_cancel_partial_and_reject_corrupt_restore(self):
        for source in (False,True):
            h,p,q,r,t,u,v,s=fixture(source);finish(h);s.call('h8ReaderAction',15);frame(h)
            self.assertEqual(s.arrays['h8ReaderWords'][11],1)
            close(h,read=False);self.assertEqual(list(s.arrays['p08Words'][36:38]),[0,0])
            self.assertEqual(list(s.arrays['h8ReaderWords']),[0]*40)
            s.call('h8ReaderAction',15);self.assertEqual(s.arrays['h8ReaderWords'][11],0);frame(h)
            backend=Backend(h.vm);h.call('writeSave');good=copy.deepcopy(backend.saved);live=h.vm.snapshot()
            for name,index,value in [('mask',11,4),('record',3,17),('reserved_tail',39,1),('session',28,4),('actor',20,1)]:
                h.vm.restore(copy.deepcopy(good));s.arrays['h8ReaderWords'][index]=value;bad=h.vm.snapshot()
                h.vm.restore(copy.deepcopy(live));load(h,backend,bad)
                self.assertEqual((s.p['h8Failure'],s.p['h8Enabled']),(21,0),name)
                self.assertEqual(list(s.arrays['p08Words'][32:40]),[0]*8)
                load(h,backend,good)
                self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid']),(0,1),name)
                self.assertEqual(s.arrays['h8ReaderWords'][11],1)


if __name__=='__main__':unittest.main(verbosity=2)
