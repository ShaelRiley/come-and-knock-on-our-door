"""Current-canon SCI regressions, all using public gameplay histories."""
import copy,itertools,json
from pathlib import Path
from test_domain import (Harness,ByteVM,source_vm,C,ENGAGED,GATE,M,CO,RECORD_UNITS,P11World,replace,unittest,SIDE_PASSAGE,PORCH,COURTYARD,CONSERVATORY,HERE,encode_world,decode_words,encode_save)
from cakood.p04_model import project_gate
from dependencies.p04_numeric_model import P04,Obj,Bunting,Code
MEASUREMENTS=[]

class PairedVM:
 def __init__(self):
  self.source=source_vm.VM();self.emitted=ByteVM();self.p=self.source.p;self.calls=0
 def call(self,name,*args):
  self.emitted.p.update(self.p)
  left=self.source.call(name,*args);right=self.emitted.call(name,*args);self.calls+=1
  if left!=right or self.p!=self.emitted.p:raise AssertionError(('source/emitted state',name,args,left,right))
  for k,v in self.source.arrays.items():
   if v!=list(self.emitted.machine.domain.arrays[k]):raise AssertionError(('source/emitted arrays',name,k))
  return left
 def persistent(self):return self.source.persistent()

def repaired_gate():
 p=P04();p.context(3,0,1,1);p.topic(Obj.FELIX,1);p.open_gate();p.place_wedge();p.context(3,0,1,0)
 p.move_bunting(Bunting.HELD);p.move_bunting(Bunting.HOOK);p.recover_wedge();p.context(3,0,1,1);p.close_gate(1);p.open_gate()
 if not p.validate() or not p.tested:raise RuntimeError('Actual P04 preparation failed')
 return p

