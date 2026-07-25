# Weekly Content Generation System

A two-part machine for weekly local-service-business marketing content:

1. **`push_content.py`** — pushes a full week of video scripts + IG Story plans into Notion.
2. **`daily_story.py`** — renders finished 1080×1920 Instagram Story PNGs over your own photos.

Both read the same source of truth (`week_content.py`), so Notion and the images
never drift apart: same hooks, same named frameworks, same DM keywords.

---

## Quick start (Windows)

```bat
pip install requests pillow

:: 1) configure
copy .env.example .env
:: edit .env -> set NOTION_TOKEN, IG_HANDLE, PHOTO_DIR

:: 2) push the week to Notion (clears + rebuilds all 7 day pages, then verifies)
python push_content.py

:: 3) render this week's story images
python daily_story.py all
```

Outputs land in `story_output\<Day>\<Day>_1.png` … (the folder is wiped each run).

---

## Configuration (`.env`)

| Key | What it is |
|-----|------------|
| `NOTION_TOKEN` | Your Notion internal integration token (starts `secret_`/`ntn_`). **Never commit it** — `.env` is git-ignored. |
| `IG_HANDLE` | Watermark on every story image, e.g. `@youragency`. |
| `PHOTO_DIR` | Folder of real work photos (jpg/png/webp) used as story backgrounds. |
| `NOTION_PAGE_<DAY>` | *(optional)* pin a page ID to skip auto-discovery. |

---

## First-time Notion setup

You need **one integration** and **7 pages** (Monday…Sunday) shared with it.

1. Go to **notion.so/my-integrations** → **New integration** → name it (e.g.
   "Content Bot") → **Submit**. Copy the **Internal Integration Secret** into
   `.env` as `NOTION_TOKEN`.
2. In Notion, create 7 pages titled exactly **Monday, Tuesday, …, Sunday**
   (they can live under one parent page).
3. Share **each** page with the integration: open the page → top-right **•••**
   menu → **Connections** → add your integration. (Do this on all 7.)
4. Run `python push_content.py`. It finds each page by title via the API, no IDs
   needed. Resolved IDs are cached in `notion_pages.json`.

If a page isn't found, the script tells you which one and how to fix it.

---

## `push_content.py`

Rebuilds each day page from scratch every run:

- **Header callout** with the day's theme color + name.
- **Daily checklist** (film / captions / post IG+TikTok / 3 stories / 2 TikTok
  lives / outreach / reply for 1h).
- **4 video ideas** per day (Mon–Sat), each with: Content Style / Format,
  Content Pillar, Hook, Script, CTA, Caption.
- **Today's 3 IG Stories** plans.
- Sunday = rest / repurpose note only.

All HTTP goes through a retrying session (5 retries, exponential backoff on
429/5xx). Notion API version `2022-06-28`.

```bat
python push_content.py              :: all 7 days + verify
python push_content.py --day Monday :: one day
python push_content.py --verify-only
python push_content.py --dry-run    :: build blocks, print counts, no network
```

The run ends with a **verify** pass that re-fetches each page and counts the
video + story blocks so you know the push actually landed.

---

## `daily_story.py`

Renders story sequences over your photos. Block types: `text` (white/dark box
with inline `[r]red[/] [g]green[/] [o]orange[/]` markup), `table` (before/after
case study), `poll` (2 answer pills — add the real IG sticker in-app), `qa`
(Thursday's Questions box). Every slide gets your `@handle` and an `n/N` counter.

```bat
python daily_story.py            :: today
python daily_story.py Tuesday    :: one day
python daily_story.py all        :: every day
python daily_story.py all --photos "C:\path\to\photos"
```

No photos found? It falls back to generated gradient backgrounds so you still
see the layout — then point `PHOTO_DIR` at your real work pics.

---

## Weekly cadence

Say **"update all content for the week"** and a fresh themed week is written into
`week_content.py` (new hooks/angles — see `ARCHIVE.md` so nothing repeats),
pushed to Notion, and all story images are regenerated to match. The rules every
week must follow live in `CONTENT_RULES.md`.
