#!/usr/bin/env python3
"""Deterministic opening exporter. All anatomy/anchors require reviewed config.

No production source is modified. Inputs are eight RGBA 4x2 master sheets.
Output cels use one affine scale per character and exact original font0 bits.
This tool proves structural/pixel closure, never animation/native acceptance.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import sys

import numpy as np
import PIL
from PIL import Image, ImageDraw

from extract_references import read_font, read_palette, PINNED_PALETTE
from inspect_view import decode_view
from view_writer import Cel, encode_view

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REF = HERE.parent / 'references'
CAST = [
    ('jackie','Jackie Tree',245,214,300),
    ('bunny','Bunny Easter',246,219,101),
    ('frankie','Frankie Maplewood',247,218,101),
    ('stringer','Mr. Stringer',248,222,302),
    ('milo','Milo Pennant',249,221,304),
    ('vivian','Vivian Voss',250,236,100),
    ('rita','Rita Stringer',251,223,302),
    ('felix','Felix Bunt',252,225,303),
]
CAST_BY_SLUG = {row[0]:row for row in CAST}
ACCENTS = {'jackie':(81,127,118),'bunny':(204,101,83),'frankie':(178,138,43),'stringer':(145,78,45),'milo':(207,120,43),'vivian':(95,54,94),'rita':(44,139,136),'felix':(169,121,48)}
STARTS = [0,24,48,60,72,84,96,108]

def sha(data): return hashlib.sha256(data).hexdigest()
def file_sha(path): return sha(Path(path).read_bytes())
def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def required(condition,message):
    if not condition: raise ValueError(message)
def round_pixel(value): return math.floor(value+0.5)

class Art:
    def __init__(self,reference_dir=REF):
        self.reference_dir=Path(reference_dir)
        pdata=(self.reference_dir/'999.palette.bin').read_bytes()
        required(sha(pdata)==PINNED_PALETTE,'Palette999 hash changed')
        self.colors=read_palette(pdata)
        self.flat=sum(self.colors,[])
        fdata=(self.reference_dir/'000.font.bin').read_bytes()
        self.font=read_font(fdata)
        ledger=json.loads((self.reference_dir/'SOURCE-REFERENCE-LEDGER.json').read_text())
        required(sha(fdata)==ledger['font0_sha256'],'Original font0 hash changed')
        self.ledger=ledger
        self.palette_hash=sha(pdata); self.font_hash=sha(fdata)
        self.cream=self.near((233,210,163)); self.ink=self.near((33,49,58))

    def near(self,rgb):
        return min(range(218),key=lambda i:sum((rgb[k]-self.colors[i][k])**2 for k in range(3)))

    def blank(self,size,color=255):
        im=Image.new('P',size,color); im.putpalette(self.flat); im.info['transparency']=255
        return im

    def index(self,im):
        rgba=np.asarray(im.convert('RGBA'),dtype=np.uint8)
        flat=rgba.reshape(-1,4); result=np.full(flat.shape[0],255,dtype=np.uint8)
        opaque=flat[:,3]>=128
        rgb,inverse=np.unique(flat[opaque,:3],axis=0,return_inverse=True)
        palette=np.array(self.colors[:218],dtype=np.int32)
        indices=np.zeros(len(rgb),dtype=np.uint8)
        for start in range(0,len(rgb),4096):
            d=rgb[start:start+4096,None,:].astype(np.int32)-palette[None,:,:]
            indices[start:start+4096]=np.argmin(np.sum(d*d,axis=2),axis=1).astype(np.uint8)
        result[opaque]=indices[inverse]
        out=self.blank(im.size); out.putdata(result.tolist()); return out

    def lettering(self,text,scale=1,color=None):
        color=self.ink if color is None else color
        glyphs=[]
        for ch in text:
            required(str(ord(ch)) in self.font['glyphs'],f'Unsupported original font0 character {ch!r}')
            glyphs.append(self.font['glyphs'][str(ord(ch))])
        width=sum(g['width'] for g in glyphs)*scale
        out=self.blank((width,self.font['height']*scale)); d=ImageDraw.Draw(out); x0=0
        for glyph in glyphs:
            w,h=glyph['width'],glyph['height']; stride=(w+7)//8; rows=bytes.fromhex(glyph['rows_hex'])
            for y in range(h):
                for x in range(w):
                    if rows[y*stride+x//8] & (0x80>>(x%8)):
                        d.rectangle((x0+x*scale,y*scale,x0+(x+1)*scale-1,(y+1)*scale-1),fill=color)
            x0+=w*scale
        return out

    def motif(self,slug,final):
        if slug=='jackie':
            box=final.convert('RGBA').getbbox(); required(box is not None,'Empty final Jackie')
            mask=final.crop(box).convert('RGBA').getchannel('A')
            out=self.blank(mask.size); out.paste(self.near(ACCENTS[slug]),(0,0),mask)
            return out,box[:2]
        im=self.blank((128,104)); d=ImageDraw.Draw(im); col=self.near(ACCENTS[slug])
        if slug=='bunny':
            pts=[(64+round_pixel((47 if i%2==0 else 32)*math.cos(i*math.pi/12)),52+round_pixel((47 if i%2==0 else 32)*math.sin(i*math.pi/12))) for i in range(24)]
            d.polygon(pts,fill=col)
        elif slug=='frankie':
            for x in range(8,125,16):d.line((x,10,x,96),fill=col,width=2)
            for y in range(10,98,14):d.line((8,y,120,y),fill=col,width=2)
        elif slug=='stringer':
            d.line((10,8,10,97),fill=col,width=2);d.line((10,96,120,96),fill=col,width=2)
            for y in range(8,97,8):d.line((10,y,20 if y%16==8 else 27,y),fill=col,width=2)
            for x in range(18,121,8):d.line((x,96,x,87 if x%16==2 else 81),fill=col,width=2)
            d.line((28,16,114,16),fill=col,width=2)
        elif slug=='milo':
            for i in range(11):
                theta=math.pi+i*math.pi/10
                d.line((64,92,64+round_pixel(55*math.cos(theta)),87+round_pixel(76*math.sin(theta))),fill=col,width=3)
        elif slug=='vivian':
            d.rectangle((8,12,60,94),fill=col);d.rectangle((66,12,120,94),fill=self.near((159,116,149)))
        elif slug=='rita':
            for box in [(7,6,59,58),(53,24,122,93),(14,59,48,93)]:d.ellipse(box,outline=col,width=5)
        elif slug=='felix':
            d.polygon([(12,92),(12,12),(118,92)],outline=col,width=3)
            d.line((26,28,26,77,99,77),fill=col,width=2)
            for x,y in [(98,22),(108,32),(105,10)]:d.line((x-5,y,x+5,y),fill=col);d.line((x,y-5,x,y+5),fill=col)
        box=im.convert('RGBA').getbbox(); required(box is not None,'Empty motif')
        return im.crop(box),box[:2]

    def name(self,slug,text):
        if slug=='jackie': return self.lettering(text,2)
        parts=text.split(' ',1); words=[self.lettering(part,2) for part in parts]
        out=self.blank((max(w.width for w in words)+12,40),self.cream)
        for line,word in enumerate(words):out.paste(word,((out.width-word.width)//2,3+line*18),word.convert('RGBA').getchannel('A'))
        return out

    def title(self):
        title=self.blank((288,72)); shade=self.near((81,127,118))
        for text,y in [('Come and Knock',4),('on Our Door',40)]:
            shadow=self.lettering(text,3,shade);words=self.lettering(text,3);x=(288-words.width)//2
            title.paste(shadow,(x+2,y+2),shadow.convert('RGBA').getchannel('A'))
            title.paste(words,(x,y),words.convert('RGBA').getchannel('A'))
        return title

def source_cells(master,spec):
    if 'source_rects' in spec:
        rects=spec['source_rects']; required(len(rects)==8,'Exactly eight source_rects required')
    else:
        w,h=master.size; required(w%4==0 and h%2==0,'4x2 master dimensions must divide exactly; supply explicit source_rects otherwise')
        rects=[[(i%4)*w//4,(i//4)*h//2,(i%4+1)*w//4,(i//4+1)*h//2] for i in range(8)]
    for i,rect in enumerate(rects):
        required(len(rect)==4 and all(isinstance(v,int) for v in rect),f'Cel{i}: integer source rectangle required')
        l,t,r,b=rect; required(0<=l<r<=master.width and 0<=t<b<=master.height,f'Cel{i}: invalid source rectangle')
    return rects

def registered_poses(master,spec,art):
    required(spec.get('registration_reviewed') is True,'Review measured anatomical height and all shoe anchors; set registration_reviewed=true')
    required('upright_height_source' in spec and spec['upright_height_source']>0,'Provide measured upright person height, excluding props')
    required(spec.get('target_upright_height',78)==78,'Actor scale tradeoff needs explicit revised contract; target must remain78px')
    scale=78/spec['upright_height_source']
    anchors=spec.get('source_anchors'); required(isinstance(anchors,list) and len(anchors)==8,'Eight explicit per-cel shoe anchors are required')
    screen=spec.get('screen_anchor',[122 if spec['slug']=='jackie' else 118,134])
    required(len(screen)==2 and screen[1]==134,'Fixed screen feet anchor must be y134')
    frames=[]; records=[]
    rects=source_cells(master,spec)
    for i,(rect,anchor) in enumerate(zip(rects,anchors)):
        cell=master.crop(rect).convert('RGBA'); a=cell.getchannel('A').point(lambda v:255 if v>=128 else 0); box=a.getbbox()
        required(box is not None,f'Cel{i}: empty source cell')
        required(box[0]>0 and box[1]>0 and box[2]<cell.width and box[3]<cell.height,f'Cel{i}: opaque pixels touch source cell border {box}')
        required(len(anchor)==2 and 0<=anchor[0]<cell.width and 0<=anchor[1]<cell.height,f'Cel{i}: invalid shoe anchor {anchor}')
        # Transform the entire cell with a common inverse affine scale. Pixel
        # centers align anchor source pixels to screen pixels; no per-cel resize.
        inv=1/scale; tx=anchor[0]+0.5-(screen[0]+0.5)*inv; ty=anchor[1]+0.5-(screen[1]+0.5)*inv
        # Expanded render catches offscreen art instead of silently clipping it.
        margin=320
        extended=cell.transform((960,784),Image.Transform.AFFINE,(inv,0,tx-margin*inv,0,inv,ty-margin*inv),Image.Resampling.NEAREST,fillcolor=(0,0,0,0))
        ebox=extended.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox(); required(ebox is not None,f'Cel{i}: vanished during scaling')
        bounds=[ebox[0]-margin,ebox[1]-margin,ebox[2]-margin,ebox[3]-margin]
        required(0<=bounds[0]<bounds[2]<=320 and 0<=bounds[1]<bounds[3]<=144,f'Cel{i}: art outside320x144: {bounds}; do not shrink automatically')
        frame=art.index(extended.crop((margin,margin,margin+320,margin+144)))
        frames.append(frame)
        records.append({'cel':i,'source_rect':rect,'source_alpha_bbox':list(box),'source_shoe_anchor_cell':anchor,'source_shoe_anchor_sheet':[anchor[0]+rect[0],anchor[1]+rect[1]],'uniform_scale':scale,'screen_opaque_bbox':bounds,'native_pixels_sha256':sha(frame.tobytes())})
    required(len({f.tobytes() for f in frames})==8,'Duplicate native cels: eight distinct performed poses required')
    union=[min(r['screen_opaque_bbox'][0] for r in records),min(r['screen_opaque_bbox'][1] for r in records),max(r['screen_opaque_bbox'][2] for r in records),max(r['screen_opaque_bbox'][3] for r in records)]
    return [f.crop(union) for f in frames],union,screen,records

def budget(loops):
    pixels=[sum(im.width*im.height for im in loop) for loop in loops]
    tables=18+16*len(loops)+36*sum(len(loop) for loop in loops)
    return {'loop_pixel_bytes':pixels,'header_table_bytes':tables,'total_bytes':tables+sum(pixels),'limit':65535,'headroom':65535-tables-sum(pixels)}

def geometry_entry(loop,images,draw,purpose):
    return {'loop':loop,'cels':len(images),'size':list(images[0].size),'draw':list(draw),'purpose':purpose}

def generation_lineage(spec,config_dir,master_path):
    if 'generation_provenance_file' not in spec:return None
    path=(config_dir/spec['generation_provenance_file']).resolve();ledger=json.loads(path.read_text())
    entries={(path.parent/g['master']).resolve():g for g in ledger['generations']}
    targets=[master_path]
    if spec.get('stable_prop',{}).get('replacement_master'):
        targets.append((config_dir/spec['stable_prop']['replacement_master']).resolve())
    chains=[]
    for target in targets:
        chain=[];seen=set()
        while target is not None:
            required(target not in seen,'Generation lineage cycle');seen.add(target)
            required(target in entries,f'Generated master not recorded in authoritative ledger: {target}')
            row=entries[target];required(file_sha(target)==row['sha256'],f'Generation master hash differs: {target}')
            prompt=(path.parent/row['exact_prompt']).resolve();required(file_sha(prompt)==row['prompt_sha256'],f'Generation prompt hash differs: {prompt}')
            chain.append(row)
            target=(path.parent/row['edit_target']).resolve() if row.get('edit_target') else None
        chains.append(chain)
    return {'path':str(path),'sha256':file_sha(path),'source_reference':ledger['source_references'][spec['slug']],'generation_chains_newest_first':chains}

def separate_stable_prop(cels,union,spec,config_dir,art):
    """Apply reviewed pixel-selection masks only; never repaint hidden pixels."""
    layer=spec.get('stable_prop')
    if not layer:return cels,union,None,None
    required(layer.get('separation_reviewed') is True,'Stable prop separation must be explicitly reviewed')
    required(layer.get('source_cel')==0,'Stable props must derive once from accepted cel0')
    paths=layer.get('actor_keep_masks',[]);required(len(paths)==8,'Eight reviewed actor masks required')
    originals=[];actors=[];mask_records=[]
    for ci,(im,path) in enumerate(zip(cels,paths)):
        original=art.blank((320,144));original.paste(im,tuple(union[:2]));originals.append(original)
        path=(config_dir/path).resolve();mask=Image.open(path).convert('L')
        required(mask.size==(320,144),f'Stable actor mask{ci} must be320x144')
        required(set(mask.tobytes())<={0,255},f'Stable actor mask{ci} must be binary')
        actor=art.blank((320,144));actor.paste(original,(0,0),mask);actors.append(actor)
        mask_records.append({'cel':ci,'path':str(path),'sha256':file_sha(path)})
    prop_path=(config_dir/layer['source_prop_mask']).resolve();mask=Image.open(prop_path).convert('L')
    required(mask.size==(320,144) and set(mask.tobytes())<={0,255},'Source prop mask must be binary320x144')
    prop=art.blank((320,144));prop.paste(originals[0],(0,0),mask)
    a=np.asarray(actors[0]);p=np.asarray(prop);o=np.asarray(originals[0])
    required(not np.any((a!=255)&(p!=255)),'Actor0/prop masks overlap opaque source pixels')
    recomposed=np.where(a!=255,a,p)
    required(np.array_equal(recomposed,o),'Actor0/prop masks must partition every original cel0 pixel exactly')
    boxes=[im.convert('RGBA').getbbox() for im in actors];required(all(boxes),'Actor mask removes entire pose')
    bounds=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
    pbox=prop.convert('RGBA').getbbox();required(pbox is not None,'Empty stable prop')
    data={'status':'ONCE_DERIVED_VISIBLE_CEL0_PIXELS_NO_HIDDEN_PIXEL_SYNTHESIS','source_cel':0,'source_prop_mask':str(prop_path),'source_prop_mask_sha256':file_sha(prop_path),'actor_keep_masks':mask_records,'source_cel0_exact_recomposition':True,'draw':list(pbox[:2]),'size':[pbox[2]-pbox[0],pbox[3]-pbox[1]],'purpose':layer.get('purpose','Stable registered prop'),'native_palette_pixels_sha256':sha(prop.crop(pbox).tobytes())}
    if 'replacement_master' in layer:
        required(layer.get('replacement_new_reconstruction') is True,'A newly generated prop must be labeled new reconstruction')
        master_path=(config_dir/layer['replacement_master']).resolve();prompt_path=(config_dir/layer['replacement_prompt']).resolve()
        generated=Image.open(master_path).convert('RGBA');scale=layer['replacement_uniform_scale'];sa=layer['replacement_source_anchor'];da=layer['replacement_screen_anchor'];inv=1/scale
        required(scale>0 and prompt_path.is_file(),'Replacement prop scale/prompt is invalid')
        tx=sa[0]+.5-(da[0]+.5)*inv;ty=sa[1]+.5-(da[1]+.5)*inv
        extended=generated.transform((960,784),Image.Transform.AFFINE,(inv,0,tx-320*inv,0,inv,ty-320*inv),Image.Resampling.NEAREST,fillcolor=(0,0,0,0))
        box=extended.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox();required(box is not None,'Empty reconstructed prop')
        prop_bounds=[box[0]-320,box[1]-320,box[2]-320,box[3]-320]
        required(0<=prop_bounds[0]<prop_bounds[2]<=320 and 0<=prop_bounds[1]<prop_bounds[3]<=144,'Reconstructed prop leaves artwork band')
        prop=art.index(extended.crop((320,320,640,464)));pbox=prop.convert('RGBA').getbbox()
        data.update(status='NEW_GENERATED_MATCHED_PROP_RECONSTRUCTION_INCLUDING_PREVIOUSLY_OCCLUDED_PIXELS',source_cel=None,visible_original_prop_pixels_sha256=data['native_palette_pixels_sha256'],replacement_master=str(master_path),replacement_master_sha256=file_sha(master_path),replacement_prompt=str(prompt_path),replacement_prompt_sha256=file_sha(prompt_path),replacement_uniform_scale=scale,replacement_source_anchor=sa,replacement_screen_anchor=da,draw=list(pbox[:2]),size=[pbox[2]-pbox[0],pbox[3]-pbox[1]],native_palette_pixels_sha256=sha(prop.crop(pbox).tobytes()),source_cel0_exact_recomposition_meaning='Original actor/visible-prop masks partition sourcecel0 exactly; the new generated replacement intentionally changes the static prop pixels.')
    return [im.crop(bounds) for im in actors],bounds,prop.crop(pbox),data

def export_one(spec,config_dir,output,art,config_path):
    slug=spec['slug']; _,name,view,identity,background=CAST_BY_SLUG[slug]
    master_path=(config_dir/spec['master']).resolve(); prompt_path=(config_dir/spec['prompt']).resolve()
    required(master_path.is_file() and prompt_path.is_file(),'Master and exact saved prompt must exist')
    required(bool(spec.get('master_version')),'master_version is required')
    lineage=generation_lineage(spec,config_dir,master_path)
    with Image.open(master_path) as opened:
        required('A' in opened.getbands() or 'transparency' in opened.info,'Master has no transparency channel')
        master=opened.convert('RGBA')
    cels,union,screen,records=registered_poses(master,spec,art)
    cels,union,stable_prop,stable_record=separate_stable_prop(cels,union,spec,config_dir,art)
    required(len({im.tobytes() for im in cels})==8,'Separation produced duplicate actor poses')
    motif,offset=art.motif(slug,cels[7]); name_image=art.name(slug,name)
    draw0=union[:2]
    draw1=([draw0[0]+offset[0]+4,draw0[1]+offset[1]] if slug=='jackie' else [178+offset[0],20+offset[1]])
    draw2=([178,63] if slug=='jackie' else [242-name_image.width//2,62])
    loops=[cels,[motif],[name_image]]
    geometry={'schema':'CAKOOD_OPENING_GEOMETRY_R2','character':name,'slug':slug,'view':view,'background_view':background,'source_identity_view':identity,'canvas':[320,200],'scene':[320,144],'uniform_scale':78/spec['upright_height_source'],'nominal_upright_height':78,'screen_feet':screen,'common_transparent_crop_screen':union,'loop0':geometry_entry(0,cels,draw0,'Eight distinct performed action poses; cel7 freezes'),'loop1':geometry_entry(1,[motif],draw1,'Teal offset final silhouette' if slug=='jackie' else 'Canonical geometric freeze motif'),'loop2':geometry_entry(2,[name_image],draw2,'Exact name in unmodified original font0 glyph shapes'),'freeze_panel':[166,0,320,144],'freeze_panel_palette_index':art.cream,'freeze_start':120,'card_end_exclusive':360,'action_cel_starts':([0,18,36,54,72,84,96,108] if slug=='jackie' else STARTS),'controls_band':[0,144,320,200],'stable_prop_loops':[]}
    if slug=='vivian':
        title=art.title();loops.append([title]); geometry['shared_title']=geometry_entry(3,[title],[16,30],'Come and Knock on Our Door; cards0and9 only')
        geometry['shared_title']['scene_background_palette_index']=10
        geometry['shared_title']['accent_rectangles']=[{'rect':[18,10,302,12],'palette_index':4},{'rect':[40,116,280,119],'palette_index':4},{'rect':[80,125,240,127],'palette_index':37}]
    if stable_prop is not None:
        index=len(loops);loops.append([stable_prop]);entry=geometry_entry(index,[stable_prop],stable_record['draw'],stable_record['purpose']);entry['derive_from_cel']=stable_record['source_cel'];entry['draw_before_loop0']=True;entry['pixel_provenance']=stable_record['status'];geometry['stable_prop_loops'].append(entry)
    for key in ['loop0','loop1','loop2']+(['shared_title'] if slug=='vivian' else []):
        g=geometry[key];x,y=g['draw'];w,h=g['size']
        required(0<=x and x+w<=320 and 0<=y and y+h<=144,f'{slug}:{key} draw leaves artwork band')
    size=budget(loops)
    required(size['headroom']>=0,f'{slug}: VIEW{view} would be {size["total_bytes"]} bytes, exceeds65535 by{-size["headroom"]}. Keep78px/8poses; review transparent margins or stable-prop separation and update renderer before retry.')
    payload=encode_view([[Cel(im.width,im.height,im.tobytes()) for im in loop] for loop in loops])
    decoded=decode_view(payload)
    required(len(payload)==size['total_bytes'],'Writer budget mismatch')
    for li,loop in enumerate(loops):
        for ci,im in enumerate(loop):
            required(decoded[li][ci]['pixels']==im.tobytes(),'Independent decode mismatch')
            required(decoded[li][ci]['clear_key']==255,'Unexpected transparency')
            required(set(im.tobytes())<=set(range(218))|{255},'Reserved palette index used')
    directory=output/'cels'/slug;directory.mkdir(parents=True,exist_ok=True)
    cel_ledger=[]
    for li,loop in enumerate(loops):
        for ci,im in enumerate(loop):
            stem=f'loop{li:02}-cel{ci:02}'; indexed=directory/f'{stem}-indexed.png';rgba=directory/f'{stem}-rgba.png'
            im.save(indexed,transparency=255);im.convert('RGBA').save(rgba)
            cel_ledger.append({'loop':li,'cel':ci,'size':list(im.size),'pixel_sha256':sha(im.tobytes()),'indexed_path':str(indexed.relative_to(output)),'indexed_sha256':file_sha(indexed),'rgba_path':str(rgba.relative_to(output)),'rgba_sha256':file_sha(rgba)})
    resource=output/'resources'/f'{view:03}.view.bin';resource.parent.mkdir(parents=True,exist_ok=True);resource.write_bytes(payload)
    proof=output/'proof'/slug;dump(proof/'geometry-contract.json',geometry)
    refs=[r for r in art.ledger['references'] if r['view'] in (identity,background)]
    report={'status':'STRUCTURAL_PIXEL_CLOSURE_PASS_VISUAL_AND_NATIVE_ACCEPTANCE_PENDING','character':name,'slug':slug,'view':view,'resource_path':str(resource.relative_to(output)),'resource_bytes':len(payload),'resource_sha256':sha(payload),'budget':size,'loops':[len(x) for x in loops],'independent_decode_byte_equal':True,'all_action_cels_distinct':True,'performed_choreography_reviewed':False,'native_animation_verified':False,'source_master':str(master_path),'master_sha256':file_sha(master_path),'master_size':list(master.size),'master_version':spec['master_version'],'prompt_path':str(prompt_path),'prompt_sha256':file_sha(prompt_path),'config_path':str(config_path),'config_sha256':file_sha(config_path),'accepted_registration':spec,'source_crops':records,'palette999_sha256':art.palette_hash,'font0_sha256':art.font_hash,'inherited_references':refs,'stable_prop_derivation':stable_record,'new_pixels':'All action cel pixels derive from new generated master; motifs are code-native geometry except Jackie silhouette derives from final action alpha; lettering uses exact original font0 glyph bits. Stable props, when present, retain only visible sourcecel0 pixels without hidden-pixel synthesis. No claim of recovered lost245–252 bytes.','tool_hashes':{p.name:file_sha(p) for p in [HERE/'export_opening.py',HERE/'view_writer.py',HERE/'inspect_view.py',HERE/'extract_references.py']},'versions':{'python':platform.python_version(),'pillow':PIL.__version__,'numpy':np.__version__},'cel_files':cel_ledger}
    report['generation_lineage']=lineage
    report['new_pixels']='All action pixels derive from the recorded new generated master. Motifs use code-native geometry except Jackie final-alpha silhouette. Lettering uses exact original font0 bits. Stringer chairs derive once from visible cel0; Rita replacement bench is explicitly new generated reconstruction including previously occluded regions. No claim of recovered lost245–252 bytes.'
    dump(proof/'export-checks.json',report)
    render_previews(output,proof,art,geometry,loops)
    return report,geometry

def render_previews(output,proof,art,g,loops):
    record=next(r for r in art.ledger['references'] if r['view']==g['background_view'])
    bg=Image.open(art.reference_dir/record['outputs'][0]['file']).convert('RGBA')
    required(bg.size==(320,144),'Background must be exact320x144')
    def frame(ci,freeze=False):
        out=bg.copy()
        if freeze:
            ImageDraw.Draw(out).rectangle((166,0,319,143),fill=tuple(art.colors[art.cream])+(255,))
            out.alpha_composite(loops[1][0].convert('RGBA'),tuple(g['loop1']['draw']))
            out.alpha_composite(loops[2][0].convert('RGBA'),tuple(g['loop2']['draw']))
        for prop in g['stable_prop_loops']:
            out.alpha_composite(loops[prop['loop']][0].convert('RGBA'),tuple(prop['draw']))
        out.alpha_composite(loops[0][ci].convert('RGBA'),tuple(g['loop0']['draw']))
        return out
    contact=Image.new('RGBA',(320*4,144*2),(0,0,0,255))
    for ci in range(8):
        f=frame(ci);f.save(proof/f'action-{ci:02}-native.png'); contact.alpha_composite(f,((ci%4)*320,(ci//4)*144))
    contact.save(proof/'all-eight-native-contact.png')
    freeze=frame(7,True);freeze.save(proof/'freeze-native.png');freeze.resize((1280,576),Image.Resampling.NEAREST).save(proof/'freeze-4x.png')
    if 'shared_title' in g:
        title=Image.new('RGBA',(320,144),tuple(art.colors[g['shared_title']['scene_background_palette_index']])+(255,))
        for item in g['shared_title']['accent_rectangles']:
            x0,y0,x1,y1=item['rect'];ImageDraw.Draw(title).rectangle((x0,y0,x1-1,y1-1),fill=tuple(art.colors[item['palette_index']])+(255,))
        title.alpha_composite(loops[3][0].convert('RGBA'),(16,30));title.save(proof/'shared-title-native.png')

def inspect_master(path):
    im=Image.open(path).convert('RGBA');rects=source_cells(im,{})
    rows=[]
    for i,rect in enumerate(rects):
        cell=im.crop(rect);a=cell.getchannel('A').point(lambda v:255 if v>=128 else 0);box=a.getbbox()
        rows.append({'cel':i,'cell_rect':rect,'alpha_bbox':box,'unreviewed_foot_guess':None if box is None else [(box[0]+box[2]-1)/2,box[3]-1],'opaque_extent_height':None if box is None else box[3]-box[1]})
    return {'master':str(path),'sha256':file_sha(path),'size':list(im.size),'warning':'Bounds include props. Measure upright human anatomy and actual shoe anchors; these are only inspection aids, never accepted registration.','cells':rows}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('inspect');p.add_argument('masters',nargs='+',type=Path)
    p=sub.add_parser('export');p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--characters',nargs='*');p.add_argument('--references',type=Path,default=REF)
    args=parser.parse_args(argv)
    if args.command=='inspect':
        for path in args.masters:print(json.dumps(inspect_master(path),indent=2))
        return 0
    config_path=args.config.resolve();config=json.loads(config_path.read_text());specs=config['characters'];required(len({s['slug'] for s in specs})==len(specs),'Duplicate character specs')
    for s in specs:required(s['slug'] in CAST_BY_SLUG,f'Unallocated character {s["slug"]}')
    if args.characters:specs=[s for s in specs if s['slug'] in args.characters];required(len(specs)==len(set(args.characters)),'Requested character missing from config')
    else:required({s['slug'] for s in specs}==set(CAST_BY_SLUG),'Full export must specify all eight characters')
    art=Art(args.references);reports=[];geometry=[];output=args.output.resolve()
    for spec in specs:
        report,g=export_one(spec,config_path.parent,output,art,config_path);reports.append(report);geometry.append(g)
        print(json.dumps({'slug':spec['slug'],'view':report['view'],'bytes':report['resource_bytes'],'headroom':report['budget']['headroom'],'actor_size':g['loop0']['size'],'draw':g['loop0']['draw']}),flush=True)
    complete=len(reports)==8
    manifest={'schema':'CAKOOD_OPENING_ASSET_RECONSTRUCTION_R2','status':'STRUCTURAL_PIXEL_CLOSURE_PASS_VISUAL_AND_NATIVE_ACCEPTANCE_PENDING','complete_eight_character_export':complete,'total_action_cels':sum(r['loops'][0] for r in reports),'palette999_sha256':art.palette_hash,'font0_sha256':art.font_hash,'native_verified':False,'resources':[{k:r[k] for k in ('slug','character','view','resource_path','resource_bytes','resource_sha256','loops')} for r in reports],'geometry':geometry}
    dump(output/('OPENING-ASSET-MANIFEST.json' if complete else 'PARTIAL-OPENING-ASSET-MANIFEST.json'),manifest)
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,OSError) as error:print(f'BLOCKED: {error}',file=sys.stderr);sys.exit(2)
