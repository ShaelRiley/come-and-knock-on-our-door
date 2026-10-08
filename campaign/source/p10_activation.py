"""Additive P10 playable controls and owner-bound whole-page receipts."""
from pathlib import Path
import json
from source_tools import methods
from source_derivation import merge,insert,replace,append_locals
H=Path(__file__).resolve().parent
NAMES=['h10Active','h10Dispatch','h10Menu','h10Choice','h10Open','h10Frame','h10Retire','h10Controls','h10Label','h10ContextMatch','h10ReaderCheck']
def apply(o,s):
 records=json.loads((H/'p10-input/generated/line-document-map.json').read_text())
 assert len(records)==23 and all(v['document_id']==1199+v['local_line_key'] for v in records.values())
 for i,n in enumerate(NAMES,3367):
  assert n not in s and i not in s.values(),(n,i)
  s[n]=i
 m=methods(o['module992.sc']);patch=methods((H/'p10_active.sc.in').read_text())
 patch['h10Q']=replace(m['h10Q'],'(= cue (self p10CueIndex: obj))\n (if (and (< cue 0)', '''(if (and (or (== obj 410) (== obj 411)) (self h10Active:))
  (if (== mode 2) (return 4))
  (if (== mode 3) (return (and (== ((ScriptID 0 0) location?) 4) (not ((ScriptID 0 0) onApron?))))))
 (= cue (self p10CueIndex: obj))
 (if (and (< cue 0)''')
 patch['h10Q']=replace(patch['h10Q'],'(if (== mode 3) (return 0)) ; Physical/action activation is a later gate.', '(if (== mode 3) (return (and (self h10Active:) (or (< (self p10RackIndex: obj) 0) (== (h location?) 4)))))')
 patch['h10Stop']='(method (h10Stop obj target) (return (and (not (self h10Active:)) (or (!= (self h10Q: 0 obj) -2) (!= (self h10Q: 0 target) -2)))))'
 patch['h10Load']=insert(m['h10Load'],'(self h10Retire:)')
 o['module992.sc']=append_locals(merge(o['module992.sc'],patch),'[h10Reader 16] [h10PendingAction 7] [h10Selected 1]')
 m=methods(o['main.sc']);p={}
 for n in ('hostActNow','uiHostAct'):
  p[n]=insert(m[n],'(if ((ScriptID 992 0) h10Frame: 3) (return 0))')
 p['bridgeActAtArrival']=insert(m['bridgeActAtArrival'],'(if ((ScriptID 992 0) h10Dispatch: action obj target) (return 0))')
 p['uiHostChoice']=insert(m['uiHostChoice'],'(if ((ScriptID 992 0) h10Choice: context id) (return 0))')
 p['uiHostClosed']=insert(m['uiHostClosed'],'((ScriptID 992 0) h10Retire:)')
 p['writeSave']=insert(m['writeSave'],'((ScriptID 992 0) h10Retire:)')
 p['uiHostWorldControls']=replace(m['uiHostWorldControls'],'(return 1))','((ScriptID 992 0) h10Controls:) (return 1))')
 p['render']=insert(m['render'],'((ScriptID 992 0) h10Frame: 0)')
 p['render']=replace(p['render'],'H8_reader_flush_done: ldi 0\n            aTop dirty', '''H8_reader_flush_done: ldi 0\n            aTop dirty\n            pushi #h10Frame
            push1
            push1
            push2
            pushi 992
            push0
            callk ScriptID, 4
            send 6
            ''')
 p['drawWorld']=replace(m['drawWorld'],'(if (and p08 (>= (p08 h8V: 1 0) 5)) (p08 h8VD:) (return 1))', '(if (and p08 (>= (p08 h8V: 1 0) 5)) (if (p08 h8VD:) ((ScriptID 992 0) h10Frame: 2)) (return 1))')
 for n in ('uiHostItemLabel','uiHostShortLabel'):
  p[n]=insert(m[n],'(if (and p08 (== (p08 h8V: 1 0) 6) (or (== arg1 410) (== arg1 411) (>= ((ScriptID 992 0) p10CueIndex: arg1) 0))) (return ((ScriptID 992 0) h10Label: arg1)))')
 for n,value in [('approachX',200),('approachY',110),('uiHostDefaultVerb',5)]:
  p[n]=insert(m[n],f'(if (or (== arg1 410) (== arg1 411)) (return {value}))')
 p['p03BuildTopics']=replace(m['p03BuildTopics'],'(return 1))','(if (and (== actor 30) ((ScriptID 992 0) h10Active:)) (self uiAddChoice: 120 "Discuss the ceramic cues" 0 1)) (return 1))')
 p['p04BuildJournal']=m['p04BuildJournal'][:-1]+'(if (and ((ScriptID 992 0) h10Active:) ((ScriptID 992 0) p10Ready:)) (self uiAddChoice: 105 "Restored cue order" 0 1)))'
 o['main.sc']=merge(o['main.sc'],p)
 return o,s
