#!/usr/bin/env python3
"""Fresh coherent P05 host proof universe; no historical/native compatibility."""
from pathlib import Path
import json,re,struct,hashlib,shutil,subprocess,sys
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'tools'))
(H/'VERIFICATION.json').write_text(json.dumps({'status':'BUILDING','native_acceptance':False})+'\n')
# Invalidate acceptance before any project-local import can fail.
_B=H/'build/coherent';_B.mkdir(parents=True,exist_ok=True)
(_B/'compile-receipt.json').write_text(json.dumps({'status':'BUILDING','native_acceptance':False})+'\n')
if sys.flags.optimize:
 (_B/'compile-receipt.json').write_text(json.dumps({'status':'FAILED','reason':'optimized Python forbidden'})+'\n')
 raise RuntimeError('Optimized Python is forbidden')
try:
 from validate_selected_inputs import check
 check(H)
except BaseException as e:
 (_B/'compile-receipt.json').write_text(json.dumps({'status':'FAILED','reason':str(e)})+'\n')
 raise
from source_tools import spans,tokens
from extract_sci11 import extract
import pack
P=H.parent/'p04-native-inventory-fix-reconstruction'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def declarations(source):
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
 assert not sys.flags.optimize
 B=H/'build/coherent';B.mkdir(exist_ok=True,parents=True);dump(B/'compile-receipt.json',dict(status='BUILDING'))
 numbers=[980,981,982,983,984,985]+([986] if (H/'src/module986.sc').exists() else [])+[0]
 # Reserve the completed Contest ABI even for intentionally unavailable host routes.
 selectors=json.loads((H/'snapshot/contest/selectors.json').read_text())
 old=dict(selectors);needed=set()
 for p in (H/'src').glob('*.sc'):
  s=p.read_text();needed.update(spans(s))
  for props in re.findall(r'\(properties\s+([^)]*)\)',s):
   a=[t.group() for t in tokens(props)];assert len(a)%2==0;needed.update(a[::2])
 n=max(v for v in selectors.values() if v<4096)+1
 for i,name in enumerate(sorted(needed-selectors.keys()),n):selectors[name]=i
 assert len(set(selectors.values()))==len(selectors)
 dump(H/'selectors.json',selectors);pack.SELECTORS=selectors
 resources={}
 # Immutable existing static resources, never import a compiled module.
 for p in (P/'staging-proof/verification-checkpoint/assets/resources').iterdir():
  bits=p.name.split('.');types={'vocab':6,'text':3,'font':7,'view':0,'palette':11,'sound':4,'patch':9,'pic':1}
  if len(bits)==3 and bits[1] in types:resources[types[bits[1]],int(bits[0])]=p.read_bytes()
 owners=[0,0,980,981,982,983,984,985]+([986] if 986 in numbers else [])
 resources[6,996]=struct.pack('<'+'H'*len(owners)*2,*sum(([0,n] for n in owners),[]));resources[6,997]=pack.selector_resource()
 resources[3,205]=(H/'snapshot/scene/205.text.bin').read_bytes()
 if (H/'CONTEST-INTEGRATION.json').exists():resources[3,230]=(H/'snapshot/contest-scene/230.text.bin').read_bytes()
 for n in [304,227]:
  choices=list((H.parent/'p05-art-reconstruction').glob(f'**/{n}.view.bin'));assert choices
  resources[0,n]=choices[0].read_bytes()
 if (H/'COURTYARD-INTEGRATION.json').exists():
  for n in [305,228]:resources[0,n]=(H/f'snapshot/courtyard/{n}.view.bin').read_bytes()
 if (H/'DRAWER-INTEGRATION.json').exists():resources[0,229]=(H/'snapshot/drawer/229.view.bin').read_bytes()
 if (H/'STAGE-INTEGRATION.json').exists():
  for n in [330,331]:resources[0,n]=(H/f'snapshot/stage/{n}.view.bin').read_bytes()
 for n in [240,241,242]:
  assert (3,n) not in resources,('resource collision',n)
  resources[3,n]=(H/f'generated/static/{n}.text.bin').read_bytes()
 pack.pack_resources(resources,B)
 (B/'game.ini').write_text('[Game]\nName=P05 host guarded reconstruction\nLanguage=sci\n[Script]\nn000=main\n'+''.join(f'n{n}=module{n}\n' for n in numbers if n))
 (B/'src').mkdir(exist_ok=True);(B/'compiled').mkdir(exist_ok=True)
 for p in (B/'src').glob('*'):p.unlink()
 for p in (H/'src').glob('*.sc'):shutil.copy2(p,B/'src'/p.name)
 selector_list=[dict(name=n,selector_id=i) for n,i in sorted(selectors.items(),key=lambda a:a[1])];dump(B/'selector-list.json',selector_list)
 abi={'selectors':selector_list,'modules':{}};rows=[]
 compiler=H.parent/'p03-editable-checkpoint/toolchain/scicompile';assert sha(compiler)=='608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e'
 baseline=json.loads((P/'staging-proof/verification-checkpoint/source-provenance/ABI-MAPPINGS.json').read_text())
 for n in numbers:
  src=B/'src'/('main.sc' if n==0 else f'module{n}.sc');out=B/f'compiled/{n}.scr.bin'
  out.unlink(missing_ok=True);Path(str(out)+'.hep').unlink(missing_ok=True)
  r=subprocess.run([str(compiler),'--version','sci11',str(B),str(src),str(out)],capture_output=True,text=True)
  log=r.stdout+r.stderr;(B/f'compile-{n}.log').write_text(log);assert not r.returncode and '[error]' not in log,log
  layout=extract(out,str(out)+'.hep',B/'selector-list.json');decls=declarations(src.read_text());assert sum(a['word_count'] for a in decls)==layout['locals_word_count'],(n,decls,layout['locals_word_count'])
  for a in decls:a['initial_words']=layout['locals'][a['word_offset']:a['word_offset']+a['word_count']]
  classes=[{'name':o['name'],'properties':o['properties'],'methods':o['methods']} for o in layout['objects'] if o['is_class']]
  if str(n) in baseline['modules']:
   prev=baseline['modules'][str(n)]
   if n!=982:assert [{k:a[k] for k in ('name','word_offset','word_count')} for a in decls[:len(prev['locals'])]]==[{k:a[k] for k in ('name','word_offset','word_count')} for a in prev['locals']],('old local ABI',n)
   for c in prev['classes']:
    now=next(a for a in classes if a['name']==c['name']);assert [p['selector_id'] for p in now['properties'][:len(c['properties'])]]==[p['selector_id'] for p in c['properties']],('property ABI',n)
  abi['modules'][str(n)]=dict(source='src/'+src.name,sha256=sha(src),local_words=layout['locals_word_count'],locals=decls,classes=classes,reference_layout=layout)
  size=out.stat().st_size+Path(str(out)+'.hep').stat().st_size+(2 if out.stat().st_size&2 else 0);assert size<=65535,(n,size)
  rows.append(dict(module=n,source_sha256=sha(src),script_sha256=sha(out),heap_sha256=sha(str(out)+'.hep'),combined_bytes=size,class_species=[c['species'] for c in layout['objects'] if c['is_class']]))
 C=B/'verification-checkpoint';(C/'assets/resources').mkdir(exist_ok=True,parents=True);inventory=[]
 suffix={0:'view',1:'pic',3:'text',4:'sound',6:'vocab',7:'font',9:'patch',11:'palette'}
 for (t,n),data in resources.items():
  name=f'{n:03}.{suffix[t]}.bin';(C/'assets/resources'/name).write_bytes(data);inventory.append(dict(type=t,number=n,extracted_path=name,size=len(data),sha256=hashlib.sha256(data).hexdigest()))
 dump(C/'reference/resources.json',inventory);dump(C/'source-provenance/ABI-MAPPINGS.json',abi);dump(B/'ABI-MAPPINGS.json',abi)
 dump(B/'compile-receipt.json',dict(status='PASS_FRESH_COMPILE',modules=rows,class_owners=owners,native_acceptance=False,runtime_package=False,compiler_sha256=sha(compiler),preserved_selectors=len(old),added_selectors=len(selectors)-len(old)))
 print([(a['module'],a['combined_bytes']) for a in rows])
if __name__=='__main__':build()
