"""NEW P14 helper shell, not a recovered complete historical test file.
The constants/c14 are retained partial-source bindings; workflow helpers below
are newly authored public-method fixture drivers. Real joins live separately.
"""
from dataclasses import replace
from cakood.p14_model import P14World,P14Context,PREREQUISITES as P14REQ,TERMS,PENCIL,PEOPLE,COURTYARD,LIVING
from cakood.p12_model import CurrentRig
from cakood.verbal_contest import VerbalContests
from test_verbal_contest import CATALOG,prepared,play,leave
RIG=CurrentRig(COURTYARD,True,'MIC',True)
ACTORS=tuple((p,COURTYARD) for p in PEOPLE[1:])
UNSIGNED={'object_id':TERMS,'location':'inventory','signed':False,'repair_date':None,'signature_owner':'P14','terms_record_id':'P09.READ.002'}
def contests(wins=(),losses=()):
 w=VerbalContests(CATALOG)
 for enc in (*wins,*losses):prepared(enc,w);play(w,[enc in wins]*3,enc);leave(w)
 return w
def c14(vc=None):return P14Context(COURTYARD,flags=P14REQ,inventory=frozenset((TERMS,PENCIL)),npc_locations=ACTORS,rig=RIG,contests=vc or contests(wins=('VC01','VC02','VC03','VC04')),repair_date='the agreed Saturday',vivian_tone='professional')
def read(w,c,source):
 r=w.begin_presentation(c,source)
 if r.presentation_id:w.acknowledge_presentation(c,r.presentation_id,record_id=w.SOURCES[source])
 return r
def approve14(w=None,c=None,order=PEOPLE):
 w=w or P14World();c=c or c14();w.start(c,UNSIGNED)
 for p in order:read(w,c,'approve:'+p);w.pin_card(c,p)
 return w,c
def finish14(w=None,c=None):
 w,c=approve14(w,c);read(w,c,'signature');w.pin_signature(c)
 c=replace(c,inventory=c.inventory-{TERMS});w.give_pencil(c);c=replace(c,inventory=c.inventory-{PENCIL})
 for s in ('date','readback','return_pencil'):read(w,c,s)
 w.complete_commitments(c);c=replace(c,inventory=c.inventory|{PENCIL})
 return w,c
def to_freeze(w=None,c=None,urls=()):
 w,c=finish14(w,c);w.start_finale(urls)
 for s in ('closing:'+w.vivian_tone,'meal','tag'):
  if s=='tag':c=replace(c,room=LIVING,npc_locations=tuple((p,LIVING) for p in PEOPLE[1:]))
  read(w,c,s);w.advance_finale()
 return w,c
