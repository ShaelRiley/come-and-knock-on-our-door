"""NEW revision-2 reference commit witness, bound to the live owner's history.

An owner-held chain advances only after actual successful outcome commits. The
composite saved owner record carries it separately from the observation list.
The hash is an ordinary consistency checksum, not authentication. Raw owner
state/semantics are unchanged; native atomic owner/history saving remains open.
"""
from dataclasses import dataclass
from pathlib import Path
import copy,hashlib,json
from dependencies.vc_owner.verbal_contest import atomic_write

KIND='cakood-p14-observed-contests'
SCHEMA=2
WITNESS_KEY='reference_commit_witness'
ALGORITHM='cakood-observed-outcomes-sha256-v1'
EMPTY=hashlib.sha256(b'cakood observed contest outcome history v1').hexdigest()

def canonical(value):
 return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')

@dataclass(frozen=True)
class Witness:
 count: int
 head: str
 def saved(self):return {'algorithm':ALGORITHM,'count':self.count,'head':self.head}

@dataclass(frozen=True)
class Outcome:
 id: str
 winner: str

@dataclass(frozen=True)
class ObservedAttempt:
 encounter_id: str
 outcome: Outcome

def initialize(owner):
 # Only a genuinely new owner starts with the empty commitment. Raw restore
 # explicitly detaches it; no historical commitment is inferred from counts.
 owner._observed_results=[]
 owner._reference_commit_witness=Witness(0,EMPTY)

def detach(owner):
 owner._observed_results=[]
 owner._reference_commit_witness=None

def extend(previous,state):
 return Witness(previous.count+1,hashlib.sha256(canonical({
  'algorithm':ALGORITHM,'previous':previous.head,'index':previous.count+1,
  'observed_outcome':state})).hexdigest())

def parsed_witness(value):
 if type(value) is not dict or set(value)!={'algorithm','count','head'} or value['algorithm']!=ALGORITHM or type(value['count']) is not int or value['count']<0 or type(value['head']) is not str or len(value['head'])!=64 or any(c not in '0123456789abcdef' for c in value['head']):
  raise ValueError('Invalid owner-side observation commit witness')
 return Witness(value['count'],value['head'])

def check_binding(owner):
 """Compare to the independently retained live witness; never reseal a ledger."""
 witness=owner.__dict__.get('_reference_commit_witness')
 if witness is None:return False
 if type(witness) is not Witness:raise ValueError('Invalid live observation commit witness')
 rows=owner.__dict__.get('_observed_results')
 if type(rows) is not list:raise ValueError('Missing paired observed contest history')
 derived=Witness(0,EMPTY)
 for row in rows:derived=extend(derived,row)
 if derived!=witness:raise ValueError('Owner-side commit witness does not match the paired observed history')
 return True

def capture(owner):
 """After accepted commit, under the same facade lock as the owner transaction."""
 if owner._reference_commit_witness is None:return
 s=owner.snapshot();a=s['active']
 if not a or not a['ko_committed']:return
 rows=owner._observed_results
 if rows and rows[-1]['active']['serial']==a['serial']:return
 witness=owner._reference_commit_witness
 if sum(h['completed'] for h in s['history'].values())!=witness.count+1:
  raise ValueError('Outcome observation boundary is incomplete')
 # Prepare by value before publishing either field while the owner lock is held.
 next_rows=[*rows,s];next_witness=extend(witness,s)
 owner._observed_results=next_rows
 owner._reference_commit_witness=next_witness

def attempts(owner):
 with owner._lock:
  return _attempts(owner)

def _attempts(owner):
 owner.validate();current=owner.snapshot()
 if not check_binding(owner):raise ValueError('Actual owner history needs its paired observed commit witness')
 rows=owner._observed_results
 totals={e:{'completed':0,'wins':0,'latest_winner':None,'concession_record':None,'last_outcome':None} for e in current['history']}
 answer=[];last=0
 for state in rows:
  owner._validate(state);a=state['active']
  if not a or not a['ko_committed'] or a['serial']<=last:raise ValueError('Observed outcome order mismatch')
  enc=a['encounter'];h=totals[enc];h['completed']+=1;h['wins']+=a['winner']=='jackie'
  h.update(latest_winner=a['winner'],concession_record=enc+('.WIN' if a['winner']=='jackie' else '.LOSS'),last_outcome=a['serial'])
  if totals!=state['history']:raise ValueError('Observed ledger lacks genuine earlier outcomes')
  if state['revision']>current['revision'] or a['serial']>current['attempt_serial']:raise ValueError('Observed outcome belongs to another timeline')
  if any(value and not current['knowledge'][p][k] for p,half in state['knowledge'].items() for k,value in half.items()):raise ValueError('Observed learning absent in invoking owner')
  answer.append(ObservedAttempt(enc,Outcome(f'{enc}:A{a["serial"]}:KO','jack' if a['winner']=='jackie' else 'opponent')))
  last=a['serial']
 if totals!=current['history']:raise ValueError('Actual owner history needs its paired observed outcome ledger')
 return tuple(answer)

def save(owner):
 # The owner, its independent commit witness and the ledger are one locked
 # snapshot. Owner.save retains its accepted raw format and lifecycle semantics.
 with owner._lock:
  _attempts(owner)
  record=json.loads(owner.save())
  record[WITNESS_KEY]=owner._reference_commit_witness.saved()
  return {'kind':KIND,'schema':SCHEMA,'owner':record,'observations':copy.deepcopy(owner._observed_results)}

def load(cls,data,*,owner_generation):
 if type(data) is not dict or set(data)!={'kind','schema','owner','observations'} or data['kind']!=KIND or type(data['schema']) is not int or data['schema']!=SCHEMA or type(data['owner']) is not dict or type(data['observations']) is not list:
  raise ValueError('Paired contest history requires schema 2 with an owner-side commit witness')
 record=data['owner']
 if set(record)!={'payload','sha256',WITNESS_KEY}:raise ValueError('Composite owner record lacks its observation commit witness')
 witness=parsed_witness(record[WITNESS_KEY])
 raw={k:copy.deepcopy(record[k]) for k in ('payload','sha256')}
 # Construct a disposable owner. Failed validation never replaces live state.
 owner=cls.load(canonical(raw),owner_generation=owner_generation)
 owner._reference_commit_witness=witness
 owner._observed_results=copy.deepcopy(data['observations'])
 _attempts(owner)
 return owner

def save_file(owner,path):
 # One reference host file, same-directory temporary + fsync + replace through
 # the accepted writer. This does not install native/kernel persistence.
 atomic_write(Path(path),canonical(save(owner)))

def load_file(cls,path,*,owner_generation):
 return load(cls,json.loads(Path(path).read_text()),owner_generation=owner_generation)
