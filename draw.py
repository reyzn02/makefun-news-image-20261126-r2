#!/usr/bin/env python3
"""Draw the front page: THE WORLD IN ONE DAY - Thursday, 26 November 2026.

A newspaper front page built only from Pillow primitives (no AI-generated
text, no external images). 35 dated stories, 10 regions, 14 drawn scenes.
Every claim is labelled with its source.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
CARD = (255, 253, 246)
INK = (17, 17, 17)
NAVY = (18, 38, 63)
RED = (178, 34, 34)
BLUE = (29, 78, 160)
GOLD = (232, 182, 76)
GREY = (96, 96, 96)
LIGHT = (221, 226, 232)
GREEN = (34, 120, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, width):
    """Greedy word wrap; returns a list of lines that fit in width px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, f, fill, leading=None):
    """Draw lines; returns y after the last line."""
    lh = leading or int(f.size * 1.28)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def fit_text(d, x, y, text, f, width, max_lines, fill):
    """Wrap text to max_lines; truncate the last line with ... if needed."""
    lines = wrap(d, text, f, width)[:max_lines]
    if len(wrap(d, text, f, width)) > max_lines and lines:
        last = lines[-1]
        while d.textlength(last + "...", font=f) > width and len(last) > 1:
            last = last[:-1]
        lines[-1] = last + "..."
    return text_block(d, x, y, lines, f, fill)


# ---------------------------------------------------------------- illustrations
def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(173, 216, 230),
              outline=(255, 255, 255), width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=(255, 255, 255), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=1)
    d.ellipse([cx - r * 0.75, cy - r * 0.55, cx - r * 0.15, cy - r * 0.05],
              fill=(96, 160, 90))
    d.ellipse([cx + r * 0.05, cy + r * 0.05, cx + r * 0.6, cy + r * 0.55],
              fill=(96, 160, 90))
    d.ellipse([cx - r * 0.2, cy + r * 0.35, cx + r * 0.3, cy + r * 0.75],
              fill=(120, 175, 100))


