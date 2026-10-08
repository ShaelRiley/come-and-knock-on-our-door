#!/usr/bin/env python3
"""Derive geometry tables from accepted editable art, correcting only native identity."""
from pathlib import Path
import hashlib,json,sys,importlib.util
H=Path(__file__).resolve().parent
if sys.flags.optimize:raise RuntimeError('Optimized Python forbidden')
g=json.loads((H/'inputs/layout-geometry/geometry-manifest.json').read_text())
spec=importlib.util.spec_from_file_location('view_decoder',H/'inputs/layout-geometry/view_decoder.py');decoder=importlib.util.module_from_spec(spec);spec.loader.exec_module(decoder)
cels=decoder.decode_view((H/'snapshot/resources/228.view.bin').read_bytes())[0]
objects=['ceramic_carrier','pa_kit','completed_screen','serving_table','credit_slate'];zones=['HATCH','WALL','ALCOVE','LANE']
assert g['stage']==[320,144] and g['positions']==['UNPLACED']+zones
assert g['object_ids']==dict(zip(objects,[34,63,83,120,40])) # exact reviewed historical proposal; consumer reconciles screen to81
assert len(cels)==18 and all(c['clear_key']==255 for c in cels)
lines=['; Generated from immutable reviewed art geometry. Native screen identity is81, never plan83.']
def switch(name,args,entries,default=-1):
 lines.append(f'(method ({name} {args}) (switch index')
 lines.extend(f' ({i} (return {v}))' for i,v in enumerate(entries));lines.append(f') (return {default}))')
switch('h8LayoutNative','index',[34,63,81,120,40])
lines.append('(method (h8LayoutIndex native) (switch native (34 (return 0)) (36 (return 0)) (63 (return 1)) (81 (return 2)) (120 (return 3)) (40 (return 4))) (return -1))')
switch('h8OriginValue','index',[v for obj in objects for xy in g['origins'][obj] for v in xy])
lines.append('(method (h8LayoutOrigin object position axis) (if (or (< object 0) (> object 4) (< position 0) (> position 4) (< axis 0) (> axis 1)) (return -1)) (return (self h8OriginValue: (+ (* (+ (* object 5) position) 2) axis))))')
switch('h8CelSizeValue','index',[v for c in cels for v in (c['width'],c['height'])])
lines.append('(method (h8CelSize cel axis) (if (or (< cel 0) (> cel 17) (< axis 0) (> axis 1)) (return -1)) (return (self h8CelSizeValue: (+ (* cel 2) axis))))')
switch('h8ZoneValue','index',[v for zone in zones for v in g['zone_rects'][zone]+g['zone_approaches'][zone]])
lines.append('(method (h8LayoutZone position field) (if (or (< position 1) (> position 4) (< field 0) (> field 6)) (return -1)) (return (self h8ZoneValue: (+ (* (- position 1) 7) field))))')
source='\n'.join(lines)+'\n';out=H/'templates/geometry989.sc.in'
if '--check' in sys.argv:
 if not out.exists() or out.read_text()!=source:raise RuntimeError('Geometry derivation drift')
else:out.write_text(source)
print('PASS_EXACT_ART_GEOMETRY_50_ORIGIN_WORDS_36_CEL_DIMENSIONS_28_ZONE_WORDS')
