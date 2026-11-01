---
name: seo-client-sop
description: Growth100X SEO onboarding + execution SOP. Given a new client's website, classify the site, run audit + analytics checks, generate a phased, gated SEO task list (xlsx), then execute it task by task with worklogs and weekly reports. Use when Sumit says "start SEO for <client>", "run the SEO SOP", "onboard <domain> for SEO", "build the SEO task list", "next SEO task", or "weekly SEO report" for a client.
---

# Growth100X SEO Client SOP

Distilled from four live engagements (Metairfare, Growth100X, Tooth Simplified, imTransporter, Apr–Oct 2026). Every gate below exists because skipping it cost weeks on at least one of them.

Three modes:
- **ONBOARD**: given a domain, produce the profile and the task list.
- **EXECUTE**: "next task" means run the next task.
- **REPORT**: the weekly report.

Work in the client's local project folder under `SEO/`. Use the Growth100x Chrome profile for GSC/GA4/Bing unless Sumit says otherwise. A wrong profile once produced a false "access blocked" report.

---

## MODE 1 — ONBOARD (domain → task list)

### Step 1. Intake (≤10 min, no blocking)
Gather from the site itself plus anything Sumit gives. Ask at most one question, and only if the business model is unclear.
- Business: what they sell, ICPs, geography, primary conversion (call / WhatsApp / form / booking / app install), price points.
- Stack: check the CMS and any SEO plugin (Yoast/Rank Math), page builder, and whether the site renders client-side (SPA). Check the CDN (Cloudflare?) and the hosts (www + blog subdomain?).
- People: who can edit what (Claude via WP REST app password, client dev for custom code, client for accounts/GBP).
- History: GSC age, recent domain migration, existing content count.

Write `SEO/00-client-profile.md` with these **flags** (Y/N + one-line evidence). The flags decide which conditional tasks enter the list.

| Flag | Meaning | Trigger evidence |
|---|---|---|
| WP | WordPress (note .com plan limits) | wp-json responds |
| CUSTOM | Laravel/custom/headless, so changes go via dev tickets | no CMS, dev team |
| SPA | JS-rendered pages (Angular/React without SSR) | view-source lacks body content |
| MULTIHOST | blog or app on a subdomain | blog.* exists |
| LOCAL | physical location or service area | address, "near me" intent |
| YMYL | health / finance / legal | topic |
| REGULATED | advertising rules apply (SEC/FINRA, medical, legal) | licensed advisor, clinic |
| PROGRAMMATIC | repeatable data pages (city/route/service×location) | data source exists |
| INTL | multiple countries or currencies | ICPs abroad |
| ECOM | online store | cart |
| MIGRATION | domain/URL change in the last 6 months or planned | old domain |
| ESTABLISHED | ≥1k impr/28d in GSC → refresh-first strategy | GSC |
| NEW | <1k impr/28d → foundation + coverage strategy | GSC |

### Step 2. Diagnose (reuse existing engines, don't rebuild)
1. Run the **analytics-setup-engine** skill: GSC (domain property if MULTIHOST), GA4, GTM, Bing WMT, key events.
2. Run the **seo-audit-engine** skill: live crawl, scores, keyword map, competitor and AI-visibility scan.
3. Pull baselines into `SEO/01-baseline.md`:
   - GSC 3-month clicks / impressions / CTR / position, and the branded vs non-branded split.
   - Indexed vs not-indexed, split into Discovered-not-indexed and Crawled-not-indexed.
   - Top 50 queries sorted by **impressions**, not clicks.
   - Bing clicks and AI Performance citations.
   - GA4 key events per 28 days.
   - Referring domains and GBP review count, plus the review counts of the top 3 competitors.
4. Run 5–8 AI-visibility test queries (buyer questions) across Google AIO, Perplexity, ChatGPT and Bing Copilot. Log who is cited.

### Step 3. Set targets from run-rate (not ambition)
- One commercial KPI (leads or consultations per month).
- Leading indicators: indexed pages, non-branded clicks, query count, avg position, referring domains, reviews, AI citations.
- 90-day target = current run-rate × realistic multiplier (2–4× for NEW, 1.5–2× for ESTABLISHED).
  - The "1M impressions" target at Tooth Simplified was 48× run-rate and had to be re-baselined to 100k cumulative.

### Step 4. Generate the task list
Start with every **Core** task from the Task Library below. Add each **Conditional** task whose flag is Y. Then add every Critical/High finding from the audit-engine checklist as an extra row, tagged `AUD-n`. Drop tasks the audit proves are already done (mark Done, evidence in Notes).

