# Deriving the per-client tracking plan

The event set comes from the client's business model, not a template. Work backwards: how does this business make money → what website actions predict that revenue → those are the key events. Everything else is supporting context.

## The derivation questions

1. What is a "lead" or "sale" for this client, concretely? (a form? a call? a WhatsApp message? an order? a booking? a demo?)
2. Which of those happen ON the website vs off it (walk-ins, marketplace)? Track the on-site ones; note the off-site gap in the one-pager.
3. What earlier actions signal intent? (pricing page view, fare-estimate use, brochure download, 3+ service pages viewed)
4. What does the client already ask about? ("how many calls came from the site?") — guaranteed key events.
5. What content decisions will this data feed? (SEO/content teams need landing-page × query × engagement views — this shapes reports more than events)

## Event naming

snake_case, verb_noun, GA4-reserved-names avoided, consistent across clients: `form_submit`, `phone_click`, `whatsapp_click`, `email_click`, `quote_request`, `estimate_used`, `brochure_download`, `booking_complete`. Parameters carry the detail (`form_id`, `link_url`, `service_name`, `city`) — don't mint per-form event names.

## Industry starting points (starting points, not templates)

- **Local/field services** (movers, clinics, repair): phone_click + whatsapp_click usually beat forms in India — make both key events. form_submit, quote_request, direction/map clicks, per-city landing page engagement. GBP traffic will show as organic — note it.
- **Ecommerce**: use the standard GA4 ecommerce schema (view_item, add_to_cart, begin_checkout, purchase) via dataLayer — do not invent parallel names. Platform plugins (Shopify, WooCommerce) may already push these; audit before adding.
- **SaaS/B2B**: sign_up, demo_request, pricing_view, trial_start, docs engagement; longer cycles → key events are the top-of-funnel commits.
- **Content/publisher**: engaged reads (scroll 75% + 30s), newsletter_signup, outbound affiliate clicks.

## Key-event discipline

3–6 key events maximum. A key event = the client would want to be texted about it. Marking everything "key" destroys the signal and pollutes any future ads optimization. Scroll depth is a diagnostic, not a key event.

## The sign-off table (present in chat before building)

| # | Business goal | Event | Trigger (plain words) | Params | Key event? | Surfaces in |
|---|---------------|-------|----------------------|--------|-----------|-------------|

Get explicit approval, then this exact table drives GTM config, GA4 key-event marking, the xlsx, and the one-pager. Any event added mid-build goes back through a quick confirm.
