"""Guarded additive P09 derivative of the exact sealed P08 candidate."""
from pathlib import Path
import hashlib,importlib.util,json,sys,shutil
H=Path(__file__).resolve().parent;S=H.parent;B=S/'campaign-p08-courtyard-candidate';DATA=S/'p09-scene-data'
sys.path.insert(0,str(H));from source_tools import methods,spans
PIN='2ccb5064223b0d9a90562531098aa7353b5e30394205b496c3ad78d9215644c0'
GDD_PIN='779734c8a9d919de188415c02b02f1de0ad9433fffc504f7d46b9ba5582912b9'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def once(s,a,b):assert s.count(a)==1,(a,s.count(a));return s.replace(a,b,1)
def insert(s,cls,body):n=spans(s,'class')[cls][1]-1;return s[:n]+'\n'+body+'\n'+s[n:]
def update(s,new):
 for n,m in methods(s).items():
  if n in new and new[n]!=m:s=once(s,m,new[n])
 return s

def head(m,body):i=m.index('\n') if '\n' in m else m.index(')')+1;return m[:i]+'\n'+body+'\n'+m[i:]
def main_source(s):
 new=methods(s).copy()
 def add(n,b):new[n]=head(new[n],b)
 def rep(n,a,b):new[n]=once(new[n],a,b)
 add('play','(= p09 (ScriptID 990 0)) (p09 p09Init:)')
 rep('play','(p08 cEnabled: (p08 cRoutesReady: self))','(p08 cEnabled: (p08 cRoutesReady: self)) (p09 dEnabled: (p09 dRoutesReady: self))')
 add('replay','(= p09 (ScriptID 990 0)) (p09 dCancel:)')
 rep('replay','(p08 cAfterRestore: self)','(p08 cAfterRestore: self) (p09 dAfterRestore: self)')
 add('writeSave','(if (and p09 (not (p09 dSaveReady: self))) (= uiFailure 10) (= dirty 1) (return 0)) (if p09 (p09 dCancel:))')
 for n in ('readSave','uiHostMenu','bridgeBegin'):add(n,'(if p09 (p09 dCancel:))')
 rep('bridgeActAtArrival','(self bridgeBegin:)','(self bridgeBegin:)\n(if (and p09 (p09 dDispatch: self action obj target)) (return 0))')
 add('uiHostShortLabel','(if (== obj 399) (return ""))')
 add('uiHostAct','(if (and (== action 0) (not second) (or (== first 397) (== first 398))) (= action 7))')
 rep('uiChooseObject','(== item 109) (and (== location 4)', '(== item 109) (== item 397) (== item 398) (and (== location 4)')
 add('campaignHeld','(if (and p09 (>= obj 395) (<= obj 399)) (return (p09 dHeld: obj)))')
 add('campaignReachable','(if (and p09 (p09 dHandles: self obj)) (return (p09 dReachable: self obj)))')
 for n in ('p02Held','p02ObjectLocation','p02Reachable'):add(n,'(if (>= obj 395) (return '+('-1' if n=='p02ObjectLocation' else '0')+'))')
 for n in ('p02Act','p02Delegate','act'):add(n,'(if (or (>= obj 395) (>= target 395)) (return 0))')
 for n in ('uiBuildFocus','uiTurnPage','uiRender'):rep(n,'(<= uiChoiceContext 232)','(<= uiChoiceContext 235)')
 add('uiHostChoice','(if (and p09 (>= context 233) (<= context 235)) (p09 dChoice: self context id) (return 0))')
 add('uiHostClosed','(if p09 (p09 dClosed: self))')
 rep('uiHostClosed','(if p08 (p08 cAfterClosed: self))','(if p08 (p08 cAfterClosed: self)) (if p09 (p09 dAfterClosed: self))')
 rep('dialoguePresented','(if p08 (p08 cCancel:)) (return 0)','(if p08 (p08 cCancel:)) (if p09 (p09 dCancel:)) (return 0)')
 rep('dialoguePresented','(= generation (dialogue sdGeneration?))','(if p09 (p09 dPresented: self uiDocument uiPage (dialogue sdGeneration?) (p09 dPaintEpoch?)) (if (p09 dFailure?) (= uiFailure 10)))\n(= generation (dialogue sdGeneration?))')
 rep('render','(render &tmp i [line 100])','(render &tmp i paintEpoch [line 100])')
 add('render','(= paintEpoch (if p09 (p09 dPaintBegin: self) else 0))')
 rep('render','(Graph 12 0 0 200 320 1)', '(Graph 12 0 0 200 320 1) (if p09 (p09 dPaintCommit: self paintEpoch))')
 add('dialogueCanSpeak','(if (and p09 (== (dialogue sdAudioModule?) 921)) (return (p09 dCanSpeak: self who)))')
 for n in ('dialogueOpen','uiTurnPage','speechCancel'):rep(n,'(if p08 (p08 cTrack: self))','(if p08 (p08 cTrack: self)) (if p09 (p09 dTrack: self))')
 add('p03PreparationHint','(if (and p09 (== location 6) (p08 p08EveningStarted?)) (p09 dRun: self 4 0 0 0) (p09 dFinish: self) (return 0))')
 rep('uiRender','(if (== i uiFocus)', '(if (and (== action 3) (== [uiPayloads i] 399) p09 (p09 dHeld: 399)) (DrawCel 243 0 2 (+ [uiLefts i] 4) (+ [uiTops i] 1) -1 0))\n            (if (== i uiFocus)')
 rep('p04SetUIItem','(> obj 92)','(> obj 399)')
 out=update(s,new).replace('(properties','(properties p09 0',1)
 (H/'generated/p09-host-methods.json').write_text(json.dumps(dict(changed=[n for n in new if new[n]!=methods(s)[n]]),indent=2)+'\n')
 return out

