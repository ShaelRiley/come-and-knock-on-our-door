from pathlib import Path
import json,hashlib,sys,re
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tools'))
from source_tools import methods,tokens
sha=lambda b:hashlib.sha256(b).hexdigest()
def check(ok,msg):
 if not ok:raise RuntimeError(msg)
old=(H/'snapshot/domain/module988.sc').read_text();new=(H/'src/module988.sc').read_text()
a,b=methods(old),methods(new)
check(set(a)<=set(b),'Original P07 methods lost')
check(all(a[n]==b[n] for n in a),'Original P07 method source changed')
selectors=json.loads((H/'selectors.json').read_text())
for filename in ['snapshot/base/selectors.json','snapshot/domain/selectors.json']:
 for n,i in json.loads((H/filename).read_text()).items():check(selectors.get(n)==i,'ABI selector changed '+n)
check(len(set(selectors.values()))==len(selectors),'Duplicate selector ID')
check(all(2200<=selectors[n]<=2399 for n in set(b)-set(a)),'P07 host selector out of reservation')
layout0=json.loads((H/'snapshot/domain/layout.json').read_text());abi=json.loads((H/'build/coherent/ABI-MAPPINGS.json').read_text());layout1=abi['modules']['988']['reference_layout']
check(layout1['objects'][0]['species']==10,'P07 species changed')
check(layout1['locals_word_count']>=layout0['locals_word_count'],'P07 locals lost')
for x,y in zip(layout0['objects'][0]['properties'][9:],layout1['objects'][0]['properties'][9:]):check((x['selector_id'],x['raw_value'])==(y['selector_id'],y['raw_value']),'P07 property prefix changed')
rows=[]
for layout,blob in [(layout0,(H/'snapshot/domain/988.scr.bin').read_bytes()),(layout1,(H/'build/coherent/compiled/988.scr.bin').read_bytes())]:
 positions=sorted({x['code_offset'] for o in layout['objects'] for x in o['methods']}|{layout['script_relocation_offset']})
 rows.append({x['selector']:blob[x['code_offset']:positions[positions.index(x['code_offset'])+1]] for x in layout['objects'][0]['methods']})
check(all(v==rows[1][n] for n,v in rows[0].items()),'Original P07 emitted method changed')
# Exact canonical rows and metadata retained; host aliases never enlarge data arrays.
base_scene=(H/'snapshot/scene/module982.sc').read_text();current_scene=(H/'src/module982.sc').read_text()
for name in ['sdStarts','sdCounts','sdPageData','sdTextResources','sdAudioModules','sdPageDurations']:
 pattern=r'\['+name+r'\s+\d+\]\s*=\s*\[([^]]*)\]'
 check(re.search(pattern,base_scene).group()==re.search(pattern,current_scene).group(),'Canonical scene table changed '+name)
for n in ['sdRoute','sdPageCount']:
 check('document 971' in methods(current_scene)[n] and 'document 972' in methods(current_scene)[n],'Missing exact slice aliases')
main=methods((H/'src/main.sc').read_text());caption=methods((H/'snapshot/base/main.caption-fixed.sc.txt').read_text())
check(main['walk']==caption['walk'],'Guarded return-caption fix changed')
check('h7Render:' in main['drawKitchen'],'Missing physical cooking layer')
check('p07Handoff:' not in (H/'templates/host.sc.in').read_text(),'Unauthorized future player handoff')
check('p07LoadCommit: 1' in b['h7RestoreBegin'] and 'p05RetireTransient' in main['p05RetireTransient'],'Missing restore admission/retirement')
check(b['h7RestoreBegin'].index('p07LoadCommit: 1')<b['h7RestoreBegin'].index('p07BindSession:'),'Session bound before payload/context admission')
check(b['h7Presented'].index('h7SeenCount h7PendingPages')<b['h7Presented'].index('p07AcknowledgePage:'),'Knowledge acknowledged before full native pagination')
for source in (H/'templates').glob('*.sc.in'):
 s=source.read_text();spans=methods(s);remaining=s
 for v in spans.values():remaining=remaining.replace(v,'',1)
 check(not tokens(remaining),'Unparsed template expressions '+source.name)
report={'status':'PASS','original_p07_source_methods':len(a),'original_p07_emitted_methods_byte_exact':len(rows[0]),'added_p07_host_methods':len(set(b)-set(a)),'preserved_domain_source_sha256':sha(old.encode()),'domain_emitted_spans':{n:sha(v) for n,v in rows[0].items()},'compile_sha256':sha((H/'build/coherent/compile-receipt.json').read_bytes()),'main_bytes':next(x['combined_bytes'] for x in json.loads((H/'build/coherent/compile-receipt.json').read_text())['modules'] if x['module']==0),'native_acceptance':False}
(H/'evidence/architecture.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS source and byte-exact domain ABI',len(a))
