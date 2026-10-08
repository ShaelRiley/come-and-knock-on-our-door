#!/usr/bin/env python3
"""Run the two room/actor/legacy-return repair methods on a pinned fresh build."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys, time, unittest
sys.dont_write_bytecode = True
T = Path(__file__).resolve().parent
C = T.parent
TESTS = ['test_room_render_fix.RoomRenderFix']
def require(ok, message):
    if not ok: raise RuntimeError(message)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def identity(work):
    return {str(p.relative_to(work)): sha(p)
            for directory in ('src','tests','tools','build/coherent/compiled')
            for p in sorted((work/directory).rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts}
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True,help='New directory outside campaign/')
    args=parser.parse_args()
    require(not sys.flags.optimize,'Optimized Python is forbidden')
    require(not any(os.environ.get(n) for n in ('P09_DIAGNOSTIC_CACHE','P10_DEV_REUSE','CAKOOD_SELECTOR_LIST')), 'Optional diagnostic/selector overrides forbidden')
    files=json.loads((T/'HARNESS-MANIFEST.json').read_text())['files']
    actual={str(p.relative_to(T)): {'sha256':sha(p),'bytes':p.stat().st_size}
            for folder in ('tests','tools') for p in (T/folder).rglob('*') if p.is_file()}
    require(actual==files,'Harness input membership or bytes changed')
    work=args.work.resolve()
    require(not work.exists() and not work.is_relative_to(C),'A new external work directory is required')
    subprocess.run([sys.executable,'-B',str(C/'reproduce.py'),'--out',str(work)],check=True)
    for folder in ('tests','tools'):
        for p in (T/folder).rglob('*'):
            if not p.is_file(): continue
            target=work/folder/p.relative_to(T/folder)
            require(not target.exists() or target.read_bytes()==p.read_bytes(),'Harness would replace build tooling: '+str(target))
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    (work/'evidence').mkdir(exist_ok=True)
    sys.path[:0]=[str(work/'tests'),str(work/'tools'),str(work)]
    os.chdir(work)
    suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(n) for n in TESTS)
    require(suite.countTestCases()==2,'Expected exactly two repair methods')
    before=identity(work);started=time.monotonic()
    report={'status':'RUNNING','expected_methods':2,'cases':[], 'native_acceptance':False,
            'native_launch_performed':False,'native_save_files_tested':False,
            'optional_diagnostic_snapshot_reuse':False,
            'inherited_authenticated_prerequisite_cache_allowed':True,
            'start_contains_no_cached_states':not any((work/'evidence').iterdir()),
            'binding':before}
    output=work/'evidence/PUBLIC-REPAIR-RESULT.json'
    def write(): output.write_text(json.dumps(report,indent=2)+'\n')
    class Result(unittest.TextTestResult):
        def startTest(self,t):
            self.started=time.monotonic();report['active']=t.id();write();super().startTest(t)
        def addSuccess(self,t):
            super().addSuccess(t);require(identity(work)==before,'Bound input changed during tests')
            report['cases'].append({'case':t.id(),'status':'PASS','seconds':round(time.monotonic()-self.started,3)});write()
        def addFailure(self,t,e): super().addFailure(t,e);self.record(t,e)
        def addError(self,t,e): super().addError(t,e);self.record(t,e)
        def record(self,t,e):
            report['cases'].append({'case':t.id(),'status':'FAIL','error':self._exc_info_to_string(e,t)});write()
        def addSubTest(self,t,s,e):
            super().addSubTest(t,s,e)
            if e is not None:self.record(s,e)
    write()
    result=unittest.TextTestRunner(verbosity=2,resultclass=Result,failfast=True).run(suite)
    pins=json.loads((C/'OUTPUT-PINS.json').read_text())
    unchanged=identity(work)==before
    exact=all(sha(work/'build/coherent'/p)==h for p,h in pins['outputs'].items())
    report.update(status='PASS' if result.wasSuccessful() and len(report['cases'])==2 and unchanged and exact else 'FAIL',
                  methods_run=result.testsRun,seconds=round(time.monotonic()-started,3),
                  inputs_unchanged=unchanged,exact_outputs_unchanged=exact,
                  compile_sha256=sha(work/'build/coherent/compile-receipt.json'))
    report.pop('active',None);write()
    print(report['status'],result.testsRun,'paired methods; native acceptance not asserted',flush=True)
    return 0 if report['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
