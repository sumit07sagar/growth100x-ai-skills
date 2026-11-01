---
name: website-engine
description: 'Mockup-first website production engine for pitching and building client sites. Given a company name, its industry, and a design direction ("more like Apple", "more like Amazon", "like stripe.com", any reference brand or URL), produce a premium single-file HTML mockup with real content — then, once the user approves it, build the full website: on WordPress (hands-on via WP admin/Elementor in the browser) or as a production-grade static site deployed to Netlify. Use this whenever the user asks for a website mockup, a landing page concept, a site design to pitch a company, says "build a website for X" or "make a mockup for X", names a company plus a look-and-feel reference, or wants a website built on WordPress or in code — even if they only describe the company and vibe without saying "mockup".'
---

# Website Engine

Two-stage pipeline: **mockup → approval → build**. The mockup is the product being sold — it must look like a finished premium website, not a draft. Never skip to the build without an approved mockup, and never show anything unstyled or generic; a raw-looking mockup loses the pitch.

## Inputs

Required: **company name**, **industry**, **design direction** (reference brand(s) or URL(s), or an adjective brief like "premium minimal" / "high-energy crypto").
Useful: services/products to feature, target audience + geography, existing logo/brand colors, sections wanted, competitor sites, the one action visitors should take (call, buy, book, signup).

Missing details are not blockers — research the company, infer the rest, and state assumptions when presenting the mockup.

## Stage 1 — Research (before any pixels)

1. **The company**: search for it — real services, locations, phone, reviews, existing site if any. Real content is the difference between a pitch that lands and a template. If the company is new/unfindable, generate credible industry-accurate content and mark it clearly as placeholder-for-review.
2. **The reference**: read `references/design-dna.md`, then extract the reference brand's design DNA — if it's a URL, actually fetch/visit it and codify what makes it feel the way it feels (type scale, spacing, color logic, layout patterns, motion). "More like Apple" means adopting its principles (restraint, huge type, whitespace, one idea per screen) applied to THIS company — never cloning content or copying protected assets/logos.
3. **The industry**: what do the 2–3 best sites in this niche always have (trust signals, pricing displays, booking flows)? Include the conventions, beat them on polish.

## Stage 2 — Mockup

Read `references/mockup-spec.md`, then produce ONE self-contained HTML file: the full homepage plus (as scroll sections or simple tab/anchor navigation) the key inner-page concepts. Real company content, working interactions (nav, hovers, mobile menu, accordion FAQs), fully responsive. Save as `Website Engine/<company>/mockup-v1.html`, present it, and iterate on feedback (v2, v3… — keep every version).

**Wait for explicit approval before Stage 3.** When presenting, ask which build path (WordPress vs code) if not already stated, and list any content assumptions needing correction.

## Stage 3 — Build

### Path A: WordPress
The user provides WP admin access (client install or staging). Read `references/wordpress-build.md`. Build pages matching the approved mockup via the browser (Growth100x Chrome profile) + code snippets. Confirm before installing plugins or changing themes on an install that has an existing live site.

### Path B: Code + Netlify
Read `references/code-build.md`. Expand the mockup into a production multi-page static site (each mockup section that represented an inner page becomes a real page), SEO/AEO-ready from birth, deployed to Netlify for a live link. (Cloudflare deploys are handled manually by the user — prep files, don't drive the CF dashboard.)

## Quality bar

- **Premium and bespoke, always.** No stock-template look, no lorem ipsum, no default-blue links, no unstyled anything. Every mockup should be pitchable at a $2k+ price point as-is.
- **Real content or clearly-flagged placeholders** — invented phone numbers/testimonials must be marked for replacement before anything goes live.
- **Respect the reference, serve the company**: design DNA from the reference, information architecture from the company's actual business. An Apple-style site for a movers company still needs the quote form above the fold.
- **Built sites are SEO/AEO-born**: titles, meta, schema, answer-first copy, performance — see code-build.md §SEO. A site from this engine should score well on the seo-audit-engine out of the box.
- **Mobile is half the pitch** — check every deliverable at phone width before presenting.

## Example

Input: "mockup for Sharma Dental, dental clinic in Pune, more like apple.com"
→ Research: finds their GBP listing (4.6★, 210 reviews), 6 services. Apple DNA: oversized type, generous whitespace, one message per screen, muted palette + single accent.
→ `mockup-v1.html`: hero "Dentistry, designed around you." with booking CTA, services as clean cards, reviews strip pulling the real 4.6★, doctor profiles, FAQ accordion, sticky call button on mobile.
→ Approval + "WordPress" → builds pages in their WP/Elementor matching the mockup, launch checklist done.
