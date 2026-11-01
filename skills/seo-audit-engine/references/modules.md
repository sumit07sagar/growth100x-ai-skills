# Module rubrics

Grade each applicable module 0–100. A module score is an editorial judgment against the rubric below, anchored by evidence — not a mechanical checklist count. For every finding record: what was observed (with URL/tag/search-result evidence), why it matters (one clause), and the specific proposed fix. Severity: **Critical** (gates other work), **High**, **Medium**, **Low**.

Scoring anchors for all modules: 85+ = genuinely strong, minor polish only; 60–84 = solid foundation, clear gaps; 35–59 = major gaps, fundamentals missing; <35 = broken or absent.

## 1. Technical SEO

- **Indexability first.** Compare `site:` indexed count vs sitemap count. A large gap is the headline finding. If the collector flags `likely_js_rendered_shell` pages, the site may be invisible to crawlers — Critical, and it caps this module at ~30 regardless of everything else.
- Crawl hygiene: robots.txt sanity (not blocking CSS/JS or whole site), sitemap exists + fresh + only 200/indexable URLs, no orphan doorway-page bloat (hundreds of thin near-duplicate URLs in sitemap).
- Consolidation: one canonical host (www vs non-www 301s, http→https), canonical tags present and self-referencing, no duplicate `-2` style URLs, 404s return 404 (not soft-200).
- Speed/CWV: PSI performance scores + lab metrics; field CWV if present (note when field data is absent due to low traffic — don't treat absence as failure).
- Mobile: viewport meta, PSI mobile score.
- Misc: compression enabled, hreflang if multi-locale, no meta-robots noindex accidents.

## 2. On-Page

- Titles: unique, 30–60 chars, primary keyword + differentiator, no "Home". Rollup `duplicate_titles` > 0 is High.
- Meta descriptions: present, 70–160 chars, written to earn the click.
- Headings: exactly one H1 per page, logical H2/H3 tree that mirrors subtopics; heading text contains real entities, not "Welcome".
- URL structure: short, hyphenated, keyword-bearing, consistent trailing slash.
- Internal linking: service pages reachable in ≤3 clicks from home; descriptive anchors; hub↔spoke links both directions; internal link count per page not near-zero.
- Schema: page-type-appropriate JSON-LD (Organization/LocalBusiness sitewide; Service, FAQPage, Article, BreadcrumbList, Product/Review where relevant). "INVALID_JSONLD" in collector output is High.
- Answer-first content: does the first paragraph directly answer "what is this page about / what does this company do" in 1–3 sentences? Check `first_paragraph` per page.
- Images: alt coverage (`images_missing_alt`), descriptive filenames.

## 3. Keyword Research & Mapping

This module is graded on the *site's current state* (does each money keyword have a dedicated, optimized page?) and produces the keyword map deliverable (Phase 4).

- Coverage: every core service × every target geo has a mappable page.
- Intent split: does the site have commercial pages (service/comparison/pricing) or only informational blog posts — or vice versa?
- Long-tail: question keywords answered anywhere? Comparison ("X vs Y") and alternative ("X alternatives") pages exist?
- Cannibalization: multiple pages targeting the same head term.
- Buyer keywords: pricing/cost pages, "best <category>" presence, near-me variants for local businesses.

## 4. Content Strategy

- Topical authority: pick the 2–4 topics the business must own; estimate cluster completeness (pillar page + supporting spokes, interlinked both ways).
- Content depth: avg word count on money pages (thin <300 words is High for service pages); but judge usefulness, not length for its own sake.
- Formats that win: comparison pages, alternatives pages, free tools/calculators (strong link + AI-citation magnets), original data/stats posts, refresh candidates (outdated years in titles).
- Freshness: last-modified signals, blog cadence, stale content with old dates.
- E-E-A-T: author bylines with real names/credentials, about page, editorial signals.

## 5. AI Visibility (AEO/GEO) — read references/aeo-geo.md before scoring

- AI crawler access matrix from collector: GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, Google-Extended blocked = Critical each.
- Presence spot check: does the brand appear when AI-shaped queries are searched (best/top/vs/how-to in their category)? Do competitors?
- Citation-source coverage: is the brand present on the sources AI engines actually cite in this niche (Reddit, Quora, G2/Clutch, industry directories, Wikipedia-adjacent)?
- On-site answer engineering: answer-first paragraphs, FAQ blocks with real questions, quotable one-liner stats, tables/lists that extract cleanly, dated + attributed content.
- Entity signals: Organization schema with sameAs to profiles, consistent NAP/brand facts, an "about" entity page.
- llms.txt: note presence as hygiene, not a ranking lever (see aeo-geo.md — do not oversell it).

## 6. Programmatic SEO (skip with one-line rationale if no data angle)

- Is there a scalable dataset (cities, integrations, templates, comparisons, calculators, glossary)?
- Existing programmatic pages: quality gates (unique value per page vs thin doorway spam — doorway bloat is a *negative* finding under Technical too), index management, template structure.
- Opportunity sizing: propose the template + data source + realistic page count; require a uniqueness ingredient per page (local data, prices, reviews).

## 7. Off-Page & Authority

- Backlink proxy signals (searches, brand mentions, `"<brand>" -site:` results); paid-tool numbers only if provided — otherwise mark "requires Ahrefs/GSC access".
- Digital PR angles: what data/story could this business pitch?
- Directories + communities: niche directories, G2/Clutch/JustDial-type platforms, Reddit/Quora presence where buyers ask questions (also feeds AI citations).
- Guest posting / partnerships realistic for the niche.
- Brand search volume as authority proxy: does anyone search the brand?

## 8. Local SEO (only when physical locations / local service areas exist)

- Google Business Profile: exists, claimed, category, photos, posts, Q&A.
- Reviews: count + rating vs top-3 local competitors; review velocity; response habit. For local service businesses reviews are usually the #1 lever — say so plainly.
- Location pages: one real page per city/area with unique content (not doorway boilerplate), LocalBusiness schema, embedded map, local proof (reviews, jobs done, phone).
- NAP consistency across site, GBP, directories.
- Local pack presence for "<service> <city>" head terms.

## 9. Analytics & Measurement

- GSC + GA4 (or equivalent) installed? Verify tag presence in HTML.
- Conversion tracking: are forms/calls/checkouts measurable as events?
- Bot pollution: flag if traffic patterns suggest bot inflation (common on WP; if unverifiable, add "audit GA4 filters" to roadmap).
- Rank tracking: recommend a lightweight tracked keyword set (the P1s from the keyword map).
- Attribution sanity for the business model (calls vs forms vs ecommerce).

## 10. Strategy & Roadmap

Not scored 0-100 like the others — this module *synthesizes*: the competitive displacement thesis (which competitor's traffic can realistically be taken, via which page types), non-branded growth plan, topical map, and the compounding loop (content → links/citations → authority → faster indexing → more content). It becomes the exec summary and the 90-day roadmap.

## Overall score

Weighted average of scored modules; default weights: Technical 20, On-Page 15, AI Visibility 15, Keywords 12, Content 12, Off-Page 10, Local 8 (redistribute if skipped), Analytics 4, Programmatic 4. Also report a standalone **AI Visibility score** next to the overall — it's the differentiator clients haven't seen elsewhere.
