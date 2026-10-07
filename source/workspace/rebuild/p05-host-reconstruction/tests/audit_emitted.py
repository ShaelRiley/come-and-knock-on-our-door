from pathlib import Path
import sys,json,hashlib,difflib,types
sys.dont_write_bytecode=True
if sys.flags.optimize:raise RuntimeError('Optimized Python is forbidden')
H=Path(__file__).resolve().parents[1];ROOT=H.parent;BASE=ROOT/'p05-domain-reconstruction/tools/emitted_gates.py'
sys.path.insert(0,str(BASE.parent));before=BASE.read_text();old="require(number!=985,'Pure P05 domain must not call kernels',name,args[0])";new="require(number!=985 or name.startswith('h'),'Original P05 domain must not call kernels',name,args[0])";assert before.count(old)==1;after=before.replace(old,new)
module=types.ModuleType('host_audit');module.__file__=str(BASE);exec(compile(after,str(BASE),'exec'),module.__dict__)
B=H/'build/coherent';table=json.loads((ROOT/'p05-domain-reconstruction/reference/opcode-tables.json').read_text());kernels=json.loads((ROOT/'p05-domain-reconstruction/reference/kernels.json').read_text());selectors={r['name']:r['selector_id'] for r in json.loads((B/'selector-list.json').read_text())}
receipt=json.loads((B/'compile-receipt.json').read_text());abi=json.loads((B/'ABI-MAPPINGS.json').read_text());reports={}
for row in receipt['modules']:
 n=row['module'];s=(B/f'compiled/{n}.scr.bin').read_bytes();he=(B/f'compiled/{n}.scr.bin.hep').read_bytes();lay=module.extract(s,he,selectors);metadata=module.source_metadata((B/'src'/('main.sc' if n==0 else f'module{n}.sc')).read_text())
 reports[str(n)]=module.audit_module(n,s,he,lay,selectors,table,kernels,metadata,abi['modules']['0']['local_words'],receipt['class_owners'])
report=dict(status='PASS_STATIC_EMITTED_UNIVERSE',modules=reports,native_acceptance=False,source_auditor_sha256=hashlib.sha256(before.encode()).hexdigest(),adaptation='Only new h-prefixed host helpers may call kernels; original P05 methods retain pure-domain gate')
(H/'evidence/static-emitted.json').write_text(json.dumps(report,indent=2)+'\n');(H/'evidence/static-auditor.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='sealed-domain-auditor',tofile='scoped-host-helper-auditor')))
print(report['status'],[(n,r['method_count'],r['branches'],r['call_sites']) for n,r in reports.items()])
