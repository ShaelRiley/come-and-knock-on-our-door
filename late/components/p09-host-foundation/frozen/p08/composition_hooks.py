"""Explicit composition of reviewed additive components and gait resources."""
from pathlib import Path
import importlib.util
from source_tools import methods
from source_derivation import merge,insert,replace

ROOT=Path(__file__).resolve().parent


def corrected(source,folder):
    path=ROOT/'inputs/corrections'/folder/'apply_patch.py'
    spec=importlib.util.spec_from_file_location(folder.replace('-','_'),path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.transform(source)


def composition_base(output):
    # Apply the full old-method guard before the new layout gateway prepends its hook.
    output['main.sc']=corrected(output['main.sc'],'porch-exit-geometry-correction')
    return output


def composition_hooks(output):
    # Complete original-method and geometry dependency guards remain authoritative.
    output['module985.sc']=corrected(output['module985.sc'],'milo-approach-correction')
    mm=methods(output['module989.sc']);hooks={}
    hooks['h8LayoutInput']=insert(mm['h8LayoutInput'],'(if (self h8RouteBusy:) (return 0))')
    body=replace(mm['h8RouteDrawActor'],'audio node target)','audio node target pose view)')
    old=''' ; TEMPORARY CLOSED-MOUTH SLIDING PREVIEW. Original218/219 have no gait.
 ; New237/238 integration and native visual acceptance remain separate.
 (DrawCel (if actor 219 else 218) loop mouth'''
    new=''' ; Exact idle/talk resources stay original; gait advances only with the route clock.
 (= pose (self h8RoutePose: actor)) (= view (if actor 219 else 218))
 (if pose (= view (if actor 238 else 237)) (= mouth pose))
 (DrawCel view loop mouth'''
    hooks['h8RouteDrawActor']=replace(body,old,new)
    render=mm['h8LayoutRender']
    render=replace(render,'(if (not (self h8LayoutActive:)) (return 0))',
        '(if (not (or (self h8LayoutActive:) (and (self h8RouteBusy:) (self h8RouteValid:) (== (self h8RouteCamera:) 4) (== (self h8Preparations:) 8191)))) (return 0))')
    render=replace(render,'(h8Host drawJack:)', '(if (not (self h8RouteMode:)) (h8Host drawJack:))')
    hooks['h8LayoutRender']=render
    route=mm['h8RouteRender']
    route=replace(route,'camera actor slot)', 'camera actor slot pass mask best feet candidate)')
    old=''' (if (self h8RouteBusy:)
  ; Provisional clean-background cutaway; does not move Jackie to the camera.
  (DrawCel (if (== camera 1) 101 else (if (== camera 2) 300 else 305)) 0 0 0 0 -1 0))
 (if (and (not (h8Host onApron?)) (== camera (h8Host location?)) (self h8RouteBusy:)) (h8Host drawJack:))
 (for ((= actor 0)) (< actor 2) ((++ actor))
  (if (== camera (self h8RouteRoom: actor)) (self h8RouteDrawActor: actor)))'''
    new=''' (if (and (self h8RouteBusy:) (not (self h8SceneView: camera))) (return 0))
 ; Preserve the art contract's props-before-actors layers. People sort by actual feet.
 (= mask 0)
 (for ((= pass 0)) (< pass 3) ((++ pass))
  (= best -1) (= feet 32767)
  (for ((= actor 0)) (< actor 3) ((++ actor))
   (if (and (not (& mask (<< 1 actor)))
    (if (== actor 2) (and (not (h8Host onApron?)) (== camera (h8Host location?)))
      else (== camera (self h8RouteRoom: actor))))
    (= candidate (if (== actor 2) (/ (h8Host motionY?) 64) else (self h8RouteValue: actor 2)))
    (if (< candidate feet) (= feet candidate) (= best actor))))
  (if (>= best 0)
   (= mask (| mask (<< 1 best)))
   (if (== best 2) (h8Host drawJack:) else (self h8RouteDrawActor: best))))'''
    hooks['h8RouteRender']=replace(route,old,new)
    output['module989.sc']=merge(output['module989.sc'],hooks)
    return output
