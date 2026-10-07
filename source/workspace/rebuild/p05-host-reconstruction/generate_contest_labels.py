"""Canonical menu strings reloaded from packaged text, never trusted saved heap."""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;G=H/'generated/static';G.mkdir(parents=True,exist_ok=True)
j=json.loads((H/'snapshot/contest/canonical-bindings.json').read_text());rows={r['id']:r for r in j['records']};manifest=json.loads((H/'snapshot/contest/manifest.json').read_text())
def norm(t):return t.translate(str.maketrans({'’':"'",'‘':"'",'“':'"','”':'"','—':'-','–':'-','…':'...'})).upper()
entries=[];source=[];decl=[];meta=[]
def emit(name,arg,items,words):
 source.append(f'(method ({name} {arg}) (switch {arg}')
 for ident,rid,text in items:
  entry=len(entries);value=norm(text);assert len(value.encode('latin1'))+1<=words*2
  entries.append(value);buf=f'{name}Buffer{ident:02d}';decl.append(f'[{buf} {words}]')
  source.append(f' ({ident} (GetFarText 242 {entry} @{buf}) (return @{buf}))')
  meta.append(dict(method=name,id=ident,record=rid,entry=entry,text=value,buffer_words=words))
 source.append(') (return 0))')
emit('hVCLabel','id',[(n,rid,rows[rid]['text']) for rid,n in manifest['records'].items() if rid.startswith('VC.UI.')],40)
emit('hVCReplyLabel','pair',[(i,f'IR{i:02d}.REPLY',rows[f'IR{i:02d}.REPLY']['text']) for i in range(1,25)],40)
emit('hVCSetupLabel','pair',[(i,None,f'IR{i:02d}') for i in range(1,25)],4)
source += ['(method (hLabelsInit &tmp i) (for ((= i 1)) (<= i 13) ((++ i)) (self hVCLabel: i)) (for ((= i 1)) (<= i 24) ((++ i)) (self hVCReplyLabel: i) (self hVCSetupLabel: i)) (return 1))']
source += ['(method (hLabelWord entry index) (switch entry']
for row in meta:source.append(f' ({row["entry"]} (return [{row["method"]}Buffer{row["id"]:02d} index]))')
source += [') (return 0))', '(method (hLabelsValidate &tmp entry i count) (for ((= entry 0)) (< entry 61) ((++ entry)) (for ((= i 0)) (< i 64) ((++ i)) (= [hStaticBuffer i] 0)) (GetFarText 242 entry @hStaticBuffer) (= count (if (< entry 37) 40 else 4)) (for ((= i 0)) (< i count) ((++ i)) (if (!= [hStaticBuffer i] (self hLabelWord: entry i)) (= hFailure 41) (return 0)))) (return 1))']
(H/'contest_labels.sc.inc').write_text('; Exact canonical text; fresh packaged-resource load on every use.\n'+'\n'.join(source)+'\n')
(G/'label-locals.inc').write_text('\n'.join(decl)+'\n');(G/'242.text.bin').write_bytes(b''.join(t.encode('latin1')+b'\0' for t in entries));(G/'labels.json').write_text(json.dumps(meta,indent=2)+'\n')
print('generated',len(entries),'canonical fresh-buffer labels')
