"""Narrow additive actor-route hooks. Accepted domain methods remain literal."""
from source_tools import methods
from source_derivation import merge,insert,replace

def route_hooks(output):
 mm=methods(output['main.sc']);hooks={}
 walk=replace(mm['p02Walk'],'&tmp destination)','&tmp destination routeFrom routeRevision)')
 walk=replace(walk,'(= location destination)','(= routeFrom location) (= routeRevision p02Revision) (if p08 (p08 h8RouteArm: routeFrom obj routeRevision)) (= location destination)')
 walk=replace(walk,'(self p02HostText: 134 location)','(if p08 (p08 h8RouteTravel: routeFrom obj routeRevision))\n(self p02HostText: 134 location)')
 hooks['p02Walk']=walk
 transition=replace(mm['p05Transition'],'(p05Transition room)','(p05Transition room &tmp routeFrom)')
 transition=insert(transition,'(if (and p08 (p08 h8RouteBusy:)) (return 0))')
 transition=replace(transition,'(= location room)','(= routeFrom location) (= location room)')
 transition=replace(transition,'(return 1)','(if p08 (p08 h8RouteTravel: routeFrom 0 p02Revision)) (return 1)')
 hooks['p05Transition']=transition
 hooks['advance']=insert(mm['advance'],'(if (and p08 (p08 h8RouteTick: arg1)) (return 0))')
 hooks['input']=insert(mm['input'],'(if (and p08 (p08 h8RouteInput:)) (return 0))')
 hooks['uiHostChoice']=insert(mm['uiHostChoice'],'(if (and p08 (p08 h8RouteChoice: context)) (return 0))')
 hooks['uiHostConfirm']=insert(mm['uiHostConfirm'],'(if (and p08 (p08 h8RouteChoice: context)) (return 0))')
 hooks['hostActNow']=insert(mm['hostActNow'],'(if (and p08 (p08 h8RouteBlock: arg1 arg2 arg3)) (return 0))')
 hooks['bridgeActAtArrival']=insert(mm['bridgeActAtArrival'],'(if (and p08 (p08 h8RouteBlock: action obj target)) (return 0))')
 hooks['p02ObjectLocation']=insert(mm['p02ObjectLocation'],'(if (and p06 (== obj 8)) (return (p06 h6FrankieRoom?)))')
 hooks['livingPerson']=insert(mm['livingPerson'],'(if (and (== who 3) p06 (!= (p06 h6FrankieRoom?) 1)) (return 0))')
 hooks['uiAddControl']=insert(mm['uiAddControl'],'(if (and p06 (== action 1) (== payload 8) (!= location (p06 h6FrankieRoom?))) (return 1))')
 hooks['drawWorld']=insert(mm['drawWorld'],'(if (and p08 (p08 h8RouteBusy:)) (p08 h8RouteRender:) (return 1))')[:-1]+'\n)'
 hooks['drawWorld']=replace(hooks['drawWorld'],'(return 1))\n)','(if (and p08 (p08 h8RouteMeeting:)) (p08 h8RouteRender:)) (return 1))\n)') if False else hooks['drawWorld']
 hooks['drawWorld']=replace(hooks['drawWorld'],'(if p06 (p06 h6Render:))','(if p06 (p06 h6Render:)) (if (and p08 (p08 h8RouteMeeting:)) (p08 h8RouteRender:))')
 hooks['uiHostWorldControls']=replace(mm['uiHostWorldControls'],'(return 1)','(if p08 (p08 h8RouteControls:)) (return 1)')
 hooks['dialogueCanSpeak']=insert(mm['dialogueCanSpeak'],'(if (and p08 (p08 h8RouteBusy:)) (return 0)) (if (and p08 (p08 h8RouteCanSpeak: who)) (return 1)) (if (and (== who 3) p06 (!= location (p06 h6FrankieRoom?))) (return 0))')
 hooks['writeSave']=insert(mm['writeSave'],'(if (and p08 (not (p08 h8RouteSave:))) (return 0))')
 hooks['readSave']=insert(mm['readSave'],'(if p08 (p08 h8RouteRetire:))')
 hooks['p05RetireTransient']=insert(mm['p05RetireTransient'],'(if p08 (p08 h8RouteRetire:))')
 output['main.sc']=merge(output['main.sc'],hooks)
 mm=methods(output['module989.sc'])
 output['module989.sc']=merge(output['module989.sc'],{
  'h8SaveReady':insert(mm['h8SaveReady'],'(if (not (self h8RouteSaveValid:)) (return 0))'),
  'h8RestoreBegin':replace(mm['h8RestoreBegin'],'(not (self h8SupportedHistory:))','(not (self h8SupportedHistory:)) (not (self h8RouteSaveValid:))')})
 mm=methods(output['module987.sc'])
 guarded=replace(mm['h6OwnersValid'],'(!= h6FrankieRoom 1)','(not (or (== h6FrankieRoom 1) (and (h6Host p08?) ((h6Host p08?) h8RouteActorValid: 0))))')
 output['module987.sc']=merge(output['module987.sc'],{'h6OwnersValid':guarded})
 mm=methods(output['module988.sc'])
 guarded=replace(mm['h7PhysicalValid'],'(if (or (== (h7Controller hBunnyRoom?) 2)','(if (or (and (h7Host p08?) ((h7Host p08?) h8RouteInvite:)) (and (== (h7Controller hBunnyRoom?) 2) (or (not (h7Host p08?)) (not ((h7Host p08?) h8RouteMode:))))')
 output['module988.sc']=merge(output['module988.sc'],{'h7PhysicalValid':guarded})
 mm=methods(output['module985.sc'])
 # A P08 record must agree even when the old broad room range would admit it.
 output['module985.sc']=merge(output['module985.sc'],{'hPhysicalValid':insert(mm['hPhysicalValid'],'(if (and (== hBunnyRoom 4) (not (and (hHost p08?) ((hHost p08?) h8RouteActorValid: 1)))) (return 0)) (if (and (hHost p08?) ((hHost p08?) h8RouteMode:) (not ((hHost p08?) h8RouteActorValid: 1))) (return 0))')})
 return output
