"""Isolated accepted P14 process prevents evaluator/module-name contamination."""
from pathlib import Path
import sys,json,traceback
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];D=H/'frozen-candidates/p14-domain-reconstruction';R=D/'reference/component'
sys.path[:0]=[str(D/'tests'),str(D),str(R),str(R/'tests')]
from dataclasses import replace
from harness import EmittedDomain,SourceDomain
from codec import M,encode_world,project_context,decode_words,NativeCreditReplay
from test_late_campaign_models import c14,approve14,read,finish14,to_freeze
from cakood.p14_model import P14World,TERMS,PENCIL
owner=None
for line in sys.stdin:
 try:
  request=json.loads(line);op=request['op']
  if op=='prepare':
   c=replace(c14(),repair_date=request['date']);stage=request.get('stage','readback');w=P14World()
   if stage=='readback':
    w,c=approve14(w,c);read(w,c,'signature');w.pin_signature(c);c=replace(c,inventory=c.inventory-{TERMS});w.give_pencil(c);c=replace(c,inventory=c.inventory-{PENCIL});read(w,c,'date')
   elif stage=='consent':w,c=approve14(w,c)
   elif stage=='credits':
    w,c=to_freeze(w,c,tuple(request.get('urls',[])));w.acknowledge_freeze(w.pending_freeze_id);w.advance_finale()
   elif stage=='approvals':w.start(c,{'object_id':TERMS,'location':'inventory','signed':False,'repair_date':None,'signature_owner':'P14','terms_record_id':'P09.READ.002'})
   else:raise ValueError('Unknown stage')
   typ=EmittedDomain if request['kind']=='emitted' else SourceDomain
   owner=typ();owner.p.update(encode_world(w));project_context(owner.call,c,17)
   result=dict(properties=owner.p,source_sha256=M['source_sha256'])
  elif op=='call':result=owner.call(request['name'],*request.get('args',[]))
  elif op=='replay_create':
   original_owner=owner;original_words={k:owner.p[k] for k in M['persisted_properties']}
   owner.persistent=lambda:{k:owner.p[k] for k in M['persisted_properties']}
   def factory():
    viewer=typ();viewer.persistent=lambda:{k:viewer.p[k] for k in M['persisted_properties']};return viewer
   replay=NativeCreditReplay.create(owner,request['session'],factory);owner=replay.viewer;project_context(owner.call,c,23);result=replay.save()
  elif op=='replay_save':result=replay.save()
  elif op=='replay_load':replay=NativeCreditReplay.load(request['envelope'],factory);owner=replay.viewer;project_context(owner.call,c,24);result=replay.save()
  elif op=='replay_return':
   result=dict(session=replay.return_session(cancel=True),original_unchanged={k:original_owner.p[k] for k in M['persisted_properties']}==original_words)
  elif op=='properties':result=owner.p
  elif op=='persisted':result={k:owner.p[k] for k in M['persisted_properties']}
  elif op=='restore':
   values={k:owner.p[k] for k in M['persisted_properties']};decode_words(list(values.values()));owner=typ();owner.p.update(values);result=owner.call('p14AfterRestore')
  elif op=='stop':print(json.dumps({'result':True}),flush=True);break
  else:raise ValueError('Unknown op')
  print(json.dumps({'result':result}),flush=True)
 except Exception as e:print(json.dumps({'error':type(e).__name__+': '+str(e),'trace':traceback.format_exc()}),flush=True)
