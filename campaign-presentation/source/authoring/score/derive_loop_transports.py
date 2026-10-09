#!/usr/bin/env python3
"""Derive transport tables from the exact approved musical event streams."""
from pathlib import Path
import hashlib,importlib.util,json,sys,shutil
H=Path(__file__).resolve().parent;R=H/'recovered'
sys.path.insert(0,str(R/'tools'))
from music_generate import decode_sound
spec=importlib.util.spec_from_file_location('r3_generator',R/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
LOOPS=[101,103,*range(105,119),120]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def derive(n):
 m=g.manifest(n);ev=decode_sound((H/f'assets/{n}.sound.bin').read_bytes());ch=[r['channel']for r in m['roles']]
 assert len(ch)==8
 notes=[];times={m['loop']['start_tick'],m['loop']['end_tick']};expr=[]
 for c,rows in ev.items():
  if c==15:continue
  active={}
  for idx,(tick,msg)in enumerate(rows):
   k=msg[0]&240
   if k in(128,144)or(k==176 and msg[1]==11):times.add(tick)
   if k==176 and msg[1]==11 and tick:expr.append((tick,ch.index(c),msg[2]))
   if k==144 and msg[2]:assert msg[1]not in active;active[msg[1]]=(tick,msg[2],idx)
   elif k==128 or(k==144 and not msg[2]):
    assert msg[1]in active;on,vel,idx=active.pop(msg[1]);notes.append((c,idx,on,tick,msg[1],vel))
  assert not active
 notes.sort();expr.sort();windows=[];held=[]
 for a,b in zip(sorted(times),sorted(times)[1:]):
  if a<m['loop']['start_tick']:continue
  first=(a+3)//2*2;last=(b-7)//2*2
  if first>last:continue
  keys=[(ch.index(c),p,v,off)for c,_,on,off,p,v in notes if on<=first<off]
  if any(ch[c]==9 for c,_,_,_ in keys):continue
  windows.append([first,last,b,len(held),len(keys)]);held.extend(x for row in keys for x in row)
 initial=[m['initial_controllers'][str(c)]['cc11']for c in ch];loop=initial[:]
 for tick,c,val in expr:loop[c]=val
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
 main=[r['volume']for r in m['roles']]
 # The accepted HOME reduced-row balance is applied role-wise, retaining each
 # cue's actual instrumentation, expression history and one parser/clock.
 home=[r['volume']for r in g.manifest(102)['roles']];reduced_ref=[99,83,0,71,73,44,0,59]
 reduced=[min(127,round(v*r/b))if b else 0 for v,r,b in zip(main,reduced_ref,home)]
 t=dict(currentGains=[0]*8,targetGains=[0]*8,historyTableA=ha,historyTableB=hb,midiChannels=ch,mainStateGains=main,reducedStateGains=reduced,midiPrograms=[r['program']for r in m['roles']],midiPans=[r['pan']for r in m['roles']],initialExpression=initial,loopExpression=loop,expressionEvents=[x for row in expr for x in row],keyWindows=[x for row in windows for x in row],heldNotes=held,stateGains=main+reduced)
 # This initial transport edition uses unmodified originals. Transition gating
 # is independently source-derived and may not assume all empty-key gaps fit.
 m=dict(m,source_resource=n,edits=[],gates=[])
 return m,t,notes

def main():
 old=g.derive;g.derive=derive
 rows=[]
 for i,n in enumerate(LOOPS):
  module=950+i;guard=260+i;prefix=f'cue{n}'
  g.transport(n,module,guard,prefix)
  for name in(f'module{module}.sc',f'{guard}.text.bin',f'{n}-tables.json'):
   shutil.copy2(R/'generated'/name,H/'generated'/name)
  source=H/f'generated/module{module}.sc';text=source.read_text();count=len(derive(n)[1]['expressionEvents'])//3
  text=text.replace('label_0a83: lst 1\n            ldi 48',f'label_0a83: lst 1\n            ldi {count}')
  source.write_text(text)
  rows.append(dict(cue=n,aliases=[101,104]if n==101 else[n],sound=n,module=module,guard=guard,sha256=sha(H/f'assets/{n}.sound.bin'),table_sha256=sha(H/f'generated/{n}-tables.json'),full_gain=derive(n)[1]['mainStateGains'],reduced_gain=derive(n)[1]['reducedStateGains']))
 dump(H/'generated/LOOP-TRANSPORTS.json',dict(schema=1,transports=rows,composition_edits=False,reduced_gain_status='Role-wise accepted HOME reduction balance; final composed listening gate remains required',native_acceptance=False))
 print('Derived',len(rows),'independent local-table transports, no musical bytes changed')
if __name__=='__main__':main()
