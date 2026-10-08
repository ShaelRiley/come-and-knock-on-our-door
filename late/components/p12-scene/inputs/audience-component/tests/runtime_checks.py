"""Bounded controller execution. Native kernels are explicit deterministic mocks.

Scene page properties are supplied as an isolated fixture, not integrated route
or pixel proof. All acceptance/cancel/mute methods execute unchanged source and
copied emitted bytecode. Sync mocks consume the actual generated Sync payloads.
"""
from pathlib import Path
import json
import struct
import sys
H=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(H/'runtime/tests'))
sys.path.insert(0,str(H/'runtime/tools'))
import scene_vm
import host_vm
host_vm.HERE=H/'runtime/tools'

def require(ok, why):
    if not ok:raise AssertionError(why)

def pairs(data):
    require(data[:2]==b'\x8e\x00' and data[-2:]==b'\xff\xff','Sync framing')
    return list(struct.iter_unpack('<hh',data[2:-2]))

class SyncStream:
    def __init__(self):self.current=[];self.index=0
    def step(self,args):
        op=args[0]
        if op==0:
            name='@'+base36(args[2],3)+base36(args[3],2)+base36(args[4],2)+'.'+base36(args[5],2)+base36(args[6],1)
            self.current=pairs((H/'generated/speech'/('#'+name[1:])).read_bytes());self.index=0
        elif op==1:
            time,cue=self.current[self.index] if self.index<len(self.current) else (-1,-1)
            self.index+=1;args[1].p.update(syncTime=time,syncCue=cue)
        elif op==2:self.current=[];self.index=0
        else:raise AssertionError('Unexpected DoSync operation')
        return 0

def base36(n,width):
    value=''
    while n:value='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[n%36]+value;n//=36
    return (value or '0').rjust(width,'0')

class SourceVM(scene_vm.VM):
    def __init__(self,*args):super().__init__(*args);self.stream=SyncStream()
    def ev(self,n,e):
        if isinstance(n,list) and n and n[0]=='DoSync':
            args=[self.ev(x,e) for x in n[1:]];self.kernel.append(('DoSync',args));return self.stream.step(args)
        return super().ev(n,e)

class EmittedVM(host_vm.HostVM):
    def __init__(self):
        self.stream=SyncStream()
        super().__init__(checkpoint=H/'runtime/verification-checkpoint',build=H/'runtime',budget=4000000)
    def _kernel(self,k,args):
        if self.knames.get(k)=='DoSync':
            self.ktrace.append(('DoSync',tuple(args)));return self.stream.step(args)
        return super()._kernel(k,args)

class Adapter:
    def __init__(self,kind):
        self.kind=kind
        if kind=='source':
            self.a=SourceVM(H/'runtime/src/module980.sc','PresentationAudio')
            self.d=SourceVM(H/'runtime/src/module982.sc','SceneDialogue')
            self.vm=None
        else:
            self.vm=EmittedVM();self.a=self.vm.objects['presentationAudio'];self.d=self.vm.objects['sceneDialogue']
    def position(self,tick):
        if self.vm:self.vm.audio_position=tick
        else:self.a.audio_position=tick
    def starts(self):
        trace=self.vm.ktrace if self.vm else self.a.kernel
        return [list(args) for op,args in trace if op=='DoAudio' and args[0]==2]
    def calla(self,name,*args):return self.a.call(name,*args)
    def calld(self,name,*args):return self.d.call(name,*args)
    def prepare(self,row):
        self.calla('cancel',13)
        self.d.p.update(sdActive=1,sdFailure=0,sdVoice=row['voice_index'],sdSpeaker=0,sdAudioModule=924,
                        sdVoiceEnd=row['duration_ticks'],sdPage=0,sdGeneration=10,sdPaintGeneration=-1,
                        sdPendingStart=1,sdArmed=0,sdExpectedAudioToken=-1)
    def accept(self,row):
        self.prepare(row)
        require(self.calld('sdPresented',10,0,self.a.p['token'])==0,'Pre-paint acceptance')
        self.d.p['sdPaintGeneration']=10
        require(self.calld('sdPresented',9,0,self.a.p['token'])==0,'Stale generation accepted')
        require(self.calld('sdPresented',10,1,self.a.p['token'])==0,'Stale page accepted')
        require(self.calld('sdPresented',10,0,self.a.p['token'])==1,'Speaker zero was not armed')
        require(self.calld('sdPresented',10,0,self.a.p['token'])==0,'Duplicate paint accepted')
        require(self.calld('sdSpeak',self.a,10,1)==0,'Wrong page started')
        token=self.calld('sdSpeak',self.a,10,0)
        require(token==self.a.p['token'] and self.a.p['lane']==1,'Group not on speech lane')
        require(self.a.p['speaker']==0 and self.a.p['mouth']==0,'Group remapped or animated')
        require(self.calld('sdSpeak',self.a,10,0)==0,'Duplicate start')
        return token

