;;; Sierra Script 1.0 - (do not remove this comment)
; Original compile-only harness. No scene, audio, save kernel or UI.
(script# 0)
(use module995)
(public p13Harness 0)
(local [globals 100])
(class Game
    (properties
        type 0 message 0 modifiers 0 x 0 y 0
        helper 0 failure 0
    )
    (method (play)
        (= helper (ScriptID 995 0))
        (if (not helper) (= failure 1) (return 0))
        (if (not (IsObject P13State)) (= failure 2) (return 0))
        (helper p13Init:)
        (helper p13Context: 4 0 1 1 1 1 4 1 1 1 0 1 4 4 4 4 4 4 4 1)
        (if (not (helper p13ValidateContext:)) (= failure 3))
        (return 0))
)
(instance p13Harness of Game)
