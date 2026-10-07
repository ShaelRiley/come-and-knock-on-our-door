#!/usr/bin/env python3
"""Generate a reviewable SCI fragment. Never modifies the current host."""
from common import ROOT,Guard,write_json,sha
_entry_guard=Guard('host_fragment') if __name__=='__main__' else None
from geometry import *

def run():
 g=_entry_guard or Guard('host_fragment')
 lines=['; NEW courtyard art reconstruction. Static-only reviewed source fragment.',
 '; Append these methods to P05State985; host owns selector assignment/compilation.',
 '; DrawCel305/228 and reused227 use palette999/font0. No model/owner mutation.',
 '(method (hCourtVisible)',
 '    (return (and hHost (not (hHost onApron?)) (== (hHost location?) 4)',
 '        (== hPAOwner 1) (== hPARoom 4) (self p05NZ: S_COMPLETE))))',
 '(method (hCourtControls)',
 '    (if (or (not hHost) (hHost onApron?) (!= (hHost location?) 4)) (return 0))']
 for name,label in [('house_arch','LIVING ROOM'),('side_gate','SIDE GATE'),('audience_edge','AUDIENCE EDGE')]:
  s=EXITS[name];a,b,c,d=s['rect'];lines.append(f'    (hHost uiAddControl: 1 {s["object"]} {b} {a} {d} {c} "{label}")')
 lines+=['    (if (self hCourtVisible:)','        (self hControl: 71 137 103 162 127)',
 '        ; Carve kit around exit19 so control iteration order cannot steal gate.',
 '        (self hControl: 63 164 61 282 129)',
 '        (self hControl: 63 282 111 291 129))',
 '    (hHost uiAddControl: 1 32 2 160 12 211 "NOTES")','    (return 1))']
 for suffix,coordinate in [('X',0),('Y',1)]:
  lines +=[f'(method (hCourtApproach{suffix} obj)','    (switch obj']
  for spec in [*EXITS.values(),P05['kit'],P05['slate']]:lines.append(f'        ({spec["object"]} (return {spec["approach"][coordinate]}))')
  lines +=['    )',f'    (return {114 if coordinate==0 else 140}))']
 lines+=['(method (hCourtScale) (return 127))','(method (hCourtRender &tmp p4)',
 '    (if (or (not hHost) (hHost onApron?) (!= (hHost location?) 4)) (return 0))',
 '    (DrawCel 305 0 0 0 0 -1 0)',
 '    (= p4 (hHost p04?))',
 '    ; Physical gate only: OPEN1 shows base; RESTING0/CLOSED2 show closed layer.',
 '    (if (or (not p4) (!= (p4 p04Gate?) 1)) (DrawCel 228 0 11 281 36 -1 0))']
 for c,(x,y) in MARKS:lines.append(f'    (DrawCel 228 0 {c} {x} {y} -1 0)')
 xy=P05['hardware_origins']
 def draw(c):x,y=xy[c];return f'(DrawCel 227 0 {c} {x} {y} -1 0)'
 lines+=['    (if (self hCourtVisible:)',f'        (if (== [p05Words 66] 1) {draw(6)} else {draw(5)})',f'        {draw(0)}',f'        {draw(9)}',f'        (DrawCel 227 0 (+ 10 [p05Words 67]) {xy[10][0]} {xy[10][1]} -1 0)',f'        (if (== [p05Words 66] 1) {draw(13)} else {draw(12)})',f'        {draw(4)}',f'        (DrawCel 227 0 (+ 1 [p05Words 68]) {xy[1][0]} {xy[1][1]} -1 0)',
 '        (DrawCel 227 0 8 137 103 -1 0)',
 '        (Display "TAPE" 100 185 84 102 0 105 0 106 24 121)',
 '        (Display "MIC" 100 212 84 102 0 105 0 106 18 121))',
 '    ; Main sets scale127 for courtyard walking/approaches before drawJack.',
 '    ; Return1 suppresses the old blockout and prevents a second actor draw.',
 '    (hHost drawJack:)',
 '    (return 1))','']
 (ROOT/'host-integration.sc.in').write_text('\n'.join(lines))
 write_json(ROOT/'host-integration.json',{'scope':'P05 room4 static presentation fragment; no compiled/native acceptance','append_target':'P05State script985, no new class/species','fragment':'host-integration.sc.in','resources':{'305':sha(ROOT/'resources/305.view.bin'),'228':sha(ROOT/'resources/228.view.bin'),'227':sha(ROOT/'reference/227.view.bin')},'entry_hooks':{'hWorldControls':'if room4 call hCourtControls before existing garage logic','hRenderWorld':'if room4 call hCourtRender before existing garage logic; return1 skips entire old blockout/drawJack tail','approaches':'route courtyard18/19/9/63/71 through hCourtApproachX/Y','drawJack':'room4 scale128=127, feet x26..293 and y124..141; floor corridor141, use documented approach feet','reader':'Look63 stages inspection; Look/Use71 must present existing exact document462; no garage return, pocket token or new credit text','gate':'query current p04Gate; only OPEN1 visual open; existing authorized exit19 dispatch retains P04 physical permission','owner':'show rig only completed P05, hPAOwner1/hPARoom4; owner2 delegates to future P08 projection after physical ACK','P08':'not implemented by fragment; must provide canonical-label overlap chooser and source acknowledgment/ownership/autosave host','apron':'fragment returns0, preserving current audience overlay and return path'},'controls':{'kit63_fragments':[[164,61,282,129],[282,111,291,129]],'slate71':[137,103,162,127],'approaches':{'63':[114,140,127],'71':[111,139,127]}},'forbidden_changes':['P05 credit/connection/source/aim history','P04 gate/peg/latch history','pocket inventory','handcart72/listener69 positions','P08 position UNPLACED or ownership before ACK','display panel reveal','P07 pot kitchen ownership']})
 g.done(fragment_sha256=sha(ROOT/'host-integration.sc.in'))
if __name__=='__main__':run()
