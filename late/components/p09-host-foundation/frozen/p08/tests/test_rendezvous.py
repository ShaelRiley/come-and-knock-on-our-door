"""Bounded route gate from actual P01-P07 histories; deterministic native kernels.
No game flag or positive actor location is synthesized by these tests.
"""
import copy,json,unittest
from pathlib import Path
import host
from host import act,choice,close,frame
from campaign_route import prepared,living
from source_host import VM as SourceVM
from test_transactions import logical
from test_restore import Backend,load
CACHE={}

def actors(h):
 return tuple(h.vm.objects[n] for n in ('cakood','p03State','p04State','p05State','p06State','p07State','contestState','p08State'))

def fixture(source=False):
 import hashlib
 vm=SourceVM() if source else host.VM();vm.budget=900000000
 proof_dir=host.H/'evidence/rendezvous-fixtures';proof_dir.mkdir(exist_ok=True)
 path=proof_dir/('source.json' if source else 'emitted.json')
 current=vm.snapshot()['program']
 creator={str(p.relative_to(host.H)):hashlib.sha256(p.read_bytes()).hexdigest()
  for folder in ('tests','tools') for p in (host.H/folder).glob('*.py')
  if p.name not in ('test_rendezvous.py','run_rendezvous.py','probe_route.py','run_route_native_checkpoint.py')}
 if source not in CACHE and path.exists():
  saved=json.loads(path.read_text())
  if {k:v for k,v in saved['creator'].items() if Path(k).name!='run_route_native_checkpoint.py'}==creator and saved['state']['program']==current:
   assert hashlib.sha256(json.dumps(saved['state'],sort_keys=True).encode()).hexdigest()==saved['state_sha256']
   CACHE[source]=saved['state']
 if source not in CACHE:
  values=prepared(source);h=values[0];s=values[-1]
  assert s.call('h8RouteMode')==1,('real entry did not reserve route',list(s.arrays['h8RouteWords']))
  CACHE[source]=h.vm.snapshot()
  path.write_text(json.dumps({'origin':'actual unmodified campaign_route.prepared actions, no positive fixture edits',
   'creator':creator,'state':CACHE[source],
   'state_sha256':hashlib.sha256(json.dumps(CACHE[source],sort_keys=True).encode()).hexdigest()},sort_keys=True)+'\n')
 else:
  vm.restore(copy.deepcopy(CACHE[source]));h=vm.objects['cakood'];values=actors(h)
 return values

def step(h,ticks=6):
 s=h.vm.objects['p08State'];r=h.vm.objects['p05State'];t=h.vm.objects['p06State'];u=h.vm.objects['p07State']
 old=(t.p['h6FrankieRoom'],r.p['hBunnyRoom']);jack=h.p['location']
 h.call('drawWorld');h.call('advance',ticks)
 assert h.p['location']==jack,('camera changed Jackie',jack,h.p['location'])
 assert s.p['h8Failure']==0,('route failure',list(s.arrays['h8RouteWords']))
 assert s.call('h8RouteValid')==r.call('hPhysicalValid')==t.call('h6OwnersValid')==u.call('h7PhysicalValid')==1
 new=(t.p['h6FrankieRoom'],r.p['hBunnyRoom'])
 changes=[]
 for actor,(a,b) in enumerate(zip(old,new)):
  if a!=b:
   assert (a,b) in ((1,4),(4,1),(2,1),(1,2)),('illegal actor edge',actor,a,b)
   changes.append((actor,a,b))
 return changes

def finish(h):
 s=h.vm.objects['p08State'];edges=[]
 for i in range(250):
  if not s.call('h8RouteBusy'):return edges
  edges+=step(h)
 raise AssertionError(('route did not finish',list(s.arrays['h8RouteWords'])))

def reset_route(h):
 s=h.vm.objects['p08State'];assert s.call('h8RouteCancel')==1;finish(h);assert s.call('h8RouteMode')==0

