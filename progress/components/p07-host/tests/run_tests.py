#!/usr/bin/env python3
"""Exact discovery and durable per-case source/build-bound execution receipts."""
from pathlib import Path
import sys,json,unittest,hashlib,gc,time
H=Path(__file__).resolve().parents[1];OUT=H/'evidence/p07-tests.json';PART=H/'evidence/p07-case-progress.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
dump(OUT,{'status':'RUNNING','native_acceptance':False})
try:
 if sys.flags.optimize:raise RuntimeError('Optimized Python forbidden')
 import test_host as t
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(t.HostTests)
 ids=[x.id() for x in suite];expected=json.loads((H/'tests/EXPECTED-P07-TESTS.json').read_text())
 if not ids or len(set(ids))!=len(ids) or sorted(ids)!=expected:raise RuntimeError('Exact P07 test membership mismatch')
 binding={'compile_receipt':sha(H/'build/coherent/compile-receipt.json'),'test_source':sha(H/'tests/test_host.py'),'source':{p.name:sha(p) for p in (H/'src').glob('*.sc')}}
 metrics=[]
 class Result(unittest.TextTestResult):
  def startTest(self,test):
   self.started=time.monotonic();super().startTest(test);dump(PART,{'status':'RUNNING','current_case':test.id(),'binding':binding,'completed':metrics})
  def addFailure(self,test,err):
   super().addFailure(test,err);self.stream.writeln(self._exc_info_to_string(err,test))
  def addError(self,test,err):
   super().addError(test,err);self.stream.writeln(self._exc_info_to_string(err,test))
  def stopTest(self,test):
   bad=any(x.id()==test.id() for x,_ in self.errors+self.failures+self.skipped+self.expectedFailures)
   metrics.append(dict(test=test.id(),status='FAIL' if bad else 'PASS',seconds=time.monotonic()-self.started,instructions=sum(v.steps for v in t.VMS),source_expressions=sum(getattr(getattr(v,'source',None),'expressions',0) for v in t.VMS),frames=sum(v.frames for v in t.VMS)))
   dump(PART,{'status':'RUNNING','binding':binding,'completed':metrics});t.VMS.clear();gc.collect();super().stopTest(test)
 result=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
 good=result.wasSuccessful() and not(result.skipped or result.expectedFailures or result.unexpectedSuccesses) and result.testsRun==len(expected)
 if binding!={'compile_receipt':sha(H/'build/coherent/compile-receipt.json'),'test_source':sha(H/'tests/test_host.py'),'source':{p.name:sha(p) for p in (H/'src').glob('*.sc')}}:raise RuntimeError('Inputs changed during tests')
 report=dict(status='PASS' if good else 'FAIL',tests=result.testsRun,test_ids=ids,failures=[(str(x),s) for x,s in result.failures],errors=[(str(x),s) for x,s in result.errors],skipped=result.skipped,metrics=metrics,binding=binding,native_acceptance=False)
 dump(OUT,report);dump(PART,dict(status=report['status'],binding=binding,completed=metrics));raise SystemExit(not good)
except BaseException as e:
 if not isinstance(e,SystemExit):dump(OUT,dict(status='FAIL',error=str(e),native_acceptance=False))
 raise
