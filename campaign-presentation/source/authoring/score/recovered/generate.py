#!/usr/bin/env python3
"""Re-derive every transport table from exact151/152 encoded events; no composition."""
from pathlib import Path
import json,re,sys,hashlib,struct
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'tools'))
from music_generate import decode_sound

def need(v,msg):
 if not v:raise RuntimeError(msg)
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def manifest(n):
 folder=H/('inputs/bridge-reference/generated' if 148<=n<=154 else 'inputs/music/analysis')
 return next(json.loads(p.read_text())for p in folder.glob('*-manifest.json')if json.loads(p.read_text())['resource_id']==n)
def stream(n):return decode_sound((H/f'inputs/bridge-reference/generated/{n}.sound.bin').read_bytes())
def derive(n):
 m=manifest(n);base=manifest(m['source_resource']);ev=stream(n);ch=[r['channel']for r in base['roles']];notes=[];times={m['loop']['start_tick'],m['loop']['end_tick']};expr=[]
 for c,rows in ev.items():
  if c==15:continue
  active={}
  for i,(t,msg) in enumerate(rows):
   k=msg[0]&240
   if k in(128,144)or(k==176 and msg[1]==11):times.add(t)
   if k==176 and msg[1]==11 and t:expr.append((t,ch.index(c),msg[2]))
   if k==144 and msg[2]:need(msg[1]not in active,'overlap');active[msg[1]]=(t,msg[2],i)
   elif k==128 or(k==144 and not msg[2]):
    need(msg[1]in active,'unbalanced off');on,vel,idx=active.pop(msg[1]);notes.append((c,idx,on,t,msg[1],vel))
  need(not active,'unreleased note')
 notes.sort();expr.sort();windows=[];held=[]
 for a,b in zip(sorted(times),sorted(times)[1:]):
  if a<m['loop']['start_tick']:continue
  first=(a+3)//2*2;last=(b-7)//2*2
  if first>last:continue
  keys=[(ch.index(c),p,v,off)for c,_,on,off,p,v in notes if on<=first<off]
  need(not any(ch[c]==9 for c,_,_,_ in keys),'percussion rejoin')
  windows.append([first,last,b,len(held),len(keys)]);held.extend(x for row in keys for x in row)
 initial=[base['initial_controllers'][str(c)]['cc11']for c in ch];loop=initial[:]
 for t,c,v in expr:loop[c]=v
 def at(c,t,wrapped):
  val=(loop if wrapped else initial)[c]
  for tick,p,v in expr:
   if c==p and tick<=t:val=v
  return val
 ha=[];hb=[]
 for first,last,deadline,offset,count in windows:
  parts=[held[offset+4*i]for i in range(count)]
  ha.append(int(all(at(c,first,False)==at(c,first,True)for c in parts)))
  hb.append(int(all(at(c,first,False)==at(c,first,True)for c in range(8))))
 states=[[r['volume']for r in manifest(i)['roles']]for i in range(140,146)] if n==152 else [[r['volume']for r in base['roles']],[99,83,0,71,73,44,0,59]]
 tables=dict(currentGains=[0]*8,targetGains=[0]*8,historyTableA=ha,historyTableB=hb,midiChannels=ch,mainStateGains=states[0],reducedStateGains=states[-1],midiPrograms=[r['program']for r in base['roles']],midiPans=[r['pan']for r in base['roles']],initialExpression=initial,loopExpression=loop,expressionEvents=[x for row in expr for x in row],keyWindows=[x for row in windows for x in row],heldNotes=held,stateGains=[x for row in states for x in row])
 ref=json.loads((H/f'inputs/bridge-reference/generated/{n}-transport-tables.json').read_text())
 for key,other in [('keyWindows','key_windows'),('heldNotes','held_words'),('historyTableA','history_a'),('historyTableB','history_b')]:
  expected=[x for row in ref[other]for x in row]if other=='key_windows'else ref[other]
  
  if key=='heldNotes':
   for w in windows:
    off,cnt=w[3:];need(sorted(tuple(tables[key][k:k+4])for k in range(off,off+cnt*4,4))==sorted(tuple(expected[k:k+4])for k in range(off,off+cnt*4,4)),'accepted held set mismatch')
  else:need(tables[key]==expected,'accepted table mismatch '+key)
 for gate in m['gates']:
  need(gate['dispatch_first']>=gate['keyoff_tick']+2,'drainage')
  need(gate['dispatch_last']<=gate['next_event_tick']-3,'attack clearance')
  need(not any(on<=t<off for _,_,on,off,_,_ in notes for t in range(gate['dispatch_first'],gate['dispatch_last']+1)),'held key in gate')
 return m,tables,notes

