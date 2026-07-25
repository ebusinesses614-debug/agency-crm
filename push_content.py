# -*- coding: utf-8 -*-
"""
push_content.py -- Weekly content pusher for Notion.

Clears and rebuilds all 7 day pages (Monday..Sunday) with the current week
defined in week_content.py. Every Mon-Sat page gets:

    * a themed header callout (day theme + color)
    * a daily to-do checklist
    * 4 video ideas (Style / Pillar / Hook / Script / CTA / Caption)
    * "Today's 3 IG Stories" plans

Sunday gets a rest/repurpose note only.

Usage:
    python push_content.py                 # push all 7 days, then verify
    python push_content.py --day Monday    # push a single day
    python push_content.py --no-verify     # push without the count check
    python push_content.py --verify-only   # only fetch + count existing pages
    python push_content.py --dry-run       # build blocks, print counts, no network

Setup:
    pip install requests
    Copy .env.example -> .env and set NOTION_TOKEN.
    Create 7 Notion pages named Monday..Sunday and share EACH with your
    integration (page ... -> "..." menu -> Connections -> your integration).
    Page IDs are auto-discovered by title, or pin them in .env.
"""

import argparse
import json
import os
import re
import sys
import time

import requests
from requests.adapters import HTTPAdapter

try:
    from urllib3.util.retry import Retry
except Exception:  # pragma: no cover
    from requests.packages.urllib3.util.retry import Retry  # type: ignore

from week_content import WEEK, THEME, CHECKLIST, DAY_ORDER

NOTION_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
PAGE_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "notion_pages.json")

THEME_EMOJI = {
    "Monday": "🔧", "Tuesday": "📈", "Wednesday": "🩸", "Thursday": "🎥",
    "Friday": "🧩", "Saturday": "🥊", "Sunday": "🌙",
}


# ---------------------------------------------------------------------------
# .env loading (no external dependency)
# ---------------------------------------------------------------------------
def load_env():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key, val = key.strip(), val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val


# ---------------------------------------------------------------------------
# Rich-text + block builders
# ---------------------------------------------------------------------------
MARKUP_COLOR = {"r": "red", "g": "green", "o": "orange"}
MARKUP_RE = re.compile(r"\[(r|g|o)\](.*?)\[/\]", re.S)
MAX_RT = 1900  # Notion hard limit is 2000 chars per rich_text item


def rt(content, bold=False, color="default"):
    return {"type": "text",
            "text": {"content": content},
            "annotations": {"bold": bold, "color": color}}


def rt_plain(text, bold=False):
    """Split long plain text into <=MAX_RT rich_text chunks (keeps newlines)."""
    if text == "":
        return [rt("")]
    return [rt(text[i:i + MAX_RT], bold=bold) for i in range(0, len(text), MAX_RT)]


def parse_markup(text):
    """Turn [r]..[/] / [g]..[/] / [o]..[/] into colored rich_text items."""
    parts, idx = [], 0
    for m in MARKUP_RE.finditer(text):
        if m.start() > idx:
            parts.append((text[idx:m.start()], "default"))
        parts.append((m.group(2), MARKUP_COLOR[m.group(1)]))
        idx = m.end()
    if idx < len(text):
        parts.append((text[idx:], "default"))
    if not parts:
        parts = [(text, "default")]
    out = []
    for txt, color in parts:
        if txt:
            out.extend(rt(txt[i:i + MAX_RT], color=color)
                       for i in range(0, len(txt), MAX_RT))
    return out or [rt("")]


def block(kind, payload):
    return {"object": "block", "type": kind, kind: payload}


def paragraph(rich):
    return block("paragraph", {"rich_text": rich})


def labeled(label, value):
    return paragraph([rt(label + ": ", bold=True)] + rt_plain(value))


def heading(level, text):
    kind = "heading_%d" % level
    return block(kind, {"rich_text": [rt(text, bold=True)]})


def callout(text, emoji, color):
    return block("callout", {"rich_text": [rt(text, bold=True)],
                             "icon": {"type": "emoji", "emoji": emoji},
                             "color": color})


def to_do(text):
    return block("to_do", {"rich_text": [rt(text)], "checked": False})


def toggle(title_rich, children):
    return block("toggle", {"rich_text": title_rich, "children": children})


def bullet(rich):
    return block("bulleted_list_item", {"rich_text": rich})


