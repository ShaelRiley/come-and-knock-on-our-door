"""New API wrapper over unchanged accepted emitted SCI1.1 evaluator.

The model is not used for execution. Call-frame stack, bounds and word behavior
remain those of tools/host_vm.py, whose accepted hash is verified.
"""
from harness import EmittedDomain, B
from source_vm import validate_call
class Compiled:
    def __init__(self,here,module,defaults):
        if module!=995:raise ValueError('P13 domain only')
        self.domain=EmittedDomain(budget=1000000000)
        self.blob=(B/'compiled/995.scr.bin').read_bytes()
        self.trace=[]
    @property
    def steps(self):return self.domain.vm.steps
    def execute(self,name,p,args=()):
        validate_call(name,args)
        self.domain.p.update(p)
        result=self.domain.call(name,*args)
        p.update(self.domain.p)
        return result
