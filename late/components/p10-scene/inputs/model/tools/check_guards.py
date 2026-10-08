"""Run two deliberately invalid disposable copies; failures are required."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[2]
PROBE=ROOT/'probes/guard copies'
if PROBE.exists(): raise RuntimeError('Use a fresh guard-probe destination')
reports=[]
for name in ('missing tests', 'changed authority'):
    destination=PROBE/name
    for directory in ('component','provenance'):
        shutil.copytree(ROOT/directory,destination/directory)
    if name=='missing tests':
        (destination/'component/tests/test_p10_model.py').rename(destination/'component/tests/disabled.py.txt')
        expected='Incomplete or unexpected test discovery: 0'
    else:
        path=destination/'component/authority/full-line-catalog.json'
        path.write_bytes(path.read_bytes()+b' ')
        expected='Vendored input mismatch: component/authority/full-line-catalog.json'
    for options in (['-B'],['-O','-B']):
        result=subprocess.run([sys.executable,*options,str(destination/'component/tools/run_tests.py')],cwd=destination,
                              capture_output=True,text=True)
        if result.returncode==0 or expected not in result.stdout+result.stderr:
            raise RuntimeError('Guard did not fail closed: '+name+' '+result.stdout+result.stderr)
        reports.append(dict(probe=name,options=options,exit_code=result.returncode,expected_failure=expected))
path=ROOT/'evidence/guard-probes.json';path.write_text(json.dumps(reports,indent=2)+'\n')
print('Four normal/optimized expected-failure guards verified')
