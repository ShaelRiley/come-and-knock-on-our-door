#!/usr/bin/env python3
"""Bounded reproducibility guards. Probes are confined to disposable copies."""
from pathlib import Path
import json,shutil,subprocess,sys
H=Path(__file__).resolve().parents[1]
P=H/'probes/guard copies'

def run(args,cwd,needle):
    r=subprocess.run(args,cwd=cwd,capture_output=True,text=True)
    text=r.stdout+r.stderr
    if r.returncode==0 or needle not in text:raise RuntimeError((args,r.returncode,text))
    return dict(command=args,cwd=str(cwd.relative_to(H)),returncode=r.returncode,expected=needle,output=text)

def main():
    results=[]
    for script,args in [('generate.py',[]),('build.py',[]),('run_tests.py',['domain'])]:
        # Optimization rejection must never poison the good compile receipt.
        dest=P/('optimized '+script)
        if dest.exists():shutil.rmtree(dest)
        shutil.copytree(H,dest,ignore=shutil.ignore_patterns('probes','delivery','relocated','__pycache__'))
        results.append(run([sys.executable,'-O','-B',script,*args],dest,'Optimized'))
    dest=P/'changed authority'
    if dest.exists():shutil.rmtree(dest)
    shutil.copytree(H,dest,ignore=shutil.ignore_patterns('probes','delivery','relocated','__pycache__'))
    p=dest/'reference/component/authority/full-line-catalog.json';p.write_bytes(p.read_bytes()+b'\n')
    results.append(run([sys.executable,'-B','generate.py'],dest,'Immutable input mismatch'))
    dest=P/'missing domain tests'
    if dest.exists():shutil.rmtree(dest)
    shutil.copytree(H,dest,ignore=shutil.ignore_patterns('probes','delivery','relocated','__pycache__'))
    (dest/'tests/test_domain.py').unlink()
    results.append(run([sys.executable,'-B','run_tests.py','domain'],dest,'Incomplete or unexpected discovery: 0'))
    dest=P/'changed generated source'
    if dest.exists():shutil.rmtree(dest)
    shutil.copytree(H,dest,ignore=shutil.ignore_patterns('probes','delivery','relocated','__pycache__'))
    p=dest/'src/module993.sc';p.write_bytes(p.read_bytes()+b'\n')
    results.append(run([sys.executable,'-B','build.py'],dest,'Generated binding mismatch'))
    (H/'evidence/guard-probes.json').write_text(json.dumps(dict(status='PASS',probes=results),indent=2)+'\n')
    print('PASS_GUARD_PROBES',len(results))
if __name__=='__main__':main()
