#!/usr/bin/env python3
"""Sole aggregate source/emitted gate; never installs, launches, or activates."""
from pathlib import Path
import sys,json,hashlib,datetime,subprocess,unittest,traceback
H=Path(__file__).resolve().parent;E=H/'evidence';E.mkdir(exist_ok=True)
def status(state,**kw):(E/'current-status.json').write_text(json.dumps(dict(status=state,native_acceptance=False,listening_accepted=False,live_activated=False,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**kw),indent=2)+'\n')
status('RUNNING',stage='bootstrap')
try:
 if sys.flags.optimize:raise RuntimeError('Optimized Python forbidden')
 import gate_support as g
 g.check_inventories(allow_absent_generated=True);g.check_build_inventory(allow_absent=True)
 locked_source=g.fingerprints(g.source_files()+['SOURCE-INVENTORY.json'])
 sys.path[:0]=[str(H),str(H/'tools')]
 for script in('generate.py','compile.py','integrate.py','tools/stack_audit.py'):
  status('RUNNING',stage=script)
  with(E/(Path(script).stem+'.log')).open('w')as out:
   p=subprocess.run([sys.executable,'-u',str(H/script)],cwd=H,stdout=out,stderr=subprocess.STDOUT)
  g.need(p.returncode==0,'Stage failed: '+script);g.unchanged(locked_source)
 g.check_inventories()
 loader=unittest.TestLoader();suite=loader.discover(str(H/'tests'),pattern='test_*.py');actual=sorted(t.id()for t in g.flatten(suite));expected=json.loads((H/'REQUIRED-TESTS.json').read_text())
 g.need(not loader.errors,'Test discovery/import errors');g.need(actual==expected and actual,'Missing/extra required test identities');g.check_loaded_classes()
 locked_outputs=g.fingerprints(g.files('generated')+g.files('build')+['evidence/allocation-scan.json','evidence/host-composition.json','evidence/layouts.json','evidence/stack-audit.json'])
 def guard():g.unchanged(locked_source);g.unchanged(locked_outputs)
 def result_factory(*args,**kwargs):
  r=g.DurableResult(*args,**kwargs);r.source_guard=guard;return r
 status('RUNNING',stage='tests',required=len(expected))
 with(E/'tests.log').open('w',buffering=1)as out:result=unittest.TextTestRunner(stream=out,verbosity=2,resultclass=result_factory).run(suite)
 outcome=g.accept(result,len(expected));guard();g.check_inventories();g.check_build_inventory();g.check_loaded_classes()
 pins={rel:g.sha(H/rel)for rel in g.proof_files()}
 (E/'verified-files.json').write_text(json.dumps(pins,indent=2)+'\n')
 status('PASS_SOURCE_EMITTED_ONLY',stage='complete',acceptance_schema=1,test_outcomes=outcome,required_tests=expected,proof_manifest_sha256=g.sha(E/'verified-files.json'),single_sound_slot=True,accents_enabled=False)
 print('PASS_SOURCE_EMITTED_ONLY',len(expected),'tests; native/listening/activation remain false',flush=True)
except BaseException as exc:
 status('FAILED',stage='aborted',error=str(exc));traceback.print_exc();sys.exit(1)
