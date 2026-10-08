#!/usr/bin/env python3
"""Source, emitted namespace/segments, frozen art and inactive gate audit."""
from pathlib import Path
import json,struct,sys
H=Path(__file__).resolve().parent;F=H/'frozen/foundation';sys.path.insert(0,str(H/'tools'))
from source_tools import methods
from derive import derive,sha,dump,require,array
from extract_sci11 import extract
from measure import measure
def audit():
 derive(check=True);pixels=measure();B=H/'build/coherent'
 receipt=json.loads((B/'compile-receipt.json').read_text());prior=json.loads((F/'build/coherent/compile-receipt.json').read_text())
 require(receipt['status']=='PASS_FRESH_COMPILE','Fresh compile required')
 olds={r['module']:r for r in prior['modules']};modules=[];exact=[]
 for row in receipt['modules']:
  n=row['module'];src=H/'src'/('main.sc' if not n else f'module{n}.sc');scr=B/f'compiled/{n}.scr.bin';hep=Path(str(scr)+'.hep')
  require((sha(src),sha(scr),sha(hep))==(row['source_sha256'],row['script_sha256'],row['heap_sha256']),'Changed compiled program')
  layout=extract(scr,hep,B/'selector-list.json')
  total=scr.stat().st_size+hep.stat().st_size+(2 if scr.stat().st_size&2 else 0)
  require(total==row['combined_bytes'] and total<=65535,'Segment capacity')
  modules.append({'module':n,'script_bytes':scr.stat().st_size,'heap_bytes':hep.stat().st_size,'alignment_bytes':2 if scr.stat().st_size&2 else 0,'combined_bytes':total,'headroom':65535-total,'class_species':row['class_species']})
  if all(row[k]==olds[n][k] for k in ('script_sha256','heap_sha256')):exact.append(n)
  if n==990:
   cls=next(o for o in layout['objects'] if o['is_class']);inst=next(o for o in layout['objects'] if o['name']=='p09State')
   require(cls['species']==12 and inst['superclass']==12 and layout['exports']==[inst['heap_offset']],'P09 production identity')
   require(len(cls['methods'])==67 and layout['locals_word_count']==699,'Expected 64+3 methods and619+80 locals')
 require(exact==[980,981,982,983,984,985,986,987,988,989],'Unexpected earlier emitted drift')
 before=json.loads((F/'selectors.json').read_text());now=json.loads((H/'selectors.json').read_text())
 require(all(now[n]==v for n,v in before.items()),'Prior selector changed')
 new={n:v for n,v in now.items() if n not in before};require(new=={'h9Geo':3164,'h9Label':3165,'h9UI':3166},'New allocation drift')
 require(sum(len(n)+2 for n in new)==22 and len(set(now.values()))==len(now),'Selector name/collision budget')
 blob=(B/'verification-checkpoint/assets/resources/997.vocab.bin').read_bytes();require(len(blob)==37616 and struct.unpack_from('<H',blob)[0]==4103,'Vocab budget/boundary')
 for name,value in now.items():
  pos=struct.unpack_from('<H',blob,2+2*value)[0];size=struct.unpack_from('<H',blob,pos)[0];require(blob[pos+2:pos+2+size].decode()==name,'Vocab link '+name)
 mm=methods((H/'src/module990.sc').read_text());old=methods((F/'src/module990.sc').read_text())
 require(all(mm[n]==v for n,v in old.items()) and len(old)==64,'Accepted domain/foundation method drift')
 require(mm['h9Active']=='(method (h9Active) (return 0))','Activation opened')
 require(not any(x in mm['h9UI'] for x in ('p09Context:','p09Act:','p09Begin:','p09Acknowledge:','h9Active: 1')),'Presentation grants P09 state')
 require('(and (== mode 0) (not (c h8EveningReady:)))' in mm['h9UI'],'Persistent/current availability conflated')
 require('h8ActorRoom: 4' in mm['h9UI'] and 'h8ActorRoom: 7' in mm['h9UI'],'Actual cast bridge missing')
 base_main=methods((F/'src/main.sc').read_text());main=methods((H/'src/main.sc').read_text())
 delta=json.loads((H/'INTEGRATION-DELTA.json').read_text())
 require({n for n in main if main[n]!=base_main[n]}==set(delta['changed_main_methods']),'Unexpected Main method delta')
 for name in ['campaignHeld','campaignReachable','p02ObjectLocation','p02SyncInventory','p03HostReservation','bridgeActAtArrival']:
  require(main[name]==base_main[name],'High-ID/dispatch guard changed '+name)
 require(main['uiHit']==base_main['uiHit'] and main['uiInput']==base_main['uiInput'],'Existing click semantics changed')
 resources=B/'verification-checkpoint/assets/resources';oldres=F/'build/coherent/verification-checkpoint/assets/resources'
 require({p.name for p in resources.iterdir()}=={p.name for p in oldres.iterdir()},'Unexpected resource allocation')
 require(all(sha(p)==sha(oldres/p.name) for p in resources.iterdir() if p.name!='997.vocab.bin'),'Original resource changed')
 for file in (F/'frozen/scene/generated/speech').iterdir():require(sha(file)==json.loads((F/'INPUT-SEAL.json').read_text())[str(file.relative_to(F))],'Audio prefix/resource drift')
 closure=json.loads((H/'toolchain/SOURCE-MANIFEST.json').read_text())['files'];require(len(closure)==198,'Compiler closure count')
 for name,digest in closure.items():require(sha(H/'toolchain/source'/name)==digest,'Compiler source closure drift')
 result={'status':'PASS','active_p09':False,'native_acceptance':False,'modules':modules,'byte_identical_prior_modules':exact,'unchanged_prior990_methods':64,'literal_domain_methods':61,'new_methods':new,'vocab997_bytes':len(blob),'new_name_string_bytes':22,'new_resource_ids':[],'new_saved_properties':[],'new_viewpoint_state':False,'new_static_local_words':80,'geometry_is_not_progress':True,'all_original_art_font_palette_bytes_preserved':True,'all_high_id_guards_preserved':True,'measurements_sha256':sha(H/'evidence/MEASUREMENTS.json'),'jackie_poses_measured':pixels['jackie_pose_count'],'historical_front_max_actor_overlap_pixels':pixels['approaches']['historical_front']['maximum_actor_overlap'],'limits':['Render/control positive branch remains deliberately unreachable in the actual campaign','Static decoded pixels are not native screenshots','View arrival/source receipts/card publication/native validation are later gates']}
 dump(H/'evidence/static-audit.json',result);return result
if __name__=='__main__':print(json.dumps(audit(),indent=2))