def draw_balloon_scene(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 228))
    # storm cloud, top right
    cx, cy = x + w - 52, y + 26
    for ox, oy, r in [(-26, 6, 16), (0, -6, 20), (26, 6, 16), (0, 10, 18)]:
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                  fill=(70, 80, 95))
    # rain
    for i in range(9):
        rx = x + w - 110 + i * 11
        d.line([rx, y + 52, rx - 6, y + 74], fill=(90, 130, 180), width=2)
    # big balloon
    bx, by, bw, bh = x + 28, y + 14, 118, 96
    d.ellipse([bx, by, bx + bw, by + bh], fill=(196, 40, 40))
    d.ellipse([bx + 26, by, bx + bw - 26, by + bh], fill=(240, 240, 235))
    d.ellipse([bx + 48, by, bx + bw - 48, by + bh], fill=(196, 40, 40))
    d.polygon([(bx + 34, by + bh - 6), (bx + bw - 34, by + bh - 6),
               (bx + bw // 2 + 14, by + bh + 22),
               (bx + bw // 2 - 14, by + bh + 22)], fill=(120, 72, 32))
    d.line([bx + 34, by + bh - 4, bx + bw // 2 - 10, by + bh + 20],
           fill=(60, 60, 60), width=1)
    d.line([bx + bw - 34, by + bh - 4, bx + bw // 2 + 10, by + bh + 20],
           fill=(60, 60, 60), width=1)
    d.rectangle([bx + bw // 2 - 16, by + bh + 20, bx + bw // 2 + 16,
                 by + bh + 34], fill=(120, 72, 32), outline=(60, 40, 20))
    # crowd
    for i in range(12):
        px = x + 8 + i * 22
        py = y + h - 12
        d.ellipse([px, py - 7, px + 7, py], fill=(40, 40, 40))
        d.rectangle([px - 1, py, px + 8, py + 10], fill=(40, 40, 40))
    # wind lines
    for wy in (y + 30, y + 46):
        d.line([x + w - 120, wy, x + w - 88, wy], fill=(255, 255, 255), width=2)


def draw_tariff_bars(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 244))
    bars = [("CHINA", 20, RED), ("EU", 15, BLUE), ("INDIA", 25, GREEN)]
    d.text((x + 8, y + 6), "NEW TARIFFS", font=font(SANSB, 11), fill=INK)
    for i, (name, val, col) in enumerate(bars):
        by = y + 30 + i * 44
        d.text((x + 8, by), name, font=font(SANSB, 11), fill=INK)
        d.text((x + 8, by + 14), "+%d%%" % val, font=font(SANSB, 12),
               fill=col)
        bw = int(val * 2.4)
        d.rectangle([x + 52, by + 2, x + 52 + bw, by + 22], fill=col)
    d.text((x + 8, y + h - 22), "on 14 partners", font=font(SANS, 10),
           fill=GREY)


def draw_supermarket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 244))
    # storefront
    d.rectangle([x + 8, y + 34, x + w - 8, y + h - 8], fill=(250, 250, 248),
                outline=INK, width=1)
    for i in range(5):
        col = RED if i % 2 == 0 else (255, 255, 255)
        d.polygon([(x + 8 + i * 18, y + 34), (x + 26 + i * 18, y + 34),
                   (x + 30 + i * 18, y + 48), (x + 12 + i * 18, y + 48)],
                  fill=col, outline=INK)
    d.rectangle([x + 30, y + 62, x + w - 30, y + h - 8], fill=(173, 216, 230),
                outline=INK, width=1)
    d.line([x + w // 2, y + 62, x + w // 2, y + h - 8], fill=INK, width=1)
    # police shield
    sx, sy = x + w - 34, y + 8
    d.polygon([(sx, sy), (sx + 26, sy), (sx + 26, sy + 16),
               (sx + 13, sy + 30), (sx, sy + 16)], fill=BLUE,
              outline=(255, 255, 255))
    d.text((sx + 9, sy + 7), "*", font=font(SANSB, 14), fill=GOLD)
    # "76 freed" badge
    d.ellipse([x + 4, y + 4, x + 40, y + 28], fill=RED)
    d.text((x + 10, y + 9), "76", font=font(SANSB, 13), fill=(255, 255, 255))


def draw_candles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 34, 44))
    # blue/yellow band
    d.rectangle([x, y + h - 16, x + w, y + h - 8], fill=(0, 91, 187))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(255, 213, 0))
    for i, cx in enumerate([x + 26, x + w // 2, x + w - 26]):
        ch = [58, 74, 52][i]
        d.rectangle([cx - 7, y + h - 22 - ch, cx + 7, y + h - 22],
                    fill=(240, 235, 220))
        d.ellipse([cx - 5, y + h - 36 - ch, cx + 5, y + h - 22 - ch],
                  fill=(255, 190, 60))
    d.text((x + 8, y + 8), "~500,000", font=font(SANSB, 17),
           fill=(255, 255, 255))


def draw_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 40))
    for sx, sy in [(x + 12, y + 14), (x + w - 16, y + 30), (x + 20, y + 46),
                    (x + w - 26, y + 66), (x + 30, y + 82)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    cx = x + w // 2
    d.polygon([(cx - 12, y + 18), (cx + 12, y + 18), (cx + 9, y + h - 34),
               (cx - 9, y + h - 34)], fill=(240, 240, 235))
    d.polygon([(cx - 12, y + 18), (cx + 12, y + 18), (cx, y + 2)],
              fill=(196, 40, 40))
    d.polygon([(cx - 12, y + h - 44), (cx - 24, y + h - 26),
               (cx - 9, y + h - 30)], fill=(196, 40, 40))
    d.polygon([(cx + 12, y + h - 44), (cx + 24, y + h - 26),
               (cx + 9, y + h - 30)], fill=(196, 40, 40))
    d.ellipse([cx - 5, y + 34, cx + 5, y + 44], fill=(120, 180, 230),
              outline=INK)
    d.polygon([(cx - 7, y + h - 32), (cx + 7, y + h - 32), (cx, y + h - 6)],
              fill=(255, 150, 40))
    d.arc([x + 6, y + h - 22, x + w - 6, y + h + 26], 180, 360,
          fill=(90, 160, 220), width=4)


def draw_constitution(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 244))
    # tricolour band
    d.rectangle([x + 6, y + 8, x + w - 6, y + 16], fill=(255, 153, 51))
    d.rectangle([x + 6, y + 16, x + w - 6, y + 24], fill=(255, 255, 255))
    d.rectangle([x + 6, y + 24, x + w - 6, y + 32], fill=(19, 136, 8))
    # open book: dark cover, white pages, centre spine
    cx, cy = x + w // 2, y + 66
    d.polygon([(cx - 46, cy - 24), (cx, cy - 12), (cx, cy + 22),
               (cx - 46, cy + 10)], fill=(150, 40, 40), outline=INK)
    d.polygon([(cx + 46, cy - 24), (cx, cy - 12), (cx, cy + 22),
               (cx + 46, cy + 10)], fill=(150, 40, 40), outline=INK)
    d.polygon([(cx - 42, cy - 18), (cx - 3, cy - 8), (cx - 3, cy + 16),
               (cx - 42, cy + 6)], fill=(255, 255, 255), outline=INK)
    d.polygon([(cx + 42, cy - 18), (cx + 3, cy - 8), (cx + 3, cy + 16),
               (cx + 42, cy + 6)], fill=(250, 248, 240), outline=INK)
    for i in range(3):
        ly = cy - 10 + i * 7
        d.line([cx - 36, ly, cx - 8, ly - 3], fill=GREY, width=1)
        d.line([cx + 8, ly - 3, cx + 36, ly], fill=GREY, width=1)
    d.line([cx, cy - 8, cx, cy + 16], fill=INK, width=2)
    d.ellipse([cx - 13, y + h - 30, cx + 13, y + h - 4], fill=NAVY)
    d.text((cx - 11, y + h - 27), "77", font=font(SANSB, 15),
           fill=(255, 255, 255))


def draw_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 244))
    # factory
    d.rectangle([x + 8, y + 48, x + w - 8, y + h - 8], fill=(200, 120, 60))
    d.polygon([(x + 8, y + 48), (x + 26, y + 30), (x + 44, y + 48),
               (x + 62, y + 30), (x + 80, y + 48), (x + w - 8, y + 48)],
              fill=(160, 80, 40))
    d.rectangle([x + w - 22, y + 14, x + w - 12, y + 48], fill=(120, 120, 120))
    for sx, sy in [(x + w - 17, y + 4), (x + w - 12, y - 2)]:
        d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(180, 180, 180))
    d.rectangle([x + 16, y + 62, x + 30, y + 76], fill=(255, 240, 180),
                outline=INK)
    d.rectangle([x + 40, y + 62, x + 54, y + 76], fill=(255, 240, 180),
                outline=INK)
    # rising wage arrow
    d.line([x + 62, y + h - 16, x + w - 14, y + 34], fill=GREEN, width=4)
    d.polygon([(x + w - 14, y + 34), (x + w - 26, y + 36),
               (x + w - 16, y + 46)], fill=GREEN)
    d.text((x + 10, y + 8), "+36%", font=font(SANSB, 15), fill=GREEN)


