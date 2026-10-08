"""NEW finite reference join fixture. No native/visual/host execution claim.

The P07/P11/P12 owners earn their own states. Other completed early-campaign
preparations are explicit accepted initial inputs. Actor routes below are
simulated, observed logical paths, never a claim that sprites were rendered.
"""
import copy,json,tempfile
from pathlib import Path
from dataclasses import replace
from cakood.p12_model import P12World,P12Context,CurrentRig,PEOPLE,COURTYARD,KITCHEN,LIVING,SIDE,PORCH
from cakood.p13_model import P13World,P13Context
from cakood.p10_model import P10World,P10Context,TILE_IDS,ORDER
from cakood.p09_model import P09World,P09Context
from cakood.p11_model import P11World,P11Context
from cakood.p04_model import project_gate
from cakood.p08_model import P08World,P08Context,PREPARATIONS,Position,READINESS_RECORDS
from dependencies.p03_numeric_model import P03
from dependencies.p04_numeric_model import P04,Obj,Bunting
from dependencies.p07_owner.cakood.p07_model import P07World,P07Context,Source,Action,Measure,P13Handoff,OwnedObject
from dependencies.p07_owner.cakood.composition import MemoryTransactionHost
from test_verbal_contest import prepared,play,leave


def require(condition,message):
 if not condition:raise RuntimeError(message)

def shown(w,c,s,trace=None):
 p=w.begin_presentation(c,s)
 require(p.presentation_id is not None,'Scene not admitted '+s+': '+p.code)
 # Actual finite renderer boundary: every exact token is selected and logged
 # before its receipt. This verifies ledger behavior, not pixels/audio.
 tokens=w._tokens(s)
 if trace is not None:trace.append({'kind':'canonical-caption','source':s,'record':w.SOURCES[s],'tokens':tokens})
 r=w.acknowledge_presentation(c,p.presentation_id,record_id=w.SOURCES[s])
 require(w._complete(s),'Incomplete '+s)
 return r

def make_gate():
 p=P04();p.context(3,0,1,1);p.topic(Obj.FELIX,1);p.open_gate();p.place_wedge()
 p.context(3,0,1,0);p.move_bunting(Bunting.HELD);p.move_bunting(Bunting.HOOK);p.recover_wedge()
 p.context(3,0,1,1);p.close_gate(1);p.open_gate()
 require(p.tested and p.validate(),'Current P04 not genuinely tested')
 return p

def cook_pot():
 p=P07World();c=P07Context(KITCHEN,flags=frozenset({'PLAN_AGREED'}),bunny_room=KITCHEN)
 h=MemoryTransactionHost(p,c);reads=[]
 p.perform(c,Action.INTRODUCE,host=h)
 for source in Source:
  r=p.open_source(c,source,host=h)
  for page in r.pages:
   reads.append({'record_id':page.record_id,'text':page.text,'sha256':page.sha256})
   p.acknowledge_source_page(c,r.token,page,host=h)
 for action in (Action.ADD_BASE,Action.MEASURE_STOCK,Action.ADD_STOCK,Action.ADD_VEGETABLES,Action.COOK,Action.TURN_HEAT_OFF,Action.ADD_HERBS,Action.CLOSE_LID):
  kw={'measure':Measure.EIGHT_TASTING_BOWLS} if action==Action.MEASURE_STOCK else {}
  p.perform(c,action,host=h,**kw)
 require('FOOD_READY' in p.flags,'Pot not cooked')
 return p,c,h,reads

def pot_projection(p,c):
 q=p.projection(c);pot=next(x for x in q.objects if x.object_id=='hotpot_pot')
 require(pot.owner=='P07' and pot.location=='kitchen_waiting' and set(q.contents)=={'base','stock','vegetables','herbs'} and not q.heat_on,'Wrong original pot')
 return dict(object_id=pot.object_id,room=pot.room,lid_closed=q.lid_closed,portions=q.tasting_bowls,portion_kind='tasting',includes_jackie=q.includes_jackie)

