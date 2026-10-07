"""Conservative emitted-instruction stack/branch audit, no native execution."""
from collections import deque
from music_vm import MusicVM
from host_vm import require,signed

def audit():
 v=MusicVM();reports=[];unknown=None
 for number in (940,941,942,943,981,986):
  m=v.modules[number];entries={row['code_offset']:row['selector'] for obj in m.layout['objects'] for row in obj['methods']}
  if number in v.apis:
   for name,index in v.apis[number].items():entries[m.layout['exports'][index]]=name
  for entry,name in sorted(entries.items()):
   allowed=v.method_boundaries(m,entry);work=deque([(entry,(),None)]);seen=set();peak=0;returns=set();kernels=0;sends=0
   while work:
    pc,st,acc=work.popleft();key=(pc,st,acc)
    if key in seen:continue
    seen.add(key);require(len(seen)<100000,'Static audit state explosion',number,name)
    require(pc in allowed,'Branch leaves procedure',number,name,pc)
    op,args,end=v.decode(m,pc);stack=list(st);peak=max(peak,len(stack));arg=args[0] if args else None
    def pop():require(stack,'Static operand stack underflow',number,name,pc);return stack.pop()
    if op in range(1,11) or op in range(13,23):pop();acc=None
    elif op in(0,11,12):acc=None
    elif op==26:acc=signed(arg)
    elif op==27:stack.append(acc)
    elif op==28:stack.append(signed(arg))
    elif op==29:pop()
    elif op==30:val=pop();stack.extend([val,val])
    elif op in(59,60,61):stack.append(op-59)
    elif op in(48,58,62):stack.append(None)
    elif op in(31,):pass
    elif op in(40,45,46,49,53,54,57):acc=None
    elif op==50:pass
    elif op in(51,55,56):stack.append(None)
    elif op==52:pop()
    elif op in(32,33,35):
     count=args[-1]//2;require(args[-1]%2==0,'Odd call argument bytes');packet=[pop()for _ in range(count+1)][::-1]
     require(packet[0]==count,'Static call argc mismatch',number,name,pc,packet,count);acc=None;kernels+=int(op==33)
    elif op in(37,42):
     count=arg//2;require(arg%2==0,'Odd send argument bytes');packet=[pop()for _ in range(count)][::-1];i=0
     while i<len(packet):
      require(i+2<=len(packet),'Static send header',number,name,pc);selector,argc=packet[i:i+2]
      require(isinstance(selector,int) and selector in v.names,'Static selector identity',number,name,pc,selector)
      require(isinstance(argc,int) and argc>=0,'Static send arity unknown',number,name,pc,argc);i+=2+argc
     require(i==len(packet),'Static send size mismatch',number,name,pc,packet);acc=None;sends+=1
    elif op>=64:
     family=(op-64)//16;tos=bool(op&4)
     if family==1:
      if tos or op&8:pop()
     elif tos:stack.append(None)
     else:acc=None
    elif op==36:returns.add(len(stack));continue
    elif op not in(23,24,25):raise RuntimeError(('Unsupported static opcode',number,name,v.opnames[op]))
    nexts=[end+arg] if op==25 else [end,end+arg] if op in(23,24) else [end]
    for nxt in nexts:work.append((nxt,tuple(stack),acc))
   require(bool(returns),'No reachable return',number,name)
   reports.append({'module':number,'entry':name,'entry_pc':entry,'reachable_states':len(seen),'maximum_operand_words':peak,'return_operand_words':sorted(returns),'kernel_call_paths':kernels,'send_paths':sends})
 return {'status':'PASS','scope':'Every940/941/942/943/981/986 method and exported music procedure; conservative branches; call counts, selector identity and stack underflow checked. Not a native VM proof.','entries':reports,'maximum_operand_words':max(r['maximum_operand_words'] for r in reports)}
if __name__=='__main__':
 import json
 from music_vm import H
 result=audit();(H/'evidence/stack-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(len(result['entries']),'entry points checked; max stack',result['maximum_operand_words'])
