from pathlib import Path
import sys,re,json,hashlib,shutil
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'tools'))
(H/'VERIFICATION.json').write_text(json.dumps({'status':'BUILDING_SOURCE','native_acceptance':False})+'\n')
if sys.flags.optimize:raise RuntimeError('Optimized Python is forbidden')
from validate_selected_inputs import check
check(H)
from source_tools import methods,spans,merge_methods,tokens

def insert_body(s,code):
 ts=tokens(s);depth=0
 for q in ts[2:]:
  if q.group()=='(':depth+=1
  elif q.group()==')':
   depth-=1
   if depth==0:return s[:q.end()]+'\n'+code+'\n'+s[q.end():]
 raise Exception('signature')

def balanced(s):
 depth=0
 for t in tokens(s):
  if t.group()=='(':depth+=1
  elif t.group()==')':depth-=1
  if depth<0:raise AssertionError(('unbalanced',s[:t.start()].count('\n')+1))
 assert depth==0,depth

contest=(H/'CONTEST-INTEGRATION.json').exists()
courtyard=(H/'COURTYARD-INTEGRATION.json').exists()
drawer=(H/'DRAWER-INTEGRATION.json').exists()
stage=(H/'STAGE-INTEGRATION.json').exists()
main=(H/'snapshot/r2/main.sc').read_text();m=methods(main);new={}
hooks={
 'p04Initialize':'(self p05Initialize:)',
 'uiHostAct':'(if p05 (if (p05 hBarrier:) (return 0)))',
 'hostActNow':'(if (and p05 (p05 hBarrier:)) (return 0))',
 'bridgeActAtArrival':'(if (and p05 (p05 hBarrier:)) (return 0))',
 'bridgeBegin':'(if p05 (p05 hCancelReader:))',
 'uiHostChoice':'(if (and p05 (p05 hBarrier:)) (return 0)) (if (and p05 (p05 hChoice: context id)) (return 0))',
 'dialoguePresented':'(if p05 (p05 hPresented: uiDocument uiPage (dialogue sdGeneration?)))',
 'writeSave':'(if (and p05 (not (p05 hSaveReady:))) (return 0))',
 'uiHostConfirm':'(if (and p05 (p05 hBarrier:)) (return 0))',
 'readSave':'(if (and p05 (p05 hCritical?)) (return 0))',
 'replay':'(if (not (self p05RestoreBegin:)) (self p05RestoreReject:) (return 0))',
 'p02ObjectLocation':'(if (and p05 (or (and p02PlanAgreed (or (== obj 2) (== obj 28))) (and (>= obj 63) (<= obj 72)))) (return (p05 hLocation: obj)))',
 'uiAddControl':'(if (and p05 p02PlanAgreed (== action 1) (or (== payload 2) (== payload 28)) (!= location (p05 hLocation: payload))) (return 1))',
 'livingPerson':'(if (and p05 (== who 2) (!= (p05 hBunnyRoom?) 1)) (return 0))',
}
visual=H/'visual-work/visual-methods.sc.inc'
if visual.exists():
 hooks.update({
  'uiHostWorldControls':'(if (and p05 p02PlanAgreed (p05 hWorldControls:)) (return 0))',
  'drawWorld':'(if (and p05 p02PlanAgreed (p05 hRenderWorld:)) (return 0))',
  'uiHostItemLabel':'(if (and p05 (>= arg1 63) (<= arg1 72)) (return (p05 hLabel: arg1)))',
  'uiHostShortLabel':'(if (and p05 (>= arg1 63) (<= arg1 72)) (return (p05 hShortLabel: arg1)))',
  'approachX':'(if (and p05 p02PlanAgreed (== location 5) (not onApron)) (return (p05 hApproachX: arg1)))',
  'approachY':'(if (and p05 p02PlanAgreed (== location 5) (not onApron)) (return (p05 hApproachY: arg1)))',
 })
 hooks['uiHostAct']+=' (if p05 (p05 hCaptureTarget: (if arg3 arg3 else arg2)))'
