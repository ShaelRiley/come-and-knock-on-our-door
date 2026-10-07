from pathlib import Path
import json
H=Path(__file__).resolve().parent
m=json.loads((H/'snapshot/scene/manifest.json').read_text());routes=[r for r in m['routes'] if r['puzzle']=='P07'];pages=[p for p in m['pages'] if p['puzzle']=='P07']
a=['; Exact scene manifest routes; all canonical content remains unedited.']
for name,key in [('h7Document','document_id'),('h7ExpectedPages','page_count'),('h7LineKey','global_line_key')]:
 a.append('(method ('+name+' record) (switch record')
 for r in routes:a.append(f' ({r["record"]} (return {r[key]}))')
 a.append(') (return 0))')
for name,key in [('h7PageUnit','unit'),('h7PageEntry','entry')]:
 a.append('(method ('+name+' record page) (switch record')
 for r in routes:
  pp=[p for p in pages if p['record']==r['record']]
  a.append(f' ({r["record"]} (switch page '+''.join(f'({p["record_page"]} (return {p[key]})) ' for p in pp)+'))')
 a.append(') (return -1))')
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
value='\n'.join(a)+'\n';path=H/'generated/routes.sc.inc'
if args.check:
 if path.read_text()!=value:raise RuntimeError('Generated canonical routes differ from exact scene manifest')
 print('PASS_CANONICAL_ROUTE_DERIVATION_CHECK')
else:path.write_text(value)
