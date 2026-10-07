"""Actual emitted complete P05 lifecycle fixture; explicit native save transfer model."""
import copy,json
from music_vm import MusicVM,H
from host_vm import Object,require,EndOfEvents
class RestoreTransfer(Exception):
 def __init__(self,restored):self.restored=restored
class SaveVM(MusicVM):
 def __init__(self):
  super().__init__('p05-composition');self.save_result=1;self.saves=[];self.load_snapshot=None;self.load_calls=0;self.native_restore_retired=[];self.retiring_events=False
  folder=H/'inputs/revision2/p05-replay-resources'
  for row in json.loads((folder/'manifest.json').read_text()):self.resources[3,row['number']]=(folder/row['extracted_path']).read_bytes()
 def call(self,obj,name,args=()):
  if name=='eventLoop':self.retiring_events=False
  return super().call(obj,name,args)
 def _kernel(self,k,args):
  name=self.knames[k]
  if name=='SaveGame':
   require(args==[0,-1,0],'Save kernel packet',args)
   require(not self.saves,'Fixture capture must start empty')
   self.saves.append(copy.deepcopy(self));return self.save_result
  if name=='RestoreGame':
   require(args==[0,-1,0],'Restore kernel packet',args);self.load_calls+=1
   if self.load_snapshot is None:return 0
   # Stock RestoreGame clears old playlist before loading saved slots and abandons
   # its old SCI invocation stack. This models that transfer; no native proof.
   self.native_restore_retired.extend(o.name for o in self.parsers);self.parsers.clear()
   restored=copy.deepcopy(self.load_snapshot);restored.depth=0
   raise RestoreTransfer(restored)
  if name=='SetCursor':
   require(args in([205,0,0],[1],[0]),'SetCursor packet',args);return self._kernel_accumulator
  if name=='GetEvent' and self.retiring_events:
   # hRetireTransient drains the empty native backlog before resumed eventLoop.
   require(args[0]==32767 and isinstance(args[1],Object),'retirement GetEvent');return 0
  # Pinned soundcmd.cpp:283-317,873-895 returns the accumulator for absent slots.
  if name=='DoSound' and args[0]in(7,9,16)and args[1]not in self.parsers:
   obj=args[1];require(isinstance(obj,Object)and obj.module.number==0 and obj.name in('credits','bed'),'No-slot retired legacy owner',args)
   require(len(args)==(3 if args[0]==16 else 2),'No-slot sound arity')
   if args[0]==16:obj.p['loop']=-1 if args[2]==-1 else 1
   self.ktrace.append(('DoSound',tuple(args)));return self._kernel_accumulator
  return super()._kernel(k,args)
def full_fixture():
 v=SaveVM();h,d,a,p,q,r=[v.objects[n]for n in('cakood','sceneDialogue','presentationAudio','p03State','p04State','p05State')]
 h.p.update(dialogue=d,presentation=a,p03=p,p04=q,p05=r,opening=0,initialized=1,houseEntered=1,traySafe=1,tray=2,location=1,roomSeen=1,wedge=1,audioReady=1,masterVolume=61,musicMuted=0,paused=0,menuOpen=0,audioDuckTicks=0,audioDesired=0)
 h.call('p02Init');p.call('p03Init');q.call('p04Init');r.call('hInit',h);p.p['bEnabled']=1
 q.p['qEnabled']=q.call('qRoutesReady',h);h.call('p02SyncInventory',0);h.call('p02HostInventory')
 require(r.call('hSaveReady')==1,'Complete P05 fixture must be save-ready')
 require(v.proc('rbInit',v.objects['responsiveSound'],v.objects['musicTransport'],0,17061)==1,'Music fixture init')
 for _ in range(10):v.advance(2);h.call('audioPoll',2)
 return v

def load_earlier(v,saved):
 v.load_snapshot=saved
 try:v.objects['cakood'].call('readSave')
 except RestoreTransfer as transfer:restored=transfer.restored
 else:raise AssertionError('Actual readSave did not transfer to saved state')
 # Native reconstruction is modeled by the captured frozen parser graph above.
 restored.event_queue=[];restored.retiring_events=True
 try:restored.objects['cakood'].call('replay')
 except EndOfEvents:pass
 finally:restored.event_queue=None
 require(restored.depth==0,'Old/replay stack must unwind')
 return restored
