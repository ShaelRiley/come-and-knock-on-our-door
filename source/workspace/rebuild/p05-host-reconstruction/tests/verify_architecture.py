from pathlib import Path
import json,sys,hashlib,re
sys.dont_write_bytecode=True
if sys.flags.optimize:raise RuntimeError('Optimized Python is forbidden')
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tools'));from source_tools import methods,spans,tokens
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
D=H/'snapshot/domain/module985.sc';assert sha(D)=='38a5bf402514511f24e74d25a445ee47716aab0552144b73724e7eb36a926cea'
base=methods(D.read_text());now=methods((H/'src/module985.sc').read_text());assert all(now[k]==v for k,v in base.items())
main=methods((H/'src/main.sc').read_text());old=methods((H/'snapshot/r2/main.sc').read_text())
changed=sorted(k for k in old if main[k]!=old[k]);added=sorted(set(main)-set(old))
assert 'BUNT.' in main['uiHostShortLabel'];assert 'Welcome bunting' not in main['uiHostShortLabel']
# Exact existing source guard; never hide TextSize failure9.
for label in ['ldi 9','aTop uiFailure']:
 assert main['uiRender'].count(label)==old['uiRender'].count(label)
assert main['eventLoop']==old['eventLoop']
assert '(self p05RestoreBegin:)' in main['replay'].split('(asm')[0]
assert main['p05RetireTransient'].index('presentation cancel:')<main['p05RetireTransient'].index('GetEvent 32767 self')
assert '(< i 64)' in main['p05RetireTransient']
# New private source callback has exactly one production invocation.
src=(H/'src/main.sc').read_text();assert src.count('hPresented:')==1
assert 'scenePageIdentity:' in now['hPresented'] and 'sdPaintGeneration?' in now['hPresented']
assert 'sdPresented:' not in now['hPresented'] and 'DoAudio' not in now['hPresented']
assert 'hPendingSource' in now['hRestoreValidate'] and 'hSeenCount' in now['hRestoreValidate']
# Original P04 r2 snapshot is protected; all other old source inputs unmodified.
B=H.parent/'p04-native-inventory-fix-reconstruction/staging-proof'
for p in (H/'snapshot/r2').glob('*.sc'):assert sha(p)==sha(B/'src'/p.name),(p,'snapshot changed')
abi=json.loads((H/'build/coherent/ABI-MAPPINGS.json').read_text());prior=json.loads((B/'verification-checkpoint/source-provenance/ABI-MAPPINGS.json').read_text());selectors={r['name']:r['selector_id'] for r in abi['selectors']}
assert all(selectors[r['name']]==r['selector_id'] for r in prior['selectors'])
for n in ['0','980','981','983','984']:
 assert [{k:a[k] for k in ['name','word_offset','word_count']} for a in abi['modules'][n]['locals']]==[{k:a[k] for k in ['name','word_offset','word_count']} for a in prior['modules'][n]['locals']]
receipt=json.loads((H/'build/coherent/compile-receipt.json').read_text());assert receipt['native_acceptance'] is False
assert receipt['class_owners']==[0,0,980,981,982,983,984,985]+([986] if '986' in abi['modules'] else [])
report=dict(status='PASS_ARCHITECTURE_ABI_SOURCE',domain_methods_preserved=len(base),old_main_methods=len(old),main_changed=changed,main_added=added,main_local_words=abi['modules']['0']['local_words'],budget=[dict(module=r['module'],used=r['combined_bytes'],remaining=65535-r['combined_bytes']) for r in receipt['modules']],native_acceptance=False,source_receipt_callsite='Main.dialoguePresented, reached after render/Graph12 in unchanged eventLoop',provenance={str(p.relative_to(H)):sha(p) for p in sorted((H/'snapshot').rglob('*')) if p.is_file()})
(H/'evidence/architecture-abi.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],len(changed),'old methods changed',len(added),'added')