Build `SEO/<client>-SEO-Task-List.xlsx` (use the xlsx skill) with these sheets:
- **Tasks**: ID | Phase | Sprint | Module | Task | Why (evidence / lesson) | Acceptance check | Owner (G100X / Client dev / Client / Sumit) | Depends on | Gate | Priority (P1–P3) | Effort hrs | Status (Todo / Doing / Blocked / Done) | Done date | Notes
- **Needs Client / Sumit**: Item | Why it's blocked on them | Exact ask | Date asked | Chased.
- **Keyword Map**: Keyword | Intent | Cluster | Target URL / NEW slug | Priority | Content type | SERP features | Current pos.
- **Content Calendar**: # | Cluster | Type (refresh/new) | Title | Primary KW | Status | Target date | URL.
- **Striking Distance Log**: URL | Query | Pos before | Change made | Date | Recheck date | Pos after | Clicks after.
- **KPI Tracker**: one row per week. Columns are the Step 3 metrics plus a "peak to date" row.
- **Gates**: the gate list below with current status (Open / Passed).

Sprints are 2 weeks. Sort order: Phase, then Priority, then dependency.

Present the list to Sumit with a 5-line summary: profile flags, top 3 blockers, sprint 1 contents, and the Needs-Client asks. **Wait for approval before executing.**

---

## GATES (hard rules, checked before the tasks they guard)

- **G1 Measurement first.** No reporting, and no content scaling, until every key event has been test-fired and is visible in GA4 DebugView/Realtime.
  - Bots must be filtered and the internal-traffic filter set to *Active*, not Testing.
  - Real cases: Metairfare logged 8 leads/mo until tracking was fixed (then 144). imT had +137% organic and 0 leads. Tooth Simplified's phone_click was 0. Growth100X had dead key events.
- **G2 Index health before scale.** Hold bulk or programmatic publishing while (Discovered + Crawled-not-indexed) is above 25% of indexed pages, or has risen 2 weeks running.
  - Growth100X shipped 250 city pages and froze at 168 indexed. Tooth Simplified's templated posts pushed Discovered-not-indexed to 261.
- **G3 Upgrade before new.** Before any new page, pull the live inventory (WP REST / sitemap) and check intent overlap. If a page exists, refresh it or 301 the duplicates into a winner.
- **G4 Canonical check before editing.** Confirm the page is its own canonical. Tooth Simplified edited a post that was canonicalised elsewhere, so the edits were ignored.
- **G5 Authority starts in Sprint 1, in parallel.** Off-page was the ceiling on all four sites: DR 0 and only 2–3 referring domains after months.
- **G6 Facts and claims.** Every price, statistic or claim is verified and source-noted. Prices come from the client's authoritative list.
  - REGULATED: every page and post passes compliance review. No performance promises, testimonials or "best" claims without a basis. Disclosures stay intact.
- **G7 Sitewide or brand changes need Sumit's sign-off.** This covers templates, nav, header/footer, marketing claims and plugins. Write a rollback note before any change.
- **G8 Re-test after every performance or template change.** Run PSI mobile the same day and again 48h later. Run a SERP regression check on the top 10 URLs. Growth100X's LCP went from 3.6s to 6.4s and was never caught.
- **G9 CTR work only where it can pay.** Title/meta rewrites go only to pages at position ≤15 with impressions ≥100/28d. Above that, the lever is content, links or internal links.
  - Growth100X at position 45–100 and Metairfare's FAQ hubs got zero return from title tweaks.
- **G10 Read data correctly.**
  - Use URL Inspection (live) for single URLs; the Page indexing summary lags 1–2 weeks.
  - Sort by impressions.
  - Compare against prior period **and** peak; week-on-week deltas once hid a plateau.

---

## TASK LIBRARY

Format: `ID | Task | Acceptance check | Owner`. Tasks marked [C:FLAG] are conditional on that flag.

