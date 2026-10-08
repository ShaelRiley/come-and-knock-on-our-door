"""Finite scene receipts, exact prior windows and original audio preservation."""
from pathlib import Path
import unittest,json,sys,hashlib,itertools
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests'),str(H/'inputs/model'),str(H/'inputs/model/tests')]
import mapping,extend_dialogue as ext
from source_tools import methods
from host import setup,frame,base
from source_factory import VM as SourceVM
M=json.loads((H/'generated/manifest.json').read_text());OLD=json.loads((H/'inputs/p12-manifest.json').read_text());EVIDENCE={}
class DisplayEvidence:
 """Model only: authenticates every modeled emitted paint against an exact lease.
 It does not establish a native actor, screenshot, PA, save or host receipt.
 """
 def __init__(self,h,d,a,document,pages):
  self.h,self.d,self.a=h,d,a;self.document=document;self.required=tuple(pages);self.seen=[]
  assert h.call('dialogueOpen',document)==1
  self.generation=d.p['sdGeneration'];self.token=a.p['token']
 def paint(self,page):
  if self.d.p['sdGeneration']!=self.generation or self.a.p['token']!=self.token:return False
  if self.d.p['sdPage']!=page:self.h.call('uiTurnPage',page-self.d.p['sdPage']);self.generation=self.d.p['sdGeneration'];self.token=self.a.p['token']
  before=sum(n=='Graph' and v[0]==12 for n,v in self.h.vm.ktrace);frame(self.h)
  if self.h.call('scenePageIdentity')!=1:return False
  if self.d.p['sdDocument']!=self.document or self.d.p['sdPage']!=page:return False
  if sum(n=='Graph' and v[0]==12 for n,v in self.h.vm.ktrace)<=before:return False
  pair=(self.document,page)
  if pair not in self.required:return False
  if pair not in self.seen:self.seen.append(pair)
  self.token=self.a.p['token']
  return True
 @property
 def complete(self):return tuple(self.seen)==self.required and self.d.p['sdGeneration']==self.generation and self.a.p['token']==self.token

def evidence(h,d,a,plan):return DisplayEvidence(h,d,a,plan['pages'][0][0],[tuple(p) for p in plan['pages']])