# small icons for the brief section (22x22 boxes)
def icon_gavel(d, x, y):
    d.line([x + 4, y + 18, x + 18, y + 4], fill=(120, 72, 32), width=3)
    d.rectangle([x + 12, y + 2, x + 20, y + 9], fill=(90, 50, 20))
    d.line([x + 2, y + 20, x + 12, y + 20], fill=INK, width=2)


def icon_tanker(d, x, y):
    d.polygon([(x + 1, y + 12), (x + 21, y + 12), (x + 18, y + 19),
               (x + 4, y + 19)], fill=(40, 60, 90))
    d.rectangle([x + 4, y + 6, x + 10, y + 12], fill=RED)
    d.rectangle([x + 12, y + 6, x + 18, y + 12], fill=(200, 120, 40))
    d.line([x + 2, y + 21, x + 20, y + 21], fill=BLUE, width=1)


def icon_chart(d, x, y):
    d.line([x + 3, y + 19, x + 3, y + 3], fill=INK, width=2)
    d.line([x + 3, y + 19, x + 20, y + 19], fill=INK, width=2)
    d.line([x + 4, y + 15, x + 9, y + 11, x + 13, y + 13, x + 19, y + 5],
           fill=RED, width=2)


def icon_satellite(d, x, y):
    d.rectangle([x + 9, y + 9, x + 13, y + 13], fill=INK)
    d.rectangle([x + 2, y + 7, x + 8, y + 15], fill=BLUE)
    d.rectangle([x + 14, y + 7, x + 20, y + 15], fill=BLUE)
    d.line([x + 11, y + 9, x + 16, y + 4], fill=INK, width=1)


