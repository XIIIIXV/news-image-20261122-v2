#!/usr/bin/env python3
"""Front page v2 for Sunday 22 November 2026 (1024x1024 PNG).

Rebuild of the v1 entry following the GLM judge's fix plan:
a top-line summary deck under the masthead, a sport-light grid
(1 sport card, backfilled with health / energy / disaster news),
fully geographic region tabs (SPORT gone, OCEANIA in), a compact
fact-control box (DATE CHECK + sources + certainty key), a tightly
cropped world map whose pins match the card numbers, and de-densified
small-text areas (12-item ALSO list, 6-entry UTC timeline).

25 stories, 7 regions. Every story is one of the 33 date-checked
stories of v1 — nothing new was added, only rebalanced and relabelled.

Deterministic: fixed fonts, fixed palette, no network, no randomness.
Reads stories_v2.json next to this file and writes entry.png beside it.
Run twice -> byte-identical output.
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "stories_v2.json")))

W = H = 1024
PAPER = (247, 242, 231)
INK = (25, 25, 25)
NAVY = (20, 38, 74)
NAVY2 = (28, 52, 96)
AMBER = (232, 163, 23)
RED = (179, 64, 46)
TEAL = (31, 111, 107)
GREEN = (46, 125, 70)
CARD = (255, 255, 255)
LINE = (200, 192, 172)
MUTED = (90, 86, 76)
SKY = (168, 205, 226)
SEA = (44, 92, 140)
OCEAN = (178, 208, 228)
LAND = (232, 222, 196)
BOX = (255, 243, 205)

PILL_FILL = {"REPORTED": NAVY, "CLAIM": AMBER, "CONFIRMED": GREEN,
             "ONGOING": RED}
PILL_TEXT = {"REPORTED": (255, 255, 255), "CLAIM": (25, 25, 25),
             "CONFIRMED": (255, 255, 255), "ONGOING": (255, 255, 255)}


def font(name, size):
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/" + name + ".ttf", size)


def serif_b(s):
    return font("DejaVuSerif-Bold", s)


def sans_b(s):
    return font("DejaVuSans-Bold", s)


def sans(s):
    return font("DejaVuSans", s)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, width, max_lines, bold=True, shrink_to=10):
    size = fnt.size
    while size > shrink_to:
        name = "DejaVuSans-Bold" if bold else "DejaVuSans"
        f = font(name, size)
        lines = wrap(draw, text, f, width)
        if len(lines) <= max_lines:
            return f, lines
        size -= 1
    f = font("DejaVuSans-Bold" if bold else "DejaVuSans", shrink_to)
    lines = wrap(draw, text, f, width)
    if len(lines) > max_lines:
        # Never silently truncate mid-sentence: fail loudly so a cut-off
        # dek is caught at build time, not by a human reading a crop.
        raise ValueError(
            "text needs %d lines, max %d at min size %d: %r -> %r"
            % (len(lines), max_lines, shrink_to, text, lines))
    return f, lines


def pill(draw, x, y, text, size=10):
    f = sans_b(size)
    w = draw.textlength(text, font=f) + 10
    draw.rounded_rectangle([x, y, x + w, y + size + 8], radius=3,
                           fill=PILL_FILL[text])
    draw.text((x + 5, y + 4), text, font=f, fill=PILL_TEXT[text])
    return w


def num_badge(draw, x, y, n, r=10):
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], outline=(255, 255, 255), width=1)
    t = str(n)
    f = sans_b(12 if n < 10 else 10)
    tw = draw.textlength(t, font=f)
    draw.text((x + r - tw / 2, y + r - 7), t, font=f, fill=(255, 255, 255))

# ---------------------------------------------------------------- icons
# Each icon draws a small flat scene inside (x, y, w, h). All coordinates
# are local to the box so the same icon works at hero and card sizes.

def icon_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 24, x + w, y + h], fill=SEA)
    for i in range(4):
        d.arc([x + 10 + i * 26, y + h - 32, x + 32 + i * 26, y + h - 10],
              200, 340, fill=(255, 255, 255), width=3)
    d.polygon([(x + 20, y + 48), (x + w - 20, y + 48), (x + w - 34, y + 70),
               (x + 34, y + 70)], fill=(60, 60, 66))
    for j, col in enumerate((RED, AMBER, TEAL)):
        d.rectangle([x + 30 + j * 26, y + 26, x + 50 + j * 26, y + 48],
                    fill=col)
    d.rectangle([x + w - 44, y + 30, x + w - 26, y + 48], fill=(240, 240, 240))
    cx, cy = x + w - 34, y + 14
    d.polygon([(cx, cy - 11), (cx + 8, cy + 3), (cx + 4, cy + 1),
               (cx + 6, cy + 9), (cx, cy + 3), (cx - 6, cy + 9),
               (cx - 4, cy + 1), (cx - 8, cy + 3)], fill=(255, 140, 0))


def icon_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    cx = x + w // 2
    d.pieslice([cx - 32, y + 10, cx + 32, y + 60], 180, 360,
               fill=(255, 255, 255))
    d.rectangle([cx - 38, y + 50, cx + 38, y + 58], fill=(255, 255, 255))
    for i in range(-2, 3):
        d.rectangle([cx + i * 16 - 4, y + 58, cx + i * 16 + 4, y + 82],
                    fill=(255, 255, 255))
    d.rectangle([x + 10, y + 82, x + w - 10, y + 90], fill=(255, 255, 255))
    d.line([cx, y + 4, cx, y + 12], fill=RED, width=3)
    d.polygon([(cx, y + 4), (cx + 12, y + 8), (cx, y + 12)], fill=RED)


def icon_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 60, 80))
    cx, cy, r = x + w // 2, y + h // 2 + 4, 32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 140, 90))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 60, 300, fill=(255, 255, 255), width=2)
    d.line([cx, cy - r, cx, cy + r], fill=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    d.ellipse([x + w - 24, y + 10, x + w - 8, y + 26], fill=AMBER)


def icon_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 196))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=SEA)
    d.polygon([(x + 18, y + 52), (x + w - 18, y + 52), (x + w - 30, y + 72),
               (x + 30, y + 72)], fill=(90, 90, 96))
    d.rectangle([x + w // 2 - 4, y + 22, x + w // 2 + 4, y + 52],
                fill=(60, 60, 66))
    d.rectangle([x + w // 2 + 4, y + 24, x + w // 2 + 24, y + 40], fill=RED)
    cx, cy = x + 30, y + 20
    for dx, dy in [(0, -11), (9, -6), (11, 4), (5, 11), (-5, 11), (-11, 4),
                   (-9, -6)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=(255, 140, 0), width=3)


def icon_shield(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    cx = x + w // 2
    d.polygon([(cx - 28, y + 12), (cx + 28, y + 12), (cx + 28, y + 46),
               (cx, y + 78), (cx - 28, y + 46)], fill=NAVY)
    d.polygon([(cx - 20, y + 19), (cx + 20, y + 19), (cx + 20, y + 44),
               (cx, y + 68), (cx - 20, y + 44)], fill=(255, 255, 255))
    d.text((cx - 7, y + 28), "\u2605", font=sans_b(22), fill=AMBER)


def icon_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    cx, cy, r = x + w // 2, y + h // 2, 28
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 220, 60))
    d.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=(255, 255, 255), width=3)
    d.arc([cx - r, cy - r, cx + r, cy + r], 120, 240, fill=(255, 255, 255), width=3)


def icon_badge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 224, 190))
    cx, cy = x + w // 2, y + h // 2 - 6
    outer = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = 30 if i % 2 == 0 else 15
        outer.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(outer, fill=AMBER)
    d.polygon([(cx - 11, cy + 28), (cx + 11, cy + 28), (cx + 7, cy + 42),
               (cx - 7, cy + 42)], fill=RED)


def icon_target(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 196))
    cx, cy = x + w // 2, y + h // 2
    for r, col in [(32, RED), (22, (255, 255, 255)), (12, RED)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=INK)


def icon_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    cx, cy = x + w // 2, y + h // 2
    d.rounded_rectangle([cx - 28, cy - 24, cx + 28, cy + 28], radius=4,
                        fill=(255, 255, 255), outline=NAVY, width=2)
    d.line([cx - 20, cy + 2, cx - 7, cy + 15], fill=GREEN, width=5)
    d.line([cx - 7, cy + 15, cx + 22, cy - 16], fill=GREEN, width=5)
    d.rectangle([cx - 28, cy + 32, cx + 28, cy + 36], fill=NAVY)


def icon_flag(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    cx = x + w // 2
    d.line([cx - 24, y + 14, cx - 24, y + 80], fill=(255, 255, 255), width=3)
    for r in range(3):
        for c in range(4):
            col = INK if (r + c) % 2 == 0 else (255, 255, 255)
            d.rectangle([cx - 22 + c * 11, y + 14 + r * 11,
                         cx - 11 + c * 11, y + 25 + r * 11], fill=col)


def icon_bolt(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 44))
    cx = x + w // 2
    d.polygon([(cx + 8, y + 8), (cx - 14, y + 48), (cx - 2, y + 48),
               (cx - 10, y + 82), (cx + 14, y + 40), (cx + 2, y + 40)],
              fill=AMBER)
    d.ellipse([x + 8, y + h - 16, x + 20, y + h - 4], fill=(255, 255, 255))


def icon_flame(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 26, 22))
    cx, base = x + w // 2, y + h - 12
    d.polygon([(cx, y + 8), (cx + 22, y + 44), (cx + 12, y + 44),
               (cx + 18, y + 62), (cx, base), (cx - 18, y + 62),
               (cx - 12, y + 44), (cx - 22, y + 44)], fill=(255, 110, 20))
    d.polygon([(cx, y + 34), (cx + 11, y + 56), (cx, base),
               (cx - 11, y + 56)], fill=AMBER)


def icon_cross(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([cx - 9, cy - 26, cx + 9, cy + 26], fill=(255, 255, 255))
    d.rectangle([cx - 26, cy - 9, cx + 26, cy + 9], fill=(255, 255, 255))
    d.rectangle([x + 8, y + h - 14, x + w - 8, y + h - 8], fill=(255, 255, 255))


ICONS = {"tanker": icon_tanker, "capitol": icon_capitol, "globe": icon_globe,
         "ship": icon_ship, "shield": icon_shield, "tennis": icon_tennis,
         "badge": icon_badge, "target": icon_target, "ballot": icon_ballot,
         "flag": icon_flag, "bolt": icon_bolt, "flame": icon_flame,
         "cross": icon_cross}

# ---------------------------------------------------------------- map
# Rough continent outlines, normalised (0..1) inside the map panel.
CONTINENTS = [
    [(0.05, 0.25), (0.10, 0.10), (0.20, 0.08), (0.28, 0.18), (0.30, 0.35),
     (0.24, 0.45), (0.18, 0.55), (0.12, 0.50), (0.06, 0.40)],
    [(0.30, 0.05), (0.34, 0.05), (0.34, 0.14), (0.30, 0.14)],
    [(0.26, 0.55), (0.32, 0.52), (0.36, 0.60), (0.34, 0.75), (0.30, 0.90),
     (0.27, 0.75)],
    [(0.46, 0.12), (0.52, 0.08), (0.56, 0.14), (0.55, 0.24), (0.50, 0.28),
     (0.46, 0.22)],
    [(0.47, 0.32), (0.55, 0.30), (0.60, 0.38), (0.58, 0.55), (0.53, 0.68),
     (0.49, 0.55), (0.46, 0.42)],
    [(0.56, 0.08), (0.70, 0.05), (0.85, 0.10), (0.95, 0.20), (0.92, 0.35),
     (0.85, 0.45), (0.75, 0.50), (0.65, 0.45), (0.58, 0.35), (0.56, 0.20)],
    [(0.82, 0.68), (0.90, 0.66), (0.93, 0.74), (0.88, 0.82), (0.83, 0.76)],
]

# v1's map left wide empty margins around the landmasses (a judged craft
# flaw). Widen everything about the panel centre so the continents fill
# the panel horizontally; the same transform applies to pins, so pins
# stay on land. Vertical scale stays 1.0: the northern pins (Sparta II,
# Finland) already sit near the top edge, and any vertical stretch
# pushes their badges out of the panel.
MAP_SX, MAP_SY = 1.15, 1.0


def map_xy(px, py):
    mx = 0.5 + (px - 0.5) * MAP_SX
    my = 0.5 + (py - 0.5) * MAP_SY
    return (min(max(mx, 0.02), 0.98), min(max(my, 0.03), 0.97))


# ---------------------------------------------------------------- page
def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14

    # ---- masthead (0-88)
    d.rectangle([0, 0, W, 84], fill=NAVY)
    d.rectangle([0, 84, W, 88], fill=AMBER)
    d.text((M, 10), "THE WORLD IN ONE PAGE", font=serif_b(32),
           fill=(255, 255, 255))
    d.text((M, 52), "SUNDAY 22 NOVEMBER 2026  \u00b7  THE DAY'S NEWS, IN ONE IMAGE",
           font=sans_b(14), fill=AMBER)
    d.text((W - M - 200, 14), "25 STORIES", font=sans_b(25),
           fill=(255, 255, 255))
    d.text((W - M - 200, 50), "7 REGIONS", font=sans_b(13),
           fill=(200, 210, 230))

    # ---- summary deck (88-134): FIX 1, the highest-impact change.
    # The three biggest stories of the day, big enough to read at 300px.
    deck_lines = wrap(d, DATA["deck"], sans_b(19), W - 2 * M)
    assert len(deck_lines) <= 2, "deck needs %d lines: %r" % (
        len(deck_lines), deck_lines)
    dy = 91
    for ln in deck_lines:
        d.text((M, dy), ln, font=sans_b(19), fill=RED)
        dy += 22

    # ---- numbers strip (134-170)
    ny = 134
    d.rectangle([0, ny, W, ny + 36], fill=NAVY2)
    nums = DATA["numbers"]
    seg = W // len(nums)
    for i, n in enumerate(nums):
        cx = i * seg + seg // 2
        d.text((cx, ny + 2), n["value"], font=sans_b(15), fill=AMBER,
               anchor="ma")
        lab = wrap(d, n["label"].upper(), sans_b(7), seg - 8)
        ly = ny + 20
        for ln in lab[:2]:
            d.text((cx, ly), ln, font=sans_b(7), fill=(200, 210, 230),
                   anchor="ma")
            ly += 8

    # ---- region tabs, fully geographic (170-194): FIX 3, SPORT is gone.
    ty = 170
    d.rectangle([0, ty, W, ty + 24], fill=(255, 255, 255))
    d.rectangle([0, ty + 24, W, ty + 25], fill=LINE)
    regs = DATA["regions"]
    tw = (W - 2 * M) // len(regs)
    for i, r in enumerate(regs):
        x = M + i * tw
        d.text((x + 4, ty + 5), r["name"], font=sans_b(11), fill=NAVY)
        d.text((x + tw - 26, ty + 5), str(r["count"]), font=sans_b(12),
               fill=RED)
        if i:
            d.line([x, ty + 4, x, ty + 20], fill=LINE, width=1)

    # ---- leads: 3 big cards (200-360)
    y0, lh = 200, 160
    cw = (W - 2 * M - 20) // 3
    for i, st in enumerate(DATA["leads"]):
        x = M + i * (cw + 10)
        d.rounded_rectangle([x, y0, x + cw, y0 + lh], radius=6, fill=CARD,
                            outline=LINE, width=1)
        ICONS[st["icon"]](d, x + 6, y0 + 6, cw - 12, 62)
        num_badge(d, x + 10, y0 + 10, i + 1)
        pw = pill(d, x + 10, y0 + 74, st["pill"], size=9)
        d.text((x + 14 + pw, y0 + 77), st["region"], font=sans_b(9), fill=RED)
        f, lines = fit_lines(d, st["headline"], sans_b(16), cw - 20, 2)
        yy = y0 + 94
        for ln in lines:
            d.text((x + 10, yy), ln, font=f, fill=INK)
            yy += f.size + 2
        sf, slines = fit_lines(d, st["sub"], sans(11), cw - 20, 2, bold=False)
        for ln in slines:
            d.text((x + 10, yy), ln, font=sf, fill=MUTED)
            yy += sf.size + 1

    # ---- grid: 10 cards, 5 x 2 (368-570). FIX 2: one sport card only.
    y1, ih = 368, 97
    tw5 = (W - 2 * M - 24) // 5
    for i, st in enumerate(DATA["grid"]):
        r, c = divmod(i, 5)
        x = M + c * (tw5 + 6)
        y = y1 + r * (ih + 8)
        d.rounded_rectangle([x, y, x + tw5, y + ih], radius=6, fill=CARD,
                            outline=LINE, width=1)
        ICONS[st["icon"]](d, x + 5, y + 5, 58, ih - 10)
        num_badge(d, x + 8, y + 8, i + 4, r=9)
        tx = x + 68
        pw = pill(d, tx, y + 6, st["pill"], size=8)
        d.text((tx + pw + 4, y + 8), st["region"], font=sans_b(8), fill=RED)
        f, lines = fit_lines(d, st["headline"], sans_b(12), tw5 - 74, 3)
        yy = y + 24
        for ln in lines:
            d.text((tx, yy), ln, font=f, fill=INK)
            yy += f.size + 1
        sf, slines = fit_lines(d, st["sub"], sans(10), tw5 - 74, 2, bold=False)
        for ln in slines:
            d.text((tx, yy), ln, font=sf, fill=MUTED)
            yy += sf.size + 1

    # ---- world map, tightly cropped (578-718): FIX 5.
    my = 578
    d.text((M, my), "WHERE IT HAPPENED", font=sans_b(13), fill=NAVY)
    d.text((W - M, my), "pins 1\u201313 match the cards above",
           font=sans(11), fill=MUTED, anchor="ra")
    mx, mw, mh = M, W - 2 * M, 120
    my0 = my + 20
    d.rectangle([mx, my0, mx + mw, my0 + mh], fill=OCEAN, outline=LINE)
    for poly in CONTINENTS:
        pts = [(mx + map_xy(px, py)[0] * mw,
                my0 + map_xy(px, py)[1] * mh) for px, py in poly]
        d.polygon(pts, fill=LAND, outline=(180, 170, 140))
    # Urals line, so Europe reads apart from Asia (same transform).
    ux1, uy1 = map_xy(0.565, 0.06)
    ux2, uy2 = map_xy(0.585, 0.34)
    d.line([(mx + ux1 * mw, my0 + uy1 * mh),
            (mx + ux2 * mw, my0 + uy2 * mh)],
           fill=(150, 138, 105), width=2)
    all_cards = DATA["leads"] + DATA["grid"]
    for i, st in enumerate(all_cards):
        qx, qy = map_xy(*st["pin"])
        cx, cy = mx + qx * mw, my0 + qy * mh
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED,
                  outline=(255, 255, 255), width=2)
        t = str(i + 1)
        f = sans_b(11 if i + 1 < 10 else 9)
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 7), t, font=f, fill=(255, 255, 255))

    # ---- ALSO ON SUNDAY, 12 items in 2 columns (726-874): FIX 6.
    ay = 726
    d.text((M, ay), "ALSO ON SUNDAY", font=sans_b(13), fill=NAVY)
    d.text((W - M, ay), "14\u201325  \u00b7  status in grey",
           font=sans(11), fill=MUTED, anchor="ra")
    col_w = (W - 2 * M - 20) // 2
    for i, st in enumerate(DATA["also"]):
        c, r = divmod(i, 6)
        x = M + c * (col_w + 20)
        y = ay + 22 + r * 21
        d.text((x, y), str(14 + i) + ".", font=sans_b(12), fill=RED)
        hl = st["headline"]
        f = sans(13)
        assert d.textlength(hl, font=f) <= col_w - 90, (
            "also headline too long at 13pt: %r" % hl)
        d.text((x + 28, y), hl, font=f, fill=INK)
        hw = d.textlength(hl, font=f)
        d.text((x + 28 + hw + 6, y + 1), st["pill"], font=sans_b(8),
               fill=MUTED)

    # ---- UTC timeline, 6 entries in 2 rows x 3 cols (880-914): FIX 6.
    ty2 = 880
    d.rectangle([0, ty2, W, ty2 + 34], fill=NAVY)
    d.text((M, ty2 + 3), "SUNDAY IN UTC", font=sans_b(11), fill=AMBER)
    tl = DATA["timeline"]
    seg2 = (W - 2 * M - 130) // 3
    for i, t in enumerate(tl):
        r, c = divmod(i, 3)
        x = M + 130 + c * seg2
        y = ty2 + 3 + r * 15
        d.text((x, y), t["time"], font=sans_b(10), fill=AMBER)
        d.text((x + 38, y), t["label"], font=sans(10),
               fill=(255, 255, 255))

    # ---- fact-control box (918-1010): FIX 4.
    dy = 918
    d.rectangle([0, dy, W, dy + 92], fill=BOX)
    d.rectangle([0, dy, W, dy + 92], outline=RED, width=2)
    d.text((M, dy + 5), "DATE CHECK \u2014 LEFT OUT ON PURPOSE (NOT 22 NOVEMBER):",
           font=sans_b(11), fill=RED)
    dc = ("400-drone / 110-missile strike on Ukraine \u2014 19-20 Nov  \u00b7  "
          "ICJ: Myanmar guilty of Rohingya genocide \u2014 19 Nov  \u00b7  "
          "Nigeria boat capsizes, 24 dead \u2014 20 Nov  \u00b7  "
          "Sparta II drone strike itself \u2014 21 Nov  \u00b7  "
          "FIFA names UK 2035 Women's World Cup host \u2014 23 Nov")
    f, lines = fit_lines(d, dc, sans(11), W - 2 * M, 2, bold=False)
    yy = dy + 21
    for ln in lines:
        d.text((M, yy), ln, font=f, fill=INK)
        yy += f.size + 1
    d.text((M, dy + 49),
           "TODAY'S VERIFIED COUNT: 186 drones launched; 161 downed  \u00b7  "
           "NOT DECIDED ON SUNDAY: COP31 final vote \u00b7 Gaza aid crossings",
           font=sans_b(10), fill=RED)
    d.text((M, dy + 66),
           "Sources: Reuters, AP, BBC, Al Jazeera, CNN, Ukrainian Air Force, "
           "RFE/RL  \u00b7  REPORTED = carried by the day's wires \u00b7  "
           "CLAIM = one side's account \u00b7  FORECAST = still to happen",
           font=sans(10), fill=INK)

    # ---- footer (1012-1024)
    d.text((M, 1012),
           "All 25 stories happened or were first reported Sunday "
           "22 Nov 2026 \u00b7 Claims marked CLAIM.",
           font=sans(10), fill=MUTED)
    return img


def main():
    img = draw()
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
