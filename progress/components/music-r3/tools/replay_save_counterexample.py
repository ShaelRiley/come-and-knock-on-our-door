from pathlib import Path
import sys,copy,types,json
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H/'tools'),str(H)]
from music_vm import MusicVM
v=MusicVM('p05-composition');h=v.objects['cakood'];s=v.objects['responsiveSound'];assert v.proc('rbInit',s,v.objects['musicTransport'],0,17061)==1
h.p.update(opening=0,audioReady=1,masterVolume=61,musicMuted=0,paused=0,menuOpen=0,audioDuckTicks=0,audioDesired=0,onApron=0,location=1,p05=0,p04=0)
for _ in range(3):v.advance(2);h.call('audioPoll',2)
d=v.objects['contestState'];d.call('vcInit');d.call('vcBindGeneration',0,1);w=v.domain_words();w[6]=1
for i in range(10,22):w[i]=1
assert d.call('vcEnter',1,0,7,1)==1;assert d.call('vcCommit')==1;assert v.proc('rbHostCommitted',3,d)==1;ready=d.call('vcSaveReady');assert ready==1
v.arrays(943)['rbGenerationHi'][0]=32767;v.arrays(943)['rbGenerationLo'][0]=32767;assert v.proc('rbRequest',151)==0
calls=[]
def kernel(vm,k,args):
 if vm.knames[k]=='SaveGame':calls.append(args);return 1
 return MusicVM._kernel(vm,k,args)
v._kernel=types.MethodType(kernel,v);h.p['audioSaveResult']=1;before=list(w);ret=h.call('writeSave');h.call('render')
r=dict(scope='exact independent R2 event/ceiling sequence through actual emitted Main; typed kernels, not native',domain_save_ready=ready,save_kernel_entered=len(calls),write_return=ret,save_result=h.p['audioSaveResult'],generation=[v.status(3),v.status(4)],failure=v.status(5),owner=v.status(0),chooser=v.status(7),gameplay_unchanged=list(w)==before,save_reason_visible='SAVE UNAVAILABLE: MUSIC LIFETIME LIMIT.'in v.paint)
assert r['save_kernel_entered']==0 and r['write_return']==0 and r['save_result']==0 and r['save_reason_visible']
(H/'evidence/r3-exhausted-save-probe.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
