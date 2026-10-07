#!/usr/bin/env python3
"""Offline relocated source/generator/compile/native-package reproduction.

The 44-test result is hash-bound, not replayed here. No engine is launched.
Speech exports are stored once in the bundled native game and materialized from
exact accepted per-file identities, never synthesized by a fixture.
"""
from pathlib import Path
import sys,json,hashlib,shutil,subprocess,ast,importlib.util,argparse,os
P=Path(__file__).resolve().parent;STATUS=P/'LAST-REBUILD.json';STATUS.write_text('{"status":"RUNNING","native_acceptance":false}\n');sys.dont_write_bytecode=True
EXPECTED_ASSEMBLY='cdcb32f5f0607165f4db1c0c2556dea87fdce81d809b9897e02336177b155970';EXPECTED_EXPORTS='0e07d924a2ba9887b3d09dfdf6f443c1e6371c32d55f228df27187e15e4d479f'
HOST_SEAL='3702d7501adb5602f8daff63873eea7e516fe564c7f567170a646c51b2ffb0e2';NATIVE_SEAL='dcf4be1c89dba28a4557ac9b9176d7b9894f40be8eeec1aa74f64b0f7473d3bb'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(ok,message):
 if not ok:raise RuntimeError(message)
def load(p):return json.loads(Path(p).read_text())
def identity(p):p=Path(p);return {'bytes':p.stat().st_size,'sha256':sha(p)}
def check(p,wanted):require(identity(p)=={k:wanted[k] for k in ['bytes','sha256']},'Input differs: '+str(p))
def relative(s):
 p=Path(s);require(not p.is_absolute() and '..' not in p.parts and bool(p.parts),'Unsafe package path');return p
