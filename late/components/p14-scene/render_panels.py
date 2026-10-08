"""Actual 320x200 coordinates and 8-pixel leading; software font-matrix proof."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,struct
H=Path(__file__).resolve().parent
FONT=(H/'generated/001.font.bin').read_bytes()
def draw_text(image,text,x,y):
 d=ImageDraw.Draw(image);origin=x
 for c in text:
  if c=='\n':x=origin;y+=8;continue
  pos=struct.unpack_from('<H',FONT,6+ord(c)*2)[0]
  for row,b in enumerate(FONT[pos+2:pos+10]):
   for col in range(6):
    if b&(128>>col):d.point((x+col,y+row),fill='white')
  x+=6

def main():
 m=json.loads((H/'generated/manifest.json').read_text());credit=next(p for p in m['pages'] if p['record_id']=='END.ASSET.AUDIENCE.01' and p['document_page']==1)
 # Exactly three rows, including descenders followed immediately by capitals.
 text='gypqj '+('x'*44)+'\nCAPITALS AFTER DESCENDERS MiXeD Case\nhttps://freesound.org/people/Benboncan/'
 raw='MiXeD selected test date ';raw+='q'*(80-len(raw));assert len(raw)==80
 template=next(r['text'] for r in m['canonical_records'] if r['id']=='P14.READ.001');expanded=template.format(repair_date=raw);date='\n'.join(expanded[i:i+50] for i in range(0,150,50))
 panels=[('Exact8px leading, all3rows and descenders',text),('Canonical wrapped credit body, exact panel geometry',credit['text']),('Synthetic80char mixed-case date, exact first page',date)]
 final=Image.new('RGB',(1280,3*280),'#162335');fdraw=ImageDraw.Draw(final)
 for i,(label,body) in enumerate(panels):
  panel=Image.new('RGB',(320,200),'black');d=ImageDraw.Draw(panel);d.rectangle((0,144,319,199),fill='#162335');draw_text(panel,'P14 FONT1',6,147);draw_text(panel,body,6,158)
  assert len(body.splitlines())<=3 and all(len(x)<=50 for x in body.splitlines())
  # Every body glyph stays inside the24-pixel 158..181 body band.
  pixel_rows=[y for y in range(158,200) if any(panel.getpixel((x,y))==(255,255,255) for x in range(6,315))];assert pixel_rows and max(pixel_rows)<=181
  final.paste(panel.crop((0,144,320,200)).resize((1280,224),Image.Resampling.NEAREST),(0,i*280+40));fdraw.text((16,i*280+12),label+'; source pixels only, no native screenshot claim',fill='white')
 final.save(H/'evidence/font1-exact-panel-leading.png')
 (H/'evidence/font-panel-pixels.json').write_text(json.dumps(dict(status='PASS_SOFTWARE_FONT_MATRIX',body_coordinates=[6,158,314,182],leading_pixels=8,rows=3,glyph_height=8,all_glyph_pixels_inside_body=True,native_screenshot_acceptance=False),indent=2)+'\n')
if __name__=='__main__':main()