if contest:
 hooks['uiHostChoice']='(if (and p05 (p05 hVCChoice: context id)) (return 0)) '+hooks['uiHostChoice']
 hooks['p03PreparationHint']='(if (and p05 (p05 hBarrier:)) (return 0)) (if (and p05 p02PlanAgreed (== location 5) (not (& (p05 p05Flags:) 4))) (p05 hHintNext:) (return 0))'
 hooks['p02Hint']='(if (and p05 (p05 hBarrier:)) (return 0))'
 hooks['p02Journal']='(if (and p05 (p05 hBarrier:)) (return 0))'
 hooks['startReplay']='(if (and p05 (p05 hBarrier:)) (return 0))'
 hooks['renderCaption']='(if (and p05 (p05 hVCHud:)) (return 0))'
if stage:
 hooks['advance']='(if p05 (p05 hStageTick: arg1))'
 for method in ['uiClose','uiHostMenu','speechCancel','voiceOff','motionCancel']:
  hooks[method]='(if p05 (p05 hStageRetire:)) '+hooks.get(method,'')
 hooks['writeSave']+=' (if p05 (p05 hStageRetire:))'
if drawer:
 for name in ['uiHostWorldControls','drawWorld','approachX','approachY']:
  hooks[name]=hooks[name].replace('p05 p02PlanAgreed','p05')
if courtyard:
 hooks['uiHostWorldControls']='(if (and p05 (p05 hCourtControls:)) (return 0)) '+hooks['uiHostWorldControls']
 hooks['drawWorld']='(if (and p05 (p05 hCourtRender:)) (return 0)) '+hooks['drawWorld']
 for name,method in [('approachX','hCourtApproachX'),('approachY','hCourtApproachY')]:
  hooks[name]=f'(if (and p05 (== location 4) (not onApron)) (return (p05 {method}: arg1))) '+hooks[name]
 hooks['motionScale']='(if (and p05 (not onApron) (or (== location 4) (== location 5))) (return 127))'
for method in ['advance','audioPoll','speechPoll','hostObserve']:
 hooks[method]='(if (and p05 (p05 hFailure?)) (return 0)) '+hooks.get(method,'')
hooks['drawWorld']='(if (and p05 (p05 hFailure?)) (p05 hFailureWorld:) (return 0)) '+hooks['drawWorld']
for name,code in hooks.items():
 assert name in m,name;new[name]=insert_body(m[name],code)
# Preserve old validity and before-travel checks before handling new actions.
s=new['bridgeActAtArrival'];anchor='(self bridgeBegin:)';assert s.count(anchor)==1
new['bridgeActAtArrival']=s.replace(anchor,'(if (and p05 (p05 hDispatch: action obj target)) (return 0))\n'+anchor,1)
# Read/close happens before escort completion and cannot award a source receipt.
new['uiHostClosed']=m['uiHostClosed'][:-1]+'\n(if p05 (p05 hClosed:))\n)'
# Existing replay retirement/validation runs first; only reissue current source ticket afterward.
s=new['replay'];needle='pushi #p04Restore\n            push0\n            self 4';assert s.count(needle)==1
new['replay']=s.replace(needle,needle+'\n            pushi #p05RestoreValidate\n            push0\n            self 4')
new['p05RestoreValidate']='(method (p05RestoreValidate) (if (and p05 (not (p05 hRestoreValidate:))) (= uiPanel 0) (= uiBackPanel 0) (= uiChoiceCount 0) (= bridgeReaderActive 0) (= bridgeQueueCount 0) (= bridgeQueueIndex 0) (= uiFailure 10) (= dirty 1) (return 0)) (return 1))'
for name in ['uiBuildFocus','uiTurnPage','uiRender']:
 s=new.get(name,m[name]);needle='pTos uiChoiceContext\n            ldi 208';assert s.count(needle)==1,(name,s.count(needle));new[name]=s.replace(needle,'pTos uiChoiceContext\n            ldi '+('218' if contest else '214'))
# Respect all original busy/motion guards before current actor speech authority.
s=m['dialogueCanSpeak'];anchor='(if (or opening (!= motionPhase 0)) (return 0))';assert s.count(anchor)==1
new['dialogueCanSpeak']=s.replace(anchor,anchor+'\n(if (and p05 p02PlanAgreed (== who 2)) (return (if (and (not onApron) (== location (p05 hBunnyRoom?))) 1 else 0)))\n(if (and p05 p02PlanAgreed (== who 5)) (return (if (and (not onApron) (== location (p05 hMiloRoom?))) 1 else 0)))')
if courtyard:
 # Change only the room4 corridor; keep every other legacy movement path.
 s=m['motionRequest'];anchor='ldi 132\n            aTop motionTargetY';assert s.count(anchor)==1
 new['motionRequest']=s.replace(anchor,'pushi #p05WalkCorridor\n            push0\n            self 4\n            aTop motionTargetY')
 s=m['motionArrive'];anchor='(= motionTargetY 132)';assert s.count(anchor)==1
 new['motionArrive']=s.replace(anchor,'(= motionTargetY (self p05WalkCorridor:))')
 new['p05WalkCorridor']='(method (p05WalkCorridor) (return (if (and p05 (== location 4) (not onApron)) 141 else 132)))'
