"""Pixel-accurate static previews, not stock runtime evidence."""
import json,struct,itertools,hashlib
from common import ROOT,Guard,write_json,sha
_entry_guard=Guard("preview") if __name__=="__main__" else None
from PIL import Image,ImageDraw
import numpy as np
from common import ROOT,Guard,write_json,sha
from inspect_view import decode_view
from geometry import *
class Renderer:
 def __init__(self):
  self.palette=json.loads((ROOT/'reference/palette-999.json').read_text())['rgb'];self.views={};self.cache={};self.font=(ROOT/'reference/000.font.bin').read_bytes()
  for v in [214,219,221,224,227,228,305]:self.views[v]=decode_view((ROOT/('resources' if v in [228,305] else 'reference')/f'{v}.view.bin').read_bytes())
 def cel(self,v,c=0,l=0):
  key=(v,c,l)
  if key not in self.cache:
   b=self.views[v][l][c];im=Image.frombytes('P',(b['width'],b['height']),b['pixels']);im.putpalette(sum(self.palette,[]));im.info['transparency']=255;self.cache[key]=im.convert('RGBA')
  return self.cache[key]
 def put(self,canvas,v,c,origin,l=0,scale=128):
  im=self.cel(v,c,l)
  if scale!=128:im=im.resize((im.width*scale//128,im.height*scale//128),Image.Resampling.NEAREST)
  canvas.alpha_composite(im,tuple(origin))
 def actor(self,canvas,feet=(42,140),scale=127,v=214,pose=0,loop=0):
  self.put(canvas,v,pose,(feet[0]-26*scale//128,feet[1]-78*scale//128),loop,scale)
 def font0(self,canvas,text,pos,color=(251,231,181,255)):
  x,y=pos
  for ch in text:
   o=struct.unpack_from('<H',self.font,6+ord(ch)*2)[0];w,h=self.font[o:o+2]
   for yy in range(h):
    for xx in range(w):
     if self.font[o+2+yy] & (128>>xx):canvas.putpixel((x+xx,y+yy),color)
   x+=w
 def clean(self,marks=False,gate_open=True):
  im=self.cel(305).copy()
  if not gate_open:self.put(im,228,11,(281,36))
  if marks:
   for c,xy in MARKS:self.put(im,228,c,xy)
  return im
 def pa_staging(self,im,connected=1,source=1,aim=2):
  for c in staging_components(connected,source,aim):self.put(im,227,c,P05['hardware_origins'][c])
  self.put(im,227,8,P05['slate_origin']);self.font0(im,'TAPE',(185,84),(14,17,30,255));self.font0(im,'MIC',(212,84),(14,17,30,255))
 def p05(self,loan=True,connected=1,source=1,aim=2,actor=True,feet=(42,140),scale=127,marks=True,gate_open=True):
  im=self.clean(marks,gate_open)
  if loan:self.pa_staging(im,connected,source,aim)
  if actor:self.actor(im,feet,scale)
  return im
 def p08(self,positions,facing=1,unpacked=False,actors=False,connected=1,source=1):
  im=self.clean(True);items=[]
  for obj,pos in zip(OBJECTS,positions):
   if obj=='pa_kit' and pos==0:continue
   c=pa_layout_cel(connected,source,facing) if obj=='pa_kit' else CELS[obj];xy=ORIGINS[obj][pos]
   # Explicit visual stacking. Screen behind service/table; slate above table.
   z={'completed_screen':0,'serving_table':1,'pa_kit':2,'ceramic_carrier':3,'credit_slate':4}[obj]
   items.append((z,obj,c,xy))
  for z,obj,c,xy in sorted(items):
   if obj=='ceramic_carrier' and unpacked:
    # Unpacked service is the same bundle identity, displayed as the exact P03
    # plate motif in three laid-out positions; no food or displayed ceramic panel.
    plate=self.cel(228,6).resize((15,8),Image.Resampling.NEAREST)
    for dx,dy in [(0,21),(13,18),(24,22)]:im.alpha_composite(plate,(xy[0]+dx,xy[1]+dy))
   else:self.put(im,228,c,xy)
  if positions[1]==0:self.pa_staging(im,connected,source)
  else:
   xy=ORIGINS['pa_kit'][positions[1]];self.put(im,227,8,(xy[0]+55,xy[1]+(21 if positions[1]==4 else 27)))
  if actors:self.actor(im)
  return im
 def hud(self,im,label):
  out=Image.new('RGBA',(320,200),(14,17,30,255));out.alpha_composite(im,(0,0));d=ImageDraw.Draw(out);d.rectangle((0,0,319,11),fill=(14,17,30,255));self.font0(out,'COURTYARD',(6,2));self.font0(out,label[:45],(6,146));self.font0(out,'LOOK  USE  PUSH  PULL  WALK',(6,158));self.font0(out,'STATIC PREVIEW / NOT NATIVE PLAY',(6,185));return out

def run():
 g=_entry_guard or Guard('preview');r=Renderer();p=ROOT/'previews';(p/'p05-states').mkdir(exist_ok=True);(p/'all-layouts').mkdir(exist_ok=True)
 def save(im,name):im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(p/name)
 save(r.clean(),'clean-background-4x.png');save(r.clean(True,False),'closed-gate-4x.png');save(r.p05(),'p05-staging-4x.png');save(r.p05(gate_open=False),'p05-staging-gate-closed-4x.png');save(r.hud(r.p05(),'KIT STAGED / CREDIT READER71'),'p05-staging-with-hud-4x.png');save(r.p05(False),'pre-loan-4x.png')
 for conn,src,aim in itertools.product(range(2),range(2),range(3)):
  r.p05(True,conn,src,aim).save(p/'p05-states'/f'connection{conn}-source{src}-aim{aim}.png')
 intended=(1,2,3,1,1);save(r.p08((0,0,0,0,0),actors=True),'p08-unplaced-4x.png');save(r.p08(intended,unpacked=True,actors=True),'p08-intended-layout-4x.png')
 im=r.p05();d=ImageDraw.Draw(im)
 for name,spec in [*EXITS.items(),('hatch',HATCH),('slate',P05['slate']),('kit',P05['kit'])]:
  a,b,c,e=spec['rect'];d.rectangle((a,b,c-1,e-1),outline=(0,255,255));x,y,sc=spec['approach'];d.line((x-2,y,x+2,y),fill=(255,255,255));d.line((x,y-2,x,y+2),fill=(255,255,255))
 save(im,'p05-hotspots-4x.png')
 # Factor sheet explicitly covers wrong screen placements and both PA directions.
 sheet=Image.new('RGBA',(1280,432),(14,17,30,255))
 for col,pos in enumerate(range(1,5)):
  vals=list(intended);vals[2]=pos
  for row,(facing,unpacked) in enumerate([(1,False),(1,True),(2,True)]):sheet.alpha_composite(r.p08(tuple(vals),facing,unpacked,True),(col*320,row*144))
 sheet.save(p/'screen-directions-service-matrix.png')
 # Complete Cartesian render hashes preserve full native-pixel comparisons.
 # The superset includes logically impossible snapshots to test total rendering.
 index=[]
 for positions in itertools.product(range(5),repeat=5):
  for facing,unpacked in itertools.product([1,2],[False,True]):
   im=r.p08(positions,facing,unpacked)
   index.append({'ordinal':len(index),'positions':positions,'facing':facing,'unpacked':unpacked,'rgba_sha256':hashlib.sha256(im.tobytes()).hexdigest()})
 counter=len(index);write_json(p/'all-layouts/render-hashes.json',index)
 # Complete PA wiring/source/facing projection matrix, including prior tampering.
 hardware=Image.new('RGBA',(1280,576),(0,0,0,255));case=0
 for connected,source,facing in itertools.product([0,1],[0,1],[1,2]):
  im=r.p08(intended,facing,True,False,connected,source);hardware.alpha_composite(im,(case%4*320,case//4*144));case+=1
 hardware.save(p/'p08-preserved-pa-hardware-matrix.png')
 # Every accepted actor's actual direction/pose/approach bounds are previewed.
 targets=[*[(n,s['approach']) for n,s in EXITS.items()],('hatch',HATCH['approach']),('kit',P05['kit']['approach']),('slate',P05['slate']['approach']),*APPROACHES.items()]
 sheet=Image.new('RGBA',(320*5,144*len(targets)),(0,0,0,255))
 for row,(name,(x,y,scale)) in enumerate(targets):
  for col,pose in enumerate(range(5)):
   im=r.p05(actor=False);r.actor(im,(x,y),scale,pose=pose);sheet.alpha_composite(im,(col*320,row*144))
 sheet.save(p/'jackie-all-approaches-all-poses.png');g.done(p05_hardware_states=12,p08_cartesian_composites=counter,scope='Static composites only; not native input/render/save acceptance',inputs={'manifest':sha(ROOT/'manifest.json'),'geometry':sha(ROOT/'src/geometry.py'),'renderer':sha(ROOT/'src/render.py')})
if __name__=='__main__':run()