try:
 require(not sys.flags.optimize,'Optimized reproduction is forbidden')
 for key in ['CAKOOD_BUILD','CAKOOD_CHECKPOINT','CAKOOD_SELECTORS']:require(not os.environ.get(key),'Unbound environment override '+key)
 parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True,help='New, nonexistent reproduction directory');args=parser.parse_args();O=args.out.resolve();require(not O.exists(),'Output already exists; no existing work or saves are overwritten')
 require(sha(P/'ASSEMBLY-INVENTORY.json')==EXPECTED_ASSEMBLY,'Assembly inventory identity changed');require(sha(P/'ACCEPTED-SPEECH-EXPORTS.json')==EXPECTED_EXPORTS,'Speech export map identity changed')
 inventory=load(P/'ASSEMBLY-INVENTORY.json')['files']
 require(len(inventory)==1427,'Assembly membership extent changed')
 for file,meta in inventory.items():
  p=P/relative(file);require(not p.is_symlink(),'Package symlink forbidden');check(p,meta)
 BUNDLE=P/'workspace/rebuild';BH=BUNDLE/'p05-host-reconstruction';BN=BUNDLE/'p05-native-candidate-reconstruction'
 require(sha(BH/'INPUTS.json')==HOST_SEAL and sha(BN/'PACKAGE-MANIFEST.json')==NATIVE_SEAL,'Selected host/native identities changed')
 native=load(BN/'PACKAGE-MANIFEST.json');require(len(native['files'])==780 and len(native['resource_inputs'])==80 and len(native['speech_origins'])==778,'Native universe extent changed')
 exports=load(P/'ACCEPTED-SPEECH-EXPORTS.json');expected_exports={r['source']:{'bundled_game_file':'workspace/rebuild/p05-native-candidate-reconstruction/game/'+name,'bytes':r['bytes'],'sha256':r['sha256'],'owner':r['owner']} for name,r in native['speech_origins'].items()}
 require(exports==expected_exports,'Accepted source-export mapping differs')
 O.mkdir(parents=True);W=O/'workspace/rebuild';W.mkdir(parents=True)
 # Explicit workspace inventory only; omit the packaged game and build it fresh.
 prefix='workspace/rebuild/';gameprefix=prefix+'p05-native-candidate-reconstruction/game/'
 for file,meta in inventory.items():
  if file.startswith(prefix) and not file.startswith(gameprefix):
   dest=O/relative(file);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/file,dest)
 for file,row in exports.items():
  dest=W/relative(file);require(not dest.exists(),'Speech source shadows another input');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/row['bundled_game_file'],dest);check(dest,row)
 H=W/'p05-host-reconstruction';N=W/'p05-native-candidate-reconstruction';(H/'evidence').mkdir(exist_ok=True)
 # Invoke the exact fixed-membership predicates from the sealed public verifier.
 require(sha(H/'verify.py')=='fe59417685a6fa1ae5a2dda9b95cc3b78d8b2c4564cf76e09a663050ebc1edc4','Verifier source differs')
 tree=ast.parse((H/'verify.py').read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('require','inventory')];require(len(defs)==2,'Inventory predicate shape')
 env={'H':H,'R':W,'json':json,'Path':Path,'sha':sha};exec(compile(ast.Module(body=defs,type_ignores=[]),str(H/'verify.py'),'exec'),env);env['inventory']()
 compiler=W/'p03-editable-checkpoint/toolchain/scicompile';require(sha(compiler)=='608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e','Compiler differs');compiler.chmod(0o755)
 require(not (H/'build').exists(),'Rebuild must start without host compiled outputs')
 commands=['visual-work/generate_fragment.py','tools/make_courtyard_controls.py','tools/generate_static_guards.py','generate_contest_labels.py','derive.py','build.py','tests/verify_architecture.py','tests/audit_emitted.py']
 for command in commands:
  log=O/(Path(command).stem+'.log')
  with log.open('w') as f:r=subprocess.run([sys.executable,command],cwd=H,stdout=f,stderr=subprocess.STDOUT)
  require(r.returncode==0,'Fresh command failed: '+command+'; see '+str(log))
 env['inventory']() # Every regenerated authoritative source/data input is identical.
 B=H/'build/coherent';receipt=load(B/'compile-receipt.json');require(receipt['status']=='PASS_FRESH_COMPILE','Fresh compile receipt missing')
 require(receipt['modules']==native['compiled_modules'] and receipt['class_owners']==native['class_owners'],'Fresh script/heap/source/ABI universe differs')
 resources={}
 for row in load(B/'verification-checkpoint/reference/resources.json'):
  p=B/'verification-checkpoint/assets/resources'/row['extracted_path'];require(sha(p)==row['sha256'],'Fresh static resource differs');resources[row['type'],row['number']]=p.read_bytes()
 for row in receipt['modules']:
  for kind,suffix in [(2,''),(17,'.hep')]:resources[kind,row['module']]=(B/f'compiled/{row["module"]}.scr.bin{suffix}').read_bytes()
 require(set(f'{t}:{n}' for t,n in resources)==set(native['resource_inputs']),'Fresh resource set differs')
 for (t,n),data in resources.items():require({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}==native['resource_inputs'][f'{t}:{n}'],'Fresh resource payload differs')
 spec=importlib.util.spec_from_file_location('checkpoint13_resource_codec',N/'tools/resource_codec.py');codec=importlib.util.module_from_spec(spec);spec.loader.exec_module(codec)
 mapping,volume=codec.encode(resources);require(codec.decode(mapping,volume)==resources,'Native resource roundtrip failed')
 game=N/'game';require(not game.exists(),'Fresh native output must not preexist');game.mkdir();(game/'resource.map').write_bytes(mapping);(game/'resource.000').write_bytes(volume)
 for name,row in native['speech_origins'].items():shutil.copy2(W/row['source'],game/name)
 require({p.name for p in game.iterdir()}==set(native['files']),'Fresh native file membership differs')
 for name,wanted in native['files'].items():check(game/name,wanted)
 with (O/'native-package-check.log').open('w') as f:r=subprocess.run([sys.executable,str(N/'check.py')],stdout=f,stderr=subprocess.STDOUT)
 require(r.returncode==0,'Independent packaged candidate check failed')
 original_suite=BH/'evidence/suite.json';require(sha(original_suite)=='11cffdf624f1dc20c450b96fba84186db472decac0975444597d4b86a8187d2e','Frozen44-test evidence changed')
 report={'status':'PASS_RELOCATED_GENERATORS_COMPILE_PACKAGE','host_input_manifest_sha256':HOST_SEAL,'native_package_manifest_sha256':NATIVE_SEAL,'fresh_modules':receipt['modules'],'fresh_resources':80,'fresh_game_files':780,'materialized_exact_speech_exports':778,'fresh_host_build_was_absent':True,'regenerated_generators':commands[:4],'game_file_hashes_byte_identical':True,'full44_test_receipt_sha256':sha(original_suite),'full44_tests_rerun':False,'native_acceptance':False,'engine_launched':False,'original_workspace_access_required':False,'output':str(O)}
 (O/'REBUILD-RESULT.json').write_text(json.dumps(report,indent=2)+'\n');STATUS.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
except BaseException as e:
 STATUS.write_text(json.dumps({'status':'FAIL','error':str(e),'native_acceptance':False},indent=2)+'\n');raise
