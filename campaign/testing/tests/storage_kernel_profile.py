"""Exact-tag SCI16 slot/cache model with in-memory files; NOT native I/O proof."""
import copy,re
import host
from test_restore import Backend

class StorageBackend(Backend):
 def __init__(self,vm,occupied=(),raw=(),unsupported=(),result=1):
  self.target='renamed-campaign';self.recognized=set(occupied);self.unsupported=set(unsupported)
  self.raw={f'{self.target}.{i:03d}':f'manual-{i}'.encode() for i in occupied}
  self.raw.update({name:b'opaque occupied file' for name in raw});self.auto_result=result
  self.last_virtual=1;self.last_physical=5;self.auto_operations=[];self.autosaved={};self.checks=[];self.before_return=None
  super().__init__(vm)
 def kernel(self,k,args):
  name=self.vm.knames.get(k)
  if name=='GetSaveFiles':
   assert len(args)==3 and host.base.read_string(args[0])=='cakood'
   names,slots=args[1:];assert names.region.limit(names.offset)-names.offset==722
   assert slots.region.limit(slots.offset)-slots.offset==40
   before_names=list(names.region.words);before_slots=list(slots.region.words)
   self.last_virtual=100;ids=sorted(self.recognized)[:20]
   for i,n in enumerate(ids):
    host.base.write_string(host.base.Pointer(names.region,names.offset+36*i),f'manual-{n}')
    slots.region.words[slots.offset//2+i]=100+n
   names.region.put(names.offset+36*len(ids),0)
   # The names and IDs share the same SCI locals region. Assert their union only.
   allowed=set(range(names.offset//2,names.offset//2+361))|set(range(slots.offset//2,slots.offset//2+20))
   assert all(a==b for i,(a,b) in enumerate(zip(before_names,names.region.words)) if i not in allowed)
   self.auto_operations.append(('enumerate',len(ids)));self.vm.ktrace.append((name,tuple(args)));return len(ids)
  if name=='CheckSaveGame':
   assert len(args)==2 and host.base.read_string(args[0])=='cakood';virtual=args[1];assert 101<=virtual<=199
   self.checks.append(virtual);self.vm.ktrace.append((name,tuple(args)))
   return int(virtual-100 in self.recognized and virtual-100 not in self.unsupported)
  if name=='FileIO' and args[0]==10 and host.base.read_string(args[1]).startswith('*.'):
   assert len(args)==2;pattern=host.base.read_string(args[1]);m=re.fullmatch(r'\*\.([0-9]{3})',pattern);assert m
   present=any(n.endswith(pattern[1:]) for n in self.raw);self.auto_operations.append(('exists',pattern,int(present)));self.vm.ktrace.append((name,tuple(args)));return int(present)
  if name=='SaveGame' and args[0]!=0:
   assert len(args)==3 and host.base.read_string(args[0])=='cakood' and args[1]==1 and host.base.read_string(args[2])=='BEGIN THE EVENING.'
   s=self.vm.objects['p08State'];h=self.vm.objects['cakood']
   assert s.arrays['h8IO'][0]==2 and s.p['h8Critical']==0 and s.p['p08Busy']==0
   assert h.p['uiPanel']==0 and h.p['motionPhase']==0
   slot=self.last_physical if self.last_virtual==1 else next((i for i in range(1,100) if i not in self.recognized),None)
   assert slot is not None,'native fatal full-slot branch would have been entered'
   assert slot==s.arrays['h8IO'][10] and not any(n.endswith(f'.{slot:03d}') for n in self.raw),'unchecked/occupied slot'
   self.last_virtual=1;self.last_physical=slot;self.auto_operations.append(('save',slot,self.auto_result));self.vm.ktrace.append((name,tuple(args)))
   snapshot=copy.deepcopy(self.vm.snapshot())
   if self.auto_result==1:
    self.autosaved[slot]=snapshot;self.recognized.add(slot);self.raw[f'{self.target}.{slot:03d}']=f'auto-{slot}-{len(self.auto_operations)}'.encode()
   if self.before_return:self.before_return(snapshot)
   return self.auto_result
  return super().kernel(k,args)
