"""Strict P14 selection/receipt plans. Pure host glue, separately unaccepted.

Plans do not prove current actors, PA, shipped assets or pixels. The host must
recheck the live owner before every frame/receipt and retire on lifecycle change.
"""
from pathlib import Path
from copy import deepcopy
import hashlib,json,sys
H=Path(__file__).resolve().parent
from caption_layout import admit_date
M=json.loads((H/'generated/manifest.json').read_text());A=json.loads((H/'inputs/reference-schema.json').read_text())
def require(ok,why):
 if not ok:raise ValueError(why)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def integer(value,lo,hi,label):require(type(value) is int and lo<=value<=hi,'Invalid '+label);return value
def date_snapshot(domain):
 require(domain.call('p14Validate')==1,'Invalid actual P14 owner')
 p=domain.p;sid=A['sources']['readback'];n=integer(p['p14DateLength'],1,80,'selected date length');points=[]
 for i in range(80):
  hi=integer(domain.call('p14DateHiAt',i),0,33,'date high');lo=integer(domain.call('p14DateLoAt',i),0,32767,'date low');v=hi*32768+lo
  if i<n:points.append(v)
  else:require(v==0,'Date tail must be empty')
 raw=''.join(chr(v) for v in points);admit_date(raw)
 require(p['p14PresentationSource']==sid,'Actual current readback presentation required')
 snapshot=dict(owner_script=996,owner_export=0,owner_instance=str(id(domain)),epoch=integer(p['p14Epoch'],1,32767,'epoch'),revision=[p['p14RevisionHi'],p['p14RevisionLo']],start=[p['p14StartHi'],p['p14StartLo']],source='readback',source_number=sid,source_start=[domain.call('p14SerialHi',sid+16),domain.call('p14SerialLo',sid+16)],repair_date=raw,date_scalars=points,source_sha256=A['source_sha256'],record_id='P14.READ.001',unit_id='P14.READ.001.01')
 require(snapshot['source_start']==[p['p14PresentationHi'],p['p14PresentationLo']],'Current readback serial required')
 for key in ('revision','start','source_start'):
  require(len(snapshot[key])==2 and all(type(v) is int and 0<=v<=32767 for v in snapshot[key]) and any(snapshot[key]),'Invalid '+key)
 return snapshot
DATE_KEYS={'owner_script','owner_export','owner_instance','epoch','revision','start','source','source_number','source_start','repair_date','date_scalars','source_sha256','record_id','unit_id'}
def validate_date_snapshot(s):
 require(type(s) is dict and set(s)==DATE_KEYS,'Exact captured date snapshot required')
 require(s['owner_script']==996 and type(s['owner_script']) is int and s['owner_export']==0 and type(s['owner_export']) is int,'Exact P14 owner required')
 require(type(s['owner_instance']) is str and s['owner_instance'].isascii() and s['owner_instance'].isdigit(),'Captured owner instance required')
 require(s['source']=='readback' and s['source_number']==A['sources']['readback'] and s['source_sha256']==A['source_sha256'] and s['record_id']=='P14.READ.001' and s['unit_id']=='P14.READ.001.01','Date source identity')
 integer(s['epoch'],1,32767,'epoch');admit_date(s['repair_date'])
 require(type(s['date_scalars']) is list and all(type(v) is int for v in s['date_scalars']) and s['date_scalars']==list(map(ord,s['repair_date'])),'Exact selected scalar identity')
 for key in ('revision','start','source_start'):require(type(s[key]) is list and len(s[key])==2 and all(type(v) is int and 0<=v<=32767 for v in s[key]) and any(s[key]),'Invalid '+key)
 return s

def date_plan(snapshot,unit=False):
 validate_date_snapshot(snapshot);require(type(unit) is bool,'Exact unit/record choice required')
 original=next(r for r in M['canonical_records'] if r['id']=='P14.READ.001');text=original['text'].format(repair_date=snapshot['repair_date']);doc=1801 if unit else 1800;pages=[]
 # Native protocol preserves every ASCII character, adding only line breaks.
 for start in range(0,len(text),150):
  raw=text[start:start+150];shown='\n'.join(raw[i:i+50] for i in range(0,len(raw),50));pages.append(dict(document_id=doc,page=len(pages),raw_text=raw,text=shown,source_char_range=[start,start+len(raw)],source_utf8_byte_range=[start,start+len(raw)],bytes_with_nul=len(shown)+1))
 at=original['text'].index('{repair_date}')
 return dict(record_id='P14.READ.001',unit_id='P14.READ.001.01' if unit else None,document_id=doc,pages=pages,source_text=text,canonical_template=original,substitution=dict(template_range=[at,at+13],expanded_range=[at,at+len(snapshot['repair_date'])],value=snapshot['repair_date']),snapshot=deepcopy(snapshot),snapshot_sha256=digest(snapshot),audio_gap='Runtime native audio absent unless exact selected snapshot materialization is separately integrated',voice_index=0,mouth_gate='closed',display_authority=False,source_receipt_authority=False)
