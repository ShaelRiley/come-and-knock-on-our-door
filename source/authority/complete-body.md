# Come and Knock on Our Door

## Game Design Document

Complete authored proposal for review

A 90–120 minute point-and-click ensemble comedy about turning an oversold house party into an honest shared success. Play Jackie Tree as he helps Bunny Easter and Frankie Maplewood prepare a supper-club trial, navigates the neighbors’ contradictory expectations, and wins a concrete agreement about the household’s future. One evening, seven reusable scenes, fourteen connected puzzles with four embedded verbal competitions, and eight principal characters keep the design small enough to finish.

The game presents a late-1970s and early-1980s sitcom world with colorful party culture, an original reactive MIDI score, a laugh track, and a physically present studio audience beyond the authored set boundaries. The audience can participate in a few fair puzzles; it cannot reveal private facts or bypass the adventure. Monkey Island 2 is the main interface and musical-methodology reference. The secondary adventure references are King’s Quest, Quest for Glory, and Indiana Jones and the Fate of Atlantis. The design combines tactile object puzzles, characterful favors, investigation, and ensemble comedy while using modern hints, saves, readable interactions, and recoverable mistakes.

## Confirmed direction and authored choices

Confirmed by the brief: exact title Come and Knock on Our Door; playable Jackie Tree; roommates Bunny Easter and brunette Frankie Maplewood; Mr. Stringer as the house’s landlord, who permits Jackie to live with the women because he believes Jackie is gay; original analogues for the wider sitcom ensemble; the small 90–120 minute scope; Monkey Island 2’s nine-verb interaction system; unmodified stock ScummVM as the required runtime; an original reactive soundtrack targeting FluidSynth with FluidR3_GM.sf2, including authorized adaptation and reuse of the user’s five Suno-created MIDI bundles; generous authored crowd reactions in dialogue and physical comedy; eight distinct procedural speech-balk voices with synchronized mouths; an animated physical-comedy opening introducing all eight principal characters through original movement followed by freeze frames and name cards; the sixteen supplied visual references reproduced in the visual reference gallery; and occasional fourth-wall interaction with a live audience at the map boundaries. The user also requires four recurring face-to-face insult competitions with a learned repertoire, original fighting-game-style composure meters and social KOs, plus a happy final freeze-frame with audience celebration and a full fictional television-production end-credit sequence.

The specific story, puzzle solutions, occupations, other character names, visual layout, control conveniences, pacing estimates, cue structures, and relationship details below are authored design choices for review. They form one complete proposal, rather than unresolved plot placeholders. Milo Pennant, Vivian Voss, Rita Stringer, and Felix Bunt are new names; Felix is a freelance handyman and stage-effects enthusiast, never a second landlord.

SCI1.1 is the chosen implementation foundation, with an original stock-compatible P01 checkpoint running in unmodified official ScummVM 2026.3.0 on cloud Linux. This is an implemented first-puzzle foundation, not a completed production game or full audio acceptance. The required FluidSynth, FluidR3_GM.sf2, and reactive-music contract is unchanged. The broader integrated slice, remaining game, final score and art, and actual Steam Deck controller/listening acceptance remain open. Historical patched-runtime diagnostics are not the shipping route. Distribution details and release clearance remain production work.

## Reading this document

The narrative and puzzle sections define the complete playable route, prerequisites, items, clues, hints, and consequences. The interaction and presentation sections define how the player experiences it. The audio section specifies the complete score and audience system for later production. The research appendix explains the qualified three-episode shortlist and thirty moment abstractions. The directed relationship appendix includes every named character’s feelings and wants toward each of the other seven.

