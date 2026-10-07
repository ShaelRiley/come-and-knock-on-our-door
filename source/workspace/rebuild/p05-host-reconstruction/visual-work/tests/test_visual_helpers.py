#!/usr/bin/env python3
"""Execute freshly emitted SCI against deterministic existing kernel mocks.
Pixel ownership is exhaustively checked from emitted uiAddControl array results.
No native UI, sound, pixel-render, motion-path or save-compatibility claims.
"""
from pathlib import Path
import sys,json,hashlib,itertools,struct,unittest
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];ROOT=H.parents[1]
sys.path.insert(0,str(ROOT/'p04-native-inventory-fix-reconstruction/inputs/verification'))
import host_vm as core
core.HERE=ROOT/'p04-native-inventory-fix-reconstruction/inputs/verification'
D=json.loads((ROOT/'p05-art-reconstruction/design-contract.json').read_text());META=json.loads((H/'interfaces.json').read_text());VMS=[]
def setup():
 vm=core.HostVM(checkpoint=H/'build/verification-checkpoint',build=H/'build',budget=20000000);VMS.append(vm)
 h=vm.objects['cakood'];p=vm.objects['p05State'];a=vm.objects['presentationAudio'];p.call('p05Init')
 h.p.update(location=5,onApron=0,presentation=0,motionX=26*64,motionY=140*64,motionPhase=0,motionLoop=0,motionPose=0,p05Visual=p,uiControlCount=0,uiFocus=-1,x=0,y=0)
 p.p.update(hHost=h,hBunnyRoom=5,hPAOwner=1,hPARoom=5,hCartOwner=1,hCartRoom=5,hSelectedMark=1)
 return vm,h,p,a

def controls(h):
 a=h.arrays
 return [{'obj':a['uiPayloads'][i],'rect':[a[n][i] for n in ['uiLefts','uiTops','uiRights','uiBottoms']],'label':core.read_string(a['uiLabels'][i]),'index':i} for i in range(h.p['uiControlCount'])]
def inside(r,x,y):return r[0]<=x<r[2] and r[1]<=y<r[3]
def hit(rows,x,y):return next((r['obj'] for r in rows[::-1] if inside(r['rect'],x,y)),0)
def native_hit(h,x,y):
 i=h.call('uiHit',x,y);return h.arrays['uiPayloads'][i] if i>=0 else 0
