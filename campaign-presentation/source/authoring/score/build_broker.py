#!/usr/bin/env python3
from pathlib import Path
import json,re,collections
import build_catalog as c
from guard_chunks import guard_split
H=c.H;g=c.g

def prepend(src,name,body):
 m=re.search(r'(?m)^\(procedure \('+name+r'[^\n]*\n',src);assert m,name
 return src[:m.end()]+body+'\n'+src[m.end():]
def main():
 src=(H/'src/module943.sc').read_text();start=src.index('(procedure (rbVerify ')
 proc=src[start:]
 # Remove/rebuild rbVerify against the complete generated static rows.
 names=re.findall(r'\(procedure \((\w+)',proc)
 verifyend=proc.index('\n(procedure (',1);proc=proc[verifyend+1:]
 # Preserve all A04 original finite arrays byte-for-byte.
 oldrows=[]
 for name,count,vals in re.findall(r'\[([A-Za-z]\w*) (\d+)\] = \[([^\]]*)\]',src[:start]):
  v=[int(x)for x in vals.split()];assert len(v)==int(count)
  if name!='rbHighwater':oldrows.append((name,v,False))
 oldrows=[r for r in oldrows if r[0] not in('rbBridgeMetadata','rbBridgeControllers')]
 bridge=[];controls=[]
 for n in [*range(122,129),148,149,150,153,154,220]:
  ev=c.decode_sound((H/f'assets/{n}.sound.bin').read_bytes());end=max(t for rows in ev.values()for t,msg in rows)
  off=max(t for ch,rows in ev.items()if ch!=15 for t,msg in rows if msg[0]&240==128 or(msg[0]&240==144 and msg[-1]==0))
  attack=min(t for ch,rows in ev.items()if ch!=15 for t,msg in rows if msg[0]&240==144 and msg[-1])
  bridge.extend([n,end,off,attack])
  for ch,rows in ev.items():
   if ch!=15:
    controls += [v for tick,msg in rows if tick==0 and msg[0]&240 in(176,192)for v in[n,ch,msg[0]&240,msg[1],msg[2]if len(msg)>2 else 0]]
 rows=oldrows+[('rbBridgeMetadata',bridge,False),('rbBridgeControllers',controls,False)]
 catalog=json.loads((H/'generated/FULL-SCORE-CATALOG.json').read_text());edges=catalog['edges'];adj=collections.defaultdict(list)
 for e in edges:adj[e['source']].append(e['target'])
 # State aliases may retain a semantic identity while contest transport stays152.
 for a in range(140,146):
  for b in range(140,146):
   if a!=b:adj[a].append(b)
 route=[]
 for source in sorted(adj):
  seen={source};todo=collections.deque((v,v)for v in adj[source])
  while todo:
   target,first=todo.popleft()
   if target in seen:continue
   seen.add(target);route.extend([source,target,first])
   todo.extend((v,first)for v in adj[target]if v not in seen)
 ids=[*range(101,130),*range(140,146)];route_map={(route[i],route[i+1]):route[i+2]for i in range(0,len(route),3)}
 flat=[route_map.get((a,b),255)for a in ids for b in ids];flat += [255]*(len(flat)%2)
 packed=[flat[i]|(flat[i+1]<<8)for i in range(0,len(flat),2)]
 rows.append(('fsRoutes',packed,False))
 notes=[];ctrl=[];windows=[];silence={}
 for n in(119,121,128,129):
  ev=c.decode_sound((H/f'assets/{n}.sound.bin').read_bytes());bounds={0};nn=[]
  for ch,events in ev.items():
   if ch==15:continue
   held={}
   for tick,msg in events:
    k=msg[0]&240;bounds.add(tick)
    if k==144 and msg[2]:assert msg[1]not in held;held[msg[1]]=(tick,msg[2])
    elif k==128 or(k==144 and not msg[2]):
     on,vel=held.pop(msg[1]);nn.append([on,tick,ch,msg[1],vel])
    elif k in(176,192,208,224):ctrl.extend([n,tick,ch,k,msg[1],msg[2]if len(msg)>2 else 0])
   assert not held
  end=max(t for ee in ev.values()for t,msg in ee);bounds.add(end)
  for a,b in zip(sorted(bounds),sorted(bounds)[1:]):
   first=(a+3)//2*2;last=(b-5)//2*2
   if first<=last and not any(ch==9 and on<=first<off for on,off,ch,p,v in nn):windows.extend([n,first,last])
   if n==129 and b-a>200 and not any(on<=a<off for on,off,ch,p,v in nn):silence[n]=(a+2,b-3)
  notes.extend(v for r in sorted(nn)for v in[n,*r])
 rows += [('fsFiniteNotes',notes,False),('fsFiniteControls',ctrl,False),('fsFiniteWindows',windows,False)]
 loops=json.loads((H/'generated/LOOP-TRANSPORTS.json').read_text())['transports'];mapping={151:(941,'home'),152:(942,'contest'),**{r['sound']:(r['module'],f"cue{r['cue']}")for r in loops}}
 priv=(H/'src/full-broker.inc').read_text()+'\n'+(H/'src/full-finite.inc').read_text()
 switch='(switch number '+' '.join(f'({n} (return (ScriptID {m} 0)))'for n,(m,p)in mapping.items())+')'
 ver='(switch number '+' '.join(f'({n} (return (proc{m}_1)))'for n,(m,p)in mapping.items())+')'
 val='(switch number '+' '.join(f'({n} (return (proc{m}_2 rbSound)))'for n,(m,p)in mapping.items())+')'
 tokens={'@TRANSPORT_SWITCH@':switch,'@VERIFY_SWITCH@':ver,'@VALIDATE_SWITCH@':val,'@ROUTE_COUNT@':len(route)//3,'@BRIDGE_COUNT@':len(bridge)//4,'@BRIDGE_CONTROL_COUNT@':len(controls)//5,'@FINITE_NOTE_COUNT@':len(notes)//6,'@FINITE_CONTROL_COUNT@':len(ctrl)//6,'@FINITE_WINDOW_COUNT@':len(windows)//3,'@SPEECH_GAP_FIRST@':silence[129][0],'@SPEECH_GAP_LAST@':silence[129][1]}
 for a,b in tokens.items():priv=priv.replace(a,str(b))
 proc=c.replace_proc(proc,'rbTransport','(procedure (rbTransport) (return (fsTransport rbOwner)))')
 proc=c.replace_proc(proc,'rbStatic','(procedure (rbStatic) (return (and (rbVerify) (pmVerify) (if (fsTransport rbOwner) (fsVerify rbOwner) else 1))))')
 proc=proc.replace('(= rbSound actualSound) (= rbEnabled 1) (= rbDesired 151)', '(= rbSound actualSound) (= rbEnabled 1) (= rbDesired 151) (= fsEnabled 1)',1)
 proc=proc.replace('(= rbResponse cursor) (= rbConsumedResponses', '(= rbThinking 0) (= rbResponse cursor) (= rbConsumedResponses')
 proc=prepend(proc,'rbRequest',''' (if fsEnabled
  (if (== family 152)
   (if (not (and rbActive (not rbExit))) (return 0))
   (if (or (< fsTarget 140) (> fsTarget 145)) (= fsReturnCue fsTarget) (= fsReturnRow fsTargetRow))
   (return (fsRequest (+ 140 rbEncounter) (if rbThinking 5 else rbEncounter) 1)))
  (if (== family 151) (return (fsRequest (if fsReturnCue fsReturnCue else 102) fsReturnRow 2)))
  (return 0))''')
 proc=c.replace_proc(proc,'rbScoreRequest','(procedure (rbScoreRequest cue row reason) (return (fsRequest cue row reason)))')
 proc=prepend(proc,'rbPoll',' (if (and fsEnabled (!= rbMode 4)) (return (fsPoll hi lo domain)))')
 proc=prepend(proc,'rbRestoreBegin',' (if (and fsEnabled (or (== rbMode 1) (== rbMode 2))) (return (fsRestoreBegin actualSound)))')
 proc=prepend(proc,'rbRestoreResume',' (if (and fsEnabled (or (== rbMode 1) rbSavedBridge)) (return (fsRestoreResume domain)))')
 # A04 opening path remains unchanged; only other cues branch to separate tables.
 proc=prepend(proc,'rpRestoreBegin',' (if (== rpCue 128) (return (fsDiscardResponseOnRestore actualSound)))')
 proc=prepend(proc,'rpValidate',' (if (!= rpCue 100) (return (fsFiniteValidate)))')
 proc=prepend(proc,'rpPoll',' (if (!= rpCue 100) (return (fsFinitePoll)))')
 proc=proc.replace('(> (rbSound min?) 1)','(> (rbSound min?) (/ rpEnd 3600))')
 proc=proc.replace('(if (!= rbMode 4) (return 1))','(if (and (!= rbMode 4) (not (or (== fsTarget 119) (== fsTarget 121)))) (return 1))',1)
 proc=prepend(proc,'rbPresentation',''' (if (and (== command 0) (or (== cue 119) (== cue 121)))
  (if (or logicalTick held rbRestoring rbChooser (not rbEnabled) (== rbUnavailable 9)) (return 0))
  (if (not (rbAdvanceGeneration)) (return 0))
  (if (not (rbRetire)) (return 0))
  (= fsTarget cue) (= fsTargetRow 0) (= rbDesired cue)
  (return (fsFiniteStart cue)))''')
 # Catalog size-bound bridges; opening controls/serial retirement are untouched.
 proc=proc.replace('(< i 5) ((++ i)) (if (== [rbBridgeMetadata','(< i '+str(len(bridge)//4)+') ((++ i)) (if (== [rbBridgeMetadata')
 # Split generic mutable/ledger validation from actual selected owner validation.
 old='(not (or (== rbDesired 151) (== rbDesired 152)))'
 proc=proc.replace(old,'(not (or (and (not fsTarget) (== rbDesired 151)) (and fsTarget (== rbDesired (fsNative fsTarget)))))')
 marker=' (if (== rbMode 4) (return (rpValidate)))'
 assert marker in proc
 stale=' (if (or rpPauseSampleValid rpCue rpOffset rpEnd rpHeld rpPause rpRejoin rpPosition rpRestoreCheckpoint rpTerminal (!= rpFrozenPosition -1)) (return 0))'
 if stale not in proc:stale=' (if (or rpCue rpOffset rpEnd rpHeld rpPause rpRejoin rpPosition rpRestoreCheckpoint rpTerminal (!= rpFrozenPosition -1)) (return 0))'
 assert stale in proc
 proc=proc.replace(stale,stale+'\n (if fsEnabled (return (fsState)))',1)
 # Append initial full-score transport metadata without materializing inactive instances.
 local=src[src.index('(local\n')+len('(local\n'):start]
 local=re.sub(r'\s*\[([A-Za-z]\w*) (\d+)\] = \[([^\]]*)\]',lambda m:m.group(0)if m[1]=='rbHighwater'else'',local)
 local=local[:local.rfind(')')]
 local+='\n fsEnabled = 0\n fsCue = 0\n fsTarget = 0\n fsTargetRow = 0\n fsReturnCue = 0\n fsReturnRow = 0\n fsBridgeSource = 0\n fsBridgeTarget = 0\n'
 header=src[:src.index('(local\n')]+'(use \"module994\")\n(use \"module996\")\n(use \"module997\")\n'
 source=header+'(local\n'+g.local(rows)+'\n'+local+'\n)\n'+guard_split(H,'rb',rows)+'\n'+proc+'\n'+priv
 # Broker UI text follows the newly rederived exact guard. Change only its base.
 text=H/'generated/248.text.bin';raw=text.read_bytes();first=raw.count(b'\0')
 labels=json.loads((R:=(H/'recovered')) .joinpath('src/broker-ui-labels.json').read_text())['labels']
 text.write_bytes(raw+b''.join(x.encode()+b'\0'for x in labels))
 source=re.sub(r'\(GetFarText 248 \(\+ \d+ \(- state 2\)\)',f'(GetFarText 248 (+ {first} (- state 2))',source)
 source=source.replace('(if (and (== fsTarget cue) (== fsTargetRow row)) (return 1))','(if (and rbOwner (== fsTarget cue) (== fsTargetRow row)) (return 1))')
 (H/'generated/module943.sc').write_text(source)
 c.dump(H/'generated/FULL-BROKER-TABLES.json',dict(routes=[route[i:i+3]for i in range(0,len(route),3)],finite_notes=len(notes)//6,finite_windows=len(windows)//3,finite_controllers=len(ctrl)//6,speech_gap=silence[129],bridge_count=len(bridge)//4,broker_abi=list(range(40)),native_acceptance=False))
 print('Broker generated;',len(route)//3,'routes;',len(notes)//6,'finite notes')
if __name__=='__main__':main()
