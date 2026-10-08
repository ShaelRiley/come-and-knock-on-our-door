"""A separate voiced intro intent/display authority; silent source checks stay exact."""
from source_tools import methods
from source_derivation import merge,insert,replace

def intro_hooks(output):
 m=methods(output['module989.sc']);h={}
 h['h8SupportedHistory']=replace(m['h8SupportedHistory'],'[p08Words S_ONCE_INTRO] [p08Words (+ S_ONCE_INTRO 1)]','')
 h['h8ReaderRestore']=replace(m['h8ReaderRestore'],'(return (self h8ReaderCheck: 0 0))','(return (and (self h8ReaderCheck: 0 0) (self h8IntroControl: 10 0)))')
 h['h8ReaderRestore']=replace(h['h8ReaderRestore'],'(self h8ReaderRetire: 4)','(self h8ReaderRetire: 4) (if (not (self h8IntroControl: 7 0)) (return 0))')
 h['h8ReaderFrame']=replace(m['h8ReaderFrame'],'(if (== phase 1) (Graph 12 0 0 200 320 1))','(if (== phase 1) (self h8IntroControl: 4 0))\n (if (== phase 0) (self h8IntroControl: 3 0))')
 h['h8ReaderPresented']=insert(m['h8ReaderPresented'],'(self h8IntroControl: 5 0)')
 h['h8ReaderRetire']=insert(m['h8ReaderRetire'],'(self h8IntroControl: 6 reason)')
 h['h8ReaderClosed']=insert(m['h8ReaderClosed'],'(if (and [h8IntroWords 4] (== (h8Host uiDocument?) 973) (== (h8Host bridgeQueueIndex?) (+ [h8IntroWords 5] 1))) (self h8IntroControl: 6 1))')
 h['h8ReaderCheck']=replace(m['h8ReaderCheck'],'(if (== mode 2) (return (and state (== value [h8ReaderWords 2]))))','(if (== mode 2) (return (or (self h8IntroControl: 8 value) (and state (== value [h8ReaderWords 2])))))')
 h['h8ReaderOpen']=insert(m['h8ReaderOpen'],'(if (self h8IntroControl: 8 document) (return (self h8IntroControl: 2 0)))')
 h['h8ReaderAction']=insert(m['h8ReaderAction'],'(if [h8IntroWords 4] (return 0))')
 h['h8RouteTick']=replace(m['h8RouteTick'],'(if save (h8Host writeSave:))','(self h8IntroControl: 9 0) (if save (h8Host writeSave:))')
 h['h8RouteBlock']=insert(m['h8RouteBlock'],'(if (and (== action 6) (== object 8) (not target) (self h8RouteMeeting:) (!= [h8IntroWords 2] 63)) (self h8IntroAction:) (return 1))')
 output['module989.sc']=merge(output['module989.sc'],h)
 return output
