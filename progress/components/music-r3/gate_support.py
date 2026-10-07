"""Strict inventories and result admission shared by the aggregate and verifier."""
from pathlib import Path
import ast,hashlib,json,sys,unittest,inspect
H=Path(__file__).resolve().parent
IGNORED={'__pycache__'}
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files(folder):return sorted(str(p.relative_to(H))for p in(H/folder).rglob('*')if p.is_file()and (folder in ('generated','build')or not any(x in IGNORED for x in p.parts)))
def source_files():
 names=[]
 for folder in('src','tools','tests','inputs','reference','toolchain','licenses'):names+=files(folder)
 names += [p.name for p in H.iterdir()if p.is_file()and p.name not in('SOURCE-INVENTORY.json','ARCHIVE-MANIFEST.json')]
 return sorted(names)
def check_inventories(allow_absent_generated=False):
 need(not sys.flags.optimize,'Optimized Python forbidden')
 expected=json.loads((H/'SOURCE-INVENTORY.json').read_text())
 need(source_files()==expected,'Missing/extra source/input/test/helper file')
 generated=json.loads((H/'GENERATED-INVENTORY.json').read_text())
 actual=files('generated')
 need((allow_absent_generated and not actual)or actual==generated,'Missing/extra generated file, including nested preview')
 pins=json.loads((H/'INPUT-PINS.json').read_text());need(sorted(pins)==sorted(files('inputs')+files('reference')+files('toolchain')),'Missing/extra immutable input pin')
 for rel,digest in pins.items():need(sha(H/rel)==digest,'Immutable input changed: '+rel)
 classes={}
 for p in sorted((H/'tests').glob('*.py')):
  tree=ast.parse(p.read_text(),filename=str(p));classes[p.name]=sorted(n.name for n in tree.body if isinstance(n,ast.ClassDef))
 expected_classes=json.loads((H/'REQUIRED-CLASSES.json').read_text());need(classes==expected_classes['declared'],'Missing/extra test file or class')
def loaded_classes():
 result={}
 for p in sorted((H/'tests').glob('*.py')):
  module=sys.modules.get(p.stem)
  need(module is not None,'Test helper/module was not loaded: '+p.name)
  result[p.name]=sorted((name,cls.__module__+'.'+cls.__qualname__)for name,cls in vars(module).items()if inspect.isclass(cls)and issubclass(cls,unittest.TestCase))
 return {k:[list(x)for x in v]for k,v in result.items()}
def check_loaded_classes():
 need(loaded_classes()==json.loads((H/'REQUIRED-CLASSES.json').read_text())['visible_testcases'],'Missing/extra imported or dynamically created test class')
def check_build_inventory(allow_absent=False):
 actual=files('build');expected=json.loads((H/'BUILD-INVENTORY.json').read_text())
 need((allow_absent and not actual)or actual==expected,'Missing/extra recursive build/checkpoint output')
def fingerprints(paths):return {rel:sha(H/rel)for rel in paths}
def unchanged(snapshot):
 for rel,digest in snapshot.items():need((H/rel).is_file()and sha(H/rel)==digest,'File changed during proof: '+rel)
def flatten(suite):
 for item in suite:
  if isinstance(item,unittest.TestSuite):yield from flatten(item)
  else:yield item
def outcomes(result):return dict(run=result.testsRun,skipped=len(result.skipped),expected_failures=len(result.expectedFailures),unexpected_successes=len(result.unexpectedSuccesses),failures=len(result.failures),errors=len(result.errors))
def accept(result,required):
 d=outcomes(result);need(required>0 and d['run']==required,'Not every required test executed')
 for k in('skipped','expected_failures','unexpected_successes','failures','errors'):need(d[k]==0,'Unacceptable test outcome: '+k)
 need(result.wasSuccessful(),'Unsuccessful suite');return d
class DurableResult(unittest.TextTestResult):
 def startTest(self,test):super().startTest(test);self.stream.flush()
 def stopTest(self,test):
  super().stopTest(test);self.stream.flush()
  if getattr(self,'source_guard',None):self.source_guard()
 def addSkip(self,test,reason):super().addSkip(test,reason);self.stop()
 def addExpectedFailure(self,test,err):super().addExpectedFailure(test,err);self.stop()
 def addUnexpectedSuccess(self,test):super().addUnexpectedSuccess(test);self.stop()
 def addFailure(self,test,err):super().addFailure(test,err);self.stop()
 def addError(self,test,err):super().addError(test,err);self.stop()
def proof_files():
 return sorted(source_files()+['SOURCE-INVENTORY.json']+files('generated')+files('build')+['evidence/allocation-scan.json','evidence/host-composition.json','evidence/layouts.json','evidence/stack-audit.json','evidence/phase-sweep.json','evidence/tests.log'])

def validate_probe_report(report,expected,kind='primary'):
 need(report.get('schema')==2 and report.get('status')=='PASS','Guard report schema/status invalid')
 need(isinstance(expected,list)and len(expected)>0 and len(set(expected))==len(expected),'Invalid fixed guard manifest')
 rows=report.get('probes');need(isinstance(rows,list),'Guard probe list missing')
 names=[r.get('name')for r in rows if isinstance(r,dict)]
 need(len(rows)==len(expected)and len(names)==len(rows)and len(set(names))==len(names)and sorted(names)==sorted(expected),'Guard probe identities incomplete/duplicate/substituted')
 need(type(report.get('count'))is int and report['count']==len(rows),'Guard probe count inconsistent')
 outcome_names={'real-outcome-skip':'skipped','real-outcome-expected_failure':'expected_failures','real-outcome-unexpected_success':'unexpected_successes','real-outcome-failure':'failures','real-outcome-error':'errors'}
 outcome_keys={'run','skipped','expected_failures','unexpected_successes','failures','errors'}
 for row in rows:
  need(row.get('status')=='PASS_REJECTED'and isinstance(row.get('error'),str)and bool(row['error']),'Guard probe result missing/not rejected: '+str(row.get('name')))
  name=row['name']
  if kind=='primary'and(name in outcome_names or name=='zero-execution'):
   out=row.get('outcome');need(isinstance(out,dict)and set(out)==outcome_keys and all(type(v)is int for v in out.values()),'Guard outcome result incomplete: '+name)
   expected_out={k:0 for k in outcome_keys}
   if name!='zero-execution':expected_out['run']=1;expected_out[outcome_names[name]]=1
   need(out==expected_out,'Guard outcome result inconsistent: '+name)
  else:
   need(type(row.get('exit'))is int and row['exit']!=0 and isinstance(row.get('terminal'),str)and bool(row['terminal']),'Guard external result missing: '+name)
 return True

def bound_probe_report(path,manifest_path):
 report=json.loads(path.read_text());expected=json.loads(manifest_path.read_text())
 validate_probe_report(report,expected,'packaging'if manifest_path.name=='REQUIRED-PACKAGING-GUARDS.json'else'primary')
 need(report.get('required_manifest_sha256')==sha(manifest_path),'Guard manifest identity changed')
 need(report.get('validated_receipt_sha256')==sha(H/'evidence/current-status.json')and report.get('validated_files_sha256')==sha(H/'evidence/verified-files.json'),'Stale guard proof')
 return report
