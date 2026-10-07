"""Run the fixed-r2 complete world-frame regression unchanged against this build.
Only fixture construction chooses the freshly compiled P05 universe; no method
or expected render guard is replaced. One old-r1 oracle remains intentionally old.
"""
from host import *
import importlib.util,unittest,json
P=H.parent/'p04-native-inventory-fix-reconstruction/tests/render_regressions.py'
spec=importlib.util.spec_from_file_location('inherited_r2',P);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
base.HERE=H/'tools'
original=old.setup;VMS=[]
def setup_new(old=False):
 if old:return original(True)
 h,d,a,p,q,r=setup();h.p.update(location=3,roomSeen=3);VMS.append(h.vm);return h,d,a,p,q
old.setup=setup_new
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(old.RenderRegression))
 report=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,failures=[(str(t),s) for t,s in result.failures],errors=[(str(t),s) for t,s in result.errors],instructions=sum(v.steps for v in VMS),frames=sum(v.frames for v in VMS),native_acceptance=False)
 (H/'evidence/inherited-render-tests.json').write_text(json.dumps(report,indent=2)+'\n');raise SystemExit(not result.wasSuccessful())
