"""Playable P09 integration: genuine Gate B, actual controls, source + emitted.
These are deterministic interpreter tests, not native pixels, audio or save I/O.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import unittest
import host
from source_host import VM as SourceVM
from test_confirmation_boundaries import stage
from test_layout_controls import menu_pick, controls
from test_practical import input_action, arrive, enter_control
from test_restore import load
from storage_kernel_profile import StorageBackend
from test_card_ownership import owners, words

CACHE = {}

def diagnostic_identity(source):
 root=Path(__file__).resolve().parents[1]
 paths={p for folder in ('src','tools','build/coherent/compiled') for p in (root/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 paths.update(root/'tests'/n for n in ('host.py','source_host.py','domain_source_vm.py'))
 rows={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
 return {'backend':'source' if source else 'emitted','files':rows}

def gate_b(source):
 cache_dir=os.environ.get('P09_DIAGNOSTIC_CACHE')
 identity=diagnostic_identity(source) if cache_dir else None
 cache_path=Path(cache_dir)/('gate-b-source.json' if source else 'gate-b-emitted.json') if cache_dir else None
 if source not in CACHE and cache_path and cache_path.exists():
  prior=json.loads(cache_path.read_text())
  if prior['identity']==identity:
   CACHE[source]=prior['state']
   print('DIAGNOSTIC ONLY: verified genuinely earned Gate B cache',prior['origin_test_sha256'],flush=True)
 if source not in CACHE:
  h,p,q,r,t,u,v,s = stage(source,'menu')
  StorageBackend(h.vm)
  menu_pick(h,1)
  for _ in range(10):
   h.vm.pump([{}])
   if s.arrays['h8VP'][0] == 3: break
  assert h.p['uiDocument'] == 1013
  enter_control(h,12)
  assert s.arrays['h8VP'][0] == 4
  assert s.call('h8VF',4) == 1
  s.call('h8V',0,0)
  assert s.arrays['h8VP'][0] == 5
  h.call('render')
  assert s.call('h8GB',1) == 1
  assert s.call('h8EveningReady') == 1
  CACHE[source] = h.vm.snapshot()
  if cache_path:
   cache_path.parent.mkdir(parents=True,exist_ok=True)
   cache_path.write_text(json.dumps({'identity':identity,'origin':'stage(menu), real confirmation, reader Close, final h8VF/h8V/render, h8GB==1','origin_test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'state':CACHE[source]}))
 vm = SourceVM() if source else host.VM()
 vm.budget = 900000000
 vm.restore(copy.deepcopy(CACHE[source]))
 h = vm.objects['cakood']
 return h,vm.objects['p09State']

def walk(h,obj,room):
 h.vm.pump([{'type':4,'message':27},{}])
 assert h.p['uiVerb'] == 0
 enter_control(h,1,obj)
 for _ in range(350):
  h.vm.pump([{}])
  if h.p['motionPhase']==0:break
 assert h.p['motionPhase']==0,(obj,h.p['location'],h.p['motionPhase'],h.p['motionX'],h.p['motionY'])
 host.close(h)
 assert h.p['location'] == room,(obj,h.p['location'],room)

def conservatory(source):
 h,d = gate_b(source)
 walk(h,18,1);walk(h,17,0);walk(h,16,6)
 return h,d

def expose_control(h,obj):
 if (1,obj) not in controls(h):
  h.vm.pump([{'type':4,'message':27},{'type':1,'x':285,'y':136}])
  arrive(h)
 assert (1,obj) in controls(h),(obj,h.p['motionX'],h.p['motionY'])

def pick_topic(h,topic,paint=False):
 if h.p['uiPanel']: h.call('uiClose')
 input_action(h,6,29);arrive(h)
 assert h.p['uiChoiceContext'] == 239,h.p['uiChoiceContext']
 for legacy in range(1,10):
  if h.call('p02TopicAvailable',29,legacy):assert h.call('uiGetChoice',100+legacy)>=0
 # The actual menu has been reached through input; call its production choice
 # entrypoint without pumping, so frame boundaries can be inspected precisely.
 h.call('uiHostChoice',239,topic)
 if paint: h.call('render')

def counts(d):return tuple(d.call('p09Count',s) for s in range(1,10))
def p10_state(h):
 p=h.vm.objects['p10State']
 return (dict(p.p),{k:list(v) for k,v in p.arrays.items()})

class P09Active(unittest.TestCase):
 def test_01_real_first_click_modal_close_reopen_and_routes(self):
  for source in (False,True):
   h,d = conservatory(source);old=owners(h);p10=p10_state(h)
   self.assertEqual(d.call('h9Active'),1)
   self.assertIn((1,395),controls(h))
   self.assertEqual(counts(d),(0,)*9)
   # Mandatory regression: first click must both admit context and queue text.
   input_action(h,5,395);arrive(h)
   self.assertEqual((h.p['uiPanel'],h.p['uiDocument']),(4,1103))
   self.assertEqual(d.call('p09Count',3),1)
   self.assertEqual(d.p['p09RumorCleared'],1)
   before=counts(d);position=(h.p['location'],h.p['motionPhase'])
   h.vm.pump([{'type':1,'x':25,'y':80},{}])
   self.assertEqual((h.p['location'],h.p['motionPhase']),position)
   self.assertEqual(counts(d),before)
   modal_words=words(d)
   d.call('h9Dispatch',5,397,0);h.call('uiHostChoice',239,7)
   self.assertEqual(words(d),modal_words)
   self.assertFalse(any(a==1 and o in (395,396,397,398,29) for a,o in controls(h)))
   enter_control(h,12)
   input_action(h,5,396);arrive(h)
   self.assertEqual(h.p['uiDocument'],1102);self.assertEqual(d.call('p09Count',2),1)
   enter_control(h,12)
   expose_control(h,397);input_action(h,5,397);arrive(h)
   self.assertEqual(h.p['uiDocument'],1105)
   first=d.call('p09Count',5);self.assertGreater(first,0);self.assertLess(first,3)
   enter_control(h,12)
   self.assertEqual(d.p['p09ContextValid'],0)
   self.assertIn(5,[d.call('p09PendingAt',i) for i in range(9)])
   expose_control(h,397);input_action(h,5,397);arrive(h)
   self.assertEqual(h.p['uiDocument'],1105)
   host.close(h)
   self.assertEqual(d.call('p09Count',5),3)
   self.assertEqual(owners(h),old);self.assertEqual(p10_state(h),p10)
   if source:
    for method in ('h9Dispatch','h9Choice','h9Frame','h9ReaderCheck','h9Closed'):
     self.assertGreater(h.vm.sources['p09State'].source_calls[method],0,method)
    self.assertGreater(h.vm.sources['cakood'].source_calls['uiHostChoice'],0)
    self.assertGreater(h.vm.sources['cakood'].source_calls['uiHostClosed'],0)

 def test_02_terms_exact_units_restore_success_and_card(self):
  for source in (False,True):
   h,d=conservatory(source);old=owners(h);p10=p10_state(h)
   pick_topic(h,4)
   self.assertEqual(h.p['uiDocument'],1105)
   self.assertEqual(d.call('p09Count',4),0)
   h.call('render');self.assertEqual(d.call('p09Count',4),1)
   host.close(h)
   self.assertEqual(d.call('p09Count',4),3)
   pick_topic(h,7)
   self.assertEqual((h.p['uiDocument'],h.p['uiPageCount']),(1109,5))
   self.assertEqual(d.call('p09Count',7),0)
   for page in range(5):
    if page:h.call('uiTurnPage',1)
    self.assertEqual(d.call('p09Count',7),page)
    self.assertEqual(h.call('campaignHeld',399),0)
    # Metadata callbacks and unprepared flush cannot substitute for rendering.
    h.call('dialoguePresented');d.call('h9Frame',1)
    self.assertEqual(d.call('p09Count',7),page)
    h.call('render')
    self.assertEqual(d.call('p09Count',7),page+1)
    self.assertEqual(d.p['p09Ready'],int(page==4))
    self.assertEqual(h.call('campaignHeld',399),int(page==4))
   self.assertEqual(h.p['uiDocument'],1109)
   self.assertEqual(list(h.arrays['uiItems']).count(399),1)
   self.assertIn(7,[d.call('p09PendingAt',i) for i in range(9)])
   # Save precisely between card acquisition and the separate success record.
   b=StorageBackend(h.vm);h.call('writeSave');self.assertIsNotNone(b.saved)
   saved=copy.deepcopy(b.saved);before=words(d)
   load(h,b,saved)
   self.assertEqual(words(d),before)
   self.assertEqual(d.call('p09Count',7),5)
   self.assertEqual(list(h.arrays['uiItems']).count(399),1)
   # Actual NEXT opens the separate success reader only after the fifth receipt.
   self.assertTrue(any(action==11 for action,payload in controls(h)))
   enter_control(h,11)
   self.assertEqual(h.p['uiDocument'],1116)
   self.assertEqual(d.call('p09Count',7),6)
   load(h,b,saved)
   self.assertEqual(d.call('p09Count',7),5)
   pick_topic(h,7)
   self.assertEqual(h.p['uiDocument'],1116)
   self.assertEqual(d.call('p09Count',7),5)
   h.call('dialoguePresented');self.assertEqual(d.call('p09Count',7),5)
   h.call('render');self.assertEqual(d.call('p09Count',7),6)
   enter_control(h,12)
   # Inventory action is real; its two-page descriptor must remain uncollapsed.
   card_page=d.call('h9CardReservation',399)//8
   while h.p['uiInventoryPage']<card_page:enter_control(h,5)
   while h.p['uiInventoryPage']>card_page:enter_control(h,4)
   input_action(h,2,399);arrive(h)
   self.assertEqual((h.p['uiDocument'],h.p['uiPageCount']),(1111,2))
   self.assertEqual(d.call('p09Count',9),0)
   h.call('uiTurnPage',1);h.call('dialoguePresented')
   self.assertEqual(d.call('p09Count',9),0)
   h.call('render');self.assertEqual(d.call('p09Count',9),1)
   host.close(h)
   pick_topic(h,8);host.close(h)
   self.assertEqual(d.call('p09Count',8),4)
   for _ in range(3):
    self.assertEqual(h.call('p02HostInventory'),1)
    self.assertEqual(list(h.arrays['uiItems']).count(399),1)
    self.assertEqual(d.call('h9InventoryValid'),1)
   self.assertEqual(owners(h),old);self.assertEqual(p10_state(h),p10)
   self.assertEqual(d.call('p09Validate'),1)
   if source:
    for method in ('h9Restore','h9ProjectCard','h9Frame'):
     self.assertGreater(h.vm.sources['p09State'].source_calls[method],0,method)
    self.assertGreater(h.vm.sources['p09State'].source_calls['h9Draw'],0)

 def test_03_stale_foreign_metadata_and_fresh_restore_frames(self):
  for source in (False,True):
   h,d=conservatory(source)
   expose_control(h,398);input_action(h,5,398);arrive(h)
   self.assertEqual(h.p['uiDocument'],1100)
   host.close(h)
   self.assertEqual(d.call('p09Count',1),2)
   hint_counts=counts(d)
   for document in (1117,1118,1119):
    h.call('p03PreparationHint')
    self.assertEqual(h.p['uiDocument'],document)
    host.close(h);self.assertEqual(counts(d),hint_counts)
   pick_topic(h,6)
   self.assertEqual(h.p['uiDocument'],1107);host.close(h)
   self.assertEqual(d.call('p09Count',6),2)
   pick_topic(h,4)
   opened=h.vm.snapshot();before=counts(d)
   foreign=h.vm.objects['P09State']
   for phase in (0,1,2,3):self.assertEqual(foreign.call('h9Frame',phase),0)
   self.assertEqual(foreign.call('h9Draw'),0)
   self.assertEqual(foreign.call('h9Choice',239,4),0)
   self.assertEqual(d.call('h9Frame',2),0)
   self.assertEqual(counts(d),before)
   h.call('dialoguePresented');d.call('h9Frame',1)
   self.assertEqual(counts(d),before)
   # Every descriptor mismatch rejects even after a candidate frame is prepared.
   dialog=h.vm.objects['sceneDialogue']
   self.assertEqual(d.call('h9Frame',0),1)
   self.assertEqual(d.call('h9Draw'),1);dialog.call('sdDraw',0)
   self.assertEqual(d.call('h9Frame',1),1)
   self.assertEqual(d.call('p09Count',4),before[3]+1)
   kernel=h.vm._kernel
   for accumulator in (0,1,-1):
    h.vm.restore(copy.deepcopy(opened))
    def varied_flush(number,args):
     value=kernel(number,args)
     return accumulator if h.vm.knames.get(number)=='Graph' and args[0]==12 else value
    h.vm._kernel=varied_flush
    try:h.call('render')
    finally:h.vm._kernel=kernel
    self.assertEqual(d.call('p09Count',4),before[3]+1,accumulator)
   mutations=[('document',lambda:dialog.p.__setitem__('sdDocument',1107)),
    ('page',lambda:dialog.p.__setitem__('sdPage',1)),
    ('voice_end',lambda:dialog.p.__setitem__('sdVoiceEnd',dialog.p['sdVoiceEnd']+1)),
    ('generation',lambda:dialog.call('sdMark',2)),
    ('room',lambda:h.p.__setitem__('location',1)),
    ('menu',lambda:h.p.__setitem__('menuOpen',1)),
    ('panel',lambda:h.p.__setitem__('uiPanel',0))]
   for label,mutate in mutations:
    h.vm.restore(copy.deepcopy(opened));d.call('h9Frame',0);d.call('h9Draw');dialog.call('sdDraw',0);mutate()
    d.call('h9Frame',1);h.call('dialoguePresented')
    self.assertEqual(counts(d),before,label)
   h.vm.restore(copy.deepcopy(opened))
   # Corrupt each captured frame field individually; no mutated receipt is valid.
   d.call('h9Frame',0);d.call('h9Draw');dialog.call('sdDraw',0)
   captured=list(d.arrays['h9F'])
   for index in range(len(captured)):
    h.vm.restore(copy.deepcopy(opened));d.call('h9Frame',0);d.call('h9Draw');dialog.call('sdDraw',0)
    d.arrays['h9F'][index]=captured[index]+101
    d.call('h9Frame',1)
    self.assertEqual(counts(d),before,index)
   h.vm.restore(copy.deepcopy(opened));b=StorageBackend(h.vm)
   h.call('writeSave');self.assertIsNotNone(b.saved)
   observed=[]
   def restore_boundary(obj,name,args,result):
    if obj.name=='p09State' and name=='h9Restore' and args and args[0]==1:
     observed.append((counts(d),list(d.arrays['h9F'])))
   h.vm.after_actual_call=restore_boundary
   load(h,b,copy.deepcopy(b.saved))
   h.vm.after_actual_call=None
   self.assertTrue(observed)
   self.assertEqual(observed[0][0],before)
   self.assertEqual(observed[0][1],[0]*len(d.arrays['h9F']))
   self.assertEqual(h.p['uiDocument'],1105)
   valid_saved=copy.deepcopy(b.saved);bad_saved=copy.deepcopy(b.saved)
   offset=next(row['word_offset'] for row in h.vm.abi['modules']['990']['locals'] if row['name']=='h9R')
   bad_saved['locals']['990'][offset+2]+=1
   load(h,b,bad_saved)
   self.assertEqual(counts(d),before)
   self.assertNotEqual(h.p['uiFailure'],0)
   load(h,b,valid_saved)
   host.close(h);self.assertEqual(d.call('p09Count',4),3)
   self.assertEqual(d.call('p09Validate'),1)

if __name__=='__main__':unittest.main(verbosity=2)
