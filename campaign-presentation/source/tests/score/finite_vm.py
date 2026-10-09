"""Actual composed bytecode + explicit typed MIDI mock. Never a native receipt."""
from pathlib import Path
import copy,json,sys,os
from collections import Counter
H=Path(__file__).resolve().parents[2]/'authoring/score'
sys.path[:0]=[str(Path(__file__).resolve().parent/'vm'),str(H/'recovered/tools')]
import host_vm as base
base.HERE=H/'recovered'
from host_vm import Object,VMError,EndOfEvents,require,signed
from music_generate import decode_sound
class RestoreTransfer(Exception):
 def __init__(self,vm):self.vm=vm
class FiniteVM(base.HostVM):
 def __init__(self,instructions_per_tick=10000):
  B=Path(os.environ.get('CAKOOD_SCORE_BUILD',str(H.parents[1]/'build/coherent'))).resolve()
  super().__init__(B/'verification-checkpoint',B,budget=300000000)
  self.parsers={};self.max_parsers=0;self.native_trace=[];self.midi=[];self.after_read=None
  self.save_result=1;self.saves=[];self.load_snapshot=None;self.load_calls=0
  self.retiring_events=False;self.snapshots_are_models=True;self.rejoin_measurements=[];self.restore_guards=[];self.fail_next_init=False;self.startup_projection=[];self.serialization_metrics=[]
  self.apis={int(n):v for n,v in json.loads((H/'generated/api.json').read_text()).items()}
  self.instructions_per_tick=instructions_per_tick
  self.symbol_names={}
  for n,api in self.apis.items():
   m=self.modules[n]
   for name,index in api.items():self.symbol_names[n,m.layout['exports'][index]]=name
 def execute(self,obj,m,name,pc,args):
  name=self.symbol_names.get((m.number,pc),name) if hasattr(self,'symbol_names')else name
  track=bool(m.number==943 and name=='rbPoll' and self.arrays(943)['rpRejoin'][0])
  begin_steps=self.steps;begin_time=self.now
  result=super().execute(obj,m,name,pc,args)
  if name in ('psRestoreBegin','psRestoreResume','rbRestoreBegin','rbRestoreResume','rbRestoreReject','rbValidate'):
   self.restore_guards.append(dict(module=m.number,name=name,result=result,now=self.now,owner=self.arrays(943)['rbOwner'][0],mode=self.arrays(943)['rbMode'][0],rp_frozen=self.arrays(943)['rpFrozenPosition'][0],native=[dict(tick=p['tick'],pauses=p['pauses'],status=p['status'])for p in self.parsers.values()]))
  if track and self.arrays(943)['rpRejoin'][0]==0 and self.arrays(943)['rbMode'][0]==4:
   self.rejoin_measurements.append(dict(instructions=self.steps-begin_steps,modeled_ticks=(self.now-begin_time)&65535,resource=self.arrays(943)['rbOwner'][0],native_position=self.arrays(943)['rpPosition'][0]))
  return result
 def proc(self,name,*args):
  n=next(n for n,api in self.apis.items()if name in api)
  m=self.modules[n];index=self.apis[n][name];self.calls[n,name]+=1
  return self.execute(self.objects['cakood'],m,name,m.layout['exports'][index],args)
 def apply_midi(self,obj,ch,msg,origin):
  p=self.parsers[obj];kind=msg[0]&240
  if ch==15:
   if kind==192:p['signal']=msg[1]
   return
  if kind==176:
   p['cc'][ch,msg[1]]=msg[2]
   if msg[1]==120:p['keys']={k:v for k,v in p['keys'].items()if k[0]!=ch}
  elif kind==192:p['programs'][ch]=msg[1]
  elif kind==144 and msg[2]:p['keys'][ch,msg[1]]=msg[2]
  elif kind==128 or(kind==144 and not msg[2]):p['keys'].pop((ch,msg[1]),None)
  self.midi.append((self.now,obj.name,p['tick'],ch,tuple(msg),origin,p['volume']))
 def advance(self,ticks):
  require(ticks>=0,'No backwards mock clock')
  for _ in range(ticks):
   self.now=signed(self.now+1)
   for obj,p in list(self.parsers.items()):
    if not p['playing']or p['pauses']or p['status']!='playing':continue
    tick=p['tick']+1
    if tick>=p['end']:
     if p['loop']:tick=p['start']
     else:tick=p['end'];p['playing']=False;p['status']='stopped';p['signal']=255;obj.p['handle']=0
    p['tick']=tick
    for ch,events in p['streams'].items():
     for t,msg in events:
      if t==tick:self.apply_midi(obj,ch,msg,'native')
 def call(self,obj,name,args=()):
  if name=='eventLoop':self.retiring_events=False
  track_projection=bool(obj.name=='cakood' and name=='p02HostInventory' and obj.p['opening'] and not obj.p['initialized'] and not obj.p['initCount'] and not obj.p['audioReady'])
  if track_projection:
   before_props={o.name:dict(o.p)for o in self.objects.values()}
   before_arrays={n:{name:list(a)for name,a in self.arrays(n).items()}for n in self.modules}
  result=super().call(obj,name,args)
  if track_projection:
   prop_changes={o.name:{key:[before_props[o.name][key],value]for key,value in o.p.items()if before_props[o.name][key]!=value}for o in self.objects.values()}
   prop_changes={k:v for k,v in prop_changes.items()if v}
   array_changes=[]
   for n,m in before_arrays.items():
    after=self.arrays(n)
    for key,values in m.items():
     delta=[[i,a,b]for i,(a,b)in enumerate(zip(values,after[key]))if a!=b]
     if delta:array_changes.append(dict(module=n,array=key,changes=delta))
   self.startup_projection.append(dict(result=result,property_changes=prop_changes,array_changes=array_changes,ui_items_before=before_arrays[0]['uiItems'],ui_items_after=list(self.arrays(0)['uiItems']),initialized=obj.p['initialized'],initCount=obj.p['initCount']))
  if name in ('readSave','h8Recover','p05RetireTransient','h11ReadAbort','musicBeforeChooser','musicAfterChooser','p05RestoreBegin','p05RestoreValidate','p05RestoreReject','hRestoreBegin','hRestoreValidate','h6RestoreBegin','h6RestoreValidate','h7RestoreBegin','h7RestoreValidate','h8RestoreBegin','h8RestoreFinish','h9RestoreCard','h11Load','h12Load','h13Load','h14Load'):
   self.restore_guards.append(dict(module=obj.module.number,name=name,args=[str(x)if isinstance(x,Object)else x for x in args],result=result,now=self.now))
  return result
 def saved_model(self):
  # Capture actual persistent SCI graph only, as typed words/object references.
  # Compiler caches, Python call frames, traces and old runtimes are not a save.
  state=self.snapshot();a=self.arrays(943);d=self.arrays(944);host=self.objects['cakood']
  sounds=[dict(owner=obj.name,number=obj.p['number'],**{k:p[k]for k in ('playing','status','tick','start','end','loop','volume','signal')})for obj,p in self.parsers.items()]
  native=sounds[0]if sounds else {}
  observation=dict(now=self.now,card=host.p['creditCard'],tick=host.p['creditElapsed'],held=host.p['creditHeld'],opening=host.p['opening'],initialized=host.p['initialized'],initCount=host.p['initCount'],uiFailure=host.p['uiFailure'],host_unavailable=host.p['musicUnavailable'],director=[d[k][0]for k in ('psReady','psCue','psRow','psMode','psUnavailable','psRestoring','psChooser')],broker=[a[k][0]for k in ('rbOwner','rbMode','rbDesired','rbGenerationHi','rbGenerationLo','rbUnavailable','rbChooser','rbRestoring')],native_tick=native.get('tick'),native_pauses=self.parsers[next(iter(self.parsers))]['pauses']if self.parsers else None,native_gain=native.get('volume'))
  payload=json.dumps(dict(game=state,sounds=sounds),sort_keys=True,separators=(',',':')).encode()
  import hashlib
  metric=dict(bytes=len(payload),sha256=hashlib.sha256(payload).hexdigest(),local_words=sum(len(x)for x in state['locals'].values()),objects=len(state['objects']),native_entries=len(sounds))
  self.serialization_metrics.append(metric)
  return dict(format='ACTUAL_SAVEGAME_TYPED_KERNEL_MODEL_NOT_NATIVE',game=state,sounds=sounds,observation=observation,calls=dict(self.calls),max_parsers=self.max_parsers,source_clock=self.instructions_per_tick,metrics=list(self.serialization_metrics))
 def restored_model(self,saved):
  require(saved['format']=='ACTUAL_SAVEGAME_TYPED_KERNEL_MODEL_NOT_NATIVE','Typed model format')
  restored=FiniteVM(saved['source_clock'])
  restored.restore(saved['game'])  # Exact compiled-program hashes are checked.
  require(restored.snapshot()==saved['game'],'Every saved gameplay word/object reference must round-trip exactly')
  restored.serialization_metrics=list(saved['metrics'])
  restored.serialization_metrics[-1]['exact_gameplay_roundtrip']=True
  restored.now=self.now;restored.steps=self.steps;restored.calls=Counter(saved['calls'])
  restored.depth=0;restored.chain=[];restored.event_queue=[];restored.retiring_events=True
  restored.max_parsers=saved['max_parsers']
  require(len(saved['sounds'])<=1,'More than one saved native owner')
  for row in saved['sounds']:
   require(row['owner']=='responsiveSound','Untrusted native saved owner')
   obj=restored.objects[row['owner']];require(obj.p['number']==row['number'],'Saved Sound resource mismatch')
   require(row['status']=='paused','A successful chooser snapshot is natively paused')
   p={k:row[k]for k in ('playing','status','tick','start','end','loop','volume','signal')}
   p.update(pauses=0,keys={},cc={},programs={},streams=decode_sound((H/f"assets/{row['number']}.sound.bin").read_bytes()))
   restored.parsers[obj]=p
  return restored
 def _kernel(self,k,args):
  name=self.knames[k]
  if name=='SetCursor':
   require(args in([205,0,0],[1],[0]),'Cursor packet',args);return self._kernel_accumulator
  if name=='GetTime':
   if not args:return self.now
   if args==[2]:
    sec=(self.now&65535)//60;return((sec//3600)<<11)|(((sec//60)%60)<<5)|((sec%60)//2)
   if args==[3]:return (46<<9)|(10<<5)|9
  if name=='GetEvent':
   if self.chain and self.chain[-1]==('cakood','p05RetireTransient') and not self.event_queue:return 0
   if self.retiring_events:return 0
   if self.event_queue==[]:raise EndOfEvents()
   delta=self.frame_tick;self.frame_tick=0
   try:result=super()._kernel(k,args)
   finally:self.frame_tick=delta
   self.advance(delta);return result
  if name=='SaveGame':
   require(args==[0,-1,0],'Save kernel packet',args);self.saves.append(self.saved_model());return self.save_result
  if name=='RestoreGame':
   require(args==[0,-1,0],'Restore kernel packet',args);self.load_calls+=1
   if self.load_snapshot is None:return 0
   restored=self.restored_model(self.load_snapshot)
   self.parsers.clear();raise RestoreTransfer(restored)
  if name!='DoSound':return super()._kernel(k,args)
  require(args,'Sound subop');op=args[0];self.ktrace.append((name,tuple(args)))
  if op in(0,1,2,3,4,5,12,13,15):return 0
  require(op in(6,7,8,9,10,14,16,17,18),'Sound subop',op)
  obj=args[1];require(isinstance(obj,Object),'Sound owner')
  self.native_trace.append((self.now,op,obj.name,obj.p.get('number'),tuple(args[2:])))
  if op==6:
   require(obj.name=='responsiveSound','Legacy or second native owner initialized',obj.name)
   require(obj not in self.parsers,'Init before retirement',obj.name)
   n=obj.p['number'];asset=H/f'assets/{n}.sound.bin';require(asset.exists(),'Unadmitted score asset',n)
   streams=decode_sound(asset.read_bytes());end=max(t for events in streams.values()for t,_ in events)
   loop=n in {r[1]for r in json.loads((H/'generated/FULL-SCORE-CATALOG.json').read_text())['cues']if r[3]==0};start=12 if loop else 0
   self.parsers[obj]=dict(playing=False,status='stopped',pauses=0,tick=0,start=start,end=end,loop=loop,volume=0,signal=0,cc={},programs={},keys={},streams=streams)
   obj.p['nodePtr']=0 if self.fail_next_init else obj
   self.fail_next_init=False;return 0
  if obj not in self.parsers:
   require(op in(7,9,14,16),'Missing parser',op,obj.name)
   return self._kernel_accumulator
  p=self.parsers[obj]
  if op==7:del self.parsers[obj];obj.p.update(handle=0,nodePtr=0)
  elif op==8:
   require(not any(q['playing']for o,q in self.parsers.items()if o!=obj),'Second running parser')
   p['playing']=True;p['status']='playing';obj.p.update(handle=obj,nodePtr=obj)
   for ch,events in p['streams'].items():
    for tick,msg in events:
     if tick==0:self.apply_midi(obj,ch,msg,'native')
  elif op==9:p['playing']=False;p['status']='stopped';p['keys'].clear();obj.p['handle']=0
  elif op==10:
   p['pauses']=p['pauses']+1 if args[2]else max(0,p['pauses']-1)
   if args[2]:p['keys'].clear();p['status']='paused'
   elif p['pauses']==0 and p['status']=='paused':p['status']='playing'
  elif op==14:p['volume']=args[2];obj.p['vol']=args[2]
  elif op==16:require(args[2]==(-1 if p['loop']else 1),'Loop contract')
  elif op==17:
   tick=p['tick'];obj.p.update(min=tick//3600,sec=tick%3600//60,frame=tick%60//2,signal=p['signal'])
   if self.after_read:self.after_read(self,obj)
  elif op==18:
   ch=(args[2]&15)-1 if args[2]&15 else 0
   require(ch in(0,1,2,3,4,5,6,9),'Owner channel',ch)
   msg=bytes([args[3]|ch,args[4],args[5]])if len(args)==6 else bytes([176|ch,args[3],args[4]])
   self.apply_midi(obj,ch,msg,'controller')
  self.max_parsers=max(self.max_parsers,sum(q['playing']for q in self.parsers.values()))
  return 0
 def start(self):
  self.event_queue=[]
  try:self.objects['cakood'].call('play')
  except EndOfEvents:pass
  self.event_queue=None
  return self
