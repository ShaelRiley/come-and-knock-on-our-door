from pathlib import Path
import sys,json,struct,copy
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tools'))
import host_vm as base
base.HERE=H/'tools'
from sound_stop_mock import install
SoundStopVM=install(base.HostVM,base)
class VM(SoundStopVM):
 def __init__(self):
  B=H/'build/coherent';super().__init__(checkpoint=B/'verification-checkpoint',build=B,budget=20000000);self.measurements=[];self.text_reads=[]
 def call(self,obj,name,args):
  result=super().call(obj,name,args)
  if name=='hVCPresented' and result==1:
   self.receipts=getattr(self,'receipts',[])+[dict(document=obj.p['hVCDocument'],record=obj.p['hVCRecord'],unit=obj.p['hVCUnit'],pages=obj.p['hVCPages'],seen=obj.p['hVCSeenCount'],graph12=sum(1 for n,a in self.ktrace if n=='Graph' and a[0]==12))]
  hook=getattr(self,'after_actual_call',None)
  if hook is not None:hook(obj,name,args,result)
  return result
 def _kernel(self,k,args):
  name=self.knames.get(k)
  if name=='SetCursor':
   assert args in ([205,0,0],[1],[0]),args
   self.cursor_calls=getattr(self,'cursor_calls',[])+[list(args)]
   return self._kernel_accumulator
  if name=='TextSize':
   dest,text,font,width=args;before=list(dest.region.words);prior=self._kernel_accumulator
   result=super()._kernel(k,args);start=dest.offset//2;after=dest.region.words
   assert before[:start]==after[:start] and before[start+4:]==after[start+4:]
   self.measurements.append(dict(text=base.read_string(text),width=width,width_limit=width,rect=after[start:start+4]));return prior
  if name=='GetFarText':
   result=super()._kernel(k,args);dest=args[2]
   self.text_reads.append(dict(resource=args[0],entry=args[1],bytes=len(base.read_string(dest).encode('latin1'))+1,capacity=dest.region.limit(dest.offset)-dest.offset));return result
  return super()._kernel(k,args)

def setup(plan=True):
 vm=VM();h,d,a,p,q,r=[vm.objects[n] for n in ('cakood','sceneDialogue','presentationAudio','p03State','p04State','p05State')]
 h.p.update(dialogue=d,presentation=a,p03=p,p04=q,p05=r,opening=0,initialized=1,houseEntered=1,traySafe=1,tray=2,location=1,roomSeen=1,wedge=1)
 h.call('p02Init');p.call('p03Init');q.call('p04Init');r.call('hInit',h);p.p['bEnabled']=1
 if plan:h.p.update(p02PlanAgreed=1,p02CopyJack=14,p02CopyBunny=14,p02CopyStringer=14,p02MasterHeld=1,p02Observed=63,p02BoardRecords=7,p02Compared=1,p02KnowPurpose=1,p02KnowOrder=1,p02SelectedAims=7)
 q.p['qEnabled']=q.call('qRoutesReady',h);h.call('p02SyncInventory',0);h.call('p02HostInventory')
 return h,d,a,p,q,r

def frame(h):
 h.p['dirty']=1;h.vm.pump([{}]);assert h.p['uiFailure']==0,(h.p['uiFailure'],h.p['location'],h.p['uiPanel'])
def close(h,read=True):
 for _ in range(40):
  if h.p['uiPanel'] not in (1,4):break
  if read:
   for page in range(h.p['uiPageCount']):
    if h.p['uiPage']!=page:h.call('uiTurnPage',page-h.p['uiPage'])
    frame(h)
  h.call('uiClose')
 frame(h)
def act(h,v,o,t=0):
 if h.p['uiPanel'] in (1,4):close(h)
 h.call('hostActNow',v,o,t)
 close(h)
def choice(h,c,i):h.call('uiHostChoice',c,i);close(h)
def garage(h):act(h,0,17);act(h,0,15);assert h.p['location']==5

def practical(h,r,listener=2):
 garage(h)
 if listener==2:act(h,0,9);act(h,6,10);choice(h,210,1);act(h,0,11)
 else:raise NotImplementedError
 act(h,7,65,66);act(h,7,64);choice(h,212,1);act(h,8,68);choice(h,213,listener)
 act(h,6,65);choice(h,214,listener)
 act(h,7,25,71);act(h,6,28);choice(h,211,3)
 assert r.call('p05Flags')==3,(r.call('p05Flags'),r.p['hLastCode'])
 return h
if __name__=='__main__':
 h,d,a,p,q,r=setup();frame(h);practical(h,r);print('PRACTICAL',r.call('p05Flags'),h.p['uiFailure'],r.p['hLastCode']);act(h,6,28);choice(h,211,5);print('LOAN BLOCKED',r.call('p05Flags'),r.p['hPARoom'],r.p['hLastCode'])
