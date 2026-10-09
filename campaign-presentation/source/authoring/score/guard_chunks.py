"""A07 complete decimal guard partition with preserved transport prefixes."""
from pathlib import Path
import hashlib,json,shutil

def guard_split(home,prefix,rows):
 amendment=home/'metadata/guard-pages.json'
 a=json.loads(amendment.read_text());assert a['allocation']['resources']==[248,260,261]
 pages={248:bytearray()};entry={248:0}
 for row in a['protected_prefixes']:
  n=row['resource'];data=(home/'prefixes'/f'{n}.text.bin').read_bytes()
  assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
  pages[n]=bytearray(data);entry[n]=data.count(b'\0')
 ids=[248,260,261];page=0;records=[];access=[]
 for name,values,mutable in rows:
  if mutable:continue
  groups=[]
  for k in range(0,len(values),20):
   chunk=(''.join(f'{v&65535:05d} 'for v in values[k:k+20]+[0]*(20-len(values[k:k+20])))+'\0').encode()
   ceiling=59400 if ids[page]==248 else 60000
   if len(pages[ids[page]])+len(chunk)>ceiling:page+=1
   assert page<len(ids),'A07 pages exhausted'
   n=ids[page];assert len(pages[n])+len(chunk)<=60000
   index=entry[n];pages[n].extend(chunk);entry[n]+=1
   records.append(dict(row=name,row_chunk=k//20,first_word=k,word_count=min(20,len(values)-k),resource=n,text_index=index,byte_sha256=hashlib.sha256(chunk).hexdigest()))
   if groups and groups[-1]['resource']==n:groups[-1]['chunks']+=1
   else:groups.append(dict(resource=n,first_row_chunk=k//20,first_text_index=index,chunks=1))
  access.append((name,len(values),groups))
 for n,data in pages.items():(home/f'generated/{n}.text.bin').write_bytes(data)
 lines=[f'(procedure ({prefix}Verify &tmp index slot word digit value i chunk)',f'(for ((= i 0)) (< i 64) ((++ i)) (= [{prefix}Buffer i] 0))']
 for name,count,groups in access:
  lines += [f'(for ((= index 0)) (< index {count}) ((++ index))', '(if (== (mod index 20) 0)', '(= chunk (/ index 20))']
  for group in groups:
   low=group['first_row_chunk'];high=low+group['chunks'];n=group['resource'];at=group['first_text_index']
   lines.append(f'(if (and (>= chunk {low}) (< chunk {high})) (GetFarText {n} (+ {at} (- chunk {low})) @{prefix}Buffer))')
  lines += [')','(= slot (mod index 20)) (= value 0)','(for ((= i 0)) (< i 5) ((++ i))',f'(= word [{prefix}Buffer (+ (* slot 3) (/ i 2))])','(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))','(if (or (< digit 0) (> digit 9)) (return 0))','(= value (+ (* value 10) digit)))',f'(if (!= (>> [{prefix}Buffer (+ (* slot 3) 2)] 8) 32) (return 0))',f'(if (!= [{name} index] value) (return 0)))']
 lines+=['(return 1))']
 (home/'generated/BROKER-GUARD-CHUNKS.json').write_text(json.dumps(dict(schema=1,amendment_sha256=hashlib.sha256(amendment.read_bytes()).hexdigest(),rows=[dict(name=n,words=len(v))for n,v,m in rows if not m],chunks=records,pages=[dict(resource=n,bytes=len(v),sha256_before_ui=hashlib.sha256(v).hexdigest())for n,v in pages.items()],protected_prefixes=a['protected_prefixes'],word_count=sum(len(v)for _,v,m in rows if not m)),indent=2)+'\n')
 return '\n'.join(lines)
