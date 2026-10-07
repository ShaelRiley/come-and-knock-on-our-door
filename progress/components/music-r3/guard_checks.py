#!/usr/bin/env python3
"""Bounded, durable negative probes. No background jobs or native processes."""
from pathlib import Path
import sys,json,shutil,subprocess,ast,hashlib,importlib.util,unittest,io
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import gate_support as g
P=H/'guard-work';E=H/'evidence';reports=[]
def write(): (E/'guard-probes.json').write_text(json.dumps(dict(status='RUNNING',probes=reports),indent=2)+'\n')
def clone(name):
 d=P/name
 if d.exists():shutil.rmtree(d)
 d.mkdir(parents=True)
 for rel in g.source_files()+['SOURCE-INVENTORY.json']+g.files('generated'):
  dest=d/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(H/rel,dest)
 # Receipt recheck probes require the exact build too; small, bounded compiled fixtures.
 for rel in g.files('build')+['evidence/current-status.json','evidence/verified-files.json','evidence/allocation-scan.json','evidence/host-composition.json','evidence/layouts.json','evidence/stack-audit.json','evidence/phase-sweep.json','evidence/tests.log']:
  dest=d/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(H/rel,dest)
 return d
def probe(name,edit,command='verify.py',flags=()):
 d=clone(name);edit(d);out=subprocess.run([sys.executable,*flags,str(d/command)],cwd=d,capture_output=True,text=True)
 state=json.loads((d/'evidence/current-status.json').read_text())
 g.need(out.returncode!=0 and state['status']=='FAILED','Guard failed to reject '+name)
 reports.append(dict(name=name,status='PASS_REJECTED',exit=out.returncode,error=state.get('error'),terminal=(out.stdout+out.stderr)[-800:]));write();print(name,'PASS_REJECTED',flush=True);shutil.rmtree(d)
def remove(rel):return lambda d:(d/rel).unlink()
def append(rel,text):
 def f(d):p=d/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text((p.read_text()if p.exists()else'')+text)
 return f
def main():
 g.need(not sys.flags.optimize,'optimized Python forbidden');subprocess.run([sys.executable,str(H/'verify.py')],cwd=H,check=True);P.mkdir(exist_ok=True);write()
 probe('missing-helper',remove('tools/music_vm.py'),'run.py')
 probe('missing-test-file',remove('tests/test_events.py'),'run.py')
 probe('extra-test-file',append('tests/unrequested.py','x=1\n'),'run.py')
 probe('extra-empty-class',append('tests/test_events.py','\nclass UnsealedClass: pass\n'),'run.py')
 def hidden_class(d):
  append('tools/music_vm.py','\nimport unittest\nclass HiddenExtra(unittest.TestCase): pass\n')(d)
  append('tests/test_events.py','\nfrom music_vm import HiddenExtra\n')(d)
 probe('extra-imported-class',hidden_class,'run.py')
 def during_test(d):
  p=d/'tests/test_events.py';s=p.read_text();needle=' def test_01_current_commit_only_and_all_encounters(self):';g.need(s.count(needle)==1,'Probe target changed');s=s.replace(needle,needle+'\n  p=H/"run.py";p.write_text(p.read_text()+"\\n#changed during proof\\n")');p.write_text(s)
 probe('source-changed-during-test',during_test,'run.py')
 probe('syntax-error',append('tests/test_events.py','\ninvalid (\n'),'run.py')
 probe('immutable-input',append('inputs/domain/module986.sc','\n;corrupt\n'),'run.py')
 probe('missing-generated',remove('generated/module941.sc'),'run.py')
 probe('extra-generated',append('generated/preview.txt','unsealed'),'run.py')
 probe('nested-generated',append('generated/nested/preview.svg','unsealed'),'run.py')
 probe('stale-source',append('src/broker-procedures.inc','\n;changed after proof\n'))
 probe('stale-compiled',append('build/fresh/compiled/941.scr.bin.extra','unsealed'))
 probe('missing-compiled',remove('build/fresh/compiled/941.scr.bin'))
 probe('stale-receipt',append('evidence/verified-files.json',' '))
 probe('optimized-run',lambda d:None,'run.py',('-O',))
 probe('optimized-verify',lambda d:None,'verify.py',('-O',))
 # Exercise the exact aggregate result-admission function using real tiny suites.
 cases={'skip':'@unittest.skip("probe")\n def test_case(self):pass','expected_failure':'@unittest.expectedFailure\n def test_case(self):self.fail("probe")','unexpected_success':'@unittest.expectedFailure\n def test_case(self):pass','failure':'def test_case(self):self.fail("probe")','error':'def test_case(self):raise RuntimeError("probe")'}
 for name,body in cases.items():
  namespace={'unittest':unittest};exec('class Probe(unittest.TestCase):\n '+body,namespace)
  result=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(namespace['Probe']))
  try:g.accept(result,1)
  except RuntimeError as exc:reports.append(dict(name='real-outcome-'+name,status='PASS_REJECTED',error=str(exc),outcome=g.outcomes(result)))
  else:raise RuntimeError('Outcome accepted '+name)
  write();print('real-outcome-'+name,'PASS_REJECTED',flush=True)
 result=unittest.TestResult()
 try:g.accept(result,0)
 except RuntimeError as exc:reports.append(dict(name='zero-execution',status='PASS_REJECTED',error=str(exc),outcome=g.outcomes(result)))
 else:raise RuntimeError('Zero execution accepted')
 (E/'guard-probes.json').write_text(json.dumps(dict(schema=2,status='PASS',required_manifest_sha256=g.sha(H/'REQUIRED-GUARDS.json'),validated_receipt_sha256=g.sha(E/'current-status.json'),validated_files_sha256=g.sha(E/'verified-files.json'),probes=reports,count=len(reports),scope='Fresh recursive inventory/receipt rejections and real strict-outcome admission'),indent=2)+'\n')
 g.bound_probe_report(E/'guard-probes.json',H/'REQUIRED-GUARDS.json')
 print(len(reports),'negative probes passed',flush=True)
 packaging_probes()
