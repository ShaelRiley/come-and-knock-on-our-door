#!/usr/bin/env python3
"""Exact-input guarded source composition. Default inactive. No live installation."""
from pathlib import Path
import json,re,sys,hashlib,shutil,subprocess,struct
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'tools'))
import pack
from extract_sci11 import extract

def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prefix(s,name,body):
 pat=r'(\(method \('+re.escape(name)+r'(?:\s[^)]*)?\)\n?)';matches=list(re.finditer(pat,s));need(len(matches)==1,'Ambiguous host method '+name)
 m=matches[0];return s[:m.end()]+'\n'+body+'\n'+s[m.end():]
def apply(sources):
 main=sources['main.sc'];host=sources['module985.sc']
 for filename in('main.sc','module985.sc'):
  sources[filename]=sources[filename].replace('(script# '+('0'if filename=='main.sc'else'985')+')','(script# '+('0'if filename=='main.sc'else'985')+')\n(use "module943")',1)
 main=sources['main.sc'];host=sources['module985.sc']
 # Successful actual986 commit only. Music return value never changes game result.
 needle=' (if ok (= hContestBlocked 1)) (return ok))';need(host.count(needle)==1,'Commit-boundary changed')
 host=host.replace(needle,' (if ok (rbHostCommitted operation hContest) (= hContestBlocked 1)) (return ok))')
 # Resume only after the entire host restore validator (including P06) succeeds.
 line=next(line for line in main.splitlines()if line.startswith('(method (p05RestoreValidate)'))
 need(line.endswith('(return 1))'),'Restore-validator terminal changed')
 replacement=line[:-len('(return 1))')]+'(if (not (rbRestoreResume (ScriptID 986 0))) (self p05RestoreReject:) (return 0)) (return 1))'
 main=main.replace(line,replacement,1)
 needle=' (if p05 (return (p05 hRestoreBegin: self))) (return 0))'
 if needle in main:
  need(main.count(needle)==1,'P05 early replay boundary changed')
  main=main.replace(needle,' (if p05 (if (not (p05 hRestoreBegin: self)) (return 0)) (return (rbRestoreBegin responsiveSound))) (return 0))')
 else:
  needle=' (return (p06 h6RestoreBegin: self p05)))'
  need(main.count(needle)==1,'P06 early replay boundary changed')
  main=main.replace(needle,' (if (not (p06 h6RestoreBegin: self p05)) (return 0)) (return (rbRestoreBegin responsiveSound)))')
 main=prefix(main,'writeSave','''(if (rbStatus 23) (= audioSaveResult 0))
(if (not (rbSaveAdmit)) (= audioSaveResult 0) (= dirty 1) (return 0))''')
 # readSave alone may open a chooser with a validated, fully retired failed owner.
 a=main.index('    (method (readSave)');b=main.index('    ; Delivered offset',a)
 read=main[a:b];anchor='            pushi 693\n            push0\n            self 4'
 need(read.count(anchor)==1,'Load chooser boundary changed')
 read=read.replace(anchor,'            push1\n            pushSelf\n            calle rbLoadChooser, 2')
 main=main[:a]+read+main[b:]

 main=prefix(main,'musicSelectOwner','''(if (rbStatus 23)
 (if opening (self musicStopOwner:)
 else (= musicOwner responsiveSound) (= musicOwnerKind 3) (rbHostStatus self) (return 1)))''')
 main=prefix(main,'musicRequests','''(if (rbStatus 23)
 (rbHomeRequest audioDesired)
 (rbPreference (/ (* masterVolume (if audioDuckTicks 60 else 100)) 100) (if musicMuted 1 else 0) (if (or paused menuOpen) 1 else 0))
 (return 1))''')
 main=prefix(main,'musicStopOwner','''(if (rbStatus 23) (rbDisable) (= musicOwner (ScriptID 981 0)) (= musicOwnerKind 0) (= musicChooserKind 0) (return 1))''')
 main=prefix(main,'audioPoll','''(if (rbStatus 23)
 (self musicSelectOwner:) (self musicRequests:)
 (rbPoll (rbStatus 3) (rbStatus 4) (ScriptID 986 0))
 (rbHostStatus self))''')
 main=prefix(main,'audioHolds','''(if (rbStatus 23) (self musicRequests:))''')
 main=prefix(main,'audioTrace','''(if (rbStatus 23) (return 0))''')
 main=prefix(main,'musicBeforeChooser','''(if (rbStatus 23)
 (self syncAudio:) (self musicSelectOwner:) (self audioHolds:)
 (if (not (rbBeforeChooser)) (= musicUnavailable 1) (return 0))
 (= musicChooserKind 3) (return 1))''')
 main=prefix(main,'musicAfterChooser','''(if (rbStatus 23)
 (= musicChooserKind 0)
 (if (not (rbAfterChooser)) (= musicUnavailable 1) (return 0))
 (self musicRequests:) (return 1))''')
 main=prefix(main,'audioRestore','''(if (rbStatus 23)
 ; P05 already retired PCM/transient work. Wait for hRestoreValidate admission.
 (= musicOwner responsiveSound) (= musicOwnerKind 3) (= musicChooserKind 0)
 (= audioPCMheld 0) (= audioPending 0) (= audioDuckTicks 0) (= audioLastPCM -1)
 (= audioPhase opening) (rbHomeRequest audioDesired) (rbHostStatus self) (return 1))''')
 main=prefix(main,'musicRetry','''(if (rbStatus 23)
 (if (rbRetry responsiveSound) (rbHostStatus self) (= dirty 1) (return 1))
 (rbHostStatus self) (return 0))''')
 # Replace only the exact footer entry; preserve disabled legacy owner rendering.
 footer='            L_13fd: pToa musicUnavailable'
 need(main.count(footer)==1,'Music footer anchor changed')
 draw_index=json.loads((H/'generated/api.json').read_text())['943']['rbDrawStatus']
 main=main.replace(footer,'            L_13fd: push1\n            pTos musicUnavailable\n            calle rbDrawStatus, 2\n            bt L_141e\n            pToa musicUnavailable')
 main=prefix(main,'p05RestoreReject','''(rbRestoreReject responsiveSound)''')
 main+='\n; Inactive by default. No rbInit call exists in any host source.\n(instance responsiveSound of Sound (properties number 151 loop -1 priority 100 vol 0))\n'
 sources['main.sc']=main;sources['module985.sc']=host
 return sources

