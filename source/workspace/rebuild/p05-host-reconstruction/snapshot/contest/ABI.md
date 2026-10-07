# NEW Contest numeric ABI

This is a newly authored stock SCI1.1 domain. Original scripts986/997 are missing. No recovered source, historical enum, ABI, save compatibility or native implementation is claimed.

## Allocation and immutable text

Script986, class ContestState species8, instance contestState export0. The coherent compile preserves class slots0–7 and all1,001 sealed P05 selectors, appending sorted Contest selectors from993; reserved compiler IDs4096–4103 are unchanged. See build/compile-receipt.json and selectors.json for exact allocation. Main is the corrected r2 P04 source and has no Contest call sites. Compiler proofs are non-runnable.

manifest.json is the numeric allocation authority. Encounter1–4 = VC01–VC04, source5–8 = P02/P06/P11_SAFE/P12_P13. Pair/reply IDs1–24 are IR01–IR24; response0 is absent,25 is explicit exchange yield. Half0 = complete setup/reply/recap sequence;1=setup,2=reply,3=recap. Phase1–8 follows the accepted reference exactly. Event kind1=attempt,2=exchange,3=outcome,4=text. Winner0/1/2=none/Jackie/opponent; reason0/1/2=none/zero/explicit contest yield.

Canonical record IDs1–154 and speech-unit IDs1–134 are fixed in manifest.json in unchanged fixture order. A unit ID0 means readable silent text, not an invented actor. The same manifest retains exact speaker strings and eight-writer attribution; each writer has three accepted pairs. The unchanged canonical fixture contains every byte, speech owner, optional Bunny quotation and credit. Numeric results instruct the host which exact item to render; this domain neither truncates nor rewrites text. No replacement scenes or native glyph mapping were generated.

## 140-word logical state

Every word is nonnegative0–32767. Each serial is unsigned30 represented high then low, base32768. A high/low pair supports0–1,073,741,823 exactly; no signed overflow or rollover is used. Seed uses two bytes0–255. manifest.json.state_offsets is authoritative:

- 0–5: revision, attempt serial, presentation serial, two words each
- 6–9: four introduced bits;10–57: setup/reply bits for24 pairs, in pair order
- 58–89: four histories, eight words each: completedHi/Lo, winsHi/Lo, latestWinner, concessionRecord, lastOutcomeHi/Lo
- 90–105: active flag, encounter, phase, seedHi/Lo, cursor, Jackie/opponent composure, pendingResponse, exchangeSlot, winner, reason, KO committed, KO consumed, result presented, prior-win bit
- 106–110: exact saved ordered deck, five pair IDs
- 111–125: five exchange triples response/correct/effectConsumed; slot is index+1 and pair is the matching deck item
- 126–131: purpose, source, pair, half, textCursor, textCount
- 132–139: four record IDs followed by four unit IDs, unused entries zero

An absent active attempt or presentation requires all its fields/padding zero. Active serial equals global attempt serial; presentation serial equals global presentation serial. These equalities, exchange pair/slot identity and canonical single-half selection are represented once, not redundantly with independently mutable copies. The bridge to the reference schema is lossless; tests compare all140 words after every logical step. Normal load never recomputes or replaces a saved deck: validation computes a separate scratch expected deck only to reject corruption.

## Candidate transaction protocol

The documented public action API prepares one candidate and returns1 on success. The committed live words remain unchanged. Invalid/stale operations return0 without a candidate. A successful prepare sets vcBusy1; subsequent mutations, save, load and lifecycle work are rejected until the synchronous owner resolves the transaction.

1. Invoke the action, returning1
2. Read exactly140 vcCandidateWord(index) values while vcBusy1
3. Atomically commit this candidate with relevant campaign/P05 state using the host persistence coordinator
4. Call vcCommit only after definitive successful persistence; publication copies the candidate and exposes any new effect
5. On a definite non-commit, vcAbort discards the candidate
6. If durable outcome is uncertain, call vcStorageUncertain and recover the authoritative snapshot through vcLoadBegin/Word/Commit with a newer ownership generation. Neither rollback nor retry is asserted

vcRead(index), vcFlags, vcLearned, vcNotebook, vcAlternative and vcPractice read committed words even during persistence. vcCandidateWord is the explicit candidate view. The finite domain performs no filesystem writes, kernel calls, rendering or external callbacks. The host must enforce synchronous exclusive coordination; direct properties, internal helpers and local arrays are not an untrusted plugin interface.

Flags: resolved bits1/2/4/8, permanent won bits16/32/64/128, ALL_VC_WON256. A committed loss resolves; it cannot remove an earlier won latch. Introduction queues exact entry text only. Flags do not imply campaign completion or external puzzle prerequisites. RESULT_PENDING is a hard campaign interaction barrier even though committed flags are already readable for atomic persistence.

## Operations and text receipts

