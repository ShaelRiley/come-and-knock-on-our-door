"""NEW paired P14 adapter on genuine accepted upstream Python owners.

This does not turn the R2 witness or cross-owner transfers into native storage.
Every forwarded P14 action compares actual emitted instructions with the source
and the accepted model. The original joined fixture owns physical dispatch.
"""
from test_domain import Harness,M,CO,P14World,PairedVM,oid
from codec import encode_world,project_context,credit_masks,terms_handoff_args
from paired import restore_words
import finale_join
N={'actions':0,'queries':0,'restores':0,'callbacks':0}
CONTEXT={'start':'p14StartCommitments','give_card':'p14GiveCard','confirm_jackie':'p14ConfirmJackie','pin_card':'p14PinCard','request_signature':'p14RequestSignature','pin_signature':'p14PinSignature','give_pencil':'p14GivePencil','complete_commitments':'p14CompleteCommitments','begin_presentation':'p14Begin','resume_presentation':'p14Resume','hint':'p14Hint','dispatch':'p14Act','present_finale':'p14PresentFinale'}
PLAIN={'advance_finale':'p14AdvanceFinale','claim_tag_laugh':'p14ClaimTagLaugh','claim_celebration':'p14ClaimCelebration','pause_finale':'p14PauseFinale','skip_finale':'p14SkipFinale','audio_finished':'p14AudioFinished'}
class JoinedPair:
 # Expose accepted model field metadata to its unchanged dataclass codec.
 __dataclass_fields__=P14World.__dataclass_fields__
 def __init__(self,w=None):
  self.h=Harness(PairedVM,w);self.h.epoch=200;self.last_context=None
  if w is not None:
   self.h.v=restore_words(list(encode_world(w).values()));N['restores']+=1
 def __getattr__(self,name):
  if name in CONTEXT:
   def call(c,*args):
    if name=='start':terms_handoff_args(args[0] if args else None)
    self._project(c)
    r=self.h.action(name,CONTEXT[name],*args,c=c);N['actions']+=1;return r
   return call
  if name in PLAIN:
   def call(*args):
    if name=='audio_finished':
     r=self.h.w.audio_finished(*args);self.h.v.call('p14AudioFinished');r=self.h.check(r)
    else:r=self.h.plain(name,PLAIN[name],*args)
    N['actions']+=1;return r
   return call
  return getattr(self.h.w,name)
 def _project(self,c):
  # Validate the complete actual owner evidence before changing durable P14.
  self.last_context=c;self.h.epoch+=1
  project_context(self.h.v.call,c,self.h.epoch);self.h.context=c
 def start_finale(self,urls=()):
  masks=credit_masks(urls);r=self.h.w.start_finale(urls);self.h.v.call('p14StartFinale',*masks);N['actions']+=1;return self.h.check(r)
 def acknowledge_presentation(self,c,handle,record_id=None,speech_unit_ids=()):
  self._project(c);w=self.h.w
  source=handle.split(':',2)[2].rsplit(':',1)[0]
  current=source in w.presentations and handle==w._handle(source)
  serial=int(handle.rsplit(':',1)[1]);sid=M['sources'][source]
  if current:self.h.v.call('p14Resume',sid)
  r=w.acknowledge_presentation(c,handle,record_id=record_id,speech_unit_ids=speech_unit_ids)
  self.h.v.call('p14Acknowledge',sid,*divmod(serial,32768),self.h.epoch if current else self.h.epoch-1,M['line_ids'][record_id] if record_id else 0,M['speech_unit_ids'][speech_unit_ids[0]] if speech_unit_ids else 0,M['speech_unit_ids'][speech_unit_ids[-1]] if speech_unit_ids else 0)
  N['actions']+=1;N['callbacks']+=1;return self.h.check(r)
 def cancel_presentation(self,handle):
  w=self.h.w;source=handle.split(':',2)[2].rsplit(':',1)[0];serial=int(handle.rsplit(':',1)[1]);current=source in w.presentations and handle==w._handle(source)
  r=w.cancel_presentation(handle);self.h.v.call('p14Cancel',M['sources'][source],*divmod(serial,32768),self.h.epoch if current else self.h.epoch-1);N['actions']+=1;return self.h.check(r)
 def acknowledge_freeze(self,handle):
  w=self.h.w;current=handle==w.pending_freeze_id;r=w.acknowledge_freeze(handle)
  self.h.v.call('p14AcknowledgeFreeze',*divmod(w.finale_started_at,32768),self.h.epoch if current else self.h.epoch-1);N['actions']+=1;return self.h.check(r)
 def notebook_gate(self,c):
  self._project(c);self.h.notebook(c);N['queries']+=1;return self.h.w.notebook_gate(c)
 def restart(self,c):
  raw=self.h.w.save();words=list(self.h.v.persistent().values());self.h.w=P14World.load(raw);self.h.v=restore_words(words);self._project(c);self.h.queries();N['restores']+=1
class FinaleJoined(finale_join.FinaleJoined):
 def __setattr__(self,name,value):
  if name=='w' and isinstance(value,P14World):value=JoinedPair(value)
  super().__setattr__(name,value)
class ModelFactory:
 def __call__(self,*a,**kw):return JoinedPair(P14World(*a,**kw))
 def load(self,*a,**kw):return JoinedPair(P14World.load(*a,**kw))
 def __getattr__(self,name):return getattr(P14World,name)
