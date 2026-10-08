;;; Sierra Script 1.0 - (do not remove this comment)
; Original shared PCM ownership module. No Sierra framework or game assets.
(script# 980)
(public presentationAudio 0)
(class PresentationAudio
    (properties
        token 0 lane 0 speaker 0 mouth 0 syncTime -1 syncCue -1 dirty 0
        voiceVolume 80 audienceVolume 80 effectsVolume 70 masterVolume 100
        voiceMuted 0 audienceMuted 0 effectsMuted 0
        pendingLaugh 0 laughToken 0 laughDue 0 laughReady 0 laughStrength 0
        laughModule 0 laughNoun 0 laughVerb 0 laughCond 0 laughSeq 0
        lastFoleyEvent -1 lastFoleyOrdinal -1 lastLaughEvent -1
        rejected 0 played 0 lastGain -1 silentClock 0 voiceOffset 0 voiceEnd 0
        dMode 0 dIndex 0 dTicks 0 dNoun 0 dGen -1 dPage -1
    )
    (method (pcmPosition &tmp position)
        (= position (DoAudio 6))
        (if (and (== lane 1) silentClock (>= position 0))
            (= position (+ position voiceOffset))
            (if (>= position voiceEnd) (return -1)))
        (return position))
    (method (cancel reason)
(if dMode (proc998_0)) (= dMode 0) (= dIndex 0) (= dTicks 0) (= dNoun 0) (= dGen -1) (= dPage -1)

        (= token (mod (+ token 1) 30000))
        (DoAudio 3) (DoSync 2)
        (= lastGain -1) (= silentClock 0) (= voiceOffset 0) (= lane 0) (= mouth 0) (= syncTime -1) (= syncCue -1)
        (= pendingLaugh 0) (= laughReady 0) (= dirty 1)
        (return token))
    (method (ownerGain &tmp gain)
        (= gain 0)
        (switch lane
            (1 (if (not voiceMuted) (= gain voiceVolume)))
            (2 (if (not audienceMuted) (= gain audienceVolume)))
            (3 (if (not effectsMuted) (= gain effectsVolume)))
            (4 (if (not effectsMuted) (= gain effectsVolume))))
        (return (/ (* gain masterVolume) 100)))
    (method (refreshGain &tmp gain position)
(if (and dMode (== (self ownerGain:) 0)) (self cancel: 1) (return 0))

        ; A native GMM settings reset can raise the shared speech-category gain.
        ; Nonvoice zero must mean no stream and no latent audience request.
        (if (or audienceMuted (== (/ (* audienceVolume masterVolume) 100) 0))
            (= pendingLaugh 0) (= laughReady 0))
        (if lane
            (= gain (self ownerGain:))
            (if (and (!= lane 1) (== gain 0))
                (DoAudio 3) (= lane 0) (= lastGain 0) (return 0))
            ; Zero-valued PCM keeps the native clock without an audible stream
            ; that stock GMM's mixer-settings reset could accidentally reveal.
            (if (and (== lane 1) (== gain 0) (not silentClock))
                (= position (DoAudio 6))
                (if (>= position 0)
                    (= voiceOffset position) (= silentClock 1)
                    (DoAudio 3) (DoAudio 8 0) (DoAudio 2 911 1 1 0 1)))
            (if (and (== lane 1) silentClock) (= gain 0))
            (DoAudio 8 gain) (= lastGain gain)))
    (method (setOff owner off)
        (switch owner
            (1 (= voiceMuted (if off 1 else 0)))
            (2 (= audienceMuted (if off 1 else 0))
                (if audienceMuted
                    (= pendingLaugh 0)
                    (if (== lane 2) (DoAudio 3) (= lane 0))))
            (3 (= effectsMuted (if off 1 else 0))
                (if (and effectsMuted (or (== lane 3) (== lane 4)))
                    (DoAudio 3) (= lane 0))))
        (self refreshGain:))
    (method (startVoice module noun verb condition seq who)
(if (== module 927)
 (if (or (!= noun 1) (!= seq 1) (!= who 3)) (self cancel: 1) (return 0))
 (return (self dStart: verb condition)))

        (self cancel: 1)
        (= lane 1) (= speaker who) (= mouth 0)
        (DoSync 0 self module noun verb condition seq) (DoSync 1 self)
        (if (== (self ownerGain:) 0)
            (= silentClock 1) (= voiceOffset 0)
            (self refreshGain:) (DoAudio 2 911 1 1 0 1)
        else (self refreshGain:) (DoAudio 2 module noun verb condition seq))
        (++ played) (= dirty 1) (return token))
    (method (queueLaugh eventId strength module noun verb condition seq now expected)
        (if (or (!= expected token) (== eventId lastLaughEvent))
            (++ rejected) (return 0))
        (if (or audienceMuted (== (/ (* audienceVolume masterVolume) 100) 0))
            (= lastLaughEvent eventId) (= pendingLaugh 0) (= laughReady 0)
            (++ rejected) (return 0))
        (if (and pendingLaugh (< strength laughStrength)) (++ rejected) (return 0))
        (= pendingLaugh 1) (= laughToken token)
        (= laughStrength strength)
        (= laughModule module) (= laughNoun noun) (= laughVerb verb)
        (= laughCond condition) (= laughSeq seq)
        ; Consumption belongs to this occurrence, even if a newer scene drops it.
        (= lastLaughEvent eventId)
        (if (== lane 0) (= laughDue now) (= laughReady 1)
        else (= laughReady 0))
        (return 1))
    (method (requestFoley eventId ordinal module noun verb condition seq foreground age expected)
        (if (or (!= expected token) (< age 0)
                (> age (if foreground 3 else 2))
                (and (== eventId lastFoleyEvent) (== ordinal lastFoleyOrdinal)))
            (++ rejected) (return 0))
        ; Consume a current contact even when protected speech makes it inaudible.
        (= lastFoleyEvent eventId) (= lastFoleyOrdinal ordinal)
        (if (or effectsMuted (== (/ (* effectsVolume masterVolume) 100) 0)
                (== lane 1) (and (not foreground) (!= lane 0)))
            (++ rejected) (return 0))
        (if lane (DoAudio 3))
        (= lane (if foreground 3 else 4)) (= mouth 0)
        (self refreshGain:) (DoAudio 2 module noun verb condition seq)
        (++ played) (return 1))
    (method (poll now expected &tmp pos nextMouth laughAge)
(if dMode
 (if (!= expected token) (++ rejected) (return 0))
 (return (self dPoll: now)))

        (if (!= expected token) (++ rejected) (return 0))
        (if (or audienceMuted (== (/ (* audienceVolume masterVolume) 100) 0))
            (= pendingLaugh 0) (= laughReady 0))
        (if (and lane (!= lane 1) (== (self ownerGain:) 0)) (self refreshGain:))
        (= pos (self pcmPosition:))
        (if (== lane 1)
            (if (== pos -1)
                (if silentClock (DoAudio 3)) (= silentClock 0) (= voiceOffset 0)
                (= lane 0) (= mouth 0) (DoSync 2) (= dirty 1)
                (if pendingLaugh (= laughDue now) (= laughReady 1))
            else
                (= nextMouth mouth)
                (while (and (!= syncTime -1) (<= syncTime pos))
                    (= nextMouth syncCue) (DoSync 1 self))
                (if (!= nextMouth mouth) (= mouth nextMouth) (= dirty 1)))
        else
            (if (and lane (== pos -1))
                (= lane 0)
                (if (and pendingLaugh (not laughReady))
                    (= laughDue now) (= laughReady 1))))
        (if (and pendingLaugh laughReady)
            ; Signed 16-bit subtraction preserves short ages across GetTime wrap.
            (= laughAge (- now laughDue))
            (if (or (!= laughToken token) audienceMuted (> laughAge 90) (< laughAge 0))
                (= pendingLaugh 0) (++ rejected)
            else
                (if (and (== lane 0) (>= laughAge 8))
                    (= pendingLaugh 0) (= lane 2)
                    (self refreshGain:)
                    (DoAudio 2 laughModule laughNoun laughVerb laughCond laughSeq)
                    (++ played))))
        (return lane))

    (method (cancelFoley)
        ; An interaction/motion barrier cannot cancel another owner's voice/laugh.
        (if (or (== lane 3) (== lane 4))
            (DoAudio 3) (= lane 0) (= lastGain -1)))

(method (dStart generation page &tmp duration)
 ; Only reserved927 can enter; the bank checks exact current reader/Frankie/owner.
 (self cancel: 1) (= lane 1) (= speaker 3) (= mouth 0)
 (if (== (self ownerGain:) 0) (= lane 0) (return token))
 (= duration (proc998_1 generation page))
 (if (< duration 1) (= lane 0) (return token))
 (= voiceEnd duration) (= dMode 1) (= dIndex 0) (= dGen generation) (= dPage page)
 (self dNext:) (= dirty 1) (return token))
(method (dNext &tmp noun ticks)
 (= noun (proc998_3 dIndex 0)) (= ticks (proc998_3 dIndex 1))
 (if (or (< noun 0) (< ticks 1))
  (DoAudio 3) (DoSync 2) (= lane 0) (= dMode 0) (= mouth 0)
  (= syncTime -1) (= syncCue -1) (= dirty 1) (proc998_0) (return 0))
 (if (or (> noun 120) (> ticks 4000)) (self cancel: 1) (return 0))
 (= dNoun noun) (= dTicks ticks) (++ dIndex)
 (DoAudio 3) (DoSync 2) (= mouth 0) (= syncTime -1) (= syncCue -1)
 (if noun
  (DoSync 0 self 927 noun 1 0 1) (DoSync 1 self)
  (DoAudio 8 (self ownerGain:)) (DoAudio 2 927 noun 1 0 1)
 else (DoAudio 8 0) (DoAudio 2 927 121 1 0 1))
 (++ played) (= dirty 1) (return 1))
(method (dPoll now &tmp pos nextMouth)
 (if (or (!= lane 1) (!= speaker 3) (not (proc998_2 dGen dPage)) (== (self ownerGain:) 0))
  (self cancel: 1) (return 0))
 (= pos (DoAudio 6))
 (if (or (== pos -1) (and (== dNoun 0) (>= pos dTicks)))
  ; Stock DoAudio exposes completion, not error cause. A missing atom
  ; cannot block captions; advance once and never retry a segment.
  (if (not (self dNext:))
   (if pendingLaugh (= laughDue now) (= laughReady 1)))
  (return lane))
 (= nextMouth mouth)
 (while (and (!= syncTime -1) (<= syncTime pos))
  (= nextMouth syncCue) (DoSync 1 self))
 (if (!= nextMouth mouth) (= mouth nextMouth) (= dirty 1)) (return lane))








)
(instance presentationAudio of PresentationAudio)
