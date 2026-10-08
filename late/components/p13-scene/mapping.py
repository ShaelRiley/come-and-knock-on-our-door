"""Finite explicit P13 output-to-document mapping; this module grants no receipt."""
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
    rr=exact(lines,m['routes']+[dict(r,document_kind='existing_support_label',binding_required=False) for r in m['supporting_labels']],'local_line_key');uu=exact(units,m['unit_routes'],'speech_unit_id')
    if {r['record_id'] for r in rr}&{u['record_id'] for u in uu}:raise ValueError('Whole record and its unit must not be conflated')
    if any(r['binding_required'] for r in rr+uu):raise ValueError('Observed failed-layout snapshot required; template routes are not displayable')
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
        if bound['binding_required']:raise ValueError('Failure binding is not a receipt source')
        if binding_snapshot is not None:raise ValueError('Unexpected dynamic binding')
        return {'source':source,'record_id':rid,'units':[],'pages':bound['pages'],'domain_form':[bound['record_number'],0,0],'display_authority':False}
    allunits=[u['line_id'] for u in bound['units']]
    if not unit_ids or len(unit_ids)!=len(set(unit_ids)) or any(u not in allunits for u in unit_ids):raise ValueError('Unknown/empty/repeated unit selection')
    indices=[allunits.index(u) for u in unit_ids]
    if indices!=list(range(indices[0],indices[0]+len(indices))):raise ValueError('Contiguous units in canonical order required')
    if bound['binding_required']:raise ValueError('Failure binding is not a receipt source')
    if binding_snapshot is not None:raise ValueError('Unexpected dynamic binding')
    rows=[m['unit_receipts'][u] for u in unit_ids]
    return {'source':source,'record_id':rid,'units':list(unit_ids),'pages':[p for r in rows for p in r['pages']],
        'domain_form':[0,rows[0]['speech_unit_id'],rows[-1]['speech_unit_id']],'display_authority':False}

def capture_blocked_snapshot(domain,cue):
    """Read an explicit current domain projection; this does not prove live ownership.

    Context and canonical speaker information are observations. Actual host
    actor/PA eligibility is a separate obligation before any voice or receipt.
    """
    if type(cue) is not int or cue not in (1,2):raise ValueError('Actual failed SERVE or SHOW operation required')
    return dict(cue=cue,status_code=domain.p['p13Code'],line_ids=[domain.call('p13Line',i) for i in range(domain.p['p13LineCount'])],
        blocked_label_key=domain.call('p13BlockedLayout',cue),epoch=domain.p['p13Epoch'],revision=domain.p['p13RevisionHi']*32768+domain.p['p13RevisionLo'],
        layout={name:domain.p['p13'+name] for name in ('BuffetAtHatch','HatchVisible','LaneClear','FootprintClear','DisplayConcealed')})

def binding_plan(snapshot,unit=False):
    """Select exact approved P08 label from the observed failed route. No fallback.

    The failure record has no P13 source receipt. Display evidence is still
    document/page specific, and it never grants a source or game-state receipt.
    """
    m=json.loads((H/'generated/manifest.json').read_text());a=json.loads((H/'inputs/domain/schema.json').read_text())
    if type(unit) is not bool:raise ValueError('Exact record/unit choice required')
    keys={'cue','status_code','line_ids','blocked_label_key','epoch','revision','layout'}
    if type(snapshot) is not dict or set(snapshot)!=keys:raise ValueError('Exact current failure/layout observation required')
    for key,low,high in [('cue',1,2),('status_code',1,32767),('blocked_label_key',46,49),('epoch',1,32767),('revision',1,1073741823)]:
        if type(snapshot[key]) is not int or not low<=snapshot[key]<=high:raise ValueError('Invalid observed '+key)
    layout=snapshot['layout'];layout_keys={'BuffetAtHatch','HatchVisible','LaneClear','FootprintClear','DisplayConcealed'}
    if type(layout) is not dict or set(layout)!=layout_keys or any(type(v) is not int or v not in (0,1) for v in layout.values()):raise ValueError('Exact Boolean domain layout projection required')
    cue=snapshot['cue'];code=a['codes']['buffet_or_hatch_blocked' if cue==1 else 'display_lane_or_footprint_blocked']
    if snapshot['status_code']!=code or snapshot['line_ids']!=[a['line_ids']['P13.FAILURE.009']] or any(type(x) is not int for x in snapshot['line_ids']):raise ValueError('The actual operation must have emitted this failure record')
    if cue==1:label='P08.LABEL.002' if not layout['BuffetAtHatch'] else 'P08.LABEL.006' if not layout['HatchVisible'] else None
    else:label='P08.LABEL.001' if not layout['LaneClear'] else 'P08.LABEL.004' if not (layout['FootprintClear'] and layout['DisplayConcealed']) else None
    if label is None or snapshot['blocked_label_key']!=a['line_ids'][label]:raise ValueError('p13BlockedLayout result does not match actual failed condition')
    rows=m['variant_unit_routes'] if unit else m['variant_routes'];row=next(r for r in rows if r['predicate']['label_record_id']==label)
    import copy
    return dict(record_id='P13.FAILURE.009',units=['P13.FAILURE.009.01'] if unit else [],documents=[row['document_id']],
        pages=[[row['document_id'],n] for n in range(row['page_count'])],variant_id=row['variant_id'],bindings=dict(row['predicate']['bindings']),
        label_record_id=label,snapshot=copy.deepcopy(snapshot),requires_every_selected_page=True,requires_current_snapshot_recheck=True,
        display_authority=False,source_receipt_authority=False,voice_eligibility=False,fallback=False)

def binding_is_current(plan,snapshot):
    if type(plan) is not dict or not plan.get('variant_id'):return False
    try:return binding_plan(snapshot,bool(plan['units']))==plan
    except (ValueError,KeyError,TypeError):return False
