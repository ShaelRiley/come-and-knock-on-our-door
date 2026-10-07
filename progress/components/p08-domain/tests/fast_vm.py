"""Execution accelerators for exhaustive tests. No domain transition shortcuts.
Source functions are translated from parsed editable SCI forms. Emitted functions
are separately translated from actual SCI1.1 opcodes and relative branch targets.
The slow interpreters remain separate cross-checks. Unknown opcodes fail closed.
"""
from source_vm import VM,Array,Literal,word
import hashlib
_SOURCE_CACHE={}
_EMITTED_CACHE={}
from bytecode_vm import BytecodeVM,signed,decode

def require(ok,msg='VM bound failed'):
 if not ok:raise RuntimeError(msg)
def at(a,i):require(type(i) is int and 0<=i<len(a),('index',i,len(a)));return a[i]
def put(a,i,v):require(type(i) is int and 0<=i<len(a),('index',i,len(a)));a[i]=v;return v

def source_function(vm,method):
 sig=method[1][1:];split=sig.index('&tmp') if '&tmp' in sig else len(sig);params=sig[:split];temps=sig[split+1:];local=set(params+temps)
 def expr(n):
  if isinstance(n,(int,Literal)):return repr(n)
  if isinstance(n,Array):return 'at('+('t['+repr(n[0])+']' if n[0] in local else 'self.arrays['+repr(n[0])+']')+','+expr(n[1])+')'
  if isinstance(n,str):
   if n in local:return 't['+repr(n)+']'
   if n in vm.p:return 'self.p['+repr(n)+']'
   if n in vm.constants:return repr(vm.constants[n])
   raise RuntimeError(('value',n))
  op,*a=n
  if op=='self':
   require(type(a[0]) is str and a[0].endswith(':') and not any(type(v)is str and v.endswith(':') for v in a[1:]),'one selector per expression')
   return 'self.call('+repr(a[0][:-1])+''.join(','+expr(v) for v in a[1:])+')'
  if op=='not':return 'int(not '+expr(a[0])+')'
  if op in ('and','or'):return '('+(' '+op+' ').join(expr(x) for x in a)+')'
  symbol={'==':'==','!=':'!=','<':'<','>':'>','<=':'<=','>=':'>=','+':'+','-':'-','*':'*','&':'&','|':'|'}.get(op)
  if symbol:return ('int' if op in ('==','!=','<','>','<=','>=') else 'word')+'('+(' '+symbol+' ').join(expr(x) for x in a)+')'
  if op=='mod':return 'word('+expr(a[0])+'-int('+expr(a[0])+'/'+expr(a[1])+')*'+expr(a[1])+')'
  raise RuntimeError(('expression',n))
 lines=['def run(self,*args):',f' require(len(args)=={len(params)},"source arity")',' t=dict(zip('+repr(params)+',args))']
 for temp in temps:lines.append(' t['+repr(temp)+']=0')
 counter=[0]
 def emit(n,indent=1):
  pad=' '*indent;op,*a=n
  if op=='=':
   dest,val=a
   if isinstance(dest,Array):lines.append(pad+'put('+('t['+repr(dest[0])+']' if dest[0] in local else 'self.arrays['+repr(dest[0])+']')+','+expr(dest[1])+','+expr(val)+')')
   else:lines.append(pad+('t' if dest in local else 'self.p')+'['+repr(dest)+']='+expr(val))
  elif op in ('++','--'):emit(['=',a[0],['+' if op=='++' else '-',a[0],1]],indent)
  elif op=='return':lines.append(pad+'return '+(expr(a[0]) if a else '0'))
  elif op=='if':
   cut=a.index('else') if 'else' in a else len(a);lines.append(pad+'if '+expr(a[0])+':')
   for child in a[1:cut]:emit(child,indent+1)
   if cut<len(a):
    lines.append(pad+'else:')
    for child in a[cut+1:]:emit(child,indent+1)
  elif op=='switch':
   counter[0]+=1;name='switch'+str(counter[0]);lines.append(pad+name+'='+expr(a[0]))
   for i,b in enumerate(a[1:]):
    lines.append(pad+('else:' if b[0]=='else' else ('if ' if i==0 else 'elif ')+name+'=='+expr(b[0])+':'))
    for child in b[1:]:emit(child,indent+1)
  elif op=='for':
   for child in a[0]:emit(child,indent)
   lines.append(pad+'while '+expr(a[1])+':')
   for child in a[3:]:emit(child,indent+1)
   for child in a[2]:emit(child,indent+1)
  else:lines.append(pad+expr(n))
 for n in method[2:]:emit(n)
 lines.append(' return 0');env={'word':word,'at':at,'put':put,'require':require};exec('\n'.join(lines),env);return env['run']

class FastSource(VM):
 def __init__(self,*a,**kw):self.fast={};super().__init__(*a,**kw)
 def call(self,name,*args):
  if name not in self.fast:
   key=(repr(self.constants),repr(self.methods[name]))
   if key not in _SOURCE_CACHE:_SOURCE_CACHE[key]=source_function(self,self.methods[name])
   self.fast[name]=_SOURCE_CACHE[key]
  return self.fast[name](self,*args)

