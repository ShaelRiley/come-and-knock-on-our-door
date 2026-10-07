from pathlib import Path
import sys,unittest,json,time,hashlib
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tests'))
import test_domain as tests
kind=sys.argv[1]
classes={'domain':tests.DomainTests,'finite':tests.FiniteTests}
cls=classes[kind];names=unittest.defaultTestLoader.getTestCaseNames(cls)
expected={'domain':13,'finite':1}
if len(names)!=expected[kind]:raise RuntimeError(('Test membership changed',names))
files=['src/module989.sc','manifest.json','selectors.json','build/compiled/989.scr.bin','build/compiled/989.scr.bin.hep']
def hashes():return {r:hashlib.sha256((H/r).read_bytes()).hexdigest() for r in files}
before=hashes();start=time.monotonic();result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(cls(n) for n in names))
report={'suite':kind,'run':result.testsRun,'passed':result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),'failures':[{'test':t.id(),'trace':trace} for t,trace in result.failures],'errors':[{'test':t.id(),'trace':trace} for t,trace in result.errors],'skipped':result.skipped,'named_tests':[cls(n).id() for n in names],'metrics':tests.METRICS,'source_binary_binding':before,'binding_unchanged':before==hashes(),'seconds':time.monotonic()-start,'native_acceptance':False}
(H/f'reports/{kind}.json').write_text(json.dumps(report,indent=2)+'\n')
raise SystemExit(0 if result.wasSuccessful() and result.testsRun==len(names) and not result.skipped and report['binding_unchanged'] else 1)
