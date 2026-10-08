from pathlib import Path
import sys,json,unittest,copy,tempfile,hashlib
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests'),str(H/'tools')]
from host import setup,frame
from test_runtime import exp
from remote_owner import Owner
import mapping,materialize_date
A=json.loads((H/'inputs/reference-schema.json').read_text());M=json.loads((H/'generated/manifest.json').read_text())
class Evidence:
 """Finite test receipt shell around actual emitted Graph12 and page identity.
 It is not a production or native host and cannot supply actor/PA eligibility.
 """
 def __init__(self,h,d,a,plan):self.h,self.d,self.a=h,d,a;self.plan=plan;self.seen=[];self.retired=False
 def show(self,pair):
  doc,page=pair
  if not self.d.p['sdActive'] or self.d.p['sdDocument']!=doc:assert self.h.call('dialogueOpen',doc)==1
  if self.d.p['sdPage']!=page:self.h.call('uiTurnPage',page-self.d.p['sdPage'])
  before=sum(n=='Graph' and v[0]==12 for n,v in self.h.vm.ktrace);frame(self.h)
  assert self.h.call('scenePageIdentity')==1 and self.d.p['sdDocument']==doc and self.d.p['sdPage']==page
  assert sum(n=='Graph' and v[0]==12 for n,v in self.h.vm.ktrace)>before
  if pair in self.plan['pages'] and pair not in self.seen:self.seen.append(pair)
 @property
 def complete(self):return not self.retired and self.seen==self.plan['pages']
