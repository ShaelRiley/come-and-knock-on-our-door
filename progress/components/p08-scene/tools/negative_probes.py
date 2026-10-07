from pathlib import Path as _Path
import json as _Json
_REPORT=_Path(__file__).resolve().parents[1]/'evidence/negative-checks.json'
_REPORT.parent.mkdir(parents=True,exist_ok=True)
(_REPORT.parents[1]/'GATE-SEAL.json').unlink(missing_ok=True)
_REPORT.write_text('{"status":"RUNNING","native_acceptance":false}\n')
try:
 """Negative acceptance tests, in isolated hardlink copies with copy-on-replace edits."""
 from pathlib import Path
 import sys,json,shutil,subprocess,os,hashlib
 H=Path(__file__).resolve().parents[1];sys.dont_write_bytecode=True
 if sys.flags.optimize:raise RuntimeError('Run negative harness normally; it probes optimized child entry points')
 D=H/'negative-probes';D.mkdir(exist_ok=True)
 def clone(name):
  out=D/name
  if out.exists():shutil.rmtree(out)
  shutil.copytree(H,out,copy_function=os.link,ignore=shutil.ignore_patterns('negative-probes','portability','delivery','regression-probes','__pycache__','VERIFICATION.json','current-status.json'))
  # Every child may rewrite these status files; sever links before any child runs.
  for name in ['evidence/tests.json','SOURCE-SEAL.json','OUTPUT-SEAL.json']:
   p=out/name
   if p.exists():data=p.read_bytes();p.unlink();p.write_bytes(data)
  baseline=subprocess.run([sys.executable,'run.py','verify'],cwd=out,capture_output=True,text=True)
  if baseline.returncode:raise RuntimeError('Negative baseline is not clean: '+name+' '+baseline.stderr)
  return out
 def replace(root,name,data):
  p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.unlink(missing_ok=True);p.write_bytes(data)
 def run(root,args,log):
  # A planted stale PASS must be replaced by the attempted public entry point.
  for p in [root/'VERIFICATION.json',root/'evidence/current-status.json']:p.parent.mkdir(parents=True,exist_ok=True);p.unlink(missing_ok=True);p.write_text('{"status":"PASS_BOUND_COMPONENT"}\n')
  result=subprocess.run([sys.executable,*args],cwd=root,capture_output=True,text=True)
  (D/(log+'.log')).write_text(result.stdout+result.stderr)
  if result.returncode==0:raise RuntimeError('Negative unexpectedly succeeded: '+log)
  if log in ['changed_generator','changed_catalog','missing_helper']:wanted='Source inventory/hash mismatch'
  elif log=='mismatched_output_seal':wanted='Output belongs to another source seal'
  elif log.startswith('optimized'):wanted='Optimized Python forbidden'
  elif log in ['suite_empty','suite_extra']:wanted='Exact test inventory mismatch'
  elif log.startswith('suite_'):wanted='Non-exact clean test result'
  else:wanted='Output inventory/hash mismatch'
  if wanted not in result.stdout+result.stderr:raise RuntimeError('Wrong rejection reason for '+log+': '+result.stderr)
  for p in [root/'VERIFICATION.json',root/'evidence/current-status.json']:
   if json.loads(p.read_text())['status']!='FAILED':raise RuntimeError('Stale acceptance survived: '+log)
  return dict(name=log,returncode=result.returncode,clean_baseline_verified=True,rejection=wanted,stale_pass_cleared=True)
 rows=[]
 checks=[('changed_generator','generate.py'),('changed_catalog','inputs/authority/full-line-catalog.json'),('changed_pcm',next(str(p.relative_to(H)) for p in (H/'generated/speech').glob('@*'))),('changed_sync',next(str(p.relative_to(H)) for p in (H/'generated/speech').glob('#*'))),('changed_emitted982','build/coherent/compiled/982.scr.bin'),('changed_packed_fixture','generated/fixture-game/resource.000'),('changed_static244','generated/static/244.text.bin')]
 for name,path in checks:
  root=clone(name);raw=(root/path).read_bytes();replace(root,path,raw[:-1]+bytes([raw[-1]^1]));rows.append(run(root,['run.py','package'],name));shutil.rmtree(root)
 for name,path in [('missing_helper','tools/resource_codec.py'),('missing_text','generated/208.text.bin')]:
  root=clone(name);(root/path).unlink();rows.append(run(root,['run.py','verify'],name));shutil.rmtree(root)
 root=clone('extra_output');replace(root,'generated/speech/STALE.bin',b'stale');rows.append(run(root,['run.py','package'],'extra_output'));shutil.rmtree(root)
 root=clone('mismatched_output_seal');j=json.loads((root/'OUTPUT-SEAL.json').read_text());j['source_seal_sha256']='0'*64;replace(root,'OUTPUT-SEAL.json',(json.dumps(j)+'\n').encode());rows.append(run(root,['run.py','package'],'mismatched_output_seal'));shutil.rmtree(root)
 for flag in ['-O','-OO']:
  root=clone('optimized'+flag);rows.append(run(root,[flag,'run.py','verify'],'optimized'+flag));shutil.rmtree(root)
 ids=json.loads((H/'tests/EXPECTED-TESTS.json').read_text());names=[x.rsplit('.',1)[1] for x in ids]
 for mode in ['empty','extra','all_skipped','all_expected_failure']:
  root=clone(mode);s='import unittest\nEVIDENCE={}\nVMS=[]\nclass SceneTests(unittest.TestCase):\n'
  selected=[] if mode=='empty' else names+(['test_unregistered'] if mode=='extra' else [])
  if not selected:s+=' pass\n'
  for name in selected:
   if mode=='all_skipped':s+=' @unittest.skip("negative probe")\n'
   if mode=='all_expected_failure':s+=' @unittest.expectedFailure\n'
   s+=f' def {name}(self):\n  self.fail("negative probe")\n'
  replace(root,'tests/test_scene.py',s.encode());rows.append(run(root,['tests/run_suite.py'],'suite_'+mode));shutil.rmtree(root)
 if [r['name'] for r in rows]!=json.loads((H/'tests/EXPECTED-NEGATIVES.json').read_text()):raise RuntimeError('Negative inventory mismatch')
 (H/'evidence/negative-checks.json').write_text(json.dumps(dict(status='PASS',checks=rows,tests=len(rows),source_seal_sha256=hashlib.sha256((H/'SOURCE-SEAL.json').read_bytes()).hexdigest(),output_seal_sha256=hashlib.sha256((H/'OUTPUT-SEAL.json').read_bytes()).hexdigest(),native_acceptance=False),indent=2)+'\n');sys.path.insert(0,str(H));import run as entry;entry.seal_negative_evidence();print('negative probes passed and bound',len(rows))
except BaseException as _error:
 _REPORT.write_text(_Json.dumps(dict(status='FAILED',error=str(_error),native_acceptance=False))+'\n')
 raise
