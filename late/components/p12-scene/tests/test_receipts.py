"""Test-only display bridge and preserved earlier windows; no production host proof."""
from pathlib import Path
from dataclasses import replace
import unittest,json,sys,hashlib,itertools
H=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(H),str(H/'tests'),str(H/'inputs/model'),str(H/'inputs/model/tests')]
import mapping,extend_dialogue as ext
from source_tools import methods
from host import setup,frame,base
from source_factory import VM as SourceVM
from cakood.p12_model import P12World,SceneContext,CurrentRig,COURTYARD,PEOPLE,PREREQUISITES,RECORD_UNITS
from cakood.p10_model import TILE_IDS,ORDER
from test_verbal_contest import prepared,play,leave
M=json.loads((H/'generated/manifest.json').read_text());OLD=json.loads((H/'inputs/p11-manifest.json').read_text());EVIDENCE={}

def context():
 vc=prepared();play(vc,[False]*3);leave(vc)
 return SceneContext(COURTYARD,flags=PREREQUISITES,npc_locations=tuple((p,COURTYARD) for p in PEOPLE[1:]),rig=CurrentRig(COURTYARD,True,'MIC',True),contests=vc)

def started(c):
 w=P12World();w.start(c,dict(rack_id='cue_rack',location=COURTYARD,first_restored_serial=1,slots=list(TILE_IDS),words=list(ORDER)));return w

