---
name: analytics-setup-engine
description: 'Productized measurement onboarding for any new client. Given a client domain and business context, drive the full Google Search Console + Google Analytics 4 + Google Tag Manager setup hands-on in the browser: verify access, audit what already exists, derive a per-client tracking plan (key events based on their business model), configure GSC/GA4/GTM, verify every tag actually fires, build GA4 reports + a Looker Studio dashboard, and produce three deliverables — a client setup report (PDF), an internal tracking plan (xlsx), and a measurement one-pager. Use this whenever the user says "onboard clientname", "set up analytics/tracking for a domain", "run analytics onboarding", mentions GA4/GTM/GSC setup for a client, asks to fix or verify tracking, wants key events or conversion tracking configured, or asks for a client measurement dashboard — even if they only name one of the three tools.'
---

# Analytics Setup Engine

Turn "we got access to the client's accounts" into fully verified GSC + GA4 + GTM measurement with dashboards and client-ready documentation, in one guided run. The differentiator is *verification*: nothing is reported as "set up" until it has been watched firing with real data.

## Inputs

Required: **client domain** and **business context** (what they sell, how they get customers). Useful: website platform (WordPress/Shopify/custom SPA), target geography, what access has been granted so far, existing GA4/GTM/GSC assets, the conversion actions that matter to the client.

## Ground rules (read first)

- All account work happens in the browser via Claude in Chrome, in the **Growth100x** Chrome profile, inside accounts the user is already logged into. Never enter passwords or handle credentials — if a login wall appears, hand the browser to the user and wait.
- **Granting/changing account access (adding users, changing roles, transferring ownership) is done by the user personally** — prepare the exact steps and the email/role to add, then ask them to click it. Same for accepting Terms of Service on new GA4/GTM accounts.
- Confirm with the user before any irreversible or client-visible action: publishing a GTM container version, deleting existing tags/properties, changing data retention or filters on a property that already collects data.
- An existing, working setup is never torn down — audit it, keep what's correct, and fix incrementally. Clients often have half-working tracking with history worth preserving.
- If the site is a JS SPA (Angular/React), history-change tracking in GTM is mandatory or every pageview after the first is lost — see gtm-setup.md.

## Pipeline

### Phase 0 — Access + discovery

1. Confirm which of the three products the user can currently reach for this client (open each in the browser and look). Missing access → produce the access-request instructions for the client (exact steps + the agency email + required role: GSC Owner, GA4 Editor/Admin, GTM Publish/Admin) and pause that track until granted.
2. Audit current state before touching anything: existing GSC properties (domain vs URL-prefix), GA4 properties/streams and what events they receive, GTM containers and what's in them, hardcoded gtag/analytics snippets in the site source (fetch the homepage HTML and look), duplicate tracking risks.
3. Snapshot findings — they go in the deliverables as "before" state.

### Phase 1 — Tracking plan (get sign-off before building)

Read `references/tracking-plan.md`. Derive the event set from the client's business model — do not apply a fixed template. Map: business goal → user action → event name → trigger definition → parameters → key event yes/no → where it surfaces (report/dashboard). Present the plan as a compact table in chat and get the user's explicit sign-off before configuring anything. This table becomes the xlsx core and the one-pager.

### Phase 2 — Setup, tool by tool

Work in this order (GSC first — verification is a prerequisite for the GA4 link; GTM before GA4 events — tags need somewhere to fire from):

1. **GSC** — read `references/gsc-setup.md`: property (domain property preferred), verification, sitemap submission, baseline checks (indexing, manual actions, money-page URL inspection), GA4 link, user access.
2. **GTM** — read `references/gtm-setup.md`: container, Google tag, event tags/triggers/variables from the tracking plan, naming conventions, consent mode if needed, SPA handling, Preview verification, publish (with user confirmation).
3. **GA4** — read `references/ga4-setup.md`: property/stream config, enhanced measurement, mark key events, internal-traffic + referral exclusions, data retention, GSC/Ads links, Library reports, DebugView verification.

### Phase 3 — End-to-end verification (the money step)

Prove every tracking-plan row live: GTM Preview shows the tag firing on the real action → the event appears in GA4 DebugView/Realtime with correct parameters → key events show as key events. Perform the actual test actions on the live site in the browser (submit the test form with obviously-test data, click the phone link). Capture screenshots of each proof — they go in the client PDF. Any row that can't be verified is marked FAILED/PENDING with the reason, never glossed over.

### Phase 4 — Dashboards

1. **GA4 native**: publish the report collection from ga4-setup.md (traffic, key events, landing pages, GSC queries).
2. **Looker Studio**: client-facing dashboard — connect the GA4 property (+ GSC connector), one page: scorecards (users, sessions, key events), trend line, top pages, top queries, traffic sources, key-event breakdown. Share view-link with the client's email; confirm with the user before sharing externally.

### Phase 5 — Deliverables

Read `references/outputs.md` for exact structures, then build:

1. **Client setup report (PDF)** — via the pdf skill: what was set up, before/after, verification proof (screenshots), how to read your data, dashboard links, glossary.
2. **Internal tracking plan (xlsx)** — via the xlsx skill: Events matrix, GTM inventory, Access log, Verification checklist, Links & IDs.
3. **Measurement one-pager (PDF, 1 page)** — goals → events → where to look, for the client's team.

Save all three to the user's project folder under `Analytics Setup Engine/<domain>/` (one folder per client) and present them.

## Quality bar

- "Configured" ≠ "verified". The run is not done until Phase 3 proofs exist for every P1 event.
- Never report data the tools didn't show. New properties have no history — say so; don't promise numbers by a date.
- Test data pollutes: use DebugView/Preview for validation, exclude internal traffic before real reporting starts, and label any test events fired during setup.
- Leave every account better documented than found: GTM version notes, consistent naming, the xlsx as the client's single source of truth.

## Re-run mode

If the user re-runs the engine for an existing client ("check tracking for <domain>"), skip to Phase 0 discovery + Phase 3 verification and produce a short health report (what still fires, what broke) instead of full deliverables.
