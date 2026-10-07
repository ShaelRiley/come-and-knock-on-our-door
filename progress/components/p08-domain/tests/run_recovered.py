#!/usr/bin/env python3
"""Run 22 applicable literal tests unchanged with the requested SCI backend.
Three historical diagnostics are retained and run by reference-baseline/verify.sh.
"""
from pathlib import Path
import sys,unittest,json,hashlib,time
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tests'))
from adapter import SourceWorld,EmittedWorld,FastSourceWorld,FastEmittedWorld
from tests import test_p08_model as legacy
GAPS={'test_canonical_bindings_exact_ids_and_result_surface','test_composes_real_prior_models_without_rewriting_their_history','test_native_object_proposals_do_not_duplicate_existing_manifest_ids'}
backend=sys.argv[1];legacy.P08World={'source':FastSourceWorld,'emitted':FastEmittedWorld,'source-slow':SourceWorld,'emitted-slow':EmittedWorld}[backend]
names=unittest.defaultTestLoader.getTestCaseNames(legacy.P08Tests)
if len(names)!=25 or not GAPS<=set(names):raise RuntimeError('Literal suite membership changed')
files=['src/module989.sc','manifest.json','selectors.json','build/compiled/989.scr.bin','build/compiled/989.scr.bin.hep']
def hashes():return {r:hashlib.sha256((H/r).read_bytes()).hexdigest() for r in files}
before=hashes();start=time.monotonic()
result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(legacy.P08Tests(n) for n in names if n not in GAPS))
report={'backend':backend,'run':result.testsRun,'passed':result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),'failures':[{'test':t.id(),'trace':trace} for t,trace in result.failures],'errors':[{'test':t.id(),'trace':trace} for t,trace in result.errors],'skipped':result.skipped,'named_tests':[legacy.P08Tests(n).id() for n in names if n not in GAPS],'historical_exclusions':sorted(GAPS),'source_binary_binding':before,'binding_unchanged':before==hashes(),'seconds':time.monotonic()-start}
(H/f'reports/recovered-{backend}.json').write_text(json.dumps(report,indent=2)+'\n')
raise SystemExit(0 if result.wasSuccessful() and result.testsRun==22 and not result.skipped and report['binding_unchanged'] else 1)
