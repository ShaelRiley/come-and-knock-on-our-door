#!/usr/bin/env python3
"""Derive reviewable candidate-only transport tables, with no script allocation."""
import json
import build as b
ROOT=b.ROOT;g=b.g

def main():
    for num in (151,152):
        m=next(json.loads(p.read_text())for p in (ROOT/'generated').glob('*READY*-manifest.json')if json.loads(p.read_text())['resource_id']==num)
        source=b.manifest(m['source_resource']);s=g.decode_sound((ROOT/f'generated/{num}.sound.bin').read_bytes());ns=b.notes_of(s);channels=[r['channel']for r in source['roles']];times={12,m['loop']['end_tick']};expr=[]
        for ch,es in s.items():
            if ch==15:continue
            for t,msg in es:
                if msg[0]&240 in (128,144)or(msg[0]&240==176 and msg[1]==11):times.add(t)
                if msg[0]&240==176 and msg[1]==11 and t:expr.append((t,channels.index(ch),msg[2]))
        expr.sort();windows=[];held=[]
        for left,right in zip(sorted(times),sorted(times)[1:]):
            if left<12:continue
            first=(left+3)//2*2;last=(right-7)//2*2
            if first>last:continue
            keys=[n for n in ns if n['on']<=first<n['off']]
            b.check(all(n['channel']!=9 for n in keys),'Percussion rejoin')
            windows.append([first,last,right,len(held),len(keys)])
            for n in keys:held.extend([channels.index(n['channel']),n['pitch'],n['velocity'],n['off']])
        initial=[source['initial_controllers'][str(ch)]['cc11']for ch in channels];loop=initial[:]
        for _,ch,v in expr:loop[ch]=v
        def at(part,t,wrapped):
            v=(loop if wrapped else initial)[part]
            for tick,p,x in expr:
                if p==part and tick<=t:v=x
            return v
        ha=[];hb=[]
        for first,last,right,off,count in windows:
            parts=[held[off+i*4]for i in range(count)];ha.append(int(all(at(p,first,False)==at(p,first,True)for p in parts)));hb.append(int(all(at(p,first,False)==at(p,first,True)for p in range(8))))
        color=[]
        if num==152:
            src=ROOT/'inputs/preserved/music-v4-binding-reconstruction-r2/inputs/music/analysis'
            for resource in range(140,146):
                row=next(json.loads(p.read_text())for p in src.glob('*-manifest.json')if json.loads(p.read_text())['resource_id']==resource);color.append([r['volume']for r in row['roles']])
        result=dict(resource=num,source_family=m['source_resource'],status='UNCOMPILED_NEW_TRANSPORT_TABLE_CANDIDATE',required_new_script_allocation=None,existing940_unchanged=True,existing981_unchanged=True,native_tick_us=b.TICK,loop=m['loop'],channels=channels,programs=[r['program']for r in source['roles']],pans=[r['pan']for r in source['roles']],initial_expression=initial,loop_expression=loop,expression_events=expr,key_windows=windows,held_words=held,history_a=ha,history_b=hb,state_gain_rows=color,source_exact_140_color_reference=num==152,phrase_handoff_gates=m['gates'],new_guard_text_resource=None,native_tested=False)
        b.dump(ROOT/f'generated/{num}-transport-tables.json',result)
if __name__=='__main__':main()
