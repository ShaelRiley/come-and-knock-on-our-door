#!/usr/bin/env python3
"""Guarded additive P08 host assembly from reviewed editable sources."""
from pathlib import Path
import sys,json,hashlib,subprocess
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'tools'))
from source_tools import methods,tokens
from source_derivation import merge,append_properties,append_locals,balanced,insert,replace

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check_method_template(source):
 ts=tokens(source);depth=0;names=[]
 for i,t in enumerate(ts):
  value=t.group()
  if depth==0:
   if value!='(' or i+3>=len(ts) or ts[i+1].group()!='method' or ts[i+2].group()!='(':
    raise RuntimeError('Non-method or orphan template expression')
   names.append(ts[i+3].group())
  if value=='(':depth+=1
  elif value==')':depth-=1
  if depth<0:raise RuntimeError('Unbalanced method template')
 if depth:raise RuntimeError('Unbalanced method template')
 if len(set(names))!=len(names):raise RuntimeError('Duplicate template method')
 if set(names)!=set(methods(source)):raise RuntimeError('Unparsed template method')
 return names

def derive(check=False):
 if sys.flags.optimize:raise RuntimeError('Optimized Python forbidden')
 inputs=json.loads((H/'SOURCE-INPUTS.json').read_text())
 actual={str(p.relative_to(H)) for folder in ('inputs','snapshot/resources','toolchain') for p in (H/folder).rglob('*') if p.is_file()}
 if actual!=set(inputs):raise RuntimeError('Immutable input inventory changed')
 subprocess.run([sys.executable,'-B',str(H/'generate_routes.py'),'--check'],check=True)
 subprocess.run([sys.executable,'-B',str(H/'generate_geometry.py'),'--check'],check=True)
 subprocess.run([sys.executable,'-B',str(H/'generate_cutaways.py'),'--check'],check=True)
 subprocess.run([sys.executable,'-B',str(H/'generate_reader_map.py'),'--check'],check=True)
 for name,digest in inputs.items():
  if sha(H/name)!=digest:raise RuntimeError('Immutable input changed '+name)
 for template in (H/'templates').glob('*.sc.in'):check_method_template(template.read_text())
 output={}
 for p in (H/'inputs/scene/src').glob('*.sc'):output[p.name]=p.read_text()
 from composition_hooks import composition_base
 output=composition_base(output)
 domain=(H/'inputs/domain/module989.sc').read_text();original=methods(domain)
 added=methods((H/'templates/host.sc.in').read_text()+'\n'+(H/'templates/cloth989.sc.in').read_text()+'\n'+(H/'templates/restore989.sc.in').read_text()+'\n'+(H/'templates/routes.sc.in').read_text()+'\n'+(H/'templates/geometry989.sc.in').read_text()+'\n'+(H/'templates/presentation989.sc.in').read_text()+'\n'+(H/'templates/layout989.sc.in').read_text()+'\n'+(H/'templates/rendezvous989.sc.in').read_text()+'\n'+(H/'templates/cutaway989.sc.in').read_text()+'\n'+(H/'templates/reader-map989.sc.in').read_text()+'\n'+(H/'templates/reader989.sc.in').read_text()+'\n'+(H/'templates/intro989.sc.in').read_text()+'\n'+(H/'templates/ready989.sc.in').read_text())
 if set(original)&set(added):raise RuntimeError('Domain method replacement')
 domain=append_locals(domain,(H/'templates/host-locals.inc').read_text())
 domain=append_properties(domain,(H/'templates/host-properties.inc').read_text())
 domain=merge(domain,added)
 if any(methods(domain)[name]!=value for name,value in original.items()):raise RuntimeError('Domain method changed')
 output['module989.sc']=domain
 # Add only the root reference and exact later-owner guards. No active player dispatch yet.
 output['main.sc']=append_properties(output['main.sc'],'p08 0')
 mm=methods(output['main.sc']);hooks={}
 for name in sorted({name for name,body in mm.items() if 'hBarrier:' in body}|{'bridgeActAtArrival','hostActNow','uiHostAct','uiHostChoice','uiHostConfirm','dialoguePresented','uiClose','speechPoll'}):
  hooks[name]=insert(mm[name],'(if (and p08 (p08 h8ActionBarrier:)) (return 0))')
 hooks['writeSave']=insert(mm['writeSave'],'(if (and p08 (not (p08 h8SaveReady:))) (return 0))')
 hooks['readSave']=insert(mm['readSave'],'(if (and p08 (or (p08 h8Critical?) (p08 h8Restoring?))) (return 0)) (if (and p08 (or (p08 h8Failure?) (not (p08 h8RestoreValid?)))) (return (p08 h8Recover:)))')
 output['main.sc']=merge(output['main.sc'],hooks)
 mm=methods(output['main.sc']);hooks={}
 hooks['p04Initialize']=mm['p04Initialize'][:-1]+'\n(= p08 (ScriptID 989 0)) (if (not (p08 h8Init: self)) (p08 h8Uncertain:))\n)'
 hooks['p05RestoreBegin']=insert(mm['p05RestoreBegin'],'(= p08 (ScriptID 989 0)) (if (or (not p08) (not (p08 h8RestoreBegin: self))) (return 0))')
 restore=replace(mm['p05RestoreValidate'],'(return 1)','(if (and p08 (not (p08 h8RestoreFinish:))) (self p05RestoreReject:) (return 0)) (return 1)')
 restore=replace(restore,'(if p07 (p07 h7RestoreValid: 0)) (return 0))','(if p07 (p07 h7RestoreValid: 0)) (if p08 (p08 h8RestoreReject:)) (return 0))')
 hooks['p05RestoreValidate']=restore
 hooks['p05RestoreReject']=insert(mm['p05RestoreReject'],'(if p08 (p08 h8RestoreReject:))')
 hooks['bridgeActAtArrival']=replace(mm['bridgeActAtArrival'],'(if (and p06 (p06 h6Dispatch: action obj target))','(if (and p08 (p08 h8Dispatch: action obj target)) (return 0))\n(if (and p06 (p06 h6Dispatch: action obj target))')
 hooks['p02ObjectLocation']=insert(mm['p02ObjectLocation'],'(if (and p08 (p08 h8OwnedNative: obj)) (return (p08 h8NativeLocation: obj)))')
 hooks['campaignHeld']=insert(mm['campaignHeld'],'(if (and p08 (p08 h8HandlesCloth: obj)) (return (p08 h8ClothHeld: obj)))')
 controls=mm['p03KitchenControls']
 for obj,key,rect in [(34,1,'54 214 81 256'),(36,1,'54 216 64 252'),(40,5,'63 260 83 282')]:
  call=f'(self uiAddControl: 1 {obj} {rect} (self p03Label: {obj}))'
  controls=replace(controls,call,f'(if (or (not p08) (not (p08 h8Owns: {key}))) {call})')
 hooks['p03KitchenControls']=controls
 render=mm['drawKitchen']
 for key,call in [(1,'(DrawCel 224 0 1 215 55 -1 0)'),(5,'(DrawCel 224 0 4 261 64 -1 0)')]:
  render=replace(render,call,f'(if (or (not p08) (not (p08 h8Owns: {key}))) {call})')
 hooks['drawKitchen']=render[:-1]+'\n(if p08 (p08 h8RenderCloth:))\n)'
 hooks['uiHostWorldControls']=replace(mm['uiHostWorldControls'],'(return 1)','(if p08 (p08 h8ClothControls:)) (return 1)')
 for method,value in [('approachX',139),('approachY',130)]:
  hooks[method]=insert(mm[method],f'(if (and p08 (== location 2) (p08 h8ClothTarget: arg1)) (return {value}))')
 # Narrow layout hooks; all state, geometry and publication remain in989.
 hooks['h6BaseDrawWorld']=insert(mm['h6BaseDrawWorld'],'(if (and p08 (p08 h8LayoutRender:)) (return 0))')
 hooks['h6BaseControls']=insert(mm['h6BaseControls'],'(if (and p08 (p08 h8LayoutControls:)) (return 0))')
 hooks['campaignReachable']=insert(mm['campaignReachable'],'(if (and p08 (p08 h8LayoutTarget: obj)) (return 1))')
 hooks['p02ObjectLocation']=insert(hooks['p02ObjectLocation'],'(if (and p08 (p08 h8LayoutTarget: obj)) (return 4))')
 hooks['uiHostItemLabel']=insert(mm['uiHostItemLabel'],'(if (and p08 (>= arg1 116) (<= arg1 122)) (return (p08 h8LayoutLabel: arg1)))')
 hooks['uiHostShortLabel']=insert(mm['uiHostShortLabel'],'(if (and p08 (>= arg1 116) (<= arg1 122)) (return (p08 h8LayoutLabel: arg1)))')
 hooks['uiChooseObject']=insert(mm['uiChooseObject'],'(if (and p08 (p08 h8LayoutFirst: item uiVerb uiNounA)) (return 0))')
 hooks['uiHostChoice']=insert(mm['uiHostChoice'],'(if (and p08 (p08 h8LayoutChoice: context id)) (return 0))')
 hooks['uiClose']=insert(mm['uiClose'],'(if p08 (p08 h8LayoutRetire:))')
 for method,axis in [('approachX',0),('approachY',1)]:
  hooks[method]=insert(hooks[method],f'(if (and p08 (p08 h8LayoutTarget: arg1)) (return (p08 h8LayoutApproach: arg1 {axis})))')
 for method in ['uiBuildFocus','uiTurnPage','uiRender']:
  if method not in mm:continue
  if 'ldi 228' in mm[method]:hooks[method]=replace(mm[method],'ldi 228','ldi 234')
 output['main.sc']=merge(output['main.sc'],hooks)
 # Only P03 bridge projection changes; all p03 domain methods stay exact.
 bridge=output['module983.sc'];original03=methods(bridge);bm={}
 bm['bHeld']=insert(original03['bHeld'],'(if (and (h p08?) ((h p08?) h8HandlesCloth: obj)) (return ((h p08?) h8ClothHeld: obj)))')
 bm['bReachable']=insert(original03['bReachable'],'(if (and (h p08?) ((h p08?) h8OwnedNative: obj)) (return ((h p08?) h8NativeReachable: obj)))')
 marker='(for ((= i 0)) (< i 3) ((++ i)) (self bAppend: (self p03InventoryAt: i)))'
 bm['bInventory']=replace(original03['bInventory'],marker,marker+'\n(if (and (h p08?) ((h p08?) h8ClothHeld: ((h p08?) h8OriginalCloth:))) (self bAppend: ((h p08?) h8OriginalCloth:)))')
 bm.update(methods((H/'templates/cloth983.sc.in').read_text()))
 bridge=append_locals(bridge,'[b8Slots 64] [b8Reservations 51]');bridge=append_properties(bridge,'b8Extent 0 b8Prepared 0')
 output['module983.sc']=merge(bridge,bm)
 if any(methods(output['module983.sc'])[n]!=body for n,body in original03.items() if n.startswith('p03')):raise RuntimeError('P03 historical method drift')
 bridge=append_locals(output['module984.sc'],'[q8Slots 64] [q8Reservations 63]');bridge=append_properties(bridge,'q8Extent 0 q8Prepared 0')
 output['module984.sc']=merge(bridge,methods((H/'templates/cloth984.sc.in').read_text()))
 old=methods(output['module985.sc'])
 guarded=replace(old['hPhysicalValid'],'(!= hPAOwner 1)','(not (or (== hPAOwner 1) (and (hHost p08?) ((hHost p08?) h8PAOwnerValid:))))')
 output['module985.sc']=merge(output['module985.sc'],{'hPhysicalValid':guarded,'hBarrier':insert(old['hBarrier'],'(if (and hHost (hHost p08?) ((hHost p08?) h8GlobalBarrier:)) (return 1))')})
 old=methods(output['module987.sc'])
 guarded=replace(old['h6OwnersValid'],"(!= h6ScreenOwner 1)\n  (!= h6ScreenPosition 0) (!= h6ScreenRoom (if (self p06LiveNZ: S_COMPLETE) 4 else 0))","(not (or (and (== h6ScreenOwner 1) (== h6ScreenPosition 0) (== h6ScreenRoom (if (self p06LiveNZ: S_COMPLETE) 4 else 0))) (and (h6Host p08?) ((h6Host p08?) h8ScreenOwnerValid:))))")
 output['module987.sc']=merge(output['module987.sc'],{'h6OwnersValid':guarded,'h6Barrier':insert(old['h6Barrier'],'(if (and h6Host (h6Host p08?) ((h6Host p08?) h8GlobalBarrier:)) (return 1))')})
 for method in ['h6Controls','h6Render']:
  output['module987.sc']=merge(output['module987.sc'],{method:insert(old[method],'(if (and (h6Host p08?) ((h6Host p08?) h8LayoutActive:)) (return 0))')})
 old=methods(output['module988.sc'])
 output['module988.sc']=merge(output['module988.sc'],{'h7Barrier':insert(old['h7Barrier'],'(if (and h7Host (h7Host p08?) ((h7Host p08?) h8GlobalBarrier:)) (return 1))')})
 from route_hooks import route_hooks
 output=route_hooks(output)
 from composition_hooks import composition_hooks
 output=composition_hooks(output)
 from window_hooks import window_hooks
 output=window_hooks(output)
 from reader_hooks import reader_hooks
 output=reader_hooks(output)
 from intro_hooks import intro_hooks
 output=intro_hooks(output)
 from ready_hooks import ready_hooks
 output=ready_hooks(output)
 selectors=json.loads((H/'inputs/base/selectors.json').read_text())
 for name,value in json.loads((H/'inputs/domain/selectors.json').read_text()).items():
  if name in selectors and selectors[name]!=value:raise RuntimeError(('Selector drift',name))
  if name not in selectors and value in selectors.values():raise RuntimeError(('Selector collision',name,value))
  selectors[name]=value
 host_selectors=json.loads((H/'HOST-SELECTORS.json').read_text())
 for name,value in host_selectors.items():
  if not 2800<=value<=2999 or name in selectors or value in selectors.values():raise RuntimeError(('Host reservation',name,value))
  selectors[name]=value
 for name,source in output.items():
  balanced(source)
  needed=set(methods(source))
  import re
  for props in re.findall(r'\(properties\s+([^)]*)\)',source):needed.update([t.group() for t in tokens(props)][::2])
  if needed-selectors.keys():raise RuntimeError(('Unallocated selector',needed-selectors.keys()))
  path=H/'src'/name
  if check:
   if not path.exists() or path.read_text()!=source:raise RuntimeError('Derived source drift '+name)
  else:path.write_text(source)
 blob=json.dumps(selectors,indent=2)+'\n'
 if check:
  if (H/'selectors.json').read_text()!=blob:raise RuntimeError('Selector drift')
 else:(H/'selectors.json').write_text(blob)
 if {p.name for p in (H/'src').glob('*.sc')}!=set(output):raise RuntimeError('Unexpected source module')
 print('PASS_P08_GUARDED_DERIVATION',len(output),'modules',len(original),'preserved domain methods')
if __name__=='__main__':derive('--check' in sys.argv)
