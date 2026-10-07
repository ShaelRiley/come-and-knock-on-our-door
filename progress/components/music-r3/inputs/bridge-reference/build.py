#!/usr/bin/env python3
"""Deterministic new bridge authoring and actual-source phrase audit; no live writes."""
from pathlib import Path
import sys, json, hashlib, struct, math, collections
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
import generate as g
TICK=16667; PPQ=480

def check(ok, why):
    if not ok: raise RuntimeError(why)
def sha(data):return hashlib.sha256(data).hexdigest()
def dump(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def manifest(n):
    name={102:'MUS02_HOUSE_LIVING',140:'MUS11_VERBAL_COMPETITIONS_BASE'}[n]
    return json.loads((ROOT/'inputs/music'/f'{name}-manifest.json').read_text())
def stream(n):return g.decode_sound((ROOT/'inputs/music'/f'{n}.sound.bin').read_bytes())
def swing(x,r):
    b=math.floor(x); f=x-b
    return b+(f*r/.5 if f<=.5 else r+(f-.5)*(1-r)/.5)
def notes_of(s):
    active={}; out=[]
    for ch,rows in s.items():
        if ch==15:continue
        for t,msg in rows:
            kind=msg[0]&240; key=(ch,msg[1])
            if kind==144 and msg[2]:
                check(key not in active,'Overlapping same-pitch note')
                active[key]=(t,msg[2])
            elif kind==128 or (kind==144 and not msg[2]):
                check(key in active,'Unpaired note-off')
                on,v=active.pop(key);out.append(dict(channel=ch,on=on,off=t,pitch=msg[1],velocity=v))
    check(not active,'Hanging keys')
    return sorted(out,key=lambda n:(n['on'],n['channel'],n['pitch']))
def gaps(s,start,end):
    notes=notes_of(s);ev=collections.defaultdict(int)
    for n in notes:ev[n['on']]+=1;ev[n['off']]-=1
    out=[]; held=0; last=0
    for t in sorted(ev):
        if not held and t>last and t>start:out.append([max(start,last),t])
        held+=ev[t];check(held>=0,'Negative held count');last=t
    if last<end:out.append([last,end])
    return out

def read_map(p):
    b=p.read_bytes();headers=[];i=0
    while True:
        typ=b[i];off=int.from_bytes(b[i+1:i+3],'little');headers.append((typ,off));i+=3
        if typ==255:break
    out=[]
    for (typ,a),(_,bnd) in zip(headers,headers[1:]):
        check((bnd-a)%5==0,'Not SCI1.1 map')
        for j in range(a,bnd,5):out.append((typ&127,int.from_bytes(b[j:j+2],'little')))
    return out

def allocate():
    evidence=[]; sounds=set()
    for p in sorted((ROOT/'inputs/maps').glob('*')):
        rows=read_map(p);nums=sorted(n for t,n in rows if t==4);sounds.update(nums)
        evidence.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()),sound_ids=nums,script_ids=sorted(n for t,n in rows if t==2)))
    fullbank=set(range(100,130))|set(range(140,148)); sounds.update(fullbank)
    ids=[148,149,150];check(not set(ids)&sounds,'Bridge Sound collision')
    dump(ROOT/'ALLOCATION.json',dict(status='LOCAL_CANDIDATE_SOUND_ALLOCATIONS_ONLY',resource_type={'name':'Sound','type_id':4},sound_ids=ids,script_ids=[],text_ids=[],new_species=0,new_selectors=0,checked_maps=evidence,preserved_full_v4_sound_ids=sorted(fullbank),retained_registry='inputs/registry/retained-registry-subset.json',limits='No complete historical registry survives. Coordinator must reserve these typed Sound IDs before a future coherent merge. Script940 is a separate namespace. No live map is changed.'))

