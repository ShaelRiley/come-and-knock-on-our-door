from pathlib import Path
from copy import deepcopy
import importlib.util
import json
import sys
import unittest
import wave
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parents[1];SCI=HERE/'inputs/p08';ROOT=HERE/'inputs/model'
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT))
import generate
import extend_dialogue as extend
import host_contract as host
from cakood import p09_model as model

def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
from source_factory import VM
M=json.loads((HERE/'generated/manifest.json').read_text())
A=json.loads((HERE/'inputs/domain/schema.json').read_text())
C=json.loads((HERE/'generated/extension-contract.json').read_text())
CAT={r['id']:r for r in json.loads((generate.AUTHORITY/'full-line-catalog.json').read_text())['records']}
UNITS={u['line_id']:u for u in json.loads((generate.AUTHORITY/'speech-units.json').read_text())['units']}
BANK=(HERE/'generated/210.text.bin').read_bytes().split(b'\0')[:-1]

def resources():
    r={int(p.name.split('.')[0]):p.read_bytes().split(b'\0')[:-1] for p in (SCI/'inputs/resources').glob('*.text.bin')}
    r[208]=(SCI/'generated/208.text.bin').read_bytes().split(b'\0')[:-1]
    r[210]=BANK;return r

def evidence(req,index=0,**changes):
    doc,page=req['pages'][index]
    r=dict(kind='visible_graph12',source=req['source'],start_hi=0,start_lo=1,epoch=9,document=doc,page=page,
        unobscured=True,draw_succeeded=True,graph12=True,current_room=6,on_apron=False,evening_started=True,
        contest_active=False,stringer_room=6,rita_room=6,view=req['view'] or 'front',plan_agreed=True,card_available=True)
    r.update(changes);return r

def receipt(req):return host.VisibleReceipt(req,start_hi=0,start_lo=1,epoch=9)

