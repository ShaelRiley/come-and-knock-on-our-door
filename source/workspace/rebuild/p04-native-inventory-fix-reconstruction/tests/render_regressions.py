#!/usr/bin/env python3
"""Actual emitted world/frame regression for the native inventory failure.
No game method is replaced. Only deterministic graphics/audio kernels are mocked.
TextSize output stores and accumulator preservation are checked against stock API.
"""
from pathlib import Path
import hashlib,json,struct,sys,unittest
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'inputs/verification'))
import host_vm as base
base.HERE=H/'inputs/verification'
VMS=[]
class MeasuredVM(base.HostVM):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.measurements=[];self.text_reads=[]
 def _kernel(self,k,args):
  name=self.knames.get(k)
  if name=='TextSize':
   dest,text,font,width=args;before=list(dest.region.words);prior=self._kernel_accumulator
   value=super()._kernel(k,args);start=dest.offset//2;after=dest.region.words
   if before[:start]!=after[:start] or before[start+4:]!=after[start+4:]:raise AssertionError('TextSize escaped its4-word destination')
   self.measurements.append({'text':base.read_string(text),'width_limit':width,'rect':after[start:start+4],'destination':dest.region.name,'word_offset':start})
   return prior # Stock kTextSize preserves r_acc; UI consumes written height.
  if name=='GetFarText':
   result=super()._kernel(k,args);dest=args[2]
   self.text_reads.append({'resource':args[0],'entry':args[1],'bytes_with_nul':len(base.read_string(dest).encode('latin1'))+1,'capacity_bytes':dest.region.limit(dest.offset)-dest.offset})
   return result
  return super()._kernel(k,args)

def setup(old=False):
 B=H/'reference/accepted/build' if old else H/'staging-proof'
 vm=MeasuredVM(checkpoint=B/'verification-checkpoint',build=B,budget=10000000);VMS.append(vm)
 h,d,a,p,q=[vm.objects[n] for n in ('cakood','sceneDialogue','presentationAudio','p03State','p04State')]
 h.p.update(dialogue=d,presentation=a,p03=p,p04=q,opening=0,initialized=1,houseEntered=1,traySafe=1,tray=2,location=3,roomSeen=3,wedge=1)
 h.call('p02Init');p.call('p03Init');q.call('p04Init');p.p['bEnabled']=1
 h.p.update(p02PlanAgreed=1,p02CopyJack=14,p02CopyBunny=14,p02CopyStringer=14,p02MasterHeld=1,p02Observed=63,p02BoardRecords=7,p02Compared=1,p02KnowPurpose=1,p02KnowOrder=1,p02SelectedAims=7)
 q.p['qEnabled']=q.call('qRoutesReady',h);h.call('p02SyncInventory',0);h.call('p02HostInventory')
 return h,d,a,p,q

def frame(h,allow_failure=False):
 h.p['dirty']=1;h.vm.pump([{}]);
 if not allow_failure:assert h.p['uiFailure']==0,h.p['uiFailure']

def close_scenes(h,world=True,allow_failure=False):
 for _ in range(20):
  if h.p['uiPanel'] not in (1,4):break
  for page in range(h.p['uiPageCount']):
   if h.p['uiPage']!=page:h.call('uiTurnPage',page-h.p['uiPage'])
   frame(h,allow_failure)
  h.call('uiClose')
 if world:frame(h,allow_failure)

def act(h,verb,obj,target=0,allow_failure=False):
 if h.p['uiPanel']:close_scenes(h,allow_failure=allow_failure)
 h.call('hostActNow',verb,obj,target)
 close_scenes(h,allow_failure=allow_failure)

def pull(h,old=False):
 for action in ((2,60),(7,4,60),(9,62)):act(h,*action,allow_failure=old)

def inventory(h):
 h.call('uiBuildFocus');rows=[]
 for i in range(h.p['uiControlCount']):
  if h.arrays['uiActions'][i]==3:
   rect=[h.arrays[n][i] for n in ('uiLefts','uiTops','uiRights','uiBottoms')]
   rows.append({'obj':h.arrays['uiPayloads'][i],'label':base.read_string(h.arrays['uiLabels'][i]),'rect':rect,'width_limit':rect[2]-rect[0]-4,'height_limit':rect[3]-rect[1]-2})
 return rows

