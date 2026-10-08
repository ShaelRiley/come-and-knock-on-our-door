#!/usr/bin/env python3
"""Export complete canonical P10 captions and exact presentation metadata.

Use the existing approved local eight-profile procedural renderer, never an
external TTS service, native launch, or mutation outside this directory. Existing
voice bytes may be copied only for an exact raw source span and speaker match.
"""
from pathlib import Path
from copy import deepcopy
import importlib.util
import argparse
import json
import sys
import textwrap

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE/'inputs/model'
SCI = HERE/'inputs/p08'
AUTHORITY = HERE/'inputs/authority'
BASELINE = HERE/'inputs'
CATALOG_SHA = '3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c'
MODULE, TEXT_RESOURCE = 922, 211
import caption_util as util
sha, dump, norm, paginate = util.sha, util.dump, util.norm, util.paginate
SPEAKERS = util.SPEAKERS
sys.path.insert(0, str(ROOT))
from cakood import p10_model as model


def generate(reuse_audio=False):
    from guard import input_check
    input_check()
    out = HERE/'generated'
    for name in ('generated/speech','snapshot','evidence'):
        (HERE/name).mkdir(parents=True, exist_ok=True)
    revision_file = AUTHORITY/'CURRENT-SCRIPT-REVISION.json'
    revision = json.loads(revision_file.read_text())
    catalog_file, speech_file = AUTHORITY/revision['catalog'], AUTHORITY/revision['speech']
    assert revision['editorial_revision'] == 3
    assert revision['catalog_sha256'] == sha(catalog_file.read_bytes()) == CATALOG_SHA
    catalog, speech = json.loads(catalog_file.read_text()), json.loads(speech_file.read_text())
    fixture_file = ROOT/'tests/fixtures/p10/canonical-bindings.json'
    adapter_file = HERE/'inputs/domain/schema.json'
    fixture, adapter = json.loads(fixture_file.read_text()), json.loads(adapter_file.read_text())
    catalog_records={r['id']:r for r in catalog['records'] if r['id'].startswith('P10.')}
    speech_units={u['line_id']:u for u in speech['units'] if u['record_id'].startswith('P10.')}
    # Native domain IDs are authoritative; catalog/alphabetical order is not an ABI.
    records={rid:catalog_records[rid] for rid in sorted(adapter['line_ids'],key=adapter['line_ids'].get)}
    units=[speech_units[uid] for uid in sorted(adapter['speech_unit_ids'],key=adapter['speech_unit_ids'].get)]
    assert len(records)==23 and len(units)==20
    assert set(records)==set(catalog_records)==set(fixture['records'])
    assert list(adapter['line_ids'].values())==list(range(1,24))
    assert list(adapter['speech_unit_ids'].values())==list(range(1,21))
    assert adapter['speech_metadata']==units
    assert fixture['catalog_sha256']==CATALOG_SHA and fixture['speech_sha256']==sha(speech_file.read_bytes())
    assert fixture['gdd_sha256']==sha((AUTHORITY/'complete-body.md').read_bytes())=='18e2eb1a300cc1ac1192916441b640ca6134af619ee17eb424637b4dde28647c'
    assert adapter['source_bindings']==fixture['source_bindings']==model.P10World.SOURCES
    assert fixture['record_units']=={k:list(v) for k,v in model.RECORD_UNITS.items()}
    by_record = {rid:[u for u in units if u['record_id']==rid] for rid in records}
    registry_file = HERE/'COMPATIBILITY.json'
    registry = json.loads(registry_file.read_text())
    assert registry['text']==211 and registry['audio']==922
    assert registry['record_documents']==[1200,1222] and registry['unit_documents']==[1223,1242]
    existing_voices, audio_audit = [], [] # All P10 fragments regenerated from frozen approved profiles
    profile_hash=sha((SCI/'inputs/talk-prototype/profiles.json').read_bytes())
    renderer_hash=sha((SCI/'inputs/talk-prototype/talk.py').read_bytes())
    previous=json.loads((out/'manifest.json').read_text()) if reuse_audio else None
    if previous:
        assert previous['profile_sha256']==profile_hash and previous['renderer_sha256']==renderer_hash
    old_audio={v['fragment_id']:v for v in previous['speech']} if previous else {}
    protected = [p for p in (HERE/'inputs').rglob('*') if p.is_file()]
    protected += [HERE/'COMPATIBILITY.json',HERE/'caption_util.py']
    hashes = {str(p.relative_to(HERE)):sha(p.read_bytes()) for p in sorted(protected)}
    for source,name in ((revision_file,'CURRENT-SCRIPT-REVISION.json'),(fixture_file,'canonical-bindings.json'),
                        (adapter_file,'domain-manifest.json')):
        (HERE/'snapshot'/name).write_bytes(source.read_bytes())
    dump(HERE/'snapshot/canonical-records.json',{'catalog_sha256':CATALOG_SHA,'records':list(records.values())})
    dump(HERE/'snapshot/canonical-speech-units.json',{'speech_sha256':sha(speech_file.read_bytes()),'units':units})
    bank, bank_index, pages, routes, voices, missing = [], {}, [], [], [], []
    def entry(text):
        data = text.encode('ascii'); assert b'\0' not in data
        if data not in bank_index:
            bank_index[data]=len(bank); bank.append(data)
        return bank_index[data]
    for rid,record in records.items():
        local = adapter['line_ids'][rid]; document = 1199+local
        provenance = fixture['records'][rid]
        assert record['text_sha256'] == provenance['text_sha256'] == sha(json.dumps(record['text'],ensure_ascii=False).encode())
        assert fixture['record_units'][rid] == [u['line_id'] for u in by_record[rid]]
        assert {u['line_id']:fixture['speakers'][u['line_id']] for u in by_record[rid]} == {u['line_id']:u['speaker_id'] for u in by_record[rid]}
        assert provenance['source_obligations'] == record['source_obligations']
        first = len(pages)
        segments = util.source_segments(record,by_record[rid])
        for si,segment in enumerate(segments):
            raw = segment['source_text']
            segment.update(source_text_sha256=sha(raw.encode()),source_words=len(raw.split()),
                source_characters=len(raw),source_utf8_bytes=len(raw.encode()))
            uid = adapter['speech_unit_ids'].get(segment['line_id'],0)
            unit = next((u for u in by_record[rid] if u['line_id']==segment['line_id']),None)
            if unit: segment['canonical_speech_unit']=unit
            group = paginate(raw); header=entry(norm(segment['source_speaker']))
            assert len(bank[header])*6 <= 204
            for part,page in enumerate(group):
                page.update(record_id=rid,document_id=document,local_line_key=local,global_line_key=document,
                    line_id=segment['line_id'],speech_unit_id=uid,source_pointer=segment['source_pointer'],
                    segment_index=si,source_text_sha256=segment['source_text_sha256'],part=part,part_count=len(group),
                    last_of_unit=bool(uid and part==len(group)-1),resource=TEXT_RESOURCE,entry=entry(page['text']),
                    header_entry=header,display_name=segment['source_speaker'],speaker_id=segment['speaker_id'],
                    speaker_number=SPEAKERS.get(segment['speaker_id'],0),role=segment['role'],
                    voice_index=0,audio_module=0,duration_ticks=0,canonical_location=record['location'],
                    source_words=len(page['raw_text'].split()),source_characters=len(page['raw_text']),
                    source_utf8_bytes=len(page['raw_text'].encode()),canonical_speech_unit=unit,
                    delivery='silent_text',mouth_gate='no_actor_mouth',document_kind='record')
                if uid:
                    match=next((v for v in existing_voices if v['speaker_id']==page['speaker_id'] and v['raw_text']==page['raw_text']),None)
                    if match:
                        noun=len(voices)+1
                        filename=util.talk.patch_name(MODULE,noun)
                        for src,name in ((match['source_audio'],filename),(match['source_sync'],'#'+filename[1:])):
                            (out/'speech'/name).write_bytes(Path(src).read_bytes())
                        voice={k:page[k] for k in ('record_id','line_id','speaker_id','raw_text','raw_text_sha256','part','part_count')}
                        voice.update(fragment_id=f'{segment["line_id"]}.page{part+1:02d}',voice_index=noun,
                            audio36={'module':MODULE,'noun':noun,'verb':1,'cond':0,'seq':1},
                            audio_file=filename,sync_file='#'+filename[1:],audio_sha256=match['audio_sha256'],
                            sync_sha256=match['sync_sha256'],duration_ticks=match['duration_ticks'],
                            mouth_events=match['mouth_events'],reuse_source_manifest=match['source_manifest'],
                            reuse_source_audio=match['source_audio'],reuse_source_sync=match['source_sync'],
                            audible_gate='actual_actor_in_current_room',mouth_gate='actual_visible_actor_in_current_room')
                        voice.update(canonical_speech_unit=unit,laugh_opportunity=unit['laugh_opportunity'])
                        voices.append(voice)
                        page.update(voice_index=noun,audio_module=MODULE,duration_ticks=voice['duration_ticks'],
                            delivery='principal',mouth_gate='actual_visible_actor_in_current_room')
                    else:
                        noun=len(voices)+1;fragment=f'{segment["line_id"]}.page{part+1:02d}'
                        plan=util.talk.schedule(fragment,segment['speaker_id'],page['raw_text'])
                        filename=util.talk.patch_name(MODULE,noun);sync=util.talk.sync_patch(plan)
                        if reuse_audio:
                            old=old_audio[fragment]
                            assert old['raw_text_sha256']==page['raw_text_sha256'] and old['speaker_id']==page['speaker_id']
                            audio=(out/'speech'/filename).read_bytes()
                            assert sha(audio)==old['audio_sha256'] and sha(sync)==old['sync_sha256']
                            assert (out/'speech'/('#'+filename[1:])).read_bytes()==sync
                        else:audio=util.talk.render(plan)
                        (out/'speech'/filename).write_bytes(audio)
                        (out/'speech'/('#'+filename[1:])).write_bytes(sync)
                        voice={k:page[k] for k in ('record_id','line_id','speaker_id','raw_text','raw_text_sha256','part','part_count')}
                        voice.update(fragment_id=fragment,voice_index=noun,
                            audio36={'module':MODULE,'noun':noun,'verb':1,'cond':0,'seq':1},
                            audio_file=filename,sync_file='#'+filename[1:],audio_sha256=sha(audio),sync_sha256=sha(sync),
                            duration_ticks=plan['duration_ticks'],mouth_events=plan['mouth_events'],
                            generation='existing_local_original_profile_procedural_renderer',
                            profile_sha256=profile_hash,renderer_sha256=renderer_hash,
                            audible_gate='actual_actor_in_current_room',mouth_gate='actual_visible_actor_in_current_room')
                        voice.update(canonical_speech_unit=unit,laugh_opportunity=unit['laugh_opportunity'])
                        voices.append(voice)
                        page.update(voice_index=noun,audio_module=MODULE,duration_ticks=voice['duration_ticks'],
                            delivery='principal',mouth_gate='actual_visible_actor_in_current_room')
                page['fields']=[page['entry'],document,part,len(group),page['speaker_number'],page['voice_index'],header,page['bytes_with_nul']]
                page['record_page']=page['document_page']=len(pages)-first
                page['page_index']=len(pages)
                pages.append(page)
        routes.append({'record_id':rid,'local_line_key':local,'global_line_key':document,'document_id':document,
            'document_kind':'record','dispatch':'scene','first_page':first,'page_count':len(pages)-first,
            'page_indices':list(range(first,len(pages))),'kind':record['kind'],'source_ref':record['source_ref'],
            'trigger':record['trigger'],'source_obligations':record['source_obligations'],
            'canonical_provenance':provenance,'canonical_location':record['location'],
            'source_text':record['text'],'source_text_json_sha256':record['text_sha256'],'segments':segments,
            'canonical_units':[u['line_id'] for u in by_record[rid]],'required_response':record['kind'] not in ('label','inventory')})
    record_page_count=len(pages)
    by_id={r['record_id']:r for r in routes}
    unit_routes=[]
    for unit in units:
        uid=adapter['speech_unit_ids'][unit['line_id']];document=1222+uid;first=len(pages)
        originals=[p for p in pages[:record_page_count] if p['line_id']==unit['line_id']]
        for index,original in enumerate(originals):
            p=deepcopy(original)
            p.update(document_id=document,global_line_key=document,document_page=index,document_kind='speech_unit',
                     source_record_page_index=original['page_index'],page_index=len(pages))
            p['fields'][1]=document;pages.append(p)
        unit_routes.append({'record_id':unit['record_id'],'line_id':unit['line_id'],'speech_unit_id':uid,
            'local_line_key':adapter['line_ids'][unit['record_id']],'document_id':document,'global_line_key':document,
            'document_kind':'speech_unit','dispatch':'scene','first_page':first,'page_count':len(pages)-first,
            'page_indices':list(range(first,len(pages))),'source_record_document':by_id[unit['record_id']]['document_id'],
            'source_record_pages':[p['record_page'] for p in originals],
            'canonical_speech_unit':unit,'source_text':unit['text'],'source_text_sha256':sha(unit['text'].encode())})
    units_by_id={u['line_id']:u for u in unit_routes}
    record_receipts={r['record_id']:{'record_id':r['record_id'],'record_number':r['local_line_key'],
        'document_id':r['document_id'],'pages':[[r['document_id'],n] for n in range(r['page_count'])],
        'canonical_tokens':list(model.RECORD_UNITS[r['record_id']] or (r['record_id'],)),
        'units':[{'line_id':u,'speech_unit_id':adapter['speech_unit_ids'][u],
            'record_pages':units_by_id[u]['source_record_pages'],
            'last_record_page':units_by_id[u]['source_record_pages'][-1],
            'unit_document':units_by_id[u]['document_id']} for u in r['canonical_units']]}
        for r in routes}
    unit_receipts={u['line_id']:{'line_id':u['line_id'],'record_id':u['record_id'],'speech_unit_id':u['speech_unit_id'],
        'document_id':u['document_id'],'pages':[[u['document_id'],n] for n in range(u['page_count'])],
        'record_pages':[[u['source_record_document'],n] for n in u['source_record_pages']],
        'source_text_sha256':u['source_text_sha256']} for u in unit_routes}
    source_receipts={source:{'source_number':adapter['sources'][source],'record_ids':[rid],
        'documents':[by_id[rid]['document_id']],
        'canonical_tokens':[t['token'] for t in adapter['receipts'][source]],
        'token_numbers':[adapter['tokens'][t['token']] for t in adapter['receipts'][source]]}
        for source,rid in adapter['source_bindings'].items()}
    payload=b'\0'.join(bank)+b'\0';assert len(payload)<32768
    (out/'211.text.bin').write_bytes(payload)
    offsets=[];position=0
    for item in bank:offsets.append(position);position+=len(item)+1
    for page in pages:
        page['text_bank_byte_range']=[offsets[page['entry']],offsets[page['entry']]+page['bytes_with_nul']]
        page['display_ascii_sha256']=sha(bank[page['entry']])
    document_routes=[{k:r[k] for k in ('document_id','record_id','document_kind','first_page','page_count','page_indices')}
        | ({'line_id':r['line_id'],'speech_unit_id':r['speech_unit_id']} if 'line_id' in r else {}) for r in routes+unit_routes]
    manifest={'schema':1,'scope':'New current-authority P10 canonical scene and procedural audio component; no recovered historical exporter or native host claim.',
        'editorial_revision':3,'catalog_sha256':CATALOG_SHA,'speech_sha256':sha(speech_file.read_bytes()),
        'gdd_sha256':fixture['gdd_sha256'],'protected_inputs_sha256':hashes,
        'baseline_source':'inputs/src/module982.sc','baseline_source_sha256':hashes['inputs/src/module982.sc'],
        'text_resource':TEXT_RESOURCE,'text_resource_sha256':sha(payload),'text_bytes':len(payload),'entries':len(bank),
        'max_body_bytes':max(p['bytes_with_nul'] for p in pages),'audio_modules':[MODULE],
        'profile_sha256':profile_hash,'renderer_sha256':renderer_hash,
        'audio_policy':'Unchanged frozen approved eight-profile local original procedural renderer; all fragments regenerated; no external TTS.',
        'speaker_numbers':SPEAKERS,'geometry':{'columns':50,'body_lines':3,'font':util.font_metrics(),
            'body':[6,158,314,182],'header':[6,147,210,155],'header_separate':True},
        'typography':{'display_only':'Established uppercase ASCII and punctuation transliteration; line wrapping only.',
            'source_reconstruction':'Concatenate exact raw_text per source segment; retain original Unicode punctuation and character/byte ranges.'},
        'shared_zero_clock':{'module':911,'noun':1,'verb':1,'cond':0,'seq':1},
        'line_keys':{r['record_id']:r['document_id'] for r in routes},'local_line_keys':adapter['line_ids'],
        'local_unit_keys':adapter['speech_unit_ids'],'unit_documents':{u['line_id']:u['document_id'] for u in unit_routes},
        'canonical_speech_units':units,'routes':routes,'unit_routes':unit_routes,'document_routes':document_routes,
        'pages':pages,'speech':voices,'missing_speech':missing,
        'silent_readers':{source:{'record_id':rid,'document_id':by_id[rid]['document_id'],'pages':by_id[rid]['page_indices'],
            'dispatch':'complete canonical scene pagination, silent','acknowledge':'Host-authenticated unobscured draw+Graph12 for every page under exact source/start/epoch lease'}
            for source,rid in adapter['source_bindings'].items() if not by_record[rid]},
        'source_bindings':adapter['source_bindings'],
        'record_receipts':record_receipts,'unit_receipts':unit_receipts,'source_receipts':source_receipts,
        'receipt_semantics':{'full_record_requires_all_pages':True,'unit_requires_all_unit_pages':True,
            'queue_open_last_page_audio_completion_are_not_display_receipts':True,
            'full_source_and_unit_authority_distinct':True,'printed_interface_choices_hints_silent':True},
        'host_api':{'domain_script':992,'domain_standalone_species':1,'domain_production_reserved_species':14,
            'scene_script':982,'scene_species':4,'record_document':'explicit p10Line key map; locals1..23',
            'unit_document':'explicit p10Unit key map; units1..20',
            'acknowledge':'p10Acknowledge(source,startHi,startLo,epoch,recordNumber,firstUnit,lastUnit); exactly one form.',
            'unit_boundary':'last_of_unit after every exact unit page is visibly authenticated by host',
            'lease':'Begin/resume arms exact current source/start/epoch; boundary, load, replacement or close retires it.',
            'presentation':'sdOpen; sdDraw; unobscured Graph12; exact host receipt; sdPresented; actual actor gate; optional sdSpeak.',
            'cancel_on':['travel','apron','menu','load','replacement','reader close/cancel','unseen skipped page'],
            'audio_skip':'Shown text may count when audio is skipped or muted; audio completion and unshown pages never count.',
            'presence':'Canonical location is metadata only. Host must establish actual room, eligibility and visible actor before speech/mouth activity.',
            'journal':'Only exact acknowledged record/unit content; partial unit evidence never grants an unshown parent record.',
            'generic_codes':'Internal machine codes have no invented fallback dialogue.'},
        'cue_handoff':adapter['cue_handoff'],
        'original_controls':{k:v for k,v in adapter['own_objects'].items()},
        'original_tile_units':[48,49,50],
        'ownership_contract':{'stable_cue_ids':adapter['cue_ids'],'domain_owned_paper_cues':[412,413,414],
            'original_ceramic_units':[48,49,50],'aggregate35_projection':'Later campaign host responsibility; never substitute group35 for actual tile ownership.',
            'rack_contents':'Query current slot identity and labels; never infer from cached completion flag.',
            'signature_consent':'No P09/P14 signature, date or consent changes.'},
        'coverage':{'authority_records':len(records),'adapter_records':len(adapter['line_ids']),
            'canonical_speech_units':len(units),'record_documents':len(routes),'unit_documents':len(unit_routes),
            'routable_documents':len(document_routes),'record_pages':record_page_count,'unit_pages':len(pages)-record_page_count,
            'pages':len(pages),'voiced_fragments':len(voices),'procedural_voice_fragments':len(voices),
            'missing_voice_fragments':len(missing),'caption_only_pages':sum(not p['voice_index'] for p in pages),
            'source_words':sum(s['source_words'] for r in routes for s in r['segments']),
            'source_characters':sum(s['source_characters'] for r in routes for s in r['segments'])},
        'explicit_gaps':['No P10 native host or playable campaign integration.',
            'Native display receipt authentication, actor eligibility, ownership composition, controller and save/restore are later host gates.',
            'No playback, listening, room/actor placement or native visual acceptance.']}
    dump(out/'manifest.json',manifest)
    dump(out/'line-document-map.json',{r['record_id']:{k:r[k] for k in ('local_line_key','document_id','page_count')} for r in routes})
    dump(out/'unit-document-map.json',{u['line_id']:{k:u[k] for k in ('speech_unit_id','document_id','source_record_document','source_record_pages','page_count')} for u in unit_routes})
    dump(out/'receipt-map.json',{k:manifest[k] for k in ('record_receipts','unit_receipts','source_receipts','receipt_semantics')})
    dump(out/'route-inventory.json',{k:manifest[k] for k in ('document_routes','source_bindings','silent_readers','host_api','cue_handoff')})
    def sc_array(name,values):return f'[{name} {len(values)}] = ['+' '.join(map(str,values))+']'
    (out/'p10-host-tables.inc').write_text('; P10 local page indices; add extension existing_pages for absolute scene table indices.\n'+'\n'.join([
        sc_array('p10RecordDocuments',[0]+[r['document_id'] for r in routes]),
        sc_array('p10UnitDocuments',[0]+[r['document_id'] for r in unit_routes]),
        sc_array('p10PageUnits',[p['speech_unit_id'] for p in pages]),
        sc_array('p10PageLastOfUnit',[int(p['last_of_unit']) for p in pages]),
        sc_array('p10PageRecordIds',[p['local_line_key'] for p in pages])])+'\n')
    dump(HERE/'evidence/allocation-check.json',{'status':'PASS','text':211,'reserved_audio36_module':922,
        'used_record_documents':[1200,1222],'used_unit_documents':[1223,1242],
        'evidence':'inputs/typed-resource-inventory.json','namespace_rule':'Explicit unused typed resources/documents on frozen P09 universe; existing P09 reservation left intact.'})
    for path,digest in hashes.items():assert sha((HERE/path).read_bytes())==digest,path
    print(json.dumps({'coverage':manifest['coverage'],'text_bytes':len(payload),'entries':len(bank)},indent=2))
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--reuse-audio',action='store_true')
    generate(parser.parse_args().reuse_audio)
