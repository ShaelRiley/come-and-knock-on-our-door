#!/usr/bin/env python3
"""Guarded, additive P07 host reconstruction; a pinned base is never modified."""
from pathlib import Path
import sys,re,json,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'tools'))
from source_tools import methods,spans,tokens

def insert(s,code):
 ts=tokens(s);d=0
 for t in ts[2:]:
  if t.group()=='(':d+=1
  elif t.group()==')':
   d-=1
   if d==0:return s[:t.end()]+'\n'+code+'\n'+s[t.end():]
 raise RuntimeError('signature')
def merge(s,new):
 old=methods(s)
 for n,(a,b) in sorted(spans(s).items(),key=lambda x:x[1][0],reverse=True):
  if n in new:s=s[:a]+new[n]+s[b:]
 end=next(iter(spans(s,'class').values()))[1]-1
 return s[:end]+'\n'+'\n'.join(new[n] for n in new if n not in old)+'\n'+s[end:]
def replace(s,a,b,count=1):
 if s.count(a)!=count:raise RuntimeError(('guard',a,s.count(a),count))
 return s.replace(a,b)
def append_properties(s,code):
 a=s.index('(properties');b=s.index(')',a);return s[:b]+'\n'+code+'\n'+s[b:]
def append_locals(s,code):
 ts=tokens(s);i=next(i for i,t in enumerate(ts) if t.group()=='(' and ts[i+1].group()=='local');d=0
 for t in ts[i:]:
  if t.group()=='(':d+=1
  elif t.group()==')':
   d-=1
   if d==0:return s[:t.start()]+'\n'+code+'\n'+s[t.start():]
 raise RuntimeError('locals')
def balanced(s):
 d=0
 for t in tokens(s):
  d+=int(t.group()=='(')-int(t.group()==')')
  if d<0:raise RuntimeError('unbalanced')
 if d:raise RuntimeError(('unbalanced',d))
