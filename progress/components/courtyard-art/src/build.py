#!/usr/bin/env python3
"""Deterministic asset conversion and simple native plan-symbol construction.
No painted scene/character generation. All creative pixels come from recorded
imagegen masters or the exact preserved original game views.
"""
from pathlib import Path
import json,hashlib
from common import ROOT,sha,write_json,require,Guard
_entry_guard=Guard("build") if __name__=="__main__" else None
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
from common import ROOT,sha,write_json,require,Guard
from view_writer import Cel,encode_view
from inspect_view import decode_view

def run():
 g=_entry_guard or Guard('build');pal=json.loads((ROOT/'reference/palette-999.json').read_text())['rgb'];arr=np.array(pal[:255],dtype=np.int32)
 def quant(im):
  a=np.array(im.convert('RGBA'));rgb=a[:,:,:3].reshape(-1,3).astype(np.int32);idx=np.empty(len(rgb),dtype=np.uint8)
  for s in range(0,len(rgb),2048):idx[s:s+2048]=((rgb[s:s+2048,None,:]-arr[None,:,:])**2).sum(axis=2).argmin(axis=1)
  idx=idx.reshape(a.shape[:2]);idx[a[:,:,3]<128]=255;o=Image.fromarray(idx,'P');o.putpalette(sum(pal,[]));o.info['transparency']=255;return o
 def native(n,c=0):
  v=decode_view((ROOT/'reference'/f'{n}.view.bin').read_bytes())[0][c];im=Image.frombytes('P',(v['width'],v['height']),v['pixels']);im.putpalette(sum(pal,[]));im.info['transparency']=255;return im
 manifest={'classification':'New original courtyard reconstruction; copied original assets remain byte-identical','cels':[],'resources':{},'quantizer':'nearest squared RGB index0..254, alpha<128 =>255, ties first index, no dither','native_refs':{},'sources':{}}
 def save_view(n,parts):
  native_cels=[]
  for c,(name,im,source) in enumerate(parts):
   if im.mode!='P':im=quant(im)
   p=ROOT/'indexed-cels'/f'{n}-loop00-cel{c:02d}-{name}.png';im.save(p,transparency=255,optimize=False);native_cels.append(Cel(*im.size,im.tobytes()));a=np.array(im);ys,xs=np.where(a!=255)
   manifest['cels'].append({'view':n,'loop':0,'cel':c,'name':name,'file':str(p.relative_to(ROOT)),'size':list(im.size),'opaque_bbox':[int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1],'pixel_sha256':hashlib.sha256(im.tobytes()).hexdigest(),'source':source,'sha256':sha(p)})
  data=encode_view([native_cels]);check=decode_view(data)
  require(all(x.pixels==y['pixels'] for x,y in zip(native_cels,check[0])),'Independent native decoder mismatch')
  p=ROOT/'resources'/f'{n}.view.bin';p.write_bytes(data);manifest['resources'][str(n)]={'file':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':len(data),'cel_count':len(parts)}
 bg=Image.open(ROOT/'source-masters/courtyard-clean-v1.png').convert('RGBA').resize((320,144),Image.Resampling.LANCZOS)
 save_view(305,[('courtyard-clean',bg,{'master':'source-masters/courtyard-clean-v1.png','crop':'full','resize':[320,144]})])
 master=Image.open(ROOT/'source-masters/screen-table-v1.png').convert('RGBA');alpha=np.array(master)[:,:,3]>=128;labs,n=label(alpha);counts=np.bincount(labs.ravel());counts[0]=0;objects=sorted(np.argsort(counts)[-2:],key=lambda i:int(np.where(labs==i)[1].min()))
 props=[]
 for name,idx,size in zip(['completed-screen','serving-table'],objects,[(54,57),(66,30)]):
  ys,xs=np.where(labs==idx);box=[int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1];part=master.crop(box);a=np.array(part);a[:,:,3]=np.where(labs[box[1]:box[3],box[0]:box[2]]==idx,a[:,:,3],0);part=Image.fromarray(a);part.save(ROOT/'components'/f'{name}-source.png');props.append((name,part.resize(size,Image.Resampling.LANCZOS),{'master':'source-masters/screen-table-v1.png','crop':box,'alpha_cleanup':'largest two source connected components, ordered left to right','resize':list(size)}))
 # PA is a palette-exact nearest-neighbor derivative of the accepted view227.
 # Do not include handcart7 or marks14/15. The slate is a separate original item.
 orig={0:(143,92),1:(213,61),2:(213,61),3:(213,61),4:(123,91),5:(132,110),6:(133,92),9:(154,71),10:(144,84),11:(144,84),12:(193,92),13:(184,92)}
 for facing,aim in [('inward',3),('neighbor',1)]:
  im=Image.new('P',(128,68),255);im.putpalette(sum(pal,[]));im.info['transparency']=255
  for c in [6,0,9,11,13,4,aim]:
   part=native(227,c);xy=orig[c];im.paste(part,(xy[0]-123,xy[1]-61),Image.fromarray(np.where(np.array(part)!=255,255,0).astype(np.uint8),'L'))
  props.append((f'pa-{facing}',im.resize((86,46),Image.Resampling.NEAREST),{'view':227,'cels':[6,0,9,11,13,4,aim],'unscaled_canvas':[128,68],'resize':[86,46],'filter':'nearest','state':'P08 retained tested live source; use exact227 projection for P05 hardware state'}))
 # Preserve P03 carrier/slate indices; no newly invented service design.
 for name,c in [('ceramic-carrier',1),('rita-credit-slate',4),('service-plate',7)]:props.append((name,native(224,c),{'view':224,'loop':0,'cel':c,'conversion':'exact pixel indices'}))
 # These are simple authored symbols, not substitute raster scene artwork.
 cream=tuple(pal[1]);ink=(251,220,145,255)
 for name,size in [('hatch-mark',(66,16)),('wall-mark',(64,16)),('alcove-mark',(62,16)),('lane-chevrons',(276,10))]:
  im=Image.new('RGBA',size,(0,0,0,0));d=ImageDraw.Draw(im)
  if name=='lane-chevrons':
   for x in range(3,size[0]-10,18):d.line([(x,1),(x+7,4),(x,7)],fill=ink,width=2);d.line([(x+5,1),(x+12,4),(x+5,7)],fill=ink,width=1)
  else:
   d.polygon([(2,12),(9,3),(size[0]-9,3),(size[0]-2,12)],outline=ink,width=1)
   if name=='hatch-mark':d.line([(25,8),(42,8),(39,11),(28,11),(25,8)],fill=ink,width=1);d.arc((28,3,39,10),180,360,fill=ink)
   elif name=='wall-mark':d.polygon([(28,7),(31,7),(35,4),(35,12),(31,9),(28,9)],outline=ink);d.arc((35,3,44,13),270,90,fill=ink)
   else:d.rectangle((25,3,38,11),outline=ink);d.line((26,12,25,14),fill=ink);d.line((37,12,38,14),fill=ink)
  props.append((name,im,{'authored_symbol':name,'geometry_in':'src/build.py','not_dialogue':True}))
 gate=native(226,0).crop((27,0,76,67)).transpose(Image.Transpose.FLIP_LEFT_RIGHT).resize((34,63),Image.Resampling.NEAREST)
 props.append(('side-gate-closed',gate,{'view':226,'loop':0,'cel':0,'crop':[27,0,76,67],'mirror':'horizontal courtyard-side projection','resize':[34,63],'filter':'nearest','state':'P04 gate RESTING0/CLOSED2 only'}))
 # Preserve deliberately altered P05 wiring/source in later P08 projections.
 # Cels12..17 fill the other six connection/source/direction combinations.
 for conn,source in [(0,0),(0,1),(1,0)]:
  for facing,aim in [('inward',3),('neighbor',1)]:
   im=Image.new('P',(128,68),255);im.putpalette(sum(pal,[]));im.info['transparency']=255
   choices=[6 if conn else 5,0,9,11 if source else 10,13 if conn else 12,4,aim]
   for c in choices:
    part=native(227,c);xy=orig[c];im.paste(part,(xy[0]-123,xy[1]-61),Image.fromarray(np.where(np.array(part)!=255,255,0).astype(np.uint8),'L'))
   props.append((f'pa-connection{conn}-source{source}-{facing}',im.resize((86,46),Image.Resampling.NEAREST),{'view':227,'cels':choices,'resize':[86,46],'filter':'nearest','preserve_prior_state':True}))
 save_view(228,props)
 for p in sorted((ROOT/'reference').glob('*.bin')):manifest['native_refs'][p.name]=sha(p)
 for p in sorted((ROOT/'source-masters').glob('*.png')):manifest['sources'][p.name]={'sha256':sha(p),'size':list(Image.open(p).size)}
 write_json(ROOT/'manifest.json',manifest);write_json(ROOT/'SOURCE-MASTERS.json',{'tool':'built-in image_gen.imagegen','prompts':'GENERATION-PROMPTS.json','masters':manifest['sources']});g.done(resources=manifest['resources'])
if __name__=='__main__':run()
