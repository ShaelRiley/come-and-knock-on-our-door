#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib,struct
N=Path(__file__).resolve().parent;OUT=N/'PACKAGE-CHECK.json';OUT.write_text('{"status":"RUNNING","native_acceptance":false}\n');sys.dont_write_bytecode=True
try:
 if sys.flags.optimize:raise RuntimeError('Optimized check forbidden')
 sys.path.insert(0,str(N/'tools'));from resource_codec import decode
 j=json.loads((N/'PACKAGE-MANIFEST.json').read_text());game=N/'game'
 if hashlib.sha256((N/'receipts/HOST-REVIEW-RESULT.json').read_bytes()).hexdigest()!=j['independent_review_sha256']:raise RuntimeError('Independent host receipt differs')
 if type(j.get('schema')) is not int or j['schema']!=1 or len(j['files'])!=780 or len(j['resource_inputs'])!=80 or len(j['speech_origins'])!=778:raise RuntimeError('Fixed native inventory extent mismatch')
 if j['host_input_seal']!='3702d7501adb5602f8daff63873eea7e516fe564c7f567170a646c51b2ffb0e2' or j['class_owners']!=[0,0,980,981,982,983,984,985,986]:raise RuntimeError('Source/class universe mismatch')
 if [r['module'] for r in j['compiled_modules']]!=[980,981,982,983,984,985,986,0]:raise RuntimeError('Compiled module inventory mismatch')
 if {p.name for p in game.iterdir()}!=set(j['files']):raise RuntimeError('Game file set mismatch')
 for name,wanted in j['files'].items():
  p=game/name
  if p.stat().st_size!=wanted['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=wanted['sha256']:raise RuntimeError('Game file differs: '+name)
 resources=decode((game/'resource.map').read_bytes(),(game/'resource.000').read_bytes())
 if set(f'{t}:{n}' for t,n in resources)!=set(j['resource_inputs']):raise RuntimeError('Resource inventory mismatch')
 for key,data in resources.items():
  wanted=j['resource_inputs'][f'{key[0]}:{key[1]}']
  if len(data)!=wanted['bytes'] or hashlib.sha256(data).hexdigest()!=wanted['sha256']:raise RuntimeError('Packed resource differs')
 for row in j['compiled_modules']:
  for kind,part in [(2,'script'),(17,'heap')]:
   if hashlib.sha256(resources[kind,row['module']]).hexdigest()!=row[part+'_sha256']:raise RuntimeError('Packed compiled universe differs')
 if resources[6,996]!=struct.pack('<18H',*sum(([0,n] for n in j['class_owners']),[])):raise RuntimeError('Class vocabulary differs')
 if json.loads((N/'NAMESPACE.json').read_text())!=j['namespace'] or j['namespace']['imports_older_saves']:raise RuntimeError('Namespace mismatch')
 if hashlib.sha256((N/'SAVE-COMPATIBILITY.json').read_bytes()).hexdigest()!=j['namespace']['save_compatibility_sha256']:raise RuntimeError('Source save compatibility marker differs')
 OUT.write_text(json.dumps({'status':'PASS_PACKED_CANDIDATE_STATIC','files':len(j['files']),'resources':len(resources),'native_acceptance':False},indent=2)+'\n');print(OUT.read_text())
except BaseException as e:
 OUT.write_text(json.dumps({'status':'FAIL','error':str(e),'native_acceptance':False})+'\n');raise
