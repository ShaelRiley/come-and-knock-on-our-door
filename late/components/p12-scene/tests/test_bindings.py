"""All observed physical permutations; templates are never player-visible text."""
from pathlib import Path
import sys,json,itertools,copy,unittest
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests')]
import mapping,generate
from scene_vm import VM as RawVM
from host import setup
from test_receipts import DisplayEvidence
M=json.loads((H/'generated/manifest.json').read_text());A=json.loads((H/'inputs/domain/schema.json').read_text());EVIDENCE={}

def domain(order,source):
 d=RawVM(H/'inputs/domain/src/module994.sc','P12State');d.call('p12Init')
 def context(apron,epoch):return d.call('p12Context',4,apron,1,1,1,1,4,1,1,1,0,1,4,4,4,4,4,4,4,epoch)
 assert context(0,1)==1
 # Handoff swaps the first two physical cards; provide the inverse observed order.
 d.call('p12Handoff',410,4,0,1,48,49,50,order[1],order[0],order[2])
 assert d.p['p12Code']==A['codes']['rack_rehung'];assert context(1,2)==1
 d.call('p12View',1 if source=='audience_view' else 0)
 assert d.p['p12Code']==A['codes']['presentation_pending']
 return d,context

def snapshot(d,source):
 sid=A['sources'][source]
 return dict(source=source,source_start=d.call('p12SerialHi',sid+7)*32768+d.call('p12SerialLo',sid+7),epoch=d.p['p12Epoch'],word_ids=[d.call('p12VisibleWord',i) for i in range(3)])

class BindingTests(unittest.TestCase):
 def test_all_six_observed_permutations_both_sources_full_and_unit(self):
  h,scene,a,*_=setup();cases=0
  for order,source,unit in itertools.product(itertools.permutations((1,2,3)),('audience_view','self_view'),(False,True)):
   d,ctx=domain(order,source);s=snapshot(d,source);self.assertEqual(s['word_ids'],list(order));rid=M['source_bindings'][source];uid=rid+'.01'
   plan=mapping.source_plan(source,unit_ids=(uid,),binding_snapshot=s) if unit else mapping.source_plan(source,record_id=rid,binding_snapshot=s)
   self.assertTrue(mapping.binding_is_current(plan,s));self.assertFalse(plan['display_authority'] or plan['fallback']);self.assertEqual(plan['bindings']['visible_cue_order'],', '.join(next(k for k,v in A['words'].items() if v==n) for n in order))
   before=copy.deepcopy(d.p);ev=DisplayEvidence(h,scene,a,plan['documents'][0],[tuple(p) for p in plan['pages']]);self.assertFalse(ev.complete);self.assertEqual(d.p,before)
   for doc,page in plan['pages']:self.assertTrue(ev.paint(page))
   self.assertTrue(ev.complete);self.assertEqual(d.p,before);self.assertNotIn('{',str(scene.arrays['sdTextBuffer']));self.assertTrue(str(scene.arrays['sdTextBuffer']).startswith(plan['bindings']['visible_cue_order']))
   sid=A['sources'][source];hi,lo=divmod(s['source_start'],32768)
   self.assertTrue(mapping.binding_is_current(plan,snapshot(d,source)))
   d.call('p12Acknowledge',sid,hi,lo,s['epoch'],*plan['domain_form']);self.assertEqual(d.p['p12Code'],A['codes']['presentation_acknowledged']);self.assertEqual(d.call('p12Count',sid),1);cases+=1
  EVIDENCE['observed_binding_source_emitted_cases']=cases
 def test_invalid_missing_or_retired_binding_cannot_select_or_acknowledge(self):
  d,ctx=domain((2,1,3),'self_view');s=snapshot(d,'self_view');plan=mapping.binding_plan('self_view',s);before=copy.deepcopy(d.p)
  for bad in (None,{},dict(s,word_ids=[1,1,3]),dict(s,word_ids=[True,2,3]),dict(s,word_ids=[0,2,3]),dict(s,word_ids=[1,2]),dict(s,source='audience_view'),dict(s,source_start=0),dict(s,epoch=True)):
   with self.assertRaises(ValueError):mapping.binding_plan('self_view',bad)
   self.assertFalse(mapping.binding_is_current(plan,bad))
  self.assertEqual(d.p,before)
  for source in ('audience_view','self_view'):
   rid=M['source_bindings'][source]
   with self.assertRaises(ValueError):mapping.source_plan(source,record_id=rid)
   with self.assertRaises(ValueError):mapping.plan(lines=(M['local_line_keys'][rid],))
   with self.assertRaises(ValueError):mapping.plan(units=(M['local_unit_keys'][rid+'.01'],))
  ctx(1,3);self.assertFalse(mapping.binding_is_current(plan,snapshot(d,'self_view')))
  hi,lo=divmod(s['source_start'],32768);d.call('p12Acknowledge',A['sources']['self_view'],hi,lo,s['epoch'],*plan['domain_form']);self.assertEqual(d.p['p12Code'],A['codes']['stale_presentation']);self.assertEqual(d.call('p12Count',A['sources']['self_view']),0)
  self.assertFalse(mapping.binding_is_current(plan,dict(s,word_ids=[1,2,3])))
 def test_canonical_templates_and_exact_expansions_all_raw_spans(self):
  self.assertEqual(M['dynamic_records'],['P12.DIALOGUE.001','P12.LOOK.003']);self.assertEqual(len(M['variant_routes']),12);self.assertEqual(len(M['variant_unit_routes']),12)
  h,d,a,*_=setup()
  for doc in M['reserved_template_documents']:
   self.assertEqual(d.call('sdPageCount',doc),0);self.assertEqual(d.call('sdOpen',doc,0,0,0,a),0)
  for r in M['variant_routes']+M['variant_unit_routes']:
   expected=r['source_template'].format(**r['predicate']['bindings']);self.assertEqual(r['source_text'],expected);self.assertEqual(''.join(M['pages'][i]['raw_text'] for i in r['page_indices']),expected)
   for i in r['page_indices']:
    p=M['pages'][i];self.assertEqual(p['canonical_speech_unit']['text'],r['source_template']);self.assertEqual(p['canonical_speech_unit']['line_id'],r['record_id']+'.01');self.assertEqual(p['binding'],r['predicate']);self.assertNotIn('{',p['raw_text']);self.assertNotIn('}',p['text'])
  for s in M['speech']:self.assertNotIn('{',s['raw_text']);self.assertNotIn('}',s['raw_text'])
  bank=(H/'generated/213.text.bin').read_bytes();self.assertNotIn(b'{',bank);self.assertNotIn(b'}',bank)
 def test_caption_paginator_preserves_raw_newline_evidence(self):
  raw='FIRST LINE\nSECOND LINE\nTHIRD LINE\nFOURTH LINE';pages=generate.paginate(raw)
  self.assertEqual(''.join(p['raw_text'] for p in pages),raw);self.assertEqual([p['text'] for p in pages],['FIRST LINE\nSECOND LINE\nTHIRD LINE','FOURTH LINE'])
if __name__=='__main__':unittest.main()