class ReceiptTests(unittest.TestCase):
 def test_all37_prior_p08_unit_windows_and_new_rejection(self):
  B=H/'build/window';vm=base.HostVM(checkpoint=B/'verification-checkpoint',build=B,budget=100000000);d=vm.objects['sceneDialogue'];a=vm.objects['presentationAudio']
  m=json.loads((H/'inputs/p08/generated/line-document-unit-map.json').read_text());windows=[u for u in m['output_windows'] if u['kind']=='unit_only'];self.assertEqual(len(windows),37)
  for u in windows:
   first,count=u['first_record_page'],u['page_count'];self.assertEqual(d.call('sdOpenWindow',u['document_id'],first,count,0,0,0,a),1)
   self.assertEqual(d.p['sdPage'],first);self.assertEqual(d.call('sdTurn',-1,a),0)
   for page in range(first,first+count):
    if page>first:self.assertEqual(d.call('sdTurn',1,a),1)
    self.assertEqual(d.call('sdLoad'),1);self.assertEqual(d.call('sdDraw',0),1)
   self.assertEqual(d.call('sdTurn',1,a),0);self.assertEqual(d.call('sdAfterRestore',a),1);self.assertEqual(d.call('sdWindowValue',2),1)
  for doc in range(1500,1593):self.assertEqual(d.call('sdOpenWindow',doc,0,1,0,0,0,a),0)
  EVIDENCE['preserved_p08_unit_windows']=37
 def test_all_old_p12_variants_pcm_and_tables_are_exact(self):
  old=(H/'inputs/src/module982.sc').read_text();new=(H/'generated/module982.sc').read_text()
  for n in ext.ARRAYS:self.assertEqual(ext.read_array(new,n)[:len(ext.read_array(old,n))],ext.read_array(old,n))
  h,d,a,*_=setup();cases=0
  for route in OLD['variant_routes']+OLD['variant_unit_routes']:
   for muted in (0,1):
    a.p['voiceMuted']=muted;self.assertEqual(d.call('sdOpen',route['document_id'],0,0,0,a),1)
    for pn,i in enumerate(route['page_indices']):
     if pn:self.assertEqual(d.call('sdTurn',1,a),1)
     g=d.p['sdGeneration'];self.assertEqual(d.call('sdSpeak',a,g,pn),0);self.assertEqual(d.call('sdDraw',0),1)
     self.assertEqual(str(d.arrays['sdTextBuffer']),OLD['pages'][i]['text']);self.assertEqual(d.call('sdPresented',g,pn,a.p['token']),1);self.assertGreater(d.call('sdSpeak',a,g,pn),0)
     starts=[v for n,v in h.vm.ktrace if n=='DoAudio' and v[0]==2];self.assertEqual(starts[-1][1],911 if muted else 924)
     d.call('sdAfterRestore',a);self.assertEqual(d.call('sdPresented',g,pn,a.p['token']),0);cases+=1
  for v in OLD['speech']:
   for kind in ('audio','sync'):self.assertEqual(hashlib.sha256((H/'inputs/p12-speech'/v[kind+'_file']).read_bytes()).hexdigest(),v[kind+'_sha256'])
  EVIDENCE['old_variant_pages_mute_restore']=cases
 def test_every_partial_old_unit_page_prefix_is_incomplete(self):
  h,d,a,*_=setup();cases=0
  for route in OLD['variant_unit_routes']:
   expected=[(route['document_id'],n) for n in range(route['page_count'])]
   for prefix in range(route['page_count']):
    ev=DisplayEvidence(h,d,a,route['document_id'],expected)
    for page in range(prefix):self.assertTrue(ev.paint(page))
    self.assertFalse(ev.complete);g=d.p['sdGeneration'];d.call('sdClose',a);self.assertFalse(ev.complete);self.assertEqual(d.call('sdPresented',g,d.p['sdPage'],a.p['token']),0);cases+=1
  EVIDENCE['partial_old_unit_prefixes']=cases
 def test_exact_198_file_compiler_closure_and_current_intro_source_preserved(self):
  root=H/'inputs/compiler-toolchain';manifest=json.loads((root/'SOURCE-MANIFEST.json').read_text());actual={str(p.relative_to(root/'source')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'source').rglob('*') if p.is_file()};self.assertEqual(len(actual),198);self.assertEqual(actual,manifest['files']);self.assertFalse(any('Prof-UIS' in n for n in actual))
  self.assertEqual((root/'scicompile').read_bytes(),(H/'tools/scicompile').read_bytes());self.assertEqual(hashlib.sha256((root/'scicompile').read_bytes()).hexdigest(),'608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e')
  for name in ('sdOpenWindow','sdWindowValue'):
   self.assertEqual(methods((H/'inputs/current-p08-intro/src/module982.sc').read_text())[name],methods((H/'generated/window-src/module982.sc').read_text())[name])
  self.assertTrue((H/'inputs/current-p08-intro/src/module989.sc').is_file());self.assertNotIn('989',json.loads((H/'build/coherent/ABI-MAPPINGS.json').read_text())['modules'])

if __name__=='__main__':unittest.main()

