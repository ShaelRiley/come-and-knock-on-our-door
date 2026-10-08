#!/usr/bin/env python3
"""Bounded additive P09 foundation over a frozen, accepted production universe."""
from pathlib import Path
import hashlib,json,re,sys
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'tools'))
from source_tools import methods,tokens
from source_derivation import merge,append_properties,insert,replace,balanced

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def require(ok,message):
 if not ok:raise RuntimeError(message)
def verify_inputs():
 require(not sys.flags.optimize,'Optimized Python forbidden')
 pins=json.loads((H/'INPUT-SEAL.json').read_text())
 actual={str(p.relative_to(H)) for f in ('frozen','toolchain') for p in (H/f).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 require(actual==set(pins),'Frozen input membership changed')
 for n,s in pins.items():require(sha(H/n)==s,'Frozen input changed: '+n)
 manifest=json.loads((H/'toolchain/SOURCE-MANIFEST.json').read_text())
 require(manifest['publication_revision']==2 and len(manifest['files'])==198,'Exact R2 compiler closure required')
def array(source,name):
 m=re.search(r'\['+name+r' (\d+)\] = \[([^]]*)\]',source)
 require(m is not None,'Array absent '+name)
 v=list(map(int,m[2].split()));require(len(v)==int(m[1]),'Array extent '+name);return v
def replace_array(source,name,values):
 matches=list(re.finditer(r'\['+name+r' \d+\] = \[[^]]*\]',source))
 require(len(matches)==1,'Array shape '+name);m=matches[0]
 return source[:m.start()]+'['+name+' '+str(len(values))+'] = ['+' '.join(map(str,values))+']'+source[m.end():]

def transform_scene(source):
 # Match the accepted predecessor data while retaining the later P08 reader code.
 scene=H/'frozen/scene'
 pin=json.loads((scene/'COMPATIBILITY.json').read_text())['predecessor']
 extended=json.loads((scene/'generated/extension-contract.json').read_text())['arrays']
 for name,digest in pin['array_hashes'].items():
  old=array(source,name)
  require(hashlib.sha256(json.dumps(old,separators=(',',':')).encode()).hexdigest()==digest,'Pre-P09 scene array changed '+name)
  require(extended[name][:len(old)]==old,'Earlier scene prefix changed '+name)
  source=replace_array(source,name,extended[name])
 mm=methods(source);hooks={}
 for name in ('sdRoute','sdPageCount'):
  hooks[name]=replace(mm[name],'(> document 1017)','(> document 1139)')
 body=replace(mm['sdLoad'],'(>= index (* 1138 8))','(>= index (* 1191 8))')
 for prop,value in [('sdResource',210),('sdAudioModule',921)]:
  matches=list(re.finditer(r'\(and(?:\s+\(!= '+prop+r' \d+\))+\)',body))
  require(len(matches)==1,'Scene allowlist shape '+prop)
  old=matches[0].group();body=replace(body,old,old[:-1]+f' (!= {prop} {value}))')
 hooks['sdLoad']=body
 hooks['hStaticAt']=methods((scene/'generated/static/module982-methods.inc').read_text())['hStaticAt']
 return merge(source,hooks)

def derive(check=False):
 verify_inputs()
 base=H/'frozen/p08';source={p.name:p.read_text() for p in (base/'src').glob('*.sc')}
 original={n:methods(s) for n,s in source.items()}
 domain=(H/'frozen/domain/src/module990.sc').read_text();dm=methods(domain)
 require(len(dm)==61,'Domain method count')
 domain=append_properties(domain,'h9Host 0')
 domain=merge(domain,methods((H/'templates/host990.sc.in').read_text()))
 require(all(methods(domain)[n]==s for n,s in dm.items()),'Literal domain drift')
 source['module990.sc']=domain
 source['module982.sc']=transform_scene(source['module982.sc'])
 guard=methods((H/'frozen/scene/generated/static/guard-methods.inc').read_text())
 # All other static families must match the current production source values.
 static=json.loads((H/'frozen/scene/generated/static/manifest.json').read_text())
 for t in static['tables']:
  expected=[v&65535 for v in array(source[f'module{t["module"]}.sc'],t['name'])]
  require(expected==t['values'],'Static data changed '+t['name'])
 source['module985.sc']=merge(source['module985.sc'],{n:guard[n] for n in ('hStaticCount','hStaticFirst','hStaticLoad')})
 mm=methods(source['main.sc']);hooks={}
 hooks['p04Initialize']=mm['p04Initialize'][:-1]+'\n(= p09 (ScriptID 990 0)) (p09 h9Init: self)\n)'
 hooks['bridgeActAtArrival']=insert(mm['bridgeActAtArrival'],'(if (and p09 (p09 h9Dispatch: action obj target)) (return 0))')
 for n,value in [('campaignHeld',0),('campaignReachable',0),('p02ObjectLocation',-1)]:
  hooks[n]=insert(mm[n],f'(if (and (>= obj 395) (<= obj 399)) (return {value}))')
 # The old reservation array is 33 words; no high-ID object may index it.
 hooks['p02SyncInventory']=replace(mm['p02SyncInventory'],'(= obj [p02Slots i])',
  '(= obj [p02Slots i])\n            (if (or (< obj 0) (> obj 32)) (= p02InventoryOverflow 1) (return 0))')
 source['main.sc']=merge(append_properties(source['main.sc'],'p09 0'),hooks)
 permitted={'main.sc':set(hooks),'module982.sc':{'sdRoute','sdPageCount','sdLoad','hStaticAt'},'module985.sc':{'hStaticCount','hStaticFirst','hStaticLoad'}}
 delta={}
 for name,before in original.items():
  after=methods(source[name]);changed=[n for n in before if before[n]!=after[n]]
  require(set(changed)<=permitted.get(name,set()),'Unexpected method change '+name)
  require(set(before)==set(after),'Unexpected old-module method membership '+name)
  delta[name]={'changed_methods':changed,'preserved_methods':len(before)-len(changed),'source_sha256':hashlib.sha256(source[name].encode()).hexdigest()}
 selectors=json.loads((base/'selectors.json').read_text())
 plan=json.loads((H/'ALLOCATION-PLAN.json').read_text())
 new=plan['domain_new_names']+plan['foundation_host_new_names']
 require(len(new)==164 and sum(len(n.encode('ascii'))+2 for n in new)==2718,'Pre-allocation measurement drift')
 allocation={n:3000+i for i,n in enumerate(new)}
 require(not(set(new)&set(selectors)) and not(set(allocation.values())&set(selectors.values())),'Selector collision')
 selectors.update(allocation)
 require(max(allocation.values())<4096 and not any(2987<=v<=2999 for v in allocation.values()),'Reserved selector boundary')
 for name,text in source.items():
  balanced(text)
  needed=set(methods(text))
  for props in re.findall(r'\(properties\s+([^)]*)\)',text):needed.update([t.group() for t in tokens(props)][::2])
  require(not (needed-selectors.keys()),'Unallocated names '+repr(needed-selectors.keys()))
  path=H/'src'/name
  if check:require(path.exists() and path.read_text()==text,'Derived source drift '+name)
  else:path.write_text(text)
 require({p.name for p in (H/'src').glob('*.sc')}==set(source),'Unexpected source file')
 if check:require(json.loads((H/'selectors.json').read_text())==selectors,'Selector drift')
 else:
  dump(H/'selectors.json',selectors);dump(H/'HOST-ALLOCATION.json',allocation)
  dump(H/'INTEGRATION-DELTA.json',{'baseline':'frozen/p08','baseline_is_current_e03':False,'active_dispatch':False,'production_species':12,'export':0,'domain_literal_methods':61,'old_modules':delta,'rebase_rule':'Reapply guarded additive transforms to final accepted P08 E03 source. Never replace its module989 or readiness/storage source with this older baseline.'})
 return source,selectors

if __name__=='__main__':
 derive('--check' in sys.argv);print('PASS_GUARDED_P09_FOUNDATION')
