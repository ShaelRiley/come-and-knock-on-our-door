"""Independent native save rejection, source/model parity, all physical projections."""
from test_domain import *
import random
del DomainTests,BytecodeTests

def snapshots():
 w=P12World();out=[]
 def snap():out.append(w.save())
 def act(fn,*args,c=C):getattr(w,fn)(c,*args);snap()
 def show(source,c=C):
  act('begin_presentation',source,c=c)
  for token in w._tokens(source):
   if token in M['speech_unit_ids']:w.acknowledge_presentation(c,w._handle(source),speech_unit_ids=(token,))
   else:w.acknowledge_presentation(c,w._handle(source),record_id=token)
   snap()
 snap();act('start',RACK)
 for source in ('opening','rack','diagram','edge'):show(source)
 for source in ('audience_view','self_view','catch','rehearsal'):show(source,A)
 act('release_catch',c=A);act('rotate_rack');act('order_cards',TILE_IDS);show('introduction');act('commit_introduction');act('release_confetti');show('confetti');act('claim_laugh');show('cleanup');act('finish_welcome')
 return out

def model_valid(p):
 try:
  d=decode_words(list(p.values()));P12World.load(d)
  # A native vector is canonical only if no word was discarded by decoding.
  return encode_save(d)==p
 except (ValueError,KeyError,TypeError,IndexError):return False

class TransportTests(unittest.TestCase):
 def test_ordinary_saved_histories_roundtrip_in_both_evaluators(self):
  from paired import PairedVM,MEASUREMENTS
  states=snapshots();v=PairedVM()
  for data in states:
   p=encode_save(data);words=list(p.values());decoded=decode_words(words)
   self.assertEqual(decoded,data);self.assertEqual(encode_save(decoded),p);P12World.load(decoded)
   v.p.update(p);self.assertEqual(v.call('p12AfterRestore'),1);self.assertEqual(v.persistent(),p)
   self.assertEqual(v.p['p12ContextValid'],0);self.assertEqual(v.arrays['p12Lease'],[0]*12)
  (HERE/'evidence/ordinary-transport.json').write_text(json.dumps(dict(status='PASS',reachable_saves=len(states),paired=MEASUREMENTS),indent=2)+'\n')
 def test_strict_codec_malformed_types_and_restore_fail_closed(self):
  raw=snapshots()[-1]
  for value in (True,'1',1.1,-1,M['max_serial']+1):
   bad=copy.deepcopy(raw);bad['state']['revision']=value
   with self.assertRaises(ValueError):encode_save(bad)
  for key,value in [('kind','other'),('schema',True),('state',[]),('extra',1)]:
   bad=copy.deepcopy(raw);bad[key]=value
   with self.assertRaises(ValueError):encode_save(bad)
  for key,value in [('slots',['cue_rack']*3),('words',{'bad':'SERVE'}),('presentations',{'bad':{'serial':1,'receipts':{}}})]:
   bad=copy.deepcopy(raw);bad['state'][key]=value
   with self.assertRaises(ValueError):encode_save(bad)
  bad=copy.deepcopy(raw);p=bad['state']['presentations']['introduction'];p['receipts']=dict(reversed(list(p['receipts'].items())))
  with self.assertRaises(ValueError):encode_save(bad)
  for typ in (source_vm.VM,ByteVM):
   h=Harness(typ);h.repair();h.begin('introduction');h.project();p=encode_world(h.w);p['p12ReleaseLo']=0;h.v.p.update(p);self.assertEqual(h.v.call('p12AfterRestore'),0);self.assertEqual(h.v.p['p12ContextValid'],0)
   self.assertEqual(h.v.p['p12EventCount'],0);self.assertEqual(h.v.p['p12PresentationSource'],0)
   before=h.v.persistent();h.v.call('p12ReleaseConfetti');self.assertEqual(CO[h.v.p['p12Code']],'invalid_state');self.assertEqual(before,h.v.persistent())
 def test_context_words_and_unregistered_inventory_fail_closed(self):
  args=[4,0,1,1,1,1,4,1,1,1,0,1,4,4,4,4,4,4,4,1]
  for typ in (source_vm.VM,ByteVM):
   v=typ()
   for i in range(len(args)):
    for x in (-2,7,32767):
     if i==19 and x>0:continue
     bad=list(args);bad[i]=x
     if i!=19:bad[-1]=100+i*3+(x%3)
     self.assertEqual(v.call('p12Context',*bad),0)
   args[-1]=500;self.assertEqual(v.call('p12Context',*args),1)
   # Current P07 owns pot_lid93, which is a valid external inventory item.
   args[-1]+=1;self.assertEqual(v.call('p12Context',*args),1)
   self.assertEqual(v.call('p12ContextItem',oid('pot_lid')),1)
   for obj in (0,115,394,409,421,32767,oid('jack'),oid('felix')):
    args[-1]+=1;self.assertEqual(v.call('p12Context',*args),1);self.assertEqual(v.call('p12ContextItem',obj),0);self.assertEqual(v.p['p12ContextValid'],0)

if __name__=='__main__':unittest.main()