class Helpers(unittest.TestCase):
 def test_exact_mark_boundaries_and_same_x_different_y(self):
  v,h,p,a=setup()
  for x in range(250,301):
   for y in range(118,147):
    want=1 if inside([253,120,283,134],x,y) else 2 if inside([273,134,297,144],x,y) else 0
    self.assertEqual(p.call('hMarkAt',x,y),want,(x,y))
  self.assertEqual([p.call('hMarkAt',277,y) for y in [119,120,133,134,143,144]],[0,1,1,2,2,0])
 def test_keyboard_focus_capture_overrides_stale_pointer(self):
  v,h,p,a=setup();p.call('hWorldControls');rows=controls(h);marks=[r for r in rows if r['obj']==69]
  h.p.update(x=270,y=126)
  for row,want,xy in [(marks[1],2,[285,140]),(marks[0],1,[268,139])]:
   h.p['uiFocus']=row['index'];self.assertEqual(p.call('hCaptureTarget',69),want)
   self.assertEqual([p.call('hApproachX',69),p.call('hApproachY',69)],xy)
  h.p.update(uiFocus=-1,x=277,y=138);self.assertEqual(p.call('hCaptureTarget',69),2)
  h.p.update(x=270,y=138);self.assertEqual(p.call('hCaptureTarget',69),0);self.assertEqual(p.p['hSelectedMark'],2)
  for obj in [0,2,28,63,9,11]:self.assertEqual(p.call('hCaptureTarget',obj),0)
 def test_controls_priority_exhaustive_pixels_and_hud_boundaries(self):
  for present,cart,bunny in itertools.product([False,True],repeat=3):
   v,h,p,a=setup();p.p.update(hPARoom=5 if present else 4,hCartRoom=5 if cart else 4,hBunnyRoom=5 if bunny else 1)
   before=list(p.arrays['p05Words']);self.assertEqual(p.call('hWorldControls'),1);rows=controls(h)
   self.assertLessEqual(len(rows)+25,64);self.assertEqual(h.p['uiFailure'],0)
   actor_indices=[r['index'] for r in rows if r['obj'] in [2,28]]
   hardware=[r for r in rows if 63<=r['obj']<=72]
   self.assertTrue(all(r['index']<min(actor_indices) for r in hardware))
   self.assertEqual(sum(r['obj']==9 for r in rows),1)
   self.assertEqual(sum(r['obj']==69 for r in rows),2)
   self.assertEqual(any(r['obj']==72 for r in rows),cart)
   self.assertEqual(any(r['obj']==2 for r in rows),bunny)
   self.assertEqual(any(r['obj']==63 for r in rows),present)
   for row in rows:
    if row['obj']==32:continue
    l,t,r,b=row['rect'];self.assertTrue(0<=l<r<=320 and 44<=t<b<=144,row)
    for x,y in [(l,t),(r-1,b-1),(l,b-1),(r-1,t)]:self.assertEqual(native_hit(h,x,y),hit(rows,x,y))
   # Verify every target pixel: no late actor rectangle obscures any earlier
   # world target. Existing hardware overlap priorities follow contract order.
   nonactors=[r for r in rows if r['obj'] not in [2,28,32]]
   for y in range(44,144):
    for x in range(320):
     expected=hit(nonactors,x,y)
     if expected:self.assertEqual(hit(rows,x,y),expected,(present,cart,bunny,x,y))
   self.assertEqual(list(p.arrays['p05Words']),before)
 def test_approach_coordinates_match_contract(self):
  v,h,p,a=setup()
  for name,t in D['targets'].items():
   if t['object']==69:p.p['hSelectedMark']=t['listener']
   self.assertEqual([p.call('hApproachX',t['object']),p.call('hApproachY',t['object'])],t['approach'],name)
 def test_location_owner_and_apron_guards(self):
  v,h,p,a=setup()
  for room,apron in itertools.product(range(7),[0,1]):
   h.p.update(location=room,onApron=apron,uiControlCount=0);h.draws.clear()
   want=int(room==5 and not apron)
   self.assertEqual(p.call('hWorldControls'),want)
   self.assertEqual(p.call('hRenderWorld'),want)
   if not want:self.assertEqual(h.p['uiControlCount'],0);self.assertEqual(h.draws,[])
  for owner,room in itertools.product([0,1,2,4],[0,4,5]):
   p.p.update(hPAOwner=owner,hPARoom=room,hCartOwner=owner,hCartRoom=room)
   self.assertEqual(p.call('hKitVisible'),int(owner==1 and room==5));self.assertEqual(p.call('hCartVisible'),int(owner==1 and room==5))
 def test_render_all_twelve_hardware_states_and_loan_omission(self):
  v,h,p,a=setup()
  for connected,source,aim in itertools.product(range(2),range(2),range(3)):
   p.arrays['p05Words'][66:69]=[connected,source,aim];before=list(p.arrays['p05Words']);h.draws.clear();v.paint.clear()
   self.assertEqual(p.call('hRenderWorld'),1)
   expected=[(304,0),(227,14),(227,15),(227,7),(227,6 if connected else 5),(227,0),(227,9),(227,10+source),(227,13 if connected else 12),(227,4),(227,1+aim),(227,8),(219,0),(221,0),(214,0)]
   self.assertEqual([(r[0],r[2]) for r in h.draws],expected)
   self.assertEqual(v.paint,['TAPE','MIC','PORCH','EDGE']);self.assertEqual(list(p.arrays['p05Words']),before)
   for row in h.draws:
    if row[0]!=227:continue
    cel=next(x for x in D['components'] if x['cel']==row[2]);self.assertEqual(list(row[3:5]),cel['origin'])
  p.p['hPARoom']=4;h.draws.clear();v.paint.clear();p.call('hRenderWorld')
  self.assertEqual([r[2] for r in h.draws if r[0]==227],[14,15,7]);self.assertEqual(v.paint,['PORCH','EDGE'])
  p.p['hCartRoom']=4;h.draws.clear();p.call('hRenderWorld');self.assertEqual([r[2] for r in h.draws if r[0]==227],[14,15])
 def test_actor_anchors_depth_speech_and_absence(self):
  v,h,p,a=setup()
  for feet in [126,127,128,129,140]:
   h.p['motionY']=feet*64;h.draws.clear();p.call('hRenderWorld');actors=[r[0] for r in h.draws if r[0] in [214,219,221]]
   self.assertEqual(actors,[214,219,221] if feet<127 else [219,214,221] if feet<129 else [219,221,214])
  h.p['presentation']=a
  for who,speaker,view,origin in [(2,2,219,[245,57]),(28,5,221,[77,59])]:
   for mouth in [0,1,2,3,-1]:
    a.p.update(lane=1,speaker=speaker,mouth=mouth);h.draws.clear();self.assertEqual(p.call('hDrawActor',who),1)
    row=h.draws[-1];self.assertEqual([row[0],row[2],*row[3:5],*row[6:]],[view,mouth if mouth in [0,1,2] else 0,*origin,116,116])
   a.p.update(lane=1,speaker=speaker,mouth=2);h.p['motionPhase']=1;h.draws.clear();p.call('hDrawActor',who);self.assertEqual(h.draws[-1][2],0);h.p['motionPhase']=0
  p.p['hBunnyRoom']=1;h.draws.clear();self.assertEqual(p.call('hDrawActor',2),0);p.call('hRenderWorld');self.assertNotIn(219,[r[0] for r in h.draws])
 def test_native_text_labels_distinct_stable_and_compact(self):
  v,h,p,a=setup();pointers={};texts=v.resources[3,205].split(b'\0');font=v.resources[7,0]
  for o,entry in META['label_entries'].items():
   obj=int(o);ptr=p.call('hLabel',obj);pointers[obj]=ptr;self.assertEqual(core.read_string(ptr),texts[entry].decode('latin1'))
   s=core.read_string(p.call('hShortLabel',obj));width=sum(font[struct.unpack_from('<H',font,6+ord(c)*2)[0]] for c in s)
   self.assertLessEqual(width,32);self.assertLessEqual(struct.unpack_from('<H',font,4)[0],10)
   self.assertGreaterEqual(ptr.region.limit(ptr.offset)-ptr.offset,len(texts[entry])+1)
  self.assertEqual(len({(id(p.region),p.offset) for p in pointers.values()}),10)
  for o,ptr in pointers.items():self.assertEqual(core.read_string(ptr),texts[META['label_entries'][str(o)]].decode('latin1'))
  self.assertEqual(p.call('hLabel',999),0);self.assertEqual(p.call('hShortLabel',999),0)
 def test_unchanged_original_domain_and_inputs(self):
  sys.path.insert(0,str(H.parent/'tools'));from source_tools import spans
  original=(ROOT/'p05-domain-reconstruction/src/module985.sc').read_text();fixture=(H/'build/src/module985.sc').read_text()
  for k,(a,b) in spans(original).items():
   aa,bb=spans(fixture)[k];self.assertEqual(original[a:b],fixture[aa:bb],k)
  pins=json.loads((H/'evidence/input-pins.json').read_text())
  for path,expected in pins.items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),expected)
  lay=json.loads((H/'build/layout-985.json').read_text());self.assertEqual([x['species'] for x in lay['objects'] if x['is_class']],[7])
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Helpers))
 report={'status':'PASS_EMITTED_VISUAL_HELPERS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'instructions':sum(v.steps for v in VMS),'native_acceptance':False,'pixel_render_acceptance':False,'scope':'Fresh emitted SCI render traces, authoritative physical-owner gates, controls, exhaustive target pixel ownership, exact marks, stable text205 labels and measured font0 compact widths','vm_source_sha256':hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest()}
 (H/'evidence/tests.json').write_text(json.dumps(report,indent=2)+'\n');sys.exit(not result.wasSuccessful())
