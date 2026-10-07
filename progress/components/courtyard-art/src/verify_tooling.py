#!/usr/bin/env python3
"""Bounded independent regeneration, import safety, optimized mode and stale-PASS tests."""
from common import ROOT,Guard,write_json,require,sha
_entry_guard=Guard('tooling') if __name__=='__main__' else None
import shutil,subprocess,sys,json,os

def run():
 g=_entry_guard or Guard('tooling');base=ROOT/'evidence/tooling-fixture'
 if base.exists():shutil.rmtree(base)
 base.mkdir()
 for d in ['src','reference','source-masters','indexed-cels','resources']:
  shutil.copytree(ROOT/d,base/d,ignore=shutil.ignore_patterns('__pycache__'))
 (base/'evidence').mkdir();(base/'components').mkdir();(base/'previews').mkdir();shutil.copy2(ROOT/'manifest.json',base/'manifest.json')
 def call(args):
  p=subprocess.run([sys.executable,*args],cwd=base,text=True,capture_output=True);return p
 good=call(['src/build.py']);require(good.returncode==0,'Source regeneration failed: '+good.stderr)
 m=json.loads((ROOT/'manifest.json').read_text());new=json.loads((base/'manifest.json').read_text());require(m==new,'Deterministic conversion manifest differs')
 for c in m['cels']:require(sha(ROOT/c['file'])==sha(base/c['file']),'Indexed source regeneration differs')
 for v in m['resources'].values():require(sha(ROOT/v['file'])==sha(base/v['file']),'Native regeneration differs')
 encoded=call(['src/encode_indexed.py']);require(encoded.returncode==0,'Indexed conversion failed');require(json.loads((base/'manifest.json').read_text())==m,'Indexed-only regeneration changed bytes')
 # Import pure modules cannot regenerate or mutate files.
 before={str(p.relative_to(base)):sha(p) for p in base.rglob('*') if p.is_file() and '__pycache__' not in str(p)}
 imported=call(['-c',"import sys;sys.dont_write_bytecode=True;sys.path.insert(0,'src');import build,render,validate,encode_indexed,host_fragment,geometry,inspect_view,view_writer"])
 require(imported.returncode==0,'Pure imports failed: '+imported.stderr)
 after={str(p.relative_to(base)):sha(p) for p in base.rglob('*') if p.is_file() and '__pycache__' not in str(p)};require(before==after,'Import mutated data')
 cases=[]
 for tool,status in [('build','build'),('render','preview'),('validate','validation'),('encode_indexed','encode_indexed')]:
  write_json(base/'evidence'/f'{status}.json',{'status':'PASS'});write_json(base/'evidence/validation.json',{'status':'PASS'})
  p=call(['-O',f'src/{tool}.py']);require(p.returncode!=0,'Optimized mode accepted');require(json.loads((base/'evidence'/f'{status}.json').read_text())['status']=='FAIL','Optimized failure left stale PASS');require(json.loads((base/'evidence/validation.json').read_text())['status']!='PASS','Dependent validation retained stale PASS');cases.append(tool+' -O')
 for tool,status in [('build','build'),('render','preview'),('validate','validation'),('encode_indexed','encode_indexed')]:
  write_json(base/'evidence'/f'{status}.json',{'status':'PASS'});write_json(base/'evidence/validation.json',{'status':'PASS'})
  p=call(['-c',f"import sys,runpy;sys.path.insert(0,'src');sys.modules['PIL']=None;runpy.run_path('src/{tool}.py',run_name='__main__')"])
  require(p.returncode!=0,'Missing dependency accepted');require(json.loads((base/'evidence'/f'{status}.json').read_text())['status']=='FAIL','Import failure left stale PASS');require(json.loads((base/'evidence/validation.json').read_text())['status']!='PASS','Dependency failure retained stale PASS');cases.append(tool+' unavailable PIL')
 # A native mutation must fail verification and invalidate its old PASS.
 write_json(base/'evidence/validation.json',{'status':'PASS'});p=base/'resources/305.view.bin';raw=bytearray(p.read_bytes());raw[-1]^=1;p.write_bytes(raw)
 bad=call(['src/validate.py']);require(bad.returncode!=0 and json.loads((base/'evidence/validation.json').read_text())['status']=='FAIL','Mutated native resource accepted')
 report={'source_regeneration':'byte-identical indexed/native/manifest','indexed_only_regeneration':'byte-identical','pure_imports':'no output mutation','rejected_guard_cases':cases,'tampered_native':'rejected','scope':'tooling/static only'}
 write_json(ROOT/'evidence/reproducibility.json',report);shutil.rmtree(base);g.done(**report)
if __name__=='__main__':run()
