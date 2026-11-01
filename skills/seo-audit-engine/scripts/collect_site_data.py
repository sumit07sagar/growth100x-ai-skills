#!/usr/bin/env python3
"""SEO Audit Engine - live site data collector.

Usage:
    python collect_site_data.py example.com --output audit_data.json --pages 12

Collects robots.txt (AI-crawler access matrix), sitemaps, llms.txt,
homepage + sampled pages (on-page extraction), site-level hygiene checks,
and PageSpeed Insights (mobile + desktop) for the homepage.
Outputs a single JSON file. Requires: requests, beautifulsoup4.
"""
import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36 SEOAuditEngine/1.0")

AI_CRAWLERS = [
    "GPTBot", "ChatGPT-User", "OAI-SearchBot",           # OpenAI
    "ClaudeBot", "Claude-User", "Claude-SearchBot", "anthropic-ai",  # Anthropic
    "PerplexityBot", "Perplexity-User",                   # Perplexity
    "Google-Extended", "GoogleOther",                     # Google AI
    "Bingbot", "CCBot", "Amazonbot", "meta-externalagent", "Applebot-Extended",
]

session = requests.Session()
session.headers.update({"User-Agent": UA})


def get(url, timeout=12, retries=1, **kw):
    """GET with one short backoff on 429/503 (WP/CDN rate limits are common)."""
    for attempt in range(retries + 1):
        try:
            r = session.get(url, timeout=timeout, allow_redirects=True, **kw)
        except requests.RequestException as e:
            return e
        if r.status_code in (429, 503) and attempt < retries:
            time.sleep(2)
            continue
        return r
    return r


def parse_robots(text):
    """Return {crawler: 'allowed'|'blocked'|'partial'} + sitemap urls."""
    groups, current_agents, rules = [], [], []
    for raw in text.splitlines():
        line = raw.split("#")[0].strip()
        if not line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip().lower(), val.strip()
        if key == "user-agent":
            if rules:
                groups.append((current_agents, rules))
                current_agents, rules = [], []
            current_agents.append(val.lower())
        elif key in ("allow", "disallow") and current_agents:
            rules.append((key, val))
    if current_agents:
        groups.append((current_agents, rules))

    sitemaps = re.findall(r"(?im)^sitemap:\s*(\S+)", text)

    def status_for(agent):
        agent_l = agent.lower()
        matched = None
        for agents, rls in groups:
            if agent_l in agents:
                matched = rls
                break
        if matched is None:
            for agents, rls in groups:
                if "*" in agents:
                    matched = rls
                    break
        if matched is None:
            return "allowed"
        dis = [v for k, v in matched if k == "disallow"]
        if any(v == "/" for v in dis):
            return "blocked"
        return "partial" if dis else "allowed"

    return {c: status_for(c) for c in AI_CRAWLERS}, sitemaps


FETCH_NOTES = []


def fetch_sitemap_urls(sm_url, limit=2000, depth=0):
    if depth > 2:
        return []
    r = get(sm_url)
    if isinstance(r, Exception) or r.status_code != 200:
        FETCH_NOTES.append(f"{sm_url} -> "
                           f"{r if isinstance(r, Exception) else 'HTTP ' + str(r.status_code)}")
        return []
    urls, is_index = [], "<sitemapindex" in r.text[:2000]
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)
    if is_index:
        for child in locs[:6]:
            time.sleep(0.5)  # be gentle; WP/CDNs 429 on burst requests
            urls.extend(fetch_sitemap_urls(child, limit - len(urls), depth + 1))
            if len(urls) >= limit:
                break
    else:
        urls = locs[:limit]
    return urls


