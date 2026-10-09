#!/usr/bin/env python3
"""Build readable64-pose and8-freeze proof images from exported cels."""
import argparse
import json
from pathlib import Path
from PIL import Image
from export_opening import Art, CAST, file_sha, dump

def build(output):
    art=Art();manifest=json.loads((output/'OPENING-ASSET-MANIFEST.json').read_text())
    assert manifest['complete_eight_character_export'] and manifest['total_action_cels']==64
    sheet=Image.new('RGBA',(1024,126*8),tuple(art.colors[art.cream])+(255,))
    freezes=Image.new('RGBA',(1280,288),(0,0,0,255));rows=[]
    for row,(slug,name,view,*_) in enumerate(CAST):
        proof=output/'proof'/slug;g=json.loads((proof/'geometry-contract.json').read_text());checks=json.loads((proof/'export-checks.json').read_text())
        label=art.lettering(name);sheet.alpha_composite(label.convert('RGBA'),(4,row*126+2))
        row_proof=Image.new('RGBA',(1024,126),tuple(art.colors[art.cream])+(255,));row_proof.alpha_composite(label.convert('RGBA'),(4,2))
        for ci in range(8):
            canvas=Image.new('RGBA',(320,144))
            for prop in g['stable_prop_loops']:
                im=Image.open(output/'cels'/slug/f'loop{prop["loop"]:02}-cel00-rgba.png');canvas.alpha_composite(im,tuple(prop['draw']))
            im=Image.open(output/'cels'/slug/f'loop00-cel{ci:02}-rgba.png');canvas.alpha_composite(im,tuple(g['loop0']['draw']))
            tile=canvas.crop((62,32,190,144));sheet.alpha_composite(tile,(ci*128,row*126+14));row_proof.alpha_composite(tile,(ci*128,14))
            numeral=art.lettering(str(ci));sheet.alpha_composite(numeral.convert('RGBA'),(ci*128+116,row*126+2));row_proof.alpha_composite(numeral.convert('RGBA'),(ci*128+116,2))
        row_proof.resize((2048,252),Image.Resampling.NEAREST).save(proof/'all-eight-isolated-2x.png')
        freezes.alpha_composite(Image.open(proof/'freeze-native.png').convert('RGBA'),((row%4)*320,(row//4)*144))
        rows.append({'row':row,'slug':slug,'view':view,'resource_sha256':checks['resource_sha256'],'loop0_common_size':g['loop0']['size'],'stable_prop_loops':g['stable_prop_loops']})
    review=output/'review';review.mkdir(exist_ok=True)
    sheet.resize((2048,2016),Image.Resampling.NEAREST).save(review/'ALL-64-POSES-2X.png')
    freezes.save(review/'ALL-8-FREEZES-NATIVE.png');freezes.resize((2560,576),Image.Resampling.NEAREST).save(review/'ALL-8-FREEZES-2X.png')
    title=Image.open(output/'proof/vivian/shared-title-native.png');title.save(review/'SHARED-TITLE-NATIVE.png');title.resize((1280,576),Image.Resampling.NEAREST).save(review/'SHARED-TITLE-4X.png')
    dump(review/'REVIEW-IMAGE-INDEX.json',{'status':'OFFLINE_PIXEL_PROOFS_NOT_NATIVE_RUNTIME_ACCEPTANCE','rows':rows,'files':{p.name:file_sha(p) for p in review.glob('*.png')},'notes':['All64 action cels at the same native scale, enlarged2x without resampling blur.','Static chairs/bench are composited from their single separate loops.','Both title cards use the same250/3 cel; not counted as cast action poses.']})
    print(str(review/'ALL-64-POSES-2X.png'))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args();build(args.output.resolve())
