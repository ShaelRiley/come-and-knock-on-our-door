"""Mapping, interruption and preservation of the separately accepted window API."""
from pathlib import Path
import sys,json,unittest,struct
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H));sys.path.insert(0,str(H/'tests'));sys.path.insert(0,str(H/'tools'))
from source_tools import methods
from source_factory import VM as SourceVM
from host import setup,base
import mapping,extend_dialogue as ext
M=json.loads((H/'generated/manifest.json').read_text())

class CompositionTests(unittest.TestCase):
 def test_record_and_unit_resume_maps_exact_domain_ids(self):
  for r in M['routes']:
   p=mapping.plan(lines=(r['local_line_key'],));self.assertEqual(p['documents'],[r['document_id']]);self.assertFalse(p['display_authority'])
  for u in M['unit_routes']:
   p=mapping.plan(units=(u['speech_unit_id'],));self.assertEqual(p['documents'],[u['document_id']]);self.assertEqual(p['identity'][0]['kind'],'speech_unit')
  self.assertEqual(mapping.plan()['documents'],[])
  for bad in [(True,),(-1,),(0,),(24,),('1',),(1,1)]:
   with self.assertRaises(ValueError):mapping.plan(lines=bad)
  with self.assertRaises(ValueError):mapping.plan(lines=(1,),units=(1,))
 def test_source_plans_distinguish_whole_source_and_unit(self):
  for source,rid in M['source_bindings'].items():
   full=mapping.source_plan(source,record_id=rid);self.assertEqual(full['domain_form'],[M['local_line_keys'][rid],0,0]);self.assertFalse(full['display_authority'])
   units=[u for u in M['unit_routes'] if u['record_id']==rid]
   for u in units:
    partial=mapping.source_plan(source,unit_ids=(u['line_id'],));self.assertEqual(partial['domain_form'],[0,u['speech_unit_id'],u['speech_unit_id']]);self.assertNotEqual(partial['pages'],full['pages'])
  for kwargs in [dict(source='intro',record_id='P10.READ.001'),dict(source='intro',unit_ids=('P10.OPEN.001.02','P10.OPEN.001.01')),dict(source='intro',unit_ids=('P10.OPEN.001.01','P10.OPEN.001.03')),dict(source='intro',record_id='P10.OPEN.001',unit_ids=('P10.OPEN.001.01',)),dict(source='plan',unit_ids=('P10.OPEN.001.01',))]:
   with self.assertRaises(ValueError):mapping.source_plan(**kwargs)
 def test_all_new_source_routes_restore_and_boundary_retirement(self):
  d=SourceVM(H/'generated/module982.sc','SceneDialogue');a=SourceVM(H/'inputs/src/module980.sc','PresentationAudio',d.resources)
  for route in M['document_routes']:
   self.assertEqual(d.call('sdOpen',route['document_id'],2,3,4,a),1)
   d.p['sdPage']=route['page_count']-1;self.assertEqual(d.call('sdLoad'),1);generation=d.p['sdGeneration']
   self.assertEqual(d.call('sdAfterRestore',a),1);self.assertEqual(d.p['sdPage'],route['page_count']-1)
   self.assertEqual(d.call('sdPresented',generation,d.p['sdPage'],a.p['token']),0)
   self.assertEqual(d.call('sdTurn',1,a),0)
   self.assertEqual(d.call('sdClose',a),1);self.assertEqual(d.call('sdSpeak',a,generation,d.p['sdPage']),0)
  for reason in [10,11,12,13,14]:
   d.call('sdOpen',1223,0,0,0,a);g=d.p['sdGeneration'];d.call('sdDraw',0);d.call('sdPresented',g,0,a.p['token'])
   d.call('sdInterrupt',a,reason);self.assertEqual(d.call('sdSpeak',a,g,0),0);self.assertEqual(d.p['sdArmed'],0);self.assertEqual(a.p['mouth'],0)
  for bad in [-1,1,32767]:
   d.call('sdOpen',1223,0,0,0,a);d.p['sdPage']=bad;self.assertEqual(d.call('sdAfterRestore',a),0);self.assertEqual(d.p['sdActive'],0)
 def test_window_primitive_survives_table_extension_and_compiles(self):
  before=(H/'generated/window-predecessor.sc').read_text();after=(H/'generated/window-src/module982.sc').read_text()
  self.assertEqual(ext.apply_source(before)[0],after)
  old,new=methods(before),methods(after)
  for name in old:
   if name not in ('sdRoute','sdPageCount','sdLoad','hStaticAt'):self.assertEqual(old[name],new[name],name)
  # The inserted load window guards remain byte-for-byte; only table limits/banks change.
  self.assertIn('(self sdWindowValue: 2)',new['sdLoad'])
  for name in ext.ARRAYS:self.assertEqual(ext.read_array(after,name),ext.read_array((H/'generated/module982.sc').read_text(),name))
  self.assertIn('[sdWindowBounds 2]',after)
  B=H/'build/window';vm=base.HostVM(checkpoint=B/'verification-checkpoint',build=B,budget=10000000);d=vm.objects['sceneDialogue'];a=vm.objects['presentationAudio']
  self.assertEqual(d.call('sdOpenWindow',973,1,1,0,0,0,a),1);self.assertEqual(d.p['sdPage'],1)
  self.assertEqual(d.call('sdTurn',1,a),0);self.assertEqual(d.call('sdTurn',-1,a),0)
  self.assertEqual(d.call('sdAfterRestore',a),1);self.assertEqual(d.call('sdWindowValue',2),1)
  self.assertEqual(d.call('sdOpenWindow',1200,0,1,0,0,0,a),0) # P08 primitive not widened to P10
  self.assertEqual(d.call('sdOpen',1200,0,0,0,a),1);self.assertEqual(d.call('sdWindowValue',2),0)
  for route in M['document_routes']:
   self.assertEqual(d.call('sdOpen',route['document_id'],0,0,0,a),1)
   for page in range(route['page_count']):d.p['sdPage']=page;self.assertEqual(d.call('sdLoad'),1)
 def test_every_source_vm_route_and_page_matches_exact_arrays(self):
  d=SourceVM(H/'generated/module982.sc','SceneDialogue');a=SourceVM(H/'inputs/src/module980.sc','PresentationAudio',d.resources)
  t=json.loads((H/'generated/extension-contract.json').read_text())['arrays'];seen=set()
  for document in range(1243):
   start,count=t['sdStarts'][document],t['sdCounts'][document]
   if document==0:start,count=-1,0
   if document in (971,972):start,count=(1059,3) if document==971 else (1062,2)
   self.assertEqual(d.call('sdRoute',document),start);self.assertEqual(d.call('sdPageCount',document),count)
   if not count:continue
   self.assertEqual(d.call('sdOpen',document,0,0,0,a),1)
   for page in range(count):
    d.p['sdPage']=page;self.assertEqual(d.call('sdLoad'),1);index=start+page;seen.add(index)
    self.assertEqual([d.p[n] for n in ('sdEntry','sdLineKey','sdPart','sdPartCount','sdSpeaker','sdVoice','sdHeader','sdBytes')],t['sdPageData'][8*index:8*index+8])
  self.assertEqual(seen,set(range(1241)))
 def test_binary_sync_closed_terminal_and_monotonic_ticks(self):
  for v in M['speech']:
   raw=(H/'generated/speech'/v['sync_file']).read_bytes();self.assertEqual(raw[:2],b'\x8e\x00');self.assertEqual(raw[-2:],b'\xff\xff')
   rows=list(struct.iter_unpack('<hh',raw[2:-2]));self.assertEqual(rows[-1],(v['duration_ticks'],0));self.assertEqual([r[0] for r in rows],sorted(r[0] for r in rows));self.assertTrue(all(pose in (0,1,2) for tick,pose in rows))
if __name__=='__main__':unittest.main()
