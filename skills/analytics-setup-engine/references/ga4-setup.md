# GA4 setup runbook

## Property + stream

- Audit first: existing property receiving data? Multiple properties/streams causing confusion? Keep the one with history; document the others as deprecated in the xlsx.
- New setup: account (client-owned, agency granted access — not created under the agency's account, so the client keeps their data if the relationship ends), property in client's timezone + currency, one web data stream on the canonical origin.
- The stream's Measurement ID goes into the GTM Google tag (gtm-setup.md) — no hardcoded gtag if GTM is the tag system.

## Configuration checklist

- **Enhanced measurement**: review toggles per site — outbound clicks + scrolls usually on; site-search on if the site has search (set the query param); form-interactions OFF when GTM handles forms (double counting).
- **Key events**: mark exactly the tracking-plan rows flagged as key events (Admin > Events > toggle, or create-event first for GTM-sourced custom events once they've been seen). 3–6 max.
- **Internal traffic**: define internal IPs (the user's + client's office) → activate the Internal Traffic filter (it ships in "testing" state — must be set to Active, the #1 missed step). Add developer traffic exclusions if a dev site shares the stream.
- **Referral exclusions**: payment gateways (Razorpay/PayU/Stripe/PayPal) and the client's own domains.
- **Data retention**: 2/14 months → set to 14 (another silently-bad default); reset-on-activity on.
- **Google Signals / granular consent**: decide per client privacy posture; note the decision.
- **Links**: GSC (enables the Search Console report collection — publish it in Library), Google Ads if they run ads.
- **Data quality**: check for bot/spam pollution patterns (see the Growth100X GA4 lesson: 90%+ "direct" spikes with 0-second sessions = bot noise; add hostname/spam filters and say real numbers may drop after cleanup — that's honesty, warn the client in the report).

## Reports + Library (the "managed dashboards" part)

Publish a client collection in Reports > Library:
1. **Acquisition overview** — sessions/users by channel, trended.
2. **Key events report** — key events by channel + landing page (this answers "what's driving leads").
3. **Landing pages** — sessions, engagement rate, key events per landing page (content team's main view).
4. **GSC collection** — queries + Google-organic landing pages (after GSC link).
Plus one Exploration saved for the user: funnel of the money path (landing → intent page → key event).

## Verification

- DebugView with GTM Preview: each event arrives with params.
- Realtime: live test actions appear (event + key-event count).
- 24–48h later (note as follow-up): events in standard reports, key events attributed, no (not set) explosions, GSC data flowing.

## Common traps

- Marking an event "key" before GA4 has seen it once → create the event definition or fire a test first.
- Enhanced measurement form_submit + GTM form_submit = double counting; pick one source.
- Property in wrong timezone silently misaligns "yesterday" with ad platforms.
- Filters are not retroactive — internal traffic before activation stays in the data; annotate the cleanup date.