class ExportTests(unittest.TestCase):
    def test_every_canonical_source_character_word_byte_clause_and_speaker(self):
        words=chars=0
        for route in M['routes']:
            record=CAT[route['record_id']];rebuilt=[]
            self.assertEqual(route['source_text'],record['text'])
            self.assertEqual(route['source_text_json_sha256'],record['text_sha256'])
            self.assertEqual(route['source_obligations'],record['source_obligations'])
            for si,s in enumerate(route['segments']):
                pages=[M['pages'][i] for i in route['page_indices'] if M['pages'][i]['segment_index']==si]
                raw=''.join(p['raw_text'] for p in pages)
                self.assertEqual(raw,s['source_text']);self.assertEqual(generate.sha(raw.encode()),s['source_text_sha256'])
                a=b=w=0
                for p in pages:
                    self.assertEqual((p['source_char_range'][0],p['source_utf8_byte_range'][0],p['word_range'][0]),(a,b,w))
                    a,b,w=p['source_char_range'][1],p['source_utf8_byte_range'][1],p['word_range'][1]
                    self.assertEqual(raw[slice(*p['source_char_range'])],p['raw_text'])
                    self.assertEqual(raw.encode()[slice(*p['source_utf8_byte_range'])].decode(),p['raw_text'])
                    self.assertEqual(' '.join(generate.norm(p['raw_text']).split()),' '.join(p['text'].split()))
                self.assertEqual((a,b,w),(len(raw),len(raw.encode()),len(raw.split())))
                if s['line_id']:
                    unit=UNITS[s['line_id']];self.assertEqual((raw,s['speaker_id'],s['source_speaker']),(unit['text'],unit['speaker_id'],unit['speaker']))
                rebuilt.append({'speaker':s['source_speaker'],'text':raw});words+=len(raw.split());chars+=len(raw)
            self.assertEqual(rebuilt if isinstance(record['text'],list) else rebuilt[0]['text'],record['text'])
        self.assertEqual((words,chars),(371,2051))

    def test_text210_byte_offsets_geometry_and_headers(self):
        payload=(HERE/'generated/210.text.bin').read_bytes()
        self.assertEqual(M['geometry']['font'],generate.util.font_metrics())
        for p in M['pages']:
            self.assertEqual(payload[slice(*p['text_bank_byte_range'])],p['text'].encode()+b'\0')
            self.assertEqual(generate.sha(p['text'].encode()),p['display_ascii_sha256'])
            self.assertEqual(BANK[p['entry']].decode(),p['text'])
            self.assertEqual(BANK[p['header_entry']].decode(),generate.norm(p['display_name']))
            self.assertLessEqual(len(p['text'].splitlines()),3);self.assertTrue(all(len(x)<=50 for x in p['text'].splitlines()))
            self.assertLessEqual(p['bytes_with_nul'],153);self.assertLessEqual(len(BANK[p['header_entry']])*6,204)

    def test_all_twenty_unit_documents_exact_and_independent(self):
        self.assertEqual(M['local_unit_keys'],A['speech_unit_ids'])
        self.assertEqual([u['document_id'] for u in M['unit_routes']],list(range(1120,1140)))
        for u in M['unit_routes']:
            self.assertEqual(''.join(M['pages'][i]['raw_text'] for i in u['page_indices']),UNITS[u['line_id']]['text'])
            self.assertEqual(u['canonical_speech_unit'],UNITS[u['line_id']])
            for i in u['page_indices']:
                p=M['pages'][i];original=M['pages'][p['source_record_page_index']]
                for key in ('raw_text','entry','header_entry','speaker_number','voice_index','duration_ticks','last_of_unit'):
                    self.assertEqual(p[key],original[key])
                self.assertEqual(p['fields'][1],u['document_id'])
            self.assertTrue(M['pages'][u['page_indices'][-1]]['last_of_unit'])

    def test_all_speech_formats_hashes_finite_sync_and_exact_metadata(self):
        self.assertEqual(len(M['speech']),20);self.assertEqual(M['missing_speech'],[])
        self.assertEqual({v['line_id'] for v in M['speech']},{u for u in UNITS if u.startswith('P09.')})
        for v in M['speech']:
            self.assertEqual(v['canonical_speech_unit'],UNITS[v['line_id']])
            self.assertEqual(v['laugh_opportunity'],UNITS[v['line_id']]['laugh_opportunity'])
            audio=HERE/'generated/speech'/v['audio_file'];sync=HERE/'generated/speech'/v['sync_file']
            self.assertEqual(generate.sha(audio.read_bytes()),v['audio_sha256']);self.assertEqual(generate.sha(sync.read_bytes()),v['sync_sha256'])
            self.assertEqual(v['audio_file'],generate.util.talk.patch_name(921,v['voice_index']))
            with wave.open(str(audio)) as wav:
                self.assertEqual((wav.getnchannels(),wav.getsampwidth(),wav.getframerate()),(1,2,22050))
                self.assertEqual(wav.getnframes(),round(v['duration_ticks']*22050/60))
            plan=generate.util.talk.schedule(v['fragment_id'],v['speaker_id'],v['raw_text'])
            self.assertEqual(generate.util.talk.sync_patch(plan),sync.read_bytes());self.assertEqual(plan['mouth_events'],v['mouth_events'])
            self.assertLessEqual(v['duration_ticks'],1800)
            self.assertEqual(v['mouth_events'][-1],{'tick':v['duration_ticks'],'pose':0})
        self.assertEqual({p.name for p in (HERE/'generated/speech').iterdir()},{v[k] for v in M['speech'] for k in ('audio_file','sync_file')})

    def test_local_original_profiles_reproduce_pcm(self):
        for speaker in ('jack','stringer','rita'):
            v=next(v for v in M['speech'] if v['speaker_id']==speaker)
            plan=generate.util.talk.schedule(v['fragment_id'],speaker,v['raw_text'])
            self.assertEqual(generate.sha(generate.util.talk.render(plan)),v['audio_sha256'])

    def test_nonspoken_material_stays_silent(self):
        for route in M['routes']:
            if route['kind'] in ('read','choice','label','inventory','hint'):
                for i in route['page_indices']:
                    p=M['pages'][i];self.assertEqual((p['voice_index'],p['audio_module'],p['duration_ticks']),(0,0,0));self.assertIsNone(p['line_id'])

    def test_protected_inputs_and_resource_hash_unchanged(self):
        for path,digest in M['protected_inputs_sha256'].items():self.assertEqual(generate.sha((HERE/path).read_bytes()),digest,path)
        self.assertEqual(generate.sha((HERE/'generated/210.text.bin').read_bytes()),M['text_resource_sha256'])

    def test_prior_arrays_methods_and_routes_preserved(self):
        before=(HERE/'snapshot/module982-input.sc').read_text();after=(HERE/'generated/module982.sc').read_text()
        for name in extend.ARRAYS:self.assertEqual(extend.read_array(after,name)[:len(extend.read_array(before,name))],extend.read_array(before,name))
        old=VM(HERE/'snapshot/module982-input.sc','SceneDialogue');new=VM(HERE/'generated/module982.sc','SceneDialogue')
        for name in old.methods:
            if name not in ('sdRoute','sdPageCount','sdLoad','hStaticAt'):self.assertEqual(old.methods[name],new.methods[name])
        for doc in range(C['existing_document_slots']):
            self.assertEqual(old.call('sdRoute',doc),new.call('sdRoute',doc));self.assertEqual(old.call('sdPageCount',doc),new.call('sdPageCount',doc))
        self.assertEqual((C['existing_pages'],C['added_pages'],C['total_pages']),(1138,53,1191))

    def test_extension_rejects_reapply_missing_bank_and_route_collision(self):
        before=(HERE/'snapshot/module982-input.sc').read_text()
        with self.assertRaises(AssertionError):extend.apply_source((HERE/'generated/module982.sc').read_text())
        values=extend.read_array(before,'sdTextResources');values=[207 if x==208 else x for x in values]
        with self.assertRaises(AssertionError):extend.apply_source(extend.replace_array(before,'sdTextResources',values))
        values=extend.read_array(before,'sdPageData');values[1]=1100
        with self.assertRaises(AssertionError):extend.apply_source(extend.replace_array(before,'sdPageData',values))

    def test_every_new_page_draws_complete_exact_caption(self):
        res=resources();d=VM(HERE/'generated/module982.sc','SceneDialogue',res)
        a=VM(generate.BASELINE/'src/module980.sc','PresentationAudio',res)
        for route in M['document_routes']:
            self.assertEqual(d.call('sdPageCount',route['document_id']),route['page_count'])
            self.assertTrue(d.call('sdOpen',route['document_id'],0,0,0,a))
            for n,i in enumerate(route['page_indices']):
                if n:self.assertTrue(d.call('sdTurn',1,a))
                self.assertTrue(d.call('sdDraw',0));p=M['pages'][i]
                self.assertEqual(d.arrays['sdTextBuffer'],p['text'])
                self.assertEqual((d.p['sdResource'],d.p['sdLineKey'],d.p['sdVoice'],d.p['sdSpeaker']),(210,route['document_id'],p['voice_index'],p['speaker_number']))

    def test_voice_uses921_and_muted_clock911_after_visible_barrier(self):
        res=resources();d=VM(HERE/'generated/module982.sc','SceneDialogue',res)
        a=VM(generate.BASELINE/'src/module980.sc','PresentationAudio',res)
        for muted in (0,1):
            a.p['voiceMuted']=muted
            for u in M['unit_routes']:
                d.call('sdOpen',u['document_id'],0,0,0,a);g=d.p['sdGeneration']
                self.assertEqual(d.call('sdPresented',g,0,a.p['token']),0)
                d.call('sdDraw',0);self.assertEqual(d.call('sdPresented',g,0,a.p['token']),1)
                self.assertGreater(d.call('sdSpeak',a,g,0),0)
                starts=[args for op,args in a.kernel if op=='DoAudio' and args[0]==2]
                self.assertEqual(starts[-1][1],911 if muted else 921)

    def test_complete_readers_exact_and_fit(self):
        vm=VM(HERE/'generated/reader-proof.sc','ReaderProof',resources())
        for n,r in enumerate(M['readers'].values()):
            self.assertEqual(r['raw_text'],CAT[r['record_id']]['text'])
            self.assertEqual(' '.join(r['text'].split()),' '.join(generate.norm(r['raw_text']).split()))
            self.assertLessEqual(len(r['text'].splitlines()),14)
            self.assertEqual(vm.call('drawPage',n),1);self.assertEqual(vm.arrays['body'],r['text'])
        self.assertEqual(vm.call('drawPage',2),0);self.assertEqual(vm.call('drawPage',-1),0)

    def test_domain_maps_sources_tokens_and_unsigned_card_exact(self):
        self.assertEqual(M['local_line_keys'],A['line_ids']);self.assertEqual(M['domain_bindings'],A['bindings'])
        for source,r in M['source_receipts'].items():
            self.assertEqual(r['canonical_tokens'],[x['token'] for x in A['receipts'][source]])
            self.assertEqual(r['record_ids'],list(model.SOURCE_BINDINGS[source]))
        self.assertEqual(M['card_handoff'],A['card_handoff']);self.assertFalse(M['card_handoff']['signed']);self.assertIsNone(M['card_handoff']['repair_date'])

    def test_whole_record_needs_all_pages_and_exact_lease(self):
        req=host.requirements('terms',record_id='P09.DIALOGUE.002');r=receipt(req)
        for n in range(len(req['pages'])):
            self.assertIsNone(r.acknowledgment());self.assertTrue(r.observe(**evidence(req,n)))
        self.assertEqual(r.acknowledgment(),(7,0,1,9,10,0,0))
        for changes in ({'epoch':8},{'start_lo':2},{'source':'direct_question'},{'kind':'audio_complete'},
                        {'unobscured':False},{'draw_succeeded':False},{'graph12':False},{'document':1116},
                        {'current_room':4},{'on_apron':True},{'evening_started':False},{'contest_active':True},
                        {'stringer_room':4},{'plan_agreed':False},{'epoch':True}):
            self.assertFalse(receipt(req).observe(**evidence(req,**changes)),changes)
        r.cancel();self.assertIsNone(r.acknowledgment())

    def test_all_four_earliest_correction_routes(self):
        pairs=(('chairs','P09.LOOK.001.01'),('direct_question','P09.DIALOGUE.001.01'),
               ('front_context','P09.DIALOGUE.001.01'),('accusation','P09.FAILURE.001.01'))
        for source,unit in pairs:
            for mode in ('unit_document','record_pages'):
                req=host.requirements(source,unit_ids=(unit,),unit_mode=mode);r=receipt(req)
                for n in range(len(req['pages'])):self.assertTrue(r.observe(**evidence(req,n)))
                self.assertEqual(r.acknowledgment()[4:],(0,A['speech_unit_ids'][unit],A['speech_unit_ids'][unit]))
        req=host.requirements('chairs',record_id='P09.LOOK.001')
        self.assertTrue(receipt(req).observe(**evidence(req,stringer_room=4,rita_room=4)))

    def test_restricted_accusation_and_absent_rita(self):
        with self.assertRaises(ValueError):host.requirements('accusation',record_id='P09.FAILURE.001',variant='stringer_only')
        with self.assertRaises(ValueError):host.requirements('accusation',unit_ids=('P09.FAILURE.001.02',),variant='stringer_only')
        req=host.requirements('accusation',unit_ids=('P09.FAILURE.001.01',),variant='stringer_only')
        self.assertTrue(receipt(req).observe(**evidence(req,rita_room=4)))
        req=host.requirements('accusation',unit_ids=('P09.FAILURE.001.02',))
        self.assertFalse(receipt(req).observe(**evidence(req,rita_room=4)))

    def test_terms_success_separate_and_success_resumes_elsewhere(self):
        units=tuple(M['receipt_semantics']['terms_grant_units'])+('P09.SUCCESS.001.01',)
        with self.assertRaises(ValueError):host.requirements('terms',unit_ids=units)
        req=host.requirements('terms',record_id='P09.SUCCESS.001')
        self.assertTrue(receipt(req).observe(**evidence(req,current_room=4,stringer_room=0,plan_agreed=False)))
        self.assertFalse(receipt(req).observe(**evidence(req,card_available=False)))

    def test_view_and_optional_shared_wish_speaker_gates(self):
        for source,rid,wrong in (('intro','P09.OPEN.001','front'),('front_context','P09.DIALOGUE.001','side')):
            req=host.requirements(source,record_id=rid)
            self.assertFalse(receipt(req).observe(**evidence(req,view=wrong)))
        req=host.requirements('shared_wish',record_id='P09.DIALOGUE.003')
        self.assertFalse(receipt(req).observe(**evidence(req,rita_room=4)))

    def test_cross_source_unknown_out_of_order_and_typed_ids_rejected(self):
        cases=(dict(source='chairs',record_id='P09.CHOICE.001'),dict(source='chairs',unit_ids=('P09.DIALOGUE.001.01',)),
               dict(source='direct_question',unit_ids=('P09.DIALOGUE.001.03','P09.DIALOGUE.001.01')),
               dict(source='direct_question',unit_ids=('P09.DIALOGUE.001.01','P09.DIALOGUE.001.03')),
               dict(source='chairs',record_id='P09.LOOK.001',unit_ids=('P09.LOOK.001.01',)))
        for args in cases:
            with self.assertRaises(ValueError):host.requirements(**args)
        for value in (True,0,21,'1'):
            with self.assertRaises(ValueError):host.route(value)
        self.assertTrue(host.result_plan()['empty_status_is_unbound'])
        self.assertEqual(host.result_plan(lines=(4,),units=(7,))['documents'],[1103,1126])


if __name__=='__main__':unittest.main()
