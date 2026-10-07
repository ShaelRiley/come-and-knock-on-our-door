"""Current predecessor, actual emitted routing/rendering and fail-closed regression gates."""
from pathlib import Path
import unittest,json,sys,copy
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H));sys.path.insert(0,str(H/'tools'));sys.path.insert(0,str(H/'tests'));sys.dont_write_bytecode=True
import extend_dialogue as ext
from source_tools import methods
from host import setup,base,frame
from guard import require
M=json.loads((H/'generated/manifest.json').read_text());C=json.loads((H/'generated/extension-contract.json').read_text());EVIDENCE={}
PROPS=['sdEntry','sdLineKey','sdPart','sdPartCount','sdSpeaker','sdVoice','sdHeader','sdBytes']
class CurrentTests(unittest.TestCase):
 def test_every1191_emitted_page_and_all1140_route_counts(self):
  h,d,a,p,q,g=setup();t=C['arrays'];seen=set();new={1138+p['page_index']:p for p in M['pages']}
  for doc in range(1140):
   start,count=t['sdStarts'][doc],t['sdCounts'][doc]
   if doc in [971,972]:start,count=(1059,3) if doc==971 else (1062,2)
   if doc==0:start,count=-1,0
   self.assertEqual(d.call('sdRoute',doc),start);self.assertEqual(d.call('sdPageCount',doc),count)
   if count==0:continue
   self.assertEqual(d.call('sdOpen',doc,0,0,0,a),1)
   for page in range(count):
    d.p['sdPage']=page;self.assertEqual(d.call('sdLoad'),1);idx=start+page;seen.add(idx)
    self.assertEqual([d.p[n] for n in PROPS],t['sdPageData'][8*idx:8*idx+8]);self.assertEqual(d.p['sdResource'],t['sdTextResources'][idx]);self.assertEqual(d.p['sdAudioModule'],t['sdAudioModules'][idx]);self.assertEqual(d.p['sdVoiceEnd'],t['sdPageDurations'][idx])
    if idx in new:self.assertEqual(str(d.arrays['sdTextBuffer']),new[idx]['text'])
  self.assertEqual(seen,set(range(1191)))
  for doc in [-32768,-1,1140,32767]:self.assertEqual(d.call('sdRoute',doc),-1);self.assertEqual(d.call('sdPageCount',doc),0)
  EVIDENCE['emitted_pages']=len(seen);EVIDENCE['emitted_route_counts']=1140;EVIDENCE['route_vm']=h.vm.report()
 def test_every_new_emitted_caption_graph12_and_audio_visible_barrier(self):
  h,d,a,p,q,g=setup();count=0
  for r in M['document_routes']:
   self.assertEqual(h.call('dialogueOpen',r['document_id']),1)
   for pn,idx in enumerate(r['page_indices']):
    if pn:h.call('uiTurnPage',1)
    graph=sum(n=='Graph' and args[0]==12 for n,args in h.vm.ktrace);paint=len(h.vm.paint)
    frame(h)
    self.assertGreater(sum(n=='Graph' and args[0]==12 for n,args in h.vm.ktrace),graph);self.assertIn(M['pages'][idx]['text'],h.vm.paint[paint:]);self.assertEqual(d.p['sdPaintGeneration'],d.p['sdGeneration']);self.assertEqual(h.call('scenePageIdentity'),1);count+=1
  for muted in [0,1]:
   a.p['voiceMuted']=muted
   for r in M['unit_routes']:
    self.assertEqual(d.call('sdOpen',r['document_id'],0,0,0,a),1);gen=d.p['sdGeneration'];self.assertEqual(d.call('sdSpeak',a,gen,0),0)
    self.assertEqual(d.call('sdDraw',0),1);self.assertEqual(d.call('sdPresented',gen,0,a.p['token']),1);self.assertGreater(d.call('sdSpeak',a,gen,0),0)
    starts=[args for n,args in h.vm.ktrace if n=='DoAudio' and args[0]==2];self.assertEqual(starts[-1][1],911 if muted else 921)
    d.call('sdAfterRestore',a);self.assertEqual(d.call('sdPresented',gen,0,a.p['token']),0)
  self.assertEqual(count,53);EVIDENCE['new_emitted_graph12_pages']=count;EVIDENCE['emitted_voice_starts']=40
 def test_static_integrity_families_and_corrupt_old_and_new_words(self):
  h,d,a,p,q,g=setup();tables=json.loads((H/'generated/static/manifest.json').read_text())['tables'];self.assertEqual(len(tables),20)
  for t in tables:
   owner=h.vm.objects[{982:'sceneDialogue',985:'p05State',981:'musicTransport'}[t['module']]]
   for idx in sorted({0,t['count']-1}):
    self.assertEqual(g.call('hStaticRange',t['id'],idx,1),1);old=owner.arrays[t['name']][idx];owner.arrays[t['name']][idx]=old^1;self.assertEqual(g.call('hStaticRange',t['id'],idx,1),0);owner.arrays[t['name']][idx]=old;self.assertEqual(g.call('hStaticRange',t['id'],idx,1),1)
  # Tampered last P09 route and page cannot pass the normal emitted load gate.
  for name,idx in [('sdStarts',1139),('sdCounts',1139),('sdPageData',1190*8+1),('sdTextResources',1190),('sdAudioModules',1190),('sdPageDurations',1190)]:
   old=d.arrays[name][idx];d.arrays[name][idx]=old^1;self.assertEqual(d.call('sdOpen',1139,0,0,0,a),0,name);d.arrays[name][idx]=old
  self.assertEqual(d.call('sdOpen',1139,0,0,0,a),1);EVIDENCE['static_families']=20;EVIDENCE['static_word_mutations']=40+6
 def test_exact_predecessor_admission_for_each_array_and_method(self):
  source=(H/'inputs/src/module982.sc').read_text()
  for name in ext.ARRAYS:
   vals=ext.read_array(source,name);vals[-1]^=1
   with self.assertRaises(AssertionError):ext.apply_source(ext.replace_array(source,name,vals))
  for old,new in [('(> document 1017)','(> document 1018)'),('(!= sdResource 208)','(!= sdResource 209)'),('(!= sdAudioModule 918)','(!= sdAudioModule 919)')]:
   self.assertIn(old,source)
   with self.assertRaises(AssertionError):ext.apply_source(source.replace(old,new))
  EVIDENCE['predecessor_negative_mutations']=10
 def test_scope_and_current_array_gaps(self):
  for path in (H/'generated/src').glob('*.sc'):
   old=methods((H/'inputs/src'/path.name).read_text());new=methods(path.read_text());self.assertEqual(list(old),list(new))
   allowed={'module982.sc':{'sdRoute','sdPageCount','sdLoad','hStaticAt'},'module985.sc':{'hStaticCount','hStaticFirst','hStaticLoad'}}.get(path.name,set())
   self.assertLessEqual({n for n in old if old[n]!=new[n]},allowed)
  for doc in range(1018,1100):self.assertEqual((C['arrays']['sdStarts'][doc],C['arrays']['sdCounts'][doc]),(-1,0))
  receipt=json.loads((H/'evidence/compile-proof.json').read_text());self.assertTrue(receipt['baseline_recompiles_exactly']);self.assertEqual(receipt['new_selectors'],0);self.assertEqual(receipt['new_resources'],[[3,210]])
 def test_two_complete_emitted_readers_and_invalid_bounds(self):
  B=H/'build/reader';vm=base.HostVM(checkpoint=B/'verification-checkpoint',build=B,budget=1000000);r=vm.objects['readerProof']
  for i,reader in enumerate(M['readers'].values()):
   paint=len(vm.paint);self.assertEqual(r.call('drawPage',i),1);self.assertEqual(str(r.arrays['body']),reader['text']);self.assertIn(reader['text'],vm.paint[paint:])
  self.assertEqual(r.call('drawPage',-1),0);self.assertEqual(r.call('drawPage',2),0);EVIDENCE['emitted_complete_readers']=2
if __name__=='__main__':unittest.main()
