"""Strict finite P14 save/context transport and detached by-value replay envelope.

Native SCI independently validates every branch word; this file never supplies a
successful transition or substitutes a model transition for emitted bytecode.
"""
from pathlib import Path
from dataclasses import asdict
import copy,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from cakood.p14_model import P14World,P14Context,PEOPLE,CONTEST_IDS
M=json.loads((HERE/'manifest.json').read_text());BASE=32768
STAMPS=[('Revision','revision'),('Start','start_at'),('Signature','signature_at'),('Pencil','pencil_at'),('Complete','complete_at'),('Finale','finale_started_at'),('Frame','frame_at'),('Celebration','celebration_at'),('Laugh','laugh_at')]
def integer(v,lo,hi,label):
 if type(v) is not int or not lo<=v<=hi:raise ValueError('Invalid '+label)
 return v
def ordinal(identity,contest):
 if type(identity) is not str or not identity.startswith(contest+':A') or not identity.endswith(':KO'):raise ValueError('Invalid outcome identity')
 value=identity[len(contest)+2:-3]
 if not value.isascii() or not value.isdigit() or value.startswith('0'):raise ValueError('Outcome must use the actual canonical positive ordinal')
 return integer(int(value),1,M['max_serial'],'outcome ordinal')
def encode_save(data):
 # Read exact fields/types/prefix order before finite conversion loses JSON form.
 w=P14World.load(data);s=data['state']
 out=dict.fromkeys(M['persisted_properties'],0);out['p14Initialized']=1
 def serial(name,value):
  integer(value,0,M['max_serial'],'serial');out['p14'+name+'Hi'],out['p14'+name+'Lo']=divmod(value,BASE)
 for name,key in STAMPS:serial(name,s[key])
 for p,value in s['pinned'].items():serial('Pin'+p.title(),value)
 if s['entry_flags']:out['p14EntryHi']=8191;out['p14EntryLo']=32767
 for i,c in enumerate(CONTEST_IDS):
  if c in s['winning_attempts']:out[f'p14Win{i}Hi'],out[f'p14Win{i}Lo']=divmod(ordinal(s['winning_attempts'][c],c),BASE)
 out['p14DateLength']=len(s['repair_date'])
 for i,c in enumerate(s['repair_date']):out[f'p14Date{i}Hi'],out[f'p14Date{i}Lo']=divmod(ord(c),BASE)
 out['p14Tone']=M['tones'].index(s['vivian_tone']);out['p14Phase']=M['phases'].index(s['finale_phase'])
 for field,key in [('Paused','finale_paused'),('Skipped','finale_skipped'),('Replay','replay_mode')]:out['p14'+field]=int(s[key])
 out['p14CreditCount']=len(s['credit_ids']);out['p14CreditCursor']=s['credit_cursor']
 for i,record in enumerate(s['credit_ids']):out['p14Credit'+str(i)]=M['sources']['credit:'+record]
 for source,p in s['presentations'].items():
  serial(M['serials'][M['sources'][source]+16],p['serial'])
  for b in M['receipts'][source]:
   if b['token'] in p['receipts']:serial(M['serials'][b['slot']],p['receipts'][b['token']])
 return out
