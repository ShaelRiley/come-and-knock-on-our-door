#!/usr/bin/env python3
"""Genuine P01-P07 progression / P08 admission in original/new source/emitted paint."""
from pathlib import Path
import sys,json,time,hashlib
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests')]
import host,campaign_route
from paint_source import VM as PaintVM
from check_milestone import state,trace
from derive import dump,sha,MOVED
from paint_matrix import Recorder

class Emitted(host.VM):
 def __init__(self):super().__init__();self.trace=Recorder(self)
class Source(PaintVM):
 def __init__(self):super().__init__();self.trace=Recorder(self)

def run():
 expected={};proof=[];coverage=[]
 for index,(root,VM) in enumerate([(H/'frozen/p09',Emitted),(H,Emitted),(H/'frozen/p09',Source),(H,Source)]):
  host.H=root;campaign_route.EMITTED=VM
  def stage(h,label):
   logical=state(h);kernels=trace(h.vm)
   evidence={'state':logical,'trace':kernels}
   target=H/'evidence/preparation'/f"variant{index}-{label.replace(' ','-')}.json";dump(target,evidence)
   digest=hashlib.sha256(json.dumps(evidence,sort_keys=True,separators=(',',':')).encode()).hexdigest()
   if index==0:expected[label]=digest
   assert expected[label]==digest,(index,label,'state/kernel mismatch',target)
   proof.append({'variant':index,'phase':label,'room':h.p['location'],'steps':h.vm.steps,'kernel_calls':len(kernels),'evidence_sha256':sha(target),'semantic_sha256':digest})
   dump(H/'evidence/preparation-progress.json',{'status':'RUNNING','phases':proof,'native_acceptance':False})
   h.vm.ktrace.clear();print('PASS_PREPARATION_PHASE',index,label,flush=True)
  campaign_route.stage=stage
  h,*owners=campaign_route.prepared(False)
  for n in ('renderCaption','drawWorld','render'):h.call(n)
  stage(h,'prepared-draw-repeat')
  from test_transactions import layout
  layout(owners[-1]);assert owners[-1].call('h8OwnersValid')==1
  h.call('drawKitchen');h.call('h6BaseDrawWorld');stage(h,'genuine-layout-owner-paints')
  h.call('bridgeFlush');host.close(h)
  h.call('h6BaseDrawWorld');stage(h,'layout-reader-drained-world')
  h.call('uiHostMenu');h.call('render');stage(h,'prepared-menu')
  vm=h.vm;r=vm.trace
  coverage.append({'variant':index,'instructions':[list(x) for x in sorted(r.instructions)],'branches':[list(x) for x in sorted(r.branches)],'source_instruction_count':len(getattr(vm,'source_instructions',set())),'source_branch_outcomes':len(getattr(vm,'source_branches',set()))})
  dump(H/'evidence/preparation-coverage.json',coverage)
 dump(H/'evidence/preparation-progress.json',{'status':'PASS_FOUR_WAY_ACTUAL_PREPARATION','phases':proof,'native_acceptance':False})
 print('PASS_PREPARATION_MATRIX',len(proof),flush=True)
if __name__=='__main__':run()
