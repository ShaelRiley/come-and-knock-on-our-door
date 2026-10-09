#!/usr/bin/env python3
"""Source alpha/crop and decoded registration checks for an isolated export."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image
from export_opening import Art, source_cells, dump, file_sha
from inspect_view import decode_view

def components(mask):
    unseen=set(zip(*np.where(mask)))
    sizes=[]
    while unseen:
        first=unseen.pop();stack=[first];size=0
        while stack:
            y,x=stack.pop();size+=1
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    p=(y+dy,x+dx)
                    if p in unseen:unseen.remove(p);stack.append(p)
        sizes.append(size)
    return sorted(sizes,reverse=True)

def verify(config_path,output):
    art=Art();config=json.loads(config_path.read_text());results=[]
    for spec in config['characters']:
        slug=spec['slug'];proof=output/'proof'/slug
        if not (proof/'export-checks.json').exists():continue
        report=json.loads((proof/'export-checks.json').read_text());g=json.loads((proof/'geometry-contract.json').read_text())
        master=Image.open(config_path.parent/spec['master']).convert('RGBA');rgba=np.asarray(master);a=rgba[:,:,3]
        cells=[];draw=g['loop0']['draw'];resource=output/report['resource_path'];decoded=decode_view(resource.read_bytes())
        assert file_sha(resource)==report['resource_sha256']
        qa=Image.new('RGBA',(8*96,4*104),(0,0,0,255))
        bg_record=next(r for r in art.ledger['references'] if r['view']==g['background_view'])
        bg=Image.open(art.reference_dir/bg_record['outputs'][0]['file']).convert('RGBA')
        static_base=bg.copy();static_mask=Image.new('L',(320,144))
        for prop in g.get('stable_prop_loops',[]):
            pi=Image.open(output/'cels'/slug/f'loop{prop["loop"]:02}-cel00-indexed.png')
            assert pi.tobytes()==decoded[prop['loop']][0]['pixels']
            static_base.alpha_composite(pi.convert('RGBA'),tuple(prop['draw']))
            static_mask.paste(pi.convert('RGBA').getchannel('A'),tuple(prop['draw']))
        for i,rect in enumerate(source_cells(master,spec)):
            l,t,r,b=rect;cell=a[t:b,l:r];binary=cell>=128
            edge=int(binary[0,:].sum()+binary[-1,:].sum()+binary[:,0].sum()+binary[:,-1].sum())
            assert edge==0
            im=Image.open(output/'cels'/slug/f'loop00-cel{i:02}-indexed.png');native=np.asarray(im);native_alpha=np.asarray(im.convert('RGBA'))[:,:,3]
            assert set(np.unique(native_alpha))<=set([0,255]);assert bytes(im.tobytes())==decoded[0][i]['pixels']
            component_sizes=components(native!=255)
            yy,xx=np.where(native!=255)
            bounds=[int(xx.min())+draw[0],int(yy.min())+draw[1],int(xx.max()+1)+draw[0],int(yy.max()+1)+draw[1]]
            assert bounds[3]<=135 and bounds[1]>=0
            frame=Image.open(proof/f'action-{i:02}-native.png').convert('RGBA')
            expected=static_base.copy();expected.alpha_composite(im.convert('RGBA'),tuple(draw));assert frame.tobytes()==expected.tobytes()
            mask=static_mask.copy();actor_mask=Image.new('L',(320,144));actor_mask.paste(im.convert('RGBA').getchannel('A'),tuple(draw));transparent=(np.asarray(mask)==0)&(np.asarray(actor_mask)==0)
            assert np.array_equal(np.asarray(frame)[transparent],np.asarray(bg)[transparent])
            for row,color in enumerate([(236,218,183),(30,67,98),(38,75,48),(15,16,22)]):
                tile=Image.new('RGBA',(96,104),color+(255,));tile.alpha_composite(im.convert('RGBA'),((96-im.width)//2,94-im.height));qa.alpha_composite(tile,(i*96,row*104))
            cells.append({'cel':i,'source_alpha_min':int(cell.min()),'source_alpha_max':int(cell.max()),'source_pixels_alpha_below128':int((cell<128).sum()),'source_pixels_alpha_atleast128':int(binary.sum()),'source_border_opaque_pixel_count':edge,'source_alpha_bbox':list(master.crop(rect).getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox()),'native_screen_opaque_bbox':bounds,'native_alpha_values':[int(v) for v in np.unique(native_alpha)],'native_transparent_pixels':int((native==255).sum()),'native_8connected_component_sizes':component_sizes,'transparent_composite_pixels_equal_actual_background':True,'decoded_indexed_pixels_equal':True})
        path=proof/'four-background-alpha-2x.png';qa.resize((1536,832),Image.Resampling.NEAREST).save(path)
        result={'slug':slug,'status':'ALPHA_CROP_REGISTRATION_AND_DECODE_GATES_PASS','source_master_sha256':file_sha(config_path.parent/spec['master']),'source_alpha_range':[int(a.min()),int(a.max())],'source_corners_alpha':[int(a[0,0]),int(a[0,-1]),int(a[-1,0]),int(a[-1,-1])],'common_cel_size':g['loop0']['size'],'fixed_screen_anchor':g['screen_feet'],'one_common_scale':g['uniform_scale'],'resource_bytes':report['resource_bytes'],'resource_sha256':report['resource_sha256'],'alpha_proof':str(path.relative_to(output)),'cells':cells,'meaning':'Binary output alpha has no semitransparent halo; every transparent pixel composites to exact background. Components are measured, not automatically removed. Visual review must distinguish detached prop pixels from unwanted fragments.'}
        dump(proof/'alpha-registration-checks.json',result);results.append(result)
    summary={'status':('ALL64_SOURCE_AND_PIXEL_GATES_PASS' if len(results)==8 else 'PARTIAL_EXPORT_SOURCE_AND_PIXEL_GATES_PASS'),'characters':[r['slug'] for r in results],'results':results,'all_eight_structural_export':len(results)==8,'all_eight_choreography_acceptance':False,'native_verified':False}
    dump(output/'ALPHA-REGISTRATION-CHECKS.json',summary)
    print(json.dumps({r['slug']:{'bytes':r['resource_bytes'],'sole_max_y_exclusive':[c['native_screen_opaque_bbox'][3] for c in r['cells']],'components':[c['native_8connected_component_sizes'] for c in r['cells']]} for r in results},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args();verify(args.config.resolve(),args.output.resolve())
