# Side-passage score identity correction

An ordinary native New Game route reached the side passage with Music ON
and displayed `MUSIC UNAVAILABLE. F3 TO LOAD.` Later save requests were
refused by the existing music safety guard. Read-only inspection of the
unmodified stock runtime identified the requested sound as 105, with the
transport unavailable before a sound handle was admitted.

The recovered generator applied operand replacements sequentially. Its
template sound 140 first became resource 105; the next replacement treated
that new 105 as the template window-count operand and changed it to 190.
The canonical and editable generated `module952.sc` consequently compared
the real sound object's number against 190 in `start`, `rawPosition` and
`observeHistory`.

All three number comparisons now use 105. The two actual window-count
comparisons remain 190. The generator replaces original operands in one
pass, so a newly inserted resource number cannot be remapped a second time.
No ownership, lifecycle, history, save guard, transition rule or engine code
has been weakened. No progress or save state has been edited.

The bounded static pin check now inspects these three comparisons in each
of the 17 transports, in both canonical and editable generated sources
(102 comparisons). It also exercises the pure replacement function on the
specific 140-to-105 / 105-to-190 collision. This is source verification,
not a substitute for native acceptance.

The same candidate corrects obsolete player captions that described the
already replaced audience recordings as synthetic test chuffs. Five text
strings changed; reaction consumption, sound controls and recordings did
not. Historical source-specific rights and procedural character voice
qualifications remain intact.

All four bounded static cases pass. All 46 modules compile; receipt SHA256
`e4dd3fb97063f504cf8dff992c8c74a1272c469912f57e7b3638efb924ef1789`.
Fresh staging produces 1,759 game files and 254 typed resources. The only
compiled changes are module952 script and module991 script/heap; the other
89 compiled artifacts are byte identical. Native New Game acceptance is
in progress and no complete native pass is claimed. Predecessor saves remain preserved in
separate directories and their compatibility is unproved. Subjective
listening has not been performed.

The corrected candidate has now completed a genuine New Game opening and
P01-P04 with Music ON. P01 save/change/restore and a genuine P04 save after
the gate success passed. The Music unavailable warning did not recur.
The corrected Audience OFF/ON captions were observed; Audience ON was
restored. These observations do not validate P05-P14, all four required
wins, the ending, credits or subjective audio quality. Generic sample-tile
inventory labels remain a presentation issue for a subsequent correction.
