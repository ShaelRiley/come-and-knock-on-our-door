#!/usr/bin/env python3
"""Controlled presentation fixtures on combined source/emitted host, no listening claim."""
from pathlib import Path
import sys,json,hashlib
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H/'tests'),str(H/'tools')]
import p06_support
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
binding={'compile_receipt':sha(H/'build/coherent/compile-receipt.json'),'test_source':sha(Path(__file__)),'source':{p.name:sha(p) for p in (H/'src').glob('*.sc')}}
OUT=H/'evidence/combined-mouth-probe.json';rows=[]
def write(status,error=None):OUT.write_text(json.dumps(dict(status=status,binding=binding,cases=rows,count=len(rows),error=error,native_acceptance=False,listening=False),indent=2)+'\n')
write('RUNNING')
try:
 for kind in ['source','bytecode']:
  h,d,a,p,q,r,s,v=p06_support.new(kind)
  h.p.update(location=0,roomSeen=0,onApron=0,motionPhase=0)
  r.p.update(hVCEncounter=2,hVCStage=1,hVCWinceActor=0,hVCHitActor=0,hStageKOAge=0)
  def check(case,wanted,value=1):
   before=h.vm.snapshot();h.vm.ktrace=[];assert s.call('h6DrawJack')==value
   draws=[list(args) for n,args in h.vm.ktrace if n=='DrawCel'];assert draws==wanted,(case,draws)
   assert h.vm.snapshot()==before
   rows.append(dict(kind=kind,case=case,status='PASS',draws=draws,state_unchanged=True));write('RUNNING')
  for mouth in [0,1,2]:
   a.p.update(lane=1,speaker=1,mouth=mouth);check('Jackie current mouth'+str(mouth),[[216,1,mouth,145,63,-1,127,127]])
  a.p.update(lane=1,speaker=6,mouth=2);check('Vivian owns PCM',[[214,1,0,145,63,-1,127,127]])
  a.p.update(lane=1,speaker=1,mouth=2);r.p['hVCWinceActor']=1;check('Wince priority',[[330,1,0,145,63,-1,127,127]])
  r.p['hVCWinceActor']=0
  for obj,key,value,normal in [(r,'hVCEncounter',1,2),(r,'hVCStage',0,1),(h,'location',1,0),(h,'onApron',1,0)]:
   obj.p[key]=value;check('Retained path '+key,[],0);obj.p[key]=normal
 assert len(rows)==18
 assert binding['compile_receipt']==sha(H/'build/coherent/compile-receipt.json')
 write('PASS');print('PASS 18 combined source/emitted presentation fixtures; no listening or native claim')
except BaseException as e:write('FAIL',str(e));raise
