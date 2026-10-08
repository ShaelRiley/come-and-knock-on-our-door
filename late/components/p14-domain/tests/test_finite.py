"""NEW finite capacity, ordinary saved words, and emitted runner guard tests."""
import unittest,json,copy,tempfile,os
from test_domain import *
from paired import restore_words
from harness import EmittedDomain
MEASUREMENTS=[]
class FiniteTests(unittest.TestCase):
 def test_mutating_boundaries_exhaust_atomically(self):
  cases=[]
  class RecordingVM(source_vm.VM):
   def call(self,name,*args):
    root=not getattr(self,'recording_depth',0);self.recording_depth=getattr(self,'recording_depth',0)+1
    before=copy.deepcopy((self.p,self.arrays)) if root and name!='p14Init' else None
    try:r=super().call(name,*args)
    finally:self.recording_depth-=1
    if before and (self.p['p14RevisionHi'],self.p['p14RevisionLo'])!=(before[0]['p14RevisionHi'],before[0]['p14RevisionLo']):cases.append((name,args,before))
    return r
  h=Harness(RecordingVM);c=h.finish();h.start_finale()
  for s in ('closing:professional','meal','tag'):
   c=finale_context(c,s);h.show(s,c)
   if s=='tag':h.plain('claim_tag_laugh','p14ClaimTagLaugh')
   h.plain('advance_finale','p14AdvanceFinale')
  h.ack_freeze();h.plain('claim_celebration','p14ClaimCelebration');h.plain('advance_finale','p14AdvanceFinale')
  h.plain('pause_finale','p14PauseFinale',True);h.plain('pause_finale','p14PauseFinale',False)
  for rec in h.w.credit_ids:
   h.show('credit:'+rec,c);h.plain('advance_finale','p14AdvanceFinale')
  for name,args,(props,arrays) in cases:
   v=PairedVM();v.p.update(props)
   for key,value in arrays.items():v.arrays[key][:]=value;v.emitted.domain.arrays[key][:]=value
   v.p['p14RevisionHi'],v.p['p14RevisionLo']=divmod(M['max_serial'],32768)
   before=v.persistent();v.call(name,*args)
   self.assertEqual(CO[v.p['p14Code']],'serial_exhausted',name);self.assertEqual(v.persistent(),before);self.assertEqual(v.p['p14EventCount'],0)
  MEASUREMENTS.append(dict(gate='all_reachable_mutating_boundaries',count=len(cases),methods=sorted({n for n,a,b in cases})))
 def test_serial_limb_carry_last_start_and_restore(self):
  for revision in (32766,32767,32768,65535,65536,M['max_serial']-1):
   h=Harness(PairedVM,P14World(revision=revision));h.start();self.assertEqual(h.w.revision,revision+1);h.restore();h.queries()
  MEASUREMENTS.append(dict(gate='serial_limb_boundaries',cases=6))
 def test_emitted_bad_opcode_stack_packet_and_strict_arity_rejected(self):
  from host_vm import VMError
  v=PairedVM()
  for args in ((),(1,2),(True,),('1',),(1.0,),(32768,),(-32769,)):
   with self.assertRaises(ValueError):v.call('p14Hint',*args)
  for opcode,needle in ((29,'Operand stack underflow'),(32,'Unsupported opcode')):
   d=EmittedDomain();vm=d.vm;m,pc=vm.resolve(d.object,'p14Ready');vm.method_boundaries(m,pc);_,_,end=vm.decode(m,pc);m.decoded[pc]=(opcode,[],end)
   with self.assertRaisesRegex(VMError,needle):d.call('p14Ready')
  d=EmittedDomain();sel=next(i for i,n in d.vm.names.items() if n=='p14Ready')
  with self.assertRaisesRegex(VMError,'Send argument count'):d.vm.send(d.object,[sel,1])
 def test_all_ordinary_save_snapshots_restart_actual_bytecode(self):
  from test_validation import snapshots
  states=snapshots()
  for saved in states:
   words=list(encode_save(saved).values());v=restore_words(words)
   self.assertEqual(decode_words(list(v.persistent().values())),saved)
   for key in ('p14ContextValid','p14EventCount','p14PresentationSource'):self.assertEqual(v.p[key],0)
  MEASUREMENTS.append(dict(gate='ordinary_save_transport',reachable_snapshots=len(states),native_savegame=False))