def make_bridge(spec):
    src=manifest(spec.get('fragment_source_resource',spec['source_family']));roles=[dict(r) for r in src['roles']]
    # Keep the established logical eight-role bank, with only bass/keys/one lead/kit active.
    active_channels={0,1,spec['source_fragment']['channel'],9}
    for r in roles:
        if r['channel'] not in active_channels:r['volume']=0
        if r['channel']==4:r['program']=59
    origin=round(.2*spec['tempo_map'][0][1]/60*PPQ)/PPQ
    at=lambda b:origin+swing(b,spec['swing'])
    notes=[]
    def add(b,d,ch,p,v,provenance):
        check(b>=0 and b+d<=spec['beats'],'Bridge note exceeds phrase')
        notes.append(dict(beat=at(b),duration=at(b+d)-at(b),unswung_beat=b,unswung_duration=d,channel=ch,pitch=p,velocity=round(v),provenance=provenance))
    fragment=spec['source_fragment']
    for sid in fragment['source_ids']:
        options=[n for n in src['notes'] if n.get('source',{} ) and n['source']['source_note_id']==sid]
        n=min(options,key=lambda n:n['unswung_beat'])
        scale=fragment['time_scale'];b=(n['unswung_beat']-fragment['offset'])*scale;d=n['unswung_duration']*scale
        # For action source use actual emitted articulation, not its stale unswung-duration field.
        if spec['source_family']==140:d=n['duration']*scale
        add(b,d,fragment['channel'],n['pitch'],n['velocity']*fragment['velocity_scale'],dict(kind='explicit_source_fragment',manifest=fragment['manifest'],source_note=n,uniform_time_scale=scale,note_pitch_unchanged=True,source_resource_unchanged=True))
    for b,d,p,v in spec['bass']:add(b,d,0,p,v,dict(kind='new_authored',basis='Existing root/fifth broad-pulse bass vocabulary and explicit source harmony'))
    for b,d,h,v in spec['comp']:
        for p in spec['harmony'][h][3]:add(b,d,1,p,v,dict(kind='new_authored',basis='Exact source-family two-note shell',harmony=spec['harmony'][h][1]))
    for b,p,v in spec['kit']:add(b,.09,9,p,v,dict(kind='new_authored',basis='Existing restrained closed-hat/cross-stick/kick vocabulary; no percussion result accent'))
    ev=[]
    for r in roles:
        ch=r['channel'];ev.append((0,-10,bytes((192|ch,r['program']))))
        for cc,val in [(7,r['volume']),(10,r['pan']),(11,100 if ch in (3,4) else 127),(64,0),(1,0)]:ev.append((0,-9,bytes((176|ch,cc,val))))
        ev.append((0,-8,bytes((224|ch,0,64))))
    for n in notes:
        ev.extend([(round(n['beat']*PPQ),2,bytes((144|n['channel'],n['pitch'],n['velocity']))),(round((n['beat']+n['duration'])*PPQ),0,bytes((128|n['channel'],n['pitch'],0)))])
    for beat,bpm in spec['tempo_map']:ev.append((round(at(beat)*PPQ) if beat else 0,-30,b'\xff\x51\x03'+round(60000000/bpm).to_bytes(3,'big')))
    for beat,label,*_ in spec['harmony']:
        text=label.encode();ev.append((round(at(beat)*PPQ),-20,b'\xff\x06'+g.vlq(len(text))+text))
    ending=round(at(spec['beats'])*PPQ);ev.extend([(0,-29,b'\xff\x58\x04\x04\x02\x18\x08'),(ending,99,b'\xff\x2f\0')])
    body=bytearray();last=0
    for t,order,msg in sorted(ev,key=lambda e:(e[0],e[1])):body+=g.vlq(t-last)+msg;last=t
    midi=b'MThd'+struct.pack('>IHHH',6,0,1,PPQ)+b'MTrk'+struct.pack('>I',len(body))+body
    converted,timing=g.convert_smf(midi);streams=collections.defaultdict(list)
    for t,msg in converted:streams[msg[0]&15].append((t,msg))
    # Obtain exact EOT tempo integration without inferring it from last note-off.
    ppq,parsed=g.parse_smf(midi);from fractions import Fraction
    tempo=500000;prior=0;elapsed=Fraction(0)
    for t,_,msg in parsed:
        elapsed+=Fraction((t-prior)*tempo,ppq);prior=t
        if msg[:2]==b'\xff\x51':tempo=int.from_bytes(msg[2:],'big')
    end=round(elapsed/TICK)
    streams[15]=[(0,b'\xcf\0'),(6,b'\xcf\1'),(12,b'\xcf\2'),(end,b'\xbf\x50\0')]
    payload=g.sound_resource(dict(streams),{r['channel']:r['voices'] for r in roles});decoded=g.decode_sound(payload);native_notes=notes_of(decoded)
    events=sorted([(n['on'],1,n['channel'])for n in native_notes]+[(n['off'],-1,n['channel'])for n in native_notes],key=lambda e:(e[0],e[1]));active=collections.Counter();peak=0;per=collections.Counter()
    for _,d,ch in events:active[ch]+=d;peak=max(peak,sum(active.values()));per[ch]=max(per[ch],active[ch])
    check(peak<=18,'Voice budget');check(all(per[r['channel']]<=r['voices']for r in roles),'Role voice budget')
    check(max(n['off'] for n in native_notes)<end,'No natural ending')
    num=spec['resource_id'];name=spec['name']
    for rel,data in [(f'generated/{name}.mid',midi),(f'generated/{num}.sound.bin',payload),(f'generated/sound.{num}',b'\x84\0'+payload)]: (ROOT/rel).write_bytes(data)
    out=dict(spec,notes=notes,roles=roles,native_notes=native_notes,loop=None,one_shot=True,first_attack=min(n['on']for n in native_notes),last_keyoff=max(n['off']for n in native_notes),end_tick=end,duration_seconds=end*TICK/1e6,max_held_notes=peak,per_channel_peak=dict(per),controller_guard=[6,8],midi_sha256=sha(midi),native_sha256=sha(payload),maximum_quantization_error_us=max(r['error_us']for r in timing),native_runtime_tested=False,listening_accepted=False,release_tail_silence_proven=False)
    dump(ROOT/f'generated/{name}-manifest.json',out)
    dump(ROOT/f'generated/{num}-native-events.json',{str(ch):[dict(tick=t,message=msg.hex())for t,msg in rows]for ch,rows in decoded.items()})
    return out

