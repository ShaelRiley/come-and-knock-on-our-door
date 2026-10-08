"""Run each retained matrix in a fresh bounded process, retaining every bank."""
from pathlib import Path
import sys,subprocess,concurrent.futures,json,hashlib,time
H=Path(__file__).resolve().parents[1]
def run(row):
 kind,bank=row;p=H/'evidence'/f'matrix-{kind}-{bank:03}.json';runner=H/'tools/run_matrix_bank.py'
 if p.exists():
  r=json.loads(p.read_text())
  if r['status']=='PASS' and r['runner_sha256']==hashlib.sha256(runner.read_bytes()).hexdigest():return (kind,bank,'retained')
 result=subprocess.run([sys.executable,'-B',str(runner),kind,str(bank)],capture_output=True,text=True)
 log=H/'evidence'/f'matrix-{kind}-{bank:03}.log';log.write_text(result.stdout+result.stderr)
 if result.returncode:raise RuntimeError((kind,bank,result.returncode,result.stdout+result.stderr))
 return (kind,bank,'PASS')
if __name__=='__main__':
 jobs=[(kind,bank) for kind,count in [('approval',81),('vectors',15)] for bank in range(count)]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  for row in pool.map(run,jobs):print(*row,flush=True)
 rows=[json.loads((H/'evidence'/f'matrix-{kind}-{bank:03}.json').read_text()) for kind,bank in jobs]
 for kind,total in [('approval',6561),('vectors',1485)]:
  selected=[r for r in rows if r['kind']==kind]
  if [x[0] for r in selected for x in r['vectors']]!=list(range(total)):raise RuntimeError('Missing or duplicate matrix indices')
 summary=dict(status='PASS',banks=len(rows),rows={k:dict(count=sum(r['count'] for r in rows if r['kind']==k),valid=sum(r['valid'] for r in rows if r['kind']==k),rejected=sum(r['rejected'] for r in rows if r['kind']==k),instructions=sum(r['paired']['instructions'] for r in rows if r['kind']==k)) for k in ('approval','vectors')},native_acceptance=False)
 (H/'evidence/matrix-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary,flush=True)
