#!/usr/bin/env python3
"""Fresh-process focused emitted checks; no native saves or campaign fabrication."""
from pathlib import Path
import gc,hashlib,json,os,resource,sys,time,traceback
from finite_vm import FiniteVM,H
from lifecycle_helpers import tick,diag,restore,observed,check

def opening(kind):
 v=FiniteVM().start();h=v.objects['cakood'];s=v.objects['responsiveSound']
 check(v.proc('psRead',0)==1 and v.proc('rbStatus',0)==100,diag(v))
 v.advance(5);h.call('openingHold');h.call('nextCard')
 if kind=='running':h.call('openingHold');tick(v,31)
 v.saves=[];h.call('writeSave');check(len(v.saves)==1,('actual Save refused',diag(v)))
 saved=v.saves[0];before=diag(saved)
 h.call('nextCard');v=restore(v,saved);h=v.objects['cakood'];s=v.objects['responsiveSound']
 check((h.p['creditCard'],h.p['creditElapsed'],h.p['creditHeld'])==(before['card'],before['tick'],before['held']),('exact restored visual tuple',diag(v),before))
 check(v.proc('psRead',4)==0 and not v.proc('psRead',6) and not v.proc('psRead',7),('admission',diag(v)))
 if kind=='held':
  at=observed(v);v.advance(60);tick(v,1);check(observed(v)==at and v.parsers[s]['pauses']==1,'held owner moved');h.call('openingHold')
 while v.arrays(943)['rpRejoin'][0] and not v.proc('rbStatus',5):tick(v,2)
 check(not v.proc('rbStatus',5) and v.parsers[s]['volume']>0,('resume',diag(v)))
 return dict(kind=kind,saved=before,restored=diag(v),max_parsers=v.max_parsers,instructions=v.steps,scope='Actual Main native-kernel-model Save/Restore; no native file created')
def startup():
 v=FiniteVM().start();h=v.objects['cakood'];s=v.objects['responsiveSound'];h.call('finishOpening',2)
 before=v.steps;v.proc('psPoll',h,v.now);start_cost=v.steps-before
 check(v.proc('psRead',1)==101 and v.proc('rbStatus',0)==101,'P01 invitation not activated')
 before_event=(v.proc('rbStatus',19),v.proc('psRead',1));check(v.proc('psCommitted',h,994,8,0,1,0,0)==0,'forged confetti accepted');check(before_event==(v.proc('rbStatus',19),v.proc('psRead',1)),'forged receipt changed ownership')
 for _ in range(12):v.advance(2);v.proc('psPoll',h,v.now)
 costs=[];guard_before=v.calls[943,'rbVerify']+v.calls[948,'pmVerify']
 for _ in range(5):
  v.advance(2);before=v.steps;v.proc('psPoll',h,v.now);costs.append(v.steps-before)
 guard_after=v.calls[943,'rbVerify']+v.calls[948,'pmVerify'];check(guard_after==guard_before,'unchanged frame scanned static guards')
 starts=v.proc('rbStatus',19);parser=id(v.parsers[s]);check(v.proc('rbScoreRequest',104,0,0)==1,'alias request')
 check(v.proc('rbStatus',19)==starts and id(v.parsers[s])==parser,'alias restarted clock')
 # Audio-only route request: actual game facts are not changed or claimed.
 before=v.steps;check(v.proc('rbScoreRequest',102,0,0)==1,'valid explicit audio edge');request_cost=v.steps-before
 begin=v.now&65535
 while v.proc('rbStatus',0)!=151 and not v.proc('rbStatus',5):
  v.advance(2);v.proc('rbPoll',v.proc('rbStatus',3),v.proc('rbStatus',4),v.objects['contestState'])
  check(((v.now&65535)-begin)%65536<5500,'finite source-edge bound exceeded')
 check(v.proc('rbStatus',0)==151 and not v.proc('rbStatus',5),('edge did not complete',diag(v)))
 return dict(start_cue=101,unchanged_frame_instructions=costs,unchanged_guard_calls=guard_after-guard_before,initial_owner_admission_instructions=start_cost,changed_request_instructions=request_cost,alias_restarts=0,max_active_parsers=v.max_parsers,scope='Genuine startup/P01; subsequent alias and edge are explicit audio-component calls, no changed campaign facts')
def guards():
 v=FiniteVM(instructions_per_tick=0);check(v.proc('rbVerify')==1,'full emitted guard rejected')
 j=json.loads((H/'generated/BROKER-GUARD-CHUNKS.json').read_text());results=[]
 # One real corruption on each typed page plus each page-crossing row boundary.
 picks=[]
 for n in(248,260,261):picks.append(next(r for r in j['chunks']if r['resource']==n))
 for r in picks:
  key=(3,r['resource']);raw=v.resources[key];parts=raw.split(b'\0');i=r['text_index'];part=bytearray(parts[i]);part[0]=57 if part[0]!=57 else 56;parts[i]=bytes(part);v.resources[key]=b'\0'.join(parts)
  check(v.proc('rbVerify')==0,('corrupted typed page accepted',key));v.resources[key]=raw;results.append(r['resource'])
 check(v.proc('rbVerify')==1,'guard failed after exact resource restoration')
 return dict(emitted_corruption_rejected=results,exact_words=j['word_count'],scope='Real compiled rbVerify reading typed Text resources')
