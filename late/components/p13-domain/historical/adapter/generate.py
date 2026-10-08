#!/usr/bin/env python3
"""Bind canonical P13 model identities to an isolated original SCI1.1 adapter."""
from pathlib import Path
import hashlib,json,re,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from cakood import p13_model as model
from cakood.p02_model import ROOMS
from cakood.p10_model import ORDER
SOURCES={x:i+1 for i,x in enumerate(model.P13World.SOURCES)}
STAMPS=[('Revision','revision'),('Start','start_at'),('Program','program_at'),('Seated','seated_at'),('Pot','pot_at'),('Served','served_at'),('Display','display_at'),('Screen','screen_at'),('Show','show_at'),('Board','board_at'),('Toast','toast_at'),('ContestRequest','contest_request_at'),('Wrong','wrong_at'),('WrongVisual','wrong_visual_at'),('Laugh','laugh_at')]
SERIALS=[x for x,_ in STAMPS]+['ServeSave','ShowSave','ToastSave','Attempts']+[x.title().replace('_','')+'Start' for x in SOURCES]
RECEIPTS={}
for source in SOURCES:
 RECEIPTS[source]=[]
 for token in model.P13World()._tokens(source):
  RECEIPTS[source].append({'slot':len(SERIALS),'token':token});SERIALS.append(source.title().replace('_','')+'Receipt'+str(len(RECEIPTS[source])))
