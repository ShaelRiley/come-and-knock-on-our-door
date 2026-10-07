# Source-item routing contract

## Namespaces and lookup

Domain identifiers are taken unchanged from the accepted986 manifest. Context0 is a generic notebook/interface;1–4 are VC01–VC04;5 is P02/LEARN_A;6 is P06;7 is safely completed P11;8 is P12–P13. Context is a caller attestation, never inferred from the cast name. Actual location, actor availability, protected choreography, practical prerequisites and eligibility belong to the host.

Lookup uses `(record, unit, context, variant)`. Static records and opponent-bound dynamic results use variant0. Notebook dynamic variants are selected only from the finite contract. Unknown IDs, booleans as integers, absent contexts, masks outside bits0–8, ambiguous routes and malformed state fail closed. A matching context mask does not grant narrative admission.

Every active row now has first_page0 and page_count equal to the full document's sdPageCount. The28 aliases854–881 use existing absolute page-row starts and counts. They add only112 bytes of start/count words, no physical pages, text or audio. Full aggregate backing documents remain available and unchanged, but their unit0 routes are deliberately absent for multi-unit ENTRY/WIN/LOSS. Individual domain items always use alias documents. `generated/vc01-routing-proof.json` shows every reused original record and all exact-unit aliases.

No aggregate containing all setup variants exists. Each IRxx.SETUP context speech unit selects only its canonical unit; unit0 external lessons route to an explicitly silent exact-caption document. The silent external header is the existing canonical Notebook label; the original source speaker remains Active opponent in provenance. Optional Bunny speech exists only under its own canonical LEARN_A unit/context. Neither a silent lesson nor a domain0 item silently chooses Milo.

Singleton replies retain exact Jackie unit IDs. The host may gate or mute audio when an actual actor is absent; it must preserve the full canonical text. Silence, stage/control text, audience captions and interface fields never create a new profile.

## Receipt and outcome boundaries

A draw/open/queue/voice event is not a source receipt. Use the existing fresh, unobscured, successful sdDraw/Graph12 presentation receipt for every page of the exact document, together with the current domain owner generation, presentation serial, cursor, record and unit. The alias identity does not authorize counting the backing aggregate again. One queued canonical source item has one domain receipt, independent of how many aliases expose the same bytes. sdPresented returns whether sound was armed, so0 is normal for a successfully presented silent caption; its return is not the text-acknowledgment predicate. The host separately verifies the exact completed draw/Graph12 observation.

Each entry unit and concession/flourish unit is separately acknowledged. Wrong-context, stale, hidden, skipped and sibling-unit presentations cannot advance it. Audio ending or being skipped does not acknowledge text or teach a reply. Logical score/KO results are committed by986 independently of performance. The host must not let newly committed RESOLVED hide a still-unpresented concession behind a loan, room change or practical handoff.

All four WON latches remain distinct from RESOLVED and all physical/personal outcomes. This exporter never changes either, never grants admission and never completes P14 or a promise. It does not implement whole-VM callback retirement or campaign atomic save composition.

## Exact dynamic UI fields

All nine dynamic records retain their original raw templates and source obligations. Every displayed expansion uses that template literally except the named fields. `dynamic-contract.json` contains172 finite variants, canonical-value JSON pointers, state constraints and ordered fixed/field spans. All values are silent captions, bounded by512 UTF-8 bytes before pagination and64 pages (actual maximum3). Text pages retain contiguous expanded-string character/UTF-8 spans, clearly distinguished from template spans.

- opponent_name: exact unit speaker name for the active VC01–VC04 encounter
- insult/retort: exact accepted pair strings. PAIR requires both learned halves; SETUP_ONLY requires learned setup and unlearned reply
- won_count: decimal population count of the four earned WON flags
- missing_contest_names: the exact opponent names for missing wins, ordered VC01–VC04, joined with comma-space. For all four wins, the UI selects the exact VC.GATE.ALL_WON record; no empty-list prose is invented
- learned_count/required_count: count of fully learned eligible pairs, out of6/12/18/24 for the actual encounter. Later knowledge does not inflate an earlier pool
- learned_valid_retorts: only the exact learned accepted-other-response subset, ordered by canonical response ID and joined with newline. Empty subsets hide this optional field. An untaught alternative is never exposed

The host should derive these from canonical state, as routes.ui_route does; it must never accept arbitrary field strings. No field order, canonical words, existing names or accepted-answer relations are rewritten. A notebook UI read does not itself grant a pending domain lesson receipt.

## Resource/segment budget

Current source982 is44,288 aligned bytes, leaving21,247 of the65,535-byte script/heap segment. Existing local tables contain12,345 words. Each additional physical page consumes11 words (22 bytes):8 page fields plus text resource, audio module and duration. Each added document or page-sharing alias adds2 words (4 bytes). Thus a later expansion with P physical pages, D documents and C new code/alignment bytes needs at least22P+4D+C bytes.

P06–P14 remain unimplemented in this export and have no invented page estimates. Reserve the entire21,247-byte remainder for their independently measured scene tables and any reviewed code growth. Even if C were zero, one-page documents would fit at most817 additional documents; this is an optimistic arithmetic bound, not a capacity promise. Every later import must recompile, recheck signed indices/local offsets, alignment and the full segment. The399-row host lookup consumes5,586 bytes outside982 and must be budgeted in its actual owner, not Main by default.
