from pathlib import Path
import unittest,sys,copy
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests'),str(H/'tools')]
from host import setup,base
class CalleTests(unittest.TestCase):
 def case(self):
  h,d,a,*_=setup();v=h.vm;m,pc=v.resolve(d,'hStaticAt');pcs=v.method_boundaries(m,pc);call=next(p for p in sorted(pcs) if v.decode(m,p)[0]==35 and v.decode(m,p)[1]==[999,0,4]);return v,d,m,call
 def test_argument_packet_cleanup_and_nested_return(self):
  v,d,m,pc=self.case();before=len(v.returns)
  self.assertEqual(d.call('hStaticAt',21,0),1552);self.assertEqual(d.call('hStaticAt',21,-1),0)
  rows=v.returns[before:];self.assertTrue(any(n==999 for n,*_ in rows));self.assertTrue(all(len(stack)<=1 for n,name,at,temps,stack in rows));self.assertEqual(d.call('hStaticAt',1,1),-1)
  bank=v.modules[999];self.assertFalse(bank.layout['objects']);self.assertFalse(bank.layout['script_relocations']);self.assertFalse(bank.layout['heap_relocations'])
 def test_odd_and_oversized_call_packets_reject(self):
  for callbytes in (3,6):
   v,d,m,pc=self.case();op,args,end=v.decode(m,pc);raw=bytearray(m.blob);raw[end-1]=callbytes;m.blob=bytes(raw);m.decoded.pop(pc,None)
   with self.assertRaises(base.VMError):d.call('hStaticAt',21,0)
 def test_wrong_module_export_and_arity_reject(self):
  for field,value in [(0,998),(1,20),(1,1)]:
   v,d,m,pc=self.case();op,args,end=v.decode(m,pc);args[field]=value;m.decoded[pc]=(op,args,end)
   with self.assertRaises(base.VMError):d.call('hStaticAt',21,0)
 def test_export_object_outside_code_and_missing_module_reject(self):
  for mode in ('object','outside','missing'):
   v,d,m,pc=self.case();bank=v.modules[999]
   if mode=='object':bank.objects[bank.layout['exports'][0]]=d
   elif mode=='outside':bank.layout['exports'][0]=len(bank.blob)+100
   else:del v.modules[999]
   with self.assertRaises(base.VMError):d.call('hStaticAt',21,0)
if __name__=='__main__':unittest.main()
