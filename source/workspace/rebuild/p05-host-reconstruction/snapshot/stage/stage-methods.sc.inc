; ORIGINAL VC01.STAGE reconstruction. Append inside P05State985, not a new class.
; SINGLE OWNER: hVCStageRender replaces the ENTIRE ordinary garage actor path.
; Visual anchors are constants only. No motion/world/owner/score writes.
(method (hStageActive)
 (return (if (and hVCStage hHost (== (hHost location?) 5)
  (not (hHost onApron?)) (== hMiloRoom 5) hContest
  (== (hContest vcRead: 90) 1) (== (hContest vcRead: 91) 1)
  (>= (hContest vcRead: 92) 1) (<= (hContest vcRead: 92) 8)) 1 else 0)))
(method (hStageRetire)
 (if (and hHost (or hVCHitActor hVCWinceActor hStageHitAge hStageKOAge)) (hHost dirty: 1))
 (= hVCHitActor 0) (= hVCWinceActor 0)
 (= hStageHitAge 0) (= hStageKOAge 0) (return 1))
(method (hStageTick dt &tmp oldJack oldMilo)
 ; Host calls once per normal frame. Ages never gate a choice/result/receipt.
 (if (not (self hStageActive:)) (return (self hStageRetire:)))
 (= oldJack (self hStagePose: 1)) (= oldMilo (self hStagePose: 2))
 (if (< dt 0) (= dt 0)) (if (> dt 6) (= dt 6))
 (if hVCHitActor
  (if (< hStageHitAge 18) (= hStageHitAge (+ hStageHitAge dt)))
 else (= hStageHitAge 0))
 (if hVCWinceActor
  (if (< hStageKOAge 24) (= hStageKOAge (+ hStageKOAge dt)))
 else (= hStageKOAge 0))
 (if (or (!= oldJack (self hStagePose: 1)) (!= oldMilo (self hStagePose: 2))) (hHost dirty: 1))
 (return 1))
(method (hStagePose who)
 ; Reduced-motion keeps one still non-contact pose until ordinary lifecycle
 ; cancellation. No oscillation, offset, animation, new sound, or event.
 (if (and (== hVCWinceActor who) (or hVCReducedMotion (< hStageKOAge 24))) (return 1))
 (if (and (== hVCHitActor who) (or hVCReducedMotion (< hStageHitAge 18))) (return 1))
 (return 0))
(method (hStageActors &tmp presenter mouth)
 (if (not (self hStageActive:)) (return 0))
 ; Ordinary collective studio onlookers gather under the authored STAGE cue.
 ; They are silent extras, NOT a ninth principal, private witness, or new invite.
 (DrawCel 331 0 0 20 58 -1 116 116)
 (DrawCel 331 0 1 273 61 -1 116 116)
 ; Actual Bunny remains at her room anchor and requires both location/willingness.
 (if (and hVCBunnyWilling (== hBunnyRoom 5))
  (DrawCel 219 1 0 245 57 -1 116 116))
 ; Static code-derived transparent checker matte dims room and willing audience.
 ; Principals are then drawn once in the clear theatrical beam; props stay put.
 (DrawCel 331 0 2 0 44 -1 0)
 (= presenter (hHost presentation?)) (= mouth 0)
 (if (and presenter (== (presenter lane?) 1) (== (presenter speaker?) 5))
  (= mouth (presenter mouth?)))
 (if (or (< mouth 0) (> mouth 2)) (= mouth 0))
 ; Existing Milo: foot100,129 native26,78 scale116, right-facing.
 (if (self hStagePose: 2) (DrawCel 330 0 1 77 59 -1 116 116)
 else (DrawCel 221 0 mouth 77 59 -1 116 116))
 ; Jackie display-only foot180,140 scale127, left-facing. World fields untouched.
 (if (self hStagePose: 1) (DrawCel 330 1 0 155 63 -1 127 127)
 else (DrawCel 214 1 0 155 63 -1 127 127))
 (return 1))
(method (hVCStageRender)
 (if (not (self hStageActive:)) (return 0))
 (self hGarageBackdrop:)
 (self hStageActors:)
 (return 1))
(method (hStageMeter left value &tmp c i x)
 (= c (if (== value 3) 16 else (if (== value 2) 33 else 208)))
 (for ((= i 0)) (< i 3) ((++ i))
  (= x (+ left (* i 36)))
  (Graph 11 27 x 38 (+ x 33) 1 c 0 0)
  (Graph 11 28 (+ x 1) 37 (+ x 32) 1 (if (< i value) c else 5) 0 0))
 (return 1))
(method (hVCHud &tmp a b color)
 (if (not (self hStageActive:)) (return 0))
 (= a (hContest vcRead: 96)) (= b (hContest vcRead: 97))
 (if (or (< a 0) (> a 3) (< b 0) (> b 3) (and (== a 0) (== b 0))) (return 0))
 (Graph 11 0 0 44 320 1 0 0 0)
 (Graph 11 42 0 44 320 1 9 0 0)
 ; The named sides align with actual actors: Milo on left, Jackie on right.
 (Display "MILO PENNANT" 100 8 4 102 1 105 0 106 100 121)
 (Display "JACKIE TREE" 100 246 4 102 1 105 0 106 70 121)
 (Format @hVCMeterText "%d/3" b)
 (Display @hVCMeterText 100 8 16 102 1 105 0 106 24 121)
 (Format @hVCMeterText "%d/3" a)
 (Display @hVCMeterText 100 294 16 102 1 105 0 106 24 121)
 (Display "COMPOSURE" 100 44 16 102 1 105 0 106 60 121)
 (Display "COMPOSURE" 100 212 16 102 1 105 0 106 60 121)
 (self hStageMeter: 8 b) (self hStageMeter: 207 a)
 (= color (if (or (== a 0) (== b 0)) 208 else 13))
 (Graph 11 11 145 34 175 1 color 0 0)
 (Graph 11 12 146 33 174 1 0 0 0)
 (Display "KO" 100 154 19 102 color 105 0 106 18 121)
 (return 1))
