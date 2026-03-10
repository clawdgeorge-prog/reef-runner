# MODEL_ROUTING.md

## Default policy

### Main session (George + Brant)
- Use **OpenAI Codex** when configured.
- Current preferred main model: `openai-codex/gpt-5.4`
- Use this for: high-value conversation, nuanced reasoning, important planning, sensitive writing, and tasks where quality matters more than cost.

### Subagents / spawned work
- Default to **MiniMax** unless Brant explicitly agrees otherwise.
- Preferred default worker model: `minimax/MiniMax-M2.5`
- Use this for: scraping, cron jobs, X/news collection, recurring research, browser chores, batch work, and routine file updates.

## When to keep work on MiniMax
- Cron jobs
- X scraping / trending / news digests
- Repetitive research collection
- Background browsing
- Multi-step but low-stakes automation
- Any task likely to run frequently or burn lots of tokens

## When to ask before using OpenAI for workers
Only move a subagent or cron workload to OpenAI if Brant and George agree first.
Typical reasons:
- materially better reasoning is needed
- writing quality matters a lot
- hard synthesis / judgment call
- important coding/debugging where better model quality may save time

## Cron guidance
- Pin routine cron payloads to `minimax/MiniMax-M2.5`
- Do not let routine cron jobs inherit the main OpenAI model by accident
- Prefer explicit Telegram delivery (`channel: telegram`, `to: 8544038857`) over vague/last-session delivery for important recurring jobs
- Use `delivery.mode: none` for silent maintenance jobs like vector-memory housekeeping

## Current preference from Brant
- George/main session on OpenAI
- routine scraping and cron jobs on MiniMax
- spawned agents default to MiniMax
- OpenAI for non-main workers only by explicit agreement
