# Companion walking art: additive resource contract

Generated 2026-10-07. This is new original editable art, not recovered lost animation. Source-format and offline geometry gates passed. Native gameplay, input, animation timing, DrawCel scaling, occlusion, and final visual acceptance remain pending in the integrating host.

## Resources

| Actor | New walking view | SHA-256 | Payload bytes |
|---|---:|---|---:|
| Frankie | 237 | `51b274b900b691fb05395de0d1d7ee20950c5398c7cf2e2624d4f9a8a92be0d4` | 42010 |
| Bunny | 238 | `3149ff4bff8a0862cd1ce36018bb19c086c562ff4bb7d4d00acd442c5e911225` | 42010 |

Both are literal SCI1.1 payloads, without resource-map or patch-file prefixes. Every cel is 52×80, displacement (0,0), clear key 255, palette999. The nominal local foot anchor is (26,78), row79 is clear. Two loops are stored explicitly: 0 right, 1 left. Cel0 is an exact indexed copy of that actor's corresponding old closed-mouth idle. Cels1–4 are new contact, passing, opposite contact, opposite passing candidates. Each holds six host game ticks; one cycle is24 ticks. Contacts are1/3. Both horizontal directions support travel and reversal. No new front/back/north/south facing is provided.

Old Frankie218 and Bunny219 remain byte-identical. Keep their dialogue mouth0–2 behavior. Frankie is native object8, speaker3; Bunny is native object2, speaker2. On stationary or restored boundaries, use original218/219, with cel0 outside speech. Stop-to-idle intentionally restores the old pose exactly. New left gait cels use x→52−x (mirror plus one), while old left idle is copied directly.

## Art and provenance

Frankie preserves the reference's auburn hair, face and closed mouth, ochre blouse, olive flared trousers and brown shoes. Bunny preserves her blonde bob, closed mouth, red blouse, cream flared trousers and brown shoes. Both retain the reference proportions and muted palette. The newly generated pixels are newly authored renderings of those identities, not pixel-identical upper-body copies. Identity and gait are visually reviewable in the all-cel sheets. No Jackie body pixels were incorporated.

Selected editable masters: `masters/frankie-walk-v4.png` and `masters/bunny-walk-v2.png`. Earlier attempts and every prompt are retained. The initial Frankie repeat-leg/high-knee candidate was banked separately, then refined. The third Frankie attempt failed to improve leg crossover and was rejected; v4 corrects passing silhouettes. Generated masters are flat transparent PNGs. All20 indexed PNG cels remain editable.

Image generation produced supported local PNG files, which were verified and copied into this project. `PROVENANCE.json` records the exact originals, prompts and source hashes. Replaying a generative prompt does not guarantee identical pixels; rebuilding the retained masters into native views does.

## Deterministic build and proof

Requirements: Python3, Pillow and NumPy. Font-based review sheets use DejaVu Sans at the recorded system path; native resource generation itself uses no external renderer or network service.

Run `python tools/import_masters.py` from this directory. It reads `authoring.json`, the selected masters and pinned palette999. Operations are crop, one uniform scale per character, nearest-neighbor sampling, integer canvas registration, alpha threshold128, squared-RGB nearest-palette matching excluding255, and mirror-plus-one. No procedural limb painting, body deformation or creative raster editing occurs in the importer. It writes indexed cels and native resources. Displacements remain zero; registration is baked into the fixed52×80 canvas.

The independent strict decoder checks offsets, record sizes, dimensions, transparency, literal bytes and absence of trailing data. Every decoded cel equals its PNG, and encode(decode(payload)) equals the original payload. A second complete import produced identical hashes for all20 cels and both views (`review/rebuild-identity.json`).

Run `python tools/preview_qa.py` for offline metrics and review artifacts. It checks the pinned original218/219 against the untouched source snapshot when this recovery tree is available. It writes all-frame geometry,200 route-anchor/view/loop/cel checks, all-prop-position overlap measurements, actual-background travel/return references, four representative courtyard layouts and looped GIF/APNG review animations. The review renderer is a deterministic approximation using nearest-neighbor scaling, not SCI runtime evidence. It does not implement native click routing, host ownership, save behavior or portal occlusion.

