"""Typed parity harness for the numeric SCI ABI, not a gameplay implementation.
Transitions, consistency validation, and admission execute only SCI instructions.
This file translates enums, word frames and literal event payload shapes.
"""
from pathlib import Path
from dataclasses import fields
from itertools import count
import json,sys
H=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(H/'fixtures/reference-baseline'))
from cakood.model import Event,Verb
from cakood.p08_model import P08Context,P08Result,Position,Facing,LAYOUT_OBJECTS,CLOTH_IDS,FLAG_IDS,ONCE_IDS,SOURCE_BINDINGS,EVENING_POSITIONS,READINESS_RECORDS,FIXED_OBJECTS
from source_vm import VM,word
from bytecode_vm import BytecodeVM
M=json.loads((H/'manifest.json').read_text());F=M['state_offsets'];W=M['state_widths'];O=M['output_offsets']
OBJ=M['objects'];RECORD=M['records'];REC={v:k for k,v in RECORD.items()};UNIT={v:k for k,v in M['units'].items()};CODES={v:k for k,v in M['codes'].items()};EVENT={v:k for k,v in M['events'].items()};ROOM=M['rooms'];RROOM={v:k for k,v in ROOM.items()};SESSION=count(1)
SERIALS='revision request_serial pending_request_serial pending_requested_at checklist_receipt confirmed_at completed_request_serial completed_requested_at completed_checklist_receipt completed_confirmation_receipt'.split()
SCALARS={'facing':'facing','service_unpacked':'service_unpacked','returned_padding':'returned_padding','hint_level':'hint_level','pending_phase':'pending_phase'}
GROUPS={'source_serials':('source',tuple(SOURCE_BINDINGS)),'placement_serials':('place',(*LAYOUT_OBJECTS,'pa_facing')),'consumed':('once',('P08_INTRO','P08_UNPACK','P08_EVENING')),'ownership_serials':('owner',('ceramic_carrier','pa_kit','completed_screen','credit_slate','padding')),'acknowledged_handoffs':('ack',('ceramic_carrier','pa_kit','completed_screen','credit_slate','padding')),'unpacked_surface_receipts':('surface',('ceramic_carrier','serving_table'))}
POSITIONFIELDS='carrier_position pa_position screen_position table_position credit_position'.split()
KEYS={'positions',*SCALARS,*SERIALS,*GROUPS,'flags','observed_sources'}
def pair(v):
 if type(v) is not int or not 0<=v<=M['serial_max']:raise ValueError('SCI serial outside unsigned32')
 return word(v>>16),word(v&65535)
def integer(a,b):return ((a&65535)<<16)|(b&65535)
def slot(prefix,k):return F[prefix+'_'+(k.removeprefix('P08_').lower() if prefix=='once' else k)]
def unpack_state(words):
 def serial(n):i=F[n];return integer(words[i],words[i+1])
 state={k:serial(k) for k in SERIALS};state.update(positions={k:words[F[v]] for k,v in zip(LAYOUT_OBJECTS,POSITIONFIELDS)},facing=words[F['facing']],service_unpacked=bool(words[F['service_unpacked']]),returned_padding={0:None,1:'clean_towel',2:'clean_napkin'}[words[F['returned_padding']]],hint_level=words[F['hint_level']],pending_phase=words[F['pending_phase']])
 for name,(prefix,keys) in GROUPS.items():
  d={k:integer(words[slot(prefix,k)],words[slot(prefix,k)+1]) for k in keys}
  if name=='ownership_serials':
   order=[{v:k for k,v in M['ownership_order_keys'].items()}[words[F['owner_order_0']+i]] for i in range(words[F['owner_order_count']])]
   state[name]={k:d[k] for k in order}
  else:state[name]={k:v for k,v in sorted(d.items(),key=lambda x:x[1]) if v}
 state['flags']=[k for k,n in [('LAYOUT_READY','layout_ready'),('EVENING_STARTED','evening_started')] if words[F[n]]]
 state['flags'].sort();state['observed_sources']=sorted(state['source_serials'])
 return state

