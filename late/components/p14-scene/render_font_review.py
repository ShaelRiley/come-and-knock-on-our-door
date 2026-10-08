from pathlib import Path
from PIL import Image,ImageDraw
import struct,json
H=Path(__file__).resolve().parent
font=(H/'generated/001.font.bin').read_bytes()
def paint(im,text,x,y,scale=4):
 for c in text:
  if c=='\n':x=16;y+=8*scale;continue
  pos=struct.unpack_from('<H',font,6+ord(c)*2)[0]
  for row,b in enumerate(font[pos+2:pos+10]):
   for col in range(6):
    if b&(128>>col):ImageDraw.Draw(im).rectangle([x+col*scale,y+row*scale,x+(col+1)*scale-1,y+(row+1)*scale-1],fill='white')
  x+=6*scale
im=Image.new('RGB',(1264,400),'#162335');d=ImageDraw.Draw(im)
d.text((16,8),'P14 ORIGINAL FONT1: all printable ASCII, 6x8 pixels enlarged 4x. Pipe glyph exists but is rejected as markup.',fill='white')
for i,start in enumerate(range(32,127,16)):
 paint(im,''.join(chr(c) for c in range(start,min(start+16,127))),16,40+i*48)
im.save(H/'evidence/font1-glyph-contact-sheet.png')
f=json.loads((H/'inputs/canonical-bindings.json').read_text());r=next(r for r in f['records'] if r['id']=='END.ASSET.AUDIENCE.01')
from caption_layout import paginate
url=next(w for w in r['text'].split() if w.startswith('https://'))
example='Example selected date: MiXeD Tue 17 May '+('x'*43)
lines=[p['text'] for p in paginate(url,preserve_case=True)]+[example[i:i+50] for i in range(0,len(example),50)]
im=Image.new('RGB',(1264,280),'#162335');d=ImageDraw.Draw(im)
d.text((16,8),'SOURCE FONT MATRIX REVIEW ONLY: wrapped canonical URL and explicit synthetic date fixture; no selected game date/native screenshot claim',fill='white')
for i,line in enumerate('\n'.join(lines).splitlines()):paint(im,line,16,44+i*36)
im.save(H/'evidence/font1-url-date-examples.png')