def encode_world(world):return encode_save({'kind':'cakood-p14-branch','schema':1,'state':{k:v for k,v in asdict(world).items() if not k.startswith('_')}})
def decode_words(words):
 if type(words) is not list or len(words)!=len(M['persisted_properties']):raise ValueError('Invalid vector')
 for value in words:integer(value,0,32767,'word')
 p=dict(zip(M['persisted_properties'],words))
 if p['p14Initialized']!=1:raise ValueError('Uninitialized')
 def serial(slot):
  name=M['serials'][slot] if type(slot) is int else slot
  return p['p14'+name+'Hi']*BASE+p['p14'+name+'Lo']
 s={key:serial(name) for name,key in STAMPS};s.update(entry_flags=[],winning_attempts={},pinned={},presentations={})
 if (p['p14EntryHi'],p['p14EntryLo'])==(8191,32767):s['entry_flags']=M['prerequisites'].copy()
 elif p['p14EntryHi'] or p['p14EntryLo']:raise ValueError('Invalid task ledger')
 for i,c in enumerate(CONTEST_IDS):
  value=p[f'p14Win{i}Hi']*BASE+p[f'p14Win{i}Lo']
  if value:s['winning_attempts'][c]=f'{c}:A{value}:KO'
 for person in PEOPLE:
  value=serial('Pin'+person.title())
  if value:s['pinned'][person]=value
 n=integer(p['p14DateLength'],0,80,'date length');chars=[]
 for i in range(80):
  value=p[f'p14Date{i}Hi']*BASE+p[f'p14Date{i}Lo']
  if i<n:chars.append(chr(integer(value,32,0x10ffff,'date scalar')))
  elif value:raise ValueError('Date outside declared length')
 s['repair_date']=''.join(chars)
 s['vivian_tone']=M['tones'][integer(p['p14Tone'],0,2,'tone')]
 s['finale_phase']=M['phases'][integer(p['p14Phase'],0,6,'phase')]
 for field,key in [('Paused','finale_paused'),('Skipped','finale_skipped'),('Replay','replay_mode')]:s[key]=bool(integer(p['p14'+field],0,1,'boolean'))
 n=integer(p['p14CreditCount'],0,59,'credit count');s['credit_ids']=[];s['credit_cursor']=p['p14CreditCursor']
 reverse={v:k for k,v in M['sources'].items()}
 for i in range(59):
  source=p['p14Credit'+str(i)]
  if i<n:
   if source not in reverse or not reverse[source].startswith('credit:'):raise ValueError('Invalid credit source')
   s['credit_ids'].append(reverse[source][7:])
  elif source:raise ValueError('Credit outside count')
 for source,id in M['sources'].items():
  if serial(id+16):s['presentations'][source]={'serial':serial(id+16),'receipts':{b['token']:serial(b['slot']) for b in M['receipts'][source] if serial(b['slot'])}}
  elif any(serial(b['slot']) for b in M['receipts'][source]):raise ValueError('Orphan receipt')
 result={'kind':'cakood-p14-branch','schema':1,'state':s};P14World.load(result);return result

def project_context(call,c,epoch):
 """Project validated actual model owners. Return only after native sealing."""
 if type(c) is not P14Context:raise ValueError('P14 context required')
 c.__post_init__();integer(epoch,1,32767,'epoch')
 mask=sum(1<<i for i,f in enumerate(M['prerequisites']) if f in c.flags);rooms=dict(c.npc_locations)
 args=[M['rooms'][c.room],int(c.on_apron),*divmod(mask,BASE),M['rooms'][c.board_room],M['tones'].index(c.vivian_tone),int(c.contest_active),*[M['rooms'][rooms[p]] if p in rooms else -1 for p in PEOPLE[1:]],epoch]
 if not call('p14Context',*args):raise ValueError('Native context rejected')
 for obj in c.inventory:
  if obj not in M['objects'] or not call('p14ContextItem',M['objects'][obj]):raise ValueError('Invalid context inventory')
 if c.contests is not None:
  c.contests.validate()
  for a in c.contests.attempts:
   if a.outcome is not None and a.outcome.winner=='jack':
    if not call('p14ContextWin',CONTEST_IDS.index(a.encounter_id),*divmod(ordinal(a.outcome.id,a.encounter_id),BASE)):raise ValueError('Native winning timeline rejected')
 for i,char in enumerate(c.repair_date):
  if not call('p14ContextDateChar',i,*divmod(ord(char),BASE)):raise ValueError('Native date rejected')
 if not call('p14SealContext'):raise ValueError('Native context not sealed')

