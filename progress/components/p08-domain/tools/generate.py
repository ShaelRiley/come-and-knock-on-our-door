#!/usr/bin/env python3
"""Editable P08 lowering. Templates contain behavior; tables bind exact canon.
This is a new SCI reconstruction of literal recovered P08, not an old binary.
"""
import hashlib, json, re, sys
from pathlib import Path
H=Path(__file__).resolve().parents[1]
MODEL=H/'fixtures/reference-baseline/cakood/p08_model.py'
FIELDS={};WIDTH={}
def field(name,width=1):
 FIELDS[name]=sum(WIDTH.values());WIDTH[name]=width
for name in 'carrier_position pa_position screen_position table_position credit_position facing service_unpacked returned_padding layout_ready evening_started hint_level pending_phase'.split():field(name)
for name in 'revision request_serial pending_request_serial pending_requested_at checklist_receipt confirmed_at completed_request_serial completed_requested_at completed_checklist_receipt completed_confirmation_receipt'.split():field(name,2)
for group,keys in [('source', 'circulation_plan sightline_plan placement_symbols credit_slate'),('place','ceramic_carrier pa_kit completed_screen serving_table credit_slate pa_facing'),('once','intro unpack evening'),('owner','ceramic_carrier pa_kit completed_screen credit_slate padding'),('ack','ceramic_carrier pa_kit completed_screen credit_slate padding'),('surface','ceramic_carrier serving_table')]:
 for key in keys.split():field(group+'_'+key,2)
