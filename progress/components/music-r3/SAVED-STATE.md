# Saved-state admission and retirement

This describes the complete modeled saved music state; it is not a claim that an arbitrary damaged native save file is safe for ScummVM itself.

## Exact static state

All local constants in941/942 and943 are compared to fresh245/246/247 text chunks. Each read buffer is cleared before use. Validation is a function call, never a saved boolean. Current/target gains are excluded from static equality and validated separately. The original240–244 and940 scopes are unchanged. Sound assets, compiler, selectors and source inputs are byte-pinned by the offline aggregate gate.

## Broker state

The sound object supplied by Main must exactly equal the saved owner pointer. Active owner numbers and mode must agree; a running bed must be151/152, and a bridge must match a complete static metadata row. Only one transport may report running. A bed cannot retain bridge position/end/pause/open state. Bridge end/release values must match their exact row, bridge position must be bounded and user/chooser pause must own a real bridge pause.

Whole gain is0–100. Mute/pause/chooser/active/exit/thinking/result/degraded/restore flags are exact0/1. Attempt/generation limbs are nonnegative15-bit words, nonzero where active. Per-encounter highwaters must exactly match the active identity. Exchange is0–5 and consumed responses cannot exceed it. Desired family is151/152 and active desired152 requires a non-exited encounter. Diagnostic counters are bounded0–29999. Invalid enum, owner, pointer, context or checkpoint flags reject before dispatch. A saved disabled bit cannot bypass admission when saved owner/lifecycle work is present.

`rbRestoreBegin` admits only a genuinely frozen chooser checkpoint, not an already-restoring state. It invalidates prior request generation and disposes a saved bridge immediately. Invalid state uses the explicit trusted Main Sound object for stop/dispose, not the untrusted saved pointer or an inherited owner's restored method fields. A retained bed remains frozen until every included host validator succeeds.

`rbRestoreResume` requires ready, nonbusy, nonloading, certain986. An already-active music identity must match the exact restored domain. Highwater, response or exchange cannot be ahead of committed state. It then suppresses every committed response/result already present in that snapshot, without replay or new event consumption counters. Newly established durable context is read directly, not synthesized as a new committed notification.

## Existing MusicTransport state

Admission validates both owner references and optional recovery owner, running flag, all boolean lifecycle fields, state indices, current/target gains, whole targets, modes, current/paused/recovery positions, rejoin/history window indices, bounded rejoin attempts, history/recovery enums and all modulo30000 revision/epoch fields. Current target gains must equal the selected source-derived row. Whole/mute/pause values must agree with broker preferences. A chooser requires the genuine saveGuard plus pausedCheckpoint and owned pause.

Other inherited fields are either signed tick/civil anchors rebuilt by the existing frozen-restore/clock/rejoin path, or diagnostic-only counters that carry no permission or domain identity. Their original43-method arithmetic is preserved. The source/emitted tests check the actual frozen protocol, current gains, clock retention, static mutation rejection, range/owner mismatches, pending response/KO suppression, bridge retirement and repeated same-snapshot loads. Native slot reconstruction, physical channel mapping and wall-clock cadence remain required native gates.

## Host order and no replay

The stock2026.3.0 saved-music path clears the old playlist before reconstructing saved entries. Its replay path abandons the old invocation stack. The guarded host first executes existing P05/P06 domain/PCM/UI/movement retirement, then musical retirement, then its original replay body. The candidate's audioRestore stays frozen. Only final successful Main p05RestoreValidate, after all included domain/physical/scene validators, invokes musical resume. No independent timer, callback, or second parser retains an old musical generation.

A bed's existing frozen parser/clock is preserved. A saved one-shot is discarded and never replayed; only the validated current bed can subsequently start. This is why the scheme does not pretend that a restored counter is globally unique across repeated loads.

Ordinary save/restore coverage refers to this coherent candidate build. Backward save compatibility with older script0 layouts is not claimed; stock ScummVM checks the saved game-object/script0 identity.

## Revision-2 presentation state

The broker UI cache is constrained to -1..6 but grants no admission, generation or ownership. Its display buffer is cleared and freshly loaded before use. Generation exhaustion remains error9 through requests, polls and user retry; it is not cleared by presentation or equal-target coalescing. Ordinary complete restore admission remains required.

## Revision-3 save admission

A new active save is refused at the maximum generation or error9 before a native snapshot can be produced. `rbSaveRefused` is only a 0/1 display diagnostic; changing it cannot authorize a save. The last admissible counter reserves the existing restore advance. Ownerless failure can open only the validated load chooser, never the save chooser. Cancel and R leave the finite lifetime unchanged. Earlier successful saves load through complete Main/P05/986 replay admission.
