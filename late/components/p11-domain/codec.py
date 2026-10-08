"""Typed model/native transport; SCI validates chronology and finite receipts independently."""
from dataclasses import asdict
from pathlib import Path
import json
M=json.loads((Path(__file__).resolve().parent/'manifest.json').read_text());BASE=32768

def integer(v,lo,hi,label):
 if type(v) is not int or not lo<=v<=hi:raise ValueError('Invalid '+label)
 return v

def encode_save(data):
 if type(data) is not dict or set(data)!={'kind','schema','state'} or data['kind']!='cakood-p11-branch' or type(data['schema']) is not int or data['schema']!=1:raise ValueError('Invalid envelope')
 s=data['state']
 if type(s) is not dict or set(s)!={'presentations','phase','hint_level',*M['state_serials'].values()}:raise ValueError('Invalid state fields')
 out={k:0 for k in M['persisted_properties']};out.update(p11Initialized=1,p11HintLevel=integer(s['hint_level'],0,32767,'hint word'),p11Phase=integer(s['phase'],0,32767,'phase word'))
 def serial(name,value):
  integer(value,0,M['max_serial'],'serial');out['p11'+name+'Hi'],out['p11'+name+'Lo']=divmod(value,BASE)
 for native,key in M['state_serials'].items():serial(native,s[key])
 if s['phase']==1 and s['revision']==M['max_serial']:raise ValueError('No safety recovery serial headroom')
 if type(s['presentations']) is not dict or not set(s['presentations'])<=set(M['sources']):raise ValueError('Invalid presentation ledger')
 for source,p in s['presentations'].items():
  if type(p) is not dict or set(p)!={'serial','receipts'}:raise ValueError('Invalid presentation fields')
  serial(M['serials'][M['sources'][source]+10],integer(p['serial'],1,M['max_serial'],'start'))
  if type(p['receipts']) is not dict:raise ValueError('Invalid receipts')
  bindings=M['receipts'][source]
  if list(p['receipts'])!=[r['token'] for r in bindings[:len(p['receipts'])]]:raise ValueError('Invalid receipt prefix')
  for b in bindings:
   if b['token'] in p['receipts']:serial(M['serials'][b['slot']],integer(p['receipts'][b['token']],1,M['max_serial'],'receipt'))
 return out

def encode_world(world):
 return encode_save({'kind':'cakood-p11-branch','schema':1,'state':{k:v for k,v in asdict(world).items() if not k.startswith('_')}})

def decode_words(words):
 names=M['persisted_properties']
 if type(words) is not list or len(words)!=len(names):raise ValueError('Invalid vector')
 for v in words:integer(v,0,32767,'saved scalar')
 p=dict(zip(names,words))
 if p['p11Initialized']!=1:raise ValueError('Uninitialized')
 def serial(slot):
  name=M['serials'][slot] if type(slot) is int else slot
  return p['p11'+name+'Hi']*BASE+p['p11'+name+'Lo']
 state={key:serial(native) for native,key in M['state_serials'].items()}
 state.update(presentations={},phase=p['p11Phase'],hint_level=p['p11HintLevel'])
 for source,id in M['sources'].items():
  start=serial(id+10);receipts={b['token']:serial(b['slot']) for b in M['receipts'][source] if serial(b['slot'])}
  if receipts and not start:raise ValueError('Orphan receipt')
  if start:state['presentations'][source]={'serial':start,'receipts':receipts}
 return {'kind':'cakood-p11-branch','schema':1,'state':state}
