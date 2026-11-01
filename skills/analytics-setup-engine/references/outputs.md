# Output templates

Three deliverables per onboarding. Save to `Analytics Setup Engine/<domain>/`. Default brand: Growth100X (same visual language as the seo-audit-engine PDFs) unless the user says otherwise.

## 1. Client setup report — `<domain>-analytics-setup-<YYYY-MM-DD>.pdf` (8–12 pages)

1. **Cover** — "Measurement & Analytics Setup: <Brand>", domain, date.
2. **Executive summary** — what is now being measured in business terms ("every call, WhatsApp message and quote request from your website is now counted"), before → after in 3–4 bullets, dashboard link.
3. **What was set up** — one page per tool (GSC / GTM / GA4): configuration table (IDs, property names, settings chosen and why, in one plain-language line each).
4. **Your key events** — the tracking-plan table, client-readable: action → what we call it → why it matters.
5. **Verification proof** — the Phase-3 evidence: per key event, the test performed + screenshot of it firing/arriving. Any PENDING items with reason and owner.
6. **How to read your data** — 3–4 short walkthroughs with screenshots: "How many leads did the website generate this month?", "Which pages bring customers?", "What are people searching to find you?" (GSC), "Where do visitors come from?". Each: where to click, what the number means.
7. **Dashboard guide** — Looker Studio link, what each widget shows, refresh cadence, data-lag notes (GSC ~2 days; new property = history starts today).
8. **Housekeeping** — access log summary, what NOT to touch (filters, GTM container), support contact.

Rules: plain language throughout, jargon decoded on first use; only verified claims — "configured, verification pending" is an acceptable status, silent failure is not.

## 2. Internal tracking plan — `<domain>-tracking-plan-<YYYY-MM-DD>.xlsx`

1. **Events matrix** — Event | Business goal | Trigger (GTM) | Trigger detail/selector | Params | Key event | Destination | Verified (date) | Notes. One row per tracking-plan row; verification column color-coded.
2. **GTM inventory** — every tag/trigger/variable created or modified: Name | Type | What it does | Version added.
3. **Access log** — Product | Account/Property/Container ID | Who has access | Role | Granted date | Owner (client/agency).
4. **Verification checklist** — the Phase-3 test log: Test | Expected | Observed | Pass/Fail | Screenshot ref | Date. Plus the 24–48h follow-up checks as open rows.
5. **Links & IDs** — GA4 property + Measurement ID, GTM container ID + latest version, GSC property, Looker Studio URL, site platform notes. This sheet is the single source of truth for re-runs.

## 3. Measurement one-pager — `<domain>-measurement-guide-<YYYY-MM-DD>.pdf` (exactly 1 page)

For the client's team. Three columns/blocks: **Your goals** (in their words) → **What we measure** (key events, plain names) → **Where to see it** (dashboard widget / GA4 report, linked). Footer: dashboard URL, who to contact, "data starts <date>".

## Handoff message

After presenting files, give the user a short paste-ready summary they can send the client (what's live, dashboard link, what to expect in the first 2 weeks) — code block, their voice, no hype.
