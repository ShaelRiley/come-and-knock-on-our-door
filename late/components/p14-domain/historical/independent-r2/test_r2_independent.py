"""Independent R2 paired-owner boundary checks; ordinary consistency only."""
from pathlib import Path
import argparse,copy,json,sys,tempfile,threading,unittest
from unittest.mock import patch

p=argparse.ArgumentParser();p.add_argument('--component',type=Path,required=True);p.add_argument('--results',type=Path,required=True);args=p.parse_args()
C=args.component.resolve();sys.path[:0]=[str(C),str(C/'tests')]
from cakood.verbal_contest import VerbalContests
from cakood import contest_evidence as ev
from cakood.p14_model import P14World,CONTEST_IDS
from test_verbal_contest import prepared,play,leave
from test_late_campaign_models import c14,UNSIGNED,contests

def state(owner):
    return copy.deepcopy((owner.snapshot(),owner.owner_generation,owner._reference_commit_witness,owner._observed_results,owner._suppressed))

class R2Independent(unittest.TestCase):
    def test_invalid_raw_restore_keeps_witness_generation_state_and_effects(self):
        owner=contests(wins=CONTEST_IDS);before=state(owner)
        with self.assertRaises(ValueError):owner.restore(b'not a save',owner_generation=2)
        self.assertEqual(state(owner),before)
        valid=owner.save();before=state(owner)
        with self.assertRaises(ValueError):owner.restore(valid,owner_generation=1)
        self.assertEqual(state(owner),before)

    def test_invalid_paired_restore_generation_is_atomic_for_existing_owner(self):
        owner=contests(wins=CONTEST_IDS);packet=owner.save_with_evidence();before=state(owner)
        for generation in (True,0,1):
            with self.subTest(generation=generation),self.assertRaises(ValueError):
                owner.restore_with_evidence(packet,owner_generation=generation)
            self.assertEqual(state(owner),before)
        malformed=copy.deepcopy(packet);malformed['owner'][ev.WITNESS_KEY]['head']='0'*64
        with self.assertRaises(ValueError):owner.restore_with_evidence(malformed,owner_generation=2)
        self.assertEqual(state(owner),before)

    def test_raw_restore_detaches_all_reference_support_even_after_new_outcome(self):
        owner=contests(wins=CONTEST_IDS);raw=owner.save();flags=owner.flags;knowledge=owner.snapshot()['knowledge']
        owner.restore(raw,owner_generation=2)
        self.assertIsNone(owner._reference_commit_witness)
        play(owner,[False]*3,'VC01');leave(owner)
        self.assertIsNone(owner._reference_commit_witness)
        self.assertEqual(owner._observed_results,[])
        self.assertEqual(owner.flags,flags);self.assertEqual(owner.snapshot()['knowledge'],knowledge)
        world=P14World();before=copy.deepcopy(world.__dict__)
        for _ in range(2):
            with self.assertRaises(ValueError):world.start(c14(owner),UNSIGNED)
            self.assertEqual(world.__dict__,before)

    def test_paired_load_restore_are_by_value_and_later_loss_keeps_first_win(self):
        owner=contests(wins=CONTEST_IDS);packet=owner.save_with_evidence();original=copy.deepcopy(packet)
        restored=VerbalContests.load_with_evidence(packet,owner_generation=2)
        target=VerbalContests();target.restore_with_evidence(packet,owner_generation=2)
        packet['observations'].clear();packet['owner'][ev.WITNESS_KEY]['head']='0'*64
        self.assertEqual(restored.save_with_evidence(),original);self.assertEqual(target.save_with_evidence(),original)
        world=P14World();world.start(c14(restored),UNSIGNED);first=dict(world.winning_attempts)
        oldw=restored._reference_commit_witness
        play(restored,[False]*3,'VC01');leave(restored)
        self.assertEqual(restored._reference_commit_witness.count,oldw.count+1)
        self.assertNotEqual(restored._reference_commit_witness.head,oldw.head)
        world.validate_context(c14(restored));self.assertEqual(world.winning_attempts,first)
        self.assertEqual(target.save_with_evidence(),original)

    def test_result_and_lesson_transactions_do_not_advance_witness(self):
        owner=prepared('VC01');initial=owner._reference_commit_witness
        owner.present_lesson('VC01','IR01',half='setup');owner.cancel_lesson()
        self.assertEqual(owner._reference_commit_witness,initial)
        play(owner,[True]*3,'VC01');witness=owner._reference_commit_witness
        self.assertEqual(witness.count,initial.count+1)
        owner.claim_effect(owner.active.outcome_id);leave(owner)
        owner.present_lesson('VC01','IR01',half='reply');owner.cancel_lesson()
        self.assertEqual(owner._reference_commit_witness,witness)
        self.assertEqual(owner.save_with_evidence()['owner'][ev.WITNESS_KEY],witness.saved())

    def test_pre_replace_fsync_failure_keeps_previous_paired_file(self):
        owner=contests(wins=CONTEST_IDS)
        with tempfile.TemporaryDirectory(prefix='independent p14 paired ') as td:
            path=Path(td)/'save.json';owner.save_with_evidence_file(path);before=path.read_bytes()
            play(owner,[False]*3,'VC01');leave(owner)
            with patch('dependencies.vc_owner.verbal_contest.os.fsync',side_effect=OSError('ordinary file sync failure')):
                with self.assertRaises(OSError):owner.save_with_evidence_file(path)
            self.assertEqual(path.read_bytes(),before)
            self.assertEqual(list(Path(td).iterdir()),[path])
            loaded=VerbalContests.load_with_evidence_file(path,owner_generation=2)
            self.assertEqual(loaded._reference_commit_witness.count,4)
            owner.save_with_evidence_file(path)
            self.assertEqual(VerbalContests.load_with_evidence_file(path,owner_generation=3)._reference_commit_witness.count,5)

    def test_save_waits_through_owner_persistence_then_witness_commit(self):
        owner=prepared('VC01');owner.enter('VC01',0,admitted=True);token=owner.yield_contest(owner.active.id)
        writing=threading.Event();release=threading.Event();save_requested=threading.Event();saved=threading.Event();packets=[];errors=[]
        def persist(_):
            writing.set()
            if not release.wait(5):raise RuntimeError('test release timeout')
        owner._persist=persist
        def commit():
            try:owner.commit_ko(token)
            except BaseException as exc:errors.append(str(exc))
        def save():
            save_requested.set()
            try:packets.append(owner.save_with_evidence())
            except BaseException as exc:errors.append(str(exc))
            finally:saved.set()
        one=threading.Thread(target=commit);two=threading.Thread(target=save);one.start()
        try:
            self.assertTrue(writing.wait(5));two.start();self.assertTrue(save_requested.wait(5));self.assertFalse(saved.wait(.05))
        finally:release.set();one.join(5);two.join(5)
        self.assertFalse(one.is_alive());self.assertFalse(two.is_alive());self.assertEqual(errors,[])
        self.assertEqual(len(packets),1)
        loaded=VerbalContests.load_with_evidence(packets[0],owner_generation=2)
        self.assertEqual(len(loaded.attempts),1);self.assertEqual(loaded._reference_commit_witness.count,1)

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(R2Independent))
    args.results.write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'optimized':bool(sys.flags.optimize),'passed':result.wasSuccessful()},indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
