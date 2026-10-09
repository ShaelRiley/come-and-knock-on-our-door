;;; Sierra Script 1.0 - (do not remove this comment)
; New transition-ready arrangement transport; source/emitted-only candidate.
(script# 959)
(use "module981")
(public cue112ReadyTransport 0 cue112Verify 1 cue112Validate 2)
(local
 [currentGains 8] = [ 0 0 0 0 0 0 0 0 ]
 [targetGains 8] = [ 0 0 0 0 0 0 0 0 ]
 [historyTableA 188] = [ 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ]
 [historyTableB 188] = [ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ]
 [midiChannels 8] = [ 0 1 2 3 4 5 6 9 ]
 [mainStateGains 8] = [ 110 107 70 112 109 96 94 98 ]
 [reducedStateGains 8] = [ 99 83 0 71 73 44 0 59 ]
 [midiPrograms 8] = [ 33 4 48 71 59 27 11 0 ]
 [midiPans 8] = [ 64 49 75 55 75 82 40 64 ]
 [initialExpression 8] = [ 127 127 127 100 100 127 127 127 ]
 [loopExpression 8] = [ 127 127 127 96 96 127 127 127 ]
 [expressionEvents 144] = [ 12 3 90 45 3 96 77 3 103 110 3 100 143 3 98 274 3 110 405 3 105 536 3 100 667 3 96 797 3 90 896 3 94 981 3 96 1059 4 90 1092 4 96 1125 4 103 1157 4 100 1190 4 98 1321 4 110 1452 4 105 1583 4 100 1714 4 96 1845 4 90 1943 4 94 2028 4 96 2107 3 90 2139 3 96 2172 3 103 2205 3 100 2237 3 98 2368 3 110 2499 3 105 2630 3 100 2761 3 96 2892 3 90 2990 3 94 3075 3 96 3154 4 90 3186 4 96 3219 4 103 3252 4 100 3285 4 98 3416 4 110 3546 4 105 3677 4 100 3808 4 96 3939 4 90 4037 4 94 4122 4 96 ]
 [keyWindows 940] = [ 18 22 30 0 3 34 36 44 12 2 70 70 77 20 1 84 88 96 24 2 100 102 109 32 2 122 122 129 40 1 150 168 176 44 2 188 188 195 52 1 200 200 208 56 1 224 234 241 60 1 254 254 261 64 0 266 266 273 64 1 280 284 291 68 4 296 300 307 84 2 318 318 325 92 1 384 384 391 96 1 412 416 423 100 2 426 430 437 108 2 542 546 553 116 4 558 560 568 132 2 580 580 587 140 1 608 612 619 144 2 624 626 633 152 2 640 642 649 160 4 672 678 685 176 2 688 688 696 184 4 706 708 716 200 2 724 724 732 208 0 754 754 762 208 3 770 774 781 220 1 790 790 797 224 0 804 808 815 224 4 820 822 830 240 2 854 856 863 248 0 870 888 896 248 1 908 908 915 252 0 920 920 928 252 0 934 954 961 252 1 974 974 981 256 0 986 986 994 256 0 1000 1000 1008 256 3 1010 1020 1027 268 1 1038 1038 1046 272 0 1052 1052 1059 272 0 1066 1072 1079 272 1 1082 1084 1091 276 2 1116 1116 1124 284 1 1132 1136 1144 288 2 1146 1150 1157 296 2 1196 1216 1223 304 2 1236 1236 1243 312 1 1248 1248 1255 316 1 1262 1280 1288 320 1 1300 1300 1308 324 0 1312 1312 1320 324 1 1328 1332 1339 328 4 1344 1346 1354 344 2 1366 1366 1373 352 1 1398 1398 1405 356 2 1458 1462 1470 364 2 1474 1478 1485 372 2 1562 1562 1569 380 1 1590 1594 1601 384 4 1606 1608 1615 400 2 1654 1660 1667 408 2 1670 1672 1680 416 2 1688 1688 1696 424 4 1720 1724 1732 440 2 1736 1736 1743 448 4 1752 1756 1763 464 2 1772 1772 1779 472 0 1802 1802 1809 472 3 1818 1820 1828 484 1 1836 1838 1845 488 0 1852 1854 1862 488 4 1866 1870 1877 504 2 1902 1902 1910 512 0 1916 1936 1943 512 1 1956 1956 1963 516 0 1968 1968 1976 516 0 1982 2000 2008 516 1 2020 2020 2028 520 0 2032 2034 2041 520 0 2048 2048 2055 520 3 2058 2066 2074 532 1 2086 2086 2093 536 0 2098 2100 2107 536 0 2114 2116 2124 536 4 2128 2128 2136 552 4 2146 2148 2156 568 2 2164 2164 2171 576 1 2178 2182 2190 580 2 2194 2196 2204 588 2 2210 2212 2220 596 4 2244 2262 2269 612 2 2282 2282 2290 620 1 2294 2294 2301 624 1 2342 2344 2352 628 2 2360 2360 2368 636 1 2374 2378 2386 640 4 2390 2392 2400 656 2 2426 2426 2434 664 0 2440 2446 2453 664 1 2456 2458 2466 668 2 2472 2474 2481 676 4 2506 2510 2518 692 2 2522 2522 2529 700 4 2538 2540 2548 716 2 2556 2556 2564 724 1 2572 2572 2579 728 4 2582 2590 2597 744 2 2610 2610 2617 752 1 2622 2622 2630 756 1 2636 2656 2663 760 2 2688 2688 2696 768 1 2702 2720 2727 772 2 2734 2740 2748 780 2 2752 2752 2759 788 2 2768 2772 2780 796 2 2784 2786 2794 804 2 2806 2806 2813 812 1 2844 2852 2859 816 1 2872 2872 2879 820 0 2884 2884 2892 820 0 2898 2902 2910 820 3 2912 2918 2925 832 1 2936 2936 2944 836 0 2950 2950 2957 836 0 2964 2982 2990 836 1 3002 3002 3010 840 0 3014 3016 3023 840 0 3030 3048 3056 840 1 3068 3068 3075 844 0 3080 3080 3088 844 0 3094 3094 3102 844 3 3104 3114 3121 856 1 3134 3134 3141 860 0 3146 3146 3154 860 0 3160 3164 3171 860 3 3176 3178 3186 872 2 3198 3198 3205 880 1 3226 3230 3238 884 2 3242 3244 3251 892 2 3264 3264 3271 900 1 3292 3310 3317 904 2 3330 3330 3337 912 1 3342 3342 3349 916 1 3366 3376 3383 920 1 3408 3408 3415 924 1 3422 3426 3433 928 4 3438 3440 3448 944 2 3460 3460 3467 952 1 3526 3526 3533 956 1 3552 3558 3565 960 2 3568 3572 3579 968 2 3656 3656 3663 976 1 3684 3688 3695 980 4 3700 3702 3710 996 2 3722 3722 3729 1004 1 3750 3754 3761 1008 2 3764 3768 3775 1016 2 3782 3782 3790 1024 4 3814 3820 3827 1040 2 3830 3830 3838 1048 4 3848 3850 3858 1064 2 3866 3866 3874 1072 0 3896 3896 3903 1072 3 3912 3916 3923 1084 1 3930 3932 3939 1088 0 3946 3950 3957 1088 4 3962 3964 3971 1104 2 3996 3998 4005 1112 0 4012 4030 4037 1112 1 4050 4050 4057 1116 0 4062 4062 4070 1116 0 4076 4096 4103 1116 1 4128 4128 4136 1120 0 4142 4142 4150 1120 3 4152 4160 4168 1132 1 4180 4180 4188 1136 0 4192 4194 4201 1136 0 4208 4212 4219 1136 3 4222 4226 4234 1148 1 4246 4246 4253 1152 0 4258 4258 4266 1152 0 4272 4292 4299 1152 1 4312 4312 4319 1156 0 4324 4324 4332 1156 0 ]
 [heldNotes 1156] = [ 0 41 66 55 1 56 54 30 1 63 54 30 0 41 66 55 3 72 69 44 3 72 69 77 0 48 61 120 3 84 69 96 0 48 61 120 3 82 69 109 3 84 69 129 0 40 66 185 3 79 73 208 3 79 73 208 3 79 73 208 0 47 61 251 3 67 73 273 0 37 66 316 1 53 54 291 1 59 54 291 3 66 82 293 0 37 66 316 3 87 79 315 3 77 79 325 3 65 79 391 0 36 66 447 3 67 77 423 0 36 66 447 3 86 77 446 0 41 66 578 1 56 54 553 1 63 54 553 3 72 77 554 0 41 66 578 3 70 74 568 3 72 74 587 0 50 61 633 3 72 74 619 0 50 61 633 3 72 74 633 0 44 60 664 1 63 49 649 1 60 49 649 3 72 74 665 0 44 66 685 3 72 72 685 0 43 60 716 1 59 49 696 1 65 49 696 3 71 72 719 0 43 60 716 3 71 72 719 0 43 60 781 1 53 49 762 1 71 49 762 0 43 60 781 0 36 66 840 1 59 54 815 1 64 54 815 3 72 72 816 0 36 66 840 3 76 69 830 0 43 61 905 0 36 66 971 0 43 61 1036 1 64 49 1008 1 58 49 1008 0 43 61 1036 0 41 46 1102 0 41 46 1102 4 72 61 1091 4 72 61 1124 0 48 43 1167 4 84 61 1144 0 48 43 1167 4 82 61 1157 0 40 46 1233 4 79 64 1255 4 79 64 1255 4 79 64 1255 0 47 43 1298 4 67 64 1320 0 37 66 1364 1 59 54 1339 1 65 54 1339 4 66 73 1340 0 37 66 1364 4 87 70 1362 4 77 70 1373 0 44 61 1429 4 65 70 1405 0 36 66 1495 4 67 73 1470 0 36 66 1495 4 86 73 1493 4 64 73 1569 0 41 66 1625 1 56 54 1601 1 63 54 1601 4 72 81 1601 0 41 66 1625 4 70 78 1615 0 50 61 1680 4 72 78 1667 0 50 61 1680 4 72 78 1681 0 44 60 1712 1 63 49 1696 1 60 49 1696 4 72 78 1712 0 44 66 1732 4 72 81 1732 0 43 60 1763 1 59 49 1743 1 65 49 1743 4 71 81 1766 0 43 60 1763 4 71 81 1766 0 43 60 1828 1 53 49 1809 1 71 49 1809 0 43 60 1828 0 36 66 1887 1 59 54 1862 1 64 54 1862 4 72 78 1863 0 36 66 1887 4 76 75 1877 0 43 61 1953 0 36 66 2018 0 43 61 2084 1 64 49 2055 1 58 49 2055 0 43 61 2084 0 41 66 2125 1 56 54 2124 1 63 54 2124 3 68 64 2171 0 46 60 2156 1 56 49 2136 1 62 49 2136 3 68 64 2171 0 46 60 2156 3 68 64 2171 3 68 64 2171 0 53 61 2204 3 67 64 2190 0 53 61 2204 3 67 64 2204 0 43 60 2235 1 58 49 2220 1 65 49 2220 3 74 64 2269 0 43 66 2280 3 74 64 2269 3 74 68 2301 3 74 68 2301 0 36 60 2352 3 73 68 2368 3 73 68 2368 0 36 66 2411 1 64 54 2386 1 58 54 2386 3 73 74 2387 0 36 66 2411 3 72 71 2400 0 43 61 2466 0 43 61 2466 3 70 71 2466 0 41 60 2497 1 56 49 2481 1 63 49 2481 3 72 71 2498 0 41 66 2518 3 72 75 2518 0 43 60 2548 1 63 49 2529 1 58 49 2529 3 70 75 2564 0 43 60 2548 3 70 75 2564 3 70 75 2564 0 44 61 2607 1 60 49 2579 1 67 49 2579 3 72 75 2727 0 44 61 2607 3 72 75 2727 3 72 75 2727 3 72 75 2727 0 44 51 2673 3 72 75 2727 3 72 75 2727 0 51 48 2727 3 72 75 2727 0 46 60 2759 3 68 72 2761 0 46 60 2759 3 68 72 2761 0 46 66 2804 3 68 68 2780 0 46 66 2804 3 68 68 2822 3 68 68 2822 0 53 61 2869 0 36 66 2934 1 64 54 2910 1 70 54 2910 0 36 66 2934 0 43 61 3000 0 36 66 3065 0 43 61 3131 1 64 49 3102 1 70 49 3102 0 43 61 3131 0 41 59 3196 1 63 49 3171 1 68 49 3171 0 41 59 3196 4 72 70 3186 4 75 70 3205 0 48 55 3262 4 84 70 3238 0 48 55 3262 4 82 70 3251 4 84 70 3271 0 40 59 3327 4 79 73 3349 4 79 73 3349 4 79 73 3349 0 47 55 3393 4 67 73 3415 0 37 66 3458 1 59 54 3433 1 65 54 3433 4 66 80 3434 0 37 66 3458 4 87 77 3457 4 77 77 3467 4 65 77 3533 0 36 66 3589 4 67 78 3565 0 36 66 3589 4 86 78 3588 4 64 78 3663 0 41 66 3720 1 56 54 3695 1 63 54 3695 4 72 77 3696 0 41 66 3720 4 70 74 3710 4 72 74 3729 0 50 61 3775 4 72 74 3761 0 50 61 3775 4 72 74 3775 0 44 60 3806 1 63 49 3790 1 60 49 3790 4 72 74 3807 0 44 66 3827 4 72 71 3827 0 43 60 3858 1 59 49 3838 1 65 49 3838 4 71 71 3860 0 43 60 3858 4 71 71 3860 0 43 60 3923 1 53 49 3903 1 71 49 3903 0 43 60 3923 0 36 66 3982 1 59 54 3957 1 64 54 3957 4 72 71 3958 0 36 66 3982 4 76 68 3971 0 43 61 4047 0 36 66 4113 0 43 61 4178 1 64 49 4150 1 58 49 4150 0 43 61 4178 0 41 66 4244 1 56 54 4219 1 60 54 4219 0 41 66 4244 0 48 61 4309 ]
 [stateGains 16] = [ 110 107 70 112 109 96 94 98 99 83 0 71 73 44 0 59 ]
 [cue112Buffer 64]
)
(procedure (cue112Verify &tmp index slot word digit value i)
(for ((= i 0)) (< i 64) ((++ i)) (= [cue112Buffer i] 0))
(for ((= index 0)) (< index 188) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 0 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [historyTableA index] value) (return 0)))
(for ((= index 0)) (< index 188) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 10 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [historyTableB index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 20 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiChannels index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 21 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [mainStateGains index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 22 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [reducedStateGains index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 23 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiPrograms index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 24 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiPans index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 25 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [initialExpression index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 26 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [loopExpression index] value) (return 0)))
(for ((= index 0)) (< index 144) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 27 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [expressionEvents index] value) (return 0)))
(for ((= index 0)) (< index 940) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 35 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [keyWindows index] value) (return 0)))
(for ((= index 0)) (< index 1156) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 82 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [heldNotes index] value) (return 0)))
(for ((= index 0)) (< index 16) ((++ index))
(if (== (mod index 20) 0) (GetFarText 269 (+ 140 (/ index 20)) @cue112Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue112Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue112Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [stateGains index] value) (return 0)))
(return 1))
(procedure (cue112Validate sound &tmp i value wanted)
(if (not (cue112Verify)) (return 0))
(if (or (not (IsObject sound)) (!= (sound number?) 112)) (return 0))
(if (or (!= (cue112ReadyTransport musicBed?) sound) (!= (cue112ReadyTransport ownedBed?) sound)) (return 0))
(= wanted (cue112ReadyTransport nextRequestedState?))
(if (or (< wanted 0) (> wanted 1)) (return 0))
(= value (cue112ReadyTransport wholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue112ReadyTransport desiredWholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue112ReadyTransport savedWholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue112ReadyTransport transportMode?))
(if (or (< value 0) (> value 9)) (return 0))
(= value (cue112ReadyTransport resumeMode?))
(if (or (< value 0) (> value 9)) (return 0))
(= value (cue112ReadyTransport settledState?))
(if (or (< value -1) (> value 1)) (return 0))
(= value (cue112ReadyTransport musicPosition?))
(if (or (< value 0) (> value 4331)) (return 0))
(= value (cue112ReadyTransport pausedPosition?))
(if (or (< value 0) (> value 4331)) (return 0))
(= value (cue112ReadyTransport previousPosition?))
(if (or (< value -1) (> value 4331)) (return 0))
(= value (cue112ReadyTransport recoveryLastPosition?))
(if (or (< value -1) (> value 4331)) (return 0))
(= value (cue112ReadyTransport rejoinWindow?))
(if (or (< value -1) (> value 187)) (return 0))
(= value (cue112ReadyTransport historyWindow?))
(if (or (< value -1) (> value 187)) (return 0))
(= value (cue112ReadyTransport lastBatchKeys?))
(if (or (< value 0) (> value 32)) (return 0))
(= value (cue112ReadyTransport recoverySamples?))
(if (or (< value 0) (> value 32767)) (return 0))
(= value (cue112ReadyTransport recoveryReason?))
(if (or (< value 0) (> value 10)) (return 0))
(= value (cue112ReadyTransport historyRoute?))
(if (or (< value 0) (> value 10)) (return 0))
(= value (cue112ReadyTransport requestRevision?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue112ReadyTransport saveRevision?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue112ReadyTransport previousGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue112ReadyTransport loopEpoch?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue112ReadyTransport rejoinEpoch?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue112ReadyTransport lifecycleGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue112ReadyTransport recoveryGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue112ReadyTransport gainRefreshes?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue112ReadyTransport historyEpisodes?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue112ReadyTransport rejoinAttempts?))
(if (or (< value 0) (> value 32)) (return 0))
(= value (cue112ReadyTransport musicRunning?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue112ReadyTransport musicPaused?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue112ReadyTransport ownedPauseHeld?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue112ReadyTransport pausePhaseKnown?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue112ReadyTransport pausedCheckpoint?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue112ReadyTransport recoveryPhaseKnown?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue112ReadyTransport musicMuted?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue112ReadyTransport loopHasWrapped?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue112ReadyTransport saveGuard?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue112ReadyTransport remapGuard?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue112ReadyTransport remapDrain?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue112ReadyTransport positionUncertain?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue112ReadyTransport recoveryWrapped?))
(if (or (< value 0) (> value 1)) (return 0))
(if (or (!= (cue112ReadyTransport musicMuted?) (if (cue112ReadyTransport musicMuted?) 1 else 0)) (< (cue112ReadyTransport transportMode?) 1)) (return 0))
(if (and (cue112ReadyTransport recoveryBed?) (!= (cue112ReadyTransport recoveryBed?) sound)) (return 0))
(if (!= (cue112ReadyTransport musicRunning?) 1) (return 0))
(if (and (cue112ReadyTransport pausedCheckpoint?) (not (cue112ReadyTransport saveGuard?))) (return 0))
(if (and (cue112ReadyTransport saveGuard?) (not (cue112ReadyTransport ownedPauseHeld?))) (return 0))
(for ((= i 0)) (< i 8) ((++ i))
(if (or (< [currentGains i] 0) (> [currentGains i] 127)) (return 0))
(if (!= [targetGains i] [stateGains (+ (* wanted 8) i)]) (return 0)))
(return 1))
(instance cue112ReadyTransport of MusicTransport
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
            pushi 4332
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
            ldi 112
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
            ldi 4332
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
            label_057b: pushi 4332
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
            ldi 188
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
            ldi 112
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
            ldi 4208
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
            label_07c5: pushi 4332
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
            ldi 4208
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
            label_0951: pushi 4332
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
        (if (not (cue112Verify))
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
            ldi 112
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
        (if (not (cue112Verify))
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
        (if (not (cue112Verify))
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
        (if (not (cue112Verify))
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
        (if (not (cue112Verify))
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
            ldi 188
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
            ldi 4324
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