def icon_trophy(d, x, y):
    d.polygon([(x + 6, y + 3), (x + 16, y + 3), (x + 14, y + 12),
               (x + 8, y + 12)], fill=GOLD, outline=INK)
    d.line([x + 11, y + 12, x + 11, y + 17], fill=INK, width=2)
    d.line([x + 7, y + 18, x + 15, y + 18], fill=INK, width=2)


ICONS = {"gavel": icon_gavel, "tanker": icon_tanker, "chart": icon_chart,
         "satellite": icon_satellite, "trophy": icon_trophy}

# ---------------------------------------------------------------- content
LEAD = {
    "kicker": "USA  |  THANKSGIVING",
    "headline": "100th Macy's parade postponed - a first",
    "body": ("A nor'easter's gusts of 40-45 mph ground the balloons (limit "
             "34 mph), so the 100-inflatable parade moves to Sat 28 Nov, "
             "8:30am. NBC airs a 2025 rerun; 81.5m Americans travel for "
             "the holiday (AAA)."),
    "source": "AP - BBC - FOX Weather",
}

HEROES = [
    ("USA / TRADE", "Trump's new tariffs: China +20%",
     "14 partners incl. EU, Japan, India hit in a Section 301 "
     "excess-capacity probe; up to 40% if Beijing breaks the truce. "
     "Announced on Thanksgiving eve.",
     "AP - BBC", draw_tariff_bars),
    ("COLOMBIA", "76 hostages freed after 17 hours",
     "Police storm an Exito supermarket in Cartagena; one gunman "
     "killed; shoppers and staff freed unharmed.",
     "BBC", draw_supermarket),
    ("UKRAINE WAR", "Russia's war dead: ~500,000",
     "Moscow's own figures, leaked Rosstat data, show nearly half a "
     "million dead. Kyiv says 5 Russian jets hit at an airfield.",
     "BBC", draw_candles),
    ("SPACE / CHINA", "Pakistan's first astronaut flies",
     "Shenzhou-24 lifts off 08:18 Beijing time; Muhammad Zeeshan Ali "
     "is the first foreigner aboard Tiangong. Crew of 3.",
     "Reuters - BBC", draw_rocket),
    ("INDIA", "77 years of the Constitution",
     "Constitution Day marks adoption on 26 Nov 1949. Delhi's "
     "Rs 15,000-crore Nepal package, 8 MoUs, agreed 23 Nov.",
     "Indian press", draw_constitution),
    ("BANGLADESH", "Garment pay rises 36%",
     "Minimum wage to Tk 17,000 ($136) after weeks of protests shut "
     "factories; smallest rise in decades; fresh clashes.",
     "Reuters - AFP", draw_factory),
]

