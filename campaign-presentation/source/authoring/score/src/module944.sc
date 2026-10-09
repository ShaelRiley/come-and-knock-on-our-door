;;; Sierra Script 1.0 - (do not remove this comment)
; Phase A production director. Full-score/ending edges remain unadmitted.
(script# 944)
(use "module943")
(use "module948")
(public psInit 0 psCommitted 1 psPoll 2 psPreferences 3 psOpeningBegin 4 psOpeningPosition 5 psOpeningHold 6 psOpeningNext 7 psOpeningFinish 8 psSaveAdmit 9 psBeforeChooser 10 psAfterChooser 11 psRestoreBegin 12 psRestoreResume 13 psReplayBegin 14 psReplayEnd 15 psRead 16 psStop 17)
(local
 psReady = 0
 psCue = 0
 psRow = 0
 psMode = 0
 psUnavailable = 0
 psReturnCue = 0
 psReturnRow = 0
 psRestoring = 0
 psChooser = 0
 psLastWhole = -1
 psLastMuted = -1
 psLastPaused = -1
 ; Paired checkpoint r1: independently witnessed Main/native state.
 psPairValid = 0
 psPairMode = 0
 psPairCard = 0
 psPairElapsed = 0
 psPairHeld = 0
 psPairNative = 0
 psPairOwner = 0
 psPairOffset = 0
 psPairGenerationHi = 0
 psPairGenerationLo = 0
)
(procedure (psInit host actualSound)
 (if (or psReady (!= host (ScriptID 0 0)) (!= actualSound (ScriptID 0 1))) (return 0))
 ; Main runs actual domain/PCM initialization first; no saved admission bit substitutes.
 (if (or (not (pmVerify)) (not (proc945_6 host)) (not (proc946_4 host))
  (not (rbAdmitProduction host actualSound))) (= psUnavailable 1) (return 0))
 (= psReady 1) (= psCue 0) (= psRow 0) (= psMode 0) (= psUnavailable 0)
 (= psReturnCue 0) (= psReturnRow 0) (= psRestoring 0) (= psChooser 0)
 (psPairClear)
 (= psLastWhole -1) (= psLastMuted -1) (= psLastPaused -1)
 (return 1))
(procedure (psCommitted host sourceScript event receiptHi receiptLo arg0 arg1 &tmp domain)
 (if (or (not (psHost host)) psRestoring psChooser psMode
  (!= sourceScript 985) (not (or (== event 3) (== event 4) (== event 6) (== event 8) (== event 9)))
  arg0 arg1) (return 0))
 (= domain (ScriptID 986 0))
 (if (or (!= receiptHi (domain vcRead: 2)) (!= receiptLo (domain vcRead: 3))
  (and (== receiptHi 0) (== receiptLo 0))) (return 0))
 ; Real R3 ledger rechecks committed phase, exchange, reason and meter; no mutation.
 (if (not (rbHostCommitted event domain)) (return 0))
 (= psCue (if (== (rbStatus 2) 152) (+ 140 (rbStatus 9)) else 102))
 (= psRow (if (== (rbStatus 2) 152) (rbStatus 9) else (host audioDesired?)))
 (return 1))
(procedure (psPoll host now)
 (if (or (not (psHost host)) psRestoring psChooser) (return 0))
 ; Main supplies its existing clock; the finite backend reports its own position.
 ; The Phase A gameplay disposition is quiet P01, then the admitted HOME return.
 (if (and (== psMode 0) (not (host opening?)) (host houseEntered?) (== psCue 0))
  (if (rbScoreRequest 102 (host audioDesired?) 0) (= psCue 102) (= psRow (host audioDesired?))))
 (psPreferences host)
 (rbPoll (rbStatus 3) (rbStatus 4) (ScriptID 986 0))
 (if (rbStatus 5) (= psUnavailable 1) (host musicUnavailable: 1 dirty: 1))
 (return (not psUnavailable)))
(procedure (psPreferences host &tmp whole muted paused pcm)
 (if (not (psHost host)) (return 0))
 (= whole (host masterVolume?)) (= muted (host musicMuted?))
 (= paused (if (host opening?) 0 else (if (or (host paused?) (host menuOpen?)) 1 else 0)))
 (if (or (< whole 0) (> whole 100) (< muted 0) (> muted 1)) (return 0))
 (= pcm (ScriptID 980 0))
 ; Preserve the original sixty-percent duck target, observing the actual PCM owner.
 (if (or (> (host audioDuckTicks?) 0)
  (and (or (== (pcm lane?) 1) (== (pcm lane?) 2)) (> (pcm ownerGain:) 0)))
  (= whole (/ (* whole 60) 100)))
 (if (and (== whole psLastWhole) (== muted psLastMuted) (== paused psLastPaused)) (return 1))
 (if (not (rbPreference whole muted paused)) (return 0))
 (= psLastWhole whole) (= psLastMuted muted) (= psLastPaused paused)
 (return 1))
(procedure (psOpeningBegin host mode)
 (if (or (not (psHost host)) psRestoring psChooser psMode (< mode 0) (> mode 1)
  (!= (host opening?) 1) (host creditCard?) (host creditElapsed?) (host creditHeld?)
  (!= (host replayOpening?) mode)) (return 0))
 (if (and (== mode 0) (or (host initialized?) (host initCount?))) (return 0))
 (= psReturnCue (if mode psCue else 0)) (= psReturnRow (if mode psRow else 0))
 (if (not (psPreferences host)) (= psUnavailable 1) (return 0))
 (if (not (rbPresentation 0 100 0 0)) (= psUnavailable 1) (return 0))
 (psPairClear)
 (= psMode (+ mode 1)) (= psCue 100) (= psRow 0) (= psUnavailable 0)
 (return 1))
(procedure (psOpeningPosition host)
 (if (or (not (psHost host)) (not (or (== psMode 1) (== psMode 2))) psUnavailable) (return -1))
 (return (rbPresentationPosition)))
(procedure (psOpeningHold host held)
 (if (or (not (psOpeningValid host)) psRestoring psChooser (< held 0) (> held 1)
  (!= held (host creditHeld?))) (return 0))
 (if (not (rbPresentation 2 0 0 held)) (= psUnavailable 1) (return 0)) (return 1))
(procedure (psOpeningNext host card held)
 (if (or (not (psOpeningValid host)) psRestoring psChooser (< card 1) (> card 9)
  (!= card (host creditCard?)) (host creditElapsed?) (!= held (host creditHeld?))) (return 0))
 (if (not (rbPresentation 1 100 (* card 360) held)) (= psUnavailable 1) (return 0)) (psPairClear) (return 1))
(procedure (psOpeningFinish host reason returnMode &tmp target row ok)
 (if (or (not (psHost host)) psRestoring psChooser (< reason 0) (> reason 3)
  (< returnMode 0) (> returnMode 1)) (return 0))
 (if (== psMode 0) (return 1))
 (if (or (!= psMode (+ returnMode 1)) (!= (host replayOpening?) returnMode)
  (!= (host opening?) 1)) (return 0))
 (= target psReturnCue) (= row psReturnRow)
 (proc945_5 host 2) (proc946_3 host 2)
 (= ok (rbPresentation 3 0 0 0))
 ; Restore invoking menu/pause preference before a captured return target can start.
 (= psLastPaused (if (or (host paused?) (host menuOpen?)) 1 else 0))
 (if ok (rbPreference (rbStatus 20) (rbStatus 21) psLastPaused))
 (psPairClear)
 (= psMode 0) (= psCue 0) (= psRow 0) (= psReturnCue 0) (= psReturnRow 0)
 (if (and ok returnMode target)
  (= ok (rbScoreRequest target row 2))
  (if ok (= psCue target) (= psRow row)))
 (if (not ok) (= psUnavailable 1)) (return ok))
(procedure (psSaveAdmit host &tmp observed)
 (if (not (psStateValid host)) (return 0))
 (if (or (not (psHost host)) psRestoring psUnavailable (not (pmVerify))
  (not (proc945_6 host)) (not (proc946_4 host)) (not (rbSaveAdmit))) (return 0))
 (if (or (< psMode 0) (> psMode 2) (< psChooser 0) (> psChooser 1)) (return 0))
 (if psMode
  (if (not (psOpeningValid host)) (return 0))
  (= observed (rbPresentationPosition))
  (if (< observed 0) (return 0))
  ; Main and the MIDI callback are independent clocks. Capture their actual
  ; paused pair once; never rewrite either timeline or infer one from the other.
  (if psChooser
   (if (not psPairValid)
    (if (not (psPairCapture host observed)) (return 0)))
   (if (not (psPairMatches host observed)) (return 0))))
 (return 1))
(procedure (psBeforeChooser host kind &tmp ok)
 (if (or (not (psHost host)) psRestoring psChooser (< kind 0) (> kind 1)
  (not (pmVerify))) (return 0))
 (psPairClear)
 ; UI recovery only. A rejected domain/audience ledger cannot authorize Save or
 ; playback, but it must not prevent selecting a different valid native save.
 ; Existing host retirement runs first; immutable catalog and actual stopped
 ; canonical ownership are freshly verified by the broker's narrow Load path.
 (if (and (== kind 1) (== (rbStatus 1) 3))
  (proc945_5 host 3) (proc946_3 host 3)
  (= ok (rbLoadChooser host))
  (if ok (= psChooser 1)) (return ok))
 (if (or (not (proc945_6 host)) (not (proc946_4 host))) (return 0))
 (proc945_5 host 3) (proc946_3 host 3)
 (= ok (rbBeforeChooser))
 (if ok (= psChooser 1)) (return ok))

(procedure (psAfterChooser host outcome)
 (if (or (not (psHost host)) psRestoring (not psChooser) (< outcome 0) (> outcome 2)) (return 0))
 (if (not (rbAfterChooser)) (= psUnavailable 1) (= psChooser 0) (return 0))
 (= psChooser 0) (psPairClear) (return 1))
(procedure (psRestoreBegin host actualSound)
 (if (or (!= host (ScriptID 0 0)) (!= actualSound (ScriptID 0 1)) (not psReady)
  (!= (host musicOwner?) actualSound) (!= (host musicOwnerKind?) 3)
  psRestoring (not psChooser) (not (pmVerify))) (return 0))
 (if (or (not (proc945_7 host 0)) (not (proc946_5 host 0))) (return 0))
 ; Verify the serialized pair before the broker advances its lifetime generation.
 (if psMode
  (if (not (psPairMatches host (rbPresentationPosition))) (return 0)))
 (if (not (rbRestoreBegin actualSound)) (= psUnavailable 1) (return 0))
 ; The genuine restore creates exactly one new broker lifetime, not a new pair.
 (if psMode
  (= psPairGenerationHi (rbStatus 3)) (= psPairGenerationLo (rbStatus 4)))
 (= psRestoring 1) (return 1))
(procedure (psRestoreResume host domain986 &tmp observed)
 (if (not (psStateValid host)) (return 0))
 (if (or (not (psHost host)) (!= domain986 (ScriptID 986 0)) (not psRestoring)
  (not psChooser) (not (pmVerify))
  (not (proc945_7 host 1)) (not (proc946_5 host 1))
  (not (proc945_6 host)) (not (proc946_4 host))) (return 0))
 (if psMode
  (if (not (psOpeningValid host)) (return 0))
  (= observed (rbPresentationPosition))
  (if (not (psPairMatches host observed)) (return 0)))
 (if (not (rbRestoreResume domain986)) (= psUnavailable 1) (return 0))
 (psPairClear)
 (= psRestoring 0) (= psChooser 0) (= psUnavailable 0)
 (= psLastWhole -1) (= psLastMuted -1) (= psLastPaused -1)
 (return (psPreferences host)))
(procedure (psReplayBegin host kind)
 ; Finale121 transport is intentionally not admitted before the opening native gate.
 (return 0))
(procedure (psReplayEnd host reason) (return 0))
(procedure (psRead field)
 (switch field (0 (return psReady)) (1 (return psCue)) (2 (return psRow))
  (3 (return psMode)) (4 (return psUnavailable)) (5 (return (psOpeningPosition (ScriptID 0 0))))
  (6 (return psRestoring)) (7 (return psChooser))) (return -1))
(procedure (psStop host reason)
 (if (or (!= host (ScriptID 0 0)) (< reason 0) (> reason 2)) (return 0))
 (psPairClear)
 (proc945_5 host 8) (proc946_3 host 8)
 (if (== reason 1)
  ; Preserve admission and durable ledger so a genuine earlier save remains loadable.
  (rbFail 8) (= psUnavailable 1) (= psChooser 0) (= psRestoring 0)
  (return 1))
 (rbDisable)
 (= psMode 0) (= psCue 0) (= psRow 0) (= psReturnCue 0) (= psReturnRow 0)
 (= psChooser 0) (= psRestoring 0) (= psReady 0) (return 1))
(procedure (psHost host)
 (return (and psReady (== host (ScriptID 0 0))
  (== (host musicOwner?) (ScriptID 0 1)) (== (host musicOwnerKind?) 3))))
(procedure (psOpeningValid host)
 (return (and (psHost host) (or (== psMode 1) (== psMode 2)) (== psCue 100)
  (== (host opening?) 1) (== (host replayOpening?) (- psMode 1))
  (>= (host creditCard?) 0) (<= (host creditCard?) 9)
  (>= (host creditElapsed?) 0) (< (host creditElapsed?) 360)
  (>= (host creditHeld?) 0) (<= (host creditHeld?) 1))))

(procedure (psStateValid host)
 (if (or (not (psHost host)) (< psMode 0) (> psMode 2)) (return 0))
 (if (or (< psPairValid 0) (> psPairValid 1)) (return 0))
 (if psPairValid
  (if (or (not psMode) (not psChooser)) (return 0))
 else
  (if (or psPairMode psPairCard psPairElapsed psPairHeld psPairNative
          psPairOwner psPairOffset psPairGenerationHi psPairGenerationLo) (return 0)))
 (if psMode (return (and (== (rbStatus 1) 4) (psOpeningValid host))))
 (return (and (not (host opening?)) (!= (rbStatus 1) 4) (!= psCue 100))))

; Private pair helpers. No new class, selector, public export or playback owner.
(procedure (psPairClear)
 (= psPairValid 0)
 (= psPairMode 0)
 (= psPairCard 0)
 (= psPairElapsed 0)
 (= psPairHeld 0)
 (= psPairNative 0)
 (= psPairOwner 0)
 (= psPairOffset 0)
 (= psPairGenerationHi 0)
 (= psPairGenerationLo 0)
 (return 1))
(procedure (psPairCapture host observed &tmp offset frozen)
 (if (or psPairValid (not psChooser) (not (psOpeningValid host))
         (!= (rbStatus 1) 4) (not (rbStatus 7)) (rbStatus 8)) (return 0))
 (= offset (rbStatus 24)) (= frozen (rbStatus 25))
 ; Both coordinates belong to this exact source suffix. There is no numerical
 ; jitter allowance: native regression/end bounds remain broker-enforced.
 (if (or (< offset 0) (> offset 3240) (!= (mod offset 360) 0)
         (< frozen 0) (< observed offset) (> observed 3600)
         (!= observed (+ offset frozen))
         (< (+ (* (host creditCard?) 360) (host creditElapsed?)) offset)
         (!= (rbStatus 0) (pmOpening (/ offset 360) 0))) (return 0))
 (= psPairMode psMode) (= psPairCard (host creditCard?))
 (= psPairElapsed (host creditElapsed?)) (= psPairHeld (host creditHeld?))
 (= psPairNative observed) (= psPairOwner (rbStatus 0)) (= psPairOffset offset)
 (= psPairGenerationHi (rbStatus 3)) (= psPairGenerationLo (rbStatus 4))
 (= psPairValid 1) (return 1))
(procedure (psPairMatches host observed)
 (if (or (!= psPairValid 1) (not psChooser) (not (psOpeningValid host))
         (!= psPairMode psMode) (!= psPairCard (host creditCard?))
         (!= psPairElapsed (host creditElapsed?)) (!= psPairHeld (host creditHeld?))
         (< observed 0) (!= psPairNative observed)
         (!= psPairOwner (rbStatus 0)) (!= psPairOffset (rbStatus 24))
         (!= psPairNative (+ psPairOffset (rbStatus 25)))
         (!= psPairGenerationHi (rbStatus 3)) (!= psPairGenerationLo (rbStatus 4))) (return 0))
 (return 1))
