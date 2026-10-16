"""Small emitted rendering regressions, not a campaign or native acceptance run.

Credit visibility and final-pose waiting use explicit unit fixtures for read-only
scene/page validators. They cannot earn campaign progression or forge save proof.
The compiled branch, owner/page/token comparisons and painting execute unchanged.
"""
from presentation_vm import PresentationVM,S,base
import sys,json,time,resource
class FixtureVM(PresentationVM):
 def __init__(self):
  super().__init__();self.root_source=53;self.replay_source=29;self.replay_active=0
  self.root_reader_ok=1;self.replay_reader_ok=1;self.claims=0
 def call(self,o,name,args=()):
  n=o.module.number
  if n==996:
   if name in ('h14Valid','h14Base'):return 1
   if name=='h14RawRoom':return -1
   if name=='h14ReaderCheck':return self.root_reader_ok
   if name=='p14CurrentSource':return self.root_source
  if n==997:
   if name=='h14ReplayActive':return self.replay_active
   if name=='p14CurrentSource':return self.replay_source
   if name=='h14ReplayCheck':return self.replay_reader_ok
  if n==993:
   if name in ('h11PayGuard','h11ReaderCheck','p11Complete'):return 1
   if name=='p11ClaimLaugh':self.claims+=1;return 0
  if n==0 and name=='h11RenderLive':return 1
  return super().call(o,name,args)
