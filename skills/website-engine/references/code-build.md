# Code build runbook — static site + Netlify

The approved mockup expands into a production multi-page static site. No framework unless the user asks — hand-written HTML/CSS/JS is faster to build, trivially hostable, and scores ~100 on performance by default.

## Project structure

```
<company>-site/
├── index.html
├── <page>.html            (one per real page: services, about, contact, per-service pages)
├── css/main.css           (extracted from mockup, shared)
├── js/main.js             (nav, accordions, reveals — shared)
├── img/                   (optimized: WebP/AVIF + width variants where it matters)
├── sitemap.xml, robots.txt, llms.txt, favicon set, 404.html
└── netlify.toml           (redirects, headers)
```

- Factor the mockup's inline CSS/JS into the shared files; keep the design tokens as CSS variables at `:root` so client tweaks stay one-line.
- Every "inner page" concept from the mockup becomes a real page with its own full content — expand, don't stub. Consistent header/footer across pages (copy exactly; there's no templating — a mismatch looks broken).
- Forms: Netlify Forms (`data-netlify="true"`) with a styled success page, plus honeypot field for spam — zero-backend and actually works. Confirm the receiving email with the user.

## SEO/AEO at birth (non-negotiable — sites from this engine should pass the seo-audit-engine)

- Per page: unique title (30–60ch, keyword + differentiator), meta description, canonical, one h1, semantic heading tree, answer-first opening paragraph.
- JSON-LD: Organization/LocalBusiness sitewide; Service / FAQPage / BreadcrumbList per page type. Real NAP data.
- OG + Twitter card meta with a default share image; `lang` attribute; descriptive alt text everywhere.
- sitemap.xml (only real pages), robots.txt (allow all incl. AI crawlers), llms.txt with markdown links to key pages.
- Performance: inline critical CSS if needed, `loading="lazy"` below-fold images, font-display swap, no render-blocking third-party JS. Target Lighthouse ≥90 across the board; actually run it and check.

## Netlify deploy

1. Deploy via Netlify CLI (`npx netlify-cli deploy --prod --dir .`) or the drop UI: if the CLI needs auth interactively, prepare everything and hand the final auth/deploy step to the user rather than handling their credentials.
2. `netlify.toml`: trailing-slash consistency, 301s for any planned URL moves, security headers (X-Frame-Options, referrer-policy), long-cache for /css /js /img.
3. Verify live: click through every page on the live URL, run a Lighthouse pass, test the form end-to-end (real submission arrives), check 404 page.
4. Custom domain: give the user the exact DNS records (A/ALIAS/CNAME) to add — DNS changes are theirs to make. Cloudflare-hosted deploys are also theirs (prep files, don't drive the CF dashboard).

## Handover

Deliver: live Netlify URL, the full project folder in `Website Engine/<company>/site/`, DNS instructions, a short "how to request changes" note (edits go through the user, not the client hacking files), Lighthouse scores, and the suggestion to run analytics-setup-engine + seo-audit-engine next.
