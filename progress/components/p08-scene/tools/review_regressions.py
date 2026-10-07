"""Actual packaging regressions; optional unmodified R1 archive reproduces both old defects."""
from pathlib import Path
import sys,json,hashlib,subprocess,shutil,os,zipfile,copy,argparse
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];OUT=H/'evidence/review-regressions.json';OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text('{"status":"RUNNING","native_acceptance":false}\n')
def require(ok,why):
 if not ok:raise RuntimeError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def replace(root,name,data):
 p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.unlink(missing_ok=True);p.write_bytes(data)
def invoke(root,mode,log,expected=0,reason=None):
 result=subprocess.run([sys.executable,'-B',str(root/'run.py'),mode],cwd=root,capture_output=True,text=True);log.parent.mkdir(parents=True,exist_ok=True);log.write_text(result.stdout+result.stderr)
 require(result.returncode==expected,f'{log.stem} wrong exit code {result.returncode}: '+result.stderr)
 status=json.loads((root/'VERIFICATION.json').read_text())['status'];require(status==('FAILED' if expected else 'PASS_BOUND_COMPONENT'),'Incorrect terminal status '+log.stem)
 if reason:require(reason in result.stdout+result.stderr,'Incorrect rejection reason '+log.stem)
 return dict(command=mode,returncode=result.returncode,status=status,reason=reason)
def clone(source,dest):
 if dest.exists():shutil.rmtree(dest)
 shutil.copytree(source,dest,copy_function=os.link,ignore=shutil.ignore_patterns('delivery','portability','negative-probes','regression-probes','__pycache__','VERIFICATION.json','current-status.json'))
 return dest

