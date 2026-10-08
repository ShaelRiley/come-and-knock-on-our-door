"""NEW focused P14-REF-001 ordinary branch/owner-observation consistency tests."""
import copy,json,tempfile,threading,unittest
from pathlib import Path
from unittest.mock import patch
from cakood.verbal_contest import VerbalContests
from cakood.p14_model import P14World,CONTEST_IDS
from cakood import contest_evidence as evidence
from test_verbal_contest import prepared,play,leave
from test_late_campaign_models import c14,UNSIGNED,contests

def first(owner,enc='VC01'):
 return next(a.outcome.id for a in owner.attempts if a.encounter_id==enc and a.outcome.winner=='jack')

def fork_pair():
 seed=prepared('VC01').save_with_evidence();out=[]
 for gen,results in ((2,(True,False,False)),(3,(False,True,False))):
  w=VerbalContests.load_with_evidence(copy.deepcopy(seed),owner_generation=gen)
  for index,won in enumerate(results):
   play(w,[won]*3,'VC01')
   if gen==3 and index==0:
    if w.claim_effect(w.active.outcome_id) is None:raise RuntimeError('Expected actual logical effect')
   leave(w)
  for enc in CONTEST_IDS[1:]:prepared(enc,w);play(w,[True]*3,enc);leave(w)
  out.append(w)
 return out

