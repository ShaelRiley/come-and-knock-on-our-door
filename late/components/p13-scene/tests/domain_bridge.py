"""New test-only adapter over accepted source and emitted P13. No native host."""
from pathlib import Path
import json,sys,importlib.util
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests'),str(H/'inputs/model'),str(H/'inputs/model/tests')]
from scene_vm import VM
from host import base
from cakood.p13_model import P13World
from cakood.p12_model import PEOPLE
from test_late_campaign_models import c13,actors,POT,DISPLAY
spec=importlib.util.spec_from_file_location('p13_accepted_codec',H/'inputs/domain/codec.py');codec=importlib.util.module_from_spec(spec);spec.loader.exec_module(codec)
A=json.loads((H/'inputs/domain/schema.json').read_text())
def domain(kind,world=None,c=None,epoch=1):
 if kind=='source':d=VM(H/'inputs/domain/src/module995.sc','P13State')
 else:
  b=H/'inputs/domain/accepted-emitted';v=base.HostVM(checkpoint=b/'verification-checkpoint',build=b,budget=100000000);d=v.objects['p13State']
 d.call('p13Init')
 if world is not None:d.p.update(codec.encode_world(world))
 if c is not None:project(d,c,epoch)
 return d

def project(d,c,epoch):
 rooms=dict(c.npc_locations);g=c.gate
 def oid(o):return A['objects'].get(o,32767)
 args=[A['rooms'][c.room],int(c.on_apron),*[int(x in c.flags) for x in ('INTRODUCTION_CLEAR','FOOD_READY','DISPLAY_STAGED','HELP_ACCEPTED','EVENING_STARTED')],*[int(getattr(c,x)) for x in ('welcome_cleared','queue_clear','buffet_at_hatch','hatch_visible','display_concealed','lane_clear','footprint_clear')],A['rooms'][c.board_room],A['rooms'][c.rig.location],int(c.rig.connected),int(c.rig.source=='MIC'),int(c.rig.facing_inward),int(c.contest_active),int(c.resolved('VC04')),*[A['rooms'][rooms[p]] if p in rooms else -1 for p in PEOPLE[1:]],int(g is not None),oid(g.peg_id) if g else 0,A['rooms'][g.peg_location] if g else 0,*[int(getattr(g,x)) if g else 0 for x in ('tested','peg_available','peg_engaged','gate_open','wedge_in_gate')],epoch]
 assert d.call('p13Context',*args)==1
 return d

def started():
 c=c13();w=P13World();assert w.start(c,POT,DISPLAY).code=='deliveries_started';return w,c

def seated():
 from dataclasses import replace
 from cakood.p12_model import PORCH
 w,c=started();w.give_program(actors(replace(c,room=PORCH),milo=PORCH));w.confirm_seating(c);assert w.seated_at;return w,c

def served():
 from dataclasses import replace
 from cakood.p12_model import KITCHEN
 w,c=seated();w.deliver_pot(actors(replace(c,room=KITCHEN),bunny=KITCHEN));w.pull_serve(c);assert w.served_at;return w,c

def display_ready():
 w,c=served();r=w.begin_presentation(c,'rita_ready');w.acknowledge_presentation(c,r.presentation_id,record_id='P13.DIALOGUE.004');assert w.rita_consented;return w,c

def reveal_ready():
 from dataclasses import replace
 from cakood.p12_model import SIDE
 w,c=display_ready();w.deliver_display(actors(replace(c,room=SIDE),felix=SIDE,vivian=SIDE));w.open_screen(c);assert w.screen_at;return w,c
