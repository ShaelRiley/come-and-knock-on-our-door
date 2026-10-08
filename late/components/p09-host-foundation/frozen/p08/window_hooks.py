"""Exact additive SceneDialogue window hooks; no table or full-record identity change."""
from pathlib import Path
from source_tools import methods
from source_derivation import merge,insert,replace,append_locals
ROOT=Path(__file__).resolve().parent

def window_hooks(output):
    source=output['module982.sc']
    assert source==(ROOT/'inputs/window-basis/module982.sc').read_text(),'scene basis differs'
    mm=methods(source);hooks=methods((ROOT/'templates/window982.sc.in').read_text())
    assert not set(hooks)&set(mm)
    hooks['sdOpen']=insert(mm['sdOpen'],'(= [sdWindowBounds 0] 0) (= [sdWindowBounds 1] 0)')
    hooks['sdLoad']=insert(mm['sdLoad'],'''(if (or (< (self sdWindowValue: 2) 0)
 (and (self sdWindowValue: 2) (or (< sdPage (self sdWindowValue: 0))
  (>= sdPage (+ (self sdWindowValue: 0) (self sdWindowValue: 1)))))) (= sdFailure 6) (return 0))''')
    turn=insert(mm['sdTurn'],'(if (< (self sdWindowValue: 2) 0) (= sdFailure 6) (return 0))')
    turn=replace(turn,'(= wanted (+ sdPage delta))','''(= wanted (+ sdPage delta))
 (if (self sdWindowValue: 2)
  (if (and (> delta 0) (> delta (- (- (+ (self sdWindowValue: 0) (self sdWindowValue: 1)) 1) sdPage)))
   (= wanted (- (+ (self sdWindowValue: 0) (self sdWindowValue: 1)) 1)))
  (if (and (< delta 0) (< delta (- (self sdWindowValue: 0) sdPage))) (= wanted (self sdWindowValue: 0))))''')
    turn=replace(turn,'(if (< wanted 0) (= wanted 0))','(if (< wanted (self sdWindowValue: 0)) (= wanted (self sdWindowValue: 0)))')
    turn=replace(turn,'(if (>= wanted sdCount) (= wanted (- sdCount 1)))','(if (>= wanted (+ (self sdWindowValue: 0) (self sdWindowValue: 1))) (= wanted (- (+ (self sdWindowValue: 0) (self sdWindowValue: 1)) 1)))')
    hooks['sdTurn']=turn
    for name in ('sdControlAction','sdBuildControls'):
        body=replace(mm[name],'(> sdPage 0)','(> sdPage (self sdWindowValue: 0))')
        body=replace(body,'(< sdPage (- sdCount 1))','(< sdPage (- (+ (self sdWindowValue: 0) (self sdWindowValue: 1)) 1))')
        hooks[name]=body
    hooks['sdDraw']=replace(mm['sdDraw'],'(Format @sdCounter "%d/%d" (+ sdPage 1) sdCount)',
        '(Format @sdCounter "%d/%d" (+ (- sdPage (self sdWindowValue: 0)) 1) (self sdWindowValue: 1))')
    hooks['sdClose']=replace(mm['sdClose'],'(= sdActive 0)','(= sdActive 0) (= [sdWindowBounds 0] 0) (= [sdWindowBounds 1] 0)')
    restore=replace(mm['sdAfterRestore'],'(self sdInterrupt: audio 14)', '''(self sdInterrupt: audio 14)
 (if (or (< (self sdWindowValue: 2) 0)
  (and (self sdWindowValue: 2) (or (not sdActive) (!= sdCount (self sdPageCount: sdDocument)))))
  (= sdFailure 6) (= sdActive 0) (return 0))''')
    hooks['sdAfterRestore']=restore
    output['module982.sc']=merge(append_locals(source,'[sdWindowBounds 2]'),hooks)
    for name,body in mm.items():
        if name not in hooks:assert methods(output['module982.sc'])[name]==body
    return output
