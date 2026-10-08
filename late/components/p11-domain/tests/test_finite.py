"""Finite transport boundaries and exact canonical/native identity gates."""
from test_domain import (Harness,C,ENGAGED,M,CO,RECORD_UNITS,P11World,replace,unittest,HERE,CONSERVATORY,SIDE_PASSAGE,json,encode_save,decode_words,copy)
from test_adaptations import PairedVM
MEASUREMENTS=[]
class FiniteTests(unittest.TestCase):
 def test_limb_carry_and_safety_serial_reserve(self):
  routes=0;instructions=0
  for revision in (32766,32767,32768,65535,65536,M['max_serial']-2,M['max_serial']-1,M['max_serial']):
   h=Harness(PairedVM,P11World(revision=revision));h.project(C)
   self.assertEqual(h.v.call('p11Present',0),1);before=h.v.persistent()
   if revision<=M['max_serial']-2:
    h.action('lift','p11Lift');self.assertEqual(h.w.revision,revision+1)
    h.action('set_back','p11SetBack',c=replace(C,room=CONSERVATORY,on_apron=True,felix_room=CONSERVATORY,contest_active=True,flags=frozenset()))
    self.assertEqual(h.w.revision,revision+2)
   else:
    h.v.call('p11Lift');self.assertEqual(CO[h.v.p['p11Code']],'serial_exhausted');self.assertEqual(h.v.persistent(),before)
    self.assertEqual(h.v.p['p11EventCount'],0)
    if revision==M['max_serial']-1:h.action('hint','p11Hint',1)
   h.restore();self.assertEqual(h.v.call('p11Validate'),1);routes+=1;instructions+=h.v.emitted.machine.steps
  MEASUREMENTS.append(dict(gate='serial_boundaries',cases=routes,emitted_instructions=instructions))
 def test_receipt_carry_last_commit_and_duplicate_at_max(self):
  for revision in (32764,32765,32766,M['max_serial']-5):
   h=Harness(PairedVM,P11World(revision=revision));h.action('lift','p11Lift',c=ENGAGED)
   h.action('release_catch','p11ReleaseCatch',c=ENGAGED);h.action('pull_handle','p11PullHandle',c=ENGAGED)
   h.begin('sincere',ENGAGED);h.ack('sincere',units=RECORD_UNITS['P11.DIALOGUE.002'][:1],c=ENGAGED)
   h.restore();h.resume('sincere',ENGAGED)
   if h.w.revision<M['max_serial']:h.ack('sincere',record='P11.DIALOGUE.002',c=ENGAGED)
   else:
    before=h.v.persistent();start=h.w.presentations['sincere'].serial
    h.v.call('p11Acknowledge',M['sources']['sincere'],*divmod(start,32768),h.epoch,M['line_ids']['P11.DIALOGUE.002'],0,0)
    self.assertEqual(CO[h.v.p['p11Code']],'serial_exhausted');self.assertEqual(h.v.persistent(),before)
    h.ack('sincere',units=RECORD_UNITS['P11.DIALOGUE.002'][:1],c=ENGAGED)
   h.queries()
 def test_epoch_exhaustion_invalidates_then_host_retires_callbacks(self):
  h=Harness(PairedVM);h.epoch=32765;h.action('lift','p11Lift');h.begin('sincere');old=tuple((M['sources']['sincere'],*divmod(h.w.presentations['sincere'].serial,32768),h.epoch,M['line_ids']['P11.DIALOGUE.002'],0,0))
  h.project(replace(C,rita_room=SIDE_PASSAGE));self.assertEqual(h.v.p['p11Epoch'],32767)
  before=h.v.persistent();args=[3,0,1,1,1,1,3,0,4,6,3,3,0,0,0,1,1,0,1,0,32767]
  self.assertEqual(h.v.call('p11Context',*args),0);self.assertEqual(h.v.persistent(),before)
  self.assertEqual(h.v.p['p11ContextValid'],0);self.assertEqual(h.v.source.arrays['p11Lease'],[0]*9)
  with self.assertRaises(ValueError):h.v.call('p11Context',*args[:-1],32768)
  h.restore();self.assertEqual(h.v.p['p11Epoch'],0)
  # Host retirement is an explicit obligation, not a claimed native facility.
  # Fresh low epoch is tested with old high callback; epoch reuse is unsupported
  # unless the host has retired the old callback objects.
  h.epoch=0;h.context=None;h.resume('sincere');before=h.v.persistent()
  h.v.call('p11Acknowledge',*old);self.assertEqual(CO[h.v.p['p11Code']],'stale_presentation');self.assertEqual(h.v.persistent(),before)
  h.ack('sincere',record='P11.DIALOGUE.002');h.action('set_back','p11SetBack');h.queries()
 def test_current_native_ids_and_all_bound_words_match_authority(self):
  self.assertEqual(M['own_objects'],{'display_wing':415,'wing_catch':416,'display_handle':417,'staging_pocket':418})
  self.assertEqual([M['objects'][k] for k in ('completed_screen','courtyard_plan','screen_token','clip_marks')],[81,83,80,84])
  self.assertEqual((HERE/'codec.py').read_bytes(),(HERE/'historical/stock-sci/p11-domain-adapter/codec.py').read_bytes())
  self.assertEqual(len(M['persisted_properties']),87);self.assertEqual(len(M['serials']),42)
  self.assertEqual((len(M['line_ids']),len(M['speech_unit_ids'])),(26,36))
  root=HERE/'reference/component';fixture=json.loads((root/'tests/fixtures/p11/canonical-bindings.json').read_text())
  catalog=json.loads((root/'authority/full-line-catalog.json').read_text());speech=json.loads((root/'authority/speech-units.json').read_text())
  expected={r['id']:r for r in catalog['records'] if r['id'] in M['line_ids']}
  self.assertEqual(fixture['records'],expected)
  self.assertEqual(M['speech_metadata'],[r for r in speech['units'] if r['record_id'] in M['line_ids']])
  for name in ('VC03.WIN','VC03.LOSS'):
   self.assertEqual(fixture['vc03_records'][name],next(r for r in catalog['records'] if r['id']==name))
   self.assertEqual(fixture['vc03_records'][name]['variant_binding']['priority'],['ordinary','pre_engaged'])
  self.assertEqual(M['rescue_credit_variants'],{'ordinary':1,'pre_engaged':2})
 def test_credit_getter_does_not_create_history_or_mutate_state(self):
  for ctx in (C,ENGAGED):
   h=Harness(PairedVM);before=h.v.persistent();self.assertEqual(h.v.call('p11RescueCreditVariant'),0);self.assertEqual(h.v.persistent(),before)
   h.action('lift','p11Lift',c=ctx);self.assertEqual(h.v.call('p11RescueCreditVariant'),0)
   c=h.rescue(ctx);before=h.v.persistent();self.assertEqual(h.v.call('p11RescueCreditVariant'),2 if ctx==ENGAGED else 1)
   self.assertEqual(h.v.persistent(),before)
if __name__=='__main__':unittest.main()
