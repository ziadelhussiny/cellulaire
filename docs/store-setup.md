# Installation and store data

This repository is a native Shopify theme. Local preview fixtures in `tools/fixtures.mjs` never ship in the theme. Prices, inventory, cart, checkout and contact delivery are supplied by Shopify on the real store.

1. Upload the packaged theme as an unpublished theme, or run `npx shopify theme dev --store YOUR-STORE.myshopify.com` after signing in to the intended store.
2. Create published Online Store pages with handles `our-story`, `contact`, `faq`, `science`. Assign templates `page.our-story`, `page.contact`, `page.faq`, `page.science` respectively. Create a blog with handle `journal`.
3. In the home skin-need section, select each real collection. In Best Sellers and the Our Story collection section, select each matching product. A missing resource links to the all-products collection; no fictional variant IDs are submitted.
4. Select the actual Signature Set product in The Complete Routine. The displayed price and compare-at price come from that product. Update the promotional badge to match the real offer.
5. Set customer-care email, phone, WhatsApp, business hours, social URLs and menus. Phone and social links are omitted until configured; no placeholder links are published. Enable customer accounts in Shopify if needed.
6. Review all FAQ answers and shipping/return policies against actual operations. Add shipping and returns copy in the product section. Optional product metafields: `custom.short_description`, `custom.ingredients`, `custom.how_to_use`.
7. Replace bundled extracted asset fallbacks with original full-resolution photographs through image pickers when available. The source PDFs contain flattened illustrations, including decorative text inside some photo regions. Bodoni Moda is the closest supplied implementation font, not a verified original brand font. The original font file/name and unflattened photos are still needed for exact fidelity.
8. Verify the unpublished theme in Shopify on desktop and mobile: all navigation, collection selections, product variants, stock failures, add to bag, quantity changes/removal, checkout handoff, contact delivery and legal links. Local preview cannot verify these external services.

The homepage mobile hero uses the supplied composite banner to preserve its original crop and typography, with an accessible heading and a real clickable link over the banner button. Uploading a clean mobile photo automatically enables the native visible heading and button. The Our Story portrait also retains its original composite caption and uses distinct desktop/mobile crops. Its accessible caption remains in HTML, and uploaded clean images enable the visible native caption separately for each viewport. Other page text, forms and controls render natively.

The homepage testimonial reproduces a quote shown in the supplied mockup. Confirm it is approved for publication and replace/add actual reviews in the theme editor. The PDF crops for the home and story pages end before the complete page footer; shared contact-page footer styling is used for those pages.

Publishing the theme is a separate final deployment action after native-store verification.
