"""Focused controlled mouth cues, actual source/emitted methods, no audio claim."""
from pathlib import Path
import sys,json,hashlib,copy
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'tests'));sys.path.insert(0,str(H/'tools'))
import host,source_host
from source_tools import methods
OUT=H/'evidence/mouth-delta.json';OUT.write_text('{"status":"RUNNING","native_acceptance":false}\n')
rows=[]
for kind in ['source','bytecode']:
 original=host.VM
 try:
  if kind=='source':host.VM=source_host.VM
  h,d,a,p,q,r=host.setup();s=h.vm.objects['p06State']
 finally:host.VM=original
 h.p.update(location=0,roomSeen=0,onApron=0,motionPhase=0)
 r.p.update(hVCEncounter=2,hVCStage=1,hVCWinceActor=0,hVCHitActor=0,hStageKOAge=0)
 for mouth in [0,1,2]:
  a.p.update(lane=1,speaker=1,mouth=mouth);before=h.vm.snapshot();h.vm.ktrace=[]
  assert s.call('h6DrawJack')==1
  draws=[list(args) for name,args in h.vm.ktrace if name=='DrawCel'];assert draws==[[216,1,mouth,145,63,-1,127,127]],draws
  assert h.vm.snapshot()==before
  rows.append(dict(kind=kind,case='real Jackie voice owner cue'+str(mouth),draw=draws[0],state_unchanged=True))
 a.p.update(lane=1,speaker=6,mouth=2);before=h.vm.snapshot();h.vm.ktrace=[];s.call('h6DrawJack')
 draws=[list(args) for name,args in h.vm.ktrace if name=='DrawCel'];assert draws==[[214,1,0,145,63,-1,127,127]],draws;assert h.vm.snapshot()==before
 rows.append(dict(kind=kind,case='Vivian owns PCM; Jackie is idle',state_unchanged=True))
 a.p.update(lane=1,speaker=1,mouth=2);r.p['hVCWinceActor']=1;before=h.vm.snapshot();h.vm.ktrace=[];s.call('h6DrawJack')
 draws=[list(args) for name,args in h.vm.ktrace if name=='DrawCel'];assert draws==[[330,1,0,145,63,-1,127,127]],draws;assert h.vm.snapshot()==before
 rows.append(dict(kind=kind,case='wince takes priority',state_unchanged=True))
 r.p['hVCWinceActor']=0
 for obj,key,value,normal in [(r,'hVCEncounter',1,2),(r,'hVCStage',0,1),(h,'location',1,0),(h,'onApron',1,0)]:
  obj.p[key]=value;before=h.vm.snapshot();h.vm.ktrace=[];assert s.call('h6DrawJack')==0;assert not any(n=='DrawCel' for n,args in h.vm.ktrace);assert h.vm.snapshot()==before;obj.p[key]=normal
  rows.append(dict(kind=kind,case='leave retained drawJack path: '+key,state_unchanged=True))
# Everything except this one render function is exact source, including all105 domain methods.
baseline=H.parent/'revision-2';changes={}
for p in (H/'src').glob('*.sc'):
 a=methods((baseline/'src'/p.name).read_text());b=methods(p.read_text());changed=[n for n in a if a[n]!=b.get(n)]
 if changed:changes[p.name]=changed
assert changes=={'module987.sc':['h6DrawJack']},changes
assert (H/'selectors.json').read_bytes()==(baseline/'selectors.json').read_bytes()
old=json.loads((baseline/'build/coherent/compile-receipt.json').read_text());new=json.loads((H/'build/coherent/compile-receipt.json').read_text())
for row in new['modules']:
 if row['module']!=987:assert row==next(x for x in old['modules'] if x['module']==row['module'])
report=dict(status='PASS',cases=rows,count=len(rows),source_changes=changes,no_state_or_publication_changes=True,other_eight_modules_source_and_emitted_exact=True,selectors_unchanged=True,compile_receipt_sha256=hashlib.sha256((H/'build/coherent/compile-receipt.json').read_bytes()).hexdigest(),native_acceptance=False,listening=False)
OUT.write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(rows),'source/emitted mouth/pose/gate cases; all state unchanged')