main=merge_methods(main,new)
main=main.replace('p04 0 p04Invalid 0 p04HostError 0 p04LastStatus 0','p04 0 p04Invalid 0 p04HostError 0 p04LastStatus 0\n        p05 0')
helpers=(H/'main_helpers.sc.in').read_text();main=merge_methods(main,methods(helpers))
# Without visual module, the focus hook is still callable safely with no new game route.
if not visual.exists():main=merge_methods(main,{'p05FocusMark':'(method (p05FocusMark) (return 0))'})
balanced(main);(H/'src/main.sc').write_text(main)
domain=(H/'snapshot/domain/module985.sc').read_text()
locals=(H/'host_locals.inc').read_text();props=(H/'host_properties.inc').read_text();extra=(H/'host_methods.sc.in').read_text()
if visual.exists():
 visual_source=visual.read_text()
 # Explicit integration metadata correction: world porch keeps old object17;
 # object11 remains exclusively the shared apron Return action. Pixels unchanged.
 for a,b in [('(self hControl: 11 7 44 44 124)','(self hControl: 17 7 44 44 124)'),('(11 (return 29))','(17 (return 29))'),('(11 (return 135))','(17 (return 135))'),('(11 (return "PORCH"))','(17 (return "PORCH"))')]:
  assert visual_source.count(a)==(2 if a=='(11 (return "PORCH"))' else 1),(a,visual_source.count(a));visual_source=visual_source.replace(a,b)
 # Hardware is visible but non-interactive until the P02 plan is agreed.
 visual_source=visual_source.replace('(self hControl: 69 253 120 283 134)\n    (self hControl: 69 273 134 297 144)','(if (hHost p02PlanAgreed?) (self hControl: 69 253 120 283 134) (self hControl: 69 273 134 297 144))')
 visual_source=visual_source.replace('(if (self hCartVisible:) (self hControl:', '(if (and (hHost p02PlanAgreed?) (self hCartVisible:)) (self hControl:')
 pos=visual_source.index('(method (hWorldControls');end=visual_source.index('(method (',pos+8)
 prefix=visual_source[pos:end].replace('(if (self hKitVisible:)','(if (and (hHost p02PlanAgreed?) (self hKitVisible:))')
 visual_source=visual_source[:pos]+prefix+visual_source[end:]
 if drawer:
  visual_source=visual_source.replace('(self hControl: 9 298 44 320 144)','(self hControl: 9 298 44 320 144) (self hInvitationDrawerControls:)')
  for name in ['hApproachX','hApproachY']:
   mm=methods(visual_source)[name];value=74 if name.endswith('X') else 139
   mm=insert_body(mm,f'(if (or (== obj 27) (== obj 24)) (return {value}))')
   a,b=spans(visual_source)[name];visual_source=visual_source[:a]+mm+visual_source[b:]
  visual_source=visual_source.replace('(DrawCel 304 0 0 0 0 -1 0)','(DrawCel 304 0 0 0 0 -1 0) (self hDrawInvitationDrawer:)')
  raw=(H/'snapshot/drawer/host-integration.sc.in').read_text()
  visual_source+='\n(method (hDrawInvitationDrawer &tmp drawerCel)\n'+raw+'\n(return 1))\n'
  visual_source+='''
(method (hInvitationDrawerControls)
 (if (and (hHost p02MiloShown?) (hHost p02DrawerOpen?) (not (hHost p02MasterHeld?)))
  (hHost uiAddControl: 1 27 48 46 61 76 (hHost uiHostItemLabel: 27))
  (hHost uiAddControl: 1 27 61 46 68 53 (hHost uiHostItemLabel: 27))
  (hHost uiAddControl: 1 27 61 68 68 76 (hHost uiHostItemLabel: 27))
  (hHost uiAddControl: 1 27 68 46 79 76 (hHost uiHostItemLabel: 27))
  (hHost uiAddControl: 1 24 61 53 68 68 (hHost uiHostShortLabel: 24))
 else (hHost uiAddControl: 1 27 48 46 79 76 (hHost uiHostItemLabel: 27)))
 (return 1))
'''
 # One reusable room-prop owner for ordinary and theatrical renderers.
 mm=methods(visual_source)['hRenderWorld'];a=mm.index('(DrawCel 304');b=mm.index('; Closed/active mouths')
 backdrop=mm[a:b];replace=mm[:a]+'(self hGarageBackdrop:)\n    '+mm[b:]
 start,end=spans(visual_source)['hRenderWorld'];visual_source=visual_source[:start]+replace+visual_source[end:]
 visual_source+='\n(method (hGarageBackdrop)\n'+backdrop+'(return 1))\n'
 extra+='\n'+visual_source
 extra=extra.replace('(if (!= who 28) (return 0))','(if (or (!= who 28) (!= hMiloRoom 5)) (return 0))')
 for filename,dest in [('visual-locals.inc','local'),('visual-properties.inc','prop')]:
  p=H/'visual-work'/filename
  if p.exists():
   if dest=='local':locals+='\n'+p.read_text()
   else:props+='\n'+p.read_text()
