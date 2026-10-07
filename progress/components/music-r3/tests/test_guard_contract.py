from support import *
import gate_support as g
class GuardContractProof(unittest.TestCase):
 def fixture(self):
  d=json.loads((H/'inputs/revision1/guard-probes-r1.json').read_text());d['schema']=2
  for row in d['probes']:
   if row['name']=='zero-execution':row['outcome']={k:0 for k in('run','skipped','expected_failures','unexpected_successes','failures','errors')}
  return d
 def expected(self):return json.loads((H/'REQUIRED-GUARDS.json').read_text())
 def test_01_complete_fixed_primary_records_are_structurally_admitted(self):self.assertTrue(g.validate_probe_report(self.fixture(),self.expected()))
 def test_02_empty_list_with_unchanged_count_is_rejected(self):
  d=self.fixture();d['probes']=[]
  with self.assertRaisesRegex(RuntimeError,'identities'):g.validate_probe_report(d,self.expected())
 def test_03_duplicate_missing_and_substituted_cases_are_rejected(self):
  for kind in('duplicate','missing','substituted'):
   d=self.fixture()
   if kind=='duplicate':d['probes'][-1]=d['probes'][0].copy()
   elif kind=='missing':d['probes'].pop()
   else:d['probes'][-1]['name']='invented-case'
   with self.assertRaisesRegex(RuntimeError,'identities'):g.validate_probe_report(d,self.expected())
 def test_04_success_missing_result_or_zero_exit_cannot_count(self):
  for field,value in(('status','PASS'),('error',''),('exit',0),('terminal','')):
   d=self.fixture();d['probes'][0][field]=value
   with self.assertRaises(RuntimeError):g.validate_probe_report(d,self.expected())
 def test_05_named_outcome_requires_exact_nonzero_rejection(self):
  d=self.fixture();row=next(r for r in d['probes']if r['name']=='real-outcome-skip');row['outcome']['skipped']=0
  with self.assertRaisesRegex(RuntimeError,'inconsistent'):g.validate_probe_report(d,self.expected())
 def test_06_count_cannot_replace_membership(self):
  d=self.fixture();d['count']+=1
  with self.assertRaisesRegex(RuntimeError,'count inconsistent'):g.validate_probe_report(d,self.expected())
 def test_07_old_seal_counterexamples_are_preserved(self):
  old=json.loads((H/'inputs/revision1/reproduced/empty-probe-package.json').read_text());self.assertTrue(old['incorrectly_accepted']);self.assertEqual(old['exit_code'],0)
  rows=json.loads((H/'inputs/revision1/reproduced/host-chooser-probes.json').read_text())['cases'];c=next(x for x in rows if x['method']=='generation-exhaustion-next-gate');self.assertEqual((c['request_return'],c['owner'],c['unavailable']),(0,148,9));self.assertGreater(c['retirements_after'],c['retirements_before'])
  rows=json.loads((H/'inputs/revision1/reproduced/lifecycle-probes.json').read_text())['cases'];c=next(x for x in rows if x['name']=='main-pending-valid-transition-status');self.assertEqual((c['unavailable'],c['broker_failure'],c['retry']),(1,0,0))
