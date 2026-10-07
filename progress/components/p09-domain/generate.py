#!/usr/bin/env python3
"""New deterministic P09 SCI generator. Historical evidence is read-only input."""
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from reference.cakood import p09_model as model

def ident(s): return re.sub(r'[^A-Z0-9]','_',s.upper())
def switch(name,args,rows,default='0'):
    return f'(method ({name} {args})\n (switch {args.split()[0]}\n'+''.join(f'  ({k} {body})\n' for k,body in rows)+f' ) (return {default}))\n'
def generate():
    m=json.loads((ROOT/'schema.json').read_text()); out=[';;; Sierra Script 1.0 - (do not remove this comment)',
    '; NEW P09 reconstruction; historical fragments retained separately. No native acceptance.',
    '(script# 990)','(public p09State 0)',
    '(local [p09Lines 8] [p09Units 6] [p09Events 3] [p09EventArgs 9] [p09Held 400] [p09Lease 10] [p09Order 9] [p09Journal 20] [p09Stage 77] [p09Backup 77])']
    for field,prefix in [('objects','OBJ'),('rooms','ROOM'),('sources','SOURCE'),('codes','CODE'),('events','EVENT'),('line_ids','LINE'),('speech_unit_ids','UNIT'),('tokens','TOKEN')]:
        out.extend(f'(define {prefix}_{ident(k)} {v})' for k,v in m[field].items())
    out.extend(f'(define BIND_{ident(k)} {v["id"]})' for k,v in m['bindings'].items())
    out.append('(class P09State\n (properties\n'+''.join(f'  {k} {v}\n' for k,v in m['all_properties'].items())+' )')
    for suffix in ('Hi','Lo'):
        out.append(switch('p09Serial'+suffix,'slot',[(i,f'(return p09{s}{suffix})') for i,s in enumerate(m['serials'])]))
    out.append(switch('p09SetSerial','slot hi lo',[(i,f'(= p09{s}Hi hi) (= p09{s}Lo lo) (return 1)') for i,s in enumerate(m['serials'])]))
    out.append(switch('p09Word','index',[(i,f'(return {p})') for i,p in enumerate(m['persisted_properties'])]))
    out.append(switch('p09SetWord','index value',[(i,f'(= {p} value) (return 1)') for i,p in enumerate(m['persisted_properties'])]))
    out.append(switch('p09Capacity','source',[(v,f'(return {len(m["receipts"][k])})') for k,v in m['sources'].items()]))
    out.append(switch('p09ReceiptBase','source',[(v,f'(return {m["receipts"][k][0]["slot"]})') for k,v in m['sources'].items()],'-1'))
    out.append(switch('p09Token','source index',[(v,'(switch index '+''.join(f'({i} (return {m["tokens"][r["token"]]}))' for i,r in enumerate(m['receipts'][k]))+')') for k,v in m['sources'].items()]))
    out.append(switch('p09SourceRecord','source',[(v,f'(return {m["line_ids"][model.SOURCE_BINDINGS[k][0]]})') for k,v in m['sources'].items()]))
    token_records={t:r for r in model.SOURCE_BINDINGS.values() for r in r for t in model._record_tokens(r)}
    out.append(switch('p09TokenRecord','token',[(v,f'(return {m["line_ids"][token_records[t]]})') for t,v in m['tokens'].items()]))
    out.append(switch('p09TokenUnit','token',[(v,f'(return {m["speech_unit_ids"].get(t,0)})') for t,v in m['tokens'].items()]))
    out.append(switch('p09RecordFirst','record',[(m['line_ids'][r],f'(return {m["tokens"][model._record_tokens(r)[0]]})') for r in dict.fromkeys(token_records.values())]))
    out.append(switch('p09RecordSize','record',[(v,f'(return {len(model._record_tokens(r))})') for r,v in m['line_ids'].items()]))
    out.append(switch('p09Bind','binding',[(v['id'],' '.join(f'(self p09AddLine: {m["line_ids"][r]})' for r in v['records'])+' (return 1)') for v in m['bindings'].values()]))
    out.append(switch('p09Fixed','obj',[(m['objects'][x],'(return 1)') for x in sorted(model.FIXED_OBJECTS|{model.CARD})]))
    out.append((ROOT/'templates/domain.sc.in').read_text())
    out.append('; Five complete historical methods reused after comparison with the unchanged model.\n'+(ROOT/'historical/module990-five-complete-methods.sc.txt').read_text())
    out.append(')\n(instance p09State of P09State)\n')
    text='\n'.join(out);(ROOT/'src/module990.sc').write_text(text)
    receipt={'scope':'NEW reconstruction generated source, not recovered historical body','sha256':hashlib.sha256(text.encode()).hexdigest(),'historical_methods':'literal exact reuse; all new supporting methods in templates/domain.sc.in','model_sha256':hashlib.sha256((ROOT/'reference/cakood/p09_model.py').read_bytes()).hexdigest(),'native_acceptance':False}
    (ROOT/'evidence/generation.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt
if __name__=='__main__':print(json.dumps(generate(),indent=2))
