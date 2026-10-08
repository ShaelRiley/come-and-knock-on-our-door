"""Recovered finite transport and restore checks only; broad mutation corpus retained immutable but omitted here."""
from test_domain import P10World,C,RACK,KNOWN,replace,COURTYARD,TILE_IDS,PAPER_IDS,ORDER,M,encode_world,encode_save,decode_words,Compiled,source_vm,HERE,hashlib,json,unittest,copy,itertools

def snapshots():
 out=[]
 def add(w):out.append(encode_world(w))
 w=P10World();add(w)
 r=w.introduce(C);add(w)
 for u in w._tokens('intro'):w.acknowledge_presentation(C,r.presentation_id,speech_unit_ids=(u,));add(w)
 r=w.begin_presentation(C,'plan');add(w);w.acknowledge_presentation(C,r.presentation_id,record_id='P10.READ.001');add(w)
 w.prepare_paper(C);add(w)
 for ids in (TILE_IDS,PAPER_IDS):
  for obj,word in zip(ids,ORDER):w.write(C,obj,word);add(w)
 for i,obj in enumerate(TILE_IDS):w.place(RACK,obj,i);add(w)
 for source in ('tiles','rack','credit','bread_agreement','notebook'):
  ctx=replace(RACK,rita_room=COURTYARD);r=w.begin_presentation(ctx,source);add(w)
  for token in w._tokens(source):
   kw={'speech_unit_ids':(token,)} if token in M['speech_unit_ids'] else {'record_id':token}
   w.acknowledge_presentation(ctx,r.presentation_id,**kw);add(w)
 for i in range(3):w.remove(RACK,i);add(w)
 for i,obj in enumerate(PAPER_IDS):w.place(RACK,obj,i);add(w)
 w.write(RACK,PAPER_IDS[0],None);add(w);w.hint(RACK,3);add(w)
 for revision in (32766,32767,32768,M['max_serial']):
  w=P10World(revision=revision);add(w)
  if revision<M['max_serial']-2:w.introduce(C);add(w)
 return out

def model_verdict(p):
 try:
  data=decode_words([p[k] for k in M['persisted_properties']])
  if encode_save(data)!=p:return 0
  P10World.load(data);return 1
 except (ValueError,TypeError,KeyError):return 0

class ValidationTests(unittest.TestCase):
 def test_strict_transport_types_and_fields(self):
  pristine=P10World().save()
  for mutation in (lambda d:d.update(schema=True),lambda d:d['state'].update(revision=True),lambda d:d['state'].update(revision=M['max_serial']+1),lambda d:d['state'].update(unknown=1),lambda d:d['state'].update(hint_level=True),lambda d:d['state']['labels'].update({TILE_IDS[0]:True}),lambda d:d['state'].update(slots=[True,None,None]),lambda d:d['state'].update(labels={})):
   value=copy.deepcopy(pristine);mutation(value)
   with self.assertRaises(ValueError):encode_save(value)
  w=P10World();r=w.introduce(C);w.acknowledge_presentation(C,r.presentation_id,speech_unit_ids=('P10.OPEN.001.01','P10.OPEN.001.02'))
  for mutation in (lambda d:d['state']['presentations']['intro'].update(serial=0),lambda d:d['state']['presentations']['intro']['receipts'].update({'P10.OPEN.001.01':0}),lambda d:d['state']['presentations']['intro'].update(receipts={'P10.OPEN.001.02':3,'P10.OPEN.001.01':3})):
   value=w.save();mutation(value)
   with self.assertRaises(ValueError):encode_save(value)
  words=list(encode_world(w).values())
  for value in (True,-1,32768,'0'):
   bad=words.copy();bad[2]=value
   with self.assertRaises(ValueError):decode_words(bad)
  with self.assertRaises(ValueError):decode_words(words[:-1])
 def test_corrupt_restore_drains_callbacks_and_fails_closed(self):
  from test_domain import ByteVM,Harness,CO,oid
  for typ in (source_vm.VM,ByteVM):
   h=Harness(typ);h.prepare();before=h.v.persistent();h.v.p['p10Slot0']=oid(TILE_IDS[0]);h.v.p['p10Slot1']=oid(TILE_IDS[0])
   self.assertEqual(h.v.call('p10AfterRestore'),0);self.assertEqual(h.v.p['p10ContextValid'],0)
   h.v.call('p10Write',oid(TILE_IDS[0]),1);self.assertEqual(CO[h.v.p['p10Code']],'invalid_state')
   self.assertEqual(h.v.p['p10EventCount'],0)

if __name__=='__main__':unittest.main()
