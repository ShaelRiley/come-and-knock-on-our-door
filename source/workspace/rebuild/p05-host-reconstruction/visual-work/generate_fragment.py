#!/usr/bin/env python3
"""Generate editable P05 geometry helpers from the accepted art contract.
No existing source or art is modified. No gameplay state is inferred from art.
"""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent; R=H.parents[1]
D=json.loads((R/'p05-art-reconstruction/design-contract.json').read_text()); T=D['targets']
def subtract(r,c):
 x1,y1,x2,y2=r;a,b,d,e=c;l=max(x1,a);t=max(y1,b);rr=min(x2,d);bb=min(y2,e)
 if l>=rr or t>=bb:return [r]
 return [q for q in [(x1,y1,x2,t),(x1,bb,x2,y2),(x1,t,l,bb),(rr,t,x2,bb)] if q[0]<q[2] and q[1]<q[3]]
def carve(rect,cuts):
 a=[rect]
 for c in cuts:a=[piece for r in a for piece in subtract(r,c)]
 return a
def control(obj,r):return f'        (self hControl: {obj} '+ ' '.join(map(str,r))+')'
small=[k for k,v in T.items() if v['object'] in (64,65,66,67,68,70,71)]
base=carve(T['pa_kit']['rect'],[T[k]['rect'] for k in small])
# Source actor art is 52x80 with native feet anchor26,78; fixed scale116.
actors={}
for name in ('milo','bunny'):
 a=D['actors'][name];px,py=a['feet'];s=a['scale128'];x=px-26*s//128;y=py-78*s//128
 rect=[x,y,x+52*s//128,y+80*s//128]
 actors[name]={'whole':rect,'fragments':carve(rect,[v['rect'] for v in T.values()])}
text='''; NEW P05 visual/geometry helper methods only. Append INSIDE P05State (species7).
; Add declarations from visual-locals.inc to the existing local block.
; Properties are supplied by the controller; see interfaces.json.
; uiHit searches in reverse registration order. Hardware is registered first;
; PA base and actor hit rectangles are disjoint from higher-priority hardware.
; Every rectangle is half-open. This fragment changes no domain state.
(method (hKitVisible)
    (return (if (and (== hPAOwner 1) (== hPARoom 5)) 1 else 0)))
(method (hCartVisible)
    (return (if (and (== hCartOwner 1) (== hCartRoom 5)) 1 else 0)))
(method (hMarkAt px py)
    (if (and (>= px 253) (< px 283) (>= py 120) (< py 134)) (return 1))
    (if (and (>= px 273) (< px 297) (>= py 134) (< py 144)) (return 2))
    (return 0))
(method (hCaptureTarget obj &tmp mark)
    (if (or (not hHost) (!= obj 69) (hHost onApron?) (!= (hHost location?) 5)) (return 0))
    ; Focus center supports keyboard navigation, stationary pointers, and clicks.
    (= mark (hHost p05FocusMark:))
    (if (not mark) (= mark (self hMarkAt: (hHost x?) (hHost y?))))
    (if (or (== mark 1) (== mark 2)) (= hSelectedMark mark) (return mark))
    (return 0))
(method (hControl obj left top right bottom)
    (return (hHost uiAddControl: 1 obj top left bottom right (self hShortLabel: obj))))
(method (hWorldControls)
    (if (or (not hHost) (hHost onApron?) (!= (hHost location?) 5)) (return 0))
    ; Explicit apron edge9 is navigation only. Audience10 and return11 retain
    ; the existing onApron branch; standing near a mark never invites anyone.
    (self hControl: 11 7 44 44 124)
    (self hControl: 9 298 44 320 144)
    (self hControl: 69 253 120 283 134)
    (self hControl: 69 273 134 297 144)
    (if (self hCartVisible:) (self hControl: 72 44 80 87 126))
    (if (self hKitVisible:)
'''
for k in small:text+=control(T[k]['object'],T[k]['rect'])+'\n'
text+='        ; Broad PA base is carved around the microphone, socket and handle.\n'
for r in base:text+=control(63,r)+'\n'
text+='    )\n    ; Register actor fragments last without stealing active props or exits.\n'
for name in ('milo','bunny'):
 if name=='bunny':text+='    (if (== hBunnyRoom 5)\n'
 for r in actors[name]['fragments']:text+=control(D['actors'][name]['object'],r)+'\n'
 if name=='bunny':text+='    )\n'
text+='''    (hHost uiAddControl: 1 32 2 160 12 211 "NOTES")
    (return 1))
(method (hApproachX obj)
    (switch obj
        (2 (return 268)) (28 (return 100))
'''
for k,v in T.items():
 if v['object']==69:continue
 text+=f"        ({v['object']} (return {v['approach'][0]}))\n"
text+='''        (69 (return (if (== hSelectedMark 2) 285 else 268))))
    (return 149))
(method (hApproachY obj)
    (switch obj
        (2 (return 139)) (28 (return 139))
'''
for k,v in T.items():
 if v['object']==69:continue
 text+=f"        ({v['object']} (return {v['approach'][1]}))\n"
text+='''        (69 (return (if (== hSelectedMark 2) 140 else 139))))
    (return 139))
(method (hDrawActor who &tmp view px py speaker scaleValue mouth facing presenter)
    (if (or (not hHost) (hHost onApron?) (!= (hHost location?) 5)) (return 0))
    (if (== who 2)
        (if (!= hBunnyRoom 5) (return 0))
        (= view 219) (= px 268) (= py 127) (= speaker 2)
    else
        (if (!= who 28) (return 0))
        (= view 221) (= px 100) (= py 129) (= speaker 5))
    (= scaleValue 116) (= mouth 0)
    (= facing (if (< (/ (hHost motionX?) 64) px) 1 else 0))
    (= presenter (hHost presentation?))
    (if (and presenter (== (hHost motionPhase?) 0)
        (== (presenter lane?) 1) (== (presenter speaker?) speaker))
        (= mouth (presenter mouth?)))
    (if (or (< mouth 0) (> mouth 2)) (= mouth 0))
    (DrawCel view facing mouth (- px (/ (* 26 scaleValue) 128))
        (- py (/ (* 78 scaleValue) 128)) -1 scaleValue scaleValue)
    (return 1))
(method (hRenderWorld &tmp feet)
    (if (or (not hHost) (hHost onApron?) (!= (hHost location?) 5)) (return 0))
    ; Main owns SetPort, palette999, captions, HUD, and the final Graph12 flush.
    ; Return1 tells Main to skip ALL old drawWorld, including its drawJack tail.
    (DrawCel 304 0 0 0 0 -1 0)
    (DrawCel 227 0 14 254 121 -1 0)
    (DrawCel 227 0 15 274 131 -1 0)
    (if (self hCartVisible:) (DrawCel 227 0 7 45 82 -1 0))
    (if (self hKitVisible:)
        (if (== [p05Words 66] 1) (DrawCel 227 0 6 133 92 -1 0)
        else (DrawCel 227 0 5 132 110 -1 0))
        (DrawCel 227 0 0 143 92 -1 0)
        (DrawCel 227 0 9 154 71 -1 0)
        (DrawCel 227 0 (+ 10 [p05Words 67]) 144 84 -1 0)
        (if (== [p05Words 66] 1) (DrawCel 227 0 13 184 92 -1 0)
        else (DrawCel 227 0 12 193 92 -1 0))
        (DrawCel 227 0 4 123 91 -1 0)
        (DrawCel 227 0 (+ 1 [p05Words 68]) 213 61 -1 0)
        (DrawCel 227 0 8 112 59 -1 0)
        (Display "TAPE" 100 144 84 102 0 105 0 106 24 121)
        (Display "MIC" 100 171 84 102 0 105 0 106 18 121))
    ; Closed/active mouths share unchanged219/221; draw order follows feet depth.
    (= feet (/ (hHost motionY?) 64))
    (if (< feet 127) (hHost drawJack:))
    (self hDrawActor: 2)
    (if (and (>= feet 127) (< feet 129)) (hHost drawJack:))
    (self hDrawActor: 28)
    (if (>= feet 129) (hHost drawJack:))
    (Display "PORCH" 100 8 115 102 1 105 0 106 32 121)
    (Display "EDGE" 100 294 135 102 2 105 0 106 26 121)
    (return 1))
(method (hLabel obj)
    ; Each label has its own persistent64-byte buffer. Canonical native font0
    ; normalization (case/apostrophe) comes from accepted text205, not new prose.
    (switch obj
'''
entries={63:10,64:12,65:16,66:18,67:22,68:24,69:26,70:28,71:30,72:32}
for obj,e in entries.items():text+=f'        ({obj} (GetFarText 205 {e} @hLabel{obj}) (return @hLabel{obj}))\n'
text+='''        (2 (return "BUNNY")) (28 (return "MILO"))
        (9 (return "AUDIENCE EDGE")) (11 (return "PORCH")))
    (return 0))
(method (hShortLabel obj)
    ; At most five6px font0 glyphs: all fit the compact32x10 item cell.
    (switch obj
'''
short={63:'PA',64:'INPUT',65:'MIC',66:'SOCK',67:'SPKR',68:'TURN',69:'MARK',70:'TAPE',71:'SLATE',72:'CART',2:'BUNNY',28:'MILO',9:'EDGE',11:'PORCH'}
for o,s in short.items():text+=f'        ({o} (return "{s}"))\n'
text+='    ) (return 0))\n'
(H/'visual-methods.sc.inc').write_text(text)
(H/'visual-locals.inc').write_text(' '.join(f'[hLabel{o} 32]' for o in entries)+'\n')
meta={'classification':'new helper fragment; no native acceptance','required_properties':{'hHost':0,'hBunnyRoom':1,'hPAOwner':1,'hPARoom':5,'hCartOwner':1,'hCartRoom':5,'hSelectedMark':1},'added_locals':{f'hLabel{o}':32 for o in entries},'label_text_resource':205,'label_entries':entries,'compact_labels':short,'pa_fragments':base,'actors':actors,'external_host_methods':{'p05FocusMark':'zero-arg helper returns hMarkAt center of focused control when action1/payload69, otherwise0','uiAddControl':'action payload top left bottom right label; existing Main','drawJack':'zero args; existing Main'},'public_interfaces':{'hWorldControls':'() -> 1 overrides complete garage controls, 0 lets Main handle another room/apron','hRenderWorld':'() -> 1 overrides complete garage drawWorld, 0 lets Main handle another room/apron','hApproachX':'(obj) -> garage floor x; mark69 uses hSelectedMark','hApproachY':'(obj) -> garage floor y; mark69 uses hSelectedMark','hMarkAt':'(x,y) -> 1 Bunny mark,2 audience mark,0 outside both','hCaptureTarget':'(obj) -> selected mark1/2,0 no capture; call before movement','hLabel':'(obj) -> stable full-label pointer,0 unhandled','hShortLabel':'(obj) -> compact label pointer,0 unhandled'}}
(H/'interfaces.json').write_text(json.dumps(meta,indent=2)+'\n')
print('Generated visual-methods.sc.inc, visual-locals.inc, interfaces.json')
