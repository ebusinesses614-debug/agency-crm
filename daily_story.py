# -*- coding: utf-8 -*-
"""
daily_story.py -- Instagram Story image generator (1080x1920 PNGs).

Renders finished story sequences over your real work photos. Content mirrors
the week pushed to Notion (same hooks, frameworks, DM keywords) via week_content.py.

Block types:
    text  -- rounded box; box="white" (dark text) or "dark" (white text).
             Inline markup: [r]red[/] (pain) [g]green[/] (win) [o]orange[/] (DM word)
    table -- dark card: uppercase header + label/value rows, values red (before)
             or green (after). For before/after case studies.
    poll  -- dark card: uppercase question + 2 answer pills (first highlighted).
             Placeholder -- add the real interactive poll sticker in the IG app.
    qa    -- dark card: Q&A prompt (Thursday). Add the real Questions sticker in-app.

Every slide gets your @handle (bottom-left) and an n/N counter (bottom-right).

Usage:
    python daily_story.py                 # today
    python daily_story.py Tuesday         # one day
    python daily_story.py all             # every day
    python daily_story.py all --photos "C:\\path\\to\\photos"

Output: story_output/<Day>/<Day>_1.png ...  (whole folder is wiped first)
Config: set IG_HANDLE and PHOTO_DIR in .env, or edit the constants below.
"""

import argparse
import datetime
import os
import re
import shutil
import sys

from PIL import Image, ImageDraw, ImageFont

from week_content import WEEK, THEME, DAY_ORDER

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
CANVAS = (1080, 1920)
MARGIN = 60
CONTENT_W = CANVAS[0] - 2 * MARGIN          # 960
BODY_SIZE = 50
TOP_START = 290
GAP = 28
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "story_output")

# Fonts: Arial Bold on Windows first, then common fallbacks.
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\Arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]

MARKUP_RE = re.compile(r"\[(r|g|o)\](.*?)\[/\]", re.S)
MARKUP_COLOR = {"r": "red", "g": "green", "o": "orange"}
INLINE = {"red": (231, 76, 60), "green": (46, 204, 113), "orange": (243, 156, 18)}


def load_env():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v


# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
_FONT_PATH = None
_FONT_CACHE = {}


def _resolve_font_path():
    global _FONT_PATH
    if _FONT_PATH is not None:
        return _FONT_PATH
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            _FONT_PATH = p
            return p
    _FONT_PATH = ""      # signal: use PIL default
    return _FONT_PATH


def font(size):
    if size in _FONT_CACHE:
        return _FONT_CACHE[size]
    path = _resolve_font_path()
    try:
        f = ImageFont.truetype(path, size) if path else ImageFont.load_default(size)
    except Exception:
        f = ImageFont.load_default()
    _FONT_CACHE[size] = f
    return f


# ---------------------------------------------------------------------------
# Inline-markup text layout
# ---------------------------------------------------------------------------
def _runs(text):
    runs, idx = [], 0
    for m in MARKUP_RE.finditer(text):
        if m.start() > idx:
            runs.append((text[idx:m.start()], "default"))
        runs.append((m.group(2), MARKUP_COLOR[m.group(1)]))
        idx = m.end()
    if idx < len(text):
        runs.append((text[idx:], "default"))
    return runs or [(text, "default")]


def _tokens(text):
    """List of ('nl',) or ('w', word, color)."""
    toks = []
    for sub, color in _runs(text):
        for part in re.split(r"(\n)", sub):
            if part == "\n":
                toks.append(("nl",))
            elif part:
                for w in part.split(" "):
                    if w:
                        toks.append(("w", w, color))
    return toks


def _is_punct(word):
    """True for leading punctuation that should hug the previous word."""
    return bool(word) and all(ch in ".,!?:;)]}" for ch in word)


def _wrap(text, fnt, max_w, draw):
    space = draw.textlength(" ", font=fnt)
    lines, cur, cur_w = [], [], 0.0
    for tk in _tokens(text):
        if tk[0] == "nl":
            lines.append(cur)
            cur, cur_w = [], 0.0
            continue
        w = draw.textlength(tk[1], font=fnt)
        lead = space if (cur and not _is_punct(tk[1])) else 0
        if cur and cur_w + lead + w > max_w:
            lines.append(cur)
            cur, cur_w = [tk], w
        else:
            cur.append(tk)
            cur_w += lead + w
    lines.append(cur)
    return lines, space


