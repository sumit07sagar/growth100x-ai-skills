---
name: seo-audit-engine
description: 'Full-service productized SEO/AEO/GEO audit engine for any client. Given just a website domain and brief context about its services, run a complete LIVE audit — technical SEO, on-page, keyword research + mapping, content strategy, off-page, local SEO, AI/LLM visibility (AEO/GEO), programmatic opportunities, analytics — and produce two deliverables in one run, a polished client-facing PDF report (scores, findings, 90-day roadmap, pricing) plus an internal execution checklist (xlsx). Use this whenever the user asks to audit a website or domain, says "run the audit engine" or "audit somedomain.com", wants to productize SEO for a client, asks for an SEO/AEO/GEO analysis, proposal, or roadmap for a site, or simply provides a domain plus a description of its services expecting an SEO deliverable — even if they do not say the word "audit".'
---

# SEO Audit Engine

Turn a domain + one paragraph of context into a full, evidence-based SEO/AEO/GEO audit with two deliverables: a client-ready PDF and an internal execution checklist. Everything is grounded in live data collected during the run — never invent findings.

## Inputs

Required: **domain** and **brief context** (what they sell/do). Useful if given, but don't block on them: target geography, main competitors, priority services, whether they have physical locations (decides the Local module), current traffic/GSC access notes.

If the user gave only a domain, infer context from the site itself during collection. Ask at most ONE clarifying question, and only if the business model is genuinely ambiguous after looking at the homepage.

## Pipeline

Work through phases in order. Phases 1–2 can run concurrently.

### Phase 1 — Live data collection (scripted)

Run the bundled collector (install deps once: `pip install requests beautifulsoup4 --break-system-packages`). Shell calls are often time-limited (~45s), so run it stage by stage — state accumulates in the output JSON and re-runs resume automatically:

```bash
python scripts/collect_site_data.py <domain> --output audit_data.json --stage infra
python scripts/collect_site_data.py <domain> --output audit_data.json --stage sitemap
python scripts/collect_site_data.py <domain> --output audit_data.json --stage pages --pages 12 --batch 5
# repeat the pages stage until it prints "pages_remaining": 0
python scripts/collect_site_data.py <domain> --output audit_data.json --stage psi-mobile
python scripts/collect_site_data.py <domain> --output audit_data.json --stage psi-desktop
```

Space stage invocations out (do search-side research between them) — bursting requests at one site triggers CDN rate limits (429s), which slows every later fetch.

(In an environment without shell time limits, `--stage all` does everything except PSI in one call.)

It fetches robots.txt (with per-AI-crawler access matrix), sitemaps, llms.txt, homepage + up to N sampled pages, and extracts per page: title/meta/canonical/robots meta, heading tree, word count, JSON-LD schema types, OG/Twitter cards, internal/external links, images missing alt, answer-first check on the opening paragraph, viewport/lang, plus site-level checks (https, www consolidation, 404 handling, compression, redirects). It also calls the PageSpeed Insights API (mobile + desktop) for the homepage.

If the script fails on a page (JS-rendered SPA, bot-blocking), note it — that is itself a critical technical finding (see the imTransporter pattern: Angular SPA → not indexable). Fall back to WebFetch for individual pages.

### Phase 2 — Search-side research (parallel with Phase 1)

Use web search to gather what the script can't see:

1. **Indexation reality**: search `site:<domain>` — indexed page count vs sitemap count.
2. **Brand SERP**: search the brand name — what appears, knowledge panel, reviews, competitors ranking on brand.
3. **Competitor scan**: search 3–5 head terms from the context; record who ranks, their page types (comparison pages, tools, listicles).
4. **AI-engine visibility spot check**: search 4–6 "best/top X" and question-form queries a buyer would ask an AI engine; note whether the client or competitors appear in results, AI Overviews, and heavily-cited sources (Reddit, G2, industry blogs) — those are the citation sources to target.
5. **Keyword expansion**: from the service context, build a seed list, then expand with long-tail, question, comparison ("X vs Y", "X alternatives"), and buyer-intent modifiers (pricing, near me, for <niche>).
6. **Backlink/mention proxy**: search `"<brand>" -site:<domain>` for mentions, guest posts, directories.