def analyze_page(url):
    r = get(url)
    if isinstance(r, Exception):
        return {"url": url, "error": str(r)}
    out = {"url": url, "final_url": r.url, "status": r.status_code,
           "redirected": r.url.rstrip("/") != url.rstrip("/")}
    ctype = r.headers.get("Content-Type", "")
    if r.status_code != 200 or "html" not in ctype:
        return out
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    md = soup.find("meta", attrs={"name": "description"})
    canon = soup.find("link", rel="canonical")
    robots_meta = soup.find("meta", attrs={"name": "robots"})

    headings = []
    for h in soup.find_all(re.compile(r"^h[1-6]$")):
        headings.append({"tag": h.name, "text": h.get_text(" ", strip=True)[:120]})

    schema_types = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
            items = data if isinstance(data, list) else [data]
            for it in items:
                if isinstance(it, dict):
                    graph = it.get("@graph", [it])
                    for g in graph:
                        if isinstance(g, dict) and g.get("@type"):
                            t = g["@type"]
                            schema_types.extend(t if isinstance(t, list) else [t])
        except (json.JSONDecodeError, TypeError):
            schema_types.append("INVALID_JSONLD")

    host = urlparse(r.url).netloc
    internal = external = 0
    for a in soup.find_all("a", href=True):
        href = urljoin(r.url, a["href"])
        p = urlparse(href)
        if p.scheme in ("http", "https"):
            if p.netloc.replace("www.", "") == host.replace("www.", ""):
                internal += 1
            else:
                external += 1

    imgs = soup.find_all("img")
    imgs_no_alt = sum(1 for i in imgs if not (i.get("alt") or "").strip())

    # answer-first: first substantial paragraph within first 600 chars of text
    first_para = ""
    for p in soup.find_all("p"):
        t = p.get_text(" ", strip=True)
        if len(t) > 60:
            first_para = t[:400]
            break

    og = {m.get("property"): (m.get("content") or "")[:200]
          for m in soup.find_all("meta") if (m.get("property") or "").startswith("og:")}
    tw = {m.get("name"): (m.get("content") or "")[:200]
          for m in soup.find_all("meta") if (m.get("name") or "").startswith("twitter:")}

    # crude JS-dependency signal: little text but big HTML, or root app containers
    js_shell = bool(len(text) < 400 and (
        soup.find(id="root") or soup.find("app-root") or soup.find(id="app") or "__NEXT_DATA__" in html))

    out.update({
        "title": title, "title_length": len(title),
        "meta_description": (md.get("content", "") if md else "")[:400],
        "meta_description_length": len(md.get("content", "")) if md else 0,
        "canonical": canon.get("href") if canon else None,
        "robots_meta": robots_meta.get("content") if robots_meta else None,
        "h1_count": sum(1 for h in headings if h["tag"] == "h1"),
        "headings": headings[:40],
        "word_count": len(text.split()),
        "schema_types": sorted(set(map(str, schema_types))),
        "internal_links": internal, "external_links": external,
        "images": len(imgs), "images_missing_alt": imgs_no_alt,
        "first_paragraph": first_para,
        "og_tags": og, "twitter_tags": tw,
        "lang": (soup.html.get("lang") if soup.html else None),
        "viewport": bool(soup.find("meta", attrs={"name": "viewport"})),
        "hreflang_count": len(soup.find_all("link", rel="alternate", hreflang=True)),
        "likely_js_rendered_shell": js_shell,
        "compression": r.headers.get("Content-Encoding"),
        "cache_control": r.headers.get("Cache-Control"),
        "html_kb": round(len(html) / 1024, 1),
    })
    return out


def psi(url, strategy):
    api = ("https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
           f"?url={url}&strategy={strategy}"
           "&category=performance&category=seo&category=accessibility&category=best-practices")
    r = get(api, timeout=90)
    if isinstance(r, Exception) or r.status_code != 200:
        return {"error": str(r) if isinstance(r, Exception) else f"HTTP {r.status_code}"}
    d = r.json()
    lr = d.get("lighthouseResult", {})
    cats = lr.get("categories", {})
    audits = lr.get("audits", {})

    def metric(key):
        a = audits.get(key, {})
        return a.get("displayValue")

    out = {
        "scores": {k: round((v.get("score") or 0) * 100) for k, v in cats.items()},
        "lab": {"LCP": metric("largest-contentful-paint"), "CLS": metric("cumulative-layout-shift"),
                "TBT": metric("total-blocking-time"), "FCP": metric("first-contentful-paint"),
                "SI": metric("speed-index")},
    }
    field = d.get("loadingExperience", {})
    if field.get("metrics"):
        out["field_cwv"] = {k: v.get("category") for k, v in field["metrics"].items()}
        out["field_overall"] = field.get("overall_category")
    return out


def stage_infra(result, domain, base):
    variants = {}
    for v in (f"https://{domain}", f"http://{domain}",
              f"https://www.{domain}" if not domain.startswith("www.") else f"https://{domain[4:]}"):
        r = get(v, timeout=15)
        variants[v] = (str(r) if isinstance(r, Exception)
                       else {"status": r.status_code, "final": r.url})
    result["site_checks"] = {"variants": variants}

    r404 = get(f"{base}/definitely-not-a-page-{int(time.time())}")
    result["site_checks"]["404_returns"] = (
        str(r404) if isinstance(r404, Exception) else r404.status_code)

    r = get(f"{base}/robots.txt")
    sitemap_urls_declared = []
    if not isinstance(r, Exception) and r.status_code == 200:
        matrix, sitemap_urls_declared = parse_robots(r.text)
        result["robots"] = {"exists": True, "ai_crawler_access": matrix,
                            "declared_sitemaps": sitemap_urls_declared,
                            "raw_first_2000": r.text[:2000]}
    else:
        result["robots"] = {"exists": False,
                            "note": "No robots.txt (all crawlers allowed by default)"}

    r = get(f"{base}/llms.txt")
    result["llms_txt"] = {
        "exists": (not isinstance(r, Exception)) and r.status_code == 200
        and "html" not in r.headers.get("Content-Type", ""),
        "preview": (r.text[:1500] if not isinstance(r, Exception) and r.status_code == 200 else None)}


