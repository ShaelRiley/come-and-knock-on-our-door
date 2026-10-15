#!/usr/bin/env python3
"""P12 status backing/receipt checks with explicit admission/device fixtures, not native acceptance."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
SOURCE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(SOURCE/'tests'),str(SOURCE/'tools')]
from presentation_vm import PresentationVM,base
from check_late_ui import display_rectangle,intersects
from inspect_opening_view import decode_view
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
BACKING=(19,130,111,140)

class WelcomeFixture(PresentationVM):
 def __init__(self,build=None,kind=5):
  super().__init__(build);self.kind=kind;self.active=True;self.valid=True;self.successor=False;self.flush_witness=[]
  self.h.p.update(location=4,onApron=0,motionPhase=0,opening=0,paused=0,menuOpen=0,uiPanel=0,uiControlCount=0,uiFailure=0,p05=0,p06=0,p08=0,p09=0,currentCaption=0,navNoticeTicks=0)
  self.arrays(994)['h12Lease'][0]=1
  for i in range(7):
   self.arrays(994)['h12Actors'][12*i]=self.call(self.instance(994),'h12SuccessorObject',(i,))
   self.arrays(994)['h12Actors'][12*i+2]=4
 def call(self,obj,name,args=()):
  if obj.module.number==995 and name=='h13Has':return int(self.successor)
  if obj.module.number==994:
   if name=='h12Active':return int(self.active)
   if name=='h12SuccessorValid':return int(self.valid)
   if name=='p12Present':return int(args[0]==self.kind)
  return super().call(obj,name,args)
 def kernel(self,k,args):
  if self.knames.get(k)=='Graph' and args[0]==12:self.flush_witness.append(list(self.arrays(994)['h12WelcomePaint']))
  return super().kernel(k,args)

class CompositionFixture(WelcomeFixture):
 def call(self,obj,name,args=()):
  key=(obj.module.number,name)
  if key==(0,'drawWorld'):return self.call(self.instance(994),'h12WelcomeFrame',(2,))
  if key==(0,'p03Checkpoint'):return 1  # Observed three-line preparation header.
  if key==(0,'uiRender'):return 0  # Unrelated footer controls modeled out here.
  if key==(0,'renderCaption'):return 0  # No unrelated scene-reader caption.
  if key==(994,'h12Frame'):return 0  # No campaign progress earned by composition fixture.
  return super().call(obj,name,args)

def state(v):
 return {'properties':{n:dict(v.instance(n).p) for n in (994,995,996)},'locals':{n:{k:list(a) for k,a in v.arrays(n).items() if not(n==994 and k=='h12WelcomePaint')} for n in (994,995,996)}}

def label(v,text):
 return [(i,a) for i,(name,a) in enumerate(v.ktrace) if name=='Display' and base.read_string(a[0])==text]

def run(build=None,reference=False):
 cases=[];v=WelcomeFixture(build);p=v.instance(994);before=state(v)
 assert v.call(p,'h12WelcomeFrame',(2,))==1 and state(v)==before
 index,args=label(v,'SHARED CONFETTI')[0];rect=display_rectangle(v,args)
 assert rect==(20,131,110,139) and rect[3]-rect[1]==8
 assert args[2:4]==(20,131)
 assert args[args.index(102)+1]==2 and args[args.index(105)+1]==0
 assert args[args.index(106)+1]==140
 cases.append('actual bundled-font caption remains one row at original origin/color/width')
 fills=[(i,a) for i,(name,a) in enumerate(v.ktrace[:index]) if name=='Graph' and a[0]==11]
 back=[(i,a) for i,a in fills if (a[2],a[1],a[4],a[3])==BACKING and a[6]==0]
 if reference:assert not back and len(fills)==20
 else:
  assert len(back)==1 and back[0][0]==index-1
  assert len(fills)==21
  assert BACKING==(rect[0]-1,rect[1]-1,rect[2]+1,rect[3]+1)
  # Every modeled background pixel inside the glyph box has uniform contrast;
  # the20 existing flourish rectangles precede it, rather than cover the text.
  pixels={(x,y):(7 if (x+y)%2 else 12) for y in range(rect[1],rect[3]) for x in range(rect[0],rect[2])}
  for _,packet in fills:
   _,top,left,bottom,right,_,color,*_=packet
   for x,y in pixels:
    if left<=x<right and top<=y<bottom:pixels[x,y]=color
  assert set(pixels.values())=={0},'Actual ordered fill packets must remove all adversarial/background/confetti contrast under glyphs'
 cases.append('reference unbacked floor collision reproduced' if reference else 'actual backing is last paint immediately before text, uniform black and exactly one-pixel padding')
 assert not any(n=='Graph' and a[0]==12 for n,a in v.ktrace)
 assert list(v.arrays(994)['h12WelcomePaint'])==[5,0,0,0,0,0]
 cases.append('phase2 paints without flush/publication; same serial witness only')
 v.ktrace.clear();assert v.call(p,'h12Controls')==1
 a=v.arrays(0);controls=[]
 for i in range(v.h.p['uiControlCount']):
  box=(a['uiLefts'][i],a['uiTops'][i],a['uiRights'][i],a['uiBottoms'][i]);controls.append((a['uiPayloads'][i],box));assert not intersects(BACKING,box)
 assert len(controls)==9 and dict(controls)[420]==(166,128,304,142)
 assert BACKING[1]>=43 and BACKING[3]<=144
 cases.append('all seven actual companion controls/rack/rotate and header/footer remain clear')
 v.ktrace.clear();assert v.call(p,'h12SuccessorPaint')==1;body_count=0
 for name,a in v.ktrace:
  if name!='DrawCel':continue
  view,loop,cel,left,top,_,sx,sy=a;c=decode_view(v.resources[0,view])[loop][cel];w=c['width']
  for i,value in enumerate(c['pixels']):
   if value==c['clear_key']:continue
   x,y=left+(i%w)*sx//128,top+(i//w)*sy//128
   assert not(BACKING[0]<=x<BACKING[2] and BACKING[1]<=y<BACKING[3])
  assert v.resources[0,view]==(SOURCE/'assets/resources'/f'{view}.view.bin').read_bytes();body_count+=1
 assert body_count==7
 cases.append('actual original-art companion draw packets do not intersect the tight backing')
 v.ktrace.clear();assert v.call(p,'h12WelcomeFrame',(1,))==1
 assert v.flush_witness==[[5,0,0,0,0,0]]
 assert list(v.arrays(994)['h12WelcomePaint'])==[0,0,0,5,0,0] and state(v)==before
 cases.append('existing phase1 Graph12 happens before unchanged visible receipt publication')
 bad=WelcomeFixture(build);bad.call(bad.instance(994),'h12WelcomeFrame',(2,));bad.arrays(994)['h12WelcomePaint'][2]=1;bad.ktrace.clear()
 assert bad.call(bad.instance(994),'h12WelcomeFrame',(1,))==0
 assert not bad.flush_witness and bad.arrays(994)['h12WelcomePaint'][3]==0
 cases.append('mismatched paint serial cannot flush or acknowledge')
 for name,changes in [('wrong room',{'location':3}),('apron',{'onApron':1}),('walking',{'motionPhase':1})]:
  q=WelcomeFixture(build);q.h.p.update(changes);stable=state(q)
  assert q.call(q.instance(994),'h12WelcomeFrame',(2,))==0
  assert not any(n in {'Graph','Display','DrawCel'} for n,a in q.ktrace) and state(q)==stable and not any(q.arrays(994)['h12WelcomePaint']);cases.append(name+' stays unpainted/unacknowledged')
 for name,field in [('inactive','active'),('invalid successor','valid'),('successor owner','successor')]:
  q=WelcomeFixture(build);setattr(q,field,field=='successor');stable=state(q)
  assert q.call(q.instance(994),'h12WelcomeFrame',(2,))==0
  assert not any(n in {'Graph','Display','DrawCel'} for n,a in q.ktrace) and state(q)==stable and not any(q.arrays(994)['h12WelcomePaint']);cases.append(name+' keeps the existing fail-closed context')
 q=WelcomeFixture(build,kind=7);stable=state(q);assert q.call(q.instance(994),'h12WelcomeFrame',(2,))==1
 assert not label(q,'SHARED CONFETTI') and len(label(q,'WELCOME SURFACE CLEARED'))==1 and state(q)==stable
 cases.append('cleared welcome branch keeps original caption/backing and unchanged state')
 q=CompositionFixture(build);q.call(q.h,'render');at,_=label(q,'SHARED CONFETTI')[0]
 later=[a for name,a in q.ktrace[at+1:] if name=='Graph' and a[0]==11]
 assert any(a[1:5]==(0,0,43,320) for a in later),later
 assert not any(intersects(BACKING,(a[2],a[1],a[4],a[3])) for a in later)
 cases.append('actual Main.render header clear occurs later and preserves world caption; y33 would be erased')
 return {'status':'REFERENCE_DEFECT_REPRODUCED_NOT_NATIVE' if reference else 'PASS_EMITTED_NOT_NATIVE','case_count':len(cases),'cases':cases,'caption_rectangle':rect,'backing_rectangle':BACKING,'controls':controls,'compile_receipt_sha256':SHA((Path(build) if build else SOURCE/'build/coherent')/'compile-receipt.json'),'native_acceptance':False,'limits':['P12/successor admissions and cue-kind availability are explicit fixtures; no campaign earned.','Real emitted WelcomeFrame, control registration, draw packets, bundled font and phase1 witness comparisons execute.','Composition fixture retains actual Main header clear with unrelated footer/reader and late-progress hooks modeled out.','Fixed companion opaque projection is a geometry model; variable player positions and native visual/audio acceptance remain separate.']}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--build',type=Path);p.add_argument('--reference',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args()
 if a.output:assert not a.output.exists(),'Refuse prior evidence overwrite'
 result=run(a.build,a.reference)
 if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result))
