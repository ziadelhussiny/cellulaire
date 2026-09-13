# Cellulaire Shopify theme

Native Shopify Liquid sections and JSON templates based on the supplied Cellulaire website mockup and branding PDFs.

```powershell
npm install
npm run preview
npm test
npm run check
npm run package
```

Local preview: http://127.0.0.1:9292. It renders the native theme templates with separate local fixture data and simulated commerce. No live order is created and no email is sent.

See [design contract](docs/design-contract.md), [store setup](docs/store-setup.md) and [asset provenance](docs/asset-provenance.json).

Reference-page templates: `index`, `page.our-story`, `page.contact`. Supporting templates: `collection`, `product`, `cart`, `search`, `page.science`, `page.faq`, `blog`, `article`, `page`, `404`, `list-collections`.

Store installation and resource mapping remain necessary. Unflattened imagery and the actual brand font are necessary to finish exact visual fidelity. Inherited Horizon sections remain in the source tree; the active storefront templates use the Cellulaire sections.