def guards(prefix,textid,rows):
 chunks=[];access=[]
 for name,vals,mutable in rows:
  if mutable:continue
  first=len(chunks)
  for i in range(0,len(vals),20):chunks.append(''.join(f'{v&65535:05d} 'for v in vals[i:i+20]+[0]*(20-len(vals[i:i+20]))))
  access.append((name,len(vals),first))
 (H/f'generated/{textid}.text.bin').write_bytes(b''.join(x.encode()+b'\0'for x in chunks))
 lines=[f'(procedure ({prefix}Verify &tmp index slot word digit value i)',f'(for ((= i 0)) (< i 64) ((++ i)) (= [{prefix}Buffer i] 0))']
 for name,count,first in access:
  lines += [f'(for ((= index 0)) (< index {count}) ((++ index))',f'(if (== (mod index 20) 0) (GetFarText {textid} (+ {first} (/ index 20)) @{prefix}Buffer))','(= slot (mod index 20)) (= value 0)','(for ((= i 0)) (< i 5) ((++ i))',f'(= word [{prefix}Buffer (+ (* slot 3) (/ i 2))])','(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))','(if (or (< digit 0) (> digit 9)) (return 0))','(= value (+ (* value 10) digit)))',f'(if (!= (>> [{prefix}Buffer (+ (* slot 3) 2)] 8) 32) (return 0))',f'(if (!= [{name} index] value) (return 0)))']
 lines+=['(return 1))'];return '\n'.join(lines)
def local(rows):
 return '\n'.join(f' [{n} {len(v)}] = [ '+' '.join(str(x)for x in v)+' ]'for n,v,_ in rows)

