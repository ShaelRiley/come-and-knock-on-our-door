#!/usr/bin/env python3
"""Build the composed presentation program from explicit, pinned source inputs."""
from pathlib import Path
import json,hashlib,struct,shutil,subprocess,sys,re
H=Path(__file__).resolve().parent;D=H;B=H/'build/coherent';B.mkdir(parents=True,exist_ok=True)
# Retire receipts before imports or any input that may fail.
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
dump(B/'compile-receipt.json',{'status':'BUILDING','native_acceptance':False})
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
 raw=source[ts[i+1].end():end]
 raw=re.sub(r';[^\n]*','',raw)
 ts=re.findall(r'\[|\]|=|[^\s\[\]=]+',raw);offset=0;rows=[];i=0
 while i<len(ts):
  if ts[i]=='[':
   name,count=ts[i+1],int(ts[i+2]);assert ts[i+3]==']';i+=4
  else:name,count=ts[i],1;i+=1
  if i<len(ts) and ts[i]=='=':
   i+=1
   if ts[i]=='[':
    i+=1
    while ts[i]!=']':i+=1
    i+=1
   else:i+=1
  rows.append(dict(name=name,word_offset=offset,word_count=count,byte_offset=offset*2));offset+=count
 return rows


def profile():
 p=json.loads((H/'BUILD-PROFILE.json').read_text())
 art=json.loads((H/'OPENING-ASSET-MANIFEST.json').read_text())
 if sys.argv[1:]==['--phase-a']:
  if p['phase']!='A' or art.get('fixture_category')!='AUDIO_TIMING_ONLY_STATIC_REFERENCE_NO_ANIMATION_ACCEPTANCE':raise RuntimeError('Explicit Phase A fixture profile required')
 elif sys.argv[1:]==['--composition']:
  if p['phase']!='B' or p.get('build_status')!='COMPOSITION_IN_PROGRESS':raise RuntimeError('Engineering composition profile required')
  # Compilation can check shared ABI before every authored payload is ready.
  # This mode cannot be staged as a complete candidate or published as a release.
 elif sys.argv[1:] in (['--candidate'],['--release']):
  required_phase='B' if sys.argv[1:]==['--candidate'] else 'C'
  if p['phase']!=required_phase or art.get('fixture_category') or art.get('performed_pose_count')!=64:raise RuntimeError('Complete presentation refuses fixture or incomplete opening')
  if set(p['modules'])!=({0,*range(980,1000),941,942,943,944,945,946,948,970,*range(950,967)}):raise RuntimeError('Complete presentation module universe')
  if set(art.get('views',[]))!=set(range(245,253)):raise RuntimeError('Eight opening view identities required')
  coverage=json.loads((H/'FINAL-COVERAGE-MANIFEST.json').read_text())
  if coverage.get('status')!='COMPLETE_ASSETS_AND_SOURCE_GATES' or coverage.get('fixture_categories'):raise RuntimeError('Final release coverage incomplete')
  if set(coverage.get('requirements',{}))!={'opening','score','audience','foley','laugh_pool'} or any(row.get('status')!='SOURCE_AND_ASSET_COMPLETE' for row in coverage['requirements'].values()):raise RuntimeError('Five presentation scopes must be complete together')
  for item in coverage.get('bound_inputs',[]):
   if sha(H/item['path'])!=item['sha256']:raise RuntimeError(('coverage input identity',item['path']))
  if not coverage.get('bound_inputs'):raise RuntimeError('Coverage input pins missing')
  if any('AUDIO_TIMING_ONLY_STATIC_REFERENCE_NO_ANIMATION_ACCEPTANCE' in x.read_text() for x in (H/'src').glob('*.sc')):raise RuntimeError('Fixture source in release')
 else:raise RuntimeError('Choose explicit --phase-a, --composition, --candidate or --release; no implicit release')
 for name,pin in p['protected_inputs'].items():
  if sha(H/name)!=pin:raise RuntimeError(('protected input changed',name))
 modules=[0 if n=='main.sc' else int(n.removeprefix('module').removesuffix('.sc')) for n in json.loads((H/'SOURCE-ORDER.json').read_text())]
 if len(modules)!=len(set(modules)) or set(modules)!=set(p['modules']):raise RuntimeError('Explicit module membership')
 if not set(p['required_phase_a_modules'])<=set(modules):raise RuntimeError('Missing real Phase A controller modules')
 if set(x.name for x in (H/'src').glob('*.sc'))!={('main.sc' if n==0 else f'module{n}.sc') for n in modules}:raise RuntimeError('Canonical source membership')
 return p

