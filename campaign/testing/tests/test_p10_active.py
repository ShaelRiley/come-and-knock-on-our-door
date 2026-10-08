"""P10 actual actor/reader/rack actions; deterministic source and emitted host."""
import copy,unittest,json,os,hashlib
from pathlib import Path
import host
from test_card_ownership import committed
from test_practical import enter_control,input_action as base_input_action
from host import frame,close,act
from campaign_route import living
from test_restore import Backend,load

def input_action(h,verb,obj,target=0):
 # Inventory ownership does not imply that its page is currently displayed.
 # Navigate via the actual PREV/NEXT controls, preserving dense reservations.
 items=list(h.arrays['uiItems'])
 if obj in items:
  page=items.index(obj)//8
  while h.p['uiInventoryPage']<page:enter_control(h,5)
  while h.p['uiInventoryPage']>page:enter_control(h,4)
 base_input_action(h,verb,obj,target)

def arrive(h):
 # Wait for the real approach and its pending first input, rather than pumping
 # dozens of unrelated idle frames after completion. Never force motion fields.
 d=h.vm.objects['p10State']
 for _ in range(70):
  h.vm.pump([{}])
  if h.p['motionPhase']==0 and not d.arrays['h10PendingAction'][0]:break
 assert h.p['motionPhase']==0 and not d.arrays['h10PendingAction'][0]
 frame(h)

def pick(h,id):
 index=next(i for i in range(h.p['uiChoiceCount']) if h.arrays['uiChoiceIds'][i]==id)
 for _ in range(32):
  h.call('uiBuildFocus')
  controls=[(h.arrays['uiActions'][i],h.arrays['uiPayloads'][i]) for i in range(h.p['uiControlCount'])]
  if (13,index) in controls:break
  before=h.p['uiPage'];enter_control(h,11 if h.p['uiPage']<index else 10)
  assert h.p['uiPage']!=before
 else:raise AssertionError(('choice never became visible',id,index))
 enter_control(h,13,index)

def ready(source):
 cache=host.H/'evidence'/('p10-earned-'+str(source)+'.json')
 if os.getenv('P10_DEV_REUSE') and cache.exists():
  from source_host import VM as SourceVM
  vm=SourceVM() if source else host.VM();vm.budget=900000000
  vm.restore(json.loads(cache.read_text()));h=vm.objects['cakood'];return h,vm.objects['p10State']
 h,_=committed(source);s=h.vm.objects['p08State']
 for _ in range(10):
  if s.arrays['h8VP'][0]==3:break
  h.vm.pump([{}])
 enter_control(h,12)
 s.call('h8V',0,0);h.call('render')
 assert s.call('h8EveningReady')==1
 cache.write_text(json.dumps(h.vm.snapshot()))
 return h,h.vm.objects['p10State']