def build_fixture(name,folder):
 selectors=json.loads((folder/'selectors.json').read_text());src={p.name:p.read_text()for p in(folder/'src').glob('*.sc')};src=apply(src)
 B=H/f'build/{name}'
 if B.exists():shutil.rmtree(B)
 (B/'src').mkdir(parents=True);(B/'compiled').mkdir()
 for n in(941,942,943):src[f'module{n}.sc']=(H/f'generated/module{n}.sc').read_text()
 src['module940.sc']=(H/'inputs/accepted-v4/generated/module940.sc').read_text()
 for n,s in src.items():(B/'src'/n).write_text(s)
 existing=sorted(int(p.stem[6:])for p in(folder/'src').glob('module*.sc'))
 order=[n for n in existing if n!=985]+[940,941,942,943,985,0]
 # Canonical species ordering is retained; all added modules are class-free.
 owners=[0,0,980,981,982,983,984,985,986]+([987]if 987 in existing else [])
 pack.SELECTORS=selectors
 pack.pack_resources({(6,996):struct.pack('<'+'H'*len(owners)*2,*sum(([0,n]for n in owners),[])),(6,997):pack.selector_resource()},B)
 selector_list=[dict(name=n,selector_id=i)for n,i in sorted(selectors.items(),key=lambda x:x[1])];(B/'selector-list.json').write_text(json.dumps(selector_list,indent=2)+'\n')
 (B/'game.ini').write_text('[Game]\nName=Guarded inactive '+name+' music adapter\nLanguage=sci\n[Script]\nn000=main\n'+''.join(f'n{n}=module{n}\n'for n in order if n))
 receipts=[]
 compiler=H/'toolchain/scicompile'
 for n in order:
  source=B/f'src/{"main"if not n else "module"+str(n)}.sc';target=B/f'compiled/{n}.scr.bin'
  p=subprocess.run([str(compiler),'--version','sci11',str(B),str(source),str(target)],capture_output=True,text=True)
  (B/f'compile-{n}.log').write_text(p.stdout+p.stderr);need(not p.returncode and '[error]'not in p.stdout+p.stderr,p.stdout+p.stderr)
  layout=extract(target,Path(str(target)+'.hep'),B/'selector-list.json');size=target.stat().st_size+Path(str(target)+'.hep').stat().st_size+2;need(size<65536,'SCI segment overflow')
  receipts.append(dict(module=n,source_sha256=sha(source),script_sha256=sha(target),heap_sha256=sha(Path(str(target)+'.hep')),combined_bytes=size))
 # Exact unchanged protected module source and freshly compiled bytes, not splices.
 before=json.loads((folder/'build/coherent/compile-receipt.json').read_text())['modules']
 for n in existing:
  if n==985:continue
  row=next(r for r in receipts if r['module']==n);old=next(r for r in before if r['module']==n)
  for key in('source_sha256','script_sha256','heap_sha256'):need(row[key]==old[key],f'{name} protected{n} {key} changed')
 for n in(940,941,942,943):
  current=next(r for r in receipts if r['module']==n)
  for key,tail in(('script_sha256',''),('heap_sha256','.hep')):need(current[key]==sha(H/f'build/fresh/compiled/{n}.scr.bin{tail}'),f'{name} additive{n} emitted universe mismatch')
 need('rbInit'not in src['main.sc'].replace('; Inactive by default. No rbInit call exists in any host source.',''),'Host activated candidate')
 report=dict(status='PASS_FRESH_COMPILE',scope='GUARDED_SOURCE_COMPOSITION_ONLY',host=name,modules=receipts,selector_source_sha256=sha(folder/'selectors.json'),new_selectors=0,activation=False,native_tested=False)
 (B/'compile-receipt.json').write_text(json.dumps(report,indent=2)+'\n');print(name,receipts[-1]['combined_bytes'],'Main segment bytes',flush=True);return report
if __name__=='__main__':
 need(not sys.flags.optimize,'optimized Python forbidden')
 reports=[build_fixture('p05-composition',H/'inputs/p05'),build_fixture('p06-composition',H/'inputs/p06-frozen')]
 (H/'evidence/host-composition.json').write_text(json.dumps(reports,indent=2)+'\n')