def run():
    m=json.loads((H/'generated/manifest.json').read_text());results=[]
    for kind in ['source','emitted']:
        v=Adapter(kind);checks=0
        for row in m['speech']:
            duration=row['duration_ticks']
            for muted in [0,1]:
                v.a.p.update(voiceMuted=muted,voiceVolume=80,masterVolume=100)
                token=v.accept(row)
                require(v.starts()[-1]==[2,911 if muted else 924,1 if muted else row['voice_index'],1,0,1],'Incorrect Audio36 or silent911 tuple')
                for tick in [0,1,3,duration//2,duration-1]:
                    v.position(tick);require(v.calla('poll',tick,token)==1,'Early lane completion')
                    require(v.a.p['mouth']==0 and v.a.p['speaker']==0,'Principal mouth activated')
                v.position(duration if muted else -1)
                require(v.calla('poll',duration,token)==0,'Exact duration did not finish')
                require(v.a.p['mouth']==0 and v.a.p['silentClock']==0,'End cleanup')
                checks+=1
            # Mute after 19 ticks must preserve elapsed offset and exact end.
            v.a.p.update(voiceMuted=0,voiceVolume=80,masterVolume=100)
            token=v.accept(row);v.position(19);v.calla('setOff',1,1)
            require(v.a.p['silentClock']==1 and v.a.p['voiceOffset']==19,'Mid-line mute lost position')
            require(v.starts()[-1]==[2,911,1,1,0,1],'Mid-line mute not silent clock')
            v.calla('setOff',1,0)
            require(v.a.p['silentClock']==1 and v.a.p['lastGain']==0,'Unmute exposes latent audio')
            v.position(duration-20);require(v.calla('poll',duration-1,token)==1,'Muted offset early end')
            v.position(duration-19);require(v.calla('poll',duration,token)==0,'Muted offset late end')
            # Audience control remains laughter-only; this canonical dialogue is voice.
            v.a.p.update(voiceMuted=0,audienceMuted=1)
            token=v.accept(row)
            require(v.starts()[-1][1]==924,'Audience mute wrongly silenced canonical speech')
            require(v.calla('queueLaugh',77,1,900,1,1,0,1,0,token)==0,'Muted laughter accepted')
            v.a.p['audienceMuted']=0
            require(v.calla('queueLaugh',78,1,900,1,1,0,1,0,token)==1,'Current laughter queue rejected')
            v.position(duration//2);v.calla('poll',duration//2,token)
            require(v.a.p['lane']==1,'Laughter overlapped speech')
            v.calld('sdInterrupt',v.a,11)
            require(v.a.p['lane']==0 and v.a.p['pendingLaugh']==0 and v.a.p['mouth']==0,'Cancel cleanup')
            require(v.calla('poll',duration,token)==0 and v.a.p['lane']==0,'Stale callback resurrected audio')
            # Every scene barrier supported by sdInterrupt cancels and invalidates.
            for reason in [10,11,12,13,14]:
                token=v.accept(row);v.calld('sdInterrupt',v.a,reason)
                require(v.a.p['token']!=token and v.a.p['lane']==0 and v.d.p['sdArmed']==0,'Scene boundary cancel failed')
            # Stale owner token must be rejected even after valid presentation.
            v.prepare(row);v.d.p['sdPaintGeneration']=10
            v.calld('sdPresented',10,0,v.a.p['token']);v.calla('cancel',15)
            require(v.calld('sdSpeak',v.a,10,0)==0,'Stale owner token accepted')
            # Zero master and zero Voice volume use silent911 even if not muted.
            for voice,master in [(0,100),(80,0)]:
                v.a.p.update(voiceMuted=0,voiceVolume=voice,masterVolume=master)
                v.accept(row);require(v.starts()[-1]==[2,911,1,1,0,1],'Zero gain used audible resource')
            checks+=10
        results.append(dict(mode=kind,scenario_groups=checks,fragments=len(m['speech']),
                            emitted_instructions=v.vm.steps if v.vm else None,
                            scope='Isolated actual controller methods; manually supplied page properties and mock PCM clock/Sync. No route/native/listening/graphics acceptance.'))
    return dict(status='PASS',runs=results,no_runtime_sources_modified=True,no_native_launch=True,
                safety='No source/domain/world object is loaded or updated. No observation credit APIs are invoked.')
