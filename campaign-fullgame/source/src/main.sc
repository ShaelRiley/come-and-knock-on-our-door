;;; Sierra Script 1.0 - (do not remove this comment)
; Reconstructed from exact delivered DoorFix module0 instructions and heap.
; Editable symbolic SCI assembly. Original high-level source is not claimed.
(script# 0)
(public cakood 0)
(local
    [globals 100] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0
    ]
    [uiItems 64] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiActions 64] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiPayloads 64] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiTops 64] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiLefts 64] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiBottoms 64] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiRights 64] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiLabels 64] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiChoiceIds 32] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiChoiceLabels 32] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiChoiceSelected 32] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiChoiceEnabled 32] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiSentence 128] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiInline 400] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiReadBuffer 400] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [uiMeasure 4] = [
        0 0 0 0
    ]
    [p02Slots 64] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [p02Reserved 33] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0
    ]
    [bridgeQueue 32] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]
    [bridgeVisited 64] = [
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ]

[h11MainRead 1]
)
(define V_WALK 0)
(define V_GIVE 1)
(define V_OPEN 2)
(define V_CLOSE 3)
(define V_PICK 4)
(define V_LOOK 5)
(define V_TALK 6)
(define V_USE 7)
(define V_PUSH 8)
(define V_PULL 9)
(define O_DOOR 1)
(define O_BUNNY 2)
(define O_BENCH 3)
(define O_WEDGE 4)
(define O_TRAY 5)
(define O_PACKET 6)
(define O_BOARD 7)
(define O_FRANKIE 8)
(define O_EDGE 9)
(define O_AUDIENCE 10)
(define O_RETURN 11)
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
    
        p04 0 p04Invalid 0 p04HostError 0 p04LastStatus 0
        p05 0
    
p06 0

p07 0

p08 0

