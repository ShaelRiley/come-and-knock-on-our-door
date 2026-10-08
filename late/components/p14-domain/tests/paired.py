"""Compare every source return/property/local against actual emitted SCI."""
from source_vm import VM as SourceVM
from compiled_vm import Compiled
from codec import M,decode_words
from harness import H
MEASUREMENTS={'instances':0,'calls':0,'instructions':0}
class PairedVM:
 def __init__(self):
  self.source=SourceVM();self.emitted=Compiled(H,996,self.source.p)
  self.p=self.source.p;self.other=self.p.copy();self.calls=0
  self.arrays=self.source.arrays;MEASUREMENTS['instances']+=1
 def call(self,name,*args):
  self.other.update(self.p)
  before=self.emitted.steps
  left=self.source.call(name,*args);right=self.emitted.execute(name,self.other,args)
  self.calls+=1;MEASUREMENTS['calls']+=1;MEASUREMENTS['instructions']+=self.emitted.steps-before
  if left!=right or self.p!=self.other:raise AssertionError(('source/emitted return or properties',name,args,left,right))
  for k,v in self.source.arrays.items():
   if v!=list(self.emitted.domain.arrays[k]):raise AssertionError(('source/emitted local arrays',name,k))
  return left
 def persistent(self):return self.source.persistent()
def restore_words(words):
 decode_words(words)
 v=PairedVM();v.p.update(zip(M['persisted_properties'],words))
 if not v.call('p14AfterRestore'):raise ValueError('Invalid restored P14 branch')
 return v
