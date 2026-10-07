# Garage visual helper integration

New editable source fragment only. Append `visual-methods.sc.inc` inside the existing P05State class (script985, species7). Append the ten local arrays from `visual-locals.inc` to the original local declaration. Required controller properties and exact interfaces are listed in `interfaces.json`. Existing sources and resources were never edited.

## Main hooks

1. At the beginning of `uiHostWorldControls`, call `(p05 hWorldControls:)`; if it returns1, return immediately. This method includes the existing NOTES control. It deliberately returns0 on the apron so existing audience10/return11 controls remain in charge there.
2. At the beginning of `drawWorld`, call `(p05 hRenderWorld:)`; if it returns1, return immediately. Do not call `drawJack` a second time: this helper already draws Jackie exactly once at the right feet-depth position. Keep the existing outer render SetPort/Palette999, caption/HUD rendering, and final Graph12 flush.
3. Before movement for a garage target69, call `(p05 hCaptureTarget: obj)`. `hSelectedMark` starts1 and changes only on a verified full rectangle. Capture before Jackie moves, not at action commit. Keyboard focus uses the same focused control rectangle as pointer activation. On an apron never capture a garage mark.
4. Add Main's zero-argument `p05FocusMark` helper. See the exact method below. Replace the fixture name `p05Visual` with the actual Main property holding the P05 controller. This is the only extra Main method the visual fragment requires.
5. Garage-only, non-apron approach hooks should call `(p05 hApproachX: obj)` and `(p05 hApproachY: obj)`. All authored target approaches exactly match accepted geometry and y135..140.
6. In full label and short label methods intercept63..72 before legacy dispatch and call `hLabel` / `hShortLabel`. Full labels come from accepted text205 and each has its own persistent buffer. The compact labels are intentionally limited to five verified6px glyphs, fitting32x10. If using convenience object2/28/9/11 labels, apply them only in garage/non-apron so PORCH does not overwrite apron RETURN.
7. The art's porch exit is object11, but old Main.p02Exit has garage exit17. The host must explicitly route11 to room0 in garage/non-apron; leave apron11 as return-from-apron. This is a navigation hook, never an invitation.

Exact Main wrapper (shown with fixture controller name):

    (method (p05FocusMark &tmp i)
        (= i uiFocus)
        (if (or (< i 0) (>= i uiControlCount)) (return 0))
        (if (or (!= [uiActions i] 1) (!= [uiPayloads i] 69)) (return 0))
        (return (p05Visual hMarkAt: (/ (+ [uiLefts i] [uiRights i]) 2)
            (/ (+ [uiTops i] [uiBottoms i]) 2))))

## Bunny's actual room

Actual Main has these independent old paths, so changing just reachability is insufficient:

- `p02ObjectLocation` hardcodes object2 to room1 after P02 becomes available, otherwise0. Return the controller's authoritative `hBunnyRoom` instead when the P05 controller is initialized; keep old behavior before initialization.
- `livingPerson who` draws Bunny219 whenever who2 is requested. `drawLiving` calls it unconditionally. Guard `livingPerson` for who2 unless actual room is1. This preserves Frankie3 and the living-room depth sorting.
- `uiHostWorldControls` room1 unconditionally registers object2. Guard that registration using actual Bunny room1. Its room0 branch already calls `p02Reachable` for object2, so the authoritative object-location hook removes the obsolete porch hit target.
- `dialogueCanSpeak who` currently permits Bunny2 only in room1 or the pre-entry porch. Gate Bunny2 on actual room and allow room5/non-apron only when hBunnyRoom5. Preserve existing opening/movement checks. Mouth animation alone is not authorization for audible dialogue.
- Porch `drawWorld` has a pre-entry speaker2 mouth217 path, otherwise chooses view211 (pre-entry Bunny/window) or view215 (houseEntered empty window). After P02, houseEntered is true and view215 is already the empty-window convention: keep that background fixture. Do not add another219 overlay to porch. If a reconstruction lets Bunny leave before entry, gate only the pre-entry Bunny211/217 path by actual room0 and draw empty-window215 in its absence.

## Physical ownership and input priority

`hKitVisible` is true only for hPAOwner1/hPARoom5, so after authoritative loan publication to room4 all kit cels0..6 and8..13, font labels, and targets63..68/70/71 disappear from the garage. Cart7/object72 follows its distinct hCartOwner1/hCartRoom5. Marks14/15 remain floor fixtures. No completion, actor invite, item transfer, loan, cart movement, or contest state is generated here.

The accepted design requires small controls before the PA base and all hardware before actors, while Main.uiHit searches backward. Therefore the source carves the broad PA target around smaller hardware and carves actor rectangles around every authored hardware/mark/exit target. Registration order remains hardware-first, and exhaustive pixel ownership tests prove later actor entries cannot steal those targets. Carving stays constant when hardware is absent, leaving conservative gaps in the actor hit region rather than changing actor interaction semantics.

The controller must validate domain values before normal rendering: connected0/1, source0/1, aim0/1/2. These helpers read those values; they never clamp or correct domain state.

## Checks and limits

Run `python generate_fragment.py`, `python build_fixture.py`, `python tests/test_visual_helpers.py`, and `python tests/audit_emitted.py` in this directory. The isolated fixture compiles all seven modules from source; Main receives only a controller-pointer property and the focus-center wrapper. Its game routing is intentionally not replaced. The fixture executes actual emitted SCI instructions using the existing deterministic graphics/text kernel mocks, and reads the real accepted text205/font0/native art resources.

Nine tests cover all twelve hardware combinations, garage/apron ownership gates, immutable original domain methods, all exact target approaches, same-x/different-y mark selection, stale-pointer/keyboard focus capture, full-label pointer independence, compact font metrics, actor anchor/depth/speech gating, and every target pixel across eight kit/cart/Bunny visibility combinations. These tests establish emitted helper behavior and trace geometry; they do not establish native rendering, full Main action integration, click-to-walk collision acceptance, audio output, or native save compatibility.
