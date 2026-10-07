"""Concrete ordinary restored-source/menu/ownership consistency regressions."""
import unittest,copy,json
from host import *
from test_practical import restore
from test_contest import taught,start,reply,win
VMS=[]
def offset(vm,module,name):return next(t['word_offset'] for t in vm.abi['modules'][str(module)]['locals'] if t['name']==name)
class SavedConsistency(unittest.TestCase):
 def test_packaged_table_text_rejects_malformed_length_words_and_labels(self):
  import tempfile,shutil
  from validate_static_inputs import validate
  with tempfile.TemporaryDirectory(prefix='p05-table-data-') as td:
   root=Path(td)
   names=['snapshot/contest/canonical-bindings.json','snapshot/contest/manifest.json','snapshot/r2/module981.sc','snapshot/contest-scene/module982.sc','snapshot/contest-scene/route-tables.inc']+[f'generated/static/{n}.text.bin' for n in (240,241,242)]
   for name in names:
    dest=root/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(H/name,dest)
   self.assertEqual(validate(root)['resource_numbers'],[240,241,242])
   probes=[]
   for n in [240,241,242]:
    path=root/f'generated/static/{n}.text.bin';original=path.read_bytes()
    for kind,changed in [('truncated',original[:-1]),('oversized',b'0'*200+b'\0'+original),('wrong-byte',b'X'+original[1:])]:
     path.write_bytes(changed)
     with self.assertRaises(RuntimeError):validate(root)
     probes.append([n,kind]);path.write_bytes(original)
   (H/'evidence/static-package-rejection-probes.json').write_text(json.dumps({'status':'PASS','probes':probes,'scope':'Pre-packaging exact data/length validation; not arbitrary native resource damage'},indent=2)+'\n')
 def test_each_static_table_family_rejects_mismatched_saved_words(self):
  h,d,a,p,q,r=setup();VMS.append(h.vm);h.vm.budget=100000000
  baseline=h.vm.snapshot();tables=json.loads((H/'generated/static/manifest.json').read_text())['tables'];proof=[]
  for t in tables:
   saved=copy.deepcopy(baseline);at=offset(h.vm,t['module'],t['name']);index=min(5,t['count']-1);old=saved['locals'][str(t['module'])][at+index]
   saved['locals'][str(t['module'])][at+index]=0 if old else 1
   restore(h,saved,[{'type':4,'message':13},{}])
   self.assertEqual((r.p['hRestoreValid'],r.call('hSaveReady'),h.p['uiFailure']),(0,0,10),t['name'])
   self.assertEqual(r.p['hFailure'],40,t['name']);proof.append(t['name'])
  restore(h,baseline,[{},{}]);self.assertEqual((r.p['hRestoreValid'],h.p['uiFailure']),(1,0))
  (H/'evidence/saved-static-families.json').write_text(json.dumps({'status':'PASS','tables':proof,'native_acceptance':False},indent=2)+'\n')
 def test_menu_reply_saved_buffer_and_pointer_mismatch_reject(self):
  h,d,a,p,q,r,v=taught();VMS.append(h.vm);h.vm.budget=100000000;start(h,v);saved=h.vm.snapshot()
  for array in ['hVCLabelBuffer09','hVCReplyLabelBuffer01','hVCSetupLabelBuffer01']:
   bad=copy.deepcopy(saved);at=offset(h.vm,985,array);bad['locals']['985'][at]=0
   restore(h,bad,[{}]);self.assertEqual((r.p['hRestoreValid'],r.p['hFailure'],h.p['uiFailure']),(0,41,10))
  restore(h,saved,[{},{}]);self.assertEqual(r.p['hRestoreValid'],1)
  before=(v.call('vcRead',96),v.call('vcRead',97));h.call('uiHostChoice',217,1)
  for cancel in ['back','close']:
   if cancel=='back':h.call('uiHostChoice',218,2)
   else:h.call('uiClose')
   self.assertEqual((h.p['uiChoiceContext'],v.call('vcRead',92)),(217,4));self.assertEqual(r.call('hSaveReady'),1)
   state=h.vm.snapshot();restore(h,state,[{},{}]);self.assertEqual(r.p['hRestoreValid'],1)
   self.assertEqual((v.call('vcRead',96),v.call('vcRead',97)),before)
   h.call('uiHostChoice',217,1)
 def test_response_menu_world_consistency_matrix(self):
  h,d,a,p,q,r,v=taught();VMS.append(h.vm);h.vm.budget=100000000;start(h,v);saved=h.vm.snapshot()
  cases=[('cakood','uiPanel',0),('cakood','uiChoiceContext',211),('p05State','hContestEnabled',0),('p05State','hMiloRoom',1),('cakood','onApron',1),('p05State','hVCStage',0),('p05State','hVCJackX',-32768)]
  for obj,key,value in cases:
   bad=copy.deepcopy(saved);bad['objects'][obj][key]=value;restore(h,bad,[{}])
   self.assertEqual((r.p['hRestoreValid'],r.call('hSaveReady'),h.p['uiFailure']),(0,0,10),(obj,key))
  restore(h,saved,[{},{}]);self.assertEqual(r.p['hRestoreValid'],1)
 def test_only_current_campaign_ownership_is_restorable(self):
  h,d,a,p,q,r,v=taught();VMS.append(h.vm);h.vm.budget=100000000;win(h,v);act(h,6,28);choice(h,211,5);saved=h.vm.snapshot()
  for key,value in [('hPAOwner',2),('hCartOwner',3),('hCartOwner',4)]:
   bad=copy.deepcopy(saved);bad['objects']['p05State'][key]=value;restore(h,bad,[{}]);self.assertEqual((r.p['hRestoreValid'],r.call('hSaveReady'),h.p['uiFailure']),(0,0,10),key)
  restore(h,saved,[{},{}]);self.assertEqual(r.p['hRestoreValid'],1);self.assertEqual((r.p['hPARoom'],r.p['hCartRoom']),(4,5))
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SavedConsistency));(H/'evidence/saved-consistency-tests.json').write_text(json.dumps({'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':[(str(t),s) for t,s in result.failures],'errors':[(str(t),s) for t,s in result.errors],'instructions':sum(v.steps for v in VMS),'native_acceptance':False},indent=2)+'\n');raise SystemExit(not result.wasSuccessful())
