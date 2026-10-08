#!/usr/bin/env python3
"""Generate finite P14 SCI tables from accepted model and frozen canonical records."""
from pathlib import Path
import hashlib,json,re,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from cakood import p14_model as model
from cakood.p02_model import ROOMS
SOURCES={x:i+1 for i,x in enumerate(model.P14World.SOURCES)}
SERIALS=['Revision','Start','Signature','Pencil','Complete','Finale','Frame','Celebration','Laugh']+['Pin'+p.title() for p in model.PEOPLE]+['Source'+str(i)+'Start' for i in SOURCES.values()]
RECEIPTS={}
for source in SOURCES:
 RECEIPTS[source]=[]
 for i,token in enumerate(model.P14World()._tokens(source)):
  RECEIPTS[source].append({'slot':len(SERIALS),'token':token});SERIALS.append('Source'+str(SOURCES[source])+'Receipt'+str(i+1))
PROPS=dict.fromkeys(['p14Initialized','p14EntryHi','p14EntryLo','p14DateLength','p14Tone','p14Phase','p14Paused','p14Skipped','p14Replay','p14CreditCount','p14CreditCursor']+['p14Win'+str(i)+l for i in range(4) for l in ('Hi','Lo')]+['p14Date'+str(i)+l for i in range(80) for l in ('Hi','Lo')]+['p14Credit'+str(i) for i in range(59)]+['p14'+n+l for n in SERIALS for l in ('Hi','Lo')],0)
PERSISTED=list(PROPS)
CONTEXT=('Room','Apron','FlagsHi','FlagsLo','BoardRoom','InputTone','ContestActive','BunnyRoom','FrankieRoom','MiloRoom','VivianRoom','RitaRoom','FelixRoom','StringerRoom','Epoch')
PROPS.update(dict.fromkeys(['p14'+x for x in ('ContextValid','ContextBuilding','ContextDateLength',*CONTEXT,'Code','LineCount','UnitCount','EventCount','ResultHi','ResultLo','PresentationSource','PresentationHi','PresentationLo')],0))
# Status names extracted only from accepted model plus bounded transport errors.
base=(ROOT/'cakood/p14_model.py').read_text()+(ROOT/'cakood/p12_model.py').read_text()+(ROOT/'cakood/p10_model.py').read_text()
names=list(dict.fromkeys(re.findall(r"(?:_result|_commit)\('([^']+)'",(ROOT/'cakood/p14_model.py').read_text())))
names+=['offscreen','contest_active','speaker_absent','presentation_not_started','presentation_complete','presentation_pending','presentation_already_acknowledged','presentation_acknowledged','stale_presentation','presentation_cancelled','audio_has_no_authority','hint','finale_paused','finale_resumed','invalid_argument','invalid_context','invalid_state','serial_exhausted','replay_prepared','no_pending_finale_text']
CODES={n:i+1 for i,n in enumerate(dict.fromkeys(names))}
EVENTS={n:i+1 for i,n in enumerate(('P14_PRESENTATION_QUEUED','P14_PRESENTED','P14_COMMITMENT_START','P14_CARD_PINNED','P14_TERMS_SIGNED','P14_PENCIL_HANDOFF','P14_GAME_COMPLETE','P14_FINALE_BEGIN','P14_FINALE_SCENE','P14_FREEZE_PRESENTED','LAF14','P14_CELEBRATION','P14_FINALE_PAUSE','P14_FINALE_SKIP'))}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ident(s):return re.sub('[^A-Z0-9_]','_',s.upper())
def switches(arg,mapping):
 if len(mapping)>16:
  groups={}
  for k,v in mapping.items():groups.setdefault(k//16,{})[k]=v
  return f'(switch (/ {arg} 16) '+''.join(f'({bucket} '+switches(arg,items)+')' for bucket,items in groups.items())+')'
 return f'(switch {arg} '+''.join(f'({k} {v})' for k,v in mapping.items())+')'
def table(name,arg,mapping,default=0):
 return f'(method ({name} {arg} &tmp answer) (= answer {default}) '+switches(arg,{k:f'(= answer {v})' for k,v in mapping.items()})+' (return answer))\n'
def setter(name,arg,mapping):
 return f'(method ({name} {arg} value) '+switches(arg,{i:f'(= {p} value)' for i,p in mapping.items()})+' (return 1))\n'
def main():
 fixture=json.loads((ROOT/'tests/fixtures/p14/canonical-bindings.json').read_text());registry=json.loads((ROOT/'docs/native-resource-registry.json').read_text())
 assert 'P14State species18' in registry['scripts']['996']
 authority=Path('/workspace/shared/cakood/full-script/CURRENT-SCRIPT-REVISION.json');current=json.loads(authority.read_text())
 assert fixture['catalog_sha256']==current['catalog_sha256']=='1226a97873a3693867c08afe2731ddb55adef6f0eaeabc1222e103c04c0d9fa7' and current['editorial_revision']==3
 assert sha(authority.parent/current['catalog'])==current['catalog_sha256'];assert sha(authority.parent/current['speech'])==fixture['speech_sha256']
 records={x['id']:x for x in fixture['records']};assert set(records)==set(model.RECORD_UNITS)
 assert {u['line_id']:u['speaker_id'] for u in fixture['speech_units']}==model.UNIT_SPEAKERS
 for record,units in model.RECORD_UNITS.items():assert tuple(u['line_id'] for u in fixture['speech_units'] if u['record_id']==record)==units
 objects=json.loads((HERE.parent/'p12-domain-adapter/manifest.json').read_text())['objects']
 p09=json.loads((HERE.parent/'p09-domain-adapter/manifest.json').read_text())['objects'];objects.update(p09)
 own={model.CARD_IDS[p]:435+i for i,p in enumerate(model.PEOPLE)}
 assert all(p in registry['object_id_reservations']['435-442'] for p in model.PEOPLE)
 assert not set(own.values())&set(objects.values())
 objects.update({'pledge_board':433});objects.update(own)
 (HERE/'object-bindings.json').write_text(json.dumps(own,indent=2)+'\n')
 lines={name:i+1 for i,name in enumerate(records)};units={x['line_id']:i+1 for i,x in enumerate(fixture['speech_units'])}
 tokens={t:i+1 for i,t in enumerate(dict.fromkeys(x['token'] for rs in RECEIPTS.values() for x in rs))}
 constants=[]
 for prefix,values in (('OBJ',objects),('CODE',CODES),('EVENT',EVENTS),('SOURCE',SOURCES),('LINE',lines),('UNIT',units),('TOKEN',tokens)):
  constants += [f'(define {prefix}_{ident(k)} {v})' for k,v in values.items()]
 constants += [f'(define ROOM_{k} {v.number})' for k,v in ROOMS.items()]
 generated=''
 for limb in ('Hi','Lo'):generated+=table('p14Serial'+limb,'slot',{i:'p14'+n+limb for i,n in enumerate(SERIALS)})
 generated+='(method (p14SetSerial slot hi lo) '+switches('slot',{i:f'(= p14{n}Hi hi) (= p14{n}Lo lo)' for i,n in enumerate(SERIALS)})+' (return 1))\n'
 generated+=table('p14Capacity','source',{SOURCES[s]:len(rs) for s,rs in RECEIPTS.items()})
 generated+=table('p14ReceiptBase','source',{SOURCES[s]:rs[0]['slot'] for s,rs in RECEIPTS.items()})
 generated+=table('p14SourceRecord','source',{SOURCES[s]:lines[model.P14World.SOURCES[s]] for s in SOURCES})
 generated+='(method (p14Token source index &tmp answer) (= answer 0) (switch source\n'
 for s,rs in RECEIPTS.items():generated+=f' ({SOURCES[s]} (switch index '+''.join(f' ({i} (= answer {tokens[r["token"]]}))' for i,r in enumerate(rs))+'))\n'
 generated+=') (return answer))\n'
 generated+=table('p14TokenUnit','token',{v:units.get(k,0) for k,v in tokens.items()})
 generated+=table('p14TokenSpeaker','token',{v:objects.get(model.UNIT_SPEAKERS.get(k,''),0) for k,v in tokens.items()})
 generated+=table('p14ActorRoom','obj',{objects[x]:'p14'+x.title()+'Room' for x in model.PEOPLE[1:]},-1)
 generated+=table('p14Person','index',{i:objects[p] for i,p in enumerate(model.PEOPLE)})
 generated+=table('p14PersonIndex','obj',{objects[p]:i for i,p in enumerate(model.PEOPLE)},-1)
 generated+=table('p14Card','index',{i:objects[model.CARD_IDS[p]] for i,p in enumerate(model.PEOPLE)})
 generated+=table('p14CardIndex','obj',{objects[model.CARD_IDS[p]]:i for i,p in enumerate(model.PEOPLE)},-1)
 for name,count in [('Credit',59),('DateHi',80),('DateLo',80),('WinHi',4),('WinLo',4)]:
  if name in ('Credit',):mapping={i:f'p14Credit{i}' for i in range(count)}
  else:mapping={i:f'p14{name[:-2]}{i}{name[-2:]}' for i in range(count)}
  generated+=table('p14'+name+'At','index',mapping);generated+=setter('p14Set'+name,'index',mapping)
 inv_limit=max(objects.values())+1
 generated+='(method (p14ContextItem obj &tmp valid) (if (not p14ContextBuilding) (return 0)) (= valid 0) (switch obj\n'
 for name,id in objects.items():
  if name not in (*model.PEOPLE,'audience',*model.CARD_IDS.values()):generated+=f' ({id} (= valid 1))\n'
 generated+=') (if valid (= [p14Held obj] 1) (return 1)) (return (self p14ContextError:)))\n'
 fields=' '.join(x[0].lower()+x[1:] for x in CONTEXT)
 generated+=f'(method (p14Context {fields} &tmp i) (self p14Invalidate:) (= p14ContextBuilding 0) (= p14ContextDateLength 0)\n(for ((= i 0)) (< i P14_INVENTORY_LIMIT) ((++ i)) (= [p14Held i] 0))\n(for ((= i 0)) (< i 4) ((++ i)) (= [p14FirstWinHi i] 0) (= [p14FirstWinLo i] 0) (= [p14LastWinHi i] 0) (= [p14LastWinLo i] 0) (= [p14MatchingWin i] 0))\n(for ((= i 0)) (< i 160) ((++ i)) (= [p14InputDate i] 0))\n(if (or '
 for name in CONTEXT:
  arg=name[0].lower()+name[1:]
  lo,hi=(-1,6) if name.endswith('Room') and name not in ('Room','BoardRoom') else (0,6) if name.endswith('Room') else (0,1)
  if name=='Epoch':generated+='(< epoch 1) (<= epoch p14Epoch) '
  elif name=='FlagsHi':generated+='(< flagsHi 0) (> flagsHi 8191) '
  elif name=='FlagsLo':generated+='(< flagsLo 0) '
  elif name=='InputTone':generated+='(< inputTone 0) (> inputTone 2) '
  elif name=='BoardRoom':generated+='(and (!= boardRoom 1) (!= boardRoom 4)) '
  else:generated+=f'(< {arg} {lo}) (> {arg} {hi}) '
 generated+=') (= p14Code CODE_INVALID_CONTEXT) (return 0))\n'+''.join(f'(= p14{x} {x[0].lower()+x[1:]}) ' for x in CONTEXT)+'(= p14ContextBuilding 1) (return 1))\n'
 generated+=table('p14CreditCanonicalSource','index',{i:SOURCES['credit:'+r] for i,r in enumerate((*model.CREDIT_ORDER,*model.ASSET_CREDITS))})
 methods=(HERE/'src/methods.sc.in').read_text()
 source=';;; Sierra Script 1.0 - (do not remove this comment)\n; Original isolated P14 domain adapter. Canonical IDs only.\n(script# 996)\n(public p14State 0)\n'+f'(local [p14Lines 3] [p14Units 8] [p14Events 1] [p14EventArgs 4] [p14EventHi 1] [p14EventLo 1] [p14Held {inv_limit}] [p14Lease 88] [p14OrderedSources 87] [p14OrderedHi 87] [p14OrderedLo 87] [p14InputDate 160] [p14FirstWinHi 4] [p14FirstWinLo 4] [p14LastWinHi 4] [p14LastWinLo 4] [p14MatchingWin 4] [p14ValidationHi {len(SERIALS)}] [p14ValidationLo {len(SERIALS)}] [p14ValidationOwners {len(SERIALS)}])\n'+'\n'.join(constants)+'\n'+f'(define P14_SERIAL_COUNT {len(SERIALS)})\n(define P14_LINE_LIMIT {len(lines)})\n(define P14_INVENTORY_LIMIT {inv_limit})\n(class P14State\n(properties\n'+'\n'.join(f' {k} {v}' for k,v in PROPS.items())+'\n)\n'+generated+methods+'\n)\n(instance p14State of P14State)\n'
 (HERE/'src/module996.sc').write_text(source)
 manifest=dict(scope='Isolated SCI1.1 domain bytecode; host and native presentation acceptance pending',script=996,export=0,export_name='p14State',standalone_species=1,production_reserved_species=18,objects=objects,own_objects=own,rooms={k:v.number for k,v in ROOMS.items()},sources=SOURCES,codes=CODES,events=EVENTS,line_ids=lines,speech_unit_ids=units,tokens=tokens,serials=SERIALS,receipts=RECEIPTS,source_bindings=model.P14World.SOURCES,source_start_offset=16,terms_record_id=2,persisted_properties=PERSISTED,all_properties=PROPS,max_serial=1073741823,serial_limb_base=32768,line_capacity=3,speech_unit_capacity=8,event_capacity=1,event_arg_capacity=4,external_inventory_capacity=inv_limit,prerequisites=sorted(model.PREREQUISITES),people=list(model.PEOPLE),phases=['not_started','closing','meal','tag','freeze','credits','finished'],tones=['professional','friendly','cautiously_romantic'],credit_order=model.CREDIT_ORDER,asset_credits=model.ASSET_CREDITS,context_fields=CONTEXT,model_sha256=sha(ROOT/'cakood/p14_model.py'),fixture_sha256=sha(ROOT/'tests/fixtures/p14/canonical-bindings.json'),registry_sha256=sha(ROOT/'docs/native-resource-registry.json'),source_sha256=sha(HERE/'src/module996.sc'),authority_sha256=sha(authority),gdd_sha256=sha(Path('/workspace/shared/cakood/ending-seam-20261005/current-gdd.txt')),speech_metadata=fixture['speech_units'],canonical_records=records)
 (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(f'Generated script996: {len(source)} bytes, {len(SERIALS)} serials, {len(lines)} canonical records')
if __name__=='__main__':main()
