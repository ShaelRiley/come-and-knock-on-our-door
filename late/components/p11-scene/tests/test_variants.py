"""Actual owner histories and modeled page receipts. Never native presentation proof."""
from pathlib import Path
from dataclasses import replace
import unittest,json,sys,copy,importlib.util,zipfile,hashlib
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests'),str(H/'inputs/model'),str(H/'inputs/model/tests')]
import mapping
from scene_vm import VM as RawVM
from host import setup,frame
from test_current_contract import repaired_gate
from test_p11_model import C,read,clone
from cakood.p11_model import P11World,RECORD_UNITS
from cakood.p04_model import project_gate
EVIDENCE={}
M=json.loads((H/'generated/manifest.json').read_text());D=json.loads((H/'inputs/domain/schema.json').read_text())
spec=importlib.util.spec_from_file_location('frozen_contest_owner',H/'inputs/contest-owner/verbal_contest.py');vc=importlib.util.module_from_spec(spec);sys.modules[spec.name]=vc;spec.loader.exec_module(vc)


def history(pre):
 owner=repaired_gate()
 if pre:owner.set_peg(1)
 c=replace(C,gate=project_gate(owner));w=P11World();w.lift(c)
 if not pre:
  w.request_peg(c);owner.set_peg(1);c=replace(c,gate=project_gate(owner));w.acknowledge_peg(c,w.pending_peg_request_id)
 w.release_catch(c);w.pull_handle(c);w.stage_display(c);read(w,c,'sincere')
 assert w.ready and w.contest_eligible
 assert c.bunny_room=='L03_PORCH' and c.frankie_room=='L05_COURTYARD'
 request=w.request_contest(c);event=request.events[0]
 snapshot={k:event.payload[k] for k in ['rescue_credit_variant','peg_ack_at','advance_peg_at']}
 w.acknowledge_contest_request(c,w.pending_contest_request_id)
 return owner,w,c,snapshot


def raw_domain(w):
 d=RawVM(H/'inputs/domain/src/module993.sc','P11State');d.call('p11Init')
 d.p.update(p11Initialized=1,p11Phase=int(w.phase),p11HintLevel=w.hint_level)
 for native,key in D['state_serials'].items():d.p['p11'+native+'Hi'],d.p['p11'+native+'Lo']=divmod(getattr(w,key),32768)
 return d


def present_outcome_unit(w,snapshot,emitted,limit=None):
 """Test-only bridge: exact page evidence precedes original owner receipt."""
 p=w.pending_text();assert p is not None and p.record_id in ('VC03.WIN','VC03.LOSS') and p.unit_id
 plan=mapping.outcome_plan(p.record_id,snapshot,(p.unit_id,));route=next(r for r in M['variant_unit_routes'] if r['document_id']==plan['documents'][0]);visible=[]
 h,d,a=emitted;assert h.call('dialogueOpen',route['document_id'])==1
 maximum=route['page_count'] if limit is None else limit
 for page,i in enumerate(route['page_indices'][:maximum]):
  if page:h.call('uiTurnPage',1)
  assert d.p['sdPage']==page
  before=sum(n=='Graph' and args[0]==12 for n,args in h.vm.ktrace);frame(h)
  assert sum(n=='Graph' and args[0]==12 for n,args in h.vm.ktrace)>before
  assert str(d.arrays['sdTextBuffer'])==M['pages'][i]['text'];visible.append([route['document_id'],page])
 complete=visible==plan['pages']
 if complete:w.acknowledge_text(p.receipt)
 return dict(record=p.record_id,unit=p.unit_id,variant=plan['variant_id'],raw=''.join(M['pages'][i]['raw_text'] for i in route['page_indices']),pages=visible,owner_base_text=p.text,complete=complete)


def read_contest(w,snapshot=None,emitted=None):
 shown=[]
 while (p:=w.pending_text()) is not None:
  if snapshot is not None and p.record_id in ('VC03.WIN','VC03.LOSS') and p.unit_id:
   shown.append(present_outcome_unit(w,snapshot,emitted));assert shown[-1]['complete']
  else:w.acknowledge_text(p.receipt)
 return shown


def play(w,win):
 w.enter('VC03',0,admitted=True)
 for _ in range(3):
  w.begin_turn(w.active.id);read_contest(w)
  a=w.active;pair=a.deck[a.cursor];reply=next(iter(w.catalog.pairs[pair].accepted_response_ids)) if win else vc.YIELD_EXCHANGE
  w.choose_response(a.exchange_id,reply);w.commit_response(a.exchange_id);read_contest(w)
  if w.active.phase==vc.Phase.KO_PENDING:break
 w.commit_ko(w.active.outcome_id)