def story_blocks(slide):
    """Render one story slide (list of visual blocks) into Notion blocks."""
    out = []
    for b in slide:
        t = b["type"]
        if t == "poll":
            out.append(bullet([rt("📊 POLL - ", bold=True), rt(b["question"])]))
            out.append(bullet([rt("Answers: ", bold=True),
                               rt(" / ".join(b["options"]))]))
        elif t == "text":
            tag = "▫️ white box - " if b["box"] == "white" else "◾ dark box - "
            out.append(bullet([rt(tag, bold=True)] + parse_markup(b["text"])))
        elif t == "table":
            out.append(bullet([rt("📋 " + b["header"], bold=True)]))
            for label, value, kind in b["rows"]:
                color = ("red" if kind == "before"
                         else "green" if kind == "after" else "default")
                out.append(bullet([rt("   " + label + ": ", bold=True),
                                   rt(value, color=color)]))
        elif t == "qa":
            out.append(bullet([rt("❓ Q&A BOX - ", bold=True), rt(b["prompt"])]))
    return out


def build_day_blocks(day):
    data = WEEK[day]
    theme = THEME[day]
    emoji = THEME_EMOJI[day]
    blocks = [callout("%s  --  %s" % (day, theme["name"]), emoji, theme["notion"])]

    if day == "Sunday":
        blocks.append(heading(2, "🌙 Rest / Repurpose"))
        for line in data["note"].split("\n"):
            blocks.append(paragraph(rt_plain(line)))
        blocks.append(heading(2, "📱 This Week's Story"))
        for i, slide in enumerate(data.get("stories", []), 1):
            blocks.append(toggle([rt("Story %d" % i, bold=True)],
                                 story_blocks(slide)))
        return blocks

    blocks.append(heading(2, "✅ Daily Checklist"))
    for item in CHECKLIST:
        blocks.append(to_do(item))

    blocks.append(heading(2, "🎬 Today's 4 Videos"))
    for i, v in enumerate(data["videos"], 1):
        children = [
            labeled("Content Style / Format", v["style"]),
            labeled("Content Pillar", v["pillar"]),
            labeled("Hook", v["hook"]),
            labeled("Script", v["script"]),
            labeled("CTA", v["cta"]),
            labeled("Caption", v["caption"]),
        ]
        title = [rt("Video %d  -  %s" % (i, v["style"]), bold=True)]
        blocks.append(toggle(title, children))

    blocks.append(heading(2, "📱 Today's 3 IG Stories"))
    for i, slide in enumerate(data["stories"], 1):
        blocks.append(toggle([rt("Story %d" % i, bold=True)], story_blocks(slide)))

    return blocks


