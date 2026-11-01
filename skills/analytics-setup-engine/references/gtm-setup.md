# GTM setup runbook

## Container

- One container per site. If the client has an existing container, audit it first: export a version snapshot (Admin > Export) before changing anything — that's the rollback.
- Container snippet installed once, sitewide (head + noscript body). WordPress: prefer a site-wide code manager or theme hook, not per-page. Verify with a fetch of the live HTML that (a) the GTM snippet is present and (b) there is **no duplicate** hardcoded gtag snippet double-counting pageviews — if there is, plan its removal in the same release as the GTM-based Google tag going live.

## Naming conventions (non-negotiable — future-you is the audience)

- Tags: `GA4 | Event | form_submit`, `GA4 | Config | Google tag`
- Triggers: `CE | form_submit` (custom event), `Click | tel links`, `Visibility | thank-you`
- Variables: `DLV | form_id`, `JS | page_type`
- Folders per purpose (GA4, Ads, Utilities). Every publish gets a version name + note describing the change.

## Build from the tracking plan

- **Google tag** (GA4 measurement ID) on All Pages / Initialization.
- Event tags per tracking-plan row. Prefer robust triggers in this order: dataLayer events pushed by the site/plugin (most reliable) > element visibility of a thank-you state > click triggers on stable selectors (tel:, wa.me, mailto: via Click URL contains) > form-submit listener (flaky on AJAX forms — verify hard).
- Params via dataLayer variables where possible; page-derived (URL/path regex) as fallback.
- **SPA sites (Angular/React/Vue): add a History Change trigger** and fire the Google tag/page_view on it, or every post-load navigation is invisible. Test multi-page journeys in Preview specifically.
- Consent mode v2 (EU/UK traffic or client requests it): default-denied consent state + CMP integration before any personalization tags. For India-only local businesses, note the decision in the xlsx rather than building it.
- Built-in variables: enable Click URL/Classes/Element, Form ID, History fragments as needed.

## Verification (Preview, then live)

1. Preview mode → perform every tracking-plan action on the real site: watch each tag fire exactly once, with correct params (check the API call tab). Screenshot each firing tag for the client PDF.
2. Check for double-fires (tag firing on both dataLayer event and click trigger).
3. Publish only after user confirmation; version note lists the events added.
4. Post-publish: re-test one event live (not preview) and see it in GA4 Realtime — preview-passes-live-fails happens (consent blockers, published version mismatch).

## Common traps

- AJAX forms that never navigate: the classic Form trigger won't fire — use the plugin's dataLayer push (CF7, WPForms, Elementor forms all have known events) or element visibility of the success message.
- Click triggers on nested elements: enable "wait for tags" carefully; prefer Click URL over Click Text (text changes, URLs less so).
- GTM published but site cached: WordPress/CDN cache serves old HTML without the snippet — purge cache, then verify.
- Duplicate containers (old agency's GTM still in the theme) → decide with the user which survives; never leave two firing GA4 pageviews.