class P10Active(unittest.TestCase):
 def test_real_plan_bread_paper_and_rack(self):
  for source in (False,True):
   print('P10 BACKEND',source,flush=True)
   h,d=ready(source);s=h.vm.objects['p08State'];p09=h.vm.objects['p09State']
   self.assertEqual(p09.p['p09Ready'],0)
   living(h)
   arrivals=[]
   def observe(obj,name,args,result):
    if obj.name=='p10State' and name=='h10Dispatch':arrivals.append(list(d.arrays['h10PendingAction']))
   h.vm.after_actual_call=observe
   input_action(h,2,7);arrive(h)
   h.vm.after_actual_call=None
   self.assertTrue(any(row[0] for row in arrivals),arrivals)
   self.assertEqual((h.p['uiPanel'],h.p['uiChoiceContext']),(2,240))
   pick(h,2)
   self.assertEqual(h.p['uiDocument'],1202)
   close(h)
   self.assertEqual(d.call('p10Complete',2),1)
   act(h,0,12)
   input_action(h,5,5);arrive(h);pick(h,1)
   self.assertEqual(h.p['uiDocument'],1200)
   close(h)
   self.assertEqual(d.call('p10Complete',1),1)
   input_action(h,5,5);arrive(h);pick(h,7);close(h)
   self.assertEqual(d.call('p10Complete',7),1)
   print('P10 actual plan and Bunny readers',source,flush=True)
   living(h);act(h,0,13)
   input_action(h,5,410);arrive(h)
   self.assertEqual(h.p['uiChoiceContext'],240)
   pick(h,5);close(h)
   self.assertEqual(d.call('p10Complete',5),1)
   input_action(h,5,410);arrive(h);pick(h,8);close(h)
   for i,cue in enumerate((412,413,414)):
    input_action(h,5,cue);arrive(h);pick(h,i+1);close(h)
    input_action(h,5,cue);arrive(h);pick(h,4);pick(h,i);close(h)
   self.assertEqual(d.call('p10RackCorrect'),1)
   self.assertEqual(d.call('p10Ready'),1)
   serial=(d.p['p10RestoredHi'],d.p['p10RestoredLo'])
   print('P10 paper rack restored',source,serial,flush=True)
   input_action(h,5,410);arrive(h);pick(h,20);pick(h,5);close(h)
   self.assertEqual(d.call('p10RackCorrect'),0)
   self.assertEqual(d.call('p10Ready'),1)
   input_action(h,5,412);arrive(h);pick(h,4);pick(h,0);close(h)
   self.assertEqual((d.p['p10RestoredHi'],d.p['p10RestoredLo']),serial)
   # Ceramic originals use the same real controls and replace, rather than duplicate, their dense inventory reservations.
   for slot in range(3):
    input_action(h,5,410);arrive(h);pick(h,20+slot);pick(h,5);close(h)
   for slot,cue in enumerate((48,49,50)):
    if slot==0:
     input_action(h,5,cue);arrive(h);pick(h,6);close(h)
     self.assertEqual(d.call('p10Complete',4),1)
    input_action(h,5,cue);arrive(h);pick(h,slot+1);close(h)
    input_action(h,5,cue);arrive(h);pick(h,4);pick(h,slot);close(h)
   self.assertEqual([d.call('p10SlotAt',i) for i in range(3)],[48,49,50])
   input_action(h,5,410);arrive(h);pick(h,20);pick(h,0);close(h)
   self.assertEqual(d.call('p10RackCorrect'),0)
   input_action(h,5,410);arrive(h);pick(h,20);pick(h,1);close(h)
   self.assertEqual(d.call('p10RackCorrect'),1)
   self.assertEqual((d.p['p10RestoredHi'],d.p['p10RestoredLo']),serial)
   self.assertEqual(h.call('campaignHeld',24),1);self.assertEqual(h.call('campaignHeld',25),1)
   input_action(h,2,32);arrive(h);pick(h,105);close(h)
   self.assertEqual(d.call('p10Complete',3),1)
   living(h);act(h,0,17);act(h,0,16)
   input_action(h,6,30);arrive(h);pick(h,120);close(h)
   self.assertEqual(d.call('p10Complete',6),1)
   self.assertTrue(all(d.call('p10Complete',i) for i in range(1,8)))
   print('P10 seven sources and ceramic rack',source,flush=True)
   b=Backend(h.vm);h.call('writeSave');saved=copy.deepcopy(b.saved)
   self.assertIsNotNone(saved);load(h,b,saved)
   self.assertEqual(d.call('p10RackCorrect'),1);self.assertEqual(d.call('h10Inv'),1)
   self.assertEqual(d.call('h10Save'),1)
   receipt={'backend':'source' if source else 'emitted','native_acceptance':False,
    'sources':{str(i):d.call('p10Count',i) for i in range(1,8)},
    'first_restoration':list(serial),'rack':[d.call('p10SlotAt',i) for i in range(3)],
    'labels':[d.call('p10LabelFor',i) for i in (48,49,50,412,413,414)],
    'domain_words':[d.call('h10Word',0,i,0) for i in range(61)],
    'reservations':list(d.arrays['h10S']),'inventory':list(h.arrays['uiItems']),
    'p09_complete':p09.p['p09Ready'],'graph12_calls':sum(n=='Graph' and a[0]==12 for n,a in h.vm.ktrace),
    'pending_arrival_observed':any(row[0] for row in arrivals),
    'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'compile_receipt_sha256':hashlib.sha256((host.H/'build/coherent/compile-receipt.json').read_bytes()).hexdigest()}
   (host.H/'evidence'/('p10-active-proof-'+str(source)+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
   if source:
    self.assertGreater(h.vm.sources['p10State'].source_calls['h10Frame'],0)
    self.assertGreater(h.vm.sources['p10State'].source_calls['h10Choice'],0)

 def test_unseen_skip_close_save_and_foreign_reader_do_not_credit(self):
  for source in (False,True):
   h,d=ready(source);sd=h.vm.objects['sceneDialogue'];living(h);act(h,0,12)
   input_action(h,5,5);arrive(h)
   h.call('uiHostChoice',240,1)
   self.assertEqual((h.p['uiDocument'],d.call('p10Count',1)),(1200,0))
   captured=list(d.arrays['h10Reader'])
   self.assertEqual(h.vm.objects['P10State'].call('h10Frame',0),0)
   self.assertEqual(h.vm.objects['P10State'].call('h10Retire'),0)
   self.assertEqual(list(d.arrays['h10Reader']),captured)
   self.assertEqual(d.call('h10Frame',1),0)
   sd.call('sdDraw',0);d.call('h10Frame',1)
   self.assertEqual(d.call('p10Count',1),0)
   h.call('render');h.call('uiTurnPage',5);h.call('render')
   self.assertEqual(d.call('p10Count',1),0)
   self.assertLess(d.arrays['h10Reader'][6],d.arrays['h10Reader'][7])
   start=(d.call('p10SerialHi',4),d.call('p10SerialLo',4))
   b=Backend(h.vm);h.call('writeSave');saved=copy.deepcopy(b.saved)
   self.assertIsNotNone(saved);load(h,b,saved)
   self.assertEqual(d.arrays['h10Reader'][0],0)
   self.assertEqual(d.call('p10Count',1),0)
   h.call('uiClose');frame(h)
   input_action(h,5,5);arrive(h);h.call('uiHostChoice',240,1)
   self.assertEqual((d.call('p10SerialHi',4),d.call('p10SerialLo',4)),start)
   # A changed canonical descriptor is not authenticated by a matching document.
   entry=sd.p['sdEntry'];sd.p['sdEntry']=entry+1
   h.call('render');self.assertEqual(d.call('p10Count',1),0)
   sd.p['sdEntry']=entry;h.call('uiClose');frame(h)
   input_action(h,5,5);arrive(h);h.call('uiHostChoice',240,1)
   # Switching to another owner's modal without close cannot reuse P10 intent.
   h.call('dialogueOpen',1100);h.call('render')
   self.assertEqual(d.call('p10Count',1),0)
   self.assertEqual(d.arrays['h10Reader'][0],0)
   h.call('uiClose');frame(h)
   input_action(h,5,5);arrive(h);pick(h,1);close(h)
   self.assertEqual(d.call('p10Complete',1),1)
   self.assertEqual((d.call('p10SerialHi',4),d.call('p10SerialLo',4)),start)
