#!/usr/bin/env python3
"""Decode original resources; measure pure geometry and make static references.

Nearest-neighbor pixel composites are analysis artifacts, not native captures.
No campaign state, actor ownership, or positive P09 progression is supplied.
"""
from pathlib import Path
import hashlib,json,struct,sys
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'tools'))
from view_decoder import decode_view
from derive import dump,sha,require
R=H/'frozen/foundation/frozen/p08/snapshot/resources'

def intersect(a,b):return a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]
def scale_for(y):return ((y-50)*128+45)//90
def cel(number,loop,index):return decode_view((R/f'{number:03}.view.bin').read_bytes())[loop][index]
def sprite(number,loop,index,xy,scale=128):
 c=cel(number,loop,index);palette=(R/'999.palette.bin').read_bytes()[37:]
 im=Image.frombytes('P',(c['width'],c['height']),c['pixels']);im.putpalette(palette);im.info['transparency']=c['clear_key']
 im=im.convert('RGBA')
 if scale!=128:im=im.resize((c['width']*scale//128,c['height']*scale//128),Image.Resampling.NEAREST)
 canvas=Image.new('RGBA',(320,144));canvas.alpha_composite(im,xy);return canvas
def jack(number,loop,index,feet):
 x,y=feet;s=scale_for(y);return sprite(number,loop,index,(x-26*s//128,y-78*s//128),s)
def overlap(a,b):return sum(bool(x and y) for x,y in zip(a.getchannel('A').getdata(),b.getchannel('A').getdata()))
def actor(which,frame=0):
 if which=='stringer':return sprite(222,1,frame,(149,61),108)
 s=scale_for(130);return sprite(223,1,frame,(252-26*s//128,130-78*s//128),s)
def tags(im,contract):
 d=ImageDraw.Draw(im);palette=(R/'999.palette.bin').read_bytes()[37:];colors=[tuple(palette[i:i+3]) for i in range(0,len(palette),3)]
 for row in contract['tag_shapes']:
  t,l,b,r=row['rect'];x,y,end=row['thread']
  for rect,col in [((x,y,x+1,end),0),((l,t,r,b),0),((l+1,t+1,r-1,b-1),1),((l+2,t+3,r-2,t+4),0),((l+2,t+5,r-2,t+6),0)]:
   x0,y0,x1,y1=rect;d.rectangle((x0,y0,x1-1,y1-1),fill=colors[col])
 return im
def measure():
 c=json.loads((H/'GEOMETRY-CONTRACT.json').read_text());folder=H/'references';folder.mkdir(exist_ok=True)
 meta={};poses=[]
 for n in (214,216,222,223):
  for loop,frames in enumerate(decode_view((R/f'{n}.view.bin').read_bytes())):
   for frame,row in enumerate(frames):
    mask=Image.frombytes('L',(row['width'],row['height']),bytes(255 if p!=row['clear_key'] else 0 for p in row['pixels']))
    bbox=list(mask.getbbox());meta[f'{n}/{loop}/{frame}']={'size':[row['width'],row['height']],'opaque_bbox':bbox,'clear_key':row['clear_key']}
    if n in (214,216):poses.append((n,loop,frame))
 result={}
 for name,point in [('front',c['controls'][5]['approach']),('side',c['controls'][6]['approach']),('historical_front',c['historical_geometry_rejected']['front'])]:
  samples=[]
  for n,l,f in poses:
   me=jack(n,l,f,point)
   samples.append({'cel':[n,l,f],'overlap_pixels':{who:max(overlap(me,actor(who,m)) for m in range(3)) for who in ('stringer','rita')}})
  result[name]={'feet':point,'poses':samples,'maximum_actor_overlap':max(max(x['overlap_pixels'].values()) for x in samples)}
 require(result['front']['maximum_actor_overlap']==result['side']['maximum_actor_overlap']==0,'Proposed point overlaps an actor')
 require(result['historical_front']['maximum_actor_overlap']>0,'Historical overlap counterexample absent')
 font=(R/'000.font.bin').read_bytes();glyphs=struct.unpack_from('<H',font,2)[0];height=struct.unpack_from('<H',font,4)[0]
 def width(text):
  total=0
  for ch in text:
   code=ord(ch);require(code<glyphs,'Unrepresentable UI label');offset=struct.unpack_from('<H',font,6+2*code)[0];total+=font[offset]
  return total
 label_metrics={x:{'width':width(x),'height':height} for x in sorted(set(row['label'] for row in c['controls'])|set(c['labels'].values()))}
 for row in c['controls'][-2:]:
  t,l,b,r=row['rect'];v=label_metrics[row['label']];require(v['width']<=r-l-4 and v['height']<=b-t-4,'Floor view label does not fit')
 manifest=json.loads((H/'frozen/foundation/frozen/scene/generated/manifest.json').read_text());records={r['record_id']:r for r in manifest['routes']}
 require(records['P09.READ.001']['source_text']==c['chair_tag_text'],'Canonical tag drift')
 require(records['P09.LABEL.001']['source_text']==c['labels']['395'],'Canonical chair label drift')
 require(records['P09.INVENTORY.001']['source_text']==c['labels']['399'],'Canonical card label drift')
 for name,point in [('side',c['controls'][6]['approach']),('front',c['controls'][5]['approach']),('historical-front',c['historical_geometry_rejected']['front'])]:
  im=tags(sprite(302,0,0,(0,0)),c)
  im.alpha_composite(sprite(224,0,8,(63,46)));im.alpha_composite(sprite(224,0,10,(282,58)))
  im.alpha_composite(actor('stringer'));im.alpha_composite(actor('rita'));im.alpha_composite(jack(214,0,0,point))
  canvas=Image.new('RGB',(960,486),'#111827');canvas.paste(im.resize((960,432),Image.Resampling.NEAREST).convert('RGB'),(0,42))
  draw=ImageDraw.Draw(canvas);draw.text((12,8),f'DECODED STATIC REFERENCE, NOT NATIVE CAPTURE | {name} feet {point} | newly authored tag marks',fill='white')
  canvas.save(folder/f'{name}-static-reference.png')
 # Original unmodified background and all relevant cel metadata stay separate.
 sprite(302,0,0,(0,0)).convert('RGB').save(folder/'original-background302.png')
 provenance={str(p.relative_to(H)):sha(p) for p in [R/f'{n:03}.view.bin' for n in (214,216,222,223,224,302)]+[R/'000.font.bin',R/'999.palette.bin']}
 proof={'status':'PASS_STATIC_MEASUREMENTS','native_capture':False,'resource_provenance':provenance,'all_actor_cels':meta,'jackie_pose_count':len(poses),'approaches':result,'font_labels':label_metrics,'font_floor_control_padding':4,'canonical_routes':{n:{k:records[n][k] for k in ('document_id','first_page','page_count','source_text','source_text_json_sha256')} for n in ('P09.LABEL.001','P09.READ.001','P09.INVENTORY.001')},'tag_draw_order':'background, new tag marks, existing props, then original actor depth ordering; no overlay above actor pixels','control_count':7,'mask_rounding_limit':'Offline nearest-neighbor decoded reference with conservative one-pixel host bounds. Native scaling/visual acceptance is deferred.'}
 dump(H/'evidence/MEASUREMENTS.json',proof);return proof
if __name__=='__main__':
 r=measure();print('PASS_STATIC_MEASUREMENTS',r['jackie_pose_count'],'Jackie poses; historical overlap',r['approaches']['historical_front']['maximum_actor_overlap'])