def emitted_function(vm,name):
 start=vm.methods[name];pending=[start];instructions={}
 while pending:
  pc=pending.pop()
  if pc in instructions:continue
  op,args,end=decode(vm.blob,pc,vm.argtypes);instructions[pc]=(op,args,end)
  if op in (23,24,25):pending.append(end+args[0])
  if op not in (25,36):pending.append(end)
 leaders={start}
 for pc,(op,args,end) in instructions.items():
  if op in (23,24,25):leaders.add(end+args[0]);leaders.add(end)
 leaders &= set(instructions)
 blocks={}
 for leader in sorted(leaders):
  block=[];pc=leader
  while True:
   op,args,end=instructions[pc];block.append((pc,op,args,end))
   if op in (23,24,25,36) or end in leaders:break
   pc=end
  blocks[leader]=block
 lines=['def run(self,*params):',f' require(len(params)=={vm.arities[name]},"emitted arity")',' self.depth+=1;self.max_depth=max(self.max_depth,self.depth)',' stack=[];acc=0;prev=0;temps=[];par=[len(params),*params]',f' pc={start}',' visits=0',' while True:','  visits+=1;require(visits<100000,"emitted runaway")']
 for b,(leader,block) in enumerate(blocks.items()):
  lines.append(('  if ' if b==0 else '  elif ')+f'pc=={leader}:');pad='   ';lines.append(pad+f'self.executed+={len(block)}')
  for pc,op,args,end in block:
   arg=args[0] if args else None
   if op==31:line=f'temps=[0]*{arg}'
   elif op==26:line=f'acc={signed(arg)}'
   elif op==27:line='stack.append(acc)'
   elif op==28:line=f'stack.append({signed(arg)})'
   elif op==29:line='stack.pop()'
   elif op==30:line='stack.append(stack[-1])'
   elif op in (59,60,61):line=f'stack.append({op-59})'
   elif op==62:line='stack.append(self)'
   elif op==46:line='acc=self'
   elif op==48:line='stack.append(prev)'
   elif op in (23,24):line=f'pc={end+arg} if '+('acc' if op==23 else 'not acc')+f' else {end};continue'
   elif op==25:line=f'pc={end+arg};continue'
   elif op==12:line='acc=int(not acc)'
   elif op==11:line='acc=word(-acc)'
   elif op==0:line='acc=word(~acc)'
   elif op in range(1,11) or op in range(13,23):
    expressions={1:'l+r',2:'l-r',3:'l*r',4:'int(l/r)',5:'l-int(l/r)*r',6:'(l&65535)>>r',7:'l<<r',8:'l^r',9:'l&r',10:'l|r',13:'int(l==r)',14:'int(l!=r)',15:'int(l>r)',16:'int(l>=r)',17:'int(l<r)',18:'int(l<=r)',19:'int((l&65535)>(r&65535))',20:'int((l&65535)>=(r&65535))',21:'int((l&65535)<(r&65535))',22:'int((l&65535)<=(r&65535))'}
    line='l=stack.pop();r=acc;'+('prev=r;' if op>=13 else '')+'acc=word('+expressions[op]+')'
   elif op in range(49,57):
    key=repr(vm.propmap[arg]);ref=f'self.p[{key}]'
    line={49:f'acc={ref}',50:f'{ref}=acc',51:f'stack.append({ref})',52:f'{ref}=stack.pop()'}.get(op)
    if line is None:line=f'{ref}=word({ref}'+('+1' if op in (53,55) else '-1')+');'+(f'acc={ref}' if op in (53,54) else f'stack.append({ref})')
   elif op in (42,37):
    count=arg//2;line=f'require({count}<=len(stack));vals=stack[-{count}:];del stack[-{count}:];acc=self.send('+('self' if op==42 else 'acc')+',vals)'
   elif op>=64:
    scope=op&3;require(scope!=0,'global opcode forbidden');space={1:'self.locals',2:'temps',3:'par'}[scope];idx=f'{arg}'+('+acc' if op&8 else '');family=(op-64)//16;tos=bool(op&4)
    if family==0:line=('stack.append(' if tos else 'acc=')+f'at({space},{idx})'+(')' if tos else '')
    elif family==1:line=f'put({space},{idx},'+('stack.pop()' if tos or op&8 else 'acc')+')'
    else:line=f'i={idx};value=word(at({space},i)'+('+1' if family==2 else '-1')+f');put({space},i,value);'+('stack.append(value)' if tos else 'acc=value')
   elif op==36:line=f'require(len(stack)<={vm.switches[name]},"return stack imbalance");self.depth-=1;return acc'
   else:raise RuntimeError(('unsupported emitted opcode',name,pc,op,args))
   lines.append(pad+line)
   if 'stack.append' in line:lines.append(pad+'self.max_stack=max(self.max_stack,len(stack))')
  if block[-1][1] not in (23,24,25,36):lines.append(pad+f'pc={block[-1][3]};continue')
 lines.append('  else:raise RuntimeError(("bad emitted PC",pc))');env={'word':word,'at':at,'put':put,'require':require};exec('\n'.join(lines),env);return env['run']

class FastBytecode(BytecodeVM):
 def __init__(self,*a,**kw):self.fast={};super().__init__(*a,**kw)
 def call(self,name,*params):
  if name not in self.fast:
   key=(hashlib.sha256(self.blob).hexdigest(),name,repr(self.propmap),repr(self.arities),self.switches[name])
   if key not in _EMITTED_CACHE:_EMITTED_CACHE[key]=emitted_function(self,name)
   self.fast[name]=_EMITTED_CACHE[key]
  return self.fast[name](self,*params)
