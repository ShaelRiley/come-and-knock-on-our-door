"""Delegate only new P14 pages to class-free script999; old arrays stay exact."""
from pathlib import Path
import json,re,sys,shutil
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'tools'))
from source_tools import methods,spans
from caption_layout import sha
TABLES=('fbStarts','fbCounts','fbPageData','fbTextResources','fbAudioModules','fbPageDurations','fbDatePrefix','fbDateSuffix')
def merge(source,replacements):
 ranges=spans(source)
 for n in sorted(replacements,key=lambda n:ranges[n][0],reverse=True):
  a,b=ranges[n];source=source[:a]+replacements[n]+source[b:]
 return source
def arrays(source):
 return {m[1]:[int(x) for x in m[3].split()] for m in re.finditer(r'\[(\w+) (\d+)\] = \[([^]]*)\]',source)}
def generate():
 p=H/'frozen-candidates/p13-scene-reconstruction';m=json.loads((H/'generated/manifest.json').read_text());old=arrays((p/'generated/src/module982.sc').read_text());assert len(old['sdStarts'])==1593 and len(old['sdPageData'])==1552*8
 docs=m['document_routes'];N=1799-1600;data={n:[] for n in TABLES};data['fbStarts']=[-1]*N;data['fbCounts']=[0]*N
 for r in docs:data['fbStarts'][r['document_id']-1600]=1552+r['first_page'];data['fbCounts'][r['document_id']-1600]=r['page_count']
 for page in m['pages']:
  data['fbPageData'].extend(page['fields']);data['fbTextResources'].append(page['resource']);data['fbAudioModules'].append(page['audio_module']);data['fbPageDurations'].append(page['duration_ticks'])
 from date_source import source as date_source,PUBLICS,LOCALS
 template=next(r['text'] for r in m['canonical_records'] if r['id']=='P14.READ.001');prefix,suffix=template.split('{repair_date}');data['fbDatePrefix']=list(prefix.encode('ascii'));data['fbDateSuffix']=list(suffix.encode('ascii'))
 bank=';;; Sierra Script 1.0 - (do not remove this comment)\n; New class-free P14 presentation data. Ending director remains unimplemented.\n(script# 999)\n'+PUBLICS+'\n(local\n'+LOCALS+''.join(' ['+n+' '+str(len(v))+'] = ['+' '.join(map(str,v))+']\n' for n,v in data.items())+')\n(procedure (finaleBankAt table index)\n (switch table\n'+''.join(f' ({i} (if (or (< index 0) (>= index {len(data[n])})) (return 0)) (return [{n} index]))\n' for i,n in enumerate(TABLES,21))+') (return 0))\n'
 bank+=date_source(prefix,suffix)
 (H/'generated/module999.sc').write_text(bank)
 def apply(source):
  before=methods(source);changes={}
  assert arrays(source)==old
  for n,table,bad in [('sdRoute',21,-1),('sdPageCount',22,0)]:
   sig=before[n].index(')')+1
   extra=f'\n (if (or (== document 1800) (== document 1801)) (return '+('(if (proc999_5 0 0) 0 else -1)' if n=='sdRoute' else '(proc999_5 0 0)')+'))\n'
   extra+=f' (if (and (>= document 1600) (<= document 1798))\n  (if (not ((ScriptID 985 0) hStaticRange: {table} (- document 1600) 1)) (return {bad}))\n  (return (proc999_0 {table} (- document 1600))))\n'
   changes[n]=before[n][:sig]+extra+before[n][sig:]
  load=before['sdLoad'];start=load.index('        (= index (* row 8))');end=load.index('        ; Per-page resource')
  retained=load[start:end];delegated='\n (if (>= row 1552)\n  (if (>= row '+str(1552+len(m['pages']))+') (= sdFailure 1) (return 0))\n  (= row (- row 1552)) (= index (* row 8))\n  (if (or '+ ' '.join(f'(not ((ScriptID 985 0) hStaticRange: {t} {idx} {count}))' for t,idx,count in [(23,'index',8),(24,'row',1),(25,'row',1),(26,'row',1)])+') (= sdFailure 5) (return 0))\n'+''.join(f'  (= {prop} (proc999_0 23 (+ index {i})))\n' for i,prop in enumerate(['sdEntry','sdLineKey','sdPart','sdPartCount','sdSpeaker','sdVoice','sdHeader','sdBytes']))+''.join(f'  (= {prop} (proc999_0 {t} row))\n' for t,prop in [(24,'sdResource'),(25,'sdAudioModule'),(26,'sdVoiceEnd')])+' else\n'+retained+')\n'
  load=load[:start]+delegated+load[end:]
  load=load.replace('(!= sdResource 214))','(!= sdResource 214) (!= sdResource 215))').replace('(!= sdAudioModule 925))))','(!= sdAudioModule 925) (!= sdAudioModule 926))))');header=next(p['header_entry'] for p in m['pages'] if p['speaker_id']=='frankie')
  sig=load.index(')')+1
  special=f'''
 (if (or (== sdDocument 1800) (== sdDocument 1801))
  (= sdPartCount (proc999_5 0 0))
  (if (or (< sdPartCount 1) (< sdPage 0) (>= sdPage sdPartCount)) (= sdFailure 1) (return 0))
  (= sdBytes (proc999_6 sdPage @sdTextBuffer))
  (if (or (< sdBytes 1) (> sdBytes 153)) (= sdFailure 5) (return 0))
  (= sdEntry 0) (= sdLineKey sdDocument) (= sdPart sdPage) (= sdSpeaker 3)
  (= sdVoice 0) (= sdAudioModule 0) (= sdVoiceEnd 0) (= sdResource 215) (= sdHeader {header})
  (GetFarText 215 sdHeader @sdHeaderBuffer) (return 1))
'''
  load=load[:sig]+special+load[sig:];changes['sdLoad']=load
  draw=before['sdDraw'];draw=draw.replace('@sdTextBuffer 0 308','@sdTextBuffer (if (>= sdDocument 1600) 1 else 0) 308').replace('@sdHeaderBuffer 0 204','@sdHeaderBuffer (if (>= sdDocument 1600) 1 else 0) 204').replace('105 0','105 (if (>= sdDocument 1600) 1 else 0)');changes['sdDraw']=draw
  changes['hStaticAt']=before['hStaticAt'].replace('(switch table','(switch table\n'+''.join(f' ({t} (return (proc999_0 {t} index)))\n' for t in range(21,29)))
  # Retire the new date binding on close, restore and replacement by old/static text.
  interrupt=before['sdInterrupt'];sig=interrupt.index(')')+1
  changes['sdInterrupt']=interrupt[:sig]+'\n (if (or (== reason 13) (== reason 14)) (proc999_1))\n'+interrupt[sig:]
  opened=before['sdOpen'];sig=opened.index(')')+1
  changes['sdOpen']=opened[:sig]+'\n (if (and (!= document 1800) (!= document 1801)) (proc999_1))\n'+opened[sig:]
  after=merge(source,changes);assert arrays(after)==old
  assert re.findall(r'\(method \(([^)]*)\)',source)==re.findall(r'\(method \(([^)]*)\)',after)
  assert all(methods(after)[n]==body for n,body in before.items() if n not in changes)
  return after
 for stage,src in [('src',p/'generated/src'),('window-src',p/'generated/window-src')]:
  dst=H/'generated'/stage;dst.mkdir(exist_ok=True)
  for path in src.glob('*.sc'):shutil.copy2(path,dst/path.name)
  (dst/'module982.sc').write_text(apply((src/'module982.sc').read_text()));(dst/'module999.sc').write_text(bank)
 # Existing static table IDs and chunk offsets remain exact. Append new tables.
 oldstatic=json.loads((p/'generated/static/manifest.json').read_text());tables=oldstatic['tables'];chunks=[]
 for t in tables:
  assert t['first_chunk']==len(chunks)
  for i in range(0,t['count'],20):
   v=t['values'][i:i+20];chunks.append(''.join(f'{x&65535:05d} ' for x in v+[0]*(20-len(v))))
 for tid,n in enumerate(TABLES,21):
  v=data[n];t=dict(id=tid,module=982,name=n,count=len(v),first_chunk=len(chunks),source='generated/module999.sc',source_sha256=sha(bank.encode()),values=[x&65535 for x in v],delegated_script=999,delegated_export=0);tables.append(t)
  for i in range(0,len(v),20):
   w=v[i:i+20];chunks.append(''.join(f'{x&65535:05d} ' for x in w+[0]*(20-len(w))))
 resources=[240,241,244,245];assert len(chunks)<=480*len(resources)
 static=H/'generated/static';static.mkdir(exist_ok=True)
 for i,n in enumerate(resources):(static/f'{n}.text.bin').write_bytes(b''.join(c.encode()+b'\0' for c in chunks[i*480:(i+1)*480]))
 for stage in ['src','window-src']:
  path=H/'generated'/stage/'module985.sc';s=path.read_text();oldm=methods(s);changes={}
  for name,field in [('hStaticCount','count'),('hStaticFirst','first_chunk')]:changes[name]=oldm[name].replace('(switch table','(switch table\n'+''.join(f' ({t["id"]} (return {t[field]}))\n' for t in tables[20:]))
  changes['hStaticOwner']=oldm['hStaticOwner'].replace('(switch table','(switch table\n'+''.join(f' ({t["id"]} (return (ScriptID 982 0)))\n' for t in tables[20:]))
  changes['hStaticLoad']=oldm['hStaticLoad'].replace('(>= chunk 1440)','(>= chunk 1920)').replace('(if (< chunk 960) 241 else 244)','(if (< chunk 960) 241 else (if (< chunk 1440) 244 else 245))')
  changes['hStaticAll']=oldm['hStaticAll'].replace('(<= table 20)','(<= table 28)')
  path.write_text(merge(s,changes))
 (static/'manifest.json').write_text(json.dumps(dict(tables=tables,resources=resources,chunks=len(chunks),prior_table_ids_and_chunk_offsets_preserved=True,append_only_integrity_capacity=True),indent=2)+'\n')
 contract=dict(status='CANDIDATE_NEW_BANK',bank_script=999,new_classes=0,new_selectors=0,prior_pages=1552,prior_slots=1593,added_pages=len(m['pages']),bank_documents=[1600,1798],all_old_arrays_exact=True,changed_scene_methods=['sdRoute','sdPageCount','sdLoad','hStaticAt','sdDraw','sdOpen','sdInterrupt'],new_static_table_ids=list(range(21,29)),static_resources=resources,static_chunks=len(chunks),dynamic_date_runtime_pending=False)
 (H/'generated/extension-contract.json').write_text(json.dumps(contract,indent=2)+'\n');print(contract)
if __name__=='__main__':generate()
