"""Narrow SCI1-late DoSound9/16 no-live-slot transport mocks.

This harness has no synthesizer/music slots: previous DoSound6/8 calls are
transport stubs. Match the exact stock no-slot branch, not a live audio engine.
Verified source: runtime-reference/SOURCE.json, kernel_tables.h:144,151;
soundcmd.cpp:306-317,873-895. Stop preserves accumulator without a live
slot; SetLoop writes -1/1 to the object before the absent-slot return. No score, reader, ownership or callback is synthesized.
"""
def install(base_class, core):
 class StopVM(base_class):
  def _kernel(self,k,args):
   if self.knames.get(k)=='DoSound' and args and args[0] in (9,16):
    core.require(len(args)==(2 if args[0]==9 else 3),'Unsupported DoSound9/16 arity',args)
    obj=args[1]
    core.require(isinstance(obj,core.Object) and obj.module.number==0 and obj.name in ('credits','bed'),'Unsupported DoSound9/16 owner',args)
    core.require(hasattr(self,'_kernel_accumulator'),'DoSound9/16 needs actual pre-call SCI accumulator')
    if args[0]==16:
     core.require(type(args[2]) is int and -32768<=args[2]<=32767,'Invalid DoSound16 loop',args)
     obj.p['loop']=-1 if args[2]==-1 else 1
    self.ktrace.append(('DoSound',tuple(args)))
    return self._kernel_accumulator
   return super()._kernel(k,args)
 return StopVM
