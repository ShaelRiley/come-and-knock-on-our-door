#!/usr/bin/env python3
"""Pack the reviewed whole-source P05 candidate; no GUI/runtime invocation."""
from pathlib import Path
import sys,json,hashlib,shutil,re,struct
N=Path(__file__).resolve().parent;R=N.parent;H=R/'p05-host-reconstruction';STATUS=N/'STAGING-STATUS.json'
STATUS.write_text('{"status":"RUNNING","native_acceptance":false}\n');sys.dont_write_bytecode=True
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(ok,why):
 if not ok:raise RuntimeError(why)
def read(p):return json.loads(Path(p).read_text())
def identity(p):return {'bytes':Path(p).stat().st_size,'sha256':sha(p)}
def check(p,wanted):require(identity(p)==wanted,'Changed input '+str(p))
def dump(p,v):Path(p).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
try:
 require(not sys.flags.optimize,'Optimized staging is forbidden');require(len(sys.argv)==1,'No source/namespace override')
 review=R/'p05-host-independent-review/REVIEW-RESULT.json';require(sha(review)=='1d33e8c7bc9d2bcf8022b5a8d9d4f8c5594eb847c9ff6435e309d6d8cf1ca580','Final independent host receipt changed')
 gate=read(H/'VERIFICATION.json');require(gate['status']=='PASS_SOURCE_EMITTED_STATIC_ONLY','Current complete host verifier has not passed')
 require(sha(H/'INPUTS.json')==gate['input_manifest_sha256']=='3702d7501adb5602f8daff63873eea7e516fe564c7f567170a646c51b2ffb0e2','Host input seal differs from final reviewed universe')
 inputs=read(H/'INPUTS.json')
 for root,key in [(H,'local'),(R,'external')]:
  for file,wanted in inputs[key].items():check(root/file,wanted)
 for file,digest in gate['proofs'].items():require(sha(H/file)==digest,'Host proof changed: '+file)
 B=H/'build/coherent';receipt=read(B/'compile-receipt.json');require(receipt['status']=='PASS_FRESH_COMPILE','No coherent compile')
 require(receipt['class_owners']==[0,0,980,981,982,983,984,985,986],'Class universe mismatch')
 require([r['module'] for r in receipt['modules']]==[980,981,982,983,984,985,986,0],'Module universe mismatch')
 sys.path.insert(0,str(N/'tools'));from resource_codec import encode,decode
 resources={};resource_inputs={}
 for item in read(B/'verification-checkpoint/reference/resources.json'):
  key=(item['type'],item['number']);p=B/'verification-checkpoint/assets/resources'/item['extracted_path'];require(sha(p)==item['sha256'] and p.stat().st_size==item['size'],'Static resource differs')
  require(key not in resources,'Duplicate static resource');resources[key]=p.read_bytes();resource_inputs[f'{key[0]}:{key[1]}']=identity(p)
 for row in receipt['modules']:
  n=row['module'];require(row['combined_bytes']<=65535,'SCI16 segment limit')
  for kind,suffix,label in [(2,'','script'),(17,'.hep','heap')]:
   p=B/f'compiled/{n}.scr.bin{suffix}';require(sha(p)==row[label+'_sha256'],'Compiled module differs');resources[kind,n]=p.read_bytes();resource_inputs[f'{kind}:{n}']=identity(p)
 require(resources[6,996]==struct.pack('<18H',*sum(([0,n] for n in receipt['class_owners']),[])),'Class vocabulary bytes differ')
 speech={};origins={}
 def add(root,file,wanted,owner):
  p=root/file;check(p,wanted);name=p.name;require(re.fullmatch(r'[@#][0-9A-Z]{7}\.\d{3}',name) is not None,'Speech filename contract')
  require(name not in speech,'Speech namespace collision '+name);speech[name]=p;origins[name]={'owner':owner,'source':str(p.relative_to(R)),**wanted}
 P=R/'p04-native-inventory-fix-reconstruction';require(sha(P/'inputs/LOCK.json')=='bea7f7c6a8ba07e1a0d29a65c30894b0648a5438c31a912808bfef524d425712','Accepted P04 audio lock changed');lock=read(P/'inputs/LOCK.json')
 for folder,key in [('base-speech','preserved_speech'),('p04-scene/speech','added_speech')]:
  for file,wanted in lock[key].items():add(P/'inputs'/folder,file,wanted,'preserved P01-P04')
 require(len(speech)==404,'Preserved speech count')
 S=R/'p05-scene-reconstruction';require(sha(S/'evidence/immutable-export-lock.json')=='16b6171f2e047bae72a454cf9ed000acf828597f09f4b9a04d37275454d4ea6a','Accepted P05 scene lock changed');lock=read(S/'evidence/immutable-export-lock.json')['identity']['assets']
 for file,wanted in lock.items():
  if file.startswith('generated/speech/'):add(S,file,wanted,'accepted P05/VC01')
 require(len(speech)==528,'P05 speech count')
 S=R/'contest-scene-reconstruction';require(sha(S/'evidence/immutable-export-lock.json')=='229cb2411cab10348c15471beadb6108738fdb5d7cb7c0032fdd8a387f2fb830','Accepted final Contest scene lock changed');lock=read(S/'evidence/immutable-export-lock.json')['files']
 for file,wanted in lock.items():
  if file.startswith('generated/speech/'):add(S,file,wanted,'accepted shared Contest')
 runtime=R/'runtime/stock-scummvm/usr/games/scummvm';require(sha(runtime)=='050ed72eba6fd5760d87a3decc5425d74760115b2d77a71f5c6876aa1f96e0ad','Selected runtime is not pinned stock2026.3.0')
 game=N/'game';require(not game.exists(),'Candidate game already exists; use a reviewed new namespace rather than overwrite it')
 staging=N/'staging';require(not staging.exists(),'Prior incomplete staging requires explicit inspection');staging.mkdir()
 mapping,volume=encode(resources);require(decode(mapping,volume)==resources,'Packed resource roundtrip failed')
 (staging/'resource.map').write_bytes(mapping);(staging/'resource.000').write_bytes(volume)
 for name,p in speech.items():shutil.copy2(p,staging/name)
 expected={'resource.map':identity(staging/'resource.map'),'resource.000':identity(staging/'resource.000'),**{n:identity(p) for n,p in speech.items()}}
 require({p.name for p in staging.iterdir()}==set(expected),'Unexpected game output files')
 for name,wanted in expected.items():check(staging/name,wanted)
 staging.rename(game)
 target='cakood-p05-reconstruction-20261006-r1'
 namespace={'target':target,'state_directory':target,'save_directory':'saves','config_filename':'scummvm.ini','engineid':'sci','gameid':'sci-fanmade','imports_older_saves':False,'native_acceptance':False,'music_limitation':'MUS11 is not activated; retained room music is provisional for contest presentation'}
 compatibility={'source_namespace':target,'format':'exact-whole-program-v1','modules':[{k:row[k] for k in ['module','source_sha256','script_sha256','heap_sha256','class_species']} for row in receipt['modules']],'class_owners':receipt['class_owners'],'selector_vocabulary_sha256':hashlib.sha256(resources[6,997]).hexdigest(),'class_vocabulary_sha256':hashlib.sha256(resources[6,996]).hexdigest()}
 compatibility['program_fingerprint']=hashlib.sha256(json.dumps(compatibility,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 compatibility['enforcement']='Wrapper-bound exact program identity plus fresh empty save directory; no historical save import or automatic migration is authorized.'
 compatibility['config_alias_is_not_compatibility']=True
 dump(N/'SAVE-COMPATIBILITY.json',compatibility)
 namespace['save_compatibility_sha256']=sha(N/'SAVE-COMPATIBILITY.json')
 dump(N/'NAMESPACE.json',namespace)
 (N/'receipts').mkdir(exist_ok=True);shutil.copy2(review,N/'receipts/HOST-REVIEW-RESULT.json')
 dump(N/'PACKAGE-MANIFEST.json',{'schema':1,'independent_review_sha256':sha(review),'namespace':namespace,'files':expected,'resource_inputs':resource_inputs,'speech_origins':origins,'host_input_seal':sha(H/'INPUTS.json'),'host_verification_sha256':sha(H/'VERIFICATION.json'),'compiled_modules':receipt['modules'],'class_owners':receipt['class_owners'],'selector_vocabulary_sha256':hashlib.sha256(resources[6,997]).hexdigest(),'runtime_sha256':sha(runtime),'native_acceptance':False})
 dump(STATUS,{'status':'PASS_STATIC_NATIVE_CANDIDATE','package_manifest_sha256':sha(N/'PACKAGE-MANIFEST.json'),'files':len(expected),'resources':len(resources),'speech_files':len(speech),'native_acceptance':False,'launch_performed':False,'remaining':['Fresh native route/restore/audio proof','MUS11 and player-facing reduced-motion setting']})
 print(json.dumps(read(STATUS),indent=2))
except BaseException as e:
 dump(STATUS,{'status':'FAIL','error':str(e),'native_acceptance':False});raise
