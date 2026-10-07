(method (hStaticAt table index) (switch table
 (1 (if (or (< index 0) (>= index 1018)) (return 0)) (return [sdStarts index]))
 (2 (if (or (< index 0) (>= index 1018)) (return 0)) (return [sdCounts index]))
 (3 (if (or (< index 0) (>= index 9104)) (return 0)) (return [sdPageData index]))
 (4 (if (or (< index 0) (>= index 75)) (return 0)) (return [sdLegacyVoiceDurations index]))
 (5 (if (or (< index 0) (>= index 1138)) (return 0)) (return [sdTextResources index]))
 (6 (if (or (< index 0) (>= index 1138)) (return 0)) (return [sdAudioModules index]))
 (7 (if (or (< index 0) (>= index 1138)) (return 0)) (return [sdPageDurations index]))
) (return 0))
