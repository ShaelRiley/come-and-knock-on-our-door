#!/usr/bin/env python3
"""Explicit guarded reconciliation of accepted P08 presentation and P09/P10 ownership."""
from pathlib import Path
import sys,json,hashlib,importlib.util,re,difflib
H=Path(__file__).resolve().parent;sys.dont_write_bytecode=True;sys.path.insert(0,str(H/'tools'))
from source_tools import methods,tokens
from source_derivation import merge,insert,append_locals,replace,balanced
from reader_derive import derive as reader

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')

def load_patch():
 spec=importlib.util.spec_from_file_location('accepted_inventory_delta',H/'p10-input/derive.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def local(source):
 ts=tokens(source);i=next(i for i,t in enumerate(ts) if t.group()=='(' and ts[i+1].group()=='local');depth=0
 for t in ts[i:]:
  depth+=(t.group()=='(')-(t.group()==')')
  if not depth:return source[ts[i].start():t.end()]
 raise AssertionError('locals')

def derive(check=False,pre=False):
 assert not pre
 current,selectors=reader(emit=False);original=current.copy();P=load_patch();P.verify_inputs()
 B=H/'p10-input/frozen/baseline';baseline={p.name:p.read_text() for p in (B/'src').glob('*.sc')}
 # P09 additions are imported method-by-method, never whole frozen owners.
 cm,bm=methods(current['main.sc']),methods(baseline['main.sc']);hooks={}
 for name in ('campaignHeld','p02HostInventory','p05RestoreBegin','p05RestoreReject','p05RestoreValidate','writeSave','h9PublishCard'):
  hooks[name]=bm[name]
 # This shared query keeps the current P08 actor override and the original card override.
 name='p02ObjectLocation';prefix='(if (and p08 (or (== obj 29) (== obj 30))) (return (p08 h8ActorRoom: (if (== obj 29) 4 else 7))))'
 assert prefix in cm[name] and prefix not in bm[name]
 hooks[name]=insert(bm[name],prefix)
 current['main.sc']=merge(current['main.sc'],hooks)
 cm,bm=methods(current['module990.sc']),methods(baseline['module990.sc'])
 assert all(cm[n]==bm[n] for n in cm)
 current['module990.sc']=merge(append_locals(current['module990.sc'],'[h9CardSlot 1] = [-1] [h9CardAdmission 1] = [1]'),{n:bm[n] for n in bm if n not in cm})
 # Extend only the immutable static-bank tables. Every old element is a literal prefix;
 # writable reader locals and P08 controls remain the current accepted definitions.
 name='module982.sc';a,b=local(current[name]),local(baseline[name])
 pattern=r'\[(\w+)\s+(\d+)\](?:\s*=\s*\[([^]]*)\])?'
 aa={m[1]:(int(m[2]),m[3],m[0]) for m in re.finditer(pattern,a)};bb={m[1]:(int(m[2]),m[3],m[0]) for m in re.finditer(pattern,b)}
 assert set(aa)==set(bb)
 for k,(count,values,raw) in aa.items():
  n,new,newraw=bb[k]
  if (count,values)==(n,new):continue
  assert k in ('sdStarts','sdCounts','sdPageData','sdTextResources','sdAudioModules','sdPageDurations'),k
  assert n>=count and new.split()[:count]==values.split(),('static prefix',k)
  current[name]=replace(current[name],raw,newraw)
 bm=methods(baseline[name]);current[name]=merge(current[name],{n:bm[n] for n in ('hStaticAt','sdLoad','sdPageCount','sdRoute')})
 bm=methods(baseline['module985.sc']);current['module985.sc']=merge(current['module985.sc'],{n:bm[n] for n in ('hStaticCount','hStaticFirst')})
 current['module992.sc']=baseline['module992.sc']
 prior=json.loads((B/'selectors.json').read_text())
 for n,i in prior.items():
  if n in selectors:assert selectors[n]==i
  else:assert i not in selectors.values();selectors[n]=i
 # Validate all remaining differences from inventory baseline are known P08-only methods.
 allowed={'main.sc':{'p02ObjectLocation','uiHostAct'},'module987.sc':set()}
 _,delta=P.patch(baseline.copy())
 for name,names in delta.items():
  a,b=methods(current[name]),methods(baseline[name])
  for n in names:assert a[n]==b[n] or n in allowed.get(name,set()),('unreconciled touched method',name,n)
 current,changed=P.patch(current)
 mapping=json.loads((H/'p10-input/INTEGRATION-DELTA.json').read_text())['mapping']
 assert not set(mapping)&set(selectors) and not set(mapping.values())&set(selectors.values());selectors.update(mapping)
 # Accepted P08 presentation methods and original domain methods remain byte-for-byte.
 for name,source in original.items():
  old,new=methods(source),methods(current[name])
  for n in old:
   if name!='main.sc' and n.startswith(('p03','p04','p05','p06','p07','p08','p09')):assert old[n]==new[n],('domain drift',name,n)
  if name=='module989.sc':
   for n in old:
    if n not in ('h8SaveReady','h8ReserveCloth'):assert old[n]==new[n],('P08 drift',n)
  if name=='module991.sc':assert source==current[name],'renderer drift'
 from gate_b_derive import apply as final_handoff
 current,selectors=final_handoff(current,selectors)
 from p09_active import apply as active_p09
 current,selectors=active_p09(current,selectors)
 from coexistence import apply as coexistence
 current,selectors=coexistence(current,selectors)
 from room_render_fix import apply as room_render_fix
 current=room_render_fix(current)
 for name,source in current.items():
  balanced(source)
  if check:assert (H/'src'/name).read_text()==source
  else:(H/'src'/name).write_text(source)
 if check:assert json.loads((H/'selectors.json').read_text())==selectors
 else:(H/'selectors.json').write_text(json.dumps(selectors,indent=2)+'\n')
 if not check:(H/'COMPOSITION.diff').write_text(''.join(''.join(difflib.unified_diff(original.get(n,'').splitlines(True),s.splitlines(True),fromfile='accepted-reader/'+n,tofile='composed/'+n)) for n,s in sorted(current.items()) if original.get(n)!=s))
 return current,selectors
if __name__=='__main__':derive(check='--check' in sys.argv);print('PASS_GUARDED_CAMPAIGN_COMPOSITION')
