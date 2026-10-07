#!/usr/bin/env python3
"""Fixed current-host test inventory; no empty, optimized, skipped or stale PASS."""
from pathlib import Path
import sys,json,unittest,hashlib,gc
H=Path(__file__).resolve().parents[1];OUT=H/'evidence/suite.json';OUT.parent.mkdir(exist_ok=True);OUT.write_text('{"status":"RUNNING","native_acceptance":false}\n')
sys.dont_write_bytecode=True
try:
 if sys.flags.optimize:raise RuntimeError('Optimized Python is forbidden')
 import test_practical,test_contest,test_saved_consistency,test_presentation_controls,test_inherited_render
 classes=[test_practical.Practical,test_contest.Contest,test_saved_consistency.SavedConsistency,test_presentation_controls.PresentationControls,test_inherited_render.old.RenderRegression]
 suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in classes)
 def flatten(s):
  for t in s:
   if isinstance(t,unittest.TestSuite):yield from flatten(t)
   else:yield t
 ids=[t.id() for t in flatten(suite)];expected=json.loads((H/'tests/EXPECTED-TESTS.json').read_text())
 if not ids or len(ids)!=len(set(ids)) or sorted(ids)!=expected:raise RuntimeError('Fixed test inventory mismatch/zero discovery')
 metrics=[]
 class Result(unittest.TextTestResult):
  def stopTest(self,test):
   modules=[test_practical,test_contest,test_saved_consistency,test_presentation_controls,test_inherited_render,test_inherited_render.old]
   unique={id(vm):vm for m in modules for vm in getattr(m,'VMS',[])}
   metrics.append({'test':test.id(),'instructions':sum(vm.steps for vm in unique.values()),'frames':sum(vm.frames for vm in unique.values())})
   for m in modules:
    if hasattr(m,'VMS'):m.VMS.clear()
   super().stopTest(test);gc.collect()
 result=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
 report={'status':'PASS' if result.wasSuccessful() and not result.skipped and result.testsRun==len(expected) else 'FAIL','tests':result.testsRun,'test_ids':ids,'failures':[(str(t),s) for t,s in result.failures],'errors':[(str(t),s) for t,s in result.errors],'skipped':result.skipped,'case_metrics':metrics,'native_acceptance':False}
 OUT.write_text(json.dumps(report,indent=2)+'\n')
 raise SystemExit(report['status']!='PASS')
except BaseException as e:
 if not isinstance(e,SystemExit) or e.code:
  OUT.write_text(json.dumps({'status':'FAIL','error':str(e),'native_acceptance':False})+'\n')
 raise
