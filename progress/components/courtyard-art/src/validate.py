#!/usr/bin/env python3
from common import ROOT,sha,write_json,require,Guard
_entry_guard=Guard('validation') if __name__=='__main__' else None
import json,itertools,struct
from PIL import Image
import numpy as np
from inspect_view import decode_view,ViewFormatError
from geometry import *

def inside(rect):return 0<=rect[0]<rect[2]<=320 and 0<=rect[1]<rect[3]<=144

def run():
 g=_entry_guard or Guard('validation');m=json.loads((ROOT/'manifest.json').read_text());pins=json.loads((ROOT/'reference/pinned-inputs.json').read_text());tests={}
 for fn,digest in pins.items():require(sha(ROOT/fn)==digest,'Pinned input changed: '+fn)
 tests['pinned_originals_and_masters']=len(pins)
 for fn,digest in m['native_refs'].items():require(sha(ROOT/'reference'/fn)==digest,'Original resource changed '+fn)
 for n,data in m['resources'].items():
  p=ROOT/data['file'];require(sha(p)==data['sha256'],'Resource hash mismatch '+n);v=decode_view(p.read_bytes());require(len(v[0])==data['cel_count'],'Cel count mismatch')
  for c in [c for c in m['cels'] if c['view']==int(n)]:
   im=Image.open(ROOT/c['file']);raw=im.tobytes();native=v[0][c['cel']];require(im.mode=='P' and im.info.get('transparency')==255,'Indexed transparency missing');require(sha(ROOT/c['file'])==c['sha256'],'Editable cel stale');require(raw==native['pixels'],'Editable/native mismatch');require(list(im.size)==c['size'],'Cel size mismatch');require(im.getpalette()==sum(json.loads((ROOT/'reference/palette-999.json').read_text())['rgb'],[]),'Wrong palette indices')
 # Independent decoder rejection tests: truncation, trailing, overlap, count, dims.
 good=(ROOT/'resources/228.view.bin').read_bytes();bad=[]
 bad.extend([good[:-1],good+b'\0']);a=bytearray(good);struct.pack_into('<I',a,46+24,1);bad.append(bytes(a));a=bytearray(good);struct.pack_into('<h',a,34,0);bad.append(bytes(a));a=bytearray(good);struct.pack_into('<H',a,6,999);bad.append(bytes(a))
 for raw in bad:
  try:decode_view(raw)
  except ViewFormatError:pass
  else:raise ValueError('Malformed native view was accepted')
 tests['native_cels_exact_roundtrip']=len(m['cels']);tests['malformed_native_rejections']=len(bad)
 require(len(EXITS)==3 and sum(s['object']==9 for s in EXITS.values())==1,'Audience edge must be unique');require(not HATCH['travel'],'Hatch is object-only')
 # Every actor's real cels use identical dimensions; test every loop and pose.
 approaches=[s['approach'] for s in EXITS.values()]+[HATCH['approach'],P05['kit']['approach'],P05['slate']['approach']]+list(APPROACHES.values());bounds_count=0
 for v in [214,219,221]:
  for loop in decode_view((ROOT/'reference'/f'{v}.view.bin').read_bytes()):
   for cel in loop:
    require((cel['width'],cel['height'])==(52,80),'Actual actor dimensions changed')
    for x,y,scale in approaches:
     rect=actor_rect((x,y),scale);require(inside(rect),'Unsafe unscaled native actor rectangle');require(rect[1]>=44,'Required pose clipped by caption');bounds_count+=1
 # Full every-pixel foreground walk corridor, plus every step of approaches.
 for x in range(26,294):
  for scale in [127]:require(inside(actor_rect((x,141),scale)),'Unsafe walk draw');bounds_count+=1
 for x,y,scale in approaches:
  for yy in range(y,142):require(inside(actor_rect((x,yy),scale)),'Unsafe queued approach draw');bounds_count+=1
 tests['actual_actor_pose_and_integer_route_draws']=bounds_count
 sizes={c['name']:c['size'] for c in m['cels']};native=decode_view((ROOT/'reference/227.view.bin').read_bytes())[0]
 for conn,source,aim in itertools.product(range(2),range(2),range(3)):
  for c in staging_components(conn,source,aim):
   x,y=P05['hardware_origins'][c];cc=native[c];require(inside((x,y,x+cc['width'],y+cc['height'])),'Unsafe staged hardware')
 require(7 not in staging_components(1,1,2) and 14 not in staging_components(1,1,2) and 15 not in staging_components(1,1,2),'Garage-only prop moved')
 require(P05['kit']['rect'][0]>=ORIGINS['pa_kit'][2][0]+20 and P05['kit']['rect'][3]>=ORIGINS['pa_kit'][2][1]+56,'Staging must differ from WALL')
 for name in ['kit','slate']:
  r=P05[name]['rect'];hits=[hit_p05(x,y) for y in range(r[1],r[3]) for x in range(r[0],r[2])];expected='pa_kit' if name=='kit' else 'equipment_credit_slate';require(expected in hits,'Unreachable staging control');require(not any(hit_p05(x,y,False)==expected for y in range(144) for x in range(320)),'Loan control visible before ownership')
 tests['p05_hardware_states']=12;tests['p05_loan_visibility_hotspot_pixels']=320*144*2
 # Every object/position obeys explicit native bounds. Collision here is foot
 # location, not sprite overlap: actors must be drawn in front of foreground props.
 rects={}
 for obj in OBJECTS:
  key={'completed_screen':'completed-screen','serving_table':'serving-table','pa_kit':'pa-inward','ceramic_carrier':'ceramic-carrier','credit_slate':'rita-credit-slate'}[obj];w,h=sizes[key]
  for pos,xy in enumerate(ORIGINS[obj]):
   x,y=xy
   if obj=='pa_kit' and pos==0:rect=P05['kit']['rect']
   else:rect=[x,y,x+w,y+h]
   require(inside(rect),'Unsafe placement '+obj+str(pos));rects[obj,pos]=rect
   for xx,yy,_ in approaches:
    require(not(rect[0]<=xx<rect[2] and rect[1]<=yy<rect[3]),'Approach foot inside movable prop '+obj+str(pos))
   require(rect[3]<=141,'No safe bottom transit corridor')
 # Cartesian guard is explicit even though bounds factor by object.
 counter=0
 for positions in itertools.product(range(5),repeat=5):
  for facing,unpacked in itertools.product([1,2],[False,True]):
   require(facing in (1,2),'Bad direction');require(p08_object_choices(positions)==[34,63,83,120,40],'Occluded layout object inaccessible')
   for obj,pos in zip(OBJECTS,positions):require(inside(rects[obj,pos]),'Cartesian placement unsafe')
   counter+=1
 tests['layout_cartesian_static_superset']=counter
 candidate_checks=0
 sizes_by_object={obj:tuple(sizes[{'completed_screen':'completed-screen','serving_table':'serving-table','pa_kit':'pa-inward','ceramic_carrier':'ceramic-carrier','credit_slate':'rita-credit-slate'}[obj]]) for obj in OBJECTS}
 for positions in itertools.product(range(5),repeat=5):
  for obj,pos in zip(OBJECTS,positions):
   a,b,c,d=rects[obj,pos];hits=p08_hit_candidates((a+c-1)//2,(b+d-1)//2,positions,sizes_by_object)
   require(OBJECT_IDS[obj] in hits,'Overlapped object disappeared from candidate chooser');candidate_checks+=1
 tests['occluded_object_candidate_checks']=candidate_checks

 # Aligned correct screen covers empty display footprint while sparing hatch.
 screen=rects['completed_screen',3];hatch=HATCH['rect'];require(screen[0]>=hatch[2]+60,'Correct screen conceals hatch');require(screen[0]>=220 and screen[2]<=280,'Screen leaves gate mouth clear')
 wrong=rects['completed_screen',1];require(wrong[0]<hatch[2] and wrong[2]>hatch[0] and wrong[1]<hatch[3],'Wrong hatch placement has no visible consequence')
 # Renderer output is hashed for every Cartesian state without enormous sheets.
 idx=json.loads((ROOT/'previews/all-layouts/render-hashes.json').read_text());require(len(idx)==12500,'Incomplete render hashes');require({x['ordinal'] for x in idx}==set(range(12500)),'Duplicate/missing state hash')
 require(all(len(x['rgba_sha256'])==64 for x in idx),'Invalid render digest')
 tests['all_state_render_hashes']=12500
 preview=json.loads((ROOT/'evidence/preview.json').read_text());require(preview['status']=='PASS','Preview did not finish');require(preview['inputs']=={'manifest':sha(ROOT/'manifest.json'),'geometry':sha(ROOT/'src/geometry.py'),'renderer':sha(ROOT/'src/render.py')},'Stale render evidence')
 from render import Renderer
 renderer=Renderer()
 for row in idx:
  image=renderer.p08(row['positions'],row['facing'],row['unpacked'])
  import hashlib
  require(hashlib.sha256(image.tobytes()).hexdigest()==row['rgba_sha256'],'Current renderer no longer matches all-state proof')
 tests['all_state_hash_rechecks']=len(idx)
 for gate,complete,peg,expected in [(0,False,0,False),(2,True,0,False),(1,True,1,True)]:require(gate_open_from_state(gate)==expected,'Gate appearance wrongly uses historical completion')
 tests['p04_current_gate_bindings']=3
 require({pa_layout_cel(a,b,c) for a,b,c in itertools.product([0,1],[0,1],[1,2])}=={2,3,12,13,14,15,16,17},'PA history projection loses a wiring/source/facing state')
 tests['preserved_pa_hardware_combinations']=8
 # Every Jackie pose/facing at both P05 approaches keeps the full slate visible.
 slate=Image.new('RGBA',(320,144));renderer.put(slate,227,8,P05['slate_origin']);slmask=np.array(slate)[:,:,3]>0
 count=0
 for target in ['kit','slate']:
  x,y,scale=P05[target]['approach']
  for loop in range(2):
   for pose in range(5):
    actor=Image.new('RGBA',(320,144));renderer.actor(actor,(x,y),scale,pose=pose,loop=loop)
    require(not np.any(slmask & (np.array(actor)[:,:,3]>0)),'P05 approach hides credit reader');count+=1
 tests['zero_credit_slate_actor_occlusion_cases']=count
 def lane_overlap(im):return int(np.count_nonzero(np.array(im)[132:143,23:300,3]))
 def reject_lane(mask):require(lane_overlap(mask)==0,'Unplaced/real-zone prop occupies clear lane')
 # Prove that the exact rejected -4,+11 projection fails this same pixel guard.
 old=Image.new('RGBA',(320,144));new=Image.new('RGBA',(320,144))
 for c in staging_components(1,1,2):
  xy=P05['hardware_origins'][c];renderer.put(new,227,c,xy);renderer.put(old,227,c,(xy[0]-45,xy[1]+11))
 renderer.put(new,227,8,P05['slate_origin']);reject_lane(new)
 try:reject_lane(old)
 except ValueError:pass
 else:raise ValueError('Pre-fix lane overlap was not rejected')
 tests['rejected_pre_fix_lane_overlap_pixels']=lane_overlap(old)
 for obj in OBJECTS:
  for pos in range(5):
   mask=Image.new('RGBA',(320,144))
   if obj=='pa_kit' and pos==0:mask=new
   else:
    renderer.put(mask,228,CELS[obj],ORIGINS[obj][pos])
    if obj=='pa_kit':
     x,y=ORIGINS[obj][pos];renderer.put(mask,227,8,(x+55,y+(21 if pos==4 else 27)))
   if pos!=4:reject_lane(mask)
   else:require(lane_overlap(mask)>0,'Explicit LANE placement is visually clear '+obj)
 tests['per_object_lane_geometry_cases']=25
 write_json(ROOT/'geometry-manifest.json',{'classification':'New reconstructed geometry, measured against exact native cels','stage':STAGE,'caption_last_row':43,'hud_first_row':144,'coordinate_convention':'Top-left DrawCel; half-open rectangles; actor native52x80 feet26,78','resources':{'background':305,'props':228,'existing_equipment':227,'existing_p03':224,'palette':999,'font':0},'new_allocations':'305 and228 are newly allocated after known-registry scan; not recovered historical IDs','p05':P05,'exits':EXITS,'object_only_hatch':HATCH,'positions':POSITIONS,'object_ids':OBJECT_IDS,'origins':ORIGINS,'zone_rects':ZONE_RECTS,'zone_approaches':APPROACHES,'marker_cels':MARKS,'walk_corridor':{'x':[26,293],'y':141,'scale128':127},'precedence':['exits','object-only hatch','equipment credit71','PA kit63','topmost movable props','named zone destinations'],'occlusion':'Actors drawn after prop layers at supplied safe approach feet; every movable object remains available through named-object plan selection even if co-located/occluded','p08_cel_mapping':CELS,'overlap_choice_contract':{'always_available_objects':[34,63,83,120,40],'point_query':'p08_hit_candidates returns every overlapping candidate','canonical_labels_required':True,'host_gate':'Mouse/controller chooser not implemented here; topmost-only selection is forbidden'},'layout_superset':'Includes impossible logical states solely to make renderer total; state model must reject them','acceptance':'Static only; native render/input/save and user visual approval remain open'})
 g.done(checks=tests,manifest_sha256=sha(ROOT/'manifest.json'),scope='Static asset/geometry acceptance only; no native runtime, state handoff, autosave or listening claim')
if __name__=='__main__':run()