def terms_handoff_args(h):
 if (type(h) is not dict or h.get('object_id')!='renewal_repair_card' or h.get('location')!='inventory'
     or h.get('signed') is not False or h.get('repair_date') is not None
     or h.get('signature_owner')!='P14' or h.get('terms_record_id')!='P09.READ.002'):
  raise ValueError('Original unsigned P09 terms card handoff required')
 return (M['objects']['renewal_repair_card'],1,0,0,14,M['terms_record_id'])

def credit_masks(urls):
 if type(urls) is not tuple or any(type(x) is not str for x in urls) or not set(urls)<=set(M['asset_credits'].values()):raise ValueError('Unknown shipped source acknowledgment')
 masks=[0,0,0]
 for i,url in enumerate(M['asset_credits'].values()):
  if url in urls:masks[i//15]|=1<<(i%15)
 return tuple(masks)

class NativeCreditReplay:
 """Own a fresh native instance and immutable JSON invoking session by value.

 vm_factory must return a fresh independent native state object with p/call and
 persistent APIs. Production host must provide an isolated SCI heap/session and
 persist the envelope atomically; this transport does not call a save kernel.
 """
 def __init__(self,viewer,session,returned=False):
  self.viewer=viewer;self._invoking=json.loads(json.dumps(session,allow_nan=False));self.returned=returned
  if type(self._invoking) is not dict:raise ValueError('Invoking session must be a save object')
 @classmethod
 def create(cls,source,invoking_session,vm_factory):
  # Validate both before mutation, and never give the viewer the caller's VM.
  session=json.loads(json.dumps(invoking_session,allow_nan=False))
  if type(session) is not dict:raise ValueError('Invoking session must be a save object')
  words=list(source.persistent().values());decode_words(words)
  viewer=vm_factory()
  if viewer is source or viewer.p is source.p:raise ValueError('Replay requires a detached native instance')
  source_machine=getattr(source,'machine',None);viewer_machine=getattr(viewer,'machine',None)
  if source_machine is not None and viewer_machine is not None:
   if viewer_machine is source_machine or viewer_machine.locals is source_machine.locals:raise ValueError('Replay requires an isolated native local arena')
  source_arrays=getattr(source,'arrays',None);viewer_arrays=getattr(viewer,'arrays',None)
  if source_arrays is not None and viewer_arrays is not None:
   if viewer_arrays is source_arrays or bool({id(v) for v in viewer_arrays.values()} & {id(v) for v in source_arrays.values()}):raise ValueError('Replay requires isolated source arrays')
  viewer.p.update(zip(M['persisted_properties'],words))
  if not viewer.call('p14AfterRestore') or not viewer.call('p14PrepareReplay'):raise ValueError('Credits require legitimate completion')
  return cls(viewer,session)
 def save(self):
  return {'kind':'cakood-native-credit-replay','schema':1,'words':list(self.viewer.persistent().values()),'invoking_session':copy.deepcopy(self._invoking),'returned':self.returned}
 @classmethod
 def load(cls,data,vm_factory):
  if type(data) is not dict or set(data)!={'kind','schema','words','invoking_session','returned'} or data['kind']!='cakood-native-credit-replay' or type(data['schema']) is not int or data['schema']!=1 or type(data['returned']) is not bool or type(data['invoking_session']) is not dict:raise ValueError('Invalid replay envelope')
  state=decode_words(data['words'])['state']
  if not state['replay_mode'] or state['finale_phase'] not in ('credits','finished'):raise ValueError('Invalid detached credit roll')
  viewer=vm_factory();viewer.p.update(zip(M['persisted_properties'],data['words']))
  if not viewer.call('p14AfterRestore'):raise ValueError('Invalid native replay')
  return cls(viewer,data['invoking_session'],data['returned'])
 def return_session(self,cancel=False):
  if type(cancel) is not bool:raise ValueError('Invalid replay exit')
  if self.viewer.p['p14Phase']!=6:
   if not cancel:raise ValueError('Finish or explicitly close replay')
   self.viewer.call('p14SkipFinale')
   if self.viewer.p['p14Phase']!=6:raise ValueError('Replay could not close')
  self.returned=True;return copy.deepcopy(self._invoking)
