;;; Sierra Script 1.0 - (do not remove this comment)
; New transition-ready arrangement transport; source/emitted-only candidate.
(script# 954)
(use "module981")
(public cue107ReadyTransport 0 cue107Verify 1 cue107Validate 2)
(local
 [currentGains 8] = [ 0 0 0 0 0 0 0 0 ]
 [targetGains 8] = [ 0 0 0 0 0 0 0 0 ]
 [historyTableA 178] = [ 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ]
 [historyTableB 178] = [ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ]
 [midiChannels 8] = [ 0 1 2 3 4 5 6 9 ]
 [mainStateGains 8] = [ 110 107 70 112 109 96 94 98 ]
 [reducedStateGains 8] = [ 99 83 0 71 73 44 0 59 ]
 [midiPrograms 8] = [ 33 4 48 65 59 27 11 0 ]
 [midiPans 8] = [ 64 49 75 55 75 82 40 64 ]
 [initialExpression 8] = [ 127 127 127 100 100 127 127 127 ]
 [loopExpression 8] = [ 127 127 127 96 96 127 127 127 ]
 [expressionEvents 144] = [ 12 3 90 44 3 96 76 3 103 108 3 100 141 3 98 269 3 110 398 3 105 526 3 100 655 3 96 783 3 90 880 3 94 963 3 96 1041 4 90 1073 4 96 1105 4 103 1137 4 100 1169 4 98 1298 4 110 1426 4 105 1555 4 100 1683 4 96 1812 4 90 1908 4 94 1992 4 96 2069 3 90 2101 3 96 2133 3 103 2166 3 100 2198 3 98 2326 3 110 2455 3 105 2583 3 100 2712 3 96 2840 3 90 2937 3 94 3020 3 96 3098 4 90 3130 4 96 3162 4 103 3194 4 100 3226 4 98 3355 4 110 3483 4 105 3612 4 100 3740 4 96 3869 4 90 3965 4 94 4049 4 96 ]
 [keyWindows 890] = [ 18 22 29 0 3 34 36 44 12 2 68 68 75 20 1 82 88 95 24 2 98 100 108 32 2 120 120 127 40 1 146 166 173 44 2 184 184 192 52 1 196 196 204 56 1 212 212 219 60 3 222 230 237 72 1 276 278 286 76 4 290 294 301 92 2 404 408 416 100 2 420 422 430 108 2 506 506 513 116 1 532 536 544 120 4 564 568 576 136 2 596 602 609 144 2 628 630 637 152 4 662 666 673 168 2 676 676 684 176 4 692 698 706 192 2 726 726 733 200 3 740 740 748 212 3 758 764 771 224 1 790 794 801 228 4 806 808 815 244 2 840 840 848 252 0 860 872 880 252 1 892 892 899 256 0 904 904 912 256 0 918 936 944 256 1 956 956 963 260 0 968 968 976 260 0 982 982 990 260 3 992 1000 1008 272 1 1020 1020 1028 276 0 1032 1034 1041 276 0 1046 1052 1060 276 1 1062 1064 1072 280 2 1084 1084 1091 288 1 1096 1096 1104 292 1 1112 1116 1123 296 2 1126 1128 1136 304 2 1176 1194 1201 312 2 1214 1214 1221 320 1 1226 1226 1233 324 1 1240 1258 1266 328 1 1278 1278 1285 332 0 1290 1290 1297 332 1 1304 1308 1315 336 4 1320 1322 1330 352 2 1406 1406 1413 360 1 1432 1436 1444 364 2 1448 1450 1458 372 2 1470 1470 1477 380 1 1534 1534 1541 384 1 1562 1564 1572 388 4 1576 1578 1586 404 2 1626 1630 1637 412 2 1640 1642 1650 420 2 1658 1658 1666 428 4 1690 1694 1701 444 2 1722 1724 1732 452 2 1740 1740 1748 460 0 1754 1754 1762 460 3 1770 1770 1777 472 3 1786 1788 1796 484 1 1804 1804 1812 488 0 1818 1822 1829 488 4 1834 1836 1844 504 2 1868 1868 1876 512 0 1890 1900 1908 512 1 1920 1920 1928 516 0 1932 1934 1941 516 0 1946 1966 1973 516 1 1984 1984 1992 520 0 1996 1998 2005 520 0 2012 2012 2019 520 3 2022 2030 2037 532 1 2062 2062 2069 536 0 2076 2078 2086 536 4 2088 2094 2101 552 2 2114 2114 2121 560 1 2126 2126 2133 564 1 2140 2158 2166 568 2 2190 2190 2197 576 1 2204 2208 2216 580 2 2220 2222 2229 588 2 2268 2268 2276 596 4 2284 2286 2293 612 2 2318 2318 2326 620 1 2332 2336 2344 624 4 2348 2350 2358 640 2 2370 2370 2378 648 1 2382 2384 2391 652 1 2412 2416 2423 656 2 2434 2434 2441 664 1 2462 2464 2471 668 2 2476 2480 2487 676 1 2492 2498 2506 680 1 2526 2526 2533 684 4 2540 2544 2551 700 2 2576 2576 2583 708 1 2590 2608 2615 712 2 2628 2628 2635 720 1 2640 2640 2647 724 1 2654 2658 2666 728 2 2670 2672 2680 736 2 2704 2704 2712 744 1 2718 2724 2731 748 2 2734 2736 2744 756 2 2756 2756 2763 764 1 2768 2768 2776 768 1 2782 2782 2790 772 4 2798 2800 2808 788 2 2832 2832 2840 796 1 2846 2850 2858 800 4 2862 2866 2873 816 2 2884 2884 2891 824 1 2896 2898 2905 828 0 2926 2926 2934 828 3 2942 2946 2953 840 2 2976 2978 2985 848 2 2988 2994 3001 856 1 3008 3012 3019 860 1 3040 3040 3047 864 4 3050 3058 3065 880 2 3078 3078 3085 888 1 3090 3090 3097 892 1 3104 3108 3115 896 3 3120 3122 3129 908 2 3154 3154 3161 916 1 3168 3172 3180 920 2 3184 3186 3193 928 2 3206 3206 3213 936 1 3232 3250 3258 940 2 3270 3270 3278 948 1 3282 3282 3290 952 1 3296 3296 3304 956 3 3306 3316 3323 968 1 3334 3334 3342 972 0 3346 3346 3354 972 1 3362 3364 3372 976 4 3376 3380 3387 992 2 3490 3494 3501 1000 2 3506 3508 3515 1008 2 3618 3622 3629 1016 4 3650 3654 3662 1032 2 3682 3686 3694 1040 2 3714 3716 3723 1048 4 3746 3750 3758 1064 2 3762 3762 3770 1072 4 3778 3784 3792 1088 2 3812 3812 3819 1096 3 3826 3826 3834 1108 3 3842 3848 3856 1120 1 3876 3878 3886 1124 4 3890 3894 3901 1140 2 3926 3926 3933 1148 0 3946 3958 3965 1148 1 3978 3978 3985 1152 0 3990 3990 3998 1152 0 4004 4022 4030 1152 1 4042 4042 4049 1156 0 4054 4054 4062 1156 0 4068 4068 4076 1156 3 4078 4086 4094 1168 1 4106 4106 4113 1172 0 4118 4118 4126 1172 0 4132 4136 4144 1172 3 4146 4150 4158 1184 1 4170 4170 4178 1188 0 4182 4182 4190 1188 0 4196 4216 4223 1188 1 4234 4234 4242 1192 0 4246 4248 4255 1192 0 ]
 [heldNotes 1192] = [ 0 41 66 54 1 56 54 29 1 63 54 29 0 41 66 54 3 72 69 44 3 72 69 75 0 48 61 118 3 84 69 95 0 48 61 118 3 82 69 108 3 84 69 127 0 40 66 182 3 79 73 204 3 79 73 204 3 79 73 204 0 47 61 247 1 55 49 219 1 62 49 219 0 47 61 247 0 37 66 311 1 53 54 286 1 59 54 286 3 66 82 288 0 37 66 311 3 87 79 310 0 36 66 439 3 67 77 416 0 36 66 439 3 86 77 438 3 64 77 513 0 41 66 552 1 56 54 544 1 63 54 544 3 72 77 544 0 44 61 577 3 72 74 576 0 50 61 616 3 72 74 609 0 44 61 648 1 63 49 637 1 60 49 637 3 72 74 653 0 44 66 673 3 72 72 673 0 43 60 686 1 59 49 684 1 65 49 684 3 71 72 706 0 47 61 713 3 71 72 706 0 44 61 737 1 56 49 733 1 68 49 733 0 43 60 750 1 53 49 748 1 71 49 748 0 35 61 777 0 36 66 825 1 59 54 801 1 64 54 801 3 72 72 801 0 36 66 825 3 76 69 815 0 43 61 889 0 36 66 954 0 43 61 1018 1 64 49 990 1 58 49 990 0 43 61 1018 0 41 46 1082 0 41 46 1082 4 72 61 1072 4 75 61 1091 4 72 61 1104 0 48 43 1147 4 84 61 1123 0 48 43 1147 4 82 61 1136 0 40 46 1211 4 79 64 1233 4 79 64 1233 4 79 64 1233 0 47 43 1275 4 67 64 1297 0 37 66 1339 1 59 54 1315 1 65 54 1315 4 66 73 1316 0 37 66 1339 4 87 70 1338 4 65 70 1413 0 36 66 1468 4 67 73 1444 0 36 66 1468 4 86 73 1467 4 76 73 1477 4 64 73 1541 0 41 66 1597 1 56 54 1572 1 63 54 1572 4 72 81 1573 0 41 66 1597 4 70 78 1586 0 50 61 1650 4 72 78 1637 0 50 61 1650 4 72 78 1651 0 44 60 1681 1 63 49 1666 1 60 49 1666 4 72 78 1682 0 44 66 1702 4 72 81 1701 0 43 60 1732 4 71 81 1735 0 44 61 1766 1 56 49 1762 1 68 49 1762 0 43 60 1796 1 53 49 1777 1 71 49 1777 0 43 60 1796 0 36 66 1854 1 59 54 1829 1 64 54 1829 4 72 78 1830 0 36 66 1854 4 76 75 1844 0 43 61 1918 0 36 66 1982 0 43 61 2047 1 64 49 2019 1 58 49 2019 0 43 61 2047 0 41 66 2111 1 57 54 2086 1 60 54 2086 3 69 67 2183 0 41 66 2111 3 69 67 2183 3 69 67 2183 3 69 67 2183 0 48 61 2175 3 69 67 2183 3 72 64 2197 0 40 66 2239 3 71 68 2216 0 40 66 2239 3 71 68 2229 0 52 61 2304 1 55 49 2276 1 60 49 2276 3 72 68 2281 0 52 61 2304 3 72 68 2293 3 72 68 2326 0 38 66 2368 1 53 54 2344 1 60 54 2344 3 77 74 2345 0 38 66 2368 3 76 71 2358 3 72 71 2409 3 72 71 2409 0 45 61 2432 3 74 71 2441 3 74 71 2441 0 43 60 2471 3 76 71 2472 3 74 75 2506 3 74 75 2506 0 50 61 2561 1 53 49 2533 1 58 49 2533 3 72 75 2537 0 50 61 2561 3 74 75 2551 3 74 75 2583 0 36 51 2625 3 76 75 2615 3 76 72 2647 3 76 72 2647 0 43 48 2689 3 72 72 2666 0 43 48 2689 3 72 72 2697 3 74 72 2731 0 40 66 2754 3 74 72 2731 0 40 66 2754 3 76 68 2763 3 76 68 2763 3 76 68 2795 0 47 61 2818 1 56 49 2790 1 62 49 2790 3 76 68 2795 0 47 61 2818 3 71 68 2826 3 74 68 2858 0 45 66 2882 1 55 54 2858 1 60 54 2858 3 74 68 2858 0 45 66 2882 3 72 65 2891 3 72 65 2891 0 44 60 2953 1 60 49 2934 1 54 49 2934 0 44 60 2953 3 75 65 2955 0 43 60 2985 3 74 65 3019 3 74 65 3019 3 74 65 3019 0 43 61 3075 1 64 49 3047 1 58 49 3047 3 76 63 3097 0 43 61 3075 3 76 63 3097 3 76 63 3097 3 76 63 3097 0 41 59 3139 1 56 49 3115 1 63 49 3115 0 41 59 3139 4 72 70 3129 4 72 70 3161 0 48 55 3204 4 84 70 3180 0 48 55 3204 4 82 70 3193 4 84 70 3213 0 40 59 3268 4 79 73 3290 4 79 73 3290 4 79 73 3290 0 47 55 3332 1 55 44 3304 1 62 44 3304 0 47 55 3332 4 67 73 3354 0 37 66 3397 1 53 54 3372 1 59 54 3372 4 66 80 3373 0 37 66 3397 4 87 77 3395 0 36 66 3525 4 67 78 3501 0 36 66 3525 4 86 78 3524 0 41 66 3638 1 56 54 3629 1 63 54 3629 4 72 77 3630 0 44 61 3662 4 72 74 3662 0 50 61 3702 4 72 74 3694 0 44 61 3734 1 63 49 3723 1 60 49 3723 4 72 74 3739 0 44 66 3759 4 72 71 3758 0 43 60 3772 1 59 49 3770 1 65 49 3770 4 71 71 3792 0 47 61 3798 4 71 71 3792 0 44 61 3823 1 56 49 3819 1 68 49 3819 0 43 60 3836 1 53 49 3834 1 71 49 3834 0 35 61 3863 0 36 66 3911 1 59 54 3886 1 64 54 3886 4 72 71 3887 0 36 66 3911 4 76 68 3901 0 43 61 3975 0 36 66 4039 0 43 61 4104 1 64 49 4076 1 58 49 4076 0 43 61 4104 0 41 66 4168 1 56 54 4144 1 60 54 4144 0 41 66 4168 0 48 61 4232 ]
 [stateGains 16] = [ 110 107 70 112 109 96 94 98 99 83 0 71 73 44 0 59 ]
 [cue107Buffer 64]
)
(procedure (cue107Verify &tmp index slot word digit value i)
(for ((= i 0)) (< i 64) ((++ i)) (= [cue107Buffer i] 0))
(for ((= index 0)) (< index 178) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 0 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [historyTableA index] value) (return 0)))
(for ((= index 0)) (< index 178) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 9 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [historyTableB index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 18 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiChannels index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 19 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [mainStateGains index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 20 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [reducedStateGains index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 21 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiPrograms index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 22 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiPans index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 23 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [initialExpression index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 24 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [loopExpression index] value) (return 0)))
(for ((= index 0)) (< index 144) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 25 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [expressionEvents index] value) (return 0)))
(for ((= index 0)) (< index 890) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 33 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [keyWindows index] value) (return 0)))
(for ((= index 0)) (< index 1192) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 78 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [heldNotes index] value) (return 0)))
(for ((= index 0)) (< index 16) ((++ index))
(if (== (mod index 20) 0) (GetFarText 264 (+ 138 (/ index 20)) @cue107Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue107Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue107Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [stateGains index] value) (return 0)))
(return 1))
(procedure (cue107Validate sound &tmp i value wanted)
(if (not (cue107Verify)) (return 0))
(if (or (not (IsObject sound)) (!= (sound number?) 107)) (return 0))
(if (or (!= (cue107ReadyTransport musicBed?) sound) (!= (cue107ReadyTransport ownedBed?) sound)) (return 0))
(= wanted (cue107ReadyTransport nextRequestedState?))
(if (or (< wanted 0) (> wanted 1)) (return 0))
(= value (cue107ReadyTransport wholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue107ReadyTransport desiredWholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue107ReadyTransport savedWholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue107ReadyTransport transportMode?))
(if (or (< value 0) (> value 9)) (return 0))
(= value (cue107ReadyTransport resumeMode?))
(if (or (< value 0) (> value 9)) (return 0))
(= value (cue107ReadyTransport settledState?))
(if (or (< value -1) (> value 1)) (return 0))
(= value (cue107ReadyTransport musicPosition?))
(if (or (< value 0) (> value 4254)) (return 0))
(= value (cue107ReadyTransport pausedPosition?))
(if (or (< value 0) (> value 4254)) (return 0))
(= value (cue107ReadyTransport previousPosition?))
(if (or (< value -1) (> value 4254)) (return 0))
(= value (cue107ReadyTransport recoveryLastPosition?))
(if (or (< value -1) (> value 4254)) (return 0))
(= value (cue107ReadyTransport rejoinWindow?))
(if (or (< value -1) (> value 177)) (return 0))
(= value (cue107ReadyTransport historyWindow?))
(if (or (< value -1) (> value 177)) (return 0))
(= value (cue107ReadyTransport lastBatchKeys?))
(if (or (< value 0) (> value 32)) (return 0))
(= value (cue107ReadyTransport recoverySamples?))
(if (or (< value 0) (> value 32767)) (return 0))
(= value (cue107ReadyTransport recoveryReason?))
(if (or (< value 0) (> value 10)) (return 0))
(= value (cue107ReadyTransport historyRoute?))
(if (or (< value 0) (> value 10)) (return 0))
(= value (cue107ReadyTransport requestRevision?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue107ReadyTransport saveRevision?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue107ReadyTransport previousGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue107ReadyTransport loopEpoch?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue107ReadyTransport rejoinEpoch?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue107ReadyTransport lifecycleGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue107ReadyTransport recoveryGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue107ReadyTransport gainRefreshes?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue107ReadyTransport historyEpisodes?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue107ReadyTransport rejoinAttempts?))
(if (or (< value 0) (> value 32)) (return 0))
(= value (cue107ReadyTransport musicRunning?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue107ReadyTransport musicPaused?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue107ReadyTransport ownedPauseHeld?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue107ReadyTransport pausePhaseKnown?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue107ReadyTransport pausedCheckpoint?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue107ReadyTransport recoveryPhaseKnown?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue107ReadyTransport musicMuted?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue107ReadyTransport loopHasWrapped?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue107ReadyTransport saveGuard?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue107ReadyTransport remapGuard?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue107ReadyTransport remapDrain?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue107ReadyTransport positionUncertain?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue107ReadyTransport recoveryWrapped?))
(if (or (< value 0) (> value 1)) (return 0))
(if (or (!= (cue107ReadyTransport musicMuted?) (if (cue107ReadyTransport musicMuted?) 1 else 0)) (< (cue107ReadyTransport transportMode?) 1)) (return 0))
(if (and (cue107ReadyTransport recoveryBed?) (!= (cue107ReadyTransport recoveryBed?) sound)) (return 0))
(if (!= (cue107ReadyTransport musicRunning?) 1) (return 0))
(if (and (cue107ReadyTransport pausedCheckpoint?) (not (cue107ReadyTransport saveGuard?))) (return 0))
(if (and (cue107ReadyTransport saveGuard?) (not (cue107ReadyTransport ownedPauseHeld?))) (return 0))
(for ((= i 0)) (< i 8) ((++ i))
(if (or (< [currentGains i] 0) (> [currentGains i] 127)) (return 0))
(if (!= [targetGains i] [stateGains (+ (* wanted 8) i)]) (return 0)))
(return 1))
(instance cue107ReadyTransport of MusicTransport
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
            pushi 4255
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
            ldi 107
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
            ldi 4255
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
            label_057b: pushi 4255
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
            ldi 178
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
            ldi 107
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
            ldi 4131
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
            label_07c5: pushi 4255
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
            ldi 4131
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
            label_0951: pushi 4255
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
        (if (not (cue107Verify))
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
            ldi 107
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
        (if (not (cue107Verify))
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
        (if (not (cue107Verify))
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
        (if (not (cue107Verify))
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
        (if (not (cue107Verify))
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
            ldi 178
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
            ldi 4247
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