def date_commands(snapshot):
 validate_date_snapshot(snapshot)
 return [(2,[996,snapshot['epoch'],*snapshot['revision'],*snapshot['start'],*snapshot['source_start'],len(snapshot['repair_date'])])]+[(3,[i,c]) for i,c in enumerate(snapshot['date_scalars'])]+[(4,[])]
def date_is_current(plan,domain):
 try:return date_plan(date_snapshot(domain),plan['unit_id'] is not None)==plan
 except (ValueError,KeyError,TypeError):return False

def notebook_snapshot(owner):
 require(owner is not None,'Actual retained contest owner required');owner.validate();state=owner.snapshot();missing=list(owner.missing_wins)
 require(len(missing)==len(set(missing)) and all(v in A['contest_ids'] for v in missing),'Owner contest IDs')
 require(missing==[v for v in A['contest_ids'] if v in missing],'Canonical missing-contest order')
 return dict(owner_generation=integer(owner.owner_generation,1,2147483647,'contest owner generation'),owner_instance=str(id(owner)),owner_snapshot_sha256=digest(state),missing_contest_ids=missing,won_count=4-len(missing),missing_contest_names=', '.join(A['contest_names'][A['contest_ids'].index(c)] for c in missing))
def notebook_plan(owner,gate=False):
 require(type(gate) is bool,'Exact gate choice required');s=notebook_snapshot(owner);rid='VC.GATE.MISSING_WINS' if gate and s['missing_contest_ids'] else 'VC.GATE.ALL_WON' if gate else 'VC.NOTEBOOK.WINS'
 if rid=='VC.GATE.ALL_WON':r=next(r for r in M['routes'] if r['record_id']==rid)
 else:
  mask=sum(1<<i for i,c in enumerate(A['contest_ids']) if c not in s['missing_contest_ids']);r=next(r for r in M['variant_routes'] if r['record_id']==rid and r['binding']['mask']==mask)
 return dict(record_id=rid,document_id=r['document_id'],pages=[[r['document_id'],i] for i in range(r['page_count'])],snapshot=s,display_authority=False,source_receipt_authority=False)
def notebook_is_current(plan,owner):
 try:return plan==notebook_plan(owner,plan['record_id']!='VC.NOTEBOOK.WINS')
 except (ValueError,KeyError,TypeError):return False

def credit_selection(shipped_manifest,root):
 """Require explicit shipped-byte provenance, never fetch an asset for a credit.

 The caller owns truthful provenance and final shipping inclusion; this validates
 exact file bytes and known URLs. It is not a license or authorship detector.
 """
 require(type(shipped_manifest) is list,'Exact shipped artifact manifest required');root=Path(root).resolve();rows=[];urls=[]
 for row in shipped_manifest:
  require(type(row) is dict and set(row)=={'path','sha256','source_url'},'Exact shipped-source row required')
  require(all(type(v) is str and v for v in row.values()),'Exact shipped-source strings required')
  path=(root/row['path']).resolve();require(path.is_relative_to(root) and path.is_file() and not (root/row['path']).is_symlink(),'Actual in-root shipped file required')
  require(hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],'Shipped file hash mismatch')
  require(row['source_url'] in A['asset_credits'].values(),'Unknown acknowledgment source');rows.append(deepcopy(row));urls.append(row['source_url'])
 require(len({r['path'] for r in rows})==len(rows),'Repeated shipped artifact')
 ids=list(A['credit_order'])+[rid for rid,url in A['asset_credits'].items() if url in urls]
 return dict(credit_ids=ids,shipped_rows=rows,selection_sha256=digest(rows),urls=[url for url in A['asset_credits'].values() if url in urls],actual_shipped_evidence_required=True)
def validate_credit_selection(selection):
 require(type(selection) is dict and set(selection)=={'credit_ids','shipped_rows','selection_sha256','urls','actual_shipped_evidence_required'},'Exact shipped selection required')
 rows=selection['shipped_rows'];require(type(rows) is list and all(type(r) is dict and set(r)=={'path','sha256','source_url'} and all(type(v) is str and v for v in r.values()) for r in rows),'Exact shipped rows')
 require(selection['selection_sha256']==digest(rows),'Shipped selection digest')
 urls=[url for url in A['asset_credits'].values() if any(r['source_url']==url for r in rows)]
 require(selection['urls']==urls and all(r['source_url'] in A['asset_credits'].values() for r in rows),'Exact selected source URLs')
 expected=list(A['credit_order'])+[rid for rid,url in A['asset_credits'].items() if url in urls]
 require(selection['credit_ids']==expected and selection['actual_shipped_evidence_required'] is True,'Exact mandatory/conditional credit prefix')
 return selection

