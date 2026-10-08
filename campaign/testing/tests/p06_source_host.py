"""Independent editable-source987 execution against the emitted retained host.
No new gameplay transitions are copied into Python. All987 expressions execute
from src/module987.sc; Main/982/985/986 remain real emitted code and kernel mocks.
"""
import host
from p06_domain_source_vm import VM as DomainSource,Array,Literal

class Source987(DomainSource):
 def __init__(self,game):
  self.game=game;self.expressions=0
  super().__init__(host.H/'src/module987.sc')
  self.p=game.objects['p06State'].p;self.arrays=game.arrays(987)
 def call(self,name,*args):
  result=super().call(name,*args)
  return result
 def external(self,value):
  if value is self:return self.game.objects['p06State']
  if isinstance(value,Literal):
   if value not in self.game.source_strings:
    module=self.game.modules[987]
    offset=module.heap.find(value.encode('latin1')+b'\0',module.layout['strings_start'])
    assert offset>=module.layout['strings_start'],('source literal not emitted',value)
    self.game.source_strings[value]=host.base.Pointer(module.heapregion,offset)
   return self.game.source_strings[value]
  return value
 def ev(self,n,e):
  self.expressions+=1
  if isinstance(n,list) and not isinstance(n,Array) and n:
   op,*a=n
   target=None
   if isinstance(op,list):target=self.ev(op,e)
   elif type(op)is str and op!='self':
    target=e.get(op,self.p.get(op))
   if target is not None and hasattr(target,'call'):
    i=0;result=0
    while i<len(a):
     selector=a[i];i+=1;args=[]
     while i<len(a) and not(type(a[i])is str and a[i].endswith((':','?'))):args.append(self.external(self.ev(a[i],e)));i+=1
     name=selector[:-1]
     if selector.endswith('?'):
      assert not args;result=target.p[name]
     elif name in target.p:
      assert len(args)==1;target.p[name]=args[0];result=args[0]
     else:result=target.call(name,*args)
    return result
   if type(op)is str and op in self.game.kernel_ids:
    args=[self.external(self.ev(x,e)) for x in a]
    return self.game._kernel(self.game.kernel_ids[op],args)
  return super().ev(n,e)

class VM(host.VM):
 def __init__(self):
  self.source=None;self.source_strings={}
  super().__init__();self.kernel_ids={v:k for k,v in self.knames.items()}
  self.source=Source987(self)
 def call(self,obj,name,args=()):
  if self.source is not None and obj.name=='p06State':
   value=self.source.call(name,*args)
   return self.source.external(value)
  return super().call(obj,name,args)
 def restore(self,state):
  result=super().restore(state)
  self.source.p=self.objects['p06State'].p;self.source.arrays=self.arrays(987)
  return result
