#!/usr/bin/env python3
"""Exact guarded extraction; newly reconstructed script991, no historical claim."""
from pathlib import Path
import sys,json,hashlib,re
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;F=H/'frozen/p09'
sys.path.insert(0,str(H/'tools'))
from source_tools import tokens,methods,spans
MOVED=['renderCaption','navNoticeRender','h6BaseDrawWorld','roomTitle','blockPerson','drawJack','drawLiving','livingPerson','neighborPerson','drawKitchen','drawP03Conservatory','p03Rita','drawSidePassage','p04Felix']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def require(v,*s):
 if not v:raise RuntimeError(s)
def verify_inputs():
 for n,v in json.loads((H/'INPUT-MANIFEST.json').read_text()).items():require(sha(H/n)==v,'Changed sealed input',n)
def relocate(source,properties,selectors):
 ts=tokens(source);depth=0;sig_end=None
 for i,t in enumerate(ts[2:],2):
  if t.group()=='(':depth+=1
  if t.group()==')':
   depth-=1
   if depth==0:sig_end=i;break
 require(sig_end is not None,'Method signature')
 sig=[t.group() for t in ts[4:sig_end]];split=sig.index('&tmp') if '&tmp' in sig else len(sig)
 args=sig[:split];temps=sig[split+1:];require('owner' not in sig and 'savedAcc' not in sig,'Reserved parameter collision')
 edits=[];asmranges=[]
 for i,t in enumerate(ts):
  if t.group()=='(' and ts[i+1].group()=='asm':
   end=next(q for q in ts[i+2:] if q.group()==')');asmranges.append((t.start(),end.end()))
   raw=source[ts[i+1].end():end.start()]
   require(not re.search(r'\b(?:aTop|sTop|\+ap|-ap|\+sp|-sp|lal|lsl|lali|lsli|sal|ssl|sali|ssli|lap|lsp|sap|ssp|selfID|pushSelf)\b',raw),'Unsupported context opcode')
   def prop(m):
    op,p=m.groups();require(p in properties and p in selectors,'Property mapping',p)
    seq=f'pushi {selectors[p]}\n            push0\n            lap 1\n            send 4'
    # pTos must preserve the original accumulator as well as stack position.
    return (f'sat {len(temps)}\n            '+seq+f'\n            push\n            lat {len(temps)}') if op=='pTos' else seq
   raw=re.sub(r'\b(pToa|pTos)\s+(\w+)',prop,raw)
   raw=re.sub(r'\bself (\d+)',r'lap 1\n            send \1',raw)
   edits.append((ts[i+1].end(),end.start(),raw))
 # Replace only actual body tokens, never strings/comments, selectors or parameter declarations.
 for t in ts[sig_end+1:]:
  if any(a<=t.start()<b for a,b in asmranges):continue
  v=t.group()
  if v in properties and v not in args+temps:edits.append((t.start(),t.end(),f'(owner {v}?)'))
  elif v=='self':edits.append((t.start(),t.end(),'owner'))
 signature=' '.join([ts[3].group(),'owner',*args]+(['&tmp',*temps,'savedAcc'] if asmranges else (['&tmp',*temps] if temps else [])))
 edits.append((ts[3].start(),ts[sig_end].start(),signature))
 for a,b,v in sorted(edits,reverse=True):source=source[:a]+v+source[b:]
 return source,args

def derive(check=False):
 verify_inputs();base=(F/'src/main.sc').read_text();old=methods(base);selectors=json.loads((F/'selectors.json').read_text())
 abi=json.loads((F/'build/coherent/ABI-MAPPINGS.json').read_text());properties={p['selector'] for p in abi['modules']['0']['classes'][0]['properties'] if p['index']>=9}
 output={p.name:p.read_text() for p in (F/'src').glob('*.sc')};moved={};wrappers={};inventory=[]
 for name in MOVED:
  moved[name],args=relocate(old[name],properties,selectors)
  wrappers[name]=f'(method ({name}'+(' '+' '.join(args) if args else '')+')\n (return ((ScriptID 991 0) '+name+': self'+(' '+' '.join(args) if args else '')+')))'
  inventory.append(dict(method=name,selector=selectors[name],parameters=args,baseline_method_sha256=digest(old[name]),renderer_method_sha256=digest(moved[name]),wrapper_sha256=digest(wrappers[name]),assembly_reads=re.findall(r'pTo[as]\s+(\w+)',old[name])))
 main=base
 for name,(a,b) in sorted(spans(base).items(),key=lambda x:x[1][0],reverse=True):
  if name in wrappers:main=main[:a]+wrappers[name]+main[b:]
 output['main.sc']=main
 output['module991.sc']=';;; Sierra Script 1.0 - (do not remove this comment)\n; New extraction from accepted source, not recovered historical991.\n; Stateless renderer: owner is supplied on every call; all self dispatch stays on owner.\n(script# 991)\n(public sceneRenderer 0)\n(class SceneRenderer\n (properties)\n'+'\n\n'.join(moved.values())+'\n)\n(instance sceneRenderer of SceneRenderer)\n'
 for n,s in output.items():
  if check:require((H/'src'/n).read_text()==s,'Derived source drift',n)
  else:(H/'src'/n).write_text(s)
 if check:require(json.loads((H/'selectors.json').read_text())==selectors,'Selector drift')
 else:
  dump(H/'selectors.json',selectors);dump(H/'EXTRACTION-INVENTORY.json',inventory)
 return output,selectors
if __name__=='__main__':derive('--check' in sys.argv);print('PASS_GUARDED_EXTRACTION')
