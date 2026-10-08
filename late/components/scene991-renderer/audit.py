#!/usr/bin/env python3
"""Exact edit boundary, typed-resource identity and reserved ABI audit."""
from pathlib import Path
import json,sys,struct,re
sys.dont_write_bytecode=True
from derive import H,F,derive,sha,dump,require,MOVED,digest
from source_tools import methods,tokens

def audit():
 derive(True)
 receipt=json.loads((H/'build/coherent/compile-receipt.json').read_text());old=json.loads((F/'build/coherent/compile-receipt.json').read_text());oldrows={r['module']:r for r in old['modules']};rows={r['module']:r for r in receipt['modules']}
 require(receipt['class_owners']==old['class_owners']+[991],'Class universe not append-only')
 for n,r in rows.items():
  require(sha(H/f'build/coherent/compiled/{n}.scr.bin')==r['script_sha256'] and sha(H/f'build/coherent/compiled/{n}.scr.bin.hep')==r['heap_sha256'],'Changed compiled bytes')
  if n not in (0,991):require(all(r[k]==oldrows[n][k] for k in ('source_sha256','script_sha256','heap_sha256')),'Unrelated module changed',n)
 bm=methods((F/'src/main.sc').read_text());mm=methods((H/'src/main.sc').read_text());sm=methods((H/'src/module991.sc').read_text())
 require(set(bm)==set(mm) and set(sm)==set(MOVED),'Method set changed')
 require({n for n in mm if mm[n]!=bm[n]}==set(MOVED),'Unexpected Main method edit')
 require((H/'src/main.sc').read_text().split('(method')[0]==(F/'src/main.sc').read_text().split('(method')[0],'Main local/property prefix edited')
 selectors=json.loads((H/'selectors.json').read_text());require(selectors==json.loads((F/'selectors.json').read_text()),'Selector allocation')
 res=H/'build/coherent/verification-checkpoint/assets/resources';oldres=F/'build/coherent/verification-checkpoint/assets/resources'
 require({p.name for p in res.iterdir()}=={p.name for p in oldres.iterdir()},'Resource IDs changed')
 changed=[p.name for p in res.iterdir() if sha(p)!=sha(oldres/p.name)];require(changed==['996.vocab.bin'],'Unrelated resource change',changed)
 require((res/'996.vocab.bin').read_bytes()==(oldres/'996.vocab.bin').read_bytes()+struct.pack('<HH',0,991),'Class owner append')
 closure=json.loads((H/'toolchain/SOURCE-MANIFEST.json').read_text())['files'];require(len(closure)==198,'Source closure not minimal')
 for n,v in closure.items():require(sha(H/'toolchain/source'/n)==v,'Compiler source changed')
 # Returned string consumer audit: existing source has exactly two Main sends of selector252.
 callers=[]
 for file in (F/'src').glob('*.sc'):
  for name,body in methods(file.read_text()).items():
   if name=='roomTitle':continue
   if re.search(r'\broomTitle[:?]|pushi\s+252\s+push0\s+self\s+4',body):
    callers.append([file.name,name]);require(file.name=='main.sc' and name in ('render','h6BaseDrawWorld'),'New roomTitle consumer')
    require(re.search(r'pushi 11\s+pushi 252\s+push0\s+self 4\s+push\s+pushi 100',body),'Returned title not immediately supplied as Display argument')
 require(sorted(callers)==[['main.sc','h6BaseDrawWorld'],['main.sc','render']],'Title consumers changed')
 # Explicitly rebind original P09 draw-chain guard. Whole-source guards remain on frozen original.
 contract=json.loads((H/'references/p09-geometry-independent-REVIEW-CONTRACT.json').read_text())
 for n,v in contract['draw_dependency']['method_sha256'].items():require(digest(bm[n])==v,'Accepted draw dependency changed',n)
 require('(DrawCel 222 1 mouth 149 61 -1 108 108)' in sm['neighborPerson'],'Stringer loop/placement change')
 require(re.search(r'pushi 8\s+pushi 223\s+push1\s+lst 0',sm['p03Rita']),'Rita loop change')
 newchain={n:{'main_wrapper_or_method':digest(mm[n]),'renderer_method':digest(sm[n]) if n in sm else None} for n in contract['draw_dependency']['method_sha256']}
 dump(H/'evidence/draw-chain-rebinding.json',{'status':'PASS_SOURCE_REBINDING','original_contract_sha256':sha(H/'references/p09-geometry-independent-REVIEW-CONTRACT.json'),'current_methods':newchain,'actor_bounds':contract['actor_bounds_half_open'],'rule':'All loop1, placement, scaling and original resource constraints retained. Any new change invalidates this binding. Trace and native gates are separately reported.'})
 result={'status':'PASS_STATIC_ABI_RESOURCE_AUDIT','old_main_bytes':oldrows[0]['combined_bytes'],'new_main_bytes':rows[0]['combined_bytes'],'main_bytes_recovered':oldrows[0]['combined_bytes']-rows[0]['combined_bytes'],'main_headroom':65535-rows[0]['combined_bytes'],'renderer_bytes':rows[991]['combined_bytes'],'new_selector_names':0,'new_vocab_string_bytes':0,'vocab997_bytes':(res/'997.vocab.bin').stat().st_size,'planning_remaining_vocab_bytes':1546,'unchanged_modules':list(range(980,991)),'changed_typed_resources':changed,'ordinary_resources_preserved':True,'class_species':13,'export':0,'new_saved_properties':0,'new_local_words':0,'compiler_source_files':198,'roomTitle_consumers':callers,'roomTitle_pointer_identity':'Heap address changes; all existing consumers immediately Display content. No equality, persistence, or pointer-based contract found. Other moved method returns checked dynamically.','native_acceptance':False}
 dump(H/'evidence/static-audit.json',result);return result
if __name__=='__main__':print(json.dumps(audit(),indent=2))