### Phase 0 — Access & Measurement (Week 0–1) — Gate G1
- M01 | Get access: GSC (Owner), GA4 (Editor), GTM, Bing WMT, GBP (Manager), CMS (WP REST app password, not browser login), Cloudflare, Ahrefs/Semrush if any | All logins tested; any missing ones go on Needs-Client | Client
- M02 | GSC property: domain property; sitemap(s) submitted | Sitemap "Success", URL count matches | G100X
- M03 | Bing WMT via GSC import; sitemap submitted; IndexNow on | Bing shows sitemap and URLs. Bing feeds ChatGPT and Copilot. | G100X
- M04 | Event plan: one key event per conversion (call_click, whatsapp_click, form_submit/generate_lead, booking) | Each fires exactly once in DebugView; no double-fire | G100X
- M05 | GA4 hygiene: internal-traffic filter Active, bot/spam check (Ashburn/China/SG/VN), retention 14 months, AI Assistant channel group, Google AIO not counted as referral | Filters Active; channel group visible | G100X
- M06 | Remove legacy or duplicate tags (old UA, duplicate GTM containers) | One GA4 hit per pageview | G100X
- M07 | Cloudflare Bot Fight Mode if bot traffic appears [C:CDN] | Bot geos gone from GA4 within 2 weeks | G100X/Client
- M08 | Baseline file plus KPI Tracker row 1 | 01-baseline.md complete | G100X
- M09 [C:MULTIHOST] | Shared GA4 across hosts, cross-domain config, blog GTM container confirmed ON | Blog sessions appear under the same property | G100X

### Phase 1 — Indexability & Technical Foundation (Sprint 1)
- T01 | robots.txt review incl. AI crawlers (GPTBot, PerplexityBot, ClaudeBot, Google-Extended, Bingbot) allowed | robots matrix all allow (unless the client opts out) | G100X
- T02 | Sitemap hygiene: only 200, indexable, canonical URLs; no attachment/image/feed/tag junk; lastmod accurate; cache not stale after publish | Sitemap URL count = indexable pages; 0 non-200 | G100X
- T03 | Indexing triage: export not-indexed, bucket into noindex / 301 / enhance / fine, with a redirect CSV | Triage CSV; buckets actioned | G100X
- T04 | Host canonicalisation: https, single www/non-www, trailing slash, one 301 hop | curl shows 1 hop to the canonical | G100X/Dev
- T05 | 404 / redirect-chain sweep incl. nav and footer links | 0 internal 404s, 0 chains | G100X
- T06 | Single H1 per template, unique titles per template, no double-encoded entities | Crawl: 1 H1 per page | G100X/Dev
- T07 | Thin and junk pages: archives, date pages, empty categories, tag pages → noindex or 410 | Not in sitemap; noindex verified | G100X
- T08 | Core Web Vitals: PSI mobile/desktop for home plus top templates; fix biggest LCP/TBT cause → G8 | Mobile LCP <2.5s, or a documented cause | G100X/Dev
- T09 | HTML cacheability at CDN (cookies or no-cache on every response blocks caching) [C:CDN] | cf-cache-status HIT on HTML | Dev
- T10 | Orphan check: every money page has ≥3 internal inbound links; hub pages exist | URL Inspection shows a referring page | G100X
- T11 | Request indexing for money pages (≤10/day, money pages first) | Live inspect "URL is on Google" | G100X
- T12 [C:SPA] | SSR/prerender so body, H1, FAQ and schema are in the raw HTML | view-source shows content | Dev
- T13 [C:WP] | Plugin audit (read-only first): overlaps, inline CSS/JS bloat, page-builder duplicate H1 | Plugin table; removals approved per G7 | G100X
- T14 [C:MIGRATION] | Migration check: Change of Address, old→new 301 map, old domain absent from schema/canonicals/hreflang, Bing re-added | 0 old-domain refs in JSON-LD; CoA done | G100X
- T15 [C:CUSTOM] | Dev ticket pack: numbered tickets (D1…) with paste-ready blocks, a "do not touch" list and a curl acceptance test each | Dev replies shipped; G100X re-verifies | G100X→Dev

### Phase 2 — On-page, Entity & Schema (Sprint 1–2)
- O01 | Title/meta rewrite on G9-eligible pages: query first, price or number hook, year, credential | Logged in Striking Distance Log | G100X
- O02 | Answer-first opening (40–80 words) on all money and pillar pages | First paragraph answers the H1 query | G100X
- O03 | Intent check: page type matches the SERP (service page vs listicle vs guide); retarget mismatches | SERP screenshot note per P1 keyword | G100X
- O04 | Conversion on every page: above-fold CTA, mid- and end-article CTA, floating WhatsApp/call where relevant | CTA event fires from a blog post | G100X
- S01 | Organization/WebSite schema with correct site name, logo and sameAs; no duplicate hand-written blocks | Rich Results Test clean; one Organization node | G100X
- S02 | Article + BreadcrumbList + author Person on posts | Valid | G100X
- S03 | FAQPage schema whose JSON-LD matches the visible Q&A exactly | Valid; text identical | G100X
- S04 | Service schema on service pages | Valid | G100X
- S05 [C:LOCAL] | LocalBusiness subtype (Dentist, MovingCompany, FinancialService…) with NAP identical to GBP and areaServed | Valid; NAP diff = 0 | G100X
- S06 | Review/AggregateRating only from real, current review data; keep the count synced with GBP | No "missing itemReviewed" errors | G100X
- E01 | Entity profiles: Crunchbase, LinkedIn, Wikidata (if notable), industry directories, plus sameAs links | Listed in the Organization sameAs | G100X/Client
- E02 [C:YMYL] | E-E-A-T: named expert author with credentials, bio page, "reviewed by" box, editorial policy, sources cited | Bio page live; byline on all posts | G100X/Client
- E03 [C:REGULATED] | Compliance pack: required disclosures/footer, claim rules, approver named, review SLA | Approver signs off the template | Client
- E04 | llms.txt listing money pages and pillar guides | /llms.txt returns 200 | G100X

