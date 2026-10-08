"""NEW bounded bank runner for the exact retained matrices, both SCI evaluators."""
from pathlib import Path
import sys,json,time,hashlib,itertools,random
H=Path(__file__).resolve().parents[1];sys.dont_write_bytecode=True
sys.path[:0]=[str(H/'tests'),str(H),str(H/'reference/component'),str(H/'reference/component/tests')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
 from verify_source import verify
 verify()
 from test_validation import snapshots,model_valid
 from test_domain import M,PEOPLE,O,P14World,encode_save,encode_world,approve14
 from paired import PairedVM,MEASUREMENTS
 kind=sys.argv[1];bank=int(sys.argv[2]);size=81 if kind=='approval' else 100
 start=bank*size;stop=start+size;t0=time.monotonic();vm=PairedVM();valid=invalid=0;vectors=[]
 if kind=='approval':
  base,_=approve14();total=6561
  if not 0<=start<total:raise ValueError('Out-of-range bank')
  for index,projection in enumerate(itertools.islice(itertools.product(range(3),repeat=8),start,stop),start):
   w=P14World.load(base.save())
   for person,state in zip(PEOPLE,projection):
    if state<2:del w.pinned[person]
    if state==0:del w.presentations['approve:'+person]
   w.validate();p=encode_world(w);vm.p.update(p);before=vm.persistent()
   if vm.call('p14Validate')!=1:raise AssertionError(('projection rejected',index,projection))
   if tuple(O[x] for i in range(9) if (x:=vm.call('p14InventoryAt',i)))!=w.inventory:raise AssertionError(('inventory',index))
   if vm.persistent()!=before:raise AssertionError(('mutating query',index))
   vectors.append([index,list(projection),sha_bytes(list(p.values()))]);valid+=1
 else:
  states=[encode_save(s) for s in snapshots()];cases={tuple(p.values()):p for p in states};rng=random.Random(140996);done,empty=states[-1],states[0]
  def add(p,changes):
   q={**p,**changes};cases[tuple(q.values())]=q
  for key in M['persisted_properties']:add(done,{key:-1});add(done,{key:0})
  for source,sid in M['sources'].items():
   name=M['serials'][M['source_start_offset']+sid];add(done,{'p14'+name+'Hi':0,'p14'+name+'Lo':0})
   for receipt in M['receipts'][source]:
    name=M['serials'][receipt['slot']];add(empty,{'p14RevisionLo':3,'p14'+name+'Lo':2})
  for _ in range(240):
   p=rng.choice(states);key=rng.choice(M['persisted_properties']);add(p,{key:rng.choice((0,1,2,32767))})
  total=len(cases)
  if total!=1485:raise AssertionError(('retained corpus count changed',total))
  if not 0<=start<total:raise ValueError('Out-of-range bank')
  for index,p in enumerate(itertools.islice(cases.values(),start,stop),start):
   expected=model_valid(p);vm.p.update(p);before=vm.persistent();actual=bool(vm.call('p14Validate'))
   if actual!=expected or vm.persistent()!=before:raise AssertionError(('vector parity',index,actual,expected))
   valid+=actual;invalid+=not actual;vectors.append([index,expected,sha_bytes(list(p.values()))])
 vmachine=vm.emitted.domain.vm
 if any(r[4] for r in vmachine.returns) or vmachine.depth or vmachine.chain or vmachine.kernel_attempts:raise AssertionError('Nonempty return/active frame/kernel')
 report=dict(status='PASS',kind=kind,bank=bank,start=start,stop=min(stop,total),total=total,count=valid+invalid,valid=valid,rejected=invalid,vectors=vectors,paired=MEASUREMENTS,elapsed_seconds=time.monotonic()-t0,source_sha256=sha(H/'src/module996.sc'),runner_sha256=sha(Path(__file__)),native_acceptance=False)
 p=H/'evidence'/f'matrix-{kind}-{bank:03}.json';p.write_text(json.dumps(report,indent=2)+'\n');print('PASS_MATRIX_BANK',kind,bank,len(vectors),MEASUREMENTS,time.monotonic()-t0,flush=True)
def sha_bytes(value):return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()
if __name__=='__main__':main()
