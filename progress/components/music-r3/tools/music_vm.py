"""Emitted SCI runner plus typed sound mock. Not native synthesis or listening."""
from pathlib import Path
import json,re,copy
from host_vm import HostVM,require,Object,signed
from music_generate import decode_sound
H=Path(__file__).resolve().parents[1]
def locals_abi(source):
 source=re.sub(r';[^\n]*','',source);match=re.search(r'\(local\b',source)
 if not match:return []
 pos=match.end();end=source.index(')',pos);text=source[pos:end];tokens=re.findall(r'\[|\]|=|[^\s\[\]=]+',text);i=0;offset=0;out=[]
 while i<len(tokens):
  if tokens[i]=='[':
   name=tokens[i+1];count=int(tokens[i+2]);require(tokens[i+3]==']','Local declaration');i+=4
  else:name=tokens[i];count=1;i+=1
  if i<len(tokens) and tokens[i]=='=':
   i+=1
   if tokens[i]=='[':
    i+=1
    while tokens[i]!=']':i+=1
    i+=1
   else:i+=1
  out.append(dict(name=name,word_offset=offset,word_count=count));offset+=count
 return out

def prepare_checkpoint(build_name="fresh"):
 folder=H/f'build/checkpoints/{build_name}';(folder/'source-provenance').mkdir(parents=True,exist_ok=True);(folder/'reference').mkdir(exist_ok=True);(folder/'assets/resources').mkdir(parents=True,exist_ok=True)
 abi={'selectors':json.loads((H/f'build/{build_name}/selector-list.json').read_text()),'modules':{}}
 if build_name!='fresh':
  input_name='p05'if build_name=='p05-composition'else'p06-frozen'
  abi['modules']=json.loads((H/f'inputs/{input_name}/build/coherent/ABI-MAPPINGS.json').read_text())['modules']
 for number,name in [(0,'main')]+[(n,'module'+str(n))for n in(981,986,940,941,942,943)]:abi['modules'][str(number)]={'locals':locals_abi((H/f'build/{build_name}/src/{name}.sc').read_text())}
 (folder/'source-provenance/ABI-MAPPINGS.json').write_text(json.dumps(abi))
 (folder/'reference/resources.json').write_text(json.dumps([dict(type=3,number=n,extracted_path=f'{n}.text.bin')for n in(243,245,246,247)]+[dict(type=7,number=0,extracted_path='0.font.bin')]))
 (folder/'assets/resources/0.font.bin').write_bytes((H/'inputs/ui/0.font.bin').read_bytes())
 for n in(243,245,246,247):(folder/f'assets/resources/{n}.text.bin').write_bytes((H/('inputs/accepted-v4/generated'if n==243 else 'generated')/f'{n}.text.bin').read_bytes())
 return folder