### Phase 3 — Module analysis and scoring

Read `references/modules.md` and grade every applicable module 0–100 against its rubric, citing concrete evidence from Phases 1–2 for each finding (URL, tag content, search result). Read `references/aeo-geo.md` before scoring the AI Visibility module — it contains current research data (what actually moves citations vs. what doesn't) that must shape the recommendations.

Skip the Local module for pure-SaaS/online businesses; skip Programmatic when there's no scalable data angle — say why in one line rather than padding.

### Phase 4 — Keyword map

Build the keyword mapping table: keyword → intent (info/commercial/transactional/navigational) → mapped URL (existing page, or "NEW: <proposed slug>") → priority (P1–P3) → content type (service page, comparison, guide, tool, location page). 30–60 keywords for a typical SMB. Every P1 keyword must map to a page; clusters of related long-tails map to one page, not one page each.

### Phase 5 — Roadmap + pricing

Convert findings into a 90-day roadmap: weeks 1–2 critical fixes, month 1 foundations, month 2 content + AEO, month 3 authority + scaling. Each item: task, module, impact (H/M/L), effort (hours), owner (client/agency). Then derive 3 pricing tiers from the roadmap scope. Format spec in `references/output-templates.md`.

### Phase 6 — Deliverables

Read `references/output-templates.md` for the exact structure of both outputs, then:

1. **Client PDF** — build via the pdf skill (read its SKILL.md first). Polished, exec-summary-first, scores dashboard, per-module findings with evidence, keyword map (top 25 in PDF), roadmap, pricing. Explain jargon in one clause the first time it appears.
2. **Internal checklist** — build via the xlsx skill. Full task list (every finding = a row), all keywords, raw scores. Dense, no polish.

Save both to the user's project folder under `SEO Audit Engine/<domain>/` (one subfolder per client — keeps multi-client runs separated and makes re-audit diffs easy to find) and present them. Filenames: `<domain>-seo-audit-<YYYY-MM-DD>.pdf` and `<domain>-execution-checklist-<YYYY-MM-DD>.xlsx`. Keep `audit_data.json` in the same folder for the next re-audit.

## Quality bar

- **Evidence or it doesn't ship.** Every finding names the URL/tag/search result that proves it. "Improve your title tags" is banned; "Homepage title is 'Home' (7 chars) — rewrite to '<proposed title>'" is the standard. Include the proposed fix, not just the problem.
- **Prioritize ruthlessly.** Lead with the 3–5 issues that gate everything else (indexability, crawler blocks, no schema). A wall of 200 equal-weight items is worthless.
- **AI visibility is a first-class citizen**, not an appendix — buyers increasingly ask ChatGPT/Perplexity before Google. Score it, benchmark it against competitors, and roadmap it.
- **No fabricated metrics.** If a number needs GSC/GA4/paid-tool access you don't have, mark it "requires access" and add obtaining access to the roadmap week 1.
- **Speed**: a full run should take roughly 15–30 min. Don't gold-plate collection; 10–12 sampled pages reveal the template-level patterns that matter.

## Example

Input: "audit acmemovers.in — packers and movers, 8 Indian cities"
→ Collector finds Angular SPA, 3 pages indexed vs 400 in sitemap, no schema, GPTBot blocked. Search finds zero AI-engine presence; competitors win via city pages + reviews.
→ P1s: prerendering/SSR, unblock AI crawlers, LocalBusiness+Service schema, GBP + review engine, 8 city hub pages.
→ PDF: overall 31/100, AI visibility 12/100, 90-day roadmap, 3 tiers. Xlsx: 74 tasks, 48 keywords mapped.