def _draw_lines(draw, lines, fnt, x, y, default_color, line_h, space):
    for line in lines:
        tx, first = x, True
        for tk in line:
            if not first and not _is_punct(tk[1]):
                tx += space
            first = False
            col = INLINE.get(tk[2], default_color)
            draw.text((tx, y), tk[1], font=fnt, fill=col)
            tx += draw.textlength(tk[1], font=fnt)
        y += line_h
    return y


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------
def make_background(photo_path, accent):
    tw, th = CANVAS
    if photo_path and os.path.exists(photo_path):
        try:
            img = Image.open(photo_path).convert("RGB")
            scale = max(tw / img.width, th / img.height)
            img = img.resize((max(1, int(img.width * scale)),
                              max(1, int(img.height * scale))), Image.LANCZOS)
            left = (img.width - tw) // 2
            top = (img.height - th) // 2
            img = img.crop((left, top, left + tw, top + th))
        except Exception:
            img = _gradient(accent)
    else:
        img = _gradient(accent)

    base = img.convert("RGBA")
    # ~25% black overlay for text contrast.
    base.alpha_composite(Image.new("RGBA", CANVAS, (0, 0, 0, 64)))
    return base


def _gradient(accent):
    """Fallback background when no photo is available."""
    tw, th = CANVAS
    top = tuple(int(c * 0.55) for c in accent)
    bot = tuple(int(c * 0.18) for c in accent)
    grad = Image.new("RGB", (1, th))
    for y in range(th):
        t = y / th
        grad.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * t)
                                    for i in range(3)))
    return grad.resize((tw, th))


# ---------------------------------------------------------------------------
# Block renderers -- each returns the new y cursor
# ---------------------------------------------------------------------------
def _card(base, x0, y0, x1, y1, fill, radius=40):
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill)
    base.alpha_composite(overlay)


def draw_text_box(base, y, blk, accent):
    pad, radius = 44, 40
    white = blk.get("box") == "white"
    fill = (245, 245, 245, 236) if white else (17, 17, 20, 212)
    default_color = (22, 22, 26) if white else (240, 240, 244)
    fnt = font(BODY_SIZE)
    line_h = int(BODY_SIZE * 1.28)

    draw = ImageDraw.Draw(base)
    lines, space = _wrap(blk["text"], fnt, CONTENT_W - 2 * pad, draw)
    box_h = 2 * pad + len(lines) * line_h
    x0, x1 = MARGIN, MARGIN + CONTENT_W
    _card(base, x0, y, x1, y + box_h, fill, radius)
    _draw_lines(ImageDraw.Draw(base), lines, fnt, x0 + pad, y + pad,
                default_color, line_h, space)
    return y + box_h


def draw_table(base, y, blk, accent):
    pad, radius = 40, 40
    hfont, lfont = font(34), font(46)
    rows = blk["rows"]
    header_h, row_h = 60, 76
    box_h = 2 * pad + header_h + row_h * len(rows)
    x0, x1 = MARGIN, MARGIN + CONTENT_W
    _card(base, x0, y, x1, y + box_h, (17, 17, 20, 220), radius)

    d = ImageDraw.Draw(base)
    d.text((x0 + pad, y + pad), blk["header"].upper(), font=hfont, fill=(168, 168, 174))
    ry = y + pad + header_h
    for label, value, kind in rows:
        col = INLINE["red"] if kind == "before" else \
            INLINE["green"] if kind == "after" else (240, 240, 244)
        d.text((x0 + pad, ry), label, font=lfont, fill=(232, 232, 236))
        vw = d.textlength(value, font=lfont)
        d.text((x1 - pad - vw, ry), value, font=lfont, fill=col)
        ry += row_h
    return y + box_h


