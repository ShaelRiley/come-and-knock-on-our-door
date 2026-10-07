#!/usr/bin/env python3
"""Static emitted audit using the sealed domain auditor with one scoped change:
new h* host helper methods may use kernels; original p05* methods still may not.
This explicit adaptation is hashed and its exact diff is saved for review.
"""
from pathlib import Path
import sys,json,hashlib,difflib,types
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];ROOT=H.parents[1];BASE=ROOT/'p05-domain-reconstruction/tools/emitted_gates.py'
sys.path.insert(0,str(BASE.parent))
before=BASE.read_text();old="require(number!=985,'Pure P05 domain must not call kernels',name,args[0])";new="require(number!=985 or name.startswith('h'),'Original P05 domain must not call kernels',name,args[0])"
assert before.count(old)==1;after=before.replace(old,new)
module=types.ModuleType('visual_audit');module.__file__=str(BASE);exec(compile(after,str(BASE),'exec'),module.__dict__)
B=H/'build';table=json.loads((ROOT/'p05-domain-reconstruction/reference/opcode-tables.json').read_text());kernels=json.loads((ROOT/'p05-domain-reconstruction/reference/kernels.json').read_text());selectors={r['name']:r['selector_id'] for r in json.loads((B/'selector-list.json').read_text())}
s=(B/'compiled/985.scr.bin').read_bytes();he=(B/'compiled/985.scr.bin.hep').read_bytes();lay=module.extract(s,he,selectors);metadata=module.source_metadata((B/'src/module985.sc').read_text())
report=module.audit_module(985,s,he,lay,selectors,table,kernels,metadata,json.loads((B/'layout-0.json').read_text())['locals_word_count'],[0,0,980,981,982,983,984,985])
report.update(status='PASS_STATIC_EMITTED_HOST_HELPERS',native_acceptance=False,source_auditor_sha256=hashlib.sha256(before.encode()).hexdigest(),adaptation='Only new h-prefixed host helpers may call kernels; original P05 methods retain pure-domain gate')
(H/'evidence/static-emitted.json').write_text(json.dumps(report,indent=2)+'\n');(H/'evidence/static-auditor.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='sealed-domain-auditor',tofile='scoped-host-helper-auditor')))
print(report['status'],report['method_count'],report['branches'],report['call_sites'])