def credit_snapshot(domain,selection):
 validate_credit_selection(selection)
 require(domain.call('p14Validate')==1,'Invalid actual P14 owner')
 expected=selection['credit_ids'];actual=[next((rid for rid,key in A['line_ids'].items() if key==domain.call('p14CreditRecord',i)),None) for i in range(domain.p['p14CreditCount'])]
 require(actual==expected,'Live credit prefix and shipped-source selection differ')
 return dict(selection=deepcopy(selection),owner_instance=str(id(domain)),epoch=domain.p['p14Epoch'],credit_ids=actual,cursor=domain.p['p14CreditCursor'],phase=domain.p['p14Phase'],replay=domain.p['p14Replay'],revision=[domain.p['p14RevisionHi'],domain.p['p14RevisionLo']])

def credit_is_current(binding,domain,root):
 try:
  selection=credit_selection(binding['selection']['shipped_rows'],root)
  return credit_snapshot(domain,selection)==binding
 except (ValueError,KeyError,TypeError):return False

def source_plan(source,record_id=None,unit_ids=(),date_binding=None,credit_binding=None):
 require(type(source) is str and source in A['source_bindings'],'Unknown source');rid=A['source_bindings'][source];r=next(r for r in M['routes'] if r['record_id']==rid)
 require(type(unit_ids) in (list,tuple) and all(type(x) is str for x in unit_ids),'Exact canonical units required')
 if source.startswith('credit:'):
  keys={'selection','owner_instance','epoch','credit_ids','cursor','phase','replay','revision'}
  require(type(credit_binding) is dict and set(credit_binding)==keys,'Actual selected credit snapshot required');validate_credit_selection(credit_binding['selection'])
  require(credit_binding['credit_ids']==credit_binding['selection']['credit_ids'] and type(credit_binding['cursor']) is int and 0<=credit_binding['cursor']<len(credit_binding['credit_ids']) and credit_binding['phase']==5 and credit_binding['credit_ids'][credit_binding['cursor']]==rid,'Current selected credit cursor required')
 elif credit_binding is not None:raise ValueError('Unexpected credit binding')
 if record_id is not None:
  require(type(record_id) is str and record_id==rid and not unit_ids,'Exactly one bound record/unit form required');form=[A['line_ids'][rid],0,0]
  if rid=='P14.READ.001':p=date_plan(date_binding);pages=[[p['document_id'],v['page']] for v in p['pages']]
  else:require(date_binding is None,'Unexpected date binding');pages=[[r['document_id'],n] for n in range(r['page_count'])]
 else:
  legal=r['canonical_units'];require(unit_ids and len(set(unit_ids))==len(unit_ids) and all(u in legal for u in unit_ids),'Unknown/empty/repeated canonical unit')
  indices=[legal.index(u) for u in unit_ids];require(indices==list(range(indices[0],indices[0]+len(indices))),'Contiguous canonical units required');form=[0,A['speech_unit_ids'][unit_ids[0]],A['speech_unit_ids'][unit_ids[-1]]]
  if rid=='P14.READ.001':p=date_plan(date_binding,True);pages=[[p['document_id'],v['page']] for v in p['pages']]
  else:
   require(date_binding is None,'Unexpected date binding');rows=[next(r for r in M['unit_routes'] if r['line_id']==u) for u in unit_ids];pages=[[r['document_id'],n] for r in rows for n in range(r['page_count'])]
 return dict(source=source,source_number=A['sources'][source],record_id=rid,units=list(unit_ids),domain_form=form,pages=pages,date_snapshot=deepcopy(date_binding),credit_snapshot=deepcopy(credit_binding),display_authority=False,receipt_requires_exact_live_source_start_epoch_and_every_page=True)

class DateBinding:
 """Testable host-side lifecycle shell, separately unaccepted for production.

 The bank alone does not authenticate a live domain. This shell compares every
 date character and every serial against the actual owner before display.
 """
 def __init__(self,domain,bank_call,unit=False):
  self.domain=domain;self.bank_call=bank_call;self.plan=date_plan(date_snapshot(domain),unit);self.retired=False
  for n,args in date_commands(self.plan['snapshot']):require(bank_call(n,*args)==1,'Native date protocol rejected snapshot')
 def current(self):
  if self.retired:return False
  if not date_is_current(self.plan,self.domain):self.retire();return False
  if self.bank_call(4)!=1:self.retire();return False
  s=self.plan['snapshot'];expected=[len(s['repair_date']),len(s['repair_date']),996,s['epoch'],*s['revision'],*s['start'],*s['source_start'],0]
  if [self.bank_call(5,2,i) for i in range(11)]!=expected or [self.bank_call(5,1,i) for i in range(len(s['repair_date']))]!=s['date_scalars']:
   self.retire();return False
  return True
 def retire(self):self.retired=True;self.bank_call(1);return False
