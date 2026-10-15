#!/usr/bin/env python3
"""Explicit full-ledger/Fold fixture; not native campaign acceptance."""
from pathlib import Path
import json
from p11_payoff_fixture import Probe, SOURCE

class RouteProbe(Probe):
    def __init__(self, build=None):
        super().__init__(build)
        self.budget=30000000
        self.h.p.update(roomSeen=3,apronSeen=0,motionX=self.call(self.h,'approachX',(415,))*64, motionY=self.call(self.h,'approachY',(415,))*64, uiVerb=5)
        self.instance(990).p.update(p09RumorCleared=1,p09Ready=1)
        self.h.p['p04']=self.instance(984)
        self.call(self.instance(984),'p04Init')
        p=self.instance(993)
        owners=self.arrays(993)['h11Owners']
        for i,room in enumerate((0,4,3,3,3)):
            owners[12*i]=1;owners[12*i+1]=room
        # Actual domain initialized/advanced through its public operations below.
        for key in p.p:
            if key.startswith('p11'):
                p.p[key]=0
        assert self.call(p,'p11Init')==1
        assert self.call(p,'p11Context',(3,0,1,1,1,1,3,0,4,3,3,3,0,0,0,1,1,1,1,0,1))==1
        assert self.call(p,'p11Lift')==15
        for source in (2,3,4,5,6):
            self.call(p,'p11Begin',(source,))
            hi=self.call(p,'p11SerialHi',(source+10,));lo=self.call(p,'p11SerialLo',(source+10,))
            self.call(p,'p11Acknowledge',(source,hi,lo,p.p['p11Epoch'],self.call(p,'p11SourceRecord',(source,)),0,0))
            assert self.call(p,'p11Complete',(source,))==1,(source,p.p['p11Code'])
        assert self.call(p,'p11ReleaseCatch')==29
        assert self.call(p,'p11PullHandle')==32
        assert self.call(p,'p11Validate')==1
        assert self.call(p,'h11PayEvent',(8,))==1
        self.call(p,'p11Begin',(7,))
        assert self.call(p,'h11Open',(7,))==1
        self.event_calls=[]
        self.track_route=True

    def call(self,obj,name,args=()):
        key=(obj.module.number,name)
        if key in {(989,'h8EveningReady'),(989,'h8EveningCommitted'),(992,'p10Ready')}:return 1
        if key == (989,'h8ActorRoom'):
            return {2:0,3:4,7:3,8:3}.get(args[0],0)
        if getattr(self,'track_route',False) and name in {'uiInput','uiActivate','uiChooseObject','uiHostAct','speechCancel','sdInterrupt','h11PayInterrupt','h11PayDrop','motionRequest','h11PayMove','h11Menu','h11PayMenu','h11PayMenuDone','h11Retire','h11PayRetire','motionCancel','motionArrive','h11Dispatch','h11Ctx','p11Context','h11PayGuard','p11ClaimLaugh','h11PayEvent','h11Choice','uiHostChoice'}:
            self.event_calls.append({'module':obj.module.number,'method':name,'args':[str(a) for a in args],
                                     'mode_before':self.arrays(993)['h11Pay'][0]})
        return super().call(obj,name,args)

    def note(self,label):
        p=self.instance(993);pay=self.arrays(993)['h11Pay'];d=self.h.p['dialogue']
        return {'label':label,'mode':pay[0],'pose':pay[1],'painted_pose':pay[14],
                'heard':pay[20],'reader_complete':self.arrays(993)['h11Reader'][15],
                'actual_domain_fold_complete':self.call(p,'p11Complete',(7,)),
                'actual_domain_valid':self.call(p,'p11Validate'),
                'page':d.p['sdPage'],'panel':self.h.p['uiPanel'],'token':self.a.p['token'],
                'pending':d.p['sdPendingStart'],'suppressed':d.p['sdSuppressed']}

def prepare_closed(build=None):
    v=RouteProbe(build);p=v.instance(993);d=v.h.p['dialogue'];snap=[]
    for page in range(4):
        v.call(v.h,'render');v.call(v.h,'dialoguePresented')
        assert d.p['sdPendingStart']==0 and d.p['sdAudioToken']==v.a.p['token'],(page,d.p)
        for step in range(10 if page==0 else 0):
            v.now+=6;v.call(v.h,'render')
        v.audio_position=-1
        v.call(v.a,'poll',(v.now,v.a.p['token']))
        v.call(v.h,'render')
        snap.append(v.note(f'page{page+1} natural EOF'))
        if page<3:v.call(v.h,'uiTurnPage',(1,))
    assert snap[-1]['heard']==4 and snap[-1]['painted_pose']==6
    assert snap[-1]['actual_domain_fold_complete']==1 and snap[-1]['reader_complete']==1
    v.call(v.h,'uiClose')
    snap.append(v.note('actual ordinary Close'))
    assert snap[-1]['mode']==2,snap[-1]
    v.event_calls=[]
    return v,snap
