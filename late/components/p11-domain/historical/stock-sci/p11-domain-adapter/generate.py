#!/usr/bin/env python3
"""Original isolated stock SCI1.1 P11 adapter; numeric canonical bindings only."""
from pathlib import Path
import ast,hashlib,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from cakood import p11_model as model
from cakood.p02_model import ROOMS
SOURCES={x:i+1 for i,x in enumerate(model.P11World.SOURCES)}
STATE_SERIALS={'Revision':'revision','FirstLift':'first_lift_at','Lift':'lift_at','Catch':'catch_at','Fold':'fold_at','Stage':'stage_at','PegRequest':'peg_request_at','PegAck':'peg_ack_at','AdvancePeg':'advance_peg_at','ContestRequest':'contest_request_at','Laugh':'laugh_at'}
SERIALS=list(STATE_SERIALS)+[x.title()+'Start' for x in SOURCES]
RECEIPTS={}
for source in SOURCES:
 RECEIPTS[source]=[]
 for i,token in enumerate(model.P11World()._tokens(source)):
  RECEIPTS[source].append({'slot':len(SERIALS),'token':token});SERIALS.append(source.title()+'Receipt'+str(i+1))
PROPS=dict.fromkeys(['p11Initialized','p11HintLevel','p11Phase']+['p11'+n+l for n in SERIALS for l in ('Hi','Lo')],0)
PERSISTED=list(PROPS)
PROPS.update(dict.fromkeys(['p11'+p for p in ('ContextValid','Room','Apron','Evening','Rumor','Terms','Cues','FelixRoom','BunnyRoom','FrankieRoom','RitaRoom','CartRoom','DisplayRoom','ContestActive','ClaimReady','Resolved','GateTested','GateAvailable','GateEngaged','GateOpen','Wedge','Epoch','Code','LineCount','UnitCount','EventCount','ResultHi','ResultLo','PresentationSource','PresentationHi','PresentationLo')],0))
CODES={name:i+1 for i,name in enumerate(('p09_and_p10_required','offscreen','contest_active','rescue_not_started','initial_concern_finished','supported_scene_finished','display_not_folded','display_not_staged','speaker_absent','already_supported','already_folded','felix_required','existing_cart_and_display_required','tested_gate_required','display_supported','already_safe','display_back_on_cart','support_required','bunny_at_porch_required','gate_already_pegged','peg_request_pending','peg_requested','stale_peg_request','helper_unavailable','peg_not_yet_engaged','peg_acknowledged','frankie_at_courtyard_required','catch_already_released','catch_released','peg_required','catch_required','display_folded_safe','already_staged','safe_fold_required','display_staged','display_safe','fold_do_not_force','look','no_p11_description','rescue_and_conversation_required','contest_request_pending','contest_requested','stale_contest_request','contest_handoff_unavailable','contest_request_cancelled','contest_request_acknowledged','laugh_already_consumed','protected_scene','earned_physical_reaction','hint','no_p11_action','presentation_not_started','presentation_complete','presentation_pending','presentation_already_acknowledged','presentation_acknowledged','stale_presentation','invalid_argument','invalid_context','invalid_state','serial_exhausted'))}
EVENTS={name:i+1 for i,name in enumerate(('P11_PRESENTATION_QUEUED','P11_PRESENTED','P11_LIFT','P11_SET_BACK','P11_PEG_REQUEST','P11_PEG_ACK','P11_CATCH_RELEASED','P11_FOLD','P11_STAGED','P11_VC03_REQUEST','P11_VC03_ACK','LAF11','P11_HINT'))}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(name,arg,mapping,default=0):
 return f'(method ({name} {arg} &tmp answer)\n (= answer {default})\n (switch {arg}\n'+''.join(f' ({k} (= answer {v}))\n' for k,v in mapping.items())+') (return answer))\n'