def encode_save(data):
 if type(data) is not dict or set(data)!={'kind','schema','state'} or data['kind']!='cakood-p08-branch' or type(data['schema']) is not int or data['schema']!=1 or type(data['state']) is not dict or set(data['state'])!=KEYS:raise ValueError('Invalid P08 save envelope')
 s=data['state'];out=[0]*M['state_words']
 def scalar(name,value,allowed,typ=int):
  if type(value) is not typ or value not in allowed:raise ValueError('Invalid scalar '+name)
  out[F[name]]=int(value)
 def serial(name,v):i=F[name];out[i:i+2]=pair(v)
 if type(s['positions']) is not dict or set(s['positions'])!=set(LAYOUT_OBJECTS):raise ValueError('Invalid positions')
 for k,n in zip(LAYOUT_OBJECTS,POSITIONFIELDS):scalar(n,s['positions'][k],range(5))
 scalar('facing',s['facing'],(1,2));scalar('service_unpacked',s['service_unpacked'],(False,True),bool)
 padding=s['returned_padding']
 if padding is not None and (type(padding) is not str or padding not in CLOTH_IDS):raise ValueError('Invalid padding')
 out[F['returned_padding']]={None:0,'clean_towel':1,'clean_napkin':2}[padding]
 scalar('hint_level',s['hint_level'],range(4));scalar('pending_phase',s['pending_phase'],range(4))
 for k in SERIALS:serial(k,s[k])
 for name,(prefix,keys) in GROUPS.items():
  if type(s[name]) is not dict or not set(s[name])<=set(keys):raise ValueError('Invalid ledger '+name)
  for key,v in s[name].items():
   if not v:raise ValueError('Zero receipt is absence')
   serial(prefix+'_'+(key.removeprefix('P08_').lower() if prefix=='once' else key),v)
 for n,allowed in [('flags',FLAG_IDS),('observed_sources',set(SOURCE_BINDINGS))]:
  value=s[n]
  if type(value) is not list or any(type(k) is not str for k in value) or len(value)!=len(set(value)) or not set(value)<=allowed:raise ValueError('Invalid '+n)
 if set(s['observed_sources'])!=set(s['source_serials']):raise ValueError('Source markers/receipts differ')
 out[F['layout_ready']]=int('LAYOUT_READY' in s['flags']);out[F['evening_started']]=int('EVENING_STARTED' in s['flags'])
 out[F['owner_order_count']]=len(s['ownership_serials'])
 for i,key in enumerate(s['ownership_serials']):out[F['owner_order_0']+i]=M['ownership_order_keys'][key]
 return out

def conditions(mask):return {k:bool(mask&(1<<i)) for i,k in enumerate(('buffet_at_hatch','sound_facing_inward','display_concealed','hatch_visible','lane_clear'))}
def handoff(key,serial,padding):
 obj=padding if key=='padding' else key
 return {'handoff_id':'P08:OWN:'+key,'serial':serial,'from_owner':{'ceramic_carrier':'P03','credit_slate':'P03','pa_kit':'P05','completed_screen':'P06','padding':'P03'}[key],'to_owner':'P08','object_id':obj,'includes':('ceramic_service',) if key=='ceramic_carrier' else (), 'destination':'linen_hook' if key=='padding' else 'courtyard_layout','room':'L02_KITCHEN' if key=='padding' else 'L05_COURTYARD'}

