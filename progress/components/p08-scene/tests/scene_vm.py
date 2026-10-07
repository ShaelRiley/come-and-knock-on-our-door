"""Adapted recovered actual-source VM. Only import path changed and unused setup removed.
Mock kernels: never native/audio proof.
"""
from pathlib import Path
import importlib.util,struct
H=Path(__file__).resolve().parents[1];S=H/'tests'
spec=importlib.util.spec_from_file_location('scene_base_vm',S/'scene_base_vm.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
class VM(base.VM):
 def __init__(self,path,classname,resources=None):
  ast=base.parse(Path(path).read_text());cl=next(n for n in ast if n[:2]==['class',classname]);props=next(n[1:] for n in cl[2:] if n[0]=='properties')
  self.p=dict(zip(props[::2],props[1::2]));self.methods={n[1][0]:n for n in cl[2:] if n[0]=='method'}
  self.constants={n[1]:n[2] for n in ast if n[0]=='define'};self.arrays={};self.capacities={};self.calls=[];self.paint=[];self.stub_callbacks=False
  self.resources=resources or {};self.kernel=[];self.audio_position=-1;self.objects={};self.time=10
  for local in [n[1:] for n in ast if n[0]=='local']:
   i=0
   while i<len(local):
    a=local[i];assert isinstance(a,base.Array),(path,a)
    self.arrays[a[0]]=[0]*a[1];self.capacities[a[0]]=a[1]*2;i+=1
    if i<len(local) and local[i]=='=':
     initial=list(local[i+1]);assert len(initial)==a[1];self.arrays[a[0]][:]=initial;i+=2
 def call(self,name,*args):
  old=base.METHODS;base.METHODS=self.methods
  try:
   result=super().call(name,*args);return ((result+32768)%65536)-32768 if type(result) is int else result
  finally:base.METHODS=old
 def ev(self,n,e):
  if type(n) is str:
   if n in self.constants:return self.constants[n]
   if n in self.objects:return self.objects[n]
  if isinstance(n,list) and not isinstance(n,base.Array) and n:
   op=n[0]
   if isinstance(op,list):
    target=self.ev(op,e);selector=n[1];assert isinstance(target,VM) and selector.endswith(':');return target.call(selector[:-1],*[self.ev(x,e) for x in n[2:]])
   if op!='self' and type(op) is str and (op in e or op in self.p or op in self.objects):
    target=e.get(op,self.p.get(op,self.objects.get(op)))
    if isinstance(target,VM):
     selector=n[1]
     if selector.endswith('?'):return target.p[selector[:-1]]
     assert selector.endswith(':'),n
     member=selector[:-1];args=[self.ev(x,e) for x in n[2:]]
     if member in target.methods:return target.call(member,*args)
     assert member in target.p and len(args)==1,(member,args);target.p[member]=args[0];return args[0]
   if op=='GetFarText':
    resource,index,dest=[self.ev(x,e) for x in n[1:]]
    if dest.name=='hStaticBuffer':
     raw=self.resources[resource][index]+b'\0';assert len(raw)<=128;dest.write(list(struct.unpack('<64h',raw.ljust(128,b'\0'))))
    else:self.write(dest,self.resources[resource][index].decode('ascii'))
    return dest
   if op=='>>':return (self.ev(n[1],e)&65535)>>self.ev(n[2],e)
   if op=='GetTime':return self.time
   if op=='ScriptID':return self.objects['script'+str(self.ev(n[1],e))]
   if op=='DoAudio':
    args=[self.ev(x,e) for x in n[1:]];self.kernel.append(('DoAudio',args))
    if args[0]==2:self.audio_position=0
    if args[0]==3:self.audio_position=-1
    return self.audio_position if args[0]==6 else 0
   if op=='DoSync':
    args=[self.ev(x,e) for x in n[1:]];self.kernel.append(('DoSync',args))
    if args[0] in (0,1):self.p['syncTime']=-1;self.p['syncCue']=0
    return 0
   if op in ('DoSound','DrawCel','IsObject'):self.kernel.append((op,n[1:]));return 1
   if op=='FileIO':return -1 if self.ev(n[1],e)==0 else 0
  return super().ev(n,e)
