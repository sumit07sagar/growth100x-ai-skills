# GSC setup runbook

## Property setup

1. Prefer a **Domain property** (covers http/https, www/non-www, subdomains) — requires DNS TXT verification, which the client's team usually has to add. Prepare the exact TXT record text for them. If DNS is slow/unavailable, create a URL-prefix property on the canonical origin (e.g. `https://www.client.com/`) now and migrate to domain property later; verification via GA/GTM works when the agency's tag is already live.
2. If the client granted access to their existing property, audit rather than create: right property type? Canonical host? Old disused properties causing confusion?
3. Access: the client adds the agency email; verified-owner status survives staff changes better than delegated — record who owns what in the xlsx Access log.

## Baseline configuration + checks (do all, screenshot key ones)

- Submit sitemap(s); confirm status "Success" and discovered-URL count is sane vs the site's real page count. Both www/non-www sitemaps if URL-prefix properties are split (then fix the split).
- Indexing > Pages: indexed vs excluded counts and the top exclusion reasons — this is the "before" snapshot.
- URL-inspect the homepage + 3–5 money pages: indexed? canonical Google chose = canonical declared? Request indexing for critical unindexed pages.
- Security & Manual actions: confirm both clean (screenshot — clients love this proof).
- Removals: check nothing unexpected is suppressed.
- Settings: crawler stats sane; association with the GA4 property (Settings > Associations, or from GA4 side per ga4-setup.md).
- Note Performance data lag (~2 days) and that a fresh property starts with zero history — set expectation in deliverables.

## Common traps

- Sitemap URL 301s (e.g. old domain in robots.txt) → submit the final URL. Stale robots.txt sitemap lines are a real, common finding — fix at source too.
- Domain property + separate old URL-prefix properties: keep both temporarily (URL-prefix retains history), but report from one.
- "Discovered – currently not crawled" on a small site usually = weak internal linking or crawl-unfriendly rendering, not a GSC problem.
