# AEO/GEO working knowledge (updated 2026-07)

What actually moves AI-engine citations, per multi-source research as of mid-2026. Use this to weight findings and to keep recommendations honest.

## What moves citations (roughly in order of leverage)

1. **FAQ schema quality** (~20% weight in AEO scoring models) — real buyer questions with direct, complete answers; on-page FAQ content matching the markup.
2. **Answer-first formatting** (~19%) — the first paragraph of a page directly answers the query the page targets, in extractable plain prose. Rewrite openings before writing new content.
3. **Statistical density** (~16%) — concrete numbers, dates, named entities, original data. Quotable one-liners ("X% of Y do Z") get lifted verbatim into AI answers.
4. **Author/entity signals (E-E-A-T)** — identifiable humans with LinkedIn profiles, credentials, publication history carry more retrieval weight than anonymous bylines. Organization schema with `sameAs`, consistent brand facts.
5. **Presence on the sources engines already cite** — in most niches AI engines repeatedly cite the same third-party surfaces (Reddit, Quora, G2/Clutch, niche directories, industry blogs). Getting the brand onto those surfaces often beats another on-site tweak. Identify them per-niche via the Phase-2 spot checks.
6. **Crawler access** — GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended must not be blocked. Note: blocking GPTBot does NOT block ChatGPT live browsing (different agent), but allow both anyway.

## What does NOT move citations (don't oversell)

- **llms.txt: essentially no citation impact today.** Four independent datasets (Limy 515M bot events; OtterlyAI 90-day study; ALLMO 94,614 cited URLs; SE Ranking 300k domains) plus Google's own statements agree. Recommend it as cheap hygiene/futureproofing only — never as a headline fix, never with promised results.
- Keyword density, exact-match repetition, backlink volume for AEO specifically (backlinks still matter for classic SEO authority).

## Expectation-setting timelines (put these in client deliverables)

- Structural fixes (FAQ schema, answer-first rewrites): visible in Perplexity ~2–7 days, ChatGPT ~7–21 days.
- Claude + Google AI Overviews: ~14–45 days.
- Reputational/third-party signals: 30–90 days.
- Citation overlap across engines is only ~11% — monitoring one platform captures <25% of AI visibility. Spot-check at least ChatGPT-style, Perplexity-style, and Google AI Overview surfaces; recommend multi-engine monitoring.

## Practical audit moves

- Build the "AI-shaped query set": 6–10 queries a buyer would ask an assistant ("best <category> for <niche>", "<brand> vs <competitor>", "how much does <service> cost in <geo>", "is <brand> legit"). Record who gets cited today.
- Map each money page to the question it should be the canonical answer for; check its first paragraph actually answers it.
- Propose 3–5 quotable stats the client can publish from their own operational data (original numbers are citation magnets).
- Check `is <brand> legit/reviews` results — reputation gaps poison AI answers about the brand.
