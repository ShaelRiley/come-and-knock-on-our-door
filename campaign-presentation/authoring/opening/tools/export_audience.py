#!/usr/bin/env python3
"""Bounded shared audience-apron art export; no source or hotspot changes."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
from export_opening import Art
from view_writer import Cel,encode_view
from inspect_view import decode_view

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audience-apron-r1'
ART=Art()
MASTER=ROOT/'masters/audience-apron-background-r1.png'
PROMPT=ROOT/'prompts/audience-apron-background-r1.txt'
OLD102=ROOT/'references/102-original-audience.view.bin'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put_text(im,text,xy):
    glyph=ART.lettering(text,1,ART.ink)
    im.paste(glyph,xy,glyph.convert('RGBA').getchannel('A'))

def main():
    OUT.mkdir(exist_ok=True)
    source=Image.open(MASTER).convert('RGBA')
    native=source.resize((320,144),Image.Resampling.LANCZOS)
    base=ART.index(native)
    oldcel=decode_view(OLD102.read_bytes())[0][0]
    old=ART.blank((320,144));old.putdata(oldcel['pixels'])
    arrow=old.crop((8,68,14,77));back=arrow.getpixel((0,0))
    arrowmask=Image.new('L',arrow.size)
    arrowmask.putdata([0 if v==back else 255 for v in arrow.tobytes()])
    assert set(base.tobytes())<=set(range(218))
    base.save(OUT/'shared-background-indexed.png')
    records=[]
    for view,label in [(102,'SAME PORCH'),(103,'SAME LIVING')]:
        im=base.copy();d=ImageDraw.Draw(im)
        # Existing labels use original glyph pixels; revised placement stays
        # inside original left wing and unchanged return interaction region.
        d.rectangle((43,51,119,64),fill=ART.cream)
        put_text(im,label,(47,54))
        d.rectangle((11,115,88,128),fill=ART.cream)
        put_text(im,'  RETURN',(16,118))
        im.paste(ART.ink,(16,117,22,126),arrowmask)
        d.rectangle((166,131,277,143),fill=ART.cream)
        put_text(im,'TALK TO AUDIENCE',(171,134))
        payload=encode_view([[Cel(320,144,im.tobytes())]])
        decoded=decode_view(payload)
        assert len(decoded)==1 and len(decoded[0])==1
        assert decoded[0][0]['pixels']==im.tobytes()
        assert len(payload)<=65535 and 255 not in im.tobytes()
        p=OUT/f'{view}.view.bin';p.write_bytes(payload)
        im.save(OUT/f'{view}-indexed.png')
        im.convert('RGB').resize((1280,576),Image.Resampling.NEAREST).save(OUT/f'{view}-review-4x.png')
        records.append({'view':view,'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':len(payload),'loop':0,'cel':0,'size':[320,144],'draw':[0,0],'return_label':label,'decoded_pixel_equality':True,'opaque_palette_range':[0,217]})
    data={'schema':'CAKOOD_AUDIENCE_APRON_ART_R1','master':str(MASTER.relative_to(ROOT)),'master_sha256':sha(MASTER),'prompt':str(PROMPT.relative_to(ROOT)),'prompt_sha256':sha(PROMPT),'one_shared_background':True,'palette999_sha256':ART.palette_hash,'font0_sha256':ART.font_hash,'generated_lettering':False,'less_than_arrow_source':{'resource':'VIEW102','sha256':sha(OLD102),'crop':[8,68,14,77]},'hotspots_unchanged':{'return':[8,102,112,134],'audience':[161,52,307,130],'notes':[160,2,211,12]},'resources':records,'scope':'Replaces current prototype audience-apron pixels only; no new interaction or source edits.','native_verified':False}
    (OUT/'AUDIENCE-ART-MANIFEST.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
if __name__=='__main__':main()
