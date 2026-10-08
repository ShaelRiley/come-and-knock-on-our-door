"""Native caption-only selected-date protocol; the future host owns its lease.

The bank checks its complete mutable value each time, and reloads immutable
source words through the existing static guard. It never grants game receipts.
"""
def source(prefix,suffix):
 P,S=len(prefix),len(suffix)
 return f'''
; Exports1..7 form a caption binding protocol. They accept no audio/receipt claim.
; Host MUST match the actual domain snapshot before every draw and after restore.
(procedure (finaleDateClear &tmp i)
 (for ((= i 0)) (< i 11) ((++ i)) (= [fbDateState i] 0))
 (for ((= i 0)) (< i 80) ((++ i)) (= [fbDate i] 0))
 (for ((= i 0)) (< i 80) ((++ i)) (= [fbCaption i] 0)) (return 1))
(procedure (finaleDateBegin owner epoch revHi revLo startHi startLo sourceHi sourceLo length)
 (proc999_1)
 (if (or (!= owner 996) (< epoch 1) (> epoch 32767) (< length 1) (> length 80)
  (< revHi 0) (< revLo 0) (< startHi 0) (< startLo 0) (< sourceHi 0) (< sourceLo 0)
  (not (or revHi revLo)) (not (or startHi startLo)) (not (or sourceHi sourceLo))) (return 0))
 (= [fbDateState 0] length) (= [fbDateState 2] owner) (= [fbDateState 3] epoch)
 (= [fbDateState 4] revHi) (= [fbDateState 5] revLo)
 (= [fbDateState 6] startHi) (= [fbDateState 7] startLo)
 (= [fbDateState 8] sourceHi) (= [fbDateState 9] sourceLo) (return 1))
(procedure (finaleDateChar index value)
 (if (or (< index 0) (>= index [fbDateState 0]) (!= index [fbDateState 1])
  (< value 32) (> value 126) (== value 124)) (proc999_1) (return 0))
 (= [fbDate index] value) (++ [fbDateState 1]) (return 1))
(procedure (finaleDateValidate &tmp i value)
 (if (or (< [fbDateState 0] 1) (> [fbDateState 0] 80) (!= [fbDateState 0] [fbDateState 1])
  (!= [fbDateState 2] 996) (< [fbDateState 3] 1) (> [fbDateState 3] 32767) [fbDateState 10]) (return 0))
 (for ((= i 4)) (< i 10) ((++ i)) (if (< [fbDateState i] 0) (return 0)))
 (if (or (not (or [fbDateState 4] [fbDateState 5])) (not (or [fbDateState 6] [fbDateState 7])) (not (or [fbDateState 8] [fbDateState 9]))) (return 0))
 (for ((= i 0)) (< i 80) ((++ i))
  (= value [fbDate i])
  (if (< i [fbDateState 0])
   (if (or (< value 32) (> value 126) (== value 124)) (return 0))
   else (if value (return 0))))
 (if (or (not ((ScriptID 985 0) hStaticRange: 27 0 {P})) (not ((ScriptID 985 0) hStaticRange: 28 0 {S}))) (return 0))
 (return 1))
(procedure (finaleDateInfo field index)
 (switch field
  (0 (if (not (proc999_4)) (return 0)) (return (/ (+ {P+S+149} [fbDateState 0]) 150)))
  (1 (if (or (< index 0) (>= index 80)) (return 0)) (return [fbDate index]))
  (2 (if (or (< index 0) (>= index 11)) (return 0)) (return [fbDateState index]))) (return 0))
(procedure (finaleDateCopy page target &tmp i count start index value length last)
 (if (or (not target) (not (proc999_4)) (< page 0) (>= page (proc999_5 0 0))) (return 0))
 (for ((= i 0)) (< i 80) ((++ i)) (= [fbCaption i] 0))
 (= start (* page 150)) (= count (- (+ {P+S} [fbDateState 0]) start))
 (if (> count 150) (= count 150)) (= index 0)
 (for ((= i 0)) (< i count) ((++ i))
  (if (and i (== (mod i 50) 0))
   (if (mod index 2) (= [fbCaption (/ index 2)] (| [fbCaption (/ index 2)] (<< 10 8))) else (= [fbCaption (/ index 2)] 10)) (++ index))
  (= value (proc999_7 (+ start i)))
  (if (mod index 2) (= [fbCaption (/ index 2)] (| [fbCaption (/ index 2)] (<< value 8))) else (= [fbCaption (/ index 2)] value)) (++ index))
 (StrCpy target @fbCaption) (return (+ index 1)))
(procedure (finaleDateRawChar index)
 (if (or (< index 0) (>= index (+ {P+S} [fbDateState 0]))) (return 0))
 (if (< index {P}) (return [fbDatePrefix index]))
 (= index (- index {P}))
 (if (< index [fbDateState 0]) (return [fbDate index]))
 (= index (- index [fbDateState 0])) (return [fbDateSuffix index]))
'''
PUBLICS='(public finaleBankAt 0 finaleDateClear 1 finaleDateBegin 2 finaleDateChar 3 finaleDateValidate 4 finaleDateInfo 5 finaleDateCopy 6 finaleDateRawChar 7)'
LOCALS=' [fbDateState 11]\n [fbDate 80]\n [fbCaption 80]\n'
