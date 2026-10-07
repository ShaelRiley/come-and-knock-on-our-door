"""Run the fixed R2 order suite, optionally against preserved R1 as a control."""
from pathlib import Path
import hashlib,json,os,sys,time,unittest
H=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(H/'tests'))
subject=Path(os.environ.get('CAKOOD_P08_SUBJECT',H)).resolve()
if subject!=H:sys.path.insert(0,str(subject/'tests'))
import test_order as tests
names=unittest.defaultTestLoader.getTestCaseNames(tests.OrderTests)
if len(names)!=6:raise RuntimeError('Order regression membership changed')
files=['src/module989.sc','manifest.json','selectors.json','build/compiled/989.scr.bin','build/compiled/989.scr.bin.hep']
def hashes():return {r:hashlib.sha256((subject/r).read_bytes()).hexdigest() for r in files}
before=hashes();start=time.monotonic();result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(tests.OrderTests(n) for n in names))
report={'suite':'order','subject':'R2' if subject==H else 'preserved R1 negative control','run':result.testsRun,'passed':result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),'failures':[{'test':t.id(),'trace':trace} for t,trace in result.failures],'errors':[{'test':t.id(),'trace':trace} for t,trace in result.errors],'skipped':result.skipped,'named_tests':[tests.OrderTests(n).id() for n in names],'metrics':tests.METRICS,'source_binary_binding':before,'binding_unchanged':before==hashes(),'seconds':time.monotonic()-start,'native_acceptance':False}
name='order' if subject==H else 'r1-order-negative-control'
(H/f'reports/{name}.json').write_text(json.dumps(report,indent=2)+'\n')
raise SystemExit(0 if result.wasSuccessful() and result.testsRun==6 and not result.skipped and report['binding_unchanged'] else 1)
