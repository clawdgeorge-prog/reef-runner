#!/usr/bin/env python3
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DATA.mkdir(parents=True, exist_ok=True)
CONFIG = json.loads((BASE / "config.json").read_text())

ARTICLES_PATH = DATA / "articles.json"
SOURCES_PATH = DATA / "sources.json"
REPORT_PATH = DATA / "latest_discovery_report.md"

UTC = timezone.utc


def now_utc():
    return datetime.now(UTC)


def iso(dt):
    return dt.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return default
    return default


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True))


def fetch(url, timeout=25):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 Chrome/122 Safari/537.36"
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def resolve_final_url(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.geturl()
    except Exception:
        return url


def is_relevant(query, title, source_name):
    text = f"{query} {title} {source_name}".lower()
    must_have_any = [
        "rural health", "rural hospital", "critical access", "forhp", "flex", "ship", "telehealth", "medicaid", "maternal", "workforce", "nrha", "healthcare"
    ]
    if not any(term in text for term in must_have_any):
        return False
    blocked = ["iran", "oil reserves", "ships in gulf", "war in", "navy", "cruise ship"]
    if any(term in text for term in blocked):
        return False
    return True


def parse_google_news_rss(query, limit=8):
    q = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={q}+when:7d&hl=en-US&gl=US&ceid=US:en"
    raw = fetch(url)
    root = ET.fromstring(raw)
    items = []
    for item in root.findall("./channel/item")[: limit * 2]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = item.findtext("pubDate") or ""
        source = item.find("source")
        source_name = (source.text or "").strip() if source is not None else ""
        try:
            published_at = parsedate_to_datetime(pub).astimezone(UTC)
        except Exception:
            published_at = now_utc()
        if " - " in title:
            title = title.rsplit(" - ", 1)[0].strip()
        if not is_relevant(query, title, source_name):
            continue
        final_link = resolve_final_url(link)
        items.append(
            {
                "query": query,
                "title": title,
                "link": final_link,
                "google_news_link": link,
                "source": source_name,
                "published_at": iso(published_at),
            }
        )
        if len(items) >= limit:
            break
    return items


def domain_from_url(url):
    try:
        host = urllib.parse.urlparse(url).netloc.lower()
        return host[4:] if host.startswith("www.") else host
    except Exception:
        return ""


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:120]


def score_article(article):
    score = 0
    title = (article.get("title") or "").lower()
    q = (article.get("query") or "").lower()
    source = (article.get("source") or "").lower()
    boost_terms = {
        "conference": 3,
        "program": 2,
        "funding": 2,
        "grant": 2,
        "telehealth": 2,
        "medicaid": 2,
        "hospital": 2,
        "closure": 3,
        "workforce": 2,
        "policy": 2,
        "rural": 2,
        "health": 1,
        "success": 2,
        "award": 1,
        "expansion": 2,
        "partnership": 2,
    }
    for term, pts in boost_terms.items():
        if term in title:
            score += pts
        if term in q:
            score += 1
    if source in {"modern healthcare", "becker's hospital review", "fierce healthcare", "kff health news", "health affairs"}:
        score += 2
    try:
        age_hours = (now_utc() - datetime.fromisoformat(article["published_at"].replace("Z", "+00:00"))).total_seconds() / 3600
        score += max(0, 72 - age_hours) / 24
    except Exception:
        pass
    return round(score, 2)


def main():
    articles_db = load_json(ARTICLES_PATH, {"articles": [], "updated_at": None})
    sources_db = load_json(SOURCES_PATH, {"sources": [], "updated_at": None})

    article_map = {a.get("id"): a for a in articles_db.get("articles", []) if a.get("id")}
    source_map = {s.get("source_key"): s for s in sources_db.get("sources", []) if s.get("source_key")}
    discovered_now = []
    fetched = 0

    for query in CONFIG["queries"]:
        try:
            items = parse_google_news_rss(query, CONFIG.get("max_results_per_query", 8))
        except Exception as e:
            print(f"WARN failed query {query!r}: {e}", file=sys.stderr)
            continue
        time.sleep(1)
        for item in items:
            fetched += 1
            domain = domain_from_url(item["link"])
            source_key = (item.get("source") or domain or "unknown").lower()
            article_id = slugify(item["title"] + "-" + source_key)
            item["id"] = article_id
            item["domain"] = domain
            item["source_key"] = source_key
            item["score"] = score_article(item)
            existing = article_map.get(article_id, {})
            item["first_seen_at"] = existing.get("first_seen_at", iso(now_utc()))
            item["last_seen_at"] = iso(now_utc())
            article_map[article_id] = {**existing, **item}

            if source_key and source_key not in source_map:
                source_map[source_key] = {
                    "source_key": source_key,
                    "name": item.get("source") or domain or "Unknown source",
                    "domain": domain,
                    "first_seen_at": iso(now_utc()),
                    "last_seen_at": iso(now_utc()),
                    "example_title": item["title"],
                    "example_link": item["link"],
                    "tags": sorted({item["query"]}),
                    "discovered_via": "google_news_rss",
                }
                discovered_now.append(source_map[source_key])
            elif source_key:
                source_map[source_key]["last_seen_at"] = iso(now_utc())
                if domain and not source_map[source_key].get("domain"):
                    source_map[source_key]["domain"] = domain
                tags = set(source_map[source_key].get("tags", []))
                tags.add(item["query"])
                source_map[source_key]["tags"] = sorted(tags)

    max_age = timedelta(days=CONFIG.get("max_story_age_days", 7))
    cutoff = now_utc() - max_age
    kept_articles = []
    for art in article_map.values():
        try:
            dt = datetime.fromisoformat(art["published_at"].replace("Z", "+00:00"))
        except Exception:
            dt = now_utc()
        if dt >= cutoff and is_relevant(art.get("query", ""), art.get("title", ""), art.get("source", "")):
            kept_articles.append(art)

    kept_articles.sort(key=lambda a: (a.get("score", 0), a.get("published_at", "")), reverse=True)
    articles_db = {"updated_at": iso(now_utc()), "articles": kept_articles}
    sources = list(source_map.values())
    sources.sort(key=lambda s: s.get("last_seen_at", ""), reverse=True)
    sources_db = {"updated_at": iso(now_utc()), "sources": sources}
    save_json(ARTICLES_PATH, articles_db)
    save_json(SOURCES_PATH, sources_db)

    top_domains = Counter((a.get("source") or a.get("domain")) for a in kept_articles if (a.get("source") or a.get("domain"))).most_common(10)
    lines = [
        f"# Rural Health Discovery Report ({now_utc().date().isoformat()})",
        "",
        f"- Queries run: {len(CONFIG['queries'])}",
        f"- Stories fetched: {fetched}",
        f"- Stories stored (last {CONFIG.get('max_story_age_days', 7)}d): {len(kept_articles)}",
        f"- New domains discovered tonight: {len(discovered_now)}",
        "",
        "## New domains",
    ]
    if discovered_now:
        for src in discovered_now[:20]:
            label = src.get('name') or src.get('domain') or src.get('source_key')
            lines.append(f"- {label} — {src['example_link']}")
    else:
        lines.append("- No new domains tonight")
    lines += ["", "## Most active domains"]
    for domain, count in top_domains:
        lines.append(f"- {domain}: {count} stories")
    REPORT_PATH.write_text("\n".join(lines) + "\n")

    print(json.dumps({
        "queries": len(CONFIG["queries"]),
        "stories_fetched": fetched,
        "stories_stored": len(kept_articles),
        "new_domains": len(discovered_now),
        "report": str(REPORT_PATH)
    }))


if __name__ == "__main__":
    main()
