"""Generate only the explicitly coordinated original Audience resources."""
from pathlib import Path
import hashlib
import json
import sys
sys.dont_write_bytecode=True
import audience
H=Path(__file__).resolve().parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def check_inputs():
    for name,digest in json.loads((H/'INPUT-SEAL.json').read_text()).items():
        if sha((H/name).read_bytes())!=digest:raise ValueError('Protected input changed: '+name)

def build():
    check_inputs()
    handoff=json.loads((H/'reference/audience-audio-handoff.json').read_text())
    units={u['line_id']:u for u in json.loads((H/'reference/authority/speech-units.json').read_text())['units']}
    records={r['id']:r for r in json.loads((H/'reference/authority/full-line-catalog.json').read_text())['records']}
    rows=[]
    for row in handoff['rows']:
        raw=row['raw_text'];unit=units[row['line_id']]
        if row['canonical_speech_unit']!=unit or row['canonical_template']!=unit['text']:raise ValueError('Canonical unit changed')
        binding=row['binding'];source=unit['text']
        if binding:
            if binding['query']!='p12VisibleWord' or binding['query_indices']!=[0,1,2] or not binding['no_default']:raise ValueError('Observed binding required')
            source=source.format(**binding['bindings'])
        if source[slice(*row['source_char_range'])]!=raw or source.encode()[slice(*row['source_utf8_byte_range'])].decode()!=raw:raise ValueError('Source span mismatch')
        if sha(raw.encode())!=row['raw_text_sha256']:raise ValueError('Fragment hash mismatch')
        plan=audience.schedule(row['fragment_id'],'audience',raw)
        pcm=audience.render(plan);sync=audience.sync_patch(plan);key=row['proposed_audio36'];name=audience.patch_name(**key)
        (H/'generated/speech').mkdir(parents=True,exist_ok=True)
        (H/'generated/speech'/name).write_bytes(pcm);(H/'generated/speech'/('#'+name[1:])).write_bytes(sync)
        dump(H/'generated/plans'/(row['fragment_id']+'.json'),plan)
        rows.append({**row,'audio36':key,'voice_index':key['noun'],'audio_file':name,'sync_file':'#'+name[1:],
                     'audio_sha256':sha(pcm),'sync_sha256':sha(sync),'duration_ticks':plan['duration_ticks'],
                     'mouth_events':plan['mouth_events'],'speaker_number':0,'display_name':'Audience',
                     'source_template_sha256':sha(unit['text'].encode()),'canonical_record':records[row['record_id']],
                     'delivery':'original_procedural_group_voice','profile_id':audience.PROFILE['id'],
                     'audible_gate':'future_host_proves_actual_current_audience_eligibility_and_pa_cue_context',
                     'mouth_gate':'no_principal_or_group_mouth','observation_credit':False,
                     'laugh_opportunity':unit['laugh_opportunity']})
    manifest=dict(schema=1,status='NEW_ORIGINAL_REVIEW_CANDIDATE',scope='Isolated Audience audio/data component; no host/native/listening acceptance',
                  speech=rows,coverage=dict(source_variants=len(rows),canonical_units=len({r['line_id'] for r in rows}),dynamic_variants=sum(r['binding'] is not None for r in rows)),
                  sample_rate=22050,channels=1,sample_width=2,signed_pcm=True,
                  profile_sha256=sha((H/'audience-profile.json').read_bytes()),renderer_sha256=sha((H/'audience.py').read_bytes()),
                  handoff_sha256=sha((H/'reference/audience-audio-handoff.json').read_bytes()),
                  catalog_sha256=sha((H/'reference/authority/full-line-catalog.json').read_bytes()),
                  speech_units_sha256=sha((H/'reference/authority/speech-units.json').read_bytes()),
                  principal_renderer_sha256=sha((H/'reference/principal/talk.py').read_bytes()),
                  principal_profiles_sha256=sha((H/'reference/principal/profiles.json').read_bytes()),
                  integration=dict(runtime_speaker=0,canonical_speaker_id='audience',lane=1,volume_control='Voice',mute_control='Voice',
                                   silent_clock_audio36=dict(module=911,noun=1,verb=1,cond=0,seq=1),
                                   no_speaker_registry_expansion=True,no_audio_observation_credit=True,actual_audience_eligibility_required=True,
                                   automatic_laughter_enabled=False))
    dump(H/'generated/manifest.json',manifest)
    return manifest
if __name__=='__main__':
    m=build();print(json.dumps(dict(status=m['status'],coverage=m['coverage'],files=[r['audio_file'] for r in m['speech']])))
