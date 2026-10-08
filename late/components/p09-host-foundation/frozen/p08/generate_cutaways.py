#!/usr/bin/env python3
"""Derive actual cutaway prop rendering from the pinned current scene methods."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'tools'))
from source_tools import methods

def generate(check=False):
    m=methods((ROOT/'inputs/presentation-basis/main.sc').read_text())
    u=methods((ROOT/'inputs/presentation-basis/module988.sc').read_text())
    s=methods((ROOT/'inputs/presentation-basis/module989.sc').read_text())
    living=m['drawLiving'];living=living[living.index('(DrawCel 101'):living.index('(= feet')]
    cooking=u['h7Render'];cooking=cooking[cooking.index('(DrawCel 233'):cooking.rindex('(return 1)')].replace('(self ','(p07 ')
    cloth=s['h8RenderCloth'];cloth=cloth[cloth.index('(Graph 11'):cloth.rindex('(return 1)')]
    kitchen=m['drawKitchen'];kitchen=kitchen[kitchen.index('(DrawCel 300'):].rsplit(')',1)[0]
    assert kitchen.count('(if p07 (p07 h7Render:))')==1
    kitchen=kitchen.replace('(if p07 (p07 h7Render:))',cooking)
    kitchen=kitchen.replace('(if p07 (p07 h7DrawBunny:))','')
    kitchen=kitchen.replace('(if p08 (p08 h8RenderCloth:))','(if (self h8Owns: 22)\n'+cloth+'\n)')
    # Exit labels belong to the interactive camera. The cutaway has no room controls.
    label='(Display "LIVING ROOM" 100 12 112 102 1 105 0 106 66 121)'
    assert kitchen.count(label)==1;kitchen=kitchen.replace(label,'')
    text='''; Generated from pinned full scene methods. No physical actor or player location writes.
(method (h8SceneView camera &tmp p03 p07 p08 tray pot p02BoardRecords p02CopyBunny p02PlanAgreed wedge)
 (if (or (self h8Barrier:) (not (self h8PublishersReady:)) (not (self h8RouteBusy:)) (not (self h8RouteValid:)) (!= camera (self h8RouteCamera:))) (return 0))
 (if (== camera 4) (return (self h8LayoutRender:)))
 (if (== camera 1)
  (= p02BoardRecords (h8Host p02BoardRecords?)) (= p02CopyBunny (h8Host p02CopyBunny?))
  (= p02PlanAgreed (h8Host p02PlanAgreed?)) (= wedge (h8Host wedge?))
'''+living+''' (return 1))
 (if (== camera 2)
  (= p03 (h8Host p03?)) (= p07 (h8Host p07?)) (= p08 self) (= tray (h8Host tray?))
'''+kitchen+''' (return 1))
 (return 0))
'''
    out=ROOT/'templates/cutaway989.sc.in'
    if check:assert out.read_text()==text,'cutaway derivation drift'
    else:out.write_text(text)
    print('PASS_PINNED_ACTUAL_ROOM_PROP_DERIVATION')

if __name__=='__main__':generate('--check' in sys.argv)
