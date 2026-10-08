#!/usr/bin/env python3
"""Guarded additive closed P10 original-cue ownership seam."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,re
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H/'tools')]
from source_tools import methods
from source_derivation import balanced

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def require(v,*s):
 if not v:raise RuntimeError(s)
def verify_inputs():
 require(not sys.flags.optimize,'Optimized Python forbidden')
 pins=json.loads((H/'INPUT-MANIFEST.json').read_text())
 actual={str(p.relative_to(H)) for d in ('frozen','toolchain','references') for p in (H/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 require(actual==set(pins),'Immutable membership changed')
 for n,v in pins.items():require(sha(H/n)==v,'Immutable bytes changed',n)
 m=json.loads((H/'toolchain/SOURCE-MANIFEST.json').read_text());require(m['publication_revision']==2 and len(m['files'])==198,'Approved compiler closure')
 for n,v in m['files'].items():require(sha(H/'toolchain/source'/n)==v,'Compiler closure bytes',n)
def once(s,old,new):require(s.count(old)==1,'Expected unique hook',old);return s.replace(old,new)
def first(s,name,code):
 m=methods(s)[name];at=m.index('\n');return once(s,m,m[:at+1]+code+'\n'+m[at+1:])
def end(s,name,code):
 m=methods(s)[name];at=m.rfind('(return ');require(at>=0,'Missing final return',name);return once(s,m,m[:at]+code+' '+m[at:])
def patch(source):
 old=source.copy();m=source['main.sc'];p=source['module983.sc'];q=source['module984.sc'];s=source['module989.sc'];n=source['module990.sc'];d=source['module992.sc'];t=source['module987.sc']
 # Preserve the requested page until the complete late tail has been rebuilt.
 # Earlier owners legitimately expose a smaller intermediate roster.
 for owner,names,host in (("m",("p02HostInventory","h6PublishNative"),"self"),("p",("bInventory",),"h"),("q",("qInventory",),"h")):
  text={"m":m,"p":p,"q":q}[owner]
  for name in names:
   before=methods(text)[name];after=before
   if '&tmp' in after:after=after.replace('&tmp ','&tmp h10Page ',1)
   else:after=after.replace(name+')',name+' &tmp h10Page)',1)
   at=after.index(')')+1
   after=after[:at]+(' (= h10Page uiInventoryPage)' if host=='self' else f' (= h10Page ({host} uiInventoryPage?))')+after[at:]
   text=once(text,before,after)
  if owner=="m":m=text
  elif owner=="p":p=text
  else:q=text
 # Main queries use -2 exclusively as not-owned sentinel; old maps stay bounded.
 for name,mode in [('campaignHeld',1),('campaignReachable',3),('p02ObjectLocation',2)]:
  before=methods(m)[name];after=before
  if '&tmp' in after:after=after.replace('&tmp ','&tmp h10Answer ',1)
  else:after=after.replace('obj)','obj &tmp h10Answer)',1)
  at=after.index('\n');after=after[:at+1]+f'(= h10Answer ((ScriptID 992 0) h10Q: {mode} obj)) (if (!= h10Answer -2) (return h10Answer))\n'+after[at+1:];m=once(m,before,after)
 for name in ('uiHostAct','hostActNow'):m=first(m,name,'(if ((ScriptID 992 0) h10Stop: arg2 arg3) (return 0))')
 # Final publication hooks, also reached by direct P03/P04 and P06 publishers.
 m=end(m,'p02HostInventory','(if (not ((ScriptID 992 0) h10Proj:)) (= uiFailure 10) (return 0))')
 m=end(m,'h6PublishNative','(if (and p09 (not (p09 h9ProjectCard:))) (return 0)) (if (not ((ScriptID 992 0) h10Proj:)) (return 0))')
 for name,args in [('uiInventoryAdd','item'),('uiInventoryRemove','item'),('uiInventoryCombine','first second combined'),('uiInventoryCompact','')]:
  before=methods(m)[name];m=once(m,before,f'(method ({name} {args}) (return ((ScriptID 992 0) {name}: self {args})))')
 ui='''(method (h10UI index obj)
 (if (or (< index 0) (>= index 64) (< obj 0) (== obj 35)
  (and (> obj 94) (!= obj 399) (< ((ScriptID 992 0) p10CueIndex: obj) 0))) (return 0))
 (if (and (>= ((ScriptID 992 0) p10CueIndex: obj) 0) (!= ((ScriptID 992 0) h10Q: 1 obj) 1)) (return 0))
 (= [uiItems index] obj) (return 1))'''
 m=once(m,'\n)\n(class Sound','\n'+ui+'\n)\n(class Sound')
 # Genuine grant stays in literal P03; only legacy bridge presentation is retired.
 for name,mode in [('bHeld',1),('bReachable',3)]:
  before=methods(p)[name];after=before.replace('h obj)','h obj &tmp result)',1);at=after.index('\n');after=after[:at+1]+f'(= result ((ScriptID 992 0) h10Q: {mode} obj)) (if (!= result -2) (return result))\n'+after[at+1:];p=once(p,before,after)
 for name in ('bAppend','b8Append'):p=first(p,name,'(if (!= ((ScriptID 992 0) h10Q: 0 obj) -2) (return 1))')
 p=first(p,'bDispatch','(if ((ScriptID 992 0) h10Stop: obj target) (self bCancelPending:) (return 1))')
 p=first(p,'bPresented','(if ((ScriptID 992 0) h10Stop: bPendingObject 0) (self bCancelPending:) (return 0))')
 p=end(p,'bInventory','(if (and (h p09?) (not ((h p09?) h9ProjectCard:))) (= bFailure 3) (return 0)) (if (not ((ScriptID 992 0) h10Proj:)) (= bFailure 3) (return 0))')
 # Direct q rebuild ignores foreign late originals instead of indexing qReserve.
 q=once(q,'(if (and obj (self qHeld: h obj)) (self qAppend: obj))','(if (and obj (<= obj 62) (== ((ScriptID 992 0) h10Q: 0 obj) -2) (self qHeld: h obj)) (self qAppend: obj))')
 q=end(q,'qInventory','(if (and (h p09?) (not ((h p09?) h9ProjectCard:))) (= qFailure 3) (return 0)) (if (not ((ScriptID 992 0) h10Proj:)) (= qFailure 3) (return 0))')
 # P09's high-ID compatibility check is leaf-only, never P10 whole-inventory.
 for name in ('h9InventoryValid','h9ProjectCard'):
  before=methods(n)[name];after=once(before,'(and (> obj 94) (!= obj 399))','(and (> obj 94) (!= obj 399) (!= ((ScriptID 992 0) h10Q: 1 obj) 1))');n=once(n,before,after)
 before=methods(n)['h9ProjectCard'];after=once(before,'(if (or (>= extent 64)',
  '(if ((ScriptID 992 0) h10Q: 5 [h9CardSlot 0]) (if (> (+ extent ((ScriptID 992 0) h10Q: 6 0)) 63) (return 0)) (if (not ((ScriptID 992 0) h10Proj:)) (return 0)) (= extent (h9Host uiInventoryExtent?)))\n (if (or (>= extent 64)');n=once(n,before,after)
 n=first(n,'h9Init','(if (not ((ScriptID 992 0) h10Init:)) (return 0))')
 n=first(n,'h9Dispatch','(if ((ScriptID 992 0) h10Stop: obj target) (return 1))')
 n=first(n,'h9SaveReady','(if (not ((ScriptID 992 0) h10Save:)) (return 0))')
 n=first(n,'h9RestoreCard','(if (== phase 0) (= [h9CardRestoreSlot 0] [h9CardSlot 0]))\n(if (not ((ScriptID 992 0) h10Load: phase)) (= [h9CardAdmission 0] 0) (return 0))\n(if (== phase 1) (= [h9CardSlot 0] [h9CardRestoreSlot 0]))')
 before=methods(n)['h9RestoreCard'];after=once(before,'(not (self h9SaveReady:))','(not (and (== [h9CardAdmission 0] 1) (self h9InventoryValid:)))');n=once(n,before,after)
 n=once(n,'[h9CardAdmission 1] = [1]','[h9CardAdmission 1] = [1] [h9CardRestoreSlot 1] = [-1]')
 # Both manual and automatic checkpoint I/O must see the ownership admission.
 s=first(s,'h8SaveReady','(if (not ((ScriptID 992 0) h10Save:)) (return 0))')
 before=methods(t)['h6ReserveInventory'];after=once(before,'(and (!= obj 75) (!= obj 76))','(and (!= obj 75) (!= obj 76) (not ((ScriptID 992 0) h10Q: 4 i)))');t=once(t,before,after)
 # Predict exactly the final card+six-cue layer in the existing cloth transaction.
 before=methods(s)['h8ReserveCloth'];after=once(before,'(= high [h8ClothHistory 0])','''(if (not ((ScriptID 992 0) h10Save:)) (return 0))
 (if (and ((ScriptID 990 0) h9CardHeld: 399) (not ((ScriptID 992 0) h10Q: 5 ((ScriptID 990 0) h9CardReservation: 399))))
  (if (>= extent 64) (return 0)) (= [h8InventorySlots extent] 399) (++ extent))
 (if (or (p p03Ready?) ((ScriptID 992 0) p10Present: 2))
  (if (> (+ extent 6) 64) (return 0))
  (for ((= i 0)) (< i 6) ((++ i)) (= obj ((ScriptID 992 0) p10CueAt: i))
   (= [h8InventorySlots extent] (if (== ((ScriptID 992 0) h10Q: 1 obj) 1) obj else 0)) (++ extent)))
 (if (and ((ScriptID 990 0) h9CardHeld: 399) ((ScriptID 992 0) h10Q: 5 ((ScriptID 990 0) h9CardReservation: 399)))
  (if (>= extent 64) (return 0)) (= [h8InventorySlots extent] 399) (++ extent))
 (= high [h8ClothHistory 0])''');s=once(s,before,after)
 # Restore only a page which exists in the completed roster. Selection remains
 # untouched unless the existing owner logic proves its original no longer held.
 for owner,names,host in (("m",("p02HostInventory","h6PublishNative"),"self"),("p",("bInventory",),"h"),("q",("qInventory",),"h")):
  text={"m":m,"p":p,"q":q}[owner]
  for name in names:text=end(text,name,'(if (and (>= h10Page 0) (< h10Page uiInventoryPages)) (= uiInventoryPage h10Page))' if host=='self' else f'(if (and (>= h10Page 0) (< h10Page ({host} uiInventoryPages?))) ({host} uiInventoryPage: h10Page))')
  if owner=="m":m=text
  elif owner=="p":p=text
  else:q=text
 d=once(d,'[p10Lease 8])','[p10Lease 8] '+(H/'patch/locals.inc').read_text()+')')
 d=once(d,'\n)\n(instance p10State','\n'+(H/'patch/cue-host.inc').read_text()+'\n)\n(instance p10State')
 source.update({'main.sc':m,'module983.sc':p,'module984.sc':q,'module989.sc':s,'module990.sc':n,'module992.sc':d,'module987.sc':t})
 for name,text in source.items():balanced(text)
 for owner,prefix in [('module983.sc','p03'),('module984.sc','p04'),('module987.sc','p06'),('module989.sc','p08'),('module990.sc','p09'),('module992.sc','p10')]:
  a,b=methods(old[owner]),methods(source[owner])
  for name in a:
   if name.startswith(prefix):require(a[name]==b[name],'Literal accepted domain drift',owner,name)
 changed={name:[key for key,v in methods(old[name]).items() if v!=methods(source[name])[key]] for name in sorted(old) if old[name]!=source[name]}
 return source,changed

def derive(check=False,pre=False):
 verify_inputs();F=H/'frozen/baseline';old={p.name:p.read_text() for p in (F/'src').glob('*.sc')};source,changed=patch(old.copy())
 selectors=json.loads((F/'selectors.json').read_text());mapping=json.loads((H/'references/P10-OWNERSHIP-HOST-SELECTOR-RESERVATION-20261007.json').read_text())['reserved_names']
 new={name for text in source.values() for name in methods(text) if name not in selectors};require(new==set(mapping),'New method census',new,set(mapping));require(not set(mapping.values())&set(selectors.values()),'Selector collision');selectors.update(mapping)
 for name,text in source.items():(H/'src'/name).write_text(text)
 dump(H/'selectors.json',selectors)
 dump(H/'INTEGRATION-DELTA.json',dict(baseline_source='frozen/baseline',baseline_compile_sha256=sha(F/'build/coherent/compile-receipt.json'),mapping=mapping,new_selector_count=len(mapping),vocabulary_added_bytes=sum(len(n)+2 for n in mapping),main_growth_ceiling=256,changed_methods=changed,domain_methods_literal=True,active_p09=False,active_p10=False,evening_ready=False))
 return source,selectors
if __name__=='__main__':derive();print('PASS_P10_CUE_DERIVATION')
