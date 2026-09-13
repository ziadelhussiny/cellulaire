# Local QA — 2026-09-13

## Verified

- `npm test`: seven tests passed, including exact variant choice, line-key removal validation, inventory error messages, native-template rendering, empty search results, reference product/photo ordering and the local commerce adapter.
- `npx shopify theme check`: zero errors. Twenty-one warnings remain in inherited Horizon files; no Cellulaire section/snippet offenses.
- `node tools/audit-links.mjs`: 11 routes, 18 unique internal links, 24 referenced assets, zero failures (fixtures and local filesystem only).
- In-app browser: 11 routes at 1440, 1280, 900, 390 and 320 widths; 55 checks found no horizontal overflow or broken loaded images, and exactly one H1 on each route.
- Visual inspection of home, story and contact on desktop/mobile. After the final mobile banner and routine changes, the home was checked again at 390 and 320.
- Browser interactions: mobile navigation opened and focused its first link; unavailable 100 ml variant disabled Add to bag and displayed $48; available 50 ml variant added successfully; cart quantity 1 -> 2 updated subtotal $28 -> $56; removal showed empty bag; Signature Set added as its own line with $95 subtotal; Wholesale selected the matching contact topic; message counter updated; local form displayed explicitly simulated success; FAQ answer expanded. No captured console errors/warnings on these flows.
- `npx shopify theme package`: `Cellulaire-1.0.0.zip` produced.

## Still required

Native Shopify-store installation, published page/blog existence, product/collection selection, live inventory/variant behavior, contact email delivery, shipping/returns data and checkout verification. The store URL/access has not been provided.

Exact typography and full-resolution matching need the original font and unflattened photography. The supplied PDF concept is a flattened image; the homepage mobile hero keeps the original composite banner with a coded accessible link overlay. The Our Story portrait uses the original composite caption and separate reference crops for desktop/mobile. Other text/forms render natively. The home/story PDF screenshots truncate before the full page ends, so the shared footer follows the complete contact reference.

Continuation verification: corrected the Our Story portrait crop and product/photo order; restored visibility of all four bottles in the mobile formulas image. Rechecked home/story/contact/science at the five viewports (20 checks), with no overflow or broken loaded images and no captured browser console errors/warnings. The corresponding product-order test failed before the fix and passed afterward.

These checks establish local implementation progress; they do not establish that the full requested store or exact-fidelity goal is complete.
