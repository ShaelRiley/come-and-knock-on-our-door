#!/usr/bin/env python3
"""Author two separately allocated transition-ready arrangements with explicit edits."""
from pathlib import Path
import sys,json,struct,collections,copy
sys.dont_write_bytecode=True
import build as b
g=b.g;ROOT=b.ROOT;PPQ=480;TICK=16667

def smf(events,ppq):
    body=bytearray();prev=0
    for t,order,msg in sorted(events,key=lambda e:(e[0],e[1])):
        if msg[0]==255:msg=msg[:2]+g.vlq(len(msg)-2)+msg[2:]
        body+=g.vlq(t-prev)+msg;prev=t
    return b'MThd'+struct.pack('>IHHH',6,0,1,ppq)+b'MTrk'+struct.pack('>I',len(body))+body

def make(spec):
    m=b.manifest(spec['source_resource']);raw=(ROOT/'inputs/music'/Path(m['midi_path']).name).read_bytes();ppq,es=g.parse_smf(raw)
    source_notes=b.notes_of(b.stream(spec['source_resource']))
    origin=round(.2*m['bpm']/60*ppq);boundaries=[origin+round(x*ppq)for x in spec['boundaries']]
    ev=[list(x)for x in es];held={};edits=[]
    for i,(t,order,msg) in enumerate(es):
        kind=msg[0]&240;ch=msg[0]&15
        if msg[0]>=240:continue
        key=(ch,msg[1])
        if kind==144 and msg[2]:held[key]=i
        elif kind==128 or (kind==144 and not msg[2]):
            j=held.pop(key);on=es[j][0];off=t;new_on=on;new_off=off;why=[]
            boundary=next((x for x in boundaries if on<x),None)
            if boundary:
                cutoff=boundary-round(spec['breath_beats']*ppq)
                if new_off>cutoff:
                    new_off=cutoff;why.append('New phrase-ending release; existing source remains unchanged')
                b.check(new_off>new_on,'Breath would erase a note')
            ev[j][0]=new_on;ev[i][0]=new_off
            if new_on!=on or new_off!=off:edits.append(dict(channel=ch,pitch=msg[1],velocity=es[j][2][2],original_on_smf=on,original_off_smf=off,new_on_smf=new_on,new_off_smf=new_off,phrase_boundary_smf=boundary,reason=why))
    b.check(not held,'Source note imbalance')
    # Stable tie order: all note-offs before new attacks at the same tick.
    for e in ev:
        msg=e[2]
        if msg[0]<240:e[1]=-1 if msg[0]&240==128 else 1 if msg[0]&240==144 else 0
    midi=smf(ev,ppq);converted,timing=g.convert_smf(midi);streams=collections.defaultdict(list)
    for t,msg in converted:streams[msg[0]&15].append((t,msg))
    controls=copy.deepcopy(b.stream(spec['source_resource'])[15]);notes=b.notes_of(dict(streams));allgaps=b.gaps(dict(streams),12,m['loop']['end_tick']);gates=[]
    for idx,beat in enumerate(spec['boundaries']):
        from fractions import Fraction
        boundary_tick=round(Fraction(origin+round(beat*ppq),ppq)*round(60000000/m['bpm'])/TICK)
        # Last exact boundary EOT has no note-on; others share source next attack.
        gap=next((r for r in allgaps if r[0]<boundary_tick<=r[1]),None)
        b.check(gap and gap[1]-gap[0]>=8,f'Insufficient native phrase gap at {beat}: {gap}')
        first=gap[0]+2;last=boundary_tick-3;b.check(last-first>=2,'Insufficient host aperture')
        if spec['source_resource']==102:
            bridge=148 if beat%32 in (8,24) or beat==132 else 153
            harmonic='HOME eight-beat clause; Am7/deceptive E7→Am7' if bridge==148 else 'HOME Gm11 or closing C7; expand the source ii–V cadence'
        else:
            if beat==78:bridge=154;harmonic='Eb/G ending shares G/Bb with Gm7; continue ii–V into F'
            elif beat in (72,84,88,96,132) or beat%32==0:bridge=150;harmonic='Source C7/C7(b9), Bb9sus4, or Fm7 turnaround connects through C7'
            elif beat%32==16.5:bridge=150;harmonic='Complete Cmaj9 terminal flourish and its next Fm7 tonic arrival; C7 redirects the new breath toward Fmajor'
            else:bridge=149;harmonic='Em7 upper structure or G7 local dominant receives Cmaj7→C7'
        gate=dict(boundary_beat=beat,keyoff_tick=gap[0],next_event_tick=boundary_tick,dispatch_first=first,dispatch_last=last,bridge_resource=bridge,rationale=harmonic,held_keys_at_dispatch=0,release_reverb_silence_proven=False,cue=20+idx)
        gates.append(gate);controls.append((first,bytes((207,20+idx))))
    streams[15]=sorted(controls,key=lambda e:e[0]);payload=g.sound_resource(dict(streams),{r['channel']:r['voices']for r in m['roles']});decoded=g.decode_sound(payload);newnotes=b.notes_of(decoded)
    b.check(len(source_notes)==len(newnotes),'New arrangement dropped a source note')
    identity=lambda ns:collections.Counter((n['channel'],n['pitch'],n['velocity'])for n in ns)
    b.check(identity(source_notes)==identity(newnotes),'Source note identity changed')
    num=spec['resource_id'];name=spec['name']
    (ROOT/f'generated/{name}.mid').write_bytes(midi);(ROOT/f'generated/{num}.sound.bin').write_bytes(payload);(ROOT/f'generated/sound.{num}').write_bytes(b'\x84\0'+payload)
    starts=[r['dispatch_first']for r in gates];cycle=m['loop']['end_tick']-12;intervals=[y-x for x,y in zip(starts,starts[1:])]+[starts[0]+cycle-starts[-1]];wait=max(intervals)+2
    result=dict(spec,roles=m['roles'],loop=m['loop'],source_manifest=Path(m['midi_path']).stem+'-manifest.json',notes=newnotes,note_count=len(newnotes),edited_note_count=len(edits),edits=edits,gates=gates,first_attack=min(n['on']for n in newnotes),native_sha256=b.sha(payload),midi_sha256=b.sha(midi),duration_seconds=m['duration_seconds'],worst_wait_ticks=wait,worst_wait_seconds=wait*TICK/1e6,poll_max_ticks=2,original_resources_unchanged=True,native_runtime_tested=False,human_listening_accepted=False,live_permission=False)
    b.dump(ROOT/f'generated/{name}-manifest.json',result)
    b.dump(ROOT/f'generated/{num}-native-events.json',{str(ch):[dict(tick=t,message=msg.hex())for t,msg in rows]for ch,rows in decoded.items()})
    return result

