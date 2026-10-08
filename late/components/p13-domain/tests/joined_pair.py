"""Current reference owner joins with every P13 transition checked in emitted SCI.

The wrapper forwards genuine upstream model ownership and logical actor events.
It does not implement a native host or use bytecode to simulate other owners.
"""
from test_domain import Harness,M,CO,oid,PairedVM
from codec import encode_world
from cakood.p13_model import P13World
import current_join
from dataclasses import replace
N={'actions':0,'restores':0,'queries':0,'callbacks':0}
METHODS={'start':'p13Handoff','give_program':'p13GiveProgram','confirm_seating':'p13ConfirmSeating','deliver_pot':'p13DeliverPot','pull_serve':'p13PullServe','deliver_display':'p13DeliverDisplay','open_screen':'p13OpenScreen','pull_show':'p13PullShow','deliver_board':'p13DeliverBoard','request_contest':'p13RequestContest','pull_toast':'p13PullToast','protect_furniture':'p13ProtectFurniture','claim_laugh':'p13ClaimLaugh','begin_presentation':'p13Begin','resume_presentation':'p13Resume','preview':'p13Preview','hint':'p13Hint','dispatch':'p13Act','ask_rita':'p13AskRita','call_attention':'p13CallAttention'}
class JoinedPair:
 def __init__(self,w=None):self.h=Harness(PairedVM,w);self.h.epoch=100;self.last_context=None
 def __getattr__(self,name):
  if name in METHODS:
   def call(c,*args):
    self.last_context=c;self.h.context=None
    if name in ('ask_rita','call_attention'):
     self.h.project(c);r=getattr(self.h.w,name)(c,*args);self.h.v.call('p13Begin',M['sources']['rita_ready' if name=='ask_rita' else 'attention']);self.h.check(r)
    else:r=self.h.action(name,METHODS[name],*args,c=c)
    N['actions']+=1;return r
   return call
  return getattr(self.h.w,name)
 def _project(self,c=None):
  if c is not None:self.last_context=c
  if self.last_context is None:raise ValueError('No genuine current context')
  self.h.context=None;self.h.project(self.last_context)
 def acknowledge_presentation(self,c,handle,record_id=None,speech_unit_ids=()):
  self._project(c);w=self.h.w
  source=next((s for s in w.presentations if handle==w._handle(s)),None)
  if source is None:
   bits=handle.split(':');source=bits[-2] if len(bits)>2 and bits[-2] in M['sources'] else next(iter(w.presentations))
  p=w.presentations[source];sid=M['sources'][source];current=handle==w._handle(source)
  self.h.v.call('p13Resume',sid)
  r=w.acknowledge_presentation(c,handle,record_id=record_id,speech_unit_ids=speech_unit_ids)
  self.h.v.call('p13Acknowledge',sid,*divmod(p.serial,32768),self.h.epoch if current else self.h.epoch-1,M['line_ids'][record_id] if record_id else 0,M['speech_unit_ids'][speech_unit_ids[0]] if speech_unit_ids else 0,M['speech_unit_ids'][speech_unit_ids[-1]] if speech_unit_ids else 0)
  N['actions']+=1;N['callbacks']+=1;return self.h.check(r)
 def finish_contest_request(self,request,accepted):
  self._project();w=self.h.w;serial=w.contest_request_at;current=request==w.pending_contest_request_id
  r=w.finish_contest_request(request,accepted);self.h.v.call('p13FinishContestRequest',*divmod(serial,32768),self.h.epoch if current else self.h.epoch-1,int(accepted));N['actions']+=1;return self.h.check(r)
 def acknowledge_wrong_visual(self,c,request):
  self._project(c);w=self.h.w;current=request==w.pending_wrong_visual_id;serial=w.wrong_at
  r=w.acknowledge_wrong_visual(c,request);self.h.v.call('p13AcknowledgeWrongVisual',*divmod(serial,32768),self.h.epoch if current else self.h.epoch-1);N['actions']+=1;return self.h.check(r)
 def audio_finished(self,*args):
  r=self.h.w.audio_finished(*args);self.h.v.call('p13AudioFinished');N['actions']+=1;return self.h.check(r)
 def acknowledge_autosave(self,request):
  self._project();w=self.h.w;bits=request.split(':');cue=bits[-2];serial=int(bits[-1]);current=any(q['request_id']==request for q in w.pending_autosaves)
  r=w.acknowledge_autosave(request);self.h.v.call('p13AcknowledgeAutosave',M['words'][cue],*divmod(serial,32768),self.h.epoch if current else self.h.epoch-1,1);N['actions']+=1;return self.h.check(r)
 def cancel_presentation(self,handle):
  w=self.h.w;source=next(s for s in w.presentations if w._handle(s)==handle);p=w.presentations[source]
  r=w.cancel_presentation(handle);self.h.v.call('p13Cancel',M['sources'][source],*divmod(p.serial,32768),self.h.epoch);N['actions']+=1;return self.h.check(r)
 def restart(self,c):
  saved=self.h.w.save();words=list(self.h.v.persistent().values());old=self.h.epoch
  self.h.w=P13World.load(saved,context=c)
  from paired import restore_words
  self.h.v=restore_words(words);self.h.epoch=old+1;self.h.context=None;self.last_context=c;self._project();self.h.queries();N['restores']+=1
 def queries(self,c):self._project(c);self.h.queries();N['queries']+=1
class Joined(current_join.Joined):
 def __setattr__(self,name,value):
  if name=='w' and isinstance(value,P13World):
   value=JoinedPair(value)
   if hasattr(self,'board_room'):value.last_context=self.context()
  super().__setattr__(name,value)
