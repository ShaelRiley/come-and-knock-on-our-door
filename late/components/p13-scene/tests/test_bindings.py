"""Actual source/emitted failed-condition queries and exact label-bound captions."""
from pathlib import Path
import sys,json,itertools,copy,unittest
from dataclasses import replace
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests')]
import mapping,generate
from host import setup
from test_receipts import DisplayEvidence
from domain_bridge import domain,project,seated,display_ready,A
from cakood.p12_model import KITCHEN,SIDE
from test_late_campaign_models import actors
M=json.loads((H/'generated/manifest.json').read_text());EVIDENCE={}
class BindingTests(unittest.TestCase):
 def test_every_condition_projection_actual_source_and_emitted_failures(self):
  h,scene,a,*_=setup();cases=0;expected_labels=set()
  for kind,cue,bits in itertools.product(('source','emitted'),(1,2),itertools.product((False,True),repeat=5)):
   w,c=seated() if cue==1 else display_ready()
   c=replace(c,buffet_at_hatch=bits[0],hatch_visible=bits[1],lane_clear=bits[2],footprint_clear=bits[3],display_concealed=bits[4])
   c=actors(replace(c,room=KITCHEN),bunny=KITCHEN) if cue==1 else actors(replace(c,room=SIDE),felix=SIDE,vivian=SIDE)
   d=domain(kind,w,c);code=d.call('p13DeliverPot' if cue==1 else 'p13DeliverDisplay',2 if cue==1 else 3)
   snap=mapping.capture_blocked_snapshot(d,cue);blocked=not(bits[0] and bits[1]) if cue==1 else not(bits[2] and bits[3] and bits[4])
   if cue==2 and not bits[0]:
    self.assertEqual(code,A['codes']['invalid_context'])
    with self.assertRaises(ValueError):mapping.binding_plan(snap)
    continue
   if not blocked:
    self.assertEqual(snap['blocked_label_key'],0)
    with self.assertRaises(ValueError):mapping.binding_plan(snap)
    continue
   self.assertEqual(code,A['codes']['buffet_or_hatch_blocked' if cue==1 else 'display_lane_or_footprint_blocked']);before=copy.deepcopy(d.p)
   for unit in (False,True):
    plan=mapping.binding_plan(snap,unit);expected_labels.add(plan['label_record_id']);self.assertTrue(mapping.binding_is_current(plan,snap));self.assertFalse(plan['display_authority'] or plan['source_receipt_authority'] or plan['voice_eligibility'] or plan['fallback'])
    ev=DisplayEvidence(h,scene,a,plan['documents'][0],[tuple(p) for p in plan['pages']]);self.assertFalse(ev.complete)
    for doc,page in plan['pages']:self.assertTrue(ev.paint(page))
    self.assertTrue(ev.complete);self.assertEqual(d.p,before);self.assertTrue(str(scene.arrays['sdTextBuffer']).startswith(generate.norm(plan['bindings']['blocked_place_name'])));self.assertNotIn('{',str(scene.arrays['sdTextBuffer']));cases+=1
  self.assertEqual(expected_labels,{'P08.LABEL.001','P08.LABEL.002','P08.LABEL.004','P08.LABEL.006'});EVIDENCE['actual_failed_layout_record_unit_paints']=cases
 def test_missing_forged_clear_foreign_or_stale_observations_fail_closed(self):
  w,c=seated();c=actors(replace(c,room=KITCHEN,buffet_at_hatch=False),bunny=KITCHEN);d=domain('emitted',w,c);d.call('p13DeliverPot',2);s=mapping.capture_blocked_snapshot(d,1);plan=mapping.binding_plan(s)
  for bad in (None,{},dict(s,cue=True),dict(s,cue=3),dict(s,status_code=A['codes']['pot_delivered']),dict(s,epoch=0),dict(s,revision=True),dict(s,line_ids=[38,38]),dict(s,blocked_label_key=49),dict(s,layout=dict(s['layout'],BuffetAtHatch=True)),dict(s,layout=dict(s['layout'],BuffetAtHatch=1))):
   with self.assertRaises(ValueError):mapping.binding_plan(bad)
   self.assertFalse(mapping.binding_is_current(plan,bad))
  for changed in (dict(s,epoch=2),dict(s,revision=s['revision']+1)):
   self.assertFalse(mapping.binding_is_current(plan,changed))
  project(d,c,2);self.assertFalse(mapping.binding_is_current(plan,mapping.capture_blocked_snapshot(d,1)))
  for cue in (0,3,True,'SERVE'):
   with self.assertRaises(ValueError):mapping.capture_blocked_snapshot(d,cue)
  with self.assertRaises(ValueError):mapping.plan(lines=(38,))
  with self.assertRaises(ValueError):mapping.plan(units=(36,))
  with self.assertRaises(ValueError):mapping.source_plan('blocked_layout',record_id='P13.FAILURE.009')
 def test_exact_canonical_templates_label_provenance_and_raw_spans(self):
  self.assertEqual(M['dynamic_records'],['P13.FAILURE.009']);self.assertEqual(len(M['variant_routes']),4);self.assertEqual(len(M['variant_unit_routes']),4)
  h,d,a,*_=setup()
  for doc in M['reserved_template_documents']:self.assertEqual(d.call('sdPageCount',doc),0);self.assertEqual(d.call('sdOpen',doc,0,0,0,a),0)
  for r in M['variant_routes']+M['variant_unit_routes']:
   expected=r['source_template'].format(**r['predicate']['bindings']);self.assertEqual(r['source_text'],expected);self.assertEqual(''.join(M['pages'][i]['raw_text'] for i in r['page_indices']),expected)
   label=r['predicate']['label_provenance'];self.assertEqual(r['predicate']['bindings']['blocked_place_name'],label['text']);self.assertEqual(label,A['canonical_records'][label['id']])
   for i in r['page_indices']:
    p=M['pages'][i];self.assertEqual(p['canonical_speech_unit']['text'],r['source_template']);self.assertEqual(p['canonical_speech_unit']['line_id'],'P13.FAILURE.009.01');self.assertEqual(p['binding'],r['predicate']);self.assertNotIn('{',p['raw_text'])
  bank=(H/'generated/214.text.bin').read_bytes();self.assertNotIn(b'{',bank);self.assertNotIn(b'}',bank)
  for s in M['speech']:self.assertNotIn('{',s['raw_text']);self.assertNotIn('}',s['raw_text'])
 def test_supporting_local_label_ids_reuse_exact_prior_documents(self):
  h,d,a,*_=setup();self.assertEqual([(r['local_line_key'],r['document_id']) for r in M['supporting_labels']],[(46,974),(47,976),(48,980),(49,984)])
  for r in M['supporting_labels']:
   self.assertEqual(mapping.plan(lines=(r['local_line_key'],))['documents'],[r['document_id']]);self.assertEqual(d.call('sdOpen',r['document_id'],0,0,0,a),1);d.call('sdDraw',0);self.assertEqual(str(d.arrays['sdTextBuffer']),generate.norm(r['canonical_provenance']['text']))
 def test_caption_paginator_preserves_raw_newline_evidence(self):
  raw='FIRST LINE\nSECOND LINE\nTHIRD LINE\nFOURTH LINE';pages=generate.paginate(raw);self.assertEqual(''.join(p['raw_text'] for p in pages),raw);self.assertEqual([p['text'] for p in pages],['FIRST LINE\nSECOND LINE\nTHIRD LINE','FOURTH LINE'])
if __name__=='__main__':unittest.main()
