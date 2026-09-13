# Local QA — 2026-09-13

## Verified

- `npm test`: nine tests passed, including exact variant choice, line-key removal validation, inventory error messages, native-template rendering, empty search results, reference product/photo ordering and the local commerce adapter.
- `npx shopify theme check`: zero errors. Twenty-one warnings remain in inherited Horizon files; no Cellulaire section/snippet offenses.
- `node tools/audit-links.mjs`: 11 routes, 18 unique internal links, 28 referenced assets, zero failures (fixtures and local filesystem only).
- In-app browser: 11 routes at 1440, 1280, 900, 390 and 320 widths; 55 checks found no horizontal overflow or broken loaded images, and exactly one H1 on each route.
- Visual inspection of home, story and contact on desktop/mobile. After the final mobile banner and routine changes, the home was checked again at 390 and 320.
- Browser interactions: mobile navigation opened and focused its first link; unavailable 100 ml variant disabled Add to bag and displayed $48; available 50 ml variant added successfully; cart quantity 1 -> 2 updated subtotal $28 -> $56; removal showed empty bag; Signature Set added as its own line with $95 subtotal; Wholesale selected the matching contact topic; message counter updated; local form displayed explicitly simulated success; FAQ answer expanded. No captured console errors/warnings on these flows.
- `npx shopify theme package`: `Cellulaire-1.0.0.zip` produced.

## Still required

Native Shopify-store installation, published page/blog existence, product/collection selection, live inventory/variant behavior, contact email delivery, shipping/returns data and checkout verification. The store URL/access has not been provided.

Exact typography and full-resolution matching need the original font and unflattened photography. The supplied PDF concept is a flattened image; the homepage mobile hero keeps the original composite banner with a coded accessible link overlay. The Our Story portrait uses the original composite caption and separate reference crops for desktop/mobile. Other text/forms render natively. The home/story PDF screenshots truncate before the full page ends, so the shared footer follows the complete contact reference.

Continuation verification: corrected the Our Story portrait crop and product/photo order; restored visibility of all four bottles in the mobile formulas image. Rechecked home/story/contact/science at the five viewports (20 checks), with no overflow or broken loaded images and no captured browser console errors/warnings. The corresponding product-order test failed before the fix and passed afterward.

These checks establish local implementation progress; they do not establish that the full requested store or exact-fidelity goal is complete.

## Supplied PNG implementation pass

- Extracted imagery directly from the three supplied PNG attachments; source paths and crop boxes are recorded in asset-provenance.json.
- Rebuilt desktop Home/Our Story/Contact banners and mobile Home/Our Story banners from their supplied artwork. Accessible native headings/descriptions and working button overlays remain. Clean uploaded images enable visible native editable text. The mobile formulas photo uses the full four-bottle scene from branding slide 13 to avoid the truncated phone crop.
- Refined serif typography, mobile heading sizes, values spacing, native compact product links and desktop story/mission columns.
- Fixed a zero-height banner link overlay caught by an actual browser click. Verified the home banner navigates to /collections/all on desktop and mobile, and the Our Story banner scrolls to its section.
- The preview now resolves the actual bundled native product/collection handle fallbacks. A new test verifies four product/collection links and the distinct signature-set variant. Selected editor resources still take precedence.
- Fixed duplicate document titles caused by the inherited meta-tags snippet; all routes now have one meaningful title.
- Nine tests passed. Theme Check completed with exit code 0 using the bundled Node runtime: zero errors, 21 inherited warnings, no Cellulaire offenses. The system Node runtime had an unrelated shutdown assertion after producing its report; the bundled runtime completed normally.
- Rechecked 55 route/viewport combinations. After the final layout and overlay corrections, rechecked the four changed pages at all five widths (20 checks), including nonzero usable banner link areas: no overflow or broken loaded images.
- Verified one face mist adds to the local bag with a $28 subtotal, Wholesale selects its contact subject, the character counter updates, and the local contact endpoint displays simulated success. No captured browser console warnings/errors.
- Packaged the updated native Shopify theme; local fixtures, developer tools and documentation are excluded.

Product-media completion pass: mapped the four known face mists and Signature Set to their corresponding bundled imagery in product cards, main galleries and cart lines when Shopify media is absent. A regression test removes media for each of the five products and verifies gallery/cart photo identity and a valid main-image target. Browser checked the five product pages at 1280/390/320 (15 checks), with no overflow or broken loaded images, then added Hydration to the local bag and verified its photo and $28 subtotal.

## Full-width correction

The supplied complaint screenshot showed the storefront capped at 1280 px with large empty side gutters. At a 1920 px browser viewport (1905 px usable width), measured header/hero width was 1280 px with 312.5 px left/right margins. Removed the `.wrap` width cap and automatic centering: all outer page containers now use width:100% with no maximum. Prose remains readable by constraining the inner text to 72ch inside a full-width section.

Verified 11 routes at 2560/1920/1440/1280/900/390/320 (77 checks). Every rendered `.wrap` container begins at x=0 and matches available viewport width within 1 px. No horizontal overflow or broken loaded images. Inspected desktop and mobile screenshots and rechecked the home banner link at both sizes. Packaged the updated stylesheet in the native theme ZIP. This correction is verified locally; it does not change the existing external-store installation status.
