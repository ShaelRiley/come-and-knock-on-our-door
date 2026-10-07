#!/usr/bin/env python3
"""Regenerate native views from editable indexed PNG cels, without re-quantizing."""
from common import ROOT,Guard,sha,write_json,require
_entry_guard=Guard('encode_indexed') if __name__=='__main__' else None
import json,hashlib
from PIL import Image
from view_writer import Cel,encode_view
from inspect_view import decode_view

def run():
 g=_entry_guard or Guard('encode_indexed');m=json.loads((ROOT/'manifest.json').read_text());pal=sum(json.loads((ROOT/'reference/palette-999.json').read_text())['rgb'],[])
 for n,item in m['resources'].items():
  records=[c for c in m['cels'] if c['view']==int(n)];records.sort(key=lambda c:c['cel']);cels=[]
  for c in records:
   p=ROOT/c['file'];im=Image.open(p);require(im.mode=='P' and list(im.size)==c['size'],'Indexed edit changed canvas');require(im.getpalette()==pal and im.info.get('transparency')==255,'Palette/clear-key changes are forbidden');cels.append(Cel(*im.size,im.tobytes()));c['sha256']=sha(p);c['pixel_sha256']=hashlib.sha256(im.tobytes()).hexdigest();opaque=[(i%im.width,i//im.width) for i,value in enumerate(im.tobytes()) if value!=255];require(bool(opaque),'Fully empty prop is not an accepted edit');c['opaque_bbox']=[min(x for x,y in opaque),min(y for x,y in opaque),max(x for x,y in opaque)+1,max(y for x,y in opaque)+1]
  raw=encode_view([cels]);d=decode_view(raw);require(all(x.pixels==y['pixels'] for x,y in zip(cels,d[0])),'Independent roundtrip mismatch');p=ROOT/item['file'];p.write_bytes(raw);item['sha256']=sha(p);item['bytes']=len(raw)
 write_json(ROOT/'manifest.json',m);g.done()
if __name__=='__main__':run()
