#!/usr/bin/env python3
import re
import build_catalog as c
H=c.H

def body(s,name):
 m=re.search(r'(?m)^\(procedure \('+name+r'(?:\s|\))',s);assert m
 b=s.find('\n(procedure (',m.start()+1)
 return s[m.start():b if b>=0 else len(s)]
def main():
 src=(H/'src/module944.sc').read_text()
 src=src.replace('; Phase A production director. Full-score/ending edges remain unadmitted.','; Full approved-score production director; native/listening acceptance remains separate.')
 src=src.replace('(local\n','(local\n psDirty = 1\n psEnded = 0\n psPassage = 0\n [psFacts 24]\n [psReceipts 15]\n',1)
 src=src.replace('(use "module948")','(use "module948")\n(use "module996")\n(use "module997")')
 comm='''(procedure (psCommitted host sourceScript event receiptHi receiptLo arg0 arg1 &tmp domain)
 (if (or (not (psHost host)) psRestoring psChooser (== psMode 1) (== psMode 2)) (return 0))
 (if (== sourceScript 985)
  (if (or arg0 arg1 (not (or (== event 3) (== event 4) (== event 6) (== event 8) (== event 9)))) (return 0))
  (= domain (ScriptID 986 0))
  (if (or (!= receiptHi (domain vcRead: 2)) (!= receiptLo (domain vcRead: 3))
   (and (== receiptHi 0) (== receiptLo 0))) (return 0))
  (if (== event 4)
   (if (not (rbEvent 2 domain 1)) (return 0))
  else (if (not (rbHostCommitted event domain)) (return 0)))
  (= psDirty 1) (return 1))
 (if (== sourceScript 0)
  (if (or receiptHi (!= receiptLo (host p02Revision?))
   (!= arg0 (host location?)) (!= arg1 (host onApron?))
   (not (or (== event 453) (and (>= event 1) (<= event 7)) (and (>= event 20) (<= event 26))))) (return 0))
  (= psDirty 1) (return 1))
 (if (or (< sourceScript 993) (> sourceScript 997)
  (< receiptHi 0) (< receiptLo 0) (and (== receiptHi 0) (== receiptLo 0))
  (not (psEventValid sourceScript event receiptHi receiptLo arg0 arg1))) (return 0))
 (if (not (psConsume sourceScript event receiptHi receiptLo)) (return 1))
 (= psDirty 1)
 (if (and (== sourceScript 994) (== event 8)) (= psPassage 128))
 (if (and (>= sourceScript 996) (or (== event 14) (and (== event 9) (== arg0 6))))
  ; Explicit player Skip retires current finite content promptly.
  (rbPresentation 3 0 0 0) (= psCue 0) (= psRow 0) (= psPassage 0)
  (if (== psMode 4) (return 1)) (= psMode 0) (= psEnded 1))
 (return 1))'''
 src=c.replace_proc(src,'psCommitted',comm)
 src=c.replace_proc(src,'psPoll','''(procedure (psPoll host now)
 (if (or (not (psHost host)) psRestoring psChooser) (return 0))
 (psObserve host)
 (if (and psPassage (== (rbStatus 0) psPassage) (== (rbStatus 26) 1))
  (= psPassage 0) (= psDirty 1))
 (if (and psDirty (not (host opening?))) (psResolve host 0))
 (psPreferences host)
 (rbPoll (rbStatus 3) (rbStatus 4) (ScriptID 986 0))
 (if (rbStatus 5) (= psUnavailable 1) (host musicUnavailable: 1 dirty: 1))
 (return (not psUnavailable)))''')
 src=src.replace('(or (host paused?) (host menuOpen?)) 1 else 0)', '(or (host paused?) (host menuOpen?) (and (== psMode 3) ((ScriptID 996 0) p14Paused?)) (and (== psMode 4) ((ScriptID 997 0) p14Paused?))) 1 else 0)')
 # Opening pair helpers and their exact tuple coordinates remain unchanged.
 for name in ('psSaveAdmit','psRestoreBegin','psRestoreResume'):
  text=body(src,name)
  text=text.replace('(> psMode 2)','(> psMode 4)')
  text=text.replace('(if psMode\n','(if (or (== psMode 1) (== psMode 2))\n')
  src=c.replace_proc(src,name,text)
 # Reconcile without dispatching old event callbacks; retained receipt watermarks
 #consume historical opportunities even when a saved bridge is retired.
 txt=body(src,'psRestoreResume')
 txt=txt.replace('(= psRestoring 0) (= psChooser 0) (= psUnavailable 0)','(= psRestoring 0) (= psChooser 0) (= psUnavailable 0)\n (= psPassage 0) (= psDirty 1) (psObserve host) (psResolve host 2)')
 src=c.replace_proc(src,'psRestoreResume',txt)
 src=c.replace_proc(src,'psReplayBegin','''(procedure (psReplayBegin host kind)
 (if (or (!= kind 2) (not (psHost host)) psRestoring psChooser
  (== psMode 1) (== psMode 2) (== psMode 4)
  (not ((ScriptID 997 0) h14ReplayActive:))
  (not ((ScriptID 997 0) h14ReplayValid:))) (return 0))
 (= psReturnCue psCue) (= psReturnRow psRow)
 (if (not (rbPresentation 0 121 0 0)) (= psUnavailable 1) (return 0))
 (= psMode 4) (= psCue 121) (= psRow 0) (= psDirty 0) (return 1))''')
 src=c.replace_proc(src,'psReplayEnd','''(procedure (psReplayEnd host reason &tmp target row ok)
 (if (or (not (psHost host)) psRestoring psChooser (!= psMode 4) (< reason 0) (> reason 2)) (return 0))
 (= target psReturnCue) (= row psReturnRow)
 (= ok (rbPresentation 3 0 0 0))
 (= psMode 0) (= psCue 0) (= psRow 0) (= psPassage 0)
 (= psReturnCue 0) (= psReturnRow 0) (= psDirty 1) (= psEnded (if ((ScriptID 996 0) p14Ready:) 1 else 0))
 ; A completed household returns to the ending/menu's quiet state; replay never
 ;restarts the quiet tag, credits or celebration as a campaign reward.
 (if (and ok target (< target 119))
  (= ok (rbScoreRequest target row 2))
  (if ok (= psCue target) (= psRow row)))
 (return ok))''')
 src=c.replace_proc(src,'psStateValid','''(procedure (psStateValid host)
 (if (or (not (psHost host)) (< psMode 0) (> psMode 4)
  (< psPairValid 0) (> psPairValid 1)) (return 0))
 (if psPairValid
  (if (or (not (or (== psMode 1) (== psMode 2))) (not psChooser)) (return 0))
 else
  (if (or psPairMode psPairCard psPairElapsed psPairHeld psPairNative
   psPairOwner psPairOffset psPairGenerationHi psPairGenerationLo) (return 0)))
 (if (or (== psMode 1) (== psMode 2)) (return (and (== (rbStatus 1) 4) (psOpeningValid host))))
 (if (host opening?) (return 0))
 (if (and psCue (!= (pmCue psCue 8 0) 1)) (return 0))
 (if (== psMode 3) (if (not ((ScriptID 996 0) p14Ready:)) (return 0)))
 (if (== psMode 4) (if (not ((ScriptID 997 0) h14ReplayValid:)) (return 0)))
 (return (!= psCue 100)))''')
 private=(H/'src/full-director.inc').read_text()
 private=private.replace('((ScriptID 985 0) hVCThinking?)','(and (>= ((ScriptID 986 0) vcRead: 92) 2) (<= ((ScriptID 986 0) vcRead: 92) 4))')
 cases=[]
 for script,prefix in[(993,'p11'),(994,'p12'),(995,'p13'),(996,'p14'),(997,'p14')]:
  cases.append(f'''({script}
   (= count (d {prefix}EventCount?))
   (if (or (< count 1) (> count 2)) (return 0))
   (for ((= i 0)) (< i count) ((++ i))
    (if (and (== (d {prefix}Event: i) event) (== (d {prefix}EventSerialHi: i) hi)
     (== (d {prefix}EventSerialLo: i) lo) (== (d {prefix}EventArg: i 0) a) (== (d {prefix}EventArg: i 1) b)) (return 1))))''')
 private=private.replace('@EVENT_VALIDATORS@','\n'.join(cases))
 src+='\n'+private
 txt=body(src,'psBeforeChooser');txt=txt.replace(' (psPairClear)', ' (if (not (or (== psMode 1) (== psMode 2))) (= psPassage 0) (= psDirty 1) (psObserve host) (psResolve host 2))\n (psPairClear)',1);src=c.replace_proc(src,'psBeforeChooser',txt)
 src=src.replace('(procedure (psStateValid host)\n', '(procedure (psStateValid host)\n (if (not (psLedgerValid)) (return 0))\n')
 # Every actual Begin records a fresh semantic transition even if the previous
 #opening was a detached replay of the current cue.
 txt=body(src,'psOpeningFinish');txt=txt.replace('(= psMode 0) (= psCue 0)', '(= psDirty 1) (= psMode 0) (= psCue 0)');src=c.replace_proc(src,'psOpeningFinish',txt)
 (H/'generated/module944.sc').write_text(src)
 print('Full director generated;A04 pair helpers unchanged')
if __name__=='__main__':main()
