# CLAUDE.md — how to run this repo

This is a weekly content generation system for local-service-business marketing.

## Files
- `week_content.py` — **single source of truth** for the current week (video
  scripts + story plans + DM keywords + theme metadata). Both scripts import it.
- `push_content.py` — pushes the week to Notion (clears + rebuilds 7 day pages, verifies).
- `daily_story.py` — renders IG Story PNGs from real photos.
- `CONTENT_RULES.md` — **the rules every week must follow. Read it before writing any content.**
- `ARCHIVE.md` — log of past hooks/frameworks/angles. **Never repeat what's in here.**
- `.env` — secrets/config (git-ignored): `NOTION_TOKEN`, `IG_HANDLE`, `PHOTO_DIR`,
  and optional `NOTION_PARENT_PAGE`.

## How this pushes to Notion — TWO paths

**Path A — Notion connector (PRIMARY, what's in use).** This workspace reaches
Notion through the **Notion MCP connector** (routed via Anthropic, so it works
even when the sandbox network policy blocks `api.notion.com`). The live pages
already exist — see `NOTION_PAGES.md` for the parent + 7 day-page IDs. To refresh
a week, **update those pages in place** with the Notion tools
(`notion-update-page`, `command:"replace_content"`), one day per page. Do NOT
create new pages each week — reuse the IDs so links stay stable.

**Path B — REST API script (fallback).** `push_content.py` hits `api.notion.com`
directly with a token. Only works if the environment's network policy allows
Notion (Custom/Full + `api.notion.com`) and `NOTION_TOKEN` is set. Auto-creates
day pages under `NOTION_PARENT_PAGE`. Use `--dry-run` to build+count with no
network.

### Notion connector markdown gotchas (learned the hard way)
- Each script line goes on **its own line** → each becomes its own block
  ("one line per breath"). Blank lines between them are stripped, that's fine.
- **Escape STAR label brackets**: write `\[S — SHOCK, spoken\]:` not `[...]:`,
  or Notion treats the line as a link-reference definition and hides it.
- **Escape dollar signs**: `\$1,500` (bare `$…$` can trigger math).
- Video = `<details><summary>**Video N — Style**</summary> … </details>` toggle.
- Story slide colors = `<span color="red|green|orange">…</span>`.
- Day theme header = `<callout icon="🔧" color="blue_bg">**Day — Theme**</callout>`.

## Weekly cadence — when the user says "update all content for the week"
1. Read `CONTENT_RULES.md` and `ARCHIVE.md`.
2. Write a **fresh themed week** into `week_content.py` — new angle, new named
   frameworks/roadmaps, new hooks, new DM keywords. Nothing may repeat `ARCHIVE.md`.
3. Keep the fixed weekly themes (Mon One Specific Fix … Sat Objection Crusher,
   Sun rest), the 4-videos/day + STAR + format rotation (Clone ~2×, Miro ~2×,
   no carousels), and the 3-stories/day (poll / proof-or-agitate / CTA; Thursday Q&A).
4. **Push (Path A):** for each day in `NOTION_PAGES.md`, `notion-update-page`
   with `replace_content` and that day's markdown. Then `notion-fetch` the parent
   to confirm all 7 still nest and counts look right. (Or Path B if Notion is
   network-allowed: `python push_content.py`.)
5. `python daily_story.py all` — regenerate all story images (needs the photos).
6. Append the new week to `ARCHIVE.md`.

> Requires the **Notion connector enabled in the chat**. If Notion tools aren't
> available, tell the user to enable the Notion connector for this session.

## Notes
- Never commit `.env`, `notion_pages.json`, `story_output/`, or client photos.
- Notion API version pinned to `2022-06-28`; all calls use a retrying session.