class PairingTests(unittest.TestCase):
 def test_identical_aggregate_forks_have_different_owner_witnesses(self):
  a,b=fork_pair();self.assertEqual(a.save(),b.save());self.assertEqual((first(a),first(b)),('VC01:A1:KO','VC01:A2:KO'))
  pa,pb=a.save_with_evidence(),b.save_with_evidence()
  self.assertNotEqual(pa['owner'][evidence.WITNESS_KEY],pb['owner'][evidence.WITNESS_KEY])
  for owner_part,ledger_part in ((pa,pb),(pb,pa)):
   mixed=copy.deepcopy(owner_part);mixed['observations']=copy.deepcopy(ledger_part['observations'])
   with self.assertRaisesRegex(ValueError,'commit witness'):VerbalContests.load_with_evidence(mixed,owner_generation=4)
  self.assertEqual(a.save_with_evidence(),pa);self.assertEqual(b.save_with_evidence(),pb)

 def test_live_mispaired_ledger_cannot_be_resealed_or_commit(self):
  a,b=fork_pair();raw=a.snapshot();witness=a._reference_commit_witness
  a._observed_results=copy.deepcopy(b._observed_results)
  for op in (lambda:a.attempts,a.save_with_evidence,lambda:a.enter('VC01',0,admitted=True)):
   with self.assertRaisesRegex(ValueError,'commit witness'):op()
  self.assertEqual(a.snapshot(),raw);self.assertEqual(a._reference_commit_witness,witness)

 def test_same_save_restores_and_next_outcomes_evolve_from_saved_prefix(self):
  root=prepared('VC01');play(root,[True]*3,'VC01');leave(root);saved=root.save_with_evidence()
  a=VerbalContests.load_with_evidence(saved,owner_generation=2);b=VerbalContests.load_with_evidence(saved,owner_generation=3)
  self.assertEqual(a.save_with_evidence(),saved);self.assertEqual(b.save_with_evidence(),saved)
  self.assertIsNot(a._observed_results,b._observed_results)
  for w,result in ((a,True),(b,False)):play(w,[result]*3,'VC01');leave(w)
  wa=a.save_with_evidence()['owner'][evidence.WITNESS_KEY];wb=b.save_with_evidence()['owner'][evidence.WITNESS_KEY]
  self.assertEqual(wa['count'],2);self.assertEqual(wb['count'],2)
  self.assertNotEqual(wa['head'],wb['head']);self.assertEqual(first(a),'VC01:A1:KO');self.assertEqual(first(b),'VC01:A1:KO')
  self.assertEqual(root.save_with_evidence(),saved)

 def test_atomic_file_roundtrip_and_failed_replacement_preserve_previous_pair(self):
  a,b=fork_pair()
  with tempfile.TemporaryDirectory(prefix='p14 paired save ') as td:
   p=Path(td)/'owner and evidence.json';a.save_with_evidence_file(p);previous=p.read_bytes()
   actual=VerbalContests.load_with_evidence_file(p,owner_generation=4)
   self.assertEqual(actual.save_with_evidence(),a.save_with_evidence());self.assertEqual(first(actual),'VC01:A1:KO')
   with patch('dependencies.vc_owner.verbal_contest.os.replace',side_effect=OSError('injected before replacement')):
    with self.assertRaises(OSError):b.save_with_evidence_file(p)
   self.assertEqual(p.read_bytes(),previous)
   b.save_with_evidence_file(p);self.assertEqual(first(VerbalContests.load_with_evidence_file(p,owner_generation=5)),'VC01:A2:KO')

 def test_outcome_witness_does_not_advance_on_failed_persistence_or_repeat(self):
  w=prepared('VC01');w.enter('VC01',0,admitted=True);token=w.yield_contest(w.active.id)
  before=w.save_with_evidence()
  def fail(_):raise OSError('injected raw owner callback failure')
  w._persist=fail
  with self.assertRaises(OSError):w.commit_ko(token)
  self.assertEqual(w.save_with_evidence(),before)
  w._persist=None;w.commit_ko(token);one=w.save_with_evidence()
  self.assertEqual(one['owner'][evidence.WITNESS_KEY]['count'],1)
  with self.assertRaises(ValueError):w.commit_ko(token)
  self.assertEqual(w.save_with_evidence(),one)

 def test_pending_effect_restore_preserves_witness_and_old_callbacks_stay_stale(self):
  w=prepared('VC01');play(w,[True]*3,'VC01');old=w.active.outcome_id;oldtext=w.pending_text().receipt
  witness=w._reference_commit_witness.saved()
  self.assertIsNotNone(w.claim_effect(old));packet=w.save_with_evidence()
  self.assertEqual(packet['owner'][evidence.WITNESS_KEY],witness)
  r=VerbalContests.load_with_evidence(packet,owner_generation=2)
  with self.assertRaises(ValueError):r.claim_effect(old)
  with self.assertRaises(ValueError):r.acknowledge_text(oldtext)
  self.assertIsNone(r.claim_effect(r.active.outcome_id));leave(r)
  self.assertEqual(r.save_with_evidence()['owner'][evidence.WITNESS_KEY],witness);self.assertEqual(first(r),'VC01:A1:KO')

 def test_after_entry_later_losses_keep_original_wins_across_paired_restore(self):
  v=contests(wins=CONTEST_IDS);w=P14World();w.start(c14(v),UNSIGNED);firsts=dict(w.winning_attempts)
  for enc in CONTEST_IDS:play(v,[False]*3,enc);leave(v)
  v=VerbalContests.load_with_evidence(v.save_with_evidence(),owner_generation=2)
  w.validate_context(c14(v));self.assertEqual(w.winning_attempts,firsts);self.assertEqual(v.missing_wins,())
  w=P14World.load(w.save());w.validate_context(c14(v));self.assertEqual(w.winning_attempts,firsts)

 def test_raw_restore_detaches_evidence_but_preserves_all_earned_owner_progress(self):
  a,b=fork_pair();pa=a.save_with_evidence();pb=b.save_with_evidence();raw=b.save();flags=b.flags;knowledge=b.snapshot()['knowledge']
  a.restore(raw,owner_generation=4)
  self.assertEqual(a.flags,flags);self.assertEqual(a.snapshot()['knowledge'],knowledge)
  for op in (lambda:a.attempts,a.save_with_evidence):
   with self.assertRaises(ValueError):op()
  world=P14World();before=copy.deepcopy(world.__dict__)
  with self.assertRaises(ValueError):world.start(c14(a),UNSIGNED)
  self.assertEqual(world.__dict__,before)
  a.restore_with_evidence(pa,owner_generation=5);self.assertEqual(first(a),'VC01:A1:KO')
  before=a.save_with_evidence();bad=copy.deepcopy(pa);bad['observations']=pb['observations']
  with self.assertRaises(ValueError):a.restore_with_evidence(bad,owner_generation=6)
  self.assertEqual(a.save_with_evidence(),before);self.assertEqual(a.owner_generation,5)
  a.restore_with_evidence(pb,owner_generation=6);self.assertEqual(first(a),'VC01:A2:KO')

 def test_unwitnessed_old_envelope_is_explicitly_unsupported(self):
  w=contests(wins=CONTEST_IDS);packet=w.save_with_evidence();flags=w.flags
  old=copy.deepcopy(packet);old['schema']=1;del old['owner'][evidence.WITNESS_KEY]
  for bad in (old,{**packet,'owner':json.loads(w.save())}):
   with self.assertRaises(ValueError):VerbalContests.load_with_evidence(bad,owner_generation=2)
  self.assertEqual(w.flags,flags);self.assertEqual(w.save_with_evidence(),packet)

 def test_paired_snapshot_waits_until_owner_and_witness_share_commit_boundary(self):
  w=prepared('VC01');w.enter('VC01',0,admitted=True);token=w.yield_contest(w.active.id)
  committed=threading.Event();release=threading.Event();saving=threading.Event();done=threading.Event();errors=[];saved=[]
  original=evidence.capture
  def delayed(owner):
   committed.set()
   if not release.wait(5):raise RuntimeError('test barrier timed out')
   return original(owner)
  def commit():
   try:w.commit_ko(token)
   except BaseException as e:errors.append(e)
  def save():
   saving.set()
   try:saved.append(w.save_with_evidence())
   except BaseException as e:errors.append(e)
   finally:done.set()
  with patch.object(evidence,'capture',delayed):
   one=threading.Thread(target=commit);two=threading.Thread(target=save);one.start()
   try:
    self.assertTrue(committed.wait(5));two.start();self.assertTrue(saving.wait(5));self.assertFalse(done.wait(0.05))
   finally:release.set();one.join(5);two.join(5)
  self.assertFalse(one.is_alive());self.assertFalse(two.is_alive());self.assertEqual(errors,[]);self.assertEqual(len(saved),1)
  restored=VerbalContests.load_with_evidence(saved[0],owner_generation=2)
  self.assertEqual(len(restored.attempts),1);self.assertEqual(saved[0]['owner'][evidence.WITNESS_KEY]['count'],1)

if __name__=='__main__':unittest.main()
