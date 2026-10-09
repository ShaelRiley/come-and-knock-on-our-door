"""Portable emitted SCI test runner. Typed kernel mocks are not native proof."""
from pathlib import Path
import sys,inspect,textwrap,re
S=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(S/'tools'),str(S/'tests/vm')]
import host_vm as base
from host_vm import HostVM,require
# Permit all compiler-emitted private procedures, with strict CFG boundaries.
code=textwrap.dedent(inspect.getsource(HostVM.execute))
code,n=re.subn(r"(?m)^( +)require\(target in m\.layout\['exports'\].*\n\1index=m\.layout\['exports'\]\.index\(target\);acc=self\.procedure\(m\.number,index,values\[1:\]\)",lambda m:m[1]+"acc=self.execute(obj,m,'private@'+str(target),target,values[1:])",code)
assert n==1
scope=dict(vars(base));exec(code,scope)
class PresentationVM(HostVM):
 execute=scope['execute']
 def __init__(self,build=None):
  B=Path(build) if build else S/'build/coherent'
  super().__init__(B/'verification-checkpoint',B,budget=8000000)
  self.h=self.objects['cakood'];self.a=self.objects['presentationAudio']
  self.h.p['presentation']=self.a
  self.h.p['dialogue']=self.modules[982].objects[self.modules[982].layout['exports'][0]]
 def method_boundaries(self,m,entry):
  if not hasattr(m,'cfg_boundaries'):m.cfg_boundaries={}
  if entry not in m.cfg_boundaries:
   todo=[entry];allowed=set()
   while todo:
    pc=todo.pop()
    if pc in allowed:continue
    require(0<=pc<m.layout['script_relocation_offset'],'Procedure address',m.number,pc)
    allowed.add(pc);op,args,end=self.decode(m,pc)
    if op==36:continue
    if op in (23,24,25):todo.append(end+args[0])
    if op!=25:todo.append(end)
   m.cfg_boundaries[entry]=allowed
  return m.cfg_boundaries[entry]
 def proc(self,module,index,*args):
  m=self.modules[module];return self.execute(self.h,m,'export'+str(index),m.layout['exports'][index],args)
 def instance(self,module):return self.modules[module].objects[self.modules[module].layout['exports'][0]]