if courtyard:
 court=(H/'snapshot/courtyard/host-integration.sc.in').read_text()
 for name,replacement in methods((H/'courtyard_controls.sc.in').read_text()).items():
  a,b=spans(court)[name];court=court[:a]+replacement+court[b:]
 for name,value in [('hCourtApproachX',114),('hCourtApproachY',140)]:
  a,b=spans(court)[name];replacement=insert_body(court[a:b],f'(if (or (and (>= obj 64) (<= obj 68)) (== obj 70)) (return {value}))');court=court[:a]+replacement+court[b:]
 extra+='\n'+court
if contest:
 extra+='\n'+(H/'generated/static/guard-methods.inc').read_text()+'\n'+(H/'generated/static/module985-methods.inc').read_text()
 props+='\nhStaticParseOK 0\n'
 locals+='\n'+(H/'generated/static/guard-locals.inc').read_text()+'\n'+(H/'generated/static/label-locals.inc').read_text()
 extra+='\n'+(H/'contest_methods.sc.in').read_text()+'\n'+(H/'contest_labels.sc.inc').read_text()
 props+='\n'+(H/'contest_properties.inc').read_text()
 table=(H/'snapshot/contest-scene/route-tables.inc').read_text()
 count=int(re.search(r'\[vcSceneRoutes (\d+)\]',table)[1])
 locals+='\n'+(H/'contest_locals.inc').read_text()+'\n'+table
 domain=domain.replace('(class P05State',f'(define VC_ROUTE_WORDS {count})\n(class P05State',1)
 if stage:
  stage_methods=methods((H/'snapshot/stage/stage-methods.sc.inc').read_text())
  a,b=spans(extra)['hVCHud'];extra=extra[:a]+stage_methods.pop('hVCHud')+extra[b:]
  extra+='\n'+'\n'.join(stage_methods.values())
  a,b=spans(extra)['hRenderWorld'];extra=extra[:a]+insert_body(extra[a:b],'(if (self hVCStageRender:) (return 1))')+extra[b:]
 ex=methods(extra)
 ex['hContestFlags']='(method (hContestFlags) (return (if (and hContest hContestEnabled) (hContest vcFlags:) else 0)))'
 ex['hBarrier']='(method (hBarrier) (return (if (or hCritical hFailure hContestBlocked p05Busy p05Loading (not p05Ready) (and hContestEnabled (or (hContest vcBusy?) (not (hContest vcReady?))))) 1 else 0)))'
 ex['hInit']=ex['hInit'].replace('(= hEnabled (self hRoutesReady:))','(= hEnabled (self hRoutesReady:)) (self hVCInit:)')
 ex['hClosed']=insert_body(ex['hClosed'],'(if hVCSession (self hVCClosed:) (return 1))')
 ex['hPresented']=insert_body(ex['hPresented'],'(if hVCSession (return (self hVCPresented: document page generation)))')
 ex['hSaveReady']=insert_body(ex['hSaveReady'],'(if (or (not (self hVCValidateWorld:)) (not (hContest vcSaveReady:))) (return 0))')
 ex['hRestoreBegin']=ex['hRestoreBegin'].replace('(hHost p05RetireTransient:)','(if (not (self hVCAfterRestore:)) (= hFailure 20)) (hHost p05RetireTransient:)')
 ex['hRestoreValidate']=insert_body(ex['hRestoreValidate'],'(if (not (self hVCRestoreValidate:)) (return 0))')
 ex['hStartContest']='''(method (hStartContest &tmp code)
 (if (not (self hVCAdmission:)) (return (self hRun: 16 0)))
 (if (hContest vcRead: 6) (return (self hVCMenu:)))
 (if (not (self hBegin:)) (return 0))
 (self hSnapshot:) (= hCritical 1)
 (= code (self p05RequestContest:))
 (if (!= code CODE_CONTEST_REQUESTED) (= hCritical 0) (return 0))
 (self p05ContestTicket:) (self hCaptureTicket:)
 (if (or (not (hContest vcIntroduce: 1 1)) (not (self hVCCommit:)))
  (self hRollback:) (= hCritical 0) (return 0))
 (self hInput: 4 hTicketHi hTicketLo)
 (if (!= (self p05AcknowledgeContest: 0) CODE_CONTEST_REQUEST_ACKNOWLEDGED)
  (= hFailure 29) (= hCritical 0) (return 0))
 (= hCritical 0) (= hVCSession 1) (= hContestBlocked 1)
 (self hForgetReader:) (return (self hVCShow: 0)))'''
 for name,(a,b) in sorted(spans(extra).items(),key=lambda x:x[1][0],reverse=True):
  extra=extra[:a]+ex[name]+extra[b:]
