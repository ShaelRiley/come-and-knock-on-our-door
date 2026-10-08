from pathlib import Path
import sys,json,unittest,copy,hashlib
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests'),str(H/'tools')]
from host import setup,frame,base
M=json.loads((H/'generated/manifest.json').read_text());P=H/'frozen-candidates/p13-scene-reconstruction'
from extend_dialogue import arrays

def exp(vm,d,index,*args):
 m=vm.modules[999];return vm.execute(d,m,'export'+str(index),m.layout['exports'][index],args)
def bind(vm,d,text):
 assert exp(vm,d,2,996,17,0,32,0,1,0,32,len(text))==1
 for i,c in enumerate(text):assert exp(vm,d,3,i,ord(c))==1
 assert exp(vm,d,4)==1
class RuntimeTests(unittest.TestCase):
 def test_all_new_routes_pages_and_paint_barriers(self):
  h,d,a,*_=setup();vm=h.vm
  for r in M['document_routes']:
   self.assertEqual(h.call('dialogueOpen',r['document_id']),1)
   for pn,pi in enumerate(r['page_indices']):
    if pn:h.call('uiTurnPage',1)
    g=d.p['sdGeneration'];self.assertEqual(d.call('sdSpeak',a,g,pn),0)
    before=sum(n=='Graph' and args[0]==12 for n,args in vm.ktrace);frame(h)
    self.assertEqual(h.call('scenePageIdentity'),1);self.assertGreater(sum(n=='Graph' and args[0]==12 for n,args in vm.ktrace),before)
    self.assertEqual(str(d.arrays['sdTextBuffer']),M['pages'][pi]['text']);self.assertEqual(d.p['sdLineKey'],r['document_id'])
   self.assertEqual(d.call('sdTurn',1,a),0)
 def test_all_old_routes_and_words_remain_exact(self):
  h,d,a,*_=setup();old=arrays((P/'generated/src/module982.sc').read_text())
  for name,words in old.items():self.assertEqual([v&65535 for v in d.arrays[name]],[v&65535 for v in words])
  for document in range(1,1593):
   route=old['sdStarts'][document];count=old['sdCounts'][document]
   if document==971:route,count=1059,3
   if document==972:route,count=1062,2
   self.assertEqual(d.call('sdRoute',document),route);self.assertEqual(d.call('sdPageCount',document),count)
  for document in [-32768,-1,0,1593,1599,1799,1802,32767]+M['reserved_template_documents']:
   self.assertEqual(d.call('sdOpen',document,0,0,0,a),0)
 def test_all37_existing_unit_windows_new_exclusion(self):
  b=H/'build/window';v=base.HostVM(checkpoint=b/'verification-checkpoint',build=b,budget=100000000);d=v.objects['sceneDialogue'];a=v.objects['presentationAudio'];w=json.loads((H/'inputs/p08/generated/line-document-unit-map.json').read_text())['output_windows'];w=[u for u in w if u['kind']=='unit_only'];self.assertEqual(len(w),37)
  for u in w:
   self.assertEqual(d.call('sdOpenWindow',u['document_id'],u['first_record_page'],u['page_count'],0,0,0,a),1);self.assertEqual(d.call('sdTurn',-1,a),0)
   for i in range(u['page_count']):
    if i:self.assertEqual(d.call('sdTurn',1,a),1)
    self.assertEqual(d.call('sdDraw',0),1)
   self.assertEqual(d.call('sdTurn',1,a),0)
  for doc in [1600,1725,1768,1800,1801]:self.assertEqual(d.call('sdOpenWindow',doc,0,1,0,0,0,a),0)
 def test_all28_static_table_mutations_fail_and_restore(self):
  h,d,a,p,q,guard=setup();v=h.vm;tables=json.loads((H/'generated/static/manifest.json').read_text())['tables']
  for t in tables:
   module=t.get('delegated_script',t['module']);words=v.arrays(module)[t['name']];i=len(words)//2;old=words[i];self.assertEqual(guard.call('hStaticRange',t['id'],i,1),1);words[i]=(old+1)%32768;self.assertEqual(guard.call('hStaticRange',t['id'],i,1),0,t['name']);words[i]=old;self.assertEqual(guard.call('hStaticRange',t['id'],i,1),1)
 def test_stale_integrity_resources_reject_new_words(self):
  h,d,a,p,q,g=setup();v=h.vm
  before=v.resources[3,245];v.resources[3,245]=b'00000 '*20+b'\0'
  with self.assertRaises((base.VMError,ValueError)):g.call('hStaticRange',28,0,1)
  v.resources[3,245]=before;self.assertEqual(g.call('hStaticRange',28,0,1),1)
  data=bytearray(before);data[0]=ord('X');v.resources[3,245]=bytes(data)
  # Table26 crosses into this resource; exact selected chunk fails parsing.
  t=next(t for t in json.loads((H/'generated/static/manifest.json').read_text())['tables'] if t['first_chunk']<=1440<t['first_chunk']+(t['count']+19)//20)
  self.assertEqual(g.call('hStaticRange',t['id'],(1440-t['first_chunk'])*20,1),0)
 def test_date_closed_mouth_and_lifecycle_retirement(self):
  h,d,a,*_=setup();v=h.vm;bind(v,d,'MiXeD actual supplied fixture');self.assertEqual(d.call('sdOpen',1800,0,0,0,a),1);self.assertEqual(d.call('sdDraw',0),1);self.assertEqual(d.p['sdVoice'],0);self.assertEqual(d.call('sdSpeak',a,d.p['sdGeneration'],0),0)
  snap=v.snapshot();self.assertEqual(d.call('sdClose',a),1);self.assertEqual(exp(v,d,5,0,0),0);v.restore(snap);self.assertEqual(d.call('sdAfterRestore',a),0);self.assertEqual(d.p['sdActive'],0);self.assertEqual(exp(v,d,5,0,0),0)
  bind(v,d,'Again');d.call('sdOpen',1800,0,0,0,a);d.call('sdOpen',1600,0,0,0,a);self.assertEqual(exp(v,d,5,0,0),0)
 def test_old_new_old_font_selection_and_restore(self):
  h,d,a,*_=setup();v=h.vm
  for doc,font in [(1500,0),(1600,1),(1500,0)]:
   self.assertEqual(d.call('sdOpen',doc,0,0,0,a),1);before=len(v.ktrace);self.assertEqual(d.call('sdDraw',0),1)
   traces=v.ktrace[before:];self.assertTrue(all(args[2]==font for n,args in traces if n=='TextSize'))
   for n,args in traces:
    if n=='Display':self.assertEqual(args[list(args).index(105)+1],font)
  snap=v.snapshot();d.call('sdOpen',1600,0,0,0,a);v.restore(snap);d.call('sdAfterRestore',a);before=len(v.ktrace);self.assertEqual(d.call('sdDraw',0),1);self.assertTrue(all(args[2]==0 for n,args in v.ktrace[before:] if n=='TextSize'))
 def test_date_mutation_and_input_rejection(self):
  h,d,a,*_=setup();v=h.vm
  for code in [-1,0,31,124,127,255,32767]:
   self.assertEqual(exp(v,d,2,996,1,0,1,0,1,0,1,1),1);self.assertEqual(exp(v,d,3,0,code),0);self.assertEqual(exp(v,d,5,0,0),0)
  for args in [(996,0,0,1,0,1,0,1,1),(995,1,0,1,0,1,0,1,1),(996,1,0,0,0,1,0,1,1),(996,1,0,1,0,1,0,1,81)]:self.assertEqual(exp(v,d,2,*args),0)
  bind(v,d,'Correct');words=v.arrays(999)['fbDate'];old=words[0];words[0]=124;self.assertEqual(exp(v,d,4),0);words[0]=old;words[79]=65;self.assertEqual(exp(v,d,4),0)
 def test_snapshot_program_and_bank_identity(self):
  h,d,a,*_=setup();v=h.vm;s=v.snapshot();bad=copy.deepcopy(s);bad['program']['999'][0]='0'*64
  with self.assertRaises(base.VMError):v.restore(bad)
  bad=copy.deepcopy(s);bad['locals']['999'].pop()
  with self.assertRaises(base.VMError):v.restore(bad)
if __name__=='__main__':unittest.main()
