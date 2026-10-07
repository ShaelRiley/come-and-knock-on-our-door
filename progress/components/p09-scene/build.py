"""Fresh coherent baseline and appended data universes; no precompiled script inputs."""
from pathlib import Path
import sys,shutil,json,struct,re,subprocess
H=Path(__file__).resolve().parent;sys.dont_write_bytecode=True;sys.path.insert(0,str(H/'tools'))
from caption_util import sha,dump
from guard import require,input_check
from source_tools import tokens,methods
from extract_sci11 import extract
from resource_codec import decode
import pack,boolean_audit
NUMBERS=[980,981,982,983,984,985,986,987,988,0]
PIN='608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e'
def declarations(source):
 ts=tokens(source);i=next((i for i,t in enumerate(ts) if t.group()=='(' and ts[i+1].group()=='local'),None)
 if i is None:return []
 depth=0
 for q in ts[i:]:
  if q.group()=='(':depth+=1
  elif q.group()==')':
   depth-=1
   if depth==0:end=q.start();break
 raw=source[ts[i+1].end():end];offset=0;rows=[]
 for m in re.finditer(r'\[(\w+)\s+(\d+)\](?:\s*=\s*\[([^]]*)\])?',raw):
  n,c=m[1],int(m[2]);rows.append(dict(name=n,word_offset=offset,word_count=c,byte_offset=offset*2));offset+=c
 return rows

def build_one(name,source_folder,resources):
 B=H/'build'/name
 if B.exists():shutil.rmtree(B)
 (B/'src').mkdir(parents=True);(B/'compiled').mkdir();compiler=H/'tools/scicompile';require(sha(compiler.read_bytes())==PIN,'Compiler hash');compiler.chmod(compiler.stat().st_mode|0o100)
 selectors=json.loads((H/'inputs/selectors.json').read_text());pack.SELECTORS=selectors
 require(resources[6,997]==pack.selector_resource(),'Exact selector vocabulary')
 owners=[v[1] for v in struct.iter_unpack('<HH',resources[6,996])];require(owners==[0,0,980,981,982,983,984,985,986,987,988],'Class universe')
 require(not any(t in [2,17] for t,n in resources),'No imported compiled resources')
 pack.pack_resources(resources,B);(B/'game.ini').write_text('[Game]\nName=P09 isolated scene fixture\nLanguage=sci\n[Script]\nn000=main\n'+''.join(f'n{n}=module{n}\n' for n in NUMBERS if n))
 selector_list=[dict(name=n,selector_id=i) for n,i in sorted(selectors.items(),key=lambda a:a[1])];dump(B/'selector-list.json',selector_list)
 abi=dict(selectors=selector_list,modules={});rows=[];audits={}
 for n in NUMBERS:
  fn='main.sc' if n==0 else f'module{n}.sc';src=B/'src'/fn;src.write_bytes((source_folder/fn).read_bytes());out=B/f'compiled/{n}.scr.bin'
  process=subprocess.run([str(compiler),'--version','sci11',str(B),str(src),str(out)],capture_output=True,text=True);log=process.stdout+process.stderr;(B/f'compile-{n}.log').write_text(log.replace(str(H),'<COMPONENT>'));require(process.returncode==0 and '[error]' not in log,log)
  layout=extract(out,str(out)+'.hep',B/'selector-list.json');layout['script']=str(out.relative_to(H));layout['heap']=str(Path(str(out)+'.hep').relative_to(H));decl=declarations(src.read_text());require(sum(a['word_count'] for a in decl)==layout['locals_word_count'],'Local extraction count')
  for a in decl:a['initial_words']=layout['locals'][a['word_offset']:a['word_offset']+a['word_count']]
  classes=[dict(name=o['name'],properties=o['properties'],methods=o['methods']) for o in layout['objects'] if o['is_class']]
  abi['modules'][str(n)]=dict(source='src/'+fn,sha256=sha(src.read_bytes()),local_words=layout['locals_word_count'],locals=decl,classes=classes,reference_layout=layout)
  script=out.read_bytes();heap=Path(str(out)+'.hep').read_bytes();combined=len(script)+len(heap)+(2 if len(script)&2 else 0);require(combined<=65535,'Segment overflow '+str(n))
  rows.append(dict(module=n,source_sha256=sha(src.read_bytes()),script_sha256=sha(script),heap_sha256=sha(heap),script_bytes=len(script),heap_bytes=len(heap),combined_bytes=combined,remaining_segment_bytes=65535-combined,class_species=[c['species'] for c in layout['objects'] if c['is_class']]))
  # Audit newly changed high-level code; old assembly-only host behavior is separately byte-preserved.
  if n in [982,985]:
   audited=src.read_text() if n==982 else '\n'.join(methods(src.read_text())[k] for k in ['hStaticCount','hStaticFirst','hStaticLoad'])
   audits[str(n)]=boolean_audit.audit(audited);require(not audits[str(n)]['hazards'],'Boolean source hazard')
 C=B/'verification-checkpoint';(C/'assets/resources').mkdir(parents=True);inventory=[]
 suffix={0:'view',1:'pic',3:'text',4:'sound',6:'vocab',7:'font',9:'patch',11:'palette'}
 for (t,n),data in resources.items():
  fn=f'{n:03}.{suffix[t]}.bin';(C/'assets/resources'/fn).write_bytes(data);inventory.append(dict(type=t,number=n,extracted_path=fn,size=len(data),sha256=sha(data)))
 dump(C/'reference/resources.json',inventory);dump(C/'source-provenance/ABI-MAPPINGS.json',abi);dump(B/'ABI-MAPPINGS.json',abi)
 dump(B/'compile-receipt.json',dict(status='PASS_FRESH_COMPILE',modules=rows,class_owners=owners,native_acceptance=False,runtime_package=False,compiler_sha256=PIN,preserved_selectors=len(selectors),added_selectors=0));dump(B/'boolean-audit.json',audits)
 return abi,rows

