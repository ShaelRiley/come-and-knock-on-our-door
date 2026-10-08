#!/usr/bin/env python3
"""Materialize and reproduce one explicitly isolated WIP component, offline."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,shutil,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
MAP=ROOT/'late/manifests/COMPONENTS.json'
EXPECTED=ROOT/'late/manifests/EXPECTED-OUTPUTS.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def safe(name):
 p=PurePosixPath(name)
 if p.is_absolute() or p.as_posix()!=name or '..' in p.parts or '\\' in name:raise ValueError('Unsafe relative member')
 return p
def materialize(name,dest):
 files=json.loads(MAP.read_text())[name]['files']
 dest.mkdir(parents=True)
 for n,row in files.items():
  src=ROOT/safe(row['from']);target=dest/safe(n)
  if not (ROOT==src.resolve() or ROOT in src.resolve().parents) or src.is_symlink() or not src.is_file() or sha(src)!=row['sha256'] or src.stat().st_size!=row['bytes'] or src.stat().st_mode&0o777!=row['mode']:raise RuntimeError('Source identity differs: '+n)
  target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target);target.chmod(row['mode'])
 for folder in ['evidence','generated']:(dest/folder).mkdir(exist_ok=True)
 if name not in ['p08-scene','p09-scene']:(dest/'reports').mkdir(exist_ok=True)
 if name=='p09-scene':(dest/'historical').mkdir(exist_ok=True)
 if name=='courtyard-art':
  for folder in ['indexed-cels','resources','previews','previews/all-layouts']:(dest/folder).mkdir(parents=True,exist_ok=True)
 return dest
def command(work,args,log,env=None):
 environment={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONOPTIMIZE':''}
 if env:environment.update(env)
 started=time.monotonic()
 with log.open('w') as out:r=subprocess.run([sys.executable,'-B',*args],cwd=work,stdout=out,stderr=subprocess.STDOUT,env=environment)
 if r.returncode:raise RuntimeError('Command failed; see '+str(log))
 return {'command':['python3','-B',*args],'exit_code':r.returncode,'seconds':round(time.monotonic()-started,3),'log_sha256':sha(log)}
BUILD={
 'p08-evening-ack':[['generate_routes.py'],['build.py'],['evidence/emitted_ack_audit.py','.']],
 'scene991-renderer':[['derive.py'],['build.py'],['audit.py'],['tests/check_milestone.py']],
 'p09-host-foundation':[['run.py','seal'],['build.py'],['audit.py']],
 'p09-geometry-scaffold':[['run.py','seal'],['build.py'],['audit.py']],
 **{f'p{n}-domain':[['generate.py'],['build.py']] for n in range(10,15)},
 **{f'p{n}-scene':[['run.py','seal-source'],['run.py','rebuild']] for n in range(10,15)},
}
TESTS={
 'p08-evening-ack':{**{f'ack{i:02}':['tests/run_evening_boundaries.py',f'{i:02}'] for i in range(1,8)},'publisher':['evidence/run_evening_publisher_observer.py'],'prior':['evidence/run_evening_prior_selected.py'],'storage':['evidence/run_storage_after_ack.py']},
 'scene991-renderer':{'first':['tests/check_milestone.py'],'matrix':['tests/paint_matrix.py'],'supplement':['tests/branch_supplement.py'],'order':['tests/state_order.py'],'preparation':['tests/preparation_matrix.py']},
 'p09-host-foundation':{'all':['run.py','test']},
 'p09-geometry-scaffold':{'all':['run.py','test']},
 'p10-domain':{g:['run_tests.py',g] for g in ['domain','finite','transport','reference']},
 'p11-domain':{g:['run_tests.py',g] for g in ['domain','adaptations','finite','transport','finite_projection']},
 'p12-domain':{g:['run_tests.py',g] for g in ['domain','finite','transport','projection']},
 'p13-domain':{g:['run_tests.py',g] for g in ['domain','validation','finite']},
 'p14-domain':{},
 **{f'p{n}-scene':{'all':['tests/run_suite.py']} for n in range(10,15)},
}
p14_pin=json.loads(MAP.read_text())['p14-domain']['files']['tests/EXPECTED-TESTS.json']['from']
TESTS['p14-domain']={g:['run_tests.py',g] for g in json.loads((ROOT/safe(p14_pin)).read_text())}
def normalize_output(raw,work,kind):
 text=raw.decode().replace(str(work),'<COMPONENT>')
 if kind=='component-root-text':return text.encode()
 obj=json.loads(text)
 if kind=='typed-resource-order':obj=sorted(obj,key=lambda x:(x['type'],x['number']))
 return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()
def compare(name,work):
 expected=json.loads(EXPECTED.read_text()).get(name,{})
 normalized=json.loads((ROOT/'late/manifests/NORMALIZED-OUTPUTS.json').read_text()).get(name,{})
 differences=[n for n,d in expected.items() if not (work/safe(n)).is_file() or sha(work/n)!=d]
 for n,row in normalized.items():
  p=work/safe(n)
  if not p.is_file() or hashlib.sha256(normalize_output(p.read_bytes(),work,row['normalization'])).hexdigest()!=row['sha256']:differences.append(n)
 for n,mode in json.loads((ROOT/'late/manifests/OUTPUT-MODES.json').read_text()).get(name,{}).items():
  if not (work/safe(n)).is_file() or (work/n).stat().st_mode&0o777!=mode:differences.append(n+' (mode)')
 if differences:raise RuntimeError('Reproduced output mismatch: '+', '.join(differences[:20]))
 return {'expected_outputs':len(expected),'matched_outputs':len(expected),'normalized_metadata_outputs':len(normalized),'expected_manifest_sha256':sha(EXPECTED),'normalized_manifest_sha256':sha(ROOT/'late/manifests/NORMALIZED-OUTPUTS.json')}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('component',choices=BUILD);p.add_argument('--out',type=Path,required=True);p.add_argument('--phase',choices=['build','test','materialize'],default='build');p.add_argument('--suite');a=p.parse_args()
 if sys.flags.optimize:raise RuntimeError('Optimized Python is forbidden')
 out=a.out.resolve();work=out/'component'
 if ROOT==out or ROOT in out.parents:raise RuntimeError('Choose an output outside the source repository')
 component_files=json.loads(MAP.read_text())[a.component]['files']
 files_hash=hashlib.sha256(json.dumps(component_files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 report={'schema':1,'component':a.component,'phase':a.phase,'suite':a.suite,'status':'RUNNING','native_acceptance':False,'playable_release':False,'component_map_sha256':sha(MAP),'component_files_sha256':files_hash,'driver_sha256':sha(Path(__file__).resolve()),'commands':[]}
 if a.phase!='test':
  if out.exists():raise RuntimeError('Output must be new')
  out.mkdir(parents=True);materialize(a.component,work)
 else:
  prior=json.loads((out/'build-result.json').read_text())
  same=prior.get('component_files_sha256')==files_hash or ('component_files_sha256' not in prior and prior['component_map_sha256']==sha(MAP))
  if prior['component']!=a.component or prior['status']!='PASS_CLEAN_REPRODUCTION' or not same:raise RuntimeError('A matching completed build is required')
  for n,row in json.loads(MAP.read_text())[a.component]['files'].items():
   if n not in ('SOURCE-SEAL.json','OUTPUT-SEAL.json','VERIFICATION.json') and sha(work/n)!=row['sha256']:raise RuntimeError('Source changed since materialization: '+n)
 (out/'logs').mkdir(exist_ok=True)
 result=out/('test-'+str(a.suite)+'.json' if a.phase=='test' else 'build-result.json');dump(result,report)
 try:
  if a.phase=='materialize':report['status']='MATERIALIZED_NOT_BUILT';return
  if a.phase=='build':
   if a.component=='milo-approach':
    dep=materialize('p07-host',out/'p07-dependency')
    for i,args in enumerate(BUILD['p07-host']):report['commands'].append(command(dep,args,out/f'logs/dependency-{i}.log'))
    compare('p07-host',dep)
    shutil.copytree(dep/'build',work/'fixture/build',dirs_exist_ok=True)
   for i,args in enumerate(BUILD[a.component]):report['commands'].append(command(work,args,out/f'logs/build-{i}.log'))
   report.update(compare(a.component,work));report['status']='PASS_CLEAN_REPRODUCTION'
  else:
   suites=TESTS.get(a.component,{})
   if a.suite not in suites:raise RuntimeError('Choose one of: '+', '.join(suites))
   if a.component=='music-r3':
    # Its aggregate accepts an absent build and constructs test checkpoints on
    # test import. A compile-only build intentionally lacks those checkpoints.
    shutil.rmtree(work/'build')
   env={'PYTHONPATH':str(work/'reference')} if a.component=='p09-domain' and a.suite=='reference' else None
   report['commands'].append(command(work,suites[a.suite],out/f'logs/test-{a.suite}.log',env));report.update(compare(a.component,work));report['status']='PASS_BOUNDED_TEST_PHASE'
 except BaseException as e:report['status']='FAILED';report['error']=str(e);raise
 finally:dump(result,report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