Companion player-facing script. [Come and Knock on Our Door — Complete Player Script](https://docs.google.com/document/d/1HpiFbCn7FniV3kLjTDP5nP1Ow0N5JMHuEeO0EeG1rEQ/edit) is the authority for the full player-facing wording: dialogue, interaction responses, narration, hints, captions, and performance directions. The GDD remains authoritative for mechanics, puzzle structure, scope, and story requirements. The separately authorized verbal competitions and final credit presentation below expand the mechanics and ending presentation and must be reflected in the complete script. Outside those explicit additions, the editorial pass remains language-only: improve phrasing, characterization, comic timing, and authored reaction placement without adding or altering puzzle flags, prerequisites, solutions, inventory behavior, knowledge gates, rooms, relationships, or endings. Extra comedy-beat IDs are presentation metadata, not new puzzle state. The illustrative lines retained here do not replace the complete script.

The separate relationship map source in the project folder also records beliefs, misunderstandings, and suggested dramatic leverage. This Google Doc is the single living canonical GDD. Its project-folder source is a link-only file, not a synchronized duplicate of the document.

## The game in one evening

Jackie Tree, Bunny Easter, and Frankie Maplewood share a rented coastal house in an invented late-1970s/early-1980s seaside neighborhood. Mr. Stringer rents the house to the three friends because he believes Jackie is gay. That mistaken belief is an inherited complication, not a performance the player must imitate or a reason to mock anyone’s identity.

Tomorrow, the household and Stringer are due to discuss renewal and overdue courtyard repairs. Tonight, the housemates have offered a small, resident-run supper-club trial to demonstrate that their shared home can accommodate guests responsibly. Jackie sees a chance to establish himself as a cook; Bunny wants her event promotion taken seriously; Frankie wants the household’s responsibilities and Stringer’s promises written down. These are authored fictional circumstances, not statements about tenancy law. There is no midnight eviction or real-time legal deadline.

Neighbor Milo Pennant has promoted an evening of “new partners” using three selectively abridged versions of the same invitation. Jackie expects potential culinary collaborators, Vivian Voss expects to evaluate a styling collaboration, Rita Stringer expects her ceramics to be credited, Felix Bunt expects a practical demonstration of his repair work, and Mr. Stringer expects an impeccably quiet household supper. Nobody has agreed to the evening everyone else imagines. Jackie’s original mistake is saying yes to each person without asking what the promise means.

The player turns these incompatible expectations into one genuine event. The solution is a physical as well as social achievement: transport clattery ceramics, repair a decoration-obstructed gate, route a temperamental sound setup, build a privacy screen, cook for eight, fit the activity into a tiny courtyard, retrieve a useful viewpoint from the live studio audience, and finally send people, dinner, and a cumbersome display through three different openings in the correct order.

The ending gives the household an ordinary renewal commitment and a scheduled repair, gives every contributor visible credit, and leaves room for the sitcom to continue. Mr. Stringer is persuaded to judge the tenants by their conduct and care for the property. Jackie does not need to disclose or perform a sexual identity, pursue a romance, or expose anyone else’s private life to win. Vivian’s collaboration works whether Jackie expresses friendly, professional, or cautiously romantic interest.

## Cast functions in this story

- Jackie Tree is the sole playable character. He can cook and improvise, but his desire to please everyone produces avoidable promises. His playable growth is asking precise questions and accepting competent help.

- Bunny Easter is socially bold, kind, and observant. She notices how people interpret a room and can recruit willing listeners. Her literal reading of inflated publicity catches Milo’s exaggerations.

- Frankie Maplewood is the brunette housemate, dry and practical. She turns vague intentions into a workable plan and notices the release mechanism when Jackie panics over an awkward physical problem.

- Mr. Stringer is the only landlord. His public propriety and need to appear in control collide with his private affection for the household and his wish to make Rita happy.

- Milo Pennant is a neighboring party promoter and second-hand hi-fi trader. He overstates his importance but genuinely wants to be useful. He supplies the public-address kit and handcart once Jackie offers honest credit instead of another bluff.

- Vivian Voss is an event stylist. She may be attracted to Jackie, but her tangible goal is a competent collaboration. She supplies a folding screen frame and teaches the player to control sightlines.

- Rita Stringer is a ceramics tutor and social organizer. She lends her service and brings a ceramic house-number panel she has made for the three tenants. She wants authorship, a real part in the evening, and a social life that does not depend on being introduced as someone’s wife.

- Felix Bunt is a freelance handyman and amateur stage-effects enthusiast. He is talented and anxious to be respected. He repairs and tests equipment; he has no lease, rent, eviction, or official inspection powers.

- The studio audience is one collective theatrical presence, not an expanding ninth cast. Audience members can report what they can genuinely see or hear and respond to an invitation to participate. They do not know private character facts or supply arbitrary inventory items.

The full directed relationship map should remain the authority for feelings and wants. Every puzzle below pays off one or more of those wants rather than treating people as interchangeable inventory dispensers.

## Finite geography

Seven principal screens are sufficient. Close-ups and audience-apron reveals reuse their parent scene and do not create a second navigable world.

- L01. Principal screen: Shared living room Exits and permanent functions: Front door to L03; kitchen door to L02; rear arch to L05. Planning chalkboard, invitation comparison, finale pledge board.

- L02. Principal screen: Kitchen Exits and permanent functions: Door to L01; serving hatch to L05. Recipe, pantry, clean linen, utensils, cooking and service. The hatch passes objects; Jackie cannot climb through it.

- L03. Principal screen: Front porch Exits and permanent functions: Front door to L01; side path to L04; short neighborhood exit links to L06/L07. Welcome sign, arrivals, initial tutorial.

- L04. Principal screen: Side passage Exits and permanent functions: Porch to L03; spring gate to L05. Laundry clips, decoration hooks, temporary display staging pocket, gate mechanism.

- L05. Principal screen: Courtyard Exits and permanent functions: Rear arch to L01; gate to L04; object-only hatch to L02. Three clearly marked activity zones and one protected circulation lane. The principal finale stage.

- L06. Principal screen: Milo’s garage lounge Exits and permanent functions: Short return route to L03. PA, record/tape demo station, invitation master, handcart.

- L07. Principal screen: Stringers’ conservatory Exits and permanent functions: Short return route to L03. Rita’s ceramic service and display, Stringer’s chairs, invitation copy.

The short neighborhood transition is one click between the named neighbor destinations, not an eighth exploration screen. Bedrooms, bathrooms, street businesses, rooftops, vehicles, a separate nightclub, and a second house interior are outside this version’s scope.

### The edge of the set

Walking beyond a visibly terminating wall or scenic masking flat pulls the camera back to reveal a narrow audience apron. This is a real Walk to interaction, never merely an invisible-wall quip. A permanent Return to the house hotspot and an ordinary walk back onto the visible set restore the exact prior room state. Save/load also preserves which side Jackie is on.

The seven scenes share one bounded seating/apron treatment with scene-specific sightlines. The audience apron has only a seat row, a speaking position, the visible edge of the active set, and the return path. It cannot reach another room, bypass a locked story gate, take Jackie behind inaccessible machinery, or introduce a hidden inventory store.

P01 shows one conspicuously unfinished scenic edge and an optional captioned audience greeting, making the convention discoverable. P05 accepts an audience soundcheck as an alternative to Bunny’s help. P12 requires the different audience-side viewpoint to read the actual public cue cards. The audience only reports the visible words, not their correct interpretation or sequence. An unobtrusive stage-edge icon and optional hotspot reveal make this fair even for players unfamiliar with fourth-wall games.

## Opening credits and freeze frame introductions

Confirmed feature: a new game begins with an animated physical-comedy opening that introduces each of the eight principal characters through original performed movement before a stylized freeze frame and exact-name reveal. The order, portraits, timing, visual treatment, and controls below are authored design choices for review. These illustrative portraits sit outside live gameplay; their props are not pickups, puzzle demonstrations, or changes to anyone’s starting position.

E00 lasts 60 seconds in default autoplay: 0–6 seconds for the original game-title card; 6–54 seconds for eight consecutive six-second introductions in the order below; 54–60 seconds for the final title composition and transition to the live porch. Each introduction has roughly two seconds of original character action followed by a four-second freeze and name card. This minute is included in the existing 12–15 minute opening/P01–P02 allowance and the overall 90–120 minute target. Pauses and manual card holds may extend viewing time without adding gameplay.

Jackie Tree steadies an empty saucepan while catching its wobbling lid. Freeze on his delighted, overconfident recovery; a teal offset paper-cut silhouette carries the name Jackie Tree.

Bunny Easter lifts a handmade paper-sun garland and peers through its central opening. Freeze on her bright, appraising glance; a coral sunburst frames the name Bunny Easter.

Frankie squares a small blank planning board, then notices that its frame is still crooked. Freeze on her dry raised eyebrow; a mustard geometric grid frames the name Frankie Maplewood, with her brunette hair clearly readable.

Mr. Stringer measures the gap between two chairs with theatrical precision. Freeze as he checks the ruler against his own judgment; rust-colored measuring lines frame the name Mr. Stringer.

Milo Pennant fans a handful of unprinted party cards like a grand showman. Freeze before the cards can fall; an orange radiating fan supports the name Milo Pennant, without displaying invitation text or a puzzle clue.

Vivian Voss compares two fabric swatches against her sleeve and decisively chooses one. Freeze on her confident appraisal; a plum split-color mat presents the name Vivian Voss.

Rita Stringer turns a freshly made cup at her workbench to admire its glaze. Freeze on the maker’s proud inspection; turquoise ceramic-circle shapes frame the name Rita Stringer, giving her independent creative identity.

Felix Bunt checks his spirit level, then realizes his own hat is askew. Freeze on the sideways glance; ochre drafting marks carry the name Felix Bunt. No landlord, official inspector, or tenancy authority is implied.

Opening animation requirement. Stage visible physical setup, escalation, and payoff before the freeze-frame reveals. The opening may draw on the adventurous comic pacing of Indiana Jones and the Fate of Atlantis and Monkey Island 1 and 2, while using original actions, staging, assets, dialogue, and choreography. The eight actions and 60-second structure already specified remain the design baseline; static cards alone do not satisfy it. The prototype’s ten static title/cast/end cards establish timing and controls only, not finished physical animation.

Use the original cast and reusable set crops, with readable portrait expressions informed by V04 and ensemble warmth informed by V07–V16 in the visual reference gallery. Bold period-inspired typography, warm graphic shapes, and restrained print-style offsets are proposed treatments; the references do not themselves establish a freeze-frame layout. Keep the eight actions, name cards, order, and timing above unchanged. Avoid flashing cuts, actor likenesses, copied television shots or choreography, recognizable logo treatments, and borrowed theme music. Cards identify fictional characters, not invented performers. Any displayed production credit must name a verified contributor and role; the supplied Suno MIDI bundles have recorded source authorization; final art, other music sources, recordings, fonts, and notices retain the existing provenance and release checks.

MUS01_INVITATION gains a CREDITS arrangement using HOME motifs developed from the authorized source MIDI bank and the confirmed FluidSynth/FluidR3_GM target. Preserve the 60-second default opening contract. Earlier first-pass bar/tempo choices are superseded as arrangement defaults. Select the revised form after the short feel audition is accepted; rendered audio tails must not add mandatory screen time, and native timing still requires validation. Visual card timing need not coincide with bar boundaries. The full-watch ending resolves into MUS01’s quiet P01 state. Pause freezes both picture and transport; manual card advance repositions the presentation and its authored musical segment together with note/controller cleanup, without waiting for a bar. Holding a card pauses its picture and music. Skip uses a short controlled fade and cleanup before entering the same P01 music state. Exact seek/restart behavior belongs in the native audio proof; these are composition and implementation requirements, not finished assets.

Provide an always-available Skip opening control and pause/manual-advance controls through mouse, keyboard, and mapped controller input. Reduced-motion mode uses static portraits and brief dissolves. Name cards stay high-contrast, clear of faces, and readable in the large-text presentation; holding a card allows unlimited reading time. No narration or hearing is required. An optional short, original or cleared collective audience applause may accompany the title under the Audience volume/Off setting; no extra laugh cue or ninth named cast introduction is needed.

Completion or skipping during New Game initializes P01 once: Jackie on L03 with the covered bread-cue tray and print packet, every NPC at the existing arrival position, and no solved puzzle flags. The verb HUD appears only when control is handed to the player. Continue loads the selected save without replaying E00. Replay opening from the menu uses isolated presentation state and returns to the invoking menu or session without changing inventory, progress, saves, or consumed laugh flags. The live P01 scenic-edge greeting remains the playable discovery of the studio audience.

## Narrative sequence and estimated pacing

Target: approximately 90–120 minutes for a first play with ordinary exploration and some failed ideas. This is an authored pacing target, not a measured claim. Validate it in blind playtests; an experienced player following the walkthrough should finish substantially faster.

- Opening credits and P01–P02. Approximate first-play allowance: 12–15 minutes, including the default 60-second credit sequence within this allowance. Play and story purpose: Jackie’s doorway problem establishes verbs, the ensemble, and three contradictory invitations. The household names its real goal.

- Parallel preparation P03–P07. Approximate first-play allowance: 28–33 minutes Play and story purpose: Ceramics, gate, sound, screen, and cooking can be progressed in a flexible order. Each involves a person’s specific practical need. VC01 with Milo and VC02 with Vivian occupy short social beats within these existing branches.

- Courtyard arrangement P08 and transition. Approximate first-play allowance: 8–10 minutes Play and story purpose: Assemble the branches spatially; use a clear readiness checklist before the evening advances.

- Rumor, cues, rescue, and microphone P09–P12. Approximate first-play allowance: 24–28 minutes Play and story purpose: Misinterpretations peak, an unwieldy object creates a cooperative rescue, and Jackie learns to make the whole truth public. VC03 follows the completed safe rescue and sincere conversation, before the public introduction.

- Three-door finale P13–P14 and ending. Approximate first-play allowance: 12–14 minutes Play and story purpose: Execute the learned routes, deliver dinner and the reveal, earn the written commitments, and finish on the household. VC04 follows the served meal, consented display reveal, and board delivery. All four eventual contest wins precede P14’s final commitment; the happy freeze-frame and full end credits follow the quiet household tag.

- Optional observations and conversations. Approximate first-play allowance: 6–10 minutes Play and story purpose: Audience banter, household history, and nonessential prop jokes. No mandatory collectibles.

The lower and upper allowances overlap with how much dialogue a player reads and how much optional exploration they choose. If testing regularly exceeds two hours, shorten repeated travel and dialogue before deleting causal clues. If it falls below ninety minutes, strengthen the existing physical puzzles rather than add disconnected errands. The four competitions share one concise learned-response system and replace or extend existing conversational beats; they are not four extra long minigames. Preserve the 90–120 minute first-play target, including normal practice and recovery, and validate the completed pacing rather than assuming the additions are free. Full credit viewing is skippable and replayable; disclose its viewing time separately in playtest reports.

### Event IDs for presentation and music

E00 is the noninteractive opening-credit sequence, before any gameplay. E01 is the invitation reveal, spanning P01–P02. E02 is preparation, spanning P03–P08. E03 begins when the player explicitly says the supper is ready, covering P09–P10. E04 is the hinged-display rescue in P11. E05 is the honest microphone performance in P12, ending with the shared confetti mishap. E06 is the three-door supper, display reveal, and pledge gathering in P13–P14. E07 is the completed commitment, quiet household meal and pencil/flyer tag, followed by the happy freeze-frame and full end credits. VC01–VC04 identify the embedded verbal competitions independently of E00–E07.

These supersede any earlier provisional event ordering. All are state-driven. No task depends on the real clock, music timing, reaction speed, or hearing an audio cue.

## Character availability by phase

Character movement is deterministic and introduced by a short line or visible transition. There is no wandering NPC search or appointment to miss.

- Arrival and preparation. Reliable positions and availability: Bunny starts at the living-room window, then uses L01/L02; Frankie stays by the L01 board; Stringer and Rita are in L07; Milo is in L06; Vivian waits at the L03 welcome table with her screen frame; Felix works at the L04 gate. Calling Bunny for the P05 soundcheck is an explicit, reversible escort, after which she returns home.

- Evening begins after P08. Reliable positions and availability: Bunny sets snacks in L02; Frankie checks L01 cues; Stringer returns to L07 to finish his chair labels, where Rita prepares her panel; Milo and Vivian wait in L05; Felix remains near L04. Short dialogue announces Stringer and Rita’s nearby errand, making P09 discoverable.

- Display rescue P11. Reliable positions and availability: Jackie and Felix are visibly in L04; Bunny can be called to the porch-side peg and Frankie to the courtyard-side catch. Rita waits safely beside the cart. “Set it back on the cart” restores ordinary movement and every NPC’s relevant topic.

- Microphone and finale. Reliable positions and availability: The ensemble regathers in L05 for P12’s standing welcome; Rita’s panel remains in L04. After clearing the confetti, people visibly return to L01/L02/L04 collection points to fetch the meal, drinks, display, and board before P13’s actual seating. P13 explicitly assigns each delivery and moves only its willing helpers. Anyone needed for a remaining pledge stays on the courtyard screen until P14 is complete.

A character who is briefly assisting an animation is available immediately afterward. Starting a later phase never removes a needed conversation, clue, or pickup. Where a task calls for a helper who has already moved, the relevant Talk to option performs a short visible escort rather than requiring a search. Once introduced, each contest opponent retains a clearly labeled practice/rematch topic at their current safe, accessible location until the ending starts. Busy rescue or delivery actions finish first; the journal names the current location. No contest depends on catching an unannounced appointment.

## Puzzle contract

The authored verb vocabulary is Give, Open, Close, Pick up, Look at, Talk to, Use, Push, and Pull; Walk to is the default movement action. Exact sentence examples below describe player-facing commands, not engine code. Equivalent obvious actions should be accepted where specified.

Items are never consumed by a failed attempt. Essential objects cannot be discarded, sold, eaten, or carried away by an inaccessible NPC. A completed multi-use item remains available until its last required use. Ordinary speech choices can set tone, and all respectful, truthful formulations satisfying the same practical agreement succeed. The explicit verbal competitions alone test learned semantic counters through the published response-ID contract below; they cannot replace a practical agreement or consent gate. There is no affection score that secretly locks the story.

Every puzzle has three optional hint levels: a reminder of the goal, a relevant observation, and an explicit next action. Hints are requested, not spoken automatically by the audience. Puzzles can remember completed substeps; retries do not replay a whole conversation or laugh.

## Verbal insult competitions

Confirmed scope. Four original face-to-face shouting competitions, VC01–VC04, recur within the existing evening. Jackie must eventually win all four before the final commitment and ending. Losses are recoverable social setbacks with immediate or later fair rematches, continued exploration, and retained learning. There are no weapons, sword fighting, physical attacks, injury, death, new locations, or tournament bracket. The comedy is two people standing and yelling witty lines at one another while onlookers gather.

### Encounters and narrow social stakes

VC01 — Milo, during P05 in L06. After the soundcheck and truthful loan terms are established, contest who gets the spoken promotional flourish or last word. A Jackie win gives him the concise introduction; a Milo win requires Jackie to let Milo have a limited, truthful flourish. The exact equipment credit remains “Sound equipment courtesy of Milo Pennant” in either outcome, with every factual qualifier preserved. Completing an attempt sets VC01_RESOLVED; SOUND_READY requires PA_TESTED, MILO_ROLE_AGREED, and VC01_RESOLVED together. VC01_WON is a separate eventual-win requirement.

VC02 — Vivian, during P06 at the L03 welcome table. After agreeing tonight’s scope and demonstrating the screen, contest who has the stylistic last word on the welcome presentation. A Jackie win gives him that flourish; a Vivian win means he accepts her concise styling direction. Her equipment, work and personal boundaries, future collaboration, and any romantic tone remain freely agreed and unchanged. VC02_RESOLVED joins SCREEN_BUILT and VIVIAN_SCOPE_AGREED for SCREEN_READY; VC02_WON is tracked separately.

VC03 — Felix, after P11’s safe rescue and protected sincere admissions, initially in L04. Contest whether the public account is concise and household-led or Felix’s more elaborate account of the shared rescue. Bunny, Frankie, Felix, and Jackie receive accurate credit in either outcome. Felix never gains sole credit or authority to waive safety. Never start while anyone supports the display, during concern, or over an honest admission. P11’s DISPLAY_STAGED and HELP_ACCEPTED remain physical/cooperative outcomes; VC03_RESOLVED is required to finish P12’s public introduction, while clue inspection and rehearsal remain available. VC03_WON is tracked separately.

VC04 — Mr. Stringer, in L05 during P13 after SERVED, DISPLAY_REVEALED, and physical pledge-board delivery. Contest whether the toast is concise and household-led or includes Stringer’s limited, truthful ceremonial flourish. A Jackie loss gives Stringer that spoken flourish; it never gives him control over tenancy privacy, sexuality, anyone’s consent, Rita’s authorship, repair safety, or the content of a signature. VC04_RESOLVED is needed before TOAST_READY. The contest cannot reorder SERVE, SHOW, board delivery, and TOAST. VC04_WON is tracked separately.

### Learning and equal writer contribution

The accepted repertoire is IR01–IR24: twenty-four original insult/retort pairs. Each of the eight fictional AI writer personas drafts six independent candidate pairs, then contributes exactly three accepted pairs. Keep the originating writer and any editorial adaptation in the attribution ledger. Later decks reuse accepted pairs verbatim by ID; rephrased setups are not hidden extra contributions. Neutral instructions, result lines, and concessions must not smuggle additional insult material outside the balanced repertoire.

Tier A comprises IR01–IR06, introduced through P02 household banter and VC01 practice. Tier B is IR07–IR12, introduced through P06 exchanges and VC02 practice. Tier C is IR13–IR18, introduced only after P11’s safe rescue and through VC03 practice. Tier D is IR19–IR24, introduced through P12–P13 public banter and VC04 practice. Allocate accepted pairs to those tier slots after curation, retaining three pairs per writer overall.

Learning is explicit and persistent. A heard or read setup is recorded in the notebook; a demonstrated or read retort is separately marked learned. A dialogue record counts once its text is presented, even when the player skips its sound. Unscored practice and an explicit recap remain available at every introduced contest, teach any missing pairs needed for that contest, and explain the semantic hook. Practice can be repeated without penalty, grinding, random drops, or private/offscreen knowledge. The player can inspect the notebook before choosing a response; there is no memory-speed test.

Create a five-prompt attempt deck from distinct learned pairs: VC01 draws five from A; VC02 draws two B followed by three A; VC03 draws two C followed by three from A/B; VC04 draws two D followed by three from A/B/C. Shuffle within these groups and save the exact ordered deck and seed. No pair repeats within an attempt. Scored play starts only after every pair in its eligible tiers has been taught: all six A pairs for VC01, all twelve A/B for VC02, all eighteen A/B/C for VC03, and all twenty-four for VC04. Both setup and retort must have been presented. Practice/recap fills any gaps without requiring completion of a different preparation branch, so P05 and P06 retain their flexible order. A match can end before all five prompts are used.

### Turns and social results

Both participants begin with three composure points. The opponent delivers one setup; Jackie chooses a learned retort from a readable list. The authored catalog gives each prompt an explicit accepted-response-ID set, including any genuinely valid alternatives. A correct retort costs the opponent exactly one point; a wrong retort or an explicit yield of that exchange costs Jackie exactly one. Every scored exchange changes exactly one side by one point, so the first zero and social KO occur within at most five exchanges. There are no timers, random damage, speed bonuses, hidden affection scores, string matching, live language judging, or laugh-based correctness detection.

At zero composure, the loser visibly winces and socially relents in the stated narrow matter. Jackie’s loss has the written concession described for that encounter; it is not silently treated as victory. Practice before starting has no stake. An explicit “Yield this contest” concludes a loss; skipping a line, opening a menu, muting, pausing, saving, or loading never does. Clear text states who won and which social concession applies, with no injury or humiliation-ending branch. Enact the concession immediately in the result exchange, including the winner’s short, truthful flourish, so even an immediate rematch cannot erase an unheard consequence. Latest-winner state governs only future, not-yet-spoken variants.

VC01_RESOLVED through VC04_RESOLVED latch after any concluded attempt; VC01_WON through VC04_WON latch only after Jackie wins that encounter. ALL_VC_WON is the conjunction of the four win flags and is required before P14’s final commitment sequence. A loss permits ordinary practical progress once the encounter is resolved, exploration, repertoire review, and immediate or later rematches. Missing wins are plainly listed in the notebook at the final gate. All necessary opponents and learning remain accessible, so there is no death or softlock.

Latest winner and concession variant are separate from the latched win flag. A rematch may renegotiate a future ceremonial flourish or last-word variant; it cannot rewrite a line already heard, remove a factual credit, change an agreed boundary, revoke a signed promise, undo a delivered object, or reset a completed practical puzzle. A later loss does not erase a win already earned in that saved timeline. Loading restores the saved timeline exactly rather than merging progress from another save.

### Stage presentation and audio

Use an original two-sided fighting-game-like HUD: named composure meters progress from yellow toward red, with numbers or equivalent non-color status and a central KO display. Both actors stand facing each other; onlookers gather around them, with a theatrical spotlight and dimmed surroundings. No weapon, attack, sword, or contact choreography is implied. Brief non-contact winces sell a line landing; a character-specific “ohhh” or groan sells the social KO. These use each speaker’s existing unique procedural voice profile, not a new human recording or extra MIDI role.

The crowd and lighting are presentation over the existing room. Use already present willing cast members and original collective-audience figures; do not conjure a ninth principal or private witnesses. Preserve world scale, foot anchors, foreground occlusion, required hotspots, and underlying actor positions on exit. Reduced motion can replace winces and lighting movement with still poses; captions, meters, and choices make muted play complete. The exact native HUD layout and final art still require proof.

Keep the dependable single PCM owner. Spoken setup and retort, queued audience reaction, foley, and character KO groan must be explicitly serialized or dropped according to the integrated arbitration policy; do not promise simultaneous PCM streams. A KO groan takes its authored slot before an optional audience reaction. New speech, skip, room change, menu, save, or load clears stale transient audio according to the lifecycle contract without reversing a committed exchange. The writer places generous but purposeful crowd reactions, while sincere dialogue remains protected and laughter never determines correctness.

MUS11_VERBAL_COMPETITIONS is a distinct original late-1970s Hong Kong action-cinema-inspired family, using transformed motifs from the authorized source MIDI bank. Provide opponent-colored variants for VC01–VC04, a low-density thinking/turn bed, compatible line/hit windows, and single-fire social-KO/result responses. Preserve space for the voices and audience; the rest of the score retains its accepted relaxed sparse swing. Do not quote a film score or use music to suggest physical fighting. Technical transitions use natural compatible musical windows, not forced audible bar chops.

### Persistence and production contract

Serialize learned setup/retort state; each resolved and won flag; latest winner and concession variant; attempt serial; active encounter and phase; both composure values; exact deck, seed, and cursor; pending chosen response; and committed exchange/result IDs. Correctness is keyed by stable IDs. Commit the outcome once before presentation, and distinguish consumed feedback from unresolved choice. Restoring a save must neither reshuffle a pending deck nor score the same response twice. Pause/skip/menu/save/load can cancel transient voice, wince, laugh, or KO replay while retaining the logical result and readable text.

For writing, aim for about ninety characters or fewer per visible insult or retort. The currently proven choice control supports at most 120 ASCII bytes and three lines within 260 pixels; the reader supports forty-eight columns by fourteen lines per page. The new stage layout remains to be tested. Longer necessary wording must use an explicit full-text or paged view, never truncation. Present only learned retorts, preserve their meaning in any short label, and make the full wording inspectable before commitment.

This is the authorized canonical feature contract, awaiting full script integration, original stage art, score production, and native implementation/acceptance. It does not claim the contests are already playable. The existing isolated voice lifecycle proof is supporting evidence only. Keep the fourteen physical/investigative puzzle IDs, seven rooms, eight principals, and all protected story agreements; these four embedded competitions are the explicit new mechanical extension.

## Complete puzzle specifications

### P01 Clear the Door with Help

Prerequisite and obstacle. After E00 finishes or is skipped in a new game, start on L03 with exactly the same initial state. Jackie has a covered tray of edible bread cue samples and a print packet under one arm. The self-closing front door makes his attempt to carry everything into the house awkward. Nothing is dropped or irreversibly damaged.

Clues and objects. Bunny is visible through the front window. The porch bench is clean and flat. A brightly painted wooden wedge sits on the sill with an obvious wedge-shaped door gap in view. Looking at Jackie’s tray says, “Three jobs, two hands. The arithmetic remains hostile.”

Solution and verbs. Talk to Bunny about needing a hand; she opens the window, and Give tray to Bunny secures it in the kitchen. Open front door and walk in. Alternatively, Use tray on porch bench, Open door, Use wedge with door, then Pick up tray and carry it inside. Both are valid. Pick up wedge remains available to either route; a missed wedge stays on the sill until needed in P04. The bread samples arrive safely in L02 regardless of route.

Comic result. Bunny accepts the tray with one hand while continuing to sort invitations: “You could have knocked. It is in the title.” Jackie looks toward the real audience only once. The joke is his overcomplication, not her rescuing an incompetent man every scene.

Wrong feedback. Trying to balance the tray on the doorknob: “That is a hinge, not a third roommate.” The tray remains held. The player can put it on the bench instead; do not refuse that sensible alternative.

Hints. 1: One job can be put down or handed off. 2: Bunny and the porch bench are both safe places for the tray. 3: Give the tray to Bunny through the window, then open the front door.

State and recovery. Set TRAY_SAFE and HOUSE_ENTERED. Any wedge holding the front door is freely retrievable after unloading; no automatic item teleport is needed. Door state cannot trap Jackie. Candidate laugh LAF01 fires once after the first successful competence reversal.

### P02 Read the Whole Invitation

Prerequisite and obstacle. P01. Three people think tonight has a different purpose. Jackie cannot build a coherent plan from his own invitation alone.

Clues and objects. Jackie’s copy says “Supper club: new partners welcome.” Bunny’s public copy on L01 says “Neighborhood preview: bring your appetite.” Mr. Stringer’s copy is openly displayed in L07 and says “Quiet household supper: a practical demonstration.” The same unusual cropped border appears on each. Talking to the recipients confirms the promise they heard. Stringer calls Felix’s promised repair demonstration “the inspection,” establishing a small misunderstanding of his professional role. Nobody hides their copy or needs a bribe.

Solution and verbs. Pick up the three copies with their owners’ permission; Use each with Frankie’s chalkboard. Look at the matched border to see that all came from one longer master. Give the compared copies to Milo in L06; he opens the unlocked invitation drawer and permits Jackie to take the master. Open master invitation reveals all the omitted qualifiers and the full event plan. Use master on chalkboard; select the three actual aims: feed eight, demonstrate responsible shared use, and discuss future collaborations without promising them tonight. The exact text is provided in the master, not guessed.

Result. Frankie gives Jackie a reusable grease pencil and pins a permanent checklist. All preparation tasks become actionable; L06 and L07 were already reachable to collect the invitation evidence. Milo admits, “I made the invitations more focused.” Bunny: “You focused each one on a different evening.”

Wrong feedback. Accusing a recipient of lying produces their complete, accurate copy and does not damage the relationship. Trying to write “romantic mixer” or “property sale” on the plan highlights the line contradicting it and leaves the board editable.

Hints. 1: Compare what people were actually sent. 2: Their invitations share a cropped border. 3: Put all three on the chalkboard, show them to Milo, and open his complete master.

State and recovery. INVITATIONS_COMPARED then PLAN_AGREED. Copies become pinned records rather than cluttering inventory; they can always be re-read. Keep the master as a reusable flat card/offcut supply for labeling; it is not destroyed by later uses.

### P03 Put Rita’s Name on It

Prerequisite and obstacle. P02. Rita will lend her distinctive ceramic service, but the borrowed carrier rattles dangerously and Milo has copied a one-letter printing error onto the credit slate, which calls it “Mr. Stringer’s collection.” Rita points out that the master had “Mrs.”; the lost letter now credits the wrong Stringer, and she would prefer her own name anyway. She needs both safe handling and visible authorship, not an apology alone.

Clues and objects. Look at the carrier shows empty fitted slots and a faded drawing of folded cloth between plates. L02 has a clean tea towel. Rita’s signature is visible on every plate and on her ceramics-class card. The slate has a wipe-clean face.

Solution and verbs. Pick up clean towel in L02. Use towel with carrier to pad its slots. Use grease pencil with credit slate and select the visibly evidenced wording “Ceramic service by Rita Stringer.” Give finished slate to Rita; she checks it, returns it for display, and releases the padded carrier plus three small reusable ceramic sample tiles. A clean spare napkin from the same linen drawer is an accepted padding alternative.

Result. Rita volunteers that she has a larger ceramic house-number panel to reveal later. Looking at its folded display by the wall shows the large wing-release catch and its inward-pointing arrows; the ceramic face remains covered, preserving the surprise. Bunny and Frankie agree to protect the surprise until Rita chooses to present it. The secret is benevolent and never used to make someone think a romantic betrayal has occurred.

Wrong feedback. Newspaper/master-invitation scraps alone: “That will stop a draft, not two plates kissing.” Rita demonstrates the clatter without breaking anything. A generic “Mrs. Stringer” credit: “I have a perfectly serviceable first name.” The slate remains editable.

Hints. 1: Solve both transport and credit. 2: The carrier drawing shows cloth, and her signature supplies the exact name. 3: Pad the carrier with the kitchen towel and write Rita Stringer on the slate.

State and recovery. CERAMICS_READY. Carrier is parked at the kitchen pass, not carried indefinitely. Its towel is recoverable once plates are laid out in P08. Sample tiles must remain available for P10. No breakage, replacement purchase, or permanently offended Rita state.

### P04 Prove Felix’s Gate Repair

Prerequisite and obstacle. P02. Felix’s newly rehung side gate fails its gentle self-closing demonstration. He is reluctant to sign off his own work until its cause is understood; he is not an inspector or an additional landlord. When Jackie repeats Stringer’s phrase “the inspection,” Felix corrects it: “Repair check. The only thing I’m judging is that gate.”

Clues and objects. Look at the gate shows fresh, aligned hinges and a strip of welcome bunting looped around the moving latch arm. A nearby fixed decoration hook is labeled with a tiny pennant symbol matching the bunting. The gate’s proper hold-open peg is visibly stowed on its frame. Felix explains that the wedge can temporarily hold the leaf while both hands are free.

Solution and verbs. Open gate, Use wooden wedge with gate, Pull bunting free of latch, and Use bunting on fixed decoration hook. Pick up wedge to release the gate. Push gate gently to demonstrate its unobstructed closing cycle. Felix accepts the test, supplies a drawn circulation plan, and makes the permanent hold-open peg usable for later carrying work.

Result. Jackie’s publicity decoration, rather than Felix’s craftsmanship, caused the problem. Felix: “An excellent gate. A deeply ambitious ribbon.” Jackie credits him on the plan.

Wrong feedback. Pulling the hinge or forcing the latch is refused with a close-up of the ribbon caught in the moving arm. Leaving the wedge in place cannot pass a self-closing test: Felix says exactly why. It can still remain open for navigation.

Hints. 1: Something added after the repair interferes with the gate. 2: The bunting belongs on a stationary hook. 3: Wedge the gate open, move the bunting, remove the wedge, and test the gate.

State and recovery. GATE_TESTED and HOLD_OPEN_AVAILABLE. All moves are reversible. The wedge remains available. Gate never damages people or inventory. A successful test is permanent even if the gate is later propped for transport.

### P05 Give Milo an Honest Spotlight

Prerequisite and obstacle. P02. Milo offers a grand-sounding PA loan, but his demonstration plays only his own taped slogan, while the loudspeaker points away from the house. His salesmanship is outrunning what the equipment is doing.

Clues and objects. The large input selector is labeled TAPE and MIC, with corresponding simple icons. The speaker has an obvious swivel handle and front grille. The microphone cable and MIC socket have matching three-dot symbols. Milo’s boastful tape is wholly original: “Milo Pennant presents tomorrow, slightly ahead of schedule.” A listener outside the speaker’s beam can hear music but not clear speech.

Solution and verbs. Use microphone with matching socket, Use selector to choose MIC, and Push speaker’s swivel handle to face the marked listener position. Invite Bunny to that position and Talk to microphone to test an ordinary complete sentence. Alternatively, Walk to the garage’s scenic boundary, Talk to the studio audience about testing the sound, return, and perform the same test toward their marked listening position. Their response reports clarity, with matching captions and a visual response card. Then offer the accurate credit “Sound equipment courtesy of Milo Pennant” on the slate beside the kit. He accepts the specific greeter role and the unchanged accurate equipment credit. Resolve VC01’s separate spoken-flourish competition, by either outcome, then borrow the working PA and handcart; a Jackie loss changes only the social flourish, and a later rematch remains available.

Result. A plain sentence finally interrupts the overwhelming promotional loop. Milo discovers that being useful gets him more genuine attention than his tape did. The audience alternative is useful but never required to hear sound.

Wrong feedback. Wrong socket does not fit; a visible icon highlights why. Correct wiring with a backward speaker produces a specific direction report, not “try again.” The kit is not loaned merely for flattering dialogue; the practical soundcheck must pass.

Hints. 1: Check the source and where the sound is going. 2: The selector still says TAPE and the grille faces away from the listener. 3: Select MIC, connect the matching cable, turn the grille toward Bunny or the invited audience, and test a full sentence. If the practical test is complete, practice and resolve VC01; its result never alters the equipment credit.

State and recovery. PA_TESTED, MILO_ROLE_AGREED, and VC01_RESOLVED together set SOUND_READY; VC01_WON is separately needed before P14. Loan kit is moved automatically to L05 with Jackie’s on-screen agreement; handcart stays usable in L06 or its clearly marked parking spot. No cable is consumed. AUD_SOUNDTEST and LAF05 are one-time success cues.

### P06 Agree Vivian’s Role

Prerequisite and obstacle. P02. At the L03 welcome table, Vivian has brought a folding screen frame but no intact cloth panels. She is willing to style the evening if Jackie states what he is actually offering, returns her equipment, and demonstrates a workable sightline. Neither attraction nor a date purchases her cooperation.

Clues and objects. Her frame carries an assembly drawing: fabric over the upper rail, clipped at the marked pairs of dots, with the lower edge clear of feet. L04 has large laundry clips. Frankie can point out a clean spare sheet in L02 and confirms it is available. Vivian places two visible cardboard figures on her sample layout: an arriving visitor and Rita’s surprise display.

Solution and verbs. Ask Vivian to collaborate on tonight’s styling and discuss any future work after the trial. Jackie can express professional, friendly, or cautiously romantic interest without changing the puzzle reward; promises of a date are never necessary. Pick up clean sheet and clips, Use sheet with frame, and Use clips at the marked rail. Push the assembled miniature screen token on Vivian’s sample layout until the arriving visitor cannot see the display while the kitchen hatch remains visible. Two clearly drawn sightlines update as the token moves. Resolve VC02’s separate styling-last-word competition after the agreed scope and successful mock-up. Either outcome permits Vivian to lend the completed screen and mark its correct full-size courtyard location; a Jackie loss accepts her stylistic flourish without changing any work or personal boundary.

Glamorous temptation. Vivian mentions an industry mixer she could take Jackie to that evening. Jackie can acknowledge its appeal and suggest another occasion or after the household has finished. The game does not pretend abandoning the promised supper is a viable required solution. She respects that he keeps his actual commitment.

Wrong feedback. Tying cloth around the lower legs visibly blocks feet and she explains the issue. A screen placement that hides the kitchen blocks the highlighted service sightline. Jackie can immediately move it. Flirting alone returns to the concrete equipment and scope question.

Hints. 1: Make the screen usable and hide only the surprise. 2: Follow the frame’s clip marks and the two visible sightlines. 3: Put the sheet over the upper rail, clip its marked points, and place the screen across the display sightline without crossing the hatch sightline. Once scope and sightlines are agreed, practice and resolve VC02; no romantic response buys success.

State and recovery. SCREEN_BUILT, VIVIAN_SCOPE_AGREED, and VC02_RESOLVED produce SCREEN_READY; VC02_WON is separately needed before P14. Clips stay attached and are never separately needed later. Failed arrangements do not tear fabric or consume clips. The assembled screen is moved to L05 after the approved mock-up.

### P07 Cook the Household Special

Prerequisite and obstacle. P02. Jackie’s courtyard hotpot recipe makes six full suppers; tonight there are eight contributors. The alternative tasting-size method is written in the recipe margin, so success requires reading the actual plan rather than guessing a culinary fact.

Clues and objects. The recipe says: “Eight tasting bowls: add stock to the marked jug line. Base first, vegetables second; finish with herbs after turning off the heat.” The kitchen has a prepared bean-and-tomato base, a vegetable bowl, a stock bottle, a jug with a large eight-bowl mark, an herb sachet, and a lidded pot. The herb sachet repeats “finish off the heat.”

Solution and verbs. Use base with pot; Use stock with jug and select the prominently marked eight-bowl level; Use measured jug with pot; Use vegetables with pot; Use stove. A short cooking montage reaches the next state immediately, without a timer. Use stove to turn it off, then Use herb sachet with pot and Close lid. Accept combining the base and measured stock in either order; the important distinction is cooked components before the fresh finish. All eight contributors, including Jackie, receive appropriate tasting portions, not eight magically full meals from six portions.

Comic beat. Jackie’s ordinary onion tears make Bunny think he is moved by Rita’s generosity. He can admit the onion first and add sincerely that the generosity matters too. No illness, drug, allergy, or deliberate food tampering gag.

Wrong feedback. Herbs over active heat: “The little packet is making an unusually specific request.” No ingredient is lost. Too-small portion selection highlights the guest count and the recipe annotation. Forgotten lid gets a clear transport reminder.

Hints. 1: Count people, then read the recipe’s margin. 2: Eight tasting bowls require the marked stock measure and herbs off the heat. 3: Add base, eight-bowl stock measure and vegetables; cook; turn off heat; add herbs and lid.

State and recovery. FOOD_READY. Ingredients are treated as refillable pantry supplies until the dish is complete. The lidded pot waits in the kitchen until P13. No burning, food spoilage, hunger timer, or toxic combination exists. Optional LAF07 follows the first onion misunderstanding, never the sincere follow-up.

### P08 Fit Three Agendas into One Courtyard

Prerequisites and obstacle. P03–P07 complete. The courtyard cannot accommodate a buffet, PA, concealed display, and through-traffic if all are placed by the most impressive doorway.

Clues and objects. Felix’s circulation plan marks the gate-to-house lane with floor chevrons. Vivian’s sightline plan specifies which side conceals the display. The hatch has a matching tray icon; the inward-facing speaker spot has a sound icon; the display alcove has a panel-shaped footprint. All information has already been demonstrated practically.

Solution and verbs. Use carrier with the buffet position below the hatch; Use PA at the wall position, facing into the courtyard; Use screen at the marked alcove, leaving the gate lane clear. Move the small serving table with Push/Pull into the hatch footprint. Place Rita’s credit slate at the buffet. A plan overlay shows the three final conditions. Once all are true, Talk to Frankie and choose “We’re ready to start.” She reads the short checklist before a confirmable phase transition.

Result. The space really works, briefly. Housemates have agreed to keep Rita’s ceramic panel concealed until after the meal. Bunny’s invitations now make sense as a single event rather than three competing parties.

Wrong feedback. Every placement is reversible and states a spatial consequence: blocked gate, hidden hatch, sound aimed at neighbor, or display visible too early. There are no pixel-perfect coordinates. Three generous named positions plus the visibly prohibited lane are enough.

Hints. 1: Each object needs a position and a clear route. 2: Match the plan’s tray, sound, and panel shapes; keep chevrons empty. 3: Buffet under hatch; speaker facing house; screened display alcove; gate lane clear.

State and recovery. LAYOUT_READY, then EVENING_STARTED only on explicit readiness. The confirmation explains that people move to the evening’s positions; no essential area or item becomes permanently inaccessible. Autosave before the transition. The towel is returned to the kitchen linen hook after the plates are unpacked.

### P09 Ask What Is Actually Leaving

Prerequisite and obstacle. P08. At the side of the conservatory, Jackie hears Stringer say “all three out of the house” and “finished by tomorrow,” then sees a tag reading “HOUSE LOT — THREE.” It sounds like the tenants are about to be removed. It actually concerns three unloved chairs whose removal will give Rita room for her ceramics class.

Clues and objects. The label hangs from a chair, not a tenancy file. The other two chairs carry matching tags. Walking to the conservatory’s front gives the complete conversational context; the player can also simply ask Stringer what the phrase means. The game must honor that natural direct question without demanding an unnecessary object ritual.

Solution and verbs. Look at tagged chairs, or Talk to Stringer and select the precise question “What are the three things leaving?” He explains the chairs. Ask what would make tonight a successful household demonstration, using Frankie’s plan. He agrees to written conduct-based terms: care for the house, keep the agreed guest/noise arrangements, and carry out the promised repair. He gives Jackie an unsigned plain-language renewal-and-repair card for the later toast.

Result. The supposed threat dissolves, but the meaningful goal remains: make tonight work and obtain an actual commitment. Rita and Stringer both want her class space, although each thinks the other dislikes the idea. Jackie can explicitly connect that shared wish.

Wrong feedback. “You’re throwing us out tonight!” receives an immediate correction and points at the chairs; it never locks a persuasion state. An attempt to burn or hide the tag is refused because the chair itself is not the problem.

Hints. 1: Identify the subject of the overheard sentence. 2: There are exactly three tagged chairs. 3: Ask Stringer what the three things leaving actually are, then discuss the written plan.

State and recovery. RUMOR_CLEARED and TERMS_CARD_AVAILABLE. This is deliberately a short knowledge puzzle amid longer physical puzzles. Looking and direct questioning are both valid. No real-world legal guarantee or binding contract simulation is implied.

### P10 Replace the Edible Service Cues

Prerequisite and obstacle. P08; independent of P09. Bunny has innocently offered the bread cue samples as welcome snacks after finding them on the kitchen snack tray. Jackie’s sequence reminders, “SERVE,” “SHOW,” and “TOAST,” have been eaten. No paper, metal, or non-food substance was consumed.

Clues and objects. The full event order remains legible on Frankie’s chalkboard: feed the contributors; let Rita reveal her panel; then make and record commitments. Rita’s three ceramic sample tiles have wipe-clean faces. The grease pencil works on the credit slate and the tiles. A cue rack by the microphone has three built-in spring clips, each sized for either a sample tile or a flat card. These are part of the rack, not the laundry clips already attached to the screen.

Solution and verbs. Pick up the sample tiles, Use grease pencil on each and select the three words from the original plan, then Use labeled tiles with the rack in SERVE, SHOW, TOAST order. The labels appear as both words and distinct icons. Ask Bunny to reserve future bread samples for eating, not scheduling.

Result. Rita instantly recognizes her own distinctive tile shapes, and Jackie openly credits the substitution instead of pretending he made them. Her real craft becomes practical help. “My first durable menu,” he says; Rita replies, “Try not to toast the ceramics.”

Wrong feedback. Blank or reversed tiles prompt the character to describe what instruction would come next and why it is premature. The player can remove and rewrite any tile without consumption. Paper cues are an accepted alternate if clipped to the same rack using the available master-invitation card; ceramic cues remain the canonical visual solution, not an arbitrary material restriction.

Hints. 1: Recover the order, then use something nobody will eat. 2: The chalkboard still has the sequence and the sample tiles wipe clean. 3: Write SERVE, SHOW, TOAST and put them in that order on the cue rack.

State and recovery. CUES_RESTORED. The rack remains readable and editable through the finale. The three words and icons appear in the notebook. No dependency on remembering an earlier unrepeatable line.

### P11 Move the Oversized Display Together

Prerequisites and obstacle. P09 and P10. Rita’s ceramic panel is safely fastened to a three-wing folding display. After Jackie and Felix lift it from Milo’s nearby padded handcart to negotiate the side passage’s narrow corner, an unsecured wing swings open and catches the narrow passage beside the gate. Both men are supporting the weight. The panel itself is not cracking and nobody is injured, but they cannot complete the move alone in that posture.

Clues and objects. The folding wing has a large release marked by two arrows pointing inward; it was visible on the earlier display. Felix’s gate peg is reachable from the other side. Bunny sees the control clearly from the porch; Frankie can reach the wing latch from the courtyard. Jackie’s first attempt to conceal the situation by calling it a “moving exhibit” is visibly absurd.

Solution and verbs. Talk to Bunny: ask her to engage the gate’s proper hold-open peg. Talk to Frankie: ask her to release the marked wing catch. Then Pull display handle with Felix; the wings fold onto their padded stops and the pair lower the folded display safely onto Milo’s handcart. Park it in the side passage’s out-of-view staging pocket, ready for Rita’s chosen reveal. This is an existing recess hidden by the house wall, not a second screen item. The order of the two helper requests is free. If the player already engaged the peg before carrying, that substep is satisfied rather than reset.

Human beat. Confined together behind their enormous display, Felix admits that he wants his repair to be trusted, not described as a trick. Jackie admits he keeps promising to be everybody’s solution. Bunny and Frankie initially hurry over because his muffled “stuck” sounds worse than it is; then they diagnose the actual problem. The player earns the rescue by asking clearly and applying what was learned.

Wrong feedback and recovery. Trying to push harder produces a harmless flex and an explicit “fold, don’t force” clue. Jackie can always say “Set it back on the cart,” reverting to the start of this puzzle and restoring free movement. No walking, saving, or menu restriction traps the player. Do not require reactions while anyone holds the display.

Hints. 1: Stop trying to supply every pair of hands yourself. 2: The gate peg and wing catch are on opposite sides. 3: Ask Bunny to peg the gate, ask Frankie to release the wing catch, then pull the display’s handle with Felix.

State. DISPLAY_STAGED and HELP_ACCEPTED. The complete unfolded silhouette briefly resembles a formal parade float before folding neatly; LAF11 is a single earned physical-duet reaction. No laugh plays over the honest conversation or the roommates’ initial concern. Only after safe staging and the sincere beat are complete does VC03 become available. Its shared-credit social account cannot change the rescue flags or omit Bunny and Frankie’s help.

### P12 Tell the Truth into the Microphone

Prerequisite and obstacle. P11. Vivian has rehung the cue rack neatly along the courtyard’s set-edge rail beside the microphone, inadvertently turning the words toward the studio audience and leaving only decorative backs visible to Jackie. Stringer has also overheard the fragment “we’ve got him right where we want him” from the display planning and suspects that the supper is a trap to make him agree to anything.

Clues and objects. Look at the rack from the courtyard shows three blank backs, arrows on its rotating rail, and a small diagram reading “Release catch on audience side, then rotate.” The catch is physically on the far side of the tall rail and cannot be reached from the set. The visible scenic edge leads to audience seating. The audience can plainly see the words on the public side. The original chalkboard and notebook still explain SERVE, SHOW, TOAST.

Solution and verbs. Walk past the scenic boundary; Talk to the audience and ask what the physical cards say. They report the visible order only, in captions as well as voice. Jackie can Look at the rack from this viewpoint himself as an equally valid action. Pull the clearly visible swivel-release catch on this audience-facing side; it stays released without anyone holding it. Return to the set. Pull the rack’s rotating handle to face the words inward, then Use the cards to restore the known order if the decorative rehanging has swapped the first two. Use microphone and choose the complete, truthful introduction: tonight is a meal and collaboration trial; all contributors are named; “partners” has not promised anyone a date or a new job. The player can rehearse it to the willing audience first, but performance approval is not a hidden skill check. Finish VC03’s shared-rescue-account competition before committing this public introduction. Its winner affects only the truthful flourish; clue inspection, cue-rack repair, and rehearsal never require winning or resolving it first.

Information reversal. Jackie deliberately supplies the full innocuous sentence into the working microphone: “We’ve got him right where we want him: in the front row for Rita’s work.” This corrects the earlier overheard fragment in public instead of inventing another cover story. Stringer unexpectedly likes the clear, modest welcome more than Milo’s inflated promotion.

Shared mess. As everybody finally stops posing, Milo attempts a ceremonial flourish with his reusable invitation-confetti tube. It releases a cloud of harmless paper offcuts onto every carefully presented outfit, including his own. It is one authored visual flourish, not a food fight or a player-controlled projectile mechanic. Everyone helps clear the working surface. This has been a standing welcome, not the seating: afterward the contributors visibly return to the house and side-passage collection points to fetch drinks, dinner, the display, and the pledge board. Their next trip back is the P13 delivery-and-seating problem. Rita’s ceramic panel remains concealed and undamaged.

Wrong feedback. Trying to rotate the rack from the set before releasing it produces a safe click and highlights the diagram showing the far-side catch; no character pretends Jackie lacks knowledge he could otherwise obtain. Talking into the unplugged or tape-selected PA invokes the already learned P05 symbols; previous wiring is retained unless the player deliberately changed it. An incomplete or boastful introduction is gently questioned with the missing qualifier, and choices remain open. There is no public humiliation fail ending.

Hints. 1: Somebody else has the useful view of the cue rack. 2: The audience side has both the printed faces and the swivel-release catch. 3: Step beyond the set edge, read or ask about the cards, pull the far-side catch, return, rotate the rail, and restore SERVE, SHOW, TOAST before making the complete introduction. If the introduction is otherwise ready, the notebook points to VC03 practice and its recoverable social result with Felix.

State and recovery. AUD_CUE_VIEW, CUE_RAIL_RELEASED, CUE_RACK_FACING_HOST, and INTRODUCTION_CLEAR. Audience view does not reveal private motives, answer the order puzzle, or bypass the preparation. LAF12 follows the shared confetti flourish; no laughter accompanies the boundary-respecting explanation of what the evening does and does not promise. INTRODUCTION_CLEAR also requires VC03_RESOLVED, while VC03_WON remains the separate eventual-win goal.

### P13 Send Everything through the Right Door

Prerequisite and obstacle. P12. Returning from those collection points, everybody enthusiastically tries to help through the same house doorway and rear arch. Jackie has to stage three deliveries in the previously agreed SERVE, SHOW, TOAST order. This is the playable farce climax, not a long noninteractive speech.

The visible control. The cue rack becomes the scene’s three-step command surface. Selecting a cue previews the relevant load and three generous route hotspots. The preview displays width, destination, and occupied-lane markers. Every attempted route is a turn; there is no countdown. Talk to a helper repeats what they are carrying and where they want to end up.

Step one, SERVE. Give the guest-program card to Milo and ask him to greet from the front door; he directs the other waiting contributors through the living room’s rear arch to their courtyard places, then takes his own place after the queue clears. Jackie and Bunny Use lidded pot with the kitchen hatch, directly onto the already placed buffet. Frankie clears the buffet surface and opens the bowls. The pot never travels through the audience seating. The player then Pulls the SERVE cue to confirm the food is on the table.

Step two, SHOW. Talk to Rita to obtain her explicit ready-to-reveal cue. Ask Felix and Vivian to bring the folded display on the handcart through the side gate, held by the already tested peg. Use screen’s pull tab to open the viewing side only after the display is in its footprint. Rita unveils the original ceramic house-number panel: three differently colored small doors around one shared table, a tribute to the tenants rather than an imitation of any television prop. Jackie Pulls the SHOW cue after her presentation.

Step three, TOAST. Give the blank pledge board to Frankie, who brings it from L01 through the ordinary front/rear doorway route once the arrival queue is clear. With SERVED, DISPLAY_REVEALED, and the board physically delivered, practice and resolve VC04’s narrow toast-flourish competition with Stringer. Then call everybody’s attention using the correctly oriented microphone and Pull the TOAST cue. Neither result changes the factual pledges or Rita’s consent. Stringer stays voluntarily because Rita has asked him to see her work and he has seen the evening function; no one locks him in, steals his keys, or forges a signature.

Fairness and failure. A display cannot fit through the narrow hatch; its drawn width and the hatch opening make this obvious before selection. Sending the pot the long way meets the stationary guest queue, prompts “The hatch puts us straight over the buffet,” and resets only that delivery. Showing the panel before serving prompts Rita to preserve her agreed reveal order; no penalty. Sending people through the hatch prompts “Not that kind of social climbing,” then leaves them at their start positions. At most one first-time comic wrong-route animation gets LAF13; repeated retries are quiet.

Hints. 1: Three loads, three openings, three established cues. 2: Dinner belongs at the hatch; the wide display needs the side gate; people use the house door. 3: Seat people and serve through the hatch, bring Rita’s display through the pegged side gate and reveal it with permission, then bring the board through the clear house doorway, resolve VC04’s toast-flourish competition, and cue the toast.

State and recovery. SERVED and DISPLAY_REVEALED advance in that order; after the board is physically delivered, VC04_RESOLVED permits TOAST_READY. VC04_WON is separately required before P14. Completed deliveries remain complete. Undoing an optional furniture movement before a delivery is allowed; the overlay tells the player exactly which prerequisite became false. After a delivery, occupied furniture is protected from disruptive moves with an ordinary in-world explanation. Autosave at each completed cue.

### P14 Put the Promises in Writing

Prerequisite and obstacle. P13 and ALL_VC_WON, meaning Jackie has won VC01, VC02, VC03, and VC04 at least once in this saved timeline. The notebook clearly lists any missing win and the safe practice/rematch location; ordinary exploration remains open until these are complete. A successful party could still end as another collection of vague claims. Frankie asks Jackie to match concrete responsibilities to the people who actually agreed to them, and Stringer must be asked for his own promised contribution.

Clues and objects. The permanent notebook records the explicit promises. Each person’s pledge card uses a distinct portrait/name and one short practical commitment: Jackie cooking and kitchen cleanup; Bunny accurate invitations and guest count; Frankie shared plan and written terms; Milo loaned sound and agreed volume; Vivian tonight’s styling and a later conversation, with no guaranteed booking; Rita credited service and display; Felix the tested gate and scheduled repair work; Stringer renewal commitment and funding/scheduling the agreed repair. The repair date is an in-fiction selected date on the card, not a real calendar action.

Solution and verbs. Give each of the seven nonplayer cards to its named contributor for approval. Use Jackie’s own card with the board and confirm his cooking-and-cleanup promise. Cards with unrelated promises are returned with a specific correction. Use the other approved cards on the board. Give Stringer the renewal-and-repair card from P09 and select the concrete conduct-based terms already discussed. He signs and pins it in front of the others. Finally, Give the grease pencil to Frankie so she can add the agreed date and read it back; she returns it. This last handoff completes the object’s progression from correcting publicity to recording an actual promise.

Alternative tones. Jackie can be warmly sincere or dryly funny in his toast. Romance choice from P06 colors Vivian’s closing line, not the signature or ending. Stringer’s remaining assumptions about Jackie are neither confirmed nor disproved. The important change is an explicit standard that private relationships are not the basis for the household’s treatment.

Ending. The event settles into an unposed meal. The roommates notice that Rita’s little three-door house resembles their home despite none of its objects being exact. The place matters because they have made room for one another. In the final quiet living-room tag, Milo offers a new flyer: “Mutual Benefit Supper.” All three housemates reach for the grease pencil. Jackie turns to the studio audience: “Put ‘It’s a meal’ underneath. In very large letters.” After this pencil/flyer punchline, end on a happy household freeze-frame with an original or cleared studio-audience laugh, cheer, and applause, followed by the full television-style end-credit sequence. Preserve the preceding quiet meal and emotional beat without a laugh over them. The extended household-theme reprise carries the credits after the celebration.

Hints. 1: Record only what people actually agreed to do. 2: The notebook and portrait cards pair each promise with its owner. 3: Get the eight named cards approved, pin them, ask Stringer to sign the P09 terms, and hand Frankie the pencil to date them. Before the final commitment, finish any of the four clearly listed contest wins using practice and rematches; no win substitutes for an approved promise.

State and recovery. ALL_VC_WON permits the final commitment; the genuinely approved promises set COMMITMENTS_SIGNED and GAME_COMPLETE before the finale presentation begins. No forged, stolen, coerced, or blackmailed signature is accepted. A mistaken card never cancels an earlier approval. Completion may offer return to the pre-finale save for optional observations, clearly labeled as revisiting the evening rather than changing the ending. Credit skip or replay never grants, revokes, or repeats a promise, contest result, or completion reward.

### Happy freeze frame and full end credits

After legitimate completion and the final pencil/flyer tag, hold an original happy ensemble freeze-frame, play a clearly cleared laugh/cheer/applause celebration, then run a complete fictional television-production credit sequence. Create an original show-within-the-game studio and crew with playful, plausible job titles and original names. The fictional framing must be clear; no invented person is represented as actual production labor, and no real studio or performer endorsement is implied.

Interweave clearly truthful actual credits for Shael Riley’s creation and creative direction, with additional writing, design, music, and production role wording grounded in his actual contribution and the final production record. Credit dot/OpenAI AI assistance accurately rather than implying an actual human crew. The in-universe composer wink is exactly “Music by Haru Suno,” an original fictional persona. This replaces the plain Suno title line; preserve the true user-provided Suno source-generation provenance in the production record and any required acknowledgment without suggesting that Haru is a real person.

Individually credit the fictional AI writers’ room: Ned Still (laconic head), Quinn Keyes (interactive assistant head), Roxy Bellows (club), Perry Quibble (social friction), Kit Glitch (meta), Bea Bunch (ensemble), Ada Branch (adventure), and Mira Aside (outsider). Identify them as fictional AI writer personas, never as the real people who inspired a comic approach. Their individual insult-pair contributions remain traceable in the equal-contribution ledger.

Include all actual asset, tool, runtime, soundfont, and license acknowledgments required for what ships, selected from the final shipped-asset manifest. Keep full acknowledgments readable and accessible, including title, author, source and license URLs, and adaptation details where required for CC BY material. Audition-only material is not automatically a shipped credit. Preserve the existing source-bank authorization and all original-art/television-asset constraints. The complete script supplies the full original fictional roll and final truthful wording; production checks it against the actual manifest before release.

The end sequence must support pause, skip, readable text, muted completion, and replay through an appropriate menu entry, preserving the invoking session and completion state. The freeze-frame celebration and credits are presentation after GAME_COMPLETE, not another puzzle or timed input. The audience celebration uses one cleared composite or serial cues on the existing PCM lane, without a new simultaneous-stream assumption. This is a newly required presentation contract; the opening-credit prototype does not establish that a full ending roll or its replay is implemented.

## Dependency graph and shortest reliable walkthrough

![Embedded source image 1](embedded-images/image9.png)

P01 → P02 → five preparation branches P03, P04, P05, P06, P07 → P08. P03–P07 can be completed in any order, with previously found common props allowed to satisfy later steps. P08 → P09 and P10 in either order. Both → P11 → P12 → P13 → P14. The diagram shows the fourteen-puzzle physical/investigative spine. Embedded social resolution gates are VC01→P05, VC02→P06, VC03→P12 after safe P11, and VC04→P13 after the food/reveal/board prerequisites. The additional global gate is VC01_WON AND VC02_WON AND VC03_WON AND VC04_WON → P14’s final commitment; losses leave accessible rematches.

Cross-branch object links: P01 wedge is reused in P04; P02 grease pencil is reused in P03, P05, P10, and P14; P03 tiles support the canonical P10 solution; P04 peg returns in P11 and P13; P05 cart returns in P11 and P13; P06 screen returns in P08 and P13; P07 food is delivered only in P13; P09 terms card is signed in P14. The paper-cue alternate in P10 prevents an arbitrary single-material bottleneck without changing the dependency spine.

- Secure the tray with Bunny or the bench, enter the house, and take the wedge from the porch.

- Compare the three invitation copies on the chalkboard, show Milo, and read the complete master; agree the actual plan.

- Pad Rita’s carrier with clean cloth and correct the credit slate using the grease pencil. Receive the service and sample tiles.

- Wedge the side gate, move bunting from moving latch to fixed hook, remove wedge, and demonstrate the repaired gate. Note its hold-open peg.

- Plug Milo’s microphone into its matching socket, select MIC, aim the speaker at Bunny or the participating audience, test speech, and agree the truthful equipment credit. Borrow the cart and PA. Practice and win VC01’s spoken-flourish contest without changing that factual credit.

- State Vivian’s honest role; assemble sheet, frame, and clips according to the diagram; satisfy the two sightlines on her small plan. Practice and win VC02’s narrow styling-last-word contest.

- Read the eight-tasting-bowl recipe annotation; measure stock, assemble and cook base/vegetables, turn off heat, add herbs, and lid the pot.

- Put buffet at hatch, PA facing inward, and screened display footprint in the alcove; clear the gate lane. Tell Frankie the checklist is ready.

- Clarify the three-chair rumor directly or inspect the tagged chairs; agree the concrete terms and take the unsigned card.

- Replace the eaten bread cues with labeled ceramic tiles or clipped card; set SERVE, SHOW, TOAST.

- Ask Bunny to peg the gate and Frankie to release the display wing; fold and safely lower the panel onto the cart with Felix. After safety and sincere dialogue, practice and win VC03; accurately credit everyone’s rescue help.

- Step off the visible set to obtain the cue rack’s audience-side view and pull its far-side release catch; return, rotate/reorder the cards, and make the complete introduction into the working microphone.

- Seat the contributors through the house door, serve the pot through the hatch, bring the display through the side gate, reveal it with Rita, bring the board, practice and win VC04’s narrow toast-flourish contest, and call the toast.

- Approve and pin the eight named promises; give Stringer the agreed card, obtain his signature, and let Frankie date and read it back. Confirm all four contest wins before starting this final commitment, then watch or skip the happy freeze-frame and full end credits.

## Inventory and object lifecycle

- Covered bread-sample tray. Starts or becomes available: Jackie, P01 Required uses: Door tutorial; later source of edible cues Exhaustion and recovery: Safely reaches L02 by either solution. Bread is eaten only at scripted P10; the sequence survives on the board.

- Wooden wedge. Starts or becomes available: Porch sill, P01 Required uses: Optional tutorial; gate hold during P04 Exhaustion and recovery: Never consumed. Remains at last visible door until picked up. Proper gate peg replaces its transport role.

- Three invitation copies and master. Starts or becomes available: P02, L01/L07/L06 Required uses: Reconstruct event; permanent reference; optional card-cue material Exhaustion and recovery: Pinned copies can be read forever. Master supply is sufficient for the one permitted paper-cue alternative.

- Grease pencil. Starts or becomes available: Frankie after P02 Required uses: Rita credit, Milo credit, cue tiles, final commitments Exhaustion and recovery: Unlimited writing, always returned after an NPC uses it.

- Clean towel or napkin. Starts or becomes available: L02 linen drawer Required uses: Pad ceramic carrier; optional spill-cleanup gag Exhaustion and recovery: Returned to linen hook after P08 unpacking. No later critical task depends on a dirty or discarded cloth.

- Padded ceramic carrier and service. Starts or becomes available: Rita after P03 Required uses: Establish buffet P08; serve P13 Exhaustion and recovery: Carried as one object until stationed; plates never break.

- Three ceramic sample tiles. Starts or becomes available: Rita after P03 Required uses: Canonical P10 cue solution Exhaustion and recovery: Rewritable, removable, cannot be eaten or lost.

- Credit slate. Starts or becomes available: Rita P03; equipment slate at Milo P05 Required uses: Authorship and accurate loan credit Exhaustion and recovery: In-world fixed objects once displayed; can be corrected without loss.

- Gate peg and circulation plan. Starts or becomes available: Felix after P04 Required uses: P08 layout, P11 rescue, P13 delivery Exhaustion and recovery: Peg is a tethered fixture, never pocketable or lost. Plan persists in notebook and on board.

- PA and microphone. Starts or becomes available: Milo after P05 Required uses: Preparation, P12 explanation, P13 cues Exhaustion and recovery: Bundled rig moves by agreed scene transition; cable cannot become a hidden missing item.

- Handcart. Starts or becomes available: Milo after P05 Required uses: P11 display, P13 delivery Exhaustion and recovery: Visible parking spot; returns automatically after a completed delivery, never vanishes.

- Sheet, clips, and screen frame. Starts or becomes available: L02/L04/Vivian in P06 Required uses: Screen construction, P08 concealment, P13 reveal Exhaustion and recovery: Combined into one screen; parts do not need to be dismantled again.

- Recipe, jug, pantry ingredients, pot. Starts or becomes available: L02, P07 Required uses: Food preparation, P13 service Exhaustion and recovery: Ingredients refill until completed; pot cannot burn/spoil; recipe re-readable.

- Unsigned terms card. Starts or becomes available: Stringer after P09 Required uses: P14 signature Exhaustion and recovery: Cannot be torn, forged, or used as a disposable craft supply.

- Ceramic panel and folding display. Starts or becomes available: Rita; staging starts P11 Required uses: Cooperative transport; P13 reveal Exhaustion and recovery: Attached securely, never breaks; failed moves park it safely.

- Guest-program card and pledge board. Starts or becomes available: Planning board, P13 Required uses: Route people and record commitments Exhaustion and recovery: Clearly offered at the start of P13; no earlier hidden pickup required.

- Eight named pledge cards. Starts or becomes available: Board, P14 Required uses: Match, approve, and record promises Exhaustion and recovery: All supplied together; wrong deliveries return the card immediately.

Keep pocket inventory around six to eight meaningful objects at its busiest moment by treating positioned equipment and pinned records as world objects. Do not impose a carry-weight limit, storage puzzle, or inventory tax.

## Dialogue knowledge and representative original lines

Knowledge gates are explicit notebook entries, never remembered exact phrasing. A topic remains available until its purpose is complete, and asking it again gives a short recap.

- KNOW_EVENT_PURPOSE comes from the complete invitation in P02 and unlocks meaningful preparation requests.

- KNOW_RITA_CREDIT comes from her signature/class card; it enables the correct full-name slate, but accepting a plainly supplied name from her direct dialogue is also valid.

- KNOW_GATE_CAUSE is supplied by looking at the visible moving latch and decoration hook or by asking Felix to demonstrate it.

- KNOW_VIVIAN_SCOPE is any clear account of tonight’s work and a separate possible later conversation. It carries no romance requirement.

- KNOW_EIGHT_PORTIONS comes from the guest plan and recipe annotation; both remain available.

- KNOW_TERMS comes from the P09 conversation and becomes a re-readable card.

- KNOW_CUE_ORDER comes from the P02 plan and P10 restoration. P12 adds a physical viewpoint, not a new secret order.

- KNOW_DISPLAY_PERMISSION is Rita’s explicit readiness in P13, after dinner has been served.

Illustrative sample lines, all newly authored for this game; the companion complete script is the authority for delivered player-facing wording while this GDD retains mechanical authority:

Jackie: “I said I could bring everyone together. I should have specified a doorway.”

Bunny: “Your invitation says ‘no surprises.’ Did you send that to the surprises?”

Frankie: “A plan is a promise with the nouns filled in.”

Milo: “The equipment is vintage. The enthusiasm is under warranty.”

Vivian: “I can make a small room feel larger. I cannot make three different evenings happen in it.”

Rita: “These bowls have survived a kiln. I would still prefer they avoid your publicity.”

Felix: “It closes softly when nobody has decorated its moving parts.”

Stringer: “I asked for a quiet evening.”

Jackie: “We have reduced the number of simultaneous misunderstandings.”

Audience, asked about cue visibility: “We can see ‘SHOW’ first. We can’t tell you whether that is your plan.”

## Audience and laugh cue register

Confirmed feature: a realistic sitcom crowd laugh track using original or properly cleared recorded/generated laughter, never extracted television audio, with a varied bank of light, medium, and full reactions and the user-preferred cleaner, more natural, less-compressed texture. It complements the actual live-audience convention. Audio implementation, volume, captions, cooldown, and Off controls belong in the presentation specification.

- AUD_ENTER and AUD_EXIT reveal/leave the apron without changing time or story flags.

- AUD_SOUNDTEST is optional in P05 and has Bunny as a fully supported alternative.

- AUD_CUE_VIEW is the required physical perspective change in P12; Jackie can read the visible cards himself or ask what they show, then reach the far-side swivel-release catch.

- AUD_ADDRESS is the voluntary P12 rehearsal. Audience responses concern clarity, not hidden correctness or moral scoring.

- Example cue bindings, not a total-count cap: LAF01 follows the doorway competence reversal; LAF05 the tape-to-plain-speech contrast; LAF07 the first onion misunderstanding; LAF11 the display’s physical payoff; LAF12 the shared confetti flourish; LAF13 at most one harmless wrong-door gag; LAF14 follows the final bigger-pencil tag.

No laugh is required to understand a clue. Do not laugh at sexuality, refused advances, anxiety, apparent injury, sincere gratitude, or someone asserting a boundary. Repeated failures receive helpful text, not repeated ridicule. The audience never automatically shouts a solution.

## Solvability and bounded variations

The baseline game has one successful ending with small tone variations. Any respectful P06 relationship choice succeeds. P01 accepts help or a safe surface. P05 accepts Bunny or the audience. P09 accepts observation or a direct precise question. P10 accepts reusable ceramic tiles or visibly clipped paper. P11 permits either helper order and recognizes advance gate preparation. These variations change presentation, not the dependency graph.

There is no death, injury fail state, physical combat, theft requirement, pickpocketing, maze, pixel-hunt hotspot, hidden affection threshold, irreversible item destruction, money grind, or offscreen countdown. A blocked state always has a return route and a named missing condition. The only staged surprise consumes an explicitly edible item whose information has a permanent backup. The four authorized verbal competitions use recoverable social losses and four eventual wins; they are standing sitcom arguments, with no sword or attack mechanics.

Before delivery of a playable build, test every preparation order, both P09/P10 orders, each accepted alternative, repeated audience entry/exit, save/load on both sides of the set boundary, saving during the supported-display state, dialogue interruption, muted audio, and moving furniture before and after each delivery. The journal should report current observable facts, not unexplained designer flag names. Also test every contest’s practice, win, loss, concession, and rematch path, all four latched wins, and saving/restoring a pending response or committed KO.

Optional content is capped at twelve short Look at jokes, one extra conversation topic per principal, three audience exchanges, and two original background prop gags. It yields no required item, unique clue, or better ending. Do not add another venue, rival suitor, police officer, competition bracket, romance-meter branch, or sequel quest to reach the target duration. The four required verbal competitions and full end-credit roll are explicitly authorized core content and do not consume this optional-joke allowance.

## Interface and player comfort

The interface preserves Monkey Island 2’s verb-and-sentence interaction, with original art, icons, wording, and scene content. The nine commands are Give, Open, Close, Pick up, Look at, Talk to, Use, Push, and Pull. Walk to is the default scene action, not a tenth verb button. The original Lucasfilm reference card establishes the command set; its manual establishes the sentence line, inventory icons, and suggested right-click action. These references describe the interaction language, not permission to reuse the original interface artwork.

The authored layout uses a 320 by 200 logical canvas: a 320 by 136 scene and a 64-pixel lower interface. The top nine pixels of the interface display the current sentence. The remaining area places a three-by-three verb grid on the left and eight inventory slots plus page arrows on the right. This allocation is a production proposal to be tested for legibility; it is not a claim that these are the original game’s exact pixel measurements.

Left-clicking empty walkable space walks Jackie there. Clicking a verb selects it, then clicking a valid hotspot executes the sentence. Clicking an inventory item selects it; selecting Use and a second item or hotspot forms “Use [item] with [target].” Selecting Give and a character forms “Give [item] to [person].” Hovering previews the complete sentence before execution. A right-click chooses the authored sensible default for a hotspot, while preserving all nine verbs for deliberate experimentation. Objects that need Push or Pull visibly afford those actions and receive specific responses to other reasonable attempts.

Input feedback is immediate. Targets highlight on hover and are named on the sentence line; an interaction cursor changes when Jackie can act. Room exits occupy generous hit regions and have visible destination names after first discovery. Inventory pages never reorder unexpectedly: new items append, consumed objects leave a gap until the next room transition, and combined items occupy the first source slot. The journal automatically retains any information printed on a consumed clue.

Keyboard operation follows the same game logic: Tab cycles visible hotspots and interface regions, Shift-Tab reverses, arrow keys select verbs and inventory, Enter activates, and Escape cancels a pending sentence or opens the menu. Mouse and keyboard bindings are remappable where the chosen engine permits. No puzzle depends on dragging, double-click speed, precise pointer positioning, or holding two controls at once.

### Optional help and reduced repetition

Hold Space to reveal interactive hotspots and exits without revealing solutions. This assists visual access and removes pixel hunting. The journal groups current goals by person and records what Jackie actually learned; it does not invent information from offscreen conversations. A three-stage hint is requested from the current goal: first restate the relevant observation, then identify the relationship or object connection, then state the exact action. Hints never activate automatically or block completion.

Repeated exits can be skipped after the destination has been visited. Walking, repeated service animations, and previously heard dialogue can be skipped separately. First-time plot scenes can also be skipped, with their new clue and current objective recorded in the journal. A review button replays the most recent critical conversation as text. These conveniences change presentation only; they do not advance puzzle flags accidentally.

Use separate Music, Sound Effects, Audience, and Interface volume controls. Audience has an Off setting; muting it leaves the physical spectators and their puzzle participation intact. Eight distinct synthetic speech-balk voices with synchronized mouth motion are required, alongside complete readable text and captioned important sound events. Provide independent Voice volume and Off without removing text, silent cadence, or accessibility options. Fully spoken human voice acting would be a separate future decision. Speaker names accompany dialogue, and no essential clue is conveyed only by color, musical pitch, a facial expression, or stereo placement. Text speed, click-to-advance, reduced flashing, and reduced screen shake are player settings. A large-text mode uses a reflowing dialogue or journal panel rather than squeezing enlarged text into the original HUD.

## Visual direction and asset scope

Confirmed visual direction: the sixteen user-selected images in the visual reference gallery inform the game’s style. Observed references combine richly shaded pixel-art adventure scenes and small readable figures (V01–V06), an illustrated promotional portrait (V07), photographic promotional layouts (V08 and V16), and warm photographic sitcom interiors and ensemble staging (V09–V15). They are complementary references rather than one uniform rendering technique.

Confirmed art synthesis: create original pixel-art sprites with the level of grit and detail admired in Monkey Island 2, using richer clustered shading and readable material, hair, and cloth detail. Match the backgrounds to the same sprite-art treatment through a cohesive palette, lighting direction, shadow color, edge language, and texture density. Preserve clear silhouettes, warm lived-in household materials, expressive ensemble blocking, and period clothing. Use the photographs for set-material, costume, gesture, and expression studies, not as a requirement to insert photographs into gameplay. The original house must suit its three residents and the existing puzzles; source floor plans, faces, costumes, props, signage, logos, and interface graphics are not production assets.

Use a 320 by 200 logical art canvas with integer scaling where possible and an optional 4:3 aspect-corrected display. The engine proof must verify pixel-aspect handling, input mapping, and UI legibility on the intended host display. Choose the final palette limits after the engine is proven; the initial target is a cohesive VGA-like 256-color look, not a promise to impose a technical 256-color limit on every renderer.

### Applying the references to the original game

Palette and light. Observed: V01 and V03 contrast blue-violet shadow with gold or amber light; V02 and V05 use bright greens and cyan daylight; V09–V15 emphasize honey wood, cream, orange, rust, and plant greens. Proposed: a warm household base with costume accents and selectively cooler dusk/exterior shadows. Keep task areas and faces readable; color alone never carries a clue.

Background rendering and composition. Observed: adventure images combine painterly texture with discrete pixel clusters, large foreground shapes, and layered depth. The photographs show patterned upholstery, wicker, wood, lamps, curtains, plants, and arches. Build these materials from coherent pixel clusters with purposeful texture and grit, while reserving strong edges and value separation for doors, the gate, the serving hatch, and active props. Backgrounds and sprites must look painted for the same scene rather than separately styled layers. Richer detail must not obscure silhouettes, interactive props, or the existing clear walking lanes across the seven screens.

Character scale and expression. Observed: V01–V06 use compact, contrasting gameplay silhouettes; V04 uses much larger detailed faces; V09–V15 communicate relationships through eye lines, brows, head angles, hands, and overlapping group poses. Proposed: test sprites in the actual room framing, give all eight original cast members distinct proportions and gesture habits, and reserve extra facial detail for freeze-frame portraits. Do not derive a fixed sprite height from resized reference images.

World scale and floor contact. Character size must agree with the room’s perspective and physical landmarks, especially door openings and frames, bench seat height, and window/sill height. Define consistent floor-foot anchors and depth calibration for each room. Jackie must not look undersized beside the porch bench or doorway; Bunny’s head/body scale and position inside the window must agree with that wall plane. Check apparent adult proportions at comparable depth rather than comparing a visible head with another character’s full sprite.

Scale acceptance. Compare every principal’s walk, idle, talk, carry/use, and required reaction poses across foreground, doorway, and background depths and at room transitions. Feet must meet the intended floor, steps, or support surface without floating or sliding; scaling and pose changes must not make the actor jump in height, detach from props, or break occlusion and hotspot alignment. Door, bench, and window reference heights are the shared calibration checks. Review at the target display/pixel aspect and in the native runtime, including queued approaches to interactions.

Current art candidates and calibration. R3 porch and Jackie/Bunny character candidates are prepared and reviewed offline, with richer shading and material detail matched across sprites and background; they are not final user-approved art, and native integration remains pending. The current core P02 build still uses R2 art. The corrected authored calibration remains about 78 visible pixels for Jackie in the foreground and 56 at the doorway, with Bunny’s visible head about 9–10 pixels at the window’s wall plane. These screen-space values are candidates, not final canonical dimensions. The earlier 24-by-48 diagnostic sprite does not set the final scale. Review R3 together in the native scene for depth, floor-foot anchors, all poses, queued approaches, palette/lighting consistency, texture readability, and occlusion before accepting it.

Costumes and set dressing. Observed: the photo references include collared and striped shirts, high-waisted trousers, long dresses or loose layers, athletic separates, contrasting hair shapes, and both vivid and quieter garment colors. Proposed: design a distinct period silhouette and readable color/value grouping for each original character. Keep important hands and held objects clear; use patterns at a scale that does not turn into visual noise.

Interface and title readability. Observed: V03, V05, and V06 separate a dark verb/inventory panel from scenery, while V02 and V05 use conspicuous outlined dialogue. V07, V08, and V16 use large decorative display lettering and strong portrait grouping. Proposed: preserve scene/HUD separation, high-contrast scalable text, and recognizable original icons. Decorative lettering belongs mainly in title and credit cards, not small verbs or clues. No existing show logo, screenshot UI asset, watermark, or branded costume detail is copied.

Freeze frames and visual proof. Proposed: apply V04’s portrait legibility and V07/V16’s broad graphic shapes to the already specified eight original opening introductions; study the photographs’ clear reactions without reenacting their shots. Review one house scene, a group of original sprites, one close freeze-frame card, and the complete verb HUD together before committing the final art pipeline. Check reduced-motion presentation, muted audio, large text, overlapping characters, hotspot clarity, landmark-based character scale across poses and depths, and a consistent level of pixel shading and texture between actors and backgrounds in the native scene.

Seven reusable scene backgrounds define the production boundary: shared living room, kitchen, front porch, side passage, courtyard, Milo’s garage lounge, and the Stringers’ conservatory. Reuse these spaces across preparation, arrivals, and finale using lighting, prop placements, open doors, and character blocking. The courtyard’s festival dressing is a state layer on the same background, not an extra location. Authored set edges reveal a reusable studio apron and the live audience as an overlay on the current scene, rather than expanding into an eighth explorable neighborhood location. Returning from the apron restores the room and current puzzle state. The relationship-map artwork and puzzle dependency diagram are design sources, not in-game screens.

Eight speaking principals are the complete cast for the designed adventure. Jackie receives directional walk and idle cycles, talk gestures, pickup/use poses, tray-carry variants, and a small set of scene-specific physical-comedy animations. Other characters need readable idle, talk, and interaction poses plus only their specified puzzle animations. Background guests can be silent silhouettes or reused incidental figures; they never carry undisclosed clues or require a ninth developed personality.

## Implementation boundaries and validation

The GDD specifies the complete playable design and an unmodified stock ScummVM release requirement. SCI1.1 now provides the implemented stock-compatible P01 foundation using original scripts and resource data; historical patched-SCUMM diagnostics remain research only. The remaining game, broader integrated audio/runtime acceptance, actual Steam Deck testing, distribution details, provenance for other assets, and title/branding review remain production work. The user’s five supplied Suno MIDI bundles have recorded provenance and authorization for soundtrack production. The working title remains Come and Knock on Our Door as requested; title choice and renamed characters alone do not establish legal clearance.

Implement each puzzle as an explicit state transition, independent of animation completion. An action validates its prerequisites, changes inventory and flags once, queues feedback, and then commits a save checkpoint. Repeating a solved action produces a contextual response without duplicating rewards. Transient dialogue selections cannot strand an item, move a required character permanently away, or suppress a clue. Every room can be revisited until the ending is explicitly started.

The proposed release acceptance pass includes:

- Complete a fresh run with no hints, a run using the final hint at every gate, and a run that postpones each parallel branch until the others are finished.

- Test every legal ordering of the five preparation branches and every supported variation in the finale. Check that evidence, dialogue, and character positions agree with the saved state.

- For every puzzle gate, load immediately before the successful action, during any interruptible presentation, and after the committed result. Confirm exactly one reward, a stable inventory, correct journal entries, and restored audio state.

- Try giving every portable plot-critical item to every present character and using it on every plausible hotspot. Required items must be refused, safely returned, or transformed according to the specification; they can never disappear through a generic response.

- Play with keyboard-only input, hotspot assistance, maximum text size or accessibility display mode, muted music, and muted sound. All clues and success feedback remain available.

- Verify new-player timing against the 90–120 minute target. Treat chapter estimates as a hypothesis: reduce repetitive travel or improve clueing before padding the game with extra chores.

- Cross every authored set boundary before and after each story phase; test leaving and returning during a pending task, muting the audience, requesting repeated soundchecks, and loading after a fourth-wall reveal. No audience visit loses progress, invents offstage knowledge, or replays a consumed laugh.

- Verify all eight exact name cards appear before new-game control; test full watch, skip at every card, pause/manual advance, reduced motion, large text, muted audio, Continue, and menu replay. New-game paths must reach identical P01 inventory, NPC, puzzle, and music state; replay must preserve the invoking session. Check default 60-second timing within the opening allowance, readable names, clean audio transitions, and original/cleared credit assets. Also verify character scale against door, bench, and window landmarks across rooms, poses, and depth planes, with stable floor-foot anchors and consistent occlusion.

- For each VC01–VC04, prove a first win, a loss with a real narrow concession, immediate and later rematches, persistent learning, correct tier/deck order, no repeated prompt within an attempt, and restoration of the exact deck and pending response. Test all-win and mixed-loss paths, previous-win/later-loss behavior, final-gate reporting, and practical progress after resolved losses. Assert that credits, consent, repair safety, deliveries, and signatures never change because of an insult result. Test skip/mute/menu/save/load before and after a scored exchange and social KO, with one committed outcome and no stale voice/laugh/wince replay.

- Verify the original face-to-face standing presentation, gathered onlookers, non-contact winces, accessible yellow-to-red composure meters, central KO, unique voice-profile groans, and safe single-PCM/music routing. Validate the twenty-four accepted pairs and exactly three contributions from each of eight writer personas. Confirm the full ending freeze-frame, cleared audience celebration, complete fictional/actual credits, required shipped-asset notices, pause/skip/replay, and unchanged GAME_COMPLETE state in every presentation path.

- Preserve source attribution and the recorded authorization and adaptation lineage for the supplied Suno MIDI bundles. Check original writing and art and notices for other soundtrack sources, the runtime, and the soundfont before distribution. This is a release checklist, not a legal conclusion.

## Reactive music and audience audio

Status: canonical design and acceptance contract within the authorized development project. The stock-native foundation and isolated audio proofs exist; the full soundtrack, new verbal competitions, finale credits, and complete integrated runtime acceptance remain in production. All numerical budgets below are proposed production constraints, not claims about Monkey Island 2 internals.

### Confirmed listening baseline and scope

The user confirmed FluidSynth with FluidR3_GM.sf2 as the soundtrack target, matching the supplied Steam Deck ScummVM Flatpak configuration: versioninfo=2026.3.0, music_driver=fluidsynth, soundfont=/app/share/soundfonts/FluidR3_GM.sf2, mute=false. The supplied Monkey Island 2 entry has gameid=monkey2, description=Monkey Island 2: LeChuck's Revenge (SE/DOS/English), enhancements=511 and music_volume=161. These are reference settings, not proof of the source game's channel allocation or a description of remastered music. Keep the enhancement mask opaque. The new game's mix must be calibrated on its own material rather than copying a raw volume setting as a loudness target.

Deliver an original, game-reactive MIDI score built around recurring motifs and themes arranged from the user’s authorized source MIDI bank, with new supporting material as needed for the entire 90–120-minute adventure: location identity, character entrances, relationship changes, preparation progress, the supper, the hinged-display rescue, the honest microphone performance and shared confetti collapse, the four verbal competitions, the promises, the quiet ending, and the happy freeze-frame/full end credits. A sitcom laugh track and the visible studio-audience boundary are also confirmed features. “Full score” means complete dramatic coverage and authored transitions, not 120 minutes of unique linear music. A stock-native P01 audio checkpoint and a separate eight-role density fixture now exist. Final composition, MIDI production, human audience recordings, and complete in-game coverage remain implementation deliverables. This GDD supplies the design and acceptance contract.

MI2 is a methodology reference: related themes, complementary orchestrations, musically timed changes and comic phrasing. Do not reproduce its melodies, harmony sequences, signature arrangements, recordings or extracted game data. The user states that the five supplied MIDI bundles were created with Suno, asserts ownership, and authorizes their adaptation, rearrangement, further development, and reuse in this game’s soundtrack. These particular bundles are approved production source material. The game's title is not permission to quote any similarly titled television song.

ScummVM's output device is separate from the engine's scripting/audio API. A FluidSynth setting does not confer iMUSE capabilities on AGS or SCI. ScummVM documents device selection, SoundFont requirements and the distinction between MIDI instructions and synthesized sound. ScummVM audio documentation

### Stock runtime requirement and toolchain status

Historical diagnostic only: ScummC-generated original SCUMM v6 content ran under its own game identity only with a ScummVM recognition patch. This establishes diagnostic progress, but does not satisfy the unmodified stock ScummVM requirement and is not an approved production default. SCI1.1 has superseded this experiment as the implemented stock-compatible foundation. The custom ScummC result remains historical evidence only and is not the current production route. Never ship the game disguised as Day of the Tentacle. ScummC author documentation

Alternative not selected: AGS data on stock ScummVM’s AGS engine. SCI1.1 is the current implementation foundation; AGS is not selected or approved for production. The current stock implementation review found MIDI position reporting fixed at zero and MIDI seek unimplemented, so the standalone AGS audio API does not establish suitability for the proposed reactive arrangement system. Exact synchronization, simultaneous MIDI behavior, FluidSynth with FluidR3_GM.sf2, and PCM audience playback remain unproven on this route and must satisfy the same stock-runtime acceptance tests. No extra runtime plugin may be required outside the stock distribution. Pre-orchestrated MIDI variants qualify only if they meet the same reactive-music listening contract. AGS audio API, ScummVM release history

Chosen implementation foundation: original SCI1.1 Game/Sound scripts and resource data, built with the specifically approved, pinned headless SCICompanion compiler-only port. The unchanged official ScummVM 2026.3.0 Ubuntu release recognizes the checkpoint through its legitimate generic sci-fanmade fallback, and the game presents its own title. This requires no alias to a commercial game, recognition patch, custom engine plugin, upstream registration, or donor-game template. Stock launch and the bounded P01/audio evidence below are established; the complete production audio gate and actual Steam Deck acceptance are not. No musical capability reduction is approved. SCI Companion, Sound Editor, DoSound API

Hard compatibility rule: the released game must run in an unmodified stock ScummVM installation. It must not require a custom binary, recognition patch, substituted game identity, or an engine plugin added outside the stock distribution. Custom-runtime experiments are historical diagnostic evidence only, not a shipping route. Continue implementation on the verified stock-compatible SCI1.1 foundation, while retaining the full audio and device acceptance tests as release gates. If a remaining required capability fails, address it within the stock constraint or re-evaluate stock-compatible routes without waiving FluidSynth, FluidR3_GM.sf2, or reactive musical behavior. ScummVM’s support for several engines does not combine their APIs. Use “iMUSE-inspired reactive MIDI” until the selected route’s actual behavior is demonstrated.

#### Verified stock native P01 checkpoint

Foundation and provenance. The tested checkpoint uses the unchanged official ScummVM 2026.3.0 Ubuntu 24.04 release on cloud Linux, FluidSynth 2.4.4, and the recorded FluidR3_GM.sf2 asset. The original SCI1.1 Game/Sound framework and resource data use only the approved pinned compiler port. No Sierra template, framework, driver, executable, artwork, dialogue, or audio resource was imported. ScummVM may display its generic fanmade label; the game itself displays Come and Knock on Our Door. This is stock compatibility through supported fallback detection, not a substituted commercial-game identity.

Combined P01 evidence. The final native run verified both approved tray solutions, nine selectable verbs, physical-audience interaction, muted captions and saved preferences, held-credit save/load/resume, a paused-world save/restore with a live stinger, save/load cancellation, rapid room reversals, and full 60-second opening replay without resetting puzzle state. Seventeen native checks passed with zero failures, followed by a clean quit. The opening currently uses ten static placeholder cards, comprising eight cast credits plus title/end cards; it does not complete the required action-and-freeze-frame choreography. Scenery and cast art in this frozen checkpoint remain schematic placeholders; separate R2 art candidates do not retrospectively change its tested geometry.

Audio evidence and limits. The combined P01 run has a 405.23465-second actual stereo mixer capture with zero clipped samples. Final targeted waveform review supports held-credit continuation, paused-stinger replay suppression, duck/mute behavior, and clean exit; it does not close the broader production audio gate. Eight-role density and the authored 96-to-104 BPM bridge were demonstrated in a separate fixture and are not yet integrated into the tested P01 candidate. MIDI and synthetic PCM coexist, with mute and guarded save/rejoin evidence. Global-menu recovery can resume a base-only partial bar before the additional part returns at the next compatible guard; measured returns occurred after about 0.52 seconds in an earlier run and about 2.1 seconds in the final run, depending on pause position. Recovery waits for the next compatible bar; no immediate, sample-continuous, or fixed elapsed-time guarantee is claimed. Captured mixer output does not establish physical listening quality or device latency.

Soak evidence. The earlier component capture lasts 1953.05 seconds, about 32.55 minutes, including menu pauses and initial stress. Excluding pauses gives 31.29 minutes; the later uninterrupted base-only span is 29.27 engine minutes. This supports bounded loop stability and recovery evidence, not a claim of 30 continuous adaptive worst-density stress minutes. The existing full-density Deck stress requirement remains open.

Remaining production work. This checkpoint has one PCM lane and guarded manual saves; it has no independent autosave. Automatic checkpoint/save-UI work remains open. The synthetic PCM chuff is test sound, not the final human laugh track. P02–P14, remaining locations, the integrated three-room slice, broader coordination/microphone/tempo transition matrix, final score, audience recordings and everyday foley, final visual art and credit choreography, controller navigation, and actual Steam Deck listening and performance acceptance remain required. Preserve the full design and acceptance contract rather than treating this source checkpoint as game completion.

### Musical identity and cue map

Confirmed soundtrack direction: late-70s sitcom-pop, buoyant soft-rock, jaunty piano, bright brass, crisp drums, walking bass, breezy strings, handclaps, cheerful duet vocals, major-key hooks, compact tv-theme arrangement, and analog warmth. Apply this palette throughout the intimate house-and-neighbors ensemble score, adapting density and energy to the scene rather than turning every interaction into a fanfare. Approve the precise FluidR3 patches and mix by listening; retain space for dialogue, sincere moments, and clear action feedback.

#### Buoyant arrangement blueprint

The earlier author blueprint is preserved verbatim below as the invitation and buoyancy reference, not a measured description of any current arrangement. The latest swing, dynamics, relaxation, and sparsity refinements that follow control its realization. Preserve the confirmed instrument palette, repeated use of authorized source-bank motifs, and the full native/audio acceptance contract while avoiding the rejected heavy, overly frantic, rhythmically disconnected, or static treatments.

Author direction, quoted verbatim: “Give me buoyancy. Let the whole thing skip. Feel the bar in two big pulses, and let the little notes play between them. Put the melody slightly ahead of the floor sometimes—little pickups, anticipations, syncopations, phrases that seem to tumble happily into the next phrase. Give the bass a personality. Let it walk, hop, answer the tune, reach for passing notes, and occasionally arrive early. Let the drums smile: crisp hi-hat, light snare, little kicks in the right places, small fills that turn the corner for us. Put some air between the gestures. Short piano chords. Bright guitar punctuation. Percussion that flickers around the beat. Every instrument gets to make a witty little entrance and then get out of the way. Write the accompaniment almost like physical comedy. Somebody steps forward, somebody answers, somebody trips into the next bar, somebody catches him. The groove should have knees and elbows. And make the melody rise. Give it pickups that launch the line, little upward intervals that feel expectant, and cadences that spring into the next thought. I want the listener to feel the front door opening before anybody sings a word. Think two-beat lilt inside four-four: ba-DUM, ba-DUM, with subdivisions bubbling around it. The rhythm section supplies the trampoline; the tune does the jumping. This is an invitation. Make it sound like three people are already laughing in the next room.”

Latest controlling musical refinement. Use one shared, consistent gentle swing and a relaxed late-1970s easy-breezy jazz feel, adjacent to yacht rock. The ensemble should be sparse, precise, and unhurried, with room to breathe: err on the side of less. Melody, bass, comping, and percussion must inhabit the same groove rather than sounding independently displaced. Preserve buoyancy and the welcoming invitation through this relaxed shared feel, not through frantic activity.

Phrasing, dynamics, and coherence. Give whole phrases genuine rise, fall, accent, release, and breathing space through purposeful performance dynamics, articulation, voicing, register, and selective entrances. A static pattern with only a global gain change does not meet this direction. Keep source-derived melodic phrases and their harmony coherent; traceable source notes alone do not prove that a phrase hangs together musically. Use a small active ensemble with precise gestures and silence, and allow phrases to continue naturally across barlines. Internal bar markers must not force audible chops or a reset at every measure.

Creative acceptance gate. The user accepted the V3 short audition’s musical direction with “Bingo!”: relaxed 112 BPM, one shared 60:40 swing feel, coherent source-derived phrasing and harmony, genuine phrase dynamics, and sparse precise instrumentation. V2 remains rejected as disjunct/offbeat and too static. Full-score rearrangement may now proceed from V3’s accepted direction. This is listening approval of a short directional audition, not acceptance of every cue, the full score, or native lifecycle/PCM integration. Keep the front-door invitation and buoyancy while letting quieter or sincere scenes breathe.

Three original motif families organize the score: HOME is an inviting question-and-answer phrase with an unfinished ending; PRESENTATION is a tidier, overcontrolled transformation used for public composure; TOGETHER lets previously competing answers finish one another. Develop these families by arranging, representing, and repeatedly reprising motifs from the provided source MIDI bank. Reuse recognizable material throughout locations, conversations, preparation, setbacks, and payoffs through reharmonization, instrumentation, register, rhythm, tempo, counterline, density, and variation; newly composed connective material supports that recurring identity rather than replacing the source bank with unrelated themes. Character colors transform material within the current cue rather than starting a complete new song whenever someone speaks.

Source traceability and reprise. Preserve the supplied stems and maintain an arrangement map identifying the source bundle/file, note or phrase identity, original timing and pitch, and each transformation used in the score. Repeated use is a confirmed production direction, not merely optional inspiration. Keep the existing HOME, PRESENTATION, and TOGETHER dramatic functions and story/puzzle cue bindings; transformations must not introduce new gameplay state or replace the full reactive-score acceptance contract.

Duet-vocal aesthetic. “Cheerful duet vocals” remains part of the requested sound. The earlier superseded auditions used paired brass/flute MIDI lines as a call-and-response approach. Paired leads or any future choir patch are MIDI instrumental renderings, not recorded singing. Actual sung vocals are not promised or silently assumed to be complete; their realization would require a separate production and native-resource decision. No extra PCM lane or MIDI role has been added for vocals.

Superseded arrangement status. The first three offline arrangements were MUS01_CREDITS, MUS02_HOUSE_LIVING, and its reduced variant. Their lead theme was a hand-curated contiguous 33-note upper-line reduction from the B01S06 brass part in the Come and Dance on our Floor 2 bundle, with each arranged lead note traced to source identity, pitch, timing, hash, and transformation. The composer subsequently completed a local full-bank composition pass, but it was not uploaded or delivered and is now superseded after the user rejected its heavy, straight feel. All 46 source stems remain preserved byte-for-byte; the catalog still identifies five longer phrases spanning all five bundles and three short answers. The earlier full and reduced house variants had identical note, program, tempo, and guard streams with gain-only changes; that technical structure did not establish the requested feel. The source catalog and traceability remain available for revision. The subsequent V2 short feel audition was also rejected. The user has now accepted V3’s short relaxed-swing direction, and full-score rearrangement is active from that reference. The old bank remains superseded; V3’s short directional acceptance does not approve the whole production score. Remaining cue listening and native lifecycle/remapping/PCM integration gates stay open.

Pulse and tempo planning. Feel two large pulses inside 4/4 with one shared gentle swing; use the latest relaxed, sparse, precise phrasing refinements to govern the earlier blueprint’s subdivisions and anticipations. The earlier 96/104/112 BPM phase plan is a superseded arrangement proposal, not approved final tempi or a constraint on the revised feel. Use the accepted V3 short audition as the main-score feel reference, choosing scene-appropriate tempi and phrase treatment while preserving the 60-second opening contract, authored transition bars, safe musical boundaries, and the full reactive-state behavior. Do not use arbitrary playback-speed changes as a substitute for arranging the groove. Every state still needs a quiet arrangement that remains listenable during a long puzzle pause.

- MUS01_INVITATION. Game binding: E00 opening credits, then E01 porch-to-house opening and invitation reveal, P01–P02, L03 porch then L01 living room Authored material and reactive variants: Nonlooping CREDITS arrangement built from authorized source-derived HOME material, with the E00 pause/skip/replay contract; restrained live-play opening; P01 assistance acknowledgment; P02 revelation pickup, then a measured handoff into the exploration family

- MUS02_HOUSE. Game binding: L01 living room, L02 kitchen; E02 preparation Authored material and reactive variants: Common harmonic spine; living-room conversational arrangement; kitchen practical pulse; prepared/unfinished states share phrase positions

- MUS03_THRESHOLDS. Game binding: L03 porch, L04 side passage, L05 courtyard Authored material and reactive variants: Same exploration pulse as MUS02; airier porch; sparse side passage; courtyard arrangement combining neighbor colors; smooth room-to-room handoffs

- MUS04_MILO. Game binding: L06 Milo's garage lounge Authored material and reactive variants: Relaxed garage color over the neighborhood spine; presentational and sincere variants respond only to confirmed dialogue facts

- MUS05_STRINGERS. Game binding: L07 Stringers' conservatory Authored material and reactive variants: Precise decorative articulation, less rigid after an earned relationship change; compatible phrase/tempo grid with MUS02–MUS04

- MUS06_SUPPER. Game binding: E03 explicit Ready at P08; P09–P10 supper-evening opening Authored material and reactive variants: A deliberately composed ensemble version; surface-composure and conversational-pressure states; no implied player countdown

- MUS07_DISPLAY_RESCUE. Game binding: E04 hinged-display rescue, P11 Authored material and reactive variants: Stable comic-pressure loop; practical answers coordinate when help is accepted; earned completion cadence; no death timer

- MUS08_HONEST_MICROPHONE. Game binding: E05 honest microphone performance, P12; ends in shared confetti/status collapse Authored material and reactive variants: Space for the truthful line, then PRESENTATION relaxes into TOGETHER; the collective confetti gag has one authored music/audience response

- MUS09_THREE_DOORS. Game binding: E06 three-door supper, reveal and pledges; P13–P14 setup Authored material and reactive variants: TOGETHER arrangement; correctly routed actions and stated promises contribute complementary responses; no cue exposes a reveal before the story does

- MUS10_HOUSEHOLD_QUIET. Game binding: E07 signed commitments/quiet tag; P14 completion Authored material and reactive variants: Reduced HOME completed by TOGETHER; deliberate silence after the ending cadence; the required happy freeze-frame celebration and full end credits use an extended original reprise after the quiet tag, leaving room for audience cheer/laugh/applause

- MUS11_VERBAL_COMPETITIONS. Game binding: VC01 Milo/P05, VC02 Vivian/P06, VC03 Felix after safe P11 and before P12 introduction, VC04 Stringer after P13 food/reveal/board prerequisites. A distinct original late-1970s Hong Kong action-cinema-inspired source-motif family supplies opponent colors, a restrained turn bed, line/hit windows, and single-fire social-KO/result responses. The stylistic contrast is authorized; the main score retains its accepted relaxed sparse swing. No film-score copying or physical-combat implication. Event IDs VC_ENTER, VC_TURN, VC_RESPONSE_COMMITTED, VC_KO_COMMITTED, and VC_EXIT carry encounter ID and attempt/exchange serials; one committed event owns each response, with no replay on restore. These are new production bindings awaiting implementation and native proof.

- MUS_AUDIENCE_OVERLAY. Game binding: Authored set-boundary/audience-apron moments within L01–L07 Authored material and reactive variants: A short exposed-stage variation of the active motif; removes decorative layers, preserves underlying story state and returns to its phrase grid; no eighth full location is implied

MUS02–MUS05 each require a 32–64-bar main form with authored variation and a reduced repeat. MUS06–MUS08 require a 32-bar loopable form plus scene-specific passages. MUS01, MUS09 and MUS10 are shaped to scene pacing. The original main-score budget is approximately ten cue families, 20–24 principal arrangement states, 8–12 reusable or scene-specific bridges and up to fourteen short story/puzzle acknowledgments. The explicitly added MUS11 verbal-competition family and full MUS10 ending reprise extend that scope; their final variants and transitions must be budgeted without silently cutting existing coverage. These are content-budget ceilings to refine with the final puzzle map, not a demand that every puzzle get a separate jingle.

Character colors are mutually exclusive answers within the CHARACTER role: Jackie uses HOME's searching lead; Bunny gives it a clear practical reply; Frankie gives it a playful displaced reply; Mr. Stringer initially uses PRESENTATION; Rita's own, uncrowded mallet/woodwind phrase becomes audible when her work is credited; Milo moves from a showy flourish to a simpler sincere answer; Vivian moves from a clipped boundary-setting phrase to a complementary answer after an agreement; Felix receives a short mechanical ostinato used sparingly. These are original composition proposals, not personality statistics. Cast members do not each consume another continuously playing instrument. The studio audience is a collective presence, not a ninth named cast member.

### Puzzle-to-score ledger

- P01 Clear Door with Help. Committed event/score treatment: MUS01 briefly joins two answers; early acknowledgment of accepted assistance, without announcing later themes

- P02 Read Whole Invitation. Committed event/score treatment: MUS01 reveal pickup hands off to MUS02 exploration after the completed plan; no repeated sting when rereading

- P03 Put Rita's Name on It. Committed event/score treatment: MUS05 acknowledges Rita's work with her uncluttered answer; warm state persists

- P04 Prove Felix's Gate Repair. Committed event/score treatment: Short practical accent, not final rescue fanfare; keep gate and preparation states distinct

- P05 Give Milo an Honest Spotlight. Committed event/score treatment: MUS04's flourish simplifies after the bluff is dropped; no punitive musical sting

- P06 Agree Vivian's Role. Committed event/score treatment: Her phrase becomes complementary only after the boundary/collaboration agreement

- P07 Cook Household Special. Committed event/score treatment: MUS02 kitchen pulse reaches a settled variant; routine ingredient attempts remain unscored

- P08 Fit Three Agendas into One Courtyard. Committed event/score treatment: MUS03 combines the three compatible answers; E03 owns the eventual supper-start transition

- P09 Ask What Is Actually Leaving. Committed event/score treatment: One clarity cadence for the resolved chair-removal misunderstanding; do not pre-signal the answer

- P10 Replace Edible Service Cues. Committed event/score treatment: MUS06 advances one arrangement state after the replacement exists; physical/visual service cues remain sufficient without audio

- P11 Move Oversized Display Together. Committed event/score treatment: MUS07's TOGETHER answers become coordinated when Jackie accepts help; phrase timing decorates the completed action

- P12 Tell Truth into Microphone. Committed event/score treatment: MUS08 leaves deliberate space for the line, then gives ensemble resolution; music and audience reactions never cover the consequential words

- P13 Send Everything through Right Door. Committed event/score treatment: MUS09's correctly routed responses and earned cadence; no timer, rhythm test or required musical guessing

- P14 Put Promises in Writing. Committed event/score treatment: MUS09's completed responses flow into MUS10; home, credit and privacy commitments determine the ending state

The ledger keys on committed puzzle outcomes. Inspecting props, retrying incorrect combinations, re-entering a room or loading a save must not replay success music or reveal future relationship changes.

### MIDI parts, channels and runtime resources

Keep four terms separate: a source MIDI track organizes events; a musical part/stem is an arrangement role; a MIDI channel carries instrument/controller state; a synthesizer voice is an actually sounding sample/oscillator. An engine's sampled-audio mixer channel or iMUSE player is another resource entirely. Eight software players do not mean eight audible instruments. ScummVM iMUSE implementation

Proposed portable arrangement budget: seven melodic roles plus one percussion role, with no more than 18 simultaneously held MIDI notes in ordinary play and 24 at a brief climax, including percussion and overlapping releases in listening/profiling checks. These are conservative upper budgets for the confirmed FluidSynth output, not a minimum instrumentation or density target and not guarantees about any historical sound card. The latest arrangement direction favors fewer active parts and room to breathe. Profile actual FluidSynth voice use because one note can occupy more than one synthesis voice.

- BASS. Proposed GM channel, human numbering: 1 Function: Harmonic foundation, normally monophonic

- PULSE. Proposed GM channel, human numbering: 2 Function: Piano/guitar rhythmic figure, at most three notes at once

- HARMONY. Proposed GM channel, human numbering: 3 Function: Compact two- or three-note bed

- HOME_LEAD. Proposed GM channel, human numbering: 4 Function: Main motif, normally monophonic

- CHARACTER. Proposed GM channel, human numbering: 5 Function: Current character's answer, replaces rather than stacks character themes

- TEXTURE. Proposed GM channel, human numbering: 6 Function: Air/room identity, restrained two-note maximum

- ACCENT. Proposed GM channel, human numbering: 7 Function: Transition pickup, stinger or ensemble response; reserved when unused

- RHYTHM. Proposed GM channel, human numbering: 10 Function: Sparse percussion

Unused channels remain spare. This is an authoring map; SCUMM/iMUSE or SCI may remap parts to physical channels. Do not force MIDI-channel arithmetic over an engine allocator. Each compiled route must demonstrate the equivalent arrangement budget and stable patch/controller ownership. A dedicated MT-32 version is outside the confirmed baseline and would need a separately authored mapping and polyphony audit.

Default runtime model: one active musical sequence and one pending destination; within-cue part changes or pre-orchestrated same-length variants provide reactivity. Do not assume independently starting eight MIDI files creates synchronized stems. A second musical player may be used for an authored overlap only after channel isolation, note cleanup and save/load have passed. Otherwise transitions are serial musical bridges with natural tails. One short acknowledgment at a time; queue at most one, discard stale low-priority requests and never replay routine successes on re-entry.

#### Everyday foley and material feedback

Confirmed sound-design requirement. Give regular actions believable material and physical presence: doors opening and closing, latches and hinges, window movement, ceramic and metal clatter, setting down or lifting objects, tray/wedge contact, footsteps where appropriate, and restrained impacts. Match timbre, weight, surface, and apparent distance to the visible action. Use controlled variation among suitable takes or treatments without exaggerating an ordinary touch into a crash, and avoid conspicuous identical repetition.

Timing and information. Bind foley to the committed action or the actual animation contact, latch, step, or impact event, not merely to clicking a verb or starting an unsuccessful attempt. Repeated input, interrupted animation, scene skip, save/load, or replay must not duplicate a committed impact. Do not play a delayed clatter after the relevant contact has passed. Foley supports verisimilitude and clear feedback; it is not an automatic correctness signal. All required clues and success/failure information remain complete in text and visible state with sound muted.

Sources and controls. Use original or properly licensed foley, retain best-available source files and provenance/required credits, and document any edits and native derivatives. Preserve natural transients and tails at controlled gain without clipping. Use the independent Sound Effects volume and Off control, separate from Music, Voice, Audience, and Interface controls. Stock-native playback and scene-context listening must validate the chosen derivatives; no unproven format or simultaneous multi-PCM capability is assumed.

Current implementation status. Committed domain events are available for door, window, tray, and wedge actions, but foley production, integrated samples, walking-contact timing, and an accepted speech/laugh/foley arbitration implementation are still pending. The existing isolated talk proof covers one PCM owner, new speech preempting old laughter, natural-end queued laughter, and mute/cancel/save/restore behavior; it is not proof of integrated foley.

Sampled sound ownership. Synthetic speech-balks, critical effects, ambient/secondary effects, interface sounds, and audience reactions are logical owners of the single available PCM lane, not simultaneous physical streams. Proposed next integration policy: active speech keeps ownership; timely committed action/contact foley takes priority over audience and decorative PCM once that lane is available; an eligible authored laugh may then play if its moment is still valid. Action foley may preempt an audience or decorative sound, but must not overlap speech on a second lane. If the visible contact has already passed while speech owned the lane, omit that foley rather than play a stale impact; retain visible/captioned feedback and stage important action contacts to avoid the collision. No second PCM lane or extra MIDI voice is assumed. Critical dialogue/clues and required feedback outrank audience reactions, which outrank decorative effects. Critical feedback remains visible/captioned, and decorative effects may be queued or omitted. New talk, skip/cancel, menu, room change, save, and load clear stale queued reactions. Audience murmur and foreground laughter never stack. Keep only the current cue, expected next cue/bridge, and bounded common voice/audience banks resident; unload superseded resources, coalesce redundant volume/controller writes, and bound every event queue. Simultaneous PCM output and FluidSynth MIDI remains a stock-runtime proof requirement; speech/laugh/foley priority, walking/contact synchronization, and the full score still need integrated native validation.

### Authored markers and state contract

Maintain an engine-neutral cue manifest with cue ID, variant, tempo map, meter, key/compatible harmonic zones, logical part map, loop bounds, safe entry points, exit opportunities, transitions, priority, one-shot rules and source/license provenance. Author master MIDI at 480 PPQ; the export stage converts to the target engine's tick resolution and verifies timing. The 480 PPQ value is a source-workflow choice, not a promised engine format.

Every looping cue supplies START, LOOP_IN, LOOP_OUT, EXIT_BAR, EXIT_PHRASE, REJOIN and END markers; optional ACCENT and BRIDGE markers have explicit IDs. Markers are authoring metadata to compile into actual SCUMM hooks, SCI cues or an AGS sidecar/state mechanism. Generic MIDI marker text is not assumed to trigger game scripts automatically. Every safe entry includes the required patch, bank, pitch-bend and controller state; controller chase must be explicit or validated. Guards and bar markers identify compatible technical opportunities, not mandatory audible rests, chopped tails, or measure-by-measure resets. Per-role continuity must follow natural musical windows; do not rearticulate a held note merely because a guard is reached. Meet the native transition/save contract with verified phrasing and exports while preserving the musical line across barlines.

State input contains location, story phase, active conversation/speaker, only already-known relationship flags, solved puzzle flags, cinematic ownership and audio preferences. The game publishes committed state changes once with an event ID. Audio derives one target arrangement; it does not mutate puzzle logic. A music marker must never be required for solving the hinged-display rescue or another puzzle. Gameplay responds immediately, while its decorative score may wait for a musical boundary.

Priority order: pause/load safety; scene-owned E04/E05 passages or ending; major committed reveal; an authored audience-address moment; active conversation/relationship color; room identity; quiet-repeat variation. A higher-priority scene preserves the lower-priority intended destination to return to afterward. Conversation affects orchestration, not the entire cue, unless a specific reveal owns the scene. Relationship changes must correspond to actual game flags, not an invented affection meter.

Rules: room/state changes use the next compatible bar; larger phase/harmonic changes use an authored bridge at the next phrase exit. A destination with no compatible near-term exit gets a short neutral bridge, never an abrupt harmonic collision. Design normal location responses to become audible within one bar (about 2.5 seconds at 96 BPM); major phase bridges should resolve within four bars. Critical action SFX and visual feedback remain immediate. Comic one-shots use the next suitable beat or an explicitly authored free-time sting. They do not hold dialogue hostage.

On rapid reversals, retain only the latest requested destination and retarget from the current state; do not repeatedly restart intros. If a fade reverses, continue from its current level. Never change patches under sustained notes. Notes/pedals on a discarded part must terminate deliberately; avoid killing a continuing part through shared-channel all-notes-off. A fade is an arrangement tool, not a substitute for every composed transition.

### Save, load, pause and returning to a room

Persist logical cue/variant, current section and last safe rejoin marker, phrase phase where supported, active arrangement mask, pending target, story-event consumption flags and deterministic variation seed. Use native engine save facilities as appropriate; do not promise identical byte-level behavior across engines. Restore game facts first and derive the valid musical target from them.

On load, clear stale audio and restore instrument/controller state before sounding notes. Preferred behavior restores the musical phase through validated silent event chasing; safe fallback enters at the saved REJOIN or phrase start with a short unobtrusive fade. Never emit previously consumed success/reveal stingers, a duplicate intro or a stale destination from before the save. Saving mid-bridge must produce one coherent source/destination after loading. Exact sample-level resume is not a requirement; correct scene, arrangement and clean musical re-entry are.

Within one exploration family, room return preserves the common phrase clock if the backend can do so. Across major scenes, resume at the destination's authored rejoin. After absence, choose the variant from current story facts rather than old room cache. Pause freezes music/game clocks together where supported; resuming must not catch up missed notes or stingers in a burst. Cutscene skip sets the final narrative/audio state directly and suppresses intermediate one-shots.

### Accessibility, mix and modern usability

Music, effects, audience reactions and synthetic speech-balk voices have separate accessible controls, with mute remembered independently. Offer reduced music variation/intensity without hiding information. No puzzle depends on hearing pitch, rhythm or a musical change; captions and visible game-state responses convey essential sounds and progress. Preserve subtitle readability and permit manual dialogue advance. Music under dialogue uses a measured gentle reduction with a smooth recovery, calibrated on the fixed SoundFont; do not assume a MIDI controller percentage equals a specified dB change.

#### Synthetic speech voices and mouth timing

Required character voices. Give each of the eight principals a distinct, original procedural speech-balk identity with recognizable timbre, pitch range, rhythm, and cadence. These are expressive nonverbal speech sounds accompanying the full text, not copied actor voices or a substitute for readable dialogue. Keep each voice bound to the correct stable speaker identity across rooms, lines, and saves. Voice volume and Off are independent of Audience volume and Off; muting sound preserves all wording, clues, progress feedback, and silent presentation cadence.

Mouth and lifecycle contract. Drive closed, narrow, and open mouth poses from the same native timing source as the active utterance. The current Sync36 approach follows amplitude/cadence events, not phonemes. Pause must freeze the utterance and its mouth timing coherently; skip, cancel, a new line, or leaving the presentation must stop stale sound/events and return the mouth to a safe pose. Save/load and menu/room transitions must restore coherent speaker/text/mouth state without replaying stale speech or laughs. Never force the player to wait for audio before advancing text.

Single-lane speech-to-laugh proposal. The reference queue lets one tagged laugh wait until natural speech completion plus eight native ticks, and expire ninety ticks after it becomes ready. New talk, skip, menu, room change, save, and load clear that pending reaction immediately. These are prototype timing parameters requiring native lifecycle and integration proof, not a fixed user timing requirement. Per-owner logical Voice/Audience gains use the shared lane; Off keeps silent cadence and text. A dialogue laugh belongs in an authored conversational pause or payoff, without claiming overlapping speech and laughter on the one PCM lane.

Current isolated proof. The repaired fixture ran in unmodified stock ScummVM 2026.3.0, completed ten native lifecycle checks with zero failures, and exited cleanly. All eight original PCM profiles played with waveform correlation of at least 0.999997 each and no clipping; all 363 mouth transitions matched the intended pose at the exact native PCM tick. With Voice Off, thirty mouth changes continued while no output sample exceeded one PCM16 least-significant bit. Thirty static tests pass. The fixture uses a synthetic chuff and schematic face. Real laugh-bank and full-score integration, final cast-mouth art, complete player UI, and actual Steam Deck testing remain pending; this is isolated proof, not finished production integration.

#### Authored audience and laugh-track behavior

The laugh track defaults to On at a restrained calibrated level. Use realistic crowd laughter from original or clearly licensed recorded/generated takes, rendered as native-compatible PCM; synthetic test chuffs and television samples are not final laugh assets. The user preferred the higher-quality, more-natural, hi-fi, less-compressed audition. Use the cleaner mono 22,050 Hz signed PCM16 baseline; this supersedes the earlier 11,025 Hz/8-bit crunchy preference. The audible sitcom track and the visible audience share one authored reaction system: an offscreen laugh must not be followed by an accidental second copy when the audience becomes visible. Prefer natural small chuckles and short ensemble laughs; reserve applause or a bigger reaction for rare earned moments. Use generous writer-authored reactions throughout witty dialogue and physical setup-to-payoff sequences, while keeping intensity and timing appropriate to each moment. This is not an automatic response to every action.

Production bank target. Build a substantial pool of genuinely distinct accepted takes in three authored intensity tiers: light, medium, and full. An initial production target is 24–36 accepted takes across the tiers; this is a planning proposal, not a user-fixed count or a completed-bank claim. Intensity describes the crowd’s performance and energy, not merely volume. Pitch/speed changes, microphone or mix variants, and alternate crops of the same reaction do not count as new takes.

Sourcing and current status. Use compatible public CC0, Creative Commons, or copyleft archives, original recordings, or generated laughter with clear reuse rights. Record source, creator, exact stated license, required credits/redistribution conditions, and take identity. The current source pool contains twenty-four candidates, eight per intensity tier: twenty CC0-labeled and four CC BY-labeled clips with credits. The user gave positive feedback on the three examples in the first audition reel and chose its cleaner texture; this is not blanket acceptance of all clips or their new shortened cuts. Expanded-bank listening and native QA remain pending. Preserve unchanged best-available source files and provenance separately from derivatives, and retain higher-quality masters when available rather than implying that preview downloads are archival originals.

Native sampling and derivatives. The chosen production baseline is mono 22,050 Hz signed PCM16 RIFF/WAVE, preserving the cleaner, more natural, less-compressed character the user preferred. Do not deliberately reduce the bank to the superseded 11,025 Hz/8-bit crunchy treatment. Preserve source files separately from reproducible native derivatives and record filtering, resampling, dither, gain, trims, and natural-tail treatment. Avoid clipping, harsh conversion artifacts, overprocessing, and loss of ensemble realism. Format and edit variants retain the same source take ID and do not count as new performances. Each final cut still requires listening and stock-runtime verification.

Generation fallback. If a sufficient usable bank cannot be sourced or generated, prepare a Suno prompt for the requested crowd reactions. A prompt is a fallback to audition, not a claim that Suno will reliably produce pure laughter or that new outputs automatically have reuse rights. Record the rights and provenance of any new generated laugh assets. The separate authorization for the user’s original five supplied Suno music bundles remains unchanged.

Narrative-bound audience events: AUD_ENTER(room,boundary) and AUD_EXIT(room) control bounded apron overlays; AUD_SOUNDTEST is P05's optional audience feedback alternative to Bunny; AUD_CUE_VIEW is P12's required audience-side observation and release of the physically reversed cue rack’s catch, setting CUE_RAIL_RELEASED; AUD_ADDRESS is P12's rehearsal; AUD_REACT owns writer-authored dialogue and physical-comedy setup/payoff responses. These are audio/scene adapter events, not extra puzzles. Crossing an authored set boundary enters AUDIENCE mode: expose the physical audience/apron, lower nonessential music layers at the next beat, substitute quiet studio murmur for outside ambience and leave all puzzle/world state intact. Leaving the apron restores the current room's arrangement at a safe boundary. Repeated boundary visits do not replay a discovery fanfare.

AUD_SOUNDTEST supplies both audible and visible speaker-direction feedback. AUD_CUE_VIEW makes the cue rack's actual reversed orientation and its audience-side release catch visible; the audience does not reveal private facts or become an all-purpose hint oracle. Musical emphasis must not substitute for either observation. The P12 audience-side view remains available and understandable with all audio off.

Existing example reaction bindings, not a fixed total cap: LAF01/P01 tray-and-door competence reversal; LAF05/P05 overblown tape interrupted by a plain voice; LAF07/P07 onion-tear misread; LAF11/P11 hinged-display duet's first success; LAF12/P12 shared confetti collapse; LAF13/P13 first harmless wrong-door visual; LAF14/P14 one short response to the separate final bigger-pencil joke after the sincere household beat. LAF13 is a one-time scripted visual beat, not a general wrong-answer sound. P05's test feedback has its own neutral response rather than applause that implies success. Do not place laughter over private-life discussions, consequential personal admissions, signed promises, or the sincere quiet household beat. After that beat has resolved, LAF14 may respond once to the distinct final bigger-pencil punchline; the household theme follows without mocking the emotional resolution.

Generous authored coverage and progress. The complete script may add presentation-only reaction IDs for dialogue exchanges and physical setup/payoff beats beyond the seven examples above. A well-placed reaction may subtly reinforce already-visible authored progress, but laughter is not an automatic correctness detector, a hidden clue channel, or a replacement for explicit text and visible feedback. Every puzzle remains fully intelligible and solvable with all sound muted. Preserve the existing rules against mockery during sincere dialogue, consequential admissions, boundaries, or apparent harm; generosity of comic reactions does not override them.

Every laugh follows an authored comedy beat ID after its punchline has completed. It never fires merely because the player clicked an invalid action. Consume one-shot beats once, use at most one pending reaction, select the beat’s authored intensity from a shuffled eligible pool, exclude the last five played take IDs across all their derivatives, and apply a proposed eight-second minimum between ordinary laughs. If no take is eligible in that intensity, drop the laugh instead of repeating a recent take or substituting the wrong strength. Respect the single shared PCM lane and speech-to-laugh ownership rather than stacking or overlapping reactions. Do not delay a queued laugh until it lands on unrelated dialogue; drop it when its moment has passed. A major scene ending may deliberately override the ordinary cooldown. A recording's tail can be shortened with a natural fade if the user advances dialogue; never require waiting for laughter before continuing.

On AUD_REACT, the director permits a small music reduction and keeps any vital speech/SFX clear; it does not abruptly stop the tune. While Jackie addresses the audience, murmur drops out. Visible audience animation uses the same beat/event as the sound, but its response and any puzzle-relevant participation occur even when Audience Volume is zero or Off. Important reactions have concise captions, such as an audible collective response or a visible gesture described in dialogue; sound cannot be the only solution signal. Muting the laugh track does not remove the physical audience, change puzzle difficulty or make an interaction unavailable.

Save/load persists consumed audience beat IDs, audience-mode ownership, the last five played take IDs, and shuffled-pool state. Do not resume midway through a stale laugh after loading. Rebuild the visible audience's correct pose/state and return with silence or the appropriate low murmur. Test the audience system with music alone, audience alone, all sound disabled and rapid scene skips.

### Native proof and listening acceptance

Remaining integrated acceptance, beyond the implemented P01 foundation, requires an original vertical slice on unmodified stock ScummVM using L01/L02/L03, one dialogue state, one puzzle acknowledgment, a two-step E04/P11-style coordination event, an E05/P12-style microphone/confetti change and an authored audience-boundary reveal/reaction. Include final-style MIDI part density, simultaneous PCM audience and MIDI, room switches, a tempo-changing bridge, save/load and controller input. Use original game assets and new musical material or the user’s authorized supplied MIDI material; do not borrow assets or motifs from third-party games.

Remaining device proof target: unmodified ScummVM 2026.3.0 Flatpak on the user's Steam Deck, FluidSynth and the exact FluidR3 GM asset/version; record runtime build, SoundFont SHA-256, synth library version, gain/effects/sample rate and relevant game settings. The supplied file name alone is not a content hash. Only an unmodified stock installation counts as release-compatibility success. Historical custom builds and recognition-patched runs do not pass this acceptance gate. Retain desktop regression coverage in addition to the required Steam Deck pass; the existing cloud Ubuntu checkpoint does not substitute for that device test.

Pass criteria:

- The original game is detected through a supported identity or the legitimate SCI fanmade fallback, displays its own in-game title, and launches from a clean, unmodified stock ScummVM installation using documented game files and settings, without a commercial-game alias, custom binary, or recognition patch

- All eight logical musical roles sound with correct FluidR3 instruments, percussion mapping, sustain and controller reset behavior

- Every legal transition is tested at the first/last beat of each source bar and around loop boundaries; no missed/duplicated beat, hanging note, abrupt wrong patch or unintended silence

- Boundary timing stays within one target audio buffer or 30 ms, whichever is larger, after accounting for fixed output latency; recording/listening is the authority when APIs report misleading positions

- Fifty rapid legal location/state reversals produce bounded queues, the latest correct destination and no stacked introductions

- Save/load is tested in quiet loops, dialogue ducking, a transition, before/after a one-shot and during display coordination; no lost progress, false success or replayed reveal

- Pause, resume, cutscene skip, music mute/unmute and leaving/re-entering every location preserve coherent state

- Worst-density climax plus permitted SFX has no audible voice stealing, clipping, crackle or resource growth across a 30-minute loop/stress session on the Deck

- Synthetic speech-balks and laughter serialize correctly on the single PCM lane while MIDI continues; no stale overlap, score stoppage, or loss of critical visible/captioned feedback occurs. Voice and Audience gains/Off work independently, with synchronized silent mouth cadence and intact visual/puzzle participation

- Foley acceptance. In native scenes, test opening/closing doors and windows, object handling/clatter, footsteps/contact events, and impacts while speech, laughter, and MIDI are active. Verify material fit, controlled variation, separate volume/Off, correct event timing, single-PCM priority/preemption, stale-event drops, and no duplicated sounds after pause, skip, room change, or save/load. No sound may imply a state change that did not occur, and muted play must retain every clue and action result.

- Speech-balk acceptance. Verify all eight speaker identities, native-clock mouth cadence, pause/resume, early advance, skip/cancel, new-line interruption, Voice/Audience volume and Off, room/menu transitions, save/load, and single-lane speech-to-laugh handoff with the real bank and full score. Confirm that cancelled lines cannot leave a moving mouth or stale reaction behind. Isolated profiles, static tests, or the interrupted lifecycle run do not constitute full integration acceptance.

- Repeating the same failed action, re-entering an audience boundary, loading after a punchline or skipping a scene cannot spam a laugh, applause or a duplicate visible reaction. Validate authored intensity, shuffled selection, five-take exclusion, no-eligible-take drops, and save/load pool state; mute, cooldown, stale-drop, caption, and sincere-dialogue rules must remain intact

- Laugh-bank acceptance. Human-audition every retained take and its intended native derivative for realistic ensemble sound, distinct performance identity, appropriate intensity, clean starts/natural tails, and the user-preferred cleaner, natural texture. Reject duplicates, wrong-strength reactions, distracting speech/music, clipping, or destructive conversion artifacts. Verify the accepted bank in stock ScummVM with MIDI, the one PCM lane, mute, stale queues, repeated scenes, and save/load; source and license records must accompany each accepted take. Candidate downloads and format conversions do not count as completed listening or native acceptance.

- The entire puzzle slice is solvable with music and effects muted; essential sound cues have captions or visible equivalents

- Headphone and Deck-speaker listening confirms motifs remain identifiable, dialogue is comfortable, long loops are not fatiguing and new and authorized adapted material feels cohesive without quoting unapproved third-party references

The complete production score later requires a cue/transition coverage report against every reachable story/puzzle state and a full-game listening pass. A successful standalone MIDI render does not establish native game integration. A polished fallback that fails the agreed reactive behavior must be presented as a scope decision, not silently substituted.

### Rights and distribution record

Supplied music provenance: the user states that the five bundles in CaKoOD Soundtrack Inspiration.zip were created with Suno, asserts ownership, and authorizes soundtrack adaptation, rearrangement, development, and reuse. This records user-provided provenance and permission for these particular files, not an independent legal audit or a general claim about Suno outputs. No further source-rights approval is pending for these bundles.

The current official ScummVM Flatpak manifest sources fluid-soundfont 3.1 from Debian and installs FluidR3_GM.sf2 at the user's supplied path. The corresponding package COPYING contains Frank Wen's MIT permission notice, copyright 2000–2002 and 2008, requiring the copyright and permission notices to accompany redistributed copies/substantial portions. Preserve that notice and the exact asset provenance if bundling the font. Verify the pinned release's binary/package chain during production; do not rely only on a generic website's license summary. Flatpak manifest, Package license

ScummVM's iMUSE source is an open reimplementation under GPLv3-or-later, separate from LucasArts' original game data and music. Historical modified diagnostic runtimes retain their license/source obligations and are not release dependencies for this stock-ScummVM game. Audit authoring templates, fonts, graphics, every sound sample and any plugin separately; the compiler's license does not establish asset rights. Maintain a small third-party notices document and source/license ledger. iMUSE source, ScummVM FAQ, AGS distribution license guidance

### Foundation status and remaining production gates

- Stock detection and launch are verified for the SCI1.1 checkpoint on the unchanged official ScummVM 2026.3.0 Ubuntu release through its generic fanmade fallback; actual Steam Deck acceptance remains open, and a custom-runtime shipping option is excluded

- SCI1.1 with the approved pinned compiler is the chosen implemented foundation; broader integrated audio/runtime acceptance and the remaining game are pending. The patched ScummC diagnostic is historical research only

- Preserve the checkpoint’s recorded runtime, FluidSynth 2.4.4, FluidR3 asset hashes, and synth/mix parameters; reproduce and verify the confirmed target on the Steam Deck rather than assuming cloud-device equivalence

- Complete the eight required synthetic speech-balk voices, final synchronized mouth art, and native lifecycle/integration acceptance; full spoken human voice acting is a separate future choice, and the game remains complete with sound muted

- The V3 short main-score direction is user accepted: shared gentle swing, genuine phrase dynamics, relaxed late-1970s jazz/yacht-rock-adjacent feel, and sparse precise ensemble. Full-score rearrangement is active; verify the preserved palette, recurring authorized source motifs, source/harmonic coherence, every remaining cue, transitions, and any future vocal realization. Produce the distinct MUS11 verbal-competition family and full MUS10 end-credit reprise. Source-bundle use remains authorized; short creative acceptance does not replace full listening/native/audio validation

Canonical story/puzzle sequence: E00=opening credits before gameplay; E01=P01–P02; E02=P03–P08 preparation; E03=P08 Ready plus P09–P10; E04=P11; E05=P12; E06=P13 and P14 setup; E07=P14 completion. The named LAF01, LAF05, LAF07, LAF11, LAF12, LAF13, and LAF14 beats are existing examples, not a fixed total laugh limit. The complete script may author additional dialogue and physical-comedy reaction IDs as presentation metadata. The separately authorized VC01–VC04 competitions add only the explicit repertoire, contest, resolution, concession, and eventual-win state in their canonical section; the full final credit sequence adds presentation after legitimate completion. Unrelated editorial revisions must not add screens, characters, puzzles, or puzzle-state flags.

## Authorized soundtrack source archive

CaKoOD Soundtrack Inspiration.zip is retained in the project folder as authorized soundtrack source material. It contains 46 valid format-1 MIDI instrument-part files at 480 ticks per quarter note, across five bundles: Come and Dance on our Floor 2 (8 parts); Kisses are Hers and Hers and His 1 (10); We’ve been Waiting for You 1 (9); Tree’s Company 1 (10); and Tree’s Company 2 (9). It contains no rendered audio.

The user states that these tracks were created with Suno, asserts ownership, and explicitly authorizes adaptation, rearrangement, further development, and reuse in the game’s soundtrack. The source-rights gate for these five supplied bundles is resolved for this project; they are available for production rather than analysis only. Preserve this user-provided provenance and track the source parts used in each adaptation. Arrangement quality, listening tests, and native integration remain acceptance requirements.

## Episode research and influence traceability

“Most popular” is treated here as a crowd-ranked fan-favorite shortlist, cross-checked against independent fan discussion and criticism. The retrieved Ranker list placed Up in the Air first (194 votes, 86% upvotes), Two Flew Over the Cuckoo’s Nest second (192, 81%), and A Camping We Will Go third (176, 80%). These are one list’s snapshot, not representative audience totals or original broadcast ratings. Another community, Episode Ninja, gave a different top three. The selection therefore remains qualified rather than a universal ranking. Ranker, Episode Ninja

Ranker’s plot blurbs contained errors, so the episode summaries below use separate sources. There is no established universal ranking of thirty gags or impactful moments. M01–M30 are an unranked, source-grounded selection spanning physical farce, misunderstandings, loyalty, ensemble competence, and the emotional meaning of home. Each numbered entry below identifies its actual use in this game.

### Up in the Air

Jack accompanies Janet to a formal island party, where his high-energy performance upsets the planned social occasion and an assumed romantic relationship is corrected. The transferable shape is a carefully managed social appearance becoming public physical spectacle. This game uses a completely different event, cause, props, music, movement, and resolution; it does not recreate the episode’s dance or party sequence. Official episode guide

### Two Flew Over the Cuckoo’s Nest

The roommates mistake Terri’s psychiatrist friend for a patient and reinterpret ordinary behavior as evidence supporting that mistaken role. The transferable shape is an apparently coherent explanation built on one wrong premise. The new game applies this to event work, equipment, and social roles, with no mental-illness or supposed-dangerousness joke. Official episode guide, Independent season guide

### A Camping We Will Go

Larry’s overselling assembles people with incompatible expectations in an inadequate shared space. Overlapping personal agendas and inconvenient furniture turn the cramped retreat into ensemble physical comedy. This game translates that abstract pressure into one rented-house event and its constrained routes; it does not reproduce the cabin, hammock business, errand, or pursuit choreography. Episode record, Independent episode guide

### What the reception suggests for this game

Repeated fan discussion emphasizes sustained physical performance, the wider ensemble’s interplay, and the roommates’ home as a place of belonging. These are qualitative signals from self-selected viewers, not a representative poll. The design consequently gives Bunny and Frankie meaningful practical agency, lets visual jokes build through consequences, and gives every principal an ending payoff. Suzanne Somers’s Television Academy interview also supports treating apparent innocence as a consistent set of values rather than a lack of competence. Fan discussion, Ensemble discussion, Chris Mann retrospective, Television Academy interview

### Thirty source moments

Source descriptions establish the research reference; the game borrows only an abstract mechanism. Several mechanisms share a puzzle or recur as a payoff. This is thirty influences inside one adventure, not thirty separate scenes.

#### M01 Social image-management backfires

Janet's plan to influence a romantic prospect by bringing Jack to the party does not proceed as intended. Up in the Air. Official guide

Design mechanism: An ally agrees to play a social role; the role creates new obligations.

In this game: P02: Milo’s targeted invitations create the expectations the entire game must reconcile.

#### M02 Recovery becomes the performance

Jack's high-energy party dancing becomes an extended physical-comedy centerpiece. Up in the Air. Official guide, fan reception

Design mechanism: Each attempt to recover one's dignity supplies the next movement in a spectacle.

In this game: P11: Jackie tries to call the jammed moving display an intentional exhibit before admitting he needs help.

#### M03 Misidentified relationship

The apparent romantic competition at the party turns out to be the host's sister. Up in the Air. Official guide

Design mechanism: An assumed connection misdirects the social plan.

In this game: P06/P12: Vivian’s interest in a real collaboration is not a promised date; the complete introduction corrects the “partners” assumption.

#### M04 Incorrect professional role

Terri's doctor friend is assigned the wrong role by the roommates. Two Flew Over the Cuckoo's Nest. Official guide

Design mechanism: A correct fact about a workplace is attached to the wrong occupation.

In this game: P02/P04: Stringer calls Felix’s repair demonstration an “inspection”; Felix explicitly corrects this to a practical repair check and has no official powers.

#### M05 Innocent words acquire the wrong meaning

Fan recollections repeatedly single out the awkward everyday-word misunderstandings surrounding the misidentified visitor. Two Flew Over the Cuckoo's Nest. Fan discussion, long-running forum

Design mechanism: Listeners reinterpret neutral words according to an already false belief.

In this game: P09: “all three out of the house” refers to tagged chairs, not the three tenants.

#### M06 Private preoccupation misread from outside

A visitor's effort to recall a song becomes another apparent confirmation of the roommates' misconception. Two Flew Over the Cuckoo's Nest. Fan quiz documenting the setup, fan reception

Design mechanism: Harmless concentration looks suspicious without its cause.

In this game: P09: Stringer’s secretive chair-clearing plan seems like a house clearance until the player asks its actual purpose.

#### M07 An oversold promise gathers the wrong crowd

Larry misrepresents Jack's professional importance and the quality of the getaway. A Camping We Will Go. Episode guide

Design mechanism: A promoter's exaggeration creates several incompatible expectations.

In this game: P02/P05: Milo promotes grand partnerships before proving he can make his modest PA carry a clear sentence.

#### M08 Too many agendas in too little space

The hoped-for retreat is a one-room cabin filled with people who want different things. A Camping We Will Go. Episode guide

Design mechanism: Spatial scarcity forces social collision.

In this game: P08: buffet, performance, display, and traffic must fit one courtyard using learned sightlines and lanes.

#### M09 Pursuit chain

The overlapping Larry, Lana, Furley, and Jack agendas drive the camping ensemble's crossings. A Camping We Will Go. Dedicated discussion

Design mechanism: Moving one person changes where several others go.

In this game: P13: people follow the roles they want, and Jackie redirects each willing helper through the opening suited to that task.

#### M10 The comfort object fights back

The tired Jack's attempt to settle into a hammock becomes physical comedy. A Camping We Will Go. Favorite-episode discussion, episode guide

Design mechanism: Familiar furniture has an inconvenient physical rule.

In this game: P06/P11: an elegant screen and a folding display become awkward objects with clear, solvable geometry. No hammock is used.

#### M11 Partial overhearing invents a crisis

Roper hears a conversation through plumbing and attaches a false explanation to it. Stanley's Hotline. Official guide

Design mechanism: A listener receives enough information for confidence but not understanding.

In this game: P09: Jackie hears an eviction-shaped fragment and obtains the full context.

#### M12 The observed people regain control

After discovering the eavesdropping, the roommates and Helen turn Roper's spying against him. Stanley's Hotline. Official guide

Design mechanism: Discovery of an information channel reverses the power balance.

In this game: P12: Jackie knowingly broadcasts the full harmless sentence about putting Stringer in Rita’s front row.

#### M13 Shared constraint requires cooperation

Jack and Chrissy cannot separate after playing with handcuffs whose key is absent. Handcuffed. TVmaze, Television Academy's interview index

Design mechanism: Two people's movements or tasks become mechanically interdependent.

In this game: P11: Jackie and Felix support a folded display while Bunny and Frankie operate the controls they cannot reach.

#### M14 Hidden cooperation looks impossible

Attempts to conceal the pair's connection generate visual absurdity. Handcuffed. Independent episode review

Design mechanism: The audience understands two contributors where an onlooker thinks there is one.

In this game: P11: the “moving exhibit” pretense is more conspicuous than simply asking for help.

#### M15 Ordinary appetite meets special importance

Chrissy eats from Jack's competition entry before understanding what it is. The Bake-Off. Official guide

Design mechanism: An everyday use accidentally destroys a high-stakes object's intended use.

In this game: P10: edible bread cues are served as snacks because Jackie left them on the snack tray.

#### M16 The substitute carries a tell

The replacement dessert comes from a bakery whose owner is judging the competition. The Bake-Off. Official guide

Design mechanism: A substitution fails because provenance is recognizable.

In this game: P10: Rita recognizes her ceramic sample tiles and receives open credit for the durable cue solution.

#### M17 Shared mess dissolves status

The effort to escape the competition problem ends in a mousse-throwing melee. The Bake-Off. Official guide

Design mechanism: A ceremonial hierarchy collapses when everyone becomes equally ridiculous.

In this game: P12: Milo’s ceremonial paper flourish lands on every carefully presented outfit, dissolving the hierarchy without a food fight.

#### M18 A changed arrangement destroys a rehearsed plan

Jack's hidden cue cards become useless when studio props are rearranged. And Now Here's Jack. Official guide

Design mechanism: An apparently cosmetic change breaks the association between cues and actions.

In this game: P12: Vivian’s tidy rehanging reverses and swaps the cue rack, requiring a new physical viewpoint.

#### M19 Failure succeeds with a different audience

The disastrous television demonstration unexpectedly attracts restaurant customers. And Now Here's Jack. Official guide

Design mechanism: The protagonist misjudges the audience's real value criterion.

In this game: P12: Stringer and the actual audience prefer Jackie’s clear, ungrand introduction to Milo’s pomp.

#### M20 Emotion has more than one cause

The roommates mistake the doctor's tears of laughter for a bad medical outcome. Chrissy's Hospitality. Official guide

Design mechanism: A true observation supports a false causal story.

In this game: P07: ordinary onion tears are mistaken for gratitude, allowing a small truthful emotional follow-up.

#### M21 A false alarm reveals genuine care

Jack and Janet's efforts to comfort Chrissy reveal how frightened they are of losing her. Chrissy's Hospitality. Official guide, fan recollection

Design mechanism: Mistaken stakes still expose real affection.

In this game: P11: the roommates hurry to Jackie’s muffled “stuck,” then competently solve the actual noninjury problem.

#### M22 Loyalty costs an attractive opportunity

Chrissy insists the trio keep their accepted Christmas invitation despite a more exciting option. Three's Christmas. Official guide

Design mechanism: A character's value system changes the plan.

In this game: P06: Jackie acknowledges Vivian’s attractive industry invitation while keeping his commitment to tonight’s household.

#### M23 Apparent opponents secretly share a goal

Both hosts and guests are trying to leave for the same other Christmas party. Three's Christmas. Official guide

Design mechanism: Politeness conceals aligned interests and prolongs an avoidable conflict.

In this game: P09: Rita and Stringer both want room for her class but have assumed the other would resist.

#### M24 A benevolent secret creates a team

The roommates cooperate to protect a puppy despite the landlord's no-pets rule. No Children, No Dogs. Official guide

Design mechanism: Shared protective responsibility makes concealment affectionate rather than selfish.

In this game: P03/P08/P13: the household preserves Rita’s ceramic-house reveal until she chooses to present it.

#### M25 One printed error threatens the whole event

Larry prints the wrong opening date on the restaurant flyers. Opening Night. Official guide

Design mechanism: A tiny clerical mistake becomes a large logistical problem.

In this game: P03: the omitted “s” in the existing “Mr. Stringer” collection credit becomes a concrete authorship problem; Jackie replaces the whole attribution accurately.

#### M26 The social network is a real resource

Larry gathers visiting relatives to rescue the empty restaurant opening. Opening Night. Official guide

Design mechanism: A flawed friend genuinely helps by knowing people.

In this game: P11–P14: each contributor’s previously negotiated useful role is required for the successful event.

#### M27 Forced proximity permits honesty

Jack and Furley share a candid conversation while trapped in a freezer. Baby, It's Cold Inside. Official guide

Design mechanism: Pausing the normal hierarchy allows an admission.

In this game: P11: Jackie and Felix speak plainly while mutually supporting the unwieldy display.

#### M28 Friends outside the spotlight complete the rescue

The women find out where Jack and Furley are and rescue them. Baby, It's Cold Inside. Official guide

Design mechanism: The protagonist's friends exercise practical agency when he is stuck.

In this game: P11: Bunny operates the gate and Frankie spots/releases the wing catch; Jackie’s playable contribution is accepting and coordinating that help.

#### M29 The shared home becomes emotionally legible

The finale has the roommates leave and look back at their home; fan discussion finds meaning in the breakup of the household while often criticizing the surrounding ending. Friends and Lovers. Episode reference, fan response

Design mechanism: A familiar space gains meaning when its continuity is threatened.

In this game: P13/P14: Rita’s nonliteral ceramic house and the quiet closing meal make the home’s value about the people who share it.

#### M30 A helpful partner amplifies an object problem

The ironing-board business with Jack and Cindy is singled out by both a season-five critic and fans. Make Room for Daddy. Season-five criticism, fan discussion

Design mechanism: A well-meant second pair of hands changes the physical problem instead of solving it.

In this game: P04 foreshadows gate motion; P11 pays it off with the original folding-display/gate sequence, distinct from an ironing-board routine.

### Originality and release review

Preserve the requested title Come and Knock on Our Door during design. It is also the main title of Chris Mann’s reference book; title and branding need review before release. No claim of clearance follows from changing character names. Book record

Use original dialogue, character designs, animation, music, props, floor plans, and comic sequences. Do not import television recordings, theme lyrics, actor likenesses or voice imitations, branded sets, signature costumes, or beat-for-beat choreography. The provided MIDI archive is authorized production source material under the user’s stated Suno provenance, ownership, and permission recorded in the authorized soundtrack source archive. This approval applies to the supplied music, while the television and game-asset restrictions above remain in force. The research reduces creative dependence on specific expression; it is not a legal opinion or a guarantee of release clearance.

## Full directed relationship map

All eight principal characters are adults. This appendix records all 56 directed named-character relationships. Feelings and wants are not automatically reciprocal. Extended characterizations are authored choices for review. The separate relationship-map source contains additional beliefs and scene opportunities; the puzzle specification controls the final implemented actions.

![Embedded source image 2](embedded-images/image7.png)

The diagram shows the major pressures only. The complete directed entries below are authoritative for feelings and wants.

### Jackie Tree toward the others

- Toward Bunny Easter. Feels: Affectionate trust, mixed with guilt about overusing her goodwill. Wants: Her candid read of guests and a genuinely shared supper-club plan.

- Toward Frankie Maplewood. Feels: Respect, dependence and mild fear of her accurate verdicts. Wants: Her logistical help and a chance to earn back credibility.

- Toward Mr. Stringer. Feels: Anxious politeness toward the person controlling the tenancy. Wants: Ordinary renewal forms, promised courtyard repairs and fair judgment of the household.

- Toward Milo Pennant. Feels: Enjoys his audacity but distrusts his grand announcements. Wants: The promised hi-fi equipment and an accurate account of the supper-club promotion.

- Toward Vivian Voss. Feels: Attracted and impressed; flustered by her directness. Wants: A sincere connection without promising time he cannot give.

- Toward Rita Stringer. Feels: Likes her wit and suspects she sees through him. Wants: An ally in a fair conversation with Stringer.

- Toward Felix Bunt. Feels: Amused impatience that can grow into genuine respect. Wants: A safe repair, usable equipment and precise access instructions.

### Bunny Easter toward the others

- Toward Jackie Tree. Feels: Fond and protective, but tired of being volunteered. Wants: Honesty, mutual backup and a meaningful job of her own.

- Toward Frankie Maplewood. Feels: Deep affection with irritation at being managed. Wants: Trust in her social judgment and room to improvise.

- Toward Mr. Stringer. Feels: Dislikes his rules but hopes he can behave better. Wants: Permission to enjoy her home without being patronized.

- Toward Milo Pennant. Feels: Likes his energy; increasingly skeptical of his showmanship. Wants: Follow-through and invitations that mean what they say.

- Toward Vivian Voss. Feels: Admiration without romantic rivalry. Wants: Styling advice and recognition as a capable co-host.

- Toward Rita Stringer. Feels: Feels welcomed as an equal and enjoys her mischief. Wants: A mentor who takes her ideas seriously.

- Toward Felix Bunt. Feels: Finds his earnestness endearing; defends him from mockery. Wants: A demonstration she can understand and a safe way to help.

### Frankie Maplewood toward the others

- Toward Jackie Tree. Feels: Loyal affection tempered by exasperation. Wants: Straight answers and a fair share of the workload.

- Toward Bunny Easter. Feels: Protective love and genuine respect she rarely says aloud. Wants: Early warning before a generous offer becomes household work.

- Toward Mr. Stringer. Feels: Open skepticism toward arbitrary authority. Wants: Written renewal and repair commitments, consistent rules and acknowledgment of tenant competence.

- Toward Milo Pennant. Feels: Enjoys his jokes, refuses to subsidize his boasting. Wants: Return of borrowed things and one accurate inventory.

- Toward Vivian Voss. Feels: Professional respect with a touch of territorial caution. Wants: A reliable collaborator who will respect the shared home.

- Toward Rita Stringer. Feels: Respects her insight, distrusts covert maneuvering. Wants: Direct support when Stringer applies a double standard.

- Toward Felix Bunt. Feels: Respects real skill; has no patience for invented rules. Wants: A specific repair and accurate diagnosis, without unauthorized changes.

### Mr. Stringer toward the others

- Toward Jackie Tree. Feels: Conditional approval mixed with suspicion when appearances change. Wants: A quiet, credible supper club and reassurance that his judgment was correct.

- Toward Bunny Easter. Feels: Paternalistic fondness; underestimates her acuity. Wants: Deference and a cheerful endorsement of his decisions.

- Toward Frankie Maplewood. Feels: Wary respect; feels challenged by her precision. Wants: Cooperation without a public argument.

- Toward Milo Pennant. Feels: Finds him disreputable, while envying his social ease. Wants: Fewer disturbances and an invitation that feels respectable.

- Toward Vivian Voss. Feels: Intimidated by her confidence and eager to seem worldly. Wants: Public respect and reassurance the gathering has standards.

- Toward Rita Stringer. Feels: Longstanding affection hidden under habitual defensiveness. Wants: Loyal support and protection from public embarrassment.

- Toward Felix Bunt. Feels: Likes his formal manner; doubts the bill. Wants: A practical layout and working courtyard repair without unapproved expense.

### Milo Pennant toward the others

- Toward Jackie Tree. Feels: Real friendship complicated by competitive swagger. Wants: A capable cook who makes his overpromoted supper club deliver.

- Toward Bunny Easter. Feels: Likes her enthusiasm and fears disappointing her. Wants: Help correcting the new-partners promotion while keeping willing guests interested.

- Toward Frankie Maplewood. Feels: Respects her competence; dreads her ledger. Wants: Enough organizational help to rescue his reputation.

- Toward Mr. Stringer. Feels: Resents the policing but craves the stamp of respectability. Wants: Permission for a limited event and recognition as useful.

- Toward Vivian Voss. Feels: Professional admiration and wounded vanity. Wants: Her styling talent and endorsement of his event credentials.

- Toward Rita Stringer. Feels: Enjoys her wit and recognizes a better organizer. Wants: An introduction and rescue from an overpromised social obligation.

- Toward Felix Bunt. Feels: Amiable rivalry between a salesman and a perfectionist. Wants: Working borrowed gear without a lecture or an inflated claim.

### Vivian Voss toward the others

- Toward Jackie Tree. Feels: Genuine attraction mixed with irritation at evasiveness. Wants: A clear answer and reliable collaboration.

- Toward Bunny Easter. Feels: Warm respect for her eye and social courage. Wants: An imaginative co-promoter who distinguishes the real event from Milo's promises.

- Toward Frankie Maplewood. Feels: Respect with friction over who decides the room's presentation. Wants: Clear constraints and freedom within them.

- Toward Mr. Stringer. Feels: Skeptical amusement with no desire to indulge his assumptions. Wants: Respectful treatment and a practical decision.

- Toward Milo Pennant. Feels: Enjoys the banter; distrusts his business promises. Wants: Accurate numbers, correct credit and delivery of what he offered.

- Toward Rita Stringer. Feels: Creative kinship and admiration for her social intelligence. Wants: A distinctive contribution and a partner who claims authorship.

- Toward Felix Bunt. Feels: Respects his craft; winces at his theatrical sales pitch. Wants: Safe, adaptable equipment and an honest limit.

### Rita Stringer toward the others

- Toward Jackie Tree. Feels: Amused affection and concern for his exhausting evasions. Wants: Honesty with his housemates and help with her own plan.

- Toward Bunny Easter. Feels: Fondness grounded in respect for her emotional intelligence. Wants: A willing co-organizer with her own voice.

- Toward Frankie Maplewood. Feels: Mutual respect enlivened by their different methods. Wants: A workable plan that leaves room for delight.

- Toward Mr. Stringer. Feels: Affection, frustration and a wish to be seen anew. Wants: Equal credit, private honesty and a willing dance partner.

- Toward Milo Pennant. Feels: Enjoys his vitality, distrusts his shortcuts. Wants: Useful help and a promise he can actually keep.

- Toward Vivian Voss. Feels: Delighted by her confidence and protective of her independence. Wants: Creative partnership and credit for her ceramic supper service.

- Toward Felix Bunt. Feels: Finds him funny and recognizes unacknowledged skill. Wants: A reliable courtyard mechanism and someone willing to rehearse its cue.

### Felix Bunt toward the others

- Toward Jackie Tree. Feels: Wants his friendship, resents being rushed. Wants: An attentive assistant who follows the agreed procedure.

- Toward Bunny Easter. Feels: Grateful for her interest and anxious to impress her. Wants: A patient demonstration audience and honest feedback.

- Toward Frankie Maplewood. Feels: Wary admiration for someone who checks his work. Wants: A clear job brief and acknowledgment when he gets it right.

- Toward Mr. Stringer. Feels: Defers to the client but dislikes haggling and shortcuts. Wants: Approval for necessary repairs and payment for agreed work.

- Toward Milo Pennant. Feels: Likes his enthusiasm, distrusts how he handles equipment. Wants: Returned gear, accurate labeling and credit for the working setup.

- Toward Vivian Voss. Feels: Professional admiration with fragile pride. Wants: A design request that respects technical limits.

- Toward Rita Stringer. Feels: Feels understood and enjoys her theatrical instincts. Wants: A real cue to perform and sincere recognition.

### Audience relationships

The studio audience is a collective world-role rather than a ninth named principal. It can report what is visible or audible from the seats, never private offstage information. Its participation in P05 and P12 obeys the same puzzle-state rules whether audience sound is On or Off.

- Jackie Tree toward the audience: Feels flattered, then self-conscious. Wants a useful perspective and a chance to recover gracefully. Audience toward Jackie Tree: Feels affection for his effort and impatience with evasion. Wants him to make a choice and own it.

- Bunny Easter toward the audience: Feels energized and treats spectators as guests. Wants an honest response to her introduction. Audience toward Bunny Easter: Enjoys her warmth and notices her insight. Wants her contribution acknowledged.

- Frankie Maplewood toward the audience: Feels watched rather than helped. Wants a quiet, fair hearing for an actual practical problem. Audience toward Frankie Maplewood: Respects her precision and anticipates her dry payoff. Wants her to allow a little spontaneity.

- Mr. Stringer toward the audience: Feels important until laughter unsettles him. Wants visible approval of his respectable image. Audience toward Mr. Stringer: Sees his contradictory standards. Wants him to honor the condition he stated aloud.

- Milo Pennant toward the audience: Feels he has found his ideal market. Wants applause, willing guests and proof that he belongs. Audience toward Milo Pennant: Enjoys his bravado but expects a payoff. Wants one boast turned into a real contribution.

- Vivian Voss toward the audience: Feels comfortable presenting work, dislikes being reduced to a romantic spectacle. Wants useful feedback. Audience toward Vivian Voss: Admires her assurance and craft. Wants a clear account of what she is offering.

- Rita Stringer toward the audience: Feels delight at having her own audience. Wants her name and contribution heard. Audience toward Rita Stringer: Enjoys her social intelligence. Wants her to claim the spotlight she keeps giving away.

- Felix Bunt toward the audience: Feels thrilled and terrified by a live demonstration. Wants a fair test and applause for what works. Audience toward Felix Bunt: Enjoys his grand buildup but roots for genuine competence. Wants a safe, legible effect.

The audience’s reactions never decide anyone’s romantic consent, test an orientation, certify a repair’s safety, or grant the household’s agreement. Jackie’s direct observations and the characters’ own commitments resolve those matters.

## Visual reference gallery

All sixteen supplied examples appear below in their attachment order, with their original proportions and visible source markings preserved. “Observed” describes the supplied image; “Proposed application” is an original-game design choice. The first six examples primarily inform adventure rendering and presentation; the remaining examples inform portrait treatment, period setting, costume, ensemble performance, and graphic framing. The original files are retained in the project Library folder. Inclusion as a design reference does not establish production reuse rights; provenance and permissions remain subject to the existing release review.

### V01 Warm lights against blue night

![Embedded source image 3](embedded-images/image14.png)

Observed: A dense pixel-rendered wooden scene contrasts cobalt shadows and roof planes with gold lamps, rust-red walls, and warm floor reflections. Small, differently shaped figures occupy distinct levels. Promotional logos overlay the supplied image.

Proposed application: Use warm light pools and cooler peripheral shapes to organize the house and courtyard. Preserve clear actor staging within textured backgrounds; do not carry over the pirate setting or logo overlays.

Original reference V01: image(20261004-154616).png

### V02 Daylight framing and readable dialogue

![Embedded source image 4](embedded-images/image5.png)

Observed: Bright cyan water and sky, leafy greens, a sandy path, and dark foreground foliage frame two strongly contrasting figures. White dialogue with a dark outline remains conspicuous over the scene.

Proposed application: Give outdoor scenes layered depth and uncluttered walking areas. Set high-contrast dialogue apart from scenery; use original character proportions and seaside-house geography.

Original reference V02: image(20261004-154617).png

### V03 Night lighting and complete verb interface

![Embedded source image 5](embedded-images/image16.png)

Observed: Blue-violet rock and darkness contrast with yellow-green reflected light and a small amber lantern. A curved bridge creates a strong silhouette. A separate black lower panel holds purple verbs, a sentence line, and large inventory icons; visible scanlines texture the supplied capture.

Proposed application: Borrow light hierarchy, separated interaction space, and clear icon shapes. Treat scanlines as a reference-image treatment rather than a required game filter; keep UI colors and typography accessible.

Original reference V03: image(20261004-154619).png

### V04 Painterly pixel portrait detail

![Embedded source image 6](embedded-images/image11.png)

Observed: Two large illustrated faces have softly shaded skin, bright eyes, readable hair shapes, and lavender-white costume detail against a deep blue starry field. This close portrait has far more facial detail than the small gameplay figures.

Proposed application: Use this difference in scale to inform expressive freeze-frame portraits. Render original faces and period clothing; do not force gameplay sprites to carry portrait-level detail.

Original reference V04: image(20261004-154620).png

### V05 Ensemble silhouettes above a stable HUD

![Embedded source image 7](embedded-images/image6.png)

Observed: A bright outdoor lineup varies height, width, stance, and saturated costume colors. A darker foreground and black lower interface separate figures, white outlined dialogue, the purple verb grid, sentence line, and inventory.

Proposed application: Make each original cast member identifiable at room scale through silhouette, posture, and color grouping. Retain the nine-verb interaction grammar and clear scene/HUD separation without copying interface artwork.

Original reference V05: image(20261004-154622).png

### V06 Textured room with large practical props

![Embedded source image 8](embedded-images/image4.png)

Observed: Warm stone, worn plaster, a large foreground barrel, a circular wall prop, and angled wooden furniture form a compact pixel-art room. Three figures remain distinguishable against the material texture; verbs and inventory sit in a separate dark panel.

Proposed application: Use readable large prop contours for the gate, serving hatch, and folding display. Reserve high-detail texture for surfaces that do not compete with required hotspots.

Original reference V06: image(20261004-154623).png

### V07 Illustrated ensemble badge and warm lettering

![Embedded source image 9](embedded-images/image8.png)

Observed: Three smiling illustrated portraits overlap a circular gold, orange, and rose-colored badge with stars. Large curved decorative lettering and grainy print texture create a warm promotional illustration, distinct from the gameplay screenshots.

Proposed application: Use the warmth, overlapping portrait rhythm, and restrained print texture for original credit cards or title art. Do not reproduce the pictured faces, badge composition, stars, or existing show lettering as a finished logo.

Original reference V07: image(20261004-154624).png

### V08 Photographic cast grouping and costume blocks

![Embedded source image 10](embedded-images/image2.png)

Observed: A photographed trio forms a compact overlapping group below large white decorative lettering on a cool blue-violet field. A red patterned top, striped polo, light ringer-style shirt, dark trousers, and distinct hair shapes create separate color blocks. Printed names and packaging marks are present.

Proposed application: Study broad collar shapes, garment contrast, and friendly group spacing for original costumes and ensemble framing. The package typography, credited names, faces, and marks remain reference content.

Original reference V08: image(20261004-154625).png

### V09 Shared prop and warm lived in room

![Embedded source image 11](embedded-images/image10.png)

Observed: Three people gather around a corded telephone on a patterned sofa. Honey-colored wood, wicker furniture, warm carpet, plants, and shelving surround pale blue, navy-cream, magenta, and rust clothing. Leaning poses focus attention on one shared prop.

Proposed application: Stage household conversations around a visible common task or object. Combine warm set materials with distinct clothing blocks, while keeping the original house layout and characters.

Original reference V09: image(20261004-154741).png

### V10 Physical comedy as a readable group shape

![Embedded source image 12](embedded-images/image18.png)

Observed: Three people overlap in a broad couch-based physical-comedy pose, with the central figure held across the others. Pale blue, red-orange, and light plaid garments separate limbs against a densely patterned sofa, plants, and warm curtains.

Proposed application: Design original cooperative-comedy key poses with a clear overall silhouette and distinct costume values. Preserve readability when bodies overlap; do not reproduce this specific staging or add it as a new puzzle.

Original reference V10: image(20261004-154742).png

### V11 Large prop silhouette and contrasting reactions

![Embedded source image 13](embedded-images/image13.png)

Observed: A large cardboard box obscures much of one standing figure, beside two plainly readable reaction poses. A long blue dress and pale collared shirt with dark high-waisted trousers contrast against warm wood, wicker, and green plants.

Proposed application: Use an oversized original prop to establish a clear comic silhouette, with reactions legible beside it. This is a composition reference, not a requirement for undressing, the same gag, or an added scene.

Original reference V11: image(20261004-154744).png

### V12 Faces above one broad color shape

![Embedded source image 14](embedded-images/image15.png)

Observed: A large orange blanket groups three seated figures into one warm foreground shape. Their separate faces and eye directions carry the interaction above it, with patterned upholstery and muted plants behind.

Proposed application: Simplify busy ensemble moments into a few large color shapes, allowing eyes, brows, head angles, and hand gestures to carry contrast. Use original framing rather than re-creating the photographed situation.

Original reference V12: image(20261004-154745).png

### V13 Full body costume and posture contrast

![Embedded source image 15](embedded-images/image12.png)

Observed: A long plum outfit with a loose patterned outer layer contrasts with a dark athletic jacket, striped shorts, tube socks, and sneakers. One figure gestures at the chest while the other folds their arms. Warm carpet, a patterned sofa, and an arched doorway establish depth.

Proposed application: Give original cast members different garment lengths, collar profiles, stance, and gesture habits. Translate period clothing into readable sprite silhouettes without copying branded details or actor likenesses.

Original reference V13: image(20261004-154746).png

### V14 Conversational hands and quieter clothing values

![Embedded source image 16](embedded-images/image3.png)

Observed: Two seated figures hold flat cards or photographs and look toward the shared material. Taupe and cream clothing allows their hands, faces, and the rectangular props to stand out within a warmly lit, patterned room.

Proposed application: Use quieter costume or background values during clue exchanges so a card, slate, or pointing hand remains readable. Draw original clue props at a scale suited to inspection.

Original reference V14: image(20261004-154747).png

### V15 Four person reaction line and color separation

![Embedded source image 17](embedded-images/image17.png)

Observed: Four standing figures occupy one conversational plane, differentiated by pink, tan, gray-green, and cream garments. A document held between the right-hand figures and their differing head angles organize attention. The warm interior includes an arched opening and small framed decoration.

Proposed application: Stage multi-person conversations so the active speaker, listener, and shared object are apparent. Use distinct color/value groups and original door placement rather than reproducing the photographed set.

Original reference V15: image(20261004-154749).png

### V16 Cutout ensemble against bold graphic rays

![Embedded source image 18](embedded-images/image1.png)

Observed: A photographic trio overlaps broad cream, peach, orange, and red radiating shapes beside a dark blue rectangle containing white decorative show lettering. The clean graphic field differs from both the textured interiors and pixel-art backgrounds.

Proposed application: Use original radiating shapes, strong contrast, and uncluttered name space as one option for freeze-frame credit cards. Retain the eight existing introduction actions and exact character names; develop a separate original title treatment.

Original reference V16: image(20261004-154750).png
