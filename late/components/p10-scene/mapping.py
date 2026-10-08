"""Finite explicit P10 output-to-document mapping; this module grants no receipt."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent

def plan(lines=(),units=()):
    m=json.loads((H/'generated/manifest.json').read_text())
    def exact(values,rows,key):
        if type(values) not in (tuple,list) or any(type(x) is not int for x in values):raise ValueError('Exact local integer IDs required')
        lookup={r[key]:r for r in rows}
        if len(values)!=len(set(values)) or any(x not in lookup for x in values):raise ValueError('Unknown or repeated local ID')
        return [lookup[x] for x in values]
    rr=exact(lines,m['routes'],'local_line_key');uu=exact(units,m['unit_routes'],'speech_unit_id')
    if {r['record_id'] for r in rr}&{u['record_id'] for u in uu}:raise ValueError('Whole record and its unit must not be conflated')
    return {'documents':[r['document_id'] for r in rr+uu],
        'identity':[{'kind':r['document_kind'],'record':r['record_id'],'unit':r.get('line_id')} for r in rr+uu],
        'empty_status_is_unbound':True,'display_authority':False}

def source_plan(source,record_id=None,unit_ids=()):
    m=json.loads((H/'generated/manifest.json').read_text())
    if type(source) is not str or source not in m['source_bindings']:raise ValueError('Unknown source')
    rid=m['source_bindings'][source];bound=m['record_receipts'][rid]
    if type(unit_ids) not in (tuple,list) or any(type(x) is not str for x in unit_ids):raise ValueError('Exact unit IDs required')
    if record_id is not None:
        if type(record_id) is not str or record_id!=rid or unit_ids:raise ValueError('Exactly one bound form required')
        return {'source':source,'record_id':rid,'units':[],'pages':bound['pages'],'domain_form':[bound['record_number'],0,0],'display_authority':False}
    allunits=[u['line_id'] for u in bound['units']]
    if not unit_ids or len(unit_ids)!=len(set(unit_ids)) or any(u not in allunits for u in unit_ids):raise ValueError('Unknown/empty/repeated unit selection')
    indices=[allunits.index(u) for u in unit_ids]
    if indices!=list(range(indices[0],indices[0]+len(indices))):raise ValueError('Contiguous units in canonical order required')
    rows=[m['unit_receipts'][u] for u in unit_ids]
    return {'source':source,'record_id':rid,'units':list(unit_ids),'pages':[p for r in rows for p in r['pages']],
        'domain_form':[0,rows[0]['speech_unit_id'],rows[-1]['speech_unit_id']],'display_authority':False}