def add_bridges():
    p=ROOT/'src/bridge-score.json';source=json.loads(p.read_text());home=copy.deepcopy(source['bridges'][0]);home.update(resource_id=153,name='BRIDGE_HOME_GM7_C7_TO_CONTEST',harmony=[[0,'Gm7',7,[58,65]],[1,'C7',0,[58,64]]],rationale='The last D-to-E pair of HOME, uniformly condensed by half, expands its actual Gm7→C7 cadential relation. This is suitable for the new Gm11 or C7 clause breath, then Fminor. A C7 source can take a brief ii–V cadential extension.',bass=[[0,.8,43,57],[1,.85,36,59],[2,.8,43,54],[3,.55,36,52]],comp=[[0,.35,0,46],[1,.35,1,48],[2,.3,1,45],[3,.22,1,41]])
    home['source_fragment'].update(source_ids=[2058,2065],offset=27.5);home['tempo_map']=[[0,112],[1,116],[3,120]]
    back=copy.deepcopy(home);back.update(resource_id=154,name='BRIDGE_CONTEST_GM7_C7_TO_HOME',source_family=140,target_family=102,tempo_map=[[0,120],[1,116],[3,112]],swing=.5,rationale='The middle-section Eb/G ending retains G in bass and Bb in its melodic answer; Gm7 shares those tones before C7 resolves to Fmajor. The melodic D–E cadence is explicitly borrowed from HOME, preparing its return.')
    # Fragment source may differ from outgoing family: make_bridge reads this source explicitly.
    for spec in (home,back):spec['fragment_source_resource']=102
    return [b.make_bridge(home),b.make_bridge(back)]

def main():
    b.check(not sys.flags.optimize,'Optimized Python forbidden');add_bridges()
    results=[make(s)for s in json.loads((ROOT/'src/ready-arrangements.json').read_text())['arrangements']]
    allocation=json.loads((ROOT/'ALLOCATION.json').read_text());occupied=set(allocation['preserved_full_v4_sound_ids'])|{x for row in allocation['checked_maps']for x in row['sound_ids']};new=list(range(148,155));b.check(not occupied&set(new),'Additional Sound collision');allocation['sound_ids']=new;b.dump(ROOT/'ALLOCATION.json',allocation)
    lat=[]
    for r in results:
        candidates=[json.loads(p.read_text())for p in (ROOT/'generated').glob('BRIDGE_*-manifest.json')];dur=max(x['duration_seconds']for x in candidates if x['resource_id']in {g['bridge_resource']for g in r['gates']})
        lat.append(dict(source=r['resource_id'],target=152 if r['resource_id']==151 else 151,source_family=r['source_resource'],target_family=140 if r['source_resource']==102 else 102,max_wait_seconds=r['worst_wait_seconds'],max_request_to_bridge_first_attack_seconds=r['worst_wait_seconds']+.200004,max_bridge_seconds=dur,max_request_to_target_first_attack_seconds=r['worst_wait_seconds']+dur+.200004,edited_notes=r['edited_note_count'],preserved_notes=r['note_count']))
    b.dump(ROOT/'generated/ready-latency.json',dict(status='RESPONSIVE_OFFLINE_CANDIDATE_ASSUMING_REVIEWED_HOST',rows=lat,conditions=['Selected new arrangements151/152, not immutable102/140','≤2 native-tick polling, unchanged request, normal active playback','All three native/listening/release-tail gates remain false']))
    print(json.dumps(lat,indent=2))
if __name__=='__main__':main()