def stage_sitemap(result, base):
    declared = result.get("robots", {}).get("declared_sitemaps", [])
    candidates = list(dict.fromkeys(
        declared + [f"{base}/sitemap.xml", f"{base}/sitemap_index.xml"]))
    all_urls = []
    for sm in candidates[:4]:
        all_urls = fetch_sitemap_urls(sm)
        if all_urls:
            result["sitemap"] = {"url": sm, "url_count": len(all_urls),
                                 "sample": all_urls[:30], "all_urls": all_urls[:500]}
            break
    if not all_urls:
        result["sitemap"] = {"url": None, "url_count": 0,
                             "note": "No sitemap URLs retrieved — check fetch_errors before "
                                     "concluding the sitemap is missing (429 = rate-limited, "
                                     "retry this stage later)",
                             "fetch_errors": FETCH_NOTES[-8:]}


def stage_pages(result, base, n_pages, batch):
    """Analyze pages in batches so each invocation stays short. Re-run until done."""
    all_urls = result.get("sitemap", {}).get("all_urls", [])
    planned = [base]
    if all_urls:
        step = max(1, len(all_urls) // max(1, n_pages - 1))
        for u in all_urls[::step]:
            if u.rstrip("/") != base and u not in planned:
                planned.append(u)
            if len(planned) >= n_pages:
                break
    done_urls = {p["url"] for p in result.get("pages", [])}
    result.setdefault("pages", [])
    todo = [u for u in planned if u not in done_urls][:batch]
    for u in todo:
        sys.stderr.write(f"analyzing {u}\n")
        result["pages"].append(analyze_page(u))
        time.sleep(0.3)
    remaining = len([u for u in planned if u not in {p['url'] for p in result['pages']}])
    result["pages_remaining"] = remaining

    ok_pages = [p for p in result["pages"] if p.get("status") == 200 and "title" in p]
    titles = [p["title"] for p in ok_pages]
    result["rollups"] = {
        "pages_analyzed": len(ok_pages),
        "duplicate_titles": len(titles) - len(set(titles)),
        "pages_missing_meta_desc": sum(1 for p in ok_pages if not p["meta_description"]),
        "pages_multiple_or_no_h1": sum(1 for p in ok_pages if p["h1_count"] != 1),
        "pages_with_schema": sum(1 for p in ok_pages if p["schema_types"]),
        "schema_types_sitewide": sorted({t for p in ok_pages for t in p["schema_types"]}),
        "avg_word_count": (round(sum(p["word_count"] for p in ok_pages) / len(ok_pages))
                           if ok_pages else 0),
        "js_shell_pages": sum(1 for p in ok_pages if p.get("likely_js_rendered_shell")),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("domain")
    ap.add_argument("--output", default="audit_data.json")
    ap.add_argument("--pages", type=int, default=12, help="total pages to analyze")
    ap.add_argument("--batch", type=int, default=5, help="pages per invocation")
    ap.add_argument("--stage",
                    choices=["infra", "sitemap", "pages", "psi-mobile", "psi-desktop", "all"],
                    default="all",
                    help="run one stage per invocation in time-limited shells; "
                         "state accumulates in --output")
    args = ap.parse_args()

    domain = re.sub(r"^https?://", "", args.domain).strip("/")
    base = f"https://{domain}"

    # resume from existing output if present
    try:
        with open(args.output) as f:
            result = json.load(f)
        if result.get("domain") != domain:
            result = {}
    except (FileNotFoundError, json.JSONDecodeError):
        result = {}
    result.setdefault("domain", domain)
    result["collected_at"] = datetime.now(timezone.utc).isoformat()

    if args.stage in ("infra", "all"):
        stage_infra(result, domain, base)
    if args.stage in ("sitemap", "all"):
        stage_sitemap(result, base)
    if args.stage in ("pages", "all"):
        stage_pages(result, base, args.pages, args.batch if args.stage == "pages" else args.pages)
    if args.stage in ("psi-mobile",):
        result.setdefault("psi", {})["mobile"] = psi(base, "mobile")
    if args.stage in ("psi-desktop",):
        result.setdefault("psi", {})["desktop"] = psi(base, "desktop")

    with open(args.output, "w") as f:
        json.dump(result, f, indent=1)
    status = {"stage_done": args.stage,
              "pages_analyzed": len(result.get("pages", [])),
              "pages_remaining": result.get("pages_remaining"),
              "sitemap_urls": result.get("sitemap", {}).get("url_count")}
    print(json.dumps(status))


if __name__ == "__main__":
    main()