def bridge(s,m):
 D=json.loads((S/'p09-domain-adapter/manifest.json').read_text())
 props='dEnabled dFailure dInvalid dTransaction dOwned dGrantHi dGrantLo dView dEpoch dEpochFailure dPending dCount dCursor dPage dCode dDocument dDisplayPage dGeneration dSource dReceiptHi dReceiptLo dReceiptEpoch dNextMenu dPaintEpoch dFrameDoc dFramePage dFrameGeneration'.split()
 s=once(s,'(properties','(properties\n'+' '.join(n+' 0' for n in props)+'\n')
 persisted=D['persisted_properties']+['dOwned','dGrantHi','dGrantLo']
 s=once(s,'(local ',f'(local [dBefore {len(persisted)}] [dDocs 14] ')
 out=[]
 for name,write in [('dSnapshot',True),('dRollback',False)]:
  out.append('(method ('+name+')\n'+'\n'.join(f'(= [dBefore {i}] {p})' if write else f'(= {p} [dBefore {i}])' for i,p in enumerate(persisted))+'\n(return 1))')
 routes=m['routes']+m['unit_routes']
 out.append('(method (dExpectedPages doc) (switch doc\n'+'\n'.join(f'({r["document_id"]} (return {r["page_count"]}))' for r in routes)+') (return 0))')
 receipts=json.loads((DATA/'generated/receipt-map.json').read_text())
 rows=[]
 for r in receipts['record_receipts'].values():
  if r['units']:rows.append(f'({r["document_id"]} (switch page '+ ' '.join(f'({u["last_record_page"]} (return {u["speech_unit_id"]}))' for u in r['units'])+'))')
 for u in receipts['unit_receipts'].values():rows.append(f'({u["document_id"]} (if (== page {len(u["pages"])-1}) (return {u["speech_unit_id"]})))')
 out.append('(method (dPageUnitEnd doc page) (switch doc\n'+'\n'.join(rows)+') (return 0))')
 for name,key in [('dChoiceLabel','CHOICE'),('dRecordLabel',None)]:
  rows=[]
  for r in m['routes']:
   if key and key not in r['record_id']:continue
   label=(' '.join(p['text'].replace('\n',' ') for p in m['pages'] if p.get('document_id')==r['document_id']) if key else {'P09.OPEN.001':'OVERHEARD EXCHANGE','P09.LABEL.001':'CHAIR TAG','P09.READ.001':'CHAIR TAG','P09.LOOK.001':'THE THREE CHAIRS','P09.DIALOGUE.001':'WHAT IS LEAVING','P09.FAILURE.001':'THE CORRECTION','P09.DIALOGUE.002':'HOUSEHOLD AND REPAIR TERMS','P09.READ.002':'RENEWAL AND REPAIR CARD','P09.DIALOGUE.003':'SHARED WISHES','P09.SUCCESS.001':'UNSIGNED CARD RECEIVED'}.get(r['record_id'],'CONSERVATORY EVIDENCE'))
   rows.append(f'({r["local_line_key"]} (return '+json.dumps(label)+'))')
  out.append('(method ('+name+' line) (switch line '+' '.join(rows)+') (return "EVIDENCE"))')
 out.append('(method (dUnitLabel unit) (switch unit '+' '.join(f'({u["speech_unit_id"]} (return "RECORDED LINE {u["speech_unit_id"]}"))' for line,u in receipts['unit_receipts'].items())+') (return "RECORDED LINE"))')
 labels={1:'RESUME OVERHEARD EXCHANGE',2:'RESUME CHAIR TAG',3:'RESUME CHAIR INSPECTION',4:'RESUME DIRECT QUESTION',5:'RESUME FRONT CONTEXT',6:'RESUME ACCUSATION',7:'RESUME TERMS AND CARD',8:'RESUME SHARED WISHES',9:'RESUME CARD READER'}
 out.append('(method (dSourceLabel source) (switch source '+' '.join(f'({i} (return "{v}"))' for i,v in labels.items())+') (return "PENDING"))')
 out.extend((H/'src'/n).read_text() for n in ('p09-bridge.sc.in','p09-ui.sc.in'))
 (H/'generated/p09-bridge-tables.inc').write_text('\n'.join(out[:-2])+'\n')
 return insert(s,'P09State','\n'.join(out))
