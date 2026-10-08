"""First bounded actual-campaign emission equivalence milestone."""
import sys,json,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H));sys.path.insert(0,str(H/'tests'))
import host
from test_return_caption import boot,first_entry
from host import act,close
from derive import dump,sha

def value(v):
 if isinstance(v,host.base.Object):return ['object',v.name]
 if isinstance(v,host.base.Pointer):
  if v.region.data is not None:return ['string',host.base.read_string(v)]
  return ['pointer',v.region.name,v.offset]
 return v

def state(h):
 vm=h.vm
 return {'objects':{n:{k:value(v) for k,v in o.p.items()} for n,o in vm.objects.items() if o.module.number!=991},'locals':{n:[value(v) for v in m.local.words] for n,m in vm.modules.items() if n!=991}}
def trace(vm):return [(n,[value(v) for v in a]) for n,a in vm.ktrace if not(n=='ScriptID' and list(a)==[991,0])]
def compare(pair,method,*args):
 rows=[]
 for h in pair:
  h.vm.ktrace.clear();before=state(h);r=h.call(method,*args);rows.append((value(r),trace(h.vm),state(h)))
 assert rows[0]==rows[1],(method,args,rows[0],rows[1])
 return len(rows[0][1])

def run():
 pair=[boot(H/'frozen/p09'),boot(H)];checks=[]
 for phase in ['porch','living','kitchen','conservatory','side']:
  if phase=='living':
   for h in pair:first_entry(h)
  elif phase=='kitchen':
   for h in pair:act(h,0,12)
  elif phase=='conservatory':
   for h in pair:act(h,0,18);act(h,0,1);act(h,0,16);close(h)
  elif phase=='side':
   for h in pair:act(h,0,17);act(h,0,14);close(h)
  assert pair[0].p['location']==dict(porch=0,living=1,kitchen=2,conservatory=6,side=3)[phase],phase
  assert state(pair[0])==state(pair[1]),phase
  for method,args in [('roomTitle',()),('drawWorld',()),('renderCaption',()),('render',())]:
   checks.append({'phase':phase,'room':pair[0].p['location'],'method':method,'kernel_calls':compare(pair,method,*args)})
 result={'status':'PASS_FIRST_EMITTED_EQUIVALENCE','checks':checks,'input_manifest_sha256':sha(H/'INPUT-MANIFEST.json'),'compile_receipt_sha256':sha(H/'build/coherent/compile-receipt.json'),'native_acceptance':False,'new_renderer_resolution':'Only ScriptID(991,0) excluded; every other kernel call, argument, order, return and state retained.'}
 dump(H/'evidence/first-equivalence.json',result);print(result['status'],len(checks))
if __name__=='__main__':run()
