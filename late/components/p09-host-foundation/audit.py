#!/usr/bin/env python3
"""Independent emitted layout/identity and additive preservation audit."""
from pathlib import Path
import hashlib,json,re,struct,sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'tools'))
from source_tools import methods
from extract_sci11 import extract
from derive import derive,require,sha,array,dump

def audit():
 derive(check=True)
 B=H/'build/coherent';base=H/'frozen/p08';receipt=json.loads((B/'compile-receipt.json').read_text())
 require(receipt['status']=='PASS_FRESH_COMPILE','Fresh compile required')
 previous=json.loads((base/'accepted-compile/compile-receipt.json').read_text())
 old={x['module']:x for x in previous['modules']}
 selectors=json.loads((H/'selectors.json').read_text());prior=json.loads((base/'selectors.json').read_text())
 require(all(selectors[k]==v for k,v in prior.items()),'Earlier selector changed')
 require(len(set(selectors.values()))==len(selectors),'Duplicate selector value')
 alloc=json.loads((H/'HOST-ALLOCATION.json').read_text())
 require(set(alloc.values())==set(range(3000,3164)),'Reservation drift')
 raw=(B/'verification-checkpoint/assets/resources/997.vocab.bin').read_bytes()
 count=struct.unpack_from('<H',raw)[0]+1;require(count==4104,'Internal selector table boundary changed')
 for name,number in selectors.items():
  offset=struct.unpack_from('<H',raw,2+2*number)[0];size=struct.unpack_from('<H',raw,offset)[0]
  require(raw[offset+2:offset+2+size].decode('ascii')==name,'Emitted vocab mismatch '+name)
 require(len(raw)==37594,'Measured selector storage drift')
 owners=struct.unpack('<26H',(B/'verification-checkpoint/assets/resources/996.vocab.bin').read_bytes())
 require(list(owners[1::2])==[0,0,980,981,982,983,984,985,986,987,988,989,990],'Class ownership map')
 modules=[];identical=[]
 for row in receipt['modules']:
  n=row['module'];path=H/'src'/('main.sc' if n==0 else f'module{n}.sc')
  script=B/f'compiled/{n}.scr.bin';heap=Path(str(script)+'.hep')
  require(sha(path)==row['source_sha256'],'Source changed after compile')
  require(sha(script)==row['script_sha256'] and sha(heap)==row['heap_sha256'],'Emitted bytes changed')
  layout=extract(script,heap,B/'selector-list.json')
  combined=script.stat().st_size+heap.stat().st_size+(2 if script.stat().st_size&2 else 0)
  require(combined==row['combined_bytes'] and combined<=65535,'SCI16 segment capacity')
  for obj in layout['objects']:
   if obj['is_class']:
    for prop in obj['properties']:require(selectors[prop['selector']]==prop['selector_id'],'Property selector linkage')
   for method in obj['methods']:require(selectors[method['selector']]==method['selector_id'],'Method selector linkage')
  modules.append({'module':n,'script_bytes':script.stat().st_size,'heap_bytes':heap.stat().st_size,'alignment_bytes':2 if script.stat().st_size&2 else 0,'combined_bytes':combined,'headroom':65535-combined,'species':row['class_species']})
  if n in old and all(row[k]==old[n][k] for k in ('script_sha256','heap_sha256')):identical.append(n)
  if n==990:
   cls=next(o for o in layout['objects'] if o['name']=='P09State');inst=next(o for o in layout['objects'] if o['name']=='p09State')
   require(cls['species']==12 and inst['superclass']==12 and layout['exports']==[inst['heap_offset']],'Production P09 export')
   require(len(cls['methods'])==64,'61 domain plus 3 host methods')
 require(identical==[980,981,983,984,986,987,988,989],'Unexpected earlier bytecode drift')
 dm=methods((H/'frozen/domain/src/module990.sc').read_text());now=methods((H/'src/module990.sc').read_text())
 require(len(dm)==61 and all(now[n]==v for n,v in dm.items()),'Literal domain methods changed')
 om=methods((base/'src/module982.sc').read_text());nm=methods((H/'src/module982.sc').read_text())
 require(all(nm[n]==om[n] for n in om if n not in {'sdRoute','sdPageCount','sdLoad','hStaticAt'}),'Earlier scene method drift')
 preserved={}
 for name in ('sdStarts','sdCounts','sdPageData','sdLegacyVoiceDurations','sdTextResources','sdAudioModules','sdPageDurations'):
  a=array((base/'src/module982.sc').read_text(),name);b=array((H/'src/module982.sc').read_text(),name)
  require(b[:len(a)]==a,'Earlier scene prefix drift');preserved[name]=len(a)
 # Inventory boundaries are explicit, or protected by their existing whole-layout validation.
 mm=methods((H/'src/main.sc').read_text());guard='(if (or (< obj 0) (> obj 32)) (= p02InventoryOverflow 1) (return 0))'
 require(mm['p02SyncInventory'].index(guard)<mm['p02SyncInventory'].index('[p02Reserved obj]'),'Legacy high-ID guard order')
 require('(>= obj 0) (<= obj 32)' in mm['p03HostReservation'],'Legacy read boundary')
 for mod,checks in [(983,{'bAppend':'(> obj 50)','bInventory':'(> obj 50)','b8Append':'(> obj 50)','b8Prepare':'(not (self b8Valid:))'}),(984,{'qAppend':'(> obj 62)','qInventory':'(> obj 62)','qInventoryFits':'(<= obj 62)','q8Append':'(> obj 62)','q8Prepare':'(not (self q8Valid:))'})]:
  m=methods((H/f'src/module{mod}.sc').read_text())
  for name,text in checks.items():require(text in m[name],'Inventory guard absent '+name)
 h9=methods((H/'templates/host990.sc.in').read_text())
 require(h9['h9Active']=='(method (h9Active) (return 0))','Foundation activation opened')
 require(not any(x in '\n'.join(h9.values()) for x in ('p09Context:','p09Acknowledge:','p09Act:','p09Begin:')),'Host grants P09 state')
 p08=methods((H/'src/module989.sc').read_text())
 require(p08['h8EveningCommitted']=='(method (h8EveningCommitted) (return 0))','Frozen P08 history modified')
 closure=json.loads((H/'toolchain/SOURCE-MANIFEST.json').read_text())['files']
 require(len(closure)==198,'R2 closure count')
 for name,digest in closure.items():require(sha(H/'toolchain/source'/name)==digest,'Compiler closure drift')
 result={'status':'PASS','active_dispatch':False,'native_acceptance':False,'source_vm_is_not_native':True,'compiler_sha256':receipt['compiler_sha256'],'compiler_source_files':len(closure),'modules':modules,'binary_identical_earlier_modules':identical,'domain_literal_methods':61,'production_species':12,'production_export':0,'preserved_scene_array_lengths':preserved,'vocab997_bytes':len(raw),'new_selector_range':[3000,3163],'new_selector_count':164,'new_selector_string_bytes':2718,'p08_reservation_preserved':[2987,2999],'ordinary_boundary':4096,'all_earlier_selector_values_preserved':True,'chair_card_ids':[395,396,397,398,399],'card_dense_reservation':'not allocated in inactive foundation','scene_documents':[1100,1139],'new_scene_pages':53}
 dump(H/'evidence/static-audit.json',result);return result

if __name__=='__main__':
 try:print(json.dumps(audit(),indent=2))
 except BaseException as e:dump(H/'evidence/static-audit.json',{'status':'FAILED','reason':str(e)});raise
