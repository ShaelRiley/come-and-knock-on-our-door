#!/usr/bin/env python3
"""NEW portable adaptation of retained generator for finite SOURCE comparison."""
from pathlib import Path
import hashlib,json,re,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from cakood import p12_model as model
from cakood.p02_model import ROOMS
from cakood.p10_model import CUE_IDS,ORDER
SOURCES={x:i+1 for i,x in enumerate(model.P12World.SOURCES)}
SERIALS=['Revision','Handoff','Release','Face','Intro','Confetti','Laugh','Collection']+[x.title().replace('_','')+'Start' for x in SOURCES]
RECEIPTS={}
for source in SOURCES:
 RECEIPTS[source]=[]
 for i,token in enumerate(model.P12World()._tokens(source)):
  RECEIPTS[source].append({'slot':len(SERIALS),'token':token});SERIALS.append(source.title().replace('_','')+'Receipt'+str(i+1))
PROPS=dict.fromkeys(['p12Initialized']+['p12Slot'+str(i) for i in range(3)]+['p12Word'+str(i) for i in range(6)]+['p12'+n+l for n in SERIALS for l in ('Hi','Lo')],0)
PERSISTED=list(PROPS)
CONTEXT=('Room','Apron','Evening','CuesRestored','DisplayStaged','HelpAccepted','RigRoom','Connected','Mic','Inward','ContestActive','VC03Resolved','BunnyRoom','FrankieRoom','MiloRoom','VivianRoom','RitaRoom','FelixRoom','StringerRoom','Epoch')
PROPS.update(dict.fromkeys(['p12'+p for p in ('ContextValid',*CONTEXT,'Code','LineCount','UnitCount','EventCount','ResultHi','ResultLo','PresentationSource','PresentationHi','PresentationLo')],0))
CODES={name:i+1 for i,name in enumerate(('offscreen','contest_active','speaker_absent','already_rehung','p11_required','rack_rehung','rack_handoff_required','pa_not_present','microphone_unplugged','selector_tape','speaker_not_facing_inward','repair_rack_first','vc03_resolution_required','faces_now_on_set','rack_now_facing_host','confetti_not_released','confetti_scene_pending','catch_already_released','catch_released','already_facing_host','catch_required','audience_side_observation_required','rack_facing_host','rotate_first','welcome_order_protected','order_unchanged','cues_reordered','introduction_already_clear','incomplete_introduction','whole_introduction_required','introduction_clear','confetti_already_released','introduction_required','ensemble_absent','confetti_released','laugh_consumed','laugh_window_closed','collection_already_started','cleanup_text_required','collection_started','unhandled_action','hint','presentation_not_started','presentation_complete','presentation_pending','presentation_already_acknowledged','presentation_acknowledged','stale_presentation','presentation_cancelled','audio_has_no_authority','invalid_argument','invalid_context','invalid_state','serial_exhausted'))}
EVENTS={name:i+1 for i,name in enumerate(('P12_PRESENTATION_QUEUED','P12_PRESENTED','P12_RACK_HANDOFF','P12_CATCH_RELEASED','P12_RACK_ROTATED','P12_CUES_REORDERED','P12_INTRODUCTION_CLEAR','P12_CONFETTI','LAF12','P12_COLLECTION_POINTS'))}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(name,arg,mapping,default=0):
 return f'(method ({name} {arg} &tmp answer)\n (= answer {default})\n (switch {arg}\n'+''.join(f' ({k} (= answer {v}))\n' for k,v in mapping.items())+') (return answer))\n'
