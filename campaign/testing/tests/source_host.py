"""Execute new989 plus changed/new983/984 bridge methods from editable source.
All other campaign methods are the real emitted code. No gameplay transition is
copied into Python; this adapter only supplies sends, shared storage and kernels.
"""
import host
from collections import Counter
from domain_source_vm import VM as DomainSource,Array,Literal

class SourceModule(DomainSource):
 def __init__(self,game,number,classname,object_name,owned=None):
  self.game=game;self.number=number;self.object_name=object_name;self.owned=owned
  self.expressions=0;self.source_calls=Counter();self.constructing=True
  super().__init__(host.H/('src/main.sc' if number==0 else f'src/module{number}.sc'),classname=classname)
  self.constructing=False
  self.p=game.objects[object_name].p;self.arrays=game.arrays(number)
 def call(self,name,*args):
  if self.constructing and name=='p08Init':return 0
  if self.owned is not None and name not in self.owned:
   return self.game.emitted_call(self.game.objects[self.object_name],name,tuple(self.external(a) for a in args))
  self.source_calls[name]+=1
  result=super().call(name,*args)
  hook=getattr(self.game,'after_actual_call',None)
  if hook is not None:hook(self.game.objects[self.object_name],name,args,result)
  return result
 def external(self,value):
  if value is self:return self.game.objects[self.object_name]
  if isinstance(value,Literal):
   key=(self.number,value)
   if key not in self.game.source_strings:
    module=self.game.modules[self.number]
    offset=module.heap.find(value.encode('latin1')+b'\0',module.layout['strings_start'])
    assert offset>=module.layout['strings_start'],('source literal not emitted',value)
    self.game.source_strings[key]=host.base.Pointer(module.heapregion,offset)
   return self.game.source_strings[key]
  return value
 def ev(self,n,e):
  self.expressions+=1
  if type(n) is str and n not in e and n not in self.p and n in self.game.objects:return self.game.objects[n]
  if type(n) is str and n.startswith("@"):
   array=self.arrays[n[1:]];return host.base.Pointer(array.region,array.start*2)
  if isinstance(n,list) and not isinstance(n,Array) and n:
   op,*a=n;target=None
   # SCI literals are addresses, including internal self-call results. Native
   # getter pointers and source literals must compare in the same value domain.
   if op=='u>' and len(a)==2:
    return int((self.ev(a[0],e)&65535)>(self.ev(a[1],e)&65535))
   if op in ('==','!=') and len(a)==2:
    # SCI self remains the canonical heap object even when copied to a local.
    # external() maps that one adapter receiver and literal addresses only;
    # pointers, foreign objects and ordinary numbers retain exact identity/value.
    left,right=[self.external(self.ev(x,e)) for x in a]
    return int(left==right) if op=='==' else int(left!=right)
   if isinstance(op,list):target=self.ev(op,e)
   elif type(op)is str and op!='self':target=e.get(op,self.p.get(op))
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
    return self.game._kernel(self.game.kernel_ids[op],[self.external(self.ev(x,e)) for x in a])
  return super().ev(n,e)

class VM(host.VM):
 def __init__(self):
  self.sources={};self.source_strings={}
  super().__init__();self.kernel_ids={v:k for k,v in self.knames.items()}
  from source_tools import methods
  owned983={n for n in methods((host.H/'src/module983.sc').read_text()) if n.startswith('b8')}|{'bHeld','bReachable','bInventory','bAppend','bDispatch','bPresented'}
  owned984={n for n in methods((host.H/'src/module984.sc').read_text()) if n.startswith('q8')}|{'qInventory'}
  owned982={'sdOpenWindow','sdWindowValue','sdOpen','sdLoad','sdTurn','sdControlAction','sdBuildControls','sdDraw','sdClose','sdAfterRestore'}
  for number,cls,obj,owned in [(989,'P08State','p08State',None),(983,'P03State','p03State',owned983),(984,'P04State','p04State',owned984),(982,'SceneDialogue','sceneDialogue',owned982),(991,'SceneRenderer','sceneRenderer',{'h8VD','h8VR','h8VC','h8VF','h8ReaderMap','h8GB','h8VI'}),(990,'P09State','p09State',None),(992,'P10State','p10State',None),(987,'P06State','p06State',{'h6ReserveInventory','h6Control','h6OwnersValid'}),(985,'P05State','p05State',{'hStageActive'}),(988,'P07State','p07State',{'h7PhysicalValid','h7DrawBunny','h7ReturnBunny'})]:
   self.sources[obj]=SourceModule(self,number,cls,obj,owned)
  self.sources['cakood']=SourceModule(self,0,'Game','cakood',{'p03BuildTopics','uiHostWorldControls','bridgeActAtArrival','uiHostClosed','p03PreparationHint','drawWorld','dialogueCanSpeak','p04BuildJournal','uiHostChoice','h9PublishCard','p02HostInventory','campaignHeld','p02ObjectLocation','p05RestoreBegin','p05RestoreValidate','p05RestoreReject','h10UI','campaignReachable','h6PublishNative','uiInventoryAdd','uiInventoryRemove','uiInventoryCombine','uiInventoryCompact'})
  self.source=self.sources['p08State']
 def emitted_call(self,obj,name,args):return super().call(obj,name,args)
 def call(self,obj,name,args=()):
  source=self.sources.get(obj.name)
  if source is not None and (source.owned is None or name in source.owned):
   return source.external(source.call(name,*args))
  return self.emitted_call(obj,name,args)
 def restore(self,state):
  result=super().restore(state)
  for obj,source in self.sources.items():source.p=self.objects[obj].p;source.arrays=self.arrays(source.number)
  return result
