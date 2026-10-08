"""Final-world access layer over the verified phase-5 publication checkpoint."""
from pathlib import Path
from source_tools import methods
from source_derivation import merge,insert,replace,append_locals
H=Path(__file__).resolve().parent

def apply(output):
 m=methods(output['module989.sc']);hooks={}
 # Phase6 is an earned ordinary-frame handoff. Restore preserves historical completion and refreshes only a separate live binding.
 for name in ('h8VA','h8VC','h8V','h8ReaderFrame','h8GB','h8RouteValid'):
  hooks[name]=m[name].replace('(== [h8VP 0] 5)','(>= [h8VP 0] 5)').replace('(!= [h8VP 0] 5)','(< [h8VP 0] 5)')
 hooks['h8V']=replace(hooks['h8V'],'(if (not h8Restoring) (return 0)) (self h8V: 4 0)',
  '(if (not h8Restoring) (return 0)) (self h8V: 4 0)\n  (if (and (== [h8VP 0] 6) (not ((ScriptID 991 0) h8GB: h8Host self 3))) (return 0))')
 hooks['h8V']=replace(hooks['h8V'],'(return (self h8VR: 3 0)))',
  '(if (== [h8VP 0] 6) (= [h8GL 0] [h8VP 2]) (= [h8GL 1] [h8VP 3]) (= [h8GL 2] h8Lease)) (return (self h8VR: 3 0)))')

 # Completed validated handoff no longer owns the ordinary movement/stage clock.
 hooks['h8RouteTick']=insert(m['h8RouteTick'],'(if (and (== [h8VP 0] 6) (self h8VC: 1)) (return 0))')
 hooks['h8GB']=(H/'gate_b_templates/final-access.sc.in').read_text()
 hooks['h8EveningReady']='(method (h8EveningReady) (return (self h8GB: 1)))'
 hooks['h8ActionBarrier']=replace(m['h8ActionBarrier'],'(if [h8EW 0] (return 1))','(if (and [h8EW 0] (not (and (== [h8VP 0] 6) (self h8VC: 1)))) (return 1))')
 hooks['h8VI']=insert(m['h8VI'],'(if (and (== cmd 0) (== [h8VP 0] 6) (self h8VC: 1) (not (self h8GlobalBarrier:))) (return 0))')
 for name in ('h8RouteTravel','h8RouteBlock','h8RouteMeeting','h8RouteRender','h8RouteCanSpeak','h8LayoutInput','h8RouteChoice'):
  hooks[name]=insert(m[name],'(if (self h8GB: 9) (return 0))')
 hooks['h8RouteValid']=replace(hooks['h8RouteValid'],'(not (self h8RouteFacts:))','(and (not (self h8GB: 9)) (not (self h8RouteFacts:)))')
 hooks['h8RouteValid']=replace(hooks['h8RouteValid'],'(!= (h8Host location?) 4)','(and (not (self h8GB: 9)) (!= (h8Host location?) 4))')
 hooks['h8RouteValid']=hooks['h8RouteValid'].replace('(and (< [h8VP 0] 5) (!= (self h8RouteRoom:', '(and (not (self h8GB: 9)) (!= (self h8RouteRoom:')
 hooks['h8LayoutControls']=replace(m['h8LayoutControls'],'(if [h8VP 0] (return (self h8VI: 2 0 0 0)))', '''(if (>= [h8VP 0] 5)
  (if (and (== (h8Host location?) 4) (not (h8Host onApron?)))
   (h8Host uiAddControl: 1 28 61 13 125 56 "MILO")
   (h8Host uiAddControl: 1 85 61 271 125 314 "VIVIAN")) (return 0))
 (if [h8VP 0] (return (self h8VI: 2 0 0 0)))''')
 hooks['h8E']=replace(m['h8E'],'(if (== cmd 3) (return 1))','(if (== cmd 3) (return 1))\n (if (>= [h8VP 0] 5) (return (self h8VC: 0)))')
 hooks['h8VD']=replace(m['h8VD'], '(if (and result (== [h8VP 0] 3)', '(if (and result (>= [h8VP 0] 5) (== [h8VF 0] 6)) (= [h8VF 12] 42))\n (if (and result (== [h8VP 0] 3)')
 hooks['h8ReaderClosed']=insert(m['h8ReaderClosed'],'(if (>= [h8VP 0] 5) (self h8GB: 7) (return 1))')
 # Read-only archive projection is separate from the captured live-reader mask.
 hooks['h8V']=insert(hooks['h8V'],'(if (== cmd 18) (if (or (< value 0) (>= value 3)) (return -1)) (return [h8GA value]))\n (if (== cmd 19) (if (or (< value 0) (>= value 14)) (return -1)) (return [h8GO value]))\n (if (== cmd 20) (if (or (< value 0) (>= value 3)) (return -1)) (return [h8GL value]))')
 output['module989.sc']=append_locals(merge(output['module989.sc'],hooks),'[h8GA 3] [h8GO 14] [h8GL 3]')
 m=methods(output['module988.sc']);output['module988.sc']=merge(output['module988.sc'],{'h7PhysicalValid':m['h7PhysicalValid'].replace('(== ((h7Host p08?) h8V: 1 0) 5)','((h7Host p08?) h8GB: 9)')})
 m=methods(output['module985.sc']);s=m['hStageActive'];s=replace(s,'(== (hHost location?) 5)','(== (hHost location?) hMiloRoom)');s=replace(s,'(== hMiloRoom 5)','(or (== hMiloRoom 5) (and (== hMiloRoom 4) (hHost p08?) ((hHost p08?) h8VA: 5)))');output['module985.sc']=merge(output['module985.sc'],{'hStageActive':s})
 m=methods(output['module987.sc']);hooks={}
 hooks['h6Control']=insert(m['h6Control'],'(if (and (== object 85) (!= (h6Host location?) h6VivianRoom)) (return 0))')
 output['module987.sc']=merge(output['module987.sc'],hooks)
 m=methods(output['main.sc']);hooks={}
 hooks['drawWorld']=insert(m['drawWorld'],'(if (and p08 (>= (p08 h8V: 1 0) 5)) (p08 h8VD:) (return 1))')
 hooks['dialogueCanSpeak']=replace(m['dialogueCanSpeak'],'(if (and p08 (p08 h8V: 1 0))','(if (and p08 (> (p08 h8V: 1 0) 0) (< (p08 h8V: 1 0) 5))')
 hooks['dialogueCanSpeak']=insert(hooks['dialogueCanSpeak'],'(if (and p08 (>= (p08 h8V: 1 0) 5) (or (== uiDocument 1013) (== uiDocument 1017))) (return 0))')
 hooks['p04BuildJournal']=replace(m['p04BuildJournal'],'(if p06 (self uiAddChoice: 102 "Vivian: screen observations" 0 1))','''(if p06 (self uiAddChoice: 102 "Vivian: screen observations" 0 1))
(if (and p08 (>= (p08 h8V: 1 0) 5))
 (self uiAddChoice: 103 "Evening archive: the system note" 0 1)
 (self uiAddChoice: 104 "Evening archive: what everyone said" 0 1))''')
 hooks['uiHostChoice']=insert(m['uiHostChoice'],'(if (and p08 (== context 208) (or (== id 103) (== id 104)) (>= (p08 h8V: 1 0) 5)) (p08 h8GB: id) (return 0))')
 output['main.sc']=merge(output['main.sc'],hooks)
 m=methods(output['module991.sc']);s=m['h8GB']
 s=s.replace('(== (controller h8V: 10 0) 5)','(>= (controller h8V: 10 0) 5)').replace('(!= (controller h8V: 10 0) 5)','(or (< (controller h8V: 10 0) 5) (> (controller h8V: 10 0) 6))')
 s=replace(s,'(!= (owner location?) 4) (owner onApron?) (owner motionPhase?)','(< (owner location?) 0) (> (owner location?) 6)')
 s=replace(s,'(if (or (owner bridgeReaderActive?) (!= (owner bridgeQueueCount?) (owner bridgeQueueIndex?))) (return 0))','')
 a='(!= (owner motionX?) 16000)';b='(owner motionApron?)) (return 0)))';start=s.index(a);end=s.index(b,start)+len(b);s=s[:start]+'(not (or (== (controller h8V: 10 0) 5) (== (controller h8V: 10 0) 6)))) (return 0)))'+s[end:]
 s=insert(s,'''(if (or (< (controller h8V: 18 0) 0) (> (controller h8V: 18 0) 31)
  (not (or (== (controller h8V: 18 1) 0) (== (controller h8V: 18 1) 1013) (== (controller h8V: 18 1) 1017)))
  (and (!= (controller h8V: 18 1) 1017) (controller h8V: 18 2))
  (< (controller h8V: 18 2) 0) (> (controller h8V: 18 2) 3)) (return 0))''')
 # Distinct raw final-owner authority mode ignores transient proof buffers.
 anchor=' (return (and (== mode 1)';assert s.count(anchor)==1;s=s.replace(anchor,' (if (or (== mode 2) (== mode 3)) (return 1))\n'+anchor)
 s=insert(s,'''(if (!= mode 2) (if (== (controller h8V: 10 0) 5)
  (for ((= i 0)) (< i 14) ((++ i)) (if (controller h8V: 19 i) (return 0)))
  (for ((= i 0)) (< i 3) ((++ i)) (if (controller h8V: 20 i) (return 0)))
 else
  (if (or (!= (controller h8V: 19 0) 1)
   (controller h8SerialBefore: (controller h8V: 10 2) (controller h8V: 10 3) (controller h8V: 19 1) (controller h8V: 19 2))
   (controller h8SerialBefore: (controller h8V: 19 1) (controller h8V: 19 2) (controller h8V: 15 2) (controller h8V: 15 3))
   (< (controller h8V: 19 3) 1) (> (controller h8V: 19 3) 2)
   (!= (controller h8V: 20 0) (controller h8V: 10 2)) (!= (controller h8V: 20 1) (controller h8V: 10 3))
   (!= (controller h8V: 20 2) (if (== mode 3) (if (== (controller h8Lease?) 1) 2 else 1) else (controller h8Lease?)))
   (!= (controller h8V: 19 4) (controller h8V: 15 2)) (!= (controller h8V: 19 5) (controller h8V: 15 3))
   (!= (controller h8V: 19 6) (controller h8V: 14 39)) (!= (controller h8V: 19 7) (controller h8V: 14 40))
   (!= (controller h8V: 19 8) (controller h8V: 16 31))
   (< (controller h8V: 19 9) 0) (> (controller h8V: 19 9) 6)
   (< (controller h8V: 19 10) 0) (> (controller h8V: 19 10) 1)
   (< (controller h8V: 19 11) 0) (> (controller h8V: 19 11) 20480)
   (< (controller h8V: 19 12) 0) (> (controller h8V: 19 12) 12800)
   (!= (controller h8V: 19 13) 42)) (return 0))))''')
 s=insert(s,'(if (and (== mode 3) (or (!= (controller h8Restoring?) 1) (controller h8RestoreValid?) (controller h8Enabled?))) (return 0))')
 # Archive identity checker is the canonical read-only descriptor validator, independent of actor presence.
 archive=m['h8VR'];archive=archive[:archive.index(' (if (== mode 0)')]+ ' (return 1))\n'
 archive=replace(archive,'(method (h8VR owner controller mode speaker','(method (h8VI owner controller')
 archive=replace(archive,'(!= (controller h8V: 10 0) 3)','(< (controller h8V: 10 0) 5)')
 archive=replace(archive,'(= doc (controller h8V: 10 5))','(= doc (controller h8V: 18 1))')
 draw=insert(m['h8VD'],(H/'gate_b_templates/final-draw.sc.in').read_text())
 guard='(if (or (!= self (ScriptID 991 0)) (!= controller (ScriptID 989 0))) (return 0))\n (if (!= owner (controller h8Host?)) (return 0))'
 s=insert(s,guard);archive=insert(archive,guard);draw=insert(draw,guard)
 output['module991.sc']=merge(output['module991.sc'],{'h8GB':s,'h8VI':archive,'h8VD':draw})
 return output
