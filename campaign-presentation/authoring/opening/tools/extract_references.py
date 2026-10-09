#!/usr/bin/env python3
"""Extract actual retained project pixels, never label them generated masters."""
from pathlib import Path
import hashlib
import json
import struct
from PIL import Image, ImageDraw
from inspect_view import decode_view

ROOT = Path(__file__).resolve().parents[2]
DEST = Path(__file__).resolve().parents[1] / 'references'
SOURCE = ROOT.parent / 'source/assets/resources'
PINNED_PALETTE = '432ddf6a8f2ae34d7bdfd5c9c226ee0ba5e1e8e178bf851b59cb76f6ea5c0642'
NAMES = {214:'jackie',219:'bunny',218:'frankie',222:'stringer',221:'milo',236:'vivian',223:'rita',225:'felix'}
BACKGROUNDS = {100:'porch',101:'living',300:'kitchen',302:'conservatory',303:'side-passage',304:'garage'}

def sha(data): return hashlib.sha256(data).hexdigest()

def read_palette(data):
    if len(data) != 805 or data[25] != 0 or struct.unpack_from('<H',data,29)[0] != 256 or data[32] != 1:
        raise ValueError('Expected current project full SCI1.1 constant RGB palette')
    return [list(data[i:i+3]) for i in range(37,805,3)]

def read_font(data):
    zero,count,height = struct.unpack_from('<HHH',data)
    if zero or count != 128: raise ValueError('Unexpected original font0 layout')
    out = {}
    for code in range(count):
        at = struct.unpack_from('<H',data,6+2*code)[0]
        w,h = data[at:at+2]; stride = (w+7)//8
        raw = data[at+2:at+2+h*stride]
        if len(raw) != h*stride: raise ValueError('Truncated font glyph')
        out[str(code)] = {'width':w,'height':h,'rows_hex':raw.hex()}
    return {'height':height,'count':count,'glyphs':out}

def extract():
    DEST.mkdir(parents=True,exist_ok=True)
    palette_data = (SOURCE/'999.palette.bin').read_bytes()
    assert sha(palette_data) == PINNED_PALETTE
    palette = read_palette(palette_data)
    (DEST/'palette999.json').write_text(json.dumps({'source':str((SOURCE/'999.palette.bin').relative_to(ROOT)), 'source_sha256':sha(palette_data),'colors_rgb':palette,'allowed_opaque_indices':[0,217],'transparent_index':255},indent=2)+'\n')
    font_data = (SOURCE/'000.font.bin').read_bytes()
    font = read_font(font_data)
    font.update(source=str((SOURCE/'000.font.bin').relative_to(ROOT)),source_sha256=sha(font_data),status='EXACT_FONT0_BITMAP_EXTRACTION_NO_SYNTHESIS')
    (DEST/'font0-glyphs.json').write_text(json.dumps(font,indent=2)+'\n')
    ledger=[]
    for number,slug in {**NAMES,**BACKGROUNDS}.items():
        src=SOURCE/f'{number:03}.view.bin'; data=src.read_bytes(); loops=decode_view(data)
        record={'view':number,'slug':slug,'source':str(src.relative_to(ROOT)),'source_sha256':sha(data),'source_bytes':len(data),'status':'EXTRACTED_CURRENT_COMPILED_PIXELS_NOT_RECOVERED_MASTER','loops':[len(x) for x in loops],'outputs':[]}
        record['origin_qualification'] = ('Historical user-project bytes established; individual creation receipts remain incomplete. Inherited qualification preserved.' if number in (221,222,223,300,302) else 'Current retained source; extraction establishes byte provenance, not a new creation claim.')
        selections = [(li,ci,cel) for li,loop in enumerate(loops) for ci,cel in enumerate(loop) if ci==0] if number in NAMES else [(0,0,loops[0][0])]
        for li,ci,cel in selections:
            im=Image.frombytes('P',(cel['width'],cel['height']),cel['pixels']); im.putpalette(sum(palette,[])); im.info['transparency']=cel['clear_key']
            stem=f'{number}-{slug}-loop{li:02}-cel{ci:02}'
            p=DEST/f'{stem}.png'; im.save(p,transparency=cel['clear_key'])
            rgba=im.convert('RGBA'); p2=DEST/f'{stem}-10x-transparent.png'; rgba.resize((rgba.width*10,rgba.height*10),Image.Resampling.NEAREST).save(p2)
            record['outputs'].append({'loop':li,'cel':ci,'size':list(im.size),'opaque_bbox':rgba.getbbox(),'clear_key':cel['clear_key'],'pixels_sha256':sha(cel['pixels']),'file':p.name,'sha256':sha(p.read_bytes()),'enlarged_file':p2.name,'enlarged_sha256':sha(p2.read_bytes())})
        ledger.append(record)
    for filename,data in [('999.palette.bin',palette_data),('000.font.bin',font_data)]:
        (DEST/filename).write_bytes(data)
    manifest={'status':'SOURCE_REFERENCE_EXTRACTION_ONLY','source_root':str(SOURCE.relative_to(ROOT)),'palette_sha256':sha(palette_data),'font0_sha256':sha(font_data),'extraction_script_sha256':sha(Path(__file__).read_bytes()),'decoder_sha256':sha((Path(__file__).parent/'inspect_view.py').read_bytes()),'references':ledger}
    (DEST/'SOURCE-REFERENCE-LEDGER.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'references':len(ledger),'rita':[o['enlarged_file'] for r in ledger if r['view']==223 for o in r['outputs']]},indent=2))

if __name__=='__main__': extract()
