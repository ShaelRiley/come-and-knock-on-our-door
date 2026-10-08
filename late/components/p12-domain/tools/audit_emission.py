"""Whole-method disassembly and finite runtime opcode/frame evidence."""
from pathlib import Path
import sys,json,collections
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests'),str(H/'reference/component'),str(H/'reference/component/tests')]
from verify_source import verify
from test_domain import Harness,C,A
from paired import PairedVM
def main():
 if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
 source=verify();h=Harness(PairedVM);h.confetti();h.action('claim_laugh','p12ClaimLaugh');h.show('cleanup');h.action('finish_welcome','p12FinishWelcome');h.restore();h.queries()
 vm=h.v.emitted.domain.vm;m=vm.modules[994]
 supported=set(range(32))|{33,36,37,40,42,45,46,48}|set(range(49,63))|set(range(64,128))
 methods=[];opcodes=collections.Counter()
 for obj in m.layout['objects']:
  if not obj['is_class']:continue
  for method in obj['methods']:
   pcs=vm.method_boundaries(m,method['code_offset'])
   for pc in pcs:
    op,args,end=vm.decode(m,pc)
    if op not in supported:raise ValueError(('Unsupported emitted opcode',method['selector'],pc,op))
    if op in (23,24,25) and end+args[0] not in pcs:raise ValueError(('Branch leaves method',method['selector'],pc))
    opcodes[vm.opnames[op]]+=1
   methods.append(dict(name=method['selector'],instructions=len(pcs)))
 report=dict(status='PASS',source=source,methods=methods,static_instructions=sum(opcodes.values()),static_opcodes=dict(sorted(opcodes.items())),runtime=vm.report(),returns=len(vm.returns),depth_at_finish=vm.depth,chain_at_finish=vm.chain,return_stack_semantics='SCI RET discards a frame; switch deciding values may remain inside that frame, never on caller stack',native_acceptance=False)
 if vm.depth or vm.chain or vm.kernel_attempts:raise ValueError('Unexpected active frames or kernel attempts')
 (H/'evidence/emission-audit.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS_STATIC_EMISSION_AND_RUNTIME',len(methods),sum(opcodes.values()),vm.steps,len(vm.returns))
if __name__=='__main__':main()
