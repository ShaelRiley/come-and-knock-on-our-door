"""Reachable display masks and exact voiced page authority, never synthetic wins."""
import copy,unittest
import host
from host import frame,close
from test_rendezvous import fixture,finish
from test_restore import Backend,load
from test_practical import input_action,arrive

class IntroNegative(unittest.TestCase):
 def test_02_every_reachable_mask_restores_and_resumes_first_unread(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);finish(h);opened=h.vm.snapshot();backend=Backend(h.vm)
   once=list(s.arrays['p08Words'][52:54])
   # Every subset is reachable with actual page-turn/display controls.
   # No positive mask is installed in the fixture or written by this test.
   for mask in range(64):
    h.vm.restore(copy.deepcopy(opened))
    for page in range(6):
     if mask & (1<<page):
      if h.p['uiPage']!=page:h.call('uiTurnPage',page-h.p['uiPage'])
      frame(h)
    self.assertEqual(s.arrays['h8IntroWords'][2],mask,(source,mask))
    close(h,read=False)
    self.assertEqual(s.call('h8SaveReady'),1,(source,mask))
    backend.saved=None;h.call('writeSave');self.assertIsNotNone(backend.saved,(source,mask));saved=copy.deepcopy(backend.saved)
    close(h,read=False);load(h,backend,saved)
    self.assertEqual((s.p['h8RestoreValid'],s.p['h8Failure'],s.arrays['h8IntroWords'][2]),(1,0,mask),(source,mask))
    opened_rows=[]
    def opened_hook(obj,name,args,result):
     if obj.name=='p08State' and name=='h8IntroControl' and args[0]==2 and result:
      opened_rows.append((h.p['uiDocument'],h.p['uiPage'],s.arrays['h8IntroWords'][2]))
    h.vm.after_actual_call=opened_hook
    input_action(h,6,8)
    for _ in range(70):
     if not h.p['motionPhase']:break
     h.vm.pump([{}])
    self.assertEqual(h.p['motionPhase'],0);h.vm.after_actual_call=None
    if mask<63:
     expected=next(i for i in range(6) if not mask&(1<<i))
     self.assertEqual(opened_rows,[(973,expected,mask)],(source,mask))
     self.assertEqual((h.p['uiDocument'],h.p['uiPage'],s.arrays['h8IntroWords'][2]),(973,expected,mask|(1<<expected)),(source,mask))
     self.assertEqual(s.call('h8IntroCheck',0),1)
    else:self.assertEqual(s.arrays['h8IntroWords'][4],0)
    self.assertEqual(list(s.arrays['p08Words'][52:54]),once)
    self.assertEqual(list(s.arrays['p08Words'][32:40]),[0]*8)

 def test_03_voiced_frames_exact_identity_windows_and_graph_accumulator(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);finish(h);d=h.vm.objects['sceneDialogue'];a=h.vm.objects['presentationAudio'];opened=h.vm.snapshot()
   original=h.vm._kernel
   for result in (0,1,-1):
    h.vm.restore(copy.deepcopy(opened))
    def kernel(k,args):
     value=original(k,args)
     return result if h.vm.knames.get(k)=='Graph' and args[0]==12 else value
    h.vm._kernel=kernel;frame(h);self.assertEqual(s.arrays['h8IntroWords'][2],1)
   h.vm._kernel=original
   for field in ('opening','paused','menuOpen'):
    h.vm.restore(copy.deepcopy(opened));h.p[field]=1;h.call('render');h.call('dialoguePresented')
    self.assertEqual(s.arrays['h8IntroWords'][2],0,field)
   h.vm.restore(copy.deepcopy(opened));h.vm.draw_success=False
   with self.assertRaises(host.base.VMError):h.call('render')
   self.assertEqual(s.arrays['h8IntroWords'][2],0);h.vm.draw_success=True
   h.vm.restore(copy.deepcopy(opened));h.call('dialoguePresented');d.call('sdPresented',d.p['sdGeneration'],0,a.p['token'])
   self.assertEqual(s.arrays['h8IntroWords'][2],0)
   # Each admitted unit-only window is excluded even if its page paints.
   for page in range(6):
    h.vm.restore(copy.deepcopy(opened));self.assertEqual(d.call('sdOpenWindow',973,page,1,0,0,0,a),1)
    h.p['uiPage']=page;h.call('render');h.call('dialoguePresented');self.assertEqual(s.arrays['h8IntroWords'][2],0,page)
   mutations=[('document',lambda:d.p.__setitem__('sdDocument',974)),('page',lambda:d.p.__setitem__('sdPage',1)),
    ('generation',lambda:d.call('sdMark',2)),('speaker',lambda:d.p.__setitem__('sdSpeaker',2)),
    ('voice',lambda:d.p.__setitem__('sdVoice',2)),('audio',lambda:d.p.__setitem__('sdAudioModule',917)),
    ('text',lambda:d.p.__setitem__('sdResource',207)),('entry',lambda:d.p.__setitem__('sdEntry',3)),
    ('header',lambda:d.p.__setitem__('sdHeader',2)),('line',lambda:d.p.__setitem__('sdLineKey',730)),
    ('part',lambda:d.p.__setitem__('sdPart',2)),('parts',lambda:d.p.__setitem__('sdPartCount',2)),
    ('root_doc',lambda:h.p.__setitem__('uiDocument',974)),('queue_doc',lambda:h.arrays['bridgeQueue'].__setitem__(s.arrays['h8IntroWords'][5],974)),
    ('queue_index',lambda:h.p.__setitem__('bridgeQueueIndex',0)),('bunny_room',lambda:r.p.__setitem__('hBunnyRoom',1)),
    ('frankie_room',lambda:t.p.__setitem__('h6FrankieRoom',1)),('jackie_room',lambda:h.p.__setitem__('location',1)),
    ('group',lambda:s.arrays['h8IntroWords'].__setitem__(6,2)),('lease',lambda:s.p.__setitem__('h8Lease',2)),
    ('revision',lambda:s.arrays['p08Words'].__setitem__(13,99))]
   mutations += [(f'session_{i}',lambda i=i:s.arrays['p08Session'].__setitem__(i,99)) for i in range(8)]
   for name,mutate in mutations:
    h.vm.restore(copy.deepcopy(opened));self.assertEqual(s.call('h8IntroControl',3,0),1);d.call('sdDraw',0);mutate()
    s.call('h8IntroControl',4,0);h.call('dialoguePresented');self.assertEqual(s.arrays['h8IntroWords'][2],0,name)
   h.vm.restore(copy.deepcopy(opened));self.assertEqual(s.call('h8IntroControl',3,0),1);d.call('sdDraw',0)
   n=sum(k=='Graph' and args[0]==12 for k,args in h.vm.ktrace)
   self.assertEqual(s.call('h8IntroControl',4,0),1)
   self.assertEqual(sum(k=='Graph' and args[0]==12 for k,args in h.vm.ktrace),n+1)
   self.assertEqual(s.arrays['h8IntroWords'][2],0);h.call('dialoguePresented');self.assertEqual(s.arrays['h8IntroWords'][2],1)

if __name__=='__main__':unittest.main(verbosity=2)
