;;; Sierra Script 1.0 - (do not remove this comment)
; Original compile-only harness. No scene, audio, save kernel or UI.
(script# 0)
(use module993)
(public p11Harness 0)
(local [globals 100])
(class Game
    (properties
        type 0 message 0 modifiers 0 x 0 y 0
        helper 0 failure 0
    )
    (method (play)
        (= helper (ScriptID 993 0))
        (if (not helper) (= failure 1) (return 0))
        (if (not (IsObject P11State)) (= failure 2) (return 0))
        (helper p11Init:)
        (helper p11Context: 3 0 1 1 1 1 3 0 4 6 3 3 0 0 0 1 1 0 1 0 1)
        (if (not (helper p11ValidateContext:)) (= failure 3))
        (return 0))
)
(instance p11Harness of Game)
