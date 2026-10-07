#!/usr/bin/env python3
"""Exact complete-record admission tables from the accepted scene window map."""
from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent
m=json.loads((H/'inputs/scene/line-document-unit-map.json').read_text())
routes=[r for r in m['routes'] if r['owner']=='P08']
assert len(routes)==44 and [r['record'] for r in routes]==list(range(1,45))
units={r['record']:[u['unit'] for u in m['units'] if u['owner']=='P08' and u['record']==r['record'] and u['unit']] for r in routes}
s='(method (h8ExpectedPages record) (switch record\n'+''.join(f' ({r["record"]} (return {r["page_count"]}))\n' for r in routes)+') (return 0))\n'
s+='(method (h8ExpectedStart record) (switch record\n'+''.join(f' ({r["record"]} (return {r["absolute_page_start"]}))\n' for r in routes)+') (return -1))\n'
s+='(method (h8ExpectedUnitCount record) (switch record\n'+''.join(f' ({k} (return {len(v)}))\n' for k,v in units.items())+') (return 0))\n'
s+='(method (h8ExpectedUnit record index) (switch record\n'+''.join(f' ({k} (switch index '+''.join(f' ({i} (return {u}))' for i,u in enumerate(v))+'))\n' for k,v in units.items() if v)+') (return 0))\n'
p=H/'templates/routes.sc.in'
if '--check' in sys.argv:
 if p.read_text()!=s:raise RuntimeError('Canonical route-admission table drift')
else:p.write_text(s)
print('PASS_CANONICAL_P08_ADMISSION_TABLES')
