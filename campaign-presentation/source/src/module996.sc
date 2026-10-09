;;; Sierra Script 1.0 - (do not remove this comment)
; Original isolated P14 domain adapter. Canonical IDs only.
(define H14_CREDIT_MASK0 32767)
(define H14_CREDIT_MASK1 32255)
(define H14_CREDIT_MASK2 7)
(define H14_HOST_BUNNY 2)
(define H14_HOST_FRANKIE 8)
(define H14_HOST_MILO 28)
(define H14_HOST_VIVIAN 85)
(define H14_HOST_RITA 30)
(define H14_HOST_FELIX 54)
(define H14_HOST_STRINGER 29)
(script# 996)
(public p14State 0)
(local [p14Lines 3] [p14Units 8] [p14Events 1] [p14EventArgs 4] [p14EventHi 1] [p14EventLo 1] [p14Held 443] [p14Lease 88] [p14OrderedSources 87] [p14OrderedHi 87] [p14OrderedLo 87] [p14InputDate 160] [p14FirstWinHi 4] [p14FirstWinLo 4] [p14LastWinHi 4] [p14LastWinLo 4] [p14MatchingWin 4] [p14ValidationHi 202] [p14ValidationLo 202] [p14ValidationOwners 202]
[h14Owner 8] [h14Facts 31] [h14Date 81] [h14Edit 5] [h14EditChars 80] [h14EditText 43] [h14Reader 24] [h14Selected 1] [h14Freeze 4] [h14MenuPaint 8]

[h14Reaction 8]
)
(define OBJ_FRONT_DOOR 1)
(define OBJ_BUNNY 2)
(define OBJ_BENCH 3)
(define OBJ_WEDGE 4)
(define OBJ_TRAY 5)
(define OBJ_PRINT_PACKET 6)
(define OBJ_BOARD 7)
(define OBJ_FRANKIE 8)
(define OBJ_AUDIENCE_EDGE 9)
(define OBJ_AUDIENCE 10)
(define OBJ_RETURN_TO_HOUSE 11)
(define OBJ_EXIT_KITCHEN 12)
(define OBJ_EXIT_COURTYARD 13)
(define OBJ_EXIT_SIDE 14)
(define OBJ_EXIT_GARAGE 15)
(define OBJ_EXIT_CONSERVATORY 16)
(define OBJ_EXIT_PORCH 17)
(define OBJ_EXIT_LIVING 18)
(define OBJ_EXIT_GATE 19)
(define OBJ_COPY_JACK 20)
(define OBJ_COPY_BUNNY 21)
(define OBJ_COPY_STRINGER 22)
(define OBJ_COMPARED_COPIES 23)
(define OBJ_MASTER_INVITATION 24)
(define OBJ_GREASE_PENCIL 25)
(define OBJ_MATCHED_BORDER 26)
(define OBJ_INVITATION_DRAWER 27)
(define OBJ_MILO 28)
(define OBJ_STRINGER 29)
(define OBJ_RITA 30)
(define OBJ_CHECKLIST 31)
(define OBJ_JOURNAL 32)
(define OBJ_CARRIER_DRAWING 33)
(define OBJ_CERAMIC_CARRIER 34)
(define OBJ_CERAMIC_SAMPLE_TILES 35)
(define OBJ_CERAMIC_SERVICE 36)
(define OBJ_CLASS_CARD 37)
(define OBJ_CLEAN_NAPKIN 38)
(define OBJ_CLEAN_TOWEL 39)
(define OBJ_CREDIT_SLATE 40)
(define OBJ_DISPLAY_MARKINGS 41)
(define OBJ_FOLDED_DISPLAY 42)
(define OBJ_KITCHEN_PASS 43)
(define OBJ_LINEN_DRAWER 44)
(define OBJ_LINEN_HOOK 45)
(define OBJ_NEWSPAPER 46)
(define OBJ_PLATE_SIGNATURE 47)
(define OBJ_RITA_SAMPLE_TILE_1 48)
(define OBJ_RITA_SAMPLE_TILE_2 49)
(define OBJ_RITA_SAMPLE_TILE_3 50)
(define OBJ_ALIGNED_HINGES 51)
(define OBJ_CIRCULATION_BOARD 52)
(define OBJ_CIRCULATION_PLAN 53)
(define OBJ_FELIX 54)
(define OBJ_FIXED_HOOK 55)
(define OBJ_HOLD_OPEN_PEG 56)
(define OBJ_JACK 57)
(define OBJ_LATCH_ARM 58)
(define OBJ_SCREWDRIVER 59)
(define OBJ_SIDE_GATE 60)
(define OBJ_VIVIAN 61)
(define OBJ_WELCOME_BUNTING 62)
(define OBJ_PA_KIT 63)
(define OBJ_INPUT_SELECTOR 64)
(define OBJ_MICROPHONE 65)
(define OBJ_MIC_SOCKET 66)
(define OBJ_LOUDSPEAKER 67)
(define OBJ_SPEAKER_SWIVEL_HANDLE 68)
(define OBJ_MARKED_LISTENING_POSITION 69)
(define OBJ_SLOGAN_TAPE 70)
(define OBJ_EQUIPMENT_CREDIT_SLATE 71)
(define OBJ_HANDCART 72)
(define OBJ_GATE_LANE 116)
(define OBJ_BUFFET_POSITION 117)
(define OBJ_SPEAKER_POSITION 118)
(define OBJ_DISPLAY_ALCOVE 119)
(define OBJ_SERVING_TABLE 120)
(define OBJ_KITCHEN_HATCH 121)
(define OBJ_PLAN_OVERLAY 122)
(define OBJ_PLACEMENT_SYMBOLS 123)
(define OBJ_TAGGED_CHAIRS 395)
(define OBJ_CHAIR_TAG 396)
(define OBJ_CONSERVATORY_FRONT 397)
(define OBJ_CONSERVATORY_SIDE 398)
(define OBJ_RENEWAL_REPAIR_CARD 399)
(define OBJ_SCREEN_FRAME 73)
(define OBJ_UPPER_RAIL 74)
(define OBJ_CLEAN_SHEET 75)
(define OBJ_LAUNDRY_CLIPS 76)
(define OBJ_SAMPLE_LAYOUT 77)
(define OBJ_VISITOR_FIGURE 78)
(define OBJ_DISPLAY_FIGURE 79)
(define OBJ_SCREEN_TOKEN 80)
(define OBJ_COMPLETED_SCREEN 81)
(define OBJ_ASSEMBLY_DRAWING 82)
(define OBJ_COURTYARD_PLAN 83)
(define OBJ_CLIP_MARKS 84)
(define OBJ_HOTPOT_RECIPE 86)
(define OBJ_BEAN_TOMATO_BASE 87)
(define OBJ_VEGETABLE_BOWL 88)
(define OBJ_STOCK_BOTTLE 89)
(define OBJ_MEASURING_JUG 90)
(define OBJ_HERB_SACHET 91)
(define OBJ_HOTPOT_POT 92)
(define OBJ_POT_LID 93)
(define OBJ_STOVE 94)
(define OBJ_CUE_RACK 410)
(define OBJ_RACK_SPRING_CLIPS 411)
(define OBJ_MASTER_INVITATION_CUE_1 412)
(define OBJ_MASTER_INVITATION_CUE_2 413)
(define OBJ_MASTER_INVITATION_CUE_3 414)
(define OBJ_DISPLAY_WING 415)
(define OBJ_WING_CATCH 416)
(define OBJ_DISPLAY_HANDLE 417)
(define OBJ_STAGING_POCKET 418)
(define OBJ_GUEST_PROGRAM_CARD 432)
(define OBJ_PLEDGE_BOARD 433)
(define OBJ_SCREEN_PULL_TAB 434)
(define OBJ_PLEDGE_CARD_JACK 435)
(define OBJ_PLEDGE_CARD_BUNNY 436)
(define OBJ_PLEDGE_CARD_FRANKIE 437)
(define OBJ_PLEDGE_CARD_MILO 438)
(define OBJ_PLEDGE_CARD_VIVIAN 439)
(define OBJ_PLEDGE_CARD_RITA 440)
(define OBJ_PLEDGE_CARD_FELIX 441)
(define OBJ_PLEDGE_CARD_STRINGER 442)
(define CODE_CANONICAL_TASKS_INCOMPLETE 1)
(define CODE_ALL_FOUR_ACTUAL_WINS_REQUIRED 2)
(define CODE_BOARD_NOT_PHYSICALLY_DELIVERED 3)
(define CODE_COMMITMENTS_ALREADY_STARTED 4)
(define CODE_ORIGINAL_TERMS_CARD_REQUIRED 5)
(define CODE_AGREED_FICTIONAL_DATE_REQUIRED 6)
(define CODE_COMMITMENTS_STARTED 7)
(define CODE_COMMITMENTS_NOT_STARTED 8)
(define CODE_COMMITMENTS_ALREADY_COMPLETE 9)
(define CODE_FINALE_NOT_STARTED 10)
(define CODE_FINALE_PAUSED 11)
(define CODE_NOT_CURRENT_FINALE_SCENE 12)
(define CODE_PROMISE_ALREADY_PINNED 13)
(define CODE_ALL_EIGHT_APPROVED_AND_PINNED_REQUIRED 14)
(define CODE_PENCIL_HANDOFF_REQUIRED 15)
(define CODE_DATE_TEXT_REQUIRED 16)
(define CODE_COMPLETE_READBACK_REQUIRED 17)
(define CODE_RECIPIENT_ABSENT 18)
(define CODE_UNRELATED_PROMISE_RETURNED 19)
(define CODE_CARD_ALREADY_PINNED 20)
(define CODE_APPROVAL_REQUIRED 21)
(define CODE_APPROVED_CARD_PINNED 22)
(define CODE_ALREADY_SIGNED 23)
(define CODE_SIGNATURE_REFUSED 24)
(define CODE_WHOLE_CONSENT_SCENE_REQUIRED 25)
(define CODE_TERMS_SIGNED_AND_PINNED 26)
(define CODE_PENCIL_ALREADY_HANDED_OVER 27)
(define CODE_SIGNED_TERMS_REQUIRED 28)
(define CODE_ORIGINAL_PENCIL_REQUIRED 29)
(define CODE_FRANKIE_ABSENT 30)
(define CODE_PENCIL_HANDED_OVER 31)
(define CODE_COMPLETE_DATED_READBACK_AND_RETURN_REQUIRED 32)
(define CODE_GAME_COMPLETE 33)
(define CODE_LEGITIMATE_COMPLETION_REQUIRED 34)
(define CODE_FINALE_ALREADY_STARTED 35)
(define CODE_FINALE_STARTED 36)
(define CODE_FREEZE_FRAME_PENDING 37)
(define CODE_FINALE_INACTIVE 38)
(define CODE_WHOLE_FINALE_RECORD_REQUIRED 39)
(define CODE_VISIBLE_FREEZE_REQUIRED 40)
(define CODE_FINALE_ADVANCED 41)
(define CODE_STALE_FREEZE 42)
(define CODE_FREEZE_PRESENTED 43)
(define CODE_LAUGH_CONSUMED 44)
(define CODE_TAG_LAUGH_UNAVAILABLE 45)
(define CODE_CELEBRATION_CONSUMED 46)
(define CODE_CELEBRATION_UNAVAILABLE 47)
(define CODE_PAUSE_UNCHANGED 48)
(define CODE_FINALE_SKIPPED 49)
(define CODE_UNHANDLED_ACTION 50)
(define CODE_OFFSCREEN 51)
(define CODE_CONTEST_ACTIVE 52)
(define CODE_SPEAKER_ABSENT 53)
(define CODE_PRESENTATION_NOT_STARTED 54)
(define CODE_PRESENTATION_COMPLETE 55)
(define CODE_PRESENTATION_PENDING 56)
(define CODE_PRESENTATION_ALREADY_ACKNOWLEDGED 57)
(define CODE_PRESENTATION_ACKNOWLEDGED 58)
(define CODE_STALE_PRESENTATION 59)
(define CODE_PRESENTATION_CANCELLED 60)
(define CODE_AUDIO_HAS_NO_AUTHORITY 61)
(define CODE_HINT 62)
(define CODE_FINALE_RESUMED 63)
(define CODE_INVALID_ARGUMENT 64)
(define CODE_INVALID_CONTEXT 65)
(define CODE_INVALID_STATE 66)
(define CODE_SERIAL_EXHAUSTED 67)
(define CODE_REPLAY_PREPARED 68)
(define CODE_NO_PENDING_FINALE_TEXT 69)
(define EVENT_P14_PRESENTATION_QUEUED 1)
(define EVENT_P14_PRESENTED 2)
(define EVENT_P14_COMMITMENT_START 3)
(define EVENT_P14_CARD_PINNED 4)
(define EVENT_P14_TERMS_SIGNED 5)
(define EVENT_P14_PENCIL_HANDOFF 6)
(define EVENT_P14_GAME_COMPLETE 7)
(define EVENT_P14_FINALE_BEGIN 8)
(define EVENT_P14_FINALE_SCENE 9)
(define EVENT_P14_FREEZE_PRESENTED 10)
(define EVENT_LAF14 11)
(define EVENT_P14_CELEBRATION 12)
(define EVENT_P14_FINALE_PAUSE 13)
(define EVENT_P14_FINALE_SKIP 14)
(define SOURCE_OPENING 1)
(define SOURCE_APPROVE_JACK 2)
(define SOURCE_APPROVE_BUNNY 3)
(define SOURCE_APPROVE_FRANKIE 4)
(define SOURCE_APPROVE_MILO 5)
(define SOURCE_APPROVE_VIVIAN 6)
(define SOURCE_APPROVE_RITA 7)
(define SOURCE_APPROVE_FELIX 8)
(define SOURCE_APPROVE_STRINGER 9)
(define SOURCE_CARD_JACK 10)
(define SOURCE_CARD_BUNNY 11)
(define SOURCE_CARD_FRANKIE 12)
(define SOURCE_CARD_MILO 13)
(define SOURCE_CARD_VIVIAN 14)
(define SOURCE_CARD_RITA 15)
(define SOURCE_CARD_FELIX 16)
(define SOURCE_CARD_STRINGER 17)
(define SOURCE_WARM_TOAST 18)
(define SOURCE_DRY_TOAST 19)
(define SOURCE_SIGNATURE 20)
(define SOURCE_DATE 21)
(define SOURCE_READBACK 22)
(define SOURCE_RETURN_PENCIL 23)
(define SOURCE_CLOSING_PROFESSIONAL 24)
(define SOURCE_CLOSING_FRIENDLY 25)
(define SOURCE_CLOSING_CAUTIOUSLY_ROMANTIC 26)
(define SOURCE_MEAL 27)
(define SOURCE_TAG 28)
(define SOURCE_CREDIT_END_CREDIT_TITLE 29)
(define SOURCE_CREDIT_END_CREDIT_FICTIONAL_STUDIO 30)
(define SOURCE_CREDIT_END_CREDIT_REAL_CREATION 31)
(define SOURCE_CREDIT_END_CREDIT_CAST 32)
(define SOURCE_CREDIT_END_CREDIT_WRITERS_HEADER 33)
(define SOURCE_CREDIT_END_CREDIT_WRITERS_HEAD 34)
(define SOURCE_CREDIT_END_CREDIT_WRITERS_ASSISTANT 35)
(define SOURCE_CREDIT_END_CREDIT_WRITERS_CLUB 36)
(define SOURCE_CREDIT_END_CREDIT_WRITERS_SOCIAL 37)
(define SOURCE_CREDIT_END_CREDIT_WRITERS_META 38)
(define SOURCE_CREDIT_END_CREDIT_WRITERS_ENSEMBLE 39)
(define SOURCE_CREDIT_END_CREDIT_WRITERS_ADVENTURE 40)
(define SOURCE_CREDIT_END_CREDIT_WRITERS_OUTSIDER 41)
(define SOURCE_CREDIT_END_CREDIT_REAL_PRODUCTION 42)
(define SOURCE_CREDIT_END_CREDIT_FICTIONAL_PRODUCERS 43)
(define SOURCE_CREDIT_END_CREDIT_FICTIONAL_FLOOR 44)
(define SOURCE_CREDIT_END_CREDIT_FICTIONAL_CAMERA 45)
(define SOURCE_CREDIT_END_CREDIT_FICTIONAL_SOUND 46)
(define SOURCE_CREDIT_END_CREDIT_FICTIONAL_ART 47)
(define SOURCE_CREDIT_END_CREDIT_FICTIONAL_WARDROBE 48)
(define SOURCE_CREDIT_END_CREDIT_FICTIONAL_POST 49)
(define SOURCE_CREDIT_END_CREDIT_FICTIONAL_PRODUCTION 50)
(define SOURCE_CREDIT_END_CREDIT_FICTIONAL_MUSIC 51)
(define SOURCE_CREDIT_END_CREDIT_FICTIONAL_AUDIENCE 52)
(define SOURCE_CREDIT_END_CREDIT_REAL_ASSISTANCE 53)
(define SOURCE_CREDIT_END_CREDIT_THANKS 54)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_01 55)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_02 56)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_03 57)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_04 58)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_05 59)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_06 60)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_07 61)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_08 62)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_09 63)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_10 64)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_11 65)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_12 66)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_13 67)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_14 68)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_15 69)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_16 70)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_17 71)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_18 72)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_19 73)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_20 74)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_21 75)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_22 76)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_23 77)
(define SOURCE_CREDIT_END_ASSET_AUDIENCE_24 78)
(define SOURCE_CREDIT_END_ASSET_FOLEY_01 79)
(define SOURCE_CREDIT_END_ASSET_FOLEY_02 80)
(define SOURCE_CREDIT_END_ASSET_FOLEY_03 81)
(define SOURCE_CREDIT_END_ASSET_FOLEY_04 82)
(define SOURCE_CREDIT_END_ASSET_FOLEY_05 83)
(define SOURCE_CREDIT_END_ASSET_FOLEY_06 84)
(define SOURCE_CREDIT_END_ASSET_FOLEY_07 85)
(define SOURCE_CREDIT_END_ASSET_FOLEY_08 86)
(define SOURCE_CREDIT_END_ASSET_FOLEY_09 87)
(define LINE_P14_OPEN_001 1)
(define LINE_P14_CARD_JACK 2)
(define LINE_P14_LABEL_JACK 3)
(define LINE_P14_APPROVE_JACK 4)
(define LINE_P14_WRONG_JACK 5)
(define LINE_P14_CARD_BUNNY 6)
(define LINE_P14_LABEL_BUNNY 7)
(define LINE_P14_APPROVE_BUNNY 8)
(define LINE_P14_WRONG_BUNNY 9)
(define LINE_P14_CARD_FRANKIE 10)
(define LINE_P14_LABEL_FRANKIE 11)
(define LINE_P14_APPROVE_FRANKIE 12)
(define LINE_P14_WRONG_FRANKIE 13)
(define LINE_P14_CARD_MILO 14)
(define LINE_P14_LABEL_MILO 15)
(define LINE_P14_APPROVE_MILO 16)
(define LINE_P14_WRONG_MILO 17)
(define LINE_P14_CARD_VIVIAN 18)
(define LINE_P14_LABEL_VIVIAN 19)
(define LINE_P14_APPROVE_VIVIAN 20)
(define LINE_P14_WRONG_VIVIAN 21)
(define LINE_P14_CARD_RITA 22)
(define LINE_P14_LABEL_RITA 23)
(define LINE_P14_APPROVE_RITA 24)
(define LINE_P14_WRONG_RITA 25)
(define LINE_P14_CARD_FELIX 26)
(define LINE_P14_LABEL_FELIX 27)
(define LINE_P14_APPROVE_FELIX 28)
(define LINE_P14_WRONG_FELIX 29)
(define LINE_P14_CARD_STRINGER 30)
(define LINE_P14_LABEL_STRINGER 31)
(define LINE_P14_APPROVE_STRINGER 32)
(define LINE_P14_WRONG_STRINGER 33)
(define LINE_P14_SUCCESS_001 34)
(define LINE_P14_FAILURE_001 35)
(define LINE_P14_CHOICE_001 36)
(define LINE_P14_DIALOGUE_001 37)
(define LINE_P14_CHOICE_002 38)
(define LINE_P14_DIALOGUE_002 39)
(define LINE_P14_CHOICE_003 40)
(define LINE_P14_DIALOGUE_003 41)
(define LINE_P14_FAILURE_002 42)
(define LINE_P14_SUCCESS_002 43)
(define LINE_P14_SUCCESS_003 44)
(define LINE_P14_READ_001 45)
(define LINE_P14_SUCCESS_004 46)
(define LINE_P14_DIALOGUE_004 47)
(define LINE_P14_DIALOGUE_005 48)
(define LINE_P14_DIALOGUE_006 49)
(define LINE_P14_ENDING_001 50)
(define LINE_P14_ENDING_002 51)
(define LINE_P14_READ_002 52)
(define LINE_P14_SYSTEM_001 53)
(define LINE_P14_HINT_1 54)
(define LINE_P14_HINT_2 55)
(define LINE_P14_HINT_3 56)
(define LINE_VC_NOTEBOOK_WINS 57)
(define LINE_VC_GATE_MISSING_WINS 58)
(define LINE_VC_GATE_ALL_WON 59)
(define LINE_END_CREDIT_TITLE 60)
(define LINE_END_CREDIT_FICTIONAL_STUDIO 61)
(define LINE_END_CREDIT_REAL_CREATION 62)
(define LINE_END_CREDIT_CAST 63)
(define LINE_END_CREDIT_WRITERS_HEADER 64)
(define LINE_END_CREDIT_WRITERS_HEAD 65)
(define LINE_END_CREDIT_WRITERS_ASSISTANT 66)
(define LINE_END_CREDIT_WRITERS_CLUB 67)
(define LINE_END_CREDIT_WRITERS_SOCIAL 68)
(define LINE_END_CREDIT_WRITERS_META 69)
(define LINE_END_CREDIT_WRITERS_ENSEMBLE 70)
(define LINE_END_CREDIT_WRITERS_ADVENTURE 71)
(define LINE_END_CREDIT_WRITERS_OUTSIDER 72)
(define LINE_END_CREDIT_REAL_PRODUCTION 73)
(define LINE_END_CREDIT_FICTIONAL_PRODUCERS 74)
(define LINE_END_CREDIT_FICTIONAL_FLOOR 75)
(define LINE_END_CREDIT_FICTIONAL_CAMERA 76)
(define LINE_END_CREDIT_FICTIONAL_SOUND 77)
(define LINE_END_CREDIT_FICTIONAL_ART 78)
(define LINE_END_CREDIT_FICTIONAL_WARDROBE 79)
(define LINE_END_CREDIT_FICTIONAL_POST 80)
(define LINE_END_CREDIT_FICTIONAL_PRODUCTION 81)
(define LINE_END_CREDIT_FICTIONAL_MUSIC 82)
(define LINE_END_CREDIT_FICTIONAL_AUDIENCE 83)
(define LINE_END_CREDIT_REAL_ASSISTANCE 84)
(define LINE_END_CREDIT_THANKS 85)
(define LINE_END_FREEZE 86)
(define LINE_END_UI_PAUSE 87)
(define LINE_END_UI_CONTINUE 88)
(define LINE_END_UI_SKIP 89)
(define LINE_END_UI_REPLAY 90)
(define LINE_END_UI_ACKNOWLEDGMENTS 91)
(define LINE_END_UI_RETURN 92)
(define LINE_END_ASSET_AUDIENCE_01 93)
(define LINE_END_ASSET_AUDIENCE_02 94)
(define LINE_END_ASSET_AUDIENCE_03 95)
(define LINE_END_ASSET_AUDIENCE_04 96)
(define LINE_END_ASSET_AUDIENCE_05 97)
(define LINE_END_ASSET_AUDIENCE_06 98)
(define LINE_END_ASSET_AUDIENCE_07 99)
(define LINE_END_ASSET_AUDIENCE_08 100)
(define LINE_END_ASSET_AUDIENCE_09 101)
(define LINE_END_ASSET_AUDIENCE_10 102)
(define LINE_END_ASSET_AUDIENCE_11 103)
(define LINE_END_ASSET_AUDIENCE_12 104)
(define LINE_END_ASSET_AUDIENCE_13 105)
(define LINE_END_ASSET_AUDIENCE_14 106)
(define LINE_END_ASSET_AUDIENCE_15 107)
(define LINE_END_ASSET_AUDIENCE_16 108)
(define LINE_END_ASSET_AUDIENCE_17 109)
(define LINE_END_ASSET_AUDIENCE_18 110)
(define LINE_END_ASSET_AUDIENCE_19 111)
(define LINE_END_ASSET_AUDIENCE_20 112)
(define LINE_END_ASSET_AUDIENCE_21 113)
(define LINE_END_ASSET_AUDIENCE_22 114)
(define LINE_END_ASSET_AUDIENCE_23 115)
(define LINE_END_ASSET_AUDIENCE_24 116)
(define LINE_END_ASSET_FOLEY_01 117)
(define LINE_END_ASSET_FOLEY_02 118)
(define LINE_END_ASSET_FOLEY_03 119)
(define LINE_END_ASSET_FOLEY_04 120)
(define LINE_END_ASSET_FOLEY_05 121)
(define LINE_END_ASSET_FOLEY_06 122)
(define LINE_END_ASSET_FOLEY_07 123)
(define LINE_END_ASSET_FOLEY_08 124)
(define LINE_END_ASSET_FOLEY_09 125)
(define UNIT_P14_OPEN_001_01 1)
(define UNIT_P14_OPEN_001_02 2)
(define UNIT_P14_OPEN_001_03 3)
(define UNIT_P14_APPROVE_JACK_01 4)
(define UNIT_P14_WRONG_JACK_01 5)
(define UNIT_P14_APPROVE_BUNNY_01 6)
(define UNIT_P14_WRONG_BUNNY_01 7)
(define UNIT_P14_APPROVE_FRANKIE_01 8)
(define UNIT_P14_WRONG_FRANKIE_01 9)
(define UNIT_P14_APPROVE_MILO_01 10)
(define UNIT_P14_WRONG_MILO_01 11)
(define UNIT_P14_APPROVE_VIVIAN_01 12)
(define UNIT_P14_WRONG_VIVIAN_01 13)
(define UNIT_P14_APPROVE_RITA_01 14)
(define UNIT_P14_WRONG_RITA_01 15)
(define UNIT_P14_APPROVE_FELIX_01 16)
(define UNIT_P14_WRONG_FELIX_01 17)
(define UNIT_P14_APPROVE_STRINGER_01 18)
(define UNIT_P14_WRONG_STRINGER_01 19)
(define UNIT_P14_SUCCESS_001_01 20)
(define UNIT_P14_FAILURE_001_01 21)
(define UNIT_P14_DIALOGUE_001_01 22)
(define UNIT_P14_DIALOGUE_002_01 23)
(define UNIT_P14_DIALOGUE_003_01 24)
(define UNIT_P14_DIALOGUE_003_02 25)
(define UNIT_P14_DIALOGUE_003_03 26)
(define UNIT_P14_DIALOGUE_003_04 27)
(define UNIT_P14_DIALOGUE_003_05 28)
(define UNIT_P14_FAILURE_002_01 29)
(define UNIT_P14_SUCCESS_002_01 30)
(define UNIT_P14_SUCCESS_003_01 31)
(define UNIT_P14_READ_001_01 32)
(define UNIT_P14_SUCCESS_004_01 33)
(define UNIT_P14_DIALOGUE_004_01 34)
(define UNIT_P14_DIALOGUE_005_01 35)
(define UNIT_P14_DIALOGUE_006_01 36)
(define UNIT_P14_ENDING_001_01 37)
(define UNIT_P14_ENDING_001_02 38)
(define UNIT_P14_ENDING_001_03 39)
(define UNIT_P14_ENDING_001_04 40)
(define UNIT_P14_ENDING_001_05 41)
(define UNIT_P14_ENDING_002_01 42)
(define UNIT_P14_ENDING_002_02 43)
(define TOKEN_P14_OPEN_001_01 1)
(define TOKEN_P14_OPEN_001_02 2)
(define TOKEN_P14_OPEN_001_03 3)
(define TOKEN_P14_APPROVE_JACK_01 4)
(define TOKEN_P14_APPROVE_BUNNY_01 5)
(define TOKEN_P14_APPROVE_FRANKIE_01 6)
(define TOKEN_P14_APPROVE_MILO_01 7)
(define TOKEN_P14_APPROVE_VIVIAN_01 8)
(define TOKEN_P14_APPROVE_RITA_01 9)
(define TOKEN_P14_APPROVE_FELIX_01 10)
(define TOKEN_P14_APPROVE_STRINGER_01 11)
(define TOKEN_P14_CARD_JACK 12)
(define TOKEN_P14_CARD_BUNNY 13)
(define TOKEN_P14_CARD_FRANKIE 14)
(define TOKEN_P14_CARD_MILO 15)
(define TOKEN_P14_CARD_VIVIAN 16)
(define TOKEN_P14_CARD_RITA 17)
(define TOKEN_P14_CARD_FELIX 18)
(define TOKEN_P14_CARD_STRINGER 19)
(define TOKEN_P14_DIALOGUE_001_01 20)
(define TOKEN_P14_DIALOGUE_002_01 21)
(define TOKEN_P14_DIALOGUE_003_01 22)
(define TOKEN_P14_DIALOGUE_003_02 23)
(define TOKEN_P14_DIALOGUE_003_03 24)
(define TOKEN_P14_DIALOGUE_003_04 25)
(define TOKEN_P14_DIALOGUE_003_05 26)
(define TOKEN_P14_SUCCESS_003_01 27)
(define TOKEN_P14_READ_001_01 28)
(define TOKEN_P14_SUCCESS_004_01 29)
(define TOKEN_P14_DIALOGUE_004_01 30)
(define TOKEN_P14_DIALOGUE_005_01 31)
(define TOKEN_P14_DIALOGUE_006_01 32)
(define TOKEN_P14_ENDING_001_01 33)
(define TOKEN_P14_ENDING_001_02 34)
(define TOKEN_P14_ENDING_001_03 35)
(define TOKEN_P14_ENDING_001_04 36)
(define TOKEN_P14_ENDING_001_05 37)
(define TOKEN_P14_ENDING_002_01 38)
(define TOKEN_P14_ENDING_002_02 39)
(define TOKEN_END_CREDIT_TITLE 40)
(define TOKEN_END_CREDIT_FICTIONAL_STUDIO 41)
(define TOKEN_END_CREDIT_REAL_CREATION 42)
(define TOKEN_END_CREDIT_CAST 43)
(define TOKEN_END_CREDIT_WRITERS_HEADER 44)
(define TOKEN_END_CREDIT_WRITERS_HEAD 45)
(define TOKEN_END_CREDIT_WRITERS_ASSISTANT 46)
(define TOKEN_END_CREDIT_WRITERS_CLUB 47)
(define TOKEN_END_CREDIT_WRITERS_SOCIAL 48)
(define TOKEN_END_CREDIT_WRITERS_META 49)
(define TOKEN_END_CREDIT_WRITERS_ENSEMBLE 50)
(define TOKEN_END_CREDIT_WRITERS_ADVENTURE 51)
(define TOKEN_END_CREDIT_WRITERS_OUTSIDER 52)
(define TOKEN_END_CREDIT_REAL_PRODUCTION 53)
(define TOKEN_END_CREDIT_FICTIONAL_PRODUCERS 54)
(define TOKEN_END_CREDIT_FICTIONAL_FLOOR 55)
(define TOKEN_END_CREDIT_FICTIONAL_CAMERA 56)
(define TOKEN_END_CREDIT_FICTIONAL_SOUND 57)
(define TOKEN_END_CREDIT_FICTIONAL_ART 58)
(define TOKEN_END_CREDIT_FICTIONAL_WARDROBE 59)
(define TOKEN_END_CREDIT_FICTIONAL_POST 60)
(define TOKEN_END_CREDIT_FICTIONAL_PRODUCTION 61)
(define TOKEN_END_CREDIT_FICTIONAL_MUSIC 62)
(define TOKEN_END_CREDIT_FICTIONAL_AUDIENCE 63)
(define TOKEN_END_CREDIT_REAL_ASSISTANCE 64)
(define TOKEN_END_CREDIT_THANKS 65)
(define TOKEN_END_ASSET_AUDIENCE_01 66)
(define TOKEN_END_ASSET_AUDIENCE_02 67)
(define TOKEN_END_ASSET_AUDIENCE_03 68)
(define TOKEN_END_ASSET_AUDIENCE_04 69)
(define TOKEN_END_ASSET_AUDIENCE_05 70)
(define TOKEN_END_ASSET_AUDIENCE_06 71)
(define TOKEN_END_ASSET_AUDIENCE_07 72)
(define TOKEN_END_ASSET_AUDIENCE_08 73)
(define TOKEN_END_ASSET_AUDIENCE_09 74)
(define TOKEN_END_ASSET_AUDIENCE_10 75)
(define TOKEN_END_ASSET_AUDIENCE_11 76)
(define TOKEN_END_ASSET_AUDIENCE_12 77)
(define TOKEN_END_ASSET_AUDIENCE_13 78)
(define TOKEN_END_ASSET_AUDIENCE_14 79)
(define TOKEN_END_ASSET_AUDIENCE_15 80)
(define TOKEN_END_ASSET_AUDIENCE_16 81)
(define TOKEN_END_ASSET_AUDIENCE_17 82)
(define TOKEN_END_ASSET_AUDIENCE_18 83)
(define TOKEN_END_ASSET_AUDIENCE_19 84)
(define TOKEN_END_ASSET_AUDIENCE_20 85)
(define TOKEN_END_ASSET_AUDIENCE_21 86)
(define TOKEN_END_ASSET_AUDIENCE_22 87)
(define TOKEN_END_ASSET_AUDIENCE_23 88)
(define TOKEN_END_ASSET_AUDIENCE_24 89)
(define TOKEN_END_ASSET_FOLEY_01 90)
(define TOKEN_END_ASSET_FOLEY_02 91)
(define TOKEN_END_ASSET_FOLEY_03 92)
(define TOKEN_END_ASSET_FOLEY_04 93)
(define TOKEN_END_ASSET_FOLEY_05 94)
(define TOKEN_END_ASSET_FOLEY_06 95)
(define TOKEN_END_ASSET_FOLEY_07 96)
(define TOKEN_END_ASSET_FOLEY_08 97)
(define TOKEN_END_ASSET_FOLEY_09 98)
(define ROOM_L03_PORCH 0)
(define ROOM_L01_LIVING_ROOM 1)
(define ROOM_L02_KITCHEN 2)
(define ROOM_L04_SIDE_PASSAGE 3)
(define ROOM_L05_COURTYARD 4)
(define ROOM_L06_GARAGE 5)
(define ROOM_L07_CONSERVATORY 6)
(define P14_SERIAL_COUNT 202)
(define P14_LINE_LIMIT 125)
(define P14_INVENTORY_LIMIT 443)
(class P14State
(properties
 p14Initialized 0
 p14EntryHi 0
 p14EntryLo 0
 p14DateLength 0
 p14Tone 0
 p14Phase 0
 p14Paused 0
 p14Skipped 0
 p14Replay 0
 p14CreditCount 0
 p14CreditCursor 0
 p14Win0Hi 0
 p14Win0Lo 0
 p14Win1Hi 0
 p14Win1Lo 0
 p14Win2Hi 0
 p14Win2Lo 0
 p14Win3Hi 0
 p14Win3Lo 0
 p14Date0Hi 0
 p14Date0Lo 0
 p14Date1Hi 0
 p14Date1Lo 0
 p14Date2Hi 0
 p14Date2Lo 0
 p14Date3Hi 0
 p14Date3Lo 0
 p14Date4Hi 0
 p14Date4Lo 0
 p14Date5Hi 0
 p14Date5Lo 0
 p14Date6Hi 0
 p14Date6Lo 0
 p14Date7Hi 0
 p14Date7Lo 0
 p14Date8Hi 0
 p14Date8Lo 0
 p14Date9Hi 0
 p14Date9Lo 0
 p14Date10Hi 0
 p14Date10Lo 0
 p14Date11Hi 0
 p14Date11Lo 0
 p14Date12Hi 0
 p14Date12Lo 0
 p14Date13Hi 0
 p14Date13Lo 0
 p14Date14Hi 0
 p14Date14Lo 0
 p14Date15Hi 0
 p14Date15Lo 0
 p14Date16Hi 0
 p14Date16Lo 0
 p14Date17Hi 0
 p14Date17Lo 0
 p14Date18Hi 0
 p14Date18Lo 0
 p14Date19Hi 0
 p14Date19Lo 0
 p14Date20Hi 0
 p14Date20Lo 0
 p14Date21Hi 0
 p14Date21Lo 0
 p14Date22Hi 0
 p14Date22Lo 0
 p14Date23Hi 0
 p14Date23Lo 0
 p14Date24Hi 0
 p14Date24Lo 0
 p14Date25Hi 0
 p14Date25Lo 0
 p14Date26Hi 0
 p14Date26Lo 0
 p14Date27Hi 0
 p14Date27Lo 0
 p14Date28Hi 0
 p14Date28Lo 0
 p14Date29Hi 0
 p14Date29Lo 0
 p14Date30Hi 0
 p14Date30Lo 0
 p14Date31Hi 0
 p14Date31Lo 0
 p14Date32Hi 0
 p14Date32Lo 0
 p14Date33Hi 0
 p14Date33Lo 0
 p14Date34Hi 0
 p14Date34Lo 0
 p14Date35Hi 0
 p14Date35Lo 0
 p14Date36Hi 0
 p14Date36Lo 0
 p14Date37Hi 0
 p14Date37Lo 0
 p14Date38Hi 0
 p14Date38Lo 0
 p14Date39Hi 0
 p14Date39Lo 0
 p14Date40Hi 0
 p14Date40Lo 0
 p14Date41Hi 0
 p14Date41Lo 0
 p14Date42Hi 0
 p14Date42Lo 0
 p14Date43Hi 0
 p14Date43Lo 0
 p14Date44Hi 0
 p14Date44Lo 0
 p14Date45Hi 0
 p14Date45Lo 0
 p14Date46Hi 0
 p14Date46Lo 0
 p14Date47Hi 0
 p14Date47Lo 0
 p14Date48Hi 0
 p14Date48Lo 0
 p14Date49Hi 0
 p14Date49Lo 0
 p14Date50Hi 0
 p14Date50Lo 0
 p14Date51Hi 0
 p14Date51Lo 0
 p14Date52Hi 0
 p14Date52Lo 0
 p14Date53Hi 0
 p14Date53Lo 0
 p14Date54Hi 0
 p14Date54Lo 0
 p14Date55Hi 0
 p14Date55Lo 0
 p14Date56Hi 0
 p14Date56Lo 0
 p14Date57Hi 0
 p14Date57Lo 0
 p14Date58Hi 0
 p14Date58Lo 0
 p14Date59Hi 0
 p14Date59Lo 0
 p14Date60Hi 0
 p14Date60Lo 0
 p14Date61Hi 0
 p14Date61Lo 0
 p14Date62Hi 0
 p14Date62Lo 0
 p14Date63Hi 0
 p14Date63Lo 0
 p14Date64Hi 0
 p14Date64Lo 0
 p14Date65Hi 0
 p14Date65Lo 0
 p14Date66Hi 0
 p14Date66Lo 0
 p14Date67Hi 0
 p14Date67Lo 0
 p14Date68Hi 0
 p14Date68Lo 0
 p14Date69Hi 0
 p14Date69Lo 0
 p14Date70Hi 0
 p14Date70Lo 0
 p14Date71Hi 0
 p14Date71Lo 0
 p14Date72Hi 0
 p14Date72Lo 0
 p14Date73Hi 0
 p14Date73Lo 0
 p14Date74Hi 0
 p14Date74Lo 0
 p14Date75Hi 0
 p14Date75Lo 0
 p14Date76Hi 0
 p14Date76Lo 0
 p14Date77Hi 0
 p14Date77Lo 0
 p14Date78Hi 0
 p14Date78Lo 0
 p14Date79Hi 0
 p14Date79Lo 0
 p14Credit0 0
 p14Credit1 0
 p14Credit2 0
 p14Credit3 0
 p14Credit4 0
 p14Credit5 0
 p14Credit6 0
 p14Credit7 0
 p14Credit8 0
 p14Credit9 0
 p14Credit10 0
 p14Credit11 0
 p14Credit12 0
 p14Credit13 0
 p14Credit14 0
 p14Credit15 0
 p14Credit16 0
 p14Credit17 0
 p14Credit18 0
 p14Credit19 0
 p14Credit20 0
 p14Credit21 0
 p14Credit22 0
 p14Credit23 0
 p14Credit24 0
 p14Credit25 0
 p14Credit26 0
 p14Credit27 0
 p14Credit28 0
 p14Credit29 0
 p14Credit30 0
 p14Credit31 0
 p14Credit32 0
 p14Credit33 0
 p14Credit34 0
 p14Credit35 0
 p14Credit36 0
 p14Credit37 0
 p14Credit38 0
 p14Credit39 0
 p14Credit40 0
 p14Credit41 0
 p14Credit42 0
 p14Credit43 0
 p14Credit44 0
 p14Credit45 0
 p14Credit46 0
 p14Credit47 0
 p14Credit48 0
 p14Credit49 0
 p14Credit50 0
 p14Credit51 0
 p14Credit52 0
 p14Credit53 0
 p14Credit54 0
 p14Credit55 0
 p14Credit56 0
 p14Credit57 0
 p14Credit58 0
 p14RevisionHi 0
 p14RevisionLo 0
 p14StartHi 0
 p14StartLo 0
 p14SignatureHi 0
 p14SignatureLo 0
 p14PencilHi 0
 p14PencilLo 0
 p14CompleteHi 0
 p14CompleteLo 0
 p14FinaleHi 0
 p14FinaleLo 0
 p14FrameHi 0
 p14FrameLo 0
 p14CelebrationHi 0
 p14CelebrationLo 0
 p14LaughHi 0
 p14LaughLo 0
 p14PinJackHi 0
 p14PinJackLo 0
 p14PinBunnyHi 0
 p14PinBunnyLo 0
 p14PinFrankieHi 0
 p14PinFrankieLo 0
 p14PinMiloHi 0
 p14PinMiloLo 0
 p14PinVivianHi 0
 p14PinVivianLo 0
 p14PinRitaHi 0
 p14PinRitaLo 0
 p14PinFelixHi 0
 p14PinFelixLo 0
 p14PinStringerHi 0
 p14PinStringerLo 0
 p14Source1StartHi 0
 p14Source1StartLo 0
 p14Source2StartHi 0
 p14Source2StartLo 0
 p14Source3StartHi 0
 p14Source3StartLo 0
 p14Source4StartHi 0
 p14Source4StartLo 0
 p14Source5StartHi 0
 p14Source5StartLo 0
 p14Source6StartHi 0
 p14Source6StartLo 0
 p14Source7StartHi 0
 p14Source7StartLo 0
 p14Source8StartHi 0
 p14Source8StartLo 0
 p14Source9StartHi 0
 p14Source9StartLo 0
 p14Source10StartHi 0
 p14Source10StartLo 0
 p14Source11StartHi 0
 p14Source11StartLo 0
 p14Source12StartHi 0
 p14Source12StartLo 0
 p14Source13StartHi 0
 p14Source13StartLo 0
 p14Source14StartHi 0
 p14Source14StartLo 0
 p14Source15StartHi 0
 p14Source15StartLo 0
 p14Source16StartHi 0
 p14Source16StartLo 0
 p14Source17StartHi 0
 p14Source17StartLo 0
 p14Source18StartHi 0
 p14Source18StartLo 0
 p14Source19StartHi 0
 p14Source19StartLo 0
 p14Source20StartHi 0
 p14Source20StartLo 0
 p14Source21StartHi 0
 p14Source21StartLo 0
 p14Source22StartHi 0
 p14Source22StartLo 0
 p14Source23StartHi 0
 p14Source23StartLo 0
 p14Source24StartHi 0
 p14Source24StartLo 0
 p14Source25StartHi 0
 p14Source25StartLo 0
 p14Source26StartHi 0
 p14Source26StartLo 0
 p14Source27StartHi 0
 p14Source27StartLo 0
 p14Source28StartHi 0
 p14Source28StartLo 0
 p14Source29StartHi 0
 p14Source29StartLo 0
 p14Source30StartHi 0
 p14Source30StartLo 0
 p14Source31StartHi 0
 p14Source31StartLo 0
 p14Source32StartHi 0
 p14Source32StartLo 0
 p14Source33StartHi 0
 p14Source33StartLo 0
 p14Source34StartHi 0
 p14Source34StartLo 0
 p14Source35StartHi 0
 p14Source35StartLo 0
 p14Source36StartHi 0
 p14Source36StartLo 0
 p14Source37StartHi 0
 p14Source37StartLo 0
 p14Source38StartHi 0
 p14Source38StartLo 0
 p14Source39StartHi 0
 p14Source39StartLo 0
 p14Source40StartHi 0
 p14Source40StartLo 0
 p14Source41StartHi 0
 p14Source41StartLo 0
 p14Source42StartHi 0
 p14Source42StartLo 0
 p14Source43StartHi 0
 p14Source43StartLo 0
 p14Source44StartHi 0
 p14Source44StartLo 0
 p14Source45StartHi 0
 p14Source45StartLo 0
 p14Source46StartHi 0
 p14Source46StartLo 0
 p14Source47StartHi 0
 p14Source47StartLo 0
 p14Source48StartHi 0
 p14Source48StartLo 0
 p14Source49StartHi 0
 p14Source49StartLo 0
 p14Source50StartHi 0
 p14Source50StartLo 0
 p14Source51StartHi 0
 p14Source51StartLo 0
 p14Source52StartHi 0
 p14Source52StartLo 0
 p14Source53StartHi 0
 p14Source53StartLo 0
 p14Source54StartHi 0
 p14Source54StartLo 0
 p14Source55StartHi 0
 p14Source55StartLo 0
 p14Source56StartHi 0
 p14Source56StartLo 0
 p14Source57StartHi 0
 p14Source57StartLo 0
 p14Source58StartHi 0
 p14Source58StartLo 0
 p14Source59StartHi 0
 p14Source59StartLo 0
 p14Source60StartHi 0
 p14Source60StartLo 0
 p14Source61StartHi 0
 p14Source61StartLo 0
 p14Source62StartHi 0
 p14Source62StartLo 0
 p14Source63StartHi 0
 p14Source63StartLo 0
 p14Source64StartHi 0
 p14Source64StartLo 0
 p14Source65StartHi 0
 p14Source65StartLo 0
 p14Source66StartHi 0
 p14Source66StartLo 0
 p14Source67StartHi 0
 p14Source67StartLo 0
 p14Source68StartHi 0
 p14Source68StartLo 0
 p14Source69StartHi 0
 p14Source69StartLo 0
 p14Source70StartHi 0
 p14Source70StartLo 0
 p14Source71StartHi 0
 p14Source71StartLo 0
 p14Source72StartHi 0
 p14Source72StartLo 0
 p14Source73StartHi 0
 p14Source73StartLo 0
 p14Source74StartHi 0
 p14Source74StartLo 0
 p14Source75StartHi 0
 p14Source75StartLo 0
 p14Source76StartHi 0
 p14Source76StartLo 0
 p14Source77StartHi 0
 p14Source77StartLo 0
 p14Source78StartHi 0
 p14Source78StartLo 0
 p14Source79StartHi 0
 p14Source79StartLo 0
 p14Source80StartHi 0
 p14Source80StartLo 0
 p14Source81StartHi 0
 p14Source81StartLo 0
 p14Source82StartHi 0
 p14Source82StartLo 0
 p14Source83StartHi 0
 p14Source83StartLo 0
 p14Source84StartHi 0
 p14Source84StartLo 0
 p14Source85StartHi 0
 p14Source85StartLo 0
 p14Source86StartHi 0
 p14Source86StartLo 0
 p14Source87StartHi 0
 p14Source87StartLo 0
 p14Source1Receipt1Hi 0
 p14Source1Receipt1Lo 0
 p14Source1Receipt2Hi 0
 p14Source1Receipt2Lo 0
 p14Source1Receipt3Hi 0
 p14Source1Receipt3Lo 0
 p14Source2Receipt1Hi 0
 p14Source2Receipt1Lo 0
 p14Source3Receipt1Hi 0
 p14Source3Receipt1Lo 0
 p14Source4Receipt1Hi 0
 p14Source4Receipt1Lo 0
 p14Source5Receipt1Hi 0
 p14Source5Receipt1Lo 0
 p14Source6Receipt1Hi 0
 p14Source6Receipt1Lo 0
 p14Source7Receipt1Hi 0
 p14Source7Receipt1Lo 0
 p14Source8Receipt1Hi 0
 p14Source8Receipt1Lo 0
 p14Source9Receipt1Hi 0
 p14Source9Receipt1Lo 0
 p14Source10Receipt1Hi 0
 p14Source10Receipt1Lo 0
 p14Source11Receipt1Hi 0
 p14Source11Receipt1Lo 0
 p14Source12Receipt1Hi 0
 p14Source12Receipt1Lo 0
 p14Source13Receipt1Hi 0
 p14Source13Receipt1Lo 0
 p14Source14Receipt1Hi 0
 p14Source14Receipt1Lo 0
 p14Source15Receipt1Hi 0
 p14Source15Receipt1Lo 0
 p14Source16Receipt1Hi 0
 p14Source16Receipt1Lo 0
 p14Source17Receipt1Hi 0
 p14Source17Receipt1Lo 0
 p14Source18Receipt1Hi 0
 p14Source18Receipt1Lo 0
 p14Source19Receipt1Hi 0
 p14Source19Receipt1Lo 0
 p14Source20Receipt1Hi 0
 p14Source20Receipt1Lo 0
 p14Source20Receipt2Hi 0
 p14Source20Receipt2Lo 0
 p14Source20Receipt3Hi 0
 p14Source20Receipt3Lo 0
 p14Source20Receipt4Hi 0
 p14Source20Receipt4Lo 0
 p14Source20Receipt5Hi 0
 p14Source20Receipt5Lo 0
 p14Source21Receipt1Hi 0
 p14Source21Receipt1Lo 0
 p14Source22Receipt1Hi 0
 p14Source22Receipt1Lo 0
 p14Source23Receipt1Hi 0
 p14Source23Receipt1Lo 0
 p14Source24Receipt1Hi 0
 p14Source24Receipt1Lo 0
 p14Source25Receipt1Hi 0
 p14Source25Receipt1Lo 0
 p14Source26Receipt1Hi 0
 p14Source26Receipt1Lo 0
 p14Source27Receipt1Hi 0
 p14Source27Receipt1Lo 0
 p14Source27Receipt2Hi 0
 p14Source27Receipt2Lo 0
 p14Source27Receipt3Hi 0
 p14Source27Receipt3Lo 0
 p14Source27Receipt4Hi 0
 p14Source27Receipt4Lo 0
 p14Source27Receipt5Hi 0
 p14Source27Receipt5Lo 0
 p14Source28Receipt1Hi 0
 p14Source28Receipt1Lo 0
 p14Source28Receipt2Hi 0
 p14Source28Receipt2Lo 0
 p14Source29Receipt1Hi 0
 p14Source29Receipt1Lo 0
 p14Source30Receipt1Hi 0
 p14Source30Receipt1Lo 0
 p14Source31Receipt1Hi 0
 p14Source31Receipt1Lo 0
 p14Source32Receipt1Hi 0
 p14Source32Receipt1Lo 0
 p14Source33Receipt1Hi 0
 p14Source33Receipt1Lo 0
 p14Source34Receipt1Hi 0
 p14Source34Receipt1Lo 0
 p14Source35Receipt1Hi 0
 p14Source35Receipt1Lo 0
 p14Source36Receipt1Hi 0
 p14Source36Receipt1Lo 0
 p14Source37Receipt1Hi 0
 p14Source37Receipt1Lo 0
 p14Source38Receipt1Hi 0
 p14Source38Receipt1Lo 0
 p14Source39Receipt1Hi 0
 p14Source39Receipt1Lo 0
 p14Source40Receipt1Hi 0
 p14Source40Receipt1Lo 0
 p14Source41Receipt1Hi 0
 p14Source41Receipt1Lo 0
 p14Source42Receipt1Hi 0
 p14Source42Receipt1Lo 0
 p14Source43Receipt1Hi 0
 p14Source43Receipt1Lo 0
 p14Source44Receipt1Hi 0
 p14Source44Receipt1Lo 0
 p14Source45Receipt1Hi 0
 p14Source45Receipt1Lo 0
 p14Source46Receipt1Hi 0
 p14Source46Receipt1Lo 0
 p14Source47Receipt1Hi 0
 p14Source47Receipt1Lo 0
 p14Source48Receipt1Hi 0
 p14Source48Receipt1Lo 0
 p14Source49Receipt1Hi 0
 p14Source49Receipt1Lo 0
 p14Source50Receipt1Hi 0
 p14Source50Receipt1Lo 0
 p14Source51Receipt1Hi 0
 p14Source51Receipt1Lo 0
 p14Source52Receipt1Hi 0
 p14Source52Receipt1Lo 0
 p14Source53Receipt1Hi 0
 p14Source53Receipt1Lo 0
 p14Source54Receipt1Hi 0
 p14Source54Receipt1Lo 0
 p14Source55Receipt1Hi 0
 p14Source55Receipt1Lo 0
 p14Source56Receipt1Hi 0
 p14Source56Receipt1Lo 0
 p14Source57Receipt1Hi 0
 p14Source57Receipt1Lo 0
 p14Source58Receipt1Hi 0
 p14Source58Receipt1Lo 0
 p14Source59Receipt1Hi 0
 p14Source59Receipt1Lo 0
 p14Source60Receipt1Hi 0
 p14Source60Receipt1Lo 0
 p14Source61Receipt1Hi 0
 p14Source61Receipt1Lo 0
 p14Source62Receipt1Hi 0
 p14Source62Receipt1Lo 0
 p14Source63Receipt1Hi 0
 p14Source63Receipt1Lo 0
 p14Source64Receipt1Hi 0
 p14Source64Receipt1Lo 0
 p14Source65Receipt1Hi 0
 p14Source65Receipt1Lo 0
 p14Source66Receipt1Hi 0
 p14Source66Receipt1Lo 0
 p14Source67Receipt1Hi 0
 p14Source67Receipt1Lo 0
 p14Source68Receipt1Hi 0
 p14Source68Receipt1Lo 0
 p14Source69Receipt1Hi 0
 p14Source69Receipt1Lo 0
 p14Source70Receipt1Hi 0
 p14Source70Receipt1Lo 0
 p14Source71Receipt1Hi 0
 p14Source71Receipt1Lo 0
 p14Source72Receipt1Hi 0
 p14Source72Receipt1Lo 0
 p14Source73Receipt1Hi 0
 p14Source73Receipt1Lo 0
 p14Source74Receipt1Hi 0
 p14Source74Receipt1Lo 0
 p14Source75Receipt1Hi 0
 p14Source75Receipt1Lo 0
 p14Source76Receipt1Hi 0
 p14Source76Receipt1Lo 0
 p14Source77Receipt1Hi 0
 p14Source77Receipt1Lo 0
 p14Source78Receipt1Hi 0
 p14Source78Receipt1Lo 0
 p14Source79Receipt1Hi 0
 p14Source79Receipt1Lo 0
 p14Source80Receipt1Hi 0
 p14Source80Receipt1Lo 0
 p14Source81Receipt1Hi 0
 p14Source81Receipt1Lo 0
 p14Source82Receipt1Hi 0
 p14Source82Receipt1Lo 0
 p14Source83Receipt1Hi 0
 p14Source83Receipt1Lo 0
 p14Source84Receipt1Hi 0
 p14Source84Receipt1Lo 0
 p14Source85Receipt1Hi 0
 p14Source85Receipt1Lo 0
 p14Source86Receipt1Hi 0
 p14Source86Receipt1Lo 0
 p14Source87Receipt1Hi 0
 p14Source87Receipt1Lo 0
 p14ContextValid 0
 p14ContextBuilding 0
 p14ContextDateLength 0
 p14Room 0
 p14Apron 0
 p14FlagsHi 0
 p14FlagsLo 0
 p14BoardRoom 0
 p14InputTone 0
 p14ContestActive 0
 p14BunnyRoom 0
 p14FrankieRoom 0
 p14MiloRoom 0
 p14VivianRoom 0
 p14RitaRoom 0
 p14FelixRoom 0
 p14StringerRoom 0
 p14Epoch 0
 p14Code 0
 p14LineCount 0
 p14UnitCount 0
 p14EventCount 0
 p14ResultHi 0
 p14ResultLo 0
 p14PresentationSource 0
 p14PresentationHi 0
 p14PresentationLo 0
)
(method (p14SerialHi slot &tmp answer) (= answer 0) (switch (/ slot 16) (0 (switch slot (0 (= answer p14RevisionHi))(1 (= answer p14StartHi))(2 (= answer p14SignatureHi))(3 (= answer p14PencilHi))(4 (= answer p14CompleteHi))(5 (= answer p14FinaleHi))(6 (= answer p14FrameHi))(7 (= answer p14CelebrationHi))(8 (= answer p14LaughHi))(9 (= answer p14PinJackHi))(10 (= answer p14PinBunnyHi))(11 (= answer p14PinFrankieHi))(12 (= answer p14PinMiloHi))(13 (= answer p14PinVivianHi))(14 (= answer p14PinRitaHi))(15 (= answer p14PinFelixHi))))(1 (switch slot (16 (= answer p14PinStringerHi))(17 (= answer p14Source1StartHi))(18 (= answer p14Source2StartHi))(19 (= answer p14Source3StartHi))(20 (= answer p14Source4StartHi))(21 (= answer p14Source5StartHi))(22 (= answer p14Source6StartHi))(23 (= answer p14Source7StartHi))(24 (= answer p14Source8StartHi))(25 (= answer p14Source9StartHi))(26 (= answer p14Source10StartHi))(27 (= answer p14Source11StartHi))(28 (= answer p14Source12StartHi))(29 (= answer p14Source13StartHi))(30 (= answer p14Source14StartHi))(31 (= answer p14Source15StartHi))))(2 (switch slot (32 (= answer p14Source16StartHi))(33 (= answer p14Source17StartHi))(34 (= answer p14Source18StartHi))(35 (= answer p14Source19StartHi))(36 (= answer p14Source20StartHi))(37 (= answer p14Source21StartHi))(38 (= answer p14Source22StartHi))(39 (= answer p14Source23StartHi))(40 (= answer p14Source24StartHi))(41 (= answer p14Source25StartHi))(42 (= answer p14Source26StartHi))(43 (= answer p14Source27StartHi))(44 (= answer p14Source28StartHi))(45 (= answer p14Source29StartHi))(46 (= answer p14Source30StartHi))(47 (= answer p14Source31StartHi))))(3 (switch slot (48 (= answer p14Source32StartHi))(49 (= answer p14Source33StartHi))(50 (= answer p14Source34StartHi))(51 (= answer p14Source35StartHi))(52 (= answer p14Source36StartHi))(53 (= answer p14Source37StartHi))(54 (= answer p14Source38StartHi))(55 (= answer p14Source39StartHi))(56 (= answer p14Source40StartHi))(57 (= answer p14Source41StartHi))(58 (= answer p14Source42StartHi))(59 (= answer p14Source43StartHi))(60 (= answer p14Source44StartHi))(61 (= answer p14Source45StartHi))(62 (= answer p14Source46StartHi))(63 (= answer p14Source47StartHi))))(4 (switch slot (64 (= answer p14Source48StartHi))(65 (= answer p14Source49StartHi))(66 (= answer p14Source50StartHi))(67 (= answer p14Source51StartHi))(68 (= answer p14Source52StartHi))(69 (= answer p14Source53StartHi))(70 (= answer p14Source54StartHi))(71 (= answer p14Source55StartHi))(72 (= answer p14Source56StartHi))(73 (= answer p14Source57StartHi))(74 (= answer p14Source58StartHi))(75 (= answer p14Source59StartHi))(76 (= answer p14Source60StartHi))(77 (= answer p14Source61StartHi))(78 (= answer p14Source62StartHi))(79 (= answer p14Source63StartHi))))(5 (switch slot (80 (= answer p14Source64StartHi))(81 (= answer p14Source65StartHi))(82 (= answer p14Source66StartHi))(83 (= answer p14Source67StartHi))(84 (= answer p14Source68StartHi))(85 (= answer p14Source69StartHi))(86 (= answer p14Source70StartHi))(87 (= answer p14Source71StartHi))(88 (= answer p14Source72StartHi))(89 (= answer p14Source73StartHi))(90 (= answer p14Source74StartHi))(91 (= answer p14Source75StartHi))(92 (= answer p14Source76StartHi))(93 (= answer p14Source77StartHi))(94 (= answer p14Source78StartHi))(95 (= answer p14Source79StartHi))))(6 (switch slot (96 (= answer p14Source80StartHi))(97 (= answer p14Source81StartHi))(98 (= answer p14Source82StartHi))(99 (= answer p14Source83StartHi))(100 (= answer p14Source84StartHi))(101 (= answer p14Source85StartHi))(102 (= answer p14Source86StartHi))(103 (= answer p14Source87StartHi))(104 (= answer p14Source1Receipt1Hi))(105 (= answer p14Source1Receipt2Hi))(106 (= answer p14Source1Receipt3Hi))(107 (= answer p14Source2Receipt1Hi))(108 (= answer p14Source3Receipt1Hi))(109 (= answer p14Source4Receipt1Hi))(110 (= answer p14Source5Receipt1Hi))(111 (= answer p14Source6Receipt1Hi))))(7 (switch slot (112 (= answer p14Source7Receipt1Hi))(113 (= answer p14Source8Receipt1Hi))(114 (= answer p14Source9Receipt1Hi))(115 (= answer p14Source10Receipt1Hi))(116 (= answer p14Source11Receipt1Hi))(117 (= answer p14Source12Receipt1Hi))(118 (= answer p14Source13Receipt1Hi))(119 (= answer p14Source14Receipt1Hi))(120 (= answer p14Source15Receipt1Hi))(121 (= answer p14Source16Receipt1Hi))(122 (= answer p14Source17Receipt1Hi))(123 (= answer p14Source18Receipt1Hi))(124 (= answer p14Source19Receipt1Hi))(125 (= answer p14Source20Receipt1Hi))(126 (= answer p14Source20Receipt2Hi))(127 (= answer p14Source20Receipt3Hi))))(8 (switch slot (128 (= answer p14Source20Receipt4Hi))(129 (= answer p14Source20Receipt5Hi))(130 (= answer p14Source21Receipt1Hi))(131 (= answer p14Source22Receipt1Hi))(132 (= answer p14Source23Receipt1Hi))(133 (= answer p14Source24Receipt1Hi))(134 (= answer p14Source25Receipt1Hi))(135 (= answer p14Source26Receipt1Hi))(136 (= answer p14Source27Receipt1Hi))(137 (= answer p14Source27Receipt2Hi))(138 (= answer p14Source27Receipt3Hi))(139 (= answer p14Source27Receipt4Hi))(140 (= answer p14Source27Receipt5Hi))(141 (= answer p14Source28Receipt1Hi))(142 (= answer p14Source28Receipt2Hi))(143 (= answer p14Source29Receipt1Hi))))(9 (switch slot (144 (= answer p14Source30Receipt1Hi))(145 (= answer p14Source31Receipt1Hi))(146 (= answer p14Source32Receipt1Hi))(147 (= answer p14Source33Receipt1Hi))(148 (= answer p14Source34Receipt1Hi))(149 (= answer p14Source35Receipt1Hi))(150 (= answer p14Source36Receipt1Hi))(151 (= answer p14Source37Receipt1Hi))(152 (= answer p14Source38Receipt1Hi))(153 (= answer p14Source39Receipt1Hi))(154 (= answer p14Source40Receipt1Hi))(155 (= answer p14Source41Receipt1Hi))(156 (= answer p14Source42Receipt1Hi))(157 (= answer p14Source43Receipt1Hi))(158 (= answer p14Source44Receipt1Hi))(159 (= answer p14Source45Receipt1Hi))))(10 (switch slot (160 (= answer p14Source46Receipt1Hi))(161 (= answer p14Source47Receipt1Hi))(162 (= answer p14Source48Receipt1Hi))(163 (= answer p14Source49Receipt1Hi))(164 (= answer p14Source50Receipt1Hi))(165 (= answer p14Source51Receipt1Hi))(166 (= answer p14Source52Receipt1Hi))(167 (= answer p14Source53Receipt1Hi))(168 (= answer p14Source54Receipt1Hi))(169 (= answer p14Source55Receipt1Hi))(170 (= answer p14Source56Receipt1Hi))(171 (= answer p14Source57Receipt1Hi))(172 (= answer p14Source58Receipt1Hi))(173 (= answer p14Source59Receipt1Hi))(174 (= answer p14Source60Receipt1Hi))(175 (= answer p14Source61Receipt1Hi))))(11 (switch slot (176 (= answer p14Source62Receipt1Hi))(177 (= answer p14Source63Receipt1Hi))(178 (= answer p14Source64Receipt1Hi))(179 (= answer p14Source65Receipt1Hi))(180 (= answer p14Source66Receipt1Hi))(181 (= answer p14Source67Receipt1Hi))(182 (= answer p14Source68Receipt1Hi))(183 (= answer p14Source69Receipt1Hi))(184 (= answer p14Source70Receipt1Hi))(185 (= answer p14Source71Receipt1Hi))(186 (= answer p14Source72Receipt1Hi))(187 (= answer p14Source73Receipt1Hi))(188 (= answer p14Source74Receipt1Hi))(189 (= answer p14Source75Receipt1Hi))(190 (= answer p14Source76Receipt1Hi))(191 (= answer p14Source77Receipt1Hi))))(12 (switch slot (192 (= answer p14Source78Receipt1Hi))(193 (= answer p14Source79Receipt1Hi))(194 (= answer p14Source80Receipt1Hi))(195 (= answer p14Source81Receipt1Hi))(196 (= answer p14Source82Receipt1Hi))(197 (= answer p14Source83Receipt1Hi))(198 (= answer p14Source84Receipt1Hi))(199 (= answer p14Source85Receipt1Hi))(200 (= answer p14Source86Receipt1Hi))(201 (= answer p14Source87Receipt1Hi))))) (return answer))
(method (p14SerialLo slot &tmp answer) (= answer 0) (switch (/ slot 16) (0 (switch slot (0 (= answer p14RevisionLo))(1 (= answer p14StartLo))(2 (= answer p14SignatureLo))(3 (= answer p14PencilLo))(4 (= answer p14CompleteLo))(5 (= answer p14FinaleLo))(6 (= answer p14FrameLo))(7 (= answer p14CelebrationLo))(8 (= answer p14LaughLo))(9 (= answer p14PinJackLo))(10 (= answer p14PinBunnyLo))(11 (= answer p14PinFrankieLo))(12 (= answer p14PinMiloLo))(13 (= answer p14PinVivianLo))(14 (= answer p14PinRitaLo))(15 (= answer p14PinFelixLo))))(1 (switch slot (16 (= answer p14PinStringerLo))(17 (= answer p14Source1StartLo))(18 (= answer p14Source2StartLo))(19 (= answer p14Source3StartLo))(20 (= answer p14Source4StartLo))(21 (= answer p14Source5StartLo))(22 (= answer p14Source6StartLo))(23 (= answer p14Source7StartLo))(24 (= answer p14Source8StartLo))(25 (= answer p14Source9StartLo))(26 (= answer p14Source10StartLo))(27 (= answer p14Source11StartLo))(28 (= answer p14Source12StartLo))(29 (= answer p14Source13StartLo))(30 (= answer p14Source14StartLo))(31 (= answer p14Source15StartLo))))(2 (switch slot (32 (= answer p14Source16StartLo))(33 (= answer p14Source17StartLo))(34 (= answer p14Source18StartLo))(35 (= answer p14Source19StartLo))(36 (= answer p14Source20StartLo))(37 (= answer p14Source21StartLo))(38 (= answer p14Source22StartLo))(39 (= answer p14Source23StartLo))(40 (= answer p14Source24StartLo))(41 (= answer p14Source25StartLo))(42 (= answer p14Source26StartLo))(43 (= answer p14Source27StartLo))(44 (= answer p14Source28StartLo))(45 (= answer p14Source29StartLo))(46 (= answer p14Source30StartLo))(47 (= answer p14Source31StartLo))))(3 (switch slot (48 (= answer p14Source32StartLo))(49 (= answer p14Source33StartLo))(50 (= answer p14Source34StartLo))(51 (= answer p14Source35StartLo))(52 (= answer p14Source36StartLo))(53 (= answer p14Source37StartLo))(54 (= answer p14Source38StartLo))(55 (= answer p14Source39StartLo))(56 (= answer p14Source40StartLo))(57 (= answer p14Source41StartLo))(58 (= answer p14Source42StartLo))(59 (= answer p14Source43StartLo))(60 (= answer p14Source44StartLo))(61 (= answer p14Source45StartLo))(62 (= answer p14Source46StartLo))(63 (= answer p14Source47StartLo))))(4 (switch slot (64 (= answer p14Source48StartLo))(65 (= answer p14Source49StartLo))(66 (= answer p14Source50StartLo))(67 (= answer p14Source51StartLo))(68 (= answer p14Source52StartLo))(69 (= answer p14Source53StartLo))(70 (= answer p14Source54StartLo))(71 (= answer p14Source55StartLo))(72 (= answer p14Source56StartLo))(73 (= answer p14Source57StartLo))(74 (= answer p14Source58StartLo))(75 (= answer p14Source59StartLo))(76 (= answer p14Source60StartLo))(77 (= answer p14Source61StartLo))(78 (= answer p14Source62StartLo))(79 (= answer p14Source63StartLo))))(5 (switch slot (80 (= answer p14Source64StartLo))(81 (= answer p14Source65StartLo))(82 (= answer p14Source66StartLo))(83 (= answer p14Source67StartLo))(84 (= answer p14Source68StartLo))(85 (= answer p14Source69StartLo))(86 (= answer p14Source70StartLo))(87 (= answer p14Source71StartLo))(88 (= answer p14Source72StartLo))(89 (= answer p14Source73StartLo))(90 (= answer p14Source74StartLo))(91 (= answer p14Source75StartLo))(92 (= answer p14Source76StartLo))(93 (= answer p14Source77StartLo))(94 (= answer p14Source78StartLo))(95 (= answer p14Source79StartLo))))(6 (switch slot (96 (= answer p14Source80StartLo))(97 (= answer p14Source81StartLo))(98 (= answer p14Source82StartLo))(99 (= answer p14Source83StartLo))(100 (= answer p14Source84StartLo))(101 (= answer p14Source85StartLo))(102 (= answer p14Source86StartLo))(103 (= answer p14Source87StartLo))(104 (= answer p14Source1Receipt1Lo))(105 (= answer p14Source1Receipt2Lo))(106 (= answer p14Source1Receipt3Lo))(107 (= answer p14Source2Receipt1Lo))(108 (= answer p14Source3Receipt1Lo))(109 (= answer p14Source4Receipt1Lo))(110 (= answer p14Source5Receipt1Lo))(111 (= answer p14Source6Receipt1Lo))))(7 (switch slot (112 (= answer p14Source7Receipt1Lo))(113 (= answer p14Source8Receipt1Lo))(114 (= answer p14Source9Receipt1Lo))(115 (= answer p14Source10Receipt1Lo))(116 (= answer p14Source11Receipt1Lo))(117 (= answer p14Source12Receipt1Lo))(118 (= answer p14Source13Receipt1Lo))(119 (= answer p14Source14Receipt1Lo))(120 (= answer p14Source15Receipt1Lo))(121 (= answer p14Source16Receipt1Lo))(122 (= answer p14Source17Receipt1Lo))(123 (= answer p14Source18Receipt1Lo))(124 (= answer p14Source19Receipt1Lo))(125 (= answer p14Source20Receipt1Lo))(126 (= answer p14Source20Receipt2Lo))(127 (= answer p14Source20Receipt3Lo))))(8 (switch slot (128 (= answer p14Source20Receipt4Lo))(129 (= answer p14Source20Receipt5Lo))(130 (= answer p14Source21Receipt1Lo))(131 (= answer p14Source22Receipt1Lo))(132 (= answer p14Source23Receipt1Lo))(133 (= answer p14Source24Receipt1Lo))(134 (= answer p14Source25Receipt1Lo))(135 (= answer p14Source26Receipt1Lo))(136 (= answer p14Source27Receipt1Lo))(137 (= answer p14Source27Receipt2Lo))(138 (= answer p14Source27Receipt3Lo))(139 (= answer p14Source27Receipt4Lo))(140 (= answer p14Source27Receipt5Lo))(141 (= answer p14Source28Receipt1Lo))(142 (= answer p14Source28Receipt2Lo))(143 (= answer p14Source29Receipt1Lo))))(9 (switch slot (144 (= answer p14Source30Receipt1Lo))(145 (= answer p14Source31Receipt1Lo))(146 (= answer p14Source32Receipt1Lo))(147 (= answer p14Source33Receipt1Lo))(148 (= answer p14Source34Receipt1Lo))(149 (= answer p14Source35Receipt1Lo))(150 (= answer p14Source36Receipt1Lo))(151 (= answer p14Source37Receipt1Lo))(152 (= answer p14Source38Receipt1Lo))(153 (= answer p14Source39Receipt1Lo))(154 (= answer p14Source40Receipt1Lo))(155 (= answer p14Source41Receipt1Lo))(156 (= answer p14Source42Receipt1Lo))(157 (= answer p14Source43Receipt1Lo))(158 (= answer p14Source44Receipt1Lo))(159 (= answer p14Source45Receipt1Lo))))(10 (switch slot (160 (= answer p14Source46Receipt1Lo))(161 (= answer p14Source47Receipt1Lo))(162 (= answer p14Source48Receipt1Lo))(163 (= answer p14Source49Receipt1Lo))(164 (= answer p14Source50Receipt1Lo))(165 (= answer p14Source51Receipt1Lo))(166 (= answer p14Source52Receipt1Lo))(167 (= answer p14Source53Receipt1Lo))(168 (= answer p14Source54Receipt1Lo))(169 (= answer p14Source55Receipt1Lo))(170 (= answer p14Source56Receipt1Lo))(171 (= answer p14Source57Receipt1Lo))(172 (= answer p14Source58Receipt1Lo))(173 (= answer p14Source59Receipt1Lo))(174 (= answer p14Source60Receipt1Lo))(175 (= answer p14Source61Receipt1Lo))))(11 (switch slot (176 (= answer p14Source62Receipt1Lo))(177 (= answer p14Source63Receipt1Lo))(178 (= answer p14Source64Receipt1Lo))(179 (= answer p14Source65Receipt1Lo))(180 (= answer p14Source66Receipt1Lo))(181 (= answer p14Source67Receipt1Lo))(182 (= answer p14Source68Receipt1Lo))(183 (= answer p14Source69Receipt1Lo))(184 (= answer p14Source70Receipt1Lo))(185 (= answer p14Source71Receipt1Lo))(186 (= answer p14Source72Receipt1Lo))(187 (= answer p14Source73Receipt1Lo))(188 (= answer p14Source74Receipt1Lo))(189 (= answer p14Source75Receipt1Lo))(190 (= answer p14Source76Receipt1Lo))(191 (= answer p14Source77Receipt1Lo))))(12 (switch slot (192 (= answer p14Source78Receipt1Lo))(193 (= answer p14Source79Receipt1Lo))(194 (= answer p14Source80Receipt1Lo))(195 (= answer p14Source81Receipt1Lo))(196 (= answer p14Source82Receipt1Lo))(197 (= answer p14Source83Receipt1Lo))(198 (= answer p14Source84Receipt1Lo))(199 (= answer p14Source85Receipt1Lo))(200 (= answer p14Source86Receipt1Lo))(201 (= answer p14Source87Receipt1Lo))))) (return answer))
(method (p14SetSerial slot hi lo) (switch (/ slot 16) (0 (switch slot (0 (= p14RevisionHi hi) (= p14RevisionLo lo))(1 (= p14StartHi hi) (= p14StartLo lo))(2 (= p14SignatureHi hi) (= p14SignatureLo lo))(3 (= p14PencilHi hi) (= p14PencilLo lo))(4 (= p14CompleteHi hi) (= p14CompleteLo lo))(5 (= p14FinaleHi hi) (= p14FinaleLo lo))(6 (= p14FrameHi hi) (= p14FrameLo lo))(7 (= p14CelebrationHi hi) (= p14CelebrationLo lo))(8 (= p14LaughHi hi) (= p14LaughLo lo))(9 (= p14PinJackHi hi) (= p14PinJackLo lo))(10 (= p14PinBunnyHi hi) (= p14PinBunnyLo lo))(11 (= p14PinFrankieHi hi) (= p14PinFrankieLo lo))(12 (= p14PinMiloHi hi) (= p14PinMiloLo lo))(13 (= p14PinVivianHi hi) (= p14PinVivianLo lo))(14 (= p14PinRitaHi hi) (= p14PinRitaLo lo))(15 (= p14PinFelixHi hi) (= p14PinFelixLo lo))))(1 (switch slot (16 (= p14PinStringerHi hi) (= p14PinStringerLo lo))(17 (= p14Source1StartHi hi) (= p14Source1StartLo lo))(18 (= p14Source2StartHi hi) (= p14Source2StartLo lo))(19 (= p14Source3StartHi hi) (= p14Source3StartLo lo))(20 (= p14Source4StartHi hi) (= p14Source4StartLo lo))(21 (= p14Source5StartHi hi) (= p14Source5StartLo lo))(22 (= p14Source6StartHi hi) (= p14Source6StartLo lo))(23 (= p14Source7StartHi hi) (= p14Source7StartLo lo))(24 (= p14Source8StartHi hi) (= p14Source8StartLo lo))(25 (= p14Source9StartHi hi) (= p14Source9StartLo lo))(26 (= p14Source10StartHi hi) (= p14Source10StartLo lo))(27 (= p14Source11StartHi hi) (= p14Source11StartLo lo))(28 (= p14Source12StartHi hi) (= p14Source12StartLo lo))(29 (= p14Source13StartHi hi) (= p14Source13StartLo lo))(30 (= p14Source14StartHi hi) (= p14Source14StartLo lo))(31 (= p14Source15StartHi hi) (= p14Source15StartLo lo))))(2 (switch slot (32 (= p14Source16StartHi hi) (= p14Source16StartLo lo))(33 (= p14Source17StartHi hi) (= p14Source17StartLo lo))(34 (= p14Source18StartHi hi) (= p14Source18StartLo lo))(35 (= p14Source19StartHi hi) (= p14Source19StartLo lo))(36 (= p14Source20StartHi hi) (= p14Source20StartLo lo))(37 (= p14Source21StartHi hi) (= p14Source21StartLo lo))(38 (= p14Source22StartHi hi) (= p14Source22StartLo lo))(39 (= p14Source23StartHi hi) (= p14Source23StartLo lo))(40 (= p14Source24StartHi hi) (= p14Source24StartLo lo))(41 (= p14Source25StartHi hi) (= p14Source25StartLo lo))(42 (= p14Source26StartHi hi) (= p14Source26StartLo lo))(43 (= p14Source27StartHi hi) (= p14Source27StartLo lo))(44 (= p14Source28StartHi hi) (= p14Source28StartLo lo))(45 (= p14Source29StartHi hi) (= p14Source29StartLo lo))(46 (= p14Source30StartHi hi) (= p14Source30StartLo lo))(47 (= p14Source31StartHi hi) (= p14Source31StartLo lo))))(3 (switch slot (48 (= p14Source32StartHi hi) (= p14Source32StartLo lo))(49 (= p14Source33StartHi hi) (= p14Source33StartLo lo))(50 (= p14Source34StartHi hi) (= p14Source34StartLo lo))(51 (= p14Source35StartHi hi) (= p14Source35StartLo lo))(52 (= p14Source36StartHi hi) (= p14Source36StartLo lo))(53 (= p14Source37StartHi hi) (= p14Source37StartLo lo))(54 (= p14Source38StartHi hi) (= p14Source38StartLo lo))(55 (= p14Source39StartHi hi) (= p14Source39StartLo lo))(56 (= p14Source40StartHi hi) (= p14Source40StartLo lo))(57 (= p14Source41StartHi hi) (= p14Source41StartLo lo))(58 (= p14Source42StartHi hi) (= p14Source42StartLo lo))(59 (= p14Source43StartHi hi) (= p14Source43StartLo lo))(60 (= p14Source44StartHi hi) (= p14Source44StartLo lo))(61 (= p14Source45StartHi hi) (= p14Source45StartLo lo))(62 (= p14Source46StartHi hi) (= p14Source46StartLo lo))(63 (= p14Source47StartHi hi) (= p14Source47StartLo lo))))(4 (switch slot (64 (= p14Source48StartHi hi) (= p14Source48StartLo lo))(65 (= p14Source49StartHi hi) (= p14Source49StartLo lo))(66 (= p14Source50StartHi hi) (= p14Source50StartLo lo))(67 (= p14Source51StartHi hi) (= p14Source51StartLo lo))(68 (= p14Source52StartHi hi) (= p14Source52StartLo lo))(69 (= p14Source53StartHi hi) (= p14Source53StartLo lo))(70 (= p14Source54StartHi hi) (= p14Source54StartLo lo))(71 (= p14Source55StartHi hi) (= p14Source55StartLo lo))(72 (= p14Source56StartHi hi) (= p14Source56StartLo lo))(73 (= p14Source57StartHi hi) (= p14Source57StartLo lo))(74 (= p14Source58StartHi hi) (= p14Source58StartLo lo))(75 (= p14Source59StartHi hi) (= p14Source59StartLo lo))(76 (= p14Source60StartHi hi) (= p14Source60StartLo lo))(77 (= p14Source61StartHi hi) (= p14Source61StartLo lo))(78 (= p14Source62StartHi hi) (= p14Source62StartLo lo))(79 (= p14Source63StartHi hi) (= p14Source63StartLo lo))))(5 (switch slot (80 (= p14Source64StartHi hi) (= p14Source64StartLo lo))(81 (= p14Source65StartHi hi) (= p14Source65StartLo lo))(82 (= p14Source66StartHi hi) (= p14Source66StartLo lo))(83 (= p14Source67StartHi hi) (= p14Source67StartLo lo))(84 (= p14Source68StartHi hi) (= p14Source68StartLo lo))(85 (= p14Source69StartHi hi) (= p14Source69StartLo lo))(86 (= p14Source70StartHi hi) (= p14Source70StartLo lo))(87 (= p14Source71StartHi hi) (= p14Source71StartLo lo))(88 (= p14Source72StartHi hi) (= p14Source72StartLo lo))(89 (= p14Source73StartHi hi) (= p14Source73StartLo lo))(90 (= p14Source74StartHi hi) (= p14Source74StartLo lo))(91 (= p14Source75StartHi hi) (= p14Source75StartLo lo))(92 (= p14Source76StartHi hi) (= p14Source76StartLo lo))(93 (= p14Source77StartHi hi) (= p14Source77StartLo lo))(94 (= p14Source78StartHi hi) (= p14Source78StartLo lo))(95 (= p14Source79StartHi hi) (= p14Source79StartLo lo))))(6 (switch slot (96 (= p14Source80StartHi hi) (= p14Source80StartLo lo))(97 (= p14Source81StartHi hi) (= p14Source81StartLo lo))(98 (= p14Source82StartHi hi) (= p14Source82StartLo lo))(99 (= p14Source83StartHi hi) (= p14Source83StartLo lo))(100 (= p14Source84StartHi hi) (= p14Source84StartLo lo))(101 (= p14Source85StartHi hi) (= p14Source85StartLo lo))(102 (= p14Source86StartHi hi) (= p14Source86StartLo lo))(103 (= p14Source87StartHi hi) (= p14Source87StartLo lo))(104 (= p14Source1Receipt1Hi hi) (= p14Source1Receipt1Lo lo))(105 (= p14Source1Receipt2Hi hi) (= p14Source1Receipt2Lo lo))(106 (= p14Source1Receipt3Hi hi) (= p14Source1Receipt3Lo lo))(107 (= p14Source2Receipt1Hi hi) (= p14Source2Receipt1Lo lo))(108 (= p14Source3Receipt1Hi hi) (= p14Source3Receipt1Lo lo))(109 (= p14Source4Receipt1Hi hi) (= p14Source4Receipt1Lo lo))(110 (= p14Source5Receipt1Hi hi) (= p14Source5Receipt1Lo lo))(111 (= p14Source6Receipt1Hi hi) (= p14Source6Receipt1Lo lo))))(7 (switch slot (112 (= p14Source7Receipt1Hi hi) (= p14Source7Receipt1Lo lo))(113 (= p14Source8Receipt1Hi hi) (= p14Source8Receipt1Lo lo))(114 (= p14Source9Receipt1Hi hi) (= p14Source9Receipt1Lo lo))(115 (= p14Source10Receipt1Hi hi) (= p14Source10Receipt1Lo lo))(116 (= p14Source11Receipt1Hi hi) (= p14Source11Receipt1Lo lo))(117 (= p14Source12Receipt1Hi hi) (= p14Source12Receipt1Lo lo))(118 (= p14Source13Receipt1Hi hi) (= p14Source13Receipt1Lo lo))(119 (= p14Source14Receipt1Hi hi) (= p14Source14Receipt1Lo lo))(120 (= p14Source15Receipt1Hi hi) (= p14Source15Receipt1Lo lo))(121 (= p14Source16Receipt1Hi hi) (= p14Source16Receipt1Lo lo))(122 (= p14Source17Receipt1Hi hi) (= p14Source17Receipt1Lo lo))(123 (= p14Source18Receipt1Hi hi) (= p14Source18Receipt1Lo lo))(124 (= p14Source19Receipt1Hi hi) (= p14Source19Receipt1Lo lo))(125 (= p14Source20Receipt1Hi hi) (= p14Source20Receipt1Lo lo))(126 (= p14Source20Receipt2Hi hi) (= p14Source20Receipt2Lo lo))(127 (= p14Source20Receipt3Hi hi) (= p14Source20Receipt3Lo lo))))(8 (switch slot (128 (= p14Source20Receipt4Hi hi) (= p14Source20Receipt4Lo lo))(129 (= p14Source20Receipt5Hi hi) (= p14Source20Receipt5Lo lo))(130 (= p14Source21Receipt1Hi hi) (= p14Source21Receipt1Lo lo))(131 (= p14Source22Receipt1Hi hi) (= p14Source22Receipt1Lo lo))(132 (= p14Source23Receipt1Hi hi) (= p14Source23Receipt1Lo lo))(133 (= p14Source24Receipt1Hi hi) (= p14Source24Receipt1Lo lo))(134 (= p14Source25Receipt1Hi hi) (= p14Source25Receipt1Lo lo))(135 (= p14Source26Receipt1Hi hi) (= p14Source26Receipt1Lo lo))(136 (= p14Source27Receipt1Hi hi) (= p14Source27Receipt1Lo lo))(137 (= p14Source27Receipt2Hi hi) (= p14Source27Receipt2Lo lo))(138 (= p14Source27Receipt3Hi hi) (= p14Source27Receipt3Lo lo))(139 (= p14Source27Receipt4Hi hi) (= p14Source27Receipt4Lo lo))(140 (= p14Source27Receipt5Hi hi) (= p14Source27Receipt5Lo lo))(141 (= p14Source28Receipt1Hi hi) (= p14Source28Receipt1Lo lo))(142 (= p14Source28Receipt2Hi hi) (= p14Source28Receipt2Lo lo))(143 (= p14Source29Receipt1Hi hi) (= p14Source29Receipt1Lo lo))))(9 (switch slot (144 (= p14Source30Receipt1Hi hi) (= p14Source30Receipt1Lo lo))(145 (= p14Source31Receipt1Hi hi) (= p14Source31Receipt1Lo lo))(146 (= p14Source32Receipt1Hi hi) (= p14Source32Receipt1Lo lo))(147 (= p14Source33Receipt1Hi hi) (= p14Source33Receipt1Lo lo))(148 (= p14Source34Receipt1Hi hi) (= p14Source34Receipt1Lo lo))(149 (= p14Source35Receipt1Hi hi) (= p14Source35Receipt1Lo lo))(150 (= p14Source36Receipt1Hi hi) (= p14Source36Receipt1Lo lo))(151 (= p14Source37Receipt1Hi hi) (= p14Source37Receipt1Lo lo))(152 (= p14Source38Receipt1Hi hi) (= p14Source38Receipt1Lo lo))(153 (= p14Source39Receipt1Hi hi) (= p14Source39Receipt1Lo lo))(154 (= p14Source40Receipt1Hi hi) (= p14Source40Receipt1Lo lo))(155 (= p14Source41Receipt1Hi hi) (= p14Source41Receipt1Lo lo))(156 (= p14Source42Receipt1Hi hi) (= p14Source42Receipt1Lo lo))(157 (= p14Source43Receipt1Hi hi) (= p14Source43Receipt1Lo lo))(158 (= p14Source44Receipt1Hi hi) (= p14Source44Receipt1Lo lo))(159 (= p14Source45Receipt1Hi hi) (= p14Source45Receipt1Lo lo))))(10 (switch slot (160 (= p14Source46Receipt1Hi hi) (= p14Source46Receipt1Lo lo))(161 (= p14Source47Receipt1Hi hi) (= p14Source47Receipt1Lo lo))(162 (= p14Source48Receipt1Hi hi) (= p14Source48Receipt1Lo lo))(163 (= p14Source49Receipt1Hi hi) (= p14Source49Receipt1Lo lo))(164 (= p14Source50Receipt1Hi hi) (= p14Source50Receipt1Lo lo))(165 (= p14Source51Receipt1Hi hi) (= p14Source51Receipt1Lo lo))(166 (= p14Source52Receipt1Hi hi) (= p14Source52Receipt1Lo lo))(167 (= p14Source53Receipt1Hi hi) (= p14Source53Receipt1Lo lo))(168 (= p14Source54Receipt1Hi hi) (= p14Source54Receipt1Lo lo))(169 (= p14Source55Receipt1Hi hi) (= p14Source55Receipt1Lo lo))(170 (= p14Source56Receipt1Hi hi) (= p14Source56Receipt1Lo lo))(171 (= p14Source57Receipt1Hi hi) (= p14Source57Receipt1Lo lo))(172 (= p14Source58Receipt1Hi hi) (= p14Source58Receipt1Lo lo))(173 (= p14Source59Receipt1Hi hi) (= p14Source59Receipt1Lo lo))(174 (= p14Source60Receipt1Hi hi) (= p14Source60Receipt1Lo lo))(175 (= p14Source61Receipt1Hi hi) (= p14Source61Receipt1Lo lo))))(11 (switch slot (176 (= p14Source62Receipt1Hi hi) (= p14Source62Receipt1Lo lo))(177 (= p14Source63Receipt1Hi hi) (= p14Source63Receipt1Lo lo))(178 (= p14Source64Receipt1Hi hi) (= p14Source64Receipt1Lo lo))(179 (= p14Source65Receipt1Hi hi) (= p14Source65Receipt1Lo lo))(180 (= p14Source66Receipt1Hi hi) (= p14Source66Receipt1Lo lo))(181 (= p14Source67Receipt1Hi hi) (= p14Source67Receipt1Lo lo))(182 (= p14Source68Receipt1Hi hi) (= p14Source68Receipt1Lo lo))(183 (= p14Source69Receipt1Hi hi) (= p14Source69Receipt1Lo lo))(184 (= p14Source70Receipt1Hi hi) (= p14Source70Receipt1Lo lo))(185 (= p14Source71Receipt1Hi hi) (= p14Source71Receipt1Lo lo))(186 (= p14Source72Receipt1Hi hi) (= p14Source72Receipt1Lo lo))(187 (= p14Source73Receipt1Hi hi) (= p14Source73Receipt1Lo lo))(188 (= p14Source74Receipt1Hi hi) (= p14Source74Receipt1Lo lo))(189 (= p14Source75Receipt1Hi hi) (= p14Source75Receipt1Lo lo))(190 (= p14Source76Receipt1Hi hi) (= p14Source76Receipt1Lo lo))(191 (= p14Source77Receipt1Hi hi) (= p14Source77Receipt1Lo lo))))(12 (switch slot (192 (= p14Source78Receipt1Hi hi) (= p14Source78Receipt1Lo lo))(193 (= p14Source79Receipt1Hi hi) (= p14Source79Receipt1Lo lo))(194 (= p14Source80Receipt1Hi hi) (= p14Source80Receipt1Lo lo))(195 (= p14Source81Receipt1Hi hi) (= p14Source81Receipt1Lo lo))(196 (= p14Source82Receipt1Hi hi) (= p14Source82Receipt1Lo lo))(197 (= p14Source83Receipt1Hi hi) (= p14Source83Receipt1Lo lo))(198 (= p14Source84Receipt1Hi hi) (= p14Source84Receipt1Lo lo))(199 (= p14Source85Receipt1Hi hi) (= p14Source85Receipt1Lo lo))(200 (= p14Source86Receipt1Hi hi) (= p14Source86Receipt1Lo lo))(201 (= p14Source87Receipt1Hi hi) (= p14Source87Receipt1Lo lo))))) (return 1))
(method (p14Capacity source &tmp answer) (= answer 0) (switch (/ source 16) (0 (switch source (1 (= answer 3))(2 (= answer 1))(3 (= answer 1))(4 (= answer 1))(5 (= answer 1))(6 (= answer 1))(7 (= answer 1))(8 (= answer 1))(9 (= answer 1))(10 (= answer 1))(11 (= answer 1))(12 (= answer 1))(13 (= answer 1))(14 (= answer 1))(15 (= answer 1))))(1 (switch source (16 (= answer 1))(17 (= answer 1))(18 (= answer 1))(19 (= answer 1))(20 (= answer 5))(21 (= answer 1))(22 (= answer 1))(23 (= answer 1))(24 (= answer 1))(25 (= answer 1))(26 (= answer 1))(27 (= answer 5))(28 (= answer 2))(29 (= answer 1))(30 (= answer 1))(31 (= answer 1))))(2 (switch source (32 (= answer 1))(33 (= answer 1))(34 (= answer 1))(35 (= answer 1))(36 (= answer 1))(37 (= answer 1))(38 (= answer 1))(39 (= answer 1))(40 (= answer 1))(41 (= answer 1))(42 (= answer 1))(43 (= answer 1))(44 (= answer 1))(45 (= answer 1))(46 (= answer 1))(47 (= answer 1))))(3 (switch source (48 (= answer 1))(49 (= answer 1))(50 (= answer 1))(51 (= answer 1))(52 (= answer 1))(53 (= answer 1))(54 (= answer 1))(55 (= answer 1))(56 (= answer 1))(57 (= answer 1))(58 (= answer 1))(59 (= answer 1))(60 (= answer 1))(61 (= answer 1))(62 (= answer 1))(63 (= answer 1))))(4 (switch source (64 (= answer 1))(65 (= answer 1))(66 (= answer 1))(67 (= answer 1))(68 (= answer 1))(69 (= answer 1))(70 (= answer 1))(71 (= answer 1))(72 (= answer 1))(73 (= answer 1))(74 (= answer 1))(75 (= answer 1))(76 (= answer 1))(77 (= answer 1))(78 (= answer 1))(79 (= answer 1))))(5 (switch source (80 (= answer 1))(81 (= answer 1))(82 (= answer 1))(83 (= answer 1))(84 (= answer 1))(85 (= answer 1))(86 (= answer 1))(87 (= answer 1))))) (return answer))
(method (p14ReceiptBase source &tmp answer) (= answer 0) (switch (/ source 16) (0 (switch source (1 (= answer 104))(2 (= answer 107))(3 (= answer 108))(4 (= answer 109))(5 (= answer 110))(6 (= answer 111))(7 (= answer 112))(8 (= answer 113))(9 (= answer 114))(10 (= answer 115))(11 (= answer 116))(12 (= answer 117))(13 (= answer 118))(14 (= answer 119))(15 (= answer 120))))(1 (switch source (16 (= answer 121))(17 (= answer 122))(18 (= answer 123))(19 (= answer 124))(20 (= answer 125))(21 (= answer 130))(22 (= answer 131))(23 (= answer 132))(24 (= answer 133))(25 (= answer 134))(26 (= answer 135))(27 (= answer 136))(28 (= answer 141))(29 (= answer 143))(30 (= answer 144))(31 (= answer 145))))(2 (switch source (32 (= answer 146))(33 (= answer 147))(34 (= answer 148))(35 (= answer 149))(36 (= answer 150))(37 (= answer 151))(38 (= answer 152))(39 (= answer 153))(40 (= answer 154))(41 (= answer 155))(42 (= answer 156))(43 (= answer 157))(44 (= answer 158))(45 (= answer 159))(46 (= answer 160))(47 (= answer 161))))(3 (switch source (48 (= answer 162))(49 (= answer 163))(50 (= answer 164))(51 (= answer 165))(52 (= answer 166))(53 (= answer 167))(54 (= answer 168))(55 (= answer 169))(56 (= answer 170))(57 (= answer 171))(58 (= answer 172))(59 (= answer 173))(60 (= answer 174))(61 (= answer 175))(62 (= answer 176))(63 (= answer 177))))(4 (switch source (64 (= answer 178))(65 (= answer 179))(66 (= answer 180))(67 (= answer 181))(68 (= answer 182))(69 (= answer 183))(70 (= answer 184))(71 (= answer 185))(72 (= answer 186))(73 (= answer 187))(74 (= answer 188))(75 (= answer 189))(76 (= answer 190))(77 (= answer 191))(78 (= answer 192))(79 (= answer 193))))(5 (switch source (80 (= answer 194))(81 (= answer 195))(82 (= answer 196))(83 (= answer 197))(84 (= answer 198))(85 (= answer 199))(86 (= answer 200))(87 (= answer 201))))) (return answer))
(method (p14SourceRecord source &tmp answer) (= answer 0) (switch (/ source 16) (0 (switch source (1 (= answer 1))(2 (= answer 4))(3 (= answer 8))(4 (= answer 12))(5 (= answer 16))(6 (= answer 20))(7 (= answer 24))(8 (= answer 28))(9 (= answer 32))(10 (= answer 2))(11 (= answer 6))(12 (= answer 10))(13 (= answer 14))(14 (= answer 18))(15 (= answer 22))))(1 (switch source (16 (= answer 26))(17 (= answer 30))(18 (= answer 37))(19 (= answer 39))(20 (= answer 41))(21 (= answer 44))(22 (= answer 45))(23 (= answer 46))(24 (= answer 47))(25 (= answer 48))(26 (= answer 49))(27 (= answer 50))(28 (= answer 51))(29 (= answer 60))(30 (= answer 61))(31 (= answer 62))))(2 (switch source (32 (= answer 63))(33 (= answer 64))(34 (= answer 65))(35 (= answer 66))(36 (= answer 67))(37 (= answer 68))(38 (= answer 69))(39 (= answer 70))(40 (= answer 71))(41 (= answer 72))(42 (= answer 73))(43 (= answer 74))(44 (= answer 75))(45 (= answer 76))(46 (= answer 77))(47 (= answer 78))))(3 (switch source (48 (= answer 79))(49 (= answer 80))(50 (= answer 81))(51 (= answer 82))(52 (= answer 83))(53 (= answer 84))(54 (= answer 85))(55 (= answer 93))(56 (= answer 94))(57 (= answer 95))(58 (= answer 96))(59 (= answer 97))(60 (= answer 98))(61 (= answer 99))(62 (= answer 100))(63 (= answer 101))))(4 (switch source (64 (= answer 102))(65 (= answer 103))(66 (= answer 104))(67 (= answer 105))(68 (= answer 106))(69 (= answer 107))(70 (= answer 108))(71 (= answer 109))(72 (= answer 110))(73 (= answer 111))(74 (= answer 112))(75 (= answer 113))(76 (= answer 114))(77 (= answer 115))(78 (= answer 116))(79 (= answer 117))))(5 (switch source (80 (= answer 118))(81 (= answer 119))(82 (= answer 120))(83 (= answer 121))(84 (= answer 122))(85 (= answer 123))(86 (= answer 124))(87 (= answer 125))))) (return answer))
(method (p14Token source index &tmp answer) (= answer 0) (switch source
 (1 (switch index  (0 (= answer 1)) (1 (= answer 2)) (2 (= answer 3))))
 (2 (switch index  (0 (= answer 4))))
 (3 (switch index  (0 (= answer 5))))
 (4 (switch index  (0 (= answer 6))))
 (5 (switch index  (0 (= answer 7))))
 (6 (switch index  (0 (= answer 8))))
 (7 (switch index  (0 (= answer 9))))
 (8 (switch index  (0 (= answer 10))))
 (9 (switch index  (0 (= answer 11))))
 (10 (switch index  (0 (= answer 12))))
 (11 (switch index  (0 (= answer 13))))
 (12 (switch index  (0 (= answer 14))))
 (13 (switch index  (0 (= answer 15))))
 (14 (switch index  (0 (= answer 16))))
 (15 (switch index  (0 (= answer 17))))
 (16 (switch index  (0 (= answer 18))))
 (17 (switch index  (0 (= answer 19))))
 (18 (switch index  (0 (= answer 20))))
 (19 (switch index  (0 (= answer 21))))
 (20 (switch index  (0 (= answer 22)) (1 (= answer 23)) (2 (= answer 24)) (3 (= answer 25)) (4 (= answer 26))))
 (21 (switch index  (0 (= answer 27))))
 (22 (switch index  (0 (= answer 28))))
 (23 (switch index  (0 (= answer 29))))
 (24 (switch index  (0 (= answer 30))))
 (25 (switch index  (0 (= answer 31))))
 (26 (switch index  (0 (= answer 32))))
 (27 (switch index  (0 (= answer 33)) (1 (= answer 34)) (2 (= answer 35)) (3 (= answer 36)) (4 (= answer 37))))
 (28 (switch index  (0 (= answer 38)) (1 (= answer 39))))
 (29 (switch index  (0 (= answer 40))))
 (30 (switch index  (0 (= answer 41))))
 (31 (switch index  (0 (= answer 42))))
 (32 (switch index  (0 (= answer 43))))
 (33 (switch index  (0 (= answer 44))))
 (34 (switch index  (0 (= answer 45))))
 (35 (switch index  (0 (= answer 46))))
 (36 (switch index  (0 (= answer 47))))
 (37 (switch index  (0 (= answer 48))))
 (38 (switch index  (0 (= answer 49))))
 (39 (switch index  (0 (= answer 50))))
 (40 (switch index  (0 (= answer 51))))
 (41 (switch index  (0 (= answer 52))))
 (42 (switch index  (0 (= answer 53))))
 (43 (switch index  (0 (= answer 54))))
 (44 (switch index  (0 (= answer 55))))
 (45 (switch index  (0 (= answer 56))))
 (46 (switch index  (0 (= answer 57))))
 (47 (switch index  (0 (= answer 58))))
 (48 (switch index  (0 (= answer 59))))
 (49 (switch index  (0 (= answer 60))))
 (50 (switch index  (0 (= answer 61))))
 (51 (switch index  (0 (= answer 62))))
 (52 (switch index  (0 (= answer 63))))
 (53 (switch index  (0 (= answer 64))))
 (54 (switch index  (0 (= answer 65))))
 (55 (switch index  (0 (= answer 66))))
 (56 (switch index  (0 (= answer 67))))
 (57 (switch index  (0 (= answer 68))))
 (58 (switch index  (0 (= answer 69))))
 (59 (switch index  (0 (= answer 70))))
 (60 (switch index  (0 (= answer 71))))
 (61 (switch index  (0 (= answer 72))))
 (62 (switch index  (0 (= answer 73))))
 (63 (switch index  (0 (= answer 74))))
 (64 (switch index  (0 (= answer 75))))
 (65 (switch index  (0 (= answer 76))))
 (66 (switch index  (0 (= answer 77))))
 (67 (switch index  (0 (= answer 78))))
 (68 (switch index  (0 (= answer 79))))
 (69 (switch index  (0 (= answer 80))))
 (70 (switch index  (0 (= answer 81))))
 (71 (switch index  (0 (= answer 82))))
 (72 (switch index  (0 (= answer 83))))
 (73 (switch index  (0 (= answer 84))))
 (74 (switch index  (0 (= answer 85))))
 (75 (switch index  (0 (= answer 86))))
 (76 (switch index  (0 (= answer 87))))
 (77 (switch index  (0 (= answer 88))))
 (78 (switch index  (0 (= answer 89))))
 (79 (switch index  (0 (= answer 90))))
 (80 (switch index  (0 (= answer 91))))
 (81 (switch index  (0 (= answer 92))))
 (82 (switch index  (0 (= answer 93))))
 (83 (switch index  (0 (= answer 94))))
 (84 (switch index  (0 (= answer 95))))
 (85 (switch index  (0 (= answer 96))))
 (86 (switch index  (0 (= answer 97))))
 (87 (switch index  (0 (= answer 98))))
) (return answer))
(method (p14TokenUnit token &tmp answer) (= answer 0) (switch (/ token 16) (0 (switch token (1 (= answer 1))(2 (= answer 2))(3 (= answer 3))(4 (= answer 4))(5 (= answer 6))(6 (= answer 8))(7 (= answer 10))(8 (= answer 12))(9 (= answer 14))(10 (= answer 16))(11 (= answer 18))(12 (= answer 0))(13 (= answer 0))(14 (= answer 0))(15 (= answer 0))))(1 (switch token (16 (= answer 0))(17 (= answer 0))(18 (= answer 0))(19 (= answer 0))(20 (= answer 22))(21 (= answer 23))(22 (= answer 24))(23 (= answer 25))(24 (= answer 26))(25 (= answer 27))(26 (= answer 28))(27 (= answer 31))(28 (= answer 32))(29 (= answer 33))(30 (= answer 34))(31 (= answer 35))))(2 (switch token (32 (= answer 36))(33 (= answer 37))(34 (= answer 38))(35 (= answer 39))(36 (= answer 40))(37 (= answer 41))(38 (= answer 42))(39 (= answer 43))(40 (= answer 0))(41 (= answer 0))(42 (= answer 0))(43 (= answer 0))(44 (= answer 0))(45 (= answer 0))(46 (= answer 0))(47 (= answer 0))))(3 (switch token (48 (= answer 0))(49 (= answer 0))(50 (= answer 0))(51 (= answer 0))(52 (= answer 0))(53 (= answer 0))(54 (= answer 0))(55 (= answer 0))(56 (= answer 0))(57 (= answer 0))(58 (= answer 0))(59 (= answer 0))(60 (= answer 0))(61 (= answer 0))(62 (= answer 0))(63 (= answer 0))))(4 (switch token (64 (= answer 0))(65 (= answer 0))(66 (= answer 0))(67 (= answer 0))(68 (= answer 0))(69 (= answer 0))(70 (= answer 0))(71 (= answer 0))(72 (= answer 0))(73 (= answer 0))(74 (= answer 0))(75 (= answer 0))(76 (= answer 0))(77 (= answer 0))(78 (= answer 0))(79 (= answer 0))))(5 (switch token (80 (= answer 0))(81 (= answer 0))(82 (= answer 0))(83 (= answer 0))(84 (= answer 0))(85 (= answer 0))(86 (= answer 0))(87 (= answer 0))(88 (= answer 0))(89 (= answer 0))(90 (= answer 0))(91 (= answer 0))(92 (= answer 0))(93 (= answer 0))(94 (= answer 0))(95 (= answer 0))))(6 (switch token (96 (= answer 0))(97 (= answer 0))(98 (= answer 0))))) (return answer))
(method (p14TokenSpeaker token &tmp answer) (= answer 0) (switch (/ token 16) (0 (switch token (1 (= answer 8))(2 (= answer 57))(3 (= answer 8))(4 (= answer 57))(5 (= answer 2))(6 (= answer 8))(7 (= answer 28))(8 (= answer 61))(9 (= answer 30))(10 (= answer 54))(11 (= answer 29))(12 (= answer 0))(13 (= answer 0))(14 (= answer 0))(15 (= answer 0))))(1 (switch token (16 (= answer 0))(17 (= answer 0))(18 (= answer 0))(19 (= answer 0))(20 (= answer 57))(21 (= answer 57))(22 (= answer 29))(23 (= answer 57))(24 (= answer 29))(25 (= answer 8))(26 (= answer 29))(27 (= answer 8))(28 (= answer 8))(29 (= answer 8))(30 (= answer 61))(31 (= answer 61))))(2 (switch token (32 (= answer 61))(33 (= answer 2))(34 (= answer 57))(35 (= answer 2))(36 (= answer 8))(37 (= answer 57))(38 (= answer 28))(39 (= answer 57))(40 (= answer 0))(41 (= answer 0))(42 (= answer 0))(43 (= answer 0))(44 (= answer 0))(45 (= answer 0))(46 (= answer 0))(47 (= answer 0))))(3 (switch token (48 (= answer 0))(49 (= answer 0))(50 (= answer 0))(51 (= answer 0))(52 (= answer 0))(53 (= answer 0))(54 (= answer 0))(55 (= answer 0))(56 (= answer 0))(57 (= answer 0))(58 (= answer 0))(59 (= answer 0))(60 (= answer 0))(61 (= answer 0))(62 (= answer 0))(63 (= answer 0))))(4 (switch token (64 (= answer 0))(65 (= answer 0))(66 (= answer 0))(67 (= answer 0))(68 (= answer 0))(69 (= answer 0))(70 (= answer 0))(71 (= answer 0))(72 (= answer 0))(73 (= answer 0))(74 (= answer 0))(75 (= answer 0))(76 (= answer 0))(77 (= answer 0))(78 (= answer 0))(79 (= answer 0))))(5 (switch token (80 (= answer 0))(81 (= answer 0))(82 (= answer 0))(83 (= answer 0))(84 (= answer 0))(85 (= answer 0))(86 (= answer 0))(87 (= answer 0))(88 (= answer 0))(89 (= answer 0))(90 (= answer 0))(91 (= answer 0))(92 (= answer 0))(93 (= answer 0))(94 (= answer 0))(95 (= answer 0))))(6 (switch token (96 (= answer 0))(97 (= answer 0))(98 (= answer 0))))) (return answer))
(method (p14ActorRoom obj &tmp answer) (= answer -1) (switch obj (2 (= answer p14BunnyRoom))(8 (= answer p14FrankieRoom))(28 (= answer p14MiloRoom))(61 (= answer p14VivianRoom))(30 (= answer p14RitaRoom))(54 (= answer p14FelixRoom))(29 (= answer p14StringerRoom))) (return answer))
(method (p14RematchRoom index &tmp answer) (= answer -1) (switch index (0 (= answer 5))(1 (= answer 0))(2 (= answer 3))(3 (= answer 4))) (return answer))
(method (p14Person index &tmp answer) (= answer 0) (switch index (0 (= answer 57))(1 (= answer 2))(2 (= answer 8))(3 (= answer 28))(4 (= answer 61))(5 (= answer 30))(6 (= answer 54))(7 (= answer 29))) (return answer))
(method (p14PersonIndex obj &tmp answer) (= answer -1) (switch obj (57 (= answer 0))(2 (= answer 1))(8 (= answer 2))(28 (= answer 3))(61 (= answer 4))(30 (= answer 5))(54 (= answer 6))(29 (= answer 7))) (return answer))
(method (p14Card index &tmp answer) (= answer 0) (switch index (0 (= answer 435))(1 (= answer 436))(2 (= answer 437))(3 (= answer 438))(4 (= answer 439))(5 (= answer 440))(6 (= answer 441))(7 (= answer 442))) (return answer))
(method (p14CardIndex obj &tmp answer) (= answer -1) (switch obj (435 (= answer 0))(436 (= answer 1))(437 (= answer 2))(438 (= answer 3))(439 (= answer 4))(440 (= answer 5))(441 (= answer 6))(442 (= answer 7))) (return answer))
(method (p14CreditAt index &tmp answer) (= answer 0) (switch (/ index 16) (0 (switch index (0 (= answer p14Credit0))(1 (= answer p14Credit1))(2 (= answer p14Credit2))(3 (= answer p14Credit3))(4 (= answer p14Credit4))(5 (= answer p14Credit5))(6 (= answer p14Credit6))(7 (= answer p14Credit7))(8 (= answer p14Credit8))(9 (= answer p14Credit9))(10 (= answer p14Credit10))(11 (= answer p14Credit11))(12 (= answer p14Credit12))(13 (= answer p14Credit13))(14 (= answer p14Credit14))(15 (= answer p14Credit15))))(1 (switch index (16 (= answer p14Credit16))(17 (= answer p14Credit17))(18 (= answer p14Credit18))(19 (= answer p14Credit19))(20 (= answer p14Credit20))(21 (= answer p14Credit21))(22 (= answer p14Credit22))(23 (= answer p14Credit23))(24 (= answer p14Credit24))(25 (= answer p14Credit25))(26 (= answer p14Credit26))(27 (= answer p14Credit27))(28 (= answer p14Credit28))(29 (= answer p14Credit29))(30 (= answer p14Credit30))(31 (= answer p14Credit31))))(2 (switch index (32 (= answer p14Credit32))(33 (= answer p14Credit33))(34 (= answer p14Credit34))(35 (= answer p14Credit35))(36 (= answer p14Credit36))(37 (= answer p14Credit37))(38 (= answer p14Credit38))(39 (= answer p14Credit39))(40 (= answer p14Credit40))(41 (= answer p14Credit41))(42 (= answer p14Credit42))(43 (= answer p14Credit43))(44 (= answer p14Credit44))(45 (= answer p14Credit45))(46 (= answer p14Credit46))(47 (= answer p14Credit47))))(3 (switch index (48 (= answer p14Credit48))(49 (= answer p14Credit49))(50 (= answer p14Credit50))(51 (= answer p14Credit51))(52 (= answer p14Credit52))(53 (= answer p14Credit53))(54 (= answer p14Credit54))(55 (= answer p14Credit55))(56 (= answer p14Credit56))(57 (= answer p14Credit57))(58 (= answer p14Credit58))))) (return answer))
(method (p14SetCredit index value) (switch (/ index 16) (0 (switch index (0 (= p14Credit0 value))(1 (= p14Credit1 value))(2 (= p14Credit2 value))(3 (= p14Credit3 value))(4 (= p14Credit4 value))(5 (= p14Credit5 value))(6 (= p14Credit6 value))(7 (= p14Credit7 value))(8 (= p14Credit8 value))(9 (= p14Credit9 value))(10 (= p14Credit10 value))(11 (= p14Credit11 value))(12 (= p14Credit12 value))(13 (= p14Credit13 value))(14 (= p14Credit14 value))(15 (= p14Credit15 value))))(1 (switch index (16 (= p14Credit16 value))(17 (= p14Credit17 value))(18 (= p14Credit18 value))(19 (= p14Credit19 value))(20 (= p14Credit20 value))(21 (= p14Credit21 value))(22 (= p14Credit22 value))(23 (= p14Credit23 value))(24 (= p14Credit24 value))(25 (= p14Credit25 value))(26 (= p14Credit26 value))(27 (= p14Credit27 value))(28 (= p14Credit28 value))(29 (= p14Credit29 value))(30 (= p14Credit30 value))(31 (= p14Credit31 value))))(2 (switch index (32 (= p14Credit32 value))(33 (= p14Credit33 value))(34 (= p14Credit34 value))(35 (= p14Credit35 value))(36 (= p14Credit36 value))(37 (= p14Credit37 value))(38 (= p14Credit38 value))(39 (= p14Credit39 value))(40 (= p14Credit40 value))(41 (= p14Credit41 value))(42 (= p14Credit42 value))(43 (= p14Credit43 value))(44 (= p14Credit44 value))(45 (= p14Credit45 value))(46 (= p14Credit46 value))(47 (= p14Credit47 value))))(3 (switch index (48 (= p14Credit48 value))(49 (= p14Credit49 value))(50 (= p14Credit50 value))(51 (= p14Credit51 value))(52 (= p14Credit52 value))(53 (= p14Credit53 value))(54 (= p14Credit54 value))(55 (= p14Credit55 value))(56 (= p14Credit56 value))(57 (= p14Credit57 value))(58 (= p14Credit58 value))))) (return 1))
(method (p14DateHiAt index &tmp answer) (= answer 0) (switch (/ index 16) (0 (switch index (0 (= answer p14Date0Hi))(1 (= answer p14Date1Hi))(2 (= answer p14Date2Hi))(3 (= answer p14Date3Hi))(4 (= answer p14Date4Hi))(5 (= answer p14Date5Hi))(6 (= answer p14Date6Hi))(7 (= answer p14Date7Hi))(8 (= answer p14Date8Hi))(9 (= answer p14Date9Hi))(10 (= answer p14Date10Hi))(11 (= answer p14Date11Hi))(12 (= answer p14Date12Hi))(13 (= answer p14Date13Hi))(14 (= answer p14Date14Hi))(15 (= answer p14Date15Hi))))(1 (switch index (16 (= answer p14Date16Hi))(17 (= answer p14Date17Hi))(18 (= answer p14Date18Hi))(19 (= answer p14Date19Hi))(20 (= answer p14Date20Hi))(21 (= answer p14Date21Hi))(22 (= answer p14Date22Hi))(23 (= answer p14Date23Hi))(24 (= answer p14Date24Hi))(25 (= answer p14Date25Hi))(26 (= answer p14Date26Hi))(27 (= answer p14Date27Hi))(28 (= answer p14Date28Hi))(29 (= answer p14Date29Hi))(30 (= answer p14Date30Hi))(31 (= answer p14Date31Hi))))(2 (switch index (32 (= answer p14Date32Hi))(33 (= answer p14Date33Hi))(34 (= answer p14Date34Hi))(35 (= answer p14Date35Hi))(36 (= answer p14Date36Hi))(37 (= answer p14Date37Hi))(38 (= answer p14Date38Hi))(39 (= answer p14Date39Hi))(40 (= answer p14Date40Hi))(41 (= answer p14Date41Hi))(42 (= answer p14Date42Hi))(43 (= answer p14Date43Hi))(44 (= answer p14Date44Hi))(45 (= answer p14Date45Hi))(46 (= answer p14Date46Hi))(47 (= answer p14Date47Hi))))(3 (switch index (48 (= answer p14Date48Hi))(49 (= answer p14Date49Hi))(50 (= answer p14Date50Hi))(51 (= answer p14Date51Hi))(52 (= answer p14Date52Hi))(53 (= answer p14Date53Hi))(54 (= answer p14Date54Hi))(55 (= answer p14Date55Hi))(56 (= answer p14Date56Hi))(57 (= answer p14Date57Hi))(58 (= answer p14Date58Hi))(59 (= answer p14Date59Hi))(60 (= answer p14Date60Hi))(61 (= answer p14Date61Hi))(62 (= answer p14Date62Hi))(63 (= answer p14Date63Hi))))(4 (switch index (64 (= answer p14Date64Hi))(65 (= answer p14Date65Hi))(66 (= answer p14Date66Hi))(67 (= answer p14Date67Hi))(68 (= answer p14Date68Hi))(69 (= answer p14Date69Hi))(70 (= answer p14Date70Hi))(71 (= answer p14Date71Hi))(72 (= answer p14Date72Hi))(73 (= answer p14Date73Hi))(74 (= answer p14Date74Hi))(75 (= answer p14Date75Hi))(76 (= answer p14Date76Hi))(77 (= answer p14Date77Hi))(78 (= answer p14Date78Hi))(79 (= answer p14Date79Hi))))) (return answer))
(method (p14SetDateHi index value) (switch (/ index 16) (0 (switch index (0 (= p14Date0Hi value))(1 (= p14Date1Hi value))(2 (= p14Date2Hi value))(3 (= p14Date3Hi value))(4 (= p14Date4Hi value))(5 (= p14Date5Hi value))(6 (= p14Date6Hi value))(7 (= p14Date7Hi value))(8 (= p14Date8Hi value))(9 (= p14Date9Hi value))(10 (= p14Date10Hi value))(11 (= p14Date11Hi value))(12 (= p14Date12Hi value))(13 (= p14Date13Hi value))(14 (= p14Date14Hi value))(15 (= p14Date15Hi value))))(1 (switch index (16 (= p14Date16Hi value))(17 (= p14Date17Hi value))(18 (= p14Date18Hi value))(19 (= p14Date19Hi value))(20 (= p14Date20Hi value))(21 (= p14Date21Hi value))(22 (= p14Date22Hi value))(23 (= p14Date23Hi value))(24 (= p14Date24Hi value))(25 (= p14Date25Hi value))(26 (= p14Date26Hi value))(27 (= p14Date27Hi value))(28 (= p14Date28Hi value))(29 (= p14Date29Hi value))(30 (= p14Date30Hi value))(31 (= p14Date31Hi value))))(2 (switch index (32 (= p14Date32Hi value))(33 (= p14Date33Hi value))(34 (= p14Date34Hi value))(35 (= p14Date35Hi value))(36 (= p14Date36Hi value))(37 (= p14Date37Hi value))(38 (= p14Date38Hi value))(39 (= p14Date39Hi value))(40 (= p14Date40Hi value))(41 (= p14Date41Hi value))(42 (= p14Date42Hi value))(43 (= p14Date43Hi value))(44 (= p14Date44Hi value))(45 (= p14Date45Hi value))(46 (= p14Date46Hi value))(47 (= p14Date47Hi value))))(3 (switch index (48 (= p14Date48Hi value))(49 (= p14Date49Hi value))(50 (= p14Date50Hi value))(51 (= p14Date51Hi value))(52 (= p14Date52Hi value))(53 (= p14Date53Hi value))(54 (= p14Date54Hi value))(55 (= p14Date55Hi value))(56 (= p14Date56Hi value))(57 (= p14Date57Hi value))(58 (= p14Date58Hi value))(59 (= p14Date59Hi value))(60 (= p14Date60Hi value))(61 (= p14Date61Hi value))(62 (= p14Date62Hi value))(63 (= p14Date63Hi value))))(4 (switch index (64 (= p14Date64Hi value))(65 (= p14Date65Hi value))(66 (= p14Date66Hi value))(67 (= p14Date67Hi value))(68 (= p14Date68Hi value))(69 (= p14Date69Hi value))(70 (= p14Date70Hi value))(71 (= p14Date71Hi value))(72 (= p14Date72Hi value))(73 (= p14Date73Hi value))(74 (= p14Date74Hi value))(75 (= p14Date75Hi value))(76 (= p14Date76Hi value))(77 (= p14Date77Hi value))(78 (= p14Date78Hi value))(79 (= p14Date79Hi value))))) (return 1))
(method (p14DateLoAt index &tmp answer) (= answer 0) (switch (/ index 16) (0 (switch index (0 (= answer p14Date0Lo))(1 (= answer p14Date1Lo))(2 (= answer p14Date2Lo))(3 (= answer p14Date3Lo))(4 (= answer p14Date4Lo))(5 (= answer p14Date5Lo))(6 (= answer p14Date6Lo))(7 (= answer p14Date7Lo))(8 (= answer p14Date8Lo))(9 (= answer p14Date9Lo))(10 (= answer p14Date10Lo))(11 (= answer p14Date11Lo))(12 (= answer p14Date12Lo))(13 (= answer p14Date13Lo))(14 (= answer p14Date14Lo))(15 (= answer p14Date15Lo))))(1 (switch index (16 (= answer p14Date16Lo))(17 (= answer p14Date17Lo))(18 (= answer p14Date18Lo))(19 (= answer p14Date19Lo))(20 (= answer p14Date20Lo))(21 (= answer p14Date21Lo))(22 (= answer p14Date22Lo))(23 (= answer p14Date23Lo))(24 (= answer p14Date24Lo))(25 (= answer p14Date25Lo))(26 (= answer p14Date26Lo))(27 (= answer p14Date27Lo))(28 (= answer p14Date28Lo))(29 (= answer p14Date29Lo))(30 (= answer p14Date30Lo))(31 (= answer p14Date31Lo))))(2 (switch index (32 (= answer p14Date32Lo))(33 (= answer p14Date33Lo))(34 (= answer p14Date34Lo))(35 (= answer p14Date35Lo))(36 (= answer p14Date36Lo))(37 (= answer p14Date37Lo))(38 (= answer p14Date38Lo))(39 (= answer p14Date39Lo))(40 (= answer p14Date40Lo))(41 (= answer p14Date41Lo))(42 (= answer p14Date42Lo))(43 (= answer p14Date43Lo))(44 (= answer p14Date44Lo))(45 (= answer p14Date45Lo))(46 (= answer p14Date46Lo))(47 (= answer p14Date47Lo))))(3 (switch index (48 (= answer p14Date48Lo))(49 (= answer p14Date49Lo))(50 (= answer p14Date50Lo))(51 (= answer p14Date51Lo))(52 (= answer p14Date52Lo))(53 (= answer p14Date53Lo))(54 (= answer p14Date54Lo))(55 (= answer p14Date55Lo))(56 (= answer p14Date56Lo))(57 (= answer p14Date57Lo))(58 (= answer p14Date58Lo))(59 (= answer p14Date59Lo))(60 (= answer p14Date60Lo))(61 (= answer p14Date61Lo))(62 (= answer p14Date62Lo))(63 (= answer p14Date63Lo))))(4 (switch index (64 (= answer p14Date64Lo))(65 (= answer p14Date65Lo))(66 (= answer p14Date66Lo))(67 (= answer p14Date67Lo))(68 (= answer p14Date68Lo))(69 (= answer p14Date69Lo))(70 (= answer p14Date70Lo))(71 (= answer p14Date71Lo))(72 (= answer p14Date72Lo))(73 (= answer p14Date73Lo))(74 (= answer p14Date74Lo))(75 (= answer p14Date75Lo))(76 (= answer p14Date76Lo))(77 (= answer p14Date77Lo))(78 (= answer p14Date78Lo))(79 (= answer p14Date79Lo))))) (return answer))
(method (p14SetDateLo index value) (switch (/ index 16) (0 (switch index (0 (= p14Date0Lo value))(1 (= p14Date1Lo value))(2 (= p14Date2Lo value))(3 (= p14Date3Lo value))(4 (= p14Date4Lo value))(5 (= p14Date5Lo value))(6 (= p14Date6Lo value))(7 (= p14Date7Lo value))(8 (= p14Date8Lo value))(9 (= p14Date9Lo value))(10 (= p14Date10Lo value))(11 (= p14Date11Lo value))(12 (= p14Date12Lo value))(13 (= p14Date13Lo value))(14 (= p14Date14Lo value))(15 (= p14Date15Lo value))))(1 (switch index (16 (= p14Date16Lo value))(17 (= p14Date17Lo value))(18 (= p14Date18Lo value))(19 (= p14Date19Lo value))(20 (= p14Date20Lo value))(21 (= p14Date21Lo value))(22 (= p14Date22Lo value))(23 (= p14Date23Lo value))(24 (= p14Date24Lo value))(25 (= p14Date25Lo value))(26 (= p14Date26Lo value))(27 (= p14Date27Lo value))(28 (= p14Date28Lo value))(29 (= p14Date29Lo value))(30 (= p14Date30Lo value))(31 (= p14Date31Lo value))))(2 (switch index (32 (= p14Date32Lo value))(33 (= p14Date33Lo value))(34 (= p14Date34Lo value))(35 (= p14Date35Lo value))(36 (= p14Date36Lo value))(37 (= p14Date37Lo value))(38 (= p14Date38Lo value))(39 (= p14Date39Lo value))(40 (= p14Date40Lo value))(41 (= p14Date41Lo value))(42 (= p14Date42Lo value))(43 (= p14Date43Lo value))(44 (= p14Date44Lo value))(45 (= p14Date45Lo value))(46 (= p14Date46Lo value))(47 (= p14Date47Lo value))))(3 (switch index (48 (= p14Date48Lo value))(49 (= p14Date49Lo value))(50 (= p14Date50Lo value))(51 (= p14Date51Lo value))(52 (= p14Date52Lo value))(53 (= p14Date53Lo value))(54 (= p14Date54Lo value))(55 (= p14Date55Lo value))(56 (= p14Date56Lo value))(57 (= p14Date57Lo value))(58 (= p14Date58Lo value))(59 (= p14Date59Lo value))(60 (= p14Date60Lo value))(61 (= p14Date61Lo value))(62 (= p14Date62Lo value))(63 (= p14Date63Lo value))))(4 (switch index (64 (= p14Date64Lo value))(65 (= p14Date65Lo value))(66 (= p14Date66Lo value))(67 (= p14Date67Lo value))(68 (= p14Date68Lo value))(69 (= p14Date69Lo value))(70 (= p14Date70Lo value))(71 (= p14Date71Lo value))(72 (= p14Date72Lo value))(73 (= p14Date73Lo value))(74 (= p14Date74Lo value))(75 (= p14Date75Lo value))(76 (= p14Date76Lo value))(77 (= p14Date77Lo value))(78 (= p14Date78Lo value))(79 (= p14Date79Lo value))))) (return 1))
(method (p14WinHiAt index &tmp answer) (= answer 0) (switch index (0 (= answer p14Win0Hi))(1 (= answer p14Win1Hi))(2 (= answer p14Win2Hi))(3 (= answer p14Win3Hi))) (return answer))
(method (p14SetWinHi index value) (switch index (0 (= p14Win0Hi value))(1 (= p14Win1Hi value))(2 (= p14Win2Hi value))(3 (= p14Win3Hi value))) (return 1))
(method (p14WinLoAt index &tmp answer) (= answer 0) (switch index (0 (= answer p14Win0Lo))(1 (= answer p14Win1Lo))(2 (= answer p14Win2Lo))(3 (= answer p14Win3Lo))) (return answer))
(method (p14SetWinLo index value) (switch index (0 (= p14Win0Lo value))(1 (= p14Win1Lo value))(2 (= p14Win2Lo value))(3 (= p14Win3Lo value))) (return 1))
(method (p14ContextItem obj &tmp valid) (if (not p14ContextBuilding) (return 0)) (= valid 0) (switch obj
 (1 (= valid 1))
 (3 (= valid 1))
 (4 (= valid 1))
 (5 (= valid 1))
 (6 (= valid 1))
 (7 (= valid 1))
 (9 (= valid 1))
 (11 (= valid 1))
 (12 (= valid 1))
 (13 (= valid 1))
 (14 (= valid 1))
 (15 (= valid 1))
 (16 (= valid 1))
 (17 (= valid 1))
 (18 (= valid 1))
 (19 (= valid 1))
 (20 (= valid 1))
 (21 (= valid 1))
 (22 (= valid 1))
 (23 (= valid 1))
 (24 (= valid 1))
 (25 (= valid 1))
 (26 (= valid 1))
 (27 (= valid 1))
 (31 (= valid 1))
 (32 (= valid 1))
 (33 (= valid 1))
 (34 (= valid 1))
 (35 (= valid 1))
 (36 (= valid 1))
 (37 (= valid 1))
 (38 (= valid 1))
 (39 (= valid 1))
 (40 (= valid 1))
 (41 (= valid 1))
 (42 (= valid 1))
 (43 (= valid 1))
 (44 (= valid 1))
 (45 (= valid 1))
 (46 (= valid 1))
 (47 (= valid 1))
 (48 (= valid 1))
 (49 (= valid 1))
 (50 (= valid 1))
 (51 (= valid 1))
 (52 (= valid 1))
 (53 (= valid 1))
 (55 (= valid 1))
 (56 (= valid 1))
 (58 (= valid 1))
 (59 (= valid 1))
 (60 (= valid 1))
 (62 (= valid 1))
 (63 (= valid 1))
 (64 (= valid 1))
 (65 (= valid 1))
 (66 (= valid 1))
 (67 (= valid 1))
 (68 (= valid 1))
 (69 (= valid 1))
 (70 (= valid 1))
 (71 (= valid 1))
 (72 (= valid 1))
 (116 (= valid 1))
 (117 (= valid 1))
 (118 (= valid 1))
 (119 (= valid 1))
 (120 (= valid 1))
 (121 (= valid 1))
 (122 (= valid 1))
 (123 (= valid 1))
 (395 (= valid 1))
 (396 (= valid 1))
 (397 (= valid 1))
 (398 (= valid 1))
 (399 (= valid 1))
 (73 (= valid 1))
 (74 (= valid 1))
 (75 (= valid 1))
 (76 (= valid 1))
 (77 (= valid 1))
 (78 (= valid 1))
 (79 (= valid 1))
 (80 (= valid 1))
 (81 (= valid 1))
 (82 (= valid 1))
 (83 (= valid 1))
 (84 (= valid 1))
 (86 (= valid 1))
 (87 (= valid 1))
 (88 (= valid 1))
 (89 (= valid 1))
 (90 (= valid 1))
 (91 (= valid 1))
 (92 (= valid 1))
 (93 (= valid 1))
 (94 (= valid 1))
 (410 (= valid 1))
 (411 (= valid 1))
 (412 (= valid 1))
 (413 (= valid 1))
 (414 (= valid 1))
 (415 (= valid 1))
 (416 (= valid 1))
 (417 (= valid 1))
 (418 (= valid 1))
 (432 (= valid 1))
 (433 (= valid 1))
 (434 (= valid 1))
) (if valid (= [p14Held obj] 1) (return 1)) (return (self p14ContextError:)))
(method (p14Context room apron flagsHi flagsLo boardRoom inputTone contestActive bunnyRoom frankieRoom miloRoom vivianRoom ritaRoom felixRoom stringerRoom epoch &tmp i) (self p14Invalidate:) (= p14ContextBuilding 0) (= p14ContextDateLength 0)
(for ((= i 0)) (< i P14_INVENTORY_LIMIT) ((++ i)) (= [p14Held i] 0))
(for ((= i 0)) (< i 4) ((++ i)) (= [p14FirstWinHi i] 0) (= [p14FirstWinLo i] 0) (= [p14LastWinHi i] 0) (= [p14LastWinLo i] 0) (= [p14MatchingWin i] 0))
(for ((= i 0)) (< i 160) ((++ i)) (= [p14InputDate i] 0))
(if (or (< room 0) (> room 6) (< apron 0) (> apron 1) (< flagsHi 0) (> flagsHi 8191) (< flagsLo 0) (and (!= boardRoom 1) (!= boardRoom 4)) (< inputTone 0) (> inputTone 2) (< contestActive 0) (> contestActive 1) (< bunnyRoom -1) (> bunnyRoom 6) (< frankieRoom -1) (> frankieRoom 6) (< miloRoom -1) (> miloRoom 6) (< vivianRoom -1) (> vivianRoom 6) (< ritaRoom -1) (> ritaRoom 6) (< felixRoom -1) (> felixRoom 6) (< stringerRoom -1) (> stringerRoom 6) (< epoch 1) (<= epoch p14Epoch) ) (= p14Code CODE_INVALID_CONTEXT) (return 0))
(= p14Room room) (= p14Apron apron) (= p14FlagsHi flagsHi) (= p14FlagsLo flagsLo) (= p14BoardRoom boardRoom) (= p14InputTone inputTone) (= p14ContestActive contestActive) (= p14BunnyRoom bunnyRoom) (= p14FrankieRoom frankieRoom) (= p14MiloRoom miloRoom) (= p14VivianRoom vivianRoom) (= p14RitaRoom ritaRoom) (= p14FelixRoom felixRoom) (= p14StringerRoom stringerRoom) (= p14Epoch epoch) (= p14ContextBuilding 1) (return 1))
(method (p14CreditCanonicalSource index &tmp answer) (= answer 0) (switch (/ index 16) (0 (switch index (0 (= answer 29))(1 (= answer 30))(2 (= answer 31))(3 (= answer 32))(4 (= answer 33))(5 (= answer 34))(6 (= answer 35))(7 (= answer 36))(8 (= answer 37))(9 (= answer 38))(10 (= answer 39))(11 (= answer 40))(12 (= answer 41))(13 (= answer 42))(14 (= answer 43))(15 (= answer 44))))(1 (switch index (16 (= answer 45))(17 (= answer 46))(18 (= answer 47))(19 (= answer 48))(20 (= answer 49))(21 (= answer 50))(22 (= answer 51))(23 (= answer 52))(24 (= answer 53))(25 (= answer 54))(26 (= answer 55))(27 (= answer 56))(28 (= answer 57))(29 (= answer 58))(30 (= answer 59))(31 (= answer 60))))(2 (switch index (32 (= answer 61))(33 (= answer 62))(34 (= answer 63))(35 (= answer 64))(36 (= answer 65))(37 (= answer 66))(38 (= answer 67))(39 (= answer 68))(40 (= answer 69))(41 (= answer 70))(42 (= answer 71))(43 (= answer 72))(44 (= answer 73))(45 (= answer 74))(46 (= answer 75))(47 (= answer 76))))(3 (switch index (48 (= answer 77))(49 (= answer 78))(50 (= answer 79))(51 (= answer 80))(52 (= answer 81))(53 (= answer 82))(54 (= answer 83))(55 (= answer 84))(56 (= answer 85))(57 (= answer 86))(58 (= answer 87))))) (return answer))
(method (p14Clear &tmp i)
 (= p14Code 0) (= p14LineCount 0) (= p14UnitCount 0) (= p14EventCount 0)
 (= p14ResultHi 0) (= p14ResultLo 0) (= p14PresentationSource 0) (= p14PresentationHi 0) (= p14PresentationLo 0)
 (for ((= i 0)) (< i 3) ((++ i)) (= [p14Lines i] 0))
 (for ((= i 0)) (< i 8) ((++ i)) (= [p14Units i] 0))
 (for ((= i 0)) (< i 1) ((++ i)) (= [p14Events i] 0) (= [p14EventHi i] 0) (= [p14EventLo i] 0))
 (for ((= i 0)) (< i 4) ((++ i)) (= [p14EventArgs i] 0)) (return 1))
(method (p14Init)
 (if p14Initialized (return (self p14Validate:))) (= p14Initialized 1) (self p14Clear:) (return 1))
(method (p14AppendLine line)
 (if (or (< line 1) (> line P14_LINE_LIMIT) (>= p14LineCount 3)) (return 0))
 (= [p14Lines p14LineCount] line) (++ p14LineCount) (return 1))
(method (p14Line index)
 (if (or (< index 0) (>= index p14LineCount)) (return 0)) (return [p14Lines index]))
(method (p14Unit index)
 (if (or (< index 0) (>= index p14UnitCount)) (return 0)) (return [p14Units index]))
(method (p14Event index)
 (if (or (< index 0) (>= index p14EventCount)) (return 0)) (return [p14Events index]))
(method (p14EventSerialHi index)
 (if (or (< index 0) (>= index p14EventCount)) (return 0)) (return [p14EventHi index]))
(method (p14EventSerialLo index)
 (if (or (< index 0) (>= index p14EventCount)) (return 0)) (return [p14EventLo index]))
(method (p14EventArg index arg)
 (if (or (< index 0) (>= index p14EventCount) (< arg 0) (> arg 3)) (return 0))
 (return [p14EventArgs (+ (* index 4) arg)]))
(method (p14Status code line)
 (= p14Code code) (if line (self p14AppendLine: line)) (return code))
(method (p14Invalidate &tmp i)
 (self p14Clear:) (= p14ContextValid 0) (= p14ContextBuilding 0)
 (for ((= i 0)) (< i 88) ((++ i)) (= [p14Lease i] 0)) (return 1))
(method (p14Start context)
 (self p14Clear:)
 (if (not (self p14Validate:)) (= p14Code CODE_INVALID_STATE) (return 0))
 (if (and context (not p14ContextValid)) (= p14Code CODE_INVALID_CONTEXT) (return 0)) (return 1))
(method (p14CanCommit count)
 (if (and (== p14RevisionHi 32767) (> p14RevisionLo (- 32767 count))) (= p14Code CODE_SERIAL_EXHAUSTED) (return 0)) (return 1))
(method (p14Commit)
 (if (== p14RevisionLo 32767) (= p14RevisionLo 0) (++ p14RevisionHi) else (++ p14RevisionLo))
 (= p14ResultHi p14RevisionHi) (= p14ResultLo p14RevisionLo) (return 1))
(method (p14Stamp slot) (return (self p14SetSerial: slot p14RevisionHi p14RevisionLo)))
(method (p14Emit event a b c d &tmp i)
 (if (>= p14EventCount 1) (return 0)) (= i (* p14EventCount 4))
 (= [p14Events p14EventCount] event) (= [p14EventHi p14EventCount] p14RevisionHi) (= [p14EventLo p14EventCount] p14RevisionLo)
 (= [p14EventArgs i] a) (= [p14EventArgs (+ i 1)] b) (= [p14EventArgs (+ i 2)] c) (= [p14EventArgs (+ i 3)] d)
 (++ p14EventCount)
 (proc946_1 (ScriptID 0 0) 996 event p14RevisionHi p14RevisionLo a b (- p14EventCount 1) ((ScriptID 0 0) location?) ((ScriptID 0 0) onApron?) (GetTime) ((ScriptID 980 0) token?))
 (proc944_1 (ScriptID 0 0) 996 event p14RevisionHi p14RevisionLo a b) (return 1))
(method (p14Present slot) (return (not (not (or (self p14SerialHi: slot) (self p14SerialLo: slot))))))
(method (p14Equal a b)
 (return (and (== (self p14SerialHi: a) (self p14SerialHi: b)) (== (self p14SerialLo: a) (self p14SerialLo: b)))))
(method (p14Earlier a b &tmp hi other)
 (= hi (self p14SerialHi: a)) (= other (self p14SerialHi: b))
 (return (or (< hi other) (and (== hi other) (< (self p14SerialLo: a) (self p14SerialLo: b))))))
(method (p14Count source &tmp count i base)
 (= count 0) (= base (self p14ReceiptBase: source))
 (for ((= i 0)) (< i (self p14Capacity: source)) ((++ i))
  (if (self p14Present: (+ base i)) (++ count))) (return count))
(method (p14Complete source)
 (return (and (self p14Present: (+ source 16)) (== (self p14Count: source) (self p14Capacity: source)))))
(method (p14Pending source &tmp count last i)
 (if (not (self p14Present: (+ source 16))) (return (self p14Status: CODE_PRESENTATION_NOT_STARTED 0)))
 (= count (self p14Count: source)) (= last (- (self p14Capacity: source) 1))
 (if (> count last) (return (self p14Status: CODE_PRESENTATION_COMPLETE 0)))
 (if (not (self p14Block: source count last)) (return p14Code))
 (= p14PresentationSource source) (= p14PresentationHi (self p14SerialHi: (+ source 16)))
 (= p14PresentationLo (self p14SerialLo: (+ source 16))) (= [p14Lease source] p14Epoch)
 (if (== count 0) (self p14AppendLine: (self p14SourceRecord: source))
 else (for ((= i count)) (<= i last) ((++ i))
  (= [p14Units p14UnitCount] (self p14TokenUnit: (self p14Token: source i))) (++ p14UnitCount)))
 (return (self p14Status: CODE_PRESENTATION_PENDING 0)))
(method (p14Resume source)
 (if (not (self p14Start: 1)) (return p14Code))
 (if (or (< source 1) (> source 87)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (if (self p14Present: (+ source 16)) (= [p14Lease source] p14Epoch))
 (return (self p14Pending: source)))
; BeginInternal preserves already emitted physical events from Introduce.
(method (p14BeginInternal source)
 (if (not (self p14Block: source 0 (- (self p14Capacity: source) 1))) (return p14Code))
 (if (self p14Present: (+ source 16))
  (if (self p14Complete: source) (return (self p14Status: CODE_PRESENTATION_COMPLETE (self p14SourceRecord: source))))
  (return (self p14Pending: source)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (self p14Commit:) (self p14Stamp: (+ source 16))
 (self p14Emit: EVENT_P14_PRESENTATION_QUEUED source 0 0 0) (return (self p14Pending: source)))
(method (p14Begin source)
 (if (not (self p14Start: 1)) (return p14Code))
 (if (or (< source 1) (> source 87)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (return (self p14BeginInternal: source)))
(method (p14Acknowledge source hi lo epoch record firstUnit lastUnit &tmp first last i total count base)
 (if (not (self p14Start: 1)) (return p14Code))
 (if (or (< source 1) (> source 87) (< hi 0) (< lo 0)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (if (or (not (self p14Present: (+ source 16))) (!= hi (self p14SerialHi: (+ source 16))) (!= lo (self p14SerialLo: (+ source 16)))
  (!= epoch p14Epoch) (!= epoch [p14Lease source])) (return (self p14Status: CODE_STALE_PRESENTATION 0)))
 (= first -1) (= last -1) (= total (self p14Capacity: source))
 (if record
  (if (or firstUnit lastUnit (!= record (self p14SourceRecord: source))) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
  (= first 0) (= last (- total 1))
 else
  (if (or (<= firstUnit 0) (<= lastUnit 0)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
  (for ((= i 0)) (< i total) ((++ i))
   (if (== firstUnit (self p14TokenUnit: (self p14Token: source i))) (= first i))
   (if (== lastUnit (self p14TokenUnit: (self p14Token: source i))) (= last i))))
 (if (or (< first 0) (< last first) (>= last total)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (= count (self p14Count: source))
 (if (< last count) (return (self p14Status: CODE_PRESENTATION_ALREADY_ACKNOWLEDGED 0)))
 (if (> first count) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (if (not (self p14Block: source count last)) (return p14Code))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (self p14Commit:) (= base (self p14ReceiptBase: source))
 (for ((= i count)) (<= i last) ((++ i)) (self p14Stamp: (+ base i)))
 (self p14Emit: EVENT_P14_PRESENTED source count last 0)
 (return (self p14Status: CODE_PRESENTATION_ACKNOWLEDGED 0)))
(method (p14OrderSources &tmp source count hi lo j)
 (= count 0)
 (for ((= source 1)) (<= source 87) ((++ source))
  (= hi (self p14SerialHi: (+ source 16))) (= lo (self p14SerialLo: (+ source 16)))
  (if (or hi lo)
   (for ((= j count)) (and (> j 0) (or (< hi [p14OrderedHi (- j 1)]) (and (== hi [p14OrderedHi (- j 1)]) (< lo [p14OrderedLo (- j 1)])))) ((-- j))
    (= [p14OrderedSources j] [p14OrderedSources (- j 1)]) (= [p14OrderedHi j] [p14OrderedHi (- j 1)]) (= [p14OrderedLo j] [p14OrderedLo (- j 1)]))
   (= [p14OrderedSources j] source) (= [p14OrderedHi j] hi) (= [p14OrderedLo j] lo) (++ count))) (return count))
(method (p14SourceRank rank &tmp count)
 (= count (self p14OrderSources:)) (if (or (< rank 0) (>= rank count)) (return 0)) (return [p14OrderedSources rank]))
(method (p14PendingAt index &tmp rank source count total)
 (if (< index 0) (return 0)) (= total (self p14OrderSources:)) (= count 0)
 (for ((= rank 0)) (< rank total) ((++ rank)) (= source [p14OrderedSources rank])
  (if (not (self p14Complete: source)) (if (== index count) (return source)) (++ count))) (return 0))
(method (p14JournalAt index units &tmp rank source i unit count total)
 (if (< index 0) (return 0)) (= total (self p14OrderSources:)) (= count 0)
 (for ((= rank 0)) (< rank total) ((++ rank)) (= source [p14OrderedSources rank])
  (if units
   (for ((= i 0)) (< i (self p14Count: source)) ((++ i)) (= unit (self p14TokenUnit: (self p14Token: source i)))
    (if unit (if (== index count) (return unit)) (++ count)))
  else (if (self p14Complete: source) (if (== index count) (return (self p14SourceRecord: source))) (++ count)))) (return 0))
(method (p14AfterRestore &tmp i)
 (self p14Clear:) (self p14Invalidate:) 
 (for ((= i 0)) (< i P14_INVENTORY_LIMIT) ((++ i)) (= [p14Held i] 0)) (return (self p14Validate:)))
(method (p14Hint level)
 (if (not (self p14Start: 0)) (return p14Code))
 (if (or (< level 1) (> level 3)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (return (self p14Status: CODE_HINT (+ LINE_P14_HINT_1 (- level 1)))))
(method (p14AudioFinished)
 (if (not (self p14Start: 0)) (return p14Code)) (return (self p14Status: CODE_AUDIO_HAS_NO_AUTHORITY 0)))
(method (p14Cancel source hi lo epoch)
 (if (not (self p14Start: 1)) (return p14Code))
 (if (or (< source 1) (> source 87)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (if (or (not (self p14Present: (+ source 16))) (!= hi (self p14SerialHi: (+ source 16))) (!= lo (self p14SerialLo: (+ source 16))) (!= epoch p14Epoch) (!= epoch [p14Lease source])) (return (self p14Status: CODE_STALE_PRESENTATION 0)))
 (self p14Invalidate:) (return (self p14Status: CODE_PRESENTATION_CANCELLED 0)))
(method (p14DoneSlot source)
 (if (not (self p14Complete: source)) (return 0)) (return (+ (self p14ReceiptBase: source) (- (self p14Capacity: source) 1))))
; Context projection is staged. Only a sealed complete snapshot can serve actions.
(method (p14ContextError) (= p14ContextValid 0) (= p14ContextBuilding 0) (self p14Clear:) (= p14Code CODE_INVALID_CONTEXT) (return 0))
(method (p14ContextDateChar index hi lo)
 (if (not p14ContextBuilding) (return 0))
 (if (or (!= index p14ContextDateLength) (< index 0) (>= index 80) (< hi 0) (> hi 33) (< lo 0) (and (== hi 33) (> lo 32767)) (and (== hi 0) (< lo 32))) (return (self p14ContextError:)))
 (= [p14InputDate (* index 2)] hi) (= [p14InputDate (+ (* index 2) 1)] lo) (++ p14ContextDateLength) (return 1))
(method (p14ContextWin contest hi lo)
 (if (not p14ContextBuilding) (return 0))
 (if (or (< contest 0) (> contest 3) (< hi 0) (< lo 0) (not (or hi lo))) (return (self p14ContextError:)))
 (if (or (< hi [p14LastWinHi contest]) (and (== hi [p14LastWinHi contest]) (<= lo [p14LastWinLo contest]))) (return (self p14ContextError:)))
 (if (not (or [p14FirstWinHi contest] [p14FirstWinLo contest])) (= [p14FirstWinHi contest] hi) (= [p14FirstWinLo contest] lo))
 (= [p14LastWinHi contest] hi) (= [p14LastWinLo contest] lo)
 (if (and (== hi (self p14WinHiAt: contest)) (== lo (self p14WinLoAt: contest))) (= [p14MatchingWin contest] 1)) (return 1))
(method (p14SealContext)
 (if (not p14ContextBuilding) (return 0)) (= p14ContextBuilding 0) (= p14ContextValid 1) (return 1))
(method (p14AllWins &tmp i)
 (for ((= i 0)) (< i 4) ((++ i)) (if (not (or [p14FirstWinHi i] [p14FirstWinLo i])) (return 0))) (return 1))
(method (p14MissingWin index)
 (if (or (not p14ContextValid) (< index 0) (> index 3)) (return 0)) (return (not (or [p14FirstWinHi index] [p14FirstWinLo index]))))
(method (p14Scene room)
 (if (or (!= p14Room room) p14Apron) (= p14Code CODE_OFFSCREEN) (return 0))
 (if p14ContestActive (= p14Code CODE_CONTEST_ACTIVE) (return 0)) (return 1))
(method (p14Gate)
 (if (not (self p14Scene: ROOM_L05_COURTYARD)) (return 0))
 (if (or (!= p14FlagsHi 8191) (!= p14FlagsLo 32767)) (= p14Code CODE_CANONICAL_TASKS_INCOMPLETE) (return 0))
 (if (not (self p14AllWins:)) (self p14Status: CODE_ALL_FOUR_ACTUAL_WINS_REQUIRED LINE_VC_GATE_MISSING_WINS) (return 0))
 (if (!= p14BoardRoom ROOM_L05_COURTYARD) (= p14Code CODE_BOARD_NOT_PHYSICALLY_DELIVERED) (return 0)) (return 1))
(method (p14ValidateContext &tmp i)
 (if (not p14ContextValid) (return 0))
 (if (self p14Present: 1)
  (if (or (!= p14FlagsHi 8191) (!= p14FlagsLo 32767) (not (self p14AllWins:))) (return 0))
  (if (and p14ContestActive (not (self p14Ready:))) (return 0))
  (for ((= i 0)) (< i 4) ((++ i)) (if (not [p14MatchingWin i]) (return 0))))
 (if (and (self p14Present: 2) [p14Held OBJ_RENEWAL_REPAIR_CARD]) (return 0))
 (if (and (self p14PencilWithFrankie:) [p14Held OBJ_GREASE_PENCIL]) (return 0))
 (if (and (self p14Ready:) (not [p14Held OBJ_GREASE_PENCIL])) (return 0)) (return 1))
(method (p14BaseBlock)
 (if (not (self p14Gate:)) (return 0))
 (if (not (self p14Present: 1)) (= p14Code CODE_COMMITMENTS_NOT_STARTED) (return 0))
 (if (self p14Ready:) (= p14Code CODE_COMMITMENTS_ALREADY_COMPLETE) (return 0))
 (if (not (self p14ValidateContext:)) (= p14Code CODE_INVALID_CONTEXT) (return 0)) (return 1))
(method (p14AllPinned &tmp i)
 (for ((= i 0)) (< i 8) ((++ i)) (if (not (self p14Present: (+ i 9))) (return 0))) (return 1))
(method (p14LatestPin &tmp i slot)
 (= slot 0)
 (for ((= i 9)) (< i 17) ((++ i)) (if (self p14Present: i) (if (or (== slot 0) (self p14Earlier: slot i)) (= slot i)))) (return slot))
(method (p14Block source first last &tmp room i speaker)
 (if (>= source SOURCE_CLOSING_PROFESSIONAL)
  (if (or (not (self p14Ready:)) (== p14Phase 0)) (= p14Code CODE_FINALE_NOT_STARTED) (return 0))
  (if p14Paused (= p14Code CODE_FINALE_PAUSED) (return 0))
  (if (!= source (self p14CurrentSource:)) (= p14Code CODE_NOT_CURRENT_FINALE_SCENE) (return 0))
  (if (< source SOURCE_CREDIT_END_CREDIT_TITLE)
   (= room ROOM_L05_COURTYARD) (if (== source SOURCE_TAG) (= room ROOM_L01_LIVING_ROOM))
   (if (not (self p14Scene: room)) (return 0)))
 else
  (if (not (self p14BaseBlock:)) (return 0))
  (if (and (>= source SOURCE_APPROVE_JACK) (<= source SOURCE_APPROVE_STRINGER))
   (if (self p14Present: (+ source 7)) (= p14Code CODE_PROMISE_ALREADY_PINNED) (return 0)))
  (if (== source SOURCE_SIGNATURE)
   (if (not (self p14AllPinned:)) (= p14Code CODE_ALL_EIGHT_APPROVED_AND_PINNED_REQUIRED) (return 0))
   (if (and (not [p14Held OBJ_RENEWAL_REPAIR_CARD]) (not (self p14Present: 2))) (= p14Code CODE_ORIGINAL_TERMS_CARD_REQUIRED) (return 0)))
  (if (and (>= source SOURCE_DATE) (<= source SOURCE_RETURN_PENCIL))
   (if (not (self p14Present: 3)) (= p14Code CODE_PENCIL_HANDOFF_REQUIRED) (return 0))
   (if (and (== source SOURCE_READBACK) (not (self p14Complete: SOURCE_DATE))) (= p14Code CODE_DATE_TEXT_REQUIRED) (return 0))
   (if (and (== source SOURCE_RETURN_PENCIL) (not (self p14Complete: SOURCE_READBACK))) (= p14Code CODE_COMPLETE_READBACK_REQUIRED) (return 0))))
 (for ((= i first)) (<= i last) ((++ i)) (= speaker (self p14TokenSpeaker: (self p14Token: source i)))
  (if (and speaker (!= speaker OBJ_JACK) (!= (self p14ActorRoom: speaker) p14Room)) (= p14Code CODE_SPEAKER_ABSENT) (return 0))) (return 1))
(method (p14StartCommitments object location signed dated owner record &tmp i)
 (if (not (self p14Start: 1)) (return p14Code)) (if (not (self p14Gate:)) (return p14Code))
 (if (self p14Present: 1) (return (self p14Status: CODE_COMMITMENTS_ALREADY_STARTED 0)))
 ; Terms metadata belongs to P09.READ.002; record value2 in this finite handoff.
 (if (or (!= object OBJ_RENEWAL_REPAIR_CARD) (!= location 1) signed dated (!= owner 14) (!= record 2)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (if (not [p14Held OBJ_RENEWAL_REPAIR_CARD]) (return (self p14Status: CODE_ORIGINAL_TERMS_CARD_REQUIRED 0)))
 (if (not p14ContextDateLength) (return (self p14Status: CODE_AGREED_FICTIONAL_DATE_REQUIRED 0)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (= p14EntryHi p14FlagsHi) (= p14EntryLo p14FlagsLo) (= p14DateLength p14ContextDateLength) (= p14Tone p14InputTone)
 (for ((= i 0)) (< i 4) ((++ i)) (self p14SetWinHi: i [p14FirstWinHi i]) (self p14SetWinLo: i [p14FirstWinLo i]) (= [p14MatchingWin i] 1))
 (for ((= i 0)) (< i p14DateLength) ((++ i)) (self p14SetDateHi: i [p14InputDate (* i 2)]) (self p14SetDateLo: i [p14InputDate (+ (* i 2) 1)]))
 (self p14Commit:) (self p14Stamp: 1) (self p14Emit: EVENT_P14_COMMITMENT_START 0 0 0 0) (return (self p14Status: CODE_COMMITMENTS_STARTED 0)))
(method (p14GiveCard person recipient)
 (if (not (self p14Start: 1)) (return p14Code))
 (if (or (< person 0) (> person 7) (< recipient 0) (> recipient 7)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (if (not (self p14BaseBlock:)) (return p14Code))
 (if (and recipient (!= (self p14ActorRoom: (self p14Person: recipient)) ROOM_L05_COURTYARD)) (return (self p14Status: CODE_RECIPIENT_ABSENT 0)))
 (if (!= person recipient) (return (self p14Status: CODE_UNRELATED_PROMISE_RETURNED (+ LINE_P14_WRONG_JACK (* recipient 4)))))
 (return (self p14Begin: (+ SOURCE_APPROVE_JACK person))))
(method (p14ConfirmJackie) (return (self p14Begin: SOURCE_APPROVE_JACK)))
(method (p14PinCard person)
 (if (not (self p14Start: 1)) (return p14Code))
 (if (or (< person 0) (> person 7)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (if (not (self p14BaseBlock:)) (return p14Code))
 (if (self p14Present: (+ person 9)) (return (self p14Status: CODE_CARD_ALREADY_PINNED 0)))
 (if (not (self p14Complete: (+ SOURCE_APPROVE_JACK person))) (return (self p14Status: CODE_APPROVAL_REQUIRED LINE_P14_FAILURE_001)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (self p14Commit:) (self p14Stamp: (+ person 9)) (self p14Emit: EVENT_P14_CARD_PINNED person 0 0 0) (return (self p14Status: CODE_APPROVED_CARD_PINNED LINE_P14_SUCCESS_001)))
(method (p14RequestSignature action)
 (if (not (self p14Start: 1)) (return p14Code))
 (if (or (< action 0) (> action 2)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (if (not (self p14BaseBlock:)) (return p14Code))
 (if (self p14Present: 2) (return (self p14Status: CODE_ALREADY_SIGNED 0)))
 (if action (return (self p14Status: CODE_SIGNATURE_REFUSED LINE_P14_FAILURE_002)))
 (return (self p14Begin: SOURCE_SIGNATURE)))
(method (p14PinSignature)
 (if (not (self p14Start: 1)) (return p14Code)) (if (not (self p14BaseBlock:)) (return p14Code))
 (if (self p14Present: 2) (return (self p14Status: CODE_ALREADY_SIGNED 0)))
 (if (not (self p14Complete: SOURCE_SIGNATURE)) (return (self p14Status: CODE_WHOLE_CONSENT_SCENE_REQUIRED 0)))
 (if (not [p14Held OBJ_RENEWAL_REPAIR_CARD]) (return (self p14Status: CODE_ORIGINAL_TERMS_CARD_REQUIRED 0)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (self p14Commit:) (self p14Stamp: 2) (self p14Emit: EVENT_P14_TERMS_SIGNED 0 0 0 0) (return (self p14Status: CODE_TERMS_SIGNED_AND_PINNED LINE_P14_SUCCESS_002)))
(method (p14GivePencil)
 (if (not (self p14Start: 1)) (return p14Code)) (if (not (self p14BaseBlock:)) (return p14Code))
 (if (self p14Present: 3) (return (self p14Status: CODE_PENCIL_ALREADY_HANDED_OVER 0)))
 (if (not (self p14Present: 2)) (return (self p14Status: CODE_SIGNED_TERMS_REQUIRED 0)))
 (if (not [p14Held OBJ_GREASE_PENCIL]) (return (self p14Status: CODE_ORIGINAL_PENCIL_REQUIRED 0)))
 (if (!= p14FrankieRoom ROOM_L05_COURTYARD) (return (self p14Status: CODE_FRANKIE_ABSENT 0)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (self p14Commit:) (self p14Stamp: 3) (self p14Emit: EVENT_P14_PENCIL_HANDOFF 0 0 0 0) (return (self p14Status: CODE_PENCIL_HANDED_OVER 0)))
(method (p14CompleteCommitments)
 (if (not (self p14Start: 1)) (return p14Code))
 (if (self p14Ready:) (return (self p14Status: CODE_COMMITMENTS_ALREADY_COMPLETE 0)))
 (if (not (self p14BaseBlock:)) (return p14Code))
 (if (not (self p14Complete: SOURCE_RETURN_PENCIL)) (return (self p14Status: CODE_COMPLETE_DATED_READBACK_AND_RETURN_REQUIRED 0)))
 (if (!= p14FrankieRoom ROOM_L05_COURTYARD) (return (self p14Status: CODE_FRANKIE_ABSENT 0)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (self p14Commit:) (self p14Stamp: 4) (self p14Emit: EVENT_P14_GAME_COMPLETE 0 0 0 0) (return (self p14Status: CODE_GAME_COMPLETE 0)))
(method (p14Ready) (return (self p14Present: 4)))
(method (p14PencilWithFrankie) (return (and (self p14Present: 3) (not (self p14Ready:)))))
(method (p14InventoryAt index &tmp person count)
 (= count 0)
 (if (self p14Present: 1) (for ((= person 0)) (< person 8) ((++ person)) (if (not (self p14Present: (+ person 9))) (if (== index count) (return (self p14Card: person))) (++ count)))) (return 0))
(method (p14ReservedAt index) (if (and (== index 0) (self p14Present: 2)) (return OBJ_RENEWAL_REPAIR_CARD)) (return 0))
(method (p14Approved person) (if (or (< person 0) (> person 7)) (return 0)) (return (self p14Complete: (+ SOURCE_APPROVE_JACK person))))
(method (p14Act verb obj target &tmp person recipient)
 (if (not (self p14Start: 1)) (return p14Code))
 (if (or (< verb 1) (> verb 9)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (= person (self p14CardIndex: obj)) (= recipient (self p14PersonIndex: target))
 (if (and (== verb 1) (>= person 0) (>= recipient 0)) (return (self p14GiveCard: person recipient)))
 (if (and (== verb 7) (>= person 0) (== target OBJ_PLEDGE_BOARD)) (return (self p14PinCard: person)))
 (if (and (== verb 1) (== obj OBJ_RENEWAL_REPAIR_CARD) (== target OBJ_STRINGER)) (return (self p14RequestSignature: 0)))
 (if (and (== verb 1) (== obj OBJ_GREASE_PENCIL) (== target OBJ_FRANKIE)) (return (self p14GivePencil:)))
 (return (self p14Status: CODE_UNHANDLED_ACTION 0)))
; Finale mutates presentation state only. Current physical stage belongs to host.
(method (p14CurrentSource &tmp answer)
 (= answer 0)
 (switch p14Phase
  (1 (= answer (+ SOURCE_CLOSING_PROFESSIONAL p14Tone)))
  (2 (= answer SOURCE_MEAL)) (3 (= answer SOURCE_TAG))
  (5 (if (< p14CreditCursor p14CreditCount) (= answer (self p14CreditAt: p14CreditCursor))))) (return answer))
(method (p14CreditRecord index)
 (if (or (< index 0) (>= index p14CreditCount)) (return 0)) (return (self p14SourceRecord: (self p14CreditAt: index))))
(method (p14StartFinale mask0 mask1 mask2 &tmp i bits)
 (if (not (self p14Start: 0)) (return p14Code))
 (if (not (self p14Ready:)) (return (self p14Status: CODE_LEGITIMATE_COMPLETION_REQUIRED 0)))
 (if (self p14Present: 5) (return (self p14Status: CODE_FINALE_ALREADY_STARTED 0)))
 (if (or (< mask0 0) (< mask1 0) (< mask2 0) (> mask2 7)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (= p14CreditCount 26)
 (for ((= i 0)) (< i 26) ((++ i)) (self p14SetCredit: i (self p14CreditCanonicalSource: i)))
 (= bits mask0)
 (for ((= i 0)) (< i 33) ((++ i))
  (if (== i 15) (= bits mask1)) (if (== i 30) (= bits mask2))
  (if (& bits 1) (self p14SetCredit: p14CreditCount (self p14CreditCanonicalSource: (+ i 26))) (++ p14CreditCount))
  (= bits (/ bits 2)))
 (= p14Phase 1) (self p14Commit:) (self p14Stamp: 5) (self p14Emit: EVENT_P14_FINALE_BEGIN 0 0 0 0) (return (self p14Status: CODE_FINALE_STARTED 0)))
(method (p14PresentFinale &tmp source)
 (if (not (self p14Start: 1)) (return p14Code))
 (if p14Paused (return (self p14Status: CODE_FINALE_PAUSED 0)))
 (= source (self p14CurrentSource:)) (if source (return (self p14Begin: source)))
 (if (== p14Phase 4) (return (self p14Status: CODE_FREEZE_FRAME_PENDING 0))) (return (self p14Status: CODE_NO_PENDING_FINALE_TEXT 0)))
(method (p14AdvanceFinale &tmp source)
 (if (not (self p14Start: 0)) (return p14Code))
 (if p14Paused (return (self p14Status: CODE_FINALE_PAUSED 0)))
 (if (or (== p14Phase 0) (== p14Phase 6)) (return (self p14Status: CODE_FINALE_INACTIVE 0)))
 (= source (self p14CurrentSource:))
 (if (and source (not (self p14Complete: source))) (return (self p14Status: CODE_WHOLE_FINALE_RECORD_REQUIRED 0)))
 (if (and (== p14Phase 4) (not (self p14Present: 6))) (return (self p14Status: CODE_VISIBLE_FREEZE_REQUIRED 0)))
 ; A structurally loadable exhausted cursor cannot commit past the finite roll.
 (if (and (== p14Phase 5) (>= p14CreditCursor p14CreditCount)) (return (self p14Status: CODE_INVALID_STATE 0)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (if (== p14Phase 5) (++ p14CreditCursor) (if (== p14CreditCursor p14CreditCount) (= p14Phase 6)) else (++ p14Phase))
 (self p14Commit:) (self p14Emit: EVENT_P14_FINALE_SCENE p14Phase 0 0 0) (return (self p14Status: CODE_FINALE_ADVANCED 0)))
(method (p14FreezePending) (return (and (== p14Phase 4) (not (self p14Present: 6)))))
(method (p14AcknowledgeFreeze hi lo epoch)
 (if (not (self p14Start: 1)) (return p14Code))
 (if p14Paused (return (self p14Status: CODE_FINALE_PAUSED 0)))
 (if (or (not (self p14FreezePending:)) (!= hi p14FinaleHi) (!= lo p14FinaleLo) (!= epoch p14Epoch)) (return (self p14Status: CODE_STALE_FREEZE 0)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (self p14Commit:) (self p14Stamp: 6) (self p14Emit: EVENT_P14_FREEZE_PRESENTED 0 0 0 0) (return (self p14Status: CODE_FREEZE_PRESENTED 0)))
(method (p14ClaimTagLaugh)
 (if (not (self p14Start: 0)) (return p14Code))
 (if (self p14Present: 8) (return (self p14Status: CODE_LAUGH_CONSUMED 0)))
 (if (or p14Paused (and (!= p14Phase 3) (!= p14Phase 4)) (not (self p14Complete: SOURCE_TAG))) (return (self p14Status: CODE_TAG_LAUGH_UNAVAILABLE 0)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (self p14Commit:) (self p14Stamp: 8) (self p14Emit: EVENT_LAF14 0 0 0 0) (return (self p14Status: CODE_LAUGH_CONSUMED 0)))
(method (p14ClaimCelebration)
 (if (not (self p14Start: 0)) (return p14Code))
 (if (self p14Present: 7) (return (self p14Status: CODE_CELEBRATION_CONSUMED 0)))
 (if (or p14Paused (!= p14Phase 4) (not (self p14Present: 6))) (return (self p14Status: CODE_CELEBRATION_UNAVAILABLE 0)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (self p14Commit:) (self p14Stamp: 7) (self p14Emit: EVENT_P14_CELEBRATION 0 0 0 0) (return (self p14Status: CODE_CELEBRATION_CONSUMED 0)))
(method (p14PauseFinale paused)
 (if (not (self p14Start: 0)) (return p14Code))
 (if (or (< paused 0) (> paused 1)) (return (self p14Status: CODE_INVALID_ARGUMENT 0)))
 (if (or (== p14Phase 0) (== p14Phase 6) (== paused p14Paused)) (return (self p14Status: CODE_PAUSE_UNCHANGED 0)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (= p14Paused paused) (self p14Commit:) (self p14Emit: EVENT_P14_FINALE_PAUSE paused 0 0 0)
 (if paused (return (self p14Status: CODE_FINALE_PAUSED 0))) (return (self p14Status: CODE_FINALE_RESUMED 0)))
(method (p14SkipFinale)
 (if (not (self p14Start: 0)) (return p14Code))
 (if (or (== p14Phase 0) (== p14Phase 6)) (return (self p14Status: CODE_FINALE_INACTIVE 0)))
 (if (not (self p14CanCommit: 1)) (return p14Code))
 (= p14Phase 6) (= p14Skipped 1) (= p14Paused 0) (self p14Commit:) (self p14Emit: EVENT_P14_FINALE_SKIP 0 0 0 0) (return (self p14Status: CODE_FINALE_SKIPPED 0)))
; Call only on a detached copy owned by a saved replay envelope (see codec.py).
(method (p14PrepareReplay &tmp source i base)
 (if (not (self p14Start: 0)) (return 0))
 (if (or (not (self p14Ready:)) (not (self p14Present: 5))) (= p14Code CODE_LEGITIMATE_COMPLETION_REQUIRED) (return 0))
 (for ((= source SOURCE_CREDIT_END_CREDIT_TITLE)) (<= source 87) ((++ source))
  (self p14SetSerial: (+ source 16) 0 0) (= base (self p14ReceiptBase: source))
  (for ((= i 0)) (< i (self p14Capacity: source)) ((++ i)) (self p14SetSerial: (+ base i) 0 0)))
 (= p14Phase 5) (= p14CreditCursor 0) (= p14Replay 1) (= p14Paused 0) (= p14Skipped 0)
 (self p14Invalidate:) (= p14Code CODE_REPLAY_PREPARED) (return (self p14Validate:)))
; Structural save validation mirrors the model; it is not a cryptographic history.
(method (p14Validate &tmp slot hi lo source start base i receipt previous gap gate other count owner last)
 (if (!= p14Initialized 1) (return 0))
 (if (or (< p14EntryHi 0) (> p14EntryHi 8191) (< p14EntryLo 0) (< p14DateLength 0) (> p14DateLength 80) (< p14Tone 0) (> p14Tone 2) (< p14Phase 0) (> p14Phase 6)
  (< p14Paused 0) (> p14Paused 1) (< p14Skipped 0) (> p14Skipped 1) (< p14Replay 0) (> p14Replay 1) (< p14CreditCount 0) (> p14CreditCount 59) (< p14CreditCursor 0) (> p14CreditCursor p14CreditCount)) (return 0))
 (for ((= slot 0)) (< slot P14_SERIAL_COUNT) ((++ slot))
  (= hi (self p14SerialHi: slot)) (= lo (self p14SerialLo: slot))
  (if (or (< hi 0) (< lo 0) (> hi p14RevisionHi) (and (== hi p14RevisionHi) (> lo p14RevisionLo))) (return 0)))
 (for ((= i 0)) (< i 80) ((++ i))
  (= hi (self p14DateHiAt: i)) (= lo (self p14DateLoAt: i))
  (if (< i p14DateLength)
   (if (or (< hi 0) (> hi 33) (< lo 0) (and (== hi 0) (< lo 32))) (return 0))
  else (if (or hi lo) (return 0))))
 (for ((= i 0)) (< i 4) ((++ i))
  (= hi (self p14WinHiAt: i)) (= lo (self p14WinLoAt: i))
  (if (or (< hi 0) (< lo 0)) (return 0))
  (if (self p14Present: 1) (if (not (or hi lo)) (return 0)) else (if (or hi lo) (return 0))))
 (if (self p14Present: 1)
  (if (or (!= p14EntryHi 8191) (!= p14EntryLo 32767) (== p14DateLength 0)) (return 0))
 else
  (if (or p14EntryHi p14EntryLo p14DateLength) (return 0))
  (for ((= slot 2)) (< slot P14_SERIAL_COUNT) ((++ slot)) (if (self p14Present: slot) (return 0))))
 (for ((= i 0)) (< i 8) ((++ i)) (= slot (+ i 9))
  (if (self p14Present: slot) (= gate (self p14DoneSlot: (+ SOURCE_APPROVE_JACK i)))
   (if (or (== gate 0) (not (self p14Earlier: gate slot))) (return 0))))
 (if (self p14Present: 2)
  (= gate (self p14DoneSlot: SOURCE_SIGNATURE))
  (if (or (not (self p14AllPinned:)) (== gate 0) (not (self p14Earlier: (self p14LatestPin:) gate)) (not (self p14Earlier: gate 2))) (return 0)))
 (if (self p14Present: 3) (if (or (not (self p14Present: 2)) (not (self p14Earlier: 2 3))) (return 0)))
 (if (self p14Present: 4)
  (= gate (self p14DoneSlot: SOURCE_DATE)) (= slot (self p14DoneSlot: SOURCE_READBACK)) (= last (self p14DoneSlot: SOURCE_RETURN_PENCIL))
  (if (or (== gate 0) (== slot 0) (== last 0) (not (self p14Present: 3)) (not (self p14Earlier: 3 gate)) (not (self p14Earlier: gate slot)) (not (self p14Earlier: slot last)) (not (self p14Earlier: last 4))) (return 0)))
 ; Gather only caption operations; same-receipt serial may repeat within one source.
 (= count 0)
 (for ((= source 1)) (<= source 87) ((++ source))
  (= start (+ source 16)) (= base (self p14ReceiptBase: source)) (= previous start) (= gap 0)
  (if (self p14Present: start)
   (= gate 1)
   (if (== source SOURCE_SIGNATURE) (= gate 0) (if (self p14AllPinned:) (= gate (self p14LatestPin:))))
   (if (== source SOURCE_DATE) (= gate 3))
   (if (== source SOURCE_READBACK) (= gate (self p14DoneSlot: SOURCE_DATE)))
   (if (== source SOURCE_RETURN_PENCIL) (= gate (self p14DoneSlot: SOURCE_READBACK)))
   (if (>= source SOURCE_CLOSING_PROFESSIONAL) (= gate 4))
   (if (or (== gate 0) (not (self p14Present: gate)) (not (self p14Earlier: gate start))) (return 0))
   (= [p14ValidationHi count] (self p14SerialHi: start)) (= [p14ValidationLo count] (self p14SerialLo: start)) (= [p14ValidationOwners count] (- 0 source)) (++ count))
  (for ((= i 0)) (< i (self p14Capacity: source)) ((++ i)) (= receipt (+ base i))
   (if (self p14Present: receipt)
    (if (or gap (not (self p14Present: start)) (not (self p14Earlier: start receipt)) (self p14Earlier: receipt previous)) (return 0))
    (= previous receipt)
    (= [p14ValidationHi count] (self p14SerialHi: receipt)) (= [p14ValidationLo count] (self p14SerialLo: receipt)) (= [p14ValidationOwners count] source) (++ count)
   else (= gap 1))))
 (for ((= i 0)) (< i count) ((++ i))
  (for ((= other (+ i 1))) (< other count) ((++ other))
   (if (and (== [p14ValidationHi i] [p14ValidationHi other]) (== [p14ValidationLo i] [p14ValidationLo other]))
    (if (or (< [p14ValidationOwners i] 0) (!= [p14ValidationOwners i] [p14ValidationOwners other])) (return 0)))))
 (for ((= i 0)) (< i 59) ((++ i)) (= source (self p14CreditAt: i))
  (if (< i p14CreditCount)
   (if (< i 26)
    (if (!= source (self p14CreditCanonicalSource: i)) (return 0))
   else
    (if (or (< source SOURCE_CREDIT_END_ASSET_AUDIENCE_01) (> source 87)) (return 0))
    (for ((= other 26)) (< other i) ((++ other)) (if (== source (self p14CreditAt: other)) (return 0))))
  else (if source (return 0))))
 (if (self p14Present: 5)
  (if (or (not (self p14Ready:)) (not (self p14Earlier: 4 5)) (== p14Phase 0) (< p14CreditCount 26)) (return 0))
 else
  (if (or p14Phase p14CreditCount p14CreditCursor p14Paused p14Skipped (self p14Present: 6) (self p14Present: 7) (self p14Present: 8)) (return 0)))
 (if p14Replay
  (if (or (not (self p14Ready:)) (not (self p14Present: 5)) (and (!= p14Phase 5) (!= p14Phase 6))) (return 0)))
 (if (and (not p14Replay) (== p14Phase 5) (not (self p14Present: 6))) (return 0))
 (if (and (>= p14Phase 2) (<= p14Phase 4)) (if (not (self p14Complete: (+ SOURCE_CLOSING_PROFESSIONAL p14Tone))) (return 0)))
 (if (and (>= p14Phase 3) (<= p14Phase 4)) (if (not (self p14Complete: SOURCE_MEAL)) (return 0)))
 (if (and (== p14Phase 4) (not (self p14Complete: SOURCE_TAG))) (return 0))
 (if (self p14Present: 6) (= gate (self p14DoneSlot: SOURCE_TAG)) (if (or (== gate 0) (not (self p14Earlier: gate 6))) (return 0)))
 (if (self p14Present: 7) (if (or (not (self p14Present: 6)) (not (self p14Earlier: 6 7))) (return 0)))
 (if (self p14Present: 8) (= gate (self p14DoneSlot: SOURCE_TAG)) (if (or (== gate 0) (not (self p14Earlier: gate 8))) (return 0)))
 (for ((= i 0)) (< i p14CreditCursor) ((++ i)) (if (not (self p14Complete: (self p14CreditAt: i))) (return 0)))
 (if (and (== p14Phase 6) (not p14Skipped) (!= p14CreditCursor p14CreditCount)) (return 0))
 (return 1))

(method (p14WonCount &tmp i count)
 (if (not p14ContextValid) (return 0)) (= count 0)
 (for ((= i 0)) (< i 4) ((++ i)) (if (not (self p14MissingWin: i)) (++ count))) (return count))
(method (p14NotebookRecord)
 (if (not p14ContextValid) (return 0))
 (if (self p14AllWins:) (return LINE_VC_GATE_ALL_WON)) (return LINE_VC_GATE_MISSING_WINS))


(method (h14Fact index &tmp h) (= h (ScriptID 0 0)) (switch index
; AUD_CUE_VIEW
 (0 (return (not (not ((ScriptID 994 0) p12Viewed:)))))
; CERAMICS_READY
 (1 (return (not (not ((ScriptID 983 0) p03Ready?)))))
; CUES_RESTORED
 (2 (return (not (not ((ScriptID 992 0) p10Ready:)))))
; CUE_RACK_FACING_HOST
 (3 (return (not (not ((ScriptID 994 0) p12Present: 3)))))
; CUE_RAIL_RELEASED
 (4 (return (not (not ((ScriptID 994 0) p12Present: 2)))))
; DISPLAY_REVEALED
 (5 (return (not (not ((ScriptID 995 0) p13Present: 7)))))
; DISPLAY_STAGED
 (6 (return (not (not ((ScriptID 993 0) p11Ready:)))))
; EVENING_STARTED
 (7 (return (not (not ((ScriptID 989 0) h8EveningCommitted:)))))
; FOOD_READY
 (8 (return (not (not (& ((ScriptID 988 0) p07Projection: 0) 2)))))
; GATE_TESTED
 (9 (return (not (not ((h p04?) p04Ready:)))))
; HELP_ACCEPTED
 (10 (return (not (not ((ScriptID 993 0) p11SincereComplete:)))))
; HOLD_OPEN_AVAILABLE
 (11 (return (not (not ((h p04?) p04Ready:)))))
; HOUSE_ENTERED
 (12 (return (not (not (h houseEntered?)))))
; INTRODUCTION_CLEAR
 (13 (return (not (not ((ScriptID 994 0) p12Ready:)))))
; MILO_ROLE_AGREED
 (14 (return (not (not (& ((ScriptID 985 0) p05Flags:) 2)))))
; PA_TESTED
 (15 (return (not (not (& ((ScriptID 985 0) p05Flags:) 1)))))
; PLAN_AGREED
 (16 (return (not (not (h p02PlanAgreed?)))))
; RUMOR_CLEARED
 (17 (return (not (not ((ScriptID 990 0) p09RumorCleared?)))))
; SCREEN_BUILT
 (18 (return (not (not (& ((ScriptID 987 0) p06Projection: 0) 2)))))
; SCREEN_READY
 (19 (return (not (not (& ((ScriptID 987 0) p06Projection: 0) 4)))))
; SERVED
 (20 (return (not (not ((ScriptID 995 0) p13Served:)))))
; SOUND_READY
 (21 (return (not (not (& ((ScriptID 985 0) p05Flags:) 4)))))
; TERMS_CARD_AVAILABLE
 (22 (return (not (not ((ScriptID 990 0) p09Ready?)))))
; TOAST_READY
 (23 (return (not (not ((ScriptID 995 0) p13Ready:)))))
; TRAY_SAFE
 (24 (return (not (not (h traySafe?)))))
; VC01_RESOLVED
 (25 (return (not (not (or ((ScriptID 986 0) vcRead: 58) ((ScriptID 986 0) vcRead: 59))))))
; VC02_RESOLVED
 (26 (return (not (not (or ((ScriptID 986 0) vcRead: 66) ((ScriptID 986 0) vcRead: 67))))))
; VIVIAN_SCOPE_AGREED
 (27 (return (not (not (& ((ScriptID 987 0) p06Projection: 0) 1)))))
) (return 0))
(method (h14Ctx &tmp h i obj lo hi bit q)
 (= h (ScriptID 0 0)) (= q (ScriptID 985 0))
 (if (or (not (self h14Base:)) (>= p14Epoch 32767) (and [h14Owner 0] (not (self h14Valid:)))) (return 0))
 (if (not (self p14Init:)) (return 0)) (= hi 0) (= lo 0) (= bit 1)
 (for ((= i 0)) (< i 28) ((++ i))
  (= [h14Facts i] (self h14Fact: i))
  (if (== i 15) (= bit 1))
  (if [h14Facts i] (if (< i 15) (= lo (| lo bit)) else (= hi (| hi bit))))
  (if (!= i 14) (= bit (* bit 2))))
 (= [h14Facts 28] (h location?)) (= [h14Facts 29] (h onApron?))
 (= [h14Facts 30] (- ((ScriptID 987 0) p06Projection: 6) 1))
 (if (not (self p14Context: (h location?) (h onApron?) hi lo ((ScriptID 995 0) h13Location: 433)
  [h14Facts 30] (not (not (q hVCSession?)))
  (self h14RawRoom: H14_HOST_BUNNY) (self h14RawRoom: H14_HOST_FRANKIE) (self h14RawRoom: H14_HOST_MILO) (self h14RawRoom: H14_HOST_VIVIAN)
  (self h14RawRoom: H14_HOST_RITA) (self h14RawRoom: H14_HOST_FELIX) (self h14RawRoom: H14_HOST_STRINGER) (+ p14Epoch 1))) (return 0))
 (for ((= i 0)) (< i (h uiInventoryExtent?)) ((++ i))
  (= obj (h p04UIItem: i))
  (if (and obj (not (self h14Owns: obj))) (if (not (self p14ContextItem: obj)) (return 0))))
 (if [h14Owner 0]
  (if (not (self p14Present: 2)) (self p14ContextItem: 399))
  (if (not (self p14PencilWithFrankie:)) (self p14ContextItem: 25)))
 ; hVCWinning* is newly recorded result provenance, never the win counter.
 (for ((= i 0)) (< i 4) ((++ i))
  (= hi (q hVCWinningHi: (+ i 1))) (= lo (q hVCWinningLo: (+ i 1)))
  (if (or hi lo) (if (not (self p14ContextWin: i hi lo)) (return 0))))
 (for ((= i 0)) (< i [h14Date 0]) ((++ i))
  (if (not (self p14ContextDateChar: i 0 [h14Date (+ i 1)])) (return 0)))
 (return (and (self p14SealContext:) (self p14ValidateContext:))))
(method (h14Match &tmp h i)
 (= h (ScriptID 0 0))
 (if (or (not (self h14Base:)) (not (self h14Valid:)) (not (self p14ValidateContext:))
  (h motionPhase?) (!= (h location?) [h14Facts 28]) (!= (h onApron?) [h14Facts 29])
  (!= (- ((ScriptID 987 0) p06Projection: 6) 1) [h14Facts 30])) (return 0))
 (for ((= i 0)) (< i 28) ((++ i)) (if (!= [h14Facts i] (self h14Fact: i)) (return 0))) (return 1))
(method (h14DateOpen &tmp h i)
 (= h (ScriptID 0 0))
 (if (or [h14Owner 0] (not (self h14Base:)) (h motionPhase?) (h onApron?) (!= (h location?) 4)) (return 0))
 (self h14Retire:) (h speechCancel:) (h uiPanel: 0 uiBackPanel: 0)
 (= [h14Edit 0] 1) (= [h14Edit 1] [h14Date 0])
 (for ((= i 0)) (< i 80) ((++ i)) (= [h14EditChars i] [h14Date (+ i 1)]))
 (= [h14Edit 2] 0) (h dirty: 1) (return 1))
(method (h14Input &tmp h key i)
(if (and ((ScriptID 997 0) h14ReplayActive:) ((ScriptID 997 0) h14ReplayInput:)) (return 1))

 (= h (ScriptID 0 0)) (if (not [h14Edit 0]) (return 0))
 (if (not (self h14Base:)) (= [h14Edit 0] 0) (return 1))
 (if (!= (h type?) 4) (return 1)) (= key (h message?))
 (if (== key 27) (= [h14Edit 0] 0) (h dirty: 1) (return 1))
 (if (== key 13)
  (if (and [h14Edit 1] [h14Edit 3])
   (= [h14Date 0] [h14Edit 1])
   (for ((= i 0)) (< i 80) ((++ i)) (= [h14Date (+ i 1)] (if (< i [h14Edit 1]) [h14EditChars i] else 0)))
   (= [h14Edit 0] 0) (h dirty: 1)) (return 1))
 (if (== key 8)
  (if [h14Edit 1] (-- [h14Edit 1]) (= [h14EditChars [h14Edit 1]] 0))
 else
  (if (or (< key 32) (> key 126) (== key 124) (>= [h14Edit 1] 80))
   (= [h14Edit 2] 1) (h dirty: 1) (return 1))
  (= [h14EditChars [h14Edit 1]] key) (++ [h14Edit 1]))
 (= [h14Edit 3] 0) (= [h14Edit 2] 0) (h dirty: 1) (return 1))
(method (h14DateDraw &tmp i v)
 (if (not [h14Edit 0]) (return 0))
 (for ((= i 0)) (< i 43) ((++ i)) (= [h14EditText i] 0))
 (for ((= i 0)) (< i [h14Edit 1]) ((++ i))
  (= v [h14EditChars i])
  (if (mod i 2) (= [h14EditText (/ i 2)] (| [h14EditText (/ i 2)] (<< v 8))) else (= [h14EditText (/ i 2)] v)))
 (Graph 11 45 3 140 316 1 0 0 0)
 (Display "Choose the agreed in-fiction repair date" 100 8 50 102 2 105 1 106 303 121)
 (Display @h14EditText 100 8 67 102 1 105 1 106 300 121)
 (Display "1-80 printable ASCII characters; | is unavailable." 100 8 102 102 13 105 1 106 302 121)
 (Display "Enter confirms. Backspace edits. Esc cancels." 100 8 116 102 1 105 1 106 302 121)
 (if [h14Edit 2] (Display "Unsupported character or date too long." 100 8 128 102 12 105 1 106 300 121))
 (return 1))
(method (h14DateBind &tmp i source)
 (= source [h14Reader 2])
 (if (or (!= source 22) (not (self h14Match:)) (< p14DateLength 1) (> p14DateLength 80)) (return 0))
 (if (not (proc999_2 996 p14Epoch p14RevisionHi p14RevisionLo p14StartHi p14StartLo
  (self p14SerialHi: (+ source 16)) (self p14SerialLo: (+ source 16)) p14DateLength)) (return 0))
 (for ((= i 0)) (< i p14DateLength) ((++ i))
  (if (or (self p14DateHiAt: i) (not (proc999_3 i (self p14DateLoAt: i)))) (proc999_1) (return 0)))
 (return (proc999_4)))
(method (h14DateMatch &tmp i)
 (if (or (not (proc999_4)) (not (self h14Match:)) (!= [h14Reader 2] 22)
  (!= (proc999_5 2 0) p14DateLength) (!= (proc999_5 2 2) 996) (!= (proc999_5 2 3) p14Epoch)
  (!= (proc999_5 2 4) p14RevisionHi) (!= (proc999_5 2 5) p14RevisionLo)
  (!= (proc999_5 2 6) p14StartHi) (!= (proc999_5 2 7) p14StartLo)
  (!= (proc999_5 2 8) (self p14SerialHi: 38)) (!= (proc999_5 2 9) (self p14SerialLo: 38))) (return 0))
 (for ((= i 0)) (< i p14DateLength) ((++ i))
  (if (or (self p14DateHiAt: i) (!= (proc999_5 1 i) (self p14DateLoAt: i))) (return 0))) (return 1))
(method (h14Label obj)
 (switch obj (435 (return "Jackie Tree pledge")) (436 (return "Bunny Easter pledge")) (437 (return "Frankie Maplewood pledge"))
  (438 (return "Milo Pennant pledge")) (439 (return "Vivian Voss pledge")) (440 (return "Rita Stringer pledge"))
  (441 (return "Felix Bunt pledge")) (442 (return "Mr. Stringer pledge")) (399 (return "Original renewal and repair card"))
  (25 (return "Original grease pencil")) (433 (return "Promises and the ending")))
 (return ((ScriptID 995 0) h13Label: obj)))
(method (h14Menu obj &tmp h i person)
 (= h (ScriptID 0 0)) (self h14Retire:) (= [h14Selected 0] obj)
 (h speechCancel:) (h uiClearChoices: "EVERY PROMISE HAS A NAME" 256 0)
 (if (not [h14Owner 0])
  (h uiAddChoice: 1 "Enter the agreed in-fiction repair date" 0 1)
  (h uiAddChoice: 2 "Begin the commitments" 0 (and [h14Date 0] ((ScriptID 995 0) h13AllHere:)))
  (for ((= i 1)) (<= i 4) ((++ i))
   (if (not (or ((ScriptID 985 0) hVCWinningHi: i) ((ScriptID 985 0) hVCWinningLo: i)))
    (h uiAddChoice: (+ 200 i) (switch i
     (1 "Still needed: win with Milo") (2 "Still needed: win with Vivian")
     (3 "Still needed: win with Felix") (4 "Still needed: win with Stringer")) 0 0)))
 else
  (= person (self p14CardIndex: obj))
  (if (>= person 0)
   (h uiAddChoice: 100 "Read this named promise" 0 1)
   (for ((= i 0)) (< i 8) ((++ i))
    (h uiAddChoice: (+ 120 i) (switch i (0 "Confirm Jackie's own promise") (1 "Offer this card to Bunny")
     (2 "Offer this card to Frankie") (3 "Offer this card to Milo") (4 "Offer this card to Vivian")
     (5 "Offer this card to Rita") (6 "Offer this card to Felix") (7 "Offer this card to Stringer")) 0 1))
   (h uiAddChoice: 140 "Pin this approved card to the board" 0 1)
  else
   (if (not (self p14Ready:))
    (h uiAddChoice: 10 "Hear the commitments opening" 0 1)
    (for ((= i 0)) (< i 8) ((++ i))
     (h uiAddChoice: (+ 20 i) (self h14Label: (+ i 435)) (self p14Present: (+ i 9)) 1))
    (h uiAddChoice: 30 "Make the warm toast" 0 1) (h uiAddChoice: 31 "Make the dry toast" 0 1)
    (h uiAddChoice: 32 "Ask Stringer to hear the original terms" 0 1)
    (h uiAddChoice: 33 "Sign and pin the fully heard terms" 0 1)
    (h uiAddChoice: 34 "Hand Frankie the original grease pencil" 0 1)
    (h uiAddChoice: 35 "Hear the date announcement" 0 1)
    (h uiAddChoice: 36 "Read back the exact selected date and agreement" 0 1)
    (h uiAddChoice: 37 "Hear the pencil return" 0 1)
    (h uiAddChoice: 38 "Receive the pencil and finish the commitments" 0 1)
   else
    (h uiAddChoice: 40 "Begin the ending" 0 (== p14Phase 0))
    (h uiAddChoice: 41 "Read the current ending scene or credit" 0 (and (> p14Phase 0) (< p14Phase 6)))
    (h uiAddChoice: 42 "Continue after the complete scene" 0 (and (> p14Phase 0) (< p14Phase 6)))
    (if (== p14Phase 3) (h uiAddChoice: 207 "Quiet tag: walk with Milo to the living room" 0 0))
    (h uiAddChoice: 43 (if p14Paused "Resume ending" else "Pause ending") 0 (and (> p14Phase 0) (< p14Phase 6)))
    (h uiAddChoice: 44 "Skip the remaining presentation" 0 (and (> p14Phase 0) (< p14Phase 6)))
    (h uiAddChoice: 45 "Save the completed game" 0 1)
 (h uiAddChoice: 48 "Replay credits in a separate viewer" 0 (self p14Present: 5))

)))
 (= [h14MenuPaint 0] 0) (h dirty: 1) (return 1))
(method (h14Dispatch action obj target &tmp h wanted)
 (= h (ScriptID 0 0))
 (if (and (== action 0) (!= (h p02Exit: obj) -1)) (self h14Retire:) (return 0))
 (= wanted (or (self h14Owns: obj) (self h14Owns: target)
  (and (== obj 433) ((ScriptID 995 0) h13ReadyPhysical:))))
 (if (not wanted) (return 0))
 (if (or (not (self h14Base:)) (h onApron?) (h motionPhase?) (h uiPanel?)
  [h14Reader 0] [h14Edit 0] (h bridgeReaderActive?)) (return 1))
 (if (if [h14Owner 0] (not (self h14Reachable: (if target target else obj))) else (!= (h location?) 4)) (return 1))
 (return (self h14Menu: (if target target else obj))))
(method (h14Choice context id &tmp h source person)
 (if (!= context 256) (return 0)) (= h (ScriptID 0 0))
 (if (or (!= (h uiPanel?) 2) (!= (h uiChoiceContext?) 256) (== (h uiGetChoice: id) -1)
  (not (self h14Base:)) (h motionPhase?) (!= [h14MenuPaint 0] 3)
  (!= [h14MenuPaint 1] (h p02Revision?)) (!= [h14MenuPaint 2] (h location?))
  (!= [h14MenuPaint 3] [h14Selected 0]) (!= [h14MenuPaint 6] (h uiPage?))
  (!= [h14MenuPaint 7] (h uiChoiceCount?)) (!= (h p05ChoiceValue: (h uiPage?) 0) id) (!= [h14MenuPaint 4] p14RevisionHi) (!= [h14MenuPaint 5] p14RevisionLo)) (return 1))
 (= [h14MenuPaint 0] 0)
 (if (== id 1) (self h14DateOpen:) (return 1))
 (if (== id 2) (self h14Acquire:) (h uiPanel: 0 dirty: 1) (return 1))
 (if (and (>= id 20) (<= id 27)) (self h14Menu: (+ id 415)) (return 1))
 (if (== id 48) ((ScriptID 997 0) h14ReplayEnter:) (return 1))
 (if (not (self h14Ctx:)) (return 1))
 (= source 0) (= person (self p14CardIndex: [h14Selected 0]))
 (switch id
  (10 (= source 1)) (30 (= source 18)) (31 (= source 19))
  (32 (self p14RequestSignature: 0) (= source 20))
  (33 (self p14PinSignature:)) (34 (self p14GivePencil:))
  (35 (= source 21)) (36 (= source 22)) (37 (= source 23))
  (38 (self p14CompleteCommitments:))
  (40 (self p14StartFinale: H14_CREDIT_MASK0 H14_CREDIT_MASK1 H14_CREDIT_MASK2))
  (41 (self p14PresentFinale:) (= source (self p14CurrentSource:)))
  (42 (self p14AdvanceFinale:)) (43 (self p14PauseFinale: (not p14Paused)))
  (44 (self p14SkipFinale:)) (45 (h uiPanel: 0 uiBackPanel: 0) (h writeSave:) (return 1))

  (100 (if (>= person 0) (= source (+ person 10))))
  (140 (if (>= person 0) (self p14PinCard: person))))
 (if (and (>= id 120) (<= id 127) (>= person 0))
  (self p14GiveCard: person (- id 120))
  (if (== person (- id 120)) (= source (+ person 2))))
 (if source
  (self p14Begin: source)
  (if (== p14PresentationSource source) (self h14Open: source) (return 1)))
 ; Transfer custody is already committed by the literal domain, refresh before display.
 (self h14Ctx:) (h uiPanel: 0 uiBackPanel: 0 dirty: 1)
 (if (self p14Line: 0) (self h14Open: 0)) (return 1))
(method (h14Has) (return [h14Owner 0]))
(method (h14Base &tmp h)
 (= h (ScriptID 0 0))
 (return (and (== self (ScriptID 996 0)) ((ScriptID 995 0) h13ReadyPhysical:)
  (not (h opening?)) (not (h paused?)) (not (h menuOpen?)) (not (h uiFailure?)) (not (h bridgeFailure?))
  (not ((ScriptID 985 0) hBarrier:)) (not ((ScriptID 987 0) h6Barrier:)))))
(method (h14Valid &tmp i p h)
 (= p (ScriptID 995 0)) (= h (ScriptID 0 0))
 (if (or (!= [h14Owner 0] 1) (not (self p14Validate:)) (not (p h13ReadyPhysical:))
  (!= (p h13BoundaryCount:) 2046) (not ((ScriptID 990 0) h9OwnershipValid:))) (return 0))
 (if (not (self h14HistoryValid:)) (return 0))
 (if (or (< [h14Owner 1] 1) (> [h14Owner 1] (h p02Revision?))
  (and (!= [h14Owner 2] 4) (!= [h14Owner 2] 1))) (return 0))
 (if (== [h14Owner 2] 1)
  (if (or (< p14Phase 3) (!= [h14Owner 4] (+ [h14Owner 3] 1))
   (< [h14Owner 3] [h14Owner 1]) (> [h14Owner 4] (h p02Revision?))) (return 0)))
 (return 1))
(method (h14Room obj)
 (if (< ((ScriptID 995 0) h13Index: obj) 0) (return -2))
 (if (not [h14Owner 0]) (return ((ScriptID 995 0) h13Room: obj)))
 (if (not (self h14Valid:)) (return -1))
 (return (if (== obj H14_HOST_MILO) [h14Owner 2] else 4)))
(method (h14Owns obj)
 (return (and [h14Owner 0] (or (>= ((ScriptID 995 0) h13Index: obj) 0)
  (and (>= obj 435) (<= obj 442)) (== obj 25) (== obj 399) (== obj 433)))))
(method (h14Held obj)
 (if (not (self h14Valid:)) (return 0))
 (if (== obj 25) (return (not (self p14PencilWithFrankie:))))
 (if (== obj 399) (return (not (self p14Present: 2))))
 (return (and (>= obj 435) (<= obj 442) (not (self p14Present: (- obj 426))))))
(method (h14Location obj)
 (if (not (self h14Valid:)) (return -1))
 (if (>= ((ScriptID 995 0) h13Index: obj) 0) (return (self h14Room: obj)))
 (if (self h14Held: obj) (return 10)) (return 4))
(method (h14Reachable obj &tmp h)
 (= h (ScriptID 0 0))
 (return (and (self h14Base:) (not (h onApron?))
  (or (self h14Held: obj) (== (self h14Location: obj) (h location?))))))
(method (h14Acquire &tmp h p i)
 (= h (ScriptID 0 0)) (= p (ScriptID 995 0))
 (if [h14Owner 0] (return (self h14Valid:)))
 (if (or (not (self h14Base:)) (not (p h13AllHere:)) (h motionPhase?)
  (not [h14Date 0]) (not ((ScriptID 990 0) h9CardHeld: 399))
  (not (h campaignHeld: 25)) (not (self h14Ctx:)) (not [p14Held 25])) (return 0))
 (self p14StartCommitments: 399 1 0 0 14 2)
 (if (not (self p14Present: 1)) (return 0))
 ; Exact same mutation boundary owns the newly issued cards and original loans.
 (for ((= i 0)) (< i 2046) ((++ i)) (proc999_11 self i (p h13BoundaryWord: i) 1))
 (= [h14Owner 1] (h p02Revision?)) (= [h14Owner 2] 4) (= [h14Owner 0] 1)
 (p h13Retire:) (p h13Cancel:) (h dirty: 1) (return (self h14Valid:)))
(method (h14Travel before obj revision &tmp h)
 (= h (ScriptID 0 0))
 (if (not [h14Owner 0]) (return 1))
 ; Only the quiet tag needs a new room. Milo accompanies the actual exit.
 (if (and (== p14Phase 3) (== [h14Owner 2] 4) (== before 4) (== (h location?) 1)
  (== (h p02Exit: obj) 1) (== (h p02Revision?) (+ revision 1)))
  (= [h14Owner 3] revision) (= [h14Owner 4] (+ revision 1)) (= [h14Owner 2] 1))
 (self h14Retire:) (return (self h14Valid:)))
(method (h14Save)
(if (not ((ScriptID 997 0) h14ReplaySave:)) (return 0))

 (self h14Retire:) (= [h14Edit 0] 0)
 (return (or (not p14Initialized) (and (self p14Validate:) (or (not [h14Owner 0]) (self h14Valid:))))))
(method (h14Load phase)
(if (not ((ScriptID 997 0) h14ReplayLoad: phase)) (return 0))

 (self h14Retire:) (= [h14Edit 0] 0)
 (if (and (== phase 1) p14Initialized)
  (if (not (self p14AfterRestore:)) (return 0))
  (if [h14Owner 0] (return (self h14Valid:)))) (return 1))
(method (h14Stored success)
 ; Storage is explicitly tracked only after Main SaveGame's real return.
 (if (and success [h14Owner 0] (self p14Ready:))
  (= [h14Owner 5] (self p14SerialHi: 4)) (= [h14Owner 6] (self p14SerialLo: 4))) (return 1))
(method (h14HistoryValid &tmp i p) (= p (ScriptID 995 0))
 (for ((= i 0)) (< i 2046) ((++ i)) (if (!= (proc999_11 self i 0 0) (p h13BoundaryWord: i)) (return 0))) (return 1))
(method (h14RawRoom obj) (if (not [h14Owner 0]) (return ((ScriptID 995 0) h13Room: obj))) (return (if (== obj H14_HOST_MILO) [h14Owner 2] else 4)))
(method (h14Retire &tmp i)
(= [h14Reaction 0] 0)

(if ((ScriptID 980 0) dMode?) ((ScriptID 980 0) cancel: 14))

(if ((ScriptID 997 0) h14ReplayActive:) ((ScriptID 997 0) h14ReplayRetire:))

 (for ((= i 0)) (< i 24) ((++ i)) (= [h14Reader i] 0))
 (self p14Invalidate:) (proc999_1) (return 1))
(method (h14Open source &tmp h d record document i)
 (= h (ScriptID 0 0)) (= d (h dialogue?))
 (if (not (self h14Match:)) (return 0))
 (if (and source (or (!= p14PresentationSource source) (not (self p14Block: source 0 (- (self p14Capacity: source) 1))))) (return 0))
 (= record (if source (self p14SourceRecord: source) else (self p14Line: 0)))
 (= document (self h14Record: record)) (if (not document) (h uiPanel: 0 dirty: 1) (return 0))
 (for ((= i 0)) (< i 24) ((++ i)) (= [h14Reader i] 0))
 (= [h14Reader 0] 1) (= [h14Reader 1] document) (= [h14Reader 2] source) (= [h14Reader 3] p14Epoch)
 (= [h14Reader 4] (self p14SerialHi: (+ source 16))) (= [h14Reader 5] (self p14SerialLo: (+ source 16)))
 (= [h14Reader 8] (h location?)) (= [h14Reader 9] (h motionX?)) (= [h14Reader 10] (h motionY?))
 (= [h14Reader 16] record) (= [h14Reader 17] p14RevisionHi) (= [h14Reader 18] p14RevisionLo)
 (if (and (== document 1800) (not (self h14DateBind:))) (self h14Retire:) (return 0))
 (h speechCancel:) (h uiPanel: 0 uiBackPanel: 0)
 (if (not (h dialogueOpen: document)) (self h14Retire:) (return 0))
 (= [h14Reader 7] (d sdCount?)) (h dirty: 1) (return 1))
(method (h14ReaderCheck &tmp h d source row base i value)
 (= h (ScriptID 0 0)) (= d (h dialogue?)) (= source [h14Reader 2])
 (if (or (not [h14Reader 0]) (not (self h14Match:)) (!= d (ScriptID 982 0))
  (not (h scenePageIdentity:)) (!= (h uiDocument?) [h14Reader 1]) (!= (d sdDocument?) [h14Reader 1])
  (!= p14Epoch [h14Reader 3]) (!= (d sdResource?) 215) (d sdWindowValue: 2)
  (!= (d sdCount?) [h14Reader 7]) (!= (h motionX?) [h14Reader 9]) (!= (h motionY?) [h14Reader 10])
  (h bridgeReaderActive?) (d sdFailure?)) (return 0))
 (if source
  (if (or (!= [h14Reader 4] (self p14SerialHi: (+ source 16))) (!= [h14Reader 5] (self p14SerialLo: (+ source 16)))
   (!= [h14Reader 16] (self p14SourceRecord: source))
   (not (self p14Block: source 0 (- (self p14Capacity: source) 1)))) (return 0))
 else (if (or (!= p14RevisionHi [h14Reader 17]) (!= p14RevisionLo [h14Reader 18])) (return 0)))
 (if (== [h14Reader 1] 1800)
  (return (and (self h14DateMatch:) (== (d sdLineKey?) 1800) (== (d sdSpeaker?) 3)
   (== (d sdVoice?) 1) (== (d sdAudioModule?) 927) (== (d sdCount?) (proc999_5 0 0)))))
 (if (or (< [h14Reader 1] 1600) (> [h14Reader 1] 1798)) (return 0))
 (= row (- (+ (proc999_0 21 (- [h14Reader 1] 1600)) (d sdPage?)) 1552)) (= base (* row 8))
 (if (or (< row 0) (>= row 286) (not ((ScriptID 985 0) hStaticRange: 23 base 8))) (return 0))
 (for ((= i 0)) (< i 8) ((++ i))
  (= value (switch i (0 (d sdEntry?)) (1 (d sdLineKey?)) (2 (d sdPart?)) (3 (d sdPartCount?))
   (4 (d sdSpeaker?)) (5 (d sdVoice?)) (6 (d sdHeader?)) (7 (d sdBytes?))))
  (if (!= value (proc999_0 23 (+ base i))) (return 0)))
 (return (and (== (d sdAudioModule?) (proc999_0 25 row)) (== (d sdVoiceEnd?) (proc999_0 26 row))
  (== (d sdCount?) (proc999_0 22 (- [h14Reader 1] 1600))))))
(method (h14Frame phase &tmp h d source unit wasComplete)
(if ((ScriptID 997 0) h14ReplayActive:) (return ((ScriptID 997 0) h14ReplayFrame: phase)))

 (= h (ScriptID 0 0)) (= d (h dialogue?))
 (if (== phase 3) (return (or [h14Edit 0] [h14Reader 0])))
 (if (== phase 4) (= [h14Reaction 0] 0) (= [h14Reader 11] 0) (= [h14Reader 12] 0) (= [h14Reader 19] 0) (= [h14Edit 4] 0) (return 1))
 (if (== phase 0)
  (= [h14Reader 11] 0) (= [h14Reader 12] 0) (= [h14Reader 19] 0) (= [h14Edit 4] 0) (= [h14Freeze 0] 0)
  (if (and [h14Owner 0] (self p14FreezePending:) (not (h uiPanel?)) (not (h motionPhase?)) (self h14Ctx:))
   (= [h14Freeze 0] 1) (= [h14Freeze 1] p14Epoch) (= [h14Freeze 2] p14FinaleHi) (= [h14Freeze 3] p14FinaleLo))
  (if (not [h14Reader 0]) (return 0))
  (if (not (self h14ReaderCheck:)) (self h14Retire:) (return 0))
  (= [h14Reader 11] 1) (= [h14Reader 13] (d sdGeneration?)) (= [h14Reader 14] (d sdPage?))
  (d sdPaintGeneration: -1) (return 1))
 (if (== phase 2)
  (if (self h14DateDraw:) (= [h14Edit 4] 1))
  (if [h14Owner 0]
   (if (self h14Draw:)
    (if [h14Reader 11] (= [h14Reader 12] 1))
    (if [h14Freeze 0] (= [h14Freeze 0] 2)))) (return 1))
 (if (!= phase 1) (return 0))
 (self h14ReactionFrame: 0)
 (if [h14Edit 4] (Graph 12 0 0 200 320 1) (= [h14Edit 3] 1) (= [h14Edit 4] 0))
 (if (and (== [h14Freeze 0] 2) (self h14Match:) (== (h location?) 1) (== [h14Owner 2] 1)
  (not (h uiPanel?)) (not (h motionPhase?)) (not p14Paused))
  (Graph 12 0 0 200 320 1)
  (self p14AcknowledgeFreeze: [h14Freeze 2] [h14Freeze 3] [h14Freeze 1])
  (if (self p14Present: 6) (self h14Effect: 2)) (= [h14Freeze 0] 0))
 (if (or (not [h14Reader 11]) (not [h14Reader 12]) (not (self h14ReaderCheck:))
  (!= (d sdPaintGeneration?) [h14Reader 13]) (!= (d sdGeneration?) [h14Reader 13])
  (!= (d sdPage?) [h14Reader 14]) (!= (h uiPage?) [h14Reader 14])) (return 0))
 (Graph 12 0 0 200 320 1) (= [h14Reader 11] 0) (= [h14Reader 12] 0) (= [h14Reader 19] 1)
 (if (== [h14Reader 14] [h14Reader 6])
  (++ [h14Reader 6]) (= source [h14Reader 2])
  (if (and source (not [h14Reader 15]))
   (= wasComplete (self p14Complete: source))
   (= unit (self h14PageUnit: [h14Reader 1] [h14Reader 14]))
   (if unit (self p14Acknowledge: source [h14Reader 4] [h14Reader 5] [h14Reader 3] 0 unit unit))
   (if (== [h14Reader 6] [h14Reader 7])
    (self p14Acknowledge: source [h14Reader 4] [h14Reader 5] [h14Reader 3] [h14Reader 16] 0 0))
   (if (self p14Complete: source) (= [h14Reader 15] 1)
    (if (and (== source 28) (not wasComplete) (not (self p14Present: 8)))
     (= [h14Reaction 0] 1) (= [h14Reaction 1] [h14Reader 13])
     (= [h14Reaction 2] [h14Reader 14]) (= [h14Reaction 3] p14Epoch)
     (= [h14Reaction 4] [h14Reader 4]) (= [h14Reaction 5] [h14Reader 5])
     (= [h14Reaction 6] ((ScriptID 980 0) token?)) (= [h14Reaction 7] -1)))
   (if (== source 22) (self h14DateBind:)))) (return 1))
(method (h14Voice who &tmp h d obj)
(if ((ScriptID 997 0) h14ReplayActive:) (return 0))

 (= h (ScriptID 0 0)) (= d (h dialogue?))
 (if (or (< (h uiDocument?) 1600) (> (h uiDocument?) 1801)) (return -2))
 (if (or (not [h14Reader 19]) (!= (d sdSpeaker?) who) (not (d sdVoice?)) (not (or (== (d sdAudioModule?) 926) (and (== (d sdDocument?) 1800) (== who 3) (== (d sdAudioModule?) 927))))
  (!= (d sdGeneration?) [h14Reader 13]) (!= (d sdPage?) [h14Reader 14]) (not (self h14ReaderCheck:))) (return 0))
 (if (== who 1) (return 1)) (= obj ((ScriptID 994 0) h12VoiceObject: who))
 (return (and obj (== (self h14RawRoom: obj) (h location?)))))
(method (h14ControlOwn obj) (return (or (self h14Owns: obj) (and (== obj 433) ((ScriptID 995 0) h13ReadyPhysical:)))))
(method (h14Control obj)
 (if (not (self h14ControlOwn: obj)) (return 1))
 (if (not [h14Owner 0]) (return (and [h14Owner 7] (== ((ScriptID 0 0) location?) 4))))
 (return (and [h14Owner 7] (self h14Reachable: obj))))
(method (h14Controls &tmp h i obj x)
 (= h (ScriptID 0 0))
 (if (and (not [h14Owner 0]) (self h14Base:) (not (h uiPanel?)) (not (h onApron?)) (== (h location?) 4))
  (= [h14Owner 7] 1) (h uiAddControl: 1 433 128 158 144 310 "PROMISES AND ENDING") (= [h14Owner 7] 0) (return 1))
 (if (or (not [h14Owner 0]) (not (self h14Base:)) (not (self h14Valid:)) (h uiPanel?) (h onApron?)) (return 0))
 (= [h14Owner 7] 1)
 (for ((= i 0)) (< i 7) ((++ i)) (= obj ((ScriptID 995 0) h13Object: i))
  (if (== (self h14Room: obj) (h location?)) (= x ((ScriptID 994 0) h12SuccessorX: i))
   (h uiAddControl: 1 obj 62 x 124 (+ x 35) (self h14Label: obj))))
 (if (== (h location?) 4) (h uiAddControl: 1 433 128 158 144 310 "PROMISES AND ENDING"))
 (= [h14Owner 7] 0) (return 1))
(method (h14Draw &tmp h i obj x a d who mouth)
 (= h (ScriptID 0 0)) (= a (h presentation?)) (= d (h dialogue?))
 (if (or (not (self h14Valid:)) (not (self h14Base:)) (h onApron?)) (return 0))
 (for ((= i 0)) (< i 7) ((++ i)) (= obj ((ScriptID 995 0) h13Object: i))
  (if (== (self h14RawRoom: obj) (h location?))
   (= who ((ScriptID 994 0) h12SuccessorSpeaker: i)) (= mouth 0)
   (if (and (or (== (self h14Voice: who) 1)
 (and [h14Reader 11] (== (a lane?) 1) (== (d sdSpeaker?) who)
  (== (d sdGeneration?) [h14Reader 13]) (== (d sdPage?) [h14Reader 14])
  (or (== (d sdAudioModule?) 926)
   (and (== who 3) (== obj H14_HOST_FRANKIE) (== (d sdDocument?) 1800) (== (d sdAudioModule?) 927))) (self h14ReaderCheck:))) (== (a lane?) 1) (> (a ownerGain:) 0) (not (a silentClock?)) (== (a speaker?) who)
    (== (a token?) (d sdAudioToken?)) (>= (a mouth?) 0) (<= (a mouth?) 2)) (= mouth (a mouth?)))
   (DrawCel ((ScriptID 994 0) h12SuccessorView: i) 1 mouth ((ScriptID 994 0) h12SuccessorX: i) 64 -1 96 96)))
 (if (== (h location?) 4)
  (DrawCel 234 0 9 92 111 -1 0)
  (DrawCel 227 0 7 205 93 -1 0) (DrawCel 224 0 10 205 69 -1 0)
  (Graph 11 109 158 143 201 1 6 0 0)
  (for ((= i 0)) (< i 8) ((++ i))
   (if (self p14Present: (+ i 9)) (= x (+ 161 (* (mod i 4) 9)))
    (Graph 11 (+ 113 (* (/ i 4) 13)) x (+ 121 (* (/ i 4) 13)) (+ x 7) 1 15 0 0)))
  (if (self p14Present: 2) (Display "SIGNED" 100 203 128 102 2 105 1 106 64 121)))
 (if (and (== (h location?) 1) (== p14Phase 4))
  (Display "The End" 100 126 46 102 2 105 1 106 100 121))
 ; Additional used source credited on the existing real acknowledgments card.
 ; This is painted in the same reader frame, so original page receipts stay exact.
 (if (or (and (not ((ScriptID 997 0) h14ReplayActive:))
              (== (h uiPanel?) 4) (== [h14Reader 2] 53) (self h14ReaderCheck:)
              (== p14Phase 5) (== (self p14CurrentSource:) 53))
         (and ((ScriptID 997 0) h14ReplayActive:)
              (== ((ScriptID 997 0) p14CurrentSource:) 53)
              ((ScriptID 997 0) h14ReplayCheck:)))
  (Graph 11 52 4 143 316 1 4 0 0)
  (Graph 11 54 6 141 314 1 0 0 0)
  (Display "FINAL AUDIENCE CELEBRATION\nApplause - Blender Foundation / LeeZH\nCC BY 3.0\nopengameart.org/content/applause\ncreativecommons.org/licenses/by/3.0/\nAdapted: excerpt, mono resampling,\nfades and level adjustment.\nHearty laughter: ShangusBurger (CC0)\nFull source details: CREDITS.txt"
   100 12 57 102 15 105 0 106 296 121))
 (return 1))
(method (h14MenuFrame phase &tmp h)
 (= h (ScriptID 0 0))
 (if (or (!= (h uiPanel?) 2) (!= (h uiChoiceContext?) 256) (not (self h14Base:)) (h motionPhase?) (h onApron?))
  (= [h14MenuPaint 0] 0) (return 0))
 (if (== phase 0)
  (= [h14MenuPaint 0] 1) (= [h14MenuPaint 1] (h p02Revision?)) (= [h14MenuPaint 2] (h location?))
  (= [h14MenuPaint 3] [h14Selected 0]) (= [h14MenuPaint 4] p14RevisionHi) (= [h14MenuPaint 5] p14RevisionLo) (= [h14MenuPaint 6] (h uiPage?)) (= [h14MenuPaint 7] (h uiChoiceCount?)) (return 1))
 (if (== phase 2) (if (== [h14MenuPaint 0] 1) (= [h14MenuPaint 0] 2)) (return 1))
 (if (and (== phase 1) (== [h14MenuPaint 0] 2) (== [h14MenuPaint 1] (h p02Revision?))
  (== [h14MenuPaint 2] (h location?)) (== [h14MenuPaint 3] [h14Selected 0])
  (== [h14MenuPaint 4] p14RevisionHi) (== [h14MenuPaint 5] p14RevisionLo)
  (== [h14MenuPaint 6] (h uiPage?)) (== [h14MenuPaint 7] (h uiChoiceCount?)))
  (Graph 12 0 0 200 320 1) (= [h14MenuPaint 0] 3) (return 1)) (return 0))
(method (h14Effect kind &tmp h a slot)
 (= h (ScriptID 0 0)) (= a (h presentation?)) (= slot (if (== kind 1) 8 else 7))
 (if (or (not (self h14Match:)) (!= a (ScriptID 980 0)) (self p14Present: slot)) (return 0))
 (if (== kind 1) (self p14ClaimTagLaugh:) else (self p14ClaimCelebration:))
 (if (not (self p14Present: slot)) (return 0))
 ; Sole existing PCM owner arbitrates speech/laugh/effects; consumption survives mute.
 (proc945_1 h (if (== kind 1) 14 else 15) 996 (self p14SerialHi: slot) (self p14SerialLo: slot) (a token?) (GetTime)) (return 1))
(method (h14Record key) (return (proc999_9 key)))
(method (h14PageUnit doc page) (return (proc999_10 doc page)))

(method (h14PersistWord index) (return (proc999_8 self index)))

























(method (h14ReactionFrame stop &tmp h d a)
 (if stop (= [h14Reaction 0] 0) (return 1))
 (if (not [h14Reaction 0]) (return 0))
 (= h (ScriptID 0 0)) (= d (h dialogue?)) (= a (h presentation?))
 (if (or (!= self (ScriptID 996 0)) (!= a (ScriptID 980 0))
  (!= d (ScriptID 982 0)) (not (self h14Match:)) (not (self h14ReaderCheck:))
  (!= [h14Reader 2] 28) (!= p14Phase 3) p14Paused (self p14Present: 8)
  (!= (h uiPanel?) 4) (!= (d sdGeneration?) [h14Reaction 1])
  (!= (d sdPage?) [h14Reaction 2]) (!= p14Epoch [h14Reaction 3])
  (!= (self p14SerialHi: 44) [h14Reaction 4])
  (!= (self p14SerialLo: 44) [h14Reaction 5]))
  (= [h14Reaction 0] 0) (return 0))
 (if (== [h14Reaction 7] -1)
  ; The newly displayed final page must first receive its ordinary PCM token.
  (if (== (a token?) [h14Reaction 6]) (return 0))
  (if (!= (d sdAudioToken?) (a token?)) (= [h14Reaction 0] 0) (return 0))
  (= [h14Reaction 7] (a token?)))
 (if (!= (a token?) [h14Reaction 7]) (= [h14Reaction 0] 0) (return 0))
 (if (a lane?) (return 0))
 (= [h14Reaction 0] 0)
 (return (self h14Effect: 1)))
)
(instance p14State of P14State)