def main():
 from tools.verify_inputs import verify
 from tools.generate_fixture import fixture as build_fixture
 verify()
 fixture=json.loads((ROOT/'tests/fixtures/p12/canonical-bindings.json').read_text())
 expected=build_fixture()
 if fixture!=json.loads(json.dumps(expected)):raise RuntimeError('Stale or incomplete binding fixture')
 authority=ROOT/'authority/CURRENT-SCRIPT-REVISION.json'
 records={x['id']:x for x in fixture['records']}
 objects=dict(json.loads((ROOT/'dependencies/p10-current-manifest.json').read_text())['objects'])
 # Finite local source-oracle identities only, not production reservations.
 own={'swivel_release_catch':419,'rack_rotating_handle':420}
 if set(own.values())&set(objects.values()):raise RuntimeError('Local oracle object collision')
 objects.update(own)
 lines={name:i+1 for i,name in enumerate(records)};units={x['line_id']:i+1 for i,x in enumerate(fixture['speech_units'])}
 tokens={t:i+1 for i,t in enumerate(dict.fromkeys(x['token'] for rs in RECEIPTS.values() for x in rs))}
 constants=[]
 for prefix,values in (('OBJ',objects),('CODE',CODES),('EVENT',EVENTS),('SOURCE',SOURCES),('LINE',lines),('UNIT',units),('TOKEN',tokens)):
  constants += [f'(define {prefix}_{k.upper().replace(".","_")} {v})' for k,v in values.items()]
 constants += [f'(define ROOM_{k} {v.number})' for k,v in ROOMS.items()]
 generated=''
 for limb in ('Hi','Lo'):generated+=table('p12Serial'+limb,'slot',{i:'p12'+n+limb for i,n in enumerate(SERIALS)})
 generated+='(method (p12SetSerial slot hi lo) (switch slot '+''.join(f' ({i} (= p12{n}Hi hi) (= p12{n}Lo lo))' for i,n in enumerate(SERIALS))+') (return 1))\n'
 generated+=table('p12Capacity','source',{SOURCES[s]:len(rs) for s,rs in RECEIPTS.items()})
 generated+=table('p12ReceiptBase','source',{SOURCES[s]:rs[0]['slot'] for s,rs in RECEIPTS.items()})
 generated+=table('p12SourceRecord','source',{SOURCES[s]:lines[model.P12World.SOURCES[s]] for s in SOURCES})
 generated+='(method (p12Token source index &tmp answer) (= answer 0) (switch source\n'
 for s,rs in RECEIPTS.items():generated+=f' ({SOURCES[s]} (switch index '+''.join(f' ({i} (= answer {tokens[r["token"]]}))' for i,r in enumerate(rs))+'))\n'
 generated+=') (return answer))\n'
 generated+=table('p12TokenUnit','token',{v:units.get(k,0) for k,v in tokens.items()})
 generated+=table('p12TokenSpeaker','token',{v:objects.get(model.UNIT_SPEAKERS.get(k,''),0) for k,v in tokens.items()})
 generated+=table('p12CueIndex','obj',{objects[x]:i for i,x in enumerate(CUE_IDS)},-1)
 generated+=table('p12CueAt','index',{i:objects[x] for i,x in enumerate(CUE_IDS)})
 generated+=table('p12WordAt','index',{i:'p12Word'+str(i) for i in range(6)})
 generated+=table('p12SlotAt','index',{i:'p12Slot'+str(i) for i in range(3)})
 generated+=table('p12ActorRoom','obj',{objects[x]:'p12'+x.title()+'Room' for x in model.PEOPLE[1:]},-1)
 for name,n in [('Word',6),('Slot',3)]:generated+=f'(method (p12Set{name} index value) (switch index '+''.join(f'({i} (= p12{name}{i} value))' for i in range(n))+') (return 1))\n'
 inv_limit=max(objects.values())+1
 generated+='(method (p12ContextItem obj &tmp valid) (if (not p12ContextValid) (return 0)) (= valid 0) (switch obj\n'
 for name,id in objects.items():
  if name not in (*model.PEOPLE,'audience'):generated+=f' ({id} (= valid 1))\n'
 generated+=') (if valid (= [p12Held obj] 1) (return 1)) (= p12ContextValid 0) (self p12Clear:) (= p12Code CODE_INVALID_CONTEXT) (return 0))\n'
 fields=' '.join(x[0].lower()+x[1:] for x in CONTEXT)
 generated+=f'(method (p12Context {fields} &tmp i) (self p12Invalidate:) (for ((= i 0)) (< i P12_INVENTORY_LIMIT) ((++ i)) (= [p12Held i] 0))\n (if (or '
 for name in CONTEXT:
  arg=name[0].lower()+name[1:]
  lo,hi=(-1,6) if name.endswith('Room') and name not in ('Room','RigRoom') else (0,6) if name.endswith('Room') else (0,1)
  if name=='Epoch':generated+='(< epoch 1) (<= epoch p12Epoch) '
  else:generated+=f'(< {arg} {lo}) (> {arg} {hi}) '
 generated+=') (= p12Code CODE_INVALID_CONTEXT) (return 0))\n'+''.join(f'(= p12{x} {x[0].lower()+x[1:]}) ' for x in CONTEXT)+'(= p12ContextValid 1) (return 1))\n'
 methods=(HERE/'src/methods.sc.in').read_text()
 dispatch=''
 for obj,method in [('swivel_release_catch','ReleaseCatch'),('rack_rotating_handle','Rotate')]:
  if obj in objects:dispatch+=f'(if (and (== verb 9) (== obj OBJ_{obj.upper()})) (return (self p12{method}:)))\n'
 methods=methods.replace('; GENERATED_RACK_DISPATCH',dispatch)
 source=';;; Sierra Script 1.0 - (do not remove this comment)\n; Original isolated P12 domain adapter. Canonical IDs only.\n(script# 994)\n(public p12State 0)\n'+f'(local [p12Lines 3] [p12Units 8] [p12Events 1] [p12EventArgs 4] [p12EventHi 1] [p12EventLo 1] [p12Held {inv_limit}] [p12Lease 12])\n'+'\n'.join(constants)+'\n'+f'(define P12_SERIAL_COUNT {len(SERIALS)})\n(define P12_LINE_LIMIT {len(lines)})\n(define P12_INVENTORY_LIMIT {inv_limit})\n(class P12State\n(properties\n'+'\n'.join(f' {k} {v}' for k,v in PROPS.items())+'\n)\n'+generated+methods+'\n)\n(instance p12State of P12State)\n'
 (HERE/'src/module994.sc').write_text(source)
 manifest=dict(scope='NEW finite SCI SOURCE oracle only; no compile, bytecode, host or native acceptance',script=994,export=0,export_name='p12State',standalone_species=1,historical_production_reserved_species=16,production_reservation_status='UNCONFIRMED_IN_THIS_FINITE_SOURCE_GATE',objects=objects,own_objects=own,unbound_objects=[x for x in ('swivel_release_catch','rack_rotating_handle') if x not in objects],rooms={k:v.number for k,v in ROOMS.items()},sources=SOURCES,codes=CODES,events=EVENTS,line_ids=lines,speech_unit_ids=units,tokens=tokens,serials=SERIALS,receipts=RECEIPTS,source_bindings=model.P12World.SOURCES,words={v:i+1 for i,v in enumerate(ORDER)},cue_ids=list(CUE_IDS),persisted_properties=PERSISTED,all_properties=PROPS,max_serial=1073741823,serial_limb_base=32768,line_capacity=3,speech_unit_capacity=8,event_capacity=1,event_arg_capacity=4,external_inventory_capacity=inv_limit,model_sha256=sha(ROOT/'cakood/p12_model.py'),fixture_sha256=sha(ROOT/'tests/fixtures/p12/canonical-bindings.json'),p10_abi_manifest_sha256=sha(ROOT/'dependencies/p10-current-manifest.json'),source_sha256=sha(HERE/'src/module994.sc'),authority_sha256=sha(authority),gdd_sha256=sha(ROOT/'authority/complete-body.md'),accepted_pairs_sha256=sha(ROOT/'authority/accepted-insult-pairs.json'),speech_metadata=fixture['speech_units'],canonical_records=records)
 (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(f'Generated script994: {len(source)} bytes, {len(SERIALS)} serials, {len(lines)} canonical records')
if __name__=='__main__':main()
