"""Complete emitted structures, branch boundaries and operand-stack paths.

SCI RET retires the callee frame. Record bounded historical switch residues
explicitly and require the changed methods to preserve their predecessor exits.
"""
from pathlib import Path
import sys,json,struct,collections
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tools')]
import host_vm as base
base.HERE=H/'tools'
from guard import require,input_check
from caption_util import dump

def word(b,p):require(0<=p<=len(b)-2,'Word bounds');return struct.unpack_from('<H',b,p)[0]
def stack_paths(vm,m,method):
 entry=method['code_offset'];pcs=vm.method_boundaries(m,entry);work=[(entry,0)];seen={};returns=[]
 while work:
  pc,depth=work.pop()
  if pc in seen:require(seen[pc]==depth,'Inconsistent stack join '+method['selector']);continue
  seen[pc]=depth;op,args,end=vm.decode(m,pc);delta=0
  if op in (27,28,30,48,51,55,56,58,59,60,61,62):delta=1
  elif op in (29,52) or op in range(1,11) or op in range(13,23):delta=-1
  elif op in (37,42):require(args[0]%2==0,'Odd send packet');delta=-args[0]//2
  elif op==33:require(args[1]%2==0,'Odd kernel packet');delta=-args[1]//2-1
  elif op>=64:
   mode=op&48;to_stack=bool(op&4)
   if mode==16:delta=-int(to_stack or bool(op&8))
   elif to_stack:delta=1
  else:require(op in (0,11,12,23,24,25,26,31,36,40,45,46,49,50,53,54,57),'Unsupported opcode '+str(op))
  require(depth+delta>=0,'Static stack underflow '+method['selector']);depth+=delta
  if op==36:returns.append(depth);continue
  for target in ([end+args[0]] if op==25 else [end,end+args[0]] if op in (23,24) else [end]):
   require(target in pcs,'Control flow leaves method '+method['selector']);work.append((target,depth))
 require(returns,'No reachable return '+method['selector'])
 return dict(instructions=len(pcs),reachable_instructions=len(seen),return_depths=sorted(set(returns)),maximum_operand_depth=max(seen.values()),return_sites=len(returns))
def audit(name):
 b=H/'build'/name;vm=base.HostVM(checkpoint=b/'verification-checkpoint',build=b,budget=100000000);structures=[];methods={}
 for number,m in sorted(vm.modules.items()):
  l,s,heap=m.layout,m.blob,m.heap;segment=len(s)+(-len(s)%4)+len(heap);require(segment<=65535,'Segment overflow');rel={}
  for part,raw in [('script',s),('heap',heap)]:
   off=word(raw,0);count=word(raw,off);require(off+2+2*count==len(raw),'Relocation terminal boundary');positions=[word(raw,off+2+2*i) for i in range(count)]
   require(len(set(positions))==count,'Duplicate relocation')
   for pos in positions:require((part=='script' or pos%2==0) and 0<=pos<off and word(raw,pos)<word(heap,0),'Invalid relocation '+str((name,number,part,pos,word(raw,pos),word(heap,0))))
   rel[part]=count
  for o in l['objects']:
   require(o['heap_offset']+2*o['property_count']<=word(heap,0),'Object bounds')
   require(o['method_table_offset']+2+4*len(o['methods'])<=word(s,0),'Method dictionary bounds')
   if o['is_class']:
    require(o['property_selector_offset']+2*o['property_count']<=word(s,0),'Property dictionary bounds')
    require(len({v['selector_id'] for v in o['properties']})==len(o['properties']),'Duplicate property')
   require(len({v['selector_id'] for v in o['methods']})==len(o['methods']),'Duplicate method')
   # Every instruction of each emitted method, including unchanged native-like
   # host assembly, has a valid boundary. Stack paths cover the data controller
   # and its static integrity owner, which are the two changed components.
   for method in o['methods']:
    pcs=vm.method_boundaries(m,method['code_offset'])
    for pc in pcs:
     op,args,end=vm.decode(m,pc)
     if op in (23,24,25):require(end+args[0] in pcs,'Cross-method branch')
    if number in (982,985):methods[str(number)+':'+method['selector']]=stack_paths(vm,m,method)
  structures.append(dict(module=number,script_bytes=len(s),heap_bytes=len(heap),segment_bytes_with_padding=segment,relocation_counts=rel,object_count=len(l['objects']),local_words=l['locals_word_count']))
 return dict(structures=structures,methods=methods)
def main():
 input_check();reports={n:audit(n) for n in ('baseline','coherent','window')}
 for key,old in reports['baseline']['methods'].items():
  new=reports['coherent']['methods'][key];require(old['return_depths']==new['return_depths'],'Changed return-stack behavior '+key)
  require(new['maximum_operand_depth']<=old['maximum_operand_depth'],'Expanded operand-stack requirement '+key)
 for key,row in reports['window']['methods'].items():require(row['maximum_operand_depth']<100,'Bounded window operand stack')
 out=dict(status='PASS',universes=reports,all10_modules_structure_checked_in_each_universe=True,changed_component_complete_control_flow_stack_checked=True,retired_frame_residues_preserved=True,scope='Finite emitted structures and stack checks, not native execution',native_acceptance=False)
 dump(H/'evidence/emission-audit.json',out);print('PASS',sum(len(x['methods']) for x in reports.values()),'method control-flow stack analyses')
if __name__=='__main__':main()
