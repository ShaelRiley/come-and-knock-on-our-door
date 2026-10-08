"""Strict saved-word transport, independently revalidated by native methods."""
from dataclasses import asdict
from pathlib import Path
import json
M=json.loads((Path(__file__).resolve().parent/'manifest.json').read_text())
BASE=32768;STAMPS=M['stamps']
def integer(v,lo,hi,label):
 if type(v) is not int or not lo<=v<=hi:raise ValueError('Invalid '+label)
 return v
def encode_save(data):
 if type(data) is not dict or set(data)!={'kind','schema','state'} or data['kind']!='cakood-p13-branch' or type(data['schema']) is not int or data['schema']!=1:raise ValueError('Invalid envelope')
 s=data['state'];keys={k for _,k in STAMPS}|{'attempts','wrong_source','autosaves','presentations'}
 if type(s) is not dict or set(s)!=keys:raise ValueError('Invalid state fields')
 out=dict.fromkeys(M['persisted_properties'],0);out['p13Initialized']=1
 def serial(name,value):
  integer(value,0,M['max_serial'],'serial');out['p13'+name+'Hi'],out['p13'+name+'Lo']=divmod(value,BASE)
 for name,key in STAMPS:serial(name,s[key])
 serial('Attempts',s['attempts'])
 if type(s['wrong_source']) is not str or s['wrong_source'] not in ('','wrong_pot','wrong_people','wrong_display'):raise ValueError('Invalid wrong source')
 out['p13WrongSource']=M['sources'].get(s['wrong_source'],0)
 if type(s['autosaves']) is not dict or not set(s['autosaves'])<=set(M['words']):raise ValueError('Invalid autosaves')
 for cue,value in s['autosaves'].items():serial(cue.title()+'Save',integer(value,1,M['max_serial'],'autosave receipt'))
 if type(s['presentations']) is not dict or not set(s['presentations'])<=set(M['sources']):raise ValueError('Invalid sources')
 for source,p in s['presentations'].items():
  if type(p) is not dict or set(p)!={'serial','receipts'} or type(p['receipts']) is not dict:raise ValueError('Invalid presentation')
  serial(M['serials'][M['sources'][source]+18],integer(p['serial'],1,M['max_serial'],'source start'))
  bindings=M['receipts'][source]
  if list(p['receipts'])!=[x['token'] for x in bindings[:len(p['receipts'])]]:raise ValueError('Invalid prefix')
  for b in bindings:
   if b['token'] in p['receipts']:serial(M['serials'][b['slot']],integer(p['receipts'][b['token']],1,M['max_serial'],'receipt'))
 return out
def encode_world(world):return encode_save({'kind':'cakood-p13-branch','schema':1,'state':{k:v for k,v in asdict(world).items() if not k.startswith('_')}})
def decode_words(words):
 if type(words) is not list or len(words)!=len(M['persisted_properties']):raise ValueError('Invalid vector')
 for x in words:integer(x,0,32767,'word')
 p=dict(zip(M['persisted_properties'],words))
 if p['p13Initialized']!=1:raise ValueError('Uninitialized')
 def serial(slot):
  name=M['serials'][slot] if type(slot) is int else slot
  return p['p13'+name+'Hi']*BASE+p['p13'+name+'Lo']
 rev={v:k for k,v in M['sources'].items()}
 wrong=p['p13WrongSource']
 if wrong not in (0,M['sources']['wrong_pot'],M['sources']['wrong_people'],M['sources']['wrong_display']):raise ValueError('Invalid wrong source')
 s={key:serial(name) for name,key in STAMPS};s.update(attempts=serial('Attempts'),wrong_source=rev[wrong] if wrong else '',autosaves={},presentations={})
 for cue in M['words']:
  value=serial(cue.title()+'Save')
  if value:s['autosaves'][cue]=value
 for source,id in M['sources'].items():
  if serial(id+18):s['presentations'][source]={'serial':serial(id+18),'receipts':{b['token']:serial(b['slot']) for b in M['receipts'][source] if serial(b['slot'])}}
  elif any(serial(b['slot']) for b in M['receipts'][source]):raise ValueError('Orphan receipt')
 return {'kind':'cakood-p13-branch','schema':1,'state':s}
