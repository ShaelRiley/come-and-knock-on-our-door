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

from cakood import p11_model as model

def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
from source_factory import VM
M=json.loads((HERE/'generated/manifest.json').read_text())
A=json.loads((HERE/'inputs/domain/schema.json').read_text())
C=json.loads((HERE/'generated/extension-contract.json').read_text())
CAT={r['id']:r for r in json.loads((generate.AUTHORITY/'full-line-catalog.json').read_text())['records']}
UNITS={u['line_id']:u for u in json.loads((generate.AUTHORITY/'speech-units.json').read_text())['units']}
BANK=(HERE/'generated/212.text.bin').read_bytes().split(b'\0')[:-1]

def resources():
    r={int(p.name.split('.')[0]):p.read_bytes().split(b'\0')[:-1] for p in (SCI/'inputs/resources').glob('*.text.bin')}
    r[208]=(SCI/'generated/208.text.bin').read_bytes().split(b'\0')[:-1]
    r[212]=BANK;return r

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
        self.assertEqual((words,chars),(532,2828))

    def test_text212_byte_offsets_geometry_and_headers(self):
        payload=(HERE/'generated/212.text.bin').read_bytes()
        self.assertEqual(M['geometry']['font'],generate.util.font_metrics())
        for p in M['pages']:
            self.assertEqual(payload[slice(*p['text_bank_byte_range'])],p['text'].encode()+b'\0')
            self.assertEqual(generate.sha(p['text'].encode()),p['display_ascii_sha256'])
            self.assertEqual(BANK[p['entry']].decode(),p['text'])
            self.assertEqual(BANK[p['header_entry']].decode(),generate.norm(p['display_name']))
            self.assertLessEqual(len(p['text'].splitlines()),3);self.assertTrue(all(len(x)<=50 for x in p['text'].splitlines()))
            self.assertLessEqual(p['bytes_with_nul'],153);self.assertLessEqual(len(BANK[p['header_entry']])*6,204)

    def test_all36_unit_documents_exact_and_independent(self):
        self.assertEqual(M['local_unit_keys'],A['speech_unit_ids'])
        self.assertEqual([u['document_id'] for u in M['unit_routes']],list(range(1326,1362)))
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
        self.assertEqual(len(M['speech']),47);self.assertEqual(M['missing_speech'],[])
        self.assertEqual({v['line_id'] for v in M['speech']},set(A['speech_unit_ids'])|{'VC03.WIN.01','VC03.WIN.02','VC03.LOSS.01','VC03.LOSS.02'})
        for v in M['speech']:
            self.assertEqual(v['canonical_speech_unit']['speaker_id'],UNITS[v['line_id']]['speaker_id'])
            self.assertEqual(v['laugh_opportunity'],UNITS[v['line_id']]['laugh_opportunity'])
            audio=HERE/'generated/speech'/v['audio_file'];sync=HERE/'generated/speech'/v['sync_file']
            self.assertEqual(generate.sha(audio.read_bytes()),v['audio_sha256']);self.assertEqual(generate.sha(sync.read_bytes()),v['sync_sha256'])
            self.assertEqual(v['audio_file'],generate.util.talk.patch_name(923,v['voice_index']))
            with wave.open(str(audio)) as wav:
                self.assertEqual((wav.getnchannels(),wav.getsampwidth(),wav.getframerate()),(1,2,22050))
                self.assertEqual(wav.getnframes(),round(v['duration_ticks']*22050/60))
            plan=generate.util.talk.schedule(v['fragment_id'],v['speaker_id'],v['raw_text'])
            self.assertEqual(generate.util.talk.sync_patch(plan),sync.read_bytes());self.assertEqual(plan['mouth_events'],v['mouth_events'])
            self.assertLessEqual(v['duration_ticks'],1800)
            self.assertEqual(v['mouth_events'][-1],{'tick':v['duration_ticks'],'pose':0})
        self.assertEqual({p.name for p in (HERE/'generated/speech').iterdir()},{v[k] for v in M['speech'] for k in ('audio_file','sync_file')})

    def test_local_original_profiles_reproduce_pcm(self):
        for speaker in ('jack','bunny','felix','frankie'):
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
        self.assertEqual(generate.sha((HERE/'generated/212.text.bin').read_bytes()),M['text_resource_sha256'])

    def test_prior_arrays_methods_and_routes_preserved(self):
        before=(HERE/'snapshot/module982-input.sc').read_text();after=(HERE/'generated/module982.sc').read_text()
        for name in extend.ARRAYS:self.assertEqual(extend.read_array(after,name)[:len(extend.read_array(before,name))],extend.read_array(before,name))
        old=VM(HERE/'snapshot/module982-input.sc','SceneDialogue');new=VM(HERE/'generated/module982.sc','SceneDialogue')
        for name in old.methods:
            if name not in ('sdRoute','sdPageCount','sdLoad','hStaticAt'):self.assertEqual(old.methods[name],new.methods[name])
        for doc in range(C['existing_document_slots']):
            self.assertEqual(old.call('sdRoute',doc),new.call('sdRoute',doc));self.assertEqual(old.call('sdPageCount',doc),new.call('sdPageCount',doc))
        self.assertEqual((C['existing_pages'],C['added_pages'],C['total_pages']),(1241,103,1344))

    def test_extension_rejects_reapply_missing_bank_and_route_collision(self):
        before=(HERE/'snapshot/module982-input.sc').read_text()
        with self.assertRaises(AssertionError):extend.apply_source((HERE/'generated/module982.sc').read_text())
        values=extend.read_array(before,'sdTextResources');values=[207 if x==208 else x for x in values]
        with self.assertRaises(AssertionError):extend.apply_source(extend.replace_array(before,'sdTextResources',values))
        values=extend.read_array(before,'sdPageData');values[1]=1300
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
                self.assertEqual((d.p['sdResource'],d.p['sdLineKey'],d.p['sdVoice'],d.p['sdSpeaker']),(212,route['document_id'],p['voice_index'],p['speaker_number']))

    def test_voice_uses923_and_muted_clock911_after_visible_barrier(self):
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
                self.assertEqual(starts[-1][1],911 if muted else 923)

    def test_exact_domain_bindings_source_tokens_and_original_controls(self):
        self.assertEqual(M['local_line_keys'],A['line_ids']);self.assertEqual(M['local_unit_keys'],A['speech_unit_ids'])
        self.assertEqual(M['source_bindings'],model.P11World.SOURCES)
        for source,row in M['source_receipts'].items():
            self.assertEqual(row['record_ids'],[model.P11World.SOURCES[source]])
            self.assertEqual(row['canonical_tokens'],[v['token'] for v in A['receipts'][source]])
        self.assertEqual(M['ownership_contract']['original_controls'],A['own_objects'])
        self.assertEqual(M['ownership_contract']['original_display'],42)
        self.assertEqual(M['ownership_contract']['original_cart'],72)
        self.assertEqual(set(M['silent_readers']),set())
        self.assertEqual(M['host_api']['domain_production_reserved_species'],15)

if __name__=='__main__':unittest.main()