class VariantTests(unittest.TestCase):
 def test_genuine_numeric_owner_histories_and_exact_source_getters(self):
  for pre in (False,True):
   owner,w,c,snapshot=history(pre);before=owner.save();d=raw_domain(w)
   self.assertEqual(d.call('p11RescueCreditVariant'),2 if pre else 1)
   for name,slot in [('peg_ack_at',7),('advance_peg_at',8)]:self.assertEqual(d.call('p11SerialHi',slot)*32768+d.call('p11SerialLo',slot),snapshot[name])
   self.assertEqual(mapping.rescue_variant(snapshot['peg_ack_at'],snapshot['advance_peg_at']),w.rescue_credit_variant)
   self.assertEqual(owner.save(),before);self.assertEqual(clone(w,c).rescue_credit_variant,w.rescue_credit_variant)
   if pre:self.assertEqual(snapshot['peg_ack_at'],0)
 def test_actual_contest_loss_win_opposite_rematches_with_emitted_variant_pages(self):
  h,d,a,*_=setup();cases=units=pages=0
  for pre in (False,True):
   owner,w,c,snapshot=history(pre);saved=w.save();owner_saved=owner.save()
   contest=vc.VerbalContests(vc.Catalog(fixture=H/'inputs/contest-owner/canonical-bindings.json'))
   contest.introduce('VC03',admitted=True);read_contest(contest)
   for pair in contest.catalog.eligible('VC03'):contest.present_lesson('VC03',pair);read_contest(contest)
   for round_index,win in enumerate((False,True,False)):
    play(contest,win);shown=read_contest(contest,snapshot,(h,d,a));rid='VC03.WIN' if win else 'VC03.LOSS'
    selected=next(r for r in M['variant_routes'] if (r['record_id'],r['variant_id'])==(rid,snapshot['rescue_credit_variant']))
    self.assertEqual([s['unit'] for s in shown],[rid+'.01',rid+'.02']);self.assertEqual([s['raw'] for s in shown],[s['source_text'] for s in selected['segments']])
    if pre:self.assertNotEqual(shown[1]['raw'],shown[1]['owner_base_text'])
    self.assertIn('VC03_RESOLVED',contest.flags)
    if win:self.assertIn('VC03_WON',contest.flags)
    elif round_index==0:self.assertNotIn('VC03_WON',contest.flags)
    else:self.assertIn('VC03_WON',contest.flags)
    self.assertEqual(w.save(),saved);self.assertEqual(owner.save(),owner_saved);self.assertFalse(w.flags&{'VC03_WON','DISPLAY_REVEALED','GAME_COMPLETE'})
    cases+=1;units+=len(shown);pages+=sum(len(s['pages']) for s in shown)
  EVIDENCE.update(real_numeric_P04_P11_histories=2,actual_contest_outcomes=cases,selected_outcome_units=units,emitted_selected_outcome_pages=pages,loss_then_win_then_loss=True,rescue_facts_unchanged=True,generic_owner_unchanged=True,native_display_proof=False)
 def test_selected_unit_page_counts_and_partial_display_never_whole(self):
  counts={};h,d,a,*_=setup();partial_cases=0
  for pre in (False,True):
   _,w,c,snapshot=history(pre)
   for outcome in ['VC03.WIN','VC03.LOSS']:
    plan=mapping.outcome_plan(outcome,snapshot,(outcome+'.02',));counts[outcome,snapshot['rescue_credit_variant']]=len(plan['pages'])
    contest=vc.VerbalContests(vc.Catalog(fixture=H/'inputs/contest-owner/canonical-bindings.json'))
    contest.introduce('VC03',admitted=True);read_contest(contest)
    for pair in contest.catalog.eligible('VC03'):contest.present_lesson('VC03',pair);read_contest(contest)
    play(contest,outcome=='VC03.WIN')
    while contest.pending_text().record_id!=outcome:contest.acknowledge_text(contest.pending_text().receipt)
    first=present_outcome_unit(contest,snapshot,(h,d,a));self.assertTrue(first['complete']);self.assertEqual(first['unit'],outcome+'.01')
    pending=contest.pending_text();self.assertEqual(pending.unit_id,outcome+'.02');before=contest.snapshot()
    for prefix in range(len(plan['pages'])):
     shown=present_outcome_unit(contest,snapshot,(h,d,a),prefix)
     self.assertFalse(shown['complete']);self.assertEqual(len(shown['pages']),prefix);self.assertEqual(contest.snapshot(),before);self.assertEqual(contest.pending_text().receipt,pending.receipt);partial_cases+=1
    shown=present_outcome_unit(contest,snapshot,(h,d,a));self.assertTrue(shown['complete']);self.assertIsNone(contest.pending_text())
    self.assertFalse(plan['display_authority']);self.assertTrue(plan['requires_every_selected_page'])
  self.assertEqual(counts,{('VC03.WIN','ordinary'):1,('VC03.WIN','pre_engaged'):2,('VC03.LOSS','ordinary'):2,('VC03.LOSS','pre_engaged'):2})
  EVIDENCE['actual_pending_unit_partial_prefix_cases']=partial_cases
 def test_priority_invalid_history_and_mismatched_snapshot(self):
  self.assertEqual(mapping.rescue_variant(4,3),'ordinary')
  for values in [(0,0),(-1,4),(True,4),(4,'1'),(1073741824,0)]:
   with self.assertRaises(ValueError):mapping.rescue_variant(*values)
  for snapshot in [dict(rescue_credit_variant='ordinary',peg_ack_at=0,advance_peg_at=1),dict(rescue_credit_variant='pre_engaged',peg_ack_at=4,advance_peg_at=3),dict(rescue_credit_variant='ordinary',peg_ack_at=4)]:
   with self.assertRaises(ValueError):mapping.outcome_plan('VC03.WIN',snapshot)
 def test_real_both_history_priority_and_sincere_listener_gates(self):
  owner=repaired_gate();owner.set_peg(1);c=replace(C,gate=project_gate(owner));w=P11World();w.lift(c);owner.set_peg(0);released=replace(c,gate=project_gate(owner));w.request_peg(released);owner.set_peg(1);w.acknowledge_peg(c,w.pending_peg_request_id);w.release_catch(c);w.pull_handle(c);w.stage_display(c)
  self.assertGreater(w.advance_peg_at,0);self.assertGreater(w.peg_ack_at,0);self.assertEqual(raw_domain(w).call('p11RescueCreditVariant'),1)
  p=w.begin_presentation(c,'sincere');w.acknowledge_presentation(c,p.presentation_id,speech_unit_ids=RECORD_UNITS['P11.DIALOGUE.002'][:5]);before=w.save()
  for field,code in [('bunny_room','bunny_at_porch_required'),('felix_room','felix_required')]:
   away=replace(c,**{field:'L07_CONSERVATORY'});self.assertEqual(w.resume_presentation(away,'sincere').code,code);self.assertEqual(w.acknowledge_presentation(away,p.presentation_id,speech_unit_ids=RECORD_UNITS['P11.DIALOGUE.002'][5:]).code,code);self.assertEqual(w.save(),before)
 def test_variants_keep_ids_raw_spans_profiles_and_old_default_routes(self):
  for outcome in ['VC03.WIN','VC03.LOSS']:
   for variant in ['ordinary','pre_engaged']:
    rr=[r for r in M['variant_routes'] if (r['record_id'],r['variant_id'])==(outcome,variant)];uu=[r for r in M['variant_unit_routes'] if (r['record_id'],r['variant_id'])==(outcome,variant)]
    self.assertEqual(len(rr),1);self.assertEqual([u['line_id'] for u in uu],[outcome+'.01',outcome+'.02'])
    self.assertEqual(''.join(p['raw_text'] for p in [M['pages'][i] for u in uu for i in u['page_indices']]),''.join(s['source_text'] for s in rr[0]['segments']))
  import extend_dialogue as ext
  old=(H/'inputs/src/module982.sc').read_text();new=(H/'generated/module982.sc').read_text()
  for n in ext.ARRAYS:self.assertEqual(ext.read_array(new,n)[:len(ext.read_array(old,n))],ext.read_array(old,n))
 def test_all_variant_pages_mute_restore_replacement_and_late_generation(self):
  h,d,a,*_=setup()
  for muted in (0,1):
   a.p['voiceMuted']=muted
   for route in M['variant_unit_routes']:
    d.call('sdOpen',route['document_id'],0,0,0,a)
    for page in range(route['page_count']):
     if page:self.assertEqual(d.call('sdTurn',1,a),1)
     g=d.p['sdGeneration'];self.assertEqual(d.call('sdSpeak',a,g,page),0)
     d.call('sdDraw',0);self.assertEqual(d.call('sdPresented',g,page,a.p['token']),1);self.assertGreater(d.call('sdSpeak',a,g,page),0)
     starts=[v for n,v in h.vm.ktrace if n=='DoAudio' and v[0]==2];self.assertEqual(starts[-1][1],911 if muted else 923)
     d.call('sdAfterRestore',a);self.assertEqual(d.call('sdPresented',g,page,a.p['token']),0)
    g=d.p['sdGeneration'];d.call('sdOpen',1300,0,0,0,a);self.assertEqual(d.call('sdSpeak',a,g,0),0)
 def test_compiler_license_closure_and_full_typed_namespace(self):
  sha=lambda raw:hashlib.sha256(raw).hexdigest();self.assertEqual(sha((H/'tools/scicompile').read_bytes()),'608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e')
  manifest=json.loads((H/'inputs/COMPILER-SOURCE-MANIFEST.json').read_text())
  with zipfile.ZipFile(H/'inputs/compiler-source.zip') as z:
   files={n for n in z.namelist() if not n.endswith('/')};self.assertEqual(files,{'source/'+n for n in manifest['files']}|{'SOURCE-MANIFEST.json'});self.assertEqual(json.loads(z.read('SOURCE-MANIFEST.json')),manifest)
   for n,digest in manifest['files'].items():self.assertEqual(sha(z.read('source/'+n)),digest)
  self.assertTrue(list((H/'inputs/licenses').iterdir()))
  pin=json.loads((H/'inputs/typed-resource-inventory.json').read_text());typed={(r['type'],r['number']) for r in pin['typed']};self.assertNotIn((3,212),typed)
  self.assertEqual((pin['prior_audio_anchors'],pin['prior_actual_files']),(946,162))
if __name__=='__main__':unittest.main()
