"""Guarded attempt staging/restore composition; native kernel service comes next."""
from source_tools import methods
from source_derivation import merge,insert,replace

def storage_hooks(output):
 m=methods(output['module989.sc']);h={}
 h['h8RChk']=insert(m['h8RChk'],'(if (not (self h8S: 3)) (return 0))')
 act=m['h8RAct']
 act=replace(act,'(= h8Critical 1) (= [h8UI 7] 1)','(if (and (== op 3) (not (self h8S: 7))) (return 0))\n (= h8Critical 1) (= [h8UI 7] 1)')
 act=replace(act,'(if (not (self h8CommitReserved:)) (= [h8UI 7] 0) (= h8Critical 0) (return 0))','(if (and (== op 3) (not (self h8S: 1)))\n  (if p08Busy (self p08Abort:)) (= h8Prepared 0) (= [h8UI 7] 0) (= [h8UI 16] 0) (= h8Critical 0) (return 0))\n (if (not (self h8CommitReserved:)) (= [h8UI 7] 0) (= h8Critical 0) (return 0))')
 act=replace(act,'(= [h8C 9] 0) (= result (self h8RChk: 0))','(if (and (== op 3) (not (self h8S: 2))) (= [h8UI 7] 0) (= h8Critical 0) (return 0))\n (= [h8C 9] 0) (= result (self h8RChk: 0))')
 # A direct op6 call is rejected; only the consumed real Yes can select retry.
 act=insert(act,'(if (or (== [h8IO 0] 2) (== op 6)) (return 0))')
 act=replace(act,'(if (and (== op 4) (== [h8R 0] 3))','(if (and (== op 3) (== [h8R 0] 3)) (if (!= [h8IO 0] 3) (return 0)) (= op 6))\n (if (and (== op 4) (== [h8R 0] 3))')
 act=replace(act,'(> op 4)','(> op 6)')
 act=replace(act,'(= fresh (not [h8R 0]))','(if (and (== op 6) (or (!= [h8R 0] 3) (!= [h8IO 0] 3) [h8R 12] (h8Host uiPanel?))) (return 0))\n (= fresh (not [h8R 0]))')
 act=replace(act,'(switch op','(switch op\n  (6 (= code (self p08RetryAutosave: [h8R 3] [h8R 4])) (= result CODE_AUTOSAVE_REQUESTED) (= count 0))')
 act=act.replace('(and (== op 3) (not (self h8S:', '(and (or (== op 3) (== op 6)) (not (self h8S:')
 h['h8RAct']=act
 h['h8RCtl']=replace(m['h8RCtl'],'(for ((= i 0)) (< i 8) ((++ i)) (= [h8CP i] 0)) (= [h8C 9] 0)','(for ((= i 0)) (< i 8) ((++ i)) (= [h8CP i] 0)) (= [h8C 9] 0) (self h8S: 5)')
 h['h8ReaderRestore']=replace(m['h8ReaderRestore'],'(if (not (self h8RCtl: 7 0)) (return 0))','(if (not (self h8RCtl: 7 0)) (return 0)) (if (not (self h8S: 4)) (return 0))')
 h['h8RCtl']=h['h8RCtl'].replace('(and (== [h8R 0] 3) (== value 1))','(and (== [h8R 0] 3) (== value 1) (!= [h8IO 0] 3))').replace('(and (== [h8R 0] 3) (== i 0))','(and (== [h8R 0] 3) (== i 0) (!= [h8IO 0] 3))')
 h['h8LayoutMenu']=m['h8LayoutMenu'].replace('(and (== context 237) (== [h8R 0] 3) (== i 1))','(and (== context 237) (== [h8R 0] 3) (== i 1) (!= [h8IO 0] 3))')
 h['h8ActionBarrier']=insert(m['h8ActionBarrier'],'(if (== [h8IO 0] 2) (return 1))')
 h['h8RouteTick']=insert(m['h8RouteTick'],'(if (and (not (self h8RouteBusy:)) (self h8S: 0)) (return 1))')
 output['module989.sc']=merge(output['module989.sc'],h)
 main=methods(output['main.sc']);output['main.sc']=merge(output['main.sc'],{'readSave':insert(main['readSave'],'(if (and p08 (p08 h8S: 8)) (return 0))')})
 return output
