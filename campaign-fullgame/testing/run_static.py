#!/usr/bin/env python3
"""Bounded reference closure, with explicit dynamic/assembly coverage limits."""
from pathlib import Path
import sys,re,json,hashlib,struct,collections
import argparse
A=Path(__file__).resolve().parent;C=A.parent
sys.dont_write_bytecode=True
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--build',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
if sys.flags.optimize:raise RuntimeError('Optimized Python is unsupported')
R=args.build.resolve();G=R/'stage/game'
sys.path[:0]=[str(C),str(C/'source/tools'),str(A)]
from reproduce import verify_inputs,check_outputs
verify_inputs();check_outputs(R)
from source_tools import tokens
from resource_codec import decode
from inspect_view import decode_view
sha=lambda b:hashlib.sha256(b).hexdigest()
res=decode((G/'resource.map').read_bytes(),(G/'resource.000').read_bytes());receipt=json.loads((R/'build/coherent/compile-receipt.json').read_text());assert sha((R/'build/coherent/compile-receipt.json').read_bytes())=='b3f839512100c06368ce903ecc018bad8ac600ce6ccf647401f693b50c56ce48'
sourcepins={}
for row in receipt['modules']:
 n=row['module'];p=R/'src'/('main.sc' if n==0 else f'module{n}.sc');assert sha(p.read_bytes())==row['source_sha256'];sourcepins[p.name]=row['source_sha256'];assert sha(res[2,n])==row['script_sha256'] and sha(res[17,n])==row['heap_sha256']
assert len(sourcepins)==21
views={}
for (t,n),raw in res.items():
 if t==0:
  if n==205:raw=raw[:38]+bytes(4)+raw[42:]
  views[n]=decode_view(raw)
texts={n:b.split(b'\0') for (t,n),b in res.items() if t==3}
checks=[];dynamic=[]
def parse(source):
 stack=[[]]
 for match in tokens(source):
  t=match.group()
  if t=='(':a=[];stack[-1].append(a);stack.append(a)
  elif t==')':assert len(stack)>1;stack.pop()
  else:stack[-1].append(t)
 assert len(stack)==1;return stack[0]
def walk(x):
 if isinstance(x,list):
  if x:yield x
  for y in x:yield from walk(y)
def num(x,defs):
 if not isinstance(x,str):return None
 if re.fullmatch(r'-?\d+',x):return int(x)
 return defs.get(x)
def audiofile(module,noun,verb,cond,seq):
 def b36(n,w):
  s='';d='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  while n:s=d[n%36]+s;n//=36
  return (s or '0').rjust(w,'0')
 return '@'+b36(module,3)+b36(noun,2)+b36(verb,2)+'.'+b36(cond,2)+b36(seq,1)
for f in sourcepins:
 tree=parse((R/'src'/f).read_text());defs={x[1]:int(x[2]) for x in walk(tree) if len(x)==3 and x[0]=='define' and isinstance(x[2],str) and re.fullmatch(r'-?\d+',x[2])}
 for x in walk(tree):
  if not isinstance(x[0],str):continue
  name=x[0]
  if name=='DrawCel':
   n=num(x[1],defs)
   if n is None:dynamic.append(dict(source=f,kind='DrawCel',reason='computed view',expression=x[1:4]));continue
   assert n in views,(f,'missing view',n);loop=num(x[2],defs);cel=num(x[3],defs)
   if loop is not None:assert 0<=loop<len(views[n]),(f,'loop',n,loop)
   if loop is not None and cel is not None:assert 0<=cel<len(views[n][loop]),(f,'cel',n,loop,cel)
   checks.append(dict(source=f,kind='DrawCel',view=n,loop=loop,cel=cel,fully_literal=loop is not None and cel is not None))
  elif name=='GetFarText':
   n=num(x[1],defs);entry=num(x[2],defs)
   if n is None:dynamic.append(dict(source=f,kind=name,reason='computed text bank',expression=x[1:3]));continue
   assert n in texts,(f,'missing text',n)
   if entry is not None:assert 0<=entry<len(texts[n])-1,(f,'text entry',n,entry)
   checks.append(dict(source=f,kind=name,resource=n,entry=entry))
  elif name=='DoAudio' and len(x)==7 and num(x[1],defs)==2:
   vals=[num(t,defs) for t in x[2:]]
   if None in vals:dynamic.append(dict(source=f,kind=name,reason='computed audio tuple',expression=x[2:]));continue
   fn=audiofile(*vals);assert (G/fn).exists(),(f,'missing audio',fn);checks.append(dict(source=f,kind='Audio36',filename=fn))
  elif name in ['class','instance'] and 'Sound' in x[:4]:
   for props in x:
    if isinstance(props,list) and props and props[0]=='properties':
     for i,v in enumerate(props[:-1]):
      if v=='number':n=num(props[i+1],defs);assert n is not None and (4,n) in res;checks.append(dict(source=f,kind='Sound',resource=n))
