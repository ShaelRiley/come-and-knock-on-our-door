# Exact repair and byte-budget constraints

The patch changes only `991:h6BaseDrawWorld`, `988:h7DrawBunny` and
`988:h7ReturnBunny`. The compiler, heap bytes, method addresses and all script
bytes outside those three intervals match the public pre-repair baseline.
`verify_scope.py` checks the complete fourteen-module set and reverses the exact
three source replacements to recover every prior generated-source hash.

The courtyard renderer now requires location 4 and not-on-apron. Getter results
are reused in the existing temporary to preserve the renderer's byte budget.
Bunny's kitchen renderer accepts a valid final P08 owner while retaining the
prefinal invitation path and original admission guards. The unsigned mouth
clamp and commuted facing predicate are equivalent for all 65,536 SCI16 values.

The legacy Return guard queries the canonical module-989 export's valid final
publication before `h7Begin` or any transition, room or invitation mutation.
The obsolete menu choice remains visible; safe refusal occurs in the called
method. Before final publication, original admission/getter checks retain their
order, and the transition guard remains last.

The compact success tail relies on the selected SCI1.1 VM's variable-selector
write preserving the accumulator object reference. The two NOT operations then
clear the invitation and return success. The source harness instead returns the
assigned room value; original `h7PhysicalValid` requires home room 1, so the same
two NOT operations produce the same result. The ordinary transition already
sets dirty before success, making the removed extra dirty setter redundant.
The paired genuine invited-return test covers the actual valid prefinal route.
This is a deliberately pinned implementation, not a general portability promise
to unrelated VM semantics.

No gameplay source, binary resource, save or runtime was patched in place.
The repaired program is produced by guarded source composition and the existing
compiler. Frozen sources remain unchanged. `SOURCE-CHANGE.diff` is for review;
apply the supplied authoring files and rebuild rather than hand-editing emitted
scripts or saved state.