class RenderRegression(unittest.TestCase):
 def test_old_seal_fails_on_first_room3_world_frame_after_pull_without_travel(self):
  h,d,a,p,q=setup(old=True);pull(h,old=True)
  self.assertEqual((h.p['location'],q.p['p04Bunting'],q.p['p04Wedge'],q.p['qFailure'],h.p['uiFailure']),(3,1,1,0,9))
  badge=next(r for r in inventory(h) if r['obj']==62)
  self.assertEqual((badge['label'],badge['width_limit'],badge['height_limit']),('Welcome bunting',32,10))
  samples=[r for r in h.vm.measurements if r['text']=='Welcome bunting' and r['width_limit']==32]
  self.assertTrue(samples);self.assertTrue(any(r['rect'][2]>10 for r in samples))
  self.assertTrue(any('UICONTRACTERROR9' in s.replace(' ','') for s in h.vm.paint))

 def test_compact_badge_fits_real_font_and_full_name_is_unchanged(self):
  h,d,a,p,q=setup();before=h.vm.kernel_calls['GetFarText']
  self.assertEqual(base.read_string(h.call('uiHostShortLabel',62)),'BUNT.')
  self.assertEqual(base.read_string(h.call('uiHostItemLabel',62)),'Welcome bunting')
  self.assertEqual(h.vm.kernel_calls['GetFarText'],before)
  font=h.vm.resources[7,0];widths=[]
  for c in 'BUNT.':off=struct.unpack_from('<H',font,6+ord(c)*2)[0];widths.append(font[off])
  self.assertEqual(sum(widths),30);self.assertEqual(struct.unpack_from('<H',font,4)[0],8)
  pull(h);badge=next(r for r in inventory(h) if r['obj']==62);self.assertEqual(badge['label'],'BUNT.')
  self.assertTrue(all(r['rect'][2]<=10 for r in h.vm.measurements if r['text']=='BUNT.' and r['width_limit']==32))

 def test_all_rooms_travel_physical_support_and_retrieval_world_frames(self):
  h,d,a,p,q=setup();pull(h)
  # Real campaign exits, with a world frame after every scene/arrival boundary.
  visited={h.p['location']}
  for verb,obj,target in ((0,17,0),(0,16,0),(0,17,0),(0,15,0),(0,17,0),(2,1,0),(0,1,0),(0,12,0),(0,18,0),(0,13,0),(0,19,0)):
   act(h,verb,obj,target);visited.add(h.p['location'])
   self.assertEqual(h.arrays['uiItems'].count(62),1)
  self.assertEqual(visited,set(range(7)))
  self.assertEqual(h.p['location'],3)
  for args in ((7,62,55),(4,4),(8,60),(2,60),(7,56),(9,62),(7,62,55),(9,56)):
   act(h,*args);self.assertEqual(h.p['uiFailure'],0)
  self.assertEqual(q.call('p04Ready'),1)

 def test_cross_branch_publication_reward_and_restore_render_every_boundary(self):
  for reserved in (True,False):
   h,d,a,p,q=setup();pull(h)
   if not reserved:act(h,4,4)
   for args in ((0,17),(0,16),(5,37),(7,25,40)):act(h,*args)
   h.call('uiHostChoice',204,1);close_scenes(h)
   if h.p['uiPanel']:h.call('uiClose');frame(h)
   for args in ((0,17),(2,1),(0,1),(0,12),(4,39),(0,18),(0,17),(0,16),(7,39,34),(1,40,30)):act(h,*args)
   self.assertEqual((p.p['p03Ready'],q.p['p04Bunting'],h.arrays['uiItems'].count(62),h.arrays['uiItems'].count(35)),(1,1,1,1))
   state=json.loads(json.dumps(h.vm.snapshot()));oldvm=h.vm;h2,d2,a2,p2,q2=setup();h=h2.vm.restore(state)
   h.call('bridgeAfterRestore');h.p['dialogue'].call('sdAfterRestore',h.p['presentation']);h.call('p03Restore');h.call('p04Restore');frame(h)
   self.assertEqual((h.arrays['uiItems'].count(62),h.p['p04'].p['qFailure']),(1,0))

 def test_repeated_projection_and_inventory_focus_keep_bounds(self):
  h,d,a,p,q=setup();pull(h)
  # Duplicate projection and focus movement use the real control/render paths.
  for _ in range(3):p.call('bInventory',h);h.call('p02HostInventory');frame(h)
  h.call('uiBuildFocus');slot=next(i for i in range(h.p['uiControlCount']) if h.arrays['uiActions'][i]==3 and h.arrays['uiPayloads'][i]==62)
  h.p['uiFocus']=slot;h.p['uiReveal']=1;frame(h)
  self.assertEqual(h.p['uiFailure'],0)
  self.assertEqual(h.arrays['uiItems'].count(62),1)

if __name__=='__main__':
 if sys.flags.optimize:raise SystemExit('Use normal Python for assertions')
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(RenderRegression);result=unittest.TextTestRunner(verbosity=2).run(suite)
 report={'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':[(str(t),s) for t,s in result.failures],'errors':[(str(t),s) for t,s in result.errors],'instructions':sum(v.steps for v in VMS),'frames':sum(v.frames for v in VMS),'textsize_calls':sum(len(v.measurements) for v in VMS),'getfartext_calls':sum(len(v.text_reads) for v in VMS),'textsize_contract':'four bounded output words; output height at word2; stock accumulator preserved; font0 six-pixel glyph metrics verified; general wrap remains deterministic mock','native_acceptance':False}
 (H/'evidence/render-regressions.json').write_text(json.dumps(report,indent=2)+'\n');raise SystemExit(not result.wasSuccessful())
