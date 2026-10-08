"""Reproducible source, signal, and bounded controller verification."""
from pathlib import Path
import hashlib
import importlib.util
import io
import itertools
import json
import math
import struct
import sys
import wave
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'tests'))
import audience
from build import check_inputs,dump,sha
import runtime_checks

def require(ok,why):
    if not ok:raise AssertionError(why)

def metrics(data,plan):
    with wave.open(io.BytesIO(data)) as f:
        require((f.getnchannels(),f.getsampwidth(),f.getframerate(),f.getcomptype())==(1,2,22050,'NONE'),'PCM format')
        n=f.getnframes();pcm=f.readframes(n)
    require(n==round(plan['duration_ticks']*22050/60),'Sample count/tick mismatch')
    vals=struct.unpack('<'+'h'*n,pcm);peak=max(map(abs,vals));rms=math.sqrt(sum(v*v for v in vals)/n)
    nz=[i for i,v in enumerate(vals) if v]
    supports=[]
    for pulse in plan['pulses']:
        a=round(pulse['start']*22050/60);b=round((pulse['end']+2)*22050/60);supports.append((a,b))
        require(plan['text'][pulse['source_start']:pulse['source_end']]==pulse['word'],'Cadence provenance')
    require(all(b<=a for (_,b),(a,_) in zip(supports,supports[1:])),'Adjacent group bursts overlap')
    at=0
    for a,b in supports:
        require(not any(vals[at:a]),'Nonzero intended silence');at=b
    require(not any(vals[at:]),'Nonzero final silence')
    require(0<peak<=round(.18*32767) and peak<32767,'Amplitude bound/clipping')
    require(.005<rms/32767<.08,'Unexpected RMS')
    return dict(sample_count=n,seconds=n/22050,duration_ticks=plan['duration_ticks'],peak_signed16=peak,
                peak_dbfs=20*math.log10(peak/32767),rms_signed16=rms,rms_dbfs=20*math.log10(rms/32767),
                clipped_samples=sum(abs(v)>=32767 for v in vals),leading_silence_samples=nz[0],
                trailing_silence_samples=n-1-nz[-1],exact_zero_samples=sum(v==0 for v in vals),
                maximum_sample_step=max(abs(b-a) for a,b in zip(vals,vals[1:])),
                inter_burst_overlap=False,max_simultaneous_oscillators=3,
                intentional_chorus_overlap_samples=sum(max(0,round(p['end']*22050/60)-round((p['start']+2)*22050/60)) for p in plan['pulses']))

def verify():
    require(not sys.flags.optimize,'Run verification without -O')
    check_inputs();m=json.loads((H/'generated/manifest.json').read_text());handoff=json.loads((H/'reference/audience-audio-handoff.json').read_text())
    require(m['handoff_sha256']=='ad08a2d68dfd2e6cdb84df857de4c5104d69aee122d0e6d42e24863989b8cb45','Coordinated spans changed')
    require(m['catalog_sha256']=='3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c','Catalog identity')
    require(m['speech_units_sha256']=='d143242b3d56f57331b0adfb73481425792c0757f57bc0c01a1b94561527c475','Speech authority identity')
    require(m['principal_renderer_sha256']==handoff['principal_renderer_sha256'] and m['principal_profiles_sha256']==handoff['principal_profiles_sha256'],'Principal profile identity')
    require(set(p['id'] for p in json.loads((H/'reference/principal/profiles.json').read_text())['profiles'])=={'jack','bunny','frankie','stringer','milo','vivian','rita','felix'},'Principal registry expanded')
    require(m['profile_sha256']==sha((H/'audience-profile.json').read_bytes()) and m['renderer_sha256']==sha((H/'audience.py').read_bytes()),'Original implementation changed')
    require(len(m['speech'])==len(handoff['rows']),'Derived fragment count')
    require({tuple(r['binding']['word_ids']) for r in m['speech'] if r['binding']}==set(itertools.permutations([1,2,3])),'Finite observed permutations')
    for permutation in itertools.permutations([1,2,3]):
        selected=audience.select_observed_fragments(permutation,m)
        require(all(tuple(r['binding']['word_ids'])==permutation for r in selected),'Wrong observed order selected')
    for invalid in [None,[],[1,2],[1,1,2],[0,1,2],[1,2,4],[True,2,3],['1',2,3]]:
        try:audience.select_observed_fragments(invalid,m)
        except ValueError:pass
        else:raise AssertionError('Invalid observed order fell back')
    try:audience.select_observed_fragments([1,2,3],{'speech':[]})
    except ValueError:pass
    else:raise AssertionError('Missing observed variant fell back')
    signals=[];actual=set()
    for row,original in zip(m['speech'],handoff['rows']):
        require(all(row[k]==v for k,v in original.items()),'Source contract mismatch')
        plan=audience.schedule(row['fragment_id'],'audience',row['raw_text'])
        require(plan==json.loads((H/'generated/plans'/(row['fragment_id']+'.json')).read_text()),'Plan identity')
        second=audience.render(plan);first=(H/'generated/speech'/row['audio_file']).read_bytes()
        require(first==second and sha(first)==row['audio_sha256'],'Complete second PCM render mismatch')
        sync=(H/'generated/speech'/row['sync_file']).read_bytes()
        require(sync==audience.sync_patch(plan) and sha(sync)==row['sync_sha256'],'Sync repeat mismatch')
        require(runtime_checks.pairs(sync)==[(0,0),(plan['duration_ticks'],0)] and 0<plan['duration_ticks']<=1800,'Finite closed Sync bounds')
        require(row['speaker_number']==0 and row['speaker_id']=='audience' and not row['observation_credit'],'Identity/mouth/credit contract')
        signals.append(dict(fragment_id=row['fragment_id'],audio_file=row['audio_file'],audio_sha256=row['audio_sha256'],**metrics(first,plan)))
        actual.update([row['audio_file'],row['sync_file']])
    require({p.name for p in (H/'generated/speech').iterdir()}==actual,'Resource inventory')
    # Failure probes: templates and principal remapping must not emit a result.
    for speaker,text in [('jack','Ready.'),('audience','{visible_cue_order}.'),('audience',''),('audience','...'),('audience','x'*501)]:
        try:audience.schedule('INVALID',speaker,text)
        except ValueError:pass
        else:raise AssertionError('Invalid input accepted')
    # Tampering with scheduled pulses must fail, without altering any principal.
    bad=audience.schedule('NEGATIVE','audience','Ready.');bad['pulses'][0]['step']+=1
    try:audience.render(bad)
    except ValueError:pass
    else:raise AssertionError('Tampered plan accepted')
    controller=runtime_checks.run();dump(H/'evidence/controller-checks.json',controller)
    report=dict(status='PASS',full_second_render=True,source_variants=len(signals),signals=signals,
                controls=controller,principal_bytes_unchanged=True,listening_performed=False,native_launch=False,
                limitations=['DSP/format/controller-mock proof only; perceived timbral distinction and comfort require listening',
                             'Mock kernel clocks are not a native playback timing test',
                             'No runtime route writes, host activation, observation credit, actor presence, save/restore or desktop checks'])
    dump(H/'evidence/verification.json',report);return report
if __name__=='__main__':
    v=verify();print(json.dumps(dict(status=v['status'],source_variants=v['source_variants'],duration_ticks=[s['duration_ticks'] for s in v['signals']],peak_dbfs=[round(s['peak_dbfs'],2) for s in v['signals']],rms_dbfs=[round(s['rms_dbfs'],2) for s in v['signals']],controller=v['controls']['runs']),indent=2))
