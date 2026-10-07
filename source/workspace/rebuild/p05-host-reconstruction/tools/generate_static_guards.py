"""Readable packaged constants; exact restored-word equality, no saved trust flag."""
from pathlib import Path
import re,json,hashlib
H=Path(__file__).resolve().parents[1];G=H/'generated/static';G.mkdir(parents=True,exist_ok=True)
inputs=[(982,H/'snapshot/contest-scene/module982.sc',None),(985,H/'snapshot/contest-scene/route-tables.inc',None),(981,H/'snapshot/r2/module981.sc',{'currentGains','targetGains'})]
tables=[];chunks=[];access={981:[],982:[],985:[]}
for mod,p,exclude in inputs:
 for m in re.finditer(r'\[(\w+)\s+(\d+)\]\s*=\s*\[([^]]*)\]',p.read_text()):
  name,count=m[1],int(m[2]);values=[int(v)&65535 for v in m[3].split()]
  if exclude and name in exclude:continue
  assert len(values)==count,(name,count,len(values))
  if mod==981:assert not re.search(r'\b(?:sali|ssli|spli|sapi|sali\+|sali-)\s+'+name+r'\b',p.read_text()),name
  tid=len(tables)+1;base=len(chunks)
  for start in range(0,count,20):
   words=values[start:start+20];chunks.append(''.join(f'{v:05d} ' for v in words+[0]*(20-len(words))))
  tables.append(dict(id=tid,module=mod,name=name,count=count,first_chunk=base,source=str(p.relative_to(H)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),values=values))
  access[mod].append(f' ({tid} (if (or (< index 0) (>= index {count})) (return 0)) (return [{name} index]))')
assert len(chunks)<=960
for resource,start in [(240,0),(241,480)]:
 raw=b''.join(c.encode()+b'\0' for c in chunks[start:start+480]);assert len(raw)<65536;(G/f'{resource}.text.bin').write_bytes(raw)
for mod,rows in access.items():(G/f'module{mod}-methods.inc').write_text('(method (hStaticAt table index) (switch table\n'+'\n'.join(rows)+'\n) (return 0))\n')
s='''; Resource 240/241 contain named decimal tables generated from reviewed inputs.
; Never trust a saved cache, digest or validation flag. Reload each checked chunk.
(method (hStaticCount table) (switch table
'''+''.join(f' ({t["id"]} (return {t["count"]}))\n' for t in tables)+''') (return 0))
(method (hStaticFirst table) (switch table
'''+''.join(f' ({t["id"]} (return {t["first_chunk"]}))\n' for t in tables)+''') (return -1))
(method (hStaticOwner table) (switch table
'''+''.join(f' ({t["id"]} (return (ScriptID {t["module"]} 0)))\n' for t in tables)+''') (return 0))
(method (hStaticLoad table index &tmp chunk i)
 (= chunk (self hStaticFirst: table)) (if (< chunk 0) (return 0))
 (= chunk (+ chunk (/ index 20)))
 (for ((= i 0)) (< i 64) ((++ i)) (= [hStaticBuffer i] 0))
 (GetFarText (if (< chunk 480) 240 else 241) (mod chunk 480) @hStaticBuffer)
 (if (or (!= (>> [hStaticBuffer 59] 8) 32) [hStaticBuffer 60] [hStaticBuffer 61] [hStaticBuffer 62] [hStaticBuffer 63]) (return 0))
 (return 1))
(method (hStaticValue slot &tmp i word digit value)
 (= hStaticParseOK 0) (= value 0)
 (if (or (< slot 0) (>= slot 20)) (return 0))
 (for ((= i 0)) (< i 5) ((++ i))
  (= word [hStaticBuffer (+ (* slot 3) (/ i 2))])
  (= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
  (if (or (< digit 0) (> digit 9)) (return 0))
  (= value (+ (* value 10) digit)))
 (if (!= (>> [hStaticBuffer (+ (* slot 3) 2)] 8) 32) (return 0))
 (= hStaticParseOK 1) (return value))
(method (hStaticRange table first count &tmp i expected owner)
 (if (or (< first 0) (< count 1) (> (+ first count) (self hStaticCount: table))) (= hFailure 40) (return 0))
 (= owner (self hStaticOwner: table)) (if (not owner) (= hFailure 40) (return 0))
 (for ((= i first)) (< i (+ first count)) ((++ i))
  (if (or (== i first) (== (mod i 20) 0)) (if (not (self hStaticLoad: table i)) (= hFailure 40) (return 0)))
  (= expected (self hStaticValue: (mod i 20)))
  (if (or (not hStaticParseOK) (!= expected (owner hStaticAt: table i))) (= hFailure 40) (return 0)))
 (return 1))
(method (hStaticAll &tmp table)
'''+f' (for ((= table 1)) (<= table {len(tables)}) ((++ table))\n'+'''  (if (not (self hStaticRange: table 0 (self hStaticCount: table))) (return 0)))
 (return 1))
'''
(G/'guard-methods.inc').write_text(s);(G/'guard-locals.inc').write_text('[hStaticBuffer 64]\n')
(G/'manifest.json').write_text(json.dumps({'format':'20 unsigned decimal SCI16 words per NUL-terminated text entry; six ASCII bytes per word; tables padded independently','resources':[240,241],'tables':tables},indent=2)+'\n')
print([(t['id'],t['module'],t['name'],t['count']) for t in tables],len(chunks))
