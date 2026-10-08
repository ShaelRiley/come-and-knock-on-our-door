"""Only the stale-revision negative changes: intro legitimately committed revision1."""
import copy
from test_source_reader import SourceReader
import test_source_reader
from test_rendezvous import fixture,finish as finish_route
from host import close

def finish_with_actual_intro(h):
    edges=finish_route(h)
    assert h.p['uiPanel']==4 and h.p['uiDocument']==973
    close(h)
    s=h.vm.objects['p08State']
    assert s.arrays['h8IntroWords'][2]==63 and s.arrays['h8IntroWords'][4]==0
    assert list(s.arrays['p08Words'][52:54])!=[0,0]
    return edges
finish=finish_with_actual_intro
test_source_reader.finish=finish_with_actual_intro

class SourceReaderAfterIntro(SourceReader):
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
                ('vivian',lambda:t.p.__setitem__('h6VivianRoom',4)),('revision',lambda:s.arrays['p08Words'].__setitem__(13,s.arrays['p08Words'][13]+1)),
                ('group',lambda:group(10,2)),('lease',lambda:group(8,2))]
            mutations += [(f'session_{i}',lambda i=i:s.arrays['p08Session'].__setitem__(i,99)) for i in range(8)]
            for name,mutate in mutations:
                h.vm.restore(copy.deepcopy(opened));self.assertEqual(s.call('h8ReaderFrame',0),1);d.call('sdDraw',0);mutate()
                changed=copy.deepcopy((h.p['location'],r.p['hBunnyRoom'],t.p['h6FrankieRoom'],r.p['hMiloRoom'],t.p['h6VivianRoom'],list(s.arrays['p08Session'])))
                s.call('h8ReaderFrame',1);h.call('dialoguePresented')
                self.assertEqual(list(s.arrays['p08Words'][32:40]),[0]*8,name)
                self.assertEqual(s.arrays['h8ReaderWords'][11],0,name)
                self.assertEqual((h.p['location'],r.p['hBunnyRoom'],t.p['h6FrankieRoom'],r.p['hMiloRoom'],t.p['h6VivianRoom'],list(s.arrays['p08Session'])),changed,name)