def decode_result(out,state):
 code=CODES[out[O['code']]];records=tuple(REC[n] for n in out[O['records']:O['records']+out[O['record_count']]])
 events=[];reverse={v:k for k,v in OBJ.items()}
 for index in range(out[O['event_count']]):
  row=out[O['events']+12*index:O['events']+12*(index+1)]
  kind=EVENT[row[0]];serial=integer(row[1],row[2]);obj=reverse.get(row[3]);choice=row[4];request='P08:START:'+str(integer(row[5],row[6]));old=integer(row[7],row[8]);data={};eid='';etype=''
  if kind=='ownership_handoff':
   key='padding' if obj in CLOTH_IDS else obj;data=handoff(key,old,state['returned_padding']);eid='P08_OWNERSHIP_HANDOFF';etype='ownership_handoff'
  elif kind=='ownership_ack':
   key='padding' if row[3]==22 else obj;data={'handoff_id':'P08:OWN:'+key,'handoff_serial':old};eid='P08_OWNERSHIP_ACK';etype='ownership_ack'
  elif kind=='source_observed':data={'source':obj,'presented_record_id':REC[choice]};eid='P08_OBSERVE';etype='knowledge'
  elif kind=='intro':eid='P08_INTRO';etype='dialogue'
  elif kind=='place':data={'object_id':obj,'position':choice,'conditions':conditions(row[9]),'service_moves_with_carrier':bool(row[10])};eid='P08_PLACE';etype='layout'
  elif kind=='orient':data={'facing':choice,'conditions':conditions(row[9])};eid='P08_ORIENT';etype='layout'
  elif kind=='unpack':data={'service':'ceramic_service','room':'L05_COURTYARD','padding':obj,'return_room':'L02_KITCHEN','return_location':'linen_hook'};eid='P08_UNPACK';etype='object'
  elif kind=='readiness':data={'request_id':request,'required_records':READINESS_RECORDS};eid='P08_READINESS';etype='presentation'
  elif kind=='checklist':data={'request_id':request};eid='P08_CHECKLIST_PRESENTED';etype='presentation'
  elif kind=='declined':data={'request_id':request};eid='P08_START_DECLINED';etype='choice'
  elif kind=='autosave':data={'request_id':request,'before_phase':'E03','must_complete_before_transition':True};eid='P08_AUTOSAVE_REQUEST';etype='autosave_request'
  elif kind=='evening':data={'phase':'E03','request_id':request,'autosave_acknowledged':True,'npc_positions':dict(EVENING_POSITIONS),'essential_access_retained':True};eid='P08_EVENING';etype='phase'
  elif kind=='cancelled':data={'request_id':request};eid='P08_START_CANCELLED';etype='choice'
  elif kind=='hint':data={'level':choice};eid='P08_HINT';etype='hint'
  else:raise ValueError('Unmapped event')
  events.append(Event(eid,etype,{'serial':serial,'puzzle':'P08',**data}))
 # Literal Python result has empty speech_unit_ids; SCI output separately carries
 # exact renderer units. Parity compares that channel to canon independently.
 return P08Result('',tuple(events),code,records)