def draw_poll(base, y, blk, accent):
    pad, radius = 40, 40
    qfont, ofont = font(48), font(44)
    pill_h, pill_gap = 96, 22
    x0, x1 = MARGIN, MARGIN + CONTENT_W

    d = ImageDraw.Draw(base)
    qlines, space = _wrap(blk["question"].upper(), qfont, CONTENT_W - 2 * pad, d)
    q_line_h = int(48 * 1.24)
    q_h = len(qlines) * q_line_h
    box_h = 2 * pad + q_h + 26 + 2 * pill_h + pill_gap
    _card(base, x0, y, x1, y + box_h, (17, 17, 20, 220), radius)

    d = ImageDraw.Draw(base)
    ey = _draw_lines(d, qlines, qfont, x0 + pad, y + pad, (240, 240, 244),
                     q_line_h, space) + 26

    for i, opt in enumerate(blk["options"][:2]):
        py0, py1 = ey, ey + pill_h
        if i == 0:
            _card(base, x0 + pad, py0, x1 - pad, py1, accent + (255,), radius=pill_h // 2)
            txt_col = (18, 18, 20)
        else:
            _card(base, x0 + pad, py0, x1 - pad, py1, (255, 255, 255, 34), radius=pill_h // 2)
            txt_col = (240, 240, 244)
        d2 = ImageDraw.Draw(base)
        tw = d2.textlength(opt, font=ofont)
        d2.text(((x0 + x1) / 2 - tw / 2, py0 + (pill_h - 44) / 2 - 4),
                opt, font=ofont, fill=txt_col)
        ey = py1 + pill_gap
    return y + box_h


def draw_qa(base, y, blk, accent):
    pad, radius = 40, 40
    hfont, pfont, ifont = font(32), font(48), font(40)
    x0, x1 = MARGIN, MARGIN + CONTENT_W

    d = ImageDraw.Draw(base)
    plines, space = _wrap(blk["prompt"], pfont, CONTENT_W - 2 * pad, d)
    p_line_h = int(48 * 1.26)
    input_h = 92
    box_h = 2 * pad + 46 + len(plines) * p_line_h + 24 + input_h
    _card(base, x0, y, x1, y + box_h, (17, 17, 20, 222), radius)

    d = ImageDraw.Draw(base)
    d.text((x0 + pad, y + pad), "Q&A", font=hfont, fill=accent)
    py = _draw_lines(d, plines, pfont, x0 + pad, y + pad + 46, (240, 240, 244),
                     p_line_h, space) + 24
    _card(base, x0 + pad, py, x1 - pad, py + input_h, (255, 255, 255, 30), radius=28)
    ImageDraw.Draw(base).text((x0 + pad + 24, py + (input_h - 40) / 2 - 2),
                              "Type something...", font=ifont, fill=(170, 170, 176))
    return y + box_h


RENDERERS = {"text": draw_text_box, "table": draw_table,
             "poll": draw_poll, "qa": draw_qa}


# ---------------------------------------------------------------------------
# Footer + slide
# ---------------------------------------------------------------------------
def _text_shadow(draw, xy, text, fnt, fill):
    x, y = xy
    draw.text((x + 2, y + 2), text, font=fnt, fill=(0, 0, 0, 160))
    draw.text((x, y), text, font=fnt, fill=fill)


def render_slide(photo_path, blocks, idx, total, accent):
    base = make_background(photo_path, accent)
    y = TOP_START
    for blk in blocks:
        renderer = RENDERERS.get(blk["type"])
        if renderer:
            y = renderer(base, y, blk, accent) + GAP

    d = ImageDraw.Draw(base)
    ffont = font(40)
    handle = os.environ.get("IG_HANDLE", "@youragency")
    _text_shadow(d, (MARGIN, CANVAS[1] - 92), handle, ffont, (245, 245, 245))
    counter = "%d/%d" % (idx, total)
    cw = d.textlength(counter, font=ffont)
    _text_shadow(d, (CANVAS[0] - MARGIN - cw, CANVAS[1] - 92), counter,
                 ffont, (245, 245, 245))
    return base.convert("RGB")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def gather_photos(photo_dir):
    exts = (".jpg", ".jpeg", ".png", ".webp")
    if not photo_dir or not os.path.isdir(photo_dir):
        return []
    return [os.path.join(photo_dir, f) for f in sorted(os.listdir(photo_dir))
            if f.lower().endswith(exts)]


def days_to_render(arg):
    if arg == "all":
        return list(DAY_ORDER)
    if arg == "today" or arg is None:
        return [datetime.datetime.now().strftime("%A")]
    day = arg.capitalize()
    if day not in DAY_ORDER:
        sys.exit("Unknown day '%s'. Use Monday..Sunday, 'today', or 'all'." % arg)
    return [day]


def main():
    ap = argparse.ArgumentParser(description="Generate IG Story PNGs.")
    ap.add_argument("day", nargs="?", default="today",
                    help="Monday..Sunday, 'today' (default), or 'all'")
    ap.add_argument("--photos", help="override photo folder")
    args = ap.parse_args()
    load_env()

    photo_dir = args.photos or os.environ.get("PHOTO_DIR") or \
        r"C:\Users\You\Pictures\work"
    photos = gather_photos(photo_dir)
    if not photos:
        print("[!] No photos found in %r -- using generated gradient "
              "backgrounds. Set PHOTO_DIR in .env or pass --photos." % photo_dir)

    # Wipe the whole output folder so no stale slides survive.
    if os.path.isdir(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

    made = []
    for day in days_to_render(args.day):
        slides = WEEK[day].get("stories", [])
        accent = THEME[day]["rgb"]
        day_dir = os.path.join(OUTPUT_DIR, day)
        os.makedirs(day_dir, exist_ok=True)
        total = len(slides)
        for i, blocks in enumerate(slides, 1):
            photo = photos[(i - 1) % len(photos)] if photos else None
            img = render_slide(photo, blocks, i, total, accent)
            out = os.path.join(day_dir, "%s_%d.png" % (day, i))
            img.save(out, "PNG")
            made.append(out)
            print("  rendered %s" % out)

    print("\nDone. %d slide(s) written to %s" % (len(made), OUTPUT_DIR))


if __name__ == "__main__":
    main()