def transports():
 v=FiniteVM(instructions_per_tick=0);rows=json.loads((H/'generated/LOOP-TRANSPORTS.json').read_text())['transports'];results=[]
 # No host campaign is started. These are table-method unit calls against the
 #actual emitted instance, using its source-defined expression data.
 for row in rows:
  cue=row['cue'];obj=v.objects[f'cue{cue}ReadyTransport'];table=json.loads((H/f'generated/{cue}-tables.json').read_text())['tables'];events=[table['expressionEvents'][i:i+3]for i in range(0,len(table['expressionEvents']),3)]
  for wrapped in(0,1):
   obj.p['loopHasWrapped']=wrapped
   for at in(0,12,table['keyWindows'][-3]if False else json.loads((H/f'generated/{cue}-tables.json').read_text())['loop']['end_tick']-1):
    for part in range(8):
     expected=(table['loopExpression']if wrapped else table['initialExpression'])[part]
     for tick,p,value in events:
      if p==part and tick<=at:expected=value
     check(obj.call('expressionAt',part,at)==expected,('wrong local expression table',cue,part,at,wrapped))
  check(v.proc(f'cue{cue}Verify')==1,('transport guard',cue));results.append(cue)
 return dict(cues=results,actual_emitted_expression_queries=len(rows)*2*3*8,scope='Isolated emitted transport table units, not campaign/native acceptance')
def finite():
 v=FiniteVM(instructions_per_tick=0);s=v.objects['responsiveSound'];a=v.arrays(943)
 # Explicit unit boundary: only the music owner is configured. No puzzle state,
 # SaveGame, RestoreGame or production admission result is fabricated.
 for key,value in [('rbSound',s),('rbEnabled',1),('fsEnabled',1),('rbGenerationLo',1)]:a[key][0]=value
 check(v.proc('rbPresentation',0,119,0,0)==1,'finite119 start')
 check(v.proc('rbScoreRequest',121,0,1)==1,'queue121')
 v.advance(2890);v.proc('rbPoll',v.proc('rbStatus',3),v.proc('rbStatus',4),v.objects['contestState']);check(v.proc('rbStatus',0)==119,'119 truncated')
 v.advance(2);v.proc('rbPoll',v.proc('rbStatus',3),v.proc('rbStatus',4),v.objects['contestState']);check(v.proc('rbStatus',0)==121,'121 native-terminal entry')
 check(v.max_parsers==1,'two finite owners');v.proc('rbPresentation',3,0,0,0);check(not v.parsers and v.proc('rbStatus',0)==0,'Skip failed immediate retirement')
 check(v.proc('rbScoreRequest',129,0,1)==1,'speech-space start');gap=json.loads((H/'generated/FULL-BROKER-TABLES.json').read_text())['speech_gap'];v.advance(gap[0]+2);v.proc('rbPoll',v.proc('rbStatus',3),v.proc('rbStatus',4),v.objects['contestState'])
 at=v.parsers[s]['tick'];check(v.parsers[s]['pauses']==1,'source speech silence not held');v.advance(300);check(v.parsers[s]['tick']==at,'speech time driven by music')
 check(v.proc('rbScoreRequest',116,0,1)==1,'semantic pending truth target');v.proc('rbPoll',v.proc('rbStatus',3),v.proc('rbStatus',4),v.objects['contestState']);v.advance(1200);v.proc('rbPoll',v.proc('rbStatus',3),v.proc('rbStatus',4),v.objects['contestState'])
 check(v.proc('rbStatus',0)==129,'uncommitted truth admitted116')
 return dict(quiet_preserved_ticks=2892,credits_entered_at_real_end=True,speech_gap=gap,uncommitted_truth_blocked=True,max_parsers=v.max_parsers,scope='Music-only emitted units; no campaign/save admission claim')
CASES={'held':lambda:opening('held'),'running':lambda:opening('running'),'startup':startup,'guards':guards,'transports':transports,'finite':finite}
if __name__=='__main__':
 name=sys.argv[1];start=time.monotonic();build=Path(os.environ.get('CAKOOD_SCORE_BUILD',str(H.parents[1]/'build/coherent')));out=dict(case=name,native_acceptance=False,compile_sha256=hashlib.sha256((build/'compile-receipt.json').read_bytes()).hexdigest())
 try:out['result']=CASES[name]();out['status']='PASS';code=0
 except BaseException as e:out.update(status='FAIL',error=repr(e),traceback=traceback.format_exc());code=1
 out.update(exit_code=code,elapsed_seconds=time.monotonic()-start,max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (Path(__file__).resolve().parent/'results'/f'EMITTED-{name}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in('case','status','exit_code','elapsed_seconds','max_rss_kib')}),flush=True)
 if code:print(out['traceback'],flush=True)
 sys.exit(code)
