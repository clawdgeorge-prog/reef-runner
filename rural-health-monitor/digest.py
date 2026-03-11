#!/usr/bin/env python3
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
CONFIG = json.loads((BASE / "config.json").read_text())
ARTICLES = json.loads((DATA / "articles.json").read_text()) if (DATA / "articles.json").exists() else {"articles": []}
SOURCES = json.loads((DATA / "sources.json").read_text()) if (DATA / "sources.json").exists() else {"sources": []}
UTC = timezone.utc


def parse_iso(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def classify(article):
    text = f"{article.get('query','')} {article.get('title','')}".lower()
    rules = [
        ("Announcements & Funding", ["grant", "funding", "award", "program", "initiative", "appropriation"]),
        ("Competitor / Market Intel", ["partnership", "acquisition", "launch", "expansion", "competitor", "vendor", "technology"]),
        ("Policy & Programs", ["flex", "ship", "forhp", "cms", "hrsa", "medicaid", "medicare", "policy", "rule"]),
        ("Conferences & Events", ["conference", "summit", "webinar", "forum", "annual meeting"]),
        ("Success Stories & Operations", ["success", "improved", "turnaround", "quality", "workforce", "telehealth", "maternal", "closure", "hospital"]),
    ]
    for label, terms in rules:
        if any(t in text for t in terms):
            return label
    return "General Rural Health"


def short_time(dt):
    hours = int((datetime.now(UTC) - dt).total_seconds() // 3600)
    if hours < 24:
        return f"{hours}h ago"
    return f"{hours // 24}d ago"


def main():
    now = datetime.now(UTC)
    recent_cutoff = now - timedelta(days=1)
    recent = []
    for article in ARTICLES.get("articles", []):
        try:
            dt = parse_iso(article["published_at"])
        except Exception:
            continue
        if dt >= recent_cutoff:
            article = dict(article)
            article["dt"] = dt
            recent.append(article)

    recent.sort(key=lambda a: (a.get("score", 0), a["dt"]), reverse=True)
    buckets = defaultdict(list)
    for art in recent:
        buckets[classify(art)].append(art)

    discovered_cutoff = now - timedelta(days=1)
    new_sources = []
    for src in SOURCES.get("sources", []):
        try:
            dt = parse_iso(src["first_seen_at"])
        except Exception:
            continue
        if dt >= discovered_cutoff:
            new_sources.append(src)
    new_sources.sort(key=lambda s: s.get("first_seen_at", ""), reverse=True)

    lines = []
    lines.append(f"Rural Healthcare Daily Update — {now.astimezone().date().isoformat()}")
    lines.append("")
    lines.append("Top line: nightly monitor scanned rural-health queries, refreshed tracked stories, and surfaced new domains for RHTP/FLEX/SHIP and broader rural-health intel.")
    lines.append("")

    if not recent:
        lines.append("No fresh stories were captured in the last 24h. The discovery pipeline ran, but nothing new cleared the relevance filter.")
    else:
        for section in [
            "Announcements & Funding",
            "Policy & Programs",
            "Competitor / Market Intel",
            "Success Stories & Operations",
            "Conferences & Events",
            "General Rural Health",
        ]:
            items = buckets.get(section, [])[:3]
            if not items:
                continue
            lines.append(section)
            for art in items:
                lines.append(f"- {art['title']} ({art.get('source') or art.get('domain','unknown')}, {short_time(art['dt'])})")
                lines.append(f"  Link: {art['link']}")
                lines.append(f"  Why it matters: surfaced from '{art.get('query','rural health monitoring')}' and scored as relevant for rural-health ops / market awareness.")
            lines.append("")

    lines.append("New source domains discovered last night")
    if new_sources:
        for src in new_sources[:10]:
            label = src.get('name') or src.get('domain') or src.get('source_key')
            lines.append(f"- {label} — example: {src['example_link']}")
    else:
        lines.append("- No new domains discovered in the last 24h.")
    lines.append("")

    lines.append("Tracked themes")
    lines.append("- Rural hospital finance / closures")
    lines.append("- Federal and state rural programs (FORHP, FLEX, SHIP, telehealth, workforce)")
    lines.append("- Competitor and partner activity")
    lines.append("- Conferences, webinars, and showcase stories")
    lines.append("")

    lines.append("Reference files")
    lines.append(f"- Discovery report: file://{(DATA / 'latest_discovery_report.md').resolve()}")
    lines.append(f"- Story database: file://{(DATA / 'articles.json').resolve()}")
    lines.append(f"- Source registry: file://{(DATA / 'sources.json').resolve()}")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
