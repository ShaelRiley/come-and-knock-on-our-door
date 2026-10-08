#!/usr/bin/env python3
"""Bounded four-way original/new source/emitted paint equivalence."""
from pathlib import Path
import sys,json,itertools,time
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests')]
import host
from test_return_caption import boot,first_entry
from host import act,close
from check_milestone import state,trace,value
from paint_source import VM as SourceVM
from derive import MOVED,dump,sha

class Recorder:
 def __init__(self,vm):self.vm=vm;self.instructions=set();self.branches=set()
 def append(self,row):
  number,name,pc,op,args,acc,stack=row
  if number not in (0,991) or name not in MOVED:return
  self.instructions.add((number,name,pc))
  if op in ('BT','BNT'):self.branches.add((number,name,pc,bool(acc) if op=='BT' else not acc))

class Matrix:
 def __init__(self):
  self.cases=[];self.q=[];original=host.VM
  for root,source in [(H/'frozen/p09',False),(H,False),(H/'frozen/p09',True),(H,True)]:
   host.VM=SourceVM if source else original
   h=boot(root);h.vm.trace=Recorder(h.vm);self.q.append(h)
  host.VM=original
 def reset(self,snapshots):
  for h,s in zip(self.q,snapshots):h.vm.restore(s)
 def snapshots(self):return [h.vm.snapshot() for h in self.q]
 def update(self,props=None,objects=None):
  for h in self.q:
   if props:
    assert set(props)<=set(h.p),set(props)-set(h.p);h.p.update(props)
   for obj,ps in (objects or {}).items():
    assert set(ps)<=set(h.vm.objects[obj].p),(obj,set(ps)-set(h.vm.objects[obj].p));h.vm.objects[obj].p.update(ps)
 def compare(self,label,name,*args,pure=False):
  results=[]
  for h in self.q:
   h.vm.ktrace.clear();before=state(h);actual=(*args,h.call('roomTitle')) if name=='blockPerson' else args;r=h.call(name,*actual);after=state(h)
   if pure:assert before==after,('Paint changed state',label,name)
   results.append([value(r),trace(h.vm),after])
  for i,r in enumerate(results[1:],1):
   if r!=results[0]:
    for j,key in enumerate(['return','kernel trace','state']):
     if r[j]!=results[0][j]:raise AssertionError((label,name,'variant',i,key,results[0][j],r[j]))
  self.cases.append(dict(label=label,method=name,args=list(args),kernel_calls=len(results[0][1]),pure=pure))
 def bank(self,group):
  dump(H/f'evidence/matrix-{group}.json',{'status':'PASS_FOUR_WAY','cases':self.cases,'compile_receipt_sha256':sha(H/'build/coherent/compile-receipt.json'),'native_acceptance':False});print('PASS_GROUP',group,len(self.cases),flush=True)
 def campaign(self):
  expected={'porch':0,'living':1,'kitchen':2,'conservatory':6,'side':3,'courtyard':4,'garage':5}
  for phase in expected:
   actions={'porch':[],'living':None,'kitchen':[(0,12)],'conservatory':[(0,18),(0,1),(0,16)],'side':[(0,17),(0,14)],'courtyard':[(0,17),(2,1),(0,1),(0,13)],'garage':[(0,18),(0,1),(0,15)]}[phase]
   for h in self.q:
    if actions is None:first_entry(h)
    else:
     for a in actions:act(h,*a)
     close(h)
    assert h.p['location']==expected[phase],(phase,h.p['location'])
   for n in ['roomTitle','drawWorld','renderCaption','render']:self.compare('genuine-'+phase,n)
   for rep in range(3):self.compare('repeated-'+phase+f'-{rep}','drawWorld')
  self.bank('campaign')
 def fixtures(self):
  # Pure paint fixtures vary only valid presentation/property ranges. These are
  # branch evidence, never claims that story state was earned in the campaign.
  snaps=self.snapshots()
  for caption in range(61):
   self.update({'currentCaption':caption,'navNoticeTicks':0})
   self.compare(f'caption-{caption}','renderCaption',pure=True)
  for notice in range(11):
   self.update({'navNotice':notice,'navNoticeTicks':1});self.compare(f'notice-{notice}','renderCaption',pure=True);self.compare(f'notice-direct-{notice}','navNoticeRender',pure=True)
  self.reset(snaps);self.bank('caption')
  for room in range(8):
   self.update({'location':room});self.compare(f'title-{room}','roomTitle',pure=True)
  self.reset(snaps)
  for board,copy,plan,wedge,y in itertools.product(range(8),[0,1],[0,1],[0,2],[125,126,127]):
   self.update({'location':1,'onApron':0,'p02BoardRecords':board,'p02CopyBunny':copy,'p02PlanAgreed':plan,'wedge':wedge,'motionY':y*64})
   self.compare(f'living-{board}-{copy}-{plan}-{wedge}-{y}','drawLiving',pure=True)
  self.reset(snaps);self.bank('living')
  for lane,speaker,mouth,phase,loop,pose in itertools.product([0,1,2],[1,2,3,4,5,7,8],range(3),[0,1],range(2),range(3)):
   self.update({'motionPhase':phase,'motionLoop':loop,'motionPose':pose}, {'presentationAudio':{'lane':lane,'speaker':speaker,'mouth':mouth}})
   self.compare(f'jack-{lane}-{speaker}-{mouth}-{phase}-{loop}-{pose}','drawJack',pure=True)
  self.reset(snaps);self.bank('jack')
  for lane,speaker,mouth in itertools.product([0,1,2],[1,2,3,4,5,7,8],range(3)):
   self.update(objects={'presentationAudio':{'lane':lane,'speaker':speaker,'mouth':mouth}})
   for who in [2,3]:self.compare(f'living-person-{lane}-{speaker}-{mouth}-{who}','livingPerson',who,pure=True)
   for who in [4,5]:self.compare(f'neighbor-{lane}-{speaker}-{mouth}-{who}','neighborPerson',who,pure=True)
   self.compare(f'rita-{lane}-{speaker}-{mouth}','p03Rita',pure=True)
  self.reset(snaps);self.bank('people')
  for ready,cup,slate,copy,y in itertools.product([0,1],[0,1],range(3),[0,6],[125,126,129,130]):
   self.update({'location':6,'onApron':0,'p02CopyStringer':copy,'motionY':y*64}, {'p03State':{'p03Ready':ready,'p03Padding':cup,'p03Slate':slate}})
   self.compare(f'conservatory-{ready}-{cup}-{slate}-{copy}-{y}','drawP03Conservatory',pure=True)
  self.reset(snaps);self.bank('conservatory')
  for gate,peg,bunting,wedge,y in itertools.product([0,1],[0,1],[0,1,2],[0,1],[130,131]):
   self.update({'location':3,'onApron':0,'motionY':y*64},{'p04State':{'p04Gate':gate,'p04Peg':peg,'p04Bunting':bunting,'p04Wedge':wedge}})
   self.compare(f'side-{gate}-{peg}-{bunting}-{wedge}-{y}','drawSidePassage',pure=True)
  self.reset(snaps)
  for room,apron,x,phase,lane,speaker,mouth in itertools.product([1,3],[0,1],[140,170],[0,1],[0,1],[1,8],[-1,0,1,2,3]):
   self.update({'location':room,'onApron':apron,'motionX':x*64,'motionPhase':phase},{'presentationAudio':{'lane':lane,'speaker':speaker,'mouth':mouth}})
   self.compare(f'felix-{room}-{apron}-{x}-{phase}-{lane}-{speaker}-{mouth}','p04Felix',pure=True)
  self.reset(snaps);self.bank('side')
  # Current owner APIs are invoked, never substituted. Kitchen object availability
  # reflects the actual P08 owner while original P03 placement ranges are varied.
  for towel,napkin,tray,ready in itertools.product([0,1],[0,1],[0,1,2],[0,1]):
   self.update({'location':2,'onApron':0,'tray':tray},{'p03State':{'p03Towel':towel,'p03Napkin':napkin,'p03Ready':ready}})
   self.compare(f'kitchen-{towel}-{napkin}-{tray}-{ready}','drawKitchen')
  self.reset(snaps);self.bank('kitchen')
  for room,apron,entered,door,bunny,tray,wedge in itertools.product(range(7),[0,1],[0,1],[0,1],[0,1],range(3),range(3)):
   self.update({'location':room,'onApron':apron,'houseEntered':entered,'doorOpen':door,'bunnyReady':bunny,'tray':tray,'wedge':wedge})
   self.compare(f'world-{room}-{apron}-{entered}-{door}-{bunny}-{tray}-{wedge}','h6BaseDrawWorld')
  self.reset(snaps)
  for room in range(7):
   self.update({'location':room})
   self.compare(f'block-person-{room}','blockPerson',150,130,4,pure=True)
  # Missing-owner fixtures check original null guards without changing persistent
  # campaign outcomes; state is restored separately after each bounded call group.
  for missing in ('p05','p06','p07','p08','p09','presentation'):
   self.reset(snaps);self.update({missing:0})
   for room in range(7):
    self.update({'location':room,'onApron':0})
    for name in ('h6BaseDrawWorld','renderCaption','drawJack','drawKitchen','drawP03Conservatory'):
     self.compare(f'null-{missing}-room-{room}',name)
  self.reset(snaps);self.bank('world')
 def coverage(self):
  out=[]
  for index,h in enumerate(self.q):
   vm=h.vm;r=vm.trace;rows=[]
   for number in [0,991]:
    if number not in vm.modules:continue
    for name in MOVED:
     obj=vm.objects['cakood' if number==0 else 'sceneRenderer'];module,entry=vm.resolve(obj,name)
     if module.number!=number:continue
     points=vm.method_boundaries(module,entry);branches=[pc for pc in points if vm.opnames[vm.decode(module,pc)[0]] in ('BT','BNT')]
     seen=[pc for pc in points if (number,name,pc) in r.instructions]
     missed=[{'pc':pc,'op':vm.opnames[vm.decode(module,pc)[0]],'taken':take} for pc in branches for take in [False,True] if (number,name,pc,take) not in r.branches]
     rows.append({'module':number,'method':name,'instructions':len(points),'seen':len(seen),'branch_edges':2*len(branches),'uncovered_branch_edges':missed})
   out.append({'variant':index,'source_variant':index>=2,'emitted':rows,'source_methods':sorted(list(getattr(vm,'source_calls',set()))),'source_instruction_count':len(getattr(vm,'source_instructions',set())),'source_branch_outcomes':len(getattr(vm,'source_branches',set()))})
  dump(H/'evidence/matrix-coverage.json',out);return out
 def run(self):
  try:self.campaign();self.fixtures()
  finally:self.coverage()
  self.bank('complete')
if __name__=='__main__':Matrix().run()
