# Mockup spec — the single HTML file

The mockup is a sales asset. The client should open it and think "this is my new website", not "this is a sketch of it".

## Technical requirements

- One self-contained `.html` file: inline CSS + JS, no build step, no external dependencies except Google Fonts and (if needed) a single icon set via CDN. It must render perfectly from a double-click on any machine and survive being emailed.
- Fully responsive — design mobile and desktop simultaneously; test at 375px and 1440px before presenting. Mobile gets its own attention: collapsible nav, sticky primary CTA (call/WhatsApp for local businesses), touch-sized targets.
- Working interactions: navigation (smooth-scroll anchors or simple JS tab switching for "inner pages"), hover states, FAQ accordions, mobile menu, subtle scroll-reveal if the DNA calls for motion. Forms are visual (fake submit → success state) — never wired to anything.
- Images: prefer CSS/SVG art direction (gradients, patterns, abstract shapes, inline SVG illustrations) over external images — self-contained and always loads. Where photography is essential to the DNA, use neutral placeholder treatment (styled blocks with descriptive labels) the user can swap, or properly-licensed sources if instructed.
- Weight: keep under ~500KB. No frameworks — hand-rolled CSS gives the bespoke look and avoids Tailwind-default sameness.

## Content requirements

- Real company facts from Stage-1 research: actual services, real phone/locations/hours, real review scores where found. Fabricated specifics (testimonial names, exact stats) are marked `<!-- PLACEHOLDER: confirm with client -->` and flagged in the presentation message.
- Copywriting in the reference's voice, but concrete: headline states the value, subhead states for whom, CTA states the action. No "Welcome to our website".
- Include what the industry demands (see design-dna.md archetypes): trust signals, pricing anchors, service areas, credentials.
- SEO-shaped even as a mockup: one h1, logical heading tree, semantic sections — becomes free work at build time.

## Structure (typical, adapt per business)

Hero (value + primary CTA) → social proof strip → services/products → differentiator ("why us" with evidence) → deep-dive or case section → testimonials/reviews → FAQ (real buyer questions) → final CTA → full footer (NAP, links, hours). "Inner pages" the client cares about (services detail, about, contact) appear as navigable sections or JS-tabbed views so the single file demos the whole site concept.

## Presenting

Save as `Website Engine/<company>/mockup-v<N>.html`, present the file, and include: the one-paragraph DNA sheet (per design-dna.md), the list of placeholders needing client confirmation, and the question "WordPress or code?" if the build path is still open. Feedback → new version file, never overwrite (the version trail is part of the pitch record).
