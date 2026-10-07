#!/usr/bin/env python3
"""Compile isolated full SCI universe after guarded source patch. No runtime install."""
from pathlib import Path
import sys, json, shutil, hashlib, subprocess
W=Path(__file__).resolve().parent; H=W/'fixture'; B=H/'build/coherent'
sys.dont_write_bytecode=True;sys.path.insert(0,str(H/'tools'))
from extract_sci11 import extract
PIN='608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def compile_fixture():
 compiler=H/'toolchain/scicompile';assert sha(compiler)==PIN
 abi=json.loads((B/'ABI-MAPPINGS.json').read_text());rows=[]
 dump(B/'compile-receipt.json',{'status':'BUILDING','native_acceptance':False})
 for n in [980,981,982,983,984,985,986,987,988,0]:
  name='main.sc' if n==0 else f'module{n}.sc';src=H/'src'/name;shutil.copy2(src,B/'src'/name)
  out=B/f'compiled/{n}.scr.bin';hep=Path(str(out)+'.hep')
  out.unlink(missing_ok=True);hep.unlink(missing_ok=True)
  r=subprocess.run([str(compiler),'--version','sci11',str(B),str(B/'src'/name),str(out)],capture_output=True,text=True)
  (B/f'compile-{n}.log').write_text(r.stdout+r.stderr)
  assert r.returncode==0 and '[error]' not in r.stdout+r.stderr,(n,r.stdout,r.stderr)
  layout=extract(out,hep,B/'selector-list.json');old=abi['modules'][str(n)]
  classes=[{'name':o['name'],'properties':o['properties'],'methods':o['methods']} for o in layout['objects'] if o['is_class']]
  assert layout['locals_word_count']==old['local_words']
  for c in old['classes']:
   new=next(x for x in classes if x['name']==c['name']);assert c['properties']==new['properties'];assert [m['selector_id'] for m in c['methods']]==[m['selector_id'] for m in new['methods']]
  old.update(sha256=sha(src),classes=classes,reference_layout=layout)
  size=out.stat().st_size+hep.stat().st_size+(2 if out.stat().st_size&2 else 0);assert size<=65535
  rows.append(dict(module=n,source_sha256=sha(src),script_sha256=sha(out),heap_sha256=sha(hep),combined_bytes=size,class_species=[c['species'] for c in layout['objects'] if c['is_class']]))
 dump(B/'ABI-MAPPINGS.json',abi);dump(B/'verification-checkpoint/source-provenance/ABI-MAPPINGS.json',abi)
 report=dict(status='PASS_FRESH_COMPILE',modules=rows,compiler_sha256=PIN,native_acceptance=False,runtime_package=False,scope='isolated full SCI universe; resource.map/000 static inputs retained; no runtime staging')
 dump(B/'compile-receipt.json',report);dump(W/'evidence/compile-receipt.json',report);print('PASS_FRESH_COMPILE',[(r['module'],r['combined_bytes']) for r in rows])
if __name__=='__main__':compile_fixture()
