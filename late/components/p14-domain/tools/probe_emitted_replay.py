"""NEW direct emitted heap/arena replay contract; no actual native session claim."""
from pathlib import Path
import sys,json,copy,time
H=Path(__file__).resolve().parents[1];C=H/'reference/component';sys.dont_write_bytecode=True
sys.path[:0]=[str(H/'tests'),str(H),str(C),str(C/'tests')]
if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
from verify_source import verify
verify()
from native_replay_binding import ByteVM
from test_domain import finish14,Harness,encode_world
from codec import NativeCreditReplay
w,c=finish14();w.start_finale();w.skip_finale();source=ByteVM();source.p.update(encode_world(w));before=copy.deepcopy((source.p,source.machine.locals));session={'kind':'independent-unfinished-session','inventory':['grease_pencil'],'nested':{'complete':False}}
first=NativeCreditReplay.create(source,session,ByteVM);second=NativeCreditReplay.create(source,session,ByteVM);other=copy.deepcopy((second.viewer.p,second.viewer.machine.locals,second.save()));checks=[]
for kind in ('instance','properties','machine','locals'):
 def factory():
  v=ByteVM()
  if kind=='instance':return source
  if kind=='properties':v.p=source.p
  if kind=='machine':v.machine=source.machine
  if kind=='locals':v.machine.locals=source.machine.locals
  return v
 try:NativeCreditReplay.create(source,session,factory)
 except ValueError as exc:checks.append(dict(alias=kind,rejected=str(exc)))
 else:raise AssertionError(('Shared emitted arena admitted',kind))
 if (source.p,source.machine.locals)!=before:raise AssertionError('Alias probe changed source')
expected=w.create_credit_replay(session);h=Harness(ByteVM,expected.world);h.v=first.viewer
for rec in h.w.credit_ids:
 h.show('credit:'+rec,c);h.plain('advance_finale','p14AdvanceFinale')
if first.return_session()!=session or (source.p,source.machine.locals)!=before or (second.viewer.p,second.viewer.machine.locals,second.save())!=other:raise AssertionError('Parallel emitted replay isolation failed')
second.viewer.call('p14PauseFinale',1);second=NativeCreditReplay.load(json.loads(json.dumps(second.save())),ByteVM)
if not second.viewer.p['p14Paused']:raise AssertionError('Pause lost')
ret=second.return_session(cancel=True);ret['nested']['complete']=True
if second.return_session()!=session:raise AssertionError('Session return aliases')
vm=first.viewer.machine.domain.vm
if any(r[4] for r in vm.returns) or vm.depth or vm.kernel_attempts:raise AssertionError('Emitted stack/kernel')
result=dict(status='PASS',aliases_rejected=checks,credit_records=len(h.w.credit_ids),completed_viewer_instructions=vm.steps,parallel_arenas=True,native_heap_or_savegame=False)
(H/'evidence/direct-emitted-replay.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS_DIRECT_EMITTED_REPLAY',result['credit_records'],vm.steps)
