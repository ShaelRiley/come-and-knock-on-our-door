from pathlib import Path
import sys,copy,contextlib,json,hashlib
import host
from host import act,choice,close,frame,base
from test_practical import restore,enter_control,input_action,arrive
from test_contest import start,reply,consume_current
from p06_source_host import VM as SourceVM
H=host.H;VMS=[];CACHE={};BYTECODE_VM=host.VM

@contextlib.contextmanager
def execution(kind):
 old=host.VM;host.VM=SourceVM if kind=='source' else BYTECODE_VM
 try:yield
 finally:host.VM=old

def new(kind='bytecode',plan=True):
 with execution(kind):h,d,a,p,q,r=host.setup(plan)
 h.vm.budget=300000000;VMS.append(h.vm)
 return h,d,a,p,q,r,h.vm.objects['p06State'],h.vm.objects['contestState']

def materials(h):
 act(h,6,8);choice(h,202,11);act(h,0,12);act(h,4,75)
 act(h,0,18);act(h,0,17);act(h,0,14);act(h,4,76);act(h,0,17)

def practical(h,s,scope=True):
 materials(h)
 if scope:act(h,6,85);choice(h,219,1)
 act(h,7,75,73);choice(h,221,2);act(h,7,76,74)
 act(h,8,80);choice(h,222,1)
 assert s.call('p06Projection',0)==(3 if scope else 2)
 return h

def taught(kind='bytecode'):
 key=(kind,'taught',hashlib.sha256((H/'build/coherent/compile-receipt.json').read_bytes()).hexdigest())
 if key not in CACHE:
  values=new(kind);h,d,a,p,q,r,s,v=values;practical(h,s)
  act(h,6,85);choice(h,219,6)
  for pair in range(1,13):choice(h,215,1);choice(h,216,pair)
  assert all(v.call('vcLearned',i,j) for i in range(1,13) for j in [1,2])
  assert v.call('vcRead',6)==0 and v.call('vcRead',7)==1
  CACHE[key]=h.vm.snapshot()
  return values
 values=new(kind);restore(values[0],copy.deepcopy(CACHE[key]),[{},{}])
 assert values[6].p['h6RestoreValid']==1 and values[0].p['uiFailure']==0
 return values

def finish(h,v,outcome):
 start(h,v)
 if outcome=='yield':reply(h,26)
 else:
  for _ in range(3):reply(h,25 if outcome=='loss' else v.call('vcRead',106+v.call('vcRead',95)))
 assert v.call('vcRead',92)==8

def logical(h):
 s=h.vm.objects['p06State'];v=h.vm.objects['contestState'];r=h.vm.objects['p05State']
 return dict(p06=list(s.arrays['p06Words']),contest=list(v.arrays['vcWords']),
  ownership=[s.p[k] for k in ['h6ScreenOwner','h6ScreenRoom','h6ScreenPosition','h6VivianRoom','h6FrankieRoom']],
  inventory=list(h.arrays['uiItems']),location=h.p['location'],apron=h.p['onApron'],
  old_p05=list(r.arrays['p05Words']),old_actors=[r.p[k] for k in ['hBunnyRoom','hMiloRoom','hPAOwner','hPARoom','hCartOwner','hCartRoom']])
