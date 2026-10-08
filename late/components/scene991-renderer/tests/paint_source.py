"""Independent narrow source-assembly executor for the moved paint method closure.

Control flow is read from editable source labels, not disassembled code. Existing
campaign owners retain real emitted behavior. No branch results are scripted.
"""
import sys
sys.dont_write_bytecode=True
import host
from source_host import SourceModule
from domain_source_vm import Returned,Literal,word
from derive import MOVED

class PaintSource(SourceModule):
 def call(self,name,*args):
  if self.constructing and name=='p08Init':return 0
  method=self.methods[name];sig=method[1][1:];split=sig.index('&tmp') if '&tmp' in sig else len(sig)
  assert len(args)==split,(name,args,sig)
  env=dict(zip(sig[:split],args));temps=sig[split+1:]
  for n in temps:env[n]=0
  env['__temps']=temps;env['__params']=[len(args),*args];env['__method']=name;env['__acc']=0
  self.game.source_calls.add((self.number,name))
  try:
   result=0
   for n in method[2:]:result=self.ev(n,env);env['__acc']=result
   return result
  except Returned as r:return r.value
 def ev(self,n,e):
  if isinstance(n,list) and n and n[0]=='asm':return self.assembly(n[1:],e)
  if isinstance(n,list) and n and n[0]=='if':
   # Branch decisions are recorded using the actual source expression result.
   a=n[1:];cond=self.ev(a[0],e);self.game.source_branches.add((self.number,e['__method'],repr(a[0]),bool(cond)))
   cut=a.index('else') if 'else' in a else len(a);branch=a[1:cut] if cond else a[cut+1:]
   # SCI leaves a false condition in acc when a branch is not taken.
   result=cond
   for x in branch:result=self.ev(x,e)
   return result
  return super().ev(n,e)
 def assembly(self,raw,e):
  arities={'pushi':1,'ldi':1,'lap':1,'lsp':1,'lat':1,'lst':1,'sat':1,'pToa':1,'pTos':1,'lofss':1,'lofsa':1,'bnt':1,'bt':1,'jmp':1,'self':1,'send':1,'callk':2}
  code=[];labels={};i=0
  while i<len(raw):
   op=raw[i];i+=1
   if type(op)is str and op.endswith(':'):labels[op[:-1]]=len(code);continue
   count=arities.get(op,0);code.append((op,raw[i:i+count]));i+=count
  acc=self.external(e['__acc']);stack=[];pc=0;obj=self.game.objects[self.object_name];temps=e['__temps'];count=0
  def packet(n,argc=False):
   size=n//2+int(argc);assert n%2==0 and 0<size<=len(stack),(n,stack)
   v=stack[-size:];del stack[-size:]
   if argc:assert v[0]==len(v)-1
   return v
  while pc<len(code):
   count+=1;assert count<10000
   op,args=code[pc];self.game.source_instructions.add((self.number,e['__method'],pc));pc+=1
   if op=='ldi':acc=word(args[0])
   elif op=='pushi':stack.append(word(args[0]))
   elif op in ('push0','push1','push2'):stack.append(int(op[-1]))
   elif op=='push':stack.append(acc)
   elif op=='toss':stack.pop()
   elif op=='dup':stack.append(stack[-1])
   elif op=='pToa':acc=obj.p[args[0]]
   elif op=='pTos':stack.append(obj.p[args[0]])
   elif op=='lap':acc=e['__params'][args[0]]
   elif op=='lsp':stack.append(e['__params'][args[0]])
   elif op=='lat':acc=e[temps[args[0]]]
   elif op=='lst':stack.append(e[temps[args[0]]])
   elif op=='sat':e[temps[args[0]]]=acc
   elif op in ('lofss','lofsa'):
    v=self.external(args[0]);assert isinstance(v,host.base.Pointer)
    if op=='lofss':stack.append(v)
    else:acc=v
   elif op in ('bnt','bt','jmp'):
    taken=op=='jmp' or (bool(acc) if op=='bt' else not acc)
    if op!='jmp':self.game.source_branches.add((self.number,e['__method'],pc-1,bool(taken)))
    if taken:pc=labels[args[0]]
   elif op=='not':acc=int(not acc)
   elif op in ('add','sub','mul','div','mod','and','or','eq?','ne?','lt?','le?','gt?','ge?'):
    lhs=stack.pop();rhs=acc
    operations={'add':lambda:word(lhs+rhs),'sub':lambda:word(lhs-rhs),'mul':lambda:word(lhs*rhs),'div':lambda:word(int(lhs/rhs)),'mod':lambda:word(lhs-int(lhs/rhs)*rhs),'and':lambda:word(lhs&rhs),'or':lambda:word(lhs|rhs),'eq?':lambda:int(lhs==rhs),'ne?':lambda:int(lhs!=rhs),'lt?':lambda:int(lhs<rhs),'le?':lambda:int(lhs<=rhs),'gt?':lambda:int(lhs>rhs),'ge?':lambda:int(lhs>=rhs)}
    acc=operations[op]()
   elif op in ('self','send'):acc=self.game.send(obj if op=='self' else acc,packet(args[0]))
   elif op=='callk':
    values=packet(args[1],True);kernel=args[0].rstrip(',');self.game._kernel_accumulator=acc;acc=self.game.kernel(self.game.kernel_ids[kernel],values[1:])
   elif op=='ret':
    self.game.source_returns.append((self.number,e['__method'],tuple(stack)));raise Returned(acc)
   else:raise AssertionError(('unsupported source paint opcode',op,args))
  raise AssertionError(('source asm fell through',e['__method']))

class VM(host.VM):
 def __init__(self,source=True):
  self.paint_sources={};self.source_strings={};self.source_calls=set();self.source_branches=set();self.source_instructions=set();self.source_returns=[]
  super().__init__();self.kernel_ids={v:k for k,v in self.knames.items()}
  if source:
   self.paint_sources['cakood']=PaintSource(self,0,'Game','cakood',set(MOVED))
   if 991 in self.modules:self.paint_sources['sceneRenderer']=PaintSource(self,991,'SceneRenderer','sceneRenderer',set(MOVED))
 def call(self,obj,name,args=()):
  s=self.paint_sources.get(obj.name)
  if s is not None and name in s.owned:return s.external(s.call(name,*args))
  return super().call(obj,name,args)
 def restore(self,state):
  result=super().restore(state)
  for name,source in self.paint_sources.items():source.p=self.objects[name].p;source.arrays=self.arrays(source.number)
  return result
