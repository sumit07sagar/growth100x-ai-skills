# Output templates

Two deliverables per run. Same underlying findings, different audiences — the PDF sells and explains; the xlsx executes.

## Deliverable 1 — Client PDF: `<domain>-seo-audit-<YYYY-MM-DD>.pdf`

Design: clean, professional, generous whitespace. Default brand: Growth100X (dark navy/near-black base, single accent color, modern sans-serif) unless the user specifies otherwise. Score visuals: horizontal bars or donut per module. 12–20 pages typical.

Structure (exact order):

1. **Cover** — "SEO, AEO & GEO Audit: <Brand>", domain, date, prepared-by.
2. **Executive summary (1 page)** — overall score + AI Visibility score prominently; the 3–5 critical findings in plain business language; the one-paragraph growth thesis (what to displace, how); expected trajectory if roadmap is executed.
3. **Scorecard** — table/bars: every module, score, one-line verdict.
4. **How buyers find you now vs. tomorrow (½ page)** — brief AEO/GEO explainer: buyers increasingly ask AI assistants; what that changes. One clause of jargon-decoding per term (AEO, GEO, schema...). This section positions the differentiator.
5. **Per-module findings** — one section per scored module: score, what we checked, findings table (Severity | What we found (evidence) | Why it matters | The fix). Max ~8 rows in PDF per module — highest severity first; the rest live in the xlsx ("plus N more in the execution checklist").
6. **Keyword map (top 25)** — Keyword | Intent | Target page (existing/NEW) | Priority | Content type. Note total count in xlsx.
7. **90-day roadmap** — Weeks 1–2: critical fixes. Month 1: foundations. Month 2: content + AEO. Month 3: authority + scale. Table: Task | Module | Impact | Effort | Owner. Include the AEO expectation timelines from aeo-geo.md.
8. **Investment options** — 3 tiers derived from roadmap scope, e.g. Essential (critical fixes + foundations), Growth (full roadmap execution), Partner (roadmap + ongoing content/authority retainer). Scope bullets per tier; anchor prices to the user's stated pricing if known, otherwise leave price cells as "on request" placeholders and tell the user to fill them.
9. **Methodology + next steps** — what was analyzed (N pages crawled, PSI, live SERP checks, AI-visibility spot checks), what needs access (GSC/GA4/Ahrefs) and what unlocks, CTA with contact.

Rules: every finding carries its evidence; no metric without a source; anything requiring account access is marked "requires access", never estimated.

## Deliverable 2 — Internal execution checklist: `<domain>-execution-checklist-<YYYY-MM-DD>.xlsx`

Dense working file. Sheets:

1. **Tasks** — every finding from every module (not just PDF top-8): ID | Module | Severity | Finding (evidence) | Fix | Impact | Effort (hrs) | Phase (Wk1-2 / M1 / M2 / M3) | Owner (agency/client) | Status (dropdown: Todo/Doing/Done) | Notes. Filterable, frozen header, severity color-coded.
2. **Keyword map (full)** — all keywords: Keyword | Intent | Volume note (est/unknown) | Target URL | New page? | Priority | Content type | Cluster.
3. **Scores** — module scores + weights + overall calc (live formulas so scores recompute if edited).
4. **AI visibility log** — the AI-shaped query set: Query | Engine surface checked | Brand present? | Who's cited | Citation source to target.
5. **Data snapshot** — key raw numbers from the collector (indexed vs sitemap count, PSI scores, schema types found, crawler access matrix) with collection date, so future re-audits can diff.

## Re-audit mode

If the user runs the engine again on the same domain, load the previous xlsx Data snapshot if available and lead the PDF exec summary with deltas (score changes, fixed vs new issues).