# ---------------------------------------------------------------------------
# Notion HTTP layer
# ---------------------------------------------------------------------------
class Notion:
    def __init__(self, token):
        self.session = self._make_session(token)

    @staticmethod
    def _make_session(token):
        s = requests.Session()
        retry = Retry(
            total=5,
            backoff_factor=1.5,                       # 0, 1.5, 3, 6, 12s ...
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=frozenset(["GET", "POST", "PATCH", "DELETE"]),
            respect_retry_after_header=True,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        s.mount("https://", adapter)
        s.mount("http://", adapter)
        s.headers.update({
            "Authorization": "Bearer %s" % token,
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        })
        return s

    def _request(self, method, path, **kw):
        url = path if path.startswith("http") else NOTION_BASE + path
        r = self.session.request(method, url, timeout=30, **kw)
        if r.status_code >= 400:
            raise RuntimeError("Notion %s %s -> %s: %s"
                               % (method, path, r.status_code, r.text[:400]))
        return r.json() if r.text else {}

    # -- page discovery -----------------------------------------------------
    @staticmethod
    def _title_of(page):
        for prop in page.get("properties", {}).values():
            if prop.get("type") == "title":
                return "".join(t.get("plain_text", "") for t in prop["title"])
        return ""

    def find_page_id(self, day):
        body = {"query": day,
                "filter": {"property": "object", "value": "page"},
                "page_size": 50}
        for res in self._request("POST", "/search", json=body).get("results", []):
            if res.get("object") == "page" and \
                    self._title_of(res).strip().lower() == day.lower():
                return res["id"]
        return None

    # -- block ops ----------------------------------------------------------
    def children(self, block_id):
        out, cursor = [], None
        while True:
            path = "/blocks/%s/children?page_size=100" % block_id
            if cursor:
                path += "&start_cursor=%s" % cursor
            data = self._request("GET", path)
            out.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return out

    def clear_page(self, page_id):
        kids = self.children(page_id)
        for child in kids:
            self._request("DELETE", "/blocks/%s" % child["id"])
            time.sleep(0.34)  # stay under Notion's ~3 req/s
        return len(kids)

    def append(self, page_id, blocks, chunk=50):
        for i in range(0, len(blocks), chunk):
            self._request("PATCH", "/blocks/%s/children" % page_id,
                          json={"children": blocks[i:i + chunk]})
            time.sleep(0.34)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def resolve_page_ids(notion, days):
    """Return {day: page_id}, from env overrides, cache, or title search."""
    ids, cache = {}, {}
    if os.path.exists(PAGE_CACHE_FILE):
        try:
            cache = json.load(open(PAGE_CACHE_FILE, encoding="utf-8"))
        except Exception:
            cache = {}

    missing = []
    for day in days:
        env_id = os.environ.get("NOTION_PAGE_%s" % day.upper(), "").strip()
        if env_id:
            ids[day] = env_id
            continue
        if cache.get(day):
            ids[day] = cache[day]
            continue
        pid = notion.find_page_id(day)
        if pid:
            ids[day] = pid
        else:
            missing.append(day)

    if missing:
        print("\n[!] Could not find Notion pages for: %s" % ", ".join(missing))
        print("    Fix: create a page titled exactly like the day, then open it,")
        print("    click the '...' menu -> Connections -> add your integration.")
        print("    (Or pin the ID in .env as NOTION_PAGE_<DAY>.)\n")

    merged = dict(cache)
    merged.update(ids)
    try:
        json.dump(merged, open(PAGE_CACHE_FILE, "w", encoding="utf-8"), indent=2)
    except Exception:
        pass
    return ids


def push(notion, day, page_id):
    blocks = build_day_blocks(day)
    removed = notion.clear_page(page_id)
    notion.append(page_id, blocks)
    print("  %-9s cleared %2d old block(s), pushed %2d new block(s)"
          % (day, removed, len(blocks)))


def verify(notion, ids):
    print("\n=== VERIFY (fetching blocks from Notion) ===")
    ok = True
    for day in DAY_ORDER:
        if day not in ids:
            continue
        kids = notion.children(ids[day])
        videos = stories = 0
        for b in kids:
            if b.get("type") != "toggle":
                continue
            txt = "".join(t.get("plain_text", "")
                          for t in b["toggle"].get("rich_text", []))
            if txt.startswith("Video"):
                videos += 1
            elif txt.startswith("Story"):
                stories += 1
        expected_v = 0 if day == "Sunday" else 4
        good = (videos == expected_v)
        ok = ok and good
        flag = "OK " if good else "!! "
        print("  %s%-9s videos=%d (want %d)   stories=%d"
              % (flag, day, videos, expected_v, stories))
    print("=== %s ===" % ("ALL GOOD" if ok else "MISMATCH - check above"))
    return ok


def dry_run(days):
    print("=== DRY RUN (no network) ===")
    total = 0
    for day in days:
        blocks = build_day_blocks(day)
        total += len(blocks)
        vids = sum(1 for b in blocks if b["type"] == "toggle"
                   and b["toggle"]["rich_text"][0]["text"]["content"].startswith("Video"))
        stos = sum(1 for b in blocks if b["type"] == "toggle"
                   and b["toggle"]["rich_text"][0]["text"]["content"].startswith("Story"))
        print("  %-9s top-level blocks=%2d  videos=%d  stories=%d"
              % (day, len(blocks), vids, stos))
    print("  total top-level blocks: %d" % total)
    sample = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "_sample_monday_blocks.json")
    json.dump(build_day_blocks("Monday"), open(sample, "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)
    print("  wrote %s for inspection" % sample)


def main():
    ap = argparse.ArgumentParser(description="Push the weekly content to Notion.")
    ap.add_argument("--day", help="push a single day (e.g. Monday)")
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    load_env()
    days = [args.day.capitalize()] if args.day else DAY_ORDER
    for d in days:
        if d not in WEEK:
            sys.exit("Unknown day: %s" % d)

    if args.dry_run:
        dry_run(days)
        return

    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        sys.exit("NOTION_TOKEN not set. Copy .env.example -> .env and add it "
                 "(or run with --dry-run).")

    notion = Notion(token)
    ids = resolve_page_ids(notion, days)
    if not ids:
        sys.exit("No page IDs resolved - share your day pages with the integration.")

    if not args.verify_only:
        print("=== PUSHING WEEK ===")
        for day in days:
            if day in ids:
                push(notion, day, ids[day])

    if not args.no_verify:
        verify(notion, {d: ids[d] for d in ids})


if __name__ == "__main__":
    main()
