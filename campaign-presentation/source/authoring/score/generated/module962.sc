;;; Sierra Script 1.0 - (do not remove this comment)
; New transition-ready arrangement transport; source/emitted-only candidate.
(script# 962)
(use "module981")
(public cue115ReadyTransport 0 cue115Verify 1 cue115Validate 2)
(local
 [currentGains 8] = [ 0 0 0 0 0 0 0 0 ]
 [targetGains 8] = [ 0 0 0 0 0 0 0 0 ]
 [historyTableA 191] = [ 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ]
 [historyTableB 191] = [ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ]
 [midiChannels 8] = [ 0 1 2 3 4 5 6 9 ]
 [mainStateGains 8] = [ 110 107 70 112 109 96 94 98 ]
 [reducedStateGains 8] = [ 99 83 0 71 73 44 0 59 ]
 [midiPrograms 8] = [ 33 0 48 11 71 27 11 0 ]
 [midiPans 8] = [ 64 49 75 55 75 82 40 64 ]
 [initialExpression 8] = [ 127 127 127 100 100 127 127 127 ]
 [loopExpression 8] = [ 127 127 127 96 96 127 127 127 ]
 [expressionEvents 144] = [ 12 3 90 45 3 96 79 3 103 112 3 100 145 3 98 279 3 110 412 3 105 545 3 100 679 3 96 812 3 90 912 3 94 999 3 96 1079 4 90 1112 4 96 1145 4 103 1179 4 100 1212 4 98 1345 4 110 1479 4 105 1612 4 100 1745 4 96 1879 4 90 1979 4 94 2065 4 96 2145 3 90 2179 3 96 2212 3 103 2245 3 100 2279 3 98 2412 3 110 2545 3 105 2679 3 100 2812 3 96 2945 3 90 3045 3 94 3132 3 96 3212 4 90 3245 4 96 3279 4 103 3312 4 100 3345 4 98 3479 4 110 3612 4 105 3745 4 100 3879 4 96 4012 4 90 4112 4 94 4199 4 96 ]
 [keyWindows 955] = [ 18 22 30 0 4 32 38 45 16 2 58 58 65 24 1 70 72 79 28 1 86 88 95 32 4 102 104 111 48 2 124 124 131 56 1 136 138 145 60 1 152 156 164 64 2 168 172 179 72 2 234 238 245 80 1 258 258 265 84 1 270 270 278 88 1 286 288 296 92 4 302 304 311 108 2 324 324 332 116 1 336 338 345 120 1 352 354 362 124 4 368 370 378 140 2 404 404 411 148 1 418 424 431 152 2 434 438 445 160 2 486 490 498 168 2 502 504 512 176 2 524 524 531 184 1 536 538 545 188 1 552 556 563 192 4 592 592 599 208 1 618 622 629 212 4 634 638 645 228 2 658 658 665 236 1 670 670 678 240 1 686 704 712 244 2 724 724 731 252 1 760 770 778 256 2 792 792 799 264 1 818 822 830 268 4 834 838 845 284 2 858 858 865 292 1 886 888 895 296 4 902 904 912 312 2 924 924 931 320 1 952 954 962 324 2 968 970 978 332 1 984 990 998 336 1 1018 1036 1044 340 2 1052 1054 1061 348 4 1070 1070 1077 364 2 1086 1104 1112 372 2 1124 1124 1131 380 1 1136 1138 1145 384 1 1152 1158 1165 388 2 1168 1170 1178 396 2 1204 1204 1211 404 1 1218 1224 1231 408 2 1234 1238 1245 416 2 1258 1258 1265 424 1 1270 1272 1279 428 1 1286 1290 1298 432 2 1300 1304 1312 440 1 1324 1324 1331 444 1 1336 1338 1345 448 1 1352 1356 1363 452 4 1368 1370 1378 468 2 1392 1392 1399 476 1 1404 1404 1412 480 1 1418 1422 1429 484 4 1434 1438 1445 500 2 1458 1458 1465 508 1 1470 1470 1478 512 1 1486 1490 1498 516 2 1502 1504 1511 524 2 1524 1524 1531 532 1 1552 1558 1565 536 2 1568 1572 1579 544 2 1604 1604 1612 552 1 1618 1622 1630 556 4 1658 1658 1665 572 1 1686 1688 1695 576 4 1702 1704 1712 592 2 1724 1724 1732 600 1 1736 1738 1745 604 1 1752 1772 1779 608 2 1826 1838 1845 616 2 1858 1858 1865 624 1 1886 1888 1896 628 4 1902 1904 1912 644 2 1924 1924 1931 652 1 1952 1954 1962 656 4 1968 1972 1979 672 2 2018 2022 2029 680 2 2034 2038 2045 688 1 2052 2056 2064 692 1 2086 2104 2111 696 2 2118 2120 2127 704 4 2136 2136 2143 720 2 2152 2156 2163 728 3 2168 2170 2178 740 2 2204 2204 2211 748 1 2218 2222 2229 752 4 2234 2236 2244 768 2 2286 2304 2312 776 2 2324 2324 2332 784 1 2358 2372 2379 788 1 2392 2392 2399 792 0 2404 2404 2411 792 1 2418 2422 2430 796 4 2434 2438 2445 812 2 2524 2524 2531 820 1 2552 2556 2564 824 2 2568 2572 2579 832 2 2624 2624 2631 840 2 2686 2690 2697 848 2 2702 2704 2711 856 2 2724 2724 2731 864 1 2736 2736 2744 868 2 2752 2756 2764 876 2 2768 2770 2778 884 2 2784 2792 2799 892 2 2818 2824 2831 900 2 2834 2834 2842 908 4 2852 2854 2862 924 2 2902 2902 2909 932 3 2918 2922 2929 944 1 2936 2938 2945 948 0 2952 2956 2963 948 4 2968 2970 2978 964 2 3004 3004 3012 972 0 3018 3022 3029 972 3 3032 3038 3045 984 1 3058 3058 3065 988 0 3070 3072 3079 988 0 3086 3104 3112 988 1 3124 3124 3132 992 0 3152 3172 3179 992 1 3192 3192 3199 996 0 3204 3204 3212 996 0 3218 3222 3230 996 4 3232 3238 3245 1012 2 3270 3272 3279 1020 1 3286 3288 3295 1024 4 3302 3304 3311 1040 2 3324 3324 3331 1048 1 3336 3338 3345 1052 1 3352 3356 3364 1056 2 3368 3372 3379 1064 2 3434 3438 3445 1072 1 3458 3458 3465 1076 1 3470 3470 3478 1080 1 3486 3488 3496 1084 4 3502 3504 3511 1100 2 3524 3524 3532 1108 1 3536 3538 3545 1112 1 3552 3554 3562 1116 4 3568 3570 3578 1132 2 3604 3604 3611 1140 1 3618 3624 3631 1144 2 3634 3638 3645 1152 2 3686 3690 3698 1160 2 3702 3704 3712 1168 2 3724 3724 3731 1176 1 3736 3738 3745 1180 1 3752 3756 3763 1184 4 3792 3792 3799 1200 1 3818 3822 3829 1204 4 3834 3838 3845 1220 2 3858 3858 3865 1228 1 3870 3870 3878 1232 1 3886 3904 3912 1236 2 3924 3924 3931 1244 1 3958 3970 3978 1248 2 3992 3992 3999 1256 1 4018 4022 4030 1260 4 4034 4038 4045 1276 2 4058 4058 4065 1284 1 4086 4088 4095 1288 4 4102 4104 4112 1304 2 4124 4124 4131 1312 1 4152 4154 4162 1316 2 4168 4170 4178 1324 1 4184 4190 4198 1328 1 4218 4236 4244 1332 2 4252 4252 4260 1340 4 4286 4288 4296 1356 3 4298 4304 4312 1368 1 4324 4324 4332 1372 0 4336 4338 4345 1372 0 4352 4354 4362 1372 3 4364 4372 4379 1384 1 4392 4392 4399 1388 0 4404 4404 4412 1388 0 ]
 [heldNotes 1388] = [ 0 41 66 55 1 57 54 30 1 64 54 30 3 64 72 65 0 41 66 55 3 64 72 65 3 64 72 65 3 64 69 98 0 48 61 122 1 57 49 95 1 64 49 95 3 64 69 98 0 48 61 122 3 69 69 111 3 70 69 131 3 69 69 145 0 45 66 189 3 67 73 164 0 45 66 189 3 70 73 198 0 52 61 255 3 70 73 265 3 69 73 278 0 38 66 322 1 60 54 296 1 53 54 296 3 65 82 298 0 38 66 322 3 65 79 311 3 65 79 365 3 65 79 365 0 45 61 389 1 60 49 362 1 53 49 362 3 65 79 365 0 45 61 389 3 69 79 378 3 69 79 411 0 36 66 455 3 67 77 431 0 36 66 455 3 65 77 445 0 48 61 522 3 69 77 498 0 48 61 522 3 65 77 531 3 65 77 531 3 65 77 565 0 46 66 589 1 57 54 563 1 62 54 563 3 65 77 565 3 69 74 604 0 53 61 655 1 57 49 629 1 62 49 629 3 69 74 631 0 53 61 655 3 69 74 678 3 69 74 678 3 69 74 678 0 46 66 722 3 70 72 731 3 70 72 731 0 53 61 789 3 70 72 778 3 70 72 804 0 45 66 855 1 55 54 830 1 60 54 830 3 67 72 831 0 45 66 855 3 67 69 865 3 67 69 865 0 45 61 922 1 60 49 895 1 53 49 895 3 65 69 898 0 45 61 922 3 69 69 931 3 69 69 931 0 43 60 962 3 70 69 965 3 69 66 978 3 70 66 998 0 36 61 1044 3 69 66 1045 0 36 60 1077 1 64 49 1061 1 58 49 1061 3 67 66 1078 0 36 60 1077 3 67 66 1078 0 41 46 1122 4 64 64 1131 4 64 64 1131 4 64 61 1165 0 48 43 1189 4 64 61 1165 0 48 43 1189 4 69 61 1178 4 69 61 1211 0 45 46 1255 4 67 64 1231 0 45 46 1255 4 70 64 1265 4 70 64 1265 4 69 64 1298 0 52 43 1322 4 69 64 1298 0 52 43 1322 4 70 64 1331 4 69 64 1345 0 38 66 1389 1 60 54 1363 1 53 54 1363 4 65 73 1364 0 38 66 1389 4 65 70 1378 4 65 70 1431 4 65 70 1431 0 45 61 1455 1 60 49 1429 1 53 49 1429 4 65 70 1431 0 45 61 1455 4 69 70 1445 4 70 70 1465 4 69 70 1478 0 36 66 1522 4 67 73 1498 0 36 66 1522 4 65 73 1511 4 67 73 1531 0 48 61 1589 4 69 73 1565 0 48 61 1589 4 65 73 1598 4 65 73 1631 0 46 66 1655 1 57 54 1630 1 62 54 1630 4 65 73 1631 4 69 78 1671 0 53 61 1722 1 57 49 1695 1 62 49 1695 4 69 78 1698 0 53 61 1722 4 69 78 1745 4 69 78 1745 4 69 78 1745 0 46 66 1789 4 70 81 1798 0 53 61 1855 4 70 81 1845 4 70 81 1871 0 45 66 1922 1 55 54 1896 1 60 54 1896 4 67 78 1898 0 45 66 1922 4 67 75 1931 4 67 75 1931 0 45 61 1989 1 60 49 1962 1 53 49 1962 4 65 75 1965 0 45 61 1989 4 69 75 1998 0 43 60 2029 4 70 75 2031 4 69 70 2045 4 70 70 2064 0 36 61 2111 4 69 70 2111 0 36 60 2143 1 64 49 2127 1 58 49 2127 4 67 70 2145 0 36 60 2143 4 67 70 2145 0 41 66 2189 1 63 54 2163 1 56 54 2163 0 41 66 2189 3 72 64 2178 3 72 64 2211 0 48 61 2255 1 63 49 2229 1 56 49 2229 3 84 64 2231 0 48 61 2255 3 82 64 2244 0 40 66 2322 3 79 68 2345 3 79 68 2345 0 47 61 2389 3 67 68 2411 0 37 66 2455 1 53 54 2430 1 59 54 2430 3 66 74 2431 0 37 66 2455 3 87 71 2454 3 65 71 2531 0 36 66 2589 3 67 75 2564 0 36 66 2589 3 86 75 2587 0 43 61 2655 3 64 75 2631 0 41 51 2722 3 72 75 2697 0 41 51 2722 3 70 72 2711 3 72 72 2731 0 43 60 2744 3 74 72 2745 0 50 48 2778 3 72 72 2764 0 50 48 2778 3 72 72 2778 0 44 60 2810 3 72 72 2811 0 44 66 2831 3 72 68 2831 0 43 60 2862 1 59 49 2842 1 65 49 2842 3 71 68 2865 0 43 60 2862 3 71 68 2865 0 43 60 2929 1 59 49 2909 1 65 49 2909 0 43 60 2929 0 36 66 2989 1 64 54 2963 1 59 54 2963 3 72 68 2964 0 36 66 2989 3 76 65 2978 0 43 61 3055 1 64 49 3029 1 59 49 3029 0 43 61 3055 0 36 66 3122 0 43 61 3189 0 41 59 3255 1 57 49 3230 1 64 49 3230 4 64 73 3264 0 41 59 3255 4 64 73 3264 4 64 70 3298 0 48 55 3322 1 57 44 3295 1 64 44 3295 4 64 70 3298 0 48 55 3322 4 69 70 3311 4 70 70 3331 4 69 70 3345 0 45 59 3389 4 67 73 3364 0 45 59 3389 4 70 73 3398 0 52 55 3455 4 70 73 3465 4 69 73 3478 0 38 66 3522 1 60 54 3496 1 53 54 3496 4 65 80 3498 0 38 66 3522 4 65 77 3511 4 65 77 3565 4 65 77 3565 0 45 61 3589 1 60 49 3562 1 53 49 3562 4 65 77 3565 0 45 61 3589 4 69 77 3578 4 69 77 3611 0 36 66 3655 4 67 78 3631 0 36 66 3655 4 65 78 3645 0 48 61 3722 4 69 78 3698 0 48 61 3722 4 65 78 3731 4 65 78 3731 4 65 78 3765 0 46 66 3789 1 57 54 3763 1 62 54 3763 4 65 78 3765 4 69 74 3804 0 53 61 3855 1 57 49 3829 1 62 49 3829 4 69 74 3831 0 53 61 3855 4 69 74 3878 4 69 74 3878 4 69 74 3878 0 46 66 3922 4 70 71 3931 4 70 71 3931 0 53 61 3989 4 70 71 3978 4 70 71 4004 0 45 66 4055 1 55 54 4030 1 60 54 4030 4 67 71 4031 0 45 66 4055 4 67 68 4065 4 67 68 4065 0 45 61 4122 1 60 49 4095 1 53 49 4095 4 65 68 4098 0 45 61 4122 4 69 68 4131 4 69 68 4131 0 43 60 4162 4 70 68 4165 4 69 66 4178 4 70 66 4198 0 36 61 4244 4 69 66 4245 0 36 60 4276 1 64 49 4260 1 58 49 4260 4 67 66 4278 0 41 66 4322 1 57 54 4296 1 60 54 4296 0 41 66 4322 0 48 61 4389 1 57 49 4362 1 60 49 4362 0 48 61 4389 ]
 [stateGains 16] = [ 110 107 70 112 109 96 94 98 99 83 0 71 73 44 0 59 ]
 [cue115Buffer 64]
)
(procedure (cue115Verify &tmp index slot word digit value i)
(for ((= i 0)) (< i 64) ((++ i)) (= [cue115Buffer i] 0))
(for ((= index 0)) (< index 191) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 0 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [historyTableA index] value) (return 0)))
(for ((= index 0)) (< index 191) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 10 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [historyTableB index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 20 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiChannels index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 21 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [mainStateGains index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 22 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [reducedStateGains index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 23 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiPrograms index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 24 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiPans index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 25 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [initialExpression index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 26 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [loopExpression index] value) (return 0)))
(for ((= index 0)) (< index 144) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 27 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [expressionEvents index] value) (return 0)))
(for ((= index 0)) (< index 955) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 35 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [keyWindows index] value) (return 0)))
(for ((= index 0)) (< index 1388) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 83 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [heldNotes index] value) (return 0)))
(for ((= index 0)) (< index 16) ((++ index))
(if (== (mod index 20) 0) (GetFarText 272 (+ 153 (/ index 20)) @cue115Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue115Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue115Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [stateGains index] value) (return 0)))
(return 1))
(procedure (cue115Validate sound &tmp i value wanted)
(if (not (cue115Verify)) (return 0))
(if (or (not (IsObject sound)) (!= (sound number?) 115)) (return 0))
(if (or (!= (cue115ReadyTransport musicBed?) sound) (!= (cue115ReadyTransport ownedBed?) sound)) (return 0))
(= wanted (cue115ReadyTransport nextRequestedState?))
(if (or (< wanted 0) (> wanted 1)) (return 0))
(= value (cue115ReadyTransport wholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue115ReadyTransport desiredWholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue115ReadyTransport savedWholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue115ReadyTransport transportMode?))
(if (or (< value 0) (> value 9)) (return 0))
(= value (cue115ReadyTransport resumeMode?))
(if (or (< value 0) (> value 9)) (return 0))
(= value (cue115ReadyTransport settledState?))
(if (or (< value -1) (> value 1)) (return 0))
(= value (cue115ReadyTransport musicPosition?))
(if (or (< value 0) (> value 4411)) (return 0))
(= value (cue115ReadyTransport pausedPosition?))
(if (or (< value 0) (> value 4411)) (return 0))
(= value (cue115ReadyTransport previousPosition?))
(if (or (< value -1) (> value 4411)) (return 0))
(= value (cue115ReadyTransport recoveryLastPosition?))
(if (or (< value -1) (> value 4411)) (return 0))
(= value (cue115ReadyTransport rejoinWindow?))
(if (or (< value -1) (> value 190)) (return 0))
(= value (cue115ReadyTransport historyWindow?))
(if (or (< value -1) (> value 190)) (return 0))
(= value (cue115ReadyTransport lastBatchKeys?))
(if (or (< value 0) (> value 32)) (return 0))
(= value (cue115ReadyTransport recoverySamples?))
(if (or (< value 0) (> value 32767)) (return 0))
(= value (cue115ReadyTransport recoveryReason?))
(if (or (< value 0) (> value 10)) (return 0))
(= value (cue115ReadyTransport historyRoute?))
(if (or (< value 0) (> value 10)) (return 0))
(= value (cue115ReadyTransport requestRevision?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue115ReadyTransport saveRevision?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue115ReadyTransport previousGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue115ReadyTransport loopEpoch?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue115ReadyTransport rejoinEpoch?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue115ReadyTransport lifecycleGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue115ReadyTransport recoveryGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue115ReadyTransport gainRefreshes?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue115ReadyTransport historyEpisodes?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue115ReadyTransport rejoinAttempts?))
(if (or (< value 0) (> value 32)) (return 0))
(= value (cue115ReadyTransport musicRunning?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue115ReadyTransport musicPaused?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue115ReadyTransport ownedPauseHeld?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue115ReadyTransport pausePhaseKnown?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue115ReadyTransport pausedCheckpoint?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue115ReadyTransport recoveryPhaseKnown?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue115ReadyTransport musicMuted?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue115ReadyTransport loopHasWrapped?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue115ReadyTransport saveGuard?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue115ReadyTransport remapGuard?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue115ReadyTransport remapDrain?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue115ReadyTransport positionUncertain?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue115ReadyTransport recoveryWrapped?))
(if (or (< value 0) (> value 1)) (return 0))
(if (or (!= (cue115ReadyTransport musicMuted?) (if (cue115ReadyTransport musicMuted?) 1 else 0)) (< (cue115ReadyTransport transportMode?) 1)) (return 0))
(if (and (cue115ReadyTransport recoveryBed?) (!= (cue115ReadyTransport recoveryBed?) sound)) (return 0))
(if (!= (cue115ReadyTransport musicRunning?) 1) (return 0))
(if (and (cue115ReadyTransport pausedCheckpoint?) (not (cue115ReadyTransport saveGuard?))) (return 0))
(if (and (cue115ReadyTransport saveGuard?) (not (cue115ReadyTransport ownedPauseHeld?))) (return 0))
(for ((= i 0)) (< i 8) ((++ i))
(if (or (< [currentGains i] 0) (> [currentGains i] 127)) (return 0))
(if (!= [targetGains i] [stateGains (+ (* wanted 8) i)]) (return 0)))
(return 1))
(instance cue115ReadyTransport of MusicTransport
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
            pushi 4412
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
            ldi 115
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
            ldi 4412
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
            label_057b: pushi 4412
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
            ldi 191
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
            ldi 115
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
            ldi 4288
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
            label_07c5: pushi 4412
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
            ldi 4288
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
            label_0951: pushi 4412
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
        (if (not (cue115Verify))
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
            ldi 115
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
        (if (not (cue115Verify))
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
        (if (not (cue115Verify))
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
        (if (not (cue115Verify))
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
        (if (not (cue115Verify))
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
            ldi 191
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
            ldi 4404
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