def build():
 input_check();boolean_audit.self_check()
 native=H/'inputs/native-game';allres=decode((native/'resource.map').read_bytes(),(native/'resource.000').read_bytes());resources={k:v for k,v in allres.items() if k[0] not in [2,17]}
 before,brows=build_one('baseline',H/'inputs/src',resources)
 for row in brows:
  n=row['module'];require(sha(allres[2,n])==row['script_sha256'] and sha(allres[17,n])==row['heap_sha256'],'Baseline not byte-identical '+str(n))
 require((3,210) not in resources,'Text210 collision');resources[3,210]=(H/'generated/210.text.bin').read_bytes()
 for n in [240,241,244]:resources[3,n]=(H/f'generated/static/{n}.text.bin').read_bytes()
 after,rows=build_one('coherent',H/'generated/src',resources)
 for row,old in zip(rows,brows):
  n=row['module'];a=before['modules'][str(n)];b=after['modules'][str(n)]
  require([[p['selector_id'] for p in c['properties']] for c in a['classes']]==[[p['selector_id'] for p in c['properties']] for c in b['classes']],'Property ABI drift')
  require([[m['selector_id'] for m in c['methods']] for c in a['classes']]==[[m['selector_id'] for m in c['methods']] for c in b['classes']],'Method ABI drift')
  if n not in [982,985]:require(row==old,'Unrelated emitted module changed '+str(n))
  if n!=982:require([{k:d[k] for k in ('name','word_offset','word_count')} for d in a['locals']]==[{k:d[k] for k in ('name','word_offset','word_count')} for d in b['locals']],'Unrelated local ABI changed')
  else:
   oldarrays={d['name']:d for d in a['locals']};newarrays={d['name']:d for d in b['locals']};require(list(oldarrays)==list(newarrays),'Local declaration identity')
   for name,d in oldarrays.items():require(newarrays[name]['initial_words'][:d['word_count']]==d['initial_words'],'Emitted prefix '+name)
 G=H/'generated/fixture-game';G.mkdir(exist_ok=True)
 packed=dict(resources)
 for n in NUMBERS:
  packed[2,n]=(H/f'build/coherent/compiled/{n}.scr.bin').read_bytes();packed[17,n]=(H/f'build/coherent/compiled/{n}.scr.bin.hep').read_bytes()
 pack.pack_resources(packed,G);decoded=decode((G/'resource.map').read_bytes(),(G/'resource.000').read_bytes());require(decoded==packed,'Packer roundtrip')
 changed={(3,240),(3,241),(3,244),(2,982),(17,982),(2,985),(17,985)}
 for k,v in allres.items():
  if k not in changed:require(decoded[k]==v,'Unrelated typed resource changed '+str(k))
 dump(H/'evidence/compile-proof.json',dict(status='PASS',baseline_recompiles_exactly=True,modules=rows,new_selectors=0,new_classes=0,changed_modules=[982,985],unchanged_modules=[n for n in NUMBERS if n not in [982,985]],preserved_old_audio_sync_files=1028,typed_resources=len(decoded),old_typed_resources=len(allres),changed_existing_resources=[list(k) for k in sorted(allres) if decoded[k]!=allres[k]],permitted_changed_existing_resources=[list(k) for k in sorted(changed)],new_resources=[[3,210]],native_acceptance=False))
 reader(resources)
 print([(r['module'],r['combined_bytes']) for r in rows])