def kitchen(h):
 reset_route(h);act(h,0,18);act(h,6,2);choice(h,209,3)
 r=h.vm.objects['p05State'];u=h.vm.objects['p07State']
 assert (h.p['location'],r.p['hBunnyRoom'],u.p['h7BunnyInvited'])==(2,2,1)
 act(h,0,18);act(h,0,13)
 s=h.vm.objects['p08State'];assert s.call('h8RouteMode')==1 and s.arrays['h8RouteWords'][1]==2

class Rendezvous(unittest.TestCase):
 def test_real_entry_legal_edges_actual_owner_and_no_intro(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);before=logical(h);words=list(s.arrays['p08Words'])
   self.assertEqual((s.call('h8Preparations'),s.p['p08Wins']), (8191,0))
   # Clear one already drawn pose, then undrawn ticks cannot fabricate motion.
   s.call('h8RouteRetire');position=list(s.arrays['h8RouteWords'])[7:11]
   for _ in range(3):h.call('advance',6)
   self.assertEqual(list(s.arrays['h8RouteWords'])[7:11],position)
   self.assertEqual(finish(h),[(0,1,4),(1,1,4)])
   self.assertEqual(s.call('h8RouteMeeting'),1)
   self.assertEqual((h.call('p02ObjectLocation',8),h.call('p02ObjectLocation',2)),(4,4))
   self.assertEqual(logical(h),before);self.assertEqual(list(s.arrays['p08Words']),words)
   self.assertEqual(s.call('p08OutputWord',1),0)
   self.assertEqual((h.call('dialogueCanSpeak',3),h.call('dialogueCanSpeak',2)),(1,1))
   h.call('uiBuildFocus');ids=[h.arrays['uiPayloads'][i] for i in range(h.p['uiControlCount']) if h.arrays['uiActions'][i]==1]
   self.assertEqual((ids.count(8),ids.count(2)),(1,1))
   # Actual courtyard Talk cannot leak into any old invitation menu.
   act(h,6,2);act(h,6,8)
   self.assertEqual((r.p['hBunnyHome'],r.p['hEscort'],u.p['h7BunnyInvited']),(1,0,0))
   self.assertEqual(list(s.arrays['p08Words']),words)
 def test_cancel_reverses_each_acquired_boundary(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);before=logical(h);snapshots=[]
   for _ in range(250):
    state=(s.arrays['h8RouteWords'][7],s.arrays['h8RouteWords'][9])
    if state in ((0,0),(2,0),(3,0),(5,2),(5,3),(5,5)) and state not in [x[0] for x in snapshots]:snapshots.append((state,h.vm.snapshot()))
    if not s.call('h8RouteBusy'):break
    step(h)
   self.assertEqual(len(snapshots),6)
   for state,snapshot in snapshots:
    h.vm.restore(copy.deepcopy(snapshot))
    if state==(3,0):
     h.vm.pump([{'type':4,'message':27}]);self.assertEqual(s.call('h8RouteMode'),3);s.call('h8RouteRetire')
    else:s.call('h8RouteCancel')
    prior=list(s.arrays['h8RouteWords'])[7:11]
    # A stale forward drawn pose is retired. No next-frame call can advance it.
    h.call('advance',6);self.assertEqual(list(s.arrays['h8RouteWords'])[7:11],prior)
    finish(h)
    self.assertEqual((s.call('h8RouteMode'),t.p['h6FrankieRoom'],r.p['hBunnyRoom']),(0,1,1))
    self.assertEqual(list(s.arrays['h8RouteWords'])[:31],[0]*31)
    self.assertEqual(logical(h),before)
 def test_kitchen_origin_preserves_real_invitation_and_reverse(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);kitchen(h);before=logical(h)
   origin=(r.p['hBunnyHome'],u.p['h7BunnyInvited'],u.p['h7BunnyHome']);self.assertEqual(origin,(1,1,1))
   self.assertEqual(finish(h),[(0,1,4),(1,2,1),(1,1,4)])
   self.assertEqual((r.p['hBunnyHome'],u.p['h7BunnyInvited'],u.p['h7BunnyHome']),origin)
   self.assertEqual(logical(h),before)
   # Ordinary successful departure returns actors without teleporting Jackie/camera.
   act(h,0,18);self.assertEqual(h.p['location'],1);self.assertEqual(s.call('h8RouteMode'),3)
   self.assertEqual(finish(h),[(1,4,1),(1,1,2),(0,4,1)])
   self.assertEqual((r.p['hBunnyRoom'],t.p['h6FrankieRoom'],u.p['h7BunnyInvited']),(2,1,1))
   act(h,0,12);act(h,6,2);choice(h,226,4)
   self.assertEqual((h.p['location'],r.p['hBunnyRoom'],u.p['h7BunnyInvited']),(1,1,0))
 def test_entry_excludes_restore_teleport_menu_and_failed_gate(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);reset_route(h);before=logical(h)
   for method,args in [('hostRoomChanged',()),('drawWorld',()),('uiBuildFocus',()),('h8RouteEntry',(4,13,h.p['p02Revision'])),('h8RouteEntry',(1,13,h.p['p02Revision'])),('h8RouteEntry',(1,13,h.p['p02Revision']-1))]:
    (s if method.startswith('h8') else h).call(method,*args)
   self.assertEqual(s.call('h8RouteMode'),0);self.assertEqual(logical(h),before)
   act(h,0,18);self.assertEqual(h.call('p05Transition',4),1);close(h)
   self.assertEqual(s.call('h8RouteMode'),0)
   act(h,0,18);act(h,0,17);act(h,0,14);act(h,8,60)
   self.assertNotEqual(q.p['p04Gate'],1);act(h,0,19)
   self.assertEqual((h.p['location'],s.call('h8RouteMode')),(3,0))
   act(h,2,60);act(h,7,4,60);act(h,0,19)
   self.assertEqual((h.p['location'],s.call('h8RouteMode')),(4,1))
 def test_keyboard_walk_cancel_and_stale_old_choice(self):
  from test_practical import enter_control,arrive
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);reset_route(h);act(h,0,18)
   h.call('uiCancelSentence');enter_control(h,1,13);self.assertNotEqual(h.p['motionPhase'],0)
   self.assertEqual(s.call('h8RouteMode'),0);h.call('motionCancel')
   self.assertEqual(s.call('h8RouteMode'),0)
   h.call('uiCancelSentence');enter_control(h,1,13);arrive(h);close(h)
   self.assertIn(s.call('h8RouteMode'),(1,2));self.assertEqual(h.p['location'],4)
   old=logical(h);route=list(s.arrays['h8RouteWords'])
   for context,choice_id in ((209,1),(209,3),(226,4),(201,1)):
    h.call('uiHostChoice',context,choice_id)
   h.call('uiHostConfirm',201)
   self.assertEqual(logical(h),old);self.assertEqual(list(s.arrays['h8RouteWords']),route)
   finish(h)
 def test_real_garage_listener_is_excluded_until_requested_return(self):
  original=host.practical
  def bunny_practical(h,r,listener=1):
   act(h,6,2);choice(h,209,1)
   self.assertEqual((h.p['location'],r.p['hBunnyRoom']),(5,5))
   act(h,7,65,66);act(h,7,64);choice(h,212,1);act(h,8,68);choice(h,213,1)
   act(h,6,65);choice(h,214,1);act(h,7,25,71);act(h,6,28);choice(h,211,3)
   self.assertEqual(r.call('p05Flags'),3)
   return h
  try:
   for source in (False,True):
    host.practical=bunny_practical
    h,p,q,r,t,u,v,s=prepared(source)
    self.assertEqual(s.call('h8Preparations'),8191)
    self.assertEqual((s.call('h8RouteMode'),r.p['hBunnyRoom'],r.call('p05SaveWord',69)),(0,5,1))
    before=logical(h);self.assertEqual(s.call('h8RouteEntry',1,13,h.p['p02Revision']-1),0)
    self.assertEqual(logical(h),before)
    act(h,0,18);act(h,0,17);act(h,0,15);act(h,6,2);choice(h,209,2)
    self.assertEqual((r.p['hBunnyRoom'],r.p['hBunnyHome'],r.call('p05SaveWord',69)),(1,1,0))
    living(h);act(h,0,13);self.assertEqual(s.call('h8RouteMode'),1);finish(h)
  finally:host.practical=original
 def test_deferred_save_return_save_and_cancelled_load(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);backend=Backend(h.vm)
   for _ in range(4):step(h)
   h.call('writeSave');self.assertEqual(backend.operations,[]);self.assertEqual(s.arrays['h8RouteWords'][12],1)
   finish(h);self.assertEqual(backend.operations,[('save',1)]);self.assertIsNotNone(backend.saved)
   assembled=copy.deepcopy(backend.saved)
   act(h,0,18);h.call('writeSave');self.assertEqual(backend.operations,[('save',1)])
   finish(h);self.assertEqual(backend.operations,[('save',1),('save',1)])
   self.assertEqual(s.call('h8RouteMode'),0)
   load(h,backend,assembled,events=[{'type':4,'message':27},{},{}])
   self.assertEqual((s.p['h8RestoreValid'],s.p['h8Failure'],s.call('h8RouteMode')),(1,0,2))
   self.assertEqual((r.p['hBunnyRoom'],t.p['h6FrankieRoom'],h.p['location']),(4,4,4))
   self.assertEqual(s.arrays['h8RouteWords'][12],0)
   # A canceled F3 chooser retires movement receipts; it grants no completion.
   s.call('h8RouteCancel');step(h);backend.restore_result=0;h.call('readSave')
   old=list(s.arrays['h8RouteWords'])[7:11];h.call('advance',6)
   self.assertEqual(list(s.arrays['h8RouteWords'])[7:11],old);finish(h)
 def test_restore_rejects_corrupt_locations_route_and_movement(self):
  for source in (False,True):
   h,p,q,r,t,u,v,s=fixture(source);backend=Backend(h.vm);moving=h.vm.snapshot();finish(h);h.call('writeSave')
   clean=copy.deepcopy(backend.saved);live=h.vm.snapshot()
   for kind in ('moving','frankie','bunny','origin','entry','node','ticks','home','invitation','reserved','orphan_bunny'):
    h.vm.restore(copy.deepcopy(clean))
    if kind=='moving':bad=copy.deepcopy(moving)
    else:
     if kind=='frankie':t.p['h6FrankieRoom']=1
     if kind=='bunny':r.p['hBunnyRoom']=2
     if kind=='origin':s.arrays['h8RouteWords'][1]=2
     if kind=='entry':s.arrays['h8RouteWords'][5]=18
     if kind=='node':s.arrays['h8RouteWords'][7]=3
     if kind=='ticks':s.arrays['h8RouteWords'][8]=1
     if kind=='home':r.p['hBunnyHome']=2
     if kind=='invitation':u.p['h7BunnyInvited']=1
     if kind=='reserved':s.arrays['h8RouteWords'][20]=1
     if kind=='orphan_bunny':
      for i in range(31):s.arrays['h8RouteWords'][i]=0
      t.p['h6FrankieRoom']=1
     bad=h.vm.snapshot()
    h.vm.restore(copy.deepcopy(live));load(h,backend,bad)
    self.assertEqual((s.p['h8Failure'],s.p['h8RestoreValid']),(21,0),kind)
    self.assertEqual((h.p['motionPhase'],h.p['type'],h.p['message']),(0,0,0),kind)
    # F3 recovery can load the exact saved meeting after rejected raw state.
    load(h,backend,clean);self.assertEqual((s.p['h8Failure'],s.call('h8RouteMeeting')),(0,1),kind)

if __name__=='__main__':unittest.main(verbosity=2)