def controls(s):
 new=methods(s).copy()
 new['kHostUiHostItemLabel']=head(new['kHostUiHostItemLabel'],'(if (and (h p09?) (>= obj 395) (<= obj 399)) (return ((h p09?) dLabel: obj)))')
 new['kHostUiHostDefaultVerb']=head(new['kHostUiHostDefaultVerb'],'(if (and (h p09?) (>= obj 395) (<= obj 399)) (return ((h p09?) dDefaultVerb: obj)))')
 # Append exact P09 controls after preserved controls so the small tag wins hit-testing.
 new['kHostUiHostWorldControls']=new['kHostUiHostWorldControls'][:-1]+'\n(if (h p09?) ((h p09?) dWorldControls: h)))'
 for axis in 'XY':new['kHostApproach'+axis]=head(new['kHostApproach'+axis],f'(if (and (h p09?) (>= obj 395) (<= obj 399)) (return ((h p09?) dApproach{axis}: obj)))')
 return update(s,new)
def inventory(s):
 new=methods(s).copy()
 # Dense reservation storage adds one cell for card399, not306 unused IDs.
 for n in ('qValidateLayout','qInventoryFits','qAppend','qInventory'):
  new[n]=new[n].replace('> obj 92','> obj 399').replace('< i 93','< i 94')
  new[n]=new[n].replace('[qReserve obj]','[qReserve (self qReserveIndex: obj)]')
 new['qInventoryFits']=new['qInventoryFits'].replace('(<= obj 92)', '(<= obj 93)').replace('(if (self qHeld: h obj)\n            (= found', '(if (== obj 93) (= obj 399))\n        (if (self qHeld: h obj)\n            (= found')
 new['qValidateLayout']=new['qValidateLayout'].replace('(!= obj 86)))','(!= obj 86) (!= obj 399)))')
 new['qHeld']=head(new['qHeld'],'(if (== obj 399) (return (if (h p09?) ((h p09?) dHeld: obj) else 0)))\n(if (> obj 92) (return 0))')
 new['qAppend']=new['qAppend'].replace('(> obj 399)', '(and (> obj 92) (!= obj 399))')
 new['qInventory']=once(new['qInventory'],'(self qAppend: (self p04InventoryAt: 0))','(self qAppend: (self p04InventoryAt: 0))\n(if (and (h p09?) ((h p09?) dHeld: 399)) (self qAppend: 399))')
 out=update(s,new).replace('[qReserve 93]','[qReserve 94]',1)
 return insert(out,'P04State','(method (qReserveIndex obj) (if (== obj 399) (return 93)) (return obj))')

