#!/usr/bin/env python3
"""Exact owner method/kernel/persistent-store order, readers, menu, and restore."""
from pathlib import Path
import sys,json,copy,hashlib
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests')]
import host
from paint_source import VM as SourceVM
from test_return_caption import boot,first_entry
from test_restore import Backend,load
from check_milestone import value,state
from derive import dump,sha

class Writes(dict):
 def __init__(self,values,events,label):super().__init__(values);self.events=events;self.label=label
 def __setitem__(self,k,v):self.events.append(['write',self.label,k,value(v)]);super().__setitem__(k,v)
 def update(self,*a,**kw):
  for k,v in dict(*a,**kw).items():self[k]=v
class Words(list):
 def __init__(self,values,events,label):super().__init__(values);self.events=events;self.label=label
 def __setitem__(self,k,v):
  if isinstance(k,slice):
   ids=range(*k.indices(len(self)));assert len(ids)==len(v)
   for index,item in zip(ids,v):self.events.append(['word',self.label,index,value(item)])
  else:self.events.append(['word',self.label,k,value(v)])
  super().__setitem__(k,v)

def instrument(vm):
 events=[]
 def wrap_storage():
  for name,obj in vm.objects.items():
   if obj.module.number!=991:obj.p=Writes(obj.p,events,name)
  for n,m in vm.modules.items():
   if n!=991:m.local.words=Words(m.local.words,events,n)
  for name,source in getattr(vm,'paint_sources',{}).items():source.p=vm.objects[name].p;source.arrays=vm.arrays(source.number)
 wrap_storage();call=vm.call;kernel=vm._kernel;restore=vm.restore
 def call_logged(obj,name,args=()):
  source=getattr(vm,'paint_sources',{}).get(obj.name)
  keep=obj.module.number!=991 and not(source is not None and name in source.owned)
  if keep:events.append(['enter',obj.name,name,[value(v) for v in args]])
  result=call(obj,name,args)
  if keep:events.append(['return',obj.name,name,value(result)])
  return result
 def kernel_logged(k,args):
  name=vm.knames[k]
  if not(name=='ScriptID' and list(args)==[991,0]):events.append(['kernel',name,[value(v) for v in args]])
  return kernel(k,args)
 def restore_logged(s):
  result=restore(s);wrap_storage();return result
 for obj_name,source in getattr(vm,'paint_sources',{}).items():
  if source.number==991:continue
  def source_logger(source,obj_name):
   original_call=source.call
   def logged(name,*args):
    events.append(['enter',obj_name,name,[value(source.external(v)) for v in args]])
    result=original_call(name,*args)
    events.append(['return',obj_name,name,value(source.external(result))]);return result
   return logged
  source.call=source_logger(source,obj_name)
 vm.call=call_logged;vm._kernel=kernel_logged;vm.restore=restore_logged
 return events

def run():
 baseline={};rows=[];original=host.VM
 for i,(root,source) in enumerate([(H/'frozen/p09',False),(H,False),(H/'frozen/p09',True),(H,True)]):
  host.VM=SourceVM if source else original;h=boot(root);first_entry(h);host.VM=original
  backend=Backend(h.vm);events=instrument(h.vm)
  def check(label,action):
   events.clear();action();e={'events':copy.deepcopy(events),'state':state(h)}
   if i==0:baseline[label]=e
   else:
    if e!=baseline[label]:
     dump(H/f'evidence/order-failure-{i}-{label}.json',{'baseline':baseline[label],'actual':e});raise AssertionError(('Order mismatch',i,label))
   p=H/f'evidence/order/variant{i}-{label}.json';dump(p,e)
   rows.append({'variant':i,'case':label,'events':len(events),'evidence_sha256':sha(p)})
   dump(H/'evidence/state-order-progress.json',{'status':'RUNNING','cases':rows})
  for r in range(3):check(f'living-repeat-{r}',lambda:h.call('render'))
  check('open-reader',lambda:h.call('uiOpenReader',8))
  assert h.p['uiPanel'] in (1,4),(h.p['uiPanel'],h.p['uiFailure'])
  check('render-reader',lambda:h.call('render'))
  check('open-menu',lambda:h.call('uiHostMenu'))
  check('render-menu',lambda:h.call('render'))
  check('dismiss-menu',lambda:h.call('menuChoice',0))
  check('close-reader',lambda:host.close(h))
  check('save',lambda:h.call('writeSave'));assert backend.saved is not None
  saved=copy.deepcopy(backend.saved)
  check('travel-before-restore',lambda:host.act(h,0,17))
  check('restore',lambda:load(h,backend,saved));assert h.p['location']==1 and h.p['uiFailure']==0
  check('restored-render',lambda:h.call('render'))
 dump(H/'evidence/state-order-progress.json',{'status':'PASS_FOUR_WAY_ORDER_READER_MENU_RESTORE','cases':rows,'native_acceptance':False,'save_scope':'Actual writeSave/readSave/replay methods with typed same-program harness backend, not native SCI files','comparison':'Every original owner method entry/return, kernel argument and persistent property/local store in exact interleaved order; extra ScriptID991 calls excluded'})
 print('PASS_STATE_ORDER',len(rows),flush=True)
if __name__=='__main__':run()