def main():
 fixture=json.loads((ROOT/'tests/fixtures/p11/canonical-bindings.json').read_text());registry=json.loads((ROOT/'docs/native-resource-registry.json').read_text())
 assert 'P11State species15' in registry['scripts']['993'];assert 'P11' in registry['object_id_reservations']['415-418']
 assert all('P11' in owner for bounds,owner in registry['object_id_reservations'].items() if any(int(bounds.split('-')[0]) <= x <= int(bounds.split('-')[-1]) for x in range(415,419)))
 authority=Path('/workspace/shared/cakood/full-script/CURRENT-SCRIPT-REVISION.json');current=json.loads(authority.read_text())
 assert fixture['catalog_sha256']==current['catalog_sha256'] and current['editorial_revision']==3
 assert sha(authority.parent/current['catalog'])==current['catalog_sha256'];assert sha(authority.parent/current['speech'])==fixture['speech_sha256']
 assert set(fixture['records'])==set(model.RECORD_UNITS)
 assert {u['line_id']:u['speaker_id'] for u in fixture['speech_units']}==model.UNIT_SPEAKERS
 for record,units in model.RECORD_UNITS.items():assert tuple(u['line_id'] for u in fixture['speech_units'] if u['record_id']==record)==units
 objects=json.loads((HERE.parent/'p10-domain-adapter/manifest.json').read_text())['objects']
 own=dict(zip(('display_wing','wing_catch','display_handle','staging_pocket'),range(415,419)))
 assert not set(own.values())&set(objects.values());objects.update(own)
 lines={name:i+1 for i,name in enumerate(fixture['records'])};units={x['line_id']:i+1 for i,x in enumerate(fixture['speech_units'])}
 tokens={t:i+1 for i,t in enumerate(dict.fromkeys(x['token'] for rs in RECEIPTS.values() for x in rs))}
 constants=[]
 for prefix,values in (('OBJ',objects),('CODE',CODES),('EVENT',EVENTS),('SOURCE',SOURCES),('LINE',lines),('UNIT',units),('TOKEN',tokens)):
  constants += [f'(define {prefix}_{k.upper().replace(".","_")} {v})' for k,v in values.items()]
 constants += [f'(define ROOM_{k} {v.number})' for k,v in ROOMS.items()]
 generated=''
 for limb in ('Hi','Lo'):generated+=table('p11Serial'+limb,'slot',{i:'p11'+n+limb for i,n in enumerate(SERIALS)})
 generated+='(method (p11SetSerial slot hi lo)\n (switch slot\n'+''.join(f' ({i} (= p11{n}Hi hi) (= p11{n}Lo lo))\n' for i,n in enumerate(SERIALS))+') (return 1))\n'
 generated+=table('p11Capacity','source',{SOURCES[s]:len(rs) for s,rs in RECEIPTS.items()})
 generated+=table('p11ReceiptBase','source',{SOURCES[s]:rs[0]['slot'] for s,rs in RECEIPTS.items()})
 generated+=table('p11SourceRecord','source',{SOURCES[s]:lines[model.P11World.SOURCES[s]] for s in SOURCES})
 generated+='(method (p11Token source index &tmp answer)\n (= answer 0) (switch source\n'
 for s,rs in RECEIPTS.items():generated+=f' ({SOURCES[s]} (switch index '+''.join(f' ({i} (= answer {tokens[r["token"]]}))' for i,r in enumerate(rs))+'))\n'
 generated+=') (return answer))\n'
 generated+=table('p11TokenUnit','token',{v:units.get(k,0) for k,v in tokens.items()})
 generated+=table('p11TokenSpeaker','token',{v:objects.get(model.UNIT_SPEAKERS.get(k,''),0) for k,v in tokens.items()})
 generated+='(method (p11ContextItem obj &tmp valid)\n (if (not p11ContextValid) (return 0)) (= valid 0) (switch obj\n'
 allowed={name:id for name,id in objects.items() if name not in model.FIXED_OBJECTS}
 for id in sorted(set(allowed.values())):generated+=f' ({id} (= valid 1))\n'
 generated+=') (if valid (return 1)) (= p11ContextValid 0) (self p11Clear:) (= p11Code CODE_INVALID_CONTEXT) (return 0))\n'
 source=';;; Sierra Script 1.0 - (do not remove this comment)\n; Original isolated P11 domain adapter. Canonical IDs only; no campaign mutation.\n(script# 993)\n(public p11State 0)\n(local [p11Lines 3] [p11Units 6] [p11Events 2] [p11EventArgs 8] [p11EventHi 2] [p11EventLo 2] [p11Lease 9])\n'+'\n'.join(constants)+'\n'+f'(define P11_SERIAL_COUNT {len(SERIALS)})\n(define P11_LINE_LIMIT {len(lines)})\n(class P11State\n(properties\n'+'\n'.join(f' {k} {v}' for k,v in PROPS.items())+'\n)\n'+generated+(HERE/'src/methods.sc.in').read_text()+'\n)\n(instance p11State of P11State)\n'
 (HERE/'src/module993.sc').write_text(source)
 manifest=dict(scope='Original isolated SCI1.1 domain adapter; native and host integration pending',script=993,export=0,export_name='p11State',standalone_species=1,production_reserved_species=15,objects=objects,own_objects=own,external_inventory_ids=allowed,topic_targets={'peg':1,'catch':2,'contest':3,'sincere':4},rooms={k:v.number for k,v in ROOMS.items()},sources=SOURCES,codes=CODES,events=EVENTS,line_ids=lines,speech_unit_ids=units,tokens=tokens,serials=SERIALS,state_serials=STATE_SERIALS,source_start_offset=10,receipts=RECEIPTS,source_bindings=model.P11World.SOURCES,persisted_properties=PERSISTED,all_properties=PROPS,max_serial=1073741823,serial_limb_base=32768,native_representability={"supported_revision_max":1073741822,"regular_supported_mutation_reserve":2,"safe_release_reserve":1,"model_integers":"unbounded; only this native transport imposes capacity"},line_capacity=3,speech_unit_capacity=6,event_capacity=2,event_arg_capacity=4,model_sha256=sha(ROOT/'cakood/p11_model.py'),fixture_sha256=sha(ROOT/'tests/fixtures/p11/canonical-bindings.json'),registry_sha256=sha(ROOT/'docs/native-resource-registry.json'),source_sha256=sha(HERE/'src/module993.sc'),authority_sha256=sha(authority),gdd_sha256=sha(Path('/workspace/shared/cakood/ending-seam-20261005/current-gdd.txt')),contest_contract_sha256=sha(Path('/workspace/shared/cakood/verbal-competitions-update/CANONICAL-CONTRACT.md')),speech_metadata=fixture['speech_units'],display_handoff=dict(display_id='folded_display',cart_id='handcart',location=model.SIDE_PASSAGE,position='staging_pocket',folded=True,padded=True,covered=True,undamaged=True,panel_revealed=False,transport_owner='P13',rita_reveal_consent=False,shared_helpers=['jack','felix','bunny','frankie']))
 (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(f'Generated script993: {len(source)} bytes; {len(SERIALS)} serials; {len(lines)} records')
if __name__=='__main__':main()
