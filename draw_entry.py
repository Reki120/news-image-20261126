#!/usr/bin/env python3
"""Draw entry.png: a 1024x1024 news summary for 26 November 2026."""
from PIL import Image, ImageDraw, ImageFont
import math
import os

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


BG = (245, 247, 250)
INK = (24, 32, 48)
MUTED = (90, 102, 122)
CARD = (255, 255, 255)
BORDER = (205, 214, 228)
RED = (205, 44, 38)
ORANGE = (242, 120, 32)
YELLOW = (250, 190, 40)
BLUE = (36, 98, 190)
TEAL = (18, 140, 140)
PURPLE = (110, 70, 170)
GREEN = (38, 150, 80)
DARK = (40, 48, 64)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def text_center(cx, y, s, f, fill=INK):
    d.text((cx, y), s, font=f, fill=fill, anchor="ma")


def wrap(s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def panel(x, y, w, h, accent):
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=CARD, outline=BORDER, width=3)
    d.rounded_rectangle([x, y, x + w, y + 14], radius=7, fill=accent)


def label_block(cx, y, title, sub, tw, tsize=34, ssize=25):
    tf = font(tsize)
    sf = font(ssize, bold=False)
    yy = y
    for line in wrap(title, tf, tw):
        text_center(cx, yy, line, tf)
        yy += tsize + 6
    for line in wrap(sub, sf, tw):
        text_center(cx, yy, line, sf, fill=MUTED)
        yy += ssize + 4
    return yy


# ---------- header ----------
text_center(W // 2, 26, "26 November 2026", font(64))
text_center(W // 2, 102, "The day in world news", font(30, bold=False), fill=MUTED)

# ---------- lead panel: Giza tanker fire ----------
lx, ly, lw, lh = 40, 150, 944, 330
panel(lx, ly, lw, lh, RED)
# flames behind tanker
for fx, fh, col in [(210, 150, ORANGE), (300, 190, RED), (400, 160, ORANGE), (490, 200, RED), (580, 150, ORANGE)]:
    d.polygon([(fx - 42, ly + 230), (fx, ly + 230 - fh), (fx + 42, ly + 230)], fill=col)
    d.polygon([(fx - 22, ly + 230), (fx, ly + 230 - fh * 0.6), (fx + 22, ly + 230)], fill=YELLOW)
# tanker body
tx, ty = 170, ly + 205
d.rounded_rectangle([tx, ty, tx + 430, ty + 78], radius=36, fill=(225, 232, 240), outline=DARK, width=5)
d.rectangle([tx + 430, ty + 18, tx + 505, ty + 78], fill=BLUE, outline=DARK, width=5)
d.rectangle([tx + 455, ty + 30, tx + 492, ty + 52], fill=(190, 220, 245))
for wx in (tx + 70, tx + 330, tx + 465):
    d.ellipse([wx - 26, ty + 66, wx + 26, ty + 118], fill=DARK)
    d.ellipse([wx - 11, ty + 81, wx + 11, ty + 103], fill=(200, 208, 220))
# smoke
for sx, sy, sr in [(250, ly + 70, 30), (330, ly + 55, 38), (430, ly + 68, 32), (520, ly + 52, 26)]:
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 158, 170))
label_block(790, ly + 60, "Giza tanker fire", "31 dead in Egypt", 340, tsize=42, ssize=30)
text_center(790, ly + 250, "EGYPT", font(24), fill=RED)

# ---------- four panels ----------
pw, ph = 462, 232
px = [40, 522]
py = [500, 752]

# Dow Jones
x, y = px[0], py[0]
panel(x, y, pw, ph, GREEN)
gx0, gy0, gx1, gy1 = x + 40, y + 150, x + 250, y + 55
d.line([gx0, gy0, gx1, gy0], fill=BORDER, width=3)
pts = [(gx0, gy0 - 10), (gx0 + 55, gy0 - 35), (gx0 + 110, gy0 - 28), (gx0 + 165, gy0 - 70), (gx1, gy1)]
d.line(pts, fill=GREEN, width=8)
d.polygon([(gx1, gy1), (gx1 - 26, gy1 + 2), (gx1 - 6, gy1 + 24)], fill=GREEN)
label_block(x + 350, y + 55, "Dow 50,000", "first time ever", 200, tsize=36, ssize=25)

# Macy's parade postponed
x, y = px[1], py[0]
panel(x, y, pw, ph, PURPLE)
bx, by = x + 130, y + 95
d.ellipse([bx - 62, by - 62, bx + 62, by + 62], fill=PURPLE)
d.polygon([(bx - 12, by + 60), (bx + 12, by + 60), (bx, by + 82)], fill=PURPLE)
d.line([bx, by + 82, bx, by + 130], fill=DARK, width=4)
# storm cloud + rain
cx0, cy0 = x + 120, y + 45
for ox, oy, r in [(-45, 8, 30), (0, -6, 38), (45, 8, 30)]:
    d.ellipse([cx0 + ox - r, cy0 + oy - r, cx0 + ox + r, cy0 + oy + r], fill=(120, 130, 148))
for rx in (-40, -10, 20, 50):
    d.line([cx0 + rx, cy0 + 38, cx0 + rx - 10, cy0 + 62], fill=BLUE, width=5)
label_block(x + 340, y + 45, "Macy's parade", "100th, postponed by storm", 220, tsize=34, ssize=24)

# FedEx jet off runway
x, y = px[0], py[1]
panel(x, y, pw, ph, ORANGE)
# runway
d.rectangle([x + 30, y + 150, x + 270, y + 180], fill=(70, 78, 92))
for i in range(5):
    d.rectangle([x + 45 + i * 48, y + 161, x + 75 + i * 48, y + 169], fill=(240, 244, 248))
# tilted jet
jx, jy = x + 48, y + 95
d.polygon([(jx, jy + 25), (jx + 170, jy - 12), (jx + 205, jy + 2), (jx + 60, jy + 48)], fill=(225, 232, 240), outline=DARK, width=4)
d.polygon([(jx + 95, jy + 18), (jx + 140, jy - 38), (jx + 160, jy - 30), (jx + 130, jy + 20)], fill=BLUE)
d.polygon([(jx + 8, jy + 22), (jx - 12, jy - 18), (jx + 16, jy - 14), (jx + 30, jy + 24)], fill=PURPLE)
d.ellipse([jx + 178, jy - 6, jx + 198, jy + 12], fill=(190, 220, 245))
label_block(x + 360, y + 50, "FedEx jet", "off runway in Miami", 190, tsize=36, ssize=25)

# EU tech fund
x, y = px[1], py[1]
panel(x, y, pw, ph, BLUE)
ex, ey, er = x + 120, y + 110, 62
d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=BLUE)
for i in range(12):
    a = math.radians(i * 30)
    sx, sy = ex + 42 * math.cos(a), ey + 42 * math.sin(a)
    d.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=YELLOW)
text_center(ex, ey - 22, "EU", font(34), fill=(255, 255, 255))
label_block(x + 340, y + 50, "EU tech fund", "€50 billion planned", 220, tsize=36, ssize=25)

img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}, {os.path.getsize(OUT)} bytes")
