#!/usr/bin/env python3
"""Generate numeric canonical windows; no text, speaker, route or document aliases."""
from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent
def generate(check=False):
    data=json.loads((H/'inputs/scene/line-document-unit-map.json').read_text())
    routes={r['record']:r for r in data['routes'] if r['owner']=='P08'}
    maps={1:{},2:{},3:{}}
    for obj,record in [(13,16),(14,17),(15,18),(5,28)]:
        r=routes[record];maps[1][obj]=[r['document_id'],0,r['page_count'],record,r['global_line_key']]
    for row in data['output_windows']:
        if row['kind']!='unit_only':continue
        kind=2 if row['owner']=='P08' else 3
        unit=row['unit'] if kind==2 else row['transition_unit']
        assert unit not in maps[kind]
        maps[kind][unit]=[row['document_id'],row['first_record_page'],row['page_count'],row['record'],1]
    assert len(maps[2])==33 and len(maps[3])==4
    lines=['; Generated exact canonical mapping: document, first, count, record, line-key/source or unit-only flag.','(method (h8ReaderMap kind id field)',' (if (or (< field 0) (> field 4)) (return -1))',' (switch kind']
    for kind,rows in maps.items():
        lines.append(f' ({kind} (switch id')
        for id,values in sorted(rows.items()):lines.append(f'  ({id} (switch field '+' '.join(f'({i} (return {v}))' for i,v in enumerate(values))+'))')
        lines.append(' ))')
    lines.append(' ) (return -1))');text='\n'.join(lines)+'\n';p=H/'templates/reader-map989.sc.in'
    if check:assert p.read_text()==text,'canonical reader map drift'
    else:p.write_text(text)
    print('PASS_EXACT_FOUR_SOURCE_AND_37_UNIT_MAP')
if __name__=='__main__':generate('--check' in sys.argv)