def r2(D):
 sys.path.insert(0,str(H));import run as entry
 initial={name:sha(H/name) for name in entry.package_members()};rows=[]
 def clean(name):
  root=clone(H,D/name);invoke(root,'verify',D/(name+'-baseline.log'))
  result=subprocess.run([sys.executable,'-B','-c','import run; run.package_members()'],cwd=root,capture_output=True,text=True)
  require(result.returncode==0,'Clean package membership baseline rejected '+name+result.stderr)
  return root
 def negative(name,change,reason):
  root=clean(name);change(root)
  # Plant stale successful status, then demand both status files retire it.
  for p in [root/'VERIFICATION.json',root/'evidence/current-status.json']:p.parent.mkdir(parents=True,exist_ok=True);p.unlink(missing_ok=True);p.write_text('{"status":"PASS_BOUND_COMPONENT"}\n')
  result=invoke(root,'package',D/(name+'.log'),1,reason)
  require(json.loads((root/'evidence/current-status.json').read_text())['status']=='FAILED','Stale current PASS survived')
  require(json.loads((root/'delivery/PACKAGE-STATUS.json').read_text())['status']=='FAILED','Stale package PASS survived')
  require(not (root/'delivery/ARTIFACT.json').exists(),'Rejected fixture emitted package acceptance')
  rows.append(dict(name=name,clean_baseline_verified=True,rejected=True,stale_pass_cleared=True,**result));shutil.rmtree(root)
 def mutate_report(root,fn):
  j=json.loads((root/'evidence/negative-checks.json').read_text());fn(j);replace(root,'evidence/negative-checks.json',(json.dumps(j,indent=2)+'\n').encode())
 first=clean('unclassified_subtree');replace(first,'leftover-output/unreviewed-generated.bin',b'unreviewed\n')
 for mode in ['verify','package']:
  result=invoke(first,mode,D/('unclassified-subtree-'+mode+'.log'),1,'Unclassified root member')
  rows.append(dict(name='unclassified_subtree_'+mode,clean_baseline_verified=True,rejected=True,**result))
 require(not (first/'delivery/ARTIFACT.json').exists(),'Unclassified subtree was accepted');shutil.rmtree(first)
 for name,key,value,reason in [
  ('zero_returncode','returncode',0,'Negative row returncode mismatch'),('boolean_returncode','returncode',True,'Negative row returncode mismatch'),('float_returncode','returncode',1.0,'Negative row returncode mismatch'),
  ('baseline_false','clean_baseline_verified',False,'Negative row success flags mismatch'),('stale_flag_false','stale_pass_cleared',False,'Negative row success flags mismatch'),('numeric_true_flag','stale_pass_cleared',1,'Negative row success flags mismatch'),('wrong_rejection','rejection','unexpected success','Negative row rejection mismatch')]:
  negative(name,lambda root,k=key,v=value:mutate_report(root,lambda j:j['checks'][0].__setitem__(k,v)),reason)
 negative('reviewer_combined_forgery',lambda root:mutate_report(root,lambda j:j['checks'][0].update(returncode=0,clean_baseline_verified=False,stale_pass_cleared=False,rejection='unexpected success')),'Negative row returncode mismatch')
 negative('missing_row',lambda root:mutate_report(root,lambda j:j['checks'].pop()),'Negative row inventory mismatch')
 negative('duplicate_row',lambda root:mutate_report(root,lambda j:j['checks'].__setitem__(1,copy.deepcopy(j['checks'][0]))),'Negative row order/identity mismatch')
 negative('extra_row',lambda root:mutate_report(root,lambda j:j['checks'].append(copy.deepcopy(j['checks'][0]))),'Negative row inventory mismatch')
 negative('extra_row_field',lambda root:mutate_report(root,lambda j:j['checks'][0].__setitem__('unreviewed',True)),'Negative row schema mismatch')
 negative('missing_row_field',lambda root:mutate_report(root,lambda j:j['checks'][0].pop('rejection')),'Negative row schema mismatch')
 negative('boolean_test_count',lambda root:mutate_report(root,lambda j:j.__setitem__('tests',True)),'Negative gate inventory is not exact PASS')
 negative('valid_report_whitespace',lambda root:replace(root,'evidence/negative-checks.json',(root/'evidence/negative-checks.json').read_bytes()+b'\n'),'Gate evidence byte identity mismatch')
 negative('changed_approved_log',lambda root:replace(root,'evidence/tests-final.log',b'forged successful output\n'),'Gate evidence byte identity mismatch')
 negative('missing_gate_seal',lambda root:(root/'GATE-SEAL.json').unlink(),'GATE-SEAL.json')
 def extra_gate(root):
  j=json.loads((root/'GATE-SEAL.json').read_text());j['files']['evidence/nested/tests-final.log']='0'*64;replace(root,'GATE-SEAL.json',(json.dumps(j)+'\n').encode())
 negative('unapproved_gate_member',extra_gate,'Gate evidence inventory mismatch')
 positive=clean('nested_evidence_lookalike');replace(positive,'evidence/nested/tests-final.log',b'unsealed basename lookalike\n');invoke(positive,'verify',D/'nested-evidence-verify.log');result=invoke(positive,'package',D/'nested-evidence-package.log');meta=json.loads((positive/'delivery/ARTIFACT.json').read_text());package=positive/meta['path']
 expected=['p08-scene-reconstruction/'+name for name in initial]
 with zipfile.ZipFile(package) as z:
  require(z.namelist()==expected,'ZIP membership was not exactly derived from checked inventories')
  require('p08-scene-reconstruction/evidence/nested/tests-final.log' not in z.namelist(),'Nested evidence basename escaped allowlist')
  for name,digest in initial.items():require(hashlib.sha256(z.read('p08-scene-reconstruction/'+name)).hexdigest()==digest,'ZIP member identity differs')
 rows.append(dict(name='nested_evidence_not_packaged',clean_baseline_verified=True,rejected=False,unsealed_member_excluded=True,exact_members=len(expected),archive_sha256=sha(package),**result))
 shutil.rmtree(positive)
 require({name:sha(H/name) for name in initial}==initial,'Producer changed during isolated regressions')
 expected_names=json.loads((H/'tests/EXPECTED-REVIEW-REGRESSIONS.json').read_text());require([r['name'] for r in rows]==expected_names,'Regression inventory mismatch')
 return dict(status='PASS',cases=rows,tests=len(rows),source_seal_sha256=sha(H/'SOURCE-SEAL.json'),output_seal_sha256=sha(H/'OUTPUT-SEAL.json'),gate_seal_sha256=sha(H/'GATE-SEAL.json'),producer_files_unchanged=True,native_acceptance=False)
try:
 require(not sys.flags.optimize,'Optimized Python forbidden')
 D=H/'regression-probes';D.mkdir(exist_ok=True)
 result=r2(D);dump(OUT,result);print('Packaging regressions passed',result['tests'])
except BaseException as e:
 dump(OUT,dict(status='FAILED',error=str(e),native_acceptance=False));raise