# R2 makes the reference ownership dictionary iteration order explicit.
field('owner_order_count')
for i in range(5):field('owner_order_'+str(i))
COUNT=sum(WIDTH.values())
OUTFIELDS={'code':0,'revision':1,'record_count':3,'records':4,'unit_count':7,'units':8,'event_count':14,'events':15}
OUTCOUNT=39;EVENTWIDTH=12
PROPS='p08Initialized p08Ready p08Busy p08Uncertain p08Loading p08LoadIndex p08ContextValid p08Room p08Apron p08Preparations p08Wins p08ClaimedFlags p08Padding p08FrankieRoom p08BunnyRoom p08Contest p08Protected p08InventoryObject p08InventoryTarget p08RecordCapacity p08UnitCapacity p08EventCapacity p08OutputFault p08CallbackReady'.split()
ARRAYS={'p08Words':COUNT,'p08Work':COUNT,'p08Load':COUNT,'p08Output':OUTCOUNT,'p08Prepared':OUTCOUNT,'p08Session':8,'p08Callback':8,'p08CallbackRevision':2}
CODES='initialized restored invalid_argument invalid_context invalid_state session_required busy storage_uncertain serial_exhausted output_full stale_session stale_handoff handoff_acknowledged preparations_required contest_active offscreen courtyard_required layout_ready inspect_state observed credit_not_displayed source_already_observed source_observed layout_state introduced occupied_object already_positioned positioned already_oriented oriented already_unpacked buffet_surface_required service_unpacked layout_dialogue layout_incomplete evening_started handoff_pending readiness_requested confirmation_pending autosave_pending no_pending_start stale_readiness stale_confirmation declined autosave_requested stale_autosave autosave_failed start_cancelled hint unhelpful'.split()
OBJECTS='ceramic_carrier pa_kit completed_screen serving_table credit_slate gate_lane buffet_position speaker_position display_alcove kitchen_hatch plan_overlay ceramic_service circulation_plan sightline_plan placement_symbols linen_hook hotpot_pot frankie bunny clean_towel clean_napkin'.split()
PREPARATIONS='PLAN_AGREED CERAMICS_READY GATE_TESTED HOLD_OPEN_AVAILABLE PA_TESTED MILO_ROLE_AGREED VC01_RESOLVED SOUND_READY SCREEN_BUILT VIVIAN_SCOPE_AGREED VC02_RESOLVED SCREEN_READY FOOD_READY'.split()
EVENTS='ownership_handoff ownership_ack source_observed intro place orient unpack readiness checklist declined autosave evening cancelled hint'.split()

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def const(k):return re.sub('[^A-Z0-9_]','_',k.upper())
def word(v):return ((v+32768)&65535)-32768
def lookup(name,arg,cases):return f'(method ({name} {arg})\n (switch {arg}\n'+''.join(f' ({k} (return {v}))\n' for k,v in cases)+') (return 0))\n'
def main(check=False):
 if sys.flags.optimize:raise RuntimeError('Optimization is forbidden')
 fixture=json.loads((H/'fixtures/canonical-bindings.json').read_text())
 authority=H/'fixtures/reference-baseline/inputs/authority'
 cat=json.loads((authority/'full-line-catalog.json').read_text());sp=json.loads((authority/'speech-units.json').read_text())
 records={r['id']:r for r in cat['records'] if r['id'].startswith('P08.')}
 units={u['line_id']:u for u in sp['units'] if u['record_id'] in records}
 if len(records)!=44 or set(records)!=set(fixture['records']):raise ValueError('Canonical record mismatch')
 for rid,r in records.items():
  us=[u for u in units.values() if u['record_id']==rid]
  expected={**{k:r[k] for k in ('text_sha256','speaker_id','source_obligations')},'speech_units':[u['line_id'] for u in us],'speech_speakers':{u['line_id']:u['speaker_id'] for u in us}}
  if fixture['records'][rid]!=expected:raise ValueError('Canonical metadata drift: '+rid)
 sys.path.insert(0,str(H/'fixtures/reference-baseline'))
 from cakood.p08_model import SCRIPT_BINDINGS
 ri={k:i for i,k in enumerate(records,1)};ui={k:i for i,k in enumerate(units,1)};oi={k:i for i,k in enumerate(OBJECTS,1)}
 # 22 is only an ownership-key discriminator, never an object/string alias.
 oi.update({k:i for i,k in enumerate((k for k in SCRIPT_BINDINGS if k not in OBJECTS),23)})
 constants={'S_'+const(k):v for k,v in FIELDS.items()};constants.update({'O_'+const(k):v for k,v in OUTFIELDS.items()});constants.update({'R_'+const(k):v for k,v in ri.items()});constants.update({'OBJ_'+const(k):v for k,v in oi.items()});constants.update({'CODE_'+const(k):i for i,k in enumerate(CODES,1)});constants.update({'EVENT_'+const(k):i for i,k in enumerate(EVENTS,1)});constants.update({'PREP_'+k:1<<i for i,k in enumerate(PREPARATIONS)})
 constants.update(STATE_WORDS=COUNT,OUTPUT_WORDS=OUTCOUNT,ENVELOPE_WORDS=COUNT+20,EVENT_WORDS=EVENTWIDTH,ALL_PREPARATIONS=8191)
 tables=''
 for name,keys in [('PositionSlot','carrier_position pa_position screen_position table_position credit_position'),('PlacementSlot','place_ceramic_carrier place_pa_kit place_completed_screen place_serving_table place_credit_slate place_pa_facing')]:
  tables+=lookup('p08'+name,'object',[(i,FIELDS[k]) for i,k in enumerate(keys.split(),1)])
 for name,prefix in [('OwnerSlot','owner'),('AckSlot','ack')]:tables+=lookup('p08'+name,'object',[(oi[k] if k!='padding' else 22,FIELDS[prefix+'_'+k]) for k in 'ceramic_carrier pa_kit completed_screen credit_slate padding'.split()])
 tables+=lookup('p08ProtectedBit','object',[(i,1<<(i-1)) for i in range(1,6)])
 tables+=lookup('p08SourceSlot','object',[(oi[k],FIELDS['source_'+k]) for k in 'circulation_plan sightline_plan placement_symbols credit_slate'.split()])
 tables+=lookup('p08SourceRecord','object',[(oi[k],ri[f'P08.READ.{i:03}']) for i,k in enumerate('circulation_plan sightline_plan placement_symbols credit_slate'.split(),1)])
 labels='gate_lane buffet_position speaker_position display_alcove serving_table kitchen_hatch plan_overlay'.split()
 tables+=lookup('p08LabelRecord','object',[(oi[k],ri[f'P08.LABEL.{i:03}']) for i,k in enumerate(labels,1)])
 tables+=lookup('p08LookRecord','object',[(oi[k],ri[f'P08.LOOK.{i:03}']) for i,k in enumerate(labels,1)]+[(oi[k],ri[f'P08.READ.{i:03}']) for i,k in enumerate('circulation_plan sightline_plan placement_symbols credit_slate'.split(),1)]+[(20,ri['P08.SYSTEM.001']),(21,ri['P08.SYSTEM.002'])])
 tables+='(method (p08LookBinding object)\n (switch object\n'
 for key,rids in SCRIPT_BINDINGS.items():
  tables+=f' ({oi[key]} '+''.join(f'(self p08AddRecord: {ri[rid]}) ' for rid in rids)+'(return 1))\n'
 tables+=') (return 0))\n'
 tables+=lookup('p08UnitCount','record',[(ri[k],len(v['speech_units'])) for k,v in fixture['records'].items()])
 tables+='(method (p08Unit record index)\n (switch record\n'
 for rid,info in fixture['records'].items():
  if info['speech_units']:tables+=f' ({ri[rid]} (switch index '+ ' '.join(f'({i} (return {ui[u]}))' for i,u in enumerate(info['speech_units']))+'))\n'
 tables+=') (return 0))\n'
 digest=sha(H/'fixtures/canonical-bindings.json');header=[20536,2,32,COUNT,*[word(int(digest[i:i+4],16)) for i in range(0,64,4)]]
 tables+=lookup('p08Header','index',enumerate(header))
 body=tables+'\n'.join(p.read_text() for p in sorted((H/'templates').glob('*.sc.in')))
 def sub(m):
  name,limb=m.group(1),m.group(2)
  return f'[p08Work {FIELDS[name]+int(limb=="L")}]'
 body=re.sub(r'@([a-zA-Z0-9_]+)(?:\.([HL]))?',sub,body)
 source=';;; Sierra Script 1.0 - (do not remove this comment)\n; NEW P08 R2 ordered-ownership reconstruction; no Main hooks, native save or presentation implementation.\n(script# 989)\n(public p08State 0)\n(local '+' '.join(f'[{k} {v}]' for k,v in ARRAYS.items())+')\n'
 source+='\n'.join(f'(define {k} {v})' for k,v in constants.items())+'\n(class P08State\n(properties\n'+'\n'.join(f' {k} 0' for k in PROPS)+'\n)\n'+body+'\n)\n(instance p08State of P08State)\n'
 manifest={'kind':'NEW P08 SCI domain reconstruction R2 ordered ownership','script':989,'species':11,'class':'P08State','instance':'p08State','export':0,'state_offsets':FIELDS,'state_widths':WIDTH,'state_words':COUNT,'arrays':ARRAYS,'properties':PROPS,'output_offsets':OUTFIELDS,'output_words':OUTCOUNT,'event_words':EVENTWIDTH,'codes':{k:i for i,k in enumerate(CODES,1)},'events':{k:i for i,k in enumerate(EVENTS,1)},'objects':oi,'padding_handoff_key':22,'raw_save_schema':2,'ownership_order_capacity':5,'ownership_order_keys':{'ceramic_carrier':1,'pa_kit':2,'completed_screen':3,'credit_slate':5,'padding':22},'preparations':{k:1<<i for i,k in enumerate(PREPARATIONS)},'records':ri,'units':ui,'rooms':{f'L{i:02}_{s}':i for i,s in enumerate(['LIVING_ROOM','KITCHEN','PORCH','SIDE_PASSAGE','COURTYARD','GARAGE','CONSERVATORY'],1)},'kitchen_pass_location':8,'header':header,'serial_max':4294967295,'model_sha256':sha(MODEL),'fixture_sha256':digest,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'new_selector_reservation':[2600,2799],'native_acceptance':False}
 payloads={'src/module989.sc':source,'manifest.json':json.dumps(manifest,indent=2)+'\n','fixtures/p08-canonical-presentation.json':json.dumps({'records':list(records.values()),'speech_units':list(units.values()),'fixture_sha256':digest},ensure_ascii=False,indent=2)+'\n'}
 for rel,data in payloads.items():
  p=H/rel
  if check:
   if p.read_text()!=data:raise ValueError('Stale generated '+rel)
  else:p.write_text(data)
if __name__=='__main__':main('--check' in sys.argv)
