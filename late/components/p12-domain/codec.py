"""Strict saved-word transport. Native methods independently validate every ledger."""
from dataclasses import asdict
from pathlib import Path
import json
M=json.loads((Path(__file__).resolve().parent/'manifest.json').read_text())
BASE=32768;CUES=M['cue_ids'];OBJECTS=M['objects'];REVERSE_OBJECTS={v:k for k,v in OBJECTS.items()}
WORDS=M['words'];REVERSE_WORDS={v:k for k,v in WORDS.items()}
STAMPS=[('Revision','revision'),('Handoff','start_at'),('Release','release_at'),('Face','face_at'),('Intro','intro_at'),('Confetti','confetti_at'),('Laugh','laugh_at'),('Collection','collection_at')]
def integer(v,lo,hi,label):
 if type(v) is not int or not lo<=v<=hi:raise ValueError('Invalid '+label)
 return v
def encode_save(data):
 if type(data) is not dict or set(data)!={'kind','schema','state'} or data['kind']!='cakood-p12-branch' or type(data['schema']) is not int or data['schema']!=1:raise ValueError('Invalid envelope')
 s=data['state'];keys={k for _,k in STAMPS}|{'slots','words','presentations'}
 if type(s) is not dict or set(s)!=keys:raise ValueError('Invalid state fields')
 out=dict.fromkeys(M['persisted_properties'],0);out['p12Initialized']=1
 def serial(name,value):
  integer(value,0,M['max_serial'],'serial');out['p12'+name+'Hi'],out['p12'+name+'Lo']=divmod(value,BASE)
 for name,key in STAMPS:serial(name,s[key])
 if type(s['slots']) is not list or len(s['slots']) not in (0,3):raise ValueError('Invalid slots')
 if type(s['words']) is not dict or set(s['words'])!=set(s['slots']):raise ValueError('Invalid cue words')
 for i,obj in enumerate(s['slots']):
  if type(obj) is not str or obj not in CUES:raise ValueError('Invalid cue')
  out['p12Slot'+str(i)]=OBJECTS[obj]
 for obj,word in s['words'].items():
  if type(word) is not str or word not in WORDS:raise ValueError('Invalid word')
  out['p12Word'+str(CUES.index(obj))]=WORDS[word]
 if type(s['presentations']) is not dict or not set(s['presentations'])<=set(M['sources']):raise ValueError('Invalid sources')
 for source,p in s['presentations'].items():
  if type(p) is not dict or set(p)!={'serial','receipts'} or type(p['receipts']) is not dict:raise ValueError('Invalid presentation')
  serial(M['serials'][M['sources'][source]+7],integer(p['serial'],1,M['max_serial'],'source start'))
  bindings=M['receipts'][source]
  if list(p['receipts'])!=[x['token'] for x in bindings[:len(p['receipts'])]]:raise ValueError('Invalid prefix')
  for b in bindings:
   if b['token'] in p['receipts']:serial(M['serials'][b['slot']],integer(p['receipts'][b['token']],1,M['max_serial'],'receipt'))
 return out
def encode_world(world):return encode_save({'kind':'cakood-p12-branch','schema':1,'state':{k:v for k,v in asdict(world).items() if not k.startswith('_')}})
def decode_words(words):
 if type(words) is not list or len(words)!=len(M['persisted_properties']):raise ValueError('Invalid vector')
 for x in words:integer(x,0,32767,'word')
 p=dict(zip(M['persisted_properties'],words))
 if p['p12Initialized']!=1:raise ValueError('Uninitialized')
 def serial(slot):
  name=M['serials'][slot] if type(slot) is int else slot
  return p['p12'+name+'Hi']*BASE+p['p12'+name+'Lo']
 s={key:serial(name) for name,key in STAMPS};s.update(slots=[],words={},presentations={})
 for i in range(3):
  obj=p['p12Slot'+str(i)]
  if obj:
   if REVERSE_OBJECTS.get(obj) not in CUES:raise ValueError('Invalid native cue')
   s['slots'].append(REVERSE_OBJECTS[obj])
 for i,cue in enumerate(CUES):
  word=p['p12Word'+str(i)]
  if word:
   if word not in REVERSE_WORDS:raise ValueError('Invalid native word')
   s['words'][cue]=REVERSE_WORDS[word]
 for source,id in M['sources'].items():
  if serial(id+7):s['presentations'][source]={'serial':serial(id+7),'receipts':{b['token']:serial(b['slot']) for b in M['receipts'][source] if serial(b['slot'])}}
 # No absent source may silently lose an orphan receipt; no sparse slot vector may collapse.
 for source,id in M['sources'].items():
  if not serial(id+7) and any(serial(b['slot']) for b in M['receipts'][source]):raise ValueError('Orphan receipt')
 if s['slots'] and len(s['slots'])!=3:raise ValueError('Sparse rack')
 return {'kind':'cakood-p12-branch','schema':1,'state':s}
