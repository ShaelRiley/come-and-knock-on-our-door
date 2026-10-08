"""Bounded request/receipt/consent probes from actual campaign actions."""
import copy,unittest
import host
from host import frame,close,act
from test_ready_confirmation import ready,request
from test_rendezvous import actors
from test_layout_controls import place,menu_pick
from test_practical import input_action,arrive
from test_restore import Backend,load
from source_host import VM as SourceVM
CACHE={}
def stage(source,name):
 if source not in CACHE:
  h,*_=ready(source);s=h.vm.objects['p08State'];rows={'ready':h.vm.snapshot()}
  request(h);rows['page']=h.vm.snapshot()
  for page in range(3):
   if page:h.call('uiTurnPage',1)
   frame(h)
  h.call('uiClose');frame(h);h.call('uiTurnPage',1);rows['last']=h.vm.snapshot()
  frame(h);assert s.arrays['p08Words'][11]==2;rows['queued']=h.vm.snapshot()
  close(h);assert h.p['uiChoiceContext']==237;rows['menu']=h.vm.snapshot()
  menu_pick(h,1);assert s.arrays['p08Words'][11]==3;rows['pending']=h.vm.snapshot();CACHE[source]=rows
 vm=SourceVM() if source else host.VM();vm.budget=900000000;vm.restore(copy.deepcopy(CACHE[source][name]));return actors(vm.objects['cakood'])
def talk(h):input_action(h,6,8);arrive(h)
def persistent(s):return (list(s.arrays['p08Words']),list(s.arrays['h8R']),list(s.arrays['h8CP']),list(s.arrays['h8OwnerReceipts']))

