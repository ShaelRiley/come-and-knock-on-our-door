"""Packaging boundary: readable table/text data must exactly match pinned source."""
from pathlib import Path
import re,json,hashlib

def validate(H):
 H=Path(H);G=H/'generated/static';chunks=[];names=[]
 pins={'snapshot/contest/canonical-bindings.json':'cd11fda0a88847aa2d6650acf76d8a606ac9f62004dd18090f61033d69c7851e','snapshot/contest/manifest.json':'bef627740b7b2c8b8a082c2063c7dbd2b3a0df26da8830c80851e09f5fdf164b','snapshot/r2/module981.sc':'09bb8cce3d0a9e4a567a5aae4c787bd6f94fafbfd0fdfc1a8f1f7cc1a65ba8bb'}
 for f,digest in pins.items():
  if hashlib.sha256((H/f).read_bytes()).hexdigest()!=digest:raise RuntimeError('Static authority changed: '+f)
 for file in ['snapshot/contest-scene/module982.sc','snapshot/contest-scene/route-tables.inc','snapshot/r2/module981.sc']:
  for m in re.finditer(r'\[(\w+)\s+(\d+)\]\s*=\s*\[([^]]*)\]',(H/file).read_text()):
   if m[1] in ['currentGains','targetGains']:continue
   values=[int(v)&65535 for v in m[3].split()]
   if len(values)!=int(m[2]):raise RuntimeError('Static declaration length changed')
   names.append(m[1])
   for i in range(0,len(values),20):
    row=values[i:i+20];chunks.append((''.join(f'{v:05d} ' for v in row+[0]*(20-len(row)))).encode()+b'\0')
 for resource,start in [(240,0),(241,480)]:
  expected=b''.join(chunks[start:start+480]);actual=(G/f'{resource}.text.bin').read_bytes()
  if len(expected)>65535 or actual!=expected:raise RuntimeError(f'Static bank {resource} has changed length/format/words')
  if any(len(c)!=121 or re.fullmatch(rb'(?:[0-9]{5} ){20}\x00',c) is None for c in chunks[start:start+480]):raise RuntimeError('Static text buffer capacity/grammar')
 rows={r['id']:r for r in json.loads((H/'snapshot/contest/canonical-bindings.json').read_text())['records']};manifest=json.loads((H/'snapshot/contest/manifest.json').read_text())
 text=[rows[rid]['text'] for rid,n in manifest['records'].items() if rid.startswith('VC.UI.')]+[rows[f'IR{i:02d}.REPLY']['text'] for i in range(1,25)]+[f'IR{i:02d}' for i in range(1,25)]
 norm=lambda t:t.translate(str.maketrans({'’':"'",'‘':"'",'“':'"','”':'"','—':'-','–':'-','…':'...'})).upper().encode('latin1')+b'\0'
 expected=b''.join(map(norm,text))
 if (G/'242.text.bin').read_bytes()!=expected:raise RuntimeError('Canonical UI text bank changed')
 if any(len(norm(t))>(80 if i<37 else 8) for i,t in enumerate(text)):raise RuntimeError('Canonical label buffer overflow')
 return {'static_arrays':names,'words_per_entry':20,'entry_bytes_with_nul':121,'static_buffer_bytes':128,'resource_numbers':[240,241,242]}
