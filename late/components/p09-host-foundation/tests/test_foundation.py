"""Inactive production integration, exact static preservation, and ordinary play.

No P09 action prerequisites, evening history, actor locations, or progress are
fabricated. Kernel mocks and source evaluation are explicitly non-native.
"""
from pathlib import Path
import copy,json,sys,unittest
import host
from source_host import VM as SourceVM
from test_return_caption import boot,first_entry
from host import act,close,frame
H=host.H;EMITTED=host.VM
sys.path.insert(0,str(H))

def fresh(source):
 old=host.VM;host.VM=SourceVM if source else EMITTED
 try:return boot(H)
 finally:host.VM=old

def domain_image(q):
 return ({k:v for k,v in q.p.items() if k.startswith('p09')},
         {k:list(v) for k,v in q.arrays.items()})

class Foundation(unittest.TestCase):
 def test_fresh_real_boot_initializes_inactive_p09(self):
  images=[]
  for source in (False,True):
   h=fresh(source);q=h.vm.objects['p09State'];s=h.vm.objects['p08State']
   self.assertIs(h.p['p09'],q);self.assertIs(q.p['h9Host'],h)
   self.assertEqual((q.p['p09Initialized'],q.p['p09ContextValid'],q.p['p09Evening'],q.p['p09Epoch']),(1,0,0,0))
   before=domain_image(q)
   for _ in range(4):
    self.assertEqual(q.call('h9Active'),0)
    self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady')),(0,0))
    self.assertEqual(q.call('h9Init',h),1)
   self.assertEqual(domain_image(q),before)
   self.assertTrue(all(q.call('p09SerialHi',i)==q.call('p09SerialLo',i)==0 for i in range(13)))
   self.assertEqual(list(q.arrays['p09Held']),[0]*400)
   images.append(domain_image(q))
  self.assertEqual(*images)

 def test_chair_card_targets_refused_before_legacy_dispatch(self):
  for source in (False,True):
   h=fresh(source);q=h.vm.objects['p09State'];before=domain_image(q)
   legacy_before={k:list(v) for k,v in h.arrays.items() if k in ('p02Reserved','p02Slots')}
   calls=[]
   def trace(obj,name,args,result):calls.append((obj.name,name))
   h.vm.after_actual_call=trace
   for obj in range(395,400):
    for action in range(10):
     self.assertEqual(q.call('h9Dispatch',action,obj,0),1)
     self.assertEqual(q.call('h9Dispatch',action,25,obj),1)
     self.assertEqual(h.call('bridgeActAtArrival',action,obj,0),0)
     self.assertEqual(h.call('bridgeActAtArrival',action,25,obj),0)
    self.assertEqual(h.call('campaignHeld',obj),0)
    self.assertEqual(h.call('campaignReachable',obj),0)
    self.assertEqual(h.call('p02ObjectLocation',obj),-1)
    self.assertEqual(h.call('p03HostReservation',obj),-1)
   for name in ('bDispatch','qDispatch','p02Act','p09Context','p09Act','p09Begin','p09Acknowledge'):
    self.assertFalse(any(n==name for _,n in calls),name)
   self.assertEqual({k:list(h.arrays[k]) for k in legacy_before},legacy_before)
   self.assertEqual(domain_image(q),before)
   for obj in (1,5,34,63,72,73,80,81,83,86,92,94,120):self.assertEqual(q.call('h9Dispatch',6,obj,0),0)

 def test_original_entry_travel_and_ordinary_restore_stay_inactive(self):
  from test_restore import Backend,load
  for source in (False,True):
   h=fresh(source);q=h.vm.objects['p09State'];before=domain_image(q)
   first_entry(h,'bunny');act(h,0,17);act(h,2,1);act(h,0,1);close(h)
   self.assertEqual((h.p['location'],h.p['p01Consumed']),(1,1))
   backend=Backend(h.vm);h.call('writeSave');self.assertIsNotNone(backend.saved)
   saved=copy.deepcopy(backend.saved);act(h,0,17);load(h,backend,saved)
   self.assertEqual(h.p['location'],1)
   self.assertEqual(q.call('h9Active'),0);self.assertEqual(domain_image(q),before)
   self.assertEqual(q.call('p09Validate'),1)

 def test_all_prior_scene_routes_and_new53_pages_exact(self):
  from derive import array
  old=(H/'frozen/p08/src/module982.sc').read_text();new=(H/'src/module982.sc').read_text()
  manifest=json.loads((H/'frozen/scene/generated/manifest.json').read_text())
  for source in (False,True):
   h=fresh(source);d=h.vm.objects['sceneDialogue'];p=h.vm.objects['p05State']
   self.assertEqual(p.call('hStaticAll'),1)
   for document,count in enumerate(array(old,'sdCounts')):
    # The current P08 reader has two reviewed hard-coded window aliases.
    self.assertEqual(d.call('sdPageCount',document),{971:3,972:2}.get(document,count))
   for route in manifest['document_routes']:
    self.assertEqual(d.call('sdPageCount',route['document_id']),route['page_count'])
   for name in ('sdStarts','sdCounts','sdPageData','sdLegacyVoiceDurations','sdTextResources','sdAudioModules','sdPageDurations'):
    self.assertEqual(list(d.arrays[name]),[v if v<32768 else v-65536 for v in array(new,name)])
   self.assertEqual(len(d.arrays['sdTextResources'])-len(array(old,'sdTextResources')),53)
   self.assertTrue(all(d.call('sdPageCount',i)==0 for i in range(1018,1100)))

if __name__=='__main__':unittest.main(verbosity=2)