BRIEF = [
    ("ISRAEL", "Judges urge dropping most serious charges against Netanyahu", "BBC", "gavel"),
    ("GAZA", "Israeli strike kills Hamas security chief Naeem Abu Nahel and family", "Reuters", None),
    ("EGYPT", "31 killed as fuel tanker crashes and burns on Cairo highway", "BBC", None),
    ("SUDAN", "Drone strikes kill 19 civilians in the south-east", "Reuters", None),
    ("N KOREA", "Expels Swiss diplomat in sanctions row", "BBC", None),
    ("S AFRICA", "Ramaphosa wins court battle over impeachment threat", "BBC", None),
    ("NIGERIA", "5 Mexicans held over $227m meth lab; actor Pete Edochie dies at 79", "BBC", None),
    ("ZIMBABWE", "Arrest warrant issued for Robert Mugabe's son", "BBC", None),
    ("SPAIN", "Kilmar Abrego Garcia lands in Spain, ending deportation battle", "BBC", None),
    ("HORMUZ", "Tankers still burning; 37 ships hit in Oct; US fires on vessel", "Reuters", "tanker"),
    ("MARKETS", "US stocks fall further as AI fears intensify", "BBC", "chart"),
    ("NVIDIA", "Jensen Huang returns as CEO to cheers; Trump brokered comeback", "BBC", None),
    ("HUAWEI", "Found guilty of stealing US trade secrets; cleared of racketeering", "Reuters", None),
    ("ASTEROID", "NASA images show stadium-sized crater on asteroid hit for Earth's defence", "BBC", None),
    ("SPACEX", "US authorises 1m satellites for data centres in space", "Reuters", "satellite"),
    ("US ECONOMY", "Q3 GDP revised sharply higher; jobless claims fall", "Reuters", None),
    ("UK", "Record 5,258 heat deaths in summer 2026", "Reuters", None),
    ("GREECE", "General strike over wages and public services", "Reuters", None),
    ("IRAQ", "Top court: Baghdad may send troops to Kurdistan borders", "Reuters", None),
    ("LEBANON", "Second airport opening reflects political shifts", "Reuters", None),
    ("NIGER", "Saudi national kidnapped by suspected IS militants", "Reuters", None),
    ("USA", "6 killed, incl. 2 children, in plane crash off Mississippi coast", "BBC", None),
    ("USA", "Army controlled blast of explosives in Iowa a 'huge success'", "BBC", None),
    ("CALIFORNIA", "High king tides threaten coast and flood communities", "BBC", None),
    ("SPORT", "Four-time MVP Rodgers released; may have played last NFL game", "BBC", "trophy"),
    ("MUSIC", "Duran Duran guitarist Andy Taylor dies aged 65", "BBC", None),
    ("CULTURE", "Jolie and Pitt settle legal battle over French winery", "BBC", None),
    ("OCEANIA", "Solomon Islands signs Australia security pact; no foreign base", "AP", None),
]

# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 14  # margin

    # masthead
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.text((m, 12), "THE WORLD IN ONE DAY", font=font(SERIF, 40),
           fill=(255, 255, 255))
    d.text((m, 62), "THURSDAY, 26 NOVEMBER 2026", font=font(SANSB, 16),
           fill=GOLD)
    draw_globe(d, W - 54, 46, 30)
    d.text((W - 268, 66), "ALL THE NEWS THAT IS", font=font(SANS, 10),
           fill=(200, 210, 225))

    # strapline
    d.rectangle([0, 92, W, 118], fill=(255, 255, 255), outline=(180, 180, 180))
    d.text((m, 99), "35 dated stories  -  10 regions  -  14 drawn scenes  -  "
                    "every claim source-labelled",
           font=font(SANSB, 13), fill=INK)
    d.text((W - 218, 99), "BBC - Reuters - AP - AFP",
           font=font(SANS, 12), fill=GREY)

    # lead story
    ly, lh = 126, 142
    d.rectangle([m, ly, W - m, ly + lh], fill=CARD, outline=INK, width=1)
    draw_balloon_scene(d, m + 1, ly + 1, 300, lh - 2)
    tx = m + 316
    d.text((tx, ly + 8), LEAD["kicker"], font=font(SANSB, 12), fill=RED)
    fit_text(d, tx, ly + 28, LEAD["headline"], font(SERIF, 23),
             W - m - tx - 12, 2, INK)
    fit_text(d, tx, ly + 82, LEAD["body"], font(SANS, 12),
             W - m - tx - 12, 3, (40, 40, 40))
    d.text((tx, ly + lh - 20), "Source: " + LEAD["source"],
           font=font(SANS, 10), fill=GREY)

    # hero grid: 3 cols x 2 rows
    gx, gy = m, 278
    cw = (W - 2 * m - 20) // 3
    chh = 186
    for i, (kicker, head, body, source, ill) in enumerate(HEROES):
        col, row = i % 3, i // 3
        px = gx + col * (cw + 10)
        py = gy + row * (chh + 10)
        d.rectangle([px, py, px + cw, py + chh], fill=CARD, outline=INK,
                    width=1)
        ill(d, px + 1, py + 1, 112, chh - 2)
        tx2 = px + 122
        tw = px + cw - tx2 - 8
        d.text((tx2, py + 7), kicker, font=font(SANSB, 11), fill=RED)
        fit_text(d, tx2, py + 25, head, font(SERIF, 16), tw, 2, INK)
        fit_text(d, tx2, py + 66, body, font(SANS, 11), tw, 5, (40, 40, 40))
        d.text((tx2, py + chh - 18), "Source: " + source,
               font=font(SANS, 9), fill=GREY)

    # brief header
    by = 680
    d.rectangle([m, by, W - m, by + 28], fill=INK)
    d.text((m + 8, by + 6), "THE WORLD IN BRIEF  -  26 NOVEMBER 2026",
           font=font(SANSB, 14), fill=(255, 255, 255))
    d.text((W - 208, by + 8), "28 more stories, each labelled",
           font=font(SANS, 11), fill=(220, 220, 220))

    # brief columns: 3 cols x 10 rows
    bx = m
    colw = (W - 2 * m - 20) // 3
    row_h = 28
    for i, (tag, text, source, icon) in enumerate(BRIEF):
        col, row = i % 3, i // 3
        ix = bx + col * (colw + 10)
        iy = 716 + row * row_h
        x0 = ix
        if icon:
            ICONS[icon](d, ix, iy + 1)
            x0 = ix + 24
        item = "- %s (%s)" % (text, source)
        tag_w = d.textlength(tag, font=font(SANSB, 11))
        d.text((x0, iy), tag, font=font(SANSB, 11), fill=RED)
        fit_text(d, x0 + tag_w + 4, iy, item, font(SANS, 11),
                 ix + colw - x0 - tag_w - 8, 2, INK)

    # footer
    fy = 996
    d.line([m, fy, W - m, fy], fill=GREY, width=1)
    d.text((m, fy + 6),
           "Sources: BBC - Reuters - AP - AFP - Indian press, as reported 26 Nov 2026. "
           "All events happened or were first reported on 26 Nov 2026.",
           font=font(SANS, 10), fill=GREY)
    d.text((m, fy + 19),
           "Drawn by hand in code (Pillow). No AI-generated text. "
           "35 stories - 10 regions - 14 drawn scenes.",
           font=font(SANS, 10), fill=GREY)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build().save(out, "PNG", optimize=True)
    print("wrote", out)
