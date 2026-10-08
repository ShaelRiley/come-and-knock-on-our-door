"""New complete structure, SCO, relocation, segment and instruction checks."""
from pathlib import Path
import sys,json,struct,collections,hashlib
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H/'tests'),str(H),str(H/'reference/component'),str(H/'reference/component/tests')]
from verify_source import verify
from test_domain import Harness
from paired import PairedVM
from source_vm import SIGNATURES
from domain_metadata import declarations

def check(ok,*why):
 if not ok:raise ValueError(why)
def word(b,p):check(0<=p<=len(b)-2,'word bounds',p);return struct.unpack_from('<H',b,p)[0]
def sco(path,number,layout):
 b=path.read_bytes();check(b[:8]==b'SCO\x01\x00\x00\x01\x00','SCO header');check(word(b,8)==number,'SCO script')
 pubs,po,classes,co,locals_,lo=struct.unpack_from('<6H',b,10);p=22
 def w():
  nonlocal p
  n=word(b,p);p+=2;return n
 def string():
  nonlocal p
  n=w();check(n>0 and p+n<=len(b),'SCO string bounds');s=b[p:p+n];p+=n;check(s[-1]==0,'SCO string terminator');return s[:-1].decode('ascii')
 exported=[]
 if pubs:check(p==po,'SCO exports offset')
 for i in range(pubs):exported.append((w(),string()))
 check(exported==([(0,'p14State')] if number==996 else []),'SCO export contract',exported)
 check(p==co and classes==1,'SCO classes')
 name=string();np,nm,species,superclass=w(),w(),w(),w();cl=next(o for o in layout['objects'] if o['is_class'])
 check((name,np,nm,species,superclass)==(cl['name'],len(cl['properties'])-9,len(cl['methods']),cl['species'],cl['superclass']),'SCO class identity')
 props=[(w(),w()) for i in range(np)];check(props==[(r['selector_id'],r['raw_value']) for r in cl['properties'][9:]],'SCO properties')
 methods=[w() for i in range(nm)];check(methods==[r['selector_id'] for r in cl['methods']],'SCO methods')
 if locals_:check(p==lo,'SCO locals offset')
 names=[string() for i in range(locals_)];check(locals_==layout['locals_word_count'] and p==len(b),'SCO complete local coverage')
 source=H/('tools/compiler-main.sc' if number==0 else 'src/module996.sc')
 for a in declarations(source.read_text()):check(names[a['word_offset']]==a['name'],'SCO local name',a['name'])
 return dict(bytes=len(b),exports=exported,classes=classes,nondefault_properties=np,methods=nm,locals=locals_,sha256=hashlib.sha256(b).hexdigest())
def stack_paths(vm,m,method):
 entry=method['code_offset'];pcs=vm.method_boundaries(m,entry);work=[(entry,0)];seen={};returns=[]
 while work:
  pc,depth=work.pop()
  if pc in seen:
   check(seen[pc]==depth,'Inconsistent control-flow stack height',method['selector'],pc,seen[pc],depth);continue
  seen[pc]=depth;op,args,end=vm.decode(m,pc);delta=0
  if op in (27,28,30,48,51,55,56,59,60,61,62):delta=1
  elif op in (29,52) or op in range(1,11) or op in range(13,23):delta=-1
  elif op==42:delta=-args[0]//2
  elif op>=64:
   mode=op&48;to_stack=bool(op&4)
   if mode==16:delta=-int(to_stack or bool(op&8))
   elif to_stack:delta=1
  check(depth+delta>=0,'Static operand underflow',method['selector'],pc,op,depth,delta)
  depth+=delta
  if op==36:check(depth==0,'Nonempty return stack',method['selector'],pc,depth);returns.append(pc);continue
  for target in ([end+args[0]] if op==25 else [end,end+args[0]] if op in (23,24) else [end]):
   check(target in pcs,'Control flow leaves method',method['selector'],target);work.append((target,depth))
 check(returns,'No reachable method return',method['selector']);return dict(reachable_instructions=len(seen),return_sites=len(returns),all_return_operand_stacks_empty=True)
