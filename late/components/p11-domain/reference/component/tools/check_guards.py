"""Expected-failure probes in disposable copies inside this component root."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
CASES={
    'missing tests': 'Incomplete or unexpected test discovery',
    'changed authority': 'Changed pinned input: component/authority/full-line-catalog.json',
    'changed dependency': 'Changed pinned input: component/dependencies/p04_numeric_model.py',
    'partial P10': 'Changed pinned input: component/cakood/p10_model.py',
    'changed fixture': 'Current fixture differs from pinned canonical inputs',
}

def check():
    results=[]
    for name,expected in CASES.items():
        target=ROOT/'probes'/name
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)
        for tree in ('component','historical','provenance'):
            shutil.copytree(ROOT/tree,target/tree,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        if name=='missing tests':
            p=target/'component/tests/test_current_contract.py';p.rename(p.with_suffix('.removed'))
        elif name=='changed authority':
            p=target/'component/authority/full-line-catalog.json';p.write_bytes(p.read_bytes()+b'\n')
        elif name=='changed dependency':
            p=target/'component/dependencies/p04_numeric_model.py';p.write_bytes(p.read_bytes()+b'\n')
        elif name=='partial P10':
            (target/'component/cakood/p10_model.py').write_bytes((target/'historical/dependencies/p10-partial-prefix.py.txt').read_bytes())
        else:
            p=target/'component/tests/fixtures/p11/canonical-bindings.json'
            data=json.loads(p.read_text());data['catalog_sha256']='invented';p.write_text(json.dumps(data))
        run=subprocess.run([sys.executable,'-O',str(target/'component/tools/run_tests.py')],
            cwd=target,env={**os.environ,'PYTHONPATH':'','PYTHONDONTWRITEBYTECODE':'1'},
            text=True,capture_output=True)
        output=run.stdout+run.stderr
        ok=run.returncode!=0 and expected in output
        results.append(dict(case=name,returncode=run.returncode,expected=expected,passed=ok))
        (ROOT/'evidence'/('guard-'+name.replace(' ','-')+'.log')).write_text(output)
        if not ok:
            raise RuntimeError('Guard probe did not reject correctly: '+name+'\n'+output)
    (ROOT/'evidence/guard-probes.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':check()
