"""Pure geometry, ordinary early-room traces, and explicit inactive UI checks."""
from pathlib import Path
import json,sys,unittest
import host
from source_host import VM as SourceVM
from test_return_caption import boot,first_entry
from host import act,close
H=host.H;sys.path.insert(0,str(H));EMITTED=host.VM
C=json.loads((H/'GEOMETRY-CONTRACT.json').read_text())
def fresh(source=False,root=H):
 old=host.VM;host.VM=SourceVM if source else EMITTED
 try:return boot(root)
 finally:host.VM=old
def conservatory(source=False,root=H):
 h=fresh(source,root);first_entry(h,'bunny');act(h,0,17);act(h,0,16);close(h)
 assert h.p['location']==6 and not h.p['onApron'];return h
def image(q):return dict(q.p),{n:list(v) for n,v in q.arrays.items()}
def trace(vm):return [(n,tuple(host.base.read_string(v) if n=='Display' and i==0 and isinstance(v,host.base.Pointer) else v for i,v in enumerate(a))) for n,a in vm.ktrace]
class Scaffold(unittest.TestCase):
 def test_01_every_geometry_value_and_exact_label_is_pure(self):
  expected=[[c['id'],*c['rect'],*c['approach'],c['default']] for c in C['controls']]
  expected += [[396,*t['rect'],t['thread'][0],t['thread'][1],1] for t in C['tag_shapes']]
  for VM in (EMITTED,SourceVM):
   vm=VM();q=vm.objects['p09State'];before=image(q)
   self.assertEqual([[q.call('h9Geo',r,f) for f in range(8)] for r in range(10)],expected)
   for r,f in [(-1,0),(10,0),(32767,0),(0,-1),(0,8),(0,32767)]:self.assertEqual(q.call('h9Geo',r,f),-1)
   for obj,label in C['labels'].items():self.assertEqual(host.base.read_string(q.call('h9Label',int(obj))),label)
   self.assertEqual(image(q),before)

 def test_02_pure_control_fixture_preserves_half_open_reverse_hit_order(self):
  # This is an isolated UI-array fixture, not campaign activation or progress.
  for VM in (EMITTED,SourceVM):
   vm=VM();h=vm.objects['cakood'];q=vm.objects['p09State'];before=image(q)
   h.p['uiControlCount']=0
   rows=[]
   for i in range(7):
    obj,t,l,b,r,*_= [q.call('h9Geo',i,f) for f in range(8)]
    h.call('uiAddControl',1,obj,t,l,b,r,q.call('h9Label',obj));rows.append((obj,t,l,b,r))
   points=set()
   for _,t,l,b,r in rows:points.update([(l,t),(r-1,b-1),(r,b),(l-1,t),(l,t-1),((l+r)//2,(t+b)//2)])
   for x,y in points:
    expected=next((i for i in reversed(range(7)) if rows[i][2]<=x<rows[i][4] and rows[i][1]<=y<rows[i][3]),-1)
    self.assertEqual(h.call('uiHit',x,y),expected)
   self.assertEqual(rows[h.call('uiHit',190,80)][0],396)
   self.assertEqual([q.call('h9Geo',i,7) for i in range(7)],[5,5,5,5,5,0,0])
   self.assertEqual(q.call('h9Active'),0);self.assertEqual(image(q),before)

 def test_03_actual_conservatory_render_and_controls_match_accepted_foundation(self):
  baseline=conservatory(False,H/'frozen/foundation');baseline.vm.ktrace.clear();baseline.call('drawWorld');expected=trace(baseline.vm)
  baseline.call('uiBuildFocus');expected_controls={n:list(baseline.arrays[n]) for n in ['uiActions','uiPayloads','uiTops','uiLefts','uiBottoms','uiRights']}
  for source in (False,True):
   h=conservatory(source);q=h.vm.objects['p09State'];s=h.vm.objects['p08State'];before=image(q)
   self.assertEqual((s.call('h8ActorRoom',4),s.call('h8ActorRoom',7)),(6,6))
   self.assertEqual((s.call('h8EveningCommitted'),s.call('h8EveningReady'),q.call('h9Active')),(0,0,0))
   h.vm.ktrace.clear();h.call('drawWorld');self.assertEqual(trace(h.vm),expected)
   h.call('uiBuildFocus');self.assertEqual({n:list(h.arrays[n]) for n in expected_controls},expected_controls)
   self.assertFalse(any(395<=n<=399 for n in h.arrays['uiPayloads']))
   self.assertEqual(image(q),before)

 def test_04_actual_room_modal_and_history_barriers_never_publish(self):
  for source in (False,True):
   h=conservatory(source);q=h.vm.objects['p09State'];before=image(q)
   calls=[]
   h.vm.after_actual_call=lambda obj,name,args,result:calls.append((obj.name,name))
   for mode in (-1,0,1,2):
    controls=h.p['uiControlCount'];trace=len(h.vm.ktrace);self.assertEqual(q.call('h9UI',mode),0)
    self.assertEqual(h.p['uiControlCount'],controls);self.assertEqual(len(h.vm.ktrace),trace)
   self.assertIn(('p08State','h8EveningCommitted'),calls)
   self.assertNotIn(('p08State','h8EveningReady'),calls) # No committed history exists.
   # Temporary presentation-mode fixtures only; actor rooms and story history stay real.
   for prop in ('opening','paused','menuOpen','uiPanel','bridgeReaderActive','uiFailure','bridgeFailure'):
    prior=h.p[prop];h.p[prop]=1;calls.clear()
    for mode in (0,1):self.assertEqual(q.call('h9UI',mode),0)
    self.assertNotIn(('p08State','h8EveningCommitted'),calls)
    h.p[prop]=prior
   prior=h.p['motionPhase'];h.p['motionPhase']=1;calls.clear()
   self.assertEqual(q.call('h9UI',0),0);self.assertNotIn(('p08State','h8EveningCommitted'),calls)
   self.assertEqual(q.call('h9UI',1),0);self.assertIn(('p08State','h8EveningCommitted'),calls)
   h.p['motionPhase']=prior
   self.assertEqual(image(q),before)

if __name__=='__main__':unittest.main(verbosity=2)