class SciWorld:
 VMCLASS=VM
 def __init__(self):
  self.vm=self.VMCLASS();self.session=(*pair(next(SESSION)),0,0,0,0,0,1)
  if self.vm.call('p08BindSession',*self.session)!=1:raise RuntimeError('Session binding failed')
 def _state(self):return unpack_state(self.vm.arrays['p08Words'])
 def __getattr__(self,n):
  s=self._state()
  if n in s:return set(s[n]) if n in ('flags','observed_sources') else s[n]
  raise AttributeError(n)
 def _context(self,c):
  if type(c) is not P08Context:raise ValueError('P08 context required')
  mask=sum(v for k,v in M['preparations'].items() if k in c.flags);wins=int('VC01_WON'in c.flags)+2*int('VC02_WON'in c.flags);claims=int('LAYOUT_READY'in c.flags)+2*int('EVENING_STARTED'in c.flags)
  args=(ROOM[c.room],int(c.on_apron),mask,wins,claims,{None:0,'clean_towel':1,'clean_napkin':2}[c.carrier_padding],ROOM[c.frankie_room],ROOM[c.bunny_room],int(c.contest_active),sum(1<<LAYOUT_OBJECTS.index(x) for x in c.protected_objects),int(bool(c.inventory&FIXED_OBJECTS)),int(c.carrier_padding in c.inventory))
  if self.vm.call('p08SetContext',*args)!=1:raise ValueError('SCI invalid context or busy storage')
 def _call(self,name,*args,c=None,obj=None,target=None,callback=False,commit=True):
  if c is not None:
   self._context(c)
   if self.vm.call('p08Inventory',int(obj in c.inventory),int(target in c.inventory))!=1:raise RuntimeError('Inventory query failed')
  if callback:
   if self.vm.call('p08SetCallback',*self.session,*pair(self.revision))!=1:raise RuntimeError('Callback staging failed')
  code=self.vm.call(name,*args)
  if code in (M['codes']['invalid_argument'],M['codes']['invalid_context'],M['codes']['invalid_state']):raise ValueError(CODES[code])
  if self.vm.p['p08Busy']:
   if not commit:return code
   if self.vm.call('p08Commit')!=1:raise RuntimeError('Candidate commit failed')
  return decode_result(self.vm.arrays['p08Output'],self._state())
 def _id(self,obj):
  if type(obj) is not str:raise ValueError('String object required')
  return -2 if obj=="" else OBJ.get(obj,-1)
 def _request(self,request):
  if type(request) is not str:raise ValueError('String request required')
  prefix='P08:START:'
  if request.startswith(prefix):
   try:
    n=int(request[len(prefix):]);parts=pair(n)
    if request==prefix+str(n):return parts
   except ValueError:pass
  return 0,0
 def place(self,c,obj,position,*,pull=False):
  if type(obj) is not str or obj not in LAYOUT_OBJECTS or type(pull)is not bool or type(position) not in (int,Position) or position not in (1,2,3,4):raise ValueError('Invalid placement')
  return self._call('p08Place',OBJ[obj],int(position),int(pull),c=c,obj=obj)
 def orient_pa(self,c,facing):
  if type(facing) not in (int,Facing) or facing not in (1,2):raise ValueError('Invalid facing')
  return self._call('p08Orient',int(facing),c=c,obj='pa_kit')
 def look(self,c,obj):return self._call('p08Look',self._id(obj),c=c,obj=obj)
 def acknowledge_source(self,c,source,record_id):
  if type(source)is not str or source not in SOURCE_BINDINGS or type(record_id)is not str or record_id not in SOURCE_BINDINGS[source]:raise ValueError('Wrong source record')
  return self._call('p08AcknowledgeSource',OBJ[source],RECORD[record_id],c=c,obj=source,callback=True)
 def introduce(self,c):return self._call('p08Introduce',c=c,obj='frankie',target='bunny')
 def unpack_service(self,c):return self._call('p08Unpack',c=c,obj='ceramic_carrier')
 def layout_dialogue(self,c):return self._call('p08LayoutDialogue',c=c,obj='frankie',target='bunny')
 def request_start(self,c):return self._call('p08RequestStart',c=c,obj='frankie')
 def pending_presentation(self,c):return self._call('p08PendingPresentation',c=c,obj='frankie')
 def acknowledge_readiness(self,c,request_id,record_ids):
  if type(record_ids)is not tuple or record_ids!=READINESS_RECORDS:raise ValueError('Exact two readiness records required')
  return self._call('p08AcknowledgeReadiness',*self._request(request_id),*[RECORD[r] for r in record_ids],c=c,obj='frankie',callback=True)
 def confirm_start(self,c,request_id,accepted):
  if type(accepted)is not bool:raise ValueError('Explicit confirmation required')
  return self._call('p08ConfirmStart',*self._request(request_id),int(accepted),c=c,obj='frankie',callback=True)
 def retry_autosave(self,c,request_id):return self._call('p08RetryAutosave',*self._request(request_id),c=c,obj='frankie',callback=True)
 def acknowledge_autosave(self,c,request_id,succeeded):
  if type(succeeded)is not bool:raise ValueError('Explicit verified-I/O ACK required')
  return self._call('p08AcknowledgeAutosave',*self._request(request_id),int(succeeded),c=c,obj='frankie',callback=True)
 def cancel_start(self,c):return self._call('p08CancelStart',c=c)
 def acknowledge_handoff(self,handoff_id,serial):
  if type(handoff_id)is not str or type(serial)is not int:raise ValueError('Exact handoff token required')
  key=handoff_id.removeprefix('P08:OWN:');obj={'ceramic_carrier':1,'pa_kit':2,'completed_screen':3,'credit_slate':5,'padding':22}.get(key,0)
  if handoff_id!='P08:OWN:'+key:obj=0
  if not 0<=serial<=M['serial_max']:obj=0;serial=0
  return self._call('p08AcknowledgeHandoff',obj,*pair(serial),callback=True)
 def hint(self,c,level=None):
  if level is not None and (type(level)is not int or level not in (1,2,3)):raise ValueError('Invalid hint')
  return self._call('p08Hint',level or 0,c=c)
 def act(self,c,verb,obj,target=None):
  verb=Verb(verb);number=list(Verb).index(verb)+1
  return self._call('p08Act',number,self._id(obj),0 if target is None else self._id(target),c=c,obj=obj,target=target)
 def object_location(self,obj,c):
  self._context(c);v=self.vm.call('p08Query',1,self._id(obj),int(obj in c.inventory));return 'kitchen_pass' if v==8 else RROOM.get(v)
 def reachable(self,c,obj):
  self._context(c);return bool(self.vm.call('p08Query',2,self._id(obj),int(obj in c.inventory)))
 @property
 def conditions(self):
  if self.vm.p['p08Busy'] or self.vm.p['p08Uncertain']:raise RuntimeError('Committed query unavailable during publication')
  self.vm.call('p08CopyLive');return conditions(self.vm.call('p08Conditions'))
 @property
 def ready(self):return bool(self.vm.arrays['p08Words'][F['layout_ready']])
 @property
 def evening_started(self):return bool(self.vm.arrays['p08Words'][F['evening_started']])
 @property
 def inventory(self):return ()
 @property
 def pending_request_id(self):return 'P08:START:'+str(self.pending_request_serial) if self.pending_request_serial else None
 @property
 def pending_handoffs(self):
  s=self._state();pending=[];keys={v:k for k,v in M['ownership_order_keys'].items()}
  for i in range(5):
   key=self.vm.call('p08PendingKey',i)
   if not key:break
   name=keys[key];pending.append(handoff(name,s['ownership_serials'][name],s['returned_padding']))
  return tuple(pending)
 @property
 def layout_handoff(self):return {'positions':self.positions,'facing':self.facing,'service_unpacked':self.service_unpacked,'conditions':self.conditions,'returned_padding':self.returned_padding,'padding_room':'L02_KITCHEN','padding_location':'linen_hook','evening_started':self.evening_started}
 def journal_records(self):return tuple(r for s,rs in SOURCE_BINDINGS.items() if s in self.observed_sources for r in rs)
 def validate(self):
  if self.vm.call('p08ValidateCurrent',0):raise ValueError('Invalid current state')
 def validate_context(self,c):
  self._context(c)
  if self.vm.call('p08ValidateCurrent',1):raise ValueError('Invalid current context')
 def save(self):
  self.validate();return {'kind':'cakood-p08-branch','schema':1,'state':self._state()}
 @classmethod
 def load(cls,data,context=None):
  words=encode_save(data);world=cls()
  if context is not None:world._context(context)
  if world.vm.call('p08LoadBegin')!=1:raise ValueError('Load blocked')
  for i,v in enumerate(M['header']+words):
   if world.vm.call('p08LoadWord',i,v)!=1:raise ValueError('Invalid load frame')
  code=world.vm.call('p08LoadFinish',int(context is not None))
  if code!=M['codes']['restored']:raise ValueError('Invalid restored state/context')
  world.session=(*pair(next(SESSION)),0,0,0,0,0,1)
  if world.vm.call('p08BindSession',*world.session)!=1:raise ValueError('Restore rebind failed')
  return world
class SourceWorld(SciWorld):VMCLASS=VM
class EmittedWorld(SciWorld):VMCLASS=BytecodeVM

from fast_vm import FastSource,FastBytecode
class FastSourceWorld(SciWorld):VMCLASS=FastSource
class FastEmittedWorld(SciWorld):VMCLASS=FastBytecode
