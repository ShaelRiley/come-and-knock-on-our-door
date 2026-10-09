;;; Sierra Script 1.0 - (do not remove this comment)
; New transition-ready arrangement transport; source/emitted-only candidate.
(script# 966)
(use "module981")
(public cue120ReadyTransport 0 cue120Verify 1 cue120Validate 2)
(local
 [currentGains 8] = [ 0 0 0 0 0 0 0 0 ]
 [targetGains 8] = [ 0 0 0 0 0 0 0 0 ]
 [historyTableA 57] = [ 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ]
 [historyTableB 57] = [ 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ]
 [midiChannels 8] = [ 0 1 2 3 4 5 6 9 ]
 [mainStateGains 8] = [ 92 90 59 94 92 81 79 82 ]
 [reducedStateGains 8] = [ 83 70 0 60 62 37 0 49 ]
 [midiPrograms 8] = [ 33 0 48 71 73 27 11 0 ]
 [midiPans 8] = [ 64 49 75 55 75 82 40 64 ]
 [initialExpression 8] = [ 127 127 127 100 100 127 127 127 ]
 [loopExpression 8] = [ 127 127 127 100 96 127 127 127 ]
 [expressionEvents 36] = [ 12 4 90 44 4 96 76 4 103 108 4 100 141 4 98 269 4 110 398 4 105 526 4 100 655 4 96 783 4 90 880 4 94 963 4 96 ]
 [keyWindows 285] = [ 18 28 36 0 4 46 46 54 16 2 56 68 76 24 1 82 100 108 28 2 110 110 118 36 2 130 132 140 44 1 146 152 159 48 2 162 164 172 56 2 184 184 191 64 1 194 194 202 68 4 210 216 223 84 2 226 228 236 92 2 240 240 247 100 2 258 260 268 108 1 276 280 288 112 2 290 294 301 120 2 304 304 311 128 2 314 326 333 136 1 340 344 352 140 2 356 368 375 148 2 388 390 398 156 2 404 406 414 164 2 420 440 448 172 1 452 454 461 176 1 468 472 480 180 2 484 486 493 188 2 496 496 504 196 2 516 518 526 204 1 532 544 551 208 4 560 560 568 224 2 570 582 590 232 1 596 602 609 236 2 612 624 632 244 2 644 648 655 252 1 662 666 673 256 2 676 690 697 264 2 708 712 719 272 1 726 730 738 276 2 740 754 761 284 2 774 776 783 292 1 790 794 801 296 4 810 818 825 312 2 836 840 848 320 0 854 858 866 320 1 870 870 877 324 3 882 888 896 336 2 902 902 909 344 4 918 920 928 360 2 930 954 962 368 1 966 966 973 372 4 982 1010 1018 388 2 1020 1034 1041 396 1 1046 1058 1065 400 4 1068 1074 1082 416 1 1084 1098 1105 420 0 1110 1140 1147 420 1 1150 1162 1169 424 0 ]
 [heldNotes 424] = [ 0 41 46 54 1 57 38 36 1 60 38 36 4 69 62 125 0 41 46 54 4 69 62 125 4 69 62 125 0 48 43 118 4 69 62 125 0 48 43 118 4 69 62 125 4 72 59 140 0 40 46 182 4 71 61 159 0 40 46 182 4 71 61 172 4 71 61 191 0 45 42 204 1 60 34 202 1 55 34 202 4 72 61 223 0 52 43 247 4 72 61 223 0 52 43 247 4 72 61 236 0 52 43 247 4 72 61 255 4 72 61 268 0 38 36 311 4 77 68 288 0 38 36 311 4 76 65 301 0 38 36 311 4 72 65 352 4 72 65 352 0 45 33 375 4 72 65 352 0 45 33 375 4 74 65 384 0 43 42 414 4 76 65 415 0 43 42 414 4 76 65 415 4 74 63 448 4 72 63 461 0 50 33 504 4 72 63 480 0 50 33 504 4 74 63 493 0 50 33 504 4 74 63 512 4 74 63 526 0 36 46 568 1 59 38 551 1 64 38 551 4 76 64 558 0 36 46 568 4 76 61 590 4 76 61 590 0 43 43 632 4 72 61 609 0 43 43 632 4 72 61 640 4 74 61 673 0 40 46 697 4 74 61 673 0 40 46 697 4 76 59 706 4 76 59 738 0 47 43 761 4 76 59 738 0 47 43 761 4 71 59 769 4 74 59 801 0 45 46 825 1 60 38 808 1 67 38 808 4 74 59 801 0 45 46 825 4 72 58 834 0 52 43 866 0 44 42 896 1 60 34 877 1 66 34 877 0 44 42 896 4 75 58 898 0 43 42 928 1 58 34 909 1 65 34 909 4 74 58 962 0 43 42 928 4 74 58 962 4 74 58 962 0 36 42 975 1 64 34 973 1 58 34 973 4 76 57 1065 0 43 43 1018 4 76 57 1065 4 76 57 1065 0 41 42 1082 1 57 34 1065 1 64 34 1065 4 76 57 1065 0 41 42 1082 0 48 38 1147 ]
 [stateGains 16] = [ 92 90 59 94 92 81 79 82 83 70 0 60 62 37 0 49 ]
 [cue120Buffer 64]
)
(procedure (cue120Verify &tmp index slot word digit value i)
(for ((= i 0)) (< i 64) ((++ i)) (= [cue120Buffer i] 0))
(for ((= index 0)) (< index 57) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 0 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [historyTableA index] value) (return 0)))
(for ((= index 0)) (< index 57) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 3 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [historyTableB index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 6 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiChannels index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 7 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [mainStateGains index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 8 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [reducedStateGains index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 9 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiPrograms index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 10 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiPans index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 11 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [initialExpression index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 12 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [loopExpression index] value) (return 0)))
(for ((= index 0)) (< index 36) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 13 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [expressionEvents index] value) (return 0)))
(for ((= index 0)) (< index 285) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 15 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [keyWindows index] value) (return 0)))
(for ((= index 0)) (< index 424) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 30 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [heldNotes index] value) (return 0)))
(for ((= index 0)) (< index 16) ((++ index))
(if (== (mod index 20) 0) (GetFarText 276 (+ 52 (/ index 20)) @cue120Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue120Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue120Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [stateGains index] value) (return 0)))
(return 1))
(procedure (cue120Validate sound &tmp i value wanted)
(if (not (cue120Verify)) (return 0))
(if (or (not (IsObject sound)) (!= (sound number?) 120)) (return 0))
(if (or (!= (cue120ReadyTransport musicBed?) sound) (!= (cue120ReadyTransport ownedBed?) sound)) (return 0))
(= wanted (cue120ReadyTransport nextRequestedState?))
(if (or (< wanted 0) (> wanted 1)) (return 0))
(= value (cue120ReadyTransport wholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue120ReadyTransport desiredWholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue120ReadyTransport savedWholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue120ReadyTransport transportMode?))
(if (or (< value 0) (> value 9)) (return 0))
(= value (cue120ReadyTransport resumeMode?))
(if (or (< value 0) (> value 9)) (return 0))
(= value (cue120ReadyTransport settledState?))
(if (or (< value -1) (> value 1)) (return 0))
(= value (cue120ReadyTransport musicPosition?))
(if (or (< value 0) (> value 1168)) (return 0))
(= value (cue120ReadyTransport pausedPosition?))
(if (or (< value 0) (> value 1168)) (return 0))
(= value (cue120ReadyTransport previousPosition?))
(if (or (< value -1) (> value 1168)) (return 0))
(= value (cue120ReadyTransport recoveryLastPosition?))
(if (or (< value -1) (> value 1168)) (return 0))
(= value (cue120ReadyTransport rejoinWindow?))
(if (or (< value -1) (> value 56)) (return 0))
(= value (cue120ReadyTransport historyWindow?))
(if (or (< value -1) (> value 56)) (return 0))
(= value (cue120ReadyTransport lastBatchKeys?))
(if (or (< value 0) (> value 32)) (return 0))
(= value (cue120ReadyTransport recoverySamples?))
(if (or (< value 0) (> value 32767)) (return 0))
(= value (cue120ReadyTransport recoveryReason?))
(if (or (< value 0) (> value 10)) (return 0))
(= value (cue120ReadyTransport historyRoute?))
(if (or (< value 0) (> value 10)) (return 0))
(= value (cue120ReadyTransport requestRevision?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue120ReadyTransport saveRevision?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue120ReadyTransport previousGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue120ReadyTransport loopEpoch?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue120ReadyTransport rejoinEpoch?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue120ReadyTransport lifecycleGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue120ReadyTransport recoveryGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue120ReadyTransport gainRefreshes?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue120ReadyTransport historyEpisodes?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue120ReadyTransport rejoinAttempts?))
(if (or (< value 0) (> value 32)) (return 0))
(= value (cue120ReadyTransport musicRunning?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue120ReadyTransport musicPaused?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue120ReadyTransport ownedPauseHeld?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue120ReadyTransport pausePhaseKnown?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue120ReadyTransport pausedCheckpoint?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue120ReadyTransport recoveryPhaseKnown?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue120ReadyTransport musicMuted?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue120ReadyTransport loopHasWrapped?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue120ReadyTransport saveGuard?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue120ReadyTransport remapGuard?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue120ReadyTransport remapDrain?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue120ReadyTransport positionUncertain?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue120ReadyTransport recoveryWrapped?))
(if (or (< value 0) (> value 1)) (return 0))
(if (or (!= (cue120ReadyTransport musicMuted?) (if (cue120ReadyTransport musicMuted?) 1 else 0)) (< (cue120ReadyTransport transportMode?) 1)) (return 0))
(if (and (cue120ReadyTransport recoveryBed?) (!= (cue120ReadyTransport recoveryBed?) sound)) (return 0))
(if (!= (cue120ReadyTransport musicRunning?) 1) (return 0))
(if (and (cue120ReadyTransport pausedCheckpoint?) (not (cue120ReadyTransport saveGuard?))) (return 0))
(if (and (cue120ReadyTransport saveGuard?) (not (cue120ReadyTransport ownedPauseHeld?))) (return 0))
(for ((= i 0)) (< i 8) ((++ i))
(if (or (< [currentGains i] 0) (> [currentGains i] 127)) (return 0))
(if (!= [targetGains i] [stateGains (+ (* wanted 8) i)]) (return 0)))
(return 1))
(instance cue120ReadyTransport of MusicTransport
    (properties
        musicBed 0
        ownedBed 0
        musicRunning 0
        musicPaused 0
        ownedPauseHeld 0
        pausePhaseKnown 0
        pausedPosition 0
        pauseAcquires 0
        pauseReleases 0
        pausedCheckpoint 0
        checkpointRestores 0
        recoveryPhaseKnown 0
        nextRequestedState 0
        settledState 0
        requestRevision 0
        transportMode 0
        musicMuted 0
        wholeGain 0
        desiredWholeGain 100
        musicPosition 0
        previousPosition -1
        previousReadTick 0
        previousReadBin 0
        previousReadDate 0
        previousGeneration 0
        loopEpoch 0
        loopHasWrapped 0
        lastPollTick 0
        lastRampTick 0
        saveGuard 0
        remapGuard 0
        remapDrain 0
        remapStart 0
        lastProgressTick 0
        positionUncertain 0
        resumeMode 0
        savedWholeGain 0
        saveRevision 0
        rejoinAttempts 0
        rejoinStart 0
        retryAt 0
        rejoinWindow -1
        rejoinEpoch 0
        rejoinSuccesses 0
        rejoinExpired 0
        rejoinFailures 0
        lastBatchKeys 0
        initialOpens 0
        lastCue 0
        loopObservations 0
        controllerRestores 0
        gainRefreshes 0
        lifecycleGeneration 0
        recoveryGeneration 0
        recoveryBed 0
        recoverySamples 0
        recoveryLastPosition -1
        recoveryLastTick 0
        recoveryStart 0
        recoveryWrapped 0
        recoveryReason 0
        historyRoute 0
        historyWindow -1
        historySuccesses 0
        historyFailures 0
        historyEpisodes 0
        lastWallBin 0
        lastWallDate 0
        observedWallBin 0
        observedWallDate 0
    )
    ; Original method offset 0x0158; 68 instructions
    (method (acquirePause)
        (asm
            pToa ownedPauseHeld
            bt label_0161
            pToa musicRunning
            not
            bnt label_0164
            label_0161: ldi 0
            ret
            label_0164: pushi 687 ; selector/constant holdSilent
            push0
            self 4
            pTos musicBed
            pToa ownedBed
            ne?
            bt label_017a
            push1
            pTos ownedBed
            callk IsObject, 2
            not
            bnt label_0182
            label_017a: pushi 679 ; selector/constant failHistory
            push1
            push1
            self 6
            ret
            label_0182: pToa positionUncertain
            not
            bnt label_018d
            pushi 428 ; selector/constant readPosition
            push0
            self 4
            label_018d: pushi 3 ; selector/constant type
            pushi 10 ; selector/constant advance
            pTos ownedBed
            push1
            callk DoSound, 6
            ldi 1
            aTop ownedPauseHeld
            ipToa pauseAcquires
            pToa positionUncertain
            not
            bnt label_01aa
            pushi 428 ; selector/constant readPosition
            push0
            self 4
            jmp label_01b7
            label_01aa: pushi 718 ; selector/constant rawPosition
            push0
            self 4
            not
            bnt label_01b7
            ldi 1
            aTop positionUncertain
            label_01b7: pToa positionUncertain
            not
            aTop pausePhaseKnown
            pToa musicPosition
            aTop pausedPosition
            pTos lifecycleGeneration
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop lifecycleGeneration
            ldi 9
            aTop transportMode
            ldi 1
            ret
        )
    )
    ; Original method offset 0x01d3; 30 instructions
    (method (releasePause)
        (asm
            pToa ownedPauseHeld
            not
            bt label_01dd
            pToa musicRunning
            not
            bnt label_01e0
            label_01dd: ldi 0
            ret
            label_01e0: pushi 687 ; selector/constant holdSilent
            push0
            self 4
            pushi 3 ; selector/constant type
            pushi 10 ; selector/constant advance
            pTos ownedBed
            push0
            callk DoSound, 6
            ldi 0
            aTop ownedPauseHeld
            ipToa pauseReleases
            pTos lifecycleGeneration
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop lifecycleGeneration
            pushi 680 ; selector/constant finishPauseResume
            push0
            self 4
            ret
        )
    )
    ; Original method offset 0x0209; 87 instructions
    (method (finishPauseResume)
        (asm
            link 2
            push0
            callk GetTime, 0
            sat 0
            pushi 719 ; selector/constant readCivil
            push0
            self 4
            pushi 672 ; selector/constant anchorClock
            push1
            lst 0
            self 6
            ldi -1
            aTop previousPosition
            lat 0
            aTop lastProgressTick
            lat 0
            aTop lastRampTick
            pushi 718 ; selector/constant rawPosition
            push0
            self 4
            not
            bnt label_023f
            pushi 679 ; selector/constant failHistory
            push1
            pushi 3 ; selector/constant type
            self 6
            ldi 0
            ret
            label_023f: pTos musicPosition
            pToa pausedPosition
            lt?
            bnt label_0257
            pushi 1169
            pToa pausedPosition
            sub
            push
            pTos musicPosition
            ldi 12
            sub
            add
            sat 1
            jmp label_025e
            label_0257: pTos musicPosition
            pToa pausedPosition
            sub
            sat 1
            label_025e: lst 1
            ldi 4
            ugt?
            bt label_0273
            pTos musicPosition
            pToa pausedPosition
            lt?
            bnt label_0277
            pTos musicPosition
            ldi 12
            lt?
            bnt label_0277
            label_0273: ldi 0
            aTop pausePhaseKnown
            label_0277: pToa pausePhaseKnown
            bnt label_02a2
            pTos musicPosition
            pToa pausedPosition
            lt?
            bnt label_0294
            ldi 1
            aTop loopHasWrapped
            pTos loopEpoch
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop loopEpoch
            ipToa loopObservations
            label_0294: ldi 0
            aTop positionUncertain
            pushi 673 ; selector/constant anchorPosition
            push1
            lst 0
            self 6
            jmp label_02a6
            label_02a2: ldi 1
            aTop positionUncertain
            label_02a6: ldi 1
            ret
        )
    )
    ; Original method offset 0x02a9; 41 instructions
    (method (setPaused paused)
        (asm
            lap 1
            bnt label_02b1
            ldi 1
            jmp label_02b3
            label_02b1: ldi 0
            label_02b3: sap 1
            lsp 1
            pToa musicPaused
            eq?
            bnt label_02bf
            ldi 1
            ret
            label_02bf: lap 1
            aTop musicPaused
            pToa musicRunning
            not
            bt label_02cc
            pToa saveGuard
            bnt label_02cf
            label_02cc: ldi 1
            ret
            label_02cf: pToa musicPaused
            bnt label_02db
            pushi 669 ; selector/constant acquirePause
            push0
            self 4
            jmp label_02f3
            label_02db: pushi 731 ; selector/constant releasePause
            push0
            self 4
            pToa positionUncertain
            bnt label_02ed
            pushi 675 ; selector/constant beginHistory
            push0
            self 4
            jmp label_02f3
            label_02ed: pushi 398 ; selector/constant beginRejoin
            push0
            self 4
            label_02f3: ldi 1
            ret
        )
    )
    ; Original method offset 0x02f6; 16 instructions
    (method (setWholeTarget gain)
        (asm
            lsp 1
            ldi 0
            lt?
            bnt label_0301
            ldi 0
            sap 1
            label_0301: lsp 1
            ldi 100
            gt?
            bnt label_030c
            ldi 100
            sap 1
            label_030c: lap 1
            aTop desiredWholeGain
            pToa desiredWholeGain
            ret
        )
    )
    ; Original method offset 0x0313; 36 instructions
    (method (readCivil)
        (asm
            link 1
            push1
            push2
            callk GetTime, 2
            sat 0
            push1
            pushi 3 ; selector/constant type
            callk GetTime, 2
            aTop observedWallDate
            lst 0
            ldi 11
            shr
            push
            ldi 31
            and
            push
            ldi 1800
            mul
            push
            lst 0
            ldi 5
            shr
            push
            ldi 63
            and
            push
            ldi 30
            mul
            push
            lst 0
            ldi 31
            and
            add
            add
            aTop observedWallBin
            ret
        )
    )
    ; Original method offset 0x034d; 112 instructions
    (method (nextCivilDate packedDate)
        (asm
            link 5
            lsp 1
            ldi 9
            shr
            push
            ldi 127
            and
            sat 0
            lsp 1
            ldi 5
            shr
            push
            ldi 15
            and
            sat 1
            lsp 1
            ldi 31
            and
            sat 2
            ldi 31
            sat 3
            lst 0
            ldi 1980
            add
            sat 4
            lst 1
            ldi 4
            eq?
            bt label_0394
            lst 1
            ldi 6
            eq?
            bt label_0394
            lst 1
            ldi 9
            eq?
            bt label_0394
            lst 1
            ldi 11
            eq?
            bnt label_0398
            label_0394: ldi 30
            sat 3
            label_0398: lst 1
            ldi 2
            eq?
            bnt label_03c9
            ldi 28
            sat 3
            lst 4
            ldi 4
            mod
            push
            ldi 0
            eq?
            bnt label_03c9
            lst 4
            ldi 100
            mod
            push
            ldi 0
            ne?
            bt label_03c5
            lst 4
            ldi 400
            mod
            push
            ldi 0
            eq?
            bnt label_03c9
            label_03c5: ldi 29
            sat 3
            label_03c9: lst 2
            lat 3
            lt?
            bnt label_03d6
            lsp 1
            ldi 1
            add
            ret
            label_03d6: lst 1
            ldi 12
            lt?
            bnt label_03f3
            lst 0
            ldi 512
            mul
            push
            lst 1
            ldi 1
            add
            push
            ldi 32
            mul
            push
            ldi 1
            add
            add
            ret
            label_03f3: lst 0
            ldi 1
            add
            push
            ldi 127
            and
            push
            ldi 512
            mul
            push
            ldi 33
            add
            ret
        )
    )
    ; Original method offset 0x0406; 37 instructions
    (method (civilDelta previousBin previousDate)
        (asm
            link 1
            pTos observedWallDate
            lap 2
            eq?
            bnt label_0425
            pTos observedWallBin
            lap 1
            ult?
            bnt label_041b
            ldi -1
            ret
            label_041b: pTos observedWallBin
            lap 1
            sub
            sat 0
            jmp label_044a
            label_0425: pTos observedWallDate
            pushi 703 ; selector/constant nextCivilDate
            push1
            lsp 2
            self 6
            ne?
            bt label_043b
            pTos observedWallBin
            lap 1
            uge?
            bnt label_043e
            label_043b: ldi -1
            ret
            label_043e: pTos observedWallBin
            pushi -22336
            lap 1
            sub
            add
            sat 0
            label_044a: lat 0
            ret
        )
    )
    ; Original method offset 0x044d; 25 instructions
    (method (clockFresh now)
        (asm
            link 1
            pushi 719 ; selector/constant readCivil
            push0
            self 4
            pushi 677 ; selector/constant civilDelta
            push2
            pTos lastWallBin
            pTos lastWallDate
            self 8
            sat 0
            lsp 1
            pToa lastPollTick
            sub
            push
            ldi 120
            ule?
            bnt label_047a
            lst 0
            ldi 0
            ge?
            bnt label_047a
            lst 0
            ldi 2
            ule?
            label_047a: ret
        )
    )
    ; Original method offset 0x047b; 11 instructions
    (method (anchorPosition now)
        (asm
            pToa musicPosition
            aTop previousPosition
            lap 1
            aTop previousReadTick
            pToa observedWallBin
            aTop previousReadBin
            pToa observedWallDate
            aTop previousReadDate
            pToa lifecycleGeneration
            aTop previousGeneration
            ret
        )
    )
    ; Original method offset 0x0492; 67 instructions
    (method (rawPosition)
        (asm
            pTos musicBed
            pToa ownedBed
            ne?
            bt label_04a2
            push1
            pTos musicBed
            callk IsObject, 2
            not
            bnt label_04a5
            label_04a2: ldi 0
            ret
            label_04a5: pushi 156 ; selector/constant number
            push0
            pToa musicBed
            send 4
            push
            ldi 120
            ne?
            bnt label_04b6
            ldi 0
            ret
            label_04b6: push2
            pushi 17 ; selector/constant audioApplied
            pTos musicBed
            callk DoSound, 4
            pushi 129 ; selector/constant min
            push0
            pToa musicBed
            send 4
            push
            ldi 3600
            mul
            push
            pushi 254 ; selector/constant sec
            push0
            pToa musicBed
            send 4
            push
            ldi 60
            mul
            push
            pushi 104 ; selector/constant frame
            push0
            pToa musicBed
            send 4
            push
            ldi 2
            mul
            add
            add
            aTop musicPosition
            pTos musicPosition
            ldi 0
            ge?
            bnt label_0503
            pTos musicPosition
            ldi 1169
            lt?
            bnt label_0503
            pushi 256 ; selector/constant signal
            push0
            pToa musicBed
            send 4
            push
            ldi -1
            ne?
            label_0503: ret
        )
    )
    ; Original method offset 0x0504; 133 instructions
    (method (recoverGap now)
        (asm
            link 3
            pToa positionUncertain
            bt label_0528
            pToa saveGuard
            bt label_0528
            pToa remapGuard
            bt label_0528
            pToa musicPaused
            bt label_0528
            pToa ownedPauseHeld
            bt label_0528
            pTos previousPosition
            ldi 0
            lt?
            bt label_0528
            pTos previousGeneration
            pToa lifecycleGeneration
            ne?
            bnt label_052b
            label_0528: ldi 0
            ret
            label_052b: lsp 1
            pToa previousReadTick
            sub
            sat 0
            pushi 677 ; selector/constant civilDelta
            push2
            pTos previousReadBin
            pTos previousReadDate
            self 8
            sat 1
            lst 0
            ldi 600
            ugt?
            bt label_0555
            lst 1
            ldi 0
            lt?
            bt label_0555
            lst 1
            ldi 240
            ugt?
            bnt label_0558
            label_0555: ldi 0
            ret
            label_0558: pushi 687 ; selector/constant holdSilent
            push0
            self 4
            pushi 718 ; selector/constant rawPosition
            push0
            self 4
            not
            bnt label_056a
            ldi 0
            ret
            label_056a: pTos musicPosition
            pToa previousPosition
            lt?
            bnt label_058c
            pTos musicPosition
            ldi 12
            lt?
            bnt label_057b
            ldi 0
            ret
            label_057b: pushi 1169
            pToa previousPosition
            sub
            push
            pTos musicPosition
            ldi 12
            sub
            add
            sat 2
            jmp label_0593
            label_058c: pTos musicPosition
            pToa previousPosition
            sub
            sat 2
            label_0593: lst 2
            lst 0
            ldi 4
            add
            ugt?
            bnt label_05a0
            ldi 0
            ret
            label_05a0: pTos musicPosition
            pToa previousPosition
            lt?
            bnt label_05b9
            ldi 1
            aTop loopHasWrapped
            pTos loopEpoch
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop loopEpoch
            ipToa loopObservations
            label_05b9: lap 1
            aTop lastProgressTick
            pushi 673 ; selector/constant anchorPosition
            push1
            lsp 1
            self 6
            pushi 672 ; selector/constant anchorClock
            push1
            lsp 1
            self 6
            ldi 0
            aTop recoveryReason
            ldi 4
            aTop historyRoute
            ldi -1
            aTop historyWindow
            lst 2
            ldi 0
            eq?
            bnt label_05ef
            pushi 675 ; selector/constant beginHistory
            push0
            self 4
            ldi 1
            aTop recoveryPhaseKnown
            jmp label_05f8
            label_05ef: ipToa historySuccesses
            pushi 398 ; selector/constant beginRejoin
            push0
            self 4
            label_05f8: ldi 1
            ret
        )
    )
    ; Original method offset 0x05fb; 7 instructions
    (method (anchorClock now)
        (asm
            lap 1
            aTop lastPollTick
            pToa observedWallBin
            aTop lastWallBin
            pToa observedWallDate
            aTop lastWallDate
            ret
        )
    )
    ; Original method offset 0x060c; 12 instructions
    (method (holdSilent)
        (asm
            ldi 0
            aTop wholeGain
            push1
            pTos ownedBed
            callk IsObject, 2
            bnt label_0622
            pushi 3 ; selector/constant type
            pushi 14 ; selector/constant apronSeen
            pTos ownedBed
            push0
            callk DoSound, 6
            label_0622: ret
        )
    )
    ; Original method offset 0x0623; 59 instructions
    (method (beginHistory)
        (asm
            pToa musicRunning
            not
            bnt label_062b
            ldi 0
            ret
            label_062b: pushi 687 ; selector/constant holdSilent
            push0
            self 4
            ldi 1
            aTop positionUncertain
            ldi 8
            aTop transportMode
            pToa ownedPauseHeld
            bnt label_0641
            ldi 0
            aTop pausePhaseKnown
            label_0641: ldi 0
            aTop recoverySamples
            ldi -1
            aTop recoveryLastPosition
            ldi 0
            aTop recoveryWrapped
            pToa lifecycleGeneration
            aTop recoveryGeneration
            pToa ownedBed
            aTop recoveryBed
            push0
            callk GetTime, 0
            aTop recoveryStart
            pToa recoveryStart
            aTop recoveryLastTick
            pToa recoveryStart
            aTop lastProgressTick
            ldi 0
            aTop recoveryReason
            ldi 0
            aTop historyRoute
            ldi -1
            aTop historyWindow
            ldi 0
            aTop recoveryPhaseKnown
            pTos historyEpisodes
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop historyEpisodes
            ldi -1
            aTop previousPosition
            pushi 719 ; selector/constant readCivil
            push0
            self 4
            pushi 672 ; selector/constant anchorClock
            push1
            pTos recoveryStart
            self 6
            ldi 1
            ret
        )
    )
    ; Original method offset 0x06a1; 12 instructions
    (method (failHistory reason)
        (asm
            pushi 687 ; selector/constant holdSilent
            push0
            self 4
            ldi 1
            aTop positionUncertain
            ldi 6
            aTop transportMode
            lap 1
            aTop recoveryReason
            ipToa historyFailures
            ldi 0
            ret
        )
    )
    ; Original method offset 0x06ba; 29 instructions
    (method (windowAt position)
        (asm
            link 2
            ldi 0
            sat 0
            label_06c0: lst 0
            ldi 57
            lt?
            bnt label_06ed
            lst 0
            ldi 5
            mul
            sat 1
            lsp 1
            lat 1
            lali keyWindows
            ge?
            bnt label_06e9
            lsp 1
            lst 1
            ldi 1
            add
            lali keyWindows
            le?
            bnt label_06e9
            lat 0
            ret
            label_06e9: +at 0
            jmp label_06c0
            label_06ed: ldi -1
            ret
        )
    )
    ; Original method offset 0x06f0; 253 instructions
    (method (observeHistory now)
        (asm
            link 3
            pToa saveGuard
            bt label_0709
            pToa remapGuard
            bt label_0709
            pToa musicPaused
            bt label_0709
            pToa ownedPauseHeld
            bt label_0709
            pTos transportMode
            ldi 8
            ne?
            bnt label_070c
            label_0709: ldi 0
            ret
            label_070c: pTos lifecycleGeneration
            pToa recoveryGeneration
            ne?
            bt label_072a
            pTos musicBed
            pToa recoveryBed
            ne?
            bt label_072a
            pTos ownedBed
            pToa recoveryBed
            ne?
            bt label_072a
            push1
            pTos musicBed
            callk IsObject, 2
            not
            bnt label_0732
            label_072a: pushi 679 ; selector/constant failHistory
            push1
            push1
            self 6
            ret
            label_0732: pushi 156 ; selector/constant number
            push0
            pToa musicBed
            send 4
            push
            ldi 120
            ne?
            bnt label_0748
            pushi 679 ; selector/constant failHistory
            push1
            push1
            self 6
            ret
            label_0748: lsp 1
            pToa recoveryStart
            sub
            push
            ldi 1800
            uge?
            bnt label_075d
            pushi 679 ; selector/constant failHistory
            push1
            push2
            self 6
            ret
            label_075d: pushi 718 ; selector/constant rawPosition
            push0
            self 4
            not
            bt label_0772
            pToa recoveryPhaseKnown
            not
            bnt label_077b
            pTos musicPosition
            ldi 12
            lt?
            bnt label_077b
            label_0772: pushi 679 ; selector/constant failHistory
            push1
            pushi 3 ; selector/constant type
            self 6
            ret
            label_077b: pTos recoveryLastPosition
            ldi -1
            eq?
            bnt label_078b
            ldi 1
            aTop recoverySamples
            jmp label_0821
            label_078b: lsp 1
            pToa recoveryLastTick
            sub
            sat 0
            lst 0
            ldi 120
            ugt?
            bnt label_07a3
            pushi 679 ; selector/constant failHistory
            push1
            pushi 4 ; selector/constant message
            self 6
            ret
            label_07a3: pTos musicPosition
            pToa recoveryLastPosition
            lt?
            bnt label_07d7
            pTos recoveryLastPosition
            ldi 1045
            lt?
            bt label_07bc
            pTos musicPosition
            ldi 136
            gt?
            bnt label_07c5
            label_07bc: pushi 679 ; selector/constant failHistory
            push1
            pushi 3 ; selector/constant type
            self 6
            ret
            label_07c5: pushi 1169
            pToa recoveryLastPosition
            sub
            push
            pTos musicPosition
            ldi 12
            sub
            add
            sat 1
            jmp label_07df
            label_07d7: pTos musicPosition
            pToa recoveryLastPosition
            sub
            sat 1
            label_07df: lst 1
            lst 0
            ldi 4
            add
            ugt?
            bnt label_07f2
            pushi 679 ; selector/constant failHistory
            push1
            pushi 3 ; selector/constant type
            self 6
            ret
            label_07f2: lst 1
            ldi 0
            gt?
            bnt label_0821
            lap 1
            aTop lastProgressTick
            pTos musicPosition
            pToa recoveryLastPosition
            lt?
            bnt label_081c
            ldi 1
            aTop recoveryWrapped
            ldi 1
            aTop loopHasWrapped
            pTos loopEpoch
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop loopEpoch
            ipToa loopObservations
            label_081c: ldi 2
            aTop recoverySamples
            label_0821: pToa musicPosition
            aTop recoveryLastPosition
            lap 1
            aTop recoveryLastTick
            lsp 1
            pToa lastProgressTick
            sub
            push
            ldi 120
            ugt?
            bnt label_083f
            pushi 679 ; selector/constant failHistory
            push1
            pushi 5 ; selector/constant modifiers
            self 6
            ret
            label_083f: pToa remapDrain
            bnt label_0855
            lsp 1
            pToa remapStart
            sub
            push
            ldi 4
            ult?
            bnt label_0851
            ldi 0
            ret
            label_0851: ldi 0
            aTop remapDrain
            label_0855: pTos recoverySamples
            ldi 2
            lt?
            bnt label_0860
            ldi 0
            ret
            label_0860: pushi 736 ; selector/constant windowAt
            push1
            pTos musicPosition
            self 6
            sat 2
            lst 2
            ldi -1
            eq?
            bnt label_0874
            ldi 0
            ret
            label_0874: pToa recoveryPhaseKnown
            bnt label_087f
            ldi 5
            aTop historyRoute
            jmp label_08b0
            label_087f: pToa loopHasWrapped
            bnt label_0893
            pToa recoveryWrapped
            bnt label_088c
            ldi 2
            jmp label_088e
            label_088c: ldi 1
            label_088e: aTop historyRoute
            jmp label_08b0
            label_0893: lat 2
            lali historyTableB
            bnt label_08a1
            ldi 3
            aTop historyRoute
            jmp label_08b0
            label_08a1: lat 2
            lali historyTableA
            not
            bnt label_08ab
            ldi 0
            ret
            label_08ab: ldi 6
            aTop historyRoute
            label_08b0: lat 2
            aTop historyWindow
            ipToa historySuccesses
            ldi 0
            aTop positionUncertain
            pushi 673 ; selector/constant anchorPosition
            push1
            lsp 1
            self 6
            pushi 398 ; selector/constant beginRejoin
            push0
            self 4
            ldi 1
            ret
        )
    )
    ; Original method offset 0x08cd; 147 instructions
    (method (readPosition)
        (asm
            link 4
            push0
            callk GetTime, 0
            sat 0
            pushi 719 ; selector/constant readCivil
            push0
            self 4
            pushi 718 ; selector/constant rawPosition
            push0
            self 4
            not
            bnt label_08ef
            pushi 679 ; selector/constant failHistory
            push1
            pushi 3 ; selector/constant type
            self 6
            ldi -1
            ret
            label_08ef: pTos previousPosition
            ldi 0
            ge?
            bnt label_09c3
            lst 0
            pToa previousReadTick
            sub
            sat 1
            pushi 677 ; selector/constant civilDelta
            push2
            pTos previousReadBin
            pTos previousReadDate
            self 8
            sat 2
            lst 1
            ldi 120
            ugt?
            bt label_091f
            lst 2
            ldi 0
            lt?
            bt label_091f
            lst 2
            ldi 2
            ugt?
            bnt label_0928
            label_091f: pushi 675 ; selector/constant beginHistory
            push0
            self 4
            ldi -1
            ret
            label_0928: pTos musicPosition
            pToa previousPosition
            lt?
            bnt label_0962
            pTos previousPosition
            ldi 1045
            lt?
            bt label_0946
            pTos musicPosition
            ldi 136
            gt?
            bt label_0946
            pTos musicPosition
            ldi 12
            lt?
            bnt label_0951
            label_0946: pushi 679 ; selector/constant failHistory
            push1
            pushi 3 ; selector/constant type
            self 6
            ldi -1
            ret
            label_0951: pushi 1169
            pToa previousPosition
            sub
            push
            pTos musicPosition
            ldi 12
            sub
            add
            sat 3
            jmp label_0969
            label_0962: pTos musicPosition
            pToa previousPosition
            sub
            sat 3
            label_0969: lst 3
            lst 1
            ldi 4
            add
            ugt?
            bnt label_097e
            pushi 679 ; selector/constant failHistory
            push1
            pushi 3 ; selector/constant type
            self 6
            ldi -1
            ret
            label_097e: lst 3
            ldi 0
            gt?
            bnt label_0989
            lat 0
            aTop lastProgressTick
            label_0989: lst 0
            pToa lastProgressTick
            sub
            push
            ldi 120
            ugt?
            bnt label_099f
            pushi 679 ; selector/constant failHistory
            push1
            pushi 5 ; selector/constant modifiers
            self 6
            ldi -1
            ret
            label_099f: pTos musicPosition
            pToa previousPosition
            lt?
            bnt label_09c3
            pTos loopEpoch
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop loopEpoch
            ldi 1
            aTop loopHasWrapped
            ipToa loopObservations
            pushi 3 ; selector/constant type
            pushi 16 ; selector/constant audienceVolume
            pTos musicBed
            pushi -1
            callk DoSound, 6
            label_09c3: pTos previousPosition
            ldi 0
            lt?
            bnt label_09ce
            lat 0
            aTop lastProgressTick
            label_09ce: pushi 673 ; selector/constant anchorPosition
            push1
            lst 0
            self 6
            pToa musicPosition
            ret
        )
    )
    ; Original method offset 0x09d9; 13 instructions
    (method (gainAt part)
        (asm
            lsp 1
            ldi 0
            lt?
            bt label_09e7
            lsp 1
            ldi 7
            gt?
            bnt label_09ea
            label_09e7: ldi -1
            ret
            label_09ea: lap 1
            lali currentGains
            ret
        )
    )
    ; Original method offset 0x09ef; 13 instructions
    (method (targetAt part)
        (asm
            lsp 1
            ldi 0
            lt?
            bt label_09fd
            lsp 1
            ldi 7
            gt?
            bnt label_0a00
            label_09fd: ldi -1
            ret
            label_0a00: lap 1
            lali targetGains
            ret
        )
    )
    ; Original method offset 0x0a05; 46 instructions
    (method (requestState state &tmp part)
            (if (< state 0) (return 0))
            (if (> state 1) (return 0))
            (if (!= state nextRequestedState) (= requestRevision (mod (+ requestRevision 1) 30000)))
            (= nextRequestedState state)
            (for ((= part 0)) (< part 8) ((++ part))
                (= [targetGains part] [stateGains (+ (* state 8) part)]))
            (= settledState -1)
            (return 1)
        )
        (method (expressionAt part position)
        (asm
            link 3
            lsp 1
            ldi 0
            lt?
            bt label_0a6a
            lsp 1
            ldi 7
            gt?
            bnt label_0a6d
            label_0a6a: ldi -1
            ret
            label_0a6d: pToa loopHasWrapped
            bnt label_0a78
            lap 1
            lali loopExpression
            jmp label_0a7d
            label_0a78: lap 1
            lali initialExpression
            label_0a7d: sat 0
            ldi 0
            sat 1
            label_0a83: lst 1
            ldi 48
            lt?
            bnt label_0ab6
            lst 1
            ldi 3
            mul
            sat 2
            lst 2
            ldi 1
            add
            lsli expressionEvents
            lap 1
            eq?
            bnt label_0ab2
            lat 2
            lsli expressionEvents
            lap 2
            le?
            bnt label_0ab2
            lst 2
            ldi 2
            add
            lali expressionEvents
            sat 0
            label_0ab2: +at 1
            jmp label_0a83
            label_0ab6: lat 0
            ret
        )
    )
    ; Original method offset 0x0ab9; 28 instructions
    (method (clearMutedBed)
        (asm
            link 1
            pTos wholeGain
            ldi 0
            ne?
            bnt label_0ac5
            ldi 0
            ret
            label_0ac5: ldi 0
            sat 0
            label_0ac9: lst 0
            ldi 8
            lt?
            bnt label_0ae9
            pushi 5 ; selector/constant modifiers
            pushi 18 ; selector/constant audioApron
            pTos musicBed
            lat 0
            lsli midiChannels
            ldi 1
            add
            push
            pushi 120 ; selector/constant jackLeft
            push0
            callk DoSound, 10
            +at 0
            jmp label_0ac9
            label_0ae9: ldi 1
            ret
        )
    )
    ; Original method offset 0x0aec; 75 instructions
    (method (rebuildControllers position)
        (asm
            link 2
            ldi 0
            sat 0
            label_0af2: lst 0
            ldi 8
            lt?
            bnt label_0b84
            lat 0
            lsli midiChannels
            ldi 1
            add
            sat 1
            pushi 6 ; selector/constant x
            pushi 18 ; selector/constant audioApron
            pTos musicBed
            lst 1
            pushi 192 ; selector/constant p02GapJack
            lat 0
            lsli midiPrograms
            push0
            callk DoSound, 12
            pushi 5 ; selector/constant modifiers
            pushi 18 ; selector/constant audioApron
            pTos musicBed
            lst 1
            push1
            push0
            callk DoSound, 10
            pushi 5 ; selector/constant modifiers
            pushi 18 ; selector/constant audioApron
            pTos musicBed
            lst 1
            pushi 10 ; selector/constant advance
            lat 0
            lsli midiPans
            callk DoSound, 10
            pushi 5 ; selector/constant modifiers
            pushi 18 ; selector/constant audioApron
            pTos musicBed
            lst 1
            pushi 64 ; selector/constant bridgeExchangeDocument
            push0
            callk DoSound, 10
            pushi 6 ; selector/constant x
            pushi 18 ; selector/constant audioApron
            pTos musicBed
            lst 1
            pushi 224 ; selector/constant p02Place
            push0
            pushi 64 ; selector/constant bridgeExchangeDocument
            callk DoSound, 12
            pushi 5 ; selector/constant modifiers
            pushi 18 ; selector/constant audioApron
            pTos musicBed
            lst 1
            pushi 11 ; selector/constant applyMix
            pushi 408 ; selector/constant expressionAt
            push2
            lst 0
            lsp 1
            self 8
            push
            callk DoSound, 10
            pushi 5 ; selector/constant modifiers
            pushi 18 ; selector/constant audioApron
            pTos musicBed
            lst 1
            pushi 7 ; selector/constant y
            lat 0
            lsli currentGains
            callk DoSound, 10
            +at 0
            jmp label_0af2
            label_0b84: ipToa controllerRestores
            ret
        )
    )
    ; Original method offset 0x0b87; 43 instructions
    (method (beginRejoin)
        (asm
            pToa musicRunning
            not
            bnt label_0b8f
            ldi 0
            ret
            label_0b8f: ldi 0
            aTop wholeGain
            pushi 3 ; selector/constant type
            pushi 14 ; selector/constant apronSeen
            pTos musicBed
            push0
            callk DoSound, 6
            ldi -1
            aTop rejoinWindow
            ldi 0
            aTop rejoinAttempts
            ldi 0
            aTop lastBatchKeys
            push0
            callk GetTime, 0
            aTop rejoinStart
            pToa rejoinStart
            aTop retryAt
            pToa musicPaused
            bnt label_0bbb
            ldi 9
            jmp label_0bd5
            label_0bbb: pToa positionUncertain
            bnt label_0bc3
            ldi 6
            jmp label_0bd5
            label_0bc3: pToa remapGuard
            bnt label_0bcb
            ldi 7
            jmp label_0bd5
            label_0bcb: pToa musicMuted
            bnt label_0bd3
            ldi 4
            jmp label_0bd5
            label_0bd3: ldi 3
            label_0bd5: aTop transportMode
            ldi 1
            ret
        )
    )
    ; Original method offset 0x0bda; 134 instructions
    (method (start soundObject state)
        (if (not (cue120Verify))
                (if musicRunning (self holdSilent:))
                (= transportMode 6)
                (return 0))
            (asm
            link 1
            pToa musicRunning
            bt label_0bf7
            push1
            lsp 1
            callk IsObject, 2
            not
            bt label_0bf7
            pushi 156 ; selector/constant number
            push0
            lap 1
            send 4
            push
            ldi 120
            ne?
            bnt label_0bfa
            label_0bf7: ldi 0
            ret
            label_0bfa: lsp 2
            ldi 0
            lt?
            bt label_0c08
            lsp 2
            ldi 1
            gt?
            bnt label_0c0b
            label_0c08: ldi 0
            ret
            label_0c0b: lap 1
            aTop musicBed
            lap 1
            aTop ownedBed
            ldi 1
            aTop musicRunning
            pTos lifecycleGeneration
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop lifecycleGeneration
            ldi 0
            aTop saveGuard
            ldi 0
            aTop remapGuard
            ldi 0
            aTop positionUncertain
            ldi 0
            aTop wholeGain
            ldi 0
            aTop loopEpoch
            ldi 0
            aTop loopHasWrapped
            ldi 0
            aTop remapDrain
            ldi 0
            aTop musicPosition
            ldi -1
            aTop previousPosition
            ldi 0
            aTop initialOpens
            push0
            callk GetTime, 0
            aTop lastPollTick
            pToa lastPollTick
            aTop lastRampTick
            pushi 719 ; selector/constant readCivil
            push0
            self 4
            pushi 672 ; selector/constant anchorClock
            push1
            pTos lastPollTick
            self 6
            ldi 0
            sat 0
            label_0c67: lst 0
            ldi 8
            lt?
            bnt label_0c7b
            lsp 2
            ldi 8
            mul
            push
            lat 0
            add
            lsli stateGains
            lat 0
            sali currentGains
            +at 0
            jmp label_0c67
            label_0c7b: pushi 439 ; selector/constant requestState
            push1
            lsp 2
            self 6
            pushi 339 ; selector/constant vol
            push1
            push0
            pushi 125 ; selector/constant loop
            push1
            pushi -1
            pushi 256 ; selector/constant signal
            push1
            push0
            pToa musicBed
            send 18
            push2
            pushi 6 ; selector/constant x
            pTos musicBed
            callk DoSound, 4
            pushi 3 ; selector/constant type
            pushi 14 ; selector/constant apronSeen
            pTos musicBed
            push0
            callk DoSound, 6
            pushi 3 ; selector/constant type
            pushi 8 ; selector/constant a01Consumed
            pTos musicBed
            push0
            callk DoSound, 6
            pushi 3 ; selector/constant type
            pushi 16 ; selector/constant audienceVolume
            pTos musicBed
            pushi -1
            callk DoSound, 6
            pToa musicMuted
            bnt label_0cc5
            ldi 4
            jmp label_0cc7
            label_0cc5: ldi 1
            label_0cc7: aTop transportMode
            ldi 0
            aTop ownedPauseHeld
            pToa musicPaused
            bnt label_0cd7
            pushi 669 ; selector/constant acquirePause
            push0
            self 4
            label_0cd7: ldi 1
            ret
        )
    )
    ; Original method offset 0x0cda; 61 instructions
    (method (setMuted muted)
        (asm
            lap 1
            bnt label_0ce2
            ldi 1
            jmp label_0ce4
            label_0ce2: ldi 0
            label_0ce4: sap 1
            lsp 1
            pToa musicMuted
            eq?
            bnt label_0cf0
            ldi 1
            ret
            label_0cf0: lap 1
            aTop musicMuted
            pTos lifecycleGeneration
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop lifecycleGeneration
            pToa musicRunning
            not
            bnt label_0d08
            ldi 1
            ret
            label_0d08: pToa musicMuted
            bnt label_0d12
            pushi 687 ; selector/constant holdSilent
            push0
            self 4
            label_0d12: pToa saveGuard
            bt label_0d22
            pToa remapGuard
            bt label_0d22
            pToa musicPaused
            bt label_0d22
            pToa ownedPauseHeld
            bnt label_0d25
            label_0d22: ldi 1
            ret
            label_0d25: pToa positionUncertain
            bnt label_0d31
            pushi 675 ; selector/constant beginHistory
            push0
            self 4
            jmp label_0d48
            label_0d31: pToa musicMuted
            bnt label_0d3b
            ldi 4
            aTop transportMode
            jmp label_0d48
            label_0d3b: pTos transportMode
            ldi 4
            eq?
            bnt label_0d48
            pushi 398 ; selector/constant beginRejoin
            push0
            self 4
            label_0d48: ldi 1
            ret
        )
    )
    ; Original method offset 0x0d4b; 31 instructions
    (method (beforeFrozenSave)
        (if (not (cue120Verify))
                (if musicRunning (self holdSilent:))
                (= transportMode 6)
                (return 0))
            (asm
            pToa musicRunning
            not
            bt label_0d54
            pToa saveGuard
            bnt label_0d57
            label_0d54: ldi 0
            ret
            label_0d57: pushi 687 ; selector/constant holdSilent
            push0
            self 4
            pToa ownedPauseHeld
            not
            bnt label_0d68
            pushi 669 ; selector/constant acquirePause
            push0
            self 4
            label_0d68: pToa ownedPauseHeld
            not
            bnt label_0d70
            ldi 0
            ret
            label_0d70: ldi 1
            aTop saveGuard
            ldi 1
            aTop pausedCheckpoint
            ldi 5
            aTop transportMode
            pToa requestRevision
            aTop saveRevision
            ldi 1
            ret
        )
    )
    ; Original method offset 0x0d83; 31 instructions
    (method (afterFrozenSave)
        (asm
            pToa saveGuard
            not
            bt label_0d8d
            pToa pausedCheckpoint
            not
            bnt label_0d90
            label_0d8d: ldi 0
            ret
            label_0d90: ldi 0
            aTop saveGuard
            ldi 0
            aTop pausedCheckpoint
            pToa musicPaused
            bnt label_0da2
            ldi 9
            aTop transportMode
            jmp label_0dba
            label_0da2: pushi 731 ; selector/constant releasePause
            push0
            self 4
            pToa positionUncertain
            bnt label_0db4
            pushi 675 ; selector/constant beginHistory
            push0
            self 4
            jmp label_0dba
            label_0db4: pushi 398 ; selector/constant beginRejoin
            push0
            self 4
            label_0dba: ldi 1
            ret
        )
    )
    ; Original method offset 0x0dbd; 111 instructions
    (method (afterFrozenRestore)
        (if (not (cue120Verify))
                (if musicRunning (self holdSilent:))
                (= transportMode 6)
                (return 0))
            (asm
            link 1
            pToa musicRunning
            not
            bt label_0dce
            pToa saveGuard
            not
            bt label_0dce
            pToa pausedCheckpoint
            not
            bnt label_0dd1
            label_0dce: ldi 0
            ret
            label_0dd1: pushi 687 ; selector/constant holdSilent
            push0
            self 4
            pToa ownedPauseHeld
            not
            bt label_0dec
            pushi 718 ; selector/constant rawPosition
            push0
            self 4
            not
            bt label_0dec
            pTos musicPosition
            pToa pausedPosition
            ne?
            bnt label_0e03
            label_0dec: ldi 0
            aTop ownedPauseHeld
            ldi 0
            aTop saveGuard
            ldi 0
            aTop pausedCheckpoint
            pushi 679 ; selector/constant failHistory
            push1
            pushi 3 ; selector/constant type
            self 6
            ldi 0
            ret
            label_0e03: ldi 0
            aTop saveGuard
            ldi 0
            aTop pausedCheckpoint
            ldi 0
            aTop ownedPauseHeld
            ipToa checkpointRestores
            pTos lifecycleGeneration
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop lifecycleGeneration
            push0
            callk GetTime, 0
            sat 0
            pushi 719 ; selector/constant readCivil
            push0
            self 4
            pushi 672 ; selector/constant anchorClock
            push1
            lst 0
            self 6
            ldi -1
            aTop previousPosition
            lat 0
            aTop lastProgressTick
            lat 0
            aTop lastRampTick
            pToa musicPaused
            bnt label_0e69
            pushi 3 ; selector/constant type
            pushi 10 ; selector/constant advance
            pTos ownedBed
            push1
            callk DoSound, 6
            ldi 1
            aTop ownedPauseHeld
            ipToa pauseAcquires
            pToa pausePhaseKnown
            not
            aTop positionUncertain
            pToa positionUncertain
            not
            bnt label_0e63
            pushi 673 ; selector/constant anchorPosition
            push1
            lst 0
            self 6
            label_0e63: ldi 9
            aTop transportMode
            jmp label_0e8b
            label_0e69: pushi 3 ; selector/constant type
            pushi 10 ; selector/constant advance
            pTos ownedBed
            push0
            callk DoSound, 6
            pushi 680 ; selector/constant finishPauseResume
            push0
            self 4
            pToa positionUncertain
            bnt label_0e85
            pushi 675 ; selector/constant beginHistory
            push0
            self 4
            jmp label_0e8b
            label_0e85: pushi 398 ; selector/constant beginRejoin
            push0
            self 4
            label_0e8b: ldi 1
            ret
        )
    )
    ; Original method offset 0x0e8e; 50 instructions
    (method (beforeSave)
        (if (not (cue120Verify))
                (if musicRunning (self holdSilent:))
                (= transportMode 6)
                (return 0))
            (asm
            pToa musicRunning
            not
            bt label_0e97
            pToa saveGuard
            bnt label_0e9a
            label_0e97: ldi 0
            ret
            label_0e9a: pToa ownedPauseHeld
            bnt label_0ea4
            pushi 731 ; selector/constant releasePause
            push0
            self 4
            label_0ea4: pushi 678 ; selector/constant clockFresh
            push1
            push0
            callk GetTime, 0
            push
            self 6
            not
            bnt label_0eb8
            pushi 675 ; selector/constant beginHistory
            push0
            self 4
            label_0eb8: pToa positionUncertain
            not
            bnt label_0ec3
            pushi 428 ; selector/constant readPosition
            push0
            self 4
            label_0ec3: ldi 1
            aTop saveGuard
            ldi 0
            aTop pausedCheckpoint
            pToa transportMode
            aTop resumeMode
            pToa wholeGain
            aTop savedWholeGain
            pToa requestRevision
            aTop saveRevision
            ldi 0
            aTop wholeGain
            ldi 5
            aTop transportMode
            pushi 3 ; selector/constant type
            pushi 14 ; selector/constant apronSeen
            pTos musicBed
            push0
            callk DoSound, 6
            ldi 1
            ret
        )
    )
    ; Original method offset 0x0eec; 62 instructions
    (method (afterSave)
        (asm
            pToa saveGuard
            not
            bnt label_0ef4
            ldi 0
            ret
            label_0ef4: pushi 678 ; selector/constant clockFresh
            push1
            push0
            callk GetTime, 0
            push
            self 6
            not
            bnt label_0f08
            pushi 675 ; selector/constant beginHistory
            push0
            self 4
            label_0f08: pToa positionUncertain
            not
            bnt label_0f13
            pushi 428 ; selector/constant readPosition
            push0
            self 4
            label_0f13: ldi 0
            aTop saveGuard
            push0
            callk GetTime, 0
            aTop lastRampTick
            pToa lastRampTick
            aTop lastPollTick
            pTos lifecycleGeneration
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop lifecycleGeneration
            pushi 719 ; selector/constant readCivil
            push0
            self 4
            pushi 672 ; selector/constant anchorClock
            push1
            push0
            callk GetTime, 0
            push
            self 6
            pToa musicPaused
            bnt label_0f4a
            pushi 669 ; selector/constant acquirePause
            push0
            self 4
            jmp label_0f5c
            label_0f4a: pToa positionUncertain
            bnt label_0f56
            pushi 675 ; selector/constant beginHistory
            push0
            self 4
            jmp label_0f5c
            label_0f56: pushi 398 ; selector/constant beginRejoin
            push0
            self 4
            label_0f5c: ldi 1
            ret
        )
    )
    ; Original method offset 0x0f5f; 63 instructions
    (method (afterRestore)
        (if (not (cue120Verify))
                (if musicRunning (self holdSilent:))
                (= transportMode 6)
                (return 0))
            (asm
            pToa musicRunning
            not
            bt label_0f69
            pToa saveGuard
            not
            bnt label_0f6c
            label_0f69: ldi 0
            ret
            label_0f6c: pToa ownedPauseHeld
            bnt label_0f7a
            pushi 679 ; selector/constant failHistory
            push1
            push1
            self 6
            ldi 0
            ret
            label_0f7a: ldi 0
            aTop saveGuard
            ldi 0
            aTop wholeGain
            pushi 3 ; selector/constant type
            pushi 14 ; selector/constant apronSeen
            pTos musicBed
            push0
            callk DoSound, 6
            pushi 256 ; selector/constant signal
            push1
            push0
            pToa musicBed
            send 6
            ldi -1
            aTop previousPosition
            ldi 1
            aTop positionUncertain
            push0
            callk GetTime, 0
            aTop lastPollTick
            pToa lastPollTick
            aTop lastRampTick
            pTos lifecycleGeneration
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop lifecycleGeneration
            pushi 719 ; selector/constant readCivil
            push0
            self 4
            pushi 672 ; selector/constant anchorClock
            push1
            pTos lastPollTick
            self 6
            pushi 675 ; selector/constant beginHistory
            push0
            self 4
            pToa musicPaused
            bnt label_0fd1
            pushi 669 ; selector/constant acquirePause
            push0
            self 4
            label_0fd1: ldi 1
            ret
        )
    )
    ; Original method offset 0x0fd4; 22 instructions
    (method (notifyRemap)
        (asm
            pToa saveGuard
            bt label_0fdc
            pToa remapGuard
            bnt label_0fdf
            label_0fdc: ldi 0
            ret
            label_0fdf: ldi 1
            aTop remapGuard
            pTos lifecycleGeneration
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop lifecycleGeneration
            pushi 687 ; selector/constant holdSilent
            push0
            self 4
            ldi 7
            aTop transportMode
            ldi 1
            ret
        )
    )
    ; Original method offset 0x0ffc; 32 instructions
    (method (finishRemap)
        (asm
            pToa saveGuard
            bt label_1005
            pToa remapGuard
            not
            bnt label_1008
            label_1005: ldi 0
            ret
            label_1008: ldi 0
            aTop remapGuard
            pTos lifecycleGeneration
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop lifecycleGeneration
            ldi 1
            aTop remapDrain
            push0
            callk GetTime, 0
            aTop remapStart
            pushi 675 ; selector/constant beginHistory
            push0
            self 4
            push0
            callk GetTime, 0
            push
            ldi 4
            add
            aTop retryAt
            ldi 1
            ret
        )
    )
    ; Original method offset 0x1035; 20 instructions
    (method (retryRejoin)
        (asm
            pToa saveGuard
            bt label_1044
            pToa remapGuard
            bt label_1044
            pTos transportMode
            ldi 6
            ne?
            bnt label_1047
            label_1044: ldi 0
            ret
            label_1047: pToa positionUncertain
            bnt label_1052
            pushi 675 ; selector/constant beginHistory
            push0
            self 4
            ret
            label_1052: pushi 398 ; selector/constant beginRejoin
            push0
            self 4
            ret
        )
    )
    ; Original method offset 0x1059; 21 instructions
    (method (expireRejoin)
        (asm
            ldi 0
            aTop wholeGain
            pushi 3 ; selector/constant type
            pushi 14 ; selector/constant apronSeen
            pTos musicBed
            push0
            callk DoSound, 6
            pushi 400 ; selector/constant clearMutedBed
            push0
            self 4
            ipToa rejoinExpired
            ldi -1
            aTop rejoinWindow
            push0
            callk GetTime, 0
            push
            ldi 2
            add
            aTop retryAt
            ldi 0
            ret
        )
    )
    ; Original method offset 0x1080; 250 instructions
    (method (tryRejoin)
        (asm
            link 11
            pToa saveGuard
            bt label_10a1
            pToa remapGuard
            bt label_10a1
            pToa musicMuted
            bt label_10a1
            pToa musicPaused
            bt label_10a1
            pToa ownedPauseHeld
            bt label_10a1
            pToa positionUncertain
            bt label_10a1
            pTos transportMode
            ldi 3
            ne?
            bnt label_10a4
            label_10a1: ldi 0
            ret
            label_10a4: pTos rejoinAttempts
            ldi 32
            ge?
            bt label_10ba
            push0
            callk GetTime, 0
            push
            pToa rejoinStart
            sub
            push
            ldi 600
            uge?
            bnt label_10c3
            label_10ba: ldi 6
            aTop transportMode
            ipToa rejoinFailures
            ldi 0
            ret
            label_10c3: pToa remapDrain
            bnt label_10dc
            push0
            callk GetTime, 0
            push
            pToa remapStart
            sub
            push
            ldi 4
            ult?
            bnt label_10d8
            ldi 0
            ret
            label_10d8: ldi 0
            aTop remapDrain
            label_10dc: push0
            callk GetTime, 0
            push
            pToa retryAt
            sub
            push
            ldi 0
            lt?
            bnt label_10ed
            ldi 0
            ret
            label_10ed: ldi -1
            aTop rejoinWindow
            ldi 0
            sat 0
            label_10f5: lst 0
            ldi 57
            lt?
            bnt label_1125
            lst 0
            ldi 5
            mul
            sat 1
            pTos musicPosition
            lat 1
            lali keyWindows
            ge?
            bnt label_1121
            pTos musicPosition
            lst 1
            ldi 1
            add
            lali keyWindows
            le?
            bnt label_1121
            lat 0
            aTop rejoinWindow
            jmp label_1125
            label_1121: +at 0
            jmp label_10f5
            label_1125: pTos rejoinWindow
            ldi -1
            eq?
            bnt label_112f
            ldi 0
            ret
            label_112f: ipToa rejoinAttempts
            pToa musicPosition
            sat 9
            pToa loopEpoch
            aTop rejoinEpoch
            push0
            callk GetTime, 0
            sat 10
            lat 1
            lali keyWindows
            sat 2
            lst 1
            ldi 1
            add
            lali keyWindows
            sat 3
            lst 1
            ldi 2
            add
            lali keyWindows
            sat 4
            lst 1
            ldi 3
            add
            lali keyWindows
            sat 5
            lst 1
            ldi 4
            add
            lali keyWindows
            sat 6
            pushi 400 ; selector/constant clearMutedBed
            push0
            self 4
            pushi 429 ; selector/constant rebuildControllers
            push1
            lst 9
            self 6
            pushi 428 ; selector/constant readPosition
            push0
            self 4
            pToa positionUncertain
            bnt label_1189
            ldi 0
            ret
            label_1189: pTos musicPosition
            lat 9
            lt?
            bt label_11ac
            pTos musicPosition
            lat 3
            gt?
            bt label_11ac
            pTos loopEpoch
            pToa rejoinEpoch
            ne?
            bt label_11ac
            push0
            callk GetTime, 0
            push
            lat 10
            sub
            push
            ldi 4
            ugt?
            bnt label_11b3
            label_11ac: pushi 407 ; selector/constant expireRejoin
            push0
            self 4
            ret
            label_11b3: ldi 0
            aTop lastBatchKeys
            ldi 0
            sat 7
            label_11bb: lst 7
            lat 6
            lt?
            bnt label_1207
            lst 5
            lst 7
            ldi 4
            mul
            add
            sat 0
            lat 0
            lali heldNotes
            sat 8
            lat 8
            lsli currentGains
            ldi 0
            gt?
            bnt label_1203
            pushi 6 ; selector/constant x
            pushi 18 ; selector/constant audioApron
            pTos musicBed
            lat 8
            lsli midiChannels
            ldi 1
            add
            push
            pushi 144 ; selector/constant motionScale
            lst 0
            ldi 1
            add
            lsli heldNotes
            lst 0
            ldi 2
            add
            lsli heldNotes
            callk DoSound, 12
            ipToa lastBatchKeys
            label_1203: +at 7
            jmp label_11bb
            label_1207: pushi 428 ; selector/constant readPosition
            push0
            self 4
            pToa positionUncertain
            bnt label_1214
            ldi 0
            ret
            label_1214: pTos musicPosition
            lat 9
            lt?
            bt label_1234
            pTos musicPosition
            ldi 3
            add
            push
            lat 4
            gt?
            bt label_1234
            push0
            callk GetTime, 0
            push
            lat 10
            sub
            push
            ldi 6
            ugt?
            bnt label_123b
            label_1234: pushi 407 ; selector/constant expireRejoin
            push0
            self 4
            ret
            label_123b: ipToa rejoinSuccesses
            ldi 2
            aTop transportMode
            push0
            callk GetTime, 0
            aTop lastRampTick
            ldi 1
            ret
        )
    )
    ; Original method offset 0x124a; 181 instructions
    (method (ramp now)
        (asm
            link 4
            pToa musicPaused
            bt label_125c
            pToa ownedPauseHeld
            bt label_125c
            pToa saveGuard
            bt label_125c
            pToa musicMuted
            bnt label_125f
            label_125c: ldi 0
            ret
            label_125f: lsp 1
            pToa lastRampTick
            sub
            push
            ldi 2
            ult?
            bnt label_126d
            ldi 0
            ret
            label_126d: lap 1
            aTop lastRampTick
            ldi 1
            sat 2
            ldi 0
            sat 0
            label_1279: lst 0
            ldi 8
            lt?
            bnt label_1352
            lat 0
            lali currentGains
            sat 1
            lat 0
            lsli midiChannels
            ldi 1
            add
            sat 3
            lst 1
            lat 0
            lali targetGains
            ne?
            bnt label_134d
            ldi 0
            sat 2
            lst 1
            ldi 0
            eq?
            bnt label_12f8
            lat 0
            lsli targetGains
            ldi 0
            gt?
            bnt label_12f8
            lst 0
            ldi 2
            eq?
            bt label_12bd
            lst 0
            ldi 6
            eq?
            bnt label_12f6
            label_12bd: pTos musicPosition
            ldi 2
            ge?
            bnt label_12f6
            pTos musicPosition
            ldi 1161
            le?
            bnt label_12f6
            pushi 5 ; selector/constant modifiers
            pushi 18 ; selector/constant audioApron
            pTos musicBed
            lst 3
            pushi 120 ; selector/constant jackLeft
            push0
            callk DoSound, 10
            pushi 5 ; selector/constant modifiers
            pushi 18 ; selector/constant audioApron
            pTos musicBed
            lst 3
            pushi 11 ; selector/constant applyMix
            pushi 408 ; selector/constant expressionAt
            push2
            lst 0
            pTos musicPosition
            self 8
            push
            callk DoSound, 10
            ldi 4
            sat 1
            label_12f6: jmp label_132f
            label_12f8: lst 1
            lat 0
            lali targetGains
            lt?
            bnt label_1319
            lst 1
            ldi 4
            add
            sat 1
            lst 1
            lat 0
            lali targetGains
            gt?
            bnt label_1317
            lat 0
            lali targetGains
            sat 1
            label_1317: jmp label_132f
            label_1319: lst 1
            ldi 4
            sub
            sat 1
            lst 1
            lat 0
            lali targetGains
            lt?
            bnt label_132f
            lat 0
            lali targetGains
            sat 1
            label_132f: lst 1
            lat 0
            lali currentGains
            ne?
            bnt label_134d
            lst 1
            lat 0
            sali currentGains
            pushi 5 ; selector/constant modifiers
            pushi 18 ; selector/constant audioApron
            pTos musicBed
            lst 3
            pushi 7 ; selector/constant y
            lst 1
            callk DoSound, 10
            label_134d: +at 0
            jmp label_1279
            label_1352: lat 2
            bnt label_135a
            pToa nextRequestedState
            jmp label_135c
            label_135a: ldi -1
            label_135c: aTop settledState
            pTos wholeGain
            pToa desiredWholeGain
            ne?
            bnt label_139d
            pTos wholeGain
            pToa desiredWholeGain
            lt?
            bnt label_1380
            pTos wholeGain
            ldi 10
            add
            aTop wholeGain
            pTos wholeGain
            pToa desiredWholeGain
            gt?
            bnt label_137e
            pToa desiredWholeGain
            aTop wholeGain
            label_137e: jmp label_1392
            label_1380: pTos wholeGain
            ldi 10
            sub
            aTop wholeGain
            pTos wholeGain
            pToa desiredWholeGain
            lt?
            bnt label_1392
            pToa desiredWholeGain
            aTop wholeGain
            label_1392: pushi 3 ; selector/constant type
            pushi 14 ; selector/constant apronSeen
            pTos musicBed
            pTos wholeGain
            callk DoSound, 6
            label_139d: ldi 1
            ret
        )
    )
    ; Original method offset 0x13a0; 60 instructions
    (method (refreshCurrentGains)
        (asm
            link 1
            pToa musicRunning
            not
            bt label_13d5
            pToa saveGuard
            bt label_13d5
            pToa musicPaused
            bt label_13d5
            pToa ownedPauseHeld
            bt label_13d5
            pToa positionUncertain
            bt label_13d5
            pTos musicBed
            pToa ownedBed
            ne?
            bt label_13d5
            push1
            pTos ownedBed
            callk IsObject, 2
            not
            bt label_13d5
            pTos transportMode
            ldi 2
            ne?
            bnt label_13d8
            pTos transportMode
            ldi 4
            ne?
            bnt label_13d8
            label_13d5: ldi 0
            ret
            label_13d8: ldi 0
            sat 0
            label_13dc: lst 0
            ldi 8
            lt?
            bnt label_13ff
            pushi 5 ; selector/constant modifiers
            pushi 18 ; selector/constant audioApron
            pTos ownedBed
            lat 0
            lsli midiChannels
            ldi 1
            add
            push
            pushi 7 ; selector/constant y
            lat 0
            lsli currentGains
            callk DoSound, 10
            +at 0
            jmp label_13dc
            label_13ff: pTos gainRefreshes
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop gainRefreshes
            ldi 1
            ret
        )
    )
    ; Original method offset 0x140e; 152 instructions
    (method (poll)
        (asm
            link 2
            pToa musicRunning
            not
            bnt label_1418
            ldi 0
            ret
            label_1418: pToa ownedPauseHeld
            bnt label_1423
            ldi 9
            aTop transportMode
            ldi 9
            ret
            label_1423: push0
            callk GetTime, 0
            sat 0
            pushi 678 ; selector/constant clockFresh
            push1
            lst 0
            self 6
            not
            bnt label_1448
            pushi 720 ; selector/constant recoverGap
            push1
            lst 0
            self 6
            not
            bnt label_1445
            pushi 675 ; selector/constant beginHistory
            push0
            self 4
            label_1445: pToa transportMode
            ret
            label_1448: pushi 672 ; selector/constant anchorClock
            push1
            lst 0
            self 6
            pToa saveGuard
            bnt label_1457
            pToa transportMode
            ret
            label_1457: pToa remapGuard
            bnt label_145e
            ldi 7
            ret
            label_145e: pToa positionUncertain
            bnt label_1478
            pTos transportMode
            ldi 8
            eq?
            bnt label_1471
            pushi 704 ; selector/constant observeHistory
            push1
            lst 0
            self 6
            label_1471: pToa positionUncertain
            bnt label_1478
            pToa transportMode
            ret
            label_1478: pushi 428 ; selector/constant readPosition
            push0
            self 4
            pToa positionUncertain
            bnt label_1485
            pToa transportMode
            ret
            label_1485: pushi 256 ; selector/constant signal
            push0
            pToa musicBed
            send 4
            sat 1
            lst 1
            ldi 0
            gt?
            bnt label_14a3
            lat 1
            aTop lastCue
            pushi 256 ; selector/constant signal
            push1
            push0
            pToa musicBed
            send 6
            label_14a3: pToa musicMuted
            bnt label_14b0
            pushi 730 ; selector/constant refreshCurrentGains
            push0
            self 4
            pToa transportMode
            ret
            label_14b0: pTos transportMode
            ldi 1
            eq?
            bnt label_14fe
            lst 1
            ldi 1
            eq?
            bnt label_14ea
            pTos musicPosition
            ldi 6
            ge?
            bnt label_14ea
            pTos musicPosition
            ldi 8
            le?
            bnt label_14ea
            pushi 429
            push1
            pTos musicPosition
            self 6
            pushi 428
            push0
            self 4
            pToa positionUncertain
            bt label_14f8
            pTos musicPosition
            ldi 8
            gt?
            bt label_14f8
            pToa desiredWholeGain
            aTop wholeGain
            pushi 3 ; selector/constant type
            pushi 14 ; selector/constant apronSeen
            pTos musicBed
            pTos wholeGain
            callk DoSound, 6
            ldi 2
            aTop transportMode
            ipToa initialOpens
            jmp label_14fe
            label_14ea: pTos musicPosition
            ldi 8
            gt?
            bt label_14f8
            jmp label_14fe
            label_14f8: pushi 398 ; selector/constant beginRejoin
            push0
            self 4
            label_14fe: pTos transportMode
            ldi 3
            eq?
            bnt label_150b
            pushi 505 ; selector/constant tryRejoin
            push0
            self 4
            label_150b: pTos transportMode
            ldi 2
            eq?
            bnt label_1523
            pushi 427 ; selector/constant ramp
            push1
            push0
            callk GetTime, 0
            push
            self 6
            pushi 730 ; selector/constant refreshCurrentGains
            push0
            self 4
            label_1523: pToa transportMode
            ret
        )
    )
    ; Original method offset 0x1526; 35 instructions
    (method (stop)
        (asm
            pToa musicRunning
            bnt label_1542
            push1
            pTos ownedBed
            callk IsObject, 2
            bnt label_1542
            push2
            pushi 9 ; selector/constant act
            pTos ownedBed
            callk DoSound, 4
            push2
            pushi 7 ; selector/constant y
            pTos ownedBed
            callk DoSound, 4
            label_1542: pTos lifecycleGeneration
            ldi 1
            add
            push
            ldi 30000
            mod
            aTop lifecycleGeneration
            ldi 0
            aTop musicRunning
            ldi 0
            aTop transportMode
            ldi 0
            aTop wholeGain
            ldi 0
            aTop saveGuard
            ldi 0
            aTop remapGuard
            ldi 0
            aTop ownedPauseHeld
            ldi 1
            ret
        )
    )
)

