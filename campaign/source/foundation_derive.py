#!/usr/bin/env python3
"""Rebase the accepted inactive P09 and renderer deltas onto current ACK bytes.

No ancestor module989 or Main replaces the current ACK semantic basis. Only
guarded P09 method/property deltas and the fourteen stateless paint moves apply.
"""
from pathlib import Path
import sys,json,hashlib,importlib.util
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'tools'))
from source_tools import methods,spans
from source_derivation import merge,append_properties,balanced
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def require(v,*s):
 if not v:raise RuntimeError(s)
def verify_inputs():
 pins=json.loads((H/'INPUT-MANIFEST.json').read_text())
 actual={str(p.relative_to(H)) for d in ('frozen','toolchain') for p in (H/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 require(actual==set(pins),'Frozen input membership changed')
 for p,v in pins.items():require(sha(H/p)==v,'Changed sealed input',p)
 m=json.loads((H/'toolchain/SOURCE-MANIFEST.json').read_text())
 require(m['publication_revision']==2 and len(m['files'])==198,'Approved compiler source closure')
 for p,v in m['files'].items():require(sha(H/'toolchain/source'/p)==v,'Compiler source',p)

spec=importlib.util.spec_from_file_location('accepted_renderer_derivation',H/'frozen/renderer/derive.py')
renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
MOVED=renderer.MOVED
P09_MAIN={'p04Initialize','bridgeActAtArrival','campaignHeld','campaignReachable','p02ObjectLocation','p02SyncInventory','uiHostItemLabel','uiHostShortLabel','uiHostDefaultVerb','approachX','approachY','uiHostWorldControls','drawP03Conservatory'}
def derive(check=False,pre=False,emit=True):
 verify_inputs()
 ack=H/'frozen/ack';old=H/'frozen/pre-p09';geo=H/'frozen/geometry'
 output={p.name:p.read_text() for p in (ack/'src').glob('*.sc')}
 source0=output.copy();delta={}
 for name,current in list(output.items()):
  before=(old/'src'/name).read_text();after=(geo/'src'/name).read_text()
  if before==after:continue
  if name=='main.sc':
   oldm,newm,now=methods(before),methods(after),methods(current)
   changed={n:newm[n] for n in oldm if oldm[n]!=newm[n]}
   require(set(changed)==P09_MAIN,'Unexpected P09 Main delta')
   require(all(now[n]==oldm[n] for n in changed),'P09 changed method conflicts with current ACK')
   output[name]=merge(append_properties(current,'p09 0'),changed)
   # Exact new Main equals the accepted P09 predecessor plus the newer guard.
   require(methods(output[name])['readSave']==now['readSave'],'Current storage guard lost')
  else:
   require(name in ('module982.sc','module985.sc'),'Unexpected old-module P09 delta',name)
   require(current==before,'Current owner differs from P09 predecessor',name)
   output[name]=after
  delta[name]=[n for n in methods(current) if methods(current)[n]!=methods(output[name])[n]]
 output['module990.sc']=(geo/'src/module990.sc').read_text()
 require(output['module989.sc']==source0['module989.sc'],'Current ACK owner overwritten')
 selectors=json.loads((ack/'selectors.json').read_text());prior=json.loads((old/'selectors.json').read_text());added=json.loads((geo/'selectors.json').read_text())
 for n,i in added.items():
  if n in prior:require(prior[n]==i and selectors[n]==i,'Prior selector drift',n)
  else:
   require(n not in selectors and i not in selectors.values(),'Selector collision',n,i)
   require(3000<=i<=3166,'Unapproved P09 allocation',n,i);selectors[n]=i
 require(selectors['h8S']==2990 and selectors['h8E']==2991,'Current storage/ACK selector drift')
 require(not set(range(2992,3000))&set(selectors.values()),'P08 future space used')
 require(not set(range(3167,3200))&set(selectors.values()),'P09 future space used')
 extraction=[]
 if not pre:
  base=output['main.sc'];mm=methods(base)
  abi=json.loads((geo/'build/coherent/ABI-MAPPINGS.json').read_text())
  properties={p['selector'] for p in abi['modules']['0']['classes'][0]['properties'] if p['index']>=9}
  moved={};wrappers={}
  for n in MOVED:
   require(mm[n]==methods((geo/'src/main.sc').read_text())[n],'Rendering changed since accepted extraction',n)
   moved[n],args=renderer.relocate(mm[n],properties,selectors)
   wrappers[n]=f'(method ({n}'+(' '+' '.join(args) if args else '')+')\n (return ((ScriptID 991 0) '+n+': self'+(' '+' '.join(args) if args else '')+')))'
   extraction.append(dict(method=n,selector=selectors[n],before_sha256=digest(mm[n]),after_sha256=digest(moved[n])))
  for n,(a,b) in sorted(spans(base).items(),key=lambda x:x[1][0],reverse=True):
   if n in wrappers:base=base[:a]+wrappers[n]+base[b:]
  output['main.sc']=base
  output['module991.sc']=';;; Sierra Script 1.0 - (do not remove this comment)\n; New extraction from accepted source, not recovered historical991.\n; Stateless renderer: owner is supplied on every call; all self dispatch stays on owner.\n(script# 991)\n(public sceneRenderer 0)\n(class SceneRenderer\n (properties)\n'+'\n\n'.join(moved.values())+'\n)\n(instance sceneRenderer of SceneRenderer)\n'
  require(output['module991.sc']==(H/'frozen/renderer/src/module991.sc').read_text(),'Accepted renderer changed')
  # Current additions are exact; every other method is independently limited.
  before=methods(source0['main.sc']);after=methods(output['main.sc'])
  require(set(before)==set(after),'Main method membership')
  require({n for n in before if before[n]!=after[n]}==P09_MAIN|set(MOVED),'Main delta escaped bounds')
 if not emit:return output,selectors
 dest=H/'comparison/pre-extraction' if pre else H
 (dest/'src').mkdir(parents=True,exist_ok=True)
 for n,s in output.items():
  balanced(s)
  if check:require((dest/'src'/n).read_text()==s,'Derived source drift',n)
  else:(dest/'src'/n).write_text(s)
 if check:require(json.loads((dest/'selectors.json').read_text())==selectors,'Selector drift')
 else:
  dump(dest/'selectors.json',selectors)
  dump(dest/'INTEGRATION-DELTA.json',{'semantic_basis':'accepted current P08 storage/ACK','p09_old_module_changes':delta,'renderer_moves':extraction,'module989_exact_current_ack':True,'current_readSave_exact':True,'new_selectors':167,'p09_active':False,'evening_ready':False,'p10_included':False})
 return output,selectors
if __name__=='__main__':derive('--check' in sys.argv,'--pre-extraction' in sys.argv);print('PASS_REBASED_DERIVATION')