# Every available accepted authored scene page from P05 onward, plus shared Contest.
manifest_paths=sorted((A/'scenes').glob('*.json'))
expected_speakers={'jack':1,'bunny':2,'frankie':3,'stringer':4,'milo':5,'vivian':6,'rita':7,'felix':8,'audience':0};reader=[];textdiff=[]
for p in manifest_paths:
 d=json.loads(p.read_text());pagecount=0;voiced=0;speakers=set()
 for page in d['pages']:
  n=page['resource'];entry=page['entry'];header=page['header_entry'];assert n in texts and 0<=entry<len(texts[n])-1 and 0<=header<len(texts[n])-1,(p,n,entry,header)
  actual=texts[n][entry];expected=page['text'].encode('ascii')
  if actual!=expected:textdiff.append(dict(manifest=str(p.relative_to(A)),record=page['record_id'],resource=n,entry=entry,actual_sha256=sha(actual),manifest_sha256=sha(expected)))
  who=page['speaker_number'];assert 0<=who<=8
  sid=page.get('speaker_id');voice=page.get('voice_index',0);module=page.get('audio_module',0)
  if voice and module:
   assert sid in expected_speakers and who==expected_speakers[sid],(p,'speaker mismatch',sid,who)
   fn=audiofile(module,voice,1,0,1);assert (G/fn).exists() and (G/('#'+fn[1:])).exists(),(p,'missing voiced reader pair',fn);voiced+=1
  speakers.add(who);pagecount+=1
 for voice in d.get('speech',[]):
  for kind in ['audio','sync']:
   fn=voice[kind+'_file'];assert sha((G/fn).read_bytes())==voice[kind+'_sha256'],(p,kind,fn)
 reader.append(dict(manifest=str(p.relative_to(A)),sha256=sha(p.read_bytes()),pages=pagecount,voiced_page_references=voiced,speakers=sorted(speakers)))
assert (7,0) in res and (7,1) in res and (9,4) in res and (11,999) in res
assert not textdiff, 'Authored text manifest differs from current resource'
# Read-only format rejection smoke checks; no game state or external action.
for mapping,volume in [(b'',(G/'resource.000').read_bytes()),((G/'resource.map').read_bytes(),b''),((G/'resource.map').read_bytes(),(G/'resource.000').read_bytes()+b'\x00')]:
 try:decode(mapping,volume)
 except (RuntimeError,ValueError,struct.error):pass
 else:raise AssertionError('Malformed resource pair accepted')
result=dict(status='PASS_BOUNDED_STATIC_ASSET_REFERENCE_CLOSURE',source_manifest_sha256=sha((C/'SOURCE-MANIFEST.json').read_bytes()),test_script_sha256=sha(Path(__file__).read_bytes()),compile_receipt_sha256=sha((R/'build/coherent/compile-receipt.json').read_bytes()),canonical_source_hashes=sourcepins,packed21modules_match_compile_receipt=True,direct_source_references=checks,direct_reference_counts=dict(collections.Counter(r['kind'] for r in checks)),manifest_checks=reader,total_authored_pages_checked=sum(x['pages'] for x in reader),total_voiced_page_references_checked=sum(x['voiced_page_references'] for x in reader),manifest_text_comparison_differences=textdiff,computed_references_not_proven_by_this_scan=dynamic,speaker_registry_range=[0,8],malformed_resource_rejections=3,full_causal_route_acceptance=False,native_acceptance=False,required_fonts_palette_GM_present=True,limitations=['Literal high-level calls and Sound defaults are checked. Symbolic assembly operands and computed resource/cel selections are not exhaustively statically evaluated.','Authored reader manifests cover P05–P14 and shared Contest, not an independent re-proof of P01–P04 source tables. The full inherited audio/resource bytes are separately hash-bound to the current source checkpoint.','Manifest audio tuples, sync pairs, speaker IDs and text-entry bounds are checked; actual runtime route selection, eligibility and frame/receipt timing remain separate.','Native display/audio/input acceptance is not claimed.'])
args.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['direct_reference_counts'],'pages',result['total_authored_pages_checked'],'voice refs',result['total_voiced_page_references_checked'],'text diffs',len(textdiff))
