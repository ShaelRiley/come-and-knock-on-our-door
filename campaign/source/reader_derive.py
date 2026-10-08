#!/usr/bin/env python3
"""P08 presentation delta over the frozen coherent ACK/P09/991 foundation."""
from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent;sys.dont_write_bytecode=True;sys.path.insert(0,str(H/'tools'))
from source_tools import methods,tokens
from source_derivation import merge,append_locals,insert,replace,balanced
from foundation_derive import derive as foundation

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

def derive(check=False,pre=False,emit=True):
 if pre:raise RuntimeError('Use frozen foundation for its pre-extraction oracle')
 output,selectors=foundation(emit=False)
 m=methods(output['module989.sc']);hooks={}
 additions={}
 for p in sorted((H/'templates').glob('*.sc.in')):
  body=p.read_text();names=check_method_template(body)
  if set(names)&set(additions):raise RuntimeError('Duplicate cross-template method')
  additions.update(methods(body))
 assert not set(additions)&set(m)
 output['module989.sc']=append_locals(output['module989.sc'],'[h8VP 16] [h8VF 32] [h8VS 24] [h8Rooms 2] = [6 6] [h8VT 16]')
 hooks['h8ReaderMap']='(method (h8ReaderMap kind id field) (return ((ScriptID 991 0) h8ReaderMap: kind id field)))'
 hooks['h8ActorRoom']=m['h8ActorRoom'].replace('(4 (return 6))','(4 (return [h8Rooms 0]))').replace('(7 (return 6))','(7 (return [h8Rooms 1]))')
 assert hooks['h8ActorRoom']!=m['h8ActorRoom']
 hooks['h8RouteTick']=insert(m['h8RouteTick'],'(if (self h8V: 0 0) (return 1))')
 hooks['h8SupportedHistory']=insert(m['h8SupportedHistory'],'(if (not (self h8VC: 0)) (return 0))')
 hooks['h8RestoreBegin']=replace(m['h8RestoreBegin'],'(if (not (self h8E: 2))', '(if (not (self h8VC: 0)) (return (self h8RestoreReject:)))\n (if (not (self h8E: 2))')
 hooks['h8RouteRetire']=insert(m['h8RouteRetire'],'(self h8V: 4 0)')
 hooks['h8RouteSave']=insert(m['h8RouteSave'],'(self h8V: 4 0)')
 hooks['h8ReaderRestore']=replace(m['h8ReaderRestore'],'(if (not (self h8S: 4)) (return 0))','(if (not (self h8S: 4)) (return 0)) (if (not (self h8V: 5 0)) (return 0))')
 hooks['h8ReaderFrame']=insert(m['h8ReaderFrame'],'(if (>= [h8VP 0] 2) (return (self h8VF: (+ phase 1))))')
 hooks['h8ReaderPresented']=insert(m['h8ReaderPresented'],'(if (>= [h8VP 0] 2) (if (== [h8VP 0] 3) (return (self h8VF: 3))) (return 0))')
 hooks['h8ReaderClosed']=insert(m['h8ReaderClosed'],'(if (>= [h8VP 0] 2) (self h8VR: 2 0) (return 1))')
 hooks['h8RouteInput']=replace(m['h8RouteInput'],'(if [h8EW 0] (return (not (and (== (h8Host type?) 4) (or (== (h8Host message?) 15360) (== (h8Host message?) 15616))))))','(if [h8EW 0] (return (self h8VI: 0 0 0 0)))')
 hooks['h8LayoutControls']=insert(m['h8LayoutControls'],'(if [h8VP 0] (return (self h8VI: 2 0 0 0)))')
 hooks['h8RouteControls']=insert(m['h8RouteControls'],'(if [h8VP 0] (return 0))')

 e=m['h8E'];key='(for ((= i 0)) (< i 8) ((++ i)) (if (!= [h8EW (+ 23 i)] (self h8ActorRoom: (+ i 1))) (return 0)))'
 assert key in e;e=e.replace(key,'(if (< [h8VP 0] 2) '+key+')\n (if (not (self h8VC: 0)) (return 0))')
 hooks['h8E']=e
 hooks['h8LayoutRender']=replace(m['h8LayoutRender'],'(or (self h8LayoutActive:)', '(or (and [h8VP 0] (self h8VC: 1)) (self h8LayoutActive:)')
 output['module989.sc']=merge(output['module989.sc'],{**hooks,**additions})
 mm=methods(output['main.sc']);hooks={}
 hooks['render']=insert(mm['render'],'(if (and p08 (p08 h8VF: 0)) (= dirty 0) (return 0))')
 hooks['drawWorld']=insert(mm['drawWorld'],'(if (and p08 (p08 h8V: 1 0)) (p08 h8VD:) (return 1))')
 hooks['p02ObjectLocation']=insert(mm['p02ObjectLocation'],'(if (and p08 (or (== obj 29) (== obj 30))) (return (p08 h8ActorRoom: (if (== obj 29) 4 else 7))))')
 hooks['neighborPerson']=insert(mm['neighborPerson'],'(if (and p08 (== who 4) (!= location (p08 h8ActorRoom: 4))) (return 0))') if '(neighborPerson who)' in mm['neighborPerson'] else insert(mm['neighborPerson'],'(if (and p08 (== arg1 4) (!= location (p08 h8ActorRoom: 4))) (return 0))')
 hooks['p03Rita']=insert(mm['p03Rita'],'(if (and p08 (!= location (p08 h8ActorRoom: 7))) (return 0))')
 hooks['dialogueCanSpeak']=insert(mm['dialogueCanSpeak'],'(if (and p08 (p08 h8V: 1 0)) (return (p08 h8VR: 6 who)))')
 for name,command in [('dialoguePresented',7),('speechPoll',9),('uiClose',8)]:
  hooks[name]=replace(mm[name],'(if (and p08 (p08 h8ActionBarrier:)) (return 0))',f'(if (and p08 (p08 h8ActionBarrier:) (not (p08 h8VR: {command} 0))) (return 0))')
 hooks['uiHostAct']=insert(mm['uiHostAct'],'(if (and p08 (p08 h8VI: 1 arg1 arg2 arg3)) (return 0))')
 hooks['uiActivate']=insert(mm['uiActivate'],'(if (and p08 (p08 h8VI: 4 arg1 0 0)) (return 0))')
 hooks['uiInput']=insert(mm['uiInput'],'(if (and p08 (p08 h8VI: 5 0 0 0)) (return 1))')
 hooks['uiTurnPage']=insert(mm['uiTurnPage'],'(if (and p08 (p08 h8VR: 14 arg1)) (return 0))')
 hooks['h8VI']='(method (h8VI index field) (if (or (< index 0) (>= index uiControlCount)) (return -1)) (switch field (0 (return [uiActions index])) (1 (return [uiPayloads index]))) (return -1))'

 output['main.sc']=merge(output['main.sc'],hooks)
 dm=methods(output['module982.sc']);dh={}
 dh['sdBuildControls']=replace(dm['sdBuildControls'],'(for ((= i 0)) (< i sdControls) ((++ i))\n            (= action', '(if ((ScriptID 989 0) h8VR: 16 0) (= sdControls 4))\n        (for ((= i 0)) (< i sdControls) ((++ i))\n            (= action')
 dh['sdControlAction']=insert(dm['sdControlAction'],'(if ((ScriptID 989 0) h8VR: 16 0) (switch index (0 (return 11)) (1 (return 16)) (2 (return 17)) (3 (return 12))) (return 0))')
 output['module982.sc']=merge(output['module982.sc'],dh)
 pm=methods(output['module987.sc']);owned=replace(pm['h6OwnersValid'],'(!= h6VivianRoom 0)','(not (or (and (== h6VivianRoom 0) (or (not (h6Host p08?)) (< ((h6Host p08?) h8V: 1 0) 2))) (and (h6Host p08?) ((h6Host p08?) h8VA: 6))))')
 output['module987.sc']=merge(output['module987.sc'],{'h6OwnersValid':owned})
 renderer_additions={}
 for p in sorted((H/'renderer_templates').glob('*.sc.in')):
  body=p.read_text();names=check_method_template(body)
  if set(names)&set(renderer_additions):raise RuntimeError('Duplicate renderer helper')
  renderer_additions.update(methods(body))
 assert not set(renderer_additions)&set(methods(output['module991.sc']))
 output['module991.sc']=merge(output['module991.sc'],renderer_additions)

 for n,i in {'h8V':2992,'h8VC':2993,'h8VD':2994,'h8VF':2995,'h8VR':2996,'h8VA':2997,'h8VI':2998}.items():
  assert n not in selectors and i not in selectors.values();selectors[n]=i
 for n,s in output.items():
  balanced(s)
  if check:assert (H/'src'/n).read_text()==s,n
  elif emit:(H/'src'/n).write_text(s)
 if check:assert json.loads((H/'selectors.json').read_text())==selectors
 elif emit:(H/'selectors.json').write_text(json.dumps(selectors,indent=2)+'\n')
 return output,selectors
if __name__=='__main__':derive('--check' in sys.argv);print('PASS_P08_PRESENTATION_DERIVATION')