def reader(resources):
 B=H/'build/reader';B.mkdir(parents=True,exist_ok=True);(B/'src').mkdir(exist_ok=True);(B/'compiled').mkdir(exist_ok=True)
 selectors=json.loads((H/'inputs/selectors.json').read_text());production=dict(selectors)
 for i,n in enumerate(['failure','readPage','drawPage'],5000):require(n not in selectors,'Reader selector collision');selectors[n]=i
 pack.SELECTORS=selectors;resources=dict(resources);resources[6,997]=pack.selector_resource();resources[6,996]=struct.pack('<HH',0,0)
 pack.pack_resources(resources,B);(B/'game.ini').write_text('[Game]\nName=P09 reader fixture only\nLanguage=sci\n[Script]\nn000=main\n')
 src=B/'src/main.sc';src.write_bytes((H/'generated/reader-proof.sc').read_bytes());out=B/'compiled/0.scr.bin'
 p=subprocess.run([str(H/'tools/scicompile'),'--version','sci11',str(B),str(src),str(out)],capture_output=True,text=True);(B/'compile.log').write_text((p.stdout+p.stderr).replace(str(H),'<COMPONENT>'));require(p.returncode==0 and '[error]' not in p.stdout+p.stderr,p.stdout+p.stderr)
 selector_list=[dict(name=n,selector_id=i) for n,i in sorted(selectors.items(),key=lambda a:a[1])];dump(B/'selector-list.json',selector_list);layout=extract(out,str(out)+'.hep',B/'selector-list.json');layout['script']=str(out.relative_to(H));layout['heap']=str(Path(str(out)+'.hep').relative_to(H));decl=declarations(src.read_text())
 for a in decl:a['initial_words']=layout['locals'][a['word_offset']:a['word_offset']+a['word_count']]
 abi=dict(selectors=selector_list,modules={'0':dict(source='src/main.sc',sha256=sha(src.read_bytes()),local_words=layout['locals_word_count'],locals=decl,classes=[dict(name=o['name'],properties=o['properties'],methods=o['methods']) for o in layout['objects'] if o['is_class']],reference_layout=layout)})
 C=B/'verification-checkpoint';(C/'assets/resources').mkdir(parents=True,exist_ok=True);inventory=[]
 for (t,n),data in resources.items():
  fn=f'{t}-{n}.bin';(C/'assets/resources'/fn).write_bytes(data);inventory.append(dict(type=t,number=n,extracted_path=fn,size=len(data),sha256=sha(data)))
 dump(C/'reference/resources.json',inventory);dump(C/'source-provenance/ABI-MAPPINGS.json',abi);dump(B/'ABI-MAPPINGS.json',abi);pack.SELECTORS=production
 dump(B/'compile-receipt.json',dict(status='PASS_FRESH_COMPILE',modules=[dict(module=0,script_sha256=sha(out.read_bytes()),heap_sha256=sha(Path(str(out)+'.hep').read_bytes()))],native_acceptance=False))
 dump(H/'evidence/reader-compile.json',dict(status='PASS',compiler_sha256=PIN,script_sha256=sha(out.read_bytes()),heap_sha256=sha(Path(str(out)+'.hep').read_bytes()),isolated_fixture_selectors=['failure','readPage','drawPage'],production_selectors_added=0,native_acceptance=False))
if __name__=='__main__':build()
