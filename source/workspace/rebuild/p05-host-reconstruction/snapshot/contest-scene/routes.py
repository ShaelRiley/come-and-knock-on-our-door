#!/usr/bin/env python3
# Dependency imports must invalidate stale acceptance before ordinary stage guards exist.
from pathlib import Path as _BootPath
import json as _BootJson
_BOOT_ROOT = _BootPath(__file__).resolve().parent
try:
    """Fail-closed Python route reference; host may port the frozen stride7 table.

    No game flags, scoring, receipts, audio or practical outcomes are mutated here.
    """
    import json
    from integrity import H, require, sha, failed

    def load_export():
        try:
            path=H/'generated/manifest.json'
            lock=H/'evidence/immutable-export-lock.json'
            require(lock.is_file(),'Reviewed export seal is required for route loading')
            if lock.exists():
                sealed=json.loads(lock.read_text())
                require(sha(path.read_bytes())==sealed['files']['generated/manifest.json']['sha256'],'Scene manifest differs from reviewed seal')
            return json.loads(path.read_text())
        except BaseException as exc:
            failed('route-import',exc);raise

    from functools import lru_cache
    @lru_cache(maxsize=1)
    def _cached_trusted_manifest():
        return load_export()

    def trusted_manifest():
        try:
            require((H/'evidence/immutable-export-lock.json').is_file(),'Reviewed export seal is required for route loading')
            return _cached_trusted_manifest()
        except BaseException as exc:
            failed('route-import',exc);raise

    def exact_equal(a,b):
        if type(a) is not type(b):return False
        if isinstance(a,dict):return a.keys()==b.keys() and all(exact_equal(a[k],b[k]) for k in a)
        if isinstance(a,(list,tuple)):return len(a)==len(b) and all(exact_equal(x,y) for x,y in zip(a,b))
        return a==b

    def integer(value,low,high):return type(value) is int and low<=value<=high

    def validate_row(row,manifest=None):
        from generate import RECORDS, UNITS, DOMAIN, row_contexts
        require(type(row.get('contexts')) is list and row['contexts'] and all(integer(c,0,8) for c in row['contexts']), 'Malformed route context mask')
        require(row['contexts']==sorted(set(row['contexts'])), 'Duplicate or unordered context mask')
        require(integer(row.get('record'),1,154) and integer(row.get('unit'),0,134),'Malformed typed record/unit columns')
        rid=row.get('record_id');uid=row.get('unit_id')
        require(rid in RECORDS and row.get('record')==DOMAIN['records'][rid], 'Record binding changed')
        require((uid is None and row.get('unit')==0) or (uid in UNITS and row.get('unit')==DOMAIN['units'][uid] and UNITS[uid]['record_id']==rid), 'Unit binding changed')
        expected=row_contexts(RECORDS[rid],UNITS.get(uid))
        if rid.startswith('IR') and rid.endswith('.SETUP') and uid is None:expected=[5,6,7,8]
        if set(RECORDS[rid].get('dynamic_bindings',{}))=={'opponent_name'} or rid=='VC.NOTEBOOK.POOL':
            e=row.get('condition',{}).get('encounter');require(integer(e,1,4), 'Malformed dynamic encounter');expected=[e]
        require(row['contexts']==expected, 'Context mask changes canonical unit or template scope')
        require(integer(row.get('variant'),0,172) and integer(row.get('document'),471,881) and integer(row.get('first_page'),0,63) and integer(row.get('page_count'),1,64), 'Malformed route fields')
        if manifest is not None:
            matches=[r for r in manifest['routes'] if r['document_id']==row['document']]
            require(len(matches)==1 and matches[0]['record_id']==rid,'Route document binding changed')
            route=matches[0];require(row['first_page']+row['page_count']<=route['page_count'],'Page window exceeds record')
            if route['owner']!='p05':require(exact_equal(row.get('condition',{}),route.get('condition',{})),'State template condition changed')
        require((row.get('owner')=='p05' and row['document']<=479) or (row.get('owner') in ('contest','contest_alias') and row['document']>=480), 'Duplicate document ownership')

    def lookup(record,unit,context,variant=0,manifest=None):
        """Return one exact source-item window, or reject; no implicit variant union."""
        require(integer(record,1,154) and integer(unit,0,134) and integer(context,0,8) and integer(variant,0,172),'Invalid numeric route key')
        m=manifest if manifest is not None else load_export()
        rows=[r for r in m['lookup'] if (r['record'],r['unit'],r['variant'])==(record,unit,variant) and context in r['contexts']]
        require(len(rows)==1,'Missing or ambiguous source-item route')
        row=rows[0];validate_row(row,m)
        frozen=trusted_manifest()
        require(all(exact_equal(m[k],frozen[k]) for k in ('records','units','pairs','dynamic_variants')),'Supplied authority or finite template expansion changed')
        trusted=[r for r in trusted_manifest()['lookup'] if (r['record'],r['unit'],r['variant'])==(record,unit,variant) and context in r['contexts']]
        require(len(trusted)==1 and exact_equal(row,trusted[0]),'Source-item alias identity differs from the frozen exact-unit route')
        route=next(r for r in m['routes'] if r['document_id']==row['document'])
        require(row['first_page']==0 and row['page_count']==route['page_count'],'A source-item route must cover exactly its whole unit document')
        frozen_route=next(r for r in frozen['routes'] if r['document_id']==row['document'])
        require(exact_equal(route,frozen_route),'Supplied source-item document identity changed')
        storage=route.get('page_storage',route['owner'])
        from generate import BASE,UNITS,RECORDS
        pagebank=BASE['pages'] if storage=='p05' else m['pages']
        selected=[pagebank[i] for i in route['page_indices']]
        if storage!='p05':require(exact_equal(selected,[frozen['pages'][i] for i in route['page_indices']]),'Supplied source-item page content changed')
        require(len(selected)==row['page_count'] and all(p['line_id']==row['unit_id'] for p in selected),'Route exposes sibling unit pages')
        if row['unit_id'] is not None:
            expected=UNITS[row['unit_id']]
            require(''.join(p['raw_text'] for p in selected)==expected['text'] and all(p['speaker_id']==expected['speaker_id'] for p in selected),'Unit caption or speaker differs from canonical source')
        require(row['page_count']>0 and row['first_page']>=0,'Invalid page window')
        return dict(row)

    def ui_route(record,context,*,pair=0,setup_learned=(),reply_learned=(),won=(),manifest=None):
        """Derive dynamic notebook routes from exact bounded sets, not arbitrary prose/counts.

        Learned sets contain integer pair IDs1..24. Won contains encounter IDs1..4.
        Context0 is a general notebook; eligible-pool views require VC1..4.
        """
        m=manifest if manifest is not None else load_export()
        trusted=trusted_manifest()
        require(all(exact_equal(m[k],trusted[k]) for k in ('records','pairs','dynamic_variants')),'Dynamic source or state-template identity changed')
        require(integer(record,1,154) and integer(context,0,8) and integer(pair,0,24),'Invalid UI route identity')
        def exact_set(values,maximum):
            require(isinstance(values,(list,tuple,set,frozenset)),'State must be a bounded collection')
            require(all(integer(v,1,maximum) for v in values),'State identity out of bounds')
            result=set(values);require(len(result)==len(values),'Duplicate state identity');return result
        setups,replies,wins=exact_set(setup_learned,24),exact_set(reply_learned,24),exact_set(won,4)
        records={r['id']:r for r in m['records']};rid=next((r['id'] for r in m['records'] if m_record(m,r['id'])==record),None)
        require(rid is not None and records[rid].get('dynamic_bindings'),'Not a dynamic UI record')
        if rid in ('VC.NOTEBOOK.WINS','VC.GATE.MISSING_WINS') and len(wins)==4:
            return lookup(m_record(m,'VC.GATE.ALL_WON'),0,context,manifest=m)
        candidates=[v for v in m['dynamic_variants'] if v['record']==record and context in v['contexts']]
        chosen=[]
        for v in candidates:
            c=v['condition'];ok=True
            if 'pair' in c:ok=pair==c['pair']
            if 'setup_learned' in c:ok=ok and (pair in setups)==c['setup_learned']
            if 'reply_learned' in c:ok=ok and (pair in replies)==c['reply_learned']
            if 'won_mask' in c:ok=ok and sum(1<<(e-1) for e in wins)==c['won_mask']
            if 'full_pair_count' in c:
                ok=ok and len(setups&replies&set(range(1,6*context+1)))==c['full_pair_count']
            if 'learned_accepted_alternatives' in c:
                accepted=next(p['accepted_response_ids'] for p in m['pairs'] if p['pair_id']==f'IR{pair:02d}') if pair else []
                learned=sorted(r for r in accepted if r!=f'IR{pair:02d}.REPLY' and int(r[2:4]) in replies)
                ok=ok and c['learned_accepted_alternatives']==learned and pair in setups
            if ok:chosen.append(v)
        require(len(chosen)==1,'No authorized dynamic UI variant')
        value=chosen[0]
        variant=0 if set(records[rid]['dynamic_bindings'])=={'opponent_name'} else value['variant']
        return lookup(record,0,context,variant,manifest=m)

    def m_record(manifest,rid):
        # Fixture order is pinned to the domain's numeric map.
        return next(i for i,r in enumerate(manifest['records'],1) if r['id']==rid)

    def decode_route_table(text,manifest=None):
        """Validate the exported compact SCI include as exact frozen lookup rows."""
        import re
        m=manifest if manifest is not None else load_export()
        require(exact_equal(m['lookup'],trusted_manifest()['lookup']),'Supplied compact route authority changed')
        match=re.search(r'\[vcSceneRoutes (\d+)\] = \[([^\]]*)\]',text)
        require(match is not None,'Missing route table')
        words=[int(v) for v in match[2].split()]
        require(len(words)==int(match[1]) and len(words)%7==0,'Malformed route table length')
        rows=[words[i:i+7] for i in range(0,len(words),7)]
        for record,unit,mask,variant,document,first,count in rows:
            require(integer(mask,1,511),'Malformed context mask bits')
            require(integer(record,1,154) and integer(unit,0,134) and integer(variant,0,172),'Malformed route table key')
            require(integer(document,471,881) and first==0 and integer(count,1,64),'Unsafe source-item window')
        expected=[[r['record'],r['unit'],sum(1<<c for c in r['contexts']),r['variant'],r['document'],r['first_page'],r['page_count']] for r in m['lookup']]
        require(rows==expected,'Route table changes canonical identity, context or source-item window')
        return rows

except BaseException as _boot_exc:
    if not (isinstance(_boot_exc, SystemExit) and _boot_exc.code in (None, 0)):
        _boot_folder = _BOOT_ROOT / 'evidence'
        _boot_folder.mkdir(parents=True, exist_ok=True)
        _boot_receipt = {'status':'FAILED','stage':'bootstrap:routes.py','error':str(_boot_exc),'native_acceptance':False}
        for _boot_name in ('current-status','verification-status','rebuild-status'):
            (_boot_folder / (_boot_name + '.json')).write_text(_BootJson.dumps(_boot_receipt, indent=2) + '\n')
    raise