- vcIntroduce(encounter, admitted): fresh explicit host narrative admission1 required
- vcLesson(source,pair,half,admitted): encounter sources require introduction/eligibility; external sources require correct tier and explicit admission1
- vcCancelLesson(): retain only displayed setup/reply halves
- vcAcknowledge(): require captured text token; acknowledge only after every page of the entire canonical item was readable
- vcEnter(encounter,seedHi,seedLo,admitted): require idle, no queued text, introduction, full eligible repertoire and fresh admission1
- vcBeginTurn(), vcChoose(response), vcCommitResponse(), vcYieldContest(), vcCommitKO()
- Exchange yield is vcChoose(25), persist/publish, then vcCommitResponse with the same logical exchange and current-generation token; these are deliberately two transactions
- vcClaimEffect(kind,slot): persist once-only consumed bit before performance
- vcLifecycle(action):1–8 = skip/mute/pause/menu/save/load/room_change/new_speech; suppress current effects only, never score, yield or dismiss text

Before any token-based operation, call vcSetInput(generationHi,generationLo,serialHi,serialLo,kind,slot,record,unit) with the captured receipt. Attempt/outcome slots are0; exchange slots1–5. Text slot is the zero-based item cursor; it includes the exact record/unit and presentation serial. Non-text record/unit must be0. Acknowledging setup during an actual contest never teaches an unseen reply; only lesson receipts teach the displayed half. Recap and requesting text teach nothing.

Read pending text from the committed descriptor and records[textCursor]/units[textCursor], with source identifying opponent-name bindings. vcLearned(pair,2) enumerates every learned reply across all tiers. vcNotebook never returns an unlearned setup/reply. vcAlternative requires learned setup and learned reply; vcPractice returns canonical correct/mismatch record and never mutates state. Invalid query returns0.

The model’s recap list is a read-only host projection: require the encounter’s introduced bit, enumerate pair1 through encounter*6, and return its two learned bits plus the three canonical record IDs. missing_wins is the absent subset of the four won bits. result_presentation_pending is active1 and phase7. The immutable manifest supplies record IDs; these projections never acknowledge text, grant learning or start a transaction. Active/event/text query values are assembled from committed words plus the current bound generation. These query projections do not create a second state owner.

After a successfully published effect claim: vcEffect1=Jackie non-contact wince,2=opponent non-contact wince,3=standing social KO; vcEffectRecord identifies the exact KO record for kind3. No actual pose or audio is emitted here. Failed/duplicate/suppressed claims yield no new effect. Loss by contest yield has no KO effect. New input must not replay output from a prior transaction.

## Save/restore and ownership generation

Word envelope: magic22083, schema1, exact word count140, identity NEW-CONTEST-SCI-B15-V1. vcSaveReady validates the live state and suppresses old transient effects; then read all140 vcSaveWord values. vcLoadBegin(magic,schema,count,newGenerationHi,newGenerationLo), exactly ordered vcLoadWord(index,value) calls, and vcLoadCommit validate a complete candidate before replacing the entire logical timeline. Any rejected envelope/word/state leaves committed words and generation unchanged. Extra/missing/out-of-order words fail. vcLoadCancel abandons staging. The generation must be strictly newer both at begin and at final commit, so a queued older restore cannot retire a newer owner.

A native word envelope has no JSON type tags or cryptographic checksum. A JSON/file bridge must enforce exact typed schema, catalog fingerprint, integrity checksum, bounded size, duplicate-key rejection and boolean-vs-integer separation before numeric encoding; the accepted reference codec is bundled as authority. Binary word validation is fully implemented here. This packet does not claim to provide a native disk codec or protect against deliberate save forgery.

Generations, input receipts, candidate ownership, suppression arrays and PCM/task handles are conceptually host-transient and excluded from the140-word logical envelope. Whole-VM RestoreGame nevertheless restores ordinary SCI globals, locals and properties. Merely incrementing vcGeneration after restoring a saved VM is NOT process-global freshness. Before any saved callback/input resumes, the host must synchronously stop/retire every prior callback, PCM queue, page owner, pose and audience task; call vcAfterRestore to block dispatch and suppress committed effects; then establish a genuinely fresh outside-graph generation via vcBindGeneration, or independently prove total retirement before reissuing tokens. This packet supplies no UUID guarantee and makes no native lifecycle acceptance claim. At maximum generation, fail closed and use an explicitly reviewed ownership-rebuild/migration procedure; do not silently wrap.

The word-level loader’s restored text/phase/deck/learning/history exactly replace current state, never union later knowledge/wins or replay consumed/previous effects. Newly committed effects after restore remain eligible. Host admission, campaign atomicity and native callback retirement are separate integration gates, not hard-coded successful booleans.

## R2 stricter lifecycle and history validation

vcSetInput clears vcInputReady and both published output fields before any argument/busy validation. A malformed replacement therefore cannot leave the previous receipt armed. Every vcClaimEffect invocation clears published outputs before validating its kind/slot, including rejected or duplicate calls. These transient retirements never change the logical words, prepared candidate or vcPreparedEffect/vcPreparedRecord; a successfully committed candidate still publishes its prepared effect.

Every nonempty completed encounter history now requires both learned halves of its full eligible pool, regardless of win, loss or explicit yield. This invariant follows from the admission prerequisite plus monotonic learning within a retained timeline. An older valid snapshot can still replace both later knowledge and later history together; no union is performed. The140-word layout, numeric IDs, selectors and canonical fixture are unchanged.