def build():
 if sys.flags.optimize:raise RuntimeError('Optimized Python forbidden')
 config=profile()
 from extract_sci11 import extract
 from source_tools import methods
 import pack
 selectors=json.loads((D/'selectors.json').read_text())
 canonical_sources={name:(H/'src'/name).read_text() for name in json.loads((H/'SOURCE-ORDER.json').read_text())}
 from selector_aliases import apply as compile_aliases
 compiler_sources,compiler_selectors,aliases=compile_aliases(canonical_sources,selectors)
 dump(B/'selector-aliases.json',aliases)
 dump(B/'selector-alias-ledger.json',{'mapping':{n:{'alias':a,'selector_id':selectors[n]} for n,a in aliases.items()},'canonical_sources':{f:hashlib.sha256(t.encode()).hexdigest() for f,t in canonical_sources.items()},'compiler_sources':{f:hashlib.sha256(t.encode()).hexdigest() for f,t in compiler_sources.items()},'legacy_selectors_unchanged':True})
 pack.SELECTORS=compiler_selectors
 resources={}
 owners=[0,0,*range(980,998)]
 # Keep the frozen insertion order for exact inventory/metadata identity.
 inventory=json.loads((H/'RESOURCE-INVENTORY.json').read_text())
 if set(x.name for x in (H/'assets/resources').iterdir())!={r['extracted_path'] for r in inventory if (r['type'],r['number']) not in {(6,996),(6,997)}}:raise RuntimeError('resource input membership')
 if len({(r['type'],r['number']) for r in inventory})!=len(inventory):raise RuntimeError('duplicate typed resource')
 if sys.argv[1:] in (['--candidate'],['--release']) and any(r['type']==0 and 104<=r['number']<=112 for r in inventory):raise RuntimeError('Legacy static opening references excluded from complete runtime')
 for row in inventory:
  key=(row['type'],row['number'])
  if key==(6,996):data=struct.pack('<'+'H'*len(owners)*2,*sum(([0,n] for n in owners),[]))
  elif key==(6,997):data=pack.selector_resource()
  else:data=(H/'assets/resources'/row['extracted_path']).read_bytes()
  if hashlib.sha256(data).hexdigest()!=row['sha256']:raise RuntimeError(('resource identity',key))
  resources[key]=data
 speech=B/'speech';speech.mkdir(exist_ok=True)
 manifest=json.loads((H/'AUDIO-INVENTORY.json').read_text())
 for name,row in manifest['files'].items():
  p=H/'assets/audio'/name
  if p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:raise RuntimeError(('audio identity',name))
  (speech/name).write_bytes(p.read_bytes())
 if manifest.get('file_count')!=len(manifest['files']) or len(manifest['files'])!=config['audio_files'] or set(p.name for p in speech.iterdir())!=set(manifest['files']) or set(p.name for p in (H/'assets/audio').iterdir())!=set(manifest['files']):raise RuntimeError('audio membership')
 owners=[0,0,*range(980,998)]
 resources[6,996]=struct.pack('<'+'H'*len(owners)*2,*sum(([0,n] for n in owners),[]));resources[6,997]=pack.selector_resource()
 pack.pack_resources(resources,B)
 numbers=config['compile_order']
 if len(numbers)!=len(set(numbers)) or set(numbers)!=set(config['modules']):raise RuntimeError('compile order membership')
 (B/'game.ini').write_text('[Game]\nName=Come and Knock on Our Door\nLanguage=sci\n[Script]\nn000=main\n'+''.join(f'n{n}=module{n}\n' for n in numbers if n))
 (B/'src').mkdir(exist_ok=True);(B/'compiled').mkdir(exist_ok=True)
 for stale in (B/'src').glob('*.sco'):stale.unlink()
 for name,text in compiler_sources.items():(B/'src'/name).write_text(text)
 sl=[dict(name=n,selector_id=i) for n,i in sorted(selectors.items(),key=lambda x:x[1])];dump(B/'selector-list.json',sl)
 abi={'selectors':sl,'modules':{}};rows=[]
 compiler=H/'toolchain/scicompile'
 if sha(compiler)!='608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e':raise RuntimeError('compiler identity')
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
  if n==990:
   objs=layout['objects'];cls=[o for o in objs if o['is_class']];inst=next(o for o in objs if o['name']=='p09State')
   if len(cls)!=1 or cls[0]['species']!=12 or inst['superclass']!=12 or layout['exports']!=[inst['heap_offset']]:raise RuntimeError('Production P09 species/export contract')
  if n==991:
   objs=layout['objects'];cls=[o for o in objs if o['is_class']];inst=next(o for o in objs if o['name']=='sceneRenderer')
   if len(cls)!=1 or cls[0]['species']!=13 or inst['superclass']!=13 or layout['exports']!=[inst['heap_offset']]:raise RuntimeError('SceneRenderer species/export contract')
   if layout['locals_word_count'] or len(cls[0]['properties'])!=9:raise RuntimeError('Renderer must remain stateless')
  if n in (996,997):
   cls=[o for o in layout['objects'] if o['is_class']];expected=18 if n==996 else 19
   if len(cls)!=1 or cls[0]['species']!=expected:raise RuntimeError(('P14 species',n))
  if n in ({998,999}|set(config['class_free_additions'])) and any(o['is_class'] for o in layout['objects']):raise RuntimeError(f'{n} must remain class-free')
  if n==0:
   if len(layout['exports'])!=2:raise RuntimeError('Main canonical instance exports')
   if any(o['is_class'] and o['species'] not in (0,1) for o in layout['objects']):raise RuntimeError('Main class identity')
  if n==995:
   objs=layout['objects'];cls=[o for o in objs if o['is_class']];inst=next(o for o in objs if o['name']=='p13State')
   if len(cls)!=1 or cls[0]['species']!=17 or inst['superclass']!=17 or layout['exports']!=[inst['heap_offset']]:raise RuntimeError('P13 species/export contract')
  if n==994:
   objs=layout['objects'];cls=[o for o in objs if o['is_class']];inst=next(o for o in objs if o['name']=='p12State')
   if len(cls)!=1 or cls[0]['species']!=16 or inst['superclass']!=16 or layout['exports']!=[inst['heap_offset']]:raise RuntimeError('P12 species/export contract')
  if n==993:
   objs=layout['objects'];cls=[o for o in objs if o['is_class']];inst=next(o for o in objs if o['name']=='p11State')
   if len(cls)!=1 or cls[0]['species']!=15 or inst['superclass']!=15 or layout['exports']!=[inst['heap_offset']]:raise RuntimeError('P11 species/export contract')
  if n==992:
   objs=layout['objects'];cls=[o for o in objs if o['is_class']];inst=next(o for o in objs if o['name']=='p10State')
   if len(cls)!=1 or cls[0]['species']!=14 or inst['superclass']!=14 or layout['exports']!=[inst['heap_offset']]:raise RuntimeError('P10 species/export contract')
  abi['modules'][str(n)]=dict(source='src/'+src.name,sha256=sha(src),local_words=layout['locals_word_count'],locals=decls,classes=classes,reference_layout=layout)
  size=out.stat().st_size+hep.stat().st_size+(2 if out.stat().st_size&2 else 0)
  if size>65535:raise RuntimeError(('SCI16 resource budget',n,size))
  rows.append(dict(module=n,source_sha256=sha(D/'src'/src.name),compiler_source_sha256=sha(src),script_sha256=sha(out),heap_sha256=sha(hep),combined_bytes=size,class_species=[c['species'] for c in layout['objects'] if c['is_class']]))
 C=B/'verification-checkpoint';(C/'assets/resources').mkdir(parents=True,exist_ok=True);inventory=[]
 suffix={0:'view',1:'pic',3:'text',4:'sound',6:'vocab',7:'font',9:'patch',11:'palette'}
 for (t,n),data in resources.items():
  name=f'{n:03}.{suffix[t]}.bin';(C/'assets/resources'/name).write_bytes(data);inventory.append(dict(type=t,number=n,extracted_path=name,size=len(data),sha256=hashlib.sha256(data).hexdigest()))
 dump(C/'reference/resources.json',inventory);dump(C/'source-provenance/ABI-MAPPINGS.json',abi);dump(B/'ABI-MAPPINGS.json',abi)
 dump(B/'compile-receipt.json',dict(status='PASS_FRESH_COMPILE',complete_candidate=sys.argv[1:] in (['--candidate'],['--release']),compile_purpose='engineering-composition' if sys.argv[1:]==['--composition'] else 'declared-profile',phase=config['phase'],build_profile_sha256=sha(H/'BUILD-PROFILE.json'),fixture_category=config.get('fixture_category'),diagnostic_traces=False,trace_mode='removed-noop-ABI',modules=rows,class_owners=owners,native_acceptance=False,runtime_package=False,compiler_sha256=sha(compiler)))
 pack.validate_resources(B)
 print('PASS_FRESH_COMPILE',[(r['module'],r['combined_bytes']) for r in rows])
if __name__=='__main__':
 try:build()
 except BaseException as e:
  dump(B/'compile-receipt.json',{'status':'FAILED','reason':str(e),'native_acceptance':False});raise
