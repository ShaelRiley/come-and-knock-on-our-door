;;; Sierra Script 1.0 - (do not remove this comment)
; New transition-ready arrangement transport; source/emitted-only candidate.
(script# 957)
(use "module981")
(public cue110ReadyTransport 0 cue110Verify 1 cue110Validate 2)
(local
 [currentGains 8] = [ 0 0 0 0 0 0 0 0 ]
 [targetGains 8] = [ 0 0 0 0 0 0 0 0 ]
 [historyTableA 195] = [ 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ]
 [historyTableB 195] = [ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ]
 [midiChannels 8] = [ 0 1 2 3 4 5 6 9 ]
 [mainStateGains 8] = [ 110 107 70 112 109 96 94 98 ]
 [reducedStateGains 8] = [ 99 83 0 71 73 44 0 59 ]
 [midiPrograms 8] = [ 33 4 48 73 11 27 11 0 ]
 [midiPans 8] = [ 64 49 75 55 75 82 40 64 ]
 [initialExpression 8] = [ 127 127 127 100 100 127 127 127 ]
 [loopExpression 8] = [ 127 127 127 96 96 127 127 127 ]
 [expressionEvents 144] = [ 12 3 90 45 3 96 77 3 103 110 3 100 143 3 98 274 3 110 405 3 105 536 3 100 667 3 96 797 3 90 896 3 94 981 3 96 1059 4 90 1092 4 96 1125 4 103 1157 4 100 1190 4 98 1321 4 110 1452 4 105 1583 4 100 1714 4 96 1845 4 90 1943 4 94 2028 4 96 2107 3 90 2139 3 96 2172 3 103 2205 3 100 2237 3 98 2368 3 110 2499 3 105 2630 3 100 2761 3 96 2892 3 90 2990 3 94 3075 3 96 3154 4 90 3186 4 96 3219 4 103 3252 4 100 3285 4 98 3416 4 110 3546 4 105 3677 4 100 3808 4 96 3939 4 90 4037 4 94 4122 4 96 ]
 [keyWindows 975] = [ 18 22 29 0 4 32 38 45 16 2 70 70 77 24 1 84 86 94 28 4 96 102 110 44 2 134 134 142 52 1 150 154 162 56 2 166 168 175 64 2 230 232 240 72 2 266 266 273 80 1 280 284 291 84 4 296 298 306 100 2 318 318 326 108 1 332 332 339 112 1 346 348 356 116 4 362 364 372 132 2 384 384 391 140 1 412 414 421 144 2 426 430 437 152 1 444 448 456 156 1 476 482 489 160 2 492 494 502 168 2 528 528 535 176 1 542 546 553 180 4 556 560 568 196 2 580 580 588 204 1 592 594 601 208 1 608 610 618 212 4 624 626 634 228 2 658 660 667 236 1 672 678 685 240 2 688 692 699 248 2 754 758 765 256 2 790 790 797 264 1 804 808 815 268 4 820 822 830 284 2 842 842 849 292 1 854 856 863 296 0 870 872 879 296 3 902 904 912 308 2 934 938 945 316 2 948 954 961 324 1 968 972 979 328 1 1000 1020 1027 332 2 1038 1038 1046 340 1 1052 1052 1059 344 1 1066 1076 1084 348 3 1104 1104 1112 360 1 1116 1118 1125 364 1 1132 1150 1157 368 2 1182 1182 1189 376 1 1196 1202 1209 380 2 1212 1214 1222 388 2 1248 1248 1255 396 2 1262 1268 1275 404 2 1278 1280 1288 412 2 1300 1300 1307 420 1 1312 1312 1320 424 1 1328 1330 1338 428 4 1344 1346 1353 444 2 1366 1366 1373 452 1 1378 1380 1387 456 1 1392 1396 1403 460 4 1408 1412 1419 476 2 1458 1460 1468 484 2 1474 1478 1485 492 1 1490 1496 1504 496 1 1524 1528 1536 500 2 1540 1542 1549 508 2 1562 1562 1569 516 1 1574 1574 1582 520 1 1590 1592 1600 524 4 1602 1608 1615 540 2 1628 1628 1635 548 3 1640 1640 1648 560 3 1654 1658 1665 572 6 1670 1674 1681 596 4 1706 1706 1714 612 1 1720 1726 1733 616 2 1736 1740 1747 624 2 1758 1758 1765 632 1 1802 1804 1812 636 2 1836 1838 1845 644 1 1852 1854 1862 648 4 1866 1870 1877 664 2 1902 1902 1910 672 0 1916 1920 1927 672 3 1932 1932 1940 684 3 1948 1952 1959 696 2 1982 1984 1992 704 2 1994 2000 2008 712 1 2014 2020 2027 716 1 2048 2066 2074 720 2 2086 2086 2093 728 1 2098 2100 2107 732 1 2112 2116 2124 736 5 2164 2164 2172 756 1 2178 2180 2188 760 4 2194 2196 2204 776 2 2230 2230 2237 784 1 2244 2248 2256 788 2 2260 2262 2270 796 2 2282 2282 2289 804 1 2324 2328 2336 808 1 2360 2360 2368 812 1 2374 2378 2386 816 4 2390 2392 2400 832 2 2414 2414 2421 840 1 2426 2426 2434 844 1 2440 2442 2450 848 4 2456 2458 2466 864 2 2478 2478 2485 872 1 2492 2492 2499 876 1 2506 2510 2518 880 2 2522 2524 2531 888 2 2544 2544 2551 896 1 2572 2576 2584 900 2 2586 2590 2597 908 2 2622 2622 2630 916 1 2636 2642 2649 920 2 2702 2706 2714 928 2 2718 2720 2728 936 2 2740 2740 2748 944 1 2752 2752 2760 948 1 2768 2786 2794 952 2 2806 2806 2813 960 1 2840 2852 2859 964 2 2872 2872 2879 972 1 2898 2902 2909 976 4 2914 2918 2925 992 2 2936 2936 2944 1000 1 2964 2966 2974 1004 4 2980 2982 2990 1020 2 3002 3002 3009 1028 1 3030 3032 3039 1032 2 3044 3048 3055 1040 1 3062 3066 3074 1044 1 3094 3112 3120 1048 2 3128 3128 3136 1056 4 3160 3164 3171 1072 4 3174 3178 3186 1088 2 3198 3198 3206 1096 1 3212 3212 3219 1100 1 3226 3228 3236 1104 4 3238 3244 3252 1120 2 3276 3276 3284 1128 1 3292 3296 3303 1132 2 3306 3310 3317 1140 2 3372 3374 3382 1148 2 3408 3408 3415 1156 1 3422 3426 3433 1160 4 3438 3440 3448 1176 2 3460 3460 3468 1184 1 3472 3474 3481 1188 1 3488 3490 3498 1192 4 3504 3506 3514 1208 2 3526 3526 3533 1216 1 3552 3556 3563 1220 2 3568 3572 3579 1228 1 3586 3590 3598 1232 1 3618 3624 3631 1236 2 3634 3636 3644 1244 2 3656 3656 3663 1252 1 3670 3670 3677 1256 1 3684 3688 3695 1260 4 3698 3702 3710 1276 2 3722 3722 3730 1284 3 3734 3734 3742 1296 3 3750 3752 3759 1308 6 3764 3768 3776 1332 4 3800 3800 3808 1348 1 3814 3820 3827 1352 2 3830 3834 3841 1360 2 3896 3898 3906 1368 2 3930 3932 3939 1376 1 3946 3948 3956 1380 4 3962 3964 3972 1396 2 3984 3984 3991 1404 1 3996 3998 4005 1408 0 4012 4014 4021 1408 3 4026 4026 4034 1420 3 4044 4046 4054 1432 2 4076 4080 4087 1440 2 4090 4096 4103 1448 1 4108 4114 4121 1452 1 4142 4160 4168 1456 2 4180 4180 4188 1464 1 4192 4194 4201 1468 1 4208 4210 4218 1472 4 4246 4246 4253 1488 0 4258 4258 4266 1488 0 4272 4276 4283 1488 3 4286 4292 4299 1500 1 4312 4312 4319 1504 0 4324 4324 4332 1504 0 ]
 [heldNotes 1504] = [ 0 43 66 55 1 59 54 29 1 62 54 29 3 71 72 128 0 43 66 55 3 71 72 128 3 71 72 128 0 50 61 120 1 59 49 94 1 62 49 94 3 71 72 128 0 50 61 120 3 71 72 128 3 74 69 142 0 42 66 185 3 73 73 162 0 42 66 185 3 73 73 175 0 54 61 251 3 74 73 240 3 74 73 273 0 40 66 316 1 62 54 291 1 55 54 291 3 79 82 293 0 40 66 316 3 78 79 306 3 74 79 358 3 74 79 358 0 47 61 382 1 62 49 356 1 55 49 356 3 74 79 358 0 47 61 382 3 76 79 391 3 76 79 391 0 45 60 421 3 78 79 422 3 76 77 456 3 76 77 456 0 52 61 513 3 74 77 489 0 52 61 513 3 76 77 502 3 76 77 535 0 38 66 578 1 54 54 553 1 61 54 553 3 78 77 568 0 38 66 578 3 78 77 568 3 78 74 601 3 78 74 601 0 45 61 644 1 54 49 618 1 61 49 618 3 74 74 620 0 45 61 644 3 74 74 651 3 76 74 685 0 42 66 709 3 76 74 685 0 42 66 709 3 78 72 718 0 49 61 775 3 73 72 782 3 76 72 815 0 47 66 840 1 62 54 815 1 57 54 815 3 76 72 815 0 47 66 840 3 74 69 849 3 74 69 849 0 54 61 881 1 62 49 879 1 57 49 879 0 46 60 912 3 77 69 914 0 45 60 945 3 76 69 979 3 76 69 979 3 76 69 979 0 45 61 1036 3 78 66 1084 3 78 66 1084 3 78 66 1084 0 43 46 1102 3 78 66 1084 4 71 64 1175 4 71 64 1175 4 71 64 1175 0 50 43 1167 4 71 64 1175 4 74 61 1189 0 42 46 1233 4 73 64 1209 0 42 46 1233 4 73 64 1222 0 47 60 1255 4 74 64 1275 0 54 43 1298 4 74 64 1275 0 54 43 1298 4 74 64 1288 4 74 64 1307 4 74 64 1320 0 40 66 1364 1 62 54 1338 1 55 54 1338 4 79 73 1340 0 40 66 1364 4 78 70 1353 4 74 70 1405 4 74 70 1405 0 47 61 1429 1 62 49 1403 1 55 49 1403 4 74 70 1405 0 47 61 1429 4 76 70 1438 0 45 60 1468 4 78 70 1470 4 76 73 1504 4 76 73 1504 0 52 61 1560 4 74 73 1536 0 52 61 1560 4 76 73 1549 4 76 73 1569 4 76 73 1582 0 38 66 1625 1 54 54 1600 1 61 54 1600 4 78 81 1615 0 38 66 1625 4 78 81 1615 2 66 42 1697 2 73 42 1697 4 78 78 1648 2 66 42 1697 2 73 42 1697 4 78 78 1648 0 45 61 1691 1 54 49 1665 1 61 49 1665 2 66 42 1697 2 73 42 1697 4 74 78 1667 0 45 61 1691 2 66 42 1697 2 73 42 1697 4 74 78 1699 4 76 78 1733 0 42 66 1756 4 76 78 1733 0 42 66 1756 4 78 81 1765 4 78 81 1765 0 49 61 1822 4 73 81 1830 4 76 81 1862 0 47 66 1887 1 62 54 1862 1 57 54 1862 4 76 81 1862 0 47 66 1887 4 74 75 1896 0 54 61 1929 1 62 49 1927 1 57 49 1927 0 46 60 1959 1 62 49 1940 1 56 49 1940 0 46 60 1959 4 77 75 1961 0 45 60 1992 4 76 75 2027 4 76 75 2027 4 76 75 2027 0 45 61 2084 4 78 70 2132 4 78 70 2132 4 78 70 2132 0 43 66 2149 1 59 54 2124 1 54 54 2124 3 66 67 2158 4 78 70 2132 3 66 64 2191 0 50 61 2215 1 59 49 2188 1 54 49 2188 3 66 64 2191 0 50 61 2215 3 71 64 2204 3 71 64 2237 0 47 66 2280 3 69 68 2256 0 47 66 2280 3 72 68 2289 3 72 68 2289 0 54 61 2345 3 71 68 2368 0 40 66 2411 1 62 54 2386 1 55 54 2386 3 67 74 2387 0 40 66 2411 3 67 71 2400 3 67 71 2453 3 67 71 2453 0 47 61 2476 1 62 49 2450 1 55 49 2450 3 67 71 2453 0 47 61 2476 3 71 71 2466 3 72 71 2485 3 71 71 2499 0 38 66 2542 3 69 75 2518 0 38 66 2542 3 67 75 2531 3 69 75 2551 0 50 61 2607 3 71 75 2584 0 50 61 2607 3 67 75 2616 3 67 75 2649 0 36 51 2673 3 67 75 2649 0 43 48 2738 3 71 72 2714 0 43 48 2738 3 71 72 2760 3 71 72 2760 3 71 72 2760 0 36 66 2804 3 72 68 2813 3 72 68 2813 0 43 61 2869 3 72 68 2859 3 72 68 2884 0 47 66 2934 1 62 54 2909 1 57 54 2909 3 69 68 2911 0 47 66 2934 3 69 65 2944 3 69 65 2944 0 47 61 3000 1 62 49 2974 1 55 49 2974 3 67 65 2976 0 47 61 3000 3 71 65 3009 3 71 65 3009 0 45 60 3039 3 72 65 3042 3 71 63 3055 3 72 63 3074 0 38 61 3120 3 71 63 3121 0 38 60 3152 1 60 49 3136 1 54 49 3136 3 69 63 3153 0 43 59 3196 1 59 49 3171 1 62 49 3171 4 71 73 3269 0 43 59 3196 4 71 73 3269 4 71 73 3269 4 71 73 3269 0 50 55 3262 1 59 44 3236 1 62 44 3236 4 71 73 3269 0 50 55 3262 4 71 73 3269 4 74 70 3284 0 42 59 3327 4 73 73 3303 0 42 59 3327 4 73 73 3317 0 54 55 3393 4 74 73 3382 4 74 73 3415 0 40 66 3458 1 62 54 3433 1 55 54 3433 4 79 80 3435 0 40 66 3458 4 78 77 3448 4 74 77 3500 4 74 77 3500 0 47 61 3524 1 62 49 3498 1 55 49 3498 4 74 77 3500 0 47 61 3524 4 76 77 3533 4 76 77 3533 0 45 60 3563 4 78 77 3564 4 76 78 3598 4 76 78 3598 0 52 61 3654 4 74 78 3631 0 52 61 3654 4 76 78 3644 4 76 78 3663 4 76 78 3677 0 38 66 3720 1 54 54 3695 1 61 54 3695 4 78 77 3710 0 38 66 3720 4 78 77 3710 2 66 42 3791 2 73 42 3791 4 78 74 3742 2 66 42 3791 2 73 42 3791 4 78 74 3742 0 45 61 3785 1 54 49 3759 1 61 49 3759 2 66 42 3791 2 73 42 3791 4 74 74 3761 0 45 61 3785 2 66 42 3791 2 73 42 3791 4 74 74 3793 4 76 74 3827 0 42 66 3851 4 76 74 3827 0 42 66 3851 4 78 71 3860 0 49 61 3916 4 73 71 3924 4 76 71 3957 0 47 66 3982 1 62 54 3956 1 57 54 3956 4 76 71 3957 0 47 66 3982 4 74 68 3991 4 74 68 3991 0 54 61 4023 1 62 49 4021 1 57 49 4021 0 46 60 4054 1 62 49 4034 1 56 49 4034 0 46 60 4054 4 77 68 4056 0 45 60 4087 4 76 68 4121 4 76 68 4121 4 76 68 4121 0 45 61 4178 4 78 66 4226 4 78 66 4226 4 78 66 4226 0 43 66 4244 1 59 54 4218 1 62 54 4218 4 78 66 4226 0 50 61 4309 1 59 49 4283 1 62 49 4283 0 50 61 4309 ]
 [stateGains 16] = [ 110 107 70 112 109 96 94 98 99 83 0 71 73 44 0 59 ]
 [cue110Buffer 64]
)
(procedure (cue110Verify &tmp index slot word digit value i)
(for ((= i 0)) (< i 64) ((++ i)) (= [cue110Buffer i] 0))
(for ((= index 0)) (< index 195) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 0 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [historyTableA index] value) (return 0)))
(for ((= index 0)) (< index 195) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 10 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [historyTableB index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 20 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiChannels index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 21 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [mainStateGains index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 22 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [reducedStateGains index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 23 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiPrograms index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 24 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [midiPans index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 25 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [initialExpression index] value) (return 0)))
(for ((= index 0)) (< index 8) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 26 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [loopExpression index] value) (return 0)))
(for ((= index 0)) (< index 144) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 27 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [expressionEvents index] value) (return 0)))
(for ((= index 0)) (< index 975) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 35 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [keyWindows index] value) (return 0)))
(for ((= index 0)) (< index 1504) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 84 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [heldNotes index] value) (return 0)))
(for ((= index 0)) (< index 16) ((++ index))
(if (== (mod index 20) 0) (GetFarText 267 (+ 160 (/ index 20)) @cue110Buffer))
(= slot (mod index 20)) (= value 0)
(for ((= i 0)) (< i 5) ((++ i))
(= word [cue110Buffer (+ (* slot 3) (/ i 2))])
(= digit (- (if (mod i 2) (>> word 8) else (& word 255)) 48))
(if (or (< digit 0) (> digit 9)) (return 0))
(= value (+ (* value 10) digit)))
(if (!= (>> [cue110Buffer (+ (* slot 3) 2)] 8) 32) (return 0))
(if (!= [stateGains index] value) (return 0)))
(return 1))
(procedure (cue110Validate sound &tmp i value wanted)
(if (not (cue110Verify)) (return 0))
(if (or (not (IsObject sound)) (!= (sound number?) 110)) (return 0))
(if (or (!= (cue110ReadyTransport musicBed?) sound) (!= (cue110ReadyTransport ownedBed?) sound)) (return 0))
(= wanted (cue110ReadyTransport nextRequestedState?))
(if (or (< wanted 0) (> wanted 1)) (return 0))
(= value (cue110ReadyTransport wholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue110ReadyTransport desiredWholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue110ReadyTransport savedWholeGain?))
(if (or (< value 0) (> value 100)) (return 0))
(= value (cue110ReadyTransport transportMode?))
(if (or (< value 0) (> value 9)) (return 0))
(= value (cue110ReadyTransport resumeMode?))
(if (or (< value 0) (> value 9)) (return 0))
(= value (cue110ReadyTransport settledState?))
(if (or (< value -1) (> value 1)) (return 0))
(= value (cue110ReadyTransport musicPosition?))
(if (or (< value 0) (> value 4331)) (return 0))
(= value (cue110ReadyTransport pausedPosition?))
(if (or (< value 0) (> value 4331)) (return 0))
(= value (cue110ReadyTransport previousPosition?))
(if (or (< value -1) (> value 4331)) (return 0))
(= value (cue110ReadyTransport recoveryLastPosition?))
(if (or (< value -1) (> value 4331)) (return 0))
(= value (cue110ReadyTransport rejoinWindow?))
(if (or (< value -1) (> value 194)) (return 0))
(= value (cue110ReadyTransport historyWindow?))
(if (or (< value -1) (> value 194)) (return 0))
(= value (cue110ReadyTransport lastBatchKeys?))
(if (or (< value 0) (> value 32)) (return 0))
(= value (cue110ReadyTransport recoverySamples?))
(if (or (< value 0) (> value 32767)) (return 0))
(= value (cue110ReadyTransport recoveryReason?))
(if (or (< value 0) (> value 10)) (return 0))
(= value (cue110ReadyTransport historyRoute?))
(if (or (< value 0) (> value 10)) (return 0))
(= value (cue110ReadyTransport requestRevision?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue110ReadyTransport saveRevision?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue110ReadyTransport previousGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue110ReadyTransport loopEpoch?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue110ReadyTransport rejoinEpoch?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue110ReadyTransport lifecycleGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue110ReadyTransport recoveryGeneration?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue110ReadyTransport gainRefreshes?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue110ReadyTransport historyEpisodes?))
(if (or (< value 0) (> value 29999)) (return 0))
(= value (cue110ReadyTransport rejoinAttempts?))
(if (or (< value 0) (> value 32)) (return 0))
(= value (cue110ReadyTransport musicRunning?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue110ReadyTransport musicPaused?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue110ReadyTransport ownedPauseHeld?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue110ReadyTransport pausePhaseKnown?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue110ReadyTransport pausedCheckpoint?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue110ReadyTransport recoveryPhaseKnown?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue110ReadyTransport musicMuted?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue110ReadyTransport loopHasWrapped?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue110ReadyTransport saveGuard?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue110ReadyTransport remapGuard?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue110ReadyTransport remapDrain?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue110ReadyTransport positionUncertain?))
(if (or (< value 0) (> value 1)) (return 0))
(= value (cue110ReadyTransport recoveryWrapped?))
(if (or (< value 0) (> value 1)) (return 0))
(if (or (!= (cue110ReadyTransport musicMuted?) (if (cue110ReadyTransport musicMuted?) 1 else 0)) (< (cue110ReadyTransport transportMode?) 1)) (return 0))
(if (and (cue110ReadyTransport recoveryBed?) (!= (cue110ReadyTransport recoveryBed?) sound)) (return 0))
(if (!= (cue110ReadyTransport musicRunning?) 1) (return 0))
(if (and (cue110ReadyTransport pausedCheckpoint?) (not (cue110ReadyTransport saveGuard?))) (return 0))
(if (and (cue110ReadyTransport saveGuard?) (not (cue110ReadyTransport ownedPauseHeld?))) (return 0))
(for ((= i 0)) (< i 8) ((++ i))
(if (or (< [currentGains i] 0) (> [currentGains i] 127)) (return 0))
(if (!= [targetGains i] [stateGains (+ (* wanted 8) i)]) (return 0)))
(return 1))
(instance cue110ReadyTransport of MusicTransport
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
            ldi 110
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
            ldi 195
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
            ldi 110
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
        (if (not (cue110Verify))
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
            ldi 110
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
        (if (not (cue110Verify))
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
        (if (not (cue110Verify))
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
        (if (not (cue110Verify))
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
        (if (not (cue110Verify))
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
            ldi 195
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

