#!/usr/bin/env python3
"""Compile one complete source, class and selector universe. Never splice binaries."""
from pathlib import Path
import json,hashlib,struct,shutil,subprocess,sys,re
H=Path(__file__).resolve().parent;R=H.parent;B=H/'build/coherent';B.mkdir(parents=True,exist_ok=True)
# Retire receipts before imports or any input that may fail.
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
dump(B/'compile-receipt.json',{'status':'BUILDING','native_acceptance':False})
dump(H/'VERIFICATION.json',{'status':'BUILDING','native_acceptance':False})
sys.dont_write_bytecode=True
sys.path.insert(0,str(H/'tools'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def declarations(source):
 from source_tools import tokens
 ts=tokens(source);i=next((i for i,t in enumerate(ts) if t.group()=='(' and ts[i+1].group()=='local'),None)
 if i is None:return []
 depth=0
 for q in ts[i:]:
  if q.group()=='(':depth+=1
  elif q.group()==')':
   depth-=1
   if not depth:end=q.start();break
 raw=source[ts[i+1].end():end];offset=0;rows=[]
 for m in re.finditer(r'\[(\w+)\s+(\d+)\](?:\s*=\s*\[([^]]*)\])?',raw):
  n,c=m[1],int(m[2]);rows.append(dict(name=n,word_offset=offset,word_count=c,byte_offset=offset*2));offset+=c
 return rows

def build():
 if sys.flags.optimize:raise RuntimeError('Optimized Python forbidden')
 from extract_sci11 import extract
 from source_tools import methods
 import pack
 from derive import derive
 derive()
 selectors=json.loads((H/'selectors.json').read_text());pack.SELECTORS=selectors
 resources={}
 suffixes={'view':0,'pic':1,'text':3,'sound':4,'vocab':6,'font':7,'patch':9,'palette':11}
 for p in (H/'snapshot/resources').iterdir():
  parts=p.name.split('.')
  if len(parts)!=3 or parts[1] not in suffixes:raise RuntimeError('Unexpected resource input '+str(p))
  resources[suffixes[parts[1]],int(parts[0])]=p.read_bytes()
 owners=[0,0,980,981,982,983,984,985,986,987,988]
 resources[6,996]=struct.pack('<'+'H'*len(owners)*2,*sum(([0,n] for n in owners),[]));resources[6,997]=pack.selector_resource()
 pack.pack_resources(resources,B)
 numbers=[980,981,982,983,984,985,986]+([987] if (H/'src/module987.sc').exists() else [])+[988,0]
 (B/'game.ini').write_text('[Game]\nName=P07 host reconstruction\nLanguage=sci\n[Script]\nn000=main\n'+''.join(f'n{n}=module{n}\n' for n in numbers if n))
 (B/'src').mkdir(exist_ok=True);(B/'compiled').mkdir(exist_ok=True)
 for p in (H/'src').glob('*.sc'):shutil.copy2(p,B/'src'/p.name)
 sl=[dict(name=n,selector_id=i) for n,i in sorted(selectors.items(),key=lambda x:x[1])];dump(B/'selector-list.json',sl)
 abi={'selectors':sl,'modules':{}};rows=[]
 compiler=H/'toolchain/scicompile'
 if sha(compiler)!='608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e':raise RuntimeError('compiler identity')
 prev=json.loads((H/'snapshot/base/ABI-MAPPINGS.json').read_text())
 for n in numbers:
  src=B/'src'/('main.sc' if n==0 else f'module{n}.sc');out=B/f'compiled/{n}.scr.bin';hep=Path(str(out)+'.hep')
  out.unlink(missing_ok=True);hep.unlink(missing_ok=True)
  p=subprocess.run([str(compiler),'--version','sci11',str(B),str(src),str(out)],capture_output=True,text=True)
  log=p.stdout+p.stderr;(B/f'compile-{n}.log').write_text(log)
  if p.returncode or '[error]' in log:raise RuntimeError(log)
  layout=extract(out,hep,B/'selector-list.json');decls=declarations(src.read_text())
  if sum(a['word_count'] for a in decls)!=layout['locals_word_count']:raise RuntimeError(('locals',n))
  for a in decls:a['initial_words']=layout['locals'][a['word_offset']:a['word_offset']+a['word_count']]
  classes=[{'name':o['name'],'properties':o['properties'],'methods':o['methods']} for o in layout['objects'] if o['is_class']]
  if str(n) in prev['modules']:
   prior=prev['modules'][str(n)]
   if n!=982 and [{k:a[k] for k in ('name','word_offset','word_count')} for a in decls[:len(prior['locals'])]]!=[{k:a[k] for k in ('name','word_offset','word_count')} for a in prior['locals']]:raise RuntimeError(('old locals changed',n))
   for c in prior['classes']:
    now=next(x for x in classes if x['name']==c['name'])
    if [p['selector_id'] for p in now['properties'][:len(c['properties'])]]!=[p['selector_id'] for p in c['properties']]:raise RuntimeError(('old props changed',n))
  abi['modules'][str(n)]=dict(source='src/'+src.name,sha256=sha(src),local_words=layout['locals_word_count'],locals=decls,classes=classes,reference_layout=layout)
  size=out.stat().st_size+hep.stat().st_size+(2 if out.stat().st_size&2 else 0)
  if size>65535:raise RuntimeError(('SCI16 resource budget',n,size))
  rows.append(dict(module=n,source_sha256=sha(src),script_sha256=sha(out),heap_sha256=sha(hep),combined_bytes=size,class_species=[c['species'] for c in layout['objects'] if c['is_class']]))
 C=B/'verification-checkpoint';(C/'assets/resources').mkdir(parents=True,exist_ok=True);inventory=[]
 suffix={0:'view',1:'pic',3:'text',4:'sound',6:'vocab',7:'font',9:'patch',11:'palette'}
 for (t,n),data in resources.items():
  name=f'{n:03}.{suffix[t]}.bin';(C/'assets/resources'/name).write_bytes(data);inventory.append(dict(type=t,number=n,extracted_path=name,size=len(data),sha256=hashlib.sha256(data).hexdigest()))
 dump(C/'reference/resources.json',inventory);dump(C/'source-provenance/ABI-MAPPINGS.json',abi);dump(B/'ABI-MAPPINGS.json',abi)
 dump(B/'compile-receipt.json',dict(status='PASS_FRESH_COMPILE',modules=rows,class_owners=owners,native_acceptance=False,runtime_package=False,compiler_sha256=sha(compiler)))
 print('PASS_FRESH_COMPILE',[(r['module'],r['combined_bytes']) for r in rows])
if __name__=='__main__':
 try:build()
 except BaseException as e:
  dump(B/'compile-receipt.json',{'status':'FAILED','reason':str(e),'native_acceptance':False});raise