def run(case):
 v=FixtureVM() if case!='opening_geometry' else PresentationVM()
 if case=='credit_overlay':
  root=v.instance(996);root.p['p14Phase']=5;v.h.p['uiPanel']=4;v.h.p['location']=0;v.arrays(996)['h14Reader'][2]=53
  def painted():
   v.paint.clear();v.call(root,'h14Draw');return any('FINAL AUDIENCE CELEBRATION' in x for x in v.paint)
  assert painted()
  v.replay_active=1
  for source in [29,30,52,54,59,61]:v.replay_source=source;assert not painted(),source
  v.replay_source=53;assert painted()
  v.replay_reader_ok=0;assert not painted()
  v.replay_active=0;v.root_reader_ok=0;assert not painted()
  v.root_reader_ok=1;v.h.p['uiPanel']=2;assert not painted()
  v.h.p['uiPanel']=4;v.arrays(996)['h14Reader'][2]=52;assert not painted()
  detail={'cases':12,'scope':'actual emitted overlay with read-only reader validators modeled','root_source_held_at':53}
 elif case=='opening_geometry':
  art=json.loads((S/'OPENING-ASSET-MANIFEST.json').read_text())
  for card,g in enumerate(art['geometry'],1):
   for tick in [0,119,120,359]:
    for reduced in [0,1]:
     v.h.draws.clear();assert v.proc(970,8,card,tick,reduced)==1;draws=v.h.draws
     assert draws[0][:3]==(g['background_view'],0,0)
     loop0=[d for d in draws if d[0]==g['view'] and d[1]==0];assert len(loop0)==1
     assert loop0[0][3:5]==tuple(g['loop0']['draw'])
     assert loop0[0][2]==v.proc(970,2,card,tick,reduced)
     freeze=bool(reduced or tick>=120)
     for loop in [1,2]:
      got=[d for d in draws if d[0]==g['view'] and d[1]==loop];assert bool(got)==freeze
      if got:assert got[0][3:5]==tuple(g[f'loop{loop}']['draw'])
     for prop in g['stable_prop_loops']:
      got=[d for d in draws if d[0]==g['view'] and d[1]==prop['loop']];assert len(got)==1 and got[0][3:5]==tuple(prop['draw'])
      assert draws.index(got[0])<draws.index(loop0[0])
  for card in [0,9]:
   v.h.draws.clear();assert v.proc(970,8,card,0,0)==1;assert v.h.draws==[(250,3,0,16,30,-1,0)]
  assert v.proc(970,8,10,0,0)==0
  detail={'projection_cases':66,'poses':64,'native_pixels':False}
 elif case in ('laf11_wait','laf11_timeout','laf11_token_cancel','laf11_page_cancel'):
  obj=v.instance(993);a=v.arrays(993);p=a['h11Pay'];r=a['h11Reader'];d=v.h.p['dialogue']
  p[0]=3;p[1]=13;p[17]=11;p[15]=12;p[16]=13;p[20]=p[18]=4
  r[1]=11;r[4]=12;r[5]=13;r[15]=1;a['h11Read'][0]=2
  v.h.p['uiPanel']=4;d.p['sdGeneration']=d.p['sdPaintGeneration']=1;d.p['sdArmed']=1
  v.a.p['token']=7;v.now=100
  def frame():p[11]=p[12]=1;p[13]=13;return v.call(obj,'h11PayFrame',(1,))
  assert frame()==1 and p[0]==3 and p[28]==1 and v.claims==0
  v.now=200;assert frame()==1 and p[0]==3 and v.claims==0
  if case=='laf11_wait':
   d.p['sdArmed']=0;v.audio_position=-1;assert frame()==1 and p[0]==0 and v.claims==1
   assert v.call(obj,'h11PayFrame',(1,))==0 and v.claims==1
  else:
   if case=='laf11_timeout':v.now=281
   elif case=='laf11_token_cancel':v.a.p['token']=8
   else:r[5]=14
   assert frame()==0 and p[0]==0 and v.claims==0
  detail={'scope':'final pose wait unit fixture; domain claim mocked and not campaign evidence','claimed':v.claims}
 elif case=='p14_cast_layering':
  class LayerVM(FixtureVM):
   def __init__(self,room=4,panel=0,valid=1,base_ok=1,apron=0):
    super().__init__();self.valid_admit=valid;self.base_admit=base_ok;self.actor_room=room
    self.h.p.update(location=room,uiPanel=panel,onApron=apron,uiDocument=0)
    self.instance(996).p.update(p14Phase=4,p14SignatureLo=1,
     p14PinJackLo=1,p14PinBunnyLo=1,p14PinFrankieLo=1,p14PinMiloLo=1,
     p14PinVivianLo=1,p14PinRitaLo=1,p14PinFelixLo=1,p14PinStringerLo=1)
   def call(self,o,name,args=()):
    if o.module.number==996:
     if name=='h14Valid':return self.valid_admit
     if name=='h14Base':return self.base_admit
     if name=='h14RawRoom':return self.actor_room
    return super().call(o,name,args)
  checks=[]
  for panel in (0,2,4):
   q=LayerVM(panel=panel);q.ktrace.clear();assert q.call(q.instance(996),'h14Draw')==1
   events=q.ktrace
   cast=[i for i,(name,args) in enumerate(events) if name=='DrawCel' and args[0] in (219,218,221,236,223,225,222) and args[1]==1]
   props=[i for i,(name,args) in enumerate(events) if name=='DrawCel' and args[:3] in ((234,0,9),(227,0,7),(224,0,10))]
   board=[i for i,(name,args) in enumerate(events) if name=='Graph' and args[0]==11]
   signed=[i for i,(name,args) in enumerate(events) if name=='Display' and base.read_string(args[0])=='SIGNED']
   assert len(cast)==7 and len(props)==3 and len(board)==9 and len(signed)==1
   assert max(props+board+signed)<min(cast),('Court cargo or board paints over the cast',panel,props,board,signed,cast)
   actual=[tuple(args) for name,args in events if name=='DrawCel']
   assert actual[:3]==[(234,0,9,92,111,-1,0),(227,0,7,205,93,-1,0),(224,0,10,205,69,-1,0)]
   assert actual[3:]==[(view,1,0,24+41*i,64,-1,96,96) for i,view in enumerate((219,218,221,236,223,225,222))]
   checks.append({'panel':panel,'cast':len(cast),'props':len(props),'board_and_pin_graphs':len(board),'signed':len(signed)})
  for room in (0,1):
   q=LayerVM(room=room);q.ktrace.clear();assert q.call(q.instance(996),'h14Draw')==1
   draws=[args for name,args in q.ktrace if name=='DrawCel'];assert len(draws)==7
   assert not any(name=='Graph' for name,args in q.ktrace)
   words=[base.read_string(args[0]) for name,args in q.ktrace if name=='Display']
   assert words==(['The End'] if room==1 else [])
  for kwargs in ({'valid':0},{'base_ok':0},{'apron':1}):
   q=LayerVM(**kwargs);q.ktrace.clear();assert q.call(q.instance(996),'h14Draw')==0
   assert not any(name in ('DrawCel','Graph','Display') for name,args in q.ktrace)
  detail={'court_cases':checks,'non_court_cases':2,'rejected_guard_cases':3,
   'scope':'explicit room and read-only valid/base admissions; actual emitted painter order, original draw arguments, board pins, SIGNED, The End and rejection guards; not earned native progress'}
 else:raise ValueError(case)
 return {'status':'PASS_EMITTED_NOT_NATIVE','case':case,'instructions':v.steps,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,**detail}
if __name__=='__main__':print(json.dumps(run(sys.argv[1])))
