"""E03 ACK-only composition; existing actor publishers stay unchanged."""
from source_tools import methods
from source_derivation import merge,insert,replace

def evening_hooks(output):
 m=methods(output['module989.sc']);h={}
 h['h8EveningCommitted']='(method (h8EveningCommitted) (return (self h8E: 3)))'
 h['h8EveningReady']='(method (h8EveningReady) (return 0))'
 h['h8ActionBarrier']=insert(m['h8ActionBarrier'],'(if [h8EW 0] (return 1))')
 h['h8RouteInput']=insert(m['h8RouteInput'],'(if [h8EW 0] (return (not (and (== (h8Host type?) 4) (or (== (h8Host message?) 15360) (== (h8Host message?) 15616))))))')
 h['h8SaveReady']=replace(m['h8SaveReady'],'(self h8ActionBarrier:)', '(or (self h8Barrier:) (and (not [h8EW 0]) (self h8ActionBarrier:)))')
 h['h8SupportedHistory']='(method (h8SupportedHistory &tmp i)\n (if (or [p08Words S_HINT_LEVEL] (not (self h8E: 2))) (return 0))\n (if (not [h8EW 0])\n  (if (or [p08Words S_ONCE_EVENING] [p08Words (+ S_ONCE_EVENING 1)]) (return 0))\n  (for ((= i S_COMPLETED_REQUEST_SERIAL)) (< i S_SOURCE_CIRCULATION_PLAN) ((++ i)) (if [p08Words i] (return 0))))\n (return (self h8ReaderRestore: 0)))'
 h['h8RestoreBegin']=replace(m['h8RestoreBegin'],'(= p (h8Host p03?))', '(if (not (self h8E: 2)) (return (self h8RestoreReject:)))\n (= p (h8Host p03?))')
 h['h8RouteTick']=insert(m['h8RouteTick'],'(if (self h8E: 0) (return 1))\n (if [h8EW 0] (return 1))')
 h['h8S']=replace(m['h8S'],'(if (== cmd 5)', '(if (== cmd 5) (self h8E: 5))\n (if (== cmd 5)')
 h['h8S']=replace(h['h8S'],'(if (not h8Restoring) (return 0))', '(if (not h8Restoring) (return 0)) (self h8E: 5)')
 act=m['h8RAct']
 act=replace(act,'(if (and (== op 3) (== [h8R 0] 3))', '(if (and (== op 3) (== [h8R 0] 3) (== [h8IO 0] 4)) (return (self h8E: 1)))\n (if (and (== op 3) (== [h8R 0] 3))')
 h['h8RAct']=act
 for name in ('h8RCtl','h8LayoutMenu'):
  h[name]=m[name].replace('(!= [h8IO 0] 3)', '(not (or (== [h8IO 0] 3) (and (== [h8IO 0] 4) [h8EC 2])))')
 output['module989.sc']=merge(output['module989.sc'],h)
 return output
