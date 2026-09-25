#!/usr/bin/env python3
"""Regenerate assets/og.png — the 1200x630 card link previews show.

    python3 assets/make_og.py

Pillow only; fonts come from the system. Re-run after changing the tagline.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
CANVAS = (246, 243, 238)
INK = (21, 27, 40)
INK_SOFT = (85, 96, 122)
BRAND = (31, 122, 99)
AMBER = (201, 117, 42)
DV = (199, 89, 51)
TB = (46, 107, 217)

OUT = Path(__file__).resolve().parent / "og.png"

def font(names, size):
    for name in names:
        for folder in ("/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/", "/Library/Fonts/"):
            path = Path(folder) / name
            if path.exists():
                return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()

display_b = font(["Georgia Bold.ttf", "Georgia.ttf", "Times New Roman Bold.ttf"], 66)
wordmark = font(["Georgia Bold.ttf", "Georgia.ttf", "Times New Roman Bold.ttf"], 60)
sans_b = font(["Helvetica.ttc", "Arial Bold.ttf", "Arial.ttf"], 30)
sans = font(["Helvetica.ttc", "Arial.ttf"], 27)

img = Image.new("RGB", (W, H), CANVAS)
d = ImageDraw.Draw(img)

# warm wash behind the houses
d.rounded_rectangle([724, 214, 1146, 520], 36, fill=(239, 234, 226))

def house(x, base, w, h, roof_colour, lit=True):
    d.rectangle([x, base - h, x + w, base], fill=(255, 255, 255), outline=(216, 210, 200), width=3)
    d.polygon([(x - 18, base - h), (x + w / 2, base - h - 62), (x + w + 18, base - h)], fill=roof_colour)
    if lit:
        pane = 40
        gap = (w - 2 * pane) / 3
        for i in range(2):
            wx = x + gap + i * (pane + gap)
            d.rounded_rectangle([wx, base - h + 28, wx + pane, base - h + 68], 8, fill=(255, 215, 154))

house(772, 466, 128, 104, DV)
house(936, 466, 112, 86, TB)
# the one still going up
d.rectangle([1076, 392, 1126, 466], outline=(190, 184, 174), width=3)
for y in (412, 444):
    d.line([1066, y, 1136, y], fill=AMBER, width=6)
d.line([1066, 466, 1066, 384], fill=AMBER, width=6)
d.line([1136, 466, 1136, 384], fill=AMBER, width=6)
d.line([64, 552, 1136, 552], fill=(216, 210, 200), width=3)

# mark
d.rounded_rectangle([64, 70, 136, 142], 20, fill=BRAND)
d.polygon([(78, 108), (100, 90), (122, 108)], fill=(255, 215, 154))
d.rectangle([84, 108, 116, 130], fill=(255, 255, 255))

d.text((156, 88), "NeighbourDev", font=wordmark, fill=INK)
# Headline auto-fits the column left of the illustration, so wording can change freely.
HEADLINE = [("Small apps for the", INK), ("everyday, built by the", INK), ("developer next door.", BRAND)]
size = 66
while size > 34:
    f = font(["Georgia Bold.ttf", "Georgia.ttf", "Times New Roman Bold.ttf"], size)
    if max(d.textlength(line, font=f) for line, _ in HEADLINE) <= 620:
        break
    size -= 2
y = 226
for line, colour in HEADLINE:
    d.text((64, y), line, font=f, fill=colour)
    y += size + 12
d.text((64, 474), "Dream Villa  ·  Tilt Ball  ·  more on the way", font=sans, fill=INK_SOFT)
d.text((64, 512), "apps by P R Abinayaa", font=sans, fill=INK_SOFT)
d.text((64, 572), "neighbourdev.com", font=sans_b, fill=BRAND)

img.save(OUT)
print("wrote", OUT)
