#!/usr/bin/env python3
"""Build zech's news-image entry for 21 Nov 2026.

Dark 'world tonight' infographic: very dark navy background, thin
gold/teal lines, a code-drawn globe (circle + arcs, no pasted image).
Pure stdlib + PIL, no network, fully deterministic.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

NAVY_TOP = (10, 18, 40)
NAVY_BOT = (6, 11, 26)
PANEL = (17, 28, 56)
PANEL_EDGE = (58, 74, 110)
WHITE = (240, 242, 248)
MUTED = (176, 186, 205)
GOLD = (212, 175, 55)
TEAL = (45, 212, 191)
RED = (235, 87, 87)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_KICKER = font("DejaVuSans-Bold.ttf", 20)
F_DATE = font("DejaVuSans-Bold.ttf", 58)
F_SUB = font("DejaVuSans-Bold.ttf", 22)
F_TAG = font("DejaVuSans-Bold.ttf", 18)
F_HEAD = font("DejaVuSans-Bold.ttf", 25)
F_DECK = font("DejaVuSans.ttf", 19)
F_FOOT = font("DejaVuSans.ttf", 17)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_globe(draw, cx, cy, r):
    """Globe motif: outer circle, latitude arcs, meridians, orbit ring."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=2)
    # latitude arcs (horizontal chords, clipped visually by circle)
    for fy, rx in ((-0.55, 0.83), (-0.18, 0.98), (0.22, 0.97), (0.58, 0.80)):
        y = cy + int(fy * r)
        x0 = cx - int(rx * r)
        x1 = cx + int(rx * r)
        draw.arc([x0, y - 14, x1, y + 14], 200, 340, fill=TEAL, width=1)
        draw.arc([x0, y - 14, x1, y + 14], 20, 160, fill=TEAL, width=1)
    # meridians (vertical ellipses)
    for rx in (0.45, 0.85):
        draw.ellipse([cx - int(rx * r), cy - r, cx + int(rx * r), cy + r],
                     outline=TEAL, width=1)
    draw.line([cx, cy - r, cx, cy + r], fill=GOLD, width=1)
    # orbit ring + satellite dot
    draw.ellipse([cx - r - 22, cy - r - 22, cx + r + 22, cy + r + 22],
                 outline=(90, 100, 130), width=1)
    ang = math.radians(-38)
    sx = cx + int((r + 22) * math.cos(ang))
    sy = cy + int((r + 22) * math.sin(ang))
    draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=GOLD)
    # tiny stars around the globe
    for dx, dy in ((-r - 34, -r + 18), (r + 30, -r - 6), (-r - 8, r + 30),
                   (r - 12, r + 34)):
        draw.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2],
                     fill=WHITE)


def draw_header(draw):
    draw_globe(draw, 872, 132, 74)
    draw.text((64, 62), "THE WORLD TONIGHT", font=F_KICKER, fill=GOLD)
    draw.text((64, 96), "21 NOVEMBER 2026", font=F_DATE, fill=WHITE)
    draw.text((64, 168), "SATURDAY  ·  WORLD NEWS IN ONE FRAME",
              font=F_SUB, fill=TEAL)
    draw.line([64, 216, 960, 216], fill=GOLD, width=2)
    draw.line([64, 220, 960, 220], fill=(58, 74, 110), width=1)

STORIES = [
    ("ASIA-PACIFIC", "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
     "Three leaders sign a joint declaration after a rare trilateral summit."),
    ("EUROPE", "MISSILES RAIN ON KYIV, NATO JETS SCRAMBLED",
     "A heavy Russian strike hits Kyiv as missiles stray into Polish airspace."),
    ("ASIA-PACIFIC", "COURT RULES MYANMAR COMMITTED GENOCIDE",
     "The world court finds Myanmar guilty of genocide against the Rohingya people."),
    ("CLIMATE", "COP31 DRAGS ON AS FOSSIL-FUEL DEAL STALLS",
     "Talks overrun with no agreement yet on phasing out fossil fuels."),
    ("EUROPE", "RARE EU-UK SUMMIT SEALS TRADE AND CARBON PACT",
     "London and Brussels agree on trade, carbon pricing and youth mobility."),
    ("TECH", "US CLEARS 900,000 AI CHIPS FOR CHINA",
     "Washington approves a six-month flow of advanced AI chips to Chinese buyers."),
]

TAG_COLORS = {
    "ASIA-PACIFIC": TEAL,
    "EUROPE": GOLD,
    "CLIMATE": (120, 200, 110),
    "TECH": (140, 170, 255),
}


def draw_card(draw, x, y, w, h, tag, head, deck, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=PANEL, outline=PANEL_EDGE, width=1)
    draw.rectangle([x, y + 10, x + 5, y + h - 10], fill=accent)
    # tag chip
    tw = draw.textlength(tag, font=F_TAG) + 20
    draw.rounded_rectangle([x + 20, y + 16, x + 20 + tw, y + 44], radius=6,
                           outline=accent, width=1)
    draw.text((x + 30, y + 21), tag, font=F_TAG, fill=accent)
    # headline (up to 2 lines)
    hl = wrap(draw, head, F_HEAD, w - 40)
    hy = y + 56
    for line in hl[:2]:
        draw.text((x + 20, hy), line, font=F_HEAD, fill=WHITE)
        hy += 30
    # deck (up to 2 lines)
    dl = wrap(draw, deck, F_DECK, w - 40)
    dy = hy + 6
    for line in dl[:2]:
        draw.text((x + 20, dy), line, font=F_DECK, fill=MUTED)
        dy += 24


def build():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    for yy in range(H):
        draw.line([(0, yy), (W, yy)], fill=lerp(NAVY_TOP, NAVY_BOT, yy / H))
    # faint dotted grid
    for gx in range(64, W, 96):
        for gy in range(240, H, 96):
            draw.point((gx, gy), fill=(28, 40, 66))
    # frame
    draw.rectangle([24, 24, W - 25, H - 25], outline=GOLD, width=1)
    draw_header(draw)
    # 2 columns x 3 rows of cards
    cw, ch, gap = 432, 196, 32
    x0, y0 = 64, 248
    for i, (tag, head, deck) in enumerate(STORIES):
        cx = x0 + (i % 2) * (cw + gap)
        cy = y0 + (i // 2) * (ch + 24)
        draw_card(draw, cx, cy, cw, ch, tag, head, deck,
                  TAG_COLORS.get(tag, GOLD))
    # footer
    draw.line([64, 934, 960, 934], fill=(58, 74, 110), width=1)
    draw.text((64, 950), "Six stories, one frame  ·  Wire reports, 21 November 2026",
              font=F_FOOT, fill=MUTED)
    draw.text((64, 976), "DUNIA MALAM INI — ZECH", font=F_FOOT, fill=GOLD)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