p09 0
)

    ; Delivered offset0x0536; 39 original instructions
    (method (syncAudio)
        (asm
            pTos location
            ldi 0
            eq?
            bnt L_0541
            ldi 0
            jmp L_0543
            L_0541: ldi 1
            L_0543: aTop audioRoom
            pToa onApron
            aTop audioApron
            pToa opening
            bnt L_0553
            ldi 2
            jmp L_0555
            L_0553: ldi 0
            L_0555: aTop audioMusic
            pToa onApron
            bnt L_0560
            ldi 1
            jmp L_0562
            L_0560: ldi 0
            L_0562: aTop audioDesired
            pToa opening
            bnt L_0575
            pToa creditHeld
            bnt L_0571
            ldi 1
            jmp L_0573
            L_0571: ldi 0
            L_0573: jmp L_0583
            L_0575: pToa paused
            bt L_057d
            pToa menuOpen
            bnt L_0581
            L_057d: ldi 1
            jmp L_0583
            L_0581: ldi 0
            L_0583: aTop audioHold
            ret
        )
    )

    ; Delivered offset0x0587; 25 original instructions
    (method (audioEvent arg1)
        (asm
            lap 1
            aTop audioLastEvent
            ipToa audioSerial
            lsp 1
            ldi 4
            eq?
            bt L_059d
            lsp 1
            ldi 5
            eq?
            bnt L_05b6
            L_059d: pToa audienceMuted
            not
            bnt L_05b6
            pTos audioPending
            lsp 1
            ldi 4
            eq?
            bnt L_05b0
            ldi 2
            jmp L_05b2
            L_05b0: ldi 4
            L_05b2: or
            aTop audioPending
            L_05b6: ret
        )
    )

    ; Delivered offset0x05b7; 7 original instructions
    (method (takeAudio &tmp pending)
        ; The transport drains/coalesces this queue exactly once each live turn.
        (= pending audioPending)
        (= audioPending 0)
        (return pending)
    )

    ; Delivered offset0x05c6; 169 original instructions
    (method (audioTrace arg1 &tmp t0 t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13 t14 t15 t16 t17 t18 t19 t20 t21 t22 t23 t24 t25 t26 t27 t28 t29 t30 t31 t32 t33 t34 t35 t36 t37 t38 t39 t40 t41 t42 t43 t44 t45 t46 t47 t48 t49 t50 t51 t52 t53 t54 t55 t56 t57 t58 t59 t60 t61 t62 t63 t64 t65 t66 t67 t68 t69 t70 t71 t72 t73 t74 t75 t76 t77 t78 t79 t80 t81 t82 t83 t84 t85 t86 t87 t88 t89 t90 t91 t92 t93 t94 t95 t96 t97 t98 t99 t100 t101 t102 t103 t104 t105 t106 t107 t108 t109 t110 t111 t112 t113 t114 t115 t116 t117 t118 t119 t120 t121 t122 t123 t124 t125 t126 t127 t128 t129 t130 t131 t132 t133 t134 t135 t136 t137 t138 t139 t140 t141 t142 t143 t144 t145 t146 t147 t148 t149 t150 t151 t152 t153 t154 t155 t156 t157 t158 t159 t160 t161 t162 t163 t164 t165 t166 t167 t168 t169 t170 t171 t172 t173 t174 t175 t176 t177 t178 t179 t180 t181 t182 t183 t184 t185 t186 t187 t188 t189 t190 t191 t192 t193 t194 t195 t196 t197 t198 t199 t200 t201 t202 t203 t204 t205 t206 t207 t208 t209 t210 t211 t212 t213 t214 t215 t216 t217 t218 t219 t220 t221 t222 t223 t224 t225 t226 t227 t228 t229 t230 t231 t232 t233 t234 t235 t236 t237 t238 t239 t240 t241 t242 t243 t244 t245 t246 t247 t248 t249 t250 t251 t252 t253 t254 t255 t256 t257 t258 t259 t260 t261 t262 t263 t264 t265 t266 t267 t268 t269 t270 t271 t272 t273 t274 t275 t276 t277 t278 t279 t280 t281 t282 t283 t284 t285 t286 t287 t288 t289 t290 t291 t292 t293 t294 t295 t296 t297 t298 t299 t300 t301 t302 t303 t304 t305 t306 t307 t308 t309 t310 t311 t312 t313 t314 t315 t316 t317 t318 t319 t320 t321 t322 t323 t324 t325 t326 t327 t328 t329 t330 t331 t332 t333 t334 t335 t336 t337 t338 t339 t340 t341 t342 t343 t344 t345 t346 t347 t348)
        (asm
            pToa audioReady
            not
            bt L_05d4
            pToa musicOwner
            not
            bnt L_05d7
            L_05d4: ldi 0
            ret
            L_05d7: pushi 3
            lea t0
            push
            lofss "p01audio%04d.csv"
            pTos audioLogIndex
            callk Format, 6
            L_05e6: push2
            pushi 10
            lea t0
            push
            callk FileIO, 4
            bnt L_0606
            ipToa audioLogIndex
            pushi 3
            lea t0
            push
            lofss "p01audio%04d.csv"
            pTos audioLogIndex
            callk Format, 6
            jmp L_05e6
            L_0606: pushi 40
            lea t28
            push
            lofss "%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n"
            lsp 1
            push0
            callk GetTime, 0
            push
            pushi 420
            push0
            pToa musicOwner
            send 4
            push
            pTos audioDesired
            pushi 504
            push0
            pToa musicOwner
            send 4
            push
            pTos musicOwnerKind
            pTos musicMuted
            pTos audienceMuted
            pTos masterVolume
            pTos audienceVolume
            pTos audioTarget
            pTos audioHold
            pTos opening
            pTos creditCard
            pTos creditElapsed
            pTos audioDuckTicks
            pTos audioPending
            pTos audioSaveResult
            pTos paused
            pTos menuOpen
            pTos creditHeld
            pTos musicUnavailable
            pushi 421
            push0
            pToa musicOwner
            send 4
            push
            pushi 708
            push0
            pToa musicOwner
            send 4
            push
            pushi 443
            push0
            pToa musicOwner
            send 4
            push
            pushi 712
            push0
            pToa musicOwner
            send 4
            push
            pushi 676
            push0
            pToa musicOwner
            send 4
            push
            pushi 709
            push0
            pToa musicOwner
            send 4
            push
            pushi 711
            push0
            pToa musicOwner
            send 4
            push
            pushi 438
            push0
            pToa musicOwner
            send 4
            push
            pushi 681
            push0
            pToa musicOwner
            send 4
            push
            pushi 506
            push0
            pToa musicOwner
            send 4
            push
            pushi 423
            push0
            pToa musicOwner
            send 4
            push
            pushi 500
            push0
            pToa musicOwner
            send 4
            push
            pushi 435
            push0
            pToa musicOwner
            send 4
            push
            pushi 682
            push0
            pToa musicOwner
            send 4
            push
            pushi 153
            push0
            pToa musicOwner
            send 4
            push
            pushi 402
            push0
            pToa musicOwner
            send 4
            push
            callk Format, 80
            pushi 3
            push0
            lea t0
            push
            push2
            callk FileIO, 6
            sat 348
            lst 348
            ldi -1
            ne?
            bnt L_0714
            pushi 3
            pushi 6
            lst 348
            lea t28
            push
            callk FileIO, 6
            push2
            push1
            lst 348
            callk FileIO, 4
            L_0714: ipToa audioLogIndex
            ret
        )
    )

    ; Delivered offset0x0718; 54 original instructions
    (method (audioHolds &tmp t0)
        (asm
            pTos musicOwnerKind
            ldi 2
            eq?
            bnt L_0738
            pushi 734
            push1
            pToa paused
            bt L_072d
            pToa menuOpen
            bnt L_0731
            L_072d: ldi 1
            jmp L_0733
            L_0731: ldi 0
            L_0733: push
            pToa musicOwner
            send 6
            L_0738: pTos musicOwnerKind
            ldi 1
            eq?
            bnt L_0747
            pToa creditHeld
            bnt L_0747
            ldi 1
            jmp L_0749
            L_0747: ldi 0
            L_0749: sat 0
            lst 0
            pToa audioCreditsHeld
            ne?
            bnt L_076b
            pTos musicOwnerKind
            ldi 1
            eq?
            bnt L_0766
            pushi 3
            pushi 10
            lofss credits
            lst 0
            callk DoSound, 6
            L_0766: lat 0
            aTop audioCreditsHeld
            L_076b: pTos audioHold
            pToa audioPCMheld
            ne?
            bnt L_0785
            pToa audioHold
            bnt L_077f
            pushi 377
            push0
            self 4
            L_077f: pToa audioHold
            aTop audioPCMheld
            L_0785: ret
        )
    )

    ; Delivered offset0x0786; 174 original instructions
    (method (audioPoll arg1 &tmp t0 t1 t2)
(if (and p05 (p05 hFailure?)) (return 0)) 

        (asm
            pToa audioReady
            not
            bnt L_0791
            ldi 0
            ret
            L_0791: lsp 1
            ldi 0
            lt?
            bnt L_079c
            ldi 0
            sap 1
            L_079c: lsp 1
            ldi 12
            gt?
            bnt L_07a7
            ldi 12
            sap 1
            L_07a7: pushi 700
            push0
            self 4
            pushi 28
            push0
            self 4
            pToa audioHold
            not
            bnt L_07d6
            pTos audioDuckTicks
            ldi 0
            gt?
            bnt L_07d6
            pTos audioDuckTicks
            lap 1
            sub
            aTop audioDuckTicks
            pTos audioDuckTicks
            ldi 0
            lt?
            bnt L_07d6
            ldi 0
            aTop audioDuckTicks
            L_07d6: pTos masterVolume
            pToa audioDuckTicks
            bnt L_07e2
            ldi 60
            jmp L_07e4
            L_07e2: ldi 100
            L_07e4: mul
            push
            ldi 100
            div
            aTop audioTarget
            pToa audienceMuted
            bnt L_07f4
            ldi 0
            jmp L_07ff
            L_07f4: pTos masterVolume
            pToa audienceVolume
            mul
            push
            ldi 100
            div
            L_07ff: sat 1
            lst 1
            pToa audioLastPCM
            ne?
            bnt L_0836
            pToa presentation
            bnt L_0828
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
            L_0828: lat 1
            aTop audioLastPCM
            pToa audienceMuted
            bnt L_0836
            ldi 0
            aTop audioPending
            L_0836: pTos musicOwnerKind
            ldi 1
            eq?
            bnt L_0855
            pushi 3
            pushi 14
            lofss credits
            pToa musicMuted
            bnt L_084c
            ldi 0
            jmp L_084f
            L_084c: pToa masterVolume
            L_084f: push
            callk DoSound, 6
            jmp L_0888
            L_0855: pTos musicOwnerKind
            ldi 2
            eq?
            bnt L_0888
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
            bt L_087e
            pushi 421
            push0
            pToa musicOwner
            send 4
            not
            bnt L_0884
            L_087e: ldi 1
            aTop musicUnavailable
            jmp L_0888
            L_0884: ldi 0
            aTop musicUnavailable
            L_0888: pushi 260
            push0
            self 4
            sat 0
            pToa opening
            not
            bnt L_08d5
            pToa audioHold
            not
            bnt L_08d5
            lst 0
            ldi 2
            and
            bnt L_08d5
            pToa audienceMuted
            not
            bnt L_08d5
            pToa presentation
            bnt L_08cd
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
            L_08cd: pushi 52
            push1
            lofss "real audience request"
            self 6
            L_08d5: ret
        )
    )

    ; Delivered offset0x08d6; 17 original instructions
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

    ; Delivered offset0x08f8; 77 original instructions
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
            bnt L_095a
            pTos musicOwnerKind
            ldi 1
            ne?
            bt L_092d
            pTos musicChooserKind
            ldi 1
            ne?
            bnt L_0934
            L_092d: ldi 1
            aTop musicUnavailable
            ldi 0
            ret
            L_0934: ldi 0
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
            bnt L_0951
            ldi 0
            jmp L_0954
            L_0951: pToa masterVolume
            L_0954: push
            callk DoSound, 6
            jmp L_0988
            L_095a: pTos musicOwnerKind
            ldi 2
            ne?
            bt L_0968
            pTos musicChooserKind
            ldi 2
            ne?
            bnt L_096f
            L_0968: ldi 1
            aTop musicUnavailable
            ldi 0
            ret
            L_096f: ldi 0
            aTop musicChooserKind
            pushi 670
            push0
            pToa musicOwner
            send 4
            not
            bnt L_0982
            ldi 1
            aTop musicUnavailable
            L_0982: pushi 698
            push0
            self 4
            L_0988: pushi 52
            push1
            lofss "replay owner restored"
            self 6
            ret
        )
    )

    ; Delivered offset0x0991; 13 original instructions
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

    ; Delivered offset0x09ab; 15 original instructions
    (method (say arg1)
        (asm
            ldi 0
            aTop navNotice
            ldi 0
            aTop navNoticeTicks
            pToa presentation
            bnt L_09bf
            pushi 376
            push1
            lsp 1
            self 6
            L_09bf: lap 1
            aTop currentCaption
            ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x09c9; 51 original instructions
    (method (initWorld)
        ; Entry guard is shared by full-watch and skip. Replay never calls it.
        (if initialized (return 0))
        (= initialized 1) (++ initCount)
        (= location 0) (= onApron 0) (= tray 0) (= wedge 0)
        (= doorOpen 0) (= bunnyReady 0) (= traySafe 0) (= houseEntered 0)
        (= p01Consumed 0) (= a01Consumed 0) (= greetingConsumed 0)
        (= hintLevel 0) (= jackLeft 128) (= jackTarget 128) (= jackPose 0)
        (self uiCancelSentence:) (self p02Init:) (self p02HostInventory:) (self say: 1)
    )

    ; Delivered offset0x0a34; 29 original instructions
    (method (finishOpening)
        (asm
            pToa opening
            not
            bnt L_0a3c
            ldi 0
            ret
            L_0a3c: pushi 377
            push0
            self 4
            ldi 0
            aTop opening
            ldi 0
            aTop creditHeld
            pToa replayOpening
            bnt L_0a56
            ldi 0
            aTop replayOpening
            jmp L_0a5b
            L_0a56: pushi 116
            push0
            self 4
            L_0a5b: pushi 259
            push0
            self 4
            pushi 700
            push0
            self 4
            ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x0a6d; 35 original instructions
    (method (startReplay)
((ScriptID 993 0) h11PayDrop:)

(if (and p08 (p08 h8ActionBarrier:)) (return 0))

(if (and p05 (p05 hBarrier:)) (return 0))

        (asm
            ldi 0
            aTop navNotice
            ldi 0
            aTop navNoticeTicks
            pushi 377
            push0
            self 4
            pToa opening
            bnt L_0a82
            ldi 0
            ret
            L_0a82: ldi 1
            aTop replayOpening
            ldi 1
            aTop opening
            ldi 0
            aTop creditCard
            ldi 0
            aTop creditElapsed
            ldi 0
            aTop creditHeld
            ldi 0
            aTop audioPending
            push0
            callk GetTime, 0
            aTop lastTick
            pushi 259
            push0
            self 4
            pushi 700
            push0
            self 4
            ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x0ab6; 13 original instructions
    (method (nextCard)
        (++ creditCard) (= creditElapsed 0)
        (if (>= creditCard 10) (self finishOpening:))
        (= dirty 1)
    )

    ; Delivered offset0x0acf; 180 original instructions
    (method (walk obj &tmp returning)
        (if (and (== obj O_RETURN) onApron)
            (= onApron 0) (= jackLeft returnLeft) (= jackTarget jackLeft)
            (= jackPose 0) (self syncAudio:) (self say: 39) (return 0))
        (if (and (== obj O_EDGE) (not onApron))
            (= returnLeft jackLeft) (= onApron 1) (= jackTarget jackLeft)
            (= jackPose 0) (self syncAudio:) (self say: 38) (return 0))
        (if onApron (self say: 42) (return 0))
        (if (== obj O_DOOR)
            (if (== location 1)
                (= location 0) (= doorOpen (== wedge 2))
                (= jackLeft 128) (= jackTarget 128) (= jackPose 0)
                (= audioPending 0) (self syncAudio:) (self say: 37) (return 0))
            (if (not doorOpen) (self say: 33) (return 0))
            (if (and (== tray 0) (!= wedge 2))
                (= doorOpen 0) (self say: 34) (return 0))
            (if (== tray 1) (self say: 35) (return 0))
            (= returning houseEntered)
            (= location 1) (= tray 2) (= traySafe 1) (= houseEntered 1)
            (= doorOpen (== wedge 2)) (= jackLeft 81) (= jackTarget 81) (= jackPose 0)
            (= audioPending 0) (self syncAudio:)
            (if (not p01Consumed) (= p01Consumed 1) (self audioEvent: 3))
            ; Preserve the production arrival only on genuine first entry.
            ; Later arrivals reuse the existing silent room navigation notice.
            (if returning (self speechCancel:) (self navNoticeSet: 134 1)
            else (self say: 36)) (return 0))
        (= jackTarget (- x 12))
        (if (< jackTarget 8) (= jackTarget 8))
        (if (> jackTarget 260) (= jackTarget 260))
        (self say: 52)
    )

    ; Delivered offset0x0c3a; 533 original instructions
    (method (act action obj target)
        (if (or (self p04Reserved: obj) (self p04Reserved: target)) (return 0))
        (if (== action V_WALK) (self walk: obj) (return 0))
        ; Permanent return works even with Use/Give waiting for a second noun.
        (if (and (== obj O_RETURN) onApron) (self walk: obj) (return 0))
        (if onApron
            (if (and (== obj O_AUDIENCE) (== action V_TALK))
                (self say: 40)
                (if (not greetingConsumed) (= greetingConsumed 1) (self audioEvent: 5))
                (return 0))
            (if (and (== obj O_AUDIENCE) (== action V_LOOK))
                (self say: 41) (return 0))
            (self say: 42) (return 0))
        (if (and (== location 1) (or (== obj O_BUNNY) (== obj O_BENCH)))
            (self say: 55) (return 0))
        (if (== action V_LOOK)
            (switch obj
                (O_TRAY (self say: 2)) (O_BENCH (self say: 3))
                (O_DOOR (self say: 4)) (O_WEDGE (self say: 5))
                (O_BUNNY (self say: 6)) (O_PACKET (self say: 7))
                (O_BOARD (self say: 8)) (O_FRANKIE (self say: 44))
                (O_EDGE (self say: 38)) (else (self say: 56)))
            (return 0))
        (if (and (== action V_TALK) (== obj O_BUNNY))
            (if bunnyReady (self say: (if (== tray 2) 11 else 10))
            else (= bunnyReady 1) (self say: 9))
            (= audioDialogue 1) (= audioDuckTicks 120) (return 0))
        (if (and (== action V_TALK) (== obj O_FRANKIE))
            (= audioDialogue 1) (= audioDuckTicks 120) (self say: 43) (return 0))
        (if (and (== action V_GIVE) (== obj O_TRAY) (== target O_BUNNY) (== location 0))
            (if (!= tray 0) (self say: 14) (return 0))
            (if (not bunnyReady) (self say: 12) (return 0))
            (= tray 2) (= traySafe 1)
            (if (not a01Consumed) (= a01Consumed 1) (self audioEvent: 4))
            (self say: 13) (return 0))
        (if (and (== action V_USE) (== obj O_TRAY) (== target O_BENCH) (== location 0))
            (if (!= tray 0) (self say: 14) (return 0))
            (= tray 1) (self say: 15) (return 0))
        (if (and (== action V_PICK) (== obj O_TRAY) (== location 0))
            (if (!= tray 1) (self say: 17) (return 0))
            (= tray 0) (if (!= wedge 2) (= doorOpen 0))
            (self say: 16) (return 0))
        (if (and (== action V_PICK) (== obj O_WEDGE))
            (if (== wedge 1) (self say: 19) (return 0))
            (if (and (== location 1) (!= wedge 2)) (self say: 20) (return 0))
            (= wedge 1) (= doorOpen 0) (self say: 18) (return 0))
        (if (and (== action V_OPEN) (== obj O_DOOR))
            (if doorOpen (self say: 22) (return 0))
            (= doorOpen 1) (self say: 21) (return 0))
        (if (and (== action V_CLOSE) (== obj O_DOOR))
            (if (== wedge 2) (self say: 24) (return 0))
            (if (not doorOpen) (self say: 25) (return 0))
            (= doorOpen 0) (self say: 23) (return 0))
        (if (and (== action V_USE) (== obj O_WEDGE) (== target O_DOOR))
            (if (== wedge 2) (self say: 30) (return 0))
            (if (== wedge 0) (self say: 27) (return 0))
            (if (not doorOpen) (self say: 28) (return 0))
            (if (== tray 0) (self say: 29) (return 0))
            (= wedge 2) (self say: 26) (return 0))
        (if (and (== obj O_TRAY) (== target O_DOOR)) (self say: 31) (return 0))
        (self say: 32)
    )

    ; Delivered offset0x0fff; 521 original instructions
    (method (render &tmp t0 t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13 t14 t15 t16 t17 t18 t19 t20 t21 t22 t23 t24 t25 t26 t27 t28 t29 t30 t31 t32 t33 t34 t35 t36 t37 t38 t39 t40 t41 t42 t43 t44 t45 t46 t47 t48 t49 t50 t51 t52 t53 t54 t55 t56 t57 t58 t59 t60 t61 t62 t63 t64 t65 t66 t67 t68 t69 t70 t71 t72 t73 t74 t75 t76 t77 t78 t79 t80 t81 t82 t83 t84 t85 t86 t87 t88 t89 t90 t91 t92 t93 t94 t95 t96 t97 t98 t99 t100)
((ScriptID 996 0) h14MenuFrame: 0)
((ScriptID 996 0) h14Frame: 0)

((ScriptID 995 0) h13Frame: 0)

((ScriptID 994 0) h12Frame: 0)

(if (!= self (ScriptID 0 0)) (return 0))
(if [h11MainRead 0] ((ScriptID 993 0) h11ReadBegin:) (return 0))
(= [h11MainRead 0] 1)
(if (not ((ScriptID 993 0) h11ReadBegin:)) (= [h11MainRead 0] 0) (return 0))

((ScriptID 993 0) h11OwnerFrame: 0)
((ScriptID 993 0) h11Frame: 0)

((ScriptID 992 0) h10Frame: 0)

(if (and p08 (p08 h8VF: 0)) (= dirty 0)
 ((ScriptID 993 0) h11ReadEnd:) ((ScriptID 993 0) h11ReadFinish:) (= [h11MainRead 0] 0) (return 0))

(if p08 (p08 h8ReaderFrame: 0))
(if p09 (p09 h9Frame: 0))
(if (not ((ScriptID 993 0) h11ReadResume:))
 ((ScriptID 993 0) h11ReadEnd:) ((ScriptID 993 0) h11ReadFinish:) (= [h11MainRead 0] 0) (return 0))

        (asm
            pushi 6
            push0
            push0
            pushi 200
            pushi 320
            push0
            push0
            callk SetPort, 12
            pushi 3
            push1
            pushi 999
            push2
            callk Palette, 6
            pushi 9
            pushi 11
            push0
            push0
            pushi 200
            pushi 320
            push1
            push0
            push0
            push0
            callk Graph, 18
            pToa opening
            bnt L_10c7
            pushi 7
            pushi 104
            pTos creditCard
            ldi 8
            gt?
            bnt L_1041
            ldi 0
            jmp L_1043
            L_1041: pToa creditCard
            L_1043: add
            push
            push0
            push0
            push0
            push0
            pushi -1
            push0
            callk DrawCel, 14
            pushi 11
            lofss "STATIC CREDIT PROTOTYPE / 60 SECONDS"
            pushi 100
            pushi 5
            pushi 145
            pushi 102
            push2
            pushi 105
            push0
            pushi 106
            pushi 310
            pushi 121
            callk Display, 22
            pushi 11
            lofss "X SKIP N NEXT H HOLD F2/F3 SAVE/LOAD"
            pushi 100
            pushi 5
            pushi 160
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 310
            pushi 121
            callk Display, 22
            pushi 4
            lea t1
            push
            lofss "CARD %d/10 %s"
            pTos creditCard
            ldi 1
            add
            push
            pToa creditHeld
            bnt L_109f
            lofsa "HELD"
            jmp L_10a2
            L_109f: lofsa "AUTO"
            L_10a2: push
            callk Format, 8
            pushi 11
            lea t1
            push
            pushi 100
            pushi 5
            pushi 176
            pushi 102
            pushi 13
            pushi 105
            push0
            pushi 106
            pushi 310
            pushi 121
            callk Display, 22
            jmp L_13fd
            L_10c7: pushi 100
            push0
            self 4
            pushi 9
            pushi 11
            push0
            push0
            pToa currentCaption
            bt L_10ea
            pToa navNoticeTicks
            bt L_10ea
            pushi 585
            push0
            self 4
            bnt L_10ee
            pTos uiPanel
            ldi 0
            eq?
            bnt L_10ee
            L_10ea: ldi 43
            jmp L_10f0
            L_10ee: ldi 11
            L_10f0: push
            pushi 320
            push1
            push0
            push0
            push0
            callk Graph, 18
            pushi 11
            pushi 252
            push0
            self 4
            push
            pushi 100
            pushi 5
            push1
            pushi 102
            push2
            pushi 105
            push0
            pushi 106
            pushi 154
            pushi 121
            callk Display, 22
            pushi 247
            push0
            self 4
            pushi 585
            push0
            self 4
            bnt L_1165
            pTos currentCaption
            ldi 0
            eq?
            bnt L_1165
            pTos navNoticeTicks
            ldi 0
            eq?
            bnt L_1165
            pTos uiPanel
            ldi 0
            eq?
            bnt L_1165
            pushi 8
            lofss "RITA'S PREPARATION COMPLETE."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "YOU CAN CONTINUE EXPLORING."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            L_1165: pushi 11
            lofss "NOTES"
            pushi 100
            pushi 162
            push2
            pushi 102
            pushi 13
            pushi 105
            push0
            pushi 106
            pushi 47
            pushi 121
            callk Display, 22
            pushi 332
            push0
            self 4
            pToa paused
            bt L_118f
            pToa menuOpen
            bnt L_13fd
            L_118f: pushi 9
            pushi 11
            pushi 48
            pushi 18
            pushi 162
            pushi 302
            push1
            push0
            push0
            push0
            callk Graph, 18
            pushi 294
            pushi 5
            pushi 48
            pushi 18
            pushi 162
            pushi 302
            push1
            self 14
            pushi 11
            lofss "PAUSED / COME AND KNOCK"
            pushi 100
            pushi 30
            pushi 54
            pushi 102
            push2
            pushi 105
            push0
            pushi 106
            pushi 260
            pushi 121
            callk Display, 22
            pushi 11
            lofss "1 SAVE 2 LOAD 3 REPLAY OPENING"
            pushi 100
            pushi 30
            pushi 69
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 260
            pushi 121
            callk Display, 22
            pushi 11
            lofss "4 RESUME 5 QUIT 6 AUDIENCE ON/OFF"
            pushi 100
            pushi 30
            pushi 83
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 260
            pushi 121
            callk Display, 22
            pushi 11
            lofss "Y MUSIC ON/OFF +/- GAME VOLUME"
            pushi 100
            pushi 30
            pushi 98
            pushi 102
            pushi 13
            pushi 105
            push0
            pushi 106
            pushi 260
            pushi 121
            callk Display, 22
            pushi 11
            lofss "STOCK F2/F3 SAVE/LOAD IN ANY MODE"
            pushi 100
            pushi 30
            pushi 112
            pushi 102
            pushi 13
            pushi 105
            push0
            pushi 106
            pushi 260
            pushi 121
            callk Display, 22
            pToa presentation
            bnt L_13fd
            pushi 294
            pushi 5
            pushi 123
            pushi 30
            pushi 138
            pushi 150
            push1
            self 14
            pushi 294
            pushi 5
            pushi 123
            pushi 162
            pushi 138
            pushi 187
            push1
            self 14
            pushi 294
            pushi 5
            pushi 123
            pushi 212
            pushi 138
            pushi 237
            push1
            self 14
            pushi 3
            lea t1
            push
            lofss "V VOICE: %s"
            pushi 391
            push0
            pToa presentation
            send 4
            bnt L_1294
            lofsa "OFF"
            jmp L_1297
            L_1294: lofsa "ON"
            L_1297: push
            callk Format, 6
            pushi 11
            lea t1
            push
            pushi 100
            pushi 34
            pushi 126
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 110
            pushi 121
            callk Display, 22
            pushi 11
            lofss "-"
            pushi 100
            pushi 171
            pushi 126
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 8
            pushi 121
            callk Display, 22
            pushi 3
            lea t1
            push
            lofss "%d"
            pushi 394
            push0
            pToa presentation
            send 4
            push
            callk Format, 6
            pushi 11
            lea t1
            push
            pushi 100
            pushi 190
            pushi 126
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 20
            pushi 121
            callk Display, 22
            pushi 11
            lofss "+"
            pushi 100
            pushi 221
            pushi 126
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 8
            pushi 121
            callk Display, 22
            pushi 294
            pushi 5
            pushi 142
            pushi 30
            pushi 158
            pushi 150
            push1
            self 14
            pushi 294
            pushi 5
            pushi 142
            pushi 162
            pushi 158
            pushi 187
            push1
            self 14
            pushi 294
            pushi 5
            pushi 142
            pushi 212
            pushi 158
            pushi 237
            push1
            self 14
            pushi 3
            lea t1
            push
            lofss "E EFFECTS: %s"
            pushi 345
            push0
            pToa presentation
            send 4
            bnt L_1370
            lofsa "OFF"
            jmp L_1373
            L_1370: lofsa "ON"
            L_1373: push
            callk Format, 6
            pushi 11
            lea t1
            push
            pushi 100
            pushi 34
            pushi 146
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 110
            pushi 121
            callk Display, 22
            pushi 11
            lofss "-"
            pushi 100
            pushi 171
            pushi 146
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 8
            pushi 121
            callk Display, 22
            pushi 3
            lea t1
            push
            lofss "%d"
            pushi 346
            push0
            pToa presentation
            send 4
            push
            callk Format, 6
            pushi 11
            lea t1
            push
            pushi 100
            pushi 190
            pushi 146
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 20
            pushi 121
            callk Display, 22
            pushi 11
            lofss "+"
            pushi 100
            pushi 221
            pushi 146
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 8
            pushi 121
            callk Display, 22
            L_13fd: pToa musicUnavailable
            bnt L_141e
            pushi 11
            lofss "MUSIC UNAVAILABLE. R TO RETRY."
            pushi 100
            pushi 5
            pushi 190
            pushi 102
            pushi 13
            pushi 105
            push0
            pushi 106
            pushi 310
            pushi 121
            callk Display, 22
            L_141e: pushi #h11ReadEnd
            push0
            push2
            pushi 993
            push0
            callk ScriptID, 4
            send 4
            bnt H11_read_cleanup
            pToa p08
            bnt H8_reader_legacy_flush
            pushi #h8ReaderFrame
            push1
            push1
            pToa p08
            send 6
            jmp H8_reader_flush_done
            H8_reader_legacy_flush: pushi 6
            pushi 12
            push0
            push0
            pushi 200
            pushi 320
            push1
            callk Graph, 12
            H8_reader_flush_done: ldi 0
            aTop dirty
            pushi #h14MenuFrame
            push1
            push1
            push2
            pushi 996
            push0
            callk ScriptID, 4
            send 6
            pushi #h14Frame
            push1
            push1
            push2
            pushi 996
            push0
            callk ScriptID, 4
            send 6
            pushi #h13Frame
            push1
            push1
            push2
            pushi 995
            push0
            callk ScriptID, 4
            send 6
            pushi #h12Frame
            push1
            push1
            push2
            pushi 994
            push0
            callk ScriptID, 4
            send 6
            pushi #h11OwnerFrame
            push1
            push1
            push2
            pushi 993
            push0
            callk ScriptID, 4
            send 6
            pushi #h11Frame
            push1
            push1
            push2
            pushi 993
            push0
            callk ScriptID, 4
            send 6
            
            pushi #h10Frame
            push1
            push1
            push2
            pushi 992
            push0
            callk ScriptID, 4
            send 6
            
            pToa p09
            bnt H9_frame_done
            pushi #h9Frame
            push1
            push1
            pToa p09
            send 6
            H9_frame_done: jmp H11_read_cleanup
            H11_read_cleanup: sat 100
            pushi #h11ReadFinish
            push0
            push2
            pushi 993
            push0
            callk ScriptID, 4
            send 4

        )
    (= [h11MainRead 0] 0) (return t100))

    ; Delivered offset0x1434; 36 original instructions
    (method (writeSave)
(if (not ((ScriptID 996 0) h14Save:)) (return 0))

(if (not ((ScriptID 995 0) h13Save:)) (return 0))

(if (not ((ScriptID 994 0) h12Save:)) (return 0))
((ScriptID 994 0) h12Retire:)

((ScriptID 993 0) h11PayDrop:)

(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)

(if (not ((ScriptID 993 0) h11Save:)) (return 0))
((ScriptID 993 0) h11Retire:)
((ScriptID 993 0) h11OwnerRetire:)

((ScriptID 992 0) h10Retire:)

(if (and p09 (not (p09 h9SaveReady:))) (return 0))
(if (and p08 (not (p08 h8RouteSave:))) (return 0))

(if (and p08 (not (p08 h8SaveReady:))) (return 0))

(if (and p07 (not (p07 h7SaveReady:))) (return 0))

(if (and p06 (not (p06 h6SaveReady:))) (return 0))

(if (and p05 (not (p05 hSaveReady:))) (return 0)) (if p05 (p05 hStageRetire:))

        (if (and p04 (or (p04 qTransaction?) (not (p04 qProject: self)) (not (p04 qValidateLayout:))))
            (= p04HostError 1) (= uiFailure 10) (= dirty 1) (return 0))
        (asm
            pushi 560
            push0
            self 4
            pushi 377
            push0
            self 4
            pushi 693
            push0
            self 4
            not
            bnt L_144c
            ldi 0
            ret
            L_144c: pushi 52
            push1
            lofss "before save owner silent"
            self 6
            pushi 3
            push0
            pushi -1
            push0
            callk SaveGame, 6
            aTop audioSaveResult
            pushi #h14Stored
            push1
            pTos audioSaveResult
            push2
            pushi 996
            push0
            callk ScriptID, 4
            send 6
            pushi #h13Stored
            push1
            pTos audioSaveResult
            push2
            pushi 995
            push0
            callk ScriptID, 4
            send 6
            pushi 692
            push0
            self 4
            pushi 52
            push1
            lofss "after save or cancel"
            self 6
            push0
            callk GetTime, 0
            aTop lastTick
            ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x147b; 31 original instructions
    (method (readSave)
((ScriptID 996 0) h14Retire:)

((ScriptID 995 0) h13Retire:)
((ScriptID 995 0) h13Cancel:)

((ScriptID 994 0) h12SuccessorCancel:)

((ScriptID 993 0) h11PayDrop:)

(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)

(if (and p08 (p08 h8S: 8)) (return 0))

(if p08 (p08 h8RouteRetire:))

(if (and p08 (or (p08 h8Critical?) (p08 h8Restoring?))) (return 0)) (if (and p08 (or (p08 h8Failure?) (not (p08 h8RestoreValid?)))) (return (p08 h8Recover:)))

(if (and p07 (p07 h7Critical?)) (return 0))

(if (and p06 (p06 h6Critical?)) (return 0))

(if (and p05 (p05 hCritical?)) (return 0))

        (asm
            pushi 560
            push0
            self 4
            pushi 377
            push0
            self 4
            pushi 693
            push0
            self 4
            not
            bnt L_1493
            ldi 0
            ret
            L_1493: pushi 3
            push0
            pushi -1
            push0
            callk RestoreGame, 6
            pushi 692
            push0
            self 4
            pushi 52
            push1
            lofss "restore cancel or failure"
            self 6
            push0
            callk GetTime, 0
            aTop lastTick
            ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x14b7; 667 original instructions
    (method (input &tmp t0 t1)
(if ((ScriptID 996 0) h14Input:) (return 0))

(if (and p08 (p08 h8RouteInput:)) (return 0))

        (asm
            pTos type
            ldi 1
            eq?
            bnt L_1529
            pToa presentation
            bnt L_1529
            pToa menuOpen
            bt L_14cc
            pToa paused
            bnt L_1529
            L_14cc: pToa opening
            not
            bnt L_1529
            pTos y
            ldi 142
            ge?
            bnt L_1529
            pTos y
            ldi 159
            lt?
            bnt L_1529
            pTos x
            ldi 30
            ge?
            bnt L_14f6
            pTos x
            ldi 150
            lt?
            bnt L_14f6
            pushi 557
            push0
            self 4
            L_14f6: pTos x
            ldi 162
            ge?
            bnt L_150e
            pTos x
            ldi 187
            lt?
            bnt L_150e
            pushi 556
            push1
            pushi -10
            self 6
            L_150e: pTos x
            ldi 212
            ge?
            bnt L_1526
            pTos x
            ldi 237
            lt?
            bnt L_1526
            pushi 556
            push1
            pushi 10
            self 6
            L_1526: ldi 0
            ret
            L_1529: pTos type
            ldi 4
            eq?
            bnt L_1544
            pToa presentation
            bnt L_1544
            pTos message
            ldi 101
            eq?
            bnt L_1544
            pushi 557
            push0
            self 4
            ldi 0
            ret
            L_1544: pTos type
            ldi 4
            eq?
            bnt L_1574
            pToa presentation
            bnt L_1574
            pTos message
            ldi 44
            eq?
            bt L_155d
            pTos message
            ldi 46
            eq?
            bnt L_1574
            L_155d: pushi 556
            push1
            pTos message
            ldi 44
            eq?
            bnt L_156c
            ldi -10
            jmp L_156e
            L_156c: ldi 10
            L_156e: push
            self 6
            ldi 0
            ret
            L_1574: pTos type
            ldi 1
            eq?
            bnt L_15df
            pToa menuOpen
            bt L_1583
            pToa paused
            bnt L_15df
            L_1583: pToa opening
            not
            bnt L_15df
            pTos y
            ldi 123
            ge?
            bnt L_15df
            pTos y
            ldi 140
            lt?
            bnt L_15df
            pTos x
            ldi 30
            ge?
            bnt L_15ac
            pTos x
            ldi 150
            lt?
            bnt L_15ac
            pushi 392
            push0
            self 4
            L_15ac: pTos x
            ldi 162
            ge?
            bnt L_15c4
            pTos x
            ldi 187
            lt?
            bnt L_15c4
            pushi 389
            push1
            pushi -10
            self 6
            L_15c4: pTos x
            ldi 212
            ge?
            bnt L_15dc
            pTos x
            ldi 237
            lt?
            bnt L_15dc
            pushi 389
            push1
            pushi 10
            self 6
            L_15dc: ldi 0
            ret
            L_15df: pTos type
            ldi 1
            eq?
            bnt L_1650
            pToa menuOpen
            bt L_15ee
            pToa paused
            bnt L_1650
            L_15ee: pToa opening
            not
            bnt L_1650
            pTos y
            ldi 68
            ge?
            bnt L_1620
            pTos y
            ldi 82
            lt?
            bnt L_1620
            pushi 127
            push1
            pTos x
            ldi 94
            lt?
            bnt L_160f
            ldi 1
            jmp L_161d
            L_160f: pTos x
            ldi 151
            lt?
            bnt L_161b
            ldi 2
            jmp L_161d
            L_161b: ldi 3
            L_161d: push
            self 6
            L_1620: pTos y
            ldi 82
            ge?
            bnt L_164d
            pTos y
            ldi 97
            lt?
            bnt L_164d
            pushi 127
            push1
            pTos x
            ldi 96
            lt?
            bnt L_163c
            ldi 4
            jmp L_164a
            L_163c: pTos x
            ldi 153
            lt?
            bnt L_1648
            ldi 5
            jmp L_164a
            L_1648: ldi 6
            L_164a: push
            self 6
            L_164d: ldi 0
            ret
            L_1650: pTos type
            ldi 4
            eq?
            bnt L_166b
            pToa presentation
            bnt L_166b
            pTos message
            ldi 118
            eq?
            bnt L_166b
            pushi 392
            push0
            self 4
            ldi 0
            ret
            L_166b: pTos type
            ldi 4
            eq?
            bnt L_169b
            pToa presentation
            bnt L_169b
            pTos message
            ldi 91
            eq?
            bt L_1684
            pTos message
            ldi 93
            eq?
            bnt L_169b
            L_1684: pushi 389
            push1
            pTos message
            ldi 91
            eq?
            bnt L_1693
            ldi -10
            jmp L_1695
            L_1693: ldi 10
            L_1695: push
            self 6
            ldi 0
            ret
            L_169b: pTos type
            ldi 4
            eq?
            bnt L_18bc
            pTos message
            ldi 121
            eq?
            bnt L_16b7
            pToa musicMuted
            not
            aTop musicMuted
            ldi 1
            aTop dirty
            ldi 0
            ret
            L_16b7: pTos message
            ldi 114
            eq?
            bnt L_16cb
            pToa musicUnavailable
            bnt L_16cb
            pushi 699
            push0
            self 4
            ldi 0
            ret
            L_16cb: pTos message
            ldi 45
            eq?
            bt L_16e0
            pTos message
            ldi 43
            eq?
            bt L_16e0
            pTos message
            ldi 61
            eq?
            bnt L_172c
            L_16e0: pTos masterVolume
            pTos message
            ldi 45
            eq?
            bnt L_16ee
            ldi -10
            jmp L_16f0
            L_16ee: ldi 10
            L_16f0: add
            aTop masterVolume
            pTos masterVolume
            ldi 0
            lt?
            bnt L_1701
            ldi 0
            aTop masterVolume
            L_1701: pTos masterVolume
            ldi 100
            gt?
            bnt L_170e
            ldi 100
            aTop masterVolume
            L_170e: pToa presentation
            bnt L_1724
            pushi 126
            push1
            pTos masterVolume
            pToa presentation
            send 6
            pushi 370
            push0
            pToa presentation
            send 4
            L_1724: ldi 1
            aTop dirty
            ldi 0
            ret
            L_172c: pTos message
            ldi 15360
            eq?
            bnt L_173d
            pushi 342
            push0
            self 4
            ldi 0
            ret
            L_173d: pTos message
            ldi 15616
            eq?
            bnt L_174e
            pushi 245
            push0
            self 4
            ldi 0
            ret
            L_174e: pToa opening
            bnt L_17b2
            pTos message
            dup
            ldi 120
            eq?
            bnt L_1761
            pushi 102
            push0
            self 4
            jmp L_17a3
            L_1761: dup
            ldi 27
            eq?
            bnt L_176e
            pushi 102
            push0
            self 4
            jmp L_17a3
            L_176e: dup
            ldi 110
            eq?
            bnt L_177c
            pushi 154
            push0
            self 4
            jmp L_17a3
            L_177c: dup
            ldi 19712
            eq?
            bnt L_178b
            pushi 154
            push0
            self 4
            jmp L_17a3
            L_178b: dup
            ldi 104
            eq?
            bnt L_1798
            pToa creditHeld
            not
            aTop creditHeld
            jmp L_17a3
            L_1798: dup
            ldi 32
            eq?
            bnt L_17a3
            pToa creditHeld
            not
            aTop creditHeld
            L_17a3: toss
            pushi 259
            push0
            self 4
            ldi 1
            aTop dirty
            ldi 0
            ret
            L_17b2: pToa menuOpen
            bt L_17bb
            pToa paused
            bnt L_183b
            L_17bb: pTos message
            ldi 49
            ge?
            bnt L_181d
            pTos message
            ldi 54
            le?
            bnt L_181d
            pTos message
            dup
            ldi 49
            eq?
            bnt L_17d9
            pushi 342
            push0
            self 4
            jmp L_181c
            L_17d9: dup
            ldi 50
            eq?
            bnt L_17e7
            pushi 245
            push0
            self 4
            jmp L_181c
            L_17e7: dup
            ldi 51
            eq?
            bnt L_17f5
            pushi 258
            push0
            self 4
            jmp L_181c
            L_17f5: dup
            ldi 52
            eq?
            bnt L_1805
            ldi 0
            aTop menuOpen
            ldi 0
            aTop paused
            jmp L_181c
            L_1805: dup
            ldi 53
            eq?
            bnt L_1811
            ldi 1
            aTop quitRequested
            jmp L_181c
            L_1811: dup
            ldi 54
            eq?
            bnt L_181c
            pToa audienceMuted
            not
            aTop audienceMuted
            L_181c: toss
            L_181d: pTos message
            ldi 27
            eq?
            bt L_182b
            pTos message
            ldi 109
            eq?
            bnt L_1833
            L_182b: ldi 0
            aTop menuOpen
            ldi 0
            aTop paused
            L_1833: ldi 1
            aTop dirty
            ldi 0
            ret
            L_183b: pTos message
            ldi 109
            eq?
            bnt L_184b
            pushi 306
            push0
            self 4
            ldi 0
            ret
            L_184b: pTos message
            ldi 97
            eq?
            bnt L_18a9
            pToa audienceMuted
            not
            aTop audienceMuted
            pToa audienceMuted
            bnt L_1860
            ldi 0
            aTop audioPending
            L_1860: pToa presentation
            bnt L_186f
            pushi 373
            push2
            push2
            pTos audienceMuted
            pToa presentation
            send 8
            L_186f: pToa presentation
            bnt L_1895
            pToa speechCaption
            bt L_1885
            pushi 347
            push0
            pToa presentation
            send 4
            push
            ldi 1
            eq?
            bnt L_1895
            L_1885: ldi 1
            aTop dirty
            pushi 383
            push1
            lofss "audience setting"
            self 6
            jmp L_18a6
            L_1895: pushi 253
            push1
            pToa audienceMuted
            bnt L_18a1
            ldi 50
            jmp L_18a3
            L_18a1: ldi 51
            L_18a3: push
            self 6
            L_18a6: ldi 0
            ret
            L_18a9: pTos message
            ldi 27
            eq?
            bnt L_18bc
            pToa uiPanel
            not
            bnt L_18bc
            pushi 133
            push0
            self 4
            L_18bc: pToa opening
            bnt L_18f5
            pTos type
            ldi 1
            eq?
            bnt L_18f2
            pTos y
            ldi 155
            ge?
            bnt L_18f2
            pTos x
            ldi 107
            lt?
            bnt L_18dd
            pushi 102
            push0
            self 4
            jmp L_18f2
            L_18dd: pTos x
            ldi 213
            lt?
            bnt L_18ed
            pushi 154
            push0
            self 4
            jmp L_18f2
            L_18ed: pToa creditHeld
            not
            aTop creditHeld
            L_18f2: ldi 0
            ret
            L_18f5: pToa menuOpen
            bt L_18fd
            pToa paused
            bnt L_1900
            L_18fd: ldi 0
            ret
            L_1900: pushi 313
            push0
            self 4
            bnt L_190b
            ldi 0
            ret
            L_190b: pTos type
            ldi 4
            eq?
            bnt L_1941
            pTos message
            ldi 104
            eq?
            bnt L_192d
            pushi 133
            push0
            self 4
            pushi 58
            push0
            self 4
            pushi 640
            push0
            self 4
            ldi 0
            ret
            L_192d: pTos message
            ldi 15104
            eq?
            bnt L_1941
            pushi 325
            push2
            lofss "CONTROLS"
            lofss "TAB / SHIFT-TAB FOCUS. ARROWS MOVE FOCUS.\nENTER ACTS. ESC CANCELS OR GOES BACK.\nSPACE SHOWS HOTSPOTS; HIDE TURNS THEM OFF.\nRIGHT-CLICK USES THE DEFAULT ACTION.\nH HINTS. M MENU. F2 SAVE. F3 LOAD.\nY MUSIC. A AUDIENCE. +/- GAME VOLUME.\nV VOICE ON/OFF. [ ] VOICE LEVEL.\nE EFFECTS ON/OFF. , . EFFECTS LEVEL.\nVOICE ON TAKES EFFECT ON THE NEXT LINE."
            self 8
            L_1941: pTos type
            ldi 1
            eq?
            bnt L_1988
            pToa uiPanel
            not
            bnt L_1988
            pTos y
            ldi 43
            ge?
            bnt L_1988
            pTos y
            ldi 144
            lt?
            bnt L_1988
            pToa x
            sat 1
            lst 1
            ldi 40
            lt?
            bnt L_196c
            ldi 40
            sat 1
            L_196c: lst 1
            ldi 280
            gt?
            bnt L_1979
            ldi 280
            sat 1
            L_1979: pushi 142
            pushi 5
            lst 1
            pushi 132
            push0
            push0
            push0
            self 14
            L_1988: ret
        )
    )

    ; Delivered offset0x1989; 50 original instructions
    (method (advance arg1)
(if (and p08 (p08 h8RouteTick: arg1)) (return 0))

(if (and p05 (p05 hFailure?)) (return 0)) (if p05 (p05 hStageTick: arg1))

        (asm
            pushi 738
            push1
            lsp 1
            self 6
            lsp 1
            ldi 0
            lt?
            bnt L_199c
            ldi 0
            sap 1
            L_199c: lsp 1
            ldi 12
            gt?
            bnt L_19a7
            ldi 12
            sap 1
            L_19a7: pToa opening
            bnt L_19e2
            pToa creditHeld
            not
            bnt L_19df
            pTos creditElapsed
            lap 1
            add
            aTop creditElapsed
            pTos creditElapsed
            ldi 360
            ge?
            bnt L_19df
            pTos creditElapsed
            ldi 360
            sub
            aTop creditElapsed
            ipToa creditCard
            pTos creditCard
            ldi 10
            ge?
            bnt L_19da
            pushi 102
            push0
            self 4
            L_19da: ldi 1
            aTop dirty
            L_19df: ldi 0
            ret
            L_19e2: pushi 130
            push1
            lsp 1
            self 6
            ret
        )
    )

    ; Delivered offset0x19eb; 111 original instructions
    (method (eventLoop &tmp t0 t1)
        (asm
            push0
            callk GetTime, 0
            aTop lastTick
            L_19f4: pToa quitRequested
            not
            bnt L_1ab6
            push2
            pushi 32767
            pushSelf
            callk GetEvent, 4
            push0
            callk GetTime, 0
            sat 0
            lst 0
            pToa lastTick
            sub
            sat 1
            lat 0
            aTop lastTick
            pToa opening
            not
            bnt L_1a2a
            pToa menuOpen
            not
            bnt L_1a2a
            pToa paused
            not
            bnt L_1a2a
            pushi 330
            push0
            self 4
            L_1a2a: pToa type
            bnt L_1a33
            pushi 118
            push0
            self 4
            L_1a33: pushi 259
            push0
            self 4
            pushi 10
            push1
            lst 1
            self 6
            pushi 259
            push0
            self 4
            pushi 42
            push1
            lst 1
            self 6
            pushi 381
            push0
            self 4
            pushi 110
            push0
            self 4
            pToa dirty
            bnt L_1aae
            pushi 246
            push0
            self 4
            pToa opening
            not
            bnt L_1a86
            pToa menuOpen
            not
            bnt L_1a86
            pToa paused
            not
            bnt L_1a86
            pTos uiPanel
            ldi 4
            eq?
            bnt L_1a86
            pToa uiFailure
            not
            bnt L_1a86
            pushi 406
            push0
            self 4
            L_1a86: pToa opening
            not
            bnt L_1aae
            pToa menuOpen
            not
            bnt L_1aae
            pToa paused
            not
            bnt L_1aae
            pTos uiPanel
            ldi 1
            eq?
            bnt L_1aae
            pToa uiFailure
            not
            bnt L_1aae
            pushi 70
            push2
            pTos uiDocument
            pTos uiPage
            self 8
            L_1aae: push1
            push1
            callk Wait, 2
            jmp L_19f4
            L_1ab6: pushi 50
            push0
            self 4
            ldi 0
            ret
        )
    )

    ; Delivered offset0x1abe; 76 original instructions
    (method (play)
        (asm
            push2
            pushi 982
            push0
            callk ScriptID, 4
            aTop dialogue
            push2
            pushi 983
            push0
            callk ScriptID, 4
            aTop p03
            pushi 617
            push0
            pToa p03
            send 4
            pushi #p04Initialize
            push0
            self 4
            pushi 519
            push1
            pushi 544
            push1
            pushSelf
            pToa p03
            send 6
            push
            pToa p03
            send 6
            pushi 519
            push0
            pToa p03
            send 4
            not
            bnt L_1b0a
            pushi 521
            push0
            pToa p03
            send 4
            aTop p03HostError
            ldi 1
            aTop p03Invalid
            ldi 10
            aTop uiFailure
            L_1b0a: push2
            pushi 980
            push0
            callk ScriptID, 4
            aTop presentation
            push2
            pushi 981
            push0
            callk ScriptID, 4
            aTop musicOwner
            selfID
            sal 1
            pushi 3
            pushi 205
            push0
            push0
            callk SetCursor, 6
            push1
            push1
            callk SetCursor, 2
            pToa location
            aTop roomSeen
            pToa onApron
            aTop apronSeen
            pushi 259
            push0
            self 4
            pushi 29
            push0
            self 4
            pushi 246
            push0
            self 4
            pushi 101
            push0
            self 4
            ret
        )
    )

    ; Delivered offset0x1b51; 84 original instructions
    (method (replay)
(if (not (self p05RestoreBegin:)) (self p05RestoreReject:) (return 0))

        (asm
            ldi 0
            aTop navNotice
            ldi 0
            aTop navNoticeTicks
            pushi 560
            push0
            self 4
            push2
            pushi 982
            push0
            callk ScriptID, 4
            aTop dialogue
            push2
            pushi 983
            push0
            callk ScriptID, 4
            aTop p03
            push2
            pushi 984
            push0
            callk ScriptID, 4
            aTop p04
            push2
            pushi 980
            push0
            callk ScriptID, 4
            aTop presentation
            push2
            pushi 981
            push0
            callk ScriptID, 4
            aTop musicOwner
            pushi 377
            push0
            self 4
            ldi 0
            aTop audioPending
            ldi 0
            aTop audioDialogue
            push0
            callk GetTime, 0
            aTop lastTick
            ldi 1
            aTop dirty
            pushi 3
            pushi 205
            push0
            push0
            callk SetCursor, 6
            push1
            push1
            callk SetCursor, 2
            pushi 133
            push0
            self 4
            pToa location
            aTop roomSeen
            pToa onApron
            aTop apronSeen
            pushi 259
            push0
            self 4
            pushi 44
            push0
            self 4
            pushi 56
            push0
            self 4
            pushi 447
            push1
            pTos presentation
            pToa dialogue
            send 6
            pushi 645
            push0
            self 4
            pushi #p04Restore
            push0
            self 4
            pushi #p05RestoreValidate
            push0
            self 4
            pushi 259
            push0
            self 4
            pushi 28
            push0
            self 4
            pushi 246
            push0
            self 4
            pushi 101
            push0
            self 4
            ret
        )
    )

    ; Delivered offset0x1bf9; 1286 original instructions
    (method (renderCaption)
 (return ((ScriptID 991 0) renderCaption: self)))

    ; Delivered offset0x25c4; 7 original instructions
    (method (p02HostP01Act action obj target) (self act: action obj target))

    ; Delivered offset0x25d1; 31 original instructions
    (method (p02HostEvent arg1)
        (asm
            pToa presentation
            bnt L_25f3
            pushi 559
            pushi 6
            lsp 1
            pTos p02Revision
            pTos location
            pTos onApron
            push0
            callk GetTime, 0
            push
            pushi 388
            push0
            pToa presentation
            send 4
            push
            self 16
            L_25f3: lsp 1
            ldi 453
            eq?
            bnt L_2602
            pushi 24
            push1
            pushi 3
            self 6
            L_2602: pushi 111
            push0
            self 4
            ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x260d; 251 original instructions
    (method (uiHostItemLabel arg1)
(if ((ScriptID 996 0) h14Owns: arg1) (return ((ScriptID 996 0) h14Label: arg1)))

(if (and ((ScriptID 995 0) h13Has:) (or (>= ((ScriptID 995 0) h13Index: arg1) 0) (== arg1 432) (== arg1 433) (== arg1 434) (== arg1 92) (== arg1 42) (== arg1 72) (== arg1 410))) (return ((ScriptID 995 0) h13Label: arg1)))

(if (or (== arg1 419) (== arg1 420)) (return ((ScriptID 994 0) h12Label: arg1)))

(if (and (>= arg1 415) (<= arg1 418)) (return ((ScriptID 993 0) h11Label: arg1)))

(if (and p08 (== (p08 h8V: 1 0) 6) (or (== arg1 410) (== arg1 411) (>= ((ScriptID 992 0) p10CueIndex: arg1) 0))) (return ((ScriptID 992 0) h10Label: arg1)))

(if (and p09 (>= arg1 395) (<= arg1 398) (p09 h9Active:)) (return (p09 h9Label: arg1)))

(if (and p08 (>= arg1 116) (<= arg1 122)) (return (p08 h8LayoutLabel: arg1)))

(if (and p07 (>= arg1 86) (<= arg1 94)) (return (p07 h7Label: arg1)))

(if (and p06 (>= arg1 73) (<= arg1 85)) (return (p06 h6Label: arg1)))

(if (and p05 (>= arg1 63) (<= arg1 72)) (return (p05 hLabel: arg1)))

        (if (and (>= arg1 51) (<= arg1 62)) (return (self p04Label: arg1)))
        (asm
            lsp 1
            ldi -103
            eq?
            bt L_2622
            lsp 1
            ldi 33
            ge?
            bnt L_262b
            lsp 1
            ldi 50
            le?
            bnt L_262b
            L_2622: pushi 627
            push1
            lsp 1
            self 6
            ret
            L_262b: lsp 1
            dup
            ldi 0
            eq?
            bnt L_263a
            lofsa "..."
            ret
            jmp L_27cd
            L_263a: dup
            ldi 1
            eq?
            bnt L_2647
            lofsa "FRONT DOOR"
            ret
            jmp L_27cd
            L_2647: dup
            ldi 2
            eq?
            bnt L_2654
            lofsa "BUNNY"
            ret
            jmp L_27cd
            L_2654: dup
            ldi 3
            eq?
            bnt L_2661
            lofsa "BENCH"
            ret
            jmp L_27cd
            L_2661: dup
            ldi 4
            eq?
            bnt L_266e
            lofsa "WEDGE"
            ret
            jmp L_27cd
            L_266e: dup
            ldi 5
            eq?
            bnt L_267b
            lofsa "BREAD TRAY"
            ret
            jmp L_27cd
            L_267b: dup
            ldi 6
            eq?
            bnt L_2688
            lofsa "PRINT PACKET"
            ret
            jmp L_27cd
            L_2688: dup
            ldi 7
            eq?
            bnt L_2695
            lofsa "COMPARISON BOARD"
            ret
            jmp L_27cd
            L_2695: dup
            ldi 8
            eq?
            bnt L_26a2
            lofsa "FRANKIE MAPLEWOOD"
            ret
            jmp L_27cd
            L_26a2: dup
            ldi 9
            eq?
            bnt L_26af
            lofsa "AUDIENCE EDGE"
            ret
            jmp L_27cd
            L_26af: dup
            ldi 10
            eq?
            bnt L_26bc
            lofsa "AUDIENCE"
            ret
            jmp L_27cd
            L_26bc: dup
            ldi 11
            eq?
            bnt L_26c9
            lofsa "RETURN TO HOUSE"
            ret
            jmp L_27cd
            L_26c9: dup
            ldi 12
            eq?
            bnt L_26d6
            lofsa "KITCHEN"
            ret
            jmp L_27cd
            L_26d6: dup
            ldi 13
            eq?
            bnt L_26e3
            lofsa "COURTYARD"
            ret
            jmp L_27cd
            L_26e3: dup
            ldi 14
            eq?
            bnt L_26f0
            lofsa "SIDE PASSAGE"
            ret
            jmp L_27cd
            L_26f0: dup
            ldi 15
            eq?
            bnt L_26fd
            lofsa "MILO'S GARAGE"
            ret
            jmp L_27cd
            L_26fd: dup
            ldi 16
            eq?
            bnt L_270a
            lofsa "CONSERVATORY"
            ret
            jmp L_27cd
            L_270a: dup
            ldi 17
            eq?
            bnt L_2717
            lofsa "PORCH"
            ret
            jmp L_27cd
            L_2717: dup
            ldi 18
            eq?
            bnt L_2724
            lofsa "LIVING ROOM"
            ret
            jmp L_27cd
            L_2724: dup
            ldi 19
            eq?
            bnt L_2731
            lofsa "SIDE GATE"
            ret
            jmp L_27cd
            L_2731: dup
            ldi 20
            eq?
            bnt L_273e
            lofsa "JACKIE'S INVITATION"
            ret
            jmp L_27cd
            L_273e: dup
            ldi 21
            eq?
            bnt L_274b
            lofsa "BUNNY'S INVITATION"
            ret
            jmp L_27cd
            L_274b: dup
            ldi 22
            eq?
            bnt L_2757
            lofsa "STRINGER'S INVITATION"
            ret
            jmp L_27cd
            L_2757: dup
            ldi 23
            eq?
            bnt L_2763
            lofsa "COMPARED COPIES"
            ret
            jmp L_27cd
            L_2763: dup
            ldi 24
            eq?
            bnt L_276f
            lofsa "COMPLETE MASTER INVITATION"
            ret
            jmp L_27cd
            L_276f: dup
            ldi 25
            eq?
            bnt L_277b
            lofsa "GREASE PENCIL"
            ret
            jmp L_27cd
            L_277b: dup
            ldi 26
            eq?
            bnt L_2787
            lofsa "MATCHED BORDER"
            ret
            jmp L_27cd
            L_2787: dup
            ldi 27
            eq?
            bnt L_2793
            lofsa "INVITATION DRAWER"
            ret
            jmp L_27cd
            L_2793: dup
            ldi 28
            eq?
            bnt L_279f
            lofsa "MILO"
            ret
            jmp L_27cd
            L_279f: dup
            ldi 29
            eq?
            bnt L_27ab
            lofsa "STRINGER"
            ret
            jmp L_27cd
            L_27ab: dup
            ldi 30
            eq?
            bnt L_27b7
            lofsa "RITA"
            ret
            jmp L_27cd
            L_27b7: dup
            ldi 31
            eq?
            bnt L_27c3
            lofsa "PREPARATION CHECKLIST"
            ret
            jmp L_27cd
            L_27c3: dup
            ldi 32
            eq?
            bnt L_27cd
            lofsa "EVIDENCE JOURNAL"
            ret
            L_27cd: toss
            lofsa "UNKNOWN OBJECT"
            ret
        )
    )

    ; Delivered offset0x27d2; 88 original instructions
    (method (uiHostShortLabel arg1)
(if ((ScriptID 996 0) h14Owns: arg1) (return ((ScriptID 996 0) h14Label: arg1)))

(if (and ((ScriptID 995 0) h13Has:) (or (>= ((ScriptID 995 0) h13Index: arg1) 0) (== arg1 432) (== arg1 433) (== arg1 434) (== arg1 92) (== arg1 42) (== arg1 72) (== arg1 410))) (return ((ScriptID 995 0) h13Label: arg1)))

(if (or (== arg1 419) (== arg1 420)) (return ((ScriptID 994 0) h12Label: arg1)))

(if (and (>= arg1 415) (<= arg1 418)) (return ((ScriptID 993 0) h11Label: arg1)))

(if (and p08 (== (p08 h8V: 1 0) 6) (or (== arg1 410) (== arg1 411) (>= ((ScriptID 992 0) p10CueIndex: arg1) 0))) (return ((ScriptID 992 0) h10Label: arg1)))

(if (and p09 (>= arg1 395) (<= arg1 398) (p09 h9Active:)) (return (p09 h9Label: arg1)))

(if (and p08 (>= arg1 116) (<= arg1 122)) (return (p08 h8LayoutLabel: arg1)))

(if (and p07 (>= arg1 86) (<= arg1 94)) (return (p07 h7ShortLabel: arg1)))

(if (and p06 (>= arg1 73) (<= arg1 85)) (return (p06 h6ShortLabel: arg1)))

(if (and p05 (>= arg1 63) (<= arg1 72)) (return (p05 hShortLabel: arg1)))

        (if (== arg1 62) (return "BUNT."))
        (asm
            lsp 1
            dup
            ldi 39
            eq?
            bnt L_27e0
            lofsa "TOWEL"
            ret
            jmp L_27f6
            L_27e0: dup
            ldi 38
            eq?
            bnt L_27ec
            lofsa "CLOTH"
            ret
            jmp L_27f6
            L_27ec: dup
            ldi 35
            eq?
            bnt L_27f6
            lofsa "TILES"
            ret
            L_27f6: toss
            lsp 1
            dup
            ldi 4
            eq?
            bnt L_2805
            lofsa "WEDGE"
            ret
            jmp L_2863
            L_2805: dup
            ldi 5
            eq?
            bnt L_2811
            lofsa "TRAY"
            ret
            jmp L_2863
            L_2811: dup
            ldi 6
            eq?
            bnt L_281d
            lofsa "PRINT"
            ret
            jmp L_2863
            L_281d: dup
            ldi 20
            eq?
            bnt L_2829
            lofsa "J.CPY"
            ret
            jmp L_2863
            L_2829: dup
            ldi 21
            eq?
            bnt L_2835
            lofsa "BUNNY"
            ret
            jmp L_2863
            L_2835: dup
            ldi 22
            eq?
            bnt L_2841
            lofsa "STRNG"
            ret
            jmp L_2863
            L_2841: dup
            ldi 23
            eq?
            bnt L_284d
            lofsa "BNDLE"
            ret
            jmp L_2863
            L_284d: dup
            ldi 24
            eq?
            bnt L_2859
            lofsa "MASTR"
            ret
            jmp L_2863
            L_2859: dup
            ldi 25
            eq?
            bnt L_2863
            lofsa "PENCL"
            ret
            L_2863: toss
            lofsa "ITEM"
            ret
        )
    )

    ; Delivered offset0x2868; 4 original instructions
    (method (uiHostIsReturn obj) (return (== obj 11)))

    ; Delivered offset0x286e; 112 original instructions
    (method (uiHostDefaultVerb arg1)
(if (or (== arg1 419) (== arg1 420)) (return 9))

(if (and (>= arg1 415) (<= arg1 418)) (return 5))

(if (or (== arg1 410) (== arg1 411)) (return 5))

(if (and p09 (>= arg1 395) (<= arg1 398) (p09 h9Active:)) (return (p09 h9Geo: (if (== arg1 398) 6 else (if (== arg1 397) 5 else 0)) 7)))

        (if (and p04 (== arg1 4) (p04 p04Wedge?)) (return 4))
        (if (== arg1 54) (return 6))
        (if (and (>= arg1 51) (<= arg1 62)) (return 5))
        (asm
            lsp 1
            ldi 38
            eq?
            bt L_287c
            lsp 1
            ldi 39
            eq?
            bnt L_288d
            L_287c: pushi 551
            push1
            lsp 1
            self 6
            bnt L_288a
            ldi 5
            jmp L_288c
            L_288a: ldi 4
            L_288c: ret
            L_288d: lsp 1
            ldi -103
            eq?
            bt L_28a2
            lsp 1
            ldi 33
            ge?
            bnt L_28a5
            lsp 1
            ldi 50
            le?
            bnt L_28a5
            L_28a2: ldi 5
            ret
            L_28a5: lsp 1
            ldi 9
            eq?
            bt L_28c1
            lsp 1
            ldi 11
            eq?
            bt L_28c1
            lsp 1
            ldi 12
            ge?
            bnt L_28c4
            lsp 1
            ldi 19
            le?
            bnt L_28c4
            L_28c1: ldi 0
            ret
            L_28c4: lsp 1
            ldi 1
            eq?
            bnt L_28d6
            pToa doorOpen
            bnt L_28d3
            ldi 0
            jmp L_28d5
            L_28d3: ldi 2
            L_28d5: ret
            L_28d6: lsp 1
            ldi 2
            eq?
            bt L_28f9
            lsp 1
            ldi 8
            eq?
            bt L_28f9
            lsp 1
            ldi 28
            eq?
            bt L_28f9
            lsp 1
            ldi 29
            eq?
            bt L_28f9
            lsp 1
            ldi 30
            eq?
            bnt L_28fc
            L_28f9: ldi 6
            ret
            L_28fc: lsp 1
            ldi 4
            eq?
            bt L_291f
            lsp 1
            ldi 5
            eq?
            bt L_291f
            lsp 1
            ldi 20
            ge?
            bnt L_2918
            lsp 1
            ldi 22
            le?
            bt L_291f
            L_2918: lsp 1
            ldi 24
            eq?
            bnt L_2930
            L_291f: pushi 551
            push1
            lsp 1
            self 6
            bnt L_292d
            ldi 5
            jmp L_292f
            L_292d: ldi 4
            L_292f: ret
            L_2930: ldi 5
            ret
        )
    )

    ; Delivered offset0x2933; 597 original instructions
    (method (uiHostWorldControls)
((ScriptID 996 0) h14Controls:)

((ScriptID 995 0) h13Controls:)
 (self h7BaseControls:) (if p07 (p07 h7Controls:)) (if p08 (p08 h8ClothControls:)) (if p08 (p08 h8RouteControls:)) (if p09 (p09 h9UI: 0)) ((ScriptID 992 0) h10Controls:) ((ScriptID 993 0) h11Controls:) ((ScriptID 994 0) h12Controls:) (return 1))

    ; Delivered offset0x2e28; 383 original instructions
    (method (approachX arg1)
(if ((ScriptID 996 0) h14Owns: arg1) (return 180))

(if ((ScriptID 995 0) h13Owns: arg1) (if (>= ((ScriptID 995 0) h13Index: arg1) 0) (return (+ 18 ((ScriptID 994 0) h12SuccessorX: ((ScriptID 995 0) h13Index: arg1))))) (return 180))

(if ((ScriptID 994 0) h12SuccessorHas: arg1) (return (+ 18 ((ScriptID 994 0) h12SuccessorX: ((ScriptID 994 0) h12SuccessorIndex: arg1)))))

(if (or (== arg1 419) (== arg1 420)) (return 200))

(if (and (>= arg1 415) (<= arg1 418)) (return 150))

(if (or (== arg1 410) (== arg1 411)) (return 200))

(if (and p09 (>= arg1 395) (<= arg1 398) (p09 h9Active:)) (return (p09 h9Geo: (if (== arg1 398) 6 else (if (== arg1 397) 5 else 0)) 5)))

(if (and p08 (p08 h8LayoutTarget: arg1)) (return (p08 h8LayoutApproach: arg1 0)))

(if (and p08 (== location 2) (p08 h8ClothTarget: arg1)) (return 139))

(if (and p07 (or (and (>= arg1 86) (<= arg1 94)) (and (== arg1 2) (== location 2)))) (return (p07 h7ApproachX: arg1)))

(if (and p06 (>= arg1 73) (<= arg1 85)) (return (p06 h6ApproachX: arg1)))

(if (and p05 (== location 4) (not onApron)) (return (p05 hCourtApproachX: arg1))) (if (and p05 (== location 5) (not onApron)) (return (p05 hApproachX: arg1)))

        (if (and (== location 3) (not onApron)) (return (self p04ApproachX: arg1)))
        (asm
            lsp 1
            ldi 9
            eq?
            bnt L_2e52
            pTos location
            ldi 6
            eq?
            bnt L_2e3b
            ldi 294
            jmp L_2e51
            L_2e3b: pTos location
            ldi 1
            eq?
            bt L_2e49
            pTos location
            ldi 2
            eq?
            bnt L_2e4e
            L_2e49: ldi 314
            jmp L_2e51
            L_2e4e: ldi 282
            L_2e51: ret
            L_2e52: lsp 1
            ldi 11
            eq?
            bnt L_2e5c
            ldi 56
            ret
            L_2e5c: lsp 1
            ldi 10
            eq?
            bnt L_2e67
            ldi 152
            ret
            L_2e67: pTos location
            dup
            ldi 0
            eq?
            bnt L_2ecf
            lsp 1
            dup
            ldi 3
            eq?
            bnt L_2e7c
            ldi 92
            ret
            jmp L_2ecb
            L_2e7c: dup
            ldi 1
            eq?
            bnt L_2e88
            ldi 205
            ret
            jmp L_2ecb
            L_2e88: dup
            ldi 2
            eq?
            bnt L_2e94
            ldi 138
            ret
            jmp L_2ecb
            L_2e94: dup
            ldi 14
            eq?
            bnt L_2e9f
            ldi 56
            ret
            jmp L_2ecb
            L_2e9f: dup
            ldi 15
            eq?
            bnt L_2eaa
            ldi 56
            ret
            jmp L_2ecb
            L_2eaa: dup
            ldi 16
            eq?
            bnt L_2eb6
            ldi 267
            ret
            jmp L_2ecb
            L_2eb6: dup
            ldi 4
            eq?
            bnt L_2ec2
            ldi 132
            ret
            jmp L_2ecb
            L_2ec2: dup
            ldi 5
            eq?
            bnt L_2ecb
            ldi 96
            ret
            L_2ecb: toss
            jmp L_309e
            L_2ecf: dup
            ldi 1
            eq?
            bnt L_2f4b
            lsp 1
            dup
            ldi 17
            eq?
            bnt L_2ee2
            ldi 35
            ret
            jmp L_2f47
            L_2ee2: dup
            ldi 12
            eq?
            bnt L_2eee
            ldi 297
            ret
            jmp L_2f47
            L_2eee: dup
            ldi 13
            eq?
            bnt L_2efa
            ldi 171
            ret
            jmp L_2f47
            L_2efa: dup
            ldi 7
            eq?
            bnt L_2f05
            ldi 117
            ret
            jmp L_2f47
            L_2f05: dup
            ldi 8
            eq?
            bnt L_2f10
            ldi 113
            ret
            jmp L_2f47
            L_2f10: dup
            ldi 2
            eq?
            bnt L_2f1c
            ldi 211
            ret
            jmp L_2f47
            L_2f1c: dup
            ldi 21
            eq?
            bnt L_2f27
            ldi 101
            ret
            jmp L_2f47
            L_2f27: dup
            ldi 26
            eq?
            bnt L_2f32
            ldi 117
            ret
            jmp L_2f47
            L_2f32: dup
            ldi 4
            eq?
            bnt L_2f3d
            ldi 42
            ret
            jmp L_2f47
            L_2f3d: dup
            ldi 30
            eq?
            bnt L_2f47
            ldi 229
            ret
            L_2f47: toss
            jmp L_309e
            L_2f4b: dup
            ldi 2
            eq?
            bnt L_2f93
            lsp 1
            dup
            ldi 18
            eq?
            bnt L_2f5e
            ldi 54
            ret
            jmp L_2f8f
            L_2f5e: dup
            ldi 38
            eq?
            bnt L_2f69
            ldi 124
            ret
            jmp L_2f8f
            L_2f69: dup
            ldi 39
            eq?
            bnt L_2f74
            ldi 124
            ret
            jmp L_2f8f
            L_2f74: dup
            ldi 44
            eq?
            bnt L_2f7f
            ldi 124
            ret
            jmp L_2f8f
            L_2f7f: dup
            ldi 40
            eq?
            bnt L_2f8b
            ldi 244
            ret
            jmp L_2f8f
            L_2f8b: ldi 198
            ret
            L_2f8f: toss
            jmp L_309e
            L_2f93: dup
            ldi 3
            eq?
            bnt L_2fb4
            lsp 1
            dup
            ldi 17
            eq?
            bnt L_2fa6
            ldi 56
            ret
            jmp L_2fb0
            L_2fa6: dup
            ldi 19
            eq?
            bnt L_2fb0
            ldi 262
            ret
            L_2fb0: toss
            jmp L_309e
            L_2fb4: dup
            ldi 4
            eq?
            bnt L_2fd5
            lsp 1
            dup
            ldi 18
            eq?
            bnt L_2fc7
            ldi 56
            ret
            jmp L_2fd1
            L_2fc7: dup
            ldi 19
            eq?
            bnt L_2fd1
            ldi 262
            ret
            L_2fd1: toss
            jmp L_309e
            L_2fd5: dup
            ldi 5
            eq?
            bnt L_300d
            lsp 1
            dup
            ldi 17
            eq?
            bnt L_2fe8
            ldi 56
            ret
            jmp L_3009
            L_2fe8: dup
            ldi 28
            eq?
            bnt L_2ff3
            ldi 100
            ret
            jmp L_3009
            L_2ff3: dup
            ldi 27
            eq?
            bnt L_2fff
            ldi 201
            ret
            jmp L_3009
            L_2fff: dup
            ldi 24
            eq?
            bnt L_3009
            ldi 201
            ret
            L_3009: toss
            jmp L_309e
            L_300d: dup
            ldi 6
            eq?
            bnt L_309e
            lsp 1
            dup
            ldi 17
            eq?
            bnt L_3021
            ldi 56
            ret
            jmp L_309d
            L_3021: dup
            ldi 29
            eq?
            bnt L_302d
            ldi 138
            ret
            jmp L_309d
            L_302d: dup
            ldi 22
            eq?
            bnt L_3039
            ldi 213
            ret
            jmp L_309d
            L_3039: dup
            ldi 30
            eq?
            bnt L_3045
            ldi 217
            ret
            jmp L_309d
            L_3045: dup
            ldi 33
            eq?
            bnt L_3050
            ldi 102
            ret
            jmp L_309d
            L_3050: dup
            ldi 34
            eq?
            bnt L_305b
            ldi 102
            ret
            jmp L_309d
            L_305b: dup
            ldi 36
            eq?
            bnt L_3066
            ldi 76
            ret
            jmp L_309d
            L_3066: dup
            ldi 37
            eq?
            bnt L_3071
            ldi 76
            ret
            jmp L_309d
            L_3071: dup
            ldi 40
            eq?
            bnt L_307c
            ldi 125
            ret
            jmp L_309d
            L_307c: dup
            ldi 41
            eq?
            bnt L_3088
            ldi 276
            ret
            jmp L_309d
            L_3088: dup
            ldi 42
            eq?
            bnt L_3094
            ldi 276
            ret
            jmp L_309d
            L_3094: dup
            ldi 47
            eq?
            bnt L_309d
            ldi 76
            ret
            L_309d: toss
            L_309e: toss
            ldi 140
            ret
        )
    )

    ; Delivered offset0x30a3; 374 original instructions
    (method (approachY arg1)
(if ((ScriptID 996 0) h14Owns: arg1) (return 128))

(if ((ScriptID 995 0) h13Owns: arg1) (return 128))

(if ((ScriptID 994 0) h12SuccessorHas: arg1) (return 128))

(if (or (== arg1 419) (== arg1 420)) (return 110))

(if (and (>= arg1 415) (<= arg1 418)) (return 120))

(if (or (== arg1 410) (== arg1 411)) (return 110))

(if (and p09 (>= arg1 395) (<= arg1 398) (p09 h9Active:)) (return (p09 h9Geo: (if (== arg1 398) 6 else (if (== arg1 397) 5 else 0)) 6)))

(if (and p08 (p08 h8LayoutTarget: arg1)) (return (p08 h8LayoutApproach: arg1 1)))

(if (and p08 (== location 2) (p08 h8ClothTarget: arg1)) (return 130))

(if (and p07 (or (and (>= arg1 86) (<= arg1 94)) (and (== arg1 2) (== location 2)))) (return (p07 h7ApproachY: arg1)))

(if (and p06 (>= arg1 73) (<= arg1 85)) (return (p06 h6ApproachY: arg1)))

(if (and p05 (== location 4) (not onApron)) (return (p05 hCourtApproachY: arg1))) (if (and p05 (== location 5) (not onApron)) (return (p05 hApproachY: arg1)))

        (if (and (== location 3) (not onApron)) (return (self p04ApproachY: arg1)))
        (asm
            lsp 1
            ldi 9
            eq?
            bnt L_30c8
            pTos location
            ldi 1
            eq?
            bt L_30bf
            pTos location
            ldi 2
            eq?
            bt L_30bf
            pTos location
            ldi 6
            eq?
            bnt L_30c4
            L_30bf: ldi 138
            jmp L_30c7
            L_30c4: ldi 132
            L_30c7: ret
            L_30c8: lsp 1
            ldi 11
            eq?
            bnt L_30d3
            ldi 132
            ret
            L_30d3: lsp 1
            ldi 10
            eq?
            bnt L_30de
            ldi 132
            ret
            L_30de: pTos location
            dup
            ldi 0
            eq?
            bnt L_3145
            lsp 1
            dup
            ldi 3
            eq?
            bnt L_30f3
            ldi 124
            ret
            jmp L_3141
            L_30f3: dup
            ldi 1
            eq?
            bnt L_30fe
            ldi 124
            ret
            jmp L_3141
            L_30fe: dup
            ldi 2
            eq?
            bnt L_3109
            ldi 122
            ret
            jmp L_3141
            L_3109: dup
            ldi 14
            eq?
            bnt L_3115
            ldi 132
            ret
            jmp L_3141
            L_3115: dup
            ldi 15
            eq?
            bnt L_3121
            ldi 132
            ret
            jmp L_3141
            L_3121: dup
            ldi 16
            eq?
            bnt L_312d
            ldi 132
            ret
            jmp L_3141
            L_312d: dup
            ldi 4
            eq?
            bnt L_3138
            ldi 122
            ret
            jmp L_3141
            L_3138: dup
            ldi 5
            eq?
            bnt L_3141
            ldi 124
            ret
            L_3141: toss
            jmp L_3317
            L_3145: dup
            ldi 1
            eq?
            bnt L_31c2
            lsp 1
            dup
            ldi 17
            eq?
            bnt L_3158
            ldi 120
            ret
            jmp L_31be
            L_3158: dup
            ldi 12
            eq?
            bnt L_3163
            ldi 118
            ret
            jmp L_31be
            L_3163: dup
            ldi 13
            eq?
            bnt L_316e
            ldi 116
            ret
            jmp L_31be
            L_316e: dup
            ldi 7
            eq?
            bnt L_317a
            ldi 134
            ret
            jmp L_31be
            L_317a: dup
            ldi 8
            eq?
            bnt L_3186
            ldi 132
            ret
            jmp L_31be
            L_3186: dup
            ldi 2
            eq?
            bnt L_3192
            ldi 132
            ret
            jmp L_31be
            L_3192: dup
            ldi 21
            eq?
            bnt L_319e
            ldi 128
            ret
            jmp L_31be
            L_319e: dup
            ldi 26
            eq?
            bnt L_31aa
            ldi 134
            ret
            jmp L_31be
            L_31aa: dup
            ldi 4
            eq?
            bnt L_31b5
            ldi 126
            ret
            jmp L_31be
            L_31b5: dup
            ldi 30
            eq?
            bnt L_31be
            ldi 127
            ret
            L_31be: toss
            jmp L_3317
            L_31c2: dup
            ldi 2
            eq?
            bnt L_3202
            lsp 1
            dup
            ldi 18
            eq?
            bnt L_31d6
            ldi 130
            ret
            jmp L_31fe
            L_31d6: dup
            ldi 38
            eq?
            bnt L_31e2
            ldi 130
            ret
            jmp L_31fe
            L_31e2: dup
            ldi 39
            eq?
            bnt L_31ee
            ldi 130
            ret
            jmp L_31fe
            L_31ee: dup
            ldi 44
            eq?
            bnt L_31fa
            ldi 130
            ret
            jmp L_31fe
            L_31fa: ldi 132
            ret
            L_31fe: toss
            jmp L_3317
            L_3202: dup
            ldi 3
            eq?
            bnt L_3224
            lsp 1
            dup
            ldi 17
            eq?
            bnt L_3216
            ldi 129
            ret
            jmp L_3220
            L_3216: dup
            ldi 19
            eq?
            bnt L_3220
            ldi 129
            ret
            L_3220: toss
            jmp L_3317
            L_3224: dup
            ldi 4
            eq?
            bnt L_3246
            lsp 1
            dup
            ldi 18
            eq?
            bnt L_3238
            ldi 128
            ret
            jmp L_3242
            L_3238: dup
            ldi 19
            eq?
            bnt L_3242
            ldi 129
            ret
            L_3242: toss
            jmp L_3317
            L_3246: dup
            ldi 5
            eq?
            bnt L_327e
            lsp 1
            dup
            ldi 17
            eq?
            bnt L_325a
            ldi 128
            ret
            jmp L_327a
            L_325a: dup
            ldi 28
            eq?
            bnt L_3266
            ldi 132
            ret
            jmp L_327a
            L_3266: dup
            ldi 27
            eq?
            bnt L_3271
            ldi 125
            ret
            jmp L_327a
            L_3271: dup
            ldi 24
            eq?
            bnt L_327a
            ldi 125
            ret
            L_327a: toss
            jmp L_3317
            L_327e: dup
            ldi 6
            eq?
            bnt L_3317
            lsp 1
            dup
            ldi 17
            eq?
            bnt L_3294
            ldi 132
            ret
            jmp L_3316
            L_3294: dup
            ldi 29
            eq?
            bnt L_32a0
            ldi 133
            ret
            jmp L_3316
            L_32a0: dup
            ldi 22
            eq?
            bnt L_32ac
            ldi 135
            ret
            jmp L_3316
            L_32ac: dup
            ldi 30
            eq?
            bnt L_32b8
            ldi 136
            ret
            jmp L_3316
            L_32b8: dup
            ldi 33
            eq?
            bnt L_32c4
            ldi 134
            ret
            jmp L_3316
            L_32c4: dup
            ldi 34
            eq?
            bnt L_32d0
            ldi 134
            ret
            jmp L_3316
            L_32d0: dup
            ldi 36
            eq?
            bnt L_32dc
            ldi 132
            ret
            jmp L_3316
            L_32dc: dup
            ldi 37
            eq?
            bnt L_32e8
            ldi 132
            ret
            jmp L_3316
            L_32e8: dup
            ldi 40
            eq?
            bnt L_32f4
            ldi 133
            ret
            jmp L_3316
            L_32f4: dup
            ldi 41
            eq?
            bnt L_3300
            ldi 136
            ret
            jmp L_3316
            L_3300: dup
            ldi 42
            eq?
            bnt L_330c
            ldi 136
            ret
            jmp L_3316
            L_330c: dup
            ldi 47
            eq?
            bnt L_3316
            ldi 132
            ret
            L_3316: toss
            L_3317: toss
            ldi 132
            ret
        )
    )

    ; Delivered offset0x331c; 16 original instructions
    (method (motionScale)
(if (and p05 (not onApron) (or (== location 4) (== location 5))) (return 127))

        (return (/ (+ (* (- (/ motionY 64) 50) 128) 45) 90)))

    ; Delivered offset0x3334; 22 original instructions
    (method (motionCancel)
(if (and motionPhase (!= motionPhase 3)) ((ScriptID 995 0) h13Cancel:))

(if (and motionPhase (!= motionPhase 3)) ((ScriptID 994 0) h12SuccessorCancel:))

(if p07 (p07 h7RetireLaugh:))

(if p05 (p05 hStageRetire:)) 

        (asm
            pushi 560
            push0
            self 4
            ldi 0
            aTop motionPhase
            ldi 0
            aTop motionFirst
            ldi 0
            aTop motionSecond
            ldi 0
            aTop motionPose
            pTos motionX
            ldi 64
            div
            aTop motionTargetX
            pTos motionY
            ldi 64
            div
            aTop motionTargetY
            ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x3366; 54 original instructions
    (method (motionRequest arg1 arg2 arg3 arg4 arg5)
(if motionPhase ((ScriptID 995 0) h13Cancel:))

(if motionPhase ((ScriptID 994 0) h12SuccessorCancel:))

((ScriptID 993 0) h11PayMove: arg1 arg2 arg3 arg4)

        (asm
            ldi 0
            aTop navNotice
            ldi 0
            aTop navNoticeTicks
            pushi 377
            push0
            self 4
            pushi 558
            push0
            self 4
            lap 1
            aTop motionGoalX
            lap 2
            aTop motionGoalY
            lap 3
            aTop motionVerb
            lap 4
            aTop motionFirst
            lap 5
            aTop motionSecond
            pToa location
            aTop motionRoom
            pToa onApron
            aTop motionApron
            pTos motionX
            ldi 64
            div
            aTop motionTargetX
            pushi #p05WalkCorridor
            push0
            self 4
            aTop motionTargetY
            ldi 1
            aTop motionPhase
            ldi 1
            aTop motionNotice
            ldi 1
            aTop dirty
            pTos motionX
            lsp 1
            ldi 64
            mul
            eq?
            bnt L_33dc
            pTos motionY
            lsp 2
            ldi 64
            mul
            eq?
            bnt L_33dc
            ldi 3
            aTop motionPhase
            pushi 132
            push0
            self 4
            L_33dc: ret
        )
    )

    ; Delivered offset0x33dd; 55 original instructions
    (method (motionArrive &tmp action first second)
        (switch motionPhase
            (1 (= motionPhase 2) (= motionTargetX motionGoalX) (= motionTargetY (self p05WalkCorridor:)))
            (2 (= motionPhase 3) (= motionTargetY motionGoalY))
            (3
                (= action motionVerb) (= first motionFirst) (= second motionSecond)
                (self motionCancel:)
                (if (and (== location motionRoom) (== onApron motionApron))
                    (if first (self hostActNow: action first second)))))
        (= dirty 1))

    ; Delivered offset0x3450; 229 original instructions
    (method (motionAdvance arg1 &tmp t0 t1 t2 t3 t4 t5)
        (asm
            pToa motionPhase
            not
            bt L_3469
            pToa uiPanel
            bt L_3469
            pToa paused
            bt L_3469
            pToa menuOpen
            bt L_3469
            pToa opening
            bnt L_3483
            L_3469: pToa uiPanel
            bt L_347a
            pToa paused
            bt L_347a
            pToa menuOpen
            bt L_347a
            pToa opening
            bnt L_3480
            L_347a: pushi 560
            push0
            self 4
            L_3480: ldi 0
            ret
            L_3483: pToa motionX
            sat 2
            pToa motionY
            sat 3
            pToa motionPose
            sat 4
            lsp 1
            ldi 0
            lt?
            bt L_34a0
            lsp 1
            ldi 6
            gt?
            bnt L_34a4
            L_34a0: ldi 99
            jmp L_34a6
            L_34a4: ldi 0
            L_34a6: sat 5
            pToa presentation
            bnt L_34b9
            pTos foleyWalkToken
            ldi -1
            eq?
            bnt L_34b9
            pushi 558
            push0
            self 4
            L_34b9: lsp 1
            ldi 0
            lt?
            bnt L_34c4
            ldi 0
            sap 1
            L_34c4: lsp 1
            ldi 6
            gt?
            bnt L_34cf
            ldi 6
            sap 1
            L_34cf: pushi 144
            push0
            self 4
            push
            ldi 2
            div
            push
            lap 1
            mul
            sat 0
            pTos motionTargetX
            ldi 64
            mul
            push
            pToa motionX
            sub
            sat 1
            lat 1
            bnt L_3537
            lst 1
            ldi 0
            gt?
            bnt L_34fb
            ldi 0
            jmp L_34fd
            L_34fb: ldi 1
            L_34fd: aTop motionLoop
            lst 1
            ldi 0
            gt?
            bnt L_351d
            lst 0
            lat 1
            gt?
            bnt L_3512
            lat 1
            sat 0
            L_3512: pTos motionX
            lat 0
            add
            aTop motionX
            jmp L_3535
            L_351d: lst 0
            push0
            lat 1
            sub
            gt?
            bnt L_352c
            push0
            lat 1
            sub
            sat 0
            L_352c: pTos motionX
            lat 0
            sub
            aTop motionX
            L_3535: jmp L_3579
            L_3537: pTos motionTargetY
            ldi 64
            mul
            push
            pToa motionY
            sub
            sat 1
            lst 1
            ldi 0
            gt?
            bnt L_3561
            lst 0
            lat 1
            gt?
            bnt L_3556
            lat 1
            sat 0
            L_3556: pTos motionY
            lat 0
            add
            aTop motionY
            jmp L_3579
            L_3561: lst 0
            push0
            lat 1
            sub
            gt?
            bnt L_3570
            push0
            lat 1
            sub
            sat 0
            L_3570: pTos motionY
            lat 0
            sub
            aTop motionY
            L_3579: pTos motionTicks
            lap 1
            add
            aTop motionTicks
            L_3582: pTos motionTicks
            ldi 6
            ge?
            bnt L_35a2
            pTos motionTicks
            ldi 6
            sub
            aTop motionTicks
            pTos motionFrame
            ldi 1
            add
            push
            ldi 4
            mod
            aTop motionFrame
            jmp L_3582
            L_35a2: pTos motionFrame
            ldi 1
            add
            aTop motionPose
            lst 4
            pToa motionPose
            ne?
            bnt L_35e7
            pTos motionPose
            ldi 1
            eq?
            bt L_35c3
            pTos motionPose
            ldi 3
            eq?
            bnt L_35e7
            L_35c3: lst 2
            pToa motionX
            ne?
            bt L_35d3
            lst 3
            pToa motionY
            ne?
            bnt L_35e7
            L_35d3: lst 5
            ldi 0
            eq?
            bnt L_35df
            pToa motionTicks
            sat 5
            L_35df: pushi 569
            push1
            lst 5
            self 6
            L_35e7: pTos motionX
            pTos motionTargetX
            ldi 64
            mul
            eq?
            bnt L_3605
            pTos motionY
            pTos motionTargetY
            ldi 64
            mul
            eq?
            bnt L_3605
            pushi 132
            push0
            self 4
            L_3605: ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x360b; 77 original instructions
    (method (drawJack)
 (return ((ScriptID 991 0) drawJack: self)))

    ; Delivered offset0x369e; 118 original instructions
    (method (hostRoomChanged &tmp t0)
(if (and p08 (or (!= roomSeen location) (!= apronSeen onApron))) (p08 h8ReaderRetire: 1))

        (asm
            pTos roomSeen
            pToa location
            ne?
            bt L_36b1
            pTos apronSeen
            pToa onApron
            ne?
            bnt L_379e
            L_36b1: pToa roomSeen
            sat 0
            pushi 377
            push0
            self 4
            pushi 133
            push0
            self 4
            pToa location
            aTop roomSeen
            pToa onApron
            aTop apronSeen
            pToa onApron
            bnt L_36d5
            ldi 7680
            jmp L_36d8
            L_36d5: ldi 8960
            L_36d8: aTop motionX
            ldi 8448
            aTop motionY
            pTos location
            ldi 1
            eq?
            bnt L_3738
            pToa onApron
            not
            bnt L_3738
            lst 0
            dup
            ldi 0
            eq?
            bnt L_3703
            ldi 3008
            aTop motionX
            ldi 8320
            aTop motionY
            jmp L_3737
            L_3703: dup
            ldi 2
            eq?
            bnt L_3717
            ldi 18304
            aTop motionX
            ldi 8192
            aTop motionY
            jmp L_3737
            L_3717: dup
            ldi 4
            eq?
            bnt L_372b
            ldi 10944
            aTop motionX
            ldi 7936
            aTop motionY
            jmp L_3737
            L_372b: ldi 3200
            aTop motionX
            ldi 8832
            aTop motionY
            L_3737: toss
            L_3738: pToa onApron
            not
            bnt L_3757
            pTos location
            ldi 5
            eq?
            bt L_374b
            pTos location
            ldi 6
            eq?
            bnt L_3757
            L_374b: ldi 3584
            aTop motionX
            ldi 8320
            aTop motionY
            L_3757: pTos location
            ldi 6
            eq?
            bnt L_376f
            pToa onApron
            not
            bnt L_376f
            ldi 3264
            aTop motionX
            ldi 8768
            aTop motionY
            L_376f: pTos location
            ldi 2
            eq?
            bnt L_3787
            pToa onApron
            not
            bnt L_3787
            ldi 4160
            aTop motionX
            ldi 8704
            aTop motionY
            L_3787: pToa p03
            bnt L_3794
            pushi 525
            push1
            pushSelf
            pToa p03
            send 6
            L_3794: pushi #p04RoomArrived
            push1
            lst 0
            self 6
            ldi 0
            aTop motionNotice
            ldi 1
            aTop dirty
            L_379e: ret
        )
    )

    ; Delivered offset0x379f; 87 original instructions
    (method (hostActNow arg1 arg2 arg3 &tmp t0 t1 t2)
(if ((ScriptID 996 0) h14Frame: 3) (return 0))

(if ((ScriptID 995 0) h13Frame: 3) (return 0))

(if ((ScriptID 994 0) h12Frame: 3) (return 0))

(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)

(if ((ScriptID 993 0) h11Frame: 3) (return 0))

(if ((ScriptID 992 0) h10Frame: 3) (return 0))

(if ((ScriptID 992 0) h10Stop: arg2 arg3) (return 0))
(if (and p08 (p08 h8RouteBlock: arg1 arg2 arg3)) (return 0))

(if (and p08 (p08 h8ActionBarrier:)) (return 0))

(if (and p07 (p07 h7Barrier:)) (return 0))

(if (and p06 (p06 h6Barrier:)) (return 0))

(if (and p05 (p05 hBarrier:)) (return 0))

        (asm
            lap 3
            bnt L_37a9
            lap 3
            jmp L_37ab
            L_37a9: lap 2
            L_37ab: sat 2
            pToa onApron
            not
            bnt L_37df
            pTos location
            ldi 0
            eq?
            bnt L_37c5
            lst 2
            ldi 2
            eq?
            bnt L_37c5
            ldi 1
            aTop motionLoop
            L_37c5: pTos location
            ldi 1
            eq?
            bnt L_37df
            lst 2
            ldi 2
            eq?
            bt L_37da
            lst 2
            ldi 8
            eq?
            bnt L_37df
            L_37da: ldi 0
            aTop motionLoop
            L_37df: pToa onApron
            not
            bnt L_3805
            pTos location
            ldi 5
            eq?
            bnt L_37f2
            lst 2
            ldi 28
            eq?
            bt L_3800
            L_37f2: pTos location
            ldi 6
            eq?
            bnt L_3805
            lst 2
            ldi 29
            eq?
            bnt L_3805
            L_3800: ldi 0
            aTop motionLoop
            L_3805: pTos location
            ldi 6
            eq?
            bnt L_381d
            pToa onApron
            not
            bnt L_381d
            lst 2
            ldi 30
            eq?
            bnt L_381d
            ldi 0
            aTop motionLoop
            L_381d: pToa location
            sat 0
            pToa onApron
            sat 1
            pushi 54
            pushi 3
            lsp 1
            lsp 2
            lsp 3
            self 10
            pushi 111
            push0
            self 4
            pushi 259
            push0
            self 4
            ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x3842; 132 original instructions
    (method (uiHostAct arg1 arg2 arg3 &tmp t0 t1 t2)
(if ((ScriptID 996 0) h14Frame: 3) (return 0))

(if ((ScriptID 995 0) h13Frame: 3) (return 0))

(if ((ScriptID 994 0) h12Frame: 3) (return 0))

(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)

(if ((ScriptID 993 0) h11Frame: 3) (return 0))

(if ((ScriptID 992 0) h10Frame: 3) (return 0))

(if ((ScriptID 992 0) h10Stop: arg2 arg3) (return 0))
(if (and p08 (p08 h8VI: 1 arg1 arg2 arg3)) (return 0))

(if (and p08 (p08 h8ActionBarrier:)) (return 0))

(if (and p07 (p07 h7Barrier:)) (return 0))

(if (and p06 (p06 h6Barrier:)) (return 0))

(if p05 (if (p05 hBarrier:) (return 0))) (if p05 (p05 hCaptureTarget: (if arg3 arg3 else arg2)))

        (if p04Invalid (return 0))
        (asm
            pToa p03Invalid
            bnt L_384b
            ldi 0
            ret
            L_384b: pushi 377
            push0
            self 4
            pushi 133
            push0
            self 4
            lap 3
            bnt L_385f
            lap 3
            jmp L_3861
            L_385f: lap 2
            L_3861: sat 0
            lsp 1
            ldi 0
            eq?
            bnt L_3878
            pushi 551
            push1
            lst 0
            self 6
            bnt L_3878
            ldi 5
            sap 1
            L_3878: lsp 1
            ldi 0
            eq?
            bnt L_38b8
            pushi 189
            push1
            lsp 2
            self 6
            push
            ldi -1
            eq?
            bnt L_38b8
            lsp 2
            ldi 9
            ne?
            bnt L_38b8
            lsp 2
            ldi 11
            ne?
            bnt L_38b8
            pushi 142
            pushi 5
            pushi 12
            push1
            lsp 2
            self 6
            push
            pushi 13
            push1
            lsp 2
            self 6
            push
            push0
            push0
            push0
            self 14
            ldi 0
            ret
            L_38b8: pushi 551
            push1
            lst 0
            self 6
            bt L_38c9
            lst 0
            ldi 32
            eq?
            bnt L_38d8
            L_38c9: pushi 109
            pushi 3
            lsp 1
            lsp 2
            lsp 3
            self 10
            ldi 0
            ret
            L_38d8: pushi 552
            push1
            lst 0
            self 6
            not
            bnt L_38f2
            pushi 109
            pushi 3
            lsp 1
            lsp 2
            lsp 3
            self 10
            ldi 0
            ret
            L_38f2: pushi 12
            push1
            lst 0
            self 6
            sat 1
            pushi 13
            push1
            lst 0
            self 6
            sat 2
            lsp 1
            ldi 0
            eq?
            bnt L_3921
            lsp 2
            ldi 1
            eq?
            bnt L_3921
            pTos location
            ldi 0
            eq?
            bnt L_3921
            pToa doorOpen
            bnt L_3921
            ldi 115
            sat 2
            L_3921: pushi 142
            pushi 5
            lst 1
            lst 2
            lsp 1
            lsp 2
            lsp 3
            self 14
            ret
        )
    )

    ; Delivered offset0x3933; 52 original instructions
    (method (roomTitle)
 (return ((ScriptID 991 0) roomTitle: self)))

    ; Delivered offset0x398c; 106 original instructions
    (method (blockPerson px py color label)
 (return ((ScriptID 991 0) blockPerson: self px py color label)))

    ; Delivered offset0x3a36; 399 original instructions
    (method (drawBlockout &tmp t0 t1 t2 t3 t4 t5)
        (asm
            pushi 9
            pushi 11
            pushi 43
            push0
            pushi 116
            pushi 288
            push1
            pushi 8
            push0
            push0
            callk Graph, 18
            pushi 9
            pushi 11
            pushi 116
            push0
            pushi 144
            pushi 320
            push1
            pushi 9
            push0
            push0
            callk Graph, 18
            pushi 9
            pushi 11
            pushi 43
            pushi 286
            pushi 144
            pushi 289
            push1
            pushi 3
            push0
            push0
            callk Graph, 18
            pushi 11
            lofss "ROOM ART BLOCKOUT"
            pushi 100
            pushi 6
            pushi 44
            pushi 102
            push0
            pushi 105
            push0
            pushi 106
            pushi 170
            pushi 121
            callk Display, 22
            pTos location
            dup
            ldi 1
            eq?
            bnt L_3b6b
            pushi 9
            pushi 11
            pushi 53
            pushi 115
            pushi 95
            pushi 216
            push1
            pushi 4
            push0
            push0
            callk Graph, 18
            pushi 53
            pushi 4
            pushi 199
            pushi 116
            push2
            lofss "FRANKIE"
            self 12
            pushi 53
            pushi 4
            pushi 94
            pushi 116
            pushi 208
            lofss "BUNNY"
            self 12
            pushi 53
            pushi 4
            pushi 231
            pushi 112
            pushi 6
            lofss "RITA"
            self 12
            pushi 11
            lofss "PLAN BOARD"
            pushi 100
            pushi 125
            pushi 61
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 84
            pushi 121
            callk Display, 22
            pToa p02BoardRecords
            bnt L_3b4d
            pushi 9
            pushi 11
            pushi 80
            pushi 125
            pushi 91
            pushi 151
            push1
            push1
            push0
            push0
            callk Graph, 18
            pTos p02BoardRecords
            ldi 2
            and
            bnt L_3b30
            pushi 9
            pushi 11
            pushi 80
            pushi 153
            pushi 91
            pushi 179
            push1
            push1
            push0
            push0
            callk Graph, 18
            L_3b30: pTos p02BoardRecords
            ldi 4
            and
            bnt L_3b4d
            pushi 9
            pushi 11
            pushi 80
            pushi 181
            pushi 91
            pushi 207
            push1
            push1
            push0
            push0
            callk Graph, 18
            L_3b4d: pTos p02CopyBunny
            ldi 1
            eq?
            bnt L_3b68
            pushi 9
            pushi 11
            pushi 78
            pushi 84
            pushi 89
            pushi 103
            push1
            push1
            push0
            push0
            callk Graph, 18
            L_3b68: jmp L_3cb7
            L_3b6b: dup
            ldi 2
            eq?
            bnt L_3bbd
            pushi 9
            pushi 11
            pushi 83
            pushi 108
            pushi 112
            pushi 241
            push1
            pushi 4
            push0
            push0
            callk Graph, 18
            pTos tray
            ldi 2
            eq?
            bnt L_3b9f
            pushi 7
            pushi 212
            push0
            push0
            pushi 135
            pushi 85
            pushi -1
            push0
            callk DrawCel, 14
            L_3b9f: pushi 11
            lofss "KITCHEN PASS"
            pushi 100
            pushi 111
            pushi 69
            pushi 102
            push0
            pushi 105
            push0
            pushi 106
            pushi 145
            pushi 121
            callk Display, 22
            jmp L_3cb7
            L_3bbd: dup
            ldi 3
            eq?
            bnt L_3be1
            pushi 11
            lofss "HOUSE SIDE / COURTYARD GATE"
            pushi 100
            pushi 44
            pushi 59
            pushi 102
            push0
            pushi 105
            push0
            pushi 106
            pushi 237
            pushi 121
            callk Display, 22
            jmp L_3cb7
            L_3be1: dup
            ldi 4
            eq?
            bnt L_3c05
            pushi 11
            lofss "COURTYARD / PREPARATION TO FOLLOW"
            pushi 100
            pushi 41
            pushi 59
            pushi 102
            push0
            pushi 105
            push0
            pushi 106
            pushi 242
            pushi 121
            callk Display, 22
            jmp L_3cb7
            L_3c05: dup
            ldi 5
            eq?
            bnt L_3c70
            pushi 422
            push1
            pushi 5
            self 6
            pushi 9
            pushi 11
            pushi 80
            pushi 171
            pushi 113
            pushi 230
            push1
            pushi 3
            push0
            push0
            callk Graph, 18
            pushi 9
            pushi 11
            pushi 84
            pushi 177
            pushi 104
            pushi 223
            push1
            pToa p02DrawerOpen
            bnt L_3c41
            ldi 0
            jmp L_3c43
            L_3c41: ldi 9
            L_3c43: push
            push0
            push0
            callk Graph, 18
            pToa p02DrawerOpen
            bnt L_3c6e
            pToa p02MiloShown
            bnt L_3c6e
            pToa p02MasterHeld
            not
            bnt L_3c6e
            pushi 9
            pushi 11
            pushi 85
            pushi 190
            pushi 98
            pushi 211
            push1
            push1
            push0
            push0
            callk Graph, 18
            L_3c6e: jmp L_3cb7
            L_3c70: dup
            ldi 6
            eq?
            bnt L_3cb7
            pushi 422
            push1
            pushi 4
            self 6
            pushi 9
            pushi 11
            pushi 101
            pushi 192
            pushi 112
            pushi 226
            push1
            pushi 3
            push0
            push0
            callk Graph, 18
            pTos p02CopyStringer
            ldi 6
            eq?
            bnt L_3cb1
            pushi 9
            pushi 11
            pushi 87
            pushi 196
            pushi 99
            pushi 218
            push1
            push1
            push0
            push0
            callk Graph, 18
            L_3cb1: pushi 555
            push0
            self 4
            L_3cb7: toss
            ldi 0
            aTop uiControlCount
            pushi 311
            push0
            self 4
            ldi 0
            sat 0
            L_3cc7: lst 0
            pToa uiControlCount
            lt?
            bnt L_3d40
            lat 0
            lali 228
            sat 1
            lst 1
            ldi 12
            ge?
            bnt L_3d3c
            lst 1
            ldi 19
            le?
            bnt L_3d3c
            lat 0
            lali 292
            sat 3
            lat 0
            lali 356
            sat 2
            lat 0
            lali 420
            sat 5
            lat 0
            lali 484
            sat 4
            pushi 294
            pushi 5
            lst 3
            lst 2
            lst 5
            lst 4
            push1
            self 14
            pushi 11
            lat 0
            lsli 548
            pushi 100
            lst 2
            ldi 2
            add
            push
            lst 3
            ldi 2
            add
            push
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            lst 4
            lat 2
            sub
            push
            ldi 4
            sub
            push
            pushi 121
            callk Display, 22
            L_3d3c: +at 0
            jmp L_3cc7
            L_3d40: ldi 0
            aTop uiControlCount
            ret
        )
    )

    ; Delivered offset0x3d46; 348 original instructions
    (method (drawWorld)
(if (and p08 (>= (p08 h8V: 1 0) 5)) (if p09 (return (p09 h9Draw:)) else (p08 h8VD:) (return 1)))

(if (and p08 (> (p08 h8V: 1 0) 0) (< (p08 h8V: 1 0) 5)) (p08 h8VD:) (return 1))

(if (and p08 (p08 h8RouteBusy:)) (p08 h8RouteRender:) (return 1))
 (self h6BaseDrawWorld: ) (if p06 (p06 h6Render:)) (if (and p08 (p08 h8RouteMeeting:)) (p08 h8RouteRender:)) (return 1)
)

    ; Delivered offset0x3fd9; 14 original instructions
    (method (uiHostMenu)
((ScriptID 996 0) h14Retire:)

((ScriptID 995 0) h13Retire:)
((ScriptID 995 0) h13Cancel:)

((ScriptID 994 0) h12SuccessorCancel:)

((ScriptID 993 0) h11PayDrop:)

(if p07 (p07 h7RetireLaugh:))

(if p05 (p05 hStageRetire:)) 

        (asm
            pushi 560
            push0
            self 4
            pushi 377
            push0
            self 4
            ldi 1
            aTop menuOpen
            pushi 259
            push0
            self 4
            ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x3ff5; 4 original instructions
    (method (uiHostSaveRequested) (self writeSave:))

    ; Delivered offset0x3ffc; 4 original instructions
    (method (uiHostLoadRequested) (self readSave:))

    ; Delivered offset0x4003; 84 original instructions
    (method (hostTrace label &tmp file [filename 32] [line 300])
        (Format @filename "p02state%04d.csv" traceIndex)
        (while (FileIO 10 @filename) (++ traceIndex) (Format @filename "p02state%04d.csv" traceIndex))
        (Format @line "%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n"
            label (GetTime) location onApron tray wedge doorOpen houseEntered p02Revision
            p02CopyJack p02CopyBunny p02CopyStringer p02Compared p02MiloShown p02MasterHeld
            p02KnowPurpose p02KnowOrder p02SelectedAims p02PlanAgreed p02InventoryExtent
            uiPanel uiDocument uiPage bridgeVisitedCount bridgeReadSerial motionPhase
            (/ motionX 64) (/ motionY 64))
        (= file (FileIO 0 @filename 2))
        (if (!= file -1) (FileIO 6 file @line) (FileIO 1 file)))

    ; Delivered offset0x40c1; 29 original instructions
    (method (hostObserve)
(if (and p05 (p05 hFailure?)) (return 0)) 

        (if (or (!= observedRevision p02Revision) (!= observedRoom location)
            (!= observedApron onApron) (!= observedReadSerial bridgeReadSerial))
            (self hostTrace: "state")
            (= observedRevision p02Revision) (= observedRoom location)
            (= observedApron onApron) (= observedReadSerial bridgeReadSerial)))

    ; Delivered offset0x4102; 52 original instructions
    (method (menuChoice choice)
        (switch choice
            (1 (self writeSave:)) (2 (self readSave:)) (3 (self startReplay:))
            (4 (= menuOpen 0) (= paused 0)) (5 (= quitRequested 1))
            (6 (= audienceMuted (not audienceMuted))))
        (= dirty 1))

    ; Delivered offset0x415c; 58 original instructions
    (method (uiHostReaderControls &tmp obj owner)
        ; The packet is already held, but its contained original needs an
        ; explicit Pick-up action. Reading never silently grants the item.
        (if (or (!= uiPanel 1) (not (self p02Available:)) onApron) (return 0))
        (for ((= obj 20)) (<= obj 22) ((++ obj))
            (= owner (self p02CopyOwner: obj))
            (if (and (== uiDocument (self bridgeObjectDocument: obj))
                (self p02Reachable: obj) (or (== owner 13) (== owner location)))
                (self uiAddControl: 15 obj 164 174 176 304 "TAKE THIS COPY"))))

    ; Delivered offset0x41cf; 19 original instructions
    (method (uiHostTakeReader obj)
        ; Revalidate at activation; repeated clicks cannot duplicate a copy.
        (if (or (< obj 20) (> obj 22)) (return 0))
        (self bridgeActAtArrival: 4 obj 0)
        (= dirty 1))

    ; Delivered offset0x41f1; 34 original instructions
    (method (p02Init &tmp i)
        (if p02Initialized (return 0))
        (= p02Initialized 1)
        (for ((= i 0)) (< i 64) ((++ i)) (= [p02Slots i] 0))
        (for ((= i 0)) (< i 33) ((++ i)) (= [p02Reserved i] -1))
        (= [p02Slots 0] 5) (= [p02Slots 1] 6)
    )

    ; Delivered offset0x4236; 4 original instructions
    (method (p02Available) (return (and traySafe houseEntered)))

    ; Delivered offset0x423d; 6 original instructions
    (method (p02Phase) (return (if p02PlanAgreed 2 else 1)))

    ; Delivered offset0x4249; 24 original instructions
    (method (p02CopyOwner obj)
        (switch obj (20 (return p02CopyJack)) (21 (return p02CopyBunny)) (22 (return p02CopyStringer)))
        (return -1))

    ; Delivered offset0x4271; 23 original instructions
    (method (p02SetCopyOwner obj owner)
        (switch obj (20 (= p02CopyJack owner)) (21 (= p02CopyBunny owner)) (22 (= p02CopyStringer owner))))

    ; Delivered offset0x429a; 45 original instructions
    (method (p02Bit obj)
        (switch obj (20 (return 1)) (21 (return 2)) (22 (return 4))
            (24 (return 8)) (26 (return 16)) (33 (return 32)))
        (return 0))

    ; Delivered offset0x42e0; 86 original instructions
    (method (p02Held obj)
        (if (self p04Reserved: obj) (return 0))
        (switch obj
            (4 (return (== wedge 1))) (5 (return (== tray 0))) (6 (return 1))
            (20 (return (== p02CopyJack 10))) (21 (return (== p02CopyBunny 10)))
            (22 (return (== p02CopyStringer 10)))
            (23 (return (and (== p02CopyJack 12) (== p02CopyBunny 12) (== p02CopyStringer 12))))
            (24 (return p02MasterHeld)) (25 (return p02PlanAgreed)))
        (return 0))

    ; Delivered offset0x436f; 151 original instructions
    (method (p02ObjectLocation obj &tmp h10Answer owner)
(if ((ScriptID 996 0) h14Owns: obj) (return ((ScriptID 996 0) h14Location: obj)))

(if ((ScriptID 995 0) h13Owns: obj) (return ((ScriptID 995 0) h13Location: obj)))

(if ((ScriptID 994 0) h12SuccessorHas: obj) (return ((ScriptID 994 0) h12SuccessorRoom: obj)))

(if ((ScriptID 993 0) h11OwnerHas: obj) (return ((ScriptID 993 0) h11OwnerQ: 2 obj)))

(= h10Answer ((ScriptID 992 0) h10Q: 2 obj)) (if (!= h10Answer -2) (return h10Answer))
(if (and p08 (or (== obj 29) (== obj 30))) (return (p08 h8ActorRoom: (if (== obj 29) 4 else 7))))

(if (== obj 399) (return (if (and p09 (p09 h9CardHeld: obj)) 10 else -1)))
(if (and (>= obj 395) (<= obj 399)) (return -1))

(if (and p06 (== obj 8)) (return (p06 h6FrankieRoom?)))

(if (and p08 (p08 h8LayoutTarget: obj)) (return 4))

(if (and p08 (p08 h8OwnedNative: obj)) (return (p08 h8NativeLocation: obj)))

(if (and p07 (>= obj 86) (<= obj 94)) (return (p07 h7Location: obj)))

(if (and p06 (>= obj 73) (<= obj 85)) (return (p06 h6Location: obj)))

(if (and p05 (or (and p02PlanAgreed (or (== obj 2) (== obj 28))) (and (>= obj 63) (<= obj 72)))) (return (p05 hLocation: obj)))

        (if (self p04Reserved: obj) (return -1))
        (if (and (>= obj 20) (<= obj 22)) (return (self p02CopyOwner: obj)))
        (if (self p02Held: obj) (return 10))
        (switch obj
            (1 (return 17)) (2 (return (if (self p02Available:) 1 else 0)))
            (3 (return 0)) (4 (return (if (== wedge 2) 19 else 18)))
            (5 (return (if (== tray 1) 0 else 2)))
            (7 (return 1)) (8 (return 1)) (24 (return 15)) (26 (return 1))
            (27 (return 5)) (28 (return 5)) (29 (return 6)) (30 (return 6))
            (31 (return (if p02PlanAgreed 1 else -1))) (32 (return 16)))
        (return -1))

    ; Delivered offset0x446d; 151 original instructions
    (method (p02Exit obj)
        (switch location
            (0 (switch obj (1 (return 1)) (18 (return 1)) (14 (return 3)) (15 (return 5)) (16 (return 6))))
            (1 (switch obj (1 (return 0)) (17 (return 0)) (12 (return 2)) (13 (return 4))))
            (2 (if (== obj 18) (return 1)))
            (3 (switch obj (17 (return 0)) (19 (return 4))))
            (4 (switch obj (18 (return 1)) (19 (return 3))))
            (5 (if (== obj 17) (return 0)))
            (6 (if (== obj 17) (return 0))))
        (return -1))

    ; Delivered offset0x455b; 111 original instructions
    (method (p02Reachable obj &tmp owner)
        (if (self p04Reserved: obj) (return 0))
        (if onApron (return (or (== obj 10) (== obj 11) (== obj 32))))
        (if (or (== obj 9) (== obj 32) (!= (self p02Exit: obj) -1)) (return 1))
        (= owner (self p02ObjectLocation: obj))
        (if (or (== owner 10) (== owner location) (== owner 13)) (return 1))
        (if (or (== owner 17) (== owner 19)) (return (or (== location 0) (== location 1))))
        (if (== owner 18) (return (== location 0)))
        (if (or (== owner 11) (== owner 14)) (return (== location 1)))
        (if (== owner 12) (return (self p02Held: 23)))
        (if (== owner 15) (return (and (== location 5) p02DrawerOpen p02MiloShown)))
        (return 0))

    ; Delivered offset0x461c; 13 original instructions
    (method (p02InventoryItem index)
        (if (or (< index 0) (>= index p02InventoryExtent)) (return 0))
        (return [p02Slots index]))

    ; Delivered offset0x4634; 11 original instructions
    (method (p02InventoryPages) (return (if p02InventoryExtent (/ (+ p02InventoryExtent 7) 8) else 1)))

    ; Delivered offset0x4648; 18 original instructions
    (method (p02FindSlot obj &tmp i)
        (for ((= i 0)) (< i p02InventoryExtent) ((++ i))
            (if (== [p02Slots i] obj) (return i)))
        (return -1))

    ; Delivered offset0x466a; 311 original instructions
    (method (p02SyncInventory compact &tmp i j obj first slot)
(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)

        (= first -1)
        (if (>= p02GapJack 0) (= first p02GapJack))
        (if (and (>= p02GapBunny 0) (or (== first -1) (< p02GapBunny first))) (= first p02GapBunny))
        (if (and (>= p02GapStringer 0) (or (== first -1) (< p02GapStringer first))) (= first p02GapStringer))
        (for ((= i 0)) (< i p02InventoryExtent) ((++ i))
            (= obj [p02Slots i])
            (if (or (< obj 0) (> obj 32)) (= p02InventoryOverflow 1) (return 0))
            (if (and (>= obj 20) (<= obj 22))
                (if (or (== first -1) (< i first)) (= first i))
                (if (== (self p02CopyOwner: obj) 11)
                    (switch obj (20 (= p02GapJack i)) (21 (= p02GapBunny i)) (22 (= p02GapStringer i)))))
            (if (and obj (not (self p02Held: obj)))
                (= [p02Reserved obj] i) (= [p02Slots i] 0)))
        ; Explicit canonical held-item order: tray, packet, wedge, copies, bundle, master, pencil.
        (for ((= j 0)) (< j 9) ((++ j))
            (switch j (0 (= obj 5)) (1 (= obj 6)) (2 (= obj 4)) (3 (= obj 20))
                (4 (= obj 21)) (5 (= obj 22)) (6 (= obj 23)) (7 (= obj 24)) (8 (= obj 25)))
            (if (and (self p02Held: obj) (== (self p02FindSlot: obj) -1))
                (if (and (== obj 23) (>= first 0)) (= [p02Slots first] obj)
                else
                    (if (>= [p02Reserved obj] 0)
                        (= slot [p02Reserved obj]) (= [p02Slots slot] obj)
                    else
                        ; Valid P02 play has at most nine distinct physical items.
                        ; This defensive branch only detects corrupt/unvalidated state.
                        (if (>= p02InventoryExtent 64) (= p02InventoryOverflow 1) (return 0))
                        (= [p02Slots p02InventoryExtent] obj) (++ p02InventoryExtent))))
            (if (self p02Held: obj) (= [p02Reserved obj] -1)))
        (if (self p02Held: 23) (= [p02Reserved 20] -1) (= [p02Reserved 21] -1) (= [p02Reserved 22] -1))
        (if (or compact (self p02Held: 23)) (= p02GapJack -1) (= p02GapBunny -1) (= p02GapStringer -1))
        (if compact
            (for ((= i 0)) (< i 33) ((++ i)) (= [p02Reserved i] -1))
            (= j 0)
            (for ((= i 0)) (< i p02InventoryExtent) ((++ i))
                (if [p02Slots i] (= [p02Slots j] [p02Slots i]) (++ j)))
            (for ((= i j)) (< i p02InventoryExtent) ((++ i)) (= [p02Slots i] 0))
            (= p02InventoryExtent j))
        (self p02HostInventory:))

    ; Delivered offset0x48cb; 12 original instructions
    (method (p02Commit eventId arg1 arg2)
        (self p02SyncInventory: 0) (++ p02Revision)
        (self p02HostEvent: eventId arg1 arg2))

    ; Delivered offset0x48e3; 6 original instructions
    (method (p02Blocked obj) (self p02HostText: 108 obj))

    ; Delivered offset0x48ee; 2 original instructions
    (method (p02LegacyObject obj)
        (return obj))

    ; Delivered offset0x48f1; 126 original instructions
    (method (p02Delegate action obj target &tmp oldRoom oldTray oldWedge oldDoor oldBunny oldP01 oldA01 oldGreeting eventId h11Revision)
        (if (or (self p04Reserved: obj) (self p04Reserved: target)) (self p02Blocked: 4) (return 0))
        (= oldRoom location) (= oldTray tray) (= oldWedge wedge) (= oldDoor doorOpen)
        (= oldBunny bunnyReady) (= oldP01 p01Consumed) (= oldA01 a01Consumed) (= oldGreeting greetingConsumed)
        (= h11Revision p02Revision)
        (if (and (== action 0) (== obj 1))
          (if (not ((ScriptID 993 0) h11TravelArm: oldRoom obj h11Revision)) (return 0)))
        (self p02HostP01Act: action (self p02LegacyObject: obj) (self p02LegacyObject: target))
        (= eventId 0)
        (if (!= oldRoom location) (= eventId (+ 1 location))
        else
            (if (!= oldGreeting greetingConsumed) (= eventId 5)
            else
                (if (!= oldA01 a01Consumed) (= eventId 4)
                else
                    (if (!= oldBunny bunnyReady) (= eventId 8)
                    else
                        (if (!= oldTray tray) (= eventId (if (== tray 1) 9 else 10))
                        else
                            (if (!= oldWedge wedge) (= eventId (if (== wedge 1) 11 else 12))
                            else (if (!= oldDoor doorOpen) (= eventId (if doorOpen 13 else 14)))))))))
        (if (!= oldRoom location)
          (++ p02Revision)
          (if (not ((ScriptID 993 0) h11TravelDone: oldRoom obj h11Revision)) (= uiFailure 10) (return 0)))
        (self p02SyncInventory: (!= oldRoom location))
        (if eventId
            (if (== oldRoom location) (++ p02Revision)) (self p02HostEvent: eventId location 0)
            (if (!= oldP01 p01Consumed) (self p02HostEvent: 3 0 0))))

    ; Delivered offset0x49dd; 136 original instructions
    (method (p02Walk obj &tmp destination routeFrom routeRevision)
        (if (and p04 (== obj 19) (or (== location 3) (== location 4))
            (!= (p04 p04Gate?) 1))
            (self uiOpenInline: (self p04Label: 60) (self p04Label: 60)) (return 0))
        (if (and (== obj 9) (not onApron))
            (= onApron 1) (= p02PlanOpen 0)
            (self p02Commit: 6 location 1) (self p02HostText: 129 0) (return 0))
        (if (and (== obj 11) onApron)
            (= onApron 0) (self p02Commit: 7 location 0)
            (self p02HostText: 130 0) (return 0))
        (if onApron (self p02HostText: 131 0) (return 0))
        (= destination (self p02Exit: obj))
        (if (== destination -1) (self p02HostText: 132 0) (return 0))
        (if (and (or (== location 0) (== location 1)) (or (== destination 0) (== destination 1)))
            (= p02PlanOpen 0) (self p02Delegate: 0 1 0) (return 0))
        (if (not (self p02Available:)) (self p02HostText: 133 0) (return 0))
        (= routeFrom location) (= routeRevision p02Revision)
        (if (not ((ScriptID 993 0) h11TravelArm: routeFrom obj routeRevision)) (return 0))
        (if p08 (p08 h8RouteArm: routeFrom obj routeRevision)) (= location destination) (= p02PlanOpen 0)
        (++ p02Revision)
        (if (not ((ScriptID 993 0) h11TravelDone: routeFrom obj routeRevision)) (= uiFailure 10) (return 0))
        (self p02SyncInventory: 1)
        (self p02HostEvent: (+ 20 location) location (self p02Phase:))
        (if p08 (p08 h8RouteTravel: routeFrom obj routeRevision))
(self p02HostText: 134 location))

    ; Delivered offset0x4add; 59 original instructions
    (method (p02DocumentAvailable obj record)
        (if (not (self p02Available:)) (return 0))
        (if (not (or (and (>= obj 20) (<= obj 22)) (== obj 24) (== obj 31))) (return 0))
        (if record (return (or (& p02Observed (self p02Bit: obj)) (and (== obj 31) p02PlanAgreed))))
        (if (or onApron (not (self p02Reachable: obj))) (return 0))
        (if (== obj 24) (return p02MasterHeld))
        (return 1))

    ; Delivered offset0x4b46; 59 original instructions
    (method (p02Read obj record &tmp bit)
        (if (not (self p02DocumentAvailable: obj record))
            (self p02HostText: 105 obj) (return 0))
        (= bit (self p02Bit: obj))
        (if (and (not record) (!= obj 31) (not (& p02Observed bit)))
            (= p02Observed (| p02Observed bit))
            (if (== obj 24) (= p02KnowPurpose 1) (= p02KnowOrder 1))
            (self p02Commit: (+ 100 obj) obj 1))
        (self p02HostDocument: obj record))

    ; Delivered offset0x4bb6; 120 original instructions
    (method (p02Collect obj &tmp owner)
        (if (or (< obj 20) (> obj 22) (not (self p02Available:)) onApron (not (self p02Reachable: obj)))
            (self p02Blocked: obj) (return 0))
        (= owner (self p02CopyOwner: obj))
        (if (== owner 10) (self p02HostText: 136 obj) (return 0))
        (if (or (== owner 11) (== owner 12) (== owner 14))
            (self p02HostText: 83 obj) (return 0))
        (if (!= obj 20) (= p02Permissions (| p02Permissions (self p02Bit: obj))))
        (self p02SetCopyOwner: obj 10) (self p02Commit: (+ 200 obj) obj 0)
        (switch obj
            (20 (self p02HostText: 137 0))
            (21 (self p02HostText: 138 0))
            (22 (self p02HostText: 139 0))))

    ; Delivered offset0x4c93; 75 original instructions
    (method (p02Place obj &tmp bit)
        (if (or (< obj 20) (> obj 22) (not (self p02Available:)) onApron (!= location 1))
            (self p02HostText: 135 obj) (return 0))
        (if (!= (self p02CopyOwner: obj) 10) (self p02HostText: 84 obj) (return 0))
        (= bit (self p02Bit: obj)) (self p02SetCopyOwner: obj 11)
        (= p02BoardRecords (| p02BoardRecords bit)) (= p02Observed (| p02Observed bit))
        (self p02Commit: (+ 300 obj) obj 0)
        (self p02HostDocument: obj 0))

    ; Delivered offset0x4d21; 70 original instructions
    (method (p02Compare)
        (if (or (not (self p02Available:)) onApron (!= location 1)) (self p02Blocked: 26) (return 0))
        (if p02Compared (self p02HostExchange: 7) (return 0))
        (if (not (and (== p02CopyJack 11) (== p02CopyBunny 11) (== p02CopyStringer 11)))
            (self p02HostText: 33 p02BoardRecords) (return 0))
        (= p02Compared 1) (= p02Observed (| p02Observed 16))
        (= p02CopyJack 12) (= p02CopyBunny 12) (= p02CopyStringer 12)
        (= p02ComparisonConsumed 1) (self p02Commit: 400 26 1)
        (self p02HostExchange: 6))

    ; Delivered offset0x4daf; 60 original instructions
    (method (p02ShowMilo)
        (if (or (not (self p02Available:)) onApron (!= location 5)) (self p02Blocked: 28) (return 0))
        (if p02MiloShown
            (self p02HostExchange: (if p02MasterHeld 26 else 9)) (return 0))
        (if (not (and (self p02Held: 23) p02Compared))
            (self p02HostText: 87 0) (return 0))
        (= p02MiloShown 1) (= p02DrawerOpen 1)
        (self p02Commit: 401 1 10) (self p02HostExchange: 8))

    ; Delivered offset0x4e24; 52 original instructions
    (method (p02Drawer desired)
        (if (or (not (self p02Available:)) onApron (!= location 5)) (self p02Blocked: 27) (return 0))
        (if (not p02MiloShown) (self p02HostText: 90 0) (return 0))
        (if (== p02DrawerOpen desired) (self p02HostText: 140 desired) (return 0))
        (= p02DrawerOpen desired) (self p02Commit: 402 desired 0)
        (self p02HostText: 141 desired))

    ; Delivered offset0x4e89; 59 original instructions
    (method (p02TakeMaster)
        (if (or (not (self p02Available:)) onApron (not (self p02Reachable: 24))) (self p02Blocked: 24) (return 0))
        (if p02MasterHeld (self p02HostText: 93 0) (return 0))
        (if (or (not p02MiloShown) (not p02DrawerOpen) (!= location 5))
            (self p02HostText: 90 0) (return 0))
        (= p02MasterHeld 1) (self p02Commit: 403 24 0)
        (self p02HostText: 92 0))

    ; Delivered offset0x4ef8; 62 original instructions
    (method (p02TopicAvailable actor topic)
        (if (or (not (self p02Available:)) onApron (not (self p02Reachable: actor))) (return 0))
        (switch actor
            (2 (return (and (>= topic 1) (<= topic 3))))
            (29 (return (and (>= topic 4) (<= topic 7))))
            (8 (return (== topic 8))) (28 (return (== topic 9))))
        (return 0))

    ; Delivered offset0x4f5d; 184 original instructions
    (method (p02Topic actor topic &tmp obj bit exchange)
        (if (not (self p02TopicAvailable: actor topic)) (self p02Blocked: actor) (return 0))
        (if (and (>= topic 1) (<= topic 6))
            (= obj (if (<= topic 3) 21 else 22)) (= bit (self p02Bit: obj))
            (if (or (== topic 2) (== topic 5))
                (if (not (& p02Permissions bit))
                    (= p02Permissions (| p02Permissions bit)) (self p02Commit: (+ 410 actor) obj 0))
            else
                (if (not (& p02Observed bit))
                    (= p02Observed (| p02Observed bit)) (self p02Commit: (+ 100 obj) obj 0))))
        (if (and (== topic 7) (not (& p02Observed 32)))
            (= p02Observed (| p02Observed 32)) (self p02Commit: 440 33 0))
        (switch topic
            (1 (= exchange 16)) (2 (= exchange 17)) (3 (= exchange 18))
            (4 (= exchange 19)) (5 (= exchange 20)) (6 (= exchange 21))
            (7 (= exchange 22))
            (8 (= exchange (if p02PlanAgreed 13 else (if p02KnowPurpose 11 else 23))))
            (9 (= exchange (if p02MiloShown (if p02MasterHeld 26 else 9) else 24))))
        (self p02HostExchange: exchange))

    ; Delivered offset0x50b4; 50 original instructions
    (method (p02OpenTopics actor &tmp topic)
        (= topic 0)
        (switch actor (2 (= topic 1)) (29 (= topic 4)) (8 (= topic 8)) (28 (= topic 9)))
        (if (not (self p02TopicAvailable: actor topic)) (self p02Blocked: actor) (return 0))
        (self p02HostTopics: actor))

    ; Delivered offset0x510c; 68 original instructions
    (method (p02BeginPlan &tmp exchange)
        (if (or onApron (!= location 1)) (self p02Blocked: 7) (return 0))
        (if p02PlanAgreed (self p02HostExchange: 13) (return 0))
        (if (not (and p02MasterHeld p02KnowPurpose))
            (self p02HostText: 94 0) (return 0))
        (if p02PlanOpen (self p02HostExchange: 11) (self p02HostPlan:) (return 0))
        (= exchange (if p02PlanStarted 11 else 10))
        (= p02PlanStarted 1) (= p02PlanOpen 1) (self p02Commit: 450 0 0)
        (self p02HostExchange: exchange) (self p02HostPlan:))

    ; Delivered offset0x5193; 24 original instructions
    (method (p02CancelPlan)
        (if (not p02PlanOpen) (self p02HostText: 102 0) (return 0))
        (= p02PlanOpen 0) (self p02Commit: 451 0 0)
        (self p02HostText: 102 0))

    ; Delivered offset0x51c0; 24 original instructions
    (method (p02AimBit aim)
        (switch aim (1 (return 1)) (2 (return 2)) (3 (return 4))) (return 0))

    ; Delivered offset0x51e5; 11 original instructions
    (method (p02AimSelected aim) (return (if (& p02SelectedAims (self p02AimBit: aim)) 1 else 0)))

    ; Delivered offset0x51fa; 104 original instructions
    (method (p02SelectAim aim desired &tmp bit current)
        (if (or (< aim 1) (> aim 5) (< desired 0) (> desired 1)) (return -1))
        (if (or (not p02PlanOpen) onApron (!= location 1))
            (self p02HostText: 96 0) (return 0))
        (if (== aim 4) (self p02HostExchange: 14) (return 0))
        (if (== aim 5) (self p02HostExchange: 15) (return 0))
        (= bit (self p02AimBit: aim)) (= current (self p02AimSelected: aim))
        (if (== current desired) (self p02HostText: 142 aim) (return 0))
        (if desired (= p02SelectedAims (| p02SelectedAims bit)) else (= p02SelectedAims (- p02SelectedAims bit)))
        (self p02Commit: 452 aim desired)
        (self p02HostText: (if desired 52 else 53) aim))

    ; Delivered offset0x52bf; 64 original instructions
    (method (p02ConfirmPlan)
        (if (or onApron (!= location 1)) (self p02Blocked: 7) (return 0))
        (if p02PlanAgreed (self p02HostExchange: 13) (return 0))
        (if (not p02PlanOpen) (self p02HostText: 96 0) (return 0))
        (if (!= p02SelectedAims 7) (self p02HostText: 56 p02SelectedAims) (return 0))
        (= p02PlanAgreed 1) (= p02CopyJack 14) (= p02CopyBunny 14) (= p02CopyStringer 14)
        (= p02PlanOpen 0) (= p02CompleteConsumed 1)
        (self p02Commit: 453 25 31) (self p02HostExchange: 12))

    ; Delivered offset0x5342; 59 original instructions
    (method (p02Hint requested)
(if (and p08 (p08 h8ActionBarrier:)) (return 0))

(if (and p05 (p05 hBarrier:)) (return 0))

        (if (or (< requested 0) (> requested 3)) (return -1))
        (if (not (self p02Available:)) (self p02HostText: 143 0) (return 0))
        (if (== requested 0) (= requested (+ p02HintLevel 1)) (if (> requested 3) (= requested 3)))
        (if (> requested p02HintLevel) (= p02HintLevel requested) (self p02Commit: 454 requested 0))
        (self p02HostText: (+ 113 (- requested 1)) p02PlanAgreed))

    ; Delivered offset0x53b0; 35 original instructions
    (method (p02Board)
        (if (or onApron (!= location 1)) (self p02Blocked: 7) (return 0))
        (if p02PlanAgreed (self p02HostDocument: 31 1) (return 0))
        (if p02Compared (self p02HostExchange: 7) (return 0))
        (self p02HostText: 81 p02BoardRecords))

    ; Delivered offset0x53f3; 6 original instructions
    (method (p02Journal)
(if (and p08 (p08 h8ActionBarrier:)) (return 0))

(if (and p05 (p05 hBarrier:)) (return 0))
 (self p02HostJournal: p02Observed p02PlanAgreed))

    ; Delivered offset0x5400; 430 original instructions
    (method (p02Act action obj target)
        (if (or (self p04Reserved: obj) (self p04Reserved: target)) (self p02Blocked: 4) (return 0))
        (if (or (< action 0) (> action 9)) (return -1))
        (if (== action 0) (self p02Walk: obj) (return 0))
        (if onApron
            (if (and (== obj 10) (== target 0) (or (== action 5) (== action 6)))
                (self p02Delegate: action obj target) (return 0))
            (if (and (== obj 32) (== target 0) (or (== action 5) (== action 2)))
                (self p02Journal:) (return 0))
            (self p02HostText: 131 0) (return 0))
        (if (not (self p02Reachable: obj)) (self p02Blocked: obj) (return 0))
        (if (and target (not (self p02Reachable: target))) (self p02Blocked: target) (return 0))
        (if (not (self p02Available:)) (self p02Delegate: action obj target) (return 0))
        (if (and (or (== action 5) (== action 2)) (== target 0))
            (if (or (and (>= obj 20) (<= obj 22)) (== obj 24) (== obj 31))
                (self p02Read: obj 0) (return 0))
            (switch obj
                (32 (self p02Journal:) (return 0))
                (26 (self p02Compare:) (return 0))
                (7 (self p02Board:) (return 0))
                (23 (self p02HostBundle:) (return 0))
                (6
                    (if (== p02CopyJack 13) (self p02Read: 20 0)
                    else (self p02HostText: 144 0)) (return 0))))
        (if (and (== action 6) (== target 0))
            (switch obj
                (2 (self p02Topic: 2 1) (return 0)) (29 (self p02Topic: 29 4) (return 0))
                (8 (self p02Topic: 8 8) (return 0)) (28 (self p02Topic: 28 9) (return 0))
                (30 (self p02HostText: 145 0) (return 0))))
        (if (and (== action 4) (>= obj 20) (<= obj 22) (== target 0)) (self p02Collect: obj) (return 0))
        (if (and (== action 7) (>= obj 20) (<= obj 22) (== target 7)) (self p02Place: obj) (return 0))
        (if (and (== action 1) (== obj 23) (== target 28)) (self p02ShowMilo:) (return 0))
        (if (and (== obj 27) (== target 0) (or (== action 2) (== action 3)))
            (self p02Drawer: (== action 2)) (return 0))
        (if (and (== action 4) (== obj 24) (== target 0)) (self p02TakeMaster:) (return 0))
        (if (and (== action 7) (== obj 24) (== target 7)) (self p02BeginPlan:) (return 0))
        (if (or (== obj 1) (== obj 3) (== obj 4) (== obj 5))
            (self p02Delegate: action obj target) (return 0))
        (self p02HostText: 146 0))

    ; Delivered offset0x56fa; 6 original instructions
    (method (p02PreparationCount) (return (if p02PlanAgreed 5 else 0)))

    ; Delivered offset0x5706; 14 original instructions
    (method (p02PreparationStatus goal)
        (if (and p02PlanAgreed (>= goal 1) (<= goal 5)) (return 0))
        (return -1))

    ; Delivered offset0x571f; 38 original instructions
    (method (uiInventoryAdd item)
(if ((ScriptID 994 0) h12Reserved: item) (return 0))

(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)
 (return ((ScriptID 992 0) uiInventoryAdd: self item)))

    ; Delivered offset0x5769; 20 original instructions
    (method (uiInventoryRemove item)
(if ((ScriptID 994 0) h12Reserved: item) (return 0))

(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)
 (return ((ScriptID 992 0) uiInventoryRemove: self item)))

    ; Delivered offset0x578f; 47 original instructions
    (method (uiInventoryCombine first second combined)
(if (or ((ScriptID 994 0) h12Reserved: first) ((ScriptID 994 0) h12Reserved: second) ((ScriptID 994 0) h12Reserved: combined)) (return 0))

(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)
 (return ((ScriptID 992 0) uiInventoryCombine: self first second combined)))

    ; Delivered offset0x57e9; 33 original instructions
    (method (uiInventoryCompact )
(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)
 (return ((ScriptID 992 0) uiInventoryCompact: self )))

    ; Delivered offset0x582a; 56 original instructions
    (method (uiAddControl action payload top left bottom right label &tmp h11i)
(if (and (== action 3) ((ScriptID 996 0) h14Owns: payload) (not ((ScriptID 996 0) h14Held: payload))) (return 1))
(if (and (== action 1) (not ((ScriptID 996 0) h14Control: payload))) (return 1))
(if (or (!= action 1) (not ((ScriptID 996 0) h14ControlOwn: payload)))
(if (and (== action 1) (not ((ScriptID 995 0) h13Control: payload))) (return 1))
(if (or (!= action 1) (not ((ScriptID 995 0) h13Owns: payload)))
(if (and (== action 1) (not ((ScriptID 994 0) h12SuccessorControl: payload))) (return 1))
(if (or (!= action 1) (not ((ScriptID 994 0) h12SuccessorHas: payload)))
(if (and (== action 1) ((ScriptID 993 0) h11OwnerHas: payload))
  (if (!= location ((ScriptID 993 0) h11OwnerLocation: payload)) (return 1))
  (for ((= h11i 0)) (< h11i uiControlCount) ((++ h11i))
   (if (and (== [uiActions h11i] 1) (== [uiPayloads h11i] payload)) (return 1))))

(if (and p06 (== action 1) (== payload 8) (!= location (p06 h6FrankieRoom?))) (return 1))

(if (and p05 p02PlanAgreed (== action 1) (or (== payload 2) (== payload 28)) (!= location (p05 hLocation: payload))) (return 1))

)
)
)
        (if (or (>= uiControlCount 64) (< top 0) (< left 0)
            (> bottom 200) (> right 320) (<= bottom top) (<= right left))
            (= uiFailure 2) (return 0))
        (= [uiActions uiControlCount] action) (= [uiPayloads uiControlCount] payload)
        (= [uiTops uiControlCount] top) (= [uiLefts uiControlCount] left)
        (= [uiBottoms uiControlCount] bottom) (= [uiRights uiControlCount] right)
        (= [uiLabels uiControlCount] label) (++ uiControlCount)
        (return 1)
    )

    ; Delivered offset0x58a4; 73 original instructions
    (method (uiVerbLabel verb)
        (switch verb
            (0 (return "WALK TO")) (1 (return "GIVE")) (2 (return "OPEN"))
            (3 (return "CLOSE")) (4 (return "PICK UP")) (5 (return "LOOK AT"))
            (6 (return "TALK TO")) (7 (return "USE")) (8 (return "PUSH"))
            (9 (return "PULL")))
        (return "WALK TO")
    )

    ; Delivered offset0x5921; 491 original instructions
    (method (uiBuildFocus &tmp t0 t1 t2 t3 t4 t5)
(if (self h13NativeChoices: 0 0) (return 0))

        (asm
            ldi 0
            aTop uiControlCount
            pToa dialogue
            bnt L_5956
            pTos uiPanel
            ldi 4
            eq?
            bnt L_5956
            pushi 480
            push0
            pToa dialogue
            send 4
            aTop uiPage
            pushi 464
            push0
            pToa dialogue
            send 4
            aTop uiPageCount
            pushi 455
            push1
            pushSelf
            pToa dialogue
            send 6
            ldi 0
            ret
            L_5956: pToa dialogue
            bnt L_59f7
            pTos uiPanel
            ldi 2
            eq?
            bnt L_59f7
            pTos uiChoiceCount
            ldi 0
            gt?
            bnt L_59f7
            pTos uiChoiceContext
            ldi 201
            eq?
            bt L_5991
            pTos uiChoiceContext
            ldi 202
            eq?
            bt L_5991
            pTos uiChoiceContext
            ldi 204
            ge?
            bnt L_59f7
            pTos uiChoiceContext
            ldi 237
            le?
            bnt L_59f7
            L_5991: pToa uiChoiceCount
            aTop uiPageCount
            pTos uiPage
            ldi 0
            lt?
            bnt L_59a4
            ldi 0
            aTop uiPage
            L_59a4: pTos uiPage
            pToa uiPageCount
            ge?
            bnt L_59b6
            pTos uiPageCount
            ldi 1
            sub
            aTop uiPage
            L_59b6: pushi 457
            pushi 6
            pushSelf
            pTos uiChoiceCount
            pTos uiPage
            pTos uiChoiceMulti
            pToa uiPage
            lsli 644
            pToa uiPage
            lsli 708
            pToa dialogue
            send 16
            pTos uiFocus
            ldi 0
            lt?
            bnt L_59e2
            ldi 0
            aTop uiFocus
            L_59e2: pTos uiFocus
            pToa uiControlCount
            ge?
            bnt L_59f4
            pTos uiControlCount
            ldi 1
            sub
            aTop uiFocus
            L_59f4: ldi 0
            ret
            L_59f7: pTos uiPanel
            ldi 1
            eq?
            bnt L_5a0b
            pushi 287
            push1
            pTos uiDocument
            self 6
            aTop uiPageCount
            L_5a0b: pTos uiPanel
            ldi 3
            eq?
            bnt L_5a18
            ldi 1
            aTop uiPageCount
            L_5a18: pTos uiPage
            ldi 0
            lt?
            bnt L_5a25
            ldi 0
            aTop uiPage
            L_5a25: pTos uiPanel
            ldi 2
            ne?
            bnt L_5a3f
            pTos uiPage
            pToa uiPageCount
            ge?
            bnt L_5a3f
            pTos uiPageCount
            ldi 1
            sub
            aTop uiPage
            L_5a3f: pToa uiPanel
            bnt L_5b66
            pTos uiPanel
            ldi 2
            eq?
            bnt L_5ad7
            pTos uiChoiceCount
            ldi 2
            add
            push
            ldi 3
            div
            aTop uiPageCount
            pTos uiPageCount
            ldi 1
            lt?
            bnt L_5a68
            ldi 1
            aTop uiPageCount
            L_5a68: pTos uiPage
            pToa uiPageCount
            ge?
            bnt L_5a7a
            pTos uiPageCount
            ldi 1
            sub
            aTop uiPage
            L_5a7a: pTos uiPage
            ldi 3
            mul
            sat 4
            lst 4
            ldi 3
            add
            sat 5
            lst 5
            pToa uiChoiceCount
            gt?
            bnt L_5a96
            pToa uiChoiceCount
            sat 5
            L_5a96: lat 4
            sat 0
            L_5a9a: lst 0
            lat 5
            lt?
            bnt L_5ad7
            lat 0
            lali 708
            bnt L_5ad3
            pushi 44
            lst 0
            lat 4
            sub
            push
            ldi 36
            mul
            add
            sat 3
            pushi 269
            pushi 7
            pushi 13
            lst 0
            lst 3
            pushi 16
            lst 3
            ldi 32
            add
            push
            pushi 304
            lat 0
            lsli 644
            self 18
            L_5ad3: +at 0
            jmp L_5a9a
            L_5ad7: pTos uiPage
            ldi 0
            gt?
            bnt L_5af6
            pushi 269
            pushi 7
            pushi 10
            push0
            pushi 164
            pushi 16
            pushi 176
            pushi 82
            lofss "PREV"
            self 18
            L_5af6: pTos uiPage
            pTos uiPageCount
            ldi 1
            sub
            lt?
            bnt L_5b1a
            pushi 269
            pushi 7
            pushi 11
            push0
            pushi 164
            pushi 88
            pushi 176
            pushi 154
            lofss "NEXT"
            self 18
            L_5b1a: pTos uiPanel
            ldi 2
            eq?
            bnt L_5b40
            pToa uiChoiceMulti
            bnt L_5b40
            pushi 269
            pushi 7
            pushi 14
            push0
            pushi 180
            pushi 174
            pushi 192
            pushi 304
            lofss "CONFIRM CHOICES"
            self 18
            L_5b40: pushi 269
            pushi 7
            pushi 12
            push0
            pushi 180
            pushi 16
            pushi 192
            pushi 160
            pToa uiBackPanel
            bnt L_5b5d
            lofsa "BACK"
            jmp L_5b60
            L_5b5d: lofsa "CLOSE / BACK"
            L_5b60: push
            self 18
            jmp L_5cfe
            L_5b66: pushi 311
            push0
            self 4
            pushi 269
            pushi 7
            pushi 9
            push0
            pushi 144
            push0
            pushi 154
            pushi 320
            lofss "FULL SENTENCE"
            self 18
            ldi 1
            sat 0
            L_5b87: lst 0
            ldi 9
            le?
            bnt L_5bd9
            push2
            lst 0
            ldi 1
            sub
            push
            ldi 3
            div
            push
            ldi 51
            mul
            add
            sat 2
            pushi 155
            lst 0
            ldi 1
            sub
            push
            ldi 3
            mod
            push
            ldi 14
            mul
            add
            sat 3
            pushi 269
            pushi 7
            push2
            lst 0
            lst 3
            lst 2
            lst 3
            ldi 12
            add
            push
            lst 2
            ldi 49
            add
            push
            pushi 338
            push1
            lst 0
            self 6
            push
            self 18
            +at 0
            jmp L_5b87
            L_5bd9: pTos uiInventoryExtent
            ldi 7
            add
            push
            ldi 8
            div
            aTop uiInventoryPages
            pTos uiInventoryPages
            ldi 1
            lt?
            bnt L_5bf3
            ldi 1
            aTop uiInventoryPages
            L_5bf3: pTos uiInventoryPage
            pToa uiInventoryPages
            ge?
            bnt L_5c05
            pTos uiInventoryPages
            ldi 1
            sub
            aTop uiInventoryPage
            L_5c05: ldi 0
            sat 0
            L_5c09: lst 0
            ldi 8
            lt?
            bnt L_5c68
            pTos uiInventoryPage
            ldi 8
            mul
            push
            lat 0
            add
            lali 100
            sat 1
            lat 1
            bnt L_5c64
            pushi 160
            lst 0
            ldi 4
            mod
            push
            ldi 38
            mul
            add
            sat 2
            pushi 155
            lst 0
            ldi 4
            div
            push
            ldi 14
            mul
            add
            sat 3
            pushi 269
            pushi 7
            pushi 3
            lst 1
            lst 3
            lst 2
            lst 3
            ldi 12
            add
            push
            lst 2
            ldi 36
            add
            push
            pushi 309
            push1
            lst 1
            self 6
            push
            self 18
            L_5c64: +at 0
            jmp L_5c09
            L_5c68: pTos uiInventoryPage
            ldi 0
            gt?
            bnt L_5c89
            pushi 269
            pushi 7
            pushi 4
            push0
            pushi 185
            pushi 160
            pushi 199
            pushi 194
            lofss "PREV"
            self 18
            L_5c89: pTos uiInventoryPage
            pTos uiInventoryPages
            ldi 1
            sub
            lt?
            bnt L_5cae
            pushi 269
            pushi 7
            pushi 5
            push0
            pushi 185
            pushi 236
            pushi 199
            pushi 270
            lofss "NEXT"
            self 18
            L_5cae: pushi 269
            pushi 7
            pushi 6
            push0
            pushi 185
            pushi 276
            pushi 199
            pushi 318
            lofss "CANCEL"
            self 18
            pushi 269
            pushi 7
            pushi 7
            push0
            push0
            pushi 218
            pushi 10
            pushi 263
            pToa uiReveal
            bnt L_5ce2
            lofsa "HIDE"
            jmp L_5ce5
            L_5ce2: lofsa "REVEAL"
            L_5ce5: push
            self 18
            pushi 269
            pushi 7
            pushi 8
            push0
            push0
            pushi 269
            pushi 10
            pushi 316
            lofss "MENU"
            self 18
            L_5cfe: pushi 307
            push0
            self 4
            pTos uiFocus
            ldi 0
            lt?
            bnt L_5d11
            ldi 0
            aTop uiFocus
            L_5d11: pTos uiFocus
            pToa uiControlCount
            ge?
            bnt L_5d23
            pTos uiControlCount
            ldi 1
            sub
            aTop uiFocus
            L_5d23: ret
        )
    )

    ; Delivered offset0x5d24; 35 original instructions
    (method (uiHit px py &tmp i)
        ; Reverse order: later panel/HUD controls win. Half-open rectangles.
        (= i (- uiControlCount 1))
        (while (>= i 0)
            (if (and (>= py [uiTops i]) (< py [uiBottoms i])
                     (>= px [uiLefts i]) (< px [uiRights i])) (return i))
            (-- i))
        (return -1)
    )

    ; Delivered offset0x5d67; 27 original instructions
    (method (uiCycle step)
        (if (<= uiControlCount 0) (return 0))
        (= uiFocus (+ uiFocus step))
        (if (< uiFocus 0) (= uiFocus (- uiControlCount 1)))
        (if (>= uiFocus uiControlCount) (= uiFocus 0))
        (= dirty 1)
    )

    ; Delivered offset0x5da0; 100 original instructions
    (method (uiArrow dx dy &tmp i cx cy tx ty along across score best bestScore)
        (if (or (< uiFocus 0) (>= uiFocus uiControlCount)) (return 0))
        (= cx (+ [uiLefts uiFocus] [uiRights uiFocus]))
        (= cy (+ [uiTops uiFocus] [uiBottoms uiFocus]))
        (= best uiFocus) (= bestScore 32000)
        (for ((= i 0)) (< i uiControlCount) ((++ i))
            (= tx (- (+ [uiLefts i] [uiRights i]) cx))
            (= ty (- (+ [uiTops i] [uiBottoms i]) cy))
            (= along (if dx (* tx dx) else (* ty dy)))
            (= across (if dx ty else tx)) (if (< across 0) (= across (- 0 across)))
            (if (> along 0)
                (= score (+ along (* across 3)))
                (if (< score bestScore) (= bestScore score) (= best i))))
        (= uiFocus best) (= dirty 1)
    )

    ; Delivered offset0x5e66; 30 original instructions
    (method (uiPointer &tmp hit)
        ; Stationary pointer cannot undo a keyboard focus choice.
        (if (or (!= x uiLastX) (!= y uiLastY))
            (= uiLastX x) (= uiLastY y) (= hit (self uiHit: x y))
            (= uiHover hit)
            (if (>= hit 0) (= uiFocus hit))
            (= dirty 1))
    )

    ; Delivered offset0x5ea5; 13 original instructions
    (method (uiCancelSentence)
((ScriptID 996 0) h14Retire:)

((ScriptID 995 0) h13Retire:)
((ScriptID 995 0) h13Cancel:)

((ScriptID 994 0) h12SuccessorCancel:)

        (asm
            pushi 377
            push0
            self 4
            pushi 133
            push0
            self 4
            ldi 0
            aTop uiVerb
            ldi 0
            aTop uiNounA
            ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x5ec1; 52 original instructions
    (method (uiChooseObject item &tmp first verb)
(if (and p08 (p08 h8LayoutFirst: item uiVerb uiNounA)) (return 0))

(if (and p07 (p07 h7FirstNoun: item uiVerb uiNounA)) (return 0))

        (if (self uiHostIsReturn: item)
            (self uiCancelSentence:) (self uiHostAct: 0 item 0) (return 0))
        (if (or (== uiVerb 1) (== uiVerb 7))
            (if uiNounA
                (= first uiNounA) (= verb uiVerb) (= uiNounA 0)
                (self uiHostAct: verb first item)
            else (= uiNounA item))
        else (self uiHostAct: uiVerb item 0))
        (= dirty 1)
    )

    ; Delivered offset0x5f2e; 41 original instructions
    (method (uiClearChoices arg1 arg2 arg3 &tmp t0)
        (asm
            ldi 0
            aTop navNotice
            ldi 0
            aTop navNoticeTicks
            ldi 0
            aTop uiChoiceCount
            lap 2
            aTop uiChoiceContext
            lap 3
            aTop uiChoiceMulti
            pToa uiFocus
            aTop uiBackFocus
            ldi 0
            aTop uiBackPage
            lap 1
            aTop uiTitle
            ldi 2
            aTop uiPanel
            ldi 0
            aTop uiPage
            ldi 0
            aTop uiBackPanel
            ldi 0
            aTop uiReveal
            ldi 0
            aTop uiFocus
            ldi 1
            aTop dirty
            ldi 0
            sat 0
            L_5f79: lst 0
            ldi 32
            lt?
            bnt L_5f8a
            push0
            lat 0
            sali 708
            +at 0
            jmp L_5f79
            L_5f8a: ret
        )
    )

    ; Delivered offset0x5f8b; 47 original instructions
    (method (uiAddChoice id label selected enabled)
        (if (or (>= uiChoiceCount 32) (> (StrLen label) 120))
            (= uiFailure 3) (return 0))
        (TextSize @uiMeasure label 0 260)
        (if (> [uiMeasure 2] 24) (= uiFailure 3) (return 0))
        (= [uiChoiceIds uiChoiceCount] id) (= [uiChoiceLabels uiChoiceCount] label)
        (= [uiChoiceSelected uiChoiceCount] selected) (= [uiChoiceEnabled uiChoiceCount] enabled)
        (++ uiChoiceCount) (= dirty 1) (return 1)
    )

    ; Delivered offset0x5ff3; 20 original instructions
    (method (uiSetChoice id selected &tmp i)
        (for ((= i 0)) (< i uiChoiceCount) ((++ i))
            (if (== [uiChoiceIds i] id) (= [uiChoiceSelected i] selected)))
        (= dirty 1)
    )

    ; Delivered offset0x601c; 19 original instructions
    (method (uiGetChoice id &tmp i)
        (for ((= i 0)) (< i uiChoiceCount) ((++ i))
            (if (== [uiChoiceIds i] id) (return [uiChoiceSelected i])))
        (return -1)
    )

    ; Delivered offset0x6041; 23 original instructions
    (method (uiRememberBack)
        (if (== uiPanel 2)
            (= uiBackPanel 2) (= uiBackPage uiPage) (= uiBackFocus uiFocus) (= uiBackTitle uiTitle)
        else (if (not uiPanel) (= uiBackPanel 0) (= uiBackPage 0) (= uiBackFocus uiFocus)))
    )

    ; Delivered offset0x6079; 62 original instructions
    (method (uiOpenReader arg1)
(if (not ((ScriptID 993 0) h11ReadBoundary:)) (return 0))

(if (and p08 (p08 h8ReaderCheck: 2 arg1)) (return 0))

        (asm
            ldi 0
            aTop navNotice
            ldi 0
            aTop navNoticeTicks
            pushi 560
            push0
            self 4
            pToa dialogue
            bnt L_609f
            pushi 446
            push0
            pToa dialogue
            send 4
            bnt L_609f
            pushi 458
            push1
            pTos presentation
            pToa dialogue
            send 6
            L_609f: pushi 377
            push0
            self 4
            pushi 288
            push2
            lsp 1
            push0
            self 8
            push
            ldi 0
            lt?
            bnt L_60bc
            ldi 4
            aTop uiFailure
            ldi 0
            ret
            L_60bc: pushi 331
            push0
            self 4
            ldi 1
            aTop uiPanel
            lap 1
            aTop uiDocument
            pushi 289
            push1
            lsp 1
            self 6
            aTop uiTitle
            ldi 0
            aTop uiPage
            pushi 287
            push1
            lsp 1
            self 6
            aTop uiPageCount
            ldi 0
            aTop uiFocus
            ldi 0
            aTop uiReveal
            ldi 1
            aTop dirty
            ldi 1
            ret
        )
    )

    ; Delivered offset0x60f9; 72 original instructions
    (method (uiOpenInline arg1 arg2)
        (asm
            ldi 0
            aTop navNotice
            ldi 0
            aTop navNoticeTicks
            pushi 560
            push0
            self 4
            pToa dialogue
            bnt L_611f
            pushi 446
            push0
            pToa dialogue
            send 4
            bnt L_611f
            pushi 458
            push1
            pTos presentation
            pToa dialogue
            send 6
            L_611f: pushi 377
            push0
            self 4
            push1
            lsp 2
            callk StrLen, 2
            push
            ldi 798
            gt?
            bnt L_613a
            ldi 5
            aTop uiFailure
            ldi 0
            ret
            L_613a: pushi 4
            lea uiMeasure
            push
            lsp 2
            push0
            pushi 288
            callk TextSize, 8
            lsl 1670
            ldi 112
            gt?
            bnt L_615b
            ldi 5
            aTop uiFailure
            ldi 0
            ret
            L_615b: pushi 331
            push0
            self 4
            push2
            lea uiInline
            push
            lsp 2
            callk StrCpy, 4
            ldi 3
            aTop uiPanel
            lap 1
            aTop uiTitle
            ldi 0
            aTop uiPage
            ldi 1
            aTop uiPageCount
            ldi 0
            aTop uiFocus
            ldi 0
            aTop uiReveal
            ldi 1
            aTop dirty
            ldi 1
            ret
        )
    )

    ; Delivered offset0x6193; 31 original instructions
    (method (uiClose)
((ScriptID 993 0) h11PayClose:)

(if p08 (p08 h8LayoutRetire:))

(if (and p08 (p08 h8ActionBarrier:) (not (p08 h8VR: 8 0))) (return 0))

(if p07 (p07 h7RetireLaugh:))

(if p05 (p05 hStageRetire:)) 

        (asm
            pToa dialogue
            bnt L_61a9
            pTos uiPanel
            ldi 4
            eq?
            bnt L_61a9
            pushi 458
            push1
            pTos presentation
            pToa dialogue
            send 6
            L_61a9: pToa uiBackPanel
            aTop uiPanel
            pToa uiBackPage
            aTop uiPage
            pToa uiBackFocus
            aTop uiFocus
            pToa uiBackPanel
            bnt L_61c6
            pToa uiBackTitle
            aTop uiTitle
            L_61c6: ldi 0
            aTop uiBackPanel
            ldi 0
            aTop uiReveal
            ldi 1
            aTop dirty
            pushi 300
            push0
            self 4
            ret
        )
    )

    ; Delivered offset0x61dc; 121 original instructions
    (method (uiTurnPage arg1 &tmp t0 t1)
(if (self h13NativeChoices: 1 arg1) (return 0))

(if (and p09 (p09 h9Continue: 1 arg1)) (return 0))

(if (and p08 (p08 h8VR: 14 arg1)) (return 0))

        (asm
            pToa dialogue
            bnt L_620f
            pTos uiPanel
            ldi 4
            eq?
            bnt L_620f
            pushi 496
            push2
            lsp 1
            pTos presentation
            pToa dialogue
            send 8
            pushi 480
            push0
            pToa dialogue
            send 4
            aTop uiPage
            pushi 276
            push0
            self 4
            ldi 1
            aTop dirty
            ldi 0
            ret
            L_620f: pToa dialogue
            bnt L_624d
            pTos uiPanel
            ldi 2
            eq?
            bnt L_624d
            pTos uiChoiceCount
            ldi 0
            gt?
            bnt L_624d
            pTos uiChoiceContext
            ldi 201
            eq?
            bt L_6247
            pTos uiChoiceContext
            ldi 202
            eq?
            bt L_6247
            pTos uiChoiceContext
            ldi 204
            ge?
            bnt L_624d
            pTos uiChoiceContext
            ldi 237
            le?
            bnt L_624d
            L_6247: pToa uiChoiceCount
            aTop uiPageCount
            L_624d: pTos uiPage
            lap 1
            add
            aTop uiPage
            pTos uiPage
            ldi 0
            lt?
            bnt L_6263
            ldi 0
            aTop uiPage
            L_6263: pTos uiPage
            pToa uiPageCount
            ge?
            bnt L_6275
            pTos uiPageCount
            ldi 1
            sub
            aTop uiPage
            L_6275: ldi 0
            aTop uiFocus
            pushi 276
            push0
            self 4
            pTos uiPanel
            ldi 2
            ne?
            bnt L_62d5
            lsp 1
            ldi 0
            gt?
            bnt L_6293
            ldi 11
            jmp L_6295
            L_6293: ldi 10
            L_6295: sat 1
            ldi 0
            sat 0
            L_629b: lst 0
            pToa uiControlCount
            lt?
            bnt L_62b6
            lat 0
            lsli 164
            ldi 12
            eq?
            bnt L_62b2
            lat 0
            aTop uiFocus
            L_62b2: +at 0
            jmp L_629b
            L_62b6: ldi 0
            sat 0
            L_62ba: lst 0
            pToa uiControlCount
            lt?
            bnt L_62d5
            lat 0
            lsli 164
            lat 1
            eq?
            bnt L_62d1
            lat 0
            aTop uiFocus
            L_62d1: +at 0
            jmp L_62ba
            L_62d5: ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x62db; 204 original instructions
    (method (uiActivate arg1 &tmp t0 t1)
(if (and p08 (p08 h8VI: 4 arg1 0 0)) (return 0))

        (asm
            lsp 1
            ldi 0
            lt?
            bt L_62ec
            lsp 1
            pToa uiControlCount
            ge?
            bnt L_62ef
            L_62ec: ldi 0
            ret
            L_62ef: lap 1
            lali 164
            sat 0
            lap 1
            lali 228
            sat 1
            lst 0
            dup
            ldi 1
            eq?
            bnt L_6310
            pushi 281
            push1
            lst 1
            self 6
            jmp L_645e
            L_6310: dup
            ldi 18
            eq?
            bnt L_632a
            pushi 277
            push0
            self 4
            pushi 298
            pushi 3
            push0
            lst 1
            push0
            self 10
            jmp L_645e
            L_632a: dup
            ldi 2
            eq?
            bnt L_633d
            lat 1
            aTop uiVerb
            ldi 0
            aTop uiNounA
            jmp L_645e
            L_633d: dup
            ldi 3
            eq?
            bnt L_634e
            pushi 281
            push1
            lst 1
            self 6
            jmp L_645e
            L_634e: dup
            ldi 4
            eq?
            bnt L_635f
            dpToa uiInventoryPage
            ldi 0
            aTop uiFocus
            jmp L_645e
            L_635f: dup
            ldi 5
            eq?
            bnt L_6370
            ipToa uiInventoryPage
            ldi 0
            aTop uiFocus
            jmp L_645e
            L_6370: dup
            ldi 6
            eq?
            bnt L_637f
            pushi 277
            push0
            self 4
            jmp L_645e
            L_637f: dup
            ldi 7
            eq?
            bnt L_638f
            pToa uiReveal
            not
            aTop uiReveal
            jmp L_645e
            L_638f: dup
            ldi 8
            eq?
            bnt L_639e
            pushi 306
            push0
            self 4
            jmp L_645e
            L_639e: dup
            ldi 9
            eq?
            bnt L_63bc
            pushi 284
            push0
            self 4
            pushi 325
            push2
            lofss "FULL SENTENCE"
            lea uiSentence
            push
            self 8
            jmp L_645e
            L_63bc: dup
            ldi 10
            eq?
            bnt L_63cd
            pushi 336
            push1
            pushi -1
            self 6
            jmp L_645e
            L_63cd: dup
            ldi 11
            eq?
            bnt L_63dd
            pushi 336
            push1
            push1
            self 6
            jmp L_645e
            L_63dd: dup
            ldi 12
            eq?
            bnt L_63eb
            pushi 283
            push0
            self 4
            jmp L_645e
            L_63eb: dup
            ldi 13
            eq?
            bnt L_6401
            pushi 299
            push2
            pTos uiChoiceContext
            lat 1
            lsli 612
            self 8
            jmp L_645e
            L_6401: dup
            ldi 14
            eq?
            bnt L_6412
            pushi 301
            push1
            pTos uiChoiceContext
            self 6
            jmp L_645e
            L_6412: dup
            ldi 15
            eq?
            bnt L_6422
            pushi 310
            push1
            lst 1
            self 6
            jmp L_645e
            L_6422: dup
            ldi 16
            eq?
            bnt L_6440
            pToa dialogue
            bnt L_643e
            pTos uiPanel
            ldi 4
            eq?
            bnt L_643e
            pushi 490
            push1
            pTos presentation
            pToa dialogue
            send 6
            L_643e: jmp L_645e
            L_6440: dup
            ldi 17
            eq?
            bnt L_645e
            pToa dialogue
            bnt L_645e
            pTos uiPanel
            ldi 4
            eq?
            bnt L_645e
            pushi 475
            push2
            pTos presentation
            pushi 21
            pToa dialogue
            send 8
            L_645e: toss
            ldi 1
            aTop dirty
            ret
        )
    )

    ; Delivered offset0x6465; 338 original instructions
    (method (uiInput &tmp t0 t1 t2)
(if (and p08 (p08 h8VI: 5 0 0 0)) (return 1))

        (asm
            pToa dialogue
            bnt L_6495
            pTos uiPanel
            ldi 4
            eq?
            bnt L_6495
            pTos type
            ldi 4
            eq?
            bnt L_6495
            pTos message
            ldi 32
            eq?
            bnt L_6495
            pushi 475
            push2
            pTos presentation
            pushi 21
            pToa dialogue
            send 8
            ldi 1
            aTop dirty
            ldi 1
            ret
            L_6495: pTos uiPanel
            ldi 4
            eq?
            bnt L_64b4
            pTos type
            ldi 4
            eq?
            bnt L_64b4
            pTos message
            ldi 109
            eq?
            bnt L_64b4
            pushi 306
            push0
            self 4
            ldi 1
            ret
            L_64b4: pTos type
            ldi 4
            eq?
            bnt L_661f
            pTos message
            ldi 15360
            eq?
            bnt L_64cd
            pushi 308
            push0
            self 4
            ldi 1
            ret
            L_64cd: pTos message
            ldi 15616
            eq?
            bnt L_64de
            pushi 305
            push0
            self 4
            ldi 1
            ret
            L_64de: pTos message
            ldi 9
            eq?
            bnt L_64ef
            pushi 286
            push1
            push1
            self 6
            ldi 1
            ret
            L_64ef: pTos message
            ldi 3840
            eq?
            bnt L_6502
            pushi 286
            push1
            pushi -1
            self 6
            ldi 1
            ret
            L_6502: pTos message
            ldi 13
            eq?
            bnt L_6515
            pushi 267
            push1
            pTos uiFocus
            self 6
            ldi 1
            ret
            L_6515: pTos message
            ldi 27
            eq?
            bnt L_6543
            pToa uiPanel
            bnt L_6529
            pushi 283
            push0
            self 4
            jmp L_653b
            L_6529: pToa uiReveal
            bnt L_6535
            ldi 0
            aTop uiReveal
            jmp L_653b
            L_6535: pushi 277
            push0
            self 4
            L_653b: ldi 1
            aTop dirty
            ldi 1
            ret
            L_6543: pTos message
            ldi 32
            eq?
            bnt L_655d
            pToa uiPanel
            not
            bnt L_655a
            ldi 1
            aTop uiReveal
            ldi 1
            aTop dirty
            L_655a: ldi 1
            ret
            L_655d: pTos message
            ldi 19200
            eq?
            bnt L_6580
            pToa uiPanel
            bnt L_6574
            pushi 336
            push1
            pushi -1
            self 6
            jmp L_657d
            L_6574: pushi 271
            push2
            pushi -1
            push0
            self 8
            L_657d: ldi 1
            ret
            L_6580: pTos message
            ldi 19712
            eq?
            bnt L_65a1
            pToa uiPanel
            bnt L_6596
            pushi 336
            push1
            push1
            self 6
            jmp L_659e
            L_6596: pushi 271
            push2
            push1
            push0
            self 8
            L_659e: ldi 1
            ret
            L_65a1: pTos message
            ldi 18432
            eq?
            bnt L_65c4
            pToa uiPanel
            bnt L_65b8
            pushi 286
            push1
            pushi -1
            self 6
            jmp L_65c1
            L_65b8: pushi 271
            push2
            push0
            pushi -1
            self 8
            L_65c1: ldi 1
            ret
            L_65c4: pTos message
            ldi 20480
            eq?
            bnt L_65e5
            pToa uiPanel
            bnt L_65da
            pushi 286
            push1
            push1
            self 6
            jmp L_65e2
            L_65da: pushi 271
            push2
            push0
            push1
            self 8
            L_65e2: ldi 1
            ret
            L_65e5: pToa uiPanel
            bnt L_65fd
            pTos message
            ldi 18688
            eq?
            bnt L_65fd
            pushi 336
            push1
            pushi -1
            self 6
            ldi 1
            ret
            L_65fd: pToa uiPanel
            bnt L_6614
            pTos message
            ldi 20736
            eq?
            bnt L_6614
            pushi 336
            push1
            push1
            self 6
            ldi 1
            ret
            L_6614: pToa uiPanel
            bnt L_661c
            ldi 1
            ret
            L_661c: ldi 0
            ret
            L_661f: pTos type
            ldi 1
            eq?
            bnt L_66e3
            pushi 297
            push2
            pTos x
            pTos y
            self 8
            sat 0
            pTos modifiers
            ldi 3
            and
            bnt L_66c4
            pToa uiPanel
            bnt L_6648
            pushi 283
            push0
            self 4
            jmp L_66c1
            L_6648: pushi 277
            push0
            self 4
            lst 0
            ldi 0
            ge?
            bnt L_666d
            lat 0
            lsli 164
            ldi 18
            eq?
            bnt L_666d
            pushi 298
            pushi 3
            push0
            lat 0
            lsli 228
            push0
            self 10
            L_666d: lst 0
            ldi 0
            ge?
            bnt L_66c1
            lat 0
            lsli 164
            ldi 1
            eq?
            bt L_6688
            lat 0
            lsli 164
            ldi 3
            eq?
            bnt L_66c1
            L_6688: lat 0
            lali 228
            sat 1
            pushi 302
            push1
            lst 1
            self 6
            sat 2
            lst 2
            ldi 0
            ge?
            bnt L_66c1
            lst 2
            ldi 9
            le?
            bnt L_66c1
            lst 2
            ldi 1
            ne?
            bnt L_66c1
            lst 2
            ldi 7
            ne?
            bnt L_66c1
            pushi 298
            pushi 3
            lst 2
            lst 1
            push0
            self 10
            L_66c1: ldi 1
            ret
            L_66c4: lst 0
            ldi 0
            ge?
            bnt L_66db
            lat 0
            aTop uiFocus
            pushi 267
            push1
            lst 0
            self 6
            ldi 1
            ret
            L_66db: pToa uiPanel
            bnt L_66e3
            ldi 1
            ret
            L_66e3: pToa uiPanel
            bnt L_66eb
            ldi 1
            ret
            L_66eb: ldi 0
            ret
        )
    )

    ; Delivered offset0x66ee; 134 original instructions
    (method (uiComposeSentence &tmp t0 t1 t2)
        (asm
            pTos uiFocus
            ldi 0
            ge?
            bnt L_6721
            pTos uiFocus
            pToa uiControlCount
            lt?
            bnt L_6721
            pToa uiFocus
            lsli 164
            ldi 18
            eq?
            bnt L_6721
            push2
            lea uiSentence
            push
            lofss "WALK TO LIVING ROOM"
            callk StrCpy, 4
            ldi 0
            aTop uiFullSentence
            ldi 0
            ret
            L_6721: ldi 0
            sat 0
            pTos uiFocus
            ldi 0
            ge?
            bnt L_6754
            pTos uiFocus
            pToa uiControlCount
            lt?
            bnt L_6754
            pToa uiFocus
            lsli 164
            ldi 1
            eq?
            bt L_674c
            pToa uiFocus
            lsli 164
            ldi 3
            eq?
            bnt L_6754
            L_674c: pToa uiFocus
            lali 228
            sat 0
            L_6754: lat 0
            bnt L_675d
            lat 0
            aTop uiFocusObject
            L_675d: pushi 304
            push1
            pToa uiNounA
            bnt L_676b
            pToa uiNounA
            jmp L_676e
            L_676b: pToa uiFocusObject
            L_676e: push
            self 6
            sat 1
            pushi 304
            push1
            pTos uiFocusObject
            self 6
            sat 2
            push1
            lst 1
            callk StrLen, 2
            push
            ldi 100
            gt?
            bt L_6796
            push1
            lst 2
            callk StrLen, 2
            push
            ldi 100
            gt?
            bnt L_67aa
            L_6796: ldi 6
            aTop uiFailure
            push2
            lea uiSentence
            push
            lofss "ITEM NAME EXCEEDS UI CONTRACT. HOST MUST PROVIDE A READER."
            callk StrCpy, 4
            jmp L_67f8
            L_67aa: pToa uiNounA
            bnt L_67de
            pushi 6
            lea uiSentence
            push
            lofss "%s %s %s %s"
            pushi 338
            push1
            pTos uiVerb
            self 6
            push
            lst 1
            pTos uiVerb
            ldi 1
            eq?
            bnt L_67d3
            lofsa "TO"
            jmp L_67d6
            L_67d3: lofsa "WITH"
            L_67d6: push
            lst 2
            callk Format, 12
            jmp L_67f8
            L_67de: pushi 4
            lea uiSentence
            push
            lofss "%s %s"
            pushi 338
            push1
            pTos uiVerb
            self 6
            push
            lst 1
            callk Format, 8
            L_67f8: pushi 4
            lea uiMeasure
            push
            lea uiSentence
            push
            push0
            pushi 308
            callk TextSize, 8
            lsl 1670
            ldi 8
            gt?
            aTop uiFullSentence
            ret
        )
    )

    ; Delivered offset0x6817; 57 original instructions
    (method (uiFrame top left bottom right color)
        (Graph 11 top left (+ top 1) right 1 color 0 0)
        (Graph 11 (- bottom 1) left bottom right 1 color 0 0)
        (Graph 11 top left bottom (+ left 1) 1 color 0 0)
        (Graph 11 top (- right 1) bottom right 1 color 0 0)
    )

    ; Delivered offset0x6878; 639 original instructions
    (method (uiRender &tmp t0 t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13 t14 t15 t16 t17 t18 t19 t20 t21 t22 t23 t24 t25 t26 t27 t28 t29 t30)
(if (self h13NativeChoices: 2 0) (return 0))

        (asm
            pushi 276
            push0
            self 4
            pToa dialogue
            bnt L_68d5
            pTos uiPanel
            ldi 4
            eq?
            bnt L_68d5
            pushi 466
            push1
            pTos uiFocus
            pToa dialogue
            send 6
            not
            bnt L_68d2
            pTos uiDocument
            ldi 343
            ge?
            bnt L_68ac
            pTos uiDocument
            ldi 420
            le?
            bt L_68b8
            L_68ac: pushi 326
            push1
            pTos uiDocument
            self 6
            not
            bnt L_68cc
            L_68b8: ldi 0
            aTop uiPanel
            ldi 0
            aTop uiBackPanel
            ldi 0
            aTop bridgeReaderActive
            ldi 8
            aTop uiFailure
            L_68cc: pushi 332
            push0
            self 4
            L_68d2: ldi 0
            ret
            L_68d5: pToa dialogue
            bnt L_6940
            pTos uiPanel
            ldi 2
            eq?
            bnt L_6940
            pTos uiChoiceCount
            ldi 0
            gt?
            bnt L_6940
            pTos uiChoiceContext
            ldi 201
            eq?
            bt L_690d
            pTos uiChoiceContext
            ldi 202
            eq?
            bt L_690d
            pTos uiChoiceContext
            ldi 204
            ge?
            bnt L_6940
            pTos uiChoiceContext
            ldi 237
            le?
            bnt L_6940
            L_690d: pushi 467
            pushi 8
            pushSelf
            pTos uiTitle
            pToa uiPage
            lsli 644
            pTos uiPage
            pTos uiChoiceCount
            pToa uiPage
            lsli 676
            pTos uiChoiceMulti
            pToa uiPage
            lsli 708
            pToa dialogue
            send 20
            not
            bnt L_693d
            ldi 8
            aTop uiFailure
            L_693d: ldi 0
            ret
            L_6940: pushi 9
            pushi 11
            pushi 144
            push0
            pushi 200
            pushi 320
            push1
            push0
            push0
            push0
            callk Graph, 18
            pushi 284
            push0
            self 4
            pushi 11
            pToa uiFullSentence
            bnt L_6967
            lofsa "FULL SENTENCE: CLICK OR ENTER TO READ"
            jmp L_696c
            L_6967: lea uiSentence
            L_696c: push
            pushi 100
            pushi 6
            pushi 145
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 308
            pushi 121
            callk Display, 22
            pToa uiPanel
            not
            bnt L_6a06
            ldi 0
            sat 0
            L_698e: lst 0
            ldi 8
            lt?
            bnt L_69d0
            pushi 160
            lst 0
            ldi 4
            mod
            push
            ldi 38
            mul
            add
            sat 4
            pushi 155
            lst 0
            ldi 4
            div
            push
            ldi 14
            mul
            add
            sat 5
            pushi 294
            pushi 5
            lst 5
            lst 4
            lst 5
            ldi 12
            add
            push
            lst 4
            ldi 36
            add
            push
            pushi 13
            self 14
            +at 0
            jmp L_698e
            L_69d0: pushi 4
            lea t7
            push
            lofss "%d/%d"
            pTos uiInventoryPage
            ldi 1
            add
            push
            pTos uiInventoryPages
            callk Format, 8
            pushi 11
            lea t7
            push
            pushi 100
            pushi 202
            pushi 188
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 32
            pushi 121
            callk Display, 22
            jmp L_6b49
            L_6a06: pushi 9
            pushi 11
            push0
            push0
            pushi 200
            pushi 320
            push1
            push0
            push0
            push0
            callk Graph, 18
            pushi 294
            pushi 5
            pushi 6
            pushi 8
            pushi 196
            pushi 312
            push1
            self 14
            pushi 4
            lea uiMeasure
            push
            pTos uiTitle
            push0
            pushi 288
            callk TextSize, 8
            lsl 1670
            ldi 16
            le?
            bnt L_6a62
            pushi 11
            pTos uiTitle
            pushi 100
            pushi 16
            pushi 12
            pushi 102
            push2
            pushi 105
            push0
            pushi 106
            pushi 288
            pushi 121
            callk Display, 22
            jmp L_6a67
            L_6a62: ldi 7
            aTop uiFailure
            L_6a67: pushi 4
            lea t7
            push
            lofss "PAGE %d/%d"
            pTos uiPage
            ldi 1
            add
            push
            pTos uiPageCount
            callk Format, 8
            pushi 11
            lea t7
            push
            pushi 100
            pushi 16
            pushi 32
            pushi 102
            pushi 13
            pushi 105
            push0
            pushi 106
            pushi 288
            pushi 121
            callk Display, 22
            pTos uiPanel
            ldi 1
            eq?
            bt L_6aab
            pTos uiPanel
            ldi 3
            eq?
            bnt L_6b49
            L_6aab: pTos uiPanel
            ldi 1
            eq?
            bnt L_6ad3
            pushi 288
            push2
            pTos uiDocument
            pTos uiPage
            self 8
            sat 2
            pushi 3
            pushi 200
            lst 2
            lea uiReadBuffer
            push
            callk GetFarText, 6
            jmp L_6ae3
            L_6ad3: push2
            lea uiReadBuffer
            push
            lea uiInline
            push
            callk StrCpy, 4
            L_6ae3: pushi 4
            lea uiMeasure
            push
            lea uiReadBuffer
            push
            push0
            pushi 288
            callk TextSize, 8
            lsl 1670
            ldi 112
            le?
            bnt L_6b29
            lsl 1671
            ldi 288
            le?
            bnt L_6b29
            pushi 11
            lea uiReadBuffer
            push
            pushi 100
            pushi 16
            pushi 44
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 288
            pushi 121
            callk Display, 22
            jmp L_6b49
            L_6b29: ldi 8
            aTop uiFailure
            pushi 11
            lofss "PAGE OVERFLOW. NO TEXT WAS CLIPPED.\nBUILD REQUIRES REPAGINATION."
            pushi 100
            pushi 16
            pushi 44
            pushi 102
            push2
            pushi 105
            push0
            pushi 106
            pushi 288
            pushi 121
            callk Display, 22
            L_6b49: ldi 0
            sat 0
            L_6b4d: lst 0
            pToa uiControlCount
            lt?
            bnt L_6d5e
            lat 0
            lali 164
            sat 1
            lat 0
            lali 548
            sat 6
            lst 1
            ldi 1
            eq?
            bt L_6b73
            lst 1
            ldi 18
            eq?
            bnt L_6c11
            L_6b73: pToa uiReveal
            bt L_6b81
            lst 0
            pToa uiFocus
            eq?
            bnt L_6c0e
            L_6b81: pushi 294
            pushi 5
            lat 0
            lsli 292
            lat 0
            lsli 356
            lat 0
            lsli 420
            lat 0
            lsli 484
            pushi 13
            self 14
            pushi 4
            lea uiMeasure
            push
            lst 6
            push0
            lat 0
            lsli 484
            lat 0
            lali 356
            sub
            push
            ldi 4
            sub
            push
            callk TextSize, 8
            lsl 1670
            ldi 8
            le?
            bnt L_6c0e
            lsl 1670
            lat 0
            lsli 420
            lat 0
            lali 292
            sub
            push
            ldi 4
            sub
            le?
            bnt L_6c0e
            pushi 11
            lst 6
            pushi 100
            lat 0
            lsli 356
            ldi 2
            add
            push
            lat 0
            lsli 292
            ldi 2
            add
            push
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            lat 0
            lsli 484
            lat 0
            lali 356
            sub
            push
            ldi 4
            sub
            push
            pushi 121
            callk Display, 22
            L_6c0e: jmp L_6d0e
            L_6c11: lst 1
            ldi 9
            ne?
            bnt L_6d0e
            lst 1
            ldi 13
            eq?
            bnt L_6c87
            lat 0
            lali 228
            sat 3
            pushi 11
            lat 3
            lali 676
            bnt L_6c35
            lofsa "[X]"
            jmp L_6c38
            L_6c35: lofsa "[ ]"
            L_6c38: push
            pushi 100
            lat 0
            lsli 356
            ldi 3
            add
            push
            lat 0
            lsli 292
            ldi 3
            add
            push
            pushi 102
            push2
            pushi 105
            push0
            pushi 106
            pushi 20
            pushi 121
            callk Display, 22
            pushi 11
            lst 6
            pushi 100
            lat 0
            lsli 356
            ldi 24
            add
            push
            lat 0
            lsli 292
            ldi 3
            add
            push
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 260
            pushi 121
            callk Display, 22
            jmp L_6d0e
            L_6c87: pushi 4
            lea uiMeasure
            push
            lst 6
            push0
            lat 0
            lsli 484
            lat 0
            lali 356
            sub
            push
            ldi 4
            sub
            push
            callk TextSize, 8
            lsl 1670
            lat 0
            lsli 420
            lat 0
            lali 292
            sub
            push
            ldi 2
            sub
            le?
            bnt L_6d09
            pushi 11
            lst 6
            pushi 100
            lat 0
            lsli 356
            ldi 2
            add
            push
            lat 0
            lsli 292
            ldi 2
            add
            push
            pushi 102
            lst 1
            ldi 2
            eq?
            bnt L_6cea
            lat 0
            lsli 228
            pToa uiVerb
            eq?
            bnt L_6cea
            ldi 2
            jmp L_6cec
            L_6cea: ldi 1
            L_6cec: push
            pushi 105
            push0
            pushi 106
            lat 0
            lsli 484
            lat 0
            lali 356
            sub
            push
            ldi 4
            sub
            push
            pushi 121
            callk Display, 22
            jmp L_6d0e
            L_6d09: ldi 9
            aTop uiFailure
            L_6d0e: lst 0
            pToa uiFocus
            eq?
            bnt L_6d59
            pushi 294
            pushi 5
            lat 0
            lsli 292
            lat 0
            lsli 356
            lat 0
            lsli 420
            lat 0
            lsli 484
            push2
            self 14
            pushi 9
            pushi 11
            lat 0
            lsli 292
            lat 0
            lsli 356
            lat 0
            lsli 292
            ldi 3
            add
            push
            lat 0
            lsli 356
            ldi 3
            add
            push
            push1
            push1
            push0
            push0
            callk Graph, 18
            L_6d59: +at 0
            jmp L_6b4d
            L_6d5e: pToa uiFailure
            bnt L_6da3
            pushi 9
            pushi 11
            pushi 116
            pushi 8
            pushi 134
            pushi 312
            push1
            push0
            push0
            push0
            callk Graph, 18
            pushi 3
            lea t7
            push
            lofss "UI CONTRACT ERROR %d"
            pTos uiFailure
            callk Format, 6
            pushi 11
            lea t7
            push
            pushi 100
            pushi 16
            pushi 120
            pushi 102
            push2
            pushi 105
            push0
            pushi 106
            pushi 288
            pushi 121
            callk Display, 22
            L_6da3: ret
        )
    )

    ; Delivered offset0x6da4; 12 original instructions
    (method (uiAfterRestore)
        ; Rebuild transient records/pointer coordinates, preserving valid modal
        ; page/choices and sentence. Call AFTER the guarded host audio restore.
        (= uiLastX x) (= uiLastY y) (= uiReveal 0)
        (self uiBuildFocus:) (= dirty 1)
    )

    ; Delivered offset0x6dbf; 30 original instructions
    (method (bridgeCancelReading reason &tmp i)
        (if bridgePendingObject
            (++ bridgeCancelledSerial) (= bridgeLastCancelReason reason))
        (= bridgePendingObject 0) (= bridgePendingDocument 0)
        (= bridgePendingRecord 0) (= bridgePendingPages 0) (= bridgePendingRoom -1)
        (= bridgeVisitedCount 0)
        (for ((= i 0)) (< i 64) ((++ i)) (= [bridgeVisited i] 0)))

    ; Delivered offset0x6e02; 40 original instructions
    (method (bridgeBegin)
(if p08 (p08 h8ReaderRetire: 1))

(if p07 (p07 h7CancelReader:) (p07 h7RetireLaugh:))

(if p06 (p06 h6CancelReader:))

(if p05 (p05 hCancelReader:))

        (if p04 (p04 qCancel:))
        (asm
            ldi 0
            aTop navNotice
            ldi 0
            aTop navNoticeTicks
            pToa p03
            bnt L_6e16
            pushi 510
            push0
            pToa p03
            send 4
            L_6e16: ldi 0
            aTop p03WantCredit
            ldi 0
            aTop p03WantTopics
            pToa dialogue
            bnt L_6e2a
            pushi 487
            push0
            pToa dialogue
            send 4
            L_6e2a: pushi 377
            push0
            self 4
            pushi 167
            push0
            self 4
            bnt L_6e3c
            ldi 0
            aTop currentCaption
            L_6e3c: pushi 60
            push1
            push2
            self 6
            ldi 0
            aTop bridgeQueueCount
            ldi 0
            aTop bridgeQueueIndex
            ldi 0
            aTop bridgeWantPlan
            ret
        )
    )

    ; Delivered offset0x6e52; 42 original instructions
    (method (bridgeQueueDocument arg1)
        (asm
            pToa bridgeSilent
            bnt L_6e5a
            ldi 0
            ret
            L_6e5a: lsp 1
            ldi 0
            le?
            bt L_6e70
            pushi 288
            push2
            lsp 1
            push0
            self 8
            push
            ldi 0
            lt?
            bnt L_6e78
            L_6e70: ldi 1
            aTop bridgeFailure
            ldi 0
            ret
            L_6e78: pTos bridgeQueueCount
            ldi 32
            ge?
            bnt L_6e88
            ldi 2
            aTop bridgeFailure
            ldi 0
            ret
            L_6e88: pToa dialogue
            bnt L_6e98
            pushi 489
            push2
            pTos bridgeQueueCount
            push0
            pToa dialogue
            send 8
            L_6e98: lsp 1
            pToa bridgeQueueCount
            sali 1769
            ipToa bridgeQueueCount
            ret
        )
    )

    ; Delivered offset0x6ea4; 65 original instructions
    (method (bridgeShowNext &tmp t0 t1)
        (asm
            pTos bridgeQueueIndex
            pToa bridgeQueueCount
            ge?
            bnt L_6eb2
            ldi 0
            ret
            L_6eb2: pToa bridgeQueueIndex
            lali 1769
            sat 0
            pToa dialogue
            bnt L_6ecb
            pushi 488
            push1
            pTos bridgeQueueIndex
            pToa dialogue
            send 6
            jmp L_6ecd
            L_6ecb: ldi 0
            L_6ecd: sat 1
            ipToa bridgeQueueIndex
            lat 1
            bnt L_6efc
            pToa dialogue
            bnt L_6efc
            pushi 491
            push1
            lst 0
            pToa dialogue
            send 6
            push
            ldi 0
            ge?
            bnt L_6efc
            pushi 405
            push1
            lst 0
            self 6
            bnt L_6efc
            ldi 1
            aTop bridgeReaderActive
            ldi 1
            ret
            L_6efc: lst 0
            ldi 343
            ge?
            bnt L_6f19
            lst 0
            ldi 420
            le?
            bnt L_6f19
            ldi 5
            aTop bridgeFailure
            ldi 10
            aTop uiFailure
            ldi 0
            ret
            L_6f19: pushi 326
            push1
            lst 0
            self 6
            bnt L_6f28
            ldi 1
            aTop bridgeReaderActive
            L_6f28: ret
        )
    )

    ; Delivered offset0x6f29; 26 original instructions
    (method (bridgeFlush)
        ; Build requested choices first, then put the full exchange over them.
        (if bridgeWantPlan (self bridgeBuildPlan:) (= bridgeWantPlan 0))
        (if (and (== uiChoiceContext 201) (not p02PlanOpen) p02PlanAgreed)
            (= uiPanel 0) (= uiBackPanel 0))
        (self bridgeShowNext:) (= dirty 1))

    ; Delivered offset0x6f61; 210 original instructions
    (method (bridgeActAtArrival action obj target)
(if ((ScriptID 996 0) h14Dispatch: action obj target) (return 0))

(if ((ScriptID 995 0) h13Dispatch: action obj target) (return 0))

(if ((ScriptID 994 0) h12Dispatch: action obj target) (return 0))

(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)

(if ((ScriptID 993 0) h11Dispatch: action obj target) (return 0))

(if ((ScriptID 992 0) h10Dispatch: action obj target) (return 0))

(if (and p09 (p09 h9Dispatch: action obj target)) (return 0))

(if (and p08 (p08 h8RouteBlock: action obj target)) (return 0))

(if (and p08 (p08 h8ActionBarrier:)) (return 0))

(if (and p07 (p07 h7Barrier:)) (return 0))

(if (and p06 (p06 h6Barrier:)) (return 0))

(if (and p05 (p05 hBarrier:)) (return 0))

        (if p04Invalid (return 0))
        (if p03Invalid (return 0))
        (if (and p03 (or (and (== obj 11) onApron)
            (and (== action 0) (or (== obj 9) (!= (self p02Exit: obj) -1)))))
            (if (not (p03 bBeforeTravel: self))
                (self p03HostFinish:) (return 0)))
        (if (and p08 (p08 h8Dispatch: action obj target)) (return 0))
(if (and p06 (p06 h6Dispatch: action obj target)) (return 0))
(if (and p07 (p07 h7Dispatch: action obj target)) (return 0))
(if (and p05 (p05 hDispatch: action obj target)) (return 0))
(self bridgeBegin:)
        (if (and p04 (== action 6) (== obj 54) (== target 0)
            (== location 3) (not onApron) p02PlanAgreed
            (or (p04 p04IntroHi?) (p04 p04IntroLo?)))
            (self p04BuildTopics:) (return 0))
        (if (and p04 (p04 qDispatch: self action obj target))
            (self p04HostFinish:) (return 0))
        (if (and p04 p02PlanAgreed (== obj 32) (== target 0) (or (== action 2) (== action 5)))
            (self p04BuildJournal:) (return 0))
        (if (== obj -103)
            (if (and (== location 2) (not onApron))
                (self uiOpenInline: (self p03Label: -103) (self p03KitchenDescription:)))
            (return 0))
        (if (and p03 (p03 bDispatch: self action obj target))
            (self p03HostFinish:) (return 0))
        (if (and p03 p02PlanAgreed (== obj 32) (== target 0) (or (== action 2) (== action 5)))
            (self p03BuildJournal:) (return 0))
        ; p02Read is a completed whole-source observation. Defer that call until
        ; actual successful display of every page, rather than opening a reader.
        (if (and (self p02Available:) (== target 0) (or (== action 2) (== action 5)))
            (if (or (and (>= obj 20) (<= obj 22)) (== obj 24) (== obj 31))
                (self bridgeRequestRead: obj 0) (return 0))
            (if (and (== obj 6) (== p02CopyJack 13))
                (self bridgeRequestRead: 20 0) (return 0)))
        (if (and (== action 6) (== target 0) (self p02Available:)
            (or (== obj 2) (== obj 8) (== obj 28) (== obj 29)))
            (self p02OpenTopics: obj) (self bridgeFlush:) (return 0))
        (self p02Act: action obj target) (self bridgeFlush:))

    ; Delivered offset0x70d9; 84 original instructions
    (method (bridgeRequestRead obj record &tmp document pages i)
        (self bridgeCancelReading: 2)
        (if (not (self p02DocumentAvailable: obj record))
            (self p02HostText: 105 obj) (self bridgeFlush:) (return 0))
        (= document (self bridgeObjectDocument: obj)) (= pages (self uiDocCount: document))
        (if (or (<= document 0) (< pages 1) (> pages 64)) (= bridgeFailure 3) (return 0))
        (= bridgePendingObject obj) (= bridgePendingDocument document)
        (= bridgePendingRecord record) (= bridgePendingPages pages) (= bridgePendingRoom location)
        (= bridgeVisitedCount 0)
        (for ((= i 0)) (< i 64) ((++ i)) (= [bridgeVisited i] 0))
        (if (self uiOpenReader: document) (= bridgeReaderActive 1)
        else (self bridgeCancelReading: 4)))

    ; Delivered offset0x717c; 83 original instructions
    (method (bridgePageRendered document page &tmp obj record)
        ; Invoke only after uiRender and successful full-screen Graph12, with
        ; the exact page that was painted. A page-change intent is insufficient.
        (if (or (not bridgePendingObject) (!= uiPanel 1) uiFailure bridgeFailure
            (!= document bridgePendingDocument) (!= document uiDocument)
            (!= page uiPage) (< page 0) (>= page bridgePendingPages)) (return 0))
        (if (not (self p02DocumentAvailable: bridgePendingObject bridgePendingRecord))
            (self bridgeCancelReading: 3) (return 0))
        (if (not [bridgeVisited page]) (= [bridgeVisited page] 1) (++ bridgeVisitedCount))
        (if (< bridgeVisitedCount bridgePendingPages) (return 0))
        (= obj bridgePendingObject) (= record bridgePendingRecord)
        ; Clear pending first; repeated render/restore cannot replay a commit.
        (= bridgePendingObject 0) (= bridgePendingDocument 0) (= bridgePendingPages 0)
        (= bridgeCommitRead 1)
        (self p02Read: obj record)
        (= bridgeCommitRead 0) (++ bridgeReadSerial)
        (return 1))

    ; Delivered offset0x7229; 33 original instructions
    (method (bridgeAfterRestore)
        ; Restore is observational. Rebuild caches and keep visited-page state,
        ; but never commit knowledge or replay callbacks here.
        (++ bridgeRestoreSerial) (= bridgeCommitRead 0)
        (self p02HostInventory:) (self uiAfterRestore:)
        (if bridgePendingObject
            (if (or (!= uiPanel 1) (!= uiDocument bridgePendingDocument)
                (not (self p02DocumentAvailable: bridgePendingObject bridgePendingRecord)))
                (self bridgeCancelReading: 5)))
        (= dirty 1))

    ; Delivered offset0x726f; 54 original instructions
    (method (p02HostInventory &tmp h10Page) (= h10Page uiInventoryPage) (self h6BaseInventory: ) (if p06 (p06 h6Inventory:))
 (if (and p09 (not (p09 h9ProjectCard:))) (= uiFailure 10) (= dirty 1) (return 0)) (if (not ((ScriptID 992 0) h10Proj:)) (= uiFailure 10) (return 0)) (if (and (>= h10Page 0) (< h10Page uiInventoryPages)) (= uiInventoryPage h10Page)) (return 1))

    ; Delivered offset0x72dd; 28 original instructions
    (method (p02HostText arg1 arg2)
        (asm
            lsp 1
            ldi 129
            eq?
            bt L_72f5
            lsp 1
            ldi 130
            eq?
            bt L_72f5
            lsp 1
            ldi 134
            eq?
            bnt L_7300
            L_72f5: pushi 740
            push2
            lsp 1
            lsp 2
            self 8
            ret
            L_7300: pushi 399
            push1
            pushi 68
            push2
            lsp 1
            lsp 2
            self 8
            push
            self 6
            ret
        )
    )

    ; Delivered offset0x7311; 13 original instructions
    (method (p02HostDocument obj record)
        ; Direct domain observations have already committed. bridgeActAtArrival
        ; intercepts player document reads so no first-page callback grants lore.
        (if bridgeCommitRead (return 0))
        (self bridgeQueueDocument: (self bridgeObjectDocument: obj)))

    ; Delivered offset0x7327; 9 original instructions
    (method (p02HostExchange arg1)
        (asm
            pushi 399
            push1
            pushi 64
            push1
            lsp 1
            self 6
            push
            self 6
            ret
        )
    )

    ; Delivered offset0x7336; 68 original instructions
    (method (p02HostTopics actor) (self h6BaseTopics: actor) (if (and p06 (== actor 8) p02PlanAgreed) (self uiAddChoice: 11 "Ask about the spare sheet" 0 1)) (return 1))

    ; Delivered offset0x73b5; 6 original instructions
    (method (p02HostPlan) (if (not bridgeSilent) (= bridgeWantPlan 1)))

    ; Delivered offset0x73c1; 38 original instructions
    (method (bridgeBuildPlan &tmp aim)
        (if (not p02PlanOpen) (return 0))
        (= bridgeReaderActive 0)
        (self uiClearChoices: "EDIT HOUSEHOLD PLAN" 201 1)
        (for ((= aim 1)) (<= aim 5) ((++ aim))
            (self uiAddChoice: aim (self bridgeAimLabel: aim) (self p02AimSelected: aim) 1)))

    ; Delivered offset0x740a; 90 original instructions
    (method (p02HostJournal observed agreed &tmp obj)
        ; Build only read-only available records. Opening the journal grants none.
        (if bridgeSilent (return 0))
        (= bridgeReaderActive 0)
        (self uiClearChoices: "RECORDED INVITATION EVIDENCE" 203 0)
        (for ((= obj 20)) (<= obj 24) ((++ obj))
            (if (self p02DocumentAvailable: obj 1)
                (self uiAddChoice: obj (self uiDocTitle: (self bridgeObjectDocument: obj)) 0 1)))
        (if (& observed 16) (self uiAddChoice: 26 "MATCHED BORDER COMPARISON" 0 1))
        (if (& observed 32) (self uiAddChoice: 33 "STRINGER'S INSPECTION EXPECTATION" 0 1))
        (if (self p02DocumentAvailable: 31 1)
            (self uiAddChoice: 31 (self uiDocTitle: 5) 0 1))
        (if (== uiChoiceCount 0) (self bridgeQueueDocument: 342)))

    ; Delivered offset0x74b5; 5 original instructions
    (method (p02HostBundle)
        (self bridgeQueueDocument: 341))

    ; Delivered offset0x74be; 181 original instructions
    (method (uiHostChoice context id &tmp aim selected)
(if ((ScriptID 996 0) h14Choice: context id) (return 0))

(if ((ScriptID 995 0) h13Choice: context id) (return 0))

(if ((ScriptID 994 0) h12Choice: context id) (return 0))

(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)

(if ((ScriptID 993 0) h11Choice: context id) (return 0))

(if ((ScriptID 992 0) h10Choice: context id) (return 0))

(if (and p09 (p09 h9Choice: context id)) (return 0))

(if (and p08 (== context 208) (or (== id 103) (== id 104)) (>= (p08 h8V: 1 0) 5)) (p08 h8GB: id) (return 0))

(if (and p08 (p08 h8RouteChoice: context)) (return 0))

(if (and p08 (p08 h8LayoutChoice: context id)) (return 0))

(if (and p08 (p08 h8ActionBarrier:)) (return 0))

(if (and p07 (p07 h7Choice: context id)) (return 0)) (if (and p07 (p07 h7Barrier:)) (return 0))

(if (and p06 (p06 h6Choice: context id)) (return 0)) (if (and p06 (p06 h6Barrier:)) (return 0))

(if (and p05 (p05 hVCChoice: context id)) (return 0)) (if (and p05 (p05 hBarrier:)) (return 0)) (if (and p05 (p05 hChoice: context id)) (return 0))

        (if (or (== context 207) (== context 208))
            (self bridgeBegin:) (p04 qFailure: 0)
            (if (== context 207) (p04 qRun: self 2 id 54 0)
            else (switch id
                (100 (self p02HostJournal: p02Observed p02PlanAgreed))
                (101 (self p03BuildJournal:))
                (else (self p04Journal: id))))
            (self p04HostFinish:) (return 0))
        (self bridgeBegin:)
        (if (and (>= context 204) (<= context 206))
            (switch context
                (204 (p03 bSelect: self id))
                (205 (p03 bTopic: self p03TopicActor id))
                (206 (if (== id 100)
                    (self p02HostJournal: p02Observed p02PlanAgreed)
                else (p03 bJournal: self id))))
            (self p03HostFinish:) (return 0))
        (if (and (== context 202) (== id 10))
            (self p03BuildTopics: bridgeChoiceActor) (return 0))
        (switch context
            (201
                (if (not p02PlanOpen) (return 0))
                (= selected (not (self p02AimSelected: id)))
                (self p02SelectAim: id selected)
                (for ((= aim 1)) (<= aim 5) ((++ aim))
                    (self uiSetChoice: aim (self p02AimSelected: aim))))
            (202 (self p02Topic: bridgeChoiceActor id))
            (203
                (if (or (and (>= id 20) (<= id 22)) (== id 24) (== id 31))
                    (self bridgeRequestRead: id 1) (return 0))
                (if (and (== id 26) (& p02Observed 16))
                    (self bridgeQueueDocument: 7))
                (if (and (== id 33) (& p02Observed 32))
                    (self bridgeQueueDocument: 22))))
        (self bridgeFlush:))

    ; Delivered offset0x760c; 16 original instructions
    (method (uiHostConfirm context)
(if (and p08 (p08 h8RouteChoice: context)) (return 0))

(if (and p08 (p08 h8ActionBarrier:)) (return 0))

(if (and p07 (p07 h7Barrier:)) (return 0))

(if (and p06 (p06 h6Barrier:)) (return 0))

(if (and p05 (p05 hBarrier:)) (return 0))

        (if (!= context 201) (return 0))
        (self bridgeBegin:) (self p02ConfirmPlan:) (self bridgeFlush:))

    ; Delivered offset0x7628; 56 original instructions
    (method (uiHostClosed)
((ScriptID 996 0) h14Retire:)

((ScriptID 995 0) h13Retire:)
((ScriptID 995 0) h13Cancel:)

((ScriptID 994 0) h12Retire:)

(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)

((ScriptID 993 0) h11Retire:)
((ScriptID 993 0) h11PayClosed:)

((ScriptID 992 0) h10Retire:)

(if p09 (p09 h9Closed:))

(if p08 (p08 h8ReaderClosed:))

        (if p04 (p04 qClosed: self))
        (if p03
            ; uiClose already restored panel/back state, uiDocument is still old.
            (if (not (p03 bClosed: self))
                (= p03HostError (p03 bFailure?))
                (if (p03 p03Open?) (self p03BuildCredit:))
                (= uiFailure 10) (= dirty 1) (return 0)))
        ; uiClose has already consumed the key/click and restored its Back panel.
        ; Never commit merely because a reader was closed.
        (if bridgeReaderActive
            (self bridgeCancelReading: 1) (= bridgeReaderActive 0)
            (self bridgeShowNext:)
        else
            (if (and (== uiChoiceContext 201) p02PlanOpen)
                (= bridgeSilent 1) (self p02CancelPlan:) (= bridgeSilent 0)))
        (= dirty 1)
(if p05 (p05 hClosed:))

(if p06 (p06 h6Closed:))

(if p07 (p07 h7Closed:))
)

    ; Delivered offset0x769a; 6 original instructions
    (method (uiDocTitle arg1)
        (asm
            pushi 289
            push1
            lsp 1
            pToa dialogue
            send 6
            ret
        )
    )

    ; Delivered offset0x76a5; 6 original instructions
    (method (uiDocCount arg1)
        (asm
            pushi 287
            push1
            lsp 1
            pToa dialogue
            send 6
            ret
        )
    )

    ; Delivered offset0x76b0; 7 original instructions
    (method (uiDocEntry arg1 arg2)
        (asm
            pushi 288
            push2
            lsp 1
            lsp 2
            pToa dialogue
            send 8
            ret
        )
    )

    ; Delivered offset0x76bd; 38 original instructions
    (method (bridgeObjectDocument obj)
        (switch obj
            (20 (return 1))
            (21 (return 2))
            (22 (return 3))
            (24 (return 4))
            (31 (return 5))
        )
        (return 0))

    ; Delivered offset0x76f8; 150 original instructions
    (method (bridgeExchangeDocument exchange)
        (switch exchange
            (6 (return 6))
            (7 (return 7))
            (8 (return 8))
            (9 (return 9))
            (10 (return 10))
            (11 (return 11))
            (12 (return 12))
            (13 (return 13))
            (14 (return 14))
            (15 (return 15))
            (16 (return 16))
            (17 (return 17))
            (18 (return 18))
            (19 (return 19))
            (20 (return 20))
            (21 (return 21))
            (22 (return 22))
            (23 (return 23))
            (24 (return 24))
            (25 (return 25))
            (26 (return 26))
        )
        (return 0))

    ; Delivered offset0x77ec; 6 original instructions
    (method (bridgeActorTitle arg1)
        (asm
            pushi 55
            push1
            lsp 1
            pToa dialogue
            send 6
            ret
        )
    )

    ; Delivered offset0x77f6; 6 original instructions
    (method (bridgeTopicLabel arg1)
        (asm
            pushi 85
            push1
            lsp 1
            pToa dialogue
            send 6
            ret
        )
    )

    ; Delivered offset0x7800; 6 original instructions
    (method (bridgeAimLabel arg1)
        (asm
            pushi 57
            push1
            lsp 1
            pToa dialogue
            send 6
            ret
        )
    )

    ; Delivered offset0x780a; 1378 original instructions
    (method (bridgeMessageDocument messageId arg)
        (switch messageId
            (1 (return 159))
            (2 (return 160))
            (3 (return 161))
            (4 (return 162))
            (5 (return 163))
            (6 (return 164))
            (7 (return 165))
            (8 (return 166))
            (9 (return 167))
            (10 (return 168))
            (11 (return 169))
            (12 (return 170))
            (13 (return 171))
            (14 (return 172))
            (15 (return 173))
            (16 (return 174))
            (17 (return 175))
            (18 (return 176))
            (19 (return 177))
            (20 (return 178))
            (21 (return 179))
            (22 (return 180))
            (23 (return 181))
            (24 (return 182))
            (25 (return 183))
            (26 (return 184))
            (27 (return 185))
            (28 (return 186))
            (29 (return 187))
            (30 (return 188))
            (31 (return 189))
            (32 (return 190))
            (33 (switch arg (0 (return 191)) (1 (return 192)) (2 (return 193)) (3 (return 194)) (4 (return 195)) (5 (return 196)) (6 (return 197)) (7 (return 198))) (return 191))
            (34 (return 199))
            (35 (return 200))
            (36 (return 201))
            (37 (return 202))
            (38 (return 203))
            (39 (return 204))
            (40 (return 205))
            (41 (return 206))
            (42 (return 207))
            (43 (return 208))
            (44 (return 209))
            (45 (return 210))
            (46 (return 211))
            (47 (return 212))
            (48 (return 213))
            (49 (return 214))
            (50 (return 215))
            (51 (return 216))
            (52 (switch arg (1 (return 217)) (2 (return 218)) (3 (return 219))) (return 217))
            (53 (switch arg (1 (return 220)) (2 (return 221)) (3 (return 222))) (return 220))
            (54 (return 223))
            (55 (return 224))
            (56 (switch arg (0 (return 225)) (1 (return 226)) (2 (return 227)) (3 (return 228)) (4 (return 229)) (5 (return 230)) (6 (return 231))) (return 225))
            (57 (return 232))
            (58 (return 233))
            (59 (return 234))
            (60 (return 235))
            (61 (return 236))
            (62 (return 237))
            (63 (return 238))
            (64 (return 239))
            (65 (return 240))
            (66 (return 241))
            (67 (return 242))
            (68 (return 243))
            (69 (return 244))
            (70 (return 245))
            (71 (return 246))
            (72 (return 247))
            (73 (return 248))
            (74 (return 249))
            (75 (return 250))
            (76 (return 251))
            (77 (return 252))
            (78 (return 253))
            (79 (return 254))
            (80 (return 255))
            (81 (switch arg (0 (return 256)) (1 (return 257)) (2 (return 258)) (3 (return 259)) (4 (return 260)) (5 (return 261)) (6 (return 262)) (7 (return 263))) (return 256))
            (82 (return 264))
            (83 (return 265))
            (84 (return 266))
            (85 (return 267))
            (86 (return 268))
            (87 (return 269))
            (88 (return 270))
            (89 (return 271))
            (90 (return 272))
            (91 (return 273))
            (92 (return 274))
            (93 (return 275))
            (94 (return 276))
            (95 (return 277))
            (96 (return 278))
            (97 (return 279))
            (98 (return 280))
            (99 (return 281))
            (100 (return 282))
            (101 (return 283))
            (102 (return 284))
            (103 (return 285))
            (104 (return 286))
            (105 (return 287))
            (106 (return 288))
            (107 (return 289))
            (108 (return 290))
            (109 (return 291))
            (110 (return 292))
            (111 (return 293))
            (112 (return 294))
            (113 (switch arg (0 (return 295)) (1 (return 296))) (return 295))
            (114 (switch arg (0 (return 297)) (1 (return 298))) (return 297))
            (115 (switch arg (0 (return 299)) (1 (return 300))) (return 299))
            (116 (return 301))
            (117 (return 302))
            (118 (return 303))
            (119 (return 304))
            (120 (return 305))
            (121 (return 306))
            (122 (return 307))
            (123 (return 308))
            (124 (return 309))
            (125 (return 310))
            (126 (return 311))
            (127 (return 312))
            (128 (return 313))
            (129 (return 314))
            (130 (return 315))
            (131 (return 316))
            (132 (return 317))
            (133 (return 318))
            (134 (switch arg (0 (return 319)) (1 (return 320)) (2 (return 321)) (3 (return 322)) (4 (return 323)) (5 (return 324)) (6 (return 325))) (return 319))
            (135 (return 326))
            (136 (return 327))
            (137 (return 328))
            (138 (return 329))
            (139 (return 330))
            (140 (switch arg (0 (return 331)) (1 (return 332))) (return 331))
            (141 (switch arg (0 (return 333)) (1 (return 334))) (return 333))
            (142 (= arg (self p02AimSelected: arg)) (switch arg (0 (return 335)) (1 (return 336))) (return 335))
            (143 (return 337))
            (144 (return 338))
            (145 (return 339))
            (146 (return 340))
        )
        (return 0))

    ; Delivered offset0x81db; 52 original instructions
    (method (livingPerson who)
 (return ((ScriptID 991 0) livingPerson: self who)))

    ; Delivered offset0x8240; 173 original instructions
    (method (drawLiving)
 (return ((ScriptID 991 0) drawLiving: self)))

    ; Delivered offset0x8388; 18 original instructions
    (method (voiceOff)
(if p07 (p07 h7RetireLaugh:))

(if p05 (p05 hStageRetire:)) 

        (asm
            pushi 373
            push2
            push1
            pushi 391
            push0
            pToa presentation
            send 4
            not
            push
            pToa presentation
            send 8
            ldi 1
            aTop dirty
            pushi 383
            push1
            lofss "voice setting"
            self 6
            ret
        )
    )

    ; Delivered offset0x83aa; 37 original instructions
    (method (voiceAdjust arg1 &tmp t0)
        (asm
            pushi 394
            push0
            pToa presentation
            send 4
            push
            lap 1
            add
            sat 0
            lst 0
            ldi 0
            lt?
            bnt L_83c5
            ldi 0
            sat 0
            L_83c5: lst 0
            ldi 100
            gt?
            bnt L_83d0
            ldi 100
            sat 0
            L_83d0: pushi 394
            push1
            lst 0
            pToa presentation
            send 6
            pushi 370
            push0
            pToa presentation
            send 4
            ldi 1
            aTop dirty
            pushi 383
            push1
            lofss "voice setting"
            self 6
            ret
        )
    )

    ; Delivered offset0x83f1; 117 original instructions
    (method (speechTrace arg1 &tmp t0 t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13 t14 t15 t16 t17 t18 t19 t20 t21 t22 t23 t24 t25 t26 t27 t28 t29 t30 t31 t32 t33 t34 t35 t36 t37 t38 t39 t40 t41 t42 t43 t44 t45 t46 t47 t48 t49 t50 t51 t52 t53 t54 t55 t56 t57 t58 t59 t60 t61 t62 t63 t64 t65 t66 t67 t68 t69 t70 t71 t72 t73 t74 t75 t76 t77 t78 t79 t80 t81 t82 t83 t84 t85 t86 t87 t88 t89 t90 t91 t92 t93 t94 t95 t96 t97 t98 t99 t100 t101 t102 t103 t104 t105 t106 t107 t108 t109 t110 t111 t112 t113 t114 t115 t116 t117 t118 t119 t120 t121 t122 t123 t124 t125 t126 t127 t128 t129 t130 t131 t132 t133 t134 t135 t136 t137 t138 t139 t140 t141 t142 t143 t144 t145 t146 t147 t148 t149 t150 t151 t152 t153 t154 t155 t156 t157 t158 t159 t160 t161 t162 t163 t164 t165 t166 t167 t168 t169 t170 t171 t172 t173 t174 t175 t176 t177 t178 t179 t180 t181 t182 t183 t184 t185 t186 t187 t188 t189 t190 t191 t192 t193 t194 t195 t196 t197 t198 t199 t200 t201 t202 t203 t204 t205 t206 t207 t208 t209 t210 t211 t212 t213 t214 t215 t216 t217 t218 t219 t220 t221 t222 t223 t224 t225 t226 t227 t228 t229 t230 t231 t232)
        (asm
            pToa presentation
            not
            bnt L_83fc
            ldi 0
            ret
            L_83fc: pushi 3
            lea t0
            push
            lofss "speech%04d.csv"
            pTos talkLogIndex
            callk Format, 6
            L_840a: push2
            pushi 10
            lea t0
            push
            callk FileIO, 4
            bnt L_8428
            ipToa talkLogIndex
            pushi 3
            lea t0
            push
            lofss "speech%04d.csv"
            pTos talkLogIndex
            callk Format, 6
            jmp L_840a
            L_8428: pushi 19
            lea t32
            push
            lofss "%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n"
            lsp 1
            push0
            callk GetTime, 0
            push
            pushi 364
            push0
            pToa presentation
            send 4
            push
            pTos currentCaption
            pTos speechCaption
            pTos speechPart
            pushi 388
            push0
            pToa presentation
            send 4
            push
            pushi 347
            push0
            pToa presentation
            send 4
            push
            pushi 375
            push0
            pToa presentation
            send 4
            push
            pushi 362
            push0
            pToa presentation
            send 4
            push
            pushi 365
            push0
            pToa presentation
            send 4
            push
            pushi 391
            push0
            pToa presentation
            send 4
            push
            pushi 394
            push0
            pToa presentation
            send 4
            push
            pTos masterVolume
            pushi 374
            push0
            pToa presentation
            send 4
            push
            pushi 393
            push0
            pToa presentation
            send 4
            push
            pushi 390
            push0
            pToa presentation
            send 4
            push
            callk Format, 38
            pushi 3
            push0
            lea t0
            push
            push2
            callk FileIO, 6
            sat 232
            lst 232
            ldi -1
            ne?
            bnt L_84d3
            pushi 3
            pushi 6
            lst 232
            lea t32
            push
            callk FileIO, 6
            push2
            push1
            lst 232
            callk FileIO, 4
            L_84d3: ipToa talkLogIndex
            ret
        )
    )

    ; Delivered offset0x84d6; 26 original instructions
    (method (speechCancel)
(if p05 (p05 hStageRetire:)) 

        (asm
            pToa dialogue
            bnt L_84e5
            pushi 475
            push2
            push0
            pushi 20
            pToa dialogue
            send 8
            L_84e5: ldi 0
            aTop speechCaption
            ldi 0
            aTop speechPart
            pToa presentation
            bnt L_84fa
            pushi 343
            push1
            push1
            pToa presentation
            send 6
            L_84fa: ldi 1
            aTop dirty
            pushi 383
            push1
            lofss "cancel"
            self 6
            ret
        )
    )

    ; Delivered offset0x8509; 18 original instructions
    (method (speechBegin caption)
    (self speechCancel:)
    (if (or opening (not presentation)) (return 0))
    (= speechCaption caption) (= speechPart 0) (self speechNext:))

    ; Delivered offset0x852a; 31 original instructions
    (method (speechNext)
        (asm
            pushi 126
            push1
            pTos masterVolume
            pushi 16
            push1
            pTos audienceVolume
            pToa presentation
            send 12
            pushi 373
            push2
            push2
            pTos audienceMuted
            pToa presentation
            send 8
            pushi 382
            push2
            pTos speechCaption
            pTos speechPart
            self 8
            bnt L_855e
            ipToa speechPart
            pushi 383
            push1
            lofss "start"
            self 6
            jmp L_8566
            L_855e: ldi 0
            aTop speechCaption
            ldi 0
            aTop speechPart
            L_8566: ret
        )
    )

    ; Delivered offset0x8567; 94 original instructions
    (method (speechPoll)
(if (and p08 (p08 h8ActionBarrier:) (not (p08 h8VR: 9 0))) (return 0))

(if p07 (p07 h7AudioTick:))

(if (and p05 (p05 hFailure?)) (return 0)) 

        (asm
            pToa presentation
            not
            bt L_8578
            pToa opening
            bt L_8578
            pToa menuOpen
            bt L_8578
            pToa paused
            bnt L_857b
            L_8578: ldi 0
            ret
            L_857b: pToa uiPanel
            bnt L_85a9
            pTos uiPanel
            ldi 4
            ne?
            bnt L_85a9
            pToa speechCaption
            bt L_85a0
            pushi 347
            push0
            pToa presentation
            send 4
            bt L_85a0
            pushi 365
            push0
            pToa presentation
            send 4
            bnt L_85a6
            L_85a0: pushi 377
            push0
            self 4
            L_85a6: ldi 0
            ret
            L_85a9: pushi 126
            push1
            pTos masterVolume
            pToa presentation
            send 6
            pushi 370
            push0
            pToa presentation
            send 4
            pushi 367
            push2
            push0
            callk GetTime, 0
            push
            pushi 388
            push0
            pToa presentation
            send 4
            push
            pToa presentation
            send 8
            pushi 96
            push0
            pToa presentation
            send 4
            bnt L_85f0
            ldi 1
            aTop dirty
            pushi 96
            push1
            push0
            pToa presentation
            send 6
            pushi 383
            push1
            lofss "mouth"
            self 6
            L_85f0: pToa uiPanel
            not
            bnt L_8619
            pToa speechCaption
            bnt L_8619
            pushi 347
            push0
            pToa presentation
            send 4
            push
            ldi 0
            eq?
            bnt L_8619
            pushi 365
            push0
            pToa presentation
            send 4
            not
            bnt L_8619
            pushi 379
            push0
            self 4
            L_8619: ret
        )
    )

    ; Delivered offset0x861a; 1027 original instructions
    (method (speechStart arg1 arg2)
        (asm
            lsp 1
            dup
            ldi 1
            eq?
            bnt L_864d
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8649
            pushi 390
            push1
            pushi 226
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            push1
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8649: toss
            jmp L_8d33
            L_864d: dup
            ldi 2
            eq?
            bnt L_867e
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_867a
            pushi 390
            push1
            pushi 359
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            push2
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_867a: toss
            jmp L_8d33
            L_867e: dup
            ldi 3
            eq?
            bnt L_86b0
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_86ac
            pushi 390
            push1
            pushi 179
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 3
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_86ac: toss
            jmp L_8d33
            L_86b0: dup
            ldi 4
            eq?
            bnt L_86e2
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_86de
            pushi 390
            push1
            pushi 246
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 4
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_86de: toss
            jmp L_8d33
            L_86e2: dup
            ldi 5
            eq?
            bnt L_8714
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8710
            pushi 390
            push1
            pushi 315
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 5
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8710: toss
            jmp L_8d33
            L_8714: dup
            ldi 6
            eq?
            bnt L_8746
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8742
            pushi 390
            push1
            pushi 345
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 6
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8742: toss
            jmp L_8d33
            L_8746: dup
            ldi 7
            eq?
            bnt L_8778
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8774
            pushi 390
            push1
            pushi 238
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 7
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8774: toss
            jmp L_8d33
            L_8778: dup
            ldi 9
            eq?
            bnt L_87d0
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_87a7
            pushi 390
            push1
            pushi 71
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 8
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            jmp L_87cc
            L_87a7: dup
            ldi 1
            eq?
            bnt L_87cc
            pushi 390
            push1
            pushi 112
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 9
            push1
            push0
            push1
            push2
            pToa presentation
            send 16
            ldi 1
            ret
            L_87cc: toss
            jmp L_8d33
            L_87d0: dup
            ldi 10
            eq?
            bnt L_8802
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_87fe
            pushi 390
            push1
            pushi 143
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 10
            push1
            push0
            push1
            push2
            pToa presentation
            send 16
            ldi 1
            ret
            L_87fe: toss
            jmp L_8d33
            L_8802: dup
            ldi 11
            eq?
            bnt L_8834
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8830
            pushi 390
            push1
            pushi 133
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 11
            push1
            push0
            push1
            push2
            pToa presentation
            send 16
            ldi 1
            ret
            L_8830: toss
            jmp L_8d33
            L_8834: dup
            ldi 12
            eq?
            bnt L_8866
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8862
            pushi 390
            push1
            pushi 188
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 12
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8862: toss
            jmp L_8d33
            L_8866: dup
            ldi 13
            eq?
            bnt L_88c0
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8896
            pushi 390
            push1
            pushi 136
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 13
            push1
            push0
            push1
            push2
            pToa presentation
            send 16
            ldi 1
            ret
            jmp L_88bc
            L_8896: dup
            ldi 1
            eq?
            bnt L_88bc
            pushi 390
            push1
            pushi 144
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 14
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_88bc: toss
            jmp L_8d33
            L_88c0: dup
            ldi 14
            eq?
            bnt L_88f2
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_88ee
            pushi 390
            push1
            pushi 139
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 15
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_88ee: toss
            jmp L_8d33
            L_88f2: dup
            ldi 17
            eq?
            bnt L_8924
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8920
            pushi 390
            push1
            pushi 162
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 16
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8920: toss
            jmp L_8d33
            L_8924: dup
            ldi 19
            eq?
            bnt L_8956
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8952
            pushi 390
            push1
            pushi 174
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 17
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8952: toss
            jmp L_8d33
            L_8956: dup
            ldi 20
            eq?
            bnt L_8987
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8983
            pushi 390
            push1
            pushi 117
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 18
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8983: toss
            jmp L_8d33
            L_8987: dup
            ldi 22
            eq?
            bnt L_89b8
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_89b4
            pushi 390
            push1
            pushi 121
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 19
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_89b4: toss
            jmp L_8d33
            L_89b8: dup
            ldi 24
            eq?
            bnt L_89ea
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_89e6
            pushi 390
            push1
            pushi 166
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 20
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_89e6: toss
            jmp L_8d33
            L_89ea: dup
            ldi 25
            eq?
            bnt L_8a1b
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8a17
            pushi 390
            push1
            pushi 122
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 21
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8a17: toss
            jmp L_8d33
            L_8a1b: dup
            ldi 26
            eq?
            bnt L_8a4c
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8a48
            pushi 390
            push1
            pushi 103
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 22
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8a48: toss
            jmp L_8d33
            L_8a4c: dup
            ldi 27
            eq?
            bnt L_8a7e
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8a7a
            pushi 390
            push1
            pushi 157
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 23
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8a7a: toss
            jmp L_8d33
            L_8a7e: dup
            ldi 28
            eq?
            bnt L_8ab0
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8aac
            pushi 390
            push1
            pushi 147
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 24
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8aac: toss
            jmp L_8d33
            L_8ab0: dup
            ldi 29
            eq?
            bnt L_8ae2
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8ade
            pushi 390
            push1
            pushi 231
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 25
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8ade: toss
            jmp L_8d33
            L_8ae2: dup
            ldi 30
            eq?
            bnt L_8b14
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8b10
            pushi 390
            push1
            pushi 153
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 26
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8b10: toss
            jmp L_8d33
            L_8b14: dup
            ldi 31
            eq?
            bnt L_8b46
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8b42
            pushi 390
            push1
            pushi 231
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 27
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8b42: toss
            jmp L_8d33
            L_8b46: dup
            ldi 32
            eq?
            bnt L_8b78
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8b74
            pushi 390
            push1
            pushi 172
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 28
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8b74: toss
            jmp L_8d33
            L_8b78: dup
            ldi 33
            eq?
            bnt L_8ba9
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8ba5
            pushi 390
            push1
            pushi 92
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 29
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8ba5: toss
            jmp L_8d33
            L_8ba9: dup
            ldi 34
            eq?
            bnt L_8bdb
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8bd7
            pushi 390
            push1
            pushi 318
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 30
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8bd7: toss
            jmp L_8d33
            L_8bdb: dup
            ldi 35
            eq?
            bnt L_8c0d
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8c09
            pushi 390
            push1
            pushi 298
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 31
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8c09: toss
            jmp L_8d33
            L_8c0d: dup
            ldi 39
            eq?
            bnt L_8c3f
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8c3b
            pushi 390
            push1
            pushi 323
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 32
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8c3b: toss
            jmp L_8d33
            L_8c3f: dup
            ldi 40
            eq?
            bnt L_8c70
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8c6c
            pushi 390
            push1
            pushi 66
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 33
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8c6c: toss
            jmp L_8d33
            L_8c70: dup
            ldi 41
            eq?
            bnt L_8ca2
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8c9e
            pushi 390
            push1
            pushi 273
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 34
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8c9e: toss
            jmp L_8d33
            L_8ca2: dup
            ldi 42
            eq?
            bnt L_8cd3
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8cd0
            pushi 390
            push1
            pushi 323
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 35
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8cd0: toss
            jmp L_8d33
            L_8cd3: dup
            ldi 44
            eq?
            bnt L_8d04
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8d01
            pushi 390
            push1
            pushi 262
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 36
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8d01: toss
            jmp L_8d33
            L_8d04: dup
            ldi 55
            eq?
            bnt L_8d33
            lsp 2
            dup
            ldi 0
            eq?
            bnt L_8d32
            pushi 390
            push1
            pushi 129
            pToa presentation
            send 6
            pushi 384
            pushi 6
            pushi 910
            pushi 37
            push1
            push0
            push1
            push1
            pToa presentation
            send 16
            ldi 1
            ret
            L_8d32: toss
            L_8d33: toss
            ldi 0
            ret
        )
    )

    ; Delivered offset0x8d37; 20 original instructions
    (method (bridgeQueueScene document &tmp before)
        (= before bridgeQueueCount) (self bridgeQueueDocument: document)
        (if (and dialogue (> bridgeQueueCount before)) (dialogue sdQueueSet: before 1)))

    ; Delivered offset0x8d5d; 42 original instructions
    (method (dialogueOpen arg1)
(if (not ((ScriptID 993 0) h11ReadBoundary:)) (return 0))

(if (and p08 (p08 h8ReaderCheck: 2 arg1)) (return (p08 h8ReaderOpen: arg1)))

        (asm
            ldi 0
            aTop navNotice
            ldi 0
            aTop navNoticeTicks
            pushi 377
            push0
            self 4
            pushi 331
            push0
            self 4
            pushi 479
            pushi 5
            lsp 1
            pTos uiBackPanel
            pTos uiBackPage
            pTos uiBackFocus
            pTos presentation
            pToa dialogue
            send 14
            not
            bnt L_8d8d
            ldi 0
            ret
            L_8d8d: ldi 4
            aTop uiPanel
            lap 1
            aTop uiDocument
            ldi 0
            aTop uiPage
            pushi 464
            push0
            pToa dialogue
            send 4
            aTop uiPageCount
            ldi 0
            aTop uiFocus
            ldi 0
            aTop uiReveal
            ldi 1
            aTop dirty
            ldi 1
            ret
        )
    )

    ; Delivered offset0x8db9; 126 original instructions
    (method (dialoguePresented &tmp t0 t1)
(if p08 (p08 h8ReaderPresented:))

(if (and p08 (p08 h8ActionBarrier:) (not (p08 h8VR: 7 0))) (return 0))

(if p07 (p07 h7Presented: uiDocument uiPage (dialogue sdGeneration?)))

(if p06 (p06 h6Presented: uiDocument uiPage (dialogue sdGeneration?)))

(if p05 (p05 hPresented: uiDocument uiPage (dialogue sdGeneration?)))

        (if (and p04 (self scenePageIdentity:) (>= uiDocument 385) (<= uiDocument 420)
            (== uiPanel 4) (not opening) (not paused) (not menuOpen)
            (not uiFailure) (not bridgeFailure) (not (dialogue sdFailure?))
            (== (dialogue sdPaintGeneration?) (dialogue sdGeneration?)))
            (p04 qPresented: self (- uiDocument 384) uiPage)
            (if (p04 qFailure?) (= p04HostError (p04 qFailure?)) (= uiFailure 10)))
        (asm
            pushi 666
            push0
            self 4
            not
            bnt L_8dd3
            pToa p03
            bnt L_8dd0
            pushi 510
            push0
            pToa p03
            send 4
            L_8dd0: ldi 0
            ret
            L_8dd3: pToa p03
            bnt L_8e5a
            pTos uiDocument
            ldi 343
            ge?
            bnt L_8e5a
            pTos uiDocument
            ldi 384
            le?
            bnt L_8e5a
            pTos uiPanel
            ldi 4
            eq?
            bnt L_8e5a
            pToa opening
            not
            bnt L_8e5a
            pToa paused
            not
            bnt L_8e5a
            pToa menuOpen
            not
            bnt L_8e5a
            pToa uiFailure
            not
            bnt L_8e5a
            pToa bridgeFailure
            not
            bnt L_8e5a
            pushi 470
            push0
            pToa dialogue
            send 4
            not
            bnt L_8e5a
            pushi 482
            push0
            pToa dialogue
            send 4
            push
            pushi 473
            push0
            pToa dialogue
            send 4
            eq?
            bnt L_8e5a
            pushi 537
            pushi 3
            pushSelf
            pTos uiDocument
            ldi 342
            sub
            push
            pTos uiPage
            pToa p03
            send 10
            pushi 521
            push0
            pToa p03
            send 4
            bnt L_8e5a
            pushi 521
            push0
            pToa p03
            send 4
            aTop p03HostError
            ldi 10
            aTop uiFailure
            L_8e5a: pushi 473
            push0
            pToa dialogue
            send 4
            sat 0
            pushi 480
            push0
            pToa dialogue
            send 4
            sat 1
            pushi 486
            pushi 3
            lst 0
            lst 1
            pushi 388
            push0
            pToa presentation
            send 4
            push
            pToa dialogue
            send 10
            bnt L_8eb0
            pushi 404
            push1
            pushi 493
            push0
            pToa dialogue
            send 4
            push
            self 6
            bnt L_8ea8
            pushi 492
            pushi 3
            pTos presentation
            lst 0
            lst 1
            pToa dialogue
            send 10
            jmp L_8eb0
            L_8ea8: pushi 494
            push0
            pToa dialogue
            send 4
            L_8eb0: ret
        )
    )

    ; Delivered offset0x8eb1; 81 original instructions
    (method (dialogueCanSpeak who &tmp h11VoiceResult)
(if (!= self (ScriptID 0 0)) (return 0))
(= h11VoiceResult ((ScriptID 996 0) h14Voice: who))
(if (!= h11VoiceResult -2) (return h11VoiceResult))
(= h11VoiceResult ((ScriptID 995 0) h13Voice: who))
(if (!= h11VoiceResult -2) (return h11VoiceResult))
(= h11VoiceResult ((ScriptID 994 0) h12VoiceAdmission: who))
(if (!= h11VoiceResult -2) (return h11VoiceResult))

(if (!= self (ScriptID 0 0)) (return 0))
(= h11VoiceResult ((ScriptID 993 0) h11VoiceAdmission: who))
(if (!= h11VoiceResult -2) (return h11VoiceResult))

(if (and p08 (>= (p08 h8V: 1 0) 5) (or (== uiDocument 1013) (== uiDocument 1017))) (return 0))

(if (and p08 (> (p08 h8V: 1 0) 0) (< (p08 h8V: 1 0) 5)) (return (p08 h8VR: 6 who)))

(if (and p08 (p08 h8RouteBusy:)) (return 0)) (if (and p08 (p08 h8RouteCanSpeak: who)) (return 1)) (if (and (== who 3) p06 (!= location (p06 h6FrankieRoom?))) (return 0))

        (if (and (== who 8) (== location 3) (not onApron)) (return 1))
        ; Explicit current-art coverage. Extend only when a visible mouth route is proved.
        (if (or opening (!= motionPhase 0)) (return 0))
(if (and p05 p02PlanAgreed (== who 2)) (return (if (and (not onApron) (== location (p05 hBunnyRoom?))) 1 else 0)))
(if (and p05 p02PlanAgreed (== who 5)) (return (if (and (not onApron) (== location (p05 hMiloRoom?))) 1 else 0)))
        (if (and p06 (== who 6)) (return (p06 h6CanSpeak:)))
(if (== who 1) (return 1))
        (if onApron (return 0))
        (if (and (== who 7) (== location 6) houseEntered) (return 1))
        (if (and (== location 1) houseEntered (or (== who 2) (== who 3))) (return 1))
        (if (and (== location 0) (== who 2) (not houseEntered)) (return 1))
        (if (and houseEntered
            (or (and (== location 5) (== who 5)) (and (== location 6) (== who 4)))) (return 1))
        (return 0))

    ; Delivered offset0x8f3e; 52 original instructions
    (method (neighborPerson who)
(if (and p08 (== who 4) (!= location (p08 h8ActorRoom: 4))) (return 0))

 (return ((ScriptID 991 0) neighborPerson: self who)))

    ; Delivered offset0x8fa3; 14 original instructions
    (method (campaignHeld obj &tmp h10Answer)
(if ((ScriptID 996 0) h14Owns: obj) (return ((ScriptID 996 0) h14Held: obj)))

(if ((ScriptID 995 0) h13Owns: obj) (return ((ScriptID 995 0) h13Held: obj)))

(if ((ScriptID 994 0) h12SuccessorHas: obj) (return 0))

(if ((ScriptID 994 0) h12Reserved: obj) (return 0))

(if ((ScriptID 993 0) h11OwnerHas: obj) (return ((ScriptID 993 0) h11OwnerQ: 1 obj)))

(= h10Answer ((ScriptID 992 0) h10Q: 1 obj)) (if (!= h10Answer -2) (return h10Answer))
(if (== obj 399) (return (if p09 (p09 h9CardHeld: obj) else 0)))
(if (and (>= obj 395) (<= obj 399)) (return 0))

(if (and p08 (p08 h8HandlesCloth: obj)) (return (p08 h8ClothHeld: obj)))

(if (and p07 (>= obj 86) (<= obj 94)) (return 0))

(if (and p06 (>= obj 73) (<= obj 85)) (return (p06 h6Held: obj)))

        (if p04 (return (p04 qHeld: self obj)))
    (if p03 (return (p03 bHeld: self obj)))
    (return (self p02Held: obj)))

    ; Delivered offset0x8fbc; 25 original instructions
    (method (campaignReachable obj &tmp h10Answer)
(if ((ScriptID 996 0) h14Owns: obj) (return ((ScriptID 996 0) h14Reachable: obj)))

(if (and (== obj 410) ((ScriptID 995 0) h13Active:)) (return ((ScriptID 995 0) h13Reachable: obj)))

(if ((ScriptID 995 0) h13Owns: obj) (return ((ScriptID 995 0) h13Reachable: obj)))

(if ((ScriptID 994 0) h12SuccessorHas: obj) (return (and (not onApron) (== location ((ScriptID 994 0) h12SuccessorRoom: obj)))))

(if (or (== obj 419) (== obj 420) (and (== obj 410) ((ScriptID 994 0) h12Active:))) (return ((ScriptID 994 0) h12Reachable: obj)))

(if (and (>= obj 415) (<= obj 418)) (return (and ((ScriptID 993 0) h11Active:) ((ScriptID 993 0) h11OwnerReady:) (== location 3) (not onApron))))

(if ((ScriptID 993 0) h11OwnerHas: obj) (return ((ScriptID 993 0) h11OwnerQ: 3 obj)))

(= h10Answer ((ScriptID 992 0) h10Q: 3 obj)) (if (!= h10Answer -2) (return h10Answer))
(if (and (>= obj 395) (<= obj 399))
 (return (and p09 (p09 h9Active:) (not onApron) (if (== obj 399) (p09 h9CardHeld: 399) else (== location 6)))))

(if (and p08 (p08 h8LayoutTarget: obj)) (return 1))

(if (and p07 (>= obj 86) (<= obj 94)) (return (p07 h7Reachable: obj)))

(if (and p06 (>= obj 73) (<= obj 85)) (return (p06 h6Reachable: obj)))

    (if (== obj -103) (return (and (== location 2) (not onApron))))
    (if p04 (return (p04 qReachable: self obj)))
    (if p03 (return (p03 bReachable: self obj)))
    (return (self p02Reachable: obj)))

    ; Delivered offset0x8fe7; 15 original instructions
    (method (p03HostExternalHeld obj)
        (if (self p04Reserved: obj) (return 0))
    ; The current production snapshot has no newspaper pickup or P04 reservation.
    ; Extend this one external-ownership hook when those owners are integrated.
    (if (and (>= obj 1) (<= obj 32)) (return (self p02Held: obj)))
    (return 0))

    ; Delivered offset0x9001; 13 original instructions
    (method (p03HostReservation obj)
    (if (and (>= obj 0) (<= obj 32)) (return [p02Reserved obj]))
    (return -1))

    ; Delivered offset0x9018; 23 original instructions
    (method (p03HostUIItem index obj)
    (if (or (< index 0) (>= index 64) (< obj 0) (> obj 50)) (return 0))
    (= [uiItems index] obj)
    (if (and p04 (p04 qEnabled?) (== index 63))
        (if (not (p04 qInventory: self))
            (= p04HostError (p04 qFailure?)) (= uiFailure 10) (= dirty 1) (return 0)))
    (if (and p06 (== index 63)) (p06 h6Inventory:)) (return 1))

    ; Delivered offset0x9040; 35 original instructions
    (method (p03HostLinePages line &tmp pages)
    (if (or (not dialogue) (< line 1) (> line 42)) (return 0))
    (= pages (dialogue sdPageCount: (+ 342 line)))
    (return (if (and (> pages 0) (<= pages 64)) pages else 0)))

    ; Delivered offset0x907e; 46 original instructions
    (method (p03HostQueue line &tmp before)
    ; Scene-only documents must never enter the legacy text200 reader.
    (if (or bridgeSilent (not (self p03HostLinePages: line))
        (< bridgeQueueCount 0) (>= bridgeQueueCount 32)) (return 0))
    (= before bridgeQueueCount)
    (if (not (dialogue sdQueueSet: before 1)) (return 0))
    (= [bridgeQueue before] (+ 342 line)) (++ bridgeQueueCount)
    (return (if (> bridgeQueueCount before) 1 else 0)))

    ; Delivered offset0x90d7; 33 original instructions
    (method (p03HostEvent event arg hi lo)
    ; Do not project/query context here: bPublish still owns the result buffer.
    (switch event
        (5 (= p03WantCredit 1))
        (6 (= p03WantCredit 1))
        (7 (= p03WantCredit 0))
        (10 (= p03WantCredit 0)))
    (= dirty 1) (return 1))

    ; Delivered offset0x9110; 144 original instructions
    (method (p03HostStatus code obj)
    ; No fabricated status dialogue. Existing generic failures or the current
    ; object/choice view are truthful when the accepted action has no record.
    (= p03LastStatus code)
    (if (and (p03 p03Open?) (or (== code 18) (== code 20) (== code 21)))
        (= p03WantCredit 1) (return 1))
    (if (and (== obj 30) (or (== code 5) (== code 6)))
        (= p03WantTopics 30) (return 1))
    (if (== code 1) (self p02HostText: 108 0) (return 1))
    (if (== code 2)
        (return (self uiOpenInline: "EDIT HOUSEHOLD PLAN" "COMPLETE MASTER INVITATION\nCOMPARISON BOARD")))
    (if (or (== code 10) (== code 29)) (self p02HostText: 146 0) (return 1))
    (if (or (== obj 40) (== code 25) (== code 27))
        (return (self uiOpenInline: (self p03Label: 40) (self p03SlateText:))))
    (if (or (== code 5) (== code 26))
        (return (self uiOpenInline: (self p03Label: 34) (self p03Label: 34))))
    (if (== obj 44) (return (self p03DrawerView:)))
    (return (self uiOpenInline: (self uiHostItemLabel: obj) (self uiHostItemLabel: obj))))

    ; Delivered offset0x9212; 65 original instructions
    (method (p03DrawerView &tmp [contents 120])
    (StrCpy @contents (self p03Label: 44))
    (if (== (p03 p03Towel?) 0) (StrCat @contents "\n") (StrCat @contents (self p03Label: 39)))
    (if (== (p03 p03Napkin?) 0) (StrCat @contents "\n") (StrCat @contents (self p03Label: 38)))
    (return (self uiOpenInline: (self p03Label: 44) @contents)))

    ; Delivered offset0x928d; 70 original instructions
    (method (p03BuildCredit &tmp choices)
    (= p03WantCredit 0) (= choices (p03 bChoices: self))
    (if (not choices) (return 0))
    (= bridgeReaderActive 0) (self uiClearChoices: (self p03Label: 40) 204 0)
    (self uiAddChoice: 1 (self p03ChoiceLabel: 1) (== (p03 p03Slate?) 1) (& choices 1))
    (self uiAddChoice: 2 (self p03ChoiceLabel: 2) (== (p03 p03Slate?) 2) (& choices 2)) (return 1))

    ; Delivered offset0x9308; 76 original instructions
    (method (p03BuildTopics actor &tmp topics)
    (= p03WantTopics 0) (= topics (p03 bTopics: self actor))
    (if (not topics) (return 0))
    (= p03TopicActor actor) (= bridgeReaderActive 0)
    (self uiClearChoices: (self uiHostItemLabel: actor) 205 0)
    (if (& topics 1) (self uiAddChoice: 1 (self p03Label: 36) 0 1))
    (if (& topics 2) (self uiAddChoice: 2 (self p03Label: 40) 0 1))
    (if (& topics 4) (self uiAddChoice: 3 (self p03Label: 42) 0 1)) (if (and (== actor 30) ((ScriptID 992 0) h10Active:)) (self uiAddChoice: 120 "Discuss the ceramic cues" 0 1)) (return 1))

    ; Delivered offset0x9392; 49 original instructions
    (method (p03BuildJournal &tmp i line)
    (p03 bCancelPending:) (= bridgeReaderActive 0)
    (self uiClearChoices: "EVIDENCE JOURNAL" 206 0)
    (for ((= i 0)) (< i 6) ((++ i))
        (= line (p03 bJournalLine: i))
        (if line (self uiAddChoice: line (self p03JournalLabel: line) 0 1)))
    (self uiAddChoice: 100 "RECORDED INVITATION EVIDENCE" 0 1) (return 1))

    ; Delivered offset0x93f3; 52 original instructions
    (method (p03HostFinish)
        (asm
            pushi 521
            push0
            pToa p03
            send 4
            bnt L_9414
            pushi 521
            push0
            pToa p03
            send 4
            aTop p03HostError
            ldi 10
            aTop uiFailure
            ldi 1
            aTop dirty
            ldi 0
            ret
            L_9414: ldi 0
            aTop p03HostError
            pTos uiPanel
            ldi 2
            eq?
            bnt L_943e
            pTos uiChoiceContext
            ldi 204
            eq?
            bnt L_943e
            pushi 636
            push0
            pToa p03
            send 4
            not
            bnt L_943e
            ldi 0
            aTop uiPanel
            ldi 0
            aTop uiBackPanel
            L_943e: pToa p03WantCredit
            bnt L_9448
            pushi 580
            push0
            self 4
            L_9448: pToa p03WantTopics
            bnt L_9454
            pushi 582
            push1
            pTos p03WantTopics
            self 6
            L_9454: pushi 66
            push0
            self 4
            ldi 1
            ret
        )
    )

    ; Delivered offset0x945c; 99 original instructions
    (method (p03Restore)
        (asm
            pushi 533
            push0
            pToa p03
            send 4
            bnt L_9477
            pushi 666
            push0
            self 4
            not
            bnt L_9477
            pushi 510
            push0
            pToa p03
            send 4
            L_9477: ldi 0
            aTop p03WantCredit
            ldi 0
            aTop p03WantTopics
            pushi 543
            push1
            pushSelf
            pToa p03
            send 6
            not
            bnt L_94a9
            ldi 1
            aTop p03Invalid
            pushi 521
            push0
            pToa p03
            send 4
            aTop p03HostError
            ldi 10
            aTop uiFailure
            ldi 1
            aTop paused
            ldi 1
            aTop menuOpen
            ldi 0
            ret
            L_94a9: ldi 0
            aTop p03Invalid
            ldi 0
            aTop p03HostError
            pushi 636
            push0
            pToa p03
            send 4
            bnt L_9504
            pTos uiPanel
            ldi 4
            eq?
            bnt L_94fe
            pTos uiBackPanel
            ldi 2
            eq?
            bnt L_94fe
            pTos uiChoiceContext
            ldi 204
            eq?
            bnt L_94fe
            pushi 334
            push2
            push1
            pushi 654
            push0
            pToa p03
            send 4
            push
            ldi 1
            eq?
            push
            self 8
            pushi 334
            push2
            push2
            pushi 654
            push0
            pToa p03
            send 4
            push
            ldi 2
            eq?
            push
            self 8
            jmp L_9504
            L_94fe: pushi 580
            push0
            self 4
            L_9504: pushi 525
            push1
            pushSelf
            pToa p03
            send 6
            pushi 270
            push0
            self 4
            ldi 1
            ret
        )
    )

    ; Delivered offset0x9516; 10 original instructions
    (method (p03Checkpoint)
    (return (if p03 (p03 bCheckpoint: self) else p02PlanAgreed)))

    ; Delivered offset0x9529; 28 original instructions
    (method (p03PreparationHint)
(if (and p09 (p09 h9Hint:)) (return 0))
 (if (and p07 p02PlanAgreed (== location 2) (not onApron)) (p07 h7HintMenu:) (return 0)) (return (self h7BasePreparationHint:)))

    ; Delivered offset0x955c; 177 original instructions
    (method (p03KitchenControls)
    (self uiAddControl: 1 18 44 19 110 44 "LIVING ROOM")
    (self uiAddControl: 1 -103 46 190 76 273 (self p03Label: -103))
    (self uiAddControl: 1 43 78 183 86 289 (self p03Label: 43))
    (self uiAddControl: 1 44 84 142 97 169 (self p03Label: 44))
    (if (and (self p02Reachable: 5) (!= tray 0)) (self uiAddControl: 1 5 84 183 104 213 "BREAD TRAY"))
    (if (p03 p03Ready?)
        (if (or (not p08) (not (p08 h8Owns: 1))) (self uiAddControl: 1 34 54 214 81 256 (self p03Label: 34)))
        (if (or (not p08) (not (p08 h8Owns: 1))) (self uiAddControl: 1 36 54 216 64 252 (self p03Label: 36)))
        (self uiAddControl: 1 33 73 216 80 233 (self p03Label: 33))
        (if (or (not p08) (not (p08 h8Owns: 5))) (self uiAddControl: 1 40 63 260 83 282 (self p03Label: 40))))
    (if (== (p03 p03Towel?) 0) (self uiAddControl: 1 39 84 143 92 157 (self p03Label: 39)))
    (if (== (p03 p03Napkin?) 0) (self uiAddControl: 1 38 85 157 92 169 (self p03Label: 38))))

    ; Delivered offset0x96c5; 129 original instructions
    (method (p03ConservatoryControls)
    (if (== ((ScriptID 993 0) h11OwnerLocation: 30) 6) (self uiAddControl: 1 30 64 239 132 268 "RITA"))
    (if (== ((ScriptID 993 0) h11OwnerLocation: 42) 6) (self uiAddControl: 1 42 57 281 108 315 (self p03Label: 42)))
    (if (== ((ScriptID 993 0) h11OwnerLocation: 41) 6) (self uiAddControl: 1 41 74 289 88 308 (self p03Label: 41)))
    (self uiAddControl: 1 37 45 62 59 80 (self p03Label: 37))
    (if (not (p03 p03Ready?))
        (self uiAddControl: 1 36 60 64 80 83 (self p03Label: 36))
        (self uiAddControl: 1 47 64 67 78 81 (self p03Label: 47))
        (self uiAddControl: 1 34 54 86 81 128 (self p03Label: 34))
        (self uiAddControl: 1 33 72 102 80 111 (self p03Label: 33))
        (self uiAddControl: 1 40 62 128 82 151 (self p03Label: 40))))

    ; Delivered offset0x97c9; 93 original instructions
    (method (drawKitchen)
 (return ((ScriptID 991 0) drawKitchen: self)))

    ; Delivered offset0x987d; 155 original instructions
    (method (drawP03Conservatory)
 (return ((ScriptID 991 0) drawP03Conservatory: self)))

    ; Delivered offset0x99a3; 70 original instructions
    (method (p03Rita)
(if (and p08 (!= location (p08 h8ActorRoom: 7))) (return 0))

 (return ((ScriptID 991 0) p03Rita: self)))

    ; Delivered offset0x9a1f; 136 original instructions
    (method (p03Label obj)
    (switch obj
        (34 (return "Ceramic carrier"))
        (36 (return "Rita's ceramic service"))
        (37 (return "Ceramics-class card"))
        (40 (return "Credit slate"))
        (39 (return "Clean tea towel"))
        (38 (return "Clean spare napkin"))
        (44 (return "Linen drawer"))
        (35 (return "Ceramic sample tiles"))
        (42 (return "Folded display"))
        (-103 (return "Kitchen hatch"))
        (33 (return "Drawing"))
        (41 (return "Wing release"))
        (43 (return "KITCHEN PASS"))
        (45 (return "Linen hook"))
        (46 (return "Newspaper"))
        (47 (return "Signature"))
        (48 (return "Ceramic sample tiles"))
        (49 (return "Ceramic sample tiles"))
        (50 (return "Ceramic sample tiles"))
    ) (return "ITEM"))

    ; Delivered offset0x9b10; 8 original instructions
    (method (p03ChoiceLabel choice) (return (if (== choice 1) "Ceramic service by Rita Stringer." else "Ceramic service by Mrs. Stringer.")))

    ; Delivered offset0x9b20; 19 original instructions
    (method (p03SlateText) (return (if (== (p03 p03Slate?) 0) "Mr. Stringer's collection" else (self p03ChoiceLabel: (p03 p03Slate?)))))

    ; Delivered offset0x9b43; 2 original instructions
    (method (p03KitchenDescription) (return "My kitchen. Everybody agrees, especially when something needs wiping. Door to the living room; serving hatch to the courtyard. Food fits through the hatch. People don't."))

    ; Delivered offset0x9b47; 60 original instructions
    (method (p03JournalLabel line)
    (switch line
        (6 (return (self p03Label: 47))) (9 (return (self p03Label: 37)))
        (1 (return "RITA")) (30 (return (self p03Label: 40)))
        (4 (return (self p03Label: 33))) (38 (return (self p03Label: 41))))
    (return "EVIDENCE JOURNAL"))

    ; Delivered offset0x9bad; 9 original instructions
    (method (foleyNextSerial)
        ; No async callbacks retain this serial. Adjacent occurrences differ at wrap.
        (= foleySerial (mod (+ foleySerial 1) 30000)) (return foleySerial))

    ; Delivered offset0x9bbc; 9 original instructions
    (method (foleyInvalidate)
        (= foleyWalkToken -1)
        (if presentation (presentation cancelFoley:)))

    ; Delivered offset0x9bcd; 23 original instructions
    (method (foleyBeginWalk)
        (self foleyInvalidate:)
        (= foleyWalkSerial (self foleyNextSerial:)) (= foleyOrdinal 0)
        (= motionFrame 0) (= motionTicks 0) (= motionPose 0)
        (if presentation (= foleyWalkToken (presentation token?))))

    ; Delivered offset0x9bfd; 11 original instructions
    (method (foleySurface)
        ; Only the reviewed wood floors. Aprons and unfinished sets have no mapping.
        (return (and (not onApron) (or (== location 0) (== location 1)))))

    ; Delivered offset0x9c0f; 62 original instructions
    (method (foleyWalkContact age &tmp noun)
        ; Called synchronously only for a newly crossed, visibly moved contact.
        ; Consume each crossing even if its age or lane owner makes it inaudible.
        (= foleyOrdinal (mod (+ foleyOrdinal 1) 30000))
        (if (or (not presentation) (not (self foleySurface:))
                (!= location motionRoom) (!= onApron motionApron)
                (!= foleyWalkToken (presentation token?))) (return 0))
        (= noun (if (== foleyLastStep 1) 2 else 1))
        (if (presentation requestFoley: foleyWalkSerial foleyOrdinal 930 noun 1 0 1 0 age foleyWalkToken)
            (= foleyLastStep noun) (return 1)) (return 0))

    ; Delivered offset0x9c80; 118 original instructions
    (method (foleyCommitted eventId revision room apron requested expected &tmp noun age occurrence)
        (if (not (or (== eventId 11) (== eventId 12) (== eventId 13) (== eventId 14))) (return 0))
        (if (or (not presentation) (!= room location) (!= apron onApron)
                (!= expected (presentation token?))
                (and (== revision foleyLastRevision) (== eventId foleyLastDomainEvent))) (return 0))
        (= foleyLastRevision revision) (= foleyLastDomainEvent eventId)
        (= occurrence (self foleyNextSerial:))
        (if (not (self foleySurface:)) (return 0))
        (= age (- (GetTime) requested))
        (= noun (if (== eventId 13) 3 else (if (== eventId 14) 4
            else (if (== foleyLastWood 5) 6 else 5))))
        (if (presentation requestFoley: occurrence 0 930 noun 1 0 1 1 age expected)
            (if (or (== noun 5) (== noun 6)) (= foleyLastWood noun))
            (return 1)) (return 0))

    ; Delivered offset0x9d51; 19 original instructions
    (method (effectsOff)
        (if (not presentation) (return 0))
        (presentation setOff: 3 (not (presentation effectsMuted?)))
        ; Never replay a discarded contact on raise. New crossings remain eligible.
        (= dirty 1))

    ; Delivered offset0x9d73; 38 original instructions
    (method (effectsAdjust amount &tmp level)
        (if (not presentation) (return 0))
        (= level (+ (presentation effectsVolume?) amount))
        (if (< level 0) (= level 0)) (if (> level 100) (= level 100))
        (presentation effectsVolume: level) (presentation refreshGain:)
        (= dirty 1))

    ; Delivered offset0x9db9; 55 original instructions
    (method (scenePageIdentity)
    (if (or (not dialogue) (!= uiPanel 4) (not (dialogue sdActive?))
        (dialogue sdFailure?) (!= uiDocument (dialogue sdDocument?))
        (!= uiPage (dialogue sdPage?)) (!= uiPageCount (dialogue sdCount?))
        (!= (dialogue sdCount?) (dialogue sdPageCount: uiDocument))) (return 0))
    (return 1))

    ; Delivered offset0x9e22; 61 original instructions
    (method (musicRequests)
        (asm
            pToa musicOwner
            not
            bt L_9e2e
            pTos musicOwnerKind
            ldi 2
            ne?
            bnt L_9e31
            L_9e2e: ldi 0
            ret
            L_9e31: pTos masterVolume
            pToa audioDuckTicks
            bnt L_9e3d
            ldi 60
            jmp L_9e3f
            L_9e3d: ldi 100
            L_9e3f: mul
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
            bnt L_9e5e
            ldi 1
            jmp L_9e60
            L_9e5e: ldi 0
            L_9e60: push
            pToa musicOwner
            send 6
            pushi 734
            push1
            pToa paused
            bt L_9e71
            pToa menuOpen
            bnt L_9e75
            L_9e71: ldi 1
            jmp L_9e77
            L_9e75: ldi 0
            L_9e77: push
            pToa musicOwner
            send 6
            pTos audioDesired
            pushi 423
            push0
            pToa musicOwner
            send 4
            ne?
            bnt L_9e95
            pushi 439
            push1
            pTos audioDesired
            pToa musicOwner
            send 6
            L_9e95: ldi 1
            ret
        )
    )

    ; Delivered offset0x9e98; 33 original instructions
    (method (musicStopOwner)
        (asm
            pTos musicOwnerKind
            ldi 2
            eq?
            bnt L_9ea7
            pushi 502
            push0
            pToa musicOwner
            send 4
            L_9ea7: pTos musicOwnerKind
            ldi 1
            eq?
            bnt L_9ecb
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
            L_9ecb: ldi 0
            aTop musicOwnerKind
            ldi 0
            aTop audioCreditsHeld
            ldi 0
            aTop musicChooserKind
            ldi 1
            ret
        )
    )

    ; Delivered offset0x9edb; 103 original instructions
    (method (musicSelectOwner)
        (asm
            pToa audioReady
            not
            bnt L_9ee4
            ldi 0
            ret
            L_9ee4: pToa opening
            bnt L_9eef
            pTos musicOwnerKind
            ldi 1
            eq?
            bt L_9efb
            L_9eef: pToa opening
            not
            bnt L_9efe
            pTos musicOwnerKind
            ldi 2
            eq?
            bnt L_9efe
            L_9efb: ldi 1
            ret
            L_9efe: pushi 701
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
            bnt L_9f5f
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
            bnt L_9f56
            ldi 0
            jmp L_9f59
            L_9f56: pToa masterVolume
            L_9f59: push
            callk DoSound, 6
            jmp L_9f8a
            L_9f5f: pToa musicOwner
            not
            bnt L_9f6b
            ldi 1
            aTop musicUnavailable
            ldi 0
            ret
            L_9f6b: ldi 2
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
            bnt L_9f8a
            ldi 1
            aTop musicUnavailable
            L_9f8a: pushi 52
            push1
            pToa opening
            bnt L_9f96
            lofsa "credits owner"
            jmp L_9f99
            L_9f96: lofsa "world owner"
            L_9f99: push
            self 6
            pToa musicUnavailable
            bnt L_9fa4
            ldi 0
            jmp L_9fa6
            L_9fa4: ldi 1
            L_9fa6: ret
        )
    )

    ; Delivered offset0x9fa7; 67 original instructions
    (method (musicBeforeChooser)
        (asm
            pToa audioReady
            not
            bt L_9fb1
            pToa musicChooserKind
            bnt L_9fb4
            L_9fb1: ldi 0
            ret
            L_9fb4: pushi 259
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
            bnt L_9ff0
            pushi 698
            push0
            self 4
            pushi 674
            push0
            pToa musicOwner
            send 4
            not
            bnt L_9fe9
            ldi 1
            aTop musicUnavailable
            ldi 1
            aTop dirty
            ldi 0
            ret
            L_9fe9: ldi 2
            aTop musicChooserKind
            ldi 1
            ret
            L_9ff0: pTos musicOwnerKind
            ldi 1
            eq?
            bnt L_a01e
            pushi 3
            pushi 14
            lofss credits
            push0
            callk DoSound, 6
            pToa audioCreditsHeld
            bnt L_a017
            pushi 3
            pushi 10
            lofss credits
            push0
            callk DoSound, 6
            ldi 0
            aTop audioCreditsHeld
            L_a017: ldi 1
            aTop musicChooserKind
            ldi 1
            ret
            L_a01e: ldi 1
            aTop musicUnavailable
            ldi 1
            aTop dirty
            ldi 0
            ret
        )
    )

    ; Delivered offset0xa02a; 43 original instructions
    (method (musicAfterChooser &tmp t0)
        (asm
            pToa musicChooserKind
            sat 0
            ldi 0
            aTop musicChooserKind
            lst 0
            ldi 2
            eq?
            bnt L_a053
            pushi 671
            push0
            pToa musicOwner
            send 4
            not
            bnt L_a04a
            ldi 1
            aTop musicUnavailable
            L_a04a: pushi 698
            push0
            self 4
            ldi 1
            ret
            L_a053: lst 0
            ldi 1
            eq?
            bnt L_a078
            pushi 28
            push0
            self 4
            pushi 3
            pushi 14
            lofss credits
            pToa musicMuted
            bnt L_a06e
            ldi 0
            jmp L_a071
            L_a06e: pToa masterVolume
            L_a071: push
            callk DoSound, 6
            ldi 1
            ret
            L_a078: ldi 0
            ret
        )
    )

    ; Delivered offset0xa07b; 15 original instructions
    (method (musicRetry)
        (asm
            pTos musicOwnerKind
            ldi 2
            eq?
            bnt L_a097
            pToa musicUnavailable
            bnt L_a097
            pushi 442
            push0
            pToa musicOwner
            send 4
            ldi 0
            aTop musicUnavailable
            ldi 1
            aTop dirty
            L_a097: ret
        )
    )

    ; Delivered offset0xa098; 61 original instructions
    (method (navNoticeSet arg1 arg2)
        (asm
            pToa bridgeSilent
            bnt L_a0a0
            ldi 0
            ret
            L_a0a0: lsp 1
            dup
            ldi 129
            eq?
            bnt L_a0b9
            lsp 2
            ldi 0
            ne?
            bnt L_a0b3
            ldi 0
            ret
            L_a0b3: ldi 1
            aTop navNotice
            jmp L_a0f4
            L_a0b9: dup
            ldi 130
            eq?
            bnt L_a0d0
            lsp 2
            ldi 0
            ne?
            bnt L_a0ca
            ldi 0
            ret
            L_a0ca: ldi 2
            aTop navNotice
            jmp L_a0f4
            L_a0d0: dup
            ldi 134
            eq?
            bnt L_a0f1
            lsp 2
            ldi 0
            lt?
            bt L_a0e5
            lsp 2
            ldi 6
            gt?
            bnt L_a0e8
            L_a0e5: ldi 0
            ret
            L_a0e8: pushi 3
            lap 2
            add
            aTop navNotice
            jmp L_a0f4
            L_a0f1: ldi 0
            ret
            L_a0f4: toss
            ldi 0
            aTop currentCaption
            ldi 180
            aTop navNoticeTicks
            ldi 1
            aTop dirty
            ldi 1
            ret
        )
    )

    ; Delivered offset0xa106; 41 original instructions
    (method (navNoticeAdvance arg1)
        (asm
            pTos navNoticeTicks
            ldi 0
            le?
            bt L_a11e
            pToa opening
            bt L_a11e
            pToa paused
            bt L_a11e
            pToa menuOpen
            bt L_a11e
            pToa uiPanel
            bnt L_a121
            L_a11e: ldi 0
            ret
            L_a121: lsp 1
            ldi 0
            lt?
            bnt L_a12c
            ldi 0
            sap 1
            L_a12c: lsp 1
            ldi 12
            gt?
            bnt L_a137
            ldi 12
            sap 1
            L_a137: pTos navNoticeTicks
            lap 1
            sub
            aTop navNoticeTicks
            pTos navNoticeTicks
            ldi 0
            le?
            bnt L_a152
            ldi 0
            aTop navNoticeTicks
            ldi 0
            aTop navNotice
            ldi 1
            aTop dirty
            L_a152: ret
        )
    )

    ; Delivered offset0xa153; 147 original instructions
    (method (navNoticeRender)
 (return ((ScriptID 991 0) navNoticeRender: self)))

(method (p04Reserved obj)
    (return (if (and p04 (== obj 4)) (p04 p04Wedge?) else 0)))
(method (p04ExternalHeld obj)
    (if (self p04Reserved: obj) (return 0))
    (if p03 (return (p03 bHeld: self obj)))
    (return (self p02Held: obj)))
(method (p04BaseReachable obj)
    (if p03 (return (p03 bReachable: self obj)))
    (return (self p02Reachable: obj)))
(method (p04UIItem index)
    (if (or (< index 0) (>= index 64)) (return 0)) (return [uiItems index]))
(method (p04SetUIItem index obj)
    (if (or (< index 0) (>= index 64) (< obj 0) (> obj 62)) (return 0))
    (= [uiItems index] obj) (return 1))
(method (p04QueueItem index)
    (if (or (< index 0) (>= index bridgeQueueCount) (>= index 32)) (return 0))
    (return [bridgeQueue index]))
(method (p04RollbackQueue count &tmp i)
    (if (or (< count 0) (> count bridgeQueueCount)) (return 0))
    (for ((= i count)) (< i bridgeQueueCount) ((++ i))
        (= [bridgeQueue i] 0) (dialogue sdQueueSet: i 0))
    (= bridgeQueueCount count) (return 1))
(method (p04HostLinePages line &tmp pages)
    (if (or (not dialogue) (< line 1) (> line 36)) (return 0))
    (= pages (dialogue sdPageCount: (+ 384 line)))
    (return (if (and (> pages 0) (<= pages 64)) pages else 0)))
(method (p04HostQueue line &tmp before)
    (if (or bridgeSilent (not (self p04HostLinePages: line))
        (< bridgeQueueCount 0) (>= bridgeQueueCount 32)) (return 0))
    (= before bridgeQueueCount)
    (if (not (dialogue sdQueueSet: before 1)) (return 0))
    (= [bridgeQueue before] (+ 384 line)) (++ bridgeQueueCount)
    (return (if (> bridgeQueueCount before) 1 else 0)))
(method (p04HostEvent event arg arg2 hi lo)
    ; Read-only notification. No item return, completion grant or audio factory.
    (= dirty 1) (return 1))
(method (p04HostStatus code obj)
    (= p04LastStatus code)
    (if (== code 27) (self p02HostText: 108 0) (return 1))
    (if (== code 33)
        (return (self uiOpenInline: "EDIT HOUSEHOLD PLAN" "COMPLETE MASTER INVITATION\nCOMPARISON BOARD")))
    (if (or (== code 22) (== code 37)) (self p02HostText: 146 0) (return 1))
    ; Empty authored bindings are current object labels, never invented prose
    ; or stale original-state dialogue. Machine status stays diagnostic only.
    (return (self uiOpenInline: (self uiHostItemLabel: obj) (self uiHostItemLabel: obj))))
(method (p04HostFinish)
    (if (p04 qFailure?)
        (= p04HostError (p04 qFailure?)) (= uiFailure 10) (= dirty 1) (return 0))
    (= p04HostError 0) (self bridgeFlush:) (return 1))
(method (p04Restore)
    (if (not (p04 qAfterRestore: self))
        (= p04Invalid 1) (= p04HostError (p04 qFailure?))
        (= uiFailure 10) (= paused 1) (= menuOpen 1) (return 0))
    (= p04Invalid 0) (= p04HostError 0)
    (self p02HostInventory:) (self uiAfterRestore:) (return 1))
(method (p04BuildTopics)
    (= bridgeReaderActive 0)
    (self uiClearChoices: (self p04Label: 54) 207 0)
    (self uiAddChoice: 1 (self p04Label: 51) 0 1)
    (self uiAddChoice: 2 (self p04Label: 60) 0 1)
    (self uiAddChoice: 3 (self p04Label: 4) 0 1))
(method (p04BuildJournal &tmp i line)
    (p04 qCancel:) (= bridgeReaderActive 0)
    (self uiClearChoices: "EVIDENCE JOURNAL" 208 0)
    (for ((= i 0)) (< i 3) ((++ i))
        (= line (p04 p04JournalAt: i))
        (if line (self uiAddChoice: line (self p04RecordLabel: line) 0 1)))
    (self uiAddChoice: 100 "RECORDED INVITATION EVIDENCE" 0 1)
    (self uiAddChoice: 101 (self p03Label: 34) 0 1)
(if p06 (self uiAddChoice: 102 "Vivian: screen observations" 0 1))
(if (and p08 (>= (p08 h8V: 1 0) 5))
 (self uiAddChoice: 103 "Evening archive: the system note" 0 1)
 (self uiAddChoice: 104 "Evening archive: what everyone said" 0 1))
(if (and ((ScriptID 992 0) h10Active:) ((ScriptID 992 0) p10Ready:)) (self uiAddChoice: 105 "Restored cue order" 0 1))(if ((ScriptID 993 0) h11Active:) (self uiAddChoice: 106 "Move the display safely" 0 1)))
(method (p04Journal line &tmp i)
    (p04 qCancel:)
    (for ((= i 0)) (< i 3) ((++ i))
        (if (and line (== line (p04 p04JournalAt: i)))
            (return (self p04HostQueue: line)))) (return 0))
(method (p04Hint)
    (p04 qRun: self 3 0 0 0) (self p04HostFinish:))
(method (p04WorldControls)
    (if (or (not p04) onApron (!= location 3)) (return 0))
    ; uiHit searches backward: register the frozen precedence in reverse order.
    ; Own the sole room3 audience edge; omit the host's generic edge for room3.
    (self uiAddControl: 1 9 44 290 144 320 "EDGE")
    (if (== (p04 p04Gate?) 1) (self uiAddControl: 1 19 49 224 119 270 "COURTYARD"))
    (self uiAddControl: 1 17 44 10 121 62 "PORCH")
    (if (== (p04 p04Gate?) 1)
        (self uiAddControl: 1 60 56 196 126 230 (self p04Label: 60))
    else (self uiAddControl: 1 60 55 221 116 270 (self p04Label: 60)))
    (self uiAddControl: 1 54 60 141 132 171 (self p04Label: 54))
    (self uiAddControl: 1 51 61 220 111 232 (self p04Label: 51))
    (self uiAddControl: 1 55 63 181 81 194 (self p04Label: 55))
    (if (== (p04 p04Gate?) 1)
        (self uiAddControl: 1 58 78 193 95 208 (self p04Label: 58))
    else (self uiAddControl: 1 58 67 255 83 269 (self p04Label: 58)))
    ; Exactly one bunting: caught at the current latch, held (no world hit),
    ; or on the stationary hook. Caught hit bounds are the frozen 17x18 cel.
    (if (== (p04 p04Bunting?) 0)
        (if (== (p04 p04Gate?) 1)
            (self uiAddControl: 1 62 82 197 100 214 (self p04Label: 62))
        else (self uiAddControl: 1 62 69 258 87 275 (self p04Label: 62)))
    else (if (== (p04 p04Bunting?) 2)
        (self uiAddControl: 1 62 73 176 95 198 (self p04Label: 62))))
    ; The tethered fixture remains visible/inspectable before its use unlocks.
    (if (p04 p04Peg?)
        (self uiAddControl: 1 56 108 198 125 213 (self p04Label: 56))
    else (self uiAddControl: 1 56 94 217 121 230 (self p04Label: 56)))
    (if (p04 p04Wedge?) (self uiAddControl: 1 4 117 193 131 214 "WEDGE"))
    (return 1))
(method (drawSidePassage)
 (return ((ScriptID 991 0) drawSidePassage: self)))
(method (p04Felix)
 (return ((ScriptID 991 0) p04Felix: self)))
(method (p04ApproachX obj)
    (switch obj
        (4 (return 206))
        (9 (return 286))
        (13 (return 248))
        (17 (return 55))
        (19 (return 248))
        (51 (return 234))
        (54 (return 131))
        (55 (return 181))
        (56 (return (if (p04 p04Peg?) 207 else 218)))
        (58 (return (if (== (p04 p04Gate?) 1) 204 else 265)))
        (60 (return (if (== (p04 p04Gate?) 1) 213 else 248)))
        (62 (return (if (== (p04 p04Bunting?) 2) 181
            else (if (== (p04 p04Gate?) 1) 204 else 265)))))
    (return 140))
(method (p04ApproachY obj)
    (switch obj
        (4 (return 135))
        (9 (return 137))
        (13 (return 135))
        (17 (return 134))
        (19 (return 135))
        (51 (return 134))
        (54 (return 138))
        (55 (return 134))
        (56 (return 135))
        (58 (return (if (== (p04 p04Gate?) 1) 134 else 135)))
        (60 (return 135))
        (62 (return (if (== (p04 p04Bunting?) 2) 134
            else (if (== (p04 p04Gate?) 1) 134 else 135)))))
    (return 132))
(method (p04Label obj) (switch obj
    (60 (return "Side gate"))
    (51 (return "Aligned hinges"))
    (58 (return "Latch arm"))
    (62 (return "Welcome bunting"))
    (55 (return "Fixed decoration hook"))
    (56 (return "Hold-open peg"))
    (4 (return "Wooden wedge"))
    (52 (return "Felix's circulation plan"))
    (53 (return "Felix's circulation plan"))
    (54 (return "FELIX")) (57 (return "Jackie Tree")) (61 (return "VIVIAN"))
) (return "ITEM"))
(method (p04RecordLabel line) (switch line (11 (return (self p04Label: 55))) (17 (return "FELIX")) (30 (return (self p04Label: 53)))) (return (self p04Label: 60)))
(method (p04Initialize)
(self p05Initialize:)

    (= p04 (ScriptID 984 0)) (p04 p04Init:)
    (p04 qEnabled: (p04 qRoutesReady: self))
(= p08 (ScriptID 989 0)) (if (not (p08 h8Init: self)) (p08 h8Uncertain:))

(= p09 (ScriptID 990 0)) (p09 h9Init: self)
)
(method (p04RoomArrived previous)
    (if (and (== location 3) (not onApron))
        (= motionX (* (if (== previous 4) 251 else 69) 64))
        (= motionY (* (if (== previous 4) 136 else 137) 64)))
    (if p04 (self p02HostInventory:)))

(method (p05RestoreValidate)
(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)

(if (and p07 (not (p07 h7RestoreValidate:))) (self p05RestoreReject:) (return 0))
 (if (and p05 (not (p05 hRestoreValidate:))) (= uiPanel 0) (= uiBackPanel 0) (= uiChoiceCount 0) (= bridgeReaderActive 0) (= bridgeQueueCount 0) (= bridgeQueueIndex 0) (= uiFailure 10) (= dirty 1) (if p07 (p07 h7RestoreValid: 0)) (if p08 (p08 h8RestoreReject:)) (return 0)) (if (and p06 (not (p06 h6RestoreValidate:))) (self p05RestoreReject:) (return 0)) (if (and p08 (not (p08 h8RestoreFinish:))) (self p05RestoreReject:) (return 0)) (if (and p09 (not (p09 h9RestoreCard: 1 self))) (self p05RestoreReject:) (return 0)) (if (not ((ScriptID 993 0) h11Load: 1)) (self p05RestoreReject:) (return 0)) (if (not ((ScriptID 994 0) h12Load: 1)) (self p05RestoreReject:) (return 0)) (if (not ((ScriptID 995 0) h13Load: 1)) (self p05RestoreReject:) (return 0)) (if (not ((ScriptID 996 0) h14Load: 1)) (self p05RestoreReject:) (return 0)) (return 1))
(method (p05WalkCorridor) (return (if (and p05 (== location 4) (not onApron)) 141 else 132)))

(method (p05Initialize)
 (= p05 (ScriptID 985 0)) (p05 hInit: self)
(= p06 (ScriptID 987 0)) (p06 h6Init: self p05)

(= p07 (ScriptID 988 0)) (p07 h7Init: self p05)
)
(method (p05LinePages line &tmp pages)
 (if (or (not dialogue) (< line 1) (> line 59)) (return 0))
 (= pages (dialogue sdPageCount: (+ 420 line)))
 (return (if (and (> pages 0) (<= pages 64)) pages else 0)))
(method (p05Queue line &tmp before)
 (if (or bridgeSilent (not (self p05LinePages: line)) (< bridgeQueueCount 0) (>= bridgeQueueCount 32)) (return 0))
 (= before bridgeQueueCount)
 (if (not (dialogue sdQueueSet: before 1)) (return 0))
 (= [bridgeQueue before] (+ 420 line)) (++ bridgeQueueCount) (return 1))
(method (p05Transition room &tmp routeFrom)
(if (and p08 (p08 h8RouteBusy:)) (return 0))

(if (and p08 (p08 h8ActionBarrier:)) (return 0))

 (if (or p03Invalid p04Invalid (and p05 (p05 hBarrier:))) (return 0))
 (if (and p03 (not (p03 bBeforeTravel: self))) (self p03HostFinish:) (return 0))
 (self bridgeCancelReading: 3) (if p04 (p04 qCancel:))
 (= routeFrom location) (= location room) (= onApron 0) (= roomSeen -1) (= motionVerb 0) (= motionFirst 0) (= motionSecond 0)
 (= motionPhase 0) (self uiCancelSentence:)
 (= motionX (* (if (== room 5) 26 else 159) 64)) (= motionY (* 140 64))
 (self hostRoomChanged:) (= motionX (* (if (== room 5) 26 else 159) 64)) (= motionY (* 140 64)) (self p02HostInventory:) (= dirty 1) (if p08 (p08 h8RouteTravel: routeFrom 0 p02Revision)) (return 1))
(method (p05FocusMark &tmp i)
 (= i uiFocus)
 (if (or (< i 0) (>= i uiControlCount) (!= [uiActions i] 1) (!= [uiPayloads i] 69)) (return 0))
 (return (p05 hMarkAt: (/ (+ [uiLefts i] [uiRights i]) 2) (/ (+ [uiTops i] [uiBottoms i]) 2))))
(method (p05RestoreBegin)
((ScriptID 996 0) h14Load: 0)

((ScriptID 995 0) h13Load: 0)

((ScriptID 994 0) h12SuccessorCancel:)

((ScriptID 994 0) h12Load: 0)

(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)

(if (not ((ScriptID 993 0) h11Load: 0)) (return 0))

(= p09 (ScriptID 990 0)) (= p08 (ScriptID 989 0))
(if (or (not p09) (not (p09 h9RestoreCard: 0 self))) (return 0))
(= p08 (ScriptID 989 0)) (if (or (not p08) (not (p08 h8RestoreBegin: self))) (return 0))

 (= p07 (ScriptID 988 0)) (if p07 (p07 h7RestoreValid: 0)) (= p05 (ScriptID 985 0)) (= p06 (ScriptID 987 0)) (if p06 (p06 h6RestoreValid: 0)) (= dialogue (ScriptID 982 0)) (= presentation (ScriptID 980 0))
 (if (or (not p05) (not p06) (not (p05 hRestoreBegin: self))) (return 0))
 (if (not (p06 h6RestoreBegin: self p05)) (return 0)) (return (p07 h7RestoreBegin: self p05)))
(method (p05RetireTransient &tmp i)
(if p08 (p08 h8ReaderRetire: 4))

(if p08 (p08 h8RouteRetire:))

 ; RestoreGame resumes through replay, not the old invocation stack. This single
 ; dispatcher uses no registered callback objects. Drain native event backlog,
 ; synchronously cancel PCM/Sync and all current UI/audio/movement work.
 (if presentation (presentation cancel: 14))
 (if dialogue (if (not (p05 hFailure?)) (dialogue sdAfterRestore: presentation) else (dialogue sdInterrupt: presentation 14) (dialogue sdActive: 0)) (dialogue sdSuppress:))
 (= audioPending 0) (= audioDialogue 0) (= audioDuckTicks 0)
 (= motionVerb 0) (= motionFirst 0) (= motionSecond 0) (= motionPhase 0) (= motionNotice 0)
 (= uiReveal 0) (= uiControlCount 0) (= type 0) (= message 0) (= modifiers 0)
 (for ((= i 0)) (< i 64) ((++ i))
  (= [uiActions i] 0) (= [uiPayloads i] 0) (= [uiLabels i] 0))
 (while (GetEvent 32767 self))
 (= type 0) (= message 0) (= modifiers 0)
 (return 1))
(method (p05ChoiceValue index field)
 (if (or (< index 0) (>= index uiChoiceCount) (>= index 32)) (return 0))
 (switch field (0 (return [uiChoiceIds index])) (1 (return [uiChoiceLabels index]))
  (2 (return [uiChoiceEnabled index])) (3 (return [uiChoiceSelected index]))) (return 0))
(method (p05RestoreReject)
((ScriptID 996 0) h14Load: 2)

((ScriptID 995 0) h13Load: 2)

((ScriptID 994 0) h12SuccessorCancel:)

((ScriptID 994 0) h12Load: 2)

(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)

((ScriptID 993 0) h11Load: 2)

(if p09 (p09 h9RestoreCard: 2 self))
(if p08 (p08 h8RestoreReject:))

(if p07 (p07 h7RestoreValid: 0))

 (DoSound 9 credits) (DoSound 7 credits) (DoSound 9 bed) (DoSound 7 bed)
 (= musicUnavailable 1)
 (= uiPanel 0) (= uiBackPanel 0) (= uiChoiceCount 0) (= bridgeReaderActive 0)
 (= bridgeQueueCount 0) (= bridgeQueueIndex 0) (= uiFailure 10) (= dirty 1) (return 0))

(method (h6BaseControls)
(if (and p08 (p08 h8LayoutControls:)) (return 0))

(if (and p05 (p05 hCourtControls:)) (return 0)) (if (and p05 (p05 hWorldControls:)) (return 0))

        (if (and (== location 3) (not onApron))
            (self p04WorldControls:)
            (self uiAddControl: 1 32 2 160 12 211 "NOTES") (return 0))
        (asm
            pToa onApron
            bnt L_2968
            pushi 269
            pushi 7
            push1
            pushi 11
            pushi 102
            pushi 8
            pushi 134
            pushi 112
            lofss "RETURN"
            self 18
            pushi 269
            pushi 7
            push1
            pushi 10
            pushi 52
            pushi 161
            pushi 130
            pushi 307
            lofss "AUDIENCE"
            self 18
            jmp L_2e11
            L_2968: pTos location
            dup
            ldi 0
            eq?
            bnt L_2af6
            pushi 230
            push1
            pushi 3
            self 6
            bnt L_2991
            pushi 269
            pushi 7
            push1
            pushi 3
            pushi 88
            pushi 52
            pushi 119
            pushi 146
            lofss "BENCH"
            self 18
            L_2991: pushi 230
            push1
            push1
            self 6
            bnt L_29cc
            pToa doorOpen
            bnt L_29b6
            pushi 269
            pushi 7
            push1
            push1
            pushi 46
            pushi 170
            pushi 121
            pushi 191
            lofss "DOOR"
            self 18
            jmp L_29cc
            L_29b6: pushi 269
            pushi 7
            push1
            push1
            pushi 46
            pushi 170
            pushi 121
            pushi 224
            lofss "FRONT DOOR"
            self 18
            L_29cc: pushi 230
            push1
            push2
            self 6
            bnt L_29e9
            pushi 269
            pushi 7
            push1
            push2
            pushi 47
            pushi 73
            pushi 85
            pushi 125
            lofss "BUNNY"
            self 18
            L_29e9: pushi 230
            push1
            pushi 14
            self 6
            bnt L_2a0b
            pToa houseEntered
            bnt L_2a0b
            pushi 269
            pushi 7
            push1
            pushi 14
            pushi 88
            push0
            pushi 116
            pushi 33
            lofss "SIDE PASSAGE"
            self 18
            L_2a0b: pushi 230
            push1
            pushi 15
            self 6
            bnt L_2a2d
            pToa houseEntered
            bnt L_2a2d
            pushi 269
            pushi 7
            push1
            pushi 15
            pushi 49
            push0
            pushi 77
            pushi 48
            lofss "MILO'S GARAGE"
            self 18
            L_2a2d: pushi 230
            push1
            pushi 16
            self 6
            bnt L_2a52
            pToa houseEntered
            bnt L_2a52
            pushi 269
            pushi 7
            push1
            pushi 16
            pushi 20
            pushi 229
            pushi 37
            pushi 283
            lofss "CONSERVATORY"
            self 18
            L_2a52: pushi 230
            push1
            pushi 4
            self 6
            bnt L_2a9a
            pTos wedge
            ldi 1
            ne?
            bnt L_2a9a
            pTos wedge
            ldi 2
            eq?
            bnt L_2a83
            pushi 269
            pushi 7
            push1
            pushi 4
            pushi 105
            pushi 184
            pushi 119
            pushi 204
            lofss "WEDGE"
            self 18
            jmp L_2a9a
            L_2a83: pushi 269
            pushi 7
            push1
            pushi 4
            pushi 74
            pushi 131
            pushi 87
            pushi 151
            lofss "WEDGE"
            self 18
            L_2a9a: pushi 230
            push1
            pushi 5
            self 6
            bnt L_2ac0
            pTos tray
            ldi 0
            ne?
            bnt L_2ac0
            pushi 269
            pushi 7
            push1
            pushi 5
            pushi 86
            pushi 78
            pushi 105
            pushi 121
            lofss "BREAD TRAY"
            self 18
            L_2ac0: pToa doorOpen
            bnt L_2af3
            pushi 269
            pushi 7
            pushi 18
            push1
            pushi 49
            pushi 191
            pushi 105
            pushi 224
            lofss "ENTER"
            self 18
            pushi 269
            pushi 7
            pushi 18
            push1
            pushi 105
            pushi 204
            pushi 128
            pushi 235
            lofss "ENTER"
            self 18
            L_2af3: jmp L_2dae
            L_2af6: dup
            ldi 1
            eq?
            bnt L_2c0b
            pushi 269
            pushi 7
            push1
            pushi 17
            pushi 54
            pushi 18
            pushi 114
            pushi 45
            lofss "PORCH"
            self 18
            pushi 269
            pushi 7
            push1
            pushi 12
            pushi 54
            pushi 283
            pushi 116
            pushi 312
            lofss "KITCHEN"
            self 18
            pushi 269
            pushi 7
            push1
            pushi 13
            pushi 52
            pushi 158
            pushi 111
            pushi 184
            lofss "COURTYARD"
            self 18
            pushi 269
            pushi 7
            push1
            pushi 7
            pushi 50
            pushi 84
            pushi 84
            pushi 132
            lofss "COMPARISON BOARD"
            self 18
            pushi 269
            pushi 7
            push1
            pushi 8
            pushi 61
            pushi 133
            pushi 128
            pushi 157
            lofss "FRANKIE MAPLEWOOD"
            self 18
            pushi 269
            pushi 7
            push1
            push2
            pushi 62
            pushi 226
            pushi 129
            pushi 253
            lofss "BUNNY"
            self 18
            pTos p02CopyBunny
            ldi 1
            eq?
            bnt L_2ba2
            pushi 269
            pushi 7
            push1
            pushi 21
            pushi 85
            pushi 62
            pushi 95
            pushi 91
            lofss "BUNNY'S INVITATION"
            self 18
            L_2ba2: pTos p02CopyBunny
            ldi 11
            eq?
            bt L_2bb2
            pTos p02CopyBunny
            ldi 14
            eq?
            bnt L_2bc7
            L_2bb2: pushi 269
            pushi 7
            push1
            pushi 21
            pushi 58
            pushi 105
            pushi 69
            pushi 122
            lofss "BUNNY'S INVITATION"
            self 18
            L_2bc7: pToa p02BoardRecords
            bnt L_2be2
            pushi 269
            pushi 7
            push1
            pushi 26
            pushi 70
            pushi 88
            pushi 78
            pushi 129
            lofss "MATCHED BORDER"
            self 18
            L_2be2: pushi 230
            push1
            pushi 4
            self 6
            bnt L_2c08
            pTos wedge
            ldi 1
            ne?
            bnt L_2c08
            pushi 269
            pushi 7
            push1
            pushi 4
            pushi 109
            pushi 25
            pushi 119
            pushi 44
            lofss "WEDGE"
            self 18
            L_2c08: jmp L_2dae
            L_2c0b: dup
            ldi 2
            eq?
            bnt L_2c1a
            pushi 624
            push0
            self 4
            jmp L_2dae
            L_2c1a: dup
            ldi 3
            eq?
            bnt L_2c63
            pushi 230
            push1
            pushi 17
            self 6
            bnt L_2c3f
            pushi 269
            pushi 7
            push1
            pushi 17
            pushi 70
            pushi 14
            pushi 117
            pushi 64
            lofss "PORCH"
            self 18
            L_2c3f: pushi 230
            push1
            pushi 19
            self 6
            bnt L_2c60
            pushi 269
            pushi 7
            push1
            pushi 19
            pushi 70
            pushi 235
            pushi 117
            pushi 282
            lofss "SIDE GATE"
            self 18
            L_2c60: jmp L_2dae
            L_2c63: dup
            ldi 4
            eq?
            bnt L_2cac
            pushi 230
            push1
            pushi 18
            self 6
            bnt L_2c88
            pushi 269
            pushi 7
            push1
            pushi 18
            pushi 64
            pushi 14
            pushi 115
            pushi 69
            lofss "LIVING ROOM"
            self 18
            L_2c88: pushi 230
            push1
            pushi 19
            self 6
            bnt L_2ca9
            pushi 269
            pushi 7
            push1
            pushi 19
            pushi 65
            pushi 235
            pushi 116
            pushi 282
            lofss "SIDE GATE"
            self 18
            L_2ca9: jmp L_2dae
            L_2cac: dup
            ldi 5
            eq?
            bnt L_2d42
            pushi 230
            push1
            pushi 17
            self 6
            bnt L_2cd2
            pushi 269
            pushi 7
            push1
            pushi 17
            pushi 64
            pushi 14
            pushi 119
            pushi 60
            lofss "PORCH"
            self 18
            L_2cd2: pushi 230
            push1
            pushi 28
            self 6
            bnt L_2cf3
            pushi 269
            pushi 7
            push1
            pushi 28
            pushi 60
            pushi 117
            pushi 129
            pushi 143
            lofss "MILO"
            self 18
            L_2cf3: pushi 230
            push1
            pushi 27
            self 6
            bnt L_2d14
            pushi 269
            pushi 7
            push1
            pushi 27
            pushi 81
            pushi 171
            pushi 111
            pushi 230
            lofss "INVITATION DRAWER"
            self 18
            L_2d14: pushi 230
            push1
            pushi 24
            self 6
            bnt L_2d40
            pushi 194
            push1
            pushi 24
            self 6
            not
            bnt L_2d40
            pushi 269
            pushi 7
            push1
            pushi 24
            pushi 81
            pushi 187
            pushi 96
            pushi 211
            lofss "COMPLETE MASTER INVITATION"
            self 18
            L_2d40: jmp L_2dae
            L_2d42: dup
            ldi 6
            eq?
            bnt L_2dae
            pushi 230
            push1
            pushi 17
            self 6
            bnt L_2d67
            pushi 269
            pushi 7
            push1
            pushi 17
            pushi 44
            pushi 11
            pushi 112
            pushi 42
            lofss "PORCH"
            self 18
            L_2d67: pushi 230
            push1
            pushi 29
            self 6
            bnt L_2d89
            pushi 269
            pushi 7
            push1
            pushi 29
            pushi 63
            pushi 155
            pushi 129
            pushi 185
            lofss "STRINGER"
            self 18
            L_2d89: pTos p02CopyStringer
            ldi 6
            eq?
            bnt L_2da8
            pushi 269
            pushi 7
            push1
            pushi 22
            pushi 66
            pushi 220
            pushi 80
            pushi 239
            lofss "STRINGER'S INVITATION"
            self 18
            L_2da8: pushi 594
            push0
            self 4
            L_2dae: toss
            pTos location
            ldi 6
            eq?
            bnt L_2dd1
            pushi 269
            pushi 7
            push1
            pushi 9
            pushi 134
            pushi 286
            pushi 143
            pushi 318
            lofss "EDGE"
            self 18
            jmp L_2e11
            L_2dd1: pTos location
            ldi 1
            eq?
            bt L_2ddf
            pTos location
            ldi 2
            eq?
            bnt L_2df9
            L_2ddf: pushi 269
            pushi 7
            push1
            pushi 9
            pushi 116
            pushi 313
            pushi 144
            pushi 320
            lofss "EDGE"
            self 18
            jmp L_2e11
            L_2df9: pushi 269
            pushi 7
            push1
            pushi 9
            pushi 80
            pushi 288
            pushi 134
            pushi 320
            lofss "EDGE"
            self 18
            L_2e11: pushi 269
            pushi 7
            push1
            pushi 32
            push2
            pushi 160
            pushi 12
            pushi 211
            lofss "NOTES"
            self 18
            ret
        )
    )
(method (h6BaseDrawWorld)
 (return ((ScriptID 991 0) h6BaseDrawWorld: self)))
(method (h6BaseInventory &tmp t0)
        (asm
            pTos p02InventoryExtent
            ldi 64
            gt?
            bnt L_7281
            ldi 4
            aTop bridgeFailure
            ldi 0
            ret
            L_7281: pToa p02InventoryExtent
            aTop uiInventoryExtent
            ldi 0
            sat 0
            L_728b: lst 0
            ldi 64
            lt?
            bnt L_72af
            lst 0
            pToa p02InventoryExtent
            lt?
            bnt L_72a4
            pushi 210
            push1
            lst 0
            self 6
            jmp L_72a6
            L_72a4: ldi 0
            L_72a6: push
            lat 0
            sali 100
            +at 0
            jmp L_728b
            L_72af: pushi 212
            push0
            self 4
            aTop uiInventoryPages
            pTos uiInventoryPage
            pToa uiInventoryPages
            ge?
            bnt L_72ca
            pTos uiInventoryPages
            ldi 1
            sub
            aTop uiInventoryPage
            L_72ca: pToa p03
            bnt L_72d7
            pushi 525
            push1
            pushSelf
            pToa p03
            send 6
            L_72d7: pToa p04
            bnt P04_inventory_done
            pushi #qInventory
            push1
            pushSelf
            pToa p04
            send 6
            P04_inventory_done: ldi 1
            aTop dirty
            ret
        )
    )
(method (h6BaseTopics arg1 &tmp t0)
        (asm
            pToa bridgeSilent
            bnt L_7340
            ldi 0
            ret
            L_7340: lap 1
            aTop bridgeChoiceActor
            ldi 0
            aTop bridgeReaderActive
            pushi 282
            pushi 3
            pushi 55
            push1
            lsp 1
            self 6
            push
            pushi 202
            push0
            self 10
            ldi 1
            sat 0
            L_7361: lst 0
            ldi 9
            le?
            bnt L_738b
            pushi 240
            push2
            lsp 1
            lst 0
            self 8
            bnt L_7387
            pushi 268
            pushi 4
            lst 0
            pushi 85
            push1
            lst 0
            self 6
            push
            push0
            push1
            self 12
            L_7387: +at 0
            jmp L_7361
            L_738b: pToa p03
            bnt L_73b4
            pushi 550
            push2
            pushSelf
            lsp 1
            pToa p03
            send 8
            push
            ldi 4
            and
            bnt L_73b4
            pushi 268
            pushi 4
            pushi 10
            pushi 627
            push1
            pushi 42
            self 6
            push
            push0
            push1
            self 12
            L_73b4: ret
        )
    )
(method (h6PublishNative count first second extent &tmp h10Page i)
(if (not ((ScriptID 993 0) h11ReadAbort:)) (return 0))
(= [h11MainRead 0] 0)
 (= h10Page uiInventoryPage)
 (if count
  (= [bridgeQueue bridgeQueueCount] first) (dialogue sdQueueSet: bridgeQueueCount 1) (++ bridgeQueueCount))
 (if (> count 1)
  (= [bridgeQueue bridgeQueueCount] second) (dialogue sdQueueSet: bridgeQueueCount 1) (++ bridgeQueueCount))
 (for ((= i 0)) (< i 64) ((++ i)) (= [uiItems i] (p06 h6ReservedItem: i)))
 (= uiInventoryExtent extent) (= uiInventoryPages (if extent (/ (+ extent 7) 8) else 1))
 (if (>= uiInventoryPage uiInventoryPages) (= uiInventoryPage (- uiInventoryPages 1)))
 (= dirty 1) (if (and p09 (not (p09 h9ProjectCard:))) (return 0)) (if (not ((ScriptID 992 0) h10Proj:)) (return 0)) (if (and (>= h10Page 0) (< h10Page uiInventoryPages)) (= uiInventoryPage h10Page)) (return 1))

(method (h7BaseControls) (self h6BaseControls: ) (if p06 (p06 h6Controls:)) (return 1))
(method (h7BasePreparationHint)
(if (and p08 (p08 h8ActionBarrier:)) (return 0))

(if (and p06 p02PlanAgreed (== location 0) (not onApron)) (p06 h6Hint:) (return 0))

(if (and p05 (p05 hBarrier:)) (return 0)) (if (and p05 p02PlanAgreed (== location 5) (not (& (p05 p05Flags:) 4))) (p05 hHintNext:) (return 0))

        (if (and p04 p02PlanAgreed (== location 3) (not (p04 p04Ready:)))
            (self p04Hint:) (return 0))
    (if (and p03 p02PlanAgreed (not (p03 p03Ready?)))
        (p03 bHint: self 0) (self p03HostFinish:)
    else (self p02Hint: 0) (self bridgeFlush:)))
(method (h7PublishNative count first second)
 (if count (= [bridgeQueue bridgeQueueCount] first) (dialogue sdQueueSet: bridgeQueueCount 1) (++ bridgeQueueCount))
 (if (> count 1) (= [bridgeQueue bridgeQueueCount] second) (dialogue sdQueueSet: bridgeQueueCount 1) (++ bridgeQueueCount))
 (= dirty 1) (return 1))















(method (h8VI index field) (if (or (< index 0) (>= index uiControlCount)) (return -1)) (switch field (0 (return [uiActions index])) (1 (return [uiPayloads index]))) (return -1))

(method (h9PublishCard slot)
 (if (or (not p09) (< slot 0) (>= slot 64) (!= slot uiInventoryExtent)
  [uiItems slot] (not (p09 h9CardHeld: 399))) (return 0))
 (= [uiItems slot] 399) (++ uiInventoryExtent)
 (= uiInventoryPages (/ (+ uiInventoryExtent 7) 8)) (= dirty 1) (return 1))
(method (h10UI index obj)
 (if (or (< index 0) (>= index 64) (< obj 0) (== obj 35)
  (and (> obj 94) (!= obj 399) (< ((ScriptID 992 0) p10CueIndex: obj) 0))) (return 0))
 (if (and (>= ((ScriptID 992 0) p10CueIndex: obj) 0) (!= ((ScriptID 992 0) h10Q: 1 obj) 1)) (return 0))
 (= [uiItems index] obj) (return 1))



















(method (h11RenderLive) (return (and (== self (ScriptID 0 0)) [h11MainRead 0])))









































(method (h13NativeChoices mode delta)
 (if (or (!= self (ScriptID 0 0)) (not dialogue) (!= uiPanel 2)
  (< uiChoiceContext 250) (> uiChoiceContext 256) (<= uiChoiceCount 0) (> uiChoiceCount 32)) (return 0))
 (= uiPageCount uiChoiceCount)
 (if (== mode 1) (= uiPage (+ uiPage delta)) (= uiFocus 0))
 (if (< uiPage 0) (= uiPage 0)) (if (>= uiPage uiPageCount) (= uiPage (- uiPageCount 1)))
 (if (or (== mode 0) (== mode 1))
  (= uiControlCount 0)
  (dialogue sdChoiceControls: self uiChoiceCount uiPage uiChoiceMulti [uiChoiceLabels uiPage] [uiChoiceEnabled uiPage])
  (if (or (< uiFocus 0) (>= uiFocus uiControlCount)) (= uiFocus 0)))
 (if (== mode 2)
  (self uiBuildFocus:)
  (if (not (dialogue sdDrawChoice: self uiTitle [uiChoiceLabels uiPage] uiPage uiChoiceCount
   [uiChoiceSelected uiPage] uiChoiceMulti [uiChoiceEnabled uiPage])) (= uiFailure 8)))
 (if (== mode 1) (= dirty 1)) (return 1))




















































































































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
