"""Stage an unlaunched exact-program asset closure; no gameplay acceptance inferred."""
from pathlib import Path
import json,hashlib,sys,shutil,struct
H=Path(__file__).resolve().parent;B=H/'build/coherent';O=H/'stage';G=O/'game'
assert not O.exists(),'Refuse staged program overwrite'
config=json.loads((H/'BUILD-PROFILE.json').read_text())
assert sys.argv[1:]==[{'A':'--phase-a','B':'--candidate','C':'--release'}[config['phase']]],'Explicit matching stage phase required'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
c=json.loads((B/'compile-receipt.json').read_text());assert c['status']=='PASS_FRESH_COMPILE'
assert c.get('diagnostic_traces') is False and c.get('trace_mode')=='removed-noop-ABI'
assert {r['module'] for r in c['modules']}==set(config['modules'])
assert c['phase']==config['phase'] and c['build_profile_sha256']==sha(H/'BUILD-PROFILE.json')
assert config['phase']=='A' or c.get('complete_candidate') is True,'Incomplete engineering compilation cannot be staged'
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
assert len(files)==config['audio_files']+2
r={'status':'STATIC_STAGED_UNLAUNCHED_FINISHING_CANDIDATE','phase':config['phase'],'fixture_category':config.get('fixture_category'),'release_eligible':config['phase']=='C','compile_sha256':sha(B/'compile-receipt.json'),'files':files,'typed_resources':len(resources),'audio_manifest_sha256':sha(H/'AUDIO-INVENTORY.json'),'credit_selection_sha256':sha(H/'P14-CREDIT-URLS.json'),'source_mode':'editable_canonical_finishing_inputs','checkpoint_contract':'A04_EXACT_VISUAL_NATIVE_PAIR','native_acceptance':False,'genuine_campaign_acceptance':False,'save_compatibility':config['save_lineage']+'; genuine New Game only; all predecessor saves belong to separate lineages'}
for name in ('CREDITS.txt','LICENSE.md','PLAYER-GUIDE.md','RIGHTS-CONTEXT.md'):
 shutil.copy2(H/'player-package'/name,O/name)
shutil.copytree(H/'rights',O/'rights')
(O/'GAME-MANIFEST.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],len(files),len(resources),sha(O/'GAME-MANIFEST.json'))
