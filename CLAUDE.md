# CLAUDE.md — how to run this repo

This is a weekly content generation system for local-service-business marketing.

## Files
- `week_content.py` — **single source of truth** for the current week (video
  scripts + story plans + DM keywords + theme metadata). Both scripts import it.
- `push_content.py` — pushes the week to Notion (clears + rebuilds 7 day pages, verifies).
- `daily_story.py` — renders IG Story PNGs from real photos.
- `CONTENT_RULES.md` — **the rules every week must follow. Read it before writing any content.**
- `ARCHIVE.md` — log of past hooks/frameworks/angles. **Never repeat what's in here.**
- `.env` — secrets/config (git-ignored): `NOTION_TOKEN`, `IG_HANDLE`, `PHOTO_DIR`.

## Weekly cadence — when the user says "update all content for the week"
1. Read `CONTENT_RULES.md` and `ARCHIVE.md`.
2. Write a **fresh themed week** into `week_content.py` — new angle, new named
   frameworks/roadmaps, new hooks, new DM keywords. Nothing may repeat `ARCHIVE.md`.
3. Keep the fixed weekly themes (Mon One Specific Fix … Sat Objection Crusher,
   Sun rest), the 4-videos/day + STAR + format rotation (Clone ~2×, Miro ~2×,
   no carousels), and the 3-stories/day (poll / proof-or-agitate / CTA; Thursday Q&A).
4. `python push_content.py` — push + verify (4 videos + stories per day).
5. `python daily_story.py all` — regenerate all story images.
6. Append the new week to `ARCHIVE.md`.

## Validation without a token
`python push_content.py --dry-run` builds every block and prints counts with no
network — use it to confirm structure before a live push.

## Notes
- Never commit `.env`, `notion_pages.json`, `story_output/`, or client photos.
- Notion API version pinned to `2022-06-28`; all calls use a retrying session.