### Phase 3 — Content: refresh first, then gaps (Sprint 2 onward)
- C01 | Live content inventory CSV (REST/sitemap) with GSC metrics, re-pulled each run → G3 | inventory-YYYY-MM-DD.csv | G100X
- C02 | Cannibalisation consolidation: one winner per intent, 301 the rest, merge content in | Only 1 URL ranks per intent query | G100X
- C03 [C:ESTABLISHED] | Refresh run: top 30 pages by impressions at position 5–20. Rework the answer section, tables, FAQ and internal links. | Striking Distance Log rows with a recheck at +14 days | G100X
- C04 | Thin-content sweep: expand or merge anything under ~700 words on money topics | 0 thin money pages | G100X
- C05 | Keyword map and clusters: pillar + 6–10 spokes each; every P1 keyword maps to exactly one URL | Keyword Map sheet complete | G100X
- C06 | Pillar guides with bidirectional links and a "Part of our guide" callout on every spoke | Each spoke links to its pillar and back | G100X
- C07 | Ship the proven formats first:
  - comparison/decision posts ("X vs Y", "alternatives", "best X for Y")
  - cost/charges/pricing guides with tables
  - "best time to…" and checklists
  - original data/benchmark posts (citation bait)

  Acceptance: ≥50% of Sprint 2–3 posts are these formats | G100X
- C08 | Post template: question H2s with 40–80 word answers, a comparison/price table with a month-year stamp, key takeaways, FAQ (5–8), CTA blocks, byline, schema | Template checklist passes | G100X
- C09 | Publish cadence of 2–4 posts/week, only while G2 holds | Calendar statuses current | G100X
- C10 [C:LOCAL] | Location/area pages, one per real service area, with unique local proof (not just a city-name swap) | Each has a unique 300+ word local section | G100X
- C11 [C:INTL] | Currency and market policy: local currency for local intent, one fixed conversion rule, per-country pages only where demand exists | Policy tab; no mismatched currency on India-intent pages | G100X
- C12 [C:YMYL] | Trust content: safety checklist, how-to-vet, guarantees/risks, credentials (often what AI engines cite) | Live and linked from money pages | G100X
- C13 [C:REGULATED] | Every draft goes to the compliance approver before publish | Approval logged in Notes | Client

### Phase 4 — Authority & Local (starts Sprint 1, runs continuously) — Gate G5
- A01 | Backlink plan: tiers (1 directories/entity, 2 expert-quote platforms such as Connectively/Qwoted/Featured, 3 guest posts/listicle pitches, 4 client/partner credit links) | Target sheet with 30+ rows | G100X
- A02 | Weekly authority quota: 2 directory listings, 2 pitches, 1 expert-quote response, and *submitted*, not just drafted | KPI Tracker referring domains | G100X/outreach
- A03 | Unlinked brand mentions plus competitor backlink gap | List actioned | G100X
- A04 | Linkable asset: one original data study or calculator per quarter | Live, pitched to 10+ sites | G100X
- A05 | Reddit/Quora answers where buyers ask (value-first, disclosed) | 4/month | G100X
- L01 [C:LOCAL] | GBP: categories, services, hours, photos, phone, weekly post. Avoid promo or phone text in posts, which caused a policy hold at Tooth Simplified. | GBP complete; no flags | G100X/Client
- L02 [C:LOCAL] | Review engine: in-person ask, QR code, WhatsApp request, weekly tally. Target a gap-closing velocity against competitors. Reviews gate the local pack and AIO. | Reviews/week in KPI | Client
- L03 [C:LOCAL] | Citations with an identical canonical NAP block: GBP, Bing Places, Apple Business, plus niche directories | Citation sheet; NAP diff = 0 | G100X
- L04 [C:LOCAL] | GBP Q&A seed (10–12 real buyer questions) | Answered as owner | G100X

