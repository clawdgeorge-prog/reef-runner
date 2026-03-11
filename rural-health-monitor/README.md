# Rural Health Monitor

Tracks rural-health news and source discovery for Brant / REDi Health.

## What it does

- Nightly discovery job searches fresh rural-health queries via Google News RSS.
- Stores recent stories and newly discovered domains locally.
- Morning digest job turns that into a readable daily briefing with links.
- Event pipeline marks high-confidence calendar-ready events.
- Google Calendar sync can create/find the rural-health calendar and sync calendar-ready events.

## Files

- `config.json` — search topics and seed sources
- `discover.py` — nightly discovery / source discovery
- `digest.py` — morning summary generator
- `events_export.py` — event-oriented export from recent stories
- `event_pipeline.py` — event scoring, date extraction, review queue, CSV export
- `google_calendar_sync.py` — sync calendar-ready events to Google Calendar
- `data/articles.json` — recent captured stories
- `data/sources.json` — discovered source registry
- `data/latest_discovery_report.md` — latest discovery run report
- `data/event_candidates.json` — scored event candidates
- `data/event_review_queue.md` — human-readable event queue
- `data/calendar_state.json` — synced Google calendar id + event ids

## Focus areas

- Rural healthcare in the United States
- RHTP / rural transformation-related coverage
- FLEX, SHIP, FORHP, CMS, HRSA
- Conferences, funding, success stories, competitors, and market moves

## Manual run

```bash
python3 rural-health-monitor/discover.py
python3 rural-health-monitor/events_export.py
python3 rural-health-monitor/event_pipeline.py
python3 rural-health-monitor/google_calendar_sync.py
python3 rural-health-monitor/digest.py
```

## Secrets / auth

Google OAuth secrets and token are stored outside the workspace in:

- `/Users/georgeclawd/.openclaw/secrets/google/credentials.json`
- `/Users/georgeclawd/.openclaw/secrets/google/token.json`

Virtualenv for Google libraries:

- `/Users/georgeclawd/.openclaw/google-tools/venv`
