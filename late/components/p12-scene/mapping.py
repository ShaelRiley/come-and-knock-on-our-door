"""Finite explicit P12 output-to-document mapping; this module grants no receipt."""
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
    if any(r['binding_required'] for r in rr+uu):raise ValueError('Observed-order snapshot required; template routes are not displayable')
    return {'documents':[r['document_id'] for r in rr+uu],
        'identity':[{'kind':r['document_kind'],'record':r['record_id'],'unit':r.get('line_id')} for r in rr+uu],
        'empty_status_is_unbound':True,'display_authority':False}

def source_plan(source,record_id=None,unit_ids=(),binding_snapshot=None):
    m=json.loads((H/'generated/manifest.json').read_text())
    if type(source) is not str or source not in m['source_bindings']:raise ValueError('Unknown source')
    rid=m['source_bindings'][source];bound=m['record_receipts'][rid]
    if type(unit_ids) not in (tuple,list) or any(type(x) is not str for x in unit_ids):raise ValueError('Exact unit IDs required')
    if record_id is not None:
        if type(record_id) is not str or record_id!=rid or unit_ids:raise ValueError('Exactly one bound form required')
        if bound['binding_required']:return binding_plan(source,binding_snapshot)
        if binding_snapshot is not None:raise ValueError('Unexpected dynamic binding')
        return {'source':source,'record_id':rid,'units':[],'pages':bound['pages'],'domain_form':[bound['record_number'],0,0],'display_authority':False}
    allunits=[u['line_id'] for u in bound['units']]
    if not unit_ids or len(unit_ids)!=len(set(unit_ids)) or any(u not in allunits for u in unit_ids):raise ValueError('Unknown/empty/repeated unit selection')
    indices=[allunits.index(u) for u in unit_ids]
    if indices!=list(range(indices[0],indices[0]+len(indices))):raise ValueError('Contiguous units in canonical order required')
    if bound['binding_required']:return binding_plan(source,binding_snapshot,unit_ids)
    if binding_snapshot is not None:raise ValueError('Unexpected dynamic binding')
    rows=[m['unit_receipts'][u] for u in unit_ids]
    return {'source':source,'record_id':rid,'units':list(unit_ids),'pages':[p for r in rows for p in r['pages']],
        'domain_form':[0,rows[0]['speech_unit_id'],rows[-1]['speech_unit_id']],'display_authority':False}

def binding_plan(source,snapshot,unit_ids=()):
    """Explicit finite projection only. Caller must authenticate current domain context.

    word_ids are the three actual p12VisibleWord(0..2) results, never desired order.
    source_start and epoch must belong to this exact presentation request. This
    pure mapper cannot prove that the caller queried a live owner or saw a page.
    """
    m=json.loads((H/'generated/manifest.json').read_text())
    if source not in ('audience_view','self_view'):raise ValueError('No dynamic binding for this source')
    if type(snapshot) is not dict or set(snapshot)!={'source','source_start','epoch','word_ids'}:raise ValueError('Exact source lease and observed word snapshot required')
    if snapshot['source']!=source:raise ValueError('Snapshot source mismatch')
    if any(type(snapshot[k]) is not int or not 1<=snapshot[k]<=limit for k,limit in [('source_start',1073741823),('epoch',32767)]):raise ValueError('Positive bounded source lease required')
    order=snapshot['word_ids']
    if type(order) not in (list,tuple) or len(order)!=3 or any(type(n) is not int for n in order) or set(order)!={1,2,3}:raise ValueError('Exact distinct observed word IDs 1..3 required')
    rid=m['source_bindings'][source];units=[u['line_id'] for u in m['unit_routes'] if u['record_id']==rid]
    if type(unit_ids) not in (tuple,list) or (unit_ids and list(unit_ids)!=units):raise ValueError('Exact original unit ID required')
    variant='cue_'+''.join(map(str,order));rows=m['variant_unit_routes'] if unit_ids else m['variant_routes']
    row=next(r for r in rows if r['record_id']==rid and r['variant_id']==variant)
    return {'source':source,'record_id':rid,'units':list(unit_ids),'documents':[row['document_id']],
        'pages':[[row['document_id'],n] for n in range(row['page_count'])],
        'domain_form':[0,row['speech_unit_id'],row['speech_unit_id']] if unit_ids else [row['local_line_key'],0,0],
        'variant_id':variant,'bindings':dict(row['predicate']['bindings']),
        'snapshot':{'source':source,'source_start':snapshot['source_start'],'epoch':snapshot['epoch'],'word_ids':list(order)},
        'requires_every_selected_page':True,'requires_current_snapshot_recheck':True,'display_authority':False,'fallback':False}

def binding_is_current(plan,snapshot):
    if type(plan) is not dict or not plan.get('variant_id'):return False
    try:return binding_plan(plan['source'],snapshot,plan['units'])==plan
    except (ValueError,KeyError,TypeError):return False
