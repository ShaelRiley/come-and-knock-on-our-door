"""NEW test-only compatibility helpers: real owner learning/play/read transitions.
Historical test_verbal_contest.py was not recovered. No flags/state are granted.
"""
from dataclasses import replace
from cakood.verbal_contest import VerbalContests,Catalog,Phase,YIELD_EXCHANGE
CATALOG=Catalog()
def bind_rescue_result(w,p,rescue):
 """NEW test-only host presentation projection, no contest or rescue mutation.
 The frozen contest owner supplies IDs/base text. Current P11 serials select the
 authored exact variant before the host acknowledges that same readable unit.
 """
 if rescue is None or p.record_id not in ('VC03.WIN','VC03.LOSS') or p.unit_id is None:return p
 from cakood.p11_model import P11World
 if type(rescue) is not P11World:raise ValueError('Actual P11 rescue owner required')
 rescue.validate()
 if not rescue.contest_eligible:raise ValueError('Protected completed rescue required')
 unit=w.catalog.speech_unit(p.unit_id)
 if 'finite_variants' not in unit:return p
 variants={v['variant_id']:v for v in unit['finite_variants']}
 selected=None
 for key in unit['variant_binding']['priority']:
  variant=variants[key]
  checks=[]
  for predicate in variant['when']['all']:
   value=getattr(rescue,predicate['field'])
   if predicate['op']=='gt':checks.append(value>predicate['value'])
   elif predicate['op']=='eq':checks.append(value==predicate['value'])
   else:raise ValueError('Unknown canonical variant predicate')
  if all(checks):selected=variant;break
 if selected is None:raise ValueError('No truthful completed rescue account')
 record=w.catalog.record(p.record_id)
 matching=next(v for v in record['finite_variants'] if v['variant_id']==selected['variant_id'])
 if matching['text'][int(p.unit_id.rsplit('.',1)[1])-1]['text']!=selected['text']:raise ValueError('Canonical record/unit variant mismatch')
 return replace(p,text=selected['text'],bindings=(*p.bindings,('rescue_credit_variant',selected['variant_id'])))
def read_all(w,*,rescue=None):
 shown=[]
 while (p:=w.pending_text()) is not None:
  presented=bind_rescue_result(w,p,rescue);shown.append(presented)
  w.acknowledge_text(presented.receipt)
 return shown
def prepared(enc='VC03',w=None):
 w=w or VerbalContests(CATALOG)
 if enc not in w.snapshot()['introduced']:
  w.introduce(enc,admitted=True);read_all(w)
 for pair in w.catalog.eligible(enc):w.present_lesson(enc,pair);read_all(w)
 return w
def play(w,results,enc='VC03'):
 w.enter(enc,0,admitted=True)
 for win in results:
  w.begin_turn(w.active.id);read_all(w)
  a=w.active;pair=a.deck[a.cursor]
  reply=next(iter(w.catalog.pairs[pair].accepted_response_ids)) if win else YIELD_EXCHANGE
  w.choose_response(a.exchange_id,reply);w.commit_response(a.exchange_id);read_all(w)
  if w.active.phase==Phase.KO_PENDING:break
 w.commit_ko(w.active.outcome_id)
 return w
def leave(w,*,rescue=None,shown=None):
 rendered=read_all(w,rescue=rescue)
 if shown is not None:shown.extend(rendered)
 if w.active is not None:raise RuntimeError('Contest remains active before result text completed')
 return w