def renderer(s):
 new=methods(s).copy()
 new['drawP03Conservatory']=once(new['drawP03Conservatory'], '(DrawCel 302 0 0 0 0 -1 0)', '(DrawCel 302 0 0 0 0 -1 0)\n    (if ((host p08?) p08EveningStarted?)\n     (DrawCel 243 0 0 162 76 -1 0) (DrawCel 243 0 0 184 76 -1 0) (DrawCel 243 0 0 207 76 -1 0))')
 new['kitchenJug']=head(new['kitchenJug'], '(if (or (host opening?) (host paused?) (host motionPhase?)\n  (not (or (and (== (host uiPanel?) 2) (== (host uiChoiceContext?) 223))\n   (and (== (host uiPanel?) 4) (host scenePageIdentity:)\n    (or (== (host uiDocument?) 911) (== (host uiDocument?) 912)\n     (== (host uiDocument?) 925) (== (host uiDocument?) 926) (== (host uiDocument?) 934)))))) (return 0))')
 return update(s,new)
def main():
 assert sha(B/'FREEZE.json')==PIN
 seal=json.loads((B/'FREEZE.json').read_text())
 for name,digest in seal['files'].items():assert sha(B/name)==digest,('base changed',name)
 m=json.loads((DATA/'generated/manifest.json').read_text())
 canonical={p:d for p,d in m['protected_inputs_sha256'].items() if Path(p).name in ('CURRENT-SCRIPT-REVISION.json','full-line-catalog.json','speech-units.json')}
 assert len(canonical)==3
 for p,digest in canonical.items():assert sha(Path(p))==digest,('canonical authority changed',p)
 for p in (B/'src').glob('*.sc'):(H/'src'/p.name).write_bytes(p.read_bytes())
 (H/'src/main.sc').write_text(main_source((B/'src/main.sc').read_text()))
 original=(S/'p09-domain-adapter/src/module990.sc').read_text();assert original==(B/'src/module990.sc').read_text()
 (H/'src/module990.sc').write_text(bridge(original,m))
 (H/'src/module988.sc').write_text(controls((B/'src/module988.sc').read_text()))
 (H/'src/module984.sc').write_text(inventory((B/'src/module984.sc').read_text()))
 (H/'src/module991.sc').write_text(renderer((B/'src/module991.sc').read_text()))
 spec=importlib.util.spec_from_file_location('p09_extend',DATA/'extend_dialogue.py');e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
 source,report=e.apply_source((B/'src/module982.sc').read_text(),m)
 (H/'src/module982.sc').write_text(source);report.pop('arrays',None)
 (H/'evidence/p09-scene-extension.json').write_text(json.dumps(report,indent=2)+'\n')
 shutil.copy2(DATA/'generated/210.text.bin',H/'generated/210.text.bin')
 shutil.copy2(DATA/'generated/manifest.json',H/'generated/p09-scenes.json')
 inputs={str(B/name):digest for name,digest in seal['files'].items()}
 inputs.update({str(p):sha(p) for p in [S/'p09-domain-adapter/src/module990.sc',S/'p09-domain-adapter/manifest.json',DATA/'extend_dialogue.py',*sorted((DATA/'generated').rglob('*'))] if p.is_file()})
 inputs.update(canonical)
 gdd=Path('/workspace/shared/cakood/ending-seam-20261005/current-gdd.txt');assert sha(gdd)==GDD_PIN;inputs[str(gdd)]=GDD_PIN
 (H/'snapshot/p09-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
 print('Composed P09 against sealed P08; old domain methods unchanged')
if __name__=='__main__':main()
