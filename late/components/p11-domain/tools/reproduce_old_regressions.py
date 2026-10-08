#!/usr/bin/env python3
"""Replay only the four actual historical behavior gaps in a disposable copy."""
from pathlib import Path
import json,shutil,subprocess,sys
H=Path(__file__).resolve().parents[1]
def main():
 d=H/'probes/old template replay'
 if d.exists():shutil.rmtree(d)
 shutil.copytree(H,d,ignore=shutil.ignore_patterns('probes','delivery','relocated','__pycache__'))
 shutil.copy2(d/'historical/stock-sci/p11-domain-adapter/src/methods.sc.in',d/'src/methods.sc.in')
 logs=[]
 for script in ('generate.py','build.py'):
  r=subprocess.run([sys.executable,'-B',script],cwd=d,capture_output=True,text=True)
  logs.append(r.stdout+r.stderr)
  if r.returncode:raise RuntimeError(('Old template recompile failed',script,logs[-1]))
 env=__import__('os').environ.copy();env['PYTHONPATH']='tests:.'
 cases=['external_unacknowledged_peg_history_blocks_without_credit','bunny_must_be_present_during_sincere','felix_listener_blocks_final_jackie_only_reply','context_rejects_peg_wedge_and_closed_wedge']
 args=[sys.executable,'-B','-m','unittest',*[f'test_adaptations.AdaptationTests.test_{c}' for c in cases],'-v']
 r=subprocess.run(args,cwd=d,env=env,capture_output=True,text=True);logs.append(r.stdout+r.stderr)
 (H/'evidence/old-template-replayed-final.log').write_text('\n'.join(logs))
 if r.returncode==0 or 'FAILED (failures=4)' not in logs[-1]:raise RuntimeError('Expected four exact historical regressions')
 (H/'evidence/old-template-replayed-final.json').write_text(json.dumps(dict(status='PASS_EXPECTED_FOUR_FAILURES',cases=cases,paired_source_emitted=True,native_acceptance=False),indent=2)+'\n')
 print('PASS_EXPECTED_FOUR_HISTORICAL_FAILURES')
if __name__=='__main__':main()
