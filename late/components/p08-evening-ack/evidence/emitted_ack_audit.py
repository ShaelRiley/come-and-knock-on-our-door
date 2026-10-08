"""Independent static instruction/branch/stack analysis of emitted module 989."""
from pathlib import Path
import json,sys,hashlib,collections
H=Path(sys.argv[1]).resolve();R=H/'evidence';sys.dont_write_bytecode=True;sys.path[:0]=[str(H/'tests'),str(H/'tools')]
import host
vm=host.VM();m=vm.modules[989];obj=vm.classes[11];rows=[]
for name,start in sorted(obj.methods.items(),key=lambda x:x[1]):
 allowed=vm.method_boundaries(m,start);decoded={pc:vm.decode(m,pc) for pc in allowed}
 incoming={start:0};todo=[start];maxdepth=0;branches=0;sends=0;kernels=[];retdepth=set();temps=0
 while todo:
  pc=todo.pop();depth=incoming[pc];op,args,nxt=decoded[pc];out=depth
  if op in (27,28,48,51,55,56,58,59,60,61,62):out+=1
  elif op in tuple(range(1,11))+tuple(range(13,23))+(29,52):out-=1
  elif op==30:assert depth>=1,(name,pc,'dup');out+=1
  elif op==31:assert pc==start and depth==0,(name,pc,'link');temps=args[0]
  elif op in (37,42):assert args[0]%2==0;out-=args[0]//2;sends+=1
  elif op==33:assert args[1]%2==0;out-=args[1]//2+1;kernels.append(vm.knames[args[0]])
  elif op>=64:
   family=(op-64)//16;tos=bool(op&4)
   if family in (0,2,3) and tos:out+=1
   elif family==1 and (tos or op&8):out-=1
   if op&3==2:assert 0<=args[0]<temps,(name,pc,'temp',args[0],temps)
  else:assert op in (0,11,12,23,24,25,26,36,40,45,46,49,50,53,54,57),(name,pc,op)
  assert out>=0,(name,pc,'stack underflow',depth,op,args)
  maxdepth=max(maxdepth,out)
  if op in (57,58):assert pc+1 in m.relocations;assert m.layout['strings_start']<=args[0]<len(m.heap)
  if op==36:retdepth.add(out);continue
  if op in (23,24,25):
   target=nxt+args[0];assert target in allowed,(name,pc,'branch out',target);branches+=1
   successors=[target] if op==25 else [target,nxt]
  else:successors=[nxt]
  for target in successors:
   assert target in allowed,(name,pc,'fallthrough',target)
   if target in incoming:assert incoming[target]==out,(name,target,'stack merge',incoming[target],out)
   else:incoming[target]=out;todo.append(target)
 rows.append({'method':name,'entry':start,'decoded_instructions':len(allowed),'reachable_instructions':len(incoming),'branches':branches,'sends':sends,'kernels':kernels,'max_operand_words':maxdepth,'temporary_words':temps,'return_frame_stack_depths':sorted(retdepth)})
assert [x['method'] for x in rows if 'SaveGame' in x['kernels']]==['h8S']
report={'status':'PASS','scope':'All emitted class 11 / module 989 methods. Exact instruction boundaries, branch targets, equal stack depth at joins, stack underflow, temp bounds and literal relocations. SCI return discards each method frame; switch discriminator values at RET are legal.','compile_receipt_sha256':hashlib.sha256((H/'build/coherent/compile-receipt.json').read_bytes()).hexdigest(),'methods':len(rows),'instructions':sum(x['decoded_instructions'] for x in rows),'branches':sum(x['branches'] for x in rows),'max_operand_words':max(x['max_operand_words'] for x in rows),'max_temporary_words':max(x['temporary_words'] for x in rows),'rows':rows}
(R/'emitted-audit.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k!='rows'})
