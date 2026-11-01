# WordPress build runbook

Goal: the live WP pages are visually indistinguishable from the approved mockup. Work in the user's browser (Growth100x Chrome profile) on the WP install they provide.

## Before touching anything

- Confirm: is this a fresh/staging install or a live site with existing pages? On a live site, build new pages as **drafts** and never modify existing published content without explicit per-page confirmation.
- Inventory: theme (Elementor-based? block theme?), installed plugins, existing global styles. Prefer working with what's installed; confirm with the user before adding plugins (each one is a maintenance liability). Typical minimal stack: Elementor (if present/preferred), a code-snippets manager (WPCode), an SEO plugin (Yoast/RankMath) if none exists.
- Take note of WP version + backup status; if no backup exists on a live site, ask the user to trigger one first.

## Translating the mockup

1. Set **global tokens first** (site settings: colors, fonts, container widths matching the mockup's DNA sheet) so every page inherits them — never per-element one-off styling that drifts.
2. Build page by page: mockup sections → Elementor sections/containers (or block patterns on block themes). Reuse: build a section once, save as template, reuse across pages.
3. Where the mockup's custom CSS/JS exceeds builder capability (bespoke hovers, count-aware grids, animations), inject via the snippets manager as site-wide or page-scoped code — keep every snippet named and logged. On Elementor-canvas pages, PHP content filters don't run — DOM-inject via JS snippets instead.
4. Grids: `auto-fit/minmax` leaves orphan rows on some item counts — set column counts from item count via JS (3/4/5/N) with `setProperty(..., 'important')` when builder CSS resists.
5. Mobile: replicate the mockup's mobile behavior explicitly in the builder's responsive controls — builders' automatic stacking rarely matches a designed mobile view.

## Launch checklist (all before calling it done)

- Every page: title tag + meta description, one h1, headings hierarchy preserved from mockup, images with alt text, favicon, OG/social card meta.
- Schema: Organization/LocalBusiness sitewide + page-appropriate types (Service, FAQPage) — via SEO plugin or a snippet.
- Forms wired to a real destination (email/CRM) and **test-submitted successfully**.
- Performance sanity: no unused heavy plugins, images compressed, caching active if available.
- Permalinks clean, sitemap generating, robots.txt sane, site not accidentally set to "discourage search engines" (the classic staging-to-live killer — check it explicitly).
- **Visual verification**: load every published page in the browser at desktop + mobile widths and compare against the mockup — a 200 response is not "done", seeing it match is. Screenshot the pages for the delivery message.

## Handover

Tell the user what was built (pages + URLs), snippets added (names + where), plugins added (if any, with why), and the remaining client-side items (DNS, content confirmations, form recipient). Suggest running the analytics-setup-engine and seo-audit-engine as natural next steps for the same client.