class DomainTests(unittest.TestCase):
 def test_actual_source_and_emitted_date_values_and_retirement(self):
  for kind in ('source','emitted'):
   for date in ('MiXeD selected day','Q'*80):
    with Owner(kind,date) as owner:
     self.assertEqual(owner.call('p14Begin',22),A['codes']['presentation_pending']);snapshot=mapping.date_snapshot(owner);self.assertEqual(snapshot['repair_date'],date)
     h,d,a,*_=setup();bank=lambda n,*args:exp(h.vm,d,n,*args);bound=mapping.DateBinding(owner,bank);self.assertTrue(bound.current())
     plan=mapping.source_plan('readback',unit_ids=('P14.READ.001.01',),date_binding=snapshot);ev=Evidence(h,d,a,plan)
     for pair in plan['pages']:
      self.assertTrue(bound.current());self.assertFalse(ev.complete);ev.show(pair)
     self.assertTrue(ev.complete);self.assertEqual(d.p['sdVoice'],0)
     before=owner.request('persisted');owner.call('p14AudioFinished');self.assertEqual(owner.request('persisted'),before)
     self.assertEqual(owner.call('p14Acknowledge',22,*snapshot['source_start'],snapshot['epoch'],*plan['domain_form']),A['codes']['presentation_acknowledged']);self.assertEqual(owner.call('p14Complete',22),1)
     self.assertFalse(bound.current());self.assertEqual(bank(5,0,0),0)
 def test_valid_ascii_bank_tampering_is_rejected_against_live_owner(self):
  with Owner(date='CaseExact') as owner:
   owner.call('p14Begin',22);h,d,a,*_=setup();bound=mapping.DateBinding(owner,lambda n,*args:exp(h.vm,d,n,*args));self.assertTrue(bound.current());h.vm.arrays(999)['fbDate'][0]=ord('X');self.assertFalse(bound.current());self.assertEqual(exp(h.vm,d,5,0,0),0)
 def test_domain_restore_stale_epoch_and_snapshot_identity(self):
  with Owner(date='Same exact date') as owner:
   owner.call('p14Begin',22);s=mapping.date_snapshot(owner);p=mapping.date_plan(s);self.assertTrue(mapping.date_is_current(p,owner));owner.request('restore');self.assertFalse(mapping.date_is_current(p,owner))
   with self.assertRaises(ValueError):mapping.date_snapshot(owner)
   changed=copy.deepcopy(s);changed['repair_date']='Other';self.assertRaises(ValueError,mapping.date_plan,changed)
 def test_exact_selected_audio_materialization_and_no_substitute(self):
  with Owner(date='MiXeD explicit audio date') as owner:
   owner.call('p14Begin',22);s=mapping.date_snapshot(owner);p=mapping.date_plan(s)
   with tempfile.TemporaryDirectory(dir=H/'evidence') as t:
    artifact=materialize_date.materialize(s,Path(t)/'selected')
    self.assertTrue(artifact['double_render_exact']);self.assertTrue(materialize_date.eligible(artifact,p,owner));self.assertEqual(''.join(r['raw_text'] for r in artifact['rows']),p['source_text'])
    artifact['snapshot']['repair_date']='Substituted';self.assertFalse(materialize_date.eligible(artifact,p,owner))
 def test_every_approval_requires_own_display_and_audio_grants_nothing(self):
  with Owner(stage='approvals') as owner:
   h,d,a,*_=setup()
   for person in A['people']:
    source='approve:'+person;sid=A['sources'][source];self.assertEqual(owner.call('p14Begin',sid),A['codes']['presentation_pending']);props=owner.p;serial=[props[f'p14Source{sid}StartHi'],props[f'p14Source{sid}StartLo']]
    plan=mapping.source_plan(source,record_id=A['source_bindings'][source]);ev=Evidence(h,d,a,plan);before=owner.request('persisted');owner.call('p14AudioFinished');owner.call('p14Complete',sid);self.assertEqual(owner.request('persisted'),before);self.assertFalse(ev.complete)
    for pair in plan['pages']:ev.show(pair)
    self.assertTrue(ev.complete);self.assertEqual(owner.call('p14Acknowledge',sid,*serial,props['p14Epoch'],*plan['domain_form']),A['codes']['presentation_acknowledged']);self.assertEqual(owner.call('p14Complete',sid),1)
   self.assertEqual(owner.p['p14SignatureHi'],0);self.assertEqual(owner.p['p14SignatureLo'],0);self.assertEqual(owner.p['p14PencilLo'],0);self.assertEqual(owner.p['p14CompleteLo'],0)
 def test_five_consent_units_preserve_independent_receipts(self):
  for kind in ('source','emitted'):
   with Owner(kind=kind,stage='consent') as owner:
    source='signature';sid=A['sources'][source];self.assertEqual(owner.call('p14Begin',sid),A['codes']['presentation_pending']);props=owner.p;serial=[props[f'p14Source{sid}StartHi'],props[f'p14Source{sid}StartLo']]
    units=[u['line_id'] for u in M['canonical_speech_units'] if u['record_id']=='P14.DIALOGUE.003'];self.assertEqual(len(units),5);h,d,a,*_=setup()
    for index,unit in enumerate(units):
     self.assertEqual(owner.call('p14Complete',sid),0);plan=mapping.source_plan(source,unit_ids=[unit]);self.assertEqual(len(plan['units']),1);ev=Evidence(h,d,a,plan)
     for pair in plan['pages']:ev.show(pair)
     self.assertTrue(ev.complete);self.assertEqual(owner.call('p14Acknowledge',sid,*serial,props['p14Epoch'],*plan['domain_form']),A['codes']['presentation_acknowledged']);self.assertEqual(owner.call('p14Complete',sid),int(index==4))
     self.assertEqual(owner.p['p14SignatureLo'],0);self.assertEqual(owner.p['p14PencilLo'],0);self.assertEqual(owner.p['p14CompleteLo'],0)
    whole=mapping.source_plan(source,record_id='P14.DIALOGUE.003');self.assertNotEqual(whole['pages'],plan['pages']);self.assertEqual(len(whole['pages']),5)
 def test_actual_mandatory_credit_prefix_and_page_receipts(self):
  with Owner(stage='credits') as owner:
   selection=mapping.credit_selection([],H);self.assertEqual(len(selection['credit_ids']),26);h,d,a,*_=setup()
   for index,rid in enumerate(selection['credit_ids']):
    binding=mapping.credit_snapshot(owner,selection);self.assertEqual(binding['cursor'],index);source='credit:'+rid;sid=A['sources'][source];owner.call('p14Begin',sid);props=owner.p;serial=[props[f'p14Source{sid}StartHi'],props[f'p14Source{sid}StartLo']]
    plan=mapping.source_plan(source,record_id=rid,credit_binding=binding);ev=Evidence(h,d,a,plan)
    self.assertEqual(owner.call('p14AdvanceFinale'),A['codes']['whole_finale_record_required'])
    for pair in plan['pages']:
     self.assertFalse(ev.complete);ev.show(pair);self.assertEqual(d.p['sdVoice'],0)
    self.assertTrue(ev.complete);self.assertEqual(owner.call('p14Acknowledge',sid,*serial,props['p14Epoch'],*plan['domain_form']),A['codes']['presentation_acknowledged']);self.assertEqual(owner.call('p14AdvanceFinale'),A['codes']['finale_advanced'])
   self.assertEqual(owner.p['p14Phase'],6);self.assertEqual(owner.p['p14CreditCursor'],26)
 def test_detached_credit_replay_preserves_invoking_session_and_prefix(self):
  with Owner(stage='credits') as owner:
   session={'room':'L01','inventory':['grease_pencil'],'nested':{'choice':[3,1,4]},'timestamp_label':'explicit fixture'}
   envelope=owner.request('replay_create',session=session);self.assertEqual(envelope['invoking_session'],session);self.assertEqual(owner.p['p14Replay'],1)
   h,d,a,*_=setup();selection=mapping.credit_selection([],H)
   for index in range(3):
    rid=selection['credit_ids'][index];source='credit:'+rid;sid=A['sources'][source];binding=mapping.credit_snapshot(owner,selection);owner.call('p14Begin',sid);props=owner.p;plan=mapping.source_plan(source,record_id=rid,credit_binding=binding);ev=Evidence(h,d,a,plan)
    for pair in plan['pages']:ev.show(pair)
    self.assertTrue(ev.complete);owner.call('p14Acknowledge',sid,props[f'p14Source{sid}StartHi'],props[f'p14Source{sid}StartLo'],props['p14Epoch'],*plan['domain_form']);owner.call('p14AdvanceFinale')
   saved=owner.request('replay_save');self.assertEqual(owner.p['p14CreditCursor'],3);owner.request('replay_load',envelope=saved);self.assertEqual(owner.p['p14CreditCursor'],3);self.assertEqual(mapping.credit_snapshot(owner,selection)['credit_ids'],selection['credit_ids'])
   result=owner.request('replay_return');self.assertEqual(result['session'],session);self.assertTrue(result['original_unchanged'])
if __name__=='__main__':unittest.main()
