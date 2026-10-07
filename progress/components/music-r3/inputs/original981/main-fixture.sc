;;; Sierra Script 1.0 - (do not remove this comment)
(script# 0)
(public cakood 0)
(class Game
    (properties
        navNotice 0
        navNoticeTicks 0
        musicOwner 0
        musicOwnerKind 0
        musicChooserKind 0
        musicUnavailable 0
        foleySerial 0
        foleyWalkSerial 0
        foleyOrdinal 0
        foleyWalkToken -1
        foleyLastStep 0
        foleyLastWood 0
        foleyLastRevision -1
        foleyLastDomainEvent -1
        p03 0
        p03WantCredit 0
        p03WantTopics 0
        p03TopicActor 0
        p03HostError 0
        p03LastStatus 0
        p03Invalid 0
        dialogue 0
        presentation 0
        speechCaption 0
        speechPart 0
        talkLogIndex 0
        type 0
        message 0
        modifiers 0
        x 0
        y 0
        location 0
        onApron 0
        tray 0
        wedge 0
        doorOpen 0
        bunnyReady 0
        traySafe 0
        houseEntered 0
        p01Consumed 0
        a01Consumed 0
        greetingConsumed 0
        selected 0
        nounA 0
        hover 0
        currentCaption 1
        hintLevel 0
        audienceMuted 0
        musicMuted 0
        paused 0
        menuOpen 0
        quitRequested 0
        opening 1
        creditCard 0
        creditHeld 0
        creditElapsed 0
        replayOpening 0
        initialized 0
        initCount 0
        lastTick 0
        dirty 1
        jackLeft 128
        jackTarget 128
        jackPose 0
        moveTicks 0
        returnLeft 128
        audioRoom 0
        audioApron 0
        audioDialogue 0
        audioMusic 2
        audioHold 0
        audioPending 0
        audioSerial 0
        audioLastEvent 0
        masterVolume 100
        audienceVolume 100
        audioDuckTicks 0
        audioReady 0
        audioPhase -1
        audioDesired 0
        audioApplied -1
        audioFade 0
        audioTarget 100
        audioLastTarget -1
        audioLastPCM -1
        audioBedHeld 0
        audioStingHeld 0
        audioCreditsHeld 0
        audioPCMheld 0
        audioGuardCount 0
        audioLastGuard 0
        audioLogIndex 0
        audioLastRoom -1
        audioLastApron -1
        audioLastMuted 0
        audioSaveResult 0
        testFailures 0
        testChecks 0
        traceIndex 0
        testMode 0
        p02Initialized 0
        p02Revision 0
        p02CopyJack 13
        p02CopyBunny 1
        p02CopyStringer 6
        p02Permissions 0
        p02Observed 0
        p02BoardRecords 0
        p02Compared 0
        p02KnowPurpose 0
        p02KnowOrder 0
        p02PlanAgreed 0
        p02ComparisonConsumed 0
        p02CompleteConsumed 0
        p02MiloShown 0
        p02DrawerOpen 0
        p02MasterHeld 0
        p02SelectedAims 0
        p02PlanStarted 0
        p02PlanOpen 0
        p02HintLevel 0
        p02InventoryExtent 2
        p02GapJack -1
        p02GapBunny -1
        p02GapStringer -1
        p02InventoryOverflow 0
        uiPanel 0
        uiDocument 0
        uiPage 0
        uiPageCount 1
        uiTitle 0
        uiBackPanel 0
        uiBackPage 0
        uiBackFocus 0
        uiBackTitle 0
        uiFocus 0
        uiHover -1
        uiLastX -1
        uiLastY -1
        uiControlCount 0
        uiReveal 0
        uiVerb 0
        uiNounA 0
        uiFocusObject 0
        uiInventoryExtent 0
        uiInventoryPage 0
        uiInventoryPages 1
        uiChoiceCount 0
        uiChoiceContext 0
        uiChoiceMulti 0
        uiFailure 0
        uiLastCallback 0
        uiFullSentence 0
        motionX 8960
        motionY 8448
        motionTargetX 140
        motionTargetY 132
        motionGoalX 140
        motionGoalY 132
        motionPhase 0
        motionTicks 0
        motionFrame 0
        motionLoop 0
        motionPose 0
        motionVerb 0
        motionFirst 0
        motionSecond 0
        motionRoom 0
        motionApron 0
        motionNotice 0
        roomSeen 0
        apronSeen 0
        callbackOldRoom 0
        callbackOldApron 0
        integrationReady 0
        observedRevision -1
        observedRoom -1
        observedApron -1
        observedReadSerial -1
        bridgeQueueCount 0
        bridgeQueueIndex 0
        bridgeWantPlan 0
        bridgeSilent 0
        bridgeReaderActive 0
        bridgePendingObject 0
        bridgePendingDocument 0
        bridgePendingRecord 0
        bridgePendingPages 0
        bridgePendingRoom -1
        bridgeVisitedCount 0
        bridgeCommitRead 0
        bridgeReadSerial 0
        bridgeCancelledSerial 0
        bridgeRestoreSerial 0
        bridgeLastCancelReason 0
        bridgeChoiceActor 0
        bridgeFailure 0
    )
; Reconstructed P03 Main score/audio lifecycle methods.
; Insert inside Game; replace methods of the same names.
; Uses the exact P03 selector vocabulary and symbolic property/object references.
; No original source authorship claimed. See score/README.md.
; Original Main method 0x0536
(method (syncAudio)
    (asm
        pTos location
        ldi 0
        eq?
        bnt audio_label_0541
        ldi 0
        jmp audio_label_0543
        audio_label_0541: ldi 1
        audio_label_0543: aTop audioRoom
        pToa onApron
        aTop audioApron
        pToa opening
        bnt audio_label_0553
        ldi 2
        jmp audio_label_0555
        audio_label_0553: ldi 0
        audio_label_0555: aTop audioMusic
        pToa onApron
        bnt audio_label_0560
        ldi 1
        jmp audio_label_0562
        audio_label_0560: ldi 0
        audio_label_0562: aTop audioDesired
        pToa opening
        bnt audio_label_0575
        pToa creditHeld
        bnt audio_label_0571
        ldi 1
        jmp audio_label_0573
        audio_label_0571: ldi 0
        audio_label_0573: jmp audio_label_0583
        audio_label_0575: pToa paused
        bt audio_label_057d
        pToa menuOpen
        bnt audio_label_0581
        audio_label_057d: ldi 1
        jmp audio_label_0583
        audio_label_0581: ldi 0
        audio_label_0583: aTop audioHold
        ret
    )
)

; Original Main method 0x0587
(method (audioEvent eventId)
    (asm
        lap 1
        aTop audioLastEvent
        ipToa audioSerial
        lsp 1
        ldi 4
        eq?
        bt audio_label_059d
        lsp 1
        ldi 5
        eq?
        bnt audio_label_05b6
        audio_label_059d: pToa audienceMuted
        not
        bnt audio_label_05b6
        pTos audioPending
        lsp 1
        ldi 4
        eq?
        bnt audio_label_05b0
        ldi 2
        jmp audio_label_05b2
        audio_label_05b0: ldi 4
        audio_label_05b2: or
        aTop audioPending
        audio_label_05b6: ret
    )
)

; Original Main method 0x05b7
(method (takeAudio)
    (asm
        link 1
        pToa audioPending
        sat 0
        ldi 0
        aTop audioPending
        lat 0
        ret
    )
)

; Original Main method 0x0718
(method (audioHolds)
    (asm
        link 1
        pTos musicOwnerKind
        ldi 2
        eq?
        bnt audio_label_0738
        pushi 734
        push1
        pToa paused
        bt audio_label_072d
        pToa menuOpen
        bnt audio_label_0731
        audio_label_072d: ldi 1
        jmp audio_label_0733
        audio_label_0731: ldi 0
        audio_label_0733: push
        pToa musicOwner
        send 6
        audio_label_0738: pTos musicOwnerKind
        ldi 1
        eq?
        bnt audio_label_0747
        pToa creditHeld
        bnt audio_label_0747
        ldi 1
        jmp audio_label_0749
        audio_label_0747: ldi 0
        audio_label_0749: sat 0
        lst 0
        pToa audioCreditsHeld
        ne?
        bnt audio_label_076b
        pTos musicOwnerKind
        ldi 1
        eq?
        bnt audio_label_0766
        pushi 3
        pushi 10
        lofss credits
        lst 0
        callk DoSound, 6
        audio_label_0766: lat 0
        aTop audioCreditsHeld
        audio_label_076b: pTos audioHold
        pToa audioPCMheld
        ne?
        bnt audio_label_0785
        pToa audioHold
        bnt audio_label_077f
        pushi 377
        push0
        self 4
        audio_label_077f: pToa audioHold
        aTop audioPCMheld
        audio_label_0785: ret
    )
)

; Original Main method 0x0786
(method (audioPoll elapsedTicks)
    (asm
        link 3
        pToa audioReady
        not
        bnt audio_label_0791
        ldi 0
        ret
        audio_label_0791: lsp 1
        ldi 0
        lt?
        bnt audio_label_079c
        ldi 0
        sap 1
        audio_label_079c: lsp 1
        ldi 12
        gt?
        bnt audio_label_07a7
        ldi 12
        sap 1
        audio_label_07a7: pushi 700
        push0
        self 4
        pushi 28
        push0
        self 4
        pToa audioHold
        not
        bnt audio_label_07d6
        pTos audioDuckTicks
        ldi 0
        gt?
        bnt audio_label_07d6
        pTos audioDuckTicks
        lap 1
        sub
        aTop audioDuckTicks
        pTos audioDuckTicks
        ldi 0
        lt?
        bnt audio_label_07d6
        ldi 0
        aTop audioDuckTicks
        audio_label_07d6: pTos masterVolume
        pToa audioDuckTicks
        bnt audio_label_07e2
        ldi 60
        jmp audio_label_07e4
        audio_label_07e2: ldi 100
        audio_label_07e4: mul
        push
        ldi 100
        div
        aTop audioTarget
        pToa audienceMuted
        bnt audio_label_07f4
        ldi 0
        jmp audio_label_07ff
        audio_label_07f4: pTos masterVolume
        pToa audienceVolume
        mul
        push
        ldi 100
        div
        audio_label_07ff: sat 1
        lst 1
        pToa audioLastPCM
        ne?
        bnt audio_label_0836
        pToa presentation
        bnt audio_label_0828
        pushi 16
        push1
        pTos audienceVolume
        pushi 126
        push1
        pTos masterVolume
        pToa presentation
        send 12
        pushi 373
        push2
        push2
        pTos audienceMuted
        pToa presentation
        send 8
        audio_label_0828: lat 1
        aTop audioLastPCM
        pToa audienceMuted
        bnt audio_label_0836
        ldi 0
        aTop audioPending
        audio_label_0836: pTos musicOwnerKind
        ldi 1
        eq?
        bnt audio_label_0855
        pushi 3
        pushi 14
        lofss credits
        pToa musicMuted
        bnt audio_label_084c
        ldi 0
        jmp audio_label_084f
        audio_label_084c: pToa masterVolume
        audio_label_084f: push
        callk DoSound, 6
        jmp audio_label_0888
        audio_label_0855: pTos musicOwnerKind
        ldi 2
        eq?
        bnt audio_label_0888
        pushi 698
        push0
        self 4
        pushi 367
        push0
        pToa musicOwner
        send 4
        sat 2
        lst 2
        ldi 6
        eq?
        bt audio_label_087e
        pushi 421
        push0
        pToa musicOwner
        send 4
        not
        bnt audio_label_0884
        audio_label_087e: ldi 1
        aTop musicUnavailable
        jmp audio_label_0888
        audio_label_0884: ldi 0
        aTop musicUnavailable
        audio_label_0888: pushi 260
        push0
        self 4
        sat 0
        pToa opening
        not
        bnt audio_label_08d5
        pToa audioHold
        not
        bnt audio_label_08d5
        lst 0
        ldi 2
        and
        bnt audio_label_08d5
        pToa audienceMuted
        not
        bnt audio_label_08d5
        pToa presentation
        bnt audio_label_08cd
        pushi 369
        pushi 9
        pTos audioSerial
        push2
        pushi 920
        push2
        push1
        push0
        push1
        push0
        callk GetTime, 0
        push
        pushi 388
        push0
        pToa presentation
        send 4
        push
        pToa presentation
        send 22
        audio_label_08cd: pushi 52
        push1
        lofss "real audience request"
        self 6
        audio_label_08d5: ret
    )
)

; Original Main method 0x08d6
(method (audioInit)
    (asm
        ldi 1
        aTop audioReady
        ldi 0
        aTop musicOwnerKind
        ldi -1
        aTop audioPhase
        pushi 700
        push0
        self 4
        pushi 28
        push0
        self 4
        pushi 52
        push1
        lofss "audio started"
        self 6
        ret
    )
)

; Original Main method 0x08f8
(method (audioRestore)
    (asm
        pushi 377
        push0
        self 4
        ldi 0
        aTop audioPCMheld
        ldi 0
        aTop audioPending
        ldi 0
        aTop audioDuckTicks
        ldi -1
        aTop audioLastPCM
        pToa opening
        aTop audioPhase
        ldi 0
        aTop musicUnavailable
        pToa opening
        bnt audio_label_095a
        pTos musicOwnerKind
        ldi 1
        ne?
        bt audio_label_092d
        pTos musicChooserKind
        ldi 1
        ne?
        bnt audio_label_0934
        audio_label_092d: ldi 1
        aTop musicUnavailable
        ldi 0
        ret
        audio_label_0934: ldi 0
        aTop audioCreditsHeld
        ldi 0
        aTop musicChooserKind
        pushi 28
        push0
        self 4
        pushi 3
        pushi 14
        lofss credits
        pToa musicMuted
        bnt audio_label_0951
        ldi 0
        jmp audio_label_0954
        audio_label_0951: pToa masterVolume
        audio_label_0954: push
        callk DoSound, 6
        jmp audio_label_0988
        audio_label_095a: pTos musicOwnerKind
        ldi 2
        ne?
        bt audio_label_0968
        pTos musicChooserKind
        ldi 2
        ne?
        bnt audio_label_096f
        audio_label_0968: ldi 1
        aTop musicUnavailable
        ldi 0
        ret
        audio_label_096f: ldi 0
        aTop musicChooserKind
        pushi 670
        push0
        pToa musicOwner
        send 4
        not
        bnt audio_label_0982
        ldi 1
        aTop musicUnavailable
        audio_label_0982: pushi 698
        push0
        self 4
        audio_label_0988: pushi 52
        push1
        lofss "replay owner restored"
        self 6
        ret
    )
)

; Original Main method 0x0991
(method (audioStop)
    (asm
        pushi 377
        push0
        self 4
        pushi 701
        push0
        self 4
        pushi 52
        push1
        lofss "audio exit"
        self 6
        ldi 0
        aTop audioReady
        ret
    )
)

; Original Main method 0x9e22
(method (musicRequests)
    (asm
        pToa musicOwner
        not
        bt audio_label_9e2e
        pTos musicOwnerKind
        ldi 2
        ne?
        bnt audio_label_9e31
        audio_label_9e2e: ldi 0
        ret
        audio_label_9e31: pTos masterVolume
        pToa audioDuckTicks
        bnt audio_label_9e3d
        ldi 60
        jmp audio_label_9e3f
        audio_label_9e3d: ldi 100
        audio_label_9e3f: mul
        push
        ldi 100
        div
        aTop audioTarget
        pushi 735
        push1
        pTos audioTarget
        pToa musicOwner
        send 6
        pushi 499
        push1
        pToa musicMuted
        bnt audio_label_9e5e
        ldi 1
        jmp audio_label_9e60
        audio_label_9e5e: ldi 0
        audio_label_9e60: push
        pToa musicOwner
        send 6
        pushi 734
        push1
        pToa paused
        bt audio_label_9e71
        pToa menuOpen
        bnt audio_label_9e75
        audio_label_9e71: ldi 1
        jmp audio_label_9e77
        audio_label_9e75: ldi 0
        audio_label_9e77: push
        pToa musicOwner
        send 6
        pTos audioDesired
        pushi 423
        push0
        pToa musicOwner
        send 4
        ne?
        bnt audio_label_9e95
        pushi 439
        push1
        pTos audioDesired
        pToa musicOwner
        send 6
        audio_label_9e95: ldi 1
        ret
    )
)

; Original Main method 0x9e98
(method (musicStopOwner)
    (asm
        pTos musicOwnerKind
        ldi 2
        eq?
        bnt audio_label_9ea7
        pushi 502
        push0
        pToa musicOwner
        send 4
        audio_label_9ea7: pTos musicOwnerKind
        ldi 1
        eq?
        bnt audio_label_9ecb
        pushi 3
        pushi 14
        lofss credits
        push0
        callk DoSound, 6
        push2
        pushi 9
        lofss credits
        callk DoSound, 4
        push2
        pushi 7
        lofss credits
        callk DoSound, 4
        audio_label_9ecb: ldi 0
        aTop musicOwnerKind
        ldi 0
        aTop audioCreditsHeld
        ldi 0
        aTop musicChooserKind
        ldi 1
        ret
    )
)

; Original Main method 0x9edb
(method (musicSelectOwner)
    (asm
        pToa audioReady
        not
        bnt audio_label_9ee4
        ldi 0
        ret
        audio_label_9ee4: pToa opening
        bnt audio_label_9eef
        pTos musicOwnerKind
        ldi 1
        eq?
        bt audio_label_9efb
        audio_label_9eef: pToa opening
        not
        bnt audio_label_9efe
        pTos musicOwnerKind
        ldi 2
        eq?
        bnt audio_label_9efe
        audio_label_9efb: ldi 1
        ret
        audio_label_9efe: pushi 701
        push0
        self 4
        ldi 0
        aTop audioPending
        ldi 0
        aTop audioDuckTicks
        pToa opening
        aTop audioPhase
        ldi 0
        aTop musicUnavailable
        pToa opening
        bnt audio_label_9f5f
        ldi 1
        aTop musicOwnerKind
        pushi 339
        push1
        push0
        pushi 256
        push1
        push0
        lofsa credits
        send 12
        push2
        pushi 6
        lofss credits
        callk DoSound, 4
        pushi 3
        pushi 8
        lofss credits
        push0
        callk DoSound, 6
        pushi 28
        push0
        self 4
        pushi 3
        pushi 14
        lofss credits
        pToa musicMuted
        bnt audio_label_9f56
        ldi 0
        jmp audio_label_9f59
        audio_label_9f56: pToa masterVolume
        audio_label_9f59: push
        callk DoSound, 6
        jmp audio_label_9f8a
        audio_label_9f5f: pToa musicOwner
        not
        bnt audio_label_9f6b
        ldi 1
        aTop musicUnavailable
        ldi 0
        ret
        audio_label_9f6b: ldi 2
        aTop musicOwnerKind
        pushi 698
        push0
        self 4
        pushi 501
        push2
        lofss bed
        pTos audioDesired
        pToa musicOwner
        send 8
        not
        bnt audio_label_9f8a
        ldi 1
        aTop musicUnavailable
        audio_label_9f8a: pushi 52
        push1
        pToa opening
        bnt audio_label_9f96
        lofsa "credits owner"
        jmp audio_label_9f99
        audio_label_9f96: lofsa "world owner"
        audio_label_9f99: push
        self 6
        pToa musicUnavailable
        bnt audio_label_9fa4
        ldi 0
        jmp audio_label_9fa6
        audio_label_9fa4: ldi 1
        audio_label_9fa6: ret
    )
)

; Original Main method 0x9fa7
(method (musicBeforeChooser)
    (asm
        pToa audioReady
        not
        bt audio_label_9fb1
        pToa musicChooserKind
        bnt audio_label_9fb4
        audio_label_9fb1: ldi 0
        ret
        audio_label_9fb4: pushi 259
        push0
        self 4
        pushi 700
        push0
        self 4
        pushi 28
        push0
        self 4
        pTos musicOwnerKind
        ldi 2
        eq?
        bnt audio_label_9ff0
        pushi 698
        push0
        self 4
        pushi 674
        push0
        pToa musicOwner
        send 4
        not
        bnt audio_label_9fe9
        ldi 1
        aTop musicUnavailable
        ldi 1
        aTop dirty
        ldi 0
        ret
        audio_label_9fe9: ldi 2
        aTop musicChooserKind
        ldi 1
        ret
        audio_label_9ff0: pTos musicOwnerKind
        ldi 1
        eq?
        bnt audio_label_a01e
        pushi 3
        pushi 14
        lofss credits
        push0
        callk DoSound, 6
        pToa audioCreditsHeld
        bnt audio_label_a017
        pushi 3
        pushi 10
        lofss credits
        push0
        callk DoSound, 6
        ldi 0
        aTop audioCreditsHeld
        audio_label_a017: ldi 1
        aTop musicChooserKind
        ldi 1
        ret
        audio_label_a01e: ldi 1
        aTop musicUnavailable
        ldi 1
        aTop dirty
        ldi 0
        ret
    )
)

; Original Main method 0xa02a
(method (musicAfterChooser)
    (asm
        link 1
        pToa musicChooserKind
        sat 0
        ldi 0
        aTop musicChooserKind
        lst 0
        ldi 2
        eq?
        bnt audio_label_a053
        pushi 671
        push0
        pToa musicOwner
        send 4
        not
        bnt audio_label_a04a
        ldi 1
        aTop musicUnavailable
        audio_label_a04a: pushi 698
        push0
        self 4
        ldi 1
        ret
        audio_label_a053: lst 0
        ldi 1
        eq?
        bnt audio_label_a078
        pushi 28
        push0
        self 4
        pushi 3
        pushi 14
        lofss credits
        pToa musicMuted
        bnt audio_label_a06e
        ldi 0
        jmp audio_label_a071
        audio_label_a06e: pToa masterVolume
        audio_label_a071: push
        callk DoSound, 6
        ldi 1
        ret
        audio_label_a078: ldi 0
        ret
    )
)

; Original Main method 0xa07b
(method (musicRetry)
    (asm
        pTos musicOwnerKind
        ldi 2
        eq?
        bnt audio_label_a097
        pToa musicUnavailable
        bnt audio_label_a097
        pushi 442
        push0
        pToa musicOwner
        send 4
        ldi 0
        aTop musicUnavailable
        ldi 1
        aTop dirty
        audio_label_a097: ret
    )
)

)
(class Sound
    (properties
        number 1
        loop -1
        priority 100
        vol 0
        nodePtr 0
        handle 0
        signal 0
        dataInc 0
        min 0
        sec 0
        frame 0
        flags 0
    )
)
(instance cakood of Game)
(instance bed of Sound
    (properties
        number 102
        loop -1
        priority 100
        vol 0
        nodePtr 0
        handle 0
        signal 0
        dataInc 0
        min 0
        sec 0
        frame 0
        flags 0
    )
)
(instance credits of Sound
    (properties
        number 3
        loop 1
        priority 105
        vol 0
        nodePtr 0
        handle 0
        signal 0
        dataInc 0
        min 0
        sec 0
        frame 0
        flags 0
    )
)
