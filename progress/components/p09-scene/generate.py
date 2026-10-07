#!/usr/bin/env python3
"""Export complete canonical P09 captions and exact presentation metadata.

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
MODULE, TEXT_RESOURCE = 921, 210
import caption_util as util
sha, dump, norm, paginate = util.sha, util.dump, util.norm, util.paginate
SPEAKERS = util.SPEAKERS
sys.path.insert(0, str(ROOT))
from cakood import p09_model as model


def reader_text(text):
    return '\n'.join('\n'.join(textwrap.wrap(line, width=48, break_long_words=False,
        break_on_hyphens=False)) if line else '' for line in norm(text).split('\n'))


def voice_candidates():
    """Search existing canonical exports, verifying the actual reusable bytes."""
    candidates, audited = [], []
    for path in sorted([SCI/'generated/manifest.json']):
        manifest = json.loads(path.read_text())
        audited.append({'path': str(path.relative_to(HERE)), 'sha256': sha(path.read_bytes())})
        for voice in manifest.get('speech', []):
            if not all(k in voice for k in ('raw_text','speaker_id','audio_file','sync_file',
                    'audio_sha256','sync_sha256','duration_ticks','mouth_events')):
                continue
            audio, sync = (path.parent/'speech'/voice[k] for k in ('audio_file','sync_file'))
            if not audio.is_file() or not sync.is_file():
                continue
            assert sha(audio.read_bytes()) == voice['audio_sha256'], audio
            assert sha(sync.read_bytes()) == voice['sync_sha256'], sync
            candidates.append({**voice, 'source_manifest': str(path),
                               'source_audio': str(audio), 'source_sync': str(sync)})
    return candidates, audited


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
    fixture_file = ROOT/'tests/fixtures/p09/canonical-bindings.json'
    adapter_file = HERE/'inputs/domain/schema.json'
    fixture, adapter = json.loads(fixture_file.read_text()), json.loads(adapter_file.read_text())
    records = {r['id']:r for r in catalog['records'] if r['id'].startswith('P09.')}
    units = [u for u in speech['units'] if u['record_id'].startswith('P09.')]
    assert len(records) == len(units) == 20
    assert list(records) == list(adapter['line_ids']) and set(records) == set(fixture['records'])
    assert list(adapter['line_ids'].values()) == list(range(1,21))
    assert [u['line_id'] for u in units] == list(adapter['speech_unit_ids'])
    assert list(adapter['speech_unit_ids'].values()) == list(range(1,21))
    assert adapter['speech_metadata']==[{k:u[k] for k in ('line_id','record_id','speaker_id','laugh_opportunity')} for u in units]
    assert fixture['catalog_sha256'] == CATALOG_SHA and fixture['speech_sha256'] == sha(speech_file.read_bytes())
    assert {k:v['records'] for k,v in adapter['bindings'].items()} == {k:list(v) for k,v in model.SCRIPT_BINDINGS.items()}
    assert adapter['source_bindings'] == {k:list(v) for k,v in model.SOURCE_BINDINGS.items()}
    by_record = {rid:[u for u in units if u['record_id']==rid] for rid in records}
    registry_file = HERE/'COMPATIBILITY.json'
    registry = json.loads(registry_file.read_text())
    assert registry['text']==210 and registry['audio']==921
    assert registry['record_documents']==[1100,1119] and registry['unit_documents']==[1120,1139]
    existing_voices, audio_audit = voice_candidates()
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
                        (adapter_file,'domain-manifest.json'),(ROOT/'docs/p09-state-contract.md','p09-state-contract.md')):
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
        local = adapter['line_ids'][rid]; document = 1099+local
        provenance = fixture['records'][rid]
        assert record['text_sha256'] == provenance['text_sha256'] == sha(json.dumps(record['text'],ensure_ascii=False).encode())
        assert provenance['speech_units'] == [u['line_id'] for u in by_record[rid]]
        assert provenance['speech_speakers'] == {u['line_id']:u['speaker_id'] for u in by_record[rid]}
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
        uid=adapter['speech_unit_ids'][unit['line_id']];document=1119+uid;first=len(pages)
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
        'canonical_tokens':list(model._record_tokens(r['record_id'])),
        'units':[{'line_id':u,'speech_unit_id':adapter['speech_unit_ids'][u],
            'record_pages':units_by_id[u]['source_record_pages'],
            'last_record_page':units_by_id[u]['source_record_pages'][-1],
            'unit_document':units_by_id[u]['document_id']} for u in r['canonical_units']]}
        for r in routes}
    unit_receipts={u['line_id']:{'line_id':u['line_id'],'record_id':u['record_id'],'speech_unit_id':u['speech_unit_id'],
        'document_id':u['document_id'],'pages':[[u['document_id'],n] for n in range(u['page_count'])],
        'record_pages':[[u['source_record_document'],n] for n in u['source_record_pages']],
        'source_text_sha256':u['source_text_sha256']} for u in unit_routes}
    source_receipts={source:{'source_number':adapter['sources'][source],'record_ids':ids,
        'documents':[by_id[r]['document_id'] for r in ids],
        'canonical_tokens':[t['token'] for t in adapter['receipts'][source]],
        'token_numbers':[adapter['tokens'][t['token']] for t in adapter['receipts'][source]]}
        for source,ids in adapter['source_bindings'].items()}
    readers={}
    for source,rid in (('chair_tag','P09.READ.001'),('terms_card','P09.READ.002')):
        raw=records[rid]['text'];shown=reader_text(raw)
        assert len(shown.splitlines())<=14 and max(map(len,shown.splitlines()))<=48 and len(shown.encode())+1<=896
        readers[source]={'record_id':rid,'local_line_key':adapter['line_ids'][rid],
            'document_id':by_id[rid]['document_id'],'source_number':adapter['sources'][source],
            'entry':entry(shown),'header_entry':entry(norm(records[rid]['speaker'])),'text':shown,'raw_text':raw,
            'raw_text_sha256':sha(raw.encode()),'bytes_with_nul':len(shown.encode())+1,'resource':TEXT_RESOURCE,
            'geometry':{'columns':48,'maximum_lines':14,'body':[16,44,304,156]},
            'required_room':6 if source=='chair_tag' else None,
            'acknowledge':'Only complete unobscured draw+Graph12 under current exact source/start/epoch lease; never open, queue, or audio.'}
    payload=b'\0'.join(bank)+b'\0'; assert len(payload)<32768
    (out/'210.text.bin').write_bytes(payload)
    offsets=[];position=0
    for item in bank:offsets.append(position);position+=len(item)+1
    for page in pages:
        page['text_bank_byte_range']=[offsets[page['entry']],offsets[page['entry']]+page['bytes_with_nul']]
        page['display_ascii_sha256']=sha(bank[page['entry']])
    document_routes=[{k:r[k] for k in ('document_id','record_id','document_kind','first_page','page_count','page_indices')}
        | ({'line_id':r['line_id'],'speech_unit_id':r['speech_unit_id']} if 'line_id' in r else {})
        for r in routes+unit_routes]
    manifest={'schema':1,'scope':'Exact P09 scene data, source/page/unit receipts, and original-profile procedural audio; no native acceptance.',
        'editorial_revision':3,'catalog_sha256':CATALOG_SHA,'speech_sha256':sha(speech_file.read_bytes()),
        'protected_inputs_sha256':hashes,'baseline_source':'inputs/src/module982.sc',
        'baseline_source_sha256':hashes['inputs/src/module982.sc'],
        'text_resource':TEXT_RESOURCE,'text_resource_sha256':sha(payload),'text_bytes':len(payload),'entries':len(bank),
        'max_body_bytes':max(p['bytes_with_nul'] for p in pages),'audio_modules':[MODULE],
        'profile_sha256':profile_hash,'renderer_sha256':renderer_hash,
        'audio_policy':'Existing approved local eight-profile procedural renderer; no external service, software install, or voice imitation. Exact verified span+speaker reuse is permitted.',
        'speaker_numbers':SPEAKERS,'geometry':{'columns':50,'body_lines':3,'font':util.font_metrics(),
            'body':[6,158,314,182],'header':[6,147,210,155],'header_separate':True},
        'typography':{'display_only':'Uppercase ASCII with established punctuation transliteration; line wrapping only.',
            'source_reconstruction':'Concatenate exact raw_text per record segment or unit; no source characters deleted.'},
        'shared_zero_clock':{'module':911,'noun':1,'verb':1,'cond':0,'seq':1},
        'line_keys':{r['record_id']:r['document_id'] for r in routes},'local_line_keys':adapter['line_ids'],
        'local_unit_keys':adapter['speech_unit_ids'],'unit_documents':{u['line_id']:u['document_id'] for u in unit_routes},
        'canonical_speech_units':units,'routes':routes,'unit_routes':unit_routes,'document_routes':document_routes,
        'pages':pages,'speech':voices,'missing_speech':missing,'voice_reuse_audit':audio_audit,'readers':readers,
        'domain_bindings':adapter['bindings'],'binding_routes':{k:[by_id[r]['document_id'] for r in v['records']] for k,v in adapter['bindings'].items()},
        'record_receipts':record_receipts,'unit_receipts':unit_receipts,'source_receipts':source_receipts,
        'receipt_semantics':{
            'rumor_correction_units':['P09.LOOK.001.01','P09.DIALOGUE.001.01','P09.FAILURE.001.01'],
            'class_context_units':['P09.DIALOGUE.001.01','P09.FAILURE.001.02'],
            'restricted_accusation_units':['P09.FAILURE.001.01'],
            'terms_grant_record':'P09.DIALOGUE.002','terms_grant_units':[u['line_id'] for u in by_record['P09.DIALOGUE.002']],
            'separate_post_grant_record':'P09.SUCCESS.001','choice_hint_label_receipts_grant_nothing':True,
            'full_record_requires_all_pages':True,'unit_requires_all_unit_pages':True,
            'terms_and_success_must_not_share_acknowledgment':True,
            'not_knowledge':['P09.OPEN.001','P09.READ.001','P09.HINT.1','P09.HINT.2','P09.HINT.3']},
        'host_api':{'domain_script':990,'domain_species':12,'scene_script':982,'scene_species':4,
            'record_document':'1099 + p09Line(i), locals1..20','unit_document':'1119 + p09Unit(i), units1..20',
            'acknowledge':'p09Acknowledge(source,startHi,startLo,epoch,recordNumber,firstUnit,lastUnit); exactly one form.',
            'unit_boundary':'pages[].last_of_unit and speech_unit_id after EVERY page in that exact unit was visible.',
            'lease':'Begin/resume arms current source/start/epoch; context replacement or invalidate drains lease.',
            'presentation':'sdOpen; sdDraw; unobscured Graph12; exact page receipt; sdPresented; actual-actor gate; optional sdSpeak.',
            'cancel_on':['travel','apron','menu','load','replacement','reader close/cancel','unseen skipped page'],
            'audio_skip':'Previously visible complete text counts when audio is skipped or muted; unseen pages never count.',
            'presence':'Never derive actual actor presence, viewpoint, or reachability from canonical location metadata.',
            'journal':'Only exact acknowledged records/units; partial unit evidence must not reopen a whole unshown record.',
            'generic_codes':'Machine codes stay internal; no invented fallback wording.'},
        'card_handoff':adapter['card_handoff'],
        'prop_needs':[{'object_id':395,'stable_id':'tagged_chairs','need':'Three matching fixed chairs visibly carrying tag(s); inspection works without NPCs.'},
            {'object_id':396,'stable_id':'chair_tag','need':'Attached furniture tag with exact silent reader HOUSE LOT — THREE; never picked up or destroyed.'},
            {'object_id':397,'stable_id':'conservatory_front','need':'Reachable front viewpoint hotspot within L07; no extra room or teleport.'},
            {'object_id':398,'stable_id':'conservatory_side','need':'Side viewpoint within L07 for incomplete opening only.'},
            {'object_id':399,'stable_id':'renewal_repair_card','need':'One unsigned inventory card; complete reader, blank date/signature; P14 owns future signing.'}],
        'coverage':{'authority_records':len(records),'adapter_records':len(adapter['line_ids']),
            'canonical_speech_units':len(units),'record_documents':len(routes),'unit_documents':len(unit_routes),
            'routable_documents':len(document_routes),'record_pages':record_page_count,'unit_pages':len(pages)-record_page_count,
            'pages':len(pages),'voiced_fragments':len(voices),
            'reused_voice_fragments':sum('reuse_source_audio' in v for v in voices),
            'procedural_voice_fragments':sum('generation' in v for v in voices),'missing_voice_fragments':len(missing),
            'caption_only_pages':sum(not p['voice_index'] for p in pages),
            'source_words':sum(s['source_words'] for r in routes for s in r['segments']),
            'source_characters':sum(s['source_characters'] for r in routes for s in r['segments'])},
        'explicit_gaps':[
            'Native draw/Graph12 receipt authentication, current host epochs, actor gating, save/restore, and listening need host verification.',
            'Props listed separately are requirements, not generated art or native visual acceptance.',
            'No P10, P14 signature/date, legal guarantee, eviction timer, or campaign completion is introduced.']}
    dump(out/'manifest.json',manifest)
    dump(out/'line-document-map.json',{r['record_id']:{k:r[k] for k in ('local_line_key','document_id','page_count')} for r in routes})
    dump(out/'unit-document-map.json',{u['line_id']:{k:u[k] for k in ('speech_unit_id','document_id','source_record_document','source_record_pages','page_count')} for u in unit_routes})
    dump(out/'reader-route-map.json',readers)
    dump(out/'receipt-map.json',{k:manifest[k] for k in ('record_receipts','unit_receipts','source_receipts','receipt_semantics')})
    dump(out/'prop-needs.json',manifest['prop_needs'])
    dump(out/'route-inventory.json',{k:manifest[k] for k in ('document_routes','binding_routes','host_api','card_handoff')})
    def sc_array(name,values):return f'[{name} {len(values)}] = ['+' '.join(map(str,values))+']'
    (out/'p09-host-tables.inc').write_text('; P09-local page indices; add extension existing_pages to locate in scene arrays.\n'+'\n'.join([
        sc_array('p09RecordDocuments',[0]+[r['document_id'] for r in routes]),
        sc_array('p09UnitDocuments',[0]+[r['document_id'] for r in unit_routes]),
        sc_array('p09PageUnits',[p['speech_unit_id'] for p in pages]),
        sc_array('p09PageLastOfUnit',[int(p['last_of_unit']) for p in pages]),
        sc_array('p09PageRecordIds',[p['local_line_key'] for p in pages])])+'\n')
    entries=' '.join(str(r['entry']) for r in readers.values());headers=' '.join(str(r['header_entry']) for r in readers.values())
    (out/'reader-proof.sc').write_text(f''';;; Sierra Script 1.0 - (do not remove this comment)
(script# 0)
(public readerProof 0)
(local [body 448] [heading 104] [measure 4]
    [entries 2] = [{entries}] [headers 2] = [{headers}])
(class ReaderProof
    (properties failure 0)
    (method (readPage index)
        (if (or (< index 0) (>= index 2)) (return 0))
        (GetFarText 210 [entries index] @body)
        (GetFarText 210 [headers index] @heading)
        (return 1))
    (method (drawPage index)
        (if (not (self readPage: index)) (return 0))
        (TextSize @measure @body 0 288)
        (if (or (> [measure 2] 112) (> [measure 3] 288)) (= failure 1) (return 0))
        (TextSize @measure @heading 0 204)
        (if (> [measure 2] 8) (= failure 2) (return 0))
        (Display @heading 100 16 12 102 2 105 0 106 288 121)
        (Display @body 100 16 44 102 1 105 0 106 288 121)
        (Graph 12 0 0 200 320 1)
        (return 1)))
(instance readerProof of ReaderProof)
''')
    dump(HERE/'evidence/allocation-check.json',{'status':'PASS','text':210,'reserved_audio36_module':921,
        'document_reservation':[1100,1199],'used_record_documents':[1100,1119],'used_unit_documents':[1120,1139],
        'namespace_rule':'Independent typed resource namespaces; exact frozen current predecessor membership; docs1100-1139/Text210/Audio921 allocated by this reconstruction'})
    for path,digest in hashes.items():assert sha((HERE/path).read_bytes())==digest,path
    print(json.dumps({'coverage':manifest['coverage'],'text_bytes':len(payload),'entries':len(bank)},indent=2))
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--reuse-audio',action='store_true')
    generate(parser.parse_args().reuse_audio)
