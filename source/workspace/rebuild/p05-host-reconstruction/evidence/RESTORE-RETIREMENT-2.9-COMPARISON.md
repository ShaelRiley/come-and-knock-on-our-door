# Source/emitted retirement boundary, not native acceptance

This new controller deliberately relies on total stale-work retirement, not on
uniqueness of a counter stored inside a restored SCI heap. The two P05 lease
values can repeat across restores. That fact is explicit and tested; neither a
UUID nor a fabricated stock kernel is used.

## Pinned engine mechanism

The inspected upstream ScummVM v2.9.0 sources are copied here only as reference:
`https://raw.githubusercontent.com/scummvm/scummvm/v2.9.0/engines/sci/sci.cpp`
and the same engine's `engine/savegame.cpp`, `kevent.cpp`, `vm.cpp`,
`ksound.cpp`, and `kgraphics.cpp`. See the adjacent source files and provenance
hashes. `savegame.cpp:1533` requests kAbortLoadGame. `sci.cpp:710–750` leaves the
old run_vm invocation, clears `_executionStack`, and starts the game object's
`replay` selector. Saved return addresses are not resumed in the old callback
stack. `kevent.cpp:44–93` consumes GetEvent(mask, object) from the current event
manager; this game's stock mask32767 is not a peek.

## First restored script action

Main.replay begins with p05RestoreBegin before its previous assembly body.
P05State.hRestoreBegin first invokes p05AfterRestore, which blocks input and
retires input readiness. It then calls Main.p05RetireTransient synchronously:

1. Cancel the single PCM owner, stopping DoAudio and DoSync; clear pending
   laughs, audio pending/dialogue fields and duck timing
2. Invalidate scene paint/audio generation using sdAfterRestore and suppress
   replay/start/armed speech
3. Cancel pending movement/action identifiers and phase
4. Clear all64 native UI action/payload/label entries and current event fields
5. Drain GetEvent32767 until no event remains, without invoking input,
   uiActivate, narrative dispatch, audio completion, or any domain action
6. Clear captured P05 receipt words/session, then bind the replacement lease

The game has one synchronous eventLoop. It does not register timer, renderer,
reader or narrative callback objects, or a separate task capable of retaining a
P05 token. Scene queues contain document IDs and kind0/1, not callback addresses.
The only source receipt entry is hPresented called by dialoguePresented after
the frame's Graph12 call, guarded by the exact document/page/scene identity,
matching current paint generation, room/object availability, and unobscured UI.
The direct kernel/selector audit and source callsite checks establish this graph;
they do not turn an arbitrary direct test call into a native display receipt.

## Logical restoration

Strict P05 state/context/physical projection validation precedes re-enabling
normal work. A pending source is preserved only when its source/record/room,
current document, page count and exact0/1 visited bitmap/count agree. The host
reissues only the current scoped token. Invalid partial reader data is discarded
without granting knowledge; invalid physical/domain composition fails closed.
All actual P05 source records are one page. Tests therefore preserve a genuinely
unpresented one-page request and do not insert a synthetic multipage source.
Existing P03/P04 multipage restore coverage is separately rerun.

Repeated same-snapshot tests drain obsolete click/Enter events, preserve logical
state, suppress old PCM and queued speech, reject the pre-restore ticket, and
require a later fresh real frame before observation commits. These execute the
actual newly emitted replay/event-loop instructions with explicit kernel mocks.
Native ScummVM restoration, physical audio and rendered pixels remain pending.