### Phase 5 — AEO / GEO (Sprint 2 onward)
- G01 | AI visibility log: fixed set of 8 queries checked weekly (Google AIO, Perplexity, ChatGPT, Copilot); note who is cited | Weekly rows | G100X
- G02 | Bing AI Performance citations tracked weekly (Bing citations showed the earliest win on all four sites) | KPI column | G100X
- G03 | Citable blocks: definitive tables, checklists, stats with sources on every pillar | Present on pillars | G100X
- G04 | Get listed on the sources AI engines already cite for the client's queries (from G01) | 1 new source/month | G100X

### Phase 6 — Scale (Gate G2 must be passed)
- P01 [C:PROGRAMMATIC] | Template spec per page type: unique data per page (tables, local detail), 600+ unique words, schema, hub plus nearby-links widget | 5-page pilot indexed ≥80% within 4 weeks before the rest | G100X/Dev
- P02 [C:PROGRAMMATIC] | Release in batches of 10–20; next batch only when the previous one is ≥70% indexed | Batch log | G100X

### Phase 7 — Weekly Loop (forever)
- W01 | Weekly report (Mode 3)
- W02 | Striking-distance rechecks for the rows due this week
- W03 | Re-audit with seo-audit-engine every 4–6 weeks; diff against the last audit_data.json
- W04 | Sprint review every 2 weeks: close, re-plan, update Needs-Client and chase blockers older than 7 days

---

## MODE 2 — EXECUTE ("next task")
1. Open the Task List. Pick the highest-priority Todo task whose dependencies are Done and whose gate is Passed. Skip Owner = Client tasks; those live on Needs-Client.
2. State the task and its acceptance check in one line, then do it.
3. Verify with the acceptance check: live URL, curl, Rich Results Test, DebugView. "Done" without verification is not done.
4. If the task touches anything under G6 or G7, prepare the change and stop for sign-off.
5. Update Status, Done date and Notes in the xlsx. Append to `SEO/worklog/YYYY-MM-DD-<task-id>.md`: what changed, URLs, before/after, rollback.
6. If the task changed a page that ranks, add a Striking Distance Log row with a recheck date of +14 days.

Batch similar tasks in one run (e.g. all S0x schema tasks) when they share access and context.

## MODE 3 — REPORT (weekly, fixed day per client)
`SEO/reports/Weekly-SEO-Report-YYYY-MM-DD.md`. Bullets, numbers first.
1. **Step 0 live pull**: table of Metric | This period (28d) | Prior 28d | Peak to date | Δ.
   - Clicks (branded / non-branded), impressions, CTR, avg position, query count.
   - Indexed and not-indexed (Discovered / Crawled).
   - Key events, by source incl. AI Assistant.
   - Bing clicks and citations, referring domains, reviews, mobile LCP.
2. **Wins**: only those backed by data.
3. **Problems / anomalies**, each with a cause hypothesis and a check.
4. **AI visibility**: G01 table.
5. **Authority**: submitted this week, and links won.
6. **Executed this week**: task IDs with URLs.
7. **Top 3 next**, ranked by impact per effort.
8. **Needs Client / Sumit.**
9. Honest notes, e.g. CTR dilution from new long-tail impressions, or a plateau compared with the peak.

## Folder layout
```
<Client>/SEO/
  00-client-profile.md   01-baseline.md   <client>-SEO-Task-List.xlsx
  SEO Audit Engine/<domain>/ (audit pdf, checklist, audit_data.json)
  worklog/   reports/   dev-tickets/
```

## Reference implementations (in Sumit's Projects folder)
- Sprint playbook: Toothsimplified,com/Sonnet-Execution-Playbook-2026-07-24.md
- Dev tickets: Metairfare/Dev-Handoff/README.md and imT/imTransporter-Month2-Dev-Spec-mainsite.md
- Indexing triage: Metairfare/Crawled-Not-Indexed-Triage/
- Weekly report: Growth 100x/Weekly-SEO-Report-2026-09-07.md (Step 0 vs peak) and Toothsimplified,com/SEO-Report-2026-09-10.md
- Content calendar and striking-distance workbook: Toothsimplified,com/Tooth-Simplified-Content-Plan-Calendar-2026-08-02.xlsx
- Blog build: imT/client-blog-engine-prompt.md
- Backlinks: Growth 100x/Growth100X-Link-Building-Outreach-Kit.md
- Review drive: Toothsimplified,com/Review-Drive-and-AI-Overview-Plan-2026-09-03.md
