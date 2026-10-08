"""R2 mixed-branch witness admission joined to real finite SCI, not native I/O."""
from pathlib import Path
import sys,copy,json,tempfile,os,hashlib
H=Path(__file__).resolve().parents[1];C=H/'reference/component';sys.dont_write_bytecode=True
sys.path[:0]=[str(H/'tests'),str(H),str(C),str(C/'tests')]
if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
from verify_source import verify
verify()
from test_p14_pairing import fork_pair,first
from test_domain import Harness,PairedVM,c14,CONTEST_IDS,M
from cakood.verbal_contest import VerbalContests
from codec import project_context
from paired import MEASUREMENTS,restore_words
from cakood import contest_evidence as e
a,b=fork_pair()
if a.save()!=b.save():raise AssertionError('Original exact mixed branch reproduction lost')
rows=[]
for owner in (a,b):
 c=c14(owner);h=Harness(PairedVM);h.start(c);h.queries()
 expected={enc:next(x.outcome.id for x in owner.attempts if x.encounter_id==enc and x.outcome.winner=='jack') for enc in CONTEST_IDS}
 if h.w.winning_attempts!=expected:raise AssertionError('First genuine win changed')
 with tempfile.TemporaryDirectory(prefix='p14 finite ordinary pair ') as td:
  p=Path(td)/'ordinary owner and words.json';packet={'owner':owner.save_with_evidence(),'p14_words':list(h.v.persistent().values())}
  with p.open('w') as f:json.dump(packet,f);f.flush();os.fsync(f.fileno())
  back=json.loads(p.read_text())
  if back!=packet:raise AssertionError('Readback differs')
  restored=VerbalContests.load_with_evidence(back['owner'],owner_generation=9);v=restore_words(back['p14_words']);project_context(v.call,c14(restored),900)
  if v.persistent()!=h.v.persistent():raise AssertionError('Restore changed finite words')
 rows.append(dict(first_wins=expected,owner_witness=owner.save_with_evidence()['owner'][e.WITNESS_KEY],raw_sha256=hashlib.sha256(owner.save()).hexdigest()))
for left,right in ((a,b),(b,a)):
 mixed=left.save_with_evidence();mixed['observations']=copy.deepcopy(right.save_with_evidence()['observations'])
 try:VerbalContests.load_with_evidence(mixed,owner_generation=10)
 except ValueError as exc:
  if 'commit witness' not in str(exc):raise
 else:raise AssertionError('Mixed branch admitted')
raw=VerbalContests.load(a.save(),owner_generation=12);v=PairedVM();before=v.persistent()
try:project_context(v.call,c14(raw),100)
except ValueError as exc:
 if 'paired observed' not in str(exc):raise
else:raise AssertionError('Unsupported raw history admitted')
if v.persistent()!=before or raw.missing_wins:raise AssertionError('Raw import fabricated progress or lost wins')
report=dict(status='PASS',mixed_pairs_rejected=2,genuine_paired_file_restores=2,rows=rows,paired=MEASUREMENTS,native_atomic_storage=False,reference_witness_boundary=True)
(H/'evidence/pairing-emitted.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS_PAIRED_FINITE_ADMISSION',MEASUREMENTS)