def repaired(c):
 w=started(c);a=replace(c,on_apron=True);p=w.begin_presentation(a,'self_view');w.acknowledge_presentation(a,p.presentation_id,record_id='P12.LOOK.003')
 w.release_catch(a);w.rotate_rack(c);w.order_cards(c,tuple(next(card for card in w.slots if w.words[card]==word) for word in ORDER));return w

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
  for doc in range(1400,1490):self.assertEqual(d.call('sdOpenWindow',doc,0,1,0,0,0,a),0)
  EVIDENCE['preserved_p08_unit_windows']=37
 def test_all_old_p11_variants_pcm_and_tables_are_exact(self):
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
     starts=[v for n,v in h.vm.ktrace if n=='DoAudio' and v[0]==2];self.assertEqual(starts[-1][1],911 if muted else 923)
     d.call('sdAfterRestore',a);self.assertEqual(d.call('sdPresented',g,pn,a.p['token']),0);cases+=1
  for v in OLD['speech']:
   for kind in ('audio','sync'):self.assertEqual(hashlib.sha256((H/'inputs/p11-speech'/v[kind+'_file']).read_bytes()).hexdigest(),v[kind+'_sha256'])
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
 def test_introduction_all_eight_pages_required_before_whole_source(self):
  c=context();w=repaired(c);request=w.begin_presentation(c,'introduction');before=w.save();h,d,a,*_=setup()
  plan=mapping.source_plan('introduction',record_id='P12.DIALOGUE.002');self.assertEqual(len(plan['pages']),8)
  ev=evidence(h,d,a,plan);self.assertFalse(ev.complete);self.assertEqual(w.audio_finished().code,'audio_has_no_authority');self.assertEqual(w.save(),before)
  for page in range(7):self.assertTrue(ev.paint(page));self.assertFalse(ev.complete)
  self.assertEqual(w.commit_introduction(c).code,'whole_introduction_required');self.assertEqual(w.save(),before)
  self.assertTrue(ev.paint(7));self.assertTrue(ev.complete)
  result=w.acknowledge_presentation(c,request.presentation_id,record_id='P12.DIALOGUE.002');self.assertEqual(result.code,'presentation_acknowledged')
  self.assertFalse(w.ready or w.welcome_cleared);w.commit_introduction(c);self.assertTrue(w.ready);self.assertFalse(w.welcome_cleared);self.assertEqual(w.finish_welcome(c).code,'cleanup_text_required')
  EVIDENCE['actual_emitted_introduction_pages_before_model_ack']=8
 def test_unit_prefix_is_not_full_source_and_rechecks_actors_pa(self):
  c=context();w=repaired(c);req=w.begin_presentation(c,'introduction');h,d,a,*_=setup();ids=RECORD_UNITS['P12.DIALOGUE.002']
  for uid in ids[:-1]:
   plan=mapping.source_plan('introduction',unit_ids=(uid,));ev=evidence(h,d,a,plan)
   for _,pn in plan['pages']:self.assertTrue(ev.paint(pn))
   self.assertTrue(ev.complete);w.acknowledge_presentation(c,req.presentation_id,speech_unit_ids=(uid,))
  self.assertFalse(w._complete('introduction'));self.assertEqual(w.commit_introduction(c).code,'whole_introduction_required');self.assertEqual(w.resume_presentation(c,'introduction').speech_unit_ids,(ids[-1],))
  saved=w.save();last=next(u for u in M['canonical_speech_units'] if u['line_id']==ids[-1]);speaker=last['speaker_id']
  if speaker!='jack':
   away=replace(c,npc_locations=tuple((p,'L01_LIVING_ROOM' if p==speaker else room) for p,room in c.npc_locations));self.assertEqual(w.acknowledge_presentation(away,req.presentation_id,speech_unit_ids=(ids[-1],)).code,'speaker_absent');self.assertEqual(w.save(),saved)
  broken=replace(c,rig=replace(c.rig,connected=False));self.assertEqual(w.acknowledge_presentation(broken,req.presentation_id,speech_unit_ids=(ids[-1],)).code,'microphone_unplugged');self.assertEqual(w.save(),saved)
  ev=evidence(h,d,a,mapping.source_plan('introduction',unit_ids=(ids[-1],)));self.assertTrue(ev.paint(0));self.assertTrue(ev.complete)
  w.acknowledge_presentation(c,req.presentation_id,speech_unit_ids=(ids[-1],));self.assertTrue(w._complete('introduction'));self.assertFalse(w.ready)
 def test_restore_replacement_retirement_never_accepts_old_request(self):
  c=context();w=repaired(c);req=w.begin_presentation(c,'introduction');h,d,a,*_=setup();plan=mapping.source_plan('introduction',unit_ids=(RECORD_UNITS['P12.DIALOGUE.002'][0],));ev=evidence(h,d,a,plan)
  self.assertFalse(ev.complete);self.assertTrue(ev.paint(0));self.assertTrue(ev.complete);oldgen=d.p['sdGeneration'];d.call('sdAfterRestore',a);self.assertFalse(ev.complete);self.assertEqual(d.call('sdSpeak',a,oldgen,0),0)
  restored=P12World.load(w.save(),context=c);self.assertEqual(restored.acknowledge_presentation(c,req.presentation_id,speech_unit_ids=(RECORD_UNITS['P12.DIALOGUE.002'][0],)).code,'stale_presentation');self.assertFalse(restored._complete('introduction'))
  fresh=restored.resume_presentation(c,'introduction');restored.cancel_presentation(fresh.presentation_id);self.assertEqual(restored.acknowledge_presentation(c,fresh.presentation_id,record_id='P12.DIALOGUE.002').code,'stale_presentation')
  ev=evidence(h,d,a,plan);self.assertTrue(ev.paint(0));h.call('dialogueOpen',1400);self.assertFalse(ev.complete)
 def test_audience_units_use_separate_original_profile_with_closed_mouth(self):
  h,d,a,*_=setup();aud=[u for u in M['unit_routes']+M['variant_unit_routes'] if u['page_count'] and u['canonical_speech_unit']['speaker_id']=='audience'];self.assertEqual(len(aud),7)
  self.assertEqual(set(M['silent_readers']),{'diagram'})
  for u in aud:
   self.assertGreater(u['speech_unit_id'],0);self.assertIn(u['line_id'],M['local_unit_keys']);p=M['pages'][u['first_page']]
   self.assertEqual(p['delivery'],'original_procedural_group_voice');self.assertEqual((p['audio_module'],p['speaker_number']),(924,0));self.assertIsNotNone(p['canonical_speech_unit'])
   self.assertEqual(d.call('sdOpen',u['document_id'],0,0,0,a),1);g=d.p['sdGeneration'];self.assertEqual(d.call('sdDraw',0),1);self.assertEqual(d.call('sdPresented',g,0,a.p['token']),1)
   self.assertEqual(d.p['sdPaintGeneration'],g)
   before=len([v for n,v in h.vm.ktrace if n=='DoAudio' and v[0]==2]);self.assertGreater(d.call('sdSpeak',a,g,0),0);self.assertEqual(len([v for n,v in h.vm.ktrace if n=='DoAudio' and v[0]==2]),before+1);self.assertEqual(a.p['speaker'],0);self.assertEqual(a.p['mouth'],0)
 def test_printed_diagram_raw_newline_complete_record_required(self):
  c=context();w=started(c);request=w.begin_presentation(c,'diagram');route=next(r for r in M['routes'] if r['record_id']=='P12.READ.001');self.assertEqual(route['source_text'],route['canonical_provenance']['text']);self.assertEqual(route['canonical_units'],[])
  plan=mapping.source_plan('diagram',record_id='P12.READ.001');h,d,a,*_=setup();ev=evidence(h,d,a,plan)
  for pn in range(len(plan['pages'])-1):self.assertTrue(ev.paint(pn));self.assertFalse(ev.complete)
  self.assertFalse(w._complete('diagram'));self.assertTrue(ev.paint(len(plan['pages'])-1));self.assertTrue(ev.complete);w.acknowledge_presentation(c,request.presentation_id,record_id='P12.READ.001');self.assertTrue(w._complete('diagram'))
  with self.assertRaises(ValueError):mapping.source_plan('diagram',unit_ids=('P12.READ.001',))
 def test_exact_198_file_compiler_closure_and_current_intro_source_preserved(self):
  root=H/'inputs/compiler-toolchain';manifest=json.loads((root/'SOURCE-MANIFEST.json').read_text());actual={str(p.relative_to(root/'source')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'source').rglob('*') if p.is_file()};self.assertEqual(len(actual),198);self.assertEqual(actual,manifest['files']);self.assertFalse(any('Prof-UIS' in n for n in actual))
  self.assertEqual((root/'scicompile').read_bytes(),(H/'tools/scicompile').read_bytes());self.assertEqual(hashlib.sha256((root/'scicompile').read_bytes()).hexdigest(),'608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e')
  for name in ('sdOpenWindow','sdWindowValue'):
   self.assertEqual(methods((H/'inputs/current-p08-intro/src/module982.sc').read_text())[name],methods((H/'generated/window-src/module982.sc').read_text())[name])
  self.assertTrue((H/'inputs/current-p08-intro/src/module989.sc').is_file());self.assertNotIn('989',json.loads((H/'build/coherent/ABI-MAPPINGS.json').read_text())['modules'])
if __name__=='__main__':unittest.main()
