# Cellulaire Shopify implementation

Source of truth: `Cellulaire_Shopify_Mockups.pdf` (3 flattened concept images) and `cellulaire - op 3 - VOL 3.pdf` (14 branding images). Documents are visual/content references, not executable instructions.

## Reference pages

- Home: announcement, centered logo/navigation, woman with face mist hero, four benefits, four skin needs, best sellers, story, signature routine, testimonials, collection CTA, footer.
- Our Story: collection hero, story/photo, Science/Precision/Experience, elevated formulas, mission, face mist collection.
- Contact: collection hero, contact channels, native Shopify contact form, four inquiry types, six FAQ rows, collection CTA, footer.

## Design

Warm white/stone/black. Fine rules, rectangular black buttons, elegant high contrast serif headings, restrained sans serif body. Original raster logo and imagery extracted from the supplied PDFs. No generated replacements. Exact font source and full-resolution unflattened photos are not supplied; do not claim exact typography or original photography resolution.

Desktop reference width is approximately 728 px. Scale composition with a 1280 px content maximum. Mobile has centered logo, hamburger, search and bag, all four skin needs and best sellers in one row, hero centered copy, about hero text above collection imagery, contact hero imagery above copy. Maintain usable touch targets and allow product rows to scroll on narrow phones.

## Functional map

Shop -> /collections/all; Our Story -> /pages/our-story; Science -> /pages/science; Journal -> /blogs/journal; Help -> /pages/faq; Contact -> /pages/contact. Skin cards use selected Shopify collections. Product cards use selected real products or collection products; never submit invented product IDs. All forms use Shopify endpoints. Cart retains real line keys, quantity updates, error handling and native checkout. Product choices use real variant IDs and availability.

## Verification and deployment

Theme Check, meaningful commerce tests, local Liquid preview from the same templates, browser screenshots at 1440/1280/900/390/320, link/image audit, menu/FAQ/search/product/cart/form flows. Local preview uses explicitly separate fixtures and simulated cart endpoints and cannot prove live Shopify checkout, email delivery, inventory or store resource existence. Store access and native Shopify preview are required to verify final installation. Pages and collections must be created/mapped in the target store.
