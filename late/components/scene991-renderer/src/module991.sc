;;; Sierra Script 1.0 - (do not remove this comment)
; New extraction from accepted source, not recovered historical991.
; Stateless renderer: owner is supplied on every call; all self dispatch stays on owner.
(script# 991)
(public sceneRenderer 0)
(class SceneRenderer
 (properties)
(method (renderCaption owner &tmp savedAcc)
(if (and (owner p05?) ((owner p05?) hVCHud:)) (return 0))

        (asm
            sat 0
            pushi 741
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 0
            gt?
            bnt L_1c09
            pushi 739
            push0
            lap 1
            send 4
            ldi 0
            ret
            L_1c09: sat 0
            pushi 94
            push0
            lap 1
            send 4
            push
            lat 0
            dup
            ldi 1
            eq?
            bnt L_1c3c
            pushi 8
            lofss "Jackie: Tray. Packet. Spring door. Where do I grow"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "the extra hand? H hints. F1 help. M menu."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1c3c: dup
            ldi 2
            eq?
            bnt L_1c6d
            pushi 8
            lofss "Tray, packet, door. Two hands. I can't offer to do"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "anything else; I'm already using my chin."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1c6d: dup
            ldi 3
            eq?
            bnt L_1c8a
            pushi 8
            lofss "Clean, flat. The tray fits; I don't have to sit."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1c8a: dup
            ldi 4
            eq?
            bnt L_1cbb
            pushi 8
            lofss "A self-closing front door. A wedge-shaped gap is"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "visible underneath."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1cbb: dup
            ldi 5
            eq?
            bnt L_1cec
            pushi 8
            lofss "Bright wooden wedge. Same shape as the door gap. I"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "could let it do the part involving my foot."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1cec: dup
            ldi 6
            eq?
            bnt L_1d1d
            pushi 8
            lofss "Bunny sorts invitations at the window. She can open"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "it if I ask. I've chosen grunting so far."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1d1d: dup
            ldi 7
            eq?
            bnt L_1d4e
            pushi 8
            lofss "Supper club: new partners welcome. There is an"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "oddly cropped border."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1d4e: dup
            ldi 8
            eq?
            bnt L_1d7f
            pushi 8
            lofss "Frankie's board awaits the complete invitation. P02"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "is beyond this first-playable slice."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1d7f: dup
            ldi 9
            eq?
            bnt L_1db0
            pushi 8
            lofss "Jackie: A hand, please? Bunny opens the window."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "Bunny: Pass the tray. Not your elbow."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1db0: dup
            ldi 10
            eq?
            bnt L_1dcd
            pushi 8
            lofss "Bunny: The window is open. Pass the tray through."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1dcd: dup
            ldi 11
            eq?
            bnt L_1dea
            pushi 8
            lofss "Bunny: The tray is safely at the kitchen pass."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1dea: dup
            ldi 12
            eq?
            bnt L_1e07
            pushi 8
            lofss "Ask Bunny to open the window. Don't butter it."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1e07: dup
            ldi 13
            eq?
            bnt L_1e4c
            pushi 8
            lofss "Bunny: Knock next time. You looked constipated."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "[Jackie glances toward the audience; a few"
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "chuckle.] The tray is safe. My hands are free."
            pushi 100
            pushi 5
            pushi 32
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1e4c: dup
            ldi 14
            eq?
            bnt L_1e69
            pushi 8
            lofss "The tray is already safely placed."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1e69: dup
            ldi 15
            eq?
            bnt L_1e86
            pushi 8
            lofss "Jackie sets the covered tray on the clean bench."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1e86: dup
            ldi 16
            eq?
            bnt L_1ea3
            pushi 8
            lofss "Jackie picks up the tray."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1ea3: dup
            ldi 17
            eq?
            bnt L_1ec0
            pushi 8
            lofss "The tray is already held or safely inside."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1ec0: dup
            ldi 18
            eq?
            bnt L_1ef1
            pushi 8
            lofss "Jackie pockets the wedge. The door can still be"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "opened normally."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1ef1: dup
            ldi 19
            eq?
            bnt L_1f0e
            pushi 8
            lofss "The wedge is in my pocket. That's why I bulge."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1f0e: dup
            ldi 20
            eq?
            bnt L_1f2b
            pushi 8
            lofss "The wedge is still on the porch sill."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1f2b: dup
            ldi 21
            eq?
            bnt L_1f48
            pushi 8
            lofss "Jackie opens the front door."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1f48: dup
            ldi 22
            eq?
            bnt L_1f65
            pushi 8
            lofss "The front door is already open."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1f65: dup
            ldi 23
            eq?
            bnt L_1f82
            pushi 8
            lofss "Jackie closes the door."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1f82: dup
            ldi 24
            eq?
            bnt L_1f9f
            pushi 8
            lofss "Pick up the wedge first. It is holding the door."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1f9f: dup
            ldi 25
            eq?
            bnt L_1fbc
            pushi 8
            lofss "The front door is already closed."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1fbc: dup
            ldi 26
            eq?
            bnt L_1fd9
            pushi 8
            lofss "The wedge holds the door open."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_1fd9: dup
            ldi 27
            eq?
            bnt L_200a
            pushi 8
            lofss "Pick up the brightly painted wedge from the sill"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "first."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_200a: dup
            ldi 28
            eq?
            bnt L_2027
            pushi 8
            lofss "Open the door first, then wedge it open."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2027: dup
            ldi 29
            eq?
            bnt L_2058
            pushi 8
            lofss "Put the tray on the bench, or pass it to Bunny, to"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "free a hand."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2058: dup
            ldi 30
            eq?
            bnt L_2075
            pushi 8
            lofss "The wedge is already holding the door open."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2075: dup
            ldi 31
            eq?
            bnt L_20a6
            pushi 8
            lofss "A doorknob puts the bread at groin height. No. The"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "clean bench would work."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_20a6: dup
            ldi 32
            eq?
            bnt L_20c3
            pushi 8
            lofss "No help. Nothing lost. I'll leave it at that."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_20c3: dup
            ldi 33
            eq?
            bnt L_20e0
            pushi 8
            lofss "The front door is closed."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_20e0: dup
            ldi 34
            eq?
            bnt L_2111
            pushi 8
            lofss "The spring pulls the door shut. I need Bunny or the"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "clean bench to take the tray, not a bigger hip."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2111: dup
            ldi 35
            eq?
            bnt L_2142
            pushi 8
            lofss "Fetch the tray. The wedge can hold the door while I"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "pick it up. It doesn't expect a tip."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2142: dup
            ldi 36
            eq?
            bnt L_2187
            pushi 8
            lofss "The bread is safely inside. Frankie Maplewood and"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "Bunny are at the planning board. Read what everyone"
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "was actually invited to."
            pushi 100
            pushi 5
            pushi 32
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2187: dup
            ldi 37
            eq?
            bnt L_21a4
            pushi 8
            lofss "Jackie steps onto the porch."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_21a4: dup
            ldi 38
            eq?
            bnt L_21e9
            pushi 8
            lofss "Beyond the flat, an audience faces the set. The"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "same room is still right there. Walk to RETURN to"
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "go back at any time."
            pushi 100
            pushi 5
            pushi 32
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_21e9: dup
            ldi 39
            eq?
            bnt L_221a
            pushi 8
            lofss "Same set. Tray, door, wedge, progress unchanged."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "Nice to leave the house without taking a tray."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_221a: dup
            ldi 40
            eq?
            bnt L_224b
            pushi 8
            lofss "Jackie: Good evening. Audience: [A few people"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "wave.]"
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_224b: dup
            ldi 41
            eq?
            bnt L_227c
            pushi 8
            lofss "People, chairs, and a way back. They see the set,"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "not anyone's private thoughts."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_227c: dup
            ldi 42
            eq?
            bnt L_22ad
            pushi 8
            lofss "Back onto the set for that. RETURN is always open."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "The audience has seats, not a shortcut."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_22ad: dup
            ldi 43
            eq?
            bnt L_22f2
            pushi 8
            lofss "Frankie Maplewood: Bring the invitation copies to"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "the board. Let us compare the promises before"
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "anyone makes another one."
            pushi 100
            pushi 5
            pushi 32
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_22f2: dup
            ldi 44
            eq?
            bnt L_2323
            pushi 8
            lofss "Frankie wants our promises written down. Her"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "eyebrows can't keep a permanent record."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2323: dup
            ldi 45
            eq?
            bnt L_2340
            pushi 8
            lofss "One job can be put down or handed off."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2340: dup
            ldi 46
            eq?
            bnt L_2371
            pushi 8
            lofss "Bunny and the clean bench are both safe places for"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "the tray."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2371: dup
            ldi 47
            eq?
            bnt L_23b6
            pushi 8
            lofss "Talk to Bunny; Give tray to Bunny; Open door; Walk"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "in. Or Use tray on bench, pick up wedge, Open door,"
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "Use wedge, retrieve tray, enter."
            pushi 100
            pushi 5
            pushi 32
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_23b6: dup
            ldi 48
            eq?
            bnt L_23fb
            pushi 8
            lofss "The invitation comparison is next. Collect all"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "three copies and use them with the living-room"
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "board."
            pushi 100
            pushi 5
            pushi 32
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_23fb: dup
            ldi 49
            eq?
            bnt L_2440
            pushi 8
            lofss "Tab focus; arrows; Enter acts. Esc cancels. Space"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "shows hotspots. H hints; M menu; A audience; Y"
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "music; +/- volume; F2 save; F3 load."
            pushi 100
            pushi 5
            pushi 32
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2440: dup
            ldi 50
            eq?
            bnt L_2485
            pushi 8
            lofss "Audience sound OFF. Captions and audience"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "interaction remain available. Test PCM is"
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "synthetic, not a final human audience recording."
            pushi 100
            pushi 5
            pushi 32
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2485: dup
            ldi 51
            eq?
            bnt L_24ca
            pushi 8
            lofss "Audience sound ON. New reactions use a synthetic"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "test chuff. Consumed reactions are not replayed."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "This is not a final human audience recording."
            pushi 100
            pushi 5
            pushi 32
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_24ca: dup
            ldi 52
            eq?
            bnt L_24e7
            pushi 8
            lofss "Jackie walks over. Nobody is timing him."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_24e7: dup
            ldi 53
            eq?
            bnt L_252c
            pushi 8
            lofss "The household plan starts at the living-room board."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "Later preparations follow after the three aims are"
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "agreed."
            pushi 100
            pushi 5
            pushi 32
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_252c: dup
            ldi 54
            eq?
            bnt L_255c
            pushi 8
            lofss "Give or Use needs a target. Click a person or"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "object to try it with."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_255c: dup
            ldi 55
            eq?
            bnt L_2578
            pushi 8
            lofss "That is on the porch side of the set."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2578: dup
            ldi 56
            eq?
            bnt L_2594
            pushi 8
            lofss "Jackie takes a closer look."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_25c2
            L_2594: dup
            ldi 59
            eq?
            bnt L_25c2
            pushi 8
            lofss "Isolated native checks ran. Results are in the save"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "folder. Player state is unchanged."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            L_25c2: toss
            ret
        )
    )

(method (navNoticeRender owner &tmp savedAcc)
        (asm
            sat 0
            pushi 737
            push0
            lap 1
            send 4
            push
            lat 0
            dup
            ldi 1
            eq?
            bnt L_a186
            pushi 8
            lofss "JACKIE STEPS BEYOND THIS SET'S VISIBLE EDGE. THE"
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            pushi 8
            lofss "SAME ROOM HAS A PERMANENT RETURN."
            pushi 100
            pushi 5
            pushi 22
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_a267
            L_a186: dup
            ldi 2
            eq?
            bnt L_a1a3
            pushi 8
            lofss "JACKIE RETURNS TO THE SAME SET."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_a267
            L_a1a3: dup
            ldi 3
            eq?
            bnt L_a1c0
            pushi 8
            lofss "JACKIE WALKS TO PORCH."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_a267
            L_a1c0: dup
            ldi 4
            eq?
            bnt L_a1dd
            pushi 8
            lofss "JACKIE WALKS TO LIVING ROOM."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_a267
            L_a1dd: dup
            ldi 5
            eq?
            bnt L_a1f9
            pushi 8
            lofss "JACKIE WALKS TO KITCHEN."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_a267
            L_a1f9: dup
            ldi 6
            eq?
            bnt L_a215
            pushi 8
            lofss "JACKIE WALKS TO SIDE PASSAGE."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_a267
            L_a215: dup
            ldi 7
            eq?
            bnt L_a231
            pushi 8
            lofss "JACKIE WALKS TO COURTYARD."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_a267
            L_a231: dup
            ldi 8
            eq?
            bnt L_a24d
            pushi 8
            lofss "JACKIE WALKS TO MILO'S GARAGE LOUNGE."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            jmp L_a267
            L_a24d: dup
            ldi 9
            eq?
            bnt L_a267
            pushi 8
            lofss "JACKIE WALKS TO CONSERVATORY."
            pushi 100
            pushi 5
            pushi 12
            pushi 102
            push1
            pushi 105
            push0
            callk Display, 16
            L_a267: toss
            ret
        )
    )

(method (h6BaseDrawWorld owner &tmp savedAcc)
(if (and (owner p08?) ((owner p08?) h8LayoutRender:)) (return 0))

(if (and (owner p05?) ((owner p05?) hFailure?)) ((owner p05?) hFailureWorld:) (return 0)) (if (and (owner p05?) ((owner p05?) hCourtRender:)) (return 0)) (if (and (owner p05?) ((owner p05?) hRenderWorld:)) (return 0))

        (if (and (== (owner location?) 3) (not (owner onApron?)))
            (owner drawSidePassage:)
            (Display "EDGE" 100 290 135 102 2 105 0 106 32 121) (return 0))
        (asm
            pushi 161
            push0
            lap 1
            send 4
            bnt L_3db5
            pushi 7
            sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 0
            eq?
            bnt L_3d57
            ldi 102
            jmp L_3d59
            L_3d57: ldi 103
            L_3d59: push
            push0
            push0
            push0
            push0
            pushi -1
            push0
            callk DrawCel, 14
            pushi 9
            pushi 11
            pushi 49
            pushi 6
            pushi 81
            pushi 147
            push1
            pushi 8
            push0
            push0
            callk Graph, 18
            pushi 11
            pushi 252
            push0
            lap 1
            send 4
            push
            pushi 100
            pushi 8
            pushi 53
            pushi 102
            push0
            pushi 105
            push0
            pushi 106
            pushi 137
            pushi 121
            callk Display, 22
            pushi 11
            lofss "RETURN"
            pushi 100
            pushi 15
            pushi 121
            pushi 102
            push2
            pushi 105
            push0
            pushi 106
            pushi 70
            pushi 121
            callk Display, 22
            jmp L_3f96
            L_3db5: sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 0
            eq?
            bnt L_3f13
            pushi 7
            pushi 100
            push0
            push0
            push0
            push0
            pushi -1
            push0
            callk DrawCel, 14
            pushi 7
            pushi 210
            push0
            pushi 97
            push0
            lap 1
            send 4
            bnt L_3dd9
            ldi 1
            jmp L_3ddb
            L_3dd9: ldi 0
            L_3ddb: push
            pushi 174
            pushi 49
            pushi -1
            push0
            callk DrawCel, 14
            pushi 368
            push0
            lap 1
            send 4
            bnt L_3e31
            pushi 113
            push0
            lap 1
            send 4
            not
            bnt L_3e31
            pushi 347
            push0
            pushi 368
            push0
            lap 1
            send 4
            send 4
            push
            ldi 1
            eq?
            bnt L_3e31
            pushi 375
            push0
            pushi 368
            push0
            lap 1
            send 4
            send 4
            push
            ldi 2
            eq?
            bnt L_3e31
            pushi 7
            pushi 217
            pushi 88
            push0
            lap 1
            send 4
            bnt L_3e19
            ldi 1
            jmp L_3e1b
            L_3e19: ldi 0
            L_3e1b: push
            pushi 362
            push0
            pushi 368
            push0
            lap 1
            send 4
            send 4
            push
            pushi 75
            pushi 49
            pushi -1
            push0
            callk DrawCel, 14
            jmp L_3e56
            L_3e31: pushi 7
            pushi 113
            push0
            lap 1
            send 4
            bnt L_3e3c
            ldi 215
            jmp L_3e3f
            L_3e3c: ldi 211
            L_3e3f: push
            push0
            pushi 88
            push0
            lap 1
            send 4
            bnt L_3e49
            ldi 1
            jmp L_3e4b
            L_3e49: ldi 0
            L_3e4b: push
            pushi 75
            pushi 49
            pushi -1
            push0
            callk DrawCel, 14
            L_3e56: sat 0
            pushi 265
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 1
            eq?
            bnt L_3e6e
            pushi 7
            pushi 212
            push0
            push0
            pushi 79
            pushi 87
            pushi -1
            push0
            callk DrawCel, 14
            L_3e6e: sat 0
            pushi 341
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 0
            eq?
            bnt L_3e87
            pushi 7
            pushi 213
            push0
            push0
            pushi 132
            pushi 75
            pushi -1
            push0
            callk DrawCel, 14
            L_3e87: sat 0
            pushi 341
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 2
            eq?
            bnt L_3ea0
            pushi 7
            pushi 213
            push0
            push0
            pushi 185
            pushi 107
            pushi -1
            push0
            callk DrawCel, 14
            L_3ea0: pushi 97
            push0
            lap 1
            send 4
            not
            bnt L_3ec0
            pushi 11
            lofss "DOOR"
            pushi 100
            pushi 178
            pushi 116
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 47
            pushi 121
            callk Display, 22
            L_3ec0: pushi 113
            push0
            lap 1
            send 4
            bnt L_3f11
            pushi 11
            lofss "GARAGE"
            pushi 100
            push2
            pushi 49
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 48
            pushi 121
            callk Display, 22
            pushi 11
            lofss "SIDE"
            pushi 100
            push2
            pushi 91
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 30
            pushi 121
            callk Display, 22
            pushi 11
            lofss "CONSERV."
            pushi 100
            pushi 235
            pushi 24
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 48
            pushi 121
            callk Display, 22
            L_3f11: jmp L_3f45
            L_3f13: sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 1
            eq?
            bnt L_3f22
            pushi 344
            push0
            lap 1
            send 4
            jmp L_3f45
            L_3f22: sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 2
            eq?
            bnt L_3f31
            pushi 554
            push0
            lap 1
            send 4
            jmp L_3f45
            L_3f31: sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 6
            eq?
            bnt L_3f40
            pushi 555
            push0
            lap 1
            send 4
            jmp L_3f45
            L_3f40: pushi 98
            push0
            lap 1
            send 4
            L_3f45: pushi 11
            lofss "EDGE"
            pushi 100
            sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 1
            eq?
            bt L_3f61
            sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 2
            eq?
            bt L_3f61
            sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 6
            eq?
            bnt L_3f66
            L_3f61: ldi 286
            jmp L_3f69
            L_3f66: ldi 290
            L_3f69: push
            sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 1
            eq?
            bt L_3f7f
            sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 2
            eq?
            bt L_3f7f
            sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 6
            eq?
            bnt L_3f84
            L_3f7f: ldi 135
            jmp L_3f86
            L_3f84: ldi 123
            L_3f86: push
            pushi 102
            push2
            pushi 105
            push0
            pushi 106
            pushi 32
            pushi 121
            callk Display, 22
            L_3f96: pushi 161
            push0
            lap 1
            send 4
            bt L_3fa8
            sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 1
            ne?
            bnt L_3fad
            sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 6
            ne?
            bnt L_3fad
            L_3fa8: pushi 99
            push0
            lap 1
            send 4
            L_3fad: pushi 161
            push0
            lap 1
            send 4
            not
            bnt L_3fd8
            sat 0
            pushi 124
            push0
            lap 1
            send 4
            push
            lat 0
            ldi 0
            eq?
            bnt L_3fd8
            pushi 97
            push0
            lap 1
            send 4
            bnt L_3fd8
            pushi 11
            lofss "ENTER"
            pushi 100
            pushi 204
            pushi 116
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 31
            pushi 121
            callk Display, 22
            L_3fd8: ret
        )
    )

(method (roomTitle owner)
        (switch (owner location?)
            (0 (return "PORCH")) (1 (return "LIVING ROOM")) (2 (return "KITCHEN"))
            (3 (return "SIDE PASSAGE")) (4 (return "COURTYARD"))
            (5 (return "MILO'S GARAGE LOUNGE")) (6 (return "CONSERVATORY")))
        (return "UNKNOWN ROOM"))

(method (blockPerson owner px py color label)
        ; Explicit original blockout, wall plane adult-height56, feet py.
        (Graph 11 (- py 56) (- px 5) (- py 44) (+ px 5) 1 12 0 0)
        (Graph 11 (- py 43) (- px 8) (- py 21) (+ px 8) 1 color 0 0)
        (Graph 11 (- py 20) (- px 7) py (- px 1) 1 5 0 0)
        (Graph 11 (- py 20) (+ px 1) py (+ px 7) 1 5 0 0)
        (Display label 100 (- px 23) (- py 66) 102 1 105 0 106 66 121))

(method (drawJack owner &tmp t0 t1 t2 savedAcc)
(if (and (owner p06?) ((owner p06?) h6DrawJack:)) (return 1))

        (asm
            pushi 144
            push0
            lap 1
            send 4
            sat 0
            sat 3
            pushi 150
            push0
            lap 1
            send 4
            push
            lat 3
            ldi 64
            div
            push
            pushi 26
            lat 0
            mul
            push
            ldi 128
            div
            sub
            sat 1
            sat 3
            pushi 151
            push0
            lap 1
            send 4
            push
            lat 3
            ldi 64
            div
            push
            pushi 78
            lat 0
            mul
            push
            ldi 128
            div
            sub
            sat 2
            pushi 368
            push0
            lap 1
            send 4
            bnt L_3685
            sat 3
            pushi 140
            push0
            lap 1
            send 4
            push
            lat 3
            ldi 0
            eq?
            bnt L_3685
            pushi 347
            push0
            pushi 368
            push0
            lap 1
            send 4
            send 4
            push
            ldi 1
            eq?
            bnt L_3685
            pushi 375
            push0
            pushi 368
            push0
            lap 1
            send 4
            send 4
            push
            ldi 1
            eq?
            bnt L_3685
            pushi 8
            pushi 216
            sat 3
            pushi 138
            push0
            lap 1
            send 4
            push
            lat 3
            pushi 362
            push0
            pushi 368
            push0
            lap 1
            send 4
            send 4
            push
            lst 1
            lst 2
            pushi -1
            lst 0
            lst 0
            callk DrawCel, 16
            jmp L_369d
            L_3685: pushi 8
            pushi 214
            sat 3
            pushi 138
            push0
            lap 1
            send 4
            push
            lat 3
            sat 3
            pushi 141
            push0
            lap 1
            send 4
            push
            lat 3
            lst 1
            lst 2
            pushi -1
            lst 0
            lst 0
            callk DrawCel, 16
            L_369d: ret
        )
    )

(method (drawLiving owner &tmp feet)
    (DrawCel 101 0 0 0 0 -1 0) (DrawCel 220 0 0 84 50 -1 0)
    (if (& (owner p02BoardRecords?) 1) (DrawCel 220 0 1 88 58 -1 0))
    (if (& (owner p02BoardRecords?) 2) (DrawCel 220 0 1 106 58 -1 0))
    (if (& (owner p02BoardRecords?) 4) (DrawCel 220 0 1 124 58 -1 0))
    (if (== (owner p02CopyBunny?) 1) (DrawCel 220 0 2 73 87 -1 0))
    (if (not (owner p02PlanAgreed?)) (DrawCel 220 0 3 113 80 -1 0))
    (if (== (owner wedge?) 2) (DrawCel 213 0 0 27 110 -1 0))
    (= feet (/ (owner motionY?) 64))
    (if (< feet 126) (owner drawJack:)) (owner livingPerson: 3)
    (if (and (>= feet 126) (< feet 127)) (owner drawJack:)) (owner livingPerson: 2)
    (if (>= feet 127) (owner drawJack:))
    (Display "PORCH" 100 15 116 102 1 105 0 106 42 121)
    (Display "COURT" 100 151 112 102 1 105 0 106 42 121)
    (Display "KITCHEN" 100 273 118 102 1 105 0 106 47 121))

(method (livingPerson owner who &tmp scaleValue mouth)
(if (and (== who 3) (owner p06?) (!= ((owner p06?) h6FrankieRoom?) 1)) (return 0))

(if (and (owner p05?) (== who 2) (!= ((owner p05?) hBunnyRoom?) 1)) (return 0))

    (= mouth 0)
    (if (and (owner presentation?) (== ((owner presentation?) lane?) 1) (== ((owner presentation?) speaker?) who)) (= mouth ((owner presentation?) mouth?)))
    (if (== who 3) (DrawCel 218 1 mouth 121 60 -1 108 108)
    else (DrawCel 219 1 mouth 218 61 -1 109 109)))

(method (neighborPerson owner who &tmp mouth)
    (= mouth 0)
    (if (and (owner presentation?) (== ((owner presentation?) lane?) 1) (== ((owner presentation?) speaker?) who)) (= mouth ((owner presentation?) mouth?)))
    (if (== who 4) (DrawCel 222 1 mouth 149 61 -1 108 108)
    else (DrawCel 221 1 mouth 108 60 -1 108 108)))

(method (drawKitchen owner)
    ; Frozen source104 is packaged as300; credits104..112 retain their identity.
    (DrawCel 300 0 0 0 0 -1 0)
(if (owner p07?) ((owner p07?) h7Render:))
    (if (== ((owner p03?) p03Towel?) 0) (DrawCel 224 0 5 144 85 -1 0))
    (if (== ((owner p03?) p03Napkin?) 0) (DrawCel 224 0 6 158 86 -1 0))
    (if (== (owner tray?) 2) (DrawCel 212 0 0 184 85 -1 0))
    (if ((owner p03?) p03Ready?)
        (if (or (not (owner p08?)) (not ((owner p08?) h8Owns: 1))) (DrawCel 224 0 1 215 55 -1 0))
        (if (or (not (owner p08?)) (not ((owner p08?) h8Owns: 5))) (DrawCel 224 0 4 261 64 -1 0)))
    (Display "LIVING ROOM" 100 12 112 102 1 105 0 106 66 121)
(if (owner p07?) ((owner p07?) h7DrawBunny:))

(if (owner p08?) ((owner p08?) h8RenderCloth:))
)

(method (drawP03Conservatory owner &tmp t0 savedAcc)
        (asm
            pushi 7
            pushi 302
            push0
            push0
            push0
            push0
            pushi -1
            push0
            callk DrawCel, 14
            pushi 3159
            push0
            lap 1
            send 4
            bnt L_p09_geometry_tags_done
            pushi 3166
            push1
            push1
            send 6
            L_p09_geometry_tags_done: pushi 7
            pushi 224
            push0
            pushi 8
            pushi 63
            pushi 46
            pushi -1
            push0
            callk DrawCel, 14
            pushi 7
            pushi 224
            push0
            pushi 10
            pushi 282
            pushi 58
            pushi -1
            push0
            callk DrawCel, 14
            sat 1
            pushi 184
            push0
            lap 1
            send 4
            push
            lat 1
            ldi 6
            eq?
            bnt L_98cd
            pushi 7
            pushi 220
            push0
            push1
            pushi 221
            pushi 68
            pushi -1
            push0
            callk DrawCel, 14
            L_98cd: pushi 644
            push0
            pushi 572
            push0
            lap 1
            send 4
            send 4
            not
            bnt L_9945
            pushi 7
            pushi 224
            push0
            pushi 7
            pushi 65
            pushi 61
            pushi -1
            push0
            callk DrawCel, 14
            pushi 7
            pushi 224
            push0
            pushi 638
            push0
            pushi 572
            push0
            lap 1
            send 4
            send 4
            bnt L_98fe
            ldi 1
            jmp L_9900
            L_98fe: ldi 0
            L_9900: push
            pushi 87
            pushi 55
            pushi -1
            push0
            callk DrawCel, 14
            pushi 7
            pushi 224
            push0
            push2
            pushi 654
            push0
            pushi 572
            push0
            lap 1
            send 4
            send 4
            push
            ldi 1
            eq?
            bnt L_9924
            ldi 2
            jmp L_9938
            L_9924: pushi 654
            push0
            pushi 572
            push0
            lap 1
            send 4
            send 4
            push
            ldi 2
            eq?
            bnt L_9936
            ldi 1
            jmp L_9938
            L_9936: ldi 0
            L_9938: add
            push
            pushi 129
            pushi 63
            pushi -1
            push0
            callk DrawCel, 14
            L_9945: sat 1
            pushi 151
            push0
            lap 1
            send 4
            push
            lat 1
            ldi 64
            div
            sat 0
            lst 0
            ldi 126
            lt?
            bnt L_9959
            pushi 99
            push0
            lap 1
            send 4
            L_9959: pushi 422
            push1
            pushi 4
            lap 1
            send 6
            lst 0
            ldi 126
            ge?
            bnt L_9975
            lst 0
            ldi 130
            lt?
            bnt L_9975
            pushi 99
            push0
            lap 1
            send 4
            L_9975: pushi 650
            push0
            lap 1
            send 4
            lst 0
            ldi 130
            ge?
            bnt L_9988
            pushi 99
            push0
            lap 1
            send 4
            L_9988: pushi 11
            lofss "PORCH"
            pushi 100
            pushi 10
            pushi 113
            pushi 102
            push1
            pushi 105
            push0
            pushi 106
            pushi 38
            pushi 121
            callk Display, 22
            ret
        )
    )

(method (p03Rita owner &tmp t0 t1 t2 t3 savedAcc)
        (asm
            ldi 0
            sat 0
            ldi 252
            sat 2
            ldi 130
            sat 3
            lst 3
            ldi 50
            sub
            push
            ldi 128
            mul
            push
            ldi 45
            add
            push
            ldi 90
            div
            sat 1
            pushi 368
            push0
            lap 1
            send 4
            bnt L_99f1
            pushi 347
            push0
            pushi 368
            push0
            lap 1
            send 4
            send 4
            push
            ldi 1
            eq?
            bnt L_99f1
            pushi 375
            push0
            pushi 368
            push0
            lap 1
            send 4
            send 4
            push
            ldi 7
            eq?
            bnt L_99f1
            pushi 362
            push0
            pushi 368
            push0
            lap 1
            send 4
            send 4
            sat 0
            L_99f1: pushi 8
            pushi 223
            push1
            lst 0
            lst 2
            pushi 26
            lat 1
            mul
            push
            ldi 128
            div
            sub
            push
            lst 3
            pushi 78
            lat 1
            mul
            push
            ldi 128
            div
            sub
            push
            pushi -1
            lst 1
            lst 1
            callk DrawCel, 16
            ret
        )
    )

(method (drawSidePassage owner &tmp feet)
    (DrawCel 303 0 0 0 0 -1 0)
    (DrawCel 226 0 2 183 65 -1 0)
    (DrawCel 226 0 (if (== ((owner p04?) p04Gate?) 1) 1 else 0) 194 49 -1 0)
    (DrawCel 226 0 (if ((owner p04?) p04Peg?) 7 else 6) 198 96 -1 0)
    (if (== ((owner p04?) p04Bunting?) 0)
        (if (== ((owner p04?) p04Gate?) 1)
            (DrawCel 226 0 3 197 82 -1 0)
        else (DrawCel 226 0 3 258 69 -1 0))
    else (if (== ((owner p04?) p04Bunting?) 2)
        (DrawCel 226 0 5 178 73 -1 0)))
    ; Original P01 wedge213; no duplicate wedge and no held-bunting fixture.
    (if ((owner p04?) p04Wedge?) (DrawCel 213 0 0 195 119 -1 0))
    ; This method owns both actor draws. Suppress trailing drawJack in room3.
    (= feet (/ (owner motionY?) 64))
    (if (< feet 131) (owner drawJack:))
    (owner p04Felix:)
    (if (>= feet 131) (owner drawJack:)))

(method (p04Felix owner &tmp mouth facing scaleValue px py)
    (if (or (owner onApron?) (!= (owner location?) 3)) (return 0))
    (= mouth 0) (= px 156) (= py 131) (= scaleValue 116)
    (= facing (if (< (/ (owner motionX?) 64) px) 1 else 0))
    ; Canonical speaker_numbers assigns Felix8. Default closed mouth covers
    ; idle, interruption, movement and non-Felix presentation states.
    (if (and (owner presentation?) (== (owner motionPhase?) 0) (== ((owner presentation?) lane?) 1)
        (== ((owner presentation?) speaker?) 8))
        (= mouth ((owner presentation?) mouth?)))
    (if (or (< mouth 0) (> mouth 2)) (= mouth 0))
    (DrawCel 225 facing mouth (- px (/ (* 26 scaleValue) 128))
        (- py (/ (* 78 scaleValue) 128)) -1 scaleValue scaleValue))
)
(instance sceneRenderer of SceneRenderer)
