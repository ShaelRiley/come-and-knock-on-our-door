"""Minimal data append to current P07 host source, followed by complete guard rederivation."""
from pathlib import Path
import sys,json,re,shutil,subprocess
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'tools'))
from generate import require,sha,dump
from source_tools import methods,spans
def merge_methods(source,replacements):
 ranges=spans(source)
 require(set(replacements)<=set(ranges),"No new method allowed")
 for name in sorted(replacements,key=lambda n:ranges[n][0],reverse=True):
  a,b=ranges[name];source=source[:a]+replacements[name]+source[b:]
 return source
ARRAYS=('sdStarts','sdCounts','sdPageData','sdLegacyVoiceDurations','sdTextResources','sdAudioModules','sdPageDurations')
def read_array(s,n):
 m=re.search(r'\['+n+r' (\d+)\] = \[([^\]]*)\]',s);require(m is not None,'Missing '+n);a=[int(v) for v in m[2].split()];require(len(a)==int(m[1]),'Array size '+n);return a
def replace(s,old,new,count=1):require(s.count(old)==count,'Source shape '+old);return s.replace(old,new)
def extend():
 require(not sys.flags.optimize,'Optimized Python forbidden')
 manifest=json.loads((H/'generated/manifest.json').read_text());source=(H/'inputs/src/module982.sc').read_text();require(sha(source.encode())=='f6d6a3f18b80bc0c41f3f23d9f84508d031de31a70c5fcf38968f6e8efa67ae0','Latest host982 pin')
 old={n:read_array(source,n) for n in ARRAYS};new={n:v[:] for n,v in old.items()}
 require(len(old['sdStarts'])==971 and len(old['sdPageData'])==1070*8,'Baseline allocation')
 require([r['document_id'] for r in manifest['routes']]==list(range(973,1018)),'Document sequence');require([r['global_line_key'] for r in manifest['routes']]==list(range(729,774)),'Global line sequence')
 # Reserved array holes keep the existing special aliases971/972 source-identical.
 new['sdStarts'].extend([-1,-1]);new['sdCounts'].extend([0,0])
 for route in manifest['routes']:new['sdStarts'].append(route['absolute_page_start']);new['sdCounts'].append(route['page_count'])
 for p in manifest['pages']:
  new['sdPageData'].extend(p['fields']);new['sdTextResources'].append(p['resource']);new['sdAudioModules'].append(p['audio_module']);new['sdPageDurations'].append(p['duration_ticks'])
 for n,a in new.items():
  require(a[:len(old[n])]==old[n],'Old prefix '+n)
  source,c=re.subn(r'\['+n+r' \d+\] = \[[^]]*\]',f'[{n} {len(a)}] = ['+' '.join(map(str,a))+']',source,count=1);require(c==1,'Array replacement')
 source=replace(source,'(> document 970)','(> document 1017)',2)
 source=replace(source,'(>= index (* 1070 8))',f"(>= index (* {manifest['total_pages']} 8))")
 source=replace(source,'(!= sdResource 207))','(!= sdResource 207) (!= sdResource 208))')
 source=replace(source,'(!= sdAudioModule 917))','(!= sdAudioModule 917) (!= sdAudioModule 918))')
 out=H/'generated/src';out.mkdir(parents=True,exist_ok=True)
 for p in (H/'inputs/src').glob('*.sc'):shutil.copy2(p,out/p.name)
 (out/'module982.sc').write_text(source)
 p=subprocess.run([sys.executable,str(H/'tools/generate_static_guards.py')],capture_output=True,text=True);(H/'evidence/static-generation.log').write_text(p.stdout+p.stderr);require(p.returncode==0,p.stdout+p.stderr)
 static=H/'generated/static';source=merge_methods(source,methods((static/'module982-methods.inc').read_text()));(out/'module982.sc').write_text(source)
 guard=methods((static/'guard-methods.inc').read_text());old985=(out/'module985.sc').read_text();m985=methods(old985)
 # Keep exact parser/range/family validation implementations; only table counts/offsets/bank stride change.
 replacements={n:guard[n] for n in ['hStaticCount','hStaticFirst','hStaticLoad']};new985=merge_methods(old985,replacements);(out/'module985.sc').write_text(new985)
 for n in ['hStaticOwner','hStaticValue','hStaticRange','hStaticAll']:require(re.sub(r'\s+','',m985[n])==re.sub(r'\s+','',guard[n]),'Unrelated guard drift '+n)
 require(methods((out/'module981.sc').read_text())['hStaticAt']==methods((static/'module981-methods.inc').read_text())['hStaticAt'],'981 static accessor drift')
 require(methods(old985)['hStaticAt']==methods((static/'module985-methods.inc').read_text())['hStaticAt'],'985 static accessor drift')
 shutil.copy2(H/'inputs/resources/242.text.bin',static/'242.text.bin')
 changes={}
 for p in sorted(out.glob('*.sc')):
  previous=(H/'inputs/src'/p.name).read_text();before=methods(previous);after=methods(p.read_text());require(list(before)==list(after),'Method membership/order drift '+p.name)
  changes[p.name]=[n for n in before if before[n]!=after[n]]
  allowed={'module982.sc':{'sdRoute','sdPageCount','sdLoad','hStaticAt'},'module985.sc':{'hStaticCount','hStaticFirst','hStaticLoad'}}.get(p.name,set())
  require(set(changes[p.name])<=allowed,'Method change scope '+p.name)
  require(re.findall(r'\(method \(([^)]*)\)',previous)==re.findall(r'\(method \(([^)]*)\)',p.read_text()),'Method signatures changed')
 p=subprocess.run([sys.executable,str(H/'tools/generate_static_guards.py')],capture_output=True,text=True);require(p.returncode==0,p.stdout+p.stderr)
 tables=json.loads((static/'manifest.json').read_text());require(len(tables['tables'])==20,'Static family count')
 dump(H/'generated/extension-contract.json',dict(schema=1,old_pages=1070,new_pages=len(manifest['pages']),total_pages=manifest['total_pages'],old_max_document=972,new_max_document=1017,first_new_line=729,last_new_line=773,arrays=new,changed_methods=changes,static_bank_entries=480,static_resources=[240,241,244],preserved_label_resource=242,static_families=20,source982_input_sha256=sha((H/'inputs/src/module982.sc').read_bytes()),source982_output_sha256=sha(source.encode()),selectors_unchanged=True,class_owners_unchanged=True,native_acceptance=False))
 print('appended',len(manifest['pages']),'pages; rederived20 static families')

if __name__=='__main__':extend()
