#!/usr/bin/env python3
"""Run the exact inherited suites with per-case durable whole-build bindings."""
from pathlib import Path
import sys,json,unittest,hashlib,gc,time
H=Path(__file__).resolve().parents[1]
kind=sys.argv[1] if len(sys.argv)>1 else 'p05'
if kind not in ['p05','p06','caption']:raise SystemExit('Use p05, p06 or caption')
OUT=H/f'evidence/{kind}-inherited-tests.json';PART=H/f'evidence/{kind}-inherited-progress.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
dump(OUT,{'status':'RUNNING','native_acceptance':False})
try:
 if sys.flags.optimize:raise RuntimeError('Optimized Python forbidden')
 modules=[]
 if kind=='p05':
  import test_practical,test_contest,test_saved_consistency,test_presentation_controls,test_inherited_render
  modules=[test_practical,test_contest,test_saved_consistency,test_presentation_controls,test_inherited_render,test_inherited_render.old]
  classes=[test_practical.Practical,test_contest.Contest,test_saved_consistency.SavedConsistency,test_presentation_controls.PresentationControls,test_inherited_render.old.RenderRegression];expected='EXPECTED-TESTS.json'
 elif kind=='p06':
  import test_p06_host,p06_support
  modules=[test_p06_host,p06_support];classes=[test_p06_host.P06Host];expected='EXPECTED-P06-TESTS.json'
 else:
  import test_return_caption
  modules=[test_return_caption];classes=[test_return_caption.ReturnCaption];expected='EXPECTED-RETURN-TESTS.json'
 suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in classes)
 def flatten(s):
  for t in s:
   if isinstance(t,unittest.TestSuite):yield from flatten(t)
   else:yield t
 ids=[x.id() for x in flatten(suite)];expected=json.loads((H/'tests'/expected).read_text())
 if not ids or len(set(ids))!=len(ids) or sorted(ids)!=expected:raise RuntimeError('Exact inherited test membership mismatch')
 def binding():return {'compile_receipt':sha(H/'build/coherent/compile-receipt.json'),'tests':{str(p.relative_to(H)):sha(p) for p in (H/'tests').glob('*.py')},'source':{p.name:sha(p) for p in (H/'src').glob('*.sc')}}
 bound=binding();metrics=[]
 class Result(unittest.TextTestResult):
  def startTest(self,test):
   self.started=time.monotonic();super().startTest(test);dump(PART,{'status':'RUNNING','current_case':test.id(),'binding':bound,'completed':metrics})
  def addFailure(self,test,err):
   super().addFailure(test,err);self.stream.writeln(self._exc_info_to_string(err,test))
  def addError(self,test,err):
   super().addError(test,err);self.stream.writeln(self._exc_info_to_string(err,test))
  def stopTest(self,test):
   vs={id(v):v for m in modules for v in getattr(m,'VMS',[])}
   bad=any(x.id()==test.id() for x,_ in self.errors+self.failures+self.skipped+self.expectedFailures)
   metrics.append(dict(test=test.id(),status='FAIL' if bad else 'PASS',seconds=time.monotonic()-self.started,instructions=sum(v.steps for v in vs.values()),source_expressions=sum(getattr(getattr(v,'source',None),'expressions',0) for v in vs.values()),frames=sum(v.frames for v in vs.values())))
   dump(PART,{'status':'RUNNING','binding':bound,'completed':metrics})
   for m in modules:
    if hasattr(m,'VMS'):m.VMS.clear()
   gc.collect();super().stopTest(test)
 result=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
 good=result.wasSuccessful() and not(result.skipped or result.expectedFailures or result.unexpectedSuccesses) and result.testsRun==len(expected)
 if bound!=binding():raise RuntimeError('Sources/build/test harness changed during inherited run')
 report=dict(status='PASS' if good else 'FAIL',tests=result.testsRun,test_ids=ids,failures=[(str(x),s) for x,s in result.failures],errors=[(str(x),s) for x,s in result.errors],skipped=result.skipped,metrics=metrics,binding=bound,native_acceptance=False)
 dump(OUT,report);dump(PART,dict(status=report['status'],binding=bound,completed=metrics));raise SystemExit(not good)
except BaseException as e:
 if not isinstance(e,SystemExit):dump(OUT,dict(status='FAIL',error=str(e),native_acceptance=False))
 raise
