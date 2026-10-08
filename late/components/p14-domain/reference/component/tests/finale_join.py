"""NEW P13-to-P14 public-owner fixture, with explicit earlier initial inputs.

P03/P04/P07/P08/P09/P10/P11/P12/P13 public actions come from accepted Joined.
P05/P06/tray/entry are accepted initial reference facts, not fresh owner proof.
Contest exercises use actual owner methods with explicit finite admission; no
claim that the production rematch routing or notebook room guidance is fixed.
"""
from dataclasses import replace
import json
from current_join import Joined,require,shown
from test_verbal_contest import prepared,play,leave
from cakood.p14_model import *
from cakood.verbal_contest import VerbalContests

class FinaleJoined:
 def __init__(self,tone='professional'):
  self.j=Joined();self.j.finish(win=False);self.w=P14World();self.tone=tone
  self.inventory={TERMS,PENCIL};self.terms_owner='P09';self.pencil_owner='inventory';self.events=[]
  # These are explicitly accepted upstream inputs, not minted P14 task receipts.
  self.initial_flags=self.j.c8.flags|frozenset({'TRAY_SAFE','HOUSE_ENTERED'})
  for enc in ('VC01','VC02'):self.contest(enc,False)

 def contest(self,enc,win=True,read_result=True):
  before=dict(self.j.actors)
  prepared(enc,self.j.vc);play(self.j.vc,[win]*3,enc)
  if read_result:leave(self.j.vc)
  require(before==self.j.actors,'Contest test must not teleport actors')
  self.j.trace.append({'kind':'actual-contest-owner-exercise','encounter':enc,'observed_actor_rooms':before,'source_admission_only':True,'native_rematch_location_unresolved':enc!='VC04'})

 def context(self,**updates):
  flags=(self.initial_flags|self.j.flags|self.j.p12.flags|self.j.w.flags)
  flags=frozenset(x for x in flags if not x.startswith(('VC01_','VC02_','VC03_','VC04_')) and x!='ALL_VC_WON')|self.j.vc.flags
  values=dict(room=COURTYARD,flags=flags,inventory=frozenset(self.inventory),npc_locations=tuple(self.j.actors.items()),rig=self.j.rig,contests=self.j.vc,board_room=self.j.board_room,repair_date='the agreed Saturday',vivian_tone=self.tone)
  values.update(updates);return P14Context(**values)

 def start(self):return self.w.start(self.context(),self.j.p9.terms_card_handoff)
 def win_all(self):
  for enc in CONTEST_IDS:self.contest(enc,True)
 def show(self,source):return shown(self.w,self.context(),source,self.j.trace)
 def approvals(self):
  if not self.w.start_at:require(self.start().code=='commitments_started','P14 gate not ready')
  for p in PEOPLE:
   r=self.w.give_card(self.context(),p,p);require(r.presentation_id is not None,'Person absent')
   self.w.acknowledge_presentation(self.context(),r.presentation_id,record_id=self.w.SOURCES['approve:'+p])
   self.w.pin_card(self.context(),p)

 def event(self,r):
  for e in r.events:
   self.events.append((e.id,e.payload))
   if e.id=='P14_TERMS_SIGNED':
    require(self.terms_owner=='P09' and TERMS in self.inventory,'Original terms were not in pocket')
    self.inventory.remove(TERMS);self.terms_owner='P14'
   elif e.id=='P14_PENCIL_HANDOFF':
    require(self.pencil_owner=='inventory' and PENCIL in self.inventory,'Original pencil unavailable')
    self.inventory.remove(PENCIL);self.pencil_owner='frankie'
   elif e.id=='P14_GAME_COMPLETE':
    require(self.pencil_owner=='frankie' and PENCIL not in self.inventory,'Pencil return not unique')
    self.inventory.add(PENCIL);self.pencil_owner='inventory'
  return r

 def finish(self):
  self.win_all();self.approvals();self.show('signature');self.event(self.w.pin_signature(self.context()))
  self.event(self.w.give_pencil(self.context()))
  for source in ('date','readback','return_pencil'):self.show(source)
  self.event(self.w.complete_commitments(self.context()));self.w.validate_context(self.context())
  return self.w

 def restore_contests(self):
  packet=self.j.vc.save_with_evidence()
  self.j.vc=VerbalContests.load_with_evidence(json.loads(json.dumps(packet)),owner_generation=self.j.vc.owner_generation+1)
  return packet