class P13ReceiptTests(unittest.TestCase):
 def test_reveal_all_pages_and_each_unit_prefix_source_emitted(self):
  from domain_bridge import reveal_ready,domain,A
  h,d,a,*_=setup();count=0
  for kind in ('source','emitted'):
   w,c=reveal_ready();owner=domain(kind,w,c);sid=A['sources']['reveal'];self.assertEqual(owner.call('p13Begin',sid),A['codes']['presentation_pending'])
   hi,lo=owner.call('p13SerialHi',sid+18),owner.call('p13SerialLo',sid+18);epoch=owner.p['p13Epoch'];units=[u['line_id'] for u in M['unit_routes'] if u['record_id']=='P13.DIALOGUE.005']
   self.assertEqual(len(units),5)
   persisted={n:owner.p[n] for n in A['persisted_properties']};owner.call('p13AudioFinished');self.assertEqual({n:owner.p[n] for n in A['persisted_properties']},persisted)
   for uid in units:
    plan=mapping.source_plan('reveal',unit_ids=(uid,));ev=evidence(h,d,a,plan);self.assertFalse(ev.complete)
    for doc,page in plan['pages']:self.assertTrue(ev.paint(page))
    self.assertTrue(ev.complete);self.assertEqual(owner.call('p13Acknowledge',sid,hi,lo,epoch,*plan['domain_form']),A['codes']['presentation_acknowledged']);count+=len(plan['pages'])
    self.assertEqual(owner.call('p13Complete',sid),int(uid==units[-1]));self.assertEqual(owner.call('p13ShowComplete'),0)
   self.assertEqual(owner.call('p13PullShow'),A['codes']['show_complete'])
  EVIDENCE['reveal_unit_source_emitted_painted_pages']=count
 def test_whole_reveal_observation_needs_every_page_without_skip_receipt(self):
  h,d,a,*_=setup();plan=mapping.source_plan('reveal',record_id='P13.DIALOGUE.005');self.assertEqual(len(plan['pages']),5)
  for prefix in range(5):
   ev=evidence(h,d,a,plan)
   for page in range(prefix):self.assertTrue(ev.paint(page))
   self.assertFalse(ev.complete);d.p['sdPage']=4;d.call('sdLoad');self.assertFalse(ev.complete);d.call('sdAfterRestore',a);self.assertFalse(ev.complete)
  ev=evidence(h,d,a,plan)
  for page in range(5):self.assertTrue(ev.paint(page))
  self.assertTrue(ev.complete);h.call('dialogueOpen',1500);self.assertFalse(ev.complete)
 def test_actor_absence_and_changed_context_retire_receipts_not_voice_identity(self):
  from domain_bridge import reveal_ready,domain,project,A
  from dataclasses import replace
  from cakood.p12_model import LIVING
  from test_late_campaign_models import actors
  for kind in ('source','emitted'):
   w,c=reveal_ready();owner=domain(kind,w,c);sid=A['sources']['reveal'];owner.call('p13Begin',sid);hi,lo=owner.call('p13SerialHi',sid+18),owner.call('p13SerialLo',sid+18)
   plan=mapping.source_plan('reveal',unit_ids=('P13.DIALOGUE.005.01',));self.assertFalse(plan['display_authority']);self.assertEqual(M['canonical_speech_units'][23]['speaker_id'],'rita')
   away=actors(c,rita=LIVING);project(owner,away,2);before={n:owner.p[n] for n in A['persisted_properties']}
   self.assertEqual(owner.call('p13Begin',sid),A['codes']['speaker_absent']);self.assertEqual(owner.call('p13Acknowledge',sid,hi,lo,1,*plan['domain_form']),A['codes']['stale_presentation']);self.assertEqual({n:owner.p[n] for n in A['persisted_properties']},before)
   project(owner,c,3);self.assertEqual(owner.call('p13Acknowledge',sid,hi,lo,1,*plan['domain_form']),A['codes']['stale_presentation'])
 def test_printed_previews_are_silent_complete_record_receipts(self):
  from domain_bridge import started,domain,A
  h,d,a,*_=setup()
  for kind in ('source','emitted'):
   for source in ('serve_preview','show_preview','toast_preview','program'):
    w,c=started();owner=domain(kind,w,c);sid=A['sources'][source];self.assertEqual(owner.call('p13Begin',sid),A['codes']['presentation_pending'])
    plan=mapping.source_plan(source,record_id=M['source_bindings'][source]);ev=evidence(h,d,a,plan)
    for doc,page in plan['pages']:self.assertTrue(ev.paint(page));self.assertEqual(d.p['sdVoice'],0)
    self.assertTrue(ev.complete);hi,lo=owner.call('p13SerialHi',sid+18),owner.call('p13SerialLo',sid+18)
    self.assertEqual(owner.call('p13Acknowledge',sid,hi,lo,1,*plan['domain_form']),A['codes']['presentation_acknowledged']);self.assertEqual(owner.call('p13Complete',sid),1)
    with self.assertRaises(ValueError):mapping.source_plan(source,unit_ids=(M['source_bindings'][source],))