## Staging and measured limits

Keep the provisional meeting feet Frankie(76,130), Bunny(120,130), scale116. Both exact idle cels preserve the original staging behavior. All cels and facings are clear of opaque overlap with the gate, audience edge and chevron lane. The new gait expands beyond old idle bounds:

| At provisional feet | House arch control | Lower hatch control | Equipment credit control |
|---|---:|---:|---:|
| Frankie, maximum over all cels/facings |15|0|0|
| Bunny, maximum over all cels/facings |0|100|24|
| Bunny, idle0 in either facing |0|69|0|

The hatch rectangle contains1053 pixels; Bunny's69–100-pixel opaque overlap is in its lower area. Do not call the hatch pixel-clear. The source contract's old static all-cel hatch overlap69 was measured on mouth cels only. The broad equipment-control overlap is not the same as overlap with painted slate pixels; per-prop alpha overlaps are in `geometry-and-identity.json`.

The route worker reports ordinary interactions are disabled while moving, then final actors switch to exact old idle and gain controls beginning at y72. This is integration intent, not tested here. Preserve hatch access at y44–71, protected exit/equipment controls, named-object selection and keyboard/controller access. Never give the entire transparent actor canvas higher hit priority than a doorway or hatch. Screen is current native object81; plan is83.

Measured optional alternatives: Frankie(79,130) clears all protected rectangles for every gait; Bunny(117,130) clears equipment control for every gait but still has hatch overlap up to100. These are comparisons, not adopted changes. Because movement has no ordinary interaction and stops on the old idle, the provisional76/120 anchors can remain while the host explicitly handles draw depth and protected controls.

All200 tested native-sized offline projections have zero opaque pixels clipped beyond320×144. The proposed living kitchen sill(304,112), scale90, has a full transparent canvas extending2 pixels beyond the right edge; its painted pixels remain inside. Confirm actual SCI scaling/clip behavior.

## Cadence and portal boundaries

The looped courtyard GIFs/APNGs show two complete rightward cycles, exact idle stop, two complete leftward return cycles and exact idle stop at scale116. They use the route owner's proposed2 world pixels/game tick and six ticks/cel. GIF durations20/20/10ms repeat to give exactly100ms per six ticks at nominal60Hz; APNG uses1000/60ms. The lower-foot contact landmark spans are roughly23–26 screen pixels per half-cycle at scale116, close to the proposed24-pixel translation. This supports2px/tick as a candidate, not a foot-skating pass. Cels are held while the body moves; native playback must judge their apparent contact, bob and idle transition.

The three-room sheet illustrates actual living101, kitchen300 and courtyard305 backgrounds, both travel directions, original return anchors and proposed sill points. It intentionally does not erase an actor to fake crossing. Portal cuts/foreground masks, legal room-edge transfer, interpolation, cancellation/restore and native acceptance belong to host integration. An approach-point disappearance is not a doorway crossing. The lateral courtyard cadence animation is a visual review strip, not a gameplay route or collision/path acceptance.

## Allocation and acceptance

Coordinator reserved237/238. A03:33UTC read-only scan found no237/238 view payload in current host or route trees and no explicit current DrawCel use; resource types other than view do not collide with view IDs. Final assembled-map collision check is still required.245–252 and330/331 were not used.

Passed: retained master transfer, indexed palette/canvas/alpha/ground checks, exact idle copies, mirror-plus-one, independent native encode/decode identity, repeat-build identity, pinned original-resource integrity and offline200-case clipping.

Pending: assembled-map collision confirmation; native scale/depth/clip rendering; human animation timing and foot-skating acceptance; portal crossing; host travel/cancel/restore input and saves; all-layout named-object/keyboard/controller access. No host, game archive, save, desktop or GitHub state was changed by this art task.