class ConfirmationBoundaries(unittest.TestCase):
 def test_02_noncontiguous_pages_suspend_restore_represent_and_decline(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=stage(source,'page');h.call('uiTurnPage',2);frame(h)
   self.assertEqual(s.arrays['h8R'][11],4)
   h.call('uiClose');h.call('uiTurnPage',1);frame(h)
   self.assertEqual((s.arrays['h8R'][11],s.arrays['p08Words'][11]),(20,1))
   close(h,read=False);backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved);saved=copy.deepcopy(backend.saved)
   request_id=list(s.arrays['p08Words'][16:18]);load(h,backend,saved)
   self.assertEqual((s.p['h8RestoreValid'],s.arrays['h8R'][11]),(1,20));request(h)
   self.assertEqual(list(s.arrays['p08Words'][16:18]),request_id)
   frame(h);self.assertEqual(s.arrays['h8R'][11],21);h.call('uiTurnPage',1);frame(h);self.assertEqual(s.arrays['h8R'][11],23)
   h.call('uiClose');frame(h);self.assertEqual((s.arrays['h8R'][11],s.arrays['p08Words'][11]),(31,2));close(h)
   self.assertEqual(h.p['uiChoiceContext'],237);menu_pick(h,2)
   self.assertEqual(s.arrays['p08Words'][11],0);self.assertEqual(h.p['uiDocument'],1012)
   close(h);self.assertEqual(s.arrays['p08Words'][8],1);self.assertEqual(list(s.arrays['h8CP']),[0]*8)
   self.assertEqual(list(s.arrays['p08Words'][32:40]),[0]*8);self.assertEqual(s.arrays['h8IntroWords'][2],0)

 def test_03_exact_frame_identity_windows_and_flush(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=stage(source,'page');d=h.vm.objects['sceneDialogue'];a=h.vm.objects['presentationAudio'];opened=h.vm.snapshot();original=h.vm._kernel
   for result in (0,1,-1):
    h.vm.restore(copy.deepcopy(opened))
    def kernel(k,args):
     value=original(k,args);return result if h.vm.knames.get(k)=='Graph' and args[0]==12 else value
    h.vm._kernel=kernel;frame(h);self.assertEqual(s.arrays['h8R'][11],1)
   h.vm._kernel=original
   h.vm.restore(copy.deepcopy(opened));h.call('dialoguePresented');d.call('sdPresented',d.p['sdGeneration'],0,a.p['token']);self.assertEqual(s.arrays['h8R'][11],0)
   for field in ('opening','paused','menuOpen'):
    h.vm.restore(copy.deepcopy(opened));h.p[field]=1;h.call('render');h.call('dialoguePresented');self.assertEqual(s.arrays['h8R'][11],0,field)
   h.vm.restore(copy.deepcopy(opened));h.vm.draw_success=False
   with self.assertRaises(host.base.VMError):h.call('render')
   h.vm.draw_success=True;self.assertEqual(s.arrays['h8R'][11],0)
   for page in range(3):
    h.vm.restore(copy.deepcopy(opened));self.assertEqual(d.call('sdOpenWindow',1008,page,1,0,0,0,a),1);h.p['uiPage']=page
    h.call('render');h.call('dialoguePresented');self.assertEqual(s.arrays['h8R'][11],0,page)
   mutations=[('document',lambda:d.p.__setitem__('sdDocument',1009)),('page',lambda:d.p.__setitem__('sdPage',1)),
    ('generation',lambda:d.call('sdMark',2)),('speaker',lambda:d.p.__setitem__('sdSpeaker',2)),('audio',lambda:d.p.__setitem__('sdAudioModule',917)),
    ('queue',lambda:h.arrays['bridgeQueue'].__setitem__(s.arrays['h8R'][13]+1,1009)),('request',lambda:s.arrays['h8R'].__setitem__(4,99)),
    ('session',lambda:s.arrays['p08Session'].__setitem__(4,99)),('frankie_room',lambda:t.p.__setitem__('h6FrankieRoom',1)),
    ('jackie_room',lambda:h.p.__setitem__('location',1)),('lease',lambda:s.p.__setitem__('h8Lease',99)),('revision',lambda:s.arrays['p08Words'].__setitem__(13,99))]
   for name,mutate in mutations:
    h.vm.restore(copy.deepcopy(opened));self.assertEqual(s.call('h8RCtl',3,0),1);d.call('sdDraw',0);mutate()
    s.call('h8RCtl',4,0);h.call('dialoguePresented');self.assertEqual(s.arrays['h8R'][11],0,name)
   h.vm.restore(copy.deepcopy(opened));self.assertEqual(s.call('h8RCtl',3,0),1);d.call('sdDraw',0)
   n=sum(k=='Graph' and args[0]==12 for k,args in h.vm.ktrace);self.assertEqual(s.call('h8RCtl',4,0),1)
   self.assertEqual(sum(k=='Graph' and args[0]==12 for k,args in h.vm.ktrace),n+1);self.assertEqual(s.arrays['h8R'][11],0)
   h.call('dialoguePresented');self.assertEqual(s.arrays['h8R'][11],1)

 def test_04_final_menu_pointer_numeric_stale_and_real_boundary_guards(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=stage(source,'menu');saved=h.vm.snapshot();words=list(s.arrays['p08Words'])
   mutations=[('id',lambda:h.arrays['uiChoiceIds'].__setitem__(0,h.arrays['uiChoiceIds'][0]+8)),
    ('count',lambda:h.p.__setitem__('uiChoiceCount',3)),('label',lambda:h.arrays['uiChoiceLabels'].__setitem__(0,h.arrays['uiChoiceLabels'][1])),
    ('actor',lambda:t.p.__setitem__('h6FrankieRoom',1)),('preparation',lambda:h.p.__setitem__('p02PlanAgreed',0)),
    ('revision',lambda:s.arrays['h8UI'].__setitem__(6,s.arrays['h8UI'][6]+1))]
   for name,mutate in mutations:
    h.vm.restore(copy.deepcopy(saved));mutate();h.call('uiHostChoice',237,h.arrays['uiChoiceIds'][0])
    self.assertEqual(list(s.arrays['p08Words']),words,name);self.assertEqual(list(s.arrays['h8CP']),[0]*8,name)
   for module,name in ((989,'h8RP'),(982,'sdTextBuffer')):
    h.vm.restore(copy.deepcopy(saved));a=h.vm.arrays(module)[name];pointer=host.base.Pointer(a.region,a.start*2);host.base.write_string(pointer,'BEGIN THE EVENING.')
    self.assertNotEqual(pointer,h.arrays['uiChoiceLabels'][0]);h.arrays['uiChoiceLabels'][0]=pointer;menu_pick(h,1)
    self.assertEqual(list(s.arrays['p08Words']),words);self.assertEqual(list(s.arrays['h8CP']),[0]*8)
   h.vm.restore(copy.deepcopy(saved));old=h.arrays['uiChoiceIds'][0];h.call('uiClose');talk(h);self.assertNotEqual(h.arrays['uiChoiceIds'][0],old)
   h.call('uiHostChoice',237,old);self.assertEqual(list(s.arrays['p08Words']),words)
   backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved);manual=copy.deepcopy(backend.saved)
   load(h,backend,manual,events=[{'type':4,'message':13},{},{}]);self.assertEqual(s.arrays['p08Words'][11],2);self.assertEqual(list(s.arrays['h8C']),[0]*10)
   self.assertEqual(list(s.arrays['h8CP']),[0]*8);talk(h);menu_pick(h,1);self.assertEqual(s.arrays['p08Words'][11],3)

 def test_05_atomic_ack_confirm_failure_retry_and_uncertain_recovery(self):
  for source in (False,True):
   for phase,method in (('last','p08AcknowledgeReadiness'),('menu','p08ConfirmStart')):
    h,p,q,r,t,u,v,s=stage(source,phase);before=persistent(s);queue=list(h.arrays['bridgeQueue']);d=h.vm.objects['sceneDialogue'];kinds=list(d.arrays['sdQueueKinds']);fired=[]
    def fault(obj,name,args,result):
     if obj.name=='p08State' and name==method and not fired:fired.append(name);h.p['bridgeSilent']=1
    h.vm.after_actual_call=fault
    if phase=='last':frame(h)
    else:menu_pick(h,1)
    h.vm.after_actual_call=None;h.p['bridgeSilent']=0;self.assertEqual(fired,[method])
    self.assertEqual(list(s.arrays['p08Words']),before[0]);self.assertEqual(list(s.arrays['h8CP']),before[2]);self.assertEqual(list(s.arrays['h8OwnerReceipts']),before[3])
    self.assertEqual(list(h.arrays['bridgeQueue']),queue);self.assertEqual(list(d.arrays['sdQueueKinds']),kinds);self.assertEqual(s.p['p08Busy'],0)
    if phase=='last':
     self.assertEqual(s.arrays['h8R'][11],31);close(h,read=False);talk(h);menu_pick(h,1);close(h);self.assertEqual(s.arrays['p08Words'][11],2)
    else:talk(h);menu_pick(h,1);self.assertEqual(s.arrays['p08Words'][11],3)
   h,p,q,r,t,u,v,s=stage(source,'menu');backend=Backend(h.vm);h.call('writeSave');good=copy.deepcopy(backend.saved);self.assertIsNotNone(good);fired=[]
   def corrupt(obj,name,args,result):
    if obj.name=='p08State' and name=='h8CommitReserved' and result and not fired:fired.append(name);h.p['bridgeQueueCount']+=1
   h.vm.after_actual_call=corrupt;menu_pick(h,1);h.vm.after_actual_call=None
   self.assertEqual(fired,['h8CommitReserved']);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid']),(20,0));self.assertEqual(s.call('h8ActionBarrier'),1)
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0));load(h,backend,good);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.arrays['p08Words'][11]),(0,1,2))

 def test_06_ordinary_pending_phases_save_failure_and_corrupt_restore(self):
  for source in (False,True):
   for stage_name,phase in (('page',1),('queued',2),('menu',2),('pending',3)):
    h,p,q,r,t,u,v,s=stage(source,stage_name);backend=Backend(h.vm);before=persistent(s);backend.save_result=0;h.call('writeSave')
    self.assertIsNone(backend.saved);self.assertEqual(persistent(s),before)
    backend.save_result=1;h.call('writeSave');self.assertIsNotNone(backend.saved,stage_name);good=copy.deepcopy(backend.saved)
    load(h,backend,good);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.arrays['p08Words'][11]),(0,1,phase),stage_name)
    self.assertEqual(list(s.arrays['p08Words']),before[0]);self.assertEqual(list(s.arrays['h8CP']),before[2]);self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))
   h,p,q,r,t,u,v,s=stage(source,'pending');backend=Backend(h.vm);h.call('writeSave');good=copy.deepcopy(backend.saved);live=h.vm.snapshot()
   mutations=[('checkpoint_marker',lambda:s.arrays['h8CP'].__setitem__(0,2)),('checkpoint_request',lambda:s.arrays['h8CP'].__setitem__(2,99)),
    ('checkpoint_reserved',lambda:s.arrays['h8CP'].__setitem__(7,1)),('transient_consent',lambda:s.arrays['h8C'].__setitem__(0,1)),
    ('mask',lambda:s.arrays['h8R'].__setitem__(11,30)),('receipt',lambda:s.arrays['h8R'].__setitem__(8,99))]
   for name,mutate in mutations:
    h.vm.restore(copy.deepcopy(good));mutate();bad=h.vm.snapshot();h.vm.restore(copy.deepcopy(live));calls=h.vm.calls.copy();load(h,backend,bad)
    self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid']),(21,0),name)
    for key in ((983,'bInventory'),(984,'qInventory')):self.assertEqual(h.vm.calls[key],calls[key],name)
    load(h,backend,good);self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid'],s.arrays['p08Words'][11]),(0,1,3),name)

if __name__=='__main__':unittest.main(verbosity=2)