class AdaptationTests(unittest.TestCase):
 VM=PairedVM
 def h(self):return Harness(self.VM)
 def test_external_unacknowledged_peg_history_blocks_without_credit(self):
  h=self.h();h.action('lift','p11Lift');h.action('release_catch','p11ReleaseCatch')
  before=h.v.persistent();r=h.action('pull_handle','p11PullHandle',c=ENGAGED)
  self.assertEqual(r.code,'peg_history_required');self.assertEqual(h.v.persistent(),before)
  self.assertEqual((r.line_ids,r.speech_unit_ids,r.events),((),(),()))
  h.action('set_back','p11SetBack',c=ENGAGED);c=h.rescue(ENGAGED);h.queries()
  self.assertEqual(h.w.rescue_credit_variant,'pre_engaged');self.assertEqual(h.w.peg_ack_at,0)
 def test_bunny_must_be_present_during_sincere(self):
  h=self.h();c=h.rescue(ENGAGED);absent=replace(c,bunny_room=CONSERVATORY);before=h.v.persistent()
  self.assertEqual(h.begin('sincere',absent).code,'bunny_at_porch_required');self.assertEqual(h.v.persistent(),before)
  h.begin('sincere',c);h.ack('sincere',units=RECORD_UNITS['P11.DIALOGUE.002'][:5],c=c);before=h.v.persistent()
  self.assertEqual(h.ack('sincere',units=RECORD_UNITS['P11.DIALOGUE.002'][5:],c=absent).code,'bunny_at_porch_required')
  self.assertEqual(h.v.persistent(),before);h.ack('sincere',record='P11.DIALOGUE.002',c=c)
  self.assertTrue(h.w.contest_eligible)
 def test_felix_listener_blocks_final_jackie_only_reply(self):
  h=self.h();c=h.rescue();h.begin('sincere',c);h.ack('sincere',units=RECORD_UNITS['P11.DIALOGUE.002'][:5],c=c)
  absent=replace(c,felix_room=CONSERVATORY);before=h.v.persistent()
  self.assertEqual(h.resume('sincere',absent).code,'felix_required')
  self.assertEqual(h.ack('sincere',units=RECORD_UNITS['P11.DIALOGUE.002'][5:],c=absent).code,'felix_required')
  self.assertEqual(h.v.persistent(),before);self.assertFalse(h.w.contest_eligible)
  self.assertEqual(absent.felix_room,CONSERVATORY);h.restore();h.resume('sincere',c)
  h.ack('sincere',units=RECORD_UNITS['P11.DIALOGUE.002'][5:],c=c);self.assertTrue(h.w.contest_eligible)
 def test_actual_p04_owner_both_helper_orders_and_credit_variants(self):
  routes=0;instructions=0
  for advanced,order in itertools.product((False,True),itertools.permutations(('peg','catch'))):
   owner=repaired_gate()
   if advanced:owner.set_peg(1)
   original=owner.save();h=self.h();c=replace(C,gate=project_gate(owner));h.action('lift','p11Lift',c=c)
   for action in order:
    if action=='peg':
     h.action('request_peg','p11RequestPeg',c=c)
     if not advanced:
      self.assertEqual(owner.save(),original);owner.set_peg(1);c=replace(c,gate=project_gate(owner));h.ack_peg(c)
     else:self.assertEqual(owner.save(),original)
    else:h.action('release_catch','p11ReleaseCatch',c=c)
   committed=owner.save();h.action('pull_handle','p11PullHandle',c=c);h.restore();h.action('stage_display','p11StageDisplay',c=c)
   h.show('sincere',c);h.action('request_contest','p11RequestContest',c=c);h.queries()
   self.assertEqual(owner.save(),committed);self.assertEqual(h.w.rescue_credit_variant,'pre_engaged' if advanced else 'ordinary')
   self.assertEqual(h.v.call('p11RescueCreditVariant'),2 if advanced else 1)
   self.assertEqual(h.w.flags,{'DISPLAY_STAGED','HELP_ACCEPTED'});self.assertEqual(h.w.inventory,())
   self.assertEqual(h.w.reserved_external_objects,{'folded_display','handcart'})
   self.assertFalse(h.w.display_handoff['panel_revealed']);self.assertFalse(h.w.display_handoff['rita_reveal_consent'])
   routes+=1;instructions+=h.v.emitted.machine.steps
  MEASUREMENTS.append(dict(gate='actual_numeric_P04_owner',routes=routes,emitted_instructions=instructions,owner_only_mutation=True))
 def test_every_incomplete_sincere_prefix_actor_departure_restore_return(self):
  scenarios=0;instructions=0
  for advanced,posture,n in itertools.product((False,True),('cart','folded','staged'),range(6)):
   h=self.h();c=ENGAGED if advanced else C
   h.action('lift','p11Lift',c=c)
   if posture!='cart':
    if not advanced:
     h.action('request_peg','p11RequestPeg',c=c);c=ENGAGED;h.ack_peg(c)
    h.action('release_catch','p11ReleaseCatch',c=c);h.action('pull_handle','p11PullHandle',c=c)
    if posture=='staged':h.action('stage_display','p11StageDisplay',c=c)
   h.begin('sincere',c)
   if n:h.ack('sincere',units=RECORD_UNITS['P11.DIALOGUE.002'][:n],c=c)
   if posture=='cart':h.action('set_back','p11SetBack',c=c)
   for restored in (False,True):
    if restored:h.restore()
    for field,code in (('felix_room','felix_required'),('bunny_room','bunny_at_porch_required')):
     away=replace(c,**{field:CONSERVATORY});before=h.v.persistent()
     self.assertEqual(h.resume('sincere',away).code,code)
     self.assertEqual(h.ack('sincere',record='P11.DIALOGUE.002',c=away).code,code)
     self.assertEqual(h.v.persistent(),before);self.assertFalse(h.w.sincere_complete);self.assertFalse(h.w.contest_eligible)
    scenarios+=1
   h.resume('sincere',c);h.ack('sincere',record='P11.DIALOGUE.002',c=c);h.queries()
   self.assertTrue(h.w.sincere_complete);self.assertEqual(h.w.contest_eligible,posture=='staged')
   instructions+=h.v.emitted.machine.steps
  MEASUREMENTS.append(dict(gate='all_incomplete_sincere_prefixes',scenarios=scenarios,actor_barriers=2*scenarios,emitted_instructions=instructions))
 def test_pending_peg_receipt_reconciles_and_ordinary_has_priority(self):
  for advanced in (False,True):
   h=self.h();c=ENGAGED if advanced else C;h.action('lift','p11Lift',c=c)
   h.action('request_peg','p11RequestPeg',c=C);h.action('release_catch','p11ReleaseCatch',c=ENGAGED)
   if not advanced:self.assertEqual(h.action('pull_handle','p11PullHandle',c=ENGAGED).code,'peg_history_required')
   h.ack_peg(ENGAGED);h.action('pull_handle','p11PullHandle',c=ENGAGED);h.action('stage_display','p11StageDisplay',c=ENGAGED)
   self.assertEqual(h.v.call('p11RescueCreditVariant'),1);h.show('sincere',ENGAGED);h.action('request_contest','p11RequestContest',c=ENGAGED)
   self.assertEqual(h.w.rescue_credit_variant,'ordinary');self.assertEqual(bool(h.w.advance_peg_at),advanced)
 def test_loss_rematch_and_win_do_not_change_rescue_or_supply_consent(self):
  h=self.h();c=h.rescue();h.show('sincere',c);h.action('request_contest','p11RequestContest',c=c);h.ack_contest(c)
  physical=(h.w.phase,h.w.fold_at,h.w.stage_at,h.w.peg_ack_at,h.w.advance_peg_at)
  loss=replace(c,flags=c.flags|{'VC03_RESOLVED'});h.action('request_contest','p11RequestContest',c=loss);h.ack_contest(loss,True)
  self.assertTrue(h.w.ready);self.assertNotIn('VC03_WON',loss.flags)
  win=replace(loss,flags=loss.flags|{'VC03_WON'});h.action('request_contest','p11RequestContest',c=win);h.ack_contest(win)
  self.assertEqual((h.w.phase,h.w.fold_at,h.w.stage_at,h.w.peg_ack_at,h.w.advance_peg_at),physical)
  self.assertEqual(h.w.flags,{'DISPLAY_STAGED','HELP_ACCEPTED'});self.assertFalse(h.w.display_handoff['rita_reveal_consent'])
 def test_context_rejects_peg_wedge_and_closed_wedge(self):
  for engaged,opened in ((1,1),(0,0)):
   h=self.h();h.project(C);before=h.v.persistent()
   args=[3,0,1,1,1,1,3,0,4,6,3,3,0,0,0,1,1,engaged,opened,1,h.epoch+1]
   self.assertEqual(h.v.call('p11Context',*args),0);self.assertEqual(h.v.persistent(),before)
   self.assertEqual(h.v.p['p11ContextValid'],0)

 def test_actual_p04_exclusive_support_and_wedge_only_safe_setback(self):
  owner=repaired_gate();owner.set_peg(1);before=owner.save()
  self.assertEqual(owner.place_wedge(),Code.ALREADY_HELD_BY_PEG);self.assertEqual(owner.save(),before)
  owner.set_peg(0);owner.place_wedge();owner.context(3,0,1,0);before=owner.save()
  self.assertTrue(owner.validate());self.assertEqual(owner.set_peg(1),Code.RECOVER_WEDGE_REQUIRED)
  self.assertEqual(owner.save(),before);self.assertTrue(project_gate(owner).wedge_in_gate)
  c=replace(C,gate=project_gate(owner));h=self.h();h.action('lift','p11Lift',c=c);h.action('release_catch','p11ReleaseCatch',c=c)
  self.assertEqual(h.action('pull_handle','p11PullHandle',c=c).code,'peg_required')
  away=replace(c,room=CONSERVATORY,on_apron=True,felix_room=CONSERVATORY,contest_active=True,flags=frozenset())
  h.action('set_back','p11SetBack',c=away);self.assertFalse(h.w.supported);self.assertEqual(owner.save(),before)
  owner.recover_wedge();owner.context(3,0,1,1);owner.set_peg(1);after=owner.save()
  c=replace(C,gate=project_gate(owner));c=h.rescue(c);self.assertEqual(h.w.rescue_credit_variant,'pre_engaged')
  self.assertEqual(owner.save(),after);self.assertTrue(owner.validate());h.queries()

if __name__=='__main__':unittest.main()
