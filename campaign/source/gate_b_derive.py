"""Guarded Gate B publication checkpoint. Final readiness remains disabled."""
from pathlib import Path
from source_tools import methods
from source_derivation import merge,insert,replace
H=Path(__file__).resolve().parent

def apply(output,selectors):
 m=methods(output['module989.sc']);hooks={}
 hooks['h8VA']=insert(m['h8VA'],'''(if (== [h8VP 0] 5)
  (return (and (== [h8VP 15] 1) (== [h8VP 13] [h8VT 2]) (== [h8VP 14] [h8VT 3])
   (== [h8Rooms 0] 6) (== [h8Rooms 1] 6) (self h8E: 3)
   (or (and (== actor 4) (== [h8Rooms 0] 6)) (and (== actor 7) (== [h8Rooms 1] 6))
    (and (== actor 5) (== ((h8Host p05?) hMiloRoom?) 4))
    (and (== actor 6) (== ((h8Host p06?) h6VivianRoom?) 4))))))''')
 hooks['h8VC']=insert(m['h8VC'],'''(if (== [h8VP 0] 5) (return ((ScriptID 991 0) h8GB: h8Host self mode)))''')
 old='(if (and (== [h8VF 0] 2) (not (self h8VF: 4))) (self h8V: 4 0) (h8Host dirty: 1)) (return 1))'
 hooks['h8V']=replace(m['h8V'],old,'(return (self h8GB: 0)))')
 hooks['h8V']=replace(hooks['h8V'],'(if (>= [h8VP 0] 2) (self h8VR: 0 0) (return 1))','(if (== [h8VP 0] 5) (return 1))\n (if (>= [h8VP 0] 2) (self h8VR: 0 0) (return 1))')
 hooks['h8ReaderFrame']=insert(m['h8ReaderFrame'],'(if (== [h8VP 0] 5) (return (self h8GB: (+ phase 2))))')
 # Historical meeting ownership transfers to final owners without rewriting invitation history.
 route=m['h8RouteValid']
 route=replace(route,'(!= (self h8RouteRoom: actor) (self h8RoutePoint: actor node 0))','(and (!= [h8VP 0] 5) (!= (self h8RouteRoom: actor) (self h8RoutePoint: actor node 0)))')
 hooks['h8RouteValid']=route
 hooks['h8GB']=(H/'gate_b_templates/final-owner.sc.in').read_text()
 output['module989.sc']=merge(output['module989.sc'],hooks)
 # P07's invitation records are historical; final kitchen presence is not a new invitation.
 m=methods(output['module988.sc']);s=m['h7PhysicalValid']
 s=replace(s,'(!= h7BunnyInvited (if (or','(and (not (and (h7Host p08?) (== ((h7Host p08?) h8V: 1 0) 5))) (!= h7BunnyInvited (if (or')
 s=replace(s,'(h7Controller p05SaveWord: 69)))) 1 else 0))','(h7Controller p05SaveWord: 69)))) 1 else 0)))')
 output['module988.sc']=merge(output['module988.sc'],{'h7PhysicalValid':s})
 # Keep ordinary final-frame drawing distinct from the staging overlay. This checkpoint remains input locked.
 m=methods(output['main.sc']);s=m['drawWorld']
 s=replace(s,'(if (and p08 (p08 h8V: 1 0))','(if (and p08 (> (p08 h8V: 1 0) 0) (< (p08 h8V: 1 0) 5))')
 output['main.sc']=merge(output['main.sc'],{'drawWorld':s})
 # Reuse the validated immutable-request contract, with final physical destinations.
 m=methods(output['module991.sc']);s=m['h8VC']
 s=replace(s,'(method (h8VC owner controller mode','(method (h8GB owner controller mode')
 s=replace(s,'(if (== (controller h8V: 10 0) 4)','(if (== (controller h8V: 10 0) 5)')
 s=replace(s,'(controller h8V: 10 13) (controller h8V: 10 14) (controller h8V: 10 15)', '''(!= (controller h8V: 10 13) (controller h8V: 15 2))
  (!= (controller h8V: 10 14) (controller h8V: 15 3)) (!= (controller h8V: 10 15) 1)''')
 s=replace(s,'(!= ((owner p05?) hBunnyRoom?) 4)','(!= ((owner p05?) hBunnyRoom?) 2)')
 s=replace(s,'(!= ((owner p06?) h6FrankieRoom?) 4)','(!= ((owner p06?) h6FrankieRoom?) 1)')
 s=insert(s,'(if (!= (controller h8V: 10 0) 5) (return 0))')
 output['module991.sc']=merge(output['module991.sc'],{'h8GB':s})
 assert 'h8GB' not in selectors and 2999 not in selectors.values()
 selectors['h8GB']=2999
 from gate_b_access import apply as access
 output=access(output)
 return output,selectors
