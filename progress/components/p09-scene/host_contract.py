"""Reference page/receipt mapping. The host and domain authenticate real state.

This module never claims pixels appeared. It rejects malformed/stale evidence
and produces the exact adapter tuple only after trusted complete visible pages.
"""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent


def load():return json.loads((HERE/'generated/manifest.json').read_text())


def route(local_id,unit=False,manifest=None):
    m=manifest if manifest is not None else load()
    if type(local_id)is not int or not 1<=local_id<=20:raise ValueError('Unknown canonical numeric ID')
    return m['unit_routes' if unit else 'routes'][local_id-1]


def result_plan(lines=(),units=(),manifest=None):
    m=manifest if manifest is not None else load()
    routes=[route(n,manifest=m) for n in lines]+[route(n,True,m) for n in units]
    return {'documents':[r['document_id'] for r in routes],'routes':routes,'empty_status_is_unbound':not routes}


def requirements(source,*,record_id=None,unit_ids=(),variant='full',unit_mode='unit_document',manifest=None):
    m=manifest if manifest is not None else load()
    if source not in m['source_receipts'] or variant not in ('full','stringer_only'):raise ValueError('Unknown source or variant')
    if variant=='stringer_only' and source!='accusation':raise ValueError('Restricted variant belongs to accusation')
    if unit_mode not in ('unit_document','record_pages'):raise ValueError('Unknown unit presentation mode')
    if bool(record_id)==bool(unit_ids):raise ValueError('Exactly one record or unit-range form required')
    src=m['source_receipts'][source]
    tokens=src['canonical_tokens'] if variant=='full' else ['P09.FAILURE.001.01']
    if record_id:
        if record_id not in src['record_ids']:raise ValueError('Cross-source record')
        rec=m['record_receipts'][record_id]
        if not set(rec['canonical_tokens'])<=set(tokens):raise ValueError('Restricted full-record receipt')
        pages=rec['pages'];record_number=rec['record_number'];first=last=0
        requested=rec['canonical_tokens']
    else:
        if any(u not in m['unit_receipts'] or u not in tokens for u in unit_ids):raise ValueError('Unknown or cross-source unit')
        start=tokens.index(unit_ids[0])
        if list(unit_ids)!=tokens[start:start+len(unit_ids)]:raise ValueError('Out-of-order or discontinuous units')
        # Terms grant and its post-grant outcome are two different state transitions.
        if source=='terms' and 'P09.SUCCESS.001.01' in unit_ids and len(unit_ids)!=1:raise ValueError('Terms-to-success leap')
        pages=[p for u in unit_ids for p in m['unit_receipts'][u]['pages' if unit_mode=='unit_document' else 'record_pages']]
        record_number=0;first=m['local_unit_keys'][unit_ids[0]];last=m['local_unit_keys'][unit_ids[-1]]
        requested=list(unit_ids)
    deferred=source=='terms' and requested==['P09.SUCCESS.001.01']
    required_room=None if source=='terms_card' or deferred else 6
    speakers=[]
    if source in ('intro','direct_question','front_context','terms','shared_wish') and not deferred:speakers.append('stringer')
    if source=='shared_wish':speakers.append('rita')
    if source=='accusation':
        if 'P09.FAILURE.001.01' in requested:speakers.append('stringer')
        if 'P09.FAILURE.001.02' in requested:speakers.append('rita')
    return {'source':source,'source_number':src['source_number'],'canonical_tokens':requested,
        'pages':pages,'record_number':record_number,'first_unit':first,'last_unit':last,
        'required_room':required_room,'speakers':speakers,
        'view':'side' if source=='intro' else 'front' if source=='front_context' else None,
        'plan_required':source=='terms' and not deferred,'card_required':source=='terms_card' or deferred,
        'boundary':'Domain still authenticates pending prefix, actual state and exact source/start/epoch lease.'}


class VisibleReceipt:
    def __init__(self,required,*,start_hi,start_lo,epoch):
        if any(type(x)is not int for x in (start_hi,start_lo,epoch)):raise ValueError('Strict integer lease words')
        if not (0<=start_hi<=32767 and 0<=start_lo<=32767 and start_hi+start_lo>0 and 1<=epoch<=32767):raise ValueError('Invalid lease words')
        self.required=json.loads(json.dumps(required));self.start_hi=start_hi;self.start_lo=start_lo;self.epoch=epoch
        self.painted=set();self.cancelled=False
    def cancel(self):self.cancelled=True;self.painted.clear()
    def observe(self,*,kind,source,start_hi,start_lo,epoch,document,page,unobscured,draw_succeeded,graph12,
                current_room,on_apron,evening_started,contest_active,stringer_room,rita_room,view,
                plan_agreed=False,card_available=False):
        r=self.required
        if (self.cancelled or kind!='visible_graph12' or source!=r['source'] or
            any(type(x)is not int for x in (start_hi,start_lo,epoch,document,page,current_room,stringer_room,rita_room)) or
            (start_hi,start_lo,epoch)!=(self.start_hi,self.start_lo,self.epoch) or
            [document,page] not in r['pages'] or unobscured is not True or draw_succeeded is not True or
            graph12 is not True or on_apron is not False or evening_started is not True or contest_active is not False or
            current_room not in range(7) or (r['required_room'] is not None and current_room!=r['required_room']) or
            (r['view'] is not None and view!=r['view']) or
            (r['plan_required'] and plan_agreed is not True) or (r['card_required'] and card_available is not True) or
            ('stringer' in r['speakers'] and stringer_room!=6) or ('rita' in r['speakers'] and rita_room!=6)):
            return False
        self.painted.add((document,page));return True
    def acknowledgment(self):
        r=self.required
        if self.cancelled or not set(map(tuple,r['pages']))<=self.painted:return None
        return (r['source_number'],self.start_hi,self.start_lo,self.epoch,r['record_number'],r['first_unit'],r['last_unit'])
