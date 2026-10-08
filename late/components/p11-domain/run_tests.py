#!/usr/bin/env python3
"""Exact discovery gates over actual source/emitted SCI; no optimized asserts."""
from pathlib import Path
import hashlib,io,json,sys,time,unittest,subprocess
H=Path(__file__).resolve().parent
COUNTS={'domain':38,'adaptations':9,'finite':5,'transport':2,'finite_projection':1}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
 group=sys.argv[1] if len(sys.argv)>1 else 'domain'
 if group not in COUNTS:raise ValueError('Unknown test group')
 from verify_source import verify
 verify();sys.path[:0]=[str(H/'tests'),str(H),str(H/'reference/component')]
 suite=unittest.defaultTestLoader.discover(str(H/'tests'),pattern='test_'+group+'.py');count=suite.countTestCases()
 if count!=COUNTS[group]:raise RuntimeError('Incomplete or unexpected discovery: '+str(count))
 def names(s):return [n for t in s for n in (names(t) if isinstance(t,unittest.TestSuite) else [t.id()])]
 ids=names(suite);start=time.monotonic();output=io.StringIO();result=unittest.TextTestRunner(stream=output,verbosity=2).run(suite)
 text=output.getvalue();print(text,end='')
 record=dict(status='PASS' if result.wasSuccessful() else 'FAILED',group=group,tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),test_ids=ids,elapsed_seconds=time.monotonic()-start,native_acceptance=False,host_integration=False,measurements=getattr(sys.modules.get('test_'+group),'MEASUREMENTS',[]),compile_receipt=json.loads((H/'build/isolated/compile-receipt.json').read_text()),source_sha256=sha(H/'src/module993.sc'),manifest_sha256=sha(H/'manifest.json'),runner_sha256=sha(Path(__file__)),test_sha256={str(p.relative_to(H)):sha(p) for p in (H/'tests').glob('*.py')})
 (H/'evidence'/('verified-'+group+'.json')).write_text(json.dumps(record,indent=2)+'\n');(H/'evidence'/('verified-'+group+'.log')).write_text(text)
 if not result.wasSuccessful():raise SystemExit(1)
if __name__=='__main__':main()
