# Rural Health Monitor

Tracks rural-health news and source discovery for Brant / REDi Health.

## What it does

- Nightly discovery job searches fresh rural-health queries via Google News RSS.
- Stores recent stories and newly discovered domains locally.
- Morning digest job turns that into a readable daily briefing with links.

## Files

- `config.json` — search topics and seed sources
- `discover.py` — nightly discovery / source discovery
- `digest.py` — morning summary generator
- `data/articles.json` — recent captured stories
- `data/sources.json` — discovered source registry
- `data/latest_discovery_report.md` — latest discovery run report

## Focus areas

- Rural healthcare in the United States
- RHTP / rural transformation-related coverage
- FLEX, SHIP, FORHP, CMS, HRSA
- Conferences, funding, success stories, competitors, and market moves

## Manual run

```bash
python3 rural-health-monitor/discover.py
python3 rural-health-monitor/digest.py
```
