# Frozen opening asset integration, 2026-10-09

Final pixels are under `proof/export-r1/resources/245.view.bin` through252. Rebuild inputs are `tools/export-config-all-eight-r1.json`, `GENERATION-PROVENANCE.json`, the referenced masters/prompts, explicit selection masks, and exact retained palette/font/background references. `PORTABLE-SOURCE-INVENTORY.json` records the complete required file closure with byte counts and SHA256 hashes.

The composer imported manifest SHA256 `37614c005eb1b9b70631a79f6ec447e7ad63a2cd4648c51948f24a2c66f47679`. Before freeze notification, the producer added only two title-composition metadata fields: `shared_title.scene_background_palette_index` and `shared_title.accent_rectangles`. The current producer manifest is `c54e3af6aa0aeb9fb5d93439be461fb5d1e7c8665ae121693c0e5d1191b4d21d`. Removing those two fields reproduces the imported manifest byte-for-byte under its canonical JSON serialization. Every resource/cel hash and existing actor/motif/name/prop geometry is identical. Neither manifest is rewritten after the freeze.

## Exact loop0 geometry

| View | Name | Common size | Draw | Bytes |
|---|---|---|---|---:|
|245|Jackie Tree|53×79|(105,56)|39431|
|246|Bunny Easter|55×79|(94,56)|47571|
|247|Frankie Maplewood|44×79|(96,56)|42952|
|248|Mr. Stringer|49×83|(94,52)|50022|
|249|Milo Pennant|65×78|(85,57)|54039|
|250|Vivian Voss|44×80|(98,55)|62113|
|251|Rita Stringer|45×80|(92,55)|45030|
|252|Felix Bunt|49×80|(97,55)|44082|

Each loop0 has exactly eight distinct action cels. Every visible sole baseline is screen y134. A single source-anatomy scale is retained per character; crouches are not normalized. Transparent common bounds differ from historical lost resources, and Stringer's natural upright/lean variation spans the83-pixel union. No actor scale was reduced to satisfy a byte budget. Largest payload is62113, leaving3422 bytes.

Loop1 is the freeze motif and loop2 the exact original-font name. Draw their actual manifest rectangles. Paint freeze panel `[166,0,320,144)` with palette10; draw motif/name, then static prop if present, then loop0. Jackie begins cels at0/18/36/54/72/84/96/108; others at0/24/48/60/72/84/96/108. Freeze cel7 at120 through359. Reduced motion uses cel7.

## Extra loops that the renderer must draw

- VIEW248 loop3 cel0: two chairs,71×38, draw(83,97) before loop0 on every action/freeze frame. These are the exact visible cel0 chair pixels, extracted once. Explicit actor-selection masks remove every later chair copy. Cel0 actor plus original chairs recomposes pixel-for-pixel to the source registration; no hidden chair pixels are synthesized.
- VIEW251 loop3 cel0: complete matched bench,34×36, draw(82,93) before loop0 on every action/freeze frame. This is a separate newly generated reconstruction. Its previously occluded right portions are new pixels, never described as recovered. One uniform prop scale36/666 maps source anchor(218,578) to screen(82,93). The eight actor masks remove the changing bench images from the accepted one-handle Rita sheet.
- VIEW250 loop3 cel0: common title,288×72, draw(16,30), cards0and9 only. No stable prop belongs to Vivian. Fill title scene with palette10; accent rectangles are `[18,10,302,12)` index4, `[40,116,280,119)` index4, and `[80,125,240,127)` index37. This matches the recovered title compositor.

Names/title are unmodified font0 glyph shapes at integer scales. Palette999 is unchanged; all exported opaque indices are0–217 and transparent index255. Backgrounds remain300/101/101/302/304/100/302/303 in cast order. Garage304 is drawn alone; no301 or mutable world overlay is used. Controls remain outside y0–143.

## Review and verification

The combined64-pose sheet, eight freeze composites and title proof are under `proof/export-r1/review/`. Per-character native background contacts and four-background transparency proofs remain under `proof/export-r1/proof/<slug>/`. The parent reviewed all64, the freeze treatments and title. Bunny cel3 specifically hides the eye line behind the upper sun edge while leaving nose/mouth visible; clear eyes appear in cels4–7. This satisfies eye occlusion without requiring the entire face to disappear.

Nine focused tests pass, including the independent strict SCI decoder, deterministic exports, font-bit equality, alpha/palette constraints, clipping/duplicate rejection, single-scale crouch preservation, exact original actor/prop partition, and explicitly new-prop replacement without changing actor pixels. Direct source/pixel checks cover all64 action cels, all83 packed cels and fixed sole y134. Resource bytes are unchanged by preview/metadata updates.

This is offline asset/source closure. Native timing, shared-score playback, controls, replay, save/load and full-game acceptance remain the coordinator's gates. No native player or game build was launched by this asset worker. Audience102/103 work is separately owned and excluded from this eight-action closure.