PROPS=dict.fromkeys(['p13Initialized','p13WrongSource']+['p13'+n+l for n in SERIALS for l in ('Hi','Lo')],0)
PERSISTED=list(PROPS)
CONTEXT=('Room','Apron','IntroductionClear','FoodReady','DisplayStaged','HelpAccepted','EveningStarted','WelcomeCleared','QueueClear','BuffetAtHatch','HatchVisible','DisplayConcealed','LaneClear','FootprintClear','BoardRoom','RigRoom','Connected','Mic','Inward','ContestActive','VC04Resolved','BunnyRoom','FrankieRoom','MiloRoom','VivianRoom','RitaRoom','FelixRoom','StringerRoom','GatePresent','PegID','PegRoom','GateTested','PegAvailable','PegEngaged','GateOpen','WedgeInGate','Epoch')
PROPS.update(dict.fromkeys(['p13'+p for p in ('ContextValid',*CONTEXT,'Code','LineCount','UnitCount','EventCount','ResultHi','ResultLo','PresentationSource','PresentationHi','PresentationLo')],0))
# Extract only machine status constants; never player prose.
modeltext=(ROOT/'cakood/p13_model.py').read_text()
status=list(dict.fromkeys(re.findall(r"(?:_result|_commit|_route_feedback)\('([^']+)'",modeltext)))
status += ['serve_complete','show_complete','toast_complete','contest_request_acknowledged','contest_request_cancelled','presentation_not_started','presentation_complete','presentation_pending','presentation_already_acknowledged','presentation_acknowledged','stale_presentation','presentation_cancelled','audio_has_no_authority','hint','offscreen','contest_active','speaker_absent','invalid_argument','invalid_context','invalid_state','serial_exhausted','autosave_failed']
CODES={n:i+1 for i,n in enumerate(dict.fromkeys(status))}
EVENTS={n:i+1 for i,n in enumerate(('P13_PRESENTATION_QUEUED','P13_PRESENTED','P13_DELIVERY_OWNERSHIP','P13_ROUTE_ATTEMPT','P13_GUEST_ROUTE','P13_GUEST_ROUTE_COMPLETE','P13_POT_DELIVERED','P13_SERVE','P13_DISPLAY_DELIVERED','P13_SCREEN_OPENED','P13_SHOW','P13_BOARD_DELIVERED','P13_VC04_REQUEST','P13_CONTEST_HANDOFF','P13_TOAST','P13_AUTOSAVE_REQUEST','P13_AUTOSAVE_ACK','P13_WRONG_VISUAL','LAF13'))}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(name,arg,mapping,default=0):return f'(method ({name} {arg} &tmp answer) (= answer {default}) (switch {arg}\n'+''.join(f' ({k} (= answer {v}))\n' for k,v in mapping.items())+') (return answer))\n'
def main():
 fixture=json.loads((ROOT/'tests/fixtures/p13/canonical-bindings.json').read_text());registry=json.loads((ROOT/'docs/native-resource-registry.json').read_text())
 assert 'P13State species17' in registry['scripts']['995']
 authority=Path('/workspace/shared/cakood/full-script/CURRENT-SCRIPT-REVISION.json');current=json.loads(authority.read_text())
 assert fixture['catalog_sha256']==current['catalog_sha256'] and current['editorial_revision']==3
 assert sha(authority.parent/current['catalog'])==current['catalog_sha256'];assert sha(authority.parent/current['speech'])==fixture['speech_sha256']
 records={x['id']:x for x in fixture['records']};assert set(model.RECORD_UNITS)==set(records)
 records.update({x['id']:x for x in fixture['support_records']})
 assert {u['line_id']:u['speaker_id'] for u in fixture['speech_units']}==model.UNIT_SPEAKERS
 for record,units in model.RECORD_UNITS.items():assert tuple(u['line_id'] for u in fixture['speech_units'] if u['record_id']==record)==units
 objects=json.loads((HERE.parent/'p11-domain-adapter/manifest.json').read_text())['objects']
 own=json.loads((HERE/'object-bindings.json').read_text());assert own=={'guest_program_card':432,'pledge_board':433,'screen_pull_tab':434}
 for name,id in own.items():assert f'{name}{id}' in registry['object_id_reservations']['432-434']
 assert not set(own.values())&set(objects.values());objects.update(own)
 lines={name:i+1 for i,name in enumerate(records)};units={x['line_id']:i+1 for i,x in enumerate(fixture['speech_units'])}
 tokens={t:i+1 for i,t in enumerate(dict.fromkeys(x['token'] for rs in RECEIPTS.values() for x in rs))}
 constants=[]
 for prefix,values in (('OBJ',objects),('CODE',CODES),('EVENT',EVENTS),('SOURCE',SOURCES),('LINE',lines),('UNIT',units),('TOKEN',tokens)):
  constants += [f'(define {prefix}_{k.upper().replace(".","_")} {v})' for k,v in values.items()]
 constants += [f'(define ROOM_{k} {v.number})' for k,v in ROOMS.items()]
 generated=''
 for limb in ('Hi','Lo'):generated+=table('p13Serial'+limb,'slot',{i:'p13'+n+limb for i,n in enumerate(SERIALS)})
 generated+='(method (p13SetSerial slot hi lo) (switch slot '+''.join(f' ({i} (= p13{n}Hi hi) (= p13{n}Lo lo))' for i,n in enumerate(SERIALS))+') (return 1))\n'
 generated+=table('p13Capacity','source',{SOURCES[s]:len(rs) for s,rs in RECEIPTS.items()})
 generated+=table('p13ReceiptBase','source',{SOURCES[s]:rs[0]['slot'] for s,rs in RECEIPTS.items()})
 generated+=table('p13SourceRecord','source',{SOURCES[s]:lines[model.P13World.SOURCES[s]] for s in SOURCES})
 generated+='(method (p13Token source index &tmp answer) (= answer 0) (switch source\n'
 for s,rs in RECEIPTS.items():generated+=f' ({SOURCES[s]} (switch index '+''.join(f' ({i} (= answer {tokens[r["token"]]}))' for i,r in enumerate(rs))+'))\n'
 generated+=') (return answer))\n'
 generated+=table('p13TokenUnit','token',{v:units.get(k,0) for k,v in tokens.items()})
 generated+=table('p13TokenSpeaker','token',{v:objects.get(model.UNIT_SPEAKERS.get(k,''),0) for k,v in tokens.items()})
 generated+=table('p13ActorRoom','obj',{objects[x]:'p13'+x.title()+'Room' for x in model.PEOPLE[1:]},-1)
 generated+=table('p13CueSlot','cue',{1:5,2:8,3:10})
 inv_limit=max(objects.values())+1
 generated+='(method (p13ContextItem obj &tmp valid) (if (not p13ContextValid) (return 0)) (= valid 0) (switch obj\n'
 for name,id in objects.items():
  if name not in (*model.PEOPLE,'audience','hotpot_pot','handcart','folded_display','pledge_board'):generated+=f' ({id} (= valid 1))\n'
 generated+=') (if valid (= [p13Held obj] 1) (return 1)) (= p13ContextValid 0) (self p13Clear:) (= p13Code CODE_INVALID_CONTEXT) (return 0))\n'
 fields=' '.join(x[0].lower()+x[1:] for x in CONTEXT)
 generated+=f'(method (p13Context {fields} &tmp i) (self p13Invalidate:) (for ((= i 0)) (< i P13_INVENTORY_LIMIT) ((++ i)) (= [p13Held i] 0))\n (if (or '
 for name in CONTEXT:
  arg=name[0].lower()+name[1:]
  lo,hi=(-1,6) if name.endswith('Room') and name not in ('Room','RigRoom','PegRoom','BoardRoom') else (0,6) if name.endswith('Room') else (0,1)
  if name=='Epoch':generated+='(< epoch 1) (<= epoch p13Epoch) '
  elif name=='PegID':generated+=f'(< {arg} 0) (> {arg} 32767) '
  else:generated+=f'(< {arg} {lo}) (> {arg} {hi}) '
 generated+=') (= p13Code CODE_INVALID_CONTEXT) (return 0))\n'
 generated+='(if (and (!= boardRoom ROOM_L01_LIVING_ROOM) (!= boardRoom ROOM_L05_COURTYARD)) (= p13Code CODE_INVALID_CONTEXT) (return 0))\n'
 generated+='(if gatePresent (if (or (!= pegID OBJ_HOLD_OPEN_PEG) (!= pegRoom ROOM_L04_SIDE_PASSAGE) (and pegAvailable (not gateTested)) (and pegEngaged (not (and pegAvailable gateOpen)))) (= p13Code CODE_INVALID_CONTEXT) (return 0)))\n'
 generated+=''.join(f'(= p13{x} {x[0].lower()+x[1:]}) ' for x in CONTEXT)+'(= p13ContextValid 1) (return 1))\n'
 methods=(HERE/'src/methods.sc.in').read_text()
 source=';;; Sierra Script 1.0 - (do not remove this comment)\n; Original isolated P13 adapter. Canonical identities only.\n(script# 995)\n(public p13State 0)\n'+f'(local [p13Lines 3] [p13Units 8] [p13Events 2] [p13EventArgs 8] [p13EventHi 2] [p13EventLo 2] [p13Held {inv_limit}] [p13Lease 16])\n'+'\n'.join(constants)+'\n'+f'(define P13_SERIAL_COUNT {len(SERIALS)})\n(define P13_LINE_LIMIT {len(lines)})\n(define P13_INVENTORY_LIMIT {inv_limit})\n(class P13State\n(properties\n'+'\n'.join(f' {k} {v}' for k,v in PROPS.items())+'\n)\n'+generated+methods+'\n)\n(instance p13State of P13State)\n'
 (HERE/'src/module995.sc').write_text(source)
 manifest=dict(scope='Isolated SCI1.1 domain bytecode; genuine host save and native acceptance pending',script=995,export=0,export_name='p13State',standalone_species=1,production_reserved_species=17,objects=objects,own_objects=own,rooms={k:v.number for k,v in ROOMS.items()},context=list(CONTEXT),sources=SOURCES,codes=CODES,events=EVENTS,line_ids=lines,speech_unit_ids=units,tokens=tokens,serials=SERIALS,stamps=STAMPS,receipts=RECEIPTS,source_start_offset=18,preview_vocabulary={'people':1,'hotpot_pot':2,'folded_display':3,'handcart':4,'pledge_board':5,'buffet':6,'display_footprint':7,'pledge_board_position':8},preview_facts={'pot_fits_hatch':True,'people_use_house':True,'display_fits_hatch':False,'display_requires_folded_width':True,'timer':None},source_bindings=model.P13World.SOURCES,words={v:i+1 for i,v in enumerate(ORDER)},routes={v:i+1 for i,v in enumerate(model.ROUTES)},persisted_properties=PERSISTED,all_properties=PROPS,max_serial=1073741823,serial_limb_base=32768,line_capacity=3,speech_unit_capacity=8,event_capacity=2,event_arg_capacity=4,external_inventory_capacity=inv_limit,model_sha256=sha(ROOT/'cakood/p13_model.py'),fixture_sha256=sha(ROOT/'tests/fixtures/p13/canonical-bindings.json'),registry_sha256=sha(ROOT/'docs/native-resource-registry.json'),source_sha256=sha(HERE/'src/module995.sc'),authority_sha256=sha(authority),gdd_sha256=sha(Path('/workspace/shared/cakood/ending-seam-20261005/current-gdd.txt')),competition_contract_sha256=sha(Path('/workspace/shared/cakood/verbal-competitions-update/CANONICAL-CONTRACT.md')),speech_metadata=fixture['speech_units'],canonical_records=records)
 (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(f'Generated script995: {len(source)} bytes, {len(SERIALS)} serials, {len(lines)} canonical records')
if __name__=='__main__':main()