def packaging_probes():
 expected=json.loads((H/'REQUIRED-PACKAGING-GUARDS.json').read_text());base=json.loads((E/'guard-probes.json').read_text());rows=[]
 def mutate(name,data):
  if name=='package-empty-probes':data['probes']=[]
  elif name=='package-duplicate-probe':data['probes'][-1]=data['probes'][0].copy()
  elif name=='package-missing-probe':data['probes'].pop()
  elif name=='package-substituted-probe':data['probes'][-1]['name']='invented-case'
  elif name=='package-bad-result':data['probes'][0]['status']='PASS'
  elif name=='package-inconsistent-count':data['count']+=1
  elif name=='package-stale-receipt':data['validated_receipt_sha256']='0'*64
  else:raise RuntimeError(name)
 for name in expected:
  d=clone(name);data=json.loads(json.dumps(base));mutate(name,data)
  (d/'evidence/guard-probes.json').write_text(json.dumps(data,indent=2)+'\n')
  r=subprocess.run([sys.executable,str(d/'package.py')],cwd=d,capture_output=True,text=True)
  terminal=r.stdout+r.stderr
  wanted='Stale guard proof'if name=='package-stale-receipt'else'Guard probe'
  g.need(r.returncode!=0 and wanted in terminal,'Package did not reject exact mutation '+name)
  g.need(not list((d/'delivery').glob('*.zip')),'Rejected package created an archive')
  rows.append(dict(name=name,status='PASS_REJECTED',exit=r.returncode,error=terminal.strip().splitlines()[-1],terminal=terminal[-1200:]))
  (E/'packaging-guard-probes.json').write_text(json.dumps(dict(schema=2,status='RUNNING',probes=rows),indent=2)+'\n')
  print(name,'PASS_REJECTED',flush=True);shutil.rmtree(d)
 result=dict(schema=2,status='PASS',count=len(rows),probes=rows,required_manifest_sha256=g.sha(H/'REQUIRED-PACKAGING-GUARDS.json'),validated_receipt_sha256=g.sha(E/'current-status.json'),validated_files_sha256=g.sha(E/'verified-files.json'))
 (E/'packaging-guard-probes.json').write_text(json.dumps(result,indent=2)+'\n');g.bound_probe_report(E/'packaging-guard-probes.json',H/'REQUIRED-PACKAGING-GUARDS.json')
 print(len(rows),'packaging guard probes passed',flush=True)

if __name__=='__main__':main()
