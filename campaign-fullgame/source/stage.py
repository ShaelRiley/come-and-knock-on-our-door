"""Stage an unlaunched exact-program asset closure; no gameplay acceptance inferred."""
from pathlib import Path
import json,hashlib,sys,shutil,struct
H=Path(__file__).resolve().parent;B=H/'build/coherent';O=H/'stage';G=O/'game'
assert not O.exists(),'Refuse staged program overwrite'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
c=json.loads((B/'compile-receipt.json').read_text());assert c['status']=='PASS_FRESH_COMPILE'
assert {r['module'] for r in c['modules']}=={0,*range(980,1000)}
sys.path.insert(0,str(H/'tools'));from resource_codec import encode,decode
resources={}
for r in json.loads((B/'verification-checkpoint/reference/resources.json').read_text()):
 p=B/'verification-checkpoint/assets/resources'/r['extracted_path'];assert sha(p)==r['sha256'];resources[r['type'],r['number']]=p.read_bytes()
for r in c['modules']:
 canonical=H/'src'/('main.sc' if r['module']==0 else f'module{r["module"]}.sc');assert sha(canonical)==r['source_sha256']
 for kind,ext,key in [(2,'','script_sha256'),(17,'.hep','heap_sha256')]:
  p=B/f'compiled/{r["module"]}.scr.bin{ext}';assert sha(p)==r[key];resources[kind,r['module']]=p.read_bytes()
assert resources[6,996]==struct.pack('<'+'H'*2*len(c['class_owners']),*sum(([0,n] for n in c['class_owners']),[]))
G.mkdir(parents=True)
a=json.loads((H/'AUDIO-INVENTORY.json').read_text())
for name,row in a['files'].items():
 p=B/'speech'/name;assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes'];shutil.copy2(p,G/name)
m,v=encode(resources);assert decode(m,v)==resources
(G/'resource.map').write_bytes(m);(G/'resource.000').write_bytes(v)
files={p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(G.iterdir())}
assert len(files)==1713
r={'status':'STATIC_STAGED_UNLAUNCHED_FULLGAME','compile_sha256':sha(B/'compile-receipt.json'),'files':files,'typed_resources':len(resources),'audio_manifest_sha256':sha(H/'AUDIO-INVENTORY.json'),'credit_selection_sha256':sha(H/'P14-CREDIT-URLS.json'),'source_mode':'editable_canonical_public_inputs','native_acceptance':False,'genuine_campaign_acceptance':False,'save_compatibility':'New game required; no prior native-save migration claimed'}
(O/'GAME-MANIFEST.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],len(files),len(resources),sha(O/'GAME-MANIFEST.json'))
