"""Genuine P01-P07 action route; no readiness flags or actor positions are assigned."""
import host
from host import act,choice,close,frame
from test_return_caption import boot,first_entry
from source_host import VM as SourceVM
from test_contest import start,reply
from p06_support import practical as screen_practical

EMITTED=host.VM

def living(h):
 room=h.p['location']
 if room==2:act(h,0,18)
 elif room==4:act(h,0,18)
 elif room!=1:
  if room!=0:act(h,0,17)
  act(h,2,1);act(h,0,1)
 assert h.p['location']==1

def stage(h,label):print(label,'room',h.p['location'],'steps',h.vm.steps,flush=True)

def prepared(source=False,cloth=39):
 old=host.VM;host.VM=SourceVM if source else EMITTED
 try:h=boot(host.H)
 finally:host.VM=old
 h.vm.budget=900000000
 first_entry(h,'bunny');stage(h,'P01')
 for args in ((4,20),(4,21),(7,20,7),(7,21,7),(0,17),(0,16),(4,22),(0,17),(2,1),(0,1),(7,22,7),(5,26),(0,17),(0,15),(1,23,28),(4,24),(5,24)):
  act(h,*args)
 living(h);act(h,7,24,7)
 for i in (1,2,3):choice(h,201,i)
 h.call('uiHostConfirm',201);close(h)
 assert h.p['p02PlanAgreed']==1
 stage(h,'P02')
 p=h.vm.objects['p03State'];q=h.vm.objects['p04State'];r=h.vm.objects['p05State'];t=h.vm.objects['p06State'];u=h.vm.objects['p07State'];v=h.vm.objects['contestState'];s=h.vm.objects['p08State']
 h.p['p08']=s
 if not s.p['h8Host']:assert s.call('h8Init',h)==1
 else:assert s.p['h8Host'] is h and s.call('h8OwnersValid')==1
 for args in ((0,12),(4,cloth),(0,18),(0,17),(0,16),(5,37),(7,25,40)):act(h,*args)
 choice(h,204,1)
 if h.p['uiPanel']:h.call('uiClose');frame(h)
 act(h,7,cloth,34);act(h,1,40,30)
 assert p.p['p03Ready']==1 and p.call('p03Validate')==1
 stage(h,'P03')
 act(h,0,17);act(h,4,4);act(h,0,14)
 for args in ((2,60),(7,4,60),(9,62),(7,62,55),(4,4),(8,60)):act(h,*args)
 assert q.call('p04Ready')==1
 stage(h,'P04')
 living(h);host.practical(h,r)
 act(h,6,28);choice(h,211,4)
 for pair in range(1,7):choice(h,215,1);choice(h,216,pair)
 start(h,v);reply(h,26)
 assert v.call('vcFlags')==1
 act(h,6,28);choice(h,211,5)
 assert r.call('p05Flags')==7 and r.p['hCartRoom']==5
 stage(h,'P05 + VC01 loss')
 living(h);screen_practical(h,t)
 act(h,6,85);choice(h,219,6)
 for pair in range(7,13):choice(h,215,1);choice(h,216,pair)
 start(h,v);reply(h,26)
 assert v.call('vcFlags')==3
 act(h,6,85);choice(h,219,7)
 assert t.call('p06Projection',0)==7
 stage(h,'P06 + VC02 loss')
 living(h);act(h,0,12)
 for args in ((5,86),(7,89,90)):act(h,*args)
 choice(h,227,2)
 for args in ((7,87,92),(7,90,92),(7,88,92),(7,94),(7,94),(7,91,92),(3,93)):act(h,*args)
 assert u.call('p07Projection',0)==3 and u.p['h7OwnerRoom']==2
 stage(h,'P07')
 living(h);act(h,0,13)
 assert h.p['location']==4 and s.call('h8Context')==1
 assert s.call('h8Preparations')==8191 and s.p['p08Wins']==0
 assert (s.p['p08FrankieRoom'],s.p['p08BunnyRoom'])!=(5,5)
 stage(h,'P08 genuine admission')
 return h,p,q,r,t,u,v,s
if __name__=='__main__':
 h,p,q,r,t,u,v,s=prepared()
 print('COMPLETE',s.call('h8Preparations'),s.p['p08Wins'],flush=True)
