#!/usr/bin/env python3
"""Fresh, isolated seven-module emitted visual fixture. Existing files are read-only.
Main's only fixture additions are p05Visual pointer and p05FocusMark center wrapper.
This fixture does not wire game actions or claim playable/native acceptance.
"""
from pathlib import Path
import sys,json,struct,hashlib,subprocess,shutil,re
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;ROOT=H.parents[1];BASE=ROOT/'p04-native-inventory-fix-reconstruction';B=H/'build'
sys.path.insert(0,str(H.parent/'tools'));from source_tools import spans,tokens
from extract_sci11 import extract
import pack
FOCUS='''(method (p05FocusMark &tmp i)
    (= i uiFocus)
    (if (or (< i 0) (>= i uiControlCount)) (return 0))
    (if (or (!= [uiActions i] 1) (!= [uiPayloads i] 69)) (return 0))
    (return (p05Visual hMarkAt: (/ (+ [uiLefts i] [uiRights i]) 2)
        (/ (+ [uiTops i] [uiBottoms i]) 2))))'''
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def append_prop(src,classname,raw):
 start=spans(src,'class')[classname][0];p=src.index('(properties',start);end=src.index(')',p);return src[:end]+'\n'+raw+'\n'+src[end:]
def append_methods(src,classname,raw):
 end=spans(src,'class')[classname][1]-1;return src[:end]+'\n'+raw+'\n'+src[end:]
def declarations(src):
 ts=tokens(src);i=next((i for i,t in enumerate(ts) if t.group()=='(' and ts[i+1].group()=='local'),None);level=0
 if i is None:return []
 for q in ts[i:]:
  level+=(q.group()=='(')-(q.group()==')')
  if not level:end=q.start();break
 raw=src[ts[i+1].end():end];a=[];offset=0
 for m in re.finditer(r'\[(\w+)\s+(\d+)\](?:\s*=\s*\[([^]]*)\])?',raw):
  size=int(m[2]);a.append({'name':m[1],'word_offset':offset,'word_count':size,'byte_offset':offset*2});offset+=size
 return a

def build():
 B.mkdir(exist_ok=True);(B/'src').mkdir(exist_ok=True);(B/'compiled').mkdir(exist_ok=True)
 dump(B/'compile-receipt.json',{'status':'BUILDING'})
 inputs=[BASE/'staging-proof/src'/n for n in ['main.sc','module980.sc','module981.sc','module982.sc','module983.sc','module984.sc']]
 pins={str(p.relative_to(ROOT)):sha(p) for p in inputs}
 for p in inputs:shutil.copy2(p,B/'src'/p.name)
 meta=json.loads((H/'interfaces.json').read_text());domain=ROOT/'p05-domain-reconstruction/src/module985.sc';pins[str(domain.relative_to(ROOT))]=sha(domain)
 s=domain.read_text();i=s.index(')',s.index('(local'));s=s[:i]+' '+(H/'visual-locals.inc').read_text().strip()+s[i:]
 s=append_prop(s,'P05State','\n'.join(f'{k} {v}' for k,v in meta['required_properties'].items()))
 s=append_methods(s,'P05State',(H/'visual-methods.sc.inc').read_text());(B/'src/module985.sc').write_text(s)
 main=(B/'src/main.sc').read_text();main=append_prop(main,'Game','p05Visual 0');main=append_methods(main,'Game',FOCUS);(B/'src/main.sc').write_text(main)
 selectors=json.loads((ROOT/'contest-domain-reconstruction/selectors.json').read_text());old=dict(selectors);need=set()
 for p in (B/'src').glob('*.sc'):
  src=p.read_text();need.update(spans(src))
  for pr in re.findall(r'\(properties\s+([^)]*)\)',src):
   a=[x.group() for x in tokens(pr)];assert len(a)%2==0;need.update(a[::2])
 nxt=max(v for v in selectors.values() if v<4096)+1
 for i,n in enumerate(sorted(need-selectors.keys()),nxt):selectors[n]=i
 assert all(selectors[k]==v for k,v in old.items());pack.SELECTORS=selectors
 res={};types={'vocab':6,'text':3,'font':7,'view':0,'palette':11,'sound':4,'patch':9,'pic':1}
 for p in (BASE/'inputs/base-resources').iterdir():
  a=p.name.split('.')
  if len(a)==3 and a[1] in types:res[types[a[1]],int(a[0])]=p.read_bytes()
 owners=[0,0,980,981,982,983,984,985];res[6,996]=struct.pack('<16H',*sum(([0,n] for n in owners),[]));res[6,997]=pack.selector_resource()
 res[3,205]=(ROOT/'p05-scene-reconstruction/generated/205.text.bin').read_bytes()
 for n in [304,227]:res[0,n]=(ROOT/f'p05-art-reconstruction/resources/{n}.view.bin').read_bytes()
 pack.pack_resources(res,B)
 (B/'game.ini').write_text('[Game]\nLanguage=sci\n[Script]\nn000=main\n'+''.join(f'n{n}=module{n}\n' for n in range(980,986)))
 sl=[{'name':n,'selector_id':i} for n,i in sorted(selectors.items(),key=lambda z:z[1])];dump(B/'selector-list.json',sl)
 abi={'selectors':sl,'modules':{}};rows=[];compiler=ROOT/'p03-editable-checkpoint/toolchain/scicompile'
 assert sha(compiler)=='608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e'
 for n in [980,981,982,983,984,985,0]:
  src=B/'src'/('main.sc' if n==0 else f'module{n}.sc');out=B/f'compiled/{n}.scr.bin'
  p=subprocess.run([str(compiler),'--version','sci11',str(B),str(src),str(out)],capture_output=True,text=True);log=p.stdout+p.stderr;(B/f'compile-{n}.log').write_text(log)
  assert p.returncode==0 and '[error]' not in log,log
  layout=extract(out,str(out)+'.hep',B/'selector-list.json');a=declarations(src.read_text());assert sum(x['word_count'] for x in a)==layout['locals_word_count']
  abi['modules'][str(n)]={'source':'src/'+src.name,'locals':a,'reference_layout':layout};dump(B/f'layout-{n}.json',layout)
  rows.append({'module':n,'source_sha256':sha(src),'script_sha256':sha(out),'heap_sha256':sha(str(out)+'.hep'),'combined_bytes':out.stat().st_size+Path(str(out)+'.hep').stat().st_size,'class_species':[x['species'] for x in layout['objects'] if x['is_class']]})
 C=B/'verification-checkpoint';inv=[]
 for (t,n),data in res.items():
  if t not in [0,3,7]:continue
  p=C/'assets/resources'/f'{t}-{n}.bin';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);inv.append({'type':t,'number':n,'extracted_path':p.name,'sha256':sha(p)})
 dump(C/'reference/resources.json',inv);dump(C/'source-provenance/ABI-MAPPINGS.json',abi)
 assert all(sha(ROOT/p)==v for p,v in pins.items())
 dump(H/'evidence/input-pins.json',pins);dump(B/'compile-receipt.json',{'status':'PASS_FRESH_COMPILE','modules':rows,'scope':'Isolated emitted helper fixture; no action integration or native proof','native_acceptance':False})
 print([(r['module'],r['combined_bytes']) for r in rows])
if __name__=='__main__':build()