idx=domain.index('(local ');end=domain.index(')',idx);domain=domain[:end]+' '+locals+domain[end:]
idx=domain.index('(properties');end=domain.index(')',idx);domain=domain[:end]+'\n'+props+domain[end:]
end=spans(domain,'class')['P05State'][1]-1;domain=domain[:end]+'\n'+extra+'\n'+domain[end:]
balanced(domain);(H/'src/module985.sc').write_text(domain)
for n in [980,981,983,984]:shutil.copy2(H/f'snapshot/r2/module{n}.sc',H/f'src/module{n}.sc')
shutil.copy2(H/('snapshot/contest-scene/module982.sc' if contest else 'snapshot/scene/module982.sc'),H/'src/module982.sc')
if contest:shutil.copy2(H/'snapshot/contest/module986.sc',H/'src/module986.sc')
print('source derived with',len(new),'guarded Main hooks')

# Small readonly saved-table accessors; original property/local prefixes are intact.
for number,classname in [(981,'MusicTransport'),(982,'SceneDialogue')]:
 path=H/f'src/module{number}.sc';source=path.read_text()
 at=spans(source,'class')[classname][1]-1
 source=source[:at]+'\n'+(H/f'generated/static/module{number}-methods.inc').read_text()+'\n'+source[at:]
 if number==982:
  current=methods(source)
  for name,code in [('sdRoute','(if (not ((ScriptID 985 0) hStaticRange: 1 document 1)) (return -1))'),('sdPageCount','(if (or (< document 1) (> document 881)) (return 0)) (if (not ((ScriptID 985 0) hStaticRange: 2 document 1)) (return 0))')]:
   method=current[name];anchor='(return [sdStarts document])' if name=='sdRoute' else '(if (< (self sdRoute: document) 0) (return 0))'
   method=method.replace(anchor,code+'\n'+anchor);a,b=spans(source)[name];source=source[:a]+method+source[b:]
  method=methods(source)['sdLoad'];anchor='(= sdEntry [sdPageData index])'
  guard='(if (or (not ((ScriptID 985 0) hStaticRange: 3 index 8)) (not ((ScriptID 985 0) hStaticRange: 5 row 1)) (not ((ScriptID 985 0) hStaticRange: 6 row 1)) (not ((ScriptID 985 0) hStaticRange: 7 row 1))) (= sdFailure 5) (return 0))\n'
  method=method.replace(anchor,guard+anchor);a,b=spans(source)['sdLoad'];source=source[:a]+method+source[b:]
 balanced(source);path.write_text(source)
