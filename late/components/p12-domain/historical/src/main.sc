;;; Sierra Script 1.0 - (do not remove this comment)
; Original compile-only harness. No scene, audio, save kernel or UI.
(script# 0)
(use module994)
(public p12Harness 0)
(local [globals 100])
(class Game
    (properties
        type 0 message 0 modifiers 0 x 0 y 0
        helper 0 failure 0
    )
    (method (play)
        (= helper (ScriptID 994 0))
        (if (not helper) (= failure 1) (return 0))
        (if (not (IsObject P12State)) (= failure 2) (return 0))
        (helper p12Init:)
        (helper p12Context: 4 0 1 1 1 1 4 1 1 1 0 1 4 4 4 4 4 4 4 1)
        (if (not (helper p12ValidateContext:)) (= failure 3))
        (return 0))
)
(instance p12Harness of Game)
