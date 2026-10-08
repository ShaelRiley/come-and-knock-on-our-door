"""Guarded P09 activation over the current fourteen-module Gate B universe."""
from pathlib import Path
import json,hashlib
from source_tools import methods
from source_derivation import merge,insert,replace,append_locals,balanced
H=Path(__file__).resolve().parent
NAMES=['h9Context','h9StateValid','h9ReaderCheck','h9Open','h9Topics','h9Choice','h9Draw','h9Frame','h9Closed','h9Restore','h9Hint','h9Continue']
def apply(output,selectors):
 pin=json.loads((H/'P09-ACTIVE-BASE.json').read_text())
 assert {n:hashlib.sha256(s.encode()).hexdigest() for n,s in output.items()}==pin['sources'],'P09 current universe drift'
 original=output.copy();before={n:methods(s) for n,s in output.items()}
 template=(H/'p09_active.sc.in').read_text();balanced(template);hooks=methods(template)
 for n,i in zip(NAMES,range(3176,3200)):
  assert n not in selectors and i not in selectors.values(),(n,i)
  selectors[n]=i
 assert set(hooks)==set(NAMES)|{'h9Active','h9Dispatch'}
 output['module990.sc']=append_locals(merge(output['module990.sc'],hooks), '[h9R 7] [h9F 16] [h9Q 7] [h9Choice4 64] [h9Choice6 64] [h9Choice7 64] [h9Choice8 64]')
 m=methods(output['module990.sc']);hooks={}
 hooks['h9SaveReady']=insert(m['h9SaveReady'],'(self h9Frame: 3) (if (not (self h9StateValid:)) (return 0))')
 hooks['h9RestoreCard']=insert(m['h9RestoreCard'],'(if (not (self h9Restore: phase)) (return 0))')
 # Restore context rebind occurs only after both owners have admitted physical inventory.
 hooks['h9RestoreCard']=replace(hooks['h9RestoreCard'],'(if (not (self h9Restore: phase)) (return 0))','(if (== phase 2) (self h9Closed:) else (if (not (self h9Restore: 0)) (return 0)))')
 hooks['h9RestoreCard']=replace(hooks['h9RestoreCard'],'(= [h9CardAdmission 0] 1) (return 1))','(= [h9CardAdmission 0] 1) (return (self h9Restore: 1)))')
 output['module990.sc']=merge(output['module990.sc'],hooks)
 m=methods(output['module982.sc']);hooks={}
 for n in ('sdControlAction','sdBuildControls'):
  old='(< sdPage (- (+ (self sdWindowValue: 0) (self sdWindowValue: 1)) 1))'
  hooks[n]=replace(m[n],old,'(or '+old+' ((ScriptID 990 0) h9Continue: 0 0))')
 output['module982.sc']=merge(output['module982.sc'],hooks)
 m=methods(output['main.sc']);hooks={}
 hooks['campaignReachable']=replace(m['campaignReachable'],'(if (and (>= obj 395) (<= obj 399)) (return 0))','''(if (and (>= obj 395) (<= obj 399))
 (return (and p09 (p09 h9Active:) (not onApron) (if (== obj 399) (p09 h9CardHeld: 399) else (== location 6)))))''')
 hooks['uiTurnPage']=insert(m['uiTurnPage'],'(if (and p09 (p09 h9Continue: 1 arg1)) (return 0))')
 hooks['uiHostChoice']=insert(m['uiHostChoice'],'(if (and p09 (p09 h9Choice: context id)) (return 0))')
 hooks['p03PreparationHint']=insert(m['p03PreparationHint'],'(if (and p09 (p09 h9Hint:)) (return 0))')
 hooks['uiHostClosed']=insert(m['uiHostClosed'],'(if p09 (p09 h9Closed:))')
 hooks['render']=replace(m['render'],'(if p08 (p08 h8ReaderFrame: 0))','(if p08 (p08 h8ReaderFrame: 0))\n(if p09 (p09 h9Frame: 0))')
 hooks['render']=replace(hooks['render'],'''            H8_reader_flush_done: ldi 0
            aTop dirty
            ret''','''            H8_reader_flush_done: ldi 0
            aTop dirty
            pToa p09
            bnt H9_frame_done
            pushi #h9Frame
            push1
            push1
            pToa p09
            send 6
            H9_frame_done: ret''')
 hooks['drawWorld']=replace(m['drawWorld'],'(if (and p08 (>= (p08 h8V: 1 0) 5)) (p08 h8VD:) (return 1))','(if (and p08 (>= (p08 h8V: 1 0) 5)) (if p09 (return (p09 h9Draw:)) else (p08 h8VD:) (return 1)))')
 output['main.sc']=merge(output['main.sc'],hooks)
 # The old pure domains and repaired P10 owner are never rewritten.
 assert output['module992.sc']==original['module992.sc']
 for name,old in before.items():
  new=methods(output[name])
  for n,s in old.items():
   if n.startswith(('p03','p04','p05','p06','p07','p08','p09')) and name!='main.sc':assert new[n]==s,(name,n)
 assert before['module989.sc']==methods(output['module989.sc'])
 return output,selectors