class Joined:
 def __init__(self,preengaged=False,vc03win=False):
  self.trace=[];self.p7,self.c7,self.h7,self.p7_reads=cook_pot();self.p4=make_gate()
  p3=P03();p3.context(6,0,1,1);p3.look(37);p3.begin_credit();p3.select(1)
  p3.context(2,0,1,1);p3.collect(38);p3.context(6,0,1,1);p3.pad(38);p3.give_slate();self.p3=p3
  require(p3.inventory()==[35],'Actual P03 tiles not earned')
  # Accepted completed early inputs for P05/P06. Their production host join is
  # outside this finite gate; P03/P04/P07 states above are genuine owner actions.
  self.p8=P08World();self.c8=P08Context(COURTYARD,flags=PREPARATIONS,carrier_padding='clean_napkin',frankie_room=COURTYARD,bunny_room=COURTYARD)
  for source,record in (('circulation_plan','P08.READ.001'),('sightline_plan','P08.READ.002'),('placement_symbols','P08.READ.003'),('credit_slate','P08.READ.004')):
   self.p8.acknowledge_source(self.c8,source,record)
  for obj,pos in (('ceramic_carrier',Position.HATCH),('serving_table',Position.HATCH),('credit_slate',Position.HATCH),('pa_kit',Position.WALL),('completed_screen',Position.ALCOVE)):
   self.p8.place(self.c8,obj,pos)
  self.p8.unpack_service(self.c8)
  for x in self.p8.pending_handoffs:self.p8.acknowledge_handoff(x['handoff_id'],x['serial'])
  self.p8.request_start(self.c8);token=self.p8.pending_request_id
  self.p8.acknowledge_readiness(self.c8,token,READINESS_RECORDS);self.p8.confirm_start(self.c8,token,True)
  # A real temporary-file write and readback precede the reference I/O receipt.
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/'pre-evening.json';path.write_text(json.dumps(self.p8.save()));require(json.loads(path.read_text())==self.p8.save(),'P08 local snapshot failed')
   self.p8.acknowledge_autosave(self.c8,token,True)
  require(self.p8.evening_started,'P08 evening not started')
  flags=frozenset({'PLAN_AGREED'})|self.p8.flags|self.p7.flags
  self.p9=P09World();c9=P09Context('L07_CONSERVATORY',flags=flags)
  for source,record in (('direct_question','P09.DIALOGUE.001'),('terms','P09.DIALOGUE.002')):
   r=self.p9.begin_presentation(c9,source);self.p9.acknowledge_presentation(c9,r.presentation_id,record_id=record)
  flags|=self.p9.flags;self.p10=P10World();pocket=set((*TILE_IDS,'grease_pencil','master_invitation'))
  c10=P10Context(LIVING,flags=flags,inventory=frozenset(pocket));self.p10.introduce(c10);shown(self.p10,c10,'plan',self.trace)
  for cue,word in zip(TILE_IDS,ORDER):self.p10.write(c10,cue,word)
  for i,cue in enumerate(TILE_IDS):self.p10.place(replace(c10,room=COURTYARD,inventory=frozenset(pocket)),cue,i);pocket.discard(cue)
  require(self.p10.ready,'P10 rack not restored');flags|=self.p10.flags
  if preengaged:self.p4.set_peg(1)
  self.p11=P11World();c11=P11Context(SIDE,project_gate(self.p4),flags=flags)
  self.p11.lift(c11)
  if not preengaged:
   self.p11.request_peg(c11);request=self.p11.pending_peg_request_id
   self.p4.set_peg(1);c11=replace(c11,gate=project_gate(self.p4));self.p11.acknowledge_peg(c11,request)
  self.p11.release_catch(c11);self.p11.pull_handle(c11);self.p11.stage_display(c11);shown(self.p11,c11,'sincere',self.trace)
  request=self.p11.request_contest(c11);require(request.code=='contest_requested','Real VC03 entry missing')
  rescue=P11World.load(self.p11.save(),context=c11);self.p11.acknowledge_contest_request(c11,self.p11.pending_contest_request_id)
  self.vc=prepared('VC03');play(self.vc,[vc03win]*3,'VC03');self.vc03_captions=[];leave(self.vc,rescue=rescue,shown=self.vc03_captions)
  flags|=self.p11.flags;self.flags=flags;self.p12=P12World()
  self.actors={p:COURTYARD for p in PEOPLE[1:]}
  self.rig=CurrentRig(COURTYARD,True,'MIC',self.p8.conditions['sound_facing_inward'])
  self.c12=P12Context(COURTYARD,flags=flags,npc_locations=tuple(self.actors.items()),rig=self.rig,contests=self.vc)
  self.p12.start(self.c12,self.p10.cue_handoff);apron=replace(self.c12,on_apron=True)
  shown(self.p12,apron,'self_view',self.trace);self.p12.release_catch(apron);self.p12.rotate_rack(self.c12);self.p12.order_cards(self.c12,TILE_IDS)
  shown(self.p12,self.c12,'introduction',self.trace);self.p12.commit_introduction(self.c12)
  self.w=P13World();self.queue_clear=False;self.board_room=LIVING;self.physical={'hotpot_pot':('P07',KITCHEN),'folded_display':('P11',SIDE),'handcart':('P11',SIDE)}

 def cleanup(self):
  self.p12.release_confetti(self.c12);shown(self.p12,self.c12,'confetti',self.trace);shown(self.p12,self.c12,'cleanup',self.trace)
  result=self.p12.finish_welcome(self.c12)
  for actor,destination in result.events[0].payload['destinations'].items():self.move(actor,destination,'P12_COLLECTION_START')
  self.flags|=self.p12.flags
  return result

 def move(self,actor,destination,cause):
  # Short bounded legal logical paths. No inferred arrival from elapsed time.
  edges={(LIVING,KITCHEN),(LIVING,PORCH),(LIVING,SIDE),(LIVING,COURTYARD),(SIDE,COURTYARD)}
  graph={r:set() for r in (LIVING,KITCHEN,PORCH,SIDE,COURTYARD)}
  for a,b in edges:graph[a].add(b);graph[b].add(a)
  start=self.actors[actor];pending=[(start,[start])];seen=set()
  while pending:
   at,path=pending.pop(0)
   if at==destination:break
   if at in seen:continue
   seen.add(at);pending.extend((n,path+[n]) for n in sorted(graph[at]) if n not in seen)
  else:raise ValueError('No legal logical actor path')
  self.trace.append(dict(kind='logical-actor-arrival',actor=actor,path=path,cause=cause));self.actors[actor]=destination

 def context(self,room=COURTYARD,**changes):
  layout=self.p8.conditions
  values=dict(room=room,flags=frozenset(self.flags|self.p12.flags),npc_locations=tuple(self.actors.items()),rig=replace(self.rig,facing_inward=layout['sound_facing_inward']),contests=self.vc,gate=project_gate(self.p4),welcome_cleared=self.p12.welcome_cleared,queue_clear=self.queue_clear,board_room=self.board_room,footprint_clear=all(pos!=Position.ALCOVE for name,pos in self.p8.positions.items() if name!='completed_screen'),**{k:layout[k] for k in ('buffet_at_hatch','hatch_visible','display_concealed','lane_clear')})
  values.update(changes);return P13Context(**values)

 def start(self):
  self.cleanup();result=self.w.start(self.context(),pot_projection(self.p7,self.c7),self.p11.display_handoff)
  require(result.code=='deliveries_started',result.code)
  # P13 reservation is the authoritative dispatch ledger. Older projections are
  # suppressed; P07's source release occurs only after the hatch delivery.
  for obj in ('hotpot_pot','handcart','folded_display'):self.physical[obj]=('P13',self.physical[obj][1])
  self.physical['pledge_board']=('P13',LIVING)
  return result

 def serve(self):
  if not self.w.start_at:self.start()
  r=self.w.give_program(self.context(PORCH));require(r.code=='guest_route_requested',r.code)
  self.move('milo',COURTYARD,'P13_GUEST_ROUTE');self.queue_clear=True;self.w.confirm_seating(self.context())
  self.move('frankie',COURTYARD,'observed receiver arrival for hatch')
  r=self.w.deliver_pot(self.context(KITCHEN));require(r.code=='pot_delivered',r.code)
  c7=replace(self.c7,flags=self.c7.flags|self.p12.flags)
  request=P13Handoff('P13:OWN:hotpot_pot',self.w.pot_at)
  result=self.p7.handoff_to_p13(c7,request,host=self.h7);require(result.code=='pot_handed_off',result.code)
  self.c7=replace(c7,ownership=self.h7.ownership_context());self.physical['hotpot_pot']=('P13',COURTYARD)
  return self.w.pull_serve(self.context())

 def reveal(self):
  if not self.w.served_at:self.serve()
  self.move('rita',COURTYARD,'observed author arrival for consent');shown(self.w,self.context(),'rita_ready',self.trace)
  r=self.w.deliver_display(self.context(SIDE));require(r.code=='display_delivered',r.code)
  for actor in r.events[0].payload['helpers']:self.move(actor,COURTYARD,'P13_DISPLAY_DELIVERED')
  for obj in ('folded_display','handcart'):self.physical[obj]=('P13',COURTYARD)
  self.w.open_screen(self.context());self.move('bunny',COURTYARD,'observed arrival for Rita presentation')
  shown(self.w,self.context(),'reveal',self.trace)
  return self.w.pull_show(self.context())

 def board(self):
  if not self.w.show_at:self.reveal()
  self.move('frankie',LIVING,'observed board collection')
  r=self.w.deliver_board(self.context(LIVING));require(r.code=='board_delivered',r.code)
  self.move('frankie',COURTYARD,'P13_BOARD_DELIVERED');self.board_room=COURTYARD;self.physical['pledge_board']=('P13',COURTYARD)
  return r

 def contest(self,win=False,read_result=True):
  request=self.w.request_contest(self.context());require(request.code=='contest_requested',request.code)
  self.w.finish_contest_request(self.w.pending_contest_request_id,True)
  prepared('VC04',self.vc);play(self.vc,[win]*3,'VC04')
  if read_result:leave(self.vc)
  return request

 def finish(self,win=False):
  self.board();self.contest(win);shown(self.w,self.context(),'attention',self.trace)
  return self.w.pull_toast(self.context())
