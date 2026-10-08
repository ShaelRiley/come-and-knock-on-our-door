"""NEW direct emitted VM adapter exposing the real local arena to retained codec.
The literal ByteVM interface is preserved; evaluator instruction semantics remain
in the exact accepted host_vm. Paired proof uses its separate source/emitted API.
"""
from compiled_vm import Compiled
from source_vm import DEFAULTS,SIGNATURES,validate_call
from codec import M
from harness import H
class ReplayMachine(Compiled):
 @property
 def locals(self):return self.domain.vm.modules[996].local.words
 @locals.setter
 def locals(self,value):self.domain.vm.modules[996].local.words=value
class ByteVM:
 def __init__(self):
  self.machine=ReplayMachine(H,996,DEFAULTS);self.p=DEFAULTS.copy();self.call('p14Init')
 def call(self,name,*args):
  validate_call(name,args);return self.machine.execute(name,self.p,args,strict=True)
 def persistent(self):return {k:self.p[k] for k in M['persisted_properties']}