def derive_gates():
    all_reports=[]
    for num in (102,140):
        m=manifest(num);s=stream(num);windows=gaps(s,m['loop']['start_tick'],m['loop']['end_tick']);chosen=[];origin=m['notes'][0]['beat']-swing(m['notes'][0]['unswung_beat'],m['swing_offbeat_fraction'])
        def beat(t):return ((t*TICK/1e6-.2)*m['bpm']/60)
        for a,b in windows:
            if b-a<8:continue
            u=beat(b)
            rationale=None;bridge=None
            if num==102:
                if any(abs(u-x)<.08 for x in [26,58,90,122]):bridge=148;rationale='Completed HOME C tag over Am7, before its actual Ab7-Gm7-C7 closing clause; new bridge condenses that same clause'
                elif abs(u-130)<.08:bridge=148;rationale='Composed F turnaround broad-pulse breath; Am7 is its diatonic iii, followed by source closing clause'
            else:
                if any(abs(u-x)<.08 for x in [8,24,40,56,104,120]):bridge=149;rationale='Actual end of Em7 call or G7 answer before the next source harmonic clause; shared-tone/local-dominant Cmaj7 entry then source C7'
                elif any(abs(u-x)<.08 for x in [32,64,88,96,128,132]):bridge=150;rationale='Actual C7 turnaround, middle Bb9sus4 release, or full-cycle Fm7 release; dominant connector into Fmajor'
            if bridge:
                chosen.append(dict(keyoff_tick=a,next_event_tick=b,dispatch_first=a+2,dispatch_last=b-3,bridge_resource=bridge,source_beat_at_next_event=round(u,6),rationale=rationale,held_keys_at_dispatch=0,release_reverb_silence_proven=False))
        check(chosen,'No gates');start=m['loop']['start_tick'];end=m['loop']['end_tick'];cycle=end-start
        # Scheduled poll interval<=2ticks; one-tick conservative bound beyond aperture first.
        starts=[r['dispatch_first']for r in chosen];intervals=[y-x for x,y in zip(starts,starts[1:])]+[starts[0]+cycle-starts[-1]]
        maxwait=max(intervals)+2
        all_reports.append(dict(source=num,target=140 if num==102 else 102,loop=m['loop'],all_key_gaps=windows,gates=chosen,max_inter_gate_ticks=max(intervals),worst_case_wait_ticks=maxwait,worst_case_wait_seconds=maxwait*TICK/1e6,poll_contract_max_ticks=2,native_poll_guarantee_proven=False,responsive_shipping_gate=False,limitation='These immutable arrangements do not support a proven sub-5-second all-key-clear handoff. Narrower one/two-tick gaps are rejected; no note is truncated.'))
    dump(ROOT/'generated/phrase-gates.json',all_reports)
    return all_reports

def main():
    check(not sys.flags.optimize,'Optimized Python forbidden')
    for name in ('generated','evidence'): (ROOT/name).mkdir(exist_ok=True)
    allocate();spec=json.loads((ROOT/'src/bridge-score.json').read_text());bridges=[make_bridge(b)for b in spec['bridges']];gates=derive_gates()
    summary=[]
    for row in gates:
        durations=[b['duration_seconds']for b in bridges if b['source_family']==row['source']]
        summary.append(dict(source=row['source'],target=row['target'],worst_wait_seconds=row['worst_case_wait_seconds'],max_bridge_seconds=max(durations),target_authored_startup_seconds=.200004,worst_request_to_target_first_attack_seconds=row['worst_case_wait_seconds']+max(durations)+.200004))
    dump(ROOT/'generated/latency.json',dict(status='BOUNDED_CANDIDATE_NOT_RESPONSIVE_SHIPPING_SOLUTION',rows=summary,assumptions=['Active playback, not paused/muted/chooser/restore','Current generation stays unchanged','Host frame polling no slower than2 native ticks','Native atomic retire/start and release tails remain unproved']))
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