class MusicVM(HostVM):
 def __init__(self,build_name='fresh'):
  super().__init__(prepare_checkpoint(build_name),H/f'build/{build_name}',budget=100000000)
  self.apis={int(k):v for k,v in json.loads((H/'generated/api.json').read_text()).items()};self.apis[940]=json.loads((H/'inputs/accepted-v4/generated/api.json').read_text())['exports'];self.parsers={};self.midi=[];self.max_parsers=0;self.kernel_time_cost=0;self.after_read=None;self.sound_trace=[]
  self.proc_arity={}
  for module,api in self.apis.items():
   source=(H/f'build/{build_name}/src/module{module}.sc').read_text()
   for sig in re.findall(r'\(procedure \(([^)]*)\)',source):
    t=sig.split();self.proc_arity[module,t[0]]=len(t[1:t.index('&tmp')]) if '&tmp' in t else len(t)-1
 def call(self,obj,name,args=()):
  if obj.name in ('musicTransport','contestTransport','homeReadyTransport','contestReadyTransport'):
   api={r['name']:r['parameter_count'] for r in json.loads((H/'inputs/original981/api.json').read_text())}
   if name in api:require(len(args)==api[name],'Transport method arity',name,len(args),api[name])
  return super().call(obj,name,args)
 def procedure(self,module,index,args=()):
  require(module in self.apis,'Only registered music procedures');names={v:k for k,v in self.apis[module].items()};require(index in names,'Export procedure index',module,index)
  name=names[index];require(len(args)==self.proc_arity[module,name],'Procedure arity',name,len(args),self.proc_arity[module,name]);m=self.modules[module]
  self.calls[module,name]+=1
  return self.execute(self.objects['homeReadyTransport'],m,name,m.layout['exports'][index],args)
 def proc(self,name,*args):
  module=next(n for n,api in self.apis.items()if name in api)
  return self.procedure(module,self.apis[module][name],args)
 def status(self,n):return self.proc('rbStatus',n)
 def poll(self):return self.proc('rbPoll',self.status(3),self.status(4),self.objects['contestState'])
 def move_to(self,pos):
  obj=self.objects['responsiveSound'];p=self.parsers[obj];require(p['start']<=pos<p['end'],'Fixture position')
  if pos<p['tick']:self.advance(p['end']-p['tick']+pos-p['start'])
  else:self.advance(pos-p['tick'])
 def domain_words(self):return self.arrays(986)['vcWords']
 def advance(self,ticks):
  require(ticks>=0,'Clock cannot rewind')
  for _ in range(ticks):
   self.now=signed(self.now+1)
   for obj,p in self.parsers.items():
    if not p['playing'] or p['pauses']:continue
    new=p['tick']+1
    if new>=p['end']:
     if p['loop']:new=p['start'];p['wrapped']=True
     else:new=p['end'];p['playing']=False;p['signal']=255
    p['tick']=new
    for ch,es in p['streams'].items():
     for t,msg in es:
      if t==new:self.apply(obj,ch,msg,'native')
 def apply(self,obj,ch,msg,origin):
  p=self.parsers[obj];kind=msg[0]&240
  if ch==15:
   if kind==192:p['signal']=msg[1]
   return
  if kind==176:
   p['cc'][ch,msg[1]]=msg[2]
   if msg[1]==120:p['keys']={k:v for k,v in p['keys'].items() if k[0]!=ch}
  elif kind==192:p['programs'][ch]=msg[1]
  elif kind==144 and msg[2]:p['keys'][ch,msg[1]]=msg[2]
  elif kind==128 or (kind==144 and not msg[2]):p['keys'].pop((ch,msg[1]),None)
  self.midi.append((self.now,obj.name,p['tick'],ch,tuple(msg),origin,p['volume']))
 def _kernel(self,k,args):
  name=self.knames[k]
  if name=='GetTime':
   require(len(args) in (0,1),'GetTime arity')
   if not args:return self.now
   # Civil bins mirror a fixed date plus elapsed wall seconds.
   sec=(self.now&65535)//60
   if args==[2]:return ((sec//3600)<<11)|(((sec//60)%60)<<5)|((sec%60)//2)
   if args==[3]:return (46<<9)|(10<<5)|6
   raise RuntimeError('Unsupported GetTime mode')
  if name!='DoSound':return super()._kernel(k,args)
  self.ktrace.append((name,tuple(args)));require(args,'DoSound subop');op=args[0]
  require(op in (6,7,8,9,10,14,16,17,18),'Unapproved music kernel',op)
  require(len(args) in ({6:[2],7:[2],8:[3],9:[2],10:[3],14:[3],16:[3],17:[2],18:[5,6]}[op]),'DoSound arity',args)
  obj=args[1];require(isinstance(obj,Object),'Sound object')
  if op==6:
   number=obj.p['number'];require(number in (102,140,148,149,150,151,152,153,154),'Unapproved score parser',number);require(obj not in self.parsers,'Init without dispose')
   folder=H/('inputs/bridge-reference/generated'if number>=148 else 'inputs/music/analysis')
   manifest=next(json.loads(f.read_text())for f in folder.glob('*-manifest.json')if json.loads(f.read_text())['resource_id']==number)
   loop=manifest['loop'];native=H/(f'inputs/bridge-reference/generated/{number}.sound.bin'if number>=148 else f'inputs/music/native/{number}.sound.bin')
   self.parsers[obj]=dict(playing=False,pauses=0,tick=0,start=loop['start_tick']if loop else 0,end=loop['end_tick']if loop else manifest['end_tick'],loop=bool(loop),wrapped=False,volume=0,signal=0,cc={},programs={},keys={},streams=decode_sound(native.read_bytes()))

  else:
   require(obj in self.parsers,'Sound slot missing',obj,op);p=self.parsers[obj]
   if op==7:del self.parsers[obj]
   elif op==8:
    require(not p['playing'],'Duplicate parser play');require(not any(q['playing'] for o,q in self.parsers.items() if o!=obj),'Concurrent full-score parsers')
    p['playing']=True
    for ch,es in p['streams'].items():
     for t,msg in es:
      if t==0:self.apply(obj,ch,msg,'native')
   elif op==9:p['playing']=False;p['keys'].clear()
   elif op==10:p['pauses']=p['pauses']+1 if args[2] else max(0,p['pauses']-1)
   elif op==14:require(0<=args[2]<=127,'Whole Sound volume');p['volume']=args[2];obj.p['vol']=args[2]
   elif op==16:require(args[2]==(-1 if p['loop']else 1),'Looping/one-shot mismatch')
   elif op==17:
    t=p['tick'];obj.p.update(min=t//3600,sec=t%3600//60,frame=t%60//2,signal=p['signal'])
    if self.after_read:self.after_read(self,obj)
   elif op==18:
    channel=args[2]&15;channel=channel-1 if channel else 0
    require(channel in (0,1,2,3,4,5,6,9),'Reserved channel misuse',channel)
    if len(args)==5:msg=bytes([0xb0|channel,args[3],args[4]])
    else:msg=bytes([args[3]|channel,args[4],args[5]])
    self.apply(obj,channel,msg,'controller')
  self.sound_trace.append((self.now,op,obj.name,obj.p['number'],tuple(args[2:])))
  self.max_parsers=max(self.max_parsers,sum(p['playing'] for p in self.parsers.values()))
  if self.kernel_time_cost:self.advance(self.kernel_time_cost)
  return 0