def derive(check=False):
 output={}
 def emit(path,value):output[path]=value.encode() if isinstance(value,str) else value
 for name,digest in json.loads((H/'SOURCE-INPUTS.json').read_text()).items():
  if hashlib.sha256((H/name).read_bytes()).hexdigest()!=digest:raise RuntimeError('immutable input changed '+name)
 import subprocess
 subprocess.run([sys.executable,'-B',str(H/'generate_routes.py'),'--check'],check=True,cwd=H)
 for p in (H/'templates').glob('*.sc.in'):
  balanced(p.read_text())
 base=H/'snapshot/base';combined=(base/'module987.sc').exists()
 for p in base.glob('*.sc'):emit(H/'src'/p.name,p.read_bytes())
 main=(base/'main.sc').read_text()
 if not combined:
  from adapt_return_caption import transform
  main=transform(main)
  if hashlib.sha256(main.encode()).hexdigest()!='bf77821651a56cd1429b8bd99ff85a36b04931ac8679d0ec753aae330f37b608':raise RuntimeError('caption output identity')
 m=methods(main);new={}
 hooks={
  'bridgeActAtArrival':'(if (and p07 (p07 h7Barrier:)) (return 0))',
 'hostActNow':'(if (and p07 (p07 h7Barrier:)) (return 0))',
 'uiHostAct':'(if (and p07 (p07 h7Barrier:)) (return 0))',
 'uiChooseObject':'(if (and p07 (p07 h7FirstNoun: item uiVerb uiNounA)) (return 0))',
 'bridgeBegin':'(if p07 (p07 h7CancelReader:) (p07 h7RetireLaugh:))',
 'dialoguePresented':'(if p07 (p07 h7Presented: uiDocument uiPage (dialogue sdGeneration?)))',
 'writeSave':'(if (and p07 (not (p07 h7SaveReady:))) (return 0))',
 'readSave':'(if (and p07 (p07 h7Critical?)) (return 0))',
 'uiHostChoice':'(if (and p07 (p07 h7Choice: context id)) (return 0)) (if (and p07 (p07 h7Barrier:)) (return 0))',
 'uiHostConfirm':'(if (and p07 (p07 h7Barrier:)) (return 0))',
 'p02ObjectLocation':'(if (and p07 (>= obj 86) (<= obj 94)) (return (p07 h7Location: obj)))',
 'campaignHeld':'(if (and p07 (>= obj 86) (<= obj 94)) (return 0))',
 'campaignReachable':'(if (and p07 (>= obj 86) (<= obj 94)) (return (p07 h7Reachable: obj)))',
 'uiHostItemLabel':'(if (and p07 (>= arg1 86) (<= arg1 94)) (return (p07 h7Label: arg1)))',
 'uiHostShortLabel':'(if (and p07 (>= arg1 86) (<= arg1 94)) (return (p07 h7ShortLabel: arg1)))',
 'approachX':'(if (and p07 (or (and (>= arg1 86) (<= arg1 94)) (and (== arg1 2) (== location 2)))) (return (p07 h7ApproachX: arg1)))',
 'approachY':'(if (and p07 (or (and (>= arg1 86) (<= arg1 94)) (and (== arg1 2) (== location 2)))) (return (p07 h7ApproachY: arg1)))',
 
 }
 for name,code in hooks.items():new[name]=insert(m[name],code)
 new['h7BaseControls']=replace(m['uiHostWorldControls'],'(method (uiHostWorldControls','(method (h7BaseControls')
 new['uiHostWorldControls']='(method (uiHostWorldControls) (self h7BaseControls:) (if p07 (p07 h7Controls:)) (return 1))'
 new['h7BasePreparationHint']=replace(m['p03PreparationHint'],'(method (p03PreparationHint','(method (h7BasePreparationHint')
 new['p03PreparationHint']='(method (p03PreparationHint) (if (and p07 p02PlanAgreed (== location 2) (not onApron)) (p07 h7HintMenu:) (return 0)) (return (self h7BasePreparationHint:)))'
 new['p05Initialize']=m['p05Initialize'][:-1]+'\n(= p07 (ScriptID 988 0)) (p07 h7Init: self p05)\n)'
 new['bridgeActAtArrival']=replace(new['bridgeActAtArrival'],'(if (and p05 (p05 hDispatch: action obj target))','(if (and p07 (p07 h7Dispatch: action obj target)) (return 0))\n(if (and p05 (p05 hDispatch: action obj target))')
 # Overlay strictly after original kitchen300, before P03 props and actors.
 new['drawKitchen']=replace(m['drawKitchen'],'(DrawCel 300 0 0 0 0 -1 0)','(DrawCel 300 0 0 0 0 -1 0)\n(if p07 (p07 h7Render:))')
 new['drawKitchen']=new['drawKitchen'][:-1]+'\n(if p07 (p07 h7DrawBunny:))\n)'
 new['uiHostClosed']=m['uiHostClosed'][:-1]+'\n(if p07 (p07 h7Closed:))\n)'
 new['p05RestoreBegin']=replace(m['p05RestoreBegin'],'(= p05 (ScriptID 985 0))','(= p07 (ScriptID 988 0)) (if p07 (p07 h7RestoreValid: 0)) (= p05 (ScriptID 985 0))')
 if combined:
  new['p05RestoreBegin']=replace(new['p05RestoreBegin'],'(= p06 (ScriptID 987 0))','(= p06 (ScriptID 987 0)) (if p06 (p06 h6RestoreValid: 0))')
  new['p05RestoreBegin']=replace(new['p05RestoreBegin'],'(return (p06 h6RestoreBegin: self p05))','(if (not (p06 h6RestoreBegin: self p05)) (return 0)) (return (p07 h7RestoreBegin: self p05))')
 else:
  new['p05RestoreBegin']=replace(new['p05RestoreBegin'],'(if p05 (return (p05 hRestoreBegin: self))) (return 0)','(if (or (not p05) (not (p05 hRestoreBegin: self))) (return 0)) (return (p07 h7RestoreBegin: self p05))')
 new['p05RestoreValidate']=insert(m['p05RestoreValidate'],'(if (and p07 (not (p07 h7RestoreValidate:))) (self p05RestoreReject:) (return 0))')
 new['p05RestoreValidate']=replace(new['p05RestoreValidate'],'(= uiFailure 10) (= dirty 1) (return 0))','(= uiFailure 10) (= dirty 1) (if p07 (p07 h7RestoreValid: 0)) (return 0))')
 new['p05RestoreReject']=insert(m['p05RestoreReject'],'(if p07 (p07 h7RestoreValid: 0))')
 for n in ['uiBuildFocus','uiTurnPage','uiRender']:
  new[n]=replace(m[n],'pTos uiChoiceContext\n            ldi '+('225' if combined else '218'),'pTos uiChoiceContext\n            ldi 228')
 # Retirement hooks discard only P07's own pending occurrence, no new callback.
 for n in ['uiClose','uiHostMenu','voiceOff','motionCancel']:
  new[n]=insert(new.get(n,m[n]),'(if p07 (p07 h7RetireLaugh:))')
 new['speechPoll']=insert(m['speechPoll'],'(if p07 (p07 h7AudioTick:))')
 new.update(methods((H/'templates/main.sc.in').read_text()))
 main=append_properties(merge(main,new),'p07 0');balanced(main);emit(H/'src/main.sc',main)
 # Scene extension and two precise partial-output aliases. All canonical arrays exact.
 scene=(base/'module982.sc' if combined else H/'snapshot/scene/module982.sc').read_text();sm=methods(scene)
 aliases={'sdRoute':'(if (== document 971) (return 1059)) (if (== document 972) (return 1062))','sdPageCount':'(if (== document 971) (return 3)) (if (== document 972) (return 2))'}
 scene=merge(scene,{n:insert(sm[n],s) for n,s in aliases.items()});balanced(scene);emit(H/'src/module982.sc',scene)
 # Preserve985as sole Bunny and Contest authority. Add one invitation topic.
 s=(base/'module985.sc').read_text();old=methods(s);n={}
 if not combined:
  ext=methods((H/'snapshot/scene/module985.sc').read_text())
  for name in ['hStaticCount','hStaticFirst','hStaticLoad']:n[name]=ext[name]
 anchor='else (hHost uiAddChoice: 1 "Will you stand on the listening mark and tell us whether the words are clear?" 0 1)) (return 1))'
 n['hTopics']=replace(old['hTopics'],anchor,anchor.replace(' (return 1))','\n(if (hHost p07?) ((hHost p07?) h7AddBunnyChoice:)) (return 1))'))
 s=merge(s,n);balanced(s);emit(H/'src/module985.sc',s)
 domain=(H/'snapshot/domain/module988.sc').read_text();original=methods(domain)
 domain=append_locals(domain,(H/'templates/host-locals.inc').read_text());domain=append_properties(domain,(H/'templates/host-properties.inc').read_text())
 additions=methods((H/'templates/host.sc.in').read_text()+'\n'+(H/'templates/visual.sc.in').read_text()+'\n'+(H/'generated/routes.sc.inc').read_text())
 if set(original)&set(additions):raise RuntimeError('domain method overwrite')
 domain=merge(domain,additions);balanced(domain)
 if any(methods(domain)[n]!=v for n,v in original.items()):raise RuntimeError('original domain changed')
 emit(H/'src/module988.sc',domain)
 selectors=json.loads((base/'selectors.json').read_text())
 for n,i in json.loads((H/'snapshot/domain/selectors.json').read_text()).items():
  if n in selectors:
   if selectors[n]!=i:raise RuntimeError(('selector name conflict',n))
  else:
   if i in selectors.values():raise RuntimeError(('selector ID conflict',n,i))
   selectors[n]=i
 needed=set()
 for p in sorted(k for k in output if k.parent==H/'src' and k.suffix=='.sc'):
  ss=output[p].decode();needed.update(methods(ss))
  for props in re.findall(r'\(properties\s+([^)]*)\)',ss):needed.update([t.group() for t in tokens(props)][::2])
 for i,n in enumerate(sorted(needed-selectors.keys()),2200):
  if i>2399 or i in selectors.values():raise RuntimeError(('host allocation',n,i))
  selectors[n]=i
 emit(H/'selectors.json',json.dumps(selectors,indent=2)+'\n')
 emit(H/'evidence/derivation.json',json.dumps({'status':'DERIVED','combined_p06':combined,'main_changed_methods':sorted(new),'preserved_p07_domain_methods':len(original),'new_p07_host_methods':len(additions),'native_acceptance':False},indent=2)+'\n')
 expected_sources={p.name for p in output if p.parent==H/'src'}
 if check and {p.name for p in (H/'src').glob('*.sc')}!=expected_sources:raise RuntimeError('Derived source membership differs')
 for path,data in output.items():
  if check:
   if not path.is_file() or path.is_symlink() or path.read_bytes()!=data:raise RuntimeError('Generated output differs from guarded templates: '+str(path.relative_to(H)))
  else:path.write_bytes(data)
 print('PASS_GUARDED_DERIVATION_CHECK' if check else 'P07 host derived; combined P06:',combined)
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();derive(check=args.check)
