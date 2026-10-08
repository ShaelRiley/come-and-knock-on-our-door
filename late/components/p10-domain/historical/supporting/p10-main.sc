;;; Sierra Script 1.0 - (do not remove this comment)
; Original compile-only harness. No scene, audio, save kernel or UI.
(script# 0)
(use module992)
(public p10Harness 0)
(local [globals 100])
(class Game
    (properties
        type 0 message 0 modifiers 0 x 0 y 0
        helper 0 failure 0
    )
    (method (play)
        (= helper (ScriptID 992 0))
        (if (not helper) (= failure 1) (return 0))
        (if (not (IsObject P10State)) (= failure 2) (return 0))
        (helper p10Init:)
        (helper p10Context: 0 0 1 0 0 0 6 0 0 1)
        (if (not (helper p10ValidateContext:)) (= failure 3))
        (return 0))
)
(instance p10Harness of Game)