def transport(n,module,textid,prefix):
 m,t,notes=derive(n);rows=[(k,v,k in('currentGains','targetGains'))for k,v in t.items()];maxstate=5 if n==152 else 1
 # Accepted43-method port. Every instruction remains ordinary SCI source. New
 # timing constants and all locals are independently derived from new resource.
 s=(H/'inputs/accepted-v4/generated/module940.sc').read_text();body=s[s.index('(instance contestTransport'):]
 body=body.replace('contestTransport',prefix+'ReadyTransport').replace('vcVerifyTables',prefix+'Verify')
 for old,new in {140:n,3972:m['loop']['end_tick'],3848:m['loop']['end_tick']-124,3964:m['loop']['end_tick']-8,105:len(t['keyWindows'])//5}.items():
  body=re.sub(r'\b(ldi|pushi) '+str(old)+r'(?=\s*(?:;|\n))',lambda match:match[1]+' '+str(new),body)
 body=body.replace('(> state 5)',f'(> state {maxstate})')
 a=body.index('(method (start ');b=body.index('(method (setMuted ',a)
 start=body[a:b].replace('lsp 2\n            ldi 5\n            gt?',f'lsp 2\n            ldi {maxstate}\n            gt?')
 body=body[:a]+start+body[b:]
 valid=[f'(procedure ({prefix}Validate sound &tmp i value wanted)',f'(if (not ({prefix}Verify)) (return 0))',f'(if (or (not (IsObject sound)) (!= (sound number?) {n})) (return 0))',f'(if (or (!= ({prefix}ReadyTransport musicBed?) sound) (!= ({prefix}ReadyTransport ownedBed?) sound)) (return 0))',f'(= wanted ({prefix}ReadyTransport nextRequestedState?))',f'(if (or (< wanted 0) (> wanted {maxstate})) (return 0))']
 bools='musicRunning musicPaused ownedPauseHeld pausePhaseKnown pausedCheckpoint recoveryPhaseKnown musicMuted loopHasWrapped saveGuard remapGuard remapDrain positionUncertain recoveryWrapped'.split()
 ranges={'wholeGain':(0,100),'desiredWholeGain':(0,100),'savedWholeGain':(0,100),'transportMode':(0,9),'resumeMode':(0,9),'settledState':(-1,maxstate),'musicPosition':(0,m['loop']['end_tick']-1),'pausedPosition':(0,m['loop']['end_tick']-1),'previousPosition':(-1,m['loop']['end_tick']-1),'recoveryLastPosition':(-1,m['loop']['end_tick']-1),'rejoinWindow':(-1,len(t['keyWindows'])//5-1),'historyWindow':(-1,len(t['keyWindows'])//5-1),'lastBatchKeys':(0,32),'recoverySamples':(0,32767),'recoveryReason':(0,10),'historyRoute':(0,10)}
 for name in 'requestRevision saveRevision previousGeneration loopEpoch rejoinEpoch lifecycleGeneration recoveryGeneration gainRefreshes historyEpisodes'.split():ranges[name]=(0,29999)
 ranges['rejoinAttempts']=(0,32)
 for name in bools:ranges[name]=(0,1)
 for name,(lo,hi)in ranges.items():valid += [f'(= value ({prefix}ReadyTransport {name}?))',f'(if (or (< value {lo}) (> value {hi})) (return 0))']
 valid += [f'(if (or (!= ({prefix}ReadyTransport musicMuted?) (if ({prefix}ReadyTransport musicMuted?) 1 else 0)) (< ({prefix}ReadyTransport transportMode?) 1)) (return 0))',f'(if (and ({prefix}ReadyTransport recoveryBed?) (!= ({prefix}ReadyTransport recoveryBed?) sound)) (return 0))',f'(if (!= ({prefix}ReadyTransport musicRunning?) 1) (return 0))',f'(if (and ({prefix}ReadyTransport pausedCheckpoint?) (not ({prefix}ReadyTransport saveGuard?))) (return 0))',f'(if (and ({prefix}ReadyTransport saveGuard?) (not ({prefix}ReadyTransport ownedPauseHeld?))) (return 0))','(for ((= i 0)) (< i 8) ((++ i))','(if (or (< [currentGains i] 0) (> [currentGains i] 127)) (return 0))','(if (!= [targetGains i] [stateGains (+ (* wanted 8) i)]) (return 0)))','(return 1))']
 source=';;; Sierra Script 1.0 - (do not remove this comment)\n; New transition-ready arrangement transport; source/emitted-only candidate.\n'+f'(script# {module})\n(use "module981")\n(public {prefix}ReadyTransport 0 {prefix}Verify 1 {prefix}Validate 2)\n(local\n'+local(rows)+f'\n [{prefix}Buffer 64]\n)\n'+guards(prefix,textid,rows)+'\n'+'\n'.join(valid)+'\n'+body
 (H/f'generated/module{module}.sc').write_text(source)
 dump(H/f'generated/{n}-tables.json',dict(resource=n,module=module,text=textid,loop=m['loop'],tables=t,notes=notes,gates=m['gates'],state_count=maxstate+1,static_validation='fresh exact text equality',release_edits=m['edits']))
 return {prefix+'Verify':1,prefix+'Validate':2}

def allocation_scan():
 registry=json.loads((H/'inputs/ADDITIVE-ABI-RESERVATIONS.json').read_text())
 reserved=registry['responsive_music_candidate'];scripts=[941,942,943];texts=[245,246,247]
 need(sorted(reserved['scripts'].values())==scripts and reserved['static_texts']==texts,'Coordinator allocation reservation changed')
 maps=[]
 for p in sorted((H/'inputs').rglob('*.map')):
  blob=p.read_bytes();heads=[];at=0
  while True:
   need(at+3<=len(blob),'Truncated typed map header')
   typ,off=struct.unpack_from('<BH',blob,at);at+=3;heads.append((typ,off))
   if typ==255:break
  typed={}
  for (typ,a),(_,b)in zip(heads,heads[1:]):
   need(at<=a<=b<=len(blob)and(b-a)%5==0,'Invalid SCI1.1 typed map span')
   typed[typ&127]=[struct.unpack_from('<H',blob,k)[0]for k in range(a,b,5)]
  need(not(set(scripts)&set(typed.get(2,[]))),'Occupied proposed Script resource')
  need(not(set(texts)&set(typed.get(3,[]))),'Occupied proposed Text resource')
  maps.append(dict(path=str(p.relative_to(H)),sha256=hashlib.sha256(blob).hexdigest(),typed_resources=typed))
 source_scripts=set()
 for p in (H/'inputs').rglob('*.sc'):
  source_scripts.update(int(n)for n in re.findall(r'\(script#\s+(\d+)\)',p.read_text()))
 need(not(set(scripts)&source_scripts),'Proposed script already defined in a pinned host source')
 need(bool(maps),'No typed maps scanned')
 dump(H/'evidence/allocation-scan.json',dict(status='PASS_FRESH_TYPED_MAP_AND_REGISTRY_SCAN',scripts=scripts,text=texts,new_species=0,new_selectors=0,maps=maps,source_script_ids=sorted(source_scripts),registry_sha256=hashlib.sha256((H/'inputs/ADDITIVE-ABI-RESERVATIONS.json').read_bytes()).hexdigest(),native_acceptance=False,scope='Pinned retained/current host universe; final common host requires a new explicit scan'))

def main():
 need(not sys.flags.optimize,'optimized Python forbidden');(H/'generated').mkdir(exist_ok=True);(H/'evidence').mkdir(exist_ok=True);allocation_scan()
 apis={941:transport(151,941,245,'home'),942:transport(152,942,246,'contest')}
 gates=[];bridge=[];controllers=[]
 for n in (151,152):
  for gate in manifest(n)['gates']:gates.extend([n,gate['dispatch_first'],gate['dispatch_last'],gate['bridge_resource']])
 for n in(148,149,150,153,154):
  m=manifest(n);bridge.extend([n,m['end_tick'],m['last_keyoff'],m['first_attack']])
  for c,events in stream(n).items():
   if c==15:continue
   for tick,msg in events:
    if tick:continue
    if msg[0]&240 in (176,192):controllers.extend([n,c,msg[0]&240,msg[1],msg[2]if len(msg)>2 else 0])
 rows=[('rbGates',gates,False),('rbBridgeMetadata',bridge,False),('rbBridgeControllers',controllers,False)]
 proc=(H/'src/broker-procedures.inc').read_text();names=re.findall(r'\(procedure \((\w+)',proc)
 names=['rbVerify']+names;need(len(names)==len(set(names)),'duplicate exports')
 apis[943]={name:i for i,name in enumerate(names)}
 source=';;; Sierra Script 1.0 - (do not remove this comment)\n(script# 943)\n(use "module941")\n(use "module942")\n(public '+' '.join(f'{name} {i}'for i,name in enumerate(names))+')\n(local\n'+local(rows)+'\n [rbBuffer 64]\n'+(H/'src/broker-locals.inc').read_text()+'\n)\n'+guards('rb',247,rows)+'\n'+proc
 source=source.replace('@GATE_COUNT@',str(len(gates)//4)).replace('@BRIDGE_CONTROLLERS@',str(len(controllers)//5))
 ui=json.loads((H/'src/broker-ui-labels.json').read_text());need(ui['first_state']==2 and len(ui['labels'])==6,'UI state label contract')
 guard_path=H/'generated/247.text.bin';guard_bytes=guard_path.read_bytes();first_label=guard_bytes.count(b'\0')
 for label in ui['labels']:need(0<len(label.encode('ascii'))<128 and '\0'not in label,'UI label buffer bound')
 guard_path.write_bytes(guard_bytes+b''.join(label.encode('ascii')+b'\0'for label in ui['labels']))
 source=source.replace('@UI_TEXT_FIRST@',str(first_label))
 (H/'generated/module943.sc').write_text(source)
 dump(H/'generated/api.json',apis)
 dump(H/'generated/broker-tables.json',dict(gates=gates,bridge_metadata=bridge,controllers=controllers,native_tested=False,listening_accepted=False))
 for n in range(148,155):(H/f'generated/{n}.sound.bin').write_bytes((H/f'inputs/bridge-reference/generated/{n}.sound.bin').read_bytes())
 print('Derived941/942 transports and943 broker with exact fresh245/246/247 guards')
if __name__=='__main__':main()
