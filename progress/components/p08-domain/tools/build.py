#!/usr/bin/env python3
"""Fresh pinned compiler proof for domain-only script989. No Main mutation.
No binary from another source universe is spliced into a playable game.
"""
from pathlib import Path
import hashlib,json,os,shutil,struct,subprocess,sys,tempfile
H=Path(__file__).resolve().parents[1]
(H/'reports/latest.json').write_text('{"status":"FAIL","phase":"build_started_not_reverified","native_acceptance":false}\n')
sys.dont_write_bytecode=True
from emitted_gates import source_metadata,selector_encode,encode_resources,decode_resources,extract,audit_module
COMPILER_SHA='608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e'
OWNERS=[0,0,980,981,982,983,984,985,986,987,988,989]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def build():
 if sys.flags.optimize:raise RuntimeError('Optimized proof runs are forbidden')
 compiler=H/'inputs/toolchain/scicompile'
 if sha(compiler)!=COMPILER_SHA:raise RuntimeError('Compiler pin drift')
 subprocess.run([sys.executable,str(H/'tools/generate.py'),'--check'],check=True)
 source=H/'src/module989.sc';meta=source_metadata(source.read_text())
 if list(meta['classes'])!=['P08State'] or list(meta['instances'])!=['p08State'] or meta['exports']!={0:'p08State'}:raise RuntimeError('Source identity changed')
 retained=json.loads((H/'inputs/current-selectors.json').read_text())
 selectors=json.loads((H/'inputs/r1-domain-selectors.json').read_text());old=dict(selectors)
 if any(selectors.get(k)!=v for k,v in retained.items()):raise RuntimeError('R1 selector mapping changed retained current IDs')
 names=sorted((meta['methods']|meta['properties'])-set(selectors))
 free=[i for i in range(2600,2800) if i not in selectors.values()]
 if len(names)>len(free):raise RuntimeError('Reserved selector range exhausted')
 selectors.update({n:free[i] for i,n in enumerate(names)})
 if any(selectors[k]!=v for k,v in old.items()):raise RuntimeError('Retained selector changed')
 destination=H/'build'
 if destination.exists() and not (destination/'P08-BUILD-OWNED.json').is_file():raise RuntimeError('Refusing unowned build directory')
 with tempfile.TemporaryDirectory(prefix='.p08-build-',dir=H) as tmp:
  out=Path(tmp)
  for n in ('src','compiled','logs','layouts'):(out/n).mkdir()
  shutil.copy2(source,out/'src/module989.sc')
  seed={(6,996):struct.pack('<'+'H'*(2*len(OWNERS)),*[v for owner in OWNERS for v in (0,owner)]),(6,997):selector_encode(selectors)}
  map_,vol,_=encode_resources(seed);(out/'resource.map').write_bytes(map_);(out/'resource.000').write_bytes(vol)
  (out/'game.ini').write_text('[Game]\nName=P08 isolated domain compiler proof\nLanguage=sci\n[Script]\nn989=module989\n')
  binary=out/'compiled/989.scr.bin';heap=Path(str(binary)+'.hep')
  cmd=[str(compiler),'--version','sci11',str(out),str(out/'src/module989.sc'),str(binary)]
  run=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
  log=run.stdout+run.stderr;(H/'reports/compile-latest.log').write_text(log)
  (out/'logs/compile-989.log').write_text(log)
  if run.returncode or '[error]' in log.lower() or not binary.is_file() or not heap.is_file():raise RuntimeError('Compiler failed: '+log)
  data=extract(binary.read_bytes(),heap.read_bytes(),selectors)
  if [o['species'] for o in data['objects'] if o['is_class']]!=[11]:raise RuntimeError('P08 species differs')
  if next(o for o in data['objects'] if o['name']=='p08State')['superclass']!=11:raise RuntimeError('P08 instance differs')
  if decode_resources(out)!=seed:raise RuntimeError('Compiler rewrote names')
  tables=json.loads((H/'reference/opcode-tables.json').read_text());kernels=json.loads((H/'reference/kernels.json').read_text())
  gate=audit_module(985,binary.read_bytes(),heap.read_bytes(),data,selectors,tables,kernels,meta,0,OWNERS)
  gate['module']=989;gate['strict_policy']='Reused unchanged strict domain policy; 985 is policy selector only'
  receipt={'status':'PASS_FRESH_COMPILE','scope':'script989 only against preserved numeric class/selector universe','compiler_sha256':COMPILER_SHA,'source_sha256':sha(source),'script_sha256':sha(binary),'heap_sha256':sha(heap),'combined_bytes':data['combined_bytes'],'species':11,'selectors_added':{n:sid for n,sid in selectors.items() if n not in retained},'r2_selectors_added':{n:selectors[n] for n in names},'preserved_r1_selector_count':len(old),'r1_selector_sha256':sha(H/'inputs/r1-domain-selectors.json'),'preserved_selector_count':len(retained),'retained_selector_sha256':sha(H/'inputs/current-selectors.json'),'native_acceptance':False,'runtime_package':False}
  dump(out/'P08-BUILD-OWNED.json',{'schema':1,'kind':'p08-domain-build'})
  dump(out/'layouts/989.json',data);dump(out/'emitted-gates.json',gate);dump(out/'compile-receipt.json',receipt);dump(out/'selectors.json',selectors)
  if destination.exists():shutil.rmtree(destination)
  shutil.copytree(out,destination)
 dump(H/'selectors.json',selectors);dump(H/'reports/build.json',receipt);dump(H/'reports/emitted-gates.json',gate)
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':
 try:build()
 except BaseException as e:
  dump(H/'reports/build.json',{'status':'FAIL','error':str(e),'native_acceptance':False});raise
