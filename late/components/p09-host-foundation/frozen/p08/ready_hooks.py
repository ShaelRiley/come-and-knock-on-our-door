"""Additive request/display hooks; final consent and storage are later gates."""
from source_tools import methods
from source_derivation import merge,insert,replace

def ready_hooks(output):
 m=methods(output['module989.sc']);h={}
 h['h8SupportedHistory']=replace(m['h8SupportedHistory'],'[p08Words S_PENDING_PHASE]','')
 h['h8SupportedHistory']=replace(h['h8SupportedHistory'],'(= i S_REQUEST_SERIAL)','(= i S_COMPLETED_REQUEST_SERIAL)')
 h['h8ReaderRestore']=replace(m['h8ReaderRestore'],'(self h8IntroControl: 10 0)','(self h8IntroControl: 10 0) (self h8RCtl: 10 0)')
 h['h8ReaderRestore']=replace(h['h8ReaderRestore'],'(if (not (self h8IntroControl: 7 0)) (return 0))','(if (not (self h8IntroControl: 7 0)) (return 0)) (if (not (self h8RCtl: 7 0)) (return 0))')
 h['h8ReaderFrame']=replace(m['h8ReaderFrame'],'(if (== phase 1) (self h8IntroControl: 4 0))','(if (== phase 1) (if [h8R 12] (self h8RCtl: 4 0) else (self h8IntroControl: 4 0)))')
 h['h8ReaderFrame']=replace(h['h8ReaderFrame'],'(if (== phase 0) (self h8IntroControl: 3 0))','(if (== phase 0) (self h8IntroControl: 3 0) (self h8RCtl: 3 0))')
 h['h8ReaderPresented']=insert(m['h8ReaderPresented'],'(self h8RCtl: 5 0)')
 h['h8ReaderRetire']=insert(m['h8ReaderRetire'],'(self h8RCtl: 6 reason)')
 h['h8ReaderClosed']=insert(m['h8ReaderClosed'],'(self h8RCtl: 9 0)')
 h['h8ReaderCheck']=replace(m['h8ReaderCheck'],'(self h8IntroControl: 8 value)','(self h8RCtl: 8 value) (self h8IntroControl: 8 value)')
 h['h8ReaderOpen']=insert(m['h8ReaderOpen'],'(if (self h8RCtl: 8 document) (return (self h8RCtl: 2 0)))')
 for name in ('h8ReaderAction','h8IntroAction'):
  h[name]=insert(m[name],'(if [h8R 0] (if [h8R 12] (return 0)) (if (not (self h8RAct: 2)) (return 0)))')
 h['h8UIRun']=insert(m['h8UIRun'],'(if [h8R 12] (return 0))')
 h['h8CommitReserved']=replace(m['h8CommitReserved'],'(return 1))','(return (self h8RCtl: 11 0)))')
 for name in ('h8LayoutRetire','h8LayoutMenu','h8LayoutChoice','h8LayoutRestore'):
  h[name]=m[name].replace('(> context 235)', '(> context 237)').replace('(> [h8UI 1] 235)', '(> [h8UI 1] 237)').replace('(<= (h8Host uiChoiceContext?) 235)', '(<= (h8Host uiChoiceContext?) 237)')
 menu=h['h8LayoutMenu'];menu=replace(menu,'(= count (if (== context 235)', '(= count (if (== context 237) 2 else (if (== context 236) 1 else (if (== context 235)')
 menu=replace(menu,'6 else 5)))))','6 else 5)))))))')
 menu=replace(menu,'(switch context','(switch context\n   (237 (= label (self h8RCtl: 0 i)))\n   (236 (= label "WE\'RE READY TO START."))')
 menu=replace(menu,'(h8Host uiAddChoice: id label 0 1)','(h8Host uiAddChoice: id label 0 (if (and (== context 237) (== [h8R 0] 3) (== i 1)) 0 else 1))')
 h['h8LayoutMenu']=menu
 h['h8LayoutChoice']=replace(h['h8LayoutChoice'],'(switch context','(switch context\n  (237 (if (<= value 2) (self h8RAct: (if (== value 1) 3 else 4))))\n  (236 (if (== value 1) (self h8RAct: 0)))')
 h['h8LayoutChoice']=replace(h['h8LayoutChoice'],'(self h8LayoutRetire:)','(if (== context 237) (= [h8C 8] 1) (= mask (self h8RCtl: 13 value)) (= [h8C 8] 0) (if (not mask) (return 1))) (self h8LayoutRetire:)')
 h['h8RouteTick']=insert(m['h8RouteTick'],'(if (not (self h8RouteBusy:)) (self h8RCtl: 12 0))')
 h['h8RouteBlock']=insert(m['h8RouteBlock'],'(if (and (== action 6) (== object 8) (not target) (self h8RouteMeeting:) [p08Words S_LAYOUT_READY]) (if (>= [h8R 0] 2) (self h8RAct: 5) else (self h8LayoutMenu: 236 8 6)) (return 1))')
 output['module989.sc']=merge(output['module989.sc'],h)
 m=methods(output['main.sc']);h={}
 for name in ('uiBuildFocus','uiTurnPage','uiRender'):
  if 'ldi 235' in m[name]:h[name]=replace(m[name],'ldi 235','ldi 237')
 output['main.sc']=merge(output['main.sc'],h)
 return output
