from pathlib import Path
import unittest,sys,json,re,hashlib,struct,copy
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests'),str(H/'tools'),str(H/'inputs/model'),str(H/'inputs/model/tests')]
import mapping,caption_layout
M=json.loads((H/'generated/manifest.json').read_text());F=json.loads((H/'inputs/canonical-bindings.json').read_text());A=json.loads((H/'inputs/reference-schema.json').read_text())
class ExportTests(unittest.TestCase):
 def test_all125_records43units_and_every_raw_span(self):
  self.assertEqual(M['canonical_records'],F['records']);self.assertEqual(M['canonical_speech_units'],F['speech_units'])
  for r in M['routes']:
   self.assertEqual(r['canonical_provenance'],next(v for v in F['records'] if v['id']==r['record_id']))
   for i,s in enumerate(r['segments']):
    pages=[M['pages'][j] for j in r['page_indices'] if M['pages'][j]['segment_index']==i]
    if r['binding_required']:self.assertEqual(pages,[]);continue
    self.assertEqual(''.join(p['raw_text'] for p in pages),s['source_text'])
    for p in pages:self.assertEqual(s['source_text'][slice(*p['source_char_range'])],p['raw_text']);self.assertEqual(s['source_text'].encode()[slice(*p['source_utf8_byte_range'])],p['raw_text'].encode())
  for u in M['unit_routes']:
   if not u['binding_required']:self.assertEqual(''.join(M['pages'][i]['raw_text'] for i in u['page_indices']),u['canonical_speech_unit']['text'])
 def test_exact_credit_url_bytes_and_case_across_wraps(self):
  count=0
  for r in M['routes']:
   if r['kind']!='credit':continue
   pages=[M['pages'][i] for i in r['page_indices']]
   for s in r['segments']:
    for url in re.finditer(r'https?://\S+',s['source_text']):
     chunks=[c for p in pages for c in p['display_chunks'] if url.start()<=c['source_char_range'][0]<url.end()]
     self.assertEqual(''.join(c['text'] for c in chunks),url.group());count+=1
  self.assertGreaterEqual(count,29)
 def test_no_template_open_and_static_audio_boundaries(self):
  self.assertEqual(len(M['reserved_template_documents']),4);self.assertEqual(len(M['speech']),44)
  self.assertFalse(any('{' in p['raw_text'] or '}' in p['raw_text'] for p in M['pages']))
  self.assertFalse(any(v['line_id']=='P14.READ.001.01' for v in M['speech']))
  self.assertTrue(all(v['speaker_id'] in {'jack','bunny','frankie','milo','vivian','rita','felix','stringer'} for v in M['speech']))
 def test_eight_equal_writer_blocks_and_exact_credits(self):
  ids=[r['id'] for r in F['records'] if r['id'].startswith('END.CREDIT.WRITERS.') and not r['id'].endswith('HEADER')];self.assertEqual(len(ids),8)
  self.assertEqual(M['credit_order'],A['credit_order']);self.assertEqual(len(M['credit_order']),26);self.assertEqual(len(M['asset_credits']),33)
  self.assertEqual({r['record_id'] for r in M['routes'] if r['kind']=='credit'},set(M['credit_order'])|set(M['asset_credits']))
 def test_date_invalid_glyph_shape_and_no_default(self):
  for s in ['',None,False,5,'|','A\nB','é','日','Q'*81,'\x7f']:
   with self.assertRaises(ValueError):caption_layout.admit_date(s)
  for s in ['Q'*80,' '*80,'MiXeD'] :self.assertEqual(caption_layout.admit_date(s),s)
 def test_font_old_bytes_original_uppercase_and_all_printable(self):
  old=(H/'inputs/p08/inputs/resources/000.font.bin').read_bytes();new=(H/'generated/001.font.bin').read_bytes()
  self.assertEqual(hashlib.sha256(old).hexdigest(),'2b31daed762755f6b96baba9dbe0cec65b70d029c017fe6b9295240c0c7c7fbc')
  def glyph(b,c):p=struct.unpack_from('<H',b,6+c*2)[0];return b[p:p+10]
  for c in range(65,91):self.assertEqual(glyph(old,c),glyph(new,c));self.assertNotEqual(glyph(new,c),glyph(new,c+32))
  for c in range(33,127):self.assertNotEqual(glyph(new,c)[2:],bytes(8))
 def test_text215_bank_offsets_all_pages_fit(self):
  raw=(H/'generated/215.text.bin').read_bytes()
  for p in M['pages']:
   self.assertEqual(raw[slice(*p['text_bank_byte_range'])],p['text'].encode()+b'\0');self.assertLessEqual(p['bytes_with_nul'],153);self.assertLessEqual(len(p['text'].splitlines()),3);self.assertTrue(all(len(s)<=50 for s in p['text'].splitlines()))
 def test_all16_notebook_actual_retained_owner_masks(self):
  from test_late_campaign_models import contests
  for mask in range(16):
   owner=contests(wins=tuple(c for i,c in enumerate(A['contest_ids']) if mask&(1<<i)))
   for gate in (False,True):
    plan=mapping.notebook_plan(owner,gate);self.assertEqual(plan['snapshot']['won_count'],mask.bit_count());self.assertTrue(mapping.notebook_is_current(plan,owner));self.assertFalse(plan['display_authority'])
   plan=mapping.notebook_plan(owner);saved=owner.save_with_evidence();owner.restore_with_evidence(saved,owner_generation=owner.owner_generation+1);self.assertFalse(mapping.notebook_is_current(plan,owner))
 def test_selected_credit_files_required_and_no_download(self):
  self.assertEqual(mapping.credit_selection([],H)['credit_ids'],M['credit_order'])
  for row in [[{'path':'absent','sha256':'0'*64,'source_url':next(iter(M['asset_credits'].values()))}],{},[{'path':'../x','sha256':'0'*64,'source_url':'https://unknown'}]]:
   with self.assertRaises(ValueError):mapping.credit_selection(row,H)
 def test_source_unit_plans_do_not_conflate(self):
  for source,rid in M['source_bindings'].items():
   if source.startswith('credit:') or source=='readback':continue
   plan=mapping.source_plan(source,record_id=rid);self.assertTrue(plan['pages']);self.assertEqual(plan['domain_form'],[A['line_ids'][rid],0,0])
   r=next(r for r in M['routes'] if r['record_id']==rid)
   for u in r['canonical_units']:
    plan=mapping.source_plan(source,unit_ids=[u]);self.assertEqual(plan['domain_form'],[0,A['speech_unit_ids'][u],A['speech_unit_ids'][u]])
    with self.assertRaises(ValueError):mapping.source_plan(source,record_id=rid,unit_ids=[u])
 def test_exact_new_typed_namespace_includes_font(self):
  from resource_codec import decode
  oldroot=H/'frozen-candidates/p13-scene-reconstruction/generated/fixture-game';newroot=H/'generated/fixture-game'
  old=decode((oldroot/'resource.map').read_bytes(),(oldroot/'resource.000').read_bytes());new=decode((newroot/'resource.map').read_bytes(),(newroot/'resource.000').read_bytes());added=set(new)-set(old)
  self.assertEqual(added,{(2,999),(17,999),(3,215),(3,245),(7,1)});report=json.loads((H/'evidence/compile-proof.json').read_text());self.assertEqual(report['new_resources'],[list(k) for k in sorted(added)]);self.assertEqual(report['typed_resources'],len(new));self.assertEqual(new[7,0],old[7,0]);self.assertEqual(new[7,1],(H/'generated/001.font.bin').read_bytes())
 def test_compiler_exact198_source_closure(self):
  root=H/'inputs/compiler-toolchain';expected=json.loads((root/'SOURCE-MANIFEST.json').read_text())['files'];actual={str(p.relative_to(root/'source')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'source').rglob('*') if p.is_file()};self.assertEqual(actual,expected);self.assertEqual(len(actual),198)
if __name__=='__main__':unittest.main()