def main():
 if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
 guard=verify();h=Harness(PairedVM);h.finish();h.restore();h.queries();vm=h.v.emitted.domain.vm
 structures=[];opcodes=collections.Counter();methods=[]
 for number,m in sorted(vm.modules.items()):
  l=m.layout;s=m.blob;heap=m.heap;segment=len(s)+(-len(s)%4)+len(heap);check(segment<=65535,'SCI16 segment overflow')
  rel={}
  for name,b in [('script',s),('heap',heap)]:
   off=word(b,0);n=word(b,off);check(off+2+2*n==len(b),'Relocation terminal boundary',number,name)
   positions=[word(b,off+2+2*i) for i in range(n)];check(len(set(positions))==n,'Duplicate relocation')
   for x in positions:check(x%2==0 and 0<=x<off and word(b,x)<word(heap,0),'Invalid relocation',name,x)
   rel[name]=positions
  classes=[o for o in l['objects'] if o['is_class']];instances=[o for o in l['objects'] if not o['is_class']]
  check(len(classes)==1 and classes[0]['species']==(1 if number==996 else 0) and classes[0]['superclass']==65535,'Class universe')
  if number==996:
   check(len(instances)==1 and instances[0]['name']=='p14State' and instances[0]['superclass']==1 and instances[0]['species']==65535,'Instance universe')
   check(l['exports']==[instances[0]['heap_offset']] and 8 in rel['script'],'Export0 relocation')
  else:check(not instances and not l['exports'],'Isolated root has no instance or export')
  for o in l['objects']:
   check(o['heap_offset']+2*o['property_count']<=word(heap,0),'Object bounds')
   if o['is_class']:check(o['property_selector_offset']+2*o['property_count']<=word(s,0),'Property dictionary bounds')
   check(o['method_table_offset']+2+4*len(o['methods'])<=word(s,0),'Method dictionary bounds')
   if o['is_class']:check(len({v['selector_id'] for v in o['properties']})==len(o['properties']),'Duplicate property')
   else:
    check(o['property_count']==classes[0]['property_count'],'Inherited instance property count')
    check([v['raw_value'] for v in o['properties'][9:]]==[v['raw_value'] for v in classes[0]['properties'][9:]],'Instance property defaults')
   check(len({v['selector_id'] for v in o['methods']})==len(o['methods']),'Duplicate method')
   if not o['is_class']:continue
   for method in o['methods']:
    pcs=vm.method_boundaries(m,method['code_offset'])
    for pc in pcs:
     op,args,end=vm.decode(m,pc)
     check(op in set(range(32))|{36,42,48}|set(range(49,63))|set(range(64,128)),'Unexpected opcode/kernel/external call',method,pc,op)
     if op in (23,24,25):check(end+args[0] in pcs,'Cross-method branch')
     opcodes[vm.opnames[op]]+=1
    methods.append(dict(name=method['selector'],instructions=len(pcs),stack=stack_paths(vm,m,method)))
  structures.append(dict(module=number,script_bytes=len(s),heap_bytes=len(heap),segment_bytes_with_padding=segment,relocations=rel,sco=sco(H/f'build/isolated/src/{"main" if number==0 else "module996"}.sco',number,l)))
 for target,name,argc in vm.packets:check(argc==SIGNATURES[name],'Actual self-call arity',target,name,argc)
 check(not vm.depth and not vm.chain and not vm.kernel_attempts,'Unfinished stack or unexpected kernels')
 check(all(not r[4] for r in vm.returns),'Runtime operand residue')
 # Record any within-frame switch residues explicitly, never equate RET cleanup with leaked caller operands.
 report=dict(status='PASS',source=guard,structures=structures,methods=methods,static_instructions=sum(opcodes.values()),static_opcodes=dict(opcodes),runtime=vm.report(),returns=len(vm.returns),depth_at_finish=vm.depth,actual_send_arities_checked=len(vm.packets),return_stack_semantics='All reachable static returns and every executed return have empty operand stacks; temporary frames are distinct and discarded by RET',native_acceptance=False)
 (H/'evidence/emission-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS_COMPLETE_STRUCTURE_EMISSION',len(methods),sum(opcodes.values()),vm.steps)
if __name__=='__main__':main()
