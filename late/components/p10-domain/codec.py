"""Strict typed save transport. SCI independently validates the domain and receipt ledger."""
from dataclasses import asdict
from pathlib import Path
import json
M=json.loads((Path(__file__).resolve().parent/'manifest.json').read_text())
BASE=32768
WORDS={None:0,**M['words']};REVERSE_WORDS={v:k for k,v in WORDS.items()}
CUES=M['cue_ids'];OBJECTS=M['objects'];REVERSE_OBJECTS={v:k for k,v in OBJECTS.items()}

def integer(v,lo,hi,label):
 if type(v) is not int or not lo<=v<=hi:raise ValueError('Invalid '+label)
 return v

def encode_save(data):
 if type(data) is not dict or set(data)!={'kind','schema','state'} or data['kind']!='cakood-p10-branch' or type(data['schema']) is not int or data['schema']!=1:raise ValueError('Invalid envelope')
 s=data['state']
 if type(s) is not dict or set(s)!={'presentations','revision','bread_at','paper_at','restored_at','labels','slots','hint_level'}:raise ValueError('Invalid state fields')
 out={k:0 for k in M['persisted_properties']};out.update(p10Initialized=1,p10HintLevel=integer(s['hint_level'],0,32767,'hint word'))
 def serial(name,value):
  integer(value,0,M['max_serial'],'serial');out['p10'+name+'Hi'],out['p10'+name+'Lo']=divmod(value,BASE)
 for native,key in [('Revision','revision'),('Bread','bread_at'),('Paper','paper_at'),('Restored','restored_at')]:serial(native,s[key])
 if type(s['labels']) is not dict or set(s['labels'])!=set(CUES):raise ValueError('Invalid label registry')
 for i,obj in enumerate(CUES):
  value=s['labels'][obj]
  if value is not None and (type(value) is not str or value not in M['words']):raise ValueError('Invalid cue word')
  out['p10Label'+str(i)]=WORDS[value]
 if type(s['slots']) is not list or len(s['slots'])!=3:raise ValueError('Invalid slots')
 for i,obj in enumerate(s['slots']):
  if obj is not None and (type(obj) is not str or obj not in CUES):raise ValueError('Invalid cue object')
  out['p10Slot'+str(i)]=OBJECTS[obj] if obj else 0
 if type(s['presentations']) is not dict or not set(s['presentations'])<=set(M['sources']):raise ValueError('Invalid presentation ledger')
 for source,p in s['presentations'].items():
  if type(p) is not dict or set(p)!={'serial','receipts'}:raise ValueError('Invalid presentation fields')
  serial(M['serials'][M['sources'][source]+3],integer(p['serial'],1,M['max_serial'],'start'))
  if type(p['receipts']) is not dict:raise ValueError('Invalid receipts')
  bindings=M['receipts'][source]
  if list(p['receipts'])!=[r['token'] for r in bindings[:len(p['receipts'])]]:raise ValueError('Invalid receipt prefix')
  for b in bindings:
   if b['token'] in p['receipts']:serial(M['serials'][b['slot']],integer(p['receipts'][b['token']],1,M['max_serial'],'receipt'))
 return out

def encode_world(world):
 s={k:v for k,v in asdict(world).items() if not k.startswith('_')}
 return encode_save({'kind':'cakood-p10-branch','schema':1,'state':s})

def decode_words(words):
 names=M['persisted_properties']
 if type(words) is not list or len(words)!=len(names):raise ValueError('Invalid vector')
 for v in words:integer(v,0,32767,'saved scalar')
 p=dict(zip(names,words))
 if p['p10Initialized']!=1:raise ValueError('Uninitialized')
 def serial(slot):
  name=M['serials'][slot] if type(slot) is int else slot
  return p['p10'+name+'Hi']*BASE+p['p10'+name+'Lo']
 labels={}
 for i,obj in enumerate(CUES):
  value=p['p10Label'+str(i)]
  if value not in REVERSE_WORDS:raise ValueError('Invalid native label')
  labels[obj]=REVERSE_WORDS[value]
 slots=[]
 for i in range(3):
  value=p['p10Slot'+str(i)]
  if value and REVERSE_OBJECTS.get(value) not in CUES:raise ValueError('Invalid native rack object')
  slots.append(REVERSE_OBJECTS[value] if value else None)
 state=dict(presentations={},revision=serial(0),bread_at=serial(1),paper_at=serial(2),restored_at=serial(3),labels=labels,slots=slots,hint_level=p['p10HintLevel'])
 for source,id in M['sources'].items():
  if serial(id+3):state['presentations'][source]={'serial':serial(id+3),'receipts':{b['token']:serial(b['slot']) for b in M['receipts'][source] if serial(b['slot'])}}
 return {'kind':'cakood-p10-branch','schema':1,'state':state}
