"""Code-native phase cels from bundled project pixels; historical qualifications remain.
Portable function-only adaptation 2026-10-08; preview composition excluded.
"""
from pathlib import Path
import struct,hashlib
from PIL import Image,ImageDraw
from view_decoder import decode_view

def generate(inputs,out):
    inputs=Path(inputs);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    def original(n,cel):
     c=decode_view((inputs/f'{n:03d}.view.bin').read_bytes())[0][cel]
     return Image.frombytes('P',(c['width'],c['height']),c['pixels'])
    def blank(w,h):return Image.new('P',(w,h),255)
    def paste(dest,im,xy):dest.paste(im,xy,Image.frombytes('L',im.size,bytes(0 if i==255 else 255 for i in im.tobytes())))
    def write(n,cels):
     size=18+16+36*len(cels);headers=bytearray();pixels=bytearray()
     for im in cels:
      w,h=im.size;headers+=struct.pack('<hhhhBBHIIIIII',w,h,0,0,255,0,0,w*h,0,0,0,size+len(pixels),0);pixels+=im.tobytes()
     data=struct.pack('<HBBHHIBBHH',16,1,0,1,len(cels),0,16,36,320,200)+struct.pack('<BBBBIII',255,0,len(cels),0,0,0,34)+headers+pixels
     assert len(data)<65536;assert len(decode_view(data)[0])==len(cels)
     (out/f'{n:03d}.view.bin').write_bytes(data)
     return hashlib.sha256(data).hexdigest()
    cover=original(224,10);cart=original(227,7)
    # The accepted handcart is already padded. Reuse original linen pixels solely
    # as its permanent presentation padding; no inventory cloth is consumed.
    pad=original(224,5)
    for x in (5,17,26):paste(cart,pad,(x,21))
    fold=[]
    for width in (28,19,9,2):
     im=blank(96,56)
     # Three opaque covered wings. The center is the exact original covered display;
     # hinged side wings reuse its wood texture and narrow by perspective.
     wing=cover.resize((width,48),Image.Resampling.NEAREST)
     paste(im,wing,(32-width,0));paste(im,cover,(32,0));paste(im,wing.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(64,0))
     d=ImageDraw.Draw(im)
     # Padded stops and inward-arrow catch remain visible; no decorative panel face.
     for x in (31,63):d.rectangle((x,12,x+1,39),fill=218);d.rectangle((x,41,x+2,44),fill=207)
     d.line((43,24,48,27,43,30),fill=218,width=1);d.line((53,24,48,27,53,30),fill=218,width=1)
     fold.append(im)
    xs=[186,202,218,207,198,184,175];ys=[69,65,60,56,54,54,54]
    stage=[]
    for i,(x,y) in enumerate(zip(xs,ys)):
     im=blank(40,67);paste(im,cart,(0,24));paste(im,cover,(4,0))
     # Back toward the existing house corner, then behind its x=217 occlusion edge.
     # Crop the moving sprites, never repaint background or reveal another location.
     if i>=3:
      d=ImageDraw.Draw(im);d.rectangle((0,0,min(39,216-x),66),fill=255)
     stage.append(im)
    assert stage[-1].tobytes()==bytes([255])*40*67
    poses=[]
    for actor in (216,225):
     for mouth in range(3):
      im=original(actor,mouth)
      if actor==225:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
      d=ImageDraw.Draw(im)
      # Small original raised forearm geometry, using each original costume palette.
      # Both palm tips visibly meet the covered wings as the pair bring them inward.
      if actor==216:
       d.line((31,29,38,38,48,41),fill=136,width=5)
       d.line((32,29,39,37,49,40),fill=166,width=2)
       d.ellipse((47,38,51,43),fill=207)
      else:
       d.line((17,32,12,38,3,40),fill=156,width=5)
       d.line((17,31,11,37,2,39),fill=154,width=2)
       d.ellipse((0,38,5,43),fill=207)
      poses.append(im)
    hashes={239:write(239,fold),240:write(240,stage),241:write(241,poses+[cart])}
    return hashes
